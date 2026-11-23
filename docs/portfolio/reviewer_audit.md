# Persona 1 — REVIEWER audit

## Scoring rules
Raw role score is the average of Findability, Depth, Clarity and Honesty. No Observed evidence caps a role at 9.0. Fewer than two independent real sources caps it at 9.4. The case has no real users, client or UAT. The 9.0 Observed cap therefore applies to every role.

| Role | Findability | Depth | Clarity | Honesty | Raw | Start rating used | Effective score |
|---|---:|---:|---:|---:|---:|---:|---:|
| Project Manager | 6.5 | 7.5 | 7.5 | 9.0 | 7.63 | 8.0 | 7.6 |
| APM / PM | 8.0 | 8.0 | 8.0 | 9.0 | 8.25 | 8.4 | 8.3 |
| Consulting | 8.5 | 8.5 | 8.5 | 9.0 | 8.63 | 8.9 | 8.6 |
| Business Analyst | 9.0 | 9.0 | 8.5 | 9.0 | 8.88 | 9.1 | 8.9 |
| Finance | 9.0 | 9.0 | 8.5 | 9.0 | 8.88 | 9.0 | 8.9 |

The supplied starting ratings are the user's previous judgement, not rubric evidence. The effective scores above are the reviewer's independent starting point.

## Evidence ledger
| Recruiter-relevant claim | File / cell / line | Tag | Verification |
|---|---|---|---|
| Hypothetical Pune RFQ-to-quote case; no client or real users | `README.md`, opening case boundary | Brief | Read |
| 60 RFQs/month; 5 parts/RFQ; 9-day cycle; 4-day target | `numbers.json`; `docs/finance/decision_bridge.md` | Brief | Read; source is hypothetical brief |
| 5% lost RFQs; ₹20L AOV; 12% contribution margin | `numbers.json`; workbook `Inputs` | Brief / Assumption | Read; not independently validated |
| 720 annual RFQs | `numbers.json`; `Monthly Plan` | Derived | Recalculated: 60 × 12 |
| 36 annual lost RFQs | `numbers.json`; `Monthly Plan` | Derived | Recalculated: 720 × 5% |
| ₹86.4L lost-RFQ contribution pool | `docs/finance/decision_bridge.md`; workbook `Inputs` / `Control Checks` | Derived | Arithmetic checked |
| 25% win-back | workbook `Inputs` and `Adoption Economics`; `numbers.json` | Assumption | Read; no observed conversion lift |
| ₹21.6L recovered contribution | `docs/finance/decision_bridge.md`; `Monthly Plan` | Derived from assumption | Recalculated; not realised |
| ₹2L run cost; ₹8L implementation fee | workbook `Inputs`; `numbers.json` | Assumption | Read; no vendor quote |
| ₹19.6L net operating contribution | `Monthly Plan`; `docs/finance/decision_bridge.md` | Derived | Recalculated; pre-tax/pre-working-capital |
| 4.9-month operating payback | `Dashboard`; `docs/finance/monthly_planning_model.md` | Derived | `scripts/validate_monthly_workbook.py` passed |
| 23.6-month cash payback; ~₹14.8L deepest cash need | `finance/full_model.py`; `docs/finance/model_audit.md`; full model workbook | Derived from assumptions | `python -m finance.reconcile`: 64/64 matched |
| 5,400 gross / 4,680 net capacity hours | `numbers.json`; `docs/finance/capacity_and_queue.md` | Derived | Read; theoretical capacity, not cash savings |
| 2.5h current and 1h target costing effort per part | `numbers.json`; `docs/ba/KPI_dictionary.md` | Brief / Target | Read; target not achieved |
| Local application includes role-based workflow and approvals | `application/`; `docs/architecture.md` | Built | Read; tests passed; no production deployment |
| Cost engine uses Decimal-based arithmetic and rate logic | `engine/cost_engine.py` | Built | Read; reference tests executed by project script |
| Monthly workbook contains 8 sheets and 427 formulas | workbook inspection; `scripts/validate_monthly_workbook.py` | Built | Read; validator passed |
| Selected full-model outputs reconcile | `finance/reconcile.py` | Observed (test run) | Run: 64/64 matched |
| Monthly plan independently recomputes | `scripts/validate_monthly_workbook.py` | Observed (test run) | Run: exit 0; 427 formulas |
| Repository consistency checks pass | `scripts/check_consistency.py` | Observed (test run) | Run: 560/560 passed |
| Release audit passes | `scripts/portfolio_release_audit.py` | Observed (test run) | Run: 26/26 passed |
| Automated Python test suite passes | `pytest -q` | Observed (test run) | Run: 163 collected; exit 0 |
| Product event data represents real operators | `data/product_events_sample.csv`; `docs/product/simulated_product_analytics.md` | Synthetic | Read; not real usage |
| Monthly variance example represents company actuals | `data/finance_actual_vs_budget_sample.csv` | Synthetic | Read; not actuals |
| UAT scripts exist | `docs/ba/uat_scripts.md`; `data/templates/uat_execution_log_template.csv` | Built | Read; no completed business UAT |
| Interviews, task sessions, expert calls occurred | No completed evidence log | Unverified | Not trusted; no claim |
| Customer accepted the workflow | No signed UAT / customer record | Unverified | Not trusted; no claim |
| Product deployed to customer | No production deployment record | Unverified | Not trusted; no claim |
| Benefits realised / RFQs recovered | No customer ledger or outcome data | Unverified | Not trusted; explicitly not claimed |
| Live demo URL is active | No verified public URL | Unverified | Not trusted |
| Candidate independently rechecked annual-report figures | Source register only | Unverified | Not trusted until dated source check is recorded |

