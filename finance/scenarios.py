"""Named base, upside and downside scenarios for the RFQ-automation investment, plus an NPV decision threshold.

Built on finance.full_model.financials (the Python twin of the Excel model). Tags: the 25% base and 12.5% conservative
win-back come from the project's own cases; every other value here is an ILLUSTRATIVE assumption, not observed data.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from finance.full_model import FinancialAssumptions, financials


@dataclass(frozen=True)
class Scenario:
    name: str
    win_back: float
    assumptions: FinancialAssumptions
    note: str


SCENARIOS = (
    Scenario("downside", 0.125, FinancialAssumptions(working_capital_days=60, run_cost=250000),
             "Conservative win-back (project case); 60 working-capital days and 2.5 lakh run cost are assumptions"),
    Scenario("base", 0.25, FinancialAssumptions(), "Base win-back and assumptions as in the Excel model"),
    Scenario("upside", 0.375, FinancialAssumptions(working_capital_days=30),
             "37.5% win-back and 30 working-capital days are illustrative assumptions"),
)


def run_scenarios(scenarios: tuple[Scenario, ...] = SCENARIOS) -> list[dict[str, Any]]:
    rows = []
    for s in scenarios:
        f = financials(s.win_back, s.assumptions)
        rows.append({
            "scenario": s.name, "win_back": s.win_back, "revenue": f["revenue"], "contribution": f["contribution"],
            "npv": f["npv"], "irr": f["irr"], "payback_years": f["payback_years"],
            "peak_funding": -f["deepest_cash_need"], "note": s.note,
        })
    return rows


def npv_break_even_win_back(assumptions: FinancialAssumptions = FinancialAssumptions(), tolerance: float = 1e-6) -> float | None:
    """Lowest win-back rate at which three-year NPV is zero (decision threshold). None if not reached by 100%."""
    if financials(1.0, assumptions)["npv"] < 0:
        return None
    lo, hi = 0.0, 1.0
    while hi - lo > tolerance:
        mid = (lo + hi) / 2
        if financials(mid, assumptions)["npv"] >= 0:
            hi = mid
        else:
            lo = mid
    return hi
