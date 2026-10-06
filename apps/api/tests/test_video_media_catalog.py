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


def test_the_gemini_image_models_carry_a_2k_price_beside_their_1k_price() -> None:
    """A still that fills the frame is asked at 2K (docs/videos/ILLUSTRATED.md): Pro sells 2K at
    the 1K price, Flash at a half more; MiniMax draws at 1K only, so a 2K job is refused."""
    pro = find_model("gemini", "image", "gemini-3-pro-image")
    flash = find_model("gemini", "image", "gemini-3.1-flash-image")
    mini = find_model("minimax", "image", "image-01")
    assert pro is not None and flash is not None and mini is not None
    assert (pro.usd_per_image, pro.usd_per_image_2k) == (0.134, 0.134)
    assert (flash.usd_per_image, flash.usd_per_image_2k) == (0.067, 0.101)
    assert mini.usd_per_image_2k is None
    for model in MEDIA_CATALOG:
        if model.kind != "image":
            assert model.usd_per_image_2k is None, model.id


def test_only_the_gemini_image_models_take_a_style_reference() -> None:
    """The Gemini adapter forwards a role "style" reference with its own instruction; the
    MiniMax adapter sends a character reference alone, so image-01 never sees a style plate
    and the tools draw none for it (tools/video/media/keyframes.mjs)."""
    for model in MEDIA_CATALOG:
        expected = 1 if model.kind == "image" and model.vendor == "gemini" else 0
        assert model.style_references == expected, model.id
        assert model.style_references <= model.reference_images, model.id
    mini = find_model("minimax", "image", "image-01")
    assert mini is not None and mini.style_references == 0 and mini.reference_images == 1


def test_the_defaults_are_stable_catalog_entries_of_their_kind() -> None:
    for (vendor, model_id), kind in (
        (DEFAULT_IMAGE, "image"),
        (DEFAULT_CLIP, "clip"),
        (DEFAULT_MUSIC, "music"),
    ):
        found = find_model(vendor, kind, model_id)  # type: ignore[arg-type]
        assert found is not None and found.status == "stable", model_id
        assert found in media_options(vendor, kind)  # type: ignore[arg-type]


def test_lite_uses_the_gemini_api_id_and_conservative_1080p_price() -> None:
    lite = find_model("gemini", "clip", "veo-3.1-lite-generate-preview")
    assert lite is not None
    assert lite.resolutions == ("720p", "1080p") and lite.durations == (4, 6, 8)
    assert lite.reference_images == 0 and lite.native_audio is True
    assert PRICES[lite.id] == 0.08
    assert DEFAULT_CLIP != ("gemini", lite.id), "adding a model must not switch existing jobs"


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
