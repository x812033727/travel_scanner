"""Administrator overrides for the web UI copy, layered over the JSON catalogs.

Revision ID: 0053_ui_text_overrides
Revises: 0052_repair_trend_merchant_names

The message catalogs under ``apps/web/messages`` stay the versioned defaults. This
table holds only the sentences an administrator changed: one row per namespace, key
and locale, so a missing row means "show the catalog text" and an override written for
zh-TW never leaks into en. ``default_snapshot`` keeps the catalog text the value was
validated against, which lets the editor point out when the default has moved since.

``legacy`` is refused here as well as in the API. That namespace drives
``legacy-ui-localizer.tsx``, a DOM substitution keyed by literal zh-TW strings, so an
override there would rewrite API data on screen.

0001 still calls the current ``Base.metadata.create_all``, so a fresh database already
has this table while one upgrading from 0052 does not. The create is guarded through
the operations context (so the migration tests can drive it without an environment)
and offline SQL generation runs unguarded. The branch only creates an empty table, so
it needs no case in ``test_migration_dead_branches``.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0053_ui_text_overrides"
down_revision: str | None = "0052_repair_trend_merchant_names"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "ui_text_overrides"
LOCALES_SQL = "('en', 'ja', 'ko', 'zh-TW', 'zh-CN')"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _tables() -> set[str]:
    if _offline():
        return set()
    return set(sa.inspect(op.get_bind()).get_table_names())


def upgrade() -> None:
    if _offline() or TABLE not in _tables():
        op.create_table(
            TABLE,
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("namespace", sa.String(length=64), nullable=False),
            sa.Column("key", sa.String(length=200), nullable=False),
            sa.Column("locale", sa.String(length=16), nullable=False),
            sa.Column("value", sa.Text(), nullable=False),
            sa.Column("default_snapshot", sa.Text(), nullable=True),
            sa.Column("updated_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["updated_by_user_id"], ["users.id"], ondelete="SET NULL"),
            sa.CheckConstraint(f"locale IN {LOCALES_SQL}", name="ck_ui_text_override_locale"),
            sa.CheckConstraint(
                "namespace <> 'legacy'", name="ck_ui_text_override_namespace_not_legacy"
            ),
            sa.CheckConstraint("length(value) > 0", name="ck_ui_text_override_value_not_empty"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint(
                "namespace", "key", "locale", name="uq_ui_text_override_key_locale"
            ),
        )
        op.create_index("ix_ui_text_overrides_locale", TABLE, ["locale"])
        op.create_index("ix_ui_text_overrides_updated_by_user_id", TABLE, ["updated_by_user_id"])


def downgrade() -> None:
    if _offline() or TABLE in _tables():
        op.drop_table(TABLE)
