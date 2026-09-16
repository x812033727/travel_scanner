"""The links between articles: what an article points at, what points at it, and what
to read next.

Three sources feed one table (``guide_article_links``). ``inline`` rows are written when a
translation is published, from the ``article`` inlines of its published text, and deleted
when it is withdrawn -- the same transaction that moves the published pointer, so the
graph can never say what the pointer does not. ``related`` rows are the editor's picks on
the identity, replaced whole like topics. The reading list at the end of an article is
those picks first, then the articles that share a sub-topic, a parent topic, a destination
or a series group; the "cited by" list is the inline rows pointing here.

Whether a target may be *shown* is decided at read time by ``published_filters``, never by
the table: a row records that the link exists, and a withdrawn or hidden target leaves
every list the moment it is withdrawn.

Everything raised from here is a sentence a reader can be shown (``app/i18n.py``).
"""

from __future__ import annotations

from typing import Any, cast
from uuid import UUID

from sqlalchemy import and_, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.guides.models import (
    GuideArticle,
    GuideArticleLink,
    GuideArticleLocale,
    GuideArticleRevision,
    GuideArticleTopic,
    GuideTopic,
)
from app.guides.publication import published_filters
from app.guides.schemas import (
    ArticleInline,
    ArticleReference,
    GuideDocument,
    Kind,
    RichParagraphBlock,
)
from app.guides.series import catalogue_for_article
from app.i18n import Locale
from app.problems import AppError

RELATED_LIMIT = 4
BACKLINK_LIMIT = 8


# --- the document's own links ----------------------------------------------------


def inline_targets(document: GuideDocument) -> list[tuple[Kind, str]]:
    """The articles the text links to, in reading order, each once."""
    seen: list[tuple[Kind, str]] = []
    for block in document.blocks:
        if not isinstance(block, RichParagraphBlock):
            continue
        for node in block.inlines:
            if isinstance(node, ArticleInline) and (node.kind, node.slug) not in seen:
                seen.append((node.kind, node.slug))
    return seen


async def _ids_by_slug(session: AsyncSession, slugs: set[str]) -> dict[tuple[str, str], UUID]:
    if not slugs:
        return {}
    rows = await session.execute(
        select(GuideArticle.id, GuideArticle.kind, GuideArticle.slug).where(
            GuideArticle.slug.in_(sorted(slugs))
        )
    )
    return {(kind, slug): article_id for article_id, kind, slug in rows}


async def materialize_inline(
    session: AsyncSession, article_id: UUID, locale: str, document: GuideDocument
) -> list[str]:
    """Replace the translation's inline rows with the links in ``document``. Returns the
    targets that name no article at all (``kind/slug``), for the audit row: a link to an
    article that is merely unpublished resolves and is kept, since publishing the target
    later completes it without a republication here."""
    targets = inline_targets(document)
    found = await _ids_by_slug(session, {slug for _, slug in targets})
    await drop_inline(session, article_id, locale)
    unresolved: list[str] = []
    position = 0
    for kind, slug in targets:
        target = found.get((kind, slug))
        if target is None:
            unresolved.append(f"{kind}/{slug}")
            continue
        if target == article_id:
            continue
        session.add(
            GuideArticleLink(
                source_article_id=article_id,
                target_article_id=target,
                locale=locale,
                relation="inline",
                position=position,
            )
        )
        position += 1
    return unresolved


async def drop_inline(session: AsyncSession, article_id: UUID, locale: str) -> None:
    await session.execute(
        delete(GuideArticleLink).where(
            GuideArticleLink.source_article_id == article_id,
            GuideArticleLink.locale == locale,
            GuideArticleLink.relation == "inline",
        )
    )


# --- the editor's picks ----------------------------------------------------------


async def resolve_related(
    session: AsyncSession, article: GuideArticle, slugs: list[str]
) -> list[GuideArticle]:
    """The articles the slugs name, in the editor's order. An unknown slug is refused
    rather than dropped: a pick that silently vanished is a pick nobody notices."""
    wanted = list(dict.fromkeys(slug.strip().casefold() for slug in slugs if slug.strip()))
    if not wanted:
        return []
    if article.slug in wanted:
        raise AppError(422, "guide_related_self", "文章不能把自己列為延伸閱讀")
    rows = {
        row.slug: row
        for row in await session.scalars(select(GuideArticle).where(GuideArticle.slug.in_(wanted)))
    }
    missing = [slug for slug in wanted if slug not in rows]
    if missing:
        raise AppError(422, "guide_related_unknown", "延伸閱讀指定的文章不存在")
    return [rows[slug] for slug in wanted]


