"""Deleting a dropped video from /admin/videos (app/video_reviews/deletion.py): what goes, what
stays, what is refused, and that the worker cannot bring the row back while the slug stays free."""

from __future__ import annotations

import hashlib
import os
from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import STEP_UP_COOKIE, create_admin_step_up_token
from app.db import Base, SessionFactory
from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoToolToken
from app.problems import AppError
from app.video_automation import series as series_module
from app.video_automation.models import (
    VideoAiRun,
    VideoDailyBriefRequest,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaMessage,
    VideoDramaRequest,
    VideoDramaSeries,
    VideoSlidesRequest,
)
from app.video_media.models import VideoMediaJob
from app.video_media.storage import MediaStore
from app.video_reviews import admin_api, deletion
from app.video_reviews import admin_service as service
from app.video_reviews.schemas import DropIn, ProjectDeletedOut, ProjectIn, ReviewIn
from app.video_reviews.storage import ReviewStore
from app.video_shorts.models import (
    VideoShortsAsset,
    VideoShortsMetric,
    VideoShortsSlot,
    VideoShortsTopic,
)
from tests.test_video_reviews import _app

SLUG = "story-adapt-dolby-licensing"
YOUTUBE_ID = "uv-CQOKDMOI"
MODELS = (
    User,
    VideoToolToken,
    VideoProject,
    VideoReview,
    AdminAuditLog,
    VideoAiRun,
    VideoDailyBriefRequest,
    VideoDramaSeries,
    VideoDramaDoc,
    VideoDramaMessage,
    VideoDramaRequest,
    VideoDramaEpisode,
    VideoSlidesRequest,
    VideoMediaJob,
    VideoShortsAsset,
    VideoShortsMetric,
    VideoShortsSlot,
    VideoShortsTopic,
)


@dataclass
class Site:
    factory: async_sessionmaker[AsyncSession]
    owner: User
    store: ReviewStore
    media: MediaStore


@pytest.fixture
async def site(tmp_path: Path) -> AsyncIterator[Site]:
    engine = create_async_engine("sqlite+aiosqlite://")

    def restore_utc(target: Any, _context: Any, *_more: Any) -> None:
        for column in target.__table__.columns:
            value = getattr(target, column.name)
            if isinstance(value, datetime) and value.tzinfo is None:
                setattr(target, column.name, value.replace(tzinfo=UTC))

    for model in MODELS:
        event.listen(model, "load", restore_utc)
        event.listen(model, "refresh", restore_utc)
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync: Base.metadata.create_all(
                sync, tables=[model.__table__ for model in MODELS]
            )
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    owner = User(id=uuid4(), email="delete-owner@example.test", password_hash="unused")
    async with factory() as session:
        session.add(owner)
        await session.commit()
    limits = {"max_file_bytes": 10**6, "max_total_bytes": 10**7}
    try:
        yield Site(
            factory,
            owner,
            ReviewStore(tmp_path / "reviews", **limits),
            MediaStore(tmp_path / "media", **limits),
        )
    finally:
        for model in MODELS:
            event.remove(model, "load", restore_utc)
            event.remove(model, "refresh", restore_utc)
        await engine.dispose()


def _project(**fields: Any) -> VideoProject:
    values: dict[str, Any] = {
        "slug": SLUG,
        "title": "杜比怎麼收授權",
        "stage": "final",
        "format": "drama",
        "dropped_at": datetime(2026, 10, 20, tzinfo=UTC),
        "dropped_note": "舊規則，重做",
    }
    return VideoProject(**{**values, **fields})


def _upload(store: ReviewStore, body: bytes = b"preview") -> str:
    sha = hashlib.sha256(body).hexdigest()
    store.put_part(SLUG, sha, index=0, count=1, size=len(body), data=body)
    return sha


async def _delete(site: Site, session: AsyncSession, slug: str = SLUG) -> ProjectDeletedOut:
    return await deletion.delete_project(session, site.store, site.media, slug, site.owner)


async def _count(session: AsyncSession, model: Any) -> int:
    return int(await session.scalar(select(func.count()).select_from(model)) or 0)


