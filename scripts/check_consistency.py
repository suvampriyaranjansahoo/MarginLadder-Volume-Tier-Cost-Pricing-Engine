"""Check that the repo agrees with itself where a script can tell.

Run:  python3 scripts/check_consistency.py
Checks: numbers.json, figures quoted in documents, test names, links, original files, banned text, files present.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import zipfile
from collections.abc import Callable
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

RESULTS: list[tuple[str, bool, str]] = []
TAGS = {"Brief", "Derived", "Assumption", "Judgement", "Simulated", "External"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "node_modules"}


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(ok), detail))


def files(pattern: str) -> list[Path]:
    return [p for p in ROOT.rglob(pattern) if not (set(p.relative_to(ROOT).parts) & SKIP_DIRS)]


def text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def lakh(x: float) -> str:
    return f"{x:.1f}".rstrip("0").rstrip(".") if x != int(x) else str(int(x))


# 1. numbers.json is complete, tagged and regenerates identically
def numbers_checks() -> dict:
    import build_numbers

    saved = json.loads(text("numbers.json"))
    fresh = build_numbers.build()
    check("numbers.json regenerates identically", json.loads(json.dumps(fresh)) == saved)
    for key, item in saved.items():
        check(f"numbers.{key} has a known tag", item.get("tag") in TAGS, str(item.get("tag")))
        check(f"numbers.{key} has a source", bool(item.get("source")))
        check(f"numbers.{key} is a number", isinstance(item.get("value"), int | float))
    return saved


# 2. Figures quoted in documents match numbers.json
def quoted_figures(n: dict) -> None:
    v = {k: x["value"] for k, x in n.items()}
    expectations: list[tuple[str, str, str]] = [
        ("README.md", f"₹{lakh(v['margin_pool_lakh'])} lakh", "margin pool"),
        ("README.md", f"₹{lakh(v['recovered_margin_base_lakh'])} / ₹{lakh(v['recovered_margin_conservative_lakh'])} lakh", "recovered margin"),
        ("README.md", f"{v['payback_months_base_net']} months", "payback net"),
        ("README.md", f"{v['payback_months_cons_net']:.1f}", "payback cons"),
        ("README.md", f"{v['cash_payback_months']} months", "cash payback"),
        ("README.md", f"{v['irr_3yr'] * 100:.1f}%", "irr"),
        ("README.md", f"₹{v['deepest_cash_need_inr'] / 1e5:.1f} lakh", "deepest cash need"),
        ("README.md", f"{v['hours_released_gross']:,.0f} / {v['hours_released_net']:,.0f}", "hours"),
        ("README.md", f"{v['estimator_load_today'] * 100:.0f}% / {v['estimator_load_target'] * 100:.0f}%", "load"),
        ("README.md", f"{v['queue_wait_days_today']} day", "queue wait"),
        ("README.md", f"{v['capacity_break_even_fit'] * 100:.0f}%", "capacity fit"),
        ("README.md", f"{v['break_even_win_back_with_run_cost'] * 100:.1f}%", "break-even"),
        ("README.md", f"{v['break_even_win_back_fee_only'] * 100:.1f}%", "break-even fee only"),
        ("docs/finance/capacity_and_queue.md", f"{v['queue_wait_days_today']} day", "queue wait"),
        ("docs/finance/capacity_and_queue.md", f"{v['capacity_break_even_fit'] * 100:.0f}%", "capacity fit"),
        ("docs/finance/capacity_and_queue.md", f"{v['rfqs_in_progress_today']:.0f} to {v['rfqs_in_progress_target']:.0f}", "WIP"),
        ("docs/finance/model_audit.md", f"{v['cash_payback_months']} months", "cash payback"),
        ("docs/finance/model_audit.md", f"IRR {v['irr_3yr'] * 100:.1f}%", "irr"),
        ("docs/finance/model_audit.md", f"₹{v['deepest_cash_need_inr'] / 1e5:.1f} lakh", "cash need"),
        ("docs/finance/model_audit.md", f"{v['break_even_win_back_with_run_cost'] * 100:.1f}%", "break-even"),
        ("docs/finance/model_audit.md", f"{v['hours_released_net']:,.0f} h", "net hours"),
        ("docs/product/PRD_v3.md", f"{v['break_even_win_back_with_run_cost'] * 100:.1f}%", "break-even"),
        ("docs/product/PRD_v3.md", f"{v['capacity_break_even_fit'] * 100:.0f}%", "capacity fit"),
        ("docs/strategy/rollout_30_60_90.md", f"{v['cash_payback_months']} months", "cash payback"),
        ("docs/strategy/rollout_30_60_90.md", f"₹{lakh(v['margin_pool_lakh'])} lakh", "pool"),
        ("docs/go_no_go_memo.md", f"{v['break_even_win_back_with_run_cost'] * 100:.1f}%", "break-even"),
        ("docs/case_interview_5min.md", f"{v['break_even_win_back_with_run_cost'] * 100:.1f}%", "break-even"),
    ]
    for rel, needle, label in expectations:
        check(f"{rel} quotes {label} ({needle})", needle in text(rel), needle)


# 3. Test names cited in docs exist in test files
def test_names() -> None:
    defined: set[str] = set()
    for p in files("test_*.py"):
        defined.update(re.findall(r"def (test_\w+)", p.read_text(encoding="utf-8")))
    check("tests are defined", len(defined) >= 100, str(len(defined)))
    for p in files("*.md"):
        rel = str(p.relative_to(ROOT))
        for name in set(re.findall(r"`(test_\w+)`", p.read_text(encoding="utf-8"))):
            check(f"{rel} cites existing test {name}", name in defined)


# 4. Relative links, images and cited paths resolve
def links() -> None:
    link_re = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
    path_re = re.compile(r"`((?:docs|application|finance|tracekit|analytics|scripts|engine|model|prototype|data)/[\w./-]+\.\w+)`")
    skip_dirs = {ROOT / "docs" / "finance" / "extension_summary.md"}
    for p in files("*.md"):
        if p in skip_dirs:
            continue
        rel = str(p.relative_to(ROOT))
        body = p.read_text(encoding="utf-8")
        for target in set(link_re.findall(body)):
            if target.startswith(("http", "#", "mailto:")):
                continue
            tgt = (p.parent / target.split("#")[0]).resolve()
            check(f"{rel} link {target} resolves", tgt.exists())
        for target in set(path_re.findall(body)):
            if "*" in target or "your_file" in target or "demo_credentials" in target or target.endswith(".db"):
                continue
            check(f"{rel} cites existing path {target}", (ROOT / target).exists() or (p.parent / target).exists())


# 5. Original v2.0 files are unchanged unless the change is logged
def originals() -> None:
    m = json.loads(text("scripts/original_manifest.json"))
    logged = set(m["logged_changes"])
    for rel, digest in m["v2_0_sha256"].items():
        p = ROOT / rel
        if rel in logged:
            check(f"original {rel} changed only as logged", True, m["logged_changes"][rel])
        else:
            same = p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() == digest
            check(f"original {rel} is byte-identical", same)


# 6. Banned text and stray files
def banned() -> None:
    patterns = {
        "earlier-pack name": r"Iso" + r"code",
        "private key": r"BEGIN (RSA |EC )?PRIVATE KEY",
        "stale test claim": r"27 application",
        "stale auth claim": r"not authentication",
        "stale FR range": r"FR-01 to FR-12",
        "claims deployment": r"(?i)\b(is|was|been) deployed (to|at|on)\b",
        "claims users": r"(?i)\b\d+ (active )?users (have|use|used)\b",
    }
    docs = [p for p in files("*") if p.suffix in {".md", ".py", ".txt", ".html", ".yml", ".toml"} and p.name != "check_consistency.py"]
    check("text files scanned", len(docs) > 30, str(len(docs)))
    stale = {"stale test claim", "stale auth claim", "stale FR range"}
    manifest = json.loads(text("scripts/original_manifest.json"))
    untouched = {rel for rel in manifest["v2_0_sha256"] if rel not in manifest["logged_changes"]}
    for label, pat in patterns.items():
        # The manifest is stored with POSIX separators even when the validation
        # runs on Windows.  Keep immutable baseline files out of stale-text
        # scans without relying on the host path separator.
        pool = [p for p in docs if not (label in stale and p.relative_to(ROOT).as_posix() in untouched)]
        hits = [str(p.relative_to(ROOT)) for p in pool if re.search(pat, p.read_text(encoding="utf-8", errors="ignore"))]
        check(f"no '{label}' anywhere", not hits, ", ".join(hits[:3]))
    check("no database files", not files("*.db"))
    check("no demo credentials file", not (ROOT / "application/data/demo_credentials.txt").exists())
    # Bytecode and tool caches are ordinary generated artefacts; .gitignore keeps them
    # out of version control. They must not make an otherwise clean post-test check fail.
    gitignore = text(".gitignore")
    check("generated Python/tool caches are gitignored", all(token in gitignore for token in
          ("__pycache__/", ".pytest_cache/", ".mypy_cache/", ".ruff_cache/")))
    check("credentials are gitignored", "demo_credentials.txt" in text(".gitignore"))
    check("role_positioning is not in the public repo", not (ROOT / "docs/interview/role_positioning.md").exists())


# 7. Required files and labels
def required() -> None:
    must = [
        "README.md", "numbers.json", "pyproject.toml", "Dockerfile", "Makefile", "requirements.txt", "requirements-dev.txt",
        ".github/workflows/ci.yml", "docs/START_HERE.md", "docs/product/PRD_v3.md", "docs/product/decision_log.md",
        "docs/product/roadmap.md", "docs/product/pilot_design.md", "docs/product/rice_sensitivity.md",
        "docs/ba/business_rules.md", "docs/ba/data_dictionary.md", "docs/ba/use_cases.md", "docs/ba/uat_scripts.md",
        "docs/ba/glossary.md", "docs/ba/change_requests.md", "docs/requirements_traceability_v3.md",
        "docs/finance/model_audit.md", "docs/finance/capacity_and_queue.md", "docs/analytics/sql_findings.md",
        "docs/strategy/rollout_30_60_90.md", "docs/upgrade_regression_report_v3.md",
        "docs/finance/monthly_variance_analysis.md", "docs/product/simulated_product_analytics.md",
        "docs/portfolio/role_positioning.md", "docs/consulting/case_deck.md",
        "docs/ba/uat_execution_coverage.md", "docs/analytics/trace_to_sql.md", "docs/upgrade_regression_report_v3_1.md",
        "finance/variance.py", "analytics/product_metrics.py", "data/finance_actual_vs_budget_sample.csv",
        "data/product_events_sample.csv",
        "docs/analysis/queue_wait_curve.png", "docs/analysis/capacity_grid.png", "docs/analysis/margin_bridge.png",
        "docs/ba/diagrams/er.png", "docs/ba/diagrams/states.png", "tracekit/rfq_trace_template.csv",
        "finance/reconcile.py", "analytics/queries.sql", "scripts/original_manifest.json", "CHANGE_LOG.md",
        "finance/monthly_plan.py", "finance/test_monthly_plan.py", "model/MarginLadder_Monthly_FP&A_Model.xlsx",
        "docs/finance/monthly_planning_model.md", "docs/ba/discovery_and_uat_execution_pack.md",
        "docs/product/discovery_and_usability_pack.md", "docs/portfolio/one_minute_case_brief.md",
        "docs/portfolio/release_evidence_matrix.md", "docs/portfolio/research_source_register.md",
        "docs/portfolio/ai_use_disclosure.md", "docs/portfolio/final_execution_checklist.md",
        "docs/portfolio/role_paths/finance_analyst.md", "docs/portfolio/role_paths/business_analyst.md",
        "docs/portfolio/role_paths/consulting_analyst.md", "docs/portfolio/role_paths/apm.md",
        "docs/research/india_auto_components_context_2026.md", "docs/consulting/MarginLadder_Executive_Recommendation.pptx",
        "data/templates/discovery_interview_log_template.csv", "data/templates/usability_session_template.csv",
        "data/templates/uat_execution_log_template.csv", "data/templates/rfq_monthly_actuals_template.csv",
        "docs/upgrade_regression_report_v3_2.md", "docs/upgrade_regression_report_v3_2_1.md", "docs/portfolio/release_signoff.md",
        "scripts/portfolio_release_audit.py",
    ]
    for rel in must:
        check(f"required file {rel}", (ROOT / rel).exists())
    check("SQL findings say simulated", "simulated" in text("docs/analytics/sql_findings.md").lower())
    check("pilot design cites sample sizes", "per arm" in text("docs/product/pilot_design.md").lower() or "RFQs" in text("docs/product/pilot_design.md"))
    check("README is 120 lines or fewer", len(text("README.md").splitlines()) <= 120)
    readme = text("README.md").lower()
    check("README discloses hypothetical case and absence of production users",
          "hypothetical" in readme and "production users" in readme and "no real customer interviews" in readme)
    check("rules BR-01..BR-26 present", all(f"BR-{i:02d}" in text("docs/ba/business_rules.md") for i in range(1, 27)))
    check("decisions D-01..D-13 present", all(f"D-{i:02d}" in text("docs/product/decision_log.md") for i in range(1, 14)))
    check("use cases UC-01..UC-07 present", all(f"UC-{i:02d}" in text("docs/ba/use_cases.md") for i in range(1, 8)))
    check("UAT-01..UAT-12 present", all(f"UAT-{i:02d}" in text("docs/ba/uat_scripts.md") for i in range(1, 13)))
    check("portfolio package version is 3.3.0", 'version = "3.3.0"' in text("pyproject.toml"))
    check("local app API version remains 3.1.0", 'VERSION = "3.1.0"' in text("application/server.py"))
    check("monthly plan states modelled scope", "not actuals" in text("finance/monthly_plan.py").lower())
    check("monthly plan tests cover downside cases", "zero" in text("finance/test_monthly_plan.py").lower() and "win_back" in text("finance/test_monthly_plan.py"))
    check("four interview / UAT templates are header-only", all(len((ROOT / f).read_text(encoding="utf-8").splitlines()) == 1 for f in [
        "data/templates/discovery_interview_log_template.csv", "data/templates/usability_session_template.csv",
        "data/templates/uat_execution_log_template.csv", "data/templates/rfq_monthly_actuals_template.csv"]))
    deck_path = ROOT / "docs/consulting/MarginLadder_Executive_Recommendation.pptx"
    if deck_path.exists():
        with zipfile.ZipFile(deck_path) as deck_zip:
            slide_count = sum(1 for name in deck_zip.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name))
    else:
        slide_count = 0
    check("consulting deck contains 16 slides", slide_count == 16, str(slide_count))
    check("server never reads a role from the body", "actor:" not in text("application/server.py").split("class ")[1] if "class " in text("application/server.py") else True)


# 7b. Negative checks: things that must not appear
def negatives(n: dict) -> None:
    v = {k: x["value"] for k, x in n.items()}
    gross, net = f"{v['hours_released_gross']:,.0f}", f"{v['hours_released_net']:,.0f}"
    for rel in ["README.md", "docs/finance/model_audit.md", "docs/product/PRD_v3.md"]:
        body = text(rel)
        check(f"{rel} gives net hours whenever it gives gross", gross not in body or net in body)
    check("README gives IRR without working-capital release", f"{v['irr_3yr_no_wc_release'] * 100:.1f}%" in text("README.md"))
    check("README says the brief is hypothetical", "hypothetical" in text("README.md"))
    check("no document names a gate day other than 15 or 25", not re.search(r"Gate 3 \(day (?!25)\d+", "".join(text(str(p.relative_to(ROOT))) for p in files("*.md"))))
    check("no doc claims a file upload exists", not re.search(r"(?i)\bupload(s|ed)? (a|the) (drawing|file)", text("docs/product/PRD_v3.md")))
    check("UAT status is stated", "not yet executed" in text("docs/ba/uat_scripts.md"))


# 8. Python twin still matches Excel
def reconcile() -> None:
    out = subprocess.run(  # noqa: S603 -- fixed interpreter and fixed local module, not user input
        [sys.executable, "-B", "-m", "finance.reconcile"], cwd=ROOT, capture_output=True, text=True, check=False
    )
    check("Excel and Python agree on every cell", out.returncode == 0 and "64 of 64" in out.stdout, out.stdout.strip().splitlines()[-1] if out.stdout else out.stderr[-200:])


def main() -> int:
    steps: list[Callable[[], object]] = [test_names, links, originals, banned, required, reconcile]
    numbers = numbers_checks()
    quoted_figures(numbers)
    negatives(numbers)
    for step in steps:
        step()
    failed = [r for r in RESULTS if not r[1]]
    for name, ok, detail in RESULTS:
        if not ok:
            print(f"FAIL  {name}  {detail}")
    print(f"{len(RESULTS) - len(failed)} of {len(RESULTS)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
