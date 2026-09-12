"""Upgrade a fresh or an existing shape without publishing anything, and prove the
revision history is append-only where it is actually enforced: in the database.

``tests/test_guides.py`` builds its tables with ``Base.metadata.create_all`` and therefore
never sees the trigger. This file runs the real migration, which is the only place the
guard exists.
"""

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
from app.guides.models import (
    GuideArticle,
    GuideArticleLocale,
    GuideArticleRevision,
    GuideTopic,
)
from app.models import User

GUIDE_TABLES = (
    "guide_topics",
    "guide_articles",
    "guide_article_locales",
    "guide_article_revisions",
    "guide_article_topics",
)


def migration(name: str = "0072_travel_guides"):
    path = Path(__file__).parents[1] / f"migrations/versions/{name}.py"
    spec = importlib.util.spec_from_file_location(f"{name}_migration", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def plant_history(connection):
    """An article an editor already wrote and published, so a re-run must not touch it."""
    user_id, article_id, locale_id, revision_id = uuid4(), uuid4(), uuid4(), uuid4()
    now = datetime.now(UTC)
    connection.execute(
        User.__table__.insert().values(
            id=user_id,
            email=f"guides-migration-{user_id}@example.com",
            is_active=True,
            is_admin=False,
        )
    )
    connection.execute(
        GuideArticle.__table__.insert().values(
            id=article_id,
            slug="existing-article",
            kind="howto",
            destination_id="tokyo",
            valid_until=None,
            featured=False,
            display_order=100,
            is_active=True,
            version=2,
            created_at=now,
            updated_at=now,
        )
    )
    connection.execute(
        GuideArticleLocale.__table__.insert().values(
            id=locale_id,
            article_id=article_id,
            locale="zh-TW",
            version=2,
            draft_json={"preserve": "existing editor draft"},
            published_version=2,
            published_at=now,
            created_at=now,
            updated_at=now,
        )
    )
    connection.execute(
        GuideArticleRevision.__table__.insert().values(
            id=revision_id,
            article_locale_id=locale_id,
            version=2,
            action="published",
            document_json={"preserve": "complete historical content"},
            created_by_user_id=user_id,
            created_at=now,
        )
    )
    return revision_id


@pytest.mark.parametrize("fresh_metadata", [False, True])
def test_upgrade_seeds_topics_only_and_never_touches_existing_content(monkeypatch, fresh_metadata):
    module = migration()
    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    engine = sa.create_engine("sqlite://")
    with engine.begin() as connection:
        tables = [User.__table__]
        if fresh_metadata:
            tables += [
                GuideTopic.__table__,
                GuideArticle.__table__,
                GuideArticleLocale.__table__,
                GuideArticleRevision.__table__,
            ]
        Base.metadata.create_all(connection, tables=tables)
        with Operations.context(MigrationContext.configure(connection)):
            module.upgrade()
            # A migration seeds the subject vocabulary. It never writes an article, and it
            # certainly never publishes one.
            assert connection.scalar(sa.select(sa.func.count()).select_from(GuideArticle)) == 0
            # Seeded on both paths. On a fresh database 0001 has already created the table
            # from current metadata, so a seed tied to the create branch would never run
            # and the deployment would come up with no topics at all.
            topics = connection.scalar(sa.select(sa.func.count()).select_from(GuideTopic))
            assert topics == len(module.SEED_TOPICS)

            revision_id = plant_history(connection)
            module.upgrade()
            assert connection.scalar(sa.select(sa.func.count()).select_from(GuideArticle)) == 1
            assert connection.scalar(sa.select(GuideArticleLocale.draft_json)) == {
                "preserve": "existing editor draft"
            }
            assert connection.scalar(sa.select(GuideArticleLocale.published_version)) == 2
            # Re-running inserts nothing: only absent slugs are added, so no duplicates.
            assert connection.scalar(sa.select(sa.func.count()).select_from(GuideTopic)) == topics

            with pytest.raises(sa.exc.IntegrityError, match="append-only"):
                connection.execute(
                    sa.update(GuideArticleRevision)
                    .where(GuideArticleRevision.id == revision_id)
                    .values(document_json={"forged": True})
                )
            with pytest.raises(sa.exc.IntegrityError, match="append-only"):
                connection.execute(sa.delete(GuideArticleRevision))
            # Detaching a deleted account from its revisions is the one allowed transition.
            connection.execute(
                sa.update(GuideArticleRevision)
                .where(GuideArticleRevision.id == revision_id)
                .values(created_by_user_id=None)
            )
            with pytest.raises(sa.exc.IntegrityError, match="append-only"):
                connection.execute(
                    sa.update(GuideArticleRevision)
                    .where(GuideArticleRevision.id == revision_id)
                    .values(action="draft_saved")
                )
            assert connection.scalar(sa.select(GuideArticleRevision.document_json)) == {
                "preserve": "complete historical content"
            }

            # A topic an administrator renamed or turned off survives a re-run untouched.
            connection.execute(
                sa.update(GuideTopic)
                .where(GuideTopic.slug == "transport")
                .values(is_active=False, names_json={"zh-TW": "自訂名稱"})
            )
            module.upgrade()
            kept = connection.execute(
                sa.select(GuideTopic.is_active, GuideTopic.names_json).where(
                    GuideTopic.slug == "transport"
                )
            ).one()
            assert kept.is_active is False
            assert kept.names_json == {"zh-TW": "自訂名稱"}
            assert connection.scalar(sa.select(sa.func.count()).select_from(GuideTopic)) == topics

            module.downgrade()
            names = sa.inspect(connection).get_table_names()
            assert all(table not in names for table in GUIDE_TABLES)
    engine.dispose()


def test_the_models_carry_the_constraints_the_service_relies_on():
    article = {constraint.name for constraint in GuideArticle.__table__.constraints}
    assert {"uq_guide_article_slug", "ck_guide_article_kind", "ck_guide_article_version"} <= article
    row = {constraint.name for constraint in GuideArticleLocale.__table__.constraints}
    assert {
        "uq_guide_article_locale",
        "ck_guide_article_locale_locale",
        "ck_guide_article_locale_version",
        "ck_guide_article_locale_published_version",
    } <= row
    revision = {constraint.name for constraint in GuideArticleRevision.__table__.constraints}
    assert {
        "uq_guide_article_revision_version",
        "ck_guide_article_revision_action",
    } <= revision


def test_the_seeded_topics_match_the_python_vocabulary():
    """The migration and app.guides.taxonomy each carry the seed list. They must agree, or
    a fresh database and an upgraded one disagree about what a topic is called."""
    from app.guides.taxonomy import SEED_TOPICS

    module = migration()
    assert [(slug, labels) for slug, _, labels in module.SEED_TOPICS] == list(SEED_TOPICS)


def test_the_seeded_life_topics_match_the_python_vocabulary():
    """Same contract for the lifestyle vocabulary, which 0073 seeds."""
    from app.guides.taxonomy import LIFE_SEED_TOPICS

    module = migration("0074_lifestyle_guides")
    assert [
        (slug, labels) for slug, _, labels in module.LIFE_SEED_TOPICS
    ] == list(LIFE_SEED_TOPICS)


LIFE_SLUGS = ("ai", "tutorial", "software", "gadgets", "productivity", "daily", "misc")


def sections(connection) -> dict[str, str]:
    return {
        row.slug: row.section
        for row in connection.execute(sa.select(GuideTopic.slug, GuideTopic.section))
    }


def insert_article(connection, *, slug: str, kind: str):
    now = datetime.now(UTC)
    connection.execute(
        GuideArticle.__table__.insert().values(
            id=uuid4(), slug=slug, kind=kind, destination_id=None, valid_until=None,
            featured=False, display_order=100, is_active=True, version=1,
            created_at=now, updated_at=now,
        )
    )


@pytest.mark.parametrize("fresh_metadata", [False, True])
def test_0073_adds_the_life_kind_and_section_without_touching_travel_rows(
    monkeypatch, fresh_metadata
):
    """0073 on both shapes a deployment can be in: a database 0072 upgraded, and a fresh one
    where 0001 already built the tables from the current models.

    The engine deliberately leaves ``PRAGMA foreign_keys`` off, as the 0072 test does: a
    SQLite batch rebuild drops and recreates the table, and with enforcement on the implicit
    DELETE would cascade through guide_article_locales and guide_article_topics.
    """
    travel = migration()
    life = migration("0074_lifestyle_guides")
    for module in (travel, life):
        monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    engine = sa.create_engine("sqlite://")
    with engine.begin() as connection:
        tables = [User.__table__]
        if fresh_metadata:
            tables += [
                GuideTopic.__table__,
                GuideArticle.__table__,
                GuideArticleLocale.__table__,
                GuideArticleRevision.__table__,
            ]
        Base.metadata.create_all(connection, tables=tables)
        with Operations.context(MigrationContext.configure(connection)):
            travel.upgrade()
            if not fresh_metadata:
                # Before 0073 the two-value CHECK is what an upgrading database carries, so
                # the widening below is doing real work rather than passing vacuously.
                with connection.begin_nested() as nested:
                    with pytest.raises(sa.exc.IntegrityError):
                        insert_article(connection, slug="too-early", kind="life")
                    nested.rollback()

            life.upgrade()

            # Still a vocabulary migration: it seeds topics and writes no article.
            assert connection.scalar(sa.select(sa.func.count()).select_from(GuideArticle)) == 0
            total = len(travel.SEED_TOPICS) + len(life.LIFE_SEED_TOPICS)
            assert connection.scalar(sa.select(sa.func.count()).select_from(GuideTopic)) == total
            by_slug = sections(connection)
            assert {slug for slug, value in by_slug.items() if value == "life"} == set(LIFE_SLUGS)
            for slug, _, _labels in travel.SEED_TOPICS:
                assert by_slug[slug] == "travel", slug

            # The widened CHECK accepts the new kind and still refuses anything else.
            insert_article(connection, slug="ai-notes", kind="life")
            for bad in ("recipes", "lifestyle", ""):
                with connection.begin_nested() as nested:
                    with pytest.raises(sa.exc.IntegrityError):
                        insert_article(connection, slug=f"bad-{bad or 'empty'}", kind=bad)
                    nested.rollback()
            with connection.begin_nested() as nested:
                with pytest.raises(sa.exc.IntegrityError):
                    connection.execute(
                        GuideTopic.__table__.insert().values(
                            id=uuid4(), slug="hobby", names_json={}, display_order=1,
                            is_active=True, section="hobby", source="admin",
                            created_at=datetime.now(UTC), updated_at=datetime.now(UTC),
                        )
                    )
                nested.rollback()

            # The batch rebuild must not have cost the table its identity or its indexes.
            reported = sa.inspect(connection).get_indexes("guide_articles")
            indexes = {index["name"] for index in reported}
            assert {
                "ix_guide_articles_slug",
                "ix_guide_articles_destination_id",
                "ix_guide_articles_is_active",
                "ix_guide_articles_kind_active",
            } <= indexes
            with connection.begin_nested() as nested:
                with pytest.raises(sa.exc.IntegrityError):
                    insert_article(connection, slug="ai-notes", kind="life")
                nested.rollback()

            # Re-running changes nothing: only absent slugs are inserted, and both guards
            # read the shape they just wrote.
            life.upgrade()
            assert connection.scalar(sa.select(sa.func.count()).select_from(GuideTopic)) == total
            assert connection.scalar(sa.select(sa.func.count()).select_from(GuideArticle)) == 1

            # A lifestyle topic an administrator renamed or turned off survives a re-run.
            connection.execute(
                sa.update(GuideTopic).where(GuideTopic.slug == "ai").values(
                    is_active=False, names_json={"zh-TW": "自訂"}
                )
            )
            life.upgrade()
            kept = connection.execute(
                sa.select(GuideTopic.is_active, GuideTopic.names_json, GuideTopic.section)
                .where(GuideTopic.slug == "ai")
            ).one()
            assert kept.is_active is False
            assert kept.names_json == {"zh-TW": "自訂"}
            assert kept.section == "life"

            # A rollback with a published lifestyle article keeps the wider CHECK rather
            # than destroying the row; the column and the seeded topics still go.
            life.downgrade()
            assert connection.scalar(sa.select(sa.func.count()).select_from(GuideArticle)) == 1
            assert "section" not in {
                column["name"] for column in sa.inspect(connection).get_columns("guide_topics")
            }
            assert connection.scalar(
                sa.select(sa.func.count()).select_from(GuideTopic)
            ) == len(travel.SEED_TOPICS)

            # With the lifestyle articles gone the CHECK narrows back, so the API that
            # returns is the one that never knew the kind.
            connection.execute(sa.delete(GuideArticle))
            life.upgrade()
            life.downgrade()
            with connection.begin_nested() as nested:
                with pytest.raises(sa.exc.IntegrityError):
                    insert_article(connection, slug="after-rollback", kind="life")
                nested.rollback()
    engine.dispose()


@pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires isolated PostgreSQL services"
)
async def test_postgresql_append_only_guard_and_preserved_rows(monkeypatch):
    """Roll back all DDL and rows; never change the shared test schema after this test."""
    url = get_settings().database_url
    assert make_url(url).host in {"localhost", "127.0.0.1", "::1", "postgres", "db"}
    engine = create_async_engine(url, poolclass=NullPool)
    module = migration()
    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    async with engine.connect() as connection:
        transaction = await connection.begin()
        try:
            schema = f"guides_migration_{uuid4().hex}"
            await connection.execute(sa.text(f'CREATE SCHEMA "{schema}"'))
            # Do not include public: has_table must not find the shared application's
            # tables and skip the missing-table branch this test exists to exercise.
            await connection.execute(sa.text(f'SET LOCAL search_path TO "{schema}"'))

            def run(sync):
                User.__table__.create(sync, checkfirst=False)
                with Operations.context(MigrationContext.configure(sync)):
                    module.upgrade()
                    revision_id = plant_history(sync)
                    module.upgrade()
                assert sync.scalar(sa.select(sa.func.count()).select_from(GuideArticle)) == 1
                assert sync.scalar(sa.select(GuideArticleLocale.published_version)) == 2
                for statement in (
                    sa.update(GuideArticleRevision).values(document_json={"forged": True}),
                    sa.delete(GuideArticleRevision),
                ):
                    with sync.begin_nested() as nested:
                        with pytest.raises(sa.exc.DBAPIError, match="append-only"):
                            sync.execute(statement)
                        nested.rollback()
                sync.execute(
                    sa.update(GuideArticleRevision)
                    .where(GuideArticleRevision.id == revision_id)
                    .values(created_by_user_id=None)
                )
                assert sync.scalar(sa.select(GuideArticleRevision.document_json)) == {
                    "preserve": "complete historical content"
                }

            await connection.run_sync(run)
        finally:
            await transaction.rollback()
    await engine.dispose()
