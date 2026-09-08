import csv
import io
import json
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    HotelBookingOption,
    TravelServiceBrand,
    TravelServiceImport,
    TravelServiceOffer,
    TravelServiceProduct,
)
from app.travel_services.registry import BRANDS, brand_target
from app.travel_services.schemas import Facts, HotelOptionInput, Kind, ProductInput, untracked_url
from app.travel_services.service import fail, fingerprint, product_input


def parse_csv(value: str) -> list[dict[str, Any]]:
    reader = csv.DictReader(io.StringIO(value.lstrip("\ufeff")))
    required = {"source_key", "kind", "destination_id", "title", "source_url"}
    allowed = required | {"names_json", "facts", "brand", "target_url", "scope", "booking_options"}
    if (
        not reader.fieldnames
        or not required <= set(reader.fieldnames)
        or not set(reader.fieldnames) <= allowed
    ):
        raise fail("service_csv_invalid")
    result: list[dict[str, Any]] = []
    for index, raw in enumerate(reader, start=2):
        if index > 501:
            raise fail("service_csv_invalid")
        try:
            if None in raw:
                raise ValueError("Too many columns")
            data = ProductInput(
                **{k: raw[k] for k in required},
                facts=Facts.model_validate(json.loads(raw.get("facts") or "{}")),
                names_json=json.loads(raw.get("names_json") or "{}"),
            )
            row: dict[str, Any] = {"product": data.model_dump(mode="json"), "line": index}
            # Absence is not an instruction to delete independently managed options.
            if "hotel_links" not in data.facts.model_fields_set:
                row["product"]["facts"].pop("hotel_links", None)
            if raw.get("booking_options"):
                if data.kind != "hotel":
                    raise ValueError("Hotel options require a hotel")
                options = [
                    HotelOptionInput.model_validate(value)
                    for value in json.loads(raw["booking_options"])
                ]
                if len(options) > 8 or len({o.provider for o in options}) != len(options):
                    raise ValueError("Duplicate hotel platforms")
                row["booking_options"] = [o.model_dump(mode="json") for o in options]
            if raw.get("target_url") or raw.get("brand"):
                code = raw.get("brand") or ""
                if code not in BRANDS or data.kind not in BRANDS[code].kinds:
                    raise ValueError("Invalid brand")
                scope = raw.get("scope") or "product"
                if scope not in ("product", "destination"):
                    raise ValueError("Invalid scope")
                row["offer"] = {
                    "brand": code,
                    "target_url": brand_target(code, untracked_url(raw.get("target_url") or "")),
                    "scope": scope,
                }
            result.append(row)
        except (ValueError, TypeError, ValidationError):
            result.append({"line": index, "error": "service_csv_invalid"})
    if not result:
        raise fail("service_csv_invalid")
    return result


async def upsert_product(
    session: AsyncSession, data: ProductInput
) -> tuple[TravelServiceProduct, bool]:
    row = await session.scalar(
        select(TravelServiceProduct)
        .where(TravelServiceProduct.source_key == data.source_key)
        .with_for_update()
    )
    if row is not None and row.kind != data.kind:
        # Source keys are durable identities, not a way to move a product between domains.
        raise fail("service_source_kind_mismatch", 409)
    from app.travel_services.hotel_options import upsert_option
    from app.travel_services.schemas import HotelOptionInput

    # Link edits have their own review lifecycle. Never persist the legacy JSON copy.
    core = data.model_dump(mode="json")
    core["facts"].pop("hotel_links", None)
    before = product_input(row).model_dump(mode="json") if row else None
    if before:
        before["facts"].pop("hotel_links", None)
    changed = not row or fingerprint(before) != fingerprint(core)
    if row is None:
        row = TravelServiceProduct(
            **core,
            status="pending",
            version=1,
            hotel_options=[],
        )
        session.add(row)
    elif changed:
        for key, value in core.items():
            setattr(row, key, value)
        row.status = "pending"
        row.verified_at = None
        row.version += 1
    await session.flush()
    existing_options = row.hotel_options
    if "hotel_links" in data.facts.model_fields_set:
        # Legacy replacement can disable omitted options. Serialize that path with
        # independent reviews too, and increment the current (not identity-map) version.
        existing_options = list(
            await session.scalars(
                select(HotelBookingOption)
                .where(HotelBookingOption.product_id == row.id)
                .with_for_update()
                .execution_options(populate_existing=True)
            )
        )
    for link in data.facts.hotel_links:
        existing = next((o for o in existing_options if o.provider == link.provider), None)
        if existing and existing.url == link.url and existing.evidence_url == link.evidence_url:
            continue  # Legacy round-trips cannot erase independently reviewed property IDs/notes.
        _, updated = await upsert_option(session, row, HotelOptionInput(**link.model_dump()))
        changed = changed or updated
    if "hotel_links" in data.facts.model_fields_set:
        retained = {link.provider for link in data.facts.hotel_links}
        for option in existing_options:
            if (
                option.discovery_status == "found"
                and option.provider not in retained
                and option.status != "disabled"
            ):
                option.status, option.verified_at = "disabled", None
                option.version += 1
                changed = True
    return row, bool(changed)


