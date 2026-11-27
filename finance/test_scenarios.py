import json
from pathlib import Path

import pytest

from finance import scenarios as sc
from finance.full_model import FinancialAssumptions, financials

NUMBERS = json.loads((Path(__file__).resolve().parent.parent / "numbers.json").read_text(encoding="utf-8"))


def by_name():
    return {r["scenario"]: r for r in sc.run_scenarios()}


def test_three_named_scenarios_are_ordered_downside_base_upside():
    r = by_name()
    assert list(r) == ["downside", "base", "upside"]
    assert r["downside"]["npv"] < r["base"]["npv"] < r["upside"]["npv"]
    assert r["downside"]["payback_years"] > r["base"]["payback_years"] > r["upside"]["payback_years"]


def test_base_scenario_matches_numbers_json():
    base = by_name()["base"]
    assert base["npv"] == pytest.approx(NUMBERS["npv_after_tax_wc_inr"]["value"], abs=1)
    assert base["irr"] == pytest.approx(NUMBERS["irr_3yr"]["value"], abs=0.001)
    assert base["peak_funding"] == pytest.approx(NUMBERS["deepest_cash_need_inr"]["value"], abs=1)


def test_every_scenario_carries_a_note_saying_what_is_assumed():
    assert all(s.note for s in sc.SCENARIOS)


def test_npv_is_zero_at_the_break_even_win_back():
    w = sc.npv_break_even_win_back()
    assert w is not None
    assert financials(w)["npv"] == pytest.approx(0, abs=50)
    assert financials(w - 0.01)["npv"] < 0 < financials(w + 0.01)["npv"]


def test_npv_threshold_is_below_the_base_case_win_back():
    assert 0 < sc.npv_break_even_win_back() < 0.25  # type: ignore[operator]


def test_threshold_is_higher_without_working_capital_release():
    released = sc.npv_break_even_win_back(FinancialAssumptions(release_wc_at_end=True))
    kept = sc.npv_break_even_win_back(FinancialAssumptions(release_wc_at_end=False))
    assert released is not None and kept is not None and kept > released


def test_threshold_is_none_when_investment_can_never_pay_back():
    assert sc.npv_break_even_win_back(FinancialAssumptions(fee=10**9)) is None
