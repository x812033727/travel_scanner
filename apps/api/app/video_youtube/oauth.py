"""Connecting the owner's YouTube channel: the consent flow, the stored refresh token, and the
access tokens minted from it (docs/videos/HANDS-OFF.md §YouTube API 第一步).

The flow runs on the site: the owner is sent to Google's consent screen from the settings tab
and comes back to the API's callback through the site's own proxy; the refresh token Google
answers with is encrypted like the provider secrets and kept in ``video_youtube_channel``,
where nothing returns it. The scope is ``youtube.force-ssl`` alone, which is what
``videos.update``, ``captions.insert`` and ``thumbnails.set`` need.
"""

from __future__ import annotations

import base64
import hashlib
import json
import secrets
from datetime import UTC, datetime
from typing import Any, cast
from urllib.parse import urlencode

import httpx
from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import decrypt_secrets, encrypt_secrets
from app.config import Settings
from app.models import AdminAuditLog, User, VideoYoutubeChannel
from app.problems import AppError
from app.video_youtube.client import YouTubeError, _detail
from app.video_youtube.schemas import ConnectionOut, StartOut

SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
AUTHORIZE = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN = "https://oauth2.googleapis.com/token"  # noqa: S105 -- endpoint URL, not a secret
REVOKE = "https://oauth2.googleapis.com/revoke"
CHANNELS = "https://www.googleapis.com/youtube/v3/channels"
FLOW_TTL_SECONDS = 600
FLOW_KEY = "video-youtube-oauth:"


def configured(settings: Settings) -> bool:
    return bool(settings.youtube_oauth_client_id and settings.youtube_oauth_client_secret)


def callback_url(settings: Settings) -> str:
    """The redirect URI the owner registers on the Google Cloud client: the site's proxy path
    to the API's callback, so the browser lands on the site's origin with its admin cookie."""
    base = settings.next_public_site_url.rstrip("/")
    return f"{base}/api/travel/admin/video-youtube/connection/callback"


def safe_next(value: str) -> str:
    """A site path to send the browser back to, never another host."""
    value = value.strip()
    if not value.startswith("/") or value.startswith("//") or "\\" in value:
        return "/"
    return value


def _challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()


async def channel(session: AsyncSession) -> VideoYoutubeChannel | None:
    row: VideoYoutubeChannel | None = await session.scalar(
        select(VideoYoutubeChannel).order_by(VideoYoutubeChannel.connected_at.desc()).limit(1)
    )
    return row


def refresh_token_of(row: VideoYoutubeChannel, settings: Settings | None = None) -> str:
    token = decrypt_secrets(row.refresh_token_encrypted, settings).get("refresh_token")
    if not token:
        raise AppError(500, "video_youtube_token_unreadable", "YouTube 的授權讀不出來，請重新連結")
    return token


async def connection(session: AsyncSession, settings: Settings) -> ConnectionOut:
    row = await channel(session)
    return ConnectionOut(
        configured=configured(settings),
        connected=row is not None,
        channel_id=row.channel_id if row else None,
        channel_title=row.channel_title if row else None,
        connected_at=row.connected_at if row else None,
        redirect_uri=callback_url(settings),
        scope=SCOPE,
    )


async def start(redis: Redis, settings: Settings, user: User, next_path: str) -> StartOut:
    """Where to send the owner: Google's consent screen, asking for offline access so a refresh
    token comes back, with the state and PKCE verifier kept in Redis for ten minutes."""
    if not configured(settings):
        raise AppError(
            409,
            "video_youtube_not_configured",
            "先在「Azure 語音（影片旁白）」卡填 YouTube OAuth 用戶端 ID 與密鑰",
        )
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)
    record = {"user_id": str(user.id), "next": safe_next(next_path), "verifier": verifier}
    try:
        await redis.set(f"{FLOW_KEY}{state}", json.dumps(record), ex=FLOW_TTL_SECONDS)
    except RedisError as exc:
        raise AppError(503, "video_youtube_state_unavailable", "驗證服務暫時無法使用") from exc
    params = {
        "response_type": "code",
        "client_id": cast(str, settings.youtube_oauth_client_id),
        "redirect_uri": callback_url(settings),
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent",
        "include_granted_scopes": "false",
        "state": state,
        "code_challenge": _challenge(verifier),
        "code_challenge_method": "S256",
    }
    return StartOut(
        authorization_url=f"{AUTHORIZE}?{urlencode(params)}", expires_in=FLOW_TTL_SECONDS
    )


async def _flow(redis: Redis, state: str) -> dict[str, Any]:
    try:
        raw = await redis.getdel(f"{FLOW_KEY}{state}")
    except RedisError as exc:
        raise AppError(503, "video_youtube_state_unavailable", "驗證服務暫時無法使用") from exc
    if not raw:
        raise AppError(
            400, "video_youtube_state_invalid", "這次連結已過期或不是這裡發起的，請再按一次"
        )
    record = json.loads(raw)
    return record if isinstance(record, dict) else {}


