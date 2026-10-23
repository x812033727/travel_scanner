"""What /admin/videos does: the pipeline reports and submits, the owner decides.

A review is bound to the SHA-256 of what it shows (the brief, the timeline, the final cut, the
upload package). Submitting different content for the same gate supersedes the pending review;
submitting the same content again returns the review that exists, whatever its state, so a
rejected cut cannot come back as a fresh pending one without changing. Shorts final reviews
also bind the complete QA receipt; changed evidence creates a new review revision before
upload, and its publish review must name that approved final review. Files no live or decided
review refers to are deleted from the store. A video the owner dropped takes no more
submissions or decisions.

Once the owner has uploaded a video themselves and pasted its YouTube address (HANDS-OFF.md
§上傳包與「可以上架」), the row carries ``youtube_video_id`` and ``youtube_publish_at``; the
review files stay downloadable, and ``prune_published_previews`` deletes only the mp4 once the
upload confirmation and the publish time are both at least PREVIEW_RETENTION old. The publish
time is the owner's when they typed one; otherwise it is what the linked channel reports for
the video through videos.list (``youtube_publication``), so a video the owner made public in
Studio reaches the public library (public_api.py) without a second form. A video that is still
private or unlisted, with no scheduled time, keeps no publish time and stays unlisted on the
site; ``backfill_youtube_publish_times`` asks the same question for every linked video that
has none yet.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import re
from collections.abc import AsyncIterator, Iterable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit
from uuid import uuid4

import httpx
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoToolToken
from app.problems import AppError
from app.video_automation.anime_policy import (
    BODY_TOLERANCE_SECONDS,
    LONG_ANIME_POLICY,
    AnimeRuntimeSpec,
    is_long_anime,
)
from app.video_automation.judge import (
    PACKAGE_AUTO_APPROVED_NOTE,
    QA_AUTO_APPROVED_NOTE,
    QA_ITEMS,
    SCRIPT_AUTO_APPROVED_NOTE,
    SHORTS_PACKAGE_AUTO_APPROVED_NOTE,
    SHORTS_QA_AUTO_APPROVED_NOTE,
    demo_asked_of,
    pick_choice,
    pick_reason,
    video_series_kind,
)
from app.video_automation.models import (
    VideoAutomationSettings,
    VideoDramaEpisode,
    VideoDramaRequest,
    VideoDramaSeries,
)
from app.video_automation.settings import (
    AUTO_APPROVED_NOTE,
    AUTO_APPROVED_STORYBOARD_NOTE,
    auto_approves_audio,
    auto_approves_final,
    auto_approves_script,
    auto_approves_storyboard,
    auto_picks_look,
    auto_picks_outline,
    look_pick_note,
)
from app.video_media.meter import SlugSpend, spend_by_slug
from app.video_reviews import dub_retry
from app.video_reviews.producer_state import worker_view
from app.video_reviews.schemas import (
    BROWSE_STATES,
    DUB_LOCALES,
    LOCALE_PARTS,
    VIDEO_CATEGORY_CODES,
    WORKER_CAPTION_LOCALES,
    YOUTUBE_VIDEO_ID_PATTERN,
    CategoryIn,
    DecisionIn,
    DropIn,
    DubLocale,
    DubLocalesIn,
    DubRetryBlocker,
    DubRetryOut,
    FacetCount,
    FinalRenewalIn,
    FinalRenewalState,
    LanguagePartOut,
    LocaleChoice,
    LocalesIn,
    ProjectFacets,
    ProjectIn,
    ProjectOut,
    ProjectPage,
    ProjectSummary,
    ReviewFile,
    ReviewIn,
    ReviewOut,
    WorkerState,
    without_retired_locales,
)
from app.video_reviews.storage import ReviewStore, StorageRefused, valid_slug
from app.video_shorts import costs as shorts_costs
from app.video_shorts import slots as shorts_slots
from app.video_shorts.claim import duration_seconds
from app.video_shorts.settings import auto_approves_shorts
from app.video_youtube import connection
from app.video_youtube.client import YoutubeClient, YoutubeError
from app.video_youtube.errors import Refused
from app.video_youtube.requests import as_dict
from app.video_youtube.state import parse_time, public_state
from app.video_youtube.state import running as youtube_sync_running

LIVE = ("pending", "approved", "rejected")
# The list's cap, and how many public Shorts the Shorts tab gets at once: the public ones
# only grow, and the older ones are read from the numbers instead (docs/videos/SHORTS.md).
LIST_LIMIT = 200
PUBLIC_SHORTS_LIMIT = 60
# The review tab's catalog (browse_projects): a page of tutorials, the most a page may hold,
# and the longest search the owner can type.
BROWSE_PAGE_SIZE = 30
BROWSE_PAGE_LIMIT = 100
BROWSE_QUERY_MAX = 80
# How long the mp4 of a video that is on YouTube stays in the review store, counted from the
# later of the upload confirmation's decision and the publish time (HANDS-OFF.md). The
# thumbnail, captions and descriptions are small and stay.
PREVIEW_RETENTION = timedelta(days=7)
YOUTUBE_ID = re.compile(YOUTUBE_VIDEO_ID_PATTERN)
YOUTUBE_HOSTS = frozenset(
    {"youtu.be", "youtube.com", "www.youtube.com", "m.youtube.com", "studio.youtube.com"}
)
# youtube.com/<kind>/<id>: shorts, embeds and live pages, and Studio's /video/<id>/edit.
YOUTUBE_PATH_KINDS = frozenset({"shorts", "embed", "live", "video", "v"})
# Gates where approving means choosing one of the offered options (an outline; a character sheet).
CHOICE_GATES = ("outline", "look")
CHOICE_PROMPTS = {"outline": "請從 {} 選一個大綱", "look": "請從 {} 選一張角色設定圖"}
# A languages batch with nothing for the owner to upload is approved as it arrives.
LANGUAGES_AUTO_APPROVED_NOTE = "這一批沒有要你上傳的配音，依規則自動核准"
# A narrator-only explainer may use the existing drama dub path. A brand story needs additional
# proof from its current approved final cut that zh-TW is switchable CC, checked separately below.
# The dub tool still refuses a script with speaking characters.
DUBBABLE_DRAMA_CATEGORIES = frozenset({"explainer"})
EPOCH = datetime.min.replace(tzinfo=UTC)
ANIME_RUNTIME_KEYS = (
    "body_target_seconds",
    "op_ed_budget_seconds",
    "broadcast_slot_seconds",
    "slot_reserve_seconds",
)
ANIME_CONTEXT_KEYS = (
    "slug",
    "episode",
    "chapter",
    "planned_episodes",
    "open_ended",
    "closed_ending",
    "kind",
    "genre",
    "lead",
)


def _same_anime_context(raw: Any, context: dict[str, Any]) -> bool:
    return (
        isinstance(raw, dict)
        and raw.keys() == context.keys()
        and all(
            type(raw[key]) is type(value) and raw[key] == value for key, value in context.items()
        )
    )


def _same_anime_runtime(raw: Any, runtime: dict[str, Any]) -> bool:
    try:
        return AnimeRuntimeSpec.model_validate(raw).model_dump() == runtime
    except ValueError:
        return False


def anime_review_problem(
    gate: str,
    payload: dict[str, Any],
    content_sha256: str,
    series: VideoDramaSeries | None,
    episode: VideoDramaEpisode | None,
) -> str | None:
    """A runtime declaration must agree with the server's episode, even for manual approval."""
    if gate not in ("script", "audio", "final", "publish"):
        return None
    declared = (
        payload.get("production_policy") is not None or payload.get("runtime_spec") is not None
    )
    if series is None or not is_long_anime(series):
        return "動漫製作規格與影片所屬企劃不符" if declared else None
    if episode is None or payload.get("production_policy") != LONG_ANIME_POLICY:
        return "缺少影片所屬的長篇動漫製作規格或集數"
    if not isinstance(episode.beats, dict) or type(episode.beats.get("closed_ending")) is not bool:
        return "集數的終局設定無效，請重新審核章綱"
    try:
        runtime = AnimeRuntimeSpec.model_validate(series.runtime_spec).model_dump()
    except ValueError:
        return "企劃的動漫時長規格無效"
    context: dict[str, Any] = {
        "slug": series.slug,
        "episode": episode.number,
        "chapter": episode.chapter_number,
        "planned_episodes": series.planned_episodes,
        "open_ended": series.open_ended,
        "closed_ending": episode.beats["closed_ending"],
        "kind": series.kind,
        "genre": series.genre,
        "lead": series.lead,
    }
    # Canonical byte shape matches tools/video/core/anime-policy.mjs, including booleans.
    canonical = [
        LONG_ANIME_POLICY,
        [[key, runtime[key]] for key in ANIME_RUNTIME_KEYS],
        series.category,
        series.style_preset,
        [[key, context[key]] for key in ANIME_CONTEXT_KEYS],
    ]
    policy_hash = hashlib.sha256(
        json.dumps(canonical, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()
    if (
        not _same_anime_runtime(payload.get("runtime_spec"), runtime)
        or not _same_anime_context(payload.get("runtime_context"), context)
        or payload.get("runtime_policy_hash") != policy_hash
    ):
        return "時長審核已過期或不屬於這一集，請重新提交"
    if gate not in ("final", "publish"):
        return None
    proof = payload.get("runtime_proof")
    if not isinstance(proof, dict):
        return "成片缺少實際量測的動漫時長證明"
    final_sha = content_sha256 if gate == "final" else payload.get("final_media_sha256")
    if (
        proof.get("basis") != "measured"
        or proof.get("production_policy") != LONG_ANIME_POLICY
        or not _same_anime_runtime(proof.get("runtime_spec"), runtime)
        or not _same_anime_context(proof.get("runtime_context"), context)
        or proof.get("policy_hash") != policy_hash
        or not isinstance(final_sha, str)
        or not re.fullmatch(r"[0-9a-f]{64}", final_sha)
        or proof.get("final_sha256") != final_sha
        or not isinstance(proof.get("speech_hash"), str)
        or not re.fullmatch(r"[0-9a-f]{16}", proof["speech_hash"])
        or type(proof.get("fps")) is not int
        or proof["fps"] != 30
    ):
        return "成片的時長證明與目前規格或檔案不符"
    for part in ("body", "op_ed", "presentation"):
        frames, seconds = proof.get(f"{part}_frames"), proof.get(f"{part}_seconds")
        if (
            type(frames) is not int
            or frames < 0
            or frames > runtime["broadcast_slot_seconds"] * 30
            or type(seconds) not in (int, float)
            or seconds != frames / 30
        ):
            return "時長證明必須記錄實際影格與秒數"
    body, op_ed, presentation = (
        proof["body_frames"],
        proof["op_ed_frames"],
        proof["presentation_frames"],
    )
    if (
        presentation != body + op_ed
        or not (runtime["body_target_seconds"] - BODY_TOLERANCE_SECONDS) * 30
        <= body
        <= (runtime["body_target_seconds"] + BODY_TOLERANCE_SECONDS) * 30
        or op_ed > runtime["op_ed_budget_seconds"] * 30
        or presentation > (runtime["broadcast_slot_seconds"] - runtime["slot_reserve_seconds"]) * 30
    ):
        return "正文、OP／ED 或成片時長超出這一集的規格"
    if gate == "final":
        report = payload.get("qa") or payload.get("manual_review_qa")
        if (
            not isinstance(report, dict)
            or report.get("final_sha256") != final_sha
            or report.get("policy_hash") != policy_hash
            or not _same_anime_runtime(report.get("runtime_spec"), runtime)
            or not _same_anime_context(report.get("runtime_context"), context)
        ):
            return "成片品管報告缺少目前檔案與時長規格的綁定"
    return None


async def _check_anime_review(
    session: AsyncSession,
    project: VideoProject,
    gate: str,
    payload: dict[str, Any],
    content_sha256: str,
) -> bool:
    # The worker may update the project's labels. The server-created episode is authority.
    row = await session.scalar(
        select(VideoDramaSeries)
        .join(VideoDramaEpisode, VideoDramaEpisode.series_id == VideoDramaSeries.id)
        .where(VideoDramaEpisode.slug == project.slug)
    )
    series = row if isinstance(row, VideoDramaSeries) else None
    if series is None and project.series_slug is not None:
        row = await session.scalar(
            select(VideoDramaSeries).where(VideoDramaSeries.slug == project.series_slug)
        )
        series = row if isinstance(row, VideoDramaSeries) else None
    episode = None
    if (
        series is not None
        and is_long_anime(series)
        and gate in ("script", "audio", "final", "publish")
    ):
        if project.series_slug != series.slug:
            raise AppError(
                409, "video_anime_runtime_invalid", "影片的系列標記與正式動漫集數不符"
            )
        episode = await session.scalar(
            select(VideoDramaEpisode).where(
                VideoDramaEpisode.series_id == series.id,
                VideoDramaEpisode.number == project.episode_number,
                VideoDramaEpisode.slug == project.slug,
            )
        )
        if not isinstance(episode, VideoDramaEpisode):
            episode = None
    problem = anime_review_problem(gate, payload, content_sha256, series, episode)
    if problem:
        raise AppError(409, "video_anime_runtime_invalid", problem)
    if series is not None and is_long_anime(series) and gate == "publish":
        final = _current_final(await _reviews(session, project, refresh=True))
        if (
            final is None
            or final.status != "approved"
            or final.content_sha256 != payload.get("final_media_sha256")
            or anime_review_problem("final", final.payload, final.content_sha256, series, episode)
            or final.payload.get("runtime_proof") != payload.get("runtime_proof")
        ):
            raise AppError(
                409,
                "video_anime_final_review_stale",
                "上傳包必須綁定目前已核准的動漫成片與時長證明，請重新提交",
            )
    return series is not None and is_long_anime(series)


def review_store(settings: Settings) -> ReviewStore:
    return ReviewStore(
        settings.video_review_dir,
        max_file_bytes=settings.video_review_max_file_bytes,
        max_total_bytes=settings.video_review_max_total_bytes,
    )


def outline_choices(payload: dict[str, Any]) -> list[str]:
    """The option keys an outline review offers (A, B, C), from its payload."""
    options = payload.get("options")
    if not isinstance(options, list):
        return []
    return [str(item["key"]) for item in options if isinstance(item, dict) and item.get("key")]


def decision_problem(review: VideoReview, decision: DecisionIn) -> str | None:
    """Why this decision cannot be recorded, or None."""
    if review.status != "pending":
        return "這一項已經決定過或被新版本取代"
    if decision.decision == "reject" and not (decision.note or "").strip():
        return "退回時請寫下原因，工具會把它帶回給撰稿與查核"
    choices = outline_choices(review.payload) if review.gate in CHOICE_GATES else []
    if decision.decision == "approve" and choices and decision.choice not in choices:
        return CHOICE_PROMPTS[review.gate].format("、".join(choices))
    return None


def locale_choices(project: VideoProject) -> dict[str, LocaleChoice]:
    """The owner's language choice as stored (docs/videos/LANGUAGES.md), empty for a shape no
    page wrote. A language the video is no longer made in (zh-CN, chosen before 2026-10-09) is
    left out, not an error: the other languages keep working."""
    raw = without_retired_locales(project.locales if isinstance(project.locales, dict) else {})
    try:
        chosen = LocalesIn.model_validate({"locales": raw}).locales
    except ValueError:
        return {}
    return {str(locale): choice for locale, choice in chosen.items()}


def locale_options(project: VideoProject) -> list[DubLocale]:
    """The languages the panel offers this video (docs/videos/LANGUAGES.md): all eight, for
    every category and an imported video alike, since 2026-10-20 the worker makes titles,
    descriptions and captions in each (WORKER_CAPTION_LOCALES), and since 2026-10-20 dubs
    them too (WORKER_DUB_LOCALES). What of a language may be chosen is ``_apply_locales``'s
    rule: no dub on a drama whose characters speak."""
    _ = project
    return list(WORKER_CAPTION_LOCALES)


def _part_state(value: Any) -> tuple[str | None, str | None]:
    """A part as a languages review reports it: "ready" or {"status": "skipped", "reason"}."""
    if isinstance(value, str):
        return value, None
    if isinstance(value, dict):
        status = value.get("status")
        reason = value.get("reason")
        return (status if isinstance(status, str) else None), (
            reason if isinstance(reason, str) else None
        )
    return None, None


def _dub_file_sha(review: VideoReview, locale: str, parts: dict[str, Any]) -> str | None:
    """The SHA-256 of the dub track a languages batch attaches for this locale, or None: the
    file under the role the entry names, or under the role review-push gives a dub."""
    named = parts.get("file_role")
    role = named if isinstance(named, str) else f"dub_{locale.lower().replace('-', '_')}"
    for item in review.files or []:
        if isinstance(item, dict) and item.get("role") == role:
            sha = item.get("sha256")
            return sha if isinstance(sha, str) and sha else None
    return None


def language_states(
    choices: dict[str, LocaleChoice],
    reviews: Iterable[VideoReview],
    retries: dict[str, Any] | None = None,
) -> dict[str, dict[str, LanguagePartOut]]:
    """Where each chosen part stands, from the languages reviews (docs/videos/LANGUAGES.md).

    The batches are read oldest first, so a later batch (the languages added after the first)
    speaks last for the parts it names and leaves the rest as they were. A part a batch reports
    "ready" or "skipped" (with the worker's reason) is that; a dub track "ready" in an approved
    batch is "uploaded", since approving the batch is how the owner says they uploaded it;
    a chosen part no batch has reported is "working". Sent-back batches count for nothing.

    A track the owner already confirmed stays "uploaded" when a later pending batch restates
    the same file: every batch lists every chosen language again, so after one dub is made
    again the others would otherwise fall back to "ready" although nothing of theirs is new.

    ``retries`` is the video's ``dub_retries`` (docs/videos/DUBS.md §再做一次). A chosen dub
    whose request the worker took reads "working" until its batch or the worker's refusal
    ends the request; a request that is only asked changes nothing here.
    """
    states: dict[str, dict[str, LanguagePartOut]] = {
        locale: {part: LanguagePartOut(state="working") for part in choice.chosen()}
        for locale, choice in choices.items()
    }
    batches = sorted(
        (
            review
            for review in reviews
            if review.gate == "languages" and review.status in ("pending", "approved")
        ),
        key=lambda review: review.created_at or EPOCH,
    )
    confirmed: dict[str, set[str]] = {}
    for review in batches:
        reported = review.payload.get("locales") if isinstance(review.payload, dict) else None
        if not isinstance(reported, dict):
            continue
        for locale, parts in reported.items():
            if locale not in states or not isinstance(parts, dict):
                continue
            fallback = parts.get("reason") if isinstance(parts.get("reason"), str) else None
            for part in LOCALE_PARTS:
                if part not in states[locale] or part not in parts:
                    continue
                state, reason = _part_state(parts[part])
                if state not in ("ready", "skipped"):
                    continue
                if state == "ready" and part == "dub":
                    track = _dub_file_sha(review, locale, parts)
                    if review.status == "approved":
                        state = "uploaded"
                        if track is not None:
                            confirmed.setdefault(locale, set()).add(track)
                    elif track is not None and track in confirmed.get(locale, ()):
                        state = "uploaded"
                states[locale][part] = LanguagePartOut(
                    state=state, reason=(reason or fallback) if state == "skipped" else None
                )
    if isinstance(retries, dict):
        for locale, entry in retries.items():
            if "dub" in states.get(locale, {}) and dub_retry.reads_working(entry):
                states[locale]["dub"] = LanguagePartOut(state="working")
    return states


def _batch_dubs(payload: dict[str, Any]) -> dict[str, tuple[str | None, str | None]]:
    """What a languages batch says of each locale's dub: its state and, for a skip, the reason
    (the entry's own, or the older shape's beside the parts). A locale whose entry does not name
    the dub is left out."""
    reported = payload.get("locales") if isinstance(payload, dict) else None
    if not isinstance(reported, dict):
        return {}
    dubs: dict[str, tuple[str | None, str | None]] = {}
    for locale, parts in reported.items():
        if not isinstance(parts, dict) or "dub" not in parts:
            continue
        fallback = parts.get("reason") if isinstance(parts.get("reason"), str) else None
        state, reason = _part_state(parts["dub"])
        dubs[str(locale)] = (state, reason or fallback)
    return dubs


def languages_need_owner(payload: dict[str, Any]) -> bool:
    """Whether a languages batch carries a dub track, the one part only the owner can upload."""
    reported = payload.get("locales") if isinstance(payload, dict) else None
    if not isinstance(reported, dict):
        return False
    return any(
        _part_state(parts.get("dub"))[0] == "ready"
        for parts in reported.values()
        if isinstance(parts, dict)
    )


def ready_to_upload(
    project: VideoProject,
    publish_approved_at: datetime | None,
    languages: dict[str, dict[str, LanguagePartOut]],
) -> bool:
    """Whether the video may be scheduled (docs/videos/LANGUAGES.md §上架流程): its upload
    confirmation approved, its languages decided and every chosen part ready, skipped or
    uploaded, no YouTube id yet, and not dropped."""
    if project.dropped_at is not None or project.youtube_video_id is not None:
        return False
    if publish_approved_at is None or project.locales_decided_at is None:
        return False
    return all(part.state != "working" for parts in languages.values() for part in parts.values())


def kept_files(reviews: Iterable[VideoReview]) -> set[str]:
    """Keep live previews and evidence for historical decisions, not abandoned drafts."""
    rows = list(reviews)
    # Explicit owner renewals preserve even the undecided version they replaced. The
    # references live on the new review so the original evidence is never rewritten.
    retained: set[str] = set()
    for row in rows:
        renewal = (row.payload or {}).get(RENEWAL_KEY)
        ids = renewal.get("retained_review_ids") if isinstance(renewal, dict) else None
        if isinstance(ids, list):
            retained.update(item for item in ids if isinstance(item, str))
    return {
        str(item["sha256"])
        for review in rows
        if review.status in LIVE or review.decided_at is not None or str(review.id) in retained
        for item in review.files
        if isinstance(item, dict) and item.get("sha256")
    }


def _review_out(review: VideoReview) -> ReviewOut:
    return ReviewOut(
        id=review.id,
        gate=review.gate,
        subject=review.subject,
        content_sha256=review.content_sha256,
        summary=review.summary,
        payload=review.payload,
        files=[ReviewFile.model_validate(item) for item in review.files],
        status=review.status,
        choice=review.choice,
        note=review.note,
        decided_at=review.decided_at,
        created_at=review.created_at,
    )


def _summary(
    project: VideoProject,
    pending: int,
    spend: SlugSpend | None = None,
    publish_approved_at: datetime | None = None,
    languages: dict[str, dict[str, LanguagePartOut]] | None = None,
    *,
    compilation: bool = False,
    download_available: bool = False,
    hold: shorts_slots.Hold | None = None,
    producer: WorkerState | None = None,
    tidied_at: str | None = None,
    publish_usable: bool | None = None,
) -> dict[str, Any]:
    choices = locale_choices(project)
    stored_retries = project.dub_retries or {}
    states = (
        languages if languages is not None else language_states(choices, [], stored_retries)
    )
    is_short = project.shorts_line is not None
    # The owner's requests to make a skipped dub again, and why one cannot be asked for now
    # (docs/videos/DUBS.md §再做一次). A Short has no language panel, so neither. Without the
    # video's publish reviews (the lists do not load them) "a batch could be used" is read from
    # what the row knows: an upload confirmation was approved, or the video is on YouTube.
    retries: dict[str, DubRetryOut] = {}
    retry_blocked: dict[str, DubRetryBlocker] = {}
    if not is_short:
        usable = (
            publish_usable
            if publish_usable is not None
            else (publish_approved_at is not None or project.youtube_video_id is not None)
        )
        retries = dub_retry.views(
            stored_retries,
            [locale for locale, choice in choices.items() if choice.dub],
            datetime.now(UTC),
        )
        for locale, parts in states.items():
            dub = parts.get("dub")
            asked = retries.get(locale)
            if dub is None or dub.state != "skipped" or (asked is not None and asked.open):
                continue
            code = dub_retry.blocker(
                reason=dub.reason,
                tidied_at=tidied_at,
                producer=producer,
                stage=project.stage,
                publish_usable=usable,
            )
            if code is not None:
                retry_blocked[locale] = code
    return {
        "dub_retries": retries,
        "dub_retry_blocked": retry_blocked,
        "shorts_line": project.shorts_line,
        "shorts_series": project.shorts_series,
        "source_slug": project.source_slug,
        "shorts_state": (
            shorts_slots.state_of(project, pending, publish_approved_at, hold)
            if is_short
            else None
        ),
        "slot_at": hold.starts_at if is_short and hold is not None else None,
        "youtube_removed_at": project.youtube_removed_at,
        "compilation": compilation,
        "download_available": download_available,
        "slug": project.slug,
        "title": project.title,
        "format": project.format or "slides",
        "stage": project.stage,
        "checklist": project.checklist,
        "youtube_video_id": project.youtube_video_id,
        "youtube_publish_at": project.youtube_publish_at,
        "publish_approved_at": publish_approved_at,
        "last_synced_at": project.last_synced_at,
        "pending": pending,
        "source_guide": project.source_guide,
        "category": project.category,
        "dropped_at": project.dropped_at,
        "dropped_note": project.dropped_note,
        "retry_request_id": project.retry_request_id,
        "retry_acknowledged_id": project.retry_acknowledged_id,
        "media_usd": spend.usd if spend else 0.0,
        "clip_seconds": spend.clip_seconds if spend else 0,
        "locales": choices,
        "locale_options": locale_options(project),
        "locales_decided_at": project.locales_decided_at,
        "languages": states,
        "worker_state": None if is_short else producer,
        # A Short's languages are the Shorts settings', not a choice made video by video, so
        # it waits for no decision on the language panel.
        "ready_to_upload": (
            publish_approved_at is not None
            and project.youtube_video_id is None
            and project.dropped_at is None
            if is_short
            else ready_to_upload(project, publish_approved_at, states)
        ),
        "dub_locales": [locale for locale, choice in choices.items() if choice.dub],
        "series_slug": project.series_slug,
        "episode_number": project.episode_number,
        "youtube_sync": public_state(project.youtube_sync),
    }


async def _project(session: AsyncSession, slug: str, *, lock: bool = False) -> VideoProject:
    statement = select(VideoProject).where(VideoProject.slug == slug)
    if lock:
        statement = statement.with_for_update().execution_options(populate_existing=True)
    project: VideoProject | None = (
        await session.scalar(statement)
        if valid_slug(slug)
        else None
    )
    if project is None:
        raise AppError(404, "video_project_not_found", "找不到這支影片")
    return project


def _refuse_dropped(project: VideoProject) -> None:
    if project.dropped_at is not None:
        raise AppError(409, "video_project_dropped", "站主已經放棄這支影片")


async def _reviews(
    session: AsyncSession, project: VideoProject, *, refresh: bool = False
) -> list[VideoReview]:
    statement = (
        select(VideoReview)
        .where(VideoReview.project_id == project.id)
        .order_by(VideoReview.created_at.desc())
    )
    if refresh:
        statement = statement.execution_options(populate_existing=True)
    rows = await session.scalars(statement)
    return list(rows)


def _apply_dub_retry(
    session: AsyncSession, project: VideoProject, applied: dub_retry.Applied
) -> None:
    """Store what a report or a batch did to the dub retry requests, one audit row per
    transition. Every change dub_retry makes comes with an event, so no event means nothing to
    write. The caller holds the project's row lock and commits."""
    if not applied.events:
        return
    project.dub_retries = applied.retries
    for event in applied.events:
        session.add(
            AdminAuditLog(
                actor_user_id=None,
                action=event.action,
                target=f"video_project:{project.id}",
                metadata_json={"slug": project.slug, **event.details},
            )
        )


async def upsert_project(
    session: AsyncSession, store: ReviewStore, slug: str, payload: ProjectIn
) -> ProjectOut:
    if not valid_slug(slug):
        raise AppError(422, "video_review_bad_slug", "影片代號只能用小寫英文、數字與連字號")
    now = datetime.now(UTC)
    project = await session.scalar(
        select(VideoProject).where(VideoProject.slug == slug).with_for_update()
    )
    if project is None:
        project = VideoProject(slug=slug, created_at=now)
        session.add(project)
    project.title = payload.title
    project.stage = payload.stage
    project.checklist = [item.model_dump() for item in payload.checklist]
    # The owner records the id on /admin/videos first; a report that does not carry it yet
    # (the worker reads it back a round later) must not clear it.
    if payload.youtube_video_id is not None:
        project.youtube_video_id = payload.youtube_video_id
    if payload.source_guide is not None:
        project.source_guide = payload.source_guide
    # A report files a video nobody filed yet; the owner's choice on the page sticks.
    if payload.category is not None and project.category is None:
        project.category = payload.category
    if payload.format is not None:
        project.format = payload.format
    if payload.series_slug is not None:
        project.series_slug = payload.series_slug
    if payload.episode_number is not None:
        project.episode_number = payload.episode_number
    if payload.shorts_line is not None:
        project.shorts_line = payload.shorts_line
    if payload.shorts_series is not None:
        project.shorts_series = payload.shorts_series
    if payload.source_slug is not None:
        project.source_slug = payload.source_slug
    # The card pipeline only makes Shorts, and the lists tell a Short by its content line: a
    # row in that format without one would show among the tutorials.
    if project.format == "shorts" and project.shorts_line is None:
        raise AppError(
            422,
            "video_shorts_line_missing",
            "Shorts 要帶內容線（shorts_line：lab、cut 或 drama）",
        )
    # A stale or unrelated report cannot consume a newer retry request.
    if payload.retry_acknowledged_id == project.retry_request_id:
        project.retry_acknowledged_id = payload.retry_acknowledged_id
    # A story cut can change between the worker's readiness read and this report. Never
    # acknowledge a paid retry take after its exact switchable-CC final becomes ineligible.
    retry_report = payload.dub_retries
    if (
        isinstance(retry_report, dict)
        and any(
            isinstance(item, dict) and item.get("status") == "taken"
            for item in retry_report.values()
        )
        and project.format == "drama"
        and (project.category == "story" or await video_series_kind(session, slug) == "story")
        and not _story_dub_ready(await _reviews(session, project))
    ):
        retry_report = {
            locale: item for locale, item in retry_report.items()
            if not (isinstance(item, dict) and item.get("status") == "taken")
        }
    # Only the request the worker names by id moves; the answer says what the site accepted.
    _apply_dub_retry(
        session,
        project,
        dub_retry.apply_worker(project.dub_retries or {}, retry_report, now),
    )
    project.last_synced_at = now
    project.updated_at = now
    current = _current_final(await _reviews(session, project)) if project.id else None
    if (
        current is not None and RENEWAL_KEY in (current.payload or {})
        and current.status != "approved"
    ):
        _hold_final_review(project)
    await _decide_story_locales(session, project, now)
    await session.commit()
    # A video on YouTube keeps its upload package for the owner to download; only the mp4 goes,
    # and only after PREVIEW_RETENTION (prune_published_previews), so nothing is deleted here
    # and the store is not touched.
    return await project_view(session, slug)


def publish_approved_at(reviews: Iterable[VideoReview]) -> datetime | None:
    """When the upload confirmation was last approved, or None while it was not."""
    decided = [
        review.decided_at
        for review in reviews
        if review.gate == "publish" and review.status == "approved" and review.decided_at
    ]
    return max(decided) if decided else None


def _confirmations() -> Any:
    """Per video, when its upload confirmation was last approved (a subquery)."""
    return (
        select(VideoReview.project_id, func.max(VideoReview.decided_at).label("decided_at"))
        .where(VideoReview.gate == "publish", VideoReview.status == "approved")
        .group_by(VideoReview.project_id)
        .subquery()
    )


async def project_view(session: AsyncSession, slug: str, work_dir: str | None = None) -> ProjectOut:
    project = await _project(session, slug)
    reviews = await _reviews(session, project)
    series_kind = (
        await video_series_kind(session, slug)
        if project.format == "drama" and project.shorts_line is None else None
    )
    pending = sum(1 for review in reviews if review.status == "pending")
    spend = await spend_by_slug(session, [project.slug])
    languages = language_states(locale_choices(project), reviews, project.dub_retries or {})
    compiled = work_dir is not None and slug in await compilation_slugs(session)
    held = await shorts_slots.holds(session, [slug]) if project.shorts_line is not None else {}
    # One bounded read of auto.json gives the registration and the tidy date.
    seen = worker_view(work_dir, slug) if project.shorts_line is None else None
    return ProjectOut(
        **_summary(
            project,
            pending,
            spend.get(project.slug),
            publish_approved_at(reviews),
            languages,
            compilation=compiled,
            download_available=compiled and download_file(work_dir, slug) is not None,
            hold=held.get(slug),
            producer=seen.state if seen is not None else None,
            tidied_at=seen.tidied_at if seen is not None else None,
            # The page has every review, so it reads the rule the producer binds a batch by;
            # the lists keep _summary's approximation.
            publish_usable=dub_retry.publish_usable(
                reviews, on_youtube=project.youtube_video_id is not None
            ),
        ),
        reviews=[_review_out(review) for review in reviews],
        dub_allowed=_dub_allowed(project, series_kind, reviews),
        story_dub_preselectable=_story_dub_preselectable(project, series_kind),
    )


async def _language_batches(
    session: AsyncSession, projects: list[VideoProject]
) -> dict[Any, list[VideoReview]]:
    """The languages reviews of these videos, by project id, for the list's states."""
    if not projects:
        return {}
    rows = await session.scalars(
        select(VideoReview).where(
            VideoReview.project_id.in_([project.id for project in projects]),
            VideoReview.gate == "languages",
            VideoReview.status.in_(("pending", "approved")),
        )
    )
    batches: dict[Any, list[VideoReview]] = {}
    for review in rows:
        batches.setdefault(review.project_id, []).append(review)
    return batches


async def compilation_slugs(session: AsyncSession) -> set[str]:
    """The slugs of every compilation video a binge series started (docs/videos/BINGE.md)."""
    rows = await session.scalars(
        select(VideoDramaSeries.compilation_slug).where(
            VideoDramaSeries.compilation_slug.is_not(None)
        )
    )
    return {str(slug) for slug in rows.all() if slug}


def download_file(work_dir: str | None, slug: str) -> Path | None:
    """Where a compilation's 1080p cut sits on the worker's volume, when the API can see it."""
    if not work_dir or not valid_slug(slug):
        return None
    root = Path(work_dir)
    file = root / slug / "upload" / "final.mp4"
    try:
        if not file.is_file() or not file.resolve().is_relative_to(root.resolve()):
            return None
    except OSError:
        return None
    return file


async def download_path(session: AsyncSession, work_dir: str | None, slug: str) -> Path:
    """The compilation cut the owner downloads from /admin/videos, or a 404 that says why."""
    project = await _project(session, slug)
    _refuse_dropped(project)
    if slug not in await compilation_slugs(session):
        raise AppError(404, "video_download_not_found", "只有合集的成片從這裡下載")
    file = download_file(work_dir, slug)
    if file is None:
        raise AppError(404, "video_download_not_found", "成片還不在工人的工作區，或 API 沒有掛載它")
    return file


def _is_public(now: datetime) -> Any:
    """A video whose publish time is past: what the Shorts tab counts as public."""
    return and_(
        VideoProject.youtube_video_id.is_not(None), VideoProject.youtube_publish_at <= now
    )


def _not_public(now: datetime) -> Any:
    return or_(
        VideoProject.youtube_video_id.is_(None),
        VideoProject.youtube_publish_at.is_(None),
        VideoProject.youtube_publish_at > now,
    )


async def list_projects(
    session: AsyncSession,
    *,
    video_format: str | None = None,
    series_slug: str | None = None,
    shorts: str | None = None,
    state: str | None = None,
    limit: int | None = None,
    before: datetime | None = None,
    work_dir: str | None = None,
) -> list[ProjectSummary]:
    """The videos, newest first; a format or a series narrows them (docs/videos/SERIES.md),
    so a hundred episodes do not push the tutorials past the cap. With the worker's work
    directory, a compilation says whether its cut is there to download.

    ``shorts`` keeps the Shorts apart (docs/videos/SHORTS.md): ``exclude`` is every list that
    existed before them, ``only`` is the Shorts tab and the worker's Shorts round. With
    ``only`` the Shorts still to deal with all come, and of the public ones the latest
    PUBLIC_SHORTS_LIMIT; ``state`` keeps one state, and ``limit`` and ``before`` page through
    it (``before`` is the publish time of the last public Short read, or the last report of
    any other).
    """
    now = datetime.now(UTC)
    statement = _listing_statement()
    if video_format is not None:
        statement = statement.where(VideoProject.format == video_format)
    if series_slug is not None:
        statement = statement.where(VideoProject.series_slug == series_slug)
    if shorts == "exclude":
        statement = statement.where(VideoProject.shorts_line.is_(None))
    elif shorts == "only":
        statement = statement.where(VideoProject.shorts_line.is_not(None))
    cap = limit or LIST_LIMIT
    if shorts != "only":
        if before is not None:
            statement = statement.where(VideoProject.last_synced_at < before)
        listed = list(
            (
                await session.execute(
                    statement.order_by(VideoProject.last_synced_at.desc()).limit(cap)
                )
            ).all()
        )
    else:
        listed = []
        if state in (None, "published"):
            public = statement.where(_is_public(now))
            if before is not None and state == "published":
                public = public.where(VideoProject.youtube_publish_at < before)
            listed += list(
                (
                    await session.execute(
                        public.order_by(VideoProject.youtube_publish_at.desc()).limit(
                            limit or PUBLIC_SHORTS_LIMIT
                        )
                    )
                ).all()
            )
        if state != "published":
            waiting = statement.where(_not_public(now))
            if before is not None and state is not None:
                waiting = waiting.where(VideoProject.last_synced_at < before)
            # Read whole and cut after the state is known: a state is not a column, and the
            # Shorts that are not public yet are a few dozen.
            listed = (
                list(
                    (
                        await session.execute(
                            waiting.order_by(VideoProject.last_synced_at.desc()).limit(LIST_LIMIT)
                        )
                    ).all()
                )
                + listed
            )
    summaries = await _summaries(session, listed, work_dir)
    if shorts == "only" and state is not None:
        summaries = [item for item in summaries if item.shorts_state == state][:cap]
    return summaries


def _listing_statement() -> Any:
    """Every video with its pending count and when its upload confirmation was approved."""
    pending = (
        select(VideoReview.project_id, func.count().label("pending"))
        .where(VideoReview.status == "pending")
        .group_by(VideoReview.project_id)
        .subquery()
    )
    confirmed = _confirmations()
    return (
        select(VideoProject, func.coalesce(pending.c.pending, 0), confirmed.c.decided_at)
        .outerjoin(pending, pending.c.project_id == VideoProject.id)
        .outerjoin(confirmed, confirmed.c.project_id == VideoProject.id)
    )


async def _summaries(
    session: AsyncSession, listed: list[Any], work_dir: str | None
) -> list[ProjectSummary]:
    """The rows of _listing_statement as the page's summaries, in the rows' order."""
    spend = await spend_by_slug(session, [project.slug for project, _count, _at in listed])
    batches = await _language_batches(session, [project for project, _count, _at in listed])
    compiled = await compilation_slugs(session) if work_dir is not None else set()
    held = await shorts_slots.holds(
        session, [project.slug for project, _count, _at in listed if project.shorts_line]
    )
    summaries: list[ProjectSummary] = []
    for project, count, approved_at in listed:
        # One bounded read of auto.json per video gives the registration and the tidy date.
        seen = worker_view(work_dir, project.slug) if project.shorts_line is None else None
        summaries.append(
            ProjectSummary(
                **_summary(
                    project,
                    int(count),
                    spend.get(project.slug),
                    approved_at,
                    language_states(
                        locale_choices(project),
                        batches.get(project.id, []),
                        project.dub_retries or {},
                    ),
                    compilation=project.slug in compiled,
                    download_available=project.slug in compiled
                    and download_file(work_dir, project.slug) is not None,
                    hold=held.get(project.slug),
                    producer=seen.state if seen is not None else None,
                    tidied_at=seen.tidied_at if seen is not None else None,
                )
            )
        )
    return summaries


def _browse_scope() -> Any:
    """The review tab's population: every video that is not a Short, tutorials and dramas
    alike. The Shorts tab groups the Shorts by state and is the only place that lists them."""
    return VideoProject.shorts_line.is_(None)


def _category_filter(category: str) -> Any:
    if category == "none":
        return VideoProject.category.is_(None)
    return VideoProject.category == category


def _state_filter(state: str) -> Any:
    if state == "dropped":
        return VideoProject.dropped_at.is_not(None)
    if state == "published":
        return and_(VideoProject.dropped_at.is_(None), VideoProject.youtube_video_id.is_not(None))
    return and_(VideoProject.dropped_at.is_(None), VideoProject.youtube_video_id.is_(None))


def _search_filter(q: str) -> Any:
    """The title or the slug contains the words, case-insensitively; % and _ are literal."""
    escaped = q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    pattern = f"%{escaped}%"
    return or_(
        VideoProject.title.ilike(pattern, escape="\\"),
        VideoProject.slug.ilike(pattern, escape="\\"),
    )


async def browse_projects(
    session: AsyncSession,
    *,
    category: str | None = None,
    state: str | None = None,
    q: str | None = None,
    page: int = 1,
    limit: int = BROWSE_PAGE_SIZE,
    work_dir: str | None = None,
) -> ProjectPage:
    """One page of the review tab's catalog, newest report first (docs/videos/HANDS-OFF.md
    §影片分類): the tutorials and the dramas, narrowed by a category (``none`` for the unfiled
    ones), a state and a search, with how many each other value of the two filters would list."""
    query = q.strip() if q else ""
    filters: dict[str, Any] = {"scope": _browse_scope()}
    if category is not None:
        filters["category"] = _category_filter(category)
    if state is not None:
        filters["state"] = _state_filter(state)
    if query:
        filters["q"] = _search_filter(query)

    def without(name: str) -> list[Any]:
        return [clause for key, clause in filters.items() if key != name]

    total = int(
        await session.scalar(select(func.count(VideoProject.id)).where(*filters.values())) or 0
    )
    pages = (total + limit - 1) // limit
    listed = list(
        (
            await session.execute(
                _listing_statement()
                .where(*filters.values())
                .order_by(VideoProject.last_synced_at.desc(), VideoProject.id.desc())
                .offset((page - 1) * limit)
                .limit(limit)
            )
        ).all()
    )
    category_rows = {
        (str(value) if value is not None else "none"): int(count)
        for value, count in (
            await session.execute(
                select(VideoProject.category, func.count(VideoProject.id))
                .where(*without("category"))
                .group_by(VideoProject.category)
            )
        ).all()
    }
    state_counts = [
        FacetCount(
            code=value,
            count=int(
                await session.scalar(
                    select(func.count(VideoProject.id)).where(
                        *without("state"), _state_filter(value)
                    )
                )
                or 0
            ),
        )
        for value in BROWSE_STATES
    ]
    return ProjectPage(
        items=await _summaries(session, listed, work_dir),
        total=total,
        page=page,
        pages=pages,
        facets=ProjectFacets(
            category=[
                FacetCount(code=code, count=category_rows.get(code, 0))
                for code in (*VIDEO_CATEGORY_CODES, "none")
            ],
            state=state_counts,
        ),
    )


async def set_category(
    session: AsyncSession, slug: str, user: User, payload: CategoryIn
) -> ProjectOut:
    """The owner files a video under a category, or under none; logged as
    ``video_category_set``. A dropped video can be filed too: the catalog lists it."""
    project = await _project(session, slug)
    previous = project.category
    if payload.category != previous:
        now = datetime.now(UTC)
        project.category = payload.category
        project.updated_at = now
        session.add(
            AdminAuditLog(
                actor_user_id=user.id,
                action="video_category_set",
                target=f"video_project:{project.id}",
                metadata_json={"slug": slug, "category": payload.category, "previous": previous},
            )
        )
        await session.commit()
    return await project_view(session, slug)


def _same_qa(first: dict[str, Any], second: dict[str, Any]) -> bool:
    # Key order is irrelevant; JSON preserves booleans versus numbers and list order.
    return json.dumps(first.get("qa"), sort_keys=True, separators=(",", ":")) == json.dumps(
        second.get("qa"), sort_keys=True, separators=(",", ":")
    )


async def _short_revision_allowed(session: AsyncSession, project: VideoProject) -> None:
    """Renew only before any uploader can have acted on the old approved package."""
    if (
        project.youtube_video_id is not None
        or project.youtube_upload_session is not None
        or (project.youtube_sync or {}).get("status") in ("queued", "running")
    ):
        raise AppError(
            409, "video_shorts_review_upload_started",
            "影片已開始上傳或同步，請先核對 YouTube 狀態；目前不能重新送審成片",
        )
    # The VPS sender takes the same project lock before staging or starting an upload.
    from app.video_youtube import vps
    from app.video_youtube.errors import Refused

    try:
        await vps.assert_idle(session, project.slug, upload=True)
    except Refused as error:
        raise AppError(error.status, error.code, error.detail) from error


RENEWAL_KEY = "_final_renewal"
RENEWAL_GATES = ("final", "publish", "languages", "dubs")


def _current_final(reviews: list[VideoReview]) -> VideoReview | None:
    return next((row for row in reviews if row.gate == "final" and row.subject is None), None)


# QA items a brand story's dub does not wait on once the owner approved the cut (owner,
# 2026-10-18): the owner watched the cut and judged its pacing and Jev's stance score
# themselves, and neither changes what the dub has to say or when it is said. Every other
# item, the assemble, narration and zh-TW captions among them, still has to pass.
STORY_DUB_WAIVED_QA_ITEMS: frozenset[str] = frozenset({"pace", "policy"})
# A captions item from before the QA tool stopped failing chosen locales that are translated
# only after the final gate ("en: no caption file; ja: no caption file"). The languages step
# makes those files, so a report failing on them alone does not lock a story's dub.
_FOREIGN_CAPTION_MISSING = re.compile(r"(?:en|ja|ko): no caption file")


def _story_qa_item_waived(entry: dict[str, Any]) -> bool:
    name = entry.get("id")
    if name in STORY_DUB_WAIVED_QA_ITEMS:
        return True
    if name != "captions":
        return False
    detail = entry.get("detail")
    parts = detail.split("; ") if isinstance(detail, str) and detail else []
    return bool(parts) and all(_FOREIGN_CAPTION_MISSING.fullmatch(part) for part in parts)


def _story_dub_qa_passed(report: Any, sha: str | None) -> bool:
    """Whether a story's final QA clears dubbing: bound to this cut, every item reported, and
    each failing one waived (STORY_DUB_WAIVED_QA_ITEMS, or captions missing only foreign files).

    ``final_qa_passed`` stays the rule for auto-approval and everything else; this one is read
    only after the owner approved the cut.
    """
    if not isinstance(report, dict) or not sha or report.get("final_sha256") != sha:
        return False
    items = report.get("items")
    if not isinstance(items, list):
        return False
    entries = [entry for entry in items if isinstance(entry, dict) and entry.get("id") in QA_ITEMS]
    if {entry.get("id") for entry in entries} != set(QA_ITEMS):
        return False
    return all(entry.get("ok") is True or _story_qa_item_waived(entry) for entry in entries)


def _story_dub_ready(reviews: list[VideoReview]) -> bool:
    """Only an approved current cut with switchable zh-TW CC and a clearing QA may be dubbed.

    The QA report is bound to the final mp4 hash and includes the captions check. Older cuts
    have no subtitle-mode evidence and stay locked. A newer pending, rejected or superseded
    final also locks the choice, even if an earlier cut was approved. The owner's approval
    stands in for the items in STORY_DUB_WAIVED_QA_ITEMS (_story_dub_qa_passed).
    """
    final = _current_final(reviews)
    if final is None or final.status != "approved":
        return False
    payload = final.payload or {}
    report = payload.get("qa")
    if not isinstance(report, dict):
        report = payload.get("manual_review_qa")
    return (
        isinstance(report, dict)
        and report.get("subtitles_burned_in") is False
        and _story_dub_qa_passed(report, final.content_sha256)
    )


def _story_dub_preselectable(project: VideoProject, series_kind: str | None) -> bool:
    """An owner may save dub intent for a story before its first clean final exists."""
    return (
        project.shorts_line is None
        and (project.format or "slides") == "drama"
        and (series_kind == "story" or project.category == "story")
    )


def _dub_allowed(
    project: VideoProject, series_kind: str | None, reviews: list[VideoReview]
) -> bool:
    """The detail page and both locale endpoints use one eligibility rule.

    The series kind comes from the server's episode row, so recategorising a brand story as
    an explainer does not unlock an older cut. The category also catches a standalone story.
    """
    if project.shorts_line is not None:
        return False
    if (project.format or "slides") != "drama":
        return True
    if _story_dub_preselectable(project, series_kind):
        return _story_dub_ready(reviews)
    return project.category in DUBBABLE_DRAMA_CATEGORIES


def _renewable_final(project: VideoProject, reviews: list[VideoReview]) -> VideoReview:
    _refuse_dropped(project)
    if project.shorts_line is not None or project.format == "shorts":
        raise AppError(409, "video_final_renewal_long_only", "這個換版流程只適用長片")
    upload_items = [item for item in project.checklist or [] if item.get("key") == "on_youtube"]
    # The producer reports its *next* step as stage. "on YouTube" with a single
    # explicitly unfinished checklist item is waiting to upload, not a published cut.
    waiting_upload = len(upload_items) == 1 and upload_items[0].get("done") is False
    if (
        project.youtube_video_id is not None or project.youtube_upload_session is not None
        or project.youtube_sync is not None or project.youtube_publish_at is not None
        or project.youtube_removed_at is not None
        or project.stage.strip().lower() in ("published", "uploaded", "done")
        or (project.stage.strip().lower() == "on youtube" and not waiting_upload)
        or any(item.get("done") is True for item in upload_items)
    ):
        raise AppError(
            409, "video_final_renewal_upload_started",
            "影片已有上傳紀錄或完成狀態，請先核對上傳身分；不能直接換版",
        )
    final = _current_final(reviews)
    if final is None or (
        final.status != "approved"
        and not (final.status in LIVE and RENEWAL_KEY in (final.payload or {}))
    ):
        raise AppError(409, "video_final_renewal_not_ready", "目前沒有可換版的成片審核")
    return final


def _renewal_version(project: VideoProject, reviews: list[VideoReview]) -> str:
    # Include mutable evidence as well as ids: a tool may update a pending review in place.
    def values(row: Any) -> dict[str, Any]:
        return {column.name: getattr(row, column.name) for column in row.__table__.columns}

    state = {"project": values(project), "reviews": [values(row) for row in reviews]}
    return hashlib.sha256(
        json.dumps(state, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


async def final_renewal_state(session: AsyncSession, slug: str) -> FinalRenewalState:
    project = await _project(session, slug)
    reviews = await _reviews(session, project)
    final = _renewable_final(project, reviews)
    return FinalRenewalState(
        version=_renewal_version(project, reviews), final_review_id=final.id,
        final_sha256=final.content_sha256,
    )


def _verify_renewal_files(store: ReviewStore, slug: str, payload: ReviewIn) -> None:
    roles = [item.role for item in payload.files]
    if len(roles) != len(set(roles)) or not any(
        item.role == "preview" and item.content_type == "video/mp4" for item in payload.files
    ):
        raise AppError(409, "video_final_renewal_files_invalid", "新版成片需要唯一的預覽附件")
    for item in payload.files:
        path = store.path(slug, item.sha256)
        if path is None:
            raise AppError(409, "video_review_files_missing", "新版審核附件尚未上傳完")
        digest = hashlib.sha256()
        size = 0
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                size += len(chunk)
                digest.update(chunk)
        if size != item.size or digest.hexdigest() != item.sha256:
            raise AppError(409, "video_final_renewal_files_invalid", "新版審核附件與雜湊不符")


def _hold_final_review(project: VideoProject) -> None:
    project.stage = "final video approved"
    items = [dict(item) for item in project.checklist or []]
    after_final = False
    for item in items:
        after_final = after_final or item.get("key") == "final_video_approved"
        if after_final or item.get("key") in ("on_youtube", "package", "publish", "languages"):
            item["done"] = False
    if not after_final:
        items.append({"key": "final_video_approved", "label": "成片核准", "done": False})
    project.checklist = items


async def renew_final(
    session: AsyncSession, store: ReviewStore, slug: str, user: User, payload: FinalRenewalIn
) -> ReviewOut:
    """Replace an unuploaded long cut, retaining every old decision and its evidence."""
    project = await _project(session, slug, lock=True)
    reviews = await _reviews(session, project, refresh=True)
    final = _renewable_final(project, reviews)
    if (
        payload.expected_version != _renewal_version(project, reviews)
        or payload.expected_final_review_id != final.id
        or payload.expected_final_sha256 != final.content_sha256
    ):
        raise AppError(409, "video_final_renewal_stale", "影片或審核已變更，請重新讀取後再換版")
    candidate = payload.review
    await _check_anime_review(
        session, project, candidate.gate, candidate.payload, candidate.content_sha256
    )
    if candidate.content_sha256 == final.content_sha256 or any(
        row.gate == "final" and row.content_sha256 == candidate.content_sha256 for row in reviews
    ):
        raise AppError(409, "video_final_renewal_same_content", "換版必須提供未送審過的新成片")
    # The uploaders take the same project lock, then the VPS configuration lock.
    from app.video_youtube import vps
    from app.video_youtube.errors import Refused

    try:
        await vps.assert_idle(session, slug, upload=True)
    except Refused as error:
        raise AppError(error.status, error.code, error.detail) from error
    await asyncio.to_thread(_verify_renewal_files, store, slug, candidate)
    now = datetime.now(UTC)
    details = dict(candidate.payload)
    qa = details.pop("qa", None)
    if qa is not None:
        details["manual_review_qa"] = qa
    details["manual_review"] = True
    details["manual_review_reason"] = payload.reason.strip()
    details[RENEWAL_KEY] = {
        "previous_review_id": str(final.id),
        "previous_sha256": final.content_sha256,
        "expected_version": payload.expected_version,
        "previous_stage": project.stage,
        "retained_review_ids": [
            str(row.id) for row in reviews if row.gate in RENEWAL_GATES and row.status in LIVE
        ],
    }
    replacement = VideoReview(
        id=uuid4(),
        project_id=project.id,
        gate="final",
        subject=None,
        content_sha256=candidate.content_sha256,
        revision=0,
        summary=candidate.summary,
        payload=details,
        files=[item.model_dump() for item in candidate.files],
        status="pending",
        created_at=now,
        updated_at=now,
    )
    for older in reviews:
        if older.gate not in RENEWAL_GATES or older.status not in LIVE:
            continue
        session.add(
            AdminAuditLog(
                actor_user_id=user.id,
                action="video_review_superseded",
                target=f"video_review:{older.id}",
                metadata_json={
                    "slug": slug,
                    "gate": older.gate,
                    "previous_status": older.status,
                    "replacement_review_id": str(replacement.id),
                    "sha256": older.content_sha256,
                    "reason": payload.reason.strip(),
                },
            )
        )
        older.status = "superseded"
        older.updated_at = now
    session.add(replacement)
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="video_final_renewed",
            target=f"video_project:{project.id}",
            metadata_json={"slug": slug, "review_id": str(replacement.id), **details[RENEWAL_KEY]},
        )
    )
    _hold_final_review(project)
    if project.format == "drama" and (
        project.category == "story" or await video_series_kind(session, slug) == "story"
    ):
        _withdraw_story_dubs_for_new_cut(session, project, now)
    project.updated_at = now
    project.last_synced_at = now
    await session.commit()
    # Do not prune: even superseded, never-decided evidence belongs to this explicit revision.
    return _review_out(replacement)


def _renewed_submission(
    reviews: list[VideoReview], payload: ReviewIn
) -> VideoReview | None:
    if RENEWAL_KEY in payload.payload:
        raise AppError(422, "video_final_renewal_reserved", "換版記錄只能由站主換版流程建立")
    final = _current_final(reviews)
    if final is None or RENEWAL_KEY not in (final.payload or {}):
        return None
    if payload.gate == "final" and payload.content_sha256 == final.content_sha256:
        return final  # A worker resend cannot replace the owner's pending evidence or enable QA.
    if payload.gate in RENEWAL_GATES and (
        payload.gate == "final" or final.status != "approved"
        or payload.payload.get("final_review_id") != str(final.id)
    ):
        raise AppError(
            409, "video_final_renewal_review_required",
            "新版成片須先由站主核准；後續上架與語言審核須綁定這筆成片審核",
        )
    return None


def _renewed_source(store: ReviewStore, slug: str, payload: ReviewIn, final: VideoReview) -> None:
    """A new review id alone cannot relabel the old upload package or caption timeline."""
    role = "metadata" if payload.gate == "publish" else "languages_manifest"
    item = next((item for item in payload.files if item.role == role), None)
    if item is None or item.sha256 != payload.content_sha256:
        raise AppError(409, "video_final_renewal_source_stale", "新上架包或語言須附來源清單")
    path = store.path(slug, item.sha256)
    raw = path.read_bytes() if path else b""
    if len(raw) != item.size or hashlib.sha256(raw).hexdigest() != item.sha256:
        raise AppError(409, "video_final_renewal_source_stale", "來源清單與審核附件不符")
    try:
        metadata = json.loads(raw)
    except (ValueError, UnicodeError) as error:
        raise AppError(409, "video_final_renewal_source_stale", "來源清單格式不正確") from error
    if not isinstance(metadata, dict):
        raise AppError(409, "video_final_renewal_source_stale", "來源清單格式不正確")
    if payload.gate == "publish":
        valid = (
            metadata.get("final_sha256") == final.content_sha256
            and metadata.get("branding_hash") == final.payload.get("branding_hash")
            and all(item.sha256 == final.content_sha256
                    for item in payload.files if item.role == "final")
        )
    else:
        source = metadata.get("source")
        valid = isinstance(source, dict) and source.get("final") == {
            "review_id": str(final.id), "content_sha256": final.content_sha256,
        } and source.get("branding_hash") == final.payload.get("branding_hash")
    if not valid:
        raise AppError(
            409, "video_final_renewal_source_stale", "來源仍是舊成片，請重製上架包與語言"
        )


def _supersede_short_reviews(
    session: AsyncSession,
    project: VideoProject,
    reviews: list[VideoReview],
    gates: tuple[str, ...],
    new_id: Any,
    now: datetime,
) -> None:
    for older in reviews:
        if older.gate not in gates or older.status not in LIVE:
            continue
        session.add(
            AdminAuditLog(
                actor_user_id=None,
                action="video_review_superseded",
                target=f"video_review:{older.id}",
                metadata_json={
                    "slug": project.slug, "gate": older.gate,
                    "previous_status": older.status, "replacement_review_id": str(new_id),
                    "sha256": older.content_sha256, "revision": older.revision or 0,
                },
            )
        )
        older.status = "superseded"
        older.updated_at = now


async def submit_review(
    session: AsyncSession,
    store: ReviewStore,
    slug: str,
    payload: ReviewIn,
    token: VideoToolToken,
) -> ReviewOut:
    # All review writes take the project before a review lock, also used by the uploaders.
    project = await _project(session, slug, lock=True)
    _refuse_dropped(project)
    manual_anime = await _check_anime_review(
        session, project, payload.gate, payload.payload, payload.content_sha256
    )
    # A video the worker did not make is pushed by a person or an agent by hand
    # (tools/video/review/sync.mjs marks it `hand_pushed`): the owner decides at every gate,
    # whatever the automatic checks say (owner, 2026-10-17; docs/videos/HANDS-OFF.md).
    owner_decides = manual_anime or payload.payload.get("hand_pushed") is True
    missing = [item.sha256 for item in payload.files if store.path(slug, item.sha256) is None]
    if missing:
        raise AppError(
            409, "video_review_files_missing", f"這些檔案還沒上傳完：{', '.join(missing)}"
        )
    reviews = await _reviews(session, project, refresh=True)
    renewed = _renewed_submission(reviews, payload)
    if renewed is not None:
        await session.commit()
        return _review_out(renewed)
    current = _current_final(reviews)
    if (
        current is not None
        and RENEWAL_KEY in (current.payload or {})
        and payload.gate in ("publish", "languages", "dubs")
    ):
        await asyncio.to_thread(_renewed_source, store, slug, payload, current)
    # A subject is part of what was reviewed: every character's look review is bound to the one
    # characters/manifest.json, so they share a hash and only the subject tells them apart.
    same = next(
        (
            review
            for review in reviews
            if review.gate == payload.gate
            and review.subject == payload.subject
            and review.content_sha256 == payload.content_sha256
        ),
        None,
    )
    now = datetime.now(UTC)
    short_gate = project.shorts_line is not None and payload.gate in ("final", "publish")
    revision = 0
    if short_gate:
        current = next(
            (row for row in reviews if row.gate == payload.gate and row.status in LIVE), None
        )
        if payload.gate == "publish":
            final = next(
                (row for row in reviews if row.gate == "final" and row.status in LIVE), None
            )
            if (
                final is None
                or final.status != "approved"
                or payload.payload.get("final_review_id") != str(final.id)
            ):
                raise AppError(
                    409,
                    "video_shorts_final_review_stale",
                    "上傳包必須綁定目前已核准的成片審核，請重新執行 push",
                )
        matches = (
            current is not None
            and current.content_sha256 == payload.content_sha256
            and (
                _same_qa(current.payload, payload.payload)
                if payload.gate == "final"
                else current.payload.get("final_review_id")
                == payload.payload.get("final_review_id")
            )
        )
        same = current if matches else None
        if same is None:
            # Even a pending changed receipt gets a new id, so an owner looking at an
            # older page cannot approve evidence they have not seen.
            await _short_revision_allowed(session, project)
            revision = 1 + max(
                (
                    row.revision or 0
                    for row in reviews
                    if row.gate == payload.gate and row.content_sha256 == payload.content_sha256
                ),
                default=-1,
            )
    if (
        payload.gate == "final"
        and same is None
        and project.format == "drama"
        and (project.category == "story" or await video_series_kind(session, slug) == "story")
        and _story_dub_ready(reviews)
    ):
        _withdraw_story_dubs_for_new_cut(session, project, now)
    if payload.gate == "languages":
        # A languages batch is the answer to a dub the owner asked for again
        # (docs/videos/DUBS.md §再做一次), and it closes the request in the transaction that
        # stores it, the identical-batch return below included: that one commits too, so a
        # retry that gives up with the same reason still ends. ``counted`` is whether the
        # states will read the review this resolves to; a batch equal to one that was sent
        # back or superseded shows no card, so its track is not made as far as the owner sees.
        counted = same is None or same.status in ("pending", "approved")
        _apply_dub_retry(
            session,
            project,
            dub_retry.close_on_batch(
                project.dub_retries or {}, _batch_dubs(payload.payload), now, counted=counted
            ),
        )
    if same is not None and same.status != "pending":
        await session.commit()  # release the project lock on an idempotent resend
        return _review_out(same)
    if same is not None:
        # The same file sent again while it waits: the newer payload, summary and files
        # replace the older ones (a quality check run after the fact, captions fixed without
        # touching the video), and the rules below run again on them (HANDS-OFF.md).
        same.summary = payload.summary
        same.payload = payload.payload
        same.files = [item.model_dump() for item in payload.files]
        same.updated_at = now
        review = same
    else:
        # A new submission replaces the pending one of the same gate and subject: one look
        # review per character stays open at a time, and the older gates (subject None)
        # behave as before.
        for older in reviews:
            if not short_gate and (
                older.gate == payload.gate
                and older.status == "pending"
                and older.subject == payload.subject
            ):
                older.status = "superseded"
                older.updated_at = now
        review = VideoReview(
            id=uuid4(),
            project_id=project.id,
            gate=payload.gate,
            subject=payload.subject,
            content_sha256=payload.content_sha256,
            revision=revision,
            summary=payload.summary,
            payload=payload.payload,
            files=[item.model_dump() for item in payload.files],
            status="pending",
            submitted_by_token_id=token.id,
            created_at=now,
            updated_at=now,
        )
        if short_gate:
            gates = ("final", "publish") if payload.gate == "final" else ("publish",)
            _supersede_short_reviews(session, project, reviews, gates, review.id, now)
            if payload.gate == "final":
                await shorts_slots.release(session, slug, now)
        session.add(review)
    # The owner chose on 2026-09-25 to let Jev's check stand for them on the narration: when it
    # passed every line and the setting is on, the review is decided as it arrives.
    auto_note = None
    # A drama reads its own switches (docs/videos/DRAMA-FLOW.md §一); a project row from before
    # formats existed reads as a tutorial.
    video_format = project.format or "slides"
    series_slug = project.series_slug
    if (
        not owner_decides
        and payload.gate == "audio"
        and await auto_approves_audio(session, payload.payload, video_format)
    ):
        auto_note = AUTO_APPROVED_NOTE
    # A drama's storyboard may stand on the judge's scores when the owner turned that on, or
    # when the series is hands-off (docs/videos/BINGE.md); an illustrated slides video's reads
    # its own switch (docs/videos/ILLUSTRATED.md).
    elif (
        not owner_decides
        and payload.gate == "storyboard"
        and await auto_approves_storyboard(session, payload.payload, series_slug, video_format)
    ):
        auto_note = AUTO_APPROVED_STORYBOARD_NOTE
    # A character's sheet is picked by the judge's score when the owner turned that on.
    elif (
        not owner_decides
        and payload.gate == "look"
        and await auto_picks_look(session, payload.payload, series_slug)
    ):
        auto_note = look_pick_note(payload.payload)
        review.choice = str(payload.payload.get("suggested"))
    # An episode's screenplay stands on the checker's coverage on a hands-off series.
    elif (
        not owner_decides
        and payload.gate == "script"
        and await auto_approves_script(session, series_slug, payload.payload)
    ):
        auto_note = SCRIPT_AUTO_APPROVED_NOTE
    # The owner decided on 2026-09-27 (docs/videos/HANDS-OFF.md) that Jev chooses the outline
    # and that a final cut and its upload confirmation stand on the automatic checks.
    elif (
        not owner_decides
        and payload.gate == "outline"
        and await auto_picks_outline(session, payload.payload, project.category)
    ):
        auto_note = pick_reason(payload.payload, demo_asked_of(project.category))
        review.choice = pick_choice(payload.payload)
    # A Short is held to its own twelve checks and reads its own switch
    # (docs/videos/SHORTS.md §自動品管); a long video's report never approves one, so the
    # rule below is not asked about a Short at all.
    elif (
        not owner_decides
        and payload.gate in ("final", "publish")
        and project.shorts_line is not None
    ):
        if await auto_approves_shorts(
            session, payload.gate, payload.payload, payload.content_sha256
        ):
            auto_note = (
                SHORTS_QA_AUTO_APPROVED_NOTE
                if payload.gate == "final"
                else SHORTS_PACKAGE_AUTO_APPROVED_NOTE
            )
    elif (
        not owner_decides
        and payload.gate in ("final", "publish")
        and await auto_approves_final(
            session,
            payload.gate,
            payload.payload,
            payload.content_sha256,
            video_format,
            compilation=slug in await compilation_slugs(session),
        )
    ):
        auto_note = QA_AUTO_APPROVED_NOTE if payload.gate == "final" else PACKAGE_AUTO_APPROVED_NOTE
    # A batch of languages waits for the owner only for a dub track they must upload in Studio;
    # descriptions and captions the site sends itself (docs/videos/LANGUAGES.md).
    elif (
        not owner_decides
        and payload.gate == "languages"
        and not languages_need_owner(payload.payload)
    ):
        auto_note = LANGUAGES_AUTO_APPROVED_NOTE
    if auto_note is not None:
        review.status = "approved"
        review.note = auto_note
        review.decided_at = now
        session.add(
            AdminAuditLog(
                actor_user_id=None,
                action="video_review_auto_approved",
                target=f"video_review:{review.id}",
                metadata_json={"slug": slug, "gate": review.gate, "sha256": review.content_sha256},
            )
        )
        await _short_approved(session, project, review, now)
    project.last_synced_at = now
    await session.commit()
    store.keep_only(slug, kept_files([*reviews, review]))
    return _review_out(review)


async def _short_approved(
    session: AsyncSession, project: VideoProject, review: VideoReview, now: datetime
) -> None:
    """What follows a Short's approval, whoever gave it (docs/videos/SHORTS.md): the final
    cut's reported usage goes into the ledger, and an approved upload package takes the Short
    to its slot, or to the library while the run has none for it. The caller commits."""
    if project.shorts_line is None:
        return
    if review.gate == "final":
        await shorts_costs.record_usage(
            session, project.slug, review.payload, review.content_sha256, now
        )
        await shorts_costs.record_media(session, project.slug, now)
    elif review.gate == "publish":
        await shorts_slots.assign_approved(session, project, now)


async def decide(
    session: AsyncSession, slug: str, review_id: Any, user: User, decision: DecisionIn
) -> ReviewOut:
    project = await _project(session, slug, lock=True)
    _refuse_dropped(project)
    review = await session.scalar(
        select(VideoReview)
        .where(VideoReview.id == review_id, VideoReview.project_id == project.id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if review is None:
        raise AppError(404, "video_review_not_found", "找不到這一項審核")
    problem = decision_problem(review, decision)
    if problem:
        raise AppError(409, "video_review_not_decidable", problem)
    if decision.decision == "approve":
        await _check_anime_review(
            session, project, review.gate, review.payload, review.content_sha256
        )
    now = datetime.now(UTC)
    review.status = "approved" if decision.decision == "approve" else "rejected"
    review.choice = decision.choice if review.gate in CHOICE_GATES else None
    review.note = (decision.note or "").strip() or None
    review.decided_at = now
    review.decided_by_user_id = user.id
    review.updated_at = now
    # A newly submitted replacement already withdrew consent from the previous approved cut.
    # Clearing again here would erase a fresh preselection made while this final was pending,
    # including the owner's choice before the very first clean final.
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action=f"video_review_{review.status}",
            target=f"video_review:{review.id}",
            metadata_json={
                "slug": slug,
                "gate": review.gate,
                "sha256": review.content_sha256,
                "choice": review.choice,
            },
        )
    )
    if review.status == "approved":
        await _short_approved(session, project, review, now)
    await session.commit()
    return _review_out(review)


async def drop_project(
    session: AsyncSession, store: ReviewStore, slug: str, user: User, payload: DropIn
) -> ProjectOut:
    """Stop a video for good: nothing waits on the owner any more and its previews go.

    Its row stays, so the next automatic draft still sees its topic as made.
    """
    project = await _project(session, slug)
    if project.dropped_at is not None:
        return await project_view(session, slug)
    now = datetime.now(UTC)
    for review in await _reviews(session, project):
        if review.status == "pending":
            review.status = "superseded"
            review.updated_at = now
    project.dropped_at = now
    project.dropped_note = payload.note.strip()
    project.dropped_by_user_id = user.id
    project.updated_at = now
    if project.shorts_line is not None:
        # A dropped Short leaves its slot to the next one in the library.
        await shorts_slots.release(session, slug, now)
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="video_project_dropped",
            target=f"video_project:{project.id}",
            metadata_json={"slug": slug},
        )
    )
    await _skip_abandoned_episode(session, project, user, now)
    await session.commit()
    store.keep_only(slug, set())
    return await project_view(session, slug)


