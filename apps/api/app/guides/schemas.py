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
from app.affiliates.content_links import ContentCategory
from app.affiliates.schemas import AffiliateModule
from app.guides.publication import ArticleStatus
from app.i18n import LOCALES, Locale
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
# How a public listing is ordered. ``latest`` is publication time, newest first -- right for
# dated intel. ``curated`` is the editor's order: featured first, then ``display_order``,
# then newest, then the slug -- what a hub's "featured guides" and the lifestyle listing
# want, so an overview piece stays on page one however many batches follow it. ``news`` is
# the day the news happened, newest first, undated rows last -- what a news list wants,
# since a batch import gives a week of stories the same publication time.
ListSort = Literal["latest", "curated", "news"]
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
    # A diagram's long description: the fares, times and labels its ``<desc>`` states, as text
    # in the document, so a page that references the file rather than inlining it still
    # carries them. Drawn folded under the caption; empty for a photograph. Capped where a
    # paragraph is.
    description: PlainText = Field(default="", max_length=4000)
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


def code_text(value: str) -> str:
    """Code is displayed as escaped text, never interpreted as HTML or Markdown."""
    if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", value):
        raise ValueError("unsupported control character in code")
    return value.replace("\r\n", "\n").replace("\r", "\n")


class TextInline(StrictModel):
    type: Literal["text"]
    text: str = Field(min_length=1, max_length=4000)

    @field_validator("text")
    @classmethod
    def safe_text(cls, value: str) -> str:
        plain_text(value)
        return value  # preserve spaces between adjacent inline nodes


class CodeInline(StrictModel):
    type: Literal["code"]
    text: Annotated[str, AfterValidator(code_text)] = Field(min_length=1, max_length=1000)


class LinkInline(StrictModel):
    type: Literal["link"]
    text: NonemptyText = Field(max_length=500)
    url: Annotated[str, AfterValidator(safe_http_url)] = Field(max_length=2000)


class ArticleInline(StrictModel):
    type: Literal["article"]
    text: NonemptyText = Field(max_length=500)
    kind: Kind = "life"
    slug: Annotated[str, AfterValidator(article_slug)] = Field(max_length=120)


Inline = Annotated[
    TextInline | CodeInline | LinkInline | ArticleInline, Field(discriminator="type")
]


class RichParagraphBlock(StrictModel):
    type: Literal["rich_paragraph"]
    inlines: list[Inline] = Field(min_length=1, max_length=80)

    @model_validator(mode="after")
    def limit_text(self) -> Self:
        if sum(len(node.text) for node in self.inlines) > 4000:
            raise ValueError("paragraph exceeds 4000 characters")
        return self


