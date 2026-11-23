-- MarginLadder cycle-time analysis in SQL (SQLite dialect).
-- Table cycle(rfq, intake, costing, routing, approval, send, total, customer_hold) holds working days per stage.
-- Data in this repo is SIMULATED (data/simulated_rfq_log.csv). The same queries run unchanged on the
-- real Week-1 trace once it is loaded into the same shape.

-- name: percentiles
-- Median and 90th percentile with linear interpolation (matches tracekit.analyze.percentile).
WITH ranked AS (
  SELECT total, ROW_NUMBER() OVER (ORDER BY total) AS rn, COUNT(*) OVER () AS n FROM cycle
), pos AS (
  SELECT q.label, q.p, (SELECT n FROM ranked LIMIT 1) AS n FROM (SELECT 'median' AS label, 0.5 AS p UNION ALL SELECT 'p90', 0.9) q
), pick AS (
  SELECT label, p, n, 1 + (n - 1) * p AS position, CAST(1 + (n - 1) * p AS INTEGER) AS lo FROM pos
)
SELECT pick.label,
       ROUND(lo_row.total + (pick.position - pick.lo) * COALESCE(hi_row.total - lo_row.total, 0), 2) AS days
FROM pick
JOIN ranked lo_row ON lo_row.rn = pick.lo
LEFT JOIN ranked hi_row ON hi_row.rn = pick.lo + 1
ORDER BY pick.p;

-- name: stage_share
-- Share of total elapsed time by stage.
SELECT stage, ROUND(SUM(days), 1) AS days, ROUND(100.0 * SUM(days) / (SELECT SUM(total) FROM cycle), 1) AS pct_of_cycle
FROM (
  SELECT 'Intake wait' AS stage, intake AS days FROM cycle UNION ALL
  SELECT 'Costing', costing FROM cycle UNION ALL
  SELECT 'Routing wait', routing FROM cycle UNION ALL
  SELECT 'Approval wait', approval FROM cycle UNION ALL
  SELECT 'Send and rework', send FROM cycle)
GROUP BY stage ORDER BY pct_of_cycle DESC;

-- name: largest_stage_per_rfq
-- For each RFQ, which stage took longest? Counts how often each stage is the single biggest delay.
WITH long AS (
  SELECT rfq, 'Intake wait' AS stage, intake AS days FROM cycle UNION ALL
  SELECT rfq, 'Costing', costing FROM cycle UNION ALL
  SELECT rfq, 'Routing wait', routing FROM cycle UNION ALL
  SELECT rfq, 'Approval wait', approval FROM cycle UNION ALL
  SELECT rfq, 'Send and rework', send FROM cycle
), ranked AS (
  SELECT rfq, stage, days, RANK() OVER (PARTITION BY rfq ORDER BY days DESC) AS r FROM long
)
SELECT stage, COUNT(*) AS rfqs_where_largest FROM ranked WHERE r = 1 GROUP BY stage ORDER BY rfqs_where_largest DESC, stage;

-- name: variance_drivers
-- Which stage explains the spread of total time? Cov(stage, total) / Var(total); the five shares add to 100%.
WITH m AS (
  SELECT AVG(intake) ai, AVG(costing) ac, AVG(routing) ar, AVG(approval) ap, AVG(send) asd, AVG(total) at FROM cycle
), v AS (
  SELECT AVG((total - m.at) * (total - m.at)) AS var_total,
         AVG((intake - m.ai) * (total - m.at)) AS c_intake,
         AVG((costing - m.ac) * (total - m.at)) AS c_costing,
         AVG((routing - m.ar) * (total - m.at)) AS c_routing,
         AVG((approval - m.ap) * (total - m.at)) AS c_approval,
         AVG((send - m.asd) * (total - m.at)) AS c_send
  FROM cycle, m
)
SELECT 'Intake wait' AS stage, ROUND(100 * c_intake / var_total, 1) AS pct_of_variance FROM v UNION ALL
SELECT 'Costing', ROUND(100 * c_costing / var_total, 1) FROM v UNION ALL
SELECT 'Routing wait', ROUND(100 * c_routing / var_total, 1) FROM v UNION ALL
SELECT 'Approval wait', ROUND(100 * c_approval / var_total, 1) FROM v UNION ALL
SELECT 'Send and rework', ROUND(100 * c_send / var_total, 1) FROM v
ORDER BY pct_of_variance DESC;

-- name: aging_buckets
SELECT CASE WHEN total <= 4 THEN '1. within 4 days (target)'
            WHEN total <= 7 THEN '2. over 4 to 7 days'
            WHEN total <= 10 THEN '3. over 7 to 10 days'
            ELSE '4. over 10 days' END AS bucket,
       COUNT(*) AS rfqs,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM cycle), 1) AS pct,
       ROUND(100.0 * SUM(COUNT(*)) OVER (ORDER BY MIN(total)) / (SELECT COUNT(*) FROM cycle), 1) AS cumulative_pct
FROM cycle GROUP BY 1 ORDER BY 1;

-- name: costing_over_40pct
-- Week-1 rule: if costing is more than 40% of the cycle, cut scope to costing only. How many RFQs breach it?
SELECT COUNT(*) AS rfqs_costing_over_40pct,
       (SELECT COUNT(*) FROM cycle) AS rfqs,
       (SELECT ROUND(100.0 * SUM(costing) / SUM(total), 1) FROM cycle) AS costing_share_of_total_pct
FROM cycle WHERE costing > 0.4 * total;

-- name: what_if
-- Scenario table on the same RFQs. Rules are ASSUMPTIONS, not forecasts.
-- A: costing time falls to 40% (1 h from 2.5 h a part).
-- B: A, and approval wait is capped at 0.75 day (the PRD budget).
-- C: B, and intake and routing waits are capped at 0.5 day each (register, clock and routing rule).
WITH s AS (
  SELECT 'Today (simulated)' AS scenario, 0 AS ord, total AS t FROM cycle UNION ALL
  SELECT 'A: costing at 1 h a part', 1, total - costing * 0.6 FROM cycle UNION ALL
  SELECT 'B: A + approval capped at 0.75 day', 2, total - costing * 0.6 - MAX(approval - 0.75, 0) FROM cycle UNION ALL
  SELECT 'C: B + intake and routing capped at 0.5 day', 3,
         total - costing * 0.6 - MAX(approval - 0.75, 0) - MAX(intake - 0.5, 0) - MAX(routing - 0.5, 0) FROM cycle
)
SELECT scenario, ROUND(AVG(t), 2) AS mean_days, SUM(t <= 4) AS within_4_days, COUNT(*) AS rfqs,
       ROUND(100.0 * SUM(t <= 4) / COUNT(*), 1) AS pct_within_4
FROM s GROUP BY scenario, ord ORDER BY ord;


-- name: customer_hold_overlay
-- Customer holds are stored separately and are not added to the stage stack: they may
-- overlap the residual elapsed interval. They are a diagnostic overlay, not another stage.
SELECT ROUND(AVG(customer_hold), 2) AS mean_customer_hold_days,
       SUM(customer_hold > 0) AS rfqs_with_customer_hold,
       COUNT(*) AS completed_rfqs,
       ROUND(100.0 * SUM(customer_hold > 0) / COUNT(*), 1) AS pct_with_customer_hold
FROM cycle;
