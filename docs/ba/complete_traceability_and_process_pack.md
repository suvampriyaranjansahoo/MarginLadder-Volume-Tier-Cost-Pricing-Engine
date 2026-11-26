# Business Analyst — traceability and process pack

**Purpose:** let a reviewer trace a business rule to a requirement, test and screen quickly.  
**Reader:** BA interviewer, product owner, QA and operations.  
**Recruiter conclusion:** requirements are connected to workflow proof; unbuilt and untested items are visible.  
**30-second explanation:** “I turn the RFQ process into numbered rules and requirements, then connect each to acceptance tests and the screen. I separate automated tests from business UAT.”

## 1. Traceability
The table follows `docs/requirements_traceability_v3.md` and adds the screen. Rule numbers (BR-xx) are the ones in `docs/ba/business_rules.md`. `python3 scripts/check_role_packs.py` fails if any of the 26 rules is missing from the traceability tables.

| Requirement | What it protects | Rules | Automated test | UAT | Screen | Status |
|---|---|---|---|---|---|---|
| FR-01 | 9 days vs 4-day target: every RFQ has an owner, due date and age [Brief] | BR-01 to BR-03 | `test_create_rfq_persists_and_audits`, `test_assignment_update_rejects_past_due_date`, `test_overdue_rfq_can_be_reassigned_with_its_unchanged_due_date` | UAT-03 | New RFQ form; RFQ register | Built |
| FR-02 | Find an RFQ fast | none | `test_pagination_and_count`, `test_search_treats_percent_and_underscore_literally` | UAT-03 | RFQ register (search and paging) | Built |
| FR-03 | Controlled status path | BR-04, BR-05 | `test_invalid_status_transition_is_blocked`, `test_only_plant_head_can_clear_routing_review` | UAT-11 | RFQ detail (status control) | Built |
| FR-04 | Same inputs give the same price [Brief] | BR-06, BR-07, BR-08, BR-10 | `test_create_quote_produces_three_tiers_and_snapshot`; engine T10 | UAT-04 | RFQ detail (costing, three prices) | Built; parity with Company A's Excel open |
| FR-05 | Old quotes stay reproducible [Brief] | BR-09 | `test_create_quote_produces_three_tiers_and_snapshot`; engine T20 | UAT-04 | RFQ detail (quote versions) | Built |
| FR-06 | ₹25 lakh approval rule [Brief] | BR-11 to BR-13; BR-26 (approval wait budget, measured by the FR-12 KPI) | `test_large_quote_requires_sales_approval`, `test_estimator_cannot_approve`; engine T21, T22 | UAT-04, UAT-06 | RFQ detail (approval card) | Built; GST basis open (BR-12) |
| FR-07 | Send-back with a reason | BR-14, BR-15 | `test_send_back_requires_reason_and_returns_to_costing`, `test_quote_versions_increment_after_send_back` | UAT-07, UAT-08 | RFQ detail (send-back with reason) | Built |
| FR-08 | Only approved quotes go out | BR-16 | `test_sales_head_can_approve_and_quote_can_be_sent` | UAT-10 | RFQ detail (mark as sent) | Built |
| FR-09 | Audit trail [Brief: audit log] | BR-17 | `test_audit_trail_captures_approval_lifecycle`, `test_login_and_failure_are_audited` | UAT-09 | Activity and audit trail | Built |
| FR-10 | Printable quote | none | `test_print_view_requires_sign_in_and_escapes_html` | UAT-10 | Print view of the quote | Built; no signed PDF |
| FR-11 | Named users with roles [Brief: named users] | BR-18 to BR-20 | `test_login_returns_working_session_and_logout_ends_it`, `test_lockout_after_five_failures_blocks_even_the_right_password`, `test_token_is_not_stored_in_clear` | UAT-01, UAT-02 | Sign in | Built at demo grade; no MFA, no reset |
| FR-12 | Live KPIs from events | BR-23; BR-26 (reported, not enforced) | `test_kpis_use_working_days_and_report_missing_rate`, `test_approval_wait_pairs_request_and_decision` | none | Live KPIs panel | Built |
| FR-13 | Real baseline replaces the simulated log | BR-21 to BR-25 | `test_trace_import_and_summary`, `test_trace_import_is_all_or_nothing` | UAT-12 | Week-1 trace import panel | Built; waits for real data |
| FR-14 | Honest evidence labels | none | `test_dashboard_distinguishes_application_data_and_simulation` | none | Notices on dashboard and print view | Built |
| NFR-01 | Data survives upgrades | none | `test_v2_database_upgrades_without_losing_data`, `test_migrations_run_once` | none | None (start-up migration) | Built |
| NFR-02 | No secrets in the repo or the database | BR-17 | `test_password_hash_is_salted_and_verifies`, `test_token_is_not_stored_in_clear` | none | None (storage rule) | Built |
| NFR-03 | A page of the register loads in one query | none | `test_listing_includes_latest_quote_without_extra_queries` | none | RFQ register | Built |
| NFR-04 | Numbers in documents match the models | none | `test_every_python_cell_matches_the_excel_workbook` | none | None (document check script) | Built |
| AT-01 | Parity with Company A's Excel on 20 parts [Brief] | none | none | none | None yet | **Open: needs Company A's signed-off rates** |
| AT-06 | AI value shows its source and blocks costing until accepted | BR-X2 | none | none | None (not built) | **Not built** |
| AT-10 | Users see only their customer groups; drawing views logged | BR-X3 | none | none | None (not built) | **Not built** (no file store) |
| AT-12 | Six estimators and the Sales head use the register in Week 1 | none | none | none | None yet | **Open: needs a pilot** |

**Orphan rule:** a requirement with no test, UAT or screen is marked Open or Not built in the Status column, never left blank. Requirements that have no rule (for example FR-02 and FR-10) say `none`. Do not describe an automated test as business acceptance.

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
