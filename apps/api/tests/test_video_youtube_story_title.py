"""A brand story's YouTube titles say so before the captions tag (the owner's rule of 2026-10-20,
「…？｜品牌故事｜CC字幕」), whatever package or card text they came from."""

from __future__ import annotations

from app.video_reviews.schemas import ADDED_LOCALES
from app.video_youtube import requests
from tests.test_video_youtube import METADATA


def test_a_story_title_carries_its_story_tag_before_the_captions_tag_once() -> None:
    assert requests.captioned("輪子行李箱為什麼等了這麼久？", "zh-TW", story=True) == (
        "輪子行李箱為什麼等了這麼久？｜品牌故事｜CC字幕"
    )
    assert requests.captioned("Why did wheels wait?", "en", story=True) == (
        "Why did wheels wait?｜Brand Story｜CC Subtitles"
    )
    assert requests.captioned("t", "ja", story=True) == "t｜ブランドストーリー｜字幕付き"
    assert requests.captioned("t", "ko", story=True) == "t｜브랜드 스토리｜CC 자막"
    # A package the worker composed after the rule already has both: nothing is added twice.
    done = "輪子行李箱｜品牌故事｜CC字幕"
    assert requests.captioned(done, "zh-TW", story=True) == done
    # A package from before the rule has only the captions tag: the story tag goes before it.
    assert requests.captioned("輪子行李箱｜CC字幕", "zh-TW", story=True) == done
    # Another language's tags, or tags typed by hand, are replaced rather than added to.
    assert requests.captioned("Wheels | Brand Story | CC字幕", "zh-TW", story=True) == (
        "Wheels｜品牌故事｜CC字幕"
    )
    # The other videos' titles do not change.
    assert requests.captioned("輪子行李箱", "zh-TW") == "輪子行李箱｜CC字幕"
    # Every language a video may have names its own tag.
    assert set(requests.STORY_TAGS) == set(requests.CAPTION_TAGS)
    assert set(requests.STORY_TAGS) >= set(ADDED_LOCALES)


def test_the_story_tag_is_left_off_when_even_the_short_captions_tag_would_not_fit() -> None:
    tag = requests.STORY_TAGS["en"]
    fits = "a" * (requests.TITLE_MAX_CHARS - len(tag) - len(requests.SHORT_CAPTION_TAG))
    assert requests.captioned(fits, "en", story=True) == f"{fits}{tag}｜CC"
    # One more character and the story tag goes; the captions tag then fits whole.
    too_long = fits + "a"
    assert requests.captioned(too_long, "en", story=True) == f"{too_long}｜CC Subtitles"


def test_a_story_s_request_bodies_tag_every_title() -> None:
    snippet = requests.insert_body(METADATA, "AI 模型怎麼挑", "d", story=True)["snippet"]
    assert snippet["title"] == "AI 模型怎麼挑｜品牌故事｜CC字幕"
    body = requests.update_body(
        {"id": "v"},
        METADATA,
        title="AI 模型怎麼挑",
        description="d",
        visibility="private",
        publish_at=None,
        story=True,
    )
    assert body["snippet"]["title"] == "AI 模型怎麼挑｜品牌故事｜CC字幕"
    assert {locale: entry["title"] for locale, entry in body["localizations"].items()} == {
        "en": "Picking an AI model｜Brand Story｜CC Subtitles",
        "ja": "AIモデルの選び方｜ブランドストーリー｜字幕付き",
    }
    # Without ``story`` the bodies are as before.
    plain = requests.localizations(METADATA)
    assert plain["en"]["title"] == "Picking an AI model｜CC Subtitles"
