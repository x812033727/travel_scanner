"""HTTP surface of the video automation settings.

``admin_router`` is the settings tab on /admin/videos: anyone who reviews videos can read it,
only an admin who manages settings can change it, since it chooses paid models and budgets.
``tool_router`` is how the worker (or the owner's own copy of the tool) reads the same values
with a video tool token, through apps/web/app/api/video/automation.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from pydantic import AwareDatetime, BaseModel, ConfigDict, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.ai.jev import JevError, JevRequestInvalid
from app.auth.service import require_capability
from app.db import get_session
from app.infra import enforce_named_rate_limit, get_redis
from app.models import User, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import messages as drama_messages
from app.video_automation import requests as drama_requests
from app.video_automation import series as drama_series
from app.video_automation import settings as service
from app.video_automation.ai import StageFailed, run_stage
from app.video_automation.judge import (
    JudgeOutlineIn,
    JudgePolicyIn,
    OutlinePick,
    PolicyVerdict,
    judge_outline,
    judge_policy,
)
from app.video_automation.messages import MessageRefused
from app.video_automation.models import DOC_KINDS
from app.video_automation.requests import RequestRefused
from app.video_automation.schemas import (
    MESSAGE_SUBJECT_PATTERN,
    BingeQuoteOut,
    DramaRequestIn,
    DramaRequestOut,
    DramaRequestsOut,
    DramaRequestStart,
    MessageAnswerIn,
    MessageAnswerOut,
    MessageIn,
    MessageJobOut,
    MessageOut,
    MessagesOut,
    NextDramaRequestOut,
    SeriesAction,
    SeriesActionOut,
    SeriesCompilationStartIn,
    SeriesCompilationStartOut,
    SeriesContextOut,
    SeriesDocDecisionIn,
    SeriesDocEditIn,
    SeriesDocOut,
    SeriesDocSubmitIn,
    SeriesEpisodeEditIn,
    SeriesEpisodeOut,
    SeriesEpisodeRecapIn,
    SeriesEpisodeStartIn,
    SeriesEpisodeStartOut,
    SeriesIn,
    SeriesJobOut,
    SeriesKind,
    SeriesListOut,
    SeriesOut,
    SeriesPatch,
    SeriesSummary,
    SeriesWithdrawnOut,
    SettingsSave,
    SettingsView,
    SettingsWrite,
    StageModelsWrite,
    StagePromptsOut,
    StageRunIn,
    StageRunOut,
    TopicsOut,
    VisualTier,
)
from app.video_automation.series import SeriesRefused
from app.video_automation.stories import import_story_rows
from app.video_automation.topics import gather_topics
from app.video_reviews.admin_service import LIST_LIMIT, list_projects
from app.video_reviews.schemas import ProjectSummary, VideoFormat
from app.video_shorts.schemas import ShortsFilter, ShortsState
from app.video_speech.admin_api import VideoTool
from app.video_speech.checking import CheckUnavailable

# A whole video is a few dozen stage calls; this only stops a runaway loop.
RUNS_PER_HOUR = 120
TOPIC_LOOKUPS_PER_HOUR = 12
# The worker asks every few minutes; this only stops a runaway loop.
REQUEST_CALLS_PER_HOUR = 240
SERIES_CALLS_PER_HOUR = 240
# Two Jev judgements per video at most; this only stops a runaway loop.
JUDGE_CALLS_PER_HOUR = 60
# The request that carries a compiled stories.json to the import: nearly three times the 1.4 MB
# a hundred stories take now (docs/videos/STORY.md), since the file grows with what the fact
# checkers leave each story. It stays under the 5 MiB the site's relay and this API take by
# default (API_PROXY_MAX_BODY_BYTES, API_MAX_REQUEST_BYTES; nginx's client_max_body_size is 6m),
# so a file over it is refused here, by name, rather than by a nameless 413 on the way.
STORY_IMPORT_MAX_BYTES = 4 * 1024 * 1024

admin_router = APIRouter(prefix="/admin/video-automation", tags=["admin video automation"])
tool_router = APIRouter(prefix="/video/automation", tags=["video automation (pipeline)"])
Session = Annotated[AsyncSession, Depends(get_session)]
ContentReader = Annotated[User, Depends(require_capability("content.read"))]
ContentManager = Annotated[User, Depends(require_capability("content.manage"))]
SettingsManager = Annotated[User, Depends(require_capability("settings.manage"))]


class ToolSettingsView(SettingsWrite):
    updated_at: datetime | None


@admin_router.get("/settings", response_model=SettingsView)
async def get_video_automation_settings(user: ContentReader, session: Session) -> SettingsView:
    _ = user
    return await service.settings_view(session)


async def _save(session: AsyncSession, user: User, payload: SettingsWrite) -> SettingsView:
    problems = service.settings_problems(payload, await load_runtime_settings(session))
    if problems:
        raise AppError(422, "video_automation_settings_invalid", "；".join(problems))
    return await service.update_settings(session, user, payload)


def _validated(values: dict[str, Any]) -> SettingsWrite:
    """The merged settings as a whole, or 422 naming what does not hold together.

    The bounds and the consistency rules (a shortest length above the longest, no topic
    source) live on ``SettingsWrite``; a save sends only some fields, so they can only be
    checked once what was sent lies over what is stored.
    """
    try:
        return SettingsWrite.model_validate(values)
    except ValidationError as error:
        problems = "；".join(
            f"{'.'.join(str(part) for part in problem['loc'])}: {problem['msg']}"
            if problem["loc"]
            else str(problem["msg"])
            for problem in error.errors()
        )
        raise AppError(422, "video_automation_settings_invalid", problems) from error


@admin_router.put("/settings", response_model=SettingsView)
async def put_video_automation_settings(
    payload: SettingsSave, user: SettingsManager, session: Session
) -> SettingsView:
    """Save the fields the tab sent; the rest keep their stored values (SettingsSave)."""
    current = service.settings_values(await service.settings_row(session)).model_dump()
    return await _save(session, user, _validated(payload.merged_over(current)))


@admin_router.get("/prompts", response_model=StagePromptsOut)
async def get_video_stage_prompts(user: ContentReader, session: Session) -> StagePromptsOut:
    """What each stage was last told, standing instructions included, as the worker sent it."""
    _ = user
    return StagePromptsOut(prompts=await service.stage_prompts(session))


@admin_router.put("/settings/models", response_model=SettingsView)
async def put_video_automation_models(
    payload: StageModelsWrite, user: SettingsManager, session: Session
) -> SettingsView:
    """Change only the stage models, from the AI settings page.

    The drama's models change only when the page sends them: null means the drama follows the
    tutorial's, left out keeps the stored choice (docs/videos/DRAMA-FLOW.md §一).
    """
    current = service.settings_values(await service.settings_row(session)).model_dump()
    sent = payload.model_dump()
    values = {**current, "stage_models": sent["stage_models"]}
    if "drama_stage_models" in payload.model_fields_set:
        values["drama"] = {**current["drama"], "drama_stage_models": sent["drama_stage_models"]}
    return await _save(session, user, _validated(values))


@tool_router.get("/settings", response_model=ToolSettingsView)
async def get_tool_video_automation_settings(tool: VideoTool, session: Session) -> ToolSettingsView:
    _ = tool
    row = await service.settings_row(session)
    await session.commit()
    return ToolSettingsView(**service.settings_values(row).model_dump(), updated_at=row.updated_at)


@tool_router.post("/judge/outline", response_model=OutlinePick)
async def judge_video_outline(
    payload: JudgeOutlineIn, tool: VideoTool, session: Session
) -> OutlinePick:
    """Jev chooses among a brief's outlines against the channel's stance; one Jev call."""
    await enforce_named_rate_limit(
        "video_judge", str(tool.id), limit=JUDGE_CALLS_PER_HOUR, window_seconds=3600
    )
    row = await service.settings_row(session)
    await session.commit()
    stance = (row.channel_stance or "").strip()
    if not row.auto_pick_outline or not stance:
        raise AppError(
            409,
            "video_judge_not_enabled",
            "頻道立場還是空白，或「由 Jev 挑大綱」關著；大綱照舊等站主",
        )
    runtime = await load_runtime_settings(session)
    try:
        return await judge_outline(runtime, get_redis(), stance, payload.brief, payload.options)
    except CheckUnavailable as error:
        raise AppError(error.status, error.code, error.detail) from error
    except JevRequestInvalid as error:
        raise AppError(422, "video_judge_invalid", f"Jev 拒絕這個問題（{error}）") from error
    except (JevError, httpx.HTTPError) as error:
        raise AppError(502, "video_judge_upstream_failed", "Jev 暫時無法判斷") from error


@tool_router.post("/judge/policy", response_model=PolicyVerdict)
async def judge_video_policy(
    payload: JudgePolicyIn, tool: VideoTool, session: Session
) -> PolicyVerdict:
    """Jev judges a final cut's narration against the stance (the quality check's policy item)."""
    await enforce_named_rate_limit(
        "video_judge", str(tool.id), limit=JUDGE_CALLS_PER_HOUR, window_seconds=3600
    )
    row = await service.settings_row(session)
    await session.commit()
    stance = (row.channel_stance or "").strip()
    if not stance:
        raise AppError(409, "video_judge_not_enabled", "頻道立場還是空白，Jev 沒有依據可以判斷")
    runtime = await load_runtime_settings(session)
    try:
        return await judge_policy(runtime, get_redis(), stance, payload.viewpoint, payload.script)
    except CheckUnavailable as error:
        raise AppError(error.status, error.code, error.detail) from error
    except JevRequestInvalid as error:
        raise AppError(422, "video_judge_invalid", f"Jev 拒絕這個問題（{error}）") from error
    except (JevError, httpx.HTTPError) as error:
        raise AppError(502, "video_judge_upstream_failed", "Jev 暫時無法判斷") from error


@tool_router.post("/run", response_model=StageRunOut)
async def run_video_stage(request: StageRunIn, tool: VideoTool, session: Session) -> StageRunOut:
    """One writing stage with the model the owner chose for it; the model is not the caller's."""
    await enforce_named_rate_limit(
        "video_ai_run", str(tool.id), limit=RUNS_PER_HOUR, window_seconds=3600
    )
    # Kept before the run, and committed on its own, so a run the vendor refuses still leaves
    # the owner the prompt to read.
    await service.remember_prompt(session, request)
    await session.commit()
    row = await service.settings_row(session)
    runtime = await load_runtime_settings(session)
    try:
        return await run_stage(session, runtime, row, request, tool.id)
    except StageFailed as error:
        raise AppError(
            error.status,
            error.code,
            error.detail,
            headers={"Retry-After": error.retry_after} if error.retry_after else None,
        ) from error


