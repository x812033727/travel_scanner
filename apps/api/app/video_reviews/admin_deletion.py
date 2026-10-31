"""Delete a dropped video for good: its row, its reviews and its files on the site.

A drop keeps the row so the next automatic draft still sees the topic as made; this is the step
after it, for the owner clearing the catalog. What it takes and what it leaves:

- Goes: the ``video_projects`` row (languages, YouTube sync state and the backup record are its
  columns), its ``video_reviews``, its Shorts metrics, and its folders in the review and media
  stores. The owner's own material for a Shorts topic stays in the media store, as the prune
  keeps it: it cannot be generated again.
- Stays, because it is a record of what happened and not of the video: ``admin_audit_logs`` and
  every row money is summed over (``video_ai_runs``, ``video_media_jobs``, the pilot budget
  ledger, ``video_shorts_costs``, ``video_runpod_sessions``). They name the slug as text.
- Stays, closed: the request row the video started from, which the day's and month's counts and
  the redo limit read; and the episode, which belongs to the series' plan and keeps its slug for
  ``redo_episode``. A compilation's ``compilation_slug`` stays too: one compilation a series, and
  clearing it would have the worker start another.
- Not the site's to touch: YouTube (the upload stays public or private as it is), the Drive
  backup, and the worker's work directory, which the API mounts read-only. The worker marks its
  copy dropped on its next round (``Automation.bookkeeping``) and ``tidy`` clears it on the same
  terms as any dropped video.

The slug is free afterwards: a later report that does not claim to have been here before
(``ProjectIn.on_site``) registers it anew.
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User, VideoReview
from app.problems import AppError
from app.video_automation.models import (
    VideoDailyBriefRequest,
    VideoDramaRequest,
    VideoSlidesRequest,
)
from app.video_media.models import LIVE_STATUSES, VideoMediaJob
from app.video_media.storage import MediaStore
from app.video_reviews import admin_service as service
from app.video_reviews.schemas import ProjectDeletedOut
from app.video_reviews.storage import ReviewStore
from app.video_shorts import slots as shorts_slots
from app.video_shorts.models import (
    VideoShortsAsset,
    VideoShortsMetric,
    VideoShortsSlot,
    VideoShortsTopic,
)

CLOSED_NOTE = "站主刪除了這支影片"


async def _close_started_requests(session: AsyncSession, slug: str, now: datetime) -> None:
    """A started request reads as still in the making when its video has no row to say it was
    dropped: the article could not be asked for again and the worker's list would keep it."""
    for table in (VideoDramaRequest, VideoSlidesRequest):
        await session.execute(
            update(table)
            .where(table.slug == slug, table.status == "started")
            .values(status="cancelled", cancelled_at=now, updated_at=now)
        )
    await session.execute(
        update(VideoDailyBriefRequest)
        .where(VideoDailyBriefRequest.slug == slug, VideoDailyBriefRequest.status == "started")
        .values(status="cancelled", skip_reason=CLOSED_NOTE, cancelled_at=now, updated_at=now)
    )


async def _let_go_of_shorts(session: AsyncSession, slug: str, now: datetime) -> int:
    """Close what the Shorts tab holds under this slug; returns the metrics deleted.

    Topics first, the order ``_drop_empty_video`` takes the topic and the video in. A topic in
    the making closes as dropped, or the next job would have the worker start it again. A slot
    still ahead opens; one past keeps the slug as a record the way a missed one does, outside
    the unique index, so the slug can hold a slot again.
    """
    topics = await session.scalars(
        select(VideoShortsTopic).where(VideoShortsTopic.project_slug == slug).with_for_update()
    )
    for topic in topics:
        if topic.status == "making":
            topic.status = "dropped"
            topic.finished_at = now
            topic.note = CLOSED_NOTE
        topic.project_slug = None
        topic.updated_at = now
    await shorts_slots.release(session, slug, now)
    slots = await session.scalars(
        select(VideoShortsSlot)
        .where(
            VideoShortsSlot.project_slug == slug,
            VideoShortsSlot.status.in_(("scheduled", "published")),
        )
        .with_for_update()
    )
    for slot in slots:
        if slot.starts_at > now:
            shorts_slots._empty(slot, now)
        else:
            slot.status = "skipped"
            slot.updated_at = now
    metrics = await session.execute(
        delete(VideoShortsMetric).where(VideoShortsMetric.project_slug == slug)
    )
    return int(metrics.rowcount)  # type: ignore[attr-defined]


async def delete_project(
    session: AsyncSession,
    store: ReviewStore,
    media: MediaStore,
    slug: str,
    user: User,
) -> ProjectDeletedOut:
    """Delete a video the owner already dropped; anything else is refused with a 409."""
    project = await service._project(session, slug)
    if project.dropped_at is None:
        raise AppError(
            409, "video_project_not_dropped", "只有已放棄的影片能刪除：請先放棄這支影片"
        )
    now = datetime.now(UTC)
    metrics_deleted = await _let_go_of_shorts(session, slug, now)
    # Dropped before the drop learned to close them (PR #1023), the episode and its request may
    # still be open. Idempotent: an episode already skipped or done is left as it is.
    await service._skip_abandoned_episode(session, project, user, now)
    await _close_started_requests(session, slug, now)
    # Expired as the prune expires a finished video's, so a queued one is not sent to the vendor.
    # The rows stay: the month's spend is summed over them.
    await session.execute(
        update(VideoMediaJob)
        .where(VideoMediaJob.slug == slug, VideoMediaJob.status.in_(LIVE_STATUSES))
        .values(status="expired", updated_at=now)
    )
    # Locked last, the series, the episode and the topic being what the other paths lock first.
    project = await service._project(session, slug, lock=True)
    if project.dropped_at is None:
        raise AppError(
            409, "video_project_not_dropped", "只有已放棄的影片能刪除：請先放棄這支影片"
        )
    reviews = await session.scalar(
        select(func.count()).select_from(VideoReview).where(VideoReview.project_id == project.id)
    )
    # What the row said, since the audit record is all that will say it from here on.
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="video_project_deleted",
            target=f"video_project:{project.id}",
            metadata_json={
                "slug": slug,
                "title": project.title,
                "format": project.format,
                "category": project.category,
                "source_guide": project.source_guide,
                "series_slug": project.series_slug,
                "episode_number": project.episode_number,
                "shorts_line": project.shorts_line,
                "youtube_video_id": project.youtube_video_id,
                "dropped_at": project.dropped_at.isoformat(),
                "dropped_note": project.dropped_note,
                "reviews_deleted": reviews or 0,
                "metrics_deleted": metrics_deleted,
            },
        )
    )
    youtube_video_id = project.youtube_video_id
    # The foreign key cascades on PostgreSQL; spelled out so the count above is what went.
    await session.execute(delete(VideoReview).where(VideoReview.project_id == project.id))
    await session.delete(project)
    owned = await session.scalar(
        select(VideoShortsAsset.id).where(VideoShortsAsset.topic_slug == slug).limit(1)
    )
    await session.commit()
    # After the commit, as drop_project lets go of its previews: a failed commit leaves a video
    # whose files are all there.
    store.delete_project(slug)
    if owned is None:
        media.delete_project(slug)
    return ProjectDeletedOut(
        slug=slug,
        youtube_video_id=youtube_video_id,
        reviews_deleted=reviews or 0,
        metrics_deleted=metrics_deleted,
    )
