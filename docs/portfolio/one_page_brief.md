# MarginLadder: one-page brief

**Case.** A hypothetical Pune auto-components manufacturer receives 60 RFQs a month (5 parts each). Quotes take 9 working
days; the target is 4. Should it fund an ₹8 lakh build? There are no production users and no real customer interviews;
all figures are modelled.

**Recommendation.** Do not approve the full costing build yet. Measure first, pilot a reversible queue-visibility and
approval workflow, and automate costing only if measured data shows costing is the bottleneck.

## The arithmetic in four lines
1. 60 × 12 = 720 RFQs a year; 5% lost = 36.
2. 36 × ₹20 lakh × 12% margin = **₹86.4 lakh** theoretical lost-margin pool (a ceiling).
3. At an assumed 25% win-back: **₹21.6 lakh** a year (₹10.8 lakh at 12.5%). Win-back is an assumption, not observed.
4. After ₹2 lakh run cost, break-even win-back is **11.6%** (9.3% on the fee alone).

## Why not "approve, it pays back in 4.9 months"
| View | Result | What it leaves out |
|---|---:|---|
| Operating payback | 4.9 months | Tax and working capital |
| Cash payback | 23.6 months | Includes both |
| 3-year IRR | 75.8% with working-capital release, 43.0% without | Release is itself an assumption |
| Deepest cash need | ₹14.8 lakh | More than the ₹8 lakh fee |

Released estimator capacity (5,400 gross / 4,680 net hours) is not cash unless a cash-releasing action is decided.

## What would change the recommendation
- Observed win-back below about 11.6%: the build does not cover its run cost.
- Stage timestamps showing costing is a small share of the 9 days: automate something else.
- Rework or price-parity data showing costing errors drive lost RFQs: approve costing automation earlier.
- A real vendor quote far from ₹8 lakh: re-run the break-even.

## What exists
A reconciled Excel model (64 of 64 cells match its Python twin), a Decimal costing engine, a FastAPI + SQLite workflow
prototype with role-gated approvals, tests, CI, and a claim-by-claim evidence ledger.

## What does not
Real users, interviews, UAT sign-off, a deployment, or any measured improvement.
