import pytest
from pydantic import ValidationError

from app.trips.router import SaveTripRequest, destination_timezone


def test_blank_trip_preferences_are_normalized_for_persistence() -> None:
    request = SaveTripRequest.model_validate(
        {
            "source": "blank",
            "name": "首爾朋友旅行",
            "destination_name": "韓國首爾",
            "start_date": "2026-11-10",
            "end_date": "2026-11-15",
            "travelers": {"adults": 3, "children": 1, "children_ages": [8], "rooms": 2},
            "preferences": {
                "budget_twd": 90000,
                "hotel_min_nightly_twd": 3000,
                "hotel_max_nightly_twd": 7000,
                "accepted_property_types": ["hotel", "vacation_rental"],
                "hotel_min_review_score": 8,
                "hotel_min_review_count": 100,
                "pace": "relaxed",
                "interests": ["food", "culture"],
            },
            "notes": "  不要一直換飯店  ",
        }
    )

    assert request.travelers.children_ages == [8]
    assert request.preferences.accepted_property_types == ["hotel", "vacation_rental"]
    assert request.preferences.pace == "relaxed"
    assert request.planning_mode == "ai_draft"
    assert request.notes == "不要一直換飯店"
    assert destination_timezone(request.destination_name or "") == "Asia/Seoul"


def test_destination_timezone_prefers_the_catalog_over_keyword_rules() -> None:
    # Cities the old keyword list never mentioned, plus an English alias.
    assert destination_timezone("仙台") == "Asia/Tokyo"
    assert destination_timezone("Kanazawa") == "Asia/Tokyo"
    assert destination_timezone("台中") == "Asia/Taipei"
    # Free text outside the catalog still falls back to the keyword rules.
    assert destination_timezone("日本某個小鎮") == "Asia/Tokyo"
    assert destination_timezone("火星基地") == "UTC"


def test_manual_blank_mode_is_rejected_for_saved_search_plans() -> None:
    with pytest.raises(ValidationError, match="only available for blank trips"):
        SaveTripRequest.model_validate(
            {
                "source": "search",
                "planning_mode": "manual_blank",
                "search_id": "77f4bb8e-55c4-457c-a7e0-9aac2a33a836",
                "plan_id": "4bdfd2c8-eaac-45b5-810d-a4d086d1d879",
                "name": "搜尋結果行程",
            }
        )


def test_blank_trip_rejects_invalid_hotel_price_range() -> None:
    with pytest.raises(ValidationError):
        SaveTripRequest.model_validate(
            {
                "source": "blank",
                "name": "東京",
                "destination_name": "東京",
                "start_date": "2026-11-10",
                "end_date": "2026-11-15",
                "preferences": {
                    "hotel_min_nightly_twd": 8000,
                    "hotel_max_nightly_twd": 3000,
                },
            }
        )
