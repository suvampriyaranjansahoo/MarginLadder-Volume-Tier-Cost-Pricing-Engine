.PHONY: run test lint reconcile monthly-plan check release-audit
run:
	uvicorn application.server:app --reload
test:
	PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider
lint:
	ruff check --no-cache . && mypy --cache-dir /tmp/marginladder-mypy-cache
reconcile:
	python -B -m finance.reconcile
	python -B -m finance.monthly_plan
	python -B -m finance.variance
	python -B -m analytics.product_metrics
check: lint test reconcile
	python -B scripts/check_consistency.py
	python -B scripts/portfolio_release_audit.py

release-audit:
	python -B scripts/portfolio_release_audit.py
