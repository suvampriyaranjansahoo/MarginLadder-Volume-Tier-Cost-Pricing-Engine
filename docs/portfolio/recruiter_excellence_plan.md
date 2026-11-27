# Recruiter evidence plan: MarginLadder

## Purpose and claim boundary

This page maps portfolio evidence to the roles MarginLadder targets. It is not a claim of production delivery or user adoption. The workflow application is local; application records and operational data are synthetic unless they are explicitly labelled public benchmark data.

## Shared review path (all roles)

1. Run the local application and sign in with a demo account.
2. Use the **Forging economics simulator** to change steel price, yield, cycle time, energy, utilisation and working-capital days.
3. Review the **Bharat Forge FY26 public-data benchmark** and its stated limits.
4. Inspect the RFQ workflow, quote snapshot and audit trail.
5. Follow the appropriate role path below.

The deliberate design principle is traceability: public ranges, synthetic demo records, assumptions and calculated values are separate states. A recruiter should be able to identify which is which in the interface and the documentation.

## Product Finance Analyst

**Question answered:** Is the workflow investment financially justified under base and downside assumptions?

1. Open `model/MarginLadder_Monthly_FP&A_Model.xlsx` and inspect Inputs, Monthly Plan, Tornado and Audit Checks.
2. Compare operating payback with the cash view; do not treat the former as cash payback.
3. Use the simulator to stress working capital and material price, then compare the result with `docs/finance/real_company_benchmark.md`.
4. Read `docs/portfolio/Investment_Memo.md` and `docs/finance/decision_bridge.md`.

**Evidence:** driver model, reconciliation, scenario analysis, cash discipline and explicit investment gates.

## Finance Analyst

**Question answered:** Can the analyst create a reproducible operating plan, explain variance and protect model integrity?

1. Run `python -m finance.reconcile`.
2. Review `data/finance_actual_vs_budget_sample.csv` and `docs/finance/monthly_variance_analysis.md`.
3. Trace a dashboard metric to `finance/case_model.py` or `finance/forging_scenarios.py`.
4. Review the documented actual-versus-budget boundary: sample values are not actual company results.

**Evidence:** reproducible calculations, variance framework, source boundaries and audit checks.

## Business Analyst

**Question answered:** Can the analyst turn an operational problem into controls, requirements and testable delivery work?

1. Compare `docs/ba/swimlane_as_is.png` and `docs/ba/swimlane_to_be.png`.
2. Read `docs/ba/user_stories.md`, `docs/ba/business_rules.md` and `docs/requirements_traceability_v3.md`.
3. In the app, create an RFQ, cost it, apply the approval threshold and inspect its audit events.
4. Review `docs/ba/uat_scripts.md` and `docs/validation/ui_workflow_check.md`.

**Evidence:** process mapping, acceptance criteria, business rules, traceability and controlled workflow evidence.

## Associate Product Manager

**Question answered:** Can the APM make disciplined scope, metric and roadmap decisions under uncertainty?

1. Read `docs/product/PRD_v3.md` and `docs/product/decision_log.md`.
2. Review `docs/product/prioritisation_matrix.md`, `docs/product/rice_sensitivity.md` and `docs/product/roadmap.md`.
3. Use the dashboard to identify the primary metric: quote turnaround, while checking approval compliance and margin-floor guardrails.
4. Read `docs/product/experiment_plan.md` and `docs/product/pilot_design.md`; note that these are proposed validation designs, not executed research.

**Evidence:** problem framing, non-goals, prioritisation trade-offs, metric discipline, pilot design and accountable product decisions.

## Consulting Analyst

**Question answered:** Can the analyst diagnose a commercial problem, size the range of impact and recommend a staged response?

1. Read `docs/consulting/case_deck.md` and `docs/go_no_go_memo.md`.
2. Compare the workflow-visibility pilot against broad costing automation using the decision layer and simulator.
3. Use the Bharat Forge reference only as a public range check, then state the limits.
4. Review `docs/strategy/rollout_30_60_90.md` for the implementation recommendation.

**Evidence:** issue-led thinking, alternative evaluation, quantified decision support and a sequenced recommendation.

## Project / Programme Manager

**Question answered:** Can the manager deliver a controlled pilot with clear owners, dependencies and escalation paths?

1. Review `docs/pm/schedule_and_critical_path.md` and `docs/pm/gantt_12_week.png`.
2. Inspect `docs/pm/raci_tasks.md`, `docs/pm/raid_log.md` and `docs/pm/change_control_and_communications.md`.
3. Tie pilot milestones to the product gates in `docs/product/roadmap.md`.
4. Use `docs/pm/status_reports_templates.md` to communicate on-track and at-risk work.

**Evidence:** scope control, ownership, dependency management, governance and stakeholder communication.

## Evaluation rubric

| Criterion | Strong evidence in this repository |
|---|---|
| Domain context | Synthetic forging and machining scenarios plus a labelled public FY26 benchmark |
| Decision quality | A recommendation that distinguishes pilot from scale and identifies evidence needed |
| Analytical rigour | Decimal calculations, tests, reconciliations and documented sensitivity |
| Product judgement | PRD, non-goals, RICE trade-offs, metric tree and pilot/kill criteria |
| Delivery discipline | Requirements, UAT design, audit events, RACI, RAID and delivery plan |
| Credibility | Clear separation of public data, synthetic data, assumptions and derived results |

## Remaining validation needed

The strongest next evidence is still real discovery and timestamp data: interview three to five estimators, sales or finance users; obtain signed rate ownership; and import an observed RFQ trace. Until then, the project demonstrates a built MVP and decision-quality artefacts, not adoption or realised business benefit.
