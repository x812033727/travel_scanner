"""The channel's daily YouTube Reporting API reports (video_youtube_report_*).

Revision ID: 0145_video_youtube_reports
Revises: 0144_video_runpod_sessions

docs/videos/YOUTUBE-REPORTS.md. YouTube writes one CSV a day per reporting job and deletes it
after 60 days; the site keeps each file (gzipped, untouched) so a paired video tool can read the
channel's numbers from the site. Three new tables, nothing existing changes.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0145_video_youtube_reports"
down_revision: str | None = "0144_video_runpod_sessions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

JOBS = "video_youtube_report_jobs"
REPORTS = "video_youtube_reports"
STATE = "video_youtube_report_state"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _create_jobs() -> None:
    op.create_table(
        JOBS,
        sa.Column("job_id", sa.String(64), primary_key=True),
        sa.Column("channel_id", sa.String(64), nullable=False),
        sa.Column("report_type_id", sa.String(100), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expire_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_video_youtube_report_jobs_channel_id", JOBS, ["channel_id"])


def _create_reports() -> None:
    op.create_table(
        REPORTS,
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("report_id", sa.String(64), nullable=False, unique=True),
        sa.Column(
            "job_id",
            sa.String(64),
            sa.ForeignKey(f"{JOBS}.job_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("channel_id", sa.String(64), nullable=False),
        sa.Column("report_type_id", sa.String(100), nullable=False),
        sa.Column("day", sa.Date(), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("create_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("downloaded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("columns", sa.JSON(), nullable=False),
        sa.Column("row_count", sa.Integer(), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("content_gzip", sa.LargeBinary(), nullable=False),
        sa.UniqueConstraint(
            "channel_id", "report_type_id", "day", name="uq_video_youtube_reports_type_day"
        ),
        sa.CheckConstraint("row_count >= 0", name="ck_video_youtube_reports_rows"),
    )
    op.create_index("ix_video_youtube_reports_job_id", REPORTS, ["job_id"])


def _create_state() -> None:
    op.create_table(
        STATE,
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("synced_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("attempted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("problem", sa.Text(), nullable=True),
        sa.Column("chosen_types", sa.JSON(), nullable=False),
        sa.CheckConstraint("id = 1", name="ck_video_youtube_report_state_single"),
    )


def upgrade() -> None:
    if _offline():
        _create_jobs()
        _create_reports()
        _create_state()
        return
    inspector = sa.inspect(op.get_bind())
    if not inspector.has_table(JOBS):
        _create_jobs()
    if not inspector.has_table(REPORTS):
        _create_reports()
    if not inspector.has_table(STATE):
        _create_state()


def downgrade() -> None:
    if _offline():
        op.drop_table(STATE)
        op.drop_table(REPORTS)
        op.drop_table(JOBS)
        return
    inspector = sa.inspect(op.get_bind())
    for table in (STATE, REPORTS, JOBS):
        if inspector.has_table(table):
            op.drop_table(table)