@tool_router.get("/videos", response_model=list[ProjectSummary])
async def list_tool_videos(
    tool: VideoTool,
    session: Session,
    format: VideoFormat | None = None,
    shorts: ShortsFilter | None = None,
    state: ShortsState | None = None,
    limit: Annotated[int | None, Query(ge=1, le=LIST_LIMIT)] = None,
    before: AwareDatetime | None = None,
) -> list[ProjectSummary]:
    """Every video on /admin/videos, dropped ones too, so a new draft does not repeat a topic.

    The rounds that make tutorials and dramas ask with ``shorts=exclude``, so ninety days of
    Shorts do not push their videos past the cap; the Shorts round asks with ``shorts=only``
    (docs/videos/SHORTS.md)."""
    _ = tool
    if state is not None and shorts != "only":
        raise AppError(422, "video_shorts_state_needs_only", "state 只能跟 shorts=only 一起用")
    return await list_projects(
        session, video_format=format, shorts=shorts, state=state, limit=limit, before=before
    )


@tool_router.get("/topics", response_model=TopicsOut)
async def get_video_topics(tool: VideoTool, session: Session) -> TopicsOut:
    """Candidate topics for the next draft: the site's recent articles, then a web search."""
    await enforce_named_rate_limit(
        "video_topics", str(tool.id), limit=TOPIC_LOOKUPS_PER_HOUR, window_seconds=3600
    )
    row = await service.settings_row(session)
    runtime = await load_runtime_settings(session)
    return await gather_topics(session, runtime, get_redis(), row)


