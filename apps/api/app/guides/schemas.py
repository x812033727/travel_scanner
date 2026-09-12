"""Request and response shapes for travel intel and guide articles.

The document body deliberately reuses ``app.site_pages.schemas``' structured blocks rather
than accepting HTML or Markdown: the same validator that keeps a privacy policy free of
embeds and control characters keeps an article free of them, and the same web renderer can
draw both, so the admin preview cannot drift from the public page.
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from typing import Annotated, Literal, Self
from urllib.parse import urlsplit
from uuid import UUID

from pydantic import AfterValidator, BaseModel, Field, field_validator, model_validator

from app.admin.schemas import AdminAuditView
from app.affiliates.schemas import AffiliateModule
from app.guides.publication import ArticleStatus
from app.i18n import Locale
from app.site_pages.schemas import (
    HeadingBlock,
    LinkBlock,
    ListBlock,
    NonemptyText,
    ParagraphBlock,
    StrictModel,
    plain_text,
    safe_http_url,
)

Kind = Literal["intel", "howto", "life"]
# The kinds in the order the admin facets list them. Kept beside the Literal because the
# facet counts iterate it, so a kind added above must appear here or vanish from the list.
KINDS: tuple[Kind, ...] = ("intel", "howto", "life")
# A section is a reader-facing area with its own URL space, navigation entry and topic
# vocabulary. The travel section holds intel and how-to articles at /guides; the lifestyle
# section holds `life` articles at /life. Nothing else about an article differs.
Section = Literal["travel", "life"]
SECTION_KINDS: dict[Section, tuple[Kind, ...]] = {"travel": ("intel", "howto"), "life": ("life",)}
RevisionAction = Literal["created", "draft_saved", "published", "unpublished", "restored"]


def section_of(kind: Kind) -> Section:
    return "life" if kind == "life" else "travel"

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def article_slug(value: str) -> str:
    normalized = plain_text(value).lower()
    if not SLUG_PATTERN.match(normalized):
        raise ValueError("slug uses lowercase letters, digits and single hyphens")
    return normalized


class SourceRef(StrictModel):
    """Where a fare, a rule or an opening time came from.

    Intel goes stale and readers need to check it themselves; an article that states a
    visa rule without saying where it read it is not something this site should publish.
    """

    title: NonemptyText = Field(max_length=200)
    url: str = Field(min_length=1, max_length=2000)
    checked_on: date | None = None

    @field_validator("url")
    @classmethod
    def safe_source(cls, value: str) -> str:
        if re.search(r"\s|[\x00-\x1f\x7f-\x9f\\]", value):
            raise ValueError("unsafe link")
        parsed = urlsplit(value)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("only HTTP and HTTPS sources are supported")
        if not parsed.hostname or parsed.username is not None or parsed.password is not None:
            raise ValueError("source requires a host and must not contain credentials")
        return value


# --- the guide-only blocks ----------------------------------------------------
#
# Managed site documents keep the four shared blocks (heading, paragraph, list, link). An
# article needs more to be worth reading -- a photo with its licence, a fare table, a
# warning box, a partner button next to the paragraph that made the reader want one -- and
# those live here rather than in the shared union, so a legal page can never carry them and
# the site-pages editor never meets a block it has no fields for.

PlainText = Annotated[str, AfterValidator(plain_text)]

# Self-hosted only: `apps/web/public/guides/<slug>/<name>.<ext>`. A path rather than a URL,
# so an article can never make the reader's browser fetch an image from somewhere else.
IMAGE_SRC_PATTERN = re.compile(
    r"^/guides/[a-z0-9]+(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*\.(?:webp|jpg|png|svg)$"
)
# The hero doubles as the social-card image, and those crawlers do not render SVG.
HERO_SRC_PATTERN = re.compile(
    r"^/guides/[a-z0-9]+(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*\.(?:webp|jpg|png)$"
)
MAX_IMAGE_SIDE = 4000
MAX_TABLE_COLUMNS = 6
MAX_TABLE_ROWS = 30


def image_src(value: str) -> str:
    if not IMAGE_SRC_PATTERN.match(value):
        raise ValueError("image src must be a self-hosted /guides/<slug>/<name>.<ext> path")
    return value


def hero_src(value: str) -> str:
    if not HERO_SRC_PATTERN.match(value):
        raise ValueError("hero src must be a self-hosted raster image under /guides/")
    return value


class ImageCredit(StrictModel):
    """Who made the picture and under what terms. Required for every photograph the site did
    not take itself; a self-drawn diagram credits the site."""

    author: NonemptyText = Field(max_length=120)
    license: NonemptyText = Field(max_length=60)
    source_url: str | None = Field(default=None, max_length=2000)

    @field_validator("source_url")
    @classmethod
    def safe_source(cls, value: str | None) -> str | None:
        return None if value is None or not value.strip() else safe_http_url(value.strip())


class HeroImage(StrictModel):
    src: Annotated[str, AfterValidator(hero_src)] = Field(max_length=200)
    alt: NonemptyText = Field(max_length=200)
    width: int = Field(ge=1, le=MAX_IMAGE_SIDE, strict=True)
    height: int = Field(ge=1, le=MAX_IMAGE_SIDE, strict=True)
    credit: ImageCredit | None = None


class ImageBlock(StrictModel):
    type: Literal["image"]
    src: Annotated[str, AfterValidator(image_src)] = Field(max_length=200)
    alt: NonemptyText = Field(max_length=200)
    # Both sides are stored so the reader's browser reserves the box before the bytes arrive.
    width: int = Field(ge=1, le=MAX_IMAGE_SIDE, strict=True)
    height: int = Field(ge=1, le=MAX_IMAGE_SIDE, strict=True)
    caption: PlainText = Field(default="", max_length=300)
    credit: ImageCredit | None = None


class TableBlock(StrictModel):
    type: Literal["table"]
    header: list[Annotated[NonemptyText, Field(max_length=120)]] = Field(
        min_length=1, max_length=MAX_TABLE_COLUMNS
    )
    rows: list[list[Annotated[PlainText, Field(max_length=300)]]] = Field(
        min_length=1, max_length=MAX_TABLE_ROWS
    )
    caption: PlainText = Field(default="", max_length=200)

    @model_validator(mode="after")
    def rectangular(self) -> Self:
        if any(len(row) != len(self.header) for row in self.rows):
            raise ValueError("every table row needs one cell per header column")
        return self


class CalloutBlock(StrictModel):
    type: Literal["callout"]
    tone: Literal["tip", "warning", "info"] = "tip"
    title: PlainText = Field(default="", max_length=80)
    text: NonemptyText = Field(max_length=2000)


class OfferBlock(StrictModel):
    """A partner button placed by the editor, next to the paragraph that earns it.

    Which brands show is still the catalog's decision (an approved, verified destination
    offer for that destination and module); the block only says where and for which module.
    `destination_id` overrides the article's own, which is what lets a cross-destination
    notice ("autumn leaves in Tokyo and Kyoto") point each section at its own city. The
    catalog check happens in ``admin_service`` on write, not here: this model also validates
    every stored revision on the public read path, and a destination retired from the
    catalog must degrade to "no button", never to a 500.
    """

    type: Literal["offer"]
    module: AffiliateModule
    destination_id: str | None = Field(default=None, max_length=64)
    heading: PlainText = Field(default="", max_length=120)

    @field_validator("destination_id")
    @classmethod
    def normalize_destination(cls, value: str | None) -> str | None:
        normalized = (value or "").strip().casefold()
        return normalized or None


GuideBlock = Annotated[
    HeadingBlock
    | ParagraphBlock
    | ListBlock
    | LinkBlock
    | ImageBlock
    | TableBlock
    | CalloutBlock
    | OfferBlock,
    Field(discriminator="type"),
]


class GuideDocument(StrictModel):
    title: NonemptyText = Field(max_length=200)
    description: NonemptyText = Field(max_length=500)
    # Optional, and absent from every revision written before it existed: a missing key is
    # not an unknown one, so ``extra="forbid"`` still accepts the old rows.
    hero: HeroImage | None = None
    blocks: list[GuideBlock] = Field(min_length=1, max_length=200)
    sources: list[SourceRef] = Field(default_factory=list, max_length=20)

    @model_validator(mode="after")
    def limit_document_size(self) -> Self:
        if len(json.dumps(self.model_dump(mode="json"), ensure_ascii=False)) > 120_000:
            raise ValueError("document exceeds 120000 characters")
        return self


class PublishedDocument(GuideDocument):
    version: int
    published_at: datetime
    # When the version readers currently see went live. Moves on every republication where
    # ``published_at`` deliberately does not, so a corrected notice can say so and the
    # sitemap's ``lastmod`` can tell a crawler to come back.
    modified_at: datetime


# --- taxonomy -----------------------------------------------------------------


class TopicOption(BaseModel):
    slug: str
    label: str
    section: Section


class TopicList(BaseModel):
    topics: list[TopicOption]


# --- admin writes -------------------------------------------------------------


class ArticleCreate(StrictModel):
    slug: str = Field(min_length=2, max_length=120)
    kind: Kind
    destination_id: str | None = Field(default=None, max_length=64)
    topics: list[str] = Field(default_factory=list, max_length=10)
    valid_until: date | None = None
    document: GuideDocument
    locale: Locale = "zh-TW"

    @field_validator("slug")
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        return article_slug(value)


class ArticleUpdate(StrictModel):
    """Taxonomy only. The text of a translation is changed through its own draft, and
    whether the article is hidden through ``VisibilityWrite``: a classification save must
    never quietly put an article back on the site."""

    expected_version: int = Field(ge=1, le=2_147_483_646, strict=True)
    kind: Kind
    destination_id: str | None = Field(default=None, max_length=64)
    topics: list[str] = Field(default_factory=list, max_length=10)
    valid_until: date | None = None
    featured: bool = False
    display_order: int = Field(default=100, ge=0, le=100_000)


class DraftWrite(StrictModel):
    expected_version: int = Field(ge=1, le=2_147_483_646, strict=True)
    document: GuideDocument


class PublishWrite(StrictModel):
    expected_version: int = Field(ge=1, le=2_147_483_646, strict=True)
    confirmed: bool = Field(strict=True)
    reason: NonemptyText = Field(max_length=500)

    @field_validator("confirmed")
    @classmethod
    def require_confirmation(cls, value: bool) -> bool:
        if not value:
            raise ValueError("publication requires explicit confirmation")
        return value


class RestoreWrite(StrictModel):
    expected_version: int = Field(ge=1, le=2_147_483_646, strict=True)
    revision_id: UUID
    reason: NonemptyText = Field(max_length=500)


class VisibilityWrite(PublishWrite):
    """Hide a whole article from every public surface, or put it back.

    Same weight as withdrawing a translation, so the same gate: explicit confirmation and a
    reason. ``expected_version`` is the article's own version, not a translation's.
    """


VisibilityAction = Literal["hide", "unhide"]


class BatchVisibilityItem(StrictModel):
    id: UUID
    expected_version: int = Field(ge=1, le=2_147_483_646, strict=True)


class BatchVisibilityWrite(StrictModel):
    items: list[BatchVisibilityItem] = Field(min_length=1, max_length=100)
    action: VisibilityAction
    confirmed: bool = Field(strict=True)
    reason: NonemptyText = Field(max_length=500)

    @field_validator("confirmed")
    @classmethod
    def require_confirmation(cls, value: bool) -> bool:
        if not value:
            raise ValueError("batch visibility changes require explicit confirmation")
        return value

    @field_validator("items")
    @classmethod
    def one_row_per_article(cls, value: list[BatchVisibilityItem]) -> list[BatchVisibilityItem]:
        if len({item.id for item in value}) != len(value):
            raise ValueError("each article may appear once")
        return value


# --- admin reads --------------------------------------------------------------


class LocaleState(BaseModel):
    locale: Locale
    version: int
    published_version: int | None
    published_at: datetime | None
    title: str
    updated_at: datetime


class RevisionSummary(BaseModel):
    id: UUID
    version: int
    action: RevisionAction
    created_at: datetime
    created_by_user_id: UUID | None


class RevisionDetail(RevisionSummary):
    document: GuideDocument


class ArticleSummary(BaseModel):
    id: UUID
    slug: str
    kind: Kind
    destination_id: str | None
    destination_label: str | None
    topics: list[TopicOption]
    valid_until: date | None
    expired: bool
    featured: bool
    display_order: int
    is_active: bool
    status: ArticleStatus
    version: int
    locales: list[LocaleState]
    updated_at: datetime


class FacetCount(BaseModel):
    code: str
    count: int


class ArticleFacets(BaseModel):
    status: list[FacetCount]
    kind: list[FacetCount]


class ArticleList(BaseModel):
    articles: list[ArticleSummary]
    total: int
    page: int
    pages: int
    facets: ArticleFacets


class BatchVisibilityResult(BaseModel):
    updated: int
    # Rows already in the requested state. They keep their version and get no audit row,
    # so an editor who clicks twice does not fabricate history.
    skipped: int
    status: Literal["hidden", "active"]
    articles: list[ArticleSummary]


class ArticleDetail(ArticleSummary):
    locale: Locale
    draft: GuideDocument
    published: PublishedDocument | None
    revisions: list[RevisionSummary]
    audit: list[AdminAuditView]


# --- public reads -------------------------------------------------------------


class PublicSummary(BaseModel):
    slug: str
    kind: Kind
    destination_id: str | None
    destination_label: str | None
    topics: list[TopicOption]
    title: str
    description: str
    hero: HeroImage | None = None
    published_at: datetime
    valid_until: date | None
    featured: bool


class PublicList(BaseModel):
    articles: list[PublicSummary]
    next_cursor: str | None = None


class PublicArticle(BaseModel):
    slug: str
    kind: Kind
    locale: Locale
    status: Literal["published", "unpublished"]
    destination_id: str | None = None
    destination_label: str | None = None
    topics: list[TopicOption] = Field(default_factory=list)
    valid_until: date | None = None
    # An expired notice keeps its page. Withdrawing the URL would 404 every link already
    # pointing at it; the page says plainly what date it applied until instead. It leaves
    # the listings and the sitemap, which is where "current" is what the reader expects.
    expired: bool = False
    document: PublishedDocument | None = None
    # Only the locales this article is genuinely published in. The web layer turns this
    # into hreflang, so an unwritten translation is never advertised as one.
    published_locales: list[Locale] = Field(default_factory=list)


class SitemapEntry(BaseModel):
    kind: Kind
    slug: str
    locale: Locale
    published_at: datetime
    # The current public version's own timestamp: the honest ``lastmod``. Optional on the
    # wire so a web layer built against the older shape keeps parsing the file.
    modified_at: datetime | None = None


class SitemapList(BaseModel):
    entries: list[SitemapEntry]
