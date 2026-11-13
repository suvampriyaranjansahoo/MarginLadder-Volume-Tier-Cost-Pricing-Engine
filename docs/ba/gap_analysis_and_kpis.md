# Gap analysis and KPIs

## Gap analysis
| Area | Today | Target | Gap | How it closes |
|---|---|---|---|---|
| RFQ-to-quote time | 9 working days | 4 | 5 days | Register and clock, routing queue, one-screen approval, faster costing |
| Costing time | 12.5 h per RFQ (2.5 h a part) | 5 h (1 h a part) | 7.5 h, 0.94 day | One screen, AI-read values accepted by a person, fixed formulas |
| Visibility | No register, no age | Every RFQ has owner, due day, age | Not tracked | Early Release at Gate 2 |
| Rate control | Copied by hand | Effective-dated master, snapshot per quote | Errors and rework | Rate master loaded from the ERP export |
| Approval | Waits for the Sales head | Mean wait inside 0.75 day | Unknown | 70% trigger, one card, deputy, 4 h reminder |
| Lost RFQs | 5% | Lower | 36 a year | Faster, consistent quotes |

## Why 70%
If the trigger sends 70% of quotes to the Sales head and each waits one working day on average, the mean approval wait is 0.70 × 1 = 0.70 day. That sits inside the 0.75-day approval budget. At 80% it is 0.80 and breaks the budget. The Week 2 test on 1,400 past quotes checks the real share.

## KPI definitions
| KPI | Definition | Baseline | Target | Measured by |
|---|---|---|---|---|
| Cycle time | Working days from RFQ received to quote sent, median and 90th percentile | 9 days (Brief) | 4 | Register timestamps |
| Hands-on costing | Hours from costing start to costing done, per part | 2.5 h (Brief) | 1 h | Costing screen clock |
| On-time rate | Share of RFQs quoted within 4 days | Not measured | 80% by day 30 after go-live | Register |
| Approval wait | Mean working days from "ready" to "approved" | Not measured | 0.75 or less | Approval log |
| Parity | Lines within ₹0.01 of the client's Excel on 20 parts | n/a | 100% | AT-01 |
| Lost RFQ rate | RFQs lost / RFQs received, trailing 6 months | 5% (Brief) | Lower; see model | Sales records |
| Adoption | RFQs costed in the tool / all RFQs | 0% | 100% after the parallel run | Register |

## Baseline method (Week 1)
1. Pick 10 recent RFQs. Trace each from email to quote sent with timestamps from email, Excel and the approval message.
2. Split each trace into intake wait, costing, routing wait, approval wait, and send.
3. Replace `data/simulated_rfq_log.csv` with the real trace and re-draw the chart.
4. If costing is over 40% of the cycle, cut scope to the costing screen and engine.

## Simulated log
`data/simulated_rfq_log.csv` has 60 simulated RFQs. Stage means (1.5, 1.56, 1.9, 2.4 and 1.64 days) are assumptions (A5). Only the 1.56 days of costing is derived from the brief. It is a placeholder for the Week 1 trace, not a finding. Generator: `data/simulate_rfq_log.py`.
