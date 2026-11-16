# MarginLadder as a 5-minute case answer

Use this for consulting and strategy interviews. Say it in this order. Every number is tagged: Brief (given), Derived (worked out), Assumption or Judgement (mine).

## 1. The question (20 seconds)
A Pune auto-parts maker takes 9 working days to send a quote against a 4-day target and loses 5% of RFQs. Should it pay ₹8 lakh plus GST for a costing app? [Brief]

## 2. Clarify first (20 seconds)
- What does "lost" mean: lost on price, or lost on delay?
- Does the plant have spare capacity to make extra orders?
- Is the 9 days measured, or an estimate?

## 3. Issue tree (30 seconds)
Why does a quote take 9 days, not 4?
- Work time: costing 5 parts at 2.5 h each is 12.5 h, or 1.56 days. [Derived]
- Wait time: checks, approval, sending, queueing. The other 7.44 days (83%). [Derived]

Is the answer worth the cost?
- Value: lost RFQs recovered × margin per order.
- Cost: fee, running cost, tax, working capital.
- Risk: will faster quotes actually win orders?

## 4. Hypothesis (15 seconds)
Waiting, not costing, is most of the delay. A costing screen alone closes about 0.94 day of the 5-day gap. The register, clock and approval rule must close the rest. [Derived]

## 5. Two analyses (90 seconds)
**Where the days go.** Costing is 17% of the cycle. If a Week 1 trace of 10 RFQs shows costing above 40%, cut scope to the screen and engine.

**Does it pay?** 36 lost RFQs a year × ₹2.4 lakh margin × 25% win-back is ₹21.6 lakh a year. Break-even win-back is 11.6%. [Derived, win-back is an Assumption]
- Margin payback: 4.9 months; with a 6-month ramp and no GST credit, 8.8 months.
- After tax and working capital: cash payback 24 months, IRR 76% over 3 years.
- Risk: the 25% is 50% of losses due to delay × 50% that a faster quote wins. The case fails in 6 of 30 combinations.

## 6. Recommendation (30 seconds)
Go in two steps. Step 1: fund the register and clock (about ₹2 to 2.5 lakh [Judgement]). Step 2: fund the full build at Gate 3 only if costing is under 40% of the cycle, at least 25% of lost RFQs trace to delay, and the plant has spare capacity. Stop if win-back is under 10% after six months.

## 7. Risks and next steps (30 seconds)
- Win-back unproven; capacity untested; vendor funds delivery before cash arrives (peak gap about ₹3.5 lakh, 44% of the fee).
- Next 30 days: code the reasons on 20 lost RFQs, trace 10 RFQs, ask three lost customers whether they would have waited.

## Stress test of my own answer (30 seconds, if time allows)
I modelled five outcomes and an imperfect gate. Building now has an expected NPV of ₹27.7 lakh; staging has ₹25.1 lakh, because stopping at Gate 3 still costs 40% of the fee. Staging wins only if the chance of zero benefit (no capacity, or delay was not the cause) is above about 35%. I assumed 15%. [Assumption] So I stage for speed, reversibility and risk, not for expected value, and I would build now if the trace and capacity check are clean.

## Industry context (10 seconds)
In a BCG and ACMA study of 450 suppliers, the 75 most resilient earned 1.4 points more EBITDA margin in FY25, after early spending on technology and capacity. It shows association, not cause, and says nothing about quoting.

## Likely follow-ups
- **Is it a big market?** No. The recoverable pool across Indian auto components is about ₹342 crore a year, under 0.1% of turnover, on assumptions that 30% of turnover is RFQ-quoted. Right-sized for an internal tool. [Assumption]
- **How do you know 25%?** I do not. It is two judgements multiplied. The plan is built so the first money buys the evidence.
- **Why stage if building now has higher expected value?** See the stress test above: staging gives up about ₹2.6 lakh of expected value in exchange for lower regret if capacity or diagnosis is wrong.
- **What if the client says no to a two-step plan?** Then fix the Excel for ₹1 to 2 lakh. It closes about a quarter of the gap. [Judgement]
