# v3 upgrade and regression report

The v2 report (`upgrade_regression_report.md`) is kept unchanged. This report covers v2.0 to v3.0.

## Strategy
v3 was built on a copy of v2.0. Original `engine/`, `data/`, `model/`, `prototype/` and image files are byte-identical (checked by `scripts/check_consistency.py` against a hash manifest). Files changed on purpose are listed in `CHANGE_LOG.md`.

## What changed
- Sign-in, server-side roles, lockout, 8-hour sessions, security headers.
- Numbered migrations; v2.0 databases upgrade in place.
- Safe RFQ code allocation, one-query register with paging, escaped search, uncapped dashboard counts.
- Live KPIs from audit events in working days.
- Week-1 trace import and analysis (`tracekit/`).
- Python twin of the Excel model, queue model, capacity model.
- SQL analytics, RICE sensitivity, sample-size maths.
- BA pack, PRD v3, decision log, roadmap, pilot design.

## Test results (build sandbox)
| Suite | Result |
|---|---|
| Original engine | 24 / 24 |
| Service (21) + hardening (26) | 47 / 47 |
| Trace tool | 21 / 21 |
| Finance | 31 / 31 |
| Analytics | 20 / 20 |
| Excel to Python reconciliation | 64 / 64 cells |
| API tests (11) | Ran against a stand-in for FastAPI, not the real package |

The 119 pytest tests exclude the API file. Run `pytest` after `pip install -r requirements-dev.txt` to run all 130.

## Browser check
The UI was driven in Chromium against the real route code through the stand-in. Sign-in, register, KPIs, queue panel and trace import rendered and worked. Screenshots were viewed. It has not run against real FastAPI.

## Known limits
- Real FastAPI wiring is untested here.
- Local sign-in only. No SSO, MFA or password reset.
- The Excel extension (DCF, comps) is not reproduced in Python.
- All SQL findings and the RICE ranking use simulated data.
- No users, no pilot, no deployment.