## Five biggest gaps by role

### Project Manager
1. [REPO] No integrated 12-week Gantt with three gates, dependencies and critical path.
2. [REPO] No RACI covering each delivery task with exactly one Accountable role.
3. [REPO] RAID details are not in one owner/likelihood/impact/trigger/mitigation/status log.
4. [REPO] Change control and stakeholder communication are not one usable page.
5. [REPO] No three dated-but-empty RAG report templates with explicit decisions needed.

### APM / PM
1. [REPO] Journey, opportunity tree and metrics tree are split across docs.
2. [REPO] RICE sensitivity does not make the exact rank-flipping input obvious.
3. [REPO] Experiment sample size and stop rules need one pack.
4. [REPO] Cut list and rollback checklist need direct recruiter navigation.
5. [USER] No real task sessions or user feedback exist.

### Consulting
1. [REPO] Issue tree, sizing and recommendation are spread across memo and deck.
2. [REPO] Weighted options and weight sensitivity are not prominent in the deck.
3. [REPO] Red-team challenge and five decision-changing facts are missing.
4. [REPO] External numbers need clearer source-to-number linkage in the deck.
5. [USER] No independent practitioner challenge or completed source-check log exists.

### Business Analyst
1. [REPO] Rule → requirement → test → screen trace is not consolidated.
2. [REPO] AS-IS and TO-BE pain points are not numbered against requirement IDs in one view.
3. [REPO] Ten edge cases need explicit expected handling.
4. [REPO] Data dictionary and glossary are separate from the traceability route.
5. [USER] No stakeholder rule confirmation or independent UAT has occurred.

### Finance
1. [REPO] Model map needs sheet/cell addresses for a fast hand-reproduction.
2. [REPO] Visible workbook audit checks should be explicit on a sheet.
3. [REPO] ₹86.4L → ₹19.6L → cash payback bridge needs one numbered explanation.
4. [REPO] Synthetic month-end commentary and a ranked sensitivity table need one page.
5. [USER] No real ledger, cost quote, observed win-back or independent finance review exists.

## Three likely questions the repository cannot answer
| Role | Questions |
|---|---|
| Project Manager | What was actually late? Who did you escalate to? Which delivery trade-off did you personally negotiate? |
| APM / PM | Which user said this was the most painful problem? What task did you observe fail? What changed after real feedback? |
| Consulting | Which practitioner independently challenged the recommendation? What real evidence disproved your first hypothesis? What did a client decide? |
| Business Analyst | Who approved the business rule? What happened when a real user failed UAT? Which requirement changed after elicitation? |
| Finance | Which ledger supports the 5% loss rate? Which actual cost or contribution changed? Who approved the cash-flow assumptions? |
