# MarginLadder v2 upgrade and regression report

## Change strategy

The v2 work was added on top of a fresh copy of the supplied ZIP. The root README was extended to document the new application and run steps; every other original file—the three HTML prototypes, Python costing engine, two Excel workbooks, simulated RFQ file, product / BA documents, images, GIF and PDF—was retained byte-for-byte. New application and documentation files were added alongside them.

## Added capabilities

- FastAPI local application and responsive workspace UI.
- SQLite persistence for RFQs, quote versions and audit events.
- Search and status filtering for the RFQ register.
- Controlled RFQ lifecycle transitions, including Plant Head routing clearance.
- Quote calculation for all three existing volume tiers through the original costing engine.
- Persisted quote input / formula / effective-rate snapshots.
- Sales Head / Deputy approval and reasoned send-back workflow.
- Approved-only quote send action and print-friendly quotation output.
- Dashboard cards for local demo records and a separately labelled synthetic cycle-time diagnostic.
- Independently testable finance arithmetic in Python.
- Expanded PRD, KPI dictionary, event taxonomy, experiment plan, finance methodology, architecture and role-positioning guide.

## Test results

| Suite | Result | What it covers |
|---|---:|---|
| Original costing engine | 24 / 24 passed | Pricing formula, rounding, rate validity, deterministic output, approval threshold boundary |
| New service + API tests | 27 / 27 passed | RFQ creation, owner / due-date edits, role gates, status transitions, multi-line quote snapshots, three tiers, approval, send-back, send and audit behaviour |
| New finance arithmetic tests | 5 / 5 passed | Brief arithmetic, payback distinctions, capacity bridge, monotonic scenarios and input validation |
| **Total** | **56 / 56 passed** | Original and new automated checks |

Commands:

```bash
python3 engine/cost_engine.py
python3 -m pytest -q application/tests finance/test_case_model.py
```

## Regression / downgrade review

- Existing costing engine file unchanged; its original 24 tests pass.
- Existing finance workbooks unchanged; no sheets or formulas were overwritten.
- Existing original prototypes remain available and linked from the v2 workspace.
- Existing simulated data was not modified and is still labelled synthetic.
- Existing assumptions and original business-review conclusions were not silently replaced.
- New application imports and calls the original engine rather than copying or reimplementing its formulas.
- New finance script reproduces only the simple brief arithmetic; it does not replace the Excel model's tax, working-capital, DCF, NPV or IRR schedules.

## Known limitations — not a production sign-off

- Role is provided by the local browser dropdown, not a verified identity; it can be spoofed.
- SQLite is local demo persistence, not a production deployment architecture.
- No file upload / secure drawing storage, real AI extraction, ERP/CRM integration, email reminders or scheduled escalation.
- Seeded RFQs and sample rates are fictional / illustrative.
- Quote parity against a real customer's signed-off Excel is still an open gate.
- The print view uses browser Print / Save as PDF, not a generated digitally signed customer quote.
- No live adoption, turnaround improvement, recovered revenue or realised savings have been measured.

## Release recommendation

Use v2 as a portfolio demonstration and a foundation for interviews. Do not describe it as production-ready or as evidence of customer outcomes. The next product build should prioritise identity / access controls and real baseline / parity validation before adding AI or ERP integrations.
