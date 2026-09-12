"""Reading published travel intel and guide articles, and the lookups both sides share.

Authoring lives in ``app.guides.admin_service``. The split is not only tidiness: everything
raised from this module is a sentence a reader can be shown, and
``tests/test_error_localization.py`` holds public modules to a translated sentence for every
error code. Keeping the operator errors out of here keeps that boundary honest.
"""

from __future__ import annotations

import base64
import hashlib
import json
from datetime import datetime
from typing import Any, cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.destinations.catalog import destination_for_id
from app.destinations.localized import city_name
from app.guides.models import (
    GuideArticle,
    GuideArticleLocale,
    GuideArticleRevision,
    GuideArticleTopic,
    GuideTopic,
)
from app.guides.publication import article_is_live, published_filters
from app.guides.schemas import (
    GuideDocument,
    Kind,
    PublicArticle,
    PublicList,
    PublicSummary,
    PublishedDocument,
    SitemapEntry,
    SitemapList,
)
from app.guides.taxonomy import topic_option
from app.i18n import LOCALES, Locale
from app.problems import AppError

MAX_PAGE = 50
SITEMAP_LIMIT = 1000


def _target(article_id: UUID, locale: str | None = None) -> str:
    """AdminAuditLog.target is String(128) and a slug may be 120 characters, so the slug
    cannot go in here. The id also survives a slug rename, which the audit trail should."""
    return f"guide:{article_id}:{locale}" if locale else f"guide:{article_id}"


