# MarginLadder — final role audit report

## 1. Role ratings
| Role | Start rating supplied | After repository work | Conditional after user actions | Cap now | Reason |
|---|---:|---:|---:|---|---|
| Project Manager | 8.0 | **9.0** | 9.0–9.1 | Observed cap | Delivery plan and controls are findable; no live 12-week project was managed |
| APM / PM | 8.4 | **9.0** | 9.1–9.3 | Observed cap | Journey, metrics, RICE, experiment and rollback are together; no real task evidence |
| Consulting | 8.9 | **9.0** | 9.1–9.3 | Observed cap | Issue tree, sizing, options and red-team challenge are present; no client decision |
| Business Analyst | 9.1 | **9.0** | 9.1–9.3 | Observed cap | Traceability and edge-case pack improved; no stakeholder validation or independent UAT |
| Finance | 9.0 | **9.0** | 9.1–9.3 | Observed cap | Reproduction bridge and visible checks added; no real ledger or independent finance review |

No role can score above 9.0 without Observed evidence. No role can score above 9.4 without two or more independent real sources. Current scores are capped at 9.0. Conditional ranges are not promises.

## 2. Honest ceiling if no user actions happen
**9.0/10 for every role.** The documents can be clear and complete. They cannot create real users, business UAT, actual ledgers, a public deployment or realised outcomes.

## 3. Judgement calls
- The PM schedule is relative to an assumed start; no live status is reported.
- The RACI uses roles, not named people. One Accountable role is assigned to each task.
- RAID likelihood and impact are qualitative planning judgements, not measured probabilities.
- The 90 person-day base estimate plus 15 day reserve is a planning estimate with ±30% range, not a vendor quote.
- RICE and option scores are judgement inputs, not user preferences.
- Experiment success/stop thresholds are proposed rules, not measured outcomes.
- Sample size is not stated as a final number because baseline rate/variance and minimum detectable effect are unknown.
- The 40% costing-stage threshold is a proposed decision rule, not an observed threshold.
- Synthetic monthly variance values are teaching examples only.
- Industry reports are context only. They do not validate the hypothetical company's economics.
- No interviews, task sessions, expert calls, stakeholder call, UAT, live link or annual-report candidate check has happened in this package.

## 4. Key file interview notes
| File | Two-line explanation |
|---|---|
| `README.md` | One hypothetical RFQ-to-quote decision case. I recommend measure first, pilot second, automate only if evidence supports it. |
| `docs/portfolio/evidence_ledger.md` | Every recruiter-relevant claim has a source and tag. It separates tests from customer outcomes. |
| `docs/pm/12_week_delivery_plan.md` | Three gates and critical path are visible. This is a proposed schedule, not completed delivery. |
| `docs/pm/raid_log.md` | Risks and assumptions have owners, triggers and responses. All entries remain open because there is no live programme. |
| `docs/product/apm_pm_decision_pack.md` | The product bet is queue visibility with metrics and stop rules. RICE scores are judgement inputs until users validate them. |
| `docs/consulting/MarginLadder_Executive_Recommendation.pptx` | The deck frames the decision and options. The added slides show counter-arguments, decision flips and weight sensitivity. |
| `docs/ba/complete_traceability_and_process_pack.md` | Rules link to requirements, tests and screens. Open and not-built proof is marked rather than hidden. |
| `docs/finance/finance_manager_reproduction_pack.md` | The number bridge is hand-checkable. Operating payback and cash payback are separate measures. |
| `model/MarginLadder_Monthly_FP&A_Model.xlsx` | The monthly plan has driver inputs, blank actuals and six visible audit checks. The actuals are not fabricated. |
| `docs/validation/AUDITOR_FINAL_PASS.md` | The hostile review lists what passed and what did not. It preserves the unverified claims and remaining limits. |

## 5. Auditor before / after
Before: PM controls were spread; APM journey and metrics were separate; consulting lacked a visible red-team section; BA screen trace and edge cases were hard to find; Finance lacked a hand bridge and visible audit sheet.
After: dedicated PM plan, RACI, RAID, change control, status and resourcing; APM pack; consulting challenge slides; BA trace/process pack; Finance reproduction pack and recalculated Audit Checks sheet.
Still open: no real user evidence, independent UAT, live demo, candidate-performed annual-report check or actual company data.

## 6. Tests and workbook
| Check | Result |
|---|---:|
| Python tests | 163 collected; run exit 0 |
| Finance reconciliation | 64/64 matched |
| Monthly workbook validation | Exit 0; 439 formulas |
| Workbook recalculation | LibreOffice; 0 stored formula errors |
| Visible workbook checks | 6/6 PASS |
| Repository consistency | 642/642 passed |
| Portfolio release audit | 26/26 passed |
| Deck render | 16/16 slides rendered and contact sheet inspected |
| Static PNG review | 18/18 assets inspected |
| HTML dashboard browser render | Failed (Chromium exit -6); not claimed as passed |
| Python compileall | Not completed in final pass; not claimed as passed |

## 7. Five hard interview questions per role
See `docs/portfolio/interview_defence_guide.md`. The answers explicitly state where the evidence is hypothetical, derived, assumed or synthetic.

## 8. Final decision
The repository now has clear recruiter-facing evidence for all five role families. Project Manager meets the 9.0 target at the cap. The other targets above 9.0 cannot be reached honestly without real people, independent UAT, source checks and permissioned business evidence.