async def _episode_of(
    session: AsyncSession, project: VideoProject
) -> tuple[VideoDramaEpisode, VideoDramaSeries] | None:
    """The episode this video is being made as and its series, both locked, or None.

    Only a video that reports itself as an episode is looked up (a Short or a tutorial never
    is one); the episode is then the server's own row whose slug is the video's. The series is
    locked before the episode, the order app.video_automation.series takes them in.
    """
    if project.series_slug is None or project.shorts_line is not None:
        return None
    series = await session.scalar(
        select(VideoDramaSeries)
        .join(VideoDramaEpisode, VideoDramaEpisode.series_id == VideoDramaSeries.id)
        .where(VideoDramaEpisode.slug == project.slug)
        .with_for_update(of=VideoDramaSeries)
    )
    if series is None:
        return None
    episode = await session.scalar(
        select(VideoDramaEpisode)
        .where(VideoDramaEpisode.series_id == series.id, VideoDramaEpisode.slug == project.slug)
        .with_for_update()
    )
    return None if episode is None else (episode, series)


async def _skip_abandoned_episode(
    session: AsyncSession, project: VideoProject, user: User, now: datetime
) -> None:
    """Skip the episode a dropped video was being made as (docs/videos/STORY.md §伺服器).

    Nothing else will make it under this slug, and a started one would hold its place in
    ``series_max_in_flight`` for ever. Every kind of series: the next episode of a long series
    waits for the one before to be done or skipped, so it may start now, as it may after the
    owner skips an episode on the series page. An episode already done stays done. When it was
    the series' last open episode the series finishes, as ``skip_episode`` has it. The request
    row the episode travelled as (``start_episode``) is cancelled while it is still started, so
    the owner's request list and the worker's active list stop showing it in the making; one
    already done stays done. The caller commits.
    """
    # Imported here: app.video_automation.series imports this module.
    from app.video_automation.series import EPISODE_OPEN, finish_if_complete

    found = await _episode_of(session, project)
    if found is None:
        return
    episode, series = found
    if episode.status not in EPISODE_OPEN:
        return
    episode.status = "skipped"
    episode.updated_at = now
    await _cancel_started_request(session, episode, now)
    episodes = await session.scalars(
        select(VideoDramaEpisode).where(VideoDramaEpisode.series_id == series.id)
    )
    finish_if_complete(series, list(episodes), now)
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="video_series_episode_skipped",
            target=f"video-series:{series.slug}",
            metadata_json={"number": episode.number, "dropped_video": project.slug},
        )
    )


