# MarginLadder consulting case deck — 13-slide map

**Audience:** CFO, Operations Head, Sales Head and product sponsor.  
**Case status:** Hypothetical case brief; no client, customer interviews or production data. All modelled figures retain their assumption labels in the exported deck.

| Slide | Headline / purpose | Decision-useful content |
|---:|---|---|
| 1 | Instrument the RFQ flow before funding automation | Executive recommendation and case boundary |
| 2 | A nine-day RFQ cycle is a process outcome—not yet a software diagnosis | Current / target cycle, monthly RFQ volume and target |
| 3 | Separate facts, derived arithmetic and open questions | Brief inputs, derived effort, unknowns and judgement |
| 4 | Structure the diagnosis around five possible sources of delay | Issue tree spanning intake, costing, approvals, customer delay and dispatch |
| 5 | The value pool is material—but the recovery rate is pivotal | ₹86.4 lakh theoretical lost-RFQ margin pool, ₹21.6 lakh base contribution case and 11.6% break-even win-back |
| 6 | Hands-on costing is not the same as elapsed cycle time | 1.56 working days of hands-on effort; 7.44-day residual remains undecomposed |
| 7 | Choose the smallest reversible option | Costing screen vs workflow visibility vs full integration |
| 8 | The MVP should improve control, not replace commercial judgement | Target operating flow, ownership, human approval and audit |
| 9 | Measure process performance and product adoption separately | Operational and product/control metrics, pilot thresholds and kill criteria |
| 10 | Operating payback is not cash payback | Setup / run cost, 4.9-month operating payback, 23.6-month cash payback and cash need |
| 11 | Industry growth is context; cost volatility keeps margin discipline central | ACMA FY25 and ICRA FY27 research, with non-comparable peer examples excluded from direct benchmarking |
| 12 | Approve the evidence sprint; make the larger investment conditional | Discovery, 10-RFQ trace, 20-case price-parity, business UAT and go/no-go gates |
| 13 | Sources and boundaries | Primary source links, hypothetical-case limitations and assumption disclosures |

## Recommendation and decision logic

**Recommendation:** authorise measurement and a limited, reversible workflow-visibility pilot. Do not approve a full costing-system build based only on the base-case win-back assumption.

The 9-working-day cycle minus 12.5 hours of hands-on costing (1.56 eight-hour working days) leaves a 7.44-day elapsed residual. That residual is not a measured stage split. The first intervention should expose handoffs, ownership, due dates, approval queues and exception reasons. Keep a costing screen as a fallback if trace evidence shows hands-on costing dominates the cycle; defer deep integration until process, capacity and price-parity gates pass.

The case model shows a theoretical ₹86.4 lakh annual lost-RFQ margin pool. The ₹21.6 lakh base recovered-contribution case assumes 25% win-back. The 11.6% break-even includes the first-year implementation and run-cost hurdle. Released estimator time is capacity, not cash savings. Operating payback and tax / working-capital cash payback are different measures.

## Evidence plan and decision gates

- Trace at least 10 recent RFQs with complete event pairs, consistent working-time rules and coded holds.
- Interview relevant practitioners using the last specific RFQ, not idealised process descriptions.
- Confirm the lost-RFQ denominator, contribution definition, capacity and delivery constraints.
- Test price parity across at least 20 representative part / volume cases.
- Execute business UAT against a frozen build and obtain accountable sign-off before any live pilot.

No timing or gate implies implementation at a real company. The fieldwork and UAT instruments are prepared, but execution is pending.

## Source discipline

Use `numbers.json`, `docs/finance/model_audit.md`, `docs/finance/capacity_and_queue.md`, `docs/validation/evidence_register.md` and `docs/product/pilot_design.md` for case evidence. External sector context is detailed in `docs/research/india_auto_components_context_2026.md` and `docs/portfolio/research_source_register.md`. External industry sources contextualise the decision; they do not validate the hypothetical firm's economics or the assumed RFQ problem.

---

## External sector context added for the presentation (reviewed 18 November 2026)

- ACMA reports FY25 Indian auto-component turnover of ₹6.73557 lakh crore, +9.6% YoY, with OEM supply of ₹5.70145 lakh crore.
- ICRA's 28 September 2026 FY27 outlook forecasts domestic OEM supply growth of 8–10% and aftermarket growth of 9–11%; it flags commodity, energy, freight and currency risk to margins.
- Primary annual-report examples from Samvardhana Motherson and Bharat Forge are retained as reading sources, not used as direct comparable multiples or SME target margins because their scale, segment mix, revenue definitions and consolidation perimeter differ.

See `docs/research/india_auto_components_context_2026.md` and `docs/portfolio/research_source_register.md` for the source-level limitations. The actual PowerPoint deliverable is `docs/consulting/MarginLadder_Executive_Recommendation.pptx`.
