"""A search index over published translations, and the names readers type for an article.

Revision ID: 0077_guide_search_and_aliases
Revises: 0076_guide_topic_hierarchy

``guide_search_entries`` holds one flattened row per published (article, locale), written
by the publish path and deleted by the withdraw path; ``guide_article_aliases`` holds the
other names an article answers to. Both are new, empty tables, guarded the way 0072 guards
its own: ``0001_initial`` builds current metadata on a fresh database, so there the tables
already exist and only the index below is left to do.

On PostgreSQL the match runs as ``LIKE '%term%'`` over ``search_text``, which is a
sequential scan without a trigram index. ``pg_trgm`` is a trusted extension, so the
database owner may create it without superuser rights; the GIN index is created outside
the has-table guard because a fresh database needs it just the same. Neither exists on
SQLite, where the test leg accepts the scan.

This migration builds no rows. After deploying it, run ``python -m app.cli
guides-search-reindex`` once, or every search answers with nothing until each article is
republished.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0077_guide_search_and_aliases"
down_revision: str | None = "0076_guide_topic_hierarchy"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LOCALE_CHECK = "locale IN ('en', 'ja', 'ko', 'zh-TW', 'zh-CN')"
TRIGRAM_INDEX = "ix_guide_search_entries_search_text_trgm"


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    if inspector is None or not inspector.has_table("guide_search_entries"):
        op.create_table(
            "guide_search_entries",
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column(
                "article_id",
                sa.Uuid(),
                sa.ForeignKey("guide_articles.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("locale", sa.String(16), nullable=False),
            sa.Column("revision_version", sa.Integer(), nullable=False),
            sa.Column("title", sa.String(200), nullable=False),
            sa.Column("description", sa.String(500), nullable=False),
            sa.Column("title_norm", sa.String(200), nullable=False),
            sa.Column("description_norm", sa.String(500), nullable=False),
            sa.Column("headings_norm", sa.Text(), nullable=False),
            sa.Column("aliases_norm", sa.Text(), nullable=False),
            sa.Column("body_text", sa.Text(), nullable=False),
            sa.Column("search_text", sa.Text(), nullable=False),
            sa.Column("hero_json", sa.JSON(none_as_null=True), nullable=True),
            sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("indexed_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("article_id", "locale", name="uq_guide_search_entry_locale"),
            sa.CheckConstraint(LOCALE_CHECK, name="ck_guide_search_entry_locale"),
        )
        op.create_index(
            "ix_guide_search_entries_article_id", "guide_search_entries", ["article_id"]
        )
        op.create_index("ix_guide_search_entries_locale", "guide_search_entries", ["locale"])

    if inspector is None or not inspector.has_table("guide_article_aliases"):
        op.create_table(
            "guide_article_aliases",
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column(
                "article_id",
                sa.Uuid(),
                sa.ForeignKey("guide_articles.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("locale", sa.String(16), nullable=False),
            sa.Column("alias", sa.String(120), nullable=False),
            sa.Column("alias_norm", sa.String(120), nullable=False),
            sa.Column("source", sa.String(16), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint(
                "article_id", "locale", "alias_norm", name="uq_guide_article_alias"
            ),
            sa.CheckConstraint(LOCALE_CHECK, name="ck_guide_article_alias_locale"),
            sa.CheckConstraint(
                "source IN ('term', 'keyword', 'series', 'editor')",
                name="ck_guide_article_alias_source",
            ),
        )
        op.create_index(
            "ix_guide_article_aliases_article_id", "guide_article_aliases", ["article_id"]
        )
        op.create_index(
            "ix_guide_article_aliases_lookup", "guide_article_aliases", ["locale", "alias_norm"]
        )

    # Outside the guard on purpose: a fresh database has the table from 0001 and still
    # needs the index. ``IF NOT EXISTS`` makes a re-run harmless.
    if not context.is_offline_mode() and op.get_bind().dialect.name == "postgresql":
        op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        op.execute(
            f"CREATE INDEX IF NOT EXISTS {TRIGRAM_INDEX} ON guide_search_entries "
            "USING gin (search_text gin_trgm_ops)"
        )


def downgrade() -> None:
    if context.is_offline_mode():
        op.execute(f"DROP INDEX IF EXISTS {TRIGRAM_INDEX}")
        op.drop_table("guide_article_aliases")
        op.drop_table("guide_search_entries")
        return
    bind = op.get_bind()
    tables = set(sa.inspect(bind).get_table_names())
    if bind.dialect.name == "postgresql":
        # The extension stays: another table may have come to rely on it, and creating it
        # again is free.
        op.execute(f"DROP INDEX IF EXISTS {TRIGRAM_INDEX}")
    if "guide_article_aliases" in tables:
        op.drop_table("guide_article_aliases")
    if "guide_search_entries" in tables:
        op.drop_table("guide_search_entries")