async def _cancel_started_request(
    session: AsyncSession, episode: VideoDramaEpisode, now: datetime
) -> None:
    """Cancel the request row a dropped episode travelled as, while it is still started.

    Nothing else would ever close it: ``finish_episode`` marks it done only for a video that
    was made. Locked after the series and the episode, the order ``start_episode`` takes them
    in. A request already done, or cancelled, is left as it is.
    """
    if episode.request_id is None:
        return
    request = await session.scalar(
        select(VideoDramaRequest)
        .where(VideoDramaRequest.id == episode.request_id)
        .with_for_update()
    )
    if request is None or request.status != "started":
        return
    request.status = "cancelled"
    request.cancelled_at = now
    request.updated_at = now


async def _apply_locales(
    session: AsyncSession, project: VideoProject, user: User, payload: LocalesIn
) -> None:
    """Store the owner's language choice, note when they first decided, and log the change.

    Every video may choose titles, captions and dubs in all eight languages: the worker dubs
    es, pt, id, vi and th as well since phase two of
    tasks/open/2026-10-19-worker-video-languages-five.md (an imported video's tracks are still
    made outside the pipeline). Explainer dubs keep their narrator-only category rule, and a
    drama whose characters speak is refused a dub in any language. A brand story may store a
    dub choice early; the worker still needs the exact approved cut's switchable-CC QA before
    starting any language production.
    """
    if (project.format or "slides") == "drama" and any(
        choice.dub for choice in payload.locales.values()
    ):
        series_kind = await video_series_kind(session, project.slug)
        story = _story_dub_preselectable(project, series_kind)
        if not story and not _dub_allowed(project, series_kind, []):
            raise AppError(
                422,
                "video_locales_dub_not_for_drama",
                "有角色說話的漫劇還不能配音（docs/videos/DUBS.md），只有分類是觀念解說（explainer）的漫劇可以；"
                "這裡先只能選標題說明與 CC",
            )
    chosen: dict[str, Any] = {
        locale: choice.model_dump() for locale, choice in payload.locales.items()
    }
    if chosen == dict(project.locales or {}) and project.locales_decided_at is not None:
        return
    _record_locales(session, project, chosen, datetime.now(UTC), user)
    await session.commit()


