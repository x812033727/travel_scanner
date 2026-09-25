"""What the video pipeline has spent this month, measured against the owner's budgets."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import case, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.video_automation.models import VideoAiRun, VideoAutomationSettings
from app.video_automation.schemas import UsageView

# A draft is counted when its planning stage first succeeds in the month.
DRAFT_STAGE = "planner"


def month_start(now: datetime | None = None) -> datetime:
    moment = now or datetime.now(UTC)
    return moment.astimezone(UTC).replace(day=1, hour=0, minute=0, second=0, microsecond=0)


async def usage_view(
    session: AsyncSession, row: VideoAutomationSettings, now: datetime | None = None
) -> UsageView:
    since = month_start(now)
    tokens, calls, failed = (
        await session.execute(
            select(
                func.coalesce(func.sum(VideoAiRun.input_tokens + VideoAiRun.output_tokens), 0),
                func.count(VideoAiRun.id),
                func.coalesce(func.sum(case((VideoAiRun.status == "failed", 1), else_=0)), 0),
            ).where(VideoAiRun.created_at >= since)
        )
    ).one()
    drafts = await session.scalar(
        select(func.count(distinct(VideoAiRun.slug))).where(
            VideoAiRun.created_at >= since,
            VideoAiRun.stage == DRAFT_STAGE,
            VideoAiRun.status == "ok",
        )
    )
    return UsageView(
        tokens=int(tokens or 0),
        token_budget=row.monthly_token_budget_millions * 1_000_000,
        drafts=int(drafts or 0),
        draft_budget=row.max_drafts_per_month,
        calls=int(calls or 0),
        failed_calls=int(failed or 0),
    )


async def slug_has_draft(session: AsyncSession, slug: str, now: datetime | None = None) -> bool:
    """Whether this video already counts as one of the month's drafts."""
    found = await session.scalar(
        select(VideoAiRun.id)
        .where(
            VideoAiRun.slug == slug,
            VideoAiRun.stage == DRAFT_STAGE,
            VideoAiRun.status == "ok",
            VideoAiRun.created_at >= month_start(now),
        )
        .limit(1)
    )
    return found is not None


def budget_problem(usage: UsageView, *, new_draft: bool) -> str | None:
    """Why a call may not run now, in the owner's words; None when it may."""
    if usage.tokens >= usage.token_budget:
        return (
            f"本月模型 token 已用 {usage.tokens:,}，達到上限 {usage.token_budget:,}；"
            "可以在影片審核的設定分頁調高"
        )
    if new_draft and usage.drafts >= usage.draft_budget:
        return f"本月已產生 {usage.drafts} 支草稿，達到上限 {usage.draft_budget} 支"
    return None