# The owner's drama requests (docs/videos/DRAMA.md): filed on /admin/videos, claimed by the worker.


def _refused(error: RequestRefused) -> AppError:
    return AppError(error.status, error.code, error.detail)


@admin_router.get("/drama-requests", response_model=DramaRequestsOut)
async def list_drama_requests(user: ContentReader, session: Session) -> DramaRequestsOut:
    """Every request the owner filed, newest first, with the video each one became."""
    _ = user
    return DramaRequestsOut(requests=await drama_requests.list_requests(session))


@admin_router.post("/drama-requests", response_model=DramaRequestOut, status_code=201)
async def create_drama_request(
    payload: DramaRequestIn, user: ContentManager, session: Session
) -> DramaRequestOut:
    """The owner asks for a one-off drama: a one-episode series whose story bible the worker
    plans on its next round (docs/videos/DRAMA-FLOW.md §二); the answer names the series in
    ``series_slug``. Refused while the drama route is switched off, so nothing queues for a
    worker that will never take it."""
    row = await service.settings_row(session)
    if not row.drama_enabled:
        raise AppError(
            409, "video_drama_disabled", "漫劇還沒開啟：先在影片審核的設定分頁打開 AI 漫劇"
        )
    try:
        return await drama_series.create_one_off(session, user, payload)
    except SeriesRefused as error:
        raise _series_refused(error) from error


