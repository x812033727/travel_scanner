"""Versioned drafts and explicit publication of public information pages.

Revision ID: 0069_site_pages
Revises: 0068_admin_operations_center
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0069_site_pages"
down_revision: str | None = "0068_admin_operations_center"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    # 0001 creates current metadata on a fresh database. Never recreate those
    # tables or seed/overwrite a draft as a side effect of a migration.
    if inspector is None or not inspector.has_table("site_pages"):
        op.create_table(
            "site_pages",
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column("slug", sa.String(16), nullable=False),
            sa.Column("locale", sa.String(16), nullable=False),
            sa.Column("version", sa.Integer(), nullable=False),
            sa.Column("draft_json", sa.JSON(), nullable=False),
            sa.Column("published_version", sa.Integer(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("slug", "locale", name="uq_site_page_slug_locale"),
            sa.CheckConstraint(
                "slug IN ('privacy', 'terms', 'about', 'contact')", name="ck_site_page_slug"
            ),
            sa.CheckConstraint(
                "locale IN ('en', 'ja', 'ko', 'zh-TW', 'zh-CN')", name="ck_site_page_locale"
            ),
            sa.CheckConstraint("version >= 1", name="ck_site_page_version"),
            sa.CheckConstraint(
                "published_version IS NULL OR "
                "(published_version >= 1 AND published_version <= version)",
                name="ck_site_page_published_version",
            ),
        )
    if inspector is None or not inspector.has_table("site_page_revisions"):
        op.create_table(
            "site_page_revisions",
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column("page_id", sa.Uuid(), sa.ForeignKey("site_pages.id"), nullable=False),
            sa.Column("version", sa.Integer(), nullable=False),
            sa.Column("action", sa.String(32), nullable=False),
            sa.Column("document_json", sa.JSON(), nullable=False),
            sa.Column(
                "created_by_user_id",
                sa.Uuid(),
                sa.ForeignKey("users.id", ondelete="SET NULL"),
                nullable=True,
            ),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("page_id", "version", name="uq_site_page_revision_version"),
            sa.CheckConstraint("version >= 1", name="ck_site_page_revision_version"),
            sa.CheckConstraint(
                "action IN ('initialized', 'draft_saved', 'published', 'restored')",
                name="ck_site_page_revision_action",
            ),
        )
        op.create_index("ix_site_page_revisions_page_id", "site_page_revisions", ["page_id"])

    if not context.is_offline_mode() and op.get_bind().dialect.name == "postgresql":
        op.execute("""
            CREATE OR REPLACE FUNCTION public.prevent_site_page_revision_mutation()
            RETURNS trigger AS $$
            BEGIN
                IF TG_OP = 'UPDATE'
                   AND OLD.created_by_user_id IS NOT NULL
                   AND NEW.created_by_user_id IS NULL
                   AND (to_jsonb(NEW) - 'created_by_user_id') =
                       (to_jsonb(OLD) - 'created_by_user_id')
                THEN
                    RETURN NEW;
                END IF;
                RAISE EXCEPTION 'site_page_revisions is append-only';
            END;
            $$ LANGUAGE plpgsql
        """)
        op.execute("DROP TRIGGER IF EXISTS site_page_revisions_append_only ON site_page_revisions")
        op.execute("""
            CREATE TRIGGER site_page_revisions_append_only
            BEFORE UPDATE OR DELETE ON site_page_revisions
            FOR EACH ROW EXECUTE FUNCTION public.prevent_site_page_revision_mutation()
        """)
    elif not context.is_offline_mode() and op.get_bind().dialect.name == "sqlite":
        op.execute("""
            CREATE TRIGGER IF NOT EXISTS site_page_revisions_no_delete
            BEFORE DELETE ON site_page_revisions
            BEGIN SELECT RAISE(ABORT, 'site_page_revisions is append-only'); END
        """)
        op.execute("""
            CREATE TRIGGER IF NOT EXISTS site_page_revisions_no_update
            BEFORE UPDATE ON site_page_revisions
            WHEN NOT (
                OLD.created_by_user_id IS NOT NULL AND NEW.created_by_user_id IS NULL
                AND NEW.id IS OLD.id AND NEW.page_id IS OLD.page_id
                AND NEW.version IS OLD.version AND NEW.action IS OLD.action
                AND NEW.document_json IS OLD.document_json AND NEW.created_at IS OLD.created_at
            )
            BEGIN SELECT RAISE(ABORT, 'site_page_revisions is append-only'); END
        """)


def downgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    if inspector is None or inspector.has_table("site_page_revisions"):
        op.drop_table("site_page_revisions")
    if inspector is None or inspector.has_table("site_pages"):
        op.drop_table("site_pages")
    if not context.is_offline_mode() and op.get_bind().dialect.name == "postgresql":
        op.execute("DROP FUNCTION IF EXISTS public.prevent_site_page_revision_mutation()")
