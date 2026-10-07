"""The public video library: the videos the site has published on YouTube, for /videos.

Only what a reader may see leaves here. A video is listed once it is public on YouTube by the
site's own record: it has a YouTube id, the time the owner scheduled it to go public has
passed, and nobody dropped it. A video uploaded as private or unlisted has no publication time
(``youtube_publish_at`` stays null), so it is never listed, whatever its id.
"""

from __future__ import annotations

import base64
import binascii
from datetime import UTC, datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel
from sqlalchemy import ColumnElement, and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.guides.models import GuideArticle
from app.models import VIDEO_CATEGORIES, VideoProject

Session = Annotated[AsyncSession, Depends(get_session)]
public_router = APIRouter(prefix="/videos", tags=["public videos"])

PAGE_SIZE = 24
VideoKind = Literal["long", "shorts"]


class PublicVideo(BaseModel):
    slug: str
    title: str
    youtube_video_id: str
    category: str | None
    kind: VideoKind
    # The article the video retells, so the card can link to it: its slug and its kind, which
    # decides the article's address. Both null when the article is unknown or inactive.
    source_guide: str | None
    source_guide_kind: str | None
    published_at: datetime


class PublicVideoPage(BaseModel):
    videos: list[PublicVideo]
    next_cursor: str | None
    categories: list[str]


def _cursor(project: VideoProject) -> str:
    assert project.youtube_publish_at is not None
    raw = f"{project.youtube_publish_at.isoformat()}|{project.id}"
    return base64.urlsafe_b64encode(raw.encode()).decode()


def _read_cursor(value: str) -> tuple[datetime, UUID] | None:
    try:
        stamp, ident = base64.urlsafe_b64decode(value.encode()).decode().split("|", 1)
        return datetime.fromisoformat(stamp), UUID(ident)
    except (ValueError, binascii.Error, UnicodeDecodeError):
        return None


def _published(now: datetime) -> ColumnElement[bool]:
    return and_(
        VideoProject.youtube_video_id.is_not(None),
        VideoProject.youtube_publish_at.is_not(None),
        VideoProject.youtube_publish_at <= now,
        VideoProject.dropped_at.is_(None),
    )


@public_router.get("", response_model=PublicVideoPage)
async def list_videos(
    response: Response,
    session: Session,
    category: Annotated[str | None, Query(max_length=16)] = None,
    kind: VideoKind | None = None,
    guide: Annotated[str | None, Query(max_length=120)] = None,
    cursor: Annotated[str | None, Query(max_length=200)] = None,
    limit: Annotated[int, Query(ge=1, le=48)] = PAGE_SIZE,
) -> PublicVideoPage:
    """Newest first. A cursor the server cannot read starts from the top rather than failing:
    it is a reader's bookmark, not an instruction."""
    response.headers["Cache-Control"] = "public, max-age=300"
    now = datetime.now(UTC)
    query = select(VideoProject).where(_published(now))
    if category in VIDEO_CATEGORIES:
        query = query.where(VideoProject.category == category)
    if guide:
        # The article page asks for the videos that retell it.
        query = query.where(VideoProject.source_guide == guide)
    if kind == "shorts":
        query = query.where(VideoProject.shorts_line.is_not(None))
    elif kind == "long":
        query = query.where(VideoProject.shorts_line.is_(None))
    position = _read_cursor(cursor) if cursor else None
    if position is not None:
        stamp, ident = position
        query = query.where(
            or_(
                VideoProject.youtube_publish_at < stamp,
                and_(VideoProject.youtube_publish_at == stamp, VideoProject.id < ident),
            )
        )
    query = query.order_by(VideoProject.youtube_publish_at.desc(), VideoProject.id.desc())
    rows = list((await session.scalars(query.limit(limit + 1))).all())
    page = rows[:limit]
    used = await session.scalars(
        select(VideoProject.category)
        .where(_published(now), VideoProject.category.is_not(None))
        .distinct()
    )
    present = set(used.all())
    slugs = {row.source_guide for row in page if row.source_guide}
    kinds: dict[str, str] = {}
    if slugs:
        found = await session.execute(
            select(GuideArticle.slug, GuideArticle.kind).where(
                GuideArticle.slug.in_(slugs), GuideArticle.is_active.is_(True)
            )
        )
        kinds = {slug: kind for slug, kind in found.all()}
    return PublicVideoPage(
        videos=[
            PublicVideo(
                slug=row.slug,
                title=row.title,
                youtube_video_id=row.youtube_video_id or "",
                category=row.category,
                kind="shorts" if row.shorts_line else "long",
                source_guide=row.source_guide if row.source_guide in kinds else None,
                source_guide_kind=kinds.get(row.source_guide or ""),
                published_at=row.youtube_publish_at or now,
            )
            for row in page
        ],
        next_cursor=_cursor(page[-1]) if len(rows) > limit else None,
        # In the vocabulary's order, only the ones with something published.
        categories=[code for code in VIDEO_CATEGORIES if code in present],
    )