@admin_router.delete("/drama-requests/{request_id}", response_model=DramaRequestOut)
async def cancel_drama_request(
    request_id: UUID, user: ContentManager, session: Session
) -> DramaRequestOut:
    """Withdraw a request the worker has not started; a started one is dropped as a video."""
    try:
        return await drama_requests.cancel_request(session, user, request_id)
    except RequestRefused as error:
        raise _refused(error) from error


@tool_router.get("/drama-requests", response_model=DramaRequestsOut)
async def list_active_drama_requests(tool: VideoTool, session: Session) -> DramaRequestsOut:
    """The requests still queued or in the making, oldest first, so a restarted worker can
    tell which of its videos answers which request."""
    await enforce_named_rate_limit(
        "video_drama_requests", str(tool.id), limit=REQUEST_CALLS_PER_HOUR, window_seconds=3600
    )
    return DramaRequestsOut(requests=await drama_requests.list_requests(session, active_only=True))


@tool_router.get("/drama-requests/next", response_model=NextDramaRequestOut)
async def next_drama_request(tool: VideoTool, session: Session) -> NextDramaRequestOut:
    """The oldest queued request, or none: what the worker should start before a scheduled draft."""
    await enforce_named_rate_limit(
        "video_drama_requests", str(tool.id), limit=REQUEST_CALLS_PER_HOUR, window_seconds=3600
    )
    return NextDramaRequestOut(request=await drama_requests.next_request(session))


@tool_router.post("/drama-requests/{request_id}/start", response_model=DramaRequestOut)
async def start_drama_request(
    request_id: UUID, payload: DramaRequestStart, tool: VideoTool, session: Session
) -> DramaRequestOut:
    """The worker claims a queued request for the video it is about to make."""
    await enforce_named_rate_limit(
        "video_drama_requests", str(tool.id), limit=REQUEST_CALLS_PER_HOUR, window_seconds=3600
    )
    try:
        return await drama_requests.start_request(session, tool, request_id, payload.slug)
    except RequestRefused as error:
        raise _refused(error) from error


@tool_router.post("/drama-requests/{request_id}/done", response_model=DramaRequestOut)
async def finish_drama_request(
    request_id: UUID, tool: VideoTool, session: Session
) -> DramaRequestOut:
    """The worker reports the request's video is finished and published."""
    await enforce_named_rate_limit(
        "video_drama_requests", str(tool.id), limit=REQUEST_CALLS_PER_HOUR, window_seconds=3600
    )
    try:
        return await drama_requests.finish_request(session, request_id)
    except RequestRefused as error:
        raise _refused(error) from error


