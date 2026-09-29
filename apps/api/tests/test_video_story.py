"""A brand-story series (docs/videos/STORY.md): the kind, the daily quota, what the worker is
handed, the backlog import, and the month's drafts.

The rules that decide are pure and tested without a database. The import, the upload buffer
and the worker's next job run on an in-memory SQLite database built from the models, so they run
on every machine; the migration's own test (test_migration_0111_video_story_series.py) needs
PostgreSQL. The stories here are invented for the test: the real backlog is checked by
tools/video/story-plans/validate.mjs.
"""

from __future__ import annotations

import codecs
import copy
import io
import json
import sys
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy import event, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app import cli
from app.auth.service import current_user
from app.config import Settings
from app.db import Base, get_session
from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api, ai, stories
from app.video_automation import series as service
from app.video_automation import settings as settings_service
from app.video_automation.models import (
    DEFAULT_STAGE_MODELS,
    VideoAiRun,
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaMessage,
    VideoDramaRequest,
    VideoDramaSeries,
)
from app.video_automation.schemas import (
    SeriesDocSubmitIn,
    SeriesIn,
    SeriesPatch,
    StageRunIn,
)
from app.video_automation.story_cli import import_story_file
from app.video_automation.usage import usage_view
from app.video_media.models import VideoMediaJob

WHEN = datetime(2026, 10, 1, 4, 0, tzinfo=UTC)
LOOK = {
    "style": "flat 2D cartoon illustration, warm muted colours",
    "negative": "text, letters, logo, watermark, real person likeness",
    "motion": "slow steady camera move",
}
POINT = "An invented beat of the story, long enough for the checker's sixty characters."
PREFIX = {
    "A": ("everyday", "global"),
    "B": ("asia-brand", "jp"),
    "K": ("asia-brand", "kr"),
    "T": ("asia-brand", "tw"),
    "C": ("tech", "global"),
}


def _story(number: int, story_id: str, slug: str, **changes: Any) -> dict[str, Any]:
    """One invented story as the compiled file carries it, sound by every rule."""
    category, region = PREFIX[story_id[0]]
    story: dict[str, Any] = {
        "number": number,
        "id": story_id,
        "slug": slug,
        "category": category,
        "region": region,
        "subject": f"Invented object {story_id}",
        "title": f"Why the invented {story_id} took forty years",
        "logline": f"An invented object ({story_id}) waited decades for the world it needed.",
        "question": "Why did an old idea wait so long to sell?",
        "chapters": [{"key": key, "point": f"{key}: {POINT}"} for key in stories.CHAPTER_KEYS],
        "takeaway": "A good idea often waits for the world to need it.",
        "must_verify": [
            {"claim": "The first patent was filed in 1970.", "sources": [0], "core": True},
            {"claim": "A department store refused it at first.", "sources": [1, 2]},
            {"claim": "The founder says men carried the bags.", "sources": [2], "attributed": True},
            {"claim": "The four-wheel model came in 2004.", "sources": [0], "reviewer_only": True},
        ],
        "sources": [
            {
                "url": f"https://patents.example.org/{story_id}",
                "publisher": "Example Patent Office",
                "kind": "official",
                "supports": "the patent and its dates",
                "checked": "2026-09-28",
            },
            {
                "url": f"https://news.example.com/{story_id}",
                "publisher": "Example News",
                "kind": "news",
                "supports": "the refusal",
                "checked": "2026-09-28",
            },
            {
                "url": f"https://www.example.net/{story_id}",
                "publisher": "Example Magazine",
                "kind": "news",
                "supports": "the founder's account",
                "checked": "2026-09-28",
            },
        ],
        "names": ["Examplo"],
        "cast": [
            {
                "id": "founder",
                "role": "the founder",
                "appearance": "a man in his forties in a grey 1970s suit",
            }
        ],
        "image_notes": "Luggage, airports and shop floors; never a logo or a real face.",
        "sensitivity": "none",
        "related_guide": None,
        "thumbnail": {"headline": "等了四十年", "idea": "a suitcase on wheels beside a rocket"},
        "caveats": "",
        "publish": {"day": (number + 1) // 2, "slot": "12:00" if number % 2 else "20:00"},
    }
    story.update(changes)
    return story


SERIES_FILE: dict[str, Any] = {
    "slug": "stories-test",
    "title": "品牌故事（測試）",
    "kind": "story",
    "premise": "每一集講一個虛構的品牌怎麼來的，只為了測試。",
    "note": "測試用的企劃清單",
    "target_minutes": 13,
    "planned_episodes": 3,
    "episodes_per_day": 2,
    "hands_off": True,
    "compilation": False,
    "visual_tier": "stills",
    "style_preset": "custom",
    "image_model": "gemini-3.1-flash-image",
    "youtube_category_id": "27",
    "look": LOOK,
}
THREE = [
    _story(1, "A01", "story-rolling-case"),
    _story(2, "B01", "story-conveyor-sushi"),
    _story(3, "C01", "story-first-mouse"),
]


def _file(items: list[dict[str, Any]] | None = None, **series: Any) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "series": {**copy.deepcopy(SERIES_FILE), **series},
        "stories": copy.deepcopy(items if items is not None else THREE),
    }


def _settings(**changes: Any) -> VideoAutomationSettings:
    values: dict[str, Any] = {
        "series_max_in_flight": 2,
        "series_script_gate": True,
        "series_auto_continue": True,
        "series_chapter_ahead": 2,
        "series_doc_rewrites": 2,
        "series_episodes_per_month": 30,
    }
    values.update(changes)
    return VideoAutomationSettings(**values)


def _series(**changes: Any) -> VideoDramaSeries:
    values: dict[str, Any] = {
        "id": uuid4(),
        "slug": "stories-test",
        "kind": "story",
        "title": "品牌故事（測試）",
        "premise": "p",
        "aspects": [],
        "tone": "dual-male-leads-subtext",
        "style_preset": "custom",
        "target_minutes": 13,
        "planned_episodes": 100,
        "episodes_per_chapter": 10,
        "open_ended": True,
        "status": "active",
        "note": None,
        "requested_chapter": None,
        "force_next": False,
        "hands_off": True,
        "compilation": False,
        "visual_tier": "stills",
        "episodes_per_day": None,
        "image_model": "gemini-3.1-flash-image",
        "look": dict(LOOK),
        "created_at": WHEN,
        "updated_at": WHEN,
    }
    values.update(changes)
    return VideoDramaSeries(**values)


