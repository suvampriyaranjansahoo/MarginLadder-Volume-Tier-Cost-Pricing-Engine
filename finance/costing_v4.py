"""V4 price-waterfall extension; illustrative inputs only."""
from __future__ import annotations
from decimal import Decimal as D


def price_waterfall(material: D, conversion: D, scrap_recovery: D, rejection: D, rework: D = D(0), reinspection: D = D(0), additional_setup: D = D(0), tooling: D = D(0), rush_premium: D = D(0), overhead: D = D(0), packing: D = D(0), freight: D = D(0), target_contribution_margin: D = D("0.12"), discount: D = D(0)) -> dict[str, D]:
    values = {"material": material, "conversion": conversion, "scrap_recovery": scrap_recovery, "rejection": rejection, "rework": rework, "reinspection": reinspection, "additional_setup": additional_setup, "tooling": tooling, "rush_premium": rush_premium, "overhead": overhead, "packing": packing, "freight": freight}
    if any(v < 0 for v in values.values()) or not D(0) <= target_contribution_margin < 1 or not D(0) <= discount < 1:
        raise ValueError("costs must be non-negative; margin and discount must be below 100%")
    manufacturing_cost = material + conversion - scrap_recovery + rejection + rework + reinspection + additional_setup + tooling + rush_premium + overhead + packing + freight
    selling_price = manufacturing_cost / (1 - target_contribution_margin)
    net_selling_price = selling_price * (1 - discount)
    return {**values, "manufacturing_cost": manufacturing_cost, "target_contribution_margin": target_contribution_margin,
            "selling_price": selling_price, "discount": discount, "net_selling_price": net_selling_price,
            "contribution_after_discount": net_selling_price - manufacturing_cost,
            "contribution_margin_after_discount": (net_selling_price - manufacturing_cost) / net_selling_price if net_selling_price else D(0)}


def requires_margin_approval(waterfall: dict[str, D], minimum_contribution_margin: D) -> bool:
    if not D(0) <= minimum_contribution_margin < 1:
        raise ValueError("minimum contribution margin must be between 0% and 100%")
    return waterfall["contribution_margin_after_discount"] < minimum_contribution_margin
