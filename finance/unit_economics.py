"""Decision layer on top of the retained costing engine (engine/cost_engine.py, not modified).

Answers: which volume tier earns most, where unit cost is most exposed, what a material or rejection
shock does to margin at a fixed quoted price, and at what volume a quoted price covers full unit cost.

All inputs come from engine.cost_engine.SAMPLE and are ILLUSTRATIVE (assumption A21 in the PRD).
Nothing here is observed business data. Rework cost is not modelled (the PRD formula has rejection only).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from collections.abc import Mapping
from decimal import Decimal as D
from typing import Any

from engine.cost_engine import CostError, Rate, RateMaster, cost_part

COST_LINES = ("net_material", "machining", "setup", "rejection", "overhead", "packing", "freight")
MAX_SEARCH_VOLUME = 50_000_000
_RATE_START, _RATE_END = date(2000, 1, 1), date(2100, 12, 31)


def make_master(material_rate: D, machine_rate: D, material_code: str = "MAT-EN8", machine_code: str = "MC-SPINDLE") -> RateMaster:
    """A single-version rate master valid for any date, for what-if runs. Real quotes use the dated master."""
    return RateMaster([
        Rate(material_code, D(material_rate), "kg", _RATE_START, _RATE_END, "whatif"),
        Rate(machine_code, D(machine_rate), "hour", _RATE_START, _RATE_END, "whatif"),
    ])


@dataclass(frozen=True)
class TierBand:
    """A volume band: applies from min_volume (inclusive) up to the next band's min_volume (exclusive)."""
    min_volume: int
    material_rate: D


# Illustrative bands mirroring engine.cost_engine.TIER_RATES (assumption A21, not a real supplier price list).
DEFAULT_BANDS = (TierBand(90000, D("79")), TierBand(180000, D("78")), TierBand(270000, D("77")))


def rate_for_volume(bands: tuple[TierBand, ...], volume: int) -> D:
    """Material rate for an annual volume. Lower bound of each band is inclusive; below the first band is an error."""
    if not bands:
        raise CostError("no volume bands defined")
    mins = [b.min_volume for b in bands]
    if any(m <= 0 for m in mins) or mins != sorted(set(mins)):
        raise CostError("volume bands must have positive, strictly increasing minimum volumes")
    if volume < mins[0]:
        raise CostError(f"annual volume {volume} is below the first tier ({mins[0]})")
    return [b for b in bands if b.min_volume <= volume][-1].material_rate


def component_shares(result: Mapping[str, Any]) -> list[tuple[str, D]]:
    """Share of full unit cost by line, largest first. Shares add to 1 (to 4 dp rounding)."""
    cost = D(result["cost"])
    if cost <= 0:
        raise CostError("cost must be above zero to compute shares")
    shares = [(line, (D(result[line]) / cost).quantize(D("0.0001"))) for line in COST_LINES]
    return sorted(shares, key=lambda item: (-item[1], item[0]))


def tier_comparison(sample: Mapping[str, Any], tier_rates: Mapping[int, D], machine_rate: D, quote_date: date) -> list[dict[str, Any]]:
    """Cost, price and annual contribution at each volume tier. tier_rates maps annual volume to material rate.

    The tier with the most annual contribution is marked preferred, but only if the customer commits to that volume.
    """
    rows: list[dict[str, Any]] = []
    for volume, material_rate in sorted(tier_rates.items()):
        r = cost_part(dict(sample), make_master(material_rate, machine_rate), quote_date, volume)
        unit_margin = r["price"] - r["cost"]
        rows.append({
            "volume": volume, "material_rate": material_rate, "setup_per_piece": r["setup"], "unit_cost": r["cost"],
            "price": r["price"], "unit_margin": unit_margin, "margin_pct": (unit_margin / r["price"]).quantize(D("0.0001")),
            "annual_revenue": r["price"] * volume, "annual_contribution": unit_margin * volume, "preferred": False,
        })
    if rows:
        max(rows, key=lambda row: row["annual_contribution"])["preferred"] = True
    return rows


@dataclass(frozen=True)
class Shock:
    name: str
    target: str          # "material_rate", "machine_rate" or a costing input key
    mode: str            # "pct" (relative change) or "abs" (absolute change)
    amount: D


DEFAULT_SHOCKS = (
    Shock("Material price +10%", "material_rate", "pct", D("0.10")),
    Shock("Machine hour rate +10%", "machine_rate", "pct", D("0.10")),
    Shock("Cycle time +10%", "cycle_min", "pct", D("0.10")),
    Shock("Setup time +10%", "setup_min", "pct", D("0.10")),
    Shock("Rejection rate +1 point", "reject", "abs", D("0.01")),
    Shock("Scrap credit -10%", "scrap_credit", "pct", D("-0.10")),
    Shock("Freight per kg +10%", "freight_per_kg", "pct", D("0.10")),
    Shock("Overhead loading +10%", "overhead", "pct", D("0.10")),
    Shock("Packing +10%", "packing", "pct", D("0.10")),
)


def _shocked(value: D, shock: Shock) -> D:
    return value * (1 + shock.amount) if shock.mode == "pct" else value + shock.amount


def sensitivity(sample: Mapping[str, Any], material_rate: D, machine_rate: D, quote_date: date, volume: int,
                shocks: tuple[Shock, ...] = DEFAULT_SHOCKS) -> list[dict[str, Any]]:
    """Effect of each shock on unit cost and on margin if the quoted price is held. Largest margin loss first."""
    base = cost_part(dict(sample), make_master(material_rate, machine_rate), quote_date, volume)
    price = base["price"]
    out: list[dict[str, Any]] = []
    for s in shocks:
        inputs = dict(sample)
        mat, mc = material_rate, machine_rate
        if s.target == "material_rate":
            mat = _shocked(material_rate, s)
        elif s.target == "machine_rate":
            mc = _shocked(machine_rate, s)
        else:
            inputs[s.target] = str(_shocked(D(str(sample[s.target])), s))
        new = cost_part(inputs, make_master(mat, mc), quote_date, volume)
        margin_pct = (price - new["cost"]) / price
        out.append({
            "shock": s.name, "new_cost": new["cost"], "cost_change": new["cost"] - base["cost"],
            "cost_change_pct": ((new["cost"] - base["cost"]) / base["cost"]).quantize(D("0.0001")),
            "margin_pct_at_quoted_price": margin_pct.quantize(D("0.0001")),
            "margin_change_points": ((margin_pct - (price - base["cost"]) / price) * 100).quantize(D("0.01")),
        })
    return sorted(out, key=lambda row: (row["cost_change"] * -1, row["shock"]))


def break_even_volume(sample: Mapping[str, Any], material_rate: D, machine_rate: D, quote_date: date, price: D) -> int | None:
    """Smallest annual volume at which `price` covers full unit cost (setup is spread over volume).

    Returns None when even a very large volume cannot cover the price (variable cost alone is too high).
    Zero margin is the break-even here because the engine's cost already carries overhead and rejection.
    """
    master = make_master(material_rate, machine_rate)

    def covers(v: int) -> bool:
        return bool(cost_part(dict(sample), master, quote_date, v)["cost"] <= price)

    if not covers(MAX_SEARCH_VOLUME):
        return None
    lo, hi = 1, MAX_SEARCH_VOLUME
    while lo < hi:
        mid = (lo + hi) // 2
        if covers(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
