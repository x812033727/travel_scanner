import math

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


def test_measured_non_attraction_types_are_rejected() -> None:
    # Measured 2026-09-12 against every approved attraction; see DENIED_TYPES.
    for noise_type in ("Q56351315", "Q55521176", "Q2175765", "Q687188"):
        assert classify_types({noise_type})[1] == "rejected", noise_type
    # Each of these also types an approved attraction, so a human still decides.
    for kept_type in ("Q5358913", "Q285783"):
        assert classify_types({kept_type}) == ("culture", "pending", "unknown_type"), kept_type


def test_types_that_also_describe_real_sights_reach_the_human_queue() -> None:
    # Released 2026-09-19: reading the pending rows found a gusuku ruin and a citadel
    # bastion typed as military bases, a gazetted monument typed as a primary school and
    # the Hiroshima hypocentre typed as a hospital. A rejection is a tombstone that
    # discovery never revisits, so these go to a human instead; see DENIED_TYPES.
    for released_type in ("Q245016", "Q9842", "Q16917"):
        assert released_type not in DENIED_TYPES
        assert classify_types({released_type}) == (
            "culture",
            "pending",
            "unknown_type",
        ), released_type
    # A denied type wins over an allowed one on the same item: that precedence is why a
    # released type had to leave the set rather than gain a heritage override.
    assert classify_types({"Q2175765", "Q33506"}) == ("culture", "rejected", "denylisted_type")
    # A released type beside an allowed one is decided by the allowed one, like any
    # other unknown type.
    assert classify_types({"Q16917", "Q33506"}) == ("culture", "auto_approved", None)


