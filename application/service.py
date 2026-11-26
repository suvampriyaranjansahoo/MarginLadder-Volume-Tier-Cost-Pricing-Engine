"""Application service for the MarginLadder local MVP.

The service persists RFQs, quote snapshots, approval decisions and audit events in
SQLite while reusing the original deterministic costing engine unchanged.
This is a local portfolio/demo implementation, not a production security boundary.
"""
from __future__ import annotations

import csv
import json
from contextlib import contextmanager
import os
import sqlite3
from math import ceil
import uuid
from datetime import date, datetime, timedelta, UTC
from decimal import Decimal, DecimalException
from pathlib import Path
from typing import Any

from application import auth
from tracekit import analyze as trace_analyze
from engine.cost_engine import CostError, MASTER, SAMPLE, TIER_VOLUMES, cost_part, needs_sales_head

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = Path(os.getenv("MARGINLADDER_DB", Path(__file__).resolve().parent / "data" / "marginladder.db"))
SIMULATED_LOG = ROOT / "data" / "simulated_rfq_log.csv"
APPROVAL_THRESHOLD = Decimal("2500000")
VALID_STATUSES = {
    "new", "costing", "routing_review", "ready_for_quote", "pending_approval",
    "approved", "sent_back", "sent", "cancelled"
}
ALLOWED_TRANSITIONS = {
    "new": {"costing", "routing_review", "cancelled"},
    "costing": {"routing_review", "ready_for_quote", "cancelled"},
    "routing_review": {"costing", "ready_for_quote", "cancelled"},
    "ready_for_quote": {"costing", "cancelled"},
    "pending_approval": {"costing", "cancelled"},
    "approved": {"sent", "cancelled"},
    "sent_back": {"costing", "cancelled"},
    "sent": set(),
    "cancelled": set(),
}
ROLE_NAMES = {"estimator", "estimation_head", "plant_head", "sales_head", "deputy"}
SESSION_HOURS = 8
MAX_FAILED_LOGINS = 5
LOCKOUT_MINUTES = 15
SCHEMA_VERSION = 3


MIGRATIONS: list[tuple[int, str]] = [
    (1, """
        CREATE TABLE IF NOT EXISTS rfqs (
            id TEXT PRIMARY KEY,
            rfq_code TEXT NOT NULL UNIQUE,
            customer TEXT NOT NULL,
            part_description TEXT NOT NULL,
            owner TEXT NOT NULL,
            received_at TEXT NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_rfqs_status ON rfqs(status);
        CREATE INDEX IF NOT EXISTS idx_rfqs_due_date ON rfqs(due_date);
        CREATE TABLE IF NOT EXISTS quotes (
            id TEXT PRIMARY KEY,
            rfq_id TEXT NOT NULL REFERENCES rfqs(id) ON DELETE RESTRICT,
            version INTEGER NOT NULL,
            status TEXT NOT NULL,
            quote_date TEXT NOT NULL,
            approval_required INTEGER NOT NULL,
            annual_value TEXT NOT NULL,
            snapshot_json TEXT NOT NULL,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL,
            decided_by TEXT,
            decided_at TEXT,
            decision_reason TEXT,
            UNIQUE(rfq_id, version)
        );
        CREATE INDEX IF NOT EXISTS idx_quotes_rfq ON quotes(rfq_id, version);
        CREATE TABLE IF NOT EXISTS audit_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_type TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            actor TEXT NOT NULL,
            actor_role TEXT NOT NULL,
            details_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_events(entity_type, entity_id, id);
    """),
    (2, """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            display_name TEXT NOT NULL,
            role TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sessions (
            token_hash TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS login_failures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            failed_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_login_failures ON login_failures(username, failed_at);
    """),
    (3, """
        CREATE TABLE IF NOT EXISTS trace_rfqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id TEXT NOT NULL,
            rfq_ref TEXT NOT NULL,
            row_json TEXT NOT NULL,
            imported_by TEXT NOT NULL,
            imported_at TEXT NOT NULL,
            UNIQUE(batch_id, rfq_ref)
        );
        CREATE INDEX IF NOT EXISTS idx_audit_event_type ON audit_events(event_type, created_at);
    """),
]


class ServiceError(Exception):
    """Expected business or validation error from the application service."""


class NotFoundError(ServiceError):
    pass


class AccessDeniedError(ServiceError):
    pass


_DUMMY_HASH = auth.hash_password("not-a-real-password")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _json_default(value: Any) -> str:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    raise TypeError(f"Cannot JSON-serialise {type(value).__name__}")


def _json_dump(value: Any) -> str:
    return json.dumps(value, default=_json_default, separators=(",", ":"), sort_keys=True)


def _json_load(value: str | None, fallback: Any = None) -> Any:
    return json.loads(value) if value else fallback


