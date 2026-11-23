# Simulated UAT defect fix — v3.4.2

## Finding
A simulated estimator workflow showed that an existing RFQ could be edited to use a due date in the past, although RFQ creation already rejected past due dates.

## Resolution
- Enforced the same `due_date >= today` rule in the service-layer update path.
- Kept the check server-side so API callers cannot bypass it.
- Added a `min` date to the browser assignment editor as a usability aid.
- Added service and API regression tests. Both verify that a rejected edit leaves the stored due date unchanged.

## Verification
- Full pytest suite: passed.
- Finance reconciliation: 64/64 matched.
- Monthly workbook validation: passed (439 formulas).
- Consistency checks: 654/654 passed.
- Portfolio release audit: 26/26 passed.

## Evidence boundary
This is a simulated, developer-run workflow test. It is not independent external UAT, customer validation, or stakeholder sign-off.
