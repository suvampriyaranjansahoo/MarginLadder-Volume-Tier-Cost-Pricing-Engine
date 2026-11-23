"""Tests for the v3 additions: auth, migrations, codes, paging, KPIs and trace import."""
import sqlite3
from contextlib import closing
from datetime import date, timedelta

import pytest

from application import auth
from application.service import AccessDeniedError, MarginLadderService, ServiceError


@pytest.fixture
def svc(tmp_path):
    return MarginLadderService(tmp_path / "t.db", seed_demo=False)


def rfq(svc, **o):
    p = {"customer": "Aster", "part_description": "Bracket", "owner": "A", "due_date": (date.today() + timedelta(days=3)).isoformat()}
    p.update(o)
    return svc.create_rfq(p, "A", "estimator")


# ---- passwords and sessions
def test_password_hash_is_salted_and_verifies():
    a, b = auth.hash_password("correct horse"), auth.hash_password("correct horse")
    assert a != b and auth.verify_password("correct horse", a) and not auth.verify_password("wrong horse!", a)


def test_short_password_refused():
    with pytest.raises(ValueError):
        auth.hash_password("short")


def test_verify_handles_garbage_hash():
    assert auth.verify_password("x" * 12, "not-a-hash") is False
    assert auth.verify_password("x" * 12, "md5$1$2$3$aa$bb") is False


def test_login_returns_working_session_and_logout_ends_it(svc):
    svc.create_user("Aditi", "a-long-password", "estimator", "Aditi Rao")
    session = svc.authenticate("aditi", "a-long-password")
    assert svc.user_for_token(session["token"])["role"] == "estimator"
    svc.logout(session["token"])
    assert svc.user_for_token(session["token"]) is None


def test_token_is_not_stored_in_clear(svc, tmp_path):
    svc.create_user("aditi", "a-long-password", "estimator")
    token = svc.authenticate("aditi", "a-long-password")["token"]
    with closing(sqlite3.connect(tmp_path / "t.db")) as con:
        stored = [r[0] for r in con.execute("SELECT token_hash FROM sessions")]
    assert token not in stored and len(stored[0]) == 64


def test_wrong_password_and_unknown_user_give_the_same_message(svc):
    svc.create_user("aditi", "a-long-password", "estimator")
    with pytest.raises(ServiceError) as a:
        svc.authenticate("aditi", "nope-nope-nope")
    with pytest.raises(ServiceError) as b:
        svc.authenticate("ghost", "nope-nope-nope")
    assert str(a.value) == str(b.value) == "Wrong username or password"


def test_lockout_after_five_failures_blocks_even_the_right_password(svc):
    svc.create_user("aditi", "a-long-password", "estimator")
    for _ in range(5):
        with pytest.raises(ServiceError):
            svc.authenticate("aditi", "bad-bad-bad-bad")
    with pytest.raises(ServiceError, match="Too many failed"):
        svc.authenticate("aditi", "a-long-password")


def test_expired_session_is_rejected(svc, tmp_path):
    svc.create_user("aditi", "a-long-password", "estimator")
    token = svc.authenticate("aditi", "a-long-password")["token"]
    with closing(sqlite3.connect(tmp_path / "t.db")) as con:
        con.execute("UPDATE sessions SET expires_at='2000-01-01T00:00:00+00:00'")
        con.commit()
    assert svc.user_for_token(token) is None


def test_duplicate_username_and_bad_role_refused(svc):
    svc.create_user("aditi", "a-long-password", "estimator")
    with pytest.raises(ServiceError, match="already exists"):
        svc.create_user("ADITI", "a-long-password", "estimator")
    with pytest.raises(ServiceError, match="Unknown role"):
        svc.create_user("x", "a-long-password", "admin")
    with pytest.raises(ServiceError, match="Username"):
        svc.create_user("a b", "a-long-password", "estimator")


def test_seed_demo_users_once_and_all_roles(svc):
    creds = svc.seed_demo_users()
    assert set(creds) == {"estimator", "estimation_head", "plant_head", "sales_head", "deputy"}
    assert svc.seed_demo_users() is None
    assert svc.authenticate("sales_head", creds["sales_head"])["user"]["role"] == "sales_head"


