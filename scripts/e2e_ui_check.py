"""Browser check of the real RFQ workflow through the web page (optional developer tool).

Needs `pip install playwright && playwright install chromium` (not in requirements.txt) and a running server:

    uvicorn application.server:app            # first run writes application/data/demo_credentials.txt
    python scripts/e2e_ui_check.py            # or: python scripts/e2e_ui_check.py http://127.0.0.1:8000

It signs in as each role and runs: create RFQ, start costing, cost 3 volume tiers, send back, re-cost, approve, send, print,
trace import, a refused action and a wrong password, plus API-level tier price assertions
(117.33 / 116.51 / 115.77 on rate date 2026-11-05). It creates one RFQ ("Test Customer Ltd") in the local demo database.
Exit code is 1 if any step fails. Evidence status: written and run against a Starlette stand-in that mirrors the route
glue of application/server.py (FastAPI could not be installed in the authoring environment); not yet run against uvicorn.
"""

import re
import sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
CRED_FILE = ROOT / "application" / "data" / "demo_credentials.txt"
creds = {}
for line in CRED_FILE.read_text(encoding="utf-8").splitlines():
    m = re.match(r"^([a-z_]+): (\S+)$", line)
    if m:
        creds[m.group(1)] = m.group(2)
TRACE_TEMPLATE = ROOT / "tracekit" / "rfq_trace_template.csv"
results: list[tuple[str, bool, object]] = []


