from datetime import date, timedelta

import httpx
import pytest

from app.hotspots.wikimedia import WikimediaPageviewClient


@pytest.mark.asyncio
async def test_wikimedia_client_compares_two_complete_thirty_day_windows() -> None:
    start = date(2026, 7, 2)
    items = [
        {
            "timestamp": f"{start + timedelta(days=index):%Y%m%d}00",
            "views": 10 if index < 30 else 20,
        }
        for index in range(60)
    ]

    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["User-Agent"] == "TravelScannerBot/0.1 (test@example.com)"
        assert "Tokyo_Skytree" in str(request.url)
        return httpx.Response(200, json={"items": items})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    collector = WikimediaPageviewClient(
        "TravelScannerBot/0.1 (test@example.com)",
        client=client,
    )
    result = await collector.pageviews(
        "en.wikipedia.org",
        "Tokyo Skytree",
        observed_on=date(2026, 8, 30),
    )
    await client.aclose()

    assert result.previous == 300
    assert result.current == 600
    assert result.observed_on == date(2026, 8, 30)


@pytest.mark.asyncio
async def test_wikimedia_client_retries_after_rate_limit(monkeypatch) -> None:
    attempts = 0
    slept: list[float] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            return httpx.Response(429, headers={"Retry-After": "2"})
        return httpx.Response(200, json={"items": []})

    async def fake_sleep(delay: float) -> None:
        slept.append(delay)

    monkeypatch.setattr("app.hotspots.wikimedia.asyncio.sleep", fake_sleep)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    collector = WikimediaPageviewClient(
        "TravelScannerBot/0.1 (test@example.com)",
        client=client,
        retry_backoff_seconds=1.0,
    )
    result = await collector.pageviews(
        "en.wikipedia.org",
        "Tokyo Skytree",
        observed_on=date(2026, 8, 30),
    )
    await client.aclose()

    assert attempts == 3
    assert slept == [2.0, 2.0]
    assert result.current == 0


@pytest.mark.asyncio
async def test_wikimedia_client_backs_off_exponentially_without_retry_after(monkeypatch) -> None:
    slept: list[float] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429)

    async def fake_sleep(delay: float) -> None:
        slept.append(delay)

    monkeypatch.setattr("app.hotspots.wikimedia.asyncio.sleep", fake_sleep)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    collector = WikimediaPageviewClient(
        "TravelScannerBot/0.1 (test@example.com)",
        client=client,
        max_retries=2,
        retry_backoff_seconds=1.0,
    )
    with pytest.raises(httpx.HTTPStatusError):
        await collector.pageviews(
            "en.wikipedia.org",
            "Tokyo Skytree",
            observed_on=date(2026, 8, 30),
        )
    await client.aclose()

    # Two retries, each waiting longer than the last, jitter included.
    assert len(slept) == 2
    assert 1.0 <= slept[0] < 1.25
    assert 2.0 <= slept[1] < 2.5


@pytest.mark.asyncio
async def test_wikimedia_client_does_not_retry_not_found(monkeypatch) -> None:
    attempts = 0

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(404)

    async def fail_sleep(delay: float) -> None:
        raise AssertionError("404 must not be retried")

    monkeypatch.setattr("app.hotspots.wikimedia.asyncio.sleep", fail_sleep)
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    collector = WikimediaPageviewClient(
        "TravelScannerBot/0.1 (test@example.com)",
        client=client,
    )
    with pytest.raises(httpx.HTTPStatusError):
        await collector.pageviews(
            "en.wikipedia.org",
            "Missing Page",
            observed_on=date(2026, 8, 30),
        )
    await client.aclose()

    assert attempts == 1


def test_hotspot_catalog_has_stable_unique_identifiers() -> None:
    from app.hotspots.catalog import HOTSPOT_SEEDS

    assert len(HOTSPOT_SEEDS) == 265
    assert len({item.slug for item in HOTSPOT_SEEDS}) == len(HOTSPOT_SEEDS)
    assert len({item.wikidata_item_id for item in HOTSPOT_SEEDS}) == len(HOTSPOT_SEEDS)
    assert {item.country_code for item in HOTSPOT_SEEDS} == {
        "JP",
        "KR",
        "TH",
        "TW",
        "SG",
        "HK",
        "VN",
    }
    city_counts = {
        city: sum(seed.city_code == city for seed in HOTSPOT_SEEDS)
        for city in {seed.city_code for seed in HOTSPOT_SEEDS}
    }
    assert len(city_counts) == 19
    assert min(city_counts.values()) >= 13