# A long drama series (docs/videos/SERIES.md): the owner plans it on /admin/videos, approves its
# documents, and the worker plans the documents and starts the episodes in order.


def _series_refused(error: SeriesRefused) -> AppError:
    return AppError(error.status, error.code, error.detail)


async def _series_limit(tool: VideoToolToken) -> None:
    await enforce_named_rate_limit(
        "video_series", str(tool.id), limit=SERIES_CALLS_PER_HOUR, window_seconds=3600
    )


@admin_router.get("/series", response_model=SeriesListOut)
async def list_video_series(
    user: ContentReader, session: Session, kind: SeriesKind | None = None
) -> SeriesListOut:
    """Every series, newest first; ``kind`` keeps only the long series or the one-offs."""
    _ = user
    return SeriesListOut(series=await drama_series.list_series(session, kind=kind))


@admin_router.post("/series", response_model=SeriesOut, status_code=201)
async def create_video_series(
    payload: SeriesIn, user: ContentManager, session: Session
) -> SeriesOut:
    """The owner starts a series; the worker plans its setting book on its next round."""
    row = await service.settings_row(session)
    if not row.drama_enabled:
        raise AppError(
            409, "video_drama_disabled", "漫劇還沒開啟：先在影片審核的設定分頁打開 AI 漫劇"
        )
    try:
        return await drama_series.create_series(session, user, payload)
    except SeriesRefused as error:
        raise _series_refused(error) from error


@admin_router.get("/series/binge-quote", response_model=BingeQuoteOut)
async def video_series_binge_quote(
    user: ContentReader,
    session: Session,
    total_minutes: int = Query(ge=30, le=480),
    episode_minutes: int = Query(default=3, ge=1, le=8),
    visual_tier: VisualTier = "hybrid",
) -> BingeQuoteOut:
    """What a binge series of these minutes would take, before the owner presses the button
    (docs/videos/BINGE.md); declared before the slug route so the path is never a slug."""
    _ = user
    row = await service.settings_row(session)
    return drama_series.binge_quote(row, total_minutes, episode_minutes, visual_tier)


@admin_router.get("/series/{slug}", response_model=SeriesOut)
async def video_series_detail(slug: str, user: ContentReader, session: Session) -> SeriesOut:
    _ = user
    try:
        return await drama_series.series_view(session, slug)
    except SeriesRefused as error:
        raise _series_refused(error) from error


@admin_router.patch("/series/{slug}", response_model=SeriesOut)
async def patch_video_series(
    slug: str, payload: SeriesPatch, user: ContentManager, session: Session
) -> SeriesOut:
    try:
        return await drama_series.patch_series(session, user, slug, payload)
    except SeriesRefused as error:
        raise _series_refused(error) from error


@admin_router.delete("/series/{slug}", response_model=SeriesWithdrawnOut)
async def withdraw_video_series(
    slug: str, user: ContentManager, session: Session
) -> SeriesWithdrawnOut:
    """Withdraw a drama before the worker starts any of its episodes (a one-off at its story
    bible, a series at its documents); its queued requests are cancelled with it."""
    try:
        return await drama_series.withdraw_series(session, user, slug)
    except SeriesRefused as error:
        raise _series_refused(error) from error


def _doc_kind(kind: str) -> str:
    if kind not in DOC_KINDS:
        raise AppError(404, "video_series_doc_not_found", "沒有這種文件")
    return kind


@admin_router.post("/series/{slug}/docs/{kind}/decision", response_model=SeriesOut)
@admin_router.post("/series/{slug}/docs/{kind}/{chapter}/decision", response_model=SeriesOut)
async def decide_video_series_doc(
    slug: str,
    kind: str,
    payload: SeriesDocDecisionIn,
    user: ContentManager,
    session: Session,
    chapter: int = 0,
) -> SeriesOut:
    """Approve a document, or send it back with a note the worker rewrites it from."""
    try:
        return await drama_series.decide_doc(
            session, user, slug, _doc_kind(kind), chapter, payload.decision, payload.note
        )
    except SeriesRefused as error:
        raise _series_refused(error) from error


