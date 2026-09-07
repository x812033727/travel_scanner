"""Typed catalog references on immutable post versions; legacy pet IDs remain readable."""

import sqlalchemy as sa
from alembic import context, op

revision = "0060_community_places"
down_revision = "0059_pet_friendly"
branch_labels = None
depends_on = None


def upgrade() -> None:
    columns = (
        set()
        if context.is_offline_mode()
        else {
            row["name"] for row in sa.inspect(op.get_bind()).get_columns("community_post_revisions")
        }
    )
    if "place_refs" not in columns:
        op.add_column(
            "community_post_revisions",
            sa.Column("place_refs", sa.JSON(), nullable=False, server_default="[]"),
        )


def downgrade() -> None:
    op.drop_column("community_post_revisions", "place_refs")
