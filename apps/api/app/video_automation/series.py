"""A long drama series: the series, its documents, its episodes, and what the worker does next.

The owner starts a series on /admin/videos (docs/videos/SERIES.md). The worker plans the setting
book, then the whole-series outline, then one chapter's detailed outline at a time; the owner
approves each, or sends it back with a note, and the worker rewrites it. Once a chapter is
approved its episodes are ready, and the worker starts them in order: the next one when the
previous is done (cleared for upload) or skipped, while fewer than ``series_max_in_flight`` are
in the making. Every rule about "what next" is a pure function over the loaded rows
(``next_job_for``), so it can be tested without a database.

A one-off drama is a series of ``kind = "one-off"`` (docs/videos/DRAMA-FLOW.md §二): one
episode, and one document, the story bible, whose approval makes the episode ready; from there
it walks the same road as an episode of a long series. The owner's drama request form makes one
(``create_one_off``), and the request row is the episode's, filed when the bible is approved
and the worker starts it.

A brand-story series is a series of ``kind = "story"`` (docs/videos/STORY.md): active from the
start, no documents at all, its episodes the stories of a planned backlog imported ready
(``app.video_automation.stories``). The next ready story starts without waiting for the one
before, unless a limit holds (``story_quota``): the day's count on the Asia/Taipei calendar
day, the episodes in the making, the month's count, or STORY_UPLOAD_BUFFER stories cleared for
upload that the owner has not uploaded yet. A skipped story that never started can be brought
back (``restore_episode``); a skipped episode of the other kinds cannot.

The router turns ``SeriesRefused`` into the API's problem response; nothing here raises
``AppError``.
"""

from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import UTC, date, datetime
from typing import Any, cast
from uuid import uuid4
from zoneinfo import ZoneInfo

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoToolToken
from app.video_automation.judge import (
    retention_required_for,
    series_doc_note,
    series_doc_passed,
)
from app.video_automation.models import (
    DEFAULT_DRAMA,
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaMessage,
    VideoDramaRequest,
    VideoDramaSeries,
)
from app.video_automation.requests import request_view
from app.video_automation.schemas import (
    ONE_OFF_EPISODES,
    SERIES_MAX_MINUTES,
    BingeQuoteOut,
    BudgetLine,
    DramaRequestIn,
    DramaRequestOut,
    SeriesCompilationStartOut,
    SeriesContextOut,
    SeriesDocEditIn,
    SeriesDocOut,
    SeriesDocSubmitIn,
    SeriesEpisodeEditIn,
    SeriesEpisodeOut,
    SeriesEpisodeRecapIn,
    SeriesEpisodeStartOut,
    SeriesIn,
    SeriesJob,
    SeriesJobOut,
    SeriesOut,
    SeriesPatch,
    SeriesSummary,
    SeriesWithdrawnOut,
    StoryHold,
    StoryQuotaOut,
)
from app.video_media.catalog import JUDGE_USD_PER_CALL, find_model
from app.video_media.meter import spend_by_slug
from app.video_reviews.admin_service import list_projects

# The episode fields a chapter outline must give every episode, in the order the owner reads
# them: the hook, the conflict, the turn, the cliffhanger (docs/videos/SERIES.md).
BEAT_FIELDS = ("hook", "conflict", "turn", "cliffhanger")
RECENT_RECAPS = 3
ACTIVE_STATUSES = ("setting", "outline", "active")
EPISODE_OPEN = ("planned", "ready", "queued", "started")
# The episodes a drama may be withdrawn with: none of them has been handed to the worker.
WITHDRAWABLE = ("planned", "ready")
# The story bible of a one-off (docs/videos/DRAMA-FLOW.md §二): the cast as in a setting book,
# the acts, and the one outline the episode is written from; music, not_doing and lexicon are
# the planner's to fill and nothing here reads them.
BIBLE_LISTS = ("acts",)
ONE_OFF_PREFIX = "one-off-"
# The note on a version the discussion replaced (docs/videos/DRAMA-FLOW.md §三): such a version
# is not one of the owner's rewrites, so it does not count against ``series_doc_rewrites``.
DISCUSSION_NOTE = "討論後出了新版本"
# A brand-story series (docs/videos/STORY.md §每日配額與排程). A story counts against the day it
# started on in Asia/Taipei, where the owner lives and the upload slots are; and no new story
# starts while this many are cleared for upload (their upload confirmation approved) without a
# YouTube id, so a few days without uploads never piles up more finished stories.
TAIPEI = ZoneInfo("Asia/Taipei")
STORY_UPLOAD_BUFFER = 6
# What the request row of a started story says besides its title and logline.
STORY_PREMISE_FIELDS = ("question",)

# A binge series (docs/videos/BINGE.md). The genre presets the planner writes from: the
# classic xianxia series keeps today's prompts and rules; the others carry the retention
# spec, so their chapter outlines must schedule the satisfaction beats a viewer stays for.
# The satisfaction types are the same ids the worker's prompts use.
GENRE_LABELS: dict[str, str] = {
    "xianxia-bonds": "仙俠羈絆",
    "rebirth-revenge": "重生復仇",
    "system-game": "系統遊戲",
    "urban-return": "都市歸來",
    "empress-rise": "女帝崛起",
    "custom": "自訂",
}
COMMON_SATISFACTIONS = (
    "face_slap",
    "identity_reveal",
    "counter_kill",
    "level_up",
    "first_clear",
    "betrayer_punished",
    "villain_humbled",
    "hidden_power",
    "public_vindication",
    "rescue",
    "reversal",
)
GENRE_SATISFACTIONS: dict[str, tuple[str, ...]] = {
    genre: COMMON_SATISFACTIONS for genre in GENRE_LABELS
}
BEATS = ("opening", "first_half", "midpoint", "second_half", "ending")
HOOK_TYPES = ("question", "danger", "image", "line", "reversal")
LEAD_ARCS = ("wins", "suffers", "mixed")
MIN_SATISFACTION = 2
# The series' title until the setting book names it (the form left it blank).
AUTO_TITLE = "（企劃命名中）"
# What the quote assumes per episode (docs/videos/DRAMA.md): thirty shots of six seconds for
# three minutes, half of the shots retaken once, one keyframe take in three redrawn, a judge
# call per keyframe and per clip, the sheets once per series.
SHOTS_PER_MINUTE = 10
SHOT_SECONDS = 6
RETAKE_FACTOR = 1.5
KEYFRAME_TAKES = 1.3
SHEET_IMAGES = 18
TIER_CLIP_SHARE: dict[str, float] = {"clips": 1.0, "hybrid": 0.4, "stills": 0.1}


class SeriesRefused(Exception):
    """Why the change cannot be made; the router turns it into the API's error."""

    def __init__(self, status: int, code: str, detail: str):
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail


def _now() -> datetime:
    return datetime.now(UTC)


# --- pure helpers ---------------------------------------------------------------------------


