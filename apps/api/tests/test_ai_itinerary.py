from __future__ import annotations

import json
from datetime import date

import httpx
import pytest
from pydantic import ValidationError

import app.ai.itinerary as itinerary_module
from app.ai.itinerary import (
    AIDraftDay,
    AIDraftItem,
    AIItineraryDraft,
    AIItineraryPlanner,
    AIItineraryRequest,
    AIPlannerCandidate,
    AnthropicPlannerProvider,
    ResponsesPlannerProvider,
    fallback_draft,
    normalize_draft,
)
from app.config import Settings
from app.search.schemas import SearchPreferences, Travelers, TripPace
from app.trips.router import ItineraryGenerateRequest


def planner_candidates() -> list[AIPlannerCandidate]:
    rows = [
        AIPlannerCandidate(
            key=f"hotspot:{index}",
            kind="hotspot",
            name=f"東京景點 {index}",
            category="culture" if index % 2 == 0 else "nature",
            latitude=35.68 + index * 0.002,
            longitude=139.76 + index * 0.002,
            duration_minutes=90,
            map_links=[{"provider": "google", "url": f"https://maps.example/{index}"}],
            hotspot_id=f"00000000-0000-0000-0000-{index + 1:012d}",
            rank=index + 1,
        )
        for index in range(8)
    ]
    rows.extend(
        AIPlannerCandidate(
            key=f"merchant:{index}",
            kind="merchant",
            name=f"東京店家 {index}",
            local_name=f"東京料理 {index}",
            category="food",
            latitude=35.69 + index * 0.001,
            longitude=139.77 + index * 0.001,
            duration_minutes=75,
            map_links=[{"provider": "google", "url": f"https://maps.example/m/{index}"}],
            food_id=f"10000000-0000-0000-0000-{index + 1:012d}",
            merchant_id=f"20000000-0000-0000-0000-{index + 1:012d}",
            meal_types=["lunch", "dinner"],
            rank=index + 1,
        )
        for index in range(6)
    )
    return rows


def request_for(*, pace: TripPace = TripPace.BALANCED) -> AIItineraryRequest:
    return AIItineraryRequest(
        destination_name="日本東京",
        start_date=date(2026, 11, 10),
        end_date=date(2026, 11, 13),
        timezone="Asia/Tokyo",
        route_preference="LESS_WALKING",
        travelers=Travelers(adults=2, children=1, children_ages=[7], rooms=1),
        preferences=SearchPreferences(
            pace=pace,
            interests=["food", "culture"],
            budget_twd=60_000,
            hotel_min_rating=4,
        ),
        notes="不要一直換飯店",
        candidates=planner_candidates(),
    )


def draft_json() -> str:
    return AIItineraryDraft(
        summary="東京文化與美食四日草稿",
        days=[
            AIDraftDay(
                date=date(2026, 11, 10),
                items=[
                    AIDraftItem(
                        candidate_key="hotspot:0",
                        start_time="15:00",
                        reason="首日以步調較輕鬆的文化景點開始",
                    ),
                    AIDraftItem(
                        candidate_key="merchant:0",
                        start_time="18:30",
                        reason="晚餐",
                        slot_type="dinner",
                    ),
                ],
            ),
            *[
                AIDraftDay(
                    date=day,
                    items=[
                        AIDraftItem(
                            candidate_key=f"hotspot:{index * 2 - 1}",
                            start_time="10:00",
                            reason="符合美食偏好",
                        ),
                        AIDraftItem(
                            candidate_key=f"merchant:{index * 2 - 1}",
                            start_time="12:00",
                            reason="午餐",
                            slot_type="lunch",
                        ),
                        AIDraftItem(
                            candidate_key=f"hotspot:{index * 2}",
                            start_time="14:00",
                            reason="兼顧文化與少走路偏好",
                        ),
                        AIDraftItem(
                            candidate_key=f"merchant:{index * 2}",
                            start_time="18:30",
                            reason="晚餐",
                            slot_type="dinner",
                        ),
                    ],
                )
                for index, day in enumerate((date(2026, 11, 11), date(2026, 11, 12)), 1)
            ],
            AIDraftDay(
                date=date(2026, 11, 13),
                items=[
                    AIDraftItem(
                        candidate_key="hotspot:7",
                        start_time="10:00",
                        reason="末日安排交通便利的輕鬆散步",
                    ),
                    AIDraftItem(
                        candidate_key="merchant:5",
                        start_time="12:00",
                        reason="午餐",
                        slot_type="lunch",
                    ),
                ],
            ),
        ],
    ).model_dump_json()


