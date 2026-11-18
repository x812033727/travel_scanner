"""Which show and topic a video is filed under on the review page's catalog (migration 0147).

The owner, 2026-11-18: 奇聞檔案局 and 原來如此事務所 each stand on their own instead of inside
觀念解說, findable by their topics (H-歷史懸案, 生物動物與植物…), and the dramas can be picked one
at a time (種田娶妻打天下, 恁祖媽今年18…). Google Drive backup already files every video by the
same two things (app/video_backup/target.py), so the catalog reads the same rules and the two
never disagree: ``series_key`` is the show or drama, ``topic`` the explainer show's category.

The two are stored on the row (not worked out per query) because a 原來如此事務所 topic comes
from a long code table SQL cannot read. Every write of a slug, category or series_slug calls
``refresh``; ``python -m app.cli video-shelf-backfill`` fills the rows that existed before.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import VideoProject
from app.problems import AppError
from app.video_automation.models import VideoDramaSeries
from app.video_dramas.catalog import load_index

# The explainer shows that stand on their own in the catalog's first row; everything else is
# grouped by its category. The same keys as app.video_backup.target.SLUG_PREFIXES.
SHOWS: tuple[str, ...] = ("curio", "sothatswhy")
SERIES_KEY_MAX = 40
TOPIC_MAX = 40


def shelf_fields(project: VideoProject) -> tuple[str | None, str | None]:
    """``(series_key, topic)``: ``('curio', 'H-歷史懸案')``, ``('tai-nainai', None)``, or
    ``(None, None)`` for a Short or a video that belongs to no series."""
    # Imported here: target imports admin_service, which imports this module.
    from app.video_backup import target

    if project.shorts_line is not None:
        return None, None
    key: str | None = project.series_slug or target.drama_series(project)
    if key is None:
        key = next(
            (name for prefix, name in target.SLUG_PREFIXES if project.slug.startswith(prefix)),
            None,
        )
    if key is None:
        return None, None
    topic = target.ai_episode_parts(project, key)[0] if key in SHOWS else None
    return key[:SERIES_KEY_MAX], (topic[:TOPIC_MAX] if topic else None)


def refresh(project: VideoProject) -> bool:
    """Write the row's ``series_key`` and ``topic`` from its slug, category and series;
    True when either changed."""
    series_key, topic = shelf_fields(project)
    changed = project.series_key != series_key or project.topic != topic
    project.series_key = series_key
    project.topic = topic
    return changed


def series_labels(
    folder_names: Mapping[str, str], series_titles: Mapping[str, str]
) -> dict[str, str]:
    """Each series key's name for the catalog, the first that has one: the owner's Drive
    folder names, the defaults Drive backup uses, the long series' titles, then the packaged
    dramas' names. A key with none is shown as itself."""
    from app.video_backup import target

    labels: dict[str, str] = {}
    try:
        labels.update({series.key: series.name for series in load_index().series})
    except AppError:
        pass  # a missing script bundle only costs the label
    labels.update({key: title for key, title in series_titles.items() if title})
    labels.update(target.DEFAULT_FOLDER_NAMES)
    labels.update({key: name.strip() for key, name in folder_names.items() if name.strip()})
    return labels


async def load_series_labels(session: AsyncSession) -> dict[str, str]:
    from app.video_backup.admin_settings import config_of, mapping_of, settings_row

    titles = {
        str(slug): str(title)
        for slug, title in (
            await session.execute(select(VideoDramaSeries.slug, VideoDramaSeries.title))
        ).all()
    }
    folder_names = mapping_of(config_of(await settings_row(session)), "folder_names")
    return series_labels(folder_names, titles)


async def backfill(session: AsyncSession, *, apply: bool) -> dict[str, Any]:
    """Work out every video's ``series_key`` and ``topic`` (``python -m app.cli
    video-shelf-backfill``): how many would change, per show, and commit only when ``apply``.
    Safe to run again; a second run changes nothing."""
    projects = list((await session.scalars(select(VideoProject))).all())
    changed: Counter[str] = Counter()
    for project in projects:
        if refresh(project):
            changed[project.series_key or "none"] += 1
    if apply:
        await session.commit()
    else:
        await session.rollback()
    return {
        "apply": apply,
        "videos": len(projects),
        "changed": sum(changed.values()),
        "by_series": dict(sorted(changed.items())),
    }
