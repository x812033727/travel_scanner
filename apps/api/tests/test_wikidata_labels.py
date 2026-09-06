"""The Wikidata label backfill edits only what the seed cannot derive and keeps file style."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx
import pytest

from app.hotspots.wikidata_labels import (
    BOOTSTRAP_FILES,
    REQUESTED_LANGUAGES,
    apply_labels,
    detect_style,
    fetch_labels,
    fill_bootstrap_files,
    render_rows,
    site_labels,
)

HOTSPOTS_DIR = Path(__file__).resolve().parents[1] / "app" / "hotspots"
COUNTRY_BY_CITY = {"NRT": "JP", "BKK": "TH", "TPE": "TW", "ICN": "KR"}


def test_site_labels_prefer_the_most_specific_chinese_variant() -> None:
    labels = site_labels(
        {"en": "Sensō-ji", "ja": "浅草寺", "zh": "淺草寺", "zh-hans": "浅草寺", "zh-tw": " 淺草寺 "}
    )
    assert labels == {"en": "Sensō-ji", "ja": "浅草寺", "zh-TW": "淺草寺", "zh-CN": "浅草寺"}
    assert site_labels({"zh": "淺草寺"}) == {"zh-TW": "淺草寺", "zh-CN": "淺草寺"}
    assert set(REQUESTED_LANGUAGES) >= {"en", "ja", "ko", "zh-hant", "zh-hans", "th", "vi"}


def test_apply_labels_fills_the_original_and_stored_locales_only() -> None:
    row: dict[str, Any] = {
        "city_code": "BKK",
        "name": "倫披尼公園",
        "category": "nature",
        "wikidata_item_id": "Q977437",
    }
    labels = {"en": "Lumphini Park", "th": "สวนลุมพินี", "zh-CN": "伦披尼公园", "zh-TW": "倫披尼公園"}
    assert apply_labels(row, labels, country_code="TH") == ["local_name", "names"]
    assert list(row) == ["city_code", "name", "local_name", "names", "category", "wikidata_item_id"]
    assert row["local_name"] == "สวนลุมพินี"
    # Traditional Chinese stays the curated name; a label equal to it is not stored twice.
    # Simplified is not stored either — Wikidata's zh-cn label proved unreliable for these
    # places, so app.hotspots.simplified_names derives it from the Traditional name.
    assert row["names"] == {"en": "Lumphini Park"}
    # Running again is a no-op.
    assert apply_labels(row, labels, country_code="TH") == []


def test_apply_labels_never_overwrites_a_reviewed_original_unless_asked() -> None:
    row: dict[str, Any] = {"city_code": "NRT", "name": "淺草寺", "local_name": "浅草寺"}
    labels = {"ja": "浅草寺（東京都台東区）", "ko": "센소지"}
    assert apply_labels(row, labels, country_code="JP") == ["names"]
    assert row["local_name"] == "浅草寺"
    assert row["names"] == {"ja": "浅草寺（東京都台東区）", "ko": "센소지"}
    assert apply_labels(row, labels, country_code="JP", overwrite_original=True) == ["local_name"]
    assert row["local_name"] == "浅草寺（東京都台東区）"


def test_apply_labels_keeps_chinese_destinations_on_their_curated_name() -> None:
    row: dict[str, Any] = {"city_code": "TPE", "name": "龍山寺"}
    assert apply_labels(
        row, {"zh-TW": "艋舺龍山寺", "en": "Longshan Temple"}, country_code="TW"
    ) == ["names"]
    assert "local_name" not in row
    assert row["names"] == {"en": "Longshan Temple"}


@pytest.mark.parametrize("filename", BOOTSTRAP_FILES)
def test_checked_in_bootstrap_files_round_trip_in_a_known_style(filename: str) -> None:
    text = (HOTSPOTS_DIR / filename).read_text(encoding="utf-8")
    rows = json.loads(text)
    style = detect_style(text, rows)
    assert render_rows(rows, style) == text, f"{filename} is not in a style the tool can keep"


def test_render_styles_differ_only_in_array_layout() -> None:
    rows = [{"name": "x", "aliases": ["a", "b"], "source_urls": ["https://e.test/" + "a" * 90]}]
    plain = render_rows(rows, "indent")
    inline = render_rows(rows, "inline_arrays")
    short = render_rows(rows, "inline_short_arrays")
    assert '"aliases": [\n' in plain
    assert '"aliases": ["a", "b"]' in inline and '"source_urls": ["https' in inline
    assert '"aliases": ["a", "b"]' in short and '"source_urls": [\n' in short
    assert json.loads(plain) == json.loads(inline) == json.loads(short) == rows


def test_fill_bootstrap_files_is_a_dry_run_first_and_keeps_the_file_style(tmp_path: Path) -> None:
    rows = [
        {
            "city_code": "NRT",
            "name": "淺草寺",
            "aliases": ["Sensō-ji"],
            "wikidata_item_id": "Q615183",
        },
        {
            "city_code": "ICN",
            "name": "景福宮",
            "aliases": ["Gyeongbokgung"],
            "wikidata_item_id": "Q482485",
        },
        {"city_code": "TPE", "name": "手動景點", "aliases": []},
    ]
    path = tmp_path / "bootstrap.json"
    original = render_rows(rows, "inline_arrays")
    path.write_text(original, encoding="utf-8")
    requested: list[list[str]] = []

    def fake_fetch(qids: Any) -> dict[str, dict[str, str]]:
        requested.append(list(qids))
        return {"Q615183": {"ja": "浅草寺", "ko": "센소지", "en": "Sensō-ji"}}

    report = fill_bootstrap_files(
        tmp_path,
        fetch=fake_fetch,
        files=["bootstrap.json"],
        dry_run=True,
        country_for_city=COUNTRY_BY_CITY.__getitem__,
    )
    assert requested == [["Q482485", "Q615183"]]
    assert report.missing_qids == ["Q482485"]
    assert report.files == {"bootstrap.json": {"rows": 3, "changed": 1, "style": "inline_arrays"}}
    assert report.changed_rows == ["bootstrap.json: 淺草寺 (local_name, names)"]
    assert path.read_text(encoding="utf-8") == original

    fill_bootstrap_files(
        tmp_path,
        fetch=fake_fetch,
        files=["bootstrap.json"],
        country_for_city=COUNTRY_BY_CITY.__getitem__,
    )
    written = path.read_text(encoding="utf-8")
    assert '"aliases": ["Sensō-ji"]' in written
    updated = json.loads(written)[0]
    assert updated["local_name"] == "浅草寺"
    assert updated["names"] == {"en": "Sensō-ji", "ja": "浅草寺", "ko": "센소지"}
    assert json.loads(written)[1] == rows[1]


def test_fetch_labels_batches_requests_and_retries_rate_limits() -> None:
    calls: list[dict[str, str]] = []
    attempts = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        params = dict(request.url.params)
        calls.append(params)
        attempts["count"] += 1
        if attempts["count"] == 1:
            return httpx.Response(429)
        ids = params["ids"].split("|")
        return httpx.Response(
            200,
            json={"entities": {qid: {"labels": {"en": {"value": f"Label {qid}"}}} for qid in ids}},
        )

    qids = [f"Q{index}" for index in range(1, 62)]
    naps: list[float] = []
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        labels = fetch_labels(qids, client=client, sleep=naps.append)
    assert len(labels) == 61
    assert labels["Q61"] == {"en": "Label Q61"}
    assert [len(call["ids"].split("|")) for call in calls] == [50, 50, 11]
    assert calls[0]["languages"] == "|".join(REQUESTED_LANGUAGES)
    assert naps[0] == 3  # the 429 backed off before the retry
