from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.discovery.models import DiscoveryDismissal, DiscoveryPreference
from app.discovery.schemas import PreferenceInput
from app.models import User
from app.problems import AppError


def payload(row: DiscoveryPreference | None) -> dict[str, Any]:
    return {
        "version": row.version if row else 0,
        "destinations": row.destinations if row else [],
        "topics": row.topics if row else [],
        "include_saved": row.include_saved if row else False,
        "include_following": row.include_following if row else False,
    }


async def get_preferences(session: AsyncSession, user_id: UUID) -> dict[str, Any]:
    return payload(await session.get(DiscoveryPreference, user_id))


async def locked_user(session: AsyncSession, user_id: UUID) -> None:
    # Lock order matches account erasure: user before per-feature rows. It also
    # serializes concurrent first writes, for which there is no preference row yet.
    user = await session.scalar(
        select(User)
        .where(User.id == user_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if not user or not user.is_active or user.deleted_at:
        raise AppError(401, "authentication_required", "Authentication required")


async def update_preferences(
    session: AsyncSession, user_id: UUID, data: PreferenceInput
) -> dict[str, Any]:
    await locked_user(session, user_id)
    row = await session.scalar(
        select(DiscoveryPreference)
        .where(DiscoveryPreference.user_id == user_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if data.version != (row.version if row else 0):
        raise AppError(409, "discovery_version_conflict", "偏好已更新，請重新載入後儲存")
    if row is None:
        row = DiscoveryPreference(user_id=user_id, version=1)
        session.add(row)
    else:
        row.version += 1
    for name, value in data.model_dump(exclude={"version"}).items():
        setattr(row, name, value)
    row.updated_at = datetime.now(UTC)
    await session.flush()
    return payload(row)


async def erase_preferences(session: AsyncSession, user_id: UUID) -> None:
    """Account erasure owns the transaction; never commit from a shared helper."""
    await session.execute(delete(DiscoveryDismissal).where(DiscoveryDismissal.user_id == user_id))
    await session.execute(delete(DiscoveryPreference).where(DiscoveryPreference.user_id == user_id))
