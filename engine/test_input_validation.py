from datetime import date
from decimal import Decimal
import pytest
from engine.cost_engine import CostError, MASTER, SAMPLE, cost_part

@pytest.mark.parametrize(("key", "value"), [
    ("reject", "2"), ("reject", "-0.01"), ("overhead", "-0.1"),
    ("scrap_credit", "-1"), ("gst", "-0.2"), ("gst", "1.01"),
    ("packing", "-1"), ("freight_per_kg", "-1"),
    ("reject", "NaN"), ("overhead", "Infinity"),
])
def test_invalid_cost_inputs_are_rejected(key, value):
    with pytest.raises(CostError):
        cost_part({**SAMPLE, key: value}, MASTER, date(2026, 11, 5), 180000)

@pytest.mark.parametrize(("key", "value"), [
    ("reject", "0"), ("overhead", "0"), ("scrap_credit", "0"),
    ("gst", "0"), ("gst", "1"), ("packing", "0"), ("freight_per_kg", "0"),
])
def test_valid_cost_input_boundaries_are_accepted(key, value):
    result = cost_part({**SAMPLE, key: value}, MASTER, date(2026, 11, 5), 180000)
    assert result["price"] > Decimal("0")
