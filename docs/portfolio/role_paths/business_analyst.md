# Business Analyst path — MarginLadder

## Recruiter takeaway

A connected BA work sample linking the business problem, rules, use cases, process, requirements, delivery scope, traceability and a 12-scenario UAT design. It demonstrates the artefacts and technical traceability; no stakeholder elicitation or business sign-off is claimed.

## 5-minute inspection route

1. Open `docs/ba/business_rules.md`, `docs/ba/use_cases.md` and `docs/requirements_traceability_v3.md`.
2. Inspect AS-IS / TO-BE diagrams and `docs/ba/data_dictionary.md`.
3. Read `docs/ba/discovery_and_uat_execution_pack.md` and the UAT scripts.
4. Review `application/` and the test report to distinguish technical tests from business acceptance.

## Demonstrated competencies

- Current-state and future-state process framing.
- Business rules, stakeholder roles, use cases and user stories.
- Functional and operational requirements with traceability.
- Acceptance criteria and a structured UAT scenario set.
- Data definitions, missingness, timezone and cycle-time handling.
- Change-impact and defect-severity conventions.

## 60-second walkthrough

“I took the RFQ-to-quote case from a broad nine-day cycle-time goal into a requirements and control problem. I structured the process around intake, assignment, costing, approval, quote dispatch and customer response, then connected rules, use cases, stories and acceptance tests. I also treated event completeness as a requirement: incomplete timestamps and customer holds cannot be silently converted into zero-duration stages. The local application provides a demo surface for the workflow and role permissions. The UAT scripts are execution-ready test design, not customer sign-off. In a live implementation, accountable business users would execute them against an agreed build and record evidence.”

## Questions to be ready for

- What is the difference between a business rule and a functional requirement?
- How do you trace a need to a test result?
- Why are customer holds non-additive in a stage-duration waterfall?
- How do you deal with missing or incomplete timestamps?
- What separates a passed API test from business acceptance?
- What would you do when stakeholder findings contradict the original scope?

## Honest claim boundary

Claim the BA artefacts and technical traceability you built and can explain. Do not claim stakeholder interviews, validated personas, user acceptance, process adoption or business sign-off before executing the prepared fieldwork.


## Five-minute evidence pack

`docs/ba/complete_traceability_and_process_pack.md`.
