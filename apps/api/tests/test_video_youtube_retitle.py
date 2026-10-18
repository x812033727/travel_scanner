"""The run that gives the videos already on the channel the captions tag (video_youtube.retitle)."""

from __future__ import annotations

from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from typing import Any

import pytest

from app.models import AdminAuditLog
from app.video_youtube import retitle
from app.video_youtube.client import YoutubeError

ZH = "｜CC字幕"
EN = "｜CC Subtitles"
JA = "｜字幕付き"


def _video(video_id: str, title: str, **extra: Any) -> dict[str, Any]:
    snippet = {
        "title": title,
        "description": "說明",
        "tags": ["AI"],
        "categoryId": "28",
        "defaultLanguage": "zh-TW",
        "defaultAudioLanguage": "zh-TW",
        "channelId": "UC1",
        "thumbnails": {"default": {"url": "x"}},
    }
    snippet.update(extra.pop("snippet", {}))
    return {
        "id": video_id,
        "snippet": snippet,
        "status": {"privacyStatus": "public", "license": "youtube", "uploadStatus": "processed"},
        "localizations": extra.pop("localizations", {}),
    }


class FakeYoutube:
    def __init__(self, videos: list[dict[str, Any]], *, fail_on: str | None = None) -> None:
        self.items = {video["id"]: video for video in videos}
        self.order = [video["id"] for video in videos]
        self.fail_on = fail_on
        self.sent: list[dict[str, Any]] = []
        self.pages = 0

    async def uploads_playlist(self) -> str:
        return "UU1"

    async def playlist_page(
        self, playlist_id: str, page_token: str | None = None
    ) -> tuple[list[str], str | None]:
        assert playlist_id == "UU1"
        self.pages += 1
        start = int(page_token or 0)
        page = self.order[start : start + 2]  # two per page, so paging is exercised
        rest = start + 2
        return page, (str(rest) if rest < len(self.order) else None)

    async def videos(self, video_ids: Sequence[str], *, parts: str) -> list[dict[str, Any]]:
        assert parts == "snippet,status,localizations"
        return [self.items[video_id] for video_id in video_ids]

    async def update_video(self, body: dict[str, Any]) -> dict[str, Any]:
        if body["id"] == self.fail_on:
            raise YoutubeError(403, "quotaExceeded", "quota")
        self.sent.append(body)
        return body


class FakeSession:
    def __init__(self) -> None:
        self.added: list[Any] = []
        self.commits = 0

    def add(self, row: Any) -> None:
        self.added.append(row)

    async def commit(self) -> None:
        self.commits += 1


def _link(monkeypatch: pytest.MonkeyPatch, youtube: FakeYoutube) -> None:
    @asynccontextmanager
    async def linked(_session: Any) -> AsyncIterator[tuple[str, Any]]:
        yield "UC1", youtube

    monkeypatch.setattr(retitle, "_linked_youtube", linked)


def test_the_tag_follows_each_language_youtube_names() -> None:
    assert [retitle.tag_language(code) for code in ("zh-Hant", "zh-TW", "zh-CN", None, "")] == [
        "zh-TW"
    ] * 5
    assert [retitle.tag_language(code) for code in ("en-US", "en", "ja", "ko-KR", "fr")] == [
        "en",
        "en",
        "ja",
        "ko",
        "en",
    ]


def test_the_update_keeps_everything_and_tags_every_title() -> None:
    video = _video(
        "v1", "AI 模型怎麼挑", localizations={"ja": {"title": "選び方", "description": "d"}}
    )
    body = retitle.update_body(video)
    assert body["snippet"] == {
        "title": f"AI 模型怎麼挑{ZH}",
        "description": "說明",
        "tags": ["AI"],
        "categoryId": "28",
        "defaultLanguage": "zh-TW",
        "defaultAudioLanguage": "zh-TW",
    }
    assert body["status"] == {"privacyStatus": "public", "license": "youtube"}
    assert body["localizations"] == {"ja": {"title": f"選び方{JA}", "description": "d"}}
    assert video["snippet"]["title"] == "AI 模型怎麼挑", "the input is not mutated"


def test_a_title_the_tag_would_push_past_100_characters_is_reported_not_cut() -> None:
    found = retitle.plan(_video("v1", "字" * 96))
    assert found["titles"] == {"zh-TW": ["字" * 96, "字" * 96 + "｜CC"]}
    assert found["problem"] is None, "the short tag fits"
    found = retitle.plan(_video("v1", "字" * 98))
    assert found["titles"] == {}
    assert found["problem"] is not None and "103" in found["problem"]
    assert retitle.plan(_video("v2", f"已經有了{ZH}"))["titles"] == {}