def _episode(
    number: int, status: str = "ready", started_at: datetime | None = None
) -> VideoDramaEpisode:
    return VideoDramaEpisode(
        id=uuid4(),
        series_id=uuid4(),
        number=number,
        chapter_number=1,
        title=f"故事 {number}",
        logline="",
        beats={"id": f"A{number:02d}"},
        status=status,
        state_json={},
        started_at=started_at,
        created_at=WHEN,
        updated_at=WHEN,
    )


def _next(
    series: VideoDramaSeries,
    episodes: list[VideoDramaEpisode],
    settings: VideoAutomationSettings | None = None,
    *,
    now: datetime = WHEN,
    started_this_month: int = 0,
    awaiting_upload: int = 0,
) -> service.NextJob | None:
    return service.next_job_for(
        series,
        [],
        episodes,
        settings or _settings(),
        started_this_month=started_this_month,
        now=now,
        awaiting_upload=awaiting_upload,
    )


def _quota(
    series: VideoDramaSeries,
    episodes: list[VideoDramaEpisode],
    settings: VideoAutomationSettings | None = None,
    *,
    now: datetime = WHEN,
    started_this_month: int = 0,
    awaiting_upload: int = 0,
) -> Any:
    return service.story_quota(
        series,
        episodes,
        settings or _settings(),
        now=now,
        started_this_month=started_this_month,
        awaiting_upload=awaiting_upload,
    )


# --- the kind and its limits --------------------------------------------------------------------


def test_a_story_series_is_hands_off_stills_never_compiled_and_may_run_longer() -> None:
    fields = {k: v for k, v in SERIES_FILE.items() if k in SeriesIn.model_fields}
    story = SeriesIn.model_validate(fields)
    assert (story.kind, story.target_minutes, story.episodes_per_day) == ("story", 13, 2)
    assert story.look is not None and story.look.motion == "slow steady camera move"
    for wrong in ({"hands_off": False}, {"visual_tier": "clips"}, {"compilation": True}):
        with pytest.raises(ValidationError, match="hands_off"):
            SeriesIn.model_validate({**fields, **wrong})
    with pytest.raises(ValidationError, match="look"):
        SeriesIn.model_validate({**fields, "look": None})
    with pytest.raises(ValidationError, match="image model"):
        SeriesIn.model_validate({**fields, "image_model": "gemini-9-imaginary"})
    with pytest.raises(ValidationError):
        SeriesIn.model_validate({**fields, "target_minutes": 21})
    with pytest.raises(ValidationError):
        SeriesIn.model_validate({**fields, "look": {**LOOK, "style": "x" * 601}})

    # The other kinds keep their 8 minutes, and have neither a daily count nor a look.
    classic = {"slug": "xianxia", "title": "問劍", "premise": "兩個少年"}
    assert SeriesIn.model_validate({**classic, "target_minutes": 8}).target_minutes == 8
    for kind in ("series", "one-off"):
        with pytest.raises(ValidationError, match="at most 8 minutes"):
            SeriesIn.model_validate({**classic, "kind": kind, "target_minutes": 9})
        with pytest.raises(ValidationError, match="only a story series"):
            SeriesIn.model_validate({**classic, "kind": kind, "episodes_per_day": 2})
        with pytest.raises(ValidationError, match="only a story series"):
            SeriesIn.model_validate({**classic, "kind": kind, "look": LOOK})
    assert SeriesIn.model_validate({**classic, "image_model": "image-01"}).image_model == (
        "image-01"
    )

    assert SeriesPatch(target_minutes=20).target_minutes == 20
    with pytest.raises(ValidationError):
        SeriesPatch(target_minutes=21)
    with pytest.raises(ValidationError):
        SeriesPatch(episodes_per_day=13)
    classic_row = _series(kind="series", hands_off=False, visual_tier="clips", look=None)
    too_long = service.patch_problem(classic_row, {"target_minutes": 9})
    assert too_long is not None and too_long.code == "video_series_too_long"
    story_only = service.patch_problem(classic_row, {"episodes_per_day": 1})
    assert story_only is not None and story_only.code == "video_series_story_only"
    assert service.patch_problem(classic_row, {"target_minutes": 8, "image_model": "x"}) is None
    story_row = _series()
    assert service.patch_problem(story_row, {"target_minutes": 20, "episodes_per_day": 1}) is None
    for fixed in ({"hands_off": False}, {"visual_tier": "hybrid"}, {"compilation": True}):
        refused = service.patch_problem(story_row, fixed)
        assert refused is not None and refused.code == "video_series_story_fixed"
    lookless = service.patch_problem(story_row, {"look": None})
    assert lookless is not None and lookless.code == "video_series_story_look"


def test_a_story_series_takes_no_documents() -> None:
    for kind in ("setting", "outline", "chapter", "bible"):
        doc = SeriesDocSubmitIn(kind=kind, chapter_number=1, body_md="# x", body_json={})
        assert "backlog import" in str(service.doc_problem(_series(), doc))


def test_the_next_story_starts_without_documents_or_waiting_for_the_one_before() -> None:
    series = _series()
    episodes = [_episode(1, "started", WHEN - timedelta(days=1)), _episode(2), _episode(3)]
    job = _next(series, episodes)
    assert job is not None and (job.kind, job.episode_number) == ("episode", 2)
    # The lowest ready number goes first, whatever came of the others.
    skipped = [_episode(1, "skipped"), _episode(2, "done"), _episode(4), _episode(3)]
    job = _next(series, skipped)
    assert job is not None and job.episode_number == 3
    summary = service.summary_view(series, [], episodes)
    assert (summary.kind, summary.chapters, summary.image_model) == (
        "story",
        1,
        "gemini-3.1-flash-image",
    )
    assert summary.look == LOOK and summary.target_minutes == 13 and summary.quota is None


