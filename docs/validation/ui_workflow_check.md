# UI workflow check (browser, real page, real service layer)

**Evidence boundary, read first.** FastAPI could not be installed in the authoring environment (no network), so `application/server.py`
itself was **not started**. The check below ran the real `application/static/index.html` in headless Chromium against a throwaway
Starlette stand-in that mirrors the route paths, bearer-token auth and error mapping of `server.py` over the real
`MarginLadderService` and finance modules (the finance-case, analysis and printable-quote route bodies were taken from `server.py` itself).
It proves the page, the service logic and the workflow work together. It does not prove the FastAPI layer. To close that gap, run
`uvicorn application.server:app` and then `python scripts/e2e_ui_check.py` on your machine (needs `pip install playwright`).

Data is the demo seed plus one RFQ created by the test; nothing here is observed business data.

## Result: 34 of 34 steps passed (output of `scripts/e2e_ui_check.py`, re-run after the tier-rate and narrative fixes)

```
PASS Wrong password shows an error  [Wrong username or password]
PASS Signed-in user shown  [Estimator (Estimator)]
PASS Metric cards rendered (5)
PASS Finance case panel has content  [Lost-RFQ margin pool ₹86,40,000 Theoretical annual pool Base-case win-back 25.0%]
PASS KPI panel has content
PASS Analysis (queueing) panel has content
PASS Baseline (simulated) panel has content
PASS Audit panel has content
PASS Demo RFQs listed  [4 RFQs]
PASS Search with no match shows empty state
PASS New RFQ created and listed
PASS Cancel closes modal
PASS Close (X) closes modal
PASS Start costing moves RFQ to costing
PASS Edit assignment opens editor
PASS Composer opens with one part line
PASS Add part line works
PASS Remove part line works
PASS Cancel hides composer
PASS Calculate 3 volume prices creates a quote with 3 tiers  [1,80,000 UNITS / PART | ₹116.51 | Price / set · Cost ₹102.53 / set · GST ₹20.97 / set | Annual value ₹2,09,7
PASS API quote prices: 90,000 = 117.33, 180,000 = 116.51, 270,000 = 115.77  [{90000: '117.33', 180000: '116.51', 270000: '115.77'}]
PASS Quote shows an approval state  [Quote v1: Pending approval]
PASS Sign out shows login
PASS Send back with reason works (prompt)
PASS Sales head approves
PASS Estimator marks quote as sent
PASS Printable quotation opens
PASS Refresh does not error
PASS Audit trail records workflow events
PASS Trace import hidden for estimator
PASS Trace import visible for estimation head
PASS Trace import without file shows a message (not silent)  [Choose a CSV file first]
PASS Trace import of the template gives a clear result  [2 sent RFQs of 2. Median 3.11 days, 90th percentile 3.17. Costing is 38% of the cycle. Costing is 40% or less of 
PASS Role without permission gets a visible refusal  [Role 'sales_head' is not permitted for this action]
```

Only two HTTP errors occurred and both were intended: a wrong-password login (401) and a refused action by a role without permission (403).

## Static checks
- Every `/api/...` call made by `index.html` has a matching route in `server.py` (compared route by route; none missing).
- The printable quotation is opened with a bearer-token `fetch` and a blob URL, so it works despite the API needing an Authorization header.

## Prototype pages (`prototype/*.html`, opened in Chromium)
- `costing_demo.html`: 4 buttons, no page errors; each "Accept" changes the page and "Accept all high confidence" is a no-op once all are accepted.
- `approval_card.html`: buttons are disabled for the Estimator role by design. As Sales head, send-back without a reason is refused,
  send-back with a reason works, approve works, and the Deputy cannot hand over; no page errors.
- `business_dashboard.html`: all 12 buttons change the page; no script errors. It loads Google Fonts from the network, so offline it falls back to default fonts.

## Defects found
None in the application page or prototypes. Two apparent problems during testing were caused by the test script (a race reading storage and a page reload during
sign-out) and were fixed in the script, not the app.

## Not covered
Concurrency, multi-user timing, accessibility, mobile layout, and the FastAPI layer (see above).
