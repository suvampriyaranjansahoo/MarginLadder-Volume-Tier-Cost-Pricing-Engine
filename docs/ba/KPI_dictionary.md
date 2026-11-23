# MarginLadder KPI dictionary and instrumentation plan

**Purpose:** make every KPI reproducible and prevent a synthetic chart or a financial assumption from being mistaken for an observed business result.

## 1. KPI definitions

| KPI | Formula | Grain / window | Source events | Baseline / target status |
|---|---|---|---|---|
| RFQ-to-quote cycle time | `quote_sent_at - rfq_received_at`, in working hours / 8; report median and P90 | RFQ; rolling 30 days | `rfq_created`, `quote_sent` | 9 working days from brief; 4-day target from brief; actual timestamps not yet available |
| Costing touch time | Sum of active estimator timer intervals per RFQ part | Part and RFQ; weekly | `costing_started`, `costing_paused`, `costing_resumed`, `costing_completed` | 2.5 h/part from brief; 1 h/part target |
| Queue / wait time | Stage exit time minus stage entry time less recorded active touch intervals | RFQ-stage; weekly | `status_changed` with from/to | Not measured; do not infer from total cycle time alone |
| On-time quote rate | RFQs sent within 4 working days / RFQs with a sent or closed outcome | RFQ cohort; monthly | `rfq_created`, `quote_sent`, `rfq_closed` | Target 80% after the agreed stabilisation period; baseline unknown |
| Approval wait | `approved_at - approval_requested_at`, in working days; report mean, median and P90 | Quote version; monthly | `approval_requested`, `quote_approved` | Target ≤0.75 working days; baseline unknown |
| First-pass quote rate | Quote versions approved without send-back / quote versions submitted for approval | Quote version; monthly | `approval_requested`, `quote_sent_back`, `quote_approved` | Baseline unknown; establish before target-setting |
| Quote rework rate | RFQs with at least one send-back or recost / RFQs costed | RFQ; monthly | `quote_sent_back`, `quote_costed` | Baseline unknown |
| Lost-RFQ rate | RFQs explicitly marked lost / RFQs with a final outcome | RFQ; rolling 6 months | `rfq_lost`, `rfq_won`, `quote_sent` | 5% from brief; definition needs confirmation |
| Win-back rate | Eligible lost RFQs later won after a faster quote / eligible lost RFQs exposed to the intervention | Lost RFQ cohort; quarterly | CRM outcome + reason code + intervention exposure | 25% is an assumption split into 50% delay-related × 50% conversion; not validated |
| Adoption | RFQs costed in MarginLadder / all eligible RFQs received | RFQ; weekly | `quote_costed`, intake register | Target 100% after parallel run; no pilot measurement yet |
| Rate parity | Cost lines matching approved reference Excel within ₹0.01 / cost lines tested | Part / rate version | Signed parity workbook + quote snapshot | 100% on 20 agreed parts is a release gate |
| Approval threshold compliance | Quotes above ₹25 lakh with recorded Sales Head / Deputy approval before send / all quotes above threshold sent | Quote version; monthly | `quote_costed`, `quote_approved`, `quote_sent` | Target 100%; threshold comes from brief |

## 2. Event taxonomy

| Event | Required properties | Trigger |
|---|---|---|
| `rfq_created` | rfq_id, rfq_code, customer_id, part_count, received_at, owner_id, due_at, source_channel | RFQ registered |
| `rfq_owner_changed` | rfq_id, old_owner, new_owner, actor_id, reason | Owner changes |
| `status_changed` | entity_id, entity_type, from_status, to_status, actor_role, event_at | RFQ / quote stage transition |
| `costing_started` | rfq_id, part_id, estimator_id, started_at | Estimator begins work |
| `costing_completed` | rfq_id, part_id, estimator_id, completed_at, active_minutes, formula_version | Costing completed |
| `input_reviewed` | rfq_id, part_id, field_name, source_ref, confidence_band, accepted_value, reviewer_id | Extracted or manually entered technical value accepted |
| `quote_costed` | quote_id, rfq_id, version, quote_date, selected_volume, annual_value, rate_versions, formula_version | Cost snapshot created |
| `approval_requested` | quote_id, requested_role, annual_value, requested_at | Quote enters approval queue |
| `quote_approved` / `quote_sent_back` | quote_id, actor_id, actor_role, decided_at, reason | Approval decision |
| `quote_sent` | quote_id, sent_at, channel, recipient_group | Quote released to customer |
| `rfq_outcome_recorded` | rfq_id, won_lost_no_bid, reason_code, outcome_at, order_value | Commercial outcome captured |

The v2 SQLite audit log currently records a subset of these events: RFQ create/update, quote cost, approve, send-back and send. Timers, source-level extraction provenance, customer outcomes and scheduled reminders are future work, not current features.

## 3. Data quality rules

1. Use one immutable `rfq_id` and one immutable `quote_id` per version.
2. Store event timestamps in UTC; convert to the plant's agreed working calendar for duration metrics.
3. Store local plant calendar, working hours, holidays and shutdown windows as versioned configuration.
4. Do not treat blank timestamps as zero duration.
5. Distinguish customer hold, internal queue, touch time and rework; never combine them into an unexplained residual.
6. Keep both raw and normalised customer / part identifiers to support deduplication.
7. Preserve quote input and rate snapshots after a master-rate change.
8. Record a reason code for lost, no-bid, send-back and customer-hold events.
9. Mark seeded / simulated rows explicitly; exclude them from all production KPI denominators.
10. Report denominator and cohort size alongside every percentage.

## 4. Baseline plan

- Trace 10 recent RFQs as a discovery sample, then extend to 30–60 RFQs if timestamps are retrievable.
- Reconcile received time to the original email, costing touch time to estimator activity, routing wait to plant review, approval wait to approval messages and sent time to the outbound quotation.
- Have an estimation head validate stage definitions and a sales representative validate won/lost reasons.
- Publish median, P90, sample size, exclusions and missing-data rate; do not rely on a mean alone.

## 5. Dashboard interpretation

The current UI dashboard's live cards show records in the local demo database. Its baseline diagnostic reads `data/simulated_rfq_log.csv`, which contains 60 synthetic examples with assumed stage means. That diagnostic is deliberately marked simulated and must never be presented as observed plant performance.
