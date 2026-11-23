"""Monthly actual-versus-budget analysis for the MarginLadder finance workstream.

The input schema is deliberately generic. The included CSV is simulated training data,
not a company's ledger. Revenue variances are favourable when actual exceeds budget;
cost variances are favourable when actual is below budget.
"""
from __future__ import annotations

import csv
from datetime import datetime
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

D = Decimal


class VarianceError(ValueError):
    """Invalid finance variance input."""


@dataclass(frozen=True)
class VarianceRow:
    period: str
    metric: str
    category: str
    budget: Decimal
    actual: Decimal

    @property
    def variance(self) -> Decimal:
        return self.actual - self.budget

    @property
    def variance_pct(self) -> Decimal | None:
        return self.variance / self.budget * 100 if self.budget else None

    @property
    def favourability(self) -> str:
        if self.actual == self.budget:
            return "On budget"
        favourable = self.actual > self.budget if self.category == "revenue" else self.actual < self.budget
        return "Favourable" if favourable else "Unfavourable"

    @property
    def favourable(self) -> bool:
        """Compatibility boolean; an on-budget outcome is treated as non-adverse."""
        return self.favourability != "Unfavourable"


def parse_rows(rows: list[dict[str, str]]) -> list[VarianceRow]:
    result: list[VarianceRow] = []
    seen: set[tuple[str, str]] = set()
    for line_no, row in enumerate(rows, start=2):
        period = (row.get("period") or "").strip()
        metric = (row.get("metric") or "").strip()
        category = (row.get("category") or "").strip().lower()
        try:
            datetime.strptime(period, "%Y-%m")
        except ValueError as exc:
            raise VarianceError(f"line {line_no}: period must be a valid YYYY-MM month") from exc
        if not metric or category not in {"revenue", "cost"}:
            raise VarianceError(f"line {line_no}: metric is required and category must be revenue or cost")
        key = (period, metric.casefold())
        if key in seen:
            raise VarianceError(f"line {line_no}: duplicate metric {metric!r} for {period}")
        seen.add(key)
        try:
            budget, actual = D(row["budget"]), D(row["actual"])
        except (KeyError, InvalidOperation) as exc:
            raise VarianceError(f"line {line_no}: budget and actual must be decimal numbers") from exc
        if not budget.is_finite() or not actual.is_finite() or budget < 0 or actual < 0:
            raise VarianceError(f"line {line_no}: budget and actual must be finite and non-negative")
        result.append(VarianceRow(period, metric, category, budget, actual))
    if not result:
        raise VarianceError("at least one monthly metric row is required")
    return sorted(result, key=lambda item: (item.period, item.category, item.metric))


def read_csv(path: str | Path) -> list[VarianceRow]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return parse_rows(list(csv.DictReader(handle)))


def monthly_summary(rows: list[VarianceRow]) -> list[dict[str, str | None]]:
    buckets: dict[str, list[VarianceRow]] = defaultdict(list)
    for row in rows:
        buckets[row.period].append(row)
    output = []
    for period, items in sorted(buckets.items()):
        budget_revenue = sum((r.budget for r in items if r.category == "revenue"), D("0"))
        actual_revenue = sum((r.actual for r in items if r.category == "revenue"), D("0"))
        budget_cost = sum((r.budget for r in items if r.category == "cost"), D("0"))
        actual_cost = sum((r.actual for r in items if r.category == "cost"), D("0"))
        budget_contribution = budget_revenue - budget_cost
        actual_contribution = actual_revenue - actual_cost
        output.append({
            "period": period,
            "budget_revenue": str(budget_revenue),
            "actual_revenue": str(actual_revenue),
            "revenue_variance": str(actual_revenue - budget_revenue),
            "budget_cost": str(budget_cost),
            "actual_cost": str(actual_cost),
            "cost_variance": str(actual_cost - budget_cost),
            "budget_contribution_proxy": str(budget_contribution),
            "actual_contribution_proxy": str(actual_contribution),
            "contribution_variance": str(actual_contribution - budget_contribution),
            "budget_contribution_margin_pct": str(budget_contribution / budget_revenue * 100) if budget_revenue else None,
            "actual_contribution_margin_pct": str(actual_contribution / actual_revenue * 100) if actual_revenue else None,
        })
    return output


def render_markdown(rows: list[VarianceRow]) -> str:
    summary = monthly_summary(rows)
    lines = [
        "# Monthly actual-versus-budget analysis", "",
        "> **Data: SIMULATED.** This is a finance-method demonstration, not a client's management accounts.",
        "> Contribution proxy = revenue less the listed operating-cost categories. It is not EBITDA or statutory profit.", "",
        "## Metric-level variance", "", "| Period | Metric | Category | Budget | Actual | Variance | Variance % | Favourability |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        pct = f"{row.variance_pct:.1f}%" if row.variance_pct is not None else "n.m."
        lines.append(f"| {row.period} | {row.metric} | {row.category} | {row.budget} | {row.actual} | {row.variance} | {pct} | {row.favourability} |")
    lines += ["", "## Monthly operating contribution bridge", "", "| Period | Budget contribution proxy | Actual contribution proxy | Variance | Budget margin | Actual margin |", "|---|---:|---:|---:|---:|---:|"]
    for item in summary:
        lines.append(f"| {item['period']} | {item['budget_contribution_proxy']} | {item['actual_contribution_proxy']} | {item['contribution_variance']} | {item['budget_contribution_margin_pct'] or 'n.m.'} | {item['actual_contribution_margin_pct'] or 'n.m.'} |")
    lines += ["", "## Interpretation discipline", "", "- Revenue variance is favourable when actual is above budget; cost variance is favourable when actual is below budget.", "- A zero budget produces a not-meaningful percentage variance rather than division by zero.", "- A favourable variance is not automatically sustainable: volume, mix, price, timing and one-off drivers still need investigation.", "- This dataset has no balance-sheet, tax, depreciation, financing or cash timing detail; do not label the contribution proxy EBITDA, net income or cash flow.", ""]
    return "\n".join(lines)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    rows = read_csv(root / "data" / "finance_actual_vs_budget_sample.csv")
    output = root / "docs" / "finance" / "monthly_variance_analysis.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_markdown(rows), encoding="utf-8")
    print(f"wrote {output.relative_to(root)} ({len(rows)} metric-period rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
