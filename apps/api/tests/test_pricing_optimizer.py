from decimal import Decimal

import pytest

from app.optimization.engine import TripOptimizer
from app.pricing.engine import Confidence, TotalCostEngine
from app.providers.mock import MockProvider
from tests.test_mock_providers import sample_query


@pytest.mark.asyncio
async def test_total_cost_separates_confirmed_and_estimated() -> None:
    provider, query = MockProvider(), sample_query()
    flight = (await provider.search_flights(query))[0]
    hotel = (await provider.search_hotels(query))[0]
    activity = (await provider.search_activities(query))[0]
    transport = (await provider.search_transport(query))[0]
    total = TotalCostEngine().calculate(flight, hotel, activity, transport, 2)
    assert total.total_cost == total.confirmed_cost + total.estimated_cost
    assert total.estimated_cost > Decimal(0)
    assert any(part.confidence == Confidence.ESTIMATED for part in total.components)


@pytest.mark.asyncio
async def test_optimizer_returns_three_profiles_and_true_cheapest() -> None:
    provider, query = MockProvider(), sample_query()
    plans = TripOptimizer().optimize(
        query,
        await provider.search_flights(query),
        await provider.search_hotels(query),
        await provider.search_activities(query),
        await provider.search_transport(query),
    )
    assert [plan.mode for plan in plans] == ["balanced", "cheapest", "comfortable"]
    cheapest = plans[1].total_cost.total_cost
    assert all(cheapest <= plan.total_cost.total_cost for plan in plans)
    assert plans[0].score.solver in {"or-tools-cp-sat", "beam-fallback"}
