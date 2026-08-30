from fastapi import APIRouter

from app.auth.service import CurrentUser
from app.config import get_settings
from app.crawlers.airlines import AirlineFareCrawlerService
from app.crawlers.schemas import (
    AirlineCrawlerStatusResponse,
    AirlineFareSearch,
    AirlineFareSearchResponse,
)
from app.infra import enforce_rate_limit, get_redis

router = APIRouter(prefix="/crawlers/airlines", tags=["airline crawlers"])


@router.get("/status", response_model=AirlineCrawlerStatusResponse)
async def crawler_status() -> AirlineCrawlerStatusResponse:
    return AirlineCrawlerStatusResponse(
        sources=AirlineFareCrawlerService.status(),
        safety_rules=[
            "僅允許固定航空公司 HTTPS host，拒絕任意 URL，避免 SSRF",
            "快取失效後先檢查 robots.txt；無法確認時 fail closed",
            "每個來源至少間隔數秒並設回應大小、timeout 與一次 transient retry",
            "只回傳公開近期快取票價；不登入、不繞過 CAPTCHA、不呼叫私人訂位端點",
        ],
    )


@router.post("/fares", response_model=AirlineFareSearchResponse)
async def search_public_fares(
    payload: AirlineFareSearch, user: CurrentUser
) -> AirlineFareSearchResponse:
    await enforce_rate_limit(user.id)
    return await AirlineFareCrawlerService(get_settings(), get_redis()).search(payload)
