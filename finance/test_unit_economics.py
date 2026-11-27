from dataclasses import FrozenInstanceError
from datetime import date
from decimal import Decimal as D

import pytest

from engine.cost_engine import MASTER, SAMPLE, TIER_RATES, CostError, Rate, RateMaster, cost_part, r2
from finance import unit_economics as ue

QD = date(2026, 11, 5)
MAT, MC = D("78"), D("850")


def base(volume: int = 180000):
    return cost_part(dict(SAMPLE), ue.make_master(MAT, MC), QD, volume)


# ---- volume tier boundaries ----
@pytest.mark.parametrize(("volume", "rate"), [
    (90000, "79"), (179999, "79"), (180000, "78"), (269999, "78"), (270000, "77"), (10**9, "77"),
])
def test_tier_boundaries_are_inclusive_at_the_lower_edge(volume, rate):
    assert ue.rate_for_volume(ue.DEFAULT_BANDS, volume) == D(rate)


def test_volume_below_first_tier_is_refused():
    with pytest.raises(CostError, match="below the first tier"):
        ue.rate_for_volume(ue.DEFAULT_BANDS, 89999)


@pytest.mark.parametrize("bands", [
    (), (ue.TierBand(100, D(1)), ue.TierBand(100, D(2))), (ue.TierBand(200, D(1)), ue.TierBand(100, D(2))), (ue.TierBand(0, D(1)),),
])
def test_malformed_bands_are_refused(bands):
    with pytest.raises(CostError):
        ue.rate_for_volume(bands, 500)


def test_default_bands_match_the_engine_example_rates():
    assert {b.min_volume: b.material_rate for b in ue.DEFAULT_BANDS} == TIER_RATES


def test_tier_comparison_reproduces_engine_prices_and_marks_one_preferred():
    rows = ue.tier_comparison(SAMPLE, TIER_RATES, MC, QD)
    assert [str(r["price"]) for r in rows] == ["117.33", "116.51", "115.77"]
    assert sum(r["preferred"] for r in rows) == 1
    assert rows[-1]["preferred"] is True
    assert all(r["annual_contribution"] == r["unit_margin"] * r["volume"] for r in rows)


def test_unit_cost_falls_as_volume_rises():
    costs = [r["unit_cost"] for r in ue.tier_comparison(SAMPLE, TIER_RATES, MC, QD)]
    assert costs == sorted(costs, reverse=True)


# ---- rounding ----
@pytest.mark.parametrize(("raw", "expected"), [("0.004", "0.00"), ("0.005", "0.01"), ("0.015", "0.02"), ("2.675", "2.68"), ("-0.005", "-0.01")])
def test_two_decimal_rounding_is_half_up_not_bankers(raw, expected):
    assert r2(raw) == D(expected)


def test_cost_is_the_sum_of_rounded_lines_at_every_tier():
    for v in (1, 12, 90000, 180000, 10**7):
        r = base(v)
        assert sum(r[k] for k in ue.COST_LINES) == r["cost"]
        assert all(r[k] == r[k].quantize(D("0.01")) for k in ue.COST_LINES)


def test_component_shares_sum_to_one_within_rounding_and_are_sorted():
    shares = ue.component_shares(base())
    assert abs(sum((s for _, s in shares), D(0)) - 1) <= D("0.0004")
    assert [s for _, s in shares] == sorted((s for _, s in shares), reverse=True)
    assert {name for name, _ in shares} == set(ue.COST_LINES)


def test_machining_and_material_dominate_the_illustrative_part():
    top_two = {name for name, _ in ue.component_shares(base())[:2]}
    assert top_two == {"machining", "net_material"}


# ---- historical quote reproducibility ----
def test_rate_object_cannot_be_changed_after_a_quote():
    rate = MASTER.lookup("MAT-EN8", date(2026, 9, 15))
    with pytest.raises(FrozenInstanceError):
        rate.value = D("1")  # type: ignore[misc]


