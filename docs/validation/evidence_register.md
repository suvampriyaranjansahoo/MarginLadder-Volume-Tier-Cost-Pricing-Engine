# MarginLadder evidence register

This register separates the provenance and strength of project claims. It is intended to prevent assumptions, calculations and simulated examples from being described as client outcomes.

| Claim / figure | Classification | Evidence source | Confidence / caveat | Permitted wording |
|---|---|---|---|---|
| 60 RFQs per month | Brief | Hypothetical case brief captured in project docs | Not verified against a live company | “The case brief assumes 60 RFQs/month.” |
| 5 parts per RFQ | Brief | Hypothetical case brief | Confirm actual distribution in discovery | “The brief uses five parts per RFQ.” |
| 2.5 hours per part; 1-hour target | Brief / target | Hypothetical case brief | Needs time study | “The brief states 2.5 hours and targets one hour.” |
| 9 working-day cycle; 4-day target | Brief / target | Hypothetical case brief | No raw timestamp extract supplied | “The brief states a nine-day cycle and a four-day target.” |
| 1.56 days hands-on costing | Derived | 5 parts × 2.5 h ÷ 8 h/day | Arithmetic, not a measurement of all work | “Costing equates to 12.5 hours, or 1.56 eight-hour days.” |
| Remaining 7.44 days | Derived residual | 9 − 1.56 | Not a measured wait-time split | “The residual cycle time needs stage-level validation.” |
| Stage wait means and 60-RFQ chart | Simulated | `data/simulate_rfq_log.py`, `data/simulated_rfq_log.csv` | Assumed distributions and stage means | “Synthetic illustration only.” |
| 5% RFQ loss rate | Brief | Hypothetical case brief | Definition may include no-bids / capacity rejections | “The brief uses a 5% loss assumption.” |
| ₹86.4 lakh lost-RFQ margin pool | Derived | 720 × 5% × ₹20 lakh × 12% | Depends on average order value and margin definitions | “Theoretical margin pool under brief inputs.” |
| 25% win-back | Assumption | 50% delay attribution × 50% conversion | No customer cohort evidence | “Base-case assumption, to validate.” |
| ₹21.6 lakh recovered margin | Derived from assumption | ₹86.4 lakh × 25% | Not realised company benefit | “Illustrative annual margin-recovery scenario.” |
| ₹24.3 lakh capacity value | Derived from brief | 5,400 hours × ₹450 | Not booked cash savings; not added to main case | “Theoretical value of released estimator capacity.” |
| ₹8 lakh build fee / ₹2 lakh annual run cost | Proposal / assumption | Project business case | Vendor quote not contracted | “Proposed / assumed project economics.” |
| 24/24 costing engine tests | Build evidence | `engine/cost_engine.py` and `engine/test_results.txt` | Unit tests on illustrative inputs; not client parity | “24 reference engine tests pass.” |
| Automated regression suite | Build evidence | `application/tests/`, `tracekit/tests/`, `finance/`, `analytics/` | Current release suite is executed with the installed FastAPI stack in the local verification environment; the v3.2 count, coverage and environment are recorded in `docs/upgrade_regression_report_v3_2.md` | Quote the tested suite count and environment only from the latest report. |
| 64 of 64 Excel cells reproduced in Python | Build evidence | `finance/reconcile.py` | Proves arithmetic and wiring, not the assumptions | “The Python twin matches the Excel model cell by cell.” |
| Finance-module automated tests (48 in v3.2) | Build evidence | `finance/test_case_model.py`, `finance/test_full_model.py` | Case math, full model, queue and capacity | “48 finance-module tests are included in the 160-test v3.2 suite.” |
| Browser RFQ register and approval workflow | Build evidence | FastAPI + SQLite + static UI | Local demo with sign-in and server-side roles; no live users or integration | “Working local MVP demonstrates the workflow.” |
| AI extraction | Proposed / simulated | Existing costing prototype and PRD | No OCR / LLM service is implemented | “AI-assisted extraction is a proposed capability; current values are manually entered / simulated.” |
| Queue wait 0.57 day; capacity break-even 46% | Derived | `finance/queueing.py`, `finance/capacity.py` | Erlang C pressure gauge on brief inputs and assumptions A4, A5 | “Model estimate, not a measurement.” |
| SQL findings and RICE ranking | Simulated | `analytics/` | SQL runs on a simulated cycle log or raw trace input; the sample report remains simulated | “Method demonstration only.” |
| Monthly actual-versus-budget variance engine | Simulated | `finance/variance.py`, `data/finance_actual_vs_budget_sample.csv` | Decimal calculations and favourability rules tested on synthetic rows; contribution proxy is not EBITDA | “Built a monthly variance-analysis tool; example rows are simulated.” |
| Product funnel and operator cohorts | Simulated | `analytics/product_metrics.py`, `data/product_events_sample.csv` | Event definitions and calculations tested on synthetic events; no active users or adoption results | “Defined product instrumentation and built a reproducible simulated funnel/cohort analysis.” |
| Raw trace to SQL workflow | Build evidence | `tracekit/`, `analytics/run_queries.py` | Complete sent rows are transformed; incomplete stage timestamp pairs are rejected; customer holds remain a non-additive overlay | “Built a reproducible event-trace-to-SQL pipeline with explicit data-quality gates.” |
| Production adoption / time reduction / won business | Not evidenced | No production pilot or client data | Do not claim | “Not yet measured.” |

## 1. Evidence hierarchy

1. **Observed production evidence:** timestamp logs, signed customer data, live usage and independently reconciled results. None is present in this case study.
2. **Build evidence:** source code, automated tests, API behaviour and reproducible local runs.
3. **Brief inputs:** values supplied in the hypothetical business case.
4. **Derived values:** deterministic calculations from brief inputs.
5. **Assumptions:** win-back, operating cost, working capital, ramp and forecast distributions.
6. **Judgement:** prioritisation, recommended gates and the decision to stage.
7. **Synthetic data:** generated to demonstrate the method; never a business finding.

## 2. Resume / interview claim control

Good: “Built a local RFQ workflow MVP with a tested deterministic costing engine, three-tier pricing, quote version snapshots, role-gated approval actions and audit events; developed a financial case with explicit assumptions and scenario analysis.”

Avoid: “Reduced client quote turnaround by 56%,” “recovered ₹21.6 lakh,” “built and deployed AI extraction,” or “saved ₹24.3 lakh,” because none of those outcomes has been observed in a live operation.
