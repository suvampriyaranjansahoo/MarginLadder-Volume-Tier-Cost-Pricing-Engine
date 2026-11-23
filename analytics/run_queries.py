"""Run analytics/queries.sql on the cycle-time log and write docs/analytics/sql_findings.md.

Usage:  python3 -m analytics.run_queries [csv_path]
The default input is the SIMULATED log. Every reading below is generated from the query output,
so the text changes when the data changes.
"""
from __future__ import annotations

import csv
import re
import sqlite3
import sys
from pathlib import Path

from tracekit.analyze import parse_row, read_csv as read_trace_csv, stage_days, stage_observations

ROOT = Path(__file__).resolve().parents[1]
SQL = Path(__file__).with_name("queries.sql")
DEFAULT_CSV = ROOT / "data" / "simulated_rfq_log.csv"
OUT = ROOT / "docs" / "analytics" / "sql_findings.md"
COLUMNS = {"RFQ": "rfq", "Intake wait": "intake", "Costing": "costing", "Routing check wait": "routing",
           "Approval wait": "approval", "Send and rework": "send", "Total days": "total"}


def _rows_from_trace(csv_path: Path) -> list[tuple[str, float, float, float, float, float, float, float]]:
    """Convert raw event timestamps into the stable SQL cycle schema.

    Incomplete stage pairs are rejected rather than silently converted to zero. Routing
    and approval may be explicitly not applicable (both timestamps blank). Customer
    hold is stored as a separate, non-additive overlay because it can overlap elapsed
    residual time.
    """
    converted = []
    for raw in read_trace_csv(csv_path):
        row = parse_row(raw)
        stages = stage_days(row)
        if stages is None:
            continue  # Open / unsent RFQs do not have a completed cycle duration.
        observed = stage_observations(row)
        missing = [name for name, ok in observed.items() if not ok]
        if missing:
            raise ValueError(
                f"RFQ {row.ref}: incomplete timestamps for {', '.join(missing)}; "
                "complete the trace before stage-level SQL analysis."
            )
        intake = stages["intake_wait"] + stages["queue_before_costing"]
        converted.append((
            row.ref, intake, stages["costing"], stages["routing_wait"],
            stages["approval_wait"], stages["send_and_other"], stages["total"], row.hold_days,
        ))
    return converted


def load(csv_path: Path) -> sqlite3.Connection:
    """Load a trace into an in-memory SQL connection. Caller owns a successful result.

    Any parse, validation or insert failure closes the connection before propagating
    the exception, so rejected input cannot leak an in-memory SQLite handle.
    """
    con = sqlite3.connect(":memory:")
    try:
        con.execute("""CREATE TABLE cycle(
            rfq TEXT, intake REAL, costing REAL, routing REAL, approval REAL,
            send REAL, total REAL, customer_hold REAL NOT NULL DEFAULT 0
        )""")
        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = set(reader.fieldnames or ())
            if "RFQ" in fieldnames:
                rows = [(
                    r["RFQ"], *(float(r[c]) for c in list(COLUMNS)[1:]),
                    float(r.get("Customer hold days") or r.get("customer_hold_days") or 0),
                ) for r in reader]
            elif "rfq_ref" in fieldnames:
                rows = _rows_from_trace(csv_path)
            else:
                raise ValueError(
                    "CSV must use either the SQL cycle schema (RFQ, Intake wait, ...) "
                    "or the raw trace schema (rfq_ref, received_at, ...)."
                )
        con.executemany("INSERT INTO cycle VALUES(?,?,?,?,?,?,?,?)", rows)
        return con
    except Exception:
        con.close()
        raise


def queries() -> dict[str, str]:
    text = SQL.read_text(encoding="utf-8")
    parts = re.split(r"^-- name: (\w+)\s*$", text, flags=re.M)
    return {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}


def run(con: sqlite3.Connection) -> dict[str, tuple[list[str], list[tuple]]]:
    out = {}
    for name, sql in queries().items():
        cur = con.execute(sql)
        out[name] = ([d[0] for d in cur.description], cur.fetchall())
    return out


def md_table(cols: list[str], rows: list[tuple]) -> str:
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    lines += ["| " + " | ".join(str(v) for v in r) + " |" for r in rows]
    return "\n".join(lines)


