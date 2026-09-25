"""One prompt through a signed-in Claude Code account, with every tool turned off.

The owner chose on 2026-09-25 to have the video pipeline's writing stages (planning, writing,
fact-checking, the listener edit, caption translation and review) run on the subscription
accounts this agent manages, having read the providers' terms themselves. The agent stays the
only thing that touches those accounts; the API asks it for one run at a time.

What keeps a run harmless, since the prompt carries web pages that are untrusted text and the
agent runs as root:

- ``--tools ""``: no built-in tool at all, so the model can neither read a file nor run a
  command nor fetch a page; ``--strict-mcp-config`` without a config adds no MCP server either.
  Text in, text out.
- Codex is not offered: ``codex exec`` has no switch that removes its shell, and its read-only
  sandbox still reads every file this service can, including the site's ``.env``.
- The environment is built from scratch (``runner.cli_environment``), the working folder is an
  empty one under the state root, deleted afterwards, and no session is kept.
- An account whose 5-hour or weekly window is at or above the caller's cap is skipped; when all
  are, nothing runs and the answer says when the earliest window resets.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import time
import uuid
from dataclasses import dataclass
from typing import Any

from ai_accounts_agent.config import SLOTS, AgentConfig
from ai_accounts_agent.runner import CliError, cli_environment, parse_json_object

RUN_TIMEOUT_SECONDS = 900.0
MAX_PROMPT_CHARS = 3_000_000
MAX_SYSTEM_CHARS = 100_000
MODEL_PATTERN = re.compile(r"[A-Za-z0-9._:-]{1,64}")
# How the CLI says a subscription window is spent (probed 2026-09-24: "You've hit your weekly
# limit"); a run that ends like this is a pause, not a failure.
LIMIT_MESSAGE = re.compile(r"hit your (?:weekly |5-hour |session |usage )?limit|usage limit", re.I)


class RunRefused(Exception):
    """Why no run happened: the status and code the API should see."""

    def __init__(self, status: int, code: str, detail: str, extra: dict[str, Any] | None = None):
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail
        self.extra = extra or {}


@dataclass(frozen=True)
class RunRequest:
    model: str
    system: str
    prompt: str
    max_usage_percent: int
    timeout_seconds: float

    @classmethod
    def parse(cls, payload: dict[str, Any] | None) -> RunRequest:
        if payload is None:
            raise RunRefused(422, "run_invalid", "the body must be a JSON object")
        if payload.get("tool", "claude") != "claude":
            raise RunRefused(
                422, "run_tool_not_offered", "only Claude Code runs prompts; Codex keeps a shell"
            )
        model, system, prompt = payload.get("model"), payload.get("system"), payload.get("prompt")
        cap = payload.get("max_usage_percent", 80)
        timeout = payload.get("timeout_seconds", RUN_TIMEOUT_SECONDS)
        if not isinstance(model, str) or not MODEL_PATTERN.fullmatch(model):
            raise RunRefused(422, "run_invalid", "model must be a model name")
        if not isinstance(system, str) or not 0 < len(system) <= MAX_SYSTEM_CHARS:
            raise RunRefused(422, "run_invalid", "system must be text")
        if not isinstance(prompt, str) or not 0 < len(prompt) <= MAX_PROMPT_CHARS:
            raise RunRefused(422, "run_invalid", "prompt must be text within the size limit")
        if not isinstance(cap, int) or isinstance(cap, bool) or not 1 <= cap <= 100:
            raise RunRefused(422, "run_invalid", "max_usage_percent must be 1 to 100")
        if not isinstance(timeout, int | float) or not 30 <= timeout <= RUN_TIMEOUT_SECONDS:
            raise RunRefused(
                422, "run_invalid", f"timeout_seconds must be 30 to {RUN_TIMEOUT_SECONDS:.0f}"
            )
        return cls(model, system, prompt, cap, float(timeout))


def _peak(slot: dict[str, Any]) -> tuple[float | None, str | None]:
    """The fullest window of an account, and when that window resets."""
    windows = (slot.get("usage") or {}).get("windows") or []
    peak: float | None = None
    resets: str | None = None
    for window in windows:
        used = window.get("used_percent")
        if isinstance(used, int | float) and (peak is None or used > peak):
            peak, resets = float(used), window.get("resets_at")
    return peak, resets


def pick_slot(slots: list[dict[str, Any]], cap: int, default: str | None) -> str:
    """The signed-in Claude subscription with the most room below ``cap``.

    An account whose usage is not known yet is tried after every known one; that is the state
    right after sign-in, before the first usage probe has run.
    """
    known: list[tuple[float, int, str]] = []
    unknown: list[str] = []
    blocked: list[str] = []
    for slot in slots:
        if slot.get("tool") != "claude" or slot.get("logged_in") is not True:
            continue
        if slot.get("auth_method") == "api_key" or slot.get("email_allowed") is False:
            continue
        name = str(slot.get("slot"))
        peak, resets = _peak(slot)
        if peak is None:
            unknown.append(name)
        elif peak >= cap:
            if resets:
                blocked.append(resets)
        else:
            known.append((peak, 0 if name == default else 1, name))
    if known:
        return min(known)[2]
    if unknown:
        return sorted(unknown, key=lambda name: (name != default, SLOTS.index(name)))[0]
    if blocked:
        earliest = min(blocked)
        raise RunRefused(
            429,
            "subscription_quota_paused",
            f"every Claude account is at or above {cap}% of a usage window; "
            f"the earliest resets at {earliest}",
            {"resets_at": earliest},
        )
    raise RunRefused(
        409, "subscription_not_signed_in", "no Claude subscription account is signed in"
    )


def run_claude(config: AgentConfig, slot: str, request: RunRequest) -> dict[str, Any]:
    """Run the prompt once on one account; the answer's text and the tokens it took."""
    workdir = config.state_root / "runs" / uuid.uuid4().hex
    workdir.mkdir(mode=0o700, parents=True)
    try:
        system_file = workdir / "system.txt"
        system_file.write_text(request.system, encoding="utf-8")
        command = [
            *config.claude_command,
            "-p",
            "--output-format",
            "json",
            "--model",
            request.model,
            "--tools",
            "",
            "--strict-mcp-config",
            "--no-session-persistence",
            "--system-prompt-file",
            str(system_file),
        ]
        environment = cli_environment(
            config, {"CLAUDE_CONFIG_DIR": str(config.slot_path("claude", slot))}
        )
        started = time.monotonic()
        try:
            completed = subprocess.run(  # noqa: S603 - fixed argv, shell=False, no tools
                command,
                input=request.prompt,
                cwd=workdir,
                env=environment,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=request.timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise CliError(f"Claude did not finish in {request.timeout_seconds:.0f} s") from exc
        except OSError as exc:
            raise CliError(f"cannot start claude: {exc.strerror}") from exc
        duration_ms = int((time.monotonic() - started) * 1000)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    result = parse_json_object(completed.stdout)
    text = result.get("result") if result else None
    if LIMIT_MESSAGE.search(str(text or "")) or LIMIT_MESSAGE.search(completed.stderr):
        raise RunRefused(429, "subscription_quota_paused", f"account {slot} hit its usage limit")
    if (
        completed.returncode != 0
        or result is None
        or result.get("is_error")
        or not isinstance(text, str)
    ):
        reason = (text if isinstance(text, str) else completed.stderr).strip().splitlines()
        raise CliError(
            f"claude run failed: {reason[-1][:300] if reason else f'exit {completed.returncode}'}"
        )
    raw_usage = result.get("usage")
    usage: dict[str, Any] = raw_usage if isinstance(raw_usage, dict) else {}
    # Cached prompt tokens still count against the plan's window, so they count here too.
    tokens_in = 0
    for key in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"):
        tokens_in += int(usage.get(key) or 0)
    return {
        "text": text,
        "slot": slot,
        "model": str(result.get("model") or request.model),
        "input_tokens": tokens_in,
        "output_tokens": int(usage.get("output_tokens") or 0),
        "duration_ms": duration_ms,
    }
