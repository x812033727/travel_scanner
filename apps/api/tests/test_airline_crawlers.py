import json
from datetime import UTC, date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock

import httpx
import pytest
from fakeredis.aioredis import FakeRedis
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError

from app.config import Settings
from app.crawlers.airlines import (
    AirlineFareCrawlerService,
    CrawlerError,
    CrawlerPolicyError,
    RobotsAwareFetcher,
    parse_public_fares,
)
from app.crawlers.schemas import (
    AirlineBrowserCapture,
    AirlineCode,
    AirlineCrawlerSource,
    AirlineFareSearch,
    AirlineFareSearchResponse,
    CabinClass,
    SourceState,
)
from app.crawlers.verification import VerificationOutcome, build_verification_report
from app.main import app


def next_data_html(rows: list[dict[str, object]]) -> str:
    payload = {"props": {"pageProps": {"components": [{"airModule": {"fares": rows}}]}}}
    return (
        '<html><script id="__NEXT_DATA__" type="application/json">'
        f"{json.dumps(payload)}"
        "</script></html>"
    )


def fare_row(
    *,
    departure: str,
    returning: str,
    price: int,
    cabin: str = "ECONOMY",
    destination: str = "NRT",
) -> dict[str, object]:
    return {
        "originAirportCode": "TPE",
        "destinationAirportCode": destination,
        "departureDate": departure,
        "returnDate": returning,
        "flightType": "ROUND_TRIP",
        "farenetTravelClass": cabin,
        "currencyCode": "TWD",
        "totalPrice": price,
        "priceLastSeen": {"value": "3", "unit": "hours"},
    }


def test_parser_normalizes_filters_sorts_and_deduplicates_public_fares() -> None:
    rows = [
        fare_row(departure="2026-11-12", returning="2026-11-17", price=12_500),
        fare_row(departure="2026-11-10", returning="2026-11-15", price=13_000),
        fare_row(departure="2026-11-10", returning="2026-11-15", price=13_000),
        fare_row(
            departure="2026-11-10",
            returning="2026-11-15",
            price=40_000,
            cabin="BUSINESS",
        ),
        fare_row(
            departure="2026-12-20",
            returning="2026-12-25",
            price=9_000,
        ),
    ]
    query = AirlineFareSearch(
        destination="NRT",
        departure_date=date(2026, 11, 10),
        return_date=date(2026, 11, 15),
        flex_days=3,
        airlines=[AirlineCode.CHINA_AIRLINES],
    )

    quotes = parse_public_fares(
        next_data_html(rows),
        airline_code=AirlineCode.CHINA_AIRLINES,
        airline_name="中華航空",
        source_url="https://flights.china-airlines.com/example",
        query=query,
    )

    assert len(quotes) == 2
    assert quotes[0].departure_date == date(2026, 11, 10)
    assert quotes[0].total_price == Decimal("13000")
    assert quotes[0].price_last_seen == "3 hours ago"
    assert quotes[0].cabin_class == CabinClass.ECONOMY
    assert quotes[0].is_live is False
    assert quotes[0].is_bookable is False
    assert quotes[0].is_mock is False


def test_parser_supports_city_airport_groups() -> None:
    query = AirlineFareSearch(destination="TYO", limit_per_airline=5)
    rows = [
        fare_row(departure="2026-11-10", returning="2026-11-15", price=13_000),
        fare_row(
            departure="2026-11-11",
            returning="2026-11-16",
            price=14_000,
            destination="HND",
        ),
    ]
    quotes = parse_public_fares(
        next_data_html(rows),
        airline_code=AirlineCode.STARLUX,
        airline_name="星宇航空",
        source_url="https://www.starlux-airlines.com/example",
        query=query,
    )
    assert {quote.destination for quote in quotes} == {"NRT", "HND"}


def test_parser_fails_clearly_when_page_contract_changes() -> None:
    with pytest.raises(CrawlerError, match="結構化資料"):
        parse_public_fares(
            "<html><body>changed</body></html>",
            airline_code=AirlineCode.STARLUX,
            airline_name="星宇航空",
            source_url="https://www.starlux-airlines.com/example",
            query=AirlineFareSearch(destination="NRT"),
        )


@pytest.mark.asyncio
async def test_crawler_status_documents_eva_fail_closed() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/crawlers/airlines/status")
    assert response.status_code == 200
    sources = {source["airline_code"]: source for source in response.json()["sources"]}
    assert sources["CI"]["state"] == "ready"
    assert sources["JX"]["state"] == "ready"
    assert sources["BR"]["state"] == "disabled"
    assert "robots.txt" in sources["BR"]["detail"]


@pytest.mark.asyncio
async def test_crawler_search_requires_authentication() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/crawlers/airlines/fares",
            json={"origin": "TPE", "destination": "NRT"},
        )
    assert response.status_code == 401
    assert response.json()["code"] == "authentication_required"


