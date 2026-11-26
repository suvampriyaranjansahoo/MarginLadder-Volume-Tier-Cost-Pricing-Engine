# Simulated workflow test: defect found and fixed (3.4.3)

**Evidence boundary:** this is a developer-run, simulated workflow test on synthetic data. It is not independent UAT, customer validation or stakeholder sign-off.

## Defect 1: past due date accepted on edit
An existing RFQ could be edited to a due date in the past, although creation already rejected past dates.
Fix: the same `due_date >= today` rule now runs in `update_rfq` (server side, so API callers cannot bypass it). Tests: `test_assignment_update_rejects_past_due_date` and `test_update_rfq_rejects_past_due_date` (API).

## Defect 2: the first fix blocked reassigning overdue RFQs
The assignment editor sends owner and due date together. With the first fix, changing only the owner of an RFQ that was already overdue failed with "Due date cannot be in the past". Overdue RFQs are the ones that most need a new owner.
Fix: a past date is accepted only when it equals the date already stored. Any change to another past date is still rejected. Test: `test_overdue_rfq_can_be_reassigned_with_its_unchanged_due_date`.

## Lesson
A validation rule added to one path must be tested against the workflow that already uses that path, not only against the bad input.

## Still open
Independent business UAT and stakeholder sign-off have not happened. See `docs/ba/independent_uat_and_signoff_protocol.md` (status: NOT EXECUTED) and `docs/ba/stakeholder_signoff_template.md` (blank).