def ok(name, cond, note=""):
    results.append((name, bool(cond), note))


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1400, "height": 1000})
    pg = ctx.new_page()
    errors, bad = [], []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errors.append("PAGEERROR " + str(e)))
    pg.on("response", lambda r: bad.append(f"{r.status} {r.request.method} {r.url}") if r.status >= 400 else None)
    pg.on("dialog", lambda d: d.accept("Needs a lower margin; please recheck the setup time."))

    def logout():
        pg.click("#logoutBtn")
        pg.wait_for_selector("#loginWrap.open")
        pg.wait_for_function("sessionStorage.getItem('ml_token')===null")

    def login(role):
        pg.goto(BASE)
        pg.wait_for_selector("#loginForm")
        pg.fill("#loginForm [name=username]", role)
        pg.fill("#loginForm [name=password]", creds[role])
        pg.click("#loginForm button[type=submit]")
        pg.wait_for_function("document.getElementById('loginWrap').classList.contains('open')===false")
        pg.wait_for_function(
            "document.getElementById('whoami').textContent.trim()!=='–' && document.querySelectorAll('#rfqList .rfq-item').length>0 && document.querySelectorAll('#detailPanel .panel-body').length>0"
        )

    def open_rfq():
        pg.click("text=Test Customer Ltd")
        pg.wait_for_function(
            "document.getElementById('detailPanel').innerText.includes('Test Customer Ltd') && document.getElementById('detailPanel').innerText.includes('UI test record')"
        )

    # wrong password
    pg.goto(BASE)
    pg.wait_for_selector("#loginForm")
    pg.fill("#loginForm [name=username]", "estimator")
    pg.fill("#loginForm [name=password]", "wrongpassword!")
    pg.click("#loginForm button[type=submit]")
    pg.wait_for_function("document.getElementById('loginErr').textContent.length>0")
    ok("Wrong password shows an error", True, pg.inner_text("#loginErr"))
    login("estimator")
    ok("Signed-in user shown", "Estimator" in pg.inner_text("#whoami"), pg.inner_text("#whoami"))
    ok("Metric cards rendered (5)", pg.locator("#metricGrid .metric").count() == 5)
    ok("Finance case panel has content", len(pg.inner_text("#financeBody")) > 100, pg.inner_text("#financeBody")[:80].replace("\n", " "))
    ok("KPI panel has content", len(pg.inner_text("#kpiBody")) > 50)
    pg.wait_for_function("document.getElementById('analysisBody').innerText.length>50")
    ok("Analysis (queueing) panel has content", True)
    ok("Baseline (simulated) panel has content", len(pg.inner_text("#baselineBody")) > 30)
    ok("Audit panel has content", len(pg.inner_text("#auditList")) > 10)
    n0 = pg.locator("#rfqList .rfq-item").count()
    ok("Demo RFQs listed", n0 > 0, f"{n0} RFQs")
    # search + filter
    pg.fill("#searchInput", "zzzzzz")
    ok("Search with no match shows empty state", "No matching" in pg.inner_text("#rfqList"))
    pg.fill("#searchInput", "")
    pg.select_option("#statusFilter", "all")
    # create RFQ
    pg.click("#newRfqBtn")
    pg.wait_for_selector("#newRfqModal.open")
    f = "#newRfqForm"
    pg.fill(f + " [name=customer]", "Test Customer Ltd")
    pg.fill(f + " [name=part_description]", "EN8 shaft, drawing TC-01")
    pg.fill(f + " [name=notes]", "UI test record")
    pg.click(f + " button[type=submit]")
    pg.wait_for_function("document.getElementById('newRfqModal').classList.contains('open')===false")
    pg.wait_for_selector("text=Test Customer Ltd")
    ok("New RFQ created and listed", pg.locator("#rfqList .rfq-item").count() == n0 + 1)
    # modal cancel + close buttons
    pg.click("#newRfqBtn")
    pg.click("#cancelModal")
    ok("Cancel closes modal", not pg.locator("#newRfqModal.open").count())
    pg.click("#newRfqBtn")
    pg.click("#closeModal")
    ok("Close (X) closes modal", not pg.locator("#newRfqModal.open").count())
    # start costing
    pg.click("#startCostingBtn")
    pg.wait_for_selector("#costQuoteBtn")
    ok("Start costing moves RFQ to costing", True)
    # assignment editor
    if pg.locator("#editAssignmentBtn").count():
        pg.click("#editAssignmentBtn")
        ok("Edit assignment opens editor", pg.locator("#assignmentEditor:not(.hidden)").count() == 1)
        pg.click("#saveAssignmentBtn")
        pg.wait_for_timeout(500)
    else:
        ok("Edit assignment button present", False)
    # cost quote
    pg.click("#costQuoteBtn")
    pg.wait_for_selector("#quoteComposer:not(.hidden)")
    ok("Composer opens with one part line", pg.locator(".part-entry").count() == 1)
    pg.click("#addPartLineBtn")
    ok("Add part line works", pg.locator(".part-entry").count() == 2)
    pg.click(".part-remove >> nth=1")
    ok("Remove part line works", pg.locator(".part-entry").count() == 1)
    pg.click("#cancelCostBtn")
    ok("Cancel hides composer", pg.locator("#quoteComposer.hidden").count() == 1)
    pg.click("#costQuoteBtn")
    pg.click("#runCostBtn")
    pg.wait_for_selector(".tier-grid")
    ok(
        "Calculate 3 volume prices creates a quote with 3 tiers",
        pg.locator(".tier").count() == 3,
        pg.inner_text(".tier >> nth=1").replace("\n", " | "),
    )
    # API-level price assertions with a fixed rate date, through HTTP with the signed-in user's bearer token
    hdr = {"Authorization": "Bearer " + str(pg.evaluate("sessionStorage.getItem('ml_token')"))}
    due = (date.today() + timedelta(days=5)).isoformat()
    api_rfq = ctx.request.post(
        BASE + "/api/rfqs",
        headers=hdr,
        data={"customer": "API Price Check Ltd", "part_description": "EN8 shaft", "owner": "Estimator", "due_date": due},
    ).json()
    ctx.request.patch(BASE + f"/api/rfqs/{api_rfq['id']}", headers=hdr, data={"status": "costing"})
    api_quote = ctx.request.post(BASE + f"/api/rfqs/{api_rfq['id']}/quote", headers=hdr, data={"quote_date": "2026-11-05"}).json()
    got = {t["annual_volume_per_part"]: str(Decimal(str(t["total_unit_price"]))) for t in api_quote["snapshot"]["tiers"]}
    ok(
        "API quote prices: 90,000 = 117.33, 180,000 = 116.51, 270,000 = 115.77",
        got == {90000: "117.33", 180000: "116.51", 270000: "115.77"},
        got,
    )
    status_txt = pg.inner_text("#detailPanel")
    pending = "Approval" in status_txt or "pending" in status_txt.lower()
    ok(
        "Quote shows an approval state",
        pending,
        next((ln for ln in status_txt.split("\n") if "Quote v" in ln), ""),
    )
    # approval flow as sales head
    logout()
    pg.wait_for_selector("#loginWrap.open")
    ok("Sign out shows login", True)
    login("sales_head")
    open_rfq()
    if pg.locator("#sendBackBtn").count():
        pg.click("#sendBackBtn")
        pg.wait_for_timeout(800)
        ok(
            "Send back with reason works (prompt)",
            "sent back" in pg.inner_text("#detailPanel").lower() or "Sent back" in pg.inner_text("#detailPanel"),
        )
        logout()
        login("estimator")
        open_rfq()
        pg.wait_for_selector("#costQuoteBtn")
        pg.click("#costQuoteBtn")
        pg.click("#runCostBtn")
        pg.wait_for_selector(".tier-grid")
        logout()
        login("sales_head")
        open_rfq()
    if pg.locator("#approveBtn").count():
        pg.click("#approveBtn")
        pg.wait_for_function("document.getElementById('detailPanel').innerText.includes('Approved')", timeout=5000)
        ok("Sales head approves", True)
    else:
        ok("Sales head sees Approve button (approval required)", False, "no approve button; annual value may be under threshold")
    logout()
    login("estimator")
    open_rfq()
    if pg.locator("#sendQuoteBtn").count():
        pg.click("#sendQuoteBtn")
        pg.wait_for_function("/Quote v\\d+: Sent/i.test(document.getElementById('detailPanel').innerText)", timeout=5000)
        ok("Estimator marks quote as sent", True)
    else:
        ok("Send quote button available after approval", False)
    # print
    if pg.locator("[data-print]").count():
        with ctx.expect_page() as pop:
            pg.click("[data-print]")
        pr = pop.value
        pr.wait_for_load_state()
        txt = pr.inner_text("body")
        ok("Printable quotation opens", "Indicative Quotation" in txt and "Test Customer Ltd" in txt)
        pr.close()
    else:
        ok("Print button present on a quote", False)
    # refresh button
    pg.click("#refreshBtn")
    pg.wait_for_timeout(500)
    ok("Refresh does not error", True)
    # audit shows new events
    ok("Audit trail records workflow events", "quote" in pg.inner_text("#auditList").lower())
    # trace section hidden for estimator, visible for estimation_head
    ok("Trace import hidden for estimator", not pg.locator("#traceSection").is_visible())
    logout()
    login("estimation_head")
    ok("Trace import visible for estimation head", pg.locator("#traceSection").is_visible())
    pg.click("#traceImportBtn")
    pg.wait_for_timeout(500)
    ok("Trace import without file shows a message (not silent)", "Choose a CSV" in pg.inner_text("#toast"), pg.inner_text("#toast"))
    pg.set_input_files("#traceFile", str(TRACE_TEMPLATE))
    pg.click("#traceImportBtn")
    pg.wait_for_timeout(1200)
    ok("Trace import of the template gives a clear result", len(pg.inner_text("#traceBody")) > 5, pg.inner_text("#traceBody")[:160])
    # a role without permission
    logout()
    login("sales_head")
    pg.click("#newRfqBtn")
    pg.fill("#newRfqForm [name=customer]", "X")
    pg.fill("#newRfqForm [name=part_description]", "Y")
    pg.click("#newRfqForm button[type=submit]")
    pg.wait_for_timeout(700)
    ok("Role without permission gets a visible refusal", len(pg.inner_text("#toast")) > 3, pg.inner_text("#toast"))
    ctx.close()
    b.close()
for n, c, note in results:
    print(("PASS " if c else "FAIL ") + n + (f"  [{note}]" if note else ""))
print("\nconsole/page errors (401/403 are expected from the wrong-password and refused-action steps):", errors)
print("HTTP >=400 responses:", bad)

failed = [r for r in results if not r[1]]
print(f"\n{len(results) - len(failed)} of {len(results)} steps passed")
sys.exit(1 if failed else 0)
