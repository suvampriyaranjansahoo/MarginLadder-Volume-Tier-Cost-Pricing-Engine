# MarginLadder V4 execution pack

## Stages 3–4: costing and FP&A

`finance/costing_v4.py` adds a traceable waterfall: material, conversion, scrap recovery, rejection/rework, reinspection, additional setup, tooling, rush premium, overhead, packing, freight, target price, discount, and post-discount contribution. The retained engine is unchanged to protect existing quote snapshots. `finance/fpa_v4.py` provides driver-based planning, working-capital forecast and a sales price/volume bridge that must reconcile to total variance. These additions use illustrative inputs only.

## Stage 5: product management

Vision: help manufacturing quote teams produce timely, traceable RFQ decisions without representing simulated outcomes as actuals. Target users are estimator, RFQ coordinator, sales manager, finance manager, approver, and operations manager. Assumptions remain unvalidated until research is actually conducted.

The delivery sequence is: Phase 1 RFQ intake/costing; Phase 2 approvals and workflow visibility; Phase 3 profitability and decision intelligence. No production research, experiment, pilot, or UAT outcome is claimed. Existing discovery guides, experiment plans and PRD are retained as templates; `docs/product/PRD_v3.md` is the current detailed specification pending V4 traceability completion.

## Stage 6: business analysis

Canonical lifecycle: Received → Intake → Validation → Assignment → Costing → Review → Approval → Quote generation → Dispatch → Customer response → Won/Lost/Expired. Each transition needs an owner, timestamp, entry/exit criteria, SLA, exception and rework reason. The existing service persists lifecycle/audit records; existing BA documents provide use cases, data dictionary and UAT scripts. Scripts are not executed UAT and are not sign-off.

## Stage 8: product analytics

`analytics/event_contract.py` specifies canonical events and rejects incomplete records. Funnel denominators use observed prerequisite events only; incomplete lifecycles are not zero-duration records. Required metrics (median/P90 cycle time, stage duration, approval delay, rework, SLA, workload, revision, adoption and contribution) must identify source, numerator/denominator, null treatment and limitations before release.

## Stage 9: consulting and PMO

Recommendation framework: compare manual improvement, limited automation, workflow-first, staged investment, and full automation against incremental NPV, operational risk, dependency and reversible-learning criteria. The model is allowed to recommend `do_not_invest`. Existing PMO plan, RAID, RACI, change control and consulting deck are planning artefacts; completion is not claimed without executed evidence.

## Stage 10: source of truth and reconciliation

| Metric | Canonical V4 source | Current status |
|---|---|---|
| Unit cost / selling price / contribution | `engine.cost_engine` plus `finance/costing_v4` for new lines | Existing engine retained; extension Python-only |
| Incremental orders / NWC / NPV / IRR | `finance/investment.py` | V4 Python canonical; workbook update pending |
| Variance | `finance.variance` / `finance.fpa_v4` | Illustrative sample only |
| Application lifecycle | SQLite audit events | Local demo data only |
| Product funnel | `analytics.event_contract.py` | Contract added; application mapping pending |

The existing 64 Python/Excel checks pass against the unchanged legacy workbook. That is preservation evidence, not V4 workbook reconciliation. Excel/dashboard changes are intentionally deferred rather than fabricated.
