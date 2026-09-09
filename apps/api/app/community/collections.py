"""Existing private collection storage, independent of social-profile enrollment.

Callers enforce their own rollout policy. These services always check the active
account and ownership, and reauthorize referenced content on every read/write.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import Locale
from app.community.models import Collection, CollectionItem
from app.community.policy import fail, rate
from app.community.schemas import CollectionInput, CollectionItemInput
from app.models import User


async def active_account(session: AsyncSession, user: User, *, lock: bool = False) -> None:
    query = select(User.id).where(
        User.id == user.id, User.is_active.is_(True), User.deleted_at.is_(None)
    )
    if lock:
        query = query.with_for_update(key_share=True)
    if await session.scalar(query) is None:
        raise fail("authentication_required", 401)


async def owned_collection(
    session: AsyncSession, user: User, identifier: UUID, *, lock: bool = False
) -> Collection:
    await active_account(session, user, lock=lock)
    query = select(Collection).where(Collection.id == identifier, Collection.user_id == user.id)
    if lock:
        query = query.with_for_update()
    row = await session.scalar(query.execution_options(populate_existing=True))
    if row is None:
        raise fail("community_not_found", 404)
    return row


async def list_collections(session: AsyncSession, user: User) -> dict[str, Any]:
    await active_account(session, user)
    rows = (
        await session.scalars(
            select(Collection)
            .where(Collection.user_id == user.id)
            .order_by(Collection.created_at, Collection.id)
            .limit(100)
        )
    ).all()
    return {"items": [{"id": str(row.id), "name": row.name} for row in rows]}


async def create_collection(session: AsyncSession, user: User, name: str) -> dict[str, str]:
    payload = CollectionInput(name=name)
    await active_account(session, user, lock=True)
    await rate(session, user)
    count = await session.scalar(
        select(func.count()).select_from(Collection).where(Collection.user_id == user.id)
    )
    if (count or 0) >= 100:
        raise fail("community_collection_limit", 403)
    row = Collection(user_id=user.id, name=payload.name)
    session.add(row)
    await session.commit()
    return {"id": str(row.id), "name": row.name}


async def collection_items(
    session: AsyncSession, user: User, identifier: UUID, locale: Locale
) -> dict[str, Any]:
    from app.discovery.service import resolve_discovery_items

    collection = await owned_collection(session, user, identifier)
    rows = list(
        (
            await session.scalars(
                select(CollectionItem)
                .where(CollectionItem.collection_id == identifier)
                .order_by(CollectionItem.created_at.desc(), CollectionItem.id)
                .limit(500)
            )
        ).all()
    )
    keys: list[str | None] = []
    for row in rows:
        # Older collections can contain pet places and provider restaurant IDs.
        # Unsupported references remain privately removable instead of poisoning
        # a whole discovery collection; their original community view is intact.
        try:
            target = str(UUID(row.target))
        except ValueError:
            keys.append(None)
            continue
        keys.append(
            f"{row.kind}:{target}"
            if row.kind in {"hotspot", "food", "merchant", "hotel", "guide", "post"}
            else None
        )
    supported_keys = [key for key in keys if key is not None]
    resolved = {}
    for offset in range(0, len(supported_keys), 100):
        for item in await resolve_discovery_items(
            session, supported_keys[offset : offset + 100], user, locale
        ):
            resolved[item.id] = item
    items = []
    for row, key in zip(rows, keys, strict=True):
        value = resolved.get(key) if key is not None else None
        items.append(
            {
                "id": str(row.id),
                "kind": row.kind,
                "target": row.target,
                **(
                    {"discovery": value.model_dump(mode="json")} if value else {"unavailable": True}
                ),
            }
        )
    return {"id": str(collection.id), "name": collection.name, "items": items}


async def collect_reference(
    session: AsyncSession,
    user: User,
    identifier: UUID,
    kind: str,
    target: str,
    locale: Locale = "zh-TW",
) -> dict[str, bool]:
    from app.discovery.service import resolve_discovery_items

    payload = CollectionItemInput.model_validate({"kind": kind, "target": target})
    # All discovery references are canonical UUIDs, including the existing kinds.
    try:
        canonical = str(UUID(payload.target))
    except ValueError as exc:
        raise fail("community_not_found", 404) from exc
    await owned_collection(session, user, identifier, lock=True)
    await rate(session, user)
    key = f"{payload.kind}:{canonical}"
    if not await resolve_discovery_items(session, [key], user, locale):
        raise fail("community_not_found", 404)
    existing = await session.scalar(
        select(CollectionItem.id).where(
            CollectionItem.collection_id == identifier,
            CollectionItem.kind == payload.kind,
            func.lower(func.replace(CollectionItem.target, "-", "")) == UUID(canonical).hex,
        )
    )
    if existing is None:
        count = await session.scalar(
            select(func.count())
            .select_from(CollectionItem)
            .where(CollectionItem.collection_id == identifier)
        )
        if (count or 0) >= 500:
            raise fail("community_collection_limit", 403)
        session.add(CollectionItem(collection_id=identifier, kind=payload.kind, target=canonical))
        from app.analytics.service import record_event

        await record_event(
            session,
            "content_saved",
            path="/explore/collections",
            user_id=user.id,
            properties={"kind": payload.kind},
        )
    await session.commit()
    return {"collected": True, "created": existing is None}


async def remove_reference(
    session: AsyncSession, user: User, identifier: UUID, item_id: UUID
) -> dict[str, bool]:
    await owned_collection(session, user, identifier, lock=True)
    await session.execute(
        delete(CollectionItem).where(
            CollectionItem.collection_id == identifier, CollectionItem.id == item_id
        )
    )
    await session.commit()
    return {"deleted": True}


async def delete_collection(session: AsyncSession, user: User, identifier: UUID) -> dict[str, bool]:
    row = await owned_collection(session, user, identifier, lock=True)
    await session.execute(delete(CollectionItem).where(CollectionItem.collection_id == identifier))
    await session.delete(row)
    await session.commit()
    return {"deleted": True}
