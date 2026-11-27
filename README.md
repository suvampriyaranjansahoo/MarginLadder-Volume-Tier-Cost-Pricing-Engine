# MarginLadder
### RFQ-to-quote intelligence: a working workflow app, costing engine, and investment case

**Suvam Priyaranjan Sahoo** · [GitHub](https://github.com/suvampriyaranjansahoo) · [LinkedIn](https://linkedin.com/in/suvampriyaranjansahoo-18b7412bb) · [Portfolio](https://suvampriyaranjansahooportfolio.vercel.app)

> **Portfolio case, not a production claim.** MarginLadder models a hypothetical Pune auto-components manufacturer. The records, rates and business-case inputs are synthetic or assumption-led; no production users, customer interviews, UAT sign-off, deployment, or realised savings are claimed.

## See the product output

This is a locally runnable, interactive portfolio MVP. Recruiters can see the workflow, financial decision outputs and audit trail—not just documentation.

![MarginLadder interactive dashboard demo](docs/dashboard_demo.gif)

### Dashboard views

<p align="center">
  <img src="docs/dash_overview.png" alt="RFQ operations overview dashboard" width="49%" />
  <img src="docs/dash_ops.png" alt="Operations dashboard with workflow measures" width="49%" />
</p>
<p align="center">
  <img src="docs/dash_decision.png" alt="Investment decision dashboard" width="49%" />
  <img src="docs/dash_risk.png" alt="Risk and sensitivity dashboard" width="49%" />
</p>

The interactive dashboard surfaces:

- RFQ status, owners, due dates, approval queue and quote activity
- Reproducible tiered costing and versioned quote snapshots
- Business-case economics, payback and win-back sensitivity
- Application KPIs, queue analysis and an append-only audit trail
- Explicit labels separating application data, simulated diagnostics and assumption-based financial outputs

For a role-by-role recruiter review, see the [recruiter evidence plan](docs/portfolio/recruiter_excellence_plan.md). The [forging economics simulator](docs/finance/forging_economics_simulator.md) documents the new interactive sector sensitivity view and its limits.

## The decision

Quotation cycle time is modelled at 9 working days against a 4-day target. Is an ₹8 lakh build justified?

**Recommendation: do not approve the full build yet.** First capture stage timestamps and rework, then pilot a reversible queue-visibility and approval workflow. Automate costing only if observed data shows it is the bottleneck.

## Headline outputs

| Metric | Modelled output | Classification |
|---|---:|---|
| Annual RFQs / lost at 5% | 720 / 36 | Brief / derived |
| Lost-RFQ contribution pool | ₹86.4 lakh | Derived |
| Recovered margin at 25% / 12.5% win-back | ₹21.6 / ₹10.8 lakh | Assumption-led |
| Operating payback (base / conservative) | 4.9 / 10.9 months | Derived, pre-tax |
| Cash payback after tax and working capital | 23.6 months | Derived |
| 3-year IRR (with / without working-capital release) | 75.8% / 43.0% | Derived |
| Estimator hours released (gross / net) | 5,400 / 4,680 | Derived; capacity, not cash |

The operating-payback result is not the cash result. The contribution pool is a ceiling, not a forecast. Full claim traceability is in [the evidence ledger](docs/portfolio/evidence_ledger.md).

## Run the interactive demo

```bash
pip install -r requirements-dev.txt
uvicorn application.server:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). On first use, the app creates a local SQLite demo database with fictional RFQs and demo credentials at `application/data/demo_credentials.txt` (gitignored).

Suggested recruiter walkthrough:

1. Sign in with a demo account and inspect the RFQ workspace and KPI cards.
2. Choose an RFQ, calculate three volume prices, and review the saved quote snapshot.
3. Sign in as Sales Head or Deputy to approve a quote over the illustrative ₹25 lakh threshold.
4. Review business-case economics, sensitivity, queue analysis and the activity trail.
5. Open the original [finance dashboard](http://127.0.0.1:8000/prototype/business_dashboard.html) for an additional interactive decision view.

## What is built

| Layer | Location | Evidence of capability |
|---|---|---|
| Workflow application | `application/` | FastAPI + SQLite, role-gated approvals, audit events and dashboard APIs |
| Costing engine | `engine/cost_engine.py` | Decimal arithmetic, dated rates, tier pricing and quote snapshots |
| Financial model | `model/`, `finance/` | Driver-based monthly plan, cash view, NPV/IRR, tornado and reconciliation |
| Decision layer | `finance/unit_economics.py`, `finance/scenarios.py` | Sensitivity, break-even volume, downside/base/upside scenarios |
| Analytics | `analytics/`, `tracekit/` | SQL findings, product metrics, queue and sample-size tools |
| Documentation | `docs/` | PRD, rules, traceability, UAT design, finance and delivery evidence |

## Validation

```bash
pytest
python -m finance.reconcile
python -m realdata.benchmark
python scripts/check_consistency.py
python scripts/portfolio_release_audit.py
```

The Python reconciliation recomputes the financial workbook; the current check matches 64 of 64 cells. CI runs formatting, type checks, tests, coverage and portfolio consistency checks.

## Five-minute review

1. [One-page brief](docs/portfolio/one_page_brief.md) — recommendation and decision logic
2. [Evidence ledger](docs/portfolio/evidence_ledger.md) — what is built, derived, assumed or unverified
3. `model/MarginLadder_Monthly_FP&A_Model.xlsx` — driver-based plan, tornado and audit checks
4. [Decision bridge](docs/finance/decision_bridge.md) and [financial model audit](docs/finance/model_audit.md)
5. [UI workflow check](docs/validation/ui_workflow_check.md) — browser workflow evidence and limits

## Recruiter role lenses

| Role | Walkthrough |
|---|---|
| Product Finance Analyst | [Investment economics, cash and payback](docs/portfolio/role_paths/product_finance_analyst.md) |
| Finance Analyst | [FP&A, variance and reconciliation](docs/portfolio/role_paths/finance_analyst.md) |
| Business Analyst | [Process, requirements and UAT](docs/portfolio/role_paths/business_analyst.md) |
| Associate Product Manager | [Problem framing, MVP and metrics](docs/portfolio/role_paths/apm.md) |
| Consulting Analyst | [Options, recommendation and market sizing](docs/portfolio/role_paths/consulting_analyst.md) |
| Project / Programme Manager | [Delivery, governance and critical path](docs/portfolio/role_paths/project_manager.md) |

## Reality check and next step

The case assumptions were range-checked against Bharat Forge’s FY26 audited public filing; see [the benchmark note](docs/finance/real_company_benchmark.md). It is one much larger company and one year—use it as a range check, not proof.

The highest-value next step would be interviews with three to five estimators, sales or finance staff, followed by measured stage-time logging using `data/templates/discovery_interview_log_template.csv`. See [the validation plan](docs/portfolio/validation_plan.md).
