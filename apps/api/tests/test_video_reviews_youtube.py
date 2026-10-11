"""The owner's YouTube link on /admin/videos, and what the review store keeps once a video is up.

docs/videos/HANDS-OFF.md §上傳包與「可以上架」 and §YouTube API 第一步: the owner uploads the
final cut in Studio themselves, pastes the address and the publish time here, and the mp4 leaves
the review store a week later while the rest of the upload package stays.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app import cli
from app.auth.service import current_user
from app.config import Settings
from app.db import Base, get_session
from app.models import AdminAuditLog, User, VideoProject, VideoReview
from app.problems import AppError, app_error_handler
from app.video_reviews import admin_api, admin_service
from app.video_reviews.admin_service import YoutubePublication
from app.video_reviews.schemas import ProjectIn, ProjectOut, ProjectSummary, ReviewIn, YoutubeIn
from app.video_reviews.storage import ReviewStore
from app.video_youtube.client import YoutubeError
from app.video_youtube.errors import Refused

VIDEO_ID = "dQw4w9WgXcQ"
NOON = datetime(2026, 10, 1, 12, 0, tzinfo=UTC)
CHANNEL = "UCmokaair000000000000000"


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


def _view(project: VideoProject) -> ProjectOut:
    return ProjectOut(**admin_service._summary(project, 0), reviews=[])


def youtube_item(
    video_id: str,
    *,
    privacy: str = "public",
    channel: str = CHANNEL,
    published: datetime | None = NOON,
    scheduled: datetime | None = None,
) -> dict[str, Any]:
    """One videos.list item the way YouTube shapes it (snippet and status)."""
    snippet: dict[str, Any] = {"channelId": channel, "title": f"Video {video_id}"}
    if published is not None:
        snippet["publishedAt"] = published.isoformat().replace("+00:00", "Z")
    status: dict[str, Any] = {"privacyStatus": privacy}
    if scheduled is not None:
        status["publishAt"] = scheduled.isoformat().replace("+00:00", "Z")
    return {"id": video_id, "snippet": snippet, "status": status}


class FakeYoutube:
    """Stands in for ``YoutubeClient``: what videos.list answers, and what was asked of it."""

    def __init__(self, *items: dict[str, Any], failure: Exception | None = None) -> None:
        self.items = {item["id"]: item for item in items}
        self.failure = failure
        self.asked: list[list[str]] = []
        self.parts: list[str] = []

    async def video(self, video_id: str) -> dict[str, Any] | None:
        self.asked.append([video_id])
        if self.failure is not None:
            raise self.failure
        return self.items.get(video_id)

    async def videos(self, video_ids: Sequence[str], *, parts: str) -> list[dict[str, Any]]:
        assert len(video_ids) <= 50, "videos.list takes at most fifty ids"
        self.asked.append(list(video_ids))
        self.parts.append(parts)
        if self.failure is not None:
            raise self.failure
        return [self.items[video_id] for video_id in video_ids if video_id in self.items]


def link_channel(
    monkeypatch: pytest.MonkeyPatch,
    youtube: FakeYoutube | None,
    *,
    channel: str = CHANNEL,
    refused: Refused | None = None,
) -> None:
    """Make the service's linked channel ``youtube``, or ``refused`` when there is none."""

    @asynccontextmanager
    async def linked(_session: AsyncSession) -> AsyncIterator[tuple[str, Any]]:
        if refused is not None:
            raise refused
        yield channel, youtube

    monkeypatch.setattr(admin_service, "_linked_youtube", linked)


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
    monkeypatch.setattr(admin_service, "project_view", AsyncMock(return_value=_view(project)))
    asked = AsyncMock(return_value=YoutubePublication(None, admin_service.NOT_PUBLIC))
    monkeypatch.setattr(admin_service, "youtube_publication", asked)
    session = AsyncMock()
    session.add = MagicMock()
    owner = _owner()

    page = await admin_service.link_youtube(session, "v", owner, VIDEO_ID, NOON)
    assert page.youtube_publish_note is None
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
        "publish_at_source": "owner",
        "publish_at_reason": None,
    }
    session.commit.assert_awaited()
    asked.assert_not_awaited()

    # Pasting again corrects a wrong link; with no publish time YouTube is asked, and a video
    # that is still private keeps none, with the reason on the page and in the audit row.
    page = await admin_service.link_youtube(session, "v", owner, "abcdefghijk", None)
    assert (project.youtube_video_id, project.youtube_publish_at) == ("abcdefghijk", None)
    assert asked.await_args.args[1] == "abcdefghijk"
    assert page.youtube_publish_note == admin_service.NOT_PUBLIC
    assert session.add.call_args.args[0].metadata_json == {
        "slug": "v",
        "youtube_video_id": "abcdefghijk",
        "publish_at": None,
        "publish_at_source": None,
        "publish_at_reason": admin_service.NOT_PUBLIC,
    }

    with pytest.raises(AppError) as naive:
        await admin_service.link_youtube(session, "v", owner, VIDEO_ID, NOON.replace(tzinfo=None))
    assert naive.value.code == "video_youtube_publish_at_naive"

    project.dropped_at = NOON
    with pytest.raises(AppError) as dropped:
        await admin_service.link_youtube(session, "v", owner, VIDEO_ID, None)
    assert dropped.value.code == "video_project_dropped"