async def test_a_dropped_video_goes_with_its_reviews_and_files_and_the_records_stay(
    site: Site,
) -> None:
    review_file = _upload(site.store)
    media_file = _upload(site.media, b"clip")
    async with site.factory() as session:
        project = _project(
            youtube_video_id=YOUTUBE_ID,
            locales={"en": {"captions": True}},
            youtube_sync={"state": "done"},
            backup={"state": "done"},
        )
        session.add(project)
        await session.flush()
        session.add(
            VideoReview(
                project_id=project.id, gate="outline", content_sha256="a" * 64, summary="大綱"
            )
        )
        session.add(
            VideoAiRun(slug=SLUG, stage="plan", provider="x", model="m", status="ok")
        )
        session.add(
            VideoMediaJob(
                slug=SLUG,
                kind="clip",
                purpose="shot",
                provider="x",
                model="m",
                request_hash="b" * 64,
                status="queued",
                usd_estimate=1,
            )
        )
        session.add(
            AdminAuditLog(
                actor_user_id=site.owner.id,
                action="video_project_dropped",
                target=f"video_project:{project.id}",
                metadata_json={"slug": SLUG},
            )
        )
        await session.commit()
        project_id = project.id

        out = await _delete(site, session)

        assert (out.slug, out.youtube_video_id, out.reviews_deleted) == (SLUG, YOUTUBE_ID, 1)
        assert await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG)) is None
        assert await _count(session, VideoReview) == 0
        assert site.store.path(SLUG, review_file) is None
        assert site.media.path(SLUG, media_file) is None
        assert not (site.store.root / SLUG).exists() and not (site.media.root / SLUG).exists()

        # What money is summed over stays, and a job waiting for a vendor is not sent any more.
        assert await _count(session, VideoAiRun) == 1
        job = await session.scalar(select(VideoMediaJob))
        assert job is not None and job.status == "expired"

        # The earlier record stays, and the deletion says what the row said.
        audit = {row.action: row for row in await session.scalars(select(AdminAuditLog))}
        assert set(audit) == {"video_project_dropped", "video_project_deleted"}
        deleted = audit["video_project_deleted"]
        assert deleted.actor_user_id == site.owner.id
        assert deleted.target == f"video_project:{project_id}"
        assert deleted.metadata_json["slug"] == SLUG
        assert deleted.metadata_json["youtube_video_id"] == YOUTUBE_ID
        assert deleted.metadata_json["dropped_note"] == "舊規則，重做"


async def test_a_video_that_was_not_dropped_is_refused_and_keeps_everything(site: Site) -> None:
    sha = _upload(site.store)
    async with site.factory() as session:
        session.add(_project(dropped_at=None, dropped_note=None))
        await session.commit()
        with pytest.raises(AppError) as refused:
            await _delete(site, session)
        assert (refused.value.status, refused.value.code) == (409, "video_project_not_dropped")
        await session.rollback()
        assert await session.scalar(select(VideoProject.id).where(VideoProject.slug == SLUG))
        assert site.store.path(SLUG, sha) is not None
        assert await _count(session, AdminAuditLog) == 0


async def test_a_video_that_is_not_there_is_a_404(site: Site) -> None:
    async with site.factory() as session:
        with pytest.raises(AppError) as refused:
            await _delete(site, session, "nothing-here")
    assert (refused.value.status, refused.value.code) == (404, "video_project_not_found")


async def test_a_worker_that_missed_the_delete_cannot_bring_the_row_back(site: Site) -> None:
    """Its report says it was here before, so a missing row means deleted, not yet to be made."""
    async with site.factory() as session:
        session.add(_project())
        await session.commit()
        await _delete(site, session)

        stale = ProjectIn(title="杜比怎麼收授權", stage="audio", on_site=True)
        with pytest.raises(AppError) as refused:
            await service.upsert_project(session, site.store, SLUG, stale)
        assert (refused.value.status, refused.value.code) == (410, "video_project_deleted")
        await session.rollback()
        found = await session.scalar(select(VideoProject.id).where(VideoProject.slug == SLUG))
        assert found is None