def chapter_count(planned_episodes: int, episodes_per_chapter: int) -> int:
    return max(1, -(-planned_episodes // episodes_per_chapter))


def is_one_off(series: VideoDramaSeries) -> bool:
    return series.kind == "one-off"


# An illustrated explainer (docs/videos/so-thats-why/) is a one-off in this preset: its bible is a
# question's, with no cast, and its outline carries the answer, the reasons and the sources.
EXPLAINER_PRESET = "flat-explainer"


def is_explainer(series: VideoDramaSeries) -> bool:
    return is_one_off(series) and series.style_preset == EXPLAINER_PRESET


def _explainer_bible_problem(body: dict[str, Any]) -> str | None:
    """The explainer's bible: no cast, the acts, and an outline with the question, the answer,
    the reasons and the https pages the facts rest on (tools/video/automation/series.mjs)."""
    if body.get("characters") != []:
        return "an explainer's bible has no characters"
    for key in BIBLE_LISTS:
        if not isinstance(body.get(key), list) or not body[key]:
            return f"a story bible needs an {key} list"
    outline = body.get("outline")
    if not isinstance(outline, dict):
        return "a story bible needs one outline (an object)"
    for key in ("question", "answer", "hook"):
        if not isinstance(outline.get(key), str) or not outline[key].strip():
            return f"an explainer's outline needs its {key}"
    reasons = outline.get("reasons")
    if not isinstance(reasons, list) or len(reasons) < 2 or not all(
        isinstance(reason, str) and reason.strip() for reason in reasons
    ):
        return "an explainer's outline lists its reasons"
    sources = outline.get("sources")
    if not isinstance(sources, list) or not sources or not all(
        isinstance(url, str) and url.startswith("https://") for url in sources
    ):
        return "an explainer's outline lists the https pages its facts rest on"
    return None


def is_story(series: VideoDramaSeries) -> bool:
    return series.kind == "story"


def setting_kind(series: VideoDramaSeries) -> str:
    """The document that holds a series' cast: the setting book, or a one-off's story bible."""
    return "bible" if is_one_off(series) else "setting"


def chapter_range(series: VideoDramaSeries, chapter: int) -> tuple[int, int]:
    """The first and last episode number of a chapter; the last chapter may be short."""
    size = series.episodes_per_chapter
    first = (chapter - 1) * size + 1
    return first, min(chapter * size, series.planned_episodes)


def chapter_of(series: VideoDramaSeries, number: int) -> int:
    return (number - 1) // series.episodes_per_chapter + 1


def binge_shape(total_minutes: int, episode_minutes: int) -> tuple[int, int]:
    """How many episodes a compilation of ``total_minutes`` takes, and how many per chapter.

    Chapters hold six to ten episodes, whichever leaves the fullest last chapter, the larger
    size when two tie (fewer chapter outlines to plan), so a 120-minute run of 3-minute
    episodes is 40 episodes in four chapters of ten. A run of ten episodes or fewer is one
    chapter: the outline planner accepts four to ten, so the pilot is a normal series.
    """
    planned = max(1, min(500, round(total_minutes / max(1, episode_minutes))))
    if planned <= 10:
        return planned, max(4, min(10, planned))
    best = 10
    for size in range(6, 11):
        remainder = planned % size
        short = 0 if remainder == 0 else size - remainder
        current = planned % best
        current_short = 0 if current == 0 else best - current
        if (short, -size) < (current_short, -best):
            best = size
    return planned, best


def auto_slug(genre: str, now: datetime | None = None) -> str:
    """A slug for a series the form did not name: the genre, the day and four random hexits."""
    when = now or _now()
    return f"{genre[:16]}-{when:%Y%m%d}-{uuid4().hex[:4]}"


def auto_title(genre: str) -> str:
    return f"{GENRE_LABELS.get(genre, genre)}合集 {AUTO_TITLE}"


def retention_required(series: VideoDramaSeries) -> bool:
    return retention_required_for(series.genre)


def _retention_problem(series: VideoDramaSeries, episodes: list[dict[str, Any]]) -> str | None:
    """Why a chapter outline breaks the retention rules (docs/videos/BINGE.md), or None.

    Every episode names its hook type, the lead's arc and at least MIN_SATISFACTION
    satisfaction beats of the genre's types, the first of them inside the first half; two
    episodes in a row never leave the lead only suffering; any four in a row pay something off.
    """
    allowed = set(GENRE_SATISFACTIONS.get(series.genre or "", COMMON_SATISFACTIONS))
    ordered = sorted(
        (e for e in episodes if isinstance(e.get("number"), int)), key=lambda e: e["number"]
    )
    for episode in ordered:
        number = episode["number"]
        if episode.get("hook_type") not in HOOK_TYPES:
            return f"episode {number} needs hook_type: one of {', '.join(HOOK_TYPES)}"
        if episode.get("lead_arc") not in LEAD_ARCS:
            return f"episode {number} needs lead_arc: one of {', '.join(LEAD_ARCS)}"
        beats = episode.get("satisfaction")
        if not isinstance(beats, list) or len(beats) < MIN_SATISFACTION:
            return f"episode {number} needs at least {MIN_SATISFACTION} satisfaction beats"
        for beat in beats:
            if (
                not isinstance(beat, dict)
                or beat.get("beat") not in BEATS
                or beat.get("type") not in allowed
            ):
                return (
                    f"episode {number}: every satisfaction beat is {{beat: one of "
                    f"{', '.join(BEATS)}, type: one of the genre's types}}"
                )
        if beats[0].get("beat") not in ("opening", "first_half"):
            return f"episode {number}: the first satisfaction beat must land in the first half"
    for before, now in zip(ordered, ordered[1:], strict=False):
        if before.get("lead_arc") == "suffers" and now.get("lead_arc") == "suffers":
            return (
                f"episodes {before['number']} and {now['number']} both leave the lead suffering; "
                "give one of them a win"
            )
    for start in range(0, max(0, len(ordered) - 3)):
        window = ordered[start : start + 4]
        if not any(isinstance(e.get("payoffs"), list) and e["payoffs"] for e in window):
            return (
                f"episodes {window[0]['number']} to {window[-1]['number']} pay nothing off; "
                "every four in a row must pay off at least one thread"
            )
    return None


def latest_docs(docs: list[VideoDramaDoc]) -> dict[tuple[str, int], VideoDramaDoc]:
    """The newest version of every document, keyed by kind and chapter (0 for the series')."""
    latest: dict[tuple[str, int], VideoDramaDoc] = {}
    for doc in docs:
        key = (doc.kind, doc.chapter_number)
        if key not in latest or doc.version > latest[key].version:
            latest[key] = doc
    return latest


def approved_doc(docs: list[VideoDramaDoc], kind: str, chapter: int = 0) -> VideoDramaDoc | None:
    """The newest approved version of a document, whatever came after it."""
    found = [
        doc
        for doc in docs
        if doc.kind == kind and doc.chapter_number == chapter and doc.status == "approved"
    ]
    return max(found, key=lambda doc: doc.version) if found else None


def doc_problem(series: VideoDramaSeries, payload: SeriesDocSubmitIn) -> str | None:
    """Why a document the worker sends cannot be filed, in the worker's words; None when it can.

    The shapes are the contract with tools/video/automation/series.mjs: a setting book names
    its characters; an outline lists every chapter with its episodes; a chapter outline gives
    every episode of its range the beats the owner reads.
    """
    body = payload.body_json
    if is_story(series):
        return (
            "a story series has no documents: its episodes come from the backlog import "
            "(python -m app.cli video-story-import)"
        )
    if is_one_off(series) and payload.kind != "bible":
        return "a one-off drama has one document, its story bible"
    if payload.kind == "bible" and not is_one_off(series):
        return "a story bible belongs to a one-off drama; a series has a setting book"
    if payload.kind == "bible" and is_explainer(series):
        return _explainer_bible_problem(body)
    if payload.kind in ("setting", "bible"):
        name = "story bible" if payload.kind == "bible" else "setting book"
        characters = body.get("characters")
        if not isinstance(characters, list) or not characters:
            return f"a {name} needs a characters list"
        for character in characters:
            if not isinstance(character, dict) or not all(
                isinstance(character.get(key), str) and character.get(key)
                for key in ("id", "name", "appearance")
            ):
                return "every character needs an id, a name and an appearance"
        if payload.kind == "bible":
            for key in BIBLE_LISTS:
                if not isinstance(body.get(key), list) or not body[key]:
                    return f"a story bible needs an {key} list"
            if not isinstance(body.get("outline"), dict):
                return "a story bible needs one outline (an object)"
        return None
    if payload.kind == "outline":
        chapters = body.get("chapters")
        total = chapter_count(series.planned_episodes, series.episodes_per_chapter)
        if not isinstance(chapters, list) or len(chapters) != total:
            return f"an outline lists {total} chapters"
        numbers: list[int] = []
        for chapter in chapters:
            if not isinstance(chapter, dict) or not isinstance(chapter.get("episodes"), list):
                return "every chapter needs a title and an episodes list"
            for episode in chapter["episodes"]:
                if not isinstance(episode, dict) or not isinstance(episode.get("number"), int):
                    return "every episode needs a number, a title and a logline"
                numbers.append(int(episode["number"]))
        if sorted(numbers) != list(range(1, series.planned_episodes + 1)):
            return f"the outline's episodes must be numbered 1 to {series.planned_episodes}"
        return None
    first, last = chapter_range(series, payload.chapter_number)
    if payload.chapter_number < 1 or first > series.planned_episodes:
        return f"chapter {payload.chapter_number} is outside the series"
    episodes = body.get("episodes")
    if not isinstance(episodes, list):
        return "a chapter outline needs an episodes list"
    numbers = []
    for episode in episodes:
        if not isinstance(episode, dict) or not isinstance(episode.get("number"), int):
            return "every episode needs a number"
        missing = [key for key in BEAT_FIELDS if not episode.get(key)]
        if missing:
            return f"episode {episode['number']} lacks {', '.join(missing)}"
        numbers.append(int(episode["number"]))
    if sorted(numbers) != list(range(first, last + 1)):
        return f"chapter {payload.chapter_number} covers episodes {first} to {last}"
    if retention_required(series):
        return _retention_problem(series, episodes)
    return None


@dataclass(frozen=True)
class NextJob:
    kind: str
    chapter_number: int | None = None
    episode_number: int | None = None
    previous: VideoDramaDoc | None = None
    rewrites_left: int = 0


def taipei_day(moment: datetime) -> date:
    """The Asia/Taipei calendar day of a moment; a naive one (SQLite hands those back) is UTC."""
    aware = moment if moment.tzinfo is not None else moment.replace(tzinfo=UTC)
    return aware.astimezone(TAIPEI).date()


def story_quota(
    series: VideoDramaSeries,
    episodes: list[VideoDramaEpisode],
    settings: VideoAutomationSettings,
    *,
    now: datetime,
    started_this_month: int,
    awaiting_upload: int,
) -> StoryQuotaOut:
    """Where a story series stands against its limits, and why no story starts now, if one
    does not (docs/videos/STORY.md §每日配額與排程).

    ``started_this_month`` counts the series' episodes started since the first of the month
    (UTC, as for every series); ``awaiting_upload`` its stories cleared for upload without a
    YouTube id (``_awaiting_upload``). The day's count is every episode whose ``started_at``
    falls on today's Asia/Taipei calendar day, whatever became of it since: 15:59:59Z is still
    that day in Taipei, 16:00:00Z is the next. The first limit that holds is the reason.
    """
    today = taipei_day(now)
    started_today = sum(
        1 for e in episodes if e.started_at is not None and taipei_day(e.started_at) == today
    )
    in_flight = sum(1 for e in episodes if e.status == "started")
    ready = sum(1 for e in episodes if e.status == "ready")
    per_day = series.episodes_per_day
    max_in_flight = settings.series_max_in_flight
    per_month = settings.series_episodes_per_month
    hold: StoryHold | None = None
    detail: str | None = None
    if series.status != "active":
        hold = "not_active"
        detail = "作品已暫停" if series.status == "paused" else "作品不在進行中"
    elif per_day is not None and started_today >= per_day:
        hold = "per_day"
        detail = f"今天（台北時間 {today:%m/%d}）已經開始 {started_today} 支，每日上限 {per_day} 支"
    elif in_flight >= max_in_flight:
        hold = "in_flight"
        detail = f"正在做的故事有 {in_flight} 支，同時進行的上限是 {max_in_flight} 支"
    elif started_this_month >= per_month:
        hold = "per_month"
        detail = f"本月已經開始 {started_this_month} 集，每月上限 {per_month} 集"
    elif awaiting_upload >= STORY_UPLOAD_BUFFER:
        hold = "upload_buffer"
        detail = (
            f"可以上架、還沒上傳的故事已有 {awaiting_upload} 支；滿 {STORY_UPLOAD_BUFFER} 支就先"
            "不開新的，上傳並貼上 YouTube 網址後會繼續"
        )
    elif ready == 0:
        hold = "none_ready"
        detail = "沒有待做的故事：清單裡的故事都開始過了，或還沒匯入"
    return StoryQuotaOut(
        day=today,
        started_today=started_today,
        episodes_per_day=per_day,
        in_flight=in_flight,
        max_in_flight=max_in_flight,
        started_this_month=started_this_month,
        episodes_per_month=per_month,
        awaiting_upload=awaiting_upload,
        upload_buffer=STORY_UPLOAD_BUFFER,
        ready=ready,
        hold=hold,
        hold_detail=detail,
    )


def _rewrite_job(
    kind: str, chapter: int, docs: list[VideoDramaDoc], rewrites: int
) -> NextJob | None:
    """Plan (or rewrite) a document when none is waiting or approved for this kind and chapter."""
    latest = latest_docs(docs).get((kind, chapter))
    if latest is None:
        return NextJob(kind=kind, chapter_number=chapter, rewrites_left=rewrites)
    if latest.status != "rejected":
        return None
    # The first version was not a rewrite: version 2 is the first rewrite. A version the
    # discussion replaced was not the owner sending it back, so it is not counted.
    discussed = sum(
        1
        for doc in docs
        if doc.kind == kind and doc.chapter_number == chapter and doc.note == DISCUSSION_NOTE
    )
    left = rewrites - (latest.version - 1 - discussed)
    if left <= 0:
        return None
    return NextJob(kind=kind, chapter_number=chapter, previous=latest, rewrites_left=left)


def next_job_for(
    series: VideoDramaSeries,
    docs: list[VideoDramaDoc],
    episodes: list[VideoDramaEpisode],
    settings: VideoAutomationSettings,
    *,
    started_this_month: int,
    now: datetime | None = None,
    awaiting_upload: int = 0,
) -> NextJob | None:
    """What the worker should do next for this series, or None when it waits for the owner.

    Documents come first (the setting book, then the outline, then a chapter's outline when it
    is due), then the next ready episode, in order, one at a time unless the settings allow two.

    A story series has no documents and its stories do not wait for one another: the next ready
    one in number order starts unless ``story_quota`` names a reason not to. ``now`` and
    ``awaiting_upload`` are read only there.
    """
    if is_story(series):
        quota = story_quota(
            series,
            episodes,
            settings,
            now=now or _now(),
            started_this_month=started_this_month,
            awaiting_upload=awaiting_upload,
        )
        if quota.hold is not None:
            return None
        return NextJob(
            kind="episode",
            episode_number=min(e.number for e in episodes if e.status == "ready"),
        )
    rewrites = settings.series_doc_rewrites
    if series.status == "setting":
        return _rewrite_job(setting_kind(series), 0, docs, rewrites)
    if series.status == "outline":
        return _rewrite_job("outline", 0, docs, rewrites)
    if series.status == "finished":
        # Every episode is cleared for upload: a compilation series joins them once
        # (docs/videos/BINGE.md), unless nothing was made or the owner skipped it all.
        if (
            series.compilation
            and series.compilation_slug is None
            and episodes
            and all(e.status in ("done", "skipped") for e in episodes)
            and any(e.status == "done" for e in episodes)
        ):
            return NextJob(kind="compilation")
        return None
    if series.status != "active":
        return None
    by_number = {episode.number: episode for episode in episodes}
    latest = latest_docs(docs)
    started_numbers = [e.number for e in episodes if e.status in ("started", "done", "skipped")]
    reached = max(started_numbers, default=0)
    # A one-off has no chapter outlines: its bible made the episode ready.
    total = (
        0
        if is_one_off(series)
        else chapter_count(series.planned_episodes, series.episodes_per_chapter)
    )
    for chapter in range(1, total + 1):
        current = latest.get(("chapter", chapter))
        if current is not None and current.status in ("review", "generating"):
            break
        if current is not None and current.status == "approved":
            continue
        previous_ok = chapter == 1 or (
            (previous := latest.get(("chapter", chapter - 1))) is not None
            and previous.status == "approved"
        )
        if not previous_ok:
            break
        _first, last_of_previous = chapter_range(series, chapter - 1) if chapter > 1 else (0, 0)
        due = (
            chapter == 1
            or series.requested_chapter == chapter
            or reached >= last_of_previous - settings.series_chapter_ahead
        )
        if not due:
            break
        job = _rewrite_job("chapter", chapter, docs, rewrites)
        if job is not None:
            return job
        break
    in_flight = sum(1 for episode in episodes if episode.status == "started")
    if in_flight >= settings.series_max_in_flight:
        return None
    if started_this_month >= settings.series_episodes_per_month:
        return None
    ready = sorted(e.number for e in episodes if e.status == "ready")
    if not ready:
        return None
    number = ready[0]
    previous_episode = by_number.get(number - 1)
    previous_done = number == 1 or (
        previous_episode is not None and previous_episode.status in ("done", "skipped")
    )
    if series.force_next:
        return NextJob(kind="episode", episode_number=number)
    if not previous_done or (number > 1 and not settings.series_auto_continue):
        return None
    return NextJob(kind="episode", episode_number=number)


def episode_rows_from_outline(
    series: VideoDramaSeries, body: dict[str, Any]
) -> dict[int, dict[str, str]]:
    """Every episode's title and logline from an approved outline, by number."""
    rows: dict[int, dict[str, str]] = {}
    for chapter in body.get("chapters") or []:
        if not isinstance(chapter, dict):
            continue
        for episode in chapter.get("episodes") or []:
            if not isinstance(episode, dict) or not isinstance(episode.get("number"), int):
                continue
            number = int(episode["number"])
            if 1 <= number <= series.planned_episodes:
                rows[number] = {
                    "title": str(episode.get("title") or f"第 {number} 集")[:200],
                    "logline": str(episode.get("logline") or ""),
                }
    for number in range(1, series.planned_episodes + 1):
        rows.setdefault(number, {"title": f"第 {number} 集", "logline": ""})
    return rows


def beats_from_chapter(body: dict[str, Any]) -> dict[int, dict[str, Any]]:
    """Every episode's beats from an approved chapter outline, by number."""
    beats: dict[int, dict[str, Any]] = {}
    for episode in body.get("episodes") or []:
        if isinstance(episode, dict) and isinstance(episode.get("number"), int):
            beats[int(episode["number"])] = dict(episode)
    return beats


# --- views ----------------------------------------------------------------------------------


def doc_subject(kind: str, chapter: int) -> str:
    """The discussion thread's subject for a document (docs/videos/DRAMA-FLOW.md §三)."""
    return f"chapter:{chapter}" if kind == "chapter" else kind


def doc_view(doc: VideoDramaDoc, unanswered: int = 0) -> SeriesDocOut:
    return SeriesDocOut(
        id=doc.id,
        kind=cast(Any, doc.kind),
        chapter_number=doc.chapter_number,
        version=doc.version,
        body_md=doc.body_md,
        body_json=doc.body_json or {},
        status=cast(Any, doc.status),
        note=doc.note,
        decided_at=doc.decided_at,
        created_at=doc.created_at,
        unanswered=unanswered,
    )


def episode_view(
    episode: VideoDramaEpisode, video: dict[str, object] | None = None, *, beats: bool = True
) -> SeriesEpisodeOut:
    return SeriesEpisodeOut(
        number=episode.number,
        chapter_number=episode.chapter_number,
        title=episode.title,
        logline=episode.logline,
        beats=(episode.beats or {}) if beats else {},
        status=cast(Any, episode.status),
        slug=episode.slug,
        recap=episode.recap,
        started_at=episode.started_at,
        finished_at=episode.finished_at,
        video=video,
    )


def summary_view(
    series: VideoDramaSeries,
    docs: list[VideoDramaDoc],
    episodes: list[VideoDramaEpisode],
    *,
    media_usd: float = 0.0,
    clip_seconds: int = 0,
    messages_pending: int = 0,
    quota: StoryQuotaOut | None = None,
) -> SeriesSummary:
    latest = latest_docs(docs)
    return SeriesSummary(
        id=series.id,
        slug=series.slug,
        kind=cast(Any, series.kind or "series"),
        title=series.title,
        premise=series.premise,
        aspects=cast(Any, list(series.aspects or [])),
        tone=cast(Any, series.tone),
        style_preset=cast(Any, series.style_preset),
        target_minutes=series.target_minutes,
        planned_episodes=series.planned_episodes,
        episodes_per_chapter=series.episodes_per_chapter,
        # Every story is an episode of chapter 1: a story series has no chapters to plan.
        chapters=(
            1
            if is_story(series)
            else chapter_count(series.planned_episodes, series.episodes_per_chapter)
        ),
        open_ended=series.open_ended,
        status=cast(Any, series.status),
        note=series.note,
        requested_chapter=series.requested_chapter,
        force_next=series.force_next,
        episodes_done=sum(1 for e in episodes if e.status == "done"),
        episodes_started=sum(1 for e in episodes if e.status == "started"),
        episodes_ready=sum(1 for e in episodes if e.status == "ready"),
        docs_pending=sum(1 for doc in latest.values() if doc.status == "review"),
        messages_pending=messages_pending,
        media_usd=media_usd,
        clip_seconds=clip_seconds,
        genre=cast(Any, series.genre or "xianxia-bonds"),
        lead=cast(Any, series.lead or "dual-male"),
        hands_off=bool(series.hands_off),
        compilation=bool(series.compilation),
        visual_tier=cast(Any, series.visual_tier or "clips"),
        total_minutes=series.total_minutes,
        compilation_slug=series.compilation_slug,
        compilation_started_at=series.compilation_started_at,
        compilation_finished_at=series.compilation_finished_at,
        episodes_per_day=series.episodes_per_day,
        image_model=series.image_model,
        look=dict(series.look) if isinstance(series.look, dict) else None,
        quota=quota,
        created_at=series.created_at,
        updated_at=series.updated_at,
    )


# --- loading ----------------------------------------------------------------------------------


async def _series(session: AsyncSession, slug: str, *, lock: bool = False) -> VideoDramaSeries:
    statement = select(VideoDramaSeries).where(VideoDramaSeries.slug == slug)
    if lock:
        statement = statement.with_for_update()
    row = await session.scalar(statement)
    if row is None:
        raise SeriesRefused(404, "video_series_not_found", "找不到這部作品")
    return row


async def _series_by_id(
    session: AsyncSession, series_id: Any, *, lock: bool = True
) -> VideoDramaSeries:
    statement = select(VideoDramaSeries).where(VideoDramaSeries.id == series_id)
    if lock:
        statement = statement.with_for_update()
    row = await session.scalar(statement)
    if row is None:
        raise SeriesRefused(404, "video_series_not_found", "找不到這部作品")
    return row


async def _docs(session: AsyncSession, series: VideoDramaSeries) -> list[VideoDramaDoc]:
    rows = await session.scalars(
        select(VideoDramaDoc)
        .where(VideoDramaDoc.series_id == series.id)
        .order_by(VideoDramaDoc.kind, VideoDramaDoc.chapter_number, VideoDramaDoc.version)
    )
    return list(rows.all())


async def _episodes(session: AsyncSession, series: VideoDramaSeries) -> list[VideoDramaEpisode]:
    rows = await session.scalars(
        select(VideoDramaEpisode)
        .where(VideoDramaEpisode.series_id == series.id)
        .order_by(VideoDramaEpisode.number)
    )
    return list(rows.all())


async def _unanswered(session: AsyncSession, series: VideoDramaSeries) -> dict[str, int]:
    """The owner's lines still waiting for the model, by thread subject."""
    rows = await session.execute(
        select(VideoDramaMessage.subject, func.count())
        .where(
            VideoDramaMessage.series_id == series.id,
            VideoDramaMessage.author == "owner",
            VideoDramaMessage.answered_at.is_(None),
        )
        .group_by(VideoDramaMessage.subject)
    )
    return {str(subject): int(count) for subject, count in rows.all()}


async def _started_this_month(session: AsyncSession, series: VideoDramaSeries) -> int:
    now = _now()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    found = await session.scalar(
        select(func.count())
        .select_from(VideoDramaEpisode)
        .where(VideoDramaEpisode.series_id == series.id, VideoDramaEpisode.started_at >= start)
    )
    return int(found or 0)


async def _awaiting_upload(session: AsyncSession, series: VideoDramaSeries) -> int:
    """How many of the series' episodes are cleared for upload and not on YouTube yet.

    Cleared for upload is the video's upload confirmation (its ``publish`` review) approved,
    the same record the "ready to upload" list reads (app.video_reviews.admin_service); on
    YouTube is ``youtube_video_id`` set, which the owner's pasted address or the site's own
    upload writes. A dropped video is never uploaded, so it does not count.
    """
    confirmed = select(VideoReview.project_id).where(
        VideoReview.gate == "publish", VideoReview.status == "approved"
    )
    found = await session.scalar(
        select(func.count(VideoProject.id))
        .select_from(VideoProject)
        .join(VideoDramaEpisode, VideoDramaEpisode.slug == VideoProject.slug)
        .where(
            VideoDramaEpisode.series_id == series.id,
            VideoProject.youtube_video_id.is_(None),
            VideoProject.dropped_at.is_(None),
            VideoProject.id.in_(confirmed),
        )
    )
    return int(found or 0)


async def _limits(session: AsyncSession) -> VideoAutomationSettings:
    """The settings row the series limits are read from; a page read does not create it, so
    before the owner first saves the settings the defaults stand in."""
    row = await session.scalar(
        select(VideoAutomationSettings).where(VideoAutomationSettings.id == 1)
    )
    if row is not None:
        return row
    return VideoAutomationSettings(
        series_max_in_flight=DEFAULT_DRAMA["series_max_in_flight"],
        series_episodes_per_month=DEFAULT_DRAMA["series_episodes_per_month"],
    )


async def _story_quota(
    session: AsyncSession, series: VideoDramaSeries, episodes: list[VideoDramaEpisode]
) -> StoryQuotaOut | None:
    """A story series' standing for the owner's page; None for the other kinds."""
    if not is_story(series):
        return None
    return story_quota(
        series,
        episodes,
        await _limits(session),
        now=_now(),
        started_this_month=await _started_this_month(session, series),
        awaiting_upload=await _awaiting_upload(session, series),
    )


async def _spend(session: AsyncSession, episodes: list[VideoDramaEpisode]) -> tuple[float, int]:
    slugs = [episode.slug for episode in episodes if episode.slug]
    if not slugs:
        return 0.0, 0
    spend = await spend_by_slug(session, slugs)
    return (
        round(sum(item.usd for item in spend.values()), 2),
        sum(item.clip_seconds for item in spend.values()),
    )


# --- the owner's side ---------------------------------------------------------------------------


def series_values(payload: SeriesIn, now: datetime) -> dict[str, Any]:
    """The row a form fills in, with what the one-button form leaves to the server.

    With ``total_minutes`` the episode count and the chapter size come from ``binge_shape``;
    a blank slug is named after the genre and the day, a blank title after the genre until
    the setting book names it, a blank premise says the planner invents it from the genre.
    """
    values = payload.model_dump()
    if payload.total_minutes is not None:
        planned, per_chapter = binge_shape(payload.total_minutes, payload.target_minutes)
        values["planned_episodes"] = planned
        values["episodes_per_chapter"] = per_chapter
    values["slug"] = payload.slug or auto_slug(payload.genre, now)
    values["title"] = payload.title or auto_title(payload.genre)
    values["premise"] = payload.premise or (
        f"由企劃依「{GENRE_LABELS.get(payload.genre, payload.genre)}」題材預設自擬前提"
    )
    return values


async def create_series(session: AsyncSession, actor: User, payload: SeriesIn) -> SeriesOut:
    row = await add_series(session, actor, payload)
    await session.commit()
    return await series_view(session, row.slug)


async def add_series(
    session: AsyncSession, actor: User | None, payload: SeriesIn
) -> VideoDramaSeries:
    """The new series row and its audit entry, added to the caller's unit of work.

    A long series starts at its setting book, a one-off at its story bible with its episode 1
    planned; a story series is active at once, since it has no documents: its episodes come
    from the backlog import (``app.video_automation.stories``), which also calls this with no
    actor when the series does not exist yet.
    """
    now = _now()
    values = series_values(payload, now)
    taken = await session.scalar(
        select(VideoDramaSeries.id).where(VideoDramaSeries.slug == values["slug"])
    )
    if taken is not None:
        raise SeriesRefused(409, "video_series_slug_taken", f"{values['slug']} 已經是另一部作品")
    row = VideoDramaSeries(
        id=uuid4(),
        **values,
        status="active" if payload.kind == "story" else "setting",
        created_by_user_id=actor.id if actor else None,
        created_at=now,
        updated_at=now,
    )
    session.add(row)
    if is_one_off(row):
        # The one episode exists from the start; the bible's approval makes it ready. Nothing
        # tells the unit of work to write the series first: flush it before the episode.
        await session.flush()
        session.add(_new_episode(row, 1, row.title, ""))
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id if actor else None,
            action="video_series_created",
            target=f"video-series:{row.slug}",
            metadata_json={
                "kind": row.kind,
                "planned_episodes": values["planned_episodes"],
                "episodes_per_chapter": values["episodes_per_chapter"],
                "tone": payload.tone,
                "genre": payload.genre,
                "lead": payload.lead,
                "hands_off": payload.hands_off,
                "compilation": payload.compilation,
                "visual_tier": payload.visual_tier,
                "total_minutes": payload.total_minutes,
                "target_minutes": payload.target_minutes,
                "episodes_per_day": payload.episodes_per_day,
                "image_model": payload.image_model,
            },
        )
    )
    return row


