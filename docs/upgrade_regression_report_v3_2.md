# v3.2 recruiter-focused release — regression and evidence report

**Release date:** 18 November 2026  
**Portfolio package:** 3.2.0  
**Application API:** 3.1.0 (retained intentionally; no API-version change in this additive portfolio release)  
**Evidence status:** local reproducible tests and model checks only. No live customer, user, stakeholder or production evidence is claimed.

## Release scope

This release is an additive improvement to the inspected v3.1 baseline. It retains the original Decimal costing engine, original finance workbooks, browser prototypes, local FastAPI/SQLite application and its role / approval / audit behaviour. It adds:

- A monthly driver-based FP&A workbook and matching Decimal-based Python plan with a 12-period scenario, blank actuals, deterministic sensitivity, control checks and source lineage.
- Role-specific walkthroughs for Finance Analyst, Business Analyst, Consulting Analyst and Associate Product Manager.
- A 13-slide answer-first consulting recommendation deck and an India auto-components source note using current industry context with comparability caveats.
- BA discovery/UAT and APM discovery/usability execution packs, plus blank CSV evidence templates.
- A release evidence matrix, one-minute recruiter brief, AI-use disclosure, final real-world execution checklist and this regression report.

## Reproducible validation

The commands below were run from the project root in the current Linux/Python environment. Exact final counts are recorded after the release regression run.

| Check | Result |
|---|---|
| `pytest -q` | **159 passed** |
| `python3 engine/cost_engine.py` | 24/24 costing reference checks passed |
| `python3 -m finance.reconcile` | 64/64 legacy finance workbook / Python reconciliation cells matched |
| `python3 -m finance.monthly_plan` | Base-case totals reconcile to the case assumptions; 12 periods produced |
| `python3 -m finance.variance` | 12 metric-period rows generated; sample values remain labelled simulated |
| `python3 -m analytics.product_metrics` | Synthetic event-analysis method run completed |
| `python3 scripts/check_consistency.py` | **542 / 542 checks passed** |
| Consulting deck render / overflow test | **13 slides rendered; overflow test passed** |
| FP&A workbook formula scan | Zero common spreadsheet formula-error tokens found in the artifact-tool calculation snapshot |

## Finance model correction and controls

The v3.2 monthly workbook sensitivity formulas were reviewed against the driver chain. Incremental revenue now uses recovered RFQs multiplied by average order value; contribution then applies contribution margin. The base case is:

- 720 annual RFQs; 36 assumed lost RFQs; 9 assumed recovered RFQs at 25% win-back.
- ₹86.4 lakh theoretical lost-RFQ margin pool; ₹180 lakh incremental revenue; ₹21.6 lakh contribution.
- ₹2 lakh annual run cost and ₹19.6 lakh net contribution after run cost.
- 4.9 months' operating payback after annual run cost; 11.57% first-year break-even win-back including the one-time implementation cost and annual run cost.
- ₹11.6 lakh simplified 12-month project cash proxy after the ₹8 lakh setup cost, before tax and working capital.

The workbook actual column is blank by design. The simplified proxy is not EBITDA, statutory cash flow or free cash flow. The existing full finance model retains the separate 23.6-month tax-and-working-capital cash payback scenario. Reconciliation proves calculation consistency, not the truth of the brief assumptions.

## External research and source discipline

The deck and source register include ACMA FY25 sector data, ICRA's 28 September 2026 FY27 outlook, and examples from FY25 primary annual reports. Industry / listed-company material is context only; it is not a market-size estimate or direct SME margin / valuation benchmark. Publication dates, primary links and interpretation limits are included in `docs/portfolio/research_source_register.md` and `docs/research/india_auto_components_context_2026.md`.

## Evidence that remains open

This package does **not** contain completed customer or practitioner interviews, moderated usability results, executed business UAT, client approval, production deployment, real RFQ data, realised time savings, recovered orders, margin uplift or product adoption. The four execution templates are intentionally header-only. These external activities must be completed with permission and recorded before the corresponding claims can be made.

## Tooling limits

Ruff and mypy were not run because their command-line tools are not installed in this execution environment. No lint or static-type-check pass is claimed. A clean test suite does not replace security review, deployment review, accounting review, independent user research or a real pilot. Do not describe this release as recruiter-certified or assign it a guaranteed interview / hiring probability.
