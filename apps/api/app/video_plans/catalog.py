from __future__ import annotations

import logging
from collections import Counter
from pathlib import Path

from pydantic import ValidationError

from app.problems import AppError
from app.video_plans.schemas import (
    CATALOG_COUNTS,
    STAGES,
    CatalogBundle,
    CatalogCount,
    PlanCatalog,
    PlanEntry,
    PlanPage,
    PlanStage,
    StageCount,
)

logger = logging.getLogger(__name__)
CATALOG_PATH = Path(__file__).parent / "data" / "catalog.json"
MAX_CATALOG_BYTES = 16 * 1024 * 1024


def load_catalog() -> CatalogBundle:
    """Read the image's immutable bundle, failing closed on missing/invalid data.

    Do not reuse a previous successful read after a file changes: an incomplete
    image must surface as unavailable, rather than presenting stale plans as valid.
    No repository documents, database records or provider requests are consulted.
    """
    try:
        with CATALOG_PATH.open("rb") as source:
            content = source.read(MAX_CATALOG_BYTES + 1)
        if len(content) > MAX_CATALOG_BYTES:
            raise ValueError("planning catalog exceeds the packaged size limit")
        return CatalogBundle.model_validate_json(content)
    except (OSError, ValueError, ValidationError) as exc:
        logger.error("Packaged video planning catalog is unavailable (%s)", type(exc).__name__)
        raise AppError(
            503,
            "video_plans_unavailable",
            "影片企劃資料包缺漏或驗證失敗，請檢查部署版本",
        ) from exc


def _matches_search(entry: PlanEntry, query: str) -> bool:
    fields = (
        entry.id,
        entry.video_slug,
        entry.title,
    )
    return any(query in value.casefold() for value in fields)


def list_plans(
    *,
    q: str | None = None,
    catalog: PlanCatalog | None = None,
    stage: PlanStage | None = None,
    page: int = 1,
    page_size: int = 25,
) -> PlanPage:
    bundle = load_catalog()
    query = (q or "").strip().casefold()
    matches = [
        entry
        for entry in bundle.entries
        if (catalog is None or entry.catalog == catalog)
        and (stage is None or entry.stage == stage)
        and (not query or _matches_search(entry, query))
    ]
    offset = (page - 1) * page_size
    stage_counts = Counter(entry.stage for entry in bundle.entries)
    return PlanPage(
        items=matches[offset : offset + page_size],
        total=len(matches),
        page=page,
        page_size=page_size,
        catalogs=[
            CatalogCount(catalog=key, count=bundle.catalog_counts[key]) for key in CATALOG_COUNTS
        ],
        stages=[StageCount(stage=key, count=stage_counts[key]) for key in STAGES],
        catalog_total=len(bundle.entries),
        plans_sha256=bundle.plans_sha256,
    )
