# Improvement pass report (v3.4.8)

Scope: a repository review against the "master improvement prompt". Everything below was executed in this pass unless it
says "not run". The case remains hypothetical; no figure is an observed business result.

## 1. Baseline (before)

| Area | Finding |
|---|---|
| Capabilities already present | Decimal costing engine with dated rate master and quote snapshots; FastAPI + SQLite workflow with role checks and audit events; Excel model with a Python twin (64 cells); monthly plan and variance modules; SQL analytics reconciled to Python; tornado, scenario grid and break-even win-back; evidence ledger |
| Tests | 153 passed (API tests and one ASGI import test excluded: FastAPI not installable here) |
| Consistency checks | 661 of 669 passed (README rules, one CSV hash, see below) |
| Lint / types | ruff reported 15 errors and mypy 5 errors with current versions, although CI expects both clean |
| Gap: volume tiers | The engine takes a volume but has no tier table; tier rates were a demo dictionary, so there were no boundary tests |
| Gap: decision layer | No cost-line shares, no unit-cost sensitivity (material, rejection, cycle time), no break-even volume at a quoted price |
| Gap: named scenarios | Win-back grid existed; no explicit downside / base / upside, and no NPV-based decision threshold |
| Gap: rework | The PRD formula has a rejection allowance but no separate rework cost |
| Recruiter-facing | README failed its own checks; structure tree listed a folder that does not exist |

`engine/cost_engine.py` is a retained v1 file that the repository's integrity check requires to stay byte-identical, so
new logic wraps it instead of editing it.

## 2. What changed

| Change | Where |
|---|---|
| Volume-tier band lookup with inclusive lower bounds, below-first-tier and malformed-band errors | `finance/unit_economics.py` |
| Tier comparison, cost-line shares, nine-shock unit-cost sensitivity at a held price, break-even volume (exact boundary search) | `finance/unit_economics.py` |
| Downside / base / upside scenarios and an NPV break-even win-back, with and without working-capital release | `finance/scenarios.py` |
| 43 new tests: tier boundaries, half-up rounding, line sums, historical quote reproducibility, shocks vs manual recalculation, break-even boundary, scenario ordering, agreement with `numbers.json` | `finance/test_unit_economics.py`, `finance/test_scenarios.py` |
| Generated, reproducible report of the decision layer | `scripts/make_decision_layer_report.py`, `docs/finance/decision_layer_report.md` |
| 15 ruff and 5 mypy errors fixed without changing behaviour (explicit `zip(strict=False)`, a None guard, a type annotation, formatting, one unused variable) | `analytics/`, `tracekit/`, `scripts/`, `finance/test_monthly_plan.py` |
| README rewritten and made to pass its checks; CSV line endings restored (CRLF) | `README.md`, `data/simulated_rfq_log.csv` |

## 3. Test execution (what actually ran)

| Check | Result |
|---|---|
| `pytest` excluding `application/tests/test_api.py` and one ASGI import test | 228 passed (153 at the baseline; the engine folder is now collected, which adds 27 including 17 existing tests that default `pytest` and CI never ran) |
| `python engine/cost_engine.py` self-tests | 24 of 24 |
| `python -m finance.reconcile` (Python twin vs workbook values) | 64 of 64 cells match |
| `scripts/check_consistency.py` | 684 of 684 |
| `scripts/portfolio_release_audit.py` | 26 of 26 |
| `scripts/check_role_packs.py` | 20 of 20 |
| `ruff check .` and `mypy` with the settings in `pyproject.toml` | clean (ruff 0.16.9, mypy 2.3.1; both satisfy the `requirements-dev.txt` bounds). mypy now covers 44 files including `engine/` (only `engine/cost_engine.py` is exempt). **Not the full dev environment**: FastAPI is not installed here, so `application/server.py` was not type-checked against FastAPI types (`ignore_missing_imports = true`) |
| `application/tests/test_api.py` (13 tests including the new tier-price test; it compiles) and the ASGI import test | **Not run**: FastAPI is not installed and package installs are blocked in this environment. Run `pytest` locally |
| Browser workflow (`scripts/e2e_ui_check.py`): sign-in, create RFQ, cost 3 tiers, API tier-price assertions, send back, approve, send, print, trace import, refusals | 34 of 34 steps passed against a **stand-in for `server.py`** (FastAPI not installable here); see `docs/validation/ui_workflow_check.md` |
| Prototype pages in Chromium | No script errors, no dead buttons found |
| Coverage gate (85%) | **Not measured** here |
| Workbook recalculation in Excel or LibreOffice | **Not re-run**; reconciliation compares Python with the values stored in the workbook |

