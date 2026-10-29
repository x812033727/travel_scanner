"""The daily AI and tech news brief: one request a day, and its four settings.

Revision ID: 0143_video_daily_briefs
Revises: 0142_video_tool_token_colab

``video_daily_brief_requests`` holds one row per news day: once the Asia/Taipei hour in
``daily_brief_hour`` comes, the server files the previous day's published ai-news and tech-news
articles as a request (or as skipped, with too few of them), and the host worker makes the
video under the row's slug, daily-ai-YYYYMMDD
(.agents/skills/youtube-video/references/daily-brief.md). A table of its own, like the slides
requests (0127): a deployed worker asking for the next slides request must not be handed a day.

The settings row gains the switch (off), the hour (9), the least number of stories a day needs
(5) and the languages a brief's video is given without the owner (all eight, each with its
title and description, captions and dub). Every new column has a server default, so the
previous release reads and writes the row as before. 0001 builds a fresh database from the
current models, so the table and the columns are added only when missing. The downgrade drops
them; a request is a note to the worker, not a record the site needs to keep.
"""

import json
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0143_video_daily_briefs"
down_revision: str | None = "0142_video_tool_token_colab"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_daily_brief_requests"
INDEX = "ix_video_daily_brief_requests_status_date"
STATUS_CHECK = "status IN ('queued', 'started', 'done', 'skipped', 'cancelled')"
SETTINGS = "video_automation_settings"
SETTINGS_CHECK_NAME = "ck_video_daily_brief"
SETTINGS_CHECK = "daily_brief_hour BETWEEN 0 AND 23 AND daily_brief_min_stories BETWEEN 1 AND 20"
# models.DEFAULT_DAILY_BRIEF_LOCALES as it stands today, written out: the model may change later.
LOCALES = ("en", "ja", "ko", "es", "pt", "id", "vi", "th")
DEFAULT_LOCALES = json.dumps(
    {locale: {"metadata": True, "captions": True, "dub": True} for locale in LOCALES},
    ensure_ascii=True,
)


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _settings_columns() -> list[sa.Column[object]]:
    """Fresh columns each call: a Column belongs to one table once added."""
    return [
        sa.Column(
            "daily_brief_enabled", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column("daily_brief_hour", sa.Integer(), nullable=False, server_default="9"),
        sa.Column("daily_brief_min_stories", sa.Integer(), nullable=False, server_default="5"),
        sa.Column(
            "daily_brief_locales",
            sa.JSON(),
            nullable=False,
            server_default=sa.text(f"'{DEFAULT_LOCALES}'"),
        ),
    ]


def _create_table() -> None:
    op.create_table(
        TABLE,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("news_date", sa.Date(), nullable=False),
        sa.Column("slug", sa.String(80), nullable=False),
        sa.Column("source_guides", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(12), nullable=False),
        sa.Column("skip_reason", sa.Text(), nullable=True),
        sa.Column(
            "started_by_token_id",
            sa.Uuid(),
            sa.ForeignKey(
                "video_tool_tokens.id",
                name="fk_video_daily_brief_requests_token",
                ondelete="SET NULL",
            ),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("news_date", name="uq_video_daily_brief_requests_news_date"),
        sa.UniqueConstraint("slug", name="uq_video_daily_brief_requests_slug"),
        sa.CheckConstraint(STATUS_CHECK, name="ck_video_daily_brief_request_status"),
    )
    op.create_index(INDEX, TABLE, ["status", "news_date"])


def upgrade() -> None:
    if _offline():
        _create_table()
        for column in _settings_columns():
            op.add_column(SETTINGS, column)
        op.create_check_constraint(SETTINGS_CHECK_NAME, SETTINGS, SETTINGS_CHECK)
        return
    inspector = sa.inspect(op.get_bind())
    if TABLE not in inspector.get_table_names():
        _create_table()
    columns = {column["name"] for column in inspector.get_columns(SETTINGS)}
    for column in _settings_columns():
        if column.name not in columns:
            op.add_column(SETTINGS, column)
    checks = {check["name"] for check in inspector.get_check_constraints(SETTINGS)}
    if SETTINGS_CHECK_NAME not in checks:
        op.create_check_constraint(SETTINGS_CHECK_NAME, SETTINGS, SETTINGS_CHECK)


def downgrade() -> None:
    if _offline():
        op.drop_constraint(SETTINGS_CHECK_NAME, SETTINGS, type_="check")
        for column in reversed(_settings_columns()):
            op.drop_column(SETTINGS, column.name)
        op.drop_index(INDEX, table_name=TABLE)
        op.drop_table(TABLE)
        return
    inspector = sa.inspect(op.get_bind())
    checks = {check["name"] for check in inspector.get_check_constraints(SETTINGS)}
    if SETTINGS_CHECK_NAME in checks:
        op.drop_constraint(SETTINGS_CHECK_NAME, SETTINGS, type_="check")
    columns = {column["name"] for column in inspector.get_columns(SETTINGS)}
    for column in reversed(_settings_columns()):
        if column.name in columns:
            op.drop_column(SETTINGS, column.name)
    if TABLE in inspector.get_table_names():
        op.drop_index(INDEX, table_name=TABLE)
        op.drop_table(TABLE)
