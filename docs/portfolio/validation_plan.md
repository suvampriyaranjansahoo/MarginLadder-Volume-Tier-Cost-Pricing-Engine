# Validation plan: turning a modelled case into evidence

Goal: replace the largest assumptions with observations. Do not invent or back-fill any result; log what people say.

## Who to talk to (3 to 5 people, 20 to 30 minutes each)
- An estimator or costing engineer (stage times, rework, how a quote is built today)
- Someone in sales or key accounts (why RFQs are lost; customer price comparisons)
- Someone in finance or procurement (margin, approval thresholds)

Friends of friends, LinkedIn contacts in manufacturing, or college alumni all work. Say plainly that it is a student project.

## Questions, mapped to the assumption each one tests
| Assumption in the model | Ask |
|---|---|
| Lost-RFQ rate 5% | Roughly what share of quotes are lost, and how many are lost on price versus speed? |
| Win-back 25% | If you quoted two days faster, would any lost deals have been won? How many? |
| 9-day cycle, 2.5 h per part | Where does an RFQ wait? Who touches it? How long is hands-on costing? |
| Approval threshold (₹25 lakh, illustrative) | When does a quote need sign-off, and how long does that take? |
| Rework | How often is a quote revised after internal review? |

## How to log
Use `data/templates/discovery_interview_log_template.csv`. Record the date, role, company type (anonymised unless
permitted), the answer in their words, and which model input it affects. Mark every row `observed` or `opinion`.

## After the interviews
1. Update the inputs in `numbers.json` and the workbook only where an observation supports it; tag them Observed.
2. Re-run `python -m finance.reconcile` and `python scripts/check_consistency.py`.
3. Add a short "What I learned" note and update `docs/portfolio/evidence_ledger.md`: move claims from Unverified only
   for what was actually observed. Even three interviews is "early qualitative evidence", not validation of the market.
