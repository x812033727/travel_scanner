"""The anonymous endpoint the article pages read before deciding to render a slot."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.ads.service import adsense_config
from app.db import get_session

router = APIRouter(tags=["ads"])

Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("/ads/config")
async def public_ads_config(
    session: Session, request: Request, response: Response
) -> dict[str, Any]:
    # `no-store` because the owner switches this from the back office and expects the
    # next page view to reflect it; `no-referrer` so the article URL a reader is on is
    # never attached to this request.
    response.headers["Cache-Control"] = "no-store"
    response.headers["Referrer-Policy"] = "no-referrer"
    settings = await load_runtime_settings(session)
    return adsense_config(
        settings,
        tracking_allowed=request.headers.get("dnt") != "1"
        and request.headers.get("sec-gpc") != "1",
    )