class CodeBlock(StrictModel):
    type: Literal["code"]
    language: Literal[
        "text",
        "powershell",
        "bash",
        "json",
        "markdown",
        "html",
        "css",
        "javascript",
        "typescript",
        "python",
        "yaml",
        "sh",
        "shell",
        "toml",
        "csv",
    ] = "text"
    label: NonemptyText = Field(max_length=160)
    code: Annotated[str, AfterValidator(code_text)] = Field(min_length=1, max_length=24000)

    @field_validator("code")
    @classmethod
    def require_code(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("code must contain visible text")
        return value


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


def https_url(value: str) -> str:
    safe_http_url(value)
    if urlsplit(value).scheme != "https":
        raise ValueError("partner links must use HTTPS")
    return value


class PartnerLinkBlock(StrictModel):
    """A link to a non-travel affiliate program, placed by the editor where it earns its place.

    Unlike an offer, the URL is the program's own: its terms forbid hiding the traffic source
    behind a redirect (``app.affiliates.content_links``). Whether the partner is known and the
    URL belongs to it is checked against that registry on write and again on every read, never
    here: this model also validates stored revisions on the public read path, and a program
    later removed from the registry must degrade to "no link", never to a 500. That is also why
    ``partner`` is a code-shaped string rather than a literal of today's codes.
    """

    type: Literal["partner_link"]
    partner: str = Field(pattern=r"^[a-z0-9_]{2,32}$")
    url: Annotated[str, AfterValidator(https_url)] = Field(min_length=1, max_length=2000)
    label: NonemptyText = Field(max_length=80)
    note: PlainText = Field(default="", max_length=200)


class SummaryBlock(StrictModel):
    """The article's answer, in two to five sentences a reader (or an answer engine) can
    take away without reading further. One per article, ahead of the first section: it is
    the opening, not a recap. Drafted from the article's own text -- lifted from a
    「先講結論」 lead, or written by the model and read by the owner batch by batch before
    ``pack_cli summarize --from`` applies it (the owner's decision of 2026-09-16) -- and
    never a fact the body does not state: an article whose summary the text does not
    support is worse than one without."""

    type: Literal["summary"]
    items: list[Annotated[NonemptyText, Field(max_length=300)]] = Field(
        min_length=2, max_length=5
    )


class FaqItem(StrictModel):
    question: NonemptyText = Field(max_length=200)
    answer: NonemptyText = Field(max_length=1000)


class FaqBlock(StrictModel):
    """Questions readers actually ask, each with its answer, as a section of the article.
    One per article. Google has shown FAQ rich results only for government and health
    sites since 2023; the value here is the reader and the answer engines."""

    type: Literal["faq"]
    items: list[FaqItem] = Field(min_length=2, max_length=10)


GuideBlock = Annotated[
    HeadingBlock
    | ParagraphBlock
    | ListBlock
    | LinkBlock
    | ImageBlock
    | TableBlock
    | CalloutBlock
    | OfferBlock
    | PartnerLinkBlock
    | RichParagraphBlock
    | CodeBlock
    | SummaryBlock
    | FaqBlock,
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

    @model_validator(mode="after")
    def one_summary_one_faq(self) -> Self:
        """At most one summary and one FAQ, and the summary before the first section: a
        summary halfway down is a recap, and two of them contradict each other."""
        if sum(isinstance(block, SummaryBlock) for block in self.blocks) > 1:
            raise ValueError("an article carries at most one summary block")
        if sum(isinstance(block, FaqBlock) for block in self.blocks) > 1:
            raise ValueError("an article carries at most one faq block")
        for block in self.blocks:
            if isinstance(block, HeadingBlock):
                break
            if isinstance(block, SummaryBlock):
                return self
        if any(isinstance(block, SummaryBlock) for block in self.blocks):
            raise ValueError("the summary block belongs before the first heading")
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
    # The parent's slug for a sub-topic, or None at the top level. Optional on the wire so
    # a web build older than the two-level vocabulary keeps parsing the list.
    parent: str | None = None
    # The topic hub's lead paragraph in the reader's language, when the topic has one.
    description: str | None = None
    # Published articles under this topic in the request locale, and in every locale, so a
    # hub page can decide its own indexability and its hreflang set from one read. A parent
    # counts the distinct union of itself and its children.
    count: int = 0
    counts: dict[str, int] = Field(default_factory=dict)


class TopicList(BaseModel):
    topics: list[TopicOption]


def _topic_names(value: dict[str, str]) -> dict[str, str]:
    """Every locale, each a non-empty label. ``topic_label`` would show the slug where a
    label is missing, which is honest but not what an editor meant to publish."""
    cleaned = {locale: plain_text(text).strip() for locale, text in value.items()}
    missing = [locale for locale in LOCALES if not cleaned.get(locale)]
    if missing:
        raise ValueError(f"a label is needed in every locale: {', '.join(missing)}")
    return cleaned


def _topic_descriptions(value: dict[str, str] | None) -> dict[str, str] | None:
    """A lead per locale; a locale left out or emptied simply has none."""
    if value is None:
        return None
    return {locale: plain_text(text).strip() for locale, text in value.items() if text.strip()}


class TopicCreate(StrictModel):
    """A topic an editor adds without a deploy: the seed migrations only ever insert slugs
    that are absent, so a row with ``source='admin'`` survives every later seed."""

    slug: str = Field(min_length=2, max_length=64)
    section: Section
    names: dict[Locale, str]
    display_order: int = Field(default=100, ge=0, le=100_000)
    # A top-level topic of the same section, for a sub-topic; None for a top-level one.
    parent_slug: str | None = Field(default=None, max_length=64)
    descriptions: dict[Locale, str] | None = None

    @field_validator("slug")
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        return article_slug(value)

    @field_validator("names")
    @classmethod
    def every_locale(cls, value: dict[str, str]) -> dict[str, str]:
        return _topic_names(value)

    @field_validator("descriptions")
    @classmethod
    def clean_descriptions(cls, value: dict[str, str] | None) -> dict[str, str] | None:
        return _topic_descriptions(value)


class TopicUpdate(StrictModel):
    """Only what is given changes. The section never does: articles carry it."""

    names: dict[Locale, str] | None = None
    display_order: int | None = Field(default=None, ge=0, le=100_000)
    is_active: bool | None = None
    # ``None`` leaves the parent alone, ``""`` clears it, a slug sets it.
    parent_slug: str | None = Field(default=None, max_length=64)
    descriptions: dict[Locale, str] | None = None

    @field_validator("names")
    @classmethod
    def every_locale(cls, value: dict[str, str] | None) -> dict[str, str] | None:
        return None if value is None else _topic_names(value)

    @field_validator("descriptions")
    @classmethod
    def clean_descriptions(cls, value: dict[str, str] | None) -> dict[str, str] | None:
        return _topic_descriptions(value)


class AdminTopic(TopicOption):
    """A topic as the editor sees it: every label and lead, not only the reader's."""

    names: dict[str, str]
    descriptions: dict[str, str]
    display_order: int
    is_active: bool
    source: str


class DestinationFacet(BaseModel):
    """One destination with at least one published article in the request locale."""

    id: str
    label: str
    country: str
    country_label: str
    count: int


class DestinationFacetList(BaseModel):
    destinations: list[DestinationFacet]


class ContentPartnerOption(BaseModel):
    code: str
    display_name: str
    category: ContentCategory
    hosts: list[str]


class ContentPartnerList(BaseModel):
    partners: list[ContentPartnerOption]


# --- admin writes -------------------------------------------------------------


class ArticleCreate(StrictModel):
    slug: str = Field(min_length=2, max_length=120)
    kind: Kind
    destination_id: str | None = Field(default=None, max_length=64)
    topics: list[str] = Field(default_factory=list, max_length=10)
    valid_until: date | None = None
    news_date: date | None = None
    document: GuideDocument
    locale: Locale = "zh-TW"

    @field_validator("slug")
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        return article_slug(value)


# Another name a reader may type for an article (``ML``, ``機器學習``). Per locale, and few:
# a dozen is a glossary entry's worth, more is a keyword list nobody reviews.
Alias = Annotated[str, Field(min_length=1, max_length=120)]
MAX_ALIASES_PER_LOCALE = 12
# Editor-chosen further reading. Four is what the end of an article can show without the
# grid reading as a listing.
MAX_RELATED = 4
AliasMap = dict[Locale, Annotated[list[Alias], Field(max_length=MAX_ALIASES_PER_LOCALE)]]
RelatedSlugs = Annotated[list[str], Field(max_length=MAX_RELATED)]


class ArticleUpdate(StrictModel):
    """Taxonomy only. The text of a translation is changed through its own draft, and
    whether the article is hidden through ``VisibilityWrite``: a classification save must
    never quietly put an article back on the site."""

    expected_version: int = Field(ge=1, le=2_147_483_646, strict=True)
    kind: Kind
    destination_id: str | None = Field(default=None, max_length=64)
    topics: list[str] = Field(default_factory=list, max_length=10)
    valid_until: date | None = None
    # Left out, the stored date stays; ``null`` clears it. Unlike ``valid_until``, which an
    # editor always sends: this field arrived after the form did, and a save from a form
    # that does not know it must not wipe every news article's date.
    news_date: date | None = None
    featured: bool = False
    display_order: int = Field(default=100, ge=0, le=100_000)
    # ``None`` leaves the names alone; a locale listed here replaces that locale's
    # editor-written names (``[]`` clears them). Names the seed wrote (glossary, keyword
    # list, series catalogue) are not the editor's to lose and stay either way.
    aliases: AliasMap | None = None
    # ``None`` leaves the list alone; a list replaces it, in the order shown.
    related: RelatedSlugs | None = None

    @field_validator("related")
    @classmethod
    def normalize_related(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return None
        return list(dict.fromkeys(article_slug(slug) for slug in value if slug.strip()))


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
    news_date: date | None = None
    expired: bool
    featured: bool
    display_order: int
    is_active: bool
    status: ArticleStatus
    version: int
    locales: list[LocaleState]
    updated_at: datetime
    # The editor-written names per locale and the curated further reading, filled on the
    # detail read (the list has no use for them and would pay a query per row).
    aliases: dict[str, list[str]] = Field(default_factory=dict)
    related: list[str] = Field(default_factory=list)


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
    # The day the news happened (see ``GuideArticle.news_date``); null off the news topics.
    news_date: date | None = None
    featured: bool


class PublicList(BaseModel):
    articles: list[PublicSummary]
    next_cursor: str | None = None


class GuideSearchHit(PublicSummary):
    """A result card: the summary plus the passage the match was found in."""

    # A passage of the body around the first matched term, or the description when the
    # match sits in the title or the aliases only. Plain text; the web marks the terms.
    snippet: str
    # The terms the query was parsed into, folded, so the web can highlight them.
    matched: list[str]


class GuideSearchResult(BaseModel):
    query: str
    total: int
    offset: int
    limit: int
    results: list[GuideSearchHit]
    # The article whose alias or title *is* the query, shown above the ranked list and
    # left out of it.
    best_match: PublicSummary | None = None
    next_offset: int | None = None


class PublicPartnerLink(BaseModel):
    """One partner link the reader may see, resolved against the registry at read time.

    The web draws a ``partner_link`` block only when its partner and URL match an entry here,
    so a program removed from the registry leaves every published article at the next deploy
    without anyone editing one. ``key`` names the link for the click endpoint.
    """

    key: str
    partner: str
    display_name: str
    url: str


class ArticleReference(BaseModel):
    kind: Kind
    slug: str
    title: str
    # The published description, when the reference was built from a published revision:
    # what a definition card shows under a term link. Optional so a reference built
    # elsewhere (a catalogue row, an older API) still parses.
    description: str | None = None


class SeriesEntry(ArticleReference):
    number: int
    group: str
    level: str
    platforms: list[str]
    aliases: list[str]
    description: str
    minutes: int
    operation_minutes: int | None = None


class SeriesGroup(BaseModel):
    id: str
    title: str


class SeriesPath(BaseModel):
    id: str
    title: str
    slugs: list[str]


class PublicSeries(BaseModel):
    slug: str
    locale: Locale
    hub: ArticleReference
    groups: list[SeriesGroup]
    paths: list[SeriesPath]
    entries: list[SeriesEntry]


SeriesSource = Literal["api-series", "web-gemini", "catalogue"]


class SeriesSummary(BaseModel):
    """One series or tutorial hub the reader can enter from a section page. ``entries`` is
    the catalogue's count where the API holds the catalogue, and unknown otherwise."""

    slug: str
    section: Section
    hub: ArticleReference
    source: SeriesSource
    topic: str | None = None
    entries: int | None = None


class SeriesIndex(BaseModel):
    series: list[SeriesSummary]


class SeriesNavigation(BaseModel):
    slug: str
    hub: ArticleReference
    current: SeriesEntry | None = None
    previous: ArticleReference | None = None
    next: ArticleReference | None = None
    prerequisites: list[ArticleReference] = Field(default_factory=list)
    related: list[ArticleReference] = Field(default_factory=list)


class PublicArticle(BaseModel):
    slug: str
    kind: Kind
    locale: Locale
    status: Literal["published", "unpublished"]
    destination_id: str | None = None
    destination_label: str | None = None
    topics: list[TopicOption] = Field(default_factory=list)
    valid_until: date | None = None
    news_date: date | None = None
    # An expired notice keeps its page. Withdrawing the URL would 404 every link already
    # pointing at it; the page says plainly what date it applied until instead. It leaves
    # the listings and the sitemap, which is where "current" is what the reader expects.
    expired: bool = False
    document: PublishedDocument | None = None
    # Only the locales this article is genuinely published in. The web layer turns this
    # into hreflang, so an unwritten translation is never advertised as one.
    published_locales: list[Locale] = Field(default_factory=list)
    # Empty under an expired notice, for the reason offers disappear there: a purchase link
    # beneath advice that no longer applies reads as bait.
    partner_links: list[PublicPartnerLink] = Field(default_factory=list)
    article_links: list[ArticleReference] = Field(default_factory=list)
    series: SeriesNavigation | None = None
    # Further reading: the editor's picks first, then articles that share a sub-topic, a
    # parent topic, a destination or a series group (``links.related_articles``). Ordinary
    # links, so they stay under an expired notice where the partner buttons do not.
    related: list[ArticleReference] = Field(default_factory=list)
    # Published articles whose text links here, newest first.
    backlinks: list[ArticleReference] = Field(default_factory=list)
    # The other names this article answers to in this locale (glossary, keyword list and
    # editor; not a series catalogue's keyword hints).
    aliases: list[str] = Field(default_factory=list)
    # The glossary this article is an entry of, when it belongs to a catalogue-type series
    # (``series_registry.json``): the web marks such an article up as a DefinedTerm in that set.
    term_set: ArticleReference | None = None


class SitemapEntry(BaseModel):
    kind: Kind
    slug: str
    locale: Locale
    published_at: datetime
    # When the current public version went live -- the honest lastmod. A damaged public
    # revision pointer is excluded from the sitemap because its article page cannot render.
    modified_at: datetime | None = None
    # Every locale this article is published in, so a child sitemap that holds one locale can
    # still name the article's other translations as alternates.
    locales: list[Locale] = Field(default_factory=list)


class SitemapList(BaseModel):
    entries: list[SitemapEntry]
    # Present when rows follow; None on the last page. The opaque keyset is (slug, locale),
    # independent of publication timestamps and editorial ordering.
    next_cursor: str | None = None


class SitemapCount(BaseModel):
    kind: Kind
    locale: Locale
    count: int


class SitemapSummary(BaseModel):
    """How many published rows each kind has in each locale: what the sitemap index and the
    section hubs need, without paging through every row to learn it."""

    counts: list[SitemapCount]
