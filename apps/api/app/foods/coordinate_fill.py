"""Fill food merchant coordinates from the pages the seed data already cites.

Every seeded merchant carries at least one ``FoodMerchantSource``, but 154 of 155 have no
coordinates, and coordinates are the gate they all fail: ``publishable_merchant_filters``
wants a latitude/longitude whose ``coordinate_source_type`` is durable and whose
``coordinate_source_url`` is an https page. Google's Places coordinates cannot fill that in —
they are licensed for comparison, not storage — so the coordinate has to come from a page that
is itself the authority.

Those pages are already in the database. A ``merchant_website`` source is the restaurant's own
site; a ``merchant_listing`` source is a tourism board's page *about this merchant*. Their
``source_type`` is already written in the same vocabulary as ``coordinate_source_type``, so it
is carried across rather than re-derived, which keeps a ``michelin_licensed`` listing — real,
but not a durable coordinate source — out. ``destination_context`` sources are excluded
outright: 155 merchants share 23 of them, so they are city food guides that say nothing about
where one restaurant stands.

Only the page's own structured data counts: schema.org JSON-LD and geo meta tags. Coordinates
inside an embedded Google map are deliberately **not** read. They are Google's coordinates
whatever page they are pasted into, and storing them under ``merchant_official`` provenance
would launder exactly the licensing rule that makes this module necessary.

A page that describes several venues — which is what a tourism listing often is — must not
donate the first coordinate in document order to whichever merchant cited it. Candidates are
therefore collected with the name of the entity that owns each one; a candidate is accepted
only when its name matches the merchant, or when the page offers exactly one coordinate.
Anything else is reported ``ambiguous`` for a human.

Korea is not skipped here, unlike ``place_matching``: a Place ID does nothing for a KR row,
but a coordinate is still one of the things that row will need once someone supplies its
Naver place URL.

Like ``place_matching``, this advances nobody's review state. It writes the coordinate, its
provenance and ``coordinate_verified_at`` — which across this codebase means "when this
coordinate was last confirmed against its source", not "a human approved this merchant" — and
leaves ``map_match_status``, ``review_status`` and ``is_active`` alone.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from urllib.parse import urlsplit
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.locations.coordinates import DURABLE_COORDINATE_SOURCES, valid_coordinate_pair
from app.models import AdminAuditLog, FoodMerchant, FoodMerchantSource

# A source only justifies a coordinate when its page is about this one merchant.
USABLE_SCOPES = ("merchant_website", "merchant_listing")
# The merchant's own site outranks a tourism listing about it.
SCOPE_ORDER = USABLE_SCOPES

# Generous boxes: they exist to catch a head office on another continent and a regex that
# matched a phone number, not to decide which city a restaurant is in.
COUNTRY_BOUNDS: dict[str, tuple[float, float, float, float]] = {
    "JP": (24.0, 45.6, 122.9, 146.0),
    "TW": (21.8, 25.4, 118.1, 122.1),
    "KR": (33.0, 38.7, 124.5, 131.0),
    "TH": (5.5, 20.5, 97.3, 105.7),
    "VN": (8.2, 23.4, 102.1, 109.5),
    "SG": (1.15, 1.48, 103.6, 104.1),
    "HK": (22.1, 22.6, 113.8, 114.5),
    "MO": (22.1, 22.25, 113.5, 113.65),
}

# Bounded quantifiers throughout: these run against pages this process does not control, and
# an unbounded `[^>]+` before a literal backtracks quadratically on hostile input.
_JSONLD_BLOCK = re.compile(
    r"<script[^>]{0,400}?type\s*=\s*[\"']application/ld\+json[\"'][^>]{0,400}?>(.{0,400000}?)</script>",
    re.IGNORECASE | re.DOTALL,
)
_HTML_COMMENT = re.compile(r"<!--.{0,200000}?-->", re.DOTALL)
_DECIMAL = r"-?\d{1,3}\.\d{1,15}"
_META_LAT = re.compile(
    r"<meta[^>]{0,200}?(?:itemprop|property|name)\s*=\s*[\"']"
    r"(?:latitude|place:location:latitude|og:latitude)[\"'][^>]{0,200}?"
    rf"content\s*=\s*[\"']({_DECIMAL})[\"']",
    re.IGNORECASE,
)
_META_LNG = re.compile(
    r"<meta[^>]{0,200}?(?:itemprop|property|name)\s*=\s*[\"']"
    r"(?:longitude|place:location:longitude|og:longitude)[\"'][^>]{0,200}?"
    rf"content\s*=\s*[\"']({_DECIMAL})[\"']",
    re.IGNORECASE,
)
_META_POSITION = re.compile(
    r"<meta[^>]{0,200}?name\s*=\s*[\"'](?:geo\.position|ICBM)[\"'][^>]{0,200}?"
    rf"content\s*=\s*[\"']({_DECIMAL})\s*[;,]\s*({_DECIMAL})[\"']",
    re.IGNORECASE,
)
_PUNCTUATION = re.compile(r"[\s　·・,，.。()（）\[\]【】\-‐‑–—_/&'\"!！?？:：;；]+")
# schema.org keys that lead towards a place rather than sideways into an unrelated entity.
_GEO_KEYS = ("geo", "location", "address", "@graph", "mainEntity", "itemListElement")

Fetcher = Callable[[str], Awaitable[str | None]]


@dataclass(frozen=True)
class GeoCandidate:
    latitude: float
    longitude: float
    owner: str | None
    method: str

    @property
    def key(self) -> tuple[float, float]:
        return round(self.latitude, 5), round(self.longitude, 5)


@dataclass(frozen=True)
class MerchantPage:
    scope: str
    source_type: str
    url: str


@dataclass(frozen=True)
class CoordinateFillReport:
    slug: str
    name: str
    outcome: str
    latitude: float | None = None
    longitude: float | None = None
    source_type: str | None = None
    source_url: str | None = None
    method: str | None = None
    owner: str | None = None


def _number(value: Any) -> float | None:
    """A coordinate component, refusing anything that is not already a plain number.

    No comma-to-dot rewriting: it cannot tell a decimal comma from a thousands separator, and
    guessing wrong moves a restaurant by hundreds of kilometres without any error.
    """

    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, str):
        text = value.strip()
        if not re.fullmatch(r"-?\d{1,3}(?:\.\d{1,15})?", text):
            return None
        return float(text)
    return None


def _normalize(name: str) -> str:
    return _PUNCTUATION.sub("", unicodedata.normalize("NFKC", name)).casefold()


def _collect_geo(node: Any, owner: str | None, found: list[GeoCandidate], depth: int = 0) -> None:
    """Walk a JSON-LD document recording every coordinate with the entity that owns it."""

    if depth > 8:
        return
    if isinstance(node, list):
        for item in node:
            _collect_geo(item, owner, found, depth + 1)
        return
    if not isinstance(node, dict):
        return
    name = node.get("name")
    here = name.strip() if isinstance(name, str) and name.strip() else owner
    latitude = _number(node.get("latitude"))
    longitude = _number(node.get("longitude"))
    if latitude is not None and longitude is not None:
        found.append(GeoCandidate(latitude, longitude, here, "json_ld"))
        return
    for key in _GEO_KEYS:
        if key in node:
            _collect_geo(node[key], here, found, depth + 1)
    for key, value in node.items():
        if key not in _GEO_KEYS and isinstance(value, dict | list):
            _collect_geo(value, here, found, depth + 1)


def _jsonld_candidates(html: str) -> list[GeoCandidate]:
    found: list[GeoCandidate] = []
    for block in _JSONLD_BLOCK.findall(html):
        try:
            document = json.loads(block.strip())
        except (ValueError, TypeError):
            continue
        _collect_geo(document, None, found)
    return found


def _meta_candidates(html: str) -> list[GeoCandidate]:
    """Meta tags, but only when the page carries exactly one of each.

    Two independent searches over a whole document can otherwise pair a latitude from one
    venue with a longitude from another and produce a coordinate that exists nowhere.
    """

    positions = _META_POSITION.findall(html)
    if len(positions) == 1:
        return [GeoCandidate(float(positions[0][0]), float(positions[0][1]), None, "meta")]
    latitudes = _META_LAT.findall(html)
    longitudes = _META_LNG.findall(html)
    if len(latitudes) == 1 and len(longitudes) == 1:
        return [GeoCandidate(float(latitudes[0]), float(longitudes[0]), None, "meta")]
    return []


def page_candidates(html: str) -> list[GeoCandidate]:
    """Every structured coordinate the page publishes, each with its owning entity's name."""

    body = _HTML_COMMENT.sub("", html)
    candidates = [
        candidate
        for candidate in _jsonld_candidates(body) + _meta_candidates(body)
        if valid_coordinate_pair(candidate.latitude, candidate.longitude)
        and candidate.key != (0.0, 0.0)
    ]
    return candidates


