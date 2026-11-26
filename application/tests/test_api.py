"""HTTP-level tests. Needs FastAPI: pip install -r requirements-dev.txt"""
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from application import server
from application.service import MarginLadderService

PW = "demo-password-1"


@pytest.fixture
def client(tmp_path, monkeypatch):
    svc = MarginLadderService(tmp_path / "api.db", seed_demo=False)
    for role in ("estimator", "estimation_head", "plant_head", "sales_head", "deputy"):
        svc.create_user(role, PW, role, role.title())
    monkeypatch.setattr(server, "service", svc)
    return TestClient(server.app)


def sign_in(client, username):
    r = client.post("/api/login", json={"username": username, "password": PW})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['token']}"}


def new_rfq(client, h, **o):
    body = {"customer": "Aster Mobility", "part_description": "EN8 mounting bracket", "owner": "Aditi Rao",
            "due_date": (date.today() + timedelta(days=5)).isoformat()}
    body.update(o)
    return client.post("/api/rfqs", json=body, headers=h)


def test_health_is_public_and_everything_else_needs_a_session(client):
    assert client.get("/api/health").json()["status"] == "ok"
    for path in ("/api/rfqs", "/api/dashboard", "/api/audit", "/api/kpis", "/api/finance-case",
                 "/api/analysis", "/api/trace/summary", "/api/me"):
        assert client.get(path).status_code == 401, path
    assert client.get("/api/rfqs", headers={"Authorization": "Bearer nonsense"}).status_code == 401


def test_login_failure_lockout_and_logout(client):
    assert client.post("/api/login", json={"username": "estimator", "password": "wrong-wrong"}).status_code == 401
    h = sign_in(client, "estimator")
    assert client.get("/api/me", headers=h).json()["role"] == "estimator"
    client.post("/api/logout", headers=h)
    assert client.get("/api/me", headers=h).status_code == 401
    for _ in range(5):
        client.post("/api/login", json={"username": "deputy", "password": "wrong-wrong"})
    assert client.post("/api/login", json={"username": "deputy", "password": PW}).status_code == 429


def test_role_comes_from_the_session_not_the_request_body(client):
    h = sign_in(client, "estimator")
    rfq = new_rfq(client, h).json()
    client.patch(f"/api/rfqs/{rfq['id']}", json={"status": "costing"}, headers=h)
    quote = client.post(f"/api/rfqs/{rfq['id']}/quote",
                        json={"quote_date": "2026-11-05", "selected_volume": 270000}, headers=h).json()
    # The body claims sales_head. The session says estimator. The session wins.
    forged = client.post(f"/api/quotes/{quote['id']}/decision",
                         json={"action": "approve", "role": "sales_head", "actor": "Boss"}, headers=h)
    assert forged.status_code == 403
    audit = client.get("/api/audit", headers=h).json()
    assert all(e["actor"] != "Boss" for e in audit)


def test_full_workflow_with_real_roles(client):
    est, head = sign_in(client, "estimator"), sign_in(client, "sales_head")
    rfq = new_rfq(client, est)
    assert rfq.status_code == 201
    rfq = rfq.json()
    assert client.patch(f"/api/rfqs/{rfq['id']}", json={"status": "costing"}, headers=est).status_code == 200
    quote = client.post(f"/api/rfqs/{rfq['id']}/quote",
                        json={"quote_date": "2026-11-05", "selected_volume": 270000}, headers=est)
    assert quote.status_code == 201
    quote = quote.json()
    assert quote["status"] == "pending_approval" and len(quote["snapshot"]["tiers"]) == 3
    assert client.post(f"/api/quotes/{quote['id']}/decision", json={"action": "approve"}, headers=head).json()["status"] == "approved"
    assert client.post(f"/api/quotes/{quote['id']}/send", headers=est).json()["status"] == "sent"
    assert any(e["event_type"] == "quote_approved" for e in client.get("/api/audit?limit=50", headers=est).json())


def test_validation_errors_are_clear(client):
    h = sign_in(client, "estimator")
    assert new_rfq(client, h, customer="").status_code == 422
    assert new_rfq(client, h, due_date="2000-01-01").status_code == 400


