"""Searching published articles: the index rows, how they are kept, and the query.

The corpus is a few thousand documents in five languages, three of which cannot be
tokenised by ``to_tsvector``. So the match is a substring one: every term the query is
parsed into must appear in a folded copy of the article's text, and the rows that match
are ranked by *where* they match (title, then an alias, the description, a heading, the
body). The fold is NFKC plus casefold, applied to the text at write time and to the query
at read time, which is what lets a full-width ``ＡＩ`` find ``AI`` and ``Machine Learning``
find ``machine learning`` on SQLite and PostgreSQL alike; ``ILIKE`` would not, since
SQLite has no ILIKE and its ``lower()`` stops at ASCII.

Everything raised from here is a sentence a reader can be shown (``app/i18n.py``,
``_GUIDE_ERRORS``); the operator-only paths live in ``admin_service``.
"""

from __future__ import annotations

import operator
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import reduce
from typing import Any, cast
from uuid import UUID

from sqlalchemy import ColumnElement, Select, and_, case, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from app.db import escape_like
from app.guides.models import (
    GuideArticle,
    GuideArticleAlias,
    GuideArticleLocale,
    GuideArticleTopic,
    GuideSearchEntry,
)
from app.guides.publication import published_filters
from app.guides.schemas import (
    GuideDocument,
    GuideSearchHit,
    GuideSearchResult,
    HeroImage,
    Kind,
    PublicSummary,
    Section,
)
from app.guides.service import (
    _published_document,
    _topic_options_for,
    destination_label,
    destinations_in_country,
    kind_filter,
)
from app.guides.taxonomy import topic_ids_including_children
from app.i18n import Locale
from app.problems import AppError

MAX_QUERY_LENGTH = 100
MAX_TERMS = 6
MAX_LIMIT = 20
MAX_OFFSET = 200
SNIPPET_RADIUS = 60
DESCRIPTION_SNIPPET = 120

# Where a term matches decides its weight; the body is the floor every match clears.
TITLE_WEIGHT = 8
ALIAS_WEIGHT = 6
DESCRIPTION_WEIGHT = 4
HEADING_WEIGHT = 3
BODY_WEIGHT = 1

# Whitespace and the punctuation a reader separates words with, in ASCII and in the
# full-width forms a CJK keyboard produces. ``.``, ``-``, ``_``, ``+`` and ``#`` stay inside
# a term: ``Next.js``, ``GPT-4``, ``C++`` and ``C#`` are names.
_SEPARATORS = re.compile(r"[\s,，、。；;：:！!？?（）()\[\]【】「」『』《》〈〉\"'“”‘’/／|｜~～*]+")


def normalize(text: str) -> str:
    """The one fold both the index and the query go through."""
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def readable(text: str) -> str:
    """NFKC and whitespace folding without the casefold: the snippet keeps its capitals."""
    return " ".join(unicodedata.normalize("NFKC", text).split())


# --- what an article says -----------------------------------------------------


@dataclass
class DocumentText:
    title: str
    description: str
    headings: list[str] = field(default_factory=list)
    body: list[str] = field(default_factory=list)


def document_text(document: GuideDocument) -> DocumentText:
    """Every reader-visible string of a document, by the weight it carries.

    Block by block rather than a walk over the JSON, so a field that is not prose (a URL, a
    code listing, an image path, a partner code) never leaks into the match. New block
    types are a ``mypy`` error here until they say what they contribute.
    """
    text = DocumentText(title=document.title, description=document.description)
    if document.hero is not None:
        text.body.append(document.hero.alt)
    for block in document.blocks:
        if block.type == "heading":
            text.headings.append(block.text)
        elif block.type == "paragraph":
            text.body.append(block.text)
        elif block.type == "rich_paragraph":
            # Inline nodes keep their own spacing, so they join without a separator.
            text.body.append("".join(node.text for node in block.inlines))
        elif block.type == "list":
            text.body.extend(block.items)
        elif block.type == "link":
            text.body.append(block.text)
        elif block.type == "image":
            text.body.extend(part for part in (block.alt, block.caption) if part)
        elif block.type == "table":
            text.body.extend(block.header)
            text.body.extend(cell for row in block.rows for cell in row if cell)
            if block.caption:
                text.body.append(block.caption)
        elif block.type == "callout":
            text.body.extend(part for part in (block.title, block.text) if part)
        elif block.type == "code":
            # The label, never the listing: nobody searches for a line of shell.
            text.body.append(block.label)
        elif block.type == "offer":
            if block.heading:
                text.body.append(block.heading)
        elif block.type == "partner_link":
            text.body.extend(part for part in (block.label, block.note) if part)
    text.body.extend(source.title for source in document.sources)
    return text


