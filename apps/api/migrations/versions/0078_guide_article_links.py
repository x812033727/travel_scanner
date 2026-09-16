"""The link graph between articles: in-text links materialised at publish, curated picks.

Revision ID: 0078_guide_article_links
Revises: 0077_guide_search_and_aliases

One new, empty table, guarded the way 0077 guards its own: ``0001_initial`` builds current
metadata on a fresh database, so there it already exists. ``inline`` rows are written by
the publish path from a translation's ``article`` inlines and deleted by the withdraw
path; ``related`` rows are the editor's further-reading picks on the identity (NULL
locale). This migration builds no rows: after deploying it, run
``python -m app.cli guides-links-rebuild`` once, or every "cited by" list is empty until
each article is republished (the other tiers of further reading do not depend on it).
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0078_guide_article_links"
down_revision: str | None = "0077_guide_search_and_aliases"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LOCALE_CHECK = "locale IN ('en', 'ja', 'ko', 'zh-TW', 'zh-CN')"


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    if inspector is not None and inspector.has_table("guide_article_links"):
        return
    op.create_table(
        "guide_article_links",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "source_article_id",
            sa.Uuid(),
            sa.ForeignKey("guide_articles.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "target_article_id",
            sa.Uuid(),
            sa.ForeignKey("guide_articles.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("locale", sa.String(16), nullable=True),
        sa.Column("relation", sa.String(16), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "source_article_id", "locale", "relation", "target_article_id",
            name="uq_guide_article_link",
        ),
        sa.CheckConstraint(
            "relation IN ('inline', 'related')", name="ck_guide_article_link_relation"
        ),
        sa.CheckConstraint(
            f"locale IS NULL OR {LOCALE_CHECK}", name="ck_guide_article_link_locale"
        ),
    )
    op.create_index(
        "ix_guide_article_links_source_article_id", "guide_article_links", ["source_article_id"]
    )
    op.create_index(
        "ix_guide_article_links_target", "guide_article_links", ["target_article_id", "locale"]
    )


def downgrade() -> None:
    if context.is_offline_mode():
        op.drop_table("guide_article_links")
        return
    if "guide_article_links" in sa.inspect(op.get_bind()).get_table_names():
        op.drop_table("guide_article_links")
