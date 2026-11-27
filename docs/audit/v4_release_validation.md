# MarginLadder V4.0 release validation

## Executed evidence

| Check | Outcome |
|---|---|
| Stage 1 scoped baseline tests | 270 passed, 1 third-party deprecation warning |
| Stage 2 financial tests | 98 passed |
| Stage 2 full regression + legacy workbook reconciliation | 280 passed; 64 of 64 legacy Python/Excel checks match |
| Stages 3–4 finance regression | 103 passed |
| Post-change full regression | 284 passed, 1 third-party deprecation warning |
| Coverage baseline | 92% (270-test baseline) |
| Browser E2E script | Not executed: `playwright` module absent |
| Ruff | Fails: pre-existing `UP038` and `S603`, plus one new test-file unused variable identified for cleanup |
| Mypy | Fails: baseline typing issues plus new strict-test typing findings; not a clean type-check release gate |

## Reconciliation status

- Legacy Python-to-Excel: **64/64 pass** against the unchanged V3.5 workbook.
- V4 investment methodology: independent arithmetic tests pass in Python.
- SQL/application/dashboard V4 reconciliation: not completed. Canonical definitions and a source-of-truth register were added, but the app/dashboard/workbook were intentionally not represented as integrated V4 outputs.

## What changed

- Added canonical V4 investment methodology and tests in `finance/investment.py`.
- Added isolated price-waterfall and driver-based FP&A modules/tests.
- Added canonical product-event contract and tests.
- Added audit, financial methodology, execution, source-of-truth and role-evidence documentation.

## Honest limitations / remaining work

This is an evidence-backed partial V4 transformation, not a completed all-stage V4 release. The existing application was regression-tested through its Python test suite, but its UI was not browser-tested in this environment. The V4 model has not been written into Excel; the application, SQL, and dashboard have not been wired to the new V4 financial/event definitions. No production deployment, customer research, pilot, UAT, sign-off, actual results, or realised savings occurred. Ruff and mypy are not clean. These constraints must remain visible in any portfolio use.
