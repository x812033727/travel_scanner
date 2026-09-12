"""The per-source bound on public catalogue reads.

Built on a bare Starlette app rather than the real one so the middleware is the only
thing under test, following `test_auth_hardening.py`'s body-limit case.

The window counter is stood in for rather than faked at the Redis level: `fakeredis`
has no Lua, and the Lua is unchanged code the auth suite already drives against a real
Redis. What is new, and what these cases are about, is which requests get counted at
all and what happens to one that is over. The two places where Redis' own behaviour is
the subject -- fail open here, fail closed for auth -- are tested directly at the end.
"""

from collections.abc import AsyncIterator, Iterator

import pytest
from httpx import ASGITransport, AsyncClient
from redis.exceptions import RedisError
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

import app.infra as infra
import app.middleware as middleware
from app.config import get_settings
from app.middleware import PublicReadRateLimitMiddleware
from app.problems import AppError, app_error_handler

FORWARDED = {"X-Travel-Client-IP": "203.0.113.9"}
MINUTE_LIMIT = 10


async def _read(_request: Request) -> PlainTextResponse:
    return PlainTextResponse("catalogue")


@pytest.fixture
def counted(monkeypatch: pytest.MonkeyPatch) -> dict[str, int]:
    """Every window the middleware charged, keyed the way it keyed it."""
    counts: dict[str, int] = {}

    async def over(
        namespace: str, identifier: str, *, limit: int, window_seconds: int
    ) -> bool:
        key = f"{namespace}:{identifier}"
        counts[key] = counts.get(key, 0) + 1
        return counts[key] > limit

    monkeypatch.setattr(middleware, "over_named_rate_limit", over)
    return counts


@pytest.fixture
def recorded(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    hits: list[str] = []

    async def record(namespace: str, identifier: str) -> None:
        hits.append(f"{namespace}:{identifier}")

    monkeypatch.setattr(middleware, "record_rate_limit_hit", record)
    return hits


@pytest.fixture
def limited_app(monkeypatch: pytest.MonkeyPatch) -> Iterator[Starlette]:
    monkeypatch.setenv("TRUST_PROXY_CLIENT_IP", "true")
    monkeypatch.setenv("PUBLIC_READ_RATE_LIMIT_MODE", "enforce")
    monkeypatch.setenv("PUBLIC_READ_IP_LIMIT", str(MINUTE_LIMIT))
    monkeypatch.setenv("PUBLIC_READ_IP_HOUR_LIMIT", "60")
    get_settings.cache_clear()
    application = Starlette(
        routes=[
            Route("/api/v1/foods/categories", _read, methods=["GET"]),
            Route("/api/v1/foods/merchants", _read, methods=["POST"]),
            Route("/health", _read, methods=["GET"]),
        ]
    )
    application.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    application.add_middleware(PublicReadRateLimitMiddleware)
    yield application
    get_settings.cache_clear()


async def _client(application: Starlette) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=application), base_url="http://test"
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_refuses_a_source_past_the_window_with_a_retry_hint(
    limited_app: Starlette, counted: dict[str, int], recorded: list[str]
) -> None:
    async for client in _client(limited_app):
        allowed = [
            (await client.get("/api/v1/foods/categories", headers=FORWARDED)).status_code
            for _ in range(MINUTE_LIMIT)
        ]
        refused = await client.get("/api/v1/foods/categories", headers=FORWARDED)

    assert allowed == [200] * MINUTE_LIMIT
    assert refused.status_code == 429
    assert refused.json()["code"] == "rate_limit_exceeded"
    # Without this a well-behaved client has nothing to time its retry against.
    assert refused.headers["Retry-After"] == "60"
    assert recorded == ["public-read-ip:203.0.113.9"]


