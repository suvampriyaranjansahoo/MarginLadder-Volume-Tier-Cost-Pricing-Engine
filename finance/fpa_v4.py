"""Driver-based planning and reconciled variance bridges for illustrative data."""
from __future__ import annotations


def plan(units: float, unit_price: float, unit_material: float, unit_labour: float, fixed_overhead: float, working_capital_pct: float) -> dict[str, float]:
    if min(units, unit_price, unit_material, unit_labour, fixed_overhead, working_capital_pct) < 0:
        raise ValueError("planning drivers cannot be negative")
    revenue = units * unit_price
    variable_cost = units * (unit_material + unit_labour)
    contribution = revenue - variable_cost
    return {"units": units, "revenue": revenue, "material": units * unit_material, "labour": units * unit_labour,
            "fixed_overhead": fixed_overhead, "contribution": contribution, "operating_profit": contribution - fixed_overhead,
            "working_capital_forecast": revenue * working_capital_pct}


def sales_variance_bridge(budget_units: float, actual_units: float, budget_price: float, actual_price: float) -> dict[str, float]:
    volume = (actual_units - budget_units) * budget_price
    price = actual_units * (actual_price - budget_price)
    total = actual_units * actual_price - budget_units * budget_price
    return {"volume_variance": volume, "price_variance": price, "total_variance": total, "bridge_check": volume + price - total}
