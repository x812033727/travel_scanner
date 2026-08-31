from __future__ import annotations

import json
import re
import secrets
from datetime import UTC, datetime
from typing import Annotated, Any, cast
from urllib.parse import quote, urlencode
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Header, Request, Response
from pydantic import BaseModel, Field
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser
from app.config import Settings, get_settings
from app.db import get_session
from app.infra import enforce_named_rate_limit, get_redis
from app.line.client import LineApiError, LineMessagingClient, verify_webhook_signature
from app.models import LineConnection, PriceAlert
from app.problems import AppError

router = APIRouter(prefix="/line", tags=["line"])
Session = Annotated[AsyncSession, Depends(get_session)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
RedisDep = Annotated[Redis, Depends(get_redis)]
LINE_LINK_TOKEN_RE = re.compile(r"^[A-Za-z0-9_-]{10,512}$")


class LineConnectionView(BaseModel):
    configured: bool
    status: str
    display_name: str | None = None
    masked_user_id: str | None = None
    official_account_id: str | None = None
    add_friend_url: str | None = None
    linked_at: datetime | None = None


class LineLinkSessionCreate(BaseModel):
    link_token: str = Field(min_length=10, max_length=512)


class LineLinkSessionResponse(BaseModel):
    redirect_url: str
    expires_in: int = 600


def _require_line(settings: Settings) -> None:
    if not settings.line_messaging_configured:
        raise AppError(503, "line_not_configured", "LINE 價格通知尚未啟用")


def _mask_line_user_id(value: str) -> str:
    if len(value) <= 10:
        return "••••"
    return f"{value[:3]}••••{value[-4:]}"


def _add_friend_url(settings: Settings) -> str | None:
    if settings.line_add_friend_url:
        return settings.line_add_friend_url
    if not settings.line_official_account_id:
        return None
    return f"https://line.me/R/ti/p/{quote(settings.line_official_account_id, safe='@')}"


async def _connection_for_user(session: AsyncSession, user_id: UUID) -> LineConnection | None:
    return cast(
        LineConnection | None,
        await session.scalar(select(LineConnection).where(LineConnection.user_id == user_id)),
    )


@router.get("/connection", response_model=LineConnectionView)
async def line_connection(
    user: CurrentUser, session: Session, settings: SettingsDep
) -> LineConnectionView:
    connection = await _connection_for_user(session, user.id)
    status = "unlinked"
    if connection is not None:
        status = "linked" if connection.friend_status else "blocked"
    return LineConnectionView(
        configured=settings.line_messaging_configured,
        status=status,
        display_name=connection.display_name if connection else None,
        masked_user_id=_mask_line_user_id(connection.line_user_id) if connection else None,
        official_account_id=settings.line_official_account_id,
        add_friend_url=_add_friend_url(settings),
        linked_at=connection.linked_at if connection else None,
    )


@router.post("/link-session", response_model=LineLinkSessionResponse)
async def create_line_link_session(
    payload: LineLinkSessionCreate,
    user: CurrentUser,
    redis: RedisDep,
    settings: SettingsDep,
) -> LineLinkSessionResponse:
    _require_line(settings)
    if not LINE_LINK_TOKEN_RE.fullmatch(payload.link_token):
        raise AppError(422, "invalid_line_link_token", "LINE 連結權杖格式不正確")
    await enforce_named_rate_limit("line_link", str(user.id), limit=5, window_seconds=600)
    nonce = secrets.token_urlsafe(32)
    await redis.set(f"line:link:nonce:{nonce}", str(user.id), ex=600, nx=True)
    query = urlencode({"linkToken": payload.link_token, "nonce": nonce})
    return LineLinkSessionResponse(
        redirect_url=f"https://access.line.me/dialog/bot/accountLink?{query}"
    )


@router.delete("/connection", status_code=204)
async def unlink_line_connection(user: CurrentUser, session: Session) -> None:
    connection = await _connection_for_user(session, user.id)
    if connection is not None:
        await session.delete(connection)
        await session.commit()


@router.post("/test-message", status_code=204)
async def send_line_test_message(
    user: CurrentUser, session: Session, settings: SettingsDep
) -> None:
    _require_line(settings)
    await enforce_named_rate_limit("line_test", str(user.id), limit=1, window_seconds=60)
    connection = await _connection_for_user(session, user.id)
    if connection is None:
        raise AppError(409, "line_not_linked", "尚未連結 LINE 帳號")
    if not connection.friend_status:
        raise AppError(409, "line_friend_required", "請重新加入 LINE 官方帳號好友")
    try:
        await LineMessagingClient(settings).push_text(
            connection.line_user_id,
            "Travel Scanner LINE 價格通知已成功連結。",
            retry_key=uuid4(),
        )
    except LineApiError as exc:
        connection.last_delivery_error = str(exc)
        await session.commit()
        raise AppError(503, "line_delivery_failed", "LINE 測試訊息暫時無法送出") from exc
    connection.last_delivery_at = datetime.now(UTC)
    connection.last_delivery_error = None
    await session.commit()


async def _send_link_prompt(
    client: LineMessagingClient,
    settings: Settings,
    line_user_id: str,
    reply_token: str,
) -> None:
    link_token = await client.issue_link_token(line_user_id)
    link_url = (
        f"{settings.next_public_site_url.rstrip('/')}/line/link?"
        f"{urlencode({'linkToken': link_token})}"
    )
    await client.reply_link(reply_token, link_url)


async def _handle_account_link(
    event: dict[str, Any],
    session: AsyncSession,
    redis: Redis,
    client: LineMessagingClient,
) -> None:
    source = event.get("source") or {}
    link = event.get("link") or {}
    line_user_id = source.get("userId")
    nonce = link.get("nonce")
    reply_token = event.get("replyToken")
    if (
        link.get("result") != "ok"
        or not isinstance(line_user_id, str)
        or not isinstance(nonce, str)
    ):
        if isinstance(reply_token, str):
            await client.reply_text(reply_token, "帳號連結未完成，請重新輸入「綁定」再試一次。")
        return
    nonce_key = f"line:link:nonce:{nonce}"
    user_id_value = await redis.get(nonce_key)
    if not isinstance(user_id_value, str):
        if isinstance(reply_token, str):
            await client.reply_text(reply_token, "連結已過期，請重新輸入「綁定」。")
        return
    user_id = UUID(user_id_value)
    by_user = await session.scalar(select(LineConnection).where(LineConnection.user_id == user_id))
    by_line = await session.scalar(
        select(LineConnection).where(LineConnection.line_user_id == line_user_id)
    )
    if (by_user and by_user.line_user_id != line_user_id) or (
        by_line and by_line.user_id != user_id
    ):
        await redis.delete(nonce_key)
        if isinstance(reply_token, str):
            await client.reply_text(reply_token, "此帳號已有其他 LINE 綁定，請先到網站解除連結。")
        return
    profile = await client.profile(line_user_id)
    display_name = str(profile.get("displayName") or "LINE 使用者")[:255]
    connection = by_user or by_line
    if connection is None:
        connection = LineConnection(
            user_id=user_id,
            line_user_id=line_user_id,
            display_name=display_name,
            friend_status=True,
            linked_at=datetime.now(UTC),
        )
        session.add(connection)
    else:
        connection.display_name = display_name
        connection.friend_status = True
        connection.linked_at = datetime.now(UTC)
    alerts = list(
        (
            await session.scalars(
                select(PriceAlert).where(
                    PriceAlert.user_id == user_id,
                    PriceAlert.active.is_(True),
                    PriceAlert.monitoring_mode == "automatic",
                )
            )
        ).all()
    )
    for alert in alerts:
        alert.next_check_at = datetime.now(UTC)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        await redis.delete(nonce_key)
        if isinstance(reply_token, str):
            await client.reply_text(reply_token, "此 LINE 或網站帳號已被連結，請先解除原連結。")
        return
    await redis.delete(nonce_key)
    if isinstance(reply_token, str):
        await client.reply_text(reply_token, f"已連結 Travel Scanner 帳號（{display_name}）。")


async def _handle_event(
    event: dict[str, Any],
    session: AsyncSession,
    redis: Redis,
    settings: Settings,
) -> None:
    event_id = event.get("webhookEventId")
    if isinstance(event_id, str) and await redis.exists(f"line:webhook:done:{event_id}"):
        return
    lock_key = f"line:webhook:lock:{event_id or secrets.token_hex(12)}"
    if not await redis.set(lock_key, "1", ex=120, nx=True):
        return
    client = LineMessagingClient(settings)
    try:
        event_type = event.get("type")
        source = event.get("source") or {}
        line_user_id = source.get("userId")
        reply_token = event.get("replyToken")
        if event_type == "accountLink":
            await _handle_account_link(event, session, redis, client)
        elif event_type == "unfollow" and isinstance(line_user_id, str):
            connection = await session.scalar(
                select(LineConnection).where(LineConnection.line_user_id == line_user_id)
            )
            if connection is not None:
                connection.friend_status = False
                await session.commit()
        elif event_type in {"follow", "message"} and isinstance(line_user_id, str):
            if not isinstance(reply_token, str):
                return
            message = event.get("message") or {}
            text = str(message.get("text") or "").strip()
            if event_type == "follow" or text in {"綁定", "連結帳號", "綁定帳號"}:
                existing = await session.scalar(
                    select(LineConnection).where(LineConnection.line_user_id == line_user_id)
                )
                if existing is not None:
                    existing.friend_status = True
                    await session.commit()
                    await client.reply_text(reply_token, "這個 LINE 已連結 Travel Scanner 帳號。")
                else:
                    await _send_link_prompt(client, settings, line_user_id, reply_token)
        if isinstance(event_id, str):
            await redis.set(f"line:webhook:done:{event_id}", "1", ex=604_800)
    finally:
        await redis.delete(lock_key)


@router.post("/webhook", include_in_schema=False)
async def line_webhook(
    request: Request,
    session: Session,
    redis: RedisDep,
    settings: SettingsDep,
    x_line_signature: Annotated[str | None, Header(alias="X-Line-Signature")] = None,
) -> Response:
    _require_line(settings)
    body = await request.body()
    if len(body) > settings.line_webhook_max_body_bytes:
        raise AppError(413, "line_webhook_too_large", "LINE webhook 內容過大")
    if not x_line_signature or not verify_webhook_signature(
        body, x_line_signature, settings.line_channel_secret or ""
    ):
        raise AppError(401, "invalid_line_signature", "LINE webhook 簽章無效")
    try:
        payload = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AppError(400, "invalid_line_webhook", "LINE webhook 格式無效") from exc
    events = payload.get("events", []) if isinstance(payload, dict) else []
    if not isinstance(events, list):
        raise AppError(400, "invalid_line_webhook", "LINE webhook 事件格式無效")
    try:
        for event in events:
            if isinstance(event, dict):
                await _handle_event(event, session, redis, settings)
    except LineApiError as exc:
        raise AppError(503, "line_api_unavailable", "LINE API 暫時無法使用") from exc
    return Response(status_code=200)
