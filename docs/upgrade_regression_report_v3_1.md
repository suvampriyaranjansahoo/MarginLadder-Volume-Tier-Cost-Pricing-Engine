# MarginLadder v3.1 — balanced upgrade and regression report

## Release scope

Source archive: the uploaded `MarginLadder_v3.zip`.

Release: **3.1.0**. This is an additive upgrade of v3, not a replacement. The deterministic costing engine, original finance workbooks and original browser prototypes are retained. Existing hypothetical inputs and simulated logs remain labelled as such.

## Changes delivered

### Engineering and data quality

- ASGI service creation is lazy and thread-safe. Importing `application.server` no longer creates a database or demo-credentials file.
- Trace timestamps retain ISO-8601 offsets. Offset-aware timestamps are compared as instants; mixed aware and naïve timestamps are rejected.
- Stage-level coverage is measured explicitly. Incomplete timestamps are not treated as zero-duration observations or silently used in stage-scope decisions.
- Customer holds are retained as a non-additive overlay because they can overlap the residual elapsed-time stage.
- Raw timestamp traces can be transformed directly into the SQL cycle schema. Open RFQs are excluded from completed-cycle analysis and incomplete stage pairs are rejected.
- CI and Makefile steps use cache-isolated commands so ordinary test runs do not create false consistency-check failures.

### Finance Analyst

- Added a Decimal-based monthly budget-versus-actual variance engine with revenue/cost favourability rules, zero-budget handling and a contribution bridge.
- Added a small simulated monthly sample and generated variance report. The contribution bridge is explicitly not EBITDA, operating profit or cash flow.

### APM / Product Analyst

- Added reproducible product-event analytics for distinct-RFQ conversion, quote turnaround, weekly active operators and weekly cohorts.
- Added metric definitions and a generated report. All supplied event rows are synthetic; there are no measured adoption or retention outcomes.

### Consulting Analyst

- Added a 10-slide executive case-deck storyboard with problem framing, issue tree, value pool, cash constraints, strategic options, evidence plan and decision gates.
- External market benchmarks or client outcomes have not been invented.

### Business Analyst

- Added an executed-evidence coverage matrix that separates automated software tests from business UAT.
- Business UAT remains pending; the existing UAT scripts are not represented as signed-off customer testing.

### Portfolio positioning

- Added role-specific evidence, interview walkthroughs and do-not-claim boundaries for Finance Analyst, APM, Consulting Analyst and Business Analyst.

## Validation performed in this environment

Environment: Python 3.13.5, FastAPI 0.128.2, httpx 0.28.1, Pydantic 2.13.5, pytest 9.0.2 and pytest-cov 7.0.0.

| Check | Result |
|---|---:|
| Pytest suite with coverage | **150 passed** |
| Aggregate coverage | **91.79%** (configured minimum: 85%) |
| Original deterministic costing engine | **24/24 passed** |
| Excel / Python finance reconciliation | **64/64 cells matched** |
| Finance variance report generation | Passed; 12 metric-period rows |
| Product analytics report generation | Passed |
| Default SQL analytics report generation | Passed; simulated sample retained as simulated |
| Raw trace CLI smoke test | Passed on `tracekit/rfq_trace_template.csv` (2 rows) |
| Trace-to-SQL tests | Included in pytest suite; passed |
| Python AST parse | Passed |

The pytest run emitted one SQLite `ResourceWarning` during garbage collection despite all tests passing. It is recorded as a cleanup warning, not suppressed or represented as a test failure. No application assertion failed.

## Static-analysis and platform limits

- Ruff and mypy executables were not installed in this offline execution environment. An installation attempt could not reach package indexes. The GitHub Actions workflow is configured to run these checks, but they are **not claimed as locally passed**.
- The local regression run used Python 3.13.5 only. The configured CI matrix is broader; other Python versions were not executed here.
- No Docker build, hosted deployment, production traffic or live user acceptance run is claimed.

## Evidence and remaining limitations

- The automotive manufacturer, business brief, baseline economics and forecast assumptions remain hypothetical case-study inputs.
- The RFQ and product-event sample datasets are simulated. The new variance dataset is also simulated.
- No customer interviews, signed requirements, customer UAT, pilot, live adoption, measured cycle-time improvement or realised margin recovery are evidenced.
- Financial workbook reconciliation verifies that the Python twin matches the workbook; it does not validate the assumptions or certify third-party market/comparable data.
- The contribution bridge is not a full income statement. The monthly variance tool is an analytical demonstration, not a substitute for an audited ERP close or finance-control process.
- Product funnel and cohort metrics demonstrate instrumentation and calculation methods, not actual product-market fit.

## Recommended next evidence step

The highest-value next step is a small, permissioned validation exercise: interview representative estimator, sales and approver users; validate the workflow and metric definitions; execute documented UAT; and collect timestamped pilot observations. Only then should any operational benefits or adoption outcomes be stated as observed results.