async def set_related(
    session: AsyncSession, article: GuideArticle, targets: list[GuideArticle]
) -> None:
    await session.execute(
        delete(GuideArticleLink).where(
            GuideArticleLink.source_article_id == article.id,
            GuideArticleLink.relation == "related",
        )
    )
    for position, target in enumerate(targets):
        session.add(
            GuideArticleLink(
                source_article_id=article.id,
                target_article_id=target.id,
                locale=None,
                relation="related",
                position=position,
            )
        )


async def related_slugs(session: AsyncSession, article_ids: list[UUID]) -> dict[UUID, list[str]]:
    if not article_ids:
        return {}
    rows = await session.execute(
        select(GuideArticleLink.source_article_id, GuideArticle.slug)
        .join(GuideArticle, GuideArticle.id == GuideArticleLink.target_article_id)
        .where(
            GuideArticleLink.source_article_id.in_(article_ids),
            GuideArticleLink.relation == "related",
        )
        .order_by(GuideArticleLink.position)
    )
    grouped: dict[UUID, list[str]] = {}
    for source, slug in rows:
        grouped.setdefault(source, []).append(slug)
    return grouped


# --- reading them back ------------------------------------------------------------


async def references_for(
    session: AsyncSession, locale: Locale, article_ids: list[UUID]
) -> dict[UUID, ArticleReference]:
    """References for the articles published in ``locale``, titled and described from
    their published revision. An article that is hidden, expired, unpublished here or
    whose pointer is damaged is simply absent: a reading list degrades, it never 503s."""
    if not article_ids:
        return {}
    rows = await session.execute(
        select(GuideArticle, GuideArticleRevision.document_json)
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .outerjoin(
            GuideArticleRevision,
            and_(
                GuideArticleRevision.article_locale_id == GuideArticleLocale.id,
                GuideArticleRevision.version == GuideArticleLocale.published_version,
                GuideArticleRevision.action == "published",
            ),
        )
        .where(
            GuideArticle.id.in_(article_ids),
            GuideArticleLocale.locale == locale,
            *published_filters(),
        )
    )
    found: dict[UUID, ArticleReference] = {}
    for article, document_json in rows:
        title = document_json.get("title") if isinstance(document_json, dict) else None
        if not isinstance(title, str) or not title:
            continue
        description = document_json.get("description")
        found[article.id] = ArticleReference(
            kind=cast(Kind, article.kind),
            slug=article.slug,
            title=title,
            description=description if isinstance(description, str) and description else None,
        )
    return found


def _published_ids(locale: Locale) -> Any:
    """Article ids published in ``locale``, newest first, as a select to narrow further."""
    return (
        select(GuideArticle.id, func.max(GuideArticleLocale.published_at).label("published_at"))
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .where(GuideArticleLocale.locale == locale, *published_filters())
        .group_by(GuideArticle.id)
        .order_by(func.max(GuideArticleLocale.published_at).desc(), GuideArticle.slug)
    )


async def _by_topics(session: AsyncSession, locale: Locale, topic_ids: list[UUID]) -> list[UUID]:
    if not topic_ids:
        return []
    query = _published_ids(locale).where(
        GuideArticle.id.in_(
            select(GuideArticleTopic.article_id).where(GuideArticleTopic.topic_id.in_(topic_ids))
        )
    )
    return [article_id for article_id, _ in await session.execute(query)]


async def _by_destination(session: AsyncSession, locale: Locale, destination_id: str) -> list[UUID]:
    query = _published_ids(locale).where(GuideArticle.destination_id == destination_id)
    return [article_id for article_id, _ in await session.execute(query)]


async def _by_slugs(session: AsyncSession, locale: Locale, slugs: list[str]) -> list[UUID]:
    if not slugs:
        return []
    rows = await session.execute(
        select(GuideArticle.id, GuideArticle.slug)
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .where(
            GuideArticle.slug.in_(slugs), GuideArticleLocale.locale == locale, *published_filters()
        )
    )
    by_slug = {slug: article_id for article_id, slug in rows}
    return [by_slug[slug] for slug in slugs if slug in by_slug]


