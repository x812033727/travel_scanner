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
    TravelServiceBrand,
    TravelServiceImport,
    TravelServiceOffer,
    TravelServiceProduct,
)
from app.travel_services.registry import BRANDS, brand_target
from app.travel_services.schemas import Facts, ProductInput, untracked_url
from app.travel_services.service import fail, fingerprint, product_input


def parse_csv(value: str) -> list[dict[str, Any]]:
    reader = csv.DictReader(io.StringIO(value.lstrip("\ufeff")))
    required = {"source_key", "kind", "destination_id", "title", "source_url"}
    allowed = required | {"names_json", "facts", "brand", "target_url", "scope"}
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
    if row and fingerprint(product_input(row).model_dump(mode="json")) == fingerprint(
        data.model_dump(mode="json")
    ):
        return row, False
    if row is None:
        row = TravelServiceProduct(
            **data.model_dump(exclude={"facts"}),
            facts=data.facts.model_dump(mode="json"),
            status="pending",
            version=1,
        )
        session.add(row)
    else:
        for key, value in data.model_dump(mode="json").items():
            setattr(row, key, value)
        row.status = "pending"
        row.verified_at = None
        row.version += 1
    await session.flush()
    return row, True


async def commit_import(session: AsyncSession, run_id: UUID, project_id: str) -> dict[str, Any]:
    run = await session.scalar(
        select(TravelServiceImport).where(TravelServiceImport.id == run_id).with_for_update()
    )
    if run is None:
        raise fail("service_unavailable", 404)
    if run.status == "completed":
        return run.result_json
    if any("error" in row for row in run.rows_json):
        raise fail("service_csv_invalid")
    changed = 0
    for row in run.rows_json:
        product, updated = await upsert_product(
            session, ProductInput.model_validate(row["product"])
        )
        changed += int(updated)
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
