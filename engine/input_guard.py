"""Input checks that sit in front of the retained v1 costing engine.

`engine/cost_engine.py` is kept byte-identical to the v1 release, so a gap in its validation is closed here instead.
The gap: the loop that rejects zero and negative values lists `gross` and `net` in its condition but not in the tuple
it iterates, so those two weights were never range-checked. A part with `net = -1` priced at about half the normal
price, and `gross = 0` was accepted. The engine still rejects net above gross, so only the lower bound is added here.
"""
from __future__ import annotations

from decimal import Decimal as D
from typing import Any

from engine.cost_engine import CostError

POSITIVE_WEIGHT_KEYS = ("gross", "net")


def validate_part_inputs(part: dict[str, Any]) -> None:
    """Raise CostError unless gross and net weight are finite numbers above zero."""
    for key in POSITIVE_WEIGHT_KEYS:
        raw = part.get(key)
        if raw is None or str(raw).strip() == "":
            raise CostError(f"non-numeric costing input: {key} is required")
        try:
            value = D(str(raw))
        except Exception as exc:
            raise CostError(f"non-numeric costing input: {key} must be a finite number") from exc
        if not value.is_finite():
            raise CostError(f"non-numeric costing input: {key} must be a finite number")
        if value <= 0:
            raise CostError(f"{key}: must be above zero")
