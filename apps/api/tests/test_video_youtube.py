"""The site's side of YouTube: the connection, what it sends for a video, and the routes."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from urllib.parse import parse_qs, urlsplit
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.admin.service import decrypt_secrets, encrypt_secrets
from app.auth.service import current_user
from app.config import Settings
from app.db import get_session
from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoYoutubeChannel
from app.problems import AppError, app_error_handler
from app.video_reviews import admin_service as reviews
from app.video_reviews.schemas import ProjectOut
from app.video_reviews.storage import ReviewStore
from app.video_youtube import admin_api, oauth, service, sync
from app.video_youtube.client import YouTubeError
from app.video_youtube.schemas import SyncReason

NOON = datetime(2026, 9, 27, 12, tzinfo=UTC)
TOMORROW = NOON + timedelta(days=1)
SETTINGS = Settings(
    youtube_oauth_client_id="client-id.apps.googleusercontent.com",
    youtube_oauth_client_secret="client-secret",  # noqa: S106 -- a test fixture
    next_public_site_url="https://mokaair.com/",
)


class FakeRedis:
    """The two calls the consent flow makes, over a dict."""

    def __init__(self) -> None:
        self.data: dict[str, str] = {}
        self.ttl: dict[str, int] = {}

    async def set(self, key: str, value: str, ex: int | None = None) -> None:
        self.data[key] = value
        if ex is not None:
            self.ttl[key] = ex

    async def getdel(self, key: str) -> str | None:
        self.ttl.pop(key, None)
        return self.data.pop(key, None)


def _choices(**locales: dict[str, bool]) -> Any:
    return reviews.locale_choices(VideoProject(slug="v", title="t", stage="s", locales=locales))


# --- the bodies, as pure functions -----------------------------------------------------------


def test_the_update_body_merges_the_current_video_with_the_package_and_keeps_it_private() -> None:
    current = {
        "snippet": {
            "title": "old",
            "description": "old",
            "channelId": "UC1",  # read-only: never sent back
            "publishedAt": "2026-09-01T00:00:00Z",
            "tags": ["old"],
            "categoryId": "22",
            "defaultAudioLanguage": "zh-Hant",
        },
        "status": {
            "privacyStatus": "private",
            "uploadStatus": "processed",  # read-only
            "license": "creativeCommon",
            "embeddable": False,
            "publicStatsViewable": True,
        },
        "localizations": {"fr": {"title": "vieux", "description": "d"}},
    }
    metadata = {
        "title": "新標題",
        "description": "新說明",
        "tags": ["Claude Code", "克勞德"],
        "category_id": 28,
        "contains_synthetic_media": True,
        "localizations": {
            "en": {"title": "New", "description": "Desc"},
            "ja": {"title": "新しい", "description": "説明"},
        },
    }
    body = sync.update_body(
        video_id="dQw4w9WgXcQ",
        current=current,
        metadata=metadata,
        locales=["en"],
        publish_at=TOMORROW,
    )
    assert body["id"] == "dQw4w9WgXcQ"
    assert body["snippet"] == {
        "title": "新標題",
        "description": "新說明",
        "tags": ["Claude Code", "克勞德"],
        "categoryId": "28",
        "defaultLanguage": "zh-TW",
        "defaultAudioLanguage": "zh-Hant",
    }, "writable fields only, the package's zh-TW values, the audio language as it was"
    assert body["status"] == {
        "license": "creativeCommon",
        "embeddable": False,
        "publicStatsViewable": True,
        "privacyStatus": "private",
        "selfDeclaredMadeForKids": False,
        "containsSyntheticMedia": True,
        "publishAt": "2026-09-28T12:00:00Z",
    }
    assert body["localizations"] == {
        "fr": {"title": "vieux", "description": "d"},
        "en": {"title": "New", "description": "Desc"},
    }, "the chosen language is added over what is there; ja was not chosen"

    unscheduled = sync.update_body(
        video_id="dQw4w9WgXcQ", current={}, metadata={"title": "t"}, locales=[], publish_at=None
    )
    assert "publishAt" not in unscheduled["status"], "no time given, none sent"
    assert unscheduled["status"]["privacyStatus"] == "private"
    assert unscheduled["status"]["containsSyntheticMedia"] is False
    assert unscheduled["snippet"]["categoryId"] == "28", "Science & Technology by default"
    assert unscheduled["snippet"]["defaultAudioLanguage"] == "zh-TW"
    assert unscheduled["localizations"] == {}


def test_only_the_chosen_and_translated_languages_go_up_in_page_order() -> None:
    choices = _choices(
        ko={"metadata": True, "captions": True},
        en={"metadata": True},
        ja={"captions": True},
        **{"zh-CN": {"metadata": True}},
    )
    metadata = {"localizations": {"en": {}, "ko": {}, "ja": {}}}
    assert sync.description_locales(choices, metadata) == ["en", "ko"], (
        "ja has no titles chosen, zh-CN was chosen but the package has no translation"
    )
    files = {"metadata", "captions_zh-TW", "captions_ko", "captions_ja", "captions_en"}
    assert sync.caption_locales(choices, files) == ["zh-TW", "ja", "ko"], (
        "zh-TW first, then the chosen caption languages the package holds; en had no CC chosen"
    )
    assert sync.caption_locales(choices, {"captions_ko"}) == ["ko"], "no zh-TW file, none sent"
    assert sync.caption_locales({}, set()) == []


def test_the_publish_time_is_refused_on_a_video_that_is_not_private_or_a_time_gone_by() -> None:
    assert sync.schedule_problem({"privacyStatus": "private"}, TOMORROW, NOON) is None
    assert "unlisted" in str(sync.schedule_problem({"privacyStatus": "unlisted"}, TOMORROW, NOON))
    assert "不是私人" in str(sync.schedule_problem({}, TOMORROW, NOON))
    assert "已經過了" in str(sync.schedule_problem({"privacyStatus": "private"}, NOON, NOON))


def test_a_retry_uploads_only_the_caption_tracks_youtube_lacks() -> None:
    listed = [
        {"snippet": {"language": "zh-TW", "name": "zh-TW"}},
        {"snippet": {"language": "EN", "name": "English"}},
        {"snippet": {}},
        "junk",
    ]
    assert sync.existing_caption_languages(listed) == {"zh-tw", "en"}  # type: ignore[arg-type]
    assert sync.missing_captions(listed, ["zh-TW", "en", "ja"]) == ["ja"]  # type: ignore[arg-type]
    assert sync.missing_captions([], ["zh-TW"]) == ["zh-TW"]


def test_a_caption_upload_is_one_multipart_related_body() -> None:
    metadata = sync.caption_metadata("dQw4w9WgXcQ", "ja")
    assert metadata == {
        "snippet": {"videoId": "dQw4w9WgXcQ", "language": "ja", "name": "ja", "isDraft": False}
    }
    body, boundary = sync.multipart_related(
        metadata, b"1\n00:00:00,000 --> 00:00:01,000\nx\n", "text/plain"
    )
    assert body.startswith(f"--{boundary}\r\nContent-Type: application/json".encode())
    assert body.count(f"--{boundary}".encode()) == 3 and body.endswith(
        f"--{boundary}--\r\n".encode()
    )
    assert json.dumps(metadata, ensure_ascii=False).encode() in body
    assert b"Content-Type: text/plain\r\n\r\n1\n00:00:00,000" in body


def test_the_browser_only_goes_back_to_a_site_path() -> None:
    assert oauth.safe_next("/admin/videos?tab=settings") == "/admin/videos?tab=settings"
    assert oauth.safe_next("https://evil.example/") == "/"
    assert oauth.safe_next("//evil.example/") == "/"
    assert oauth.safe_next("/a\\b") == "/"
    assert oauth.safe_next("  ") == "/"
    assert oauth.callback_url(SETTINGS) == (
        "https://mokaair.com/api/travel/admin/video-youtube/connection/callback"
    )


# --- the consent flow -----------------------------------------------------------------------


def _owner() -> User:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    return owner


@pytest.mark.asyncio
async def test_connecting_needs_the_provider_card_client_and_asks_google_for_offline_access() -> (
    None
):
    redis = FakeRedis()
    owner = _owner()
    with pytest.raises(AppError) as refused:
        await oauth.start(redis, Settings(), owner, "/")  # type: ignore[arg-type]
    assert refused.value.status == 409 and refused.value.code == "video_youtube_not_configured"
    assert redis.data == {}

    started = await oauth.start(redis, SETTINGS, owner, "/admin/videos?tab=settings")  # type: ignore[arg-type]
    url = urlsplit(started.authorization_url)
    query = parse_qs(url.query)
    assert f"{url.scheme}://{url.netloc}{url.path}" == oauth.AUTHORIZE
    assert query["client_id"] == ["client-id.apps.googleusercontent.com"]
    assert query["redirect_uri"] == [oauth.callback_url(SETTINGS)]
    assert query["scope"] == [oauth.SCOPE] and query["access_type"] == ["offline"]
    assert query["prompt"] == ["consent"] and query["code_challenge_method"] == ["S256"]
    (state,) = query["state"]
    kept = json.loads(redis.data[f"{oauth.FLOW_KEY}{state}"])
    assert kept["user_id"] == str(owner.id) and kept["next"] == "/admin/videos?tab=settings"
    assert redis.ttl[f"{oauth.FLOW_KEY}{state}"] == oauth.FLOW_TTL_SECONDS == started.expires_in
    assert query["code_challenge"] == [oauth._challenge(kept["verifier"])]  # noqa: SLF001


def _google(
    calls: list[httpx.Request], *, refresh: str | None = "refresh-1", scope: str = oauth.SCOPE
) -> httpx.MockTransport:
    def handle(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if str(request.url) == oauth.TOKEN:
            body: dict[str, Any] = {"access_token": "access-1", "scope": scope, "expires_in": 3599}
            if refresh:
                body["refresh_token"] = refresh
            return httpx.Response(200, json=body)
        if str(request.url).startswith(oauth.CHANNELS):
            return httpx.Response(
                200, json={"items": [{"id": "UCabc", "snippet": {"title": "Mokaair"}}]}
            )
        if str(request.url) == oauth.REVOKE:
            return httpx.Response(200, json={})
        return httpx.Response(404, json={"error": {"message": "no such route"}})

    return httpx.MockTransport(handle)


@pytest.mark.asyncio
async def test_the_callback_keeps_the_refresh_token_encrypted_with_the_channel_it_opens() -> None:
    redis = FakeRedis()
    owner = _owner()
    started = await oauth.start(redis, SETTINGS, owner, "/admin/videos?tab=settings")  # type: ignore[arg-type]
    state = parse_qs(urlsplit(started.authorization_url).query)["state"][0]
    verifier = json.loads(redis.data[f"{oauth.FLOW_KEY}{state}"])["verifier"]
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    session.add = MagicMock()
    calls: list[httpx.Request] = []
    async with httpx.AsyncClient(transport=_google(calls)) as http:
        next_path = await oauth.finish(
            session,
            redis,  # type: ignore[arg-type]
            http,
            SETTINGS,
            owner,
            code="code-1",
            state=state,
            now=NOON,
        )
    assert next_path == "/admin/videos?tab=settings"
    exchanged = parse_qs(calls[0].content.decode())
    assert exchanged["code"] == ["code-1"] and exchanged["code_verifier"] == [verifier]
    assert exchanged["grant_type"] == ["authorization_code"]
    assert exchanged["redirect_uri"] == [oauth.callback_url(SETTINGS)]
    assert calls[1].headers["Authorization"] == "Bearer access-1"
    row, audit = (call.args[0] for call in session.add.call_args_list)
    assert isinstance(row, VideoYoutubeChannel)
    assert row.channel_id == "UCabc" and row.channel_title == "Mokaair"
    assert row.connected_by_user_id == owner.id and row.connected_at == NOON
    assert "refresh-1" not in row.refresh_token_encrypted
    assert decrypt_secrets(row.refresh_token_encrypted, SETTINGS) == {"refresh_token": "refresh-1"}
    assert oauth.refresh_token_of(row, SETTINGS) == "refresh-1"
    assert isinstance(audit, AdminAuditLog) and audit.action == "video_youtube_connected"
    assert session.commit.await_count == 1
    assert redis.data == {}, "the state is spent"

    with pytest.raises(AppError) as spent:
        await oauth.finish(session, redis, http, SETTINGS, owner, code="c", state=state)  # type: ignore[arg-type]
    assert spent.value.code == "video_youtube_state_invalid"


@pytest.mark.asyncio
async def test_the_callback_refuses_another_user_and_a_consent_without_a_refresh_token() -> None:
    redis = FakeRedis()
    owner = _owner()
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    session.add = MagicMock()

    started = await oauth.start(redis, SETTINGS, owner, "/")  # type: ignore[arg-type]
    state = parse_qs(urlsplit(started.authorization_url).query)["state"][0]
    other = _owner()
    async with httpx.AsyncClient(transport=_google([])) as http:
        with pytest.raises(AppError) as refused:
            await oauth.finish(session, redis, http, SETTINGS, other, code="c", state=state)  # type: ignore[arg-type]
    assert refused.value.status == 403

    started = await oauth.start(redis, SETTINGS, owner, "/")  # type: ignore[arg-type]
    state = parse_qs(urlsplit(started.authorization_url).query)["state"][0]
    async with httpx.AsyncClient(transport=_google([], refresh=None)) as http:
        with pytest.raises(YouTubeError, match="refresh token"):
            await oauth.finish(session, redis, http, SETTINGS, owner, code="c", state=state)  # type: ignore[arg-type]

    started = await oauth.start(redis, SETTINGS, owner, "/")  # type: ignore[arg-type]
    state = parse_qs(urlsplit(started.authorization_url).query)["state"][0]
    async with httpx.AsyncClient(
        transport=_google([], scope="https://www.googleapis.com/auth/youtube.readonly")
    ) as http:
        with pytest.raises(YouTubeError, match="權限"):
            await oauth.finish(session, redis, http, SETTINGS, owner, code="c", state=state)  # type: ignore[arg-type]
    session.add.assert_not_called()
    session.commit.assert_not_awaited()


def _channel_row() -> VideoYoutubeChannel:
    return VideoYoutubeChannel(
        id=uuid4(),
        channel_id="UCabc",
        channel_title="Mokaair",
        refresh_token_encrypted=encrypt_secrets({"refresh_token": "refresh-1"}, SETTINGS) or "",
        scope=oauth.SCOPE,
        connected_at=NOON,
    )


@pytest.mark.asyncio
async def test_revoking_tells_google_forgets_the_row_and_answers_the_empty_connection() -> None:
    owner = _owner()
    row = _channel_row()
    session = AsyncMock()
    session.scalar = AsyncMock(side_effect=[row, None])
    session.add = MagicMock()
    calls: list[httpx.Request] = []
    async with httpx.AsyncClient(transport=_google(calls)) as http:
        state = await oauth.revoke(session, http, SETTINGS, owner)
    assert [str(call.url) for call in calls] == [oauth.REVOKE]
    assert parse_qs(calls[0].content.decode()) == {"token": ["refresh-1"]}
    session.delete.assert_awaited_once_with(row)
    assert session.add.call_args.args[0].action == "video_youtube_revoked"
    assert state.connected is False and state.configured is True
    assert state.channel_id is None and state.redirect_uri == oauth.callback_url(SETTINGS)


# --- the sync -------------------------------------------------------------------------------


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Package:
    """An approved upload package in a review store: metadata.json, captions, thumbnail."""

    def __init__(self, root: Path, slug: str, metadata: dict[str, Any]) -> None:
        self.store = ReviewStore(root, max_file_bytes=10_000_000, max_total_bytes=100_000_000)
        self.slug = slug
        self.files: list[dict[str, Any]] = []
        self.shas: dict[str, str] = {}
        self.add("metadata", json.dumps(metadata, ensure_ascii=False).encode())

    def add(self, role: str, data: bytes) -> None:
        sha = _sha(data)
        (self.store.root / self.slug).mkdir(parents=True, exist_ok=True)
        (self.store.root / self.slug / sha).write_bytes(data)
        self.files.append({"role": role, "name": f"{role}.bin", "sha256": sha, "size": len(data)})
        self.shas[role] = sha

    def confirmation(self, project_id: Any, status: str = "approved") -> VideoReview:
        return VideoReview(
            id=uuid4(),
            project_id=project_id,
            gate="publish",
            status=status,
            content_sha256=self.shas["metadata"],
            summary="upload",
            payload={},
            files=list(self.files),
            created_at=NOON - timedelta(days=2),
        )


METADATA = {
    "title": "標題",
    "description": "說明",
    "tags": ["a"],
    "category_id": "28",
    "contains_synthetic_media": False,
    "localizations": {
        "en": {"title": "Title", "description": "Desc"},
        "ja": {"title": "題", "description": "説"},
    },
}


def _project(**overrides: Any) -> VideoProject:
    fields: dict[str, Any] = {
        "id": uuid4(),
        "slug": "v",
        "title": "t",
        "stage": "done",
        "youtube_video_id": "dQw4w9WgXcQ",
        "youtube_publish_at": TOMORROW,
        "locales": {"en": {"metadata": True, "captions": True}, "ja": {"captions": True}},
        "locales_decided_at": NOON - timedelta(days=3),
    }
    fields.update(overrides)
    return VideoProject(**fields)


def _batch(project_id: Any, locales: dict[str, Any], day: int = 26) -> VideoReview:
    return VideoReview(
        id=uuid4(),
        project_id=project_id,
        gate="languages",
        status="pending",
        content_sha256=str(day % 10) * 64,
        summary="languages",
        payload={"locales": locales},
        files=[],
        created_at=datetime(2026, 9, day, tzinfo=UTC),
    )


DONE = {"en": {"metadata": "ready", "captions": "ready"}, "ja": {"captions": "ready"}}


class YouTube:
    """A YouTube that answers the five calls the sync makes and remembers them."""

    def __init__(
        self, *, privacy: str = "private", captions: tuple[str, ...] = (), refuse: str | None = None
    ) -> None:
        self.privacy = privacy
        self.existing = list(captions)
        self.refuse = refuse
        self.calls: list[httpx.Request] = []

    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self.handle)

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.calls.append(request)
        url, method = str(request.url).split("?")[0], request.method
        if url == oauth.TOKEN:
            return httpx.Response(200, json={"access_token": "access-1", "expires_in": 3599})
        if self.refuse and url.endswith(self.refuse):
            return httpx.Response(
                403,
                json={
                    "error": {
                        "message": "The request is not properly authorized.",
                        "errors": [{"reason": "forbidden"}],
                    }
                },
            )
        if url.endswith("/youtube/v3/videos") and method == "GET":
            return httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "id": "dQw4w9WgXcQ",
                            "snippet": {"title": "old", "channelId": "UCabc", "categoryId": "22"},
                            "status": {"privacyStatus": self.privacy, "license": "youtube"},
                            "localizations": {},
                        }
                    ]
                },
            )
        if url.endswith("/youtube/v3/videos") and method == "PUT":
            return httpx.Response(200, json=json.loads(request.content))
        if url.endswith("/youtube/v3/captions") and method == "GET":
            return httpx.Response(
                200,
                json={"items": [{"snippet": {"language": lang}} for lang in self.existing]},
            )
        if url.endswith("/upload/youtube/v3/captions") and method == "POST":
            return httpx.Response(200, json={"id": "cap"})
        if url.endswith("/upload/youtube/v3/thumbnails/set") and method == "POST":
            return httpx.Response(200, json={"items": []})
        return httpx.Response(404, json={"error": {"message": f"no {method} {url}"}})

    def sent(self, tail: str, method: str) -> list[httpx.Request]:
        return [
            call
            for call in self.calls
            if str(call.url).split("?")[0].endswith(tail) and call.method == method
        ]

    def update(self) -> dict[str, Any]:
        (put,) = self.sent("/youtube/v3/videos", "PUT")
        return json.loads(put.content)

    def caption_languages(self) -> list[str]:
        uploaded = []
        for call in self.sent("/upload/youtube/v3/captions", "POST"):
            first = call.content.split(b"\r\n\r\n", 2)[1].split(b"\r\n--", 1)[0]
            uploaded.append(json.loads(first)["snippet"]["language"])
        return uploaded


def _wire(
    monkeypatch: pytest.MonkeyPatch,
    project: VideoProject,
    history: list[VideoReview],
    *,
    row: VideoYoutubeChannel | None,
    settings: Settings = SETTINGS,
) -> AsyncMock:
    async def load(_: Any) -> Settings:
        return settings

    monkeypatch.setattr(reviews, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(reviews, "_reviews", AsyncMock(return_value=history))
    monkeypatch.setattr(reviews, "project_view", AsyncMock(return_value="view"))
    monkeypatch.setattr(service, "load_runtime_settings", load)
    monkeypatch.setattr(oauth, "channel", AsyncMock(return_value=row))
    session = AsyncMock()
    session.add = MagicMock()
    return session


async def _run(
    session: AsyncMock, package: Package, youtube: YouTube, reason: SyncReason = "linked"
) -> None:
    def client() -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=youtube.transport())

    view = await service.sync_project(
        session, package.store, "v", reason=reason, client_factory=client, now=NOON
    )
    assert view == "view"


def _steps(project: VideoProject) -> dict[str, tuple[bool, str]]:
    assert isinstance(project.youtube_sync, dict)
    return {step["id"]: (step["ok"], step["detail"]) for step in project.youtube_sync["steps"]}


@pytest.mark.asyncio
async def test_the_sync_sends_the_chosen_languages_schedules_once_made_and_records_each_step(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    project = _project()
    package = Package(tmp_path, "v", METADATA)
    for locale in ("zh-TW", "en", "ja"):
        package.add(f"captions_{locale}", f"1\n{locale}\n".encode())
    package.add("thumbnail", b"\xff\xd8jpeg")
    history = [_batch(project.id, DONE), package.confirmation(project.id)]
    session = _wire(monkeypatch, project, history, row=_channel_row())
    youtube = YouTube(captions=("zh-TW",))

    await _run(session, package, youtube)

    assert youtube.calls[0].url == oauth.TOKEN, "an access token first, from the refresh token"
    assert parse_qs(youtube.calls[0].content.decode())["refresh_token"] == ["refresh-1"]
    assert all(call.headers.get("Authorization") == "Bearer access-1" for call in youtube.calls[1:])
    body = youtube.update()
    assert body["snippet"]["title"] == "標題" and body["snippet"]["defaultLanguage"] == "zh-TW"
    assert list(body["localizations"]) == ["en"], "ja has captions chosen, not titles"
    assert body["status"]["privacyStatus"] == "private"
    assert body["status"]["publishAt"] == "2026-09-28T12:00:00Z", "every chosen part is made"
    assert body["status"]["license"] == "youtube", "what was there stays"
    assert youtube.caption_languages() == ["en", "ja"], "zh-TW is on YouTube already"
    assert len(youtube.sent("/upload/youtube/v3/thumbnails/set", "POST")) == 1

    steps = _steps(project)
    assert steps["video"] == (True, "標題與說明：zh-TW、en；不用揭露")
    assert steps["schedule"] == (True, "排定 2026-09-28T12:00:00+00:00 由 YouTube 公開")
    assert steps["captions"] == (True, "字幕：新上傳 en、ja；已有 zh-TW")
    assert steps["thumbnail"] == (True, "縮圖已上傳")
    record = project.youtube_sync
    assert isinstance(record, dict) and record["ok"] is True and record["reason"] == "linked"
    assert record["video_id"] == "dQw4w9WgXcQ" and record["at"] == "2026-09-27T12:00:00Z"
    assert record["localizations"] == ["en"] and record["captions"] == ["zh-TW", "en", "ja"]
    assert record["thumbnail_sha256"] == package.shas["thumbnail"]
    assert project.updated_at == NOON
    audit = session.add.call_args.args[0]
    assert isinstance(audit, AdminAuditLog) and audit.action == "video_youtube_synced"
    assert audit.metadata_json["ok"] is True and audit.metadata_json["reason"] == "linked"
    assert session.commit.await_count == 1

    # Sent again: YouTube now has every track and the thumbnail did not change, so nothing is
    # uploaded twice; the titles and the time are sent whole again, which is harmless.
    again = YouTube(captions=("zh-TW", "en", "ja"))
    await _run(session, package, again, reason="manual")
    assert again.caption_languages() == []
    assert again.sent("/upload/youtube/v3/thumbnails/set", "POST") == []
    steps = _steps(project)
    assert steps["captions"] == (True, "字幕：新上傳 無；已有 zh-TW、en、ja")
    assert steps["thumbnail"] == (True, "縮圖沒變，沒有再上傳")
    assert isinstance(project.youtube_sync, dict) and project.youtube_sync["reason"] == "manual"


@pytest.mark.asyncio
async def test_the_publish_time_waits_for_the_languages_and_is_refused_when_public_or_past(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    package = Package(tmp_path, "v", METADATA)
    package.add("captions_zh-TW", b"1\nzh\n")

    # ja's captions are still in the making: everything else goes, the time does not.
    project = _project()
    working = {"en": {"metadata": "ready", "captions": "ready"}}
    history = [_batch(project.id, working), package.confirmation(project.id)]
    session = _wire(monkeypatch, project, history, row=_channel_row())
    youtube = YouTube()
    await _run(session, package, youtube, reason="languages")
    assert "publishAt" not in youtube.update()["status"]
    assert list(youtube.update()["localizations"]) == ["en"]
    steps = _steps(project)
    assert steps["schedule"] == (True, "語言還沒都做好，排程等做好那一輪再送")
    assert steps["captions"] == (True, "字幕：新上傳 zh-TW")
    assert isinstance(project.youtube_sync, dict) and project.youtube_sync["ok"] is True
    assert project.youtube_sync["scheduled_at"] is None

    # The owner never decided: the same wait.
    undecided = _project(locales={}, locales_decided_at=None)
    session = _wire(
        monkeypatch, undecided, [package.confirmation(undecided.id)], row=_channel_row()
    )
    youtube = YouTube()
    await _run(session, package, youtube)
    assert "publishAt" not in youtube.update()["status"]
    assert _steps(undecided)["schedule"][1] == "語言還沒都做好，排程等做好那一輪再送"

    # Not private any more: refused, recorded, and the captions still go up.
    project = _project()
    session = _wire(
        monkeypatch,
        project,
        [_batch(project.id, DONE), package.confirmation(project.id)],
        row=_channel_row(),
    )
    youtube = YouTube(privacy="public")
    await _run(session, package, youtube)
    assert "publishAt" not in youtube.update()["status"]
    ok, detail = _steps(project)["schedule"]
    assert ok is False and "public" in detail and "不是私人" in detail
    assert youtube.caption_languages() == ["zh-TW"]
    assert isinstance(project.youtube_sync, dict) and project.youtube_sync["ok"] is False

    # A time gone by.
    project = _project(youtube_publish_at=NOON - timedelta(hours=1))
    session = _wire(
        monkeypatch,
        project,
        [_batch(project.id, DONE), package.confirmation(project.id)],
        row=_channel_row(),
    )
    youtube = YouTube()
    await _run(session, package, youtube)
    assert "publishAt" not in youtube.update()["status"]
    ok, detail = _steps(project)["schedule"]
    assert ok is False and "已經過了" in detail

    # No time chosen yet: nothing to schedule and no schedule step at all.
    project = _project(youtube_publish_at=None)
    session = _wire(
        monkeypatch,
        project,
        [_batch(project.id, DONE), package.confirmation(project.id)],
        row=_channel_row(),
    )
    youtube = YouTube()
    await _run(session, package, youtube)
    assert "publishAt" not in youtube.update()["status"]
    assert "schedule" not in _steps(project)
    assert isinstance(project.youtube_sync, dict) and project.youtube_sync["ok"] is True


@pytest.mark.asyncio
async def test_the_sync_refuses_before_calling_youtube_when_something_is_not_in_place(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    package = Package(tmp_path, "v", METADATA)
    cases: list[
        tuple[str, VideoProject, list[VideoReview], VideoYoutubeChannel | None, Settings]
    ] = []
    unlinked = _project(youtube_video_id=None)
    cases.append(
        (
            "還沒有 YouTube 影片 id",
            unlinked,
            [package.confirmation(unlinked.id)],
            _channel_row(),
            SETTINGS,
        )
    )
    project = _project()
    cases.append(
        ("還沒連結 YouTube 頻道", project, [package.confirmation(project.id)], None, SETTINGS)
    )
    cases.append(
        (
            "還沒連結 YouTube 頻道",
            project,
            [package.confirmation(project.id)],
            _channel_row(),
            Settings(),
        )
    )
    cases.append(
        (
            "上傳包還沒核准",
            project,
            [package.confirmation(project.id, "pending")],
            _channel_row(),
            SETTINGS,
        )
    )
    stale = package.confirmation(project.id)
    stale.content_sha256 = "b" * 64
    cases.append(("雜湊對不上", project, [stale], _channel_row(), SETTINGS))
    gone = package.confirmation(project.id)
    gone.files = [{**item, "sha256": "c" * 64} for item in gone.files]
    gone.content_sha256 = "c" * 64
    cases.append(("已不在審核區", project, [gone], _channel_row(), SETTINGS))
    for expected, target, history, row, settings in cases:
        target.youtube_sync = None
        session = _wire(monkeypatch, target, history, row=row, settings=settings)
        youtube = YouTube()
        await _run(session, package, youtube)
        assert youtube.calls == [], expected
        steps = _steps(target)
        assert list(steps) == ["video"] and steps["video"][0] is False, expected
        assert expected in steps["video"][1]
        assert isinstance(target.youtube_sync, dict) and target.youtube_sync["ok"] is False
        assert session.commit.await_count == 1, "what was refused is recorded for the page"


@pytest.mark.asyncio
async def test_a_refusal_from_youtube_is_recorded_on_the_step_it_stopped_at(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    package = Package(tmp_path, "v", METADATA)
    package.add("captions_zh-TW", b"1\nzh\n")
    package.add("captions_en", b"1\nen\n")
    project = _project()
    history = [_batch(project.id, DONE), package.confirmation(project.id)]

    session = _wire(monkeypatch, project, history, row=_channel_row())
    youtube = YouTube(refuse="/upload/youtube/v3/captions")
    await _run(session, package, youtube)
    steps = _steps(project)
    assert steps["video"][0] is True and steps["schedule"][0] is True
    assert steps["captions"] == (
        False,
        "YouTube 回 403：The request is not properly authorized.（forbidden）",
    )
    assert "thumbnail" not in steps
    assert isinstance(project.youtube_sync, dict) and project.youtube_sync["ok"] is False

    session = _wire(monkeypatch, project, history, row=_channel_row())
    youtube = YouTube(refuse="/youtube/v3/videos")
    await _run(session, package, youtube)
    steps = _steps(project)
    assert list(steps) == ["video"] and steps["video"][0] is False
    assert youtube.caption_languages() == [], "nothing after the step that failed"

    # A wrong id, or another channel's video.
    session = _wire(monkeypatch, project, history, row=_channel_row())

    def nobody(request: httpx.Request) -> httpx.Response:
        if str(request.url) == oauth.TOKEN:
            return httpx.Response(200, json={"access_token": "a"})
        return httpx.Response(200, json={"items": []})

    view = await service.sync_project(
        session,
        package.store,
        "v",
        reason="manual",
        client_factory=lambda: httpx.AsyncClient(transport=httpx.MockTransport(nobody)),
        now=NOON,
    )
    assert view == "view"
    assert _steps(project)["video"] == (False, "這個頻道上找不到影片 dQw4w9WgXcQ：id 或頻道不對")


def test_the_languages_are_done_once_the_owner_decided_and_no_chosen_part_is_still_working() -> (
    None
):
    project = _project()
    assert service.languages_done(project, [_batch(project.id, DONE)]) is True
    assert service.languages_done(project, []) is False, "chosen parts nobody reported"
    partial = {
        "en": {"metadata": "ready", "captions": "ready"},
        "ja": {"captions": {"status": "skipped", "reason": "r"}},
    }
    assert service.languages_done(project, [_batch(project.id, partial)]) is True, "skipped counts"
    assert service.languages_done(_project(locales_decided_at=None), []) is False
    assert service.languages_done(_project(locales={}), []) is True, (
        "only zh-TW: nothing to wait for"
    )


@pytest.mark.asyncio
async def test_a_language_batch_queues_a_sync_only_for_a_video_already_on_youtube(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    queued: list[tuple[str, str]] = []
    monkeypatch.setattr(
        service, "enqueue_sync", lambda slug, reason: queued.append((slug, reason)) or "job-1"
    )
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    assert await service.enqueue_after_languages(session, "v") is None
    session.scalar = AsyncMock(return_value="dQw4w9WgXcQ")
    assert await service.enqueue_after_languages(session, "v") == "job-1"
    assert queued == [("v", "languages")]


def test_the_queue_being_down_is_a_warning_not_a_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    from redis.exceptions import ConnectionError as RedisConnectionError

    class Down:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def enqueue(self, *args: Any, **kwargs: Any) -> Any:
            raise RedisConnectionError("down")

    monkeypatch.setattr(service, "Queue", Down)
    monkeypatch.setattr(
        service, "get_settings", lambda: Settings(redis_url="redis://127.0.0.1:1/0")
    )
    assert service.enqueue_sync("v", "manual") is None


# --- the routes -----------------------------------------------------------------------------


def _app(
    monkeypatch: pytest.MonkeyPatch, user: User, redis: FakeRedis, settings: Settings = SETTINGS
) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.router, prefix="/api/v1")

    async def session() -> Any:
        mock = AsyncMock()
        mock.scalar = AsyncMock(return_value=None)
        mock.add = MagicMock()
        yield mock

    async def load(_: Any) -> Settings:
        return settings

    app.dependency_overrides[get_session] = session
    app.dependency_overrides[current_user] = lambda: user
    monkeypatch.setattr(admin_api, "load_runtime_settings", load)
    monkeypatch.setattr(admin_api, "get_redis", lambda: redis)
    return app


def _content() -> User:
    user = User(id=uuid4(), email="content@example.com", password_hash="unused")
    user._admin_roles_cache = frozenset({"content"})  # type: ignore[attr-defined]
    return user


@pytest.mark.asyncio
async def test_a_content_manager_sees_the_connection_and_only_the_owner_connects_or_revokes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    redis = FakeRedis()
    base = "/api/v1/admin/video-youtube/connection"
    async with AsyncClient(
        transport=ASGITransport(app=_app(monkeypatch, _content(), redis)), base_url="http://test"
    ) as client:
        seen = await client.get(base)
        not_started = await client.post(f"{base}/start", json={"next_path": "/admin/videos"})
        not_revoked = await client.delete(base)
        not_called_back = await client.get(f"{base}/callback", params={"state": "s", "code": "c"})
    assert seen.status_code == 200
    assert seen.json() == {
        "configured": True,
        "connected": False,
        "channel_id": None,
        "channel_title": None,
        "connected_at": None,
        "redirect_uri": "https://mokaair.com/api/travel/admin/video-youtube/connection/callback",
        "scope": oauth.SCOPE,
    }
    assert not_started.status_code == 403 and not_revoked.status_code == 403
    assert not_called_back.status_code == 403
    assert redis.data == {}

    owner = _owner()
    async with AsyncClient(
        transport=ASGITransport(app=_app(monkeypatch, owner, redis)), base_url="http://test"
    ) as client:
        started = await client.post(f"{base}/start", json={"next_path": "/admin/videos?tab=s"})
        assert started.status_code == 200
        state = parse_qs(urlsplit(started.json()["authorization_url"]).query)["state"][0]
        assert f"{oauth.FLOW_KEY}{state}" in redis.data
        # The owner pressed "cancel" on Google's screen: back to the tab, told so, state spent.
        denied = await client.get(
            f"{base}/callback", params={"state": state, "error": "access_denied"}
        )
        assert denied.status_code == 302
        assert denied.headers["location"] == "/admin/videos?tab=s&youtube=access_denied"
        assert redis.data == {}
        stale = await client.get(f"{base}/callback", params={"state": state, "code": "c"})
        assert stale.status_code == 400
        assert stale.json()["code"] == "video_youtube_state_invalid"

        unconfigured = await client.post(f"{base}/start", json={"next_path": "/"})
    assert unconfigured.status_code == 200, "the same app: still configured"
    async with AsyncClient(
        transport=ASGITransport(app=_app(monkeypatch, owner, redis, Settings())),
        base_url="http://test",
    ) as client:
        refused = await client.post(f"{base}/start", json={"next_path": "/"})
        state = await client.get(base)
    assert refused.status_code == 409 and refused.json()["code"] == "video_youtube_not_configured"
    assert state.json()["configured"] is False


@pytest.mark.asyncio
async def test_send_again_queues_a_sync_for_a_linked_video(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    linked = _project()
    view = ProjectOut(
        slug="v",
        title="t",
        stage="done",
        checklist=[],
        youtube_video_id="dQw4w9WgXcQ",
        last_synced_at=NOON,
        pending=0,
        reviews=[],
    )
    monkeypatch.setattr(reviews, "_project", AsyncMock(return_value=linked))
    monkeypatch.setattr(reviews, "project_view", AsyncMock(return_value=view))
    queued: list[tuple[str, str]] = []
    monkeypatch.setattr(
        service, "enqueue_sync", lambda slug, reason: queued.append((slug, reason)) or "job-1"
    )
    async with AsyncClient(
        transport=ASGITransport(app=_app(monkeypatch, _content(), FakeRedis())),
        base_url="http://test",
    ) as client:
        accepted = await client.post("/api/v1/admin/video-youtube/v/sync")
        monkeypatch.setattr(service, "enqueue_sync", lambda slug, reason: None)
        down = await client.post("/api/v1/admin/video-youtube/v/sync")
        monkeypatch.setattr(
            reviews, "_project", AsyncMock(return_value=_project(youtube_video_id=None))
        )
        unlinked = await client.post("/api/v1/admin/video-youtube/v/sync")
    assert accepted.status_code == 202 and accepted.json()["slug"] == "v"
    assert queued == [("v", "manual")]
    assert down.status_code == 503 and down.json()["code"] == "video_youtube_queue_unavailable"
    assert unlinked.status_code == 409 and unlinked.json()["code"] == "video_youtube_not_linked"
