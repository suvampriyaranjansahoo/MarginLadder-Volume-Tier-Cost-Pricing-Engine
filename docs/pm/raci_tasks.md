# RACI by task (generated)

Generated from `docs/pm/plan.csv`. **A = accountable, exactly one per task.** R = does the work, C = consulted, I = informed. `A/R` means the accountable person also does the work. A check in `scripts/check_role_packs.py` fails if any task has no A or more than one A.

Role codes: **MD** Managing Director; **EH** Estimation Head; **PH** Plant Head; **SH** Sales Head; **RO** Rate owner; **IT** Client IT; **PO** Product owner (provider); **DL** Delivery lead (provider); **BA** Business analyst (provider).

| ID | Task | MD | EH | PH | SH | RO | IT | PO | DL | BA |
|---|---|---|---|---|---|---|---|---|---|---|
| T01 | Kick-off and agreement signed | A | C | C | C | I | I | R |  |  |
| T02 | Agree definitions (RFQ / lost / hold / calendar) | I | A | C | C |  |  |  |  | R |
| T04 | Plant capacity answer (spare share of output) | I |  | A/R |  |  |  | C |  |  |
| T05 | Code the stated reason on the last 20 lost RFQs | I |  |  | A/R |  |  | C |  |  |
| T03 | Week 1 trace of 10 recent RFQs | I | A/R |  |  |  | C | I |  | R |
| T06 | Rate owner signs off the rate master |  | C |  |  | A/R |  | I |  |  |
| T07 | Build Early Release: register and clock |  |  |  |  |  |  | I | A/R | C |
| T08 | Run UAT-01 to UAT-12 on a frozen build |  | R |  |  |  |  | I | C | A/R |
| T14 | Agree and sign off the 20-part parity set | I | R |  | A | C |  | C |  |  |
| T09 | Estimators start daily use of the register | I | A/R |  |  |  |  | C |  |  |
| G2 | GATE 2: is the register in daily use? | A | C | I | C |  |  | R |  |  |
| T15 | Freeze baseline and pilot measurement sheet |  | C |  |  |  |  | I |  | A/R |
| T10 | One-screen approval card with deputy |  | I |  | C |  |  |  | A/R |  |
| T16 | Pilot of the Early Release (7 weeks) | I | R |  | C |  |  | A |  | C |
| T11 | Gate 3 evidence pack | I | C | C | C |  |  | A |  | R |
| G3 | GATE 3: build the full costing screen or stop? | A | C | C | C | I |  | R |  |  |
| T12 | Costing screen on the fixed engine and signed rates |  | C |  |  |  |  | I | A/R |  |
| T13 | Run the 20-part parity test | I | A/R |  | C |  |  |  | R |  |
| G4 | GATE 4: do prices match within INR 0.01? | A | C |  | C | I |  | R |  |  |
| T17 | Month-3 read-out: Release 2 or stop | A | C | C | C | I |  | R |  | R |

The stakeholder-level RACI for the product (who approves what) is in `docs/ba/raci_stakeholders.md`. This page is about delivering the plan.
