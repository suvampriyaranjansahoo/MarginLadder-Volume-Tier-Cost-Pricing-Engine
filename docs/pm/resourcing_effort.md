# Resourcing and effort estimate (generated figures)

**Hypothetical plan. These are planning estimates [Judgement], not timesheets.**

## Method (bottom-up, in person-days)
1. For each task in `docs/pm/plan.csv`, I estimated provider effort and client effort in person-days. Effort is not the same as duration: a 6-day build task can need 12 person-days.
2. Provider effort is split equally between the provider people marked R on the task.
3. Add 15% for programme management (weekly status, RAID log, change control, gate packs) [Assumption].
4. Add 10% contingency on the subtotal [Assumption].
5. Compare with the earlier 24 person-week plan used by the cash model (`finance/full_model.py`, 120 person-days).

| Step | Person-days |
|---|---:|
| Task effort, provider side (sum of plan.csv) | 95.0 |
| Programme management (15%) | 14.2 |
| Subtotal | 109.2 |
| Contingency (10%) | 10.9 |
| **Provider total** | **120.2** |
| Earlier plan (24 person-weeks x 5) | 120 |
| Difference | +0.2 (+0.1%) |
| Client-side effort (people at the plant, not billed) | 47.0 |

**Judgement call:** I set the task-level estimates so that the total lands close to the earlier 24 person-week plan. That makes the two numbers agree by design, so the match is a consistency check, not independent proof. Implied price per provider person-day: INR 8,00,000 / 120 = about INR 6,657.

## Effort by role (task effort only, before overhead and contingency)

| Role | Person-days | Side |
|---|---:|---|
| Managing Director | 6.0 | client |
| Estimation Head | 32.0 | client |
| Plant Head | 1.0 | client |
| Sales Head | 2.0 | client |
| Rate owner | 4.0 | client |
| Product owner (provider) | 25.0 | provider |
| Delivery lead (provider) | 47.0 | provider |
| Business analyst (provider) | 23.0 | provider |

## What would change this estimate
- The Week 1 trace shows costing is over 40% of the cycle: scope cuts to the costing screen, so T10 and T15 shrink and T12 grows.
- The rate master is late: T14 and T13 slip, but they have slack, so Gate 4 moves before the end date does.
- Estimators will not use the register: T16 restarts, which moves the end date day for day (it is on the critical path).
