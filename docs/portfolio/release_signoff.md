# MarginLadder v3.3.0 — audited correction release sign-off

**Release date:** 19 November 2026  
**Portfolio package:** 3.3.0  
**Application API:** 3.1.0 (unchanged local-demo API)  
**Decision:** approved as a recruiter portfolio demonstration, with explicit external-evidence limitations.

## Repository-owned scope completed

- Costing input validation rejects invalid and non-finite rates and costs; new boundary/adversarial tests cover rejection, overhead, scrap credit, GST, packing and freight.
- Trace analysis rejects incomplete stage pairs, out-of-lifecycle events and overlapping costing/routing/approval intervals; residual duration cannot mask over-allocation.
- Operator retention cohorts assign users to first observed activity week only.
- Dashboard scenario output is labelled as a share of simulated scenarios under selected assumptions, not a real-world probability.
- The monthly FP&A workbook links effective win-back to adoption × incremental lift; its independent semantic audit checks the base financial bridge.
- The one-page memo, go/no-go memo and 16-slide deck consistently recommend a capped measurement-led pilot before broad rollout.
- Product Finance recruiter walkthrough and role navigation are explicit.

## Reproducible local validation

| Check | Result |
|---|---:|
| Full pytest suite | **166 tests; 153 re-run and passed, 13 need FastAPI and were not run in the check environment** |
| Statement coverage | **91.97% as reported by the earlier release; not re-measured in this check** |
| Cost-engine reference checks | **24/24 passed** |
| Legacy finance workbook / Python reconciliation | **64/64 matched** |
| Monthly FP&A semantic audit | **490 formulas; independent base-case bridge passed; 0 errors after recalculation** |
| Repository consistency | **670/670 passed**; role-pack checks **20/20** |
| Recruiter artefact audit | **26/26 passed** |
| Executive memo | **1-page PDF** |
| Executive deck | **16 slides; rendered and viewed; ZIP integrity passed** |

Ruff and mypy were not available locally and were not run. Cached values in `MarginLadder_Monthly_FP&A_Model.xlsx` were written by a LibreOffice recalculation (427 formulas, 0 errors); 96 variance-sheet cells are intentionally blank until actuals are entered. Excel also recalculates on open.

## Financial decision spine

720 annual RFQs × 5% assumed lost = 36 lost RFQs. At ₹20 lakh AOV and 12% contribution margin, the theoretical contribution pool is ₹86.4 lakh. Effective win-back is modelled as 62.5% adoption × 40% incremental lift among adopted eligible RFQs = 25%. The ₹21.6 lakh result is modelled incremental contribution before programme costs, not realised benefit. After ₹2 lakh annual run cost, the operating proxy is ₹19.6 lakh; operating payback is 4.9 months before tax and working capital. The separate cash model estimates 23.6 months under its assumptions.

## External validation not completed

No real stakeholder interviews, customer discovery, signed UAT, production deployment, observed operational timestamps, price-parity test, plant-capacity validation or realised commercial outcome is claimed; these are not interviews or tests represented as completed. The portfolio artefacts are not interviews; UAT scripts are not represented as completed. These require actual participants, company data, commercial owners and permissioned evidence. The project remains a local demonstration and hypothetical decision case, not a production-ready system or validated investment proposal.
