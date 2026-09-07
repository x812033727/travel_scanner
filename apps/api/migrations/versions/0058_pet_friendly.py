"""Reviewed pet places and evidence; guarded for current-metadata fresh installs."""

import sqlalchemy as sa
from alembic import context, op

revision = "0058_pet_friendly"
down_revision = "0057_community"
branch_labels = None
depends_on = None


def upgrade() -> None:
    names = set() if context.is_offline_mode() else set(sa.inspect(op.get_bind()).get_table_names())
    if "pet_places" not in names:
        op.create_table(
            "pet_places",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("identity_key", sa.String(length=200), nullable=True),
            sa.Column("name", sa.String(length=160), nullable=False),
            sa.Column("names", sa.JSON(), nullable=False),
            sa.Column("kind", sa.String(length=20), nullable=False),
            sa.Column("country", sa.String(length=2), nullable=False),
            sa.Column("destination", sa.String(length=160), nullable=False),
            sa.Column("address", sa.String(length=400), nullable=False),
            sa.Column("official_url", sa.String(length=2048), nullable=True),
            sa.Column("latitude", sa.Float(), nullable=True),
            sa.Column("longitude", sa.Float(), nullable=True),
            sa.Column("coordinate_source_url", sa.String(length=2048), nullable=True),
            sa.Column("status", sa.String(length=16), nullable=False),
            sa.Column("policies", sa.JSON(), nullable=False),
            sa.Column("source_url", sa.String(length=2048), nullable=True),
            sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("verified_by", sa.Uuid(), nullable=True),
            sa.Column("disputed", sa.Boolean(), nullable=False),
            sa.Column("version", sa.Integer(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "status IN ('pending','approved','rejected','disabled')", name="ck_pet_place_status"
            ),
            sa.ForeignKeyConstraint(
                ["verified_by"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("identity_key"),
        )
        op.create_index(op.f("ix_pet_places_country"), "pet_places", ["country"], unique=False)
        op.create_index(
            op.f("ix_pet_places_destination"), "pet_places", ["destination"], unique=False
        )
        op.create_index(op.f("ix_pet_places_kind"), "pet_places", ["kind"], unique=False)
        op.create_index(op.f("ix_pet_places_status"), "pet_places", ["status"], unique=False)
    if "pet_place_references" not in names:
        op.create_table(
            "pet_place_references",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("place_id", sa.Uuid(), nullable=False),
            sa.Column("kind", sa.String(length=20), nullable=False),
            sa.Column("target", sa.String(length=160), nullable=False),
            sa.ForeignKeyConstraint(
                ["place_id"],
                ["pet_places.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("kind", "target", name="uq_pet_place_reference"),
        )
        op.create_index(
            op.f("ix_pet_place_references_place_id"),
            "pet_place_references",
            ["place_id"],
            unique=False,
        )
    if "pet_policy_history" not in names:
        op.create_table(
            "pet_policy_history",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("place_id", sa.Uuid(), nullable=False),
            sa.Column("actor_id", sa.Uuid(), nullable=False),
            sa.Column("before", sa.JSON(), nullable=False),
            sa.Column("after", sa.JSON(), nullable=False),
            sa.Column("reason", sa.String(length=1000), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["actor_id"],
                ["users.id"],
            ),
            sa.ForeignKeyConstraint(
                ["place_id"],
                ["pet_places.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            op.f("ix_pet_policy_history_place_id"), "pet_policy_history", ["place_id"], unique=False
        )
    if "pet_reports" not in names:
        op.create_table(
            "pet_reports",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("place_id", sa.Uuid(), nullable=False),
            sa.Column("reporter_id", sa.Uuid(), nullable=False),
            sa.Column("body", sa.String(length=2000), nullable=False),
            sa.Column("source_url", sa.String(length=2048), nullable=True),
            sa.Column("visited_on", sa.Date(), nullable=True),
            sa.Column("media_ids", sa.JSON(), nullable=False),
            sa.Column("proposed_policies", sa.JSON(), nullable=False),
            sa.Column("status", sa.String(length=16), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["place_id"],
                ["pet_places.id"],
            ),
            sa.ForeignKeyConstraint(
                ["reporter_id"],
                ["users.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_pet_reports_place_id"), "pet_reports", ["place_id"], unique=False)
        op.create_index(
            op.f("ix_pet_reports_reporter_id"), "pet_reports", ["reporter_id"], unique=False
        )
        op.create_index(op.f("ix_pet_reports_status"), "pet_reports", ["status"], unique=False)


def downgrade() -> None:
    op.drop_table("pet_reports")
    op.drop_table("pet_policy_history")
    op.drop_table("pet_place_references")
    op.drop_table("pet_places")
