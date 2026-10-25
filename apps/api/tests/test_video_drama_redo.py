"""An episode of a drama series made again (docs/videos/BINGE.md §重做一集): the owner's
``/redo`` drops the episode's video, puts the episode back to ready under a new video slug,
and the worker remakes it from the chapter outline.

The routes run against the in-memory SQLite database of test_video_story.py, with the review
area of a temporary directory. The series is a hands-off compilation series like 《系統說我是
BUG》, whose first episodes the owner wanted made again under the rules of 2026-10-24. What is
asserted: a cleared and an in-the-making video are dropped the way the owner drops them and
the episode is ready under ``-redo1``; an already dropped video is not dropped twice; the worker
starts the remake under the episode's slug although it names the planned one; the limit; the
compilation lists each episode's current video and never a dropped one; and the episodes and
the series that are refused. A one-off (a 奇聞檔案局 explainer the owner's form filed, cleared
for upload before the rules of 2026-10-25) is remade the same way from its approved story
bible, and the remake travels as a new request row that repeats the owner's form.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models import VideoProject, VideoToolToken
from app.video_automation import admin_api
from app.video_automation import series as service
from app.video_automation import settings as settings_service
from app.video_automation.anime_policy import LONG_ANIME_POLICY
from app.video_automation.models import VideoDramaDoc, VideoDramaRequest, VideoDramaSeries
from app.video_reviews import admin_service as reviews
from app.video_reviews.schemas import DropIn
from app.video_reviews.storage import ReviewStore
from tests.test_video_series import _doc
from tests.test_video_story import _episode, _series
from tests.test_video_story import db as story_db
from tests.test_video_story_admin import BASE, _audits, _client, _user
from tests.test_video_story_redo import NOON, _episode_row, _requests, _token
from tests.test_video_story_redo import clock as redo_clock

db = story_db
clock = redo_clock

SLUG = "bug-story"
REDO = f"{BASE}/{SLUG}/episodes/{{number}}/redo"
PLANNED = f"{SLUG}-e001"
REMADE = f"{SLUG}-e001-redo1"
# The one-off the owner's form filed (create_one_off): the series slug is the request's id.
ONE_OFF = "one-off-1a2b3c4d"
ONE_OFF_PLANNED = f"{ONE_OFF}-e001"
ONE_OFF_REMADE = f"{ONE_OFF}-e001-redo1"
ONE_OFF_FORM = {
    "premise": "1923 年資助挖掘的卡納文伯爵死了，報紙說是法老的詛咒；2002 年一位醫師把進過墓室的人的壽命算了一遍。",
    "title": "H24 圖坦卡門的詛咒",
    "source_guide": "tutankhamun-curse",
    "note": "只講紀錄與數字，不評論信仰",
}


@pytest.fixture
def store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> ReviewStore:
    """The review area the route drops a live video's previews from."""
    store = ReviewStore(tmp_path, max_file_bytes=1_000_000, max_total_bytes=1_000_000)

    async def give(session: AsyncSession) -> ReviewStore:
        return store

    monkeypatch.setattr(admin_api, "_review_store", give)
    return store


async def _drama(
    factory: async_sessionmaker[AsyncSession], planned: int = 2, **changes: Any
) -> VideoDramaSeries:
    """A production drama series whose first chapter is approved: every episode is ready."""
    values: dict[str, Any] = {
        "slug": SLUG,
        "kind": "series",
        "title": "系統說我是 BUG",
        "hands_off": True,
        "compilation": True,
        "visual_tier": "manga",
        "target_minutes": 3,
        "planned_episodes": planned,
        "episodes_per_chapter": planned,
        "look": None,
        "image_model": None,
    }
    values.update(changes)
    series = _series(**values)
    async with factory() as session:
        session.add(series)
        await session.flush()
        for doc in (_doc("setting"), _doc("outline"), _doc("chapter", 1)):
            doc.series_id = series.id
            session.add(doc)
        for number in range(1, planned + 1):
            episode = _episode(number, "ready")
            episode.series_id = series.id
            episode.title = f"第 {number} 集"
            episode.beats = {"hook": f"鉤子 {number}", "conflict": "衝突"}
            session.add(episode)
        await session.commit()
    return series


