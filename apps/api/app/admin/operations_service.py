from __future__ import annotations

import asyncio
import json
import math
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from redis.exceptions import RedisError
from sqlalchemy import Select, String, func, not_, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.audit_safety import safe_audit_metadata
from app.admin.operations_schemas import (
    AdminAuditItem,
    AdminAuditPage,
    AdminBootstrap,
    AdminBootstrapActor,
    AdminNavigationItem,
    AdminSystemComponent,
)
from app.auth.service import (
    can_database_maintain_user,
    can_deploy_user,
    effective_admin_capabilities,
    effective_admin_roles,
)
from app.community.models import Job
from app.config import get_settings
from app.database_admin.agent import DatabaseAgentClient
from app.deployments.agent import DeploymentAgentClient
from app.infra import get_redis
from app.models import (
    ACTIVE_DEPLOYMENT_STATUSES,
    AdminAuditLog,
    DeploymentRun,
    FoodMerchant,
    HotspotGuide,
    ProviderHealth,
    TravelFood,
    TravelHotspot,
    TravelServiceProduct,
    User,
)
from app.problems import AppError
from app.schema import expected_schema_revision

NAVIGATION_REGISTRY: tuple[AdminNavigationItem, ...] = (
    AdminNavigationItem(
        id="dashboard", group="overview", href="/admin", label_key="dashboard",
        capability="dashboard.read",
    ),
    # First-party travel intel and guides (guide_articles). No badge: ``guides_pending``
    # counts third-party HotspotGuide links, which belong to the hotspots workspace.
    AdminNavigationItem(
        id="guides", group="content", href="/admin/guides", label_key="guides",
        capability="content.read",
    ),
    AdminNavigationItem(
        id="hotspots", group="content", href="/admin/hotspots", label_key="hotspots",
        capability="content.read", badge_key="hotspots_pending",
    ),
    AdminNavigationItem(
        id="foods", group="content", href="/admin/foods", label_key="foods",
        capability="content.read", badge_key="foods_pending",
    ),
    AdminNavigationItem(
        id="hotels", group="content", href="/admin/hotels", label_key="hotels",
        capability="content.read", badge_key="hotels_pending",
    ),
    AdminNavigationItem(
        id="travel_services", group="content", href="/admin/travel-services",
        label_key="travelServices", capability="content.read",
    ),
    AdminNavigationItem(
        id="catalog_review", group="content", href="/admin/catalog-review",
        label_key="catalogReview", capability="content.read",
    ),
    AdminNavigationItem(
        id="community", group="community", href="/admin/community", label_key="community",
        capability="community.read", badge_key="community_jobs_pending",
    ),
    AdminNavigationItem(
        id="pet_friendly", group="community", href="/admin/pet-friendly",
        label_key="petFriendly", capability="community.read",
    ),
    AdminNavigationItem(
        id="users", group="operations", href="/admin/users", label_key="users",
        capability="users.read",
    ),
    AdminNavigationItem(
        id="analytics", group="operations", href="/admin/analytics", label_key="analytics",
        capability="analytics.read",
    ),
    AdminNavigationItem(
        id="partners", group="operations", href="/admin/partners", label_key="partners",
        capability="content.read",
    ),
    AdminNavigationItem(
        id="provider_settings", group="operations", href="/admin/settings",
        label_key="providerSettings", capability="settings.read",
    ),
    AdminNavigationItem(
        id="usage_settings", group="operations", href="/admin/usage-settings",
        label_key="usageSettings", capability="settings.read",
    ),
    AdminNavigationItem(
        id="layout_settings", group="operations", href="/admin/layout-settings",
        label_key="layoutSettings", capability="settings.read",
    ),
    AdminNavigationItem(
        id="ui_text", group="operations", href="/admin/ui-text", label_key="uiText",
        capability="settings.read",
    ),
    AdminNavigationItem(
        id="site_pages", group="operations", href="/admin/site-pages", label_key="sitePages",
        capability="settings.read",
    ),
    AdminNavigationItem(
        id="system_settings", group="system", href="/admin/system-settings",
        label_key="systemSettings", capability="settings.read",
    ),
    AdminNavigationItem(
        id="database", group="system", href="/admin/database", label_key="database",
        capability="database.read",
    ),
    AdminNavigationItem(
        id="deployments", group="system", href="/admin/deployments", label_key="deployments",
        capability="deploy.read",
    ),
    AdminNavigationItem(
        id="audit", group="system", href="/admin/audit", label_key="audit",
        capability="audit.read",
    ),
)


