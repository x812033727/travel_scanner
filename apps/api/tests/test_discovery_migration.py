"""Exercise the frozen 0064 schema and current-metadata fresh-install guards."""

import importlib.util
import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations

from app.db import Base
from app.discovery.models import DiscoveryDismissal, DiscoveryPreference


def migration():
    path = Path(__file__).parents[1] / "migrations/versions/0065_travel_discovery.py"
    spec = importlib.util.spec_from_file_location("discovery_migration", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_metadata_and_revision_contract():
    module = migration()
    assert module.revision == "0065_travel_discovery"
    assert module.down_revision == "0064_klook_affiliate_channels"
    for model in (DiscoveryPreference, DiscoveryDismissal):
        assert model.__table__.metadata is Base.metadata
        assert next(iter(model.__table__.c.user_id.foreign_keys)).ondelete == "CASCADE"
    assert [column.name for column in DiscoveryDismissal.__table__.primary_key] == [
        "user_id",
        "content_key",
    ]


@pytest.mark.parametrize("fresh", [False, True])
def test_sqlite_frozen_and_current_metadata_upgrade_idempotent(monkeypatch, fresh):
    module = migration()
    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    engine = sa.create_engine("sqlite://")
    with engine.begin() as connection:
        metadata = sa.MetaData()
        sa.Table("users", metadata, sa.Column("id", sa.Uuid(), primary_key=True))
        metadata.create_all(connection)
        if fresh:
            DiscoveryPreference.__table__.create(connection)
            DiscoveryDismissal.__table__.create(connection)
        with Operations.context(MigrationContext.configure(connection)):
            module.upgrade()
            module.upgrade()
            inspector = sa.inspect(connection)
            assert {"discovery_preferences", "discovery_dismissals"} <= set(
                inspector.get_table_names()
            )
            assert (
                inspector.get_foreign_keys("discovery_preferences")[0]["options"]["ondelete"]
                == "CASCADE"
            )
            module.downgrade()
            assert "discovery_preferences" not in sa.inspect(connection).get_table_names()
    engine.dispose()


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.parametrize("fresh", [False, True])
@pytest.mark.asyncio
async def test_postgresql_frozen_and_fresh_upgrade_cascade(monkeypatch, fresh):
    from sqlalchemy.ext.asyncio import create_async_engine

    from app.config import get_settings

    module = migration()
    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    engine = create_async_engine(get_settings().database_url)
    async with engine.connect() as connection, connection.begin():
        schema = "discovery_migration_" + uuid4().hex
        await connection.execute(sa.text(f'CREATE SCHEMA "{schema}"'))
        await connection.execute(sa.text(f'SET LOCAL search_path TO "{schema}"'))

        def verify(conn):
            metadata = sa.MetaData()
            users = sa.Table("users", metadata, sa.Column("id", sa.Uuid(), primary_key=True))
            metadata.create_all(conn)
            if fresh:
                DiscoveryPreference.__table__.create(conn)
                DiscoveryDismissal.__table__.create(conn)
            with Operations.context(MigrationContext.configure(conn)):
                module.upgrade()
                module.upgrade()
                user = uuid4()
                conn.execute(users.insert().values(id=user))
                conn.execute(
                    DiscoveryPreference.__table__.insert().values(
                        user_id=user, destinations=[], topics=[], updated_at=datetime.now(UTC)
                    )
                )
                conn.execute(
                    DiscoveryDismissal.__table__.insert().values(
                        user_id=user, content_key=f"guide:{uuid4()}", created_at=datetime.now(UTC)
                    )
                )
                conn.execute(users.delete().where(users.c.id == user))
                assert (
                    conn.scalar(
                        sa.select(sa.func.count()).select_from(DiscoveryPreference.__table__)
                    )
                    == 0
                )
                assert (
                    conn.scalar(
                        sa.select(sa.func.count()).select_from(DiscoveryDismissal.__table__)
                    )
                    == 0
                )
                module.downgrade()

        await connection.run_sync(verify)
        await connection.rollback()
    await engine.dispose()