async def _topic_family(session: AsyncSession, article_id: UUID) -> tuple[list[UUID], list[UUID]]:
    """The article's sub-topics, and the whole family of its parents (the parents
    themselves and every sub-topic under them)."""
    topics = list(
        await session.scalars(
            select(GuideTopic)
            .join(GuideArticleTopic, GuideArticleTopic.topic_id == GuideTopic.id)
            .where(GuideArticleTopic.article_id == article_id)
        )
    )
    children = [topic.id for topic in topics if topic.parent_id is not None]
    parents = list(
        dict.fromkeys(
            [topic.parent_id for topic in topics if topic.parent_id is not None]
            + [topic.id for topic in topics if topic.parent_id is None]
        )
    )
    if not parents:
        return children, []
    family = list(
        await session.scalars(
            select(GuideTopic.id).where(
                (GuideTopic.id.in_(parents)) | (GuideTopic.parent_id.in_(parents))
            )
        )
    )
    return children, family


async def related_articles(
    session: AsyncSession, article: GuideArticle, locale: Locale, *, limit: int = RELATED_LIMIT
) -> list[ArticleReference]:
    """What to read next: the editor's picks, then the nearest published neighbours.

    Tiers, each newest first, each skipping what an earlier tier already chose and the
    article itself: curated ``related`` rows; articles sharing a sub-topic; articles under
    the same parent topic; articles about the same destination; the other lessons of the
    same series group. Only visible articles count, so an editor's pick that is withdrawn
    makes room for a neighbour rather than leaving a gap.
    """
    chosen: list[UUID] = []

    def take(candidates: list[UUID]) -> None:
        for candidate in candidates:
            if candidate != article.id and candidate not in chosen:
                chosen.append(candidate)

    curated = await session.scalars(
        select(GuideArticleLink.target_article_id)
        .where(
            GuideArticleLink.source_article_id == article.id,
            GuideArticleLink.relation == "related",
        )
        .order_by(GuideArticleLink.position)
    )
    take(list(curated))
    references = await references_for(session, locale, chosen)
    picked = [article_id for article_id in chosen if article_id in references]
    if len(picked) < limit:
        children, family = await _topic_family(session, article.id)
        tiers: list[list[UUID]] = [
            await _by_topics(session, locale, children),
            await _by_topics(session, locale, family),
            await _by_destination(session, locale, article.destination_id)
            if article.destination_id
            else [],
        ]
        if article.kind == "life":
            catalogue = catalogue_for_article(article.slug, locale)
            lesson = (
                next((entry for entry in catalogue.entries if entry.slug == article.slug), None)
                if catalogue is not None
                else None
            )
            if catalogue is not None and lesson is not None:
                tiers.append(
                    await _by_slugs(
                        session,
                        locale,
                        [
                            entry.slug
                            for entry in catalogue.entries
                            if entry.group == lesson.group and entry.slug != article.slug
                        ],
                    )
                )
        for tier in tiers:
            take(tier)
        references = await references_for(session, locale, chosen)
        picked = [article_id for article_id in chosen if article_id in references]
    return [references[article_id] for article_id in picked[:limit]]


async def backlinks(
    session: AsyncSession, article_id: UUID, locale: Locale, *, limit: int = BACKLINK_LIMIT
) -> list[ArticleReference]:
    """The published articles whose text links here, newest first."""
    rows = await session.execute(
        select(GuideArticleLink.source_article_id)
        .join(GuideArticle, GuideArticle.id == GuideArticleLink.source_article_id)
        .join(
            GuideArticleLocale,
            and_(
                GuideArticleLocale.article_id == GuideArticle.id,
                GuideArticleLocale.locale == GuideArticleLink.locale,
            ),
        )
        .where(
            GuideArticleLink.target_article_id == article_id,
            GuideArticleLink.locale == locale,
            GuideArticleLink.relation == "inline",
            *published_filters(),
        )
        .order_by(GuideArticleLocale.published_at.desc(), GuideArticle.slug)
        .limit(limit)
    )
    sources = [source for (source,) in rows]
    references = await references_for(session, locale, sources)
    return [references[source] for source in sources if source in references]
