"""Claude on the host's subscription accounts, behind the same ``structured()`` call as the API.

The owner chose on 2026-09-25 to run every site feature that uses Claude on the subscription
accounts the host signs in at /admin/ai-accounts instead of an API key, having been told the
terms, quota and speed risks. The "AI vendors" card switches this with ``anthropic_connection``.
The API never touches those accounts: it hands the AI accounts agent one prompt, and the agent
runs Claude Code with every tool turned off on the signed-in account with the most room below
the owner's cap (``ai_accounts_agent.runs``). If a run hits the limit, the agent moves on to the
next account.

When no account can serve (every one is at the cap, none is signed in, the agent is down, or
all are busy past the wait), the call falls back to MiniMax, if the site has its key. The
provider then reports MiniMax's name and model, so the run records show what actually served.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any, Literal, Protocol, TypeVar

from pydantic import BaseModel, ValidationError

from app.admin_ai_accounts.agent import AiAccountsAgentClient
from app.admin_ai_accounts.schemas import AgentOverview
from app.ai.structured_output import extract_json_document, repair_instruction, schema_instructions
from app.config import Settings
from app.problems import AppError

TModel = TypeVar("TModel", bound=BaseModel)

Connection = Literal["api_key", "subscription"]

# Why a subscription call gives way to MiniMax: nothing ran, so trying another vendor spends
# nothing twice. A run that started and failed is reported instead.
FALLBACK_CODES = frozenset(
    {
        "subscription_quota_paused",
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


class _Structured(Protocol):
    name: Any
    model: str

    async def structured(
        self,
        schema: type[TModel],
        schema_name: str,
        instructions: str,
        payload: dict[str, Any],
    ) -> tuple[TModel, dict[str, int]]: ...

    async def close(self) -> None: ...


def on_subscription(settings: Settings, vendor: str) -> bool:
    """Whether calls to this vendor go to the host's subscription accounts."""
    return vendor == "anthropic" and settings.anthropic_connection == "subscription"


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
    """``ResearchProvider`` for Claude on the subscription accounts, falling back to MiniMax."""

    def __init__(
        self,
        settings: Settings,
        model: str,
        timeout_seconds: float,
        fallback: Callable[[], _Structured] | None = None,
        agent: AiAccountsAgentClient | None = None,
    ) -> None:
        self.name: Any = "anthropic"
        self.model = model
        # "claude:b" for the account that answered last, or the fallback vendor's name.
        self.served_by: str | None = None
        self._settings = settings
        self._timeout_seconds = run_seconds(timeout_seconds)
        self._fallback_factory = fallback
        self._fallback: _Structured | None = None
        self._agent = agent or AiAccountsAgentClient(settings)

    async def close(self) -> None:
        if self._fallback is not None:
            await self._fallback.close()

    async def _on_fallback(
        self, schema: type[TModel], schema_name: str, instructions: str, payload: dict[str, Any]
    ) -> tuple[TModel, dict[str, int]]:
        if self._fallback is None:
            assert self._fallback_factory is not None
            self._fallback = self._fallback_factory()
        # The rest of this provider's calls go there too: the accounts will not free up within
        # one guide review or one news stage.
        self.name, self.model = self._fallback.name, self._fallback.model
        self.served_by = str(self._fallback.name)
        return await self._fallback.structured(schema, schema_name, instructions, payload)

    async def structured(
        self,
        schema: type[TModel],
        schema_name: str,
        instructions: str,
        payload: dict[str, Any],
    ) -> tuple[TModel, dict[str, int]]:
        if self._fallback is not None:
            return await self._on_fallback(schema, schema_name, instructions, payload)
        system = f"{instructions.rstrip()}\n{schema_instructions(schema)}{ANSWER_RULE}"
        usage = {"input_tokens": 0, "output_tokens": 0}
        previous = ""
        failure: ValidationError | None = None
        for attempt in range(2):
            prompt = json.dumps(payload, ensure_ascii=False)
            if attempt and failure is not None:
                prompt += repair_instruction(previous, failure)
            try:
                result = await self._agent.run_prompt(
                    model=self.model,
                    system=system,
                    prompt=prompt,
                    max_usage_percent=self._settings.ai_subscription_max_usage_percent,
                    timeout_seconds=self._timeout_seconds,
                    queue_seconds=QUEUE_SECONDS,
                )
            except AppError as error:
                if error.code not in FALLBACK_CODES or self._fallback_factory is None:
                    raise
                return await self._on_fallback(schema, schema_name, instructions, payload)
            self.served_by = f"claude:{result.slot}"
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


def subscription_summary(overview: AgentOverview, cap: int) -> tuple[bool, str]:
    """For the card's connection test: can any Claude account serve, and what each one has."""
    usable: list[str] = []
    notes: list[str] = []
    for slot in overview.slots:
        if slot.tool != "claude" or slot.logged_in is not True:
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
            notes.append(f"{name} 已用 {peak:.0f}%，達上限 {cap}%")
        else:
            usable.append(f"{name}（已用 {peak:.0f}%）")
    if not usable:
        detail = "；".join(notes) if notes else "主機上沒有登入的 Claude 訂閱帳號"
        return False, f"Claude 訂閱帳號目前都不能用：{detail}"
    message = f"Claude 訂閱帳號可用：{'、'.join(usable)}"
    if notes:
        message += f"；{'；'.join(notes)}"
    return True, message
