from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import require_capability
from app.db import get_session
from app.infra import get_redis
from app.models import User
from app.news_automation import jobs, service
from app.news_automation.assets import public_asset
from app.news_automation.models import NewsCandidate, NewsSource
from app.news_automation.schemas import (
    CandidateAction,
    CandidateDetail,
    CandidatePage,
    CandidateStatus,
    SettingsView,
    SettingsWrite,
    SourcePatch,
    SourceView,
    SourceWrite,
    StatsView,
    Vertical,
)
from app.problems import AppError

Session = Annotated[AsyncSession, Depends(get_session)]
RedisDep = Annotated[Redis, Depends(get_redis)]
ContentReader = Annotated[User, Depends(require_capability("content.read"))]
ContentManager = Annotated[User, Depends(require_capability("content.manage"))]

admin_router = APIRouter(prefix="/admin/news", tags=["admin news automation"])
public_router = APIRouter(prefix="/news-assets", tags=["news assets"])


@admin_router.get("/sources", response_model=list[SourceView])
async def sources(user: ContentReader, session: Session) -> list[SourceView]:
    del user
    return await service.list_sources(session)


@admin_router.post("/sources", response_model=SourceView, status_code=201)
async def create_source(payload: SourceWrite, user: ContentManager, session: Session) -> SourceView:
    return await service.create_source(session, user, payload)


@admin_router.patch("/sources/{source_id}", response_model=SourceView)
async def update_source(
    source_id: UUID, payload: SourcePatch, user: ContentManager, session: Session
) -> SourceView:
    return await service.update_source(session, user, source_id, payload)


@admin_router.delete("/sources/{source_id}", status_code=204)
async def delete_source(source_id: UUID, user: ContentManager, session: Session) -> Response:
    await service.delete_source(session, user, source_id)
    return Response(status_code=204)


@admin_router.post("/sources/{source_id}/scan", status_code=202)
async def scan_source(source_id: UUID, user: ContentManager, session: Session) -> dict[str, str]:
    del user
    # Existence is checked before a queue record is created.
    row = await session.get(NewsSource, source_id)
    if row is None:
        raise AppError(404, "news_source_not_found", "找不到新聞來源")
    if not row.enabled:
        raise AppError(409, "news_source_disabled", "來源尚未啟用；可先執行來源驗證")
    configuration = await service.settings_row(session)
    if not configuration.enabled:
        raise AppError(409, "news_scanner_disabled", "全域掃描開關尚未啟用")
    return {"job_id": jobs.enqueue_source_scan(source_id)}


@admin_router.post("/sources/{source_id}/validate", response_model=SourceView)
async def validate_source(source_id: UUID, user: ContentManager, session: Session) -> SourceView:
    return await service.validate_source_now(session, user, source_id)


@admin_router.get("/settings", response_model=SettingsView)
async def get_settings(user: ContentReader, session: Session) -> SettingsView:
    del user
    return await service.settings_view(session)


@admin_router.put("/settings", response_model=SettingsView)
async def put_settings(
    payload: SettingsWrite, user: ContentManager, session: Session
) -> SettingsView:
    return await service.update_settings(session, user, payload)


@admin_router.get("/candidates", response_model=CandidatePage)
async def candidates(
    user: ContentReader,
    session: Session,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
    # Repeatable (?status=manual_review&status=failed) so the review list can ask for
    # exactly the statuses a person acts on instead of the newest rows of every kind.
    status: Annotated[list[CandidateStatus] | None, Query()] = None,
    vertical: Vertical | None = None,
) -> CandidatePage:
    del user
    return await service.list_candidates(
        session, page=page, limit=limit, status=list(status or []), vertical=vertical
    )


@admin_router.get("/candidates/{candidate_id}", response_model=CandidateDetail)
async def candidate(candidate_id: UUID, user: ContentReader, session: Session) -> CandidateDetail:
    del user
    return await service.candidate_detail(session, candidate_id)


@admin_router.post("/candidates/{candidate_id}/retry", response_model=CandidateDetail)
async def retry_candidate(
    candidate_id: UUID, payload: CandidateAction, user: ContentManager, session: Session
) -> CandidateDetail:
    result = await service.retry_candidate(session, user, candidate_id, payload)
    row = await session.get(NewsCandidate, candidate_id)
    jobs.enqueue_candidate(candidate_id, retry_count=row.retry_count if row else 0)
    return result


@admin_router.post("/candidates/{candidate_id}/verify", response_model=CandidateDetail)
async def verify_candidate(
    candidate_id: UUID, payload: CandidateAction, user: ContentManager, session: Session
) -> CandidateDetail:
    result = await service.reverify_candidate(session, user, candidate_id, payload)
    row = await session.get(NewsCandidate, candidate_id)
    jobs.enqueue_candidate(candidate_id, retry_count=row.retry_count if row else 0)
    return result


@admin_router.post("/candidates/{candidate_id}/not-duplicate", response_model=CandidateDetail)
async def clear_duplicate_candidate(
    candidate_id: UUID, payload: CandidateAction, user: ContentManager, session: Session
) -> CandidateDetail:
    result = await service.clear_duplicate_candidate(session, user, candidate_id, payload)
    row = await session.get(NewsCandidate, candidate_id)
    jobs.enqueue_candidate(candidate_id, retry_count=row.retry_count if row else 0)
    return result


@admin_router.post("/candidates/{candidate_id}/reject", response_model=CandidateDetail)
async def reject_candidate(
    candidate_id: UUID, payload: CandidateAction, user: ContentManager, session: Session
) -> CandidateDetail:
    return await service.reject_candidate(session, user, candidate_id, payload)


@admin_router.post("/candidates/{candidate_id}/publish", response_model=CandidateDetail)
async def publish_candidate(
    candidate_id: UUID,
    payload: CandidateAction,
    user: ContentManager,
    session: Session,
    redis: RedisDep,
) -> CandidateDetail:
    return await service.publish_candidate(session, user, candidate_id, payload, redis)


@admin_router.post("/candidates/{candidate_id}/major-error", response_model=CandidateDetail)
async def report_major_error(
    candidate_id: UUID, payload: CandidateAction, user: ContentManager, session: Session
) -> CandidateDetail:
    return await service.report_major_error(session, user, candidate_id, payload)


@admin_router.get("/stats", response_model=StatsView)
async def statistics(user: ContentReader, session: Session) -> StatsView:
    del user
    return await service.stats(session)


@public_router.get("/{filename}")
async def asset(filename: str, session: Session) -> Response:
    body, content_type, digest = await public_asset(session, filename)
    return Response(
        content=body,
        media_type=content_type,
        headers={
            "Cache-Control": "public, max-age=31536000, immutable",
            "ETag": f'"{digest}"',
            "X-Content-Type-Options": "nosniff",
        },
    )
