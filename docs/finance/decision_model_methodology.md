# MarginLadder finance case: model logic, controls and interpretation

**Purpose:** explain how the business case is derived and which values are facts, calculations, assumptions or judgement. This is the simple operating arithmetic behind the case. The two Excel workbooks remain the detailed financial models; the Python module `finance/case_model.py` provides an independently testable calculation of the core brief arithmetic.

## 1. Input register

| Input | Value | Classification | Validation needed |
|---|---:|---|---|
| RFQs per month | 60 | Brief | Confirm against intake register |
| Parts per RFQ | 5 | Brief | Confirm distribution, not just average |
| Estimators | 6 | Brief | Confirm current staffing / allocation |
| Costing hours per part | 2.5 h | Brief | Time study |
| Target costing time | 1.0 h | Brief target | Validate with pilot |
| Estimator hourly cost | ₹450 | Brief | Confirm loaded cost basis |
| RFQ loss rate | 5% | Brief | Confirm lost vs no-bid definition |
| Average order value | ₹20 lakh | Brief | Define order horizon / gross vs net |
| Order margin | 12% | Brief | Confirm whether contribution or operating margin |
| Share of lost RFQs caused by delay | 50% | Assumption | Code at least 20 lost RFQs and interview sales/customers |
| Win probability for faster quote | 50% | Assumption | Cohort-level outcome validation |
| Development fee | ₹8 lakh | Proposed commercial assumption | Confirm vendor scope and payment milestones |
| Annual run cost | ₹2 lakh | Assumption | Obtain support / hosting / maintenance estimate |

## 2. Lost-RFQ margin pool

Annual RFQs:

`60 RFQs/month × 12 months = 720 RFQs`

Annual lost RFQs:

`720 × 5% = 36 RFQs`

Margin pool attached to those lost RFQs:

`36 × ₹20,00,000 average order value × 12% margin = ₹86,40,000`

This ₹86.4 lakh is a theoretical annual margin pool associated with lost RFQs, not guaranteed recoverable profit. Some lost RFQs may be no-bids, commercially unattractive, capacity-constrained or lost for reasons unrelated to quotation speed.

## 3. Win-back decomposition

The base case deliberately splits one optimistic-looking assumption into two testable components:

`Win-back rate = delay-related share of losses × win probability after faster quote`

`25% = 50% × 50%`

`Annual recovered margin = ₹86.4 lakh × 25% = ₹21.6 lakh`

The split matters. It tells the team what to validate: the reason for loss and the counterfactual likelihood of winning if the quotation had been faster. The 25% is not observed performance.

## 4. Investment and payback bridges

| Calculation | Formula | Base-case output | Interpretation |
|---|---|---:|---|
| Gross margin payback | ₹8 lakh / ₹21.6 lakh × 12 | 4.44 months | Ignores running cost, tax and working capital |
| Operating payback after run cost | ₹8 lakh / (₹21.6 lakh − ₹2 lakh) × 12 | 4.90 months | Simple operating payback; still not cash payback |
| Break-even win-back including one year run cost | (₹8 lakh + ₹2 lakh) / ₹86.4 lakh | 11.57% | Minimum win-back under this one-year simple model |
| Cash payback | Full tax and working-capital cash flow schedule | About 24 months in the extension model | Use the Excel financial-extension workbook; assumptions include working-capital days and tax |

The 24-month cash-payback figure must not be confused with the 4.9-month simple operating payback. They answer different questions. The detailed Excel cash-flow schedule is the source for tax, receivables, stock, cash gaps, NPV and IRR assumptions.

## 5. Scenario table

| Win-back | Recovered annual margin | Net after ₹2 lakh annual run cost | Simple payback after run cost |
|---:|---:|---:|---:|
| 5% | ₹4.32 lakh | ₹2.32 lakh | 41.38 months |
| 12.5% | ₹10.80 lakh | ₹8.80 lakh | 10.91 months |
| 25% | ₹21.60 lakh | ₹19.60 lakh | 4.90 months |
| 50% | ₹43.20 lakh | ₹41.20 lakh | 2.33 months |

Reproduce these numbers with:

```bash
python3 -m finance.case_model
```

## 6. Productivity capacity — separate from cash savings

Current estimator effort:

`720 RFQs × 5 parts × 2.5 hours = 9,000 hours/year`

Target estimator effort:

`720 × 5 × 1 hour = 3,600 hours/year`

Potential time released:

`9,000 − 3,600 = 5,400 hours/year`

Theoretical capacity value:

`5,400 × ₹450 = ₹24.3 lakh`

This is not added to the recovered-margin benefit. It is a capacity opportunity, not automatically cash savings. It becomes financial value only if management redeploys the hours, avoids incremental hiring or quotes additional profitable work. Adding it to recovered margin without evidence would double count or overstate the business case.

## 7. Financial model controls

- Preserve the difference between revenue, gross / contribution margin, operating profit and cash flow.
- Do not treat GST collected as revenue or project margin.
- Apply margin as a share of selling price in the costing engine: `price = cost / (1 − margin)`. The prototype applies the ₹25 lakh approval threshold to pre-GST annual selling value; the source brief does not state the GST basis, so confirm before a pilot.
- Keep setup costs volume-sensitive and retain the rate snapshot used on the quote date.
- Model working capital from incremental receivables, inventory and payables rather than assuming revenue converts immediately to cash.
- Include a ramp-up curve; the benefit does not necessarily arrive on day one.
- Show sensitivities around loss attribution, win probability, order margin, capacity and implementation cost.
- Do not call Monte Carlo output the probability of success. It is conditional on the distributions and ranges selected by the analyst.
- Keep public-company valuation benchmarking in `MarginLadder_finance_extension.xlsx` separate from the internal-tool investment case. A DCF valuation of a listed peer is context, not evidence that MarginLadder will generate the same returns.

## 8. Investment recommendation logic

The case supports a staged recommendation only if the stage gates reduce the risk of building the wrong workflow. The extension model records that build-now has a higher expected NPV by about ₹2.6 lakh under its chosen scenario weights. Staging therefore does not win on expected value alone; its rationale is reversibility, learning and a narrower initial commitment. Management should change the recommendation if the Week 1 trace shows costing dominates the cycle, if delay is not a meaningful cause of lost business, or if plant capacity is constrained.
