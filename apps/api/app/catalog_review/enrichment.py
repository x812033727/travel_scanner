"""Server-side checks for merchant enrichment: which fetched page may back which field.

Gemini's grounded search only says where it looked; it cannot vouch for a page, and its
JSON cannot be trusted to attribute a URL to the right merchant in a batch of five. So
every candidate page is fetched independently and classified here by the two questions
a human reviewer asks first — does the page name this merchant, and does it place it
where the catalog says it is — and every correction the model returns is then checked
against the page it cites, field by field, before anything reaches the review item.

Nothing here talks to Gemini or the network; ``load_enrichment_taxonomy`` is the one
database read, so the rest can be unit-tested with plain dictionaries.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from collections.abc import Collection, Iterable
from dataclasses import dataclass
from typing import Any, Literal
from urllib.parse import urlsplit

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.catalog_review.evidence import is_trusted_source, normalize_source_url, normalize_text
from app.catalog_review.repository import normalized_name, source_urls
from app.catalog_review.schemas import (
    EnrichmentAssessment,
    EvidenceSource,
    ReviewCandidate,
)
from app.destinations.catalog import DestinationProfile
from app.foods.enrichment import CORRECTION_KINDS, is_platform_host
from app.models import CatalogReviewItem, FoodArea, FoodCategory

MIN_TERM_CHARS = 2
#: "Dai" or "Bar" inside any page proves nothing; a Latin name needs a longer match.
MIN_ASCII_TERM_CHARS = 4
MAX_ADDRESS_CHARS = 1000
MAX_AREAS_PER_DESTINATION = 40
MAX_CATEGORIES = 80
MAX_MATCH_TERMS = 8
MAX_OTHER_NAMES = 5
MAX_KNOWN_URLS = 5
SINGLE_VALUED_FIELDS = frozenset(
    {"address", "official_website_url", "listing_source_url", "area_slug"}
)
_WIKIMEDIA = ("wikimedia.org", "wikipedia.org", "wikidata.org", "wikivoyage.org")
_SPLIT = re.compile(r"[\s,、，。;；:：()（）/／\-‐–—]+")

CandidateKind = Literal["official", "listing"]


def _term(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = normalized_name(value)
    if len(normalized) < MIN_TERM_CHARS:
        return None
    if normalized.isascii() and len(normalized) < MIN_ASCII_TERM_CHARS:
        return None
    return normalized


def _dedupe(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def merchant_terms(snapshot: dict[str, Any]) -> list[str]:
    """Every label the catalog knows the merchant by, normalized for substring matching."""
    names = snapshot.get("names_json")
    values = [
        snapshot.get("name"),
        snapshot.get("local_name"),
        *((names or {}).values() if isinstance(names, dict) else ()),
    ]
    return _dedupe(term for value in values if (term := _term(value)))


def location_terms(snapshot: dict[str, Any], profile: DestinationProfile | None) -> list[str]:
    """Address fragments and the city's names in every script the catalog carries.

    Three-letter ASCII aliases (airport codes such as KIX) never survive ``_term``, so
    a page mentioning a flight does not pass as placing the merchant.
    """
    values: list[Any] = []
    address = snapshot.get("address")
    if isinstance(address, str):
        values.extend(_SPLIT.split(address))
    if profile is not None:
        values.extend(_SPLIT.split(profile.city))
        values.extend((profile.local_name, profile.english_name, *profile.aliases))
    destination_id = snapshot.get("destination_id")
    if isinstance(destination_id, str):
        values.extend(destination_id.split("-"))
    return _dedupe(term for value in values if (term := _term(value)))


def page_mentions(text: str, terms: Collection[str]) -> bool:
    haystack = normalized_name(text)
    return any(term in haystack for term in terms)


def _is_wikimedia(url: str) -> bool:
    host = (urlsplit(url).hostname or "").removeprefix("www.")
    return any(host == item or host.endswith(f".{item}") for item in _WIKIMEDIA)


@dataclass(frozen=True)
class VerifiedCandidate:
    url: str
    kind: CandidateKind
    title: str
    trusted: bool


def verify_candidates(
    snapshot: dict[str, Any],
    sources: list[EvidenceSource],
    titles: dict[str, str],
    profile: DestinationProfile | None,
    trusted_hosts: Collection[str],
) -> list[VerifiedCandidate]:
    """Classify fetched pages as the merchant's own site or a tourism listing about it.

    A tourism-board page (trusted registry, not Wikimedia) needs only to name the
    merchant. Any other page must also place it — an address fragment or the city —
    and must not be a platform, because a Tabelog page names and places every shop.
    """
    names = merchant_terms(snapshot)
    places = location_terms(snapshot, profile)
    result: list[VerifiedCandidate] = []
    seen: set[str] = set()
    for source in sources:
        if not source.fetched or not source.text:
            continue
        url = normalize_source_url(source.url)
        if url is None or url in seen or _is_wikimedia(url):
            # An encyclopedia article is evidence for the review, never a merchant source.
            continue
        haystack = normalized_name(source.text)
        if not names or not any(term in haystack for term in names):
            continue
        title = (titles.get(source.url) or titles.get(url) or "")[:255]
        if is_trusted_source(url, trusted_hosts):
            seen.add(url)
            result.append(VerifiedCandidate(url, "listing", title, True))
            continue
        if is_platform_host(url) or not any(term in haystack for term in places):
            continue
        seen.add(url)
        result.append(VerifiedCandidate(url, "official", title, False))
    return result


def _fingerprint_ok(source: EvidenceSource) -> bool:
    return source.fingerprint == hashlib.sha256(source.text.encode("utf-8")).hexdigest()


def verified_corrections(
    assessment: EnrichmentAssessment,
    candidate: ReviewCandidate,
    verified: list[VerifiedCandidate],
    *,
    area_slugs: Collection[str],
    category_slugs: Collection[str],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Keep only corrections whose cited page was fetched, still says what is quoted, and
    whose value the field-specific rule allows. Returns the accepted list (with ``kind``)
    and a count of rejections by reason for the run diagnostics."""
    by_url = {
        normalize_source_url(source.url) or source.url: source
        for source in candidate.sources
        if source.fetched and source.text and _fingerprint_ok(source)
    }
    official = {item.url for item in verified if item.kind == "official"}
    listing = {item.url for item in verified if item.kind == "listing"}
    titles = {item.url: item.title for item in verified}
    snapshot_address = candidate.data.get("address")
    accepted: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    rejected: Counter[str] = Counter()
    for correction in assessment.corrections:
        url = normalize_source_url(correction.source_url)
        source = by_url.get(url) if url else None
        if url is None or source is None:
            rejected["unknown_source"] += 1
            continue
        quote = normalize_text(correction.quote)
        if not quote or quote not in normalize_text(source.text):
            rejected["quote_not_in_source"] += 1
            continue
        value = correction.value.strip()
        if correction.field == "official_website_url":
            value_url = normalize_source_url(value)
            if value_url is None or value_url != url or url not in official:
                rejected["official_not_verified"] += 1
                continue
            value = value_url
        elif correction.field == "listing_source_url":
            value_url = normalize_source_url(value)
            if value_url is None or value_url != url or url not in listing:
                rejected["listing_not_verified"] += 1
                continue
            value = value_url
        elif correction.field == "address":
            if isinstance(snapshot_address, str) and snapshot_address.strip():
                rejected["address_already_set"] += 1
                continue
            if len(value) > MAX_ADDRESS_CHARS or normalized_name(value) not in normalized_name(
                source.text
            ):
                rejected["address_not_on_page"] += 1
                continue
        elif correction.field == "area_slug":
            if value not in area_slugs:
                rejected["area_not_allowed"] += 1
                continue
        elif correction.field == "category_slug":
            if value not in category_slugs:
                rejected["category_not_allowed"] += 1
                continue
        key = (correction.field, value)
        if key in seen or (
            correction.field in SINGLE_VALUED_FIELDS
            and any(field == correction.field for field, _ in seen)
        ):
            rejected["duplicate"] += 1
            continue
        seen.add(key)
        title = (correction.title or titles.get(url) or "").strip()[:255]
        accepted.append(
            {
                "field": correction.field,
                "value": value,
                "source_url": url,
                "quote": quote,
                "title": title or None,
                "kind": CORRECTION_KINDS[correction.field],
            }
        )
    return accepted, dict(rejected)


