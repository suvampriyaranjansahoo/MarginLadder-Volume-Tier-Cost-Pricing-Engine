# MarginLadder transformation validation report

**Scope:** repository-owned correctness and recruiter artefacts. **Evidence type:** independently rerun local checks; not external business validation.

## Baseline and changes

Baseline from the supplied Advanced Release: 160 pytest tests passed; legacy finance reconciliation 64/64; consistency 547/547; recruiter artefact audit 25/25. The baseline contained accepted invalid costing assumptions, overlapping cross-chain intervals, non-first-activation operator cohorts, a contradictory one-page memo and a disconnected adoption sensitivity sheet.

Changes made:
- Costing engine now rejects non-finite numeric inputs, negative cost drivers, rejection rates outside [0,1), GST outside [0,1], and invalid margin values.
- Trace parser rejects lifecycle timestamps outside received-to-sent bounds, incomplete interval pairs and overlapping costing/routing/approval intervals. Residual duration is guarded against negative arithmetic.
- Operator retention cohorts now use each operator's first observed activity week exactly once.
- Dashboard Monte Carlo label now describes the share of simulated scenarios with positive NPV under selected assumptions; it is not a calibrated probability.
- Monthly FP&A effective win-back links to the Adoption Economics base row (adoption × incremental lift) rather than an independent 25% hardcode.
- One-page memo and go/no-go recommendation now consistently authorise a capped measurement-led pilot only; broad rollout remains conditional.
- Corrected the user-story traceability link and README role navigation.

## Validation performed

| Check | Result |
|---|---:|
| Full pytest suite | 163 passed |
| Costing engine reference examples | 24/24 passed |
| Legacy finance workbook / Python reconciliation | 64/64 matched |
| Monthly FP&A semantic audit | Passed; 427 formulas inspected; base-case bridge independently recomputed |
| Recruiter artefact audit | Pending final rerun in release |
| Repository consistency | Pending final rerun in release |
| PDF / PPTX archive integrity | Pending final release check |

Total measured coverage is 91.97% (pytest-cov; 85% threshold). Ruff and mypy were not installed in the environment and were not run.

The monthly workbook semantic audit independently calculates 720 annual RFQs, 36 assumed lost RFQs, ₹86.4 lakh theoretical contribution pool, 25% effective win-back, ₹21.6 lakh modelled contribution, ₹19.6 lakh after run cost and 4.9-month operating payback. Excel formulas are set to recalculate on open; this environment does not provide a trusted Excel calculation engine, so no cached-formula recalculation is claimed.

## Remaining business validation

No genuine stakeholder interviews, customer discovery, signed UAT, production deployment, observed RFQ timestamps, price-parity results, plant-capacity validation or realised financial benefit are available. The pilot protocol remains a plan. Scenario values and synthetic events must not be presented as business outcomes.
