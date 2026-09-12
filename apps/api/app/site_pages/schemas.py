from __future__ import annotations

import json
import re
from datetime import date, datetime
from typing import Annotated, Literal, Self
from urllib.parse import unquote, urlsplit
from uuid import UUID

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    TypeAdapter,
    field_validator,
    model_validator,
)

from app.admin.schemas import AdminAuditView
from app.i18n import Locale

PageSlug = Literal["privacy", "terms", "about", "contact"]
PAGE_SLUGS: tuple[PageSlug, ...] = ("privacy", "terms", "about", "contact")
RequirementKey = Literal["operator", "location", "contact", "retention", "legal"]
REQUIRED_FIELDS: dict[str, tuple[RequirementKey, ...]] = {
    "privacy": ("operator", "location", "contact", "retention", "legal"),
    "terms": ("operator", "location", "contact", "retention", "legal"),
    "about": ("operator", "location", "contact"),
    "contact": ("operator", "location", "contact"),
}


def plain_text(value: str) -> str:
    normalized = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    if re.search(r"[\x00-\x09\x0b-\x1f\x7f-\x9f]", normalized):
        raise ValueError("control characters are not supported")
    if re.search(r"<[!/?A-Za-z]", normalized):
        raise ValueError("HTML is not supported; use structured blocks")
    return normalized


def nonempty_text(value: str) -> str:
    normalized = plain_text(value)
    if not normalized:
        raise ValueError("text cannot be blank")
    return normalized


NonemptyText = Annotated[str, AfterValidator(nonempty_text)]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class HeadingBlock(StrictModel):
    type: Literal["heading"]
    text: NonemptyText = Field(max_length=200)
    level: Literal[2, 3] = 2


class ParagraphBlock(StrictModel):
    type: Literal["paragraph"]
    text: NonemptyText = Field(max_length=4000)


class ListBlock(StrictModel):
    type: Literal["list"]
    items: list[Annotated[NonemptyText, Field(max_length=2000)]] = Field(
        min_length=1, max_length=30
    )
    ordered: bool = False


def safe_http_url(value: str) -> str:
    """An absolute http(s) URL with a host and no credentials, whitespace or control bytes.

    Shared by the link block here and the guide image credits, so one tightened rule cannot
    reach one surface and miss the other.
    """
    if re.search(r"\s|[\x00-\x1f\x7f-\x9f\\]", value):
        raise ValueError("unsafe link")
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("only HTTP and HTTPS links are supported")
    if not parsed.hostname or parsed.username is not None or parsed.password is not None:
        raise ValueError("link requires a host and must not contain credentials")
    _ = parsed.port  # Reject malformed ports, including out-of-range values.
    return value


class LinkBlock(StrictModel):
    type: Literal["link"]
    text: NonemptyText = Field(max_length=200)
    url: str = Field(min_length=1, max_length=2000)

    @field_validator("url")
    @classmethod
    def safe_link(cls, value: str) -> str:
        if re.search(r"\s|[\x00-\x1f\x7f-\x9f\\]", value):
            raise ValueError("unsafe link")
        parsed = urlsplit(value)
        if parsed.scheme in {"http", "https"}:
            return safe_http_url(value)
        if parsed.scheme == "mailto":
            if parsed.netloc or parsed.query or parsed.fragment:
                raise ValueError("mail links must contain only an email address")
            address = unquote(parsed.path, encoding="utf-8", errors="strict")
            if re.search(r"[\x00-\x1f\x7f-\x9f]", address):
                raise ValueError("mail links must not contain encoded control characters")
            TypeAdapter(EmailStr).validate_python(address)
            return value
        raise ValueError("only HTTP, HTTPS and mailto links are supported")


ContentBlock = Annotated[
    HeadingBlock | ParagraphBlock | ListBlock | LinkBlock, Field(discriminator="type")
]


class PageRequirements(StrictModel):
    operator: str = Field(default="", max_length=4000)
    location: str = Field(default="", max_length=4000)
    contact: str = Field(default="", max_length=4000)
    retention: str = Field(default="", max_length=4000)
    legal: str = Field(default="", max_length=4000)

    @field_validator("operator", "location", "contact", "retention", "legal")
    @classmethod
    def normalize(cls, value: str) -> str:
        return plain_text(value)


class PageDocument(StrictModel):
    title: NonemptyText = Field(max_length=200)
    description: NonemptyText = Field(max_length=500)
    blocks: list[ContentBlock] = Field(min_length=1, max_length=100)
    effective_date: date | None = None
    requirements: PageRequirements = Field(default_factory=PageRequirements)

    @model_validator(mode="after")
    def limit_document_size(self) -> Self:
        if len(json.dumps(self.model_dump(mode="json"), ensure_ascii=False)) > 60_000:
            raise ValueError("document exceeds 60000 characters")
        return self


class DraftWrite(StrictModel):
    expected_version: int = Field(ge=1, le=2_147_483_646, strict=True)
    document: PageDocument


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


class PublishedDocument(PageDocument):
    version: int
    published_at: datetime


class RevisionSummary(BaseModel):
    id: UUID
    version: int
    action: Literal["initialized", "draft_saved", "published", "restored"]
    created_at: datetime
    created_by_user_id: UUID | None


class RevisionDetail(RevisionSummary):
    document: PageDocument


class PageSummary(BaseModel):
    slug: PageSlug
    locale: Locale
    version: int
    published_version: int | None
    updated_at: datetime
    pending_requirements: list[str]


class PageDetail(PageSummary):
    draft: PageDocument
    published: PublishedDocument | None
    revisions: list[RevisionSummary]
    audit: list[AdminAuditView]


class PageList(BaseModel):
    pages: list[PageSummary]


class InitializationResult(PageList):
    created: int


class PublicPage(BaseModel):
    slug: PageSlug
    locale: Locale
    status: Literal["published", "unpublished"]
    document: PublishedDocument | None
