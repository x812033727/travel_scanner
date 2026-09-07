from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import fakeredis.aioredis
import httpx
import pytest
from pydantic import ValidationError

from app.affiliates.service import TravelpayoutsLinkClient
from app.config import Settings
from app.i18n import ERROR_DETAILS, LOCALES
from app.models import (
    TravelServiceBrand,
    TravelServiceOffer,
    TravelServiceProduct,
    TripPlan,
    TripPlanItem,
)
from app.problems import AppError
from app.travel_services.imports import parse_csv
from app.travel_services.jobs import parse_airalo
from app.travel_services.registry import affiliate_target, brand_target
from app.travel_services.router import validate_schedule
from app.travel_services.schemas import (
    CatalogConfig,
    Facts,
    ProductInput,
    SelectInput,
    safe_url,
    untracked_url,
)
from app.travel_services.service import (
    enabled,
    fresh_price,
    public_product,
    rank_products,
    ready_offer,
    require_product_review,
    trip_destinations,
)

NOW = datetime(2026, 9, 7, tzinfo=UTC)


def product(kind="hotel", city="tokyo", **facts):
    return TravelServiceProduct(
        id=uuid4(),
        source_key=uuid4().hex,
        kind=kind,
        destination_id=city,
        title="Official stay",
        source_url="https://hotel.example.com/location",
        status="approved",
        version=1,
        verified_at=NOW,
        names_json={},
        facts=Facts(latitude=35.6812, longitude=139.7671, **facts).model_dump(mode="json"),
    )


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com",
        "https://127.0.0.1/a",
        "https://[::1]",
        "https://localhost",
        "https://a.local",
        "https://u:p@example.com",
        "https://example.com:8443/a",
        "https://example.com\\@evil.com",
        "https://example.com/\n",
        "javascript:alert(1)",
    ],
)
def test_url_rejects_unsafe_targets(url):
    with pytest.raises(ValueError):
        safe_url(url)


def test_url_canonicalization_preserves_product_identity():
    assert (
        safe_url("https://WWW.KLOOK.COM/activity/123?lang=ja#top")
        == "https://www.klook.com/activity/123?lang=ja"
    )
    assert brand_target("klook", "https://www.klook.com/activity/123/")
    with pytest.raises(ValueError):
        brand_target("klook", "https://klook.com.evil.com/activity/123/")
    with pytest.raises(ValueError):
        brand_target("kkday", "https://klook.com/activity/123/")
    with pytest.raises(ValueError):
        untracked_url("https://www.klook.com/a?marker=123")
    with pytest.raises(ValueError):
        affiliate_target("https://evil.com/r")


@pytest.mark.parametrize(
    "facts",
    [
        {"latitude": float("nan"), "longitude": 1},
        {"latitude": 91, "longitude": 1},
        {"latitude": 1, "longitude": 181},
        {"latitude": 1},
        {"languages": ["fr"]},
        {"country_codes": ["Japan"]},
        {"reference_price": -1},
    ],
)
def test_strict_facts_reject_invalid_values(facts):
    with pytest.raises(ValidationError):
        Facts.model_validate(facts)


def test_exact_hotel_identity_and_evidence_are_required():
    data = ProductInput(
        source_key="hotel-1",
        title="Hotel",
        kind="hotel",
        destination_id="tokyo",
        source_url="https://hotel.example.com",
        facts=Facts(latitude=35.681, longitude=139.767, area_code="tokyo-station"),
    )
    with pytest.raises(AppError):
        require_product_review(data)
    data.facts.google_place_id = "ChIJVerified"
    data.facts.map_verified = True
    data.facts.coordinate_source_url = "https://hotel.example.com/location"
    # Use a real area code from the existing catalog instead of introducing a parallel area list.
    from app.hotspots.areas import city_areas

    data.facts.area_code = next(a.code for a in city_areas("NRT") if a.code == "marunouchi")
    require_product_review(data)
    data.destination_id = "seoul"
    with pytest.raises(AppError):
        require_product_review(data)


def test_unpriced_hotel_never_becomes_free_or_a_current_quote():
    row = product(reference_price=100, currency="USD", price_checked_at=NOW)
    result = public_product(row, "ja", NOW)
    assert result["facts"]["reference_price"] is None
    assert result["facts"]["price_checked_at"] is None
    assert "price_snapshot" not in result
    assert result["title"] == row.title


