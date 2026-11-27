"""Transparent annual-volume price schedules for the illustrative quote engine.

The costing engine returns one fully loaded cost and target-margin price for each
illustrative volume point.  A commercial quote can apply those prices in two
different, non-interchangeable ways:

* ``all_units`` applies the selected tier price to every unit ordered;
* ``marginal`` applies each tier price only to the incremental units in that
  band.  The first band starts at unit 1, not at 90,000.

This module deliberately does not infer a customer contract from the sample
tiers.  It only exposes the two common schedule mechanics so an estimator can
select and record the intended method.  The input prices and breakpoints remain
illustrative unless replaced by approved company data.
"""
from __future__ import annotations

from collections.abc import Iterable
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from engine.cost_engine import CostError

ALL_UNITS = "all_units"
MARGINAL = "marginal"
VALID_MODES = frozenset({ALL_UNITS, MARGINAL})


def money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def annual_schedule(tiers: Iterable[dict[str, Any]], selected_volume: int, mode: str) -> dict[str, Any]:
    """Return annual revenue and contribution from ordered price points.

    ``tiers`` must contain increasing ``annual_volume_per_part``, a unit price
    and a unit cost.  A selected volume must be one of the defined points. This
    intentionally prevents silent extrapolation beyond the illustrative bands.
    """
    if mode not in VALID_MODES:
        raise CostError(f"pricing mode must be one of {', '.join(sorted(VALID_MODES))}")
    rows = sorted(tiers, key=lambda row: int(row["annual_volume_per_part"]))
    volumes = [int(row["annual_volume_per_part"]) for row in rows]
    if not rows or volumes != sorted(set(volumes)) or any(volume <= 0 for volume in volumes):
        raise CostError("pricing schedule requires positive, strictly increasing volume points")
    if selected_volume not in volumes:
        raise CostError(f"selected volume must be one of {', '.join(map(str, volumes))}")

    selected_index = volumes.index(selected_volume)
    selected = rows[selected_index]
    unit_cost = Decimal(str(selected["total_unit_cost"]))
    bands: list[dict[str, Any]] = []
    if mode == ALL_UNITS:
        price = Decimal(str(selected["total_unit_price"]))
        revenue = money(price * selected_volume)
        bands.append({"from_unit": 1, "to_unit": selected_volume, "units": selected_volume, "unit_price": price, "revenue": revenue})
    else:
        previous = 0
        revenue = Decimal("0")
        for row in rows[: selected_index + 1]:
            upper = int(row["annual_volume_per_part"])
            units = upper - previous
            price = Decimal(str(row["total_unit_price"]))
            band_revenue = money(price * units)
            bands.append({"from_unit": previous + 1, "to_unit": upper, "units": units, "unit_price": price, "revenue": band_revenue})
            revenue += band_revenue
            previous = upper
        revenue = money(revenue)
    annual_cost = money(unit_cost * selected_volume)
    return {
        "pricing_mode": mode,
        "selected_volume": selected_volume,
        "annual_revenue": revenue,
        "annual_cost": annual_cost,
        "annual_contribution": money(revenue - annual_cost),
        "average_unit_price": money(revenue / Decimal(selected_volume)),
        "selected_tier_unit_cost": money(unit_cost),
        "bands": bands,
        "data_classification": "illustrative_schedule_assumption",
    }
