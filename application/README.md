# MarginLadder local MVP

This folder contains the v3.1 working workflow application (sign-in, migrations, KPIs, trace import). The original browser prototypes remain in `prototype/` and the reference costing engine remains in `engine/`.

## Run locally

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn application.server:app --reload
```

Open `http://127.0.0.1:8000`.

The first service-backed API request lazily creates a local SQLite database at `application/data/marginladder.db` and inserts four fictional demo RFQs and demo users if the database is empty. Importing the ASGI module or calling the public health endpoint does not create files. Sign-in details are written to `application/data/demo_credentials.txt` (gitignored, never commit it). An older v2 database upgrades in place. To reset the demo, stop the server and delete that database file. To use another location, set `MARGINLADDER_DB` before starting the server.

## Demonstration path

0. Sign in with a demo account from `application/data/demo_credentials.txt`. Your role comes from the account.
1. Open a `New` RFQ and select **Start costing** as an estimator.
2. Select **Calculate 3 volume prices**, edit the gross weight, net weight and cycle time for each part line, add up to 50 lines, set the common target margin and run costing.
3. Sign out and sign in as **Sales Head** or **Deputy** to approve / send back a quote above ₹25 lakh annual value.
4. Sign in as an estimator again and mark the approved quote as sent.
5. Review the quote version snapshot and activity trail. Use **Print / Save quotation PDF** to open the print-friendly quote and save it through the browser.
6. Sign in as **Plant Head** on an RFQ in routing review to demonstrate the routing gate.

The costing screen reuses `engine/cost_engine.py`; it does not duplicate formulas in JavaScript.

## API and docs

- API documentation: `http://127.0.0.1:8000/docs` (FastAPI-generated Swagger UI)
- Health check: `/api/health`
- Dashboard and KPIs: `/api/dashboard`, `/api/kpis`
- Queue and capacity: `/api/analysis`
- Week-1 trace: `/api/trace/import`, `/api/trace/summary`
- Reproducible finance case: `/api/finance-case`
- RFQ register: `/api/rfqs`
- API / data model: `../docs/architecture.md`
- Product requirements: `../docs/product/PRD_v3.md`
- KPI dictionary: `../docs/ba/KPI_dictionary.md`
- Finance methodology: `../docs/finance/decision_model_methodology.md`

## Scope and limitations

This is a local portfolio MVP. It has a login and server-side roles but no SSO, MFA, password reset, tenancy, file upload, real AI extraction, ERP link, email or monitoring. Do not expose it publicly or put real customer data in it. The seeded RFQs and costing inputs are fictional.

## Regression checks

From the repository root:

```bash
python3 -B engine/cost_engine.py                 # 24 original checks
pip install -r requirements-dev.txt
PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider  # current v3.2 suite
python3 -B -m finance.reconcile                  # 64 of 64 cells
python3 -B -m finance.variance                   # simulated monthly variance analysis
python3 -B -m analytics.product_metrics          # simulated product funnel / cohorts
```

See `docs/upgrade_regression_report_v3_2_1.md` for exact v3.2 results. The application API remains version 3.1.0; the repository portfolio package is version 3.2.1.