@pytest.mark.parametrize("hours,expected", [(0, True), (48, True), (49, False), (-1, False)])
def test_reference_price_expires(hours, expected):
    assert (
        fresh_price(
            Facts(reference_price=1, currency="USD", price_checked_at=NOW - timedelta(hours=hours)),
            NOW,
        )
        is expected
    )


def test_feature_switches_fail_closed():
    assert not enabled(CatalogConfig(), "tokyo", "hotel", public=True)
    config = CatalogConfig(enabled_kinds=["hotel"], enabled_destinations=["tokyo"])
    assert enabled(config, "tokyo", "hotel")
    assert not enabled(config, "tokyo", "hotel", public=True)
    assert not enabled(config, "kyoto", "hotel")
    assert not enabled(config, "tokyo", "tour")


@pytest.mark.parametrize(
    "change",
    [
        "product_pending",
        "offer_pending",
        "brand_pending",
        "disabled",
        "other_project",
        "expired",
        "unverified",
        "no_token",
    ],
)
def test_public_offer_gates(change):
    row = product()
    brand = TravelServiceBrand(
        id=uuid4(),
        project_id="123",
        code="booking",
        enabled=True,
        approval="approved",
        verified_at=NOW,
    )
    offer = TravelServiceOffer(
        id=uuid4(),
        product_id=row.id,
        brand_id=brand.id,
        target_url="https://www.booking.com/hotel/jp/test.html",
        status="approved",
        verified_at=NOW,
        static_url=None,
        expires_at=None,
    )
    settings = Settings(
        travelpayouts_enabled=True,
        travelpayouts_api_token="test",
        travelpayouts_project_id="123",
        travelpayouts_marker="456",
    )
    assert ready_offer(offer, brand, row, settings, NOW)
    if change == "product_pending":
        row.status = "pending"
    if change == "offer_pending":
        offer.status = "pending"
    if change == "brand_pending":
        brand.approval = "pending"
    if change == "disabled":
        brand.enabled = False
    if change == "other_project":
        brand.project_id = "999"
    if change == "expired":
        offer.expires_at = NOW - timedelta(seconds=1)
    if change == "unverified":
        offer.verified_at = NOW - timedelta(days=31)
    if change == "no_token":
        settings.travelpayouts_api_token = None
    assert not ready_offer(offer, brand, row, settings, NOW)


def test_distance_ranking_and_city_isolation_ignore_commission():
    close, far, other = [
        public_product(product(city=city), "en", NOW) for city in ("tokyo", "tokyo", "kyoto")
    ]
    close["facts"]["latitude"], far["facts"]["latitude"] = 35.682, 35.75
    close["commission"], far["commission"] = 0, 100
    result = rank_products([far, other, close], city="tokyo")
    assert [p["id"] for p in result] == [close["id"], far["id"]]
    assert len(rank_products([far, close], city="tokyo", center=(35.6812, 139.7671), radius=1)) == 1


def test_hotel_rank_uses_weighted_trip_evidence():
    first, second = [public_product(product(), "en", NOW) for _ in range(2)]
    second["facts"]["latitude"] = 35.7
    row = TripPlanItem(
        id=uuid4(),
        item_type="activity",
        latitude=Decimal("35.7"),
        longitude=Decimal("139.7671"),
        title="Stop",
        data={},
        position=0,
        duration_minutes=120,
        is_skipped=False,
    )
    result = rank_products([first, second], city="tokyo", rows=[row])
    assert result[0]["id"] == second["id"]
    assert result[0]["reason"] == "trip_distance"


def test_transfer_direction_language_and_esim_coverage():
    transfer = public_product(
        product(kind="transfer", airport="NRT", direction="arrival", passengers=3), "en", NOW
    )
    assert rank_products([transfer], city="tokyo", airport="HND") == []
    assert rank_products([transfer], city="tokyo", direction="departure") == []
    assert rank_products([transfer], city="tokyo", passengers=4) == []
    tour = public_product(product(kind="tour", languages=["ja"]), "en", NOW)
    assert rank_products([tour], city="tokyo", language="zh-TW") == []
    esim = public_product(product(kind="esim", country_codes=["JP"], validity_days=7), "en", NOW)
    assert rank_products([esim], city="kyoto", countries=["JP"], days=7)
    assert rank_products([esim], city="tokyo", countries=["JP", "KR"]) == []
    assert rank_products([esim], city="tokyo", countries=["JP"], days=8) == []


