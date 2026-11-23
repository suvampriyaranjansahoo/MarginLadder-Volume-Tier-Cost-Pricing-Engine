from decimal import Decimal

import pytest

from finance.variance import VarianceError, monthly_summary, parse_rows


def test_revenue_and_cost_variances_use_correct_favourability_direction():
    rows = parse_rows([
        {"period": "2026-01", "metric": "Sales", "category": "revenue", "budget": "100", "actual": "110"},
        {"period": "2026-01", "metric": "Material", "category": "cost", "budget": "60", "actual": "65"},
    ])
    by_metric = {row.metric: row for row in rows}
    assert by_metric["Sales"].favourable is True
    assert by_metric["Material"].favourable is False
    assert by_metric["Material"].variance == Decimal("5")
    on_budget = parse_rows([{"period": "2026-01", "metric": "Freight", "category": "cost", "budget": "5", "actual": "5"}])[0]
    assert on_budget.favourability == "On budget"


def test_zero_budget_percentage_is_not_meaningful_not_division_by_zero():
    row = parse_rows([{"period": "2026-01", "metric": "New product", "category": "revenue", "budget": "0", "actual": "5"}])[0]
    assert row.variance_pct is None


def test_monthly_contribution_bridge_reconciles():
    rows = parse_rows([
        {"period": "2026-01", "metric": "Sales", "category": "revenue", "budget": "100", "actual": "110"},
        {"period": "2026-01", "metric": "Cost", "category": "cost", "budget": "60", "actual": "70"},
    ])
    out = monthly_summary(rows)[0]
    assert out["budget_contribution_proxy"] == "40"
    assert out["actual_contribution_proxy"] == "40"
    assert out["contribution_variance"] == "0"


@pytest.mark.parametrize("bad", [
    {"period": "Jan-26", "metric": "Sales", "category": "revenue", "budget": "1", "actual": "2"},
    {"period": "2026-01", "metric": "Sales", "category": "other", "budget": "1", "actual": "2"},
    {"period": "2026-01", "metric": "Sales", "category": "revenue", "budget": "-1", "actual": "2"},
])
def test_invalid_rows_are_rejected(bad):
    with pytest.raises(VarianceError):
        parse_rows([bad])


def test_duplicate_metric_in_period_is_rejected():
    row = {"period": "2026-01", "metric": "Sales", "category": "revenue", "budget": "1", "actual": "2"}
    with pytest.raises(VarianceError, match="duplicate"):
        parse_rows([row, row])


def test_invalid_calendar_month_is_rejected():
    with pytest.raises(VarianceError, match="valid YYYY-MM"):
        parse_rows([{"period": "2026-13", "metric": "Sales", "category": "revenue", "budget": "1", "actual": "2"}])
