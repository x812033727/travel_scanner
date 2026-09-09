"""Capability roles and safe administration operations.

Revision ID: 0068_admin_operations_center
Revises: 0067_collection_inbox
"""

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
from alembic import context, op

revision: str = "0068_admin_operations_center"
down_revision: str | None = "0067_collection_inbox"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

ROLES = ("viewer", "support", "content", "operations", "database_operator", "deployer", "owner")
DB_OPERATION_STATUSES = ("queued", "running", "succeeded", "failed")
ERASURE_STATUSES = ("scheduled", "processing", "cancelled", "completed", "failed")


def _column_names(inspector: sa.Inspector | None, table: str) -> set[str]:
    if inspector is None or not inspector.has_table(table):
        return set()
    return {str(row["name"]) for row in inspector.get_columns(table)}


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    user_columns = _column_names(inspector, "users")
    for name, column_type in (
        ("last_login_at", sa.DateTime(timezone=True)),
        ("suspended_at", sa.DateTime(timezone=True)),
        ("suspended_until", sa.DateTime(timezone=True)),
        ("suspension_reason", sa.String(length=255)),
    ):
        if inspector is None or name not in user_columns:
            op.add_column("users", sa.Column(name, column_type, nullable=True))
    user_indexes = (
        set() if inspector is None else {str(row["name"]) for row in inspector.get_indexes("users")}
    )
    for column in ("last_login_at", "suspended_at", "suspended_until"):
        index_name = f"ix_users_{column}"
        if inspector is None or index_name not in user_indexes:
            op.create_index(index_name, "users", [column])

    has_roles = inspector is not None and inspector.has_table("admin_role_assignments")
    if not has_roles:
        op.create_table(
            "admin_role_assignments",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("user_id", sa.Uuid(), nullable=False),
            sa.Column("role", sa.String(length=32), nullable=False),
            sa.Column("granted_by_user_id", sa.Uuid(), nullable=True),
            sa.Column("source", sa.String(length=32), nullable=False),
            sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "role IN (" + ", ".join(f"'{role}'" for role in ROLES) + ")",
                name="ck_admin_role_assignment_role",
            ),
            sa.CheckConstraint(
                "source IN ('manual', 'legacy_backfill')",
                name="ck_admin_role_assignment_source",
            ),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["granted_by_user_id"], ["users.id"], ondelete="SET NULL"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("user_id", "role", name="uq_admin_role_assignment_user_role"),
        )
        op.create_index("ix_admin_role_assignments_user_id", "admin_role_assignments", ["user_id"])
        op.create_index("ix_admin_role_assignments_role", "admin_role_assignments", ["role"])
        op.create_index(
            "ix_admin_role_assignments_granted_by_user_id",
            "admin_role_assignments",
            ["granted_by_user_id"],
        )

    if inspector is not None:
        role_table = sa.table(
            "admin_role_assignments",
            sa.column("id", sa.Uuid()),
            sa.column("user_id", sa.Uuid()),
            sa.column("role", sa.String()),
            sa.column("granted_by_user_id", sa.Uuid()),
            sa.column("source", sa.String()),
            sa.column("expires_at", sa.DateTime(timezone=True)),
            sa.column("created_at", sa.DateTime(timezone=True)),
            sa.column("updated_at", sa.DateTime(timezone=True)),
        )
        existing = {
            (UUID(str(row.user_id)), row.role)
            for row in op.get_bind()
            .execute(sa.text("SELECT user_id, role FROM admin_role_assignments"))
            .all()
        }
        now = datetime.now(UTC)
        rows = []
        for (raw_user_id,) in op.get_bind().execute(sa.text("SELECT id FROM users WHERE is_admin")):
            user_id = UUID(str(raw_user_id))
            for role in ("support", "content", "operations"):
                if (user_id, role) not in existing:
                    rows.append(
                        {
                            "id": uuid4(),
                            "user_id": user_id,
                            "role": role,
                            "granted_by_user_id": None,
                            "source": "legacy_backfill",
                            "expires_at": None,
                            "created_at": now,
                            "updated_at": now,
                        }
                    )
        if rows:
            op.bulk_insert(role_table, rows)

    has_db_operations = inspector is not None and inspector.has_table("database_operation_runs")
    if not has_db_operations:
        op.create_table(
            "database_operation_runs",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("requested_by_user_id", sa.Uuid(), nullable=True),
            sa.Column("idempotency_key", sa.String(length=255), nullable=False),
            sa.Column("operation_type", sa.String(length=32), nullable=False),
            sa.Column("status", sa.String(length=32), nullable=False),
            sa.Column("agent_job_id", sa.String(length=64), nullable=True),
            sa.Column("backup_name", sa.String(length=255), nullable=True),
            sa.Column("checksum_sha256", sa.String(length=64), nullable=True),
            sa.Column("size_bytes", sa.BigInteger(), nullable=True),
            sa.Column("schema_revision", sa.String(length=64), nullable=True),
            sa.Column("release_sha", sa.String(length=40), nullable=True),
            sa.Column("failure_code", sa.String(length=64), nullable=True),
            sa.Column("failure_detail", sa.Text(), nullable=True),
            sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("metadata_json", sa.JSON(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "operation_type IN ('backup', 'analyze')",
                name="ck_database_operation_type",
            ),
            sa.CheckConstraint(
                "status IN (" + ", ".join(f"'{status}'" for status in DB_OPERATION_STATUSES) + ")",
                name="ck_database_operation_status",
            ),
            sa.ForeignKeyConstraint(["requested_by_user_id"], ["users.id"], ondelete="SET NULL"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("agent_job_id"),
            sa.UniqueConstraint(
                "requested_by_user_id",
                "idempotency_key",
                name="uq_database_operation_request_idempotency",
            ),
        )
        op.create_index(
            "ix_database_operation_runs_requested_by_user_id",
            "database_operation_runs",
            ["requested_by_user_id"],
        )
        op.create_index(
            "ix_database_operation_runs_operation_type",
            "database_operation_runs",
            ["operation_type"],
        )
        op.create_index("ix_database_operation_runs_status", "database_operation_runs", ["status"])
        op.create_index(
            "uq_database_operation_one_active",
            "database_operation_runs",
            [sa.text("(1)")],
            unique=True,
            postgresql_where=sa.text("status IN ('queued', 'running')"),
            sqlite_where=sa.text("status IN ('queued', 'running')"),
        )

    has_erasure = inspector is not None and inspector.has_table("account_erasure_requests")
    if not has_erasure:
        op.create_table(
            "account_erasure_requests",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("user_id", sa.Uuid(), nullable=False),
            sa.Column("requested_by_user_id", sa.Uuid(), nullable=True),
            sa.Column("idempotency_key", sa.String(length=255), nullable=False),
            sa.Column("status", sa.String(length=32), nullable=False),
            sa.Column("reason", sa.String(length=255), nullable=False),
            sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=False),
            sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("failure_code", sa.String(length=64), nullable=True),
            sa.Column("failure_detail", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "status IN (" + ", ".join(f"'{status}'" for status in ERASURE_STATUSES) + ")",
                name="ck_account_erasure_request_status",
            ),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["requested_by_user_id"], ["users.id"], ondelete="SET NULL"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint(
                "requested_by_user_id",
                "idempotency_key",
                name="uq_account_erasure_request_idempotency",
            ),
        )
        op.create_index(
            "ix_account_erasure_requests_user_id", "account_erasure_requests", ["user_id"]
        )
        op.create_index(
            "ix_account_erasure_requests_requested_by_user_id",
            "account_erasure_requests",
            ["requested_by_user_id"],
        )
        op.create_index(
            "ix_account_erasure_requests_status", "account_erasure_requests", ["status"]
        )
        op.create_index(
            "ix_account_erasure_requests_scheduled_for",
            "account_erasure_requests",
            ["scheduled_for"],
        )
        op.create_index(
            "uq_account_erasure_one_active",
            "account_erasure_requests",
            ["user_id"],
            unique=True,
            postgresql_where=sa.text("status IN ('scheduled', 'processing')"),
            sqlite_where=sa.text("status IN ('scheduled', 'processing')"),
        )

    if not context.is_offline_mode() and op.get_bind().dialect.name == "postgresql":
        # Older admin adjustments embedded the operator email in the append-only
        # usage ledger. Permit exactly one migration-time key removal, scrub all
        # historical rows, then immediately restore the strict mutation guard.
        op.execute(
            """
            CREATE OR REPLACE FUNCTION public.prevent_usage_ledger_mutation()
            RETURNS trigger AS $$
            BEGIN
                IF TG_OP = 'UPDATE'
                   AND NEW.id IS NOT DISTINCT FROM OLD.id
                   AND NEW.user_id IS NOT DISTINCT FROM OLD.user_id
                   AND NEW.account_id IS NOT DISTINCT FROM OLD.account_id
                   AND NEW.package_id IS NOT DISTINCT FROM OLD.package_id
                   AND NEW.entry_type IS NOT DISTINCT FROM OLD.entry_type
                   AND NEW.status IS NOT DISTINCT FROM OLD.status
                   AND NEW.amount IS NOT DISTINCT FROM OLD.amount
                   AND NEW.balance_after IS NOT DISTINCT FROM OLD.balance_after
                   AND NEW.reference IS NOT DISTINCT FROM OLD.reference
                   AND NEW.operation IS NOT DISTINCT FROM OLD.operation
                   AND NEW.summary IS NOT DISTINCT FROM OLD.summary
                   AND NEW.resource_id IS NOT DISTINCT FROM OLD.resource_id
                   AND NEW.unit IS NOT DISTINCT FROM OLD.unit
                   AND NEW.created_at IS NOT DISTINCT FROM OLD.created_at
                   AND NEW.metadata_json::jsonb = OLD.metadata_json::jsonb - 'actor_email'
                THEN
                    RETURN NEW;
                END IF;
                RAISE EXCEPTION 'usage_ledger is append-only';
            END;
            $$ LANGUAGE plpgsql
            """
        )
        op.execute(
            """
            UPDATE public.usage_ledger
            SET metadata_json = (metadata_json::jsonb - 'actor_email')::json
            WHERE metadata_json::jsonb ? 'actor_email'
            """
        )
        op.execute(
            """
            CREATE OR REPLACE FUNCTION public.prevent_usage_ledger_mutation()
            RETURNS trigger AS $$
            BEGIN
                RAISE EXCEPTION 'usage_ledger is append-only';
            END;
            $$ LANGUAGE plpgsql
            """
        )
        # Keep the click ledger immutable except for the one irreversible privacy
        # transition used by account erasure. Every commercial/audit field stays
        # append-only; direct edits and deletes still fail at the trigger.
        op.execute(
            """
            CREATE OR REPLACE FUNCTION public.prevent_affiliate_click_mutation()
            RETURNS trigger AS $$
            BEGIN
                IF TG_OP = 'UPDATE'
                   AND NEW.user_id IS NULL
                   AND NEW.search_id IS NULL
                   AND NEW.trip_id IS NULL
                   AND NEW.offer_id IS NULL
                   AND NEW.sub_id = ''
                   AND NEW.destination_summary = ''
                   AND NEW.id IS NOT DISTINCT FROM OLD.id
                   AND NEW.brand IS NOT DISTINCT FROM OLD.brand
                   AND NEW.service_type IS NOT DISTINCT FROM OLD.service_type
                   AND NEW.placement IS NOT DISTINCT FROM OLD.placement
                   AND NEW.destination_id IS NOT DISTINCT FROM OLD.destination_id
                   AND NEW.partner IS NOT DISTINCT FROM OLD.partner
                   AND NEW.module IS NOT DISTINCT FROM OLD.module
                   AND NEW.target_host IS NOT DISTINCT FROM OLD.target_host
                   AND NEW.status IS NOT DISTINCT FROM OLD.status
                   AND NEW.created_at IS NOT DISTINCT FROM OLD.created_at
                THEN
                    RETURN NEW;
                END IF;
                RAISE EXCEPTION 'affiliate_clicks is append-only';
            END;
            $$ LANGUAGE plpgsql
            """
        )
        op.execute(
            """
            CREATE OR REPLACE FUNCTION public.anonymize_affiliate_clicks_for_user(
                p_user_id uuid
            ) RETURNS bigint AS $$
            DECLARE
                affected bigint;
            BEGIN
                UPDATE public.affiliate_clicks AS click
                SET user_id = NULL,
                    search_id = NULL,
                    trip_id = NULL,
                    offer_id = NULL,
                    sub_id = '',
                    destination_summary = ''
                WHERE click.user_id = p_user_id
                   OR EXISTS (
                        SELECT 1 FROM public.trip_plans AS trip
                        WHERE trip.id = click.trip_id AND trip.user_id = p_user_id
                   )
                   OR EXISTS (
                        SELECT 1 FROM public.search_requests AS search
                        WHERE search.id = click.search_id AND search.user_id = p_user_id
                   )
                   OR EXISTS (
                        SELECT 1
                        FROM public.search_requests AS search
                        WHERE search.user_id = p_user_id
                          AND click.offer_id IN (
                              SELECT id FROM public.flight_offers
                              WHERE search_id = search.id
                              UNION ALL
                              SELECT id FROM public.hotel_offers
                              WHERE search_id = search.id
                              UNION ALL
                              SELECT id FROM public.activity_offers
                              WHERE search_id = search.id
                              UNION ALL
                              SELECT id FROM public.transport_offers
                              WHERE search_id = search.id
                          )
                   );
                GET DIAGNOSTICS affected = ROW_COUNT;
                RETURN affected;
            END;
            $$ LANGUAGE plpgsql
               SECURITY DEFINER
               SET search_path = pg_catalog, public
            """
        )
        op.execute(
            "REVOKE ALL ON FUNCTION public.anonymize_affiliate_clicks_for_user(uuid) FROM PUBLIC"
        )
        op.execute(
            """
            DO $$
            BEGIN
                EXECUTE format(
                    'GRANT EXECUTE ON FUNCTION ' ||
                    'public.anonymize_affiliate_clicks_for_user(uuid) TO %I',
                    current_user
                );
            END;
            $$
            """
        )


def downgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    if not context.is_offline_mode() and op.get_bind().dialect.name == "postgresql":
        op.execute(
            "DROP FUNCTION IF EXISTS public.anonymize_affiliate_clicks_for_user(uuid)"
        )
        op.execute(
            """
            CREATE OR REPLACE FUNCTION public.prevent_affiliate_click_mutation()
            RETURNS trigger AS $$
            BEGIN
                RAISE EXCEPTION 'affiliate_clicks is append-only';
            END;
            $$ LANGUAGE plpgsql
            """
        )
    if inspector is None or inspector.has_table("account_erasure_requests"):
        op.drop_table("account_erasure_requests")
    if inspector is None or inspector.has_table("database_operation_runs"):
        op.drop_table("database_operation_runs")
    if inspector is None or inspector.has_table("admin_role_assignments"):
        op.drop_table("admin_role_assignments")
    user_columns = _column_names(inspector, "users")
    user_indexes = (
        set() if inspector is None else {str(row["name"]) for row in inspector.get_indexes("users")}
    )
    for column in ("suspended_until", "suspended_at", "last_login_at"):
        index_name = f"ix_users_{column}"
        if inspector is None or index_name in user_indexes:
            op.drop_index(index_name, table_name="users")
    for name in ("suspension_reason", "suspended_until", "suspended_at", "last_login_at"):
        if inspector is None or name in user_columns:
            op.drop_column("users", name)
