"""Cycle-time analysis for the Week-1 trace.

Input: one row per RFQ with ISO-8601 timestamps (see rfq_trace_template.csv).
Output: stage durations in working days, median and P90, stage coverage, the complete-case
costing share, the within-4-day rate with a 95% interval, and the two Gate 3 lost-RFQ checks.
Offset-aware timestamps are compared as instants in the received_at timezone. Mixed
naive/aware timestamps are rejected. Missing stages are reported, never silently treated
as observed zeroes for stage-share decisions.

Working days here mean elapsed weekday time divided by 24 hours. Saturdays, Sundays and
any dates passed as holidays count as zero. [Judgement] Confirm the plant calendar in Week 1.
"""
from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from collections.abc import Iterable

TIME_FIELDS = (
    "received_at", "assigned_at", "costing_start", "costing_end",
    "routing_request_at", "routing_cleared_at",
    "approval_requested_at", "approval_decided_at", "sent_at",
)
REQUIRED = ("rfq_ref", "received_at")
OUTCOMES = {"won", "lost", "no_bid", "open", ""}
LOST_REASONS = {"delay", "price", "capacity", "technical", "customer_cancelled", "other", ""}
STAGES = ("intake_wait", "queue_before_costing", "costing", "routing_wait", "approval_wait", "send_and_other")
TARGET_DAYS = 4.0
APPROVAL_BUDGET_DAYS = 0.75      # Judgement, PRD: mean approval wait budget
COSTING_SHARE_CUT = 0.40         # Judgement, PRD: above this, cut scope to costing only
DELAY_SHARE_GATE = 0.25          # Judgement, Gate 3 condition A
MIN_CODED_LOST = 20              # Judgement, Gate 3 condition A


class TraceError(ValueError):
    """A trace row cannot be used. The message says which row and why."""


def working_days(start: datetime, end: datetime, holidays: frozenset[date] = frozenset()) -> float:
    """Elapsed weekday time in the received_at timezone; naive inputs are local wall time.

    Offset-aware inputs are compared as instants, then the end is converted to the start
    timezone before applying the weekday calendar. Mixing naive and aware datetimes is
    rejected because their relationship is unknowable without an explicit timezone.
    """
    start_aware, end_aware = start.utcoffset() is not None, end.utcoffset() is not None
    if start_aware != end_aware:
        raise TraceError("cannot mix timezone-aware and timezone-naive timestamps")
    if start_aware:
        end = end.astimezone(start.tzinfo)
    if end < start:
        raise TraceError(f"end {end.isoformat()} is before start {start.isoformat()}")
    total = 0.0
    day = datetime.combine(start.date(), time.min, tzinfo=start.tzinfo)
    while day <= end:
        nxt = day + timedelta(days=1)
        if day.weekday() < 5 and day.date() not in holidays:
            lo, hi = max(start, day), min(end, nxt)
            if hi > lo:
                total += (hi - lo).total_seconds() / 86400
        day = nxt
    return total


def _parse_time(value: str, field: str, ref: str) -> datetime | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    except ValueError as exc:
        raise TraceError(f"{ref}: {field} '{value}' is not an ISO date-time (YYYY-MM-DDTHH:MM)") from exc
    return parsed


@dataclass
class TraceRow:
    ref: str
    times: dict[str, datetime | None]
    hold_days: float
    rework: int
    outcome: str
    lost_reason: str


