"""Independent, source-backed merchant style reviews (no automatic approvals)."""

import sqlalchemy as sa
from alembic import context, op

revision = "0061_merchant_styles"
down_revision = "0060_community_places"
branch_labels = None
depends_on = None


def upgrade() -> None:
    names = set() if context.is_offline_mode() else set(sa.inspect(op.get_bind()).get_table_names())
    if "food_merchant_styles" in names:
        return
    op.create_table(
        "food_merchant_styles",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "merchant_id",
            sa.Uuid(),
            sa.ForeignKey("food_merchants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("style", sa.String(24), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("evidence_url", sa.String(2048), nullable=False),
        sa.Column("evidence_title", sa.String(255), nullable=False),
        sa.Column("rationale", sa.String(1000), nullable=False),
        sa.Column("checked_on", sa.Date(), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(timezone=True)),
        sa.Column("reviewed_by_user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("merchant_id", "style", name="uq_food_merchant_style"),
        sa.CheckConstraint("style IN ('instagrammable', 'artsy')", name="ck_merchant_style"),
        sa.CheckConstraint(
            "status IN ('pending', 'approved', 'rejected')", name="ck_merchant_style_status"
        ),
    )
    op.create_index("ix_food_merchant_styles_merchant_id", "food_merchant_styles", ["merchant_id"])


def downgrade() -> None:
    op.drop_table("food_merchant_styles")