def select_candidate(
    candidates: list[GeoCandidate], names: tuple[str | None, ...]
) -> tuple[GeoCandidate | None, str]:
    """The one coordinate this page can be said to publish about this merchant."""

    if not candidates:
        return None, "no_coordinates"
    wanted = [_normalize(name) for name in names if name]
    for candidate in candidates:
        if not candidate.owner:
            continue
        owner = _normalize(candidate.owner)
        if any(owner and name and (owner in name or name in owner) for name in wanted):
            return candidate, "named"
    distinct = {candidate.key: candidate for candidate in candidates}
    if len(distinct) == 1:
        return next(iter(distinct.values())), "only"
    return None, "ambiguous"


def in_country(country_code: str, latitude: float, longitude: float) -> bool:
    """Whether the coordinate falls in the merchant's own country.

    An unlisted country cannot be checked, so it is accepted: a missing box must not silently
    drop every merchant in a country the catalog grew into.
    """

    bounds = COUNTRY_BOUNDS.get(country_code.upper())
    if bounds is None:
        return True
    south, north, west, east = bounds
    return south <= latitude <= north and west <= longitude <= east


async def merchants_without_coordinates(
    session: AsyncSession,
    *,
    destination_ids: tuple[str, ...] = (),
    limit: int | None = None,
) -> list[FoodMerchant]:
    query = (
        select(FoodMerchant)
        .where(
            FoodMerchant.latitude.is_(None),
            FoodMerchant.review_status != "rejected",
        )
        .order_by(FoodMerchant.destination_id, FoodMerchant.display_order, FoodMerchant.name)
    )
    if destination_ids:
        query = query.where(
            FoodMerchant.destination_id.in_([item.casefold() for item in destination_ids])
        )
    if limit is not None:
        query = query.limit(limit)
    return list((await session.scalars(query)).all())


