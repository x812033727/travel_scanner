"""Monthly budgets of the media stages, on the counter the narration budget already uses.

``app.providers.usage_meter`` keys its calendar-month counters by a provider string, so the
clip seconds, images, tracks and judge calls each get their own key and the same atomic
"refuse a request that would pass the budget" reservation. Dollars are not metered there:
they are the sum of ``usd_estimate`` over this month's jobs, priced from the catalog.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal

from redis.asyncio import Redis
from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.providers.usage_meter import (
    azure_speech_usage_snapshot,
    release_azure_speech_characters,
    reserve_azure_speech_characters,
)
from app.video_automation.models import VideoAutomationSettings
from app.video_media.catalog import JUDGE_USD_PER_CALL, MediaModel
from app.video_media.models import VideoMediaJob
from app.video_media.schemas import BudgetView

CLIP_SECONDS = "video-media-clip-seconds"
IMAGES = "video-media-images"
MUSIC = "video-media-music"
JUDGE_CALLS = "video-media-judge-calls"
UNITS = {CLIP_SECONDS: "seconds", IMAGES: "images", MUSIC: "tracks", JUDGE_CALLS: "calls"}
BUDGET_NAMES = {
    CLIP_SECONDS: "clip_seconds",
    IMAGES: "images",
    MUSIC: "music",
    JUDGE_CALLS: "judge_calls",
}
METER_BY_KIND = {"clip": CLIP_SECONDS, "image": IMAGES, "music": MUSIC}


def budget_of(row: VideoAutomationSettings, meter: str) -> int:
    return {
        CLIP_SECONDS: row.monthly_clip_seconds_budget,
        IMAGES: row.monthly_images_budget,
        MUSIC: row.monthly_music_budget,
        JUDGE_CALLS: row.monthly_judge_calls_budget,
    }[meter]


def units_of(kind: str, seconds: int) -> int:
    return seconds if kind == "clip" else 1


async def reserve(redis: Redis, meter: str, units: int, budget: int) -> bool:
    """Atomically take ``units`` from this month's budget; False when they would exceed it."""
    return await reserve_azure_speech_characters(redis, units, budget, provider=meter)


async def release(redis: Redis, meter: str, units: int) -> None:
    await release_azure_speech_characters(redis, units, provider=meter)


async def used(redis: Redis, meter: str) -> int:
    snapshot = await azure_speech_usage_snapshot(redis, 0, provider=meter)
    return int(snapshot.used or 0)


async def budgets_view(redis: Redis, row: VideoAutomationSettings) -> dict[str, BudgetView]:
    view: dict[str, BudgetView] = {}
    for meter, name in BUDGET_NAMES.items():
        limit = budget_of(row, meter)
        spent = await used(redis, meter)
        view[name] = BudgetView(
            unit=UNITS[meter], limit=limit, used=spent, remaining=max(limit - spent, 0)
        )
    return view


def usd_for(model: MediaModel, kind: str, seconds: int) -> Decimal:
    """What one generation costs at the catalog's list price."""
    if kind == "clip":
        return Decimal(str(model.usd_per_second or 0)) * seconds
    if kind == "image":
        return Decimal(str(model.usd_per_image or 0))
    return Decimal(str(model.usd_per_track or 0))


def month_start(now: datetime | None = None) -> datetime:
    moment = now or datetime.now(UTC)
    return moment.astimezone(UTC).replace(day=1, hour=0, minute=0, second=0, microsecond=0)


async def month_usd(session: AsyncSession, redis: Redis, now: datetime | None = None) -> float:
    """This month's spend: submitted and ready jobs at list price, plus the judge calls."""
    total = await session.scalar(
        select(func.coalesce(func.sum(VideoMediaJob.usd_estimate), 0)).where(
            VideoMediaJob.created_at >= month_start(now),
            VideoMediaJob.status.in_(("submitted", "ready")),
        )
    )
    judged = await used(redis, JUDGE_CALLS)
    return round(float(total or 0) + judged * JUDGE_USD_PER_CALL, 4)


async def slug_usd(session: AsyncSession, slug: str) -> float:
    """What one video's generations have cost so far (any month)."""
    total = await session.scalar(
        select(func.coalesce(func.sum(VideoMediaJob.usd_estimate), 0)).where(
            VideoMediaJob.slug == slug, VideoMediaJob.status.in_(("submitted", "ready"))
        )
    )
    return round(float(total or 0), 4)


@dataclass(frozen=True)
class SlugSpend:
    """What one video's generations have cost so far, and how many clip seconds it bought."""

    usd: float
    clip_seconds: int


async def spend_by_slug(session: AsyncSession, slugs: Sequence[str]) -> dict[str, SlugSpend]:
    """The spend of each of these videos, in one query; a video with no jobs is left out."""
    if not slugs:
        return {}
    clip_seconds = case((VideoMediaJob.kind == "clip", VideoMediaJob.seconds), else_=0)
    rows = await session.execute(
        select(
            VideoMediaJob.slug,
            func.coalesce(func.sum(VideoMediaJob.usd_estimate), 0),
            func.coalesce(func.sum(clip_seconds), 0),
        )
        .where(
            VideoMediaJob.slug.in_(list(slugs)),
            VideoMediaJob.status.in_(("submitted", "ready")),
        )
        .group_by(VideoMediaJob.slug)
    )
    return {
        str(slug): SlugSpend(usd=round(float(usd or 0), 4), clip_seconds=int(seconds or 0))
        for slug, usd, seconds in rows.all()
    }