@admin_router.put("/series/{slug}/docs/{kind}", response_model=SeriesOut)
@admin_router.put("/series/{slug}/docs/{kind}/{chapter}", response_model=SeriesOut)
async def edit_video_series_doc(
    slug: str,
    kind: str,
    payload: SeriesDocEditIn,
    user: ContentManager,
    session: Session,
    chapter: int = 0,
) -> SeriesOut:
    """The owner's own version of a document, approved at once when asked."""
    try:
        return await drama_series.edit_doc(session, user, slug, _doc_kind(kind), chapter, payload)
    except SeriesRefused as error:
        raise _series_refused(error) from error


@admin_router.put("/series/{slug}/episodes/{number}", response_model=SeriesOut)
async def edit_video_series_episode(
    slug: str, number: int, payload: SeriesEpisodeEditIn, user: ContentManager, session: Session
) -> SeriesOut:
    try:
        return await drama_series.edit_episode(session, user, slug, number, payload)
    except SeriesRefused as error:
        raise _series_refused(error) from error


@admin_router.post("/series/{slug}/actions/{action}", response_model=SeriesActionOut)
async def act_on_video_series(
    slug: str, action: SeriesAction, user: ContentManager, session: Session
) -> SeriesActionOut:
    try:
        view, detail = await drama_series.act(session, user, slug, action)
    except SeriesRefused as error:
        raise _series_refused(error) from error
    return SeriesActionOut(series=view, detail=detail)


@admin_router.post("/series/{slug}/episodes/{number}/skip", response_model=SeriesOut)
async def skip_video_series_episode(
    slug: str, number: int, user: ContentManager, session: Session
) -> SeriesOut:
    try:
        return await drama_series.skip_episode(session, user, slug, number)
    except SeriesRefused as error:
        raise _series_refused(error) from error


@admin_router.post("/series/{slug}/episodes/{number}/restore", response_model=SeriesOut)
async def restore_video_series_episode(
    slug: str, number: int, user: ContentManager, session: Session
) -> SeriesOut:
    """Bring a skipped story that never started back to ready: the way back from ``/skip``,
    for a story series only (``restore_episode`` says why)."""
    try:
        return await drama_series.restore_episode(session, user, slug, number)
    except SeriesRefused as error:
        raise _series_refused(error) from error


# The brand-story backlog (docs/videos/STORY.md §企劃清單與集數列): the admin page's way to what
# the host command video-story-import does. The file's rules, the report and the audit record
# are app.video_automation.stories'; this only carries the file there and the report back.


class StoryImportIn(BaseModel):
    """A compiled stories.json and how to import it, as the host command takes them.

    ``file`` is the whole file as JSON. Anything is let through here, because the file is
    checked in one place only: whatever is wrong with it comes back in the report.
    """

    model_config = ConfigDict(extra="forbid")

    file: Any
    apply: bool = False
    limit: int | None = None
    episodes_per_day: int | None = None


class StoryImportRowsOut(BaseModel):
    model_config = ConfigDict(extra="forbid")

    create: list[str]
    update: list[str]
    renumbered: list[str]
    unchanged: list[str]
    started: list[str]
    refused: list[str]


class StoryImportOut(BaseModel):
    """``StoryImportReport.as_dict()``, field for field: what the import did, or would do with
    ``apply``. Extra fields are refused, so the two cannot drift apart unnoticed."""

    model_config = ConfigDict(extra="forbid")

    series: str
    dry_run: bool
    accepted: bool
    written: bool
    series_exists: bool
    series_created: bool
    stories_in_file: int
    stories_imported: int
    create: int
    update: int
    leave_alone: int
    refuse: int
    rows: StoryImportRowsOut
    series_differs: dict[str, dict[str, Any]]
    problems: list[str]
    notes: list[str]


