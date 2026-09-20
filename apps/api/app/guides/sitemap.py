"""Stable, publication-aware pages for the article sitemap and its index."""

from __future__ import annotations

import base64
import json
from typing import cast
from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement

from app.guides.models import GuideArticle, GuideArticleLocale, GuideArticleRevision
from app.guides.publication import published_filters
from app.guides.schemas import (
    KINDS,
    SLUG_PATTERN,
    Kind,
    Section,
    SitemapCount,
    SitemapEntry,
    SitemapList,
    SitemapSummary,
)
from app.guides.service import SITEMAP_LIMIT, kind_filter
from app.i18n import LOCALES, Locale
from app.problems import AppError


def _encode_cursor(slug: str, locale: str) -> str:
    raw = json.dumps([slug, locale], separators=(",", ":"))
    return base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")


def _decode_cursor(cursor: str | None) -> tuple[str, str] | None:
    if cursor is None:
        return None
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        position = json.loads(base64.b64decode(padded, altchars=b"-_", validate=True))
        if not isinstance(position, list) or len(position) != 2:
            raise ValueError
        slug, locale = position
        if (
            not isinstance(slug, str)
            or len(slug) > 120
            or not SLUG_PATTERN.fullmatch(slug)
            or locale not in LOCALES
        ):
            raise ValueError
        return slug, locale
    except (ValueError, TypeError, UnicodeDecodeError):
        raise AppError(422, "guide_cursor_invalid", "分頁資訊無效，請重新瀏覽") from None


def _published_revision_join() -> ColumnElement[bool]:
    """Use the same current-published-revision pointer as the public article page."""
    return and_(
        GuideArticleRevision.article_locale_id == GuideArticleLocale.id,
        GuideArticleRevision.version == GuideArticleLocale.published_version,
        GuideArticleRevision.action == "published",
    )


async def _published_locales(
    session: AsyncSession, article_ids: set[UUID]
) -> dict[UUID, list[Locale]]:
    if not article_ids:
        return {}
    rows = await session.execute(
        select(GuideArticleLocale.article_id, GuideArticleLocale.locale)
        .join(GuideArticle, GuideArticle.id == GuideArticleLocale.article_id)
        .join(GuideArticleRevision, _published_revision_join())
        .where(GuideArticleLocale.article_id.in_(article_ids), *published_filters())
    )
    found: dict[UUID, set[str]] = {}
    for article_id, locale in rows:
        found.setdefault(article_id, set()).add(locale)
    return {
        article_id: [item for item in LOCALES if item in published]
        for article_id, published in found.items()
    }


async def entries(
    session: AsyncSession,
    *,
    section: Section | None = None,
    locale: Locale | None = None,
    cursor: str | None = None,
    offset: int = 0,
    limit: int = SITEMAP_LIMIT,
) -> SitemapList:
    """Enumerate live translations by immutable article slug and locale.

    Publication timestamps can change between page requests; they must not move a row
    across the cursor. The offset is used only for numbered sitemap children, before
    their first cursor, and the API still limits every response to 1,000 rows.
    """
    kinds = kind_filter(None, section)
    size = min(max(limit, 1), SITEMAP_LIMIT)
    position = _decode_cursor(cursor)
    query = (
        select(
            GuideArticle.id,
            GuideArticle.kind,
            GuideArticle.slug,
            GuideArticleLocale.locale,
            GuideArticleLocale.published_at,
            GuideArticleRevision.created_at,
        )
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .join(GuideArticleRevision, _published_revision_join())
        .where(GuideArticleLocale.published_at.is_not(None), *published_filters())
    )
    if kinds:
        query = query.where(GuideArticle.kind.in_(kinds))
    if locale:
        query = query.where(GuideArticleLocale.locale == locale)
    if position is not None:
        slug, after_locale = position
        query = query.where(
            or_(
                GuideArticle.slug > slug,
                and_(GuideArticle.slug == slug, GuideArticleLocale.locale > after_locale),
            )
        )
    rows = list(
        await session.execute(
            query.order_by(GuideArticle.slug, GuideArticleLocale.locale)
            .offset(offset)
            .limit(size + 1)
        )
    )
    has_more = len(rows) > size
    rows = rows[:size]
    siblings = await _published_locales(session, {article_id for article_id, *_ in rows})
    return SitemapList(
        entries=[
            SitemapEntry(
                kind=cast(Kind, kind),
                slug=slug,
                locale=cast(Locale, row_locale),
                published_at=published_at,
                modified_at=modified_at,
                locales=siblings[article_id],
            )
            for article_id, kind, slug, row_locale, published_at, modified_at in rows
        ],
        next_cursor=_encode_cursor(rows[-1][2], rows[-1][3]) if has_more else None,
    )


async def summary(session: AsyncSession) -> SitemapSummary:
    """Count exactly the translations that the paged enumeration can serve."""
    rows = await session.execute(
        select(GuideArticle.kind, GuideArticleLocale.locale, func.count())
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .join(GuideArticleRevision, _published_revision_join())
        .where(GuideArticleLocale.published_at.is_not(None), *published_filters())
        .group_by(GuideArticle.kind, GuideArticleLocale.locale)
    )
    counts = [
        SitemapCount(kind=cast(Kind, kind), locale=cast(Locale, locale), count=count)
        for kind, locale, count in rows
    ]
    order = {kind: index for index, kind in enumerate(KINDS)}
    counts.sort(key=lambda item: (order[item.kind], LOCALES.index(item.locale)))
    return SitemapSummary(counts=counts)
