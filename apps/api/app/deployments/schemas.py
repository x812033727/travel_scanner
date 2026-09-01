from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

DeploymentStatus = Literal[
    "queued",
    "preflight",
    "building",
    "backing_up",
    "migrating",
    "activating",
    "verifying",
    "rolling_back",
    "succeeded",
    "failed",
    "rolled_back",
    "manual_intervention_required",
]


class DeploymentEventView(BaseModel):
    sequence: int
    stage: str
    status: str
    message: str
    created_at: datetime


class DeploymentRunView(BaseModel):
    id: UUID
    requested_by_email: str | None = None
    agent_job_id: str | None = None
    status: DeploymentStatus
    stage: str
    previous_sha: str | None = None
    target_sha: str
    target_commit_subject: str | None = None
    ci_url: str | None = None
    backup_name: str | None = None
    rollback_status: str | None = None
    failure_code: str | None = None
    failure_detail: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    events: list[DeploymentEventView] = Field(default_factory=list)


class CommitSummary(BaseModel):
    sha: str
    subject: str


class PreflightCheck(BaseModel):
    name: str
    status: Literal["ok", "warning", "failed"]
    detail: str


class AgentOverview(BaseModel):
    connected: bool = True
    deployed_sha: str | None = None
    target_sha: str | None = None
    target_commit_subject: str | None = None
    ci_status: str = "unknown"
    ci_url: str | None = None
    commits: list[CommitSummary] = Field(default_factory=list)
    checks: list[PreflightCheck] = Field(default_factory=list)


class AgentDeploymentEvent(BaseModel):
    sequence: int
    stage: str
    status: str
    message: str
    created_at: datetime


class AgentDeploymentJob(BaseModel):
    job_id: str
    status: DeploymentStatus
    stage: str
    previous_sha: str | None = None
    target_sha: str
    target_commit_subject: str | None = None
    ci_url: str | None = None
    backup_name: str | None = None
    rollback_status: str | None = None
    failure_code: str | None = None
    failure_detail: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    events: list[AgentDeploymentEvent] = Field(default_factory=list)


class DeploymentOverview(BaseModel):
    enabled: bool
    agent_connected: bool
    deployed_sha: str | None = None
    target_sha: str | None = None
    target_commit_subject: str | None = None
    update_available: bool = False
    ci_status: str = "unknown"
    ci_url: str | None = None
    commits: list[CommitSummary] = Field(default_factory=list)
    checks: list[PreflightCheck] = Field(default_factory=list)
    active_run: DeploymentRunView | None = None
    last_success: DeploymentRunView | None = None
    cooldown_until: datetime | None = None


class DeploymentCreateRequest(BaseModel):
    expected_target_sha: str = Field(min_length=40, max_length=40, pattern=r"^[0-9a-f]{40}$")
    password: str = Field(min_length=1, max_length=128)
    confirmation: str = Field(min_length=1, max_length=32)

    @field_validator("expected_target_sha")
    @classmethod
    def normalize_sha(cls, value: str) -> str:
        return value.lower()


class DeploymentPreflightResult(BaseModel):
    ok: bool
    checked_at: datetime
    checks: list[PreflightCheck]
    target_sha: str | None = None


class DeploymentRunList(BaseModel):
    items: list[DeploymentRunView]


class AgentCreateRequest(BaseModel):
    run_id: UUID
    target_sha: str


class AgentCreateResponse(BaseModel):
    job_id: str
    status: DeploymentStatus
