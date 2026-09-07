from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

import httpx
from fastapi import APIRouter, Query
from sqlalchemy import func, select

from app.admin.service import load_runtime_settings
from app.affiliates.service import TravelpayoutsLinkClient
from app.auth.service import AdminUser
from app.infra import get_redis
from app.models import (
    AdminAuditLog,
    AffiliateClick,
    TravelServiceBrand,
    TravelServiceConfig,
    TravelServiceImport,
    TravelServiceOffer,
    TravelServiceProduct,
    TripServiceSelection,
)
from app.travel_services.imports import commit_import, parse_csv, upsert_product
from app.travel_services.network import verify_link
from app.travel_services.registry import BRANDS, affiliate_target, brand_target
from app.travel_services.router import Session
from app.travel_services.schemas import (
    CITIES,
    KINDS,
    BrandInput,
    ConfigInput,
    CsvInput,
    Kind,
    OfferInput,
    ProductInput,
    ReviewInput,
)
from app.travel_services.service import (
    catalog_config,
    fail,
    link_context,
    product_input,
    ready_brand,
    require_product_review,
)

router = APIRouter(prefix="/admin/travel-services", tags=["admin travel services"])


def audit(
    session: Any, user: Any, action: str, target: str, metadata: dict[str, Any] | None = None
) -> None:
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action=f"travel_services.{action}",
            target=target,
            metadata_json=metadata or {},
        )
    )


def record(row: Any) -> dict[str, Any]:
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}


@router.get("")
async def overview(
    user: AdminUser,
    session: Session,
    destination_id: str | None = None,
    type: Kind | None = None,
    status: str | None = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(60, ge=1, le=100),
) -> dict[str, Any]:
    config, version = await catalog_config(session)
    settings = await load_runtime_settings(session)
    query = select(TravelServiceProduct)
    if destination_id:
        query = query.where(TravelServiceProduct.destination_id == destination_id)
    if type:
        query = query.where(TravelServiceProduct.kind == type)
    if status:
        query = query.where(TravelServiceProduct.status == status)
    products = list(
        await session.scalars(
            query.order_by(TravelServiceProduct.updated_at.desc()).offset(offset).limit(limit)
        )
    )
    brands = list(
        await session.scalars(
            select(TravelServiceBrand).where(
                TravelServiceBrand.project_id == (settings.travelpayouts_project_id or "")
            )
        )
    )
    offers = list(
        await session.scalars(
            select(TravelServiceOffer).where(
                TravelServiceOffer.product_id.in_([p.id for p in products])
            )
        )
    )
    all_products = list(
        await session.scalars(
            select(TravelServiceProduct).where(TravelServiceProduct.status == "approved")
        )
    )
    now = datetime.now(UTC)
    coverage = []
    for city in CITIES:
        counts = {
            kind: sum(
                p.kind == kind
                and (
                    CITIES[city][0] in p.facts.get("country_codes", [])
                    if kind == "esim"
                    else p.destination_id == city
                )
                for p in all_products
            )
            for kind in KINDS
        }
        areas = {
            p.facts.get("area_code")
            for p in all_products
            if p.destination_id == city and p.kind == "hotel" and p.facts.get("area_code")
        }
        coverage.append(
            {
                "destination_id": city,
                "counts": counts,
                "hotel_areas": len(areas),
                "complete": counts["hotel"] >= 6
                and counts["transfer"] >= 2
                and counts["tour"] >= 3
                and counts["esim"] >= 3
                and len(areas) >= 2,
            }
        )
    imports = list(
        await session.scalars(
            select(TravelServiceImport).order_by(TravelServiceImport.created_at.desc()).limit(20)
        )
    )
    return {
        "config": config.model_dump(),
        "version": version,
        "products": [record(p) for p in products],
        "offers": [record(o) for o in offers],
        "brands": [
            {**record(b), "name": BRANDS[b.code].name if b.code in BRANDS else b.code}
            for b in brands
        ],
        "brand_definitions": {
            code: {
                "name": b.name,
                "hosts": b.hosts,
                "kinds": b.kinds,
                "api_supported": b.api_supported,
            }
            for code, b in BRANDS.items()
        },
        "project_id": settings.travelpayouts_project_id,
        "network_configured": bool(
            settings.travelpayouts_enabled
            and settings.travelpayouts_api_token
            and settings.travelpayouts_marker
            and settings.travelpayouts_project_id
        ),
        "coverage": coverage,
        "review_due": sum(
            p.verified_at is None or p.verified_at < now - timedelta(days=30) for p in all_products
        ),
        "imports": [{**record(i), "rows_json": [], "row_count": len(i.rows_json)} for i in imports],
        "operations": {
            "outbound_clicks": await session.scalar(
                select(func.count())
                .select_from(AffiliateClick)
                .where(AffiliateClick.service_type.is_not(None))
            ),
            "self_reported_booked": await session.scalar(
                select(func.count())
                .select_from(TripServiceSelection)
                .where(TripServiceSelection.status == "booked")
            ),
            "confirmed_commission": None,
        },
    }