def _record_locales(
    session: AsyncSession,
    project: VideoProject,
    chosen: dict[str, Any],
    now: datetime,
    actor: User | None,
    marks: dict[str, str] | None = None,
) -> None:
    """Store a language choice, note when it was first decided, and log it as
    ``video_locales_set``: the owner's, or with no actor and ``marks`` saying so, the server's
    (``_decide_story_locales``). The caller commits.

    A dub that leaves the choice takes its waiting retry request with it (dub_retries;
    docs/videos/DUBS.md §再做一次): nothing was touched for it yet. One the worker already took
    stays, hidden while the dub is not chosen, and goes on when it is ticked again. The audit
    row names the locales whose request went.
    """
    project.locales = chosen
    project.locales_decided_at = project.locales_decided_at or now
    project.updated_at = now
    kept, withdrawn = dub_retry.withdraw_unchosen(
        project.dub_retries or {},
        [
            locale
            for locale, choice in chosen.items()
            if isinstance(choice, dict) and choice.get("dub")
        ],
    )
    if withdrawn:
        project.dub_retries = kept
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id if actor is not None else None,
            action="video_locales_set",
            target=f"video_project:{project.id}",
            metadata_json={
                "slug": project.slug,
                "locales": chosen,
                **(marks or {}),
                **({"dub_retries_withdrawn": withdrawn} if withdrawn else {}),
            },
        )
    )