async def test_the_slug_is_free_for_a_new_video_afterwards(
    site: Site, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "compilation_slugs", AsyncMock(return_value=set()))
    async with site.factory() as session:
        session.add(_project(youtube_video_id=YOUTUBE_ID, category="story"))
        await session.commit()
        await _delete(site, session)

        again = await service.upsert_project(
            session, site.store, SLUG, ProjectIn(title="重做", stage="brief")
        )
        assert again.dropped_at is None and again.youtube_video_id is None
        assert again.category is None and again.reviews == []


async def test_a_report_on_a_video_still_there_is_unchanged_by_the_new_field(
    site: Site, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "compilation_slugs", AsyncMock(return_value=set()))
    async with site.factory() as session:
        session.add(_project(dropped_at=None, dropped_note=None))
        await session.commit()
        out = await service.upsert_project(
            session, site.store, SLUG, ProjectIn(title="新標題", stage="audio", on_site=True)
        )
    assert (out.title, out.stage) == ("新標題", "audio")


async def test_started_requests_close_so_they_do_not_read_as_in_the_making(site: Site) -> None:
    async with site.factory() as session:
        session.add(_project())
        session.add(
            VideoDramaRequest(premise="p", status="started", slug=SLUG, style_preset="cinematic-3d")
        )
        session.add(VideoSlidesRequest(source_guide="some-article", status="started", slug=SLUG))
        session.add(
            VideoDailyBriefRequest(
                news_date=date(2026, 10, 20), slug=SLUG, source_guides=[], status="started"
            )
        )
        await session.commit()
        await _delete(site, session)
        requests: tuple[Any, ...] = (VideoDramaRequest, VideoSlidesRequest, VideoDailyBriefRequest)
        for model in requests:
            row = await session.scalar(select(model).where(model.slug == SLUG))
            assert row is not None and row.status == "cancelled", model
            assert row.cancelled_at is not None


async def test_a_finished_request_stays_as_it_was(site: Site) -> None:
    async with site.factory() as session:
        session.add(_project())
        session.add(VideoSlidesRequest(source_guide="some-article", status="done", slug=SLUG))
        await session.commit()
        await _delete(site, session)
        row = await session.scalar(select(VideoSlidesRequest))
        assert row is not None and row.status == "done"


async def test_an_episode_stays_with_its_series_and_can_still_be_redone(site: Site) -> None:
    """The dropped start keeps counting (its request row), and redo_episode reads the slug."""
    async with site.factory() as session:
        series = VideoDramaSeries(
            id=uuid4(), slug="saga", title="長篇", premise="p", status="active", planned_episodes=2
        )
        request = VideoDramaRequest(
            id=uuid4(), premise="p", status="started", slug=SLUG, series_id=series.id,
            episode_number=1, style_preset="cinematic-3d",
        )
        session.add_all([series, request])
        await session.flush()
        # Dropped before the drop learned to close them: the episode is still open.
        session.add(
            VideoDramaEpisode(
                series_id=series.id, number=1, chapter_number=1, title="一", slug=SLUG,
                status="started", request_id=request.id, started_at=datetime.now(UTC),
            )
        )
        session.add(_project(series_slug="saga", episode_number=1))
        await session.commit()
        await _delete(site, session)

        episode = await session.scalar(select(VideoDramaEpisode))
        assert episode is not None and (episode.status, episode.slug) == ("skipped", SLUG)
        kept = await session.scalar(select(VideoDramaRequest))
        assert kept is not None and (kept.status, kept.slug) == ("cancelled", SLUG)


async def test_a_done_episode_stays_done(site: Site) -> None:
    async with site.factory() as session:
        series = VideoDramaSeries(
            id=uuid4(), slug="saga", title="長篇", premise="p", status="active", planned_episodes=2
        )
        session.add(series)
        await session.flush()
        session.add(
            VideoDramaEpisode(
                series_id=series.id, number=1, chapter_number=1, title="一", slug=SLUG,
                status="done",
            )
        )
        session.add(_project(series_slug="saga", episode_number=1))
        await session.commit()
        await _delete(site, session)
        episode = await session.scalar(select(VideoDramaEpisode))
        assert episode is not None and episode.status == "done"


