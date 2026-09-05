from __future__ import annotations

import pytest

from app.i18n import LOCALES
from app.localized_names import (
    build_localized_names,
    has_localized_names,
    is_latin_script,
    item_names,
    join_localized_names,
    original_locale_for,
    original_name,
    resolve_item_field,
    resolve_localized_name,
    sanitize_localized_names,
)


def test_build_fills_every_site_locale_from_the_original_and_fallback_chain() -> None:
    names = build_localized_names(
        names={"zh-TW": "淺草寺", "en": "Sensō-ji"},
        original="浅草寺",
        country_code="JP",
    )
    assert names == {
        "zh-TW": "淺草寺",
        "zh-CN": "淺草寺",  # sibling Chinese script before anything else
        "en": "Sensō-ji",
        "ja": "浅草寺",  # the original language reads the original text
        "ko": "Sensō-ji",  # English before Chinese for other readers
        "original": "浅草寺",
        "original_locale": "ja",
    }
    assert set(LOCALES) <= set(names)


def test_build_keeps_non_site_originals_without_leaking_them_into_a_locale() -> None:
    names = build_localized_names(names={"en": "Thipsamai"}, original="ทิพย์สมัย", country_code="TH")
    assert names["original"] == "ทิพย์สมัย"
    assert names["original_locale"] == "th"
    assert all(names[locale] == "Thipsamai" for locale in LOCALES)


def test_build_uses_the_canonical_fallback_only_when_nothing_else_is_known() -> None:
    assert build_localized_names(names={}, fallback="景點") == dict.fromkeys(LOCALES, "景點")
    assert build_localized_names(names={"  ": "x"}) == {}
    assert build_localized_names(names={"en": " Grand Palace "}, country_code="SG")["ja"] == (
        "Grand Palace"
    )


@pytest.mark.parametrize(
    ("country", "expected"),
    [("JP", "ja"), ("kr", "ko"), ("TW", "zh-TW"), ("HK", "zh-TW"), ("VN", "vi"), (None, None)],
)
def test_original_locale_follows_the_country(country: str | None, expected: str | None) -> None:
    assert original_locale_for(country) == expected


def test_resolve_prefers_the_locale_then_the_chain_then_the_original() -> None:
    names = {"zh-TW": "淺草寺", "original": "浅草寺"}
    assert resolve_localized_name(names, "zh-TW") == "淺草寺"
    assert resolve_localized_name(names, "zh-CN") == "淺草寺"
    assert resolve_localized_name(names, "ko") == "淺草寺"
    assert resolve_localized_name({"original": "浅草寺"}, "en") == "浅草寺"
    assert resolve_localized_name({}, "en", fallback="stored") == "stored"
    assert resolve_localized_name(None, "en") is None
    assert original_name(names) == "浅草寺"
    assert original_name({"zh-TW": "淺草寺"}) is None


def test_latin_script_detection_and_sanitizing() -> None:
    assert is_latin_script("Nakamise-dori")
    assert is_latin_script("Sensō-ji")
    assert not is_latin_script("仲見世通り")
    assert not is_latin_script("동문재래시장")
    assert not is_latin_script("ทิพย์สมัย")
    assert not is_latin_script("   ")
    assert sanitize_localized_names({"en": " x ", "fr": "y", "ja": "", "original": "原"}) == {
        "en": "x",
        "original": "原",
    }
    assert has_localized_names({"original": "原"}) is False
    assert has_localized_names({"ko": "서울"}) is True


def test_join_combines_maps_locale_by_locale() -> None:
    dish = {"zh-TW": "拉麵", "en": "Ramen", "ja": "ラーメン", "original": "ラーメン"}
    merchant = {
        "zh-TW": "一蘭",
        "en": "Ichiran",
        "ja": "一蘭 渋谷店",
        "original": "一蘭 渋谷店",
        "original_locale": "ja",
    }
    joined = join_localized_names(dish, merchant)
    assert joined["zh-TW"] == "拉麵 · 一蘭"
    assert joined["en"] == "Ramen · Ichiran"
    assert joined["original"] == "ラーメン · 一蘭 渋谷店"
    assert joined["original_locale"] == "ja"
    assert "ko" not in joined
    assert join_localized_names(None, merchant)["en"] == "Ichiran"
    assert join_localized_names({"en": "Park"}, {"en": "Park"})["en"] == "Park"


def test_item_names_drop_empty_fields_and_resolve_per_field() -> None:
    labels = {"zh-TW": "淺草寺", "en": "Sensō-ji", "original": "浅草寺"}
    names = item_names(title=labels, location_name={"original": "only original"})
    assert names == {"title": labels}
    assert resolve_item_field(names, "title", "en", fallback="stored") == "Sensō-ji"
    assert resolve_item_field(names, "title", "ko", fallback="stored") == "Sensō-ji"
    assert resolve_item_field(names, "location_name", "en", fallback="stored") == "stored"
    assert resolve_item_field({}, "title", "en", fallback=None) is None
