# Change log

## 3.5.0 (portfolio release; application version stays 3.3.0)
| Change | Why |
|---|---|
| `realdata/` package and `docs/finance/real_company_benchmark.md`: Bharat Forge FY26 audited consolidated filing, recomputed ratios, DuPont, cash cycle, segment margins, dated valuation | The case was fully synthetic; the ledger had an open item for checking an annual report |
| Working-capital stress test: case financials re-run with real receivable days and cash cycle (IRR 75.8% to 44.4% and 28.4%) | 45 days was the case input furthest from the real reference |
| `engine/input_guard.py`, wired into `create_quote`: gross and net weight must be above zero | The retained v1 engine never range-checked them; `net = -1` priced at about half the normal price |
| `gst` is now an accepted part input | It was filtered out, so every quote used 18% whatever was sent |
| 4 engine test functions, 2 service regression test functions (one over 3 cases) and 12 realdata tests | The guard and gst tests fail on the old code; the realdata tests pin each sourced figure |
| Superseded v1/v2 traceability and regression docs moved to `docs/archive/`; manifest re-keyed with the same hashes | `docs/` had five regression reports and three traceability versions side by side |
| `realdata` added to pytest, mypy, ruff, coverage and CI | New code gets the same gates as the rest |

## 3.4.8 (portfolio release; application version stays 3.3.0)
| Change | Why |
|---|---|
| `engine/tier_pricing.py` wired into `create_quote` | TIER_RATES was never used by the workflow; tiers now price at 117.33 / 116.51 / 115.77 (rate date 2026-11-05) |
| Customer-hold narrative reads SQL columns by name; regenerated `docs/analytics/sql_findings.md` | Off-by-one printed "present on 60 of 60" with zero holds |
| Regression tests: service, engine tier module, API-level (not run here), narrative | Each fails on the old code |
| `engine` added to pytest testpaths, ruff and mypy scope | Existing engine tests were never collected |
| `scripts/e2e_ui_check.py` gains HTTP tier-price assertions; validation docs regenerated (34 of 34) | Current results |

## 3.4.7 (portfolio release; application version stays 3.3.0)
| Change | Why |
|---|---|
| `finance/unit_economics.py`: volume-tier bands, tier comparison, cost-line shares, unit-cost sensitivity, break-even volume | Engine had no tier lookup or decision layer; boundaries were untested |
| `finance/scenarios.py`: downside / base / upside and NPV break-even win-back | Named scenarios and a decision threshold were missing |
| 43 tests (196 pass, API tests excluded) and generated `docs/finance/decision_layer_report.md` | Reproducible, tested outputs |
| 15 ruff and 5 mypy errors fixed, behaviour unchanged | CI expects both clean |
| `docs/validation/improvement_pass_report.md` | Before and after, what ran, what did not |
| `scripts/e2e_ui_check.py` and `docs/validation/ui_workflow_check.md` | Browser test of the full RFQ workflow (33 of 33 steps) against a stand-in for server.py; evidence boundary stated |

## 3.4.6 (portfolio release; application version stays 3.3.0)
| Change | Why |
|---|---|
| README rewritten: finance-led, 82 lines, scope disclosure at the top; long version kept at `docs/portfolio/README_extended.md` | README failed the repository's own consistency checks and listed a non-existent `tests/` folder |
| `data/simulated_rfq_log.csv` restored to original CRLF line endings; `.gitattributes` pins it | Byte-identity check failed after the zip normalised line endings |
| Added `one_page_brief.md`, `validation_plan.md`, `resume_and_interview.md` under `docs/portfolio/` | One-page summary, plan for real interviews, resume and interview preparation |

## 3.4.5 (portfolio release; application version stays 3.3.0)
| Change | Why |
|---|---|
| README demo section with dashboard GIF, two prototype screens and a 3-step run | The README showed no pictures |

## 3.4.4 (portfolio release; application version stays 3.3.0)
| Change | Why |
|---|---|
| `scripts/developer_task_run.py` and `docs/validation/developer_task_run.md` | A reproducible, scripted run of 3 workflow tasks on synthetic data, labelled developer-run |

