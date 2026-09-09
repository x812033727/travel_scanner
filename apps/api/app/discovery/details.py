"""Lazy public detail projections; no provider requests and no private trip reads."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.discovery.policy import safe_source
from app.discovery.schemas import (
    DiscoveryDetail,
    DiscoveryItem,
    DiscoveryPlanning,
    PlanningMerchant,
)
from app.discovery.sources import catalog_items
from app.foods.publication import publishable_merchant_filters
from app.foods.service import _serialize_merchant_cards
from app.hotspots.intros import load_public_intros
from app.hotspots.maps import has_exact_map_identity
from app.hotspots.places import place_detail_payload
from app.i18n import Locale
from app.locations.coordinates import has_durable_coordinates
from app.models import (
    FoodMerchant,
    FoodMerchantFood,
    HotspotGuide,
    HotspotPlaceProfile,
    TravelHotspot,
    TravelServiceBrand,
    TravelServiceOffer,
    TravelServiceProduct,
)
from app.problems import AppError
from app.travel_services.hotel_options import public_options
from app.travel_services.registry import BRANDS
from app.travel_services.service import (
    catalog_config,
    product_input,
    public_product,
    ready_hotel_links,
    ready_offer,
    require_product_review,
)


def hotspot_planning(hotspot: TravelHotspot) -> DiscoveryPlanning | None:
    if not (
        hotspot.map_match_status == "verified"
        and has_exact_map_identity(
            hotspot.country_code, hotspot.google_place_id, hotspot.naver_map_url
        )
        and has_durable_coordinates(
            hotspot.latitude,
            hotspot.longitude,
            hotspot.coordinate_source_type,
            hotspot.coordinate_source_url,
        )
    ):
        return None
    return DiscoveryPlanning(
        kind="hotspot",
        id=str(hotspot.id),
        destination_id=hotspot.destination_id,
        selection_path=f"/hotspots/{hotspot.id}/trip-selections",
    )


async def hotspot_detail(
    session: AsyncSession, hotspot: TravelHotspot, locale: Locale
) -> DiscoveryDetail:
    profile = await session.scalar(
        select(HotspotPlaceProfile).where(HotspotPlaceProfile.hotspot_id == hotspot.id)
    )
    # SQLite fixtures return naive database timestamps; never modify tracked data
    # merely to project it. Production PostgreSQL timestamps are UTC-aware.
    now = datetime.now(UTC)
    if profile and profile.provider_expires_at and profile.provider_expires_at.tzinfo is None:
        now = now.replace(tzinfo=None)
    runtime = await load_runtime_settings(session)
    place = place_detail_payload(
        hotspot,
        profile,
        now=now,
        configured=bool(runtime.google_maps_api_key and runtime.hotspot_place_enrichment_enabled),
    )
    place["official_website_url"] = safe_source(place.get("official_website_url"))
    intro = (await load_public_intros(session, [hotspot.id], locale)).get(hotspot.id)
    guides = await catalog_items(
        session,
        locale,
        kinds={"article", "video"},
        related_hotspot_id=hotspot.id,
        content_locale=locale,
    )
    return DiscoveryDetail(
        intro=intro,
        place=place,
        guides=[item.model_dump(mode="json", exclude={"detail"}) for item in guides[:10]],
        planning=hotspot_planning(hotspot),
    )


async def merchant_cards(
    session: AsyncSession,
    locale: Locale,
    *,
    food_id: UUID | None = None,
    merchant_id: UUID | None = None,
) -> list[dict[str, Any]]:
    query = select(FoodMerchant).where(*publishable_merchant_filters())
    if food_id is not None:
        query = query.join(FoodMerchantFood, FoodMerchantFood.merchant_id == FoodMerchant.id).where(
            FoodMerchantFood.food_id == food_id
        )
    elif merchant_id is not None:
        query = query.where(FoodMerchant.id == merchant_id)
    else:
        return []
    merchants = list(
        (
            await session.scalars(
                query.order_by(
                    FoodMerchant.display_order, FoodMerchant.name, FoodMerchant.id
                ).limit(30)
            )
        ).all()
    )
    # This serializer rechecks exact identity, durable coordinates, current sources,
    # and existing reservation-link publication policy. No Google cache is copied.
    cards = await _serialize_merchant_cards(session, merchants, locale)
    for card in cards:
        card["official_website_url"] = safe_source(card.get("official_website_url"))
    return cards


async def hotel_detail(
    session: AsyncSession, product: TravelServiceProduct, locale: Locale
) -> DiscoveryDetail:
    now = datetime.now(UTC)
    if product.verified_at and product.verified_at.tzinfo is None:
        now = now.replace(tzinfo=None)
    config, _ = await catalog_config(session)
    settings = await load_runtime_settings(session)
    try:
        hotel = public_product(product, locale, now)
    except ValidationError:
        # Corrupt legacy facts are not a capability to mutate a trip.
        return DiscoveryDetail()
    hotel["source_url"] = safe_source(hotel.get("source_url"))
    targets: set[tuple[str, str]] = set()
    pairs = (
        await session.execute(
            select(TravelServiceOffer, TravelServiceBrand)
            .join(TravelServiceBrand, TravelServiceBrand.id == TravelServiceOffer.brand_id)
            .where(TravelServiceOffer.product_id == product.id)
            .order_by(TravelServiceOffer.id)
            .limit(100)
        )
    ).all()
    for offer, brand in pairs:
        if ready_offer(offer, brand, product, settings, now):
            if offer.scope == "product":
                targets.add((brand.code, offer.target_url))
            hotel["offers"].append(
                {
                    "id": str(offer.id),
                    "brand": brand.code,
                    "brand_name": BRANDS[brand.code].name,
                    "scope": offer.scope,
                }
            )
    hotel["booking_options"] = await public_options(
        session, product, config, settings, now, targets
    )
    hotel["direct_links"] = [
        {
            "provider": link.provider,
            "name": BRANDS[link.provider].name if link.provider != "official" else None,
        }
        for link in ready_hotel_links(product, config, now)
    ]
    detail = DiscoveryDetail(hotel=hotel)
    try:
        require_product_review(product_input(product))
    except (AppError, ValidationError, KeyError, ValueError):
        return detail
    detail.planning = DiscoveryPlanning(
        kind="hotel",
        id=str(product.id),
        product_id=str(product.id),
        destination_id=product.destination_id,
    )
    return detail


async def enrich_detail(
    session: AsyncSession, item: DiscoveryItem, locale: Locale
) -> DiscoveryItem:
    """Called only after the live discovery resolver authorized this exact record."""
    identifier = UUID(item.id.split(":", 1)[1])
    item.detail = DiscoveryDetail()
    if item.kind in {"hotspot", "article", "video"}:
        hotspot_id = identifier
        if item.kind != "hotspot":
            guide = await session.get(HotspotGuide, identifier)
            if guide is None:
                return item
            hotspot_id = guide.hotspot_id
        hotspot = await session.get(TravelHotspot, hotspot_id)
        if hotspot:
            item.detail = await hotspot_detail(session, hotspot, locale)
            item.place_ref = {
                "kind": "hotspot",
                "id": str(hotspot.id),
                "destination_id": hotspot.destination_id,
            }
            if item.detail.planning and item.detail.planning.selection_path:
                item.place_ref["selection_path"] = item.detail.planning.selection_path
            if item.kind == "hotspot" and item.detail.intro:
                item.content = {"text": item.detail.intro["body"], "format": "plain"}
    elif item.kind in {"food", "merchant"}:
        cards = await merchant_cards(
            session,
            locale,
            food_id=identifier if item.kind == "food" else None,
            merchant_id=identifier if item.kind == "merchant" else None,
        )
        item.detail.merchants = cards
        if cards:
            item.detail.planning = DiscoveryPlanning(
                kind=item.kind,
                id=str(identifier),
                destination_id=item.place_ref.get("destination_id") if item.place_ref else None,
                selection_path=f"/foods/{identifier}/trip-selections"
                if item.kind == "food"
                else f"/foods/merchants/{identifier}/trip-selections",
                merchants=[
                    PlanningMerchant(
                        id=card["id"],
                        name=card["name"],
                        destination_id=card["destination_id"],
                        selection_path=f"/foods/merchants/{card['id']}/trip-selections",
                    )
                    for card in cards
                ],
            )
        if item.summary:
            item.content = {"text": item.summary, "format": "plain"}
    elif item.kind == "hotel":
        product = await session.get(TravelServiceProduct, identifier)
        if product:
            item.detail = await hotel_detail(session, product, locale)
    return item
