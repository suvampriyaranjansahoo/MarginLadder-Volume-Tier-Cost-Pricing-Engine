# APM / PM decision pack

**Purpose:** explain why the first product bet is workflow visibility, how success is measured and when to stop.  
**Reader:** APM hiring manager, product lead, engineering and operations.  
**Recruiter conclusion:** problem, opportunity, metric, prioritisation and experiment logic are connected. All user needs remain hypotheses until real discovery.  
**30-second explanation:** “The brief gives a long RFQ cycle but does not prove where time is lost. I would first expose ownership and waiting, then automate only the proven bottleneck.”

## User journey (hypothesis from the brief)
1. Sales receives RFQ and checks completeness.
2. Estimator reviews drawings and routes the work.
3. Estimator calculates material, process, scrap, overhead and margin.
4. Approval owner reviews price and exceptions.
5. Sales sends the quote and records outcome.
6. If lost, team records reason and whether it was price, timing, capacity or product fit.

Unknowns: actual handoffs, queue ownership, rework, customer holds, timestamp quality and reasons for loss. No real user validated this journey. The current journey is a desk-based hypothesis and must not be described as user research.

## Opportunity tree
**Outcome:** improve profitable RFQ response, not simply make the screen faster.
- Reduce avoidable waiting
  - visible owner and due date
  - queue-age alerts
  - approval escalation
- Reduce rework
  - complete intake checklist
  - versioned costing assumptions
  - reason-coded send-back
- Protect contribution and fulfilment
  - price parity check
  - contribution floor
  - capacity confirmation
- Improve learning
  - timestamp completeness
  - closed-lost reason quality
  - mature cohort outcome tracking

## Metrics tree and guardrails
| Level | Metric | Formula | Guardrail |
|---|---|---|---|
| Outcome | Profitable quote win rate | Won RFQs meeting contribution floor / mature eligible RFQs | Do not count immature or cancelled RFQs |
| Outcome | Contribution per eligible RFQ | Total contribution from mature cohort / eligible RFQs | Reconcile contribution to finance source |
| Process | End-to-end cycle | Quote sent timestamp − complete RFQ received timestamp | Business hours; separate customer hold |
| Process | Queue time | Sum of non-overlapping waiting intervals | Do not add overlapping stages |
| Process | Rework rate | RFQs with at least one recost / completed RFQs | Define recost event once |
| Adoption | Weekly active operators | Distinct operators completing ≥1 target task in week | Denominator = eligible operators |
| Quality | Quote error rate | Quotes with confirmed correction / quotes sent | Track severity and cause |
| Safety | Below-floor quotes | Quotes below contribution floor / quotes sent | Stop if above agreed tolerance |

## RICE and rank sensitivity
RICE = Reach × Impact × Confidence ÷ Effort. Scores below are judgement inputs on a 1–5 scale, not user preferences.

| Opportunity | Reach | Impact | Confidence | Effort | RICE |
|---|---:|---:|---:|---:|---:|
| RFQ register / queue visibility | 5 | 3 | 3 | 2 | 22.5 |
| Approval queue and escalation | 3 | 4 | 3 | 2 | 18.0 |
| Costing screen | 4 | 5 | 2 | 5 | 8.0 |
| ERP integration | 4 | 4 | 1 | 5 | 3.2 |
| AI drawing extraction | 2 | 4 | 1 | 5 | 1.6 |

**Rank flip:** if representative traces show costing dominates the working-time bottleneck, increase costing confidence from 2 to 5 and reduce effort from 5 to 3 after a scoped technical spike: RICE becomes 33.3 and it ranks first. If approval waits dominate, the approval queue remains the first targeted workflow. The ranking changes because evidence changes, not because the scoring formula changes.

## User validation protocol — execution-ready, not yet executed

**Current status: pending real participants.** No participant sessions, user interviews, task observations or adoption measurements are claimed in this release. The repository includes blank capture templates; blank templates are not validation evidence.