async def _one_off(factory: async_sessionmaker[AsyncSession], owner_id: Any) -> VideoDramaSeries:
    """A 奇聞檔案局 one-off as the owner's form filed it (``create_one_off``) once its story
    bible was approved: the series active, its one episode ready, its request row queued."""
    series = _series(
        slug=ONE_OFF,
        kind="one-off",
        title="圖坦卡門的詛咒",
        premise=ONE_OFF_FORM["premise"],
        note=ONE_OFF_FORM["note"],
        style_preset="cute-mystery",
        hands_off=False,
        compilation=False,
        visual_tier="clips",
        target_minutes=10,
        planned_episodes=1,
        episodes_per_chapter=1,
        look=None,
        image_model="image-01",
    )
    async with factory() as session:
        session.add(series)
        await session.flush()
        bible = _doc("bible")
        bible.series_id = series.id
        session.add(bible)
        episode = _episode(1, "ready")
        episode.series_id = series.id
        episode.title = series.title
        session.add(episode)
        session.add(
            VideoDramaRequest(
                id=uuid4(),
                **ONE_OFF_FORM,
                style_preset="cute-mystery",
                target_minutes=10,
                status="queued",
                series_id=series.id,
                episode_number=1,
                created_by_user_id=owner_id,
                created_at=NOON,
                updated_at=NOON,
            )
        )
        await session.commit()
    return series


async def _start(
    factory: async_sessionmaker[AsyncSession],
    token: VideoToolToken,
    number: int,
    video_slug: str,
    *,
    project: bool = True,
    series_slug: str = SLUG,
) -> str:
    """The worker starts the episode under the slug it names and, usually, files its project;
    the slug the site made it under comes back."""
    async with factory() as session:
        started = await service.start_episode(session, token, series_slug, number, video_slug)
        made = str(started.request.slug)
        if project:
            session.add(
                VideoProject(
                    slug=made,
                    title=made,
                    stage="outline",
                    checklist=[],
                    format="drama",
                    series_slug=series_slug,
                    episode_number=number,
                )
            )
            await session.commit()
    return made


async def _finish(
    factory: async_sessionmaker[AsyncSession], number: int, *, series_slug: str = SLUG
) -> None:
    async with factory() as session:
        await service.finish_episode(session, series_slug, number)


async def _project(factory: async_sessionmaker[AsyncSession], slug: str) -> VideoProject:
    async with factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == slug))
        assert project is not None
        return project


async def _status(factory: async_sessionmaker[AsyncSession], series_slug: str = SLUG) -> str:
    async with factory() as session:
        return (await service.series_view(session, series_slug)).status


def test_an_episode_of_a_drama_series_and_a_one_off_may_be_redone_but_not_a_long_anime() -> None:
    drama = _series(kind="series", look=None, image_model=None)
    assert service.can_redo(drama)
    assert service.can_redo(_series(kind="story"))
    assert service.can_redo(_series(kind="one-off", look=None, image_model=None))
    anime = _series(kind="series", production_policy=LONG_ANIME_POLICY, look=None, image_model=None)
    assert not service.can_redo(anime)


