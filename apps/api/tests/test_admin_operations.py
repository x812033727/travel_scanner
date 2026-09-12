from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.admin import operations_router, operations_service
from app.admin.operations_schemas import AdminAuditItem, AdminAuditPage
from app.auth.service import current_user
from app.database_admin.schemas import AgentDatabaseOverview, AgentVerifiedBackup
from app.db import get_session
from app.deployments.schemas import AgentOverview
from app.models import AdminAuditLog, User
from app.problems import AppError, app_error_handler


def test_navigation_registry_has_stable_unique_destinations() -> None:
    ids = [item.id for item in operations_service.NAVIGATION_REGISTRY]
    hrefs = [item.href for item in operations_service.NAVIGATION_REGISTRY]

    assert len(ids) == len(set(ids))
    assert len(hrefs) == len(set(hrefs))
    assert "/admin/database" in hrefs
    assert "/admin/audit" in hrefs
    # The web fallback list has carried /admin/guides since PR #398, but the layout trusts
    # this registry whenever the API answers, so a missing row made the page "forbidden".
    assert "/admin/guides" in hrefs
    assert all(item.href.startswith("/admin") for item in operations_service.NAVIGATION_REGISTRY)


def test_audit_metadata_redacts_nested_credentials_and_bounds_values() -> None:
    result = operations_service._safe_audit_metadata(  # noqa: SLF001
        {
            "status": "ok",
            "token": "never expose",
            "nested": {
                "api_secret": "never expose either",
                "detail": "Authorization: Bearer exposed-value " + "x" * 1200,
                "dsn": "postgresql://travel:database-secret@postgres/db",
                "jwt": (
                    "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0."
                    "signature0123456789"
                ),
                "assignment": "api-key=exposed-api-key",
            },
            "events": list(range(120)),
        }
    )

    assert result == {
        "status": "ok",
        "nested": {
            "detail": "Authorization: *** " + "x" * 981,
            "dsn": "postgresql://travel:***@postgres/db",
            "jwt": "***",
            "assignment": "api-key=***",
        },
        "events": list(range(100)),
    }


@pytest.mark.parametrize(
    ("action", "metadata", "expected"),
    [
        ("user_roles_updated", {}, "succeeded"),
        ("database.operation.failed", {}, "failed"),
        ("deployment.rolled_back", {}, "failed"),
        ("provider.test", {"result": "failure"}, "failed"),
        ("provider.test", {"result": "success"}, "succeeded"),
        ("provider_connection_tested", {"status": "failed"}, "failed"),
        ("provider_connection_tested", {"status": "success"}, "succeeded"),
    ],
)
def test_audit_result_is_truthful_for_legacy_and_explicit_events(
    action: str, metadata: dict[str, object], expected: str
) -> None:
    assert operations_service._audit_result(action, metadata) == expected  # noqa: SLF001


@pytest.mark.asyncio
async def test_audit_detail_is_sanitized_and_missing_is_404() -> None:
    event_id = uuid4()
    audit = AdminAuditLog(
        id=event_id,
        actor_user_id=None,
        action="provider.test",
        target="provider:maps",
        metadata_json={
            "result": "failure",
            "detail": "visible",
            "access_token": "must-not-leak",
            "nested": {"client_secret": "must-not-leak", "count": 2},
        },
        created_at=datetime.now(UTC),
    )
    result = Mock()
    result.one_or_none.return_value = (audit, "operator@example.com")
    session = AsyncMock()
    session.execute.return_value = result

    item = await operations_service.get_audit_log(session, event_id)

    assert item.result == "failed"
    assert item.actor_email == "operator@example.com"
    assert item.metadata == {"detail": "visible", "nested": {"count": 2}}
    result.one_or_none.return_value = None
    with pytest.raises(AppError) as missing:
        await operations_service.get_audit_log(session, uuid4())
    assert missing.value.status == 404
    assert missing.value.code == "admin_audit_event_not_found"