async def exchange_code(
    http: httpx.AsyncClient, settings: Settings, code: str, verifier: str
) -> dict[str, Any]:
    response = await http.post(
        TOKEN,
        data={
            "code": code,
            "client_id": cast(str, settings.youtube_oauth_client_id),
            "client_secret": cast(str, settings.youtube_oauth_client_secret),
            "redirect_uri": callback_url(settings),
            "grant_type": "authorization_code",
            "code_verifier": verifier,
        },
    )
    if response.status_code >= 400:
        raise YouTubeError(response.status_code, _detail(response))
    body = response.json()
    return body if isinstance(body, dict) else {}


async def access_token(http: httpx.AsyncClient, settings: Settings, refresh_token: str) -> str:
    """A fresh access token from the stored refresh token; Google answers in well under a second."""
    response = await http.post(
        TOKEN,
        data={
            "client_id": cast(str, settings.youtube_oauth_client_id),
            "client_secret": cast(str, settings.youtube_oauth_client_secret),
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
    )
    if response.status_code >= 400:
        raise YouTubeError(response.status_code, _detail(response))
    body = response.json()
    token = body.get("access_token") if isinstance(body, dict) else None
    if not isinstance(token, str) or not token:
        raise YouTubeError(502, "Google 沒有回 access token")
    return token


async def _mine(http: httpx.AsyncClient, token: str) -> tuple[str | None, str | None]:
    response = await http.get(
        CHANNELS,
        params={"part": "snippet", "mine": "true"},
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code >= 400:
        raise YouTubeError(response.status_code, _detail(response))
    body = response.json()
    items = body.get("items") if isinstance(body, dict) else None
    first = items[0] if isinstance(items, list) and items else {}
    snippet = first.get("snippet") if isinstance(first, dict) else None
    title = snippet.get("title") if isinstance(snippet, dict) else None
    return (first.get("id") if isinstance(first, dict) else None), (
        title if isinstance(title, str) else None
    )


async def finish(
    session: AsyncSession,
    redis: Redis,
    http: httpx.AsyncClient,
    settings: Settings,
    user: User,
    *,
    code: str,
    state: str,
    now: datetime | None = None,
) -> str:
    """Google sent the owner back with a code: trade it for the tokens, keep the refresh token
    encrypted with the channel it opens, and answer the path to send the browser on to."""
    flow = await _flow(redis, state)
    if flow.get("user_id") != str(user.id):
        raise AppError(403, "video_youtube_state_other_user", "這次連結是別的帳號發起的")
    next_path = safe_next(str(flow.get("next") or "/"))
    tokens = await exchange_code(http, settings, code, str(flow.get("verifier") or ""))
    refresh = tokens.get("refresh_token")
    if not isinstance(refresh, str) or not refresh:
        raise YouTubeError(
            502,
            "Google 沒有給 refresh token：同意畫面上要允許離線存取；"
            "已授權過的話先到 Google 帳號的第三方存取撤銷再連結一次",
        )
    granted = str(tokens.get("scope") or SCOPE)
    if SCOPE not in granted.split():
        raise YouTubeError(403, f"同意的權限不含 {SCOPE}")
    channel_id, channel_title = await _mine(http, str(tokens.get("access_token") or ""))
    now = now or datetime.now(UTC)
    row = await channel(session)
    if row is None:
        row = VideoYoutubeChannel(refresh_token_encrypted="", scope=SCOPE)
        session.add(row)
    row.refresh_token_encrypted = encrypt_secrets({"refresh_token": refresh}, settings) or ""
    row.scope = granted
    row.channel_id = channel_id
    row.channel_title = channel_title
    row.connected_by_user_id = user.id
    row.connected_at = now
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="video_youtube_connected",
            target="video_youtube_channel",
            metadata_json={"channel_id": channel_id, "channel_title": channel_title},
        )
    )
    await session.commit()
    return next_path


async def revoke(
    session: AsyncSession, http: httpx.AsyncClient, settings: Settings, user: User
) -> ConnectionOut:
    """Forget the channel: Google is told to revoke the token (best effort) and the row goes."""
    row = await channel(session)
    if row is not None:
        try:
            token = refresh_token_of(row, settings)
            await http.post(REVOKE, data={"token": token})
        except (AppError, httpx.HTTPError):
            pass
        await session.delete(row)
        session.add(
            AdminAuditLog(
                actor_user_id=user.id,
                action="video_youtube_revoked",
                target="video_youtube_channel",
                metadata_json={"channel_id": row.channel_id},
            )
        )
        await session.commit()
    return await connection(session, settings)
