# MarginLadder V4.0 repository audit

## Scope and preservation

This audit was completed before changing production source. The supplied archive is preserved at `work/baseline/source_archive/MarginLadder-v3_5_0(1).zip` with SHA-256 `5174982FB5D0F7ADFDDE72927ADF58ED3858EEE6FBCDF490145FD4FE8E51B361`. The source baseline is commit `4f0cc4aaf64bfc95b0268a1247be027ace521356`; its working tree was clean before audit artefacts were added.

The machine-readable inventory contains 210 Git-tracked files. Git internals (368 files) are deliberately excluded from source inspection and release packaging; they are retained only in the local working copy for provenance.

## Architecture assessment

MarginLadder is a compact, local Python product: a costing engine (`engine`), finance modules (`finance`), analytics and SQL (`analytics`), FastAPI/SQLite application (`application`), workbook twins (`model`), trace analysis (`tracekit`), and narrative/evidence documents (`docs`). This is an appropriate single-repository architecture for a demonstrator. The principal risk is not unnecessary infrastructure; it is inconsistent definitions and duplicated financial logic across Python, Excel, application snapshots, SQL, and narrative documentation.

## File-level inventory and dependency map

`v4_file_inventory.csv` and `v4_file_inventory.json` enumerate every Git-tracked file, including type, size, purpose, test status, archival signal, assumptions signal, and recommended disposition. Core dependency flow is:

`engine.cost_engine` -> `engine.tier_pricing` / `finance.unit_economics` / `application.service`; `finance.case_model` -> `finance.full_model` / scenarios / reconciliation; `application.service` -> SQLite, engine, tracekit; `analytics` -> SQL/sample events; `model/*.xlsx` -> `finance.reconcile` and validation scripts.

The repository contains intentional historical documentation in `docs/archive`, prior PRDs and prior regression reports. It should be retained as clearly labelled archive material, not used as the canonical V4 source.

## Prioritised findings

| ID | Priority | Finding | Evidence | Recommended action |
|---|---|---|---|---|
| FIN-001 | P1 | Working capital is a revenue-days proxy, not AR/inventory/AP. | `finance/full_model.py` calculates `revenue * working_capital_days / 365`. | Replace with separately modelled AR, inventory, AP, opening/closing NWC and cash-flow movements; test independently. |
| FIN-002 | P1 | Incremental economics use a combined win-back assumption rather than explicit adoption, success, control/treatment conversion and cannibalisation. | `finance/case_model.py`. | Make the counterfactual and each funnel component explicit. |
| COST-001 | P1 | Decision-layer costing declares that rework is not modelled. | `finance/unit_economics.py`. | Add traceable rework, reinspection, tooling, rush and logistics lines without changing existing cost behaviour. |
| INT-001 | P1 | Python/Excel reconciliation is dependent on workbook tooling and legacy 64 checks. | `finance/reconcile.py`; workbooks in `model`. | Preserve existing checks, add a source-of-truth register and explicitly record methodology-driven changed expectations. |
| APP-001 | P1 | The application records lifecycle and audit events but its analytics taxonomy is not canonical across all requested events. | `application/service.py`. | Add an event contract and reconcile dashboard outputs to stored records. |
| FPA-001 | P2 | Monthly planning is not an integrated forecast and needs driver-based forecast, bridge, and working-capital linkages. | `finance/monthly_plan.py`. | Extend in a separate FP&A stage. |
| DATA-001 | P2 | Sample/simulated records exist and must remain unambiguously labelled. | `data/*sample*`, simulated logs, analytics docs. | Preserve labels and prevent claims of observed performance. |
| DOC-001 | P2 | Many legacy and role documents exist, creating discoverability and version-control risk. | `docs/portfolio`, `docs/archive`, historic PRDs. | Establish canonical V4 entry points and role packs while preserving archive references. |
| QA-001 | P2 | Initial environment lacked declared workbook/test dependencies. | Initial baseline run. | Requirements installed locally; record exact validation environment in release evidence. |
| QA-002 | P3 | Baseline ruff/mypy status needs remediation before a clean release gate. | `application/service.py`, `scripts/check_consistency.py`, initial tooling run. | Fix only after functional stages, then re-run the release gate. |

## Security and data quality

The application includes role checks, password hashing, sessions, audit records, and parameterised SQLite statements. It still requires environment-specific production hardening (secret management, HTTPS, persistence/backup policy, RBAC administration, and production migration controls), none of which should be represented as complete in a local demonstrator. Inputs and simulated logs are explicitly illustrative in several modules; V4 must preserve this distinction in all dashboards and role packs.

## Baseline release assessment

The baseline was clean in Git and the scoped suite later ran successfully once dependencies were installed. The initial broad workspace command was invalid because it discovered both the preserved baseline and the working copy; it is recorded as an environment/setup failure, not a repository failure. Full command outcomes are in `v4_baseline_report.md`.