async def _import_refused(request: Request, report: dict[str, Any]) -> JSONResponse:
    """The answer to a file with a problem: the site's problem document (a code, and a detail
    for a caller that reads nothing else) with the whole report beside it, so the page can list
    every problem."""
    problems = report["problems"]
    detail = f"企劃清單有 {len(problems)} 個問題，整份都沒有寫入。第一個：{problems[0]}"
    problem = await app_error_handler(request, AppError(422, "video_story_import_refused", detail))
    return JSONResponse(
        {**json.loads(bytes(problem.body)), **report},
        status_code=422,
        media_type="application/problem+json",
    )


@admin_router.post(
    "/series/{slug}/stories/import",
    response_model=StoryImportOut,
    responses={
        413: {"description": "The request is over STORY_IMPORT_MAX_BYTES."},
        422: {"description": "The file has a problem: a problem document with the report."},
    },
)
async def import_video_series_stories(
    slug: str, payload: StoryImportIn, request: Request, user: ContentReader, session: Session
) -> StoryImportOut | JSONResponse:
    """Check a compiled stories.json for the story series ``slug`` and, with ``apply``, import
    it: the series is created from the file when it does not exist, and each story becomes an
    episode ready to start (``import_story_rows``).

    The dry run is the default and writes nothing, so reading the series is enough for it;
    ``apply`` needs what creating a series needs. A file with a problem, the path's slug not
    being the file's ``series.slug`` among them, is refused whole: nothing is written, and the
    answer is a 422 that carries the report.
    """
    if payload.apply:
        await require_capability("content.manage")(user)
    size = len(await request.body())
    if size > STORY_IMPORT_MAX_BYTES:
        raise AppError(
            413,
            "video_story_import_too_large",
            f"企劃清單最多 {STORY_IMPORT_MAX_BYTES / 1_048_576:.1f} MB，"
            f"這次送來 {size / 1_048_576:.1f} MB",
        )
    try:
        report = await import_story_rows(
            session,
            payload.file,
            series_slug=slug,
            apply=payload.apply,
            limit=payload.limit,
            episodes_per_day=payload.episodes_per_day,
            actor=user,
        )
    except SeriesRefused as error:
        raise _series_refused(error) from error
    answer = report.as_dict()
    if report.problems:
        return await _import_refused(request, answer)
    return StoryImportOut.model_validate(answer)


# The discussion thread on every document and every screenplay (docs/videos/DRAMA-FLOW.md §三):
# the owner writes, the worker's next round answers.


def _message_refused(error: MessageRefused) -> AppError:
    return AppError(error.status, error.code, error.detail)


Subject = Annotated[str, Query(pattern=MESSAGE_SUBJECT_PATTERN, max_length=24)]


@admin_router.get("/series/{slug}/messages", response_model=MessagesOut)
async def list_video_series_messages(
    slug: str, subject: Subject, user: ContentReader, session: Session
) -> MessagesOut:
    """One thread, oldest first: the owner's lines and the model's answers."""
    _ = user
    try:
        return MessagesOut(messages=await drama_messages.list_messages(session, slug, subject))
    except SeriesRefused as error:
        raise _series_refused(error) from error


@admin_router.post("/series/{slug}/messages", response_model=MessageOut, status_code=201)
async def post_video_series_message(
    slug: str, payload: MessageIn, user: ContentManager, session: Session
) -> MessageOut:
    """The owner's line on a document or a screenplay; the model answers on the worker's next
    round. Refused once the document is approved or the screenplay gate is passed."""
    try:
        return await drama_messages.post_message(session, user, slug, payload)
    except SeriesRefused as error:
        raise _series_refused(error) from error
    except MessageRefused as error:
        raise _message_refused(error) from error


@tool_router.get("/series/messages/next", response_model=MessageJobOut)
async def next_video_series_message(tool: VideoTool, session: Session) -> MessageJobOut:
    """The oldest line waiting for the model, with what the model reads to answer it, or none."""
    await _series_limit(tool)
    return await drama_messages.next_message(session)


