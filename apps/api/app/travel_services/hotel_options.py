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


async def matching_offer(
    session: AsyncSession,
    product: TravelServiceProduct,
    option: HotelBookingOption,
    settings: Settings,
    now: datetime,
) -> TravelServiceOffer | None:
    from app.travel_services.service import ready_offer

    # Exact canonical target, same product AND same platform. Destination offers never qualify.
    pairs = (
        await session.execute(
            select(TravelServiceOffer, TravelServiceBrand)
            .join(TravelServiceBrand, TravelServiceBrand.id == TravelServiceOffer.brand_id)
            .where(
                TravelServiceOffer.product_id == product.id,
                TravelServiceOffer.target_url == option.url,
                TravelServiceOffer.scope == "product",
                TravelServiceBrand.code == option.provider,
                TravelServiceBrand.project_id == (settings.travelpayouts_project_id or ""),
            )
        )
    ).all()
    return next(
        (offer for offer, brand in pairs if ready_offer(offer, brand, product, settings, now)), None
    )


async def public_options(
    session: AsyncSession,
    product: TravelServiceProduct,
    config: CatalogConfig,
    settings: Settings,
    now: datetime,
    eligible_targets: set[tuple[str, str]] | None = None,
) -> list[dict[str, Any]]:
    from app.travel_services.hotel_quotes import ADAPTERS
    from app.travel_services.registry import BRANDS

    result = []
    for option in sorted(product.hotel_options, key=lambda o: HOTEL_PROVIDERS.index(o.provider)):
        if not ready_option(product, option, config, now):
            continue
        has_offer = (
            (option.provider, option.url or "") in eligible_targets
            if eligible_targets is not None
            else bool(await matching_offer(session, product, option, settings, now))
        )
        if not has_offer and not config.direct_hotel_links_enabled:
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
                "mode": "affiliate" if has_offer else "direct",
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
