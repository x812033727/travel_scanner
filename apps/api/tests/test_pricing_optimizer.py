from decimal import Decimal

import pytest

from app.optimization.engine import TripOptimizer
from app.pricing.engine import Confidence, TotalCostEngine
from app.providers.mock import MockProvider
from app.search.schemas import PropertyType
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


@pytest.mark.asyncio
async def test_optimizer_applies_required_hotel_filters() -> None:
    provider, query = MockProvider(), sample_query()
    query = query.model_copy(
        update={
            "preferences": query.preferences.model_copy(
                update={
                    "hotel_min_rating": 4,
                    "hotel_max_nightly_twd": 6_000,
                    "breakfast_required": True,
                    "refundable_required": True,
                    "max_station_walk_minutes": 5,
                }
            )
        }
    )
    plans = TripOptimizer().optimize(
        query,
        await provider.search_flights(query),
        await provider.search_hotels(query),
        await provider.search_activities(query),
        await provider.search_transport(query),
    )
    hotels = [plan.hotel for plan in plans if plan.hotel]
    assert hotels
    assert all(hotel.rating >= 4 for hotel in hotels)
    assert all(hotel.breakfast_included and hotel.refundable for hotel in hotels)
    assert all(hotel.station_walk_minutes <= 5 for hotel in hotels)
    assert all(
        (hotel.nightly_price or hotel.total_price / hotel.nights) <= 6_000 for hotel in hotels
    )


@pytest.mark.asyncio
async def test_optimizer_keeps_property_type_hard_and_explains_soft_relaxation() -> None:
    provider, query = MockProvider(), sample_query()
    query = query.model_copy(
        update={
            "preferences": query.preferences.model_copy(
                update={
                    "accepted_property_types": [PropertyType.VACATION_RENTAL],
                    "hotel_min_review_score": 9.5,
                    "hotel_min_review_count": 1000,
                }
            )
        }
    )
    plans = TripOptimizer().optimize(
        query,
        await provider.search_flights(query),
        await provider.search_hotels(query),
        await provider.search_activities(query),
        await provider.search_transport(query),
    )
    assert plans
    assert all(plan.hotel and plan.hotel.property_type == "vacation_rental" for plan in plans)
    assert all(any("已放寬" in warning for warning in plan.cons) for plan in plans)


@pytest.mark.asyncio
async def test_optimizer_prioritizes_activities_matching_selected_interests() -> None:
    provider, query = MockProvider(), sample_query()
    query = query.model_copy(
        update={"preferences": query.preferences.model_copy(update={"interests": ["food"]})}
    )
    plans = TripOptimizer().optimize(
        query,
        await provider.search_flights(query),
        await provider.search_hotels(query),
        await provider.search_activities(query),
        await provider.search_transport(query),
    )
    assert plans
    assert all(plan.activity and plan.activity.category == "food" for plan in plans)
    assert all(any("美食偏好" in pro for pro in plan.pros) for plan in plans)


@pytest.mark.asyncio
async def test_optimizer_explains_when_every_plan_exceeds_budget() -> None:
    provider, query = MockProvider(), sample_query()
    query = query.model_copy(
        update={"preferences": query.preferences.model_copy(update={"budget_twd": 1_000})}
    )
    plans = TripOptimizer().optimize(
        query,
        await provider.search_flights(query),
        await provider.search_hotels(query),
        await provider.search_activities(query),
        await provider.search_transport(query),
    )
    assert plans
    assert all(any("超出總預算" in con for con in plan.cons) for plan in plans)
