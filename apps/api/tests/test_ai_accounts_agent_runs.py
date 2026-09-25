"""The agent's prompt runs: which account, which flags, what comes back, and what never runs."""

from __future__ import annotations

import json
import sys
import textwrap
import time
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest

from ai_accounts_agent.config import AgentConfig
from ai_accounts_agent.runner import CliError
from ai_accounts_agent.runs import RunRefused, RunRequest, pick_slot, run_claude
from ai_accounts_agent.security import signature_for
from ai_accounts_agent.server import AgentApplication

KEY = "k" * 64

# Records what it was given in the account folder, then answers like `claude -p --output-format
# json`. The prompt decides the outcome: LIMIT answers as a spent window, FAIL exits with an error;
# a file named "spent" in the account folder makes that account answer as spent.
FAKE_CLAUDE = textwrap.dedent(
    """
    import json, os, sys
    prompt = sys.stdin.buffer.read().decode("utf-8")
    args = sys.argv[1:]
    system_file = args[args.index("--system-prompt-file") + 1]
    system = open(system_file, encoding="utf-8").read()
    record = {"args": args, "prompt": prompt, "system": system, "env": dict(os.environ)}
    folder = os.environ["CLAUDE_CONFIG_DIR"]
    with open(os.path.join(folder, "last-run.json"), "w", encoding="utf-8") as out:
        json.dump(record, out)
    if "FAIL" in prompt:
        print("boom: model overloaded", file=sys.stderr)
        sys.exit(1)
    if "LIMIT" in prompt or os.path.exists(os.path.join(folder, "spent")):
        spent = {"type": "result", "is_error": True, "result": "You've hit your weekly limit"}
        print(json.dumps(spent))
        sys.exit(1)
    usage = {"input_tokens": 100, "cache_creation_input_tokens": 20, "output_tokens": 40}
    usage["cache_read_input_tokens"] = 5
    answer = {"type": "result", "is_error": False, "result": '{"ok": true}', "usage": usage}
    answer["model"] = "claude-opus-5-5"
    print(json.dumps(answer))
    """
)


def _config(tmp_path: Path) -> AgentConfig:
    fake = tmp_path / "fake_claude.py"
    fake.write_text(FAKE_CLAUDE, encoding="utf-8")
    config = AgentConfig(
        hmac_key=KEY,
        socket_path=tmp_path / "agent.sock",
        state_root=tmp_path / "state",
        claude_command=(sys.executable, str(fake)),
        codex_command=(sys.executable, str(fake)),
    )
    for slot in ("a", "b"):
        config.slot_path("claude", slot).mkdir(parents=True, exist_ok=True)
    return config


def _request(prompt: str = '{"brief": "…"}', **changes: Any) -> RunRequest:
    payload: dict[str, Any] = {
        "tool": "claude",
        "model": "claude-opus-5-5",
        "system": "You are the fact-checker.",
        "prompt": prompt,
        "max_usage_percent": 80,
        "timeout_seconds": 60,
    }
    payload.update(changes)
    return RunRequest.parse(payload)


@pytest.mark.parametrize(
    "changes",
    [
        {"tool": "codex"},
        {"model": "opus; rm -rf /"},
        {"system": ""},
        {"prompt": ""},
        {"max_usage_percent": 0},
        {"max_usage_percent": True},
        {"timeout_seconds": 5},
        {"timeout_seconds": 10_000},
        {"queue_seconds": -1},
        {"queue_seconds": 10_000},
        {"queue_seconds": True},
    ],
)
def test_a_run_request_must_name_claude_a_model_and_sane_limits(changes: dict[str, Any]) -> None:
    with pytest.raises(RunRefused) as refused:
        _request(**changes)
    assert refused.value.status == 422


def _slot(slot: str, *peaks: float | None, **extra: Any) -> dict[str, Any]:
    windows = [
        {
            "window_minutes": minutes,
            "used_percent": peak,
            "resets_at": f"2026-09-25T1{index}:00:00Z",
        }
        for index, (minutes, peak) in enumerate(zip((300, 10080), peaks, strict=False))
        if peak is not None
    ]
    return {
        "tool": "claude",
        "slot": slot,
        "logged_in": True,
        "auth_method": "claude.ai",
        "email_allowed": None,
        "usage": {"windows": windows} if windows else None,
        **extra,
    }


