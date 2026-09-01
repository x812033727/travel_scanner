from datetime import UTC, datetime, timedelta
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import fakeredis.aioredis
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.hotspots.places import (
    automatic_refresh_allowed,
    canonical_official_website,
    choose_place_candidate,
    enrich_hotspot_place,
    place_detail_payload,
    purge_expired_place_content,
)
from app.models import HotspotPlaceProfile, TravelHotspot
from app.places.google import GoogleTravelService
from app.problems import AppError
from app.providers.usage_meter import record_google_maps_request


def _hotspot(*, latitude: Decimal | None = Decimal("34.395483")) -> TravelHotspot:
    return TravelHotspot(
        id=uuid4(),
        slug="atomic-bomb-dome",
        name="原子彈爆炸圓頂屋",
        city_code="HIJ",
        destination_id="hiroshima",
        city_name="廣島",
        country_code="JP",
        country_name="日本",
        category="culture",
        search_text="原子彈爆炸圓頂屋 原爆ドーム",
        latitude=latitude,
        longitude=Decimal("132.453592") if latitude is not None else None,
        plus_code_global="8Q6J9FW3+5C" if latitude is not None else None,
        coordinate_source_type="wikidata" if latitude is not None else None,
        coordinate_source_url=(
            "https://www.wikidata.org/wiki/Q346357" if latitude is not None else None
        ),
        metadata_json={
            "local_name": "原爆ドーム",
            "aliases": ["Atomic Bomb Dome"],
            "coordinate_source": "wikidata",
        },
        source_urls=[],
        is_active=True,
        review_status="approved",
    )


def test_candidate_match_auto_approves_exact_nearby_place() -> None:
    match = choose_place_candidate(
        _hotspot(),
        [
            {
                "place_id": "correct",
                "name": "原爆ドーム",
                "address": "日本廣島縣廣島市",
                "latitude": 34.395483,
                "longitude": 132.453592,
            },
            {
                "place_id": "wrong",
                "name": "原爆ドーム",
                "address": "日本東京都",
                "latitude": 35.67,
                "longitude": 139.76,
            },
        ],
    )
    assert match.candidate is not None
    assert match.candidate["place_id"] == "correct"
    assert match.auto_approved is True
    assert match.evidence["distance_km"] == 0


def test_candidate_without_coordinates_needs_exact_city_and_country() -> None:
    hotspot = _hotspot(latitude=None)
    match = choose_place_candidate(
        hotspot,
        [
            {
                "place_id": "correct",
                "name": "原爆ドーム",
                "address": "日本廣島縣廣島市",
                "latitude": 34.395483,
                "longitude": 132.453592,
            }
        ],
    )
    assert match.auto_approved is True


def test_candidate_country_code_handles_a_different_address_language() -> None:
    match = choose_place_candidate(
        _hotspot(),
        [{
            "place_id": "correct",
            "name": "原爆ドーム",
            "address": "1-10 Otemachi, Naka Ward, Hiroshima",
            "country_code": "JP",
            "latitude": 34.395483,
            "longitude": 132.453592,
        }],
    )
    assert match.auto_approved is True


def test_candidate_with_wrong_country_stays_pending() -> None:
    match = choose_place_candidate(
        _hotspot(),
        [{
            "place_id": "wrong-country",
            "name": "原爆ドーム",
            "address": "Hiroshima memorial, California",
            "country_code": "US",
            "latitude": 34.395483,
            "longitude": 132.453592,
        }],
    )
    assert match.candidate is not None
    assert match.auto_approved is False
    assert match.evidence["country_match"] is False


def test_close_fuzzy_name_with_city_country_and_distance_auto_approves() -> None:
    match = choose_place_candidate(
        _hotspot(),
        [{
            "place_id": "fuzzy",
            "name": "原子彈爆炸圓頂",
            "address": "日本廣島縣廣島市",
            "country_code": "JP",
            "latitude": 34.3955,
            "longitude": 132.4536,
        }],
    )
    assert match.evidence["name_similarity"] >= 0.9
    assert match.auto_approved is True


def test_official_website_rejects_booking_and_internal_hosts() -> None:
    assert canonical_official_website("https://www.city.hiroshima.lg.jp/path") == (
        "https://www.city.hiroshima.lg.jp/path"
    )
    with pytest.raises(AppError, match="官方網站"):
        canonical_official_website("https://booking.com/attraction")
    with pytest.raises(AppError, match="官方網站"):
        canonical_official_website("https://localhost/private")