## 4. Reconciliation

- Python vs Excel: 64 of 64 headline cells match (existing `finance/reconcile.py`).
- SQL vs Python: percentile, stage-share and variance-share queries are tested against the Python rule in `analytics/test_queries.py` (passing).
- New scenario outputs: the base scenario equals `numbers.json` for NPV (within INR 1), IRR (within 0.001) and peak funding (within INR 1), tested.
- Definitions that look similar but differ: 11.6% is the win-back that recovers fee and run cost in one year; the three-year NPV threshold is 7.2% with working-capital release and 13.1% without it. The second figure is higher than 11.6%, so the working-capital release assumption can change the decision.

## 4b. Defects found and fixed in the follow-up pass

| Defect | Evidence before | Fix | Regression test |
|---|---|---|---|
| `TIER_RATES` was never used by quote generation: every tier was costed on the single dated material rate | Service quote for 2026-11-05 gave 116.63 / 116.51 / 116.48 instead of the PRD example 117.33 / 116.51 / 115.77 | `engine/tier_pricing.py` applies the TIER_RATES differences (+1, 0, -1 INR/kg) to the dated master rate; `create_quote` uses it. Snapshots record the adjusted version (`v17+1`, `v17`, `v17-1`) | `application/tests/test_service.py` (3 prices, snapshot labels, multi-part sums), `engine/test_tier_pricing.py`, API-level test in `test_api.py` (not run here), and an HTTP assertion in `scripts/e2e_ui_check.py` (passes) |
| Customer-hold narrative read SQL result columns by position and was off by one | Generated report said "present on 60 of 60" beside a table showing 0 RFQs with a hold; with holds present it printed the count as the mean | Narrative reads columns by name | Three tests in `analytics/test_queries.py`; they fail on the old code and pass on the new |
| `engine/` tests were outside `testpaths`, so default `pytest` and CI never ran them | 17 existing tests in `engine/test_input_validation.py` not collected | `engine` added to `testpaths`; new engine files also brought under ruff and mypy | n/a |

## 5. Known limitations and not done

- `application/server.py` (the FastAPI layer) was **never started** in this environment. The page and service layer were tested through a stand-in that mirrors its routes.
- No defects were found in the page or prototypes; the only fixes made were lint, type and README/CSV issues listed above.
- Dashboard and Excel workbook were **not rebuilt or restyled** in this pass; existing artefacts and screenshots are unchanged.
- Rework cost is not modelled (PRD formula limitation); adding it needs a formula-version bump and a change to the retained engine.
- Fixed versus variable cost separation, budget-vs-actual on real data, and customer-level SQL are not extended; actuals are synthetic.
- Tier rates, scenario assumptions (37.5% win-back, 30 and 60 working-capital days, INR 2.5 lakh run cost) are illustrative.
- No real users, interviews, UAT or deployment; see `docs/portfolio/validation_plan.md`.

## 6. Readiness (evidence-based, entry-level)

Finance analyst roles about 8.5 of 10, business analyst about 7.5, product analyst about 7, consulting about 7. This pass improves
rigour (boundaries, sensitivity, scenarios, clean lint and types) but does not change the biggest gap, which is the lack of real-world
validation.
