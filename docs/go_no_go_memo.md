# Go / no-go memo: RFQ-to-quote costing app

**Recommendation: go, in two steps.** Ship the register and clock at Gate 2 (day 15). Decide on the full build only if the Week 1 trace confirms that waiting, not costing, is most of the 9 days.

## The numbers
- Today: 9 working days from RFQ to quote. Target: 4. Costing is 12.5 h (5 parts × 2.5 h), or 1.56 days. About 83% of the cycle is not hands-on costing [Brief, Derived].
- Cash case: 36 lost RFQs a year × ₹2.4 lakh margin × 25% win-back = ₹21.6 lakh a year (conservative, 12.5%: ₹10.8 lakh) [Assumption: the win-back rate].
- Cost: ₹8 lakh fee plus 18% GST. Payback is 4.4 months at base and 8.9 months conservative, or 4.9 and 10.9 months after ₹2 lakh a year of running cost.
- Break-even: a 9.3% win-back before running cost, 11.6% after it. A 5% win-back loses money.
- Capacity: 5,400 estimator hours a year (₹24.3 lakh at ₹450/h) are freed. This is upside. It counts only if the team quotes more.

## Why not just fix the Excel
It cuts some of the 1.56 days of costing, but it does not add an owner, a clock or an approval route. Those are where the other 7.44 days go.

## What would change the answer
| If this is true | Then |
|---|---|
| Week 1 trace shows costing is over 40% of the 9 days | Cut scope to the costing screen and engine |
| Win-back is under 10% in the first six months | Stop after Gate 3; do not fund Release 2 |
| Rate owner cannot sign off rates by Gate 2 | Hold M2; the engine cannot reach parity |
| Estimators do not use the register in the first week | Fix the process first, then the tool |

## Cash
We fund delivery before cash arrives. At net-10 terms, the peak funded gap is about ₹3.5 lakh (44% of the fee) at the end of Week 6. At 3-day terms it is about ₹2.3 lakh. See `model/MarginLadder_finance_model.xlsx`, Cash sheet.

## What is not proven
No Company A data. The win-back rate, the running cost and the stage split of the 9 days are my assumptions. The Week 1 trace replaces the split with real timestamps.
