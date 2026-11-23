from datetime import date, datetime

import pytest

from tracekit.analyze import (TraceError, parse_row, percentile, read_csv, stage_days, summarise,
                           wilson, working_days)

BASE = {"rfq_ref": "T1", "received_at": "2026-12-01T09:00", "assigned_at": "2026-12-01T12:00",
        "costing_start": "2026-12-02T09:00", "costing_end": "2026-12-03T09:00",
        "approval_requested_at": "2026-12-03T10:00", "approval_decided_at": "2026-12-04T10:00",
        "sent_at": "2026-12-04T12:00", "customer_hold_days": "0", "rework_count": "0",
        "outcome": "won", "lost_reason_code": ""}


def row(**over):
    return {**BASE, **over}


def test_working_days_skips_weekend():
    fri = datetime(2026, 12, 4, 12, 0)
    mon = datetime(2026, 12, 7, 12, 0)
    assert working_days(fri, mon) == pytest.approx(1.0)


def test_working_days_skips_listed_holiday():
    a, b = datetime(2026, 12, 24, 0, 0), datetime(2026, 12, 28, 0, 0)
    assert working_days(a, b, frozenset({date(2026, 12, 25)})) == pytest.approx(1.0)


def test_negative_span_is_an_error():
    with pytest.raises(TraceError):
        working_days(datetime(2026, 12, 2), datetime(2026, 12, 1))


def test_stage_days_add_up_to_total():
    s = stage_days(parse_row(row()))
    parts = sum(s[k] for k in ("intake_wait", "queue_before_costing", "costing", "routing_wait",
                               "approval_wait", "send_and_other"))
    assert parts == pytest.approx(s["total"])
    assert s["costing"] == pytest.approx(1.0)
    assert s["approval_wait"] == pytest.approx(1.0)


def test_unsent_rfq_has_no_stage_days():
    assert stage_days(parse_row(row(sent_at=""))) is None


@pytest.mark.parametrize("bad,msg", [
    ({"rfq_ref": ""}, "no rfq_ref"),
    ({"received_at": ""}, "received_at is required"),
    ({"received_at": "yesterday"}, "not an ISO"),
    ({"costing_end": "2026-12-01T10:00"}, "before"),
    ({"outcome": "maybe"}, "outcome must be"),
    ({"lost_reason_code": "price"}, "only valid when outcome is lost"),
    ({"outcome": "lost", "lost_reason_code": "bored"}, "lost_reason_code must be"),
    ({"customer_hold_days": "-1"}, "cannot be negative"),
    ({"rework_count": "x"}, "must be numbers"),
])
def test_bad_rows_are_refused_with_a_reason(bad, msg):
    with pytest.raises(TraceError, match=msg):
        parse_row(row(**bad))


def test_percentile_matches_numpy_rule():
    assert percentile([1, 2, 3, 4], 0.5) == 2.5
    assert percentile([1, 2, 3, 4, 5], 0.9) == pytest.approx(4.6)


def test_wilson_interval_brackets_the_rate():
    lo, hi = wilson(8, 10)
    assert lo < 0.8 < hi and 0 <= lo and hi <= 1
    assert wilson(0, 0) == (0.0, 0.0)


def test_summary_applies_the_costing_cut_rule():
    costing_heavy = row(assigned_at="2026-12-01T09:00", costing_start="2026-12-01T09:00",
                        costing_end="2026-12-03T09:00", approval_requested_at="", approval_decided_at="",
                        sent_at="2026-12-03T10:00")
    out = summarise([costing_heavy, {**costing_heavy, "rfq_ref": "T2"}])
    assert out["sent_rows"] == 2
    assert out["costing_share_of_cycle"] > 0.40
    assert out["rule_costing_only"] is True
    assert summarise([row()])["rule_costing_only"] is False


