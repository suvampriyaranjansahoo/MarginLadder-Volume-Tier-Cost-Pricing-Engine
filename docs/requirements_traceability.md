# Requirements traceability

Each row links a problem from the brief to a requirement, the feature that meets it, and the test that proves it. The client's gate is AT-01, parity with its own Excel. UT-01 is a provider-side engine test (24 automated tests) and is evidence only.

| Problem (source) | Requirement | Test | Gate |
|---|---|---|---|
| 9 working days against a 4-day target [Brief] | Every RFQ has an owner, a due date and a visible age; reminders and a daily digest | AT-12 Early Release: register, clock and upload in use by six estimators and the Sales head | G2 |
| Costing takes 2.5 h a part, goal 1 h [Brief] | One screen to cost a part and show three volume prices | AT-09 PDF numbers equal the screen; AT-11 screens respond within 2 s for 95% of actions | G3, G4 |
| Quotes disagree with the Excel the team trusts | Match Company A's Excel on 20 parts, to ₹0.01 a line, on signed-off rates | AT-01 Parity | G2, G4 |
| Same inputs must give the same price | Fixed formulas, one rounding rule | AT-02 1,000 repeat runs give one result; UT-01 engine unit tests | G2 |
| Rates change over time | Effective-dated rates; overlaps refused; missing rate blocks costing visibly | AT-03 Rate dates | G2 |
| An old quote must stay reproducible | Quote snapshot with rate version | AT-04 Approved quote does not change when a rate changes | G3 |
| Quotes above ₹25 lakh a year need the Sales head [Brief] | Approval at the boundary, estimator cannot approve, each approval logged | AT-05 ₹25,00,000 needs no Sales head; ₹25,00,001 does | G3 |
| AI may extract and suggest, never price [Brief] | AI value shows its source and blocks costing until accepted; per-customer off switch | AT-06 AI safeguards | G3 |
| Routing time is judged by hand | Suggestions show the source part; plant head reviews new routings or a cycle time over 15% from the match | AT-07 Routing review | G3 |
| Past quotes sit in files | Import with a reconciliation: imported + duplicates + rejected = rows in file | AT-08 Import | G3 |
| NDA and no training on customer drawings [Brief] | Sign-in required; users see only their customer groups; every drawing view logged | AT-10 Access | G4 |

Source tags: Brief = given in the task. Derived = worked out from the brief.
