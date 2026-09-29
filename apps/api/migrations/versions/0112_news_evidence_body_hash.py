"""A story-only hash beside each news evidence page's content hash.

Revision ID: 0112_news_evidence_body_hash
Revises: 0111_video_story_series

``content_hash`` covers the whole story region, so a re-rendered player id, a reordered
"most popular" rail or relative times held TechCrunch, Verge and CoinDesk stories at publish as
changed evidence. ``news_evidence.body_hash`` holds ``policy.body_fingerprint``, which covers
the story elements alone, and revalidation compares it when both the stored row and the current
page have one. ``news_candidates.body_hash`` is the lead page's, for the scanner's duplicate
check across URLs, hence its index.

Both columns are nullable and not backfilled: a stored row cannot be re-hashed without the page
it was read from, and rows without one keep being compared by ``content_hash``. 0001 builds a
fresh database from the current models, so each column and the index are added only when
missing. The downgrade drops them; the previous release never reads them.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0112_news_evidence_body_hash"
down_revision: str | None = "0111_video_story_series"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

EVIDENCE = "news_evidence"
CANDIDATES = "news_candidates"
COLUMN = "body_hash"
INDEX = "ix_news_candidates_body_hash"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _columns(table: str) -> set[str]:
    if _offline():
        return set()
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(table)}


def _indexes(table: str) -> set[str]:
    if _offline():
        return set()
    return {str(index.get("name")) for index in sa.inspect(op.get_bind()).get_indexes(table)}


def upgrade() -> None:
    for table in (EVIDENCE, CANDIDATES):
        if COLUMN not in _columns(table):
            op.add_column(table, sa.Column(COLUMN, sa.String(80), nullable=True))
    if INDEX not in _indexes(CANDIDATES):
        op.create_index(INDEX, CANDIDATES, [COLUMN])


def downgrade() -> None:
    if _offline() or INDEX in _indexes(CANDIDATES):
        op.drop_index(INDEX, table_name=CANDIDATES)
    for table in (EVIDENCE, CANDIDATES):
        if _offline() or COLUMN in _columns(table):
            op.drop_column(table, COLUMN)
