"""The owner's requests for a slides video of a chosen site article (docs/videos/AUTOMATION.md).

The scheduled drafts pick their own topics; a request is the owner saying "make a video of this
article next". It names one published zh-TW lifestyle article. The worker asks for the oldest
queued request before any scheduled draft, plans the video from that article, and claims the
request under the video's slug once the plan holds. The request is done once its video is on
YouTube (the worker says so, or the project row shows it), and reads as dropped once the owner
dropped that video, which frees the article to be asked for again. Only a queued request can be
cancelled: a started one is a video, dropped on /admin/videos like any other.

The rows live in their own table, not in ``video_drama_requests`` (migration 0126 says why).
The router turns ``RequestRefused`` into the API's problem response; nothing here raises
``AppError``.
"""

from __future__ import annotations

from datetime import UTC, datetime
from hashlib import sha256
from uuid import UUID, uuid4

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User, VideoProject, VideoToolToken
from app.video_automation import topics
from app.video_automation.models import VideoSlidesRequest
from app.video_automation.requests import RequestRefused
from app.video_automation.schemas import SlidesRequestIn, SlidesRequestOut

LIST_LIMIT = 100


def request_view(
    row: VideoSlidesRequest,
    youtube_video_id: str | None = None,
    dropped_at: datetime | None = None,
) -> SlidesRequestOut:
    """The request as the page and the worker see it: started and on YouTube counts as done,
    started and dropped by the owner as dropped."""
    status = row.status
    if row.status == "started" and youtube_video_id:
        status = "done"
    elif row.status == "started" and dropped_at is not None:
        status = "dropped"
    return SlidesRequestOut(
        id=row.id,
        source_guide=row.source_guide,
        title=row.title,
        url=f"{topics.SITE_URL}/{row.source_guide}",
        note=row.note,
        status=status,
        slug=row.slug,
        created_by_user_id=row.created_by_user_id,
        created_at=row.created_at,
        started_at=row.started_at,
        finished_at=row.finished_at,
        cancelled_at=row.cancelled_at,
    )


def _now() -> datetime:
    return datetime.now(UTC)


async def list_requests(session: AsyncSession) -> list[SlidesRequestOut]:
    """Every request, newest first, with what became of the video each one started."""
    rows = await session.execute(
        select(VideoSlidesRequest, VideoProject.youtube_video_id, VideoProject.dropped_at)
        .outerjoin(VideoProject, VideoProject.slug == VideoSlidesRequest.slug)
        .order_by(VideoSlidesRequest.created_at.desc())
        .limit(LIST_LIMIT)
    )
    return [request_view(row, youtube, dropped) for row, youtube, dropped in rows.all()]


async def next_request(session: AsyncSession) -> SlidesRequestOut | None:
    """The oldest queued request whose article the site still serves, which the worker should
    start before any scheduled draft. One whose article was unpublished since stays queued
    without holding up the ones behind it."""
    row = await session.scalar(
        select(VideoSlidesRequest)
        .where(
            VideoSlidesRequest.status == "queued",
            VideoSlidesRequest.source_guide.in_(topics.published_life_slugs()),
        )
        .order_by(VideoSlidesRequest.created_at.asc())
        .limit(1)
    )
    return request_view(row) if row is not None else None


