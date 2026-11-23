"""Capacity-constrained benefit: can the plant make the orders a faster quote wins back?

The base case counts 12% margin on every recovered order. If the plant is full, a won order
displaces another order and the net gain is smaller. Plant revenue and spare capacity are
unknown (Week 1 question to the plant head), so this module returns a grid, not an estimate.
"""
from __future__ import annotations

from finance.case_model import CaseInputs, calculate
from decimal import Decimal as D


def recovered_revenue(win_back: float = 0.25, inputs: CaseInputs = CaseInputs()) -> float:
    lost = float(calculate(inputs).annual_lost_rfqs)
    return lost * win_back * float(inputs.average_order_value)


def fit_share(extra_revenue: float, plant_revenue: float, spare_capacity_share: float) -> float:
    """Share of the won-back orders the plant can make from spare capacity (0 to 1)."""
    if plant_revenue <= 0 or extra_revenue < 0 or not 0 <= spare_capacity_share <= 1:
        raise ValueError("plant revenue must be positive, extra revenue non-negative, spare share in [0,1]")
    if extra_revenue == 0:
        return 1.0
    return min(1.0, spare_capacity_share * plant_revenue / extra_revenue)


def realised_margin(recovered_margin: float, fit: float, displaced_margin_ratio: float = 1.0) -> float:
    """Margin kept after displacement. Orders that do not fit displace others.

    displaced_margin_ratio = margin of the displaced order / margin of the won-back order.
    At 1.0 the displaced order was just as profitable, so the unfitted part adds nothing.
    """
    if not 0 <= fit <= 1 or not 0 <= displaced_margin_ratio <= 1:
        raise ValueError("fit and displaced_margin_ratio must be in [0,1]")
    return recovered_margin * (fit + (1 - fit) * (1 - displaced_margin_ratio))


def break_even_fit(win_back: float = 0.25, fee: float = 800000, run_cost: float = 200000,
                   inputs: CaseInputs = CaseInputs()) -> float | None:
    """Smallest fit share at which year-1 recovered margin covers fee plus running cost (ratio 1.0)."""
    recovered = float(calculate(inputs, win_back_rate=D(str(win_back))).annual_recovered_margin)
    need = (fee + run_cost) / recovered if recovered > 0 else None
    return None if need is None or need > 1 else need


def grid(plant_revenues=(200e6, 500e6, 1000e6, 2000e6), spare_shares=(0.0, 0.005, 0.01, 0.02, 0.05),
         win_back: float = 0.25, displaced_margin_ratio: float = 1.0) -> list[dict[str, float]]:
    """Illustrative grid. Plant revenues here are test values, not estimates of Company A."""
    extra = recovered_revenue(win_back)
    recovered = float(calculate(win_back_rate=D(str(win_back))).annual_recovered_margin)
    rows = []
    for rev in plant_revenues:
        for spare in spare_shares:
            fit = fit_share(extra, rev, spare)
            rows.append({"plant_revenue": rev, "spare_share": spare, "fit": fit,
                         "realised_margin": realised_margin(recovered, fit, displaced_margin_ratio)})
    return rows