def _withdraw_story_dubs_for_new_cut(
    session: AsyncSession, project: VideoProject, now: datetime
) -> None:
    """A replacement cut must not inherit dub consent from the previously approved cut.

    This is called for an authoritative story episode when a distinct final review arrives,
    including an owner-initiated renewal. The owner can reselect dubs after the new cut's
    switchable-caption evidence is approved.
    """
    chosen = dict(project.locales or {})
    if not any(isinstance(part, dict) and part.get("dub") for part in chosen.values()):
        return
    without_dubs = {
        locale: {**part, "dub": False} if isinstance(part, dict) else part
        for locale, part in chosen.items()
    }
    _record_locales(
        session, project, without_dubs, now, None, {"reason": "story_final_cut_changed"}
    )


async def _decide_story_locales(
    session: AsyncSession, project: VideoProject, now: datetime
) -> None:
    """A brand story's languages, decided by the server when its video first reports
    (docs/videos/STORY.md §伺服器).

    A story is hands-off: nobody would choose its languages, and a video without a decision is
    never ready to upload. The server writes what the language panel's "tick the defaults"
    gives a drama, the settings' ``drama_caption_locales`` with titles, descriptions and
    captions and no dub, as the same record the owner's save writes, with the server as its
    author. Once only, and never over a decision; the owner may still change it on the panel.
    A video of any other kind still waits for the owner. The caller commits.
    """
    if project.locales_decided_at is not None or project.dropped_at is not None:
        return
    if project.series_slug is None or project.shorts_line is not None:
        return
    if await video_series_kind(session, project.slug) != "story":
        return
    settings = await session.scalar(
        select(VideoAutomationSettings).where(VideoAutomationSettings.id == 1)
    )
    ticked = settings.drama_caption_locales if settings is not None else []
    chosen: dict[str, Any] = {
        locale: LocaleChoice(metadata=True, captions=True).model_dump()
        for locale in DUB_LOCALES
        if locale in ticked
    }
    # A project first seen in this report gets its id when it is written.
    await session.flush()
    _record_locales(
        session,
        project,
        chosen,
        now,
        None,
        {"decided_by": "server", "from": "drama_caption_locales"},
    )


