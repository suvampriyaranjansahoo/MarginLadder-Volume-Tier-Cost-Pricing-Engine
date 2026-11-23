# Optional field-validation protocol for a future live pilot

**Portfolio build status: complete.** This protocol applies only if the hypothetical case is later adapted for a real company. It is deliberately not marked complete because interviews, access to operating data and business sign-off must come from real participants. None of these activities is represented as having occurred, and none is a repository-delivery blocker.

## Discovery protocol

- Recruit 6–8 role-relevant practitioners across estimator, sales/RFQ owner, approver/plant or finance decision-maker, and customer-facing/procurement perspectives where feasible.
- Obtain consent for note-taking and any recording; record no unnecessary personal identifiers.
- Ask for the most recent concrete RFQ example; reconstruct timestamps and handoffs before asking what software should change.
- Seek disconfirming examples: quick RFQs, customer-hold cases, incomplete input cases, price revisions and capacity-constrained wins.
- Code findings by evidence strength and update assumptions only when the observations support it.

## Operational-data protocol

- Obtain written permission for a de-identified RFQ sample.
- Capture received, completeness, assigned, costing started, costing completed, approval requested, approval completed, sent and customer-response events.
- Record timezone, business calendar, exception reasons, missing values and customer-hold intervals.
- Compare median and P75 end-to-end cycle, stage time, complete-case share and censoring; do not silently drop incomplete RFQs.

## Business-analysis and UAT protocol

- Execute UAT-01 to UAT-12 against a frozen build ID.
- Record tester role, expected result, actual result, evidence ID, defect severity, owner, retest and disposition.
- Obtain business sign-off only from an accountable real participant.

## Product usability protocol

- Run at least five task-based sessions as an exploratory formative round, not a statistically representative study.
- Measure completion, error, time-on-task and qualitative friction; report denominator and task conditions.
- Change the prototype based on observed friction; re-test the changed path.

## Finance and implementation protocol

- Validate contribution-margin definition, order AOV, lost-RFQ denominator and whether losses are delay-attributable.
- Confirm incremental capacity, plant availability, working-capital terms, run cost and implementation cost.
- Reconcile the model to a permissioned ledger or quote/order dataset; keep modelled values separate from actuals.
- Refresh industry research and peer data before publication.
