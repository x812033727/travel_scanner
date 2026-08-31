from typing import Any
from uuid import uuid4

import fakeredis.aioredis
import httpx
import pytest

import app.affiliates.router as affiliate_router
from app.affiliates.registry import PARTNERS_BY_CODE, partner_configured, partners_for_module
from app.affiliates.service import (
    AffiliateContext,
    TravelpayoutsLinkClient,
    allowed_hosts,
    resolve_partner_target,
    validate_target_url,
)
from app.config import Settings
from app.models import AffiliateClick, SearchRequest, UsageLedger, User
from app.problems import AppError


class AffiliateSession:
    def __init__(self, search: SearchRequest | None = None) -> None:
        self.search = search
        self.added: list[Any] = []
        self.commits = 0

    async def scalar(self, _statement: object) -> SearchRequest | None:
        return self.search

    def add(self, value: Any) -> None:
        self.added.append(value)

    async def commit(self) -> None:
        self.commits += 1


def test_registry_defaults_disabled_and_orders_each_module() -> None:
    settings = Settings()
    assert all(not getattr(settings, item.enabled_field) for item in PARTNERS_BY_CODE.values())
    assert [item.code for item in partners_for_module("flight")] == [
        "skyscanner",
        "trip_com",
        "travelpayouts",
    ]
    assert [item.code for item in partners_for_module("hotel")] == [
        "booking",
        "agoda",
        "trip_com",
        "travelpayouts",
    ]
    assert [item.code for item in partners_for_module("connectivity")] == ["airalo"]


def test_partner_requires_allowlist_and_platform_identifier_when_applicable() -> None:
    assert not partner_configured(
        PARTNERS_BY_CODE["booking"],
        Settings(booking_affiliate_url_template="https://www.booking.com/search?ss={destination}"),
    )
    assert partner_configured(
        PARTNERS_BY_CODE["booking"],
        Settings(
            booking_affiliate_id="affiliate-1",
            booking_affiliate_url_template="https://www.booking.com/search?ss={destination}",
        ),
    )


@pytest.mark.parametrize(
    "target",
    (
        "http://www.booking.com/search",
        "https://booking.com.evil.example/search",
        "https://user:password@booking.com/search",
        "https://evil.example/search",
    ),
)
def test_clickout_target_rejects_open_redirects(target: str) -> None:
    with pytest.raises(ValueError):
        validate_target_url(target, {"booking.com"})
    assert validate_target_url("https://www.booking.com/search", {"booking.com"})


@pytest.mark.asyncio
async def test_static_link_renders_safe_fields_and_tracking_identifier() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(
        booking_enabled=True,
        booking_affiliate_id="affiliate-1",
        booking_affiliate_url_template=(
            "https://www.booking.com/search?ss={destination}&checkin={departure_date}"
        ),
    )
    target = await resolve_partner_target(
        PARTNERS_BY_CODE["booking"],
        AffiliateContext("hotel", "東京 站", "2026-10-10", "2026-10-14", "sub-1"),
        settings,
        redis,
    )
    assert target.startswith("https://www.booking.com/search?")
    assert "ss=%E6%9D%B1%E4%BA%AC+%E7%AB%99" in target
    assert "aid=affiliate-1" in target


