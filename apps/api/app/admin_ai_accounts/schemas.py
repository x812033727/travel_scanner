from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Tool = Literal["claude", "codex"]
Slot = Literal["a", "b", "c", "d", "e"]
LoginStatus = Literal["pending", "verifying", "succeeded", "failed", "cancelled", "expired"]
TERMINAL_LOGIN_STATUSES: frozenset[str] = frozenset({"succeeded", "failed", "cancelled", "expired"})


class _AgentModel(BaseModel):
    # Whatever else the agent may add never reaches the browser.
    model_config = ConfigDict(extra="ignore")


class AiUsageWindow(_AgentModel):
    window_minutes: int | None = None
    used_percent: float = Field(ge=0, le=100)
    resets_at: int | None = None


class AiUsage(_AgentModel):
    source: Literal["live", "snapshot"]
    recorded_at: int | None = None
    windows: list[AiUsageWindow] = Field(default_factory=list)


class AiLoginSession(_AgentModel):
    id: str = Field(pattern=r"^[0-9a-f]{32}$")
    tool: Tool
    slot: Slot
    kind: Literal["device_code", "paste_code"]
    status: LoginStatus
    url: str | None = Field(default=None, max_length=4096)
    user_code: str | None = Field(default=None, max_length=64)
    error: str | None = Field(default=None, max_length=500)
    expires_at: int


class AiAccountSlot(_AgentModel):
    tool: Tool
    slot: Slot
    is_default: bool
    logged_in: bool | None = None
    auth_method: str | None = Field(default=None, max_length=64)
    email: str | None = Field(default=None, max_length=320)
    organization: str | None = Field(default=None, max_length=255)
    plan: str | None = Field(default=None, max_length=64)
    email_allowed: bool | None = None
    usage: AiUsage | None = None
    usage_error: str | None = Field(default=None, max_length=500)
    recorder_installed: bool | None = None
    checked_at: int | None = None
    error: str | None = Field(default=None, max_length=500)
    login: AiLoginSession | None = None


class AgentOverview(_AgentModel):
    slots: list[AiAccountSlot]
    defaults: dict[Tool, Slot]
    allowlist_configured: bool


class AiAccountsOverview(BaseModel):
    enabled: bool
    agent_reachable: bool
    agent_error: str | None = None
    slots: list[AiAccountSlot] = Field(default_factory=list)
    defaults: dict[Tool, Slot] = Field(default_factory=dict)
    allowlist_configured: bool = False


class AiLoginCodeRequest(BaseModel):
    # What the Claude callback page shows: base64url pieces joined by `#`. The agent checks
    # the same pattern before it types anything into the CLI.
    code: str = Field(min_length=10, max_length=1024, pattern=r"^\s*[A-Za-z0-9._~#-]+\s*$")


class AiDefaultRequest(BaseModel):
    slot: Slot


class AiDefaults(_AgentModel):
    defaults: dict[Tool, Slot]


class AiLogoutResult(_AgentModel):
    tool: Tool
    slot: Slot
    logged_in: bool