def test_only_the_title_too_long_for_a_tag_is_left_the_others_are_tagged() -> None:
    long_en = "a" * 98
    video = _video(
        "v1",
        "溫度是什麼",
        localizations={
            "en": {"title": long_en, "description": "d"},
            "ja": {"title": "温度とは", "description": "d"},
        },
    )
    found = retitle.plan(video)
    assert found["titles"] == {
        "zh-TW": ["溫度是什麼", f"溫度是什麼{ZH}"],
        "ja": ["温度とは", f"温度とは{JA}"],
    }
    assert found["problem"] is not None and found["problem"].startswith("en ")
    body = retitle.update_body(video)
    assert body["snippet"]["title"] == f"溫度是什麼{ZH}"
    assert body["localizations"]["en"]["title"] == long_en, "left as it is, not cut"
    assert body["localizations"]["ja"]["title"] == f"温度とは{JA}"


async def test_a_report_sends_nothing_and_counts_the_quota(monkeypatch: pytest.MonkeyPatch) -> None:
    youtube = FakeYoutube(
        [
            _video("v1", "一"),
            _video("v2", f"二{ZH}"),
            _video("v3", "三", snippet={"defaultLanguage": "en"}),
            _video("v4", "字" * 99),
            _video("v5", f"五{ZH}", localizations={"en": {"title": "five", "description": ""}}),
            _video("demo", "OAuth demo"),
        ]
    )
    _link(monkeypatch, youtube)
    session = FakeSession()
    report = await retitle.caption_channel_titles(
        session,  # type: ignore[arg-type]
        apply=False,
        skip=frozenset({"demo"}),
    )
    assert youtube.pages == 3 and youtube.sent == [] and session.added == []
    counts = (report["videos"], report["to_change"], report["too_long"], report["left"])
    assert counts == (6, 3, 1, 3)
    assert report["units_for_updates"] == 150 and report["skipped"] == ["demo"]
    # v4 cannot take a tag at all: it is reported with nothing to change, every run.
    assert {item["id"]: item["titles"] for item in report["plans"]} == {
        "v1": {"zh-TW": ["一", f"一{ZH}"]},
        "v3": {"en": ["三", f"三{EN}"]},
        "v4": {},
        "v5": {"en": ["five", f"five{EN}"]},
    }


async def test_apply_sends_up_to_the_limit_and_audits_each(monkeypatch: pytest.MonkeyPatch) -> None:
    youtube = FakeYoutube([_video("v1", "一"), _video("v2", "二"), _video("v3", "三")])
    _link(monkeypatch, youtube)
    session = FakeSession()
    report = await retitle.caption_channel_titles(session, apply=True, limit=2)  # type: ignore[arg-type]
    assert [body["snippet"]["title"] for body in youtube.sent] == [f"一{ZH}", f"二{ZH}"]
    assert (report["changed"], report["left"], report["error"]) == (2, 1, None)
    assert all(isinstance(row, AdminAuditLog) for row in session.added) and session.commits == 2
    assert session.added[0].metadata_json == {
        "youtube_video_id": "v1",
        "titles": {"zh-TW": ["一", f"一{ZH}"]},
    }


async def test_a_refused_update_ends_the_run(monkeypatch: pytest.MonkeyPatch) -> None:
    youtube = FakeYoutube(
        [_video("v1", "一"), _video("v2", "二"), _video("v3", "三")], fail_on="v2"
    )
    _link(monkeypatch, youtube)
    report = await retitle.caption_channel_titles(FakeSession(), apply=True)  # type: ignore[arg-type]
    assert [body["id"] for body in youtube.sent] == ["v1"]
    assert (report["changed"], report["left"]) == (1, 2)
    assert report["error"] is not None and report["error"].startswith("v2")


def test_a_title_given_new_words_is_tagged_in_them_and_the_old_words_are_recorded() -> None:
    long_en = "a" * 98
    video = _video("v1", "溫度是什麼", localizations={"en": {"title": long_en, "description": "d"}})
    found = retitle.plan(video, {"en": "Temperature"})
    assert found["titles"] == {
        "zh-TW": ["溫度是什麼", f"溫度是什麼{ZH}"],
        "en": [long_en, f"Temperature{EN}"],
    }
    assert found["problem"] is None
    body = retitle.update_body(video, {"en": "Temperature"})
    assert body["localizations"]["en"] == {"title": f"Temperature{EN}", "description": "d"}
    unknown = retitle.plan(video, {"ko": "x"})["problem"] or ""
    assert unknown.startswith("ko 不是這支影片的語言，沒有改；en ")


async def test_new_words_reach_the_update_and_an_unknown_video_is_reported(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    youtube = FakeYoutube(
        [_video("v1", "一", localizations={"en": {"title": "a" * 98, "description": ""}})]
    )
    _link(monkeypatch, youtube)
    report = await retitle.caption_channel_titles(
        FakeSession(),  # type: ignore[arg-type]
        apply=True,
        rename={"v1": {"en": "One"}, "gone": {"en": "x"}},
    )
    assert report["changed"] == 1 and report["renamed_missing"] == ["gone"]
    assert youtube.sent[0]["localizations"]["en"]["title"] == f"One{EN}"
    assert youtube.sent[0]["snippet"]["title"] == f"一{ZH}"
