from __future__ import annotations

import asyncio
import math
from collections.abc import Collection
from dataclasses import dataclass
from typing import Any, cast
from urllib.parse import quote

import httpx

from app.hotspots.cities import DiscoveryCenter, HotspotCity

ALLOWED_TYPES = {
    "Q33506": "culture",  # museum
    # Museum subtypes that Wikidata often uses INSTEAD of Q33506, not alongside it.
    # Each was flood-measured across all 33 cities before being admitted (2026-09):
    # the whole batch adds tens of rows, not hundreds.
    "Q17431399": "culture",  # national museum
    "Q16735822": "culture",  # history museum
    "Q1865249": "culture",  # literary museum
    "Q16970": "culture",  # church
    "Q44539": "culture",  # temple
    # Named temple traditions modelled without Q44539. Q2680845 (Chinese temple) is
    # deliberately absent: measured at 94 auto-publishes in Taipei and 79 in Tainan,
    # mostly neighbourhood shrines, so it stays with human review.
    "Q7245816": "culture",  # temple of Mazu
    "Q618618": "culture",  # temple of Confucius
    "Q842400": "culture",  # Guandi temple
    "Q23413": "culture",  # castle
    "Q16560": "culture",  # palace
    "Q839954": "culture",  # archaeological site
    "Q15243209": "culture",  # historic district
    "Q194195": "family",  # amusement park
    "Q12280": "viewpoint",  # bridge
    "Q11303": "viewpoint",  # skyscraper
    "Q174782": "viewpoint",  # square
    "Q570116": "nature",  # tourist garden
    # Measured 2026-09-06 with wikibase:around over all 68 discovery centres, counting
    # only items whose direct P31 is the type and is not already allowed — which is how
    # classify_types matches. Botanical garden adds 103 rows across 23 cities, worst
    # 19 in Osaka/Kyoto: tens per city, so the confirmed lane can publish it.
    "Q167346": "nature",  # botanical garden
    "Q22698": "nature",  # park
    "Q23397": "nature",  # lake
    "Q8502": "nature",  # mountain
    "Q35509": "nature",  # cave
    "Q46169": "nature",  # national park
    "Q40080": "beach",
    "Q161741": "culture",  # memorial
    "Q4989906": "culture",  # monument
    "Q24398318": "culture",  # religious building
    "Q43501": "family",  # zoo
    "Q2281788": "family",  # aquarium
    "Q2416723": "family",  # theme park
    "Q11315": "shopping",  # shopping mall
    "Q330284": "food",  # marketplace
    "Q132510": "food",  # market
    "Q1962840": "food",  # night market
}
# A denied type is never a place a traveller visits, so a candidate carrying one is
# rejected outright instead of queued for a human. Everything here was observed in the
# 2026-09 discovery queue and checked against the attractions we kept, so nothing in the
# list can also describe a real destination. Deliberately absent: street, thoroughfare
# and arterial road (彌敦道, 通菜街, 拉差丹儂大道 are all streets), secondary school
# (培材學堂), planning area (武吉知馬), building and hall — those stay "unknown" so a
# human still decides.
DENIED_TYPES = {
    "Q5",  # human
    "Q43229",  # organization
    "Q728937",  # railway line
    "Q783794",  # company
    "Q56061",  # administrative territorial entity
    # Rail. Wikidata models a station a dozen ways, and a commuter stop matched by
    # only one of them still floods the queue.
    "Q55488",  # railway station
    "Q22808403",  # underground station
    "Q928830",  # metro station
    "Q4312270",  # railway station above ground
    "Q1147171",  # interchange station
    "Q124416148",  # underground metro station
    "Q2142091",  # over-track railway station
    "Q11670533",  # elevated station
    "Q55491",  # underground railway station
    "Q55485",  # dead-end railway station
    "Q11606300",  # last station
    "Q332496",  # overtaking station
    "Q20202072",  # terminus
    "Q85907346",  # rail company (Japan)
    "Q10438042",  # bus company
    # Air
    "Q1248784",  # airport
    "Q644371",  # international airport
    "Q94993988",  # commercial traffic aerodrome
    # Education
    "Q3914",  # school
    "Q9826",  # high school
    "Q3918",  # university
    "Q6313528",  # junior college
    "Q12592372",  # high school in South Korea
    "Q1080794",  # public school
    "Q3660535",  # women's college
    # Businesses and media
    "Q4830453",  # business
    "Q891723",  # public company
    "Q1480166",  # kabushiki gaisha
    "Q14350",  # radio station
    "Q1616075",  # television station
    "Q15265344",  # broadcaster
    "Q11032",  # newspaper
    "Q11691",  # stock exchange
    # Places too large to be an attraction, and states that no longer exist
    "Q515",  # city
    "Q1549591",  # big city
    "Q174844",  # megacity
    "Q494721",  # city of Japan
    "Q1749269",  # city designated by government ordinance
    "Q65589340",  # prefectural capital of Japan
    "Q2264924",  # port city
    "Q11422368",  # city for international conferences and tourism
    "Q6644510",  # urban district of Vietnam
    "Q13025342",  # thesaban mueang
    "Q7635776",  # Sukhaphiban
    "Q50198",  # province of Thailand
    "Q3624078",  # sovereign state
    "Q6256",  # country
    "Q3024240",  # historical country
    # Measured 2026-09-12 against all 1,247 approved attractions that carry a QID (their
    # direct P31 read from Wikidata): none has any of the types below, while together
    # they held about 50 rows of the pending queue. Deliberately absent although they
    # flood too: elementary school in Japan (Q5358913, 袋町小学校平和資料館 is approved)
    # and intersection (Q285783, the Shibuya scramble and 銀座四丁目 are approved).
    #
    # That measurement only asked whether an APPROVED row carries the type. Reading the
    # 17 pending rows that carried one of the seven (2026-09-12) against their Wikipedia
    # extracts found four genuine sights, so three of the seven were released back to the
    # human queue on 2026-09-19 (the same treatment as Q5358913 and Q285783):
    #   Q245016 military base    2 of 3 pending rows genuine (喜屋武城, a Ryukyu gusuku
    #                            ruin; 鎮平台, the Trấn Bình đài bastion of the Huế citadel)
    #   Q9842   primary school   1 of 2 (原花園尋常小學校本館, a gazetted Tainan monument)
    #   Q16917  hospital         1 of 4 (島醫院, the Hiroshima hypocentre)
    # Wikidata's P31 is correct on all four -- a gusuku is a fortification, an old school
    # building is a school -- and none carries a heritage designation to key on, so the
    # type alone cannot reject them. The four below stay denied: tram stop and Japanese
    # high school were read at zero genuine rows across eight, and the last two held no
    # pending rows at all, so for them the approved-rows measurement is still the only
    # evidence; re-read the pending queue before trusting it further. The entries above
    # this block were measured the other way round as well -- observed as the bulk of
    # the 2026-09 queue (141 of 172 rows) and checked against the attractions we kept --
    # and describe things no traveller visits (a person, a company, a station, a city).
    "Q56351315",  # Japanese high school
    "Q55521176",  # lower secondary school in Japan
    "Q2175765",  # tram stop
    "Q687188",  # ward of Vietnam
}


