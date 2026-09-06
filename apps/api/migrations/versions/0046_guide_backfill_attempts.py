"""A ledger of which (hotspot, locale) pairs the automatic guide backfill has searched.

Revision ID: 0046_guide_backfill_attempts
Revises: 0045_food_seed_ownership

The backfill now works through a list of locales, one pass each, and only the guides
that were found used to leave a trace. A hotspot with genuinely nothing in Korean
would otherwise be searched again on every run for as long as the collector lives;
this table lets the statement skip a pair that was tried recently.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0046_guide_backfill_attempts"
down_revision: str | None = "0045_food_seed_ownership"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    if "hotspot_guide_backfill_attempts" in set(inspector.get_table_names()):
        return
    op.create_table(
        "hotspot_guide_backfill_attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("hotspot_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("locale", sa.String(length=16), nullable=False),
        sa.Column("outcome", sa.String(length=16), nullable=False),
        sa.Column("created_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("attempted_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["hotspot_id"], ["travel_hotspots.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hotspot_id", "locale", name="uq_hotspot_guide_backfill_attempt"),
        sa.CheckConstraint(
            "locale IN ('en', 'ja', 'ko', 'zh-TW', 'zh-CN')",
            name="ck_hotspot_guide_backfill_attempt_locale",
        ),
        sa.CheckConstraint(
            "outcome IN ('found', 'nothing')",
            name="ck_hotspot_guide_backfill_attempt_outcome",
        ),
    )
    op.create_index(
        "ix_hotspot_guide_backfill_attempts_hotspot_id",
        "hotspot_guide_backfill_attempts",
        ["hotspot_id"],
    )
    op.create_index(
        "ix_hotspot_guide_backfill_attempts_locale",
        "hotspot_guide_backfill_attempts",
        ["locale"],
    )


def downgrade() -> None:
    op.drop_table("hotspot_guide_backfill_attempts")
