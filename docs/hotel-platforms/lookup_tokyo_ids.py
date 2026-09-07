"""One-off, four-call IDs-only lookup; no key or Google content is persisted."""
import asyncio
import json

import httpx

from app.admin.service import load_runtime_settings
from app.db import SessionFactory, engine
from app.infra import get_redis
from app.providers.usage_meter import record_google_maps_request


QUERIES = [
    ("tokyo-station-hotel", "The Tokyo Station Hotel 1-9-1 Marunouchi Tokyo Japan"),
    ("ryumeikan-tokyo", "Hotel Ryumeikan Tokyo 1-3-22 Yaesu Tokyo Japan"),
    ("mitsui-garden-kyobashi", "Mitsui Garden Hotel Kyobashi 1-3-6 Kyobashi Tokyo Japan"),
    ("millennium-mitsui-garden-tokyo", "Millennium Mitsui Garden Hotel Tokyo 5-11-1 Ginza Tokyo Japan"),
]


async def main():
    async with SessionFactory() as session:
        settings = await load_runtime_settings(session)
    if not settings.google_maps_api_key:
        raise RuntimeError("Google Maps server key is not configured")
    redis = get_redis()
    async with httpx.AsyncClient(timeout=15, trust_env=False) as client:
        for source_key, query in QUERIES:
            await record_google_maps_request(redis, "places_text_search_ids_only")
            response = await client.post(
                "https://places.googleapis.com/v1/places:searchText",
                headers={"X-Goog-Api-Key": settings.google_maps_api_key, "X-Goog-FieldMask": "places.id"},
                json={"textQuery": query, "languageCode": "ja", "regionCode": "JP", "pageSize": 2},
            )
            if response.status_code != 200:
                print(json.dumps({"source_key": source_key, "http_status": response.status_code}))
                break
            print(json.dumps({"source_key": source_key, "place_ids": [p["id"] for p in response.json().get("places", [])]}), flush=True)
    await redis.aclose()
    await engine.dispose()


asyncio.run(main())
