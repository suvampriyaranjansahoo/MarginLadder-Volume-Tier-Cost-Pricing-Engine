# Reproducible execution evidence — MarginLadder v3.4.1

**Execution date:** 23 November 2026 (environment local to this portfolio review)  
**Scope:** repository-owned automated checks and model reproduction only. This is not client execution, production monitoring, user validation or independent business UAT.

## Commands executed against this extracted release

| Command | Result | What it proves | What it does not prove |
|---|---|---|---|
| `python -m pytest -q --disable-warnings` | Exit 0; 163 tests collected and all passed | Automated regression suite passed in this local environment | No real user acceptance, production reliability or independent code review |
| `python -m finance.reconcile` | Exit 0; 64/64 selected cells matched | Python finance model reproduces selected spreadsheet outputs | Does not validate business assumptions or source data |
| `python scripts/validate_monthly_workbook.py` | Exit 0; 439 formulas; adoption 25.0%; recovered contribution ₹21.60L; net ₹19.60L; operating payback 4.9 months | Independent base-case arithmetic and workbook formula-count check | Does not run Excel's calculation engine or prove assumptions |
| `python scripts/check_consistency.py` | Exit 0; 651/651 checks passed (post-log rerun) | Internal cross-document and path consistency | Does not establish external truth |
| `python scripts/portfolio_release_audit.py` | Exit 0; 26/26 checks passed | Required portfolio files, workbook structure, templates and release boundaries are present | Does not establish actual deployment, user testing or stakeholder sign-off |

## Reconciliation details

`finance.reconcile` matched all 64 selected outputs, including cash flow, IRR, NPV, payback and funded-gap values. The monthly workbook validator reproduced the base case. The AOV sensitivity correction is separately documented in `docs/finance/finance_manager_reproduction_pack.md`.

## Execution environment caveat

The Python environment may emit a spreadsheet-runtime warm-up warning to stderr during startup. The command exit codes and explicit check summaries above are the acceptance criteria. Preserve full CI logs when running in a clean external environment.

## External evidence still pending

- Public deployment with a verified URL and safe demo credentials.
- Five real formative usability sessions and evidence-backed iteration.
- Independent UAT-01 to UAT-12 execution by another tester.
- Named stakeholder review and sign-off.
- Practitioner challenge and representative RFQ stage-time data.
- Permissioned finance source data and approved contribution definition.

Do not relabel any of the above as complete until the corresponding evidence is captured and reviewed.
