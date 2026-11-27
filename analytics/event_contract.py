"""Canonical V4 lifecycle event contract and safely computed funnel metrics."""
from __future__ import annotations
from datetime import datetime

EVENTS = ("rfq_created", "rfq_assigned", "costing_started", "costing_completed", "costing_validation_failed", "quote_generated", "quote_revised", "approval_requested", "approval_completed", "quote_sent", "quote_won", "quote_lost")


def validate_event(event: dict[str, object]) -> None:
    if event.get("event_name") not in EVENTS or not event.get("event_id") or not event.get("rfq_id") or not event.get("timestamp"):
        raise ValueError("event_id, event_name, rfq_id and timestamp are required")
    datetime.fromisoformat(str(event["timestamp"]).replace("Z", "+00:00"))


def funnel(events: list[dict[str, object]]) -> dict[str, float | int | None]:
    for event in events:
        validate_event(event)
    by_rfq: dict[str, set[str]] = {}
    for event in events:
        by_rfq.setdefault(str(event["rfq_id"]), set()).add(str(event["event_name"]))
    created = sum("rfq_created" in names for names in by_rfq.values())
    generated = sum("quote_generated" in names for names in by_rfq.values())
    sent = sum("quote_sent" in names for names in by_rfq.values())
    won = sum("quote_won" in names for names in by_rfq.values())
    return {"created": created, "generated": generated, "sent": sent, "won": won,
            "generated_per_created": generated / created if created else None,
            "sent_per_generated": sent / generated if generated else None,
            "won_per_sent": won / sent if sent else None}