@pytest.mark.asyncio
async def test_browser_bridge_requires_authentication() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        targets = await client.post(
            "/api/v1/crawlers/airlines/browser-targets",
            json={"origin": "TPE", "destination": "NRT"},
        )
        capture = await client.post(
            "/api/v1/crawlers/airlines/browser-captures",
            json={},
        )
    assert targets.status_code == 401
    assert capture.status_code == 401


@pytest.mark.asyncio
async def test_fetcher_checks_robots_and_caches_allowed_page() -> None:
    requests: list[str] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        requests.append(url)
        if url.endswith("/robots.txt"):
            return httpx.Response(200, text="User-agent: *\nAllow: /\n")
        return httpx.Response(200, text="<html>fare page</html>")

    redis = FakeRedis(decode_responses=True)
    fetcher = RobotsAwareFetcher(Settings(), redis)  # type: ignore[arg-type]
    url = "https://flights.china-airlines.com/en-tw/flights-from-taipei-to-tokyo"
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        first = await fetcher.fetch(client, url)
        second = await fetcher.fetch(client, url)
    await redis.aclose()

    assert first.cache_hit is False
    assert second.cache_hit is True
    assert first.content == second.content
    assert requests == ["https://flights.china-airlines.com/robots.txt", url]


@pytest.mark.asyncio
async def test_fetcher_follows_same_host_https_redirect_after_robots_check() -> None:
    requests: list[str] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        requests.append(url)
        if url.endswith("/robots.txt"):
            return httpx.Response(200, text="User-agent: *\nAllow: /\n")
        if "/en-tw/" in url:
            return httpx.Response(
                301,
                headers={
                    "location": "https://www.starlux-airlines.com/flights/en/"
                    "flights-from-tokyo-to-taipei"
                },
            )
        return httpx.Response(200, text="<html>reverse fare page</html>")

    redis = FakeRedis(decode_responses=True)
    fetcher = RobotsAwareFetcher(Settings(), redis)  # type: ignore[arg-type]
    url = "https://www.starlux-airlines.com/flights/en-tw/flights-from-tokyo-to-taipei"
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await fetcher.fetch(client, url)
    await redis.aclose()

    assert result.content == "<html>reverse fare page</html>"
    assert requests == [
        "https://www.starlux-airlines.com/robots.txt",
        url,
        "https://www.starlux-airlines.com/flights/en/flights-from-tokyo-to-taipei",
    ]


@pytest.mark.asyncio
async def test_fetcher_rejects_cross_host_redirect() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url).endswith("/robots.txt"):
            return httpx.Response(200, text="User-agent: *\nAllow: /\n")
        return httpx.Response(301, headers={"location": "https://example.com/fare"})

    redis = FakeRedis(decode_responses=True)
    fetcher = RobotsAwareFetcher(Settings(), redis)  # type: ignore[arg-type]
    url = "https://www.starlux-airlines.com/flights/en-tw/flights-from-tokyo-to-taipei"
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(CrawlerPolicyError, match="離開允許"):
            await fetcher.fetch(client, url)
    await redis.aclose()


@pytest.mark.asyncio
async def test_fetcher_fails_closed_when_robots_disallows_page() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        _ = request
        return httpx.Response(200, text="User-agent: *\nDisallow: /en-tw\n")

    redis = FakeRedis(decode_responses=True)
    fetcher = RobotsAwareFetcher(Settings(), redis)  # type: ignore[arg-type]
    url = "https://flights.china-airlines.com/en-tw/flights-from-taipei-to-tokyo"
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(CrawlerPolicyError, match="不允許"):
            await fetcher.fetch(client, url)
    await redis.aclose()


@pytest.mark.asyncio
async def test_browser_targets_keep_eva_disabled_and_authorize_enabled_sources() -> None:
    redis = FakeRedis(decode_responses=True)
    service = AirlineFareCrawlerService(Settings(), redis)  # type: ignore[arg-type]
    service.fetcher.authorize = AsyncMock()  # type: ignore[method-assign]
    response = await service.browser_targets(
        AirlineFareSearch(destination="NRT"), force_refresh=True
    )
    await redis.aclose()

    targets = {target.airline_code: target for target in response.targets}
    assert targets[AirlineCode.CHINA_AIRLINES].source_url == (
        "https://flights.china-airlines.com/en-tw/flights-from-taipei-to-tokyo"
    )
    assert targets[AirlineCode.STARLUX].state == SourceState.READY
    assert targets[AirlineCode.EVA_AIR].state == SourceState.DISABLED
    assert targets[AirlineCode.EVA_AIR].source_url is None
    assert service.fetcher.authorize.await_count == 2  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_browser_capture_uses_existing_normalizer_and_records_digest() -> None:
    query = AirlineFareSearch(
        destination="NRT",
        departure_date=date(2026, 11, 10),
        return_date=date(2026, 11, 15),
        flex_days=0,
        airlines=[AirlineCode.STARLUX],
    )
    rows = [fare_row(departure="2026-11-10", returning="2026-11-15", price=14_075)]
    capture = AirlineBrowserCapture(
        airline_code=AirlineCode.STARLUX,
        query=query,
        source_url="https://www.starlux-airlines.com/flights/en-tw/flights-from-taipei-to-tokyo",
        page_title="Flights from Taipei to Tokyo - STARLUX Airlines",
        captured_at=datetime.now(UTC),
        fare_rows=rows,
    )
    redis = FakeRedis(decode_responses=True)
    service = AirlineFareCrawlerService(Settings(), redis)  # type: ignore[arg-type]
    service.fetcher.authorize = AsyncMock()  # type: ignore[method-assign]
    response = await service.parse_browser_capture(capture)
    await redis.aclose()

    assert len(response.quotes) == 1
    assert response.quotes[0].total_price == Decimal("14075")
    assert response.quotes[0].is_live is False
    assert response.sources[0].policy == "browser_capture_allowlisted_robots_checked"
    assert len(response.capture_sha256) == 64


