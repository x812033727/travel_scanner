"""The one definition of "this article is public in this language".

Three readers ask that question -- the list, the article page and the sitemap -- and if
they answer it differently the site advertises a URL it will not serve, or hides one it
already told Google about. They all call in here instead, as ``app.foods.publication``
already does for merchants.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, date, datetime
from typing import Literal

from sqlalchemy import ColumnElement, and_, case, exists, or_

from app.guides.models import GuideArticle, GuideArticleLocale

# The one editor-facing state of an article. "hidden" is the article-wide switch, "expired"
# is the date, and "published" means at least one translation is live; anything else is a
# draft nobody can see yet. Precedence matters: a hidden, expired article is hidden.
ArticleStatus = Literal["published", "draft", "hidden", "expired"]
ARTICLE_STATUSES: tuple[ArticleStatus, ...] = ("published", "draft", "hidden", "expired")


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


def article_status(
    article: GuideArticle, rows: Iterable[GuideArticleLocale], *, on: date | None = None
) -> ArticleStatus:
    """``ArticleStatus`` for rows already in memory; ``admin_status_filters`` is the SQL twin."""
    if not article.is_active:
        return "hidden"
    if article.valid_until is not None and article.valid_until < (on or today()):
        return "expired"
    if any(row.published_version is not None for row in rows):
        return "published"
    return "draft"


def admin_status_expression(*, on: date | None = None) -> ColumnElement[str]:
    """The SQL twin of ``article_status``: one CASE, same precedence, on GuideArticle.

    Both the status filter and the facet counts are built from this one expression, so
    the list an editor filters by "hidden" holds exactly the rows whose pill says hidden.
    """
    cutoff = on or today()
    expired = and_(GuideArticle.valid_until.is_not(None), GuideArticle.valid_until < cutoff)
    has_published = exists().where(
        GuideArticleLocale.article_id == GuideArticle.id,
        GuideArticleLocale.published_version.is_not(None),
    )
    return case(
        (GuideArticle.is_active.is_(False), "hidden"),
        (expired, "expired"),
        (has_published, "published"),
        else_="draft",
    )


def admin_status_filters(
    status: ArticleStatus, *, on: date | None = None
) -> list[ColumnElement[bool]]:
    return [admin_status_expression(on=on) == status]
