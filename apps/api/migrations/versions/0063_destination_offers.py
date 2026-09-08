"""Add reviewed Travelpayouts offers scoped to a destination."""

import sqlalchemy as sa
from alembic import context, op

revision = "0063_destination_offers"
down_revision = "0062_merchant_platform_links"
branch_labels = None
depends_on = None


def upgrade() -> None:
    names = set() if context.is_offline_mode() else set(sa.inspect(op.get_bind()).get_table_names())
    if "destination_affiliate_offers" in names:
        return
    op.create_table(
        "destination_affiliate_offers",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "brand_id",
            sa.Uuid(),
            sa.ForeignKey("travel_service_brands.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("destination_id", sa.String(64), nullable=False),
        sa.Column("module", sa.String(32), nullable=False),
        sa.Column("target_url", sa.String(2048), nullable=False),
        sa.Column("static_url", sa.String(2048)),
        sa.Column("verification_context", sa.String(64)),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("verified_at", sa.DateTime(timezone=True)),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "brand_id",
            "destination_id",
            "module",
            name="uq_destination_affiliate_offer",
        ),
        sa.CheckConstraint(
            "module IN ('flight','hotel','activities','transport','connectivity')",
            name="ck_destination_affiliate_module",
        ),
        sa.CheckConstraint(
            "status IN ('pending','approved','disabled')",
            name="ck_destination_affiliate_status",
        ),
    )
    for column in ("brand_id", "destination_id", "module", "status"):
        op.create_index(
            f"ix_destination_affiliate_offers_{column}",
            "destination_affiliate_offers",
            [column],
        )


def downgrade() -> None:
    op.drop_table("destination_affiliate_offers")
