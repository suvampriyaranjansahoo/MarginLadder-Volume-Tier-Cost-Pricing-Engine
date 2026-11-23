# Evidence ledger — recruiter claims

`Read` means inspected. `Run` means command executed in this environment. `Unverified` means no independent proof; do not use as a claim.

| Claim | Source | Tag | Verification |
|---|---|---|---|
| Hypothetical Pune auto-parts RFQ case; no client or real users | `README.md` | Brief | Read |
| 60 RFQs/month, 5 parts/RFQ, 9-day current cycle, 4-day target | `numbers.json`, `docs/finance/decision_bridge.md` | Brief | Read |
| 5% loss rate, ₹20L AOV, 12% margin | `numbers.json`, workbook `Inputs` | Brief / Assumption | Read; unverified externally |
| 720 annual RFQs, 36 lost RFQs | workbook `Monthly Plan`; `numbers.json` | Derived | Arithmetic checked |
| ₹86.4L theoretical contribution pool | `docs/finance/decision_bridge.md`; workbook `Control Checks` | Derived | Arithmetic checked |
| 25% effective win-back | workbook `Inputs` / `Adoption Economics` | Assumption | Read; not observed |
| ₹21.6L modelled recovered contribution | workbook `Monthly Plan`; `docs/finance/decision_bridge.md` | Derived from assumption | Arithmetic checked; not realised |
| ₹2L run cost; ₹8L implementation fee | workbook `Inputs`; `numbers.json` | Assumption | Read; no quote |
| ₹19.6L net operating contribution | workbook `Monthly Plan` | Derived | Independently recalculated |
| 4.9-month operating payback | workbook `Dashboard`; `Audit Checks` | Derived | LibreOffice recalculated |
| 23.6-month cash payback; ~₹14.8L cash need | `finance/full_model.py`; `docs/finance/model_audit.md` | Derived from assumptions | 64/64 selected cells match |
| 5,400 gross / 4,680 net capacity hours | `numbers.json`; `docs/finance/capacity_and_queue.md` | Derived | Read; not cash savings |
| Application workflow and costing engine exist | `application/`, `engine/` | Built | Read; test suite run |
| Python automated regression suite passes | pytest | Observed (test run) | Run: 163 collected; exit 0 (latest recorded run; see execution evidence log) |
| 64 finance reconciliation cells match | `finance/reconcile.py` | Observed (test run) | Run: 64/64 |
| 651 consistency checks pass | `scripts/check_consistency.py` | Observed (test run) | Run: 651/651 |
| 26 portfolio release checks pass | `scripts/portfolio_release_audit.py` | Observed (test run) | Run: 26/26 |
| Monthly workbook has 439 formulas and 0 stored formula errors after Calc recalc | monthly workbook | Observed (file inspection) | Recalculated with LibreOffice; 6/6 visible audit checks PASS |
| Product analytics represent real users | `data/product_events_sample.csv` | Synthetic | Read; not real usage |
| Monthly actual-vs-budget sample is real company data | `data/finance_actual_vs_budget_sample.csv` | Synthetic | Read; not actuals |
| UAT scripts exist | `docs/ba/uat_scripts.md` | Built | Read; no completed UAT |
| Interviews, task sessions, expert calls occurred | No completed log | Unverified | Not trusted |
| Customer signed off or accepted product | No signed UAT | Unverified | Not trusted |
| Production deployment or live link exists | No verified URL / deployment record | Unverified | Not trusted |
| Financial benefits realised | No ledger or customer outcome evidence | Unverified | Not trusted; no realised benefit claimed |
| Candidate independently checked annual report pages | Existing source register only | Unverified | Must complete dated source check |

**Claim boundary:** “built”, “modelled”, “tested locally” and “synthetic example” are allowed with scope. Do not say “saved”, “recovered”, “reduced”, “adopted” or “deployed” as a real result.


## Evidence-gap status (this release)

| Gap | What this archive can prove now | What remains genuinely external |
|---|---|---|
| Project execution | Local automated test suite, finance reconciliation, workbook validation and consistency checks; see `docs/validation/EXECUTION_EVIDENCE_LOG.md` | Public deployment, independent code review, production use, real operational outcomes |
| APM / PM | Product hypotheses, metrics, experiment protocol, blank usability capture template and pre-registered formative gates | Five real task sessions, observed friction, iteration and retest |
| Consulting | Explicit top-down arithmetic, transparent unmeasured bottom-up gap, weighted options and numerical rank-flip sensitivity | Practitioner challenge, representative stage-time evidence and validated economics |
| Business Analyst | Traceability, 12 UAT scripts and blank execution log | Independent execution by business-role testers and named stakeholder acceptance |
| Finance Analyst | Corrected sensitivity arithmetic, model map, workbook validation and reconciliation | Permissioned ledger data, approved contribution definition, actuals and independent finance review |

No external activity is simulated or represented as completed. A completed template, a test run, a synthetic dataset and a real stakeholder sign-off are different evidence classes.
