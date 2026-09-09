"""Fresh/0066 migration compatibility and bounded PostgreSQL concurrency checks."""

import asyncio
import importlib.util
import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.exc import IntegrityError
from test_community_foundation import Harness
from test_community_foundation import harness as community_harness
from test_saved_flow import guide

from app.community.models import Collection, CollectionItem
from app.config import get_settings
from app.models import RestaurantFavorite, RestaurantPlace, User
from app.saved import service as saved_service

harness = community_harness


def migration():
    path = Path(__file__).parents[1] / "migrations/versions/0067_collection_inbox.py"
    spec = importlib.util.spec_from_file_location("collection_inbox_migration", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_upgrade(connection, module, fresh):
    metadata = sa.MetaData()
    users = sa.Table("users", metadata, sa.Column("id", sa.Uuid(), primary_key=True))
    if fresh:
        metadata.create_all(connection)
        Collection.__table__.create(connection)
    else:
        # Frozen 0066 table shape, not current model metadata dressed up as an old DB.
        sa.Table(
            "community_collections",
            metadata,
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
            sa.Column("name", sa.String(80), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )
        metadata.create_all(connection)
    if fresh:
        CollectionItem.__table__.create(connection)
    else:
        legacy = sa.MetaData()
        sa.Table("community_collections", legacy, autoload_with=connection)
        sa.Table(
            "community_collection_items",
            legacy,
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column("collection_id", sa.Uuid(), sa.ForeignKey("community_collections.id")),
            sa.Column("kind", sa.String(20)),
            sa.Column("target", sa.String(160)),
            sa.Column("created_at", sa.DateTime(timezone=True)),
        )
        legacy.create_all(connection)
    user, original = uuid4(), uuid4()
    now = datetime.now(UTC)
    connection.execute(users.insert().values(id=user))
    connection.execute(
        sa.text(
            "INSERT INTO community_collections "
            "(id,user_id,name,created_at,updated_at) VALUES (:id,:user_id,:name,:created,:updated)"
        ).bindparams(
            sa.bindparam("id", type_=sa.Uuid()),
            sa.bindparam("user_id", type_=sa.Uuid()),
            sa.bindparam("created", type_=sa.DateTime(timezone=True)),
            sa.bindparam("updated", type_=sa.DateTime(timezone=True)),
        ),
        {"id": original, "user_id": user, "name": "My old list", "created": now, "updated": now},
    )
    with Operations.context(MigrationContext.configure(connection)):
        module.upgrade()
        module.upgrade()
    inspector = sa.inspect(connection)
    assert "system_role" in {
        column["name"] for column in inspector.get_columns("community_collections")
    }
    assert (
        next(
            column["type"].length
            for column in inspector.get_columns("community_collection_items")
            if column["name"] == "target"
        )
        == 255
    )
    assert "uq_collection_system_role" in {
        row["name"] for row in inspector.get_unique_constraints("community_collections")
    }
    assert (
        connection.scalar(sa.select(Collection.name).where(Collection.id == original))
        == "My old list"
    )
    assert (
        connection.scalar(sa.select(Collection.system_role).where(Collection.id == original))
        is None
    )
    connection.execute(
        Collection.__table__.insert().values(
            id=uuid4(), user_id=user, name="Another normal list", created_at=now, updated_at=now
        )
    )
    connection.execute(
        Collection.__table__.insert().values(
            id=uuid4(),
            user_id=user,
            name="Private inbox",
            system_role="inbox",
            created_at=now,
            updated_at=now,
        )
    )
    with pytest.raises(IntegrityError), connection.begin_nested():
        connection.execute(
            Collection.__table__.insert().values(
                id=uuid4(),
                user_id=user,
                name="Duplicate inbox",
                system_role="inbox",
                created_at=now,
                updated_at=now,
            )
        )


@pytest.mark.parametrize("fresh", [False, True])
def test_inbox_frozen_and_current_sqlite_upgrade(monkeypatch, fresh):
    module = migration()
    assert module.revision == "0067_collection_inbox"
    assert module.down_revision == "0066_discovery_community"
    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    engine = sa.create_engine("sqlite://")
    try:
        with engine.begin() as connection:
            verify_upgrade(connection, module, fresh)
    finally:
        engine.dispose()


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.parametrize("fresh", [False, True])
@pytest.mark.asyncio
async def test_inbox_frozen_and_current_postgresql_upgrade(monkeypatch, fresh):
    from sqlalchemy.ext.asyncio import create_async_engine

    module = migration()
    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    engine = create_async_engine(get_settings().database_url)
    try:
        async with engine.connect() as connection, connection.begin():
            schema = "saved_inbox_migration_" + uuid4().hex
            await connection.execute(sa.text(f'CREATE SCHEMA "{schema}"'))
            await connection.execute(sa.text(f'SET LOCAL search_path TO "{schema}"'))
            await connection.run_sync(lambda conn: verify_upgrade(conn, module, fresh))
            # Only this transaction's randomly named scratch schema is rolled back.
            await connection.rollback()
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_postgresql_concurrent_first_save_and_organize_have_single_inbox(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = harness
    async with h.factory() as session:
        if session.get_bind().dialect.name != "postgresql":
            pytest.skip("row-level concurrency requires PostgreSQL")
    monkeypatch.setattr(get_settings(), "discovery_enabled", True)
    identifier = await guide(h)
    first, second = await asyncio.wait_for(
        asyncio.gather(
            h.call("PUT", f"/saved-items/guide/{identifier}", expected=201),
            h.call("PUT", f"/saved-items/video/{identifier}", expected=201),
        ),
        timeout=20,
    )
    assert sorted([first.json()["created"], second.json()["created"]]) == [False, True]
    async with h.factory() as session:
        assert (
            await session.scalar(
                sa.select(sa.func.count())
                .select_from(Collection)
                .where(Collection.user_id == h.ids[0], Collection.system_role == "inbox")
            )
            == 1
        )
        assert await session.scalar(sa.select(sa.func.count()).select_from(CollectionItem)) == 1
    collection = (
        await h.call("POST", "/saved-items/collections", json={"name": "Weekend"})
    ).json()["id"]
    await asyncio.wait_for(
        asyncio.gather(
            h.call(
                "POST",
                f"/saved-items/collections/{collection}/items",
                json={"kind": "guide", "id": str(identifier)},
            ),
            h.call(
                "POST",
                f"/saved-items/collections/{collection}/items",
                json={"kind": "video", "id": identifier.hex.upper()},
            ),
        ),
        timeout=20,
    )
    assert len((await h.call("GET", f"/saved-items/collections/{collection}")).json()["items"]) == 1


@pytest.mark.asyncio
async def test_postgresql_saved_lock_allows_legacy_favorite_foreign_key_insert(
    harness: Harness,
) -> None:
    h = harness
    async with h.factory() as session:
        if session.get_bind().dialect.name != "postgresql":
            pytest.skip("foreign-key row-lock compatibility requires PostgreSQL")
        place = RestaurantPlace(
            google_place_id="LegacyFavoriteRace",
            generated_maps_url="https://www.google.com/maps/search/?api=1&query=fixture",
        )
        session.add(place)
        await session.commit()
        place_id = place.id
    async with h.factory() as current:
        user = await current.get(User, h.ids[0])
        await saved_service.lock_account(current, user)

        async def legacy_insert() -> None:
            async with h.factory() as legacy:
                legacy.add(RestaurantFavorite(user_id=h.ids[0], restaurant_place_id=place_id))
                await legacy.commit()

        # A FOR UPDATE account lock would block this FK insertion. NO KEY UPDATE
        # preserves writer serialization while allowing the existing endpoint.
        await asyncio.wait_for(legacy_insert(), timeout=20)
        assert not await saved_service.insert_unique_reference(
            current,
            RestaurantFavorite,
            {"user_id": user.id, "restaurant_place_id": place_id},
            ["user_id", "restaurant_place_id"],
        )
        await current.commit()