@router.put("/config")
async def put_config(payload: ConfigInput, user: AdminUser, session: Session) -> dict[str, Any]:
    row = await session.scalar(
        select(TravelServiceConfig).where(TravelServiceConfig.id == 1).with_for_update()
    )
    if payload.version != (row.version if row else 0):
        raise fail("service_version_conflict", 409)
    data = payload.model_dump(exclude={"version"})
    if row:
        row.data = data
        row.version += 1
    else:
        row = TravelServiceConfig(id=1, data=data, version=1)
        session.add(row)
    audit(session, user, "config", "catalog")
    await session.commit()
    return {"version": row.version, **data}


@router.post("/products", status_code=201)
async def create_product(
    payload: ProductInput, user: AdminUser, session: Session
) -> dict[str, Any]:
    if await session.scalar(
        select(TravelServiceProduct.id).where(TravelServiceProduct.source_key == payload.source_key)
    ):
        raise fail("service_version_conflict", 409)
    row, _ = await upsert_product(session, payload)
    audit(session, user, "product_create", str(row.id))
    await session.commit()
    return record(row)


@router.put("/products/{product_id}")
async def edit_product(
    product_id: UUID, payload: ProductInput, version: int, user: AdminUser, session: Session
) -> dict[str, Any]:
    row = await session.scalar(
        select(TravelServiceProduct).where(TravelServiceProduct.id == product_id).with_for_update()
    )
    if not row or row.source_key != payload.source_key or row.version != version:
        raise fail("service_version_conflict", 409)
    row, _ = await upsert_product(session, payload)
    audit(session, user, "product_edit", str(row.id))
    await session.commit()
    return record(row)


@router.post("/products/{product_id}/review")
async def review_product(
    product_id: UUID, payload: ReviewInput, user: AdminUser, session: Session
) -> dict[str, Any]:
    row = await session.scalar(
        select(TravelServiceProduct).where(TravelServiceProduct.id == product_id).with_for_update()
    )
    if not row or row.version != payload.version:
        raise fail("service_version_conflict", 409)
    if payload.status == "approved":
        require_product_review(product_input(row))
    row.status = payload.status
    row.verified_at = datetime.now(UTC) if payload.status == "approved" else None
    row.version += 1
    audit(session, user, "product_review", str(row.id), {"status": row.status})
    await session.commit()
    return record(row)


@router.put("/brands")
async def put_brand(payload: BrandInput, user: AdminUser, session: Session) -> dict[str, Any]:
    settings = await load_runtime_settings(session)
    if (
        not settings.travelpayouts_project_id
        or payload.code not in BRANDS
        or (payload.enabled and payload.approval != "approved")
    ):
        raise fail("service_brand_unavailable")
    row = await session.scalar(
        select(TravelServiceBrand)
        .where(
            TravelServiceBrand.project_id == settings.travelpayouts_project_id,
            TravelServiceBrand.code == payload.code,
        )
        .with_for_update()
    )
    if row and row.version != payload.version:
        raise fail("service_version_conflict", 409)
    if row is None:
        row = TravelServiceBrand(
            project_id=settings.travelpayouts_project_id, code=payload.code, version=0
        )
        session.add(row)
    row.approval, row.enabled, row.evidence_url = (
        payload.approval,
        payload.enabled,
        payload.evidence_url,
    )
    row.verified_at = datetime.now(UTC)
    row.version += 1
    audit(
        session,
        user,
        "brand_verify",
        payload.code,
        {"project_id": row.project_id, "approval": row.approval},
    )
    await session.commit()
    return record(row)


