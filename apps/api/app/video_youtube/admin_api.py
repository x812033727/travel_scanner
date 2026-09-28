"""HTTP surface of the YouTube link on /admin/videos (docs/videos/HANDS-OFF.md §YouTube API).

``connection_router`` is the card on the settings tab: anyone who reviews videos may read it; the
OAuth client, the link and the unlink need ``settings.manage``, since the grant writes to the
channel. The link's browser half is apps/web/app/api/admin-video-youtube (start and callback),
which calls ``/oauth/start`` and ``/oauth/exchange`` with the admin's session. ``publish_router``
is the "ready to upload" card: sending a video to the channel and retrying a run that stopped
need ``content.manage``, like recording the YouTube address by hand.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import require_capability
from app.db import get_session
from app.models import User
from app.problems import AppError
from app.video_reviews.admin_service import review_store
from app.video_reviews.schemas import ProjectOut
from app.video_youtube import connection, sync, vps
from app.video_youtube.errors import Refused
from app.video_youtube.schemas import (
    ClientIn,
    ConnectionView,
    OAuthExchangeIn,
    OAuthStartIn,
    OAuthStartOut,
    PublishIn,
    UnlinkOut,
)

Session = Annotated[AsyncSession, Depends(get_session)]
ContentReader = Annotated[User, Depends(require_capability("content.read"))]
ContentManager = Annotated[User, Depends(require_capability("content.manage"))]
SettingsManager = Annotated[User, Depends(require_capability("settings.manage"))]

connection_router = APIRouter(prefix="/admin/video-youtube", tags=["admin video youtube"])
publish_router = APIRouter(prefix="/admin/videos", tags=["admin video youtube"])


@contextmanager
def answered() -> Iterator[None]:
    """A refusal from the services, answered as the API's problem response."""
    try:
        yield
    except Refused as refused:
        raise AppError(refused.status, refused.code, refused.detail) from refused


@connection_router.get("", response_model=ConnectionView)
async def read_connection(user: ContentReader, session: Session) -> ConnectionView:
    _ = user
    with answered():
        return await connection.connection_view(session)


@connection_router.put("", response_model=ConnectionView)
async def save_client(payload: ClientIn, user: SettingsManager, session: Session) -> ConnectionView:
    with answered():
        return await connection.save_client(session, user, payload)


@connection_router.post("/oauth/start", response_model=OAuthStartOut)
async def start_link(
    payload: OAuthStartIn, user: SettingsManager, session: Session
) -> OAuthStartOut:
    with answered():
        return await connection.start_link(session, user, payload)


@connection_router.post("/oauth/exchange", response_model=ConnectionView)
async def finish_link(
    payload: OAuthExchangeIn, user: SettingsManager, session: Session
) -> ConnectionView:
    with answered():
        return await connection.finish_link(session, user, payload)


@connection_router.post("/verify", response_model=ConnectionView)
async def verify(user: SettingsManager, session: Session) -> ConnectionView:
    _ = user
    with answered():
        return await connection.verify(session)


@connection_router.post("/unlink", response_model=UnlinkOut)
async def unlink(user: SettingsManager, session: Session) -> UnlinkOut:
    with answered():
        revoked, view = await connection.unlink(session, user)
    return UnlinkOut(revoked=revoked, connection=view)


@publish_router.post("/{slug}/youtube/publish", response_model=ProjectOut, status_code=202)
async def publish(
    slug: str, payload: PublishIn, user: ContentManager, session: Session
) -> ProjectOut:
    """Send the approved package to the linked channel; the run goes on after the answer."""
    with answered():
        store = review_store(await load_runtime_settings(session))
        return await sync.request_sync(session, store, slug, user, payload)


@publish_router.post("/{slug}/youtube/retry", response_model=ProjectOut, status_code=202)
async def retry(slug: str, user: ContentManager, session: Session) -> ProjectOut:
    with answered():
        return await sync.retry_sync(session, slug, user)


@publish_router.get("/{slug}/youtube/vps")
async def vps_status(slug: str, user: ContentReader, session: Session) -> dict[str, Any]:
    _ = user
    with answered():
        return await vps.status(session, slug)


@publish_router.post("/{slug}/youtube/vps", status_code=202)
async def vps_start(
    slug: str,
    payload: vps.StartIn,
    user: ContentManager,
    session: Session,
) -> dict[str, Any]:
    with answered():
        return await vps.start(session, slug, user, payload)


@publish_router.post("/{slug}/youtube/vps/stage")
async def vps_stage(slug: str, user: ContentManager, session: Session) -> dict[str, Any]:
    _ = user
    with answered():
        return await vps.stage(session, slug)


@publish_router.post("/{slug}/youtube/vps/{action}")
async def vps_action(
    slug: str,
    action: str,
    payload: vps.ResumeIn,
    user: ContentManager,
    session: Session,
) -> dict[str, Any]:
    with answered():
        return await vps.action(session, slug, user, action, payload)
