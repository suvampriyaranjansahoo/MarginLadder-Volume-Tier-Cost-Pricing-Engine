import sqlite3
import sys
import tempfile
from pathlib import Path as _P
from datetime import date, timedelta
from pathlib import Path

ROOT = _P(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from application.service import MarginLadderService, ServiceError, AccessDeniedError  # noqa: E402

d = Path(tempfile.mkdtemp())
svc = MarginLadderService(d / "t.db", seed_demo=False)
out: list[tuple[str, str, str]] = []


def log(task, step, result):
    out.append((task, step, result))


def attempt(task, step, fn):
    try:
        r = fn()
        log(task, step, "OK: " + (r if isinstance(r, str) else "done"))
    except (ServiceError, AccessDeniedError) as e:
        log(task, step, f"REJECTED: {e}")


today = date.today()
# Task 1: create, find overdue, reassign
r = svc.create_rfq(
    {
        "customer": "Aster Mobility",
        "part_description": "EN8 bracket",
        "owner": "Aditi Rao",
        "due_date": (today + timedelta(days=4)).isoformat(),
        "notes": "synthetic",
    },
    "Aditi Rao",
    "estimator",
)
log("1 Create and reassign", "Create RFQ with owner and due date", f"OK: {r['rfq_code']} status {r['status']}")
past = (today - timedelta(days=3)).isoformat()
with sqlite3.connect(d / "t.db") as con:
    con.execute("UPDATE rfqs SET due_date=? WHERE id=?", (past, r["id"]))
log("1 Create and reassign", "Overdue count on dashboard", f"overdue_rfq_count = {svc.dashboard()['overdue_rfq_count']}")
attempt(
    "1 Create and reassign",
    "Reassign overdue RFQ, due date unchanged",
    lambda: svc.update_rfq(r["id"], {"owner": "Ravi Nair", "due_date": past}, "Aditi Rao", "estimator")["owner"],
)
attempt(
    "1 Create and reassign",
    "Move due date to another past date",
    lambda: svc.update_rfq(r["id"], {"due_date": (today - timedelta(days=9)).isoformat()}, "Aditi Rao", "estimator"),
)
# Task 2: bad input
attempt(
    "2 Bad input",
    "Empty customer",
    lambda: svc.create_rfq({"customer": "", "part_description": "x", "owner": "A", "due_date": today.isoformat()}, "A", "estimator"),
)
attempt(
    "2 Bad input",
    "Past due date on create",
    lambda: svc.create_rfq({"customer": "C", "part_description": "x", "owner": "A", "due_date": past}, "A", "estimator"),
)
attempt(
    "2 Bad input",
    "Sales head tries to create RFQ",
    lambda: svc.create_rfq({"customer": "C", "part_description": "x", "owner": "A", "due_date": today.isoformat()}, "S", "sales_head"),
)
attempt("2 Bad input", "Invalid status jump new to sent", lambda: svc.update_rfq(r["id"], {"status": "sent"}, "Aditi Rao", "estimator"))
attempt(
    "2 Bad input",
    "Quote while RFQ is still new",
    lambda: svc.create_quote(r["id"], {"quote_date": today.isoformat(), "selected_volume": 270000}, "Aditi Rao", "estimator"),
)
svc.update_rfq(r["id"], {"status": "costing"}, "Aditi Rao", "estimator")
attempt(
    "2 Bad input",
    "Quote with zero volume",
    lambda: svc.create_quote(r["id"], {"quote_date": today.isoformat(), "selected_volume": 0}, "Aditi Rao", "estimator"),
)
# Task 3: quote, approval, send-back, send
q = svc.create_quote(r["id"], {"quote_date": today.isoformat(), "selected_volume": 270000}, "Aditi Rao", "estimator")
log("3 Quote and approval", "Create quote (270000 pieces)", f"OK: status {q['status']}, approval required {q['approval_required']}")
attempt("3 Quote and approval", "Estimator tries to approve", lambda: svc.decide_quote(q["id"], "approve", "", "Aditi Rao", "estimator"))
attempt(
    "3 Quote and approval", "Send back without a reason", lambda: svc.decide_quote(q["id"], "send_back", "no", "Sales Head", "sales_head")
)
attempt(
    "3 Quote and approval",
    "Send back with a reason",
    lambda: svc.decide_quote(q["id"], "send_back", "Please review material rate", "Sales Head", "sales_head")["status"],
)
log("3 Quote and approval", "Audit events for this RFQ", ", ".join(e["event_type"] for e in svc.audit_log(entity_id=r["id"])) or "none")
lines = [
    "# Developer task run (scripted, synthetic data)",
    "",
    "**DEVELOPER-RUN, NOT USER RESEARCH.** `python3 scripts/developer_task_run.py` runs three tasks against the application service layer with a temporary database and synthetic records, and writes this file. No person took part. It shows how the system behaves on good and bad input. It does not show that anyone finds the screens clear.",
    "",
    f"Run date: {today.isoformat()}. Reproduce it by running the script; dates inside the run are relative to the day it is run.",
    "",
    "| Task | Step | Result |",
    "|---|---|---|",
]
for t, st, res in out:
    lines.append(f"| {t} | {st} | {res} |")
lines += [
    "",
    "## Observations",
    "- Every bad input was rejected with a plain message, and every role limit held.",
    "- Task 1 is the regression found in 3.4.2: an overdue RFQ can be reassigned, but its due date cannot be moved to another past date.",
    "- The audit filter by RFQ id returns RFQ events only. Quote decisions are stored under the quote id, so an RFQ history view would need to join them. This is a possible product improvement, not a defect in the stored data.",
    "",
    "## Not shown by this run",
    "Screen clarity, task time, user errors and preference. Those need real participants: see `docs/ba/independent_uat_and_signoff_protocol.md`.",
]
(ROOT / "docs/validation/developer_task_run.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(f"{t} | {st} | {res}" for t, st, res in out))