def one_off_slug(request_id: Any) -> str:
    return f"{ONE_OFF_PREFIX}{str(request_id).replace('-', '')[:8]}"


async def create_one_off(
    session: AsyncSession, actor: User, payload: DramaRequestIn
) -> DramaRequestOut:
    """The owner's drama request form: a one-off series with its episode 1 planned and the
    request row that episode will travel as, pointing at the series
    (docs/videos/DRAMA-FLOW.md §二). The worker plans the story bible on its next round."""
    now = _now()
    request_id = uuid4()
    slug = one_off_slug(request_id)
    taken = await session.scalar(select(VideoDramaSeries.id).where(VideoDramaSeries.slug == slug))
    if taken is not None:
        raise SeriesRefused(409, "video_series_slug_taken", f"{slug} 已經是另一部作品")
    series = VideoDramaSeries(
        id=uuid4(),
        slug=slug,
        kind="one-off",
        title=(payload.title or payload.premise)[:200],
        premise=payload.premise,
        aspects=[],
        style_preset=payload.style_preset,
        target_minutes=payload.target_minutes,
        planned_episodes=ONE_OFF_EPISODES,
        episodes_per_chapter=ONE_OFF_EPISODES,
        open_ended=False,
        status="setting",
        note=payload.note,
        created_by_user_id=actor.id,
        created_at=now,
        updated_at=now,
    )
    session.add(series)
    # The episode and the request point at the series, and nothing tells the unit of work to
    # write the series first: flush it before they carry its id.
    await session.flush()
    session.add(_new_episode(series, 1, series.title, ""))
    request = VideoDramaRequest(
        id=request_id,
        premise=payload.premise,
        title=payload.title,
        source_guide=payload.source_guide,
        style_preset=payload.style_preset,
        target_minutes=payload.target_minutes,
        note=payload.note,
        status="queued",
        series_id=series.id,
        episode_number=1,
        created_by_user_id=actor.id,
        created_at=now,
        updated_at=now,
    )
    session.add(request)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_drama_request_created",
            target=f"video-drama-request:{request.id}",
            metadata_json={
                "series_slug": slug,
                "style_preset": payload.style_preset,
                "target_minutes": payload.target_minutes,
                "source_guide": payload.source_guide,
            },
        )
    )
    await session.commit()
    return request_view(request, series_slug=slug)


