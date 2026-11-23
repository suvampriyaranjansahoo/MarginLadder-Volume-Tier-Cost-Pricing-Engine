# Project Manager — 12-week delivery plan

**Purpose:** show a controlled path from problem validation to a reversible pilot.  
**Reader:** hiring manager, project sponsor, delivery lead.  
**Recruiter conclusion:** scope, gates, dependencies, ownership and stop points are planned. This is a proposed plan, not a live project.  
**30-second explanation:** “I start with evidence, not a software build. Three gates prevent spend moving forward until process data, control design and pilot results meet agreed checks.”

## Relative Gantt
Legend: `█` planned work; `◆` gate; `→` dependency. Week 1 begins at the approved hypothetical start date.

| Workstream / task | Owner | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 | W9 | W10 | W11 | W12 | Dependency / output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Charter, scope, baseline plan | Sponsor / PM | █ | | | | | | | | | | | | Start |
| Map AS-IS and data definitions | BA | █ | █ | | | | | | | | | | | Charter |
| Collect representative RFQ timestamps | Ops lead | █ | █ | █ | | | | | | | | | | Access and consent |
| Loss reason and price-parity review | Sales / Finance | | █ | █ | | | | | | | | | | Data definitions |
| Gate 1 — problem evidence | Sponsor | | | ◆ | | | | | | | | | | Complete trace + data quality |
| TO-BE and control requirements | BA / Ops | | | █ | █ | | | | | | | | | Gate 1 |
| Option and economics refresh | Finance | | | █ | █ | | | | | | | | | Gate 1 |
| Gate 2 — solution and business case | Sponsor | | | | ◆ | | | | | | | | | Approved scope + downside case |
| Configure register / approval workflow | Product / IT | | | | | █ | █ | | | | | | | Gate 2 |
| Security, access, audit and recovery review | IT / Security | | | | | | █ | █ | | | | | | Working build |
| Test, training and UAT preparation | QA / BA | | | | | | | █ | █ | | | | | Controls signed off |
| Independent UAT and defect closure | Business tester | | | | | | | | █ | █ | | | | UAT scenarios |
| Gate 3 — pilot readiness | Sponsor | | | | | | | | | ◆ | | | | Critical defects closed |
| Reversible pilot and daily monitoring | Ops lead | | | | | | | | | | █ | █ | | Gate 3 |
| Finance review and scale/stop decision | Finance / Sponsor | | | | | | | | | | | █ | ◆ | Mature pilot outcomes |

## Critical path
Charter → AS-IS and data definitions → timestamp/loss evidence → Gate 1 → TO-BE/control requirements + refreshed economics → Gate 2 → workflow configuration → security/control review → independent UAT → Gate 3 → pilot → finance review → scale/stop.

A delay on this chain moves the earliest scale decision. The plan has no actual start date or actual completion status.

## Three gates
- **Gate 1, end W3 — problem evidence:** timestamp completeness ≥95% in the representative sample; stage intervals are non-overlapping or explicitly concurrent; loss reasons have an owner and evidence source. If not, extend measurement and do not approve software scope.
- **Gate 2, end W4 — solution/business case:** selected option has an owner, process control, price-parity approach, downside economics and no unsupported conversion claim. If the case depends on unmeasured win-back, fund only the measurement pilot.
- **Gate 3, end W9 — pilot readiness:** no critical security/control defects; independent UAT critical scenarios pass; rollback and support owner are ready. If not, do not start pilot.

## What is late, who owns it, what happens next?
No work has started. Therefore no task is reported late. In execution, compare actual finish to baseline; the task owner records variance and forecast; PM records downstream impact; accountable sponsor decides recovery, scope change or gate movement. Use `docs/pm/status_reports_templates.md`.
