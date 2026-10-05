"""Shorts go to YouTube on the calendar (docs/videos/SHORTS.md §上架): what the site sends under
the owner's standing consent and why it holds the rest, the claim of the files the owner
uploaded, the recall, and the worker's knock that sets all of it going.

``ShortsGoogle`` adds the channel's uploads, and several videos in one call, to the fake of
test_video_youtube.py. The database is SQLite, the upload packages are in a real review store,
and ``run_sync`` is awaited directly instead of being launched as a task. The clock is the real
one, because a run writes real times into its state: the slots are set hours from now.
"""

from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import zipfile
from collections.abc import AsyncIterator, Awaitable, Callable, Sequence
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from urllib.parse import parse_qs
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

import fakeredis.aioredis
import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from redis.exceptions import ConnectionError as RedisConnectionError
from sqlalchemy import event, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import current_user
from app.config import Settings, get_settings
from app.db import Base, get_session
from app.models import (
    AdminAuditLog,
    ProviderConfig,
    User,
    VideoProject,
    VideoReview,
    VideoToolToken,
    VideoYoutubeConnection,
)
from app.problems import AppError, app_error_handler
from app.video_automation.models import VideoAutomationSettings, VideoDramaSeries
from app.video_media.models import VideoMediaJob
from app.video_reviews import admin_service
from app.video_reviews.admin_service import review_store
from app.video_reviews.storage import ReviewStore
from app.video_shorts import admin_publish_api, claim, publish
from app.video_shorts import settings as shorts_settings
from app.video_shorts import tick as knock
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.models import (
    VideoShortsCost,
    VideoShortsMetric,
    VideoShortsSettings,
    VideoShortsSlot,
    VideoShortsTopic,
)
from app.video_shorts.quota import Quota, pacific_day
from app.video_shorts.schemas import SettingsWrite, TickOut
from app.video_speech import admin_api as speech_api
from app.video_youtube import connection, requests, sync
from app.video_youtube.client import YoutubeClient
from app.video_youtube.schemas import PublishIn
from app.video_youtube.state import new_state
from tests.test_video_youtube import CHANNEL, SITE, FakeGoogle, Site

UPLOADS = "UUfixtureuploads0000000"
VIDEO = "ShortVid001"
MP4 = bytes(range(256)) * 4
SRT = "1\n00:00:00,000 --> 00:00:02,000\n字幕\n".encode()
SECONDS = 35.2
HOURS = timedelta(hours=1)
TAIPEI = ZoneInfo("Asia/Taipei")
Arrange = Callable[["ShortsSite", datetime], Awaitable[None]]


# --- a YouTube that also lists what the channel uploaded ----------------------------------------


@dataclass
class ShortsGoogle(FakeGoogle):
    """``FakeGoogle`` with the uploads playlist and videos.list for several ids and any parts."""

    # The channel's uploads, newest first.
    uploads: list[str] = field(default_factory=list)
    # The ids each videos.list for several videos asked for.
    asked: list[list[str]] = field(default_factory=list)

    def handle(self, request: httpx.Request) -> httpx.Response:
        url = request.url
        query = parse_qs(url.query.decode())
        part = query.get("part", [""])[0]
        if url.path == "/youtube/v3/channels" and part == "contentDetails":
            assert request.headers["authorization"].startswith("Bearer access-")
            refused = self._refused("channels.list")
            if refused:
                return refused
            related = {"relatedPlaylists": {"uploads": UPLOADS}}
            items = [{"id": self.channel["id"], "contentDetails": related}] if self.channel else []
            return httpx.Response(200, json={"items": items})
        if url.path == "/youtube/v3/playlistItems":
            assert request.headers["authorization"].startswith("Bearer access-")
            refused = self._refused("playlistItems.list")
            if refused:
                return refused
            assert query["playlistId"] == [UPLOADS]
            newest = self.uploads[: int(query["maxResults"][0])]
            return httpx.Response(
                200, json={"items": [{"contentDetails": {"videoId": each}} for each in newest]}
            )
        if url.path == "/youtube/v3/videos" and request.method == "GET" and "maxResults" in query:
            assert request.headers["authorization"].startswith("Bearer access-")
            refused = self._refused("videos.list")
            if refused:
                return refused
            ids = query["id"][0].split(",")
            assert len(ids) <= 50, "videos.list takes fifty ids"
            self.asked.append(ids)
            parts = part.split(",")
            items = [
                {
                    "id": each,
                    **{
                        name: copy.deepcopy(self.videos[each][name])
                        for name in parts
                        if name in self.videos[each]
                    },
                }
                for each in ids
                if each in self.videos
            ]
            return httpx.Response(200, json={"items": items})
        if url.path == "/youtube/v3/videos" and request.method == "PUT":
            # An update replaces what a part holds, except what only YouTube writes: the
            # video stays on its channel.
            video_id = json.loads(request.content)["id"]
            channel = self.videos.get(video_id, {}).get("snippet", {}).get("channelId")
            response = super().handle(request)
            if response.status_code == 200 and channel is not None:
                kept = {**self.videos[video_id]["snippet"], "channelId": channel}
                self.videos[video_id]["snippet"] = kept
            return response
        return super().handle(request)

    def put(self, video_id: str, **fields: Any) -> dict[str, Any]:
        """A video on the channel, private unless told otherwise."""
        video: dict[str, Any] = {
            "id": video_id,
            "snippet": {
                "title": "final",
                "description": "",
                "categoryId": "22",
                "channelId": CHANNEL,
            },
            "status": {"privacyStatus": "private", "embeddable": True, "license": "youtube"},
        }
        for name, value in fields.items():
            video[name] = {**video.get(name, {}), **value}
        self.videos[video_id] = video
        return video


def upload(
    video_id: str,
    name: str,
    *,
    privacy: str = "private",
    duration: str = "PT35S",
    channel: str = CHANNEL,
    kept: bool = True,
) -> dict[str, Any]:
    """An upload as videos.list answers its owner: the title Studio made from the file name,
    and the file name itself when YouTube kept it."""
    video: dict[str, Any] = {
        "id": video_id,
        "snippet": {"title": name.removesuffix(".mp4"), "channelId": channel},
        "status": {"privacyStatus": privacy},
        "contentDetails": {"duration": duration},
    }
    if kept:
        video["fileDetails"] = {"fileName": name}
    return video


# --- a site to run on ---------------------------------------------------------------------------

MODELS = (
    User,
    VideoProject,
    VideoReview,
    VideoToolToken,
    VideoYoutubeConnection,
    AdminAuditLog,
    VideoMediaJob,
    VideoAutomationSettings,
    VideoDramaSeries,
    VideoShortsSettings,
    VideoShortsSlot,
    VideoShortsTopic,
    VideoShortsMetric,
    VideoShortsCost,
    # The VPS uploader's settings row: the sender reads it (vps_settings.resolve) before it sends.
    ProviderConfig,
)


@dataclass
class ShortsSite(Site):
    store: ReviewStore
    launched: list[str]

    @property
    def youtube(self) -> ShortsGoogle:
        assert isinstance(self.google, ShortsGoogle)
        return self.google


@asynccontextmanager
async def open_shorts_site(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, database: str = "sqlite"
) -> AsyncIterator[ShortsSite]:
    """The database with the Shorts' tables, the fake YouTube and the patched site;
    test_video_shorts_stats.py shares it. ``postgresql`` is a schema of its own in the
    database CI runs the integration tests against, for what SQLite cannot show: row locks
    and a second connection that commits while the first one waits."""
    schema = f"shorts_site_{uuid4().hex}"
    administrator = None
    if database == "postgresql":
        administrator = create_async_engine(get_settings().database_url)
        async with administrator.begin() as db:
            await db.execute(text(f'CREATE SCHEMA "{schema}"'))
        engine = create_async_engine(
            get_settings().database_url, connect_args={"server_settings": {"search_path": schema}}
        )
    else:
        engine = create_async_engine("sqlite+aiosqlite://")

    # SQLite drops timezone offsets; PostgreSQL hands back aware datetimes.
    def restore_utc(target: Any, _context: Any, *_more: Any) -> None:
        for column in target.__table__.columns:
            value = getattr(target, column.name)
            if isinstance(value, datetime) and value.tzinfo is None:
                setattr(target, column.name, value.replace(tzinfo=UTC))

    for model in MODELS:
        event.listen(model, "load", restore_utc)
        event.listen(model, "refresh", restore_utc)
    try:
        async with engine.begin() as db:
            await db.run_sync(
                lambda sync_db: Base.metadata.create_all(
                    sync_db, tables=[model.__table__ for model in MODELS]
                )
            )
        factory = async_sessionmaker(engine, expire_on_commit=False)
        google = ShortsGoogle()
        settings = Settings(next_public_site_url=SITE, video_review_dir=str(tmp_path / "reviews"))
        redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
        monkeypatch.setattr(connection, "get_redis", lambda: redis)
        monkeypatch.setattr(connection, "http_client", google.client_factory())
        for module in (connection, sync, knock, admin_publish_api):
            monkeypatch.setattr(module, "load_runtime_settings", AsyncMock(return_value=settings))
        # A run is awaited by the test that wants it; nothing is left running behind a test.
        launched: list[str] = []
        monkeypatch.setattr(sync, "launch", launched.append)
        monkeypatch.setattr(sync, "BACKOFF_SECONDS", (0.0, 0.0))
        owner = User(id=uuid4(), email="owner@example.test", password_hash="unused", auth_version=1)
        owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
        async with factory() as session:
            session.add(User(id=owner.id, email=owner.email, password_hash="unused"))
            await session.commit()
        yield ShortsSite(factory, google, settings, owner, redis, review_store(settings), launched)
    finally:
        for model in MODELS:
            event.remove(model, "load", restore_utc)
            event.remove(model, "refresh", restore_utc)
        await engine.dispose()
        if administrator is not None:
            async with administrator.begin() as db:
                await db.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
            await administrator.dispose()


