"""Compare the Python model with the Excel workbook, cell by cell.

Run:  python3 -m finance.reconcile
Every row prints the sheet, the cell, the Excel value, the Python value and PASS or FAIL.
The workbook is read as saved (cached values), so open and save it in Excel after any edit.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import openpyxl

from finance import full_model as fm
from finance.case_model import calculate

WORKBOOK = Path(__file__).resolve().parents[1] / "model" / "MarginLadder_finance_model.xlsx"


@dataclass
class Check:
    sheet: str
    cell: str
    label: str
    excel: object
    python: object
    ok: bool


def _close(a, b, tol=1e-6):
    if isinstance(a, str) or isinstance(b, str) or a is None or b is None:
        return a == b
    return abs(float(a) - float(b)) <= tol * max(1.0, abs(float(a)))


def reconcile(path: Path = WORKBOOK) -> list[Check]:
    wb = openpyxl.load_workbook(path, data_only=True)
    out: list[Check] = []

    def add(sheet, cell, label, py, tol=1e-6):
        excel = wb[sheet][cell].value
        out.append(Check(sheet, cell, label, excel, py, _close(excel, py, tol)))

    base = calculate()
    m = "Model"
    add(m, "B5", "RFQs per year", base.annual_rfqs)
    add(m, "B6", "Lost RFQs per year", float(base.annual_lost_rfqs))
    add(m, "B8", "Margin ceiling", float(base.lost_rfq_margin_pool))
    add(m, "B9", "Recovered margin", float(base.annual_recovered_margin))
    add(m, "B10", "Net recovered margin", float(base.annual_net_benefit_after_run_cost))
    add(m, "B11", "Payback before running cost", 800000 / float(base.annual_recovered_margin) * 12)
    add(m, "B12", "Payback after running cost", 800000 / float(base.annual_net_benefit_after_run_cost) * 12)
    add(m, "B13", "Break-even win-back (fee only)", 800000 / float(base.lost_rfq_margin_pool))
    add(m, "B14", "Break-even win-back (with running cost)", float(base.break_even_win_back_rate_including_one_year_run_cost))
    add(m, "B16", "Hours freed", float(base.annual_hours_released))
    add(m, "B17", "Value of freed time", float(base.theoretical_capacity_value))
    add(m, "B18", "Estimator load today", fm.estimator_load(2.5))
    add(m, "B19", "Estimator load at target", fm.estimator_load(1.0))
    add(m, "B20", "3-year NPV, margin only", fm.margin_only_npv(0.25))

    for row, wbk in zip(range(4, 13), (0.0, 0.05, 0.0926, 0.125, 0.15, 0.20, 0.25, 0.35, 0.50), strict=True):
        s = fm.sensitivity_row(wbk)
        add("Sensitivity", f"B{row}", f"Recovered margin at {wbk:.2%}", s["recovered"])
        add("Sensitivity", f"E{row}", f"NPV at {wbk:.2%}", s["npv"])
        if s["payback_net_months"] is not None:
            add("Sensitivity", f"D{row}", f"Payback after running cost at {wbk:.2%}", s["payback_net_months"], 1e-4)

    f = fm.financials()
    add("Financials", "C11", "Incremental revenue", f["revenue"])
    add("Financials", "C14", "EBITDA", f["ebitda"])
    add("Financials", "C17", "Tax (shown negative)", -f["tax"])
    add("Financials", "C18", "Net income", f["net_income"])
    add("Financials", "C22", "Working capital balance", f["working_capital"])
    for col, cf in zip("BCDE", f["free_cash_flow"], strict=True):
        add("Financials", f"{col}26", f"Free cash flow ({col})", cf)
    add("Financials", "B41", "IRR over 3 years", f["irr"], 1e-5)
    add("Financials", "B42", "NPV", f["npv"])
    add("Financials", "B43", "Payback (years)", f["payback_years"], 1e-5)
    add("Financials", "B46", "Deepest cumulative cash need", f["deepest_cash_need"])
    wc_off = fm.financials(a=fm.FinancialAssumptions(release_wc_at_end=False))
    add("Financials", "B47", "IRR if working capital is never released", wc_off["irr"], 1e-5)

    gap = fm.cash_gap(8)
    for week, value in enumerate(gap["gap_by_week"], start=1):
        add("Cash", f"E{11 + week}", f"Funded gap, week {week}", value)
    add("Cash", "B20", "Peak funded gap", gap["peak"])
    add("Cash", "B21", "Peak as % of fee", gap["peak_pct_of_fee"], 1e-5)
    add("Cash", "B22", "Week of the peak", gap["peak_week"])
    return out


def main() -> int:
    checks = reconcile()
    for c in checks:
        print(f"{'PASS' if c.ok else 'FAIL'}  {c.sheet}!{c.cell:<4} {c.label:<45} excel={c.excel!s:<22} python={c.python}")
    failed = [c for c in checks if not c.ok]
    print(f"\n{len(checks) - len(failed)} of {len(checks)} cells match")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
