"""Upgrade an existing shape and a fresh-metadata shape without seeding public content."""

from __future__ import annotations

import importlib.util
import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from app.config import get_settings
from app.db import Base
from app.models import SitePage, SitePageRevision, User


def migration():
    path = Path(__file__).parents[1] / "migrations/versions/0069_site_pages.py"
    spec = importlib.util.spec_from_file_location("site_pages_migration", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def plant_history(connection):
    user_id, page_id, revision_id = uuid4(), uuid4(), uuid4()
    now = datetime.now(UTC)
    connection.execute(
        User.__table__.insert().values(
            id=user_id,
            email=f"migration-{user_id}@example.com",
            is_active=True,
            is_admin=False,
        )
    )
    connection.execute(
        SitePage.__table__.insert().values(
            id=page_id,
            slug="privacy",
            locale="en",
            version=1,
            draft_json={"preserve": "existing operator draft"},
            published_version=None,
            created_at=now,
            updated_at=now,
        )
    )
    connection.execute(
        SitePageRevision.__table__.insert().values(
            id=revision_id,
            page_id=page_id,
            version=1,
            action="initialized",
            document_json={"preserve": "complete historical content"},
            created_by_user_id=user_id,
            created_at=now,
        )
    )
    return revision_id


@pytest.mark.parametrize("fresh_metadata", [False, True])
def test_upgrade_existing_or_fresh_is_idempotent_and_does_not_seed(monkeypatch, fresh_metadata):
    module = migration()
    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    engine = sa.create_engine("sqlite://")
    with engine.begin() as connection:
        tables = [User.__table__]
        if fresh_metadata:
            tables += [SitePage.__table__, SitePageRevision.__table__]
        Base.metadata.create_all(connection, tables=tables)
        with Operations.context(MigrationContext.configure(connection)):
            module.upgrade()
            assert connection.scalar(sa.select(sa.func.count()).select_from(SitePage)) == 0
            revision_id = plant_history(connection)
            module.upgrade()
            assert connection.scalar(sa.select(sa.func.count()).select_from(SitePage)) == 1
            assert connection.scalar(sa.select(SitePage.draft_json)) == {
                "preserve": "existing operator draft"
            }
            assert connection.scalar(sa.select(SitePage.published_version)) is None
            with pytest.raises(sa.exc.IntegrityError, match="append-only"):
                connection.execute(
                    sa.update(SitePageRevision)
                    .where(SitePageRevision.id == revision_id)
                    .values(document_json={"forged": True})
                )
            with pytest.raises(sa.exc.IntegrityError, match="append-only"):
                connection.execute(sa.delete(SitePageRevision))
            # The single irreversible FK-identity scrubbing transition is allowed.
            connection.execute(
                sa.update(SitePageRevision)
                .where(SitePageRevision.id == revision_id)
                .values(created_by_user_id=None)
            )
            with pytest.raises(sa.exc.IntegrityError, match="append-only"):
                connection.execute(
                    sa.update(SitePageRevision)
                    .where(SitePageRevision.id == revision_id)
                    .values(action="published")
                )
            module.downgrade()
            assert "site_pages" not in sa.inspect(connection).get_table_names()
            assert "site_page_revisions" not in sa.inspect(connection).get_table_names()
    engine.dispose()


def test_models_have_uniqueness_bounds_and_locale_slug_checks():
    constraints = {constraint.name for constraint in SitePage.__table__.constraints}
    assert {
        "uq_site_page_slug_locale",
        "ck_site_page_slug",
        "ck_site_page_locale",
        "ck_site_page_version",
        "ck_site_page_published_version",
    } <= constraints
    assert "uq_site_page_revision_version" in {
        constraint.name for constraint in SitePageRevision.__table__.constraints
    }


@pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires isolated PostgreSQL services"
)
async def test_postgresql_migration_guard_is_append_only_and_preserves_existing_rows(monkeypatch):
    """Roll back all DDL and rows; never change the shared test schema after this test."""
    url = get_settings().database_url
    assert make_url(url).host in {"localhost", "127.0.0.1", "::1", "postgres", "db"}
    engine = create_async_engine(url, poolclass=NullPool)
    module = migration()
    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    async with engine.connect() as connection:
        transaction = await connection.begin()
        try:
            # The dedicated schema lets both missing-table branches run. The
            # function is transactional and identical to the actual migration.
            schema = f"site_pages_migration_{uuid4().hex}"
            await connection.execute(sa.text(f'CREATE SCHEMA "{schema}"'))
            # Do not include public: has_table must not discover the shared
            # application's existing table and skip our missing-table branch.
            await connection.execute(sa.text(f'SET LOCAL search_path TO "{schema}"'))

            def run(sync):
                # No unrelated production-shaped tables or credentials are read.
                User.__table__.create(sync, checkfirst=False)
                with Operations.context(MigrationContext.configure(sync)):
                    module.upgrade()
                    revision_id = plant_history(sync)
                    module.upgrade()
                assert sync.scalar(sa.select(sa.func.count()).select_from(SitePage)) == 1
                assert sync.scalar(sa.select(SitePage.published_version)) is None
                for statement in (
                    sa.update(SitePageRevision).values(document_json={"forged": True}),
                    sa.delete(SitePageRevision),
                ):
                    with sync.begin_nested() as nested:
                        with pytest.raises(sa.exc.DBAPIError, match="append-only"):
                            sync.execute(statement)
                        nested.rollback()
                sync.execute(
                    sa.update(SitePageRevision)
                    .where(SitePageRevision.id == revision_id)
                    .values(created_by_user_id=None)
                )
                assert sync.scalar(sa.select(SitePageRevision.document_json)) == {
                    "preserve": "complete historical content"
                }

            await connection.run_sync(run)
        finally:
            await transaction.rollback()
    await engine.dispose()
