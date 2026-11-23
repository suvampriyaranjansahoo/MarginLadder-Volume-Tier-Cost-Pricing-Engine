# Raw trace to SQL analytics: data lineage

`analytics.run_queries` accepts either the existing seven-column cycle-time CSV or the raw event timestamp schema in `tracekit/rfq_trace_template.csv`. For raw traces it performs these transformations:

1. Parse ISO-8601 timestamps and preserve offset semantics. Naive timestamps are treated as local wall-clock times; offset-aware timestamps are compared as instants in the `received_at` timezone. Mixing naive and aware values in one RFQ is rejected.
2. Exclude unsent RFQs from completed-cycle analysis. They remain visible in the trace tool's missing-sent rate.
3. Require complete received/assigned, assigned/costing-start and costing-start/costing-end pairs. Routing and approval are optional only when both timestamps for that stage are absent. Incomplete pairs are rejected, not converted to zero.
4. Aggregate intake wait and queue-before-costing into the SQL `intake` field; carry costing, routing and approval separately; calculate `send` as the residual of total elapsed time after measured stages.
5. Store `customer_hold_days` as a separate non-additive overlay. It may overlap the residual stage and must not be summed into the stage stack.

Run the transformation and SQL analysis:

```bash
python -m analytics.run_queries tracekit/rfq_trace_template.csv
```

The command writes `docs/analytics/sql_findings.md`. The example template contains only two illustrative rows and is not a valid operational baseline. Replace it with a de-identified, reconciled Week-1 trace before drawing business conclusions.
