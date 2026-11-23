# Decision log

One line per call: what I chose, what I gave up and what would change my mind. Tags as elsewhere: Brief, Derived, Assumption, Judgement.

| ID | Decision | Alternatives | Why | Cost of the choice | Revisit when |
|---|---|---|---|---|---|
| D-01 | Start with the register, clock and one-screen approval, then the costing screen. | Costing screen first. | Costing is 17% of the cycle [Derived]. Waiting is most of the delay. | The costing screen, which users will ask for first, comes second. | The Week 1 trace shows costing above 40% of the cycle. |
| D-02 | The fixed formula sets every price. AI reads and suggests only. | Let AI propose prices. | The brief forbids it, and a wrong price is a legal and margin risk. | Slower intake than a full-AI flow. | Never for pricing. For extraction, when an evaluated benchmark exists. |
| D-03 | Count recovered margin as the benefit. Count freed estimator time as upside only. | Count both. | Time saved is not cash unless the team quotes more or hiring is avoided. | A smaller headline number (₹21.6 lakh, not ₹45.9 lakh). | Company A shows a redeployment or hiring plan. |
| D-04 | Net the freed time of the hour spent reviewing each RFQ: 4,680 h, ₹21.06 lakh. | Show gross 5,400 h, ₹24.3 lakh. | The register adds a review step. Ignoring it overstates the gain. | The README shows two figures. | A time study gives the real review time. |
| D-05 | Split win-back into 50% due to delay × 50% won once faster. | One 25% number. | The two parts are tested by different Week 1 steps. | More to explain. | Lost-RFQ coding gives the real shares. |
| D-06 | Keep the build staged: Early Release first, full build at Gate 3. | Build everything now. | Expected value favours building now by ₹2.6 lakh at my inputs, but staging is reversible and tests the zero-benefit risk. | A small expected-value loss. | Zero-benefit chance is judged above 35% (then staging wins on value too). |
| D-07 | Payments 20/20/40/20. | 30/30/30/10 to shrink the cash gap. | 60% of the fee is paid only after delivery and acceptance. | Funded gap of ₹3.5 lakh, 44% of the fee, at net-10 terms. | Company A will not accept a longer gap. |
| D-08 | Use Erlang C as a pressure gauge, not a forecast. | Discrete event simulation. | It runs on brief inputs only and explains the shape of the problem in one table. | Ignores splitting jobs, interruptions and priorities. | The trace shows queue time is a large share. |
| D-09 | Roles come from a signed-in session. | Keep the role dropdown. | A dropdown lets anyone approve. The rule is the point of the product. | Demo needs a login. | Never. |
| D-10 | Use scrypt and the standard library, no new packages. | bcrypt, argon2. | Fewer dependencies for a local demo. | Not the strongest default. | A production pilot. Move to argon2 and add MFA. |
| D-11 | Store money as decimal text in SQLite. | Floats or integers of paise. | No binary rounding drift. | Sorting needs a cast. | A move to Postgres with numeric types. |
| D-12 | Run SQL on the simulated log and label every output simulated. | Wait for real data. | The queries are ready the day real data arrives. | Findings are method demonstrations only. | Real trace imported. |
| D-13 | Keep the original v1 and v2 files byte-identical. | Rewrite them. | A reviewer can diff and see nothing was silently changed. | Some documents still show the gross 5,400 h figure. `numbers.json` states which figure is which. | A final clean-up before sharing. |

## Rejected ideas
- **A customer portal.** The problem is internal. Outside the scope.
- **ERP write-back.** Source of truth is not agreed.
- **Automatic approval after a timeout.** The brief says approval is never automatic.
