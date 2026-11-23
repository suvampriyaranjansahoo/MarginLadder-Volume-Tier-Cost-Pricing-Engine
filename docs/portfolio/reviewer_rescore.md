# Persona 2 — BUILDER output and Reviewer re-score

## Build log by deliverable
| Deliverable | Purpose | Reader | File path | Recruiter conclusion | Acceptance test | 30-second explanation |
|---|---|---|---|---|---|---|
| 12-week Gantt | Show delivery order and gates | PM / sponsor | `docs/pm/12_week_delivery_plan.md` | Dependencies and critical path are visible | Stranger identifies gates, chain and no-live-status boundary | “Measure first, decide second, pilot third.” |
| RACI | Show one accountable role per task | Sponsor / PM | `docs/pm/raci.md` | Decision ownership is explicit | Each row has one A | “Every task has one accountable role.” |
| RAID | Show delivery exposure | PM / sponsor | `docs/pm/raid_log.md` | 16 risks/assumptions/issues/dependencies have owner and trigger | 16 rows; all required fields present | “Every major risk has an owner and response.” |
| Change and comms | Control changes and updates | Sponsor / PM | `docs/pm/change_control_and_communications.md` | Changes require impact review and approval | Request fields, approval rules and cadence exist | “No verbal scope change silently changes the baseline.” |
| RAG templates | Report status without inventing it | Sponsor | `docs/pm/status_reports_templates.md` | Three reports are blank templates | Three TEMPLATE headings and decisions-needed lines | “These are formats, not fake status reports.” |
| Effort estimate | Size resourcing | Sponsor | `docs/pm/resourcing_effort.md` | 90 base + 15 reserve = 105 PD, ±30% | Sum manually; no currency claim | “Bottom-up person-day estimate, not a quote.” |
| APM pack | Connect journey, opportunity and metrics | APM interviewer | `docs/product/apm_pm_decision_pack.md` | Product bet and stop rules are inspectable | Journey, tree, formulas, RICE, experiment, cut list and rollback included | “Visibility is first because the bottleneck is not yet proven.” |
| Consulting pack | Challenge the decision | Consulting interviewer | `docs/consulting/consulting_challenge_pack.md` | Hypothesis, sizing, alternatives and reversal facts are explicit | Issue tree, both sizing methods, options, red-team and 5 facts | “The theoretical pool is not the bottom-up addressable case.” |
| BA pack | Trace rule to screen and test | BA interviewer | `docs/ba/complete_traceability_and_process_pack.md` | Built/open/not-built evidence is separated | 10 edge cases and screen map present | “A requirement must have proof or an explicit open status.” |
| Finance pack | Reproduce headline numbers | Finance interviewer | `docs/finance/finance_manager_reproduction_pack.md` | The bridge is hand-checkable | ₹86.4L to ₹19.6L to 4.9-month operating payback reproduced | “Cash payback is separate from operating payback.” |
| Workbook audit sheet | Make formula checks visible | Finance reviewer | `model/MarginLadder_Monthly_FP&A_Model.xlsx` — `Audit Checks` | Six base-case checks visibly pass | LibreOffice recalculation; 0 stored errors | “Actuals remain blank; audit sheet checks the model outputs.” |
| Evidence ledger | Bound claims | Recruiter | `docs/portfolio/evidence_ledger.md` | Each important claim has tag and verification | Unverified claims explicitly listed | “A passing test is not a customer outcome.” |

## Reviewer re-score — same four-part rubric
Raw score is average of Findability, Depth, Clarity and Honesty. Observed cap is 9.0. Independent-source cap is 9.4. No role has real user/customer evidence, so all remain capped at 9.0.

| Role | Dimension | Start | After repository work | Proof file |
|---|---|---:|---:|---|
| Project Manager | Findability | 6.5 | 9.2 | `docs/pm/12_week_delivery_plan.md` |
|  | Depth | 7.5 | 9.0 | `docs/pm/raid_log.md` |
|  | Clarity | 7.5 | 9.0 | `docs/pm/status_reports_templates.md` |
|  | Honesty | 9.0 | 9.5 | `docs/portfolio/evidence_ledger.md` |
| APM / PM | Findability | 8.0 | 9.2 | `docs/product/apm_pm_decision_pack.md` |
|  | Depth | 8.0 | 9.2 | `docs/product/apm_pm_decision_pack.md` |
|  | Clarity | 8.0 | 9.1 | `docs/product/apm_pm_decision_pack.md` |
|  | Honesty | 9.0 | 9.5 | `docs/portfolio/evidence_ledger.md` |
| Consulting | Findability | 8.5 | 9.3 | `docs/consulting/consulting_challenge_pack.md` |
|  | Depth | 8.5 | 9.2 | `docs/consulting/consulting_challenge_pack.md` |
|  | Clarity | 8.5 | 9.1 | `docs/consulting/consulting_challenge_pack.md` |
|  | Honesty | 9.0 | 9.5 | `docs/portfolio/evidence_ledger.md` |
| Business Analyst | Findability | 9.0 | 9.4 | `docs/ba/complete_traceability_and_process_pack.md` |
|  | Depth | 9.0 | 9.2 | `docs/ba/complete_traceability_and_process_pack.md` |
|  | Clarity | 8.5 | 9.1 | `docs/ba/complete_traceability_and_process_pack.md` |
|  | Honesty | 9.0 | 9.5 | `docs/portfolio/evidence_ledger.md` |
| Finance | Findability | 9.0 | 9.4 | `docs/finance/finance_manager_reproduction_pack.md` |
|  | Depth | 9.0 | 9.2 | `model/MarginLadder_Monthly_FP&A_Model.xlsx` |
|  | Clarity | 8.5 | 9.1 | `docs/finance/finance_manager_reproduction_pack.md` |
|  | Honesty | 9.0 | 9.5 | `docs/portfolio/evidence_ledger.md` |

| Role | Raw average | Observed cap | Final after repo | User target | Result |
|---|---:|---:|---:|---:|---|
| Project Manager | 9.18 | 9.0 | **9.0** | 9.0 | Met at cap |
| APM / PM | 9.25 | 9.0 | **9.0** | 9.2 | Not met; no observed user evidence |
| Consulting | 9.28 | 9.0 | **9.0** | 9.5 | Not met; no observed independent challenge |
| Business Analyst | 9.30 | 9.0 | **9.0** | 9.5 | Not met; no observed stakeholder/UAT evidence |
| Finance | 9.30 | 9.0 | **9.0** | 9.5 | Not met; no actual ledger or independent review |

The Builder did not raise a score for effort. Scores only reflect files a recruiter can open. No remaining clearly evidenced [REPO] gap was identified within the requested scope. User targets above 9.0 require real evidence, not more templates.
