# Resume bullets and interview preparation

Use "modelled", "built" and "tested locally". Never "saved", "recovered", "reduced" or "deployed".

## Resume bullets (pick 3)
- Built a driver-based monthly FP&A model (about 490 formulas) for a hypothetical RFQ-automation investment; reconciled it
  to a Python twin (64 of 64 cells) and separated 4.9-month operating payback from 23.6-month cash payback.
- Modelled a ₹86.4 lakh lost-RFQ margin pool and a break-even win-back of 11.6%, with tornado sensitivity and an
  IRR shown with and without working-capital release (75.8% / 43.0%).
- Developed a FastAPI + SQLite RFQ workflow prototype with role-gated approvals and audit events, and a Decimal costing
  engine, covered by pytest, ruff, mypy and CI with an 85% coverage gate.
- Wrote a claim-by-claim evidence ledger and AI-use disclosure that tags every figure Brief, Assumption, Derived or
  Synthetic; recommended measuring before building.

Role tuning: for finance, lead with bullets 1 and 2; for product or BA, lead with 4 and 3; for supply chain or
operations analytics, lead with the capacity and queue model (78% to 31% estimator load, 0.57-day wait).

## Thirty-second pitch
"It is a hypothetical case about whether a manufacturer should spend ₹8 lakh automating quotes. I modelled the lost-margin
pool, showed that a 4.9-month payback becomes 23.6 months once tax and working capital are included, and recommended
measuring first. I built a working prototype too, but I'm clear that no real users have touched it."

## Questions to expect
**How did you get ₹86.4 lakh?** 720 RFQs × 5% = 36 lost; 36 × ₹20 lakh × 12% = ₹86.4 lakh. It is a ceiling because it
assumes every lost RFQ could have been won at full margin.

**Why is ₹21.6 lakh not a saving?** It is 25% of the pool under an assumed win-back rate nobody has observed. It would
be revenue-side contribution, and only if speed is why RFQs are lost.

**Why is cash payback so much longer than operating payback?** Operating payback is pre-tax and ignores working capital.
The cash model adds both, and the deepest cash need (₹14.8 lakh) exceeds the ₹8 lakh fee.

**Is the 75.8% IRR reliable?** It depends on a working-capital release assumption; without it, 43.0%. I would quote the
lower number first.

**Why not recommend building it?** Break-even win-back is 11.6% and the 25% base is an assumption. The 9-day cycle
has only about 1.56 days of hands-on costing; the other 7.44 days is an unexplained residual, so measure where it goes.

**What would change your mind?** See `one_page_brief.md`: observed win-back below break-even, timestamps showing costing is
a small share of the delay, or rework data showing costing errors drive losses.

**Did users test it?** No. UAT scripts exist but have not been executed, the data is synthetic, and it is a local demo.
Then say what you would do next: `validation_plan.md`.

**Which part did AI help with?** See `ai_use_disclosure.md`. Be ready to explain every formula yourself.
