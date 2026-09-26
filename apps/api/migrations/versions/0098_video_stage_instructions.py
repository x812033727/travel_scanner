"""The owner's standing instructions per stage, and the prompts the worker last sent.

Revision ID: 0098_video_stage_instructions
Revises: 0097_video_drama_requests

``video_automation_settings.stage_instructions`` holds, per writing stage, the text the owner
wrote on the settings tab of /admin/videos; the worker appends it to that stage's prompt on
every video. ``video_stage_prompts`` keeps, per stage and format, the instructions the worker
last sent to ``/video/automation/run``, so the owner can read the prompt as it went.

0001 builds a fresh database from the current models, so the column and the table are added
only when they are missing. The downgrade drops both: the instructions are the owner's to
retype, and the prompts are a mirror of what the worker sends anyway.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0098_video_stage_instructions"
down_revision: str | None = "0097_video_drama_requests"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SETTINGS = "video_automation_settings"
COLUMN = "stage_instructions"
TABLE = "video_stage_prompts"
STAGES = "'planner', 'writer', 'verifier', 'listener', 'translator', 'caption_reviewer'"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _tables() -> set[str]:
    return set() if _offline() else set(sa.inspect(op.get_bind()).get_table_names())


def _columns(table: str) -> set[str]:
    return (
        set() if _offline() else {c["name"] for c in sa.inspect(op.get_bind()).get_columns(table)}
    )


def upgrade() -> None:
    if COLUMN not in _columns(SETTINGS):
        op.add_column(
            SETTINGS,
            sa.Column(COLUMN, sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        )
    if TABLE not in _tables():
        op.create_table(
            TABLE,
            sa.Column("stage", sa.String(20), primary_key=True),
            sa.Column("format", sa.String(8), primary_key=True),
            sa.Column("slug", sa.String(80), nullable=False),
            sa.Column("instructions", sa.Text(), nullable=False),
            sa.Column("sent_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(f"stage IN ({STAGES})", name="ck_video_stage_prompt_stage"),
            sa.CheckConstraint(
                "format IN ('slides', 'drama')", name="ck_video_stage_prompt_format"
            ),
        )


def downgrade() -> None:
    if _offline() or TABLE in _tables():
        op.drop_table(TABLE)
    if _offline() or COLUMN in _columns(SETTINGS):
        op.drop_column(SETTINGS, COLUMN)
