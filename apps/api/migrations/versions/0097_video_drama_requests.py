"""The owner's drama requests, and which format each video is (docs/videos/DRAMA.md).

Revision ID: 0097_video_drama_requests
Revises: 0096_video_media_jobs

``video_drama_requests`` is what the owner files on /admin/videos to have an episode made next,
ahead of the scheduled drafts; the worker claims the oldest queued row and links it to the
video it makes. ``video_projects.format`` says whether a video is a slides video or a drama,
so the list can show the drama's media spend beside it.

0001 builds a fresh database from the current models, so the table and the column are added
only when they are missing. The downgrade drops both; a request is a note to the worker, not
a record the site needs to keep.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0097_video_drama_requests"
down_revision: str | None = "0096_video_media_jobs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_drama_requests"
PROJECTS = "video_projects"
FORMAT_CHECK = "ck_video_project_format"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _tables() -> set[str]:
    return set() if _offline() else set(sa.inspect(op.get_bind()).get_table_names())


def _columns(table: str) -> set[str]:
    return (
        set() if _offline() else {c["name"] for c in sa.inspect(op.get_bind()).get_columns(table)}
    )


def _checks(table: str) -> set[str]:
    if _offline():
        return set()
    return {
        str(check.get("name")) for check in sa.inspect(op.get_bind()).get_check_constraints(table)
    }


def upgrade() -> None:
    if TABLE not in _tables():
        op.create_table(
            TABLE,
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column("premise", sa.Text(), nullable=False),
            sa.Column("title", sa.String(200), nullable=True),
            sa.Column("source_guide", sa.String(120), nullable=True),
            sa.Column("style_preset", sa.String(16), nullable=False),
            sa.Column("target_minutes", sa.Integer(), nullable=False),
            sa.Column("note", sa.Text(), nullable=True),
            sa.Column("status", sa.String(12), nullable=False),
            sa.Column("slug", sa.String(80), nullable=True),
            sa.Column(
                "created_by_user_id",
                sa.Uuid(),
                sa.ForeignKey("users.id", name="fk_video_drama_requests_user", ondelete="SET NULL"),
                nullable=True,
            ),
            sa.Column(
                "started_by_token_id",
                sa.Uuid(),
                sa.ForeignKey(
                    "video_tool_tokens.id",
                    name="fk_video_drama_requests_token",
                    ondelete="SET NULL",
                ),
                nullable=True,
            ),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
            sa.UniqueConstraint("slug", name="uq_video_drama_requests_slug"),
            sa.CheckConstraint(
                "status IN ('queued', 'started', 'done', 'cancelled')",
                name="ck_video_drama_request_status",
            ),
            sa.CheckConstraint(
                "style_preset IN ('cinematic-3d', 'anime-2d', 'ink-wash', 'custom')",
                name="ck_video_drama_request_style",
            ),
        )
        op.create_index("ix_video_drama_requests_status_created", TABLE, ["status", "created_at"])
    if "format" not in _columns(PROJECTS):
        op.add_column(
            PROJECTS,
            sa.Column("format", sa.String(8), nullable=False, server_default="slides"),
        )
    if FORMAT_CHECK not in _checks(PROJECTS):
        op.create_check_constraint(FORMAT_CHECK, PROJECTS, "format IN ('slides', 'drama')")


def downgrade() -> None:
    if _offline() or FORMAT_CHECK in _checks(PROJECTS):
        op.drop_constraint(FORMAT_CHECK, PROJECTS, type_="check")
    if _offline() or "format" in _columns(PROJECTS):
        op.drop_column(PROJECTS, "format")
    if _offline() or TABLE in _tables():
        op.drop_index("ix_video_drama_requests_status_created", table_name=TABLE)
        op.drop_table(TABLE)
