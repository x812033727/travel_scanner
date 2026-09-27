"""HTTP surface of the YouTube connection and the per-video sync.

``/admin/video-youtube/connection`` is the settings tab's card: its state for any content
manager, and connecting, the callback Google sends the owner back to, and revoking for the
owner alone (it is their Google account). ``/admin/video-youtube/{slug}/sync`` queues a send
again for a video's page.
"""

from __future__ import annotations

from typing import Annotated
from urllib.parse import parse_qsl, urlencode, urlsplit

import httpx
from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import require_capability
from app.db import get_session
from app.infra import get_redis
from app.models import User
from app.problems import AppError
from app.video_reviews import admin_service as reviews
from app.video_reviews.schemas import ProjectOut
from app.video_youtube import oauth, service
from app.video_youtube.client import TIMEOUT_SECONDS, YouTubeError
from app.video_youtube.schemas import ConnectionOut, StartIn, StartOut

Session = Annotated[AsyncSession, Depends(get_session)]
ContentManager = Annotated[User, Depends(require_capability("content.manage"))]
Owner = Annotated[User, Depends(require_capability("roles.manage"))]

router = APIRouter(prefix="/admin/video-youtube", tags=["admin video youtube"])


def _http() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=TIMEOUT_SECONDS, trust_env=False)


@router.get("/connection", response_model=ConnectionOut)
async def connection(user: ContentManager, session: Session) -> ConnectionOut:
    _ = user
    return await oauth.connection(session, await load_runtime_settings(session))


@router.post("/connection/start", response_model=StartOut)
async def start(payload: StartIn, user: Owner, session: Session) -> StartOut:
    settings = await load_runtime_settings(session)
    return await oauth.start(get_redis(), settings, user, payload.next_path)


def _back(next_path: str, outcome: str) -> RedirectResponse:
    """The page the owner started from, told how it went in a ``youtube=`` query parameter."""
    parts = urlsplit(next_path)
    query = {key: value for key, value in parse_qsl(parts.query, keep_blank_values=True)}
    query["youtube"] = outcome
    target = f"{parts.path}?{urlencode(query)}"
    return RedirectResponse(url=target, status_code=302)


@router.get("/connection/callback")
async def callback(
    user: Owner,
    session: Session,
    state: Annotated[str, Query(min_length=1, max_length=200)],
    code: Annotated[str | None, Query(max_length=2000)] = None,
    error: Annotated[str | None, Query(max_length=200)] = None,
) -> RedirectResponse:
    """Google sends the owner here after the consent screen; the browser then goes back to the
    settings tab with the outcome."""
    settings = await load_runtime_settings(session)
    if error or not code:
        flow = await oauth._flow(get_redis(), state)  # noqa: SLF001 -- the state is spent either way
        return _back(oauth.safe_next(str(flow.get("next") or "/")), error or "denied")
    try:
        async with _http() as http:
            next_path = await oauth.finish(
                session, get_redis(), http, settings, user, code=code, state=state
            )
    except YouTubeError as failure:
        raise AppError(
            502, "video_youtube_connect_failed", f"Google 沒有完成連結：{failure.detail}"
        ) from failure
    except httpx.HTTPError as failure:
        raise AppError(502, "video_youtube_unreachable", "連不上 Google") from failure
    return _back(next_path, "connected")


@router.delete("/connection", response_model=ConnectionOut)
async def revoke(user: Owner, session: Session) -> ConnectionOut:
    settings = await load_runtime_settings(session)
    async with _http() as http:
        return await oauth.revoke(session, http, settings, user)


@router.post("/{slug}/sync", response_model=ProjectOut, status_code=202)
async def sync_again(slug: str, user: ContentManager, session: Session) -> ProjectOut:
    """Queue a send again for a video the owner already pasted the address of."""
    _ = user
    project = await reviews._project(session, slug)  # noqa: SLF001 -- one module's helper
    if not project.youtube_video_id:
        raise AppError(
            409, "video_youtube_not_linked", "還沒有 YouTube 影片 id：先在影片頁貼上網址"
        )
    if service.enqueue_sync(slug, "manual") is None:
        raise AppError(503, "video_youtube_queue_unavailable", "佇列暫時無法使用，稍後再試")
    return await reviews.project_view(session, slug)