def _scalar_count(model: type[Any], *criteria: Any) -> Any:
    return select(func.count()).select_from(model).where(*criteria).scalar_subquery()


async def _live_pending_counts(session: AsyncSession) -> dict[str, int]:
    # One round trip keeps the operations landing page fast even as domains grow.
    statement = select(
        _scalar_count(User).label("users"),
        _scalar_count(TravelHotspot, TravelHotspot.review_status == "pending").label(
            "hotspots_pending"
        ),
        _scalar_count(TravelFood, TravelFood.review_status == "pending").label("foods_pending"),
        _scalar_count(FoodMerchant, FoodMerchant.review_status == "pending").label(
            "merchants_pending"
        ),
        _scalar_count(HotspotGuide, HotspotGuide.review_status == "pending").label(
            "guides_pending"
        ),
        _scalar_count(
            TravelServiceProduct,
            TravelServiceProduct.kind == "hotel",
            TravelServiceProduct.status == "pending",
        ).label("hotels_pending"),
        _scalar_count(Job, Job.status == "pending").label("community_jobs_pending"),
        _scalar_count(
            DeploymentRun, DeploymentRun.status.in_(ACTIVE_DEPLOYMENT_STATUSES)
        ).label("deployments_active"),
        _scalar_count(ProviderHealth, ProviderHealth.status != "healthy").label(
            "providers_unhealthy"
        ),
    )
    values = {
        key: int(value or 0)
        for key, value in (await session.execute(statement)).mappings().one().items()
    }
    values["users_total"] = values["users"]
    values["pending_total"] = sum(
        values[key]
        for key in (
            "hotspots_pending",
            "foods_pending",
            "merchants_pending",
            "guides_pending",
            "hotels_pending",
        )
    )
    values["jobs_active"] = values["community_jobs_pending"]
    values["alerts_total"] = values["providers_unhealthy"]
    return values


async def pending_counts(session: AsyncSession) -> dict[str, int]:
    redis = get_redis()
    cache_key = "admin:operations:pending:v1"
    try:
        cached = await redis.get(cache_key)
        if cached:
            parsed = json.loads(cached)
            if isinstance(parsed, dict):
                return {str(key): int(value) for key, value in parsed.items()}
    except (RedisError, ValueError, TypeError):
        pass
    values = await _live_pending_counts(session)
    try:
        await redis.set(cache_key, json.dumps(values, separators=(",", ":")), ex=15)
    except RedisError:
        pass
    return values


