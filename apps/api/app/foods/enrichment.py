"""Fill the descriptive gaps of a food merchant from pages someone actually verified.

Two callers share this module. The Gemini catalog review proposes corrections it found
through Google Search grounding and independently fetched pages; the JSON importer carries
what a researcher confirmed in a browser. Both end here, because the rules about what may
be written are the same and must never drift apart:

* A page from Google, Naver or Michelin is never a source (``validate_editorial_url``), and
  neither is a review aggregator, reservation platform or social network (``PLATFORM_HOSTS``).
  Those sites may have led a researcher to the merchant, but the stored source has to be the
  merchant's own site or a tourism board's page about that one merchant.
* Only empty scalar fields are filled. An administrator's address, official site or 商圈 is
  never overwritten by a batch; the caller reports the skip instead.
* Sources are upserted by URL, never duplicated, and categories are only ever added.
* A Google Place ID is a pointer the importer may carry (read off the branch's own Maps
  page); it is written only when the merchant has none and no other merchant owns it.
* Coordinates, ``naver_map_url``, ``map_match_status``, ``review_status``, ``is_active`` and
  the verification stamps are never touched. Publication still needs a durable coordinate
  and a human approval, exactly as before.
"""

from __future__ import annotations

import unicodedata
from collections.abc import Collection
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal
from urllib.parse import urlsplit
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.catalog_review.evidence import is_trusted_source, normalize_source_url
from app.catalog_review.repository import TRUSTED_SOURCE_HOSTS
from app.foods.admin_router import (
    SLUG_FIELD_PATTERN,
    _validate_category_slugs,
    _validate_merchant_taxonomy,
)
from app.foods.platform_links import PLATFORMS_BY_PROVIDER
from app.models import (
    AdminAuditLog,
    FoodCategory,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantSource,
)
from app.problems import AppError
from app.restaurants.editorial import validate_editorial_url
from app.restaurants.imports import PLACE_ID_RE

AUDIT_ACTION = "food_merchant_enriched"
MAX_AUDIT_EVIDENCE = 10

#: Review aggregators, reservation platforms, delivery apps and social networks. Their
#: pages are evidence that a merchant exists, never a source about it: the seed tests have
#: pinned Tabelog, Gurunavi, HotPepper and Retty out since 2026-09-06, and the reservation
#: platforms are stored as reviewed links, not as sources. Matched by host suffix.
PLATFORM_HOSTS: frozenset[str] = frozenset(
    {
        "tabelog.com",
        "gnavi.co.jp",
        "hotpepper.jp",
        "retty.me",
        "openrice.com",
        "catchtable.co.kr",
        "catchtable.net",
        "tripadvisor.com",
        "yelp.com",
        "facebook.com",
        "fb.com",
        "instagram.com",
        "twitter.com",
        "x.com",
        "tiktok.com",
        "youtube.com",
        "line.me",
        "linktr.ee",
        "tablecheck.com",
        "ikyu.com",
        "toreta.in",
        "omakase.in",
        "pocket-concierge.jp",
        "chope.co",
        "eztable.com",
        "hungryhub.com",
        "pasgo.vn",
        "inline.app",
        "sevenrooms.com",
        "myconciergejapan.com",
        "klook.com",
        "kkday.com",
        "ubereats.com",
        "foodpanda.com",
        "wolt.com",
        "demae-can.com",
        "loco.yahoo.co.jp",
    }
    | {host for item in PLATFORMS_BY_PROVIDER.values() for host in item.hosts}
)
#: Brands whose country domains vary (tripadvisor.com.tw, tabelog.com/en …): any host
#: label equal to one of these is a platform, the way ``normalize_source_url`` treats google.
PLATFORM_LABELS: frozenset[str] = frozenset(
    {"tripadvisor", "yelp", "tabelog", "gnavi", "hotpepper", "retty", "openrice", "catchtable"}
)
#: Gurunavi hosts merchants' *own* official pages under gorp.jp; the 2026-09-06 source
#: review accepted them as ``merchant_website``, so they must not fall to the gnavi label.
HOSTED_OFFICIAL_SUFFIXES: tuple[str, ...] = ("gorp.jp",)

CorrectionField = Literal[
    "address", "official_website_url", "listing_source_url", "area_slug", "category_slug"
]
CORRECTION_KINDS: dict[str, str] = {
    "address": "address",
    "official_website_url": "merchant_website",
    "listing_source_url": "merchant_listing",
    "area_slug": "area",
    "category_slug": "category",
}


