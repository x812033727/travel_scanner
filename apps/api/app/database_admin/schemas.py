from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

DatabaseOperationType = Literal["backup", "analyze"]
DatabaseOperationStatus = Literal["queued", "running", "succeeded", "failed"]
CheckStatus = Literal["ok", "warning", "failed"]
DatabaseBackupSource = Literal["manual", "deployment"]


class DatabaseAgentCheck(BaseModel):
    name: str
    status: CheckStatus
    detail: str


class DatabaseOperationEvent(BaseModel):
    sequence: int
    status: str
    message: str
    created_at: datetime


class AgentDatabaseJob(BaseModel):
    job_id: str
    action: DatabaseOperationType
    status: DatabaseOperationStatus
    backup_name: str | None = None
    checksum_sha256: str | None = None
    size_bytes: int | None = None
    schema_revision: str | None = None
    release_sha: str | None = None
    failure_code: str | None = None
    failure_detail: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    created_at: datetime
    events: list[DatabaseOperationEvent] = Field(default_factory=list)


class AgentVerifiedBackup(BaseModel):
    backup_name: str = Field(min_length=1, max_length=255)
    checksum_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    size_bytes: int = Field(gt=0)
    schema_revision: str = Field(min_length=1, max_length=64)
    release_sha: str = Field(pattern=r"^[0-9a-f]{40}$")
    source: DatabaseBackupSource
    source_job_id: UUID | None = None
    verified_at: datetime


class AgentDatabaseOverview(BaseModel):
    connected: bool = True
    available: bool = False
    release_sha: str | None = None
    checks: list[DatabaseAgentCheck] = Field(default_factory=list)
    active_job: AgentDatabaseJob | None = None
    backups: list[AgentVerifiedBackup] = Field(default_factory=list)


class AgentDatabaseCreateRequest(BaseModel):
    run_id: UUID
    action: DatabaseOperationType


class AgentDatabaseCreateResponse(BaseModel):
    job_id: str
    status: DatabaseOperationStatus


class DatabaseConnections(BaseModel):
    active: int
    idle: int
    waiting: int
    maximum: int


class PostgreSQLSnapshot(BaseModel):
    version: str
    database_size_bytes: int
    connections: DatabaseConnections
    long_transactions: int
    lock_waits: int
    cache_hit_ratio: float | None = None


class DatabaseSchemaSnapshot(BaseModel):
    current_revision: str | None = None
    expected_revision: str
    is_current: bool


class DatabaseOperationView(BaseModel):
    id: UUID
    requested_by_email: str | None = None
    operation_type: DatabaseOperationType
    status: DatabaseOperationStatus
    agent_job_id: str | None = None
    backup_name: str | None = None
    checksum_sha256: str | None = None
    size_bytes: int | None = None
    schema_revision: str | None = None
    release_sha: str | None = None
    failure_code: str | None = None
    failure_detail: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    events: list[DatabaseOperationEvent] = Field(default_factory=list)
    source: DatabaseBackupSource = "manual"
    verified: bool = False


class DatabaseOverview(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    status: Literal["ok", "unavailable"]
    checked_at: datetime
    postgres: PostgreSQLSnapshot | None = None
    schema_info: DatabaseSchemaSnapshot | None = Field(default=None, alias="schema")
    agent: AgentDatabaseOverview
    maintenance_enabled: bool
    retention_count: int = 7
    last_backup: DatabaseOperationView | None = None
    active_operation: DatabaseOperationView | None = None
    unavailable_reason: str | None = None


class DatabaseTableSnapshot(BaseModel):
    name: str
    estimated_rows: int
    data_bytes: int
    index_bytes: int
    total_bytes: int
    dead_rows: int
    last_vacuum: datetime | None = None
    last_autovacuum: datetime | None = None
    last_analyze: datetime | None = None
    last_autoanalyze: datetime | None = None


class DatabaseTableList(BaseModel):
    items: list[DatabaseTableSnapshot]


class DatabaseOperationList(BaseModel):
    items: list[DatabaseOperationView]


class DatabaseBackupRequest(BaseModel):
    confirmation: str = Field(min_length=1, max_length=32)


class DatabaseMaintenanceRequest(BaseModel):
    action: Literal["analyze"]
    confirmation: str = Field(min_length=1, max_length=32)
