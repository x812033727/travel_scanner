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
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

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
        # `life` is the lifestyle section; `intel` and `howto` are the travel section. One
        # table, one editor, one revision history: the section only changes the URL, the
        # navigation, the topic vocabulary and the end-of-article block.
        CheckConstraint("kind IN ('intel', 'howto', 'life')", name="ck_guide_article_kind"),
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
    # The day the news happened, for a news article: what a news list is ordered by and shows.
    # Not the publication time -- news is imported in batches, so a whole week of stories
    # publishes within the same minute -- and not ``updated_at``, which moves on every fix.
    # NULL for everything that is not a dated news item, including a news topic's evergreen
    # pieces (a sources list, a yearly timeline).
    news_date: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
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
    so an editor can add a topic without a deploy and without an i18n catalog change.

    Topics are two levels deep at most: a topic with a ``parent_id`` is a sub-topic of that
    parent and the parent itself has none. The depth is a rule of ``admin_service`` and the
    seed, not a CHECK, because a self-referencing CHECK does not survive SQLite's batch
    rebuild. Filtering by a parent includes its children; listing counts them once.
    """

    __tablename__ = "guide_topics"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_guide_topic_slug"),
        CheckConstraint("source IN ('seed', 'admin')", name="ck_guide_topic_source"),
        CheckConstraint("section IN ('travel', 'life')", name="ck_guide_topic_section"),
        Index("ix_guide_topics_active_order", "is_active", "display_order"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(64), index=True)
    names_json: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    display_order: Mapped[int] = mapped_column(Integer, default=100)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    source: Mapped[str] = mapped_column(String(16), default="admin")
    # Which section's articles may carry this topic. The DDL default is not decoration:
    # 0072's seed inserts rows without this column, and on a fresh database that seed runs
    # against a table 0001 already built from this model.
    section: Mapped[str] = mapped_column(String(16), default="travel", server_default="travel")
    # The parent topic, or NULL for a top-level one. SET NULL rather than CASCADE: removing a
    # parent promotes its children rather than deleting a vocabulary articles still carry.
    parent_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("guide_topics.id", ondelete="SET NULL"), nullable=True, index=True
    )
    # One introductory paragraph per locale for the topic's hub page. Optional: a topic
    # without one still lists its articles, it just has no lead.
    descriptions_json: Mapped[dict[str, str] | None] = mapped_column(
        JSON(none_as_null=True), nullable=True
    )


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


class GuideSearchEntry(Base):
    """One published translation, flattened for the reader's search box.

    The article's text lives in a block document inside an append-only revision row; a
    search cannot LIKE its way through JSON, and it must never see a draft. So publication
    writes one row here per (article, locale) and withdrawal deletes it, in the same
    transaction as the pointer move (``admin_service._write_revision``). Nothing else about
    the article is copied: kind, destination, topics, validity and the hidden switch stay
    on ``guide_articles`` and are joined at query time, so hiding or expiring an article
    takes it out of the results without touching this table.

    The ``*_norm`` columns are NFKC-folded and casefolded once at write time so the query
    can compare with a plain ``LIKE`` on both PostgreSQL and SQLite: ``ILIKE`` does not exist
    on the latter and its ``lower()`` only folds ASCII. ``search_text`` is the concatenation
    the match runs on; the PostgreSQL trigram index over it is created by migration 0077,
    not declared here, because ``pg_trgm`` is an extension a fresh ``0001`` cannot assume.
    """

    __tablename__ = "guide_search_entries"
    __table_args__ = (
        UniqueConstraint("article_id", "locale", name="uq_guide_search_entry_locale"),
        CheckConstraint(LOCALE_CHECK, name="ck_guide_search_entry_locale"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    article_id: Mapped[UUID] = mapped_column(
        ForeignKey("guide_articles.id", ondelete="CASCADE"), index=True
    )
    locale: Mapped[str] = mapped_column(String(16), index=True)
    # The published version the row was built from; ``guide_article_locales.published_version``
    # must agree, or the row is stale and the query leaves it out.
    revision_version: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(500))
    title_norm: Mapped[str] = mapped_column(String(200))
    description_norm: Mapped[str] = mapped_column(String(500))
    headings_norm: Mapped[str] = mapped_column(Text)
    aliases_norm: Mapped[str] = mapped_column(Text)
    # The body as readable text (NFKC, whitespace folded, case kept) for the snippet.
    body_text: Mapped[str] = mapped_column(Text)
    search_text: Mapped[str] = mapped_column(Text)
    hero_json: Mapped[dict[str, Any] | None] = mapped_column(
        JSON(none_as_null=True), nullable=True
    )
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    indexed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class GuideArticleAlias(Base):
    """Another name a reader may type for an article, in one language.

    ``term`` aliases come from the AI glossary (``ML`` for the machine-learning article),
    ``series`` ones from a course catalogue's keyword hints, ``keyword`` from an editor's
    suffix list and ``editor`` from the admin panel. A name only one published article in
    the language carries is that article's exact match and heads the results; a name
    several share is a ranking hint and nothing more. Uniqueness is therefore per article,
    not per language: two lessons may both answer to ``powershell``.
    """

    __tablename__ = "guide_article_aliases"
    __table_args__ = (
        UniqueConstraint("article_id", "locale", "alias_norm", name="uq_guide_article_alias"),
        CheckConstraint(LOCALE_CHECK, name="ck_guide_article_alias_locale"),
        CheckConstraint(
            "source IN ('term', 'keyword', 'series', 'editor')",
            name="ck_guide_article_alias_source",
        ),
        Index("ix_guide_article_aliases_lookup", "locale", "alias_norm"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    article_id: Mapped[UUID] = mapped_column(
        ForeignKey("guide_articles.id", ondelete="CASCADE"), index=True
    )
    locale: Mapped[str] = mapped_column(String(16))
    alias: Mapped[str] = mapped_column(String(120))
    alias_norm: Mapped[str] = mapped_column(String(120))
    source: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class GuideArticleLink(Base):
    """One article pointing at another: the graph the end-of-article reading list and the
    "cited by" list are read from.

    ``inline`` rows are written when a translation is published, from the ``article``
    inlines of its published text, and deleted when it is withdrawn -- so they are per
    locale, and a link a reader cannot follow is never in the table. ``related`` rows are
    the editor's further-reading picks, on the identity rather than a translation, so
    their ``locale`` is NULL and uniqueness is kept by the replace-all write that maintains
    them (the same way topics are). Whether a target is *visible* is still decided at read
    time through ``published_filters``: the row says the link exists, not that it may show.
    """

    __tablename__ = "guide_article_links"
    __table_args__ = (
        UniqueConstraint(
            "source_article_id", "locale", "relation", "target_article_id",
            name="uq_guide_article_link",
        ),
        CheckConstraint("relation IN ('inline', 'related')", name="ck_guide_article_link_relation"),
        CheckConstraint(f"locale IS NULL OR {LOCALE_CHECK}", name="ck_guide_article_link_locale"),
        Index("ix_guide_article_links_target", "target_article_id", "locale"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    source_article_id: Mapped[UUID] = mapped_column(
        ForeignKey("guide_articles.id", ondelete="CASCADE"), index=True
    )
    target_article_id: Mapped[UUID] = mapped_column(
        ForeignKey("guide_articles.id", ondelete="CASCADE")
    )
    locale: Mapped[str | None] = mapped_column(String(16), nullable=True)
    relation: Mapped[str] = mapped_column(String(16))
    position: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
