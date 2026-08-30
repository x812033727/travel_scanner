import pytest

from app.ai.parser import MockAITripParser


@pytest.mark.asyncio
async def test_parser_extracts_chinese_trip_request() -> None:
    result = await MockAITripParser().parse(
        "11 月兩個人從台北去日本 5 天，預算 6 萬，想吃美食跟逛街，不要紅眼班機，住宿至少 4 星"
    )
    assert result.origin == "TPE"
    assert result.destination_region == "Japan"
    assert result.travelers.adults == 2
    assert result.trip_length_days == 5
    assert result.budget_twd == 60_000
    assert set(result.interests) == {"food", "shopping"}
    assert result.avoid_red_eye
    assert result.hotel_min_rating == 4
