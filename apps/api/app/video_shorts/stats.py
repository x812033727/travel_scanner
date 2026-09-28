"""The numbers YouTube reports for a public Short, kept as they came
(docs/videos/SHORTS.md §成效與每週報告).

A snapshot is taken in three windows after the Short went public: the first read between
24 and 48 hours is day 1, between 72 and 96 hours day 3, between 7 and 9 days day 7. A window
keeps its first read and is never overwritten, and one that passed unread stays empty rather
than being filled with a later, larger number. ``now`` is the latest read, refreshed once a day
for four months and every twenty-five days after that.

The same read tells whether the video is still there and still public: one that is gone, or
private again, is marked as taken down and no longer read. That is also the check YouTube's
developer policies ask for, at least every thirty days, of what a client stores, which is why
the numbers of an old Short are still read now and then. One the owner gave another time in
Studio is not taken down: YouTube's time is then the Short's.

Nothing here adds, averages, ranks or rates: the policies do not let a client derive metrics
from API data unless its audit covers that, and this one's does not yet.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import VideoProject
from app.video_shorts.models import VideoShortsMetric, VideoShortsSlot
from app.video_shorts.quota import Quota
from app.video_youtube.client import YoutubeClient
from app.video_youtube.requests import as_dict
from app.video_youtube.state import parse_time

WINDOWS: tuple[tuple[str, timedelta, timedelta], ...] = (
    ("d1", timedelta(hours=24), timedelta(hours=48)),
    ("d3", timedelta(hours=72), timedelta(hours=96)),
    ("d7", timedelta(days=7), timedelta(days=9)),
)
NOW_EVERY = timedelta(hours=24)
# After four months the numbers move little; they are read often enough for the thirty days
# the developer policies give.
RESTS_AFTER = timedelta(days=120)
RESTING_EVERY = timedelta(days=25)
# How long after its publish time a video may still read as private before it counts as
# taken down.
PUBLISHING_GRACE = timedelta(hours=2)
SOURCE = "data_api"
BATCH = 50
STATS_PARTS = "statistics,status"
COUNTS = (("views", "viewCount"), ("likes", "likeCount"), ("comments", "commentCount"))
NOT_PUBLIC = "YouTube 上沒有公開：影片被刪除，或改回私人了"


@dataclass(frozen=True)
class Read:
    snapshots: int = 0
    published: int = 0
    removed: int = 0
    moved: int = 0
    calls: int = 0


def due_periods(published_at: datetime, now: datetime, have: dict[str, datetime]) -> list[str]:
    """The snapshots to take of a Short now: the windows it is inside and has no read of,
    and the latest read when the one there is a day old (twenty-five days, for a Short that
    has been public four months). ``have`` maps a period to when it was read."""
    age = now - published_at
    if age < timedelta(0):
        return []
    due = [
        period for period, opens, closes in WINDOWS if opens <= age < closes and period not in have
    ]
    latest = have.get("now")
    every = NOW_EVERY if age < RESTS_AFTER else RESTING_EVERY
    if latest is None or now - latest >= every:
        due.append("now")
    return due


def counts_of(video: dict[str, Any]) -> dict[str, int | None]:
    """The counts as YouTube gave them; one it left out (likes hidden by the owner, comments
    turned off) stays empty instead of reading as zero."""
    statistics = as_dict(video.get("statistics"))
    found: dict[str, int | None] = {}
    for name, key in COUNTS:
        value = statistics.get(key)
        found[name] = int(value) if isinstance(value, int | str) and str(value).isdigit() else None
    return found


def is_public(video: dict[str, Any] | None) -> bool:
    return video is not None and as_dict(video.get("status")).get("privacyStatus") == "public"


def moved_to(video: dict[str, Any] | None, now: datetime) -> datetime | None:
    """The time a video that is not public yet is scheduled for on YouTube, when that is
    still ahead: the owner gave it another time in Studio."""
    if video is None:
        return None
    later = parse_time(as_dict(video.get("status")).get("publishAt"))
    return later if later is not None and later > now else None


async def read_due(
    session: AsyncSession, client: YoutubeClient, quota: Quota, now: datetime | None = None
) -> Read:
    """Take the snapshots that are due, mark the slots of Shorts YouTube made public, and
    mark what was taken down. The caller commits."""
    moment = now or datetime.now(UTC)
    projects = list(
        await session.scalars(
            select(VideoProject).where(
                VideoProject.shorts_line.is_not(None),
                VideoProject.youtube_video_id.is_not(None),
                VideoProject.youtube_publish_at.is_not(None),
                VideoProject.youtube_publish_at <= moment,
                VideoProject.youtube_removed_at.is_(None),
                VideoProject.dropped_at.is_(None),
            )
        )
    )
    if not projects:
        return Read()
    rows = list(
        await session.scalars(
            select(VideoShortsMetric).where(
                VideoShortsMetric.source == SOURCE,
                VideoShortsMetric.youtube_video_id.in_(
                    [str(project.youtube_video_id) for project in projects]
                ),
            )
        )
    )
    stored = {(row.youtube_video_id, row.period): row for row in rows}
    slots = {
        str(slot.project_slug): slot
        for slot in await session.scalars(
            select(VideoShortsSlot).where(
                VideoShortsSlot.status == "scheduled",
                VideoShortsSlot.project_slug.in_([project.slug for project in projects]),
            )
        )
    }
    wanted: list[tuple[VideoProject, list[str]]] = []
    for project in projects:
        video_id = str(project.youtube_video_id)
        have = {
            period: row.captured_at for (owner, period), row in stored.items() if owner == video_id
        }
        due = due_periods(project.youtube_publish_at or moment, moment, have)
        # A slot that waits to hear YouTube made its Short public is a reason to ask too.
        if due or project.slug in slots:
            wanted.append((project, due))
    snapshots = published = removed = moved = calls = 0
    for start in range(0, len(wanted), BATCH):
        batch = wanted[start : start + BATCH]
        videos = await client.videos(
            [str(project.youtube_video_id) for project, _due in batch], parts=STATS_PARTS
        )
        calls += 1
        await quota.add("videos.list")
        by_id = {str(video.get("id")): video for video in videos}
        for project, due in batch:
            video_id = str(project.youtube_video_id)
            video = by_id.get(video_id)
            slot = slots.get(project.slug)
            if not is_public(video):
                later = moved_to(video, moment)
                if later is not None:
                    project.youtube_publish_at = later
                    project.updated_at = moment
                    moved += 1
                    if slot is not None:
                        slot.note = "站主在 Studio 改了公開時間，以 YouTube 上的時間為準"
                        slot.updated_at = moment
                # YouTube makes a scheduled video public at its time, give or take a little:
                # one that is not public yet is asked about again on a later round. After
                # that it is gone, or private again, and its numbers are no longer read.
                elif moment - (project.youtube_publish_at or moment) >= PUBLISHING_GRACE:
                    project.youtube_removed_at = moment
                    project.updated_at = moment
                    removed += 1
                    if slot is not None:
                        slot.status = "missed"
                        slot.note = NOT_PUBLIC
                        slot.updated_at = moment
                continue
            if slot is not None:
                slot.status = "published"
                slot.updated_at = moment
                published += 1
            assert video is not None
            counts = counts_of(video)
            for period in due:
                row = stored.get((video_id, period))
                if row is None:
                    row = VideoShortsMetric(
                        project_slug=project.slug,
                        youtube_video_id=video_id,
                        period=period,
                        source=SOURCE,
                    )
                    session.add(row)
                    stored[(video_id, period)] = row
                row.captured_at = moment
                row.views = counts["views"]
                row.likes = counts["likes"]
                row.comments = counts["comments"]
                row.raw = as_dict(video.get("statistics"))
                row.updated_at = moment
                snapshots += 1
    return Read(snapshots=snapshots, published=published, removed=removed, moved=moved, calls=calls)
