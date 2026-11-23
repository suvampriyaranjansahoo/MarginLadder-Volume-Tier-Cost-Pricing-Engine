# Product discovery and usability execution pack

**Status:** protocol prepared; no interviews or moderated usability sessions are represented as completed. Synthetic events in `data/product_events_sample.csv` remain a method demonstration only.

## 1. Product question

Can an RFQ owner and estimator reliably understand the next action, owner, due date and approval state for an active RFQ, without weakening pricing controls or creating extra review work?

This is narrower and more testable than “build an AI costing platform.” The initial product bet is a **workflow visibility and control layer** around existing costing, not autonomous pricing.

## 2. Discovery hypotheses to challenge

| Hypothesis | What would support it | What would disconfirm it |
|---|---|---|
| H1: RFQs lose time at handoffs rather than only during costing | Timestamped handoff gaps are material and repeated | Costing itself is the dominant cycle component |
| H2: Owners lack reliable status visibility | Users check status manually or duplicate requests; source records disagree | Existing ERP/mail/board already provides trusted status |
| H3: Approval routing causes avoidable waiting | Wrong approver, re-routing or batching is observed | Approvals are fast and waiting occurs elsewhere |
| H4: A shared RFQ register is worth the workflow change | Users complete key tasks faster or with fewer errors in task tests | Users prefer existing tools or the register adds duplicate entry |
| H5: AI extraction is not needed for the first release | Manual structured intake is adequate for pilot volume | Document re-keying is shown to be a dominant, costly failure point |

## 3. Target user / JTBD framing

- **Primary workflow user:** RFQ owner or estimator who needs a trusted queue and a clear next action.
- **Control user:** approver who needs a concise exception summary and an auditable decision record.
- **Decision user:** operations / finance leader who needs cycle, capacity and economics evidence before authorising wider rollout.

These are target-role assumptions, not validated personas. Update them only after discovery.

## 4. Moderated task protocol

Run an exploratory formative round with five task sessions across the primary and control roles where feasible. Five participants can surface common interaction failures but cannot establish statistical significance or product-market fit.

**Tasks**

1. Sign in using the assigned role and locate an RFQ awaiting action.
2. Explain the RFQ's current status, owner, due date and next action.
3. Add or update a required intake field, then identify the audit evidence.
4. Submit an approval request or complete an approval if authorised.
5. Attempt an action outside the role's permission and explain what happened.
6. Locate the relevant quote snapshot and explain how the price can be reviewed.

**Capture**

- Task attempted and completion status.
- Time-on-task with start/stop rule.
- Error, misclick, wrong assumption or help required.
- Participant interpretation of labels/statuses.
- Critical control failure (yes/no).
- Severity, evidence ID and proposed product change.

Do not store participant names in the analysis export. Capture consent separately and avoid recordings unless required and explicitly agreed.

## 5. Pre-registered exploratory thresholds

These are proposed decision thresholds for a small formative round, not measured outcomes or universal product benchmarks:

- Core status/next-action task: at least 4 of 5 participants complete without moderator intervention.
- Permission boundary: zero successful unauthorised actions in all observed attempts.
- Critical misunderstanding: no participant interprets a draft or unapproved quote as approved for release.
- Evidence discoverability: at least 4 of 5 can locate the audit or quote snapshot needed for the task.
- Any critical control failure blocks the next release regardless of aggregate task success.

Report the numerator, denominator, task wording, build version and participant role mix. Avoid percentages without counts.

## 6. Event taxonomy

| Event | Required properties | Reason |
|---|---|---|
| `rfq_created` | `rfq_id`, `created_at`, `actor_role`, `source_channel` | Intake volume and origin |
| `rfq_completed` | `rfq_id`, `completed_at`, `completeness_state` | Intake quality |
| `rfq_assigned` | `rfq_id`, `assigned_at`, `assignee_role` | Queue ownership |
| `costing_started` | `rfq_id`, `started_at`, `part_count` | Work start |
| `costing_completed` | `rfq_id`, `completed_at`, `quote_version` | Estimation effort and revision |
| `approval_requested` | `rfq_id`, `requested_at`, `approval_tier` | Approval queue start |
| `approval_decided` | `rfq_id`, `decided_at`, `decision`, `approver_role` | Approval outcome |
| `quote_sent` | `rfq_id`, `sent_at`, `quote_version` | Cycle endpoint |
| `customer_hold_started/ended` | `rfq_id`, timestamps, reason code | Separate non-additive customer-hold overlay |

Do not collect free-text customer content or unnecessary personal identifiers in analytics. Use a stable pseudonymous RFQ key and a defined retention policy.

## 7. Metric definitions and guardrails

- **RFQ cycle:** working-time difference between accepted `rfq_created` and first `quote_sent`; report revisions separately.
- **Complete-case rate:** complete eligible RFQs divided by all eligible RFQs in the period; report missingness.
- **P50 / P75 cycle:** median and 75th percentile on completed eligible RFQs; state handling of censored/open cases.
- **Approval wait:** approval decision timestamp less request timestamp, adjusted to defined business calendar.
- **Task completion:** participants completing a stated task without moderator intervention divided by participants who attempted it.
- **Guardrails:** price-parity exceptions, approval-policy breaches, quote rework, missing event pairs and data corrections.

## 8. Decision rule

Keep the workflow MVP only if it solves an observed user problem without creating unacceptable duplication or control risk. Add AI document extraction only when manual intake cost is demonstrated, a labelled evaluation set exists, critical field precision/recall and correction burden are measured, and a human confirmation path is designed. AI must never set a price or approve a quote.

## 9. Blank execution template

Use `data/templates/usability_session_template.csv` and `data/templates/discovery_interview_log_template.csv`. No participant rows are pre-populated.