@pytest.fixture
async def site(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> AsyncIterator[ShortsSite]:
    async with open_shorts_site(monkeypatch, tmp_path) as value:
        yield value


@pytest.fixture(
    params=["sqlite"] + (["postgresql"] if os.getenv("RUN_INTEGRATION_TESTS") == "1" else [])
)
async def shared_site(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> AsyncIterator[ShortsSite]:
    """The site on SQLite and, where CI runs the integration tests, on PostgreSQL too: for a
    test in which another session writes while the one under test holds its transaction."""
    async with open_shorts_site(monkeypatch, tmp_path, request.param) as value:
        yield value


@pytest.fixture
def now() -> datetime:
    return datetime.now(UTC).replace(microsecond=0)


def _put(store: ReviewStore, slug: str, body: bytes) -> str:
    sha = hashlib.sha256(body).hexdigest()
    store.put_part(slug, sha, index=0, count=1, size=len(body), data=body)
    return sha


def _entry(role: str, sha: str, body: bytes, content_type: str) -> dict[str, Any]:
    return {"role": role, "sha256": sha, "size": len(body), "content_type": content_type}


async def short(
    site: ShortsSite,
    slug: str,
    *,
    line: str = "lab",
    video_id: str | None = None,
    seconds: float = SECONDS,
    approved: timedelta = timedelta(0),
) -> VideoProject:
    """A Short whose cut and upload package are approved, the package in the review store the
    way the Shorts tool sends it: no thumbnail, one caption track, no other language."""
    mp4 = MP4 + slug.encode()
    final_sha = _put(site.store, slug, mp4)
    description = f"{slug} 的說明\n\n#AI #實測\n"
    metadata = json.dumps(
        {
            "schema_version": 1,
            "kind": "shorts",
            "slug": slug,
            "line": line,
            "default_language": "zh-TW",
            "title": f"AI 真的可以？{slug}",
            "titles": [f"AI 真的可以？{slug}", f"{slug} 實測"],
            "description": description,
            "tags": ["AI", "實測"],
            "category_id": "24" if line == "drama" else "28",
            "made_for_kids": False,
            "contains_synthetic_media": line == "drama",
            "duration_seconds": seconds,
            "final_sha256": final_sha,
        },
        ensure_ascii=False,
    ).encode()
    metadata_sha = _put(site.store, slug, metadata)
    captions = SRT + slug.encode()
    moment = datetime.now(UTC) + approved
    project = VideoProject(
        id=uuid4(),
        slug=slug,
        title=f"AI 真的可以？{slug}",
        format="drama" if line == "drama" else "shorts",
        shorts_line=line,
        shorts_series="daily",
        stage="publish",
        checklist=[],
        last_synced_at=moment,
        youtube_video_id=video_id,
    )
    final = VideoReview(
        id=uuid4(),
        project_id=project.id,
        gate="final",
        content_sha256=final_sha,
        summary="成片",
        payload={"duration_seconds": seconds},
        files=[_entry("preview", final_sha, mp4, "video/mp4")],
        status="approved",
        decided_at=moment,
        created_at=moment - timedelta(minutes=2),
        updated_at=moment,
    )
    package = VideoReview(
        id=uuid4(),
        project_id=project.id,
        gate="publish",
        content_sha256=metadata_sha,
        summary="上傳包",
        payload={"package": {"ok": True, "kind": "shorts"}},
        files=[
            _entry("metadata", metadata_sha, metadata, "application/json"),
            _entry("final", final_sha, mp4, "video/mp4"),
            _entry("captions_zh-TW", _put(site.store, slug, captions), captions, "text/plain"),
            _entry(
                "description_zh-TW",
                _put(site.store, slug, description.encode()),
                description.encode(),
                "text/plain",
            ),
        ],
        status="approved",
        decided_at=moment,
        created_at=moment - timedelta(minutes=1),
        updated_at=moment,
    )
    async with site.factory() as session:
        session.add_all([project, final, package])
        await session.commit()
    return project


async def slot(
    site: ShortsSite, starts_at: datetime, slug: str | None = None, status: str = "open"
) -> UUID:
    row = VideoShortsSlot(
        id=uuid4(),
        starts_at=starts_at,
        phase=1,
        status=status,
        project_slug=slug,
        locked_at=datetime.now(UTC) if status == "locked" else None,
    )
    async with site.factory() as session:
        session.add(row)
        await session.commit()
    return row.id


def times_of(now: datetime) -> list[str]:
    """The two times of day these tests publish at: what it is in Taipei 20 and 23 hours from
    now. A slot any number of days after one of them is at a time the owner agreed to."""
    return [f"{(now + hours * HOURS).astimezone(TAIPEI):%H:%M}" for hours in (20, 23)]


async def agree(site: ShortsSite, now: datetime, **settings: Any) -> None:
    """The owner reads the wording for the settings as they are, and agrees to it."""
    async with site.factory() as session:
        row = await shorts_settings.settings_row(session)
        row.slot_times = times_of(now)
        for name, value in settings.items():
            setattr(row, name, value)
        await session.flush()
        channel = await shorts_settings.channel_facts(session)
        offer = shorts_settings.consent_view(row, channel, now).offer
        assert offer is not None
        await shorts_settings.grant_autopublish(session, site.owner, offer.text_sha256, now)


async def ready(
    site: ShortsSite,
    now: datetime,
    *,
    slug: str = "receipt",
    video_id: str = VIDEO,
    hours: int = 20,
) -> UUID:
    """A linked channel, the owner's consent, and a Short on YouTube whose slot is locked, at
    a time of day the consent names."""
    if not connection.linked(await site.connection()):
        await site.link()
        await agree(site, now)
    await short(site, slug, video_id=video_id)
    site.youtube.put(video_id)
    return await slot(site, now + hours * HOURS, slug, "locked")


async def send(site: ShortsSite, now: datetime) -> publish.Sent:
    async with site.factory() as session:
        row = await shorts_settings.settings_row(session)
        channel = await shorts_settings.channel_facts(session)
        return await publish.send_due(
            session, site.store, row, channel, Quota(site.redis, now), now
        )


async def settle(site: ShortsSite, now: datetime) -> int:
    async with site.factory() as session:
        done = await publish.settle(session, now)
        await session.commit()
    return done


async def recall(site: ShortsSite, now: datetime) -> Any:
    async with site.factory() as session, connection.http_client() as http:
        return await publish.recall(session, http, site.owner, Quota(site.redis, now), now)


async def claimed(site: ShortsSite, now: datetime) -> Any:
    async with site.factory() as session, connection.http_client() as http:
        return await claim.claim(session, http, site.owner, Quota(site.redis, now), now)


async def ticked(site: ShortsSite, now: datetime) -> Any:
    async with site.factory() as session:
        return await knock.tick(session, site.redis, now)


async def project_of(site: ShortsSite, slug: str = "receipt") -> VideoProject:
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == slug))
    assert project is not None
    return project


async def slot_of(site: ShortsSite, slot_id: UUID) -> VideoShortsSlot:
    async with site.factory() as session:
        row = await session.get(VideoShortsSlot, slot_id)
    assert row is not None
    return row


async def audits(site: ShortsSite, action: str) -> list[AdminAuditLog]:
    """The entries of one action. Two written in one transaction can carry the same moment,
    so a test that reads several sorts them by what they say."""
    async with site.factory() as session:
        return list(
            await session.scalars(select(AdminAuditLog).where(AdminAuditLog.action == action))
        )


async def change(site: ShortsSite, slug: str, **fields: Any) -> None:
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == slug))
        assert project is not None
        for name, value in fields.items():
            setattr(project, name, value)
        await session.commit()


def request_for(starts_at: datetime, video_id: str = VIDEO) -> dict[str, Any]:
    """The request of a run that schedules a video for this time."""
    return {
        "mode": "studio",
        "visibility": "scheduled",
        "publish_at": starts_at.isoformat(),
        "title": "t",
        "description": "d",
        "video_id": video_id,
        "accept_private_lock": False,
        "review_id": "r",
        "package_sha256": "p",
    }


def finished(starts_at: datetime, status: str = "done", **fields: Any) -> dict[str, Any]:
    """The state a run for this time left behind."""
    state = new_state(request_for(starts_at))
    state.update(status=status, finished_at=datetime.now(UTC).isoformat(), attempts=1)
    state.update(fields)
    return state


# --- what is sent, and when ---------------------------------------------------------------------


