"""The explainer family: flat-explainer, cute-cartoon and cute-mystery are one kind of video.

Narrator only, no cast, 8 to 20 minutes, a one-off's. The list is kept by hand in four places on
the server (the ORM tuple behind the CHECK constraints, the schema's Literal, the family tuple,
the migration), so this file compares them; tools/video/core/explainer-family.test.mjs compares
the family with the tools' and the web's.

No request in this file posts a cute preset over HTTP: the schema and the service are called
directly.
"""

from __future__ import annotations

import importlib.util
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Any, get_args
from uuid import uuid4

import pytest
from pydantic import TypeAdapter, ValidationError

from app.video_automation import series as service
from app.video_automation.models import (
    STYLE_PRESET_CHECK,
    STYLE_PRESETS,
    VideoDramaDoc,
    VideoDramaSeries,
)
from app.video_automation.schemas import (
    EXPLAINER_PRESETS,
    SeriesDocSubmitIn,
    SeriesIn,
    StoryLook,
    StylePreset,
    is_explainer_preset,
)

MIGRATION = "0130_video_cute_presets"
VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"
WHEN = datetime(2026, 10, 11, 1, 0, tzinfo=UTC)
CUTE_PRESETS = ("cute-cartoon", "cute-mystery")
cute = pytest.mark.parametrize("preset", CUTE_PRESETS)


def _migration() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        f"migration_{MIGRATION}", VERSIONS / f"{MIGRATION}.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _series(**changes: Any) -> VideoDramaSeries:
    values: dict[str, Any] = {
        "id": uuid4(),
        "slug": "xianxia",
        "kind": "series",
        "title": "問劍",
        "premise": "兩個少年在正道與魔道之間",
        "aspects": ["world", "bonds"],
        "tone": "dual-male-leads-subtext",
        "style_preset": "cinematic-3d",
        "target_minutes": 3,
        "planned_episodes": 25,
        "episodes_per_chapter": 10,
        "open_ended": True,
        "status": "active",
        "note": None,
        "requested_chapter": None,
        "force_next": False,
        "created_at": WHEN,
        "updated_at": WHEN,
    }
    values.update(changes)
    return VideoDramaSeries(**values)


def _one_off(**changes: Any) -> VideoDramaSeries:
    values: dict[str, Any] = {
        "slug": "one-off-1a2b3c4d",
        "kind": "one-off",
        "title": "雷聲",
        "aspects": [],
        "planned_episodes": 1,
        "episodes_per_chapter": 1,
        "open_ended": False,
        "status": "setting",
    }
    values.update(changes)
    return _series(**values)


def _explainer(preset: str) -> VideoDramaSeries:
    return _one_off(style_preset=preset, target_minutes=10)


def _bible(status: str = "approved") -> VideoDramaDoc:
    return VideoDramaDoc(
        id=uuid4(),
        kind="bible",
        chapter_number=0,
        version=1,
        body_md="# doc",
        body_json={},
        status=status,
        note=None,
        created_at=WHEN,
    )


def test_the_preset_lists_agree_and_fit_their_column() -> None:
    assert list(get_args(StylePreset)) == list(STYLE_PRESETS)
    assert EXPLAINER_PRESETS == ("flat-explainer", "cute-cartoon", "cute-mystery")
    assert set(EXPLAINER_PRESETS) <= set(STYLE_PRESETS)
    # style_preset is String(16) on the three tables that store one.
    assert all(len(preset) <= 16 for preset in STYLE_PRESETS)

    migration = _migration()
    assert migration.revision == MIGRATION and len(migration.revision) <= 32
    assert migration.NEW_PRESETS == STYLE_PRESETS
    assert migration._text(migration.NEW_PRESETS) == STYLE_PRESET_CHECK
    assert migration.OLD_PRESETS == tuple(
        preset for preset in STYLE_PRESETS if preset not in CUTE_PRESETS
    )
    assert len(migration.OLD_PRESETS) == 5
    assert set(migration.NEW_PRESETS) - set(migration.OLD_PRESETS) == set(migration.CUTE_PRESETS)
    assert migration.CUTE_PRESETS == CUTE_PRESETS


def test_only_the_three_family_presets_are_explainers() -> None:
    for preset in EXPLAINER_PRESETS:
        assert is_explainer_preset(preset)
    for other in ("cinematic-3d", "anime-2d", "ink-wash", "custom", "", None):
        assert not is_explainer_preset(other)
    # The settings tab's default-style list is every stored preset, so it takes the new names.
    for preset in STYLE_PRESETS:
        assert TypeAdapter(StylePreset).validate_python(preset) == preset