def test_the_account_with_the_most_room_below_the_cap_is_picked() -> None:
    assert pick_slot([_slot("a", 50, 70), _slot("b", 10, 30)], 80, "a") == "b"
    assert pick_slot([_slot("a", 30), _slot("b", 30)], 80, "b") == "b", "a tie goes to the default"
    assert pick_slot([_slot("a", 90), _slot("c")], 80, "a") == "c", "unknown usage is tried last"
    assert pick_slot([_slot("a", 10, auth_method="api_key"), _slot("b", 60)], 80, "a") == "b"
    assert pick_slot([_slot("a", 10, email_allowed=False), _slot("b", 60)], 80, "a") == "b"
    assert (
        pick_slot([{"tool": "codex", "slot": "a", "logged_in": True}, _slot("b", 1)], 80, None)
        == "b"
    )


def test_when_every_account_is_at_the_cap_nothing_runs_until_the_earliest_reset() -> None:
    with pytest.raises(RunRefused) as paused:
        pick_slot([_slot("a", 95, 10), _slot("b", 20, 85)], 80, "a")
    assert (paused.value.status, paused.value.code) == (429, "subscription_quota_paused")
    assert paused.value.extra["resets_at"] == "2026-09-25T10:00:00Z"
    with pytest.raises(RunRefused) as nobody:
        pick_slot([_slot("a", 10, logged_in=False)], 80, "a")
    assert nobody.value.code == "subscription_not_signed_in"


def test_a_run_has_no_tools_no_session_and_no_agent_secret(tmp_path: Path) -> None:
    config = _config(tmp_path)
    result = run_claude(config, "b", _request())
    assert result["text"] == '{"ok": true}' and result["slot"] == "b"
    assert (result["input_tokens"], result["output_tokens"], result["model"]) == (
        125,
        40,
        "claude-opus-5-5",
    )
    record = json.loads(
        (config.slot_path("claude", "b") / "last-run.json").read_text(encoding="utf-8")
    )
    args = record["args"]
    assert args[args.index("--tools") + 1] == "", "every built-in tool is off"
    assert {"-p", "--strict-mcp-config", "--no-session-persistence"} <= set(args)
    assert args[args.index("--model") + 1] == "claude-opus-5-5"
    assert record["prompt"] == '{"brief": "…"}' and record["system"] == "You are the fact-checker."
    assert record["env"]["CLAUDE_CONFIG_DIR"] == str(config.slot_path("claude", "b"))
    assert not any("HMAC" in name or KEY in value for name, value in record["env"].items())
    assert not any((config.state_root / "runs").iterdir()), "the run's folder is removed"


def test_a_spent_window_is_a_pause_and_a_crash_is_a_failure(tmp_path: Path) -> None:
    config = _config(tmp_path)
    with pytest.raises(RunRefused) as paused:
        run_claude(config, "a", _request("LIMIT"))
    assert paused.value.code == "subscription_quota_paused"
    with pytest.raises(CliError) as failed:
        run_claude(config, "a", _request("FAIL"))
    assert "overloaded" in str(failed.value)


class Accounts:
    """Claude slot a signed in near its cap, b with room; nothing is ever started."""

    def __init__(self, usage: dict[str, float]) -> None:
        self.usage = usage

    def status(self, slot: str) -> dict[str, Any]:
        signed = slot in self.usage
        return {"logged_in": signed, "auth_method": "claude.ai" if signed else None}

    def details(self, slot: str) -> dict[str, Any]:
        if slot not in self.usage:
            return {"usage": None}
        return {
            "usage": {
                "windows": [
                    {
                        "window_minutes": 300,
                        "used_percent": self.usage[slot],
                        "resets_at": "2026-09-25T12:00:00Z",
                    }
                ]
            }
        }

    def start_login(self, slot: str, finalize: Any) -> Any:
        raise AssertionError("no login")

    def logout(self, slot: str) -> None:
        raise AssertionError("no logout")

    def has_credentials(self, slot: str) -> bool:
        return slot in self.usage

    def refresh_usage(self, slot: str) -> bool:
        return True


