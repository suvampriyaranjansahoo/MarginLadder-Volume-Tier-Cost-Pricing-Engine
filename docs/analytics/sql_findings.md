# SQL findings: cycle-time analysis

> **Data: SIMULATED** (`data/simulated_rfq_log.csv`, 60 rows from assumed stage means). Nothing here is a finding about a real plant. The queries in `analytics/queries.sql` run unchanged on the Week-1 trace.

Regenerate with `python3 -m analytics.run_queries`. Each reading below is written from the query output.
For a raw Week-1 trace, pass the timestamp CSV directly; unsent RFQs are excluded from cycle-time SQL and incomplete stage pairs are rejected. Customer holds are an overlay, not an additive stage.

## Median and 90th percentile

| label | days |
|---|---|
| median | 8.7 |
| p90 | 12.31 |

**Reading.** Median 8.7 days and 90th percentile 12.31 days, against a 4-day target. Report both: the average hides the long tail.

## Where the days go

| stage | days | pct_of_cycle |
|---|---|---|
| Approval wait | 144.0 | 26.7 |
| Routing wait | 114.0 | 21.1 |
| Send and rework | 98.4 | 18.2 |
| Costing | 93.6 | 17.3 |
| Intake wait | 90.0 | 16.7 |

**Reading.** Approval wait is the largest block at 26.7% of elapsed time. Timestamp-derived costing is 17.3%; the brief-only hands-on arithmetic is about 17.3% of a 9-day cycle (1.56 of 9 days), so compare only after checking trace completeness and definitions.

## Longest stage per RFQ

| stage | rfqs_where_largest |
|---|---|
| Approval wait | 26 |
| Routing wait | 14 |
| Costing | 9 |
| Intake wait | 6 |
| Send and rework | 5 |

**Reading.** Approval wait is the single longest stage on 26 of 60 RFQs. No one stage is the longest everywhere, so one fix will not close the gap.

## What drives the spread

| stage | pct_of_variance |
|---|---|
| Approval wait | 37.5 |
| Send and rework | 25.7 |
| Costing | 17.3 |
| Routing wait | 10.3 |
| Intake wait | 9.2 |

**Reading.** Approval wait explains 37.5% of why some RFQs take far longer than others. Costing explains 17.3%. Fixing the stage that drives the spread matters more than fixing the average.

## Ageing buckets

| bucket | rfqs | pct | cumulative_pct |
|---|---|---|---|
| 2. over 4 to 7 days | 9 | 15.0 | 15.0 |
| 3. over 7 to 10 days | 34 | 56.7 | 71.7 |
| 4. over 10 days | 17 | 28.3 | 100.0 |

**Reading.** 0 of 60 RFQs meet the 4-day target today. 17 take more than 10 days.

## The 40% costing rule

| rfqs_costing_over_40pct | rfqs | costing_share_of_total_pct |
|---|---|---|
| 1 | 60 | 17.3 |

**Reading.** Costing is above 40% of the cycle on 1 of 60 RFQs. Across all RFQs it is 17.3% of total time, so the cut-scope rule does not trigger on this data.

## What if: three assumed changes

| scenario | mean_days | within_4_days | rfqs | pct_within_4 |
|---|---|---|---|---|
| Today (simulated) | 9.0 | 0 | 60 | 0.0 |
| A: costing at 1 h a part | 8.06 | 0 | 60 | 0.0 |
| B: A + approval capped at 0.75 day | 6.41 | 0 | 60 | 0.0 |
| C: B + intake and routing capped at 0.5 day | 4.01 | 36 | 60 | 60.0 |

**Reading.** The 4-day rate goes 0.0% today, 0.0% with faster costing (A), 0.0% with the approval cap added (B), 60.0% with intake and routing caps added (C). Faster costing alone does not reach the target; the waiting stages have to shrink too. I chose the caps, so this shows what has to be true for the target to be met, not that it will be.

## Customer holds (separate overlay)

| mean_customer_hold_days | rfqs_with_customer_hold | completed_rfqs | pct_with_customer_hold |
|---|---|---|---|
| 0.0 | 0 | 60 | 0.0 |

**Reading.** Customer hold averages 0.0 days per completed RFQ and is present on 0 of 60. It is a non-additive overlay; do not add it to the stage stack because it may overlap residual elapsed time.
