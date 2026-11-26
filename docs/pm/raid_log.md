# RAID log (planning register)

RAID = Risks, Assumptions, Issues, Dependencies. **All entries are planned items for a hypothetical case: none has happened.** Status is OPEN for all. Likelihood and impact are Low / Medium / High judgements, not measured probabilities. Score = likelihood x impact (1 to 9). Owner codes are in `docs/pm/raci_tasks.md`; task codes and days are in `docs/pm/schedule_and_critical_path.md`.

| ID | Type | Item | Owner | Likelihood | Impact | Score | Trigger | Task | Mitigation / response | Status |
|---|---|---|---|---|---|---:|---|---|---|---|
| R01 | Risk | Timestamp gaps make the cycle diagnosis unreliable | EH | Medium | High | 6 | Fewer than 95% of the 10 traced RFQs have all events | T03 | Name the required events first; check gaps daily; extend the sample before Gate 3 | OPEN |
| R02 | Risk | Overlapping stage clocks inflate the total waiting time | BA | Medium | High | 6 | Sum of stage days exceeds elapsed days | T03 | Define stage rules in T02; flag overlaps; use the union of intervals | OPEN |
| R03 | Risk | The 25% win-back is not causal | SH | High | High | 9 | Fewer than 20 coded lost RFQs, or under 25% lost to delay | T05 | Keep the benefit out of committed economics; stop after Gate 3 if the rule fails | OPEN |
| R04 | Risk | Faster quotes win low-margin orders | SH | Medium | High | 6 | A quote falls below the contribution floor | T16 | Contribution floor and price parity before any quote is released | OPEN |
| R05 | Risk | The plant cannot fulfil the extra orders | PH | Medium | High | 6 | Spare capacity is under the 46% break-even fit | T04 | Capacity answer before Gate 3; cap pilot volume | OPEN |
| R06 | Risk | Estimators do not use the register | EH | High | High | 9 | Fewer than 6 of 6 estimators log new RFQs in week 1 of use | T09 | Observe friction; simplify; Gate 2 holds the second payment | OPEN |
| R07 | Risk | Access exposes drawings or rates | IT | Medium | High | 6 | An access test fails | T08 | Least privilege; synthetic data only in the build; named users | OPEN |
| R08 | Risk | Rate master is late or disputed | RO | Medium | High | 6 | Not signed by day 9 | T06 | Escalate to the Managing Director on day 6; T14 and T13 have slack, so Gate 4 moves first | OPEN |
| R09 | Risk | Nobody independent is free to run UAT | BA | Medium | Medium | 4 | No tester booked by day 8 | T08 | Book a tester in T01; Gate 2 moves if UAT slips (T08 is on the critical path) | OPEN |
| R10 | Risk | Scope grows into ERP or AI features | PO | Medium | Medium | 4 | A request touches integration or drawing extraction | T12 | Change control; these items are listed as not planned in the roadmap | OPEN |
| R11 | Risk | Pilot is too short to read | PO | Medium | High | 6 | Fewer than 30 RFQs by day 40 | T16 | Report distributions and sample size; do not claim a result from a small sample | OPEN |
| A01 | Assumption | 60 RFQs a month is typical | EH | Medium | High | 6 | The 12-month extract differs by more than 15% | T03 | Check the extract in T03 | OPEN |
| A02 | Assumption | The 5% lost-RFQ rate has a clean denominator | SH | High | High | 9 | Closed-lost count does not reconcile to the register | T05 | Agree the eligible RFQ definition in T02 | OPEN |
| I01 | Issue | No real user or stakeholder evidence exists yet | PO | High | High | 9 | Always open in this portfolio | T03 | Claims stay as hypothetical until real sessions are held | OPEN |
| D01 | Dependency | Signed 20-part reference set from the plant | SH | Medium | High | 6 | T14 not done by day 12 | T14 | Agree the 20 parts in the first week | OPEN |
| D02 | Dependency | Plant calendar and holiday list | EH | Low | Medium | 2 | Working-day counts disagree with the plant | T02 | Load the calendar before the trace | OPEN |

## Top three by score
R03 (win-back not causal), R06 (estimators do not use the register) and R01 (timestamp gaps). Each has a day-based trigger and a gate that stops the spend.

## Review rhythm
Reviewed weekly in the status report. A risk with score 6 or more and no mitigation owner is escalated to the Managing Director within one working day.