async def test_automatic_sync_preserves_the_owner_s_studio_schedule(
    site: ShortsSite, now: datetime
) -> None:
    await ready(site, now)
    assert (await send(site, now)).sent == 1
    chosen = requests.publish_at_text(now + 44 * HOURS)
    site.youtube.videos[VIDEO]["status"]["publishAt"] = chosen

    await sync.run_sync("receipt", site.factory)

    assert site.google.updates == []
    assert site.youtube.videos[VIDEO]["status"]["publishAt"] == chosen
    state = (await project_of(site)).youtube_sync
    assert state is not None and state["status"] == "failed"
    assert "Studio" in state["error"]


async def test_an_explicit_owner_request_can_change_a_studio_schedule(
    site: ShortsSite, now: datetime
) -> None:
    await ready(site, now)
    site.youtube.videos[VIDEO]["status"]["publishAt"] = requests.publish_at_text(now + 44 * HOURS)
    async with site.factory() as session:
        await shorts_settings.set_paused(session, site.owner, True)
        await sync.request_sync(
            session,
            site.store,
            "receipt",
            site.owner,
            PublishIn(
                mode="studio", url=VIDEO, visibility="scheduled", publish_at=now + 20 * HOURS
            ),
        )
    await sync.run_sync("receipt", site.factory)
    chosen = requests.publish_at_text(now + 20 * HOURS)
    assert site.google.updates[-1]["status"]["publishAt"] == chosen


@pytest.mark.parametrize("changed", ["paused", "revoked", "expired", "replaced"])
async def test_queued_automatic_sync_rechecks_its_consent(
    site: ShortsSite, now: datetime, changed: str
) -> None:
    await ready(site, now)
    assert (await send(site, now)).sent == 1
    async with site.factory() as session:
        if changed == "paused":
            await shorts_settings.set_paused(session, site.owner, True)
        elif changed == "revoked":
            await shorts_settings.revoke_autopublish(session, site.owner)
        else:
            row = await shorts_settings.settings_row(session)
            if changed == "expired":
                row.consent_expires_at = datetime.now(UTC) - timedelta(minutes=1)
            else:
                row.consent_id = uuid4()
            await session.commit()

    await sync.run_sync("receipt", site.factory)

    assert site.google.updates == []
    state = (await project_of(site)).youtube_sync
    assert state is not None and state["status"] == "failed"


async def test_automatic_sync_rechecks_pause_after_reading_youtube(
    site: ShortsSite, now: datetime, monkeypatch: pytest.MonkeyPatch
) -> None:
    await ready(site, now)
    assert (await send(site, now)).sent == 1
    original = YoutubeClient.video

    async def pause_after_read(client: YoutubeClient, video_id: str) -> dict[str, Any] | None:
        video = await original(client, video_id)
        async with site.factory() as session:
            await shorts_settings.set_paused(session, site.owner, True)
        return video

    monkeypatch.setattr(YoutubeClient, "video", pause_after_read)
    await sync.run_sync("receipt", site.factory)
    assert site.google.updates == []
    state = (await project_of(site)).youtube_sync
    assert state is not None and state["status"] == "failed"


async def test_automatic_sync_can_finish_the_same_studio_schedule(
    site: ShortsSite, now: datetime
) -> None:
    await ready(site, now)
    when = requests.publish_at_text(now + 20 * HOURS)
    site.youtube.videos[VIDEO]["status"]["publishAt"] = when
    assert (await send(site, now)).sent == 1
    await sync.run_sync("receipt", site.factory)
    assert site.google.updates[-1]["status"]["publishAt"] == when
    state = (await project_of(site)).youtube_sync
    assert state is not None and state["status"] == "done"


async def test_a_locked_short_is_scheduled_for_its_slot_under_the_owner_s_consent(
    site: ShortsSite, now: datetime
) -> None:
    slot_id = await ready(site, now)
    when = now + 20 * HOURS
    assert await send(site, now) == publish.Sent(sent=1, held=0)
    assert site.launched == ["receipt"]
    async with site.factory() as session:
        consent = (await shorts_settings.settings_row(session)).consent_id
    (entry,) = await audits(site, "video_youtube_sync_requested")
    assert entry.actor_user_id == site.owner.id, "the one who gave the consent"
    assert entry.metadata_json["auto"] is True
    assert entry.metadata_json["consent_id"] == str(consent)
    assert (entry.metadata_json["mode"], entry.metadata_json["visibility"]) == (
        "studio",
        "scheduled",
    )
    assert entry.metadata_json["video_id"] == VIDEO
    assert await send(site, now) == publish.Sent(), "the run that is on its way is left to run"

    await sync.run_sync("receipt", site.factory)

    project = await project_of(site)
    assert project.youtube_sync is not None and project.youtube_sync["status"] == "done"
    assert {step["id"]: step["state"] for step in project.youtube_sync["steps"]} == {
        "details": "done",
        "captions": "done",
        "thumbnail": "skipped",
    }
    assert project.youtube_publish_at == when
    (sent,) = site.google.updates
    assert sent["status"]["privacyStatus"] == "private", "YouTube makes it public, at the time"
    assert sent["status"]["publishAt"] == requests.publish_at_text(when)
    assert sent["status"]["selfDeclaredMadeForKids"] is False
    assert sent["status"]["containsSyntheticMedia"] is False
    assert sent["snippet"]["title"] == "AI 真的可以？receipt"
    assert sent["snippet"]["categoryId"] == "28"
    assert sent["snippet"]["defaultLanguage"] == "zh-TW"
    assert sent["localizations"] == {}, "Traditional Chinese only, until the settings add more"
    assert [track["snippet"]["language"] for track in site.google.tracks[VIDEO]] == ["zh-TW"]
    assert site.google.thumbnails == {}, "a Short's cover is its first frame"
    assert "thumbnails.set" not in site.google.calls

    assert (await slot_of(site, slot_id)).status == "locked"
    assert await settle(site, now) == 1
    held = await slot_of(site, slot_id)
    assert (held.status, held.note) == ("scheduled", None)
    async with site.factory() as session:
        view = await admin_service.project_view(session, "receipt")
    assert (view.shorts_state, view.slot_at) == ("scheduled", when)
    assert await send(site, now) == publish.Sent()
    assert len(site.google.updates) == 1
    assert await Quota(site.redis, now).spent() == 501


async def test_a_vertical_drama_short_goes_out_as_entertainment_and_discloses_itself(
    site: ShortsSite, now: datetime
) -> None:
    await site.link()
    await agree(site, now)
    await short(site, "episode-3-cut", line="drama", video_id=VIDEO)
    site.youtube.put(VIDEO)
    await slot(site, now + 20 * HOURS, "episode-3-cut", "locked")
    assert await send(site, now) == publish.Sent(sent=1)
    await sync.run_sync("episode-3-cut", site.factory)
    (sent,) = site.google.updates
    assert sent["snippet"]["categoryId"] == "24"
    assert sent["status"]["containsSyntheticMedia"] is True


