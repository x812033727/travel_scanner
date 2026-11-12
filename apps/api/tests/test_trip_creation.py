import pytest
from pydantic import ValidationError

from app.destinations.catalog import SEARCHABLE_DESTINATIONS, match_destination
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


@pytest.mark.parametrize(
    ("destination", "code", "timezone"),
    [
        ("도쿄도", "NRT", "Asia/Tokyo"),
        ("오사카시", "KIX", "Asia/Tokyo"),
        ("冲绳", "OKA", "Asia/Tokyo"),
        ("ソウル特別市", "ICN", "Asia/Seoul"),
        ("부산광역시", "PUS", "Asia/Seoul"),
        ("バンコク", "BKK", "Asia/Bangkok"),
        ("치앙마이", "CNX", "Asia/Bangkok"),
        ("プーケット", "HKT", "Asia/Bangkok"),
        ("타이베이", "TPE", "Asia/Taipei"),
        ("ホーチミン", "SGN", "Asia/Ho_Chi_Minh"),
    ],
)
def test_localized_city_names_match_the_catalog(destination: str, code: str, timezone: str) -> None:
    # Google Places returns city names in the UI locale, so a ko or ja user who
    # picks 도쿄 or バンコク must land on the same catalog entry as 東京 or 曼谷.
    matched = match_destination(destination)
    assert matched is not None and matched.code == code
    assert destination_timezone(destination) == timezone


def test_non_ascii_aliases_never_point_at_two_destinations() -> None:
    # match_destination is a substring test, so a localized alias contained in
    # another destination's alias would silently hijack that destination.
    for first in SEARCHABLE_DESTINATIONS:
        for second in SEARCHABLE_DESTINATIONS:
            if first is second:
                continue
            for alias in first.aliases:
                if alias.isascii():
                    continue
                assert not any(alias.casefold() in other.casefold() for other in second.aliases), (
                    first.code,
                    alias,
                    second.code,
                )


def test_destination_timezone_prefers_the_catalog_over_keyword_rules() -> None:
    # Cities the old keyword list never mentioned, plus an English alias.
    assert destination_timezone("仙台") == "Asia/Tokyo"
    assert destination_timezone("Kanazawa") == "Asia/Tokyo"
    assert destination_timezone("台中") == "Asia/Taipei"
    # Free text outside the catalog still falls back to the keyword rules.
    assert destination_timezone("日本某個小鎮") == "Asia/Tokyo"
    assert destination_timezone("火星基地") == "UTC"


def test_trip_create_request_key_is_scoped_per_user_and_hashes_the_client_key() -> None:
    from uuid import uuid4

    from app.trips.router import _trip_create_request_key

    user_a, user_b = uuid4(), uuid4()
    key = _trip_create_request_key(user_a, "attempt-1234-5678")
    assert key.startswith(f"trip:create-request:{user_a}:")
    assert "attempt-1234-5678" not in key
    assert key == _trip_create_request_key(user_a, "attempt-1234-5678")
    assert key != _trip_create_request_key(user_b, "attempt-1234-5678")
    assert key != _trip_create_request_key(user_a, "attempt-1234-5679")


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