@pytest.mark.asyncio
async def test_audit_detail_route_requires_audit_capability(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_id = uuid4()
    holder = {"user": User(id=uuid4(), email="user@example.com", password_hash="unused")}

    async def override_user() -> User:
        return holder["user"]

    async def override_session() -> Any:
        yield AsyncMock()

    item = AdminAuditItem(
        id=event_id,
        actor_user_id=None,
        actor_email=None,
        action="database.operation.succeeded",
        target="backup:test",
        result="succeeded",
        metadata={},
        created_at=datetime.now(UTC),
    )
    detail = AsyncMock(return_value=item)
    monkeypatch.setattr(operations_router, "get_audit_log", detail)
    application = FastAPI()
    application.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    application.include_router(operations_router.router, prefix="/api/v1")
    application.dependency_overrides[current_user] = override_user
    application.dependency_overrides[get_session] = override_session

    async with AsyncClient(
        transport=ASGITransport(app=application), base_url="http://test"
    ) as client:
        forbidden = await client.get(f"/api/v1/admin/audit/{event_id}")
        assert forbidden.status_code == 403
        holder["user"]._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
        allowed = await client.get(f"/api/v1/admin/audit/{event_id}")

    assert allowed.status_code == 200
    assert allowed.json()["id"] == str(event_id)
    detail.assert_awaited_once()


@pytest.mark.asyncio
async def test_audit_list_rejects_naive_dates_and_normalizes_aware_boundaries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
    user._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]

    async def override_user() -> User:
        return user

    async def override_session() -> Any:
        yield AsyncMock()

    listing = AsyncMock(
        return_value=AdminAuditPage(items=[], total=0, page=1, limit=50, pages=0)
    )
    monkeypatch.setattr(operations_router, "list_audit_logs", listing)
    application = FastAPI()
    application.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    application.include_router(operations_router.router, prefix="/api/v1")
    application.dependency_overrides[current_user] = override_user
    application.dependency_overrides[get_session] = override_session

    async with AsyncClient(
        transport=ASGITransport(app=application), base_url="http://test"
    ) as client:
        naive = await client.get(
            "/api/v1/admin/audit?date_from=2026-09-01T00:00:00"
        )
        mixed = await client.get(
            "/api/v1/admin/audit?date_from=2026-09-01T00:00:00&date_to=2026-09-02T00:00:00Z"
        )
        aware = await client.get(
            "/api/v1/admin/audit?date_from=2026-09-01T08:00:00%2B08:00&date_to=2026-09-02T08:00:00%2B08:00"
        )

    assert naive.status_code == 422
    assert naive.json()["code"] == "audit_timezone_required"
    assert mixed.status_code == 422
    assert mixed.json()["code"] == "audit_timezone_required"
    assert aware.status_code == 200
    call = listing.await_args.kwargs
    assert call["date_from"] == datetime(2026, 9, 1, tzinfo=UTC)
    assert call["date_to"] == datetime(2026, 9, 2, tzinfo=UTC)


