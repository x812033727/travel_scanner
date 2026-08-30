from fastapi import APIRouter

from app.providers.registry import ProviderStatus, provider_status

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("/status")
async def get_provider_status() -> ProviderStatus:
    return provider_status()
