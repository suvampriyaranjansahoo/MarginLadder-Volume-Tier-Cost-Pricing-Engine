"""Product analytics for the RFQ workflow using event-level activity data.

The bundled dataset is synthetic. Metrics are defined here for a future instrumented
pilot; the generated report must never be represented as observed customer adoption.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

FUNNEL = ("rfq_created", "quote_created", "approval_requested", "quote_approved", "quote_sent")


class ProductEventError(ValueError):
    """An event log row is malformed or contradictory."""


def _parse_timestamp(value: str, row_no: int) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ProductEventError(f"line {row_no}: event_at must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ProductEventError(f"line {row_no}: event_at must include a timezone offset")
    return parsed.astimezone(UTC)


def load_events(path: str | Path) -> list[dict]:
    events = []
    seen_ids: set[str] = set()
    with Path(path).open(newline="", encoding="utf-8") as handle:
        for line_no, row in enumerate(csv.DictReader(handle), start=2):
            event_id = (row.get("event_id") or "").strip()
            user_id = (row.get("user_id") or "").strip()
            rfq_ref = (row.get("rfq_ref") or "").strip()
            name = (row.get("event_name") or "").strip()
            if not event_id or event_id in seen_ids or not user_id or not name:
                raise ProductEventError(f"line {line_no}: event_id must be unique; user_id and event_name are required")
            seen_ids.add(event_id)
            if name not in FUNNEL and name not in {"login", "rfq_viewed", "quote_viewed"}:
                raise ProductEventError(f"line {line_no}: unsupported event_name {name!r}")
            if name in FUNNEL and not rfq_ref:
                raise ProductEventError(f"line {line_no}: funnel event {name} requires rfq_ref")
            events.append({
                "event_id": event_id, "user_id": user_id, "rfq_ref": rfq_ref,
                "event_name": name, "event_at": _parse_timestamp(row.get("event_at", ""), line_no),
            })
    if not events:
        raise ProductEventError("event log is empty")
    return sorted(events, key=lambda event: event["event_at"])


def analyse(events: list[dict]) -> dict:
    by_rfq: dict[str, dict[str, datetime]] = defaultdict(dict)
    by_user_weeks: dict[str, set[str]] = defaultdict(set)
    for event in events:
        week = event["event_at"].strftime("%G-W%V")
        by_user_weeks[event["user_id"]].add(week)
        if event["event_name"] in FUNNEL:
            name, ref, stamp = event["event_name"], event["rfq_ref"], event["event_at"]
            if name in by_rfq[ref] and by_rfq[ref][name] != stamp:
                raise ProductEventError(f"RFQ {ref}: duplicate {name} event")
            by_rfq[ref][name] = stamp

    funnel = []
    cohort_counts: dict[str, set[str]] = defaultdict(set)
    for ref, milestones in by_rfq.items():
        created = milestones.get("rfq_created")
        if created is None:
            raise ProductEventError(f"RFQ {ref}: funnel events exist without rfq_created")
        ordered = [(name, milestones[name]) for name in FUNNEL if name in milestones]
        if any(right[1] < left[1] for left, right in zip(ordered, ordered[1:])):
            raise ProductEventError(f"RFQ {ref}: lifecycle events are out of order")
        week = created.strftime("%G-W%V")
        cohort_counts[week].add(ref)
    total = len(by_rfq)
    for name in FUNNEL:
        count = sum(1 for milestones in by_rfq.values() if name in milestones)
        funnel.append({"stage": name, "rfqs": count, "conversion_from_created_pct": round(count / total * 100, 1) if total else 0.0})

    cycle_hours = [
        (milestones["quote_sent"] - milestones["rfq_created"]).total_seconds() / 3600
        for milestones in by_rfq.values()
        if "rfq_created" in milestones and "quote_sent" in milestones
    ]
    cycle_hours.sort()
    median_cycle_hours = None
    if cycle_hours:
        mid = len(cycle_hours) // 2
        median_cycle_hours = round(cycle_hours[mid], 1) if len(cycle_hours) % 2 else round((cycle_hours[mid - 1] + cycle_hours[mid]) / 2, 1)

    weekly_active = []
    weeks = sorted({week for weeks_for_user in by_user_weeks.values() for week in weeks_for_user})
    for week in weeks:
        active = sum(1 for user_weeks in by_user_weeks.values() if week in user_weeks)
        weekly_active.append({"week": week, "active_operators": active})

    # A retention cohort is the operator's first observed activation week,
    # not every week in which the operator happened to be active.
    first_active_week = {user: min(weeks_for_user) for user, weeks_for_user in by_user_weeks.items()}
    cohorts = []
    for cohort in sorted(set(first_active_week.values())):
        first_week_users = {user for user, first_week in first_active_week.items() if first_week == cohort}
        for offset in (0, 1, 2):
            cohort_week = _week_offset(cohort, offset)
            active_users = sum(1 for user in first_week_users if cohort_week in by_user_weeks[user])
            cohorts.append({
                "cohort_week": cohort, "week_number": offset,
                "cohort_operators": len(first_week_users), "active_operators": active_users,
                "retention_pct": round(active_users / len(first_week_users) * 100, 1) if first_week_users else 0.0,
            })
    return {
        "classification": "SIMULATED event log; method demonstration only, not adoption or product outcomes",
        "rfqs_created": total,
        "funnel": funnel,
        "median_quote_cycle_hours": median_cycle_hours,
        "weekly_active_operators": weekly_active,
        "operator_retention_cohorts": cohorts,
        "definitions": {
            "funnel": "Distinct RFQs with at least one event at each lifecycle milestone, divided by RFQs created.",
            "cycle": "Median elapsed hours from rfq_created to quote_sent; calendar hours, not working hours.",
            "weekly_active": "Distinct operators with any supported event in the ISO week.",
            "retention": "Operators grouped once by their first observed activity week; retained when they generate any event in a later ISO week.",
        },
    }


def _week_offset(week: str, offset: int) -> str:
    year_text, week_text = week.split("-W")
    from datetime import date, timedelta
    monday = date.fromisocalendar(int(year_text), int(week_text), 1) + timedelta(weeks=offset)
    iso = monday.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def render_markdown(result: dict) -> str:
    lines = [
        "# Product analytics: simulated event funnel and operator cohorts", "",
        "> **Data: SIMULATED.** The event records are generated for method demonstration. They are not active users, adoption, conversion or retention outcomes from a live deployment.", "",
        f"RFQs created: **{result['rfqs_created']}**. Median created-to-sent time: **{result['median_quote_cycle_hours'] if result['median_quote_cycle_hours'] is not None else 'n.m.'} calendar hours**.", "",
        "## RFQ lifecycle funnel", "", "| Stage | RFQs | Conversion from created |", "|---|---:|---:|",
    ]
    lines.extend(f"| {row['stage']} | {row['rfqs']} | {row['conversion_from_created_pct']:.1f}% |" for row in result["funnel"])
    lines += ["", "## Weekly active operators", "", "| ISO week | Active operators |", "|---|---:|"]
    lines.extend(f"| {row['week']} | {row['active_operators']} |" for row in result["weekly_active_operators"])
    lines += ["", "## Cohort retention", "", "| Cohort week | Week | Cohort operators | Active operators | Retention |", "|---|---:|---:|---:|---:|"]
    lines.extend(f"| {row['cohort_week']} | {row['week_number']} | {row['cohort_operators']} | {row['active_operators']} | {row['retention_pct']:.1f}% |" for row in result["operator_retention_cohorts"])
    lines += ["", "## Definitions and interpretation", ""]
    lines.extend(f"- **{key.replace('_', ' ').title()}:** {value}" for key, value in result["definitions"].items())
    lines += ["- Funnel drop-off is descriptive in this synthetic sample; it does not establish causality.", "- In a pilot, instrument server-side events with stable RFQ and operator identifiers, define consent/access controls, and use a pre-registered baseline before interpreting adoption.", ""]
    return "\n".join(lines)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    result = analyse(load_events(root / "data" / "product_events_sample.csv"))
    output = root / "docs" / "product" / "simulated_product_analytics.md"
    output.write_text(render_markdown(result), encoding="utf-8")
    print(f"wrote {output.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