def parse_row(raw: dict[str, str]) -> TraceRow:
    ref = (raw.get("rfq_ref") or "").strip()
    if not ref:
        raise TraceError("a row has no rfq_ref")
    times = {f: _parse_time(raw.get(f, ""), f, ref) for f in TIME_FIELDS}
    awareness = {value.utcoffset() is not None for value in times.values() if value is not None}
    if len(awareness) > 1:
        raise TraceError(f"{ref}: do not mix timezone-aware and timezone-naive timestamps")
    if times["received_at"] is None:
        raise TraceError(f"{ref}: received_at is required")
    # All recorded milestones must lie inside the RFQ's observed lifecycle.
    received = times["received_at"]
    sent = times["sent_at"]
    for field, stamp in times.items():
        if stamp is not None and stamp < received:
            raise TraceError(f"{ref}: {field} occurs before received_at")
        if sent is not None and stamp is not None and stamp > sent:
            raise TraceError(f"{ref}: {field} occurs after sent_at")

    chains = (
        ("received_at", "assigned_at", "costing_start", "costing_end", "sent_at"),
        ("routing_request_at", "routing_cleared_at"),
        ("approval_requested_at", "approval_decided_at", "sent_at"),
    )
    for chain in chains:
        present = [(f, v) for f in chain if (v := times[f]) is not None]
        for (fa, a), (fb, b) in zip(present, present[1:], strict=False):
            if b < a:
                raise TraceError(f"{ref}: {fb} is before {fa}")
    # Stage intervals are sequential in this case model. If a real process permits
    # parallel work, it must be represented as concurrent work and not summed as stages.
    intervals = []
    for start_field, end_field, label in (
        ("costing_start", "costing_end", "costing"),
        ("routing_request_at", "routing_cleared_at", "routing"),
        ("approval_requested_at", "approval_decided_at", "approval"),
    ):
        start, end = times[start_field], times[end_field]
        if (start is None) != (end is None):
            raise TraceError(f"{ref}: {label} incomplete timestamps: interval requires both start and end timestamps")
        if start is not None:
            intervals.append((start, end, label))
    intervals.sort(key=lambda item: item[0])
    for previous, current in zip(intervals, intervals[1:], strict=False):
        if previous[1] is not None and current[0] < previous[1]:
            raise TraceError(f"{ref}: overlapping {previous[2]} and {current[2]} intervals")

    try:
        hold = float((raw.get("customer_hold_days") or "0").strip() or 0)
        rework = int(float((raw.get("rework_count") or "0").strip() or 0))
    except ValueError as exc:
        raise TraceError(f"{ref}: customer_hold_days and rework_count must be numbers") from exc
    if hold < 0 or rework < 0:
        raise TraceError(f"{ref}: customer_hold_days and rework_count cannot be negative")
    outcome = (raw.get("outcome") or "").strip().lower()
    reason = (raw.get("lost_reason_code") or "").strip().lower()
    if outcome not in OUTCOMES:
        raise TraceError(f"{ref}: outcome must be one of won, lost, no_bid, open")
    if reason not in LOST_REASONS:
        raise TraceError(f"{ref}: lost_reason_code must be one of {sorted(r for r in LOST_REASONS if r)}")
    if reason and outcome != "lost":
        raise TraceError(f"{ref}: lost_reason_code is only valid when outcome is lost")
    return TraceRow(ref, times, hold, rework, outcome, reason)


def stage_observations(row: TraceRow) -> dict[str, bool]:
    """Whether each stage is genuinely observed rather than silently treated as zero.

    Routing and approval are considered not applicable when both event timestamps are
    absent. The residual stage can only be interpreted when all timestamp pairs are
    observed or explicitly not applicable.
    """
    t = row.times
    def pair_observed(a: str, b: str, optional: bool = False) -> bool:
        left, right = t[a], t[b]
        if optional and left is None and right is None:
            return True
        return left is not None and right is not None
    observed = {
        "intake_wait": pair_observed("received_at", "assigned_at"),
        "queue_before_costing": pair_observed("assigned_at", "costing_start"),
        "costing": pair_observed("costing_start", "costing_end"),
        "routing_wait": pair_observed("routing_request_at", "routing_cleared_at", optional=True),
        "approval_wait": pair_observed("approval_requested_at", "approval_decided_at", optional=True),
    }
    observed["send_and_other"] = all(observed.values()) and t["sent_at"] is not None
    return observed


def stage_days(row: TraceRow, holidays: frozenset[date] = frozenset()) -> dict[str, float] | None:
    """Stage durations in working days, or None if the RFQ has not been sent yet."""
    t = row.times
    received, sent = t["received_at"], t["sent_at"]
    if sent is None or received is None:
        return None
    total = working_days(received, sent, holidays)

    def span(a: str, b: str) -> float:
        start, end = t[a], t[b]
        if start is None or end is None or end < start:
            return 0.0
        return working_days(start, end, holidays)

    out = {
        "intake_wait": span("received_at", "assigned_at"),
        "queue_before_costing": span("assigned_at", "costing_start"),
        "costing": span("costing_start", "costing_end"),
        "routing_wait": span("routing_request_at", "routing_cleared_at"),
        "approval_wait": span("approval_requested_at", "approval_decided_at"),
    }
    residual = total - sum(out.values())
    if residual < -1e-9:
        raise TraceError(f"{row.ref}: observed stage durations exceed end-to-end elapsed time")
    out["send_and_other"] = max(0.0, residual)
    out["total"] = total
    out["total_net_of_hold"] = max(0.0, total - row.hold_days)
    return out


