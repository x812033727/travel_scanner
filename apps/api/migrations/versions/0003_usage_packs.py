"""Replace monthly credits with non-expiring usage packs.

Revision ID: 0003_usage_packs
Revises: 0002_itinerary_sharing
"""

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

revision: str = "0003_usage_packs"
down_revision: str | None = "0002_itinerary_sharing"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _inspector() -> sa.Inspector:
    return sa.inspect(op.get_bind())


def _columns(table: str) -> set[str]:
    return {str(column["name"]) for column in _inspector().get_columns(table)}


def _indexes(table: str) -> set[str]:
    return {str(index["name"]) for index in _inspector().get_indexes(table)}


def upgrade() -> None:
    inspector = _inspector()
    if inspector.has_table("usage_reservations"):
        pending = op.get_bind().execute(
            sa.text("SELECT count(*) FROM usage_reservations WHERE status = 'reserved'")
        ).scalar_one()
        if int(pending):
            raise RuntimeError(
                "Drain or release all reserved usage requests before applying 0003_usage_packs"
            )
    if inspector.has_table("plans") and not inspector.has_table("usage_packages"):
        op.rename_table("plans", "usage_packages")
    inspector = _inspector()
    if inspector.has_table("subscriptions") and not inspector.has_table("usage_accounts"):
        op.rename_table("subscriptions", "usage_accounts")

    package_columns = _columns("usage_packages")
    if "monthly_credits" in package_columns and "uses" not in package_columns:
        op.alter_column("usage_packages", "monthly_credits", new_column_name="uses")
    package_columns = _columns("usage_packages")
    if "is_active" not in package_columns:
        op.add_column(
            "usage_packages",
            sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        )
    if "purchasable" not in package_columns:
        op.add_column(
            "usage_packages",
            sa.Column("purchasable", sa.Boolean(), server_default=sa.false(), nullable=False),
        )

    account_columns = _columns("usage_accounts")
    if "credit_balance" in account_columns and "remaining_uses" not in account_columns:
        op.alter_column("usage_accounts", "credit_balance", new_column_name="remaining_uses")
    account_columns = _columns("usage_accounts")
    if "reserved_uses" not in account_columns:
        op.add_column(
            "usage_accounts",
            sa.Column("reserved_uses", sa.Integer(), server_default="0", nullable=False),
        )
    for legacy_column in ("plan_id", "period_start", "period_end"):
        if legacy_column in account_columns:
            op.alter_column("usage_accounts", legacy_column, nullable=True)

    ledger_columns = _columns("usage_ledger")
    if "subscription_id" in ledger_columns and "account_id" not in ledger_columns:
        op.alter_column("usage_ledger", "subscription_id", new_column_name="account_id")
    ledger_columns = _columns("usage_ledger")
    additions: dict[str, sa.Column[object]] = {
        "package_id": sa.Column("package_id", sa.Uuid(), nullable=True),
        "status": sa.Column("status", sa.String(32), nullable=True),
        "operation": sa.Column("operation", sa.String(64), nullable=True),
        "summary": sa.Column("summary", sa.String(255), nullable=True),
        "resource_id": sa.Column("resource_id", sa.Uuid(), nullable=True),
        "unit": sa.Column(
            "unit", sa.String(32), server_default="legacy_credit", nullable=False
        ),
    }
    for name, column in additions.items():
        if name not in ledger_columns:
            op.add_column("usage_ledger", column)
    op.execute(
        sa.text(
            """
            UPDATE usage_ledger
            SET status = CASE entry_type
                WHEN 'debit' THEN 'charged'
                WHEN 'refund' THEN 'released'
                WHEN 'grant' THEN 'granted'
                WHEN 'expiry' THEN 'expired'
                ELSE 'adjusted'
            END
            WHERE status IS NULL
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE usage_ledger
            SET summary = CASE entry_type
                WHEN 'debit' THEN '舊制使用紀錄'
                WHEN 'refund' THEN '舊制退回紀錄'
                WHEN 'grant' THEN '舊制額度發放'
                WHEN 'expiry' THEN '舊制額度到期'
                ELSE '舊制人工調整'
            END
            WHERE summary IS NULL
            """
        )
    )
    op.alter_column("usage_ledger", "status", nullable=False)
    op.alter_column("usage_ledger", "summary", nullable=False)
    op.alter_column("usage_ledger", "unit", server_default="use")

    reservation_columns = _columns("usage_reservations")
    if "subscription_id" in reservation_columns and "account_id" not in reservation_columns:
        op.alter_column("usage_reservations", "subscription_id", new_column_name="account_id")
    reservation_columns = _columns("usage_reservations")
    if "credits" in reservation_columns and "uses" not in reservation_columns:
        op.alter_column("usage_reservations", "credits", new_column_name="uses")
    reservation_columns = _columns("usage_reservations")
    if "summary" not in reservation_columns:
        op.add_column("usage_reservations", sa.Column("summary", sa.String(255), nullable=True))
        op.execute(
            sa.text(
                "UPDATE usage_reservations SET summary = '舊制使用請求：' || operation "
                "WHERE summary IS NULL"
            )
        )
        op.alter_column("usage_reservations", "summary", nullable=False)

    ledger_indexes = _indexes("usage_ledger")
    if "ix_usage_ledger_package_id" not in ledger_indexes:
        op.create_index("ix_usage_ledger_package_id", "usage_ledger", ["package_id"])
    if "ix_usage_ledger_resource_id" not in ledger_indexes:
        op.create_index("ix_usage_ledger_resource_id", "usage_ledger", ["resource_id"])
    if "uq_usage_ledger_package_external_reference" not in ledger_indexes:
        op.create_index(
            "uq_usage_ledger_package_external_reference",
            "usage_ledger",
            ["reference"],
            unique=True,
            postgresql_where=sa.text("entry_type = 'package_grant'"),
        )
    foreign_keys = _inspector().get_foreign_keys("usage_ledger")
    has_package_fk = any(
        item.get("referred_table") == "usage_packages"
        and item.get("constrained_columns") == ["package_id"]
        for item in foreign_keys
    )
    if not has_package_fk:
        op.create_foreign_key(
            "fk_usage_ledger_package_id_usage_packages",
            "usage_ledger",
            "usage_packages",
            ["package_id"],
            ["id"],
        )

    checks = {
        str(item.get("name"))
        for item in _inspector().get_check_constraints("usage_accounts")
    }
    if "ck_usage_account_remaining_nonnegative" not in checks:
        op.create_check_constraint(
            "ck_usage_account_remaining_nonnegative", "usage_accounts", "remaining_uses >= 0"
        )
    if "ck_usage_account_reserved_nonnegative" not in checks:
        op.create_check_constraint(
            "ck_usage_account_reserved_nonnegative", "usage_accounts", "reserved_uses >= 0"
        )
    if "ck_usage_account_reserved_within_balance" not in checks:
        op.create_check_constraint(
            "ck_usage_account_reserved_within_balance",
            "usage_accounts",
            "reserved_uses <= remaining_uses",
        )

    packages = sa.table(
        "usage_packages",
        sa.column("id", sa.Uuid()),
        sa.column("code", sa.String()),
        sa.column("name", sa.String()),
        sa.column("uses", sa.Integer()),
        sa.column("price_twd", sa.Integer()),
        sa.column("is_active", sa.Boolean()),
        sa.column("purchasable", sa.Boolean()),
        sa.column("created_at", sa.DateTime(timezone=True)),
        sa.column("updated_at", sa.DateTime(timezone=True)),
    )
    connection = op.get_bind()
    connection.execute(
        packages.update()
        .where(packages.c.code.in_(["FREE", "PRO"]))
        .values(is_active=False, purchasable=False)
    )
    existing_codes = set(connection.execute(sa.select(packages.c.code)).scalars())
    now = datetime.now(UTC)
    for code, name, uses, price in (
        ("TRIAL_3", "註冊體驗", 3, 0),
        ("PACK_10", "輕量 10 次包", 10, 199),
        ("PACK_30", "常用 30 次包", 30, 499),
        ("PACK_100", "大量 100 次包", 100, 1299),
    ):
        if code not in existing_codes:
            connection.execute(
                packages.insert().values(
                    id=uuid4(),
                    code=code,
                    name=name,
                    uses=uses,
                    price_twd=price,
                    is_active=True,
                    purchasable=False,
                    created_at=now,
                    updated_at=now,
                )
            )

    accounts = sa.table(
        "usage_accounts",
        sa.column("id", sa.Uuid()),
        sa.column("user_id", sa.Uuid()),
        sa.column("remaining_uses", sa.Integer()),
    )
    ledger = sa.table(
        "usage_ledger",
        sa.column("id", sa.Uuid()),
        sa.column("user_id", sa.Uuid()),
        sa.column("account_id", sa.Uuid()),
        sa.column("entry_type", sa.String()),
        sa.column("status", sa.String()),
        sa.column("amount", sa.Integer()),
        sa.column("balance_after", sa.Integer()),
        sa.column("reference", sa.String()),
        sa.column("operation", sa.String()),
        sa.column("summary", sa.String()),
        sa.column("unit", sa.String()),
        sa.column("metadata_json", sa.JSON()),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    migration_reference = "migration:usage-packs:0003"
    migrated_users = set(
        connection.execute(
            sa.select(ledger.c.user_id).where(
                ledger.c.reference == migration_reference,
                ledger.c.entry_type == "migration",
            )
        ).scalars()
    )
    for account in connection.execute(sa.select(accounts)).mappings():
        if account["user_id"] in migrated_users:
            continue
        connection.execute(
            ledger.insert().values(
                id=uuid4(),
                user_id=account["user_id"],
                account_id=account["id"],
                entry_type="migration",
                status="migrated",
                amount=0,
                balance_after=account["remaining_uses"],
                reference=migration_reference,
                operation="legacy_credit_migration",
                summary="舊制餘額以 1:1 轉為永久使用次數",
                unit="use",
                metadata_json={"conversion": "1:1"},
                created_at=now,
            )
        )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION prevent_usage_ledger_mutation()
        RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION 'usage_ledger is append-only';
        END;
        $$ LANGUAGE plpgsql
        """
    )
    op.execute("DROP TRIGGER IF EXISTS usage_ledger_append_only ON usage_ledger")
    op.execute(
        """
        CREATE TRIGGER usage_ledger_append_only
        BEFORE UPDATE OR DELETE ON usage_ledger
        FOR EACH ROW EXECUTE FUNCTION prevent_usage_ledger_mutation()
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS usage_ledger_append_only ON usage_ledger")
    op.execute("DROP FUNCTION IF EXISTS prevent_usage_ledger_mutation()")
    # Balances and audit rows are deliberately preserved. Reverting to monthly
    # credits would discard user-owned value, so the schema downgrade stops at
    # removing the database mutation guard.
