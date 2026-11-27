"""Bharat Forge Ltd, consolidated, year ended 31 March 2026. Real, audited, sourced.

Every number is copied from one primary document and nothing here is estimated:

    NSE integrated filing (Ind AS), board meeting 7 May 2026, consolidated, audited, amounts in INR lakh.
    https://nsearchives.nseindia.com/corporate/ixbrl/INTEGRATED_FILING_INDAS_156204_07052026224447_iXBRL_WEB.html
    Retrieved 27 Nov 2026. Auditor: B S R & Co LLP, unmodified opinion.

Why this company: Pune-headquartered, forged and machined automotive and industrial components, listed, and large enough
to publish segment, cash-flow and balance-sheet detail. It is a far bigger and more export-heavy business than the
hypothetical Pune maker in the case, so it is used as a *reference point for ranges*, not as a model of that company.

Tags: Sourced = copied from the filing. Dated-market = a market input with the date it was true on.
"""
from __future__ import annotations

SOURCE_URL = (
    "https://nsearchives.nseindia.com/corporate/ixbrl/"
    "INTEGRATED_FILING_INDAS_156204_07052026224447_iXBRL_WEB.html"
)
UNIT = "INR lakh"          # 1 crore = 100 lakh
TAG = "Sourced"

PNL = {
    "revenue_from_operations": 1_681_165.30,
    "other_income": 19_868.30,
    "cost_of_materials_consumed": 777_793.10,
    "purchases_of_stock_in_trade": 7_887.10,
    "changes_in_inventories": -26_722.10,       # a negative expense: inventory build
    "employee_benefit_expense": 210_341.80,
    "finance_costs": 32_334.60,
    "depreciation_and_amortisation": 97_092.40,
    "other_expenses": 419_198.10,
    "total_expenses": 1_517_925.00,
    "profit_before_exceptional_and_tax": 183_108.60,
    "exceptional_items": -15_444.30,
    "profit_before_tax": 167_664.30,
    "current_tax": 56_060.70,
    "deferred_tax": 1_716.70,
    "total_tax": 57_777.40,
    "profit_continuing_operations": 109_886.90,
    "share_of_associates_and_jv": -947.10,
    "total_profit_for_period": 108_939.80,
    "profit_attributable_to_owners": 107_966.10,
    "profit_attributable_to_nci": 973.70,
    "paid_up_equity_share_capital": 9_562.70,
    "face_value_per_share_inr": 2,
    "eps_basic_inr": 22.58,
    "reported_debt_equity_ratio": 0.72,
}

BALANCE_SHEET = {
    "property_plant_equipment": 725_755.20,
    "capital_work_in_progress": 125_132.60,
    "goodwill": 39_025.30,
    "total_non_current_assets": 1_105_709.90,
    "inventories": 405_278.30,
    "current_investments": 117_392.20,
    "trade_receivables_current": 390_979.90,
    "cash_and_cash_equivalents": 84_788.50,
    "other_bank_balances": 14_205.70,
    "total_current_assets": 1_120_285.60,
    "total_assets": 2_225_995.50,
    "total_equity": 955_682.50,
    "borrowings_non_current": 181_235.50,
    "borrowings_current": 506_226.30,
    "trade_payables_current": 299_566.10,
    "total_non_current_liabilities": 312_169.10,
    "total_current_liabilities": 958_143.90,
    "total_liabilities": 1_270_313.00,
}

CASH_FLOW = {
    "cash_from_operations_after_tax": 148_664.20,
    "purchase_of_ppe": 114_049.60,
    "net_investing": -103_303.00,
    "net_financing": -44_198.50,
    "dividends_paid": 37_965.50,
    "interest_paid_financing": 37_522.80,
    "cash_at_end": 84_788.50,
}

SEGMENTS = {   # revenue (before inter-segment elimination) and segment result before tax and interest
    "Forgings": {"revenue": 1_392_858.20, "result": 195_609.10},
    "Defence": {"revenue": 175_717.20, "result": 8_149.70},
    "Others": {"revenue": 216_981.20, "result": 15_403.20},
}
INTER_SEGMENT_REVENUE = 104_391.30

# Company-reported figure from the results press release and earnings call, for comparison only.
REPORTED_CONSOLIDATED_EBITDA_CRORE = 2_921
REPORTED_PRESS_SOURCES = (
    "https://www.business-standard.com/markets/capital-market-news/bharat-forge-q4-pat-slips-17-yoy-to-rs-233-cr-126050700830_1.html",
    "https://www.autocarpro.in/news/bharat-forge-q4-net-profit-falls-175-revenue-rises-175-132472",
)

# Dated-market input. 7 May 2026 BSE close, from Business Standard's results-day report. It is NOT today's price.
SHARE_PRICE_INR = 1_991.0
SHARE_PRICE_DATE = "2026-05-07"
SHARE_PRICE_SOURCE = (
    "https://www.business-standard.com/amp/companies/quarterly-results/"
    "bharat-forge-q4-results-net-profit-falls-17-5-on-labour-code-impact-126050701272_1.html"
)

# Indicative EN8 round-bar listings (INR per kg, ex-GST unless the listing says otherwise). Undated marketplace
# listings from several Indian sellers, retrieved 27 Nov 2026. A rough range, not a price series.
EN8_LISTING_RANGE_INR_PER_KG = (45.0, 75.0)
EN8_LISTING_TYPICAL_INR_PER_KG = (58.0, 70.0)
EN8_LISTING_SOURCE = "https://www.tradeindia.com/products/en8-round-bar-10291633.html (and five other seller listings)"
# Same-day context from ANI, 26 Nov 2026: hot-rolled coil +36.4% year on year, TMT bar +25.1% year on year.
STEEL_PRICE_YOY_NOTE = "hot-rolled coil +36.4% and TMT bar +25.1% year on year, per ANI on 26 Nov 2026"
