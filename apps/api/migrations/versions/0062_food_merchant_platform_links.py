"""Add manually reviewed reservation-platform pages for food merchants."""

import sqlalchemy as sa
from alembic import context, op

revision = "0062_merchant_platform_links"
down_revision = "0061_merchant_styles"
branch_labels = None
depends_on = None


def upgrade() -> None:
    names = set() if context.is_offline_mode() else set(sa.inspect(op.get_bind()).get_table_names())
    if "food_merchant_platform_links" in names:
        return
    op.create_table(
        "food_merchant_platform_links",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "merchant_id",
            sa.Uuid(),
            sa.ForeignKey("food_merchants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("provider", sa.String(32), nullable=False),
        sa.Column("canonical_url", sa.String(2048)),
        sa.Column("localized_urls_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("checked_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "checked_by_user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
        ),
        sa.Column("review_note", sa.String(1000)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "merchant_id", "provider", name="uq_food_merchant_platform_provider"
        ),
        sa.UniqueConstraint("provider", "canonical_url", name="uq_food_merchant_platform_url"),
        sa.CheckConstraint(
            "status IN ('verified', 'not_found', 'ambiguous', 'disabled')",
            name="ck_food_merchant_platform_status",
        ),
        sa.CheckConstraint(
            "status != 'verified' OR canonical_url IS NOT NULL",
            name="ck_food_merchant_platform_verified_url",
        ),
    )
    op.create_index(
        "ix_food_merchant_platform_links_merchant_id",
        "food_merchant_platform_links",
        ["merchant_id"],
    )
    op.create_index(
        "ix_food_merchant_platform_links_provider",
        "food_merchant_platform_links",
        ["provider"],
    )
    op.create_index(
        "ix_food_merchant_platform_links_status",
        "food_merchant_platform_links",
        ["status"],
    )
    op.create_index(
        "ix_food_merchant_platform_links_checked_by_user_id",
        "food_merchant_platform_links",
        ["checked_by_user_id"],
    )


def downgrade() -> None:
    op.drop_table("food_merchant_platform_links")
