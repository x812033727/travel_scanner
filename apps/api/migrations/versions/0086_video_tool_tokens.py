"""Tokens the local video pipeline uses to have this server synthesize narration.

Revision ID: 0086_video_tool_tokens
Revises: 0085_news_asset_inline_content

The pipeline in tools/video runs on the site owner's computer, while the Azure Speech key
stays in the encrypted provider settings here. A token lets that one tool call
POST /api/v1/video/speech and nothing else; only its SHA-256 is stored, the owner sees it
once when it is made, and revoking it is a timestamp rather than a delete so the audit
trail keeps what existed.

0001 still calls the current ``Base.metadata.create_all``, so a fresh database already has
this table while one upgrading from 0085 does not; the create is guarded, as in 0053.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0086_video_tool_tokens"
down_revision: str | None = "0085_news_asset_inline_content"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_tool_tokens"


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
            sa.Column("name", sa.String(length=80), nullable=False),
            sa.Column("token_hash", sa.String(length=64), nullable=False),
            sa.Column("token_prefix", sa.String(length=16), nullable=False),
            sa.Column("created_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], ondelete="SET NULL"),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_video_tool_tokens_token_hash", TABLE, ["token_hash"], unique=True)
        op.create_index("ix_video_tool_tokens_created_by_user_id", TABLE, ["created_by_user_id"])


def downgrade() -> None:
    if _offline() or TABLE in _tables():
        op.drop_table(TABLE)
