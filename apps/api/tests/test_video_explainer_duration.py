"""Long explainers keep their own length without changing short drama episodes."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.models import User
from app.video_automation import series as service
from app.video_automation.models import VideoDramaSeries
from app.video_automation.schemas import EXPLAINER_PRESETS, DramaRequestIn, SeriesIn, SeriesPatch

# Every explainer preset keeps flat-explainer's length rules: 8 to 20 minutes, ten by default.
explainer_presets = pytest.mark.parametrize("preset", EXPLAINER_PRESETS)


def _row(*, preset: str = "flat-explainer", minutes: int = 3) -> VideoDramaSeries:
    return VideoDramaSeries(
        id=uuid4(),
        slug="one-off-why",
        kind="one-off",
        style_preset=preset,
        target_minutes=minutes,
        status="active",
    )


@explainer_presets
@pytest.mark.parametrize("minutes", [8, 10, 20])
def test_explainer_requests_and_one_offs_accept_the_long_range(minutes: int, preset: str) -> None:
    request = DramaRequestIn.model_validate(
        {
            "premise": "Why thunder follows lightning",
            "style_preset": preset,
            "target_minutes": minutes,
        }
    )
    series = SeriesIn.model_validate(
        {
            "kind": "one-off",
            "premise": "Why thunder follows lightning",
            "style_preset": preset,
            "target_minutes": minutes,
        }
    )
    assert request.target_minutes == series.target_minutes == minutes


@explainer_presets
@pytest.mark.parametrize("minutes", [7, 21])
def test_explainers_refuse_short_or_overlong_input(minutes: int, preset: str) -> None:
    with pytest.raises(ValidationError):
        DramaRequestIn.model_validate(
            {"premise": "p", "style_preset": preset, "target_minutes": minutes}
        )
    with pytest.raises(ValidationError):
        SeriesIn.model_validate(
            {"kind": "one-off", "premise": "p", "style_preset": preset, "target_minutes": minutes}
        )


def test_omitted_length_defaults_to_ten_for_explainers_and_three_for_dramas() -> None:
    for preset in EXPLAINER_PRESETS:
        request = DramaRequestIn.model_validate({"premise": "p", "style_preset": preset})
        one_off = SeriesIn.model_validate(
            {"kind": "one-off", "premise": "p", "style_preset": preset}
        )
        assert request.target_minutes == one_off.target_minutes == 10
    assert DramaRequestIn(premise="p").target_minutes == 3
    assert SeriesIn(kind="one-off", premise="p").target_minutes == 3
    assert SeriesIn(premise="p").target_minutes == 3
    with pytest.raises(ValidationError):
        DramaRequestIn(premise="p", target_minutes=9)
    for kind in ("series", "one-off"):
        with pytest.raises(ValidationError):
            SeriesIn.model_validate({"kind": kind, "premise": "p", "target_minutes": 9})


@pytest.mark.parametrize("value", [True, False, 8.5])
def test_lengths_are_whole_minutes_not_booleans(value: object) -> None:
    for model, fields in (
        (DramaRequestIn, {"premise": "p"}),
        (SeriesIn, {"premise": "p", "kind": "one-off"}),
        (SeriesPatch, {}),
    ):
        with pytest.raises(ValidationError):
            model.model_validate({**fields, "target_minutes": value})


@explainer_presets
@pytest.mark.parametrize("minutes", [8, 10, 20])
def test_a_legacy_short_explainer_can_be_corrected_by_patch(minutes: int, preset: str) -> None:
    patch = SeriesPatch(target_minutes=minutes).model_dump(exclude_unset=True)
    assert service.patch_problem(_row(preset=preset), patch) is None


@explainer_presets
@pytest.mark.parametrize("minutes", [7, 21, None])
def test_patch_checks_the_effective_explainer_style(minutes: int | None, preset: str) -> None:
    for row, changes in (
        (_row(preset=preset, minutes=10), {"target_minutes": minutes}),
        (_row(preset="anime-2d"), {"style_preset": preset, "target_minutes": minutes}),
    ):
        refused = service.patch_problem(row, changes)
        assert refused is not None and refused.status == 422
    refused = service.patch_problem(
        _row(preset=preset, minutes=10), {"style_preset": "anime-2d", "target_minutes": 10}
    )
    assert refused is not None and refused.code == "video_series_too_long"


def test_legacy_short_explainers_can_still_pause_or_edit_their_title() -> None:
    assert service.patch_problem(_row(), {"status": "paused", "title": "Revised question"}) is None
    ordinary = _row(preset="anime-2d")
    ordinary.kind = "series"
    refused = service.patch_problem(ordinary, {"target_minutes": 9})
    assert refused is not None and refused.code == "video_series_too_long"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("before", "minutes", "after", "expected"),
    [
        ("anime-2d", 3, "flat-explainer", 10),
        ("flat-explainer", 10, "anime-2d", 3),
        ("flat-explainer", 3, "flat-explainer", 10),
        # The cute presets are explainers too: crossing the line takes that side's default, and
        # a move inside the family keeps the length unless it is a legacy short one.
        ("anime-2d", 3, "cute-cartoon", 10),
        ("cute-mystery", 10, "anime-2d", 3),
        ("flat-explainer", 12, "cute-cartoon", 12),
        ("cute-cartoon", 3, "cute-mystery", 10),
    ],
)
async def test_style_only_patch_persists_the_correct_default(
    monkeypatch: pytest.MonkeyPatch, before: str, minutes: int, after: str, expected: int
) -> None:
    row = _row(preset=before, minutes=minutes)
    monkeypatch.setattr(service, "_series", AsyncMock(return_value=row))
    monkeypatch.setattr(service, "_docs", AsyncMock(return_value=[]))
    monkeypatch.setattr(service, "_episodes", AsyncMock(return_value=[]))
    monkeypatch.setattr(service, "series_view", AsyncMock(return_value=MagicMock()))
    session: Any = MagicMock()
    session.commit = AsyncMock()
    await service.patch_series(
        session, User(id=uuid4()), row.slug, SeriesPatch.model_validate({"style_preset": after})
    )
    assert (row.style_preset, row.target_minutes) == (after, expected)
    session.commit.assert_awaited_once()
