from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.analytics.schemas import (
    AnalyticsConfigResponse,
    AnalyticsEventBatch,
    AnalyticsIngestResponse,
    AnalyticsRange,
)
from app.analytics.service import dashboard, ingest_events, public_config
from app.auth.service import AdminUser
from app.db import get_session

router = APIRouter(prefix="/analytics", tags=["analytics"])
admin_router = APIRouter(prefix="/admin/analytics", tags=["admin analytics"])
Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("/config", response_model=AnalyticsConfigResponse)
async def get_analytics_config(response: Response, session: Session) -> AnalyticsConfigResponse:
    response.headers["Cache-Control"] = "no-store"
    return await public_config(session)


@router.post(
    "/events",
    response_model=AnalyticsIngestResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def post_analytics_events(
    request: Request,
    payload: AnalyticsEventBatch,
    session: Session,
) -> AnalyticsIngestResponse:
    return await ingest_events(session, request, payload)


@admin_router.get("/dashboard")
async def get_analytics_dashboard(
    user: AdminUser,
    session: Session,
    range: Annotated[AnalyticsRange, Query()] = "30d",
    compare: bool = True,
    include_bots: bool = False,
) -> dict[str, Any]:
    _ = user
    return await dashboard(session, range, compare, include_bots)
