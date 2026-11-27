"""Canonical V4 investment model.

All values are hypothetical case assumptions, not MarginLadder or Bharat Forge actuals.
This module is deliberately independent of the legacy Excel-twin model so that a
methodology correction does not silently rewrite the retained v3.5 workbook.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import copysign


@dataclass(frozen=True)
class InvestmentInputs:
    total_rfqs: int = 720
    eligible_share: float = 1.0
    adoption_rate: float = 1.0
    successful_processing_rate: float = 1.0
    control_conversion: float = 0.0
    treatment_conversion: float = 0.05
    average_order_value: float = 2_000_000.0
    contribution_margin: float = 0.12
    cannibalisation_rate: float = 0.0
    annual_run_cost: float = 200_000.0
    implementation_capex: float = 800_000.0
    tax_rate: float = 0.25
    discount_rate: float = 0.12
    dso: float = 45.0
    dio: float = 30.0
    dpo: float = 30.0
    launch_delay_months: int = 0
    years: int = 3
    terminal_nwc_release: bool = True

    def validate(self) -> None:
        if self.total_rfqs < 0 or self.years < 1 or not 0 <= self.launch_delay_months < self.years * 12:
            raise ValueError("RFQs/years/delay are invalid")
        for name in ("eligible_share", "adoption_rate", "successful_processing_rate", "control_conversion", "treatment_conversion", "contribution_margin", "cannibalisation_rate", "tax_rate"):
            if not 0 <= getattr(self, name) <= 1:
                raise ValueError(f"{name} must be between 0 and 1")
        for name in ("average_order_value", "annual_run_cost", "implementation_capex", "discount_rate", "dso", "dio", "dpo"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} cannot be negative")


def incremental_orders(inputs: InvestmentInputs) -> dict[str, float]:
    """Transparent counterfactual: treatment lift, not all recovered RFQs."""
    inputs.validate()
    eligible = inputs.total_rfqs * inputs.eligible_share
    processed = eligible * inputs.adoption_rate * inputs.successful_processing_rate
    control = processed * inputs.control_conversion
    treatment = processed * inputs.treatment_conversion
    gross_incremental = max(0.0, treatment - control)
    cannibalised = gross_incremental * inputs.cannibalisation_rate
    return {"total_rfqs": inputs.total_rfqs, "eligible_rfqs": eligible, "processed_rfqs": processed,
            "control_orders": control, "treatment_orders": treatment, "conversion_lift": inputs.treatment_conversion - inputs.control_conversion,
            "gross_incremental_orders": gross_incremental, "cannibalised_orders": cannibalised,
            "incremental_orders": gross_incremental - cannibalised}


def working_capital(credit_sales: float, relevant_cogs: float, supplier_purchases: float, inputs: InvestmentInputs) -> dict[str, float]:
    """Closing balances. CCC is reported only as a diagnostic, never used as a proxy."""
    inputs.validate()
    ar = credit_sales * inputs.dso / 365
    inventory = relevant_cogs * inputs.dio / 365
    ap = supplier_purchases * inputs.dpo / 365
    return {"accounts_receivable": ar, "inventory": inventory, "accounts_payable": ap,
            "net_working_capital": ar + inventory - ap, "cash_conversion_cycle_days": inputs.dso + inputs.dio - inputs.dpo}


def npv(cash_flows: list[float], rate: float) -> float:
    if rate <= -1:
        raise ValueError("discount rate must exceed -100%")
    return sum(cf / (1 + rate) ** period for period, cf in enumerate(cash_flows))


def _sign_changes(cash_flows: list[float]) -> int:
    nonzero = [x for x in cash_flows if x != 0]
    return sum(a * b < 0 for a, b in zip(nonzero, nonzero[1:], strict=False))


def irr(cash_flows: list[float]) -> float | None:
    """Bisection IRR only when there is one economic root; ambiguous multiple-IRR cases return None."""
    if _sign_changes(cash_flows) != 1:
        return None
    lo, hi = -0.999999, 1.0
    flo, fhi = npv(cash_flows, lo), npv(cash_flows, hi)
    while flo * fhi > 0 and hi < 1_000_000:
        hi *= 2
        fhi = npv(cash_flows, hi)
    if flo * fhi > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        fmid = npv(cash_flows, mid)
        if abs(fmid) < 1e-9:
            return mid
        if copysign(1, flo) == copysign(1, fmid):
            lo, flo = mid, fmid
        else:
            hi = mid
    return (lo + hi) / 2


def mirr(cash_flows: list[float], finance_rate: float, reinvestment_rate: float) -> float | None:
    if len(cash_flows) < 2 or not any(cf < 0 for cf in cash_flows) or not any(cf > 0 for cf in cash_flows):
        return None
    n = len(cash_flows) - 1
    pv_negative = sum(cf / (1 + finance_rate) ** i for i, cf in enumerate(cash_flows) if cf < 0)
    fv_positive = sum(cf * (1 + reinvestment_rate) ** (n - i) for i, cf in enumerate(cash_flows) if cf > 0)
    return (-fv_positive / pv_negative) ** (1 / n) - 1


def cash_payback(cash_flows: list[float]) -> float | None:
    cumulative = cash_flows[0]
    for period, value in enumerate(cash_flows[1:], start=1):
        before = cumulative
        cumulative += value
        if before < 0 <= cumulative and value != 0:
            return (period - 1) + (-before / value)
    return 0.0 if cumulative >= 0 else None


def monthly_cash_flow(inputs: InvestmentInputs = InvestmentInputs()) -> list[dict[str, float | int]]:
    """Monthly operating cash flow, NWC balances and FCF; terminal NWC release is explicit."""
    inputs.validate()
    economics = incremental_orders(inputs)
    annual_revenue = economics["incremental_orders"] * inputs.average_order_value
    annual_contribution = annual_revenue * inputs.contribution_margin
    annual_cogs = annual_revenue - annual_contribution
    rows, opening_nwc = [], 0.0
    for month in range(0, inputs.years * 12 + 1):
        active = month > inputs.launch_delay_months
        revenue = annual_revenue / 12 if active else 0.0
        contribution = annual_contribution / 12 if active else 0.0
        cogs = annual_cogs / 12 if active else 0.0
        run_cost = inputs.annual_run_cost / 12 if active else 0.0
        ebit = contribution - run_cost
        tax = max(0.0, ebit * inputs.tax_rate)
        operating_cash_flow = ebit - tax
        balances = working_capital(revenue * 12, cogs * 12, cogs * 12, inputs) if active else working_capital(0, 0, 0, inputs)
        closing_nwc = 0.0 if month == inputs.years * 12 and inputs.terminal_nwc_release else balances["net_working_capital"]
        change_nwc = closing_nwc - opening_nwc
        capex = inputs.implementation_capex if month == 0 else 0.0
        fcf = operating_cash_flow - capex - change_nwc
        rows.append({"month": month, "revenue": revenue, "contribution": contribution, "cogs": cogs, "run_cost": run_cost,
                     "tax": tax, "operating_cash_flow": operating_cash_flow, "accounts_receivable": balances["accounts_receivable"],
                     "inventory": balances["inventory"], "accounts_payable": balances["accounts_payable"], "closing_nwc": closing_nwc,
                     "change_nwc": change_nwc, "capex": capex, "free_cash_flow": fcf})
        opening_nwc = closing_nwc
    return rows


def evaluate(inputs: InvestmentInputs = InvestmentInputs()) -> dict[str, object]:
    rows = monthly_cash_flow(inputs)
    flows = [float(row["free_cash_flow"]) for row in rows]
    annual_flows = [sum(flows[y * 12:(y + 1) * 12]) for y in range(inputs.years + 1)]
    annual_rate = inputs.discount_rate
    return {"economics": incremental_orders(inputs), "monthly": rows, "annual_free_cash_flow": annual_flows,
            "npv": npv(annual_flows, annual_rate), "irr": irr(annual_flows),
            "mirr": mirr(annual_flows, annual_rate, annual_rate), "cash_payback_years": cash_payback(annual_flows),
            "peak_funding": -min(0.0, min(__import__('itertools').accumulate(flows))),
            "recommendation": "invest" if npv(annual_flows, annual_rate) > 0 else "do_not_invest"}