async def merchant_page_sources(
    session: AsyncSession, merchants: list[FoodMerchant]
) -> dict[UUID, list[MerchantPage]]:
    """Per merchant, the https pages about that merchant whose source type is durable."""

    ids = [merchant.id for merchant in merchants]
    if not ids:
        return {}
    rows = (
        await session.scalars(
            select(FoodMerchantSource).where(
                FoodMerchantSource.merchant_id.in_(ids),
                FoodMerchantSource.is_current.is_(True),
                FoodMerchantSource.source_scope.in_(USABLE_SCOPES),
            )
        )
    ).all()
    grouped: dict[UUID, list[MerchantPage]] = {}
    for row in rows:
        if not row.source_url.startswith("https://"):
            continue
        if row.source_type not in DURABLE_COORDINATE_SOURCES:
            continue
        grouped.setdefault(row.merchant_id, []).append(
            MerchantPage(row.source_scope, row.source_type, row.source_url)
        )
    for merchant in merchants:
        pages = grouped.setdefault(merchant.id, [])
        # official_website_url is the administrator-maintained field behind
        # official_website_verified_at, so it is first-party provenance even with no source row.
        own = merchant.official_website_url
        if own and own.startswith("https://") and all(page.url != own for page in pages):
            pages.append(MerchantPage("merchant_website", "merchant_official", own))
    return grouped


def _by_scope(pages: list[MerchantPage]) -> list[MerchantPage]:
    """Best scope first, dropping any scope this module has no provenance rule for."""

    usable = [page for page in pages if page.scope in SCOPE_ORDER]
    return sorted(usable, key=lambda page: SCOPE_ORDER.index(page.scope))


async def _coordinate_owner(
    session: AsyncSession, merchant: FoodMerchant, latitude: float, longitude: float
) -> str | None:
    """Another merchant already standing on this exact spot, if there is one.

    Two merchants citing the same multi-venue article is the realistic way this happens, and
    it means at least one of the two coordinates is wrong.
    """

    owner = await session.scalar(
        select(FoodMerchant.slug).where(
            FoodMerchant.id != merchant.id,
            FoodMerchant.latitude == Decimal(str(round(latitude, 6))),
            FoodMerchant.longitude == Decimal(str(round(longitude, 6))),
        )
    )
    return str(owner) if owner is not None else None