def test_the_days_count_turns_over_at_midnight_in_taipei() -> None:
    """15:59:59Z is still that day in Taipei; 16:00:00Z is the next one."""
    late = datetime(2026, 10, 1, 15, 59, 59, tzinfo=UTC)
    midnight = datetime(2026, 10, 1, 16, 0, 0, tzinfo=UTC)
    assert service.taipei_day(late).isoformat() == "2026-10-01"
    assert service.taipei_day(midnight).isoformat() == "2026-10-02"
    assert service.taipei_day(late.replace(tzinfo=None)).isoformat() == "2026-10-01"

    series = _series(episodes_per_day=1)
    started_late = [_episode(1, "done", late), _episode(2)]
    assert _next(series, started_late, now=late) is None
    quota = _quota(series, started_late, now=late)
    assert (quota.hold, quota.started_today, quota.day.isoformat()) == ("per_day", 1, "2026-10-01")
    assert "每日上限 1 支" in quota.hold_detail
    job = _next(series, started_late, now=midnight)
    assert job is not None and job.episode_number == 2, "a new day in Taipei"
    assert _quota(series, started_late, now=midnight).started_today == 0

    started_at_midnight = [_episode(1, "done", midnight), _episode(2)]
    next_evening = datetime(2026, 10, 2, 15, 59, 59, tzinfo=UTC)
    assert _next(series, started_at_midnight, now=next_evening) is None, "the same Taipei day"
    assert _next(series, started_at_midnight, now=next_evening + timedelta(seconds=1)) is not None
    assert _next(_series(episodes_per_day=2), started_late, now=late) is not None
    assert _next(_series(episodes_per_day=None), started_late, now=late) is not None


def test_the_other_limits_hold_a_story_and_say_why() -> None:
    series = _series()
    ready = [_episode(1), _episode(2)]
    in_flight = [_episode(1, "started", WHEN - timedelta(days=2)), _episode(2)]
    assert _next(series, in_flight, _settings(series_max_in_flight=1)) is None
    assert _quota(series, in_flight, _settings(series_max_in_flight=1)).hold == "in_flight"

    assert _next(series, ready, started_this_month=30) is None
    assert _quota(series, ready, started_this_month=30).hold == "per_month"

    assert service.STORY_UPLOAD_BUFFER == 6
    assert _next(series, ready, awaiting_upload=6) is None
    buffered = _quota(series, ready, awaiting_upload=6)
    assert (buffered.hold, buffered.awaiting_upload, buffered.upload_buffer) == (
        "upload_buffer",
        6,
        6,
    )
    assert "YouTube" in buffered.hold_detail
    job = _next(series, ready, awaiting_upload=5)
    assert job is not None and job.episode_number == 1

    assert _next(series, [_episode(1, "done")]) is None
    assert _quota(series, [_episode(1, "done")]).hold == "none_ready"
    assert _next(_series(status="paused"), ready) is None
    assert _quota(_series(status="paused"), ready).hold == "not_active"
    clear = _quota(series, ready)
    assert (clear.hold, clear.hold_detail, clear.ready, clear.max_in_flight) == (None, None, 2, 2)


def test_series_of_the_other_kinds_behave_exactly_as_before() -> None:
    """The story rules never reach a long series or a one-off: the same rows give the same job
    with or without the new arguments, however many stories wait for upload."""
    now = datetime(2026, 10, 1, 15, 0, tzinfo=UTC)
    classic = _series(kind="series", hands_off=False, visual_tier="clips", look=None)
    classic.image_model = None
    docs = [
        VideoDramaDoc(
            id=uuid4(),
            kind=kind,
            chapter_number=chapter,
            version=1,
            body_md="#",
            body_json={},
            status="approved",
            created_at=WHEN,
        )
        for kind, chapter in (("setting", 0), ("outline", 0), ("chapter", 1))
    ]
    cases = [
        [_episode(1, "done", now), _episode(2), _episode(3)],
        [_episode(1, "started", now), _episode(2), _episode(3)],
        [_episode(1, "ready"), _episode(2), _episode(3)],
    ]
    for episodes in cases:
        before = service.next_job_for(classic, docs, episodes, _settings(), started_this_month=0)
        after = service.next_job_for(
            classic, docs, episodes, _settings(), started_this_month=0, now=now, awaiting_upload=99
        )
        assert before == after
    job = service.next_job_for(classic, docs, cases[0], _settings(), started_this_month=0)
    assert job is not None and job.episode_number == 2
    assert (
        service.next_job_for(classic, docs, cases[1], _settings(), started_this_month=0) is None
    ), "a long series still waits for the episode before"
    one_off = _series(kind="one-off", slug="one-off-1a2b3c4d", planned_episodes=1, status="setting")
    job = service.next_job_for(
        one_off, [], [_episode(1, "planned")], _settings(), started_this_month=0
    )
    assert job is not None and job.kind == "bible"
    summary = service.summary_view(classic, docs, cases[0])
    assert (summary.chapters, summary.episodes_per_day, summary.look, summary.quota) == (
        10,
        None,
        None,
        None,
    )


# --- the backlog's rules --------------------------------------------------------------------------


