"""Build the project-management pack from docs/pm/plan.csv.

Reads the plan, computes the schedule and critical path (forward and backward pass),
checks the plan, then writes the Gantt picture, schedule table, RACI table and effort table.
All dates are relative: day 1 is the day the agreement is signed. 5 working days = 1 week.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PM = ROOT / "docs/pm"
ROLES = {
    "MD": "Managing Director", "EH": "Estimation Head", "PH": "Plant Head", "SH": "Sales Head",
    "RO": "Rate owner", "IT": "Client IT", "PO": "Product owner (provider)",
    "DL": "Delivery lead (provider)", "BA": "Business analyst (provider)",
}
PROVIDER = {"PO", "DL", "BA"}
HORIZON_DAYS = 60
PM_OVERHEAD = 0.15
CONTINGENCY = 0.10
EARLIER_PLAN_PD = 24 * 5   # the earlier 24 person-week plan used by finance/full_model.py


def load() -> dict[str, dict]:
    tasks: dict[str, dict] = {}
    for r in csv.DictReader((PM / "plan.csv").open(encoding="utf-8")):
        r["duration_days"] = int(r["duration_days"])
        r["pred"] = [p for p in r["predecessors"].split("|") if p]
        for k in ("responsible", "consulted", "informed"):
            r[k] = [x for x in r[k].split("|") if x]
        r["prov"] = float(r["provider_effort_pd"])
        r["client"] = float(r["client_effort_pd"])
        tasks[r["id"]] = r
    return tasks


def schedule(tasks: dict[str, dict]) -> int:
    order: list[str] = []
    seen: set[str] = set()

    def visit(t: str) -> None:
        if t in seen:
            return
        seen.add(t)
        for p in tasks[t]["pred"]:
            visit(p)
        order.append(t)

    for t in tasks:
        visit(t)
    for t in order:
        r = tasks[t]
        r["es"] = 1 + max((tasks[p]["ef"] for p in r["pred"]), default=0)
        r["ef"] = r["es"] + r["duration_days"] - 1
    end = max(r["ef"] for r in tasks.values())
    succ: dict[str, list[str]] = {t: [] for t in tasks}
    for t, r in tasks.items():
        for p in r["pred"]:
            succ[p].append(t)
    for t in reversed(order):
        r = tasks[t]
        r["lf"] = min((tasks[s]["ls"] - 1 for s in succ[t]), default=end)
        r["ls"] = r["lf"] - r["duration_days"] + 1
        r["slack"] = r["ls"] - r["es"]
        r["critical"] = r["slack"] == 0
    return end


def checks(tasks: dict[str, dict], end: int) -> list[str]:
    problems = []
    for t, r in tasks.items():
        if r["accountable"] not in ROLES:
            problems.append(f"{t}: accountable '{r['accountable']}' is not a known role")
        for k in ("responsible", "consulted", "informed"):
            for x in r[k]:
                if x not in ROLES:
                    problems.append(f"{t}: unknown role {x} in {k}")
        if not r["responsible"]:
            problems.append(f"{t}: nobody responsible")
        if r["accountable"] in r["consulted"] + r["informed"]:
            problems.append(f"{t}: accountable person also listed as consulted or informed")
    gates = [t for t, r in tasks.items() if r["kind"] == "gate"]
    if len(gates) != 3:
        problems.append(f"expected 3 gates, found {len(gates)}")
    for g, day in (("G2", 15), ("G3", 25), ("G4", 35)):
        if tasks[g]["ef"] != day:
            problems.append(f"{g} is on day {tasks[g]['ef']}, expected day {day}")
    if end > HORIZON_DAYS:
        problems.append(f"plan ends on day {end}, past the {HORIZON_DAYS}-day horizon")
    if not any(r["critical"] for r in tasks.values()):
        problems.append("no critical path found")
    return problems


def gantt(tasks: dict[str, dict], end: int) -> None:
    items = sorted(tasks.values(), key=lambda r: (r["es"], r["ef"]))
    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    for i, r in enumerate(items):
        y = len(items) - i
        if r["kind"] == "gate":
            ax.plot(r["ef"] + 0.5, y, marker="D", ms=11, color="#b45309", zorder=4)
        else:
            colour = "#0f2742" if r["critical"] else "#7fa6c9"
            ax.barh(y, r["duration_days"], left=r["es"] - 0.5, height=0.55, color=colour,
                    hatch="//" if r["critical"] else None, edgecolor="white", zorder=3)
            if r["slack"] > 0:
                ax.barh(y, r["slack"], left=r["ef"] + 0.5, height=0.12, color="#c9d3dd", zorder=2)
        for p in r["pred"]:
            pf = tasks[p]
            ax.annotate("", xy=(r["es"] - 0.5, y), xytext=(pf["ef"] + 0.5, len(items) - items.index(pf)),
                        arrowprops=dict(arrowstyle="-", color="#9aa5b1", lw=0.6), zorder=1)
    ax.set_yticks([len(items) - i for i in range(len(items))])
    ax.set_yticklabels([f"{r['id']}  {r['name'][:52]}" for r in items], fontsize=8)
    ax.set_xticks([w * 5 + 0.5 for w in range(0, 13)])
    ax.set_xticklabels([f"W{w + 1}" if w < 12 else "" for w in range(0, 13)], fontsize=8)
    ax.set_xlim(0.5, HORIZON_DAYS + 0.5)
    for w in range(0, 13):
        ax.axvline(w * 5 + 0.5, color="#e5e9ee", lw=0.6, zorder=0)
    ax.set_xlabel("Weeks from signing (relative dates; day 1 = signing day). Dark hatched bar = critical path. "
                  "Diamond = gate. Thin grey line = slack (days the task can slip).", fontsize=8)
    ax.set_title("MarginLadder 12-week plan (hypothetical): the pilot sets the end date, not the build", fontsize=11, loc="left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(PM / "gantt_12_week.png", dpi=150)
    plt.close(fig)


def write_schedule(tasks: dict[str, dict], end: int) -> None:
    rows = sorted(tasks.values(), key=lambda r: (r["es"], r["ef"]))
    crit = [r["id"] for r in rows if r["critical"]]
    lines = [
        "# Schedule and critical path (generated)", "",
        "Generated by `scripts/make_pm_artifacts.py` from `docs/pm/plan.csv`. Do not edit by hand. "
        "**TEMPLATE plan for a hypothetical case: dates are relative to signing day, not calendar dates.** "
        "A working week has 5 days.", "",
        "![12-week Gantt chart](gantt_12_week.png)", "",
        f"**Critical path** (a task here that slips one day moves the end date one day): `{' > '.join(crit)}`. "
        f"Plan ends on day {end} of {HORIZON_DAYS}, so the buffer is {HORIZON_DAYS - end} days.", "",
        "| ID | Task | Start day | End day | Week | Slack (days) | Depends on | Owner (A) | Critical |",
        "|---|---|---:|---:|---|---:|---|---|---|",
    ]
    for r in rows:
        wk = f"W{(r['es'] - 1) // 5 + 1}" if (r['es'] - 1) // 5 == (r['ef'] - 1) // 5 else f"W{(r['es'] - 1) // 5 + 1}-W{(r['ef'] - 1) // 5 + 1}"
        lines.append(f"| {r['id']} | {r['name']} | {r['es']} | {r['ef']} | {wk} | {r['slack']} | "
                     f"{', '.join(r['pred']) or 'none'} | {r['accountable']} | {'**yes**' if r['critical'] else 'no'} |")
    lines += ["", "## How to read it in 60 seconds",
              "- **What is late?** In this template nothing is late, because nothing has started. In a live plan, "
              "anything on the critical path that slips is late for the whole project. Anything with slack can slip by that many days first.",
              "- **Who owns it?** The Owner (A) column. One name per task.",
              "- **What happens next?** Gates: Gate 2 on day 15 (register in daily use), Gate 3 on day 25 (full build or stop), "
              "Gate 4 on day 35 (prices match within INR 0.01). Pass rules are in `docs/strategy/rollout_30_60_90.md` and `docs/product/roadmap.md`.",
              "- **Why the pilot is critical:** `pilot_design.md` asks for at least 6 weeks of pilot data. Seven weeks starting right after Gate 2 "
              "ends on day 50, which is later than the build chain, so a late pilot start moves the read-out."]
    (PM / "schedule_and_critical_path.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_raci(tasks: dict[str, dict]) -> None:
    cols = list(ROLES)
    lines = ["# RACI by task (generated)", "",
             "Generated from `docs/pm/plan.csv`. **A = accountable, exactly one per task.** R = does the work, C = consulted, I = informed. "
             "`A/R` means the accountable person also does the work. A check in `scripts/check_role_packs.py` fails if any task has no A or more than one A.", "",
             "Role codes: " + "; ".join(f"**{k}** {v}" for k, v in ROLES.items()) + ".", "",
             "| ID | Task | " + " | ".join(cols) + " |", "|---|---|" + "---|" * len(cols)]
    for r in sorted(tasks.values(), key=lambda r: (r["es"], r["ef"])):
        cells = []
        for c in cols:
            tag = []
            if c == r["accountable"]:
                tag.append("A/R" if c in r["responsible"] else "A")
            elif c in r["responsible"]:
                tag.append("R")
            if c in r["consulted"]:
                tag.append("C")
            if c in r["informed"]:
                tag.append("I")
            cells.append(" ".join(tag))
        lines.append(f"| {r['id']} | {r['name']} | " + " | ".join(cells) + " |")
    lines += ["", "The stakeholder-level RACI for the product (who approves what) is in `docs/ba/raci_stakeholders.md`. This page is about delivering the plan."]
    (PM / "raci_tasks.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_effort(tasks: dict[str, dict]) -> dict:
    per_role: dict[str, float] = {k: 0.0 for k in ROLES}
    for r in tasks.values():
        prov_r = [x for x in r["responsible"] if x in PROVIDER] or ["PO"]
        for x in prov_r:
            per_role[x] += r["prov"] / len(prov_r)
        client_r = [x for x in r["responsible"] if x not in PROVIDER] or [r["accountable"]]
        for x in client_r:
            if x not in PROVIDER:
                per_role[x] += r["client"] / len(client_r)
    task_total = sum(r["prov"] for r in tasks.values())
    overhead = task_total * PM_OVERHEAD
    subtotal = task_total + overhead
    cont = subtotal * CONTINGENCY
    total = subtotal + cont
    client_total = sum(r["client"] for r in tasks.values())
    lines = ["# Resourcing and effort estimate (generated figures)", "",
             "**Hypothetical plan. These are planning estimates [Judgement], not timesheets.**", "",
             "## Method (bottom-up, in person-days)",
             "1. For each task in `docs/pm/plan.csv`, I estimated provider effort and client effort in person-days. "
             "Effort is not the same as duration: a 6-day build task can need 12 person-days.",
             "2. Provider effort is split equally between the provider people marked R on the task.",
             f"3. Add {int(PM_OVERHEAD * 100)}% for programme management (weekly status, RAID log, change control, gate packs) [Assumption].",
             f"4. Add {int(CONTINGENCY * 100)}% contingency on the subtotal [Assumption].",
             "5. Compare with the earlier 24 person-week plan used by the cash model (`finance/full_model.py`, 120 person-days).", "",
             "| Step | Person-days |", "|---|---:|",
             f"| Task effort, provider side (sum of plan.csv) | {task_total:.1f} |",
             f"| Programme management ({int(PM_OVERHEAD * 100)}%) | {overhead:.1f} |",
             f"| Subtotal | {subtotal:.1f} |",
             f"| Contingency ({int(CONTINGENCY * 100)}%) | {cont:.1f} |",
             f"| **Provider total** | **{total:.1f}** |",
             f"| Earlier plan (24 person-weeks x 5) | {EARLIER_PLAN_PD} |",
             f"| Difference | {total - EARLIER_PLAN_PD:+.1f} ({(total / EARLIER_PLAN_PD - 1) * 100:+.1f}%) |",
             f"| Client-side effort (people at the plant, not billed) | {client_total:.1f} |", "",
             "**Judgement call:** I set the task-level estimates so that the total lands close to the earlier 24 person-week plan. "
             "That makes the two numbers agree by design, so the match is a consistency check, not independent proof. "
             f"Implied price per provider person-day: INR 8,00,000 / {total:.0f} = about INR {800000 / total:,.0f}.", "",
             "## Effort by role (task effort only, before overhead and contingency)", "",
             "| Role | Person-days | Side |", "|---|---:|---|"]
    for k, v in per_role.items():
        if v:
            lines.append(f"| {ROLES[k]} | {v:.1f} | {'provider' if k in PROVIDER else 'client'} |")
    lines += ["", "## What would change this estimate",
              "- The Week 1 trace shows costing is over 40% of the cycle: scope cuts to the costing screen, so T10 and T15 shrink and T12 grows.",
              "- The rate master is late: T14 and T13 slip, but they have slack, so Gate 4 moves before the end date does.",
              "- Estimators will not use the register: T16 restarts, which moves the end date day for day (it is on the critical path)."]
    (PM / "resourcing_effort.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"total": total, "task_total": task_total, "client_total": client_total}


def main() -> int:
    tasks = load()
    end = schedule(tasks)
    problems = checks(tasks, end)
    if problems:
        print("PM PLAN CHECK FAILED")
        for p in problems:
            print(" -", p)
        return 1
    gantt(tasks, end)
    write_schedule(tasks, end)
    write_raci(tasks)
    eff = write_effort(tasks)
    crit = [t for t, r in tasks.items() if r["critical"]]
    print(f"PM plan OK: {len(tasks)} items, ends day {end}, critical path {' > '.join(sorted(crit, key=lambda t: tasks[t]['es']))}")
    print(f"provider effort {eff['total']:.1f} pd, client {eff['client_total']:.1f} pd")
    return 0


if __name__ == "__main__":
    sys.exit(main())
