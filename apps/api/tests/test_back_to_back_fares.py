import json
from datetime import date
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import httpx
import pytest
from fakeredis.aioredis import FakeRedis
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError

from app.config import Settings
from app.crawlers.airlines import AirlineFareCrawlerService, CrawlerError, FetchResult
from app.crawlers.back_to_back import BackToBackFareService, build_fare_queries
from app.crawlers.fx import FxRateError, FxRateProvider
from app.crawlers.schemas import (
    AirlineCode,
    BackToBackFareSearch,
    CabinClass,
    ComparisonMode,
    ComparisonVerdict,
    FareStrategyTotal,
    FareTicketComponent,
    FareTicketRole,
    FxRateSnapshot,
    PublicFareQuote,
    TripDateRange,
)
from app.main import app


def search_request(**overrides: object) -> BackToBackFareSearch:
    values: dict[str, object] = {
        "origin": "TPE",
        "first_destination": "NRT",
        "second_destination": "NRT",
        "first_trip": TripDateRange(
            departure_date=date(2026, 11, 10), return_date=date(2026, 11, 15)
        ),
        "second_trip": TripDateRange(
            departure_date=date(2026, 12, 10), return_date=date(2026, 12, 15)
        ),
        "flex_days": 0,
        "airlines": [AirlineCode.CHINA_AIRLINES],
    }
    values.update(overrides)
    return BackToBackFareSearch.model_validate(values)


def quote(
    airline: AirlineCode,
    origin: str,
    destination: str,
    departure: date,
    returning: date,
    price: str,
    currency: str = "TWD",
) -> PublicFareQuote:
    names = {
        AirlineCode.CHINA_AIRLINES: "中華航空",
        AirlineCode.EVA_AIR: "長榮航空",
        AirlineCode.STARLUX: "星宇航空",
    }
    return PublicFareQuote(
        id=uuid4(),
        airline_code=airline,
        airline_name=names[airline],
        origin=origin,
        destination=destination,
        departure_date=departure,
        return_date=returning,
        trip_type="round_trip",
        cabin_class=CabinClass.ECONOMY,
        total_price=Decimal(price),
        currency=currency,
        source_url="https://example.test/fare",
    )


def fare_row(
    origin: str,
    destination: str,
    departure: str,
    returning: str,
    price: int,
    currency: str,
) -> dict[str, object]:
    return {
        "originAirportCode": origin,
        "destinationAirportCode": destination,
        "departureDate": departure,
        "returnDate": returning,
        "flightType": "ROUND_TRIP",
        "farenetTravelClass": "ECONOMY",
        "currencyCode": currency,
        "totalPrice": price,
        "priceLastSeen": {"value": "3", "unit": "hours"},
    }


def next_data_html(rows: list[dict[str, object]]) -> str:
    payload = {"props": {"pageProps": {"airModule": {"fares": rows}}}}
    return (
        '<html><script id="__NEXT_DATA__" type="application/json">'
        f"{json.dumps(payload)}"
        "</script></html>"
    )


def twd_rate(currency: str, rate: str) -> FxRateSnapshot:
    return FxRateSnapshot(
        base_currency=currency,
        rate=Decimal(rate),
        as_of=date(2026, 8, 30),
        source_url="https://api.frankfurter.dev/v2/rates",
    )


def test_back_to_back_search_requires_strictly_ordered_four_dates() -> None:
    with pytest.raises(ValidationError, match="dates must satisfy"):
        search_request(
            second_trip=TripDateRange(
                departure_date=date(2026, 11, 14),
                return_date=date(2026, 12, 15),
            )
        )


def test_back_to_back_search_accepts_legacy_single_destination() -> None:
    query = BackToBackFareSearch.model_validate(
        {
            "origin": "tpe",
            "destination": "nrt",
            "first_trip": {
                "departure_date": "2026-11-10",
                "return_date": "2026-11-15",
            },
            "second_trip": {
                "departure_date": "2026-12-10",
                "return_date": "2026-12-15",
            },
        }
    )

    assert query.first_destination == query.second_destination == "NRT"
    assert "destination" not in query.model_dump()