def test_a_sound_story_passes_and_each_rule_names_what_is_wrong() -> None:
    story = _story(1, "A01", "story-rolling-case")
    assert stories.story_problems(story) == []
    assert stories.story_problems({k: v for k, v in story.items() if k != "caveats"}) == []

    def problems(**changes: Any) -> str:
        return "\n".join(stories.story_problems({**copy.deepcopy(story), **changes}))

    assert 'unknown field "extra"' in problems(extra=1)
    assert "is not a letter A, B, K, T or C" in problems(id="Z01")
    assert "must be story-" in problems(slug="rolling-case")
    assert "must be story-" in problems(slug="story-" + "x" * 55)
    assert 'category "tech" does not fit id A01' in problems(category="tech")
    assert 'region "kr" does not fit id B01' in "\n".join(
        stories.story_problems(_story(1, "B01", "story-b", region="kr"))
    )
    assert "title is missing" in problems(title="  ")
    assert "title has leading or trailing space" in problems(title=" x")
    assert "title is 61 characters, at most 60" in problems(title="x" * 61)
    assert "angle bracket" in problems(title="a <b>")
    assert "question is missing" in problems(question=None)
    swapped = copy.deepcopy(story["chapters"])
    swapped[0], swapped[1] = swapped[1], swapped[0]
    assert 'chapters[0].key is "origin", expected "hook"' in problems(chapters=swapped)
    assert "chapters must be the 6 parts" in problems(chapters=story["chapters"][:5])
    short = copy.deepcopy(story["chapters"])
    short[2]["point"] = "too short"
    assert "chapters[2] (idea) is 9 characters, expected 60-400" in problems(chapters=short)
    assert "sources has 2 entries, at least 3" in problems(sources=story["sources"][:2])
    plain = copy.deepcopy(story["sources"])
    plain[1]["url"] = "http://news.example.com/A01"
    assert "sources[1].url must be an https URL" in problems(sources=plain)
    plain[1]["url"] = plain[0]["url"]
    assert "sources[1].url repeats an earlier source" in problems(sources=plain)
    facts = copy.deepcopy(story["must_verify"])
    facts[1]["sources"] = [7]
    assert "must_verify[1].sources must list indexes into sources" in problems(must_verify=facts)
    facts = copy.deepcopy(story["must_verify"])
    facts[0]["note"] = "x"
    facts[3]["reviewer_only"] = "yes"
    found = problems(must_verify=facts)
    assert 'must_verify[0] has unknown field "note"' in found
    assert "must_verify[3].reviewer_only must be true or false" in found
    facts = copy.deepcopy(story["must_verify"])
    facts[1]["sources"] = [1]
    assert "must_verify[1] rests on one secondary source" in problems(must_verify=facts)
    facts = [{**fact, "core": False} for fact in story["must_verify"]]
    assert "no must_verify claim is marked core" in problems(must_verify=facts)
    assert "must_verify has 3 claims, expected 4-10" in problems(
        must_verify=story["must_verify"][:3]
    )
    figure = {**story["cast"][0], "appearance": "the Examplo founder"}
    assert 'appearance names "Examplo"' in problems(cast=[figure])
    figure = {**story["cast"][0], "appearance": "一位創辦人"}
    assert "appearance must be English" in problems(cast=[figure])
    assert "cast has 4 figures, at most 3" in problems(cast=[story["cast"][0]] * 4)
    assert "related_guide must be" in problems(related_guide="Not A Slug")
    missing_guide = {k: v for k, v in story.items() if k != "related_guide"}
    assert "related_guide must be" in "\n".join(stories.story_problems(missing_guide))
    assert "thumbnail.headline is 13 characters" in problems(
        thumbnail={"headline": "一" * 13, "idea": "x"}
    )
    assert "publish must be" in problems(publish={"day": 1, "slot": "09:00"})
    assert "publish must be" in problems(publish={"day": 0, "slot": "12:00"})
    assert "number must be a whole number" in problems(number=True)
    assert "caveats must be text of at most 800 characters" in problems(caveats="x" * 801)
    assert stories.story_problems({**story, "caveats": "不要講沒有出處的軼事。"}) == []


def test_two_editions_of_one_encyclopedia_do_not_corroborate_each_other() -> None:
    sources = [
        {"url": "https://en.wikipedia.org/wiki/A", "publisher": "Wikipedia", "kind": "reference"},
        {
            "url": "https://ja.wikipedia.org/wiki/A",
            "publisher": "ウィキペディア",
            "kind": "reference",
        },
        {"url": "https://www.example.com/a", "publisher": "Example", "kind": "news"},
    ]
    assert stories.host_of("https://www.EXAMPLE.com/x") == "example.com"
    assert not stories.claim_supported({"claim": "c", "sources": [0, 1]}, sources)
    assert stories.claim_supported({"claim": "c", "sources": [0, 2]}, sources)
    assert stories.claim_supported({"claim": "c", "sources": [0], "attributed": True}, sources)


def test_the_file_is_checked_as_a_whole() -> None:
    check = stories.check_story_file(_file(), "stories-test")
    assert check.problems == [] and [story["id"] for story in check.stories] == [
        "A01",
        "B01",
        "C01",
    ]
    assert check.series["youtube_category_id"] == "27"

    def problems(document: Any, slug: str = "stories-test") -> str:
        return "\n".join(stories.check_story_file(document, slug).problems)

    assert "schema_version is 2" in problems({**_file(), "schema_version": 2})
    assert "but --series is 'other'" in problems(_file(), "other")
    assert 'series.kind must be "story"' in problems(_file(kind="series"))
    assert "series.target_minutes must be 12 to 15" in problems(_file(target_minutes=16))
    assert "series.episodes_per_day must be 1 to 12" in problems(_file(episodes_per_day=0))
    assert "series.look needs a style" in problems(_file(look={"style": "x"}))
    assert "series.compilation must be false" in problems(_file(compilation=True))
    assert "stories must list at least one story" in problems(_file([]))
    twice = [THREE[0], {**THREE[1], "id": "A01"}, THREE[2]]
    check = stories.check_story_file(_file(twice), "stories-test")
    assert 'A01: id "A01" is also A01\'s' in check.problems and "A01" in check.refused
    gap = [THREE[0], THREE[1], {**THREE[2], "number": 4}]
    assert "numbered 1 to 3, each once, without a gap" in problems(_file(gap))
    same_slot = [THREE[0], {**THREE[1], "publish": dict(THREE[0]["publish"])}, THREE[2]]
    assert "B01: publish day 1 12:00 is also A01's" in problems(_file(same_slot))
    bad = [THREE[0], {**THREE[1], "sources": []}, THREE[2]]
    check = stories.check_story_file(_file(bad), "stories-test")
    assert check.refused == ["B01"] and "B01: sources has 0 entries, at least 3" in check.problems
    unordered = [THREE[2], THREE[0], THREE[1]]
    ordered = stories.check_story_file(_file(unordered), "stories-test").stories
    assert [story["number"] for story in ordered] == [1, 2, 3]


# --- the import, on a database -------------------------------------------------------------------

TABLES = (
    User,
    AdminAuditLog,
    VideoToolToken,
    VideoProject,
    VideoReview,
    VideoMediaJob,
    VideoAiRun,
    VideoAutomationSettings,
    VideoDramaSeries,
    VideoDramaDoc,
    VideoDramaMessage,
    VideoDramaRequest,
    VideoDramaEpisode,
)