async def list_series(session: AsyncSession, *, kind: str | None = None) -> list[SeriesSummary]:
    statement = select(VideoDramaSeries).order_by(VideoDramaSeries.created_at.desc()).limit(50)
    if kind is not None:
        statement = statement.where(VideoDramaSeries.kind == kind)
    rows = list((await session.scalars(statement)).all())
    out: list[SeriesSummary] = []
    for series in rows:
        docs = await _docs(session, series)
        episodes = await _episodes(session, series)
        usd, seconds = await _spend(session, episodes)
        waiting = await _unanswered(session, series)
        out.append(
            summary_view(
                series,
                docs,
                episodes,
                media_usd=usd,
                clip_seconds=seconds,
                messages_pending=sum(waiting.values()),
                quota=await _story_quota(session, series, episodes),
            )
        )
    return out


async def series_view(session: AsyncSession, slug: str) -> SeriesOut:
    series = await _series(session, slug)
    docs = await _docs(session, series)
    episodes = await _episodes(session, series)
    usd, seconds = await _spend(session, episodes)
    waiting = await _unanswered(session, series)
    videos = {
        project.slug: project.model_dump(mode="json")
        for project in await list_projects(session, series_slug=series.slug, limit=1000)
    }
    return SeriesOut(
        **summary_view(
            series,
            docs,
            episodes,
            media_usd=usd,
            clip_seconds=seconds,
            messages_pending=sum(waiting.values()),
            quota=await _story_quota(session, series, episodes),
        ).model_dump(),
        docs=[
            doc_view(doc, waiting.get(doc_subject(doc.kind, doc.chapter_number), 0))
            for doc in latest_docs(docs).values()
        ],
        episodes=[episode_view(episode, videos.get(episode.slug or "")) for episode in episodes],
    )


