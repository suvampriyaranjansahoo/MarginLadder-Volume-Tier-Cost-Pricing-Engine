from datetime import date, timedelta
from decimal import Decimal

import pytest

from application.service import MarginLadderService, AccessDeniedError, ServiceError


@pytest.fixture
def svc(tmp_path):
    return MarginLadderService(tmp_path / "test.db", seed_demo=False)


def make_rfq(svc, **overrides):
    payload = {
        "customer": "Aster Mobility",
        "part_description": "EN8 mounting bracket",
        "owner": "Aditi Rao",
        "due_date": (date.today() + timedelta(days=5)).isoformat(),
        "notes": "Illustrative test record",
    }
    payload.update(overrides)
    return svc.create_rfq(payload, "Aditi Rao", "estimator")


def test_create_rfq_persists_and_audits(svc):
    rfq = make_rfq(svc)
    assert rfq["rfq_code"].startswith("RFQ-")
    assert rfq["status"] == "new"
    assert svc.get_rfq(rfq["id"])["customer"] == "Aster Mobility"
    assert svc.audit_log(entity_id=rfq["id"])[0]["event_type"] == "rfq_created"


def test_role_restriction_on_rfq_creation(svc):
    with pytest.raises(AccessDeniedError):
        svc.create_rfq({"customer": "X", "part_description": "Y", "owner": "Z", "due_date": date.today().isoformat()}, "Sales", "sales_head")


def test_required_fields_and_due_date_validation(svc):
    with pytest.raises(ServiceError, match="Customer is required"):
        make_rfq(svc, customer=" ")
    with pytest.raises(ServiceError, match="Due date cannot be in the past"):
        make_rfq(svc, due_date=(date.today() - timedelta(days=1)).isoformat())


def test_invalid_status_transition_is_blocked(svc):
    rfq = make_rfq(svc)
    with pytest.raises(ServiceError, match="Invalid status transition"):
        svc.update_rfq(rfq["id"], {"status": "sent"}, "Aditi", "estimator")


def test_estimator_can_start_costing(svc):
    rfq = make_rfq(svc)
    updated = svc.update_rfq(rfq["id"], {"status": "costing"}, "Aditi", "estimator")
    assert updated["status"] == "costing"


def test_only_plant_head_can_clear_routing_review(svc):
    rfq = make_rfq(svc)
    svc.update_rfq(rfq["id"], {"status": "costing"}, "Aditi", "estimator")
    svc.update_rfq(rfq["id"], {"status": "routing_review"}, "Aditi", "estimator")
    with pytest.raises(AccessDeniedError, match="Only the Plant Head"):
        svc.update_rfq(rfq["id"], {"status": "ready_for_quote"}, "Aditi", "estimator")
    cleared = svc.update_rfq(rfq["id"], {"status": "ready_for_quote"}, "Plant Head", "plant_head")
    assert cleared["status"] == "ready_for_quote"


def test_costing_requires_costing_stage(svc):
    rfq = make_rfq(svc)
    with pytest.raises(ServiceError, match="Cannot cost an RFQ"):
        svc.create_quote(rfq["id"], {}, "Aditi", "estimator")


def test_create_quote_produces_three_tiers_and_snapshot(svc):
    rfq = make_rfq(svc)
    svc.update_rfq(rfq["id"], {"status": "costing"}, "Aditi", "estimator")
    quote = svc.create_quote(rfq["id"], {"quote_date": "2026-11-05", "selected_volume": 180000}, "Aditi", "estimator")
    assert len(quote["snapshot"]["tiers"]) == 3
    assert quote["snapshot"]["formula_version"] == "v1.0"
    assert quote["snapshot"]["tiers"][1]["lines"][0]["result"]["price"]
    assert quote["snapshot"]["tiers"][1]["lines"][0]["result"]["snapshot"]["rates"][0][5] == "v17"


def test_large_quote_requires_sales_approval(svc):
    rfq = make_rfq(svc)
    svc.update_rfq(rfq["id"], {"status": "costing"}, "Aditi", "estimator")
    quote = svc.create_quote(rfq["id"], {"quote_date": "2026-11-05", "selected_volume": 270000}, "Aditi", "estimator")
    assert quote["approval_required"] is True
    assert quote["status"] == "pending_approval"
    assert Decimal(quote["annual_value"]) > Decimal("2500000")