async def create_request(
    session: AsyncSession, actor: User, payload: SlidesRequestIn
) -> SlidesRequestOut:
    """The owner's form: a published lifestyle article no queued or live request names and no
    live slides video already retells. A dropped video frees its article again."""
    slug = payload.source_guide
    article = await topics.site_article(session, slug)
    if article is None:
        raise RequestRefused(
            422,
            "video_slides_request_article_not_found",
            f"{slug} 不是已發布的繁中生活文章：只有站上看得到的生活文章能做成影片",
        )
    # Two forms filed for one article at once (a double submit, two tabs) would both pass the
    # checks below before either inserts; the transaction-scoped lock makes the second wait and
    # then find the first.
    lock_key = int.from_bytes(
        sha256(f"video-slides-request:{slug}".encode()).digest()[:8], signed=True
    )
    await session.execute(select(func.pg_advisory_xact_lock(lock_key)))
    duplicate = await session.scalar(
        select(VideoSlidesRequest.id)
        .outerjoin(VideoProject, VideoProject.slug == VideoSlidesRequest.slug)
        .where(
            VideoSlidesRequest.source_guide == slug,
            or_(
                VideoSlidesRequest.status == "queued",
                and_(VideoSlidesRequest.status == "started", VideoProject.dropped_at.is_(None)),
            ),
        )
        .limit(1)
    )
    if duplicate is not None:
        raise RequestRefused(
            409, "video_slides_request_duplicate", f"{slug} 已經在排隊，或工人正在做這篇的影片"
        )
    used = await session.scalar(
        select(VideoProject.slug)
        .where(
            VideoProject.format == "slides",
            VideoProject.source_guide == slug,
            VideoProject.dropped_at.is_(None),
        )
        .limit(1)
    )
    if used is not None:
        raise RequestRefused(
            409,
            "video_slides_request_article_used",
            f"影片 {used} 已經在講 {slug} 這篇；要重做就先到影片清單放棄那支",
        )
    now = _now()
    row = VideoSlidesRequest(
        id=uuid4(),
        source_guide=slug,
        title=article.title or None,
        note=payload.note,
        status="queued",
        created_by_user_id=actor.id,
        created_at=now,
        updated_at=now,
    )
    session.add(row)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_slides_request_created",
            target=f"video-slides-request:{row.id}",
            metadata_json={"source_guide": slug},
        )
    )
    await session.commit()
    return request_view(row)


async def _request(session: AsyncSession, request_id: UUID) -> VideoSlidesRequest:
    # Locked: two workers, or the owner and the worker, may act on one request at once.
    row = await session.scalar(
        select(VideoSlidesRequest).where(VideoSlidesRequest.id == request_id).with_for_update()
    )
    if row is None:
        raise RequestRefused(404, "video_slides_request_not_found", "找不到這個教學影片請求")
    return row


async def cancel_request(session: AsyncSession, actor: User, request_id: UUID) -> SlidesRequestOut:
    row = await _request(session, request_id)
    if row.status != "queued":
        raise RequestRefused(
            409,
            "video_slides_request_not_queued",
            "工人已經開始做這支了；要停就到影片清單放棄那支影片",
        )
    now = _now()
    row.status = "cancelled"
    row.cancelled_at = now
    row.updated_at = now
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_slides_request_cancelled",
            target=f"video-slides-request:{row.id}",
            metadata_json={"source_guide": row.source_guide},
        )
    )
    await session.commit()
    return request_view(row)


async def start_request(
    session: AsyncSession, token: VideoToolToken, request_id: UUID, slug: str
) -> SlidesRequestOut:
    """The worker claims a queued request for the video it has just planned. The same claim sent
    again is answered as the first was: client.mjs sends it again after a lost connection or a
    5xx, and a refusal there would throw away a plan whose claim had in fact gone through."""
    row = await _request(session, request_id)
    if row.status == "started" and row.slug == slug and row.started_by_token_id == token.id:
        return request_view(row)
    if row.status != "queued":
        raise RequestRefused(409, "video_slides_request_not_queued", "這個請求不在排隊中，不能開始")
    taken = await session.scalar(
        select(VideoSlidesRequest.id).where(
            VideoSlidesRequest.slug == slug, VideoSlidesRequest.id != row.id
        )
    )
    if taken is not None:
        raise RequestRefused(
            409, "video_slides_request_slug_taken", f"{slug} 已經是另一個請求的影片"
        )
    now = _now()
    row.status = "started"
    row.slug = slug
    row.started_at = now
    row.updated_at = now
    row.started_by_token_id = token.id
    await session.commit()
    return request_view(row)


async def finish_request(session: AsyncSession, request_id: UUID) -> SlidesRequestOut:
    """The worker reports the video is done (on YouTube, or the owner published it)."""
    row = await _request(session, request_id)
    if row.status != "started":
        raise RequestRefused(
            409, "video_slides_request_not_started", "這個請求還沒開始做，不能標成完成"
        )
    now = _now()
    row.status = "done"
    row.finished_at = now
    row.updated_at = now
    await session.commit()
    return request_view(row)
