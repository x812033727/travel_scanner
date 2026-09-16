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
    "guide_search_entries",
    "guide_article_aliases",
    "guide_article_links",
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


#: Every migration that seeds a lifestyle topic, oldest first. The application tuple is
#: appended to, never reordered, so concatenating these in revision order has to reproduce
#: it exactly -- a slug inserted mid-tuple would still pass a set comparison while a fresh
#: database and an upgraded one disagreed about its display_order.
LIFE_SEED_MIGRATIONS = (
    "0074_lifestyle_guides",
    "0075_finance_topic",
    "0076_guide_topic_hierarchy",
    "0080_crypto_and_tech_topics",
)
#: The subset that seeds sub-topics and hub leads. 0074 and 0075 predate both, so they carry
#: no ``LIFE_SEED_SUBTOPICS`` at all.
LIFE_SUBTOPIC_MIGRATIONS = ("0076_guide_topic_hierarchy", "0080_crypto_and_tech_topics")


def seeded_life_topics(name: str) -> list[tuple[str, int, object]]:
    return list(getattr(migration(name), "LIFE_SEED_TOPICS", ()))


def seeded_life_subtopics(name: str) -> list[tuple[str, str, int, object]]:
    return list(getattr(migration(name), "LIFE_SEED_SUBTOPICS", ()))


def test_the_seeded_life_topics_match_the_python_vocabulary():
    """Same contract for the lifestyle vocabulary, which 0074 and 0075 seed between them."""
    from app.guides.taxonomy import LIFE_SEED_TOPICS

    seeded = [
        (slug, labels)
        for name in LIFE_SEED_MIGRATIONS
        for slug, _, labels in migration(name).LIFE_SEED_TOPICS
    ]
    assert seeded == list(LIFE_SEED_TOPICS)


def test_the_seeded_sub_topics_match_the_python_vocabulary():
    """The sub-topics and the hub leads, concatenated in revision order, must agree with the
    application constants for the reason the parent vocabulary must."""
    from app.guides.taxonomy import LIFE_SEED_SUBTOPICS, LIFE_SEED_TOPICS, LIFE_TOPIC_DESCRIPTIONS

    seeded = [
        (slug, parent, labels)
        for name in LIFE_SUBTOPIC_MIGRATIONS
        for slug, parent, _, labels in seeded_life_subtopics(name)
    ]
    assert seeded == list(LIFE_SEED_SUBTOPICS)

    # Each revision owns a disjoint slice of the leads, which is what makes the merge order
    # irrelevant; two revisions claiming one slug would let a rollback restore the other's.
    leads: dict[str, dict[str, str]] = {}
    for name in LIFE_SUBTOPIC_MIGRATIONS:
        described = migration(name).TOPIC_DESCRIPTIONS
        assert not set(described) & set(leads), name
        leads.update(described)
    assert leads == LIFE_TOPIC_DESCRIPTIONS

    parents = {slug for slug, _ in LIFE_SEED_TOPICS}
    assert {parent for _, parent, _ in seeded} <= parents
    assert set(leads) <= parents | {slug for slug, _, _ in LIFE_SEED_SUBTOPICS}


def test_the_seeded_life_display_orders_are_unique_and_each_revision_starts_above_the_last():
    """They order one filter row, and two topics on the same number sort by slug by accident.
    One display_order column sorts parents and children alike, so no two rows may share a
    number. The old assertion was that the concatenation ascends globally, which only held
    while every revision seeded parents before children. 0079 seeds a parent at 530 after
    0076's children reached 520, so the property to hold it to is the one that was always
    meant: each revision's own rows ascend, and begin above everything already seeded."""
    highest = 0
    seen: set[int] = set()
    for name in LIFE_SEED_MIGRATIONS:
        orders = [order for _, order, _ in seeded_life_topics(name)]
        orders += [order for _, _, order, _ in seeded_life_subtopics(name)]
        assert orders == sorted(orders), name
        assert not seen & set(orders), name
        assert min(orders) > highest, name
        seen |= set(orders)
        highest = max(orders)


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


