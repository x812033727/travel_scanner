"""Independent reviewed hotel identities; retain IDs and project-free ordinary links."""

from collections.abc import Sequence
from uuid import NAMESPACE_URL, uuid5

import sqlalchemy as sa
from alembic import op

revision: str = "0057_hotel_booking_options"
down_revision: str | None = "0056_travel_services"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    existing = set(sa.inspect(bind).get_table_names())
    if "hotel_booking_options" not in existing:
        op.create_table(
            "hotel_booking_options",
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column(
                "product_id",
                sa.Uuid(),
                sa.ForeignKey("travel_service_products.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("provider", sa.String(32), nullable=False),
            sa.Column("url", sa.String(2048)),
            sa.Column("property_id", sa.String(255)),
            sa.Column("evidence_url", sa.String(2048)),
            sa.Column("identity_note", sa.String(1000), nullable=False),
            sa.Column("discovery_status", sa.String(16), nullable=False),
            sa.Column("status", sa.String(16), nullable=False),
            sa.Column("version", sa.Integer(), nullable=False),
            sa.Column("verified_at", sa.DateTime(timezone=True)),
            sa.Column("health_status", sa.String(16), nullable=False),
            sa.Column("checked_at", sa.DateTime(timezone=True)),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("product_id", "provider", name="uq_hotel_option_provider"),
            sa.UniqueConstraint("provider", "url", name="uq_hotel_option_url"),
            sa.UniqueConstraint("provider", "property_id", name="uq_hotel_option_identity"),
            sa.CheckConstraint(
                "status IN ('pending','approved','disabled')", name="ck_hotel_option_status"
            ),
            sa.CheckConstraint(
                "discovery_status IN ('found','not_found','unconfirmed')",
                name="ck_hotel_option_discovery",
            ),
        )
        op.create_index(
            "ix_hotel_booking_options_product_id", "hotel_booking_options", ["product_id"]
        )
        op.create_index("ix_hotel_booking_options_status", "hotel_booking_options", ["status"])
    if "hotel_booking_clicks" not in existing:
        op.create_table(
            "hotel_booking_clicks",
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column(
                "option_id",
                sa.Uuid(),
                sa.ForeignKey("hotel_booking_options.id", ondelete="SET NULL"),
            ),
            sa.Column("provider", sa.String(32), nullable=False),
            sa.Column("destination_id", sa.String(64), nullable=False),
            sa.Column("mode", sa.String(16), nullable=False),
            sa.Column("fallback", sa.Boolean(), nullable=False),
            sa.Column("placement", sa.String(24), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        )
        op.create_index(
            "ix_hotel_booking_clicks_created_at", "hotel_booking_clicks", ["created_at"]
        )
    products = sa.table(
        "travel_service_products",
        sa.column("id", sa.Uuid()),
        sa.column("facts", sa.JSON()),
        sa.column("kind"),
        sa.column("status"),
        sa.column("verified_at", sa.DateTime(timezone=True)),
        sa.column("created_at", sa.DateTime(timezone=True)),
        sa.column("updated_at", sa.DateTime(timezone=True)),
    )
    options = sa.Table("hotel_booking_options", sa.MetaData(), autoload_with=bind)
    for product in bind.execute(sa.select(products).where(products.c.kind == "hotel")).mappings():
        facts = dict(product["facts"] or {})
        links = facts.pop("hotel_links", [])
        for link in links:
            identifier = uuid5(
                NAMESPACE_URL, f"mokaair:hotel-option:{product['id']}:{link['provider']}"
            )
            if not bind.scalar(
                sa.select(options.c.id).where(
                    options.c.product_id == product["id"], options.c.provider == link["provider"]
                )
            ):
                bind.execute(
                    options.insert().values(
                        id=identifier,
                        product_id=product["id"],
                        provider=link["provider"],
                        url=link["url"],
                        evidence_url=link["evidence_url"],
                        identity_note="Legacy reviewed hotel link",
                        discovery_status="found",
                        status=product["status"],
                        version=1,
                        verified_at=product["verified_at"],
                        health_status="unchecked",
                        checked_at=None,
                        created_at=product["created_at"],
                        updated_at=product["updated_at"],
                    )
                )
        bind.execute(products.update().where(products.c.id == product["id"]).values(facts=facts))


def downgrade() -> None:
    bind = op.get_bind()
    products = sa.table(
        "travel_service_products",
        sa.column("id", sa.Uuid()),
        sa.column("facts", sa.JSON()),
        sa.column("status"),
        sa.column("verified_at", sa.DateTime(timezone=True)),
    )
    options = sa.Table("hotel_booking_options", sa.MetaData(), autoload_with=bind)
    for product in bind.execute(sa.select(products)).mappings():
        rows = list(
            bind.execute(sa.select(options).where(options.c.product_id == product["id"])).mappings()
        )
        if not rows:
            continue
        # An old client cannot represent independent review; fail closed on rollback.
        facts = {
            **product["facts"],
            "hotel_links": [
                {"provider": r["provider"], "url": r["url"], "evidence_url": r["evidence_url"]}
                for r in rows
                if r["discovery_status"] == "found"
            ],
        }
        bind.execute(
            products.update()
            .where(products.c.id == product["id"])
            .values(facts=facts, status="pending", verified_at=None)
        )
    op.drop_table("hotel_booking_clicks")
    op.drop_table("hotel_booking_options")
