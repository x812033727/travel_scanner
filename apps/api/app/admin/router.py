from typing import Annotated

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from redis.exceptions import RedisError
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.schemas import (
    ProviderSettingsSnapshot,
    ProviderSettingsUpdate,
    ProviderTestResult,
    PublicRuntimeConfig,
    SiteVisibility,
)
from app.admin.service import (
    apply_runtime_overrides,
    effective_site_visibility,
    provider_rows,
    public_runtime_config,
    settings_snapshot,
    test_provider_connection,
    update_provider_settings,
)
from app.ai import gemini_pool
from app.auth.service import AdminUser, CurrentUser
from app.config import get_settings
from app.db import get_session
from app.infra import get_redis

router = APIRouter(prefix="/admin/provider-settings", tags=["admin provider settings"])
runtime_router = APIRouter(prefix="/runtime", tags=["runtime configuration"])
Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=ProviderSettingsSnapshot)
async def get_provider_settings(user: AdminUser, session: Session) -> ProviderSettingsSnapshot:
    _ = user
    return await settings_snapshot(session, get_redis())


@router.put("/{provider}", response_model=ProviderSettingsSnapshot)
async def put_provider_settings(
    provider: str,
    payload: ProviderSettingsUpdate,
    user: AdminUser,
    session: Session,
) -> ProviderSettingsSnapshot:
    return await update_provider_settings(session, provider, payload, user, get_redis())


@router.post("/{provider}/test", response_model=ProviderTestResult)
async def test_provider(
    provider: str,
    user: AdminUser,
    session: Session,
) -> ProviderTestResult:
    return await test_provider_connection(session, provider, user, get_redis())


class GeminiPoolKey(BaseModel):
    fingerprint_tail: str
    position: int
    site_key: bool
    active: bool
    resting: str | None
    rest_seconds: int
    month_usd: float
    budget_usd: float | None


class GeminiPoolSnapshot(BaseModel):
    keys: list[GeminiPoolKey]
    redis_ok: bool


@router.get("/ai_vendors/gemini-pool", response_model=GeminiPoolSnapshot)
async def get_gemini_pool(user: AdminUser, session: Session) -> GeminiPoolSnapshot:
    """Each Gemini key in the order it is used, named by the last four of its fingerprint."""
    _ = user
    # The stored settings, not load_runtime_settings: that one has already swapped in the pick.
    settings = apply_runtime_overrides(get_settings(), await provider_rows(session))
    keys = gemini_pool.pool_keys(settings)
    redis = get_redis() if len(keys) > 1 else None
    redis_ok = True
    try:
        states = await gemini_pool.states(redis, settings)
    except RedisError:
        redis_ok = False
        states = await gemini_pool.states(None, settings)
    active = await gemini_pool.choose(redis, settings) if redis_ok else (keys[0] if keys else None)
    active_fp = gemini_pool.fingerprint(active) if active else None
    site = settings.hotspot_guide_gemini_api_key
    site_fp = gemini_pool.fingerprint(site) if site else None
    return GeminiPoolSnapshot(
        keys=[
            GeminiPoolKey(
                fingerprint_tail=state.fp[-4:],
                position=state.position,
                site_key=state.fp == site_fp,
                active=state.fp == active_fp,
                resting=state.resting,
                rest_seconds=state.rest_seconds,
                month_usd=state.month_usd,
                budget_usd=state.budget_usd,
            )
            for state in states
        ],
        redis_ok=redis_ok,
    )


@runtime_router.get("/public-config", response_model=PublicRuntimeConfig)
async def get_public_runtime_config(user: CurrentUser, session: Session) -> PublicRuntimeConfig:
    _ = user
    return await public_runtime_config(session)


@runtime_router.get("/site-visibility", response_model=SiteVisibility)
async def get_site_visibility(response: Response, session: Session) -> SiteVisibility:
    response.headers["Cache-Control"] = "no-store"
    return await effective_site_visibility(session)
