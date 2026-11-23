from datetime import datetime, timezone

import pytest

from analytics.product_metrics import ProductEventError, analyse, load_events


def event(event_id, user, ref, name, stamp):
    return {"event_id": event_id, "user_id": user, "rfq_ref": ref, "event_name": name,
            "event_at": datetime.fromisoformat(stamp).astimezone(timezone.utc)}


def test_product_funnel_uses_distinct_rfqs_and_expected_dropoff():
    events = [
        event("1", "u1", "r1", "rfq_created", "2026-10-01T09:00:00+00:00"),
        event("2", "u1", "r1", "quote_created", "2026-10-01T10:00:00+00:00"),
        event("3", "u1", "r1", "quote_sent", "2026-10-01T11:00:00+00:00"),
        event("4", "u2", "r2", "rfq_created", "2026-10-01T09:00:00+00:00"),
    ]
    out = analyse(events)
    assert out["rfqs_created"] == 2
    assert [r["rfqs"] for r in out["funnel"]] == [2, 1, 0, 0, 1]
    assert out["median_quote_cycle_hours"] == 2.0


def test_lifecycle_out_of_order_is_rejected():
    events = [
        event("1", "u1", "r1", "rfq_created", "2026-10-01T11:00:00+00:00"),
        event("2", "u1", "r1", "quote_sent", "2026-10-01T10:00:00+00:00"),
    ]
    with pytest.raises(ProductEventError, match="out of order"):
        analyse(events)


def test_sample_event_data_is_explicitly_synthetic():
    from pathlib import Path
    path = Path(__file__).resolve().parents[1] / "data" / "product_events_sample.csv"
    result = analyse(load_events(path))
    assert result["classification"].startswith("SIMULATED")
    assert result["rfqs_created"] == 6


def test_event_log_requires_timezone_offset(tmp_path):
    path = tmp_path / "events.csv"
    path.write_text("event_id,user_id,rfq_ref,event_name,event_at\n1,u1,r1,rfq_created,2026-10-01T09:00\n", encoding="utf-8")
    with pytest.raises(ProductEventError, match="timezone offset"):
        load_events(path)


def test_retention_cohort_uses_first_observed_activation_week_only():
    events = [
        event("1", "u1", "r1", "rfq_created", "2026-10-01T09:00:00+00:00"),
        event("2", "u1", "r1", "quote_sent", "2026-10-01T10:00:00+00:00"),
        event("3", "u1", "r2", "rfq_created", "2026-10-08T09:00:00+00:00"),
        event("4", "u2", "r3", "rfq_created", "2026-10-08T09:00:00+00:00"),
    ]
    out = analyse(events)
    cohorts = [r for r in out["operator_retention_cohorts"] if r["week_number"] == 0]
    assert [(r["cohort_week"], r["cohort_operators"]) for r in cohorts] == [("2026-W40", 1), ("2026-W41", 1)]
