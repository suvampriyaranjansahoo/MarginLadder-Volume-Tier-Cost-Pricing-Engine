import pytest
from analytics.event_contract import funnel, validate_event


def test_funnel_uses_correct_denominators_and_does_not_impute_lifecycle_steps():
    events = [{"event_id": "1", "event_name": "rfq_created", "rfq_id": "r1", "timestamp": "2026-01-01T00:00:00Z"},
              {"event_id": "2", "event_name": "quote_generated", "rfq_id": "r1", "timestamp": "2026-01-02T00:00:00Z"},
              {"event_id": "3", "event_name": "quote_sent", "rfq_id": "r1", "timestamp": "2026-01-03T00:00:00Z"},
              {"event_id": "4", "event_name": "rfq_created", "rfq_id": "r2", "timestamp": "2026-01-04T00:00:00Z"}]
    out = funnel(events)
    assert out["generated_per_created"] == .5 and out["sent_per_generated"] == 1


def test_invalid_event_is_rejected():
    with pytest.raises(ValueError):
        validate_event({"event_name": "unknown"})
