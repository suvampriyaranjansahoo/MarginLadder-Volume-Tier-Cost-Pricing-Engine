# Persona 3 hand-off — 14-day real-evidence action plan

**Dates:** 21 November–4 December 2026. These are planned dates, not completed actions.  
**Consent rule:** participation is voluntary. Obtain explicit permission before notes. Separate permission is needed for recording, quotes or public attribution. Never collect confidential drawings, customer names, live prices, personal data or credentials.

| Day | Action and why | Ready script / checklist | Consent wording | Record and save | Potential rating effect |
|---|---|---|---|---|---|
| 21 Nov | Prepare outreach and privacy plan | Select five people with relevant RFQ, quoting, approval or operations tasks. Prepare the same three tasks for each. | “This is voluntary. You may skip any question or stop. May I take anonymous notes?” | Private consent register; no public names | No score until evidence exists |
| 22 Nov | Publish and smoke-test a safe demo | Use synthetic records only; remove demo passwords; HTTPS; test private browser and mobile; verify no secrets | Not applicable to public demo; no participant data | `docs/validation/live_demo_check.md` | Findability only; does not lift Observed cap |
| 23 Nov | Task session 1 | Ask participant to create RFQ, assign owner, identify overdue item; do not coach | “May I take anonymous notes? Recording is separate and optional.” | Copy `data/templates/usability_session_template.csv` to private session log | APM/BA observed evidence |
| 24 Nov | Task session 2 | Repeat same tasks, same build and instructions | Same consent | Same log; completion time, errors, help needed | APM/BA depth |
| 25 Nov | Expert call 1 — operations | “Walk me through the last RFQ. Where did it wait? What timestamps prove it? What would make my diagnosis wrong?” | “May I keep anonymous notes? I will not identify you or your employer.” | Private call notes; public summary only if permissioned | Consulting/PM/BA |
| 26 Nov | Task session 3 | Test missing fields, recost and send-back using synthetic data | Same consent | Task log and issue IDs | APM/BA |
| 27 Nov | Stakeholder call | “Who owns each gate? What evidence is needed? Which dependency or stop condition is missing?” | Anonymous notes permission; separate attribution permission | Decision feedback and role-only notes | PM/Consulting |
| 28 Nov | Task session 4 | Test invalid rate, access restriction and version history | Same consent | Task log, defect severity and reproducible steps | APM/BA |
| 29 Nov | Annual-report source check | Open official ACMA FY25 industry review and the listed company's annual report used in the project; record exact page/table, year, unit and consolidated/standalone basis. Remove any number that cannot be traced. | Not applicable | `docs/validation/annual_report_source_check.md` | Consulting Honesty; independent source cap only if truly separate |
| 30 Nov | Task session 5 | Repeat key task after evidence-backed fixes; ask participant to explain what they think happened | Same consent | Before/after task record; no broad significance claim from n=5 | APM/BA |
| 1 Dec | Expert call 2 — finance/costing | “What source supports the lost-RFQ denominator, AOV, contribution and capacity? Which line is most likely wrong?” | Anonymous notes permission; no confidential financial data | Assumption challenge log | Finance/Consulting |
| 2 Dec | Expert call 3 — product/BA/security | “Which requirement is missing? What is unsafe? What would make this a no-go?” | Anonymous notes permission | Review notes and change log | APM/BA |
| 3 Dec | Independent UAT by someone else | Give frozen build and `docs/ba/uat_scripts.md`; do not coach; record pass/fail and defects | “This is a portfolio demo with synthetic data, not company acceptance. May I record anonymous pass/fail notes?” | Copy `data/templates/uat_execution_log_template.csv` to completed private run log | BA/PM observed evidence |
| 4 Dec | Close two-week sprint and issue RAG report | Reconcile planned/completed sessions, consent, defect closure, demo smoke test and source check. | Confirm permission for any public anonymous summary or quote | `docs/validation/status_2026-12-04.md`; update evidence ledger | Can lift Observed cap if actual evidence exists |

## Opening script
“Thanks for speaking with me. I am testing a portfolio prototype for a hypothetical RFQ-to-quote process. This is not a company project and I am not asking for confidential information. I want to see how you complete a few tasks and where the screen is unclear. There are no right answers. You may skip any question or stop at any time. I will take anonymous notes. I will not record audio, video or screen unless you separately agree. Do you consent to take part?”

## Privacy and evidence rules
- Keep participant identity key private and separate from anonymous task logs.
- Ask separately before recording, quoting or public attribution.
- If consent is declined, do not run the session.
- Do not publish employer names or confidential information.
- A small sample is qualitative usability evidence, not proof of market demand or causal conversion lift.
- Two independent real sources must independently support the same claim. Two AI summaries or two notes from the same person do not count.

## Status report templates
### 21 Nov — TEMPLATE / kickoff
RAG: NOT SET. Sessions planned/completed: [ ]. Risks: [ ]. **Decisions needed:** approve participant access and synthetic demo scope; owner [ ]; due [ ].

### 28 Nov — TEMPLATE / midpoint
RAG: NOT SET. Sessions planned/completed: [ ]. Expert calls: [ ]. Stakeholder call: [ ]. Findings: [ ]. **Decisions needed:** continue, redesign or pause; owner [ ]; due [ ].

### 4 Dec — TEMPLATE / close
RAG: NOT SET. Sessions: [ ]. UAT: [ ]. Live link: [ ]. Annual-report check: [ ]. **Decisions needed:** accept changes, keep open items or stop; owner [ ]; due [ ].
