"""Give a trip a real notes column and per-day notes.

Revision ID: 0042_trip_notes
Revises: 0041_ai_itinerary_refine
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0042_trip_notes"
down_revision: str | None = "0041_ai_itinerary_refine"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    columns = {str(column["name"]) for column in inspector.get_columns("trip_plans")}
    if "notes" not in columns:
        op.add_column("trip_plans", sa.Column("notes", sa.Text(), nullable=True))
        # The brief typed at creation has been living in trip.data["notes"],
        # where reoptimize_trip's wholesale rebuild of that blob silently drops
        # it. Move what is still there into the column that will keep it.
        op.execute(
            """
            UPDATE trip_plans
            SET notes = data ->> 'notes'
            WHERE notes IS NULL
              AND data ? 'notes'
              AND nullif(trim(data ->> 'notes'), '') IS NOT NULL
            """
        )

    if "trip_day_notes" not in set(inspector.get_table_names()):
        op.create_table(
            "trip_day_notes",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("trip_plan_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("day_date", sa.Date(), nullable=False),
            sa.Column("notes", sa.Text(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["trip_plan_id"], ["trip_plans.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("trip_plan_id", "day_date", name="uq_trip_day_note"),
        )
        op.create_index("ix_trip_day_notes_trip_plan_id", "trip_day_notes", ["trip_plan_id"])
        op.create_index("ix_trip_day_notes_day_date", "trip_day_notes", ["day_date"])


def downgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    if "trip_day_notes" in set(inspector.get_table_names()):
        op.drop_index("ix_trip_day_notes_day_date", table_name="trip_day_notes")
        op.drop_index("ix_trip_day_notes_trip_plan_id", table_name="trip_day_notes")
        op.drop_table("trip_day_notes")
    columns = {str(column["name"]) for column in inspector.get_columns("trip_plans")}
    if "notes" in columns:
        op.drop_column("trip_plans", "notes")
