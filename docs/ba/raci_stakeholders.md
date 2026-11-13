# Stakeholders and RACI

R = does the work, A = accountable (one per row), C = consulted, I = informed.

| Activity | Estimator (6) | Estimation head | Plant head | Sales head | Managing Director | Rate owner | Client IT | Provider PM |
|---|---|---|---|---|---|---|---|---|
| Log every new RFQ in the register | R | A | I | I | | | | C |
| Cost a part and price three volumes | R | A | C | I | | C | | |
| Confirm routing and cycle time | C | I | R, A | | | | | |
| Approve quotes above ₹25 lakh a year | | I | | R, A | | | | |
| Maintain and sign off rates | C | C | | | | R, A | | |
| Sign off the 20-part parity test (AT-01) | R | C | | A | | C | | R |
| Set access groups and NDA rules | | | | C | A | | R | C |
| Gate sign-off | I | C | C | R | A | | | R |
| Go-live and Excel retirement | R | A | | I | I | | C | R |

## Stakeholder notes
| Stakeholder | What they care about | Likely objection | How the plan answers it |
|---|---|---|---|
| Estimators | Not being slower, not being blamed for errors | "My Excel is faster than a new tool" | Parity with their own Excel (AT-01); Excel stays as fallback during the parallel run |
| Sales head | Margin protection, not being the bottleneck | "I should see every quote" | One-screen card, 70% trigger, deputy, 4 h reminder; never automatic approval |
| Plant head | Correct routing and cycle times | "Suggestions will be wrong" | Suggestions show their source part; review is required for new routings or a cycle time more than 15% from the match |
| Rate owner | Rates stay correct and dated | "Another place to update" | One effective-dated rate master loaded from the ERP export |
| Client IT | NDA, access, no training on drawings | "AI will leak drawings" | Named users, access groups, audit log, per-customer AI switch (AT-06, AT-10) |
| Managing Director | The 5% lost RFQs, cash, risk | "Is it worth ₹8 lakh?" | Payback 4.4 to 8.9 months; break-even win-back 9.3%; 5% win-back loses money |
