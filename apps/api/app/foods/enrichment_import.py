"""Apply a researched merchant-enrichment file through the shared enrichment writer.

The Gemini run and a person with a browser find the same things — the merchant's own
site, a tourism board's page about it, the address those pages print, the 商圈 and the
categories — but a person can also read a Google Maps branch page and copy its URL,
which is where the Place ID comes from here. Everything a researcher records lands in
one JSON file next to this module and is written by
``python -m app.cli apply-food-merchant-enrichment [--file …] [--apply]``, the way the
reservation-link reviews were.

The file is validated as a whole before anything is written, so one bad record never
lets the rest through. What may be written, and what never is, lives in
``app.foods.enrichment``; this module only decides what a record *means*:

* ``found`` / ``partial`` records carry a proposal and go through the writer.
* ``not_found`` / ``blocked_retry_later`` records carry only evidence; they leave one
  audit row so the next worklist export knows the merchant was looked at, and a retry
  file can pick the blocked ones up again.
* A dry run makes the same calls and rolls back, so its report has the same shape as
  the apply.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlsplit
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionFactory
from app.destinations.catalog import destination_for_id
from app.foods.admin_router import SLUG_FIELD_PATTERN
from app.foods.enrichment import (
    EnrichmentOrigin,
    MerchantEnrichmentProposal,
    apply_merchant_enrichment,
)
from app.foods.place_matching import SKIPPED_COUNTRIES
from app.models import (
    AdminAuditLog,
    FoodArea,
    FoodCategory,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantPlatformLink,
    FoodMerchantSource,
)
from app.problems import AppError
from app.restaurants.imports import (
    ALLOWED_GOOGLE_MAP_HOSTS,
    PLACE_ID_RE,
    SHORT_MAP_HOSTS,
    extract_place_id,
)

DATA_DIR = Path(__file__).resolve().parent / "data" / "enrichment"
DEFAULT_ENRICHMENT_FILE = DATA_DIR / "2026-09-12-pending-merchants.json"
RESEARCH_AUDIT_ACTION = "food_merchant.cli_enrichment_researched"
MAX_CATEGORIES = 3
MAX_EVIDENCE = 10
#: Outcomes that settle a merchant for the worklist; the other two are listed again.
SETTLED_OUTCOMES = frozenset({"found", "not_found"})

Outcome = Literal["found", "partial", "not_found", "blocked_retry_later"]
EvidenceRole = Literal[
    "search_result",
    "official_site",
    "tourism_listing",
    "google_maps_page",
    "open_data",
    "platform_page",
    "blocked",
    "other",
]


class EnrichmentFileError(ValueError):
    """The file cannot be imported as it is; the message names the record and the rule."""


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class EvidenceEntry(_Model):
    url: str = Field(min_length=8, max_length=2048)
    role: EvidenceRole
    observation: str = Field(min_length=1, max_length=1000)


class CitedPage(_Model):
    url: str = Field(min_length=8, max_length=2048)
    title: str = Field(min_length=1, max_length=255)
    quote: str = Field(min_length=1, max_length=300)


class ListingPage(CitedPage):
    source_type: Literal["official_tourism"] = "official_tourism"


class AddressEvidence(_Model):
    value: str = Field(min_length=1, max_length=1000)
    source_url: str = Field(min_length=8, max_length=2048)
    quote: str = Field(min_length=1, max_length=300)


class NaverOutcome(_Model):
    outcome: Literal["not_possible_in_pane", "url"]
    url: str | None = Field(default=None, max_length=2048)
    note: str | None = Field(default=None, max_length=500)


def _maps_url_place_id(url: str) -> str:
    parts = urlsplit(url)
    host = (parts.hostname or "").casefold()
    if parts.scheme != "https" or host not in ALLOWED_GOOGLE_MAP_HOSTS:
        raise ValueError("google_maps_url must be an https Google Maps URL")
    if host in SHORT_MAP_HOSTS:
        raise ValueError(
            "google_maps_url is a short link; paste the expanded URL from the address bar"
        )
    place_id = extract_place_id(url)
    if not place_id:
        raise ValueError("google_maps_url does not carry a Place ID (open the branch page)")
    return place_id


class EnrichmentRecord(_Model):
    merchant_id: UUID
    slug: str = Field(pattern=SLUG_FIELD_PATTERN, max_length=128)
    name: str = Field(min_length=1, max_length=255)
    local_name: str = Field(min_length=1, max_length=255)
    country_code: str = Field(min_length=2, max_length=2)
    destination_id: str = Field(min_length=2, max_length=64)
    outcome: Outcome
    checked_at: datetime
    address_local: AddressEvidence | None = None
    official_website: CitedPage | None = None
    listing_source: ListingPage | None = None
    google_maps_url: str | None = Field(default=None, max_length=2048)
    google_place_id: str | None = Field(default=None, max_length=255)
    map_identity_observation: str | None = Field(default=None, max_length=500)
    area_slug: str | None = Field(default=None, pattern=SLUG_FIELD_PATTERN, max_length=128)
    category_slugs: list[str] = Field(default_factory=list, max_length=MAX_CATEGORIES)
    naver: NaverOutcome | None = None
    reservation_batch_id: str | None = Field(default=None, max_length=128)
    evidence: list[EvidenceEntry] = Field(min_length=1, max_length=MAX_EVIDENCE)
    notes: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_record(self) -> EnrichmentRecord:
        self.country_code = self.country_code.upper()
        if self.checked_at.tzinfo is None:
            raise ValueError("checked_at must carry a timezone")
        if destination_for_id(self.destination_id) is None:
            raise ValueError(f"unknown destination {self.destination_id!r}")
        if self.google_place_id is not None and not PLACE_ID_RE.fullmatch(self.google_place_id):
            raise ValueError("google_place_id is not a Google Place ID")
        if self.google_maps_url is not None:
            derived = _maps_url_place_id(self.google_maps_url)
            if self.google_place_id is not None and self.google_place_id != derived:
                raise ValueError("google_place_id disagrees with the Place ID in google_maps_url")
            self.google_place_id = derived
        if self.google_place_id and not self.map_identity_observation:
            raise ValueError("a Google identity needs map_identity_observation")
        if self.area_slug and not self.area_slug.startswith(f"{self.destination_id}-"):
            raise ValueError("area_slug must belong to the record's destination")
        if len(set(self.category_slugs)) != len(self.category_slugs):
            raise ValueError("category_slugs repeats a category")
        cited = {page.url for page in (self.official_website, self.listing_source) if page}
        if self.address_local is not None and self.address_local.source_url not in cited:
            raise ValueError("address_local.source_url must be the official site or the listing")
        if self.country_code in SKIPPED_COUNTRIES:
            if self.naver is None:
                raise ValueError("Korean records must record the naver outcome")
        elif self.naver is not None:
            raise ValueError("naver applies to Korean records only")
        proposed = self.has_proposal
        if self.outcome == "found":
            if not cited:
                raise ValueError("found needs an official site or a listing")
            if not self.google_place_id and self.country_code not in SKIPPED_COUNTRIES:
                raise ValueError("found needs a Google identity outside Korea")
        elif self.outcome == "partial":
            if not proposed:
                raise ValueError("partial needs at least one proposed field")
        else:
            if proposed:
                raise ValueError(f"{self.outcome} must not propose any field")
            if self.outcome == "blocked_retry_later" and not any(
                entry.role == "blocked" for entry in self.evidence
            ):
                raise ValueError("blocked_retry_later needs an evidence entry with role blocked")
        return self

    @property
    def has_proposal(self) -> bool:
        return bool(
            self.address_local
            or self.official_website
            or self.listing_source
            or self.google_place_id
            or self.area_slug
            or self.category_slugs
        )

    def proposal(self) -> MerchantEnrichmentProposal:
        """The record as the shared writer takes it; raises for a source it refuses."""
        return MerchantEnrichmentProposal.model_validate(
            {
                "address": self.address_local.value if self.address_local else None,
                "official_website": self.official_website.model_dump()
                if self.official_website
                else None,
                "listing_source": self.listing_source.model_dump() if self.listing_source else None,
                "area_slug": self.area_slug,
                "category_slugs": list(self.category_slugs),
                "google_place_id": self.google_place_id,
            }
        )


class EnrichmentBatch(_Model):
    schema_version: Literal[1]
    batch_id: str = Field(min_length=1, max_length=128)
    researched_at: datetime
    researched_by: str = Field(min_length=1, max_length=255)
    method: str = Field(min_length=1, max_length=4000)
    rules: dict[str, str] = Field(default_factory=dict)
    records: list[EnrichmentRecord] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_batch(self) -> EnrichmentBatch:
        repeated = sorted(
            str(merchant_id)
            for merchant_id, count in Counter(r.merchant_id for r in self.records).items()
            if count > 1
        )
        if repeated:
            raise ValueError(f"merchant_id repeated in file: {repeated}")
        return self


def _record_label(error_location: tuple[Any, ...], raw: Any) -> str:
    if error_location and error_location[0] == "records" and len(error_location) > 1:
        index = error_location[1]
        records = raw.get("records") if isinstance(raw, dict) else None
        record = records[index] if isinstance(records, list) and isinstance(index, int) else None
        slug = record.get("slug") if isinstance(record, dict) else None
        return f"records[{index}] ({slug})"
    return "file"


def parse_enrichment_batch(raw: Any) -> EnrichmentBatch:
    try:
        batch = EnrichmentBatch.model_validate(raw)
    except ValidationError as exc:
        first = exc.errors()[0]
        location = ".".join(str(part) for part in first["loc"])
        raise EnrichmentFileError(
            f"{_record_label(tuple(first['loc']), raw)}: {location}: {first['msg']}"
        ) from None
    for index, record in enumerate(batch.records):
        if record.outcome in ("found", "partial"):
            try:
                record.proposal()
            except (ValidationError, AppError) as exc:
                detail = exc.errors()[0]["msg"] if isinstance(exc, ValidationError) else exc.code
                raise EnrichmentFileError(f"records[{index}] ({record.slug}): {detail}") from None
    return batch


def load_enrichment_file(path: Path) -> EnrichmentBatch:
    with path.open(encoding="utf-8") as handle:
        raw = json.load(handle)
    return parse_enrichment_batch(raw)


def record_evidence(batch: EnrichmentBatch, record: EnrichmentRecord) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = [
        {
            "url": entry.url,
            "role": entry.role,
            "observation": entry.observation,
            "batch_id": batch.batch_id,
            "checked_at": record.checked_at.isoformat(),
        }
        for entry in record.evidence
    ]
    if record.map_identity_observation:
        entries.append(
            {
                "role": "map_identity",
                "observation": record.map_identity_observation,
                "batch_id": batch.batch_id,
            }
        )
    if record.naver is not None:
        entries.append({"role": "naver", **record.naver.model_dump(), "batch_id": batch.batch_id})
    return entries[:MAX_EVIDENCE]


@dataclass(frozen=True)
class RecordOutcome:
    slug: str
    research_outcome: str
    action: str
    filled: tuple[str, ...] = ()
    skipped: dict[str, str] = field(default_factory=dict)
    detail: str | None = None


async def _research_noted(session: AsyncSession, merchant_id: UUID, batch_id: str) -> bool:
    rows = (
        await session.scalars(
            select(AdminAuditLog).where(
                AdminAuditLog.action == RESEARCH_AUDIT_ACTION,
                AdminAuditLog.target == f"food_merchant:{merchant_id}",
            )
        )
    ).all()
    return any((row.metadata_json or {}).get("batch_id") == batch_id for row in rows)


async def _enrich_one(
    session: AsyncSession, batch: EnrichmentBatch, record: EnrichmentRecord, *, apply: bool
) -> RecordOutcome:
    merchant = await session.scalar(
        select(FoodMerchant).where(FoodMerchant.id == record.merchant_id).with_for_update()
    )
    if merchant is None:
        return RecordOutcome(record.slug, record.outcome, "skipped_missing_merchant")
    if merchant.slug != record.slug:
        return RecordOutcome(
            record.slug, record.outcome, "skipped_slug_mismatch", detail=merchant.slug
        )
    if merchant.review_status in ("rejected", "disabled"):
        return RecordOutcome(
            record.slug, record.outcome, "skipped_not_enrichable", detail=merchant.review_status
        )
    if record.outcome in ("not_found", "blocked_retry_later"):
        if await _research_noted(session, merchant.id, batch.batch_id):
            return RecordOutcome(record.slug, record.outcome, "already_noted")
        if not apply:
            return RecordOutcome(record.slug, record.outcome, "would_note")
        session.add(
            AdminAuditLog(
                actor_user_id=None,
                action=RESEARCH_AUDIT_ACTION,
                target=f"food_merchant:{merchant.id}",
                metadata_json={
                    "batch_id": batch.batch_id,
                    "slug": merchant.slug,
                    "outcome": record.outcome,
                    "checked_at": record.checked_at.isoformat(),
                    "evidence": record_evidence(batch, record),
                    "notes": record.notes,
                },
            )
        )
        await session.commit()
        return RecordOutcome(record.slug, record.outcome, "noted")
    try:
        outcome = await apply_merchant_enrichment(
            session,
            merchant,
            record.proposal(),
            actor_id=None,
            origin=EnrichmentOrigin(kind="json_import", reference=batch.batch_id),
            evidence=record_evidence(batch, record),
        )
    except AppError as exc:
        await session.rollback()
        return RecordOutcome(record.slug, record.outcome, "skipped_taxonomy", detail=exc.code)
    except IntegrityError as exc:
        await session.rollback()
        return RecordOutcome(
            record.slug, record.outcome, "skipped_conflict", detail=type(exc.orig).__name__
        )
    filled = (
        *outcome.applied,
        *(("sources",) if outcome.sources_added else ()),
        *(("categories",) if outcome.categories_added else ()),
    )
    if not outcome.changed:
        await session.rollback()
        return RecordOutcome(record.slug, record.outcome, "unchanged", skipped=outcome.skipped)
    if apply:
        await session.commit()
        return RecordOutcome(record.slug, record.outcome, "enriched", filled, outcome.skipped)
    await session.rollback()
    return RecordOutcome(record.slug, record.outcome, "would_enrich", filled, outcome.skipped)


async def apply_enrichment_batch(
    session: AsyncSession,
    batch: EnrichmentBatch,
    *,
    apply: bool,
    limit: int | None = None,
    slugs: Sequence[str] = (),
    progress: bool = False,
) -> list[RecordOutcome]:
    records = [r for r in batch.records if not slugs or r.slug in set(slugs)]
    if limit:
        records = records[:limit]
    outcomes: list[RecordOutcome] = []
    for index, record in enumerate(records, start=1):
        outcome = await _enrich_one(session, batch, record, apply=apply)
        outcomes.append(outcome)
        if progress:
            print(f"[{index}/{len(records)}] {outcome.slug}: {outcome.action}", file=sys.stderr)
    return outcomes


def summarize(
    batch: EnrichmentBatch, outcomes: list[RecordOutcome], *, apply: bool
) -> dict[str, Any]:
    actions: Counter[str] = Counter()
    research: Counter[str] = Counter()
    fields: Counter[str] = Counter()
    field_skips: Counter[str] = Counter()
    skipped: list[dict[str, Any]] = []
    for outcome in outcomes:
        actions[outcome.action] += 1
        research[outcome.research_outcome] += 1
        for name in outcome.filled:
            fields[name] += 1
        for name, reason in outcome.skipped.items():
            field_skips[f"{name}:{reason.split(':', 1)[0]}"] += 1
        if outcome.action.startswith("skipped"):
            skipped.append(
                {"slug": outcome.slug, "action": outcome.action, "detail": outcome.detail}
            )
    return {
        "batch_id": batch.batch_id,
        "applied": apply,
        "records": len(batch.records),
        "processed": len(outcomes),
        "actions": dict(sorted(actions.items())),
        "research_outcomes": dict(sorted(research.items())),
        "fields": dict(sorted(fields.items())),
        "field_skips": dict(sorted(field_skips.items())),
        "skipped": skipped,
    }


async def apply_food_merchant_enrichment(
    path: Path,
    *,
    apply: bool,
    limit: int | None = None,
    slugs: Sequence[str] = (),
    check_only: bool = False,
) -> dict[str, Any]:
    batch = load_enrichment_file(path)
    if check_only:
        return {
            "batch_id": batch.batch_id,
            "valid": True,
            "records": len(batch.records),
            "research_outcomes": dict(sorted(Counter(r.outcome for r in batch.records).items())),
        }
    async with SessionFactory() as session:
        outcomes = await apply_enrichment_batch(
            session, batch, apply=apply, limit=limit, slugs=slugs, progress=True
        )
    return summarize(batch, outcomes, apply=apply)


def researched_index(data_dir: Path = DATA_DIR) -> dict[UUID, dict[str, Any]]:
    """What every committed batch says about each merchant; the latest check wins."""
    index: dict[UUID, dict[str, Any]] = {}
    if not data_dir.exists():
        return index
    for path in sorted(data_dir.glob("*.json")):
        batch = load_enrichment_file(path)
        for record in batch.records:
            current = index.get(record.merchant_id)
            if current is None or current["checked_at"] < record.checked_at:
                index[record.merchant_id] = {
                    "batch_id": batch.batch_id,
                    "outcome": record.outcome,
                    "checked_at": record.checked_at,
                }
    return index


def _names(values: Any) -> dict[str, str]:
    return {
        str(key): str(value)
        for key, value in (values.items() if isinstance(values, dict) else ())
        if isinstance(value, str) and value
    }


async def export_food_merchant_worklist(
    *,
    status: Literal["pending", "approved", "all"] = "pending",
    destination_ids: Sequence[str] = (),
    include_researched: bool = False,
    data_dir: Path = DATA_DIR,
) -> dict[str, Any]:
    """Everything a researcher needs per merchant, plus the slugs they may pick from."""
    researched = researched_index(data_dir)
    async with SessionFactory() as session:
        statement = select(FoodMerchant)
        if status != "all":
            statement = statement.where(FoodMerchant.review_status == status)
        if destination_ids:
            statement = statement.where(
                FoodMerchant.destination_id.in_([item.casefold() for item in destination_ids])
            )
        merchants = list(
            (
                await session.scalars(
                    statement.order_by(
                        FoodMerchant.country_code,
                        FoodMerchant.destination_id,
                        FoodMerchant.display_order,
                        FoodMerchant.name,
                        FoodMerchant.slug,
                    )
                )
            ).all()
        )
        ids = [merchant.id for merchant in merchants]
        sources = (
            (
                await session.scalars(
                    select(FoodMerchantSource).where(FoodMerchantSource.merchant_id.in_(ids))
                )
            ).all()
            if ids
            else []
        )
        links = (
            (
                await session.scalars(
                    select(FoodMerchantCategory).where(FoodMerchantCategory.merchant_id.in_(ids))
                )
            ).all()
            if ids
            else []
        )
        platforms = (
            (
                await session.scalars(
                    select(FoodMerchantPlatformLink).where(
                        FoodMerchantPlatformLink.merchant_id.in_(ids)
                    )
                )
            ).all()
            if ids
            else []
        )
        categories = (
            await session.scalars(
                select(FoodCategory)
                .where(FoodCategory.is_active.is_(True))
                .order_by(FoodCategory.display_order, FoodCategory.slug)
            )
        ).all()
        areas = (
            await session.scalars(
                select(FoodArea)
                .where(FoodArea.is_active.is_(True))
                .order_by(FoodArea.destination_id, FoodArea.display_order, FoodArea.slug)
            )
        ).all()
    category_slug = {row.id: row.slug for row in categories}
    area_slug = {row.id: row.slug for row in areas}
    sources_by_merchant: dict[UUID, list[dict[str, Any]]] = {}
    for source in sources:
        sources_by_merchant.setdefault(source.merchant_id, []).append(
            {
                "scope": source.source_scope,
                "type": source.source_type,
                "url": source.source_url,
                "title": source.source_title,
                "is_current": source.is_current,
            }
        )
    categories_by_merchant: dict[UUID, list[str]] = {}
    for link in sorted(links, key=lambda row: (row.display_order, str(row.id))):
        if link.category_id in category_slug:
            categories_by_merchant.setdefault(link.merchant_id, []).append(
                category_slug[link.category_id]
            )
    platforms_by_merchant: dict[UUID, list[dict[str, Any]]] = {}
    for platform in platforms:
        platforms_by_merchant.setdefault(platform.merchant_id, []).append(
            {
                "provider": platform.provider,
                "status": platform.status,
                "canonical_url": platform.canonical_url,
            }
        )
    rows: list[dict[str, Any]] = []
    destinations: set[str] = set()
    for merchant in merchants:
        note = researched.get(merchant.id)
        if note and not include_researched and note["outcome"] in SETTLED_OUTCOMES:
            continue
        destinations.add(merchant.destination_id)
        rows.append(
            {
                "id": str(merchant.id),
                "slug": merchant.slug,
                "name": merchant.name,
                "local_name": merchant.local_name,
                "names": _names(merchant.names_json),
                "destination_id": merchant.destination_id,
                "country_code": merchant.country_code,
                "address": merchant.address,
                "area_slug": area_slug.get(merchant.area_id) if merchant.area_id else None,
                "category_slugs": categories_by_merchant.get(merchant.id, []),
                "google_place_id": merchant.google_place_id,
                "naver_map_url": merchant.naver_map_url,
                "official_website_url": merchant.official_website_url,
                "sources": sources_by_merchant.get(merchant.id, []),
                "platform_links": platforms_by_merchant.get(merchant.id, []),
                "review_status": merchant.review_status,
                "map_match_status": merchant.map_match_status,
                "has_coordinates": merchant.latitude is not None,
                "researched": (
                    {**note, "checked_at": note["checked_at"].isoformat()} if note else None
                ),
            }
        )
    return {
        "exported_at": datetime.now(UTC).isoformat(),
        "status": status,
        "count": len(rows),
        "categories": [{"slug": row.slug, "names": _names(row.names_json)} for row in categories],
        "areas_by_destination": {
            destination: [
                {
                    "slug": row.slug,
                    "names": _names(row.names_json),
                    "match_terms": [str(term) for term in (row.match_terms_json or [])],
                }
                for row in areas
                if row.destination_id == destination
            ]
            for destination in sorted(destinations)
        },
        "merchants": rows,
    }
