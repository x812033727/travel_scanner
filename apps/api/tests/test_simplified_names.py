from typing import Any

import pytest

from app.hotspots import simplified_names as module
from app.hotspots.simplified_names import (
    acceptable,
    apply_conversions,
    convert_names,
    stored_label_count,
    to_simplified,
)


def test_acceptable_keeps_conversions_and_rejects_rewrites() -> None:
    assert acceptable("曼谷大皇宮", "曼谷大皇宫") is True
    assert acceptable("高尾山", "高尾山") is True
    # A different name of the same length is the failure the length check cannot catch,
    # but a name of a different length always is.
    assert acceptable("倫披尼公園", "是樂園") is False
    assert acceptable("素帖山雙龍寺", "双龙寺") is False
    # Names written the same way in both scripts are legitimately unchanged.
    assert acceptable("東京", "东京") is True
    # Latin, digits and punctuation must survive untouched.
    assert acceptable("中部電力 MIRAI TOWER", "中部电力 MIRAI TOWER") is True
    assert acceptable("中部電力 MIRAI TOWER", "中部电力_MIRAI_TOWER") is False


def test_opencc_converts_characters_and_never_renames() -> None:
    # The case the old model prompt had to forbid by name.
    assert to_simplified("鄭王廟") == "郑王庙"
    assert to_simplified("中部電力 MIRAI TOWER") == "中部电力 MIRAI TOWER"


@pytest.mark.parametrize(
    ("seeded", "simplified"),
    [
        # Seed names of Japanese places keep Japanese forms OpenCC does not know;
        # these are the five the AI conversion got right and plain t2s did not.
        ("楽水園", "乐水园"),
        ("桜井二見ヶ浦", "樱井二见ヶ浦"),
        ("円頓寺商店街", "圆顿寺商店街"),
        ("有楽苑", "有乐苑"),
        ("天神／薬院", "天神／药院"),
    ],
)
def test_japanese_forms_are_simplified_like_their_traditional_ones(
    seeded: str, simplified: str
) -> None:
    assert to_simplified(seeded) == simplified
    assert acceptable(seeded, simplified) is True


def test_the_shinjitai_table_leaves_chinese_characters_and_kana_alone() -> None:
    # 浜 is also a Chinese character (沙家浜); kana are never mapped.
    assert to_simplified("沙家浜") == "沙家浜"
    assert to_simplified("ヶ浦") == "ヶ浦"


def test_names_are_sorted_into_converted_unchanged_and_rejected() -> None:
    report = convert_names(["曼谷大皇宮", "高尾山", "東京鐵塔", "鄭王廟", "", "高尾山"])

    assert report.converted == {
        "曼谷大皇宮": "曼谷大皇宫",
        "東京鐵塔": "东京铁塔",
        "鄭王廟": "郑王庙",
    }
    # Deduplicated, and a blank name is skipped rather than reported.
    assert report.unchanged == ["高尾山"]
    assert report.rejected == []


def test_a_conversion_that_fails_the_shape_check_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # OpenCC's phrase table never rewrites a name like this; the check is what would
    # catch it if it did, so stand in for a bad table entry.
    bad = {"倫披尼公園": "是樂園"}
    monkeypatch.setattr(module, "to_simplified", lambda name: bad.get(name, name))

    report = convert_names(["倫披尼公園", "高尾山"])

    assert report.converted == {}
    assert report.unchanged == ["高尾山"]
    assert report.rejected == [("倫披尼公園", "是樂園")]


def test_stored_label_count_reports_what_a_run_would_touch() -> None:
    rows: list[dict[str, Any]] = [
        {"name": "曼谷大皇宮", "names": {"zh-CN": "曼谷大皇宫", "ja": "王宮"}},
        {"name": "暹羅海洋世界", "names": {"zh-CN": "暹羅海洋世界"}},
        {"name": "高尾山"},
    ]

    assert stored_label_count(rows) == 2


def test_a_row_only_loses_its_label_in_the_step_that_could_replace_it() -> None:
    """Clearing every label up front let a failed run write the stripped rows out."""
    rows: list[dict[str, Any]] = [
        {"name": "曼谷大皇宮", "names": {"zh-CN": "曼谷大皇宫", "ja": "王宮"}},
        {"name": "暹羅海洋世界", "names": {"zh-CN": "暹羅海洋世界"}},
    ]

    # A run that converted nothing must not be able to empty anything, because the
    # caller refuses to write at all; applying an empty map is the last line of defence.
    assert apply_conversions(rows, {"曼谷大皇宮": "曼谷大皇宫"}) == 1
    assert rows[0]["names"]["zh-CN"] == "曼谷大皇宫"
    assert rows[0]["names"]["ja"] == "王宮"  # other locales are untouched
    # The second row had no conversion, so its stale label goes rather than survive.
    assert "zh-CN" not in rows[1]["names"]


def test_conversions_are_written_onto_the_matching_seed_only() -> None:
    rows: list[dict[str, Any]] = [
        {"name": "曼谷大皇宮", "names": {"ja": "王宮"}},
        {"name": "高尾山", "names": {}},
    ]

    assert apply_conversions(rows, {"曼谷大皇宮": "曼谷大皇宫"}) == 1
    assert rows[0]["names"] == {"ja": "王宮", "zh-CN": "曼谷大皇宫"}
    assert rows[1]["names"] == {}
