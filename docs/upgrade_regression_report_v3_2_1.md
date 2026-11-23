# v3.2.1 recruiter-focused portfolio release — regression and sign-off report

**Release date:** 18 November 2026  
**Portfolio package:** 3.2.1  
**Application API:** 3.1.0 (retained; no runtime API version change)  
**Base:** v3.2.0, additive patch  
**Evidence status:** local reproducible tests and model checks only. No live customer, user, stakeholder or production evidence is claimed.

## Patch scope

This patch closes repository-owned quality and handoff issues found during the final review. It does not fabricate external validation or relabel synthetic data.

- Fixed a SQLite connection leak when `analytics.run_queries.load()` rejects invalid raw-trace input before returning its in-memory database handle. Added a regression test proving the connection is closed on that exception path.
- Added a dedicated 25-check recruiter-artefact audit for role paths, workbook structure, formula count, presentation integrity, evidence templates and claim-boundary disclosures. Wired it into the Makefile quality target and GitHub Actions CI.
- Added a release sign-off covering the four role workstreams, final internal desk checks and the explicit distinction between completed portfolio artefacts and real-world validation.
- Reframed the fieldwork checklist as an optional future live-pilot protocol rather than an unfinished repository task.
- Updated the README, app instructions and evidence register; corrected the obsolete finance-test count.

## Reproducible validation

Commands were run from the project root in the current Linux / Python 3.13.5 environment.

| Check | Result |
|---|---:|
| `pytest -q -W always::ResourceWarning` with coverage | **160 passed** |
| Total statement coverage | **92.06%** (85% minimum enforced) |
| ResourceWarning check | **No SQLite ResourceWarning observed** |
| `python -B engine/cost_engine.py` | **24/24** reference checks passed |
| `python -B -m finance.reconcile` | **64/64** legacy Excel/Python cells matched |
| `python -B -m finance.monthly_plan` | 12-period plan; base-case totals reconcile to drivers |
| `python -B -m finance.variance` | 12 metric-period output rows generated; sample values remain synthetic |
| `python -B -m analytics.product_metrics` | Synthetic event-analysis method run completed |
| `python -B scripts/check_consistency.py` | **548/548** checks passed |
| `python -B scripts/portfolio_release_audit.py` | **25/25** checks passed |
| `python -B -m compileall -q application finance tracekit analytics scripts engine` | Passed |
| Workbook structural audit | Seven expected sheets; 406 formulas; no stored error cells |
| Consulting deck archive | Valid ZIP package; 13 slides |

The test-suite command used `PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider --cov=application --cov=finance --cov=tracekit --cov=analytics --cov-report=term --cov-fail-under=85 -W always::ResourceWarning`.

## Financial base-case controls

The monthly model remains assumption-driven and does not represent actuals:

- 720 annual RFQs; 36 assumed lost RFQs; 9 assumed recovered RFQs at a 25% win-back rate.
- ₹86.4 lakh theoretical lost-RFQ contribution pool.
- ₹180 lakh incremental revenue and ₹21.6 lakh contribution in the 25% win-back scenario.
- ₹2 lakh annual run cost and ₹19.6 lakh net contribution after run cost.
- 4.9 months' operating payback after annual run cost, pre-tax and before working capital.
- ₹11.6 lakh simplified 12-month project cash proxy after ₹8 lakh setup cost, before tax and working capital.

The existing full finance model separately retains the 23.6-month tax-and-working-capital cash-payback scenario. Reconciliation proves formula consistency, not input validity or commercial feasibility.

## Tooling and environment caveats

- Ruff and mypy were not run locally because their command-line packages are not installed in this execution environment. CI installs the declared development requirements and runs both. Python bytecode compilation and the executable test/release audits passed locally.
- `pip check` reported a global environment conflict: the preinstalled MoviePy package requires Pillow below 12, while this container has Pillow 12.3.0. MoviePy is not a MarginLadder dependency and is not listed in the project's requirements; no unrelated global package was changed. This warning is not represented as a clean dependency-environment check.
- No hosted deployment, external security assessment, real business UAT, practitioner interview or independent usability study is claimed.

## Closure decision

**Approved for portfolio demonstration.** The repository-owned build, documentation, finance model, role artefacts, consulting presentation, automated checks and release packaging are complete. Interviews, moderated usability, signed business UAT, permissioned operating data, production deployment and realised outcomes remain outside a self-contained portfolio build and must only be claimed after real execution.