@tool_router.post("/series/messages/{message_id}/answer", response_model=MessageAnswerOut)
async def answer_video_series_message(
    message_id: UUID, payload: MessageAnswerIn, tool: VideoTool, session: Session
) -> MessageAnswerOut:
    """The model's reply, and the document's new version when the owner asked for a change."""
    await _series_limit(tool)
    try:
        return await drama_messages.answer_message(session, message_id, payload)
    except SeriesRefused as error:
        raise _series_refused(error) from error
    except MessageRefused as error:
        raise _message_refused(error) from error


@tool_router.get("/series/next", response_model=SeriesJobOut)
async def next_video_series_job(tool: VideoTool, session: Session) -> SeriesJobOut:
    """The next document to plan or episode to start, or none while every series waits."""
    await _series_limit(tool)
    return await drama_series.next_job(session, await service.settings_row(session))


@tool_router.get("/series/{slug}/context", response_model=SeriesContextOut)
async def video_series_context(
    slug: str, tool: VideoTool, session: Session, episode: int | None = None
) -> SeriesContextOut:
    await _series_limit(tool)
    try:
        return await drama_series.context_view(
            session, await drama_series._series(session, slug), episode
        )
    except SeriesRefused as error:
        raise _series_refused(error) from error


@tool_router.post("/series/{slug}/docs", response_model=SeriesDocOut, status_code=201)
async def submit_video_series_doc(
    slug: str, payload: SeriesDocSubmitIn, tool: VideoTool, session: Session
) -> SeriesDocOut:
    await _series_limit(tool)
    try:
        return await drama_series.submit_doc(
            session, slug, payload, await service.settings_row(session)
        )
    except SeriesRefused as error:
        raise _series_refused(error) from error


@tool_router.post("/series/{slug}/episodes/{number}/start", response_model=SeriesEpisodeStartOut)
async def start_video_series_episode(
    slug: str, number: int, payload: SeriesEpisodeStartIn, tool: VideoTool, session: Session
) -> SeriesEpisodeStartOut:
    await _series_limit(tool)
    try:
        return await drama_series.start_episode(session, tool, slug, number, payload.slug)
    except SeriesRefused as error:
        raise _series_refused(error) from error


@tool_router.post("/series/{slug}/episodes/{number}/recap", response_model=SeriesEpisodeOut)
async def recap_video_series_episode(
    slug: str, number: int, payload: SeriesEpisodeRecapIn, tool: VideoTool, session: Session
) -> SeriesEpisodeOut:
    await _series_limit(tool)
    try:
        return await drama_series.recap_episode(session, slug, number, payload)
    except SeriesRefused as error:
        raise _series_refused(error) from error


@tool_router.post("/series/{slug}/episodes/{number}/done", response_model=SeriesEpisodeOut)
async def finish_video_series_episode(
    slug: str, number: int, tool: VideoTool, session: Session
) -> SeriesEpisodeOut:
    await _series_limit(tool)
    try:
        return await drama_series.finish_episode(session, slug, number)
    except SeriesRefused as error:
        raise _series_refused(error) from error


@tool_router.post("/series/{slug}/compilation/start", response_model=SeriesCompilationStartOut)
async def start_video_series_compilation(
    slug: str, payload: SeriesCompilationStartIn, tool: VideoTool, session: Session
) -> SeriesCompilationStartOut:
    """The worker starts the compilation of a finished binge series (docs/videos/BINGE.md)."""
    await _series_limit(tool)
    try:
        return await drama_series.start_compilation(session, tool, slug, payload.slug)
    except SeriesRefused as error:
        raise _series_refused(error) from error


@tool_router.post("/series/{slug}/compilation/done", response_model=SeriesSummary)
async def finish_video_series_compilation(
    slug: str, tool: VideoTool, session: Session
) -> SeriesSummary:
    await _series_limit(tool)
    try:
        return await drama_series.finish_compilation(session, slug)
    except SeriesRefused as error:
        raise _series_refused(error) from error
