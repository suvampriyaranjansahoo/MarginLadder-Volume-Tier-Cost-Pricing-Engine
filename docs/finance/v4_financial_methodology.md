# V4 financial methodology

## Canonical decision model

`finance/investment.py` is V4's canonical incremental-investment model. `finance/full_model.py` remains a retained V3.5 Python twin of the existing workbook until the workbook is updated and reconciled in Stage 10; it is not the V4 decision source.

All inputs are hypothetical assumptions. Bharat Forge benchmarking, where retained, is separate reference information and is never MarginLadder actual performance.

## Incremental economics

The model separately calculates total RFQs, eligible RFQs, adoption, successful processing, control conversion, treatment conversion, conversion lift, gross incremental orders, cannibalisation, and net incremental orders. Incremental orders equal `(treatment orders - control orders) - cannibalised orders`, floored at zero. It does not equate recovered RFQs with incremental orders.

## Working capital and cash flow

For each active month: `AR = credit sales × DSO / 365`; `Inventory = relevant COGS × DIO / 365`; `AP = supplier purchases × DPO / 365`; `NWC = AR + Inventory - AP`; and `FCF = operating cash flow - capex - change in NWC`. The model retains opening and monthly closing NWC, exposes CCC only as a diagnostic, and releases NWC only through an explicit terminal flag.

## Appraisal and guardrails

The model calculates NPV, IRR, MIRR, cash payback, peak funding, launch delays, and a `do_not_invest` outcome. IRR returns `None` for multiple-sign-change cash flows rather than selecting an arbitrary root. Tax is applied only to positive operating earnings. Sensitivities must vary documented inputs, not outputs.
