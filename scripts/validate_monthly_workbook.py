"""Independent semantic checks for the recruiter-facing monthly FP&A workbook.

This deliberately calculates key base-case outputs in Python rather than trusting
Excel's stored formula cache. Excel recalculates the formulas when opened.
"""
from decimal import Decimal as D
from pathlib import Path
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "model" / "MarginLadder_Monthly_FP&A_Model.xlsx"
wb = load_workbook(PATH, data_only=False)
assert {"Dashboard", "Inputs", "Monthly Plan", "Variance", "Sensitivity", "Control Checks", "Sources", "Adoption Economics"}.issubset(wb.sheetnames)
inputs = wb["Inputs"]
monthly = wb["Monthly Plan"]
adoption = wb["Adoption Economics"]
# Independent read of the explicit assumptions (not formula cache values).
rfq_month = D(str(inputs["B5"].value)); lost_rate = D(str(inputs["B6"].value))
aov = D(str(inputs["B7"].value)); cm = D(str(inputs["B8"].value))
run_cost = D(str(inputs["B10"].value)); implementation = D(str(inputs["B11"].value))
adopt = D(str(adoption["B6"].value)); lift = D(str(adoption["C6"].value))
effective = adopt * lift
annual_rfqs = rfq_month * 12
lost_rfqs = annual_rfqs * lost_rate
pool = lost_rfqs * aov * cm
contribution = pool * effective
net = contribution - run_cost
payback = implementation / net * 12
assert effective == D("0.2500")
assert annual_rfqs == D("720") and lost_rfqs == D("36.00")
assert pool == D("8640000.0000") and contribution == D("2160000.000000")
assert net == D("1960000.000000")
assert D(str(payback.quantize(D("0.1")))) == D("4.9")
# Critical formula links must be live formulas, not pasted values.
assert inputs["B9"].value == "='Adoption Economics'!D6"
assert monthly["D5"].value == "=C5*Inputs!$B$9"
assert monthly["E5"].value == "=D5*Inputs!$B$7"
assert monthly["F5"].value == "=E5*Inputs!$B$8"
assert monthly["H5"].value == "=F5-G5"
assert adoption["D6"].value == "=B6*C6"
# Formula integrity: no Excel error literals in formula text and formula cells exist.
formula_cells = [(ws.title, c.coordinate, c.value) for ws in wb for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith("=")]
assert len(formula_cells) >= 400
assert not any(any(err in f.upper() for err in ("#REF!", "#DIV/0!", "#VALUE!", "#NAME?")) for _, _, f in formula_cells)
print(f"PASS: independent base-case bridge; {len(formula_cells)} formulas; adoption={effective:.1%}; contribution=INR {contribution:,.0f}; net=INR {net:,.0f}; operating payback={payback:.1f} months")
