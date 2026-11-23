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
    slot: str = "A"
    configured: bool = True
    fingerprint_tail: str
    position: int
    site_key: bool
    active: bool
    is_turn: bool = False
    resting: str | None
    rest_seconds: int
    month_usd: float
    budget_usd: float | None


class GeminiPoolSnapshot(BaseModel):
    keys: list[GeminiPoolKey]
    current_turn_slot: str | None = None
    slot_count: int = gemini_pool.DEFAULT_VISIBLE_SLOTS
    redis_ok: bool


class GeminiPoolSlotUpdate(BaseModel):
    api_key: str | None = None
    clear: bool = False
    budget_usd: float | None = None


class GeminiPoolTurnUpdate(BaseModel):
    slot: str


async def _build_gemini_pool_snapshot(session: AsyncSession) -> GeminiPoolSnapshot:
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
    turn_slot = (
        await gemini_pool.current_turn(redis, settings)
        if redis_ok
        else await gemini_pool.current_turn(None, settings)
    )
    active_fp = gemini_pool.fingerprint(active) if active else None
    site = settings.hotspot_guide_gemini_api_key
    site_fp = gemini_pool.fingerprint(site) if site else None
    extra_slots = gemini_pool.parse_extra_slots(settings.hotspot_guide_gemini_api_keys_extra)
    highest_idx = max(
        (gemini_pool.SLOT_LETTERS.index(s) for s in extra_slots if s in gemini_pool.SLOT_LETTERS),
        default=-1,
    )
    slot_count = max(gemini_pool.DEFAULT_VISIBLE_SLOTS, highest_idx + 1)
    return GeminiPoolSnapshot(
        keys=[
            GeminiPoolKey(
                slot=state.slot,
                configured=True,
                fingerprint_tail=state.fp[-4:],
                position=state.position,
                site_key=state.fp == site_fp or state.slot == gemini_pool.SITE_SLOT,
                active=state.fp == active_fp,
                is_turn=state.slot == turn_slot,
                resting=state.resting,
                rest_seconds=state.rest_seconds,
                month_usd=state.month_usd,
                budget_usd=state.budget_usd,
            )
            for state in states
        ],
        current_turn_slot=turn_slot,
        slot_count=slot_count,
        redis_ok=redis_ok,
    )


@router.get("/ai_vendors/gemini-pool", response_model=GeminiPoolSnapshot)
async def get_gemini_pool(user: AdminUser, session: Session) -> GeminiPoolSnapshot:
    """Each Gemini key in the order it is used, named by its slot and fingerprint tail."""
    _ = user
    return await _build_gemini_pool_snapshot(session)


@router.put("/ai_vendors/gemini-pool/slots/{slot}", response_model=GeminiPoolSnapshot)
async def put_gemini_pool_slot(
    slot: str,
    payload: GeminiPoolSlotUpdate,
    user: AdminUser,
    session: Session,
) -> GeminiPoolSnapshot:
    """Save or clear one individual Google AI Ultra slot (A, B, C...) and its optional budget."""
    from app.problems import AppError

    slot_key = slot.strip().upper()
    if slot_key not in gemini_pool.SLOT_LETTERS and slot_key != gemini_pool.SITE_SLOT:
        raise AppError(422, "gemini_pool_invalid_slot", "帳號槽代號必須是 A 到 Z")
    settings = apply_runtime_overrides(get_settings(), await provider_rows(session))
    extra_slots = gemini_pool.parse_extra_slots(settings.hotspot_guide_gemini_api_keys_extra)
    budgets_by_slot = gemini_pool.parse_slot_budgets(
        settings.hotspot_guide_gemini_key_budgets_usd, list(extra_slots.keys())
    )
    redis = get_redis()

    if payload.clear:
        if slot_key == gemini_pool.SITE_SLOT:
            raise AppError(422, "gemini_pool_invalid_slot", "網站金鑰請在下方金鑰欄位清除")
        extra_slots.pop(slot_key, None)
        budgets_by_slot.pop(slot_key, None)
    else:
        if payload.api_key is not None and payload.api_key.strip():
            if slot_key == gemini_pool.SITE_SLOT:
                raise AppError(422, "gemini_pool_invalid_slot", "網站金鑰請在下方金鑰欄位修改")
            new_key = payload.api_key.strip()
            for other_slot, existing_key in extra_slots.items():
                if other_slot != slot_key and existing_key == new_key:
                    raise AppError(
                        422,
                        "gemini_pool_duplicate_key",
                        f"這把金鑰已經儲存在帳號 {other_slot} 了",
                    )
            extra_slots[slot_key] = new_key
            try:
                await redis.delete(f"{gemini_pool.PREFIX}:rest:{gemini_pool.fingerprint(new_key)}")
            except RedisError:
                pass
        if "budget_usd" in payload.model_fields_set:
            if slot_key not in extra_slots and slot_key != gemini_pool.SITE_SLOT:
                raise AppError(
                    422, "gemini_pool_slot_not_configured", f"請先輸入帳號 {slot_key} 的金鑰"
                )
            budgets_by_slot[slot_key] = (
                float(payload.budget_usd)
                if payload.budget_usd is not None and payload.budget_usd > 0
                else None
            )

    new_extra_raw = gemini_pool.serialize_extra_slots(extra_slots)
    new_budgets_raw = gemini_pool.serialize_slot_budgets(budgets_by_slot)
    await update_provider_settings(
        session,
        "ai_vendors",
        ProviderSettingsUpdate(
            config={"hotspot_guide_gemini_key_budgets_usd": new_budgets_raw},
            secrets={"hotspot_guide_gemini_api_keys_extra": new_extra_raw},
        ),
        user,
        redis,
    )
    return await _build_gemini_pool_snapshot(session)


@router.post("/ai_vendors/gemini-pool/turn", response_model=GeminiPoolSnapshot)
async def post_gemini_pool_turn(
    payload: GeminiPoolTurnUpdate,
    user: AdminUser,
    session: Session,
) -> GeminiPoolSnapshot:
    """Switch the circular rotation pointer to start from the chosen slot (A, B, C...)."""
    from app.problems import AppError

    _ = user
    settings = apply_runtime_overrides(get_settings(), await provider_rows(session))
    try:
        await gemini_pool.set_turn(get_redis(), settings, payload.slot)
    except ValueError as exc:
        raise AppError(
            422, "gemini_pool_slot_not_configured", "這個帳號槽尚未設定金鑰，無法設為起始帳號"
        ) from exc
    except RedisError as exc:
        raise AppError(503, "gemini_pool_redis_unavailable", "Redis 暫時無法連線") from exc
    return await _build_gemini_pool_snapshot(session)


@runtime_router.get("/public-config", response_model=PublicRuntimeConfig)
async def get_public_runtime_config(user: CurrentUser, session: Session) -> PublicRuntimeConfig:
    _ = user
    return await public_runtime_config(session)


@runtime_router.get("/site-visibility", response_model=SiteVisibility)
async def get_site_visibility(response: Response, session: Session) -> SiteVisibility:
    response.headers["Cache-Control"] = "no-store"
    return await effective_site_visibility(session)