@dataclass(frozen=True)
class DiscoveredHotspot:
    qid: str
    name: str
    city_code: str
    category: str
    latitude: float
    longitude: float
    distance_km: float
    wikipedia_project: str
    wikipedia_title: str
    pageview_pages: tuple[tuple[str, str], ...]
    review_status: str
    review_reason: str | None
    type_ids: tuple[str, ...]
    source_urls: tuple[str, ...]


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    value = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(value))


# What one MediaWiki ``list=geosearch`` call can answer (paraminfo read 2026-09-19): pages
# within at most 10 km of one point, at most 500 of them for a non-bot client, nearest first.
# A centre configured with a larger radius used to be clamped to this ring and to 100 pages,
# so Tokyo's search saw the 100 pages nearest Shibuya and Kabuki-za (10.7 km out) could never
# be discovered. The bound is now the configured radius itself: a city sees every page inside
# it, and the per-run candidate limit picks the nearest ones that are not already known.
GEOSEARCH_MAX_RADIUS_KM = 10
GEOSEARCH_PAGE_LIMIT = 500
KM_PER_DEGREE = 111.32


def search_points(center: DiscoveryCenter) -> list[tuple[float, float, int]]:
    """``(latitude, longitude, radius_km)`` of the calls that together cover ``center``.

    A radius within the API's cap is one call at the centre. A larger one is a hexagonal
    lattice of 10 km circles: with lattice points r*sqrt(3) apart every point of the plane
    lies within r of a lattice point, and keeping the lattice points up to R + r from the
    centre covers the whole disk of radius R. Tokyo's 30 km takes 19 calls, the 100 km
    centre about 150; pages beyond the configured radius are dropped by the caller.
    """
    r = GEOSEARCH_MAX_RADIUS_KM
    if center.radius_km <= r:
        return [(center.latitude, center.longitude, center.radius_km)]
    reach = center.radius_km + r
    spacing = r * math.sqrt(3)
    row_height = spacing * math.sqrt(3) / 2
    lon_scale = KM_PER_DEGREE * math.cos(math.radians(center.latitude))
    rows = math.ceil(reach / row_height)
    cols = math.ceil(reach / spacing) + 1
    points: list[tuple[float, float, int]] = []
    for row in range(-rows, rows + 1):
        y = row * row_height
        shift = spacing / 2 if row % 2 else 0.0
        for col in range(-cols, cols + 1):
            x = col * spacing + shift
            if math.hypot(x, y) > reach:
                continue
            points.append(
                (
                    round(center.latitude + y / KM_PER_DEGREE, 5),
                    round(center.longitude + x / lon_scale, 5),
                    r,
                )
            )
    return points