def _host(url: str) -> str:
    return (urlsplit(url).hostname or "").casefold().rstrip(".").removeprefix("www.")


def is_platform_host(url: str) -> bool:
    """Whether this URL belongs to a site that may be evidence but never a source."""
    host = _host(url)
    if not host:
        return False
    if any(host == item or host.endswith(f".{item}") for item in HOSTED_OFFICIAL_SUFFIXES):
        return False
    if any(host == item or host.endswith(f".{item}") for item in PLATFORM_HOSTS):
        return True
    return any(label in PLATFORM_LABELS for label in host.split("."))


def normalized_text(value: str) -> str:
    """NFKC, casefolded, alphanumerics only — the same shape catalog review compares by."""
    return "".join(
        char for char in unicodedata.normalize("NFKC", value).casefold() if char.isalnum()
    )


def _check_source_url(url: str) -> str:
    validate_editorial_url(url)
    if normalize_source_url(url) is None:
        raise ValueError("來源必須是公開的 HTTPS 網址")
    if is_platform_host(url):
        raise ValueError("評論聚合站、訂位平台或社群頁面不能作為店家來源")
    return url


class EnrichmentSourceProposal(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    url: str = Field(min_length=8, max_length=2048)
    title: str = Field(min_length=1, max_length=255)
    quote: str = Field(default="", max_length=300)


class EnrichmentListingProposal(EnrichmentSourceProposal):
    source_type: Literal["official_tourism"] = "official_tourism"


class MerchantEnrichmentProposal(BaseModel):
    """What one caller wants written; every field is optional and independently applied."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    address: str | None = Field(default=None, min_length=1, max_length=1000)
    official_website: EnrichmentSourceProposal | None = None
    listing_source: EnrichmentListingProposal | None = None
    area_slug: str | None = Field(default=None, pattern=SLUG_FIELD_PATTERN, max_length=128)
    category_slugs: list[str] = Field(default_factory=list, max_length=6)
    google_place_id: str | None = Field(default=None, min_length=10, max_length=255)

    @model_validator(mode="after")
    def validate_sources(self) -> MerchantEnrichmentProposal:
        _validate_category_slugs(self.category_slugs)
        if self.official_website is not None:
            _check_source_url(self.official_website.url)
        if self.listing_source is not None:
            _check_source_url(self.listing_source.url)
        if self.google_place_id is not None and not PLACE_ID_RE.fullmatch(self.google_place_id):
            raise ValueError("Google Place ID 格式不正確")
        return self

    @property
    def empty(self) -> bool:
        return not (
            self.address
            or self.official_website
            or self.listing_source
            or self.area_slug
            or self.category_slugs
            or self.google_place_id
        )


class EnrichmentOrigin(BaseModel):
    """Who is writing: the reviewed Gemini run, or a researched JSON batch."""

    model_config = ConfigDict(extra="forbid")
    kind: Literal["catalog_review", "json_import"]
    reference: str = Field(min_length=1, max_length=255)

    @property
    def category_source(self) -> str:
        return "gemini" if self.kind == "catalog_review" else "admin"


@dataclass
class EnrichmentOutcome:
    applied: dict[str, Any] = field(default_factory=dict)
    skipped: dict[str, str] = field(default_factory=dict)
    sources_added: list[str] = field(default_factory=list)
    sources_refreshed: list[str] = field(default_factory=list)
    categories_added: list[str] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        """A re-verified source alone is bookkeeping, not a change worth an audit row."""
        return bool(self.applied or self.sources_added or self.categories_added)

    def as_dict(self) -> dict[str, Any]:
        return {
            "applied": dict(self.applied),
            "skipped": dict(self.skipped),
            "sources_added": list(self.sources_added),
            "sources_refreshed": list(self.sources_refreshed),
            "categories_added": list(self.categories_added),
        }


def proposal_from_corrections(corrections: list[dict[str, Any]]) -> MerchantEnrichmentProposal:
    """Fold the corrections a review item recorded into one proposal.

    A Place ID is deliberately not a correction field: the Gemini path gets it from the
    Google matcher during the identify phase, never from model output.
    """
    values: dict[str, Any] = {"category_slugs": []}
    for entry in corrections:
        field_name = entry.get("field")
        value = entry.get("value")
        if not isinstance(value, str) or not value.strip():
            continue
        if field_name == "address" and "address" not in values:
            values["address"] = value
        elif field_name == "official_website_url" and "official_website" not in values:
            values["official_website"] = {
                "url": value,
                "title": str(entry.get("title") or _host(value) or value)[:255],
                "quote": str(entry.get("quote") or "")[:300],
            }
        elif field_name == "listing_source_url" and "listing_source" not in values:
            values["listing_source"] = {
                "url": value,
                "title": str(entry.get("title") or _host(value) or value)[:255],
                "quote": str(entry.get("quote") or "")[:300],
            }
        elif field_name == "area_slug" and "area_slug" not in values:
            values["area_slug"] = value
        elif field_name == "category_slug" and value not in values["category_slugs"]:
            values["category_slugs"].append(value)
    return MerchantEnrichmentProposal.model_validate(values)


def _mentions(text: str, needle: str | None) -> bool:
    return bool(needle) and normalized_text(needle or "") in normalized_text(text)


def _claims(base: list[str], *, quote: str, address: str | None) -> list[str]:
    claims = list(base)
    if address and _mentions(quote, address) and "address" not in claims:
        claims.append("address")
    return claims


async def _current_state(
    session: AsyncSession, merchant: FoodMerchant
) -> tuple[list[FoodMerchantSource], list[FoodMerchantCategory], list[str]]:
    sources = list(
        (
            await session.scalars(
                select(FoodMerchantSource)
                .where(FoodMerchantSource.merchant_id == merchant.id)
                .order_by(FoodMerchantSource.id)
            )
        ).all()
    )
    categories = list(
        (
            await session.scalars(
                select(FoodMerchantCategory)
                .where(FoodMerchantCategory.merchant_id == merchant.id)
                .order_by(FoodMerchantCategory.display_order, FoodMerchantCategory.id)
            )
        ).all()
    )
    slugs_by_id: dict[UUID, str] = {}
    if categories:
        slugs_by_id = {
            row.id: row.slug
            for row in (
                await session.scalars(
                    select(FoodCategory).where(
                        FoodCategory.id.in_([row.category_id for row in categories])
                    )
                )
            ).all()
        }
    slugs = [slugs_by_id[row.category_id] for row in categories if row.category_id in slugs_by_id]
    return sources, categories, slugs


def _summary(
    merchant: FoodMerchant,
    sources: list[FoodMerchantSource],
    category_slugs: list[str],
) -> dict[str, Any]:
    return {
        "address": merchant.address,
        "official_website_url": merchant.official_website_url,
        "area_id": str(merchant.area_id) if merchant.area_id else None,
        "google_place_id": merchant.google_place_id,
        "category_slugs": list(category_slugs),
        "source_urls": [source.source_url for source in sources if source.is_current],
    }


def _upsert_source(
    session: AsyncSession,
    merchant: FoodMerchant,
    sources: list[FoodMerchantSource],
    outcome: EnrichmentOutcome,
    *,
    source_type: str,
    source_scope: str,
    title: str,
    url: str,
    claims: list[str],
    now: datetime,
) -> None:
    for existing in sources:
        if existing.source_url == url and existing.edition_year is None:
            merged = list(existing.claims_json or [])
            merged.extend(claim for claim in claims if claim not in merged)
            # Reassigned, not mutated: a JSON column only turns dirty on assignment.
            existing.claims_json = merged
            existing.is_current = True
            existing.last_verified_at = now
            if url not in outcome.sources_refreshed:
                outcome.sources_refreshed.append(url)
            return
    row = FoodMerchantSource(
        merchant_id=merchant.id,
        source_type=source_type,
        source_scope=source_scope,
        source_title=title,
        source_url=url,
        claims_json=list(claims),
        edition_year=None,
        distinction=None,
        is_current=True,
        last_verified_at=now,
    )
    session.add(row)
    sources.append(row)
    outcome.sources_added.append(url)


async def apply_merchant_enrichment(
    session: AsyncSession,
    merchant: FoodMerchant,
    proposal: MerchantEnrichmentProposal,
    *,
    actor_id: UUID | None,
    origin: EnrichmentOrigin,
    evidence: list[dict[str, Any]],
    trusted_hosts: Collection[str] | None = None,
    now: datetime | None = None,
) -> EnrichmentOutcome:
    """Write what the proposal is allowed to write; flush, never commit.

    Raises ``AppError`` for an unknown or inactive area/category (through the admin
    editor's own validator) and for a listing that is not on a trusted host — always
    before the first write, so a caller handling a batch can report that one row and
    go on without a rollback.
    """
    now = now or datetime.now(UTC)
    outcome = EnrichmentOutcome()
    # Every check comes before the first write, and none of the reads may flush the
    # caller's pending rows: this helper runs on the caller's session and must neither
    # leave half a proposal behind nor swallow someone else's IntegrityError (see
    # app/analytics/service.py, record_event). No SAVEPOINT for the same reason.
    with session.no_autoflush:
        sources, category_rows, category_slugs_before = await _current_state(session, merchant)
        if proposal.listing_source is not None and not is_trusted_source(
            proposal.listing_source.url, trusted_hosts or TRUSTED_SOURCE_HOSTS
        ):
            raise AppError(422, "catalog_source_untrusted", "觀光局來源必須是信任的官方或政府主機")
        area_slug = proposal.area_slug
        if area_slug and merchant.area_id:
            outcome.skipped["area_slug"] = "already_set"
            area_slug = None
        area, categories = await _validate_merchant_taxonomy(
            session,
            destination_id=merchant.destination_id,
            area_slug=area_slug,
            category_slugs=list(proposal.category_slugs),
        )
        place_owner: str | None = None
        if proposal.google_place_id and not merchant.google_place_id:
            place_owner = await session.scalar(
                select(FoodMerchant.slug).where(
                    FoodMerchant.google_place_id == proposal.google_place_id,
                    FoodMerchant.id != merchant.id,
                )
            )
    before = _summary(merchant, sources, category_slugs_before)

    if proposal.address:
        if merchant.address:
            outcome.skipped["address"] = "already_set"
        else:
            merchant.address = proposal.address
            outcome.applied["address"] = proposal.address

    if proposal.official_website is not None:
        website = proposal.official_website
        if merchant.official_website_url and merchant.official_website_url != website.url:
            outcome.skipped["official_website_url"] = "already_set"
        else:
            if not merchant.official_website_url:
                merchant.official_website_url = website.url
                merchant.official_website_verified_at = now
                outcome.applied["official_website_url"] = website.url
            _upsert_source(
                session,
                merchant,
                sources,
                outcome,
                source_type="merchant_official",
                source_scope="merchant_website",
                title=website.title,
                url=website.url,
                claims=_claims(
                    ["display_name", "official_website"],
                    quote=website.quote,
                    address=merchant.address,
                ),
                now=now,
            )

    if proposal.listing_source is not None:
        listing = proposal.listing_source
        _upsert_source(
            session,
            merchant,
            sources,
            outcome,
            source_type=listing.source_type,
            source_scope="merchant_listing",
            title=listing.title,
            url=listing.url,
            claims=_claims(["display_name"], quote=listing.quote, address=merchant.address),
            now=now,
        )

    if area is not None:
        merchant.area_id = area.id
        merchant.area_source = "admin"
        outcome.applied["area_slug"] = area.slug
    if categories:
        existing_ids = {row.category_id for row in category_rows}
        next_order = max((row.display_order for row in category_rows), default=0) + 1
        for category in categories:
            if category.id in existing_ids:
                continue
            session.add(
                FoodMerchantCategory(
                    merchant_id=merchant.id,
                    category_id=category.id,
                    is_primary=not category_rows and not outcome.categories_added,
                    display_order=next_order,
                    source=origin.category_source,
                )
            )
            next_order += 1
            existing_ids.add(category.id)
            outcome.categories_added.append(category.slug)

    if proposal.google_place_id:
        if merchant.google_place_id:
            outcome.skipped["google_place_id"] = "already_set"
        elif place_owner is not None:
            outcome.skipped["google_place_id"] = f"owned_by_other:{place_owner}"
        else:
            merchant.google_place_id = proposal.google_place_id
            outcome.applied["google_place_id"] = proposal.google_place_id

    await session.flush()
    if outcome.changed:
        after = _summary(merchant, sources, category_slugs_before + list(outcome.categories_added))
        session.add(
            AdminAuditLog(
                actor_user_id=actor_id,
                action=AUDIT_ACTION,
                target=f"food_merchant:{merchant.id}",
                metadata_json={
                    "origin": origin.model_dump(),
                    "slug": merchant.slug,
                    "before": before,
                    "after": after,
                    **outcome.as_dict(),
                    "evidence": list(evidence)[:MAX_AUDIT_EVIDENCE],
                },
            )
        )
        await session.flush()
    return outcome
