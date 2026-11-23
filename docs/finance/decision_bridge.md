# Financial decision bridge — assumptions to recommendation

## Decision
Do not commit to a full automation rollout from the modelled upside alone. Fund a limited measurement and workflow pilot first, with explicit stop/go gates.

## Base-case bridge
- 60 RFQs/month × 12 = 720 annual RFQs.
- At a 5% assumed loss rate: 36 lost RFQs/year.
- At ₹20 lakh average order value and 12% contribution margin: ₹2.4 lakh contribution per RFQ and ₹86.4 lakh annual lost-RFQ contribution pool.
- At an assumed 25% recoverable share: ₹21.6 lakh modelled incremental contribution.
- Less ₹2.0 lakh annual run cost: ₹19.6 lakh annual net contribution before tax and working capital.
- ₹8.0 lakh implementation fee / ₹19.6 lakh annual net contribution × 12 = approximately 4.9 months operating payback.

## Why this is not yet an investment approval
The 25% win-back rate, 5% loss rate, average order value, margin and costs are case assumptions. The lost-RFQ pool is an opportunity ceiling, not a forecast. The model does not prove that RFQ workflow changes cause wins. Released estimator capacity is not cash saving unless headcount, overtime or external spend changes.

## Pilot gates
1. Instrument RFQ received, assigned, costing started/completed, approval requested/approved, quote sent and outcome timestamps.
2. Capture loss reason, quote revision count, pricing exception, product family and order contribution with appropriate permissions.
3. Establish a baseline and data completeness threshold before intervention.
4. Pilot queue visibility and approval workflow with a bounded cohort; compare cycle-time distribution, rework, quote error and conversion against a comparable baseline.
5. Expand automation only if observed bottleneck evidence and incremental contribution exceed implementation and run costs under a downside case.

## Financial controls
- Keep assumptions in the input sheet; avoid hard-coded overrides in output formulas.
- Separate revenue, gross contribution, operating cost, cash flow and working capital.
- Label operating payback separately from cash payback.
- Show downside/base/upside and break-even win-back.
- Record source, owner, date and confidence for each input before treating it as observed.