def distance_to_city_km(city: HotspotCity, latitude: float, longitude: float) -> float:
    return min(
        haversine_km(center.latitude, center.longitude, latitude, longitude)
        for center in city.centers
    )


def inside_city(city: HotspotCity, latitude: float, longitude: float) -> bool:
    """Within some centre's configured radius (a few metres of slack for rounded coordinates)."""
    return any(
        haversine_km(center.latitude, center.longitude, latitude, longitude)
        <= center.radius_km + 0.05
        for center in city.centers
    )


# Measured on 2026-09-06 and deliberately left out of ALLOWED_TYPES. The counts are the
# rows each type would ADD in one city: items whose direct P31 is that type and is not
# already an allowed type. import-hotspot-candidates publishes a whitelisted type through
# its confirmed lane without a human, so a type only goes in when that number is tens.
#
#   Q5393308 Buddhist temple  2,660 in Tokyo alone
#   Q845945  Shinto shrine    1,331 in Tokyo alone
#   Q427287  wat                824 in Bangkok alone
#   Q22746   urban park         571 across 19 cities, 202 in Hong Kong
#   Q207694  art museum         424 across 26 cities, 112 in Osaka/Kyoto
#
# They are not denied either: a Kyoto temple is exactly what a traveller comes for, so
# each still reaches the review queue as pending/unknown_type and a human decides.
REVIEW_ONLY_TYPES = {
    "Q5393308",  # Buddhist temple
    "Q845945",  # Shinto shrine
    "Q427287",  # wat
    "Q22746",  # urban park
    "Q207694",  # art museum
    "Q2680845",  # Chinese temple, measured in 2026-09 at 94 auto-publishes in Taipei
}


def classify_types(type_ids: set[str]) -> tuple[str, str, str | None]:
    if type_ids & DENIED_TYPES:
        # Rejected, not queued: a denied type is a decision the collector can make on
        # its own, and sending it for review buried the real candidates. In 2026-09 the
        # queue held 172 rows and 141 of them were this.
        return "culture", "rejected", "denylisted_type"
    categories = [category for qid, category in ALLOWED_TYPES.items() if qid in type_ids]
    if not categories:
        return "culture", "pending", "unknown_type"
    return categories[0], "auto_approved", None


