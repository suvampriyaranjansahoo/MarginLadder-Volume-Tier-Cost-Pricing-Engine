import pytest

from finance.investment import InvestmentInputs, evaluate, incremental_orders, irr, mirr, monthly_cash_flow, npv, working_capital


def test_working_capital_is_separate_ar_inventory_and_ap():
    result = working_capital(36500, 18250, 14600, InvestmentInputs(dso=40, dio=20, dpo=30))
    assert result["accounts_receivable"] == 4000
    assert result["inventory"] == 1000
    assert result["accounts_payable"] == 1200
    assert result["net_working_capital"] == 3800
    assert result["cash_conversion_cycle_days"] == 30


def test_incremental_orders_use_control_treatment_and_cannibalisation():
    result = incremental_orders(InvestmentInputs(total_rfqs=100, adoption_rate=.5, successful_processing_rate=.8, control_conversion=.1, treatment_conversion=.3, cannibalisation_rate=.25))
    assert result["processed_rfqs"] == 40
    assert result["gross_incremental_orders"] == pytest.approx(8)
    assert result["incremental_orders"] == pytest.approx(6)


def test_zero_adoption_has_no_revenue_and_no_incremental_orders():
    result = evaluate(InvestmentInputs(adoption_rate=0))
    assert result["economics"]["incremental_orders"] == 0
    assert result["recommendation"] == "do_not_invest"


def test_terminal_release_reverses_prior_nwc_investment():
    rows = monthly_cash_flow(InvestmentInputs(years=1, terminal_nwc_release=True))
    assert rows[-1]["closing_nwc"] == 0
    assert rows[-1]["change_nwc"] < 0


def test_delayed_launch_defers_revenue_and_cash_flow():
    rows = monthly_cash_flow(InvestmentInputs(launch_delay_months=3))
    assert all(row["revenue"] == 0 for row in rows[1:4])
    assert rows[4]["revenue"] > 0


def test_npv_discounting_and_multiple_irr_protection():
    assert npv([-100, 110], .1) == pytest.approx(0)
    assert irr([-100, 60, 60]) == pytest.approx(.130662386, abs=1e-6)
    assert irr([-100, 230, -132]) is None


def test_mirr_and_negative_case_are_handled_honestly():
    assert mirr([-100, 60, 60], .1, .1) is not None
    result = evaluate(InvestmentInputs(treatment_conversion=0, implementation_capex=1_000_000))
    assert result["npv"] < 0 and result["recommendation"] == "do_not_invest"
