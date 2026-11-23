# Change control and stakeholder communication

## Change control
**Purpose:** prevent unapproved scope, date or cost changes. **Reader:** sponsor, PM, workstream owners.

A change request must contain:
1. Request ID, date, requester and reason.
2. Current baseline and exact proposed change.
3. Impact on scope, critical path, effort, cost, risk, security, data and benefits.
4. Options: accept, defer, reject or trade scope.
5. Recommendation and evidence.
6. Decision owner, decision date and updated version.

**Approval rules**
- Sponsor is Accountable for changes to scope, budget, gate criteria or target dates.
- PM logs and assesses every request; no verbal change is treated as approved.
- Security must approve changes to data access, retention or external integrations.
- Finance must review any change to economic assumptions or benefit calculation.
- Update Gantt, RACI, RAID, requirements traceability and release notes after approval.
- Emergency security or data issue: pause affected workflow immediately; notify sponsor and security; preserve audit records; restart only after written approval.

## Stakeholder plan
| Stakeholder | Interest / decision | Engagement | Frequency | Owner | Evidence |
|---|---|---|---|---|---|
| Sponsor | Scope, budget, gates, stop/scale | Decision review | At each gate | PM | Decision log |
| Sales | RFQ loss reasons, customer response | Workshop / sample review | Weekly in discovery | BA | Anonymised loss reason list |
| Estimators | Work steps, rework, costing | Task observation | Discovery + pilot | Ops lead | Task log with consent |
| Operations | Capacity, fulfilment, queue ownership | Process review | Weekly | Ops lead | Capacity and queue evidence |
| Finance | Contribution, cash, assumptions | Model review | Gate 2 and close | Finance | Signed-off assumptions only if real |
| IT / Security | Access, integration, audit | Design and readiness review | Gate 2 and Gate 3 | Product/IT | Control review |
| Business tester | Acceptance and usability | Independent UAT | Before Gate 3 | BA | Completed UAT log |

## Communication rhythm
- Weekly: one-page RAG status with progress, next two weeks, RAID changes and decisions needed.
- Gate reviews: evidence pack circulated at least two working days before decision.
- Daily during pilot: defects, adoption, queue measures, capacity guardrails and rollback status.
- Escalate critical data/security incident immediately; high-impact delivery risk within one working day.
- Never publish participant names, customer data or confidential pricing in the portfolio.
