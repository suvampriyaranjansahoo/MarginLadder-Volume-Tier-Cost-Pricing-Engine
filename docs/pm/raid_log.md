# RAID log — planning register

**RAID** means Risks, Assumptions, Issues and Dependencies. All entries are OPEN planning items because no live programme exists. Likelihood and impact use Low / Medium / High, not measured probabilities.

| ID | Type | Item | Owner | Likelihood | Impact | Trigger | Mitigation / response | Status |
|---|---|---|---|---|---|---|---|---|
| R01 | Risk | Timestamp gaps make cycle diagnosis unreliable | Ops lead | High | High | Completeness below 95% | Define required events; daily missingness check; extend sample | OPEN |
| R02 | Risk | Overlapping stage clocks inflate total waiting | BA | Medium | High | Sum of stage time exceeds elapsed time | Define interval semantics; flag overlap; use union of intervals | OPEN |
| R03 | Risk | 25% win-back assumption is not causal | Finance | High | High | No comparison evidence | Exclude benefit from committed case; run controlled test only if volume permits | OPEN |
| R04 | Risk | Faster quotes create low-margin orders | Sales / Finance | Medium | High | Margin below floor | Price-parity and contribution floor before release | OPEN |
| R05 | Risk | Plant cannot fulfil incremental demand | Ops lead | Medium | High | Capacity load exceeds confirmed capacity | Capacity check before acceptance; cap pilot volume | OPEN |
| R06 | Risk | Adoption lower than assumed | Product lead | High | Medium | Weekly active operators below threshold | Observe task friction; simplify workflow; stop scale if adoption low | OPEN |
| R07 | Risk | User access exposes confidential drawings or rates | Security | Medium | High | Unauthorised access test fails | Least privilege, no sensitive public data, access review | OPEN |
| R08 | Risk | Migration corrupts existing RFQ records | Product/IT | Low | High | Upgrade test fails | Backup, migration dry run, rollback plan | OPEN |
| R09 | Risk | UAT unavailable before pilot | BA | Medium | High | No independent tester booked by W7 | Book tester early; move Gate 3 if unavailable | OPEN |
| R10 | Risk | Scope expands into ERP/AI integration | PM | Medium | Medium | New request lacks approved change | Change request and impact assessment | OPEN |
| A01 | Assumption | 60 RFQs/month is representative | Ops lead | High | High | Actual monthly volume differs materially | Verify 12-month source extract | OPEN |
| A02 | Assumption | 5% lost-RFQ rate has valid denominator | Sales | High | High | Closed-lost count does not reconcile | Define eligible RFQ denominator and exclusions | OPEN |
| A03 | Assumption | 12% contribution margin applies to recovered mix | Finance | High | High | Product-level margin differs | Validate product/customer mix and contribution bridge | OPEN |
| I01 | Issue | No real user or stakeholder evidence exists | PM | High | High | No consented participant access | Keep user evidence claims blank; seek permissioned access | OPEN |
| D01 | Dependency | Approved price-parity reference set | Finance | Medium | High | Reference rates unavailable | Obtain authorised anonymised reference set | OPEN |
| D02 | Dependency | Security owner reviews access model | Security | Medium | High | No reviewer assigned | Name reviewer before Gate 2 | OPEN |