def entry_values(
    text: DocumentText,
    hero: HeroImage | None,
    aliases: list[str],
    *,
    version: int,
    published_at: datetime,
) -> dict[str, Any]:
    """The column values of one index row. ``aliases`` are already folded."""
    title_norm = normalize(text.title)
    description_norm = normalize(text.description)
    headings_norm = normalize(" ".join(text.headings))
    aliases_norm = " ".join(sorted(set(aliases)))
    body_text = readable(" ".join(text.body))
    return {
        "revision_version": version,
        "title": text.title,
        "description": text.description,
        "title_norm": title_norm,
        "description_norm": description_norm,
        "headings_norm": headings_norm,
        "aliases_norm": aliases_norm,
        "body_text": body_text,
        "search_text": search_text(
            title_norm, aliases_norm, description_norm, headings_norm, body_text
        ),
        "hero_json": hero.model_dump(mode="json") if hero is not None else None,
        "published_at": published_at,
        "indexed_at": datetime.now(UTC),
    }


def search_text(
    title_norm: str, aliases_norm: str, description_norm: str, headings_norm: str, body_text: str
) -> str:
    parts = (title_norm, aliases_norm, description_norm, headings_norm, body_text.casefold())
    return " ".join(part for part in parts if part)


# --- keeping the index ---------------------------------------------------------


async def article_aliases(session: AsyncSession, article_id: UUID, locale: str) -> list[str]:
    rows = await session.scalars(
        select(GuideArticleAlias.alias_norm).where(
            GuideArticleAlias.article_id == article_id, GuideArticleAlias.locale == locale
        )
    )
    return list(rows)


async def index_locale(
    session: AsyncSession,
    article_id: UUID,
    locale: str,
    document: GuideDocument,
    *,
    version: int,
    published_at: datetime,
) -> GuideSearchEntry:
    """Write or rewrite the row for one published translation. Not committed here: the
    caller owns the transaction, and on the publish path that is the same one that moves
    the published pointer, so the index can never say what the pointer does not."""
    values = entry_values(
        document_text(document),
        document.hero,
        await article_aliases(session, article_id, locale),
        version=version,
        published_at=published_at,
    )
    entry = await session.scalar(
        select(GuideSearchEntry).where(
            GuideSearchEntry.article_id == article_id, GuideSearchEntry.locale == locale
        )
    )
    if entry is None:
        entry = GuideSearchEntry(article_id=article_id, locale=locale, **values)
        session.add(entry)
    else:
        for column, value in values.items():
            setattr(entry, column, value)
    return entry


async def drop_locale(session: AsyncSession, article_id: UUID, locale: str) -> None:
    await session.execute(
        delete(GuideSearchEntry).where(
            GuideSearchEntry.article_id == article_id, GuideSearchEntry.locale == locale
        )
    )


async def refresh_aliases(session: AsyncSession, article_id: UUID, locale: str) -> bool:
    """Rebuild the alias columns of an existing row after its aliases changed, without
    re-reading the revision. False when the translation is not indexed (not published)."""
    entry = await session.scalar(
        select(GuideSearchEntry).where(
            GuideSearchEntry.article_id == article_id, GuideSearchEntry.locale == locale
        )
    )
    if entry is None:
        return False
    entry.aliases_norm = " ".join(sorted(set(await article_aliases(session, article_id, locale))))
    entry.search_text = search_text(
        entry.title_norm,
        entry.aliases_norm,
        entry.description_norm,
        entry.headings_norm,
        entry.body_text,
    )
    entry.indexed_at = datetime.now(UTC)
    return True


async def reindex_all(session: AsyncSession) -> dict[str, int]:
    """Rebuild the whole index from the published revisions, and drop the rows no
    published translation backs. Idempotent: a row already at the published version is
    left alone, so a re-run after a partial failure finishes the work rather than
    repeating it. Hidden and expired articles are indexed too -- the query filters them,
    and unhiding one must not wait for a republication."""
    rows = await session.execute(
        select(GuideArticle, GuideArticleLocale)
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .where(GuideArticleLocale.published_version.is_not(None))
        .order_by(GuideArticle.slug, GuideArticleLocale.locale)
    )
    existing = {
        (entry.article_id, entry.locale): entry
        for entry in await session.scalars(select(GuideSearchEntry))
    }
    report = {"indexed": 0, "unchanged": 0, "dropped": 0, "unavailable": 0}
    keep: set[tuple[UUID, str]] = set()
    for article, row in rows:
        key = (article.id, row.locale)
        keep.add(key)
        entry = existing.get(key)
        if entry is not None and entry.revision_version == row.published_version:
            report["unchanged"] += 1
            continue
        try:
            published = await _published_document(session, row)
        except AppError:
            # A dangling pointer is the article page's 503, not the reindex's crash; the
            # row is left out and counted so the operator goes looking.
            report["unavailable"] += 1
            keep.discard(key)
            continue
        if published is None:
            continue
        await index_locale(
            session,
            article.id,
            row.locale,
            published,
            version=published.version,
            published_at=published.published_at,
        )
        report["indexed"] += 1
    for key, entry in existing.items():
        if key not in keep:
            await session.delete(entry)
            report["dropped"] += 1
    return report


