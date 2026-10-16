"""API create and patch payloads for the MiniMax brand-story look."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.video_automation.models import VideoDramaSeries
from app.video_automation.schemas import SeriesIn, SeriesPatch
from app.video_automation.series import patch_problem, series_values


def _cute_payload(**changes: object) -> dict[str, object]:
    fields: dict[str, object] = {
        "slug": "story-cute-test",
        "kind": "story",
        "title": "品牌故事",
        "premise": "每集講一個品牌的真實故事。",
        "style_preset": "custom",
        "target_minutes": 10,
        "hands_off": True,
        "visual_tier": "stills",
        "image_model": "image-01",
        "look": {"preset": "cute-mystery"},
    }
    fields.update(changes)
    return fields


def test_create_payload_stores_the_exact_preset_while_story_writer_stays_custom() -> None:
    payload = SeriesIn.model_validate(_cute_payload())
    assert payload.model_dump()["look"] == {"preset": "cute-mystery"}
    row = series_values(payload, datetime(2026, 10, 15, tzinfo=UTC))
    assert (row["target_minutes"], row["image_model"], row["style_preset"]) == (
        10,
        "image-01",
        "custom",
    )
    assert row["look"] == {"preset": "cute-mystery"}
    assert SeriesPatch.model_validate({"look": {"preset": "cute-mystery"}}).model_dump(
        exclude_unset=True
    ) == {"look": {"preset": "cute-mystery"}}


@pytest.mark.parametrize(
    "changes",
    [
        {"target_minutes": 13},
        {"image_model": "gemini-3.1-flash-image"},
        {"style_preset": "cinematic-3d"},
        {"look": {"preset": "cute-mystery", "style": "extra"}},
        {"look": {"preset": "flat-explainer"}},
    ],
)
def test_create_payload_rejects_mismatched_cute_route(changes: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        SeriesIn.model_validate(_cute_payload(**changes))


def _story_row(**changes: object) -> VideoDramaSeries:
    values: dict[str, object] = {
        "slug": "story-cute-test",
        "kind": "story",
        "title": "品牌故事",
        "premise": "每集講一個品牌的真實故事。",
        "status": "active",
        "planning_only": False,
        "style_preset": "custom",
        "target_minutes": 10,
        "hands_off": True,
        "visual_tier": "stills",
        "compilation": False,
        "image_model": "image-01",
        "look": {"preset": "cute-mystery"},
    }
    values.update(changes)
    return VideoDramaSeries(**values)


def _patch_problem(row: VideoDramaSeries, changes: dict[str, object]) -> str | None:
    payload = SeriesPatch.model_validate(changes)
    problem = patch_problem(row, payload.model_dump(exclude_unset=True))
    if problem is None:
        return None
    assert problem.status == 422
    return problem.code


@pytest.mark.parametrize(
    "changes",
    [
        {"target_minutes": 13},
        {"image_model": "gemini-3.1-flash-image"},
        {"image_model": None},
        {"style_preset": "ink-wash"},
        {"look": {"style": "flat", "negative": "text"}},
    ],
)
def test_patch_refuses_a_partial_change_to_the_cute_route(changes: dict[str, object]) -> None:
    expected = (
        "video_series_story_custom_route"
        if "look" in changes
        else "video_series_story_cute_route"
    )
    assert _patch_problem(_story_row(), changes) == expected


def test_patch_checks_the_complete_route_when_switching_looks() -> None:
    custom_look = {"style": "flat", "negative": "text"}
    cute_look = {"preset": "cute-mystery"}
    assert _patch_problem(_story_row(), {"title": "新標題"}) is None
    assert _patch_problem(_story_row(), {"look": cute_look}) is None
    assert _patch_problem(_story_row(), {"look": custom_look, "target_minutes": 13}) is None
    original = _story_row(
        look=custom_look,
        target_minutes=13,
        image_model="gemini-3.1-flash-image",
    )
    assert _patch_problem(original, {"title": "新標題"}) is None
    assert _patch_problem(original, {"look": cute_look}) == "video_series_story_cute_route"
    assert _patch_problem(
        original,
        {"look": cute_look, "target_minutes": 10, "image_model": "image-01"},
    ) is None
