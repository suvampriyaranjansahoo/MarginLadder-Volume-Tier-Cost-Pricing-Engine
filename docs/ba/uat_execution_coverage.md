# UAT execution coverage and evidence boundary

**Status:** Automated technical acceptance tests are executed in this repository. Business UAT by customer stakeholders has **not** been executed. This document must not be used as a customer sign-off record.

| Business acceptance area | Available automated coverage | Remaining business UAT |
|---|---|---|
| Create and retrieve an RFQ | API tests cover validation, creation and retrieval | Confirm field names and mandatory fields with sales / estimation users |
| Assign and transition workflow status | Service/API tests cover allowed transitions and role controls | Observe real hand-offs and exception paths |
| Cost and snapshot a quote | Quote tests cover calculation and version snapshots | Run price parity on at least 20 signed-off sample parts |
| Require and record approval | Tests cover threshold and role-gated decisions | Confirm approval limit, delegation and approval SLA with finance / plant heads |
| Audit actions | Tests cover event creation and actor/role provenance | Agree audit retention and review ownership |
| Import RFQ trace | Tests cover input validation, idempotency and summary behaviour | Reconcile trace rows with source records and resolve missing timestamps |
| Cycle-time calculations | Unit tests cover timezone handling, weekends, holidays, coverage and percentiles | Confirm plant calendar, shift calendar and hold coding |

## How to execute business UAT

1. Select representative RFQs and approved test parts; remove customer-identifying data before loading.
2. Have each business role execute the 12 scenarios in `uat_scripts.md` using a controlled test database.
3. Capture tester, date, build version, test data reference, expected result, actual result, evidence link and severity for every case.
4. Log defects with owner and retest result; do not mark a scenario passed based only on an automated unit test.
5. Obtain named business sign-off only after the customer or designated process owner has reviewed the evidence.

**Current result:** automated tests run locally/CI; business UAT is pending. No stakeholder sign-off is claimed.