@pytest.mark.asyncio
async def test_travelpayouts_success_is_cached() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        assert request.headers["X-Access-Token"] == "secret-token"
        payload = request.read().decode()
        assert '"trs":123' in payload and '"marker":456' in payload
        return httpx.Response(
            200,
            json={
                "result": {
                    "links": [{"code": "success", "partner_url": "https://brand.tp.st/path"}]
                }
            },
        )

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(
        travelpayouts_api_token="secret-token",
        travelpayouts_project_id="123",
        travelpayouts_marker="456",
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        client = TravelpayoutsLinkClient(redis, settings, http)
        first = await client.create("https://brand.example/search", "sub-1")
        second = await client.create("https://brand.example/search", "sub-1")
    assert first == second == "https://brand.tp.st/path"
    assert calls == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("status", (401, 429, 500))
async def test_travelpayouts_api_failure_uses_only_safe_static_fallback(status: int) -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json={"error": "provider failure"})

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(
        travelpayouts_api_token="secret-token",
        travelpayouts_project_id="123",
        travelpayouts_marker="456",
        travelpayouts_flight_target_url="https://brand.example/search",
        travelpayouts_static_url_template="https://travelpayouts.com/flights?destination={destination}",
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        target = await resolve_partner_target(
            PARTNERS_BY_CODE["travelpayouts"],
            AffiliateContext("flight", "東京", "2026-10-10", "2026-10-14", "sub-1"),
            settings,
            redis,
            TravelpayoutsLinkClient(redis, settings, http),
        )
    assert target.startswith("https://travelpayouts.com/flights?")


@pytest.mark.asyncio
async def test_travelpayouts_timeout_without_fallback_hides_option() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out", request=request)

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(
        travelpayouts_api_token="secret-token",
        travelpayouts_project_id="123",
        travelpayouts_marker="456",
        travelpayouts_flight_target_url="https://brand.example/search",
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        with pytest.raises(ConnectionError):
            await resolve_partner_target(
                PARTNERS_BY_CODE["travelpayouts"],
                AffiliateContext("flight", "東京", None, None, "sub-1"),
                settings,
                redis,
                TravelpayoutsLinkClient(redis, settings, http),
            )


def test_status_serialization_cannot_contain_credentials() -> None:
    settings = Settings(
        booking_enabled=True,
        booking_affiliate_id="do-not-expose",
        booking_affiliate_url_template="https://booking.com/search",
        booking_demand_api_token="also-secret",
    )
    partner = PARTNERS_BY_CODE["booking"]
    public: dict[str, Any] = {
        "code": partner.code,
        "enabled": getattr(settings, partner.enabled_field),
        "configured": partner_configured(partner, settings),
        "modules": partner.modules,
        "capabilities": partner.capabilities,
    }
    assert "do-not-expose" not in str(public)
    assert "also-secret" not in str(public)
    assert allowed_hosts(settings, partner) == {"booking.com", "www.booking.com"}


@pytest.mark.asyncio
async def test_options_and_clickout_record_append_only_summary_without_usage_charge(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(
        booking_enabled=True,
        booking_affiliate_id="affiliate-1",
        booking_affiliate_url_template="https://www.booking.com/search?ss={destination}",
    )
    user = User(id=uuid4(), email="member@example.com", password_hash="unused", is_active=True)
    search = SearchRequest(
        id=uuid4(),
        user_id=user.id,
        status="completed",
        operation="full_trip_search",
        request_json={
            "destination": "東京",
            "departure_date": "2026-10-10",
            "return_date": "2026-10-14",
            "travelers": {"adults": 2},
        },
    )
    session = AffiliateSession(search)

    async def runtime_settings(_session: object) -> Settings:
        return settings

    monkeypatch.setattr(affiliate_router, "get_redis", lambda: redis)
    monkeypatch.setattr(affiliate_router, "load_runtime_settings", runtime_settings)
    response = await affiliate_router.affiliate_options(
        "hotel",
        user,
        session,
        search_id=search.id,  # type: ignore[arg-type]
    )
    assert [item.partner for item in response.options] == ["booking"]
    token = response.options[0].clickout_url.rsplit("token=", 1)[-1]

    redirect = await affiliate_router.affiliate_clickout(
        "booking",
        token,
        user,
        session,  # type: ignore[arg-type]
    )
    assert redirect.status_code == 303
    assert redirect.headers["location"].startswith("https://www.booking.com/search?")
    assert session.commits == 1
    clicks = [item for item in session.added if isinstance(item, AffiliateClick)]
    assert len(clicks) == 1
    assert clicks[0].destination_summary == "東京"
    assert clicks[0].target_host == "www.booking.com"
    assert not any(isinstance(item, UsageLedger) for item in session.added)
    assert "travelers" not in clicks[0].destination_summary

    with pytest.raises(AppError) as replay:
        await affiliate_router.affiliate_clickout(
            "booking",
            token,
            user,
            session,  # type: ignore[arg-type]
        )
    assert replay.value.code == "affiliate_link_expired"


@pytest.mark.asyncio
async def test_clickout_token_is_isolated_between_members(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    settings = Settings(
        airalo_enabled=True,
        airalo_affiliate_url_template="https://www.airalo.com/{destination}?sub={sub_id}",
    )
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused", is_active=True)
    other = User(id=uuid4(), email="other@example.com", password_hash="unused", is_active=True)
    search = SearchRequest(
        id=uuid4(),
        user_id=owner.id,
        status="completed",
        operation="full_trip_search",
        request_json={"destination": "日本"},
    )
    session = AffiliateSession(search)

    async def runtime_settings(_session: object) -> Settings:
        return settings

    monkeypatch.setattr(affiliate_router, "get_redis", lambda: redis)
    monkeypatch.setattr(affiliate_router, "load_runtime_settings", runtime_settings)
    response = await affiliate_router.affiliate_options(
        "connectivity",
        owner,
        session,
        search_id=search.id,  # type: ignore[arg-type]
    )
    token = response.options[0].clickout_url.rsplit("token=", 1)[-1]
    with pytest.raises(AppError) as error:
        await affiliate_router.affiliate_clickout(
            "airalo",
            token,
            other,
            session,  # type: ignore[arg-type]
        )
    assert error.value.code == "affiliate_link_not_found"
    assert session.commits == 0
