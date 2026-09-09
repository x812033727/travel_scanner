"""Identify a private saved-reference inbox without moving existing favorites."""

import sqlalchemy as sa
from alembic import context, op

revision = "0067_collection_inbox"
down_revision = "0066_discovery_community"
branch_labels = None
depends_on = None


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    columns = (
        set()
        if inspector is None
        else {column["name"] for column in inspector.get_columns("community_collections")}
    )
    uniques = (
        set()
        if inspector is None
        else {row["name"] for row in inspector.get_unique_constraints("community_collections")}
    )
    checks = (
        set()
        if inspector is None
        else {row["name"] for row in inspector.get_check_constraints("community_collections")}
    )
    if "system_role" not in columns:
        op.add_column(
            "community_collections", sa.Column("system_role", sa.String(16), nullable=True)
        )
    # 0001 creates current metadata on fresh installations; every addition is guarded.
    with op.batch_alter_table("community_collections") as batch:
        if "uq_collection_system_role" not in uniques:
            batch.create_unique_constraint("uq_collection_system_role", ["user_id", "system_role"])
        if "ck_collection_system_role" not in checks:
            batch.create_check_constraint(
                "ck_collection_system_role", "system_role IS NULL OR system_role = 'inbox'"
            )
    # Opaque provider place IDs already support 255 characters in RestaurantPlace.
    # Growing the reference field lets organizing retain that existing contract.
    if inspector is None or inspector.has_table("community_collection_items"):
        target_type = (
            None
            if inspector is None
            else next(
                column["type"]
                for column in inspector.get_columns("community_collection_items")
                if column["name"] == "target"
            )
        )
        if target_type is None or target_type.length < 255:
            with op.batch_alter_table("community_collection_items") as batch:
                batch.alter_column("target", existing_type=sa.String(160), type_=sa.String(255))


def downgrade() -> None:
    # Keep the backward-compatible wider target column; shrinking could destroy references.
    with op.batch_alter_table("community_collections") as batch:
        batch.drop_constraint("ck_collection_system_role", type_="check")
        batch.drop_constraint("uq_collection_system_role", type_="unique")
        batch.drop_column("system_role")