### Minimum formative round
- Recruit five independent participants who perform relevant RFQ, estimation, sales or approval work. Do not recruit only friends with no workflow exposure.
- Obtain voluntary consent; do not collect employer-confidential data, live prices, customer names, drawings or credentials.
- Freeze and record the build ID. Use the same synthetic dataset, task wording and success criteria for each participant.
- Ask participants to complete: (1) locate an overdue RFQ and identify its owner, (2) create a complete RFQ, (3) send back and re-cost a quote, (4) identify approval state and audit history.
- Do not coach during the first attempt. Record completion without help, time-on-task, errors, recovery, critical control failures and participant interpretation.
- Debrief with neutral questions: “What did you expect?”, “What was unclear?”, “What would you do next in your real workflow?”, “What evidence contradicts my assumption?”
- Log every session in `data/templates/usability_session_template.csv`; log discovery findings in `data/templates/discovery_interview_log_template.csv`.
- Change the design only against recorded findings. Re-test changed tasks with new or clearly identified returning participants.
- Report denominator and task-level outcomes. Five sessions are formative usability evidence, not statistically representative proof or product-market fit.

### Decision thresholds (pre-registered)
- Usability issue: at least 2 of 5 participants independently encounter the same material friction.
- Critical stop: any participant can bypass role controls, expose another role's data, or produce an unauthorised price/approval action.
- Continue iteration: at least 4 of 5 complete the core task without moderator help after remediation; this is a proposed usability gate, not a current result.
- Do not infer cycle-time reduction, conversion lift or adoption from a moderated prototype session.

## Experiment pack
**Hypothesis:** a visible owner, due date and approval queue will reduce avoidable queue time without increasing quote errors or below-floor quotes.

- **Primary metric:** median avoidable queue time per complete RFQ.
- **Secondary metrics:** p90 cycle time, task completion, rework rate, quote error rate, adoption.
- **Success rule:** at least 20% reduction in median avoidable queue time, no increase in quote errors, no below-floor quote, and ≥70% of eligible operators use the workflow weekly. These are proposed thresholds, not results.
- **Stop rule:** any access/privacy incident; any quote below approved floor; quote error rate rises by >5 percentage points; or operator task time rises by >20% for two consecutive review periods.
- **Worked sample-size example (ASSUMPTION, not a study result):** if baseline conversion were 20% and the minimum detectable improvement were 10 percentage points (to 30%), a two-sided 5% significance level and 80% power require about 292 RFQs per group (584 total). Allowing 15% incomplete outcomes raises this to about 344 per group (688 total). At the brief's 60 RFQs/month, even if every RFQ were eligible and split evenly, this is about 11.5 months of total volume. Actual eligible volume would likely be lower.
- **Cycle-time sample-size method:** use observed historical variance, a pre-set minimum detectable difference, 5% two-sided significance and 80% power. Cycle time may be skewed, so consider bootstrap or a suitable non-parametric method. Do not invent baseline variance.
- **Practical implication:** a short pilot is likely a feasibility/directional test, not a powered conversion experiment. Report sample size, confidence interval, data completeness and limits. Do not call a small underpowered sample proof of conversion lift.
- **Design:** pre-register eligibility, exclusions, measurement window and analysis before launch. Use a comparison group if feasible; otherwise describe the result as directional, not causal.

## What I would cut first
1. AI drawing extraction — requires labelled drawings, confidence handling and human review.
2. ERP write-back — integration and data ownership are not validated.
3. Customer portal — no evidence that customers need another interface.

## Launch and rollback checklist
- Named business owner and support contact.
- Access roles tested; no public credentials or sensitive customer files.
- Approved contribution floor and price-parity method.
- Complete timestamp definitions and event logging.
- Independent UAT completed; critical defects closed.
- Training and help route ready.
- Baseline and comparison method frozen.
- Rollback trigger: security incident, pricing error, data corruption, critical workflow outage, or guardrail breach. Disable pilot and return to prior process until approved.
