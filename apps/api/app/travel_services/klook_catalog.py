"""Add-only, pending-review Klook catalog intake; no provider requests or approvals.

Run ``python -m app.travel_services.klook_catalog --manifest PATH`` to preview.
Only ``--apply`` commits. Existing products, offers, options and enrollment gates
are never updated. Candidate-only evidence is deliberately not imported.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Literal, Self
from urllib.parse import urlsplit
from uuid import UUID, uuid4

from pydantic import Field, model_validator
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models import (
    AdminAuditLog,
    HotelBookingOption,
    TravelServiceBrand,
    TravelServiceOffer,
    TravelServiceProduct,
)
from app.travel_services.channels import klook_product_target, validate_offer_target
from app.travel_services.schemas import (
    CITIES,
    Facts,
    HotelOptionInput,
    ProductInput,
    StrictModel,
    safe_url,
)

ACTIVITY_PATH = re.compile(r"/(?:[a-z]{2}(?:-[A-Za-z]{2})?/)?activity/([1-9][0-9]*)(?:-[^/]+)?/?")
HOTEL_PATH = re.compile(
    r"/(?:[a-z]{2}(?:-[A-Za-z]{2})?/)?hotels/(?:detail/)?([1-9][0-9]*)(?:-[^/]+)?/?"
)
MANIFEST_NAME = "representative-products-2026-09-09.json"


def _identity(value: str, kind: str = "activity") -> str | None:
    """Read legacy identities across locale/slug/tracking changes without rewriting them."""
    try:
        parsed = urlsplit(value)
        if parsed.hostname != "www.klook.com" or parsed.scheme != "https":
            return None
        match = (HOTEL_PATH if kind == "hotel" else ACTIVITY_PATH).fullmatch(parsed.path)
        return match.group(1) if match else None
    except ValueError:
        return None


def _exact_target(value: str, product_id: str, kind: str) -> str:
    parsed = urlsplit(value)
    if parsed.query or parsed.fragment or "%" in parsed.path:
        raise ValueError("Original exact product URL without tracking or encoded paths required")
    target = klook_product_target(value, kind)
    if target != value or _identity(target, kind) != product_id:
        raise ValueError("Klook product ID and canonical source URL must match")
    return target


class SourceEvidence(StrictModel):
    url: str
    checked_on: date
    method: Literal["official_public_product_page"] = "official_public_product_page"


class CatalogEntry(StrictModel):
    product_id: str = Field(pattern=r"^[1-9][0-9]*$")
    kind: Literal["tour", "transfer"]
    destination_id: str
    title: str = Field(min_length=1, max_length=255)
    original_title: str | None = Field(default=None, min_length=1, max_length=255)
    source_url: str
    evidence: SourceEvidence
    other_applicable_cities: list[str] = Field(default_factory=list, max_length=5)
    airport: str | None = None
    transfer_mode: Literal["bus", "private"] | None = None
    available_directions: list[Literal["arrival", "departure", "roundtrip"]] = Field(
        default_factory=list, max_length=3
    )
    notes: str = Field(min_length=1, max_length=1000)

    @property
    def source_key(self) -> str:
        return f"klook:activity:{self.product_id}"

    @model_validator(mode="after")
    def supported_identity(self) -> Self:
        _exact_target(self.source_url, self.product_id, self.kind)
        if self.evidence.url != self.source_url:
            raise ValueError("Source evidence must identify the exact original product page")
        if self.destination_id not in CITIES or any(
            city not in CITIES or city == self.destination_id
            for city in self.other_applicable_cities
        ):
            raise ValueError("Unsupported or duplicated destination")
        if len(set(self.other_applicable_cities)) != len(self.other_applicable_cities):
            raise ValueError("Duplicate secondary destination")
        if self.kind == "transfer":
            if (
                self.airport not in CITIES[self.destination_id][3]
                or not self.transfer_mode
                or "arrival" not in self.available_directions
            ):
                raise ValueError("Transfer requires an evidenced arrival airport and mode")
        elif self.airport or self.transfer_mode or self.available_directions:
            raise ValueError("Tour cannot assert airport transfer facts")
        return self

    def product_input(self) -> ProductInput:
        facts = Facts(country_codes=[CITIES[self.destination_id][0]])
        if self.kind == "transfer":
            facts.airport = self.airport
            # A bidirectional listing is not proof of a combined round-trip ticket.
            facts.direction = "arrival"
        return ProductInput(
            source_key=self.source_key,
            kind=self.kind,
            destination_id=self.destination_id,
            title=self.title,
            source_url=self.source_url,
            facts=facts,
        )


class PendingCandidate(StrictModel):
    """Evidence awaiting identity/package review, never passed to a database writer."""

    product_id: str = Field(pattern=r"^[1-9][0-9]*$")
    kind: Literal["hotel", "esim", "tour"]
    destination_id: str
    title: str = Field(min_length=1, max_length=255)
    source_url: str
    existing_source_key: str | None = None
    checked_on: date
    evidence_method: Literal["authenticated_name_match", "official_public_product_page"]
    import_ready: Literal[False] = False
    review_needed: str = Field(min_length=1, max_length=1000)

    @model_validator(mode="after")
    def exact_identity(self) -> Self:
        _exact_target(self.source_url, self.product_id, self.kind)
        if self.destination_id not in CITIES:
            raise ValueError("Unsupported candidate destination")
        return self


class HotelLinkEntry(StrictModel):
    product_id: str = Field(pattern=r"^[1-9][0-9]*$")
    existing_source_key: str = Field(min_length=1, max_length=128)
    destination_id: str
    title: str = Field(min_length=1, max_length=255)
    source_url: str
    checked_on: date
    official_identity_url: str
    identity_note: str = Field(min_length=1, max_length=1000)
    evidence_method: Literal["browser_name_and_address_match"]

    @model_validator(mode="after")
    def exact_hotel(self) -> Self:
        _exact_target(self.source_url, self.product_id, "hotel")
        self.official_identity_url = safe_url(self.official_identity_url)
        if self.destination_id not in CITIES:
            raise ValueError("Unsupported hotel destination")
        self.option_input()
        return self

    def option_input(self) -> HotelOptionInput:
        return HotelOptionInput(
            provider="klook",
            property_id=self.product_id,
            url=self.source_url,
            evidence_url=self.official_identity_url,
            identity_note=self.identity_note,
        )


class CatalogManifest(StrictModel):
    schema_version: Literal[1]
    provenance: str = Field(min_length=1, max_length=1000)
    entries: list[CatalogEntry] = Field(min_length=1, max_length=12)
    hotel_links: list[HotelLinkEntry] = Field(default_factory=list, max_length=12)
    candidates: list[PendingCandidate] = Field(default_factory=list, max_length=12)

    @model_validator(mode="after")
    def unique_products(self) -> Self:
        identities = (
            [f"activity:{entry.product_id}" for entry in self.entries]
            + [
                f"{'hotel' if item.kind == 'hotel' else 'activity'}:{item.product_id}"
                for item in self.candidates
            ]
            + [f"hotel:{item.product_id}" for item in self.hotel_links]
        )
        if len(identities) != len(set(identities)):
            raise ValueError("One manifest record per Klook product identity")
        keys = [item.existing_source_key for item in self.hotel_links]
        if len(keys) != len(set(keys)):
            raise ValueError("Only one Klook link per existing hotel")
        return self


class RowPreview(StrictModel):
    source_key: str
    product: Literal["create", "preserve", "conflict", "skip"]
    offer: Literal["create", "preserve", "blocked"]
    option: Literal["create", "preserve", "blocked"] | None = None
    existing_product_id: UUID | None = None
    reasons: list[str] = Field(default_factory=list)


class CatalogPreview(StrictModel):
    apply_requested: bool = False
    applied: bool = False
    blockers: list[str] = Field(default_factory=list)
    rows: list[RowPreview] = Field(default_factory=list)
    hotels: list[RowPreview] = Field(default_factory=list)
    candidate_only_count: int = 0


def default_manifest_path() -> Path:
    relative = Path("docs") / "klook-products" / MANIFEST_NAME
    return next(
        (
            parent / relative
            for parent in Path(__file__).resolve().parents
            if (parent / relative).is_file()
        ),
        relative,
    )


def load_manifest(path: Path) -> CatalogManifest:
    if path.stat().st_size > 100_000:
        raise ValueError("Catalog manifest is too large")
    return CatalogManifest.model_validate_json(path.read_text(encoding="utf-8"))


async def _plan(
    session: AsyncSession, manifest: CatalogManifest, settings: Settings, *, apply: bool
) -> tuple[CatalogPreview, TravelServiceBrand | None]:
    report = CatalogPreview(apply_requested=apply, candidate_only_count=len(manifest.candidates))
    aid = settings.klook_affiliate_id or ""
    brand = None
    if not re.fullmatch(r"[1-9][0-9]{0,19}", aid):
        report.blockers.append("numeric_klook_affiliate_id_required")
    else:
        query = select(TravelServiceBrand).where(
            TravelServiceBrand.channel == "klook_direct",
            TravelServiceBrand.code == "klook",
            TravelServiceBrand.project_id == aid,
        )
        brand = await session.scalar(query.with_for_update(nowait=True) if apply else query)
        if brand is None:
            report.blockers.append("existing_matching_klook_direct_brand_required")

    products = list(await session.scalars(select(TravelServiceProduct)))
    by_source = {product.source_key: product for product in products}
    offers = (
        list(
            await session.scalars(
                select(TravelServiceOffer).where(TravelServiceOffer.brand_id == brand.id)
            )
        )
        if brand
        else []
    )
    for entry in manifest.entries:
        product = by_source.get(entry.source_key)
        same_identity = [p for p in products if _identity(p.source_url) == entry.product_id]
        row = RowPreview(
            source_key=entry.source_key,
            product="preserve" if product else "create",
            offer="create" if brand else "blocked",
            existing_product_id=product.id if product else None,
        )
        if product and (
            product.kind != entry.kind
            or product.destination_id != entry.destination_id
            or _identity(product.source_url) != entry.product_id
        ):
            row.reasons.append("existing_source_key_identity_conflict")
        if any(product is None or p.id != product.id for p in same_identity):
            row.reasons.append("product_identity_already_exists_under_another_source_key")
        matching_offers = [
            offer
            for offer in offers
            if _identity(offer.target_url) == entry.product_id
            or (product and offer.product_id == product.id)
        ]
        if matching_offers:
            if (
                len(matching_offers) != 1
                or product is None
                or matching_offers[0].product_id != product.id
                or matching_offers[0].scope != "product"
                or _identity(matching_offers[0].target_url) != entry.product_id
            ):
                row.reasons.append("existing_direct_offer_identity_conflict")
            else:
                row.offer = "preserve"
        if row.reasons:
            row.product, row.offer = "conflict", "blocked"
        report.rows.append(row)
    options = (
        list(
            await session.scalars(
                select(HotelBookingOption).where(HotelBookingOption.provider == "klook")
            )
        )
        if manifest.hotel_links
        else []
    )
    for hotel in manifest.hotel_links:
        product = by_source.get(hotel.existing_source_key)
        row = RowPreview(
            source_key=hotel.existing_source_key,
            product="preserve" if product else "skip",
            existing_product_id=product.id if product else None,
            offer="create" if brand and product else "blocked",
            option="create" if brand and product else "blocked",
        )
        if product is None:
            row.reasons.append("existing_hotel_missing_no_product_created")
            report.hotels.append(row)
            continue
        if product.kind != "hotel" or product.destination_id != hotel.destination_id:
            row.reasons.append("existing_hotel_source_key_identity_conflict")
        matching_options = [
            option
            for option in options
            if option.product_id == product.id
            or option.property_id == hotel.product_id
            or _identity(option.url or "", "hotel") == hotel.product_id
        ]
        if matching_options:
            option = matching_options[0]
            if (
                len(matching_options) != 1
                or option.product_id != product.id
                or option.url != hotel.source_url
                or option.property_id not in (None, hotel.product_id)
            ):
                row.reasons.append("existing_klook_option_identity_conflict")
            else:
                row.option = "preserve"
        matching_offers = [
            offer
            for offer in offers
            if offer.product_id == product.id
            or _identity(offer.target_url, "hotel") == hotel.product_id
        ]
        if matching_offers:
            offer = matching_offers[0]
            if (
                len(matching_offers) != 1
                or offer.product_id != product.id
                or offer.target_url != hotel.source_url
                or offer.scope != "product"
            ):
                row.reasons.append("existing_direct_hotel_offer_identity_conflict")
            else:
                row.offer = "preserve"
        if row.reasons:
            row.product, row.offer, row.option = "conflict", "blocked", "blocked"
        report.hotels.append(row)
    if any(row.product == "conflict" for row in [*report.rows, *report.hotels]):
        report.blockers.append("catalog_identity_conflict")
    return report, brand


async def import_catalog(
    session: AsyncSession,
    manifest: CatalogManifest,
    settings: Settings,
    *,
    apply: bool = False,
) -> CatalogPreview:
    """Plan or add pending rows. The caller owns commit/rollback; no network calls.

    Conflicts stop the whole batch. A savepoint prevents partial additions if a
    concurrent admin write wins a unique key; rerunning then yields a fresh plan.
    """
    if apply and (session.new or session.dirty or session.deleted):
        return CatalogPreview(apply_requested=True, blockers=["clean_session_required"])
    # Serializes this importer even on the first insertion. Independent admin
    # writers remain protected by their database unique/FK constraints.
    if apply and session.get_bind().dialect.name == "postgresql":
        lock_key = int.from_bytes(
            hashlib.sha256(b"klook-additive-catalog-v1").digest()[:8], signed=True
        )
        acquired = await session.scalar(select(func.pg_try_advisory_xact_lock(lock_key)))
        if not acquired:
            return CatalogPreview(apply_requested=True, blockers=["catalog_import_already_running"])
    with session.no_autoflush:
        report, brand = await _plan(session, manifest, settings, apply=apply)
    if not apply or report.blockers or brand is None:
        return report
    try:
        async with session.begin_nested():
            for entry, row in zip(manifest.entries, report.rows, strict=True):
                product_id = row.existing_product_id
                if row.product == "create":
                    product_id = uuid4()
                    session.add(
                        TravelServiceProduct(
                            id=product_id,
                            **entry.product_input().model_dump(mode="json"),
                            status="pending",
                            version=1,
                            verified_at=None,
                        )
                    )
                    await session.flush()
                if row.offer == "create":
                    assert product_id is not None
                    session.add(
                        TravelServiceOffer(
                            product_id=product_id,
                            brand_id=brand.id,
                            target_url=validate_offer_target(brand, entry.source_url, None),
                            scope="product",
                            status="pending",
                            version=1,
                            static_url=None,
                            verified_at=None,
                            verification_context=None,
                        )
                    )
                    await session.flush()
                if row.product == "create" or row.offer == "create":
                    session.add(
                        AdminAuditLog(
                            actor_user_id=None,
                            action="travel_services.klook_catalog_add",
                            target=entry.source_key,
                            metadata_json={
                                "source_url": entry.source_url,
                                "original_title": entry.original_title or entry.title,
                                "evidence": entry.evidence.model_dump(mode="json"),
                                "product_created": row.product == "create",
                                "offer_created": row.offer == "create",
                                "approval": "pending",
                            },
                        )
                    )
            for hotel, row in zip(manifest.hotel_links, report.hotels, strict=True):
                if row.product == "skip":
                    continue
                if row.option == "create":
                    session.add(
                        HotelBookingOption(
                            product_id=row.existing_product_id,
                            **hotel.option_input().model_dump(),
                            status="pending",
                            version=1,
                            verified_at=None,
                            health_status="unchecked",
                            checked_at=None,
                        )
                    )
                if row.offer == "create":
                    session.add(
                        TravelServiceOffer(
                            product_id=row.existing_product_id,
                            brand_id=brand.id,
                            target_url=validate_offer_target(brand, hotel.source_url, None),
                            scope="product",
                            status="pending",
                            version=1,
                            static_url=None,
                            verified_at=None,
                            verification_context=None,
                        )
                    )
                if row.option == "create" or row.offer == "create":
                    session.add(
                        AdminAuditLog(
                            actor_user_id=None,
                            action="travel_services.klook_catalog_add",
                            target=hotel.existing_source_key,
                            metadata_json={
                                "source_url": hotel.source_url,
                                "official_identity_url": hotel.official_identity_url,
                                "checked_on": hotel.checked_on.isoformat(),
                                "evidence_method": hotel.evidence_method,
                                "identity_note": hotel.identity_note,
                                "option_created": row.option == "create",
                                "offer_created": row.offer == "create",
                                "approval": "pending",
                            },
                        )
                    )
            await session.flush()
    except IntegrityError:
        report.blockers.append("concurrent_catalog_change_retry_preview")
        return report
    report.applied = True
    return report


async def _run(args: argparse.Namespace) -> int:
    # Validate local evidence before opening any database connection.
    manifest = load_manifest(args.manifest)
    from app.admin.service import load_runtime_settings
    from app.db import SessionFactory

    async with SessionFactory() as session:
        settings = await load_runtime_settings(session)
        report = await import_catalog(session, manifest, settings, apply=args.apply)
        if report.applied:
            await session.commit()
        else:
            await session.rollback()
    output: dict[str, Any] = report.model_dump(mode="json")
    output["counts"] = {
        "products": dict(Counter(row.product for row in report.rows)),
        "offers": dict(Counter(row.offer for row in report.rows)),
        "hotels": dict(Counter(row.product for row in report.hotels)),
        "hotel_options": dict(Counter(row.option for row in report.hotels)),
        "hotel_offers": dict(Counter(row.offer for row in report.hotels)),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 2 if report.blockers else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=default_manifest_path())
    parser.add_argument("--apply", action="store_true", help="Commit additions as pending review")
    args = parser.parse_args(argv)
    try:
        return asyncio.run(_run(args))
    except (OSError, ValueError, SQLAlchemyError):
        # DB errors can contain DSNs or credentials. Do not echo exceptions.
        print(json.dumps({"applied": False, "error": "catalog_validation_or_database_error"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
