"""A dropped brand story made again (docs/videos/STORY.md): the owner's ``/redo`` puts a story
whose video was dropped back to ready under a new video slug, once.

The routes run against the in-memory SQLite database of test_video_story.py, as in
test_video_story_admin.py, and the video is dropped the way the owner drops it on
/admin/videos (``drop_project``), so the episode, its request row and the project are what the
real drop leaves. What is asserted: the remake's slug and what the dropped video keeps, the
worker starting the remake through the checks every start makes, the day's and the month's
counts that still see the dropped start, the limit, and the stories and series that are
refused.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models import User, VideoProject, VideoToolToken
from app.video_automation import series as service
from app.video_automation import settings as settings_service
from app.video_automation.models import VideoDramaEpisode, VideoDramaRequest
from app.video_reviews import admin_service as reviews
from app.video_reviews.schemas import DropIn
from app.video_reviews.storage import ReviewStore
from tests.test_video_story import _episode, _file, _series
from tests.test_video_story import db as story_db
from tests.test_video_story_admin import BASE, IMPORT, _audits, _client, _episodes, _user

db = story_db

REDO = f"{BASE}/stories-test/episodes/{{number}}/redo"
NOON = datetime(2026, 10, 1, 4, 0, tzinfo=UTC)  # noon in Taipei
MIDNIGHT = datetime(2026, 10, 1, 16, 0, tzinfo=UTC)  # the next day begins in Taipei


@pytest.fixture
def clock(monkeypatch: pytest.MonkeyPatch) -> Iterator[dict[str, datetime]]:
    moment = {"now": NOON}
    monkeypatch.setattr(service, "_now", lambda: moment["now"])
    yield moment


async def _token(factory: async_sessionmaker[AsyncSession]) -> VideoToolToken:
    token = VideoToolToken(name="story-redo", token_hash=uuid4().hex, token_prefix="mkv_r")
    async with factory() as session:
        session.add(token)
        await session.commit()
    return token


async def _start_and_drop(
    factory: async_sessionmaker[AsyncSession],
    token: VideoToolToken,
    owner: User,
    tmp_path: Path,
    number: int,
    video_slug: str,
) -> None:
    """The worker starts the story under ``video_slug`` and files its project; the owner drops
    that video on /admin/videos."""
    async with factory() as session:
        await service.start_episode(session, token, "stories-test", number, video_slug)
        session.add(
            VideoProject(
                slug=video_slug,
                title=video_slug,
                stage="outline",
                checklist=[],
                format="drama",
                series_slug="stories-test",
                episode_number=number,
            )
        )
        await session.commit()
    store = ReviewStore(tmp_path, max_file_bytes=1_000_000, max_total_bytes=1_000_000)
    async with factory() as session:
        await reviews.drop_project(session, store, video_slug, owner, DropIn(note="畫面不行"))


async def _episode_row(factory: async_sessionmaker[AsyncSession], number: int) -> VideoDramaEpisode:
    async with factory() as session:
        row = await session.scalar(
            select(VideoDramaEpisode).where(VideoDramaEpisode.number == number)
        )
        assert row is not None
        return row


async def _requests(factory: async_sessionmaker[AsyncSession]) -> list[tuple[str | None, str]]:
    async with factory() as session:
        found = await session.scalars(
            select(VideoDramaRequest).order_by(VideoDramaRequest.created_at)
        )
        return [(row.slug, row.status) for row in found.all()]


def test_the_remake_slug_is_the_planned_one_and_a_number() -> None:
    assert service.redo_slug("story-rolling-case", 1) == "story-rolling-case-redo1"
    assert service.is_redo_of("story-rolling-case-redo1", "story-rolling-case")
    assert service.is_redo_of("story-rolling-case-redo12", "story-rolling-case")
    for other in (
        "story-rolling-case",
        "story-rolling-case-redo0",
        "story-rolling-case-redo",
        "story-rolling-case-redox",
        "story-rolling-cases-redo1",
        None,
    ):
        assert not service.is_redo_of(other, "story-rolling-case"), other
    # The longest planned slug (60 characters) and its remake still fit the video slug.
    longest = "story-" + "a" * 54
    assert len(service.redo_slug(longest, service.STORY_REDO_LIMIT)) <= 80


async def test_a_dropped_story_is_made_again_under_a_new_slug_and_the_old_video_stays(
    db: async_sessionmaker[AsyncSession], clock: dict[str, datetime], tmp_path: Path
) -> None:
    owner = await _user(db, "owner")
    token = await _token(db)
    async with _client(db, owner) as client:
        imported = await client.post(IMPORT, json={"file": _file(), "apply": True})
        assert imported.status_code == 200
    await _start_and_drop(db, token, owner, tmp_path, 1, "story-rolling-case")
    dropped = await _episode_row(db, 1)
    assert (dropped.status, dropped.started_at) == ("skipped", NOON)
    assert await _requests(db) == [("story-rolling-case", "cancelled")]

    async with _client(db, owner) as client:
        redone = await client.post(REDO.format(number=1))
    assert redone.status_code == 200, redone.text
    body = redone.json()
    first = body["episodes"][0]
    assert (first["number"], first["status"], first["slug"]) == (
        1,
        "ready",
        "story-rolling-case-redo1",
    )
    # The dropped start still counts for its day and its month.
    quota = body["quota"]
    assert (quota["ready"], quota["started_today"], quota["started_this_month"]) == (3, 1, 1)
    row = await _episode_row(db, 1)
    assert (row.request_id, row.started_at) == (None, None)
    # The dropped video keeps its project, its request row and its slug.
    async with db() as session:
        project = await session.scalar(
            select(VideoProject).where(VideoProject.slug == "story-rolling-case")
        )
        assert project is not None and project.dropped_at is not None
    assert await _requests(db) == [("story-rolling-case", "cancelled")]
    [record] = await _audits(db, "video_series_episode_redone")
    assert (record.actor_user_id, record.target) == (owner.id, "video-series:stories-test")
    assert record.metadata_json == {
        "number": 1,
        "story": "A01",
        "redo": 1,
        "limit": service.STORY_REDO_LIMIT,
        "dropped_video": "story-rolling-case",
        "video": "story-rolling-case-redo1",
        "reopened": False,
    }

    # Importing the backlog again leaves the remake's slug alone.
    async with _client(db, owner) as client:
        again = await client.post(IMPORT, json={"file": _file(), "apply": True})
    assert again.status_code == 200, again.text
    assert again.json()["written"] is False
    assert (await _episode_row(db, 1)).slug == "story-rolling-case-redo1"

    # The worker is handed the remake first and starts it under the new slug only.
    async with db() as session:
        settings = await settings_service.settings_row(session)
        job = (await service.next_job(session, settings)).job
        assert job is not None and job.episode is not None
        assert (job.episode.number, job.episode.slug) == (1, "story-rolling-case-redo1")
        with pytest.raises(service.SeriesRefused) as planned:
            await service.start_episode(session, token, "stories-test", 1, "story-rolling-case")
        assert planned.value.code == "video_series_story_slug"
    async with db() as session:
        started = await service.start_episode(
            session, token, "stories-test", 1, "story-rolling-case-redo1"
        )
        assert (started.episode.status, started.episode.started_at) == ("started", NOON)
    assert await _requests(db) == [
        ("story-rolling-case", "cancelled"),
        ("story-rolling-case-redo1", "started"),
    ]
    async with db() as session:
        view = await service.series_view(session, "stories-test")
        assert view.quota is not None
        assert (view.quota.started_today, view.quota.started_this_month) == (2, 2)
        assert view.quota.in_flight == 1


async def test_a_remade_story_waits_for_the_days_count_its_dropped_start_used(
    db: async_sessionmaker[AsyncSession], clock: dict[str, datetime], tmp_path: Path
) -> None:
    owner = await _user(db, "owner")
    token = await _token(db)
    async with _client(db, owner) as client:
        await client.post(IMPORT, json={"file": _file(), "apply": True, "episodes_per_day": 1})
    await _start_and_drop(db, token, owner, tmp_path, 1, "story-rolling-case")
    async with _client(db, owner) as client:
        redone = await client.post(REDO.format(number=1))
    assert redone.status_code == 200, redone.text
    assert redone.json()["quota"]["hold"] == "per_day", "today's one was the dropped video"
    async with db() as session:
        settings = await settings_service.settings_row(session)
        assert (await service.next_job(session, settings)).job is None
        with pytest.raises(service.SeriesRefused) as held:
            await service.start_episode(
                session, token, "stories-test", 1, "story-rolling-case-redo1"
            )
        assert held.value.code == "video_series_story_held"
    clock["now"] = MIDNIGHT
    async with db() as session:
        settings = await settings_service.settings_row(session)
        job = (await service.next_job(session, settings)).job
        assert job is not None and job.episode is not None
        assert (job.episode.number, job.episode.slug) == (1, "story-rolling-case-redo1")


async def test_a_story_is_redone_at_most_the_limit(
    db: async_sessionmaker[AsyncSession],
    clock: dict[str, datetime],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner = await _user(db, "owner")
    token = await _token(db)
    async with _client(db, owner) as client:
        await client.post(IMPORT, json={"file": _file(), "apply": True})
    await _start_and_drop(db, token, owner, tmp_path, 1, "story-rolling-case")
    async with _client(db, owner) as client:
        assert (await client.post(REDO.format(number=1))).status_code == 200
    await _start_and_drop(db, token, owner, tmp_path, 1, "story-rolling-case-redo1")
    assert (await _episode_row(db, 1)).status == "skipped"

    async with _client(db, owner) as client:
        refused = await client.post(REDO.format(number=1))
    assert refused.status_code == 409
    assert refused.json()["code"] == "video_series_redo_limit"
    assert f"最多重做 {service.STORY_REDO_LIMIT} 次" in refused.json()["detail"]
    row = await _episode_row(db, 1)
    assert (row.status, row.slug) == ("skipped", "story-rolling-case-redo1")
    assert len(await _audits(db, "video_series_episode_redone")) == 1

    # The limit is the constant: one more allowed, and the next remake counts from the plan.
    monkeypatch.setattr(service, "STORY_REDO_LIMIT", service.STORY_REDO_LIMIT + 1)
    async with _client(db, owner) as client:
        again = await client.post(REDO.format(number=1))
    assert again.status_code == 200, again.text
    assert again.json()["episodes"][0]["slug"] == "story-rolling-case-redo2"
    # Both dropped videos still count for today.
    assert again.json()["quota"]["started_today"] == 2


async def test_only_a_story_whose_video_was_dropped_is_redone(
    db: async_sessionmaker[AsyncSession], clock: dict[str, datetime], tmp_path: Path
) -> None:
    owner = await _user(db, "owner")
    viewer = await _user(db, "viewer")
    token = await _token(db)
    async with _client(db, owner) as client:
        await client.post(IMPORT, json={"file": _file(), "apply": True})
        # Story 2 was skipped before it ever started: restoring is its way back.
        await client.post(f"{BASE}/stories-test/episodes/2/skip")
    async with db() as session:
        await service.start_episode(session, token, "stories-test", 3, "story-first-mouse")
    before = await _episodes(db)

    async with _client(db, viewer) as client:
        forbidden = await client.post(REDO.format(number=2))
    async with _client(db, owner) as client:
        ready = await client.post(REDO.format(number=1))
        never_started = await client.post(REDO.format(number=2))
        in_the_making = await client.post(REDO.format(number=3))
        missing = await client.post(REDO.format(number=9))
        nowhere = await client.post(f"{BASE}/no-such-series/episodes/1/redo")
    assert forbidden.status_code == 403
    for refused in (ready, never_started, in_the_making):
        assert refused.status_code == 409, refused.text
        assert refused.json()["code"] == "video_series_episode_not_dropped"
    assert "恢復" in never_started.json()["detail"]
    assert "恢復" not in ready.json()["detail"]
    assert missing.status_code == 404 and nowhere.status_code == 404
    assert await _episodes(db) == before, "nothing changed"
    assert await _audits(db, "video_series_episode_redone") == []

    # A remake's slug somebody already has is refused, not silently renamed.
    await _start_and_drop(db, token, owner, tmp_path, 1, "story-rolling-case")
    async with db() as session:
        session.add(
            VideoProject(
                slug="story-rolling-case-redo1",
                title="another",
                stage="outline",
                checklist=[],
                format="drama",
            )
        )
        await session.commit()
    async with _client(db, owner) as client:
        taken = await client.post(REDO.format(number=1))
    assert taken.status_code == 409 and taken.json()["code"] == "video_series_redo_slug_taken"
    assert (await _episode_row(db, 1)).status == "skipped"


async def test_the_last_story_remade_brings_a_finished_series_back(
    db: async_sessionmaker[AsyncSession], clock: dict[str, datetime], tmp_path: Path
) -> None:
    owner = await _user(db, "owner")
    token = await _token(db)
    async with _client(db, owner) as client:
        await client.post(IMPORT, json={"file": _file(), "apply": True})
        for number in (2, 3):
            await client.post(f"{BASE}/stories-test/episodes/{number}/skip")
    await _start_and_drop(db, token, owner, tmp_path, 1, "story-rolling-case")
    async with db() as session:
        assert (await service.series_view(session, "stories-test")).status == "finished"
    async with _client(db, owner) as client:
        redone = await client.post(REDO.format(number=1))
    assert redone.status_code == 200 and redone.json()["status"] == "active"
    [record] = await _audits(db, "video_series_episode_redone")
    assert record.metadata_json["reopened"] is True


@pytest.mark.parametrize("kind", ["series", "one-off"])
async def test_the_other_kinds_of_series_are_refused(
    db: async_sessionmaker[AsyncSession], kind: str
) -> None:
    owner = await _user(db, "owner")
    slug = "xianxia" if kind == "series" else "one-off-1a2b3c4d"
    async with db() as session:
        series = _series(
            slug=slug,
            kind=kind,
            hands_off=False,
            visual_tier="clips",
            target_minutes=3,
            planned_episodes=1 if kind == "one-off" else 100,
            episodes_per_chapter=1 if kind == "one-off" else 10,
            look=None,
            image_model=None,
        )
        session.add(series)
        await session.flush()
        # An episode whose video was dropped: started, then skipped.
        episode = _episode(1, "skipped", started_at=NOON)
        episode.series_id = series.id
        episode.slug = f"{slug}-1"
        session.add(episode)
        await session.commit()
    before = await _episodes(db)
    async with _client(db, owner) as client:
        refused = await client.post(f"{BASE}/{slug}/episodes/1/redo")
    assert refused.status_code == 409
    assert refused.json()["code"] == "video_series_redo_story_only"
    assert await _episodes(db) == before
    async with db() as session:
        assert await session.scalar(select(func.count()).select_from(VideoDramaRequest)) == 0
    assert await _audits(db, "video_series_episode_redone") == []
