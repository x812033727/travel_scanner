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
from typing import Any, Literal, cast
from urllib.parse import urlsplit
from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.affiliates.content_links import PARTNERS_BY_CODE, link_key, partner_link_problem
from app.affiliates.sub_id import coarse_sub_id
from app.destinations.catalog import DESTINATIONS, DestinationProfile, destination_for_id
from app.destinations.localized import city_name, country_label
from app.guides.models import (
    GuideArticle,
    GuideArticleLocale,
    GuideArticleRevision,
    GuideArticleTopic,
    GuideTopic,
)
from app.guides.publication import article_is_live, published_filters
from app.guides.schemas import (
    KINDS,
    SECTION_KINDS,
    DestinationFacet,
    DestinationFacetList,
    GuideDocument,
    Kind,
    PartnerLinkBlock,
    PublicArticle,
    PublicList,
    PublicPartnerLink,
    PublicSummary,
    PublishedDocument,
    Section,
    SitemapCount,
    SitemapEntry,
    SitemapList,
    SitemapSummary,
    TopicOption,
)
from app.guides.series import article_navigation, resolve_article_links
from app.guides.taxonomy import parent_slugs, topic_ids_including_children, topic_option
from app.i18n import LOCALES, Locale
from app.models import AffiliateClick
from app.problems import AppError

MAX_PAGE = 50
# The largest page ``GET /guides/sitemap`` answers, and its default: a caller that predates
# paging still gets the newest thousand rows in one call, and a paging caller asks for less.
SITEMAP_LIMIT = 1000


def kind_filter(kind: Kind | None, section: Section | None) -> tuple[Kind, ...] | None:
    """The kinds a listing may show. ``None`` means no restriction; an empty tuple means
    the caller asked for a combination nothing satisfies (``?section=life&kind=intel``).

    Callers must treat the empty tuple as "answer with nothing", never as "no filter":
    the latter would let lifestyle articles leak into a travel list that only set a kind.
    """
    if section is None:
        return None if kind is None else (kind,)
    kinds = SECTION_KINDS[section]
    if kind is None:
        return kinds
    return (kind,) if kind in kinds else ()


def country_slug(country: str) -> str:
    """The URL form of a catalog country name: ``South Korea`` -> ``south-korea``."""
    return "-".join(country.strip().casefold().split())


def destinations_in_country(country: str) -> list[DestinationProfile]:
    """Every catalog destination whose country has this slug; empty for an unknown one.

    Empty is what the caller must answer with -- a filter on a country the catalog does not
    know is a request for nothing, not for everything.
    """
    wanted = country_slug(country)
    return [profile for profile in DESTINATIONS if country_slug(profile.country) == wanted]


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


