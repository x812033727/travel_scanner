"""Bounded projections of current public records, never provider discovery calls."""

import json
from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import UUID

from sqlalchemy import Text, and_, exists, or_, select
from sqlalchemy import cast as sql_cast
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import effective_site_visibility
from app.community.content import public_media_refs, published_post
from app.community.policy import public_profile, settings_for
from app.community.videos import youtube_embed_metadata
from app.db import escape_like
from app.discovery.display_topics import attach_catalog_display_topics
from app.discovery.policy import (
    aware,
    catalog_destination_ids,
    destination_id,
    destination_payload,
    safe_source,
    stamp,
)
from app.discovery.schemas import DiscoveryItem, Kind
from app.discovery.taxonomy import display_category_topics
from app.foods.publication import publishable_merchant_filters
from app.i18n import Locale
from app.models import (
    FoodDestination,
    FoodLocalization,
    FoodMerchant,
    HotspotGuide,
    HotspotLocalization,
    TravelFood,
    TravelHotspot,
    TravelServiceProduct,
    User,
)
from app.problems import AppError
from app.travel_services.service import catalog_config, product_enabled

SOURCE_LIMIT = 100


def matching(q: str, *columns: Any) -> Any:
    return or_(*(column.ilike(f"%{escape_like(q)}%", escape="\\") for column in columns))


def base_item(
    kind: Kind,
    identifier: UUID,
    title: str,
    locale: str,
    destination: str,
    updated: datetime | None,
    *,
    summary: str = "",
    source: str | None = None,
    topics: list[str] | None = None,
) -> DiscoveryItem:
    key_kind = "guide" if kind in {"article", "video"} else "post" if kind == "itinerary" else kind
    return DiscoveryItem(
        id=f"{key_kind}:{identifier}",
        kind=kind,
        title=title,
        summary=summary[:1200],
        destination=destination_payload(destination, cast(Locale, locale)),
        locale=locale,
        href=f"/{locale}/explore?content={kind}%3A{identifier}",
        source={"label": "Mokaair", "url": safe_source(source), "kind": "editorial"},
        updated_at=stamp(updated),
        collection_ref={"kind": key_kind, "id": str(identifier)},
        topics=topics or [],
        display_topics=display_category_topics(kind, topics or [], cast(Locale, locale)),
    )


