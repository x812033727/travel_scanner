"""Fetch the three opinions a candidate needs, and hand them to ``candidates.decide``.

Kept apart from ``candidates.py`` so the rule that decides what may be published stays
testable without a network. Everything here is retrieval; nothing here decides.

Wikipedia rate-limits bursts and answers a throttled request with a normal-looking
error, so calls are paced and every failure is counted rather than swallowed - an
earlier probe hid 429s and reported famous temples as having no article at all.
"""

from __future__ import annotations

import asyncio
from collections import Counter
from typing import Any, cast

import httpx

from app.hotspots.candidates import (
    GEOSEARCH_RADIUS_M,
    CandidateInput,
    CandidateResolution,
    NearbyArticle,
    decide,
)
from app.places.google import GoogleTravelService

WIKI_LANGS = ("ja", "zh", "en")
LABEL_LANGS = ("ja", "zh", "zh-tw", "zh-hant", "ko", "th", "vi", "en")
PACE_SECONDS = 0.6
USER_AGENT = "mokaair-hotspot-candidates/1.0 (https://mokaair.com; ops@mokaair.com)"


class CandidateResolver:
    def __init__(
        self,
        google: GoogleTravelService,
        client: httpx.AsyncClient,
        *,
        langs: tuple[str, ...] = WIKI_LANGS,
        pace_seconds: float = PACE_SECONDS,
    ) -> None:
        self.google = google
        self.client = client
        self.langs = langs
        self.pace_seconds = pace_seconds
        self.failures: Counter[str] = Counter()

    async def _get(self, url: str, params: dict[str, str], tag: str) -> dict[str, Any] | None:
        await asyncio.sleep(self.pace_seconds)
        try:
            response = await self.client.get(
                url, params=params, headers={"User-Agent": USER_AGENT}
            )
        except httpx.HTTPError as exc:
            self.failures[f"{tag}:{type(exc).__name__}"] += 1
            return None
        if response.status_code != 200:
            self.failures[f"{tag}:HTTP{response.status_code}"] += 1
            return None
        try:
            return cast(dict[str, Any], response.json())
        except ValueError:
            self.failures[f"{tag}:bad_json"] += 1
            return None

    async def _nearby(self, lang: str, latitude: float, longitude: float) -> list[dict[str, Any]]:
        payload = await self._get(
            f"https://{lang}.wikipedia.org/w/api.php",
            {
                "action": "query",
                "format": "json",
                "formatversion": "2",
                "generator": "geosearch",
                "ggscoord": f"{latitude}|{longitude}",
                "ggsradius": str(GEOSEARCH_RADIUS_M),
                "ggslimit": "20",
                "prop": "coordinates|pageprops",
                "ppprop": "wikibase_item",
            },
            f"geo:{lang}",
        )
        if not payload:
            return []
        found: list[dict[str, Any]] = []
        for page in payload.get("query", {}).get("pages", []):
            coordinates = (page.get("coordinates") or [{}])[0]
            qid = (page.get("pageprops") or {}).get("wikibase_item")
            if coordinates.get("lat") is None or not qid:
                continue
            found.append(
                {
                    "project": f"{lang}.wikipedia.org",
                    "title": page.get("title"),
                    "qid": qid,
                    "latitude": float(coordinates["lat"]),
                    "longitude": float(coordinates["lon"]),
                }
            )
        return found

    async def _entities(self, qids: list[str]) -> dict[str, tuple[tuple[str, ...], frozenset[str]]]:
        """Names and P31 type ids per entity, which is what identity and category need."""
        out: dict[str, tuple[tuple[str, ...], frozenset[str]]] = {}
        for start in range(0, len(qids), 40):
            payload = await self._get(
                "https://www.wikidata.org/w/api.php",
                {
                    "action": "wbgetentities",
                    "format": "json",
                    "ids": "|".join(qids[start : start + 40]),
                    "props": "labels|aliases|claims",
                    "languages": "|".join(LABEL_LANGS),
                },
                "wikidata",
            )
            if not payload:
                continue
            for qid, entity in (payload.get("entities") or {}).items():
                names = [item["value"] for item in (entity.get("labels") or {}).values()]
                for aliases in (entity.get("aliases") or {}).values():
                    names.extend(item["value"] for item in aliases)
                type_ids = {
                    claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id")
                    for claim in (entity.get("claims") or {}).get("P31", [])
                }
                type_ids.discard(None)
                out[qid] = (tuple(names), frozenset(cast(set[str], type_ids)))
        return out

    async def resolve(self, candidate: CandidateInput) -> CandidateResolution:
        found = await self.google.search_place(candidate.query, None, None, detailed=False)
        place_id = str(found.get("id") or "") if found else ""
        location = (found or {}).get("location") or {}
        latitude, longitude = location.get("latitude"), location.get("longitude")
        if not place_id or latitude is None or longitude is None:
            return decide(candidate, None, None, None, [])

        raw: list[dict[str, Any]] = []
        for lang in self.langs:
            raw.extend(await self._nearby(lang, float(latitude), float(longitude)))
        entities = await self._entities([item["qid"] for item in raw])
        articles = [
            NearbyArticle(
                wikipedia_project=item["project"],
                title=str(item["title"]),
                qid=item["qid"],
                latitude=item["latitude"],
                longitude=item["longitude"],
                names=entities.get(item["qid"], ((), frozenset()))[0],
                type_ids=entities.get(item["qid"], ((), frozenset()))[1],
            )
            for item in raw
        ]
        return decide(candidate, place_id, float(latitude), float(longitude), articles)

    async def resolve_all(self, candidates: list[CandidateInput]) -> list[CandidateResolution]:
        return [await self.resolve(candidate) for candidate in candidates]