@pytest.mark.asyncio
async def test_enrichment_persists_normalized_cache_and_expiry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = AsyncMock(spec=AsyncSession)
    session.scalar.return_value = None
    session.add = MagicMock()
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    hotspot = _hotspot()

    monkeypatch.setattr(
        GoogleTravelService,
        "search_place_candidates",
        AsyncMock(
            return_value=[
                {
                    "place_id": "ChIJ-dome",
                    "name": "原爆ドーム",
                    "address": "日本廣島縣廣島市",
                    "latitude": 34.395483,
                    "longitude": 132.453592,
                }
            ]
        ),
    )
    monkeypatch.setattr(
        GoogleTravelService,
        "place_details",
        AsyncMock(
            return_value={
                "place_id": "ChIJ-dome",
                "name": "原爆ドーム",
                "address": "日本廣島縣廣島市",
                "latitude": 34.395483,
                "longitude": 132.453592,
                "google_maps_url": "https://www.google.com/maps/place/example",
                "opening_hours_structured": {
                    "weekday_descriptions": ["星期一: 24 小時營業"],
                    "periods": [{"open": {"day": 0, "hour": 0, "minute": 0}}],
                },
                "plus_code": {"global_code": "8Q6J9FW3+5C", "compound_code": "9FW3+5C 廣島"},
                "website_url": "https://www.city.hiroshima.lg.jp/atomicbomb-peace/",
                "attributions": [],
                "data_locale": "zh-TW",
            }
        ),
    )
    now = datetime(2026, 9, 1, tzinfo=UTC)
    outcome, calls = await enrich_hotspot_place(
        session,
        redis,
        Settings(google_maps_api_key="key"),
        hotspot,
        now=now,
    )
    profile = session.add.call_args_list[0].args[0]
    assert isinstance(profile, HotspotPlaceProfile)
    assert outcome == "published"
    assert calls == 2
    assert hotspot.google_place_id == "ChIJ-dome"
    assert hotspot.map_match_status == "verified"
    assert hotspot.map_verified_at == now
    assert profile.match_status == "auto_approved"
    assert profile.plus_code_compound == "9FW3+5C 廣島"
    assert profile.website_review_status == "auto_approved"
    assert profile.provider_refresh_after == now + timedelta(days=21)
    assert profile.provider_expires_at == now + timedelta(days=30)