## 3.4.3 (portfolio release; application version stays 3.3.0)
| Change | Why |
|---|---|
| Past due dates are rejected when an RFQ is edited | Edit path accepted what creation rejected (found in a simulated workflow test) |
| A past date is allowed only if it is the date already stored | The first version of this fix blocked reassigning overdue RFQs |
| Three regression tests added (2 service, 1 API) | 166 tests in total |
| Added independent UAT protocol (not executed) and a blank sign-off template | Defines how real acceptance would be recorded |
| Simulated defect note `docs/validation/SIMULATED_UAT_DEFECT_FIX_v3_4_3.md` | States the evidence boundary |

## 3.4.1 (portfolio release; application version stays 3.3.0)
| Change | Why |
|---|---|
| Deck: three challenge slides restyled, placed in order (option weights after the options slide; red team and what-would-change-my-mind before the appendix) | They were plain text after the appendix |
| 12-week plan computed from `docs/pm/plan.csv` (dependencies, slack, critical path, Gantt picture); gates on days 15, 25, 35 | The earlier plan used different gate names and days from `docs/strategy/rollout_30_60_90.md` |
| RAID log, RACI, change control, status templates and effort rewritten to the same task IDs and roles | One plan, one vocabulary |
| Effort reconciled: 120.2 person-days against the earlier 24 person-week plan | Two different numbers before |
| `Tornado` sheet and chart in the monthly workbook | Finance pack had a table without ranking |
| BA traceability rebuilt: rule numbers now match `docs/ba/business_rules.md`; BR-06, BR-10 and BR-26 were orphans and are now traced | The pack used rule numbers that did not match the catalogue |
| `scripts/check_role_packs.py` (20 checks) | Role packs had no automatic check |
| Stale counts and the false "no audit sheet" sentence fixed; sign-off now says what was and was not re-run | Contradictions |
| Process and coaching files moved out of the repository | Recruiters should see the work, not the review notes |

## 3.3.1 (portfolio release; application version stays 3.3.0)
| Change | Why |
|---|---|
| Monthly FP&A workbook saved with calculated values | Previewers and phones showed blank cells before |
| Removed stray `.coverage` file | Build artefact |
| Moved the upgrade plan and cleanup notes out of the repo | Internal coaching, not part of the case |
| Added Project / Programme Manager role path | Fifth front door |
| Added extension evidence to the finance, product finance and consulting paths | Decision analysis, win-back stress and market sizing were hard to find |
| README now opens with a role table | Reader picks a door, not a primary story |
| Sign-off check count 553 to 560 | The script reports 560 after the new files |

# Change log: v2.0 to v3.0

Rule followed: original `engine/`, `data/`, `model/`, `prototype/` and image files are byte-identical. `scripts/original_manifest.json` holds the v2.0 hashes. Files changed on purpose are the ones listed under "Edited original files".

## Edited original files
| File | Before | After | Why |
|---|---|---|---|
| `README.md` | 142 lines, stale claims ("27 tests", role dropdown, long finance extension text) | 70 lines, pitch, role paths, key numbers, limits | Reviewers read this first. Extension text moved to `docs/finance/extension_summary.md`, unchanged |
| `application/server.py` | Role and actor sent in the request body. No sign-in | Bearer-token sessions, role from the session, 8 new routes, security headers | A client could claim any role |
| `application/service.py` | Fixed tables, code = count + 1, list loads every row, dashboard capped | Numbered migrations, codes under `BEGIN IMMEDIATE`, one-query paged register, escaped search, uncapped counts, KPIs, trace import, users and sessions | Duplicate codes under concurrency, slow list, silent cap |
| `application/static/index.html` | Role dropdown | Sign-in, KPI panel, queue panel, trace import panel | Matches the server |
| `application/tests/test_service.py` | 21 tests | 21 tests, one import renamed | `PermissionError` shadowed a built-in; now `AccessDeniedError` |
| `application/tests/test_api.py` | 6 tests, no sign-in | 11 tests with sign-in, lockout, role spoofing, paging, trace, print | Cover the new surface |
| `application/README.md`, `docs/architecture.md`, `docs/validation/evidence_register.md` | Described v2 | Describe v3 | Stop stale claims |
| `docs/business_review.md` | Finding 11 named an earlier pack | Same finding, no pack name | Keep the repo self-contained |
| `.gitignore`, `requirements-dev.txt` | Basic | Ignore demo credentials and databases; add ruff, mypy, openpyxl, pytest-cov | Tooling |
| The v2 role-positioning file (under `docs/interview/`) | In the repo | Removed | It was interview coaching, not part of the case study |

