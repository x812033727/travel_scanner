"""Durable USD 25 accounts and paid-operation holds for brand-story pilots.

Revision ID: 0132_video_pilot_budget
Revises: 0131_video_dub_retries

The original and isolated v2 pilot rows are created idempotently. A hold is committed before
vendor dispatch; its status and price ceiling survive a timeout or process restart. This is
additive so the previous API release can still run during application rollback.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import insert

revision: str = "0132_video_pilot_budget"
down_revision: str | None = "0131_video_dub_retries"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

ACCOUNT = "video_pilot_budgets"
OPERATIONS = "video_pilot_budget_operations"
PILOTS = (
    "story-rolling-suitcase",
    "story-conveyor-belt-sushi",
    "story-rolling-suitcase-v2",
    "story-conveyor-belt-sushi-v2",
)


def _tables() -> set[str]:
    return set() if op.get_context().as_sql else set(sa.inspect(op.get_bind()).get_table_names())


def upgrade() -> None:
    tables = _tables()
    if ACCOUNT not in tables:
        op.create_table(
            ACCOUNT,
            sa.Column("slug", sa.String(length=80), primary_key=True),
            sa.Column("limit_usd", sa.Numeric(12, 6), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.func.now(),
            ),
            sa.CheckConstraint("limit_usd = 25.000000", name="ck_video_pilot_budget_limit"),
        )
    if OPERATIONS not in tables:
        op.create_table(
            OPERATIONS,
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column(
                "slug",
                sa.String(length=80),
                sa.ForeignKey(f"{ACCOUNT}.slug", ondelete="RESTRICT"),
                nullable=False,
            ),
            sa.Column("operation_id", sa.String(length=160), nullable=False),
            sa.Column("category", sa.String(length=40), nullable=False),
            sa.Column("provider", sa.String(length=40), nullable=False),
            sa.Column("model", sa.String(length=128), nullable=False),
            sa.Column("max_usd", sa.Numeric(12, 6), nullable=False),
            sa.Column("actual_usd", sa.Numeric(12, 6), nullable=True),
            sa.Column("status", sa.String(length=12), nullable=False),
            sa.Column("attempts", sa.Integer(), nullable=False),
            sa.Column("receipt_ref", sa.String(length=255), nullable=True),
            sa.Column("release_reason", sa.String(length=255), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.func.now(),
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.func.now(),
            ),
            sa.UniqueConstraint("slug", "operation_id", name="uq_video_pilot_budget_operation"),
            sa.CheckConstraint(
                "status IN ('reserved', 'uncertain', 'settled', 'released')",
                name="ck_video_pilot_budget_operation_status",
            ),
            sa.CheckConstraint("max_usd > 0", name="ck_video_pilot_budget_operation_max"),
            sa.CheckConstraint(
                "actual_usd IS NULL OR actual_usd >= 0",
                name="ck_video_pilot_budget_operation_actual",
            ),
        )
        op.create_index("ix_video_pilot_budget_operations_slug", OPERATIONS, ["slug"])

    account = sa.table(
        ACCOUNT,
        sa.column("slug", sa.String(length=80)),
        sa.column("limit_usd", sa.Numeric(12, 6)),
    )
    for slug in PILOTS:
        op.execute(
            insert(account)
            .values(slug=slug, limit_usd=sa.literal(25))
            .on_conflict_do_nothing(index_elements=["slug"])
        )


def downgrade() -> None:
    tables = _tables()
    if op.get_context().as_sql or OPERATIONS in tables:
        op.drop_index("ix_video_pilot_budget_operations_slug", table_name=OPERATIONS)
        op.drop_table(OPERATIONS)
    if op.get_context().as_sql or ACCOUNT in tables:
        op.drop_table(ACCOUNT)
