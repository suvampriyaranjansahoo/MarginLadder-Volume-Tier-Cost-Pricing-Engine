# Release evidence matrix — v3.4.1 portfolio release

**Status date:** 23 November 2026. This is an internal work-sample evidence matrix, not a recruiter score. **The repository artefacts and reproducible portfolio checks are complete for this release.** Rows marked as requiring real-world evidence describe a separate, future live-pilot phase; they are not unfinished code or documentation tasks.

| Evidence area | Current evidence | Status | What is still required for a stronger claim |
|---|---|---|---|
| Business problem | Hypothetical brief with explicit inputs and boundaries | Built / assumption-led | Confirm the problem with actual practitioners |
| Costing engine | Decimal-based engine, quote logic, 24 reference checks | Built and tested | Real price parity with approved rates / quotes |
| RFQ application | Local workflow, server-derived roles, approval and audit trail | Built and technically tested | Independent business UAT, security review and deployment approval |
| Finance case | Existing project/cash model, Python reconciliation, monthly model | Built and model-reconciled | Replace assumptions with permissioned data; accounting review |
| Monthly variance | Tested Decimal engine and formula-driven workbook; actual cells blank | Method demonstrated; sample data excluded | Load reconciled monthly actuals from a ledger / ERP extract |
| BA requirements | Rules, use cases, process artefacts, stories, traceability, UAT scripts | Documentation built; discovery pending | Real elicitation and executed UAT / sign-off |
| Product strategy | PRD, decision log, prioritisation, metrics, pilot and usability protocol | Product work sample built; user evidence pending | Real interviews, moderated task sessions and iteration |
| Product analytics | SQL/event funnel and cohorts on synthetic events | Method demonstrated; synthetic | Instrument actual events and define valid denominators |
| Consulting recommendation | 16-slide deck with red-team, decision-changing facts and numeric sensitivity; source register | Desk research + modelled case | Independent practitioner challenge and validated business inputs |
| Industry research | ACMA FY25 and ICRA FY27 outlook plus primary company reports | Sourced external context | Revisit before reuse; assess comparability and date |
| AI governance | Disclosure, no-fabrication policy and source-check requirement | Documented | Candidate must be able to explain and verify all AI-assisted work |
| Commercial outcomes | No observed client / pilot outcomes | Not evidenced | Permissioned baseline and post-pilot measurement |

## Portfolio release closure

The portfolio release is considered complete when the local application, deterministic engine, finance models, role artefacts, consulting presentation, evidence disclosures and automated checks are present and reproducible. All of those repository-owned deliverables are included in v3.2. The live-evidence column is deliberately separate: interviews, business UAT, permissioned data and commercial outcomes can only be produced by real participants in a real operating context. Creating fictional records to fill those fields would reduce, not improve, recruiter trust.

## Release gate interpretation

- **Built** means repository artefacts exist and can be inspected.
- **Tested** means the stated automated checks ran in the named environment.
- **Reconciled** means two implementations agree on selected outputs; it does not mean assumptions are true.
- **Pending** means a real-world activity is not represented as complete.
- **Not evidenced** means there is no valid source for an outcome claim.

## Candidate claim controls

Permitted: “Developed a local RFQ workflow MVP and a Decimal-based costing engine; built a driver-based investment case and traced key calculations through a Python model and workbook.”

Permitted with clear label: “Modelled a ₹21.6 lakh annual recovered-margin base case under a 25% win-back assumption.”

Not permitted: “Recovered ₹21.6 lakh,” “reduced quote cycle time by 56%,” “saved ₹24.3 lakh,” “improved retention,” “validated product-market fit,” or “deployed to a customer.”
