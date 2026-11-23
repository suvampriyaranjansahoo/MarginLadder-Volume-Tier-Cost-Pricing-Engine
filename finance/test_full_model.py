import pytest

from finance import capacity, queueing
from finance import full_model as fm
from finance.reconcile import reconcile


def test_every_python_cell_matches_the_excel_workbook():
    checks = reconcile()
    assert len(checks) >= 60
    bad = [f"{c.sheet}!{c.cell} {c.label}: excel={c.excel} python={c.python}" for c in checks if not c.ok]
    assert not bad, "\n".join(bad)


def test_npv_is_zero_at_the_irr():
    f = fm.financials()
    r = f["irr"]
    assert sum(cf / (1 + r) ** t for t, cf in enumerate(f["free_cash_flow"])) == pytest.approx(0, abs=1)


def test_irr_is_none_when_cash_flows_never_turn_positive():
    assert fm.irr([-100, -50, -10]) is None


def test_payback_none_if_never_positive():
    assert fm.payback_years([-1, -2, -3]) is None


def test_net_capacity_removes_review_hours():
    n = fm.net_capacity_value()
    assert n["gross_hours"] == 5400 and n["review_hours"] == 720 and n["net_hours"] == 4680
    assert n["net_value"] == pytest.approx(2106000)


def test_cash_gap_grows_with_longer_payment_terms():
    assert fm.cash_gap(3)["peak"] < fm.cash_gap(8)["peak"] < fm.cash_gap(15)["peak"]


def test_cash_gap_uses_cash_received_not_invoices():
    # M1 arrives at signing, so week 1 is already funded by 1.6 lakh.
    assert fm.cash_gap(8)["gap_by_week"][0] < 0


# queueing
def test_erlang_c_known_value():
    # Textbook check: 2 servers, offered load 1 => P(wait) = 1/3
    assert queueing.erlang_c(2, 1.0) == pytest.approx(1 / 3)


def test_erlang_c_single_server_equals_load():
    assert queueing.erlang_c(1, 0.7) == pytest.approx(0.7)


@pytest.mark.parametrize("servers,load", [(0, 1), (2, 2), (2, 3), (2, -1)])
def test_erlang_c_rejects_bad_input(servers, load):
    with pytest.raises(ValueError):
        queueing.erlang_c(servers, load)


def test_base_case_load_and_wait():
    r = queueing.mean_wait_days(60, 12.5, 6)
    assert r["load"] == pytest.approx(0.78125)
    assert 0.5 < r["wait_days"] < 0.65
    assert 0.45 < r["p_wait"] < 0.5


def test_target_case_has_almost_no_queue():
    assert queueing.mean_wait_days(60, 5, 6)["wait_days"] < 0.01


def test_wait_rises_faster_than_load():
    rows = queueing.load_table()
    waits = [r["wait_days"] for r in rows]
    assert waits == sorted(waits)
    assert waits[-1] > 10 * waits[2]


def test_uneven_jobs_lengthen_the_wait():
    assert queueing.mean_wait_days(60, 12.5, 6, cs2=2)["wait_days"] == pytest.approx(
        1.5 * queueing.mean_wait_days(60, 12.5, 6)["wait_days"])


def test_unstable_queue_is_refused():
    with pytest.raises(ValueError, match="unstable"):
        queueing.mean_wait_days(80, 12.5, 6)


def test_littles_law():
    assert queueing.littles_law(60, 9) == pytest.approx(27)
    assert queueing.littles_law(60, 4) == pytest.approx(12)


# capacity
def test_recovered_revenue_is_one_point_eight_crore():
    assert capacity.recovered_revenue() == pytest.approx(18_000_000)


def test_break_even_fit_is_46_percent():
    assert capacity.break_even_fit() == pytest.approx(1_000_000 / 2_160_000)


def test_no_spare_capacity_means_no_gain_when_displaced_orders_are_as_profitable():
    fit = capacity.fit_share(18e6, 500e6, 0.0)
    assert capacity.realised_margin(2_160_000, fit, 1.0) == 0


def test_full_fit_keeps_full_margin():
    assert capacity.realised_margin(2_160_000, 1.0, 1.0) == 2_160_000


def test_lower_value_displaced_orders_keep_some_margin():
    assert capacity.realised_margin(2_160_000, 0.0, 0.5) == pytest.approx(1_080_000)


def test_capacity_inputs_are_validated():
    with pytest.raises(ValueError):
        capacity.fit_share(18e6, 0, 0.1)
    with pytest.raises(ValueError):
        capacity.realised_margin(1, 1.5)


def test_grid_is_monotonic_in_spare_capacity():
    rows = [r for r in capacity.grid() if r["plant_revenue"] == 500e6]
    margins = [r["realised_margin"] for r in rows]
    assert margins == sorted(margins)
