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

## 4. One-factor sensitivity
Approximate annual net operating contribution; one input changes while others are held constant.

| Input | Downside | Base | Upside | Approximate net contribution |
|---|---:|---:|---:|---:|
| Effective win-back | 12.5% | 25% | 40% | ₹8.8L / ₹19.6L / ₹32.6L |
| Contribution margin | 10% | 12% | 14% | ₹16.0L / ₹19.6L / ₹23.2L |
| AOV | ₹16L | ₹20L | ₹24L | ₹15.28L / ₹19.60L / ₹23.92L |
| Annual run cost | ₹3L | ₹2L | ₹1.5L | ₹18.6L / ₹19.6L / ₹20.1L |
| Lost-RFQ rate | 3% | 5% | 7% | ₹10.96L / ₹19.6L / ₹28.24L |

**Largest drivers:** effective win-back and lost-RFQ rate. They are also not observed. Validate the eligible loss denominator and incremental conversion before trusting the base case.

### AOV sensitivity calculation (corrected)

Formula held constant: `9 recovered RFQs × AOV × 12% contribution margin − ₹2.0L annual run cost`.

| AOV | Gross recovered contribution | Less run cost | Net operating contribution |
|---:|---:|---:|---:|
| ₹16L | 9 × ₹16L × 12% = ₹17.28L | ₹2.00L | **₹15.28L** |
| ₹20L | 9 × ₹20L × 12% = ₹21.60L | ₹2.00L | **₹19.60L** |
| ₹24L | 9 × ₹24L × 12% = ₹25.92L | ₹2.00L | **₹23.92L** |

The prior ₹12.4L / ₹26.8L endpoints were arithmetic errors and are superseded. This sensitivity changes AOV only; recovered RFQs, margin and run cost remain fixed. These are model outputs, not realised benefits.

## 5. Visible workbook controls
The workbook contains both `Control Checks` and a dedicated `Audit Checks` sheet. The current workbook contains 439 formulas; the monthly validator reproduces adoption 25%, recovered contribution ₹21.6L, net ₹19.6L and 4.9-month operating payback. The six visible `Audit Checks` rows are cached as PASS in the delivered workbook. A formula count is not proof every formula is semantically correct; recalculate in Excel/LibreOffice after any workbook edit and inspect formula errors.
