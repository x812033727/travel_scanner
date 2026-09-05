from __future__ import annotations

import hashlib
import json
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, Field
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import CurrentUser
from app.db import get_session
from app.i18n import Locale, current_locale
from app.infra import enforce_named_rate_limit, get_redis
from app.problems import AppError
from app.restaurants.google import (
    RestaurantProviderError,
    RestaurantProviderNotConfigured,
    RestaurantQuotaExceeded,
)
from app.restaurants.service import RestaurantSort, search_restaurants

router = APIRouter(prefix="/hotspots", tags=["hotspot restaurants"])
Session = Annotated[AsyncSession, Depends(get_session)]
RedisDep = Annotated[Redis, Depends(get_redis)]
RequestLocale = Annotated[Locale, Depends(current_locale)]
# A retry after a timeout must not spend Google quota twice; the first result is
# replayed for as long as the browser would plausibly retry.
RESTAURANT_SEARCH_REPLAY_TTL_SECONDS = 10 * 60


def _replay_key(user_id: UUID, hotspot_id: UUID, idempotency_key: str) -> str:
    digest = hashlib.sha256(idempotency_key.encode()).hexdigest()
    return f"restaurants:search-request:{user_id}:{hotspot_id}:{digest}"


class RestaurantSearchRequest(BaseModel):
    radius_km: Literal[5, 10] = 5
    sort: RestaurantSort = "recommended"
    cursor: int | None = Field(default=None, ge=0)
    limit: int = Field(default=20, ge=1, le=20)
    exclude_place_ids: list[str] = Field(default_factory=list, max_length=20)


@router.post("/{hotspot_id}/restaurant-searches")
async def restaurant_search(
    hotspot_id: UUID,
    payload: RestaurantSearchRequest,
    user: CurrentUser,
    session: Session,
    redis: RedisDep,
    locale: RequestLocale,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, object]:
    replay_key = _replay_key(user.id, hotspot_id, idempotency_key)
    cached = await redis.get(replay_key)
    if cached:
        raw = cached.decode() if isinstance(cached, bytes) else str(cached)
        replayed: dict[str, Any] = json.loads(raw)
        return {**replayed, "replayed": True}
    await enforce_named_rate_limit(
        "hotspot-restaurant-search-user",
        str(user.id),
        limit=30,
        window_seconds=3_600,
    )
    settings = await load_runtime_settings(session)
    try:
        result = await search_restaurants(
            session,
            redis,
            settings,
            hotspot_id,
            locale=locale,
            radius_km=payload.radius_km,
            sort=payload.sort,
            cursor=payload.cursor,
            limit=payload.limit,
            exclude_place_ids=payload.exclude_place_ids,
        )
    except RestaurantProviderNotConfigured as exc:
        raise AppError(503, "restaurant_google_not_configured", "Google 餐廳搜尋尚未啟用") from exc
    except RestaurantQuotaExceeded as exc:
        raise AppError(
            429,
            "restaurant_google_budget_exhausted",
            "本月 Google 餐廳搜尋安全額度已用完",
        ) from exc
    except RestaurantProviderError as exc:
        raise AppError(
            503, "restaurant_provider_unavailable", "Google 餐廳資料目前無法取得"
        ) from exc
    await redis.set(
        replay_key,
        json.dumps(result, ensure_ascii=False, default=str),
        ex=RESTAURANT_SEARCH_REPLAY_TTL_SECONDS,
    )
    return result
