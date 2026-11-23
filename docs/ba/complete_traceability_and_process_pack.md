# Business Analyst — traceability and process pack

**Purpose:** let a reviewer trace a business rule to a requirement, test and screen quickly.  
**Reader:** BA interviewer, product owner, QA and operations.  
**Recruiter conclusion:** requirements are connected to workflow proof; unbuilt and untested items are visible.  
**30-second explanation:** “I turn the RFQ process into numbered rules and requirements, then connect each to acceptance tests and the screen. I separate automated tests from business UAT.”

## 1. Traceability
The detailed baseline is `docs/requirements_traceability_v3.md`. The table below adds the screen link and proof status.

| Rule / requirement | Test / proof | Screen or control | Status |
|---|---|---|---|
| BR-01 / FR-01: create RFQ with owner and due date | Application service/API tests | Register / Create RFQ | Built; automated tests |
| BR-02 / FR-02: find and page RFQs | Search and pagination tests | Register search / list | Built; automated tests |
| BR-03 / FR-03: valid status transitions | State transition tests | RFQ detail status control | Built; automated tests |
| BR-04 / FR-04: deterministic costing | Cost engine reference tests | Costing screen | Built; customer price parity open |
| BR-05 / FR-05: preserve quote version | Quote snapshot tests | Quote detail / history | Built; automated tests |
| BR-06 / FR-06: approval threshold | Role and threshold tests | Approval queue | Built; GST basis requires business confirmation |
| BR-07 / FR-07: send-back reason and recost | Send-back / version tests | Approval card / recost | Built; automated tests |
| BR-08 / FR-08: approved quote dispatch | Approval/send tests | Quote detail / Send | Built; automated tests |
| BR-09 / FR-09: audit lifecycle events | Audit event tests | Audit history | Built; automated tests |
| BR-10 / FR-10: printable quote | Authenticated print route test | Quote print view | Built; signed customer PDF not built |
| BR-11 / FR-11: named users and roles | Login, lockout and session tests | Login / user session | Built; MFA/password reset not built |
| BR-12 / FR-12: operational KPIs | KPI pairing and working-day tests | Dashboard cards | Built; synthetic data only |
| BR-13 / FR-13: trace import | Atomic import and summary tests | Trace import / summary | Built; real RFQ trace absent |
| BR-14 / FR-14: label evidence and simulation | Source-label tests | Dashboard notices | Built; no real result implied |
| NFR-01: migration safety | Upgrade and migration tests | Application start / migration | Built; local tests |
| NFR-02: secret handling | Hash/session tests | Login and session | Built; security review not independent |
| AT-01: 20-part price parity | No approved customer reference set | Costing screen | OPEN — requires permissioned reference data |
| AT-06: AI drawing extraction | No screen or implementation | None | NOT BUILT |
| AT-10: customer-group drawing access | No file store / permission UI | None | NOT BUILT |
| AT-12: pilot with six estimators and Sales Head | No live participants or pilot | Register / approval queue | OPEN — requires real people and UAT |

**Orphan rule:** any requirement without a test or screen is explicitly marked OPEN or NOT BUILT above. Do not describe an automated test as business acceptance.

## 2. AS-IS and TO-BE
Pain points below are hypotheses derived from the hypothetical case, not observed stakeholder findings.

### AS-IS
1. RFQ arrives; completeness and ownership may be unclear (P1 → FR-01).
2. Estimator receives work; assignment and queue age may not be visible (P2 → FR-02).
3. Costing uses manual inputs; rework and version control may be inconsistent (P3 → FR-04/05).
4. Approval waits for a decision; escalation may be unclear (P4 → FR-06/07).
5. Quote sent; outcome and loss reason may not be consistently captured (P5 → FR-08/14).
6. Management reviews elapsed time without a complete stage-level trace (P6 → FR-12/13).

### TO-BE
1. Capture RFQ owner, due date and completeness at intake (FR-01).
2. Show status, owner and age in a searchable register (FR-02/03).
3. Preserve versioned costing and assumptions (FR-04/05).
4. Route approvals with threshold, reason and audit history (FR-06/07/09).
5. Send only approved quote versions and preserve the record (FR-08/10).
6. Track KPI definitions and trace completeness with evidence labels (FR-12/13/14).

## 3. Ten edge cases
| ID | Edge case | Expected handling | Requirement |
|---|---|---|---|
| EC-01 | RFQ missing drawing or quantity | Save as incomplete; block costing until required fields exist | FR-01 |
| EC-02 | Duplicate RFQ reference | Reject duplicate or route to controlled merge; preserve audit | FR-01/09 |
| EC-03 | Negative or >100% rejection rate | Reject input with clear validation message | FR-04 |
| EC-04 | Rate master expires mid-quote | Use effective date; require new version if rate changes | FR-04/05 |
| EC-05 | Quote below contribution floor | Block send; require authorised exception and reason | FR-04/08 |
| EC-06 | Quote crosses approval threshold | Route to authorised approver; do not permit self-approval | FR-06 |
| EC-07 | Approver sends back without reason | Require reason before recost | FR-07 |
| EC-08 | Two users update same RFQ | Detect stale version; prevent silent overwrite | FR-05/09 |
| EC-09 | Customer holds response | Record hold start/end separately; exclude from internal queue KPI | FR-12/13 |
| EC-10 | Overlapping stage timestamps | Flag overlap; do not sum durations as sequential | FR-13 |

## 4. UAT run log template
Copy `data/templates/uat_execution_log_template.csv` before use. It is empty. A real independent tester must record actual result, defect ID and retest. No business UAT has been completed in this case.

## 5. Data dictionary and glossary
See `docs/ba/data_dictionary.md` and `docs/ba/glossary.md`. Plain English summary:
- **RFQ:** request for quotation.
- **Queue time:** time waiting for the next owner.
- **Cycle time:** elapsed time from defined start to defined finish.
- **Rework:** repeated work caused by a correction or missing information.
- **Traceability:** link from rule to requirement, test and screen.
- **UAT:** user acceptance testing; a business user checks the process against real work.