async def _system_status(
    session: AsyncSession, pending: dict[str, int]
) -> dict[str, AdminSystemComponent]:
    settings = get_settings()
    current_revision = await session.scalar(text("SELECT version_num FROM alembic_version"))
    expected = expected_schema_revision()
    database = AdminSystemComponent(
        status="healthy" if current_revision == expected else "degraded",
        detail=f"schema {current_revision or 'none'} / {expected}",
    )
    try:
        await asyncio.wait_for(get_redis().ping(), timeout=1.5)
        redis = AdminSystemComponent(status="healthy")
    except (TimeoutError, RedisError):
        redis = AdminSystemComponent(status="unavailable", detail="Redis 無法連線")
    providers = AdminSystemComponent(
        status="healthy" if not pending.get("providers_unhealthy") else "degraded",
        detail=(
            None
            if not pending.get("providers_unhealthy")
            else f"{pending['providers_unhealthy']} 個 Provider 需檢查"
        ),
    )
    if not settings.deployments_configured:
        deployment = AdminSystemComponent(
            status="disabled", detail="部署功能尚未完成設定"
        )
    else:
        try:
            deployment_agent = await DeploymentAgentClient().overview()
        except AppError:
            deployment = AdminSystemComponent(
                status="unavailable", detail="部署 Agent 無法連線"
            )
        else:
            if not deployment_agent.connected:
                deployment = AdminSystemComponent(
                    status="unavailable", detail="部署 Agent 無法連線"
                )
            else:
                unhealthy_checks = [
                    check for check in deployment_agent.checks if check.status != "ok"
                ]
                deployment = AdminSystemComponent(
                    status="degraded" if unhealthy_checks else "healthy",
                    detail=(
                        f"{pending.get('deployments_active', 0)} 個部署進行中"
                        if pending.get("deployments_active")
                        else (
                            f"{len(unhealthy_checks)} 項主機檢查需注意"
                            if unhealthy_checks
                            else f"目前版本 {(deployment_agent.deployed_sha or 'unknown')[:7]}"
                        )
                    ),
                )
    queued_jobs = pending.get("community_jobs_pending", 0)
    jobs = AdminSystemComponent(
        status="degraded" if queued_jobs >= 100 else "healthy",
        detail=f"{queued_jobs} 個背景工作等待中",
    )
    agent_transport_configured = bool(
        settings.deploy_agent_hmac_key
        and len(settings.deploy_agent_hmac_key) >= 32
        and settings.deploy_agent_socket.startswith("/")
    )
    if not agent_transport_configured:
        backup = AdminSystemComponent(
            status="disabled", detail="資料庫備份 Agent 尚未設定"
        )
    else:
        try:
            database_agent = await DatabaseAgentClient().overview()
        except AppError:
            backup = AdminSystemComponent(
                status="unavailable", detail="資料庫備份 Agent 無法連線"
            )
        else:
            latest_backup = max(
                database_agent.backups,
                key=lambda item: item.verified_at,
                default=None,
            )
            if not database_agent.connected or not database_agent.available:
                backup = AdminSystemComponent(
                    status="unavailable", detail="資料庫備份 Agent 尚未就緒"
                )
            elif latest_backup is None:
                backup = AdminSystemComponent(
                    status="degraded", detail="尚無已驗證的資料庫備份"
                )
            else:
                source = "部署" if latest_backup.source == "deployment" else "手動"
                verified_at = latest_backup.verified_at.astimezone(UTC).strftime(
                    "%Y-%m-%d %H:%M UTC"
                )
                backup = AdminSystemComponent(
                    status="healthy",
                    detail=f"最近已驗證備份：{source} / {verified_at}",
                )
    return {
        "database": database,
        "redis": redis,
        "providers": providers,
        "background_jobs": jobs,
        "deployment": deployment,
        "backup": backup,
    }


async def admin_bootstrap(session: AsyncSession, actor: User) -> AdminBootstrap:
    # AsyncSession does not permit concurrent statements on one connection.
    roles = await effective_admin_roles(session, actor)
    capabilities = await effective_admin_capabilities(session, actor)
    pending = await pending_counts(session)
    navigation = [item for item in NAVIGATION_REGISTRY if item.capability in capabilities]
    system = await _system_status(session, pending)
    return AdminBootstrap(
        actor=AdminBootstrapActor(
            id=actor.id,
            email=actor.email,
            roles=sorted(roles),
            capabilities=sorted(capabilities),
        ),
        environment=get_settings().app_env,
        navigation=navigation,
        pending=pending,
        system=system,
        can_deploy=can_deploy_user(actor, roles=roles),
        can_manage_database=can_database_maintain_user(actor, roles=roles),
        generated_at=datetime.now(UTC),
    )