async def retry_project(session: AsyncSession, slug: str, user: User) -> ProjectOut:
    """Queue one retry for a blocked video; repeated clicks return the same request."""
    if not valid_slug(slug):
        raise AppError(404, "video_project_not_found", "找不到這支影片")
    project = await session.scalar(
        select(VideoProject).where(VideoProject.slug == slug).with_for_update()
    )
    if project is None:
        raise AppError(404, "video_project_not_found", "找不到這支影片")
    _refuse_dropped(project)
    if project.stage != "blocked":
        raise AppError(409, "video_retry_not_blocked", "只有卡住的影片可以重試")
    if project.retry_request_id == project.retry_acknowledged_id:
        project.retry_request_id = uuid4()
        project.updated_at = datetime.now(UTC)
        session.add(
            AdminAuditLog(
                actor_user_id=user.id,
                action="video_project_retry_requested",
                target=f"video_project:{project.id}",
                metadata_json={"slug": slug, "request_id": str(project.retry_request_id)},
            )
        )
        await session.commit()
    return await project_view(session, slug)


async def _automation_enabled(session: AsyncSession) -> bool:
    """Whether the worker runs at all: the settings row exists and 「自動產生草稿」 is on.
    While it is off the worker does nothing, so nothing should queue for it."""
    row = await session.scalar(
        select(VideoAutomationSettings).where(VideoAutomationSettings.id == 1)
    )
    return row is not None and bool(row.enabled)


