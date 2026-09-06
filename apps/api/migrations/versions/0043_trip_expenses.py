"""A per-day expense ledger, with its own budget and currency.

Revision ID: 0043_trip_expenses
Revises: 0042_trip_notes
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0043_trip_expenses"
down_revision: str | None = "0042_trip_notes"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    columns = {str(column["name"]) for column in inspector.get_columns("trip_plans")}
    if "budget_amount" not in columns:
        op.add_column("trip_plans", sa.Column("budget_amount", sa.Numeric(14, 2), nullable=True))
        # The budget picked during the original search has been sitting in the
        # immutable preferences blob; carry it over as the ledger's opening
        # target so an existing trip has something to compare against.
        op.execute(
            """
            UPDATE trip_plans
            SET budget_amount = (data -> 'preferences' ->> 'budget_twd')::numeric
            WHERE budget_amount IS NULL
              AND data -> 'preferences' ->> 'budget_twd' ~ '^[0-9]+(\\.[0-9]+)?$'
            """
        )
    if "cost_currency" not in columns:
        op.add_column(
            "trip_plans",
            sa.Column(
                "cost_currency",
                sa.String(length=3),
                nullable=False,
                server_default="TWD",
            ),
        )

    if "trip_expenses" not in set(inspector.get_table_names()):
        op.create_table(
            "trip_expenses",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("trip_plan_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("day_date", sa.Date(), nullable=False),
            sa.Column("label", sa.String(length=120), nullable=False),
            sa.Column("amount", sa.Numeric(14, 2), nullable=False),
            sa.Column("category", sa.String(length=24), nullable=False, server_default="other"),
            sa.Column("source", sa.String(length=16), nullable=False, server_default="manual"),
            sa.Column("source_key", sa.String(length=64), nullable=True),
            sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["trip_plan_id"], ["trip_plans.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            # NULLs compare distinct here, so hand-typed rows stay unconstrained
            # while a seeded source can only land once.
            sa.UniqueConstraint("trip_plan_id", "source_key", name="uq_trip_expense_source"),
            sa.CheckConstraint(
                "category IN ('flight', 'lodging', 'transport', 'food', "
                "'activity', 'shopping', 'other')",
                name="ck_trip_expense_category",
            ),
            sa.CheckConstraint("source IN ('manual', 'seeded')", name="ck_trip_expense_source"),
            sa.CheckConstraint("amount >= 0", name="ck_trip_expense_amount"),
        )
        op.create_index("ix_trip_expenses_trip_plan_id", "trip_expenses", ["trip_plan_id"])
        op.create_index("ix_trip_expenses_day_date", "trip_expenses", ["day_date"])


def downgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    if "trip_expenses" in set(inspector.get_table_names()):
        op.drop_index("ix_trip_expenses_day_date", table_name="trip_expenses")
        op.drop_index("ix_trip_expenses_trip_plan_id", table_name="trip_expenses")
        op.drop_table("trip_expenses")
    columns = {str(column["name"]) for column in inspector.get_columns("trip_plans")}
    if "cost_currency" in columns:
        op.drop_column("trip_plans", "cost_currency")
    if "budget_amount" in columns:
        op.drop_column("trip_plans", "budget_amount")
