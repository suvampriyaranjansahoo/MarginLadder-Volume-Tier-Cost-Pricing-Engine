# Product Finance model — decision method

## Driver tree
Annual RFQs = monthly RFQs × 12.
Lost RFQs = annual RFQs × loss rate.
Contribution pool = lost RFQs × average order value × contribution margin.
Recovered contribution = lost RFQs × assumed win-back × average order value × contribution margin.
Net contribution = recovered contribution − annual run cost.

## Adoption-adjusted economics
A more decision-useful model decomposes effective win-back:

`effective win-back = adoption rate × incremental win-back efficacy among adopted RFQs`

For example, 62.5% adoption × 40% efficacy = 25% effective win-back. This is a scenario illustration, not evidence. Test adoption and efficacy independently rather than treating a single 25% input as certain.

## Sensitivity to challenge
Stress adoption, efficacy, RFQ volume, loss rate, average order value, contribution margin, implementation cost, ramp delay, tax, working-capital days and terminal working-capital release. Report downside/base/upside as deterministic scenarios, not probability distributions unless a defensible distribution is available.

## Financial definitions
- Revenue: recovered order value.
- Contribution: revenue × contribution margin.
- Net contribution after run cost: contribution less annual run cost.
- Operating payback excludes tax and working capital.
- Cash payback includes cash timing, tax and working capital.
- Released estimator time is capacity, not cash saving.
- NPV/IRR are timing-sensitive; show IRR without working-capital release.

## Investment gates
Instrument the workflow; establish a baseline; verify pricing parity; pilot with a comparison; measure adoption and incremental outcomes; scale only if downside-case economics and capacity support it.

## Evidence limitations
All values are hypothetical case assumptions or derived arithmetic. The sample operational/product data is synthetic. There are no actuals, independent customer interviews, production usage or realised commercial outcomes.
