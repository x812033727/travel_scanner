from fastapi import APIRouter

from app.auth.service import CurrentUser
from app.config import get_settings
from app.crawlers.airlines import (
    AirlineFareCrawlerService,
    CrawlerError,
    CrawlerPolicyError,
)
from app.crawlers.back_to_back import BackToBackFareService
from app.crawlers.schemas import (
    AirlineBrowserCapture,
    AirlineBrowserCaptureResponse,
    AirlineBrowserTargetsResponse,
    AirlineCrawlerStatusResponse,
    AirlineFareSearch,
    AirlineFareSearchResponse,
    BackToBackFareSearch,
    BackToBackFareSearchResponse,
)
from app.infra import enforce_rate_limit, get_redis
from app.problems import AppError

router = APIRouter(prefix="/crawlers/airlines", tags=["airline crawlers"])


@router.get("/status", response_model=AirlineCrawlerStatusResponse)
async def crawler_status() -> AirlineCrawlerStatusResponse:
    return AirlineCrawlerStatusResponse(
        sources=AirlineFareCrawlerService.status(),
        safety_rules=[
            "僅允許固定航空公司 HTTPS host，拒絕任意 URL，避免 SSRF",
            "快取失效後先檢查 robots.txt；無法確認時 fail closed",
            "每個來源至少間隔數秒並設回應大小、timeout 與一次 transient retry",
            "Chrome 工具只接收後端核發的官方目標，且僅回傳 __NEXT_DATA__ 的白名單票價欄位",
            "只回傳公開近期快取票價；不登入、不繞過 CAPTCHA、不呼叫私人訂位端點",
        ],
    )


@router.post("/fares", response_model=AirlineFareSearchResponse)
async def search_public_fares(
    payload: AirlineFareSearch, user: CurrentUser
) -> AirlineFareSearchResponse:
    await enforce_rate_limit(user.id)
    return await AirlineFareCrawlerService(get_settings(), get_redis()).search(payload)


@router.post("/back-to-back-fares", response_model=BackToBackFareSearchResponse)
async def search_back_to_back_fares(
    payload: BackToBackFareSearch, user: CurrentUser
) -> BackToBackFareSearchResponse:
    await enforce_rate_limit(user.id)
    return await BackToBackFareService(get_settings(), get_redis()).search(payload)


@router.post("/browser-targets", response_model=AirlineBrowserTargetsResponse)
async def prepare_browser_targets(
    payload: AirlineFareSearch, user: CurrentUser
) -> AirlineBrowserTargetsResponse:
    await enforce_rate_limit(user.id)
    return await AirlineFareCrawlerService(get_settings(), get_redis()).browser_targets(payload)


@router.post("/browser-captures", response_model=AirlineBrowserCaptureResponse)
async def parse_browser_capture(
    payload: AirlineBrowserCapture, user: CurrentUser
) -> AirlineBrowserCaptureResponse:
    await enforce_rate_limit(user.id)
    try:
        return await AirlineFareCrawlerService(
            get_settings(), get_redis()
        ).parse_browser_capture(payload)
    except CrawlerPolicyError as exc:
        raise AppError(403, exc.code, exc.detail) from exc
    except CrawlerError as exc:
        raise AppError(422, exc.code, exc.detail) from exc
