from __future__ import annotations

import base64
import hashlib
import json
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from pydantic import ValidationError
from sqlalchemy import and_, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.community.models import Event, Notification, Profile, Relationship
from app.community.schemas import CommunitySettings
from app.config import get_settings
from app.infra import enforce_named_rate_limit
from app.models import AdminAuditLog, ProviderConfig, User
from app.problems import AppError


def fail(code: str, status: int = 400) -> AppError:
    # The client renders these codes from the five-locale message catalog.
    return AppError(status, code, code)


def aware(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


async def settings_for(session: AsyncSession) -> CommunitySettings:
    row = await session.scalar(select(ProviderConfig).where(ProviderConfig.provider == "community"))
    defaults = {"enabled": get_settings().community_enabled}
    try:
        return CommunitySettings.model_validate({**defaults, **(row.config if row else {})})
    except ValidationError as exc:
        raise fail("community_unavailable", 503) from exc


async def require_open(session: AsyncSession, feature: str | None = None) -> CommunitySettings:
    settings = await settings_for(session)
    if not settings.enabled or (feature and not getattr(settings, feature)):
        raise fail("community_closed", 403)
    return settings


async def member(
    session: AsyncSession, user: User, *, verified: bool = False, lock: bool = False
) -> Profile:
    statement = select(Profile).where(Profile.user_id == user.id, Profile.deleted_at.is_(None))
    if lock:
        statement = statement.with_for_update()
    profile = await session.scalar(statement)
    if profile is None:
        raise fail("community_profile_required", 403)
    if not user.is_active or profile.restricted:
        raise fail("community_restricted", 403)
    if verified and user.email_verified_at is None:
        raise fail("community_verification_required", 403)
    return profile


async def rate(session: AsyncSession, user: User, feature: str = "interaction") -> None:
    settings = await settings_for(session)
    limit = settings.interactions_per_minute
    window = 60
    if feature == "upload":
        limit, window = settings.uploads_per_day, 86400
    if feature == "publish":
        limit, window = settings.posts_per_day, 86400
    await enforce_named_rate_limit(
        f"community:{feature}", str(user.id), limit=limit, window_seconds=window
    )


async def blocked(session: AsyncSession, first: UUID, second: UUID) -> bool:
    return (
        await session.scalar(
            select(Relationship.id)
            .where(
                Relationship.kind == "block",
                or_(
                    and_(Relationship.actor_id == first, Relationship.target_id == second),
                    and_(Relationship.actor_id == second, Relationship.target_id == first),
                ),
            )
            .limit(1)
        )
        is not None
    )


async def visible_profile(session: AsyncSession, user_id: UUID, viewer: User | None) -> Profile:
    row = await session.scalar(
        select(Profile)
        .join(User, User.id == Profile.user_id)
        .where(
            Profile.user_id == user_id,
            Profile.deleted_at.is_(None),
            Profile.restricted.is_(False),
            User.is_active.is_(True),
            User.deleted_at.is_(None),
        )
    )
    if row is None or (viewer and await blocked(session, viewer.id, user_id)):
        raise fail("community_not_found", 404)
    return row


def public_profile(profile: Profile) -> dict[str, Any]:
    return {
        "id": str(profile.user_id),
        "handle": profile.handle,
        "display_name": profile.display_name,
        "bio": profile.bio,
        "languages": profile.languages,
        "destinations": profile.destinations,
        "avatar_id": str(profile.avatar_id) if profile.avatar_id else None,
    }


async def notify(
    session: AsyncSession, recipient: UUID, actor: UUID | None, kind: str, target: str
) -> None:
    if actor == recipient or (actor and await blocked(session, recipient, actor)):
        return
    profile = await session.get(Profile, recipient)
    if profile is None or profile.deleted_at is not None or profile.restricted:
        return
    if profile.notification_preferences.get(kind, True):
        session.add(Notification(recipient_id=recipient, actor_id=actor, kind=kind, target=target))
    await event(session, recipient, kind, target)


async def event(session: AsyncSession, recipient: UUID, kind: str, target: str) -> None:
    # Serializing event allocation until commit prevents a reconnect cursor from
    # skipping a lower sequence number that committed after a higher one.
    if session.get_bind().dialect.name == "postgresql":
        await session.execute(text("SELECT pg_advisory_xact_lock(6842061907)"))
    session.add(Event(recipient_id=recipient, kind=kind, target=target))


async def metric(session: AsyncSession, user_id: UUID, kind: str, target: str) -> None:
    from sqlalchemy.exc import IntegrityError

    from app.community.models import CommunityMetric

    try:
        async with session.begin_nested():
            session.add(
                CommunityMetric(
                    day=datetime.now(UTC).date().isoformat(),
                    user_id=user_id,
                    kind=kind,
                    target=target,
                )
            )
            await session.flush()
    except IntegrityError:
        pass


async def signal(recipient: UUID) -> None:
    from redis.exceptions import RedisError

    from app.infra import get_redis

    try:
        await get_redis().publish(f"community:{recipient}", "refresh")
    except RedisError:
        # Events are already committed. The SSE reader also polls the durable cursor.
        pass


def audit(session: AsyncSession, actor: User, action: str, target: str, **data: Any) -> None:
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action=action,
            target=target,
            metadata_json=data,
        )
    )


def cursor_encode(moment: datetime, identifier: UUID) -> str:
    return (
        base64.urlsafe_b64encode(json.dumps([aware(moment).isoformat(), str(identifier)]).encode())
        .decode()
        .rstrip("=")
    )


def cursor_decode(value: str | None) -> tuple[datetime, UUID] | None:
    if not value:
        return None
    try:
        if len(value) > 256:
            raise ValueError("cursor too long")
        moment, identifier = json.loads(base64.urlsafe_b64decode(value + "=" * (-len(value) % 4)))
        return aware(datetime.fromisoformat(moment)), UUID(identifier)
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        raise fail("community_invalid_cursor", 422) from exc


def risky(text: str, settings: CommunitySettings) -> bool:
    lowered = text.casefold()
    return lowered.count("http") > 3 or any(term in lowered for term in settings.risk_terms)
