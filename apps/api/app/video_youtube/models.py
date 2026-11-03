"""The channel's daily YouTube Reporting API reports, kept as YouTube gave them (migration 0145).

docs/videos/YOUTUBE-REPORTS.md. YouTube makes one CSV file a day for every report job a channel
has, and deletes it 60 days later, so the site downloads each one and keeps it here: a video
tool (a paired AI session) reads the rows from the site instead of from Google, and the rows
outlive Google's 60 days. One row per report type and Pacific day: when YouTube regenerates a
day (a backfill or a correction) the newer file replaces the older one, which is what the API
guide asks for. The CSV is kept gzipped and untouched, header included, so nothing here sums,
averages or rates YouTube's numbers.

Everything here goes when the channel is unlinked (connection.unlink).
"""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from sqlalchemy import (
    JSON,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


class VideoYoutubeReportJob(Base):
    """A reporting job the channel has on YouTube, one per report type the site reads. Google
    names the job; ``created_at`` is Google's createTime, from which it backfills 30 days."""

    __tablename__ = "video_youtube_report_jobs"
    job_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    channel_id: Mapped[str] = mapped_column(String(64), index=True)
    report_type_id: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Set by YouTube when the report type is deprecated or the job's reports go undownloaded.
    expire_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class VideoYoutubeReport(Base):
    """One day of one report type: the CSV YouTube generated, gzipped."""

    __tablename__ = "video_youtube_reports"
    __table_args__ = (
        UniqueConstraint(
            "channel_id", "report_type_id", "day", name="uq_video_youtube_reports_type_day"
        ),
        CheckConstraint("row_count >= 0", name="ck_video_youtube_reports_rows"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Google's report id; a regenerated day has a new one.
    report_id: Mapped[str] = mapped_column(String(64), unique=True)
    job_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("video_youtube_report_jobs.job_id", ondelete="CASCADE"), index=True
    )
    channel_id: Mapped[str] = mapped_column(String(64))
    report_type_id: Mapped[str] = mapped_column(String(100))
    # The Pacific-time day the report covers (startTime is Pacific midnight).
    day: Mapped[date] = mapped_column(Date)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    # When YouTube generated this file; of two files for one day the newer is the one to keep.
    create_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    downloaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    columns: Mapped[list[str]] = mapped_column(JSON, default=list)
    row_count: Mapped[int] = mapped_column(Integer, default=0)
    # The CSV's size before gzip, and the gzipped file itself.
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    content_gzip: Mapped[bytes] = mapped_column(LargeBinary)


class VideoYoutubeReportState(Base):
    """When the reports were last fetched, and why the last attempt stopped. A single row."""

    __tablename__ = "video_youtube_report_state"
    __table_args__ = (CheckConstraint("id = 1", name="ck_video_youtube_report_state_single"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    # The last run that went through every job (a run that stopped early leaves it).
    synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    attempted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    problem: Mapped[str | None] = mapped_column(Text, nullable=True)
    # The report type chosen for each family at the last run, e.g. channel_basic -> _a3.
    chosen_types: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
