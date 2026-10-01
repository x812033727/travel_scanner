"""A long drama series: what the worker does next, the documents' shapes, and the routes."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy import delete, select

from app.auth.service import current_user
from app.db import SessionFactory, engine, get_session
from app.models import User, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api
from app.video_automation import series as service
from app.video_automation import settings as settings_service
from app.video_automation.models import (
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaRequest,
    VideoDramaSeries,
)
from app.video_automation.requests import request_view
from app.video_automation.schemas import (
    DramaRequestIn,
    SeriesDocSubmitIn,
    SeriesEpisodeRecapIn,
    SeriesIn,
    SeriesJobOut,
    SeriesOut,
    SeriesPatch,
    SeriesWithdrawnOut,
    StoryLook,
)
from app.video_speech import admin_api as speech_api

WHEN = datetime(2026, 9, 27, 1, 0, tzinfo=UTC)


def _series(**changes: Any) -> VideoDramaSeries:
    values: dict[str, Any] = {
        "id": uuid4(),
        "slug": "xianxia",
        "kind": "series",
        "title": "問劍",
        "premise": "兩個少年在正道與魔道之間",
        "aspects": ["world", "bonds"],
        "tone": "dual-male-leads-subtext",
        "style_preset": "cinematic-3d",
        "target_minutes": 3,
        "planned_episodes": 25,
        "episodes_per_chapter": 10,
        "open_ended": True,
        "status": "active",
        "note": None,
        "requested_chapter": None,
        "force_next": False,
        "created_at": WHEN,
        "updated_at": WHEN,
    }
    values.update(changes)
    return VideoDramaSeries(**values)


def _doc(kind: str, chapter: int = 0, version: int = 1, status: str = "approved") -> VideoDramaDoc:
    return VideoDramaDoc(
        id=uuid4(),
        kind=kind,
        chapter_number=chapter,
        version=version,
        body_md="# doc",
        body_json={},
        status=status,
        note="再緊一點" if status == "rejected" else None,
        created_at=WHEN,
    )


def _episode(number: int, status: str = "ready", series: VideoDramaSeries | None = None) -> Any:
    return VideoDramaEpisode(
        id=uuid4(),
        series_id=series.id if series else uuid4(),
        number=number,
        chapter_number=(number - 1) // 10 + 1,
        title=f"第 {number} 集",
        logline="",
        beats={},
        status=status,
        state_json={},
        created_at=WHEN,
        updated_at=WHEN,
    )


def _settings(**changes: Any) -> VideoAutomationSettings:
    values: dict[str, Any] = {
        "series_max_in_flight": 1,
        "series_script_gate": True,
        "series_auto_continue": True,
        "series_chapter_ahead": 2,
        "series_doc_rewrites": 2,
        "series_episodes_per_month": 30,
    }
    values.update(changes)
    return VideoAutomationSettings(**values)


def _next(
    series: VideoDramaSeries,
    docs: list[VideoDramaDoc],
    episodes: list[Any],
    settings: VideoAutomationSettings | None = None,
    started_this_month: int = 0,
) -> service.NextJob | None:
    return service.next_job_for(
        series, docs, episodes, settings or _settings(), started_this_month=started_this_month
    )


def test_chapters_are_cut_from_the_episode_count_and_the_last_one_may_be_short() -> None:
    series = _series()
    assert service.chapter_count(25, 10) == 3
    assert service.chapter_count(100, 10) == 10
    assert service.chapter_range(series, 1) == (1, 10)
    assert service.chapter_range(series, 3) == (21, 25)
    assert service.chapter_of(series, 11) == 2


def test_documents_are_planned_in_order_and_rewritten_from_a_note_a_limited_number_of_times() -> (
    None
):
    setting = _series(status="setting")
    first = _next(setting, [], [])
    assert first is not None and (first.kind, first.previous, first.rewrites_left) == (
        "setting",
        None,
        2,
    )
    rejected = _doc("setting", status="rejected")
    again = _next(setting, [rejected], [])
    assert again is not None and again.previous is rejected and again.rewrites_left == 2
    twice = _doc("setting", version=3, status="rejected")
    assert _next(setting, [_doc("setting", version=2, status="rejected"), twice], []) is None
    assert _next(setting, [_doc("setting", status="review")], []) is None, "the owner is reading it"
    outline = _series(status="outline")
    job = _next(outline, [_doc("setting")], [])
    assert job is not None and job.kind == "outline"
    assert _next(_series(status="paused"), [], []) is None


def test_chapter_one_is_planned_before_any_episode_and_the_next_when_its_turn_is_near() -> None:
    series = _series()
    approved = [_doc("setting"), _doc("outline")]
    job = _next(series, approved, [_episode(n, "planned") for n in range(1, 26)])
    assert job is not None and (job.kind, job.chapter_number) == ("chapter", 1)

    chapter_one = approved + [_doc("chapter", 1)]
    episodes = [_episode(n, "ready") for n in range(1, 11)] + [
        _episode(n, "planned") for n in range(11, 26)
    ]
    job = _next(series, chapter_one, episodes)
    assert job is not None and (job.kind, job.episode_number) == ("episode", 1)

    # Episodes 1-7 are done: chapter 2 is not due yet (10 - 2 = 8), so episode 8 goes first.
    done = [_episode(n, "done") for n in range(1, 8)] + [_episode(n, "ready") for n in range(8, 11)]
    job = _next(series, chapter_one, done + episodes[10:])
    assert job is not None and (job.kind, job.episode_number) == ("episode", 8)
    # Episode 8 started: chapter 2 is due, and it is planned while episode 8 is in the making.
    near = (
        [_episode(n, "done") for n in range(1, 8)]
        + [_episode(8, "started")]
        + [_episode(n, "ready") for n in (9, 10)]
    )
    job = _next(series, chapter_one, near + episodes[10:])
    assert job is not None and (job.kind, job.chapter_number) == ("chapter", 2)
    # The owner asked for chapter 2 early.
    early = _series(requested_chapter=2)
    job = _next(
        early, chapter_one, done[:3] + [_episode(n, "ready") for n in range(4, 11)] + episodes[10:]
    )
    assert job is not None and (job.kind, job.chapter_number) == ("chapter", 2)
    # Chapter 2 waits for the owner: no chapter job, the episodes still move.
    waiting = chapter_one + [_doc("chapter", 2, status="review")]
    job = _next(series, waiting, done + episodes[10:])
    assert job is not None and (job.kind, job.episode_number) == ("episode", 8)


def test_episodes_start_one_at_a_time_after_the_previous_is_done_unless_the_owner_pushes() -> None:
    series = _series()
    docs = [_doc("setting"), _doc("outline"), _doc("chapter", 1)]
    ready = [_episode(n, "ready") for n in range(1, 11)]
    in_flight = [_episode(1, "started")] + ready[1:]
    assert _next(series, docs, in_flight) is None, "one at a time"
    assert _next(series, docs, in_flight, _settings(series_max_in_flight=2)) is None, (
        "episode 1 is not done"
    )
    job = _next(_series(force_next=True), docs, in_flight, _settings(series_max_in_flight=2))
    assert job is not None and job.episode_number == 2, "the owner said start the next one"
    finished = [_episode(1, "done")] + ready[1:]
    job = _next(series, docs, finished)
    assert job is not None and job.episode_number == 2
    assert _next(series, docs, finished, _settings(series_auto_continue=False)) is None
    skipped = [_episode(1, "done"), _episode(2, "skipped")] + ready[2:]
    job = _next(series, docs, skipped)
    assert job is not None and job.episode_number == 3
    assert _next(series, docs, finished, started_this_month=30) is None, "the month's cap"
    assert _next(series, docs, [_episode(n, "planned") for n in range(1, 11)]) is None, (
        "nothing ready"
    )


@pytest.mark.parametrize(
    "looks",
    [
        None,
        {},
        [{"id": "present", "appearance": ""}],
        [{"id": "present", "appearance": "x", "voice": {"name": "other"}}],
        [{"id": "present", "appearance": "x"}] * 2,
        [{"id": "../bad", "appearance": "x"}],
        [{"id": "present", "appearance": "x" * 801}],
    ],
)
def test_setting_refuses_invalid_shot_looks(looks: Any) -> None:
    payload = SeriesDocSubmitIn(
        kind="setting",
        body_md="# setting",
        body_json={
            "characters": [
                {"id": "lead", "name": "主角", "appearance": "base", "shot_looks": looks}
            ]
        },
    )
    assert service.doc_problem(_series(), payload) is not None


def test_setting_accepts_named_visual_variants_without_replacing_character_identity() -> None:
    payload = SeriesDocSubmitIn(
        kind="setting",
        body_md="# setting",
        body_json={
            "characters": [
                {
                    "id": "lead",
                    "name": "主角",
                    "appearance": "base face",
                    "voice": {"provider": "gemini", "name": "Kore"},
                    "shot_looks": [
                        {"id": "past", "appearance": "young woman in an ancient robe"},
                        {"id": "present", "appearance": "adult woman in a business suit"},
                    ],
                }
            ]
        },
    )
    assert service.doc_problem(_series(), payload) is None
    assert payload.body_json["characters"][0]["voice"]["name"] == "Kore"


def test_a_document_the_worker_sends_must_have_the_shape_the_owner_reads() -> None:
    series = _series()

    def doc(kind: str, chapter: int = 0, **body: Any) -> SeriesDocSubmitIn:
        return SeriesDocSubmitIn(kind=kind, chapter_number=chapter, body_md="# x", body_json=body)

    assert "characters" in str(service.doc_problem(series, doc("setting")))
    assert (
        service.doc_problem(
            series, doc("setting", characters=[{"id": "a", "name": "阿", "appearance": "x"}])
        )
        is None
    )
    assert "3 chapters" in str(service.doc_problem(series, doc("outline", chapters=[])))
    chapters = [
        {
            "number": k,
            "title": f"第 {k} 篇",
            "episodes": [
                {"number": n, "title": f"第 {n} 集", "logline": "…"}
                for n in range(*service.chapter_range(series, k))
            ]
            + [{"number": service.chapter_range(series, k)[1], "title": "尾", "logline": "…"}],
        }
        for k in (1, 2, 3)
    ]
    assert service.doc_problem(series, doc("outline", chapters=chapters)) is None
    beats = {"hook": "h", "conflict": "c", "turn": "t", "cliffhanger": "x"}
    short = [{"number": n, **beats} for n in range(1, 10)]
    assert "covers episodes 1 to 10" in str(
        service.doc_problem(series, doc("chapter", 1, episodes=short))
    )
    lacking = [{"number": n, **beats} for n in range(1, 11)]
    lacking[3] = {"number": 4, "hook": "h"}
    assert "episode 4 lacks conflict, turn, cliffhanger" in str(
        service.doc_problem(series, doc("chapter", 1, episodes=lacking))
    )
    assert (
        service.doc_problem(
            series, doc("chapter", 1, episodes=[{"number": n, **beats} for n in range(1, 11)])
        )
        is None
    )
    assert "outside" in str(service.doc_problem(series, doc("chapter", 9, episodes=[])))

    rows = service.episode_rows_from_outline(series, {"chapters": chapters[:1]})
    assert rows[1]["title"] == "第 1 集" and rows[25]["title"] == "第 25 集" and len(rows) == 25
    planned = service.beats_from_chapter(
        {"episodes": [{"number": 2, **beats, "tension": [2, 3, 3, 4, 5]}]}
    )
    assert planned[2]["tension"] == [2, 3, 3, 4, 5]


BIBLE = {
    "characters": [{"id": "jingwei", "name": "精衛", "appearance": "x"}],
    "acts": [{"number": 1, "title": "溺水"}, {"number": 2, "title": "化鳥"}],
    "outline": {
        "title": "精衛填海",
        "logline": "一隻鳥要填平東海",
        "hook": "h",
        "conflict": "c",
        "turn": "t",
        "cliffhanger": "x",
    },
    "music": "古琴",
    "not_doing": ["不寫戀愛"],
    "lexicon": {"東海": "the sea"},
}


def _one_off(**changes: Any) -> VideoDramaSeries:
    values: dict[str, Any] = {
        "slug": "one-off-1a2b3c4d",
        "kind": "one-off",
        "title": "精衛填海",
        "aspects": [],
        "planned_episodes": 1,
        "episodes_per_chapter": 1,
        "open_ended": False,
        "status": "setting",
    }
    values.update(changes)
    return _series(**values)


def test_a_one_off_is_one_episode_with_one_story_bible_whatever_the_form_sent() -> None:
    one_off = SeriesIn(
        slug="one-off-x", kind="one-off", title="精衛填海", premise="p", planned_episodes=30
    )
    assert (one_off.planned_episodes, one_off.episodes_per_chapter, one_off.open_ended) == (
        1,
        1,
        False,
    )
    assert one_off.aspects == [] and one_off.tone == "dual-male-leads-subtext"
    series = SeriesIn(slug="xianxia", title="問劍", premise="p")
    assert (series.kind, series.planned_episodes, series.episodes_per_chapter) == (
        "series",
        100,
        10,
    )
    with pytest.raises(ValidationError, match="at least 4"):
        SeriesIn(slug="xianxia", title="問劍", premise="p", episodes_per_chapter=2)
    with pytest.raises(ValidationError):
        SeriesIn(slug="xianxia", kind="movie", title="問劍", premise="p")  # type: ignore[arg-type]
    assert service.one_off_slug("1a2b3c4d-0000-4000-8000-000000000000") == "one-off-1a2b3c4d"


def test_a_one_off_plans_its_bible_then_starts_its_episode_and_never_a_chapter() -> None:
    fresh = _one_off()
    job = _next(fresh, [], [_episode(1, "planned", fresh)])
    assert job is not None and (job.kind, job.previous, job.rewrites_left) == ("bible", None, 2)
    rejected = _doc("bible", status="rejected")
    again = _next(fresh, [rejected], [_episode(1, "planned", fresh)])
    assert again is not None and again.kind == "bible" and again.previous is rejected
    assert _next(fresh, [_doc("bible", status="review")], []) is None, "the owner is reading it"
    active = _one_off(status="active")
    job = _next(active, [_doc("bible")], [_episode(1, "ready", active)])
    assert job is not None and (job.kind, job.episode_number) == ("episode", 1), (
        "no chapter outline stands between the bible and the episode"
    )
    assert _next(active, [_doc("bible")], [_episode(1, "started", active)]) is None
    assert _next(active, [_doc("bible")], [_episode(1, "done", active)]) is None
    assert service.setting_kind(active) == "bible" and service.setting_kind(_series()) == "setting"


def test_a_story_bible_has_the_cast_the_acts_and_one_outline_and_only_a_one_off_has_one() -> None:
    one_off = _one_off()

    def doc(kind: str, **body: Any) -> SeriesDocSubmitIn:
        return SeriesDocSubmitIn(kind=kind, body_md="# x", body_json=body)

    assert service.doc_problem(one_off, doc("bible", **BIBLE)) is None
    assert "characters" in str(service.doc_problem(one_off, doc("bible", acts=[{}], outline={})))
    assert "acts" in str(
        service.doc_problem(one_off, doc("bible", characters=BIBLE["characters"], outline={}))
    )
    assert "outline" in str(
        service.doc_problem(
            one_off, doc("bible", characters=BIBLE["characters"], acts=[{}], outline="x")
        )
    )
    assert "one document" in str(
        service.doc_problem(one_off, doc("setting", characters=BIBLE["characters"]))
    )
    assert "setting book" in str(service.doc_problem(_series(), doc("bible", **BIBLE)))


# A character with looks (docs/videos/SERIES.md, 換裝與變化); the series has 25 episodes.
GEMINI_VOICE = {"provider": "gemini", "name": "Kore", "style": "calm"}
LOOKS = [
    {"id": "coatless", "from": 3, "to": 5, "appearance": "no coat, white shirt"},
    {
        "id": "wheelchair",
        "from": 6,
        "to": None,
        "appearance": "in a wheelchair",
        "sheet_prompt": "full body, seated",
        "voice_style": "tired",
    },
]


def _setting_with(looks: Any, **character: Any) -> SeriesDocSubmitIn:
    lin = {"id": "lin", "name": "林", "appearance": "a long coat", "voice": GEMINI_VOICE}
    lin.update(character)
    if looks is not ...:
        lin["looks"] = looks
    return SeriesDocSubmitIn(
        kind="setting",
        body_md="# x",
        body_json={"characters": [{"id": "a", "name": "阿", "appearance": "x"}, lin]},
    )


def test_a_setting_book_may_give_a_character_looks_for_some_episodes() -> None:
    assert service.doc_problem(_series(), _setting_with(...)) is None, "no looks, as before"
    assert service.doc_problem(_series(), _setting_with(LOOKS)) is None
    assert service.doc_problem(_series(), _setting_with([])) is None
    one_off = _one_off()
    bible = {**BIBLE, "characters": [{**BIBLE["characters"][0], "looks": [LOOKS[0] | {"from": 1}]}]}
    assert (
        service.doc_problem(
            one_off, SeriesDocSubmitIn(kind="bible", body_md="# x", body_json=bible)
        )
        is None
    )
    bible["characters"][0]["looks"] = [LOOKS[0] | {"from": 2, "to": None}]
    assert "from 2 is after the last episode (1)" in str(
        service.doc_problem(
            one_off, SeriesDocSubmitIn(kind="bible", body_md="# x", body_json=bible)
        )
    )


@pytest.mark.parametrize(
    ("looks", "character", "problem"),
    [
        ({"id": "coatless"}, {}, "character lin: looks must be a list"),
        (["coatless"], {}, "every look needs an id and an appearance"),
        ([{"id": "coatless", "from": 3}], {}, "every look needs an id and an appearance"),
        ([{**LOOKS[0], "appearance": "  "}], {}, "every look needs an id and an appearance"),
        ([{**LOOKS[0], "id": "Coat"}], {}, "look Coat: the id must be lowercase ascii"),
        ([{**LOOKS[0], "id": "c"}], {}, "look c: the id must be lowercase ascii"),
        ([LOOKS[0], {**LOOKS[1], "id": "coatless"}], {}, "two looks are called coatless"),
        ([{**LOOKS[0], "from": 0}], {}, "look coatless: from must be the number of the first"),
        ([{**LOOKS[0], "from": "3"}], {}, "look coatless: from must be the number of the first"),
        ([{**LOOKS[0], "from": True}], {}, "look coatless: from must be the number of the first"),
        ([{k: v for k, v in LOOKS[0].items() if k != "from"}], {}, "from must be the number"),
        ([{**LOOKS[0], "to": 2}], {}, "look coatless: to must be the number of the last episode"),
        ([{**LOOKS[0], "to": "5"}], {}, "look coatless: to must be the number of the last episode"),
        ([{**LOOKS[0], "from": 26, "to": None}], {}, "from 26 is after the last episode (25)"),
        ([{**LOOKS[0], "sheet_prompt": ""}], {}, "look coatless: sheet_prompt must be text"),
        ([{**LOOKS[1], "voice_style": None}], {}, "look wheelchair: voice_style must be text"),
        (
            LOOKS,
            {"voice": {"provider": "minimax", "name": "x"}},
            "look wheelchair: voice_style needs the character's own Gemini voice",
        ),
        (LOOKS, {"voice": None}, "voice_style needs the character's own Gemini voice"),
        (
            [{**LOOKS[0], "to": 6}, LOOKS[1]],
            {},
            "looks coatless and wheelchair both cover episode 6; one look per episode",
        ),
        (
            [LOOKS[1], {**LOOKS[0], "from": 9, "to": 9}],
            {},
            "looks wheelchair and coatless both cover episode 9; one look per episode",
        ),
    ],
)
def test_a_setting_book_refuses_the_looks_the_worker_would_refuse(
    looks: Any, character: dict[str, Any], problem: str
) -> None:
    found = service.doc_problem(_series(), _setting_with(looks, **character))
    assert found is not None and problem in found, found


def test_an_explainer_bible_has_no_cast_and_answers_its_question_from_named_pages() -> None:
    explainer = _one_off()
    explainer.style_preset = "flat-explainer"
    assert service.is_explainer(explainer) and not service.is_explainer(_one_off())
    assert not service.is_explainer(_series(style_preset="flat-explainer")), "only a one-off"

    def doc(**body: Any) -> SeriesDocSubmitIn:
        return SeriesDocSubmitIn(kind="bible", body_md="# x", body_json=body)

    outline = {
        "question": "為什麼雷聲總比閃電晚到？",
        "answer": "光比聲音快太多。",
        "reasons": ["光速約每秒三十萬公里", "聲速約每秒三百四十公尺"],
        "hook": "閃電亮了，你數到幾？",
        "sources": ["https://en.wikipedia.org/wiki/Speed_of_sound"],
    }
    good = {"characters": [], "acts": [{"number": 1}], "outline": outline}
    assert service.doc_problem(explainer, doc(**good)) is None
    assert "no characters" in str(
        service.doc_problem(explainer, doc(**{**good, "characters": BIBLE["characters"]}))
    )
    assert "answer" in str(
        service.doc_problem(explainer, doc(**{**good, "outline": {**outline, "answer": " "}}))
    )
    assert "reasons" in str(
        service.doc_problem(explainer, doc(**{**good, "outline": {**outline, "reasons": ["x"]}}))
    )
    assert "https" in str(
        service.doc_problem(
            explainer, doc(**{**good, "outline": {**outline, "sources": ["http://x"]}})
        )
    )
    assert "characters" in str(service.doc_problem(_one_off(), doc(**good))), (
        "a story one-off still needs its cast"
    )


def test_only_a_one_off_is_started_in_the_explainer_preset() -> None:
    explainer = SeriesIn(
        slug="one-off-why", kind="one-off", title="雷聲", premise="p", style_preset="flat-explainer"
    )
    assert explainer.style_preset == "flat-explainer"
    assert explainer.target_minutes == 10, "an explainer targets ten minutes by default"
    with pytest.raises(ValidationError, match="an explainer is at least 8 minutes"):
        SeriesIn(
            slug="one-off-why",
            kind="one-off",
            title="雷聲",
            premise="p",
            style_preset="flat-explainer",
            target_minutes=7,
        )
    with pytest.raises(ValidationError, match="one-off explainer only"):
        SeriesIn(slug="xianxia", title="問劍", premise="p", style_preset="flat-explainer")
    with pytest.raises(ValidationError, match="one-off explainer only"):
        SeriesIn(
            slug="stories",
            kind="story",
            title="品牌故事",
            premise="p",
            style_preset="flat-explainer",
            hands_off=True,
            visual_tier="stills",
            look=StoryLook(style="flat", negative="text"),
        )
    for preset in ("cinematic-3d", "anime-2d", "ink-wash", "custom"):
        assert SeriesIn(slug="xianxia", title="問劍", premise="p", style_preset=preset)


def test_a_long_series_never_becomes_an_explainer_and_a_written_bible_fixes_a_one_offs_side() -> (
    None
):
    explainer = {"style_preset": "flat-explainer"}
    story_row = _series(slug="stories", kind="story", hands_off=True, visual_tier="stills")
    for row in (_series(), story_row):
        refused = service.patch_problem(row, explainer)
        assert refused is not None
        assert (refused.status, refused.code) == (422, "video_series_explainer_one_off")
    assert service.patch_problem(_series(), {"style_preset": "anime-2d"}) is None
    # An explainer's length, when the owner names one, is 8 to 20 minutes.
    for minutes in (7, 21):
        short = service.patch_problem(
            _one_off(style_preset="flat-explainer"), {"target_minutes": minutes}
        )
        assert short is not None and short.code == "video_series_explainer_minutes"
    assert (
        service.patch_problem(_one_off(style_preset="flat-explainer"), {"target_minutes": 10})
        is None
    )
    # A one-off crosses the explainer line freely until the worker writes its bible.
    assert service.patch_problem(_one_off(), explainer) is None
    assert (
        service.patch_problem(_one_off(style_preset="flat-explainer"), {"style_preset": "ink-wash"})
        is None
    )
    for status in ("review", "approved", "rejected"):
        written = [_doc("bible", status=status)]
        into = service.patch_problem(_one_off(status="active"), explainer, written)
        assert into is not None and (into.status, into.code) == (
            409,
            "video_series_explainer_fixed",
        )
        out_of = service.patch_problem(
            _one_off(style_preset="flat-explainer"), {"style_preset": "anime-2d"}, written
        )
        assert out_of is not None and out_of.code == "video_series_explainer_fixed"
        # A story one-off may still change between the story presets, and an explainer stay one.
        assert service.patch_problem(_one_off(), {"style_preset": "ink-wash"}, written) is None
        assert (
            service.patch_problem(_one_off(style_preset="flat-explainer"), explainer, written)
            is None
        )


@pytest.mark.asyncio
async def test_a_one_off_crossing_the_explainer_line_takes_that_sides_length(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = AsyncMock()
    session.add = lambda _row: None
    owner = User(email="owner@example.com", password_hash="unused")
    monkeypatch.setattr(service, "_docs", AsyncMock(return_value=[]))
    monkeypatch.setattr(service, "_episodes", AsyncMock(return_value=[]))
    monkeypatch.setattr(service, "series_view", AsyncMock(return_value=None))
    story_one_off = _one_off(target_minutes=3)
    monkeypatch.setattr(service, "_series", AsyncMock(return_value=story_one_off))
    patch = SeriesPatch(style_preset="flat-explainer")
    await service.patch_series(session, owner, story_one_off.slug, patch)
    assert story_one_off.target_minutes == 10, "a style-only change adopts the explainer default"
    explainer = _one_off(style_preset="flat-explainer", target_minutes=11)
    monkeypatch.setattr(service, "_series", AsyncMock(return_value=explainer))
    await service.patch_series(session, owner, explainer.slug, SeriesPatch(style_preset="ink-wash"))
    assert explainer.target_minutes == 3, "a style-only change adopts the ordinary drama default"


def _app(user: User | None = None) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.tool_router, prefix="/api/v1")
    app.include_router(admin_api.admin_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    if user is not None:
        app.dependency_overrides[current_user] = lambda: user
    return app


def _user(role: str) -> User:
    user = User(id=uuid4(), email=f"{role}@example.com", password_hash="unused")
    user._admin_roles_cache = frozenset({role})  # type: ignore[attr-defined]
    return user


def _series_in() -> dict[str, Any]:
    return {
        "slug": "xianxia",
        "title": "問劍",
        "premise": "兩個少年",
        "aspects": ["world", "bonds"],
    }


@pytest.mark.asyncio
async def test_the_owner_routes_need_the_content_capabilities_and_the_drama_switch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    row = _series()
    view = service.summary_view(row, [], [])
    out = SeriesOut(**view.model_dump(), docs=[], episodes=[])
    monkeypatch.setattr(service, "list_series", AsyncMock(return_value=[view]))
    monkeypatch.setattr(service, "create_series", AsyncMock(return_value=out))
    monkeypatch.setattr(service, "decide_doc", AsyncMock(return_value=out))
    monkeypatch.setattr(
        settings_service,
        "settings_row",
        AsyncMock(return_value=VideoAutomationSettings(drama_enabled=False)),
    )
    base = "/api/v1/admin/video-automation/series"
    async with AsyncClient(
        transport=ASGITransport(app=_app(_user("viewer"))), base_url="http://t"
    ) as client:
        listed = await client.get(base)
        refused = await client.post(base, json=_series_in())
    assert listed.status_code == 200 and listed.json()["series"][0]["slug"] == "xianxia"
    assert listed.json()["series"][0]["chapters"] == 3
    assert refused.status_code == 403
    async with AsyncClient(
        transport=ASGITransport(app=_app(_user("owner"))), base_url="http://t"
    ) as client:
        off = await client.post(base, json=_series_in())
        monkeypatch.setattr(
            settings_service,
            "settings_row",
            AsyncMock(return_value=VideoAutomationSettings(drama_enabled=True)),
        )
        created = await client.post(base, json=_series_in())
        bad = await client.post(base, json={**_series_in(), "aspects": ["world", "world"]})
        decided = await client.post(
            f"{base}/xianxia/docs/chapter/2/decision",
            json={"decision": "approve", "expected_version": 1},
        )
        unbound = await client.post(
            f"{base}/xianxia/docs/chapter/2/decision", json={"decision": "approve"}
        )
        unknown = await client.post(
            f"{base}/xianxia/docs/boss/decision",
            json={"decision": "approve", "expected_version": 1},
        )
    assert off.status_code == 409 and off.json()["code"] == "video_drama_disabled"
    assert created.status_code == 201 and created.json()["status"] == "active"
    assert created.json()["kind"] == "series"
    assert bad.status_code == 422
    assert decided.status_code == 200
    assert unbound.status_code == 422
    assert service.decide_doc.await_args.args[3:] == ("chapter", 2, "approve", None)  # type: ignore[attr-defined]
    assert service.decide_doc.await_args.kwargs == {"expected_version": 1}  # type: ignore[attr-defined]
    assert unknown.status_code == 404


@pytest.mark.asyncio
async def test_the_request_form_makes_a_one_off_and_the_list_filters_by_kind(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner = _user("owner")
    one_off = _one_off()
    listed = AsyncMock(return_value=[service.summary_view(one_off, [], [])])
    monkeypatch.setattr(service, "list_series", listed)
    monkeypatch.setattr(
        settings_service,
        "settings_row",
        AsyncMock(return_value=VideoAutomationSettings(drama_enabled=True)),
    )
    request = VideoDramaRequest(
        id=uuid4(),
        premise="精衛填海",
        style_preset="ink-wash",
        target_minutes=2,
        status="queued",
        series_id=one_off.id,
        episode_number=1,
        created_at=WHEN,
    )
    create = AsyncMock(return_value=request_view(request, series_slug=one_off.slug))
    monkeypatch.setattr(service, "create_one_off", create)
    decide = AsyncMock(
        return_value=SeriesOut(**listed.return_value[0].model_dump(), docs=[], episodes=[])
    )
    monkeypatch.setattr(service, "decide_doc", decide)
    base = "/api/v1/admin/video-automation"
    async with AsyncClient(transport=ASGITransport(app=_app(owner)), base_url="http://t") as client:
        only_one_offs = await client.get(f"{base}/series", params={"kind": "one-off"})
        every = await client.get(f"{base}/series")
        bad_kind = await client.get(f"{base}/series", params={"kind": "movie"})
        filed = await client.post(
            f"{base}/drama-requests",
            json={"premise": "精衛填海", "style_preset": "ink-wash", "target_minutes": 2},
        )
        approved = await client.post(
            f"{base}/series/{one_off.slug}/docs/bible/decision",
            json={"decision": "approve", "expected_version": 1},
        )
    assert only_one_offs.status_code == 200
    assert only_one_offs.json()["series"][0]["kind"] == "one-off"
    assert listed.await_args_list[0].kwargs == {"kind": "one-off"}
    assert every.status_code == 200 and listed.await_args_list[1].kwargs == {"kind": None}
    assert bad_kind.status_code == 422
    assert filed.status_code == 201, filed.text
    assert filed.json()["series_slug"] == one_off.slug and filed.json()["episode_number"] == 1
    assert filed.json()["status"] == "queued"
    payload = create.await_args.args[2]
    assert isinstance(payload, DramaRequestIn) and payload.style_preset == "ink-wash"
    assert approved.status_code == 200
    assert decide.await_args.args[3:] == ("bible", 0, "approve", None)


@pytest.mark.asyncio
async def test_withdrawing_a_drama_needs_the_manage_capability_and_says_why_it_was_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    withdrawn = SeriesWithdrawnOut(slug="one-off-1a2b3c4d", requests_cancelled=1)
    started = service.SeriesRefused(409, "video_series_started", "第 1 集已經開始做了，不能撤回")
    withdraw = AsyncMock(side_effect=[withdrawn, started])
    monkeypatch.setattr(service, "withdraw_series", withdraw)
    url = "/api/v1/admin/video-automation/series/one-off-1a2b3c4d"
    async with AsyncClient(
        transport=ASGITransport(app=_app(_user("viewer"))), base_url="http://t"
    ) as client:
        forbidden = await client.delete(url)
    assert forbidden.status_code == 403 and withdraw.await_count == 0
    async with AsyncClient(
        transport=ASGITransport(app=_app(_user("owner"))), base_url="http://t"
    ) as client:
        done = await client.delete(url)
        refused = await client.delete(url)
    assert done.status_code == 200
    assert done.json() == {"slug": "one-off-1a2b3c4d", "requests_cancelled": 1}
    assert withdraw.await_args_list[0].args[2] == "one-off-1a2b3c4d"
    assert refused.status_code == 409 and refused.json()["code"] == "video_series_started"


@pytest.mark.asyncio
async def test_the_owner_routes_refuse_the_explainer_preset_on_a_long_series(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create = AsyncMock()
    monkeypatch.setattr(service, "create_series", create)
    long_series = _series()
    one_off = _one_off(style_preset="flat-explainer", status="active")
    monkeypatch.setattr(service, "_series", AsyncMock(side_effect=[long_series, one_off]))
    monkeypatch.setattr(service, "_docs", AsyncMock(return_value=[_doc("bible")]))
    base = "/api/v1/admin/video-automation/series"
    async with AsyncClient(
        transport=ASGITransport(app=_app(_user("owner"))), base_url="http://t"
    ) as client:
        created = await client.post(base, json={**_series_in(), "style_preset": "flat-explainer"})
        patched = await client.patch(f"{base}/xianxia", json={"style_preset": "flat-explainer"})
        crossed = await client.patch(f"{base}/{one_off.slug}", json={"style_preset": "anime-2d"})
    assert created.status_code == 422 and "one-off explainer only" in created.text
    assert create.await_count == 0
    assert patched.status_code == 422
    assert patched.json()["code"] == "video_series_explainer_one_off"
    assert long_series.style_preset == "cinematic-3d", "the refused change was not applied"
    assert crossed.status_code == 409 and crossed.json()["code"] == "video_series_explainer_fixed"
    assert one_off.style_preset == "flat-explainer"


@pytest.mark.asyncio
async def test_the_worker_routes_need_a_token_and_ask_for_the_next_job(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = _app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        anonymous = await client.get("/api/v1/video/automation/series/next")
    assert anonymous.status_code == 401
    app.dependency_overrides[speech_api.video_tool] = lambda: VideoToolToken(
        id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x"
    )
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(settings_service, "settings_row", AsyncMock(return_value=_settings()))
    monkeypatch.setattr(service, "next_job", AsyncMock(return_value=SeriesJobOut(job=None)))
    problem = service.SeriesRefused(
        422, "video_series_doc_invalid", "a setting book needs a characters list"
    )
    monkeypatch.setattr(service, "submit_doc", AsyncMock(side_effect=problem))
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        nothing = await client.get("/api/v1/video/automation/series/next")
        refused = await client.post(
            "/api/v1/video/automation/series/xianxia/docs",
            json={"kind": "setting", "body_md": "# x", "body_json": {}},
        )
    assert nothing.status_code == 200 and nothing.json() == {"job": None}
    assert refused.status_code == 422 and refused.json()["code"] == "video_series_doc_invalid"


integration = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


@pytest_asyncio.fixture(loop_scope="module")
async def clean_series() -> AsyncIterator[str]:
    slug = f"it-{uuid4().hex[:8]}"
    yield slug
    async with SessionFactory() as session:
        found = await session.scalar(select(VideoDramaSeries).where(VideoDramaSeries.slug == slug))
        if found is not None:
            await session.execute(
                delete(VideoDramaRequest).where(VideoDramaRequest.series_id == found.id)
            )
            await session.delete(found)
            await session.commit()
    await engine.dispose()


@integration
@pytest.mark.asyncio(loop_scope="module")
async def test_a_series_is_planned_document_by_document_and_made_episode_by_episode(
    clean_series: str,
) -> None:
    slug = clean_series
    async with SessionFactory() as session:
        owner = User(email=f"series-{uuid4()}@example.com", password_hash="unused")
        session.add(owner)
        token = VideoToolToken(name="series-test", token_hash=uuid4().hex, token_prefix="mkv_t")
        session.add(token)
        await session.commit()
        settings = await settings_service.settings_row(session)
        created = await service.create_series(
            session,
            owner,
            SeriesIn(
                slug=slug,
                title="問劍",
                premise="兩個少年",
                planned_episodes=25,
                episodes_per_chapter=10,
            ),
        )
        assert created.status == "setting" and created.chapters == 3

        job = (await service.next_job(session, settings)).job
        assert job is not None and job.kind == "setting" and job.series.slug == slug
        await service.submit_doc(
            session,
            slug,
            SeriesDocSubmitIn(
                kind="setting",
                body_md="# 設定集",
                body_json={
                    "characters": [{"id": "a", "name": "阿", "appearance": "x"}],
                    "mysteries": [{"id": "m1"}],
                },
            ),
        )
        assert (await service.next_job(session, settings)).job is None, "the owner is reading it"
        sent_back = await service.decide_doc(
            session, owner, slug, "setting", 0, "reject", "再暗一點", expected_version=1
        )
        assert sent_back.docs[0].status == "rejected"
        job = (await service.next_job(session, settings)).job
        assert job is not None and job.kind == "setting" and job.previous is not None
        assert job.previous.note == "再暗一點" and job.rewrites_left == 2
        await service.submit_doc(
            session,
            slug,
            SeriesDocSubmitIn(
                kind="setting",
                body_md="# 設定集 v2",
                body_json={
                    "characters": [{"id": "a", "name": "阿", "appearance": "x"}],
                    "mysteries": [{"id": "m1"}],
                },
            ),
        )
        approved = await service.decide_doc(
            session, owner, slug, "setting", 0, "approve", None, expected_version=2
        )
        assert approved.status == "outline" and approved.docs[0].version == 2

        job = (await service.next_job(session, settings)).job
        assert job is not None and job.kind == "outline"
        plan = _series(planned_episodes=25)
        chapters = [
            {
                "number": k,
                "title": f"第 {k} 篇",
                "episodes": [
                    {"number": n, "title": f"第 {n} 集", "logline": f"L{n}"}
                    for n in range(
                        service.chapter_range(plan, k)[0],
                        service.chapter_range(plan, k)[1] + 1,
                    )
                ],
            }
            for k in (1, 2, 3)
        ]
        await service.submit_doc(
            session,
            slug,
            SeriesDocSubmitIn(kind="outline", body_md="# 總綱", body_json={"chapters": chapters}),
        )
        active = await service.decide_doc(
            session, owner, slug, "outline", 0, "approve", None, expected_version=1
        )
        assert active.status == "active" and len(active.episodes) == 25
        assert active.episodes[24].title == "第 25 集" and active.episodes[0].status == "planned"

        job = (await service.next_job(session, settings)).job
        assert job is not None and (job.kind, job.chapter_number) == ("chapter", 1)
        assert job.context.setting is not None and job.context.mysteries == [{"id": "m1"}]
        beats = {
            "hook": "h",
            "conflict": "c",
            "turn": "t",
            "cliffhanger": "x",
            "tension": [2, 3, 3, 4, 5],
        }
        await service.submit_doc(
            session,
            slug,
            SeriesDocSubmitIn(
                kind="chapter",
                chapter_number=1,
                body_md="# 第一篇",
                body_json={
                    "episodes": [{"number": n, "title": f"E{n}", **beats} for n in range(1, 11)]
                },
            ),
        )
        ready = await service.decide_doc(
            session, owner, slug, "chapter", 1, "approve", None, expected_version=1
        )
        assert [e.status for e in ready.episodes[:11]] == ["ready"] * 10 + ["planned"]
        assert ready.episodes[0].title == "E1" and ready.episodes[0].beats["tension"] == [
            2,
            3,
            3,
            4,
            5,
        ]

        job = (await service.next_job(session, settings)).job
        assert (
            job is not None
            and job.kind == "episode"
            and job.episode is not None
            and job.episode.number == 1
        )
        started = await service.start_episode(session, token, slug, 1, f"{slug}-e001")
        assert started.request.status == "started" and started.request.slug == f"{slug}-e001"
        assert started.episode.status == "started" and started.context.chapter is not None
        assert (await service.next_job(session, settings)).job is None, "one at a time"
        await service.recap_episode(
            session, slug, 1, SeriesEpisodeRecapIn(recap="阿下山了", state={"a": "下山"})
        )
        finished = await service.finish_episode(session, slug, 1)
        assert finished.status == "done" and finished.recap == "阿下山了"
        request = await session.scalar(
            select(VideoDramaRequest).where(VideoDramaRequest.slug == f"{slug}-e001")
        )
        assert request is not None and request.status == "done" and request.episode_number == 1

        job = (await service.next_job(session, settings)).job
        assert (
            job is not None
            and job.kind == "episode"
            and job.episode is not None
            and job.episode.number == 2
        )
        assert job.context.recaps == [
            {"number": 1, "title": "E1", "recap": "阿下山了", "state": {"a": "下山"}}
        ]

        view = await service.series_view(session, slug)
        assert (view.episodes_done, view.episodes_ready, view.docs_pending) == (1, 9, 0)
        await session.delete(owner)
        await session.delete(token)
        await session.commit()


@pytest_asyncio.fixture(loop_scope="module")
async def clean_one_off() -> AsyncIterator[list[str]]:
    slugs: list[str] = []
    yield slugs
    async with SessionFactory() as session:
        for slug in slugs:
            found = await session.scalar(
                select(VideoDramaSeries).where(VideoDramaSeries.slug == slug)
            )
            if found is not None:
                await session.execute(
                    delete(VideoDramaRequest).where(VideoDramaRequest.series_id == found.id)
                )
                await session.delete(found)
        await session.commit()
    await engine.dispose()


@integration
@pytest.mark.asyncio(loop_scope="module")
async def test_a_one_off_goes_from_the_request_form_through_its_bible_to_its_episode(
    clean_one_off: list[str],
) -> None:
    async with SessionFactory() as session:
        owner = User(email=f"one-off-{uuid4()}@example.com", password_hash="unused")
        session.add(owner)
        token = VideoToolToken(name="one-off-test", token_hash=uuid4().hex, token_prefix="mkv_o")
        session.add(token)
        await session.commit()
        settings = await settings_service.settings_row(session)
        from app.video_automation import requests as drama_requests

        filed = await service.create_one_off(
            session,
            owner,
            DramaRequestIn(
                premise="精衛填海", title="精衛", style_preset="ink-wash", target_minutes=2
            ),
        )
        assert filed.series_slug is not None and filed.series_slug.startswith("one-off-")
        slug = filed.series_slug
        clean_one_off.append(slug)
        assert filed.status == "queued" and filed.episode_number == 1
        assert await drama_requests.next_request(session) is None or (
            (await drama_requests.next_request(session)).id != filed.id  # type: ignore[union-attr]
        ), "an episode's request starts through the series, not the old queue"

        created = await service.series_view(session, slug)
        assert (created.kind, created.status, created.chapters) == ("one-off", "setting", 1)
        assert (created.planned_episodes, created.episodes_per_chapter) == (1, 1)
        assert [e.status for e in created.episodes] == ["planned"]
        assert created.title == "精衛" and created.style_preset == "ink-wash"

        job = (await service.next_job(session, settings)).job
        assert job is not None and job.kind == "bible" and job.series.slug == slug
        assert job.context.setting is None
        with pytest.raises(service.SeriesRefused, match="one document"):
            await service.submit_doc(
                session,
                slug,
                SeriesDocSubmitIn(kind="setting", body_md="# x", body_json=BIBLE),
            )
        await service.submit_doc(
            session, slug, SeriesDocSubmitIn(kind="bible", body_md="# 故事聖經", body_json=BIBLE)
        )
        assert (await service.next_job(session, settings)).job is None, "the owner is reading it"
        approved = await service.decide_doc(
            session, owner, slug, "bible", 0, "approve", None, expected_version=1
        )
        assert approved.status == "active" and approved.docs[0].kind == "bible"
        episode = approved.episodes[0]
        assert episode.status == "ready" and episode.title == "精衛填海"
        assert episode.logline == "一隻鳥要填平東海" and episode.beats["hook"] == "h"

        job = (await service.next_job(session, settings)).job
        assert job is not None and (job.kind, job.episode.number) == ("episode", 1)  # type: ignore[union-attr]
        assert job.context.setting is not None and job.context.setting.kind == "bible"
        assert job.context.chapter is None and job.context.chapter_range == (1, 1)
        started = await service.start_episode(session, token, slug, 1, f"{slug}-e001")
        assert started.request.id == filed.id, "the request filed with the form travels on"
        assert started.request.status == "started" and started.request.series_slug == slug
        assert started.episode.status == "started"
        assert (
            started.context.setting is not None
            and "characters" in started.context.setting.body_json
        )
        assert (await service.next_job(session, settings)).job is None
        finished = await service.finish_episode(session, slug, 1)
        assert finished.status == "done"
        assert (await service.series_view(session, slug)).status == "finished"
        request = await session.get(VideoDramaRequest, filed.id)
        assert request is not None and request.status == "done"
        with pytest.raises(service.SeriesRefused, match="集數不能改"):
            await service.patch_series(session, owner, slug, SeriesPatch(planned_episodes=3))
        await session.delete(owner)
        await session.delete(token)
        await session.commit()


@integration
@pytest.mark.asyncio(loop_scope="module")
async def test_a_drama_is_withdrawn_before_its_episode_starts_and_not_after(
    clean_one_off: list[str],
) -> None:
    async with SessionFactory() as session:
        owner = User(email=f"withdraw-{uuid4()}@example.com", password_hash="unused")
        session.add(owner)
        token = VideoToolToken(name="withdraw-test", token_hash=uuid4().hex, token_prefix="mkv_w")
        session.add(token)
        await session.commit()
        form = DramaRequestIn(premise="精衛填海", style_preset="ink-wash", target_minutes=2)

        # Still at its story bible: the series goes, the request stays as a cancelled row.
        waiting = await service.create_one_off(session, owner, form)
        assert waiting.series_slug is not None
        clean_one_off.append(waiting.series_slug)
        out = await service.withdraw_series(session, owner, waiting.series_slug)
        assert (out.slug, out.requests_cancelled) == (waiting.series_slug, 1)
        with pytest.raises(service.SeriesRefused, match="找不到"):
            await service.series_view(session, waiting.series_slug)
        request = await session.get(VideoDramaRequest, waiting.id)
        assert request is not None
        await session.refresh(request)
        assert request.status == "cancelled" and request.cancelled_at is not None
        assert request.series_id is None
        await session.delete(request)

        # Approved and started: refused, nothing changes.
        begun = await service.create_one_off(session, owner, form)
        assert begun.series_slug is not None
        slug = begun.series_slug
        clean_one_off.append(slug)
        await service.submit_doc(
            session, slug, SeriesDocSubmitIn(kind="bible", body_md="# 故事聖經", body_json=BIBLE)
        )
        await service.decide_doc(
            session, owner, slug, "bible", 0, "approve", None, expected_version=1
        )
        await service.start_episode(session, token, slug, 1, f"{slug}-e001")
        with pytest.raises(service.SeriesRefused, match="已經開始做了") as refused:
            await service.withdraw_series(session, owner, slug)
        assert refused.value.code == "video_series_started"
        await session.rollback()
        assert (await service.series_view(session, slug)).episodes[0].status == "started"
        await session.delete(owner)
        await session.delete(token)
        await session.commit()
