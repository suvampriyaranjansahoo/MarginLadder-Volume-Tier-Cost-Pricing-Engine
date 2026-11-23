# Interview defence — five roles

All answers stay within the hypothetical case boundary.

## Project Manager
1. **What did you manage?** I prepared a 12-week delivery plan for a hypothetical RFQ workflow. I did not manage a live company project or team. The plan defines three gates, dependencies, roles, risks and status templates.
2. **What is the critical path?** Charter, process map, timestamp evidence, Gate 1, solution design, Gate 2, workflow build, security review, UAT, Gate 3, pilot and scale/stop decision. A delay in this chain moves the decision date.
3. **What is late today?** Nothing is reported late because no live project has started. In execution I compare actual finish to baseline, record downstream impact and ask the accountable owner for recovery or a change decision.
4. **Who owns delivery?** The RACI assigns one Accountable role per task. The sponsor owns gates and baseline decisions; the PM coordinates reporting. Real names and decision rights would need confirmation.
5. **What makes you stop?** Critical security or pricing defect, failed independent UAT, missing capacity, or economics below the agreed hurdle. The plan has explicit gates and rollback triggers.

## APM / PM
1. **Why workflow visibility first?** The brief gives a nine-day cycle but does not explain the stages. I would measure ownership and waiting before assuming a costing tool is the answer.
2. **Who validated the problem?** No real user has validated it. The journey is a hypothesis from the case brief. The action plan explains how I would run consent-based task sessions.
3. **How did you prioritise?** I used RICE: reach × impact × confidence ÷ effort. Scores are judgement inputs. The pack shows the rank can change if evidence proves costing is the dominant bottleneck.
4. **How will you know it worked?** Measure queue time, task completion, adoption and quote quality. Conversion needs mature outcomes and a comparison method. Faster quotes alone do not prove value.
5. **What would you cut?** AI drawing extraction, ERP write-back and customer portal. They add data, integration and access risk before the workflow and business case are proven.

## Consulting Analyst
1. **What is the recommendation?** Measure the RFQ flow and pilot reversible queue visibility before approving broad costing automation. A nine-day cycle is an outcome, not a diagnosis.
2. **How did you size the pool?** 720 annual RFQs × 5% assumed losses = 36 lost RFQs. Each average order contributes ₹2.4L at ₹20L AOV and 12% margin. The theoretical pool is ₹86.4L.
3. **How do you reach ₹21.6L?** Assume 25% effective win-back: 9 RFQs × ₹2.4L contribution = ₹21.6L. This is modelled, not realised.
4. **Why not build the full platform?** Queue, approval or customer holds may explain the residual cycle. Full integration is expensive and less reversible. A smaller pilot creates evidence first.
5. **What would change your mind?** A representative trace showing costing is >40% of working-time cycle, price parity passing, confirmed capacity and viable downside economics would support a costing screen. Price-led losses would remove the win-back benefit.

## Business Analyst
1. **How did you translate the problem into requirements?** I mapped the RFQ journey, defined business rules and linked requirements to tests and screens. Open and not-built items are marked.
2. **How do you prevent scope ambiguity?** Each requirement has an ID, acceptance test and status. Traceability shows whether proof is automated, demo-only or requires a business user.
3. **Technical test versus UAT?** A technical test checks code behaviour. UAT means a business user checks whether the workflow meets their work needs. Scripts exist; no business UAT is completed.
4. **How do you handle missing timestamps?** Do not treat missing values as zero. Report completeness, use agreed exclusions and separate customer holds. Overlapping stages must not be added as sequential time.
5. **What is still uncertain?** The exact business basis for the approval threshold and GST treatment requires a real process owner to confirm it.

## Finance Analyst
1. **Explain ₹86.4L.** 720 annual RFQs × 5% assumed losses = 36 lost RFQs. Each average order contributes ₹2.4L at ₹20L AOV and 12% margin. 36 × ₹2.4L = ₹86.4L theoretical pool.
2. **How do you reach ₹19.6L?** Assume 25% effective win-back, or 9 RFQs. Nine × ₹20L × 12% = ₹21.6L contribution. Less ₹2L run cost = ₹19.6L net operating contribution.
3. **Why 4.9 months and 23.6 months?** 4.9 months is simplified operating payback before tax and working capital. 23.6 months comes from the separate full cash model with tax and working-capital timing.
4. **Which input matters most?** Effective win-back and lost-RFQ rate move the answer most in sensitivity. They are not observed. Validate the denominator and incremental lift first.
5. **Are actuals real?** No. Actual cells are blank. The variance example is synthetic. A real analysis needs reconciled ledger or ERP data.
