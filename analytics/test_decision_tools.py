import pytest

from analytics import rice_sensitivity as rs
from analytics import sample_size as ss


def test_matrix_parses_and_matches_its_own_rice_column():
    items = rs.load_items()
    assert len(items) == 9
    for i in items:
        assert rs.rice(i["reach"], i["impact"], i["confidence"], i["effort"]) == pytest.approx(i["rice"], abs=0.06), i["name"]


def test_ranks_are_a_permutation():
    assert sorted(rs.ranks([5, 1, 9, 3])) == [1, 2, 3, 4] and rs.ranks([5, 1, 9, 3]) == [2, 4, 1, 3]


def test_simulation_is_repeatable_and_ranks_in_range():
    a, b = rs.simulate(rs.load_items(), 300, 1), rs.simulate(rs.load_items(), 300, 1)
    assert a == b
    assert all(1 <= r["p10_rank"] <= r["median_rank"] <= r["p90_rank"] <= 9 for r in a)


def test_costing_stays_first_in_base_case():
    assert rs.simulate(rs.load_items(), 200, 3)[0]["name"].startswith("Deterministic costing")


def test_classic_sample_size():
    assert 385 <= ss.n_per_period(0.5, 0.6) <= 390


def test_bigger_effects_need_fewer_rfqs():
    assert ss.n_per_period(0.1, 0.5) < ss.n_per_period(0.1, 0.3) < ss.n_per_period(0.1, 0.2)


def test_mde_is_consistent_with_sample_size():
    p1 = ss.minimum_detectable_rate(0.10, 90)
    assert p1 is not None and ss.n_per_period(0.10, p1) <= 90 < ss.n_per_period(0.10, p1 - 0.01)


def test_tiny_samples_cannot_detect_anything_reasonable():
    assert ss.minimum_detectable_rate(0.5, 5) is None


@pytest.mark.parametrize("p0,p1", [(0, 0.5), (0.5, 0.5), (0.5, 1.0)])
def test_bad_rates_refused(p0, p1):
    with pytest.raises(ValueError):
        ss.n_per_period(p0, p1)
