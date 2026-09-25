"""A writing stage on the Claude subscription accounts, through the host's AI accounts agent.

The owner chose on 2026-09-25 to run the automated writing on the subscriptions the host signs
in, having read Anthropic's terms themselves. The API never touches those accounts: it hands the
agent one prompt, and the agent runs Claude Code with every tool turned off on the account with
the most room below the owner's cap (ai_accounts_agent.runs). The answer is the model's text; the
worker parses and lints it as it does an API answer.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from app.admin_ai_accounts.agent import AiAccountsAgentClient
from app.config import Settings
from app.problems import AppError
from app.video_automation.errors import StageFailed

ANSWER_RULE = (
    "\n\nThe user message is the payload as JSON. Answer with the JSON object the instructions "
    "ask for and nothing else: no Markdown fence, no text before or after it."
)


@dataclass(frozen=True)
class PlanRun:
    text: str
    model: str
    input_tokens: int
    output_tokens: int


def _failure(error: AppError) -> StageFailed:
    if error.code == "subscription_quota_paused":
        # Nothing ran; the worker tries again on its next round, after the window moves on.
        return StageFailed(429, "video_ai_subscription_paused", error.detail, "900")
    if error.code == "subscription_not_signed_in":
        return StageFailed(
            503,
            "video_ai_provider_not_configured",
            "主機上沒有登入的 Claude 訂閱帳號：請在「AI 帳號」頁登入一個",
        )
    if error.code == "ai_accounts_agent_unavailable":
        return StageFailed(503, "video_ai_upstream_unreachable", error.detail, "60")
    return StageFailed(502, "video_ai_upstream_failed", f"Claude 訂閱帳號執行失敗：{error.detail}")


async def run_on_subscription(
    runtime: Settings,
    *,
    model: str,
    instructions: str,
    payload: dict[str, Any],
    max_usage_percent: int,
    client: AiAccountsAgentClient | None = None,
) -> PlanRun:
    agent = client or AiAccountsAgentClient(runtime)
    try:
        result = await agent.run_prompt(
            model=model,
            system=instructions + ANSWER_RULE,
            prompt=json.dumps(payload, ensure_ascii=False),
            max_usage_percent=max_usage_percent,
        )
    except AppError as error:
        raise _failure(error) from error
    return PlanRun(result.text, result.model, result.input_tokens, result.output_tokens)
