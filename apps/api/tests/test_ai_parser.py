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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("trip_text", "destination", "region"),
    [
        ("明年去札幌 5 天看自然", "CTS", "Japan"),
        ("兩個人去釜山 4 天吃美食", "PUS", "South Korea"),
        ("想去清邁慢旅行 6 天做 SPA", "CNX", "Thailand"),
        ("普吉跳島與海灘旅行 5 天", "HKT", "Thailand"),
    ],
)
async def test_parser_supports_priority_asia_destinations(
    trip_text: str, destination: str, region: str
) -> None:
    result = await MockAITripParser().parse(trip_text)
    assert result.destination == destination
    assert result.destination_region == region


@pytest.mark.asyncio
async def test_parser_extracts_family_hotel_and_pace_preferences() -> None:
    result = await MockAITripParser().parse(
        "兩個人帶 2 個小孩去曼谷 5 天，住宿每晚最多 4500，含早餐、可免費取消，"
        "車站步行 8 分鐘，想住暹羅，行程悠閒"
    )
    assert result.destination == "BKK"
    assert result.travelers.children == 2
    assert result.hotel_max_nightly_twd == 4_500
    assert result.breakfast_required
    assert result.refundable_required
    assert result.max_station_walk_minutes == 8
    assert result.preferred_area == "暹羅"
    assert result.pace == "relaxed"


@pytest.mark.asyncio
async def test_parser_recognizes_deep_travel_language() -> None:
    for phrase in ("深度旅遊", "在地小眾", "巷弄冷門", "近郊"):
        result = await MockAITripParser().parse(f"台北 4 天，想走{phrase}行程")
        assert "deep_travel" in result.interests
