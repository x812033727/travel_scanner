"""Taking an uploaded-but-unscheduled video's YouTube link off, so a remade cut can go up again.

The owner (2026-11-14): a re-pushed episode that still shows 「已連結，未記錄公開時間」 must be
unlinkable from /admin/videos. A scheduled or public video, one being sent, and a dropped one are
refused; the old id never comes back from a report that still carries it in video.json.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast
from unittest.mock import AsyncMock
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import current_user
from app.db import Base, get_session
from app.models import AdminAuditLog, User, VideoProject, VideoReview
from app.problems import AppError, app_error_handler
from app.video_reviews import admin_api, admin_service
from app.video_reviews.schemas import ProjectIn, ProjectOut
from app.video_reviews.storage import ReviewStore
from app.video_youtube import vps
from app.video_youtube.errors import Refused
from tests.test_video_youtube import Site, open_site
from tests.test_video_youtube_sync import SLUG, STUDIO_ID, _package
from tests.test_video_youtube_vps import Remote, _configure_vps, begin

OLD = "dQw4w9WgXcQ"
NEW = "abcdefghijk"
NOON = datetime(2026, 11, 14, 12, 0, tzinfo=UTC)


@pytest.fixture
async def factory() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    models = (User, VideoProject, VideoReview, AdminAuditLog)
    tables = [cast(Table, model.__table__) for model in models]
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    yield async_sessionmaker(engine, expire_on_commit=False)
    await engine.dispose()


def _owner() -> User:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    return owner


async def _seed(factory: async_sessionmaker[AsyncSession], owner: User, **fields: Any) -> None:
    values: dict[str, Any] = {
        "id": uuid4(),
        "slug": "v",
        "title": "重做的一集",
        "stage": "done",
        "checklist": [],
        "last_synced_at": NOON,
        "youtube_video_id": OLD,
    }
    async with factory() as session:
        session.add(User(id=owner.id, email=owner.email, password_hash="unused"))
        session.add(VideoProject(**{**values, **fields}))
        await session.commit()


async def _row(factory: async_sessionmaker[AsyncSession]) -> VideoProject:
    async with factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == "v"))
        assert project is not None
        return project


@pytest.fixture
def quiet(monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    """No VPS uploader configured, and the page's view is not what these tests read."""
    idle = AsyncMock()
    monkeypatch.setattr(vps, "assert_idle", idle)
    monkeypatch.setattr(admin_service, "project_view", AsyncMock(return_value="view"))
    return idle


@pytest.mark.asyncio
async def test_unlinking_clears_every_trace_of_the_old_upload_and_writes_an_audit_row(
    factory: async_sessionmaker[AsyncSession], quiet: AsyncMock
) -> None:
    owner = _owner()
    await _seed(
        factory,
        owner,
        youtube_upload_session=f"{'a' * 64} https://upload.example/session",
        youtube_sync={"status": "failed", "request": {"video_id": OLD}},
        youtube_removed_at=NOON,
    )
    async with factory() as session:
        assert await admin_service.unlink_youtube(session, "v", owner) == "view"
    quiet.assert_awaited_once()
    project = await _row(factory)
    assert project.youtube_video_id is None
    assert project.youtube_publish_at is None
    assert project.youtube_upload_session is None
    assert project.youtube_sync is None
    assert project.youtube_removed_at is None
    async with factory() as session:
        audit = (await session.scalars(select(AdminAuditLog))).one()
    assert (audit.action, audit.target, audit.actor_user_id) == (
        "video_youtube_unlinked",
        "video_project:v",
        owner.id,
    )
    assert audit.metadata_json["youtube_video_id"] == OLD
    assert audit.metadata_json["had_upload_session"] is True
    assert audit.metadata_json["youtube_sync_status"] == "failed"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("fields", "code"),
    [
        ({"youtube_publish_at": NOON}, "video_youtube_unlink_scheduled"),
        (
            {"youtube_sync": {"status": "running", "lease_until": "2099-01-01T00:00:00+00:00"}},
            "video_youtube_unlink_sync_running",
        ),
        ({"dropped_at": NOON}, "video_project_dropped"),
        ({"youtube_video_id": None}, "video_youtube_not_linked"),
    ],
)
async def test_a_scheduled_sending_dropped_or_unlinked_video_is_refused_without_writing(
    factory: async_sessionmaker[AsyncSession],
    quiet: AsyncMock,
    fields: dict[str, Any],
    code: str,
) -> None:
    owner = _owner()
    await _seed(factory, owner, **fields)
    async with factory() as session:
        with pytest.raises(AppError) as refused:
            await admin_service.unlink_youtube(session, "v", owner)
    assert (refused.value.status, refused.value.code) == (409, code)
    project = await _row(factory)
    assert project.youtube_video_id == fields.get("youtube_video_id", OLD)
    async with factory() as session:
        assert (await session.scalars(select(AdminAuditLog))).first() is None


