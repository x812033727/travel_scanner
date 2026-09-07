from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Header, Query, Request
from fastapi.responses import StreamingResponse
from redis.exceptions import RedisError
from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import CurrentUser, _authenticate
from app.community.content import published_post
from app.community.models import Conversation, Event, Message, Notification, Profile, Relationship
from app.community.policy import (
    blocked,
    digest,
    event,
    fail,
    member,
    notify,
    public_profile,
    rate,
    require_open,
    signal,
    visible_profile,
)
from app.community.router import OpenSession
from app.community.schemas import MessageInput, ReadInput
from app.db import SessionFactory
from app.infra import get_redis
from app.models import User
from app.problems import AppError

router = APIRouter(prefix="/community", tags=["community messaging"])


async def pair_allowed(
    session: AsyncSession, user: User, other: UUID, *, lock: bool = False
) -> None:
    if user.id == other:
        raise fail("community_self_action", 422)
    if lock:
        # Both directions and follow/block mutations share these row locks.
        await session.execute(
            select(Profile)
            .where(Profile.user_id.in_([user.id, other]))
            .order_by(Profile.user_id)
            .with_for_update()
        )
    await member(session, user, verified=True)
    await visible_profile(session, other, user)
    other_user = await session.get(User, other)
    if other_user is None or other_user.email_verified_at is None:
        raise fail("community_mutual_required", 403)
    count = await session.scalar(
        select(func.count())
        .select_from(Relationship)
        .where(
            Relationship.kind == "follow",
            or_(
                and_(Relationship.actor_id == user.id, Relationship.target_id == other),
                and_(Relationship.actor_id == other, Relationship.target_id == user.id),
            ),
        )
    )
    if count != 2 or await blocked(session, user.id, other):
        raise fail("community_mutual_required", 403)


async def conversation_for(
    session: AsyncSession, identifier: UUID, user: User
) -> tuple[Conversation, UUID]:
    await member(session, user)
    row = await session.get(Conversation, identifier)
    if row is None or user.id not in {row.first_user_id, row.second_user_id}:
        raise fail("community_not_found", 404)
    other = row.second_user_id if row.first_user_id == user.id else row.first_user_id
    return row, other


async def can_send(session: AsyncSession, user: User, other: UUID) -> bool:
    try:
        await pair_allowed(session, user, other)
        return True
    except AppError:
        return False


@router.post("/conversations/{other_id}", status_code=201)
async def begin_conversation(
    other_id: UUID, user: CurrentUser, session: OpenSession
) -> dict[str, str]:
    await require_open(session, "messaging_enabled")
    await rate(session, user)
    await pair_allowed(session, user, other_id, lock=True)
    first, second = sorted([user.id, other_id])
    row = await session.scalar(
        select(Conversation).where(
            Conversation.first_user_id == first,
            Conversation.second_user_id == second,
        )
    )
    if row is None:
        row = Conversation(first_user_id=first, second_user_id=second)
        session.add(row)
    await session.commit()
    return {"id": str(row.id)}


@router.get("/conversations")
async def conversations(user: CurrentUser, session: OpenSession) -> dict[str, Any]:
    await require_open(session, "messaging_enabled")
    await member(session, user)
    rows = (
        await session.scalars(
            select(Conversation)
            .where(
                or_(
                    Conversation.first_user_id == user.id,
                    Conversation.second_user_id == user.id,
                )
            )
            .order_by(Conversation.updated_at.desc())
            .limit(100)
        )
    ).all()
    items: list[dict[str, Any]] = []
    for row in rows:
        other = row.second_user_id if row.first_user_id == user.id else row.first_user_id
        if await blocked(session, user.id, other):
            continue
        profile = await session.get(Profile, other)
        read_id = row.first_read_id if row.first_user_id == user.id else row.second_read_id
        unread = await session.scalar(
            select(func.count())
            .select_from(Message)
            .where(
                Message.conversation_id == row.id,
                Message.sender_id != user.id,
                Message.id > read_id,
            )
        )
        items.append(
            {
                "id": str(row.id),
                "other": public_profile(profile)
                if profile and profile.deleted_at is None
                else None,
                "unread": unread or 0,
                "can_send": await can_send(session, user, other),
            }
        )
    return {"items": items}