@pytest.mark.asyncio
async def test_failed_refresh_preserves_still_valid_cache(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = datetime(2026, 9, 1, tzinfo=UTC)
    hotspot = _hotspot()
    hotspot.google_place_id = "ChIJ-dome"
    profile = HotspotPlaceProfile(
        hotspot_id=hotspot.id,
        place_id_source="legacy",
        match_status="approved",
        formatted_address="日本廣島縣廣島市",
        provider_fetched_at=now - timedelta(days=21),
        provider_refresh_after=now,
        provider_expires_at=now + timedelta(days=9),
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.return_value = profile
    session.add = MagicMock()
    monkeypatch.setattr(GoogleTravelService, "place_details", AsyncMock(return_value={}))

    outcome, calls = await enrich_hotspot_place(
        session,
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(google_maps_api_key="key"),
        hotspot,
        now=now,
    )

    assert (outcome, calls) == ("failed", 1)
    assert profile.match_status == "approved"
    assert profile.formatted_address == "日本廣島縣廣島市"
    assert profile.provider_expires_at == now + timedelta(days=9)


@pytest.mark.asyncio
async def test_google_refresh_does_not_override_rejected_website(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = datetime(2026, 9, 1, tzinfo=UTC)
    hotspot = _hotspot()
    hotspot.google_place_id = "ChIJ-dome"
    profile = HotspotPlaceProfile(
        hotspot_id=hotspot.id,
        place_id_source="legacy",
        match_status="approved",
        website_review_status="rejected",
    )
    session = AsyncMock(spec=AsyncSession)
    session.scalar.return_value = profile
    session.add = MagicMock()
    monkeypatch.setattr(
        GoogleTravelService,
        "place_details",
        AsyncMock(return_value={
            "address": "日本廣島縣廣島市",
            "latitude": 34.395483,
            "longitude": 132.453592,
            "website_url": "https://www.city.hiroshima.lg.jp/atomicbomb-peace/",
        }),
    )

    outcome, _calls = await enrich_hotspot_place(
        session,
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(google_maps_api_key="key"),
        hotspot,
        now=now,
    )

    assert outcome == "published"
    assert profile.provider_website_uri == (
        "https://www.city.hiroshima.lg.jp/atomicbomb-peace/"
    )
    assert profile.website_review_status == "rejected"


@pytest.mark.asyncio
async def test_automatic_refresh_pauses_at_relevant_google_sku_threshold() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(
        google_maps_essentials_free_limit=10,
        google_maps_pro_free_limit=10,
        google_maps_enterprise_free_limit=10,
    )
    for _ in range(9):
        await record_google_maps_request(redis, "places_text_search_locate")
    assert await automatic_refresh_allowed(redis, settings) is False


@pytest.mark.asyncio
async def test_expired_provider_content_is_purged_but_manual_identity_survives() -> None:
    now = datetime(2026, 9, 1, tzinfo=UTC)
    profile = HotspotPlaceProfile(
        hotspot_id=uuid4(),
        place_id_source="manual",
        match_status="approved",
        manual_official_website_url="https://www.city.hiroshima.lg.jp/",
        website_review_status="approved",
        google_maps_uri="https://maps.google.com/expired",
        formatted_address="expired address",
        plus_code_compound="9FW3+5C 廣島",
        opening_hours_json={"weekday_descriptions": ["24 小時營業"]},
        provider_website_uri="https://provider.example/",
        provider_attributions_json=[{"provider": "Example"}],
        provider_expires_at=now,
    )
    session = AsyncMock(spec=AsyncSession)
    result = MagicMock()
    result.all.return_value = [profile]
    session.scalars.return_value = result

    assert await purge_expired_place_content(session, now=now) == 1
    assert profile.google_maps_uri is None
    assert profile.formatted_address is None
    assert profile.opening_hours_json == {}
    assert profile.provider_attributions_json == []
    assert profile.manual_official_website_url == "https://www.city.hiroshima.lg.jp/"
    assert profile.website_review_status == "approved"
    session.commit.assert_awaited_once()


def test_public_payload_hides_expired_google_fields_but_keeps_curated_coordinates() -> None:
    hotspot = _hotspot()
    hotspot.google_place_id = "ChIJ-dome"
    hotspot.map_match_status = "verified"
    now = datetime(2026, 9, 1, tzinfo=UTC)
    profile = HotspotPlaceProfile(
        hotspot_id=hotspot.id,
        match_status="approved",
        place_id_source="legacy",
        formatted_address="日本廣島縣廣島市",
        plus_code_compound="9FW3+5C 廣島",
        opening_hours_json={"weekday_descriptions": ["24 小時營業"]},
        provider_expires_at=now - timedelta(seconds=1),
        provider_fetched_at=now - timedelta(days=30),
    )
    payload = place_detail_payload(hotspot, profile, configured=True, now=now)
    assert payload["status"] == "stale"
    assert payload["address"] is None
    assert payload["opening_hours"] == {}
    assert payload["coordinates"] == {
        "latitude": 34.395483,
        "longitude": 132.453592,
        "source": "wikidata",
    }
    assert payload["field_sources"]["address"] is None
    assert payload["field_sources"]["coordinates"] == "wikidata"
    assert payload["plus_code"] == {
        "global_code": "8Q6J9FW3+5C",
        "compound_code": None,
    }
    assert "query_place_id=ChIJ-dome" in payload["google_maps_url"]


def test_public_payload_is_explicitly_unavailable_without_a_provider_key() -> None:
    payload = place_detail_payload(_hotspot(), None, configured=False)
    assert payload["status"] == "unavailable"
    assert payload["has_details"] is False
    assert payload["address"] is None
    assert payload["google_maps_url"] is None
    assert payload["map_links"] == []


def test_public_korean_place_payload_exposes_only_exact_naver_link() -> None:
    hotspot = _hotspot()
    hotspot.country_code = "KR"
    hotspot.google_place_id = "ChIJ-google-is-not-public"
    hotspot.naver_map_url = "https://map.naver.com/p/entry/place/13543735"
    hotspot.map_match_status = "verified"

    payload = place_detail_payload(hotspot, None, configured=False)

    assert payload["google_maps_url"] is None
    assert [link["provider"] for link in payload["map_links"]] == ["naver"]
    assert payload["map_links"][0]["url"] == hotspot.naver_map_url
