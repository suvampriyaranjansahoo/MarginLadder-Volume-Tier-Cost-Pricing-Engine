# Go / no-go decision memo: RFQ workflow and costing investment

**Recommendation: fund a capped, measurement-led and reversible pilot. Do not approve broad costing-app rollout yet.** This is a conditional recommendation for a hypothetical case, not an investment approval for a real company.

## Why this is the correct decision now

The brief supplies 60 RFQs per month, a 5% lost-RFQ rate, ₹20 lakh average order value, 12% contribution margin, a 9-day current cycle and a 4-day target. These imply 720 RFQs/year, 36 assumed lost RFQs and an ₹86.4 lakh theoretical lost-RFQ contribution pool. They do **not** establish why RFQs are lost or which process stage causes delay.

The break-even effective win-back is 11.6% including annual run cost (9.3% before run cost). The 25% effective win-back scenario is decomposed as 62.5% adoption × 40% incremental lift among adopted eligible RFQs. Both are explicit assumptions. The resulting ₹21.6 lakh is modelled incremental contribution before programme costs, not realised revenue or contribution. Estimator capacity released is not cash savings.

The existing operating proxy estimates 4.9 months payback before tax and working capital. The separate cash model estimates 23.6 months under its tax and working-capital assumptions. These are different measures and must not be interchanged.

## Approve now: evidence sprint and reversible workflow pilot

1. Obtain a de-identified timestamp trace for at least 10 recent RFQs, including event, actor, reason code and data-completeness status.
2. Conduct role-based discovery with estimators, RFQ owners, sales, finance controllers and approval managers. Record only sessions that actually occur; no findings are presumed in this case.
3. Test price parity on at least 20 representative part/volume combinations against an independently approved costing reference.
4. Pilot owner, status, due-date and exception visibility without replacing the existing commercial approval authority.
5. Execute business UAT with named participants, actual results, defect IDs, retests and sign-off. The existing UAT scripts are design artefacts, not completed UAT.

## Release gates for broader investment

Proceed only if all conditions hold:

- Timestamp completeness and chronology are sufficient to identify the dominant bottleneck.
- The selected intervention addresses that bottleneck; if costing dominates, scope a costing-only release.
- Price parity meets a tolerance agreed by the finance and commercial owners before testing.
- No critical/high permission, approval or audit defect remains.
- Plant capacity can fulfil incremental demand without displacing higher-contribution orders.
- A business owner accepts the workflow and measurement protocol.
- Downside economics remain within an explicitly approved investment and cash-funding cap.

If evidence is incomplete, **defer**. If validated economics are structurally negative, **reject**. If gates pass and the downside case remains acceptable, **invest in the next stage**.

## Evidence boundary

No customer interviews, production deployment, signed UAT, realised win-back, measured cycle-time improvement, vendor quote or customer financial result is claimed. These require genuine participants, company data, commercial quotations and business sign-off.
