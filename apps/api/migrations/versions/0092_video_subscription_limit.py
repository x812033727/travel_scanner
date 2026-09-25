"""Video writing stages on the Claude subscription accounts, and the usage cap they stop at.

Revision ID: 0092_video_subscription_limit
Revises: 0091_video_ai_runs

The owner chose on 2026-09-25 to run the automated writing on the Claude subscriptions the host
signs in (ai_accounts_agent.runs) rather than the API keys. ``subscription_max_usage_percent`` is
the share of an account's 5-hour or weekly window above which it is skipped. A settings row no
one has saved yet still holds the API-key defaults 0090 wrote, so it takes the new ones; a row
the owner saved keeps what they chose.

0001 builds a fresh database from the current models, so the column is added only when missing.
"""

import json
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0092_video_subscription_limit"
down_revision: str | None = "0091_video_ai_runs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_automation_settings"
COLUMN = "subscription_max_usage_percent"
SUBSCRIPTION_DEFAULTS = {
    "planner": {"provider": "claude_code", "model": "claude-sonnet-5"},
    "writer": {"provider": "claude_code", "model": "claude-sonnet-5"},
    "verifier": {"provider": "claude_code", "model": "claude-opus-5-5"},
    "listener": {"provider": "claude_code", "model": "claude-opus-5-5"},
    "translator": {"provider": "claude_code", "model": "claude-sonnet-5"},
    "caption_reviewer": {"provider": "claude_code", "model": "claude-opus-5-5"},
}


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def upgrade() -> None:
    columns = (
        set()
        if _offline()
        else {column["name"] for column in sa.inspect(op.get_bind()).get_columns(TABLE)}
    )
    if _offline() or COLUMN not in columns:
        op.add_column(
            TABLE, sa.Column(COLUMN, sa.Integer(), nullable=False, server_default=sa.text("80"))
        )
        op.create_check_constraint(
            "ck_video_automation_subscription_cap", TABLE, f"{COLUMN} BETWEEN 10 AND 100"
        )
    settings = sa.table(
        TABLE,
        sa.column("stage_models", sa.JSON()),
        sa.column("updated_by_user_id", sa.Uuid()),
    )
    op.execute(
        settings.update()
        .where(settings.c.updated_by_user_id.is_(None))
        .values(stage_models=sa.cast(json.dumps(SUBSCRIPTION_DEFAULTS), sa.JSON()))
    )


def downgrade() -> None:
    op.drop_constraint("ck_video_automation_subscription_cap", TABLE, type_="check")
    op.drop_column(TABLE, COLUMN)