def _caption_text(store: ReviewStore, slug: str, sha256: str) -> str | None:
    """A caption file of the review store as text, at most CAPTION_BYTES_MAX of it, or None
    when it cannot be read. Runs in a thread."""
    try:
        path = store.path(slug, sha256)
        if path is None:
            return None
        with path.open("rb") as source:
            return source.read(dub_retry.CAPTION_BYTES_MAX).decode("utf-8-sig")
    except (OSError, UnicodeError, StorageRefused):
        return None


def _dub_retry_blocked(code: DubRetryBlocker, tidied_at: str | None) -> AppError:
    """The refusal for a skipped dub that cannot be asked for again, by dub_retry.blocker's
    code. The page shows the same cause in place of the button (``dub_retry_blocked``)."""
    if code == "narration":
        return AppError(
            409,
            "video_dub_retry_narration",
            "這個語言就是影片原本的旁白，沒有另一條配音可做",
        )
    if code == "tidied":
        day = f"（{tidied_at[:10]}）" if tidied_at else ""
        return AppError(
            409,
            "video_dub_retry_tidied",
            f"這支影片的工作檔已經清掉{day}，成片與配音的錄音都不在了，這裡沒辦法再做一次",
        )
    if code == "publish_pending":
        return AppError(
            409,
            "video_dub_retry_publish_pending",
            "網站上最新的上架確認不是核准的（還在等、被退回，或沒有），"
            "重做的配音進不了語言包；等有核准的上架確認之後再要求",
        )
    if code == "not_adopted":
        return AppError(
            409,
            "video_dub_retry_worker_absent",
            "這支影片不在工人的工作區（不是這台工人做的，或已經放棄），工人接不到這個要求",
        )
    if code == "blocked":
        return AppError(
            409,
            "video_dub_retry_video_blocked",
            "這支影片卡住了，工人不會處理它的語言；先按「重試這支影片」，動起來之後再要求",
        )
    return AppError(
        409,
        "video_dub_retry_worker_stopped",
        "工人被 STOP 檔停住了；移掉之後再要求",
    )


async def request_dub_retry(
    session: AsyncSession,
    store: ReviewStore,
    slug: str,
    user: User,
    locale: DubLocale,
    *,
    work_dir: str | None,
    speech: dub_retry.SpeechRoom,
) -> ProjectOut:
    """The owner asks the worker to make a skipped dub track again (docs/videos/DUBS.md
    §再做一次).

    It only records the request: the dub keeps reading "skipped" until the worker takes it, so
    nothing is held for a request nobody takes, and one not taken within a day ends by itself.
    Refused, with the reason, whenever the worker could not act on it or the result could not
    be used: a dub that is not skipped, the narration's own language, a video whose work files
    were cleared, no usable upload confirmation, a video the worker does not hold or that is
    stuck, a stopped worker, automation switched off. The month's speech budget is checked
    last, against the size of the locale's captions; it is a read, not a reservation: the dub
    tool checks again before it buys and every synthesis reserves. A second click while a
    request is open returns it as it is, with no second audit row and no budget check.
    """
    project = await _project(session, slug, lock=True)
    _refuse_dropped(project)
    now = datetime.now(UTC)
    # A value no writer stores (not an object) reads as no request, as everywhere else.
    stored = project.dub_retries
    retries: dict[str, Any] = stored if isinstance(stored, dict) else {}
    previous = dub_retry.view(retries.get(locale), now)
    if previous is not None and previous.open:
        return await project_view(session, slug, work_dir)
    reviews = await _reviews(session, project)
    if project.format == "drama" and (
        project.category == "story" or await video_series_kind(session, slug) == "story"
    ) and not _story_dub_ready(reviews):
        raise AppError(
            409,
            "video_dub_retry_story_final_not_ready",
            "目前成片尚未通過無燒錄字幕與可關閉繁中 CC 的完整審核，配音重做要等通過後才開始",
        )
    part = (
        language_states(locale_choices(project), reviews, retries).get(locale, {}).get("dub")
    )
    if project.shorts_line is not None or part is None or part.state != "skipped":
        raise AppError(409, "video_dub_retry_not_skipped", "只有跳過的配音可以再做一次")
    seen = worker_view(work_dir, slug)
    code = dub_retry.blocker(
        reason=part.reason,
        tidied_at=seen.tidied_at,
        producer=seen.state,
        stage=project.stage,
        publish_usable=dub_retry.publish_usable(
            reviews, on_youtube=project.youtube_video_id is not None
        ),
    )
    if code is not None:
        raise _dub_retry_blocked(code, seen.tidied_at)
    if not await _automation_enabled(session):
        raise AppError(
            409,
            "video_automation_disabled",
            "影片自動化還沒開啟：先在影片審核的設定分頁打開「自動產生草稿」",
        )
    if not speech.configured:
        raise AppError(
            503,
            "video_speech_not_configured",
            "網站的 Gemini 金鑰還沒設定：請在「AI 設定 → API 金鑰」填 Gemini 金鑰",
        )
    captions = dub_retry.caption_sha(reviews, locale)
    text = (
        await asyncio.to_thread(_caption_text, store, slug, captions)
        if captions is not None
        else None
    )
    needed = dub_retry.estimate_characters(text)
    if speech.limit > 0:
        if not speech.available or speech.used is None:
            raise AppError(
                503,
                "video_speech_meter_unavailable",
                "讀不到本月的語音用量，先不接受這個要求；稍後再試",
            )
        if speech.used + needed > speech.limit:
            remaining = max(0, speech.limit - speech.used)
            raise AppError(
                429,
                "video_speech_budget_exhausted",
                f"本月的 Gemini 語音字數預算（{speech.limit} 字）只剩 {remaining} 字，"
                f"不夠再做一條配音（約 {needed} 字）；"
                "可調高 VIDEO_SPEECH_GEMINI_MONTHLY_CHARACTER_LIMIT，或等下個月",
            )
    entry = dub_retry.new_request(
        user_id=user.id, reason=part.reason, characters=needed, now=now
    )
    project.dub_retries = {**retries, locale: entry}
    project.updated_at = now
    # The worker's list is the newest LIST_LIMIT videos by this column: a request on an older
    # video must reach it, as a renewed final cut does.
    project.last_synced_at = now
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="video_dub_retry_requested",
            target=f"video_project:{project.id}",
            metadata_json={
                "slug": slug,
                "locale": locale,
                "request_id": entry["id"],
                "replaced_reason": part.reason,
                "estimated_characters": needed,
                "speech_used": speech.used,
                "speech_limit": speech.limit,
                # The effective status, so a request that expired is on record as that.
                "previous": (
                    {"id": str(previous.id), "status": previous.status}
                    if previous is not None
                    else None
                ),
            },
        )
    )
    await session.commit()
    return await project_view(session, slug, work_dir)


async def set_locales(
    session: AsyncSession, slug: str, user: User, payload: LocalesIn
) -> ProjectOut:
    """The owner decides a video's languages on the language panel (docs/videos/LANGUAGES.md).

    Every video is made in Traditional Chinese; here the owner says which of en, ja, ko, es,
    pt, id, vi and th to add and what of each (``locale_options``); a dub in the last five only
    on an imported video (``_apply_locales``). An empty choice is a decision too ("only Traditional
    Chinese"), and the first save of either kind is what lets the video go up. The worker makes
    only what was chosen, once the final cut is approved; a narrator-only explainer may use a
    drama dub. A brand story may save dub intent earlier, but production waits for its current
    approved cut's QA to prove switchable zh-TW captions. The choice is the owner's: the
    pipeline's reports never carry one, and a dropped video takes none. Only a
    brand story, which runs without the owner, has the server decide from the settings when its
    video first reports (``_decide_story_locales``); the owner may change that here too.

    The row is locked: a save may drop a waiting dub retry request (``_record_locales``), a
    column the worker's report and its batches write too.
    """
    project = await _project(session, slug, lock=True)
    _refuse_dropped(project)
    await _apply_locales(session, project, user, payload)
    return await project_view(session, slug)


async def set_dub_locales(
    session: AsyncSession, slug: str, user: User, payload: DubLocalesIn
) -> ProjectOut:
    """The dub checkboxes of a page from before the language panel: a ticked language gets all
    three parts, an unticked one loses its dub and keeps the rest (docs/videos/DUBS.md). Locked
    for the same reason as ``set_locales``."""
    project = await _project(session, slug, lock=True)
    _refuse_dropped(project)
    current = locale_choices(project)
    merged: dict[str, LocaleChoice] = {}
    for locale in DUB_LOCALES:
        choice = current.get(locale, LocaleChoice())
        if locale in payload.locales:
            choice = LocaleChoice(metadata=True, captions=True, dub=True)
        elif choice.dub:
            choice = LocaleChoice(metadata=choice.metadata, captions=choice.captions, dub=False)
        merged[locale] = choice
    await _apply_locales(session, project, user, LocalesIn.model_validate({"locales": merged}))
    return await project_view(session, slug)


async def file_for_admin(
    session: AsyncSession, store: ReviewStore, slug: str, sha256: str
) -> tuple[Any, str]:
    """The path and content type of a file some review of this video shows."""
    project = await _project(session, slug)
    for review in await _reviews(session, project):
        for item in review.files:
            if isinstance(item, dict) and item.get("sha256") == sha256:
                path = store.path(slug, sha256)
                if path is None:
                    break
                return path, str(item["content_type"])
    raise AppError(404, "video_review_file_not_found", "這個檔案已經不在審核區")


# --- on YouTube: the owner's link, and what the store keeps afterwards ---------------------------


def youtube_video_id(value: str) -> str | None:
    """The eleven-character id in what the owner pasted, or None when it names no video.

    Takes ``https://youtu.be/<id>``, ``https://www.youtube.com/watch?v=<id>`` (other parameters
    allowed), ``https://youtube.com/shorts/<id>``, ``https://studio.youtube.com/video/<id>/edit``
    and the bare id. Anything on another host is refused, so a pasted link cannot record an id
    that is not YouTube's.
    """
    text = value.strip()
    if YOUTUBE_ID.fullmatch(text):
        return text
    try:
        parsed = urlsplit(text if "://" in text else f"https://{text}")
        host = (parsed.hostname or "").lower()
    except ValueError:
        return None
    if parsed.scheme not in ("http", "https") or host not in YOUTUBE_HOSTS:
        return None
    parts = [part for part in parsed.path.split("/") if part]
    candidate: str | None = None
    if host == "youtu.be":
        candidate = parts[0] if parts else None
    elif parts[:1] == ["watch"]:
        candidate = next(iter(parse_qs(parsed.query).get("v", [])), None)
    elif len(parts) >= 2 and parts[0] in YOUTUBE_PATH_KINDS:
        candidate = parts[1]
    return candidate if candidate and YOUTUBE_ID.fullmatch(candidate) else None


