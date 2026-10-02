"""Where the worker's Shorts jobs go (ticket video-shorts-automation-api): the next job, the
weekly plan, new topics, the weekly report, and a Short's start and finish; and the tab's
topics, assets and reports. Registered in ``app.main`` already, so that ticket adds routes
here and nowhere else.

The file name carries ``admin`` on purpose: its errors are the operator's, in Traditional
Chinese, and ``tests/test_error_localization.py`` asks for four more languages of any
``AppError`` raised outside an admin file.

The worker's paths are the ones the site relays (apps/web/app/api/video/automation/shorts):
``next``, ``plan``, ``topics``, ``report``, ``{slug}/start`` and ``{slug}/done``.
"""

from __future__ import annotations

import re
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import require_capability
from app.db import get_session
from app.infra import enforce_named_rate_limit
from app.models import User
from app.problems import AppError
from app.video_media.admin_api import media_store
from app.video_media.settings import get_media_settings
from app.video_reviews.storage import PART_BYTES
from app.video_shorts import assets, jobs, plan, reports, topics
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.schemas import (
    NEED_KEY_PATTERN,
    TOPIC_SLUG_PATTERN,
    AssetPartOut,
    CampaignIn,
    DoneIn,
    NextOut,
    PlanIn,
    PlanOut,
    ReportIn,
    ReportOut,
    ReportsOut,
    ShortsLine,
    StartOut,
    StrictModel,
    TopicIn,
    TopicOut,
    TopicPatch,
    TopicsIn,
    TopicsOut,
    TopicStatus,
    TopicsWrittenOut,
)
from app.video_speech.admin_api import VideoTool

# The worker asks every five minutes and writes back a few times a week; these only stop a
# runaway loop.
NEXT_CALLS_PER_HOUR = 120
WRITES_PER_HOUR = 120

admin_router = APIRouter(prefix="/admin/video-shorts", tags=["admin video shorts"])
tool_router = APIRouter(prefix="/video/automation/shorts", tags=["video shorts (pipeline)"])
Session = Annotated[AsyncSession, Depends(get_session)]
ContentReader = Annotated[User, Depends(require_capability("content.read"))]
ContentManager = Annotated[User, Depends(require_capability("content.manage"))]


class AssetInfoIn(StrictModel):
    """What the owner writes about a file once its parts are in: a person's name and the
    terms of use, so it travels in a body and never in a URL."""

    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    need: str = Field(pattern=NEED_KEY_PATTERN)
    filename: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=120)
    rights_note: str = Field(min_length=1, max_length=2000)
    taken_on: date | None = None


# What the part upload refuses to find in its URL.
INFO_FIELDS = frozenset({"filename", "author", "rights_note", "taken_on"})


def refused(error: ShortsRefused) -> AppError:
    return AppError(error.status, error.code, error.detail)


def _checked_slug(slug: str) -> str:
    if not re.fullmatch(TOPIC_SLUG_PATTERN, slug):
        raise AppError(404, "video_shorts_topic_not_found", "找不到這個題目")
    return slug


# --- the tab ------------------------------------------------------------------------------------


@admin_router.get("/topics", response_model=TopicsOut)
async def list_shorts_topics(
    user: ContentReader,
    session: Session,
    line: ShortsLine | None = None,
    status: TopicStatus | None = None,
) -> TopicsOut:
    """The library in the order it is made from: release order first, then the oldest."""
    _ = user
    return TopicsOut(items=await topics.list_topics(session, line=line, status=status))


@admin_router.post("/topics", response_model=TopicOut, status_code=201)
async def add_shorts_topic(payload: TopicIn, user: ContentManager, session: Session) -> TopicOut:
    """The owner's idea: kept as an idea the planner completes, unless its spec is whole."""
    try:
        return await topics.add_idea(session, user, payload)
    except ShortsRefused as error:
        raise refused(error) from error


@admin_router.post("/topics/import", response_model=TopicsWrittenOut)
async def import_shorts_campaign(
    payload: CampaignIn, user: ContentManager, session: Session
) -> TopicsWrittenOut:
    """The campaign's topics from campaign.json as sent; importing again adds nothing."""
    try:
        return await topics.import_campaign(session, user, payload)
    except ShortsRefused as error:
        raise refused(error) from error


@admin_router.patch("/topics/{slug}", response_model=TopicOut)
async def change_shorts_topic(
    slug: str, payload: TopicPatch, user: ContentManager, session: Session
) -> TopicOut:
    try:
        return await topics.patch_topic(session, user, _checked_slug(slug), payload)
    except ShortsRefused as error:
        raise refused(error) from error


