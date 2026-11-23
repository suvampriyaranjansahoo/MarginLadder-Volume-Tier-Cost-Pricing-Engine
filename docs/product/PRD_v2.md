# MarginLadder Product Requirements Document — v2 MVP

**Product:** MarginLadder RFQ-to-quote workflow and costing workspace  
**Version:** 2.0 · **Status:** portfolio MVP, not production deployment  
**Business context:** hypothetical Pune auto-components manufacturer; no live client or customer information is included.

## 1. Product thesis

MarginLadder should reduce controllable time and rework in the RFQ-to-quote process by making ownership, stage age, costing inputs, rate versions and approval decisions visible in one workflow. It is not simply a faster calculator. The product hypothesis is that a shared register, reproducible costing and clear decision rights can reduce avoidable coordination delays while protecting commercial and technical quality.

The project brief gives a nine-working-day current cycle and a four-day target. Costing work is 2.5 hours per part for five parts per RFQ. That equals 12.5 hours, or 1.56 eight-hour workdays. The residual 7.44 days is not a measured wait-time breakdown; the stage-level dataset in this repository is simulated and must be replaced with a Week 1 timestamp trace. The local MVP supports multiple part lines but assumes one common annual-volume tier per part and one of each line per quoted set; separate line quantities / BOM ratios are a production-model enhancement.

## 2. Target users and jobs to be done

| Persona | Primary job | Product need | Decision rights |
|---|---|---|---|
| Estimator | Produce an accurate quote from an RFQ | Assigned queue, accepted inputs, deterministic cost and quote history | Create/update RFQ, run costing, prepare quote |
| Estimation Head | Balance workload and protect quote quality | Ageing, ownership, due dates, exceptions and rework visibility | Reassign owner, review estimator work |
| Plant Head | Protect manufacturability | Review genuinely new or materially changed routing assumptions | Clear routing review |
| Sales Head / Deputy | Make timely commercial decisions | One approval view with annual value, price, margin and reason | Approve or send back quotes above threshold |
| Managing Director | Decide whether the process investment is worthwhile | Reconciled KPIs, benefit bridge, cash implications and stage gates | Fund, pause, reduce scope or stop |

**JTBD statement:** When a customer RFQ arrives, the team needs to know who owns it, what evidence is missing, which rate set applies and who must decide next, so that an accurate and commercially governed quote can be sent without avoidable waiting.

## 3. Product goals and non-goals

### Goals
1. Provide one visible RFQ record with owner, due date, status and ageing.
2. Make quote calculations reproducible from accepted inputs, formula version and effective-dated rate snapshots.
3. Enforce role-appropriate routing and commercial approval decisions at the service layer.
4. Preserve an auditable event trail for RFQ and quote changes.
5. Provide decision-quality operational and financial evidence while clearly separating brief facts, derived values, assumptions and synthetic data.

### Non-goals for this MVP
- Production authentication, SSO, customer-group access controls or secure drawing storage.
- Actual OCR, LLM extraction or autonomous AI decisions.
- ERP / CRM integrations, customer portal, email reminders or scheduled escalation.
- Multi-plant rate masters, multi-currency or production-grade tax configuration.
- Replacement of the client's Excel until a signed 20-part parity test has passed.

## 4. Core workflow

1. **Register:** create RFQ, customer, part description, owner and due date.
2. **Triage:** estimator moves new work to costing; estimation head manages assignment and due dates.
3. **Technical review:** a new routing can be sent to Plant Head; only Plant Head clears that review in the prototype.
4. **Cost:** estimator enters accepted values; the original Python engine calculates 90k / 180k / 270k volume tiers using effective-dated rates.
5. **Commercial approval:** annual quote value above ₹25,00,000 requires Sales Head / Deputy approval. The demo measures annual selling value before GST; the brief does not specify whether the approval threshold should include GST, so validate this convention in discovery. A send-back requires a written reason. Approval is never automatic.
6. **Send:** only an approved quote can be marked sent.
7. **Audit:** each create, update, cost, decision and send action creates a timestamped event.

## 5. Functional requirements and acceptance criteria

