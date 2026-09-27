"""The linked channel: the owner's OAuth client, the grant, and checking that it still works.

docs/videos/HANDS-OFF.md §YouTube API 第一步. The owner creates a "web application" OAuth client
in their own Google Cloud project, pastes its id and secret on the settings tab of /admin/videos,
registers ``redirect_uri`` with it, and presses the link button: the web route
(apps/web/app/api/admin-video-youtube) starts the flow here, Google asks the owner to allow
access, and the callback hands the code back to ``finish_link``. The refresh token is stored
encrypted with the client secret and never leaves the API; the worker, agents and chats never see
it. Revoking asks Google to forget the grant and clears it here either way.

Developer Policies III.E.4 asks that a stored grant be checked at least every 30 days and that
other data read through it be refreshed or deleted within 30 days: ``verify`` reads the channel
again with channels.list (1 unit), and the card calls it whenever the last check is older than
VERIFY_EVERY.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any
from urllib.parse import urlencode

import httpx
from redis.exceptions import RedisError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import decrypt_secrets, encrypt_secrets, load_runtime_settings
from app.infra import get_redis
from app.models import AdminAuditLog, User, VideoYoutubeConnection
from app.video_youtube.client import (
    AUTHORIZE,
    SCOPE,
    AuthorizationLost,
    YoutubeClient,
    YoutubeError,
    exchange_code,
    refresh_access_token,
    revoke_token,
)
from app.video_youtube.errors import Refused
from app.video_youtube.requests import as_dict
from app.video_youtube.schemas import (
    ClientIn,
    ConnectionView,
    OAuthExchangeIn,
    OAuthStartIn,
    OAuthStartOut,
)

FLOW_TTL_SECONDS = 600
FLOW_KEY = "video-youtube-flow:{}"
VERIFY_EVERY = timedelta(days=25)
CALLBACK_PATH = "/api/admin-video-youtube/callback"
LOST_GRANT = "頻道授權已失效（在 Google 帳戶撤銷了，或太久沒用被 Google 收回），請重新連結"


def http_client() -> httpx.AsyncClient:
    """The client every Google call runs on; tests replace this function."""
    return httpx.AsyncClient(follow_redirects=False)


def redirect_uri(site_url: str) -> str:
    return f"{site_url.rstrip('/')}{CALLBACK_PATH}"


def _challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()


async def connection_row(session: AsyncSession, *, lock: bool = False) -> VideoYoutubeConnection:
    statement = select(VideoYoutubeConnection).where(VideoYoutubeConnection.id == 1)
    if lock:
        statement = statement.with_for_update()
    row = await session.scalar(statement)
    if row is None:
        row = VideoYoutubeConnection(id=1, audited=False)
        session.add(row)
        await session.flush()
    return row


def stored_secrets(row: VideoYoutubeConnection) -> dict[str, str]:
    return decrypt_secrets(row.secret_config_encrypted)


def _store_secrets(row: VideoYoutubeConnection, values: dict[str, str]) -> None:
    row.secret_config_encrypted = encrypt_secrets({k: v for k, v in values.items() if v})


def configured(row: VideoYoutubeConnection) -> bool:
    return bool(row.client_id and stored_secrets(row).get("client_secret"))


def linked(row: VideoYoutubeConnection) -> bool:
    return bool(row.channel_id and stored_secrets(row).get("refresh_token"))


def view(row: VideoYoutubeConnection, site_url: str) -> ConnectionView:
    values = stored_secrets(row)
    is_linked = bool(row.channel_id and values.get("refresh_token"))
    return ConnectionView(
        client_id=row.client_id,
        client_secret_set=bool(values.get("client_secret")),
        redirect_uri=redirect_uri(site_url),
        scope=SCOPE,
        configured=bool(row.client_id and values.get("client_secret")),
        linked=is_linked,
        channel_id=row.channel_id if is_linked else None,
        channel_title=row.channel_title if is_linked else None,
        channel_url=f"https://www.youtube.com/channel/{row.channel_id}" if is_linked else None,
        linked_at=row.linked_at if is_linked else None,
        verified_at=row.verified_at if is_linked else None,
        problem=row.problem,
        audited=row.audited,
    )


async def _site_url(session: AsyncSession) -> str:
    return (await load_runtime_settings(session)).next_public_site_url


async def connection_view(session: AsyncSession) -> ConnectionView:
    """The card, checking the grant first when the last check is older than VERIFY_EVERY."""
    row = await connection_row(session)
    stale = row.verified_at is None or row.verified_at < datetime.now(UTC) - VERIFY_EVERY
    if linked(row) and stale and row.problem is None:
        try:
            return await verify(session)
        except Refused:
            # Google did not answer this time; the card shows the old check and tries again
            # on the next read rather than failing the page.
            await session.rollback()
            row = await connection_row(session)
    await session.commit()
    return view(row, await _site_url(session))


def _audit(session: AsyncSession, user: User | None, action: str, **metadata: Any) -> None:
    session.add(
        AdminAuditLog(
            actor_user_id=user.id if user else None,
            action=action,
            target="video-youtube-connection:1",
            metadata_json=metadata,
        )
    )


async def save_client(session: AsyncSession, user: User, payload: ClientIn) -> ConnectionView:
    """Store the OAuth client and the audit switch. A new client cannot speak for the old grant,
    so the client id cannot change while a channel is linked."""
    row = await connection_row(session, lock=True)
    values = stored_secrets(row)
    if row.client_id and payload.client_id != row.client_id and values.get("refresh_token"):
        raise Refused(
            409, "video_youtube_client_in_use", "頻道還連結著舊的用戶端：先解除連結，再換用戶端"
        )
    changed = sorted(
        name
        for name, before, after in (
            ("client_id", row.client_id, payload.client_id),
            ("client_secret", values.get("client_secret"), payload.client_secret),
            ("audited", row.audited, payload.audited),
        )
        if after is not None and before != after
    )
    row.client_id = payload.client_id
    if payload.client_secret is not None:
        values["client_secret"] = payload.client_secret
    _store_secrets(row, values)
    row.audited = payload.audited
    row.updated_by_user_id = user.id
    _audit(session, user, "video_youtube_client_saved", changed=changed, audited=row.audited)
    await session.commit()
    return view(row, await _site_url(session))


async def start_link(session: AsyncSession, user: User, payload: OAuthStartIn) -> OAuthStartOut:
    row = await connection_row(session)
    if not configured(row):
        raise Refused(
            409, "video_youtube_client_missing", "先在設定分頁填好 OAuth 用戶端 ID 與密鑰"
        )
    flow_id = secrets.token_urlsafe(32)
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)
    record = {
        "state": state,
        "verifier": verifier,
        "binding": hashlib.sha256(payload.browser_binding.encode()).hexdigest(),
        "user_id": str(user.id),
        "auth_version": user.auth_version,
    }
    try:
        await get_redis().set(FLOW_KEY.format(flow_id), json.dumps(record), ex=FLOW_TTL_SECONDS)
    except RedisError as exc:
        raise Refused(
            503, "video_youtube_state_unavailable", "暫時無法開始授權，請稍後再試"
        ) from exc
    params = {
        "client_id": row.client_id,
        "redirect_uri": redirect_uri(await _site_url(session)),
        "response_type": "code",
        "scope": SCOPE,
        # A refresh token, so the site can act when the owner is not on the page; "consent"
        # makes Google issue a new one even when this client was allowed before, and
        # "select_account" lets the owner pick the Google account or brand account that owns
        # the channel.
        "access_type": "offline",
        "prompt": "select_account consent",
        "state": state,
        "code_challenge": _challenge(verifier),
        "code_challenge_method": "S256",
    }
    await session.commit()
    return OAuthStartOut(
        authorization_url=f"{AUTHORIZE}?{urlencode(params)}",
        flow_id=flow_id,
        state=state,
        expires_in=FLOW_TTL_SECONDS,
    )


async def _read_flow(user: User, payload: OAuthExchangeIn) -> dict[str, Any]:
    try:
        raw = await get_redis().getdel(FLOW_KEY.format(payload.flow_id))
    except RedisError as exc:
        raise Refused(
            503, "video_youtube_state_unavailable", "暫時無法完成授權，請再試一次"
        ) from exc
    invalid = Refused(
        401, "video_youtube_state_invalid", "授權已逾時或不是從這個瀏覽器開始的，請重新連結"
    )
    if not raw:
        raise invalid
    try:
        flow = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise invalid from exc
    binding = hashlib.sha256(payload.browser_binding.encode()).hexdigest()
    if (
        not isinstance(flow, dict)
        or not hmac.compare_digest(str(flow.get("state", "")), payload.state)
        or not hmac.compare_digest(str(flow.get("binding", "")), binding)
        or flow.get("user_id") != str(user.id)
        or flow.get("auth_version") != user.auth_version
    ):
        raise invalid
    return flow


def _scopes(value: str) -> set[str]:
    return set(value.split())


async def finish_link(
    session: AsyncSession, user: User, payload: OAuthExchangeIn
) -> ConnectionView:
    """Trade the code for the grant, read the channel it speaks for, and keep it."""
    flow = await _read_flow(user, payload)
    row = await connection_row(session, lock=True)
    values = stored_secrets(row)
    if not row.client_id or not values.get("client_secret"):
        raise Refused(409, "video_youtube_client_missing", "OAuth 用戶端被清掉了，請重新設定")
    site_url = await _site_url(session)
    async with http_client() as http:
        try:
            grant = await exchange_code(
                http,
                client_id=row.client_id,
                client_secret=values["client_secret"],
                code=payload.code,
                verifier=str(flow["verifier"]),
                redirect_uri=redirect_uri(site_url),
            )
            if SCOPE not in _scopes(grant.scope):
                raise Refused(
                    422,
                    "video_youtube_scope_missing",
                    "Google 的同意畫面上沒有勾 YouTube 的權限，請重新連結並勾選它",
                )
            if grant.refresh_token is None:
                raise Refused(
                    502,
                    "video_youtube_no_refresh_token",
                    "Google 沒有給長期授權；到 Google 帳戶移除這個應用程式的存取權後再連結一次",
                )
            channel = await YoutubeClient(http, grant.access_token).my_channel()
        except YoutubeError as error:
            raise Refused(
                502, "video_youtube_exchange_failed", f"Google 拒絕了這次授權：{error.message}"
            ) from error
        except httpx.HTTPError as error:
            raise Refused(502, "video_youtube_unreachable", "連不到 Google，請再試一次") from error
        if channel is None:
            await revoke_token(http, grant.refresh_token)
            raise Refused(
                422,
                "video_youtube_no_channel",
                "這個 Google 帳號沒有 YouTube 頻道；連結時請選擁有頻道的帳號或品牌帳號",
            )
        # Google revocation removes the project's grant, including the token just issued.
        # Replacing our stored token is enough; only an explicit unlink should revoke it.
    snippet = as_dict(channel.get("snippet"))
    now = datetime.now(UTC)
    values["refresh_token"] = grant.refresh_token
    _store_secrets(row, values)
    row.channel_id = str(channel.get("id") or "")[:64] or None
    row.channel_title = str(snippet.get("title") or "")[:200] or None
    row.scope = grant.scope
    row.linked_at = now
    row.linked_by_user_id = user.id
    row.verified_at = now
    row.problem = None
    _audit(session, user, "video_youtube_channel_linked", channel_id=row.channel_id)
    await session.commit()
    return view(row, site_url)


async def access_token(session: AsyncSession, http: httpx.AsyncClient) -> str:
    """A fresh access token from the stored grant; a lost grant is recorded on the card."""
    row = await connection_row(session)
    values = stored_secrets(row)
    refresh = values.get("refresh_token")
    if not row.client_id or not values.get("client_secret") or not refresh or not row.channel_id:
        raise Refused(409, "video_youtube_not_linked", "還沒有連結 YouTube 頻道：到設定分頁連結")
    try:
        return await refresh_access_token(
            http,
            client_id=row.client_id,
            client_secret=values["client_secret"],
            refresh_token=refresh,
        )
    except AuthorizationLost as error:
        row.problem = LOST_GRANT
        await session.commit()
        raise Refused(409, "video_youtube_grant_lost", LOST_GRANT) from error


async def verify(session: AsyncSession) -> ConnectionView:
    """channels.list with the grant: refreshes the channel's name and when it was last checked."""
    row = await connection_row(session)
    site_url = await _site_url(session)
    if not linked(row):
        await session.commit()
        return view(row, site_url)
    async with http_client() as http:
        try:
            token = await access_token(session, http)
            channel = await YoutubeClient(http, token).my_channel()
        except Refused as error:
            if error.code == "video_youtube_grant_lost":
                return view(await connection_row(session), site_url)
            raise
        except YoutubeError as error:
            raise Refused(
                502, "video_youtube_verify_failed", f"YouTube 回覆：{error.message}"
            ) from error
        except httpx.HTTPError as error:
            raise Refused(502, "video_youtube_unreachable", "連不到 YouTube，請再試一次") from error
    row = await connection_row(session, lock=True)
    if channel is None or str(channel.get("id")) != row.channel_id:
        row.problem = "授權現在對應到另一個頻道或沒有頻道了，請重新連結"
    else:
        snippet = as_dict(channel.get("snippet"))
        row.channel_title = str(snippet.get("title") or row.channel_title or "")[:200] or None
        row.verified_at = datetime.now(UTC)
        row.problem = None
    await session.commit()
    return view(row, site_url)


async def unlink(session: AsyncSession, user: User) -> tuple[bool, ConnectionView]:
    """Ask Google to revoke the grant and forget it here, whether or not Google answered."""
    row = await connection_row(session, lock=True)
    values = stored_secrets(row)
    refresh = values.pop("refresh_token", None)
    revoked = True
    if refresh:
        async with http_client() as http:
            revoked = await revoke_token(http, refresh)
    _store_secrets(row, values)
    channel_id = row.channel_id
    row.channel_id = None
    row.channel_title = None
    row.scope = None
    row.linked_at = None
    row.linked_by_user_id = None
    row.verified_at = None
    row.problem = None
    _audit(session, user, "video_youtube_channel_unlinked", channel_id=channel_id, revoked=revoked)
    await session.commit()
    return revoked, view(row, await _site_url(session))