async def test_a_cleared_episode_is_dropped_and_made_again_from_the_outline(
    db: async_sessionmaker[AsyncSession],
    clock: dict[str, datetime],
    store: ReviewStore,
) -> None:
    owner = await _user(db, "owner")
    token = await _token(db)
    await _drama(db)
    assert await _start(db, token, 1, PLANNED) == PLANNED
    await _finish(db, 1)
    assert (await _episode_row(db, 1)).status == "done"

    async with _client(db, owner) as client:
        redone = await client.post(REDO.format(number=1))
    assert redone.status_code == 200, redone.text
    first = redone.json()["episodes"][0]
    assert (first["status"], first["slug"], first["started_at"], first["finished_at"]) == (
        "ready",
        REMADE,
        None,
        None,
    )
    row = await _episode_row(db, 1)
    assert (row.request_id, row.started_at, row.finished_at) == (None, None, None)
    # The old video was dropped as the owner drops one, with the redo's note; its request row
    # stays done, since the video was made.
    project = await _project(db, PLANNED)
    assert project.dropped_at is not None
    assert (project.dropped_note, project.dropped_by_user_id) == (service.REDO_DROP_NOTE, owner.id)
    assert await _requests(db) == [(PLANNED, "done")]
    [dropped] = await _audits(db, "video_project_dropped")
    assert dropped.metadata_json == {"slug": PLANNED}
    [record] = await _audits(db, "video_series_episode_redone")
    assert (record.actor_user_id, record.target) == (owner.id, f"video-series:{SLUG}")
    assert record.metadata_json == {
        "number": 1,
        "story": None,
        "redo": 1,
        "limit": service.STORY_REDO_LIMIT,
        "dropped_video": PLANNED,
        "video": REMADE,
        "reopened": False,
    }

    # The worker is handed episode 1 again and names the planned slug, as it always does; the
    # remake is made under the episode's slug, which the request row it drafts from carries.
    async with db() as session:
        settings = await settings_service.settings_row(session)
        job = (await service.next_job(session, settings)).job
        assert job is not None and job.episode is not None
        assert (job.episode.number, job.episode.slug) == (1, REMADE)
        with pytest.raises(service.SeriesRefused) as other:
            await service.start_episode(session, token, SLUG, 1, f"{SLUG}-e002")
        assert other.value.code == "video_series_story_slug"
    assert await _start(db, token, 1, PLANNED) == REMADE
    row = await _episode_row(db, 1)
    assert (row.status, row.slug, row.started_at) == ("started", REMADE, NOON)
    assert await _requests(db) == [(PLANNED, "done"), (REMADE, "started")]
    await _finish(db, 1)
    async with db() as session:
        view = await service.series_view(session, SLUG)
    assert [(e.number, e.status, e.slug) for e in view.episodes] == [
        (1, "done", REMADE),
        (2, "ready", None),
    ]


async def test_an_episode_in_the_making_is_dropped_and_made_again(
    db: async_sessionmaker[AsyncSession],
    clock: dict[str, datetime],
    store: ReviewStore,
) -> None:
    owner = await _user(db, "owner")
    token = await _token(db)
    await _drama(db)
    await _start(db, token, 1, PLANNED)
    async with _client(db, owner) as client:
        redone = await client.post(REDO.format(number=1))
    assert redone.status_code == 200, redone.text
    assert redone.json()["episodes"][0]["slug"] == REMADE
    assert (await _project(db, PLANNED)).dropped_note == service.REDO_DROP_NOTE
    # The drop cancelled the request row the episode travelled as.
    assert await _requests(db) == [(PLANNED, "cancelled")]
    assert len(await _audits(db, "video_project_dropped")) == 1


async def test_an_episode_started_without_a_project_yet_is_made_again_without_a_drop(
    db: async_sessionmaker[AsyncSession],
    clock: dict[str, datetime],
    store: ReviewStore,
) -> None:
    owner = await _user(db, "owner")
    token = await _token(db)
    await _drama(db)
    await _start(db, token, 1, PLANNED, project=False)
    async with _client(db, owner) as client:
        redone = await client.post(REDO.format(number=1))
    assert redone.status_code == 200, redone.text
    assert redone.json()["episodes"][0]["slug"] == REMADE
    assert await _requests(db) == [(PLANNED, "cancelled")]
    assert await _audits(db, "video_project_dropped") == []


async def test_an_episode_whose_video_was_dropped_is_made_again_without_a_second_drop(
    db: async_sessionmaker[AsyncSession],
    clock: dict[str, datetime],
    store: ReviewStore,
) -> None:
    owner = await _user(db, "owner")
    token = await _token(db)
    await _drama(db)
    await _start(db, token, 1, PLANNED)
    async with db() as session:
        await reviews.drop_project(session, store, PLANNED, owner, DropIn(note="畫面不行"))
    assert (await _episode_row(db, 1)).status == "skipped"
    async with _client(db, owner) as client:
        redone = await client.post(REDO.format(number=1))
    assert redone.status_code == 200, redone.text
    assert redone.json()["episodes"][0]["slug"] == REMADE
    assert (await _project(db, PLANNED)).dropped_note == "畫面不行"
    assert len(await _audits(db, "video_project_dropped")) == 1