@pytest.fixture
async def db() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine("sqlite+aiosqlite://")

    # SQLite drops timezone offsets; PostgreSQL hands back aware datetimes.
    def restore_utc(target: Any, *_context: Any) -> None:
        for column in target.__table__.columns:
            value = getattr(target, column.name)
            if isinstance(value, datetime) and value.tzinfo is None:
                setattr(target, column.name, value.replace(tzinfo=UTC))

    for model in TABLES:
        event.listen(model, "load", restore_utc)
        event.listen(model, "refresh", restore_utc)
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync: Base.metadata.create_all(
                sync, tables=[model.__table__ for model in TABLES]
            )
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        settings = await settings_service.settings_row(session)
        settings.drama_enabled = True
        settings.series_max_in_flight = 2
        await session.commit()
    try:
        yield factory
    finally:
        for model in TABLES:
            event.remove(model, "load", restore_utc)
            event.remove(model, "refresh", restore_utc)
        await engine.dispose()


async def _import(
    factory: async_sessionmaker[AsyncSession], document: Any, **options: Any
) -> stories.StoryImportReport:
    async with factory() as session:
        return await stories.import_story_rows(
            session, document, series_slug="stories-test", **options
        )


async def _rows(factory: async_sessionmaker[AsyncSession]) -> list[VideoDramaEpisode]:
    async with factory() as session:
        found = await session.scalars(select(VideoDramaEpisode).order_by(VideoDramaEpisode.number))
        return list(found.all())


async def _count(factory: async_sessionmaker[AsyncSession], model: Any) -> int:
    async with factory() as session:
        return int(await session.scalar(select(func.count()).select_from(model)) or 0)


async def test_the_import_creates_the_series_and_its_stories_and_changes_nothing_twice(
    db: async_sessionmaker[AsyncSession],
) -> None:
    dry = await _import(db, _file())
    assert (dry.written, dry.series_created, dry.series_exists) == (False, True, False)
    assert dry.as_dict()["create"] == 3 and dry.as_dict()["refuse"] == 0
    assert "series.youtube_category_id is not kept by the server" in dry.notes
    assert await _count(db, VideoDramaSeries) == 0, "a dry run writes nothing"

    # The pilot: two stories, one a day.
    pilot = await _import(db, _file(), apply=True, limit=2, episodes_per_day=1)
    assert pilot.written and pilot.create == ["A01", "B01"] and pilot.stories == 3
    async with db() as session:
        series = await session.scalar(select(VideoDramaSeries))
        assert series is not None
        assert (series.kind, series.status, series.hands_off, series.visual_tier) == (
            "story",
            "active",
            True,
            "stills",
        )
        assert (series.target_minutes, series.episodes_per_day, series.image_model) == (
            13,
            1,
            "gemini-3.1-flash-image",
        )
        assert series.look == LOOK and series.compilation is False
    rows = await _rows(db)
    assert [(row.number, row.chapter_number, row.status, row.slug) for row in rows] == [
        (1, 1, "ready", "story-rolling-case"),
        (2, 1, "ready", "story-conveyor-sushi"),
    ]
    first = rows[0]
    assert first.title == THREE[0]["title"] and first.logline == THREE[0]["logline"]
    assert set(first.beats) == {
        "id",
        "category",
        "region",
        "subject",
        "question",
        "chapters",
        "takeaway",
        "must_verify",
        "sources",
        "names",
        "cast",
        "image_notes",
        "sensitivity",
        "related_guide",
        "thumbnail",
        "caveats",
        "publish",
    }
    assert first.beats["must_verify"][3]["reviewer_only"] is True
    audits = await _count(db, AdminAuditLog)

    again = await _import(db, _file(), apply=True, limit=2, episodes_per_day=1)
    assert (again.written, again.create, again.update, again.unchanged) == (
        False,
        [],
        [],
        ["A01", "B01"],
    )
    assert again.as_dict()["leave_alone"] == 2
    assert [(row.number, row.updated_at, row.beats) for row in await _rows(db)] == [
        (row.number, row.updated_at, row.beats) for row in rows
    ]
    assert await _count(db, AdminAuditLog) == audits, "the second run changes nothing"
    # The series row stays as the owner has it; the file's other values are only reported.
    assert again.series_differs == {"episodes_per_day": {"file": 2, "series": 1}}
    assert any("--episodes-per-day applies only" in note for note in again.notes)

    rest = await _import(db, _file(), apply=True)
    assert (rest.create, rest.unchanged, rest.written) == (["C01"], ["A01", "B01"], True)
    assert [row.number for row in await _rows(db)] == [1, 2, 3]
    last = await _import(db, _file(), apply=True)
    assert (last.written, last.create, last.update) == (False, [], [])
    assert await _count(db, VideoDramaSeries) == 1


async def test_a_bad_story_refuses_the_whole_file_and_nothing_is_written(
    db: async_sessionmaker[AsyncSession],
) -> None:
    bad = [THREE[0], {**THREE[1], "sources": THREE[1]["sources"][:2]}, THREE[2]]
    report = await _import(db, _file(bad), apply=True)
    assert not report.written and report.refused == ["B01"]
    assert report.as_dict()["refuse"] == 1 and report.as_dict()["create"] == 0
    assert "B01: sources has 2 entries, at least 3" in report.problems
    assert await _count(db, VideoDramaSeries) == 0 and await _count(db, VideoDramaEpisode) == 0

    unknown = await _import(db, _file([{**THREE[0], "rating": 5}]), apply=True)
    assert 'A01: unknown field "rating"' in unknown.problems and not unknown.written
    bad_model = await _import(db, _file(image_model="gemini-9-imaginary"), apply=True)
    assert any("image model" in problem for problem in bad_model.problems)
    assert await _count(db, VideoDramaSeries) == 0
    for limit, per_day in ((0, None), (None, 13)):
        refused = await _import(db, _file(), apply=True, limit=limit, episodes_per_day=per_day)
        assert refused.problems and not refused.written