def test_smallest_supported_volume_still_triggers_approval_under_case_rates(svc):
    # At the case assumptions, even the smallest supported tier exceeds ₹25 lakh.
    rfq = make_rfq(svc)
    svc.update_rfq(rfq["id"], {"status": "costing"}, "Aditi", "estimator")
    quote = svc.create_quote(rfq["id"], {"quote_date": "2026-11-05", "selected_volume": 90000}, "Aditi", "estimator")
    assert Decimal(quote["annual_value"]) > Decimal("2500000")
    assert quote["approval_required"] is True
    assert quote["status"] == "pending_approval"


def test_estimator_cannot_approve(svc):
    rfq = make_rfq(svc)
    svc.update_rfq(rfq["id"], {"status": "costing"}, "Aditi", "estimator")
    quote = svc.create_quote(rfq["id"], {"quote_date": "2026-11-05", "selected_volume": 270000}, "Aditi", "estimator")
    with pytest.raises(AccessDeniedError):
        svc.decide_quote(quote["id"], "approve", "", "Aditi", "estimator")


def test_sales_head_can_approve_and_quote_can_be_sent(svc):
    rfq = make_rfq(svc)
    svc.update_rfq(rfq["id"], {"status": "costing"}, "Aditi", "estimator")
    quote = svc.create_quote(rfq["id"], {"quote_date": "2026-11-05", "selected_volume": 270000}, "Aditi", "estimator")
    approved = svc.decide_quote(quote["id"], "approve", "", "Sales Head", "sales_head")
    assert approved["status"] == "approved"
    sent = svc.send_quote(quote["id"], "Aditi", "estimator")
    assert sent["status"] == "sent"
    assert svc.get_rfq(rfq["id"])["status"] == "sent"


def test_send_back_requires_reason_and_returns_to_costing(svc):
    rfq = make_rfq(svc)
    svc.update_rfq(rfq["id"], {"status": "costing"}, "Aditi", "estimator")
    quote = svc.create_quote(rfq["id"], {"quote_date": "2026-11-05", "selected_volume": 270000}, "Aditi", "estimator")
    with pytest.raises(ServiceError, match="at least five characters"):
        svc.decide_quote(quote["id"], "send_back", "no", "Sales Head", "sales_head")
    returned = svc.decide_quote(quote["id"], "send_back", "Please review material rate", "Sales Head", "sales_head")
    assert returned["status"] == "sent_back"
    assert svc.get_rfq(rfq["id"])["status"] == "sent_back"


def test_quote_versions_increment_after_send_back(svc):
    rfq = make_rfq(svc)
    svc.update_rfq(rfq["id"], {"status": "costing"}, "Aditi", "estimator")
    first = svc.create_quote(rfq["id"], {"quote_date": "2026-11-05", "selected_volume": 270000}, "Aditi", "estimator")
    svc.decide_quote(first["id"], "send_back", "Correct cycle time", "Sales Head", "sales_head")
    second = svc.create_quote(rfq["id"], {"quote_date": "2026-11-06", "selected_volume": 270000}, "Aditi", "estimator")
    assert second["version"] == 2
    assert first["snapshot"]["quote_date"] == "2026-11-05"


def test_invalid_volume_and_part_inputs_are_blocked(svc):
    rfq = make_rfq(svc)
    svc.update_rfq(rfq["id"], {"status": "costing"}, "Aditi", "estimator")
    with pytest.raises(ServiceError, match="Selected volume"):
        svc.create_quote(rfq["id"], {"selected_volume": 123}, "Aditi", "estimator")
    with pytest.raises(ServiceError, match="net weight exceeds gross weight"):
        svc.create_quote(rfq["id"], {"quote_date": "2026-11-05", "parts": [{"gross": "0.5", "net": "0.9"}]}, "Aditi", "estimator")


