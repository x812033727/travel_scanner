"""Hotspot themes (season and shop-type tags), first-party intros and their AI runs.

Revision ID: 0050_hotspot_themes_intros
Revises: 0049_trip_place_candidates

A hotspot keeps its one ``category`` and gains any number of themes: the season it is
known for, with the months that apply (overridable per hotspot, because Sapporo's
sakura is May), or the kind of shop it is. ``hotspot_intros`` holds the one first-party
paragraph per hotspot and locale that readers see once an administrator approves it;
``hotspot_intro_runs`` records each AI drafting job the way
``hotspot_guide_ai_search_runs`` does for guide searches.

0001 still calls the current ``Base.metadata.create_all``, so a fresh database already
has these tables while one upgrading from 0049 does not. Every step inspects first
(through the operations context, so the migration tests can drive it without an
environment), and offline SQL generation runs unguarded.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0050_hotspot_themes_intros"
down_revision: str | None = "0049_trip_place_candidates"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

THEMES = "hotspot_themes"
LINKS = "hotspot_theme_links"
INTROS = "hotspot_intros"
RUNS = "hotspot_intro_runs"
LOCALES_SQL = "('en', 'ja', 'ko', 'zh-TW', 'zh-CN')"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _tables() -> set[str]:
    if _offline():
        return set()
    return set(sa.inspect(op.get_bind()).get_table_names())


def _timestamps() -> list[sa.Column[object]]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    ]


def upgrade() -> None:
    tables = _tables()
    if _offline() or THEMES not in tables:
        op.create_table(
            THEMES,
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("slug", sa.String(length=64), nullable=False),
            sa.Column("kind", sa.String(length=16), nullable=False),
            sa.Column("names_json", sa.JSON(), nullable=False, server_default="{}"),
            sa.Column("months_json", sa.JSON(), nullable=False, server_default="[]"),
            sa.Column("display_order", sa.Integer(), nullable=False, server_default="100"),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("source", sa.String(length=16), nullable=False, server_default="admin"),
            *_timestamps(),
            sa.CheckConstraint("kind IN ('season', 'shop')", name="ck_hotspot_theme_kind"),
            sa.CheckConstraint("source IN ('seed', 'admin')", name="ck_hotspot_theme_source"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("slug"),
        )
        op.create_index("ix_hotspot_themes_slug", THEMES, ["slug"])
        op.create_index("ix_hotspot_themes_is_active", THEMES, ["is_active"])
        op.create_index("ix_hotspot_themes_kind_active", THEMES, ["kind", "is_active"])
    if _offline() or LINKS not in tables:
        op.create_table(
            LINKS,
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("hotspot_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("theme_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("months_json", sa.JSON(), nullable=True),
            sa.Column("source", sa.String(length=16), nullable=False, server_default="admin"),
            sa.Column("note", sa.String(length=500), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            *_timestamps(),
            sa.ForeignKeyConstraint(["hotspot_id"], ["travel_hotspots.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["theme_id"], [f"{THEMES}.id"], ondelete="CASCADE"),
            sa.CheckConstraint(
                "source IN ('seed', 'admin', 'ai')", name="ck_hotspot_theme_link_source"
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("hotspot_id", "theme_id", name="uq_hotspot_theme_link"),
        )
        op.create_index("ix_hotspot_theme_links_hotspot_id", LINKS, ["hotspot_id"])
        op.create_index("ix_hotspot_theme_links_theme_id", LINKS, ["theme_id"])
        op.create_index("ix_hotspot_theme_links_is_active", LINKS, ["is_active"])
    if _offline() or INTROS not in tables:
        op.create_table(
            INTROS,
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("hotspot_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("locale", sa.String(length=16), nullable=False),
            sa.Column("body", sa.Text(), nullable=False),
            sa.Column(
                "review_status", sa.String(length=24), nullable=False, server_default="pending"
            ),
            sa.Column("review_reason", sa.Text(), nullable=True),
            sa.Column("source", sa.String(length=16), nullable=False, server_default="manual"),
            sa.Column("ai_provider", sa.String(length=32), nullable=True),
            sa.Column("ai_model", sa.String(length=128), nullable=True),
            sa.Column("generated_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("reviewed_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column("metadata_json", sa.JSON(), nullable=False, server_default="{}"),
            *_timestamps(),
            sa.ForeignKeyConstraint(["hotspot_id"], ["travel_hotspots.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["reviewed_by_user_id"], ["users.id"], ondelete="SET NULL"),
            sa.CheckConstraint(f"locale IN {LOCALES_SQL}", name="ck_hotspot_intro_locale"),
            sa.CheckConstraint(
                "review_status IN ('pending', 'approved', 'rejected', 'disabled')",
                name="ck_hotspot_intro_review_status",
            ),
            sa.CheckConstraint("source IN ('ai', 'manual')", name="ck_hotspot_intro_source"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("hotspot_id", "locale", name="uq_hotspot_intro_locale"),
        )
        op.create_index("ix_hotspot_intros_hotspot_id", INTROS, ["hotspot_id"])
        op.create_index("ix_hotspot_intros_locale", INTROS, ["locale"])
        op.create_index("ix_hotspot_intros_review_status", INTROS, ["review_status"])
        op.create_index("ix_hotspot_intros_source", INTROS, ["source"])
        op.create_index("ix_hotspot_intros_reviewed_by_user_id", INTROS, ["reviewed_by_user_id"])
        op.create_index("ix_hotspot_intros_status_locale", INTROS, ["review_status", "locale"])
    if _offline() or RUNS not in tables:
        op.create_table(
            RUNS,
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("actor_user_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column("hotspot_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("idempotency_key", sa.String(length=255), nullable=False),
            sa.Column("requested_locales", sa.JSON(), nullable=False, server_default="[]"),
            sa.Column("provider", sa.String(length=16), nullable=False),
            sa.Column("model", sa.String(length=128), nullable=False),
            sa.Column("force", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("status", sa.String(length=16), nullable=False, server_default="queued"),
            sa.Column("progress", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("progress_json", sa.JSON(), nullable=False, server_default="{}"),
            sa.Column("usage_json", sa.JSON(), nullable=False, server_default="{}"),
            sa.Column("result_json", sa.JSON(), nullable=False, server_default="{}"),
            sa.Column("error_code", sa.String(length=64), nullable=True),
            sa.Column("error_message", sa.Text(), nullable=True),
            sa.Column("queue_job_id", sa.String(length=128), nullable=True),
            sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
            *_timestamps(),
            sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"], ondelete="SET NULL"),
            sa.ForeignKeyConstraint(["hotspot_id"], ["travel_hotspots.id"], ondelete="CASCADE"),
            sa.CheckConstraint(
                "provider IN ('minimax', 'openai', 'anthropic', 'gemini')",
                name="ck_hotspot_intro_run_provider",
            ),
            sa.CheckConstraint(
                "status IN ('queued', 'running', 'partial', 'completed', 'failed')",
                name="ck_hotspot_intro_run_status",
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint(
                "actor_user_id", "idempotency_key", name="uq_hotspot_intro_run_idempotency"
            ),
        )
        op.create_index("ix_hotspot_intro_runs_actor_user_id", RUNS, ["actor_user_id"])
        op.create_index("ix_hotspot_intro_runs_hotspot_id", RUNS, ["hotspot_id"])
        op.create_index("ix_hotspot_intro_runs_provider", RUNS, ["provider"])
        op.create_index("ix_hotspot_intro_runs_status", RUNS, ["status"])


def downgrade() -> None:
    tables = _tables()
    for table in (RUNS, INTROS, LINKS, THEMES):
        if _offline() or table in tables:
            op.drop_table(table)