def patch_problem(series: VideoDramaSeries, changes: dict[str, Any]) -> SeriesRefused | None:
    """Why a change the schema accepts does not fit this kind of series, or None.

    Only a story series has a daily count and a shared look, and only a story runs longer than
    SERIES_MAX_MINUTES. A story series stays hands-off, stills only and never compiled, keeps a
    look, and has no chapters to resize.
    """
    if not is_story(series):
        if changes.get("episodes_per_day") is not None or changes.get("look") is not None:
            return SeriesRefused(
                422, "video_series_story_only", "每日支數與共用畫風只有品牌故事作品才有"
            )
        if (changes.get("target_minutes") or 0) > SERIES_MAX_MINUTES:
            return SeriesRefused(
                422, "video_series_too_long", f"漫劇一集最長 {SERIES_MAX_MINUTES} 分鐘"
            )
        return None
    if (
        changes.get("hands_off") is False
        or changes.get("compilation") is True
        or changes.get("visual_tier", "stills") != "stills"
    ):
        return SeriesRefused(
            409, "video_series_story_fixed", "品牌故事一律免關卡、全部靜態圖，也不做合集"
        )
    if "look" in changes and changes["look"] is None:
        return SeriesRefused(422, "video_series_story_look", "品牌故事要留著每個故事共用的畫風")
    if "episodes_per_chapter" in changes:
        return SeriesRefused(409, "video_series_story_fixed", "品牌故事沒有篇章，不分每篇集數")
    return None


async def patch_series(
    session: AsyncSession, actor: User, slug: str, payload: SeriesPatch
) -> SeriesOut:
    series = await _series(session, slug, lock=True)
    changes = payload.model_dump(exclude_unset=True)
    refused = patch_problem(series, changes)
    if refused is not None:
        raise refused
    if "status" in changes and series.status in ("setting", "outline"):
        raise SeriesRefused(
            409, "video_series_not_planned", "設定集與總綱核准之後，作品才能暫停、繼續或完結"
        )
    if is_one_off(series) and {"planned_episodes", "episodes_per_chapter"} & set(changes):
        raise SeriesRefused(409, "video_series_one_off_fixed", "單集漫劇只有一集，集數不能改")
    episodes = await _episodes(session, series)
    reached = max((e.number for e in episodes if e.status != "planned"), default=0)
    if "planned_episodes" in changes and changes["planned_episodes"] < reached:
        raise SeriesRefused(
            409, "video_series_too_short", f"已經做到第 {reached} 集，集數不能比它少"
        )
    if "episodes_per_chapter" in changes and episodes:
        raise SeriesRefused(409, "video_series_chapters_fixed", "總綱核准之後，每篇集數就固定了")
    if "visual_tier" in changes and reached:
        raise SeriesRefused(409, "video_series_tier_fixed", "已經有集數開始做，畫面等級不能再改")
    for key, value in changes.items():
        setattr(series, key, value)
    series.updated_at = _now()
    # A story series' episodes are its imported stories, so its count changes no rows.
    if "planned_episodes" in changes and episodes and not is_story(series):
        # A longer series: the new episodes exist as planned rows, titled by number.
        known = {episode.number for episode in episodes}
        for number in range(1, series.planned_episodes + 1):
            if number not in known:
                session.add(_new_episode(series, number, f"第 {number} 集", ""))
        for episode in episodes:
            if episode.number > series.planned_episodes and episode.status == "planned":
                await session.delete(episode)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_series_updated",
            target=f"video-series:{series.slug}",
            metadata_json={"changed": sorted(changes)},
        )
    )
    await session.commit()
    return await series_view(session, slug)


async def withdraw_series(session: AsyncSession, actor: User, slug: str) -> SeriesWithdrawnOut:
    """The owner takes back a drama no episode of which has started: a one-off still at its
    story bible, or a series still at its documents. The series goes with its documents,
    threads and episode rows; the requests still queued for it stay as cancelled rows, so the
    request list keeps the record. Once an episode is in the making it is dropped as a video."""
    series = await _series(session, slug, lock=True)
    begun = [e.number for e in await _episodes(session, series) if e.status not in WITHDRAWABLE]
    if begun:
        raise SeriesRefused(
            409,
            "video_series_started",
            f"第 {min(begun)} 集已經開始做了，不能撤回；要停就到影片清單放棄那支影片",
        )
    now = _now()
    requests = list(
        (
            await session.scalars(
                select(VideoDramaRequest)
                .where(
                    VideoDramaRequest.series_id == series.id,
                    VideoDramaRequest.status == "queued",
                )
                .with_for_update()
            )
        ).all()
    )
    for request in requests:
        request.status = "cancelled"
        request.cancelled_at = now
        request.updated_at = now
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_series_withdrawn",
            target=f"video-series:{series.slug}",
            metadata_json={
                "kind": series.kind,
                "status": series.status,
                "requests_cancelled": [str(request.id) for request in requests],
            },
        )
    )
    # The requests keep their row and lose the series (ON DELETE SET NULL); write their new
    # status before the series goes.
    await session.flush()
    await session.delete(series)
    await session.commit()
    return SeriesWithdrawnOut(slug=slug, requests_cancelled=len(requests))


def _new_episode(
    series: VideoDramaSeries, number: int, title: str, logline: str
) -> VideoDramaEpisode:
    now = _now()
    return VideoDramaEpisode(
        id=uuid4(),
        series_id=series.id,
        number=number,
        chapter_number=chapter_of(series, number),
        title=title,
        logline=logline,
        beats={},
        status="planned",
        state_json={},
        created_at=now,
        updated_at=now,
    )


async def _doc(
    session: AsyncSession, series: VideoDramaSeries, kind: str, chapter: int
) -> VideoDramaDoc:
    doc = await session.scalar(
        select(VideoDramaDoc)
        .where(
            VideoDramaDoc.series_id == series.id,
            VideoDramaDoc.kind == kind,
            VideoDramaDoc.chapter_number == chapter,
        )
        .order_by(VideoDramaDoc.version.desc())
        .limit(1)
        .with_for_update()
    )
    if doc is None:
        raise SeriesRefused(404, "video_series_doc_not_found", "這份文件還沒有產生")
    return doc


