import pytest
from pydantic import ValidationError

from app.search.schemas import SearchCreate, SearchModule, TripLeg, TripType


def search(**updates: object) -> SearchCreate:
    values: dict[str, object] = {
        "origin": "TPE",
        "destination": "NRT",
        "departure_date": "2026-11-10",
        "return_date": "2026-11-15",
        "modules": [SearchModule.FLIGHT],
    }
    values.update(updates)
    return SearchCreate.model_validate(values)


def test_flexible_dates_compatibility_and_supported_ranges() -> None:
    legacy = search(flexible_dates=True)
    three_days = search(flex_days=3)

    assert legacy.flex_days == 7 and legacy.flexible_dates
    assert three_days.flex_days == 3 and three_days.flexible_dates
    with pytest.raises(ValidationError):
        search(flex_days=5)


def test_multi_city_rejects_flexible_dates() -> None:
    with pytest.raises(ValidationError, match="multi_city does not support flexible dates"):
        SearchCreate(
            trip_type=TripType.MULTI_CITY,
            legs=[
                TripLeg(origin="TPE", destination="NRT", departure_date="2026-11-10"),
                TripLeg(origin="NRT", destination="KIX", departure_date="2026-11-15"),
            ],
            modules=[SearchModule.FLIGHT],
            flex_days=7,
        )
