# Change request log and impact analysis

The log is empty of real requests because there is no live project. The two entries below are **worked examples** that show how I would assess a change. They are not client requests.

## Template
| Field | Content |
|---|---|
| CR id and date | |
| Requested by | |
| What changes | |
| Why now | |
| Requirements and rules touched | |
| Code, data and documents touched | |
| Effort (person-days) and cost at the rate card | |
| Effect on the plan, gates and payments | |
| Risk and rollback | |
| Decision, by whom, date | |

## Worked example CR-001: add a fourth volume tier
| Field | Content |
|---|---|
| What changes | Quotes show four prices, adding 3,60,000 units a part. |
| Why now | A customer asks for a larger volume. |
| Touched | BR-08; US-04; AT-01 test set (20 parts × 4 tiers); `TIER_VOLUMES` in the engine; quote screen; PDF layout; data dictionary. |
| Effort | About 2 person-days to build and test. Parity must be re-run with the client's Excel on a fourth tier. |
| Plan effect | Uses part of the 0.5-day buffer if raised before Gate 2. After Gate 2 it is a paid change under the agreement. |
| Risk | The ₹25 lakh rule fires on every tier already, so approval volume does not change. Rollback is to hide the tier. |

## Worked example CR-002: test the ₹25 lakh rule on the GST-inclusive value
| Field | Content |
|---|---|
| What changes | BR-12 changes from value before GST to value with GST. |
| Why now | Company A's Sales Head says the rule has always used the invoice value. |
| Touched | BR-11, BR-12; `create_quote`; AT-05 boundary values; the 70% approval share and the 0.75-day approval budget. |
| Effort | Under 1 person-day for code. The approval share rises, so the budget in the PRD must be re-derived. |
| Plan effect | None on dates. The derived 70% trigger no longer holds: more quotes cross ₹25 lakh at the same price. |
| Risk | Approval wait rises. Check the new share against the 75% ceiling at which the budget cannot be met. |
