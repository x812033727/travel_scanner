"""Invitation-gated creators and reference-only videos on reviewed snapshots."""

import sqlalchemy as sa
from alembic import context, op

revision = "0066_discovery_community"
down_revision = "0065_travel_discovery"
branch_labels = None
depends_on = None


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    columns = (
        set()
        if inspector is None
        else {row["name"] for row in inspector.get_columns("community_post_revisions")}
    )
    if "video_refs" not in columns:
        op.add_column(
            "community_post_revisions",
            sa.Column("video_refs", sa.JSON(), nullable=False, server_default="[]"),
        )
    if inspector is None or not inspector.has_table("community_creator_invitations"):
        op.create_table(
            "community_creator_invitations",
            sa.Column(
                "user_id",
                sa.Uuid(),
                sa.ForeignKey("users.id", ondelete="CASCADE"),
                primary_key=True,
            ),
            sa.Column("invited", sa.Boolean(), nullable=False),
            sa.Column("version", sa.Integer(), nullable=False),
            sa.Column(
                "granted_by_user_id",
                sa.Uuid(),
                sa.ForeignKey("users.id", ondelete="SET NULL"),
                nullable=True,
            ),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint("version >= 1", name="ck_creator_invitation_version"),
        )


def downgrade() -> None:
    op.drop_table("community_creator_invitations")
    op.drop_column("community_post_revisions", "video_refs")
