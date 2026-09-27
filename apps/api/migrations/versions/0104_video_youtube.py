"""The YouTube channel the site publishes through, and what it last sent for each video.

Revision ID: 0104_video_youtube
Revises: 0103_video_locales

After the owner uploads a cut in YouTube Studio and pastes its address on /admin/videos, the
site adds the titles and descriptions of the languages chosen, the captions and the thumbnail,
and schedules the video with the YouTube Data API (docs/videos/HANDS-OFF.md §YouTube API 第一步,
docs/videos/LANGUAGES.md). ``video_youtube_channel`` holds the one channel the owner connected:
the refresh token their consent gave, encrypted the way the provider secrets are, with the
channel's id and title for the settings tab. ``video_projects.youtube_sync`` records what the
site last sent for a video and how each step went, for the video's page.

0001 builds a fresh database from the current models, so the table and the column are added
only when missing.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0104_video_youtube"
down_revision: str | None = "0103_video_locales"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

PROJECTS = "video_projects"
CHANNEL = "video_youtube_channel"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _tables() -> set[str]:
    return set() if _offline() else set(sa.inspect(op.get_bind()).get_table_names())


def _columns(table: str) -> set[str]:
    return (
        set() if _offline() else {c["name"] for c in sa.inspect(op.get_bind()).get_columns(table)}
    )


def upgrade() -> None:
    if CHANNEL not in _tables():
        op.create_table(
            CHANNEL,
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column("channel_id", sa.String(length=64), nullable=True),
            sa.Column("channel_title", sa.String(length=200), nullable=True),
            sa.Column("refresh_token_encrypted", sa.Text(), nullable=False),
            sa.Column("scope", sa.String(length=200), nullable=False),
            sa.Column(
                "connected_by_user_id",
                sa.Uuid(),
                sa.ForeignKey("users.id", ondelete="SET NULL"),
                nullable=True,
            ),
            sa.Column("connected_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )
    if "youtube_sync" not in _columns(PROJECTS):
        op.add_column(PROJECTS, sa.Column("youtube_sync", sa.JSON(), nullable=True))


def downgrade() -> None:
    if _offline() or "youtube_sync" in _columns(PROJECTS):
        op.drop_column(PROJECTS, "youtube_sync")
    if _offline() or CHANNEL in _tables():
        op.drop_table(CHANNEL)
