from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.db import get_session
from app.providers.registry import ProviderStatus, provider_status

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("/status")
async def get_provider_status(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ProviderStatus:
    return provider_status(await load_runtime_settings(session))
