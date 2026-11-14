from __future__ import annotations

import logging
from collections import Counter
from pathlib import Path

from pydantic import ValidationError

from app.problems import AppError
from app.video_pools.schemas import (
    CategoryCount,
    ExpansionPage,
    PoolBundle,
    PoolOverview,
    SeriesBundle,
    SeriesKey,
    SeriesOverview,
    ThemeDetail,
    ThemePage,
    ThemeSort,
    ThemeStatus,
    ThemeSummary,
)

logger = logging.getLogger(__name__)
BUNDLE_PATH = Path(__file__).parent / "data" / "pools.json"
MAX_BUNDLE_BYTES = 16 * 1024 * 1024


def load_bundle() -> PoolBundle:
    """Read the image's immutable pool bundle, failing closed on missing or invalid data.

    The bundle is generated from docs/videos by tools/video/pool-admin/bundle.mjs; the API
    never reads repository documents, host directories or the database for it.
    """
    try:
        with BUNDLE_PATH.open("rb") as source:
            content = source.read(MAX_BUNDLE_BYTES + 1)
        if len(content) > MAX_BUNDLE_BYTES:
            raise ValueError("pool bundle exceeds the packaged size limit")
        return PoolBundle.model_validate_json(content)
    except (OSError, ValueError, ValidationError) as exc:
        logger.error("Packaged video pool bundle is unavailable (%s)", type(exc).__name__)
        raise AppError(
            503,
            "video_pools_unavailable",
            "題目池資料包缺漏或驗證失敗，請檢查部署版本",
        ) from exc


def _series(bundle: PoolBundle, key: SeriesKey) -> SeriesBundle:
    return next(series for series in bundle.series if series.key == key)


def overview() -> PoolOverview:
    bundle = load_bundle()
    return PoolOverview(
        series=[
            SeriesOverview(
                key=series.key,
                name=series.name,
                revision=series.revision,
                counts=series.counts,
                audience_min=series.audience_min,
                themes_sha256=series.sources.themes_sha256,
            )
            for series in bundle.series
        ]
    )


def _status_matches(theme: ThemeDetail, status: ThemeStatus) -> bool:
    if status == "producible":
        return theme.producible
    if status == "reserve":
        return theme.long and not theme.producible
    if status == "short":
        return not theme.long
    return True


def _search(theme: ThemeDetail, query: str) -> bool:
    return any(query in value.casefold() for value in (theme.id, theme.title, theme.core_question))


def _summary(theme: ThemeDetail) -> ThemeSummary:
    return ThemeSummary.model_validate(
        theme.model_dump(include=set(ThemeSummary.model_fields)), strict=False
    )


def list_themes(
    key: SeriesKey,
    *,
    status: ThemeStatus = "producible",
    category: str | None = None,
    min_score: float | None = None,
    q: str | None = None,
    sort: ThemeSort = "rank",
    page: int = 1,
    page_size: int = 25,
) -> ThemePage:
    series = _series(load_bundle(), key)
    query = (q or "").strip().casefold()
    in_status = [theme for theme in series.themes if _status_matches(theme, status)]
    matches = [
        theme
        for theme in in_status
        if (category is None or theme.category == category)
        and (
            min_score is None or (theme.audience is not None and theme.audience.score >= min_score)
        )
        and (not query or _search(theme, query))
    ]
    if sort == "rank":
        matches.sort(
            key=lambda theme: (
                theme.audience is None,
                theme.audience.rank if theme.audience else 0,
                theme.id,
            )
        )
    else:
        matches.sort(key=lambda theme: theme.id)
    offset = (page - 1) * page_size
    categories = Counter(theme.category for theme in in_status if theme.category)
    return ThemePage(
        items=[_summary(theme) for theme in matches[offset : offset + page_size]],
        total=len(matches),
        page=page,
        page_size=page_size,
        categories=[
            CategoryCount(category=name, count=count) for name, count in sorted(categories.items())
        ],
    )


def theme_detail(key: SeriesKey, theme_id: str) -> ThemeDetail:
    series = _series(load_bundle(), key)
    for theme in series.themes:
        if theme.id == theme_id:
            return theme
    raise AppError(404, "video_pool_theme_not_found", "找不到這個題案")


def expansions(key: SeriesKey) -> ExpansionPage:
    series = _series(load_bundle(), key)
    return ExpansionPage(
        expansions=list(reversed(series.expansions)), checkpoints=list(reversed(series.checkpoints))
    )
