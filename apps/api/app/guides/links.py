"""The links between articles: what an article points at, what points at it, and what
to read next.

Three sources feed one table (``guide_article_links``). ``inline`` rows are written when a
translation is published, from the ``article`` inlines of its published text, and deleted
when it is withdrawn -- the same transaction that moves the published pointer, so the
graph can never say what the pointer does not. ``related`` rows are the editor's picks on
the identity, replaced whole like topics. The reading list starts with those picks, then
nearby coverage of the same subject for dated AI and tech news. It fills remaining slots
from the sub-topic, parent topic, destination and series group in that order. The "cited by"
list is the inline rows pointing here.

Whether a target may be *shown* is decided at read time by ``published_filters``, never by
the table: a row records that the link exists, and a withdrawn or hidden target leaves
every list the moment it is withdrawn.

Everything raised from here is a sentence a reader can be shown (``app/i18n.py``).
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from datetime import date
from difflib import SequenceMatcher
from typing import Any, cast
from uuid import UUID

from sqlalchemy import ColumnElement, Row, Select, and_, delete, select
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
NEWS_WINDOW_DAYS = 5


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


def _published_references(locale: Locale) -> Select[UUID, str, str, Any, Any]:
    """Select just the card fields from the visible translation's published revision."""
    return (
        select(
            GuideArticle.id,
            GuideArticle.kind,
            GuideArticle.slug,
            GuideArticleRevision.document_json["title"],
            GuideArticleRevision.document_json["description"],
        )
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .join(
            GuideArticleRevision,
            and_(
                GuideArticleRevision.article_locale_id == GuideArticleLocale.id,
                GuideArticleRevision.version == GuideArticleLocale.published_version,
                GuideArticleRevision.action == "published",
            ),
        )
        .where(GuideArticleLocale.locale == locale, *published_filters())
    )


def _read_references(
    rows: Iterable[Row[UUID, str, str, Any, Any]],
) -> dict[UUID, ArticleReference]:
    found: dict[UUID, ArticleReference] = {}
    for article_id, kind, slug, title, description in rows:
        if not isinstance(title, str) or not title:
            continue
        found[article_id] = ArticleReference(
            kind=cast(Kind, kind),
            slug=slug,
            title=title,
            description=description if isinstance(description, str) and description else None,
        )
    return found


async def references_for(
    session: AsyncSession, locale: Locale, article_ids: list[UUID]
) -> dict[UUID, ArticleReference]:
    """Absent, damaged or withdrawn translations have no card."""
    if not article_ids:
        return {}
    rows = await session.execute(
        _published_references(locale).where(GuideArticle.id.in_(article_ids))
    )
    return _read_references(rows)


def _has_topics(topic_ids: Sequence[UUID] | Select[UUID]) -> ColumnElement[bool]:
    return GuideArticle.id.in_(
        select(GuideArticleTopic.article_id).where(GuideArticleTopic.topic_id.in_(topic_ids))
    )


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


def _news_terms(slug: str, topic: str) -> list[str]:
    prefix = f"{topic}-"
    stem, _, stamp = slug.removeprefix(prefix).rpartition("-")
    if not slug.startswith(prefix) or len(stamp) != 8 or not stamp.isdigit():
        return []
    return stem.split("-")


def _subject_overlap(terms: list[str], other: list[str]) -> int:
    """A shared subject phrase starts at the beginning of at least one headline slug."""
    a, b, size = SequenceMatcher(None, terms, other, autojunk=False).find_longest_match()
    if size < 3 or (a and b) or sum(word.isalpha() for word in terms[a : a + size]) < 2:
        return 0
    # Two releases of e.g. claude-code-2-1 with different patch numbers are distinct.
    if a + size < len(terms) and b + size < len(other):
        if all(any(c.isdigit() for c in word) for word in (terms[a + size], other[b + size])):
            return 0
    return size


