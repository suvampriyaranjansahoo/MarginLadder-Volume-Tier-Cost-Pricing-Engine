# MarginLadder — one-minute case brief

**Decision question:** Should a hypothetical Pune auto-components manufacturer fund a broad costing-system build to reduce RFQ turnaround from nine working days to four?

**Recommendation:** Do not approve the full build yet. Start with event-level measurement, clear queue ownership and a reversible RFQ visibility / approval workflow. Add deeper costing automation only if price-parity and stage-level data show that costing is a material bottleneck.

## What the case brief says

- 60 RFQs arrive each month; each RFQ covers five parts.
- Estimation currently takes 2.5 hours per part (12.5 hours per RFQ); the target is one hour per part.
- End-to-end cycle time is nine working days; the target is four.
- The case uses a 5% lost-RFQ rate, ₹20 lakh average order value and 12% contribution margin.

## What the arithmetic says

- 60 × 12 = 720 RFQs/year; 5% implies 36 lost RFQs.
- 36 × ₹20 lakh × 12% = ₹86.4 lakh theoretical lost-RFQ margin pool.
- At an assumed 25% win-back, recovered margin is ₹21.6 lakh/year; at 12.5%, it is ₹10.8 lakh.
- Including ₹2 lakh annual run cost, the modelled break-even win-back rate is 11.6%.
- The 12.5 hours of hands-on costing equate to 1.56 eight-hour working days. The remaining 7.44 days are a residual, not a proven waiting-time decomposition.

## What the work sample demonstrates

A deterministic costing engine, local RFQ workflow MVP, role-gated approvals, audit events, trace-to-SQL pipeline, finance model, monthly variance/planning work, business-analysis traceability, product requirements and analytics, and an executive recommendation deck.

## What remains unproven

There is no real manufacturer, production dataset, participant interview, business UAT sign-off, product usability result, pilot, measured cycle-time improvement or realised recovered margin. Simulated examples remain labelled as such. The app is a local demo.

## The decision-changing evidence

1. Complete timestamp pairs and reason codes for a representative RFQ sample.
2. Stakeholder confirmation of the actual failure points and decision rights.
3. Price parity across at least 20 representative part/volume cases before replacing the existing costing spreadsheet.
4. Plant capacity confirmation for recovered orders and executed role-based UAT.

**Bottom line:** the case recommends instrumenting the workflow and buying evidence before committing to broad automation. It is a business case and working prototype, not a success story about a real customer.
