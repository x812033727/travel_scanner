"""Add configurable usage packages and operation costs.

Revision ID: 0017_usage_settings
Revises: 0016_trip_route_segments
"""

from collections.abc import Sequence
from datetime import UTC, datetime

import sqlalchemy as sa
from alembic import op

revision: str = "0017_usage_settings"
down_revision: str | None = "0016_trip_route_segments"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LOCALES = ("zh-TW", "zh-CN", "en", "ja", "ko")
BUILTIN_NAMES: dict[str, dict[str, str]] = {
    "TRIAL_3": {
        "zh-TW": "註冊體驗",
        "zh-CN": "注册体验",
        "en": "Registration trial",
        "ja": "登録トライアル",
        "ko": "가입 체험",
    },
    "PACK_10": {
        "zh-TW": "輕量包",
        "zh-CN": "轻量包",
        "en": "Light pack",
        "ja": "ライトパック",
        "ko": "라이트 팩",
    },
    "PACK_30": {
        "zh-TW": "常用包",
        "zh-CN": "常用包",
        "en": "Standard pack",
        "ja": "スタンダードパック",
        "ko": "스탠다드 팩",
    },
    "PACK_100": {
        "zh-TW": "大量包",
        "zh-CN": "大容量包",
        "en": "Bulk pack",
        "ja": "大容量パック",
        "ko": "대용량 팩",
    },
}
OPERATIONS = (
    "travel_search",
    "flexible_flight_search",
    "flight_hotel_search",
    "full_trip_search",
    "multi_city_search",
    "public_airline_fare_search",
    "back_to_back_fare_search",
    "live_back_to_back_fare_search",
    "flight_status_lookup",
    "ai_itinerary_generation",
    "itinerary_optimization",
    "price_reoptimization",
)


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    columns = {str(column["name"]) for column in inspector.get_columns("usage_packages")}
    if "localized_names" not in columns:
        op.add_column(
            "usage_packages",
            sa.Column("localized_names", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        )
    if "display_order" not in columns:
        op.add_column(
            "usage_packages",
            sa.Column("display_order", sa.Integer(), nullable=False, server_default="100"),
        )
    if "is_featured" not in columns:
        op.add_column(
            "usage_packages",
            sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.false()),
        )

    packages = sa.table(
        "usage_packages",
        sa.column("id", sa.Uuid()),
        sa.column("code", sa.String()),
        sa.column("name", sa.String()),
        sa.column("localized_names", sa.JSON()),
        sa.column("display_order", sa.Integer()),
        sa.column("is_active", sa.Boolean()),
        sa.column("is_featured", sa.Boolean()),
    )
    connection = op.get_bind()
    package_rows = connection.execute(
        sa.select(packages.c.id, packages.c.code, packages.c.name, packages.c.is_active)
    ).mappings()
    for row in package_rows:
        names = BUILTIN_NAMES.get(str(row["code"])) or {
            locale: str(row["name"]) for locale in LOCALES
        }
        order = {"TRIAL_3": 0, "PACK_10": 10, "PACK_30": 20, "PACK_100": 30}.get(
            str(row["code"]), 100
        )
        connection.execute(
            packages.update()
            .where(packages.c.id == row["id"])
            .values(
                localized_names=names,
                display_order=order,
                is_featured=row["code"] == "PACK_30" and bool(row["is_active"]),
            )
        )

    indexes = {str(item["name"]) for item in inspector.get_indexes("usage_packages")}
    if "uq_usage_packages_single_active_featured" not in indexes:
        op.create_index(
            "uq_usage_packages_single_active_featured",
            "usage_packages",
            ["is_featured"],
            unique=True,
            postgresql_where=sa.text("is_active AND is_featured"),
        )

    inspector = sa.inspect(op.get_bind())
    if not inspector.has_table("usage_operation_costs"):
        op.create_table(
            "usage_operation_costs",
            sa.Column("operation", sa.String(64), primary_key=True),
            sa.Column("uses", sa.Integer(), nullable=False, server_default="1"),
            sa.Column(
                "updated_by_user_id",
                sa.Uuid(),
                sa.ForeignKey("users.id", ondelete="SET NULL"),
                nullable=True,
            ),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "uses >= 0 AND uses <= 100", name="ck_usage_operation_cost_range"
            ),
        )
        op.create_index(
            "ix_usage_operation_costs_updated_by_user_id",
            "usage_operation_costs",
            ["updated_by_user_id"],
        )

    costs = sa.table(
        "usage_operation_costs",
        sa.column("operation", sa.String()),
        sa.column("uses", sa.Integer()),
        sa.column("updated_by_user_id", sa.Uuid()),
        sa.column("created_at", sa.DateTime(timezone=True)),
        sa.column("updated_at", sa.DateTime(timezone=True)),
    )
    existing = set(connection.execute(sa.select(costs.c.operation)).scalars())
    now = datetime.now(UTC)
    for operation in OPERATIONS:
        if operation not in existing:
            connection.execute(
                costs.insert().values(
                    operation=operation,
                    uses=1,
                    updated_by_user_id=None,
                    created_at=now,
                    updated_at=now,
                )
            )


def downgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    if inspector.has_table("usage_operation_costs"):
        op.drop_index(
            "ix_usage_operation_costs_updated_by_user_id",
            table_name="usage_operation_costs",
        )
        op.drop_table("usage_operation_costs")
    indexes = {
        str(item["name"]) for item in sa.inspect(op.get_bind()).get_indexes("usage_packages")
    }
    if "uq_usage_packages_single_active_featured" in indexes:
        op.drop_index("uq_usage_packages_single_active_featured", table_name="usage_packages")
    columns = {
        str(column["name"])
        for column in sa.inspect(op.get_bind()).get_columns("usage_packages")
    }
    for name in ("is_featured", "display_order", "localized_names"):
        if name in columns:
            op.drop_column("usage_packages", name)
