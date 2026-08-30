from datetime import date

import pytest

from app.providers.mock import MockProvider
from app.search.schemas import SearchCreate


def sample_query() -> SearchCreate:
    return SearchCreate(
        origin="TPE",
        destination="NRT",
        departure_date=date(2026, 11, 10),
        return_date=date(2026, 11, 15),
        modules=["flight", "hotel", "activities", "transport"],
        preferences={"avoid_red_eye": True, "hotel_min_rating": 4, "optimization_mode": "balanced"},
    )


@pytest.mark.asyncio
async def test_mock_offers_are_deterministic() -> None:
    first = await MockProvider().search_flights(sample_query())
    second = await MockProvider().search_flights(sample_query())
    assert [offer.id for offer in first] == [offer.id for offer in second]
    assert all(offer.is_mock and offer.currency == "TWD" for offer in first)


@pytest.mark.asyncio
async def test_all_mock_modules_produce_offers() -> None:
    provider, query = MockProvider(), sample_query()
    assert len(await provider.search_flights(query)) >= 3
    assert len(await provider.search_hotels(query)) >= 3
    assert await provider.search_activities(query)
    assert await provider.search_transport(query)
