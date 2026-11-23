# MarginLadder v2 requirements traceability

| Requirement | Product / business artefact | API / implementation | Verification evidence | Status |
|---|---|---|---|---|
| Register RFQ with owner / due date | PRD FR-01; user story US-01 | `POST /api/rfqs`, SQLite `rfqs` | `test_create_rfq_persists_and_audits`; API workflow test | Implemented in local MVP |
| Search and filter RFQs | PRD FR-02 | `GET /api/rfqs?search=&status=` | API register/filter test | Implemented in local MVP |
| Govern status transitions | PRD FR-03; existing swimlanes | `PATCH /api/rfqs/{id}` and `ALLOWED_TRANSITIONS` | invalid transition and Plant Head-only tests | Implemented in local MVP |
| Reuse the fixed costing formula | PRD FR-04; original Appendix A.3 | `POST /api/rfqs/{id}/quote` calls `engine.cost_engine.cost_part` | Original 24 engine tests + quote service tests | Implemented; client Excel parity remains open |
| Save rate / formula snapshots | PRD FR-05; user story US-05 | `quotes.snapshot_json` | snapshot and quote-version tests | Implemented in local MVP |
| Enforce ₹25 lakh approval rule | PRD FR-06; user story US-07 | `needs_sales_head` + `decide_quote` | original threshold boundary tests + positive / negative permission tests | Implemented in local MVP |
| Require send-back rationale | PRD FR-07 | `POST /api/quotes/{id}/decision` | missing-reason and return-to-costing tests | Implemented in local MVP |
| Send only approved quotes | PRD FR-08 | `POST /api/quotes/{id}/send` | approve-then-send test | Implemented in local MVP |
| Record key actions | PRD FR-09; KPI event taxonomy | SQLite `audit_events`; `GET /api/audit` | audit lifecycle test | Subset implemented; event taxonomy has future events too |
| Print quote | PRD FR-10; user story US-09 | `GET /api/quotes/{id}/print` | print-view API smoke test | Print-to-PDF via browser; no signed PDF engine |
| Show operational context | PRD FR-11; KPI dictionary | `GET /api/dashboard` | dashboard / simulation label tests | Implemented with clearly labelled simulation |
| Keep evidence labels honest | PRD FR-12; evidence register | UI notices and response metadata | API response assertions; manual copy review | Implemented as labelling controls, not a formal data-lineage platform |
| Secure customer data | User story US-11; architecture security section | Not implemented | Security is a release blocker | Not implemented; no production data allowed |
| AI extraction and provenance | User story US-03; experiment plan | Not implemented; sample values are typed | Not implemented; validate extraction benchmark first |
| Email / reminder / escalation | User stories US-01 / US-08 | Not implemented | Not implemented; requires scheduler and notification integration |

## Verification note

Tests confirm service behaviour for the local MVP. They do not demonstrate production-grade security, actual customer Excel parity, operational adoption or realised cycle-time improvements. Those require the pilot and release gates in `docs/product/PRD_v2.md`.
