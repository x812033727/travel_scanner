"""Versioned series order joined to live, per-locale published revisions.

The catalogue never supplies public titles or bodies. A draft, withdrawn translation or
hidden identity cannot reappear through a series, prerequisite or inline reference.
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.guides.models import GuideArticle, GuideArticleLocale, GuideArticleRevision
from app.guides.publication import published_filters
from app.guides.schemas import (
    ArticleInline,
    ArticleReference,
    GuideDocument,
    Kind,
    PublicSeries,
    RichParagraphBlock,
    SeriesEntry,
    SeriesGroup,
    SeriesNavigation,
    SeriesPath,
)
from app.i18n import Locale
from app.problems import AppError
from app.site_pages.schemas import StrictModel


class Lesson(StrictModel):
    slug: str
    title: str
    outcome: str
    sources: list[str]
    number: int = Field(ge=1)
    group: str
    level: Literal["beginner", "intermediate", "advanced"]
    platforms: list[str]
    aliases: list[str]
    prerequisites: list[str] = Field(default_factory=list)
    related: list[str] = Field(default_factory=list, max_length=3)


class Catalogue(StrictModel):
    slug: str
    locale: Locale
    hub: str
    groups: list[SeriesGroup]
    paths: list[SeriesPath]
    entries: list[Lesson]

    @model_validator(mode="after")
    def consistent(self) -> Catalogue:
        slugs = {entry.slug for entry in self.entries}
        groups = {group.id for group in self.groups}
        if len(slugs) != len(self.entries) or self.hub in slugs:
            raise ValueError("duplicate series article")
        if [entry.number for entry in self.entries] != list(range(1, len(slugs) + 1)):
            raise ValueError("series numbers must be contiguous and ordered")
        for entry in self.entries:
            if entry.group not in groups or not set(entry.prerequisites + entry.related) <= slugs:
                raise ValueError("unknown series reference")
            if entry.slug in entry.prerequisites + entry.related:
                raise ValueError("self reference in series")
        for path in self.paths:
            if not set(path.slugs) <= slugs or len(path.slugs) != len(set(path.slugs)):
                raise ValueError("invalid learning path")
        return self


@lru_cache(maxsize=1)
def catalogues() -> tuple[Catalogue, ...]:
    root = Path(__file__).with_name("series_data")
    return tuple(
        Catalogue.model_validate(json.loads(path.read_text(encoding="utf-8")))
        for path in sorted(root.glob("*.json"))
    )


def catalogue_for_article(slug: str) -> Catalogue | None:
    return next(
        (
            item
            for item in catalogues()
            if slug == item.hub or any(entry.slug == slug for entry in item.entries)
        ),
        None,
    )


async def published_documents(
    session: AsyncSession,
    locale: Locale,
    targets: set[tuple[Kind, str]],
) -> dict[str, tuple[ArticleReference, GuideDocument]]:
    if not targets:
        return {}
    rows = await session.execute(
        select(GuideArticle, GuideArticleRevision)
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
            GuideArticle.slug.in_([slug for _, slug in targets]),
            GuideArticleLocale.locale == locale,
            *published_filters(),
        )
    )
    found: dict[str, tuple[ArticleReference, GuideDocument]] = {}
    for article, revision in rows:
        if (article.kind, article.slug) not in targets:
            continue
        if revision is None:
            raise AppError(503, "guide_article_unavailable", "暫時無法取得這篇文章，請稍後再試")
        document = GuideDocument.model_validate(revision.document_json)
        reference = ArticleReference(kind=article.kind, slug=article.slug, title=document.title)
        found[article.slug] = (reference, document)
    return found


async def resolve_article_links(
    session: AsyncSession,
    locale: Locale,
    document: GuideDocument,
) -> list[ArticleReference]:
    targets = {
        (node.kind, node.slug)
        for block in document.blocks
        if isinstance(block, RichParagraphBlock)
        for node in block.inlines
        if isinstance(node, ArticleInline)
    }
    return [ref for ref, _ in (await published_documents(session, locale, targets)).values()]


async def public_series(
    session: AsyncSession,
    slug: str,
    locale: Locale,
) -> PublicSeries | None:
    catalogue = next(
        (item for item in catalogues() if item.slug == slug and item.locale == locale), None
    )
    if catalogue is None:
        return None
    targets: set[tuple[Kind, str]] = {("life", entry.slug) for entry in catalogue.entries}
    targets.add(("life", catalogue.hub))
    visible = await published_documents(session, locale, targets)
    if catalogue.hub not in visible:
        return None
    entries = []
    for item in catalogue.entries:
        if item.slug not in visible:
            continue
        reference, document = visible[item.slug]
        text = " ".join(
            " ".join(node.text for node in block.inlines)
            if isinstance(block, RichParagraphBlock)
            else getattr(block, "text", "")
            for block in document.blocks
        )
        entries.append(
            SeriesEntry(
                **reference.model_dump(),
                number=item.number,
                group=item.group,
                level=item.level,
                platforms=item.platforms,
                aliases=item.aliases,
                description=document.description,
                minutes=max(1, math.ceil(len(text) / 450)),
            )
        )
    return PublicSeries(
        slug=slug,
        locale=locale,
        hub=visible[catalogue.hub][0],
        entries=entries,
        groups=[group for group in catalogue.groups if any(e.group == group.id for e in entries)],
        paths=[
            SeriesPath(id=path.id, title=path.title, slugs=[s for s in path.slugs if s in visible])
            for path in catalogue.paths
            if any(s in visible for s in path.slugs)
        ],
    )


async def article_navigation(
    session: AsyncSession,
    kind: Kind,
    slug: str,
    locale: Locale,
) -> SeriesNavigation | None:
    catalogue = catalogue_for_article(slug) if kind == "life" else None
    if catalogue is None:
        return None
    series = await public_series(session, catalogue.slug, locale)
    if series is None:
        return None
    if slug == catalogue.hub:
        return SeriesNavigation(slug=series.slug, hub=series.hub)
    visible = {
        entry.slug: ArticleReference(kind=entry.kind, slug=entry.slug, title=entry.title)
        for entry in series.entries
    }
    for index, entry in enumerate(series.entries):
        if entry.slug == slug:
            lesson = next(item for item in catalogue.entries if item.slug == slug)
            return SeriesNavigation(
                slug=series.slug,
                hub=series.hub,
                current=entry,
                previous=visible[series.entries[index - 1].slug] if index else None,
                next=visible[series.entries[index + 1].slug]
                if index + 1 < len(series.entries)
                else None,
                prerequisites=[visible[s] for s in lesson.prerequisites if s in visible],
                related=[visible[s] for s in lesson.related if s in visible],
            )
    return None
