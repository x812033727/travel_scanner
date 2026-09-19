"""Which guide article placed the button a click came from.

Revision ID: 0081_affiliate_click_article
Revises: 0080_crypto_and_tech_topics

One nullable column and its index on ``affiliate_clicks``, guarded the way 0079 guards
its own: ``0001_initial`` builds current metadata on a fresh database, so there the column
already exists. Additive only. The append-only trigger 0006 put on this table (and 0068
rewrote) fires on UPDATE and DELETE; an ADD COLUMN is neither, so the trigger is left as it
is and no existing row is rewritten.

Nothing is backfilled. Offer clicks written before this revision have no article left to
recover -- ``sub_id`` stops at destination x module x locale x placement on purpose, since
it is what the partners see -- and stay NULL. The partner-link clicks (``status = 'clicked'``,
since 2026-09-13) carried the slug in ``destination_summary`` because waiting for this
column would have lost it, and still do; the click report reads
``coalesce(article_slug, destination_summary)`` for those rows instead of this migration
copying anything across.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0081_affiliate_click_article"
down_revision: str | None = "0080_crypto_and_tech_topics"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

INDEX = "ix_affiliate_clicks_article_slug"


def upgrade() -> None:
    if not context.is_offline_mode():
        inspector = sa.inspect(op.get_bind())
        columns = {column["name"] for column in inspector.get_columns("affiliate_clicks")}
        if "article_slug" in columns:
            return
    with op.batch_alter_table("affiliate_clicks") as batch:
        batch.add_column(sa.Column("article_slug", sa.String(120), nullable=True))
        batch.create_index(INDEX, ["article_slug"])


def downgrade() -> None:
    if not context.is_offline_mode():
        inspector = sa.inspect(op.get_bind())
        columns = {column["name"] for column in inspector.get_columns("affiliate_clicks")}
        if "article_slug" not in columns:
            return
    with op.batch_alter_table("affiliate_clicks") as batch:
        batch.drop_index(INDEX)
        batch.drop_column("article_slug")
