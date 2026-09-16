"""The two operator commands behind the link graph: a full rebuild and a link check.

Kept out of ``app/cli.py`` so they can be exercised against the guides test database,
and out of ``links`` so that module stays free of the session factory and the read path.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db import SessionFactory
from app.guides import links
from app.guides.autolink import SITE_LINK
from app.guides.models import GuideArticle, GuideArticleLink, GuideArticleLocale
from app.guides.publication import article_is_live
from app.guides.schemas import GuideDocument, LinkInline, RichParagraphBlock
from app.guides.service import _published_document
from app.problems import AppError
from app.site_pages.schemas import LinkBlock


async def _published_rows(
    session: AsyncSession, locale: str | None
) -> list[tuple[GuideArticle, GuideArticleLocale]]:
    query = (
        select(GuideArticle, GuideArticleLocale)
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .where(GuideArticleLocale.published_version.is_not(None))
        .order_by(GuideArticle.slug, GuideArticleLocale.locale)
    )
    if locale:
        query = query.where(GuideArticleLocale.locale == locale)
    return [(article, row) for article, row in await session.execute(query)]


async def rebuild_all(session: AsyncSession) -> dict[str, Any]:
    """Rebuild every published translation's inline rows from its published revision and
    drop the rows no published translation backs. Idempotent; hidden and expired
    articles are rebuilt too, since the read path decides what shows."""
    report: dict[str, Any] = {"materialized": 0, "dropped": 0, "unavailable": 0, "unresolved": []}
    keep: set[tuple[Any, str]] = set()
    for article, row in await _published_rows(session, None):
        try:
            published = await _published_document(session, row)
        except AppError:
            report["unavailable"] += 1
            continue
        if published is None:
            continue
        keep.add((article.id, row.locale))
        unresolved = await links.materialize_inline(session, article.id, row.locale, published)
        report["materialized"] += 1
        report["unresolved"].extend(
            f"{article.slug} ({row.locale}): {target}" for target in unresolved
        )
    stale = await session.execute(
        select(GuideArticleLink.source_article_id, GuideArticleLink.locale)
        .where(GuideArticleLink.relation == "inline")
        .distinct()
    )
    for source, locale in stale:
        if (source, locale) not in keep and locale is not None:
            await links.drop_inline(session, source, locale)
            report["dropped"] += 1
    return report


@dataclass(frozen=True)
class Finding:
    source: str
    locale: str
    target: str
    problem: str


async def check_all(session: AsyncSession, *, locale: str | None = None) -> list[Finding]:
    """Every in-text link of a published translation that a reader cannot follow, and every
    raw site URL that should be an article inline."""
    findings: list[Finding] = []
    rows = await _published_rows(session, locale)
    articles = {article.slug: article for article in await session.scalars(select(GuideArticle))}
    published: dict[tuple[Any, str], GuideArticleLocale] = {
        (row.article_id, row.locale): row
        for row in await session.scalars(
            select(GuideArticleLocale).where(GuideArticleLocale.published_version.is_not(None))
        )
    }
    for article, row in rows:
        try:
            document = await _published_document(session, row)
        except AppError:
            findings.append(Finding(article.slug, row.locale, "-", "unavailable"))
            continue
        if document is None:
            continue
        for kind, slug in links.inline_targets(document):
            target = articles.get(slug)
            label = f"{kind}/{slug}"
            if target is None:
                findings.append(Finding(article.slug, row.locale, label, "missing"))
            elif target.kind != kind:
                findings.append(Finding(article.slug, row.locale, label, "wrong_kind"))
            elif (target.id, row.locale) not in published:
                findings.append(Finding(article.slug, row.locale, label, "unpublished"))
            elif not target.is_active:
                findings.append(Finding(article.slug, row.locale, label, "hidden"))
            elif not article_is_live(target):
                findings.append(Finding(article.slug, row.locale, label, "expired"))
        for url in _raw_urls(document):
            if SITE_LINK.match(url) is not None:
                findings.append(Finding(article.slug, row.locale, url, "raw_url"))
    return findings


def _raw_urls(document: GuideDocument) -> list[str]:
    urls: list[str] = []
    for block in document.blocks:
        if isinstance(block, LinkBlock):
            urls.append(block.url)
        elif isinstance(block, RichParagraphBlock):
            urls.extend(node.url for node in block.inlines if isinstance(node, LinkInline))
    return urls


async def rebuild_guide_links(
    *, dry_run: bool = False, factory: async_sessionmaker[AsyncSession] | None = None
) -> dict[str, Any]:
    async with (factory or SessionFactory)() as session:
        report = await rebuild_all(session)
        if dry_run:
            await session.rollback()
        else:
            await session.commit()
        return {"dry_run": dry_run, **report}


async def check_guide_links(
    *, locale: str | None = None, factory: async_sessionmaker[AsyncSession] | None = None
) -> dict[str, Any]:
    async with (factory or SessionFactory)() as session:
        findings = await check_all(session, locale=locale)
        return {"locale": locale, "findings": [asdict(item) for item in findings]}