@cute
def test_a_cute_preset_is_for_a_one_off_only(preset: str) -> None:
    one_off = SeriesIn.model_validate(
        {"slug": "one-off-why", "kind": "one-off", "title": "雷聲", "premise": "p",
         "style_preset": preset}
    )
    assert (one_off.style_preset, one_off.target_minutes) == (preset, 10)
    refusal = f'style_preset "{preset}" is for a one-off explainer only'
    with pytest.raises(ValidationError, match=refusal):
        SeriesIn.model_validate(
            {"slug": "xianxia", "title": "問劍", "premise": "p", "style_preset": preset}
        )
    with pytest.raises(ValidationError, match=refusal):
        SeriesIn.model_validate(
            {
                "slug": "stories",
                "kind": "story",
                "title": "品牌故事",
                "premise": "p",
                "style_preset": preset,
                "hands_off": True,
                "visual_tier": "stills",
                "look": StoryLook(style="flat", negative="text"),
            }
        )


def test_the_refusal_names_the_preset_that_was_sent() -> None:
    with pytest.raises(ValidationError, match='style_preset "flat-explainer" is for a one-off'):
        SeriesIn(slug="xianxia", title="問劍", premise="p", style_preset="flat-explainer")


@cute
def test_a_cute_one_off_is_an_explainer_and_its_bible_is_a_questions(preset: str) -> None:
    row = _explainer(preset)
    assert service.is_explainer(row)
    assert not service.is_explainer(_series(style_preset=preset)), "only a one-off"

    def doc(**body: Any) -> SeriesDocSubmitIn:
        return SeriesDocSubmitIn(kind="bible", body_md="# x", body_json=body)

    outline = {
        "question": "為什麼雷聲總比閃電晚到？",
        "answer": "光比聲音快太多。",
        "reasons": ["光速約每秒三十萬公里", "聲速約每秒三百四十公尺"],
        "hook": "閃電亮了，你數到幾？",
        "sources": ["https://en.wikipedia.org/wiki/Speed_of_sound"],
    }
    good = {"characters": [], "acts": [{"number": 1}], "outline": outline}
    assert service.doc_problem(row, doc(**good)) is None
    cast = [{"id": "nuwa", "name": "女娃", "appearance": "紅衣少女"}]
    assert service.doc_problem(row, doc(**{**good, "characters": cast})) == (
        "an explainer's bible has no characters"
    )


@cute
def test_a_long_or_story_series_never_takes_a_cute_preset(preset: str) -> None:
    story = _series(slug="stories", kind="story", hands_off=True, visual_tier="stills")
    for row in (_series(), story):
        refused = service.patch_problem(row, {"style_preset": preset})
        assert refused is not None
        assert (refused.status, refused.code) == (422, "video_series_explainer_one_off")


@cute
def test_a_written_bible_fixes_which_side_of_the_explainer_line_a_one_off_is_on(
    preset: str,
) -> None:
    # Before the worker wrote the bible a one-off crosses freely, in both directions.
    assert service.patch_problem(_one_off(), {"style_preset": preset}) is None
    assert service.patch_problem(_explainer(preset), {"style_preset": "ink-wash"}) is None
    for status in ("review", "approved", "rejected"):
        written = [_bible(status)]
        into = service.patch_problem(_one_off(), {"style_preset": preset}, written)
        assert into is not None
        assert (into.status, into.code) == (409, "video_series_explainer_fixed")
        out_of = service.patch_problem(_explainer(preset), {"style_preset": "anime-2d"}, written)
        assert out_of is not None
        assert (out_of.status, out_of.code) == (409, "video_series_explainer_fixed")
        assert "解說與故事之間" in out_of.detail
        # Sending the preset it already has changes nothing and stays allowed.
        assert service.patch_problem(_explainer(preset), {"style_preset": preset}, written) is None


@pytest.mark.parametrize(
    ("before", "after"),
    [
        ("flat-explainer", "cute-cartoon"),
        ("cute-cartoon", "cute-mystery"),
        ("cute-mystery", "flat-explainer"),
    ],
)
def test_a_written_bible_also_fixes_which_explainer_series_a_one_off_is(
    before: str, after: str
) -> None:
    """Each explainer preset is a series of its own, and the bible was written for one of them."""
    change = {"style_preset": after}
    assert service.patch_problem(_explainer(before), change) is None, "allowed before a bible"
    assert service.patch_problem(_explainer(before), change, []) is None
    for status in ("review", "approved", "rejected"):
        refused = service.patch_problem(_explainer(before), change, [_bible(status)])
        assert refused is not None
        assert (refused.status, refused.code) == (409, "video_series_explainer_fixed")
        assert "另一個解說系列" in refused.detail