def readings(res: dict[str, tuple[list[str], list[tuple]]], n: int) -> dict[str, str]:
    pct = {r[0]: r[2] for r in res["stage_share"][1]}
    top = res["stage_share"][1][0]
    var = {r[0]: r[1] for r in res["variance_drivers"][1]}
    top_var = res["variance_drivers"][1][0]
    pcts = {r[0]: r[1] for r in res["percentiles"][1]}
    buckets = {r[0][3:]: r[1] for r in res["aging_buckets"][1]}
    within = next((r for r in res["aging_buckets"][1] if r[0].startswith("1.")), None)
    breach, _, share = res["costing_over_40pct"][1][0]
    wi = res["what_if"][1]
    return {
        "percentiles": f"Median {pcts['median']} days and 90th percentile {pcts['p90']} days, against a 4-day target. Report both: the average hides the long tail.",
        "stage_share": f"{top[0]} is the largest block at {top[2]}% of elapsed time. Timestamp-derived costing is {pct['Costing']}%; the brief-only hands-on arithmetic is about 17.3% of a 9-day cycle (1.56 of 9 days), so compare only after checking trace completeness and definitions.",
        "largest_stage_per_rfq": f"{res['largest_stage_per_rfq'][1][0][0]} is the single longest stage on {res['largest_stage_per_rfq'][1][0][1]} of {n} RFQs. No one stage is the longest everywhere, so one fix will not close the gap.",
        "variance_drivers": f"{top_var[0]} explains {top_var[1]}% of why some RFQs take far longer than others. Costing explains {var['Costing']}%. Fixing the stage that drives the spread matters more than fixing the average.",
        "aging_buckets": f"{within[1] if within else 0} of {n} RFQs meet the 4-day target today. {buckets.get('over 10 days', 0)} take more than 10 days.",
        "costing_over_40pct": (f"Costing is above 40% of the cycle on {breach} of {n} RFQs. Across all RFQs it is {share}% of total time, "
                               + ("so the cut-scope rule does not trigger on this data." if share <= 40 else "so the cut-scope rule triggers on this data.")),
        "what_if": (f"The 4-day rate goes {wi[0][4]}% today, {wi[1][4]}% with faster costing (A), {wi[2][4]}% with the approval cap added (B), "
                    f"{wi[3][4]}% with intake and routing caps added (C). "
                    + ("Faster costing alone does not reach the target; the waiting stages have to shrink too. " if wi[1][4] < 50 else "")
                    + "I chose the caps, so this shows what has to be true for the target to be met, not that it will be."),
        "customer_hold_overlay": (
            f"Customer hold averages {res['customer_hold_overlay'][1][0][1]} days per completed RFQ "
            f"and is present on {res['customer_hold_overlay'][1][0][2]} of {n}. It is a non-additive overlay; "
            "do not add it to the stage stack because it may overlap residual elapsed time."
        ),
    }


def main(argv: list[str]) -> int:
    csv_path = Path(argv[1]) if len(argv) > 1 else DEFAULT_CSV
    con = load(csv_path)
    try:
        n = con.execute("SELECT COUNT(*) FROM cycle").fetchone()[0]
        res = run(con)
        read = readings(res, n)
    finally:
        con.close()
    simulated = csv_path.resolve() == DEFAULT_CSV.resolve()
    is_template = csv_path.name == "rfq_trace_template.csv"
    titles = {"percentiles": "Median and 90th percentile", "stage_share": "Where the days go",
              "largest_stage_per_rfq": "Longest stage per RFQ", "variance_drivers": "What drives the spread",
              "aging_buckets": "Ageing buckets", "costing_over_40pct": "The 40% costing rule",
              "what_if": "What if: three assumed changes", "customer_hold_overlay": "Customer holds (separate overlay)"}
    doc = ["# SQL findings: cycle-time analysis", "",
           ("> **Data: SIMULATED** (`data/simulated_rfq_log.csv`, 60 rows from assumed stage means). Nothing here is a finding about a real plant. "
            "The queries in `analytics/queries.sql` run unchanged on the Week-1 trace." if simulated else f"> Data: `{csv_path}`."),
           "", "Regenerate with `python3 -m analytics.run_queries`. Each reading below is written from the query output.",
           "For a raw Week-1 trace, pass the timestamp CSV directly; unsent RFQs are excluded from cycle-time SQL and incomplete stage pairs are rejected. Customer holds are an overlay, not an additive stage.", ""]
    for name, (cols, rows) in res.items():
        doc += [f"## {titles[name]}", "", md_table(cols, rows), "", f"**Reading.** {read[name]}", ""]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(doc), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