def test_login_and_failure_are_audited(svc):
    svc.create_user("aditi", "a-long-password", "estimator")
    with pytest.raises(ServiceError):
        svc.authenticate("aditi", "bad-bad-bad-bad")
    svc.authenticate("aditi", "a-long-password")
    kinds = [e["event_type"] for e in svc.audit_log()]
    assert "login_failed" in kinds and "login" in kinds
    assert all("password" not in str(e["details"]).lower() for e in svc.audit_log())


# ---- migrations
def test_v2_database_upgrades_without_losing_data(tmp_path):
    path = tmp_path / "old.db"
    con = sqlite3.connect(path)
    con.executescript("""
        CREATE TABLE rfqs (id TEXT PRIMARY KEY, rfq_code TEXT NOT NULL UNIQUE, customer TEXT NOT NULL,
          part_description TEXT NOT NULL, owner TEXT NOT NULL, received_at TEXT NOT NULL, due_date TEXT NOT NULL,
          status TEXT NOT NULL, notes TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
        INSERT INTO rfqs VALUES('1','RFQ-2611-001','Old Co','Part','Z','2026-11-01T00:00:00+00:00','2026-11-09','new','','x','x');
    """)
    con.commit()
    con.close()
    svc = MarginLadderService(path)
    assert svc.get_rfq("1")["customer"] == "Old Co"
    svc.create_user("aditi", "a-long-password", "estimator")


def test_migrations_run_once(svc, tmp_path):
    MarginLadderService(tmp_path / "t.db")
    with closing(sqlite3.connect(tmp_path / "t.db")) as con:
        assert [r[0] for r in con.execute("SELECT version FROM schema_version ORDER BY version")] == [1, 2, 3]


# ---- RFQ codes, seed dates, paging, search
def test_codes_never_collide_even_after_a_gap(svc, tmp_path):
    codes = [rfq(svc)["rfq_code"] for _ in range(3)]
    with closing(sqlite3.connect(tmp_path / "t.db")) as con:
        con.execute("PRAGMA foreign_keys=ON")
        con.execute("DELETE FROM rfqs WHERE rfq_code=?", (codes[1],))
        con.commit()
    new = rfq(svc)["rfq_code"]
    assert new not in codes and new.endswith("004")


def test_seed_due_dates_are_never_in_the_past(tmp_path):
    svc = MarginLadderService(tmp_path / "s.db", seed_demo=True)
    assert all(not r["is_overdue"] for r in svc.list_rfqs())


def test_pagination_and_count(svc):
    for i in range(7):
        rfq(svc, customer=f"C{i}")
    assert len(svc.list_rfqs(limit=3)) == 3
    assert len(svc.list_rfqs(limit=3, offset=6)) == 1
    assert svc.count_rfqs() == 7
    assert svc.count_rfqs(search="C3") == 1


def test_search_treats_percent_and_underscore_literally(svc):
    rfq(svc, customer="100% Steel")
    rfq(svc, customer="Plain")
    assert [r["customer"] for r in svc.list_rfqs(search="%")] == ["100% Steel"]
    assert svc.list_rfqs(search="_") == []


def test_listing_includes_latest_quote_without_extra_queries(svc):
    r = rfq(svc)
    svc.update_rfq(r["id"], {"status": "costing"}, "A", "estimator")
    svc.create_quote(r["id"], {"quote_date": "2026-11-05", "selected_volume": 270000}, "A", "estimator")
    row = svc.list_rfqs()[0]
    assert row["latest_quote"]["version"] == 1 and "q_id" not in row


def test_dashboard_counts_are_not_capped_by_the_page_size(svc):
    for i in range(3):
        rfq(svc, customer=f"C{i}")
    assert svc.dashboard()["rfq_count"] == 3 and svc.dashboard()["open_rfq_count"] == 3


