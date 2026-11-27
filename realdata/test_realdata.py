import json
from pathlib import Path

import pytest

from realdata import benchmark as bm
from realdata import bharat_forge_fy26 as bf

NUMBERS = json.loads((Path(__file__).resolve().parent.parent / "numbers.json").read_text(encoding="utf-8"))


def test_expenses_add_up_to_the_filing_total():
    p = bf.PNL
    parts = (p["cost_of_materials_consumed"] + p["purchases_of_stock_in_trade"] + p["changes_in_inventories"]
             + p["employee_benefit_expense"] + p["finance_costs"] + p["depreciation_and_amortisation"] + p["other_expenses"])
    assert parts == pytest.approx(p["total_expenses"], abs=0.1)


def test_profit_lines_chain_through():
    p = bf.PNL
    assert p["revenue_from_operations"] + p["other_income"] - p["total_expenses"] == pytest.approx(p["profit_before_exceptional_and_tax"], abs=0.1)
    assert p["profit_before_exceptional_and_tax"] + p["exceptional_items"] == pytest.approx(p["profit_before_tax"], abs=0.1)
    assert p["profit_before_tax"] - p["total_tax"] == pytest.approx(p["profit_continuing_operations"], abs=0.1)
    assert p["profit_continuing_operations"] + p["share_of_associates_and_jv"] == pytest.approx(p["total_profit_for_period"], abs=0.1)
    assert p["profit_attributable_to_owners"] + p["profit_attributable_to_nci"] == pytest.approx(p["total_profit_for_period"], abs=0.1)


def test_balance_sheet_balances():
    assert bm.balance_sheet_balances()


def test_segments_reconcile_to_revenue():
    total = sum(s["revenue"] for s in bf.SEGMENTS.values())
    assert total - bf.INTER_SEGMENT_REVENUE == pytest.approx(bf.PNL["revenue_from_operations"], abs=0.1)


def test_eps_agrees_with_profit_and_share_count():
    shares = bf.PNL["paid_up_equity_share_capital"] / bf.PNL["face_value_per_share_inr"]
    assert bf.PNL["profit_attributable_to_owners"] / shares == pytest.approx(bf.PNL["eps_basic_inr"], abs=0.01)


def test_recomputed_debt_equity_matches_the_ratio_the_company_reported():
    assert bm.metrics()["debt_to_equity"] == pytest.approx(bf.PNL["reported_debt_equity_ratio"], abs=0.005)


def test_recomputed_ebitda_is_within_one_percent_of_the_reported_figure():
    assert abs(bm.metrics()["reported_ebitda_gap_pct"]) < 0.01


def test_dupont_factors_multiply_to_roe():
    m = bm.metrics()
    direct = bf.PNL["total_profit_for_period"] / bf.BALANCE_SHEET["total_equity"]
    assert m["roe"] == pytest.approx(direct, abs=1e-9)


def test_stress_test_base_row_reproduces_the_case_irr():
    base = bm.working_capital_stress()[0]
    assert base["days"] == 45
    assert base["irr"] == pytest.approx(NUMBERS["irr_3yr"]["value"], abs=0.001)


def test_longer_working_capital_cycles_lower_the_irr():
    irrs = [r["irr"] for r in bm.working_capital_stress()]
    assert irrs == sorted(irrs, reverse=True)
    assert irrs[0] > irrs[-1]


def test_report_states_its_limits_and_the_price_date():
    text = bm.render()
    assert "not today's price" in text and bf.SHARE_PRICE_DATE in text
    assert "still hypothetical" in text
    assert "None" not in text


def test_every_hard_coded_source_is_an_https_link():
    for url in (bf.SOURCE_URL, bf.SHARE_PRICE_SOURCE, *bf.REPORTED_PRESS_SOURCES):
        assert url.startswith("https://")
