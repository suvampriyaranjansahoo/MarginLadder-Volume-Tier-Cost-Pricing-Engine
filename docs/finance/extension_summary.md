# Market context and the finance extension

**This is a modelling exercise on public data, not a view on any stock.** It shows how the case behaves against real firms' ratios. It is not investment advice and is not endorsed by any company named.

Moved here from the README in v3. Text is unchanged from v2. External figures are tagged [External] and come from the linked pages; verify against filings before quoting.

## Market context and benchmarks
- Indian auto-component industry turnover was ₹7.60 lakh crore in FY26, up 12.7% ([ACMA, via Autocar Professional, 7 July 2026](https://www.autocarpro.in/news/acma-indian-auto-component-industry-grows-127-percent-to-inr-76-lakh-crore-in-fy26-133454)).
- Operating margin for 59 listed auto-component companies was 13.6% in FY26, flat on the year ([Elara Capital, via Kotak Neo](https://www.kotakneo.com/news/sectors/auto-ancillaries-fy26-revenue-growth-margins-elara-report/)). This case uses 12%, from the brief, which is 1.6 points below that peer figure. Listed firms are much larger than a small plant, so treat it as a sense check, not a match.
- I found no reliable independent source for the win-back rate after faster quoting. The results were vendor blogs. The 25% stays an assumption and the Risk tab tests a 0 to 50% range.

## Finance extension: a real company as a check
`model/MarginLadder_finance_extension.xlsx` (10 sheets, 860 formulas, no errors) tests the case against Endurance Technologies, a listed auto-component maker, and six listed peers. Financials come from [stockanalysis.com](https://stockanalysis.com/quote/nse/ENDURANCE/financials/income-statement/) and [screener.in](https://www.screener.in/company/ENDURANCE/consolidated/), cross-checked against the [company-reported FY26 results](https://www.autocarpro.in/news/endurance-techs-fy26-income-rises-26-percent-europe-growth-gets-acquisition-boost-132659).
- **Ratios:** five years of DuPont, ROIC, leverage, interest cover, cash conversion and implied capex.
- **DCF:** bear, base and bull cases at an 11.8% WACC (risk-free rate and beta sourced, equity premium assumed). Base value is ₹1,077 a share against a ₹2,520 price (bear ₹720, bull ₹1,379).
- **Reverse DCF:** the price implies a discount rate of about 8.1% on base-case cash flows, or about 39% yearly revenue growth for five years against an 18% four-year record that includes an acquisition. The sector trades far above what a 12% discount rate supports; Endurance is the cheapest of seven on EV to operating profit.
- **Peers:** Gabriel India, Sansera, Uno Minda, Bharat Forge, Sundram Fasteners and Sona BLW. Gabriel India's P/E is distorted by other income and a merger; the sheet explains why.
- **MarginLadder link:** the case assumed 45 working-capital days. Observed values run from −12 to 115, median 22. IRR is 76% at 45 days and never below 33% across the observed range.
- **Win-back:** the 25% is split into two factors, with a grid showing where the case fails.
- **Decision analysis:** a five-scenario decision tree and weighted scoring of seven options. Building now has an expected NPV of ₹27.7 lakh against ₹25.1 lakh staged; staging wins only if the chance of zero benefit is above about 35%. The plan stays staged for speed, reversibility and risk, and the Week 1 trace and capacity check test that risk directly.
- **Market sizing:** the recoverable pool across the industry is about ₹342 crore a year, under 0.1% of turnover. This fits an internal tool, not a product bet.

Context: a [BCG and ACMA study](https://www.autocarpro.in/news/resilience-gives-indias-auto-component-makers-a-competitive-edge-bcg-acma-study-134440) of 450 suppliers found the 75 most resilient earned 1.4 points more EBITDA margin in FY25 after early investment in technology and capacity. That is association, not cause, and it does not cover quoting.