# --- the query ----------------------------------------------------------------


def parse_query(q: str) -> list[str]:
    """The folded terms of a query, or a 422 when nothing searchable is left.

    Splits on whitespace and punctuation, drops a lone ASCII character (``a`` matches
    every English article and ``,`` matches none) while keeping a lone CJK one (``雪`` is
    a word), and keeps the first six distinct terms.
    """
    folded = normalize(q[:MAX_QUERY_LENGTH])
    terms: list[str] = []
    for term in _SEPARATORS.split(folded):
        if not term or (len(term) == 1 and term.isascii()) or term in terms:
            continue
        terms.append(term)
        if len(terms) == MAX_TERMS:
            break
    if not terms:
        raise AppError(422, "guide_search_query_invalid", "請輸入要搜尋的字詞")
    return terms


def _pattern(term: str) -> str:
    return f"%{escape_like(term)}%"


def _contains(column: InstrumentedAttribute[str], term: str) -> ColumnElement[bool]:
    return column.like(_pattern(term), escape="\\")


def _score(terms: list[str]) -> ColumnElement[int]:
    return reduce(
        operator.add,
        (
            case(
                (_contains(GuideSearchEntry.title_norm, term), TITLE_WEIGHT),
                (_contains(GuideSearchEntry.aliases_norm, term), ALIAS_WEIGHT),
                (_contains(GuideSearchEntry.description_norm, term), DESCRIPTION_WEIGHT),
                (_contains(GuideSearchEntry.headings_norm, term), HEADING_WEIGHT),
                else_=BODY_WEIGHT,
            )
            for term in terms
        ),
    )


def _visible(*columns: Any, conditions: list[ColumnElement[bool]]) -> Select[Any]:
    """Index rows a reader of this locale may see: joined to the translation and the
    article so ``published_filters`` decides, and only at the version the pointer names."""
    return (
        select(*columns)
        .select_from(GuideSearchEntry)
        .join(
            GuideArticleLocale,
            and_(
                GuideArticleLocale.article_id == GuideSearchEntry.article_id,
                GuideArticleLocale.locale == GuideSearchEntry.locale,
            ),
        )
        .join(GuideArticle, GuideArticle.id == GuideSearchEntry.article_id)
        .where(
            GuideArticleLocale.published_version == GuideSearchEntry.revision_version,
            *published_filters(),
            *conditions,
        )
    )


def _summary(
    entry: GuideSearchEntry, article: GuideArticle, locale: Locale, topics: dict[UUID, list[Any]]
) -> dict[str, Any]:
    return {
        "slug": article.slug,
        "kind": cast(Kind, article.kind),
        "destination_id": article.destination_id,
        "destination_label": destination_label(article.destination_id, locale),
        "topics": topics.get(article.id, []),
        "title": entry.title,
        "description": entry.description,
        "hero": HeroImage.model_validate(entry.hero_json) if entry.hero_json else None,
        "published_at": entry.published_at,
        "valid_until": article.valid_until,
        "featured": article.featured,
    }


def snippet(body_text: str, description: str, terms: list[str]) -> str:
    """The passage around the first term found in the body, or the description's start.

    The search is done on a casefolded copy and the slice taken from the readable one,
    which is only sound while the two are the same length; the rare letters that fold to
    more than one character (``ß``) send the reader the description instead of a shifted
    passage.
    """
    for folded in (body_text.casefold(), body_text.lower()):
        if len(folded) != len(body_text):
            continue
        positions = [index for index in (folded.find(term) for term in terms) if index >= 0]
        if not positions:
            break
        start = max(0, min(positions) - SNIPPET_RADIUS)
        end = min(len(body_text), min(positions) + SNIPPET_RADIUS)
        passage = body_text[start:end].strip()
        return f"{'…' if start else ''}{passage}{'…' if end < len(body_text) else ''}"
    if len(description) <= DESCRIPTION_SNIPPET:
        return description
    return description[:DESCRIPTION_SNIPPET].rstrip() + "…"


