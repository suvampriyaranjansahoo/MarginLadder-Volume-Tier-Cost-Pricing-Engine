# Product analytics: simulated event funnel and operator cohorts

> **Data: SIMULATED.** The event records are generated for method demonstration. They are not active users, adoption, conversion or retention outcomes from a live deployment.

RFQs created: **6**. Median created-to-sent time: **48.0 calendar hours**.

## RFQ lifecycle funnel

| Stage | RFQs | Conversion from created |
|---|---:|---:|
| rfq_created | 6 | 100.0% |
| quote_created | 6 | 100.0% |
| approval_requested | 2 | 33.3% |
| quote_approved | 2 | 33.3% |
| quote_sent | 5 | 83.3% |

## Weekly active operators

| ISO week | Active operators |
|---|---:|
| 2026-W41 | 4 |
| 2026-W42 | 4 |
| 2026-W43 | 4 |

## Cohort retention

| Cohort week | Week | Cohort operators | Active operators | Retention |
|---|---:|---:|---:|---:|
| 2026-W41 | 0 | 4 | 4 | 100.0% |
| 2026-W41 | 1 | 4 | 4 | 100.0% |
| 2026-W41 | 2 | 4 | 4 | 100.0% |

## Definitions and interpretation

- **Funnel:** Distinct RFQs with at least one event at each lifecycle milestone, divided by RFQs created.
- **Cycle:** Median elapsed hours from rfq_created to quote_sent; calendar hours, not working hours.
- **Weekly Active:** Distinct operators with any supported event in the ISO week.
- **Retention:** Operators grouped once by their first observed activity week; retained when they generate any event in a later ISO week.
- Funnel drop-off is descriptive in this synthetic sample; it does not establish causality.
- In a pilot, instrument server-side events with stable RFQ and operator identifiers, define consent/access controls, and use a pre-registered baseline before interpreting adoption.
