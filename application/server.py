"""FastAPI HTTP layer for the MarginLadder local MVP (v3).

Run from the repository root: uvicorn application.server:app --reload

This is a sign-in-free local portfolio demo. Visitors select a demo role in the
browser; it is used only to reveal the role-specific demonstration paths and is
not an identity or security control.
"""
from __future__ import annotations

import html
from threading import Lock
from pathlib import Path
from typing import Any, NoReturn

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from finance import capacity as capacity_model
from finance import forging_scenarios, full_model, queueing
from finance.case_model import output_dict as finance_output, scenario_table as finance_scenarios

from application.service import (
    AccessDeniedError,
    MarginLadderService,
    NotFoundError,
    ROLE_NAMES,
    ServiceError,
)

VERSION = "3.1.0"
ROOT = Path(__file__).resolve().parents[1]
STATIC = Path(__file__).resolve().parent / "static"
# Constructed lazily so importing the ASGI module is side-effect free. This matters for
# test collection, static analysis, CLI tooling and worker processes.
service: MarginLadderService | None = None
_service_lock = Lock()


def get_service() -> MarginLadderService:
    """Return the process service, initialising the local demo only on first use."""
    global service
    current = service
    if current is not None:
        return current
    with _service_lock:
        current = service
        if current is None:
            current = MarginLadderService(seed_demo=True)
            service = current
    return current


app = FastAPI(
    title="MarginLadder RFQ Workspace",
    description="Local portfolio MVP for RFQ tracking, deterministic costing, approvals, KPIs and audit events.",
    version=VERSION,
)
app.mount("/static", StaticFiles(directory=STATIC), name="static")
app.mount("/prototype", StaticFiles(directory=ROOT / "prototype"), name="prototype")
app.mount("/case-docs", StaticFiles(directory=ROOT / "docs"), name="case-docs")


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("Cache-Control", "no-store")
    return response


class CreateRFQRequest(BaseModel):
    customer: str = Field(min_length=1, max_length=120)
    part_description: str = Field(min_length=1, max_length=180)
    owner: str = Field(min_length=1, max_length=80)
    due_date: str
    notes: str = Field(default="", max_length=1000)


class UpdateRFQRequest(BaseModel):
    owner: str | None = Field(default=None, min_length=1, max_length=80)
    due_date: str | None = None
    status: str | None = None


class PartInput(BaseModel):
    description: str = Field(default="Part", max_length=180)
    mat_code: str = "MAT-EN8"
    mc_code: str = "MC-SPINDLE"
    gross: str | float | int = "0.61"
    net: str | float | int = "0.52"
    cycle_min: str | float | int = "3.2"
    setup_min: str | float | int = "90"
    scrap_credit: str | float | int = "28"
    reject: str | float | int = "0.015"
    overhead: str | float | int = "0.15"
    packing: str | float | int = "1.80"
    freight_per_kg: str | float | int = "4.00"
    margin: str | float | int = "0.12"
    gst: str | float | int = "0.18"


class CreateQuoteRequest(BaseModel):
    quote_date: str | None = None
    selected_volume: int = 180000
    pricing_mode: str = "all_units"
    parts: list[PartInput] = Field(default_factory=list, max_length=50)


class DecisionRequest(BaseModel):
    action: str
    reason: str = Field(default="", max_length=1000)


class TraceImportRequest(BaseModel):
    rows: list[dict[str, str | None]] = Field(max_length=2000)
    batch_id: str | None = Field(default=None, max_length=60)


class ForgingScenarioRequest(BaseModel):
    """Illustrative scenario inputs; each percentage is supplied as a decimal."""

    steel_price_change_pct: float = Field(default=0, ge=-0.5, le=0.5)
    forging_yield_pct: float = Field(default=0.88, ge=0.5, le=0.99)
    machining_cycle_min: float = Field(default=3.2, ge=0.5, le=30)
    energy_cost_change_pct: float = Field(default=0, ge=-0.5, le=1)
    utilisation_pct: float = Field(default=0.78, ge=0.3, le=1)
    working_capital_days: float = Field(default=45, ge=0, le=365)


def _raise_http(exc: Exception) -> NoReturn:
    if isinstance(exc, NotFoundError):
        raise HTTPException(status_code=404, detail=str(exc))
    if isinstance(exc, AccessDeniedError):
        raise HTTPException(status_code=403, detail=str(exc))
    if isinstance(exc, ServiceError):
        raise HTTPException(status_code=400, detail=str(exc))
    raise exc


