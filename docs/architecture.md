# MarginLadder v3 architecture and implementation boundaries

## 1. Architecture overview

```text
Browser UI (HTML / CSS / JavaScript)
        |
        | JSON over local HTTP
        v
FastAPI route layer (`application/server.py`)
        |
        v
Service layer (`application/service.py`)
   |            |               |
   |            |               +--> Audit event writer
   |            +--> SQLite persistence (RFQs / quote versions / events)
   +--> Original deterministic costing engine (`engine/cost_engine.py`)
                         |
                         +--> Effective-dated rate lookup + Decimal formulas

Separate analysis layers:
Excel finance models + Python twin (`finance/full_model.py`, reconciled by `finance/reconcile.py`)
Queue and capacity models (`finance/queueing.py`, `finance/capacity.py`)
Trace tool for real timestamps (`tracekit/`)
SQL and decision tools on the simulated log (`analytics/`)
Simulated workflow source: `data/simulated_rfq_log.csv`
Single source of truth for figures: `numbers.json` (`scripts/build_numbers.py`)
```

## 2. Main data entities

| Entity | Key fields | Integrity rule |
|---|---|---|
| RFQ | id, code, customer, part, owner, received_at, due_date, status | Unique RFQ code; status transition validation |
| Quote | id, rfq_id, version, status, quote_date, approval_required, annual_value, snapshot | Unique version per RFQ; immutable calculation snapshot is retained |
| Audit event | entity_type, entity_id, event_type, actor, role, details, created_at | Append-only insert path in the service; records action context |

Quote snapshots retain the quote date, formula version, line inputs, three volume tiers, cost lines and rate versions. A changed rate in the original rate master does not rewrite a saved JSON snapshot. The current MVP assumes the selected annual volume applies equally to every line and sums line prices into a per-set price; customer BOM ratios and independent per-line quantities are future model enhancements.

## 3. API surface (v3.1.0)

Public: `GET /`, `GET /api/health`, `POST /api/login`. Everything else needs `Authorization: Bearer <token>`.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/logout`, GET `/api/me` | End a session; who am I |
| GET | `/api/dashboard`, `/api/kpis` | Counts (SQL, not capped) and live KPIs from audit events in working days |
| GET | `/api/finance-case` | Tagged base case, sensitivity, net capacity and cash view |
| GET | `/api/analysis` | Queue model and capacity fit |
| GET / POST | `/api/rfqs` | Register with search, status, `limit`, `offset`, `X-Total-Count`; create |
| GET / PATCH | `/api/rfqs/{id}` | Read; update owner, due date, status |
| POST | `/api/rfqs/{id}/quote` | Calculate and save a versioned three-tier quote |
| GET | `/api/rfqs/{id}/quotes`, `/api/quotes/{id}` | Quote history and full snapshot |
| POST | `/api/quotes/{id}/decision`, `/api/quotes/{id}/send` | Approve or send back with reason; send an approved quote |
| GET | `/api/quotes/{id}/print` | Printable quote, HTML escaped |
| POST / GET | `/api/trace/import`, `/api/trace/summary` | Week-1 timestamp import (all or nothing), stage summary |
| GET | `/api/audit` | Audit events |

## 4. Identity and role gates

- Sign-in uses scrypt password hashes. Session tokens are random, stored only as SHA-256 hashes, and last 8 hours. Five failed sign-ins in 15 minutes lock the user. A wrong user and a wrong password give the same error.
- The role comes from the session on the server. Request bodies carry no role or actor, so a client cannot claim one.
- Estimator and Estimation Head: create RFQs, move work through permitted stages, calculate quotes. Only the Estimation Head imports a trace.
- Plant Head clears a routing review. Sales Head and Deputy approve or send back. Approved quotes can be sent by the estimators or the approvers.
- Demo credentials are generated lazily on the first service-backed API request into a gitignored file. Never commit them.

## 5. Local data storage

SQLite is used so the project can run with a small local setup. Schema changes are numbered migrations (v1 to v3) tracked in a `schema_version` table, and a v2.0 database upgrades in place. RFQ codes are allocated inside a `BEGIN IMMEDIATE` transaction. Money is stored as decimal text. The database is created at `application/data/marginladder.db` by default and is excluded from the source archive. Override it with the `MARGINLADDER_DB` environment variable. The seeded records are fictional and inserted only when the database has no RFQs.

## 6. Security and production gaps

Before any customer or company information is used, implement and test:

- Lockout is per username. Anyone who knows a username can lock that user out for 15 minutes. Acceptable on a laptop, not on a network. Add per-address limits and alerts.
- SSO and a managed identity provider. v3 has local sign-in only, with no password reset, no MFA and no per-customer tenancy.
- Server-enforced customer and plant tenancy, row-level authorisation and least privilege.
- HTTPS, secure secret management, CSRF protections where cookie auth is used, security headers and rate limiting.
- Encrypted file/object storage, malware scanning, access logging, retention and deletion controls for drawings.
- Database backups, restore drills, migrations, monitoring, alerting and operational ownership.
- ERP / rate-master source-of-truth and signed rate approval.
- A security review and privacy / NDA review before external exposure.

The current local MVP accepts no file uploads, has local sign-in only, does not call an AI model and does not connect to ERP / CRM. It should run only on a developer machine or a trusted local demo environment.
