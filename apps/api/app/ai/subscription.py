"""Claude and Codex subscription accounts behind the API's ``structured()`` call.

The AI vendors card selects API key or a host subscription account for Claude and OpenAI
research calls. The API hands the AI accounts agent one prompt; the agent runs Claude Code or
Codex with tools disabled on a signed-in account. If a run hits the limit, it rotates accounts.

The call always runs the vendor and model the feature chose. When no account can serve (every
one is at the cap, none is signed in, the agent is down, or all are busy past the wait), the
error goes back to the caller, which tries again later (the news pipeline pauses the candidate).
The owner decided on 2026-09-28 that a full account hands over to the next one and never to
MiniMax: the MiniMax fallback and its setting were removed.
"""

from __future__ import annotations

import json
from typing import Any, Literal, TypeVar

from pydantic import BaseModel, ValidationError

from app.admin_ai_accounts.agent import AiAccountsAgentClient
from app.admin_ai_accounts.schemas import AgentOverview
from app.ai.structured_output import extract_json_document, repair_instruction, schema_instructions
from app.config import Settings

TModel = TypeVar("TModel", bound=BaseModel)

Connection = Literal["api_key", "subscription"]
SUBSCRIPTION_TOOLS = {"anthropic": "claude", "openai": "codex"}
SUBSCRIPTION_LABELS = {"claude": "Claude", "codex": "Codex"}

# The owner's choice of 2026-09-26: no usage cap. The accounts take turns in slot order
# (A, B, C, … and back to A), and one is left only when its 5-hour or weekly window is full.
FULL_PERCENT = 100

# Why a subscription call is put off rather than failed: nothing ran, so trying again later
# spends nothing twice. A run that started and failed is reported instead.
WAIT_CODES = frozenset(
    {
        "subscription_quota_paused",
        # Every account rests for failing to authenticate (a 403 access grant, an expired
        # OAuth token): nothing ran, and a person signs one in again on /admin/ai-accounts.
        "subscription_auth_failed",
        "subscription_not_signed_in",
        "subscription_busy",
        "ai_accounts_agent_unavailable",
    }
)
# Claude Code starts a fresh session per run, which adds seconds to what the API would take;
# the agent refuses a run limit below 30 s or above 900 s.
CLI_OVERHEAD_SECONDS = 60.0
MAX_RUN_SECONDS = 900.0
# Background callers can wait for another feature's run to end rather than give up.
QUEUE_SECONDS = 120.0

ANSWER_RULE = (
    "\n\nThe user message is the payload as JSON. Answer with the JSON object the schema "
    "describes and nothing else: no Markdown fence, no text before or after it."
)


def on_subscription(settings: Settings, vendor: str) -> bool:
    """Whether calls to this vendor go to the host's subscription accounts."""
    return (vendor == "anthropic" and settings.anthropic_connection == "subscription") or (
        vendor == "openai" and settings.openai_connection == "subscription"
    )


def vendor_ready(settings: Settings, vendor: str) -> bool:
    """Whether the site can call this vendor: its key, or the agent for a subscription."""
    if on_subscription(settings, vendor):
        return settings.ai_accounts_configured
    keys = {
        "openai": settings.openai_api_key,
        "anthropic": settings.anthropic_api_key,
        "minimax": settings.minimax_api_key,
        "gemini": settings.hotspot_guide_gemini_api_key,
    }
    return bool(keys.get(vendor))


def run_seconds(timeout_seconds: float) -> float:
    """The agent's limit for one run, from the caller's limit for one API call."""
    return min(MAX_RUN_SECONDS, timeout_seconds + CLI_OVERHEAD_SECONDS)


class SubscriptionResearchProvider:
    """``ResearchProvider`` on a vendor's subscription accounts, and nothing else."""

    def __init__(
        self,
        settings: Settings,
        model: str,
        timeout_seconds: float,
        agent: AiAccountsAgentClient | None = None,
        vendor: Literal["anthropic", "openai"] = "anthropic",
    ) -> None:
        self.name: Any = vendor
        self.model = model
        # "claude:b" for the account that answered last.
        self.served_by: str | None = None
        self._settings = settings
        self._tool = SUBSCRIPTION_TOOLS[vendor]
        self._timeout_seconds = run_seconds(timeout_seconds)
        self._agent = agent or AiAccountsAgentClient(settings)

    async def close(self) -> None:
        return None

    async def structured(
        self,
        schema: type[TModel],
        schema_name: str,
        instructions: str,
        payload: dict[str, Any],
    ) -> tuple[TModel, dict[str, int]]:
        system = f"{instructions.rstrip()}\n{schema_instructions(schema)}{ANSWER_RULE}"
        usage = {"input_tokens": 0, "output_tokens": 0}
        previous = ""
        failure: ValidationError | None = None
        for attempt in range(2):
            prompt = json.dumps(payload, ensure_ascii=False)
            if attempt and failure is not None:
                prompt += repair_instruction(previous, failure)
            # A full account hands over to the next one inside the agent (A -> B -> ... -> A);
            # an error here means none of them can take the run now.
            result = await self._agent.run_prompt(
                tool=self._tool,
                model=self.model,
                system=system,
                prompt=prompt,
                max_usage_percent=FULL_PERCENT,
                timeout_seconds=self._timeout_seconds,
                queue_seconds=QUEUE_SECONDS,
            )
            self.served_by = f"{self._tool}:{result.slot}"
            usage["input_tokens"] += result.input_tokens
            usage["output_tokens"] += result.output_tokens
            previous = extract_json_document(result.text)
            try:
                return schema.model_validate_json(previous), usage
            except ValidationError as error:
                if attempt:
                    raise
                failure = error
        raise ValueError("AI structured output validation failed")


def _peak(slot: Any) -> float | None:
    windows = slot.usage.windows if slot.usage else []
    return max((window.used_percent for window in windows), default=None)


def subscription_summary(
    overview: AgentOverview, cap: int = FULL_PERCENT, *, tool: str = "claude"
) -> tuple[bool, str]:
    """For the card's connection test: can any account of this tool serve?"""
    label = SUBSCRIPTION_LABELS[tool]
    usable: list[str] = []
    notes: list[str] = []
    for slot in overview.slots:
        if slot.tool != tool or slot.logged_in is not True:
            continue
        name = slot.slot.upper()
        if slot.auth_method == "api_key":
            notes.append(f"{name} 是 API 金鑰登入，不會用")
            continue
        if slot.email_allowed is False:
            notes.append(f"{name} 不在允許清單")
            continue
        peak = _peak(slot)
        if peak is None:
            usable.append(f"{name}（用量未知）")
        elif peak >= cap:
            notes.append(f"{name} 已用滿（{peak:.0f}%），等額度重置")
        else:
            usable.append(f"{name}（已用 {peak:.0f}%）")
    if not usable:
        detail = "；".join(notes) if notes else f"主機上沒有登入的 {label} 訂閱帳號"
        return False, f"{label} 訂閱帳號目前都不能用：{detail}"
    message = f"{label} 訂閱帳號可用：{'、'.join(usable)}"
    if notes:
        message += f"；{'；'.join(notes)}"
    return True, message