@pytest.mark.asyncio
async def test_openai_responses_uses_schema_store_false_and_rest_output_shape() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured.update(json.loads(request.content))
        return httpx.Response(
            200,
            json={
                "status": "completed",
                "output": [
                    {
                        "type": "message",
                        "content": [{"type": "output_text", "text": draft_json()}],
                    }
                ],
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = ResponsesPlannerProvider(
            "openai", "https://api.openai.com/v1", "secret", "gpt-test", 1, 4000, client
        )
        result = await provider.generate(request_for())

    assert result.days[0].items[0].candidate_key == "hotspot:0"
    assert captured["store"] is False
    assert captured["text"]["format"]["type"] == "json_schema"  # type: ignore[index]
    serialized_input = str(captured["input"])
    assert "不要一直換飯店" in serialized_input
    assert "email" not in serialized_input.lower()


@pytest.mark.asyncio
async def test_anthropic_uses_structured_output_config() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured.update(json.loads(request.content))
        return httpx.Response(
            200,
            json={"content": [{"type": "text", "text": draft_json()}]},
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = AnthropicPlannerProvider(
            "https://api.anthropic.com/v1", "secret", "claude-test", 1, 4000, client
        )
        result = await provider.generate(request_for())

    assert result.days[-1].date == date(2026, 11, 13)
    assert captured["output_config"]["format"]["type"] == "json_schema"  # type: ignore[index]


def test_fallback_covers_every_day_and_obeys_pace_counts() -> None:
    draft = fallback_draft(request_for(pace=TripPace.PACKED))
    assert [day.date for day in draft.days] == [
        date(2026, 11, 10),
        date(2026, 11, 11),
        date(2026, 11, 12),
        date(2026, 11, 13),
    ]
    assert [len(day.items) for day in draft.days] == [2, 5, 5, 2]
    meal_roles = [
        [item.slot_type for item in day.items if item.slot_type != "activity"] for day in draft.days
    ]
    assert meal_roles == [
        ["dinner"],
        ["lunch", "dinner"],
        ["lunch", "dinner"],
        ["lunch"],
    ]


def test_fallback_leaves_unusable_arrival_and_departure_windows_empty() -> None:
    request = request_for(pace=TripPace.PACKED).model_copy(
        update={
            "first_day_available_from": "20:30",
            "last_day_available_until": "09:00",
        }
    )

    draft = fallback_draft(request)
    normalized, partial = normalize_draft(request, draft)

    assert partial is False
    assert normalized.days[0].items == []
    assert normalized.days[-1].items == []
    assert [len(day.items) for day in normalized.days[1:-1]] == [5, 5]


def test_normalize_fills_missing_days_and_rewrites_safe_slots() -> None:
    partial = AIItineraryDraft(
        summary="不完整草稿",
        days=[
            AIDraftDay(
                date=date(2026, 11, 11),
                items=[
                    AIDraftItem(
                        candidate_key="hotspot:1",
                        start_time="21:00",
                        reason="文化景點",
                    )
                ],
            )
        ],
    )
    normalized, was_partial = normalize_draft(request_for(), partial)
    assert was_partial is True
    assert len(normalized.days) == 4
    assert all(day.items for day in normalized.days)
    assert normalized.days[1].items[0].start_time == "10:00"


def test_normalize_rejects_unknown_candidate_and_never_persists_free_text() -> None:
    request = request_for()
    draft = AIItineraryDraft(
        summary="包含未知地點",
        days=[
            AIDraftDay(
                date=request.start_date,
                items=[
                    AIDraftItem(
                        candidate_key="hotspot:not-approved",
                        start_time="15:00",
                        reason="模型自行產生的候選",
                    )
                ],
            )
        ],
    )

    normalized, partial = normalize_draft(request, draft)

    assert partial is True
    assert all(
        item.candidate_key != "hotspot:not-approved"
        for day in normalized.days
        for item in day.items
    )


@pytest.mark.asyncio
async def test_catalog_without_exact_candidates_returns_explicit_gaps() -> None:
    request = request_for().model_copy(update={"candidates": []})
    result = await AIItineraryPlanner(
        Settings(
            ai_planner_mode="fallback",
            openai_api_key=None,
            anthropic_api_key=None,
            minimax_api_key=None,
        )
    ).generate(request)

    assert result.planning.readiness == "needs_setup"
    assert all(not day.items for day in result.itinerary)
    assert result.unscheduled_slots


def test_tokyo_four_day_fallback_keeps_exact_pois_in_neighboring_day_groups() -> None:
    places = [
        ("淺草寺", 35.7148, 139.7967),
        ("東京晴空塔", 35.7101, 139.8107),
        ("上野公園", 35.7140, 139.7730),
        ("新宿御苑", 35.6852, 139.7101),
        ("明治神宮", 35.6764, 139.6993),
        ("澀谷十字路口", 35.6595, 139.7005),
    ]
    exact_hotspots = [
        AIPlannerCandidate(
            key=f"hotspot:tokyo:{index}",
            kind="hotspot",
            name=name,
            category="culture",
            latitude=latitude,
            longitude=longitude,
            duration_minutes=90,
            map_links=[{"provider": "google", "url": f"https://maps.example/tokyo/{index}"}],
            hotspot_id=f"30000000-0000-0000-0000-{index + 1:012d}",
            rank=index + 1,
        )
        for index, (name, latitude, longitude) in enumerate(places)
    ]
    request = request_for().model_copy(update={"candidates": exact_hotspots})

    draft = fallback_draft(request)
    itinerary = normalize_draft(request, draft)[0]
    activity_days = [
        [item for item in day.items if item.slot_type == "activity"] for day in itinerary.days
    ]

    assert [len(items) for items in activity_days] == [1, 2, 2, 1]
    assert len({item.candidate_key for items in activity_days for item in items}) == 6
    candidates = {candidate.key: candidate for candidate in exact_hotspots}
    for items in activity_days:
        longitudes = [candidates[item.candidate_key].longitude for item in items]
        assert not longitudes or max(longitudes) - min(longitudes) < 0.04
    assert all(
        "與" not in candidates[item.candidate_key].name for items in activity_days for item in items
    )


@pytest.mark.asyncio
async def test_planner_without_keys_returns_persistable_catalog_fallback() -> None:
    settings = Settings(
        ai_planner_mode="auto",
        openai_api_key=None,
        anthropic_api_key=None,
        minimax_api_key=None,
    )
    result = await AIItineraryPlanner(settings).generate(request_for())
    assert result.planning.status == "fallback"
    assert result.planning.provider == "catalog"
    assert {day.date for day in result.itinerary} == {
        date(2026, 11, 10),
        date(2026, 11, 11),
        date(2026, 11, 12),
        date(2026, 11, 13),
    }
    assert all(
        item.data["generated_by"] == "ai_planner" for day in result.itinerary for item in day.items
    )
    assert [
        {item.system_role for item in day.items if item.system_role} for day in result.itinerary
    ] == [{"dinner"}, {"lunch", "dinner"}, {"lunch", "dinner"}, {"lunch"}]
    assert not result.unscheduled_slots
    assert all(
        item.latitude is not None and item.longitude is not None
        for day in result.itinerary
        for item in day.items
    )
    assert all(
        item.data["needs_place_confirmation"] is False
        for day in result.itinerary
        for item in day.items
    )


@pytest.mark.asyncio
async def test_auto_mode_fails_over_to_next_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    class ProviderStub:
        def __init__(self, name: str, model: str, error: Exception | None = None) -> None:
            self.name = name
            self.model = model
            self.error = error

        async def generate(self, _request: AIItineraryRequest) -> AIItineraryDraft:
            if self.error:
                raise self.error
            return AIItineraryDraft.model_validate_json(draft_json())

    providers = [
        ProviderStub("openai", "openai-test", httpx.ReadTimeout("timed out")),
        ProviderStub("anthropic", "claude-test"),
    ]
    monkeypatch.setattr(itinerary_module, "_providers", lambda _settings: providers)
    result = await AIItineraryPlanner(Settings()).generate(request_for())

    assert result.planning.provider == "anthropic"
    assert result.planning.model == "claude-test"
    assert result.planning.status == "live"
    assert result.planning.warnings == ["openai 暫時無法產生有效行程（ReadTimeout）"]


def test_itinerary_generation_scope_is_backward_compatible_and_validated() -> None:
    full_trip = ItineraryGenerateRequest(version=3)
    assert full_trip.scope == "trip"
    assert full_trip.day_date is None

    single_day = ItineraryGenerateRequest(
        version=3,
        scope="day",
        day_date=date(2026, 11, 11),
    )
    assert single_day.scope == "day"
    assert single_day.day_date == date(2026, 11, 11)

    with pytest.raises(ValidationError):
        ItineraryGenerateRequest(version=3, scope="day")
    with pytest.raises(ValidationError):
        ItineraryGenerateRequest(
            version=3,
            scope="trip",
            day_date=date(2026, 11, 11),
        )
