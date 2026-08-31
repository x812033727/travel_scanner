from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.schemas import (
    ProviderSettingsSnapshot,
    ProviderSettingsUpdate,
    ProviderTestResult,
    PublicRuntimeConfig,
)
from app.admin.service import (
    public_runtime_config,
    settings_snapshot,
    test_provider_connection,
    update_provider_settings,
)
from app.auth.service import AdminUser, CurrentUser
from app.db import get_session
from app.infra import get_redis

router = APIRouter(prefix="/admin/provider-settings", tags=["admin provider settings"])
runtime_router = APIRouter(prefix="/runtime", tags=["runtime configuration"])
Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=ProviderSettingsSnapshot)
async def get_provider_settings(user: AdminUser, session: Session) -> ProviderSettingsSnapshot:
    _ = user
    return await settings_snapshot(session)


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


@runtime_router.get("/public-config", response_model=PublicRuntimeConfig)
async def get_public_runtime_config(user: CurrentUser, session: Session) -> PublicRuntimeConfig:
    _ = user
    return await public_runtime_config(session)
