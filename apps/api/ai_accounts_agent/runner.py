import json
import os
import subprocess
from collections.abc import Mapping, Sequence
from typing import Any

from ai_accounts_agent.config import AgentConfig

SYSTEM_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"


class CliError(RuntimeError):
    """A CLI call failed; the message is already safe to show."""


def cli_environment(config: AgentConfig, extra: Mapping[str, str]) -> dict[str, str]:
    """Build the CLI environment from scratch.

    Nothing is inherited from the agent: its environment holds the HMAC key, and the CLIs
    have no business seeing it. HOME points at a directory the service may write, so a CLI
    that caches outside its config directory stays inside ReadWritePaths.
    """
    environment = {
        "PATH": SYSTEM_PATH,
        "HOME": str(config.home_path),
        "LANG": "C.UTF-8",
        "DISABLE_AUTOUPDATER": "1",
        "BROWSER": "/bin/false",
    }
    if os.name == "nt":  # The tests run fake CLIs through Python on Windows too.
        environment["SYSTEMROOT"] = os.environ.get("SYSTEMROOT", "")
    environment.update(extra)
    return environment


def run_cli(
    command: Sequence[str], environment: Mapping[str, str], timeout: float
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(  # noqa: S603 - fixed argv from the agent config, shell=False
            list(command),
            env=dict(environment),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise CliError(f"{os.path.basename(command[-1])} did not answer in time") from exc
    except OSError as exc:
        raise CliError(f"cannot start {os.path.basename(command[0])}: {exc.strerror}") from exc


def parse_json_object(text: str) -> dict[str, Any] | None:
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        return None
    try:
        value = json.loads(text[start : end + 1])
    except ValueError:
        return None
    return value if isinstance(value, dict) else None


def text_or_none(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    return value.strip() or None