async def test_a_story_is_updated_until_it_starts_and_left_alone_after(
    db: async_sessionmaker[AsyncSession],
) -> None:
    await _import(db, _file(), apply=True)
    async with db() as session:
        first = await session.scalar(select(VideoDramaEpisode).where(VideoDramaEpisode.number == 1))
        assert first is not None
        first.status = "started"
        first.started_at = WHEN
        second = await session.scalar(
            select(VideoDramaEpisode).where(VideoDramaEpisode.number == 3)
        )
        assert second is not None
        second.status = "skipped"
        await session.commit()
    changed = [
        {**THREE[0], "title": "A new title for a started story"},
        {**THREE[1], "title": "A new title for a ready story", "caveats": "不要講那個軼事。"},
        {**THREE[2], "title": "A new title for a skipped story"},
    ]
    report = await _import(db, _file(changed), apply=True)
    assert (report.update, report.started, report.written) == (["B01"], ["A01", "C01"], True)
    assert report.as_dict()["leave_alone"] == 2
    rows = await _rows(db)
    assert [row.title for row in rows] == [
        THREE[0]["title"],
        "A new title for a ready story",
        THREE[2]["title"],
    ]
    assert rows[1].beats["caveats"] == "不要講那個軼事。"
    # A planned row is not started either: it becomes ready with the story's content.
    async with db() as session:
        row = await session.scalar(select(VideoDramaEpisode).where(VideoDramaEpisode.number == 2))
        assert row is not None
        row.status = "planned"
        await session.commit()
    report = await _import(db, _file(changed), apply=True)
    assert report.update == ["B01"] and (await _rows(db))[1].status == "ready"


async def test_a_moved_schedule_renumbers_the_rows_that_have_not_started(
    db: async_sessionmaker[AsyncSession],
) -> None:
    await _import(db, _file(), apply=True)
    swapped = [
        THREE[0],
        {**THREE[2], "number": 2, "publish": dict(THREE[1]["publish"])},
        {**THREE[1], "number": 3, "publish": dict(THREE[2]["publish"])},
    ]
    report = await _import(db, _file(swapped), apply=True)
    assert report.written and sorted(report.renumbered) == ["B01", "C01"]
    rows = await _rows(db)
    assert [(row.number, row.beats["id"], row.slug) for row in rows] == [
        (1, "A01", "story-rolling-case"),
        (2, "C01", "story-first-mouse"),
        (3, "B01", "story-conveyor-sushi"),
    ]
    assert rows[1].beats["publish"] == THREE[1]["publish"]

    # A started story keeps its number: a file that puts another story there is refused.
    async with db() as session:
        first = await session.scalar(select(VideoDramaEpisode).where(VideoDramaEpisode.number == 1))
        assert first is not None
        first.status = "started"
        await session.commit()
    moved = [
        {**THREE[2], "number": 1, "publish": dict(THREE[0]["publish"])},
        {**THREE[0], "number": 2, "publish": dict(THREE[1]["publish"])},
        {**THREE[1], "number": 3, "publish": dict(THREE[2]["publish"])},
    ]
    report = await _import(db, _file(moved), apply=True)
    assert not report.written and "C01" in report.refused
    assert any(
        problem.startswith("C01: number 1 is episode 1 (A01), which has started")
        for problem in report.problems
    )
    assert any("A01 is started as episode 1 and keeps that number" in note for note in report.notes)
    assert [row.beats["id"] for row in await _rows(db)] == ["A01", "C01", "B01"], "nothing moved"