def test_build_fare_queries_expands_the_four_ticket_windows() -> None:
    queries = build_fare_queries(search_request())

    assert queries[FareTicketRole.CONVENTIONAL_FIRST].return_date == date(2026, 11, 15)
    assert queries[FareTicketRole.CONVENTIONAL_SECOND].departure_date == date(2026, 12, 10)
    assert queries[FareTicketRole.WRAPPER].return_date == date(2026, 12, 15)
    reverse = queries[FareTicketRole.REVERSE]
    assert (reverse.origin, reverse.destination) == ("NRT", "TPE")
    assert (reverse.departure_date, reverse.return_date) == (
        date(2026, 11, 15),
        date(2026, 12, 10),
    )


def test_different_destinations_only_expand_verifiable_round_trips() -> None:
    queries = build_fare_queries(search_request(second_destination="SEL"))

    assert set(queries) == {
        FareTicketRole.CONVENTIONAL_FIRST,
        FareTicketRole.CONVENTIONAL_SECOND,
    }
    assert queries[FareTicketRole.CONVENTIONAL_FIRST].destination == "NRT"
    assert queries[FareTicketRole.CONVENTIONAL_SECOND].destination == "SEL"


def test_strategy_selection_returns_lowest_mixed_and_same_airline_totals() -> None:
    candidates = {
        FareTicketRole.CONVENTIONAL_FIRST: [
            quote(
                AirlineCode.CHINA_AIRLINES,
                "TPE",
                "NRT",
                date(2026, 11, 10),
                date(2026, 11, 15),
                "10000",
            ),
            quote(
                AirlineCode.STARLUX,
                "TPE",
                "NRT",
                date(2026, 11, 10),
                date(2026, 11, 15),
                "9000",
            ),
        ],
        FareTicketRole.CONVENTIONAL_SECOND: [
            quote(
                AirlineCode.CHINA_AIRLINES,
                "TPE",
                "NRT",
                date(2026, 12, 10),
                date(2026, 12, 15),
                "11000",
            ),
            quote(
                AirlineCode.STARLUX,
                "TPE",
                "NRT",
                date(2026, 12, 10),
                date(2026, 12, 15),
                "13000",
            ),
        ],
        FareTicketRole.WRAPPER: [
            quote(
                AirlineCode.CHINA_AIRLINES,
                "TPE",
                "NRT",
                date(2026, 11, 10),
                date(2026, 12, 15),
                "15000",
            ),
            quote(
                AirlineCode.STARLUX,
                "TPE",
                "NRT",
                date(2026, 11, 10),
                date(2026, 12, 15),
                "14000",
            ),
        ],
        FareTicketRole.REVERSE: [
            quote(
                AirlineCode.CHINA_AIRLINES,
                "NRT",
                "TPE",
                date(2026, 11, 15),
                date(2026, 12, 10),
                "20000",
                "JPY",
            ),
            quote(
                AirlineCode.STARLUX,
                "NRT",
                "TPE",
                date(2026, 11, 15),
                date(2026, 12, 10),
                "24000",
                "JPY",
            ),
        ],
    }
    rates = {"TWD": twd_rate("TWD", "1"), "JPY": twd_rate("JPY", "0.2")}

    mixed_normal = BackToBackFareService._best_strategy(
        FareTicketRole.CONVENTIONAL_FIRST,
        FareTicketRole.CONVENTIONAL_SECOND,
        candidates,
        rates,
        same_airline=False,
        back_to_back=False,
    )
    same_normal = BackToBackFareService._best_strategy(
        FareTicketRole.CONVENTIONAL_FIRST,
        FareTicketRole.CONVENTIONAL_SECOND,
        candidates,
        rates,
        same_airline=True,
        back_to_back=False,
    )
    mixed_reverse = BackToBackFareService._best_strategy(
        FareTicketRole.WRAPPER,
        FareTicketRole.REVERSE,
        candidates,
        rates,
        same_airline=False,
        back_to_back=True,
    )

    assert mixed_normal is not None and mixed_normal.estimated_twd == Decimal("20000")
    assert [ticket.quote.airline_code for ticket in mixed_normal.tickets] == [
        AirlineCode.STARLUX,
        AirlineCode.CHINA_AIRLINES,
    ]
    assert same_normal is not None and same_normal.estimated_twd == Decimal("21000")
    assert mixed_reverse is not None and mixed_reverse.estimated_twd == Decimal("18000")
    comparison = BackToBackFareService._comparison(
        ComparisonMode.MIXED_AIRLINES, mixed_normal, mixed_reverse
    )
    assert comparison.verdict == ComparisonVerdict.BACK_TO_BACK_CHEAPER
    assert comparison.savings_twd == Decimal("2000")
    assert comparison.savings_percent == Decimal("10.0")


