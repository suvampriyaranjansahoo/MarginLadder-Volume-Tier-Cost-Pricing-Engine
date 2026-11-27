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
| 166 Python tests exist; 153 ran and passed in a clean check, 13 need FastAPI | pytest | Observed (test run), partly | Run: 153 passed with the API tests excluded. The 12 API tests and 1 server-import test need FastAPI and were not run in the check environment. Run `pytest` once on your own machine |
| 64 finance reconciliation cells match | `finance/reconcile.py` | Observed (test run) | Run: 64/64 |
| 670 consistency checks pass | `scripts/check_consistency.py` | Observed (test run) | Run: 670/670 |
| Scripted developer run of 3 workflow tasks (15 steps) behaves as documented | `scripts/developer_task_run.py`; `docs/validation/developer_task_run.md` | Observed (developer run), Synthetic | Run: reproducible; no person took part, so this is not user research |
| 20 role-pack checks pass (PM plan, RAID, BA rule coverage, workbook, deck) | `scripts/check_role_packs.py` | Observed (test run) | Run: 20/20 |
| 26 portfolio release checks pass | `scripts/portfolio_release_audit.py` | Observed (test run) | Run: 26/26 |
| Monthly workbook has 490 formulas and 0 stored formula errors after Calc recalc | monthly workbook | Observed (file inspection) | Recalculated with LibreOffice; 6/6 visible audit checks PASS; Tornado check PASS. 96 variance cells are blank by design |
| Win-back and lost-RFQ rate move the answer most | workbook `Tornado`; `docs/finance/tornado.png` | Derived; ranges are Judgement | Recalculated; ranges differ in size, so the rank shows where uncertainty is judged to be |
| 12-week plan: gates on days 15, 25 and 35; critical path runs through the pilot; ends day 58 of 60 | `docs/pm/plan.csv`; `scripts/make_pm_artifacts.py` | Judgement (planning estimates) | Run: generated and checked |
| Provider effort 120 person-days | `docs/pm/resourcing_effort.md` | Judgement | Run; set to agree with the earlier 24 person-week plan, so it is a consistency check, not independent proof |
| Product analytics represent real users | `data/product_events_sample.csv` | Synthetic | Read; not real usage |
| Monthly actual-vs-budget sample is real company data | `data/finance_actual_vs_budget_sample.csv` | Synthetic | Read; not actuals |
| UAT scripts exist | `docs/ba/uat_scripts.md` | Built | Read; no completed UAT |
| Bharat Forge FY26 consolidated figures (revenue ₹16,811.7 cr, PBT ₹1,676.6 cr, total assets ₹22,260 cr) | `realdata/bharat_forge_fy26.py`; NSE integrated filing, audited, 7 May 2026 | Sourced | Run: P&L chain, balance sheet and segment totals reconcile; recomputed debt/equity 0.72 equals the company's reported ratio. The candidate should still open the filing and tick-check these figures by hand |
| Case assumptions are within or outside real ranges (margin, material share, working-capital days, steel rate) | `docs/finance/real_company_benchmark.md` | Derived from Sourced data | One large company, one year; not a peer set. Marketplace steel listings are undated and unverified |
| Share price used for the valuation lines | `realdata/bharat_forge_fy26.py` | Dated-market | ₹1,991 is the BSE close on 7 May 2026, not a current price; refresh before quoting multiples |
| Interviews, task sessions, expert calls occurred | No completed log | Unverified | Not trusted |
| Customer signed off or accepted product | No signed UAT | Unverified | Not trusted |
| Production deployment or live link exists | No verified URL / deployment record | Unverified | Not trusted |
| Financial benefits realised | No ledger or customer outcome evidence | Unverified | Not trusted; no realised benefit claimed |
| Candidate independently checked annual report pages | Existing source register only | Unverified | Must complete dated source check |

**Claim boundary:** “built”, “modelled”, “tested locally” and “synthetic example” are allowed with scope. Do not say “saved”, “recovered”, “reduced”, “adopted” or “deployed” as a real result.
