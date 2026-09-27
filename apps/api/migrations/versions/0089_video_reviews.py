"""Videos the owner reviews on /admin/videos, and each decision the pipeline waits for.

Revision ID: 0089_video_reviews
Revises: 0088_news_needs_redraft_status

The video pipeline runs on the owner's computer; the owner asked to review drafts and finished
videos on the site instead of in chat. ``video_projects`` is what the pipeline last reported
about one video; ``video_reviews`` is one thing to decide (an outline, the narration, the final
cut, or whether to upload), bound to the SHA-256 of what was reviewed. The preview files
themselves live on the host's disk, not in the database.

0001 still calls the current ``Base.metadata.create_all``, so a fresh database already has
these tables while one upgrading from 0088 does not; the creates are guarded, as in 0086.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0089_video_reviews"
down_revision: str | None = "0088_news_needs_redraft_status"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

PROJECTS = "video_projects"
REVIEWS = "video_reviews"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _tables() -> set[str]:
    if _offline():
        return set()
    return set(sa.inspect(op.get_bind()).get_table_names())


def upgrade() -> None:
    tables = _tables()
    if _offline() or PROJECTS not in tables:
        op.create_table(
            PROJECTS,
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("slug", sa.String(length=80), nullable=False),
            sa.Column("title", sa.String(length=200), nullable=False),
            sa.Column("stage", sa.String(length=40), nullable=False),
            sa.Column("checklist", sa.JSON(), nullable=False),
            sa.Column("youtube_video_id", sa.String(length=32), nullable=True),
            sa.Column("last_synced_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_video_projects_slug", PROJECTS, ["slug"], unique=True)
    if _offline() or REVIEWS not in tables:
        op.create_table(
            REVIEWS,
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("gate", sa.String(length=20), nullable=False),
            sa.Column("content_sha256", sa.String(length=64), nullable=False),
            sa.Column("summary", sa.String(length=500), nullable=False),
            sa.Column("payload", sa.JSON(), nullable=False),
            sa.Column("files", sa.JSON(), nullable=False),
            sa.Column("status", sa.String(length=20), nullable=False),
            sa.Column("choice", sa.String(length=40), nullable=True),
            sa.Column("note", sa.Text(), nullable=True),
            sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("decided_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column("submitted_by_token_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "gate IN ('outline', 'audio', 'final', 'publish')", name="ck_video_review_gate"
            ),
            sa.CheckConstraint(
                "status IN ('pending', 'approved', 'rejected', 'superseded')",
                name="ck_video_review_status",
            ),
            sa.ForeignKeyConstraint(["project_id"], [f"{PROJECTS}.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["decided_by_user_id"], ["users.id"], ondelete="SET NULL"),
            sa.ForeignKeyConstraint(
                ["submitted_by_token_id"], ["video_tool_tokens.id"], ondelete="SET NULL"
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint(
                "project_id", "gate", "content_sha256", name="uq_video_review_content"
            ),
        )
        op.create_index("ix_video_reviews_project_id", REVIEWS, ["project_id"])


def downgrade() -> None:
    tables = _tables()
    if _offline() or REVIEWS in tables:
        op.drop_table(REVIEWS)
    if _offline() or PROJECTS in tables:
        op.drop_table(PROJECTS)
