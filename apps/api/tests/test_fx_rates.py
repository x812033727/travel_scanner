from __future__ import annotations

from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

import app.fx.router as fx_router
from app.crawlers.fx import FxRateError
from app.crawlers.schemas import FxRateSnapshot
from app.main import app
from app.problems import AppError


@pytest.mark.asyncio
async def test_fx_rate_endpoint_requires_authentication() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/fx/rate", params={"base": "JPY", "quote": "TWD"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_fx_rate_endpoint_returns_the_cached_pair_and_maps_misses_to_404(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user_id = uuid4()
    limits: list[tuple[str, str]] = []
    requested: list[tuple[str, str]] = []

    async def enforce(namespace: str, identifier: str, **_kwargs: object) -> None:
        limits.append((namespace, identifier))

    class Provider:
        def __init__(self, *_args: object) -> None:
            pass

        async def rate(self, base: str, quote: str) -> FxRateSnapshot:
            requested.append((base, quote))
            if base == "XXX":
                raise FxRateError("目前無法取得 TWD 估算匯率")
            return FxRateSnapshot(
                base_currency=base,
                quote_currency=quote,
                rate=Decimal("0.2028"),
                as_of=date(2026, 9, 5),
                source_url="https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/jpy.min.json",
            )

    monkeypatch.setattr(fx_router, "enforce_named_rate_limit", enforce)
    monkeypatch.setattr(fx_router, "FxRateProvider", Provider)
    monkeypatch.setattr(fx_router, "get_redis", lambda: object())

    snapshot = await fx_router.get_fx_rate(
        SimpleNamespace(id=user_id),  # type: ignore[arg-type]
        "JPY",
        "TWD",
    )
    assert snapshot.rate == Decimal("0.2028")
    assert limits == [("fx-rate-user", str(user_id))]
    assert requested == [("JPY", "TWD")]

    with pytest.raises(AppError) as missing:
        await fx_router.get_fx_rate(SimpleNamespace(id=user_id), "XXX", "TWD")  # type: ignore[arg-type]
    assert missing.value.status == 404
    assert missing.value.code == "fx_rate_unavailable"