@dataclass(frozen=True)
class EnrichmentTaxonomy:
    """The slugs the model may pick from, with just enough names to pick sensibly."""

    areas_by_destination: dict[str, list[dict[str, Any]]]
    categories: list[dict[str, Any]]

    @property
    def category_slugs(self) -> list[str]:
        return [str(item["slug"]) for item in self.categories]

    def area_slugs(self, destination_id: str | None) -> list[str]:
        return [
            str(item["slug"]) for item in self.areas_by_destination.get(destination_id or "", [])
        ]

    def prompt_catalog(self, destination_ids: Collection[str]) -> dict[str, Any]:
        return {
            "areas": {
                destination_id: self.areas_by_destination.get(destination_id, [])
                for destination_id in sorted(set(destination_ids))
            },
            "category_slugs": self.category_slugs,
            "categories": self.categories,
        }


def _names(row_names: Any) -> dict[str, str]:
    names = row_names if isinstance(row_names, dict) else {}
    return {
        locale: str(names[locale])
        for locale in ("en", "zh-TW")
        if isinstance(names.get(locale), str) and names[locale]
    }


async def load_enrichment_taxonomy(session: AsyncSession) -> EnrichmentTaxonomy:
    areas: dict[str, list[dict[str, Any]]] = {}
    rows = (
        await session.scalars(
            select(FoodArea)
            .where(FoodArea.is_active.is_(True))
            .order_by(FoodArea.destination_id, FoodArea.display_order, FoodArea.slug)
        )
    ).all()
    for area in rows:
        bucket = areas.setdefault(area.destination_id, [])
        if len(bucket) >= MAX_AREAS_PER_DESTINATION:
            continue
        bucket.append(
            {
                "slug": area.slug,
                "names": _names(area.names_json),
                "match_terms": [
                    str(term) for term in (area.match_terms_json or [])[:MAX_MATCH_TERMS]
                ],
            }
        )
    categories = [
        {"slug": category.slug, "names": _names(category.names_json)}
        for category in (
            await session.scalars(
                select(FoodCategory)
                .where(FoodCategory.is_active.is_(True))
                .order_by(FoodCategory.display_order, FoodCategory.slug)
                .limit(MAX_CATEGORIES)
            )
        ).all()
    ]
    return EnrichmentTaxonomy(areas_by_destination=areas, categories=categories)


def merchant_prompt_context(
    item: CatalogReviewItem, profile: DestinationProfile | None
) -> dict[str, Any]:
    """What the grounded search needs to find this branch and nothing it must not see."""
    snapshot = item.snapshot_json or {}
    names = snapshot.get("names_json")
    other_names = _dedupe(
        str(value)
        for value in ((names or {}).values() if isinstance(names, dict) else ())
        if isinstance(value, str)
        and value not in {snapshot.get("name"), snapshot.get("local_name")}
    )[:MAX_OTHER_NAMES]
    destination: dict[str, Any] = {"id": item.destination_id}
    if profile is not None:
        destination.update(
            {
                "city": profile.city,
                "local_name": profile.local_name,
                "english_name": profile.english_name,
                "country": profile.country,
            }
        )
    return {
        "candidate_id": str(item.id),
        "name": snapshot.get("name") or item.name,
        "local_name": snapshot.get("local_name") or "",
        "other_names": other_names,
        "destination": destination,
        "address": snapshot.get("address"),
        "known_urls": source_urls(snapshot)[:MAX_KNOWN_URLS],
    }
