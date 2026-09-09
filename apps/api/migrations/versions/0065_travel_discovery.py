"""Private, erasable explicit discovery preferences; no content or browsing log."""

import sqlalchemy as sa
from alembic import context, op

from app.discovery import models  # noqa: F401 -- register current metadata for fresh 0001

revision = "0065_travel_discovery"
down_revision = "0064_klook_affiliate_channels"
branch_labels = None
depends_on = None


def upgrade() -> None:
    tables = (
        set() if context.is_offline_mode() else set(sa.inspect(op.get_bind()).get_table_names())
    )
    if "discovery_preferences" not in tables:
        op.create_table(
            "discovery_preferences",
            sa.Column(
                "user_id",
                sa.Uuid(),
                sa.ForeignKey("users.id", ondelete="CASCADE"),
                primary_key=True,
            ),
            sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
            sa.Column("destinations", sa.JSON(), nullable=False),
            sa.Column("topics", sa.JSON(), nullable=False),
            sa.Column("include_saved", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("include_following", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint("version >= 1", name="ck_discovery_preference_version"),
        )
    if "discovery_dismissals" not in tables:
        op.create_table(
            "discovery_dismissals",
            sa.Column(
                "user_id",
                sa.Uuid(),
                sa.ForeignKey("users.id", ondelete="CASCADE"),
                primary_key=True,
            ),
            sa.Column("content_key", sa.String(64), primary_key=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        )


def downgrade() -> None:
    op.drop_table("discovery_dismissals")
    op.drop_table("discovery_preferences")
