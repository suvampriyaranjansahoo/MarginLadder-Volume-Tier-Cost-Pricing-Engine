# Role positioning

**Primary story: Product Finance / Finance Analyst.** The project is one investment decision supported by four skill lenses. Do not pitch four unrelated products. Finance is the spine; BA, product and consulting artefacts explain how the decision is scoped, delivered and communicated.

# MarginLadder: role-specific portfolio positioning

This is one hypothetical business case, presented through four different professional lenses. The project is a local MVP and analytical case study; it has no client, production users, customer-validated outcomes or live pilot. Use only the evidence and wording below.

## Business Analyst

**Core story:** Translate an ambiguous RFQ-to-quote performance problem into traceable requirements, process controls and a testable workflow.

**Evidence to demonstrate:** AS-IS / TO-BE process maps; 26 documented business rules; seven use cases; 12 UAT scripts; requirements-to-test traceability; FastAPI workflow; role-controlled approvals; raw timestamp trace validation; missing-stage coverage reporting; direct trace-to-SQL analytics feed.

**Interview walkthrough:** Start with the business objective and stakeholder map. Show one workflow change, connect it to the business rule and acceptance criterion, then demonstrate the API or UI behaviour and the test covering it.

**Do not claim:** stakeholder sign-off, executed client UAT, reduced cycle time or production adoption. UAT scripts and automated acceptance tests are build evidence, not customer approval.

## Finance Analyst / Business Finance Analyst

**Core story:** Build a transparent investment case, challenge its assumptions, reconcile calculations and explain how operating changes affect contribution and cash.

**Evidence to demonstrate:** original Excel model; 64-cell Python reconciliation; cash flow, NPV, IRR, payback and working-capital sensitivity; queue and capacity model; Decimal-based monthly actual-versus-budget variance tool; revenue/cost favourability rules; contribution bridge; explicit treatment of zero-budget percentage variances.

**Interview walkthrough:** Separate brief inputs, derived arithmetic, assumptions and simulated values. Reconcile one key number to Excel, explain gross versus operating versus cash payback, then walk through an unfavourable cost variance and its operational drivers.

**Do not claim:** the sample monthly variance figures are actuals, contribution proxy is EBITDA, theoretical capacity release is booked savings, or the assumed recovered margin was realised.

## Consulting Analyst

**Core story:** Structure an operational problem, identify where the evidence is weak, quantify options and stage investment behind decision gates.

**Evidence to demonstrate:** issue tree; fact / assumption / judgement separation; cycle-time and capacity analysis; investment economics; downside case; options matrix; risk register; 30/60/90-day rollout; go/no-go recommendation and consulting-style case deck.

**Interview walkthrough:** Lead with the recommendation, then give the two or three supporting insights, state the main uncertainty and define the next test that would change the recommendation.

**Do not claim:** market research or competitive benchmarking is independently verified where the cited source is aggregator data, and do not represent synthetic stage data as an industry benchmark.

## Associate Product Manager

**Core story:** Convert an operational problem into a product bet, sequence features, instrument the funnel and define evidence-based release gates.

**Evidence to demonstrate:** PRD; personas labelled as assumptions; decision log; RICE sensitivity; roadmap and kill criteria; pilot design; event schema; distinct-RFQ funnel; weekly active operator and cohort-retention definitions; working RFQ and approval MVP.

**Interview walkthrough:** Explain why the first release exposes waiting rather than only accelerating costing. Show a prioritisation trade-off, then define the events and guardrails needed to judge a real pilot.

**Do not claim:** user discovery, adoption, retention or conversion improvements have occurred. Current product metrics run on a deliberately simulated event log.

## One-line positioning

“MarginLadder is a hypothetical RFQ-to-quote decision platform I built to connect process requirements, operational analytics, financial modelling and product delivery—with explicit controls separating verified build evidence from simulated business outcomes.”

## Role-specific artefacts

| Role | Lead with | Demonstrate next | Close with |
|---|---|---|---|
| Business Analyst | Process and requirement traceability | Rule → workflow → acceptance test | Open questions and UAT plan |
| Finance Analyst | Investment case and model audit | Reconciliation and variance bridge | Downside case and cash payback |
| Consulting Analyst | Executive recommendation | Issue tree and option economics | Decision gates and implementation plan |
| APM | Product bet and PRD | Prioritisation and event funnel | Pilot metrics and kill criteria |
