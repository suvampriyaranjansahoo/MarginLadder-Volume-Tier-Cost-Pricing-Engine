"""Transparent, assumption-tagged arithmetic for the MarginLadder business case.

This model intentionally reproduces the simple economics in the project brief.
It does not replace the Excel model's tax, working-capital, DCF or IRR schedules.
All currency amounts are INR and Decimal is used to avoid binary-float drift.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

D = Decimal


def money(value: Decimal) -> Decimal:
    return value.quantize(D("0.01"), rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class CaseInputs:
    # Values labelled Brief are supplied by the hypothetical client brief.
    rfqs_per_month: int = 60                         # Brief
    months_per_year: int = 12                        # Calendar convention
    parts_per_rfq: int = 5                           # Brief
    estimator_count: int = 6                         # Brief
    costing_hours_per_part: Decimal = D("2.5")     # Brief
    target_hours_per_part: Decimal = D("1.0")      # Brief target
    estimator_hourly_cost: Decimal = D("450")      # Brief
    lost_rfq_rate: Decimal = D("0.05")              # Brief
    average_order_value: Decimal = D("2000000")    # Brief
    order_margin: Decimal = D("0.12")               # Brief
    delay_related_loss_share: Decimal = D("0.50") # Assumption
    faster_quote_win_rate: Decimal = D("0.50")     # Assumption
    development_fee: Decimal = D("800000")         # Proposed fee
    annual_run_cost: Decimal = D("200000")         # Assumption

    def validate(self) -> None:
        for name in ("rfqs_per_month", "months_per_year", "parts_per_rfq", "estimator_count"):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")
        for name in ("costing_hours_per_part", "target_hours_per_part", "estimator_hourly_cost", "average_order_value"):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")
        for name in ("lost_rfq_rate", "order_margin", "delay_related_loss_share", "faster_quote_win_rate"):
            value = getattr(self, name)
            if value < 0 or value > 1:
                raise ValueError(f"{name} must be between 0 and 1")
        if self.target_hours_per_part > self.costing_hours_per_part:
            raise ValueError("target costing time cannot exceed current costing time")
        if self.development_fee < 0 or self.annual_run_cost < 0:
            raise ValueError("investment and running cost cannot be negative")


@dataclass(frozen=True)
class CaseOutputs:
    annual_rfqs: int
    annual_lost_rfqs: Decimal
    lost_rfq_margin_pool: Decimal
    assumed_win_back_rate: Decimal
    annual_recovered_margin: Decimal
    annual_net_benefit_after_run_cost: Decimal
    gross_margin_payback_months: Decimal | None
    operating_payback_after_run_cost_months: Decimal | None
    break_even_win_back_rate_including_one_year_run_cost: Decimal
    current_estimator_hours: Decimal
    target_estimator_hours: Decimal
    annual_hours_released: Decimal
    theoretical_capacity_value: Decimal


def calculate(inputs: CaseInputs = CaseInputs(), win_back_rate: Decimal | None = None) -> CaseOutputs:
    inputs.validate()
    effective_win_back = (
        inputs.delay_related_loss_share * inputs.faster_quote_win_rate
        if win_back_rate is None else D(str(win_back_rate))
    )
    if effective_win_back < 0 or effective_win_back > 1:
        raise ValueError("win_back_rate must be between 0 and 1")

    annual_rfqs = inputs.rfqs_per_month * inputs.months_per_year
    lost_rfqs = D(annual_rfqs) * inputs.lost_rfq_rate
    margin_pool = lost_rfqs * inputs.average_order_value * inputs.order_margin
    recovered = margin_pool * effective_win_back
    net_benefit = recovered - inputs.annual_run_cost
    gross_payback = (inputs.development_fee / recovered * D(12)) if recovered > 0 else None
    operating_payback = (inputs.development_fee / net_benefit * D(12)) if net_benefit > 0 else None
    break_even = (inputs.development_fee + inputs.annual_run_cost) / margin_pool if margin_pool > 0 else D(0)

    current_hours = D(annual_rfqs * inputs.parts_per_rfq) * inputs.costing_hours_per_part
    target_hours = D(annual_rfqs * inputs.parts_per_rfq) * inputs.target_hours_per_part
    hours_released = current_hours - target_hours
    capacity_value = hours_released * inputs.estimator_hourly_cost

    return CaseOutputs(
        annual_rfqs=annual_rfqs,
        annual_lost_rfqs=lost_rfqs,
        lost_rfq_margin_pool=money(margin_pool),
        assumed_win_back_rate=effective_win_back,
        annual_recovered_margin=money(recovered),
        annual_net_benefit_after_run_cost=money(net_benefit),
        gross_margin_payback_months=money(gross_payback) if gross_payback is not None else None,
        operating_payback_after_run_cost_months=money(operating_payback) if operating_payback is not None else None,
        break_even_win_back_rate_including_one_year_run_cost=break_even,
        current_estimator_hours=current_hours,
        target_estimator_hours=target_hours,
        annual_hours_released=hours_released,
        theoretical_capacity_value=money(capacity_value),
    )


def scenario_table(rates: Iterable[Decimal] = (D("0.05"), D("0.125"), D("0.25"), D("0.50"))) -> list[dict[str, str]]:
    rows = []
    for rate in rates:
        result = calculate(win_back_rate=rate)
        rows.append({
            "win_back_rate": f"{rate:.1%}",
            "annual_recovered_margin_inr": str(result.annual_recovered_margin),
            "annual_net_benefit_after_run_cost_inr": str(result.annual_net_benefit_after_run_cost),
            "operating_payback_months": (
                str(result.operating_payback_after_run_cost_months)
                if result.operating_payback_after_run_cost_months is not None else "Not reached"
            ),
        })
    return rows


def output_dict(inputs: CaseInputs = CaseInputs()) -> dict[str, str | int | None]:
    """JSON-friendly output for scripts and notebooks."""
    return {key: (str(value) if isinstance(value, Decimal) else value)
            for key, value in asdict(calculate(inputs)).items()}


if __name__ == "__main__":
    result = calculate()
    print("MarginLadder base case (Brief + explicitly tagged assumptions)")
    print(f"Annual RFQs: {result.annual_rfqs:,}")
    print(f"Lost RFQs: {result.annual_lost_rfqs:,.1f}")
    print(f"Lost-RFQ margin pool: ₹{result.lost_rfq_margin_pool:,.2f}")
    print(f"Assumed win-back: {result.assumed_win_back_rate:.1%}")
    print(f"Annual recovered margin: ₹{result.annual_recovered_margin:,.2f}")
    print(f"Annual net benefit after run cost: ₹{result.annual_net_benefit_after_run_cost:,.2f}")
    print(f"Payback, before run cost: {result.gross_margin_payback_months} months")
    print(f"Operating payback, after run cost: {result.operating_payback_after_run_cost_months} months")
    print(f"Break-even win-back incl. one run-cost year: {result.break_even_win_back_rate_including_one_year_run_cost:.2%}")
    print(f"Hours released: {result.annual_hours_released:,.0f}; capacity value, not booked cash savings: ₹{result.theoretical_capacity_value:,.2f}")
    print("\nScenario table")
    for row in scenario_table():
        print(" | ".join(row.values()))