def test_audit_trail_captures_approval_lifecycle(svc):
    rfq = make_rfq(svc)
    svc.update_rfq(rfq["id"], {"status": "costing"}, "Aditi", "estimator")
    quote = svc.create_quote(rfq["id"], {"quote_date": "2026-11-05", "selected_volume": 270000}, "Aditi", "estimator")
    svc.decide_quote(quote["id"], "approve", "", "Sales Head", "sales_head")
    events = svc.audit_log(entity_id=quote["id"])
    assert {e["event_type"] for e in events} >= {"quote_costed", "quote_approved"}


def test_dashboard_distinguishes_application_data_and_simulation(svc):
    make_rfq(svc)
    dashboard = svc.dashboard()
    cycle = svc.simulated_cycle_analytics()
    assert dashboard["rfq_count"] == 1
    assert "not client results" in dashboard["data_label"]
    assert cycle["data_type"] == "simulated"
    assert cycle["sample_size"] == 60


def test_non_numeric_cost_input_is_returned_as_validation_error(svc):
    rfq = make_rfq(svc)
    svc.update_rfq(rfq["id"], {"status": "costing"}, "Aditi", "estimator")
    with pytest.raises(ServiceError, match="non-numeric costing input"):
        svc.create_quote(rfq["id"], {"quote_date": "2026-11-05", "parts": [{"gross": "not-a-number"}]}, "Aditi", "estimator")


def test_dashboard_uses_latest_quote_version_not_sum_of_old_versions(svc):
    rfq = make_rfq(svc)
    svc.update_rfq(rfq["id"], {"status": "costing"}, "Aditi", "estimator")
    first = svc.create_quote(rfq["id"], {"quote_date": "2026-11-05", "selected_volume": 270000}, "Aditi", "estimator")
    svc.decide_quote(first["id"], "send_back", "Review target margin", "Sales Head", "sales_head")
    second = svc.create_quote(rfq["id"], {
        "quote_date": "2026-11-06", "selected_volume": 270000,
        "parts": [{"description": "EN8 mounting bracket", "margin": "0.10"}],
    }, "Aditi", "estimator")
    dashboard = svc.dashboard()
    assert dashboard["quote_version_count"] == 2
    assert dashboard["latest_quote_count"] == 1
    assert Decimal(dashboard["quoted_annual_value_inr"]) == Decimal(second["annual_value"])


def test_assignment_owner_and_due_date_can_be_updated(svc):
    rfq = make_rfq(svc)
    new_due = (date.today() + timedelta(days=9)).isoformat()
    updated = svc.update_rfq(rfq["id"], {"owner": "Rahul Mehta", "due_date": new_due}, "Estimation Head", "estimation_head")
    assert updated["owner"] == "Rahul Mehta"
    assert updated["due_date"] == new_due


def test_assignment_update_rejects_past_due_date(svc):
    rfq = make_rfq(svc)
    past_due = (date.today() - timedelta(days=5)).isoformat()
    with pytest.raises(ServiceError, match="Due date cannot be in the past"):
        svc.update_rfq(rfq["id"], {"due_date": past_due}, "Aditi", "estimator")
    unchanged = svc.get_rfq(rfq["id"])
    assert unchanged["due_date"] == rfq["due_date"]


def test_multi_part_quote_aggregates_set_value_and_keeps_line_snapshots(svc):
    rfq = make_rfq(svc)
    svc.update_rfq(rfq["id"], {"status": "costing"}, "Aditi", "estimator")
    quote = svc.create_quote(rfq["id"], {
        "quote_date": "2026-11-05", "selected_volume": 180000,
        "parts": [
            {"description": "Mounting bracket", "gross": "0.61", "net": "0.52", "cycle_min": "3.2"},
            {"description": "Spindle sleeve", "gross": "0.75", "net": "0.62", "cycle_min": "4.1"},
        ],
    }, "Aditi", "estimator")
    tier = quote["snapshot"]["selected_tier"]
    assert len(tier["lines"]) == 2
    assert tier["lines"][0]["description"] == "Mounting bracket"
    assert tier["lines"][1]["description"] == "Spindle sleeve"
    assert Decimal(quote["annual_value"]) == sum((Decimal(line["result"]["annual_value"]) for line in tier["lines"]), Decimal("0"))
