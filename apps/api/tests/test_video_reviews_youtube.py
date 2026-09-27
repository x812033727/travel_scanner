"""The owner's YouTube link on /admin/videos, and what the review store keeps once a video is up.

docs/videos/HANDS-OFF.md §上傳包與「可以上架」 and §YouTube API 第一步: the owner uploads the
final cut in Studio themselves, pastes the address and the publish time here, and the mp4 leaves
the review store a week later while the rest of the upload package stays.
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.auth.service import current_user
from app.config import Settings
from app.db import get_session
from app.models import User, VideoProject, VideoReview
from app.problems import AppError, app_error_handler
from app.video_reviews import admin_api, admin_service
from app.video_reviews.schemas import ProjectIn, ProjectOut, ProjectSummary, ReviewIn, YoutubeIn
from app.video_reviews.storage import ReviewStore

VIDEO_ID = "dQw4w9WgXcQ"
NOON = datetime(2026, 10, 1, 12, 0, tzinfo=UTC)


def _store(root: Path) -> ReviewStore:
    return ReviewStore(root, max_file_bytes=50_000_000, max_total_bytes=100_000_000)


def _file(store: ReviewStore, slug: str, body: bytes) -> str:
    sha = hashlib.sha256(body).hexdigest()
    store.put_part(slug, sha, index=0, count=1, size=len(body), data=body)
    return sha


def _owner() -> User:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    return owner


def _project(**fields: Any) -> VideoProject:
    values: dict[str, Any] = {
        "id": uuid4(),
        "slug": "v",
        "title": "AI 模型怎麼挑",
        "stage": "done",
        "checklist": [],
        "last_synced_at": NOON,
    }
    return VideoProject(**{**values, **fields})


# --- the pasted address --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "pasted",
    [
        VIDEO_ID,
        f"  {VIDEO_ID}\n",
        f"https://youtu.be/{VIDEO_ID}",
        f"https://youtu.be/{VIDEO_ID}?si=share-token",
        f"https://www.youtube.com/watch?v={VIDEO_ID}",
        f"https://www.youtube.com/watch?t=30s&v={VIDEO_ID}&feature=share",
        f"https://youtube.com/watch?v={VIDEO_ID}",
        f"https://m.youtube.com/watch?v={VIDEO_ID}",
        f"https://youtube.com/shorts/{VIDEO_ID}",
        f"https://www.youtube.com/embed/{VIDEO_ID}",
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit?o=U",
        f"youtu.be/{VIDEO_ID}",
        f"www.youtube.com/watch?v={VIDEO_ID}",
    ],
)
def test_every_shape_of_a_youtube_address_yields_the_eleven_character_id(pasted: str) -> None:
    assert admin_service.youtube_video_id(pasted) == VIDEO_ID


@pytest.mark.parametrize(
    "pasted",
    [
        "",
        "dQw4w9WgXc",
        "dQw4w9WgXcQQ",
        "dQw4w9WgX Q",
        f"https://example.com/watch?v={VIDEO_ID}",
        f"https://youtube.com.example/watch?v={VIDEO_ID}",
        f"https://www.youtube.com.evil.example/shorts/{VIDEO_ID}",
        "https://www.youtube.com/watch?list=PLabcdefghij",
        "https://www.youtube.com/channel/UCabcdefghij",
        f"https://www.youtube.com/playlist/{VIDEO_ID}",
        "https://youtu.be/",
        f"ftp://youtu.be/{VIDEO_ID}",
        "javascript:alert(1)",
        "https://[not-an-address",
    ],
)
def test_anything_else_names_no_video(pasted: str) -> None:
    assert admin_service.youtube_video_id(pasted) is None


def test_the_request_takes_an_aware_publish_time_or_none() -> None:
    assert YoutubeIn(url=VIDEO_ID).publish_at is None
    aware = YoutubeIn(url=VIDEO_ID, publish_at="2026-10-01T20:00:00+08:00")  # type: ignore[arg-type]
    assert aware.publish_at == NOON
    with pytest.raises(ValueError):
        YoutubeIn(url=VIDEO_ID, publish_at="2026-10-01T12:00:00")  # type: ignore[arg-type]


# --- recording the link ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_linking_records_the_id_and_the_publish_time_and_writes_an_audit_row(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _project()
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(admin_service, "project_view", AsyncMock(return_value="view"))
    session = AsyncMock()
    session.add = MagicMock()
    owner = _owner()

    assert await admin_service.link_youtube(session, "v", owner, VIDEO_ID, NOON) == "view"
    assert (project.youtube_video_id, project.youtube_publish_at) == (VIDEO_ID, NOON)
    audit = session.add.call_args.args[0]
    assert (audit.action, audit.target, audit.actor_user_id) == (
        "video_youtube_linked",
        "video_project:v",
        owner.id,
    )
    assert audit.metadata_json == {
        "slug": "v",
        "youtube_video_id": VIDEO_ID,
        "publish_at": "2026-10-01T12:00:00+00:00",
    }
    session.commit.assert_awaited()

    # Pasting again corrects a wrong link; no publish time means the owner has not decided.
    await admin_service.link_youtube(session, "v", owner, "abcdefghijk", None)
    assert (project.youtube_video_id, project.youtube_publish_at) == ("abcdefghijk", None)
    assert session.add.call_args.args[0].metadata_json["publish_at"] is None

    with pytest.raises(AppError) as naive:
        await admin_service.link_youtube(session, "v", owner, VIDEO_ID, NOON.replace(tzinfo=None))
    assert naive.value.code == "video_youtube_publish_at_naive"

    project.dropped_at = NOON
    with pytest.raises(AppError) as dropped:
        await admin_service.link_youtube(session, "v", owner, VIDEO_ID, None)
    assert dropped.value.code == "video_project_dropped"


def test_the_summary_and_the_page_carry_both_youtube_fields() -> None:
    project = _project(youtube_video_id=VIDEO_ID, youtube_publish_at=NOON)
    summary = ProjectSummary(**admin_service._summary(project, 0))
    assert (summary.youtube_video_id, summary.youtube_publish_at) == (VIDEO_ID, NOON)
    assert summary.publish_approved_at is None
    page = ProjectOut(**admin_service._summary(project, 0, None, NOON), reviews=[])
    assert (page.youtube_publish_at, page.publish_approved_at) == (NOON, NOON)
    # An answer recorded before migration 0100 has neither time.
    older = {**admin_service._summary(_project(), 0)}
    del older["youtube_publish_at"], older["publish_approved_at"]
    assert ProjectSummary(**older).youtube_publish_at is None


def _review(gate: str, status: str, decided_at: datetime | None) -> VideoReview:
    return VideoReview(
        id=uuid4(),
        gate=gate,
        status=status,
        content_sha256="a" * 64,
        summary=gate,
        payload={},
        files=[],
        decided_at=decided_at,
        created_at=NOON - timedelta(days=3),
    )


@pytest.mark.asyncio
async def test_the_page_says_when_the_upload_was_confirmed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reviews = [
        _review("publish", "rejected", NOON + timedelta(days=1)),
        _review("publish", "approved", NOON),
        _review("publish", "approved", NOON - timedelta(days=1)),
        _review("final", "approved", NOON + timedelta(days=2)),
        _review("outline", "pending", None),
    ]
    assert admin_service.publish_approved_at(reviews) == NOON
    assert admin_service.publish_approved_at(reviews[3:]) is None
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=_project()))
    monkeypatch.setattr(admin_service, "_reviews", AsyncMock(return_value=reviews))
    monkeypatch.setattr(admin_service, "spend_by_slug", AsyncMock(return_value={}))
    page = await admin_service.project_view(AsyncMock(), "v")
    assert (page.publish_approved_at, page.pending, len(page.reviews)) == (NOON, 1, 5)


@pytest.mark.asyncio
async def test_a_report_that_carries_no_id_keeps_the_stored_one_and_the_files(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    store = _store(tmp_path)
    final = _file(store, "v", b"final cut")
    project = _project(youtube_video_id=VIDEO_ID)
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=project)
    monkeypatch.setattr(admin_service, "project_view", AsyncMock(return_value="view"))

    # An older worker leaves the field out; the current one sends null until it reads the id
    # back (tools/video/review/sync.mjs). Neither may undo what the owner pasted.
    await admin_service.upsert_project(session, store, "v", ProjectIn(title="t", stage="done"))
    assert project.youtube_video_id == VIDEO_ID
    await admin_service.upsert_project(
        session, store, "v", ProjectIn(title="t", stage="done", youtube_video_id=None)
    )
    assert project.youtube_video_id == VIDEO_ID
    assert store.path("v", final) is not None, "the upload package stays for the owner"

    reported = ProjectIn(title="t", stage="done", youtube_video_id="abcdefghijk")
    await admin_service.upsert_project(session, store, "v", reported)
    assert project.youtube_video_id == "abcdefghijk"


# --- what the store keeps afterwards -------------------------------------------------------------


def test_the_upload_package_files_are_accepted_by_the_review_schema() -> None:
    base = {"gate": "publish", "content_sha256": "a" * 64, "summary": "上傳包"}
    # The roles and types the worker sends (tools/video/review, ticket video-hands-off-worker):
    # a locale's captions and description keep the locale's own spelling in the role.
    files = [
        {"role": "final", "sha256": "b" * 64, "size": 1, "content_type": "video/mp4"},
        {"role": "thumbnail", "sha256": "c" * 64, "size": 1, "content_type": "image/jpeg"},
        {"role": "captions_zh-TW", "sha256": "d" * 64, "size": 1, "content_type": "text/plain"},
        {
            "role": "captions_en",
            "sha256": "e" * 64,
            "size": 1,
            "content_type": "application/x-subrip",
        },
        {"role": "captions_zh_cn", "sha256": "2" * 64, "size": 1, "content_type": "text/vtt"},
        {"role": "description_zh-TW", "sha256": "f" * 64, "size": 1, "content_type": "text/plain"},
        {"role": "metadata", "sha256": "1" * 64, "size": 1, "content_type": "application/json"},
    ]
    assert len(ReviewIn.model_validate({**base, "files": files}).files) == 7
    with pytest.raises(ValueError):
        ReviewIn.model_validate({**base, "files": [{**files[0], "content_type": "text/html"}]})
    for role in ("Captions_zh-TW", "captions zh", "-final", "x" * 41):
        with pytest.raises(ValueError):
            ReviewIn.model_validate({**base, "files": [{**files[0], "role": role}]})


@pytest.mark.asyncio
async def test_a_week_after_the_upload_only_the_mp4_leaves_the_store(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    store = _store(tmp_path)
    final = _file(store, "v", b"final cut")
    thumbnail = _file(store, "v", b"thumbnail")
    captions = _file(store, "v", b"1\n00:00:00,000 --> 00:00:01,000\nhi\n")
    description = _file(store, "v", b"title\n\nbody\n")
    preview = _file(store, "v", b"720p preview")
    other = _file(store, "other", b"another video's final cut")
    now = datetime(2026, 10, 10, tzinfo=UTC)
    project = _project(youtube_video_id=VIDEO_ID)
    confirmed = VideoReview(
        gate="publish",
        status="approved",
        decided_at=now - timedelta(days=8),
        payload={},
        files=[
            {"role": "final", "sha256": final, "size": 9, "content_type": "video/mp4"},
            {"role": "thumbnail", "sha256": thumbnail, "size": 9, "content_type": "image/jpeg"},
            {
                "role": "captions_en",
                "sha256": captions,
                "size": 9,
                "content_type": "application/x-subrip",
            },
            {
                "role": "description_en",
                "sha256": description,
                "size": 9,
                "content_type": "text/plain",
            },
        ],
    )
    cut = VideoReview(
        gate="final",
        status="approved",
        decided_at=now - timedelta(days=9),
        payload={},
        files=[{"role": "preview", "sha256": preview, "size": 12, "content_type": "video/mp4"}],
    )
    published = AsyncMock(return_value=[project])
    monkeypatch.setattr(admin_service, "_published_before", published)
    monkeypatch.setattr(admin_service, "_reviews", AsyncMock(return_value=[confirmed, cut]))
    session = AsyncMock()

    # The owner set it to go public five days ago: the week counts from the publish time too.
    project.youtube_publish_at = now - timedelta(days=5)
    assert await admin_service.prune_published_previews(session, store, now) == {}
    assert published.await_args.args[1] == now - timedelta(days=7)
    assert store.path("v", final) is not None and store.path("v", preview) is not None

    project.youtube_publish_at = now - timedelta(days=7)
    removed = await admin_service.prune_published_previews(session, store, now)
    assert removed == {"v": sorted([final, preview])}
    assert store.path("v", final) is None and store.path("v", preview) is None
    for kept in (thumbnail, captions, description):
        assert store.path("v", kept) is not None, "the small files stay for the owner"
    assert store.path("other", other) is not None, "only the listed video is touched"

    # A second pass finds nothing to do, and a video without a publish time goes by the
    # confirmation alone.
    assert await admin_service.prune_published_previews(session, store, now) == {}
    project.youtube_publish_at = None
    again = _file(store, "v", b"final cut")
    assert again == final
    assert await admin_service.prune_published_previews(session, store, now) == {"v": [final]}


@pytest.mark.asyncio
async def test_the_candidates_are_published_videos_whose_confirmation_is_old_enough() -> None:
    session = AsyncMock()
    session.scalars = AsyncMock(return_value=[])
    cutoff = datetime(2026, 10, 3, tzinfo=UTC)
    assert await admin_service._published_before(session, cutoff) == []
    compiled = session.scalars.await_args.args[0].compile()
    sql = str(compiled)
    assert "youtube_video_id IS NOT NULL" in sql
    assert "max(video_reviews.decided_at)" in sql
    assert set(compiled.params.values()) == {"publish", "approved", cutoff}


# --- the routes -----------------------------------------------------------------------------------


def _app(user: User) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.admin_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    app.dependency_overrides[current_user] = lambda: user
    return app


@pytest.mark.asyncio
async def test_the_youtube_route_parses_the_address_and_needs_content_manage(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _project(youtube_video_id=VIDEO_ID, youtube_publish_at=NOON)
    link = AsyncMock(return_value=ProjectOut(**admin_service._summary(project, 0), reviews=[]))
    monkeypatch.setattr(admin_service, "link_youtube", link)
    url = "/api/v1/admin/videos/v/youtube"
    owner = _owner()
    app = _app(owner)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        linked = await client.post(
            url,
            json={"url": f"https://youtu.be/{VIDEO_ID}", "publish_at": "2026-10-01T20:00:00+08:00"},
        )
        undecided = await client.post(url, json={"url": VIDEO_ID})
        not_youtube = await client.post(url, json={"url": f"https://example.com/{VIDEO_ID}"})
        naive = await client.post(url, json={"url": VIDEO_ID, "publish_at": "2026-10-01T12:00:00"})
    assert linked.status_code == 200
    assert linked.json()["youtube_video_id"] == VIDEO_ID
    assert linked.json()["youtube_publish_at"] == "2026-10-01T12:00:00Z"
    assert link.await_args_list[0].args[1:] == ("v", owner, VIDEO_ID, NOON)
    assert undecided.status_code == 200 and link.await_args_list[1].args[3:] == (VIDEO_ID, None)
    assert not_youtube.status_code == 422
    assert not_youtube.json()["code"] == "video_youtube_url_invalid"
    assert naive.status_code == 422, "a publish time without a zone is refused before the service"
    assert link.await_count == 2

    viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
    viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
    async with AsyncClient(
        transport=ASGITransport(app=_app(viewer)), base_url="http://test"
    ) as client:
        refused = await client.post(url, json={"url": VIDEO_ID})
    assert refused.status_code == 403, "a viewer can read but not record an upload"
    assert link.await_count == 2


@pytest.mark.asyncio
async def test_listing_the_videos_prunes_the_published_ones_first(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    prune = AsyncMock(return_value={})
    monkeypatch.setattr(admin_service, "prune_published_previews", prune)
    monkeypatch.setattr(admin_service, "list_projects", AsyncMock(return_value=[]))

    async def settings(_: Any) -> Settings:
        return Settings(video_review_dir=str(tmp_path))

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    app = _app(_owner())
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        listed = await client.get("/api/v1/admin/videos")
    assert listed.status_code == 200 and listed.json() == []
    prune.assert_awaited_once()
    assert prune.await_args.args[1].root == tmp_path
