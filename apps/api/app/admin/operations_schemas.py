from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class AdminNavigationItem(BaseModel):
    id: str
    group: Literal["overview", "content", "community", "operations", "system"]
    href: str
    label_key: str
    capability: str
    badge_key: str | None = None


class AdminBootstrapActor(BaseModel):
    id: UUID
    email: str
    roles: list[str]
    capabilities: list[str]


class AdminSystemComponent(BaseModel):
    status: Literal["healthy", "degraded", "unavailable", "disabled"]
    detail: str | None = None


class AdminBootstrap(BaseModel):
    actor: AdminBootstrapActor
    environment: str
    navigation: list[AdminNavigationItem]
    pending: dict[str, int]
    system: dict[str, AdminSystemComponent]
    can_deploy: bool = False
    can_manage_database: bool = False
    generated_at: datetime


class AdminAuditItem(BaseModel):
    id: UUID
    actor_user_id: UUID | None
    actor_email: str | None
    action: str
    target: str
    result: str
    metadata: dict[str, object]
    created_at: datetime


class AdminAuditPage(BaseModel):
    items: list[AdminAuditItem]
    total: int
    page: int
    limit: int
    pages: int


class AdminAuditFilters(BaseModel):
    actors: list[str] = Field(default_factory=list)
    actions: list[str] = Field(default_factory=list)
    targets: list[str] = Field(default_factory=list)