@pytest.mark.asyncio
async def test_browser_capture_rejects_non_allowlisted_page_and_disabled_adapter() -> None:
    query = AirlineFareSearch(destination="NRT", airlines=[AirlineCode.CHINA_AIRLINES])
    rows: list[dict[str, object]] = []
    redis = FakeRedis(decode_responses=True)
    service = AirlineFareCrawlerService(Settings(), redis)  # type: ignore[arg-type]

    with pytest.raises(CrawlerPolicyError, match="不符"):
        await service.parse_browser_capture(
            AirlineBrowserCapture(
                airline_code=AirlineCode.CHINA_AIRLINES,
                query=query,
                source_url="https://flights.china-airlines.com/en-tw/flights-from-taipei-to-osaka",
                fare_rows=rows,
            )
        )
    with pytest.raises(CrawlerPolicyError, match="robots.txt"):
        await service.parse_browser_capture(
            AirlineBrowserCapture(
                airline_code=AirlineCode.EVA_AIR,
                query=AirlineFareSearch(destination="NRT", airlines=[AirlineCode.EVA_AIR]),
                source_url="https://flights.evaair.com/en-tw/flights-from-taipei-to-tokyo",
                fare_rows=rows,
            )
        )
    await redis.aclose()


def test_browser_capture_rejects_fields_outside_the_public_fare_allowlist() -> None:
    with pytest.raises(ValidationError, match="bookingUrl"):
        AirlineBrowserCapture(
            airline_code=AirlineCode.CHINA_AIRLINES,
            query=AirlineFareSearch(destination="NRT"),
            source_url="https://flights.china-airlines.com/en-tw/flights-from-taipei-to-tokyo",
            fare_rows=[
                {
                    **fare_row(departure="2026-11-10", returning="2026-11-15", price=13_000),
                    "bookingUrl": "https://booking.example/private",
                }
            ],
        )


def test_verification_accepts_expected_disabled_source() -> None:
    query = AirlineFareSearch(destination="NRT")
    response = AirlineFareSearchResponse(
        quotes=[],
        warnings=[],
        sources=[
            AirlineCrawlerSource(
                airline_code=AirlineCode.CHINA_AIRLINES,
                airline_name="中華航空",
                host="flights.china-airlines.com",
                state=SourceState.SUCCESS,
                policy="robots_allowed",
                detail="ok",
                quote_count=2,
            ),
            AirlineCrawlerSource(
                airline_code=AirlineCode.EVA_AIR,
                airline_name="長榮航空",
                host="flights.evaair.com",
                state=SourceState.DISABLED,
                policy="fail_closed",
                detail="expected",
            ),
            AirlineCrawlerSource(
                airline_code=AirlineCode.STARLUX,
                airline_name="星宇航空",
                host="www.starlux-airlines.com",
                state=SourceState.SUCCESS,
                policy="robots_allowed",
                detail="ok",
                quote_count=2,
            ),
        ],
    )
    report = build_verification_report(query, response)
    assert report.passed is True
    outcomes = {source.airline_code: source.outcome for source in report.sources}
    assert outcomes[AirlineCode.EVA_AIR] == VerificationOutcome.EXPECTED_DISABLED


def test_verification_fails_when_required_source_has_no_quotes() -> None:
    query = AirlineFareSearch(destination="NRT", airlines=[AirlineCode.STARLUX])
    response = AirlineFareSearchResponse(
        quotes=[],
        warnings=["no fares"],
        sources=[
            AirlineCrawlerSource(
                airline_code=AirlineCode.STARLUX,
                airline_name="星宇航空",
                host="www.starlux-airlines.com",
                state=SourceState.SUCCESS,
                policy="robots_allowed",
                detail="no matching quote",
                quote_count=0,
            )
        ],
    )
    report = build_verification_report(query, response)
    assert report.passed is False
    assert report.sources[0].outcome == VerificationOutcome.FAILED


def test_verification_fails_when_required_source_is_missing() -> None:
    query = AirlineFareSearch(destination="NRT", airlines=[AirlineCode.STARLUX])
    response = AirlineFareSearchResponse(quotes=[], warnings=[], sources=[])
    report = build_verification_report(query, response)
    assert report.passed is False
    assert report.sources[0].airline_code == AirlineCode.STARLUX
    assert report.sources[0].outcome == VerificationOutcome.FAILED