def test_0075_seeds_finance_and_its_rollback_spares_the_other_life_topics(monkeypatch):
    """0075 adds one row and takes one row back.

    The rollback is the half worth a test. 0074 removes every ``section = 'life'`` seed,
    which is right for the revision that created the section; the same predicate here would
    make a one-step downgrade delete the seven topics 0074 owns -- and their article links --
    while the lifestyle section is still published. So this asserts what survives, not only
    what goes.

    ``PRAGMA foreign_keys`` stays off for the reason the 0074 test gives: SQLite's batch
    rebuild would cascade the implicit DELETE through the linking tables.
    """
    travel = migration()
    life = migration("0074_lifestyle_guides")
    finance = migration("0075_finance_topic")
    for module in (travel, life, finance):
        monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    engine = sa.create_engine("sqlite://")
    with engine.begin() as connection:
        Base.metadata.create_all(connection, tables=[User.__table__])
        with Operations.context(MigrationContext.configure(connection)):
            travel.upgrade()
            life.upgrade()
            before = connection.scalar(sa.select(sa.func.count()).select_from(GuideTopic))

            finance.upgrade()

            row = connection.execute(
                sa.select(
                    GuideTopic.section, GuideTopic.display_order, GuideTopic.names_json,
                    GuideTopic.is_active, GuideTopic.source,
                ).where(GuideTopic.slug == "finance")
            ).one()
            assert (row.section, row.display_order, row.is_active, row.source) == (
                "life", 270, True, "seed",
            )
            # All five labels, or the reader of a locale we did not write sees the slug.
            assert set(row.names_json) == set(finance.LOCALES)
            assert row.names_json["zh-TW"] == "理財與金錢"
            assert connection.scalar(
                sa.select(sa.func.count()).select_from(GuideTopic)
            ) == before + 1

            # Only absent slugs are inserted, so a re-run writes nothing...
            finance.upgrade()
            assert connection.scalar(
                sa.select(sa.func.count()).select_from(GuideTopic)
            ) == before + 1

            # ...and a label an administrator rewrote is not restored by one.
            connection.execute(
                sa.update(GuideTopic).where(GuideTopic.slug == "finance").values(
                    is_active=False, names_json={"zh-TW": "自訂"}
                )
            )
            finance.upgrade()
            kept = connection.execute(
                sa.select(GuideTopic.is_active, GuideTopic.names_json)
                .where(GuideTopic.slug == "finance")
            ).one()
            assert kept.is_active is False
            assert kept.names_json == {"zh-TW": "自訂"}

            finance.downgrade()

            remaining = sections(connection)
            assert "finance" not in remaining
            # The whole point: 0074's vocabulary is untouched by 0075's rollback.
            assert {slug for slug, value in remaining.items() if value == "life"} == set(LIFE_SLUGS)
            assert connection.scalar(
                sa.select(sa.func.count()).select_from(GuideTopic)
            ) == before


def test_0079_seeds_the_two_news_verticals_and_its_rollback_spares_the_earlier_vocabulary(
    monkeypatch,
):
    """0079 adds no schema, so it runs on whatever 0076 left. ``tech-news`` hangs under the
    parent this same revision seeds and ``crypto`` under ``finance``, which 0075 seeded three
    revisions earlier -- the case that would break if the parent lookup only saw its own rows.

    ``PRAGMA foreign_keys`` stays off for the reason the 0074 test gives.
    """
    names = (
        "0072_travel_guides",
        "0074_lifestyle_guides",
        "0075_finance_topic",
        "0076_guide_topic_hierarchy",
        "0080_crypto_and_tech_topics",
    )
    modules = [migration(name) for name in names]
    for module in modules:
        monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    *earlier, verticals = modules
    engine = sa.create_engine("sqlite://")
    with engine.begin() as connection:
        Base.metadata.create_all(
            connection,
            tables=[
                User.__table__,
                GuideTopic.__table__,
                GuideArticle.__table__,
                GuideArticleLocale.__table__,
                GuideArticleRevision.__table__,
            ],
        )
        with Operations.context(MigrationContext.configure(connection)):
            for module in earlier:
                module.upgrade()
            before = connection.scalar(sa.select(sa.func.count()).select_from(GuideTopic))

            verticals.upgrade()

            rows = {
                row.slug: row
                for row in connection.execute(
                    sa.select(
                        GuideTopic.slug,
                        GuideTopic.id,
                        GuideTopic.parent_id,
                        GuideTopic.section,
                        GuideTopic.display_order,
                        GuideTopic.descriptions_json,
                        GuideTopic.source,
                    )
                )
            }
            added = len(verticals.LIFE_SEED_TOPICS) + len(verticals.LIFE_SEED_SUBTOPICS)
            assert len(rows) == before + added
            for slug, parent, order, _ in verticals.LIFE_SEED_SUBTOPICS:
                assert rows[slug].parent_id == rows[parent].id, slug
                assert (rows[slug].section, rows[slug].display_order, rows[slug].source) == (
                    "life",
                    order,
                    "seed",
                )
            # The one this revision could get wrong: an older revision's parent.
            assert rows["crypto"].parent_id == rows["finance"].id
            assert rows["tech-news"].parent_id == rows["tech"].id
            assert rows["tech"].parent_id is None
            assert rows["crypto"].descriptions_json == verticals.TOPIC_DESCRIPTIONS["crypto"]

            # A re-run writes nothing, and a lead an editor rewrote is never restored.
            connection.execute(
                sa.update(GuideTopic)
                .where(GuideTopic.slug == "crypto")
                .values(descriptions_json={"zh-TW": "\u81ea\u8a02"})
            )
            verticals.upgrade()
            assert (
                connection.scalar(sa.select(sa.func.count()).select_from(GuideTopic))
                == before + added
            )
            assert connection.scalar(
                sa.select(GuideTopic.descriptions_json).where(GuideTopic.slug == "crypto")
            ) == {"zh-TW": "\u81ea\u8a02"}

            verticals.downgrade()

            remaining = sections(connection)
            assert set(remaining) & set(verticals.SLUGS) == set()
            # Everything the earlier revisions own is still here -- a rollback scoped by
            # ``section = 'life'`` would have taken the whole vocabulary with it.
            assert {"ai", "finance", "website", "marketing", "investing", "ai-news"} <= set(
                remaining
            )
            assert len(remaining) == before