def percentile(values: list[float], q: float) -> float:
    """Linear-interpolation percentile (the same rule as NumPy's default)."""
    if not values:
        raise TraceError("no values")
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    pos = (len(s) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def wilson(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def summarise(raw_rows: Iterable[dict[str, str]], holidays: frozenset[date] = frozenset()) -> dict:
    rows = [parse_row(r) for r in raw_rows]
    stages = [(r, stage_days(r, holidays)) for r in rows]
    done = [(r, s) for r, s in stages if s is not None]
    n, n_done = len(rows), len(done)
    result: dict = {
        "rows": n, "sent_rows": n_done,
        "missing_sent_rate": round(1 - n_done / n, 4) if n else 0.0,
        "caveat": "Working days are elapsed weekday time divided by 24 hours.",
    }
    if not done:
        result["decision"] = "No sent RFQs yet; no cycle-time result."
        return result
    totals = [s["total"] for _, s in done]
    within = sum(1 for t in totals if t <= TARGET_DAYS)
    lo, hi = wilson(within, n_done)
    grand = sum(totals)
    observations = {r.ref: stage_observations(r) for r, _ in done}
    complete = [(r, s) for r, s in done if all(observations[r.ref][k] for k in STAGES)]
    complete_total = sum(s["total"] for _, s in complete)
    stage_observation_count = {
        k: sum(1 for r, _ in done if observations[r.ref][k]) for k in STAGES
    }
    result.update({
        "mean_days": round(sum(totals) / n_done, 2),
        "median_days": round(percentile(totals, 0.5), 2),
        "p90_days": round(percentile(totals, 0.9), 2),
        "within_4_days": within,
        "within_4_days_rate": round(within / n_done, 4),
        "within_4_days_ci95": [round(lo, 4), round(hi, 4)],
        "stage_observation_count": stage_observation_count,
        "stage_missing_rate": {k: round(1 - stage_observation_count[k] / n_done, 4) for k in STAGES},
        "complete_stage_rows": len(complete),
        "stage_median_days": {
            k: (round(percentile([s[k] for r, s in done if observations[r.ref][k]], 0.5), 2)
                if stage_observation_count[k] else None) for k in STAGES
        },
        # Stage shares are calculated only on complete timestamp cases, never by treating
        # an unobserved interval as a measured zero.
        "stage_share_of_cycle": {
            k: (round(sum(s[k] for _, s in complete) / complete_total, 4) if complete_total else None)
            for k in STAGES
        },
        "costing_share_of_cycle": (
            round(sum(s["costing"] for _, s in complete) / complete_total, 4) if complete_total else None
        ),
        "mean_rework_count": round(sum(r.rework for r, _ in done) / n_done, 2),
        "mean_customer_hold_days": round(sum(r.hold_days for r, _ in done) / n_done, 2),
        "customer_hold_share_of_cycle_overlay": (
            round(sum(min(r.hold_days, s["total"]) for r, s in done) / grand, 4) if grand else 0.0
        ),
        "customer_hold_note": "Customer hold is a separately coded overlay, not an additive stage; it may overlap residual elapsed time.",
        "mean_internal_cycle_days_after_hold_overlay": round(
            sum(max(0.0, s["total"] - r.hold_days) for r, s in done) / n_done, 2
        ),
    })
    appr = [s["approval_wait"] for r, s in done if r.times["approval_requested_at"] is not None]
    result["share_needing_approval"] = round(len(appr) / n_done, 4)
    result["mean_approval_wait_all_rfqs_days"] = round(sum(appr) / n_done, 3)
    result["approval_budget_days"] = APPROVAL_BUDGET_DAYS
    result["approval_within_budget"] = result["mean_approval_wait_all_rfqs_days"] <= APPROVAL_BUDGET_DAYS
    lost = [r for r in rows if r.outcome == "lost"]
    coded = [r for r in lost if r.lost_reason]
    delay = [r for r in coded if r.lost_reason == "delay"]
    result["lost_rfqs"] = len(lost)
    result["lost_rfqs_coded"] = len(coded)
    result["lost_delay_share"] = round(len(delay) / len(coded), 4) if coded else None
    c = result["costing_share_of_cycle"]
    result["rule_costing_only"] = c is not None and c > COSTING_SHARE_CUT
    result["gate3_condition_a"] = (len(coded) >= MIN_CODED_LOST and bool(coded)
                                   and len(delay) / len(coded) >= DELAY_SHARE_GATE)
    result["decision"] = (
        "Insufficient complete stage timestamps: do not trigger a scope decision until stage coverage is adequate."
        if c is None else
        ("Costing is more than 40% of the cycle: cut scope to the costing screen and engine."
         if result["rule_costing_only"] else
         "Costing is 40% or less of the cycle: keep the register, clock and approval scope.")
    )
    return result


def main(argv: list[str] | None = None) -> int:
    import argparse
    import json
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("csv_path")
    parser.add_argument("--holiday", action="append", default=[], help="YYYY-MM-DD, repeatable")
    args = parser.parse_args(argv)
    holidays = frozenset(date.fromisoformat(h) for h in args.holiday)
    print(json.dumps(summarise(read_csv(args.csv_path), holidays), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