## Added, with the reason
| Area | Added | Before | After |
|---|---|---|---|
| Security | `application/auth.py` | Anyone could pick any role | scrypt hashes, hashed session tokens, lockout after 5 failures in 15 minutes, same error for a wrong user and a wrong password |
| Data | Migrations v1 to v3 | One fixed schema | v2.0 databases upgrade in place |
| Data | RFQ code allocation | Count + 1 | Highest code + 1 inside one transaction |
| Product | `tracekit/` | Stage split was simulated only | Real timestamps give stage days, the 40% costing rule and Gate 3 conditions |
| Product | Live KPIs | None | Median cycle, approval wait, on-time share from audit events in working days |
| Finance | `finance/full_model.py`, `reconcile.py` | Excel only | Python twin, 64 of 64 cells match |
| Finance | `finance/queueing.py` | "Waiting, not costing" was asserted | Queue explains 0.57 day of the 7.44 |
| Finance | `finance/capacity.py` | Margin counted on every won-back order | Needs 46% of recovered margin to be makeable |
| Finance | Net hours | 5,400 gross only | 4,680 net of review time, ₹21.06 lakh |
| Analytics | `analytics/` | None | 7 SQL queries, RICE sensitivity, sample size and detectable effect |
| BA | `docs/ba/` additions | 12 stories, KPI dictionary | 26 rules, data dictionary, 7 use cases, 12 UAT scripts, 2 worked change requests, ER and state diagrams |
| Product | `docs/product/` additions | PRD v2, experiment plan | PRD v3, 13 decisions, roadmap with kill criteria, pilot design with sample sizes |
| Quality | `pyproject.toml`, CI, Dockerfile, Makefile | None | Lint, types, coverage floor of 85%, container |
| Control | `numbers.json`, `scripts/check_consistency.py` | Figures typed by hand in many places | One source, 400+ checks. They test that quoted figures appear, links and tests resolve and originals are unchanged; they do not read prose for meaning |

## Judgement calls
1. **Kept the original engine and Excel models untouched.** Fixes sit around them, not inside them.
2. **Counted freed estimator time as upside only.** Turning hours into cash needs more quotes or fewer people; neither is in the brief.
3. **Used Erlang C as a pressure gauge.** It runs on brief inputs. A full simulation would invent more assumptions than it removes.
4. **Chose scrypt from the standard library.** No new packages for a local demo.
5. **Kept SQLite.** One plant, one writer at a time.
6. **Labelled SQL and RICE output as simulated.** The log is simulated; the method is the point.
7. **Used a stand-in for FastAPI in the sandbox.** It was not installable here. The real route code ran, but real FastAPI has not.
8. **Left the Excel extension (DCF, comps) out of the Python twin.** It uses aggregator data and does not drive the decision.

## Corrections found while building
- The v2 evidence register said "27 tests". The suite is now 130 plus 24 engine checks.
- v2 said waiting is most of the delay but never tested the estimator queue. The model shows the queue explains under 1 day.
- v2 counted margin on all won-back orders. It did not test plant capacity.
- Net-of-review hours were 4,680, not 5,400, once a review step is added.
- Review by a reader who had not seen the repo found and fixed: working-day unit note, IRR without working-capital release (43.0%), RICE versus roadmap order, Gate 3 versus pilot timing, an implied 95% win rate, a file-upload mention, a stale 'checks everything' claim, a personal-identifier fragment in the checker.


# Change log: v3.0 to v3.1 (balanced-role upgrade)

This release is an additive upgrade on the v3 archive. The original costing engine, v3 finance workbooks, and existing prototypes are retained. Existing model assumptions and synthetic evidence are not relabelled as observed results.

