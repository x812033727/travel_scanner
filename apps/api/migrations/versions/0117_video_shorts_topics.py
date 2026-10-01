"""Shorts phase two: the topic library, the owner's material, the weekly reports.

Revision ID: 0117_video_shorts_topics
Revises: 0116_video_project_category

The host worker starts making Shorts by itself (docs/videos/SHORTS.md §排片與時段, ticket
video-shorts-automation-api). Three tables are new: ``video_shorts_topics`` (what is still to
be made, with its whole spec, since the worker cannot read the campaign in the repository),
``video_shorts_assets`` (the photos and sketches only the owner can supply, with who made
them and on what terms) and ``video_shorts_reports`` (one report a week, citing the numbers
YouTube reported as they were stored). ``video_shorts_settings`` gains the month's cap on
Shorts the worker starts and when it last planned a week and wrote topics.

``video_stage_prompts`` keeps the prompt each stage was last sent; a Short's stages are kept
under their own format, and the experiment's subject is a stage of its own, so
``ck_video_stage_prompt_format`` takes ``shorts`` and ``ck_video_stage_prompt_stage`` takes
``subject``. Both are rebuilt under their names with every value they took before, as 0109
rebuilt the format check of ``video_projects``.

0001 builds a fresh database from the current models, and those do not include the video
tables, so CI runs every branch here. The new tables and columns are added only when missing.
The downgrade removes the prompts kept under the new values before the narrow checks return:
they are a mirror of what the worker sends, as 0098 says.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0117_video_shorts_topics"
down_revision: str | None = "0116_video_project_category"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SETTINGS = "video_shorts_settings"
TOPICS = "video_shorts_topics"
ASSETS = "video_shorts_assets"
REPORTS = "video_shorts_reports"
PROMPTS = "video_stage_prompts"
STAGE_CHECK = "ck_video_stage_prompt_stage"
FORMAT_CHECK = "ck_video_stage_prompt_format"
OLD_STAGES = "'planner', 'writer', 'verifier', 'listener', 'translator', 'caption_reviewer'"
NEW_STAGES = f"{OLD_STAGES}, 'subject'"
OLD_FORMATS = "'slides', 'drama'"
NEW_FORMATS = "'slides', 'drama', 'shorts'"
MONTH_CHECK = ("ck_video_shorts_settings_month", "max_per_month BETWEEN 0 AND 400")
SETTINGS_COLUMNS: tuple[tuple[str, sa.types.TypeEngine[object], str | None], ...] = (
    ("max_per_month", sa.Integer(), "60"),
    ("last_plan_at", sa.DateTime(timezone=True), None),
    ("last_brief_at", sa.DateTime(timezone=True), None),
)


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _tables() -> set[str]:
    return set() if _offline() else set(sa.inspect(op.get_bind()).get_table_names())


def _columns(table: str) -> set[str]:
    if _offline():
        return set()
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(table)}


def _checks(table: str) -> set[str]:
    if _offline():
        return set()
    return {
        str(check.get("name")) for check in sa.inspect(op.get_bind()).get_check_constraints(table)
    }


def _user(column: str, name: str) -> sa.Column[object]:
    return sa.Column(
        column,
        sa.Uuid(),
        sa.ForeignKey("users.id", name=name, ondelete="SET NULL"),
        nullable=True,
    )


def _create_topics() -> None:
    op.create_table(
        TOPICS,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("slug", sa.String(80), nullable=False),
        sa.Column("line", sa.String(8), nullable=False),
        sa.Column("series", sa.String(40), nullable=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("hook", sa.Text(), nullable=True),
        sa.Column("status", sa.String(12), nullable=False),
        sa.Column("brief", sa.JSON(), nullable=False),
        sa.Column("source_slug", sa.String(80), nullable=True),
        sa.Column("origin", sa.String(12), nullable=False),
        sa.Column("release_order", sa.Integer(), nullable=True),
        sa.Column("assets_needed", sa.JSON(), nullable=False),
        sa.Column("dedupe_key", sa.String(160), nullable=True),
        sa.Column("project_slug", sa.String(80), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        _user("created_by_user_id", "fk_video_shorts_topics_created_user"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("slug", name="uq_video_shorts_topic_slug"),
        sa.UniqueConstraint("dedupe_key", name="uq_video_shorts_topic_dedupe"),
        sa.CheckConstraint(
            "status IN ('idea', 'ready', 'needs_assets', 'making', 'made', 'dropped')",
            name="ck_video_shorts_topic_status",
        ),
        sa.CheckConstraint(
            "origin IN ('campaign', 'planner', 'owner', 'auto')",
            name="ck_video_shorts_topic_origin",
        ),
        sa.CheckConstraint("line IN ('lab', 'cut', 'drama')", name="ck_video_shorts_topic_line"),
    )


def _create_assets() -> None:
    op.create_table(
        ASSETS,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("topic_slug", sa.String(80), nullable=False),
        sa.Column("need", sa.String(40), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("filename", sa.String(200), nullable=False),
        sa.Column("content_type", sa.String(40), nullable=False),
        sa.Column("size", sa.BigInteger(), nullable=False),
        sa.Column("author", sa.String(120), nullable=False),
        sa.Column("taken_on", sa.Date(), nullable=True),
        sa.Column("rights_note", sa.Text(), nullable=False),
        _user("uploaded_by_user_id", "fk_video_shorts_assets_uploaded_user"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("topic_slug", "sha256", name="uq_video_shorts_asset_file"),
    )
    op.create_index("ix_video_shorts_assets_topic_slug", ASSETS, ["topic_slug"])


def _create_reports() -> None:
    op.create_table(
        REPORTS,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("week_start", sa.Date(), nullable=False),
        sa.Column("body_md", sa.Text(), nullable=False),
        sa.Column("rows", sa.JSON(), nullable=False),
        sa.Column("plan", sa.JSON(), nullable=False),
        sa.Column("provider", sa.String(40), nullable=True),
        sa.Column("model", sa.String(128), nullable=True),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("week_start", name="uq_video_shorts_report_week"),
    )


def _rebuild(name: str, sql: str, checks: set[str]) -> None:
    if _offline() or name in checks:
        op.drop_constraint(name, PROMPTS, type_="check")
    op.create_check_constraint(name, PROMPTS, sql)


def upgrade() -> None:
    tables = _tables()
    for table, create in (
        (TOPICS, _create_topics),
        (ASSETS, _create_assets),
        (REPORTS, _create_reports),
    ):
        if _offline() or table not in tables:
            create()
    existing = _columns(SETTINGS)
    for name, kind, default in SETTINGS_COLUMNS:
        if _offline() or name not in existing:
            op.add_column(
                SETTINGS,
                sa.Column(
                    name,
                    kind,
                    nullable=default is None,
                    server_default=sa.text(default) if default is not None else None,
                ),
            )
    if _offline() or MONTH_CHECK[0] not in _checks(SETTINGS):
        op.create_check_constraint(MONTH_CHECK[0], SETTINGS, MONTH_CHECK[1])
    checks = _checks(PROMPTS)
    _rebuild(STAGE_CHECK, f"stage IN ({NEW_STAGES})", checks)
    _rebuild(FORMAT_CHECK, f"format IN ({NEW_FORMATS})", checks)


def downgrade() -> None:
    op.execute(sa.text(f"DELETE FROM {PROMPTS} WHERE stage = 'subject' OR format = 'shorts'"))
    checks = _checks(PROMPTS)
    _rebuild(STAGE_CHECK, f"stage IN ({OLD_STAGES})", checks)
    _rebuild(FORMAT_CHECK, f"format IN ({OLD_FORMATS})", checks)
    if _offline() or MONTH_CHECK[0] in _checks(SETTINGS):
        op.drop_constraint(MONTH_CHECK[0], SETTINGS, type_="check")
    existing = _columns(SETTINGS)
    for name, _kind, _default in reversed(SETTINGS_COLUMNS):
        if _offline() or name in existing:
            op.drop_column(SETTINGS, name)
    tables = _tables()
    for table in (REPORTS, ASSETS, TOPICS):
        if _offline() or table in tables:
            op.drop_table(table)