def test_new_rate_version_does_not_change_an_old_quote_recomputed_on_its_own_date():
    old = cost_part(dict(SAMPLE), MASTER, date(2026, 9, 15), 180000)
    newer = RateMaster([*MASTER.rates, Rate("MAT-EN8", D("120"), "kg", date(2027, 4, 1), date(2027, 9, 30), "v18")])
    again = cost_part(dict(SAMPLE), newer, date(2026, 9, 15), 180000)
    assert again["price"] == old["price"]
    assert again["snapshot"] == old["snapshot"]
    assert old["snapshot"]["rates"][0][5] == "v16"


def test_costing_does_not_mutate_its_inputs():
    inputs = dict(SAMPLE)
    cost_part(inputs, MASTER, QD, 180000)
    assert inputs == SAMPLE


# ---- sensitivity ----
def test_no_default_shock_lowers_cost_and_only_setup_is_immaterial_at_base_volume():
    rows = ue.sensitivity(SAMPLE, MAT, MC, QD, 180000)
    assert len(rows) == len(ue.DEFAULT_SHOCKS)
    assert all(r["cost_change"] >= 0 and r["margin_change_points"] <= 0 for r in rows)
    flat = {r["shock"] for r in rows if r["cost_change"] == 0}
    assert flat == {"Setup time +10%"}  # setup is about 0.09 per piece at 180,000 units, below rounding at +10%


def test_setup_shock_matters_at_low_volume():
    row = next(r for r in ue.sensitivity(SAMPLE, MAT, MC, QD, 2000) if r["shock"] == "Setup time +10%")
    assert row["cost_change"] > 0


def test_sensitivity_is_sorted_largest_cost_increase_first():
    changes = [r["cost_change"] for r in ue.sensitivity(SAMPLE, MAT, MC, QD, 180000)]
    assert changes == sorted(changes, reverse=True)


def test_material_price_shock_matches_a_manual_recalculation():
    row = next(r for r in ue.sensitivity(SAMPLE, MAT, MC, QD, 180000) if r["shock"] == "Material price +10%")
    manual = cost_part(dict(SAMPLE), ue.make_master(MAT * D("1.1"), MC), QD, 180000)["cost"]
    assert row["new_cost"] == manual
    assert row["cost_change"] == manual - base()["cost"]


def test_rejection_shock_uses_absolute_points():
    row = next(r for r in ue.sensitivity(SAMPLE, MAT, MC, QD, 180000) if r["shock"].startswith("Rejection"))
    manual = cost_part({**SAMPLE, "reject": "0.025"}, ue.make_master(MAT, MC), QD, 180000)["cost"]
    assert row["new_cost"] == manual


def test_margin_at_held_price_drops_by_the_cost_change():
    b = base()
    row = ue.sensitivity(SAMPLE, MAT, MC, QD, 180000, (ue.Shock("Packing +1", "packing", "abs", D("1")),))[0]
    assert row["margin_pct_at_quoted_price"] == ((b["price"] - b["cost"] - D("1.00") - D("0")) / b["price"]).quantize(D("0.0001"))


def test_impossible_shock_is_refused_not_silently_clamped():
    with pytest.raises(CostError):
        ue.sensitivity(SAMPLE, MAT, MC, QD, 180000, (ue.Shock("Rejection +99 points", "reject", "abs", D("0.99")),))


# ---- break-even volume ----
def test_break_even_volume_is_the_exact_boundary():
    price = base()["price"]
    v = ue.break_even_volume(SAMPLE, MAT, MC, QD, price)
    assert v is not None
    assert base(v)["cost"] <= price
    assert v == 1 or base(v - 1)["cost"] > price


def test_break_even_is_one_when_price_covers_even_the_smallest_run():
    assert ue.break_even_volume(SAMPLE, MAT, MC, QD, D("100000")) == 1


def test_break_even_is_none_when_price_is_below_variable_cost():
    assert ue.break_even_volume(SAMPLE, MAT, MC, QD, D("60")) is None


def test_higher_price_needs_a_lower_or_equal_volume():
    low = ue.break_even_volume(SAMPLE, MAT, MC, QD, D("110"))
    high = ue.break_even_volume(SAMPLE, MAT, MC, QD, D("120"))
    assert low is not None and high is not None and high <= low
