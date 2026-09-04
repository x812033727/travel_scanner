from typing import Any, cast

import pytest
from fastapi import Request
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.places.router import DiscoveryRequest, LodgingPreferences, discover


def _http_request() -> Request:
    return Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/",
            "headers": [],
            "client": ("198.51.100.7", 1),
        }
    )


def _no_session() -> AsyncSession:
    """This payload carries no notes, so discover never touches the session."""
    return cast(AsyncSession, cast(Any, None))


@pytest.mark.asyncio
async def test_guided_discovery_returns_three_deterministic_candidates() -> None:
    request = DiscoveryRequest.model_validate(
        {
            "origin": "TPE",
            "destination_region": None,
            "destination_countries": ["JP", "KR", "TH"],
            "travel_window": {"start_date": "2027-02-01", "end_date": "2027-04-30"},
            "trip_length_range": {"min_days": 4, "max_days": 6},
            "travelers": {"adults": 2, "rooms": 1},
            "lodging_preferences": {
                "accepted_property_types": ["hotel", "vacation_rental"],
                "nightly_price_max_twd": 5000,
                "min_review_score": 8,
                "min_review_count": 50,
            },
            "interests": ["food", "beach"],
            "top_n": 3,
        }
    )
    first = await discover(_http_request(), request, _no_session())
    second = await discover(_http_request(), request, _no_session())
    assert first == second
    assert len(first["recommendations"]) == 3
    assert len({item["airport"] for item in first["recommendations"]}) == 3
    assert all(
        "2027-02-01" <= str(item["departure_date"]) <= "2027-04-30"
        for item in first["recommendations"]
    )
    assert all(4 <= item["trip_length_days"] <= 6 for item in first["recommendations"])
    assert first["source"] == "curated_estimate"


def test_lodging_price_range_rejects_inverted_values() -> None:
    with pytest.raises(ValidationError):
        LodgingPreferences(nightly_price_min_twd=6000, nightly_price_max_twd=3000)
