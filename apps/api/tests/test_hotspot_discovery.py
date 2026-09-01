import httpx
import pytest

from app.hotspots.cities import TARGET_PUBLIC_HOTSPOTS, DiscoveryCenter, HotspotCity
from app.hotspots.discovery import WikimediaDiscoveryClient, classify_types, haversine_km


def test_hotspot_city_targets_total_313() -> None:
    assert TARGET_PUBLIC_HOTSPOTS == 313


def test_haversine_distance_and_radius_boundary() -> None:
    assert haversine_km(25.033, 121.5654, 25.033, 121.5654) == 0
    assert 2.0 < haversine_km(25.033, 121.5654, 25.053, 121.5654) < 2.4


def test_type_allowlist_and_denylist_are_conservative() -> None:
    assert classify_types({"Q33506"}) == ("culture", "auto_approved", None)
    assert classify_types({"Q5", "Q33506"}) == (
        "culture",
        "pending",
        "denylisted_type",
    )
    assert classify_types({"Q999999"}) == ("culture", "pending", "unknown_type")


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
        return httpx.Response(
            200,
            json={
                "query": {
                    "pages": [
                        {
                            "title": "測試館",
                            "coordinates": [{"lat": 25.034, "lon": 121.5654}],
                            "pageprops": {"wikibase_item": "Q1"},
                        },
                        {
                            "title": "測試館別名",
                            "coordinates": [{"lat": 25.034, "lon": 121.5654}],
                            "pageprops": {"wikibase_item": "Q1"},
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
