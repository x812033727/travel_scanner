"""Running one writing stage of a video with the model the owner chose for it.

The worker sends the stage's prompt and inputs; the server picks the vendor and model from the
settings, checks the month's budgets, and records what the call cost. A stage runs either on the
Claude or Codex subscription accounts the host's agent signs in (``subscription``), or with
one of the site's API keys, which never leave this server. Every stage returns one file as text
(brief.md, video.json, a fact-check report, a translation): the worker lints what comes back and
sends the problems into the next call, as the agents did.
"""

from __future__ import annotations

import asyncio
import os
import time
from pathlib import Path
from typing import Any, cast

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified

from app.ai.subscription import FULL_PERCENT
from app.config import Settings
from app.hotspots.ai_search import AIProviderName, research_provider
from app.models import VideoProject
from app.video_automation.errors import StageFailed
from app.video_automation.models import (
    DEFAULT_STAGE_MODELS,
    VideoAiRun,
    VideoAutomationSettings,
    VideoStageJob,
    utcnow,
)
from app.video_automation.schemas import StageRunIn, StageRunOut, UsageView
from app.video_automation.settings import configured_providers
from app.video_automation.subscription import run_on_subscription
from app.video_automation.usage import (
    DRAFT_STAGE,
    SUBSCRIPTION_PROVIDERS,
    budget_problem,
    slug_has_draft,
    usage_view,
)
from app.video_shorts.models import VideoShortsSettings

__all__ = ["StageFailed", "run_stage", "stage_choice", "subject_choice"]

# Synchronous callers retain their provider timeout. Durable jobs wait independently of
# the BFF's 295-second response deadline, within their RQ execution bound.
STAGE_TIMEOUT_SECONDS = 300.0
DURABLE_STAGE_TIMEOUT_SECONDS = 960.0
BUSY_STATUSES = {408, 409, 429, 500, 502, 503, 504, 529}
NO_MODEL_CALL_ERRORS = frozenset(
    {
        "video_ai_subscription_paused",
        "video_ai_subscription_auth_failed",
        "video_ai_subscription_cli_outdated",
        "video_ai_provider_not_configured",
    }
)
# The subscription refusals that ran nothing at all: no call to record, and the worker asks
# again after ``retry_after``.
SUBSCRIPTION_RAN_NOTHING = frozenset(
    {"video_ai_subscription_paused", "video_ai_subscription_auth_failed"}
)


def _job_is_stopped(stop_file: str, slug: str) -> bool:
    stop = Path(stop_file)
    return stop.exists() or (stop.parent / slug / "STOP").exists()