@pytest.mark.asyncio
async def test_retry_hint_names_the_window_that_is_actually_spent(
    limited_app: Starlette, counted: dict[str, int], recorded: list[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Pointing at the burst window while the hour is gone just earns a second refusal."""
    # Room to spare per minute, so the hourly window is the only one that can trip.
    monkeypatch.setenv("PUBLIC_READ_IP_LIMIT", "500")
    monkeypatch.setenv("PUBLIC_READ_IP_WINDOW_SECONDS", "120")
    monkeypatch.setenv("PUBLIC_READ_IP_HOUR_LIMIT", "60")
    get_settings.cache_clear()
    async for client in _client(limited_app):
        for _ in range(60):
            await client.get("/api/v1/foods/categories", headers=FORWARDED)
        refused = await client.get("/api/v1/foods/categories", headers=FORWARDED)

    assert refused.status_code == 429
    assert refused.headers["Retry-After"] == "3600"


@pytest.mark.asyncio
async def test_retry_hint_follows_the_configured_burst_window(
    limited_app: Starlette, counted: dict[str, int], recorded: list[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PUBLIC_READ_IP_WINDOW_SECONDS", "120")
    get_settings.cache_clear()
    async for client in _client(limited_app):
        for _ in range(MINUTE_LIMIT):
            await client.get("/api/v1/foods/categories", headers=FORWARDED)
        refused = await client.get("/api/v1/foods/categories", headers=FORWARDED)

    assert refused.status_code == 429
    assert refused.headers["Retry-After"] == "120"


@pytest.mark.asyncio
async def test_charges_both_windows_even_once_one_is_spent(
    limited_app: Starlette, counted: dict[str, int], recorded: list[str]
) -> None:
    """The hourly figure has to stay honest about what a source actually asked for.

    Short-circuiting the second window the moment the first is spent would under-report
    exactly the sustained crawl the hourly window exists to catch.
    """
    async for client in _client(limited_app):
        for _ in range(MINUTE_LIMIT + 5):
            await client.get("/api/v1/foods/categories", headers=FORWARDED)

    assert counted["public-read-ip-minute:203.0.113.9"] == MINUTE_LIMIT + 5
    assert counted["public-read-ip-hour:203.0.113.9"] == MINUTE_LIMIT + 5


@pytest.mark.asyncio
async def test_never_limits_a_request_that_forwarded_no_address(
    limited_app: Starlette, counted: dict[str, int], recorded: list[str]
) -> None:
    """Server rendering reaches the API directly, without the BFF's forwarded address.

    Counting those would file every visitor's page render under the web container's own
    address, and the site would take itself down the moment anyone browsed quickly.
    """
    async for client in _client(limited_app):
        statuses = [
            (await client.get("/api/v1/foods/categories")).status_code for _ in range(40)
        ]

    assert statuses == [200] * 40
    assert counted == {}


@pytest.mark.asyncio
async def test_leaves_writes_and_unversioned_paths_alone(
    limited_app: Starlette, counted: dict[str, int], recorded: list[str]
) -> None:
    async for client in _client(limited_app):
        writes = [
            (await client.post("/api/v1/foods/merchants", headers=FORWARDED)).status_code
            for _ in range(20)
        ]
        health = [
            (await client.get("/health", headers=FORWARDED)).status_code for _ in range(20)
        ]

    assert writes == [200] * 20
    assert health == [200] * 20
    assert counted == {}


@pytest.mark.asyncio
async def test_ignores_a_forwarded_address_we_are_not_configured_to_believe(
    limited_app: Starlette, counted: dict[str, int], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Anyone can send the header. It only means something behind our own proxy."""
    monkeypatch.setenv("TRUST_PROXY_CLIENT_IP", "false")
    get_settings.cache_clear()
    async for client in _client(limited_app):
        statuses = [
            (await client.get("/api/v1/foods/categories", headers=FORWARDED)).status_code
            for _ in range(30)
        ]

    assert statuses == [200] * 30
    assert counted == {}


@pytest.mark.asyncio
async def test_believes_a_forwarded_address_carrying_our_proxy_token(
    limited_app: Starlette, counted: dict[str, int], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("INTERNAL_PROXY_TOKEN", "shared-secret")
    get_settings.cache_clear()
    async for client in _client(limited_app):
        await client.get(
            "/api/v1/foods/categories",
            headers={**FORWARDED, "X-Travel-Proxy-Token": "shared-secret"},
        )

    assert counted["public-read-ip-minute:203.0.113.9"] == 1


@pytest.mark.asyncio
async def test_ignores_a_forwarded_address_without_the_proxy_token(
    limited_app: Starlette, counted: dict[str, int], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Nothing at the network layer separates our BFF from anything else on the bridge.

    Both Compose files declare no networks, so container addresses are dynamic and the whole
    subnet is one trust domain. The token is what actually distinguishes the two.
    """
    monkeypatch.setenv("INTERNAL_PROXY_TOKEN", "shared-secret")
    get_settings.cache_clear()
    async for client in _client(limited_app):
        forged = [
            (await client.get("/api/v1/foods/categories", headers=FORWARDED)).status_code
            for _ in range(30)
        ]
        wrong = await client.get(
            "/api/v1/foods/categories",
            headers={**FORWARDED, "X-Travel-Proxy-Token": "guessed"},
        )

    assert forged == [200] * 30
    assert wrong.status_code == 200
    assert counted == {}


@pytest.mark.asyncio
async def test_an_unset_token_keeps_the_previous_behaviour(
    limited_app: Starlette, counted: dict[str, int]
) -> None:
    """Back-compatibility is the point, not an oversight.

    A token configured on the API but not yet on the web container would stop every
    forwarded address being believed at once, collapsing all visitors into the web
    container's single bucket -- an outage wearing a security feature's clothes.
    """
    async for client in _client(limited_app):
        await client.get("/api/v1/foods/categories", headers=FORWARDED)

    assert counted["public-read-ip-minute:203.0.113.9"] == 1


@pytest.mark.asyncio
async def test_counts_each_source_separately(
    limited_app: Starlette, counted: dict[str, int], recorded: list[str]
) -> None:
    async for client in _client(limited_app):
        for _ in range(MINUTE_LIMIT + 1):
            await client.get("/api/v1/foods/categories", headers=FORWARDED)
        neighbour = await client.get(
            "/api/v1/foods/categories", headers={"X-Travel-Client-IP": "198.51.100.8"}
        )

    assert neighbour.status_code == 200


@pytest.mark.asyncio
async def test_observe_mode_counts_and_records_without_refusing(
    limited_app: Starlette,
    counted: dict[str, int],
    recorded: list[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PUBLIC_READ_RATE_LIMIT_MODE", "observe")
    get_settings.cache_clear()
    async for client in _client(limited_app):
        statuses = [
            (await client.get("/api/v1/foods/categories", headers=FORWARDED)).status_code
            for _ in range(MINUTE_LIMIT + 5)
        ]

    assert statuses == [200] * (MINUTE_LIMIT + 5)
    # The record is the whole point of the mode: the threshold is argued from it.
    assert recorded == ["public-read-ip:203.0.113.9"] * 5


@pytest.mark.asyncio
async def test_off_mode_does_not_count_at_all(
    limited_app: Starlette,
    counted: dict[str, int],
    recorded: list[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PUBLIC_READ_RATE_LIMIT_MODE", "off")
    get_settings.cache_clear()
    async for client in _client(limited_app):
        statuses = [
            (await client.get("/api/v1/foods/categories", headers=FORWARDED)).status_code
            for _ in range(20)
        ]

    assert statuses == [200] * 20
    assert counted == {}
    assert recorded == []


@pytest.mark.asyncio
async def test_public_reads_fail_open_when_redis_is_unreachable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A public page going dark because Redis blinked is the worse failure.

    An uncounted read costs us the length of the blink; a 503 on the catalogue costs
    every reader and every crawler at once.
    """

    class Unreachable:
        async def eval(self, *_args: object, **_kwargs: object) -> int:
            raise RedisError("down")

    monkeypatch.setattr(infra, "get_redis", Unreachable)
    assert (
        await infra.over_named_rate_limit("public-read-ip", "x", limit=1, window_seconds=60)
        is False
    )


@pytest.mark.asyncio
async def test_guarded_endpoints_still_fail_closed_when_redis_is_unreachable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The opposite call, on the same counter. Losing the login guard is not a shrug."""

    class Unreachable:
        async def eval(self, *_args: object, **_kwargs: object) -> int:
            raise RedisError("down")

    monkeypatch.setattr(infra, "get_redis", Unreachable)
    with pytest.raises(AppError) as refusal:
        await infra.enforce_named_rate_limit("auth-login-ip", "x", limit=1, window_seconds=60)
    assert refusal.value.status == 503
    assert refusal.value.code == "rate_limit_unavailable"
