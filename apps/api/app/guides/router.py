from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AdminUser
from app.db import get_session
from app.guides import admin_service, service, taxonomy
from app.guides.schemas import (
    ArticleCreate,
    ArticleDetail,
    ArticleList,
    ArticleUpdate,
    DraftWrite,
    GuideDocument,
    Kind,
    PublicArticle,
    PublicList,
    PublishWrite,
    RestoreWrite,
    RevisionDetail,
    SitemapList,
    TopicList,
)
from app.i18n import Locale

Session = Annotated[AsyncSession, Depends(get_session)]
public_router = APIRouter(prefix="/guides", tags=["travel guides"])
admin_router = APIRouter(prefix="/admin/guides", tags=["admin travel guides"])


@public_router.get("", response_model=PublicList)
async def list_public(
    response: Response,
    session: Session,
    locale: Locale = "zh-TW",
    kind: Kind | None = None,
    destination: str | None = Query(default=None, max_length=64),
    topic: str | None = Query(default=None, max_length=64),
    cursor: str | None = Query(default=None, max_length=512),
    limit: int = Query(default=20, ge=1, le=50),
) -> PublicList:
    response.headers["Cache-Control"] = "no-store"
    return await service.public_list(
        session, locale, kind=kind, destination=destination, topic=topic, cursor=cursor, limit=limit
    )


@public_router.get("/topics", response_model=TopicList)
async def list_public_topics(
    response: Response, session: Session, locale: Locale = "zh-TW"
) -> TopicList:
    response.headers["Cache-Control"] = "no-store"
    return await taxonomy.list_topics(session, locale)


@public_router.get("/sitemap", response_model=SitemapList)
async def public_sitemap(response: Response, session: Session) -> SitemapList:
    response.headers["Cache-Control"] = "no-store"
    return await service.sitemap_entries(session)


@public_router.get("/{kind}/{slug}", response_model=PublicArticle)
async def get_public_article(
    kind: Kind,
    slug: str,
    response: Response,
    session: Session,
    locale: Locale = "zh-TW",
) -> PublicArticle:
    response.headers["Cache-Control"] = "no-store"
    return await service.public_article(session, kind, slug, locale)


@admin_router.get("", response_model=ArticleList)
async def list_admin(
    user: AdminUser,
    session: Session,
    locale: Locale = "zh-TW",
    kind: Kind | None = None,
    destination: str | None = Query(default=None, max_length=64),
    topic: str | None = Query(default=None, max_length=64),
    limit: int = Query(default=50, ge=1, le=50),
) -> ArticleList:
    return await admin_service.list_articles(
        session, locale, kind=kind, destination=destination, topic=topic, limit=limit
    )


@admin_router.get("/topics", response_model=TopicList)
async def list_admin_topics(
    user: AdminUser, session: Session, locale: Locale = "zh-TW"
) -> TopicList:
    return await taxonomy.list_topics(session, locale)


@admin_router.post("", response_model=ArticleDetail, status_code=201)
async def create(payload: ArticleCreate, user: AdminUser, session: Session) -> ArticleDetail:
    return await admin_service.create_article(session, user, payload)


@admin_router.get("/{article_id}", response_model=ArticleDetail)
async def get_article(
    article_id: UUID, user: AdminUser, session: Session, locale: Locale = "zh-TW"
) -> ArticleDetail:
    return await admin_service.article_detail(session, article_id, locale)


@admin_router.put("/{article_id}", response_model=ArticleDetail)
async def update(
    article_id: UUID,
    payload: ArticleUpdate,
    user: AdminUser,
    session: Session,
    locale: Locale = "zh-TW",
) -> ArticleDetail:
    return await admin_service.update_article(session, user, article_id, payload, locale)


@admin_router.post("/{article_id}/{locale}", response_model=ArticleDetail, status_code=201)
async def add_translation(
    article_id: UUID,
    locale: Locale,
    payload: GuideDocument,
    user: AdminUser,
    session: Session,
) -> ArticleDetail:
    return await admin_service.start_translation(session, user, article_id, locale, payload)


@admin_router.put("/{article_id}/{locale}/draft", response_model=ArticleDetail)
async def put_draft(
    article_id: UUID,
    locale: Locale,
    payload: DraftWrite,
    user: AdminUser,
    session: Session,
) -> ArticleDetail:
    return await admin_service.save_draft(session, user, article_id, locale, payload)


@admin_router.post("/{article_id}/{locale}/publish", response_model=ArticleDetail)
async def publish(
    article_id: UUID,
    locale: Locale,
    payload: PublishWrite,
    user: AdminUser,
    session: Session,
) -> ArticleDetail:
    return await admin_service.publish_locale(session, user, article_id, locale, payload)


@admin_router.post("/{article_id}/{locale}/unpublish", response_model=ArticleDetail)
async def unpublish(
    article_id: UUID,
    locale: Locale,
    payload: PublishWrite,
    user: AdminUser,
    session: Session,
) -> ArticleDetail:
    return await admin_service.unpublish_locale(session, user, article_id, locale, payload)


@admin_router.get("/{article_id}/{locale}/revisions/{revision_id}", response_model=RevisionDetail)
async def revision(
    article_id: UUID,
    locale: Locale,
    revision_id: UUID,
    user: AdminUser,
    session: Session,
) -> RevisionDetail:
    return await admin_service.get_revision(session, article_id, locale, revision_id)


@admin_router.post("/{article_id}/{locale}/restore", response_model=ArticleDetail)
async def restore(
    article_id: UUID,
    locale: Locale,
    payload: RestoreWrite,
    user: AdminUser,
    session: Session,
) -> ArticleDetail:
    return await admin_service.restore_revision(session, user, article_id, locale, payload)