def test_pagination_header_and_search(client):
    h = sign_in(client, "estimator")
    for i in range(4):
        new_rfq(client, h, customer=f"Cust{i}")
    page = client.get("/api/rfqs?limit=2&offset=0", headers=h)
    assert len(page.json()) == 2 and page.headers["x-total-count"] == "4"
    assert len(client.get("/api/rfqs?search=Cust3", headers=h).json()) == 1
    assert client.get("/api/rfqs?limit=0", headers=h).status_code == 422


def test_finance_and_analysis_endpoints(client):
    h = sign_in(client, "estimator")
    fin = client.get("/api/finance-case", headers=h).json()
    assert "assumptions" in fin["classification"] and fin["base_case"]["annual_recovered_margin"] == "2160000.00"
    assert fin["net_capacity"]["net_hours"] == 4680
    a = client.get("/api/analysis", headers=h).json()
    assert 0.5 < a["queueing"]["today"]["wait_days"] < 0.65
    assert a["capacity"]["break_even_fit"] == pytest.approx(0.463, abs=0.001)


def test_trace_import_only_for_the_estimation_head(client):
    row = {"rfq_ref": "R1", "received_at": "2026-12-01T09:00", "sent_at": "2026-12-03T09:00", "outcome": "won"}
    est, head = sign_in(client, "estimator"), sign_in(client, "estimation_head")
    assert client.post("/api/trace/import", json={"rows": [row]}, headers=est).status_code == 403
    ok = client.post("/api/trace/import", json={"rows": [row], "batch_id": "b1"}, headers=head)
    assert ok.status_code == 201
    assert client.get("/api/trace/summary?batch_id=b1", headers=head).json()["sent_rows"] == 1
    bad = client.post("/api/trace/import", json={"rows": [{**row, "rfq_ref": "R2", "sent_at": "2026-11-01T09:00"}]}, headers=head)
    assert bad.status_code == 400 and "Row 1" in bad.json()["detail"]


def test_print_view_requires_sign_in_and_escapes_html(client):
    h = sign_in(client, "estimator")
    rfq = new_rfq(client, h, customer="<script>alert(1)</script>").json()
    client.patch(f"/api/rfqs/{rfq['id']}", json={"status": "costing"}, headers=h)
    q = client.post(f"/api/rfqs/{rfq['id']}/quote", json={"quote_date": "2026-11-05", "selected_volume": 270000}, headers=h).json()
    assert client.get(f"/api/quotes/{q['id']}/print").status_code == 401
    page = client.get(f"/api/quotes/{q['id']}/print", headers=h)
    assert "Indicative Quotation" in page.text and "<script>alert(1)" not in page.text


def test_static_workspace_and_docs_are_served(client):
    assert "RFQ workspace" in client.get("/").text
    assert client.get("/docs").status_code == 200
    assert client.get("/prototype/business_dashboard.html").status_code == 200
    assert client.get("/").headers["x-frame-options"] == "DENY"


def test_costing_errors_come_back_as_400(client):
    h = sign_in(client, "estimator")
    rfq = new_rfq(client, h).json()
    client.patch(f"/api/rfqs/{rfq['id']}", json={"status": "costing"}, headers=h)
    r = client.post(f"/api/rfqs/{rfq['id']}/quote", json={
        "quote_date": "2026-11-05", "selected_volume": 90000,
        "parts": [{"description": "Invalid part", "gross": "0.5", "net": "0.9"}]}, headers=h)
    assert r.status_code == 400 and "net weight exceeds gross weight" in r.json()["detail"]


def test_update_rfq_rejects_past_due_date(client):
    h = sign_in(client, "estimator")
    created = new_rfq(client, h).json()
    response = client.patch(
        f"/api/rfqs/{created['id']}",
        json={"due_date": "2000-01-01"},
        headers=h,
    )
    assert response.status_code == 400
    assert "Due date cannot be in the past" in response.json()["detail"]
    unchanged = client.get(f"/api/rfqs/{created['id']}", headers=h).json()
    assert unchanged["due_date"] == created["due_date"]
