# Forging economics simulator

The local application provides an interactive, deterministic scenario panel for a representative **synthetic** forged-and-machined component. It is designed to demonstrate how commercial decisions can be tied to explicit drivers—not to estimate Bharat Forge costs or forecast any company result.

## Inputs

| Driver | Interpretation | Allowed range |
|---|---|---:|
| Steel-price change | Change applied to the illustrative billet input cost | -50% to +50% |
| Forging yield | Good output divided by material input | 50% to 99% |
| Machining cycle time | Scales the representative machining cost | 0.5 to 30 minutes |
| Energy-cost change | Change applied to illustrative energy cost | -50% to +100% |
| Capacity utilisation | Portion of representative annual volume used in annual contribution | 30% to 100% |
| Working-capital days | Revenue-based cash tie-up for sensitivity | 0 to 365 days |

## Calculation boundary

The simulator uses a fixed illustrative selling price and annual volume. It returns material, machining, energy and conversion cost; contribution per unit; annual contribution at the selected utilisation; and revenue-based working capital. Contribution is before corporate overhead, finance cost and tax.

Its recommendation is intentionally conservative: a positive contribution does not approve a build. It recommends a pilot until trace data and signed rates validate the assumptions.

## Bharat Forge reference

The adjacent benchmark panel reproduces selected, audited FY26 public metrics documented in `real_company_benchmark.md`: EBITDA margin, Forgings segment margin, material share of revenue, receivable days and cash conversion cycle. It is a range check from one large, export-heavy company and one year—not a comparable-company valuation or operational benchmark for the illustrative case.

## Reproduction

```bash
python -m pytest finance/test_forging_scenarios.py
uvicorn application.server:app --reload
```

After signing in, use **Forging economics simulator** in the local workspace. The API is `POST /api/forging-scenario`; its result includes a classification string so it remains distinguishable from public or application data.