def current_user(x_demo_role: str | None = Header(default=None)) -> dict[str, Any]:
    """Return a selected demo role; this local build intentionally has no authentication."""
    role = (x_demo_role or "estimator").strip().lower()
    if role not in ROLE_NAMES:
        raise HTTPException(status_code=400, detail="Choose a valid demo role")
    return {"username": f"demo_{role}", "display_name": role.replace("_", " ").title(), "role": role}


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return (STATIC / "index.html").read_text(encoding="utf-8")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "application": "MarginLadder", "version": VERSION}


@app.get("/api/me")
def me(user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    return user


@app.get("/api/dashboard")
def dashboard(user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    return {**get_service().dashboard(), "simulated_cycle": get_service().simulated_cycle_analytics(), "kpis": get_service().kpis()}


@app.get("/api/kpis")
def kpis(user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    return get_service().kpis()


@app.get("/api/finance-case")
def finance_case(user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    return {
        "classification": "Derived arithmetic from brief inputs plus explicitly labelled assumptions; not realised client results.",
        "base_case": finance_output(),
        "scenarios": finance_scenarios(),
        "net_capacity": full_model.net_capacity_value(),
        "cash_view": {k: v for k, v in full_model.financials().items() if k in {"npv", "irr", "payback_years", "deepest_cash_need"}},
    }


@app.get("/api/sector-benchmark")
def sector_benchmark(user: dict[str, Any] = Depends(current_user)) -> dict[str, object]:
    """Audited public FY26 range reference, separate from the synthetic case."""
    return forging_scenarios.public_benchmark()


@app.post("/api/forging-scenario")
def forging_scenario(request: ForgingScenarioRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, str]:
    """Recalculate illustrative unit economics; no data is persisted."""
    try:
        return forging_scenarios.scenario_dict(**request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/analysis")
def analysis(user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    """Queueing view of the estimator team and the plant-capacity grid. Assumption-tagged, not forecasts."""
    return {
        "queueing": {
            "today": queueing.mean_wait_days(60, 12.5, 6),
            "target": queueing.mean_wait_days(60, 5, 6),
            "load_table": queueing.load_table(),
            "in_progress_today": queueing.littles_law(60, 9),
            "in_progress_target": queueing.littles_law(60, 4),
            "label": "Assumption-based pressure gauge (Erlang C). Not a forecast.",
        },
        "capacity": {
            "break_even_fit": capacity_model.break_even_fit(),
            "grid": capacity_model.grid(),
            "label": "Illustrative grid. Plant revenue values are test values, not estimates of Company A.",
        },
    }


@app.get("/api/rfqs")
def list_rfqs(response: Response, status: str | None = None,
              search: str | None = Query(default=None, max_length=120),
              limit: int = Query(default=100, ge=1, le=500), offset: int = Query(default=0, ge=0),
              user: dict[str, Any] = Depends(current_user)) -> list[dict[str, Any]]:
    try:
        response.headers["X-Total-Count"] = str(get_service().count_rfqs(status=status, search=search))
        return get_service().list_rfqs(status=status, search=search, limit=limit, offset=offset)
    except Exception as exc:
        _raise_http(exc)


@app.post("/api/rfqs", status_code=201)
def create_rfq(request: CreateRFQRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    try:
        return get_service().create_rfq(request.model_dump(), user["display_name"], user["role"])
    except Exception as exc:
        _raise_http(exc)


@app.get("/api/rfqs/{rfq_id}")
def get_rfq(rfq_id: str, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    try:
        return get_service().get_rfq(rfq_id)
    except Exception as exc:
        _raise_http(exc)


@app.patch("/api/rfqs/{rfq_id}")
def update_rfq(rfq_id: str, request: UpdateRFQRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    try:
        return get_service().update_rfq(rfq_id, request.model_dump(exclude_none=True), user["display_name"], user["role"])
    except Exception as exc:
        _raise_http(exc)


@app.post("/api/rfqs/{rfq_id}/quote", status_code=201)
def create_quote(rfq_id: str, request: CreateQuoteRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    try:
        payload = request.model_dump()
        payload["parts"] = [part.model_dump() for part in request.parts]
        return get_service().create_quote(rfq_id, payload, user["display_name"], user["role"])
    except Exception as exc:
        _raise_http(exc)


@app.get("/api/rfqs/{rfq_id}/quotes")
def list_quotes(rfq_id: str, user: dict[str, Any] = Depends(current_user)) -> list[dict[str, Any]]:
    try:
        return get_service().list_quotes(rfq_id)
    except Exception as exc:
        _raise_http(exc)


@app.get("/api/quotes/{quote_id}")
def get_quote(quote_id: str, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    try:
        return get_service().get_quote(quote_id)
    except Exception as exc:
        _raise_http(exc)


@app.post("/api/quotes/{quote_id}/decision")
def decide_quote(quote_id: str, request: DecisionRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    try:
        return get_service().decide_quote(quote_id, request.action, request.reason, user["display_name"], user["role"])
    except Exception as exc:
        _raise_http(exc)


@app.post("/api/quotes/{quote_id}/send")
def send_quote(quote_id: str, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    try:
        return get_service().send_quote(quote_id, user["display_name"], user["role"])
    except Exception as exc:
        _raise_http(exc)


@app.post("/api/trace/import", status_code=201)
def import_trace(request: TraceImportRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    try:
        return get_service().import_trace(request.rows, user["display_name"], user["role"], request.batch_id)
    except Exception as exc:
        _raise_http(exc)


@app.get("/api/trace/summary")
def trace_summary(batch_id: str | None = Query(default=None, max_length=60),
                  user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    return get_service().trace_summary(batch_id)


@app.get("/api/audit")
def audit(limit: int = Query(default=100, ge=1, le=500), entity_id: str | None = None,
          user: dict[str, Any] = Depends(current_user)) -> list[dict[str, Any]]:
    return get_service().audit_log(limit=limit, entity_id=entity_id)


def render_quote_html(rfq: dict[str, Any], quote: dict[str, Any]) -> str:
    snap = quote["snapshot"]
    tiers = snap["tiers"]
    rows = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(value))}</td>" for value in (
            tier["annual_volume_per_part"], tier["total_unit_cost"], tier["total_unit_price"],
            tier["total_gst_per_unit"], tier["annual_value"])) + "</tr>"
        for tier in tiers
    )
    lines = []
    selected = snap["selected_tier"]
    for line in selected["lines"]:
        result = line["result"]
        lines.append(
            "<tr>" + "".join(f"<td>{html.escape(str(value))}</td>" for value in (
                line["line_number"], line["description"], result["cost"], result["price"], result["gst"], result["snapshot"]["formula"])) + "</tr>"
        )
    body = f"""<!doctype html><html><head><meta charset='utf-8'><title>MarginLadder {html.escape(rfq['rfq_code'])}</title>
    <style>body{{font:14px Arial,sans-serif;color:#172b2a;margin:36px}}h1{{margin-bottom:4px}}.muted{{color:#667773}}table{{border-collapse:collapse;width:100%;margin:18px 0}}th,td{{border:1px solid #d9e2df;padding:9px;text-align:left}}th{{background:#edf4f1}}.notice{{padding:12px;background:#fff5df;border:1px solid #ead6a8}}@media print{{button{{display:none}}body{{margin:12mm}}}}</style></head><body>
    <button onclick='window.print()'>Print / Save as PDF</button><h1>MarginLadder – Indicative Quotation</h1>
    <p class='muted'>RFQ {html.escape(rfq['rfq_code'])} · Quote version {quote['version']} · {html.escape(quote['quote_date'])}</p>
    <p><b>Customer:</b> {html.escape(rfq['customer'])}<br><b>Part:</b> {html.escape(rfq['part_description'])}<br><b>Owner:</b> {html.escape(rfq['owner'])}</p>
    <h2>Volume pricing</h2><table><thead><tr><th>Annual units / part</th><th>Cost / unit (₹)</th><th>Price / unit (₹)</th><th>GST / unit (₹)</th><th>Annual value (₹)</th></tr></thead><tbody>{rows}</tbody></table>
    <h2>Selected tier line detail ({snap['selected_volume']} units)</h2><table><thead><tr><th>#</th><th>Part</th><th>Cost (₹)</th><th>Price (₹)</th><th>GST (₹)</th><th>Formula</th></tr></thead><tbody>{''.join(lines)}</tbody></table>
    <p><b>Approval status:</b> {html.escape(quote['status'])} · <b>Approval required:</b> {'Yes' if quote['approval_required'] else 'No'}</p>
    <div class='notice'>Illustrative portfolio prototype. Validate customer-specific rates, tax treatment, technical inputs and commercial terms before external use. This output is not a customer-ready offer.</div>
    <p class='muted'>Formula version {html.escape(snap['formula_version'])}. Rate snapshot retained with this quote.</p></body></html>"""
    return body


@app.get("/api/quotes/{quote_id}/print", response_class=HTMLResponse)
def printable_quote(quote_id: str, user: dict[str, Any] = Depends(current_user)) -> HTMLResponse:
    try:
        quote = get_service().get_quote(quote_id)
        rfq = get_service().get_rfq(quote["rfq_id"])
    except Exception as exc:
        _raise_http(exc)
    return HTMLResponse(render_quote_html(rfq, quote))
