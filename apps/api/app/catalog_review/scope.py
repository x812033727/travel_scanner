"""Domain boundaries for catalog runs, including pre-scope mixed history."""

from typing import Any, Literal

from app.catalog_review.schemas import CatalogKind
from app.problems import AppError

CatalogScope = Literal["all", "hotspots", "foods"]
SCOPE_KINDS: dict[CatalogScope, tuple[CatalogKind, ...]] = {
    "all": ("hotspot", "food", "merchant"),
    "hotspots": ("hotspot",),
    "foods": ("food", "merchant"),
}
DEFAULT_COUNTS = {"hotspot": 40, "food": 20, "merchant": 40}


def request_scope(request: dict[str, Any] | None) -> CatalogScope:
    value = (request or {}).get("scope", "all")
    if not isinstance(value, str) or value not in SCOPE_KINDS:
        raise AppError(422, "catalog_scope_invalid", "無法辨識目錄審核範圍")
    return value


def scope_counts(scope: CatalogScope) -> dict[str, int]:
    return {
        kind: count if kind in SCOPE_KINDS[scope] else 0 for kind, count in DEFAULT_COUNTS.items()
    }
