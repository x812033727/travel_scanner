"""The owner's settings for the video pipeline running on the host.

Revision ID: 0090_video_automation_settings
Revises: 0089_video_reviews

One row (``id = 1``), like ``news_automation_settings``: the model for each writing stage, how
often a draft is made and on what topics, the voice, length and caption languages, the budgets,
and whether narration Jev passes line by line is approved without the owner
(docs/videos/AUTOMATION.md). The row is created with its defaults on first read.

0001 still calls the current ``Base.metadata.create_all``, so a fresh database already has the
table while one upgrading from 0089 does not; the create is guarded, as in 0089.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0090_video_automation_settings"
down_revision: str | None = "0089_video_reviews"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_automation_settings"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def upgrade() -> None:
    if not _offline() and TABLE in sa.inspect(op.get_bind()).get_table_names():
        return
    op.create_table(
        TABLE,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("draft_interval_hours", sa.Integer(), nullable=False),
        sa.Column("topics_per_run", sa.Integer(), nullable=False),
        sa.Column("max_waiting_drafts", sa.Integer(), nullable=False),
        sa.Column("topic_scope", sa.JSON(), nullable=False),
        sa.Column("topic_avoid", sa.JSON(), nullable=False),
        sa.Column("topic_from_site", sa.Boolean(), nullable=False),
        sa.Column("topic_from_search", sa.Boolean(), nullable=False),
        sa.Column("stage_models", sa.JSON(), nullable=False),
        sa.Column("voice", sa.JSON(), nullable=False),
        sa.Column("target_minutes_min", sa.Integer(), nullable=False),
        sa.Column("target_minutes_max", sa.Integer(), nullable=False),
        sa.Column("caption_locales", sa.JSON(), nullable=False),
        sa.Column("max_drafts_per_month", sa.Integer(), nullable=False),
        sa.Column("monthly_token_budget_millions", sa.Integer(), nullable=False),
        sa.Column("max_verify_rounds", sa.Integer(), nullable=False),
        sa.Column("max_retake_rounds", sa.Integer(), nullable=False),
        sa.Column("auto_approve_audio", sa.Boolean(), nullable=False),
        sa.Column("updated_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("id = 1", name="ck_video_automation_settings_singleton"),
        sa.CheckConstraint(
            "draft_interval_hours BETWEEN 6 AND 720", name="ck_video_automation_interval"
        ),
        sa.CheckConstraint("topics_per_run BETWEEN 1 AND 3", name="ck_video_automation_topics"),
        sa.CheckConstraint(
            "max_waiting_drafts BETWEEN 1 AND 10", name="ck_video_automation_waiting"
        ),
        sa.CheckConstraint(
            "target_minutes_min BETWEEN 3 AND 30 AND target_minutes_max BETWEEN 3 AND 30 "
            "AND target_minutes_min <= target_minutes_max",
            name="ck_video_automation_minutes",
        ),
        sa.CheckConstraint(
            "max_drafts_per_month BETWEEN 0 AND 60", name="ck_video_automation_drafts"
        ),
        sa.CheckConstraint(
            "monthly_token_budget_millions BETWEEN 1 AND 500", name="ck_video_automation_tokens"
        ),
        sa.CheckConstraint("max_verify_rounds BETWEEN 1 AND 5", name="ck_video_automation_verify"),
        sa.CheckConstraint("max_retake_rounds BETWEEN 0 AND 5", name="ck_video_automation_retakes"),
        sa.ForeignKeyConstraint(["updated_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table(TABLE)
