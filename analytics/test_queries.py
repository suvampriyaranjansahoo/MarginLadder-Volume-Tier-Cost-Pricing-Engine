import csv
import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from analytics import run_queries as rq
from tracekit.analyze import percentile

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def results():
    con = rq.load(rq.DEFAULT_CSV)
    try:
        yield con, rq.run(con)
    finally:
        con.close()


def test_stage_columns_add_to_total_in_the_log():
    with rq.DEFAULT_CSV.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            parts = sum(float(r[c]) for c in ("Intake wait", "Costing", "Routing check wait", "Approval wait", "Send and rework"))
            assert parts == pytest.approx(float(r["Total days"]), abs=0.011)


def test_sql_percentiles_match_the_python_rule(results):
    con, res = results
    totals = [r[0] for r in con.execute("SELECT total FROM cycle")]
    got = dict(res["percentiles"][1])
    assert got["median"] == pytest.approx(percentile(totals, 0.5), abs=0.006)
    assert got["p90"] == pytest.approx(percentile(totals, 0.9), abs=0.006)


def test_stage_shares_add_to_100(results):
    assert sum(r[2] for r in results[1]["stage_share"][1]) == pytest.approx(100, abs=0.3)


def test_variance_shares_add_to_100(results):
    assert sum(r[1] for r in results[1]["variance_drivers"][1]) == pytest.approx(100, abs=0.3)


def test_every_rfq_has_a_longest_stage(results):
    assert sum(r[1] for r in results[1]["largest_stage_per_rfq"][1]) >= 60


def test_buckets_cover_every_rfq(results):
    assert sum(r[1] for r in results[1]["aging_buckets"][1]) == 60
    assert results[1]["aging_buckets"][1][-1][3] == 100.0


def test_costing_share_is_over_all_rfqs_not_just_breachers(results):
    assert results[1]["costing_over_40pct"][1][0][2] == pytest.approx(17.3, abs=0.2)


def test_what_if_scenarios_never_get_worse(results):
    means = [r[1] for r in results[1]["what_if"][1]]
    assert means == sorted(means, reverse=True)
    within = [r[2] for r in results[1]["what_if"][1]]
    assert within == sorted(within)


def test_findings_file_marks_data_as_simulated():
    rq.main(["x"])
    text = (ROOT / "docs" / "analytics" / "sql_findings.md").read_text(encoding="utf-8")
    assert "SIMULATED" in text and "Approval wait" in text


def test_raw_trace_csv_flows_directly_into_sql_schema():
    from pathlib import Path
    trace_path = Path(__file__).resolve().parents[1] / "tracekit" / "rfq_trace_template.csv"
    with closing(rq.load(trace_path)) as con:
        assert con.execute("SELECT COUNT(*) FROM cycle").fetchone()[0] == 2
        assert con.execute("SELECT COUNT(*) FROM cycle WHERE customer_hold > 0").fetchone()[0] == 1
        assert "customer_hold_overlay" in rq.run(con)


def test_incomplete_raw_trace_pairs_are_rejected_not_zero_filled(tmp_path):
    path = tmp_path / "trace.csv"
    path.write_text(
        "rfq_ref,received_at,assigned_at,costing_start,costing_end,sent_at\n"
        "R1,2026-12-01T09:00,2026-12-01T10:00,,2026-12-02T10:00,2026-12-03T10:00\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="incomplete timestamps"):
        rq.load(path)


def test_failed_trace_load_closes_its_sqlite_connection(tmp_path, monkeypatch):
    path = tmp_path / "bad_trace.csv"
    path.write_text(
        "rfq_ref,received_at,assigned_at,costing_start,costing_end,sent_at\n"
        "R1,2026-12-01T09:00,2026-12-01T10:00,,2026-12-02T10:00,2026-12-03T10:00\n",
        encoding="utf-8",
    )
    original_connect = sqlite3.connect
    opened = []

    def tracked_connect(*args, **kwargs):
        connection = original_connect(*args, **kwargs)
        opened.append(connection)
        return connection

    monkeypatch.setattr(rq.sqlite3, "connect", tracked_connect)
    with pytest.raises(ValueError, match="incomplete timestamps"):
        rq.load(path)
    assert len(opened) == 1
    with pytest.raises(sqlite3.ProgrammingError, match="closed database"):
        opened[0].execute("SELECT 1")


# ---- regression: customer-hold narrative read the wrong result columns (positions 1 and 2 instead of 0 and 1) ----
def _readings_for(tmp_path, holds):
    """Copy the simulated log, set 'Customer hold days' on the first rows, and return the readings text."""
    with rq.DEFAULT_CSV.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for i, row in enumerate(rows):
        row["Customer hold days"] = str(holds[i]) if i < len(holds) else "0"
    path = tmp_path / "with_holds.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    con = rq.load(path)
    try:
        res = rq.run(con)
        n = con.execute("SELECT COUNT(*) FROM cycle").fetchone()[0]
        return rq.readings(res, n)["customer_hold_overlay"], res, n
    finally:
        con.close()


def test_customer_hold_narrative_with_no_holds_says_zero_of_n(tmp_path):
    text, _, n = _readings_for(tmp_path, [])
    assert n == 60
    assert "averages 0.0 days" in text
    assert "present on 0 of 60" in text  # the bug printed "present on 60 of 60"


def test_customer_hold_narrative_uses_mean_and_count_not_neighbouring_columns(tmp_path):
    text, res, n = _readings_for(tmp_path, [2, 1])  # two RFQs on hold, total 3 days over 60 RFQs
    assert "averages 0.05 days" in text
    assert "present on 2 of 60" in text
    cols, rows = res["customer_hold_overlay"]
    assert dict(zip(cols, rows[0], strict=True))["rfqs_with_customer_hold"] == 2
    assert n == 60


def test_customer_hold_narrative_matches_the_sql_table_for_any_input(tmp_path):
    text, res, _ = _readings_for(tmp_path, [0.5, 0, 4, 0, 0, 1.5])
    row = dict(zip(*res["customer_hold_overlay"][:1], res["customer_hold_overlay"][1][0], strict=True))
    assert f"averages {row['mean_customer_hold_days']} days" in text
    assert f"present on {row['rfqs_with_customer_hold']} of {row['completed_rfqs']}" in text