@pytest.mark.asyncio
async def test_a_video_the_owner_made_public_in_studio_takes_the_time_youtube_reports(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _project()
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(admin_service, "project_view", AsyncMock(return_value=_view(project)))
    session = AsyncMock()
    session.add = MagicMock()
    owner = _owner()
    youtube = FakeYoutube(youtube_item(VIDEO_ID, published=NOON - timedelta(days=2)))
    link_channel(monkeypatch, youtube)

    page = await admin_service.link_youtube(session, "v", owner, VIDEO_ID, None)
    assert project.youtube_publish_at == NOON - timedelta(days=2)
    assert page.youtube_publish_note is None
    assert youtube.asked == [[VIDEO_ID]], "one videos.list call, nothing written to YouTube"
    assert session.add.call_args.args[0].metadata_json == {
        "slug": "v",
        "youtube_video_id": VIDEO_ID,
        "publish_at": "2026-09-29T12:00:00+00:00",
        "publish_at_source": "youtube",
        "publish_at_reason": None,
    }

    # A private video scheduled in Studio takes its scheduled time, so it appears on time.
    later = NOON + timedelta(days=3)
    scheduled = youtube_item(VIDEO_ID, privacy="private", scheduled=later)
    link_channel(monkeypatch, FakeYoutube(scheduled))
    page = await admin_service.link_youtube(session, "v", owner, VIDEO_ID, None)
    assert (project.youtube_publish_at, page.youtube_publish_note) == (later, None)

    # The owner's own time wins over YouTube's, and YouTube is not even asked.
    youtube = FakeYoutube(youtube_item(VIDEO_ID))
    link_channel(monkeypatch, youtube)
    await admin_service.link_youtube(session, "v", owner, VIDEO_ID, NOON)
    assert project.youtube_publish_at == NOON and youtube.asked == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("youtube", "channel", "refused", "note"),
    [
        (
            FakeYoutube(youtube_item(VIDEO_ID, privacy="private")),
            CHANNEL,
            None,
            admin_service.NOT_PUBLIC,
        ),
        (
            FakeYoutube(youtube_item(VIDEO_ID, privacy="unlisted")),
            CHANNEL,
            None,
            admin_service.NOT_PUBLIC,
        ),
        (FakeYoutube(), CHANNEL, None, admin_service.NOT_IN_CHANNEL),
        (
            FakeYoutube(youtube_item(VIDEO_ID, channel="UCsomebodyelse0000000000")),
            CHANNEL,
            None,
            admin_service.NOT_IN_CHANNEL,
        ),
        (
            FakeYoutube(youtube_item(VIDEO_ID, published=None)),
            CHANNEL,
            None,
            admin_service.NO_PUBLISHED_AT,
        ),
        (
            None,
            CHANNEL,
            Refused(409, "video_youtube_not_linked", "還沒有連結 YouTube 頻道：到設定分頁連結"),
            "還沒有連結 YouTube 頻道：到設定分頁連結",
        ),
        (None, CHANNEL, Refused(409, "video_youtube_grant_lost", "授權失效"), "授權失效"),
        (
            FakeYoutube(failure=YoutubeError(403, "quotaExceeded", "over")),
            CHANNEL,
            None,
            admin_service._unreachable(YoutubeError(403, "quotaExceeded", "over")),
        ),
        (
            FakeYoutube(failure=httpx.ConnectError("down")),
            CHANNEL,
            None,
            admin_service._unreachable(httpx.ConnectError("down")),
        ),
    ],
    ids=[
        "private",
        "unlisted",
        "not-found",
        "another-channel",
        "public-without-time",
        "not-linked",
        "grant-lost",
        "api-refused",
        "network-down",
    ],
)
async def test_without_a_public_time_the_id_is_still_recorded_and_the_reason_is_told(
    monkeypatch: pytest.MonkeyPatch,
    youtube: FakeYoutube | None,
    channel: str,
    refused: Refused | None,
    note: str,
) -> None:
    project = _project()
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(admin_service, "project_view", AsyncMock(return_value=_view(project)))
    session = AsyncMock()
    session.add = MagicMock()
    link_channel(monkeypatch, youtube, channel=channel, refused=refused)

    page = await admin_service.link_youtube(session, "v", _owner(), VIDEO_ID, None)
    assert (project.youtube_video_id, project.youtube_publish_at) == (VIDEO_ID, None)
    assert page.youtube_publish_note == note
    metadata = session.add.call_args.args[0].metadata_json
    assert (metadata["publish_at"], metadata["publish_at_source"]) == (None, None)
    assert metadata["publish_at_reason"] == note
    session.commit.assert_awaited()


