"""The one definition of "this article is public in this language".

Three readers ask that question -- the list, the article page and the sitemap -- and if
they answer it differently the site advertises a URL it will not serve, or hides one it
already told Google about. They all call in here instead, as ``app.foods.publication``
already does for merchants.
"""

from __future__ import annotations

from datetime import UTC, date, datetime

from sqlalchemy import ColumnElement, or_

from app.guides.models import GuideArticle, GuideArticleLocale


def today() -> date:
    return datetime.now(UTC).date()


def article_is_live(article: GuideArticle, *, on: date | None = None) -> bool:
    """Whether the identity is publishable at all, regardless of translation."""
    if not article.is_active:
        return False
    return article.valid_until is None or article.valid_until >= (on or today())


def published_filters(*, on: date | None = None) -> list[ColumnElement[bool]]:
    """SQL predicates for a join of GuideArticleLocale onto GuideArticle."""
    cutoff = on or today()
    return [
        GuideArticleLocale.published_version.is_not(None),
        GuideArticle.is_active.is_(True),
        or_(GuideArticle.valid_until.is_(None), GuideArticle.valid_until >= cutoff),
    ]


def locale_is_published(
    article: GuideArticle, row: GuideArticleLocale, *, on: date | None = None
) -> bool:
    """The same rule applied to rows already in memory. Defence in depth: the loaded-row
    check and the query predicates must agree, so neither is allowed to be the only one."""
    return row.published_version is not None and article_is_live(article, on=on)