def _dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def _require_role(role: str, allowed: set[str]) -> str:
    normalised = (role or "").strip().lower()
    if normalised not in ROLE_NAMES:
        raise ServiceError("A recognised demo role is required")
    if normalised not in allowed:
        raise AccessDeniedError(f"Role '{normalised}' is not permitted for this action")
    return normalised


class MarginLadderService:
    """SQLite-backed service layer; pass a temporary db_path for isolated tests."""

    def __init__(self, db_path: str | Path = DEFAULT_DB, seed_demo: bool = False):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialise()
        if seed_demo:
            self.seed_demo_data()

    def _connect(self) -> sqlite3.Connection:
        con = sqlite3.connect(self.db_path, timeout=10)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        con.execute("PRAGMA journal_mode = WAL")
        return con

    @contextmanager
    def _db(self):
        """Commit successful units of work and always close their connection."""
        con = self._connect()
        try:
            yield con
            con.commit()
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()

    def initialise(self) -> None:
        """Apply any schema migrations not yet recorded. Safe to run on a v2.0 database."""
        with self._db() as con:
            con.execute("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)")
            done = {r[0] for r in con.execute("SELECT version FROM schema_version")}
            for version, script in MIGRATIONS:
                if version not in done:
                    con.executescript(script)
                    con.execute("INSERT INTO schema_version(version, applied_at) VALUES(?,?)", (version, utc_now()))

    def _audit(self, con: sqlite3.Connection, entity_type: str, entity_id: str,
               event_type: str, actor: str, role: str, details: dict[str, Any]) -> None:
        con.execute(
            "INSERT INTO audit_events(entity_type,entity_id,event_type,actor,actor_role,details_json,created_at) VALUES(?,?,?,?,?,?,?)",
            (entity_type, entity_id, event_type, actor, role, _json_dump(details), utc_now()),
        )

    def seed_demo_data(self) -> None:
        """Insert clearly illustrative demo records once; never overwrites user data."""
        with self._db() as con:
            count = con.execute("SELECT COUNT(*) FROM rfqs").fetchone()[0]
        if count:
            return
        samples = [
            ("RFQ-2611-101", "Aster Mobility", "EN8 mounting bracket", "Aditi Rao", "new", 5, "New request awaiting triage"),
            ("RFQ-2611-102", "Northstar Auto", "Precision spindle sleeve", "Rahul Mehta", "costing", 2, "Estimator is validating cycle time"),
            ("RFQ-2611-103", "Cobalt Components", "Transmission support plate", "Neha Iyer", "routing_review", 1, "New routing requires plant review"),
            ("RFQ-2611-104", "Aster Mobility", "EN8 mounting bracket - repeat", "Aditi Rao", "ready_for_quote", 3, "Costing complete; ready for commercial review"),
        ]
        today = date.today()
        with self._db() as con:
            for code, customer, part, owner, status, due_in, notes in samples:
                received = datetime.combine(today, datetime.min.time()).replace(tzinfo=UTC).isoformat()
                rfq_id = str(uuid.uuid4())
                now = utc_now()
                con.execute(
                    "INSERT INTO rfqs(id,rfq_code,customer,part_description,owner,received_at,due_date,status,notes,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                    (rfq_id, code, customer, part, owner, received, (today + timedelta(days=due_in)).isoformat(), status, notes, now, now),
                )
                self._audit(con, "rfq", rfq_id, "demo_rfq_seeded", "MarginLadder Demo", "system", {"rfq_code": code, "data_type": "illustrative"})

    def create_rfq(self, payload: dict[str, Any], actor: str, role: str) -> dict[str, Any]:
        role = _require_role(role, {"estimator", "estimation_head"})
        customer = str(payload.get("customer", "")).strip()
        part = str(payload.get("part_description", "")).strip()
        owner = str(payload.get("owner", actor)).strip()
        due_date = str(payload.get("due_date", "")).strip()
        notes = str(payload.get("notes", "")).strip()
        if not customer or len(customer) > 120:
            raise ServiceError("Customer is required and must be 120 characters or fewer")
        if not part or len(part) > 180:
            raise ServiceError("Part description is required and must be 180 characters or fewer")
        if not owner or len(owner) > 80:
            raise ServiceError("Owner is required and must be 80 characters or fewer")
        try:
            parsed_due = date.fromisoformat(due_date)
        except ValueError as exc:
            raise ServiceError("Due date must use YYYY-MM-DD format") from exc
        if parsed_due < date.today():
            raise ServiceError("Due date cannot be in the past")
        rfq_id = str(uuid.uuid4())
        now = utc_now()
        with self._db() as con:
            if not con.in_transaction:
                con.execute("BEGIN IMMEDIATE")  # serialise code allocation across writers
            prefix = f"RFQ-{date.today():%y%m}-"
            top = con.execute(
                "SELECT MAX(CAST(substr(rfq_code, ?) AS INTEGER)) FROM rfqs WHERE rfq_code LIKE ?",
                (len(prefix) + 1, prefix + "%")).fetchone()[0]
            code = f"{prefix}{(top or 0) + 1:03d}"
            con.execute(
                "INSERT INTO rfqs(id,rfq_code,customer,part_description,owner,received_at,due_date,status,notes,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (rfq_id, code, customer, part, owner, now, due_date, "new", notes, now, now),
            )
            self._audit(con, "rfq", rfq_id, "rfq_created", actor, role, {"rfq_code": code, "customer": customer})
        return self.get_rfq(rfq_id)

    _LATEST_QUOTE_JOIN = """
        LEFT JOIN quotes q ON q.rfq_id = r.id
         AND q.version = (SELECT MAX(version) FROM quotes WHERE rfq_id = r.id)
    """
    _RFQ_COLUMNS = ("r.*, q.id AS q_id, q.status AS q_status, q.version AS q_version, "
                    "q.annual_value AS q_annual_value, q.approval_required AS q_approval_required, "
                    "q.created_at AS q_created_at")

    def list_rfqs(self, status: str | None = None, search: str | None = None,
                  limit: int = 500, offset: int = 0) -> list[dict[str, Any]]:
        """One query for the page, latest quote included. Sorted by due date, then newest first."""
        where, args = self._rfq_filter(status, search)
        limit = max(1, min(int(limit), 500))
        offset = max(0, int(offset))
        sql = (f"SELECT {self._RFQ_COLUMNS} FROM rfqs r {self._LATEST_QUOTE_JOIN}{where} "
               "ORDER BY r.due_date ASC, r.created_at DESC, r.rfq_code ASC LIMIT ? OFFSET ?")
        with self._db() as con:
            rows = con.execute(sql, [*args, limit, offset]).fetchall()
        return [self._shape_rfq(dict(r)) for r in rows]

    def count_rfqs(self, status: str | None = None, search: str | None = None) -> int:
        where, args = self._rfq_filter(status, search)
        with self._db() as con:
            return con.execute(f"SELECT COUNT(*) FROM rfqs r{where}", args).fetchone()[0]

    @staticmethod
    def _rfq_filter(status: str | None, search: str | None) -> tuple[str, list[Any]]:
        clauses: list[str] = []
        args: list[Any] = []
        if status and status != "all":
            if status not in VALID_STATUSES:
                raise ServiceError("Unknown RFQ status filter")
            clauses.append("r.status = ?")
            args.append(status)
        if search and search.strip():
            escaped = search.strip().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            term = f"%{escaped}%"
            clauses.append("(r.rfq_code LIKE ? ESCAPE '\\' OR r.customer LIKE ? ESCAPE '\\' "
                           "OR r.part_description LIKE ? ESCAPE '\\' OR r.owner LIKE ? ESCAPE '\\')")
            args.extend([term] * 4)
        return ((" WHERE " + " AND ".join(clauses)) if clauses else ""), args

    @staticmethod
    def _shape_rfq(row: dict[str, Any]) -> dict[str, Any]:
        latest = None
        if row.get("q_id"):
            latest = {"id": row["q_id"], "status": row["q_status"], "version": row["q_version"],
                      "annual_value": row["q_annual_value"],
                      "approval_required": row["q_approval_required"], "created_at": row["q_created_at"]}
        for key in [k for k in row if k.startswith("q_")]:
            del row[key]
        row["latest_quote"] = latest
        row["is_overdue"] = row["due_date"] < date.today().isoformat() and row["status"] not in {"sent", "cancelled"}
        return row

    def get_rfq(self, rfq_id: str) -> dict[str, Any]:
        with self._db() as con:
            row = con.execute(
                f"SELECT {self._RFQ_COLUMNS} FROM rfqs r {self._LATEST_QUOTE_JOIN} WHERE r.id=?", (rfq_id,)).fetchone()
        if row is None:
            raise NotFoundError("RFQ not found")
        return self._shape_rfq(dict(row))

    def update_rfq(self, rfq_id: str, payload: dict[str, Any], actor: str, role: str) -> dict[str, Any]:
        role = _require_role(role, {"estimator", "estimation_head", "plant_head"})
        changes: dict[str, Any] = {}
        if "owner" in payload:
            if role not in {"estimation_head", "estimator"}:
                raise AccessDeniedError("Only an estimator or estimation head can change the RFQ owner")
            owner = str(payload["owner"]).strip()
            if not owner or len(owner) > 80:
                raise ServiceError("Owner must contain 1–80 characters")
            changes["owner"] = owner
        if "due_date" in payload:
            if role not in {"estimation_head", "estimator"}:
                raise AccessDeniedError("Only an estimator or estimation head can change the due date")
            due = str(payload["due_date"])
            try:
                parsed_due = date.fromisoformat(due)
            except ValueError as exc:
                raise ServiceError("Due date must use YYYY-MM-DD format") from exc
            if parsed_due < date.today():
                # A past date is allowed only if it is the date already stored. Otherwise an
                # overdue RFQ could not be reassigned: the editor sends owner and due date together.
                with self._db() as con:
                    current = con.execute("SELECT due_date FROM rfqs WHERE id=?", (rfq_id,)).fetchone()
                if current is None:
                    raise NotFoundError("RFQ not found")
                if current["due_date"] != due:
                    raise ServiceError("Due date cannot be in the past")
            changes["due_date"] = due
        if "status" in payload:
            target = str(payload["status"])
            if target not in VALID_STATUSES:
                raise ServiceError("Unknown RFQ status")
            if role == "plant_head" and target != "ready_for_quote":
                raise AccessDeniedError("Plant Head can only clear a routing review to ready_for_quote")
            with self._db() as con:
                current = con.execute("SELECT status FROM rfqs WHERE id=?", (rfq_id,)).fetchone()
                if current is None:
                    raise NotFoundError("RFQ not found")
                source = current["status"]
                if target not in ALLOWED_TRANSITIONS.get(source, set()):
                    raise ServiceError(f"Invalid status transition: {source} → {target}")
                if source == "routing_review" and target == "ready_for_quote" and role != "plant_head":
                    raise AccessDeniedError("Only the Plant Head can clear a routing review")
                changes["status"] = target
        if not changes:
            raise ServiceError("No supported RFQ fields were supplied")
        changes["updated_at"] = utc_now()
        assignments = ", ".join(f"{key}=?" for key in changes)
        with self._db() as con:
            cur = con.execute(f"UPDATE rfqs SET {assignments} WHERE id=?", (*changes.values(), rfq_id))
            if cur.rowcount == 0:
                raise NotFoundError("RFQ not found")
            self._audit(con, "rfq", rfq_id, "rfq_updated", actor, role, changes)
        return self.get_rfq(rfq_id)

    def create_quote(self, rfq_id: str, payload: dict[str, Any], actor: str, role: str) -> dict[str, Any]:
        role = _require_role(role, {"estimator", "estimation_head"})
        rfq = self.get_rfq(rfq_id)
        if rfq["status"] not in {"costing", "ready_for_quote", "sent_back"}:
            raise ServiceError(f"Cannot cost an RFQ while it is '{rfq['status']}'")
        quote_date_raw = str(payload.get("quote_date") or date.today().isoformat())
        try:
            quote_date = date.fromisoformat(quote_date_raw)
        except ValueError as exc:
            raise ServiceError("Quote date must use YYYY-MM-DD format") from exc
        parts = payload.get("parts") or [{"description": rfq["part_description"], **SAMPLE}]
        if not isinstance(parts, list) or not parts or len(parts) > 50:
            raise ServiceError("Provide between 1 and 50 part lines")
        tier_lines: dict[int, list[dict[str, Any]]] = {v: [] for v in TIER_VOLUMES}
        tier_totals: dict[int, dict[str, Decimal]] = {
            v: {"unit_price": Decimal("0"), "unit_cost": Decimal("0"), "annual_value": Decimal("0"), "gst": Decimal("0")}
            for v in TIER_VOLUMES
        }
        for index, part in enumerate(parts, start=1):
            if not isinstance(part, dict):
                raise ServiceError(f"Part line {index} must be an object")
            inputs = {**SAMPLE, **{k: v for k, v in part.items() if k in SAMPLE}}
            description = str(part.get("description") or f"Part {index}").strip()
            if not description:
                raise ServiceError(f"Part line {index} needs a description")
            for volume in TIER_VOLUMES:
                try:
                    result = cost_part(inputs, MASTER, quote_date, volume)
                except CostError as exc:
                    raise ServiceError(f"Part line {index}: {exc}") from exc
                except (DecimalException, TypeError) as exc:
                    raise ServiceError(f"Part line {index} contains a non-numeric costing input: {exc}") from exc
                result_dict = {k: (str(v) if isinstance(v, Decimal) else v) for k, v in result.items() if k != "snapshot"}
                result_dict["snapshot"] = result["snapshot"]
                line = {"line_number": index, "description": description, "result": result_dict}
                tier_lines[volume].append(line)
                tier_totals[volume]["unit_price"] += result["price"]
                tier_totals[volume]["unit_cost"] += result["cost"]
                tier_totals[volume]["annual_value"] += result["annual_value"]
                tier_totals[volume]["gst"] += result["gst"]
        tiers = []
        for volume in TIER_VOLUMES:
            total = tier_totals[volume]
            tiers.append({
                "annual_volume_per_part": volume,
                "total_unit_price": total["unit_price"].quantize(Decimal("0.01")),
                "total_unit_cost": total["unit_cost"].quantize(Decimal("0.01")),
                "total_gst_per_unit": total["gst"].quantize(Decimal("0.01")),
                "annual_value": total["annual_value"].quantize(Decimal("0.01")),
                "lines": tier_lines[volume],
            })
        selected_volume = int(payload.get("selected_volume", 180000))
        if selected_volume not in TIER_VOLUMES:
            raise ServiceError(f"Selected volume must be one of {', '.join(map(str, TIER_VOLUMES))}")
        selected = next(t for t in tiers if t["annual_volume_per_part"] == selected_volume)
        annual_value = Decimal(str(selected["annual_value"]))
        # Demo convention: approval threshold uses annual selling value excluding GST.
        # The brief does not specify the GST basis; confirm with the business before pilot.
        approval_required = needs_sales_head(annual_value, APPROVAL_THRESHOLD)
        version = rfq["latest_quote"]["version"] + 1 if rfq["latest_quote"] else 1
        quote_id = str(uuid.uuid4())
        status = "pending_approval" if approval_required else "approved"
        snapshot = {
            "engine": "engine.cost_engine.cost_part",
            "formula_version": "v1.0",
            "quote_date": quote_date.isoformat(),
            "selected_volume": selected_volume,
            "approval_threshold_inr": str(APPROVAL_THRESHOLD),
            "approval_required": approval_required,
            "parts": parts,
            "tiers": tiers,
            "selected_tier": selected,
            "data_classification": "illustrative_inputs_unless_replaced_by_signed_off_company_rates",
        }
        now = utc_now()
        with self._db() as con:
            con.execute(
                "INSERT INTO quotes(id,rfq_id,version,status,quote_date,approval_required,annual_value,snapshot_json,created_by,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (quote_id, rfq_id, version, status, quote_date.isoformat(), int(approval_required), str(annual_value), _json_dump(snapshot), actor, now),
            )
            con.execute("UPDATE rfqs SET status=?,updated_at=? WHERE id=?", (status, now, rfq_id))
            self._audit(con, "quote", quote_id, "quote_costed", actor, role,
                        {"rfq_id": rfq_id, "version": version, "selected_volume": selected_volume,
                         "annual_value": str(annual_value), "approval_required": approval_required,
                         "formula_version": "v1.0"})
            if approval_required:
                self._audit(con, "quote", quote_id, "approval_requested", actor, role,
                            {"requested_role": "sales_head_or_deputy", "annual_value": str(annual_value),
                             "threshold_inr": str(APPROVAL_THRESHOLD)})
        return self.get_quote(quote_id)

    def get_quote(self, quote_id: str) -> dict[str, Any]:
        with self._db() as con:
            row = con.execute("SELECT * FROM quotes WHERE id=?", (quote_id,)).fetchone()
        if row is None:
            raise NotFoundError("Quote not found")
        result = dict(row)
        result["snapshot"] = _json_load(result.pop("snapshot_json"), {})
        result["approval_required"] = bool(result["approval_required"])
        return result

    def list_quotes(self, rfq_id: str) -> list[dict[str, Any]]:
        self.get_rfq(rfq_id)
        with self._db() as con:
            ids = [r["id"] for r in con.execute("SELECT id FROM quotes WHERE rfq_id=? ORDER BY version DESC", (rfq_id,)).fetchall()]
        return [self.get_quote(qid) for qid in ids]

    def decide_quote(self, quote_id: str, action: str, reason: str, actor: str, role: str) -> dict[str, Any]:
        role = _require_role(role, {"sales_head", "deputy"})
        if action not in {"approve", "send_back"}:
            raise ServiceError("Decision must be 'approve' or 'send_back'")
        if action == "send_back" and len(reason.strip()) < 5:
            raise ServiceError("A send-back reason of at least five characters is required")
        quote = self.get_quote(quote_id)
        if quote["status"] != "pending_approval":
            raise ServiceError("Only a pending quote can receive an approval decision")
        if not quote["approval_required"]:
            raise ServiceError("This quote does not require Sales Head approval")
        now = utc_now()
        new_status = "approved" if action == "approve" else "sent_back"
        with self._db() as con:
            con.execute("UPDATE quotes SET status=?,decided_by=?,decided_at=?,decision_reason=? WHERE id=?",
                        (new_status, actor, now, reason.strip() if action == "send_back" else "", quote_id))
            con.execute("UPDATE rfqs SET status=?,updated_at=? WHERE id=?", (new_status, now, quote["rfq_id"]))
            self._audit(con, "quote", quote_id, f"quote_{action}d" if action == "approve" else "quote_sent_back",
                        actor, role, {"reason": reason.strip(), "new_status": new_status})
        return self.get_quote(quote_id)

    def send_quote(self, quote_id: str, actor: str, role: str) -> dict[str, Any]:
        role = _require_role(role, {"estimator", "estimation_head", "sales_head", "deputy"})
        quote = self.get_quote(quote_id)
        if quote["status"] != "approved":
            raise ServiceError("Only an approved quote can be marked as sent")
        now = utc_now()
        with self._db() as con:
            con.execute("UPDATE quotes SET status='sent' WHERE id=?", (quote_id,))
            con.execute("UPDATE rfqs SET status='sent',updated_at=? WHERE id=?", (now, quote["rfq_id"]))
            self._audit(con, "quote", quote_id, "quote_sent", actor, role, {"rfq_id": quote["rfq_id"]})
        return self.get_quote(quote_id)

    def audit_log(self, limit: int = 100, entity_id: str | None = None) -> list[dict[str, Any]]:
        limit = max(1, min(int(limit), 500))
        sql = "SELECT * FROM audit_events"
        args: list[Any] = []
        if entity_id:
            sql += " WHERE entity_id=?"
            args.append(entity_id)
        sql += " ORDER BY id DESC LIMIT ?"
        args.append(limit)
        with self._db() as con:
            rows = con.execute(sql, args).fetchall()
        events = []
        for row in rows:
            item = dict(row)
            item["details"] = _json_load(item.pop("details_json"), {})
            events.append(item)
        return events

    def dashboard(self) -> dict[str, Any]:
        statuses = {status: 0 for status in sorted(VALID_STATUSES)}
        today = date.today().isoformat()
        with self._db() as con:
            for row in con.execute("SELECT status, COUNT(*) AS n FROM rfqs GROUP BY status"):
                statuses[row["status"]] = row["n"]
            overdue = con.execute(
                "SELECT COUNT(*) FROM rfqs WHERE due_date<? AND status NOT IN ('sent','cancelled')", (today,)).fetchone()[0]
        total_rfqs = sum(statuses.values())
        quotes = []
        with self._db() as con:
            quote_rows = con.execute("""
                SELECT q.status,q.approval_required,q.annual_value
                FROM quotes q
                JOIN (SELECT rfq_id, MAX(version) AS latest_version FROM quotes GROUP BY rfq_id) latest
                  ON latest.rfq_id=q.rfq_id AND latest.latest_version=q.version
            """).fetchall()
            version_count = con.execute("SELECT COUNT(*) FROM quotes").fetchone()[0]
            audit_count = con.execute("SELECT COUNT(*) FROM audit_events").fetchone()[0]
        for row in quote_rows:
            quotes.append(dict(row))
        pending = sum(1 for q in quotes if q["status"] == "pending_approval")
        sent = sum(1 for q in quotes if q["status"] == "sent")
        total_value = sum((Decimal(q["annual_value"]) for q in quotes), Decimal("0"))
        return {
            "data_label": "Local demo database; records created here are application activity, not client results.",
            "rfq_count": total_rfqs,
            "open_rfq_count": total_rfqs - statuses["sent"] - statuses["cancelled"],
            "overdue_rfq_count": overdue,
            "status_counts": statuses,
            "latest_quote_count": len(quotes),
            "quote_version_count": version_count,
            "pending_approval_count": pending,
            "sent_quote_count": sent,
            "quoted_annual_value_inr": str(total_value),
            "audit_event_count": audit_count,
        }

    # ------------------------------------------------------------------ users and sessions
    def create_user(self, username: str, password: str, role: str, display_name: str | None = None) -> dict[str, Any]:
        username = (username or "").strip().lower()
        if not username or len(username) > 40 or not all(ch.isalnum() or ch in "._-" for ch in username):
            raise ServiceError("Username must be 1 to 40 letters, digits, dots, dashes or underscores")
        if role not in ROLE_NAMES:
            raise ServiceError("Unknown role")
        try:
            hashed = auth.hash_password(password)
        except ValueError as exc:
            raise ServiceError(str(exc)) from exc
        try:
            with self._db() as con:
                cur = con.execute(
                    "INSERT INTO users(username,display_name,role,password_hash,active,created_at) VALUES(?,?,?,?,1,?)",
                    (username, (display_name or username).strip()[:80], role, hashed, utc_now()))
                self._audit(con, "user", str(cur.lastrowid), "user_created", "system", "system",
                            {"username": username, "role": role})
        except sqlite3.IntegrityError as exc:
            raise ServiceError("That username already exists") from exc
        return {"username": username, "role": role, "display_name": (display_name or username).strip()[:80]}

    def authenticate(self, username: str, password: str) -> dict[str, Any]:
        """Check a password and open a session. The same message covers a wrong user or password."""
        username = (username or "").strip().lower()
        since = (datetime.now(UTC) - timedelta(minutes=LOCKOUT_MINUTES)).replace(microsecond=0).isoformat()
        with self._db() as con:
            recent = con.execute("SELECT COUNT(*) FROM login_failures WHERE username=? AND failed_at>=?",
                                 (username, since)).fetchone()[0]
            row = con.execute("SELECT * FROM users WHERE username=? AND active=1", (username,)).fetchone()
        if recent >= MAX_FAILED_LOGINS:
            raise ServiceError(f"Too many failed sign-ins. Try again in {LOCKOUT_MINUTES} minutes.")
        stored = row["password_hash"] if row else _DUMMY_HASH
        valid = auth.verify_password(password or "", stored) and row is not None
        if not valid:
            with self._db() as con:
                con.execute("INSERT INTO login_failures(username,failed_at) VALUES(?,?)", (username, utc_now()))
                self._audit(con, "user", username or "-", "login_failed", username or "-", "anonymous", {})
            raise ServiceError("Wrong username or password")
        token = auth.new_token()
        expires = (datetime.now(UTC) + timedelta(hours=SESSION_HOURS)).replace(microsecond=0).isoformat()
        with self._db() as con:
            con.execute("DELETE FROM login_failures WHERE username=?", (username,))
            con.execute("DELETE FROM sessions WHERE expires_at<?", (utc_now(),))
            con.execute("INSERT INTO sessions(token_hash,user_id,created_at,expires_at) VALUES(?,?,?,?)",
                        (auth.token_hash(token), row["id"], utc_now(), expires))
            self._audit(con, "user", str(row["id"]), "login", row["display_name"], row["role"], {})
        return {"token": token, "expires_at": expires,
                "user": {"username": row["username"], "display_name": row["display_name"], "role": row["role"]}}

    def user_for_token(self, token: str | None) -> dict[str, Any] | None:
        if not token:
            return None
        with self._db() as con:
            row = con.execute(
                "SELECT u.username,u.display_name,u.role,s.expires_at FROM sessions s JOIN users u ON u.id=s.user_id "
                "WHERE s.token_hash=? AND u.active=1", (auth.token_hash(token),)).fetchone()
        if row is None or row["expires_at"] < utc_now():
            return None
        return {"username": row["username"], "display_name": row["display_name"], "role": row["role"]}

    def logout(self, token: str | None) -> None:
        if token:
            with self._db() as con:
                con.execute("DELETE FROM sessions WHERE token_hash=?", (auth.token_hash(token),))

    def seed_demo_users(self) -> dict[str, str] | None:
        """Create one account per role with a random password. Returns the passwords once, else None."""
        with self._db() as con:
            if con.execute("SELECT COUNT(*) FROM users").fetchone()[0]:
                return None
        creds: dict[str, str] = {}
        for role in sorted(ROLE_NAMES):
            password = auth.new_token()[:16]
            self.create_user(role, password, role, role.replace("_", " ").title())
            creds[role] = password
        return creds

    # ------------------------------------------------------------------ KPIs from stored events
    def kpis(self) -> dict[str, Any]:
        """Cycle-time KPIs from this application's own records, in working days.

        Uses the KPI dictionary definitions. Demo records are not plant performance.
        """
        with self._db() as con:
            rfqs = con.execute("SELECT id,received_at,status FROM rfqs").fetchall()
            events = con.execute(
                "SELECT entity_type,entity_id,event_type,created_at,details_json FROM audit_events "
                "WHERE event_type IN ('rfq_updated','quote_costed','approval_requested','quote_approved','quote_sent_back','quote_sent') "
                "ORDER BY id").fetchall()
        first_costing: dict[str, str] = {}
        sent_at: dict[str, str] = {}
        req: dict[str, str] = {}
        decided: dict[str, str] = {}
        for e in events:
            d = _json_load(e["details_json"], {})
            if e["event_type"] == "rfq_updated" and d.get("status") == "costing":
                first_costing.setdefault(e["entity_id"], e["created_at"])
            elif e["event_type"] == "quote_sent":
                sent_at[d.get("rfq_id", "")] = e["created_at"]
            elif e["event_type"] == "approval_requested":
                req[e["entity_id"]] = e["created_at"]
            elif e["event_type"] in {"quote_approved", "quote_sent_back"}:
                decided[e["entity_id"]] = e["created_at"]

        def days(a: str, b: str) -> float:
            return trace_analyze.working_days(datetime.fromisoformat(a).replace(tzinfo=None),
                                              datetime.fromisoformat(b).replace(tzinfo=None))

        t2q = [days(r["received_at"], sent_at[r["id"]]) for r in rfqs if r["id"] in sent_at]
        t2c = [days(r["received_at"], first_costing[r["id"]]) for r in rfqs if r["id"] in first_costing]
        appr = [days(req[q], decided[q]) for q in req if q in decided]
        n_total = len(rfqs)
        out: dict[str, Any] = {
            "data_label": "Application records only. Demo data is not plant performance.",
            "rfq_total": n_total,
            "sent_n": len(t2q),
            "not_yet_sent_rate": round(1 - len(t2q) / n_total, 4) if n_total else 0.0,
            "time_to_quote_median_days": None, "time_to_quote_p90_days": None,
            "sent_within_4_days_rate": None,
            "intake_to_costing_median_days": None,
            "approval_wait_median_days": None, "approval_wait_n": len(appr),
        }
        if t2q:
            out["time_to_quote_median_days"] = round(trace_analyze.percentile(t2q, 0.5), 3)
            out["time_to_quote_p90_days"] = round(trace_analyze.percentile(t2q, 0.9), 3)
            out["sent_within_4_days_rate"] = round(sum(1 for x in t2q if x <= 4) / len(t2q), 4)
        if t2c:
            out["intake_to_costing_median_days"] = round(trace_analyze.percentile(t2c, 0.5), 3)
        if appr:
            out["approval_wait_median_days"] = round(trace_analyze.percentile(appr, 0.5), 3)
        return out

    # ------------------------------------------------------------------ Week-1 trace import
    def import_trace(self, rows: list[dict[str, str | None]], actor: str, role: str, batch_id: str | None = None) -> dict[str, Any]:
        """Store a batch of real RFQ timestamps. All rows are valid or none are stored."""
        role = _require_role(role, {"estimation_head"})
        if not rows or len(rows) > 2000:
            raise ServiceError("Provide between 1 and 2000 trace rows")
        parsed, seen = [], set()
        for number, raw in enumerate(rows, start=1):
            try:
                row = trace_analyze.parse_row({k: ("" if v is None else str(v)) for k, v in raw.items()})
            except trace_analyze.TraceError as exc:
                raise ServiceError(f"Row {number}: {exc}") from exc
            if row.ref in seen:
                raise ServiceError(f"Row {number}: {row.ref} appears twice in this batch")
            seen.add(row.ref)
            parsed.append((row.ref, raw))
        batch = (batch_id or datetime.now(UTC).strftime("trace-%Y%m%d-%H%M%S")).strip()[:60]
        try:
            with self._db() as con:
                for ref, raw in parsed:
                    con.execute("INSERT INTO trace_rfqs(batch_id,rfq_ref,row_json,imported_by,imported_at) VALUES(?,?,?,?,?)",
                                (batch, ref, _json_dump(raw), actor, utc_now()))
                self._audit(con, "trace", batch, "trace_imported", actor, role, {"rows": len(parsed)})
        except sqlite3.IntegrityError as exc:
            raise ServiceError("This batch id was already imported") from exc
        return {"batch_id": batch, "rows": len(parsed)}

    def trace_summary(self, batch_id: str | None = None) -> dict[str, Any]:
        sql, args = "SELECT row_json FROM trace_rfqs", []
        if batch_id:
            sql += " WHERE batch_id=?"
            args.append(batch_id)
        with self._db() as con:
            rows = [_json_load(r["row_json"], {}) for r in con.execute(sql, args)]
        if not rows:
            return {"rows": 0, "decision": "No trace rows imported yet.",
                    "data_label": "Real timestamps only. The simulated log is a separate placeholder."}
        out = trace_analyze.summarise(rows)
        out["data_label"] = "Computed from imported trace rows. Check that they are real before quoting."
        return out

    def simulated_cycle_analytics(self) -> dict[str, Any]:
        if not SIMULATED_LOG.exists():
            return {"data_type": "simulated", "available": False, "message": "Simulated source log not found"}
        with SIMULATED_LOG.open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        numeric = [float(row["Total days"]) for row in rows]
        stage_names = ["Intake wait", "Costing", "Routing check wait", "Approval wait", "Send and rework"]
        stage_means = {name: round(sum(float(row[name]) for row in rows) / len(rows), 2) for name in stage_names}
        sorted_days = sorted(numeric)
        median = sorted_days[len(sorted_days) // 2] if len(sorted_days) % 2 else (sorted_days[len(sorted_days)//2 - 1] + sorted_days[len(sorted_days)//2]) / 2
        return {
            "data_type": "simulated",
            "available": True,
            "label": "Synthetic example only — not observed client performance",
            "sample_size": len(rows),
            "mean_cycle_days": round(sum(numeric) / len(numeric), 2),
            "median_cycle_days": round(median, 2),
            "p90_cycle_days": round(sorted_days[min(len(sorted_days)-1, max(0, ceil(0.9 * len(sorted_days)) - 1))], 2),
            "within_four_days": sum(1 for value in numeric if value <= 4),
            "stage_means_days": stage_means,
            "source": "data/simulated_rfq_log.csv",
        }