@admin_router.post("/topics/{slug}/assets", response_model=AssetPartOut)
async def upload_shorts_asset(
    slug: str,
    request: Request,
    user: ContentManager,
    session: Session,
    sha256: Annotated[str, Query(pattern=r"^[0-9a-f]{64}$")],
    part: Annotated[int, Query(ge=0, le=100)],
    parts: Annotated[int, Query(ge=1, le=100)],
    size: Annotated[int, Query(ge=1)],
    need: Annotated[str, Query(pattern=NEED_KEY_PATTERN)],
) -> AssetPartOut:
    """One part (4 MiB at most) of a file the owner supplies for a topic; the URL names the
    bytes and nothing else. The file is the topic's material once ``…/assets/finish`` says
    who made it and on what terms."""
    _ = user
    held = sorted(INFO_FIELDS & request.query_params.keys())
    if held:
        # A URL lands in nginx's access log, the site's proxy log and the browser's history:
        # an old page that still puts a person's name there is stopped, not quietly obeyed.
        raise AppError(
            422,
            "video_shorts_asset_info_in_url",
            f"{'、'.join(held)} 要放在 …/assets/finish 的 JSON 內容，不能放在網址",
        )
    body = await request.body()
    if len(body) > PART_BYTES:
        raise AppError(413, "video_shorts_asset_part_too_large", f"每一段最多 {PART_BYTES} 位元組")
    try:
        return await assets.upload_part(
            session,
            media_store(get_media_settings()),
            _checked_slug(slug),
            assets.AssetPart(
                sha256=sha256, part=part, parts=parts, size=size, data=body, need=need
            ),
        )
    except ShortsRefused as error:
        raise refused(error) from error


@admin_router.post("/topics/{slug}/assets/finish", response_model=AssetPartOut)
async def finish_shorts_asset(
    slug: str, payload: AssetInfoIn, user: ContentManager, session: Session
) -> AssetPartOut:
    """A file whose parts are all in becomes the topic's material, with who made it and on
    what terms, sent once in the body."""
    try:
        return await assets.add_asset(
            session,
            media_store(get_media_settings()),
            user,
            _checked_slug(slug),
            assets.AssetInfo(**payload.model_dump()),
        )
    except ShortsRefused as error:
        raise refused(error) from error


@admin_router.get("/reports", response_model=ReportsOut)
async def list_shorts_reports(
    user: ContentReader,
    session: Session,
    limit: Annotated[int, Query(ge=1, le=reports.LIST_LIMIT)] = reports.LIST_LIMIT,
) -> ReportsOut:
    """The weekly reports, newest first, with the numbers they cite as YouTube gave them."""
    _ = user
    return ReportsOut(items=await reports.list_reports(session, limit))


# --- the worker ---------------------------------------------------------------------------------


async def _limit(name: str, tool: VideoTool, limit: int) -> None:
    await enforce_named_rate_limit(
        f"video_shorts_{name}", str(tool.id), limit=limit, window_seconds=3600
    )


@tool_router.get("/next", response_model=NextOut)
async def next_shorts_job(tool: VideoTool, session: Session) -> NextOut:
    """The next job: a report, a plan, a brief, a Short to make, or none and why."""
    await _limit("next", tool, NEXT_CALLS_PER_HOUR)
    return await jobs.next_job(session)


@tool_router.post("/plan", response_model=PlanOut)
async def write_shorts_plan(payload: PlanIn, tool: VideoTool, session: Session) -> PlanOut:
    """The planner's week, checked whole before any slot changes."""
    await _limit("write", tool, WRITES_PER_HOUR)
    try:
        return await plan.apply_plan(session, payload)
    except ShortsRefused as error:
        raise refused(error) from error


@tool_router.post("/topics", response_model=TopicsWrittenOut)
async def write_shorts_topics(
    payload: TopicsIn, tool: VideoTool, session: Session
) -> TopicsWrittenOut:
    """The planner's new topics and the ideas it completed; ready only with a whole spec."""
    await _limit("write", tool, WRITES_PER_HOUR)
    return await topics.write_planner_topics(session, payload.topics)


@tool_router.post("/report", response_model=ReportOut)
async def write_shorts_report(payload: ReportIn, tool: VideoTool, session: Session) -> ReportOut:
    """The week's report; the same week again replaces it."""
    await _limit("write", tool, WRITES_PER_HOUR)
    try:
        return await reports.save_report(session, payload)
    except ShortsRefused as error:
        raise refused(error) from error


@tool_router.post("/{slug}/start", response_model=StartOut)
async def start_short(slug: str, tool: VideoTool, session: Session) -> StartOut:
    """The worker starts the topic: it is in the making, and its Short is a video."""
    await _limit("write", tool, WRITES_PER_HOUR)
    try:
        return await jobs.start_topic(session, _checked_slug(slug))
    except ShortsRefused as error:
        raise refused(error) from error


@tool_router.post("/{slug}/done", response_model=TopicOut)
async def finish_short(
    slug: str, tool: VideoTool, session: Session, payload: DoneIn | None = None
) -> TopicOut:
    """The worker is done with the topic: its Short was pushed, or it gives none."""
    await _limit("write", tool, WRITES_PER_HOUR)
    try:
        return await jobs.finish_topic(session, _checked_slug(slug), payload or DoneIn())
    except ShortsRefused as error:
        raise refused(error) from error