def test_gate3_needs_twenty_coded_lost_rfqs_and_a_quarter_from_delay():
    lost = [row(rfq_ref=f"L{i}", outcome="lost", lost_reason_code="delay" if i < 5 else "price")
            for i in range(20)]
    assert summarise(lost)["gate3_condition_a"] is True
    assert summarise(lost[:19])["gate3_condition_a"] is False
    few_delay = [row(rfq_ref=f"L{i}", outcome="lost", lost_reason_code="delay" if i < 4 else "price")
                 for i in range(20)]
    assert summarise(few_delay)["gate3_condition_a"] is False


def test_unsent_rows_are_counted_as_missing():
    out = summarise([row(), row(rfq_ref="T2", sent_at="")])
    assert out["missing_sent_rate"] == 0.5


def test_template_file_parses():
    out = summarise(read_csv("tracekit/rfq_trace_template.csv"))
    assert out["rows"] == 2


def test_approval_wait_is_checked_against_the_budget():
    slow = row(approval_requested_at="2026-12-03T10:00", approval_decided_at="2026-12-04T10:00")      # 1 day
    quick = row(rfq_ref="T2", approval_requested_at="", approval_decided_at="")
    out = summarise([slow, quick])
    assert out["share_needing_approval"] == 0.5
    assert out["mean_approval_wait_all_rfqs_days"] == 0.5 and out["approval_within_budget"] is True
    assert summarise([slow, {**slow, "rfq_ref": "T3"}])["approval_within_budget"] is False


def test_offset_aware_timestamps_are_compared_as_instants_in_received_timezone():
    from datetime import datetime
    # Both strings describe the same instant. The old parser stripped offsets and
    # incorrectly manufactured a five-hour difference.
    start = datetime.fromisoformat("2026-12-01T09:00:00+05:30")
    end = datetime.fromisoformat("2026-12-01T03:30:00Z")
    assert working_days(start, end) == pytest.approx(0.0)


def test_parse_row_preserves_zulu_timezone_and_accepts_equivalent_offsets():
    aware = row()
    for field in ("received_at", "assigned_at", "costing_start", "costing_end",
                  "approval_requested_at", "approval_decided_at", "sent_at"):
        aware[field] = aware[field] + ":00+05:30"
    aware["received_at"] = "2026-12-01T09:00:00+05:30"
    aware["assigned_at"] = "2026-12-01T03:30:00Z"
    parsed = parse_row(aware)
    assert parsed.times["received_at"].utcoffset().total_seconds() == 19800
    assert parsed.times["assigned_at"].utcoffset().total_seconds() == 0


def test_mixed_naive_and_aware_timestamps_are_rejected():
    with pytest.raises(TraceError, match="do not mix timezone-aware"):
        parse_row(row(assigned_at="2026-12-01T12:00:00+05:30"))


def test_stage_coverage_does_not_turn_missing_intervals_into_observed_zeroes():
    incomplete = row(assigned_at="", costing_start="", costing_end="")
    out = summarise([incomplete])
    assert out["stage_missing_rate"]["intake_wait"] == 1.0
    assert out["stage_missing_rate"]["costing"] == 1.0
    assert out["complete_stage_rows"] == 0
    assert out["costing_share_of_cycle"] is None
    assert "Insufficient complete" in out["decision"]


def test_hold_is_reported_as_non_additive_overlay():
    out = summarise([row(customer_hold_days="0.5")])
    assert out["mean_customer_hold_days"] == 0.5
    assert out["customer_hold_share_of_cycle_overlay"] > 0
    assert "not an additive stage" in out["customer_hold_note"]


def test_cross_chain_overlap_is_rejected_instead_of_double_counted():
    overlapping = row(
        costing_start="2026-12-02T09:00", costing_end="2026-12-03T09:00",
        approval_requested_at="2026-12-02T12:00", approval_decided_at="2026-12-03T12:00",
        sent_at="2026-12-04T12:00",
    )
    with pytest.raises(TraceError, match="overlapping costing and approval"):
        parse_row(overlapping)


def test_milestone_after_sent_is_rejected():
    with pytest.raises(TraceError, match="after sent_at"):
        parse_row(row(approval_decided_at="2026-12-05T10:00"))