async def _apply_approval(
    session: AsyncSession, series: VideoDramaSeries, doc: VideoDramaDoc
) -> None:
    """What an approved document changes: the series moves on, the episode table fills in."""
    body = doc.body_json or {}
    if doc.kind == "bible":
        # The one-off's only document: its episode is ready, with the bible's outline as its
        # beats, and the series is active at once (no outline, no chapter to plan).
        episodes = {episode.number: episode for episode in await _episodes(session, series)}
        episode = episodes.get(1)
        if episode is None:
            episode = _new_episode(series, 1, series.title, "")
            session.add(episode)
        raw_outline = body.get("outline")
        outline: dict[str, Any] = dict(raw_outline) if isinstance(raw_outline, dict) else {}
        if episode.status in ("planned", "ready"):
            episode.title = str(outline.get("title") or series.title)[:200]
            episode.logline = str(outline.get("logline") or series.premise)
            episode.beats = {key: value for key, value in outline.items() if key != "number"}
            episode.status = "ready"
            episode.updated_at = _now()
        if series.status in ("setting", "outline"):
            series.status = "active"
    elif doc.kind == "setting":
        if series.status == "setting":
            series.status = "outline"
        # The one-button form left the title to the planner: the setting book names it.
        title = body.get("title")
        if AUTO_TITLE in series.title and isinstance(title, str) and title.strip():
            series.title = title.strip()[:200]
    elif doc.kind == "outline":
        rows = episode_rows_from_outline(series, body)
        episodes = {episode.number: episode for episode in await _episodes(session, series)}
        for number, values in rows.items():
            episode = episodes.get(number)
            if episode is None:
                session.add(_new_episode(series, number, values["title"], values["logline"]))
            elif episode.status == "planned":
                episode.title = values["title"]
                episode.logline = values["logline"]
                episode.updated_at = _now()
        if series.status == "outline":
            series.status = "active"
    else:
        beats = beats_from_chapter(body)
        episodes = {episode.number: episode for episode in await _episodes(session, series)}
        first, last = chapter_range(series, doc.chapter_number)
        for number in range(first, last + 1):
            planned = beats.get(number)
            episode = episodes.get(number)
            if episode is None:
                episode = _new_episode(series, number, f"第 {number} 集", "")
                session.add(episode)
            if episode.status not in ("planned", "ready") or planned is None:
                continue
            episode.title = str(planned.get("title") or episode.title)[:200]
            episode.logline = str(planned.get("logline") or episode.logline)
            episode.beats = {key: value for key, value in planned.items() if key != "number"}
            episode.status = "ready"
            episode.updated_at = _now()
        if series.requested_chapter == doc.chapter_number:
            series.requested_chapter = None
    series.updated_at = _now()


async def decide_doc(
    session: AsyncSession,
    actor: User,
    slug: str,
    kind: str,
    chapter: int,
    decision: str,
    note: str | None,
) -> SeriesOut:
    series = await _series(session, slug, lock=True)
    doc = await _doc(session, series, kind, chapter)
    if doc.status != "review":
        raise SeriesRefused(409, "video_series_doc_not_pending", "這份文件不在等你決定")
    text = (note or "").strip()
    if decision == "reject" and not text:
        raise SeriesRefused(422, "video_series_note_required", "退回要寫原因，模型才知道改什麼")
    doc.status = "approved" if decision == "approve" else "rejected"
    doc.note = text or None
    doc.decided_at = _now()
    doc.decided_by_user_id = actor.id
    if decision == "approve":
        await _apply_approval(session, series, doc)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action=f"video_series_doc_{doc.status}",
            target=f"video-series:{series.slug}",
            metadata_json={"kind": kind, "chapter": chapter, "version": doc.version},
        )
    )
    await session.commit()
    return await series_view(session, slug)


async def edit_doc(
    session: AsyncSession,
    actor: User,
    slug: str,
    kind: str,
    chapter: int,
    payload: SeriesDocEditIn,
) -> SeriesOut:
    """The owner's own version of a document: a new version, approved at once when asked."""
    series = await _series(session, slug, lock=True)
    docs = await _docs(session, series)
    latest = latest_docs(docs).get((kind, chapter))
    if latest is None:
        raise SeriesRefused(404, "video_series_doc_not_found", "這份文件還沒有產生")
    body_json = payload.body_json if payload.body_json is not None else latest.body_json
    if payload.approve:
        problem = doc_problem(
            series,
            SeriesDocSubmitIn(
                kind=cast(Any, kind),
                chapter_number=chapter,
                body_md=payload.body_md,
                body_json=body_json or {},
            ),
        )
        if problem:
            raise SeriesRefused(422, "video_series_doc_invalid", problem)
    if latest.status == "review":
        latest.status = "rejected"
        latest.note = latest.note or "站主自己改了一版"
        latest.decided_at = _now()
        latest.decided_by_user_id = actor.id
    doc = VideoDramaDoc(
        id=uuid4(),
        series_id=series.id,
        kind=kind,
        chapter_number=chapter,
        version=latest.version + 1,
        body_md=payload.body_md,
        body_json=body_json or {},
        status="approved" if payload.approve else "review",
        decided_at=_now() if payload.approve else None,
        decided_by_user_id=actor.id if payload.approve else None,
        created_at=_now(),
    )
    session.add(doc)
    if payload.approve:
        await _apply_approval(session, series, doc)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_series_doc_edited",
            target=f"video-series:{series.slug}",
            metadata_json={"kind": kind, "chapter": chapter, "version": doc.version},
        )
    )
    await session.commit()
    return await series_view(session, slug)


async def edit_episode(
    session: AsyncSession, actor: User, slug: str, number: int, payload: SeriesEpisodeEditIn
) -> SeriesOut:
    series = await _series(session, slug, lock=True)
    episode = await _episode(session, series, number)
    if episode.status not in ("planned", "ready"):
        raise SeriesRefused(409, "video_series_episode_started", "這一集已經開始做，不能再改細綱")
    changes = payload.model_dump(exclude_unset=True)
    for key, value in changes.items():
        if value is not None:
            setattr(episode, key, value)
    episode.updated_at = _now()
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_series_episode_edited",
            target=f"video-series:{series.slug}",
            metadata_json={"number": number, "changed": sorted(changes)},
        )
    )
    await session.commit()
    return await series_view(session, slug)


async def _episode(
    session: AsyncSession, series: VideoDramaSeries, number: int
) -> VideoDramaEpisode:
    episode = await session.scalar(
        select(VideoDramaEpisode)
        .where(VideoDramaEpisode.series_id == series.id, VideoDramaEpisode.number == number)
        .with_for_update()
    )
    if episode is None:
        raise SeriesRefused(404, "video_series_episode_not_found", f"這部作品沒有第 {number} 集")
    return episode


async def act(session: AsyncSession, actor: User, slug: str, action: str) -> tuple[SeriesOut, str]:
    """The owner pushes the series along: plan the next chapter now, or start the next episode
    without waiting for the previous one."""
    series = await _series(session, slug, lock=True)
    if is_story(series):
        # No chapter to plan, no compilation, and a story never waits for the one before it.
        raise SeriesRefused(
            409,
            "video_series_story_no_action",
            "品牌故事沒有篇章也不做合集；故事照每日支數自己開始，要調整就改每日支數或暫停作品",
        )
    docs = await _docs(session, series)
    latest = latest_docs(docs)
    total = (
        0
        if is_one_off(series)
        else chapter_count(series.planned_episodes, series.episodes_per_chapter)
    )
    if action == "compile":
        if is_one_off(series):
            raise SeriesRefused(409, "video_series_one_off_single", "單集漫劇只有一集，沒有合集")
        # The owner asks for the compilation of a finished series that was not set up to
        # make one (docs/videos/BINGE.md). A series keeps the one compilation it has: the
        # worker names the video <series>-full, that slug is the first compilation's, and
        # clearing it here would also take the first cut's download away.
        if series.status != "finished":
            raise SeriesRefused(409, "video_series_not_finished", "每一集都完成之後才能做合集")
        if series.compilation_slug is not None:
            if series.compilation_finished_at is None:
                raise SeriesRefused(409, "video_series_compiling", "合集正在做")
            raise SeriesRefused(409, "video_series_compiled", "合集已經做過；成片從作品頁下載")
        series.compilation = True
        series.compilation_started_at = None
        series.compilation_finished_at = None
        series.updated_at = _now()
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action="video_series_action",
                target=f"video-series:{series.slug}",
                metadata_json={"action": action},
            )
        )
        await session.commit()
        return await series_view(session, slug), "工人的下一輪會開始做合集"
    if series.status != "active":
        raise SeriesRefused(409, "video_series_not_active", "作品要在進行中才能推進")
    if action == "plan-next-chapter":
        pending = [
            chapter
            for chapter in range(1, total + 1)
            if (doc := latest.get(("chapter", chapter))) is None or doc.status != "approved"
        ]
        if not pending:
            raise SeriesRefused(409, "video_series_all_planned", "每一篇都已經規劃過了")
        series.requested_chapter = pending[0]
        detail = f"第 {pending[0]} 篇的細綱會在工人的下一輪產生"
    else:
        series.force_next = True
        detail = "工人的下一輪會開始下一集，不等上一集上架"
    series.updated_at = _now()
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_series_action",
            target=f"video-series:{series.slug}",
            metadata_json={"action": action},
        )
    )
    await session.commit()
    return await series_view(session, slug), detail


async def skip_episode(session: AsyncSession, actor: User, slug: str, number: int) -> SeriesOut:
    series = await _series(session, slug, lock=True)
    episode = await _episode(session, series, number)
    if episode.status not in ("planned", "ready"):
        raise SeriesRefused(409, "video_series_episode_started", "這一集已經開始做，不能跳過")
    now = _now()
    episode.status = "skipped"
    episode.updated_at = now
    # The skipped episode may have been the last one open: the series finishes the same way
    # it does when the worker reports the last episode, or a compilation series would wait
    # for a job that never comes (docs/videos/BINGE.md).
    finish_if_complete(series, await _episodes(session, series), now)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_series_episode_skipped",
            target=f"video-series:{series.slug}",
            metadata_json={"number": number},
        )
    )
    await session.commit()
    return await series_view(session, slug)