def document_hash(document: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(document, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()


def destination_label(destination_id: str | None, locale: Locale) -> str | None:
    profile = destination_for_id(destination_id)
    return city_name(profile, locale) if profile is not None else None


# --- shared lookups -----------------------------------------------------------


async def _topics_for(
    session: AsyncSession, article_ids: list[UUID]
) -> dict[UUID, list[GuideTopic]]:
    if not article_ids:
        return {}
    rows = await session.execute(
        select(GuideArticleTopic.article_id, GuideTopic)
        .join(GuideTopic, GuideTopic.id == GuideArticleTopic.topic_id)
        .where(GuideArticleTopic.article_id.in_(article_ids))
        .order_by(GuideTopic.display_order, GuideTopic.slug)
    )
    grouped: dict[UUID, list[GuideTopic]] = {}
    for article_id, topic in rows:
        grouped.setdefault(article_id, []).append(topic)
    return grouped


async def _locale_rows(
    session: AsyncSession, article_ids: list[UUID]
) -> dict[UUID, list[GuideArticleLocale]]:
    if not article_ids:
        return {}
    rows = await session.scalars(
        select(GuideArticleLocale)
        .where(GuideArticleLocale.article_id.in_(article_ids))
        .order_by(GuideArticleLocale.locale)
        # The writes above are conditional UPDATEs the ORM does not see, and the session
        # keeps instances across commit (expire_on_commit=False). Without this the detail
        # response echoes the version the caller just superseded.
        .execution_options(populate_existing=True)
    )
    grouped: dict[UUID, list[GuideArticleLocale]] = {}
    for row in rows:
        grouped.setdefault(row.article_id, []).append(row)
    return grouped


async def _published_document(
    session: AsyncSession, row: GuideArticleLocale
) -> PublishedDocument | None:
    if row.published_version is None:
        return None
    revision = await session.scalar(
        select(GuideArticleRevision).where(
            GuideArticleRevision.article_locale_id == row.id,
            GuideArticleRevision.version == row.published_version,
            GuideArticleRevision.action == "published",
        )
    )
    if revision is None:
        # A damaged pointer must never turn the current draft into a public fallback.
        raise AppError(503, "guide_article_unavailable", "暫時無法取得這篇文章，請稍後再試")
    document = GuideDocument.model_validate(revision.document_json)
    return PublishedDocument(
        **document.model_dump(),
        version=revision.version,
        published_at=row.published_at or revision.created_at,
    )


# --- public reads -------------------------------------------------------------


def _encode_cursor(published_at: datetime, slug: str) -> str:
    raw = json.dumps([published_at.isoformat(), slug], separators=(",", ":"))
    return base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")


def _decode_cursor(cursor: str | None) -> tuple[datetime, str] | None:
    if not cursor:
        return None
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        stamp, slug = json.loads(base64.urlsafe_b64decode(padded.encode()).decode())
        return datetime.fromisoformat(stamp), str(slug)
    except (ValueError, TypeError):
        # A cursor the reader hand-edited is a bad request, not a server fault, and it
        # must not silently return page one as if it were the page they asked for.
        raise AppError(422, "guide_cursor_invalid", "分頁資訊無效，請重新瀏覽") from None


async def public_list(
    session: AsyncSession,
    locale: Locale,
    *,
    kind: Kind | None = None,
    destination: str | None = None,
    topic: str | None = None,
    cursor: str | None = None,
    limit: int = 20,
) -> PublicList:
    size = min(max(limit, 1), MAX_PAGE)
    query = (
        select(GuideArticle, GuideArticleLocale)
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .where(GuideArticleLocale.locale == locale, *published_filters())
    )
    if kind is not None:
        query = query.where(GuideArticle.kind == kind)
    if destination:
        query = query.where(GuideArticle.destination_id == destination.casefold())
    if topic:
        query = query.where(
            GuideArticle.id.in_(
                select(GuideArticleTopic.article_id)
                .join(GuideTopic, GuideTopic.id == GuideArticleTopic.topic_id)
                .where(GuideTopic.slug == topic.casefold())
            )
        )
    position = _decode_cursor(cursor)
    if position is not None:
        stamp, slug = position
        query = query.where(
            (GuideArticleLocale.published_at < stamp)
            | ((GuideArticleLocale.published_at == stamp) & (GuideArticle.slug > slug))
        )
    rows = list(
        await session.execute(
            query.order_by(GuideArticleLocale.published_at.desc(), GuideArticle.slug).limit(
                size + 1
            )
        )
    )
    has_more = len(rows) > size
    rows = rows[:size]
    topics = await _topics_for(session, [article.id for article, _ in rows])
    articles: list[PublicSummary] = []
    for article, row in rows:
        published = await _published_document(session, row)
        if published is None:
            continue
        articles.append(
            PublicSummary(
                slug=article.slug,
                kind=cast(Kind, article.kind),
                destination_id=article.destination_id,
                destination_label=destination_label(article.destination_id, locale),
                topics=[topic_option(item, locale) for item in topics.get(article.id, [])],
                title=published.title,
                description=published.description,
                published_at=published.published_at,
                valid_until=article.valid_until,
                featured=article.featured,
            )
        )
    last = rows[-1] if rows and has_more else None
    return PublicList(
        articles=articles,
        next_cursor=(
            _encode_cursor(last[1].published_at or last[1].updated_at, last[0].slug)
            if last is not None
            else None
        ),
    )


async def public_article(
    session: AsyncSession, kind: Kind, slug: str, locale: Locale
) -> PublicArticle:
    article = await session.scalar(
        select(GuideArticle).where(GuideArticle.slug == slug.casefold(), GuideArticle.kind == kind)
    )
    if article is None or not article.is_active:
        return PublicArticle(slug=slug, kind=kind, locale=locale, status="unpublished")
    rows = (await _locale_rows(session, [article.id])).get(article.id, [])
    published_locales = [
        cast(Locale, row.locale) for row in rows if row.published_version is not None
    ]
    row = next((item for item in rows if item.locale == locale), None)
    if row is None or row.published_version is None:
        # An unwritten translation is not a 404: the article exists in other languages and
        # the page links to them. It is simply not published here.
        return PublicArticle(
            slug=article.slug,
            kind=cast(Kind, article.kind),
            locale=locale,
            status="unpublished",
            published_locales=[item for item in LOCALES if item in set(published_locales)],
        )
    topics = (await _topics_for(session, [article.id])).get(article.id, [])
    return PublicArticle(
        slug=article.slug,
        kind=cast(Kind, article.kind),
        locale=locale,
        status="published",
        destination_id=article.destination_id,
        destination_label=destination_label(article.destination_id, locale),
        topics=[topic_option(item, locale) for item in topics],
        valid_until=article.valid_until,
        expired=not article_is_live(article),
        document=await _published_document(session, row),
        published_locales=[item for item in LOCALES if item in set(published_locales)],
    )


async def sitemap_entries(session: AsyncSession) -> SitemapList:
    """Publication-aware enumeration for ``apps/web/app/sitemap.ts``.

    Only rows that the list and the article page would also serve. Expired intel and
    withdrawn translations leave here at the same moment they leave the site.
    """
    rows = await session.execute(
        select(
            GuideArticle.kind,
            GuideArticle.slug,
            GuideArticleLocale.locale,
            GuideArticleLocale.published_at,
        )
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .where(*published_filters())
        .order_by(GuideArticleLocale.published_at.desc())
        .limit(SITEMAP_LIMIT)
    )
    return SitemapList(
        entries=[
            SitemapEntry(
                kind=cast(Kind, kind),
                slug=slug,
                locale=cast(Locale, locale),
                published_at=published_at,
            )
            for kind, slug, locale, published_at in rows
            if published_at is not None
        ]
    )