@pytest.mark.parametrize("fresh_metadata", [False, True])
def test_0076_adds_the_hierarchy_and_its_rollback_spares_the_earlier_vocabulary(
    monkeypatch, fresh_metadata
):
    """0076 on both shapes: a database 0075 upgraded, and a fresh one where 0001 already
    built ``guide_topics`` with both columns. Either way the sub-topics land under their
    parents, a re-run writes nothing, an editor's lead is kept, and the rollback removes
    exactly this revision's rows and columns while 0074's and 0075's topics stay.

    ``PRAGMA foreign_keys`` stays off for the reason the 0074 test gives.
    """
    names = ("0072_travel_guides", "0074_lifestyle_guides", "0075_finance_topic")
    modules = [migration(name) for name in (*names, "0076_guide_topic_hierarchy")]
    for module in modules:
        monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    travel, life, finance, hierarchy = modules
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
            life.upgrade()
            finance.upgrade()
            before = connection.scalar(sa.select(sa.func.count()).select_from(GuideTopic))
            columns = {c["name"] for c in sa.inspect(connection).get_columns("guide_topics")}
            assert ("parent_id" in columns) is fresh_metadata

            hierarchy.upgrade()

            columns = {c["name"] for c in sa.inspect(connection).get_columns("guide_topics")}
            assert {"parent_id", "descriptions_json"} <= columns
            rows = {
                row.slug: row
                for row in connection.execute(
                    sa.select(
                        GuideTopic.slug,
                        GuideTopic.parent_id,
                        GuideTopic.id,
                        GuideTopic.section,
                        GuideTopic.display_order,
                        GuideTopic.descriptions_json,
                        GuideTopic.source,
                    )
                )
            }
            added = len(hierarchy.LIFE_SEED_TOPICS) + len(hierarchy.LIFE_SEED_SUBTOPICS)
            assert len(rows) == before + added
            for slug, parent, order, _ in hierarchy.LIFE_SEED_SUBTOPICS:
                assert rows[slug].parent_id == rows[parent].id, slug
                assert rows[parent].parent_id is None, parent
                assert (rows[slug].section, rows[slug].display_order, rows[slug].source) == (
                    "life",
                    order,
                    "seed",
                )
            for slug, order, _ in hierarchy.LIFE_SEED_TOPICS:
                assert rows[slug].parent_id is None and rows[slug].display_order == order
            # The lead reaches 0074's parents too, not only this revision's rows.
            assert rows["ai"].descriptions_json == hierarchy.TOPIC_DESCRIPTIONS["ai"]
            assert rows["ai-terms"].descriptions_json == hierarchy.TOPIC_DESCRIPTIONS["ai-terms"]
            assert rows["tutorial"].descriptions_json is None

            # A re-run writes nothing, and a lead an editor wrote is never restored.
            connection.execute(
                sa.update(GuideTopic)
                .where(GuideTopic.slug == "ai")
                .values(descriptions_json={"zh-TW": "自訂"})
            )
            hierarchy.upgrade()
            assert (
                connection.scalar(sa.select(sa.func.count()).select_from(GuideTopic))
                == before + added
            )
            kept = connection.scalar(
                sa.select(GuideTopic.descriptions_json).where(GuideTopic.slug == "ai")
            )
            assert kept == {"zh-TW": "自訂"}

            hierarchy.downgrade()

            remaining = sections(connection)
            assert set(remaining) & set(hierarchy.SLUGS) == set()
            assert {slug for slug, value in remaining.items() if value == "life"} == set(
                LIFE_SLUGS
            ) | {"finance"}
            assert connection.scalar(sa.select(sa.func.count()).select_from(GuideTopic)) == before
            columns = {c["name"] for c in sa.inspect(connection).get_columns("guide_topics")}
            assert not columns & {"parent_id", "descriptions_json"}
            # The rebuild kept the table's other indexes.
            names = {index["name"] for index in sa.inspect(connection).get_indexes("guide_topics")}
            assert "ix_guide_topics_active_order" in names


