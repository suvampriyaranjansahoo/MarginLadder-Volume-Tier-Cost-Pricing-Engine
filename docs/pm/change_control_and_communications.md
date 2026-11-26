# Change control and stakeholder communication

**TEMPLATE process for a hypothetical plan. No change request has been raised.** Two worked examples (not real requests) are in `docs/ba/change_requests.md`.

## Change control
**Purpose:** stop scope, date or cost changing without a decision. **Reader:** Managing Director, Product owner, task owners.

A change request has: ID, date, requester and reason; current baseline and exact change; effect on scope, critical path (`docs/pm/schedule_and_critical_path.md`), effort (`docs/pm/resourcing_effort.md`), risk, data and the payments; options (accept, defer, reject, trade scope); recommendation; decision owner and date.

| Change size | Who decides | Rule |
|---|---|---|
| Within a task, no date or cost effect | Task owner (A in `raci_tasks.md`) | Log it |
| Moves a task with slack, stays under the slack | Product owner | Log it and tell the Managing Director in the weekly status |
| Moves a critical-path task, a gate day or a payment | Managing Director | Written decision before work starts |
| Changes the INR 25 lakh rule, rates or the formula | Estimation Head with Sales Head | Version bump and parity re-test (`docs/strategy/rollout_30_60_90.md`) |
| Touches access, data retention or integration | Client IT, then Managing Director | Written approval |

After any approved change, update the plan, RACI, RAID log, traceability and release notes. In an emergency data or security issue, pause the affected workflow, tell the Managing Director and Client IT, keep the audit log, and restart only with written approval.

## Stakeholders and communication
| Stakeholder | Cares about | Channel | How often | Owner | What they receive |
|---|---|---|---|---|---|
| Managing Director | Gates, payments, stop | Gate review | Days 15, 25, 35 and 55 | PO | Evidence pack two working days before |
| Sales Head | Loss reasons, margin, approvals | Short workshop | Weekly to day 25 | BA | Coded lost-RFQ list; approval-card demo |
| Estimation Head and estimators | Not being slower, not blamed | Floor walk and register demo | Twice a week in T09 and T16 | PO | What changed; how to report a problem |
| Plant Head | Capacity, routing | Call | Once before Gate 3, then weekly | PO | Capacity question and answer |
| Rate owner | Dated, signed rates | Email and 30-minute call | Weekly until signed | DL | Rate gaps list |
| Client IT | Access, NDA, audit | Review meeting | Before day 10 and day 25 | DL | Access model and audit log sample |

## Rhythm
- Weekly: one-page RAG status (format in `docs/pm/status_reports_templates.md`) with progress, next two weeks, RAID changes and decisions needed.
- Gate reviews: pack circulated two working days before.
- During the pilot: weekly measures, defects, guardrails and rollback status.
- Escalation: a data or security incident immediately; a risk with score 6 or more within one working day.
- Never put participant names, customer data or confidential prices in this repository.
