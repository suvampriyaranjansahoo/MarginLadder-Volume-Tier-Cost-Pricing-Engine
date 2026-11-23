# Consulting challenge pack

**Purpose:** make the recommendation testable under a hostile review.  
**Reader:** consulting interviewer, sponsor, finance lead.  
**Recruiter conclusion:** the problem is structured, options are compared and decision-changing evidence is pre-defined.  
**30-second explanation:** “The brief gives a nine-day cycle, not its cause. I would measure the process and pilot reversible queue visibility before committing to a full costing platform.”

## MECE issue tree (MECE = non-overlapping and collectively complete)
**Question:** what intervention, if any, improves profitable RFQ response?
1. Demand and intake
   - RFQ volume and completeness
   - customer clarification / hold
2. Work execution
   - estimator active work
   - rework and missing information
3. Internal waiting
   - assignment queue
   - approval queue
4. Commercial outcome
   - price competitiveness
   - product fit and capacity
   - lead-time promise
5. Economics and feasibility
   - contribution margin and mix
   - implementation and run cost
   - cash timing and working capital

Hypotheses: queue visibility may reduce internal waiting; costing automation may reduce active work only if costing is the dominant bottleneck; neither will fix price-led losses or unavailable capacity.

## Top-down sizing
Brief inputs: 60 RFQs/month × 12 = 720 annual RFQs. At a 5% assumed loss rate, 36 are lost. At ₹20L AOV × 12% contribution = ₹2.4L contribution per average order. The theoretical lost-RFQ contribution pool is 36 × ₹2.4L = **₹86.4L**.

At an assumed 25% effective win-back, 9 RFQs are recovered and modelled contribution is 9 × ₹2.4L = **₹21.6L**. Less ₹2L annual run cost gives **₹19.6L net operating contribution**, before tax and working capital.

## Bottom-up sizing and gap
A bottom-up case would sum eligible RFQs by customer/product, verified loss reason, actual contribution per product, operator capacity, and measured incremental conversion. Those inputs do not exist in this hypothetical case. Therefore a credible bottom-up number cannot be calculated. The gap between ₹86.4L top-down pool and any bottom-up estimate is **not zero**; it is currently unmeasured. Do not present the theoretical pool as addressable revenue.

## Options table
Weights are analyst judgement. Scores are 1 (weak) to 5 (strong). Higher is better. The scorecard is a decision aid, not a measured preference study.

| Option | Evidence speed 25% | Reversibility 20% | Control 20% | Potential benefit 20% | Delivery risk 15% | Weighted |
|---|---:|---:|---:|---:|---:|---:|
| Queue/register visibility | 5 | 5 | 5 | 3 | 4 | 4.45 |
| Process redesign only | 4 | 5 | 3 | 2 | 5 | 3.75 |
| Dedicated costing screen | 3 | 4 | 4 | 4 | 3 | 3.60 |
| Full integrated platform | 1 | 1 | 3 | 5 | 1 | 2.20 |

**Numerical weight sensitivity (same 1–5 option scores; only weights change):**

| Option | Base weights: 25/20/20/20/15 | Benefit-heavy: 10/10/10/60/10 |
|---|---:|---:|
| Queue/register visibility | 4.45 | 3.70 |
| Process redesign only | 3.75 | 2.90 |
| Dedicated costing screen | 3.60 | **3.80** |
| Full integrated platform | 2.20 | 3.60 |

The benefit-heavy weights are evidence speed 10%, reversibility 10%, control 10%, potential benefit 60%, delivery risk 10%. Under that deliberately benefit-dominant weighting, the costing screen moves from third to first. This is a **rank-flip stress test**, not proof that costing is the bottleneck. The rank changes because the weight assigned to potential benefit changes; the underlying scores remain analyst judgement. Before sponsor approval, replace judgement scores with evidence from stage-time observations, feasibility and validated economics. The slide 16 sensitivity uses these same values.

## Recommendation
Do not approve a broad automation rollout. First instrument RFQ stage timestamps, rework, quote accuracy and loss reasons. Pilot a reversible queue-visibility and approval workflow. Expand costing automation only if representative evidence shows active costing is a material bottleneck and price/capacity guardrails pass.

## Red-team: three strongest counter-arguments
1. **“The 25% win-back is made up.”** Correct. It is an assumption. Remove the benefit from any committed case until a valid comparison supports incremental lift.
2. **“A register adds admin work.”** Correct risk. Measure task time and completion; stop if work increases without a queue-time improvement.
3. **“Faster quotes may be unprofitable or impossible to fulfil.”** Correct risk. Require contribution floor, price parity and confirmed capacity before quote release.

## What would change my mind — five observable facts
1. If a representative complete sample shows active costing is >40% of working-time cycle, prioritise a costing screen.
2. If approval waiting is the largest avoidable stage, prioritise approval queue and delegated authority controls.
3. If customer holds dominate elapsed time, prioritise intake/clarification, not workflow automation.
4. If losses are mainly price, product or lead-time related, remove the win-back benefit from the business case.
5. If plant capacity or contribution floors fail, stop scale and retain only standalone controls with proven value.

## Sizing caveat
No external market-size number is used to justify this single-company investment case. Industry context must not be confused with the manufacturer's RFQ opportunity. External industry numbers are listed separately in `docs/portfolio/research_source_register.md`. The ACMA FY25 release reports sector turnover of ₹6.73 lakh crore and 9.6% year-on-year growth; this is context only, not a company forecast. See ACMA's FY25 press release: https://www.acma.in/uploads/press-release/Press%20Release%20FY25.pdf.