async def _news_followups(
    session: AsyncSession, article: GuideArticle, locale: Locale, topic: str, topic_id: UUID
) -> list[UUID]:
    day = article.news_date
    terms = _news_terms(article.slug, topic)
    if day is None or len(terms) < 3:
        return []
    earliest = date.fromordinal(max(1, day.toordinal() - NEWS_WINDOW_DAYS))
    latest = date.fromordinal(min(date.max.toordinal(), day.toordinal() + NEWS_WINDOW_DAYS))
    rows = await session.execute(
        select(GuideArticle.id, GuideArticle.slug, GuideArticle.news_date)
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .where(
            GuideArticle.id != article.id,
            GuideArticle.kind == "life",
            GuideArticle.news_date.between(earliest, latest),
            _has_topics([topic_id]),
            GuideArticleLocale.locale == locale,
            *published_filters(),
        )
        .order_by(GuideArticleLocale.published_at.desc(), GuideArticle.slug)
    )
    matches = []
    for article_id, slug, other_day in rows:
        score = _subject_overlap(terms, _news_terms(slug, topic))
        if score and other_day is not None:
            matches.append((-score, abs((day - other_day).days), article_id))
    # Stable for equal strength and distance: publication order, then slug as above.
    matches.sort(key=lambda match: match[:2])
    return [article_id for _, _, article_id in matches]


async def related_articles(
    session: AsyncSession, article: GuideArticle, locale: Locale, *, limit: int = RELATED_LIMIT
) -> list[ArticleReference]:
    """Editor's picks, close news follow-ups, sub-topic, parent, destination, then series."""
    if limit <= 0:
        return []
    picked: list[ArticleReference] = []
    seen = {article.id}

    async def take_ranked(candidates: Sequence[UUID]) -> None:
        pending = [key for key in dict.fromkeys(candidates) if key not in seen]
        offset = 0
        while offset < len(pending) and len(picked) < limit:
            batch = pending[offset : offset + limit - len(picked)]
            found = await references_for(session, locale, batch)
            picked.extend(found[key] for key in batch if key in found)
            seen.update(batch)
            offset += len(batch)

    async def take_newest(condition: ColumnElement[bool]) -> None:
        # One published locale per article. A later tier runs only if earlier ones left room.
        query = (
            _published_references(locale)
            .where(condition)
            .order_by(GuideArticleLocale.published_at.desc(), GuideArticle.slug)
        )
        while len(picked) < limit:
            size = limit - len(picked)
            page = (
                await session.execute(query.where(GuideArticle.id.not_in(seen)).limit(size))
            ).all()
            picked.extend(_read_references(page).values())
            seen.update(row[0] for row in page)
            if len(page) < size:
                break

    curated = await session.scalars(
        select(GuideArticleLink.target_article_id)
        .where(
            GuideArticleLink.source_article_id == article.id,
            GuideArticleLink.relation == "related",
        )
        .order_by(GuideArticleLink.position)
    )
    await take_ranked(curated.all())
    if len(picked) == limit:
        return picked

    topics = (
        await session.execute(
            select(GuideTopic.id, GuideTopic.slug, GuideTopic.parent_id)
            .join(GuideArticleTopic, GuideArticleTopic.topic_id == GuideTopic.id)
            .where(GuideArticleTopic.article_id == article.id)
        )
    ).all()
    children = {slug: key for key, slug, parent in topics if parent is not None}
    if article.kind == "life" and article.news_date:
        for topic in ("ai-news", "tech-news"):
            if topic in children and article.slug.startswith(f"{topic}-"):
                await take_ranked(
                    await _news_followups(session, article, locale, topic, children[topic])
                )
                break
    if len(picked) < limit and children:
        await take_newest(_has_topics(list(children.values())))
    if len(picked) < limit and topics:
        parents = {parent or key for key, _, parent in topics}
        family = select(GuideTopic.id).where(
            GuideTopic.id.in_(parents) | GuideTopic.parent_id.in_(parents)
        )
        await take_newest(_has_topics(family))
    if len(picked) < limit and article.destination_id:
        await take_newest(GuideArticle.destination_id == article.destination_id)
    if len(picked) < limit and article.kind == "life":
        catalogue = catalogue_for_article(article.slug, locale)
        if catalogue is not None:
            lesson = next(
                (entry for entry in catalogue.entries if entry.slug == article.slug), None
            )
            if lesson is not None:
                group = [entry.slug for entry in catalogue.entries if entry.group == lesson.group]
                await take_ranked(await _by_slugs(session, locale, group))
    return picked


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
