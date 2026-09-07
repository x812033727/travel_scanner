"""One-off, ten-call IDs-only lookup; no key or Google content is persisted."""
import asyncio
import json

import httpx

from app.admin.service import load_runtime_settings
from app.db import SessionFactory, engine
from app.infra import get_redis
from app.providers.usage_meter import record_google_maps_request


QUERIES = [
    [
        "vischio-osaka",
        "hotel vischio osaka 2-4-10 Shibata Osaka Japan"
    ],
    [
        "hankyu-respire-osaka",
        "hotel hankyu respire osaka 1-1 Ofukacho Osaka Japan"
    ],
    [
        "intergate-osaka-umeda",
        "hotel intergate osaka umeda 2-5-2 Umeda Osaka Japan"
    ],
    [
        "granvia-osaka",
        "hotel granvia osaka 3-1-1 Umeda Osaka Japan"
    ],
    [
        "new-otani-osaka",
        "hotel new otani osaka 1-4-1 Shiromi Osaka Japan"
    ],
    [
        "monterey-lasoeur-osaka",
        "hotel monterey la soeur osaka 2-2-22 Shiromi Osaka Japan"
    ],
    [
        "royal-classic-osaka",
        "hotel royal classic osaka 4-3-3 Namba Osaka Japan"
    ],
    [
        "swissotel-nankai-osaka",
        "swissotel nankai osaka 5-1-60 Namba Osaka Japan"
    ],
    [
        "sotetsu-grand-fresa-osaka-namba",
        "sotetsu grand fresa osaka namba 1-1-13 Nippombashi Osaka Japan"
    ],
    [
        "gracery-osaka-namba",
        "hotel gracery osaka namba 1-4-4 Motomachi Osaka Japan"
    ]
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