class StageText(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(description="The whole output file, exactly as it should be saved.")


def stage_choice(
    row: VideoAutomationSettings,
    stage: str,
    format: str = "slides",
    shorts: VideoShortsSettings | None = None,
) -> tuple[str, str]:
    """The vendor and model a stage runs on: a drama's or a Short's own choice when the owner
    made one (docs/videos/DRAMA-FLOW.md §一, SHORTS.md §資料模型), else the tutorial's, else
    the default."""
    if format == "drama":
        own = row.drama_stage_models or {}
    elif format == "shorts" and shorts is not None:
        own = shorts.stage_models or {}
    else:
        own = {}
    choice = own.get(stage) or row.stage_models.get(stage) or DEFAULT_STAGE_MODELS[stage]
    return choice["provider"], choice["model"]


def subject_choice(shorts: VideoShortsSettings | None, variant: str | None) -> tuple[str, str]:
    """The model an experiment Short tests under ``variant`` a or b: the Shorts settings'
    ``subject_models``, never the caller's choice. ``b`` left unset tests the same model as
    ``a`` (most experiments ask one model two ways); with no ``a`` nothing runs."""
    chosen = dict((shorts.subject_models or {}) if shorts is not None else {})
    choice = chosen.get(variant or "") or (chosen.get("a") if variant == "b" else None)
    if not isinstance(choice, dict) or not choice.get("provider") or not choice.get("model"):
        raise StageFailed(
            409,
            "video_ai_subject_not_chosen",
            "Shorts 設定還沒選受測模型（subject_models 的 a），實測不能跑",
        )
    return str(choice["provider"]), str(choice["model"])


async def _shorts_row(session: AsyncSession) -> VideoShortsSettings | None:
    return cast(
        VideoShortsSettings | None,
        await session.scalar(select(VideoShortsSettings).where(VideoShortsSettings.id == 1)),
    )


def _failure(error: Exception) -> StageFailed:
    if isinstance(error, httpx.HTTPStatusError):
        status = error.response.status_code
        if status in BUSY_STATUSES:
            return StageFailed(
                503,
                "video_ai_upstream_busy",
                f"模型服務暫時無法回應（HTTP {status}），請稍後重試",
                error.response.headers.get("Retry-After") or "30",
            )
        return StageFailed(
            502, "video_ai_upstream_failed", f"模型服務拒絕了這次請求（HTTP {status}）"
        )
    if isinstance(error, httpx.HTTPError):
        return StageFailed(
            502, "video_ai_upstream_unreachable", f"連不上模型服務：{type(error).__name__}", "30"
        )
    return StageFailed(502, "video_ai_output_invalid", "模型回傳的內容不符合格式，重試兩次仍失敗")


async def _on_api_key(
    runtime: Settings,
    provider_name: str,
    model: str,
    request: StageRunIn,
    client: httpx.AsyncClient | None,
    *,
    timeout_seconds: float = STAGE_TIMEOUT_SECONDS,
) -> tuple[str, str, dict[str, int]]:
    # Video stage choices named OpenAI API / Anthropic API must stay API-billed even when
    # the site-wide research connection for that vendor uses subscription accounts.
    api_runtime = runtime.model_copy(
        update={"openai_connection": "api_key", "anthropic_connection": "api_key"}
    )
    provider = research_provider(
        api_runtime,
        cast(AIProviderName, provider_name),
        client,
        model=model,
        timeout_seconds=timeout_seconds,
        max_output_tokens=request.max_output_tokens,
    )
    try:
        result, tokens = await provider.structured(
            StageText, f"video_{request.stage}", request.instructions, dict(request.payload)
        )
    except (httpx.HTTPError, ValidationError, ValueError) as error:
        raise _failure(error) from error
    finally:
        await provider.close()
    return result.text, provider.model, tokens


async def prepare_stage(
    session: AsyncSession,
    runtime: Settings,
    row: VideoAutomationSettings,
    request: StageRunIn,
    shorts: VideoShortsSettings | None = None,
    choice: tuple[str, str] | None = None,
) -> tuple[str, str, UsageView, bool]:
    if request.format == "shorts" and shorts is None:
        shorts = await _shorts_row(session)
    if choice is not None:
        provider_name, model = choice
    elif request.stage == "subject":
        provider_name, model = subject_choice(shorts, request.variant)
    else:
        provider_name, model = stage_choice(row, request.stage, request.format, shorts)
    on_plan = provider_name in SUBSCRIPTION_PROVIDERS
    usage = await usage_view(session, row)
    # A series document, an episode planned from an approved chapter, a recap or a fix is not
    # one of the month's drafts (docs/videos/SERIES.md): the series has its own monthly cap.
    new_draft = (
        request.stage == DRAFT_STAGE
        and not request.variant
        and not await slug_has_draft(session, request.slug)
    )
    problem = budget_problem(usage, new_draft=new_draft, billed=not on_plan)
    if problem:
        raise StageFailed(429, "video_ai_budget_exhausted", problem)
    if provider_name not in configured_providers(runtime):
        raise StageFailed(
            503,
            "video_ai_provider_not_configured",
            "主機的 AI 帳號代理還沒設定，訂閱帳號用不了"
            if on_plan
            else f"{request.stage} 設定用 {provider_name}，但網站還沒有這家廠商的 API 金鑰",
        )
    return provider_name, model, usage, new_draft


async def run_stage(
    session: AsyncSession,
    runtime: Settings,
    row: VideoAutomationSettings,
    request: StageRunIn,
    token_id: Any,
    client: httpx.AsyncClient | None = None,
    shorts: VideoShortsSettings | None = None,
    *,
    job: VideoStageJob | None = None,
) -> StageRunOut:
    provider_name, model, usage, new_draft = await prepare_stage(
        session,
        runtime,
        row,
        request,
        shorts,
        choice=(job.provider, job.model) if job is not None else None,
    )
    on_plan = provider_name in SUBSCRIPTION_PROVIDERS
    if job is not None:
        stop_file = os.getenv("VIDEO_STAGE_STOP_FILE")
        stopped = False
        if stop_file:
            stopped = await asyncio.to_thread(_job_is_stopped, stop_file, request.slug)
        if stopped:
            raise StageFailed(
                409, "video_ai_worker_stopped", "影片工人的 STOP 檔仍在，待執行工作不會送出模型請求"
            )
        if request.format == "shorts":
            active_shorts = shorts or await _shorts_row(session)
            enabled = active_shorts is not None and active_shorts.enabled
        else:
            enabled = row.enabled
        if not enabled:
            raise StageFailed(
                409,
                "video_ai_automation_disabled",
                "影片自動製作已停用，待執行的工作不會送出模型請求",
            )
        if request.format == "drama" and not row.drama_enabled:
            raise StageFailed(
                409, "video_ai_drama_disabled", "AI 漫劇已停用，待執行的工作不會送出模型請求"
            )
        with session.no_autoflush:
            dropped_at = await session.scalar(
                select(VideoProject.dropped_at).where(VideoProject.slug == request.slug)
            )
        if dropped_at is not None:
            raise StageFailed(409, "video_ai_project_dropped", "影片已由站主停止，不會送出模型請求")
        # Commit the dispatch boundary before contacting the model. A process dying after
        # this point cannot prove that no paid operation ran and must never retry it.
        dispatched = await session.scalar(
            update(VideoStageJob)
            .where(
                VideoStageJob.id == job.id,
                VideoStageJob.status == "running",
                VideoStageJob.dispatched_at.is_(None),
            )
            .values(dispatched_at=utcnow())
            .returning(VideoStageJob.id)
        )
        await session.commit()
        if dispatched is None:
            raise StageFailed(
                409, "video_ai_job_dispatch_closed", "工作在送出模型請求前已中斷，沒有執行模型"
            )
    started = time.monotonic()
    tokens: dict[str, int] = {"input_tokens": 0, "output_tokens": 0}
    used_model = model
    failure: StageFailed | None = None
    text: str | None = None
    try:
        if on_plan:
            run = await run_on_subscription(
                runtime,
                tool="codex" if provider_name == "codex" else "claude",
                model=model,
                instructions=request.instructions,
                payload=dict(request.payload),
                max_usage_percent=FULL_PERCENT,
            )
            text, used_model = run.text, run.model
            tokens = {"input_tokens": run.input_tokens, "output_tokens": run.output_tokens}
        else:
            text, used_model, tokens = await _on_api_key(
                runtime,
                provider_name,
                model,
                request,
                client,
                timeout_seconds=DURABLE_STAGE_TIMEOUT_SECONDS
                if job is not None
                else STAGE_TIMEOUT_SECONDS,
            )
    except StageFailed as error:
        # A paused or signed-out subscription ran nothing; there is no call to record.
        if error.code in SUBSCRIPTION_RAN_NOTHING:
            raise
        failure = error
    session.add(
        VideoAiRun(
            slug=request.slug,
            # Recorded under "planner/setting" and the like, so the draft count (planner runs)
            # does not see a series document as a tutorial draft.
            stage=f"{request.stage}/{request.variant}" if request.variant else request.stage,
            provider=provider_name,
            model=used_model,
            status="failed" if failure else "ok",
            error_code=failure.code if failure else None,
            input_tokens=int(tokens.get("input_tokens", 0)),
            output_tokens=int(tokens.get("output_tokens", 0)),
            duration_ms=int((time.monotonic() - started) * 1000),
            token_id=token_id,
        )
    )
    if failure is not None or text is None:
        if job is not None:
            problem = failure or _failure(ValueError("no result"))
            job.status = "failed" if problem.code in NO_MODEL_CALL_ERRORS else "uncertain"
            job.error_code = problem.code
            job.error_detail = problem.detail
            job.error_status = problem.status
            job.retry_after = problem.retry_after
            job.completed_at = utcnow()
        await session.commit()
        raise failure or _failure(ValueError("no result"))
    spent = int(tokens.get("input_tokens", 0)) + int(tokens.get("output_tokens", 0))
    result = StageRunOut(
        text=text,
        provider=cast(Any, provider_name),
        model=used_model,
        input_tokens=int(tokens.get("input_tokens", 0)),
        output_tokens=int(tokens.get("output_tokens", 0)),
        usage=UsageView(
            **{
                **usage.model_dump(),
                "tokens": usage.tokens + (0 if on_plan else spent),
                "subscription_tokens": usage.subscription_tokens + (spent if on_plan else 0),
                "calls": usage.calls + 1,
                "drafts": usage.drafts + (1 if new_draft else 0),
            }
        ),
    )
    if job is not None:
        job.result_json = result.model_dump(mode="json")
        job.status = "succeeded"
        job.completed_at = utcnow()
        job.error_code = job.error_detail = job.error_status = job.retry_after = None
        # A poll may have marked the same running call uncertain while it was away.
        # These columns can still be None in this session's snapshot, so force their
        # clearing when the exact late answer proves completion.
        for field in ("error_code", "error_detail", "error_status", "retry_after"):
            flag_modified(job, field)
    # A successful call's usage record and exact answer share one transaction. There is
    # no usage-only commit that could lose the reply before the durable receipt is saved.
    await session.commit()
    return result
