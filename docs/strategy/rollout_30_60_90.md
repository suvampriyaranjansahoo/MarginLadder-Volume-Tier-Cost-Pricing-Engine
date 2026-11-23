# 30 / 60 / 90 days and decision rights

Assumes a start date, a signed agreement and a plant that shares 10 recent RFQs. Not a promise. [Judgement]

## First 30 days: learn
| Week | Do | Done when |
|---|---|---|
| 1 | Trace 10 RFQs with `python3 -m tracekit.analyze`. Three user calls. Plant capacity answer. Code the stated reason on the last 20 lost RFQs. | Costing share known. Capacity share known. |
| 2 | Ship the register and clock (Early Release). | Estimation Head uses it daily. |
| 3 | Add one-screen approval. Start the parity test on 20 parts. Gate 2 review on day 15. | Approval wait is measured. Second payment only if the register is in daily use. |
| 4 | Fix what Gate 2 found. | Register in daily use by every estimator. |

## Days 31 to 60: price
Gate 3 sits at day 25 and decides the full build on the Week-1 trace, lost-RFQ coding and the plant's capacity answer. Then the costing screen on the fixed engine, quote snapshots and print view. Parity test signed on 20 parts.

## Days 61 to 90: measure
The pilot compares the Early Release with the Week-1 baseline. It needs 6 weeks or more and about 90 RFQs, so it finishes after day 90 for a 60-a-month plant. Its rules in `docs/product/pilot_design.md` decide Release 2, not Gate 3. The month-6 win-back check follows.

## Decision rights
| Decision | Owner | Needs |
|---|---|---|
| Cut scope to costing only | Product owner | Week 1 costing share above 40% |
| Approve a quote above ₹25 lakh | Sales Head or Deputy | Reason on send-back |
| Clear a routing review | Plant Head | Nothing else |
| Change a rate or formula | Estimation Head with Sales Head | Version bump and parity re-test |
| Release the second and third payments | Managing Director | Gate 2, Gate 3 evidence |
| Stop the project | Managing Director | Any kill trigger below |

## Kill criteria
Same table as `docs/product/roadmap.md`. It is not repeated here, so it cannot drift.

## Five-slide deck outline (for a client or an interview)
1. The cost of waiting: 36 lost RFQs a year, ₹86.4 lakh margin pool, 9 days against 4.
2. Where the days go: 1.56 costing, 7.44 not. Queue explains under 1. The trace will say the rest.
3. The plan: register and clock first, costing second, three gates.
4. The money: ₹21.6 lakh base, ₹10.8 lakh conservative, break-even 11.6%, cash payback 23.6 months.
5. What could stop it: win-back, plant capacity, estimator loss. Each has a number and an owner.
