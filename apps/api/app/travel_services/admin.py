from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import UUID

import httpx
from fastapi import APIRouter, Query
from sqlalchemy import func, or_, select

from app.admin.service import load_runtime_settings
from app.affiliates.schemas import AffiliateModule
from app.affiliates.service import TravelpayoutsLinkClient
from app.auth.service import AdminUser
from app.destinations.catalog import DESTINATIONS
from app.infra import get_redis
from app.models import (
    AdminAuditLog,
    AffiliateClick,
    DestinationAffiliateOffer,
    HotelBookingClick,
    HotelBookingOption,
    TravelServiceBrand,
    TravelServiceConfig,
    TravelServiceImport,
    TravelServiceOffer,
    TravelServiceProduct,
    TripServiceSelection,
)
from app.travel_services.hotel_quotes import ADAPTERS
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
    DestinationOfferBatchReview,
    DestinationOfferInput,
    HotelLink,
    HotelOptionEdit,
    HotelOptionInput,
    HotelOptionReview,
    HotelProvider,
    HotelQuotePolicy,
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
    affiliate_module: AffiliateModule | None = None,
    offer_status: str | None = None,
    offer_brand_id: UUID | None = None,
    offer_review_due: bool = False,
) -> dict[str, Any]:
    config, version = await catalog_config(session)
    settings = await load_runtime_settings(session)
    now = datetime.now(UTC)
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
    destination_offer_query = select(DestinationAffiliateOffer)
    if destination_id:
        destination_offer_query = destination_offer_query.where(
            DestinationAffiliateOffer.destination_id == destination_id
        )
    if affiliate_module:
        destination_offer_query = destination_offer_query.where(
            DestinationAffiliateOffer.module == affiliate_module
        )
    if offer_status:
        destination_offer_query = destination_offer_query.where(
            DestinationAffiliateOffer.status == offer_status
        )
    if offer_brand_id:
        destination_offer_query = destination_offer_query.where(
            DestinationAffiliateOffer.brand_id == offer_brand_id
        )
    if offer_review_due:
        destination_offer_query = destination_offer_query.where(
            or_(
                DestinationAffiliateOffer.verified_at.is_(None),
                DestinationAffiliateOffer.verified_at < now - timedelta(days=30),
            )
        )
    destination_offers = list(
        await session.scalars(
            destination_offer_query.order_by(
                DestinationAffiliateOffer.destination_id,
                DestinationAffiliateOffer.module,
            ).limit(500)
        )
    )
    all_products = list(
        await session.scalars(
            select(TravelServiceProduct).where(TravelServiceProduct.status == "approved")
        )
    )
    coverage = []
    for city in CITIES:
        from app.travel_services.hotel_options import needs_source_credit

        hotel_ready = []
        for p in all_products:
            if p.kind != "hotel" or p.destination_id != city or needs_source_credit(p):
                continue
            checked = {
                o.provider: o for o in p.hotel_options if o.discovery_status != "unconfirmed"
            }
            usable = {
                o.provider
                for o in p.hotel_options
                if o.status == "approved"
                and o.discovery_status == "found"
                and o.verified_at
                and now - timedelta(days=30) <= o.verified_at <= now
                and o.health_status not in ("unsafe", "unavailable")
            }
            if (
                "official" in usable
                and len(usable.intersection({"booking", "trip_com", "agoda", "expedia", "rakuten"}))
                >= 2
                and {"booking", "trip_com", "agoda", "expedia", "rakuten"} <= checked.keys()
            ):
                hotel_ready.append(p)
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
                "hotel_ready": len(hotel_ready),
                "hotel_complete": len(hotel_ready) >= 10
                and len({p.facts.get("area_code") for p in hotel_ready}) >= 3,
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
        "products": [
            {
                **record(p),
                "facts": product_input(p).facts.model_dump(mode="json"),
                "booking_options": [record(o) for o in p.hotel_options],
            }
            for p in products
        ],
        "quote_providers": {
            code: {
                "adapter_available": code in ADAPTERS,
                **config.hotel_quote_policies.get(
                    cast(HotelProvider, code), HotelQuotePolicy()
                ).model_dump(),
            }
            for code in ("booking", "trip_com", "agoda", "expedia", "rakuten")
        },
        "offers": [record(o) for o in offers],
        "destination_offers": [record(o) for o in destination_offers],
        "destinations": [
            {
                "id": destination.id,
                "city": destination.city,
                "country": destination.country_label,
                "role": destination.role,
            }
            for destination in DESTINATIONS
        ],
        "brands": [
            {**record(b), "name": BRANDS[b.code].name if b.code in BRANDS else b.code}
            for b in brands
        ],
        "brand_definitions": {
            code: {
                "name": b.name,
                "hosts": b.hosts,
                "kinds": b.kinds,
                "modules": b.supported_modules,
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
        "hotel_option_review_due": sum(
            o.status == "approved"
            and (o.verified_at is None or o.verified_at < now - timedelta(days=30))
            for p in all_products
            for o in p.hotel_options
        ),
        "imports": [{**record(i), "rows_json": [], "row_count": len(i.rows_json)} for i in imports],
        "operations": {
            "affiliate_hotel_clicks": await session.scalar(
                select(func.count())
                .select_from(HotelBookingClick)
                .where(HotelBookingClick.mode == "affiliate")
            ),
            "ordinary_hotel_clicks": await session.scalar(
                select(func.count())
                .select_from(HotelBookingClick)
                .where(HotelBookingClick.mode == "direct")
            ),
            "hotel_affiliate_fallbacks": await session.scalar(
                select(func.count())
                .select_from(HotelBookingClick)
                .where(HotelBookingClick.fallback.is_(True))
            ),
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
        from app.travel_services.hotel_options import needs_source_credit

        if row.kind == "hotel" and needs_source_credit(row):
            raise fail("service_source_required")
    row.status = payload.status
    row.verified_at = datetime.now(UTC) if payload.status == "approved" else None
    row.version += 1
    audit(session, user, "product_review", str(row.id), {"status": row.status})
    await session.commit()
    return record(row)


@router.put("/products/{product_id}/booking-options")
async def edit_hotel_option(
    product_id: UUID, payload: HotelOptionEdit, user: AdminUser, session: Session
) -> dict[str, Any]:
    from app.travel_services.hotel_options import upsert_option

    product = await session.scalar(
        select(TravelServiceProduct).where(TravelServiceProduct.id == product_id).with_for_update()
    )
    if not product or product.kind != "hotel":
        raise fail("service_unavailable", 404)
    existing = await session.scalar(
        select(HotelBookingOption)
        .where(
            HotelBookingOption.product_id == product_id,
            HotelBookingOption.provider == payload.provider,
        )
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if payload.version != (existing.version if existing else 0):
        raise fail("service_version_conflict", 409)
    option, changed = await upsert_option(
        session, product, HotelOptionInput.model_validate(payload.model_dump(exclude={"version"}))
    )
    audit(session, user, "hotel_option_edit", str(option.id), {"changed": changed})
    await session.commit()
    return record(option)


@router.post("/products/{product_id}/booking-options/{option_id}/review")
async def review_hotel_option(
    product_id: UUID, option_id: UUID, payload: HotelOptionReview, user: AdminUser, session: Session
) -> dict[str, Any]:
    from app.travel_services.hotel_options import option_input, safe_click_target
    from app.travel_services.network import check_hotel_link

    option = await session.scalar(
        select(HotelBookingOption)
        .where(HotelBookingOption.id == option_id, HotelBookingOption.product_id == product_id)
        .with_for_update()
    )
    if not option or option.version != payload.version:
        raise fail("service_version_conflict", 409)
    if payload.status == "approved":
        data = option_input(option)
        if data.discovery_status != "found" or not data.url or not data.evidence_url:
            raise fail("service_identity_required")
        if not payload.identity_note.strip():
            raise fail("service_identity_required")
        await safe_click_target(option)
        try:
            health = await check_hotel_link(
                HotelLink(provider=data.provider, url=data.url, evidence_url=data.evidence_url)
            )
        except (httpx.HTTPError, ConnectionError, TimeoutError):
            health = "unconfirmed"
        except ValueError:
            health = "unsafe"
        if health in ("unsafe", "unavailable") or (
            health != "healthy" and not payload.browser_verified
        ):
            raise fail("service_link_unavailable")
        option.identity_note = payload.identity_note
        option.health_status, option.checked_at = health, datetime.now(UTC)
    option.status = payload.status
    option.verified_at = datetime.now(UTC) if payload.status == "approved" else None
    option.version += 1
    audit(
        session,
        user,
        "hotel_option_review",
        str(option.id),
        {"status": option.status, "browser_verified": payload.browser_verified},
    )
    await session.commit()
    return record(option)


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


def _validate_destination_offer(
    payload: DestinationOfferInput,
    brand: TravelServiceBrand | None,
    project_id: str | None,
) -> None:
    if (
        not brand
        or brand.project_id != project_id
        or brand.code not in BRANDS
        or payload.module not in BRANDS[brand.code].supported_modules
    ):
        raise fail("service_brand_unavailable")
    try:
        brand_target(brand.code, payload.target_url)
        if payload.static_url:
            affiliate_target(payload.static_url)
    except ValueError as exc:
        raise fail("service_offer_mismatch") from exc


@router.post("/destination-offers", status_code=201)
async def create_destination_offer(
    payload: DestinationOfferInput,
    user: AdminUser,
    session: Session,
) -> dict[str, Any]:
    settings = await load_runtime_settings(session)
    brand = await session.get(TravelServiceBrand, payload.brand_id)
    _validate_destination_offer(payload, brand, settings.travelpayouts_project_id)
    existing = await session.scalar(
        select(DestinationAffiliateOffer).where(
            DestinationAffiliateOffer.brand_id == payload.brand_id,
            DestinationAffiliateOffer.destination_id == payload.destination_id,
            DestinationAffiliateOffer.module == payload.module,
        )
    )
    if existing:
        raise fail("service_offer_mismatch", 409)
    row = DestinationAffiliateOffer(**payload.model_dump(), status="pending", version=1)
    session.add(row)
    await session.flush()
    audit(
        session,
        user,
        "destination_offer_create",
        str(row.id),
        {"destination_id": row.destination_id, "module": row.module},
    )
    await session.commit()
    return record(row)


@router.put("/destination-offers/{offer_id}")
async def edit_destination_offer(
    offer_id: UUID,
    payload: DestinationOfferInput,
    user: AdminUser,
    session: Session,
    version: int = Query(..., ge=1),
) -> dict[str, Any]:
    row = await session.scalar(
        select(DestinationAffiliateOffer)
        .where(DestinationAffiliateOffer.id == offer_id)
        .with_for_update()
    )
    if not row or row.version != version:
        raise fail("service_version_conflict", 409)
    settings = await load_runtime_settings(session)
    brand = await session.get(TravelServiceBrand, payload.brand_id)
    _validate_destination_offer(payload, brand, settings.travelpayouts_project_id)
    duplicate = await session.scalar(
        select(DestinationAffiliateOffer.id).where(
            DestinationAffiliateOffer.brand_id == payload.brand_id,
            DestinationAffiliateOffer.destination_id == payload.destination_id,
            DestinationAffiliateOffer.module == payload.module,
            DestinationAffiliateOffer.id != offer_id,
        )
    )
    if duplicate:
        raise fail("service_offer_mismatch", 409)
    for key, value in payload.model_dump().items():
        setattr(row, key, value)
    row.status = "pending"
    row.verified_at = None
    row.verification_context = None
    row.version += 1
    audit(session, user, "destination_offer_edit", str(row.id))
    await session.commit()
    return record(row)


async def _review_destination_offer_row(
    row: DestinationAffiliateOffer,
    status: str,
    session: Session,
) -> None:
    if status == "approved":
        brand = await session.get(TravelServiceBrand, row.brand_id)
        settings = await load_runtime_settings(session)
        if (
            not brand
            or not ready_brand(brand, settings, datetime.now(UTC))
            or row.module not in BRANDS[brand.code].supported_modules
        ):
            raise fail("service_brand_unavailable")
        try:
            if not row.static_url and not BRANDS[brand.code].api_supported:
                raise fail("service_link_unavailable")
            if not row.static_url and not (
                settings.travelpayouts_api_token
                and settings.travelpayouts_marker
                and settings.travelpayouts_project_id
            ):
                raise fail("service_brand_unavailable")
            target = row.static_url or await TravelpayoutsLinkClient(
                get_redis(), settings
            ).create(
                row.target_url,
                "dst_verify",
                cache_context=f"destination-verify:{row.id}:{row.version}",
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
    row.status = status
    row.verified_at = datetime.now(UTC) if status == "approved" else None
    row.version += 1


@router.post("/destination-offers/batch-review")
async def batch_review_destination_offers(
    payload: DestinationOfferBatchReview,
    user: AdminUser,
    session: Session,
) -> dict[str, Any]:
    expected = {item.id: item.version for item in payload.offers}
    if len(expected) != len(payload.offers):
        raise fail("service_version_conflict", 409)
    rows = list(
        await session.scalars(
            select(DestinationAffiliateOffer)
            .where(DestinationAffiliateOffer.id.in_(expected))
            .with_for_update()
        )
    )
    if len(rows) != len(expected) or any(row.version != expected[row.id] for row in rows):
        raise fail("service_version_conflict", 409)
    for row in rows:
        await _review_destination_offer_row(row, payload.status, session)
    audit(
        session,
        user,
        "destination_offer_batch_review",
        "batch",
        {"status": payload.status, "count": len(rows)},
    )
    await session.commit()
    return {"updated": len(rows), "status": payload.status}


@router.post("/destination-offers/{offer_id}/review")
async def review_destination_offer(
    offer_id: UUID,
    payload: ReviewInput,
    user: AdminUser,
    session: Session,
) -> dict[str, Any]:
    row = await session.scalar(
        select(DestinationAffiliateOffer)
        .where(DestinationAffiliateOffer.id == offer_id)
        .with_for_update()
    )
    if not row or row.version != payload.version:
        raise fail("service_version_conflict", 409)
    await _review_destination_offer_row(row, payload.status, session)
    audit(
        session,
        user,
        "destination_offer_review",
        str(row.id),
        {"status": row.status},
    )
    await session.commit()
    return record(row)


@router.post("/imports/preview")
async def preview_import(payload: CsvInput, user: AdminUser, session: Session) -> dict[str, Any]:
    rows = parse_csv(payload.csv)
    seen = set()
    for item in rows:
        if "error" in item:
            continue
        data = ProductInput.model_validate(item["product"])
        if data.source_key in seen:
            item["error"] = "service_csv_invalid"
            continue
        seen.add(data.source_key)
        existing = await session.scalar(
            select(TravelServiceProduct).where(TravelServiceProduct.source_key == data.source_key)
        )
        item["change"] = "new" if existing is None else "modified"
        if existing and product_input(existing) == data and not item.get("booking_options"):
            item["change"] = "unchanged"
        options = item.get("booking_options") or data.facts.hotel_links
        providers = {o.get("provider") if isinstance(o, dict) else o.provider for o in options}
        item["missing_platforms"] = (
            [
                p
                for p in ("official", "booking", "trip_com", "agoda", "expedia", "rakuten")
                if p not in providers
            ]
            if data.kind == "hotel"
            else []
        )
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
    result = await commit_import(session, run_id, settings.travelpayouts_project_id)
    audit(session, user, "import_commit", str(run_id), result)
    await session.commit()
    return result
