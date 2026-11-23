# MarginLadder PRD v3

Status: portfolio case study with a local MVP. No client, no users, no pilot. Tags: [Brief] [Derived] [Assumption] [Judgement] [Simulated].
Supersedes `PRD_v2.md` for scope and metrics. v2 stays in the repo unchanged.

## 1. Problem
60 RFQs a month, 5 parts each [Brief]. Quotes take 9 working days against a 4-day target [Brief]. Costing is 12.5 hours, or 1.56 working days at 8 h a day [Derived]. The trace measures elapsed working days, the same unit when one estimator works on one RFQ at a time (BR-23). The other 7.44 days are not costing [Derived]. 5% of RFQs are lost [Brief].

## 2. Bet [Judgement]
Most of the 7.44 days is waiting. The estimator queue explains under 1 day of it (`docs/finance/capacity_and_queue.md`). The rest is approval, routing, intake and customer holds. So the first release makes those waits visible and short. A faster costing screen comes second.

## 3. Jobs to be done
| Who | When | They want | So that |
|---|---|---|---|
| Estimator | An RFQ lands | One place that shows what is mine and what is late | I cost it without chasing |
| Estimation Head | Work piles up | Age and owner of every RFQ | I move work before it is late |
| Sales Head or Deputy | A quote is above ₹25 lakh | One screen with price, margin and reason | I decide in one sitting |
| Plant Head | A new routing arrives | Only the parts that need me | I protect manufacturability |
| Managing Director | The ₹8 lakh is on the table | Timestamps and a fixed decision rule | I fund, cut or stop |

These personas come from the brief. No interview has been done. [Assumption]

## 4. Metric tree
North star: median working days from RFQ received to quote sent. Today 9 [Brief]. Target 4 [Brief].
- Input 1: wait before costing starts. Today about 0.57 day [Derived, queue model].
- Input 2: costing days. 1.56 today, 0.63 at 1 h a part [Derived].
- Input 3: approval wait. Budget 0.75 day [Judgement].
- Input 4: routing and intake wait. Unknown until the Week 1 trace.
- Guardrail: pricing exceptions must not rise. Quote parity with the Excel on 20 parts.
- Business outcome: coded lost RFQs won back. Base 25% [Assumption], break-even 11.6% [Derived].
Definitions: `docs/ba/KPI_dictionary.md`. Live KPIs in the app come from audit events.

## 5. Scope
| Release | Contents | Gate |
|---|---|---|
| Week 1 | Trace of 10 recent RFQs; three user calls; plant capacity answer | Week-1 check: costing share and capacity |
| Early Release (Weeks 2 to 3) | Register, clock, one-screen approval, sign-in, audit. No file upload in this MVP | Gate 2: second payment |
| Gate 3 (day 25) | Decides the full build on the trace, lost-RFQ coding (condition A) and plant capacity (condition B) | Costing 40% or less, A and B met |
| Release 1 (Weeks 4 to 7) | Costing screen on the fixed engine, quote snapshots, print. Parity on 20 parts must pass before the pilot | Parity signed |
| Pilot (from day 30, 6 weeks or more) | Measure Early Release against the baseline | Rules in `pilot_design.md` decide Release 2 |
| Later | AI reading of drawings (suggest only), ERP link | Only after Gate 3 |

## 6. Non-goals
Customer portal. Automatic approval. AI-set prices. Multi-plant rates. Scope beyond RFQ-to-quote. Replacing the client's Excel before a signed 20-part parity test.

## 7. Requirements
Functional requirements FR-01 to FR-14 and acceptance tests are in `docs/requirements_traceability_v3.md`. Business rules BR-01 to BR-26 are in `docs/ba/business_rules.md`. Use cases UC-01 to UC-07 and UAT-01 to UAT-12 are in `docs/ba/`.

## 8. Rollout and fallback
Pilot on 60 or more RFQs with a control period (`docs/product/pilot_design.md`). The old Excel stays live in parallel until parity holds. Any rise in pricing exceptions stops the rollout. Rollback is switching the team back to Excel; the register data is kept.

## 9. Risks
| Risk | Number | Mitigation |
|---|---|---|
| Win-back is a guess | Breaks even at 11.6% | Code lost RFQs in Week 1 |
| The plant is full | Needs 46% of recovered margin makeable | Plant Head answer before Gate 3 |
| Estimator loss | 5 of 6 estimators gives 94% load and 4.2 days wait | Cross-train; flag in the register |
| Approval becomes the bottleneck | 0.75-day budget | Threshold at 70% of quotes; deputy cover |
| The team does not use it | Unknown | Daily use by the Estimation Head is the Gate 2 test |

## 10. Open questions for the client
1. Is the ₹25 lakh approval limit before or after GST?
2. What share of plant output could be added without overtime or new machines?
3. What does the lost-RFQ log record as the reason?


## v3.1 analytics extension

The product event schema and metric definitions are demonstrated in `analytics/product_metrics.py` and `docs/product/simulated_product_analytics.md`. The event sample is synthetic. It defines RFQ lifecycle conversion, median calendar-hour time to quote, weekly active operators and week-based retention cohorts; it is not evidence of real adoption or product outcomes. Pilot instrumentation and privacy/access controls must be agreed before collecting real events.