async def test_a_compilation_leaves_out_an_episode_whose_video_was_deleted(
    site: Site, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(series_module, "context_view", AsyncMock(return_value=None))
    captured: dict[str, Any] = {}

    def out(**fields: Any) -> dict[str, Any]:
        captured.update(fields)
        return fields

    monkeypatch.setattr(series_module, "SeriesCompilationStartOut", out)
    monkeypatch.setattr(series_module, "summary_view", lambda *_args: None)
    async with site.factory() as session:
        series = VideoDramaSeries(
            id=uuid4(), slug="saga", title="長篇", premise="p", status="finished",
            planned_episodes=3, compilation=True,
        )
        session.add(series)
        await session.flush()
        for number, video in enumerate(("saga-kept", SLUG, "saga-dropped"), start=1):
            session.add(
                VideoDramaEpisode(
                    series_id=series.id, number=number, chapter_number=1, title=str(number),
                    slug=video, status="done",
                )
            )
        session.add(VideoProject(slug="saga-kept", title="留", stage="done", format="drama"))
        session.add(
            VideoProject(
                slug="saga-dropped", title="棄", stage="done", format="drama",
                dropped_at=datetime.now(UTC),
            )
        )
        session.add(_project())
        await session.commit()
        await _delete(site, session)

        token = VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")
        await series_module.start_compilation(session, token, "saga", "saga-whole")
    assert [episode.slug for episode in captured["episodes"]] == ["saga-kept"]


async def test_a_short_lets_go_of_its_topic_slots_and_metrics_but_not_the_owner_s_material(
    site: Site,
) -> None:
    now = datetime.now(UTC)
    asset = _upload(site.media, b"photo")
    async with site.factory() as session:
        session.add(_project(format="shorts", shorts_line="lab", title="短片"))
        session.add(
            VideoShortsTopic(
                slug=SLUG, line="lab", title="題", status="making", origin="owner",
                project_slug=SLUG,
            )
        )
        session.add_all(
            [
                VideoShortsSlot(
                    starts_at=now + timedelta(days=1), project_slug=SLUG, status="scheduled"
                ),
                VideoShortsSlot(
                    starts_at=now - timedelta(days=2), project_slug=SLUG, status="missed"
                ),
            ]
        )
        session.add(
            VideoShortsMetric(
                project_slug=SLUG, youtube_video_id=YOUTUBE_ID, period="d1", source="data_api",
                captured_at=now,
            )
        )
        session.add(
            VideoShortsAsset(
                topic_slug=SLUG, need="photo", sha256=asset, filename="a.jpg",
                content_type="image/jpeg", size=5, author="站主", rights_note="自己拍的",
            )
        )
        await session.commit()
        out = await _delete(site, session)

        assert out.metrics_deleted == 1 and await _count(session, VideoShortsMetric) == 0
        topic = await session.scalar(select(VideoShortsTopic))
        assert topic is not None and (topic.status, topic.project_slug) == ("dropped", None)
        slots = await session.scalars(select(VideoShortsSlot).order_by(VideoShortsSlot.starts_at))
        assert [(slot.status, slot.project_slug) for slot in slots] == [
            ("missed", SLUG),
            ("open", None),
        ]
        assert site.media.path(SLUG, asset) is not None, "the photo cannot be generated again"


async def test_a_short_already_published_keeps_its_slot_as_a_record_and_frees_the_slug(
    site: Site,
) -> None:
    now = datetime.now(UTC)
    async with site.factory() as session:
        session.add(_project(format="shorts", shorts_line="lab", title="短片"))
        session.add(
            VideoShortsSlot(
                starts_at=now - timedelta(days=1), project_slug=SLUG, status="published"
            )
        )
        await session.commit()
        await _delete(site, session)
        session.add(
            VideoShortsSlot(
                starts_at=now + timedelta(days=1), project_slug=SLUG, status="assigned"
            )
        )
        await session.commit()
        slots = await session.scalars(select(VideoShortsSlot).order_by(VideoShortsSlot.starts_at))
        assert [slot.status for slot in slots] == ["skipped", "assigned"]


async def test_the_route_needs_the_capability_and_the_password_step(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from app.config import Settings

    async def settings(_: Any) -> Settings:
        return Settings(video_review_dir=str(tmp_path))

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    remove = AsyncMock(
        return_value=ProjectDeletedOut(
            slug=SLUG, youtube_video_id=None, reviews_deleted=0, metrics_deleted=0
        )
    )
    monkeypatch.setattr(deletion, "delete_project", remove)
    viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused", auth_version=1)
    viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
    url = f"/api/v1/admin/videos/{SLUG}"
    async with AsyncClient(
        transport=ASGITransport(app=_app(viewer)), base_url="http://test"
    ) as client:
        assert (await client.delete(url)).status_code == 403
    remove.assert_not_awaited()

    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused", auth_version=1)
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    async with AsyncClient(
        transport=ASGITransport(app=_app(owner)), base_url="http://test"
    ) as client:
        no_step = await client.delete(url)
        assert (no_step.status_code, no_step.json()["code"]) == (401, "admin_step_up_required")
        remove.assert_not_awaited()

        other, _ = create_admin_step_up_token(owner, ["database.backup"])
        client.cookies.set(STEP_UP_COOKIE, other)
        another = await client.delete(url)
        assert another.status_code == 403, "another operation's step does not count"
        assert another.json()["code"].startswith("admin_step_up"), "the dialog asks for it"
        remove.assert_not_awaited()

        token, _ = create_admin_step_up_token(owner, ["videos.delete"])
        client.cookies.set(STEP_UP_COOKIE, token)
        passed = await client.delete(url)
    assert passed.status_code == 200 and passed.json()["slug"] == SLUG
    remove.assert_awaited_once()


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
async def test_from_report_to_deleted_and_registered_again_on_postgres(tmp_path: Path) -> None:
    """Against PostgreSQL's locks and the reviews' foreign key, the whole way through."""
    slug = f"del-{uuid4().hex[:12]}"
    limits = {"max_file_bytes": 10**6, "max_total_bytes": 10**7}
    store = ReviewStore(tmp_path / "reviews", **limits)
    media = MediaStore(tmp_path / "media", **limits)
    async with SessionFactory() as session:
        owner = User(email=f"{slug}@example.com", password_hash="unused")
        token = VideoToolToken(name=slug, token_hash=uuid4().hex * 2, token_prefix="mkv_it")
        session.add_all([owner, token])
        await session.commit()
        await service.upsert_project(session, store, slug, ProjectIn(title="片", stage="outline"))
        await service.submit_review(
            session, store, slug,
            ReviewIn(
                gate="outline", content_sha256="4" * 64, summary="大綱",
                payload={"options": [{"key": "A"}, {"key": "B"}]},
            ),
            token,
        )
        with pytest.raises(AppError) as live:
            await deletion.delete_project(session, store, media, slug, owner)
        assert live.value.code == "video_project_not_dropped"
        await session.rollback()

        await service.drop_project(session, store, slug, owner, DropIn(note="不做了"))
        out = await deletion.delete_project(session, store, media, slug, owner)
        assert out.reviews_deleted == 1

        assert slug not in [item.slug for item in await service.list_projects(session)]
        with pytest.raises(AppError) as gone:
            await service.project_view(session, slug)
        assert gone.value.status == 404
        with pytest.raises(AppError) as stale:
            await service.upsert_project(
                session, store, slug, ProjectIn(title="片", stage="audio", on_site=True)
            )
        assert stale.value.status == 410
        await session.rollback()

        audit = await session.scalars(
            select(AdminAuditLog.action).where(AdminAuditLog.actor_user_id == owner.id)
        )
        assert sorted(audit) == ["video_project_deleted", "video_project_dropped"]

        again = await service.upsert_project(
            session, store, slug, ProjectIn(title="重做", stage="brief")
        )
        assert again.dropped_at is None and again.reviews == []
