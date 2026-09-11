"""First-party travel intel and guide articles.

``site_pages`` keys a document by ``(slug, locale)`` in one table because its slug set is
four fixed values. An article cannot do that: its slug, kind, destination, topics and
validity are properties of the article itself, not of any one translation, and storing
them five times lets the five copies drift. So the identity lives in ``guide_articles``
and each translation's draft/publication lifecycle lives in ``guide_article_locales``.
"""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

KINDS = ("intel", "howto")
LOCALE_CHECK = "locale IN ('en', 'ja', 'ko', 'zh-TW', 'zh-CN')"


def utcnow() -> datetime:
    return datetime.now(UTC)


class Timestamped:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class GuideArticle(Timestamped, Base):
    """The article's language-independent identity and taxonomy."""

    __tablename__ = "guide_articles"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_guide_article_slug"),
        CheckConstraint("kind IN ('intel', 'howto')", name="ck_guide_article_kind"),
        CheckConstraint("version >= 1", name="ck_guide_article_version"),
        Index("ix_guide_articles_kind_active", "kind", "is_active"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(120), index=True)
    kind: Mapped[str] = mapped_column(String(16))
    # Checked against app.destinations.catalog rather than a foreign key: the destination
    # directory is source-controlled Python, not a table. NULL is a cross-destination
    # article ("which Japan Rail Pass to buy"), which has no city to belong to.
    destination_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    # The day an offer or a rule stops being true. It is one date for the article, not one
    # per translation, and it is what takes expired intel out of the lists and the sitemap.
    valid_until: Mapped[date | None] = mapped_column(Date, nullable=True)
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    display_order: Mapped[int] = mapped_column(Integer, default=100)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    # Optimistic lock for the taxonomy fields above; each translation locks separately.
    version: Mapped[int] = mapped_column(Integer, default=1)


class GuideArticleLocale(Timestamped, Base):
    """One translation's draft and publication state. Locales publish independently."""

    __tablename__ = "guide_article_locales"
    __table_args__ = (
        UniqueConstraint("article_id", "locale", name="uq_guide_article_locale"),
        CheckConstraint(LOCALE_CHECK, name="ck_guide_article_locale_locale"),
        CheckConstraint("version >= 1", name="ck_guide_article_locale_version"),
        CheckConstraint(
            "published_version IS NULL OR "
            "(published_version >= 1 AND published_version <= version)",
            name="ck_guide_article_locale_published_version",
        ),
        # Every public list is "this locale, published, newest first". A partial index on
        # published_version would be tighter but is PostgreSQL-only, and the SQLite test
        # leg has to exercise the same plan shape.
        Index("ix_guide_article_locales_public", "locale", "published_at"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    article_id: Mapped[UUID] = mapped_column(
        ForeignKey("guide_articles.id", ondelete="CASCADE"), index=True
    )
    locale: Mapped[str] = mapped_column(String(16), index=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    draft_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    # A plain integer, not a foreign key to the revision: the revision row is written in the
    # same transaction that moves this pointer, so a circular constraint would buy nothing.
    # Read the published text by (article_locale_id, published_version).
    published_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class GuideArticleRevision(Base):
    """Append-only history. The database trigger, not the service, is what enforces that."""

    __tablename__ = "guide_article_revisions"
    __table_args__ = (
        UniqueConstraint("article_locale_id", "version", name="uq_guide_article_revision_version"),
        CheckConstraint("version >= 1", name="ck_guide_article_revision_version"),
        CheckConstraint(
            "action IN ('created', 'draft_saved', 'published', 'unpublished', 'restored')",
            name="ck_guide_article_revision_action",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    article_locale_id: Mapped[UUID] = mapped_column(
        ForeignKey("guide_article_locales.id"), index=True
    )
    version: Mapped[int] = mapped_column(Integer)
    action: Mapped[str] = mapped_column(String(32))
    document_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class GuideTopic(Timestamped, Base):
    """A subject tag. ``names_json`` holds one label per site locale, as HotspotTheme does,
    so an editor can add a topic without a deploy and without an i18n catalog change."""

    __tablename__ = "guide_topics"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_guide_topic_slug"),
        CheckConstraint("source IN ('seed', 'admin')", name="ck_guide_topic_source"),
        Index("ix_guide_topics_active_order", "is_active", "display_order"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(64), index=True)
    names_json: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    display_order: Mapped[int] = mapped_column(Integer, default=100)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    source: Mapped[str] = mapped_column(String(16), default="admin")


class GuideArticleTopic(Base):
    __tablename__ = "guide_article_topics"
    __table_args__ = (UniqueConstraint("article_id", "topic_id", name="uq_guide_article_topic"),)
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    article_id: Mapped[UUID] = mapped_column(
        ForeignKey("guide_articles.id", ondelete="CASCADE"), index=True
    )
    topic_id: Mapped[UUID] = mapped_column(
        ForeignKey("guide_topics.id", ondelete="CASCADE"), index=True
    )
