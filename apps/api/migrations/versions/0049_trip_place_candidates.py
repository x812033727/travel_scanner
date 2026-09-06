"""The waiting list a traveller pastes links into.

Revision ID: 0049_trip_place_candidates
Revises: 0048_repair_merchant_citations

A pasted link is a candidate, not a decision: it lands here until the traveller drops it
into a day. This is a real table rather than a cache because the itinerary work reads
candidates back when it compares what it offered with what is being applied, and a cache
that expired between the two would turn every apply into a conflict.

``google_place_id`` is stored as the resolver read it. When it matches a hotspot in the
catalogue the row also points at that hotspot, so the planner can show the name in the
reader's language and the depth score the catalogue already has, instead of the raw text
somebody pasted.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0049_trip_place_candidates"
down_revision: str | None = "0048_repair_merchant_citations"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "trip_place_candidates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "trip_plan_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("trip_plans.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "hotspot_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("travel_hotspots.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("raw_input", sa.Text(), nullable=False),
        sa.Column("source", sa.String(length=16), nullable=False, server_default="text"),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="inbox"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("location_name", sa.String(length=255), nullable=True),
        sa.Column("google_place_id", sa.String(length=255), nullable=True),
        sa.Column("maps_url", sa.String(length=2048), nullable=True),
        sa.Column("latitude", sa.Numeric(9, 6), nullable=True),
        sa.Column("longitude", sa.Numeric(9, 6), nullable=True),
        sa.Column("names_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("data", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint(
            "status in ('inbox', 'used', 'dismissed')",
            name="ck_trip_place_candidate_status",
        ),
    )
    op.create_index(
        "ix_trip_place_candidates_trip_status",
        "trip_place_candidates",
        ["trip_plan_id", "status"],
    )


def downgrade() -> None:
    op.drop_index("ix_trip_place_candidates_trip_status", table_name="trip_place_candidates")
    op.drop_table("trip_place_candidates")