async def fill_merchant_coordinates(
    session: AsyncSession,
    merchants: list[FoodMerchant],
    sources: dict[UUID, list[MerchantPage]],
    fetch: Fetcher,
    *,
    apply: bool = False,
    progress: Callable[[str], None] | None = None,
    pause: Callable[[float], Awaitable[None]] | None = None,
    host_delay_seconds: float = 1.0,
) -> list[CoordinateFillReport]:
    """Read each merchant's own pages until one publishes a coordinate about it.

    A page that fails only costs that merchant its turn; the batch continues. Consecutive
    requests to one host are spaced out, because the merchant ordering groups a destination's
    restaurants together and they tend to share a tourism site.
    """

    reports: list[CoordinateFillReport] = []
    last_host: str | None = None
    for merchant in merchants:
        slug, name = merchant.slug, merchant.name
        if merchant.latitude is not None and merchant.longitude is not None:
            reports.append(CoordinateFillReport(slug, name, "already_filled"))
            continue
        pages = _by_scope(sources.get(merchant.id) or [])
        if not pages:
            reports.append(CoordinateFillReport(slug, name, "no_source"))
            continue
        outcome = "no_coordinates"
        chosen: tuple[GeoCandidate, MerchantPage] | None = None
        for page in pages:
            host = urlsplit(page.url).hostname
            if pause is not None and host and host == last_host and host_delay_seconds > 0:
                await pause(host_delay_seconds)
            last_host = host
            try:
                html = await fetch(page.url)
            except Exception as exc:  # a dead link must not stop the batch
                if outcome == "no_coordinates":
                    outcome = "fetch_failed"
                if progress:
                    progress(f"{slug}: {page.url} failed ({type(exc).__name__})")
                continue
            if not html:
                if outcome == "no_coordinates":
                    outcome = "unreadable"
                continue
            candidate, reason = select_candidate(
                page_candidates(html), (merchant.name, merchant.local_name)
            )
            if candidate is None:
                if outcome == "no_coordinates" and reason != "no_coordinates":
                    outcome = reason
                continue
            if not in_country(merchant.country_code, candidate.latitude, candidate.longitude):
                if outcome == "no_coordinates":
                    outcome = "implausible"
                continue
            chosen = (candidate, page)
            break
        if chosen is None:
            reports.append(CoordinateFillReport(slug, name, outcome))
            if progress:
                progress(f"{slug}: {outcome}")
            continue
        candidate, page = chosen
        owner = await _coordinate_owner(session, merchant, candidate.latitude, candidate.longitude)
        if owner is not None:
            reports.append(
                CoordinateFillReport(
                    slug,
                    name,
                    "duplicate",
                    candidate.latitude,
                    candidate.longitude,
                    page.source_type,
                    page.url,
                    candidate.method,
                    owner,
                )
            )
            if progress:
                progress(f"{slug}: duplicate of {owner}")
            continue
        report = CoordinateFillReport(
            slug,
            name,
            "filled" if apply else "would_fill",
            candidate.latitude,
            candidate.longitude,
            page.source_type,
            page.url,
            candidate.method,
            candidate.owner,
        )
        if apply:
            merchant.latitude = Decimal(str(round(candidate.latitude, 6)))
            merchant.longitude = Decimal(str(round(candidate.longitude, 6)))
            merchant.coordinate_source_type = page.source_type
            merchant.coordinate_source_url = page.url
            merchant.coordinate_verified_at = datetime.now(UTC)
            session.add(
                AdminAuditLog(
                    actor_user_id=None,
                    action="food_merchant.cli_coordinates_filled",
                    target=f"food_merchant:{merchant.id}",
                    metadata_json={
                        "source": "cli",
                        "slug": slug,
                        "latitude": round(candidate.latitude, 6),
                        "longitude": round(candidate.longitude, 6),
                        "coordinate_source_type": page.source_type,
                        "coordinate_source_url": page.url,
                        "method": candidate.method,
                        "matched_entity": candidate.owner,
                    },
                )
            )
            await session.commit()
        reports.append(report)
        if progress:
            progress(f"{slug}: {report.outcome} {report.latitude},{report.longitude}")
    return reports


def summarize(reports: list[CoordinateFillReport]) -> dict[str, Any]:
    outcomes: dict[str, int] = {}
    for report in reports:
        outcomes[report.outcome] = outcomes.get(report.outcome, 0) + 1
    return {
        "processed": len(reports),
        "outcomes": outcomes,
        "rows": [
            {
                "slug": report.slug,
                "name": report.name,
                "outcome": report.outcome,
                "latitude": report.latitude,
                "longitude": report.longitude,
                "coordinate_source_type": report.source_type,
                "coordinate_source_url": report.source_url,
                "method": report.method,
                "matched_entity": report.owner,
            }
            for report in reports
        ],
    }
