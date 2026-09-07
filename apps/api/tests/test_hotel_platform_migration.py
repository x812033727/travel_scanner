"""Frozen legacy schema migration: real PostgreSQL, isolated transactional schema."""

import importlib.util
import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations

from app.db import engine


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.asyncio
async def test_legacy_hotels_keep_ids_and_trip_links_and_upgrade_is_idempotent():
    path = Path(__file__).parents[1] / "migrations/versions/0057_hotel_booking_options.py"
    spec = importlib.util.spec_from_file_location("hotel_option_migration", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    await engine.dispose(close=False)
    async with engine.connect() as conn, conn.begin():
        schema = "hotel_migration_" + uuid4().hex
        await conn.execute(sa.text(f'CREATE SCHEMA "{schema}"'))
        await conn.execute(sa.text(f'SET LOCAL search_path TO "{schema}"'))

        def verify(connection):
            metadata = sa.MetaData()
            products = sa.Table(
                "travel_service_products",
                metadata,
                sa.Column("id", sa.Uuid, primary_key=True),
                sa.Column("kind", sa.String),
                sa.Column("facts", sa.JSON),
                sa.Column("status", sa.String),
                sa.Column("verified_at", sa.DateTime(timezone=True)),
                sa.Column("created_at", sa.DateTime(timezone=True)),
                sa.Column("updated_at", sa.DateTime(timezone=True)),
            )
            selections = sa.Table(
                "legacy_trip_selections",
                metadata,
                sa.Column("id", sa.Uuid, primary_key=True),
                sa.Column("product_id", sa.Uuid, sa.ForeignKey(products.c.id)),
            )
            metadata.create_all(connection)
            ids = [uuid4() for _ in range(6)]
            now = datetime.now(UTC)
            for i, identifier in enumerate(ids):
                connection.execute(
                    products.insert().values(
                        id=identifier,
                        kind="hotel",
                        facts={
                            "latitude": 35.69,
                            "hotel_links": [
                                {
                                    "provider": "official",
                                    "url": f"https://hotel{i}.example.com/",
                                    "evidence_url": f"https://hotel{i}.example.com/access",
                                }
                            ],
                        },
                        status="approved" if i == 0 else "pending",
                        verified_at=now if i == 0 else None,
                        created_at=now,
                        updated_at=now,
                    )
                )
                connection.execute(selections.insert().values(id=uuid4(), product_id=identifier))
            with Operations.context(MigrationContext.configure(connection)):
                module.upgrade()
                module.upgrade()
                options = sa.Table("hotel_booking_options", sa.MetaData(), autoload_with=connection)
                rows = list(connection.execute(sa.select(options)).mappings())
                assert len(rows) == 6 and {r["product_id"] for r in rows} == set(ids)
                assert sum(r["status"] == "approved" for r in rows) == 1
                assert all(
                    "hotel_links" not in f for f in connection.scalars(sa.select(products.c.facts))
                )
                assert set(connection.scalars(sa.select(selections.c.product_id))) == set(ids)
                module.downgrade()
                assert all(
                    f["hotel_links"] for f in connection.scalars(sa.select(products.c.facts))
                )
                assert set(connection.scalars(sa.select(products.c.status))) == {"pending"}
                assert set(connection.scalars(sa.select(selections.c.product_id))) == set(ids)

        await conn.run_sync(verify)
        # Roll back the entire temporary schema, including DDL; nothing touches public.
        await conn.rollback()
    await engine.dispose()