async def search(
    session: AsyncSession,
    locale: Locale,
    *,
    q: str,
    section: Section | None = None,
    kind: Kind | None = None,
    topic: str | None = None,
    destination: str | None = None,
    country: str | None = None,
    limit: int = 10,
    offset: int = 0,
) -> GuideSearchResult:
    terms = parse_query(q)
    size = min(max(limit, 1), MAX_LIMIT)
    offset = min(max(offset, 0), MAX_OFFSET)

    def empty() -> GuideSearchResult:
        return GuideSearchResult(
            query=q, total=0, offset=offset, limit=size, results=[], best_match=None
        )

    kinds = kind_filter(kind, section)
    if kinds is not None and not kinds:
        return empty()
    topic_ids = await topic_ids_including_children(session, topic) if topic else None
    if topic_ids is not None and not topic_ids:
        return empty()
    conditions: list[ColumnElement[bool]] = [GuideSearchEntry.locale == locale]
    if kinds:
        conditions.append(GuideArticle.kind.in_(kinds))
    if destination:
        conditions.append(GuideArticle.destination_id == destination.casefold())
    if country:
        ids = [profile.id for profile in destinations_in_country(country)]
        if not ids:
            return empty()
        conditions.append(GuideArticle.destination_id.in_(ids))
    if topic_ids:
        conditions.append(
            GuideArticle.id.in_(
                select(GuideArticleTopic.article_id).where(
                    GuideArticleTopic.topic_id.in_(topic_ids)
                )
            )
        )

    best = await _best_match(session, locale, normalize(q), conditions)
    matches = [_contains(GuideSearchEntry.search_text, term) for term in terms]
    if best is not None:
        matches.append(GuideSearchEntry.article_id != best[0].article_id)
    total = int(
        await session.scalar(_visible(func.count(), conditions=[*conditions, *matches])) or 0
    )
    rows = list(
        await session.execute(
            _visible(GuideSearchEntry, GuideArticle, conditions=[*conditions, *matches])
            .order_by(_score(terms).desc(), GuideSearchEntry.published_at.desc(), GuideArticle.slug)
            .offset(offset)
            .limit(size)
        )
    )
    article_ids = [article.id for _, article in rows]
    if best is not None:
        article_ids.append(best[1].id)
    topics = await _topic_options_for(session, article_ids, locale)
    results = [
        GuideSearchHit(
            **_summary(entry, article, locale, topics),
            snippet=snippet(entry.body_text, entry.description, terms),
            matched=terms,
        )
        for entry, article in rows
    ]
    next_offset = offset + size
    return GuideSearchResult(
        query=q,
        total=total,
        offset=offset,
        limit=size,
        results=results,
        best_match=PublicSummary(**_summary(best[0], best[1], locale, topics)) if best else None,
        next_offset=next_offset if next_offset < total and next_offset <= MAX_OFFSET else None,
    )


async def _best_match(
    session: AsyncSession, locale: Locale, folded: str, conditions: list[ColumnElement[bool]]
) -> tuple[GuideSearchEntry, GuideArticle] | None:
    """The one visible article whose alias or title is the whole query.

    An alias shared by several articles is a ranking hint, not a name, so it names no
    best match; the title is tried next, newest first when two articles share one.
    """
    if not folded:
        return None
    by_alias = (
        select(GuideArticleAlias.article_id)
        .where(GuideArticleAlias.locale == locale, GuideArticleAlias.alias_norm == folded)
        .distinct()
    )
    candidates = list(await session.scalars(by_alias))
    if len(candidates) == 1:
        hit = (
            await session.execute(
                _visible(
                    GuideSearchEntry,
                    GuideArticle,
                    conditions=[*conditions, GuideSearchEntry.article_id == candidates[0]],
                ).limit(1)
            )
        ).first()
        if hit is not None:
            return cast(tuple[GuideSearchEntry, GuideArticle], tuple(hit))
    hit = (
        await session.execute(
            _visible(
                GuideSearchEntry,
                GuideArticle,
                conditions=[*conditions, GuideSearchEntry.title_norm == folded],
            )
            .order_by(GuideSearchEntry.published_at.desc(), GuideArticle.slug)
            .limit(1)
        )
    ).first()
    return cast(tuple[GuideSearchEntry, GuideArticle], tuple(hit)) if hit is not None else None