async def restore_episode(session: AsyncSession, actor: User, slug: str, number: int) -> SeriesOut:
    """Bring a skipped story back to ready: the day's count, the other limits and the worker's
    next job read the rows, so they see it at once (``story_quota``, ``next_job_for``).

    A story series only. Its stories stand alone and start in number order without waiting for
    one another, so a story brought back just takes its turn again. An episode of a long series
    is written after the one before it and from its recap, and the episodes after a skipped one
    went on without it; brought back, it would be made after them and would not fit what they
    already tell. A one-off is its only episode. Those are refused rather than reordered.

    A story that never started only: one that started (``started_at`` set) was skipped when its
    video was dropped, and its slug stays that video's, so it could never start again and, as
    the lowest ready number, would hold up every story after it. When skipping this story had
    finished the series, the series is active again.
    """
    series = await _series(session, slug, lock=True)
    if not is_story(series):
        raise SeriesRefused(
            409,
            "video_series_restore_story_only",
            "只有品牌故事能恢復略過的集數：漫劇一集接著一集寫，後面的劇情已經當這一集不存在，"
            "恢復了會接不上",
        )
    episode = await _episode(session, series, number)
    if episode.status != "skipped":
        raise SeriesRefused(
            409, "video_series_episode_not_skipped", f"第 {number} 個故事沒有被略過，不用恢復"
        )
    if episode.started_at is not None:
        raise SeriesRefused(
            409,
            "video_series_episode_was_started",
            f"第 {number} 個故事在 {taipei_day(episode.started_at):%m/%d} 開始做過、影片已經放棄，"
            f"影片代號 {episode.slug} 留給那支影片；只有從沒開始過的故事能恢復",
        )
    now = _now()
    episode.status = "ready"
    episode.updated_at = now
    reopened = series.status == "finished"
    if reopened:
        series.status = "active"
        series.updated_at = now
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_series_episode_restored",
            target=f"video-series:{series.slug}",
            metadata_json={
                "number": number,
                "story": (episode.beats or {}).get("id"),
                "reopened": reopened,
            },
        )
    )
    await session.commit()
    return await series_view(session, slug)


# --- the worker's side ----------------------------------------------------------------------------


async def context_view(
    session: AsyncSession, series: VideoDramaSeries, episode_number: int | None
) -> SeriesContextOut:
    docs = await _docs(session, series)
    episodes = await _episodes(session, series)
    # A story series has no chapter outline to read (docs/videos/STORY.md).
    chapter = (
        chapter_of(series, episode_number) if episode_number and not is_story(series) else None
    )
    episode = next((e for e in episodes if e.number == episode_number), None)
    # A one-off's story bible stands where a series' setting book does: the cast, the mysteries
    # and the document the writer reads (docs/videos/DRAMA-FLOW.md §二).
    setting = approved_doc(docs, setting_kind(series))
    done = [e for e in episodes if e.status == "done" and e.recap]
    recaps = [
        {"number": e.number, "title": e.title, "recap": e.recap, "state": e.state_json or {}}
        for e in done[-RECENT_RECAPS:]
    ]
    all_recaps = [{"number": e.number, "title": e.title, "recap": e.recap} for e in done]
    mysteries = (setting.body_json or {}).get("mysteries") if setting else None
    return SeriesContextOut(
        series=summary_view(series, docs, episodes),
        setting=doc_view(setting) if setting else None,
        outline=(doc_view(found) if (found := approved_doc(docs, "outline")) else None),
        chapter=(
            doc_view(found)
            if chapter
            and not is_one_off(series)
            and (found := approved_doc(docs, "chapter", chapter))
            else None
        ),
        chapter_number=chapter,
        chapter_range=chapter_range(series, chapter) if chapter else None,
        episode=episode_view(episode) if episode else None,
        # A story is written from its own plan alone, and a hundred whole plans are over half a
        # megabyte: the other stories are listed without their beats.
        episodes=[episode_view(e, beats=not is_story(series)) for e in episodes],
        recaps=cast(list[dict[str, object]], recaps),
        mysteries=cast(list[dict[str, object]], mysteries if isinstance(mysteries, list) else []),
        all_recaps=cast(list[dict[str, object]], all_recaps),
    )


async def next_job(session: AsyncSession, settings: VideoAutomationSettings) -> SeriesJobOut:
    """The next document to plan or episode to start across every series, oldest series first."""
    rows = list(
        (
            await session.scalars(
                select(VideoDramaSeries)
                .where(
                    or_(
                        VideoDramaSeries.status.in_(ACTIVE_STATUSES),
                        and_(
                            VideoDramaSeries.status == "finished",
                            VideoDramaSeries.compilation.is_(True),
                            VideoDramaSeries.compilation_slug.is_(None),
                        ),
                    )
                )
                .order_by(VideoDramaSeries.created_at)
            )
        ).all()
    )
    now = _now()
    for series in rows:
        docs = await _docs(session, series)
        episodes = await _episodes(session, series)
        job = next_job_for(
            series,
            docs,
            episodes,
            settings,
            started_this_month=await _started_this_month(session, series),
            now=now,
            awaiting_upload=await _awaiting_upload(session, series) if is_story(series) else 0,
        )
        if job is None:
            continue
        episode = (
            next((e for e in episodes if e.number == job.episode_number), None)
            if job.episode_number
            else None
        )
        chapter_for_context = job.chapter_number if job.kind == "chapter" else None
        context = await context_view(
            session,
            series,
            job.episode_number
            or (chapter_range(series, chapter_for_context)[0] if chapter_for_context else None),
        )
        return SeriesJobOut(
            job=SeriesJob(
                kind=cast(Any, job.kind),
                series=summary_view(series, docs, episodes),
                chapter_number=job.chapter_number if job.kind == "chapter" else None,
                episode=episode_view(episode) if episode else None,
                previous=doc_view(job.previous) if job.previous else None,
                rewrites_left=job.rewrites_left,
                context=context,
            )
        )
    return SeriesJobOut(job=None)


def auto_doc_status(
    series: VideoDramaSeries, payload: SeriesDocSubmitIn, version: int, rewrites: int
) -> tuple[str, str | None]:
    """What the server decides about a filed document, and the note that says why.

    A classic series, or a version filed without a verdict, waits for the owner. A hands-off
    series (docs/videos/BINGE.md) is approved when the checker's verdict passes, sent back for
    a rewrite while the rewrites the settings allow are not spent (version 2 is the first
    rewrite), and left for the owner with the checker's problems once they are.
    """
    if not series.hands_off or payload.judge is None:
        return "review", None
    passed = series_doc_passed(payload.judge, payload.kind)
    note = series_doc_note(payload.judge, passed)
    if passed:
        return "approved", note
    if version - 1 < rewrites:
        return "rejected", note
    return "review", note


async def submit_doc(
    session: AsyncSession,
    slug: str,
    payload: SeriesDocSubmitIn,
    settings: VideoAutomationSettings | None = None,
) -> SeriesDocOut:
    """The worker files a planned document as a new version that waits for the owner, or,
    on a hands-off series, is decided from the checker's verdict as it arrives."""
    series = await _series(session, slug, lock=True)
    problem = doc_problem(series, payload)
    if problem:
        raise SeriesRefused(422, "video_series_doc_invalid", problem)
    docs = await _docs(session, series)
    latest = latest_docs(docs).get((payload.kind, payload.chapter_number))
    if latest is not None and latest.status in ("review", "approved"):
        raise SeriesRefused(
            409, "video_series_doc_not_wanted", "這份文件已經在等站主或已核准，不能再送一版"
        )
    version = (latest.version + 1) if latest else 1
    rewrites = settings.series_doc_rewrites if settings is not None else 0
    status, note = auto_doc_status(series, payload, version, rewrites)
    now = _now()
    doc = VideoDramaDoc(
        id=uuid4(),
        series_id=series.id,
        kind=payload.kind,
        chapter_number=payload.chapter_number,
        version=version,
        body_md=payload.body_md,
        body_json=payload.body_json,
        status=status,
        note=note,
        decided_at=now if status != "review" else None,
        created_at=now,
    )
    session.add(doc)
    if status == "approved":
        await _apply_approval(session, series, doc)
    if status != "review":
        session.add(
            AdminAuditLog(
                actor_user_id=None,
                action=f"video_series_doc_auto_{status}",
                target=f"video-series:{series.slug}",
                metadata_json={
                    "kind": payload.kind,
                    "chapter": payload.chapter_number,
                    "version": version,
                    "verdicts": (payload.judge or {}).get("verdicts"),
                },
            )
        )
    series.updated_at = now
    await session.commit()
    return doc_view(doc)


