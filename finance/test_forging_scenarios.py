from decimal import Decimal as D

import pytest

from finance.forging_scenarios import ForgingScenario, calculate, public_benchmark


def test_base_scenario_is_positive_and_labeled():
    result = calculate()
    assert D(result["unit_contribution_inr"]) > 0
    assert D(result["contribution_margin_pct"]) > 10
    assert "not Bharat Forge costs" in result["classification"]


def test_steel_shock_and_lower_yield_reduce_contribution():
    base = calculate()
    shocked = calculate(ForgingScenario(steel_price_change_pct=D("0.10"), forging_yield_pct=D("0.80")))
    assert D(shocked["unit_contribution_inr"]) < D(base["unit_contribution_inr"])


def test_scenario_validation_rejects_invalid_yield():
    with pytest.raises(ValueError, match="forging_yield_pct"):
        calculate(ForgingScenario(forging_yield_pct=D("0.2")))


def test_public_benchmark_has_provenance_and_limit():
    benchmark = public_benchmark()
    assert "Bharat Forge" in benchmark["source"]
    assert len(benchmark["metrics"]) == 5
    assert "One large" in benchmark["limits"]