async def test_an_episode_is_redone_at_most_the_limit(
    db: async_sessionmaker[AsyncSession],
    clock: dict[str, datetime],
    store: ReviewStore,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner = await _user(db, "owner")
    token = await _token(db)
    await _drama(db)
    await _start(db, token, 1, PLANNED)
    await _finish(db, 1)
    async with _client(db, owner) as client:
        assert (await client.post(REDO.format(number=1))).status_code == 200
    assert await _start(db, token, 1, PLANNED) == REMADE
    await _finish(db, 1)

    async with _client(db, owner) as client:
        refused = await client.post(REDO.format(number=1))
    assert refused.status_code == 409
    assert refused.json()["code"] == "video_series_redo_limit"
    row = await _episode_row(db, 1)
    assert (row.status, row.slug) == ("done", REMADE)
    assert (await _project(db, REMADE)).dropped_at is None, "nothing was dropped"
    assert len(await _audits(db, "video_series_episode_redone")) == 1

    monkeypatch.setattr(service, "STORY_REDO_LIMIT", service.STORY_REDO_LIMIT + 1)
    async with _client(db, owner) as client:
        again = await client.post(REDO.format(number=1))
    assert again.status_code == 200, again.text
    assert again.json()["episodes"][0]["slug"] == f"{SLUG}-e001-redo2"
    assert (await _project(db, REMADE)).dropped_note == service.REDO_DROP_NOTE


async def test_the_compilation_takes_each_episode_s_current_video_and_never_a_dropped_one(
    db: async_sessionmaker[AsyncSession],
    clock: dict[str, datetime],
    store: ReviewStore,
) -> None:
    owner = await _user(db, "owner")
    token = await _token(db)
    await _drama(db)
    await _start(db, token, 1, PLANNED)
    await _finish(db, 1)
    await _start(db, token, 2, f"{SLUG}-e002")
    await _finish(db, 2)
    assert await _status(db) == "finished"

    # The last episode made again brings the finished series back; made, it finishes again.
    async with _client(db, owner) as client:
        redone = await client.post(REDO.format(number=1))
    assert redone.status_code == 200 and redone.json()["status"] == "active"
    [record] = await _audits(db, "video_series_episode_redone")
    assert record.metadata_json["reopened"] is True
    assert await _start(db, token, 1, PLANNED) == REMADE
    await _finish(db, 1)
    assert await _status(db) == "finished"
    # Episode 2's video the owner dropped on /admin/videos: the episode stays done, but nothing
    # of it is for upload.
    async with db() as session:
        await reviews.drop_project(session, store, f"{SLUG}-e002", owner, DropIn(note="不要了"))
    assert (await _episode_row(db, 2)).status == "done"

    async with db() as session:
        started = await service.start_compilation(session, token, SLUG, f"{SLUG}-full")
    assert [(e.number, e.slug) for e in started.episodes] == [(1, REMADE)]
    assert started.series.compilation_slug == f"{SLUG}-full"


async def test_only_an_episode_that_was_made_is_redone(
    db: async_sessionmaker[AsyncSession],
    clock: dict[str, datetime],
    store: ReviewStore,
) -> None:
    owner = await _user(db, "owner")
    viewer = await _user(db, "viewer")
    token = await _token(db)
    await _drama(db, planned=3)
    async with _client(db, owner) as client:
        await client.post(f"{BASE}/{SLUG}/episodes/3/skip")
    await _start(db, token, 1, PLANNED)
    async with _client(db, viewer) as client:
        forbidden = await client.post(REDO.format(number=1))
    async with _client(db, owner) as client:
        ready = await client.post(REDO.format(number=2))
        never_started = await client.post(REDO.format(number=3))
        missing = await client.post(REDO.format(number=9))
    assert forbidden.status_code == 403
    for refused in (ready, never_started):
        assert refused.status_code == 409, refused.text
        assert refused.json()["code"] == "video_series_episode_not_dropped"
        assert "還沒做過影片" in refused.json()["detail"]
    assert missing.status_code == 404
    assert await _audits(db, "video_series_episode_redone") == []
    assert (await _project(db, PLANNED)).dropped_at is None

    # Without a review area to drop into, a live video is left to the owner.
    async with db() as session:
        with pytest.raises(service.SeriesRefused) as live:
            await service.redo_episode(session, owner, SLUG, 1)
        assert live.value.code == "video_series_redo_video_live"
    assert (await _project(db, PLANNED)).dropped_at is None


async def test_an_episode_is_not_redone_once_the_compilation_started(
    db: async_sessionmaker[AsyncSession],
    clock: dict[str, datetime],
    store: ReviewStore,
) -> None:
    owner = await _user(db, "owner")
    token = await _token(db)
    await _drama(db, planned=1)
    await _start(db, token, 1, PLANNED)
    await _finish(db, 1)
    async with db() as session:
        await service.start_compilation(session, token, SLUG, f"{SLUG}-full")
    async with _client(db, owner) as client:
        refused = await client.post(REDO.format(number=1))
    assert refused.status_code == 409
    assert refused.json()["code"] == "video_series_compiled"
    assert (await _project(db, PLANNED)).dropped_at is None
    assert (await _episode_row(db, 1)).status == "done"


async def test_a_one_off_cleared_for_upload_is_dropped_and_made_again_from_its_bible(
    db: async_sessionmaker[AsyncSession],
    clock: dict[str, datetime],
    store: ReviewStore,
) -> None:
    owner = await _user(db, "owner")
    token = await _token(db)
    await _one_off(db, owner.id)
    # The one-off travels as the row its form filed (start_episode): started under the slug the
    # worker names, <series>-e001; cleared for upload, it finishes its one-episode series.
    assert await _start(db, token, 1, ONE_OFF_PLANNED, series_slug=ONE_OFF) == ONE_OFF_PLANNED
    assert await _requests(db) == [(ONE_OFF_PLANNED, "started")]
    await _finish(db, 1, series_slug=ONE_OFF)
    assert await _status(db, ONE_OFF) == "finished"

    async with _client(db, owner) as client:
        redone = await client.post(f"{BASE}/{ONE_OFF}/episodes/1/redo")
    assert redone.status_code == 200, redone.text
    body = redone.json()
    assert body["status"] == "active", "the finished one-off is active again"
    first = body["episodes"][0]
    assert (first["status"], first["slug"], first["started_at"], first["finished_at"]) == (
        "ready",
        ONE_OFF_REMADE,
        None,
        None,
    )
    project = await _project(db, ONE_OFF_PLANNED)
    assert (project.dropped_note, project.dropped_by_user_id) == (service.REDO_DROP_NOTE, owner.id)
    # The form's row stays done, since the video was made.
    assert await _requests(db) == [(ONE_OFF_PLANNED, "done")]
    [record] = await _audits(db, "video_series_episode_redone")
    assert (record.metadata_json["video"], record.metadata_json["reopened"]) == (ONE_OFF_REMADE, True)

    # The worker is handed the one-off again (its bible is still approved), names the planned
    # slug, and the remake is made under -redo1 as a new request row that repeats the owner's
    # form; the length and the style are the series' current ones.
    async with db() as session:
        settings = await settings_service.settings_row(session)
        job = (await service.next_job(session, settings)).job
        assert job is not None and job.episode is not None
        assert (job.series.slug, job.episode.number, job.episode.slug) == (ONE_OFF, 1, ONE_OFF_REMADE)
    assert await _start(db, token, 1, ONE_OFF_PLANNED, series_slug=ONE_OFF) == ONE_OFF_REMADE
    async with db() as session:
        remake = await session.scalar(
            select(VideoDramaRequest).where(VideoDramaRequest.slug == ONE_OFF_REMADE)
        )
        assert remake is not None
        assert {key: getattr(remake, key) for key in ONE_OFF_FORM} == ONE_OFF_FORM
        assert (remake.style_preset, remake.target_minutes, remake.status) == (
            "cute-mystery",
            10,
            "started",
        )
        assert (remake.series_id, remake.episode_number) == (job.series.id, 1)
    assert await _requests(db) == [(ONE_OFF_PLANNED, "done"), (ONE_OFF_REMADE, "started")]
    row = await _episode_row(db, 1)
    assert (row.status, row.slug, row.started_at) == ("started", ONE_OFF_REMADE, NOON)
    await _finish(db, 1, series_slug=ONE_OFF)
    assert await _status(db, ONE_OFF) == "finished"

    # Once: the second redo is refused like a story's.
    async with _client(db, owner) as client:
        refused = await client.post(f"{BASE}/{ONE_OFF}/episodes/1/redo")
    assert refused.status_code == 409
    assert refused.json()["code"] == "video_series_redo_limit"
    assert (await _project(db, ONE_OFF_REMADE)).dropped_at is None


async def test_a_one_off_that_never_made_a_video_is_not_redone(
    db: async_sessionmaker[AsyncSession], store: ReviewStore
) -> None:
    owner = await _user(db, "owner")
    await _one_off(db, owner.id)
    async with _client(db, owner) as client:
        refused = await client.post(f"{BASE}/{ONE_OFF}/episodes/1/redo")
    assert refused.status_code == 409
    assert refused.json()["code"] == "video_series_episode_not_dropped"
    assert "這支單集還沒做過影片" in refused.json()["detail"]
    assert await _requests(db) == [(None, "queued")]


async def test_a_long_anime_is_refused(
    db: async_sessionmaker[AsyncSession], store: ReviewStore
) -> None:
    owner = await _user(db, "owner")
    slug = "dawn"
    async with db() as session:
        # A long anime is what its CHECK constraints allow and nothing else (models.py).
        anime: dict[str, Any] = {
            "kind": "series",
            "category": "anime",
            "production_policy": LONG_ANIME_POLICY,
            "runtime_spec": {
                "body_target_seconds": 1320,
                "op_ed_budget_seconds": 180,
                "broadcast_slot_seconds": 1800,
                "slot_reserve_seconds": 300,
            },
            "style_preset": "anime-2d",
            "genre": "custom",
            "lead": "ensemble",
            "target_minutes": 22,
        }
        series = _series(
            slug=slug,
            hands_off=False,
            compilation=False,
            visual_tier="clips",
            planned_episodes=1,
            episodes_per_chapter=1,
            look=None,
            image_model=None,
            **anime,
        )
        session.add(series)
        await session.flush()
        episode = _episode(1, "done", started_at=NOON)
        episode.series_id = series.id
        episode.slug = f"{slug}-e001"
        session.add(episode)
        session.add(
            VideoProject(
                slug=f"{slug}-e001",
                title=slug,
                stage="done",
                checklist=[],
                format="drama",
                series_slug=slug,
                episode_number=1,
            )
        )
        await session.commit()
    async with _client(db, owner) as client:
        refused = await client.post(f"{BASE}/{slug}/episodes/1/redo")
    assert refused.status_code == 409
    assert refused.json()["code"] == "video_series_redo_story_only"
    assert (await _project(db, f"{slug}-e001")).dropped_at is None
    assert (await _episode_row(db, 1)).status == "done"
    assert await _audits(db, "video_series_episode_redone") == []


def test_the_docs_of_the_test_series_authorize_production() -> None:
    """The fixture's documents are what ``start_episode`` checks: all three approved."""
    docs: list[VideoDramaDoc] = [_doc("setting"), _doc("outline"), _doc("chapter", 1)]
    series = _series(
        kind="series", planned_episodes=2, episodes_per_chapter=2, look=None, image_model=None
    )
    assert service.episode_document_problem(series, docs, 1) is None
