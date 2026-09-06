from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import httpx
import pytest
from pydantic import ValidationError

import app.ai.itinerary as itinerary_module
import app.trips.router as trip_router
from app.ai.itinerary import (
    MAX_CANDIDATE_ACCESS_MINUTES,
    MAX_CANDIDATE_DURATION_MINUTES,
    MIN_CANDIDATE_DURATION_MINUTES,
    AIDraftDay,
    AIDraftItem,
    AIItineraryDraft,
    AIItineraryPlanner,
    AIItineraryRequest,
    AIPlannerCandidate,
    AnthropicPlannerProvider,
    GeminiPlannerProvider,
    ResponsesPlannerProvider,
    clamp_candidate_access,
    clamp_candidate_duration,
    fallback_draft,
    normalize_draft,
)
from app.config import Settings
from app.search.schemas import SearchPreferences, Travelers, TripPace
from app.trips.itinerary import ItineraryHotspot
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
async def test_responses_provider_accepts_markdown_fenced_json() -> None:
    """MiniMax reasoning models ignore text.format and fence their JSON."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "status": "completed",
                "output_text": f"```json\n{draft_json()}\n```",
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = ResponsesPlannerProvider(
            "minimax", "https://api.minimax.io/v1", "secret", "MiniMax-M3", 1, 4000, client
        )
        result = await provider.generate(request_for())

    assert result.days[0].items[0].candidate_key == "hotspot:0"


def test_normalize_trims_an_oversized_provider_day_to_pace_rules() -> None:
    """MiniMax sometimes stuffs 6+ items into one day; parse must accept it and
    normalize must trim it instead of dropping the whole draft."""
    request = request_for()
    overfilled = AIItineraryDraft(
        summary="模型塞爆第二天",
        days=[
            AIDraftDay(
                date=date(2026, 11, 11),
                items=[
                    AIDraftItem(
                        candidate_key=f"hotspot:{index}",
                        start_time=f"{9 + index:02d}:00",
                        reason="行程",
                    )
                    for index in range(8)
                ],
            ),
        ],
    )
    normalized, partial = normalize_draft(request, overfilled)
    assert partial is True
    day = next(day for day in normalized.days if day.date == date(2026, 11, 11))
    activities = [item for item in day.items if item.slot_type == "activity"]
    assert len(activities) <= 2  # balanced pace on a middle day
    assert len(day.items) <= 5


def test_off_hours_and_overlong_draft_fields_survive_parsing_and_normalize() -> None:
    """MiniMax likes 08:30 starts and long prose; parse must clamp, and
    normalize must rewrite times into the slot grid instead of failing."""
    draft = AIItineraryDraft.model_validate(
        {
            "summary": "很".join("長" for _ in range(600)),
            "days": [
                {
                    "date": "2026-11-11",
                    "items": [
                        {
                            "candidate_key": "hotspot:1",
                            "start_time": "08:30",
                            "reason": "理" * 400,
                        },
                        {
                            "candidate_key": "merchant:1",
                            "start_time": "23:45",
                            "reason": "宵夜",
                            "slot_type": "dinner",
                        },
                    ],
                }
            ],
        }
    )
    assert len(draft.summary) == 500
    assert len(draft.days[0].items[0].reason) == 240

    normalized, _ = normalize_draft(request_for(), draft)
    day = next(day for day in normalized.days if day.date == date(2026, 11, 11))
    for item in day.items:
        assert "09:00" <= item.start_time <= "21:30"


def test_json_document_strips_fences_and_keeps_plain_json() -> None:
    from app.ai.structured_output import extract_json_document as _json_document

    payload = '{"summary": "ok", "days": []}'
    assert _json_document(payload) == payload
    assert _json_document(f"```json\n{payload}\n```") == payload
    assert _json_document(f"```\n{payload}\n```") == payload
    assert _json_document(f"  ```json\n{payload}\n```  ") == payload


@pytest.mark.asyncio
async def test_gemini_planner_sends_a_response_schema_the_api_accepts() -> None:
    captured: dict[str, Any] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["key"] = request.headers.get("x-goog-api-key")
        captured.update(json.loads(request.content))
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {"content": {"parts": [{"text": draft_json()}]}, "finishReason": "STOP"}
                ],
                "usageMetadata": {"promptTokenCount": 20, "candidatesTokenCount": 9},
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = GeminiPlannerProvider(
            "https://generativelanguage.googleapis.com/",
            "g-key",
            "gemini-3.8-flash",
            1,
            4000,
            client,
        )
        result = await provider.generate(request_for())

    assert result.days[0].items[0].candidate_key == "hotspot:0"
    assert captured["path"] == "/v1beta/models/gemini-3.8-flash:generateContent"
    assert captured["key"] == "g-key"
    generation = captured["generationConfig"]
    assert generation["responseMimeType"] == "application/json"
    serialized_schema = json.dumps(generation["responseSchema"])
    assert "$ref" not in serialized_schema and "$defs" not in serialized_schema
    days = generation["responseSchema"]["properties"]["days"]["items"]
    assert days["properties"]["items"]["items"]["properties"]["candidate_key"]["type"] == "string"
    assert "不要一直換飯店" in captured["contents"][0]["parts"][0]["text"]
    assert captured["system_instruction"]["parts"][0]["text"] == itinerary_module.SYSTEM_PROMPT


def test_gemini_joins_the_planner_roster_with_the_shared_guide_key() -> None:
    settings = Settings(
        ai_planner_mode="auto",
        ai_planner_priority="gemini,openai",
        openai_api_key="sk-test",
        anthropic_api_key=None,
        minimax_api_key=None,
        hotspot_guide_gemini_api_key="g-key",
        gemini_model="gemini-3.5-flash",
    )
    providers = itinerary_module._providers(settings)
    assert [(provider.name, provider.model) for provider in providers] == [
        ("gemini", "gemini-3.5-flash"),
        ("openai", settings.openai_model),
    ]
    assert isinstance(providers[0], GeminiPlannerProvider)
    assert providers[0].base_url == settings.hotspot_guide_gemini_base_url.rstrip("/")
    assert providers[0].api_key == "g-key"

    pinned = itinerary_module._providers(settings.model_copy(update={"ai_planner_mode": "gemini"}))
    assert [provider.name for provider in pinned] == ["gemini"]

    without_key = itinerary_module._providers(
        settings.model_copy(update={"hotspot_guide_gemini_api_key": None})
    )
    assert [provider.name for provider in without_key] == ["openai"]


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


def test_a_stop_that_is_shut_that_day_is_passed_over_rather_than_scheduled() -> None:
    """2026-11-09 is a Monday; a museum that closes on Mondays must not be planned then."""
    monday_closed = {
        "periods": [
            {
                "open": {"day": day, "hour": 9, "minute": 30},
                "close": {"day": day, "hour": 17, "minute": 0},
            }
            for day in (0, 2, 3, 4, 5, 6)
        ]
    }
    candidates = planner_candidates()
    shut = candidates[0].model_copy(update={"opening_hours": monday_closed, "rank": 0})
    request = request_for(pace=TripPace.PACKED).model_copy(
        update={
            "start_date": date(2026, 11, 9),
            "end_date": date(2026, 11, 10),
            "trip_start_date": date(2026, 11, 9),
            "trip_end_date": date(2026, 11, 10),
            "candidates": [shut, *candidates[1:]],
        }
    )

    draft = fallback_draft(request)

    monday = next(day for day in draft.days if day.date == date(2026, 11, 9))
    tuesday = next(day for day in draft.days if day.date == date(2026, 11, 10))
    assert shut.key not in [item.candidate_key for item in monday.items]
    assert shut.key in [item.candidate_key for item in tuesday.items]


def test_a_stop_with_no_cached_hours_is_planned_exactly_as_before() -> None:
    request = request_for(pace=TripPace.PACKED)
    assert all(candidate.opening_hours == {} for candidate in request.candidates)
    draft = fallback_draft(request)
    assert [len(day.items) for day in draft.days] == [2, 5, 5, 2]


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


def test_standard_tokyo_plan_never_mixes_a_ranked_day_trip_into_an_urban_day() -> None:
    day_trip = AIPlannerCandidate(
        key="hotspot:kawagoe-kita-in",
        kind="hotspot",
        name="喜多院",
        category="culture",
        latitude=35.917525,
        longitude=139.48906667,
        duration_minutes=150,
        depth_kind="day_trip",
        access_minutes=70,
        rank=1,
    )
    request = request_for().model_copy(
        update={"candidates": [day_trip, *planner_candidates()[:8]]}
    )

    draft = fallback_draft(request)
    selected = {
        item.candidate_key
        for day in draft.days
        for item in day.items
        if item.slot_type == "activity"
    }

    assert day_trip.key not in selected
    assert len(selected) == 6


def test_deep_tokyo_plan_keeps_the_day_trip_as_a_dedicated_middle_day() -> None:
    day_trip = AIPlannerCandidate(
        key="hotspot:kawagoe-kita-in",
        kind="hotspot",
        name="喜多院",
        category="culture",
        latitude=35.917525,
        longitude=139.48906667,
        duration_minutes=150,
        depth_kind="day_trip",
        access_minutes=70,
        rank=1,
    )
    request = request_for().model_copy(
        update={
            "candidates": [day_trip, *planner_candidates()[:8]],
            "preferences": request_for().preferences.model_copy(
                update={"interests": ["culture", "deep_travel"]}
            ),
        }
    )

    draft = fallback_draft(request)
    activity_days = [
        [item for item in day.items if item.slot_type == "activity"]
        for day in draft.days
    ]

    assert [item.candidate_key for item in activity_days[2]] == [day_trip.key]
    assert all(item.candidate_key != day_trip.key for item in activity_days[0])
    assert all(item.candidate_key != day_trip.key for item in activity_days[-1])
    assert all(item.slot_type == "activity" for item in draft.days[2].items)


@pytest.mark.asyncio
async def test_candidate_loader_hides_unrequested_excursions_and_forwards_extensions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rows = [
        ItineraryHotspot(
            hotspot_id="40000000-0000-0000-0000-000000000001",
            name="明治神宮",
            category="culture",
            latitude=35.6764,
            longitude=139.6993,
            map_links=[{"provider": "google", "url": "https://maps.example/meiji"}],
        ),
        ItineraryHotspot(
            hotspot_id="40000000-0000-0000-0000-000000000002",
            name="喜多院",
            category="culture",
            latitude=35.917525,
            longitude=139.48906667,
            map_links=[{"provider": "google", "url": "https://maps.example/kitain"}],
            depth_kind="day_trip",
            access_minutes=70,
        ),
        ItineraryHotspot(
            hotspot_id="40000000-0000-0000-0000-000000000003",
            name="延伸城市景點",
            category="culture",
            latitude=35.01,
            longitude=135.75,
            map_links=[{"provider": "google", "url": "https://maps.example/extension"}],
            destination_id="requested-extension",
            destination_role="extension",
            is_cross_city=True,
        ),
    ]
    captured: dict[str, object] = {}

    async def load_hotspots(*_args: object, **kwargs: object) -> list[ItineraryHotspot]:
        captured.update(kwargs)
        return rows

    async def load_foods(*_args: object, **_kwargs: object) -> list[object]:
        return []

    monkeypatch.setattr(trip_router, "load_planner_hotspots", load_hotspots)
    monkeypatch.setattr(trip_router, "load_planner_foods", load_foods)
    base = request_for().preferences.model_copy(update={"interests": ["culture"]})

    standard = await trip_router._load_ai_planner_candidates(
        object(),
        "東京",
        base,
        start_date=date(2027, 4, 8),
        end_date=date(2027, 4, 11),
    )
    deep = await trip_router._load_ai_planner_candidates(
        object(),
        "東京",
        base.model_copy(
            update={
                "interests": ["culture", "deep_travel"],
                "extension_destination_ids": ["requested-extension"],
            }
        ),
        start_date=date(2027, 4, 8),
        end_date=date(2027, 4, 11),
    )

    assert [candidate.name for candidate in standard] == ["明治神宮"]
    assert [candidate.name for candidate in deep] == [
        "明治神宮",
        "喜多院",
        "延伸城市景點",
    ]
    assert deep[1].depth_kind == "day_trip"
    assert deep[2].is_cross_city is True
    assert captured["extension_destination_ids"] == ["requested-extension"]


@pytest.mark.asyncio
async def test_planner_without_keys_returns_persistable_catalog_fallback() -> None:
    settings = Settings(
        ai_planner_mode="auto",
        openai_api_key=None,
        anthropic_api_key=None,
        minimax_api_key=None,
        hotspot_guide_gemini_api_key=None,
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


def test_candidate_minutes_are_clamped_into_the_planner_bounds() -> None:
    assert clamp_candidate_duration(20) == MIN_CANDIDATE_DURATION_MINUTES
    assert clamp_candidate_duration(120) == 120
    assert clamp_candidate_duration(9_000) == MAX_CANDIDATE_DURATION_MINUTES
    assert clamp_candidate_duration(None) == 120

    assert clamp_candidate_access(-5) == 0
    assert clamp_candidate_access(45) == 45
    assert clamp_candidate_access(600) == MAX_CANDIDATE_ACCESS_MINUTES
    assert clamp_candidate_access(None) == 0


def test_a_seeded_place_shorter_than_a_slot_becomes_a_candidate_instead_of_a_500() -> None:
    """忠犬八公像 is seeded at 20 minutes, which is true and below the planner's minimum slot.

    Before the clamp this raised a pydantic ValidationError inside the request handler. Only
    AppError and RequestValidationError have handlers, so it escaped as a 500 and every AI
    planning request for Tokyo failed - the place is ranked fifth there, well inside the
    candidate window.
    """
    candidate = AIPlannerCandidate(
        key="hotspot:nrt-hachiko-statue",
        kind="hotspot",
        name="忠犬八公像",
        category="landmark",
        latitude=35.659,
        longitude=139.700,
        duration_minutes=clamp_candidate_duration(20),
        access_minutes=clamp_candidate_access(None),
    )
    assert candidate.duration_minutes == MIN_CANDIDATE_DURATION_MINUTES

    with pytest.raises(ValidationError):
        AIPlannerCandidate(
            key="hotspot:unclamped",
            kind="hotspot",
            name="忠犬八公像",
            category="landmark",
            latitude=35.659,
            longitude=139.700,
            duration_minutes=20,
        )


def test_every_shipped_seed_value_survives_the_clamp() -> None:
    """The bound is only as good as the data that reaches it, and the seeds are unvalidated.

    ``recommended_duration_minutes`` lands in ``metadata_json``, a free-form JSON column the
    seed importer does not check even though ``hotspots/admin_router.py`` checks the same
    field for admin edits. This walks the real seed files so the next out-of-range value
    fails here rather than in production.
    """
    seeds = sorted((Path(itinerary_module.__file__).parents[1] / "hotspots").glob("*.json"))
    assert seeds, "expected the hotspot seed files to be importable"

    checked = 0
    for path in seeds:
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = payload if isinstance(payload, list) else payload.get("hotspots") or []
        for row in rows:
            if not isinstance(row, dict):
                continue
            duration = row.get("recommended_duration_minutes")
            access = row.get("access_minutes")
            if duration is None and access is None:
                continue
            checked += 1
            AIPlannerCandidate(
                key=f"hotspot:{row.get('slug', 'seed')}",
                kind="hotspot",
                name=row.get("name") or "seed",
                category=row.get("category") or "landmark",
                latitude=0.0,
                longitude=0.0,
                duration_minutes=clamp_candidate_duration(duration),
                access_minutes=clamp_candidate_access(access),
            )
    assert checked > 100, f"only {checked} seed rows carried the fields under test"