def test_what_a_videos_list_item_says_about_publication() -> None:
    public = admin_service.publication_of(youtube_item(VIDEO_ID), CHANNEL)
    assert public == YoutubePublication(NOON, None)
    # A public video is never read as scheduled, whatever else its status carries.
    stale = youtube_item(VIDEO_ID, scheduled=NOON + timedelta(days=1))
    assert admin_service.publication_of(stale, CHANNEL).publish_at == NOON
    # Without a channel to check against (none linked), the item is read as it is.
    assert admin_service.publication_of(youtube_item(VIDEO_ID), None).publish_at == NOON
    assert admin_service.publication_of({"id": VIDEO_ID}, CHANNEL) == YoutubePublication(
        None, admin_service.NOT_IN_CHANNEL
    )
    assert admin_service.publication_of({"id": VIDEO_ID}, None) == YoutubePublication(
        None, admin_service.NOT_PUBLIC
    )


# --- the one-off backfill of the videos published from Studio -------------------------------------


@pytest.fixture
async def factory() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    tables = [cast(Table, model.__table__) for model in (User, VideoProject, AdminAuditLog)]
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    yield async_sessionmaker(engine, expire_on_commit=False)
    await engine.dispose()


def _linked(slug: str, video_id: str, **fields: Any) -> VideoProject:
    return _project(slug=slug, youtube_video_id=video_id, **fields)


async def _publish_times(factory: async_sessionmaker[AsyncSession]) -> dict[str, datetime | None]:
    """Each video's stored publish time; SQLite drops the zone, and they were written in UTC."""
    async with factory() as session:
        rows = await session.scalars(select(VideoProject).order_by(VideoProject.slug))
        return {
            row.slug: (
                row.youtube_publish_at.replace(tzinfo=UTC) if row.youtube_publish_at else None
            )
            for row in rows
        }


@pytest.mark.asyncio
async def test_the_backfill_reports_every_video_and_writes_only_with_apply(
    monkeypatch: pytest.MonkeyPatch, factory: async_sessionmaker[AsyncSession]
) -> None:
    earlier = NOON - timedelta(days=5)
    later = NOON + timedelta(days=2)
    async with factory() as session:
        session.add_all(
            [
                _linked("public", "public00001"),
                _linked("scheduled", "schedule001"),
                _linked("private", "private0001"),
                _linked("gone", "gone0000001"),
                _linked("elsewhere", "elsewhere01"),
                _linked("timed", "timed000001", youtube_publish_at=NOON),
                _linked("dropped", "dropped0001", dropped_at=NOON, dropped_note="no"),
                _project(slug="unuploaded"),
            ]
        )
        await session.commit()
    youtube = FakeYoutube(
        youtube_item("public00001", published=earlier),
        youtube_item("schedule001", privacy="private", scheduled=later),
        youtube_item("private0001", privacy="private"),
        youtube_item("elsewhere01", channel="UCsomebodyelse0000000000"),
    )
    link_channel(monkeypatch, youtube)

    async with factory() as session:
        report = await admin_service.backfill_youtube_publish_times(session, apply=False)
    assert (report["apply"], report["checked"], report["filled"]) == (False, 5, 2)
    assert youtube.asked == [
        ["elsewhere01", "gone0000001", "private0001", "public00001", "schedule001"]
    ]
    assert youtube.parts == ["snippet,status"]
    assert report["videos"] == [
        {
            "slug": "elsewhere",
            "youtube_video_id": "elsewhere01",
            "publish_at": None,
            "reason": admin_service.NOT_IN_CHANNEL,
        },
        {
            "slug": "gone",
            "youtube_video_id": "gone0000001",
            "publish_at": None,
            "reason": admin_service.NOT_IN_CHANNEL,
        },
        {
            "slug": "private",
            "youtube_video_id": "private0001",
            "publish_at": None,
            "reason": admin_service.NOT_PUBLIC,
        },
        {
            "slug": "public",
            "youtube_video_id": "public00001",
            "publish_at": "2026-09-26T12:00:00+00:00",
            "reason": None,
        },
        {
            "slug": "scheduled",
            "youtube_video_id": "schedule001",
            "publish_at": "2026-10-03T12:00:00+00:00",
            "reason": None,
        },
    ]
    assert json.dumps(report, ensure_ascii=False), "the CLI prints it as JSON"
    before = await _publish_times(factory)
    assert before["public"] is None and before["timed"] == NOON, "a dry run writes nothing"

    async with factory() as session:
        applied = await admin_service.backfill_youtube_publish_times(session, apply=True)
    assert applied["videos"] == report["videos"] and applied["filled"] == 2
    after = await _publish_times(factory)
    assert (after["public"], after["scheduled"]) == (earlier, later)
    assert (after["private"], after["gone"], after["elsewhere"]) == (None, None, None)
    assert (after["timed"], after["dropped"], after["unuploaded"]) == (NOON, None, None)
    async with factory() as session:
        audits = list(
            await session.scalars(select(AdminAuditLog).order_by(AdminAuditLog.target))
        )
    assert [(row.action, row.target, row.actor_user_id) for row in audits] == [
        ("video_youtube_publish_time_backfilled", "video_project:public", None),
        ("video_youtube_publish_time_backfilled", "video_project:scheduled", None),
    ]
    assert audits[0].metadata_json == {
        "slug": "public",
        "youtube_video_id": "public00001",
        "publish_at": "2026-09-26T12:00:00+00:00",
        "publish_at_source": "youtube",
    }

    # Run again: the filled ones are no longer asked about.
    async with factory() as session:
        again = await admin_service.backfill_youtube_publish_times(session, apply=True)
    assert [item["slug"] for item in again["videos"]] == ["elsewhere", "gone", "private"]
    assert again["filled"] == 0


