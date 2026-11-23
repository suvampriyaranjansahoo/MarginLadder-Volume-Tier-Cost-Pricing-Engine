from decimal import Decimal as D

import pytest

from finance.case_model import CaseInputs, calculate, scenario_table


def test_base_case_reproduces_brief_arithmetic():
    result = calculate()
    assert result.annual_rfqs == 720
    assert result.annual_lost_rfqs == D("36.00")
    assert result.lost_rfq_margin_pool == D("8640000.00")
    assert result.assumed_win_back_rate == D("0.2500")
    assert result.annual_recovered_margin == D("2160000.00")
    assert result.annual_net_benefit_after_run_cost == D("1960000.00")


def test_payback_and_break_even_are_separate_from_cash_payback():
    result = calculate()
    assert result.gross_margin_payback_months == D("4.44")
    assert result.operating_payback_after_run_cost_months == D("4.90")
    assert D("0.115") < result.break_even_win_back_rate_including_one_year_run_cost < D("0.116")


def test_capacity_value_is_separately_calculated():
    result = calculate()
    assert result.current_estimator_hours == D("9000.0")
    assert result.target_estimator_hours == D("3600.0")
    assert result.annual_hours_released == D("5400.0")
    assert result.theoretical_capacity_value == D("2430000.00")


def test_scenarios_are_monotonic():
    rows = scenario_table()
    amounts = [D(row["annual_recovered_margin_inr"]) for row in rows]
    assert amounts == sorted(amounts)
    assert [r["win_back_rate"] for r in rows] == ["5.0%", "12.5%", "25.0%", "50.0%"]


def test_input_validation_blocks_impossible_winback_and_time_targets():
    with pytest.raises(ValueError, match="win_back_rate"):
        calculate(win_back_rate=D("1.2"))
    with pytest.raises(ValueError, match="cannot exceed"):
        calculate(CaseInputs(target_hours_per_part=D("3")))
