# MarginLadder feature prioritisation matrix

**Method:** RICE-style scoring for relative sequencing. All reach, impact, confidence and effort values below are illustrative planning judgements, not measured adoption or engineering estimates. Reach is a notional number of RFQs or workflow instances affected in a typical month; impact is scored 0.25–3; confidence is a percentage; effort is relative person-weeks.

`RICE = Reach × Impact × Confidence / Effort`

| Capability | Reach / month | Impact | Confidence | Effort (person-weeks) | RICE | Priority | Why |
|---|---:|---:|---:|---:|---:|---|---|
| RFQ register, owner and ageing | 60 | 2.5 | 90% | 3 | 45.0 | P0 | Creates process visibility and a baseline |
| Deterministic costing and rate snapshot | 300 parts | 3.0 | 85% | 6 | 127.5 | P0 | High-frequency and commercial-critical |
| Approval queue with role gates | 42 (assumed 70% of 60) | 2.0 | 80% | 3 | 22.4 | P0 | Reduces decision ambiguity and control risk |
| Operational KPI / audit events | 60 | 2.0 | 85% | 3 | 34.0 | P0 | Enables measurement and traceability |
| Reminder and deputy escalation | 42 | 1.5 | 75% | 4 | 11.8 | P1 | Useful after real approval latency is measured |
| Historical quote import / search | 25 (assumed repeat use) | 1.5 | 55% | 7 | 2.9 | P1 | Depends on data quality and deduplication |
| AI drawing / part-list extraction | 60 | 2.5 | 40% | 10 | 6.0 | P1 | Potentially high value but high validation and liability risk |
| ERP / CRM integration | 60 | 2.0 | 35% | 12 | 3.5 | P2 | Valuable only after source-of-truth and workflow fit are known |
| Customer portal | 20 (assumed) | 1.0 | 30% | 12 | 0.5 | P2 | Outside initial internal-workflow problem |

## Sequencing decision

1. Deliver P0 visibility, costing integrity, quote snapshots and approval controls first.
2. Instrument stage events and build a clean baseline before committing to reminders or advanced AI.
3. Build AI extraction only when an evaluated document set, source provenance and human-review policy exist.
4. Defer integrations until process ownership and authoritative master data are agreed.

## Sensitivity to the scoring method

RICE is a prioritisation aid, not a decision oracle. The costing and rate-snapshot capability has the highest score because it affects every part line and is tied to quote correctness. The RFQ register remains a P0 even if its score is lower because without it the organisation cannot measure ageing or establish a valid cycle-time baseline. Compliance / commercial controls can also be P0 regardless of an aggregate score.