@pytest.mark.asyncio
async def test_an_uploader_job_still_going_is_refused(
    factory: async_sessionmaker[AsyncSession], quiet: AsyncMock
) -> None:
    owner = _owner()
    await _seed(factory, owner)
    quiet.side_effect = Refused(409, "vps_job_exists", "這支影片已有 VPS 工作")
    async with factory() as session:
        with pytest.raises(AppError) as refused:
            await admin_service.unlink_youtube(session, "v", owner)
    assert refused.value.code == "vps_job_exists"
    assert (await _row(factory)).youtube_video_id == OLD


@pytest.mark.asyncio
async def test_a_report_that_still_carries_the_unlinked_id_does_not_link_it_again(
    factory: async_sessionmaker[AsyncSession], quiet: AsyncMock, tmp_path: Path
) -> None:
    owner = _owner()
    await _seed(factory, owner)
    store = ReviewStore(tmp_path, max_file_bytes=1_000, max_total_bytes=10_000)
    async with factory() as session:
        await admin_service.unlink_youtube(session, "v", owner)

    # The worker's video.json (and the repository's) still names the old upload.
    stale = ProjectIn(title="t", stage="done", youtube_video_id=OLD)
    async with factory() as session:
        await admin_service.upsert_project(session, store, "v", stale)
    assert (await _row(factory)).youtube_video_id is None

    # The owner links the new cut; a later report of the old id does not replace it.
    async with factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == "v"))
        assert project is not None
        project.youtube_video_id = NEW
        await session.commit()
    async with factory() as session:
        await admin_service.upsert_project(session, store, "v", stale)
    assert (await _row(factory)).youtube_video_id == NEW

    # Any other id a report carries is still taken, as before.
    async with factory() as session:
        await admin_service.upsert_project(
            session, store, "v", ProjectIn(title="t", stage="done", youtube_video_id="zyxwvutsrqp")
        )
    assert (await _row(factory)).youtube_video_id == "zyxwvutsrqp"


def _app(user: User) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.admin_router, prefix="/api/v1")

    async def session() -> AsyncIterator[AsyncMock]:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    app.dependency_overrides[current_user] = lambda: user
    return app


@pytest.mark.asyncio
async def test_the_route_needs_content_manage(monkeypatch: pytest.MonkeyPatch) -> None:
    project = VideoProject(
        id=uuid4(), slug="v", title="t", stage="done", checklist=[], last_synced_at=NOON
    )
    unlink = AsyncMock(return_value=ProjectOut(**admin_service._summary(project, 0), reviews=[]))
    monkeypatch.setattr(admin_service, "unlink_youtube", unlink)
    url = "/api/v1/admin/videos/v/youtube"
    owner = _owner()
    async with AsyncClient(transport=ASGITransport(app=_app(owner)), base_url="http://test") as c:
        done = await c.delete(url)
    assert done.status_code == 200
    assert done.json()["youtube_video_id"] is None
    assert unlink.await_args.args[1:] == ("v", owner)

    viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
    viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
    async with AsyncClient(transport=ASGITransport(app=_app(viewer)), base_url="http://test") as c:
        refused = await c.delete(url)
    assert refused.status_code == 403
    assert unlink.await_count == 1


@pytest.fixture
async def uploader(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> AsyncIterator[tuple[Site, Remote]]:
    """A real approved package and database, with only the VPS uploader's HTTP faked."""
    async with open_site(monkeypatch, tmp_path) as site:
        remote = Remote()
        await _configure_vps(site)
        monkeypatch.setattr(vps, "load_runtime_settings", AsyncMock(return_value=site.settings))
        monkeypatch.setattr(
            vps,
            "http_client",
            lambda: httpx.AsyncClient(transport=httpx.MockTransport(remote.respond)),
        )
        await _package(site)
        yield site, remote


@pytest.mark.asyncio
async def test_the_uploaders_last_job_does_not_stand_for_the_new_cut_once_unlinked(
    uploader: tuple[Site, Remote],
) -> None:
    site, remote = uploader
    await begin(site, url=f"https://youtu.be/{STUDIO_ID}")
    assert remote.job
    remote.job["state"] = "done"
    async with site.factory() as session:
        await vps.action(session, SLUG, site.owner, "record", vps.ResumeIn())
        await admin_service.unlink_youtube(session, SLUG, site.owner)
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject))
        assert project is not None and project.youtube_video_id is None
        # The API sender's upload is no longer held back by the finished job of the old video.
        await vps.assert_idle(session, SLUG, upload=True)

    # The remade cut's package: the old job no longer matches it, and a new job uploads the mp4
    # instead of sending the new details to the old video.
    remote.job["review_sha256"] = "f" * 64
    again = await begin(site)
    assert again["job"]["video_id"] is None
    assert any(f["role"] == "final" for f in remote.manifest["files"])