def test_comparison_reports_when_conventional_is_cheaper() -> None:
    first_quote = quote(
        AirlineCode.CHINA_AIRLINES,
        "TPE",
        "NRT",
        date(2026, 11, 10),
        date(2026, 11, 15),
        "10000",
    )
    second_quote = quote(
        AirlineCode.CHINA_AIRLINES,
        "TPE",
        "NRT",
        date(2026, 12, 10),
        date(2026, 12, 15),
        "10000",
    )

    def total(amount: str) -> FareStrategyTotal:
        half = Decimal(amount) / 2
        return FareStrategyTotal(
            tickets=[
                FareTicketComponent(
                    role=FareTicketRole.CONVENTIONAL_FIRST,
                    quote=first_quote,
                    estimated_twd=half,
                ),
                FareTicketComponent(
                    role=FareTicketRole.CONVENTIONAL_SECOND,
                    quote=second_quote,
                    estimated_twd=half,
                ),
            ],
            original_currency_totals={"TWD": Decimal(amount)},
            estimated_twd=Decimal(amount),
        )

    comparison = BackToBackFareService._comparison(
        ComparisonMode.SAME_AIRLINE,
        total("20000"),
        total("25000"),
    )
    assert comparison.verdict == ComparisonVerdict.CONVENTIONAL_CHEAPER
    assert comparison.savings_twd == Decimal("-5000")
    assert comparison.savings_percent == Decimal("-25.0")


def test_missing_fx_never_produces_cross_currency_savings() -> None:
    reverse_quote = quote(
        AirlineCode.CHINA_AIRLINES,
        "NRT",
        "TPE",
        date(2026, 11, 15),
        date(2026, 12, 10),
        "20000",
        "JPY",
    )
    component = BackToBackFareService._ticket_component(
        FareTicketRole.REVERSE, reverse_quote, {}
    )
    comparison = BackToBackFareService._comparison(
        ComparisonMode.MIXED_AIRLINES, None, None
    )

    assert component.estimated_twd is None
    assert comparison.verdict == ComparisonVerdict.COMPARISON_UNAVAILABLE
    assert comparison.savings_twd is None


