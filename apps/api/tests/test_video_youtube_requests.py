"""A Short told without words carries no captions, so none of its titles says it has them
(tools/video/shorts/package.mjs writes ``captions: false`` into its metadata.json)."""

from __future__ import annotations

from datetime import UTC, datetime

from app.video_youtube import requests
from tests.test_video_youtube import METADATA

SILENT = {
    **METADATA,
    "captions": False,
    "title": "老公偷吃最後一塊雞排",
    "localizations": {
        "en": {
            "title": "Husband Steals the Last Fried Chicken",
            "description": "A wordless married-couple comedy.",
        },
    },
}


def test_a_video_without_captions_gets_no_captions_tag_in_any_language() -> None:
    assert requests.has_captions(METADATA) is True
    assert requests.has_captions(SILENT) is False
    assert requests.captioned("雞排", "zh-TW", captions=False) == "雞排"
    # A tag typed by hand, in any language, is taken off rather than kept.
    assert requests.captioned("雞排｜CC字幕", "zh-TW", captions=False) == "雞排"
    assert requests.captioned("Chicken | CC Subtitles", "en", captions=False) == "Chicken"
    insert = requests.insert_body(SILENT, SILENT["title"], "說明")
    assert insert["snippet"]["title"] == "老公偷吃最後一塊雞排"
    assert requests.localizations(SILENT) == {
        "en": {
            "title": "Husband Steals the Last Fried Chicken",
            "description": "A wordless married-couple comedy.",
        }
    }
    update = requests.update_body(
        {"id": "v1", "snippet": {}, "status": {}},
        SILENT,
        title=SILENT["title"],
        description="說明",
        visibility="scheduled",
        publish_at=datetime(2026, 11, 10, 12, 0, tzinfo=UTC),
    )
    assert update["snippet"]["title"] == "老公偷吃最後一塊雞排"
    assert update["localizations"]["en"]["title"] == "Husband Steals the Last Fried Chicken"


def test_a_video_with_captions_keeps_its_tag() -> None:
    insert = requests.insert_body(METADATA, METADATA["title"], "說明")
    assert insert["snippet"]["title"] == "AI 模型怎麼挑｜CC字幕"
    assert requests.localizations(METADATA)["en"]["title"] == "Picking an AI model｜CC Subtitles"
