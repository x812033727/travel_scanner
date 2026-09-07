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
        "palais-de-chine",
        "Palais de Chine Hotel 3 Chengde Road Section 1 Taipei Taiwan"
    ],
    [
        "cosmos-taipei",
        "Cosmos Hotel Taipei 43 Zhongxiao West Road Section 1 Taipei Taiwan"
    ],
    [
        "caesar-park-taipei",
        "Caesar Park Hotel Taipei 38 Zhongxiao West Road Section 1 Taipei Taiwan"
    ],
    [
        "cityinn-station-iii",
        "CityInn Hotel Taipei Station Branch III 77 Changan West Road Taipei Taiwan"
    ],
    [
        "amba-ximending",
        "amba Taipei Ximending 77 Wuchang Street Section 2 Taipei Taiwan"
    ],
    [
        "westgate",
        "WESTGATE Hotel Taipei 150 Zhonghua Road Section 1 Taipei Taiwan"
    ],
    [
        "solaria-nishitetsu-ximen",
        "Solaria Nishitetsu Hotel Taipei Ximen 88 Zhonghua Road Section 1 Taipei Taiwan"
    ],
    [
        "w-taipei",
        "W Taipei 10 Zhongxiao East Road Section 5 Taipei Taiwan"
    ],
    [
        "grand-hyatt-taipei",
        "Grand Hyatt Taipei 2 Songshou Road Taipei Taiwan"
    ],
    [
        "humble-house-taipei",
        "Humble House Taipei 18 Songgao Road Taipei Taiwan"
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
                json={"textQuery": query, "languageCode": "zh-TW", "regionCode": "TW", "pageSize": 2},
            )
            if response.status_code != 200:
                print(json.dumps({"source_key": source_key, "http_status": response.status_code}))
                break
            print(json.dumps({"source_key": source_key, "place_ids": [p["id"] for p in response.json().get("places", [])]}), flush=True)
    await redis.aclose()
    await engine.dispose()


asyncio.run(main())
