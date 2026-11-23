# Persona 3 — Auditor final pass (corrected for v3.4.1)

**Review date:** 23 November 2026  
**Case status:** hypothetical work sample. This is an artefact and reproducibility audit, not an external client audit.

## Recruiter-facing evidence
1. `README.md` — states hypothetical case, local MVP and claim boundaries.
2. `docs/portfolio/evidence_ledger.md` — separates brief inputs, derived arithmetic, assumptions, synthetic data and external evidence still missing.
3. `docs/consulting/MarginLadder_Executive_Recommendation.pptx` — 16 slides; slides 14–16 cover red-team challenges, decision-changing facts and numeric weight sensitivity.
4. `model/MarginLadder_Monthly_FP&A_Model.xlsx` — formula-driven monthly model with actuals blank and an `Audit Checks` sheet.
5. `docs/pm/12_week_delivery_plan.md` — proposed delivery plan, not a record of completed delivery.

## Finance correction
The AOV sensitivity is corrected in `docs/finance/finance_manager_reproduction_pack.md` using:
`9 recovered RFQs × AOV × 12% contribution margin − ₹2.0L annual run cost`.

| AOV | Correct net operating contribution |
|---:|---:|
| ₹16L | ₹15.28L |
| ₹20L | ₹19.60L |
| ₹24L | ₹23.92L |

The previous endpoint values ₹12.4L and ₹26.8L were errors and are superseded. Workbook base-case validator still reproduces 25% adoption, ₹21.60L recovered contribution, ₹19.60L net operating contribution and 4.9-month operating payback.

## Consulting sensitivity
The consulting challenge pack and slide 16 are aligned. Under base weights (25/20/20/20/15), the weighted scores are 4.45 / 3.75 / 3.60 / 2.20 for register / process redesign / costing screen / full integration. Under benefit-heavy weights (10/10/10/60/10), scores are 3.70 / 2.90 / 3.80 / 3.60. This is analyst-judgement sensitivity, not user-validated preference.

## Executed local checks
See `docs/validation/EXECUTION_EVIDENCE_LOG.md` for scope and caveats.

| Check | Result |
|---|---:|
| pytest | 163 collected; all passed; exit 0 |
| `python -m finance.reconcile` | 64/64 selected cells matched |
| `python scripts/validate_monthly_workbook.py` | Exit 0; 439 formulas; base case reproduced |
| `python scripts/check_consistency.py` | 651/651 passed |
| `python scripts/portfolio_release_audit.py` | 26/26 passed |
| Workbook stored error cells | 0 at the time of archive inspection; not a substitute for recalculation after future edits |

The Python environment may emit a spreadsheet-runtime warm-up warning to stderr. The recorded commands returned exit 0.

## External evidence boundary — still pending
- No real user interviews or task sessions have occurred.
- No independent UAT has been executed.
- No stakeholder has signed off.
- No production deployment or public live URL is evidenced.
- No real RFQ trace, price-parity reference set, finance ledger or realised benefit is evidenced.
- Consulting option scores remain judgement inputs pending practitioner challenge and operating data.

The archive now contains execution-ready protocols and blank capture/sign-off templates for these activities. It does **not** claim those activities have occurred. The next evidence step requires real participants and authorised source data; it cannot be completed honestly by editing documentation.

## Verdict
Repository-owned arithmetic, documentation consistency and local automated checks are improved and reproducible. The project remains a strong hypothetical portfolio build, not a validated client implementation. Do not claim real user validation, independent business acceptance, deployment or realised commercial impact.