async def start_episode(
    session: AsyncSession, token: VideoToolToken, slug: str, number: int, video_slug: str
) -> SeriesEpisodeStartOut:
    """The worker starts an episode: a request row is filed as started under the video's slug,
    so the episode travels through the same path as a one-off request."""
    series = await _series(session, slug, lock=True)
    episode = await _episode(session, series, number)
    if episode.status != "ready":
        raise SeriesRefused(
            409,
            "video_series_episode_not_ready",
            "故事聖經還沒核准"
            if is_one_off(series)
            else "這個故事已經開始、做完或略過"
            if is_story(series)
            else "這一集的篇章細綱還沒核准",
        )
    # A story's video slug was planned with it and imported (docs/videos/STORY.md); the video
    # is made under that name or not at all, so the backlog and the video list stay one.
    if is_story(series) and episode.slug and video_slug != episode.slug:
        raise SeriesRefused(
            409,
            "video_series_story_slug",
            f"這個故事的影片代號是 {episode.slug}，不是 {video_slug}",
        )
    if is_story(series):
        # GET next only advertised this job. Recheck the current limits while holding the
        # series lock, so a pause or a newly exhausted quota stops a stale or direct start.
        quota = await _story_quota(session, series, await _episodes(session, series))
        if quota is not None and quota.hold is not None:
            raise SeriesRefused(
                409,
                "video_series_story_held",
                quota.hold_detail or "這個故事目前不能開始",
            )
    taken = await session.scalar(
        select(VideoDramaRequest.id).where(VideoDramaRequest.slug == video_slug)
    )
    if taken is not None:
        raise SeriesRefused(409, "video_drama_request_slug_taken", f"{video_slug} 已經是另一支影片")
    now = _now()
    # A one-off's request row was filed with the series (or by migration 0107): the episode
    # travels as that row, so the owner's queue shows it started rather than a second request.
    queued = await session.scalar(
        select(VideoDramaRequest)
        .where(
            VideoDramaRequest.series_id == series.id,
            VideoDramaRequest.episode_number == number,
            VideoDramaRequest.status == "queued",
        )
        .with_for_update()
    )
    if queued is not None:
        request = queued
        request.status = "started"
        request.slug = video_slug
        request.started_by_token_id = token.id
        request.started_at = now
        request.updated_at = now
    else:
        beats = episode.beats or {}
        fields = STORY_PREMISE_FIELDS if is_story(series) else BEAT_FIELDS
        premise = "\n".join(
            part
            for part in (
                f"{series.title} 第 {number} 集：{episode.title}",
                episode.logline,
                *(f"{key}: {beats[key]}" for key in fields if isinstance(beats.get(key), str)),
            )
            if part
        )[:4000]
        request = VideoDramaRequest(
            id=uuid4(),
            premise=premise or episode.title,
            title=f"{series.title} 第 {number} 集 {episode.title}"[:200],
            style_preset=series.style_preset,
            target_minutes=series.target_minutes,
            note=series.note,
            status="started",
            slug=video_slug,
            series_id=series.id,
            episode_number=number,
            started_by_token_id=token.id,
            created_at=now,
            updated_at=now,
            started_at=now,
        )
        session.add(request)
    # The episode points at the request, and nothing tells the unit of work which of the two
    # to write first: flush the request before the episode carries its id.
    await session.flush()
    episode.status = "started"
    episode.slug = video_slug
    episode.request_id = request.id
    episode.started_at = now
    episode.updated_at = now
    series.force_next = False
    series.updated_at = now
    project = await session.scalar(select(VideoProject).where(VideoProject.slug == video_slug))
    if project is not None:
        project.series_slug = series.slug
        project.episode_number = number
    await session.commit()
    return SeriesEpisodeStartOut(
        request=request_view(request, series_slug=series.slug),
        episode=episode_view(episode),
        context=await context_view(session, series, number),
    )


async def recap_episode(
    session: AsyncSession, slug: str, number: int, payload: SeriesEpisodeRecapIn
) -> SeriesEpisodeOut:
    series = await _series(session, slug, lock=True)
    episode = await _episode(session, series, number)
    if episode.status not in ("started", "done"):
        raise SeriesRefused(409, "video_series_episode_not_started", "這一集還沒開始做")
    episode.recap = payload.recap
    episode.state_json = payload.state
    episode.updated_at = _now()
    await session.commit()
    return episode_view(episode)


def finish_if_complete(
    series: VideoDramaSeries, episodes: list[VideoDramaEpisode], now: datetime
) -> bool:
    """Mark the series finished once every planned episode is done or skipped; true if it did."""
    if series.status != "active":
        return False
    if len(episodes) < series.planned_episodes or not all(
        e.status in ("done", "skipped") for e in episodes
    ):
        return False
    series.status = "finished"
    series.updated_at = now
    return True


async def finish_episode(session: AsyncSession, slug: str, number: int) -> SeriesEpisodeOut:
    """The worker reports the episode is cleared for upload: the next one may start."""
    series = await _series(session, slug, lock=True)
    episode = await _episode(session, series, number)
    if episode.status != "started":
        raise SeriesRefused(409, "video_series_episode_not_started", "這一集還沒開始做")
    now = _now()
    episode.status = "done"
    episode.finished_at = now
    episode.updated_at = now
    if episode.request_id is not None:
        request = await session.get(VideoDramaRequest, episode.request_id)
        if request is not None and request.status == "started":
            request.status = "done"
            request.finished_at = now
            request.updated_at = now
    finish_if_complete(series, await _episodes(session, series), now)
    series.updated_at = now
    await session.commit()
    return episode_view(episode)


async def start_compilation(
    session: AsyncSession, token: VideoToolToken, slug: str, video_slug: str
) -> SeriesCompilationStartOut:
    """The worker starts the compilation of a finished series under the video's slug
    (docs/videos/BINGE.md); the episodes come back in play order."""
    _ = token
    series = await _series(session, slug, lock=True)
    if series.status != "finished" or not series.compilation:
        raise SeriesRefused(409, "video_series_not_finished", "每一集都完成之後才能做合集")
    if series.compilation_slug is not None:
        raise SeriesRefused(409, "video_series_compiling", "合集已經開始做")
    taken = await session.scalar(
        select(VideoDramaRequest.id).where(VideoDramaRequest.slug == video_slug)
    )
    project = await session.scalar(select(VideoProject).where(VideoProject.slug == video_slug))
    if taken is not None or project is not None:
        raise SeriesRefused(409, "video_drama_request_slug_taken", f"{video_slug} 已經是另一支影片")
    now = _now()
    series.compilation_slug = video_slug
    series.compilation_started_at = now
    series.compilation_finished_at = None
    series.updated_at = now
    await session.commit()
    episodes = [e for e in await _episodes(session, series) if e.status == "done" and e.slug]
    docs = await _docs(session, series)
    return SeriesCompilationStartOut(
        series=summary_view(series, docs, await _episodes(session, series)),
        episodes=[episode_view(episode) for episode in episodes],
        context=await context_view(session, series, None),
    )


async def finish_compilation(session: AsyncSession, slug: str) -> SeriesSummary:
    """The worker reports the compilation is cleared for upload."""
    series = await _series(session, slug, lock=True)
    if series.compilation_slug is None:
        raise SeriesRefused(409, "video_series_not_compiling", "這部作品沒有在做合集")
    now = _now()
    series.compilation_finished_at = now
    series.updated_at = now
    await session.commit()
    return summary_view(series, await _docs(session, series), await _episodes(session, series))


def binge_quote(
    settings: VideoAutomationSettings, total_minutes: int, episode_minutes: int, visual_tier: str
) -> BingeQuoteOut:
    """What one binge series takes at the settings' prices, against the month's budgets.

    Pure so the form can ask before the owner presses the button; the numbers are the
    estimate of docs/videos/DRAMA.md scaled by the tier's clip share, with the sheets once.
    """
    planned, per_chapter = binge_shape(total_minutes, episode_minutes)
    share = TIER_CLIP_SHARE.get(visual_tier, 1.0)
    shots = planned * episode_minutes * SHOTS_PER_MINUTE
    clip_shots = round(shots * share)
    clip_seconds = round(clip_shots * SHOT_SECONDS * RETAKE_FACTOR)
    images = round(shots * KEYFRAME_TAKES) + SHEET_IMAGES
    judge_calls = shots + clip_shots + SHEET_IMAGES
    clip_model = find_model(cast(Any, settings.clip_provider), "clip", settings.clip_model)
    image_model = find_model(cast(Any, settings.image_provider), "image", settings.image_model)
    clip_price = clip_model.usd_per_second if clip_model and clip_model.usd_per_second else 0.15
    image_price = image_model.usd_per_image if image_model and image_model.usd_per_image else 0.134
    usd = clip_seconds * clip_price + images * image_price + judge_calls * JUDGE_USD_PER_CALL
    usd += planned * 1.0  # narration, music and captions, well under a dollar an episode
    budgets = {
        "clip_seconds": BudgetLine(
            needed=clip_seconds,
            monthly=settings.monthly_clip_seconds_budget,
            ok=clip_seconds <= settings.monthly_clip_seconds_budget,
        ),
        "images": BudgetLine(
            needed=images,
            monthly=settings.monthly_images_budget,
            ok=images <= settings.monthly_images_budget,
        ),
        "judge_calls": BudgetLine(
            needed=judge_calls,
            monthly=settings.monthly_judge_calls_budget,
            ok=judge_calls <= settings.monthly_judge_calls_budget,
        ),
        "episodes_per_month": BudgetLine(
            needed=planned,
            monthly=settings.series_episodes_per_month,
            ok=planned <= settings.series_episodes_per_month,
        ),
    }
    return BingeQuoteOut(
        episodes=planned,
        chapters=chapter_count(planned, per_chapter),
        episodes_per_chapter=per_chapter,
        clip_seconds=clip_seconds,
        images=images,
        judge_calls=judge_calls,
        usd=round(usd, 2),
        budgets=budgets,
        ok=all(line.ok for line in budgets.values()),
    )


def month_days(now: datetime | None = None) -> int:
    """How many days this month has; the tab shows the month's episode pace against the cap."""
    when = now or _now()
    return calendar.monthrange(when.year, when.month)[1]
