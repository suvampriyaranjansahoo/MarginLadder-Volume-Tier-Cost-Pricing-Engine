# Product Finance Analyst — recruiter walkthrough

## Recruiter takeaway

This case demonstrates how to translate a workflow-product proposal into adoption-adjusted contribution, operating economics and cash consequences. It is a hypothetical case, not a client investment decision.

## 60-second walkthrough

The brief describes 720 RFQs per year and an assumed 5% lost-RFQ rate. At ₹20 lakh average order value and 12% contribution margin, the theoretical lost-RFQ contribution pool is ₹86.4 lakh. I do not treat that pool as recoverable. The base case decomposes effective win-back into 62.5% adoption multiplied by 40% incremental lift among adopted eligible RFQs, or 25%. That produces ₹21.6 lakh modelled incremental contribution before the ₹2 lakh annual run cost. The operating payback proxy is 4.9 months before tax and working capital; the separate cash model estimates 23.6 months under its assumptions. Because delay attribution, incremental lift and fulfilment capacity are unvalidated, the recommendation is a capped measurement-led pilot, not broad rollout.

## Evidence to open

1. `model/MarginLadder_Monthly_FP&A_Model.xlsx` — Inputs, Adoption Economics, Monthly Plan, Sensitivity and Control Checks.
2. `docs/finance/decision_bridge.md` — investment logic and decision gates.
3. `docs/finance/model_audit.md` — cash/operating distinction and limitations.
4. `finance/full_model.py` and `finance/reconcile.py` — reproducible cash calculations and legacy model reconciliation.

## Questions to be ready for

- How would you estimate incremental lift rather than correlation?
- Why does the base scenario not justify full rollout?
- How do capacity, product mix and working capital change the economics?
- Which variable has the greatest effect on break-even adoption?

## Honest claim boundary

The 25% effective win-back is an explicit assumption. The ₹21.6 lakh is modelled contribution, not realised revenue or profit. No real customer, production or pilot evidence is claimed.

## Added in 3.3.1: stress the 25%
Open `model/MarginLadder_finance_extension.xlsx`, sheets `Win-back` and `MarginLadder link`. The 25% is split into 50% of losses due to delay times 50% faster-quote wins. The case fails in 6 of 30 grid cells, and a 6-month ramp moves payback from 4.9 to 7.9 months [Derived]. Working-capital days seen in listed peers run from −12 to 115 (median 22), and IRR stays at or above 33% across that range.
