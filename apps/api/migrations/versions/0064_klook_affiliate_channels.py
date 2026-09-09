"""Separate direct Klook enrollment from Travelpayouts without changing existing IDs."""

import sqlalchemy as sa
from alembic import context, op

revision = "0064_klook_affiliate_channels"
down_revision = "0063_destination_offers"
branch_labels = None
depends_on = None


def upgrade() -> None:
    offline = context.is_offline_mode()
    inspector = None if offline else sa.inspect(op.get_bind())
    columns = (
        set()
        if inspector is None
        else {column["name"] for column in inspector.get_columns("travel_service_brands")}
    )
    if "channel" not in columns:
        op.add_column(
            "travel_service_brands",
            sa.Column("channel", sa.String(24), nullable=False, server_default="travelpayouts"),
        )
    constraints = (
        set()
        if inspector is None
        else {item["name"] for item in inspector.get_unique_constraints("travel_service_brands")}
    )
    if offline or "uq_service_brand_project" in constraints:
        op.drop_constraint("uq_service_brand_project", "travel_service_brands", type_="unique")
    if "uq_service_brand_channel_project" not in constraints:
        op.create_unique_constraint(
            "uq_service_brand_channel_project",
            "travel_service_brands",
            ["channel", "project_id", "code"],
        )
    checks = (
        set()
        if inspector is None
        else {item["name"] for item in inspector.get_check_constraints("travel_service_brands")}
    )
    for name, expression in {
        "ck_service_brand_channel": "channel IN ('travelpayouts','klook_direct')",
        "ck_service_brand_direct_klook": "channel != 'klook_direct' OR code = 'klook'",
    }.items():
        if name not in checks:
            op.create_check_constraint(name, "travel_service_brands", expression)


def downgrade() -> None:
    # Removing channel with direct enrollments would turn their approval into TP approval.
    if context.is_offline_mode():
        raise RuntimeError("Channel downgrade requires an online direct-enrollment safety check")
    if op.get_bind().scalar(
        sa.text("SELECT count(*) FROM travel_service_brands WHERE channel != 'travelpayouts'")
    ):
        raise RuntimeError("Cannot downgrade while direct affiliate enrollments exist")
    op.drop_constraint("ck_service_brand_direct_klook", "travel_service_brands", type_="check")
    op.drop_constraint("ck_service_brand_channel", "travel_service_brands", type_="check")
    op.drop_constraint("uq_service_brand_channel_project", "travel_service_brands", type_="unique")
    op.create_unique_constraint(
        "uq_service_brand_project", "travel_service_brands", ["project_id", "code"]
    )
    op.drop_column("travel_service_brands", "channel")