# ---- KPIs
def _stamp(path, event_type, entity_id, when, details_json="{}", entity_type="rfq"):
    con = sqlite3.connect(path)
    con.execute("INSERT INTO audit_events(entity_type,entity_id,event_type,actor,actor_role,details_json,created_at) VALUES(?,?,?,?,?,?,?)",
                (entity_type, entity_id, event_type, "t", "estimator", details_json, when))
    con.commit()
    con.close()


def test_kpis_use_working_days_and_report_missing_rate(svc, tmp_path):
    a = rfq(svc)
    rfq(svc)
    con = sqlite3.connect(tmp_path / "t.db")
    con.execute("UPDATE rfqs SET received_at='2026-12-04T12:00:00+00:00' WHERE id=?", (a["id"],))  # Friday noon
    con.commit()
    con.close()
    _stamp(tmp_path / "t.db", "quote_sent", "q1", "2026-12-07T12:00:00+00:00", f'{{"rfq_id": "{a["id"]}"}}', "quote")
    k = svc.kpis()
    assert k["sent_n"] == 1 and k["time_to_quote_median_days"] == 1.0   # weekend skipped
    assert k["sent_within_4_days_rate"] == 1.0 and k["not_yet_sent_rate"] == 0.5


def test_kpis_with_no_data_do_not_crash(svc):
    k = svc.kpis()
    assert k["time_to_quote_median_days"] is None and k["rfq_total"] == 0


def test_approval_wait_pairs_request_and_decision(svc, tmp_path):
    _stamp(tmp_path / "t.db", "approval_requested", "q9", "2026-12-01T09:00:00+00:00", entity_type="quote")
    _stamp(tmp_path / "t.db", "quote_approved", "q9", "2026-12-01T21:00:00+00:00", entity_type="quote")
    assert svc.kpis()["approval_wait_median_days"] == 0.5


# ---- trace import
ROW = {"rfq_ref": "R1", "received_at": "2026-12-01T09:00", "sent_at": "2026-12-03T09:00", "outcome": "won"}


def test_trace_import_and_summary(svc):
    out = svc.import_trace([ROW, {**ROW, "rfq_ref": "R2"}], "Head", "estimation_head", batch_id="b1")
    assert out == {"batch_id": "b1", "rows": 2}
    s = svc.trace_summary("b1")
    assert s["sent_rows"] == 2 and s["median_days"] == 2.0


def test_trace_import_is_all_or_nothing(svc):
    with pytest.raises(ServiceError, match="Row 2"):
        svc.import_trace([ROW, {**ROW, "rfq_ref": "R2", "sent_at": "2026-11-01T09:00"}], "Head", "estimation_head", "b2")
    assert svc.trace_summary()["rows"] == 0


def test_trace_import_refuses_duplicates_wrong_role_and_reused_batch(svc):
    with pytest.raises(ServiceError, match="twice"):
        svc.import_trace([ROW, ROW], "Head", "estimation_head")
    with pytest.raises(AccessDeniedError):
        svc.import_trace([ROW], "Aditi", "estimator")
    svc.import_trace([ROW], "Head", "estimation_head", "b3")
    with pytest.raises(ServiceError, match="already imported"):
        svc.import_trace([ROW], "Head", "estimation_head", "b3")


def test_empty_trace_summary_says_so(svc):
    assert "No trace rows" in svc.trace_summary()["decision"]


def test_importing_asgi_module_does_not_create_database_or_demo_credentials(tmp_path):
    import os
    import subprocess
    import sys

    root = __import__("pathlib").Path(__file__).resolve().parents[2]
    db_path = tmp_path / "must-not-exist.db"
    credentials = root / "application" / "data" / "demo_credentials.txt"
    credentials.unlink(missing_ok=True)
    env = {**os.environ, "MARGINLADDER_DB": str(db_path), "PYTHONDONTWRITEBYTECODE": "1"}
    subprocess.run([sys.executable, "-B", "-c", "import application.server"], cwd=root, env=env,
                   check=True, capture_output=True, text=True)
    assert not db_path.exists()
    assert not credentials.exists()
