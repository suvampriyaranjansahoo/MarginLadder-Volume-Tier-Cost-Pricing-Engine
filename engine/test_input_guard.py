from datetime import date

import pytest

from application.service import ACCEPTED_PART_KEYS
from engine.cost_engine import MASTER, SAMPLE, CostError, cost_part
from engine.input_guard import validate_part_inputs


@pytest.mark.parametrize(("key", "value"), [
    ("gross", "0"), ("gross", "-5"), ("net", "0"), ("net", "-1"),
    ("net", ""), ("gross", None), ("net", "NaN"), ("gross", "Infinity"), ("net", "abc"),
])
def test_weights_must_be_positive_finite_numbers(key, value):
    with pytest.raises(CostError):
        validate_part_inputs({**SAMPLE, key: value})


def test_sample_part_passes_the_guard():
    validate_part_inputs(dict(SAMPLE))


def test_the_engine_alone_accepts_a_negative_net_weight():
    """Documents the retained v1 gap. If the engine is ever fixed this test should be deleted, not the guard."""
    result = cost_part({**SAMPLE, "net": "-1"}, MASTER, date(2026, 11, 5), 180000)
    assert result["price"] > 0


def test_gst_is_an_accepted_part_key():
    assert "gst" in ACCEPTED_PART_KEYS
    assert set(SAMPLE) <= ACCEPTED_PART_KEYS
