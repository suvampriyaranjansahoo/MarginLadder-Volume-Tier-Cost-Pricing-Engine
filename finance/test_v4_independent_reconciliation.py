"""Independent arithmetic checks for the V4 decision model.

These values are calculated directly in the test rather than by calling the
model's working-capital or counterfactual helpers.
"""
import pytest

from finance.investment import InvestmentInputs, evaluate, monthly_cash_flow


def test_manual_first_operating_month_reconciles_to_model():
    inputs = InvestmentInputs(total_rfqs=100, treatment_conversion=.2, average_order_value=1000, contribution_margin=.25,
                              annual_run_cost=1200, implementation_capex=500, dso=36.5, dio=36.5, dpo=18.25, years=1)
    row = monthly_cash_flow(inputs)[1]
    # 20 orders/year -> 20,000 annual revenue -> 1,666.67/month; COGS 1,250/month.
    revenue, cogs = 20_000 / 12, 15_000 / 12
    ar, inventory, ap = 20_000 * 36.5 / 365, 15_000 * 36.5 / 365, 15_000 * 18.25 / 365
    expected_nwc = ar + inventory - ap
    expected_ocf = ((5_000 / 12) - 100) * .75
    assert row["revenue"] == pytest.approx(revenue)
    assert row["closing_nwc"] == pytest.approx(expected_nwc)
    assert row["free_cash_flow"] == pytest.approx(expected_ocf - expected_nwc)


def test_cash_flow_identity_holds_month_by_month():
    for row in monthly_cash_flow(InvestmentInputs(launch_delay_months=3)):
        assert row["free_cash_flow"] == pytest.approx(row["operating_cash_flow"] - row["capex"] - row["change_nwc"])


def test_peak_funding_uses_running_monthly_cash_not_annual_average():
    result = evaluate(InvestmentInputs(launch_delay_months=6))
    flows = [row["free_cash_flow"] for row in result["monthly"]]
    cumulative, lowest = 0.0, 0.0
    for flow in flows:
        cumulative += flow
        lowest = min(lowest, cumulative)
    assert result["peak_funding"] == pytest.approx(-lowest)
