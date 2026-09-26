"""The owner's drama requests: filed on /admin/videos, claimed by the worker (docs/videos/DRAMA.md).

The scheduled drafts pick their own topics; a request is the owner saying "make this one
next". The worker asks for the oldest queued request before it considers a scheduled draft,
starts it under the slug it chose, and the request is done once that video is on YouTube
(the worker says so, or the project row shows it). Only a queued request can be cancelled:
a started one is a video, dropped on /admin/videos like any other.

The router turns ``RequestRefused`` into the API's problem response; nothing here raises
``AppError``.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User, VideoProject, VideoToolToken
from app.video_automation.models import VideoDramaRequest
from app.video_automation.schemas import DramaRequestIn, DramaRequestOut

ACTIVE = ("queued", "started")
LIST_LIMIT = 100


class RequestRefused(Exception):
    """Why the request cannot be changed this way; the router turns it into the API's error."""

    def __init__(self, status: int, code: str, detail: str):
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail


def request_view(row: VideoDramaRequest, youtube_video_id: str | None = None) -> DramaRequestOut:
    """The request as the page and the worker see it: started and on YouTube counts as done."""
    status = "done" if row.status == "started" and youtube_video_id else row.status
    return DramaRequestOut(
        id=row.id,
        premise=row.premise,
        title=row.title,
        source_guide=row.source_guide,
        style_preset=row.style_preset,
        target_minutes=row.target_minutes,
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


async def create_request(
    session: AsyncSession, actor: User, payload: DramaRequestIn
) -> DramaRequestOut:
    now = _now()
    row = VideoDramaRequest(
        id=uuid4(),
        **payload.model_dump(),
        status="queued",
        created_by_user_id=actor.id,
        created_at=now,
        updated_at=now,
    )
    session.add(row)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_drama_request_created",
            target=f"video-drama-request:{row.id}",
            metadata_json={
                "style_preset": payload.style_preset,
                "target_minutes": payload.target_minutes,
                "source_guide": payload.source_guide,
            },
        )
    )
    await session.commit()
    return request_view(row)


async def list_requests(
    session: AsyncSession, *, active_only: bool = False
) -> list[DramaRequestOut]:
    """Every request, newest first, for the page; with ``active_only``, only the queued and
    started ones, oldest first, for the worker."""
    statement = select(VideoDramaRequest, VideoProject.youtube_video_id).outerjoin(
        VideoProject, VideoProject.slug == VideoDramaRequest.slug
    )
    if active_only:
        statement = statement.where(VideoDramaRequest.status.in_(ACTIVE)).order_by(
            VideoDramaRequest.created_at.asc()
        )
    else:
        statement = statement.order_by(VideoDramaRequest.created_at.desc())
    rows = await session.execute(statement.limit(LIST_LIMIT))
    return [request_view(row, youtube) for row, youtube in rows.all()]


async def next_request(session: AsyncSession) -> DramaRequestOut | None:
    """The oldest queued request, which the worker should start before any scheduled draft."""
    row = await session.scalar(
        select(VideoDramaRequest)
        .where(VideoDramaRequest.status == "queued")
        .order_by(VideoDramaRequest.created_at.asc())
        .limit(1)
    )
    return request_view(row) if row is not None else None


async def _request(session: AsyncSession, request_id: UUID) -> VideoDramaRequest:
    # Locked: two workers, or the owner and the worker, may act on one request at once.
    row = await session.scalar(
        select(VideoDramaRequest).where(VideoDramaRequest.id == request_id).with_for_update()
    )
    if row is None:
        raise RequestRefused(404, "video_drama_request_not_found", "找不到這個漫劇請求")
    return row


async def cancel_request(session: AsyncSession, actor: User, request_id: UUID) -> DramaRequestOut:
    row = await _request(session, request_id)
    if row.status != "queued":
        raise RequestRefused(
            409,
            "video_drama_request_not_queued",
            "工人已經開始做這支了；要停就到影片清單放棄那支影片",
        )
    now = _now()
    row.status = "cancelled"
    row.cancelled_at = now
    row.updated_at = now
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_drama_request_cancelled",
            target=f"video-drama-request:{row.id}",
            metadata_json={"style_preset": row.style_preset, "source_guide": row.source_guide},
        )
    )
    await session.commit()
    return request_view(row)


async def start_request(
    session: AsyncSession, token: VideoToolToken, request_id: UUID, slug: str
) -> DramaRequestOut:
    """The worker claims a queued request for the video it is about to make."""
    row = await _request(session, request_id)
    if row.status != "queued":
        raise RequestRefused(409, "video_drama_request_not_queued", "這個請求不在排隊中，不能開始")
    taken = await session.scalar(
        select(VideoDramaRequest.id).where(
            VideoDramaRequest.slug == slug, VideoDramaRequest.id != row.id
        )
    )
    if taken is not None:
        raise RequestRefused(
            409, "video_drama_request_slug_taken", f"{slug} 已經是另一個請求的影片"
        )
    now = _now()
    row.status = "started"
    row.slug = slug
    row.started_at = now
    row.updated_at = now
    row.started_by_token_id = token.id
    await session.commit()
    return request_view(row)


async def finish_request(session: AsyncSession, request_id: UUID) -> DramaRequestOut:
    """The worker reports the video is done (on YouTube, or the owner published it)."""
    row = await _request(session, request_id)
    if row.status != "started":
        raise RequestRefused(
            409, "video_drama_request_not_started", "這個請求還沒開始做，不能標成完成"
        )
    now = _now()
    row.status = "done"
    row.finished_at = now
    row.updated_at = now
    await session.commit()
    return request_view(row)
