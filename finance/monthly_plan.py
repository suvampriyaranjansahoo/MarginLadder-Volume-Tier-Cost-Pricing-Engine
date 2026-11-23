"""Driver-based monthly operating plan for the MarginLadder hypothetical case.

All outputs are planning calculations derived from the hypothetical case brief and
explicit assumptions. They are not actuals, an approved operating budget, an
integrated three-statement forecast, or evidence of realised benefits.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

D = Decimal


def _d(value: Decimal | int | float | str) -> Decimal:
    return value if isinstance(value, Decimal) else D(str(value))


def _money(value: Decimal) -> Decimal:
    return value.quantize(D("0.01"), rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class MonthlyPlanInputs:
    months: int = 12
    rfqs_per_month: Decimal = D("60")
    lost_rfq_rate: Decimal = D("0.05")
    average_order_value: Decimal = D("2000000")
    contribution_margin: Decimal = D("0.12")
    win_back_rate: Decimal = D("0.25")
    annual_run_cost: Decimal = D("200000")
    implementation_cost: Decimal = D("800000")

    def validate(self) -> None:
        if self.months <= 0:
            raise ValueError("months must be positive")
        for name in ("rfqs_per_month", "average_order_value"):
            if _d(getattr(self, name)) <= 0:
                raise ValueError(f"{name} must be positive")
        for name in ("lost_rfq_rate", "contribution_margin", "win_back_rate"):
            value = _d(getattr(self, name))
            if value < 0 or value > 1:
                raise ValueError(f"{name} must be between 0 and 1")
        for name in ("annual_run_cost", "implementation_cost"):
            if _d(getattr(self, name)) < 0:
                raise ValueError(f"{name} cannot be negative")


@dataclass(frozen=True)
class MonthlyPeriod:
    period: int
    rfqs: Decimal
    lost_rfqs: Decimal
    assumed_recovered_rfqs: Decimal
    incremental_revenue: Decimal
    contribution: Decimal
    run_cost: Decimal
    net_contribution_after_run_cost: Decimal
    one_time_setup_cost: Decimal
    project_cash_proxy: Decimal
    cumulative_project_cash_proxy: Decimal


def build_monthly_plan(inputs: MonthlyPlanInputs = MonthlyPlanInputs()) -> list[MonthlyPeriod]:
    """Return a flat-volume 12-period plan; one-time setup cost is charged in period 1."""
    inputs.validate()
    monthly_run_cost = _d(inputs.annual_run_cost) / D(inputs.months)
    periods: list[MonthlyPeriod] = []
    cumulative = D("0")
    run_cost_booked = D("0")
    for period in range(1, inputs.months + 1):
        rfqs = _d(inputs.rfqs_per_month)
        lost = rfqs * _d(inputs.lost_rfq_rate)
        recovered = lost * _d(inputs.win_back_rate)
        revenue = recovered * _d(inputs.average_order_value)
        contribution = revenue * _d(inputs.contribution_margin)
        run_cost = _money(monthly_run_cost) if period < inputs.months else _money(_d(inputs.annual_run_cost) - run_cost_booked)
        run_cost_booked += run_cost
        net = contribution - run_cost
        setup = _d(inputs.implementation_cost) if period == 1 else D("0")
        project_cash = net - setup
        cumulative += project_cash
        periods.append(MonthlyPeriod(
            period=period,
            rfqs=_money(rfqs),
            lost_rfqs=_money(lost),
            assumed_recovered_rfqs=_money(recovered),
            incremental_revenue=_money(revenue),
            contribution=_money(contribution),
            run_cost=run_cost,
            net_contribution_after_run_cost=_money(net),
            one_time_setup_cost=_money(setup),
            project_cash_proxy=_money(project_cash),
            cumulative_project_cash_proxy=_money(cumulative),
        ))
    return periods


def summary(inputs: MonthlyPlanInputs = MonthlyPlanInputs()) -> dict[str, Decimal | int | None]:
    """Return headline annual outputs and operating payback, with rounded amounts."""
    periods = build_monthly_plan(inputs)
    annual_rfqs = sum((p.rfqs for p in periods), D("0"))
    annual_lost_rfqs = sum((p.lost_rfqs for p in periods), D("0"))
    lost_margin_pool = annual_lost_rfqs * _d(inputs.average_order_value) * _d(inputs.contribution_margin)
    recovered_contribution = sum((p.contribution for p in periods), D("0"))
    annual_run_cost = _d(inputs.annual_run_cost)
    annual_net = recovered_contribution - annual_run_cost
    payback = (_d(inputs.implementation_cost) / annual_net * D(12)) if annual_net > 0 else None
    break_even_win_back = (
        (_d(inputs.implementation_cost) + annual_run_cost) / lost_margin_pool
        if lost_margin_pool > 0 else None
    )
    return {
        "annual_rfqs": int(annual_rfqs),
        "annual_lost_rfqs": _money(annual_lost_rfqs),
        "lost_rfq_margin_pool": _money(lost_margin_pool),
        "annual_recovered_contribution": _money(recovered_contribution),
        "annual_net_contribution_after_run_cost": _money(annual_net),
        "operating_payback_months": _money(payback) if payback is not None else None,
        "break_even_win_back_rate": break_even_win_back,
        "year_end_project_cash_proxy": periods[-1].cumulative_project_cash_proxy,
    }


if __name__ == "__main__":
    result = summary()
    print("SIMULATED / ASSUMPTION-DRIVEN CASE — not actuals")
    for key, value in result.items():
        print(f"{key}: {value}")