def _signed(application: AgentApplication, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    body = json.dumps(payload).encode()
    timestamp, nonce = str(int(time.time())), uuid4().hex
    headers = {
        "X-Agent-Timestamp": timestamp,
        "X-Agent-Nonce": nonce,
        "X-Agent-Signature": signature_for(KEY, timestamp, nonce, "POST", "/v1/runs", body),
    }
    return application.handle("POST", "/v1/runs", body, headers)


def test_the_runs_route_picks_an_account_runs_once_and_pauses_when_all_are_spent(
    tmp_path: Path,
) -> None:
    config = _config(tmp_path)
    run = {
        "tool": "claude",
        "model": "claude-sonnet-5",
        "system": "Write.",
        "prompt": "x" * 200_000,
        "max_usage_percent": 80,
    }
    application = AgentApplication(config, claude=Accounts({"a": 95, "b": 20}), codex=Accounts({}))  # type: ignore[arg-type]
    status, body = _signed(application, run)
    assert status == 200 and body["slot"] == "b" and body["text"] == '{"ok": true}'
    full = AgentApplication(config, claude=Accounts({"a": 95, "b": 99}), codex=Accounts({}))  # type: ignore[arg-type]
    status, body = _signed(full, run)
    assert status == 429 and body["code"] == "subscription_quota_paused"
    assert body["resets_at"] == "2026-09-25T12:00:00Z"
    status, body = _signed(application, {**run, "tool": "codex"})
    assert status == 422 and body["code"] == "run_tool_not_offered"


def test_a_busy_account_is_waited_for_and_a_resting_one_counts_as_spent() -> None:
    assert pick_slot([_slot("a", 10), _slot("b", 50)], 80, "a", busy={"a"}) == "b"
    with pytest.raises(RunRefused) as busy:
        pick_slot([_slot("a", 10), _slot("b", 90)], 80, "a", busy={"a"})
    assert (busy.value.status, busy.value.code) == (503, "subscription_busy")
    with pytest.raises(RunRefused) as spent:
        pick_slot([_slot("a", 10)], 80, "a", resting={"a"})
    assert (spent.value.status, spent.value.code) == (429, "subscription_quota_paused")
    assert "resets_at" not in spent.value.extra, "no reset time is known for a resting account"
    assert pick_slot([_slot("a", 10), _slot("b", 60)], 80, "a", resting={"a"}) == "b"


def test_a_run_that_hits_the_limit_moves_on_to_the_next_account_and_rests_the_first(
    tmp_path: Path,
) -> None:
    config = _config(tmp_path)
    (config.slot_path("claude", "a") / "spent").write_text("", encoding="utf-8")
    run = {"tool": "claude", "model": "claude-opus-5-5", "system": "Write.", "prompt": "{}"}
    application = AgentApplication(config, claude=Accounts({"a": 10, "b": 20}), codex=Accounts({}))  # type: ignore[arg-type]
    status, body = _signed(application, run)
    assert status == 200 and body["slot"] == "b", "a had the most room but its run hit the limit"
    assert "a" in application._runs_resting and not application._runs_busy
    (config.slot_path("claude", "b") / "last-run.json").unlink()
    (config.slot_path("claude", "a") / "last-run.json").unlink()
    status, body = _signed(application, run)
    assert status == 200 and body["slot"] == "b"
    assert not (config.slot_path("claude", "a") / "last-run.json").exists(), "a is resting"


def test_a_request_gives_up_when_every_account_with_room_stays_busy(tmp_path: Path) -> None:
    config = _config(tmp_path)
    run = {
        "tool": "claude",
        "model": "claude-opus-5-5",
        "system": "Write.",
        "prompt": "{}",
        "queue_seconds": 0,
    }
    application = AgentApplication(config, claude=Accounts({"b": 20}), codex=Accounts({}))  # type: ignore[arg-type]
    application._runs_busy.add("b")
    status, body = _signed(application, run)
    assert (status, body["code"]) == (503, "subscription_busy")
    assert not (config.slot_path("claude", "b") / "last-run.json").exists()


def test_two_runs_on_different_accounts_go_side_by_side(tmp_path: Path) -> None:
    config = _config(tmp_path)
    application = AgentApplication(config, claude=Accounts({"a": 10, "b": 20}), codex=Accounts({}))  # type: ignore[arg-type]
    first = application._claim_run_slot(_request())
    second = application._claim_run_slot(_request())
    assert {first, second} == {"a", "b"}
    application._release_run_slot(first, spent=False)
    assert application._claim_run_slot(_request()) == first
