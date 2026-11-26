# Developer task run (scripted, synthetic data)

**DEVELOPER-RUN, NOT USER RESEARCH.** `python3 scripts/developer_task_run.py` runs three tasks against the application service layer with a temporary database and synthetic records, and writes this file. No person took part. It shows how the system behaves on good and bad input. It does not show that anyone finds the screens clear.

Run date: 2026-11-26. Reproduce it by running the script; dates inside the run are relative to the day it is run.

| Task | Step | Result |
|---|---|---|
| 1 Create and reassign | Create RFQ with owner and due date | OK: RFQ-2611-001 status new |
| 1 Create and reassign | Overdue count on dashboard | overdue_rfq_count = 1 |
| 1 Create and reassign | Reassign overdue RFQ, due date unchanged | OK: Ravi Nair |
| 1 Create and reassign | Move due date to another past date | REJECTED: Due date cannot be in the past |
| 2 Bad input | Empty customer | REJECTED: Customer is required and must be 120 characters or fewer |
| 2 Bad input | Past due date on create | REJECTED: Due date cannot be in the past |
| 2 Bad input | Sales head tries to create RFQ | REJECTED: Role 'sales_head' is not permitted for this action |
| 2 Bad input | Invalid status jump new to sent | REJECTED: Invalid status transition: new → sent |
| 2 Bad input | Quote while RFQ is still new | REJECTED: Cannot cost an RFQ while it is 'new' |
| 2 Bad input | Quote with zero volume | REJECTED: Selected volume must be one of 90000, 180000, 270000 |
| 3 Quote and approval | Create quote (270000 pieces) | OK: status pending_approval, approval required True |
| 3 Quote and approval | Estimator tries to approve | REJECTED: Role 'estimator' is not permitted for this action |
| 3 Quote and approval | Send back without a reason | REJECTED: A send-back reason of at least five characters is required |
| 3 Quote and approval | Send back with a reason | OK: sent_back |
| 3 Quote and approval | Audit events for this RFQ | rfq_updated, rfq_updated, rfq_created |

## Observations
- Every bad input was rejected with a plain message, and every role limit held.
- Task 1 is the regression found in 3.4.2: an overdue RFQ can be reassigned, but its due date cannot be moved to another past date.
- The audit filter by RFQ id returns RFQ events only. Quote decisions are stored under the quote id, so an RFQ history view would need to join them. This is a possible product improvement, not a defect in the stored data.

## Not shown by this run
Screen clarity, task time, user errors and preference. Those need real participants: see `docs/ba/independent_uat_and_signoff_protocol.md`.
