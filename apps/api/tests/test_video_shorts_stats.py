"""The numbers YouTube reports for a public Short, and the day's quota they are read within
(docs/videos/SHORTS.md §成效與每週報告).

The reads go against ``ShortsGoogle`` on the site of test_video_shorts_publish.py. The windows
are counted from the moment a Short went public, so the tests place that moment hours or days
before now and read with the clock they pass.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError
from sqlalchemy import select

from app.models import VideoProject
from app.video_shorts import stats
from app.video_shorts.models import VideoShortsMetric, VideoShortsSlot
from app.video_shorts.quota import COSTS, DAILY_UNITS, READING_STOPS_AT, Quota, pacific_day
from app.video_youtube import connection
from app.video_youtube.client import YoutubeClient
from tests.test_video_shorts_publish import (
    HOURS,
    VIDEO,
    ShortsSite,
    finished,
    open_shorts_site,
    project_of,
    slot,
    slot_of,
)

DAYS = timedelta(days=1)
PUBLIC = datetime(2026, 10, 5, 11, 30, tzinfo=UTC)


@pytest.fixture
async def site(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> AsyncIterator[ShortsSite]:
    async with open_shorts_site(monkeypatch, tmp_path) as value:
        await value.link()
        yield value


@pytest.fixture
def now() -> datetime:
    return datetime.now(UTC).replace(microsecond=0)


# --- when a snapshot is due ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("age", "windows"),
    [
        (timedelta(0), []),
        (24 * HOURS - timedelta(seconds=1), []),
        (24 * HOURS, ["d1"]),
        (48 * HOURS - timedelta(seconds=1), ["d1"]),
        (48 * HOURS, []),
        (72 * HOURS, ["d3"]),
        (96 * HOURS - timedelta(seconds=1), ["d3"]),
        (96 * HOURS, []),
        (7 * DAYS, ["d7"]),
        (9 * DAYS - timedelta(seconds=1), ["d7"]),
        (9 * DAYS, []),
    ],
)
def test_the_windows_open_and_close_as_the_pilot_set_them(
    age: timedelta, windows: list[str]
) -> None:
    assert stats.due_periods(PUBLIC, PUBLIC + age, {}) == [*windows, "now"]


def test_a_window_is_read_once_and_the_latest_once_a_day() -> None:
    at = PUBLIC + 30 * HOURS
    assert stats.due_periods(PUBLIC, at, {"d1": at - HOURS}) == ["now"]
    assert stats.due_periods(PUBLIC, at, {"d1": at - HOURS, "now": at - 23 * HOURS}) == []
    assert stats.due_periods(PUBLIC, at, {"now": at - 23 * HOURS}) == ["d1"]
    assert stats.due_periods(PUBLIC, at, {"d1": at - HOURS, "now": at - 24 * HOURS}) == ["now"]
    assert stats.due_periods(PUBLIC, PUBLIC - timedelta(seconds=1), {}) == [], "not public yet"


def test_an_old_short_is_still_read_within_the_thirty_days_the_policies_give() -> None:
    old = PUBLIC + 121 * DAYS
    assert stats.due_periods(PUBLIC, old, {"now": old - 24 * DAYS}) == []
    assert stats.due_periods(PUBLIC, old, {"now": old - 25 * DAYS}) == ["now"]
    young = PUBLIC + 119 * DAYS
    assert stats.due_periods(PUBLIC, young, {"now": young - DAYS}) == ["now"]
    assert stats.RESTING_EVERY < timedelta(days=30)


def test_a_count_youtube_left_out_is_empty_and_not_zero() -> None:
    assert stats.counts_of(
        {"statistics": {"viewCount": "1204", "likeCount": "0", "commentCount": "7"}}
    ) == {"views": 1204, "likes": 0, "comments": 7}
    # The owner hid the likes and turned the comments off.
    assert stats.counts_of({"statistics": {"viewCount": "12"}}) == {
        "views": 12,
        "likes": None,
        "comments": None,
    }
    assert stats.counts_of({"statistics": {"viewCount": 12, "likeCount": "many"}}) == {
        "views": 12,
        "likes": None,
        "comments": None,
    }
    assert stats.counts_of({}) == {"views": None, "likes": None, "comments": None}


# --- through the database -----------------------------------------------------------------------


async def public_short(
    site: ShortsSite,
    slug: str,
    video_id: str,
    published: datetime,
    *,
    line: str | None = "lab",
    privacy: str = "public",
    **fields: Any,
) -> None:
    """A video the site scheduled for ``published``, and what YouTube says of it now."""
    project = VideoProject(
        id=uuid4(),
        slug=slug,
        title=f"Short {slug}",
        format="shorts" if line else "slides",
        shorts_line=line,
        stage="done",
        checklist=[],
        last_synced_at=published,
        youtube_video_id=video_id,
        youtube_publish_at=published,
        youtube_sync=finished(published),
        **fields,
    )
    async with site.factory() as session:
        session.add(project)
        await session.commit()
    site.youtube.put(
        video_id,
        status={"privacyStatus": privacy},
        statistics={"viewCount": "120", "likeCount": "9", "commentCount": "2"},
    )


async def read(site: ShortsSite, now: datetime) -> stats.Read:
    async with site.factory() as session, connection.http_client() as http:
        client = YoutubeClient(http, await connection.access_token(session, http))
        result = await stats.read_due(session, client, Quota(site.redis, now), now)
        await session.commit()
    return result


async def snapshots(site: ShortsSite, video_id: str = VIDEO) -> dict[str, VideoShortsMetric]:
    async with site.factory() as session:
        rows = await session.scalars(
            select(VideoShortsMetric).where(VideoShortsMetric.youtube_video_id == video_id)
        )
        return {row.period: row for row in rows}


def views(site: ShortsSite, count: int, video_id: str = VIDEO) -> None:
    site.google.videos[video_id]["statistics"]["viewCount"] = str(count)


async def test_a_window_keeps_its_first_read_and_the_latest_follows_the_day(
    site: ShortsSite, now: datetime
) -> None:
    await public_short(site, "receipt", VIDEO, now - 25 * HOURS)

    assert await read(site, now) == stats.Read(snapshots=2, calls=1)

    kept = await snapshots(site)
    assert sorted(kept) == ["d1", "now"]
    first = kept["d1"]
    assert (first.views, first.likes, first.comments) == (120, 9, 2)
    assert (first.project_slug, first.source, first.captured_at) == ("receipt", "data_api", now)
    assert first.raw == {"viewCount": "120", "likeCount": "9", "commentCount": "2"}
    assert site.youtube.asked == [[VIDEO]]
    assert "videos.list" in site.google.calls and site.google.updates == []

    views(site, 150)
    assert await read(site, now + HOURS) == stats.Read(), "nothing is due: nothing is asked"
    assert site.youtube.asked == [[VIDEO]]

    # A day later the first window has closed and the third day's has not opened.
    assert await read(site, now + 24 * HOURS) == stats.Read(snapshots=1, calls=1)
    kept = await snapshots(site)
    assert sorted(kept) == ["d1", "now"]
    assert (kept["d1"].views, kept["d1"].captured_at) == (120, now), "never overwritten"
    assert (kept["now"].views, kept["now"].captured_at) == (150, now + 24 * HOURS)

    views(site, 400)
    assert await read(site, now + 48 * HOURS) == stats.Read(snapshots=2, calls=1)
    views(site, 900)
    assert await read(site, now + 6 * DAYS) == stats.Read(snapshots=2, calls=1)
    kept = await snapshots(site)
    assert {period: row.views for period, row in kept.items()} == {
        "d1": 120,
        "d3": 400,
        "d7": 900,
        "now": 900,
    }
    assert await Quota(site.redis, now + 6 * DAYS).spent() == 1, "a unit a read, on its own day"


async def test_a_window_nobody_read_in_stays_empty(site: ShortsSite, now: datetime) -> None:
    await public_short(site, "receipt", VIDEO, now - 50 * HOURS)
    assert await read(site, now) == stats.Read(snapshots=1, calls=1)
    assert sorted(await snapshots(site)) == ["now"], "day 1 is not filled with a later number"


async def test_the_numbers_are_kept_as_they_came_and_nothing_is_made_of_them(
    site: ShortsSite, now: datetime
) -> None:
    await public_short(site, "receipt", VIDEO, now - 25 * HOURS)
    site.google.videos[VIDEO]["statistics"] = {"viewCount": "0", "favoriteCount": "0"}
    await read(site, now)
    row = (await snapshots(site))["d1"]
    assert (row.views, row.likes, row.comments) == (0, None, None)
    assert row.raw == {"viewCount": "0", "favoriteCount": "0"}
    derived = (
        row.engaged_views,
        row.shares,
        row.subscribers_gained,
        row.avg_view_seconds,
        row.avg_view_percent,
        row.stayed_percent,
        row.range_start,
        row.range_end,
    )
    assert derived == (None,) * 8, "the Data API gives none of these, and the site makes none up"


async def test_a_slot_is_marked_once_youtube_made_its_short_public(
    site: ShortsSite, now: datetime
) -> None:
    at = now - timedelta(minutes=10)
    await public_short(site, "receipt", VIDEO, at, privacy="private")
    slot_id = await slot(site, at, "receipt", "scheduled")

    assert await read(site, now) == stats.Read(calls=1), "a little late is not gone"
    assert (await slot_of(site, slot_id)).status == "scheduled"
    assert await snapshots(site) == {}
    assert (await project_of(site)).youtube_removed_at is None

    site.google.videos[VIDEO]["status"]["privacyStatus"] = "public"
    later = now + timedelta(minutes=5)
    assert await read(site, later) == stats.Read(snapshots=1, published=1, calls=1)
    assert (await slot_of(site, slot_id)).status == "published"
    assert sorted(await snapshots(site)) == ["now"]
    assert await read(site, later + timedelta(minutes=5)) == stats.Read()


@pytest.mark.parametrize("gone", ["deleted", "private"])
async def test_a_video_that_is_gone_or_private_again_is_taken_off_the_lists(
    site: ShortsSite, now: datetime, gone: str
) -> None:
    at = now - 3 * DAYS
    await public_short(site, "receipt", VIDEO, at)
    await read(site, at + 25 * HOURS)
    slot_id = await slot(site, at, "receipt", "published")
    fresh = await slot(site, now - 3 * HOURS, "invoice", "scheduled")
    await public_short(site, "invoice", "ShortVid002", now - 3 * HOURS)
    if gone == "deleted":
        del site.google.videos[VIDEO]
        del site.google.videos["ShortVid002"]
    else:
        site.google.videos[VIDEO]["status"] = {"privacyStatus": "private"}
        site.google.videos["ShortVid002"]["status"] = {"privacyStatus": "private"}

    assert await read(site, now) == stats.Read(removed=2, calls=1)

    assert (await project_of(site)).youtube_removed_at == now
    assert (await project_of(site, "invoice")).youtube_removed_at == now
    assert (await slot_of(site, slot_id)).status == "published", "what happened stays"
    never = await slot_of(site, fresh)
    assert (never.status, never.note) == ("missed", stats.NOT_PUBLIC)
    assert sorted(await snapshots(site)) == ["d1", "now"], "what was read is kept"
    assert await read(site, now + DAYS) == stats.Read(), "and it is not asked about again"


async def test_a_time_the_owner_changed_in_studio_is_followed(
    site: ShortsSite, now: datetime
) -> None:
    at = now - 3 * HOURS
    later = now + 3 * HOURS
    await public_short(site, "receipt", VIDEO, at, privacy="private")
    site.google.videos[VIDEO]["status"]["publishAt"] = later.strftime("%Y-%m-%dT%H:%M:%SZ")
    slot_id = await slot(site, at, "receipt", "scheduled")

    assert await read(site, now) == stats.Read(moved=1, calls=1)

    project = await project_of(site)
    assert (project.youtube_publish_at, project.youtube_removed_at) == (later, None)
    held = await slot_of(site, slot_id)
    assert held.status == "scheduled" and "Studio" in str(held.note)
    assert await read(site, now + HOURS) == stats.Read(), "it is not public before its time"
    site.google.videos[VIDEO]["status"] = {"privacyStatus": "public"}
    after = later + timedelta(minutes=5)
    assert await read(site, after) == stats.Read(snapshots=1, published=1, calls=1)
    assert (await slot_of(site, slot_id)).status == "published"


async def test_only_shorts_that_are_public_are_asked_about(site: ShortsSite, now: datetime) -> None:
    await public_short(site, "tutorial", "LongVideo01", now - 25 * HOURS, line=None)
    await public_short(site, "ahead", "ShortVid002", now + 3 * HOURS, privacy="private")
    await public_short(site, "dropped", "ShortVid003", now - 25 * HOURS, dropped_at=now)
    await public_short(site, "removed", "ShortVid004", now - 25 * HOURS, youtube_removed_at=now)
    assert await read(site, now) == stats.Read()
    assert site.youtube.asked == []
    assert await Quota(site.redis, now).spent() == 0


async def test_the_videos_are_asked_about_fifty_at_a_time(site: ShortsSite, now: datetime) -> None:
    for index in range(120):
        await public_short(site, f"short-{index:03d}", f"Vid{index:08d}", now - 25 * HOURS)
    assert await read(site, now) == stats.Read(snapshots=240, calls=3)
    assert [len(ids) for ids in site.youtube.asked] == [50, 50, 20]
    assert len({video_id for ids in site.youtube.asked for video_id in ids}) == 120
    assert await Quota(site.redis, now).spent() == 3
    async with site.factory() as session:
        rows = list(await session.scalars(select(VideoShortsMetric)))
    assert len(rows) == 240 and {row.period for row in rows} == {"d1", "now"}


async def test_a_slot_of_another_status_is_left_as_it_is(site: ShortsSite, now: datetime) -> None:
    await public_short(site, "receipt", VIDEO, now - 25 * HOURS)
    held: list[UUID] = [
        await slot(site, now - 25 * HOURS, "receipt", "missed"),
        await slot(site, now + 20 * HOURS, None, "open"),
    ]
    assert await read(site, now) == stats.Read(snapshots=2, calls=1)
    async with site.factory() as session:
        rows = [await session.get(VideoShortsSlot, each) for each in held]
    assert [row.status for row in rows if row is not None] == ["missed", "open"]


# --- the day's quota ----------------------------------------------------------------------------


def test_the_quota_s_day_turns_at_midnight_in_california() -> None:
    assert pacific_day(datetime(2026, 10, 5, 6, 59, tzinfo=UTC)) == "2026-10-04"
    assert pacific_day(datetime(2026, 10, 5, 7, 0, tzinfo=UTC)) == "2026-10-05"
    # Winter time is an hour further from UTC.
    assert pacific_day(datetime(2026, 12, 1, 7, 59, tzinfo=UTC)) == "2026-11-30"
    assert pacific_day(datetime(2026, 12, 1, 8, 0, tzinfo=UTC)) == "2026-12-01"
    assert (DAILY_UNITS, READING_STOPS_AT) == (10_000, 8_000), "four fifths"


async def test_the_units_are_counted_by_the_day_and_reading_stops_first(
    site: ShortsSite,
) -> None:
    today = datetime(2026, 10, 5, 12, 0, tzinfo=UTC)
    quota = Quota(site.redis, today)
    assert await quota.spent() == 0
    await quota.add("sync")
    await quota.add("videos.list", 3)
    await quota.add("videos.update", 0)
    assert await quota.spent() == 501 + 3
    assert COSTS["sync"] == 1 + 50 + 50 + 400, "a read, the details, the tracks, one track"
    assert 0 < await site.redis.ttl(quota.units_key) <= 60 * 60 * 50
    assert await Quota(site.redis, today + 19 * HOURS).spent() == 0, "07:00 UTC: a new day"
    assert await Quota(site.redis, today + 18 * HOURS).spent() == 504

    await site.redis.set(quota.units_key, READING_STOPS_AT - 1)
    assert await quota.allows_reading() and await quota.allows_sending()
    await quota.add("videos.list")
    assert not await quota.allows_reading()
    assert await quota.allows_sending(), "the units are for sending Shorts"

    await quota.mark_refused()
    assert await quota.refused()
    assert not await quota.allows_sending() and not await quota.allows_reading()
    tomorrow = Quota(site.redis, today + DAYS)
    assert await tomorrow.allows_sending() and await tomorrow.allows_reading()


async def test_without_redis_nothing_is_counted_and_nothing_is_stopped() -> None:
    class Down:
        def __getattr__(self, _name: str) -> Any:
            async def refuse(*_args: Any, **_kwargs: Any) -> Any:
                raise RedisConnectionError("down")

            return refuse

    quota = Quota(Down(), PUBLIC)  # type: ignore[arg-type]
    await quota.add("sync")
    await quota.mark_refused()
    assert await quota.spent() == 0
    assert not await quota.refused()
    assert await quota.allows_sending() and await quota.allows_reading()
