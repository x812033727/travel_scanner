import httpx
import pytest

from app.hotspots.cities import TARGET_PUBLIC_HOTSPOTS, DiscoveryCenter, HotspotCity
from app.hotspots.discovery import (
    ALLOWED_TYPES,
    DENIED_TYPES,
    REVIEW_ONLY_TYPES,
    WikimediaDiscoveryClient,
    classify_types,
    haversine_km,
)


def test_hotspot_city_targets_total_529() -> None:
    assert TARGET_PUBLIC_HOTSPOTS == 649


def test_haversine_distance_and_radius_boundary() -> None:
    assert haversine_km(25.033, 121.5654, 25.033, 121.5654) == 0
    assert 2.0 < haversine_km(25.033, 121.5654, 25.053, 121.5654) < 2.4


def test_type_allowlist_and_denylist_are_conservative() -> None:
    assert classify_types({"Q33506"}) == ("culture", "auto_approved", None)
    assert classify_types({"Q5", "Q33506"}) == (
        "culture",
        "rejected",
        "denylisted_type",
    )
    assert classify_types({"Q999999"}) == ("culture", "pending", "unknown_type")


def test_commuter_infrastructure_is_rejected_rather_than_queued() -> None:
    # Wikidata models a station several ways and only one of them used to be denied,
    # so a single line's stops filled the review queue.
    for station_type in ("Q55488", "Q928830", "Q22808403", "Q124416148"):
        assert classify_types({station_type})[1] == "rejected", station_type
    for noise_type in ("Q3918", "Q14350", "Q11032", "Q644371", "Q1549591", "Q3024240"):
        assert classify_types({noise_type})[1] == "rejected", noise_type


def test_museum_and_temple_subtypes_auto_approve_into_the_right_category() -> None:
    # Wikidata often types an entry with only the subtype, never Q33506/Q44539 itself,
    # so 清水寺-sized places were landing in the review queue as unknown_type.
    for museum_subtype in ("Q17431399", "Q16735822", "Q1865249"):
        assert classify_types({museum_subtype}) == ("culture", "auto_approved", None)
    for temple_tradition in ("Q7245816", "Q618618", "Q842400"):
        assert classify_types({temple_tradition}) == ("culture", "auto_approved", None)
    for market_type in ("Q132510", "Q1962840"):
        assert classify_types({market_type}) == ("food", "auto_approved", None)


def test_chinese_temple_stays_with_a_human() -> None:
    # Q2680845 was measured before the temple traditions above were admitted:
    # allowing it would auto-publish 94 rows in Taipei and 79 in Tainan alone,
    # mostly neighbourhood shrines. It must stay pending, and never be denied
    # outright either — some of those rows are real destinations.
    assert classify_types({"Q2680845"}) == ("culture", "pending", "unknown_type")


def test_streets_and_districts_still_reach_a_human() -> None:
    # 彌敦道, 通菜街 and 旺角 are streets and neighbourhoods that are also real
    # destinations, so their types must never be denied outright.
    for ambiguous_type in ("Q79007", "Q83620", "Q1304276", "Q123705", "Q159334"):
        assert classify_types({ambiguous_type}) == (
            "culture",
            "pending",
            "unknown_type",
        ), ambiguous_type


def test_denylist_never_shadows_an_allowed_type() -> None:
    assert not (set(ALLOWED_TYPES) & DENIED_TYPES)


@pytest.mark.asyncio
async def test_geosearch_deduplicates_qids_and_uses_chinese_label() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "www.wikidata.org":
            return httpx.Response(
                200,
                json={
                    "entities": {
                        "Q1": {
                            "labels": {"zh-hant": {"value": "測試博物館"}},
                            "claims": {
                                "P31": [{"mainsnak": {"datavalue": {"value": {"id": "Q33506"}}}}]
                            },
                            "sitelinks": {"enwiki": {"title": "Test Museum"}},
                        }
                    }
                },
            )
        if "pageids" in request.url.params:
            return httpx.Response(
                200,
                json={
                    "query": {
                        "pages": [
                            {"pageid": 1, "pageprops": {"wikibase_item": "Q1"}},
                            {"pageid": 2, "pageprops": {"wikibase_item": "Q1"}},
                        ]
                    }
                },
            )
        return httpx.Response(
            200,
            json={
                "query": {
                    "geosearch": [
                        {
                            "pageid": 1,
                            "title": "測試館",
                            "lat": 25.034,
                            "lon": 121.5654,
                        },
                        {
                            "pageid": 2,
                            "title": "測試館別名",
                            "lat": 25.034,
                            "lon": 121.5654,
                        },
                    ]
                }
            },
        )

    city = HotspotCity(
        "TST",
        "測試市",
        "TW",
        "台灣",
        "zh.wikipedia.org",
        10,
        (DiscoveryCenter(25.033, 121.5654, 10),),
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http_client:
        client = WikimediaDiscoveryClient("test", 1, http_client)
        candidates = await client.discover_city(city)
    assert len(candidates) == 1
    assert candidates[0].name == "測試博物館"
    assert candidates[0].review_status == "auto_approved"
    assert candidates[0].pageview_pages[-1] == ("en.wikipedia.org", "Test Museum")


def test_botanical_gardens_publish_and_the_measured_floods_stay_with_a_human() -> None:
    """Measured 2026-09-06 across all 68 discovery centres; see the comments in discovery.py.

    A whitelisted type is published by the confirmed lane of import-hotspot-candidates
    without anyone looking, so the whitelist is a claim about volume, not about whether
    the places are worth visiting. Botanical gardens add tens; the five below add
    hundreds or thousands in a single city.
    """
    assert classify_types({"Q167346"}) == ("nature", "auto_approved", None)
    for flooding_type in REVIEW_ONLY_TYPES:
        assert flooding_type not in ALLOWED_TYPES
        assert flooding_type not in DENIED_TYPES
        assert classify_types({flooding_type}) == ("culture", "pending", "unknown_type")