@router.get("/conversations/{identifier}/messages")
async def messages(
    identifier: UUID,
    user: CurrentUser,
    session: OpenSession,
    after: Annotated[int | None, Query(ge=0)] = None,
    before: Annotated[int | None, Query(ge=1)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> dict[str, Any]:
    await require_open(session, "messaging_enabled")
    await member(session, user)
    conversation, other = await conversation_for(session, identifier, user)
    if await blocked(session, user.id, other):
        raise fail("community_not_found", 404)
    if after is not None and before is not None:
        raise fail("community_invalid_cursor", 422)
    query = select(Message).where(Message.conversation_id == identifier)
    if after is not None:
        query = query.where(Message.id > after).order_by(Message.id)
    else:
        if before is not None:
            query = query.where(Message.id < before)
        query = query.order_by(Message.id.desc())
    rows = (await session.scalars(query.limit(limit + 1))).all()
    items: list[dict[str, Any]] = []
    selected = list(rows[:limit])
    if after is None:
        selected.reverse()
    for row in selected:
        card = None
        if row.card_post_id:
            try:
                post, revision, profile = await published_post(session, row.card_post_id, user)
                card = {"id": str(post.id), "title": revision.title, "author": profile.display_name}
            except AppError as exc:
                if exc.status != 404:
                    raise
        sender = await session.get(User, row.sender_id)
        items.append(
            {
                "id": row.id,
                "sender_id": str(row.sender_id) if sender and sender.is_active else None,
                "mine": row.sender_id == user.id,
                "body": row.body,
                "card": card,
                "card_unavailable": row.card_post_id is not None and card is None,
                "created_at": row.created_at,
            }
        )
    return {
        "items": items,
        "next_cursor": rows[limit - 1].id if len(rows) > limit else None,
        "latest_cursor": selected[-1].id if selected else after or 0,
        "can_send": await can_send(session, user, other),
        "other_read_id": conversation.second_read_id
        if conversation.first_user_id == user.id
        else conversation.first_read_id,
    }


@router.post("/conversations/{identifier}/messages", status_code=201)
async def send_message(
    identifier: UUID,
    payload: MessageInput,
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, Any]:
    await require_open(session, "messaging_enabled")
    conversation, other = await conversation_for(session, identifier, user)
    await pair_allowed(session, user, other, lock=True)
    fingerprint = digest({**payload.model_dump(mode="json"), "conversation": str(identifier)})
    replay = await session.scalar(
        select(Message).where(
            Message.sender_id == user.id,
            Message.idempotency_key == payload.idempotency_key,
        )
    )
    if replay:
        if replay.request_hash != fingerprint:
            raise fail("community_idempotency_conflict", 409)
        return {"id": replay.id, "replayed": True}
    await rate(session, user)
    if payload.card_post_id:
        await published_post(session, payload.card_post_id, user)
        # Do not deliver a card that is blocked for its recipient.
        recipient = await session.get(User, other)
        await published_post(session, payload.card_post_id, recipient)
    message = Message(
        conversation_id=identifier,
        sender_id=user.id,
        body=payload.body,
        card_post_id=payload.card_post_id,
        idempotency_key=payload.idempotency_key,
        request_hash=fingerprint,
    )
    session.add(message)
    conversation.updated_at = datetime.now(UTC)
    await session.flush()
    await notify(session, other, user.id, "message", str(identifier))
    await event(session, user.id, "message", str(identifier))
    await session.commit()
    await signal(other)
    await signal(user.id)
    return {"id": message.id, "replayed": False}


@router.put("/conversations/{identifier}/read")
async def read_messages(
    identifier: UUID,
    payload: ReadInput,
    user: CurrentUser,
    session: OpenSession,
) -> dict[str, bool]:
    await require_open(session, "messaging_enabled")
    conversation, other = await conversation_for(session, identifier, user)
    if await blocked(session, user.id, other):
        raise fail("community_not_found", 404)
    maximum = await session.scalar(
        select(func.max(Message.id)).where(Message.conversation_id == identifier)
    )
    through = min(payload.through_id, maximum or 0)
    field = (
        Conversation.first_read_id
        if conversation.first_user_id == user.id
        else Conversation.second_read_id
    )
    await session.execute(
        update(Conversation)
        .where(Conversation.id == identifier, field < through)
        .values({field.key: through})
    )
    await event(session, other, "read", str(identifier))
    await session.commit()
    await signal(other)
    return {"read": True}


@router.get("/notifications")
async def notifications(
    user: CurrentUser,
    session: OpenSession,
    before: Annotated[int | None, Query(ge=1)] = None,
) -> dict[str, Any]:
    await member(session, user)
    query = select(Notification).where(Notification.recipient_id == user.id)
    excluded = (
        select(Relationship.target_id)
        .where(
            Relationship.actor_id == user.id,
            Relationship.kind == "block",
        )
        .union(
            select(Relationship.actor_id).where(
                Relationship.target_id == user.id,
                Relationship.kind == "block",
            )
        )
    )
    query = query.where(
        or_(Notification.actor_id.is_(None), Notification.actor_id.not_in(excluded))
    )
    unread = await session.scalar(
        select(func.count()).select_from(
            query.where(
                Notification.read_at.is_(None),
            ).subquery()
        )
    )
    if before:
        query = query.where(Notification.id < before)
    rows = (await session.scalars(query.order_by(Notification.id.desc()).limit(51))).all()
    items: list[dict[str, Any]] = []
    for row in rows[:50]:
        profile = await session.get(Profile, row.actor_id) if row.actor_id else None
        items.append(
            {
                "id": row.id,
                "kind": row.kind,
                "target": row.target,
                "read": row.read_at is not None,
                "created_at": row.created_at,
                "actor": public_profile(profile) if profile and not profile.deleted_at else None,
            }
        )
    return {
        "items": items,
        "unread": unread or 0,
        "next_cursor": rows[49].id if len(rows) > 50 else None,
    }


@router.put("/notifications/read")
async def read_notifications(
    payload: ReadInput, user: CurrentUser, session: OpenSession
) -> dict[str, bool]:
    await member(session, user)
    await session.execute(
        update(Notification)
        .where(
            Notification.recipient_id == user.id,
            Notification.id <= payload.through_id,
            Notification.read_at.is_(None),
        )
        .values(read_at=datetime.now(UTC))
    )
    await session.commit()
    return {"read": True}


@router.get("/events")
async def events(
    request: Request,
    user: CurrentUser,
    session: OpenSession,
    after: Annotated[int, Query(ge=0)] = 0,
    last_event_id: Annotated[str | None, Header()] = None,
) -> StreamingResponse:
    if last_event_id:
        try:
            after = max(after, int(last_event_id))
        except ValueError as exc:
            raise fail("community_invalid_cursor", 422) from exc
    token = request.cookies.get("travel_access", "")
    authorization = request.headers.get("authorization", "")
    if authorization.lower().startswith("bearer "):
        token = authorization[7:]
    recipient_id = user.id
    await session.rollback()  # Do not hold a request transaction for the stream's lifetime.

    async def stream() -> AsyncIterator[str]:
        cursor = after
        previous_policy = ""
        pubsub = get_redis().pubsub()
        try:
            await pubsub.subscribe(f"community:{recipient_id}")
            for _ in range(25):
                if await request.is_disconnected():
                    break
                async with SessionFactory() as fresh:
                    # Cookie revocation, account suspension and global switches are
                    # checked on every catch-up, including already-connected readers.
                    authenticated, _, _ = await _authenticate(fresh, token)
                    effective = await require_open(fresh)
                    await member(fresh, authenticated)
                    policy = json.dumps(
                        {
                            key: value
                            for key, value in effective.model_dump().items()
                            if key == "enabled" or key.endswith("_enabled")
                        }
                    )
                    if policy != previous_policy:
                        previous_policy = policy
                        yield f"event: policy\ndata: {policy}\n\n"
                    rows = (
                        await fresh.scalars(
                            select(Event)
                            .where(
                                Event.recipient_id == recipient_id,
                                Event.id > cursor,
                            )
                            .order_by(Event.id)
                            .limit(100)
                        )
                    ).all()
                    for row in rows:
                        cursor = row.id
                        data = json.dumps({"kind": row.kind, "target": row.target})
                        yield f"id: {row.id}\ndata: {data}\n\n"
                yield ": keepalive\n\n"
                await pubsub.get_message(ignore_subscribe_messages=True, timeout=2)
                await asyncio.sleep(0.05)
        except (AppError, RedisError):
            yield "event: unavailable\ndata: {}\n\n"
        finally:
            await pubsub.aclose()  # type: ignore[no-untyped-call]

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "private, no-store",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/events/cursor")
async def event_cursor(user: CurrentUser, session: OpenSession) -> dict[str, int]:
    await member(session, user)
    value = await session.scalar(select(func.max(Event.id)).where(Event.recipient_id == user.id))
    return {"cursor": value or 0}
