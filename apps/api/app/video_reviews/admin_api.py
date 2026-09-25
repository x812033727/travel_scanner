"""HTTP surface of /admin/videos. Operator-only: readers never reach it.

``tool_router`` is what the local pipeline calls with its video tool token, through the web
routes under apps/web/app/api/video/reviews: report a video's state, upload a preview in parts,
submit something for review, and read back the owner's decisions. ``admin_router`` is the page:
the owner lists the videos, opens one, watches its previews and decides.
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import require_capability
from app.db import get_session
from app.models import User
from app.problems import AppError
from app.video_reviews import admin_service as service
from app.video_reviews.schemas import (
    DecisionIn,
    PartOut,
    ProjectIn,
    ProjectOut,
    ProjectSummary,
    ReviewIn,
    ReviewOut,
)
from app.video_reviews.storage import PART_BYTES, ReviewStore, StorageRefused
from app.video_speech.admin_api import VideoTool

Session = Annotated[AsyncSession, Depends(get_session)]
ContentReader = Annotated[User, Depends(require_capability("content.read"))]
ContentManager = Annotated[User, Depends(require_capability("content.manage"))]

tool_router = APIRouter(prefix="/video/reviews", tags=["video reviews (pipeline)"])
admin_router = APIRouter(prefix="/admin/videos", tags=["admin video reviews"])


async def _store(session: AsyncSession) -> ReviewStore:
    return service.review_store(await load_runtime_settings(session))


@tool_router.put("/{slug}", response_model=ProjectOut)
async def report_project(
    slug: str, payload: ProjectIn, tool: VideoTool, session: Session
) -> ProjectOut:
    _ = tool
    return await service.upsert_project(session, await _store(session), slug, payload)


@tool_router.get("/{slug}", response_model=ProjectOut)
async def read_project(slug: str, tool: VideoTool, session: Session) -> ProjectOut:
    """The owner's decisions, for `review-pull`."""
    _ = tool
    return await service.project_view(session, slug)


@tool_router.put("/{slug}/files/{sha256}", response_model=PartOut)
async def upload_part(
    slug: str,
    sha256: str,
    request: Request,
    tool: VideoTool,
    session: Session,
    part: Annotated[int, Query(ge=0, le=10_000)],
    parts: Annotated[int, Query(ge=1, le=10_000)],
    size: Annotated[int, Query(ge=1)],
) -> PartOut:
    _ = tool
    body = await request.body()
    if len(body) > PART_BYTES:
        raise AppError(413, "video_review_part_too_large", f"每一段最多 {PART_BYTES} 位元組")
    store = await _store(session)
    try:
        result = store.put_part(slug, sha256, index=part, count=parts, size=size, data=body)
    except StorageRefused as error:
        raise AppError(error.status, error.code, error.detail) from error
    return PartOut(received=result.received, complete=result.complete)


@tool_router.post("/{slug}/reviews", response_model=ReviewOut, status_code=201)
async def submit(slug: str, payload: ReviewIn, tool: VideoTool, session: Session) -> ReviewOut:
    return await service.submit_review(session, await _store(session), slug, payload, tool)


@admin_router.get("", response_model=list[ProjectSummary])
async def list_videos(user: ContentReader, session: Session) -> list[ProjectSummary]:
    _ = user
    return await service.list_projects(session)


@admin_router.get("/{slug}", response_model=ProjectOut)
async def video_detail(slug: str, user: ContentReader, session: Session) -> ProjectOut:
    _ = user
    return await service.project_view(session, slug)


@admin_router.post("/{slug}/reviews/{review_id}/decision", response_model=ReviewOut)
async def decide(
    slug: str, review_id: UUID, payload: DecisionIn, user: ContentManager, session: Session
) -> ReviewOut:
    return await service.decide(session, slug, review_id, user, payload)


@admin_router.get("/{slug}/files/{sha256}")
async def video_file(slug: str, sha256: str, user: ContentReader, session: Session) -> FileResponse:
    """A preview, with byte ranges so the player can seek; never cached outside the browser."""
    _ = user
    path, content_type = await service.file_for_admin(session, await _store(session), slug, sha256)
    return FileResponse(
        path,
        media_type=content_type,
        headers={"Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff"},
    )
