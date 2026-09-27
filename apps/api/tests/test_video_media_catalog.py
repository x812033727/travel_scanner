"""The media model catalog: every model priced once, defaults present, retired ones not offered."""

from __future__ import annotations

import pytest

from app.video_media import catalog
from app.video_media.catalog import (
    DEFAULT_CLIP,
    DEFAULT_IMAGE,
    DEFAULT_MUSIC,
    MEDIA_CATALOG,
    PRICES,
    MediaModel,
    find_model,
    media_options,
)


def test_every_model_has_exactly_one_price_and_a_clip_says_what_it_can_make() -> None:
    assert len({model.id for model in MEDIA_CATALOG}) == len(MEDIA_CATALOG)
    for model in MEDIA_CATALOG:
        prices = [
            price
            for price in (model.usd_per_second, model.usd_per_image, model.usd_per_track)
            if price is not None
        ]
        assert len(prices) == 1, model.id
        assert PRICES[model.id] == prices[0]
        if model.kind == "clip":
            assert model.resolutions and model.durations, model.id
            assert all(4 <= seconds <= 15 for seconds in model.durations), model.id


def test_the_defaults_are_stable_catalog_entries_of_their_kind() -> None:
    for (vendor, model_id), kind in (
        (DEFAULT_IMAGE, "image"),
        (DEFAULT_CLIP, "clip"),
        (DEFAULT_MUSIC, "music"),
    ):
        found = find_model(vendor, kind, model_id)  # type: ignore[arg-type]
        assert found is not None and found.status == "stable", model_id
        assert found in media_options(vendor, kind)  # type: ignore[arg-type]


def test_options_leave_retired_models_out_but_find_model_still_names_them(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    retired = MediaModel(
        "old-clip",
        "gemini",
        "clip",
        "Old",
        status="retired",
        resolutions=("720p",),
        durations=(8,),
        usd_per_second=0.1,
    )
    monkeypatch.setattr(catalog, "MEDIA_CATALOG", (*catalog.MEDIA_CATALOG, retired))
    assert retired not in media_options("gemini", "clip")
    assert find_model("gemini", "clip", "old-clip") is retired
    assert find_model("minimax", "clip", "old-clip") is None
    assert find_model("gemini", "image", "old-clip") is None
