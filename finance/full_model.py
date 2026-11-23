"""Python twin of the Excel finance model (MarginLadder_finance_model.xlsx).

Reproduces the Model, Sensitivity, Financials and Cash sheets so that a test can compare
every headline cell with the workbook. Inputs are the workbook's own. Tags:
Brief = given in the case, Assumption = my estimate, Derived = worked out here.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal as D
from math import ceil

from finance.case_model import CaseInputs, calculate

# Weekly effort cost from the 24 person-week plan of the earlier plan (Cash sheet, B12:B18). [Brief of the earlier plan]
WEEKLY_EFFORT_COST = (68500, 110900, 136000, 124600, 109000, 121100, 52400)
MILESTONE_SHARES = (D("0.2"), D("0.2"), D("0.4"), D("0.2"))
MILESTONE_INVOICE_DAY = (0, 15, 25, 35)        # working days from signing, Gate 2/3/4 on days 15/25/35
WORKING_DAYS_PER_WEEK = 5


@dataclass(frozen=True)
class FinancialAssumptions:
    discount_rate: float = 0.12      # Assumption
    years: int = 3                   # Assumption
    tax_rate: float = 0.25           # Assumption
    working_capital_days: int = 45   # Assumption
    amortisation_years: int = 3      # Assumption
    release_wc_at_end: bool = True   # Assumption
    run_cost: float = 200000         # Assumption
    fee: float = 800000              # Brief


def margin_only_npv(win_back: float, a: FinancialAssumptions = FinancialAssumptions(), inputs: CaseInputs = CaseInputs()) -> float:
    """3-year NPV of net recovered margin less the fee (Model!B20). No tax, no working capital."""
    pool = float(calculate(inputs, win_back_rate=D(str(win_back))).lost_rfq_margin_pool)
    net = pool * win_back - a.run_cost
    return -a.fee + sum(net / (1 + a.discount_rate) ** t for t in range(1, a.years + 1))


def sensitivity_row(win_back: float, a: FinancialAssumptions = FinancialAssumptions()) -> dict[str, float | None]:
    pool = float(calculate().lost_rfq_margin_pool)
    recovered = pool * win_back
    net = recovered - a.run_cost
    return {
        "win_back": win_back,
        "recovered": recovered,
        "payback_gross_months": a.fee / recovered * 12 if recovered > 0 else None,
        "payback_net_months": a.fee / net * 12 if net > 0 else None,
        "npv": margin_only_npv(win_back, a),
    }


def estimator_load(hours_per_part: float, inputs: CaseInputs = CaseInputs(), productive_hours_month: int = 160) -> float:
    """Hours needed over hours available (Model!B18). 160 productive hours a month is an Assumption (A4)."""
    needed = inputs.rfqs_per_month * inputs.parts_per_rfq * hours_per_part
    return needed / (inputs.estimator_count * productive_hours_month)


def review_hours_per_year(inputs: CaseInputs = CaseInputs(), hours_per_rfq: float = 1.0) -> float:
    """One hour a quote to review the RFQ in the register [Assumption: the register adds a review step]."""
    return inputs.rfqs_per_month * inputs.months_per_year * hours_per_rfq


def net_capacity_value(inputs: CaseInputs = CaseInputs(), review_hours_per_rfq: float = 1.0) -> dict[str, float]:
    gross = float(calculate(inputs).annual_hours_released)
    review = review_hours_per_year(inputs, review_hours_per_rfq)
    net = gross - review
    return {"gross_hours": gross, "review_hours": review, "net_hours": net,
            "gross_value": gross * float(inputs.estimator_hourly_cost),
            "net_value": net * float(inputs.estimator_hourly_cost)}


def financials(win_back: float = 0.25, a: FinancialAssumptions = FinancialAssumptions()) -> dict:
    """Incremental P&L, cash flow and balance sheet for the client (Financials sheet)."""
    inp = CaseInputs()
    lost = float(calculate(inp).annual_lost_rfqs)
    revenue = lost * win_back * float(inp.average_order_value)           # 36 x 25% x 20 lakh = 1.8 crore
    contribution = revenue * float(inp.order_margin)
    ebitda = contribution - a.run_cost
    amort = a.fee / a.amortisation_years
    ebit = ebitda - amort
    tax = ebit * a.tax_rate
    net_income = ebit - tax
    wc = revenue * a.working_capital_days / 365
    fcf = [-a.fee]
    wc_prev = 0.0
    for year in range(1, a.years + 1):
        wc_now = wc if (year < a.years or not a.release_wc_at_end) else 0.0
        fcf.append(net_income + amort - (wc_now - wc_prev))
        wc_prev = wc_now
    cumulative = []
    running = 0.0
    for cf in fcf:
        running += cf
        cumulative.append(running)
    npv = sum(cf / (1 + a.discount_rate) ** t for t, cf in enumerate(fcf))
    return {
        "revenue": revenue, "contribution": contribution, "ebitda": ebitda, "amortisation": amort,
        "ebit": ebit, "tax": tax, "net_income": net_income, "working_capital": wc,
        "free_cash_flow": fcf, "cumulative_cash_flow": cumulative, "npv": npv,
        "irr": irr(fcf), "payback_years": payback_years(cumulative),
        "deepest_cash_need": min(cumulative),
    }


def irr(cash_flows: list[float], lo: float = -0.99, hi: float = 10.0) -> float | None:
    def f(r: float) -> float:
        return sum(cf / (1 + r) ** t for t, cf in enumerate(cash_flows))

    if f(lo) * f(hi) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def payback_years(cumulative: list[float]) -> float | None:
    """Years until cumulative cash turns positive, linear within the year it crosses (Financials!B43)."""
    for year in range(1, len(cumulative)):
        if cumulative[year] >= 0 > cumulative[year - 1]:
            step = cumulative[year] - cumulative[year - 1]
            return (year - 1) + (-cumulative[year - 1]) / step
    return None


def cash_gap(payment_days: int, fee: float = 800000, weekly_cost: tuple[int, ...] = WEEKLY_EFFORT_COST) -> dict:
    """Vendor funded gap on cash received (Cash sheet). Receipt day = invoice day + working days to pay."""
    weeks = len(weekly_cost)
    receipts = []
    for share, invoice_day in zip(MILESTONE_SHARES, MILESTONE_INVOICE_DAY, strict=True):
        pay_days = 0 if invoice_day == 0 else payment_days
        receipts.append((invoice_day + pay_days, float(share) * fee))
    gap, peak, peak_week, cum_cost = [], 0.0, 0, 0.0
    for week in range(1, weeks + 1):
        cum_cost += weekly_cost[week - 1]
        received = sum(amount for day, amount in receipts if day == 0 or ceil(day / WORKING_DAYS_PER_WEEK) <= week)
        gap.append(cum_cost - received)
        if gap[-1] > peak:
            peak, peak_week = gap[-1], week
    return {"gap_by_week": gap, "peak": peak, "peak_pct_of_fee": peak / fee, "peak_week": peak_week}