async def test_a_slug_another_series_or_video_has_is_a_problem(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        session.add(
            VideoProject(
                slug="story-first-mouse", title="x", stage="done", checklist=[], format="drama"
            )
        )
        await session.commit()
    report = await _import(db, _file(), apply=True)
    assert "C01: slug story-first-mouse is already a video on /admin/videos" in report.problems
    assert not report.written and report.refused == ["C01"]


async def test_the_worker_gets_the_whole_story_and_the_day_holds_the_next(
    db: async_sessionmaker[AsyncSession],
) -> None:
    await _import(db, _file(), apply=True, episodes_per_day=1)
    async with db() as session:
        token = VideoToolToken(name="story-test", token_hash=uuid4().hex, token_prefix="mkv_s")
        session.add(token)
        await session.commit()
        settings = await settings_service.settings_row(session)
        job = (await service.next_job(session, settings)).job
        assert job is not None and job.kind == "episode" and job.episode is not None
        assert job.episode.number == 1 and job.episode.slug == "story-rolling-case"
        assert job.episode.beats["chapters"] == THREE[0]["chapters"]
        assert job.episode.beats["sources"] == THREE[0]["sources"]
        assert job.episode.beats["question"] == THREE[0]["question"]
        assert (job.series.kind, job.series.target_minutes, job.series.image_model) == (
            "story",
            13,
            "gemini-3.1-flash-image",
        )
        assert job.series.look == LOOK and job.series.episodes_per_day == 1
        assert job.context.chapter is None and job.context.chapter_number is None
        assert job.context.episode is not None and job.context.episode.beats == job.episode.beats
        # The other stories are listed by title and state only, not with their whole plans.
        assert [(e.number, e.beats) for e in job.context.episodes] == [(1, {}), (2, {}), (3, {})]

        with pytest.raises(service.SeriesRefused) as renamed:
            await service.start_episode(session, token, "stories-test", 1, "story-other-name")
        assert renamed.value.code == "video_series_story_slug"
        started = await service.start_episode(
            session, token, "stories-test", 1, "story-rolling-case"
        )
        assert started.episode.status == "started" and started.request.target_minutes == 13
        assert "Why did an old idea wait so long to sell?" in started.request.premise
        # One a day: the next waits for tomorrow in Taipei.
        assert (await service.next_job(session, settings)).job is None
        view = await service.series_view(session, "stories-test")
        assert view.quota is not None
        assert (view.quota.hold, view.quota.started_today, view.quota.in_flight) == (
            "per_day",
            1,
            1,
        )
        listed = await service.list_series(session, kind="story")
        assert [item.slug for item in listed] == ["stories-test"]
        assert listed[0].quota is not None and listed[0].quota.hold == "per_day"

        with pytest.raises(service.SeriesRefused, match="backlog import") as doc:
            await service.submit_doc(
                session,
                "stories-test",
                SeriesDocSubmitIn(kind="setting", body_md="# x", body_json={}),
            )
        assert doc.value.code == "video_series_doc_invalid"
        with pytest.raises(service.SeriesRefused) as action:
            await service.act(session, User(id=uuid4()), "stories-test", "start-next")
        assert action.value.code == "video_series_story_no_action"


async def test_six_stories_cleared_for_upload_without_a_youtube_id_hold_the_next(
    db: async_sessionmaker[AsyncSession],
) -> None:
    eight = [_story(number, f"A{number:02d}", f"story-invented-{number}") for number in range(1, 9)]
    await _import(db, _file(eight, planned_episodes=8), apply=True, episodes_per_day=12)
    async with db() as session:
        rows = list(
            await session.scalars(select(VideoDramaEpisode).order_by(VideoDramaEpisode.number))
        )
        projects = []
        for row in rows[:6]:
            # Long ago, so neither the day's count nor the month's is what holds the next one.
            row.status = "done"
            row.started_at = datetime(2026, 1, 5, tzinfo=UTC)
            project = VideoProject(
                slug=row.slug or "", title=row.title, stage="done", checklist=[], format="drama"
            )
            session.add(project)
            projects.append(project)
        await session.flush()
        for project in projects:
            session.add(
                VideoReview(
                    project_id=project.id,
                    gate="publish",
                    content_sha256="0" * 64,
                    summary="上架確認",
                    payload={},
                    files=[],
                    status="approved",
                    decided_at=WHEN,
                )
            )
        await session.commit()
        settings = await settings_service.settings_row(session)
        assert (await service.next_job(session, settings)).job is None
        view = await service.series_view(session, "stories-test")
        assert view.quota is not None
        assert (view.quota.hold, view.quota.awaiting_upload) == ("upload_buffer", 6)

        # The owner uploads one: its YouTube id is recorded, and the next story may start.
        projects[0].youtube_video_id = "dQw4w9WgXcQ"
        await session.commit()
        job = (await service.next_job(session, settings)).job
        assert job is not None and job.episode is not None and job.episode.number == 7
        # A dropped video will never be uploaded, so it does not count either.
        projects[0].youtube_video_id = None
        projects[1].dropped_at = WHEN
        await session.commit()
        assert (await service.next_job(session, settings)).job is not None
        # A confirmation that was sent back is not a clearance.
        projects[1].dropped_at = None
        review = await session.scalar(
            select(VideoReview).where(VideoReview.project_id == projects[2].id)
        )
        assert review is not None
        review.status = "rejected"
        await session.commit()
        assert (await service.next_job(session, settings)).job is not None


# --- the month's drafts --------------------------------------------------------------------------


async def test_a_storys_model_calls_do_not_count_against_the_months_drafts(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Every call a story makes carries a variant (docs/videos/STORY.md §伺服器), so it is not one
    of the ``max_drafts_per_month`` scheduled drafts, even with that cap reached."""

    class Provider:
        model = "claude-sonnet-5"

        async def structured(self, schema: Any, *_: Any) -> tuple[Any, dict[str, int]]:
            return schema(text="{}"), {"input_tokens": 10, "output_tokens": 5}

        async def close(self) -> None:
            return None

    monkeypatch.setattr(ai, "research_provider", lambda *_args, **_kwargs: Provider())
    runtime = Settings(anthropic_api_key="a")
    row = VideoAutomationSettings(
        stage_models={
            stage: {"provider": "anthropic", "model": choice["model"]}
            for stage, choice in DEFAULT_STAGE_MODELS.items()
        },
        monthly_token_budget_millions=20,
        max_drafts_per_month=2,
    )
    async with db() as session:
        for slug in ("tutorial-one", "tutorial-two"):
            session.add(
                VideoAiRun(slug=slug, stage="planner", provider="anthropic", model="m", status="ok")
            )
        await session.commit()
        assert (await usage_view(session, row)).drafts == 2, "the month's cap is reached"
        for stage in ("planner", "writer", "verifier", "listener"):
            request = StageRunIn(
                stage=stage,
                slug="story-rolling-case",
                instructions="Write one chapter.",
                payload={},
                format="drama",
                variant="story",
            )
            out = await ai.run_stage(session, runtime, row, request, None)
            assert out.usage.drafts == 2
        recorded = await session.scalars(
            select(VideoAiRun.stage).where(VideoAiRun.slug == "story-rolling-case")
        )
        assert sorted(recorded.all()) == [
            "listener/story",
            "planner/story",
            "verifier/story",
            "writer/story",
        ]
        assert (await usage_view(session, row)).drafts == 2
        tutorial = StageRunIn(
            stage="planner", slug="tutorial-three", instructions="Plan.", payload={}
        )
        with pytest.raises(ai.StageFailed) as refused:
            await ai.run_stage(session, runtime, row, tutorial, None)
        assert refused.value.code == "video_ai_budget_exhausted", "a scheduled draft still counts"


# --- the routes and the command -------------------------------------------------------------------


def _app(user: User) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.admin_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    app.dependency_overrides[current_user] = lambda: user
    return app


async def test_the_owner_lists_story_series_and_cannot_make_one_that_needs_the_owner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    summary = service.summary_view(_series(), [], [])
    listed = AsyncMock(return_value=[summary])
    monkeypatch.setattr(service, "list_series", listed)
    create = AsyncMock()
    monkeypatch.setattr(service, "create_series", create)
    monkeypatch.setattr(
        settings_service,
        "settings_row",
        AsyncMock(return_value=VideoAutomationSettings(drama_enabled=True)),
    )
    base = "/api/v1/admin/video-automation/series"
    fields = {k: v for k, v in SERIES_FILE.items() if k in SeriesIn.model_fields}
    async with AsyncClient(transport=ASGITransport(app=_app(owner)), base_url="http://t") as client:
        only = await client.get(base, params={"kind": "story"})
        gated = await client.post(base, json={**fields, "hands_off": False})
        clips = await client.post(base, json={**fields, "visual_tier": "clips"})
    assert only.status_code == 200 and listed.await_args.kwargs == {"kind": "story"}
    assert only.json()["series"][0]["look"] == LOOK
    assert gated.status_code == 422 and clips.status_code == 422 and create.await_count == 0


def test_the_command_reads_the_file_from_standard_input_and_fails_on_a_problem(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    document = _file()
    raw = codecs.BOM_UTF8 + json.dumps(document, ensure_ascii=False).encode("utf-8")
    outcome: dict[str, Any] = {"series": "stories-test", "problems": [], "create": 3}
    command = AsyncMock(return_value=outcome)
    monkeypatch.setattr(cli, "import_story_file", command)
    monkeypatch.setattr(sys, "stdin", SimpleNamespace(buffer=io.BytesIO(raw)))
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "app.cli",
            "video-story-import",
            "--series",
            "stories-test",
            "--apply",
            "--limit",
            "2",
            "--episodes-per-day",
            "1",
        ],
    )
    cli.main()
    text = command.await_args.args[0]
    assert json.loads(text) == document, "the byte order mark is dropped"
    assert command.await_args.kwargs == {
        "series": "stories-test",
        "apply": True,
        "limit": 2,
        "episodes_per_day": 1,
    }
    assert json.loads(capsys.readouterr().out)["create"] == 3

    outcome["problems"] = ["B01: sources has 2 entries, at least 3"]
    monkeypatch.setattr(sys, "stdin", SimpleNamespace(buffer=io.BytesIO(raw)))
    with pytest.raises(SystemExit) as failed:
        cli.main()
    assert failed.value.code == 1


async def test_a_file_that_is_not_json_is_refused_before_the_database() -> None:
    report = await import_story_file("{not json", series="stories-test")
    assert report["problems"][0].startswith("the file is not valid JSON")
    assert report["written"] is False and report["create"] == 0


@pytest.mark.parametrize("hold", ["not_active", "per_day", "in_flight", "per_month"])
async def test_story_start_rechecks_hold_after_job_was_advertised(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch, hold: str
) -> None:
    monkeypatch.setattr(service, "_now", lambda: WHEN)
    await _import(db, _file(), apply=True, episodes_per_day=2)
    async with db() as session:
        token = VideoToolToken(name="story-claim", token_hash=uuid4().hex, token_prefix="mkv_s")
        session.add(token)
        await session.commit()
        await service.start_episode(session, token, "stories-test", 1, "story-rolling-case")
        first = await session.scalar(select(VideoDramaEpisode).where(VideoDramaEpisode.number == 1))
        assert first is not None
        first.status = "done"
        await session.commit()
        settings = await settings_service.settings_row(session)
        job = (await service.next_job(session, settings)).job
        assert job is not None and job.episode is not None and job.episode.number == 2
        advertised_slug = job.episode.slug
        assert advertised_slug is not None

    # The GET only advertised a job. The owner can change its conditions before POST start.
    async with db() as session:
        series = await service._series(session, "stories-test", lock=True)
        settings = await settings_service.settings_row(session)
        if hold == "not_active":
            series.status = "paused"
        elif hold == "per_day":
            series.episodes_per_day = 1
        elif hold == "in_flight":
            first = await session.scalar(
                select(VideoDramaEpisode).where(VideoDramaEpisode.number == 1)
            )
            assert first is not None
            first.status = "started"
            settings.series_max_in_flight = 1
        else:
            settings.series_episodes_per_month = 1
        await session.commit()

    async with db() as session:
        view = await service.series_view(session, "stories-test")
        assert view.quota is not None and view.quota.hold == hold
        with pytest.raises(service.SeriesRefused) as refused:
            await service.start_episode(session, token, "stories-test", 2, advertised_slug)
        assert (refused.value.status, refused.value.code) == (409, "video_series_story_held")
        assert await session.scalar(select(func.count()).select_from(VideoDramaRequest)) == 1
        second = await session.scalar(
            select(VideoDramaEpisode).where(VideoDramaEpisode.number == 2)
        )
        assert second is not None and second.status == "ready" and second.request_id is None


async def test_story_start_preserves_allowed_start_and_same_episode_retry_guard(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "_now", lambda: WHEN)
    await _import(db, _file(), apply=True, episodes_per_day=1)
    async with db() as session:
        token = VideoToolToken(name="story-claim", token_hash=uuid4().hex, token_prefix="mkv_s")
        session.add(token)
        await session.commit()
        started = await service.start_episode(
            session, token, "stories-test", 1, "story-rolling-case"
        )
        assert started.episode.status == "started"
        with pytest.raises(service.SeriesRefused) as refused:
            await service.start_episode(session, token, "stories-test", 1, "story-rolling-case")
        assert (refused.value.status, refused.value.code) == (
            409,
            "video_series_episode_not_ready",
        )
        assert await session.scalar(select(func.count()).select_from(VideoDramaRequest)) == 1


@pytest.mark.parametrize("kind", ["series", "one-off"])
async def test_story_start_guard_does_not_change_other_kinds(
    db: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch, kind: str
) -> None:
    series = _series(kind=kind, target_minutes=5, image_model=None, look=None)
    episode = _episode(1)
    episode.series_id = series.id
    token = VideoToolToken(name="non-story", token_hash=uuid4().hex, token_prefix="mkv_s")
    quota = AsyncMock(side_effect=AssertionError("story limits must not affect other kinds"))
    monkeypatch.setattr(service, "_story_quota", quota)
    async with db() as session:
        session.add_all([series, token])
        await session.flush()
        session.add(episode)
        # Ordinary dramas require their own current approvals, independently of story quotas.
        keys = (
            [("bible", 0)]
            if kind == "one-off"
            else [("setting", 0), ("outline", 0), ("chapter", 1)]
        )
        for doc_kind, chapter in keys:
            session.add(
                VideoDramaDoc(
                    series_id=series.id,
                    kind=doc_kind,
                    chapter_number=chapter,
                    version=1,
                    body_md="# Approved",
                    body_json={"approved_fixture": True},
                    status="approved",
                )
            )
        await session.commit()
    async with db() as session:
        started = await service.start_episode(session, token, series.slug, 1, "non-story-episode")
        assert started.episode.status == "started"
        assert started.request.target_minutes == 5
        quota.assert_not_awaited()
