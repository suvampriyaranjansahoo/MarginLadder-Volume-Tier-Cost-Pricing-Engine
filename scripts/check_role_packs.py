"""Check the role evidence packs (PM, APM, consulting, BA, finance). Exit 1 if any check fails."""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import make_pm_artifacts as pm  # noqa: E402

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, bool(ok), detail))


def text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


# PM plan: one Accountable per task, 3 gates on days 15 / 25 / 35, critical path exists, effort near the earlier plan
tasks = pm.load()
end = pm.schedule(tasks)
problems = pm.checks(tasks, end)
check("PM plan passes its own checks (one A per task, 3 gates, horizon)", not problems, "; ".join(problems))
crit = [t for t, r in tasks.items() if r["critical"]]
check("PM critical path is computed and has slack elsewhere", bool(crit) and any(r["slack"] > 0 for r in tasks.values()), ",".join(crit))
prov = sum(r["prov"] for r in tasks.values()) * (1 + pm.PM_OVERHEAD) * (1 + pm.CONTINGENCY)
check("PM effort is within 5% of the earlier 120 person-day plan", abs(prov / pm.EARLIER_PLAN_PD - 1) < 0.05, f"{prov:.1f}")
for rel in ("docs/pm/gantt_12_week.png", "docs/pm/schedule_and_critical_path.md", "docs/pm/raci_tasks.md", "docs/pm/resourcing_effort.md"):
    check(f"generated file exists: {rel}", (ROOT / rel).is_file())

# RAID: at least 12 entries with every field filled
raid_rows = [ln for ln in text("docs/pm/raid_log.md").splitlines() if re.match(r"\| [RAID]\d\d \|", ln)]
cells_ok = all(len([c for c in ln.strip("|").split("|") if c.strip()]) >= 11 for ln in raid_rows)
check("RAID log has 12 or more entries, all fields filled", len(raid_rows) >= 12 and cells_ok, str(len(raid_rows)))
st = text("docs/pm/status_reports_templates.md")
check("three status-report TEMPLATES, each with a decisions-needed line",
      st.count("**Label:** TEMPLATE") == 3 and st.count("**Decisions needed:**") == 3)

# BA: every business rule BR-01..BR-26 appears in a traceability document; open items are labelled
trace = text("docs/requirements_traceability_v3.md") + text("docs/ba/complete_traceability_and_process_pack.md")
rules_in_catalogue = set(re.findall(r"^\| (BR-\d\d) \|", text("docs/ba/business_rules.md"), flags=re.M))

def _expand(txt: str) -> set[str]:
    out = set(re.findall(r"BR-\d\d", txt))
    for lo, hi in re.findall(r"BR-(\d\d) to BR-(\d\d)", txt):
        out |= {f"BR-{i:02d}" for i in range(int(lo), int(hi) + 1)}
    return out


missing = sorted(rules_in_catalogue - _expand(trace))
check("every business rule BR-01..BR-26 appears in a traceability table", not missing and len(rules_in_catalogue) == 26, ",".join(missing))
check("10 edge cases listed", len(re.findall(r"^\| EC-?\d+", text("docs/ba/complete_traceability_and_process_pack.md"), flags=re.M)) >= 10)
check("UAT run-log template is header-only", len((ROOT / "data/templates/uat_execution_log_template.csv").read_text(encoding="utf-8").splitlines()) == 1)

# Finance: workbook has the audit and tornado sheets, saved values, no error values
wbf = load_workbook(ROOT / "model/MarginLadder_Monthly_FP&A_Model.xlsx")
wbv = load_workbook(ROOT / "model/MarginLadder_Monthly_FP&A_Model.xlsx", data_only=True)
check("workbook has Audit Checks and Tornado sheets", {"Audit Checks", "Tornado"} <= set(wbf.sheetnames))
errs = [f"{ws.title}!{c.coordinate}" for ws in wbv for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith("#")]
check("no error values in the workbook", not errs, ",".join(errs[:5]))
tv = wbv["Tornado"]
check("Tornado check cell says PASS", tv["B14"].value == "PASS", str(tv["B14"].value))
check("Tornado ranks 1 and 2 are win-back and lost-RFQ rate",
      {tv.cell(r, 1).value for r in range(5, 11) if tv.cell(r, 9).value in (1, 2)} == {"Effective win-back (adoption x lift)", "Lost-RFQ rate"})
check("every audit check row passes", all(wbv["Audit Checks"].cell(r, 4).value == "PASS" for r in range(2, 8)))
check("tornado picture exists", (ROOT / "docs/finance/tornado.png").is_file())

# Consulting: deck has 16 slides and the three added slides are before the appendix
with zipfile.ZipFile(ROOT / "docs/consulting/MarginLadder_Executive_Recommendation.pptx") as z:
    n = sum(1 for x in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", x))
    last = z.read("ppt/slides/slide16.xml").decode("utf-8", "ignore") if n == 16 else ""
check("deck has 16 slides", n == 16, str(n))
check("appendix is the last slide", "Sources and boundaries" in last)

failed = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(("PASS  " if ok else "FAIL  ") + name + (f"  [{detail}]" if detail and not ok else ""))
print(f"{len(results) - len(failed)} of {len(results)} role-pack checks passed")
sys.exit(1 if failed else 0)
