# V4 baseline validation report

## Immutable baseline

- Archive SHA-256: `5174982FB5D0F7ADFDDE72927ADF58ED3858EEE6FBCDF490145FD4FE8E51B361`
- Git commit: `4f0cc4aaf64bfc95b0268a1247be027ace521356`
- Git status before audit artefacts: clean
- Python used: 3.12.10

## Results

| Check | Result | Evidence / limitation |
|---|---|---|
| Initial workspace-wide pytest | Not a valid repository result | It discovered both `work/baseline/extracted/repo` and `work/MarginLadder-v4_0`, causing import-file mismatches. It also revealed missing `openpyxl`. |
| Scoped repository pytest after dependencies | Pass | `270 passed, 1 warning in 20.02s`. Warning: Starlette `BlockingPortal` deprecation. |
| Coverage | Pending capture | The combined command did not return coverage output before the execution window elapsed; it must be rerun as a discrete release check. |
| Ruff | Baseline fail | `UP038` in `application/service.py`; `S603` in `scripts/check_consistency.py`. |
| Mypy | Baseline unavailable then pending | `mypy` was initially absent. It was installed from the declared development requirements and must be recorded from a discrete run. |
| Workbook reconciliation | Pending capture | Initially blocked by missing `openpyxl`; dependency subsequently installed. |
| App startup / browser E2E | Pending | Must run in the application stage, against a clean database. |

No test outcome above is inferred from a document or prior release report. Pending means not yet executed successfully in this run.
