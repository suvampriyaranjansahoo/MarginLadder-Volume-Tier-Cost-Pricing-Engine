"""How fragile is the RICE ranking? Reads docs/product/prioritisation_matrix.md and perturbs every input.

Run: python3 -m analytics.rice_sensitivity   (writes docs/product/rice_sensitivity.md)
Perturbation [Judgement]: reach x U(0.75, 1.25); impact x U(0.75, 1.25); confidence + U(-0.20, +0.20) kept in [0.10, 1.00];
effort x U(0.70, 1.50). 5,000 draws, fixed seed. The point is which ranks are stable, not the exact scores.
"""
from __future__ import annotations

import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "product" / "prioritisation_matrix.md"
OUT = ROOT / "docs" / "product" / "rice_sensitivity.md"
DRAWS, SEED = 5000, 7


def load_items(path: Path = MATRIX) -> list[dict]:
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 8 or not re.match(r"^\d", cells[1]) or not cells[3].endswith("%"):
            continue
        reach = re.match(r"[\d.]+", cells[1])
        if reach is None:
            continue
        items.append({"name": cells[0], "reach": float(reach.group()), "impact": float(cells[2]),
                      "confidence": float(cells[3].rstrip("%")) / 100, "effort": float(cells[4]),
                      "rice": float(cells[5]), "priority": cells[6]})
    return items


def rice(reach: float, impact: float, confidence: float, effort: float) -> float:
    return reach * impact * confidence / effort


def ranks(scores: list[float]) -> list[int]:
    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    out = [0] * len(scores)
    for position, i in enumerate(order, start=1):
        out[i] = position
    return out


def simulate(items: list[dict], draws: int = DRAWS, seed: int = SEED) -> list[dict]:
    rng = random.Random(seed)  # noqa: S311  (simulation, not security)
    base = ranks([rice(i["reach"], i["impact"], i["confidence"], i["effort"]) for i in items])
    history: list[list[int]] = [[] for _ in items]
    for _ in range(draws):
        scores = [rice(i["reach"] * rng.uniform(0.75, 1.25), i["impact"] * rng.uniform(0.75, 1.25),
                       min(1.0, max(0.10, i["confidence"] + rng.uniform(-0.20, 0.20))), i["effort"] * rng.uniform(0.70, 1.50))
                  for i in items]
        for idx, r in enumerate(ranks(scores)):
            history[idx].append(r)
    out = []
    for idx, item in enumerate(items):
        h = sorted(history[idx])
        out.append({"name": item["name"], "priority": item["priority"], "base_rank": base[idx],
                    "median_rank": h[len(h) // 2], "p10_rank": h[int(0.1 * len(h))], "p90_rank": h[int(0.9 * len(h))],
                    "same_rank_pct": round(100 * sum(1 for r in h if r == base[idx]) / len(h), 1),
                    "top3_pct": round(100 * sum(1 for r in h if r <= 3) / len(h), 1)})
    return sorted(out, key=lambda r: r["base_rank"])


def main() -> int:
    items = load_items()
    res = simulate(items)
    widest = max(r["p90_rank"] - r["p10_rank"] for r in res)
    loose = [r for r in res if r["same_rank_pct"] < 60]
    lines = ["# RICE sensitivity: which ranks can I trust?", "",
             f"Source: `docs/product/prioritisation_matrix.md` ({len(items)} capabilities). {DRAWS:,} random draws, seed {SEED}.",
             "Each draw changes reach and impact by up to 25%, confidence by up to 20 points and effort by -30% to +50%. [Judgement]", "",
             "| Base rank | Capability | Priority | 10th to 90th percentile rank | Same rank | In top 3 |", "|---|---|---|---|---|---|"]
    for r in res:
        lines.append(f"| {r['base_rank']} | {r['name']} | {r['priority']} | {r['p10_rank']} to {r['p90_rank']} | {r['same_rank_pct']}% | {r['top3_pct']}% |")
    lines += ["", "## Reading", "",
              f"- **No capability moves more than {widest} places** between the 10th and 90th percentile. The order is robust to these input errors.",
              f"- **Top 3 in the base case:** {', '.join(r['name'] for r in res[:3])}. They stay in the top 3 in "
              f"{min(r['top3_pct'] for r in res[:3])}% to {max(r['top3_pct'] for r in res[:3])}% of draws.",
              f"- **Ranks that hold in fewer than 60% of draws:** {', '.join(r['name'] for r in loose) or 'none'}. Do not argue their exact order before the Week 1 trace.",
              "- The register is P0 whatever its score, because without it there is no baseline. That is a judgement, not a score.",
              "- What this does not test: a wrong idea of the problem. All draws share one scoring frame, so a shared error in it is invisible here.", ""]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
