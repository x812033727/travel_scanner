import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_SOCKET_PATH = Path("/run/mokaair-ai-accounts/agent.sock")
DEFAULT_STATE_ROOT = Path("/var/lib/mokaair-ai-accounts")
DEFAULT_CLAUDE_BIN = "/root/.local/bin/claude"
DEFAULT_CODEX_BIN = "/usr/local/bin/codex"
DEFAULT_AGY_BIN = "/root/.local/bin/agy"
# Installed by ops/ai-accounts/install.sh; runs statusline.py with the host python3.
STATUSLINE_RECORDER = "/usr/local/lib/mokaair-ai-accounts/statusline-record"

TOOLS: tuple[str, ...] = ("claude", "codex", "agy")
# Up to five accounts per tool; the page lists the signed-in ones and offers the next
# free slot for another.
SLOTS: tuple[str, ...] = ("a", "b", "c", "d", "e")


def parse_emails(value: str) -> frozenset[str]:
    return frozenset(item.strip().lower() for item in value.split(",") if item.strip())


@dataclass(frozen=True)
class AgentConfig:
    hmac_key: str
    socket_path: Path = DEFAULT_SOCKET_PATH
    state_root: Path = DEFAULT_STATE_ROOT
    # Commands are argument prefixes rather than paths so the tests can run a fake CLI
    # through the current interpreter on any platform.
    claude_command: tuple[str, ...] = (DEFAULT_CLAUDE_BIN,)
    codex_command: tuple[str, ...] = (DEFAULT_CODEX_BIN,)
    agy_command: tuple[str, ...] = (DEFAULT_AGY_BIN,)
    statusline_command: str = STATUSLINE_RECORDER
    # Accounts a login may end on. Empty means any; the host keeps this list, so a
    # compromised API container cannot sign root's CLIs into an account of its own.
    allowed_emails: frozenset[str] = field(default_factory=frozenset)
    login_ttl_seconds: float = 900.0
    url_timeout_seconds: float = 10.0
    command_timeout_seconds: float = 8.0
    code_exchange_timeout_seconds: float = 90.0
    claude_cache_seconds: float = 30.0
    # Reading Codex limits can refresh the account's tokens; doing that every minute next
    # to an interactive session invites "refresh token already used", so read it rarely.
    codex_cache_seconds: float = 300.0
    # The Antigravity status comes from files, so it is cheap to read.
    agy_cache_seconds: float = 30.0
    # Claude usage comes from a short interactive session (see ClaudeAccounts.refresh_usage).
    # A page view starts one when the snapshot is older than max_age; the refresh button
    # can start one sooner, but never more than once per min_interval; a probe that found
    # nothing is not retried by page views for retry.
    claude_usage_max_age_seconds: float = 1800.0
    claude_usage_min_interval_seconds: float = 60.0
    claude_usage_retry_seconds: float = 300.0
    # How long a probe waits for the status line before sending one message, and after it.
    claude_usage_quiet_seconds: float = 15.0
    claude_usage_message_seconds: float = 40.0
    # agy starts a language server before its TUI; on the host the sign-in URL is there in
    # under a second. The wait must stay under the API's agent timeout (25 s): a login that
    # never shows a URL then ends as this agent's error, not as a 503 for the page. The probe
    # lets the TUI settle, opens the quota page, and gives the page a moment to reload the
    # numbers before reading it.
    agy_start_timeout_seconds: float = 15.0
    agy_usage_start_seconds: float = 4.0
    agy_usage_page_seconds: float = 2.0
    agy_usage_timeout_seconds: float = 60.0

    @property
    def home_path(self) -> Path:
        return self.state_root / "home"

    @property
    def usage_probe_path(self) -> Path:
        # One folder for every probe, so Claude asks to trust it once per account.
        return self.home_path / "usage-probe"

    def slot_path(self, tool: str, slot: str) -> Path:
        if tool not in TOOLS or slot not in SLOTS:
            raise ValueError(f"unknown account slot {tool}-{slot}")
        return self.state_root / f"{tool}-{slot}"

    def default_path(self, tool: str) -> Path:
        if tool not in TOOLS:
            raise ValueError(f"unknown tool {tool}")
        return self.state_root / f"default-{tool}"

    def recorder_for(self, slot: str) -> str:
        return f"{self.statusline_command} claude-{slot}"

    @classmethod
    def from_env(cls) -> "AgentConfig":
        key = os.environ.get("AI_ACCOUNTS_AGENT_HMAC_KEY", "")
        if len(key) < 32:
            raise RuntimeError("AI_ACCOUNTS_AGENT_HMAC_KEY must contain at least 32 characters")
        # The socket and state paths are fixed by the systemd unit (ReadWritePaths) and the
        # Compose mount; an override would only make the three disagree.
        for name, fixed in (
            ("AI_ACCOUNTS_AGENT_SOCKET", DEFAULT_SOCKET_PATH),
            ("AI_ACCOUNTS_STATE_ROOT", DEFAULT_STATE_ROOT),
        ):
            value = os.environ.get(name)
            if value is not None and Path(value) != fixed:
                raise RuntimeError(f"{name} is fixed by systemd at {fixed}")
        claude_bin = os.environ.get("AI_ACCOUNTS_CLAUDE_BIN", DEFAULT_CLAUDE_BIN)
        codex_bin = os.environ.get("AI_ACCOUNTS_CODEX_BIN", DEFAULT_CODEX_BIN)
        agy_bin = os.environ.get("AI_ACCOUNTS_AGY_BIN", DEFAULT_AGY_BIN)
        for binary in (claude_bin, codex_bin, agy_bin):
            if not binary.startswith("/"):
                raise RuntimeError(f"CLI paths must be absolute: {binary}")
        return cls(
            hmac_key=key,
            claude_command=(claude_bin,),
            codex_command=(codex_bin,),
            agy_command=(agy_bin,),
            allowed_emails=parse_emails(os.environ.get("AI_ACCOUNTS_ALLOWED_EMAILS", "")),
        )
