"""The day a news article's news happened, so a news list is ordered by it.

Revision ID: 0079_guide_news_date
Revises: 0078_guide_article_links

One nullable date column and its index on ``guide_articles``, guarded the way 0076 guards
its columns: ``0001_initial`` builds current metadata on a fresh database, so there the
column already exists. This migration writes no dates. The news packs carry ``news_date``
and ``python -m app.cli guides-import --slug ... --publish`` writes it, as it writes every
other taxonomy field; until then every row is NULL and ``sort=news`` falls back to
publication time within the undated rows.

Another branch (``claude/brave-hopper-8ezxba``, 2026-09-16) also revises 0078 with
``0079_crypto_and_tech_topics``. Whichever of the two merges second must point its
``down_revision`` at the other and take the next number, or ``alembic upgrade head`` finds
two heads.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0079_guide_news_date"
down_revision: str | None = "0078_guide_article_links"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

INDEX = "ix_guide_articles_news_date"


def upgrade() -> None:
    if not context.is_offline_mode():
        inspector = sa.inspect(op.get_bind())
        columns = {column["name"] for column in inspector.get_columns("guide_articles")}
        if "news_date" in columns:
            return
    with op.batch_alter_table("guide_articles") as batch:
        batch.add_column(sa.Column("news_date", sa.Date(), nullable=True))
        batch.create_index(INDEX, ["news_date"])


def downgrade() -> None:
    if not context.is_offline_mode():
        inspector = sa.inspect(op.get_bind())
        columns = {column["name"] for column in inspector.get_columns("guide_articles")}
        if "news_date" not in columns:
            return
    with op.batch_alter_table("guide_articles") as batch:
        batch.drop_index(INDEX)
        batch.drop_column("news_date")