async def test_a_short_dropped_while_the_sender_runs_is_not_sent(
    shared_site: ShortsSite, now: datetime, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The sender reads every due Short before its loop and holds them through it. A Short
    the owner drops in that time is caught where the request locks the project, which reads
    it again rather than keeping the values the sender's copy has."""
    site = shared_site
    slot_id = await ready(site, now)
    places = publish._places

    async def meanwhile(
        session: AsyncSession, slots: Sequence[VideoShortsSlot], timezone: str
    ) -> dict[UUID, int]:
        found = await places(session, slots, timezone)
        await change(site, "receipt", dropped_at=now)
        return found

    monkeypatch.setattr(publish, "_places", meanwhile)

    assert await send(site, now) == publish.Sent(held=1)
    assert (await slot_of(site, slot_id)).note == "站主已經放棄這支影片"
    assert site.launched == []
    assert (await project_of(site)).youtube_sync is None


async def no_upload(site: ShortsSite, _now: datetime) -> None:
    await change(site, "receipt", youtube_video_id=None)


async def no_consent(site: ShortsSite, _now: datetime) -> None:
    async with site.factory() as session:
        await shorts_settings.revoke_autopublish(session, site.owner)


async def paused(site: ShortsSite, now: datetime) -> None:
    async with site.factory() as session:
        await shorts_settings.set_paused(session, site.owner, True, now)


async def more_a_day(site: ShortsSite, _now: datetime) -> None:
    async with site.factory() as session:
        row = await shorts_settings.settings_row(session)
        values = shorts_settings.settings_values(row).model_dump()
        await shorts_settings.update_settings(
            session, site.owner, SettingsWrite.model_validate({**values, "max_per_day": 3})
        )


async def expired(site: ShortsSite, now: datetime) -> None:
    async with site.factory() as session:
        row = await shorts_settings.settings_row(session)
        row.consent_expires_at = now - timedelta(minutes=1)
        await session.commit()


async def another_channel(site: ShortsSite, _now: datetime) -> None:
    async with site.factory() as session:
        row = await connection.connection_row(session)
        row.channel_id = "UCsomeoneelse0000000000"
        await session.commit()


async def giver_gone(site: ShortsSite, _now: datetime) -> None:
    async with site.factory() as session:
        row = await shorts_settings.settings_row(session)
        row.consent_by_user_id = uuid4()
        await session.commit()


async def out_of_quota(site: ShortsSite, now: datetime) -> None:
    await Quota(site.redis, now).mark_refused()


async def dropped(site: ShortsSite, now: datetime) -> None:
    await change(site, "receipt", dropped_at=now)


async def grant_lost(site: ShortsSite, _now: datetime) -> None:
    async with site.factory() as session:
        row = await connection.connection_row(session)
        row.problem = connection.LOST_GRANT
        await session.commit()


async def owner_is_sending(site: ShortsSite, now: datetime) -> None:
    state = new_state(request_for(now + 50 * HOURS))
    await change(site, "receipt", youtube_sync=state)


async def owner_chose_another_time(site: ShortsSite, now: datetime) -> None:
    other = now + 50 * HOURS
    await change(site, "receipt", youtube_sync=finished(other), youtube_publish_at=other)


async def a_line_not_agreed_to(site: ShortsSite, now: datetime) -> None:
    """The owner narrowed the run to highlights and agreed to that; the experiment that was
    made before is still in its slot."""
    await agree(site, now, lines=["cut"], weekly_quota={"cut": 2})


async def moved_to_another_time(site: ShortsSite, now: datetime) -> None:
    async with site.factory() as session:
        for row in await session.scalars(select(VideoShortsSlot)):
            row.starts_at = now + 21 * HOURS
        await session.commit()


@pytest.mark.parametrize(
    ("arrange", "reason"),
    [
        (no_upload, publish.WAITS_FOR_UPLOAD),
        (no_consent, "還沒有自動上架授權"),
        (paused, "自動上架暫停中"),
        (more_a_day, "每天上限調高了"),
        (expired, "到期了"),
        (another_channel, "連結的頻道換了"),
        (giver_gone, "已經不在了"),
        (a_line_not_agreed_to, "授權的內容線沒有「實測」"),
        (moved_to_another_time, "不在授權的公開時間裡"),
        (out_of_quota, publish.QUOTA_SPENT),
        (dropped, "放棄"),
        (grant_lost, "重新連結"),
        (owner_is_sending, "正在送 YouTube"),
        (owner_chose_another_time, "網站不改已經排好的時間"),
    ],
    ids=lambda value: getattr(value, "__name__", None),
)
async def test_what_may_not_go_out_waits_and_its_slot_says_why(
    site: ShortsSite, now: datetime, arrange: Arrange, reason: str
) -> None:
    slot_id = await ready(site, now)
    await arrange(site, now)
    assert await send(site, now) == publish.Sent(sent=0, held=1)
    assert site.launched == [] and site.google.updates == []
    held = await slot_of(site, slot_id)
    assert held.status == "locked" and reason in str(held.note)
    assert await audits(site, "video_youtube_sync_requested") == []
    assert await Quota(site.redis, now).spent() == 0


async def test_a_slot_too_close_to_its_time_is_not_sent_any_more(
    site: ShortsSite, now: datetime
) -> None:
    await site.link()
    await agree(site, now)
    await short(site, "receipt", video_id=VIDEO)
    site.youtube.put(VIDEO)
    await slot(site, now + timedelta(minutes=4), "receipt", "locked")
    assert await send(site, now) == publish.Sent()
    assert site.launched == []


SCOPE = {
    "channel_id": CHANNEL,
    "channel_title": "Mokaair",
    "lines": ["lab", "cut"],
    "max_per_day": 2,
    "slot_times": ["12:30", "19:30"],
    "timezone": "Asia/Taipei",
}
EVENING = datetime(2026, 10, 5, 11, 30, tzinfo=UTC)


def test_each_short_is_held_to_what_the_owner_agreed_to() -> None:
    outside = publish.outside_consent
    assert outside(SCOPE, "lab", EVENING, 1) is None
    assert outside(SCOPE, "cut", EVENING - 7 * HOURS, 2) is None, "12:30 in Taipei"
    assert "漫劇直式短篇" in str(outside(SCOPE, "drama", EVENING, 1))
    late = str(outside(SCOPE, "lab", EVENING + timedelta(minutes=1), 1))
    assert "19:31" in late and "12:30、19:30" in late
    # The times are the consent's own: 19:30 in Tokyo is another moment.
    assert outside({**SCOPE, "timezone": "Asia/Tokyo"}, "lab", EVENING, 1) is not None
    assert outside({**SCOPE, "timezone": "Asia/Tokyo"}, "lab", EVENING - HOURS, 1) is None
    assert "一天最多 2 支" in str(outside(SCOPE, "lab", EVENING, 3))
    assert outside(None, "lab", EVENING, 1) == "還沒有自動上架授權"
    assert outside({}, "lab", EVENING, 1) is not None, "a consent that names nothing covers nothing"


async def test_no_more_go_out_in_a_day_than_the_owner_agreed_to(
    site: ShortsSite, now: datetime
) -> None:
    await site.link()
    await agree(site, now, slot_times=["09:00", "10:00", "11:00"], max_per_day=2)
    # Nine in the morning in Taipei, on the day that is thirty hours from now.
    morning = (now + 30 * HOURS).astimezone(TAIPEI).replace(hour=9, minute=0, second=0)
    held: list[UUID] = []
    for index, slug in enumerate(("first", "second", "third")):
        video_id = f"ShortVid00{index + 1}"
        await short(site, slug, video_id=video_id)
        site.youtube.put(video_id)
        held.append(await slot(site, (morning + index * HOURS).astimezone(UTC), slug, "locked"))
    assert await send(site, now) == publish.Sent(sent=2, held=1)
    assert site.launched == ["first", "second"]
    assert "一天最多 2 支" in str((await slot_of(site, held[2])).note)
    assert (await slot_of(site, held[0])).note is None


async def test_a_run_that_fails_is_started_again_three_times_in_all(
    site: ShortsSite, now: datetime
) -> None:
    slot_id = await ready(site, now)
    site.google.refuse["videos.update"] = (500, "backendError")
    for attempt in (1, 2, 3):
        assert await send(site, now) == publish.Sent(sent=1)
        await sync.run_sync("receipt", site.factory)
        project = await project_of(site)
        assert project.youtube_sync is not None
        assert (project.youtube_sync["status"], project.youtube_sync["attempts"]) == (
            "failed",
            attempt,
        )
        assert await settle(site, now) == 0
    assert site.launched == ["receipt"] * 3
    note = str((await slot_of(site, slot_id)).note)
    assert "上一次沒有成功" in note and "backendError" in note
    assert await send(site, now) == publish.Sent(held=1)
    held = await slot_of(site, slot_id)
    assert held.status == "locked" and "送了 3 次都沒有成功" in str(held.note)
    assert site.launched == ["receipt"] * 3, "the fourth knock starts nothing"
    assert len(await audits(site, "video_youtube_sync_requested")) == 1
    retried = await audits(site, "video_youtube_sync_retried")
    assert [entry.metadata_json["auto"] for entry in retried] == [True, True]


async def test_a_quota_refusal_stops_the_day_and_costs_no_attempt(
    site: ShortsSite, now: datetime
) -> None:
    slot_id = await ready(site, now, hours=44)
    site.google.refuse["videos.update"] = (403, "quotaExceeded")
    assert await send(site, now) == publish.Sent(sent=1)
    await sync.run_sync("receipt", site.factory)
    project = await project_of(site)
    assert project.youtube_sync is not None
    assert project.youtube_sync["error"] == publish.QUOTA_ERROR
    # Whatever was tried before, the quota is not the Short's fault.
    await change(site, "receipt", youtube_sync={**project.youtube_sync, "attempts": 5})

    assert await send(site, now) == publish.Sent(held=1)
    assert (await slot_of(site, slot_id)).note == publish.QUOTA_SPENT
    assert await Quota(site.redis, now).refused(), "nothing more is asked of YouTube today"
    assert site.launched == ["receipt"]

    # The quota is a Pacific day's: the day after, the same request is sent once more.
    site.google.refuse.clear()
    tomorrow = now + timedelta(days=1)
    assert await send(site, tomorrow) == publish.Sent(sent=1)
    assert not await Quota(site.redis, tomorrow).refused()
    await sync.run_sync("receipt", site.factory)
    assert await settle(site, tomorrow) == 1
    assert (await slot_of(site, slot_id)).status == "scheduled"


async def test_the_owner_s_own_request_for_the_slot_s_time_is_the_slot_s(
    site: ShortsSite, now: datetime
) -> None:
    slot_id = await ready(site, now)
    when = now + 20 * HOURS
    await change(site, "receipt", youtube_sync=finished(when), youtube_publish_at=when)
    assert await send(site, now) == publish.Sent(), "it is on YouTube's schedule already"
    assert await settle(site, now) == 1
    assert (await slot_of(site, slot_id)).status == "scheduled"
    assert site.launched == []


async def test_a_run_that_is_not_for_this_slot_does_not_mark_it(
    site: ShortsSite, now: datetime
) -> None:
    slot_id = await ready(site, now)
    other = now + 50 * HOURS
    await change(site, "receipt", youtube_sync=finished(other), youtube_publish_at=other)
    assert await settle(site, now) == 0
    await change(site, "receipt", youtube_sync=finished(now + 20 * HOURS, "failed", error="壞了"))
    assert await settle(site, now) == 0
    assert (await slot_of(site, slot_id)).status == "locked"


def test_taking_a_video_off_the_schedule_changes_nothing_else() -> None:
    current = {
        "id": VIDEO,
        "snippet": {
            "title": "標題",
            "description": "說明",
            "tags": ["AI"],
            "categoryId": "28",
            "defaultLanguage": "zh-TW",
            "channelId": CHANNEL,
            "thumbnails": {"default": {}},
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": "2026-10-05T11:30:00Z",
            "embeddable": False,
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": True,
            "uploadStatus": "processed",
        },
        "localizations": {"en": {"title": "t", "description": "d"}},
    }
    body = requests.unschedule_body(current)
    assert body == {
        "id": VIDEO,
        "snippet": {
            "title": "標題",
            "description": "說明",
            "tags": ["AI"],
            "categoryId": "28",
            "defaultLanguage": "zh-TW",
        },
        "status": {
            "privacyStatus": "private",
            "embeddable": False,
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": True,
        },
        # A part that is sent without what it held is emptied, so the languages go back too.
        "localizations": {"en": {"title": "t", "description": "d"}},
    }, "no publish time and no read-only field"
    assert current["status"]["publishAt"] == "2026-10-05T11:30:00Z", "the input is not mutated"
    body["localizations"]["en"]["title"] = "changed"
    assert current["localizations"]["en"]["title"] == "t"
    assert requests.unschedule_body({"id": VIDEO})["localizations"] == {}


# --- the recall ---------------------------------------------------------------------------------


async def scheduled(site: ShortsSite, now: datetime, slug: str, video_id: str, hours: int) -> UUID:
    """A Short the site scheduled on YouTube, its slot marked."""
    slot_id = await ready(site, now, slug=slug, video_id=video_id, hours=hours)
    assert (await send(site, now)).sent == 1
    await sync.run_sync(slug, site.factory)
    assert await settle(site, now) == 1
    return slot_id


async def test_a_recall_takes_what_is_scheduled_off_youtube_and_pauses(
    site: ShortsSite, now: datetime
) -> None:
    first = await scheduled(site, now, "receipt", VIDEO, 20)
    second = await scheduled(site, now, "invoice", "ShortVid002", 44)
    public = await scheduled(site, now, "public", "ShortVid003", 68)
    # A Short whose run finished a moment ago, before any knock marked its slot.
    fresh = await ready(site, now, slug="fresh", video_id="ShortVid004", hours=92)
    assert (await send(site, now)).sent == 1
    await sync.run_sync("fresh", site.factory)
    waiting = await ready(site, now, slug="waiting", video_id="ShortVid005", hours=116)
    site.google.videos["ShortVid003"]["status"] = {"privacyStatus": "public"}
    before = len(site.google.updates)

    answer = await recall(site, now)

    assert answer.recalled == 3
    assert [(item.slug, item.recalled) for item in answer.items] == [
        ("receipt", True),
        ("invoice", True),
        ("public", False),
        ("fresh", True),
    ]
    assert "已經公開" in answer.items[2].detail
    sent = site.google.updates[before:]
    assert [body["id"] for body in sent] == [VIDEO, "ShortVid002", "ShortVid004"]
    for body in sent:
        assert body["status"]["privacyStatus"] == "private"
        assert "publishAt" not in body["status"]
        assert body["snippet"]["title"].startswith("AI 真的可以？"), "the details stay"
        assert body["localizations"] == {}
    assert [(await slot_of(site, each)).status for each in (first, second, public)] == [
        "assigned",
        "assigned",
        "scheduled",
    ]
    assert [(await slot_of(site, each)).status for each in (fresh, waiting)] == [
        "locked",
        "locked",
    ]
    assert (await slot_of(site, first)).note == publish.RECALLED
    assert (await slot_of(site, waiting)).note is None, "nothing of it was on the schedule"
    assert (await project_of(site)).youtube_publish_at is None
    assert (await project_of(site, "public")).youtube_publish_at == now + 68 * HOURS
    async with site.factory() as session:
        row = await shorts_settings.settings_row(session)
        view = await admin_service.project_view(session, "receipt")
    assert row.paused_at == now, "or the next knock would schedule them again"
    assert view.shorts_state == "slotted"
    (entry,) = await audits(site, "video_shorts_recalled")
    assert entry.actor_user_id == site.owner.id
    assert entry.metadata_json == {
        "recalled": ["receipt", "invoice", "fresh"],
        "not_recalled": ["public"],
        "paused": True,
    }
    units = await Quota(site.redis, now).spent()
    assert units == 4 * 501 + 5 * 1 + 3 * 50, "four runs, five reads and three updates"


async def test_what_was_recalled_goes_out_again_once_publishing_is_resumed(
    site: ShortsSite, now: datetime
) -> None:
    slot_id = await scheduled(site, now, "receipt", VIDEO, 20)
    await recall(site, now)
    knocked = await ticked(site, now)
    assert (knocked.locked, knocked.sent, knocked.held) == (1, 0, 1)
    held = await slot_of(site, slot_id)
    assert (held.status, held.note) == ("locked", "自動上架暫停中")

    async with site.factory() as session:
        await shorts_settings.set_paused(session, site.owner, False)
    knocked = await ticked(site, now)
    assert (knocked.sent, knocked.held) == (1, 0)
    await sync.run_sync("receipt", site.factory)
    assert site.google.updates[-1]["status"]["publishAt"] == requests.publish_at_text(
        now + 20 * HOURS
    )
    assert (await ticked(site, now)).scheduled == 1
    assert (await slot_of(site, slot_id)).status == "scheduled"
    assert len(await audits(site, "video_youtube_sync_requested")) == 2


async def test_a_recall_stops_a_run_that_is_on_its_way(site: ShortsSite, now: datetime) -> None:
    slot_id = await ready(site, now)
    assert (await send(site, now)).sent == 1
    answer = await recall(site, now)
    assert (answer.recalled, answer.items) == (0, []), "YouTube had no time to take back"
    project = await project_of(site)
    assert project.youtube_sync is not None
    assert (project.youtube_sync["status"], project.youtube_sync["error"]) == (
        "failed",
        publish.RECALLED,
    )
    await sync.run_sync("receipt", site.factory)
    assert site.google.updates == [], "the run that was queued finds nothing to do"
    assert (await slot_of(site, slot_id)).status == "locked"

    async with site.factory() as session:
        await shorts_settings.set_paused(session, site.owner, False)
    assert await send(site, now) == publish.Sent(sent=1)
    assert len(await audits(site, "video_youtube_sync_requested")) == 2, "a request of its own"
    await sync.run_sync("receipt", site.factory)
    assert await settle(site, now) == 1


async def test_a_recall_says_which_videos_it_could_not_take_back(
    site: ShortsSite, now: datetime
) -> None:
    first = await scheduled(site, now, "receipt", VIDEO, 20)
    await scheduled(site, now, "invoice", "ShortVid002", 44)
    gone = await scheduled(site, now, "gone", "ShortVid003", 68)
    unscheduled = await scheduled(site, now, "studio", "ShortVid004", 92)
    del site.google.videos["ShortVid003"]
    del site.google.videos["ShortVid004"]["status"]["publishAt"]
    site.google.refuse["videos.update"] = (403, "quotaExceeded")

    answer = await recall(site, now)

    assert answer.recalled == 0
    assert [(item.slug, item.recalled) for item in answer.items] == [
        ("receipt", False),
        ("invoice", False),
        ("gone", False),
        ("studio", False),
    ]
    details = [item.detail for item in answer.items]
    assert "配額用完" in details[0]
    assert "再撤回" in details[1] and "再撤回" in details[2], "nothing more was asked today"
    assert site.google.calls.count("videos.update") == 4 + 1
    assert await Quota(site.redis, now).refused()
    assert [(await slot_of(site, each)).status for each in (first, gone, unscheduled)] == [
        "scheduled",
        "scheduled",
        "scheduled",
    ]
    async with site.factory() as session:
        assert (await shorts_settings.settings_row(session)).paused_at == now


async def test_a_video_the_owner_took_off_the_schedule_in_studio_frees_its_slot(
    site: ShortsSite, now: datetime
) -> None:
    slot_id = await scheduled(site, now, "receipt", VIDEO, 20)
    del site.google.videos[VIDEO]["status"]["publishAt"]
    gone = await scheduled(site, now, "gone", "ShortVid002", 44)
    del site.google.videos["ShortVid002"]
    answer = await recall(site, now)
    assert [(item.slug, item.recalled, item.detail) for item in answer.items] == [
        ("receipt", False, "YouTube 上已經沒有排程了"),
        ("gone", False, "YouTube 上找不到這支影片"),
    ]
    assert (await slot_of(site, slot_id)).status == "assigned"
    assert (await slot_of(site, gone)).status == "scheduled"
    assert "videos.update" not in site.google.calls[-3:]


async def test_a_recall_needs_the_channel_and_pauses_even_with_nothing_to_take_back(
    site: ShortsSite, now: datetime
) -> None:
    answer = await recall(site, now)
    assert (answer.recalled, answer.items) == (0, [])
    async with site.factory() as session:
        assert (await shorts_settings.settings_row(session)).paused_at == now
    (entry,) = await audits(site, "video_shorts_recalled")
    assert entry.metadata_json == {"recalled": [], "not_recalled": [], "paused": True}
    assert site.google.calls == [], "YouTube is not asked about nothing"

    await scheduled_without_a_channel(site, now)
    with pytest.raises(ShortsRefused) as refused:
        await recall(site, now)
    assert (refused.value.status, refused.value.code) == (409, "video_shorts_no_channel")


async def scheduled_without_a_channel(site: ShortsSite, now: datetime) -> None:
    await short(site, "receipt", video_id=VIDEO)
    await slot(site, now + 20 * HOURS, "receipt", "scheduled")


# --- the files the owner uploaded ---------------------------------------------------------------


def waiting(slug: str, seconds: float | None = 35.2) -> claim.Waiting:
    return claim.Waiting(
        slug=slug,
        title=slug,
        line="lab",
        slot_at=datetime(2026, 10, 5, 11, 30, tzinfo=UTC),
        seconds=seconds,
        final_sha256="f" * 64,
        size=1024,
    )


def test_an_upload_is_found_by_the_file_name_youtube_kept() -> None:
    name = claim.file_name("receipt-total")
    assert name == "mokaair-short-receipt-total.mp4"
    (found,) = claim.match_uploads(
        [waiting("receipt-total")],
        [upload("OtherVid001", "holiday.mp4"), upload(VIDEO, name)],
        CHANNEL,
        set(),
    )
    assert (found.result, found.youtube_video_id, found.file_name) == ("matched", VIDEO, name)
    # YouTube keeps the name as it was given; the owner's computer may have changed its case.
    (found,) = claim.match_uploads(
        [waiting("receipt-total")], [upload(VIDEO, name.upper())], CHANNEL, set()
    )
    assert found.result == "matched"


def test_without_the_file_name_the_title_studio_made_from_it_is_read() -> None:
    name = claim.file_name("receipt-total")
    (by_title,) = claim.match_uploads(
        [waiting("receipt-total")], [upload(VIDEO, name, kept=False)], CHANNEL, set()
    )
    assert (by_title.result, by_title.youtube_video_id) == ("matched", VIDEO)
    renamed = upload(VIDEO, name)
    renamed["snippet"]["title"] = "我改了標題"
    (kept,) = claim.match_uploads([waiting("receipt-total")], [renamed], CHANNEL, set())
    assert kept.result == "matched", "the file name counts, whatever the title says now"
    titled = upload(VIDEO, "holiday.mp4")
    titled["snippet"]["title"] = "mokaair-short-receipt-total"
    (other,) = claim.match_uploads([waiting("receipt-total")], [titled], CHANNEL, set())
    assert other.result == "not_found", "a file of another name is not the Short's"


@pytest.mark.parametrize(
    ("videos", "result", "video_id", "said"),
    [
        ([], "not_found", None, "沒有這個檔名"),
        ([upload(VIDEO, "mokaair-short-other.mp4")], "not_found", None, "沒有這個檔名"),
        (
            [upload(VIDEO, "mokaair-short-receipt.mp4", channel="UCsomeoneelse0000000000")],
            "not_found",
            None,
            "沒有這個檔名",
        ),
        (
            [upload(VIDEO, "mokaair-short-receipt.mp4", privacy="public")],
            "not_private",
            VIDEO,
            "現在是 public",
        ),
        (
            [upload(VIDEO, "mokaair-short-receipt.mp4", privacy="unlisted")],
            "not_private",
            VIDEO,
            "現在是 unlisted",
        ),
        (
            [upload(VIDEO, "mokaair-short-receipt.mp4", duration="PT52S")],
            "length_differs",
            VIDEO,
            "長 52 秒，成片是 35.2 秒",
        ),
        ([upload(VIDEO, "mokaair-short-receipt.mp4", duration="PT36S")], "matched", VIDEO, ""),
        ([upload(VIDEO, "mokaair-short-receipt.mp4", duration="PT34.2S")], "matched", VIDEO, ""),
        ([upload(VIDEO, "mokaair-short-receipt.mp4", duration="P0D")], "matched", VIDEO, ""),
        (
            [
                upload("NewerVid001", "mokaair-short-receipt.mp4"),
                upload(VIDEO, "mokaair-short-receipt.mp4"),
            ],
            "duplicate",
            "NewerVid001",
            "上傳了 2 次",
        ),
        (
            [
                upload("NewerVid001", "mokaair-short-receipt.mp4", duration="PT52S"),
                upload(VIDEO, "mokaair-short-receipt.mp4"),
            ],
            "duplicate",
            VIDEO,
            "NewerVid001",
        ),
    ],
    ids=[
        "nothing-uploaded",
        "another-short-s-file",
        "on-another-channel",
        "public",
        "unlisted",
        "another-length",
        "a-second-longer",
        "a-second-shorter",
        "length-unread",
        "uploaded-twice",
        "the-newer-one-is-another-file",
    ],
)
def test_what_the_channel_s_uploads_say_of_a_short(
    videos: list[dict[str, Any]], result: str, video_id: str | None, said: str
) -> None:
    (found,) = claim.match_uploads([waiting("receipt")], videos, CHANNEL, set())
    assert (found.result, found.youtube_video_id) == (result, video_id)
    assert said in found.detail


def test_a_video_another_short_has_is_not_given_twice() -> None:
    videos = [upload(VIDEO, "mokaair-short-receipt.mp4")]
    (found,) = claim.match_uploads([waiting("receipt")], videos, CHANNEL, {VIDEO})
    assert found.result == "not_found"
    (unknown,) = claim.match_uploads([waiting("receipt", None)], videos, CHANNEL, set())
    assert unknown.result == "matched", "a cut whose length nobody recorded is not refused for it"


@pytest.mark.parametrize(
    ("text", "seconds"),
    [
        ("PT35S", 35.0),
        ("PT1M2S", 62.0),
        ("PT1H", 3600.0),
        ("PT35.2S", 35.2),
        ("PT0S", 0.0),
        ("P0D", None),
        ("35", None),
        ("", None),
        (None, None),
        (35, None),
    ],
)
def test_youtube_s_durations_are_read_in_seconds(text: object, seconds: float | None) -> None:
    assert claim.duration_seconds(text) == seconds


async def test_i_uploaded_them_gives_the_waiting_shorts_their_videos(
    site: ShortsSite, now: datetime
) -> None:
    await site.link()
    for index, slug in enumerate(("receipt", "invoice", "missing", "public", "long")):
        await short(site, slug)
        await slot(
            site, now + (20 + 24 * index) * HOURS, slug, "locked" if index == 0 else "assigned"
        )
    await short(site, "later")
    await slot(site, now + timedelta(days=11), "later", "assigned")
    await short(site, "library")
    await short(site, "done", video_id="TakenVid001")
    await slot(site, now + 140 * HOURS, "done", "assigned")
    site.youtube.uploads = ["Invoice0002", "Invoice0001", "Public00001", "Long0000001", VIDEO]
    for video_id, name, privacy, duration in (
        (VIDEO, "receipt", "private", "PT35S"),
        ("Invoice0001", "invoice", "private", "PT35S"),
        ("Invoice0002", "invoice", "private", "PT35S"),
        ("Public00001", "public", "public", "PT35S"),
        ("Long0000001", "long", "private", "PT58S"),
    ):
        site.google.videos[video_id] = upload(
            video_id, claim.file_name(name), privacy=privacy, duration=duration
        )

    async with site.factory() as session:
        listed = await claim.uploads_view(session, now)
    assert listed.ahead_days == 10
    assert [item.slug for item in listed.items] == [
        "receipt",
        "invoice",
        "missing",
        "public",
        "long",
    ], "the coming ten days, in the order of their slots; what has a video is not asked for"
    first = listed.items[0]
    assert (first.file_name, first.seconds, first.size, first.line) == (
        "mokaair-short-receipt.mp4",
        SECONDS,
        len(MP4) + len("receipt"),
        "lab",
    )
    assert first.slot_at == now + 20 * HOURS

    answer = await claimed(site, now)

    assert answer.claimed == 2
    assert [(item.slug, item.result, item.youtube_video_id) for item in answer.items] == [
        ("receipt", "matched", VIDEO),
        ("invoice", "duplicate", "Invoice0002"),
        ("missing", "not_found", None),
        ("public", "not_private", "Public00001"),
        ("long", "length_differs", "Long0000001"),
    ]
    assert "Invoice0001" in answer.items[1].detail, "the copy to delete in Studio"
    assert (await project_of(site)).youtube_video_id == VIDEO
    assert (await project_of(site, "invoice")).youtube_video_id == "Invoice0002"
    assert (await project_of(site, "public")).youtube_video_id is None
    assert (await project_of(site, "long")).youtube_video_id is None
    assert site.google.calls[-3:] == ["channels.list", "playlistItems.list", "videos.list"]
    assert site.youtube.asked == [site.youtube.uploads]
    assert await Quota(site.redis, now).spent() == 3
    entries = await audits(site, "video_shorts_upload_claimed")
    assert sorted((entry.metadata_json for entry in entries), key=lambda data: data["slug"]) == [
        {
            "slug": "invoice",
            "youtube_video_id": "Invoice0002",
            "file_name": "mokaair-short-invoice.mp4",
            "result": "duplicate",
        },
        {
            "slug": "receipt",
            "youtube_video_id": VIDEO,
            "file_name": "mokaair-short-receipt.mp4",
            "result": "matched",
        },
    ]
    assert [entry.target for entry in entries if entry.metadata_json["slug"] == "receipt"] == [
        "video_project:receipt"
    ]
    assert {entry.actor_user_id for entry in entries} == {site.owner.id}

    # The second press asks only about what still waits, and never gives a video twice.
    again = await claimed(site, now)
    assert again.claimed == 0
    assert [item.slug for item in again.items] == ["missing", "public", "long"]


async def test_a_video_given_while_the_claim_asks_youtube_is_kept(
    shared_site: ShortsSite, now: datetime, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The claim reads what waits, asks YouTube for seconds, and only then locks each project.
    A Studio sync or a review that gives the Short its video in those seconds must win: the
    locked re-read sees that video and leaves it.

    The claim's session has loaded the project before the wait. SQLAlchemy 2.1.0 to 2.1.3 keep
    what a session iterated alive until the garbage collector runs (sqlalchemy#13639), and a
    re-read keeps the values an object already has unless it is told to populate them again.
    The test holds the loaded project itself, so the outcome depends neither on when the
    collector runs nor on the version."""
    site = shared_site
    await site.link()
    await short(site, "receipt")
    await slot(site, now + 20 * HOURS, "receipt", "locked")
    site.youtube.uploads = [VIDEO]
    site.google.videos[VIDEO] = upload(VIDEO, claim.file_name("receipt"))
    reads_waiting = claim.waiting_uploads
    held: list[VideoProject] = []

    async def meanwhile(
        session: AsyncSession, row: VideoShortsSettings, moment: datetime | None = None
    ) -> list[claim.Waiting]:
        waiting = await reads_waiting(session, row, moment)
        held.extend(
            (
                await session.scalars(select(VideoProject).where(VideoProject.slug == "receipt"))
            ).all()
        )
        await change(site, "receipt", youtube_video_id="StudioVid01")
        return waiting

    monkeypatch.setattr(claim, "waiting_uploads", meanwhile)

    answer = await claimed(site, now)

    assert len(held) == 1
    assert answer.claimed == 0
    assert (await project_of(site)).youtube_video_id == "StudioVid01"
    assert await audits(site, "video_shorts_upload_claimed") == []


async def test_a_claimed_short_is_sent_on_the_next_knock(site: ShortsSite, now: datetime) -> None:
    await site.link()
    await agree(site, now)
    await short(site, "receipt")
    slot_id = await slot(site, now + 20 * HOURS, "receipt", "assigned")
    knocked = await ticked(site, now)
    assert (knocked.locked, knocked.sent, knocked.held) == (1, 0, 1)
    assert (await slot_of(site, slot_id)).note == publish.WAITS_FOR_UPLOAD
    site.youtube.uploads = [VIDEO]
    site.google.videos[VIDEO] = upload(VIDEO, claim.file_name("receipt"))
    assert (await claimed(site, now)).claimed == 1
    knocked = await ticked(site, now)
    assert (knocked.sent, knocked.held) == (1, 0)
    await sync.run_sync("receipt", site.factory)
    assert (await ticked(site, now)).scheduled == 1
    assert site.google.videos[VIDEO]["status"]["publishAt"] == requests.publish_at_text(
        now + 20 * HOURS
    )


async def test_the_claim_asks_youtube_only_when_it_may_and_has_something_to_ask(
    site: ShortsSite, now: datetime
) -> None:
    with pytest.raises(ShortsRefused) as unlinked:
        await claimed(site, now)
    assert (unlinked.value.status, unlinked.value.code) == (409, "video_shorts_no_channel")
    await site.link()
    calls = len(site.google.calls)
    nothing = await claimed(site, now)
    assert (nothing.claimed, nothing.items) == (0, [])
    assert len(site.google.calls) == calls, "nothing waits: nothing is asked"

    await short(site, "receipt")
    await slot(site, now + 44 * HOURS, "receipt", "assigned")
    site.google.refuse["playlistItems.list"] = (403, "quotaExceeded")
    with pytest.raises(ShortsRefused) as spent:
        await claimed(site, now)
    assert (spent.value.status, spent.value.code) == (429, "video_shorts_quota_exhausted")
    assert await Quota(site.redis, now).refused()
    site.google.refuse.clear()
    calls = len(site.google.calls)
    with pytest.raises(ShortsRefused) as still:
        await claimed(site, now)
    assert still.value.code == "video_shorts_quota_exhausted"
    assert len(site.google.calls) == calls, "refused once, YouTube is left alone for the day"

    tomorrow = now + timedelta(days=1)
    site.google.refuse["videos.list"] = (500, "backendError")
    site.youtube.uploads = [VIDEO]
    with pytest.raises(ShortsRefused) as failed:
        await claimed(site, tomorrow)
    assert (failed.value.status, failed.value.code) == (502, "video_shorts_youtube_failed")
    site.google.refuse.clear()
    site.google.refresh_tokens.clear()
    with pytest.raises(ShortsRefused) as lost:
        await claimed(site, tomorrow)
    assert lost.value.code == "video_youtube_grant_lost"
    assert (await project_of(site)).youtube_video_id is None


async def test_the_batch_holds_every_waiting_file_under_the_name_the_claim_looks_for(
    site: ShortsSite, now: datetime, tmp_path: Path
) -> None:
    await short(site, "receipt")
    await short(site, "invoice")
    await slot(site, now + 20 * HOURS, "receipt", "locked")
    await slot(site, now + 44 * HOURS, "invoice", "assigned")
    async with site.factory() as session:
        row = await shorts_settings.settings_row(session)
        waits = await claim.waiting_uploads(session, row, now)
    path = claim.batch_zip(site.store, waits, tmp_path)
    with zipfile.ZipFile(path) as archive:
        assert archive.namelist() == ["mokaair-short-receipt.mp4", "mokaair-short-invoice.mp4"]
        assert archive.read("mokaair-short-receipt.mp4") == MP4 + b"receipt"
        assert {info.compress_type for info in archive.infolist()} == {zipfile.ZIP_STORED}
    with pytest.raises(ShortsRefused) as nothing:
        claim.batch_zip(site.store, [], tmp_path)
    assert (nothing.value.status, nothing.value.code) == (404, "video_shorts_nothing_to_upload")
    site.store.delete_project("receipt")
    site.store.delete_project("invoice")
    with pytest.raises(ShortsRefused):
        claim.batch_zip(site.store, waits, tmp_path)


# --- the knock ----------------------------------------------------------------------------------


async def test_a_knock_does_what_is_due_and_says_how_much(site: ShortsSite, now: datetime) -> None:
    # The daily check is counted per Pacific day; both knocks below must fall on the same one,
    # or a run in the last minutes before Pacific midnight sees the second knock verify again.
    if pacific_day(now + timedelta(minutes=5)) != pacific_day(now):
        now -= timedelta(minutes=10)
    await site.link()
    await agree(site, now)
    await short(site, "receipt", video_id=VIDEO)
    site.youtube.put(VIDEO)
    await short(site, "spare", approved=timedelta(minutes=-5))
    mine = await slot(site, now + 20 * HOURS, "receipt", "assigned")
    empty = await slot(site, now + 23 * HOURS)
    late = await slot(site, now + timedelta(minutes=3), "gone", "assigned")
    ahead = await slot(site, now + 30 * HOURS, None, "open")

    first = await ticked(site, now)

    assert first.model_dump() == {
        "ran": True,
        "skipped": None,
        "locked": 2,
        "missed": 1,
        "sent": 1,
        "held": 1,
        "scheduled": 0,
        "published": 0,
        "snapshots": 0,
        "removed": 0,
        "verified": True,
        "quota_units": 502,
    }
    assert [(await slot_of(site, each)).status for each in (mine, empty, late, ahead)] == [
        "locked",
        "locked",
        "missed",
        "open",
    ]
    filled = await slot_of(site, empty)
    assert filled.project_slug == "spare" and filled.note == publish.WAITS_FOR_UPLOAD
    async with site.factory() as session:
        row = await shorts_settings.settings_row(session)
    assert row.last_tick_at == now
    assert row.last_tick == first.model_dump(mode="json")
    assert await site.redis.get(knock.LOCK_KEY) is None, "the next knock is let in"

    await sync.run_sync("receipt", site.factory)
    later = now + timedelta(minutes=5)
    second = await ticked(site, later)
    assert (second.scheduled, second.locked, second.sent, second.held) == (1, 0, 0, 1)
    assert second.verified is False, "once a day"
    assert second.quota_units == 502
    assert (await slot_of(site, mine)).status == "scheduled"
    async with site.factory() as session:
        assert (await shorts_settings.settings_row(session)).last_tick_at == later
    text = json.dumps(second.model_dump(mode="json"), ensure_ascii=False)
    for secret in ("access-", "refresh-", VIDEO, "receipt", "http"):
        assert secret not in text, "counts and nothing else"


async def test_one_knock_runs_at_a_time(site: ShortsSite, now: datetime) -> None:
    await site.redis.set(knock.LOCK_KEY, "another-knock", ex=60)
    answer = await ticked(site, now)
    assert (answer.ran, answer.skipped) == (False, knock.BUSY)
    assert await site.redis.get(knock.LOCK_KEY) == "another-knock", "its lock is not taken away"
    async with site.factory() as session:
        row = await session.get(VideoShortsSettings, 1)
    assert row is None or row.last_tick_at is None

    await site.redis.delete(knock.LOCK_KEY)
    assert (await ticked(site, now)).ran is True
    assert await site.redis.get(knock.LOCK_KEY) is None


async def test_a_knock_that_fails_lets_the_next_one_in(
    site: ShortsSite, now: datetime, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(knock, "lock_due_slots", AsyncMock(side_effect=RuntimeError("broken")))
    with pytest.raises(RuntimeError):
        await ticked(site, now)
    assert await site.redis.get(knock.LOCK_KEY) is None


async def test_without_redis_the_knock_does_nothing_and_says_so(
    site: ShortsSite, now: datetime
) -> None:
    class Down:
        async def set(self, *_args: Any, **_kwargs: Any) -> bool:
            raise RedisConnectionError("down")

    async with site.factory() as session:
        answer = await knock.tick(session, Down(), now)  # type: ignore[arg-type]
    assert (answer.ran, answer.skipped) == (False, knock.NO_REDIS)


async def test_a_short_that_was_scheduled_while_nobody_knocked_is_not_given_up(
    site: ShortsSite, now: datetime
) -> None:
    await site.link()
    await agree(site, now)
    close = now + timedelta(minutes=3)
    past = now - timedelta(minutes=30)
    await short(site, "close", video_id=VIDEO)
    await short(site, "past", video_id="ShortVid002")
    await short(site, "unsent", video_id="ShortVid003")
    await change(site, "close", youtube_sync=finished(close), youtube_publish_at=close)
    await change(site, "past", youtube_sync=finished(past), youtube_publish_at=past)
    first = await slot(site, close, "close", "locked")
    second = await slot(site, past, "past", "locked")
    third = await slot(site, now + timedelta(minutes=4), "unsent", "locked")
    for video_id in (VIDEO, "ShortVid002"):
        site.youtube.put(video_id, status={"privacyStatus": "private"})

    answer = await ticked(site, now)

    assert (answer.scheduled, answer.missed, answer.sent) == (2, 1, 0)
    assert [(await slot_of(site, each)).status for each in (first, second, third)] == [
        "scheduled",
        "scheduled",
        "missed",
    ]
    async with site.factory() as session:
        view = await admin_service.project_view(session, "unsent")
    assert view.shorts_state == "missed", "back in the library, for the next empty slot"


async def test_past_four_fifths_of_the_quota_the_numbers_wait_and_shorts_still_go_out(
    site: ShortsSite, now: datetime
) -> None:
    slot_id = await ready(site, now)
    public = now - 30 * HOURS
    await short(site, "public", video_id="ShortVid002")
    await change(site, "public", youtube_sync=finished(public), youtube_publish_at=public)
    site.youtube.put(
        "ShortVid002", status={"privacyStatus": "public"}, statistics={"viewCount": "12"}
    )
    quota = Quota(site.redis, now)
    await site.redis.set(quota.units_key, 8000)
    assert not await quota.allows_reading() and await quota.allows_sending()

    answer = await ticked(site, now)

    assert (answer.sent, answer.snapshots) == (1, 0)
    assert site.youtube.asked == [], "the numbers are not what the units are for"
    assert (await slot_of(site, slot_id)).note is None
    await site.redis.set(quota.units_key, 7999)
    assert (await ticked(site, now)).snapshots == 2
    assert site.youtube.asked == [["ShortVid002"]]


async def test_a_lost_grant_stops_the_reading_and_is_said_on_the_card(
    site: ShortsSite, now: datetime
) -> None:
    await site.link()
    public = now - 30 * HOURS
    await short(site, "public", video_id=VIDEO)
    await change(site, "public", youtube_sync=finished(public), youtube_publish_at=public)
    site.youtube.put(VIDEO, status={"privacyStatus": "public"}, statistics={"viewCount": "12"})
    site.google.refresh_tokens.clear()
    answer = await ticked(site, now)
    assert (answer.ran, answer.snapshots, answer.verified) == (True, 0, False)
    assert (await site.connection()).problem == connection.LOST_GRANT
    calls = len(site.google.calls)
    assert (await ticked(site, now + timedelta(minutes=5))).snapshots == 0
    assert len(site.google.calls) == calls, "a grant that is lost is not tried every round"


# --- who may do what ----------------------------------------------------------------------------


def _app(site: ShortsSite, *roles: str, tool: bool = False) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_publish_api.admin_router, prefix="/api/v1")
    app.include_router(admin_publish_api.tool_router, prefix="/api/v1")
    user = User(id=site.owner.id, email="someone@example.test", password_hash="x", auth_version=1)
    user._admin_roles_cache = frozenset(roles)  # type: ignore[attr-defined]

    async def session() -> AsyncIterator[AsyncSession]:
        async with site.factory() as db:
            yield db

    app.dependency_overrides[get_session] = session
    app.dependency_overrides[current_user] = lambda: user
    if tool:
        app.dependency_overrides[speech_api.video_tool] = lambda: VideoToolToken(
            id=uuid4(), name="worker", token_hash="h", token_prefix="mkv_w"
        )
    return app


@pytest.fixture
def routes(site: ShortsSite, monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    limit = AsyncMock()
    monkeypatch.setattr(admin_publish_api, "get_redis", lambda: site.redis)
    monkeypatch.setattr(admin_publish_api, "enforce_named_rate_limit", limit)
    return limit


BASE = "/api/v1/admin/video-shorts/"
KNOCK = "/api/v1/video/automation/shorts/tick"
MANAGE = (("GET", "uploads/batch.zip"), ("POST", "uploads/claim"), ("POST", "recall"))


async def test_every_route_asks_for_its_capability(site: ShortsSite, routes: AsyncMock) -> None:
    async def statuses(*roles: str) -> dict[str, int]:
        transport = ASGITransport(app=_app(site, *roles))
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            return {
                f"{method} {path}": (await client.request(method, BASE + path)).status_code
                for method, path in (("GET", "uploads"), *MANAGE)
            }

    assert set((await statuses()).values()) == {403}
    viewer = await statuses("viewer")
    assert viewer.pop("GET uploads") == 200
    assert set(viewer.values()) == {403}
    assert 403 not in (await statuses("content")).values()
    listed = {
        (method, route.path)  # type: ignore[attr-defined]
        for route in admin_publish_api.admin_router.routes
        for method in route.methods  # type: ignore[attr-defined]
    }
    assert len(listed) == 1 + len(MANAGE), "a new route is added to this test"


async def test_the_knock_takes_the_tool_s_token_and_answers_with_counts(
    site: ShortsSite, routes: AsyncMock
) -> None:
    transport = ASGITransport(app=_app(site, "owner"))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        assert (await client.post(KNOCK)).status_code == 401, "an administrator is not the worker"
    transport = ASGITransport(app=_app(site, tool=True))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        answer = await client.post(KNOCK)
    assert answer.status_code == 200
    body = answer.json()
    assert body["ran"] is True and body["skipped"] is None
    assert set(body) == set(TickOut.model_fields)
    assert all(isinstance(value, bool | int) or value is None for value in body.values())
    routes.assert_awaited_once()
    assert routes.await_args is not None
    assert routes.await_args.kwargs == {"limit": 60, "window_seconds": 3600}


async def test_the_routes_answer_in_the_owner_s_words(
    site: ShortsSite, routes: AsyncMock, now: datetime
) -> None:
    transport = ASGITransport(app=_app(site, "content"))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        empty = await client.get(BASE + "uploads")
        assert empty.json() == {"ahead_days": 10, "items": []}
        nothing = await client.get(BASE + "uploads/batch.zip")
        assert (nothing.status_code, nothing.json()["code"]) == (
            404,
            "video_shorts_nothing_to_upload",
        )
        unlinked = await client.post(BASE + "uploads/claim")
        assert (unlinked.status_code, unlinked.json()["code"]) == (409, "video_shorts_no_channel")
        assert "連結" in unlinked.json()["detail"]

        await site.link()
        await short(site, "receipt")
        await slot(site, now + 20 * HOURS, "receipt", "assigned")
        site.youtube.uploads = [VIDEO]
        site.google.videos[VIDEO] = upload(VIDEO, claim.file_name("receipt"))
        listed = (await client.get(BASE + "uploads")).json()
        assert [item["file_name"] for item in listed["items"]] == ["mokaair-short-receipt.mp4"]
        batch = await client.get(BASE + "uploads/batch.zip")
        assert batch.status_code == 200
        assert batch.headers["content-type"] == "application/zip"
        assert "mokaair-shorts.zip" in batch.headers["content-disposition"]
        assert batch.headers["cache-control"] == "private, no-store"
        with zipfile.ZipFile(io.BytesIO(batch.content)) as archive:
            assert archive.namelist() == ["mokaair-short-receipt.mp4"]
            assert archive.read("mokaair-short-receipt.mp4") == MP4 + b"receipt"
        found = await client.post(BASE + "uploads/claim")
        assert found.status_code == 200 and found.json()["claimed"] == 1
        assert found.json()["items"][0]["youtube_video_id"] == VIDEO
        recalled = await client.post(BASE + "recall")
        assert recalled.status_code == 200
        assert recalled.json() == {"recalled": 0, "items": []}
    async with site.factory() as session:
        assert (await shorts_settings.settings_row(session)).paused_at is not None