@router.post("/offers", status_code=201)
async def put_offer(payload: OfferInput, user: AdminUser, session: Session) -> dict[str, Any]:
    brand = await session.get(TravelServiceBrand, payload.brand_id)
    product = await session.get(TravelServiceProduct, payload.product_id)
    if (
        not brand
        or not product
        or brand.code not in BRANDS
        or product.kind not in BRANDS[brand.code].kinds
    ):
        raise fail("service_brand_unavailable")
    try:
        brand_target(brand.code, payload.target_url)
        if payload.static_url:
            affiliate_target(payload.static_url)
    except ValueError as exc:
        raise fail("service_offer_mismatch") from exc
    existing = await session.scalar(
        select(TravelServiceOffer).where(
            TravelServiceOffer.brand_id == brand.id,
            TravelServiceOffer.target_url == payload.target_url,
        )
    )
    if existing:
        raise fail("service_offer_mismatch", 409)
    row = TravelServiceOffer(**payload.model_dump(), status="pending", version=1)
    session.add(row)
    await session.flush()
    audit(session, user, "offer_create", str(row.id))
    await session.commit()
    return record(row)


@router.post("/offers/{offer_id}/review")
async def review_offer(
    offer_id: UUID, payload: ReviewInput, user: AdminUser, session: Session
) -> dict[str, Any]:
    row = await session.scalar(
        select(TravelServiceOffer).where(TravelServiceOffer.id == offer_id).with_for_update()
    )
    if not row or row.version != payload.version:
        raise fail("service_version_conflict", 409)
    if payload.status == "approved":
        brand = await session.get(TravelServiceBrand, row.brand_id)
        settings = await load_runtime_settings(session)
        if not brand or not ready_brand(brand, settings, datetime.now(UTC)):
            raise fail("service_brand_unavailable")
        try:
            if not row.static_url and not BRANDS[brand.code].api_supported:
                raise fail("service_link_unavailable")
            if not row.static_url and not (
                settings.travelpayouts_api_token and settings.travelpayouts_marker
            ):
                raise fail("service_brand_unavailable")
            target = row.static_url or await TravelpayoutsLinkClient(get_redis(), settings).create(
                row.target_url, "svc_verify", cache_context=f"verify:{row.id}:{row.version}"
            )
            if row.static_url and not settings.travelpayouts_marker:
                raise fail("service_brand_unavailable")
            if not await verify_link(
                target,
                brand.code,
                row.target_url,
                marker=settings.travelpayouts_marker if row.static_url else None,
                project=settings.travelpayouts_project_id if row.static_url else None,
            ):
                raise fail("service_link_unavailable")
            row.verification_context = link_context(settings)
        except (httpx.HTTPError, ConnectionError, ValueError, TimeoutError) as exc:
            raise fail("service_link_unavailable") from exc
    row.status = payload.status
    row.verified_at = datetime.now(UTC) if payload.status == "approved" else None
    row.version += 1
    audit(session, user, "offer_review", str(row.id), {"status": row.status})
    await session.commit()
    return record(row)


@router.post("/imports/preview")
async def preview_import(payload: CsvInput, user: AdminUser, session: Session) -> dict[str, Any]:
    rows = parse_csv(payload.csv)
    run = TravelServiceImport(
        actor_id=user.id, source="csv", status="preview", rows_json=rows, result_json={}
    )
    session.add(run)
    await session.flush()
    audit(session, user, "import_preview", str(run.id), {"count": len(rows)})
    await session.commit()
    return record(run)


@router.post("/imports/{run_id}/commit")
async def apply_import(run_id: UUID, user: AdminUser, session: Session) -> dict[str, Any]:
    settings = await load_runtime_settings(session)
    if not settings.travelpayouts_project_id:
        raise fail("service_brand_unavailable")
    result = await commit_import(session, run_id, settings.travelpayouts_project_id)
    audit(session, user, "import_commit", str(run_id), result)
    await session.commit()
    return result
