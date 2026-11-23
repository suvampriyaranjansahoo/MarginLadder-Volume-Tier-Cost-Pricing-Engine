# Monthly FP&A planning model — workbook guide

**Workbook:** `model/MarginLadder_Monthly_FP&A_Model.xlsx`  
**Planning horizon:** April 2027–March 2028, purely illustrative.  
**Model status:** assumption-driven scenario plan; no actuals are loaded.

## Workbook structure

| Sheet | Purpose | Key controls |
|---|---|---|
| Dashboard | Annual operating volume, economics, payback and model-status summary | Labels the case and excludes tax / working capital from the operating cash proxy |
| Inputs | One place for brief inputs and model assumptions | Editable hardcodes use blue font and yellow fill; assumptions are tagged |
| Monthly Plan | 12 monthly driver calculations | Monthly RFQ volume is editable; one-time implementation cost is charged once in period 1 |
| Variance | Actual-vs-budget framework | Actual cells are blank by design; variance remains `Pending` until verified actuals are entered |
| Sensitivity | Win-back cases from 5% to 50% | Deterministic scenario analysis; not a probability distribution |
| Control Checks | Annual arithmetic tie-outs | Expected base-case checks must show `PASS` |
| Sources | Local input lineage and external industry/peer context | URLs and comparability warnings are visible inside the workbook |

## Formula chain

1. `Annual RFQs = monthly RFQs × 12`.
2. `Lost RFQs = annual RFQs × lost-RFQ rate`.
3. `Lost-RFQ margin pool = lost RFQs × average order value × contribution margin`.
4. `Assumed recovered RFQs = lost RFQs × win-back rate`.
5. `Incremental revenue = assumed recovered RFQs × average order value`.
6. `Contribution = incremental revenue × contribution margin`.
7. `Net contribution after run cost = contribution − annual run cost`.
8. `Operating payback = one-time implementation cost ÷ annual net contribution × 12`.

## Base-case checks

| Metric | Expected value |
|---|---:|
| Annual RFQs | 720 |
| Annual lost RFQs | 36 |
| Theoretical lost-RFQ margin pool | ₹86,40,000 |
| Recovered contribution at 25% win-back | ₹21,60,000 |
| Annual run cost | ₹2,00,000 |
| Annual net contribution after run cost | ₹19,60,000 |
| Operating payback | 4.9 months |
| Simplified 12-month project cash proxy after ₹8 lakh setup cost | ₹11,60,000 |

The monthly workbook's 4.9-month payback matches the existing `numbers.json` operating-payback convention. It is not the 23.6-month tax-and-working-capital cash payback from `finance/full_model.py`.

## Deliberate exclusions

The monthly workbook is not a full three-statement model or statutory forecast. It excludes taxes, financing, depreciation schedules, inventory, receivables/payables build, balance-sheet integrity, seasonal mix, ramp-up, price/mix effects and actual ledger values. The 25% tax, 45 working-capital days, three-year amortisation and 12% discount rate appear on Inputs only as context references to the existing long-form scenario model; they do not drive the monthly cash proxy. Tax and accounting treatment require professional validation.

The annual recovered contribution is not EBITDA, free cash flow or cash recovered. The new workbook is a monthly operating-plan and variance framework designed to complement, not replace, the existing full financial model.

## Update procedure

1. Change blue/yellow input cells only after documenting the source and classification.
2. Replace monthly RFQ volume only with a dated, approved forecast driver.
3. Enter actuals in the yellow Actual column only after reconciliation to the source ledger.
4. Investigate favourable/unfavourable variances by volume, mix, price/rate, efficiency and timing; do not stop at percentages.
5. Re-run `finance.monthly_plan`, workbook control checks and the repository test suite after formula or input changes.
