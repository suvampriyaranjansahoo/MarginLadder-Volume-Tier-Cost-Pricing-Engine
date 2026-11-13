"""Reference implementation of the costing formulas in the PRD (Appendix A.3).

Fixed formulas only: no AI, no randomness, no clock reads.
Same inputs + same rate snapshot + same formula version -> same output.
All inputs in SAMPLE and MASTER are ILLUSTRATIVE (assumption A21), not Company A's rates,
except gross weight, annual volume, cycle time and hour rate, which come from the brief.
Run:  python3 cost_engine.py   (prints the worked example and runs the tests)
"""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal as D, ROUND_HALF_UP

FORMULA_VERSION = "v1.0"
BATCHES_PER_YEAR = 12  # setup is spread over batch size = annual volume / 12 (A9)


class CostError(ValueError):
    """Visible error. The engine never returns a price from invalid inputs."""


def r2(x):
    return D(x).quantize(D("0.01"), rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Rate:
    code: str
    value: D
    unit: str
    eff_from: date
    eff_to: date  # inclusive
    version: str


class RateMaster:
    def __init__(self, rates):
        self.rates = list(rates)
        by = {}
        for r in self.rates:
            if r.value is None or r.value <= 0:
                raise CostError(f"{r.code}: rate must be above zero")
            if r.eff_to < r.eff_from:
                raise CostError(f"{r.code}: end date before start date")
            by.setdefault(r.code, []).append(r)
        for code, rs in by.items():
            rs.sort(key=lambda x: x.eff_from)
            for a, b in zip(rs, rs[1:]):
                if b.eff_from <= a.eff_to:
                    raise CostError(f"{code}: overlapping dates {a.version}/{b.version}")

    def lookup(self, code, on):
        hits = [r for r in self.rates if r.code == code and r.eff_from <= on <= r.eff_to]
        if not hits:
            raise CostError(f"{code}: no rate effective on {on}")
        return hits[0]


def cost_part(p, master, quote_date, volume):
    """Cost one part at one annual volume. p holds estimator-accepted inputs."""
    for k in ("gross", "net", "cycle_min", "setup_min"):
        if p.get(k) is None or D(str(p[k])) < 0 or (k in ("gross", "net", "cycle_min") and D(str(p[k])) == 0):
            raise CostError(f"{k}: missing or not valid")
    volume = D(str(volume))
    if volume <= 0:
        raise CostError("annual volume must be above zero")
    gross, net = D(str(p["gross"])), D(str(p["net"]))
    if net > gross:
        raise CostError("net weight exceeds gross weight")
    m = D(str(p["margin"]))
    if not (D(0) <= m < D(1)):
        raise CostError("margin must be at least 0 and below 100%")
    mat = master.lookup(p["mat_code"], quote_date)
    mc = master.lookup(p["mc_code"], quote_date)

    # Each line is rounded half-up to 0.01; totals are sums of rounded lines (R-02).
    material = r2(gross * mat.value)
    scrap = r2((gross - net) * D(str(p["scrap_credit"])))
    net_material = material - scrap
    machining = r2(D(str(p["cycle_min"])) / 60 * mc.value)
    setup = r2((D(str(p["setup_min"])) / 60 * mc.value) / (volume / BATCHES_PER_YEAR))
    conversion = machining + setup
    rejection = r2(D(str(p["reject"])) * (net_material + conversion))
    overhead = r2(D(str(p["overhead"])) * conversion)
    packing = r2(D(str(p["packing"])))
    freight = r2(D(str(p["freight_per_kg"])) * net)
    cost = net_material + conversion + rejection + overhead + packing + freight
    price = r2(cost / (1 - m))            # margin is a share of selling price
    margin = price - cost
    gst = r2(price * D(str(p.get("gst", "0.18"))))
    return {
        "material": material, "scrap_credit": scrap, "net_material": net_material,
        "machining": machining, "setup": setup, "conversion": conversion,
        "rejection": rejection, "overhead": overhead, "packing": packing, "freight": freight,
        "cost": cost, "margin": margin, "price": price, "gst": gst, "price_incl_gst": price + gst,
        "annual_volume": volume, "annual_value": price * volume,
        "snapshot": {"formula": FORMULA_VERSION, "quote_date": str(quote_date),
                     "rates": [(r.code, str(r.value), r.unit, str(r.eff_from), str(r.eff_to), r.version) for r in (mat, mc)]},
    }


def needs_sales_head(rfq_annual_value, threshold=D(2500000)):
    """Approval rule (R-05): strictly above the threshold needs the Sales head or deputy."""
    return D(str(rfq_annual_value)) > D(str(threshold))


# ---- Illustrative data (brief: gross, volume, cycle, hour rate; the rest is ours) ----
MASTER = RateMaster([
    Rate("MAT-EN8", D("79"), "kg", date(2026, 4, 1), date(2026, 9, 30), "v16"),
    Rate("MAT-EN8", D("78"), "kg", date(2026, 10, 1), date(2027, 3, 31), "v17"),
    Rate("MC-SPINDLE", D("850"), "hour", date(2026, 4, 1), date(2027, 3, 31), "v17"),
])
SAMPLE = dict(mat_code="MAT-EN8", mc_code="MC-SPINDLE", gross="0.61", net="0.52", cycle_min="3.2",
              setup_min="90", scrap_credit="28", reject="0.015", overhead="0.15", packing="1.80",
              freight_per_kg="4.00", margin="0.12")
TIER_VOLUMES = (90000, 180000, 270000)
# tiers use different material rates in the PRD example (illustrative volume bands)
TIER_RATES = {90000: D("79"), 180000: D("78"), 270000: D("77")}


def _master_for(rate):
    return RateMaster([Rate("MAT-EN8", rate, "kg", date(2026, 4, 1), date(2027, 3, 31), "ex"),
                       Rate("MC-SPINDLE", D("850"), "hour", date(2026, 4, 1), date(2027, 3, 31), "ex")])


def worked_example():
    return {v: cost_part(SAMPLE, _master_for(TIER_RATES[v]), date(2026, 11, 5), v) for v in TIER_VOLUMES}


def run_tests():
    out, ok = [], 0
    def t(name, fn):
        nonlocal ok
        try:
            fn(); ok += 1; out.append("PASS  " + name)
        except AssertionError as e:
            out.append(f"FAIL  {name}: {e}")
    def eq(a, b): assert a == b, f"{a} != {b}"
    def err(fn, frag):
        try:
            fn()
        except CostError as e:
            assert frag in str(e), str(e); return
        raise AssertionError("no CostError raised")
    ex = worked_example()
    b = ex[180000]
    t("T01 price at 90,000 = 117.33", lambda: eq(ex[90000]["price"], D("117.33")))
    t("T02 price at 180,000 = 116.51", lambda: eq(b["price"], D("116.51")))
    t("T03 price at 270,000 = 115.77", lambda: eq(ex[270000]["price"], D("115.77")))
    t("T04 annual value at base tier = 2,09,71,800", lambda: eq(b["annual_value"], D("20971800.00")))
    t("T05 cost lines add up to cost price (all tiers)", lambda: [eq(e["net_material"] + e["conversion"] + e["rejection"] + e["overhead"] + e["packing"] + e["freight"], e["cost"]) for e in ex.values()])
    t("T06 cost + margin = price (all tiers)", lambda: [eq(e["cost"] + e["margin"], e["price"]) for e in ex.values()])
    t("T07 price + GST = price incl GST", lambda: [eq(e["price"] + e["gst"], e["price_incl_gst"]) for e in ex.values()])
    t("T08 margin is a share of price (about 12%)", lambda: [eq(round(e["margin"] / e["price"], 2), D("0.12")) for e in ex.values()])
    t("T09 setup per piece falls as volume rises", lambda: eq(ex[90000]["setup"] > ex[270000]["setup"], True))
    t("T10 1,000 repeat runs give one answer", lambda: eq(len({str(cost_part(SAMPLE, _master_for(D("78")), date(2026, 11, 5), 180000)["price"]) for _ in range(1000)}), 1))
    t("T11 last day of a rate uses it (30 Sep -> v16)", lambda: eq(MASTER.lookup("MAT-EN8", date(2026, 9, 30)).version, "v16"))
    t("T12 next day uses the new rate (1 Oct -> v17)", lambda: eq(MASTER.lookup("MAT-EN8", date(2026, 10, 1)).version, "v17"))
    t("T13 missing rate blocks costing", lambda: err(lambda: cost_part(SAMPLE, MASTER, date(2028, 1, 1), 180000), "no rate effective"))
    t("T14 overlapping rate dates refused", lambda: err(lambda: RateMaster([Rate("X", D(1), "kg", date(2026, 1, 1), date(2026, 6, 30), "a"), Rate("X", D(2), "kg", date(2026, 6, 30), date(2026, 12, 31), "b")]), "overlapping"))
    t("T15 rate of zero refused", lambda: err(lambda: RateMaster([Rate("Y", D(0), "kg", date(2026, 1, 1), date(2026, 2, 1), "z")]), "above zero"))
    t("T16 margin of 100% refused", lambda: err(lambda: cost_part({**SAMPLE, "margin": "1"}, MASTER, date(2026, 11, 5), 180000), "margin"))
    t("T17 blank cycle time refused, not treated as zero", lambda: err(lambda: cost_part({**SAMPLE, "cycle_min": None}, MASTER, date(2026, 11, 5), 180000), "cycle_min"))
    t("T18 net weight above gross refused", lambda: err(lambda: cost_part({**SAMPLE, "net": "0.9"}, MASTER, date(2026, 11, 5), 180000), "net weight"))
    t("T19 zero volume refused", lambda: err(lambda: cost_part(SAMPLE, MASTER, date(2026, 11, 5), 0), "volume"))
    t("T20 old quote keeps its rate version in the snapshot", lambda: eq(cost_part(SAMPLE, MASTER, date(2026, 9, 15), 180000)["snapshot"]["rates"][0][5], "v16"))
    t("T21 exactly Rs 25,00,000 needs no Sales head", lambda: eq(needs_sales_head(2500000), False))
    t("T22 Rs 25,00,001 needs the Sales head", lambda: eq(needs_sales_head(2500001), True))
    t("T23 machining line = 3.2/60 x 850 = 45.33", lambda: eq(b["machining"], D("45.33")))
    t("T24 half-up rounding: 0.125 -> 0.13", lambda: eq(r2("0.125"), D("0.13")))
    return out, ok, 24


if __name__ == "__main__":
    print(f"Reference cost engine {FORMULA_VERSION} (illustrative inputs, RFQ-2611-014)\n")
    for v, e in worked_example().items():
        print(f"{v:>7} pcs  net material {e['net_material']:>6}  conversion {e['conversion']:>6}  cost {e['cost']:>7}  "
              f"price {e['price']:>7}  GST {e['gst']:>6}  annual value {e['annual_value']:>14,.2f}")
    lines, ok, n = run_tests()
    print("\n" + "\n".join(lines) + f"\n\n{ok}/{n} tests passed")
    raise SystemExit(0 if ok == n else 1)
