from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AdminUser
from app.db import get_session
from app.i18n import Locale
from app.site_pages import service
from app.site_pages.schemas import (
    DraftWrite,
    InitializationResult,
    PageDetail,
    PageList,
    PageSlug,
    PublicPage,
    PublishWrite,
    RestoreWrite,
    RevisionDetail,
)

Session = Annotated[AsyncSession, Depends(get_session)]
admin_router = APIRouter(prefix="/admin/site-pages", tags=["admin site pages"])
public_router = APIRouter(prefix="/site-pages", tags=["public information"])


@public_router.get("/{slug}", response_model=PublicPage)
async def get_public_page(
    slug: PageSlug, response: Response, session: Session, locale: Locale = "zh-TW"
) -> PublicPage:
    response.headers["Cache-Control"] = "no-store"
    return await service.public_page(session, slug, locale)


@admin_router.get("", response_model=PageList)
async def get_pages(user: AdminUser, session: Session) -> PageList:
    return await service.list_pages(session)


@admin_router.post("/initialize", response_model=InitializationResult)
async def initialize(user: AdminUser, session: Session) -> InitializationResult:
    return await service.initialize_pages(session, user)


@admin_router.get("/{slug}", response_model=PageDetail)
async def get_page(
    slug: PageSlug, user: AdminUser, session: Session, locale: Locale = "zh-TW"
) -> PageDetail:
    return await service.page_detail(session, slug, locale)


@admin_router.put("/{slug}/draft", response_model=PageDetail)
async def put_draft(
    slug: PageSlug,
    payload: DraftWrite,
    user: AdminUser,
    session: Session,
    locale: Locale = "zh-TW",
) -> PageDetail:
    return await service.save_draft(session, user, slug, locale, payload)


@admin_router.post("/{slug}/publish", response_model=PageDetail)
async def publish(
    slug: PageSlug,
    payload: PublishWrite,
    user: AdminUser,
    session: Session,
    locale: Locale = "zh-TW",
) -> PageDetail:
    return await service.publish_page(session, user, slug, locale, payload)


@admin_router.get("/{slug}/revisions/{revision_id}", response_model=RevisionDetail)
async def revision(
    slug: PageSlug,
    revision_id: UUID,
    user: AdminUser,
    session: Session,
    locale: Locale = "zh-TW",
) -> RevisionDetail:
    return await service.get_revision(session, slug, locale, revision_id)


@admin_router.post("/{slug}/restore", response_model=PageDetail)
async def restore(
    slug: PageSlug,
    payload: RestoreWrite,
    user: AdminUser,
    session: Session,
    locale: Locale = "zh-TW",
) -> PageDetail:
    return await service.restore_revision(session, user, slug, locale, payload)
