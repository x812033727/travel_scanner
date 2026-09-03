"""Add Google, LINE and Apple login identities.

Revision ID: 0033_social_login
Revises: 0032_remove_plus_codes
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0033_social_login"
down_revision: str | None = "0032_remove_plus_codes"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _tables() -> set[str]:
    if context.is_offline_mode():
        return set()
    return set(sa.inspect(op.get_bind()).get_table_names())


def _columns(table: str) -> dict[str, dict[str, object]]:
    if context.is_offline_mode():
        return {}
    return {column["name"]: column for column in sa.inspect(op.get_bind()).get_columns(table)}


def upgrade() -> None:
    offline = context.is_offline_mode()
    users = _columns("users")
    if offline or bool(users.get("password_hash", {}).get("nullable") is False):
        op.alter_column(
            "users",
            "password_hash",
            existing_type=sa.String(length=255),
            nullable=True,
        )

    if offline or "user_auth_identities" not in _tables():
        op.create_table(
            "user_auth_identities",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("user_id", sa.Uuid(), nullable=False),
            sa.Column("provider", sa.String(length=16), nullable=False),
            sa.Column("subject", sa.String(length=255), nullable=False),
            sa.Column("provider_email", sa.String(length=320), nullable=True),
            sa.Column("email_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("refresh_token_encrypted", sa.Text(), nullable=True),
            sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column(
                "revocation_pending", sa.Boolean(), nullable=False, server_default=sa.false()
            ),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "provider IN ('google', 'line', 'apple')",
                name="ck_user_auth_identity_provider",
            ),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint(
                "provider", "subject", name="uq_user_auth_identity_provider_subject"
            ),
        )
        op.create_index(
            "ix_user_auth_identities_provider", "user_auth_identities", ["provider"]
        )
        op.create_index(
            "ix_user_auth_identities_user_id", "user_auth_identities", ["user_id"]
        )


def downgrade() -> None:
    offline = context.is_offline_mode()
    if offline or "user_auth_identities" in _tables():
        op.drop_index("ix_user_auth_identities_user_id", table_name="user_auth_identities")
        op.drop_index("ix_user_auth_identities_provider", table_name="user_auth_identities")
        op.drop_table("user_auth_identities")
    if offline or "password_hash" in _columns("users"):
        op.execute(
            sa.text(
                "UPDATE users SET password_hash = '' WHERE password_hash IS NULL"
            )
        )
        op.alter_column(
            "users",
            "password_hash",
            existing_type=sa.String(length=255),
            nullable=False,
        )
