# MarginLadder
### Should a manufacturer fund RFQ-to-quote automation? A modelled investment case, with a working prototype.

**Suvam Priyaranjan Sahoo** · [GitHub](https://github.com/suvampriyaranjansahoo) ·
[LinkedIn](https://linkedin.com/in/suvam-priyaranjan-sahoo-18b7412bb) ·
[Portfolio](https://suvampriyaranjansahooportfolio.vercel.app)

> **Scope, stated up front.** The case is **hypothetical** (a Pune auto-components maker). It has **no production users**,
> **no real customer interviews**, no UAT sign-off and no realised savings. Rates and records are **synthetic**
> or assumption-led. Every figure below is a modelled scenario, not a measured result.

## The decision

Quotation cycle time is 9 working days against a 4-day target. Is a ₹8 lakh build justified?

**Recommendation: do not approve the full build yet.** Measure stage timestamps and rework first, pilot a reversible
queue-visibility and approval workflow, and automate costing only if data shows costing is the bottleneck.

## Headline numbers (all derived from `numbers.json`, each tagged Brief / Assumption / Derived)

| Metric | Value | Type |
|---|---:|---|
| Annual RFQs / lost at 5% | 720 / 36 | Brief, derived |
| Lost-RFQ contribution pool (₹20 lakh AOV, 12% margin) | ₹86.4 lakh | Derived |
| Recovered margin at 25% / 12.5% win-back | ₹21.6 / ₹10.8 lakh | Assumption |
| Operating payback (base / conservative) | 4.9 months / 10.9 months | Derived, pre-tax |
| Cash payback after tax and working capital | 23.6 months | Derived |
| Deepest cash need | ₹14.8 lakh | Derived |
| 3-year IRR (with / without working-capital release) | 75.8% / 43.0% | Derived |
| Break-even win-back (incl. run cost / fee only) | 11.6% / 9.3% | Derived |
| Estimator hours released (gross / net) | 5,400 / 4,680 | Derived, not cash |
| Estimator load today / target | 78% / 31% | Derived |
| Queue wait today | 0.57 day | Derived (queueing model) |
| Capacity break-even fit | 46% | Derived |

Read this carefully: the 4.9-month payback is operating and pre-tax. The cash view is 23.6 months. Released estimator
hours are capacity, not savings. The ₹86.4 lakh is a ceiling, not a forecast.

## What is built

| Layer | Where | What it shows |
|---|---|---|
| Financial model | `model/MarginLadder_Monthly_FP&A_Model.xlsx`, `finance/` | Driver-based monthly plan, about 490 formulas, tornado, audit checks |
| Python twin | `finance/reconcile.py` | Recomputes the workbook; 64 of 64 cells match |
| Decision layer | `finance/unit_economics.py`, `finance/scenarios.py` | Tier boundaries, cost-line shares, shock sensitivity, break-even volume, downside/base/upside, NPV threshold |
| Costing engine | `engine/cost_engine.py` | Decimal arithmetic, dated rate master, quote snapshots, visible errors |
| Workflow app | `application/` | FastAPI + SQLite, role-gated approvals, audit events, API and hardening tests |
| Analytics | `analytics/`, `tracekit/` | SQL findings, product metrics, RICE sensitivity, sample-size tools |
| Public-data check | `realdata/`, `docs/finance/real_company_benchmark.md` | Bharat Forge FY26 audited filing (NSE), recomputed ratios, DuPont, cash cycle, and the case's assumptions tested against them |
| Extension | `model/MarginLadder_finance_extension.xlsx` | DCF, reverse DCF, DuPont, comparables, decision tree |
| Documents | `docs/` | PRD, business rules, traceability, UAT scripts (not yet executed), RAID, deck |

## Run it

```bash
pip install -r requirements-dev.txt
pytest                                   # tests live inside each package
python -m finance.reconcile              # workbook vs Python, 64 cells
python -m realdata.benchmark             # real-company benchmark from the audited filing
python scripts/check_consistency.py      # figures in docs match numbers.json
python scripts/portfolio_release_audit.py
uvicorn application.server:app --reload  # local demo at http://127.0.0.1:8000
python scripts/e2e_ui_check.py           # optional browser check of the full workflow (needs playwright)
```

CI (`.github/workflows/ci.yml`) runs ruff, mypy, pytest with an 85% coverage gate and the checks above.

## Reality check on public data

The case is hypothetical, so I tested its assumptions against one real, audited filing: Bharat Forge (Pune), consolidated FY26,
copied from the NSE filing (`realdata/bharat_forge_fy26.py`, source link inside). Recomputed debt/equity matches the company's own 0.72.

| Case assumption | Case | Real reference | Reading |
|---|---:|---:|---|
| Quote margin | 12% | 17.4% EBITDA, 14.0% Forgings segment | Not aggressive |
| Material share of price | 38.7% | 45.1% of revenue | Close |
| Working capital days | 45 | 85 receivable days, 136-day cash cycle | **Light.** Re-run: IRR 75.8% falls to 44.4% and 28.4%; cash payback 1.96 to 2.33 and 2.54 years |
| EN8 steel rate | ₹78/kg | ₹58 to 70/kg typical in undated seller listings | Above typical; steel up 25 to 36% year on year |

One company, one year, a far larger business than the case's. Treat it as a range check, not proof. Details and limits:
`docs/finance/real_company_benchmark.md`.

## Evidence discipline

`docs/portfolio/evidence_ledger.md` tags every claim as Brief, Assumption, Derived, Built, Synthetic or Unverified, and
lists what is not claimed (adoption, deployment, realised benefit). `docs/portfolio/ai_use_disclosure.md` states where
AI assisted and how outputs were verified.

## Five-minute review

1. `docs/portfolio/one_page_brief.md`: decision, numbers, what would change the answer
2. `docs/portfolio/evidence_ledger.md`: claim traceability
3. `model/MarginLadder_Monthly_FP&A_Model.xlsx`: Inputs, Monthly Plan, Tornado, Audit Checks
4. `docs/finance/decision_bridge.md`, `docs/finance/model_audit.md` and `docs/finance/decision_layer_report.md`
5. `docs/validation/ui_workflow_check.md`: browser workflow test, with what it does and does not prove
6. Role lens (optional): `docs/portfolio/role_paths/`. The full earlier README is `docs/portfolio/README_extended.md`.

## Next step that would matter most

Interview three to five real estimators, sales or finance staff, log them with
`data/templates/discovery_interview_log_template.csv`, and re-run the model on observed stage times.
See `docs/portfolio/validation_plan.md`.
