from datetime import date
from decimal import Decimal as D

import pytest

from engine.cost_engine import MASTER, SAMPLE, TIER_RATES, TIER_VOLUMES, CostError, cost_part
from engine.tier_pricing import REFERENCE_VOLUME, tier_adjustment, tier_master

NOV = date(2026, 11, 5)   # master material rate v17 = 78
SEP = date(2026, 9, 15)   # master material rate v16 = 79


def test_adjustments_follow_tier_rates_relative_to_the_reference_tier():
    assert {v: tier_adjustment(v) for v in TIER_VOLUMES} == {90000: D("1"), 180000: D("0"), 270000: D("-1")}
    assert REFERENCE_VOLUME in TIER_RATES


def test_reference_tier_uses_the_master_unchanged():
    assert tier_master(MASTER, "MAT-EN8", NOV, 180000) is MASTER


@pytest.mark.parametrize(("volume", "price"), [(90000, "117.33"), (180000, "116.51"), (270000, "115.77")])
def test_tier_prices_match_the_prd_worked_example(volume, price):
    result = cost_part(dict(SAMPLE), tier_master(MASTER, "MAT-EN8", NOV, volume), NOV, volume)
    assert str(result["price"]) == price


@pytest.mark.parametrize(("when", "base", "expected"), [(NOV, 78, (79, 78, 77)), (SEP, 79, (80, 79, 78))])
def test_tier_rates_move_with_the_dated_master(when, base, expected):
    got = tuple(int(tier_master(MASTER, "MAT-EN8", when, v).lookup("MAT-EN8", when).value) for v in TIER_VOLUMES)
    assert got == expected
    assert base == expected[1]


def test_snapshot_records_the_adjusted_rate_version():
    for volume, label in [(90000, "v17+1"), (180000, "v17"), (270000, "v17-1")]:
        r = cost_part(dict(SAMPLE), tier_master(MASTER, "MAT-EN8", NOV, volume), NOV, volume)
        assert r["snapshot"]["rates"][0][5] == label


def test_machine_rate_and_the_original_master_are_not_changed():
    before = [(r.code, r.value, r.version) for r in MASTER.rates]
    tm = tier_master(MASTER, "MAT-EN8", NOV, 90000)
    assert tm.lookup("MC-SPINDLE", NOV).value == D("850")
    assert [(r.code, r.value, r.version) for r in MASTER.rates] == before


def test_undefined_tier_and_unknown_material_are_visible_errors():
    with pytest.raises(CostError, match="not a defined tier"):
        tier_master(MASTER, "MAT-EN8", NOV, 100000)
    with pytest.raises(CostError, match="no rate effective"):
        tier_master(MASTER, "MAT-XX", NOV, 90000)
    with pytest.raises(CostError, match="no rate effective"):
        tier_master(MASTER, "MAT-EN8", date(2030, 1, 1), 90000)
