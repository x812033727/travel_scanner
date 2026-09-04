from __future__ import annotations

import asyncio
import math
from dataclasses import dataclass
from typing import Any, cast
from urllib.parse import quote

import httpx

from app.hotspots.cities import HotspotCity

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

    async def discover_city(self, city: HotspotCity, limit: int = 100) -> list[DiscoveredHotspot]:
        pages_by_qid: dict[str, dict[str, Any]] = {}
        api = f"https://{city.local_wikipedia}/w/api.php"
        for center in city.centers:
            payload = await self._get(
                api,
                {
                    "action": "query",
                    "format": "json",
                    "formatversion": "2",
                    "list": "geosearch",
                    "gscoord": f"{center.latitude}|{center.longitude}",
                    "gsradius": str(min(center.radius_km * 1000, 10_000)),
                    "gslimit": str(min(limit, 100)),
                    "gsnamespace": "0",
                },
            )
            nearby = payload.get("query", {}).get("geosearch", [])
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
                        },
                    )
        qids = list(pages_by_qid)[:limit]
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
            distance = min(
                haversine_km(
                    center.latitude,
                    center.longitude,
                    float(page["latitude"]),
                    float(page["longitude"]),
                )
                for center in city.centers
            )
            if distance > max(center.radius_km for center in city.centers):
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
