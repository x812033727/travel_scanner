"""The linked YouTube channel: the OAuth client, the grant, and what the site sends YouTube.

docs/videos/HANDS-OFF.md §YouTube API 第一步. ``FakeGoogle`` answers the OAuth endpoints and the
Data API the way the reference pages describe them, so the flows run end to end on a SQLite
database without the network; test_video_youtube_sync.py reuses it for the upload runs.
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from urllib.parse import parse_qs, urlsplit
from uuid import uuid4

import fakeredis.aioredis
import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import current_user
from app.config import Settings
from app.db import Base, get_session
from app.models import (
    AdminAuditLog,
    User,
    VideoProject,
    VideoReview,
    VideoYoutubeConnection,
)
from app.problems import AppError, app_error_handler
from app.video_media.models import VideoMediaJob
from app.video_youtube import admin_api, connection, requests, sync
from app.video_youtube.client import SCOPE, YoutubeError, error_from
from app.video_youtube.errors import Refused
from app.video_youtube.schemas import ClientIn, OAuthExchangeIn, OAuthStartIn
from app.video_youtube.state import new_state, public_state, retried, running

CLIENT_ID = "123456789012-abcdefghijklmnop.apps.googleusercontent.com"
SECRET = "GOCSPX-fixture-secret"  # noqa: S105 -- a fixture value
CHANNEL = "UCfixturechannel0000000"
SITE = "https://mokaair.example"
BINDING = "b" * 43
UPLOADED_ID = "NewUpload01"


# --- a Google that answers like the reference pages ----------------------------------------------


@dataclass
class FakeGoogle:
    """OAuth, channels, videos, captions, thumbnails and resumable uploads, all in memory."""

    refresh_tokens: set[str] = field(default_factory=lambda: {"refresh-1"})
    issued_refresh_token: str = "refresh-1"
    granted_scope: str = SCOPE
    give_refresh_token: bool = True
    channel: dict[str, Any] | None = field(
        default_factory=lambda: {"id": CHANNEL, "snippet": {"title": "Mokaair"}}
    )
    videos: dict[str, dict[str, Any]] = field(default_factory=dict)
    tracks: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    thumbnails: dict[str, bytes] = field(default_factory=dict)
    revoked: list[str] = field(default_factory=list)
    updates: list[dict[str, Any]] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)
    # Upload sessions: uri -> bytes received so far, and the total they will add up to.
    sessions: dict[str, bytearray] = field(default_factory=dict)
    session_bodies: dict[str, dict[str, Any]] = field(default_factory=dict)
    # Chunk PUTs (by count) that fail with a dropped connection, once each.
    drop_chunks: set[int] = field(default_factory=set)
    chunk_count: int = 0
    # reason -> the Data API call that answers it, e.g. {"captions.insert": "quotaExceeded"}.
    refuse: dict[str, tuple[int, str]] = field(default_factory=dict)

    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self.handle)

    def client_factory(self) -> Callable[[], httpx.AsyncClient]:
        return lambda: httpx.AsyncClient(transport=self.transport())

    @staticmethod
    def api_error(status: int, reason: str) -> httpx.Response:
        return httpx.Response(
            status,
            json={"error": {"code": status, "message": reason, "errors": [{"reason": reason}]}},
        )

    def _refused(self, name: str) -> httpx.Response | None:
        self.calls.append(name)
        if name in self.refuse:
            return self.api_error(*self.refuse[name])
        return None

    def handle(self, request: httpx.Request) -> httpx.Response:
        url = request.url
        query = parse_qs(url.query.decode())
        if url.host == "oauth2.googleapis.com":
            form = parse_qs(request.content.decode())
            if url.path == "/revoke":
                self.revoked.append(form["token"][0])
                self.refresh_tokens.clear()
                return httpx.Response(200)
            if form["grant_type"] == ["authorization_code"]:
                self.calls.append("token.code")
                if form["code"] != ["the-code"] or not form.get("code_verifier"):
                    return httpx.Response(400, json={"error": "invalid_grant"})
                body: dict[str, Any] = {"access_token": "access-1", "scope": self.granted_scope}
                if self.give_refresh_token:
                    body["refresh_token"] = self.issued_refresh_token
                    self.refresh_tokens.add(self.issued_refresh_token)
                return httpx.Response(200, json=body)
            self.calls.append("token.refresh")
            if form["refresh_token"][0] not in self.refresh_tokens:
                return httpx.Response(
                    400, json={"error": "invalid_grant", "error_description": "Token revoked"}
                )
            return httpx.Response(200, json={"access_token": "access-2", "expires_in": 3599})
        assert request.headers["authorization"].startswith("Bearer access-")
        path = url.path
        if path == "/youtube/v3/channels":
            refused = self._refused("channels.list")
            return refused or httpx.Response(
                200, json={"items": [self.channel] if self.channel else []}
            )
        if path == "/youtube/v3/videos" and request.method == "GET":
            refused = self._refused("videos.list")
            video = self.videos.get(query["id"][0])
            return refused or httpx.Response(200, json={"items": [video] if video else []})
        if path == "/youtube/v3/videos" and request.method == "PUT":
            refused = self._refused("videos.update")
            if refused:
                return refused
            body = json.loads(request.content)
            self.updates.append(body)
            self.videos[body["id"]].update(body)
            return httpx.Response(200, json=body)
        if path == "/youtube/v3/captions":
            refused = self._refused("captions.list")
            return refused or httpx.Response(
                200, json={"items": self.tracks.get(query["videoId"][0], [])}
            )
        if path == "/upload/youtube/v3/captions":
            refused = self._refused("captions.insert")
            if refused:
                return refused
            boundary = request.headers["content-type"].split("boundary=")[1]
            parts = request.content.split(f"--{boundary}".encode())
            snippet = json.loads(parts[1].split(b"\r\n\r\n", 1)[1].strip())["snippet"]
            track = {"id": uuid4().hex, "snippet": {**snippet, "trackKind": "standard"}}
            self.tracks.setdefault(snippet["videoId"], []).append(track)
            return httpx.Response(200, json=track)
        if path == "/upload/youtube/v3/thumbnails/set":
            refused = self._refused("thumbnails.set")
            if refused:
                return refused
            self.thumbnails[query["videoId"][0]] = request.content
            return httpx.Response(200, json={"items": [{"default": {"url": "x"}}]})
        if path == "/upload/youtube/v3/videos" and request.method == "POST":
            refused = self._refused("videos.insert")
            if refused:
                return refused
            uri = f"https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&upload_id={uuid4().hex}"
            self.sessions[uri] = bytearray()
            self.session_bodies[uri] = json.loads(request.content)
            assert request.headers["x-upload-content-type"] == "video/mp4"
            return httpx.Response(200, headers={"Location": uri})
        if path == "/upload/youtube/v3/videos" and request.method == "PUT":
            return self._chunk(request)
        raise AssertionError(f"unexpected {request.method} {url}")

    def _chunk(self, request: httpx.Request) -> httpx.Response:
        uri = str(request.url)
        received = self.sessions.get(uri)
        if received is None:
            return httpx.Response(404)
        span, _, total = request.headers["content-range"].removeprefix("bytes ").partition("/")
        if span != "*":
            self.chunk_count += 1
            if self.chunk_count in self.drop_chunks:
                self.drop_chunks.discard(self.chunk_count)
                raise httpx.ConnectError("connection dropped", request=request)
            start = int(span.split("-")[0])
            assert start == len(received), "a chunk must continue where the session stands"
            received.extend(request.content)
        if len(received) == int(total):
            body = self.session_bodies[uri]
            video = {
                "id": UPLOADED_ID,
                "snippet": {**body["snippet"], "channelId": CHANNEL},
                "status": {**body["status"], "privacyStatus": "private"},
            }
            self.videos[UPLOADED_ID] = video
            return httpx.Response(200, json=video)
        headers = {"Range": f"bytes=0-{len(received) - 1}"} if received else {}
        return httpx.Response(308, headers=headers)


# --- a database and a site to run on -------------------------------------------------------------


@dataclass
class Site:
    factory: async_sessionmaker[AsyncSession]
    google: FakeGoogle
    settings: Settings
    owner: User
    redis: Any

    async def connection(self) -> VideoYoutubeConnection:
        async with self.factory() as session:
            return await connection.connection_row(session)

    async def link(self) -> None:
        """A channel linked the way the card does it: client saved, flow started and finished."""
        async with self.factory() as session:
            await connection.save_client(
                session, self.owner, ClientIn(client_id=CLIENT_ID, client_secret=SECRET)
            )
        async with self.factory() as session:
            started = await connection.start_link(
                session, self.owner, OAuthStartIn(browser_binding=BINDING)
            )
        async with self.factory() as session:
            await connection.finish_link(
                session,
                self.owner,
                OAuthExchangeIn(
                    flow_id=started.flow_id,
                    state=started.state,
                    code="the-code",
                    browser_binding=BINDING,
                ),
            )


# The video page reads the drama route's spend from the media jobs, so that table is here too.
MODELS = (User, VideoProject, VideoReview, VideoYoutubeConnection, AdminAuditLog, VideoMediaJob)


@asynccontextmanager
async def open_site(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> AsyncIterator[Site]:
    """The database, the fake Google and the patched site; test_video_youtube_sync.py shares it."""
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
    async with engine.begin() as db:
        await db.run_sync(
            lambda sync_db: Base.metadata.create_all(
                sync_db, tables=[model.__table__ for model in MODELS]
            )
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    google = FakeGoogle()
    settings = Settings(next_public_site_url=SITE, video_review_dir=str(tmp_path / "reviews"))
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(connection, "get_redis", lambda: redis)
    monkeypatch.setattr(connection, "http_client", google.client_factory())
    for module in (connection, sync):
        monkeypatch.setattr(module, "load_runtime_settings", AsyncMock(return_value=settings))
    owner = User(id=uuid4(), email="owner@example.test", password_hash="unused", auth_version=1)
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    async with factory() as session:
        session.add(User(id=owner.id, email=owner.email, password_hash="unused"))
        await session.commit()
    yield Site(factory, google, settings, owner, redis)
    for model in MODELS:
        event.remove(model, "load", restore_utc)
        event.remove(model, "refresh", restore_utc)
    await engine.dispose()


@pytest.fixture
async def site(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> AsyncIterator[Site]:
    async with open_site(monkeypatch, tmp_path) as value:
        yield value


# --- what is sent: pure functions ----------------------------------------------------------------


METADATA: dict[str, Any] = {
    "default_language": "zh-TW",
    "category_id": "28",
    "made_for_kids": False,
    "title": "AI 模型怎麼挑",
    "description": "這支影片回答怎麼挑 AI 模型。",
    "tags": ["AI", "模型"],
    "localizations": {
        "en": {"title": "Picking an AI model", "description": "How to pick."},
        "ja": {"title": "AIモデルの選び方", "description": "選び方。"},
        "zh-TW": {"title": "should not be copied", "description": "x"},
    },
    "contains_synthetic_media": False,
}
NOON = datetime(2026, 10, 1, 12, 0, tzinfo=UTC)


def test_the_text_youtube_would_refuse_is_named_in_the_owners_words() -> None:
    assert requests.text_problem("標題", "說明") is None
    assert requests.text_problem(" ", "") == "標題不能空白"
    assert "100" in (requests.text_problem("字" * 101, "") or "")
    assert requests.text_problem("字" * 100, "") is None
    # 5000 bytes, not characters: 1667 three-byte characters are 5001 bytes.
    assert "5000" in (requests.text_problem("t", "字" * 1667) or "")
    assert requests.text_problem("t", "字" * 1666) is None
    assert "<" in (requests.text_problem("a <b>", "") or "")
    assert ">" in (requests.text_problem("a", "b > c") or "")


def test_an_update_keeps_what_the_video_has_and_replaces_only_what_the_site_owns() -> None:
    current = {
        "id": "vid00000001",
        "snippet": {
            "title": "final",
            "description": "",
            "categoryId": "22",
            "channelId": CHANNEL,
            "thumbnails": {"default": {}},
            "defaultLanguage": "en",
        },
        "status": {
            "privacyStatus": "private",
            "embeddable": False,
            "license": "creativeCommon",
            "uploadStatus": "processed",
        },
        "localizations": {"ko": {"title": "k", "description": "d"}, "zh-TW": {"title": "old"}},
    }
    body = requests.update_body(
        current,
        METADATA,
        title="改過的標題",
        description="改過的說明",
        visibility="scheduled",
        publish_at=NOON,
    )
    assert body["id"] == "vid00000001"
    assert body["snippet"] == {
        "title": "改過的標題",
        "description": "改過的說明",
        "tags": ["AI", "模型"],
        "categoryId": "28",
        "defaultLanguage": "zh-TW",
        "defaultAudioLanguage": "zh-TW",
    }
    # The owner's own settings on the video survive; read-only fields are not sent back.
    assert body["status"] == {
        "privacyStatus": "private",
        "embeddable": False,
        "license": "creativeCommon",
        "selfDeclaredMadeForKids": False,
        "containsSyntheticMedia": False,
        "publishAt": "2026-10-01T12:00:00Z",
    }
    assert body["localizations"] == {
        "ko": {"title": "k", "description": "d"},
        "en": {"title": "Picking an AI model", "description": "How to pick."},
        "ja": {"title": "AIモデルの選び方", "description": "選び方。"},
    }
    assert current["localizations"]["zh-TW"] == {"title": "old"}, "the input is not mutated"


@pytest.mark.parametrize("visibility", ["unlisted", "private"])
def test_without_a_schedule_the_publish_time_goes_and_the_site_never_says_public(
    visibility: str,
) -> None:
    current = {
        "id": "v",
        "status": {"privacyStatus": "private", "publishAt": "2026-10-02T00:00:00Z"},
    }
    body = requests.update_body(
        current, METADATA, title="t", description="d", visibility=visibility, publish_at=None
    )
    assert body["status"]["privacyStatus"] == visibility
    assert "publishAt" not in body["status"]
    with pytest.raises(ValueError):
        requests.update_body(
            current, METADATA, title="t", description="d", visibility="scheduled", publish_at=None
        )


def test_the_upload_itself_is_private_with_no_time_and_carries_the_disclosure() -> None:
    body = requests.insert_body({**METADATA, "contains_synthetic_media": True}, "t", "d")
    assert body["status"] == {
        "privacyStatus": "private",
        "selfDeclaredMadeForKids": False,
        "containsSyntheticMedia": True,
    }
    assert body["snippet"]["categoryId"] == "28"
    assert body["snippet"]["defaultLanguage"] == "zh-TW"
    assert requests.insert_body({"title": "t"}, "t", "d")["snippet"]["categoryId"] == "28"


def test_automatic_tracks_do_not_count_and_language_tags_are_compared_loosely() -> None:
    tracks: list[dict[str, Any]] = [
        {"snippet": {"language": "zh-TW", "trackKind": "asr"}},
        {"snippet": {"language": "en", "trackKind": "standard"}},
        {"snippet": {"language": "zh-Hans", "trackKind": "standard"}},
        {"snippet": {}},
    ]
    assert requests.caption_languages(tracks) == {"en", "zh-cn"}
    assert requests.language_key("zh_TW") == "zh-tw"
    assert requests.language_key("zh-Hant") == "zh-tw"


def test_a_package_file_role_names_its_locale_in_either_spelling() -> None:
    locales = ["zh-TW", "zh-CN", "en"]
    assert requests.locale_of_role("captions_zh-TW", "captions_", locales) == "zh-TW"
    assert requests.locale_of_role("captions_zh_cn", "captions_", locales) == "zh-CN"
    assert requests.locale_of_role("captions_ko", "captions_", locales) == "ko"


def test_google_errors_are_read_in_both_shapes() -> None:
    data_api = error_from(FakeGoogle.api_error(403, "quotaExceeded"))
    assert (data_api.status, data_api.reason) == (403, "quotaExceeded")
    oauth = error_from(httpx.Response(400, json={"error": "invalid_grant"}))
    assert (oauth.reason, type(oauth).__name__) == ("invalid_grant", "AuthorizationLost")
    assert error_from(httpx.Response(502, text="<html>")).reason == "error"
    assert isinstance(data_api, YoutubeError)


def test_the_sync_state_hides_its_bookkeeping_and_knows_an_interrupted_run() -> None:
    state = new_state({"mode": "studio", "visibility": "private", "title": "t", "review_id": "r"})
    assert [item["id"] for item in state["steps"]] == ["details", "captions", "thumbnail"]
    assert running(state)
    view = public_state(state)
    assert view is not None and "review_id" not in view["request"] and "lease_until" not in view
    old = datetime.now(UTC) - timedelta(minutes=10)
    stuck = {**state, "status": "running", "lease_until": old.isoformat()}
    assert not running(stuck)
    assert public_state(stuck)["interrupted"] is True  # type: ignore[index]
    stuck["steps"][0]["state"] = "done"
    again = retried(stuck)
    assert again["status"] == "queued" and again["steps"][0]["state"] == "done"
    assert public_state(None) is None


# --- linking the channel -------------------------------------------------------------------------


async def test_the_card_starts_with_the_redirect_uri_to_register_and_nothing_linked(
    site: Site,
) -> None:
    async with site.factory() as session:
        view = await connection.connection_view(session)
    assert view.redirect_uri == f"{SITE}/api/admin-video-youtube/callback"
    assert (view.configured, view.linked, view.client_secret_set, view.audited) == (
        False,
        False,
        False,
        False,
    )
    assert view.scope == SCOPE


async def test_the_client_secret_is_stored_encrypted_and_never_shown(site: Site) -> None:
    async with site.factory() as session:
        view = await connection.save_client(
            session, site.owner, ClientIn(client_id=CLIENT_ID, client_secret=SECRET, audited=True)
        )
    assert view.client_secret_set and view.configured and view.audited
    assert SECRET not in view.model_dump_json()
    row = await site.connection()
    assert row.secret_config_encrypted and SECRET not in row.secret_config_encrypted
    # A null secret keeps the stored one.
    async with site.factory() as session:
        view = await connection.save_client(session, site.owner, ClientIn(client_id=CLIENT_ID))
    assert view.client_secret_set and view.audited is False
    async with site.factory() as session:
        actions = (await session.scalars(select(AdminAuditLog.action))).all()
    assert actions == ["video_youtube_client_saved", "video_youtube_client_saved"]


def test_the_client_id_must_look_like_a_google_web_client() -> None:
    with pytest.raises(ValueError):
        ClientIn(client_id="not-a-client", client_secret=SECRET)
    with pytest.raises(ValueError):
        ClientIn(client_id=CLIENT_ID, client_secret="has space in it")


async def test_linking_needs_the_client_first(site: Site) -> None:
    async with site.factory() as session:
        with pytest.raises(Refused) as refused:
            await connection.start_link(session, site.owner, OAuthStartIn(browser_binding=BINDING))
    assert refused.value.code == "video_youtube_client_missing"


async def test_the_authorization_url_asks_for_one_scope_offline_with_pkce(site: Site) -> None:
    async with site.factory() as session:
        await connection.save_client(
            session, site.owner, ClientIn(client_id=CLIENT_ID, client_secret=SECRET)
        )
    async with site.factory() as session:
        started = await connection.start_link(
            session, site.owner, OAuthStartIn(browser_binding=BINDING)
        )
    url = urlsplit(started.authorization_url)
    params = {key: values[0] for key, values in parse_qs(url.query).items()}
    assert (
        f"{url.scheme}://{url.netloc}{url.path}" == "https://accounts.google.com/o/oauth2/v2/auth"
    )
    assert params["scope"] == SCOPE
    assert params["access_type"] == "offline"
    assert params["prompt"] == "select_account consent"
    assert params["redirect_uri"] == f"{SITE}/api/admin-video-youtube/callback"
    assert params["code_challenge_method"] == "S256"
    assert params["state"] == started.state
    stored = json.loads(await site.redis.get(connection.FLOW_KEY.format(started.flow_id)))
    assert BINDING not in json.dumps(stored), "only the binding's hash is kept"


async def test_finishing_the_link_keeps_the_grant_and_reads_the_channel(site: Site) -> None:
    await site.link()
    row = await site.connection()
    assert (row.channel_id, row.channel_title, row.scope) == (CHANNEL, "Mokaair", SCOPE)
    assert "refresh-1" not in (row.secret_config_encrypted or "")
    assert connection.stored_secrets(row)["refresh_token"] == "refresh-1"
    async with site.factory() as session:
        view = await connection.connection_view(session)
    assert view.linked and view.channel_url == f"https://www.youtube.com/channel/{CHANNEL}"
    assert "refresh-1" not in view.model_dump_json()


async def test_reconnecting_replaces_the_token_without_revoking_the_new_grant(site: Site) -> None:
    await site.link()
    site.google.issued_refresh_token = "refresh-2"
    async with site.factory() as session:
        started = await connection.start_link(
            session, site.owner, OAuthStartIn(browser_binding=BINDING)
        )
    async with site.factory() as session:
        await connection.finish_link(
            session,
            site.owner,
            OAuthExchangeIn(
                flow_id=started.flow_id,
                state=started.state,
                code="the-code",
                browser_binding=BINDING,
            ),
        )
    assert site.google.revoked == [], "revoking the old token also invalidates the new grant"
    assert connection.stored_secrets(await site.connection())["refresh_token"] == "refresh-2"
    async with site.factory() as session:
        verified = await connection.verify(session)
    assert verified.linked and verified.problem is None


async def test_a_flow_is_good_once_and_only_in_the_browser_that_started_it(site: Site) -> None:
    async with site.factory() as session:
        await connection.save_client(
            session, site.owner, ClientIn(client_id=CLIENT_ID, client_secret=SECRET)
        )
    async with site.factory() as session:
        started = await connection.start_link(
            session, site.owner, OAuthStartIn(browser_binding=BINDING)
        )
    exchange = OAuthExchangeIn(
        flow_id=started.flow_id, state=started.state, code="the-code", browser_binding="c" * 43
    )
    async with site.factory() as session:
        with pytest.raises(Refused) as refused:
            await connection.finish_link(session, site.owner, exchange)
    assert refused.value.code == "video_youtube_state_invalid"
    # The flow was consumed by the failed attempt: the right binding cannot use it afterwards.
    async with site.factory() as session:
        with pytest.raises(Refused):
            await connection.finish_link(
                session, site.owner, exchange.model_copy(update={"browser_binding": BINDING})
            )
    assert "token.code" not in site.google.calls


async def test_a_grant_without_the_youtube_scope_or_without_a_channel_is_refused(
    site: Site,
) -> None:
    site.google.granted_scope = "openid"
    with pytest.raises(Refused) as refused:
        await site.link()
    assert refused.value.code == "video_youtube_scope_missing"
    site.google.granted_scope = SCOPE
    site.google.channel = None
    with pytest.raises(Refused) as refused:
        await site.link()
    assert refused.value.code == "video_youtube_no_channel"
    assert site.google.revoked == ["refresh-1"], "a grant with no channel is given back"
    assert not connection.linked(await site.connection())


async def test_the_client_cannot_change_under_a_linked_channel(site: Site) -> None:
    await site.link()
    other = "999999999999-zzzzzzzzzzzzzzzz.apps.googleusercontent.com"
    async with site.factory() as session:
        with pytest.raises(Refused) as refused:
            await connection.save_client(session, site.owner, ClientIn(client_id=other))
    assert refused.value.code == "video_youtube_client_in_use"


async def test_a_stale_check_reads_the_channel_again_and_a_revoked_grant_says_so(
    site: Site,
) -> None:
    await site.link()
    async with site.factory() as session:
        row = await connection.connection_row(session)
        row.verified_at = datetime.now(UTC) - timedelta(days=26)
        await session.commit()
    site.google.channel = {"id": CHANNEL, "snippet": {"title": "Mokaair 頻道"}}
    async with site.factory() as session:
        view = await connection.connection_view(session)
    assert view.channel_title == "Mokaair 頻道"
    assert view.verified_at and view.verified_at > datetime.now(UTC) - timedelta(minutes=1)
    # The owner removed the access in their Google account.
    site.google.refresh_tokens.clear()
    async with site.factory() as session:
        view = await connection.verify(session)
    assert view.problem == connection.LOST_GRANT


async def test_unlinking_revokes_the_grant_and_forgets_it(site: Site) -> None:
    await site.link()
    async with site.factory() as session:
        revoked, view = await connection.unlink(session, site.owner)
    assert revoked and not view.linked and view.channel_title is None
    assert site.google.revoked == ["refresh-1"]
    row = await site.connection()
    assert "refresh_token" not in connection.stored_secrets(row)
    assert connection.stored_secrets(row)["client_secret"] == SECRET, "the client stays"


# --- who may do what -----------------------------------------------------------------------------


def _app(roles: set[str], site: Site) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.connection_router, prefix="/api/v1")
    app.include_router(admin_api.publish_router, prefix="/api/v1")
    user = User(id=site.owner.id, email="someone@example.test", password_hash="x", auth_version=1)
    user._admin_roles_cache = frozenset(roles)  # type: ignore[attr-defined]

    async def session() -> AsyncIterator[AsyncSession]:
        async with site.factory() as db:
            yield db

    app.dependency_overrides[get_session] = session
    app.dependency_overrides[current_user] = lambda: user
    return app


async def test_a_content_reviewer_reads_the_card_but_cannot_link_or_unlink(site: Site) -> None:
    transport = ASGITransport(app=_app({"content"}, site))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        read = await client.get("/api/v1/admin/video-youtube")
        start = await client.post(
            "/api/v1/admin/video-youtube/oauth/start", json={"browser_binding": BINDING}
        )
        unlink = await client.post("/api/v1/admin/video-youtube/unlink")
        save = await client.put(
            "/api/v1/admin/video-youtube", json={"client_id": CLIENT_ID, "client_secret": SECRET}
        )
    assert read.status_code == 200 and read.json()["linked"] is False
    assert (start.status_code, unlink.status_code, save.status_code) == (403, 403, 403)


async def test_the_owner_links_through_the_routes_and_refusals_carry_their_code(
    site: Site,
) -> None:
    transport = ASGITransport(app=_app({"owner"}, site))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        early = await client.post(
            "/api/v1/admin/video-youtube/oauth/start", json={"browser_binding": BINDING}
        )
        saved = await client.put(
            "/api/v1/admin/video-youtube", json={"client_id": CLIENT_ID, "client_secret": SECRET}
        )
        start = await client.post(
            "/api/v1/admin/video-youtube/oauth/start", json={"browser_binding": BINDING}
        )
        finished = await client.post(
            "/api/v1/admin/video-youtube/oauth/exchange",
            json={
                "flow_id": start.json()["flow_id"],
                "state": start.json()["state"],
                "code": "the-code",
                "browser_binding": BINDING,
            },
        )
        unlinked = await client.post("/api/v1/admin/video-youtube/unlink")
    assert (early.status_code, early.json()["code"]) == (409, "video_youtube_client_missing")
    assert saved.status_code == 200 and "client_secret" not in saved.json()
    assert finished.status_code == 200 and finished.json()["channel_title"] == "Mokaair"
    assert unlinked.json()["revoked"] is True and unlinked.json()["connection"]["linked"] is False