async def _topic_options_for(
    session: AsyncSession, article_ids: list[UUID], locale: Locale
) -> dict[UUID, list[TopicOption]]:
    """The topic chips of each article, with a sub-topic naming its parent so the reader's
    side can link the chip to the right hub. Counts are not filled in here: a chip on a
    card is a label, and the numbers belong to the vocabulary read."""
    grouped = await _topics_for(session, article_ids)
    parents = await parent_slugs(session, [topic for items in grouped.values() for topic in items])
    return {
        article_id: [
            topic_option(
                item, locale, parent=parents.get(item.parent_id) if item.parent_id else None
            )
            for item in items
        ]
        for article_id, items in grouped.items()
    }


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
        modified_at=revision.created_at,
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
    section: Section | None = None,
    destination: str | None = None,
    country: str | None = None,
    topic: str | None = None,
    cursor: str | None = None,
    limit: int = 20,
) -> PublicList:
    kinds = kind_filter(kind, section)
    if kinds is not None and not kinds:
        return PublicList(articles=[], next_cursor=None)
    size = min(max(limit, 1), MAX_PAGE)
    topic_ids = await topic_ids_including_children(session, topic) if topic else None
    if topic_ids is not None and not topic_ids:
        # An unknown topic, like an impossible kind/section pair, is a request for nothing.
        return PublicList(articles=[], next_cursor=None)
    query = (
        select(GuideArticle, GuideArticleLocale)
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .where(GuideArticleLocale.locale == locale, *published_filters())
    )
    if kinds:
        query = query.where(GuideArticle.kind.in_(kinds))
    if destination:
        query = query.where(GuideArticle.destination_id == destination.casefold())
    if country:
        ids = [profile.id for profile in destinations_in_country(country)]
        if not ids:
            return PublicList(articles=[], next_cursor=None)
        query = query.where(GuideArticle.destination_id.in_(ids))
    if topic_ids:
        # The parent's id and its children's: an article filed under ``ai-terms`` answers
        # the ``ai`` filter without also having to carry ``ai``.
        query = query.where(
            GuideArticle.id.in_(
                select(GuideArticleTopic.article_id).where(
                    GuideArticleTopic.topic_id.in_(topic_ids)
                )
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
    topics = await _topic_options_for(session, [article.id for article, _ in rows], locale)
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
                topics=topics.get(article.id, []),
                title=published.title,
                description=published.description,
                hero=published.hero,
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
    topics = (await _topic_options_for(session, [article.id], locale)).get(article.id, [])
    expired = not article_is_live(article)
    document = await _published_document(session, row)
    return PublicArticle(
        slug=article.slug,
        kind=cast(Kind, article.kind),
        locale=locale,
        status="published",
        destination_id=article.destination_id,
        destination_label=destination_label(article.destination_id, locale),
        topics=topics,
        valid_until=article.valid_until,
        expired=expired,
        document=document,
        published_locales=[item for item in LOCALES if item in set(published_locales)],
        partner_links=[] if expired or document is None else partner_link_views(document),
        article_links=[]
        if document is None
        else await resolve_article_links(session, locale, document),
        series=None if expired else await article_navigation(session, kind, slug, locale),
    )


async def destination_facets(
    session: AsyncSession, locale: Locale, section: Section | None = None
) -> DestinationFacetList:
    """Every destination with a published article in ``locale``, with its country and how
    many articles it has, for the travel hub's "browse by destination" block.

    Counted per locale rather than per article: a city whose only guide is Japanese has
    nothing to show a Korean reader, and a pill that leads to an empty list is worse than
    no pill. Ordered by catalog position, which already groups cities by country.
    """
    kinds = kind_filter(None, section)
    query = (
        select(GuideArticle.destination_id, GuideArticle.id)
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .where(
            GuideArticleLocale.locale == locale,
            GuideArticle.destination_id.is_not(None),
            *published_filters(),
        )
    )
    if kinds is not None:
        if not kinds:
            return DestinationFacetList(destinations=[])
        query = query.where(GuideArticle.kind.in_(kinds))
    rows = await session.execute(query)
    articles: dict[str, set[UUID]] = {}
    for destination_id, article_id in rows:
        articles.setdefault(destination_id, set()).add(article_id)
    facets = [
        DestinationFacet(
            id=profile.id,
            label=city_name(profile, locale),
            country=country_slug(profile.country),
            country_label=country_label(profile, locale),
            count=len(articles[profile.id]),
        )
        for profile in DESTINATIONS
        if profile.id in articles
    ]
    return DestinationFacetList(destinations=facets)


# --- partner links ------------------------------------------------------------


def placement_for(kind: Kind) -> Literal["guide", "life"]:
    """The surface label a click from this article is recorded under, shared with offers."""
    return "life" if kind == "life" else "guide"


def partner_link_views(document: GuideDocument) -> list[PublicPartnerLink]:
    """The partner links in ``document`` a reader may see: a known partner, a URL on its hosts.

    Resolved on every read rather than trusted from the stored revision, so a program
    removed from the registry leaves every article at once. Two blocks with the same URL
    are the same link and share one entry and one key.
    """
    views: dict[str, PublicPartnerLink] = {}
    for block in document.blocks:
        if not isinstance(block, PartnerLinkBlock):
            continue
        if partner_link_problem(block.partner, block.url) is not None:
            continue
        key = link_key(block.url)
        views.setdefault(
            key,
            PublicPartnerLink(
                key=key,
                partner=block.partner,
                display_name=PARTNERS_BY_CODE[block.partner].display_name,
                url=block.url,
            ),
        )
    return list(views.values())


async def _visible_partner_link(
    session: AsyncSession, kind: Kind, slug: str, locale: Locale, key: str
) -> tuple[GuideArticle, PublicPartnerLink] | None:
    article = await session.scalar(
        select(GuideArticle).where(GuideArticle.slug == slug.casefold(), GuideArticle.kind == kind)
    )
    if article is None or not article.is_active or not article_is_live(article):
        return None
    row = await session.scalar(
        select(GuideArticleLocale).where(
            GuideArticleLocale.article_id == article.id, GuideArticleLocale.locale == locale
        )
    )
    document = await _published_document(session, row) if row is not None else None
    if document is None:
        return None
    view = next((item for item in partner_link_views(document) if item.key == key), None)
    return (article, view) if view is not None else None


async def record_partner_click(
    session: AsyncSession, kind: Kind, slug: str, locale: Locale, key: str
) -> None:
    """Count one click on a partner link the reader could actually see.

    The link is looked up in the article's currently published translation, never taken
    from the request, so the endpoint cannot log a click for a partner or URL the article
    does not carry. Drafts, hidden and expired articles, and links since removed all answer
    404. Nothing about the reader is stored: no user, no trip, no search.
    """
    found = await _visible_partner_link(session, kind, slug, locale, key)
    if found is None:
        raise AppError(404, "affiliate_link_not_found", "找不到合作連結")
    article, view = found
    partner = PARTNERS_BY_CODE[view.partner]
    placement = placement_for(kind)
    session.add(
        AffiliateClick(
            user_id=None,
            partner=partner.code,
            brand=partner.code,
            module=partner.category,
            placement=placement,
            destination_id=None,
            # The article that placed the link, until affiliate_clicks has a column of its own
            # (2026-09-12-attribute-affiliate-clicks-to-the-guide). The table is append-only,
            # so waiting for the column would lose this attribution for good.
            destination_summary=article.slug[:128],
            sub_id=coarse_sub_id("cnt", partner.category, None, locale, placement),
            target_host=(urlsplit(view.url).hostname or "")[:255],
            status="clicked",
        )
    )
    await session.commit()


def _encode_sitemap_cursor(published_at: datetime, slug: str, locale: str) -> str:
    """The sitemap's row grain is (article, locale), so its keyset carries one key more than
    the listing's; the encoding is otherwise the same, and just as opaque to the caller."""
    raw = json.dumps([published_at.isoformat(), slug, locale], separators=(",", ":"))
    return base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")


def _decode_sitemap_cursor(cursor: str | None) -> tuple[datetime, str, str] | None:
    if not cursor:
        return None
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        stamp, slug, locale = json.loads(base64.urlsafe_b64decode(padded.encode()).decode())
        return datetime.fromisoformat(stamp), str(slug), str(locale)
    except (ValueError, TypeError):
        raise AppError(422, "guide_cursor_invalid", "分頁資訊無效，請重新瀏覽") from None


async def _published_locales(
    session: AsyncSession, article_ids: set[UUID]
) -> dict[UUID, list[Locale]]:
    """Every locale each article is published in, in the site's own locale order."""
    if not article_ids:
        return {}
    rows = await session.execute(
        select(GuideArticleLocale.article_id, GuideArticleLocale.locale)
        .join(GuideArticle, GuideArticle.id == GuideArticleLocale.article_id)
        .where(GuideArticleLocale.article_id.in_(article_ids), *published_filters())
    )
    found: dict[UUID, set[str]] = {}
    for article_id, locale in rows:
        found.setdefault(article_id, set()).add(locale)
    return {
        article_id: [item for item in LOCALES if item in locales]
        for article_id, locales in found.items()
    }


async def sitemap_entries(
    session: AsyncSession,
    *,
    section: Section | None = None,
    locale: Locale | None = None,
    cursor: str | None = None,
    limit: int = SITEMAP_LIMIT,
) -> SitemapList:
    """Publication-aware enumeration for ``apps/web/app/sitemap.ts``, one page at a time.

    Only rows that the list and the article page would also serve. Expired intel and
    withdrawn translations leave here at the same moment they leave the site.

    The web splits the sitemap into one child per section and locale, so both filters exist;
    a page holds at most ``SITEMAP_LIMIT`` rows and the caller follows ``next_cursor`` until
    it is None. Newest first, with the slug and the locale as tiebreakers: a batch import
    publishes dozens of rows in the same second, and a keyset on the timestamp alone would
    repeat or skip them across pages.
    """
    kinds = kind_filter(None, section)
    size = min(max(limit, 1), SITEMAP_LIMIT)
    # The current public version's own timestamp rides along as ``modified_at``: the same
    # predicate ``_published_document`` resolves the pointer with, as an outer join so a
    # damaged pointer costs that row its lastmod rather than its place in the file.
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
        .outerjoin(
            GuideArticleRevision,
            and_(
                GuideArticleRevision.article_locale_id == GuideArticleLocale.id,
                GuideArticleRevision.version == GuideArticleLocale.published_version,
                GuideArticleRevision.action == "published",
            ),
        )
        .where(GuideArticleLocale.published_at.is_not(None), *published_filters())
    )
    if kinds:
        query = query.where(GuideArticle.kind.in_(kinds))
    if locale:
        query = query.where(GuideArticleLocale.locale == locale)
    position = _decode_sitemap_cursor(cursor)
    if position is not None:
        stamp, after_slug, after_locale = position
        query = query.where(
            or_(
                GuideArticleLocale.published_at < stamp,
                and_(GuideArticleLocale.published_at == stamp, GuideArticle.slug > after_slug),
                and_(
                    GuideArticleLocale.published_at == stamp,
                    GuideArticle.slug == after_slug,
                    GuideArticleLocale.locale > after_locale,
                ),
            )
        )
    rows = list(
        await session.execute(
            query.order_by(
                GuideArticleLocale.published_at.desc(),
                GuideArticle.slug,
                GuideArticleLocale.locale,
            ).limit(size + 1)
        )
    )
    has_more = len(rows) > size
    rows = rows[:size]
    locales = await _published_locales(session, {article_id for article_id, *_ in rows})
    entries = [
        SitemapEntry(
            kind=cast(Kind, kind),
            slug=slug,
            locale=cast(Locale, row_locale),
            published_at=published_at,
            modified_at=modified_at or published_at,
            locales=locales.get(article_id, [cast(Locale, row_locale)]),
        )
        for article_id, kind, slug, row_locale, published_at, modified_at in rows
    ]
    last = rows[-1] if rows and has_more else None
    return SitemapList(
        entries=entries,
        next_cursor=_encode_sitemap_cursor(last[4], last[2], last[3]) if last else None,
    )


async def sitemap_summary(session: AsyncSession) -> SitemapSummary:
    """Published rows per kind and locale, from the same predicate the enumeration uses, so
    the index can list only the children that have something and a section hub can tell
    which languages publish it -- one grouped query instead of paging every row."""
    rows = await session.execute(
        select(GuideArticle.kind, GuideArticleLocale.locale, func.count())
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
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
