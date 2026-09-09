from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.community.models import CreatorInvitation
from app.community.policy import fail
from app.config import get_settings
from app.models import User


def invitation_required() -> bool:
    return get_settings().discovery_enabled


def serialize_invitation(user_id: UUID, row: CreatorInvitation | None) -> dict[str, Any]:
    return {
        "user_id": str(user_id),
        "invited": bool(row and row.invited),
        "version": row.version if row else 0,
        "updated_at": row.updated_at if row else None,
    }


async def creator_invited(session: AsyncSession, user_id: UUID) -> bool:
    return bool(
        await session.scalar(
            select(CreatorInvitation.invited).where(CreatorInvitation.user_id == user_id)
        )
    )


async def lock_creator(session: AsyncSession, user_id: UUID) -> User:
    # A stable parent row serializes first-ever invitations as well as revocation.
    # Use this BEFORE Profile/Post locks, consistent with account erasure.
    user = await session.scalar(
        select(User)
        .where(User.id == user_id)
        .with_for_update(key_share=True)
        .execution_options(populate_existing=True)
    )
    if user is None or not user.is_active or user.deleted_at is not None:
        raise fail("community_not_found", 404)
    return user


async def require_creator_invitation(session: AsyncSession, user_id: UUID) -> None:
    if not invitation_required():
        return
    await lock_creator(session, user_id)
    row = await session.scalar(
        select(CreatorInvitation)
        .where(CreatorInvitation.user_id == user_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if row is None or not row.invited:
        raise fail("community_creator_invitation_required", 403)


async def erase_creator_invitation(session: AsyncSession, user_id: UUID) -> None:
    await session.execute(delete(CreatorInvitation).where(CreatorInvitation.user_id == user_id))
    await session.execute(
        update(CreatorInvitation)
        .where(CreatorInvitation.granted_by_user_id == user_id)
        .values(granted_by_user_id=None)
    )