@pytest.mark.asyncio
async def test_bootstrap_navigation_comes_from_backend_capabilities(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = SimpleNamespace(id=uuid4(), email="db@example.test")
    monkeypatch.setattr(
        operations_service,
        "effective_admin_roles",
        AsyncMock(return_value={"database_operator"}),
    )
    monkeypatch.setattr(
        operations_service,
        "effective_admin_capabilities",
        AsyncMock(
            return_value={
                "admin.access",
                "dashboard.read",
                "database.read",
                "database.maintain",
                "audit.read",
            }
        ),
    )
    monkeypatch.setattr(
        operations_service,
        "pending_counts",
        AsyncMock(return_value={"hotspots_pending": 2}),
    )
    monkeypatch.setattr(
        operations_service,
        "_system_status",
        AsyncMock(return_value={}),
    )

    result = await operations_service.admin_bootstrap(object(), actor)  # type: ignore[arg-type]

    assert result.actor.roles == ["database_operator"]
    assert {item.id for item in result.navigation} == {"dashboard", "database", "audit"}
    assert "users" not in {item.id for item in result.navigation}


@pytest.mark.asyncio
async def test_system_health_uses_live_agents_and_latest_verified_backup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = operations_service.get_settings()
    monkeypatch.setattr(settings, "deployments_enabled", True)
    monkeypatch.setattr(settings, "deploy_admin_emails", "deploy@example.com")
    monkeypatch.setattr(settings, "deploy_agent_hmac_key", "x" * 32)
    monkeypatch.setattr(settings, "deploy_agent_socket", "/run/deployer.sock")
    session = AsyncMock()
    session.scalar.return_value = operations_service.expected_schema_revision()
    redis = SimpleNamespace(ping=AsyncMock(return_value=True))
    monkeypatch.setattr(operations_service, "get_redis", lambda: redis)
    monkeypatch.setattr(
        operations_service.DeploymentAgentClient,
        "overview",
        AsyncMock(
            return_value=AgentOverview(
                connected=True,
                deployed_sha="a" * 40,
                target_sha="a" * 40,
                ci_status="success",
            )
        ),
    )
    older = datetime.now(UTC) - timedelta(days=1)
    latest = datetime.now(UTC)
    monkeypatch.setattr(
        operations_service.DatabaseAgentClient,
        "overview",
        AsyncMock(
            return_value=AgentDatabaseOverview(
                connected=True,
                available=True,
                backups=[
                    AgentVerifiedBackup(
                        backup_name="older.dump",
                        checksum_sha256="a" * 64,
                        size_bytes=100,
                        schema_revision="0068_admin_operations_center",
                        release_sha="a" * 40,
                        source="manual",
                        source_job_id=uuid4(),
                        verified_at=older,
                    ),
                    AgentVerifiedBackup(
                        backup_name="latest.dump",
                        checksum_sha256="b" * 64,
                        size_bytes=200,
                        schema_revision="0068_admin_operations_center",
                        release_sha="a" * 40,
                        source="deployment",
                        source_job_id=uuid4(),
                        verified_at=latest,
                    ),
                ],
            )
        ),
    )

    result = await operations_service._system_status(  # noqa: SLF001
        session, {"deployments_active": 0, "community_jobs_pending": 0}
    )

    assert result["deployment"].status == "healthy"
    assert result["backup"].status == "healthy"
    assert result["backup"].detail is not None
    assert "部署" in result["backup"].detail
    assert latest.strftime("%Y-%m-%d") in result["backup"].detail


@pytest.mark.asyncio
async def test_system_health_never_turns_missing_agents_into_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = operations_service.get_settings()
    monkeypatch.setattr(settings, "deployments_enabled", True)
    monkeypatch.setattr(settings, "deploy_admin_emails", "deploy@example.com")
    monkeypatch.setattr(settings, "deploy_agent_hmac_key", "x" * 32)
    monkeypatch.setattr(settings, "deploy_agent_socket", "/run/deployer.sock")
    monkeypatch.setattr(settings, "admin_database_maintenance_enabled", True)
    monkeypatch.setattr(settings, "database_admin_emails", "database@example.com")
    session = AsyncMock()
    session.scalar.return_value = operations_service.expected_schema_revision()
    redis = SimpleNamespace(ping=AsyncMock(return_value=True))
    monkeypatch.setattr(operations_service, "get_redis", lambda: redis)
    missing = AppError(503, "deployment_agent_unavailable", "offline")
    monkeypatch.setattr(
        operations_service.DeploymentAgentClient,
        "overview",
        AsyncMock(side_effect=missing),
    )
    monkeypatch.setattr(
        operations_service.DatabaseAgentClient,
        "overview",
        AsyncMock(
            side_effect=AppError(503, "database_agent_unavailable", "offline")
        ),
    )

    result = await operations_service._system_status(  # noqa: SLF001
        session, {"deployments_active": 0, "community_jobs_pending": 0}
    )

    assert result["deployment"].status == "unavailable"
    assert result["backup"].status == "unavailable"


@pytest.mark.asyncio
async def test_system_health_treats_disconnected_agent_snapshots_as_stale(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = operations_service.get_settings()
    monkeypatch.setattr(settings, "deployments_enabled", True)
    monkeypatch.setattr(settings, "deploy_admin_emails", "deploy@example.com")
    monkeypatch.setattr(settings, "deploy_agent_hmac_key", "x" * 32)
    monkeypatch.setattr(settings, "deploy_agent_socket", "/run/deployer.sock")
    session = AsyncMock()
    session.scalar.return_value = operations_service.expected_schema_revision()
    monkeypatch.setattr(
        operations_service, "get_redis", lambda: SimpleNamespace(ping=AsyncMock())
    )
    monkeypatch.setattr(
        operations_service.DeploymentAgentClient,
        "overview",
        AsyncMock(return_value=AgentOverview(connected=False)),
    )
    monkeypatch.setattr(
        operations_service.DatabaseAgentClient,
        "overview",
        AsyncMock(
            return_value=AgentDatabaseOverview(connected=False, available=False)
        ),
    )

    result = await operations_service._system_status(  # noqa: SLF001
        session, {"deployments_active": 0, "community_jobs_pending": 0}
    )

    assert result["deployment"].status == "unavailable"
    assert result["backup"].status == "unavailable"
