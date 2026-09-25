"""Running one writing stage of a video with the model the owner chose for it.

The worker sends the stage's prompt and inputs; the server picks the vendor and model from the
settings, checks the month's budgets, and records what the call cost. A stage runs either on the
Claude subscription accounts the host's agent signs in (``subscription``), or with one of the
site's API keys, which never leave this server. Every stage returns one file as text (brief.md,
video.json, a fact-check report, a translation): the worker lints what comes back and sends the
problems into the next call, as the agents did.
"""

from __future__ import annotations

import time
from typing import Any, cast

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.hotspots.ai_search import AIProviderName, research_provider
from app.video_automation.errors import StageFailed
from app.video_automation.models import DEFAULT_STAGE_MODELS, VideoAiRun, VideoAutomationSettings
from app.video_automation.schemas import StageRunIn, StageRunOut, UsageView
from app.video_automation.settings import configured_providers
from app.video_automation.subscription import run_on_subscription
from app.video_automation.usage import (
    DRAFT_STAGE,
    SUBSCRIPTION_PROVIDER,
    budget_problem,
    slug_has_draft,
    usage_view,
)

__all__ = ["StageFailed", "run_stage", "stage_choice"]

# A stage writes a whole script or report without streaming, so the read timeout covers the
# entire generation. nginx allows 300 s for /api/, and the worker calls the API directly.
STAGE_TIMEOUT_SECONDS = 300.0
BUSY_STATUSES = {408, 409, 429, 500, 502, 503, 504, 529}


class StageText(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(description="The whole output file, exactly as it should be saved.")


def stage_choice(row: VideoAutomationSettings, stage: str) -> tuple[str, str]:
    choice = row.stage_models.get(stage) or DEFAULT_STAGE_MODELS[stage]
    return choice["provider"], choice["model"]


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
) -> tuple[str, str, dict[str, int]]:
    provider = research_provider(
        runtime,
        cast(AIProviderName, provider_name),
        client,
        model=model,
        timeout_seconds=STAGE_TIMEOUT_SECONDS,
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


async def run_stage(
    session: AsyncSession,
    runtime: Settings,
    row: VideoAutomationSettings,
    request: StageRunIn,
    token_id: Any,
    client: httpx.AsyncClient | None = None,
) -> StageRunOut:
    provider_name, model = stage_choice(row, request.stage)
    on_plan = provider_name == SUBSCRIPTION_PROVIDER
    usage = await usage_view(session, row)
    new_draft = request.stage == DRAFT_STAGE and not await slug_has_draft(session, request.slug)
    problem = budget_problem(usage, new_draft=new_draft, billed=not on_plan)
    if problem:
        raise StageFailed(429, "video_ai_budget_exhausted", problem)
    if provider_name not in configured_providers(runtime):
        raise StageFailed(
            503,
            "video_ai_provider_not_configured",
            "主機的 AI 帳號代理還沒設定，Claude 訂閱帳號用不了"
            if on_plan
            else f"{request.stage} 設定用 {provider_name}，但網站還沒有這家廠商的 API 金鑰",
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
                model=model,
                instructions=request.instructions,
                payload=dict(request.payload),
                max_usage_percent=row.subscription_max_usage_percent,
            )
            text, used_model = run.text, run.model
            tokens = {"input_tokens": run.input_tokens, "output_tokens": run.output_tokens}
        else:
            text, used_model, tokens = await _on_api_key(
                runtime, provider_name, model, request, client
            )
    except StageFailed as error:
        # A paused subscription ran nothing; there is no call to record.
        if error.code == "video_ai_subscription_paused":
            raise
        failure = error
    session.add(
        VideoAiRun(
            slug=request.slug,
            stage=request.stage,
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
    await session.commit()
    if failure is not None or text is None:
        raise failure or _failure(ValueError("no result"))
    spent = int(tokens.get("input_tokens", 0)) + int(tokens.get("output_tokens", 0))
    return StageRunOut(
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
