# Roadmap: Now, Next, Later

RICE (`prioritisation_matrix.md`, `rice_sensitivity.md`) ranks the costing screen first, because it scores impact on the 12.5 hours the brief states. I put the register and clock first anyway (D-01), because the brief says most of the 9 days is waiting and RICE has no input for waiting. That is a judgement. The Week 1 trace decides it: if costing is over 40% of the cycle, the RICE order wins and scope is cut to costing. Effort in relative person-weeks.

## Now (Weeks 1 to 3): prove the delay is where I think it is
| Item | Why now | Exit test |
|---|---|---|
| Week 1 trace on 10 recent RFQs, then the larger import | Replaces the simulated log. Settles the 40% rule. | Costing share and median known with a sample size |
| Lost-RFQ coding on the last 20 lost RFQs | Tests the 50% delay share behind the 25% win-back. | At least 20 coded, at least 25% lost to delay (Gate 3 condition A) |
| Plant capacity question to the plant head | Tests the displacement risk. | Spare capacity as a share of output, against the 46% break-even fit |
| Early Release: register, clock, one-screen approval (no file upload in this MVP) | Removes waiting, which is most of the 9 days. | Six estimators and the Sales head use it for all new RFQs |
| Rate owner signs off the rate master | Parity cannot be tested without it. | Signed rates on file |

## Next (Weeks 4 to 7): the part that prices
| Item | Why | Exit test |
|---|---|---|
| Costing screen and fixed engine on signed rates | Costing from 2.5 h to about 1 h a part. | AT-01: 20 parts within ₹0.01 a line |
| Approval card with deputy and reminder | Protects the 0.75-day approval budget. | Mean approval wait at or below 0.75 day in the pilot |
| PDF quote with rate and formula version | Stops retyping. | Numbers equal the screen |

## Later: only after Gate 3
| Item | Condition to start |
|---|---|
| Past-quote import and search | Data quality check passes; duplicates and rejects reconcile. |
| AI drawing and part-list extraction | An evaluated document set, source display and a human-accept rule exist. |
| ERP or CRM link | Source of truth is agreed. |
| Real identity, MFA, TLS, hosting | Before any real customer data. |

## Not planned
Customer portal, automatic approval, AI-set prices, multi-plant rates.

## Kill criteria
| Trigger | Number | Owner | When | Action |
|---|---|---|---|---|
| Costing share of cycle | Above 40% | Product owner | End of Week 1 | Cut scope to costing only |
| Coded lost RFQs due to delay | Below 25% of at least 20 | Sales Head | Before Gate 3 | Stop after Gate 3 |
| Spare plant capacity | Below the break-even fit for the base win-back | Plant Head | Before Gate 3 | Re-run the case with displacement |
| Win-back after six months | Below 10% | Managing Director | Month 6 | Do not fund Release 2 |
| Pricing exceptions in the pilot | Any rise | Estimation Head | Weekly | Stop and fix parity |
