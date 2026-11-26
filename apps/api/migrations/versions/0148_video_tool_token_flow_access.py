"""Allow video tool tokens to call the host Flow & Flow Music MCP gateway (flow_access).

Revision ID: 0148_video_tool_token_flow_access
Revises: 0147_video_project_shelf

Cloud sessions (Claude, Codex, Antigravity, Colab) pair via `login --flow` and receive a
video tool token (`mkv_...`) with `flow_access = true`. Every existing token stays without
it until the owner explicitly creates or approves one.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0148_video_tool_token_flow_access"
down_revision: str | None = "0147_video_project_shelf"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TOKENS = "video_tool_tokens"
COLUMN = "flow_access"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def upgrade() -> None:
    if _offline():
        op.add_column(
            TOKENS, sa.Column(COLUMN, sa.Boolean(), nullable=False, server_default=sa.false())
        )
        return
    inspector = sa.inspect(op.get_bind())
    if COLUMN not in {column["name"] for column in inspector.get_columns(TOKENS)}:
        op.add_column(
            TOKENS, sa.Column(COLUMN, sa.Boolean(), nullable=False, server_default=sa.false())
        )


def downgrade() -> None:
    if _offline():
        op.drop_column(TOKENS, COLUMN)
        return
    inspector = sa.inspect(op.get_bind())
    if COLUMN in {column["name"] for column in inspector.get_columns(TOKENS)}:
        op.drop_column(TOKENS, COLUMN)
