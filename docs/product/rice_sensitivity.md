# RICE sensitivity: which ranks can I trust?

Source: `docs/product/prioritisation_matrix.md` (9 capabilities). 5,000 random draws, seed 7.
Each draw changes reach and impact by up to 25%, confidence by up to 20 points and effort by -30% to +50%. [Judgement]

| Base rank | Capability | Priority | 10th to 90th percentile rank | Same rank | In top 3 |
|---|---|---|---|---|---|
| 1 | Deterministic costing and rate snapshot | P0 | 1 to 1 | 98.8% | 100.0% |
| 2 | RFQ register, owner and ageing | P0 | 2 to 3 | 68.4% | 95.4% |
| 3 | Operational KPI / audit events | P0 | 2 to 4 | 54.5% | 81.5% |
| 4 | Approval queue with role gates | P0 | 3 to 4 | 68.5% | 22.3% |
| 5 | Reminder and deputy escalation | P1 | 5 to 5 | 80.3% | 0.7% |
| 6 | AI drawing / part-list extraction | P1 | 6 to 7 | 65.3% | 0.0% |
| 7 | ERP / CRM integration | P2 | 6 to 8 | 43.1% | 0.0% |
| 8 | Historical quote import / search | P1 | 7 to 8 | 55.1% | 0.0% |
| 9 | Customer portal | P2 | 9 to 9 | 99.8% | 0.0% |

## Reading

- **No capability moves more than 2 places** between the 10th and 90th percentile. The order is robust to these input errors.
- **Top 3 in the base case:** Deterministic costing and rate snapshot, RFQ register, owner and ageing, Operational KPI / audit events. They stay in the top 3 in 81.5% to 100.0% of draws.
- **Ranks that hold in fewer than 60% of draws:** Operational KPI / audit events, ERP / CRM integration, Historical quote import / search. Do not argue their exact order before the Week 1 trace.
- The register is P0 whatever its score, because without it there is no baseline. That is a judgement, not a score.
- What this does not test: a wrong idea of the problem. All draws share one scoring frame, so a shared error in it is invisible here.
