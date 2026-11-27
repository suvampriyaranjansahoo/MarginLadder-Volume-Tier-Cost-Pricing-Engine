from decimal import Decimal as D
from finance.costing_v4 import price_waterfall, requires_margin_approval
from finance.fpa_v4 import plan, sales_variance_bridge


def test_price_waterfall_includes_each_traceable_cost_once():
    out = price_waterfall(D(100), D(20), D(5), D(2), rework=D(3), reinspection=D(1), tooling=D(4), rush_premium=D(6), overhead=D(10), packing=D(2), freight=D(7))
    assert out["manufacturing_cost"] == D(150)
    assert out["contribution_after_discount"] == D("20.4545454545454545454545455")
    assert requires_margin_approval(out, D("0.13")) is True


def test_sales_bridge_reconciles_total_variance():
    bridge = sales_variance_bridge(100, 120, 10, 12)
    assert bridge["bridge_check"] == 0
    assert plan(100, 10, 3, 2, 100, .1)["operating_profit"] == 400