@pytest.mark.parametrize("fresh_metadata", [False, True])
def test_0077_creates_the_search_tables_once_and_its_rollback_drops_only_them(
    monkeypatch, fresh_metadata
):
    """0077 on both shapes: a database 0076 upgraded, and a fresh one where 0001 already
    built both tables from the models. Either way the tables exist afterwards with the
    constraints the service relies on, a re-run is a no-op, and the rollback drops
    exactly the two tables while the article tables stay.
    """
    from app.guides.models import GuideArticleAlias, GuideSearchEntry

    module = migration("0077_guide_search_and_aliases")
    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    engine = sa.create_engine("sqlite://")
    with engine.begin() as connection:
        tables = [
            User.__table__,
            GuideTopic.__table__,
            GuideArticle.__table__,
            GuideArticleLocale.__table__,
            GuideArticleRevision.__table__,
        ]
        if fresh_metadata:
            tables += [GuideSearchEntry.__table__, GuideArticleAlias.__table__]
        Base.metadata.create_all(connection, tables=tables)
        plant_history(connection)
        with Operations.context(MigrationContext.configure(connection)):
            module.upgrade()
            names = set(sa.inspect(connection).get_table_names())
            assert {"guide_search_entries", "guide_article_aliases"} <= names
            unique = {
                constraint["name"]
                for constraint in sa.inspect(connection).get_unique_constraints(
                    "guide_article_aliases"
                )
            }
            assert "uq_guide_article_alias" in unique
            indexes = {
                index["name"]
                for index in sa.inspect(connection).get_indexes("guide_article_aliases")
            }
            assert "ix_guide_article_aliases_lookup" in indexes
            # The migration builds no rows: the index is filled by publication and the
            # reindex command, never by a schema change.
            assert connection.scalar(sa.select(sa.func.count()).select_from(GuideSearchEntry)) == 0

            module.upgrade()  # a re-run finds the tables and does nothing

            module.downgrade()
            names = set(sa.inspect(connection).get_table_names())
            assert not names & {"guide_search_entries", "guide_article_aliases"}
            assert {"guide_articles", "guide_article_locales", "guide_article_revisions"} <= names
            assert connection.scalar(sa.select(sa.func.count()).select_from(GuideArticle)) == 1
    engine.dispose()


@pytest.mark.parametrize("fresh_metadata", [False, True])
def test_0078_creates_the_link_table_once_and_its_rollback_drops_only_it(
    monkeypatch, fresh_metadata
):
    """0078 on both shapes: a database 0077 upgraded, and a fresh one where 0001 already
    built the table from the model. The table exists afterwards with its constraints, a
    re-run is a no-op, and the rollback drops exactly it while the article tables stay."""
    from app.guides.models import GuideArticleLink

    module = migration("0078_guide_article_links")
    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    engine = sa.create_engine("sqlite://")
    with engine.begin() as connection:
        tables = [
            User.__table__,
            GuideTopic.__table__,
            GuideArticle.__table__,
            GuideArticleLocale.__table__,
            GuideArticleRevision.__table__,
        ]
        if fresh_metadata:
            tables += [GuideArticleLink.__table__]
        Base.metadata.create_all(connection, tables=tables)
        plant_history(connection)
        with Operations.context(MigrationContext.configure(connection)):
            module.upgrade()
            inspector = sa.inspect(connection)
            assert "guide_article_links" in inspector.get_table_names()
            unique = {c["name"] for c in inspector.get_unique_constraints("guide_article_links")}
            assert "uq_guide_article_link" in unique
            indexes = {i["name"] for i in inspector.get_indexes("guide_article_links")}
            assert "ix_guide_article_links_target" in indexes
            assert connection.scalar(sa.select(sa.func.count()).select_from(GuideArticleLink)) == 0

            module.upgrade()  # a re-run finds the table and does nothing

            module.downgrade()
            names = set(sa.inspect(connection).get_table_names())
            assert "guide_article_links" not in names
            assert {"guide_articles", "guide_article_locales", "guide_article_revisions"} <= names
            assert connection.scalar(sa.select(sa.func.count()).select_from(GuideArticle)) == 1
    engine.dispose()
