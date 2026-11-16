# Business review: where the case is weakest, and what each weakness does to the answer

This is a pre-mortem on MarginLadder. Every number comes from `model/MarginLadder_finance_extension.xlsx` (sheet names in brackets) or the original model. Tags: Brief, Derived, Assumption, Judgement.

## Verdict after the review
The recommendation stays: fund the register and clock first, and fund the full build only if a Week 1 trace confirms waiting dominates. The review changes why: the expected-value test (finding 13) does not favour staging on its own, so the case for staging now rests on risk, speed and reversibility. It also adds two conditions to Gate 3 (see the end).

## Findings, largest first

| # | Weakness | Effect on the answer | Status |
|---|---|---|---|
| 1 | **Win-back is the whole case.** The 25% was one guess. It is really two: the share of lost RFQs lost because the quote was slow (50% assumed) times the chance a faster quote wins (50% assumed). [Win-back] | Break-even is 11.6%. The case fails in 6 of 30 combinations of the two factors, for example when only 20% of losses come from delay and a faster quote wins 40% of those. Margin of safety at base is 2.2x. | Open. Week 1: code the stated reason on the last 20 lost RFQs and ask three lost customers whether they would have waited. |
| 2 | **Capacity to deliver the won orders is untested.** The case counts 12% margin on every recovered order. If the plant is at capacity, won orders displace other orders. | Not quantified. It could remove most of the benefit. | Open. Ask the plant head for utilisation before Gate 3. [Judgement] |
| 3 | **What "lost RFQ" means.** The 5% (Brief) may include RFQs the plant chose not to quote. Those are not recoverable by speed. | Scales the whole pool one for one. | Open. Confirm the definition with sales. |
| 4 | **Benefits arrive gradually, not on day one.** | With a 6-month linear ramp, margin payback is 7.9 months, not 4.9. [MarginLadder link] | Disclosed. Still inside the 12-month rule. |
| 5 | **GST on the fee.** The model uses ₹8 lakh. The invoice is ₹8 lakh plus 18% GST. | If input credit is not available, payback is 5.8 months. With ramp as well, 8.8 months. | Disclosed. Still inside 12 months. |
| 6 | **Margin-only payback ignores tax and working capital.** | Cash payback is 24 months, not 4.9. IRR is 76% over 3 years. | Fixed and shown beside the 4.9. |
| 7 | **The 97% chance NPV is positive is high by construction.** NPV turns positive at about a 6% win-back and the simulated range is 0 to 50%. | It says the case is robust to the ranges used, not that success is 97% likely. | Disclosed in the dashboard and README. |
| 8 | **Working-capital days (45) were a guess.** | Six listed firms and Endurance report −12 to 115 days, median 22. IRR runs from 33% (115 days) to above 100% (0 days or less). The base of 45 sits between Sansera (39) and Sundram Fasteners (86). [MarginLadder link] | Tested. Kept at 45. Listed firms get better supplier terms than a small plant. |
| 9 | **Is the 12% order margin realistic?** | Listed auto-component firms earned a 13.6% operating margin in FY26 (Elara Capital); Endurance 13.2%. The case is 1.6 points lower than the listed figure. | Sense-checked. |
| 10 | **Is this a venture-sized problem?** | No. Across the industry the recoverable pool is about ₹342 crore a year, under 0.1% of turnover, at assumptions of 30% of turnover on RFQ quotes. A 2% adoption of an ₹8 lakh tool is about ₹2.5 crore once. [Market sizing] | This supports an internal tool and process fix, not a product bet. |
| 11 | **The earlier Isocode pack states a vendor cash gap of ₹1.2 lakh.** | On a cash-received basis the peak gap is about ₹3.5 lakh (44% of the fee). | Corrected in this repo. The old pack is superseded and should not be reused. |
| 12 | **External data quality.** Peer and Endurance figures come from aggregator sites. | FY26 revenue and profit tie to the company-reported figures within rounding. EBITDA differs by about ₹159 crore because the company includes other income. Gabriel India's P/E is distorted by ₹149 crore of other income in the trailing year and a merger effective 22 May 2026. [Data, Comps] | Cross-checked. Still verify against the BSE annual report before quoting. |
| 13 | **Staging costs expected value at my assumptions.** Five scenarios (zero benefit 15%, downside 15%, conservative 20%, base 35%, upside 15%) and an imperfect gate. [Decision analysis] | Building now has an expected NPV of ₹27.7 lakh against ₹25.1 lakh staged, a gap of ₹2.6 lakh (pre-tax). Staging wins only if the chance of zero benefit rises above about 35%. Stopping at Gate 3 costs 40% of the fee, more than the small loss from building into a weak scenario. | Disclosed. Staging is kept on other grounds: it scores first of seven options on five weighted criteria (judgement), the register and clock deliver benefit before Gate 3 (not counted here), and it is reversible. The gate conditions test the zero-benefit risk directly. |

## What a sceptical reviewer will ask, and the answer in the files
- *Why is the stock at ₹2,520 when your DCF says ₹1,077?* The price implies either a discount rate near 8.1% or about 39% yearly revenue growth for five years. The company's four-year record is 18%, including an acquisition. [Reverse DCF]
- *Is that a mistake in your model?* It may be partly. The DCF uses a sourced beta, a sourced risk-free rate and assumed growth and margins. Endurance is the cheapest of seven listed peers on EV to operating profit (18.7x against a median of 41.2x), so the whole sector trades far above what a 12% discount rate supports. [Comps]
- *If expected value favours building now, why stage it?* At my assumptions, by about ₹2.6 lakh of ₹27.7 lakh. Staging wins if the chance of zero benefit is above about 35%, and it scores first on speed, reversibility and risk. I would build now if the Week 1 trace and capacity check both come back clean.
- *What would change your mind?* Win-back below 11.6% after six months, or a plant already at capacity.

## Changes to the plan from this review (my proposal, Judgement)
1. **Gate 3 condition A:** lost-RFQ reasons coded on at least 20 RFQs, with at least 25% attributed to delay. Below that, stop.
2. **Gate 3 condition B:** the plant head confirms spare capacity to make the extra orders.
