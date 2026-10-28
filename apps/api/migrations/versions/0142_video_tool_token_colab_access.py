"""A video tool token may also fetch a Colab account's credentials (colab_access).

Revision ID: 0142_video_tool_token_colab
Revises: 0141_story_remake_budgets

A video tool token authorized exactly one thing, synthesizing narration. A cloud session that
generates MiniMax H3 video on Google Colab needs the Colab CLI's OAuth token of an account the
owner signed in on /admin/ai-accounts, and the token is the credential such a session already
holds. The flag says which tokens may ask for it: set when a pairing asked for Colab and the
owner allowed it, or by the owner on the admin card; every existing token stays narration-only.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0142_video_tool_token_colab"
down_revision: str | None = "0141_story_remake_budgets"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_tool_tokens"
COLUMN = "colab_access"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def upgrade() -> None:
    if _offline():
        op.add_column(
            TABLE,
            sa.Column(COLUMN, sa.Boolean(), nullable=False, server_default=sa.false()),
        )
        return
    bind = op.get_bind()
    columns = {column["name"] for column in sa.inspect(bind).get_columns(TABLE)}
    if COLUMN not in columns:
        op.add_column(
            TABLE,
            sa.Column(COLUMN, sa.Boolean(), nullable=False, server_default=sa.false()),
        )


def downgrade() -> None:
    if _offline():
        op.drop_column(TABLE, COLUMN)
        return
    bind = op.get_bind()
    columns = {column["name"] for column in sa.inspect(bind).get_columns(TABLE)}
    if COLUMN in columns:
        op.drop_column(TABLE, COLUMN)
