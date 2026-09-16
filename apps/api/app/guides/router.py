from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.affiliates.content_links import CONTENT_PARTNERS
from app.auth.service import AdminUser
from app.db import get_session
from app.guides import admin_service, search, service, taxonomy
from app.guides.publication import ArticleStatus
from app.guides.schemas import (
    ArticleCreate,
    ArticleDetail,
    ArticleList,
    ArticleSummary,
    ArticleUpdate,
    BatchVisibilityResult,
    BatchVisibilityWrite,
    ContentPartnerList,
    ContentPartnerOption,
    DestinationFacetList,
    DraftWrite,
    GuideDocument,
    GuideSearchResult,
    Kind,
    ListSort,
    PublicArticle,
    PublicList,
    PublicSeries,
    PublishWrite,
    RestoreWrite,
    RevisionDetail,
    Section,
    SeriesIndex,
    SitemapList,
    SitemapSummary,
    TopicList,
    VisibilityWrite,
)
from app.guides.series import public_series, public_series_index
from app.i18n import Locale
from app.infra import (
    client_ip,
    enforce_named_rate_limit,
    over_named_rate_limit,
    record_rate_limit_hit,
)
from app.problems import AppError

Session = Annotated[AsyncSession, Depends(get_session)]
public_router = APIRouter(prefix="/guides", tags=["travel guides"])
admin_router = APIRouter(prefix="/admin/guides", tags=["admin travel guides"])


@public_router.get("", response_model=PublicList)
async def list_public(
    response: Response,
    session: Session,
    locale: Locale = "zh-TW",
    kind: Kind | None = None,
    section: Section | None = None,
    destination: str | None = Query(default=None, max_length=64),
    country: str | None = Query(default=None, max_length=32),
    topic: str | None = Query(default=None, max_length=64),
    cursor: str | None = Query(default=None, max_length=512),
    limit: int = Query(default=20, ge=1, le=50),
    sort: ListSort = "latest",
) -> PublicList:
    response.headers["Cache-Control"] = "no-store"
    return await service.public_list(
        session,
        locale,
        kind=kind,
        section=section,
        destination=destination,
        country=country,
        topic=topic,
        cursor=cursor,
        limit=limit,
        sort=sort,
    )


# A reader's search box, not an editor's: 120 queries a minute per address is far more
# than a person types and far less than a scraper wants. The limiter fails open on
# purpose (``over_named_rate_limit``): a search that goes dark because Redis blinked is
# the worse outcome, and the hit is recorded so a threshold can be judged before it bites.
SEARCH_RATE_LIMIT = 120
SEARCH_RATE_WINDOW_SECONDS = 60


@public_router.get("/search", response_model=GuideSearchResult)
async def search_public(
    request: Request,
    response: Response,
    session: Session,
    q: str = Query(min_length=1, max_length=search.MAX_QUERY_LENGTH),
    locale: Locale = "zh-TW",
    kind: Kind | None = None,
    section: Section | None = None,
    destination: str | None = Query(default=None, max_length=64),
    country: str | None = Query(default=None, max_length=32),
    topic: str | None = Query(default=None, max_length=64),
    limit: int = Query(default=10, ge=1, le=search.MAX_LIMIT),
    offset: int = Query(default=0, ge=0, le=search.MAX_OFFSET),
) -> GuideSearchResult:
    response.headers["Cache-Control"] = "no-store"
    ip = client_ip(request)
    if await over_named_rate_limit(
        "guide-search", ip, limit=SEARCH_RATE_LIMIT, window_seconds=SEARCH_RATE_WINDOW_SECONDS
    ):
        await record_rate_limit_hit("guide-search", ip)
        raise AppError(429, "rate_limit_exceeded", "請求過於頻繁，請稍後再試")
    return await search.search(
        session,
        locale,
        q=q,
        kind=kind,
        section=section,
        destination=destination,
        country=country,
        topic=topic,
        limit=limit,
        offset=offset,
    )


@public_router.get("/topics", response_model=TopicList)
async def list_public_topics(
    response: Response,
    session: Session,
    locale: Locale = "zh-TW",
    section: Section | None = None,
) -> TopicList:
    response.headers["Cache-Control"] = "no-store"
    return await taxonomy.list_topics(session, locale, section)


@public_router.get("/destinations", response_model=DestinationFacetList)
async def list_public_destinations(
    response: Response,
    session: Session,
    locale: Locale = "zh-TW",
    section: Section | None = None,
) -> DestinationFacetList:
    response.headers["Cache-Control"] = "no-store"
    return await service.destination_facets(session, locale, section)


@public_router.get("/sitemap", response_model=SitemapList)
async def public_sitemap(
    response: Response,
    session: Session,
    section: Section | None = None,
    locale: Locale | None = None,
    cursor: str | None = Query(default=None, max_length=512),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=service.SITEMAP_LIMIT, ge=1, le=service.SITEMAP_LIMIT),
) -> SitemapList:
    response.headers["Cache-Control"] = "no-store"
    return await service.sitemap_entries(
        session, section=section, locale=locale, cursor=cursor, offset=offset, limit=limit
    )