class WikimediaDiscoveryClient:
    def __init__(
        self,
        user_agent: str,
        timeout_seconds: float,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._owned = client is None
        self._client = client or httpx.AsyncClient(timeout=timeout_seconds)
        self._headers = {"User-Agent": user_agent}

    async def close(self) -> None:
        if self._owned:
            await self._client.aclose()

    async def _get(self, url: str, params: dict[str, str]) -> dict[str, Any]:
        for attempt in range(3):
            try:
                response = await self._client.get(url, params=params, headers=self._headers)
                response.raise_for_status()
                return cast(dict[str, Any], response.json())
            except (httpx.HTTPError, ValueError):
                if attempt == 2:
                    raise
                await asyncio.sleep(2**attempt)
        raise AssertionError("unreachable")

    async def discover_city(
        self, city: HotspotCity, limit: int = 100, *, skip: Collection[str] = ()
    ) -> list[DiscoveredHotspot]:
        """Every Wikipedia page with a Wikidata item inside the city's configured radius,
        nearest first, minus ``skip`` (items the catalogue already holds), cut to ``limit``.

        ``skip`` is what lets a weekly pass advance: without it the same nearest ``limit``
        items came back every run once they were all in the catalogue.
        """
        pages_by_qid: dict[str, dict[str, Any]] = {}
        seen_pages: set[int] = set()
        api = f"https://{city.local_wikipedia}/w/api.php"
        for center in city.centers:
            for latitude, longitude, radius_km in search_points(center):
                payload = await self._get(
                    api,
                    {
                        "action": "query",
                        "format": "json",
                        "formatversion": "2",
                        "list": "geosearch",
                        "gscoord": f"{latitude}|{longitude}",
                        "gsradius": str(radius_km * 1000),
                        "gslimit": str(GEOSEARCH_PAGE_LIMIT),
                        "gsnamespace": "0",
                    },
                )
                nearby = [
                    page
                    for page in payload.get("query", {}).get("geosearch", [])
                    if page["pageid"] not in seen_pages
                    and inside_city(city, float(page["lat"]), float(page["lon"]))
                ]
                seen_pages.update(page["pageid"] for page in nearby)
                await self._collect_pages(api, city, nearby, pages_by_qid)
        skipped = set(skip)
        qids = [
            qid
            for qid in sorted(pages_by_qid, key=lambda item: pages_by_qid[item]["distance_km"])
            if qid not in skipped
        ][:limit]
        return await self._describe(city, qids, pages_by_qid)

    async def _collect_pages(
        self,
        api: str,
        city: HotspotCity,
        nearby: list[dict[str, Any]],
        pages_by_qid: dict[str, dict[str, Any]],
    ) -> None:
        for start in range(0, len(nearby), 50):
            batch = nearby[start : start + 50]
            details = await self._get(
                api,
                {
                    "action": "query",
                    "format": "json",
                    "formatversion": "2",
                    "pageids": "|".join(str(page["pageid"]) for page in batch),
                    "prop": "pageprops",
                },
            )
            qid_by_page_id = {
                page["pageid"]: (page.get("pageprops") or {}).get("wikibase_item")
                for page in details.get("query", {}).get("pages", [])
            }
            for page in batch:
                qid = qid_by_page_id.get(page["pageid"])
                if not qid:
                    continue
                pages_by_qid.setdefault(
                    qid,
                    {
                        "title": page["title"],
                        "latitude": page["lat"],
                        "longitude": page["lon"],
                        "distance_km": distance_to_city_km(
                            city, float(page["lat"]), float(page["lon"])
                        ),
                    },
                )

    async def _describe(
        self, city: HotspotCity, qids: list[str], pages_by_qid: dict[str, dict[str, Any]]
    ) -> list[DiscoveredHotspot]:
        entities: dict[str, Any] = {}
        for start in range(0, len(qids), 50):
            payload = await self._get(
                "https://www.wikidata.org/w/api.php",
                {
                    "action": "wbgetentities",
                    "format": "json",
                    "ids": "|".join(qids[start : start + 50]),
                    "props": "labels|claims|sitelinks",
                    "languages": "zh-hant|zh|ja|ko|th|vi|en",
                },
            )
            entities.update(payload.get("entities", {}))
        candidates: list[DiscoveredHotspot] = []
        for qid in qids:
            entity = entities.get(qid, {})
            page = pages_by_qid[qid]
            claims = entity.get("claims", {})
            type_ids = {
                claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id")
                for claim in claims.get("P31", [])
            }
            type_ids.discard(None)
            category, status, reason = classify_types(type_ids)
            distance = float(page["distance_km"])
            # Pages past the configured radius are dropped before they get here, so this
            # only catches rounding at the edge. A denied type stays rejected wherever it
            # sits; sending it back to review just because it is past the radius is the
            # flood the denylist exists to stop.
            if status != "rejected" and distance > max(center.radius_km for center in city.centers):
                status, reason = "pending", "outside_city_radius"
            labels = entity.get("labels", {})
            name = next(
                (
                    labels[key]["value"]
                    for key in ("zh-hant", "zh", "ja", "ko", "th", "vi", "en")
                    if key in labels
                ),
                page["title"],
            )
            sitelinks = entity.get("sitelinks", {})
            pages: list[tuple[str, str]] = [(city.local_wikipedia, page["title"])]
            english = sitelinks.get("enwiki")
            if english and city.local_wikipedia != "en.wikipedia.org":
                pages.append(("en.wikipedia.org", english["title"]))
            sources = [
                f"https://www.wikidata.org/wiki/{qid}",
                f"https://{city.local_wikipedia}/wiki/{quote(page['title'].replace(' ', '_'))}",
            ]
            candidates.append(
                DiscoveredHotspot(
                    qid=qid,
                    name=name,
                    city_code=city.code,
                    category=category,
                    latitude=float(page["latitude"]),
                    longitude=float(page["longitude"]),
                    distance_km=distance,
                    wikipedia_project=city.local_wikipedia,
                    wikipedia_title=page["title"],
                    pageview_pages=tuple(pages),
                    review_status=status,
                    review_reason=reason,
                    type_ids=tuple(sorted(type_ids)),
                    source_urls=tuple(sources),
                )
            )
        return candidates
