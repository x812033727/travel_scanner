"""The linked YouTube channel and each video's sync state (docs/videos/HANDS-OFF.md §YouTube API).

Revision ID: 0102_video_youtube_sync
Revises: 0101_video_dub_locales

``video_youtube_connections`` holds the one channel the site publishes to: the OAuth client the
owner pasted, the client secret and refresh token encrypted together, the channel the grant
speaks for and when that was last verified. A project gains ``youtube_sync`` (what the site last
sent YouTube for it, step by step) and ``youtube_upload_session`` (the resumable upload session of
its mp4, so a retry resumes rather than uploads twice).

0001 builds a fresh database from the current models, so the table is created and the columns
added only when missing. The downgrade drops them: the grant can be made again in the browser,
and the sync state only describes calls YouTube already answered.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0102_video_youtube_sync"
down_revision: str | None = "0101_video_dub_locales"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_youtube_connections"
PROJECTS = "video_projects"
PROJECT_COLUMNS: tuple[tuple[str, sa.types.TypeEngine[object]], ...] = (
    ("youtube_sync", sa.JSON()),
    ("youtube_upload_session", sa.Text()),
)


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _tables() -> set[str]:
    return set() if _offline() else set(sa.inspect(op.get_bind()).get_table_names())


def _columns(table: str) -> set[str]:
    if _offline():
        return set()
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(table)}


def upgrade() -> None:
    if TABLE not in _tables():
        op.create_table(
            TABLE,
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("client_id", sa.String(255), nullable=True),
            sa.Column("secret_config_encrypted", sa.Text(), nullable=True),
            sa.Column("channel_id", sa.String(64), nullable=True),
            sa.Column("channel_title", sa.String(200), nullable=True),
            sa.Column("scope", sa.Text(), nullable=True),
            sa.Column("linked_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column(
                "linked_by_user_id",
                sa.Uuid(),
                sa.ForeignKey(
                    "users.id", name="fk_video_youtube_connection_linked_by", ondelete="SET NULL"
                ),
                nullable=True,
            ),
            sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("problem", sa.Text(), nullable=True),
            sa.Column("audited", sa.Boolean(), nullable=False, server_default=sa.text("false")),
            sa.Column(
                "updated_by_user_id",
                sa.Uuid(),
                sa.ForeignKey(
                    "users.id", name="fk_video_youtube_connection_updated_by", ondelete="SET NULL"
                ),
                nullable=True,
            ),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint("id = 1", name="ck_video_youtube_connection_single"),
        )
    present = _columns(PROJECTS)
    for name, kind in PROJECT_COLUMNS:
        if name not in present:
            op.add_column(PROJECTS, sa.Column(name, kind, nullable=True))


def downgrade() -> None:
    present = _columns(PROJECTS)
    for name, _kind in PROJECT_COLUMNS:
        if _offline() or name in present:
            op.drop_column(PROJECTS, name)
    if _offline() or TABLE in _tables():
        op.drop_table(TABLE)