@public_router.get("/sitemap/summary", response_model=SitemapSummary)
async def public_sitemap_summary(response: Response, session: Session) -> SitemapSummary:
    response.headers["Cache-Control"] = "no-store"
    return await service.sitemap_summary(session)


@public_router.get("/series", response_model=SeriesIndex)
async def list_public_series(
    response: Response,
    session: Session,
    locale: Locale = "zh-TW",
) -> SeriesIndex:
    response.headers["Cache-Control"] = "no-store"
    return await public_series_index(session, locale)


@public_router.get("/series/{series_slug}", response_model=PublicSeries)
async def get_public_series(
    series_slug: str,
    response: Response,
    session: Session,
    locale: Locale = "zh-TW",
) -> PublicSeries:
    response.headers["Cache-Control"] = "no-store"
    result = await public_series(session, series_slug, locale)
    if result is None:
        raise AppError(404, "guide_article_unavailable", "暫時無法取得這篇文章，請稍後再試")
    return result


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


# Not ``.../clickout``: that suffix is excluded from the site's Referrer-Policy header in
# apps/web/next.config.ts, and this request neither redirects nor needs the exemption. The
# link itself goes straight to the partner; this only counts the click, and the reader's
# browser never waits for it.
@public_router.post("/{kind}/{slug}/partner-links/{key}/click", status_code=204)
async def count_partner_click(
    kind: Kind,
    slug: Annotated[str, Path(max_length=120)],
    key: Annotated[str, Path(pattern=r"^[0-9a-f]{16}$")],
    request: Request,
    session: Session,
    locale: Locale = "zh-TW",
) -> Response:
    # Fails closed: while Redis is unreachable a click goes uncounted, which no reader sees,
    # rather than an unthrottled endpoint writing rows.
    await enforce_named_rate_limit(
        "guide-partner-click", client_ip(request), limit=60, window_seconds=60
    )
    await service.record_partner_click(session, kind, slug, locale, key)
    return Response(status_code=204, headers={"Cache-Control": "no-store"})


@admin_router.get("", response_model=ArticleList)
async def list_admin(
    user: AdminUser,
    session: Session,
    locale: Locale = "zh-TW",
    kind: Kind | None = None,
    section: Section | None = None,
    destination: str | None = Query(default=None, max_length=64),
    topic: str | None = Query(default=None, max_length=64),
    status: ArticleStatus | None = None,
    q: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=30, ge=1, le=100),
) -> ArticleList:
    return await admin_service.list_articles(
        session,
        locale,
        kind=kind,
        section=section,
        destination=destination,
        topic=topic,
        status=status,
        q=q,
        page=page,
        limit=limit,
    )


@admin_router.get("/topics", response_model=TopicList)
async def list_admin_topics(
    user: AdminUser,
    session: Session,
    locale: Locale = "zh-TW",
    section: Section | None = None,
) -> TopicList:
    return await taxonomy.list_topics(session, locale, section)


# Before ``/{article_id}``, like the routes below: that pattern would take "partners" as an
# article id and answer 422.
@admin_router.get("/partners", response_model=ContentPartnerList)
async def list_content_partners(user: AdminUser) -> ContentPartnerList:
    return ContentPartnerList(
        partners=[
            ContentPartnerOption(
                code=partner.code,
                display_name=partner.display_name,
                category=partner.category,
                hosts=list(partner.hosts),
            )
            for partner in CONTENT_PARTNERS
        ]
    )


@admin_router.post("", response_model=ArticleDetail, status_code=201)
async def create(payload: ArticleCreate, user: AdminUser, session: Session) -> ArticleDetail:
    return await admin_service.create_article(session, user, payload)


# Declared before the ``/{article_id}/...`` routes on purpose. Starlette takes the first
# pattern that matches and FastAPI then validates the parameters, so ``POST /batch`` and
# ``POST /{id}/hide`` would otherwise land in ``/{article_id}/{locale}`` and fail as 422.
@admin_router.post("/batch", response_model=BatchVisibilityResult)
async def batch_visibility(
    payload: BatchVisibilityWrite,
    user: AdminUser,
    session: Session,
    locale: Locale = "zh-TW",
) -> BatchVisibilityResult:
    return await admin_service.batch_visibility(session, user, payload, locale)


@admin_router.post("/{article_id}/hide", response_model=ArticleSummary)
async def hide(
    article_id: UUID,
    payload: VisibilityWrite,
    user: AdminUser,
    session: Session,
    locale: Locale = "zh-TW",
) -> ArticleSummary:
    return await admin_service.set_visibility(
        session, user, article_id, hidden=True, payload=payload, locale=locale
    )


@admin_router.post("/{article_id}/unhide", response_model=ArticleSummary)
async def unhide(
    article_id: UUID,
    payload: VisibilityWrite,
    user: AdminUser,
    session: Session,
    locale: Locale = "zh-TW",
) -> ArticleSummary:
    return await admin_service.set_visibility(
        session, user, article_id, hidden=False, payload=payload, locale=locale
    )


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
