# Analysis folder

| File | What it shows | Code |
|---|---|---|
| `queue_wait_curve.png` | Average wait before costing starts, as RFQs arrive faster | `finance/queueing.py` |
| `capacity_grid.png` | Share of the recovered margin the plant can make, by spare capacity | `finance/capacity.py` |
| `margin_bridge.png` | From the ₹86.4 lakh margin ceiling to year-1 net income | `finance/full_model.py` |

Regenerate with `python3 scripts/make_figures.py`. All inputs are brief values or tagged assumptions.