@pytest.mark.asyncio
async def test_pages_past_the_radius_are_dropped_and_denied_types_inside_it_stay_rejected() -> None:
    # The radius check used to turn a denied candidate back into pending, so a school just
    # past the edge of a city still reached the review queue. Now a page past the configured
    # radius is not a candidate at all, and a denied type inside it is rejected, not queued.
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "www.wikidata.org":
            return httpx.Response(
                200,
                json={
                    "entities": {
                        qid: {
                            "labels": {"zh-hant": {"value": label}},
                            "claims": {
                                "P31": [{"mainsnak": {"datavalue": {"value": {"id": type_id}}}}]
                            },
                            "sitelinks": {},
                        }
                        for qid, label, type_id in (
                            ("Q1", "近處博物館", "Q33506"),
                            ("Q2", "近處學校", "Q3914"),
                            ("Q3", "遠方博物館", "Q33506"),
                        )
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
                            {"pageid": 2, "pageprops": {"wikibase_item": "Q2"}},
                            {"pageid": 3, "pageprops": {"wikibase_item": "Q3"}},
                        ]
                    }
                },
            )
        # The real API never answers past gsradius; a page 18 km out is listed here on
        # purpose to show the client drops it even if the API returned it.
        return httpx.Response(
            200,
            json={
                "query": {
                    "geosearch": [
                        {"pageid": 1, "title": "近處館", "lat": 25.10, "lon": 121.5654},
                        {"pageid": 2, "title": "近處學校", "lat": 25.06, "lon": 121.5654},
                        {"pageid": 3, "title": "遠方館", "lat": 25.2, "lon": 121.5654},
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
        candidates = {c.qid: c for c in await client.discover_city(city)}
    assert set(candidates) == {"Q1", "Q2"}
    assert (candidates["Q1"].review_status, candidates["Q1"].review_reason) == (
        "auto_approved",
        None,
    )
    assert (candidates["Q2"].review_status, candidates["Q2"].review_reason) == (
        "rejected",
        "denylisted_type",
    )
    assert 7 < candidates["Q1"].distance_km < 8


def _flat_offset_km(center: DiscoveryCenter, latitude: float, longitude: float) -> float:
    """The lattice is laid out on a flat map around the centre; measure it the same way."""
    from app.hotspots.discovery import KM_PER_DEGREE

    dy = (latitude - center.latitude) * KM_PER_DEGREE
    dx = (longitude - center.longitude) * KM_PER_DEGREE * math.cos(math.radians(center.latitude))
    return math.hypot(dx, dy)


def test_a_radius_within_the_api_cap_is_one_call_and_a_larger_one_covers_the_disk() -> None:
    from app.hotspots.discovery import GEOSEARCH_MAX_RADIUS_KM, search_points

    small = DiscoveryCenter(25.033, 121.5654, 8)
    assert search_points(small) == [(25.033, 121.5654, 8)]

    tokyo = DiscoveryCenter(35.6595, 139.7005, 30)
    points = search_points(tokyo)
    assert 15 <= len(points) <= 25
    assert all(radius == GEOSEARCH_MAX_RADIUS_KM for _, _, radius in points)
    # No call sits farther out than it needs to (R + r), and every point of the configured
    # disk is within one call's reach: sample the disk on a fine grid.
    assert all(_flat_offset_km(tokyo, lat, lon) <= 40 + 0.01 for lat, lon, _ in points)
    for dx_km in range(-30, 31, 3):
        for dy_km in range(-30, 31, 3):
            if math.hypot(dx_km, dy_km) > 30:
                continue
            lat = tokyo.latitude + dy_km / 111.32
            lon = tokyo.longitude + dx_km / (111.32 * math.cos(math.radians(tokyo.latitude)))
            nearest = min(
                math.hypot(
                    (lat - plat) * 111.32,
                    (lon - plon) * 111.32 * math.cos(math.radians(tokyo.latitude)),
                )
                for plat, plon, _ in points
            )
            assert nearest <= GEOSEARCH_MAX_RADIUS_KM + 0.01, (dx_km, dy_km, nearest)


def _entity(label: str, type_id: str) -> dict[str, object]:
    return {
        "labels": {"zh-hant": {"value": label}},
        "claims": {"P31": [{"mainsnak": {"datavalue": {"value": {"id": type_id}}}}]},
        "sitelinks": {},
    }


@pytest.mark.asyncio
async def test_a_wide_city_reaches_pages_past_10_km_and_drops_pages_past_its_radius() -> None:
    # Kabuki-za sits 10.7 km from Shibuya and could never be discovered under the 10 km
    # clamp; a page 45 km out is beyond the 30 km radius and must not become a candidate,
    # even though a fringe call can see it.
    center = DiscoveryCenter(35.6595, 139.7005, 30)
    pages = {
        1: ("歌舞伎座", 35.6695, 139.7677, "Q1"),  # about 6 km east: inside
        2: ("遠方博物館", 35.6595 + 25 / 111.32, 139.7005, "Q2"),  # 25 km north: inside
        3: ("更遠博物館", 35.6595 + 45 / 111.32, 139.7005, "Q3"),  # 45 km north: outside
    }
    geosearch_calls: list[dict[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        params = dict(request.url.params)
        if request.url.host == "www.wikidata.org":
            wanted = params["ids"].split("|")
            return httpx.Response(
                200,
                json={
                    "entities": {
                        qid: _entity(label, "Q33506")
                        for _pid, (label, _lat, _lon, qid) in pages.items()
                        if qid in wanted
                    }
                },
            )
        if "pageids" in params:
            ids = [int(value) for value in params["pageids"].split("|")]
            return httpx.Response(
                200,
                json={
                    "query": {
                        "pages": [
                            {"pageid": pid, "pageprops": {"wikibase_item": pages[pid][3]}}
                            for pid in ids
                        ]
                    }
                },
            )
        geosearch_calls.append(params)
        lat, lon = (float(value) for value in params["gscoord"].split("|"))
        radius_km = int(params["gsradius"]) / 1000
        # Every page within this call's circle, like the real API (nearest first).
        hits = sorted(
            (
                (haversine_km(lat, lon, plat, plon), pid, title, plat, plon)
                for pid, (title, plat, plon, _qid) in pages.items()
                if haversine_km(lat, lon, plat, plon) <= radius_km
            )
        )
        return httpx.Response(
            200,
            json={
                "query": {
                    "geosearch": [
                        {"pageid": pid, "title": title, "lat": plat, "lon": plon}
                        for _d, pid, title, plat, plon in hits
                    ]
                }
            },
        )

    city = HotspotCity("TYO", "東京", "JP", "日本", "ja.wikipedia.org", 10, (center,))
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http_client:
        client = WikimediaDiscoveryClient("test", 1, http_client)
        candidates = await client.discover_city(city, 100)
        by_qid = {candidate.qid: candidate for candidate in candidates}

    assert len(geosearch_calls) > 1
    assert all(call["gsradius"] == "10000" and call["gslimit"] == "500" for call in geosearch_calls)
    assert set(by_qid) == {"Q1", "Q2"}
    assert by_qid["Q1"].review_status == "auto_approved"
    assert 10 < by_qid["Q1"].distance_km < 12 or by_qid["Q1"].distance_km < 10
    assert 24 < by_qid["Q2"].distance_km < 26
    # Nearest first, so a per-run limit keeps the closest of what is new.
    assert [candidate.qid for candidate in candidates] == ["Q1", "Q2"]

    # Items the catalogue already holds are left out before the limit is applied.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http_client:
        client = WikimediaDiscoveryClient("test", 1, http_client)
        remaining = await client.discover_city(city, 1, skip={"Q1"})
    assert [candidate.qid for candidate in remaining] == ["Q2"]
