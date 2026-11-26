# Finance manager reproduction pack

**Purpose:** reproduce the core investment numbers and identify the model limits.  
**Reader:** Finance Analyst, FP&A manager and recruiter.  
**Recruiter conclusion:** the arithmetic is transparent, actuals are not fabricated and operating payback is not confused with cash payback.  
**30-second explanation:** “The ₹86.4 lakh figure is a theoretical pool. A 25% assumed win-back gives ₹21.6 lakh modelled contribution; less ₹2 lakh run cost gives ₹19.6 lakh operating contribution. The 4.9-month operating payback is not the 23.6-month cash payback.”

## 1. Model map
Workbook: `model/MarginLadder_Monthly_FP&A_Model.xlsx`

| Sheet | Key cells / ranges | Purpose |
|---|---|---|
| Dashboard | B5:B9, D5:D9, F5:F9 | Executive outputs and payback |
| Inputs | B5:B20 | RFQ volume, loss rate, AOV, margin, win-back, fee and run cost |
| Monthly Plan | B5:H16 | Monthly RFQs, lost RFQs, recovered RFQs, contribution and net |
| Variance | D5:H52 | Budget/actual/variance; actual inputs remain blank |
| Sensitivity | A5:G12 | Scenario changes to key drivers |
| Control Checks | A4:D9 | Existing formula checks |
| Sources | A4:F12 | Driver source and assumption notes |
| Adoption Economics | A4:H7 | Adoption × incremental lift decomposition |

`python scripts/validate_monthly_workbook.py` independently recalculates the base case. It does not run Excel's formula engine.

## 2. Hand number bridge
1. Annual RFQs = 60 per month × 12 = 720.
2. Lost RFQs = 720 × 5% = 36.
3. Contribution per average order = ₹20,00,000 × 12% = ₹2,40,000.
4. Theoretical lost-RFQ contribution pool = 36 × ₹2,40,000 = **₹86,40,000 (₹86.4 lakh)**.
5. Assumed effective win-back = 25%. In the adoption bridge, this is 62.5% adoption × 40% incremental lift = 25%; both are assumptions.
6. Modelled recovered RFQs = 36 × 25% = 9.
7. Modelled recovered contribution = 9 × ₹2,40,000 = **₹21.6 lakh**.
8. Less annual run cost ₹2 lakh = **₹19.6 lakh net operating contribution**, before tax and working capital.
9. Operating payback = ₹8 lakh implementation fee ÷ ₹19.6 lakh annual net operating contribution × 12 = **4.9 months**.
10. Full cash payback = **23.6 months** in the separate full model. It includes tax and working-capital timing and cannot be derived from the simple operating ratio. Reconcile with `python -m finance.reconcile` (64/64 selected cells matched).

## 3. Synthetic month-end variance commentary
The following is an illustrative teaching example. It is not company actuals and must not be pasted into actuals cells.

| Driver | Budget | Synthetic actual | Variance | Commentary |
|---|---:|---:|---:|---|
| RFQ volume | 60 | 54 | -6 / -10% | Volume shortfall reduces the eligible opportunity pool. Do not attribute it to conversion. |
| AOV | ₹20L | ₹19L | -₹1L / -5% | Possible price or customer mix effect; split only after product/customer detail. |
| Contribution margin | 12.0% | 11.5% | -0.5 percentage point | Check material rate, process cost, scrap and discount mix. |
| Lost-RFQ rate | 5.0% | 6.0% | +1 percentage point | More losses than plan; classify price, timing, capacity and product reason. |
| Quote timing | 4-day target | 6-day example | +2 days | Period timing may shift; mature cohorts and customer holds must be checked. |

Price-volume-mix method: volume effect at budget price/margin; price effect at actual volume and budget mix; mix/margin effect as the reconciled residual. Timing is reported separately. Reconcile to ledger before calling a variance real.

## 4. Tornado: which input moves the answer most
Live version: sheet `Tornado` in the monthly workbook (formulas, rank column and a check against `Dashboard!E9`). Picture: `docs/finance/tornado.png`.

| Rank | Input | Low to high | Net contribution, low / base / high (INR lakh) |
|---:|---|---|---|
| 1 | Effective win-back | 12.5% to 36% | 8.8 / 19.6 / 29.1 |
| 2 | Lost-RFQ rate | 3% to 7% | 11.0 / 19.6 / 28.2 |
| 3 (tie) | Monthly RFQs | 48 to 72 | 15.3 / 19.6 / 23.9 |
| 3 (tie) | Average order value | INR 16 to 24 lakh | 15.3 / 19.6 / 23.9 |
| 5 | Contribution margin | 10% to 14% | 16.0 / 19.6 / 23.2 |
| 6 | Annual run cost | INR 3 to 1.5 lakh | 18.6 / 19.6 / 20.1 |

Two cautions. The ranges are my judgement and are not the same size, so the order shows where I think the uncertainty is. For the same percentage change, every multiplied driver has the same effect, which is why the last four are close. Win-back and the lost-RFQ rate lead, and neither is observed. Validate the eligible-loss denominator and the incremental conversion before trusting the base case.

## 5. Visible workbook controls
The workbook has two visible check sheets. `Control Checks` has six base-case rows. `Audit Checks` shows the same headline numbers with a PASS or FAIL flag and a plain-English note on each. `Tornado` ends with its own check against the dashboard. The validation script `scripts/validate_monthly_workbook.py` reproduces adoption 25%, recovered contribution INR 21.6 lakh, net INR 19.6 lakh and 4.9-month operating payback. A formula count is not proof that every formula is right: recalculate in Excel or LibreOffice and look for errors (the shipped file was recalculated in LibreOffice with 0 errors).