| ID | Requirement | Acceptance criteria | v2 evidence |
|---|---|---|---|
| FR-01 | RFQ register | Create and retrieve RFQs with customer, part, owner, due date and status | API + SQLite + UI |
| FR-02 | Search/filter | Search RFQ code, customer, part or owner; filter by status | UI + API tests |
| FR-03 | Status governance | Disallow invalid transitions; Plant Head alone clears routing review | Service validation + tests |
| FR-04 | Deterministic costing | Produce three tiers using the original `cost_engine.py` | Existing engine + service tests |
| FR-05 | Quote snapshots | Store formula version, quote date, line inputs, rate versions and tier outputs | SQLite JSON snapshot |
| FR-06 | Approval threshold | Pre-GST annual value > ₹25 lakh requires Sales Head / Deputy; GST basis must be validated | Service-level role checks + tests |
| FR-07 | Send-back reason | Require at least five characters and return quote to costing queue | Service validation + tests |
| FR-08 | Quote release | A quote can be marked sent only after approval | Service-level transition + tests |
| FR-09 | Audit trail | Store actor, demo role, event type, timestamp and structured details | SQLite audit log + UI |
| FR-10 | Printable quote | Provide a print stylesheet and browser Print / Save as PDF path | `/api/quotes/{id}/print` |
| FR-11 | Operational context | Show local register KPIs and separately label synthetic cycle-time analysis | Dashboard API + UI |
| FR-12 | Evidence integrity | Do not label simulated records or assumptions as observed client results | README, evidence register, UI labels |

## 6. Product metrics

**North Star candidate:** percentage of addressable RFQs sent within four working days, measured on a defined cohort and excluding customer-caused holds only when the hold reason and start/end timestamps are recorded.

Supporting metrics and exact formulas are in `docs/ba/KPI_dictionary.md`. The v2 local application records events and computes current register counts; it does not yet calculate a valid live cycle-time baseline because the seeded RFQs are illustrative and not a measured operating history.

## 7. Non-functional requirements

- **Calculation integrity:** reuse the deterministic Decimal-based engine; never substitute client-side arithmetic for quote calculation.
- **Reproducibility:** persist inputs, quote date, formula version and effective rate versions with each quote.
- **Auditability:** decision events record actor, demo role, time and decision reason.
- **Usability:** responsive register and detail workspace; visible empty, error and status states.
- **Data integrity:** SQLite foreign keys, unique RFQ code and quote version per RFQ; validation before persistence.
- **Security boundary:** local demo role switching is not authentication. The application must not be exposed to public networks or used with confidential customer drawings or production rates.

## 8. Prioritisation and roadmap

| Priority | Capability | Rationale | Exit evidence |
|---|---|---|---|
| P0 | RFQ register, status governance, costing and quote snapshots | Core workflow and commercial correctness | Regression tests; Excel parity gate still open |
| P0 | Approval roles and audit trail | Prevent unauthorised quote decisions in the demo workflow | Negative permission tests and audit assertions |
| P1 | User authentication, customer tenancy and secure file access | Required before any real customer information | Threat model, security review, access tests |
| P1 | Actual drawing/part-list extraction with source provenance and human review | Reduce data entry without allowing AI to set prices | Labelled benchmark set, extraction precision/recall and human override tracking |
| P1 | PDF generation, email delivery and reminder/escalation scheduler | Close the end-to-end quote loop | Delivery logs, template tests and notification audit |
| P2 | ERP/CRM integration and historical quote search | Reduce re-keying and improve repeat-part reuse | Reconciliation and data ownership sign-off |
| P2 | Multi-plant / multi-currency / customer-specific commercial terms | Scale beyond initial case | Configuration and regression suite |

## 9. Release gates

- **Gate 0 — Discovery:** interview estimators, estimation head, plant head and sales; confirm lost-RFQ definition and reason codes.
- **Gate 1 — Baseline:** trace at least 10 recent RFQs from received to sent and separate touch time from queue time.
- **Gate 2 — Early release:** use register and clock with the six-estimator group; validate status definitions and assignment behaviour.
- **Gate 3 — Costing and approval:** pass 20-part Excel parity to ₹0.01 per line, validate rate ownership and obtain Plant Head confirmation of available capacity.
- **Gate 4 — Controlled rollout:** complete access controls, audit review, user acceptance and support handover.

## 10. Open questions / assumptions to validate

- Does the 5% lost-RFQ rate exclude no-bids and capacity rejections?
- What proportion of losses were genuinely caused by slow quotation turnaround?
- Can the plant manufacture recovered orders without displacing higher-value work?
- Are 90k / 180k / 270k the right commercial volume tiers for each part family?
- Are the ₹25 lakh approval threshold and the 70% approval-load assumption still valid?
- Which ERP extract is authoritative for material, machine and overhead rates?
- What customer confidentiality, retention and audit requirements apply to drawings and historical quotes?

## 11. Definition of done for a production pilot

No production pilot should begin until security and tenancy are implemented, the costing engine matches signed-off company Excel on 20 representative parts to ₹0.01 per line, the timestamp baseline is independently checked, quote PDF output matches on-screen values, users complete role-based UAT, and rollback / support ownership is agreed.