@pytest.mark.asyncio
async def test_service_fetches_two_unique_pages_per_airline_and_reuses_forward_rows() -> None:
    forward_rows = [
        fare_row("TPE", "NRT", "2026-11-10", "2026-11-15", 10_000, "TWD"),
        fare_row("TPE", "NRT", "2026-12-10", "2026-12-15", 11_000, "TWD"),
        fare_row("TPE", "NRT", "2026-11-10", "2026-12-15", 15_000, "TWD"),
    ]
    reverse_rows = [
        fare_row("NRT", "TPE", "2026-11-15", "2026-12-10", 20_000, "JPY")
    ]

    async def fetch_page(_client: httpx.AsyncClient, url: str) -> FetchResult:
        rows = reverse_rows if "from-tokyo-to-taipei" in url else forward_rows
        return FetchResult(next_data_html(rows), cache_hit=False)

    redis = FakeRedis(decode_responses=True)
    settings = Settings(airline_crawler_min_interval_seconds=1)
    crawler = AirlineFareCrawlerService(settings, redis)  # type: ignore[arg-type]
    crawler.fetcher.fetch = AsyncMock(side_effect=fetch_page)  # type: ignore[method-assign]
    fx_provider = AsyncMock()
    fx_provider.rate_to_twd = AsyncMock(
        side_effect=lambda currency: twd_rate(currency, "1" if currency == "TWD" else "0.2")
    )
    service = BackToBackFareService(
        settings,
        redis,  # type: ignore[arg-type]
        crawler=crawler,
        fx_provider=fx_provider,
    )

    response = await service.search(search_request())
    await redis.aclose()

    assert crawler.fetcher.fetch.await_count == 2  # type: ignore[attr-defined]
    assert {call.args[1] for call in crawler.fetcher.fetch.await_args_list} == {  # type: ignore[attr-defined]
        "https://flights.china-airlines.com/en-tw/flights-from-taipei-to-tokyo",
        "https://flights.china-airlines.com/en-tw/flights-from-tokyo-to-taipei",
    }
    counts = {candidate.role: len(candidate.quotes) for candidate in response.candidates}
    assert counts == {role: 1 for role in FareTicketRole}
    assert response.comparisons[0].savings_twd == Decimal("2000")
    assert response.pricing_capability.value == "full_back_to_back"


@pytest.mark.asyncio
async def test_different_destinations_use_two_forward_pages_without_fake_open_jaw() -> None:
    tokyo_rows = [
        fare_row("TPE", "NRT", "2026-11-10", "2026-11-15", 10_000, "TWD")
    ]
    seoul_rows = [
        fare_row("TPE", "ICN", "2026-12-10", "2026-12-15", 8_000, "TWD")
    ]

    async def fetch_page(_client: httpx.AsyncClient, url: str) -> FetchResult:
        rows = seoul_rows if "to-seoul" in url else tokyo_rows
        return FetchResult(next_data_html(rows), cache_hit=False)

    redis = FakeRedis(decode_responses=True)
    settings = Settings(airline_crawler_min_interval_seconds=1)
    crawler = AirlineFareCrawlerService(settings, redis)  # type: ignore[arg-type]
    crawler.fetcher.fetch = AsyncMock(side_effect=fetch_page)  # type: ignore[method-assign]
    fx_provider = AsyncMock()
    fx_provider.rate_to_twd = AsyncMock(side_effect=lambda currency: twd_rate(currency, "1"))
    service = BackToBackFareService(
        settings,
        redis,  # type: ignore[arg-type]
        crawler=crawler,
        fx_provider=fx_provider,
    )

    response = await service.search(search_request(second_destination="SEL"))
    await redis.aclose()

    assert crawler.fetcher.fetch.await_count == 2  # type: ignore[attr-defined]
    assert {call.args[1] for call in crawler.fetcher.fetch.await_args_list} == {  # type: ignore[attr-defined]
        "https://flights.china-airlines.com/en-tw/flights-from-taipei-to-tokyo",
        "https://flights.china-airlines.com/en-tw/flights-from-taipei-to-seoul",
    }
    candidates = {candidate.role: candidate.quotes for candidate in response.candidates}
    assert candidates[FareTicketRole.CONVENTIONAL_FIRST]
    assert candidates[FareTicketRole.CONVENTIONAL_SECOND]
    assert candidates[FareTicketRole.WRAPPER] == []
    assert candidates[FareTicketRole.REVERSE] == []
    assert response.pricing_capability.value == "open_jaw_provider_required"
    assert response.comparisons[0].conventional is not None
    assert response.comparisons[0].conventional.estimated_twd == Decimal("18000")
    assert response.comparisons[0].back_to_back is None
    assert response.comparisons[0].verdict == ComparisonVerdict.COMPARISON_UNAVAILABLE
    assert "開口票" in response.comparisons[0].detail
    assert any("只顯示可驗證的一般買法基準" in warning for warning in response.warnings)


