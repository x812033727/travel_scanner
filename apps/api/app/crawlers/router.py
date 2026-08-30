from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

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
from app.db import get_session
from app.infra import enforce_rate_limit, get_redis
from app.models import UsageReservation
from app.problems import AppError
from app.usage.service import commit_reservation, release_reservation, reserve_use, usage_status

router = APIRouter(prefix="/crawlers/airlines", tags=["airline crawlers"])
Session = Annotated[AsyncSession, Depends(get_session)]


def require_idempotency_key(value: str | None) -> str:
    if value is None or not 8 <= len(value) <= 255:
        raise AppError(422, "idempotency_key_required", "Idempotency-Key is required")
    return value


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
    payload: AirlineFareSearch,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> AirlineFareSearchResponse:
    await enforce_rate_limit(user.id)
    key = require_idempotency_key(idempotency_key)
    summary = (
        f"航空公開票價 {payload.origin} → {payload.destination} · "
        f"{payload.departure_date or '日期未定'}"
    )
    reservation, _ = await reserve_use(
        session, user.id, key, "public_airline_fare_search", summary
    )
    await session.commit()
    try:
        result = await AirlineFareCrawlerService(get_settings(), get_redis()).search(payload)
        if result.quotes:
            await commit_reservation(session, reservation)
        else:
            await release_reservation(session, reservation, "no_public_fares")
        await session.commit()
        return result.model_copy(update={"usage": usage_status(reservation)})
    except Exception:
        await session.rollback()
        reloaded = await session.get(UsageReservation, reservation.id)
        if reloaded is not None:
            await release_reservation(session, reloaded, "crawler_error")
            await session.commit()
        raise


@router.post("/back-to-back-fares", response_model=BackToBackFareSearchResponse)
async def search_back_to_back_fares(
    payload: BackToBackFareSearch,
    user: CurrentUser,
    session: Session,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> BackToBackFareSearchResponse:
    await enforce_rate_limit(user.id)
    key = require_idempotency_key(idempotency_key)
    summary = (
        f"兩趟航空票價 {payload.origin} → {payload.first_destination}／"
        f"{payload.second_destination} · {payload.first_trip.departure_date}"
    )
    reservation, _ = await reserve_use(
        session, user.id, key, "back_to_back_fare_search", summary
    )
    await session.commit()
    try:
        result = await BackToBackFareService(get_settings(), get_redis()).search(payload)
        usable = any(
            (comparison.conventional and comparison.conventional.estimated_twd is not None)
            or (comparison.back_to_back and comparison.back_to_back.estimated_twd is not None)
            for comparison in result.comparisons
        )
        if usable:
            await commit_reservation(session, reservation)
        else:
            await release_reservation(session, reservation, "no_comparable_fares")
        await session.commit()
        return result.model_copy(update={"usage": usage_status(reservation)})
    except Exception:
        await session.rollback()
        reloaded = await session.get(UsageReservation, reservation.id)
        if reloaded is not None:
            await release_reservation(session, reloaded, "crawler_error")
            await session.commit()
        raise


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
