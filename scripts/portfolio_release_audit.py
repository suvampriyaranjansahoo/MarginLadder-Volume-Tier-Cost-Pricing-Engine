"""Audit the recruiter-facing artefacts in a MarginLadder portfolio release."""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    checks: list[tuple[str, bool, str]] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append((name, bool(condition), detail))

    required = [
        "README.md",
        "docs/START_HERE.md",
        "docs/portfolio/one_minute_case_brief.md",
        "docs/portfolio/release_signoff.md",
        "docs/portfolio/release_evidence_matrix.md",
        "docs/portfolio/ai_use_disclosure.md",
        "docs/portfolio/research_source_register.md",
        "docs/portfolio/final_execution_checklist.md",
        "docs/upgrade_regression_report_v3_2_1.md",
        "docs/one_page_memo.pdf",
        "docs/consulting/MarginLadder_Executive_Recommendation.pptx",
        "model/MarginLadder_Monthly_FP&A_Model.xlsx",
        "application/server.py",
        "engine/cost_engine.py",
        "finance/monthly_plan.py",
        "analytics/product_metrics.py",
        "tracekit/analyze.py",
    ]
    check("required recruiter and implementation artefacts exist", all((ROOT / p).is_file() for p in required))
    check("portfolio and application versions are intentionally distinct",
          'version = "3.3.0"' in (ROOT / "pyproject.toml").read_text(encoding="utf-8")
          and 'VERSION = "3.1.0"' in (ROOT / "application/server.py").read_text(encoding="utf-8"))

    role_files = {
        "Finance Analyst": "docs/portfolio/role_paths/finance_analyst.md",
        "Business Analyst": "docs/portfolio/role_paths/business_analyst.md",
        "Consulting Analyst": "docs/portfolio/role_paths/consulting_analyst.md",
        "Associate Product Manager": "docs/portfolio/role_paths/apm.md",
    }
    for role, rel in role_files.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        check(f"{role} path has a recruiter takeaway", "## Recruiter takeaway" in text)
        check(f"{role} path has a timed walkthrough", "60-second walkthrough" in text)
        check(f"{role} path has interview questions and claim boundary",
              "Questions to be ready for" in text and "Honest claim boundary" in text)

    workbook_path = ROOT / "model" / "MarginLadder_Monthly_FP&A_Model.xlsx"
    workbook = load_workbook(workbook_path, read_only=True, data_only=False)
    try:
        expected_sheets = {"Dashboard", "Inputs", "Monthly Plan", "Variance", "Sensitivity", "Control Checks", "Sources", "Adoption Economics", "Audit Checks"}
        check("monthly FP&A workbook has all nine expected sheets", expected_sheets.issubset(set(workbook.sheetnames)),
              ", ".join(workbook.sheetnames))
        formula_count = sum(
            1 for sheet in workbook.worksheets for row in sheet.iter_rows()
            for cell in row if isinstance(cell.value, str) and cell.value.startswith("=")
        )
        check("monthly FP&A workbook contains formula-driven schedules", formula_count >= 400, str(formula_count))
        inputs = workbook["Inputs"]
        check("effective win-back is formula-linked to adoption economics", inputs["B9"].value == "='Adoption Economics'!D6")
        error_cells = [
            f"{sheet.title}!{cell.coordinate}={cell.value}"
            for sheet in workbook.worksheets for row in sheet.iter_rows()
            for cell in row if cell.data_type == "e"
        ]
        check("monthly FP&A workbook has no stored Excel error cells", not error_cells, "; ".join(error_cells[:5]))
    finally:
        workbook.close()

    deck_path = ROOT / "docs" / "consulting" / "MarginLadder_Executive_Recommendation.pptx"
    try:
        with zipfile.ZipFile(deck_path) as deck:
            bad_member = deck.testzip()
            slide_count = sum(bool(re.fullmatch(r"ppt/slides/slide\d+\.xml", name)) for name in deck.namelist())
        check("consulting presentation archive is structurally valid", bad_member is None, str(bad_member or "OK"))
        check("consulting presentation contains 16 slides", slide_count == 16, str(slide_count))
    except (OSError, zipfile.BadZipFile) as exc:
        check("consulting presentation archive is structurally valid", False, str(exc))
        check("consulting presentation contains 16 slides", False, "not readable")

    templates = [
        "data/templates/discovery_interview_log_template.csv",
        "data/templates/usability_session_template.csv",
        "data/templates/uat_execution_log_template.csv",
        "data/templates/rfq_monthly_actuals_template.csv",
    ]
    check("external-evidence templates are blank headers, not fabricated records",
          all((ROOT / rel).is_file() and len((ROOT / rel).read_text(encoding="utf-8").splitlines()) == 1 for rel in templates))

    evidence = (ROOT / "docs/validation/evidence_register.md").read_text(encoding="utf-8").lower()
    matrix = (ROOT / "docs/portfolio/release_evidence_matrix.md").read_text(encoding="utf-8").lower()
    field_protocol = (ROOT / "docs/portfolio/final_execution_checklist.md").read_text(encoding="utf-8").lower()
    check("evidence register distinguishes assumptions, derivations and synthetic data",
          all(term in evidence for term in ("assumption", "derived", "simulated", "not evidenced")))
    check("release matrix distinguishes artefact completion from external proof",
          "repository artefacts and reproducible portfolio checks are complete" in matrix
          and "real-world evidence" in matrix)
    check("field protocol states portfolio build is complete",
          "portfolio build status: complete" in field_protocol)
    check("synthetic datasets remain disclosed in recruiter entry point",
          "synthetic" in (ROOT / "README.md").read_text(encoding="utf-8").lower())
    signoff = (ROOT / "docs/portfolio/release_signoff.md").read_text(encoding="utf-8").lower()
    check("release sign-off explicitly rules out fabricated external proof",
          "not interviews" in signoff and "not represented as completed" in signoff)

    passed = sum(ok for _, ok, _ in checks)
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
    print(f"\n{passed}/{len(checks)} portfolio release audit checks passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
