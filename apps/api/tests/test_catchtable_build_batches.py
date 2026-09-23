"""The CatchTable converter refuses platform hosts unless merchant_platform proves custody.

``tools/catchtable_build_batches.py`` runs outside the API package (standard library only),
so it is loaded by path. The rules it enforces mirror ``app.foods.trend_import``: an official
source is never a platform, aggregator or social page; the weaker ``merchant_platform`` kind
(2026-09-23) may sit on a platform host, but only on this alias's own CatchTable page or on
the exact URL the shop registered in its /info tab's website field.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

TOOL = Path(__file__).resolve().parents[3] / "tools" / "catchtable_build_batches.py"


def load_tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("catchtable_build_batches", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def record(*, kind: str, url: str, website: str | None = None) -> dict[str, Any]:
    alias = "sinsakkochgedang_apgujeong"
    catchtable: dict[str, Any] = {
        "listed_name": "신사꽃게당 압구정로데오점",
        "listed_address": "서울특별시 강남구 도산대로49길 13 지하1층",
        "localized_urls": {
            "zh-TW": f"https://www.catchtable.net/zh-TW/shop/{alias}",
            "zh-CN": f"https://www.catchtable.net/zh-CN/shop/{alias}",
            "ja": f"https://www.catchtable.net/ja-JP/shop/{alias}",
        },
        "booking": "reservation",
        "booking_observation": "2026-09-23 zh-TW 店頁 DINING 分頁有日期列與尋找可用時間。",
    }
    if website is not None:
        catchtable["website"] = website
    return {
        "alias": alias,
        "outcome": "import",
        "checked_at": "2026-09-23T07:00:00+00:00",
        "ranking_evidence": [
            {
                "page": "https://www.catchtable.net/zh-TW/ranking/location/location-seoul",
                "rank": 25,
                "captured_at": "2026-09-23T06:29:07+00:00",
            }
        ],
        "catchtable": catchtable,
        "merchant": {
            "name_zh": "신사꽃게당 압구정로데오점",
            "local_name": "신사꽃게당 압구정로데오점",
            "category_slugs": ["seafood"],
            "source": {
                "url": url,
                "title": "CatchTable：신사꽃게당 압구정로데오점",
                "kind": kind,
                "quote": "신사꽃게당 압구정로데오점 서울특별시 강남구 도산대로49길 13 지하1층",
            },
        },
    }


def write_candidates(tmp_path: Path, *records: dict[str, Any]) -> Path:
    path = tmp_path / "candidates.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "batch_id": "2026-09-23-test",
                "destination": "seoul",
                "collected_at": "2026-09-23T06:29:07+00:00",
                "rankings": [],
                "records": list(records),
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return path


def test_an_official_kind_on_a_social_host_is_refused(tmp_path: Path) -> None:
    tool = load_tool()
    path = write_candidates(
        tmp_path,
        record(kind="official_tourism", url="https://www.instagram.com/sinsakkochgedang/"),
    )
    with pytest.raises(tool.CandidateFileError, match="never a source"):
        tool.load_candidates(path)


def test_merchant_platform_accepts_the_shops_own_catchtable_info_tab(tmp_path: Path) -> None:
    tool = load_tool()
    path = write_candidates(
        tmp_path,
        record(
            kind="merchant_platform",
            url="https://www.catchtable.net/zh-TW/shop/sinsakkochgedang_apgujeong/info",
        ),
    )
    batch = tool.load_candidates(path)
    rows = tool.build_merchants(batch)
    assert [row["source_kind"] for row in rows] == ["merchant_platform"]


def test_merchant_platform_accepts_only_the_social_account_the_shop_registered(
    tmp_path: Path,
) -> None:
    tool = load_tool()
    registered = "https://www.instagram.com/sinsakkochgedang/"
    ok = write_candidates(
        tmp_path, record(kind="merchant_platform", url=registered, website=registered)
    )
    assert len(tool.load_candidates(ok)["records"]) == 1

    other = tmp_path / "other"
    other.mkdir()
    unregistered = write_candidates(
        other,
        record(
            kind="merchant_platform",
            url="https://www.instagram.com/explore/locations/183777154813291/",
            website=registered,
        ),
    )
    with pytest.raises(tool.CandidateFileError, match="catchtable.website"):
        tool.load_candidates(unregistered)

    nowhere = tmp_path / "nowhere"
    nowhere.mkdir()
    unrecorded = write_candidates(nowhere, record(kind="merchant_platform", url=registered))
    with pytest.raises(tool.CandidateFileError, match="catchtable.website"):
        tool.load_candidates(unrecorded)


def test_merchant_platform_still_refuses_another_shops_catchtable_page(tmp_path: Path) -> None:
    tool = load_tool()
    path = write_candidates(
        tmp_path,
        record(kind="merchant_platform", url="https://www.catchtable.net/shop/someone_else"),
    )
    with pytest.raises(tool.CandidateFileError, match="own"):
        tool.load_candidates(path)
