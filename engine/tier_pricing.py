"""Volume-tier material rates for quote generation.

The dated rate master (engine.cost_engine.MASTER) holds one material rate per effective period. The PRD worked example
prices the three annual-volume tiers on different material rates (TIER_RATES: 79, 78, 77). This module connects the two
without editing the retained engine file:

* the 180,000-unit tier uses the dated master rate unchanged (the reference tier);
* the other tiers apply the TIER_RATES difference to that dated rate (+1 at 90,000, -1 at 270,000).

So rate changes in the master still flow through to every tier, and a quote snapshot records the adjusted version label
(for example "v17+1"), which keeps historical quotes reproducible. The band differences are illustrative (assumption A21),
not a supplier price list.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal as D

from engine.cost_engine import TIER_RATES, CostError, Rate, RateMaster

REFERENCE_VOLUME = 180000


def tier_adjustment(volume: int) -> D:
    """Material rate difference (INR/kg) for a tier relative to the reference tier."""
    if volume not in TIER_RATES:
        raise CostError(f"annual volume {volume} is not a defined tier ({', '.join(map(str, sorted(TIER_RATES)))})")
    return TIER_RATES[volume] - TIER_RATES[REFERENCE_VOLUME]


def tier_master(master: RateMaster, material_code: str, quote_date: date, volume: int) -> RateMaster:
    """A rate master whose material rate for `material_code` is the dated rate plus the tier adjustment."""
    adjustment = tier_adjustment(volume)
    if adjustment == 0:
        return master
    base: Rate = master.lookup(material_code, quote_date)
    adjusted = Rate(base.code, base.value + adjustment, base.unit, base.eff_from, base.eff_to, f"{base.version}{adjustment:+}")
    return RateMaster([*(r for r in master.rates if r.code != material_code), adjusted])