def test_schedule_conflicts_preserve_existing_locked_items():
    trip = TripPlan(
        id=uuid4(), timezone="Asia/Tokyo", start_date=date(2026, 9, 10), end_date=date(2026, 9, 12)
    )
    payload = SelectInput(
        product_id=uuid4(),
        version=1,
        day_date="2026-09-10",
        start_time="2026-09-10T09:00:00+09:00",
        end_time="2026-09-10T10:00:00+09:00",
    )
    row = TripPlanItem(
        id=uuid4(),
        day_date=date(2026, 9, 10),
        start_time=payload.start_time,
        end_time=payload.end_time,
        locked=True,
        is_skipped=False,
    )
    with pytest.raises(AppError) as caught:
        validate_schedule(payload, trip, [row], Facts())
    assert caught.value.code == "service_time_conflict"
    assert row.locked and row.start_time == payload.start_time
    validate_schedule(payload, trip, [], Facts(duration_minutes=60))
    with pytest.raises(AppError):
        validate_schedule(payload, trip, [], Facts(duration_minutes=120))


def test_trip_destinations_do_not_equate_gateway_with_city():
    trip = TripPlan(destination_name="Kyoto", data={})
    assert trip_destinations(trip, []) == ["kyoto"]
    trip.destination_name = "Osaka / Kyoto"
    assert trip_destinations(trip, []) == ["osaka", "kyoto"]


def test_csv_preview_has_no_writes_and_flags_errors():
    csv = "source_key,kind,destination_id,title,source_url\nmanual:1,tour,tokyo,Official tour,https://www.klook.com/activity/1/\nmanual:2,flight,tokyo,Invalid,https://example.com\n"
    result = parse_csv(csv)
    assert result[0]["product"]["title"] == "Official tour"
    assert result[1]["error"] == "service_csv_invalid"
    assert "status" not in result[0]["product"]
    with pytest.raises(AppError):
        parse_csv("title,body\nA,B")


def test_airalo_feed_keeps_original_metadata_and_cannot_publish():
    body = (
        b'<rss xmlns:g="http://base.google.com/ns/1.0"><channel><item><g:id>j1</g:id>'
        b"<g:title>Moshi 1 GB 7 days</g:title>"
        b"<g:link>https://www.airalo.com/japan-esim/moshi-7days-1gb</g:link>"
        b"<g:price>4.00 USD</g:price></item></channel></rss>"
    )
    result = parse_airalo(body, NOW)
    assert len(result) == 1
    assert result[0].title == "Moshi 1 GB 7 days"
    assert result[0].facts.validity_days == 7
    assert result[0].facts.tethering is None
    assert not hasattr(result[0], "status")
    with pytest.raises(ValueError):
        parse_airalo(b"<!DOCTYPE rss><rss/>", NOW)


@pytest.mark.asyncio
async def test_link_cache_isolates_projects_brands_and_locale():
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(
            200, json={"result": {"links": [{"partner_url": "https://klook.tp.st/test"}]}}
        )

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(
        travelpayouts_api_token="test", travelpayouts_marker="456", travelpayouts_project_id="123"
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        client = TravelpayoutsLinkClient(redis, settings, http)
        for context in ("klook:en:1", "klook:en:1", "klook:ja:1", "kkday:ja:1"):
            await client.create(
                "https://www.klook.com/activity/1/", "svc_tour_tokyo", cache_context=context
            )
        assert len(calls) == 3
        settings.travelpayouts_project_id = "999"
        await client.create(
            "https://www.klook.com/activity/1/", "svc_tour_tokyo", cache_context="klook:en:1"
        )
        assert len(calls) == 4
    await redis.aclose()


def test_service_errors_have_five_language_parity():
    from app.travel_services.errors import SERVICE_ERRORS

    assert set(SERVICE_ERRORS) == set(LOCALES)
    for locale in LOCALES:
        assert set(SERVICE_ERRORS[locale]) == set(SERVICE_ERRORS["en"])
        for code in SERVICE_ERRORS[locale]:
            assert ERROR_DETAILS[locale][code] != code