async def catalog_items(
    session: AsyncSession,
    locale: Locale,
    *,
    q: str = "",
    destinations: list[str] | None = None,
    kinds: set[str] | None = None,
    identifiers: dict[str, list[UUID]] | None = None,
    content_locale: Locale | None = None,
    topics: list[str] | None = None,
    related_hotspot_id: UUID | None = None,
) -> list[DiscoveryItem]:
    """Every query is limited; explicit references never widen into a catalog scan."""
    output: list[DiscoveryItem] = []
    hotspot_refs: dict[str, UUID] = {}
    destinations = catalog_destination_ids(destinations or [])
    q_city = destination_id(q) if q else ""
    visibility = await effective_site_visibility(session)
    now = datetime.now(UTC)

    def enabled(kind: str) -> bool:
        return (not kinds or kind in kinds) and (identifiers is None or bool(identifiers.get(kind)))

    def conditions(model: Any, kind: str, city_column: Any = None) -> list[Any]:
        result = []
        if identifiers is not None:
            result.append(model.id.in_(identifiers.get(kind, [])))
        if destinations and city_column is not None:
            result.append(city_column.in_(destinations))
        return result

    active_hotspot = [
        TravelHotspot.is_active.is_(True),
        TravelHotspot.review_status.in_(("approved", "auto_approved")),
    ]
    if visibility.hotspots_enabled and enabled("hotspot"):
        filters = [
            *active_hotspot,
            *conditions(TravelHotspot, "hotspot", TravelHotspot.destination_id),
        ]
        if topics:
            filters.append(TravelHotspot.category.in_(topics))
        if q:
            aliases = exists(
                select(HotspotLocalization.id)
                .correlate(TravelHotspot)
                .where(
                    HotspotLocalization.hotspot_id == TravelHotspot.id,
                    matching(
                        q,
                        HotspotLocalization.name,
                        sql_cast(HotspotLocalization.aliases, Text),
                        sql_cast(HotspotLocalization.search_terms, Text),
                    ),
                )
            )
            filters.append(
                or_(
                    matching(q, TravelHotspot.name, TravelHotspot.search_text),
                    aliases,
                    TravelHotspot.destination_id.in_(catalog_destination_ids([q_city])),
                )
            )
        hotspot_rows = (
            await session.execute(
                select(TravelHotspot, HotspotLocalization.name)
                .outerjoin(
                    HotspotLocalization,
                    and_(
                        HotspotLocalization.hotspot_id == TravelHotspot.id,
                        HotspotLocalization.locale == locale,
                    ),
                )
                .where(*filters)
                .order_by(TravelHotspot.updated_at.desc(), TravelHotspot.id)
                .limit(SOURCE_LIMIT)
                .execution_options(populate_existing=True)
            )
        ).all()
        for hotspot, localized in hotspot_rows:
            item = base_item(
                "hotspot",
                hotspot.id,
                localized or hotspot.name,
                locale,
                hotspot.destination_id,
                hotspot.updated_at,
                topics=[hotspot.category],
                source=next(iter(hotspot.source_urls or []), None),
            )
            item.place_ref = {
                "kind": "hotspot",
                "id": str(hotspot.id),
                "destination_id": hotspot.destination_id,
            }
            if hotspot.map_match_status == "verified":
                item.place_ref["selection_path"] = f"/hotspots/{hotspot.id}/trip-selections"
            hotspot_refs[item.id] = hotspot.id
            output.append(item)

    if enabled("food"):
        filters = [
            TravelFood.is_active.is_(True),
            TravelFood.review_status == "approved",
            *conditions(TravelFood, "food"),
        ]
        if topics and "food" not in topics:
            filters.append(
                or_(
                    TravelFood.food_kind.in_(topics),
                    *[
                        sql_cast(TravelFood.ingredient_tags, Text).contains(json.dumps(topic))
                        for topic in topics
                    ],
                )
            )
        if destinations:
            filters.append(
                exists(
                    select(FoodDestination.id).where(
                        FoodDestination.food_id == TravelFood.id,
                        FoodDestination.destination_id.in_(destinations),
                    )
                )
            )
        if q:
            filters.append(
                or_(
                    matching(
                        q, TravelFood.local_name, TravelFood.romanized_name, TravelFood.search_text
                    ),
                    exists(
                        select(FoodLocalization.id)
                        .correlate(TravelFood)
                        .where(
                            FoodLocalization.food_id == TravelFood.id,
                            matching(q, FoodLocalization.name, FoodLocalization.summary),
                        )
                    ),
                    exists(
                        select(FoodDestination.id).where(
                            FoodDestination.food_id == TravelFood.id,
                            FoodDestination.destination_id.in_(catalog_destination_ids([q_city])),
                        )
                    ),
                )
            )
        food_rows = (
            await session.execute(
                select(TravelFood, FoodLocalization)
                .outerjoin(
                    FoodLocalization,
                    and_(
                        FoodLocalization.food_id == TravelFood.id, FoodLocalization.locale == locale
                    ),
                )
                .where(*filters)
                .order_by(TravelFood.updated_at.desc(), TravelFood.id)
                .limit(SOURCE_LIMIT)
                .execution_options(populate_existing=True)
            )
        ).all()
        destination_rows = (
            (
                await session.execute(
                    select(FoodDestination.food_id, FoodDestination.destination_id)
                    .where(FoodDestination.food_id.in_([row[0].id for row in food_rows]))
                    .order_by(FoodDestination.display_order, FoodDestination.destination_id)
                    .limit(SOURCE_LIMIT * 50)
                )
            ).all()
            if food_rows
            else []
        )
        food_cities: dict[UUID, str] = {}
        for food_id, city in destination_rows:
            if not destinations or city in destinations:
                food_cities.setdefault(food_id, city)
        for food, translated in food_rows:
            item = base_item(
                "food",
                food.id,
                translated.name if translated else food.local_name,
                locale,
                food_cities.get(food.id, ""),
                food.updated_at,
                summary=translated.summary if translated else "",
                topics=["food", food.food_kind, *(food.ingredient_tags or [])],
                source=next(iter(food.source_urls or []), None),
            )
            item.place_ref = {"kind": "food", "id": str(food.id)}
            if food_cities.get(food.id):
                item.place_ref["destination_id"] = food_cities[food.id]
            output.append(item)

    if enabled("merchant") and (not topics or "food" in topics):
        filters = [
            *publishable_merchant_filters(),
            *conditions(FoodMerchant, "merchant", FoodMerchant.destination_id),
        ]
        if q:
            filters.append(
                or_(
                    matching(
                        q,
                        FoodMerchant.name,
                        FoodMerchant.local_name,
                        sql_cast(FoodMerchant.names_json, Text),
                    ),
                    FoodMerchant.destination_id.in_(catalog_destination_ids([q_city])),
                )
            )
        merchant_rows = (
            await session.scalars(
                select(FoodMerchant)
                .where(*filters)
                .order_by(FoodMerchant.updated_at.desc(), FoodMerchant.id)
                .limit(SOURCE_LIMIT)
                .execution_options(populate_existing=True)
            )
        ).all()
        for merchant in merchant_rows:
            item = base_item(
                "merchant",
                merchant.id,
                (merchant.names_json or {}).get(locale) or merchant.name,
                locale,
                merchant.destination_id,
                merchant.updated_at,
                topics=["food"],
                source=merchant.official_website_url
                if merchant.official_website_verified_at
                else None,
            )
            item.place_ref = {
                "kind": "merchant",
                "id": str(merchant.id),
                "destination_id": merchant.destination_id,
                "selection_path": f"/foods/merchants/{merchant.id}/trip-selections",
            }
            output.append(item)

    if enabled("hotel") and (not topics or "hotel" in topics):
        config, _ = await catalog_config(session)
        if config.public_enabled and "hotel" in config.enabled_kinds:
            filters = [
                TravelServiceProduct.kind == "hotel",
                TravelServiceProduct.status == "approved",
                TravelServiceProduct.destination_id.in_(config.enabled_destinations),
                TravelServiceProduct.verified_at >= now - timedelta(days=30),
                TravelServiceProduct.verified_at <= now,
                *conditions(TravelServiceProduct, "hotel", TravelServiceProduct.destination_id),
            ]
            if q:
                filters.append(
                    or_(
                        matching(
                            q,
                            TravelServiceProduct.title,
                            sql_cast(TravelServiceProduct.names_json, Text),
                        ),
                        TravelServiceProduct.destination_id.in_(catalog_destination_ids([q_city])),
                    )
                )
            products = (
                await session.scalars(
                    select(TravelServiceProduct)
                    .where(*filters)
                    .order_by(TravelServiceProduct.updated_at.desc(), TravelServiceProduct.id)
                    .limit(SOURCE_LIMIT)
                    .execution_options(populate_existing=True)
                )
            ).all()
            for product in products:
                if product_enabled(config, product):
                    item = base_item(
                        "hotel",
                        product.id,
                        (product.names_json or {}).get(locale) or product.title,
                        locale,
                        product.destination_id,
                        product.updated_at,
                        topics=["hotel"],
                        source=product.source_url,
                    )
                    # No reference price, quote or unreviewed booking URL enters discovery.
                    output.append(item)

    if visibility.hotspots_enabled and (
        enabled("guide") or (identifiers is None and (not kinds or kinds & {"article", "video"}))
    ):
        filters = [
            *active_hotspot,
            HotspotGuide.review_status == "approved",
            or_(
                HotspotGuide.provider != "youtube",
                and_(
                    HotspotGuide.last_verified_at >= now - timedelta(days=30),
                    HotspotGuide.last_verified_at <= now,
                    HotspotGuide.metadata_expires_at > now,
                ),
            ),
            *conditions(HotspotGuide, "guide", TravelHotspot.destination_id),
        ]
        if topics:
            filters.append(TravelHotspot.category.in_(topics))
        if related_hotspot_id is not None:
            filters.append(HotspotGuide.hotspot_id == related_hotspot_id)
        if kinds and kinds & {"article", "video"}:
            filters.append(HotspotGuide.content_type.in_(kinds & {"article", "video"}))
        if content_locale:
            filters.append(HotspotGuide.locale == content_locale)
        if q:
            filters.append(
                or_(
                    matching(
                        q, HotspotGuide.title, HotspotGuide.summary, TravelHotspot.search_text
                    ),
                    TravelHotspot.destination_id.in_(catalog_destination_ids([q_city])),
                )
            )
        guide_rows = (
            await session.execute(
                select(HotspotGuide, TravelHotspot)
                .join(TravelHotspot, TravelHotspot.id == HotspotGuide.hotspot_id)
                .where(*filters)
                .order_by(HotspotGuide.updated_at.desc(), HotspotGuide.id)
                .limit(SOURCE_LIMIT)
                .execution_options(populate_existing=True)
            )
        ).all()
        for guide, hotspot in guide_rows:
            # Google/YouTube metadata may not outlive its permitted cache window.
            if guide.provider == "youtube" and (
                not guide.last_verified_at
                or not guide.metadata_expires_at
                or not now - timedelta(days=30) <= aware(guide.last_verified_at) <= now
                or aware(guide.metadata_expires_at) <= now
            ):
                continue
            source = safe_source(guide.canonical_url)
            if not source:
                continue
            item = base_item(
                cast(Kind, guide.content_type),
                guide.id,
                guide.title,
                locale,
                hotspot.destination_id,
                guide.updated_at,
                summary=guide.summary or "",
                source=source,
                topics=[hotspot.category],
            )
            item.source = {
                "label": guide.creator_name or guide.provider,
                "url": source,
                "kind": "editorial",
            }
            item.published_at = stamp(guide.published_at)
            item.locale = guide.locale
            item.content = {"text": guide.summary or "", "format": "plain"}
            hotspot_refs[item.id] = hotspot.id
            if guide.content_type == "video":
                item.video = {
                    "provider": guide.provider,
                    "video_id": guide.provider_content_id,
                    "source_url": source,
                    **youtube_embed_metadata(guide),
                }
            output.append(item)
    await attach_catalog_display_topics(session, output, hotspot_refs, locale)
    return output


async def community_item(
    session: AsyncSession, identifier: UUID, viewer: User | None, locale: Locale
) -> DiscoveryItem | None:
    if not (await settings_for(session)).enabled:
        return None
    try:
        post, revision, profile = await published_post(session, identifier, viewer)
    except AppError as exc:
        if exc.status == 404:
            return None
        raise
    kind: Kind = "itinerary" if revision.itinerary is not None else "post"
    item = base_item(
        kind,
        post.id,
        revision.title,
        locale,
        destination_id(revision.destination),
        revision.created_at,
        summary=revision.body,
        topics=revision.topics or [],
    )
    item.href = f"/{locale}/community/posts/{post.id}"
    item.locale = revision.locale
    item.author = public_profile(profile)
    item.source = {"label": profile.display_name, "url": None, "kind": "community"}
    item.published_at = stamp(post.published_at)
    # This is the already-allowlisted publication snapshot, never a private TripPlan.
    item.content = {"text": revision.body, "format": "plain", "itinerary": revision.itinerary}
    item.content["media"] = await public_media_refs(session, revision)
    from app.community.videos import public_video_refs

    item.content["video_refs"] = await public_video_refs(session, revision.video_refs or [])
    return item
