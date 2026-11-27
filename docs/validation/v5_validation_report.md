# v5 validation report

## Release scope

This release starts from the uploaded repository and preserves raw operational source files. It adds explicit all-units and marginal-band annual pricing to the application quote snapshot, with boundary tests and an estimator-facing selection. It retains the prior public-data benchmark as a separate company-level reference.

## Evidence classes

| Area | Status | Classification |
|---|---|---|
| `data/simulated_rfq_log.csv` and sample finance CSV | Preserved | Synthetic operational project data |
| Engine cost inputs and tier rates | Used in scenarios | Illustrative assumptions |
| Quote, contribution, break-even and capacity calculations | Computed | Derived from project assumptions |
| Bharat Forge FY2025–26 consolidated financial figures | Kept in `realdata/` | Official reported company-level benchmark |
| Bharat Forge product-, customer-, RFQ- or EN8-specific economics | Not available | Not fabricated |

## Checks run for this release

The release process ran the repository test suite, retained engine self-check, Python-versus-workbook reconciliation, SQL/Python consistency checks, benchmark calculation tests, release audit, lint and source type check. Exact outcomes are in the packaged `TEST_EVIDENCE.txt`: 292 pytest checks, 24 cost-engine checks, 64/64 workbook cells, 756 consistency checks, 26 release-audit checks and 20 role-pack checks passed.

## Independent arithmetic checks

At 180,000 units, the checked illustrative price points are ₹117.33, ₹116.51 and ₹115.77. The all-units calculation is ₹116.51 × 180,000 = ₹20,971,800. The marginal calculation is (₹117.33 × 90,000) + (₹116.51 × 90,000) = ₹21,045,600. Both use a selected-tier annual cost of ₹102.53 × 180,000 = ₹18,455,400. The resulting contributions are ₹2,516,400 and ₹2,590,200 respectively.

## Reconciliation status

- Python cost engine and the existing Excel model: retained all-units reconciliation, reported by `python -m finance.reconcile`.
- SQL and Python: existing tested analytics queries use the unchanged simulated operational dataset.
- Dashboard and service: quote snapshots supply the annual revenue used for approval and dashboard totals. New tests cover both stored schedule modes.
- Excel: the workbook is not presented as a live marginal-price schedule. That avoids implying a reconciliation that has not been modelled in spreadsheet formulas.

## Limits

The local FastAPI UI is a portfolio MVP. It is not production ERP, costing-master or contract management software. The Bharat Forge benchmark is a one-company consolidated comparison and must not be interpreted as product-level pricing or a direct peer valuation.
