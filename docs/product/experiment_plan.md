# MarginLadder pilot experiment and learning plan

## Hypothesis

A visible RFQ register, explicit ownership, deterministic costing and a controlled approval queue will reduce avoidable internal queue time and rework without increasing pricing errors, manufacturing exceptions or customer complaints.

This hypothesis has not yet been validated with a real client. The project brief supplies the 9-day current cycle and a 4-day target; the stage decomposition in the sample CSV is synthetic.

## Pilot design

### Phase 0 — Define the measurement system (Week 0)
- Agree what counts as an RFQ, an eligible quote, a lost RFQ and a customer-caused hold.
- Define the plant working calendar, stop-clock rules and reason codes.
- Identify 20 representative parts and obtain signed-off Excel calculations / rates for parity testing.
- Confirm plant capacity and commercial approval authority.

### Phase 1 — Baseline (Week 1)
- Trace at least 10 recent RFQs end-to-end; extend to 30–60 where source timestamps permit.
- Record touch time separately from intake, routing, approval and customer wait.
- Segment new vs repeat parts, number of parts, customer and complexity band.
- Publish median and P90 cycle time, missing-event rate and sample size.

### Phase 2 — Shadow mode (Weeks 2–3)
- Run MarginLadder alongside the approved Excel process.
- Do not send customer quotes from the prototype.
- Compare 20 agreed parts to the reference workbook, line by line, with ₹0.01 tolerance.
- Record input corrections, overrides, approval turnaround and usability issues.

### Phase 3 — Controlled operational pilot (Weeks 4–5)
- Roll out to a small estimator cohort only after access controls, data protection and UAT are signed off.
- Use a phased rollout or matched historical cohort; do not deliberately delay customer quotes to create a control group.
- Match on customer, part complexity, new/repeat status and part count where possible.
- Observe all quotes through final outcome; keep pricing and approval authority unchanged.

### Phase 4 — Decision (Week 6)
- Review the primary metric, quality guardrails, adoption and economics.
- Continue, revise, reduce scope or stop using pre-agreed gates.
- Do not claim causality from a small before/after sample; report confidence intervals or at least cohort sizes and distribution shifts when sufficient data exists.

## Metrics

**Primary:** median RFQ-to-quote working days, with P90 as a tail-risk companion.

**Secondary:** active costing hours per part, approval wait, first-pass quote rate, rework rate, on-time rate, adoption, eligible lost-RFQ share attributable to delay and recovered win rate.

**Guardrails:** cost parity, quote error rate, margin-floor compliance, plant capacity, quality rejection, unauthorised approvals, data access incidents and customer complaints.

## Decision rules

- Stop / do not expand if signed-off costing parity fails or any unauthorised quote is released.
- Pause if customer data is exposed, rate snapshots cannot reproduce an old quote, or material quality / manufacturing risk rises.
- Re-scope to the costing screen if measured hands-on costing exceeds 40% of total cycle time, consistent with the existing case hypothesis.
- Do not fund the full workflow solely on the 25% win-back assumption. Code reasons on at least 20 lost RFQs and validate with customer / sales interviews.
- Proceed only if the Plant Head confirms spare capacity for potential recovered orders.

## Research questions for user interviews

1. Walk through the last RFQ you quoted, from receipt to sending the offer.
2. Which step waited longest, and what timestamp or artefact proves it?
3. Which fields are re-entered from drawings, email or ERP?
4. What makes a part a repeat part, and how do you find comparable historical quotes?
5. What triggers plant review and Sales Head approval today?
6. What is the most common reason a customer does not proceed?
7. Which errors would make you reject an automated cost calculation?
8. What would make you trust or stop using this workflow?

## Reporting template

Every pilot readout should include: hypothesis, cohort dates, N, exclusions, baseline, intervention exposure, primary metric, P50/P90, guardrails, data completeness, user feedback, financial interpretation, caveats, decision and named owner for next action.
