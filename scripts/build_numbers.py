"""Write numbers.json: every headline figure in this repo, worked out once, with its tag and source.

README, docs and the app quote these values. scripts/check_consistency.py fails if a document disagrees.
Run:  python3 scripts/build_numbers.py
Tags: Brief = given, Derived = worked out from Brief and Assumption values, Assumption = my estimate.
"""
from __future__ import annotations

import json
import sys
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from finance import capacity, queueing  # noqa: E402
from finance import full_model as fm  # noqa: E402
from finance.case_model import calculate  # noqa: E402


def lakh(x: float) -> float:
    return round(x / 100000, 2)


def build() -> dict:
    base = calculate()
    cons = calculate(win_back_rate=D("0.125"))
    fin = fm.financials()
    net = fm.net_capacity_value()
    q_now, q_goal = queueing.mean_wait_days(60, 12.5, 6), queueing.mean_wait_days(60, 5, 6)
    gap10, gap3 = fm.cash_gap(8), fm.cash_gap(3)
    n: dict[str, dict] = {}

    def put(key: str, value, tag: str, source: str, unit: str = "") -> None:
        n[key] = {"value": value, "tag": tag, "source": source, "unit": unit}

    put("rfqs_per_year", base.annual_rfqs, "Derived", "60 x 12", "RFQs")
    put("lost_rfqs_per_year", float(base.annual_lost_rfqs), "Derived", "720 x 5%", "RFQs")
    put("margin_pool_inr", float(base.lost_rfq_margin_pool), "Derived", "36 x 20 lakh x 12%", "INR")
    put("win_back_base", 0.25, "Assumption", "50% of losses due to delay x 50% won once faster")
    put("win_back_conservative", 0.125, "Assumption", "half of base")
    put("recovered_margin_base_inr", float(base.annual_recovered_margin), "Derived", "pool x 25%", "INR")
    put("recovered_margin_base_lakh", lakh(float(base.annual_recovered_margin)), "Derived", "pool x 25%", "lakh")
    put("recovered_margin_conservative_lakh", lakh(float(cons.annual_recovered_margin)), "Derived", "pool x 12.5%", "lakh")
    put("margin_pool_lakh", lakh(float(base.lost_rfq_margin_pool)), "Derived", "ceiling, not relied on", "lakh")
    put("payback_months_base_gross", round(800000 / float(base.annual_recovered_margin) * 12, 2), "Derived", "fee / monthly margin", "months")
    put("payback_months_base_net", round(800000 / float(base.annual_net_benefit_after_run_cost) * 12, 2), "Derived", "after Rs 2 lakh a year running cost", "months")
    put("payback_months_cons_gross", round(800000 / float(cons.annual_recovered_margin) * 12, 2), "Derived", "fee / monthly margin at 12.5%", "months")
    put("payback_months_cons_net", round(800000 / float(cons.annual_net_benefit_after_run_cost) * 12, 2), "Derived", "after running cost at 12.5%", "months")
    put("break_even_win_back_fee_only", round(800000 / float(base.lost_rfq_margin_pool), 4), "Derived", "fee / pool")
    put("break_even_win_back_with_run_cost", round(float(base.break_even_win_back_rate_including_one_year_run_cost), 4), "Derived", "(fee + run) / pool")
    put("hours_released_gross", float(base.annual_hours_released), "Derived", "3,600 parts x 1.5 h", "hours")
    put("capacity_value_gross_lakh", lakh(float(base.theoretical_capacity_value)), "Derived", "5,400 h x Rs 450", "lakh")
    put("review_hours", net["review_hours"], "Assumption", "1 hour to review each of 720 RFQs a year", "hours")
    put("hours_released_net", net["net_hours"], "Derived", "gross minus review hours", "hours")
    put("capacity_value_net_lakh", lakh(net["net_value"]), "Derived", "4,680 h x Rs 450", "lakh")
    put("estimator_load_today", round(fm.estimator_load(2.5), 4), "Derived", "9,000 h / 11,520 h", "")
    put("estimator_load_target", round(fm.estimator_load(1.0), 4), "Derived", "3,600 h / 11,520 h", "")
    put("queue_wait_days_today", round(q_now["wait_days"], 2), "Assumption", "Erlang C, 6 servers, 12.5 h jobs, Poisson arrivals", "working days")
    put("queue_p_wait_today", round(q_now["p_wait"], 3), "Assumption", "Erlang C")
    put("queue_wait_days_target", round(q_goal["wait_days"], 3), "Assumption", "Erlang C at 5 h jobs", "working days")
    put("rfqs_in_progress_today", queueing.littles_law(60, 9), "Derived", "Little's law, 9 days", "RFQs")
    put("rfqs_in_progress_target", queueing.littles_law(60, 4), "Derived", "Little's law, 4 days", "RFQs")
    put("cash_payback_months", round(fin["payback_years"] * 12, 1), "Derived", "tax 25% and 45 working-capital days are assumptions", "months")
    put("irr_3yr", round(fin["irr"], 3), "Derived", "Financials sheet")
    put("irr_3yr_no_wc_release", round(fm.financials(a=fm.FinancialAssumptions(release_wc_at_end=False))["irr"], 3), "Derived", "Financials sheet B47, working capital never released")
    put("npv_after_tax_wc_inr", round(fin["npv"]), "Derived", "12% discount rate, Financials sheet", "INR")
    put("deepest_cash_need_inr", round(-fin["deepest_cash_need"]), "Derived", "client cumulative free cash flow", "INR")
    put("vendor_gap_net10_inr", gap10["peak"], "Derived", "Cash sheet, cash received basis, 8 working days to pay", "INR")
    put("vendor_gap_net10_pct", round(gap10["peak_pct_of_fee"], 3), "Derived", "of the Rs 8 lakh fee")
    put("vendor_gap_net10_week", gap10["peak_week"], "Derived", "Cash sheet", "week")
    put("vendor_gap_net3_inr", gap3["peak"], "Derived", "same plan at 3 days to pay", "INR")
    put("capacity_break_even_fit", round(capacity.break_even_fit() or 0, 3), "Derived", "(fee + run) / recovered margin")
    put("recovered_revenue_inr", capacity.recovered_revenue(), "Derived", "36 x 25% x Rs 20 lakh", "INR")
    return n


def main() -> int:
    data = build()
    (ROOT / "numbers.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"numbers.json written with {len(data)} figures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