@pytest.mark.asyncio
async def test_the_backfill_asks_fifty_ids_at_a_time_and_needs_a_linked_channel(
    monkeypatch: pytest.MonkeyPatch, factory: async_sessionmaker[AsyncSession]
) -> None:
    ids = [f"video{index:06d}" for index in range(120)]
    async with factory() as session:
        session.add_all(_linked(f"v{index:03d}", video_id) for index, video_id in enumerate(ids))
        await session.commit()
    youtube = FakeYoutube(*(youtube_item(video_id) for video_id in ids))
    link_channel(monkeypatch, youtube)

    async with factory() as session:
        report = await admin_service.backfill_youtube_publish_times(session, apply=True)
    assert (report["checked"], report["filled"]) == (120, 120)
    assert [len(batch) for batch in youtube.asked] == [50, 50, 20]
    assert all(time == NOON for time in (await _publish_times(factory)).values())

    # Without a linked channel the run stops before anything is read or written.
    async with factory() as session:
        session.add(_linked("late", "late0000001"))
        await session.commit()
    youtube = FakeYoutube()
    link_channel(
        monkeypatch, youtube, refused=Refused(409, "video_youtube_not_linked", "還沒有連結")
    )
    async with factory() as session:
        with pytest.raises(Refused) as refused:
            await admin_service.backfill_youtube_publish_times(session, apply=True)
    assert refused.value.code == "video_youtube_not_linked" and youtube.asked == []

    # And with nothing to fill, YouTube is not asked at all.
    async with factory() as session:
        for row in await session.scalars(select(VideoProject)):
            row.youtube_publish_at = NOON
        await session.commit()
    link_channel(monkeypatch, youtube)
    async with factory() as session:
        empty = await admin_service.backfill_youtube_publish_times(session, apply=True)
    assert empty == {"apply": True, "checked": 0, "filled": 0, "videos": []}
    assert youtube.asked == []


def test_the_cli_command_reports_unless_apply_and_fails_plainly_without_a_channel(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    report = {"apply": False, "checked": 1, "filled": 1, "videos": [{"slug": "v"}]}
    backfill = AsyncMock(return_value=report)
    monkeypatch.setattr(cli, "backfill_youtube_publish_times", backfill)
    monkeypatch.setattr(cli, "SessionFactory", lambda: AsyncMock())

    monkeypatch.setattr("sys.argv", ["cli", "video-youtube-backfill-publish-times"])
    cli.main()
    assert json.loads(capsys.readouterr().out) == report
    assert backfill.await_args.kwargs == {"apply": False}

    monkeypatch.setattr("sys.argv", ["cli", "video-youtube-backfill-publish-times", "--apply"])
    cli.main()
    assert backfill.await_args.kwargs == {"apply": True}

    backfill.side_effect = Refused(409, "video_youtube_not_linked", "還沒有連結 YouTube 頻道")
    with pytest.raises(SystemExit) as stopped:
        cli.main()
    assert stopped.value.code == 2
    captured = capsys.readouterr()
    assert "ERROR video_youtube_not_linked: 還沒有連結 YouTube 頻道" in captured.err


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
        {"role": "captions_ko", "sha256": "2" * 64, "size": 1, "content_type": "text/vtt"},
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
