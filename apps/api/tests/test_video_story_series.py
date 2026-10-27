"""API create and patch payloads for the MiniMax brand-story look."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.video_automation.models import VideoDramaSeries
from app.video_automation.schemas import SeriesDocSubmitIn, SeriesIn, SeriesPatch
from app.video_automation.series import (
    NARRATOR_STYLE_CHARS,
    SHEET_PROMPT_CHARS,
    doc_problem,
    patch_problem,
    series_values,
)


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
        {"target_minutes": 11},
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


# A setting book's cast may give a character its own sheet prompt (docs/videos/SERIES.md
# §人物表的 sheet_prompt): the sentence the worker's look stage draws the design sheet from, for
# a character with no human form (系統說我是 BUG's 系統, a pane of light, 2026-10-25).
def _series_row(**changes: object) -> VideoDramaSeries:
    values: dict[str, object] = {
        "slug": "xitong-shuo-wo-shi-bug",
        "kind": "series",
        "title": "系統說我是 BUG",
        "premise": "一個被系統判定為 BUG 的人",
        "style_preset": "cinematic-3d",
        "target_minutes": 3,
        "planned_episodes": 50,
        "episodes_per_chapter": 10,
        "open_ended": True,
        "status": "active",
    }
    values.update(changes)
    return VideoDramaSeries(**values)


def _setting_with_cast(*characters: Mapping[str, object]) -> SeriesDocSubmitIn:
    return SeriesDocSubmitIn(
        kind="setting", body_md="# x", body_json={"characters": [dict(c) for c in characters]}
    )


def _problem(*characters: Mapping[str, object]) -> str | None:
    return doc_problem(_series_row(), _setting_with_cast(*characters))


PANE_PROMPT = (
    "a single blank pane of pale-blue light floating in darkness, soft glow at its edges, "
    "nothing else in the picture, no person, no face, no text"
)
HERO: Mapping[str, object] = {
    "id": "a-zhu",
    "name": "阿竹",
    "appearance": "a thin young man in a grey hoodie",
}
SYSTEM: Mapping[str, object] = {
    "id": "xitong",
    "name": "系統",
    "appearance": "a blank pane of pale-blue light",
}


def test_a_setting_book_character_may_carry_its_own_sheet_prompt() -> None:
    assert _problem(HERO, SYSTEM) is None, "as before"
    assert _problem(HERO, {**SYSTEM, "sheet_prompt": PANE_PROMPT}) is None
    assert _problem(HERO, {**SYSTEM, "sheet_prompt": None}) is None, "null: as if left out"
    assert _problem({**SYSTEM, "sheet_prompt": "x" * SHEET_PROMPT_CHARS}) is None
    one_off = _series_row(kind="one-off", planned_episodes=1, episodes_per_chapter=1)
    bible = SeriesDocSubmitIn(
        kind="bible",
        body_md="# x",
        body_json={
            "characters": [{**SYSTEM, "sheet_prompt": PANE_PROMPT}],
            "acts": [{"title": "一"}],
            "outline": {"title": "x"},
        },
    )
    assert doc_problem(one_off, bible) is None, "a story bible's cast takes it too"


@pytest.mark.parametrize(
    "sheet_prompt",
    ["", "   ", 12, ["a pane of light"], "x" * (SHEET_PROMPT_CHARS + 1)],
)
def test_a_sheet_prompt_that_is_not_short_text_is_refused(sheet_prompt: object) -> None:
    problem = _problem(HERO, {**SYSTEM, "sheet_prompt": sheet_prompt})
    assert problem == "character xitong: sheet_prompt must be text of at most 600 characters"


# A setting book may name the work's own narrator (docs/videos/SERIES.md §作品的旁白), so the
# first-person male voice of 系統說我是 BUG never becomes every drama's drama_voice (2026-10-27).
def _narrated(narrator: object) -> str | None:
    setting = SeriesDocSubmitIn(
        kind="setting", body_md="# x", body_json={"characters": [dict(HERO)], "narrator": narrator}
    )
    return doc_problem(_series_row(), setting)


CHARON: Mapping[str, object] = {"provider": "gemini", "name": "Charon"}
NAME_PROBLEM = "narrator.name must be the voice's name, at most 64 characters"
STYLE_PROBLEM = "narrator.style must be text of at most 400 characters"
SHAPE_PROBLEM = "narrator must be {provider, name, style}"
PROVIDER_PROBLEM = "narrator.provider must be one of azure, gemini"


def test_a_setting_book_may_name_its_own_narrator() -> None:
    assert _narrated(None) is None, "null: the drama tab's voice, as before"
    assert _narrated(dict(CHARON)) is None
    assert _narrated({**CHARON, "style": "江河本人，邊講邊吐槽"}) is None
    assert _narrated({**CHARON, "style": "x" * NARRATOR_STYLE_CHARS}) is None
    assert _narrated({"provider": "azure", "name": "zh-TW-YunJheNeural"}) is None
    one_off = _series_row(kind="one-off", planned_episodes=1, episodes_per_chapter=1)
    bible = SeriesDocSubmitIn(
        kind="bible",
        body_md="# x",
        body_json={
            "characters": [dict(HERO)],
            "acts": [{"title": "一"}],
            "outline": {"title": "x"},
            "narrator": {"provider": "openai", "name": "alloy"},
        },
    )
    assert doc_problem(one_off, bible) == PROVIDER_PROBLEM


@pytest.mark.parametrize(
    ("narrator", "problem"),
    [
        ("Charon", SHAPE_PROBLEM),
        ({**CHARON, "rate": "+20%"}, SHAPE_PROBLEM),
        ({"provider": "elevenlabs", "name": "Adam"}, PROVIDER_PROBLEM),
        ({"provider": "gemini"}, NAME_PROBLEM),
        ({"provider": "gemini", "name": "  "}, NAME_PROBLEM),
        ({"provider": "gemini", "name": "x" * 65}, NAME_PROBLEM),
        (
            {"provider": "azure", "name": "zh-TW-YunJheNeural", "style": "快"},
            "narrator.style is a Gemini voice's; an Azure voice has none",
        ),
        ({**CHARON, "style": ""}, STYLE_PROBLEM),
        ({**CHARON, "style": "x" * (NARRATOR_STYLE_CHARS + 1)}, STYLE_PROBLEM),
    ],
)
def test_a_narrator_that_is_not_a_voice_is_refused(narrator: object, problem: str) -> None:
    assert _narrated(narrator) == problem