@dataclass(frozen=True)
class YoutubePublication:
    """When YouTube says a video went, or goes, public: ``publish_at`` from videos.list, or None
    with ``reason`` saying why there is none, in the owner's words."""

    publish_at: datetime | None
    reason: str | None = None


NOT_IN_CHANNEL = "影片不在連結的頻道裡（網址對嗎？或到設定分頁換成影片所在的頻道），沒有記公開時間"
NOT_PUBLIC = "影片在 YouTube 還是私人或未公開、也沒有排程，沒有公開時間；公開後再貼一次網址"
NO_PUBLISHED_AT = "YouTube 說影片已公開，但沒有回報公開時間；請在卡片填公開時間"


def publication_of(video: dict[str, Any] | None, channel_id: str | None) -> YoutubePublication:
    """Read a videos.list item (snippet and status) as the site's publish time.

    A public video's time is ``snippet.publishedAt``; a private one scheduled in Studio carries
    ``status.publishAt``; anything else (private, unlisted, not found, another channel's) has
    none, and a video the public can see is never mistaken for a scheduled one.
    """
    if video is None:
        return YoutubePublication(None, NOT_IN_CHANNEL)
    snippet = as_dict(video.get("snippet"))
    status = as_dict(video.get("status"))
    if channel_id is not None and snippet.get("channelId") != channel_id:
        return YoutubePublication(None, NOT_IN_CHANNEL)
    if status.get("privacyStatus") == "public":
        published = parse_time(snippet.get("publishedAt"))
        return YoutubePublication(published, None if published else NO_PUBLISHED_AT)
    scheduled = parse_time(status.get("publishAt"))
    if scheduled is not None:
        return YoutubePublication(scheduled)
    return YoutubePublication(None, NOT_PUBLIC)


@asynccontextmanager
async def _linked_youtube(session: AsyncSession) -> AsyncIterator[tuple[str, YoutubeClient]]:
    """The linked channel's id and a client that speaks for it; ``Refused`` when no channel is
    linked or its grant is lost (the same answers as the sync's ``_linked_connection``)."""
    row = await connection.connection_row(session)
    if not connection.linked(row):
        raise Refused(409, "video_youtube_not_linked", "還沒有連結 YouTube 頻道：到設定分頁連結")
    if row.problem:
        raise Refused(409, "video_youtube_grant_lost", row.problem)
    channel_id = row.channel_id or ""
    async with connection.http_client() as http:
        yield channel_id, YoutubeClient(http, await connection.access_token(session, http))


def _unreachable(error: Exception) -> str:
    return f"問不到 YouTube，沒有記公開時間（{error}）；公開後再貼一次網址或跑回填"


async def youtube_publication(session: AsyncSession, video_id: str) -> YoutubePublication:
    """Ask the linked channel when ``video_id`` went or goes public (videos.list, 1 unit).

    Never raises: no linked channel, a lost grant, a refused or failed call and a video outside
    the channel all come back as a reason, so pasting an address never fails on YouTube's
    account.
    """
    try:
        async with _linked_youtube(session) as (channel_id, client):
            video = await client.video(video_id)
    except Refused as refused:
        return YoutubePublication(None, refused.detail)
    except (YoutubeError, httpx.HTTPError) as error:
        return YoutubePublication(None, _unreachable(error))
    return publication_of(video, channel_id)


async def _verify_private_youtube_video(session: AsyncSession, video_id: str) -> None:
    """Fail closed when Studio cannot prove this is an unscheduled private video on our channel."""
    try:
        async with _linked_youtube(session) as (channel_id, client):
            videos = await client.videos(
                [video_id], parts="snippet,status,contentDetails,processingDetails"
            )
    except Refused as error:
        raise AppError(error.status, error.code, error.detail) from error
    except (YoutubeError, httpx.HTTPError) as error:
        raise AppError(
            502, "video_youtube_private_verify_failed", "無法向 YouTube 驗證私人影片，沒有記錄連結"
        ) from error
    video = next((item for item in videos if item.get("id") == video_id), None)
    if video is None:
        raise AppError(
            409, "video_youtube_private_not_found", "連結頻道找不到這支影片，沒有記錄連結"
        )
    snippet = as_dict(video.get("snippet"))
    status = as_dict(video.get("status"))
    if not channel_id or snippet.get("channelId") != channel_id:
        raise AppError(409, "video_youtube_private_channel", "影片不屬於連結的頻道，沒有記錄連結")
    if status.get("privacyStatus") != "private" or status.get("publishAt"):
        raise AppError(409, "video_youtube_not_private", "影片不是未排程的私人影片，沒有記錄連結")
    processing = as_dict(video.get("processingDetails"))
    details = as_dict(video.get("contentDetails"))
    duration = duration_seconds(details.get("duration"))
    if processing.get("processingStatus") != "succeeded" or duration is None or duration <= 0:
        raise AppError(
            409,
            "video_youtube_private_unprocessed",
            "影片尚未處理完成或沒有可播放長度，沒有記錄連結",
        )


async def _lock_private_youtube_id(session: AsyncSession, video_id: str) -> None:
    """Serialize opt-in claims of one ID until commit, including while YouTube is queried."""
    try:
        dialect = session.get_bind().dialect.name
    except (AttributeError, RuntimeError):
        dialect = ""
    if dialect == "postgresql":
        lock_key = int.from_bytes(
            hashlib.sha256(f"private-youtube-link:{video_id}".encode()).digest()[:8],
            "big",
            signed=True,
        )
        await session.execute(select(func.pg_advisory_xact_lock(lock_key)))


async def link_youtube(
    session: AsyncSession,
    slug: str,
    user: User,
    video_id: str,
    publish_at: datetime | None,
    *,
    private_only: bool = False,
) -> ProjectOut:
    """The owner uploaded the final cut in Studio: record the video's id and when it goes public.

    The publish time is the owner's when they typed one. When they left it empty, it is what
    the linked channel reports (``youtube_publication``): the time a public video was
    published, or the time a private one is scheduled for; a video that is neither keeps no
    publish time, and the audit row and the page say why. Pasting again overwrites (a wrong link
    is corrected the same way). The opt-in private-only entry is stricter: it is available only
    for a pending imported final, refuses an existing or duplicated ID, and verifies privacy
    and channel ownership before recording anything. The worker reads the id back on its next
    round and writes it into the work directory's video.json.
    """
    if publish_at is not None and publish_at.tzinfo is None:
        raise AppError(422, "video_youtube_publish_at_naive", "上架時間要帶時區")
    if private_only and publish_at is not None:
        raise AppError(422, "video_youtube_private_publish_at", "私人連結不能附上公開時間")
    if private_only:
        await _lock_private_youtube_id(session, video_id)
    project = await _project(session, slug, lock=private_only)
    _refuse_dropped(project)
    if private_only:
        if project.youtube_video_id is not None:
            raise AppError(
                409, "video_youtube_already_linked", "這支影片已有 YouTube 連結，沒有覆寫"
            )
        if youtube_sync_running(project.youtube_sync):
            raise AppError(
                409, "video_youtube_private_sync_running", "YouTube 同步進行中，沒有記錄連結"
            )
        reviews = await _reviews(session, project)
        if any(review.gate == "publish" and review.status == "approved" for review in reviews):
            raise AppError(
                409,
                "video_youtube_private_package_exists",
                "已有核准的上架包，不能提早記錄私人連結",
            )
        final = _current_final(reviews)
        if (
            project.format == "shorts"
            or project.shorts_line is not None
            or final is None
            or final.status != "pending"
            or not isinstance((final.payload or {}).get("imported"), dict)
            or re.fullmatch(r"[0-9a-f]{64}", final.content_sha256 or "") is None
            or not any(item.get("role") == "preview" for item in final.files or [])
        ):
            raise AppError(
                409, "video_youtube_private_review_required", "只可為待審的匯入成片記錄私人連結"
            )
        other_slug = await session.scalar(
            select(VideoProject.slug).where(
                VideoProject.youtube_video_id == video_id, VideoProject.id != project.id
            )
        )
        if other_slug is not None:
            raise AppError(409, "video_youtube_id_in_use", "這個 YouTube ID 已連結其他影片")
        await _verify_private_youtube_video(session, video_id)
    source: str | None = "owner" if publish_at is not None else None
    reason: str | None = None
    if publish_at is None and not private_only:
        reported = await youtube_publication(session, video_id)
        publish_at, reason = reported.publish_at, reported.reason
        source = "youtube" if publish_at is not None else None
    now = datetime.now(UTC)
    project.youtube_video_id = video_id
    project.youtube_publish_at = publish_at
    project.updated_at = now
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="video_youtube_linked",
            target=f"video_project:{slug}",
            metadata_json={
                "slug": slug,
                "youtube_video_id": video_id,
                "publish_at": publish_at.isoformat() if publish_at else None,
                "publish_at_source": source,
                "publish_at_reason": reason,
                **({"private_only": True} if private_only else {}),
            },
        )
    )
    await session.commit()
    view = await project_view(session, slug)
    return view.model_copy(update={"youtube_publish_note": reason})


async def backfill_youtube_publish_times(
    session: AsyncSession, *, apply: bool, actor: User | None = None
) -> dict[str, Any]:
    """Give every linked video without a publish time the one its channel reports.

    The videos the owner published from Studio before the site asked YouTube (the eighteen of
    2026-10-07) have an id and no time, so the public library leaves them out. One videos.list
    call per fifty ids (``snippet,status``) answers for all of them; a video that is still
    private or unlisted, gone, or in another channel is reported and left alone. Nothing is
    written unless ``apply``; ``Refused`` when no channel is linked.
    """
    rows = await session.scalars(
        select(VideoProject)
        .where(
            VideoProject.youtube_video_id.is_not(None),
            VideoProject.youtube_publish_at.is_(None),
            VideoProject.dropped_at.is_(None),
        )
        .order_by(VideoProject.slug)
    )
    projects = list(rows)
    report: dict[str, Any] = {"apply": apply, "checked": len(projects), "filled": 0, "videos": []}
    if not projects:
        return report
    found: dict[str, dict[str, Any]] = {}
    async with _linked_youtube(session) as (channel_id, client):
        ids = [project.youtube_video_id for project in projects if project.youtube_video_id]
        for start in range(0, len(ids), 50):
            for item in await client.videos(ids[start : start + 50], parts="snippet,status"):
                if isinstance(item.get("id"), str):
                    found[item["id"]] = item
    now = datetime.now(UTC)
    for project in projects:
        video_id = project.youtube_video_id or ""
        reported = publication_of(found.get(video_id), channel_id)
        report["videos"].append(
            {
                "slug": project.slug,
                "youtube_video_id": video_id,
                "publish_at": reported.publish_at.isoformat() if reported.publish_at else None,
                "reason": reported.reason,
            }
        )
        if reported.publish_at is None:
            continue
        report["filled"] += 1
        if not apply:
            continue
        project.youtube_publish_at = reported.publish_at
        project.updated_at = now
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id if actor else None,
                action="video_youtube_publish_time_backfilled",
                target=f"video_project:{project.slug}",
                metadata_json={
                    "slug": project.slug,
                    "youtube_video_id": video_id,
                    "publish_at": reported.publish_at.isoformat(),
                    "publish_at_source": "youtube",
                },
            )
        )
    if apply:
        await session.commit()
    return report


def _is_video(item: Any) -> bool:
    return isinstance(item, dict) and (
        item.get("content_type") == "video/mp4" or item.get("role") == "final"
    )


async def _published_before(session: AsyncSession, cutoff: datetime) -> list[VideoProject]:
    """Videos on YouTube whose upload confirmation was approved on or before ``cutoff``."""
    confirmed = _confirmations()
    rows = await session.scalars(
        select(VideoProject)
        .join(confirmed, confirmed.c.project_id == VideoProject.id)
        .where(VideoProject.youtube_video_id.is_not(None), confirmed.c.decided_at <= cutoff)
    )
    return list(rows)


async def prune_published_previews(
    session: AsyncSession, store: ReviewStore, now: datetime | None = None
) -> dict[str, list[str]]:
    """Delete the mp4 files of videos that have been on YouTube for PREVIEW_RETENTION.

    The rule (HANDS-OFF.md §上傳包與「可以上架」): the video has a ``youtube_video_id``, its
    upload confirmation was approved at least PREVIEW_RETENTION ago and, when the owner set a
    publish time, that time is also at least PREVIEW_RETENTION past. Only files that are
    ``video/mp4`` or play the ``final`` role go; the thumbnail, captions and descriptions stay
    so the owner can still fetch them. Idempotent and cheap, so the list page calls it: a video
    whose mp4 is already gone costs one stat per file. Returns what was removed, by slug.
    """
    now = now or datetime.now(UTC)
    cutoff = now - PREVIEW_RETENTION
    removed: dict[str, list[str]] = {}
    for project in await _published_before(session, cutoff):
        if project.youtube_publish_at is not None and project.youtube_publish_at > cutoff:
            continue
        reviews = await _reviews(session, project)
        videos = {
            str(item["sha256"])
            for review in reviews
            for item in review.files
            if _is_video(item) and item.get("sha256")
        }
        if not any(store.path(project.slug, sha256) is not None for sha256 in videos):
            continue
        gone = store.keep_only(project.slug, kept_files(reviews) - videos)
        if gone:
            removed[project.slug] = gone
    return removed
