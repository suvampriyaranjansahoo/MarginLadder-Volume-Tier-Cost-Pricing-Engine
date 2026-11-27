# V4 financial reconciliation report

## Scope

Stage 2 adds `finance/investment.py` as the canonical V4 decision model. It does **not** overwrite the V3.5 workbook or its Python twin. This avoids presenting an unreconciled workbook as a corrected V4 source.

## Checks executed

| Check | Result |
|---|---|
| Financial regression suite | Pass — 98 tests |
| New V4 methodology tests | Included in the 98 tests |
| Independent manual first-operating-month check | Included in the 98 tests |
| Existing Python-to-Excel 64-cell reconciliation | Preserved and deferred for rerun at Stage 10; source workbook unchanged in Stage 2 |

## Reconciliation identities

- `NWC = AR + Inventory - AP`
- `change NWC = closing NWC - opening NWC`
- `FCF = operating cash flow - capex - change NWC`
- Net incremental orders are control/treatment lift less cannibalisation, not recovered RFQs.

## Known boundary

Python V4 results must not yet be compared to unchanged workbook cells as if they should agree. The V3.5 workbook intentionally retains the prior revenue-days proxy. Stage 10 must update/reconcile the workbook and produce a refreshed cross-system evidence report; until then V4 investment outputs are Python-only and labelled accordingly.
