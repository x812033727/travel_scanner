from __future__ import annotations

import logging
from collections import Counter
from pathlib import Path
from typing import Any, Literal

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import VideoProject
from app.problems import AppError
from app.video_pools.schemas import (
    CategoryCount,
    EpisodePage,
    EpisodeStatus,
    EpisodeStatusRow,
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


async def episodes(
    session: AsyncSession,
    key: SeriesKey,
    *,
    status: EpisodeStatus = "published",
    q: str | None = None,
) -> EpisodePage:
    """Produced episodes with their live upload state from the site's video projects.

    A slug the site knows wins over the catalog's recorded id; the first listed slug is the
    current version, so its upload is preferred over an older recut's.
    """
    series = _series(load_bundle(), key)
    slugs = sorted({slug for episode in series.episodes for slug in episode.slugs})
    projects: dict[str, Any] = {}
    if slugs:
        result = await session.execute(
            select(
                VideoProject.slug,
                VideoProject.youtube_video_id,
                VideoProject.youtube_publish_at,
                VideoProject.stage,
                VideoProject.dropped_at,
            ).where(VideoProject.slug.in_(slugs))
        )
        projects = {row.slug: row for row in result.all()}
    rows: list[EpisodeStatusRow] = []
    for episode in series.episodes:
        known = [projects[slug] for slug in episode.slugs if slug in projects]
        uploaded = next((row for row in known if row.youtube_video_id and not row.dropped_at), None)
        current = uploaded or (known[0] if known else None)
        youtube_id = uploaded.youtube_video_id if uploaded else episode.catalog.youtube_id
        source: Literal["site", "catalog"] | None = (
            "site" if uploaded else ("catalog" if youtube_id else None)
        )
        rows.append(
            EpisodeStatusRow(
                key=episode.key,
                code=episode.code,
                title=episode.title,
                category=episode.category,
                slugs=episode.slugs,
                candidate_ids=episode.candidate_ids,
                published=youtube_id is not None,
                youtube_id=youtube_id,
                youtube_url=f"https://www.youtube.com/watch?v={youtube_id}" if youtube_id else None,
                youtube_source=source,
                site_slug=current.slug if current else None,
                publish_at=current.youtube_publish_at if current else None,
                stage=current.stage if current else None,
                dropped=bool(current and current.dropped_at),
                privacy=episode.catalog.privacy if source == "catalog" else None,
            )
        )
    query = (q or "").strip().casefold()
    matches = [
        row
        for row in rows
        if (status == "all" or row.published == (status == "published"))
        and (
            not query
            or any(
                query in value.casefold()
                for value in (row.title, row.code or "", *row.slugs, *row.candidate_ids)
            )
        )
    ]
    published = sum(row.published for row in rows)
    return EpisodePage(
        items=matches, total=len(matches), published=published, unpublished=len(rows) - published
    )
