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
    AnthropicPlannerProvider,
    ResponsesPlannerProvider,
    fallback_draft,
    normalize_draft,
)
from app.config import Settings
from app.search.schemas import SearchPreferences, Travelers, TripPace
from app.trips.router import ItineraryGenerateRequest


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
    )


def draft_json() -> str:
    return AIItineraryDraft(
        summary="東京文化與美食四日草稿",
        days=[
            AIDraftDay(
                date=date(2026, 11, 10),
                items=[
                    AIDraftItem(
                        title="淺草寺",
                        location_query="淺草寺 東京",
                        start_time="15:00",
                        duration_minutes=90,
                        category="culture",
                        reason="首日以步調較輕鬆的文化景點開始",
                        notes="",
                    )
                ],
            ),
            *[
                AIDraftDay(
                    date=day,
                    items=[
                        AIDraftItem(
                            title=f"築地場外市場 {index}",
                            location_query="築地場外市場 東京",
                            start_time="10:00",
                            duration_minutes=120,
                            category="food",
                            reason="符合美食偏好",
                            notes="",
                        ),
                        AIDraftItem(
                            title=f"上野公園 {index}",
                            location_query="上野公園 東京",
                            start_time="14:00",
                            duration_minutes=120,
                            category="culture",
                            reason="兼顧文化與少走路偏好",
                            notes="",
                        ),
                    ],
                )
                for index, day in enumerate(
                    (date(2026, 11, 11), date(2026, 11, 12)), 1
                )
            ],
            AIDraftDay(
                date=date(2026, 11, 13),
                items=[
                    AIDraftItem(
                        title="東京車站丸之內",
                        location_query="東京車站丸之內",
                        start_time="10:00",
                        duration_minutes=90,
                        category="sight",
                        reason="末日安排交通便利的輕鬆散步",
                        notes="",
                    )
                ],
            )
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

    assert result.days[0].items[0].title == "淺草寺"
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
    assert [len(day.items) for day in draft.days] == [1, 3, 3, 1]


def test_normalize_fills_missing_days_and_rewrites_safe_slots() -> None:
    partial = AIItineraryDraft(
        summary="不完整草稿",
        days=[
            AIDraftDay(
                date=date(2026, 11, 11),
                items=[
                    AIDraftItem(
                        title="明治神宮",
                        location_query="明治神宮 東京",
                        start_time="21:00",
                        duration_minutes=240,
                        category="culture",
                        reason="文化景點",
                        notes="",
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
        item.data["generated_by"] == "ai_planner"
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