@pytest.mark.asyncio
async def test_reverse_page_failure_keeps_conventional_partial_results() -> None:
    forward_rows = [
        fare_row("TPE", "NRT", "2026-11-10", "2026-11-15", 10_000, "TWD"),
        fare_row("TPE", "NRT", "2026-12-10", "2026-12-15", 11_000, "TWD"),
        fare_row("TPE", "NRT", "2026-11-10", "2026-12-15", 15_000, "TWD"),
    ]

    async def fetch_page(_client: httpx.AsyncClient, url: str) -> FetchResult:
        if "from-tokyo-to-taipei" in url:
            raise CrawlerError("source_unavailable", "外站頁面暫時無法連線")
        return FetchResult(next_data_html(forward_rows), cache_hit=True)

    redis = FakeRedis(decode_responses=True)
    settings = Settings(airline_crawler_min_interval_seconds=1)
    crawler = AirlineFareCrawlerService(settings, redis)  # type: ignore[arg-type]
    crawler.fetcher.fetch = AsyncMock(side_effect=fetch_page)  # type: ignore[method-assign]
    fx_provider = AsyncMock()
    fx_provider.rate_to_twd = AsyncMock(side_effect=lambda currency: twd_rate(currency, "1"))
    service = BackToBackFareService(
        settings,
        redis,  # type: ignore[arg-type]
        crawler=crawler,
        fx_provider=fx_provider,
    )

    response = await service.search(search_request())
    await redis.aclose()

    candidates = {candidate.role: candidate.quotes for candidate in response.candidates}
    assert candidates[FareTicketRole.CONVENTIONAL_FIRST]
    assert candidates[FareTicketRole.CONVENTIONAL_SECOND]
    assert candidates[FareTicketRole.REVERSE] == []
    assert response.sources[0].state.value == "failed"
    assert response.comparisons[0].conventional is not None
    assert response.comparisons[0].back_to_back is None
    assert response.comparisons[0].verdict == ComparisonVerdict.COMPARISON_UNAVAILABLE
    assert any("外站頁面暫時無法連線" in warning for warning in response.warnings)


@pytest.mark.asyncio
async def test_fx_provider_caches_fresh_rate_and_falls_back_to_stale() -> None:
    requests = 0

    def success(_request: httpx.Request) -> httpx.Response:
        nonlocal requests
        requests += 1
        return httpx.Response(
            200,
            json={"date": "2026-08-30", "base": "JPY", "quote": "TWD", "rate": 0.2},
        )

    redis = FakeRedis(decode_responses=True)
    provider = FxRateProvider(
        Settings(), redis, transport=httpx.MockTransport(success)  # type: ignore[arg-type]
    )
    first = await provider.rate_to_twd("JPY")
    second = await provider.rate_to_twd("JPY")
    assert first.rate == second.rate == Decimal("0.2")
    assert requests == 1

    await redis.delete("fx:frankfurter:JPY:TWD:fresh")
    provider.transport = httpx.MockTransport(lambda _request: httpx.Response(503))
    stale = await provider.rate_to_twd("JPY")
    await redis.aclose()
    assert stale.is_stale is True
    assert stale.rate == Decimal("0.2")


@pytest.mark.asyncio
async def test_fx_provider_raises_when_no_fresh_or_stale_rate_exists() -> None:
    redis = FakeRedis(decode_responses=True)
    provider = FxRateProvider(
        Settings(),
        redis,  # type: ignore[arg-type]
        transport=httpx.MockTransport(lambda _request: httpx.Response(503)),
    )
    with pytest.raises(FxRateError, match="無法取得"):
        await provider.rate_to_twd("JPY")
    await redis.aclose()


@pytest.mark.asyncio
async def test_back_to_back_endpoint_requires_authentication() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/crawlers/airlines/back-to-back-fares",
            json=search_request().model_dump(mode="json"),
        )
    assert response.status_code == 401
    assert response.json()["code"] == "authentication_required"
