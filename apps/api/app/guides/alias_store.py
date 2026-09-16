"""Reading an article's other names. Writes live in ``search`` (they refresh the index)
and the seed in ``aliases``; this module has no dependency but the models, so the public
read path can import it without pulling the search module in behind it."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.guides.models import GuideArticleAlias


async def editor_aliases(
    session: AsyncSession, article_ids: list[UUID]
) -> dict[UUID, dict[str, list[str]]]:
    """The editor-written names per article and locale, in the order they were written."""
    if not article_ids:
        return {}
    rows = await session.execute(
        select(GuideArticleAlias)
        .where(GuideArticleAlias.article_id.in_(article_ids), GuideArticleAlias.source == "editor")
        .order_by(GuideArticleAlias.locale, GuideArticleAlias.created_at, GuideArticleAlias.alias)
    )
    grouped: dict[UUID, dict[str, list[str]]] = {}
    for row in rows.scalars():
        grouped.setdefault(row.article_id, {}).setdefault(row.locale, []).append(row.alias)
    return grouped


async def public_aliases(session: AsyncSession, article_id: UUID, locale: str) -> list[str]:
    """The names a reader may be shown for the article: everything but a series catalogue's
    keyword hints, which are ranking material rather than names."""
    rows = await session.scalars(
        select(GuideArticleAlias.alias)
        .where(
            GuideArticleAlias.article_id == article_id,
            GuideArticleAlias.locale == locale,
            GuideArticleAlias.source != "series",
        )
        .order_by(GuideArticleAlias.created_at, GuideArticleAlias.alias)
    )
    return list(dict.fromkeys(rows))
