# Finance Analyst path — MarginLadder

## Recruiter takeaway

A driver-based operating case with a deterministic calculation trail, explicit assumptions, sensitivity, cash caveats and a monthly budget/actual framework.

## 5-minute inspection route

1. Open `model/MarginLadder_Monthly_FP&A_Model.xlsx` → Dashboard, Inputs, Monthly Plan, Variance, Sensitivity, Control Checks, Sources.
2. Read `docs/finance/monthly_planning_model.md` for the formula chain and scope limits.
3. Run `python3 -m finance.monthly_plan` and `python3 -m finance.reconcile`.
4. Inspect `finance/test_monthly_plan.py`, `finance/full_model.py` and `docs/finance/model_audit.md`.

## Demonstrated competencies

- Driver-based RFQ, lost-quote, win-back, revenue and contribution model.
- Monthly plan and variance framework with actuals intentionally blank.
- Decimal arithmetic, validation and deterministic tests.
- Scenario sensitivity, payback and break-even analysis.
- Separation of contribution, EBITDA, tax, working capital and theoretical capacity value.
- Source lineage and explicit warnings against treating synthetic data as actuals.

## 60-second walkthrough

“I framed a hypothetical RFQ turnaround problem as an operating and financial decision rather than assuming that automation itself creates value. I linked RFQ volume, the lost-quote rate, order value, contribution margin and a win-back assumption to an annual value pool, then challenged the assumption with a break-even calculation. I added a monthly driver-based plan and an actual-versus-budget framework where actual cells remain blank until there is a reconciled source. The operating payback is 4.9 months in the 25% win-back case, but that is pre-tax and before working capital; the full model's cash payback is longer. The main limitation is that the company and baseline are hypothetical, so I present these as modelled scenarios, not realised savings.”

## Questions to be ready for

- Why is the ₹86.4 lakh value pool not revenue? It is 36 hypothetical lost RFQs × ₹20 lakh order value × 12% contribution margin.
- Why is ₹21.6 lakh not an outcome? It assumes a 25% win-back rate with no observed customer data.
- Why is released estimator time not cash savings? It becomes cash only if it reduces cost or enables incremental work that can be fulfilled.
- Why not compare P/E or EV/EBITDA with a large public company? No common valuation date, segment perimeter, accounting basis or comparable business mix has been established.
- What would make the forecast decision-grade? Approved drivers, ledger reconciliation, capacity confirmation, sensitivity and independent model review.

## Honest claim boundary

Claim the model architecture, calculations, formulas, tests and scenario analysis you can explain and reproduce. Do not claim actual cost savings, realised margin, improved company forecast accuracy or finance-team adoption.

## Added in 3.3.1: valuation drill
`model/MarginLadder_finance_extension.xlsx` has five-year DuPont and ROIC for a listed auto-component maker, a bear/base/bull DCF at an 11.8% WACC, a reverse DCF and six peers. It is a method exercise on public data, not a view on any stock. Be ready to say why ROIC (12.6%) sits close to WACC and what that means for the DCF.


## Five-minute evidence pack

`docs/finance/finance_manager_reproduction_pack.md` and the workbook `Audit Checks` sheet.