async def commit_import(
    session: AsyncSession,
    run_id: UUID,
    project_id: str | None,
    *,
    required_kind: Kind | None = None,
) -> dict[str, Any]:
    run = await session.scalar(
        select(TravelServiceImport).where(TravelServiceImport.id == run_id).with_for_update()
    )
    if run is None:
        raise fail("service_unavailable", 404)
    if required_kind == "hotel" and run.source != "hotel_csv":
        raise fail("service_import_scope_mismatch", 409)
    scope = "hotel" if run.source == "hotel_csv" else required_kind
    if scope and any(row.get("product", {}).get("kind") != scope for row in run.rows_json):
        raise fail("service_import_scope_mismatch", 409)
    if run.status == "completed":
        return run.result_json
    if any("error" in row for row in run.rows_json):
        raise fail("service_csv_invalid")
    if not project_id and any(row.get("offer") for row in run.rows_json):
        raise fail("service_brand_unavailable")
    # Validate the entire batch before modifying any row; upsert repeats this under its lock.
    for item in run.rows_json:
        existing = await session.scalar(
            select(TravelServiceProduct)
            .where(TravelServiceProduct.source_key == item["product"]["source_key"])
            .with_for_update()
        )
        if existing is not None and existing.kind != item["product"]["kind"]:
            raise fail("service_source_kind_mismatch", 409)
    changed = 0
    for row in run.rows_json:
        product, updated = await upsert_product(
            session, ProductInput.model_validate(row["product"])
        )
        changed += int(updated)
        if row.get("booking_options"):
            from app.travel_services.hotel_options import upsert_option

            option_changes = False
            for raw_option in row["booking_options"]:
                _, option_changed = await upsert_option(
                    session, product, HotelOptionInput.model_validate(raw_option)
                )
                option_changes = option_changes or option_changed
            if option_changes and not updated:
                changed += 1
        if raw := row.get("offer"):
            brand = await session.scalar(
                select(TravelServiceBrand).where(
                    TravelServiceBrand.project_id == project_id,
                    TravelServiceBrand.code == raw["brand"],
                )
            )
            if brand is None:
                brand = TravelServiceBrand(
                    project_id=project_id, code=raw["brand"], approval="unknown", enabled=False
                )
                session.add(brand)
                await session.flush()
            offer = await session.scalar(
                select(TravelServiceOffer).where(
                    TravelServiceOffer.brand_id == brand.id,
                    TravelServiceOffer.target_url == raw["target_url"],
                )
            )
            if offer and offer.product_id != product.id:
                raise fail("service_offer_mismatch", 409)
            if offer and offer.scope != raw["scope"]:
                offer.scope = raw["scope"]
                offer.status = "pending"
                offer.verified_at = None
                offer.version += 1
            if offer is None:
                session.add(
                    TravelServiceOffer(
                        product_id=product.id,
                        brand_id=brand.id,
                        target_url=raw["target_url"],
                        scope=raw["scope"],
                        status="pending",
                    )
                )
    run.status = "completed"
    run.result_json = {
        "processed": len(run.rows_json),
        "changed": changed,
        "pending_review": changed,
    }
    run.updated_at = datetime.now(UTC)
    await session.flush()
    return run.result_json