## Engineering and analytics fixes
- Made ASGI service/database/demo-credential initialisation lazy and thread-safe; importing the server module is side-effect free.
- Preserved ISO-8601 timezone offsets in trace analysis; compared offset-aware timestamps as instants in the `received_at` timezone and rejected mixed naive/aware rows.
- Added explicit stage-pair coverage and complete-case stage-share calculations. Missing timestamps no longer silently contribute measured zeroes to scope decisions.
- Kept customer holds as a non-additive overlay and documented why they must not be summed into the stage stack.
- Connected raw timestamp CSVs directly to SQL analytics; incomplete stage pairs are rejected and unsent RFQs are excluded from completed-cycle SQL.
- Changed CI/Makefile ordering and cache handling so the consistency check runs after tests without tripping over generated artifacts.

## Balanced role workstreams
- Finance: `finance/variance.py` and a clearly simulated monthly actual-versus-budget sample, including favourable/unfavourable logic and a contribution bridge that is explicitly not EBITDA.
- APM/Product: `analytics/product_metrics.py` and a clearly simulated RFQ funnel, weekly active operator and cohort-retention report with metric definitions.
- Consulting: a 10-slide executive case-deck storyboard with issue tree, options, quantified economics, risks and decision gates.
- BA: UAT execution coverage distinguishes automated technical tests from business UAT, which remains pending.
- Portfolio: role-specific interview positioning and claim boundaries for all four roles.

## Version and validation
- Application/package version: 3.1.0.
- Validation results and environment limits: `docs/upgrade_regression_report_v3_1.md`.
- Added tests for timezone semantics, stage coverage, trace-to-SQL conversion, import side effects, finance variance logic and product event analytics.
- See `docs/upgrade_regression_report_v3_1.md` for exact test and reconciliation results.

## v3.1 planning baseline — recruiter-grade programme
- Added a role-specific, evidence-gated improvement programme for Finance Analyst, APM, Consulting Analyst and Business Analyst.
- Added competency mapping, phase exit criteria, scorecards, AI-use controls, fieldwork dependencies, risk controls and final definition of done.
- Added direct research links to IIBA and employer role descriptions used to shape the plan.
- No runtime behaviour, financial formula, workbook input or existing project outcome claim was changed in this planning-only update.

# Change log: v3.1 to v3.2 recruiter-focused release

This release is additive. The original costing engine, original Excel models, original browser prototypes, v3.1 app and existing case assumptions are retained. The local app API remains version 3.1.0; the repository portfolio package is v3.2.

## Added

- Finance: `finance/monthly_plan.py`, `finance/test_monthly_plan.py`, and `model/MarginLadder_Monthly_FP&A_Model.xlsx` with dashboard, editable inputs, 12-month illustrative plan, blank actual-versus-budget inputs, sensitivity, control checks and source register.
- BA: discovery and UAT execution protocol plus blank CSV templates for interview notes and UAT evidence.
- APM: discovery hypotheses, task-based usability protocol, pre-registered formative thresholds, event taxonomy and blank session template.
- Consulting: 13-slide answer-first executive recommendation deck and refreshed source-backed sector context.
- Portfolio: one-minute case brief, four role-specific recruiter paths, release evidence matrix, claim controls, AI-use disclosure and real-world validation checklist.
- Research: ACMA FY25, ICRA FY27 outlook and primary annual-report examples with comparability cautions.

## Quality and truth controls

- No interview, usability, business UAT or client sign-off has been invented.
- Monthly workbook actuals are blank by design; inputs and scenario assumptions are tagged.
- The monthly finance proxy is pre-tax and excludes working capital; it is not labelled EBITDA or free cash flow.
- Peer disclosures are used for context, not a direct SME margin benchmark or valuation multiple.
- External sources and publication dates are recorded in source registers and presentation footers.


# Change log: v3.2.0 to v3.2.1 final release hardening

- Closed a SQLite in-memory connection when a raw trace is rejected during SQL staging; added a targeted regression test.
- Added `scripts/portfolio_release_audit.py` (25 checks) and wired it into the standard quality target and CI.
- Added a recruiter-facing release sign-off with completed repository-owned scope, internal case checks and explicit external-evidence boundaries.
- Reframed the real-world checklist as a future field-validation protocol, not an incomplete build task.
- Corrected the obsolete finance test count and refreshed the current release verification report.
- Portfolio package patch version is 3.2.1; application API remains 3.1.0.
