"""Existing private collection storage, independent of social-profile enrollment.

Callers enforce their own rollout policy. These services always check the active
account and ownership, and reauthorize referenced content on every read/write.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import Locale
from app.community.models import Collection, CollectionItem
from app.community.policy import fail
from app.community.policy import rate as rate
from app.community.schemas import CollectionInput
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
    query = select(Collection).where(
        Collection.id == identifier, Collection.user_id == user.id, Collection.system_role.is_(None)
    )
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
            .where(Collection.user_id == user.id, Collection.system_role.is_(None))
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
        select(func.count())
        .select_from(Collection)
        .where(Collection.user_id == user.id, Collection.system_role.is_(None))
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
    from app.saved.service import canonical, project_rows

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
    projections = []
    for offset in range(0, len(rows), 100):
        projections.extend(
            await project_rows(
                session,
                user,
                [
                    SimpleNamespace(
                        kind=canonical(row.kind, row.target)[0],
                        target=canonical(row.kind, row.target)[1],
                        saved_at=row.created_at,
                    )
                    for row in rows[offset : offset + 100]
                ],
                locale,
            )
        )
    items = [
        {**value, "id": str(row.id), "kind": row.kind, "target": row.target}
        for row, value in zip(rows, projections, strict=True)
    ]
    return {"id": str(collection.id), "name": collection.name, "items": items}


async def collect_reference(
    session: AsyncSession,
    user: User,
    identifier: UUID,
    kind: str,
    target: str,
    locale: Locale = "zh-TW",
) -> dict[str, Any]:
    from app.saved.service import (
        canonical,
        collection_columns,
        key_for,
        public_id,
        save_reference,
        states,
    )

    input_kind = kind
    kind, target = canonical(kind, target, strict=True)
    await owned_collection(session, user, identifier, lock=True)
    await save_reference(session, user, input_kind, target)
    column_kind, column_target = collection_columns()
    existing = await session.scalar(
        select(CollectionItem.id).where(
            CollectionItem.collection_id == identifier,
            column_kind == kind,
            column_target == target,
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
        stored = public_id(kind, target)
        # Collection storage is reference-only and bounded; Google restaurant IDs are opaque.
        session.add(CollectionItem(collection_id=identifier, kind=kind, target=stored))
        await session.flush()
    state = (await states(session, user, [key_for(kind, target)]))["items"][0]
    await session.commit()
    return {"collected": True, "created": existing is None, **state}


async def remove_reference(
    session: AsyncSession, user: User, identifier: UUID, item_id: UUID
) -> dict[str, Any]:
    from app.saved.service import canonical, collection_columns, ensure_base, key_for, states

    await owned_collection(session, user, identifier, lock=True)
    await rate(session, user)
    row = await session.scalar(
        select(CollectionItem).where(
            CollectionItem.collection_id == identifier, CollectionItem.id == item_id
        )
    )
    key = key_for(row.kind, row.target) if row else None
    if row is not None:
        await ensure_base(session, user, row.kind, row.target, saved_at=row.created_at)
        kind, target = canonical(row.kind, row.target)
        column_kind, column_target = collection_columns()
        # Old clients could store case/UUID-format or hotel/service aliases as
        # distinct physical rows. Removing the logical membership clears them
        # all in this list, while the base save and other lists remain intact.
        await session.execute(
            delete(CollectionItem).where(
                CollectionItem.collection_id == identifier,
                column_kind == kind,
                column_target == target,
            )
        )
    result = (await states(session, user, [key]))["items"][0] if key else {}
    await session.commit()
    return {"deleted": True, **result}


async def delete_collection(session: AsyncSession, user: User, identifier: UUID) -> dict[str, bool]:
    from app.saved.service import ensure_base

    row = await owned_collection(session, user, identifier, lock=True)
    await rate(session, user)
    # Named lists are capped at 500; fail closed if legacy corruption exceeds that bound.
    items = list(
        (
            await session.scalars(
                select(CollectionItem).where(CollectionItem.collection_id == identifier).limit(501)
            )
        ).all()
    )
    if len(items) > 500:
        raise fail("community_collection_limit", 403)
    for item in items:
        await ensure_base(session, user, item.kind, item.target, saved_at=item.created_at)
    await session.execute(delete(CollectionItem).where(CollectionItem.collection_id == identifier))
    await session.delete(row)
    await session.commit()
    return {"deleted": True}
