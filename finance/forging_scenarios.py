"""Illustrative forging-economics sensitivity model for the local portfolio MVP.

This is deliberately a transparent scenario tool, not a Bharat Forge forecast or
an estimate of any real supplier's costs. Public Bharat Forge FY26 figures are
exposed separately as a range benchmark in ``public_benchmark``.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP

D = Decimal


def _money(value: Decimal) -> Decimal:
    return value.quantize(D("0.01"), rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class ForgingScenario:
    """All inputs are illustrative unit-economics assumptions."""

    steel_price_change_pct: Decimal = D("0")
    forging_yield_pct: Decimal = D("0.88")
    machining_cycle_min: Decimal = D("3.2")
    energy_cost_change_pct: Decimal = D("0")
    utilisation_pct: Decimal = D("0.78")
    working_capital_days: Decimal = D("45")

    def validate(self) -> None:
        if not D("-0.50") <= self.steel_price_change_pct <= D("0.50"):
            raise ValueError("steel_price_change_pct must be between -50% and 50%")
        if not D("0.50") <= self.forging_yield_pct <= D("0.99"):
            raise ValueError("forging_yield_pct must be between 50% and 99%")
        if not D("0.5") <= self.machining_cycle_min <= D("30"):
            raise ValueError("machining_cycle_min must be between 0.5 and 30 minutes")
        if not D("-0.50") <= self.energy_cost_change_pct <= D("1.00"):
            raise ValueError("energy_cost_change_pct must be between -50% and 100%")
        if not D("0.30") <= self.utilisation_pct <= D("1"):
            raise ValueError("utilisation_pct must be between 30% and 100%")
        if not D("0") <= self.working_capital_days <= D("365"):
            raise ValueError("working_capital_days must be between 0 and 365")


def calculate(scenario: ForgingScenario = ForgingScenario()) -> dict[str, str]:
    """Return JSON-friendly, labelled illustrative unit economics.

    The unit price and cost-driver baselines are invented for demonstration. The
    margin is contribution before corporate overhead, finance cost and tax.
    """
    scenario.validate()
    base_price, annual_volume = D("120"), D("180000")
    billet_input_per_good_unit = D("46.44")
    machining_at_base_cycle, energy_at_base, other_conversion = D("12"), D("5"), D("16")

    material = billet_input_per_good_unit * (D("1") + scenario.steel_price_change_pct) / scenario.forging_yield_pct
    machining = machining_at_base_cycle * scenario.machining_cycle_min / D("3.2")
    energy = energy_at_base * (D("1") + scenario.energy_cost_change_pct)
    unit_cost = material + machining + energy + other_conversion
    unit_contribution = base_price - unit_cost
    margin_pct = unit_contribution / base_price
    annual_contribution = unit_contribution * annual_volume * scenario.utilisation_pct
    annual_revenue_at_utilisation = base_price * annual_volume * scenario.utilisation_pct
    working_capital = annual_revenue_at_utilisation * scenario.working_capital_days / D("365")

    if unit_contribution <= 0:
        recommendation = "Defer: the illustrative scenario has negative unit contribution."
    elif margin_pct < D("0.10"):
        recommendation = "Defer: validate price, yield and material assumptions before a pilot."
    elif scenario.utilisation_pct < D("0.60"):
        recommendation = "Pilot: contribution is positive, but utilisation needs evidence before scaling."
    else:
        recommendation = "Pilot: validate trace data and signed rates before any scale decision."

    return {
        "classification": "Illustrative scenario arithmetic; not Bharat Forge costs, forecasts or client results.",
        "unit_price_inr": str(_money(base_price)),
        "material_cost_inr": str(_money(material)),
        "machining_cost_inr": str(_money(machining)),
        "energy_cost_inr": str(_money(energy)),
        "other_conversion_cost_inr": str(_money(other_conversion)),
        "unit_cost_inr": str(_money(unit_cost)),
        "unit_contribution_inr": str(_money(unit_contribution)),
        "contribution_margin_pct": str((margin_pct * D("100")).quantize(D("0.1"))),
        "annual_contribution_inr": str(_money(annual_contribution)),
        "working_capital_tied_inr": str(_money(working_capital)),
        "recommendation": recommendation,
    }


def public_benchmark() -> dict[str, object]:
    """Public FY26 range reference. Source and limits are returned with the data."""
    return {
        "classification": "Public benchmark only; independent portfolio case, not affiliated with Bharat Forge.",
        "source": "docs/finance/real_company_benchmark.md (Bharat Forge FY26 audited consolidated filing)",
        "metrics": [
            {"metric": "EBITDA margin", "value": "17.4%", "comparison": "Case quote margin: 12%; not like-for-like."},
            {"metric": "Forgings segment margin", "value": "14.0%", "comparison": "A public segment range reference, not a price target."},
            {"metric": "Material share of revenue", "value": "45.1%", "comparison": "Case sample part: 38.7% of price."},
            {"metric": "Receivable days", "value": "85 days", "comparison": "Case working-capital assumption: 45 days."},
            {"metric": "Cash conversion cycle", "value": "136 days", "comparison": "Stress test, not a forecast for the case."},
        ],
        "limits": "One large, export-heavy company and one audited year; do not infer internal operations or apply values as case facts.",
    }


def scenario_dict(**values: str | float | int | Decimal) -> dict[str, str]:
    """Build a validated scenario from API input without float arithmetic."""
    clean = {name: D(str(value)) for name, value in values.items() if value is not None}
    return calculate(ForgingScenario(**clean))


def defaults() -> dict[str, str]:
    return {key: str(value) for key, value in asdict(ForgingScenario()).items()}
