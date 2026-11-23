# Business analysis execution pack — discovery, traceability and UAT

**Purpose:** turn the existing BA artefacts into a repeatable fieldwork and acceptance process. Blank records remain blank until completed by real participants.

## 1. Elicitation plan

| Stakeholder class | What to understand | Useful evidence | Bias / risk to control |
|---|---|---|---|
| Estimator | Work arrival, data availability, rate lookup, rework and concurrent workload | One recently completed RFQ reconstructed step-by-step | Do not assume estimation time is the dominant delay |
| Sales / RFQ owner | Intake completeness, customer clarifications, quote urgency and dispatch | RFQ intake record, missing-information reasons, sent timestamp | Avoid equating late customer inputs with internal process delay |
| Approver | Approval thresholds, escalation, exception paths and delegation | Approval record and decision timestamps | Do not assume all quotes need the same approval path |
| Plant / operations | Capacity, tooling constraints, feasible lead times and schedule contention | Capacity plan, machine availability, product family constraints | Revenue recovery is not value if the plant cannot fulfil the order |
| Finance / commercial | Contribution definition, order economics, discount controls and working capital | Cost sheets, historical price approvals and margin bridge | Clarify gross margin vs contribution vs EBITDA before modelling |
| Customer-facing / procurement | Quote completeness, revision frequency, response window and supplier selection | Anonymised quote feedback and revision history | No customer identifiers or confidential terms without permission |

## 2. Interview method

1. Ask the participant to walk through the **most recent specific RFQ**, not an idealised process.
2. Reconstruct events, actors, system-of-record and handoffs before discussing solutions.
3. Ask what caused waiting, rework, missing information, approval delay and customer hold.
4. Ask for counterexamples: when did the process work quickly, and why?
5. Separate observed facts, participant interpretation, analyst inference and unresolved questions.
6. Paraphrase notes unless the participant has explicitly permitted a quotation. Store the consent reference separately from notes.

**Do not ask:** “Would an AI tool solve this?” before the current problem and its cost are understood.

## 3. Evidence coding

Each finding should use these fields:

| Field | Meaning |
|---|---|
| Finding ID | Stable identifier, e.g. `DISC-001` |
| Participant role | Role category only; avoid identity details |
| Workflow stage | Intake, assignment, costing, approval, dispatch, customer response |
| Evidence type | Observed event / artefact / participant report / analyst inference |
| Finding | Short, neutral statement |
| Frequency | Count or stated frequency, with denominator and period if known |
| Impact | Time, rework, risk, margin or customer consequence; quantify only with support |
| Counterexample | Evidence that contradicts or narrows the finding |
| Confidence | High / medium / low, with reason |
| Requirement impact | Requirement IDs affected, or `none yet` |

## 4. Requirements traceability standard

Keep existing IDs in `docs/requirements_traceability_v3.md`. For new requirements, add: source/finding ID, rationale, priority, owner, acceptance criteria, process step, UI/API/data element, test ID, result and change-request ID. A requirement without a source is an assumption and must be labelled as such.

## 5. UAT execution protocol

The existing `UAT-01` to `UAT-12` scripts remain the test specification. Execute the following sequence against a frozen build:

1. Record app version, commit or archive hash, database reset state and test data set.
2. Use the appropriate role account; do not bypass server-side permissions.
3. Execute the preconditions and steps exactly as written.
4. Capture expected and actual results, timestamp, evidence ID and pass/fail/block status.
5. Log defects with severity, reproducibility, owner, target fix and retest result.
6. Do not mark a test passed because an API unit test covers a similar code path.
7. Obtain business sign-off only from a named accountable stakeholder who actually completed the review; retain consent and approval evidence appropriately.

### Defect severity

- **Critical:** unauthorised access, pricing corruption, material data loss or inability to perform the core process.
- **High:** a core RFQ or approval path cannot be completed, or an important control can be bypassed.
- **Medium:** material workflow friction with a safe workaround.
- **Low:** cosmetic or low-impact usability issue.

## 6. Blank execution log template

Use `data/templates/uat_execution_log_template.csv`. No test rows are marked as executed in this release. The UAT status remains **not yet executed by business participants**.

## 7. Acceptance gates before any pilot

- All high-priority requirements trace to a business need and one or more acceptance tests.
- No open critical/high defect in the happy path or access-control path.
- At least 20 representative part/volume cases achieve approved price parity within a pre-agreed tolerance; every deviation has an explanation and owner.
- Incomplete timestamps, customer holds, unsent RFQs and outliers are reported rather than silently excluded.
- Business acceptance, security/privacy review and pilot owner are confirmed before real data is used.

## 8. Open questions (do not resolve by assumption)

- What exactly counts as an RFQ loss in the 5% rate?
- Does the 12% margin represent gross margin, contribution after variable conversion cost, or another measure?
- Is the nine-day cycle measured from receipt to first quote, complete quote, or final revision?
- Which workflow stages use elapsed calendar time versus working hours?
- Which approval thresholds are mandatory, and who may delegate?
- What portion of delay-related lost orders can the plant actually produce?
