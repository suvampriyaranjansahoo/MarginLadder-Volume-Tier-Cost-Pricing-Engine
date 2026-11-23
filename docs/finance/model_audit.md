# Finance model audit

Scope: `model/MarginLadder_finance_model.xlsx` (6 sheets). The finance extension workbook (10 sheets, Endurance and six peers) is described at the end.
Method: an independent Python twin (`finance/full_model.py`) is compared with the saved Excel values, cell by cell.

## Result
`python3 -m finance.reconcile` compares **64 cells** and all 64 match: Model B5 to B20, Sensitivity rows 4 to 12, Financials (revenue, EBITDA, tax, free cash flow by year, IRR, NPV, payback, deepest cash need, IRR without working-capital release) and Cash (funded gap by week, peak, week of peak). A test (`test_every_python_cell_matches_the_excel_workbook`) fails if any cell drifts. Excel and Python were built from the same assumptions, so this proves the arithmetic and the wiring, not the assumptions.

## Structure
| Sheet | Role | Reads from |
|---|---|---|
| Inputs | All inputs (yellow cells, blue text), scenario switch, source tag per row | n/a |
| Model | Cash case, capacity case, payback, break-even, 3-year NPV | Inputs |
| Sensitivity | Win-back from 0% to 50% against payback and NPV | Inputs |
| Financials | Incremental P&L, cash flow and balance sheet, IRR, NPV | Inputs, Model |
| Cash | Vendor funded gap by week on cash received | Inputs |
| Checks | Nine integrity checks, all PASS | All |

Inputs, calculations and outputs are separate. Every input has a source tag (Brief or Assumption). The balance sheet balances in every year (Financials row 38).

## Findings
| # | Finding | Severity | Status |
|---|---|---|---|
| 1 | Years 1 to 3 are flat. Benefits start on day one in the base case. | Medium | Disclosed. With a 6-month ramp, margin payback is 7.9 months, not 4.9 (extension, MarginLadder link). |
| 2 | The fee is taken before GST. If input credit is not available, payback is 5.8 months. | Low | Disclosed in the business review. |
| 3 | Payback of 4.9 months ignores tax and working capital. The cash view gives 23.6 months, IRR 75.8%, and a deepest cash need of ₹14.8 lakh. | High if misquoted | Both shown side by side. |
| 4 | The base case counts margin on every recovered order. Plant capacity is untested. | High | New: `capacity_and_queue.md`, year-1 break-even needs 46% of the margin to be makeable. |
| 5 | Freed estimator time is gross (5,400 h). The register adds a review step of about 720 h. | Medium | New: net 4,680 h, ₹21.06 lakh. Both are in `numbers.json`. |
| 6 | Working-capital days (45) and tax (25%) are assumptions. | Medium | Tested against listed firms in the extension: IRR stays above 33% across the observed range. |
| 7 | IRR of 75.8% assumes working capital is released in year 3. If it never is, IRR is 43.0% (Financials B47). | Medium | Both quoted. Use 43.0% with a CFO who doubts the release. |
| 8 | The v2 case notes say a ₹1 to 2 lakh Excel fix "closes about a quarter of the gap". The full costing screen saves 0.94 of the 5 days, about 19%. A smaller fix closes less. | Low | The quarter is a judgement, not derived. Do not quote it. |
| 9 | The model has no formal sign-off or version log inside the workbook. | Low | This audit and `numbers.json` serve as the record. |

## What the Python twin does not cover
- The finance extension (DCF, reverse DCF, comps, decision tree, market sizing). It uses aggregator data, not the annual report. The business review says to verify against the BSE filings before quoting.
- The 4,000-run simulation in `prototype/business_dashboard.html`. Its ranges are assumptions. The Python twin is deterministic.

## What would make a CFO say no
| Objection | Number | Where it bites |
|---|---|---|
| "Your 25% is a guess." | The case breaks even at 11.6% (9.3% before running cost). It fails in 6 of 30 combinations of the two factors behind the 25%. | Lost-RFQ coding in Week 1 |
| "The plant is full." | Needs 46% of recovered margin to be makeable. | Plant head's capacity answer |
| "Your payback is 5 months?" | Cash payback is 23.6 months after tax and working capital. | Quote 23.6, not 4.9, to a CFO |
| "The saved hours are not saved money." | They are upside only; the case does not count them. | Decision D-03 |
| "Why should I trust the numbers?" | 64 of 64 cells reconcile; every figure carries a tag. | `finance/reconcile.py` |


## Monthly variance-analysis extension (v3.1)

`finance/variance.py` calculates metric-level budget-versus-actual variance, percentage variance, correct revenue/cost favourability direction and a monthly contribution bridge. The bundled `data/finance_actual_vs_budget_sample.csv` is explicitly **SIMULATED**. The output is `docs/finance/monthly_variance_analysis.md`. The contribution proxy is revenue less the listed cost categories; without depreciation, financing, tax, balance-sheet and cash-timing details it must not be called EBITDA, net profit or cash flow.
