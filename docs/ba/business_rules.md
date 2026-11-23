# Business rules catalogue

One row per rule. Each rule says where it comes from, where the app enforces it and which test proves it.
Source tags: **Brief** = given in the case. **Derived** = worked out from the brief. **Assumption** or **Judgement** = mine, to be confirmed with Company A.

| ID | Rule | Source | Enforced in | Test |
|---|---|---|---|---|
| BR-01 | Every RFQ has a customer, a part description, an owner and a due date. | Judgement (PRD FR-01) | `create_rfq` | `test_required_fields_and_due_date_validation` |
| BR-02 | A due date cannot be in the past when an RFQ is registered. | Judgement | `create_rfq` | `test_required_fields_and_due_date_validation` |
| BR-03 | RFQ codes are unique and never reused, even if a record is removed. | Judgement | `create_rfq` (`BEGIN IMMEDIATE`, highest code plus one) | `test_codes_never_collide_even_after_a_gap` |
| BR-04 | An RFQ moves only along the allowed status paths. | Judgement (swimlane to-be) | `ALLOWED_TRANSITIONS`, `update_rfq` | `test_invalid_status_transition_is_blocked` |
| BR-05 | Only the Plant Head can clear a routing review. | Brief (plant head reviews new routings) | `update_rfq` | `test_only_plant_head_can_clear_routing_review` |
| BR-06 | Costing needs the RFQ to be in costing, ready to quote or sent back. | Judgement | `create_quote` | `test_costing_requires_costing_stage` |
| BR-07 | A price is calculated only by the fixed formula. AI never sets a price. | Brief | `engine.cost_engine.cost_part` | `T10` in `engine/test_results.txt` |
| BR-08 | A quote shows three volume prices: 90,000, 1,80,000 and 2,70,000 units a part. | Brief | `create_quote` | `test_create_quote_produces_three_tiers_and_snapshot` |
| BR-09 | A quote keeps the rate version, formula version and inputs it used. | Brief | `create_quote` (`snapshot_json`) | `test_create_quote_produces_three_tiers_and_snapshot` |
| BR-10 | A missing rate, a net weight above gross weight, a zero or blank input blocks costing with a visible reason. | Brief | engine `CostError`, `create_quote` | `test_invalid_volume_and_part_inputs_are_blocked`, `test_costing_errors_come_back_as_400` |
| BR-11 | An annual quote value above ₹25,00,000 needs the Sales Head or the Deputy. Exactly ₹25,00,000 does not. | Brief | `needs_sales_head`, `create_quote` | `T21` and `T22` in `engine/test_results.txt`, `test_large_quote_requires_sales_approval` |
| BR-12 | The ₹25 lakh test uses the annual selling value before GST. | Assumption (the brief does not say) | `create_quote` | No test. Open question for Company A: confirm the GST basis before a pilot. |
| BR-13 | An estimator cannot approve a quote. | Brief | `decide_quote` | `test_estimator_cannot_approve`, `test_role_comes_from_the_session_not_the_request_body` |
| BR-14 | A send-back needs a reason of at least five characters. | Judgement | `decide_quote` | `test_send_back_requires_reason_and_returns_to_costing` |
| BR-15 | A sent-back RFQ is re-costed as a new quote version. Old versions stay. | Judgement | `create_quote` | `test_quote_versions_increment_after_send_back` |
| BR-16 | Only an approved quote can be marked as sent. | Judgement | `send_quote` | `test_sales_head_can_approve_and_quote_can_be_sent` |
| BR-17 | Every create, change, decision and sign-in is written to the audit log. Passwords and tokens are never logged. | Brief (named users, audit log) | `_audit` | `test_audit_trail_captures_approval_lifecycle`, `test_login_and_failure_are_audited` |
| BR-18 | A user has one role. The role comes from the signed-in session, never from the request. | Judgement | `current_user`, `_require_role` | `test_role_comes_from_the_session_not_the_request_body` |
| BR-19 | Five wrong passwords lock a username for 15 minutes. The same message covers a wrong user and a wrong password. | Judgement | `authenticate` | `test_lockout_after_five_failures_blocks_even_the_right_password`, `test_wrong_password_and_unknown_user_give_the_same_message` |
| BR-20 | A session ends after 8 hours or on sign-out. | Assumption | `user_for_token` | `test_expired_session_is_rejected`, `test_login_returns_working_session_and_logout_ends_it` |
| BR-21 | A trace batch is stored whole or not at all. Duplicate RFQ references and impossible date orders are refused with the row number. | Judgement | `import_trace` | `test_trace_import_is_all_or_nothing`, `test_trace_import_refuses_duplicates_wrong_role_and_reused_batch` |
| BR-22 | Only the Estimation Head can import a trace. | Judgement | `import_trace` | `test_trace_import_only_for_the_estimation_head` |
| BR-23 | Working days are elapsed weekday time divided by 24 hours. Weekends and listed holidays count as zero. Unit check: 12.5 h of costing done at 8 h a day by one estimator spans 1.56 elapsed working days, so the brief's 1.56 and the trace's costing stage are in the same unit. If the estimator splits time across RFQs, elapsed time is longer, and the trace shows it. | Assumption | `tracekit.analyze.working_days` | `test_working_days_skips_weekend`, `test_working_days_skips_listed_holiday` |
| BR-24 | If costing is more than 40% of the cycle in the Week 1 trace, cut scope to the costing screen and engine. | Judgement (go/no-go memo) | `tracekit.analyze.summarise` | `test_summary_applies_the_costing_cut_rule` |
| BR-25 | Gate 3 condition A: at least 20 coded lost RFQs and at least 25% lost to delay. | Judgement (business review) | `tracekit.analyze.summarise` | `test_gate3_needs_twenty_coded_lost_rfqs_and_a_quarter_from_delay` |
| BR-26 | Mean approval wait across all RFQs stays within 0.75 day. The ₹25 lakh limit is from the brief. Whether it sends about 70% of quotes to the Sales Head is untested; 70% is the share that keeps the mean inside the budget if each escalated quote waits one day. | Judgement | `tracekit.analyze.summarise` | `test_approval_wait_is_checked_against_the_budget` |

## Rules that are not enforced yet

| ID | Rule | Why not |
|---|---|---|
| BR-X1 | Reminder after 4 hours, escalation to the Deputy after 1 working day. Approval is never automatic. | Needs a scheduler and notifications. |
| BR-X2 | An AI-read value shows its source and blocks costing until a person accepts it. | There is no AI service in this repo. |
| BR-X3 | A user sees only their customer groups. Every drawing view is logged. | There is no file store. |
