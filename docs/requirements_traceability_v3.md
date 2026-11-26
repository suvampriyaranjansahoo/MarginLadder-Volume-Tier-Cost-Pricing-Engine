# Requirements traceability v3

Chain: **problem → requirement → story → rule → use case → code → automated test → UAT script → status**.
Replaces `requirements_traceability_v2.md` (kept for history). Test names are checked by `scripts/check_consistency.py`.

| Req | Problem or goal (tag) | Story | Rules | Use case | Code | Automated test | UAT | Status |
|---|---|---|---|---|---|---|---|---|
| FR-01 | 9 days vs 4-day target: every RFQ has an owner, due date and age [Brief] | US-01 | BR-01 to BR-03 | UC-01 | `create_rfq` | `test_create_rfq_persists_and_audits` | UAT-03 | Built |
| FR-02 | Find an RFQ fast | US-01 | | UC-01 | `list_rfqs`, `count_rfqs` | `test_pagination_and_count`, `test_search_treats_percent_and_underscore_literally` | UAT-03 | Built |
| FR-03 | Controlled status path | US-06 | BR-04, BR-05 | UC-02 | `ALLOWED_TRANSITIONS` | `test_invalid_status_transition_is_blocked`, `test_only_plant_head_can_clear_routing_review` | UAT-11 | Built |
| FR-04 | Same inputs give the same price [Brief] | US-04 | BR-06, BR-07, BR-08, BR-10 | UC-02 | `engine.cost_engine` | `test_create_quote_produces_three_tiers_and_snapshot`; engine T10 | UAT-04 | Built; parity with Company A's Excel open |
| FR-05 | Old quotes stay reproducible [Brief] | US-05 | BR-09 | UC-02 | `quotes.snapshot_json` | `test_create_quote_produces_three_tiers_and_snapshot`; engine T20 | UAT-04 | Built |
| FR-06 | ₹25 lakh approval rule [Brief] | US-07 | BR-11 to BR-13 | UC-03 | `needs_sales_head`, `decide_quote` | `test_large_quote_requires_sales_approval`, `test_estimator_cannot_approve`; engine T21, T22 | UAT-04, UAT-06 | Built; GST basis open (BR-12) |
| FR-07 | Send-back with a reason | US-07 | BR-14, BR-15 | UC-04 | `decide_quote` | `test_send_back_requires_reason_and_returns_to_costing`, `test_quote_versions_increment_after_send_back` | UAT-07, UAT-08 | Built |
| FR-08 | Only approved quotes go out | US-09 | BR-16 | UC-05 | `send_quote` | `test_sales_head_can_approve_and_quote_can_be_sent` | UAT-10 | Built |
| FR-09 | Audit trail [Brief: audit log] | US-11 | BR-17 | all | `_audit` | `test_audit_trail_captures_approval_lifecycle`, `test_login_and_failure_are_audited` | UAT-09 | Built |
| FR-10 | Printable quote | US-09 | | UC-05 | `render_quote_html` | `test_print_view_requires_sign_in_and_escapes_html` | UAT-10 | Built; no signed PDF |
| FR-11 | Named users with roles [Brief: named users] | US-11 | BR-18 to BR-20 | UC-07 | `auth.py`, `authenticate`, `current_user` | `test_login_returns_working_session_and_logout_ends_it`, `test_lockout_after_five_failures_blocks_even_the_right_password`, `test_token_is_not_stored_in_clear` | UAT-01, UAT-02 | Built at demo grade; no MFA, no reset |
| FR-12 | Live KPIs from events | US-01 | BR-23 | | `kpis` | `test_kpis_use_working_days_and_report_missing_rate`, `test_approval_wait_pairs_request_and_decision` | | Built |
| FR-13 | Real baseline replaces the simulated log | US-01 | BR-21 to BR-25 | UC-06 | `import_trace`, `tracekit.analyze` | `test_trace_import_and_summary`, `test_trace_import_is_all_or_nothing` | UAT-12 | Built; waits for real data |
| FR-14 | Honest evidence labels | | | | UI notices, `numbers.json` | `test_dashboard_distinguishes_application_data_and_simulation` | | Built |
| NFR-01 | Data survives upgrades | | | | `MIGRATIONS` | `test_v2_database_upgrades_without_losing_data`, `test_migrations_run_once` | | Built |
| NFR-02 | No secrets in the repo or the database | | BR-17 | | `auth.py`, `.gitignore` | `test_password_hash_is_salted_and_verifies`, `test_token_is_not_stored_in_clear` | | Built |
| NFR-03 | A page of the register loads in one query | | | | `list_rfqs` | `test_listing_includes_latest_quote_without_extra_queries` | | Built |
| NFR-04 | Numbers in documents match the models | | | | `numbers.json`, `finance/reconcile.py` | `test_every_python_cell_matches_the_excel_workbook` | | Built |
| AT-01 | Parity with Company A's Excel on 20 parts [Brief] | US-12 | | | | | | **Open: needs Company A's signed-off rates** |
| AT-06 | AI value shows its source and blocks costing until accepted | US-03 | BR-X2 | | | | | **Not built** |
| AT-10 | Users see only their customer groups; drawing views logged | US-11 | BR-X3 | | | | | **Not built** (no file store) |
| AT-12 | Six estimators and the Sales head use the register in Week 1 | US-01 | | | | | | **Open: needs a pilot** |

## Reading the status column
- **Built**: code and an automated test exist and pass.
- **Open**: needs data or people that this repo does not have.
- **Not built**: out of scope for the local MVP. The PRD lists it as a release gate.
