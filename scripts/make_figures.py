"""Draw the two analysis figures from the Python models. Run: python3 scripts/make_figures.py"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from finance import capacity, queueing  # noqa: E402

OUT = ROOT / "docs" / "analysis"
INK, TEAL, AMBER, RED, GRID = "#17332f", "#0d655d", "#a76a16", "#b4473f", "#e1e9e6"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": GRID, "axes.labelcolor": INK,
                     "text.color": INK, "xtick.color": INK, "ytick.color": INK})


def queue_curve():
    arrivals = np.linspace(30, 76, 120)
    fig, ax = plt.subplots(figsize=(8.2, 4.6), dpi=160)
    for cs2, colour, label in ((1.0, TEAL, "Jobs vary like a typical queue (cs² = 1)"), (2.0, AMBER, "Jobs vary more (cs² = 2)")):
        waits = [queueing.mean_wait_days(a, 12.5, 6, cs2=cs2)["wait_days"] for a in arrivals]
        ax.plot(arrivals, waits, color=colour, lw=2.4, label=label)
    today = queueing.mean_wait_days(60, 12.5, 6)
    ax.scatter([60], [today["wait_days"]], color=INK, zorder=5)
    ax.annotate(f"Today: 60 RFQs a month\n78% load, {today['wait_days']:.2f} day wait", (60, today["wait_days"]),
                (40, 2.6), arrowprops={"arrowstyle": "-", "color": INK}, fontsize=10.5)
    ax.axvline(76.8, color=RED, ls="--", lw=1.4)
    ax.text(77.4, 2.2, "Capacity\nlimit\n76.8 a\nmonth", color=RED, ha="left", va="center", fontsize=10)
    ax.set_xlim(28, 84)
    ax.set_ylim(0, 5)
    ax.set_xlabel("RFQs arriving per month (6 estimators, 12.5 hours an RFQ)")
    ax.set_ylabel("Average wait before costing starts (working days)")
    ax.set_title("The estimator queue is short today and steep just ahead", loc="left", fontsize=13, fontweight="bold")
    ax.grid(color=GRID, lw=0.8)
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.text(0.01, 0.005, "Erlang C with Allen-Cunneen adjustment. Inputs: brief plus assumptions A4 (160 h a month) and A5 (8 h a day).\nA pressure gauge, not a forecast.",
             fontsize=8, color="#71817d")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(OUT / "queue_wait_curve.png")
    plt.close(fig)


def capacity_grid():
    revs = [200e6, 500e6, 1000e6, 2000e6]
    spares = [0.0, 0.005, 0.01, 0.02, 0.05]
    recovered = 2_160_000
    z = np.array([[next(r["realised_margin"] for r in capacity.grid(plant_revenues=(rev,), spare_shares=(sp,))) / recovered
                   for sp in spares] for rev in revs])
    fig, ax = plt.subplots(figsize=(8.2, 4.3), dpi=160)
    im = ax.imshow(z, cmap="YlGnBu", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(spares)), [f"{s * 100:g}%" for s in spares])
    ax.set_yticks(range(len(revs)), [f"₹{int(r / 1e7)} crore" for r in revs])
    for i in range(len(revs)):
        for j in range(len(spares)):
            ax.text(j, i, f"{z[i, j] * 100:.0f}%", ha="center", va="center", color="white" if z[i, j] > 0.55 else INK, fontsize=11)
    ax.set_xlabel("Spare plant capacity (share of annual output)")
    ax.set_ylabel("Plant revenue (test values)")
    ax.set_title("How much of the ₹21.6 lakh the plant can make", loc="left", fontsize=13, fontweight="bold")
    fig.colorbar(im, ax=ax, format=lambda v, _: f"{int(v * 100)}%")
    fig.text(0.01, 0.005, "Year-1 break-even needs 46%. Plant revenues are test values, not estimates of Company A.\nDisplaced orders are assumed equally profitable.",
             fontsize=8, color="#71817d")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(OUT / "capacity_grid.png")
    plt.close(fig)


def margin_bridge():
    from finance import full_model as fm
    f = fm.financials()
    pool = 86.4
    steps = [("Margin on all\nlost RFQs", pool, "total"), ("Not lost to\ndelay (50%)", -pool * 0.5, "down"),
             ("Not won back\n(50%)", -pool * 0.25, "down"), ("Recovered\nmargin", None, "sub"),
             ("Running\ncost", -2.0, "down"), ("EBITDA", None, "sub"),
             ("Amortisation\nand tax", -(f["amortisation"] + f["tax"]) / 1e5, "down"), ("Net income\nyear 1", None, "sub")]
    fig, ax = plt.subplots(figsize=(9.2, 4.8), dpi=160)
    running = 0.0
    xs = range(len(steps))
    for x, (_label, val, kind) in zip(xs, steps, strict=True):
        if kind == "total" and val is not None:
            ax.bar(x, val, color=TEAL)
            running = val
            ax.text(x, val + 1.5, f"{val:.1f}", ha="center")
        elif kind == "down" and val is not None:
            ax.bar(x, val, bottom=running, color=RED if abs(val) > 5 else AMBER)
            ax.text(x, running + 1.5, f"{val:.1f}", ha="center")
            running += val
        else:
            ax.bar(x, running, color=TEAL)
            ax.text(x, running + 1.5, f"{running:.1f}", ha="center", fontweight="bold")
    ax.set_ylim(0, 100)
    ax.set_xticks(list(xs), [s[0] for s in steps], fontsize=9)
    ax.set_ylabel("₹ lakh a year")
    ax.set_title("From the ₹86.4 lakh ceiling to ₹12.7 lakh of year-1 net income", loc="left", fontsize=13, fontweight="bold")
    ax.grid(axis="y", color=GRID)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.text(0.01, 0.005, "50% delay share and 50% win rate are assumptions (win-back 25%). Tax 25% and 3-year amortisation of the fee are assumptions.\nWorking capital is a cash effect and is not shown here.",
             fontsize=7.5, color="#71817d")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(OUT / "margin_bridge.png")
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    queue_curve()
    capacity_grid()
    margin_bridge()
    print("figures written to", OUT)
