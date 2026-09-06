"""Exchange rates for the planner: one pair per request, cached for a day upstream."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query

from app.auth.service import CurrentUser
from app.config import get_settings
from app.crawlers.fx import FxRateError, FxRateProvider
from app.crawlers.schemas import FxRateSnapshot
from app.infra import enforce_named_rate_limit, get_redis
from app.problems import AppError

router = APIRouter(prefix="/fx", tags=["fx"])

FX_RATE_USER_LIMIT = 120
FX_RATE_USER_WINDOW_SECONDS = 3_600

CurrencyCode = Annotated[str, Query(min_length=3, max_length=3, pattern="^[A-Za-z]{3}$")]


@router.get("/rate", response_model=FxRateSnapshot)
async def get_fx_rate(
    user: CurrentUser,
    base: CurrencyCode,
    quote: CurrencyCode = "TWD",
) -> FxRateSnapshot:
    """How much one unit of ``base`` is worth in ``quote`` today.

    Rates come from Currency-api's daily static files (Frankfurter as the last resort)
    and are cached for a day, so this never turns into a per-keystroke upstream call.
    """
    await enforce_named_rate_limit(
        "fx-rate-user",
        str(user.id),
        limit=FX_RATE_USER_LIMIT,
        window_seconds=FX_RATE_USER_WINDOW_SECONDS,
    )
    try:
        return await FxRateProvider(get_settings(), get_redis()).rate(base, quote)
    except FxRateError as exc:
        raise AppError(404, "fx_rate_unavailable", str(exc)) from exc
