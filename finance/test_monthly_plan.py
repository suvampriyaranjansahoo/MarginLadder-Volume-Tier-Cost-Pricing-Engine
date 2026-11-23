from decimal import Decimal as D

import pytest

from finance.monthly_plan import MonthlyPlanInputs, build_monthly_plan, summary


def test_base_case_reconciles_to_existing_case_arithmetic() -> None:
    result = summary()
    assert result["annual_rfqs"] == 720
    assert result["annual_lost_rfqs"] == D("36.00")
    assert result["lost_rfq_margin_pool"] == D("8640000.00")
    assert result["annual_recovered_contribution"] == D("2160000.00")
    assert result["annual_net_contribution_after_run_cost"] == D("1960000.00")
    assert result["operating_payback_months"] == D("4.90")
    assert result["break_even_win_back_rate"].quantize(D("0.0001")) == D("0.1157")


def test_monthly_rows_sum_to_annual_outputs_and_setup_is_one_off() -> None:
    periods = build_monthly_plan()
    assert len(periods) == 12
    assert sum((p.contribution for p in periods), D("0")) == D("2160000.00")
    assert sum((p.run_cost for p in periods), D("0")) == D("200000.00")
    assert sum((p.one_time_setup_cost for p in periods), D("0")) == D("800000.00")
    assert periods[0].one_time_setup_cost == D("800000.00")
    assert all(p.one_time_setup_cost == D("0.00") for p in periods[1:])
    assert periods[-1].cumulative_project_cash_proxy == D("1160000.00")


def test_conservative_win_back_case() -> None:
    result = summary(MonthlyPlanInputs(win_back_rate=D("0.125")))
    assert result["annual_recovered_contribution"] == D("1080000.00")
    assert result["annual_net_contribution_after_run_cost"] == D("880000.00")
    assert result["operating_payback_months"] == D("10.91")


@pytest.mark.parametrize("kwargs", [
    {"months": 0},
    {"rfqs_per_month": D("0")},
    {"win_back_rate": D("1.01")},
    {"lost_rfq_rate": D("-0.01")},
    {"annual_run_cost": D("-1")},
])
def test_invalid_inputs_are_rejected(kwargs: dict) -> None:
    with pytest.raises(ValueError):
        MonthlyPlanInputs(**kwargs).validate()


def test_zero_win_back_does_not_return_a_payback() -> None:
    result = summary(MonthlyPlanInputs(win_back_rate=D("0")))
    assert result["operating_payback_months"] is None
