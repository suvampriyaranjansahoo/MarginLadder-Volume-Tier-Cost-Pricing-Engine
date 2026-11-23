# User acceptance test scripts

Run these on a fresh database with the demo accounts. Passwords are in `application/data/demo_credentials.txt` after the first service-backed API request.
Each script lists steps, the expected result and where the same behaviour is tested in code. Fill in **Result** and **Date** when you run it. **Status: written, not yet executed.** No result is claimed.
Scripts UAT-01 to UAT-12 check the local app. The client acceptance tests that need Company A's own data (AT-01 parity on 20 parts, AT-12 adoption) cannot run here and stay open.

| ID | Role | Steps | Expected result | Linked | Code test | Result | Date |
|---|---|---|---|---|---|---|---|
| UAT-01 | none | Open the app. Try to read the register without signing in. | Sign-in box appears. No data shows. The API answers 401. | BR-18 | `test_health_is_public_and_everything_else_needs_a_session` | | |
| UAT-02 | any | Sign in with a wrong password five times, then the right one. | Same message each time. The sixth try is refused for 15 minutes. | BR-19 | `test_lockout_after_five_failures_blocks_even_the_right_password` | | |
| UAT-03 | estimator | Register an RFQ with a blank customer. Then with a past due date. Then a valid one. | First two are refused with a reason. The third gets a code and appears in the register. | UC-01, BR-01 to BR-03 | `test_required_fields_and_due_date_validation` | | |
| UAT-04 | estimator | Start costing on the new RFQ. Cost one part at 2,70,000 units. | Three prices show. The quote is `pending_approval` because it is above ₹25 lakh. | UC-02, BR-08, BR-11 | `test_large_quote_requires_sales_approval` | | |
| UAT-05 | estimator | Cost a part with net weight above gross weight. | Refused. The message names the problem. No quote is saved. | BR-10 | `test_costing_errors_come_back_as_400` | | |
| UAT-06 | estimator | Open the quote. Look for an Approve button. Try the approve call from the API docs page. | No button. The call returns 403. | BR-13, BR-18 | `test_role_comes_from_the_session_not_the_request_body` | | |
| UAT-07 | sales_head | Send the quote back with the reason "ok". Then with "Check material rate". | First refused (too short). Second works. The RFQ shows `sent_back`. | UC-04, BR-14 | `test_send_back_requires_reason_and_returns_to_costing` | | |
| UAT-08 | estimator | Re-cost the sent-back RFQ. | The new quote is version 2. Version 1 is still listed. | BR-15 | `test_quote_versions_increment_after_send_back` | | |
| UAT-09 | sales_head | Approve version 2. | Status `approved`. The audit trail shows who and when. | UC-03, BR-17 | `test_audit_trail_captures_approval_lifecycle` | | |
| UAT-10 | estimator | Mark the quote as sent. Open the print view. | RFQ shows `sent`. The print view shows three tiers and the notice that it is illustrative. | UC-05, BR-16 | `test_sales_head_can_approve_and_quote_can_be_sent` | | |
| UAT-11 | plant_head | Try to clear a routing review as an estimator, then as the plant head. | The estimator is refused. The plant head succeeds. | BR-05 | `test_only_plant_head_can_clear_routing_review` | | |
| UAT-12 | estimation_head | Import the template trace file. Then import a file where a send time is before the receipt time. | First shows median, 90th percentile and the decision text. Second is refused with the row number and nothing is stored. | UC-06, BR-21 | `test_trace_import_is_all_or_nothing` | | |

## What UAT cannot show
- Whether estimators prefer this to Excel. That needs real users.
- Whether the prices match Company A's Excel. That is AT-01 and needs the signed-off rates.
- Whether quotes get faster. That needs the Week 1 trace and a pilot.
