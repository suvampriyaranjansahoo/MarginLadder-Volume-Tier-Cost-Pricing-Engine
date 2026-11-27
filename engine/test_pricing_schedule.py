from decimal import Decimal

import pytest

from engine.cost_engine import CostError
from engine.pricing_schedule import ALL_UNITS, MARGINAL, annual_schedule


TIERS = [
    {"annual_volume_per_part": 90000, "total_unit_price": Decimal("117.33"), "total_unit_cost": Decimal("103.25")},
    {"annual_volume_per_part": 180000, "total_unit_price": Decimal("116.51"), "total_unit_cost": Decimal("102.53")},
    {"annual_volume_per_part": 270000, "total_unit_price": Decimal("115.77"), "total_unit_cost": Decimal("101.88")},
]


def test_all_units_applies_selected_price_to_every_unit():
    result = annual_schedule(TIERS, 180000, ALL_UNITS)
    assert result["annual_revenue"] == Decimal("20971800.00")
    assert result["average_unit_price"] == Decimal("116.51")
    assert result["annual_cost"] == Decimal("18455400.00")
    assert len(result["bands"]) == 1


def test_marginal_pricing_only_discounts_incremental_band_units():
    result = annual_schedule(TIERS, 180000, MARGINAL)
    assert result["annual_revenue"] == Decimal("21045600.00")
    assert result["average_unit_price"] == Decimal("116.92")
    assert [(band["from_unit"], band["to_unit"], band["unit_price"]) for band in result["bands"]] == [
        (1, 90000, Decimal("117.33")), (90001, 180000, Decimal("116.51")),
    ]
    assert result["annual_contribution"] == result["annual_revenue"] - result["annual_cost"]


@pytest.mark.parametrize("mode", ["", "tiered", "marginal "])
def test_bad_mode_is_visible_error(mode):
    with pytest.raises(CostError, match="pricing mode"):
        annual_schedule(TIERS, 180000, mode)


def test_no_implicit_volume_extrapolation():
    with pytest.raises(CostError, match="selected volume"):
        annual_schedule(TIERS, 200000, ALL_UNITS)
