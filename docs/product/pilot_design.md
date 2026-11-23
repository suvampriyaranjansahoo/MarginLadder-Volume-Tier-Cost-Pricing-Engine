# Pilot design (pre-registered)

Written before any real data exists, so the decision rules cannot bend to fit the result. Status: **design only**. No pilot has run.
Evidence tags as elsewhere. Sample sizes come from `analytics/sample_size.py` and are tested.

## Question
Does the Early Release (register, clock, one-screen approval) get more RFQs to the customer within 4 working days, without more pricing errors?

## Hypotheses
| ID | Hypothesis | Metric (KPI dictionary) | Direction |
|---|---|---|---|
| H1 | Median time to quote falls. | Received to sent, working days | Down |
| H2 | More RFQs are sent within 4 working days. | Share sent within 4 days, with the sample size | Up |
| H3 | Mean approval wait stays within the budget. | Mean wait across all RFQs, days | At most 0.75 |
| H4 | Faster quoting reduces losses to delay. | Share of coded lost RFQs lost to delay | Down (leading indicator only) |

## Design
- **Baseline:** the Week 1 trace, at least 60 RFQs, real timestamps. [Judgement]
- **Pilot period:** at least 6 weeks after the Early Release is live, so about 90 RFQs at 60 a month. [Derived]
- **Comparison:** before versus after on the same customers. This is not randomised.
- **Guardrails:** pricing exceptions found by the Estimation Head, rework count per RFQ, and estimators' own view of effort. Customer-hold days are subtracted and reported separately.
- **Exclusions:** RFQs with no-bid or capacity rejection; the reason is recorded, not dropped.

## How many RFQs are enough
Two periods, a two-sided 5% test, 80% power, normal approximation.

RFQs needed **in each period** to detect a rise in the 4-day rate:

| Baseline rate [Assumption] | to 35% | to 50% | to 70% |
|---|---|---|---|
| 10% | 43 | 20 | 10 |
| 20% | 138 | 39 | 15 |
| 30% | 1377 | 93 | 24 |

Smallest rise detectable from a 10% baseline with a given number of RFQs in each period:

| RFQs per period | 30 | 60 | 90 | 180 |
|---|---|---|---|---|
| Detectable 4-day rate | 40.9% | 30.4% | 26.0% | 20.6% |

**Reading.** With about 90 RFQs a period the pilot can only prove a large change, from 10% to 26% or more. A smaller real gain will look like noise. That is why H1 (median time, which uses every RFQ) is the lead metric and H2 is the check. If the baseline is above 30%, the 4-day rate cannot be tested with this volume at all.

## Decision rules (fixed in advance)
| Result at the end of the pilot | Decision |
|---|---|
| H1 improves, H2 improves, H3 holds, no rise in pricing exceptions | Roll out to every RFQ and fund Release 2. Gate 3 has already decided the build. |
| H1 improves but H3 fails | Fix the approval rule first (trigger above 70%, deputy cover). Do not fund more features. |
| H1 flat, costing above 40% of the cycle | Cut scope to the costing screen and engine. |
| H1 flat, costing 40% or less | Stop. The delay is outside the tool: customers, routing or the plant. Find it before spending more. |
| Pricing exceptions rise | Stop and fix parity before any other work. |
| Fewer than 60 RFQs in the pilot | Extend the pilot. Do not decide. |

## Threats to the result
- **Season and mix.** A quiet month or easier parts can mimic a gain. Report customer mix beside every comparison.
- **Attention effect.** People move faster when watched. Keep measuring for 3 months after the pilot.
- **Definition drift.** Freeze the working-day rule (BR-23) and the start and stop events before the baseline starts.
- **Small numbers.** Report the sample size and the interval, never a bare average.
- **Win-back.** H4 cannot be proven in six weeks. Lost RFQs lag by months.
