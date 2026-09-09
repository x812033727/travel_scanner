"""One reviewed property identity per platform, independent of affiliate enrollment."""

from datetime import datetime, timedelta
from typing import Any, cast
from urllib.parse import urlsplit

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models import (
    HotelBookingOption,
    TravelServiceBrand,
    TravelServiceOffer,
    TravelServiceProduct,
)
from app.travel_services.schemas import (
    HOTEL_PROVIDERS,
    CatalogConfig,
    HotelLink,
    HotelOptionInput,
    HotelProvider,
)


def option_input(option: HotelBookingOption) -> HotelOptionInput:
    return HotelOptionInput.model_validate(
        {key: getattr(option, key) for key in HotelOptionInput.model_fields}
    )


async def upsert_option(
    session: AsyncSession, product: TravelServiceProduct, data: HotelOptionInput
) -> tuple[HotelBookingOption, bool]:
    from app.travel_services.service import fail

    if product.kind != "hotel":
        raise fail("service_identity_required")
    keys = []
    if data.url:
        keys.append(HotelBookingOption.url == data.url)
    if data.property_id:
        keys.append(HotelBookingOption.property_id == data.property_id)
    if keys and await session.scalar(
        select(HotelBookingOption.id).where(
            HotelBookingOption.provider == data.provider,
            HotelBookingOption.product_id != product.id,
            or_(*keys),
        )
    ):
        raise fail("service_offer_mismatch", 409)
    # Reviews lock the option, not its parent product. Refresh under the same lock
    # so an import/editor cannot overwrite a concurrently completed review.
    option = await session.scalar(
        select(HotelBookingOption)
        .where(
            HotelBookingOption.product_id == product.id,
            HotelBookingOption.provider == data.provider,
        )
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if option and option_input(option) == data:
        return option, False
    if option is None:
        option = HotelBookingOption(
            **data.model_dump(), status="pending", version=1, health_status="unchecked"
        )
        product.hotel_options.append(option)
    else:
        for key, value in data.model_dump().items():
            setattr(option, key, value)
        option.status, option.verified_at = "pending", None
        option.health_status, option.checked_at = "unchecked", None
        option.version += 1
    try:
        await session.flush()
    except IntegrityError as exc:
        # Concurrent imports of different hotels can race the friendly pre-check above.
        # The request transaction rolls back; never surface raw database/identity details.
        raise fail("service_offer_mismatch", 409) from exc
    return option, True


def ready_option(
    product: TravelServiceProduct, option: HotelBookingOption, config: CatalogConfig, now: datetime
) -> bool:
    from app.travel_services.service import product_enabled

    if not (
        product.kind == "hotel"
        and product.status == "approved"
        and product_enabled(config, product)
        and option.status == "approved"
        and option.discovery_status == "found"
        and option.verified_at
        and now - timedelta(days=30) <= option.verified_at <= now
        and option.health_status not in ("unsafe", "unavailable")
    ):
        return False
    try:
        option_input(option)
    except ValueError:
        return False
    return True


def same_hotel_target(provider: str, first: str | None, second: str | None) -> bool:
    if not first or not second:
        return False
    if provider != "klook":
        return first == second
    from app.travel_services.channels import klook_product_target, same_klook_identity

    try:
        klook_product_target(first, "hotel")
        klook_product_target(second, "hotel")
        # Keep query identity both ways: an alias must not discard dates/package choices.
        return same_klook_identity(first, second) and same_klook_identity(second, first)
    except ValueError:
        return False


async def matching_offer(
    session: AsyncSession,
    product: TravelServiceProduct,
    option: HotelBookingOption,
    settings: Settings,
    now: datetime,
) -> TravelServiceOffer | None:
    from app.travel_services.channels import channel_for
    from app.travel_services.service import ready_offer

    # Same product AND platform; Klook may use its equivalent typed numeric property alias.
    # Destination offers never qualify, and other platforms retain exact-URL matching.
    pairs = (
        await session.execute(
            select(TravelServiceOffer, TravelServiceBrand)
            .join(TravelServiceBrand, TravelServiceBrand.id == TravelServiceOffer.brand_id)
            .where(
                TravelServiceOffer.product_id == product.id,
                TravelServiceOffer.scope == "product",
                TravelServiceBrand.code == option.provider,
            )
        )
    ).all()
    return next(
        (
            offer for offer, brand in sorted(
                pairs, key=lambda row: (channel_for(row[1]) != "klook_direct", str(row[0].id))
            ) if same_hotel_target(option.provider, option.url, offer.target_url)
            and ready_offer(offer, brand, product, settings, now)
        ), None
    )


async def public_options(
    session: AsyncSession,
    product: TravelServiceProduct,
    config: CatalogConfig,
    settings: Settings,
    now: datetime,
    eligible_targets: set[tuple[str, str]] | None = None,
    *,
    tracking_allowed: bool = True,
) -> list[dict[str, Any]]:
    from app.travel_services.hotel_quotes import ADAPTERS
    from app.travel_services.registry import BRANDS
    from app.travel_services.stay22 import booking_channel

    result = []
    for option in sorted(product.hotel_options, key=lambda o: HOTEL_PROVIDERS.index(o.provider)):
        if not ready_option(product, option, config, now):
            continue
        has_offer = (
            any(
                provider == option.provider and same_hotel_target(provider, option.url, target)
                for provider, target in eligible_targets
            )
            if eligible_targets is not None
            else bool(await matching_offer(session, product, option, settings, now))
        )
        channel = booking_channel(
            option, config, has_offer=has_offer, tracking_allowed=tracking_allowed
        )
        if channel is None:
            continue
        policy = config.hotel_quote_policies.get(cast(HotelProvider, option.provider))
        can_quote = bool(
            policy and policy.enabled and option.property_id and option.provider in ADAPTERS
        )
        result.append(
            {
                "id": str(option.id),
                "provider": option.provider,
                "name": BRANDS[option.provider].name if option.provider != "official" else None,
                "mode": "direct" if channel == "direct" else "affiliate",
                # Ordinary links preserve the pre-Allez response shape. The
                # optional channel describes affiliates, never a new OTA identity.
                **({"affiliate_channel": channel} if channel != "direct" else {}),
                "quote_status": "ready" if can_quote else "not_configured",
            }
        )
    return result


async def safe_click_target(option: HotelBookingOption) -> str:
    from app.catalog_review.evidence import public_request_target
    from app.travel_services.service import fail

    data = option_input(option)
    assert data.url and data.evidence_url
    HotelLink(provider=data.provider, url=data.url, evidence_url=data.evidence_url)
    # DNS safety only, never fetch booking pages in the user's click path.
    if await public_request_target(data.url) is None:
        raise fail("service_link_unavailable", 503)
    return data.url


def legacy_links(product: TravelServiceProduct) -> list[HotelLink]:
    return [
        HotelLink(provider=o.provider, url=o.url, evidence_url=o.evidence_url)
        for o in product.hotel_options
        if o.discovery_status == "found" and o.url and o.evidence_url
    ]


def needs_source_credit(product: TravelServiceProduct) -> bool:
    facts = product.facts
    source = facts.get("coordinate_source_url")
    if not source or urlsplit(source).hostname == urlsplit(product.source_url).hostname:
        return False
    return not any(c.get("url") == source for c in facts.get("source_credits", []))