def _audit_query(
    *,
    actor: str | None,
    action: str | None,
    target: str | None,
    result: str | None,
    date_from: datetime | None,
    date_to: datetime | None,
) -> Select[tuple[AdminAuditLog, str]]:
    statement = select(AdminAuditLog, User.email).outerjoin(
        User, User.id == AdminAuditLog.actor_user_id
    )
    if actor:
        escaped = actor.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        statement = statement.where(
            or_(
                User.email.ilike(f"%{escaped}%", escape="\\"),
                func.cast(AdminAuditLog.actor_user_id, String).ilike(
                    f"%{escaped}%", escape="\\"
                ),
            )
        )
    if action:
        statement = statement.where(AdminAuditLog.action == action)
    if target:
        escaped = target.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        statement = statement.where(AdminAuditLog.target.ilike(f"%{escaped}%", escape="\\"))
    if result:
        stored_result = func.lower(
            func.coalesce(
                AdminAuditLog.metadata_json["result"].as_string(),
                AdminAuditLog.metadata_json["status"].as_string(),
                "",
            )
        )
        failed = or_(
            stored_result.in_(("failed", "failure", "error", "denied")),
            AdminAuditLog.action.ilike("%failed%"),
            AdminAuditLog.action.ilike("%failure%"),
            AdminAuditLog.action.ilike("%denied%"),
            AdminAuditLog.action.ilike("%rolled_back%"),
            AdminAuditLog.action.ilike("%manual_intervention%"),
        )
        statement = statement.where(failed if result == "failed" else not_(failed))
    if date_from:
        statement = statement.where(AdminAuditLog.created_at >= date_from)
    if date_to:
        statement = statement.where(AdminAuditLog.created_at <= date_to)
    return statement


# Compatibility seam for focused tests and any internal imports written before
# the sanitizer became shared with the user-detail endpoint.
_safe_audit_metadata = safe_audit_metadata


def _audit_result(action: str, metadata: dict[str, object]) -> str:
    stored = str(metadata.get("result") or metadata.get("status") or "").lower()
    if stored in {"failed", "failure", "error", "denied"}:
        return "failed"
    if stored in {"succeeded", "success", "ok"}:
        return "succeeded"
    lowered = action.lower()
    if any(
        marker in lowered
        for marker in ("failed", "failure", "denied", "rolled_back", "manual_intervention")
    ):
        return "failed"
    return "succeeded"


def _audit_item(audit: AdminAuditLog, actor_email: str | None) -> AdminAuditItem:
    safe_metadata = safe_audit_metadata(dict(audit.metadata_json or {}))
    metadata = safe_metadata if isinstance(safe_metadata, dict) else {}
    result_value = _audit_result(audit.action, metadata)
    metadata.pop("result", None)
    return AdminAuditItem(
        id=audit.id,
        actor_user_id=audit.actor_user_id,
        actor_email=actor_email,
        action=audit.action,
        target=audit.target,
        result=result_value,
        metadata=metadata,
        created_at=audit.created_at,
    )


async def get_audit_log(session: AsyncSession, event_id: UUID) -> AdminAuditItem:
    row = (
        await session.execute(
            select(AdminAuditLog, User.email)
            .outerjoin(User, User.id == AdminAuditLog.actor_user_id)
            .where(AdminAuditLog.id == event_id)
        )
    ).one_or_none()
    if row is None:
        raise AppError(404, "admin_audit_event_not_found", "找不到這筆稽核事件")
    audit, actor_email = row
    return _audit_item(audit, actor_email)


async def list_audit_logs(
    session: AsyncSession,
    *,
    actor: str | None,
    action: str | None,
    target: str | None,
    result: str | None,
    date_from: datetime | None,
    date_to: datetime | None,
    page: int,
    limit: int,
) -> AdminAuditPage:
    query = _audit_query(
        actor=actor,
        action=action,
        target=target,
        result=result,
        date_from=date_from,
        date_to=date_to,
    )
    total = int(await session.scalar(select(func.count()).select_from(query.subquery())) or 0)
    rows = (
        await session.execute(
            query.order_by(AdminAuditLog.created_at.desc(), AdminAuditLog.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )
    ).all()
    items = [_audit_item(audit, email) for audit, email in rows]
    return AdminAuditPage(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=max(1, math.ceil(total / limit)),
    )
