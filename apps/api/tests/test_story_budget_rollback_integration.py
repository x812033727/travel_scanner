"""Exercise the 0133-on-0132 application rollback against a real PostgreSQL server.

The CI database is already migrated to head. This test creates its own short-lived
database so it can run the real Alembic commands, then executes the production
Compose migrate command from a copy of the prior application's migration tree.
No vendor request is made: ``reserve`` must refuse over-limit calls before dispatch.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Iterator
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import pytest
import sqlalchemy as sa
from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import get_settings
from app.video_budget.models import PILOT_LIMITS_USD, VideoPilotBudgetOperation

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires a local PostgreSQL service"
)

API_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = API_ROOT.parents[1]
MIGRATION_0132 = "0132_video_pilot_budget"
MIGRATION_0133 = "0133_story_followon_budget"
MIGRATION_0134 = "0134_a01_admission_fence"
MIGRATION_0133_SOURCE_SHA256 = "e18559b5b1851b47cb3e36a8203bd5863488696d829192fbbae8bc7b9dbdc780"
# Exact #1510 migration body. #1521 must be able to run this test before
# 0133 enters its release image; the #1510 checkout must match this digest.
MIGRATION_0133_SOURCE = r'''
"""Protect B18 v2 and five follow-on stories with separate USD 5 full-film ceilings.

Revision ID: 0133_story_followon_budget
Revises: 0132_video_pilot_budget

The existing B18 v2 account and every operation remain in place. Lowering its account
ceiling does not erase a prior hold or charge: the budget service refuses new dispatches
when retained exposure is above USD 5. The five new accounts are inserted independently.

Deploy the separate 0132 application compatibility release (#1521) and verify it
before this migration. Production runs migrations before switching API containers and
an application rollback does not downgrade the database.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import insert

revision: str = "0133_story_followon_budget"
down_revision: str | None = "0132_video_pilot_budget"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

ACCOUNT = "video_pilot_budgets"
CONSTRAINT = "ck_video_pilot_budget_limit"
B18_V2 = "story-conveyor-belt-sushi-v2"
FOLLOWONS = (
    "story-five-lego-legoland",
    "story-five-costco-hot-dog",
    "story-five-adidas-puma-brothers",
    "story-five-ajinomoto-chip-film",
    "story-five-pringles-vat-case",
)


def upgrade() -> None:
    # Replacing the same named constraint makes rerunning the upgrade bounded; the value
    # update and ON CONFLICT seeds do not touch operation rows or reset paid exposure.
    op.drop_constraint(CONSTRAINT, ACCOUNT, type_="check")
    op.create_check_constraint(CONSTRAINT, ACCOUNT, "limit_usd IN (5.000000, 25.000000)")

    account = sa.table(
        ACCOUNT,
        sa.column("slug", sa.String(length=80)),
        sa.column("limit_usd", sa.Numeric(12, 6)),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    op.execute(
        sa.update(account)
        .where(account.c.slug == B18_V2)
        .where(account.c.limit_usd == sa.literal(25))
        .values(limit_usd=sa.literal(5))
    )
    for slug in FOLLOWONS:
        op.execute(
            insert(account)
            .values(slug=slug, limit_usd=sa.literal(5), created_at=sa.func.now())
            .on_conflict_do_nothing(index_elements=["slug"])
        )


def downgrade() -> None:
    # Automatically expanding B18 back to USD 25 or dropping a follow-on account could
    # authorize more spend or erase the context of retained operations. Roll back only
    # the application code; a database reversal requires a separate reviewed plan.
    raise RuntimeError("The story budget ceiling cannot be downgraded automatically")
'''.lstrip("\n")
B18_V2 = "story-conveyor-belt-sushi-v2"
FOLLOWONS = (
    "story-five-lego-legoland",
    "story-five-costco-hot-dog",
    "story-five-adidas-puma-brothers",
    "story-five-ajinomoto-chip-film",
    "story-five-pringles-vat-case",
)


def _base_url() -> URL:
    url = make_url(get_settings().database_url)
    assert url.drivername == "postgresql+asyncpg"
    # Never create or drop a database on a production/remote server by accident.
    assert url.host in {"localhost", "127.0.0.1", "::1"}
    assert url.database
    return url


async def _database_ddl(url: URL, statement: str) -> None:
    engine = create_async_engine(url, isolation_level="AUTOCOMMIT")
    try:
        async with engine.connect() as connection:
            await connection.execute(sa.text(statement))
    finally:
        await engine.dispose()


async def _execute(url: URL, statement: str, parameters: dict[str, object] | None = None) -> None:
    engine = create_async_engine(url)
    try:
        async with engine.begin() as connection:
            await connection.execute(sa.text(statement), parameters or {})
    finally:
        await engine.dispose()


async def _fetch(url: URL, statement: str) -> list[tuple[object, ...]]:
    engine = create_async_engine(url)
    try:
        async with engine.connect() as connection:
            result = await connection.execute(sa.text(statement))
            return [tuple(row) for row in result.all()]
    finally:
        await engine.dispose()


async def _seed_original_b18_operations(url: URL) -> None:
    engine = create_async_engine(url)
    try:
        async with engine.begin() as connection:
            for operation_id, status, maximum, actual in (
                ("pre-upgrade-settled", "settled", "2.000000", "1.500000"),
                ("pre-upgrade-uncertain", "uncertain", "2.000000", None),
            ):
                await connection.execute(
                    sa.insert(VideoPilotBudgetOperation).values(
                        id=uuid4(),
                        slug=B18_V2,
                        operation_id=operation_id,
                        category="speech",
                        provider="gemini",
                        model="test-model",
                        max_usd=Decimal(maximum),
                        actual_usd=Decimal(actual) if actual is not None else None,
                        status=status,
                        attempts=1,
                    )
                )
    finally:
        await engine.dispose()


def _run(
    arguments: list[str], *, cwd: Path, url: URL, timeout: int = 120
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["DATABASE_URL"] = url.render_as_string(hide_password=False)
    # The copied 0132 tree must win over the current 0133 checkout on sys.path.
    environment["PYTHONPATH"] = str(cwd)
    return subprocess.run(
        [sys.executable, *arguments],
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def _assert_success(result: subprocess.CompletedProcess[str]) -> None:
    assert result.returncode == 0, f"stdout={result.stdout[-2000:]} stderr={result.stderr[-2000:]}"


def _compose_migrate_arguments() -> list[str]:
    compose = (REPO_ROOT / "docker-compose.prod.yml").read_text(encoding="utf-8")
    service = compose.split("\n  migrate:\n", 1)[1].split("\n  api:\n", 1)[0]
    match = re.search(r"(?m)^    command: (\[[^\n]+\])$", service)
    assert match, "production migrate service has no literal command"
    command: list[str] = json.loads(match.group(1))
    assert command[:2] == ["python", "-m"]
    assert command[2:] == ["app.migration_guard"]
    return command[1:]


def _copy_0132_image_tree(destination: Path) -> Path:
    assert (API_ROOT / "app" / "migration_guard.py").is_file(), (
        "#1521 migration guard must be merged before the #1510 rollback test can pass"
    )
    destination.mkdir()
    shutil.copytree(
        API_ROOT / "app",
        destination / "app",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )

    def without_future_revision(directory: str, names: list[str]) -> set[str]:
        ignored = {name for name in names if name in {"__pycache__"} or name.endswith(".pyc")}
        if Path(directory).name == "versions":
            ignored.add(f"{MIGRATION_0133}.py")
        return ignored

    shutil.copytree(
        API_ROOT / "migrations", destination / "migrations", ignore=without_future_revision
    )
    shutil.copy2(API_ROOT / "alembic.ini", destination / "alembic.ini")
    assert not (destination / "migrations" / "versions" / f"{MIGRATION_0133}.py").exists()
    return destination


@pytest.fixture
def rollback_database(tmp_path: Path) -> Iterator[tuple[URL, Path]]:
    base = _base_url()
    name = f"test_story_rollback_{uuid4().hex[:16]}"
    url = base.set(database=name)
    asyncio.run(_database_ddl(base, f'CREATE DATABASE "{name}"'))
    try:
        rollback_root = _copy_0132_image_tree(tmp_path / "rollback-api")
        yield url, rollback_root
    finally:
        asyncio.run(_database_ddl(base, f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)'))


def test_real_0133_migration_allows_only_the_reviewed_0132_rollback(
    rollback_database: tuple[URL, Path],
) -> None:
    url, rollback_root = rollback_database
    migrate_command = _compose_migrate_arguments()
    migration_source = API_ROOT / "migrations" / "versions" / f"{MIGRATION_0133}.py"
    guard_source = rollback_root / "app" / "migration_guard.py"
    source_bytes = MIGRATION_0133_SOURCE.encode("utf-8")
    assert hashlib.sha256(source_bytes).hexdigest() == MIGRATION_0133_SOURCE_SHA256
    if migration_source.exists():
        # #1510 must run precisely the source already exercised on #1521 CI.
        assert migration_source.read_bytes().replace(b"\r\n", b"\n") == source_bytes
    print(
        "ROLLBACK_SOURCE_SHA256 "
        f"0133={MIGRATION_0133_SOURCE_SHA256} "
        f"guard={hashlib.sha256(guard_source.read_bytes()).hexdigest()}"
    )

    _assert_success(_run(["-m", "alembic", "upgrade", MIGRATION_0132], cwd=rollback_root, url=url))
    assert asyncio.run(_fetch(url, "SELECT version_num FROM alembic_version")) == [
        (MIGRATION_0132,)
    ]
    assert asyncio.run(
        _fetch(
            url,
            f"SELECT slug, limit_usd FROM video_pilot_budgets WHERE slug = '{B18_V2}'",
        )
    ) == [(B18_V2, Decimal("25.000000"))]
    asyncio.run(_seed_original_b18_operations(url))

    # Install the exact future revision only in this disposable API copy. The
    # #1521 source and release image remain at 0132; remove it before rollback.
    future_revision = rollback_root / "migrations" / "versions" / f"{MIGRATION_0133}.py"
    future_revision.write_bytes(source_bytes)
    try:
        _assert_success(
            _run(["-m", "alembic", "upgrade", MIGRATION_0133], cwd=rollback_root, url=url)
        )
    finally:
        future_revision.unlink()
    assert not future_revision.exists()
    before_rollback = asyncio.run(
        _fetch(
            url,
            "SELECT id, operation_id, status, max_usd, actual_usd "
            "FROM video_pilot_budget_operations ORDER BY operation_id",
        )
    )
    assert [(row[1], row[2], row[3], row[4]) for row in before_rollback] == [
        ("pre-upgrade-settled", "settled", Decimal("2.000000"), Decimal("1.500000")),
        ("pre-upgrade-uncertain", "uncertain", Decimal("2.000000"), None),
    ]
    assert asyncio.run(_fetch(url, "SELECT version_num FROM alembic_version")) == [
        (MIGRATION_0133,)
    ]
    limits = {
        str(row[0]): Decimal(str(row[1]))
        for row in asyncio.run(_fetch(url, "SELECT slug, limit_usd FROM video_pilot_budgets"))
    }
    assert limits == PILOT_LIMITS_USD
    budget_checks = asyncio.run(
        _fetch(
            url,
            "SELECT pg_get_constraintdef(oid), convalidated FROM pg_constraint "
            "WHERE conrelid='video_pilot_budgets'::regclass "
            "AND conname='ck_video_pilot_budget_limit' AND contype='c'",
        )
    )
    assert len(budget_checks) == 1 and budget_checks[0][1] is True
    assert all(value in str(budget_checks[0][0]) for value in ("5.000000", "25.000000"))
    operation_constraints_raw = asyncio.run(
        _fetch(
            url,
            "SELECT conname, contype FROM pg_constraint "
            "WHERE conrelid='video_pilot_budget_operations'::regclass",
        )
    )
    operation_constraints = [
        (name, kind.decode("ascii") if isinstance(kind, bytes) else kind)
        for name, kind in operation_constraints_raw
    ]
    assert ("uq_video_pilot_budget_operation", "u") in operation_constraints
    assert any(kind == "f" for _, kind in operation_constraints)
    assert ("ix_video_pilot_budget_operations_slug",) in asyncio.run(
        _fetch(
            url,
            "SELECT indexname FROM pg_indexes WHERE tablename='video_pilot_budget_operations'",
        )
    )

    # Execute the old image's real production migrate command. No stamp or downgrade.
    migrated = _run(migrate_command, cwd=rollback_root, url=url)
    _assert_success(migrated)
    expected_status = (
        f"state=rollback-compatible current={MIGRATION_0133} expected={MIGRATION_0132}"
    )
    assert expected_status in migrated.stdout
    status = _run([*migrate_command, "--status"], cwd=rollback_root, url=url)
    _assert_success(status)
    assert "state=rollback-compatible" in status.stdout
    assert asyncio.run(_fetch(url, "SELECT version_num FROM alembic_version")) == [
        (MIGRATION_0133,)
    ]
    assert (
        asyncio.run(
            _fetch(
                url,
                "SELECT id, operation_id, status, max_usd, actual_usd "
                "FROM video_pilot_budget_operations ORDER BY operation_id",
            )
        )
        == before_rollback
    )

    # The rolled-back app, not a mocked readiness function, reads the 0133 DB and Redis.
    ready = _run(
        [
            "-c",
            "import asyncio, httpx\nfrom app.main import app\n"
            "async def check():\n"
            " async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), "
            "base_url='http://test') as client:\n"
            "  response = await client.get('/ready'); "
            "assert response.status_code == 200, response.text; "
            f"assert response.json()['schema'] == '{MIGRATION_0133}'; "
            "print(response.json())\n"
            "asyncio.run(check())",
        ],
        cwd=rollback_root,
        url=url,
    )
    _assert_success(ready)

    # Service-level paid boundary: every film has its own account and over-limit
    # reservations are rejected before a vendor can be called.
    budget = _run(
        [
            "-c",
            "import asyncio\nfrom decimal import Decimal\n"
            "from app.db import SessionFactory, engine\n"
            "from app.video_budget import service\n"
            f"slugs={repr((B18_V2, *FOLLOWONS))}\n"
            "async def check():\n"
            " for slug in slugs:\n"
            "  async with SessionFactory() as session:\n"
            "   view = await service.summary(session, slug); "
            "assert view is not None and view.limit_usd == Decimal('5.000000'), slug\n"
            "   ceiling = Decimal('1.500001') if slug == slugs[0] else Decimal('5.000001')\n"
            "   try:\n"
            "    await service.reserve(session, slug=slug, operation_id='must-refuse', "
            "category='speech', provider='gemini', model='test-model', max_usd=ceiling)\n"
            "   except service.BudgetError as error:\n"
            "    assert error.code == 'video_budget_exhausted', (slug, error.code)\n"
            "   else:\n"
            "    raise AssertionError(f'over-limit paid operation was allowed: {slug}')\n"
            " await engine.dispose()\n"
            "asyncio.run(check())",
        ],
        cwd=rollback_root,
        url=url,
    )
    _assert_success(budget)
    assert asyncio.run(_fetch(url, "SELECT count(*) FROM video_pilot_budget_operations")) == [(2,)]

    # Each malformed database state must reject the actual migrate command, not
    # just an isolated classify_revisions() helper.
    asyncio.run(_execute(url, "UPDATE alembic_version SET version_num='0134_unknown_test'"))
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(
        _execute(
            url,
            "UPDATE alembic_version SET version_num=:revision",
            {"revision": MIGRATION_0133},
        )
    )

    asyncio.run(
        _execute(url, "INSERT INTO alembic_version(version_num) VALUES ('0134_unknown_test')")
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(_execute(url, "DELETE FROM alembic_version WHERE version_num='0134_unknown_test'"))

    asyncio.run(
        _execute(url, "DELETE FROM video_pilot_budgets WHERE slug=:slug", {"slug": FOLLOWONS[0]})
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(
        _execute(
            url,
            "INSERT INTO video_pilot_budgets(slug, limit_usd) VALUES (:slug, 5)",
            {"slug": FOLLOWONS[0]},
        )
    )

    # A constraint with the right name but the wrong definition cannot protect
    # paid idempotency or the allowed operation states.
    asyncio.run(
        _execute(
            url,
            "ALTER TABLE video_pilot_budget_operations "
            "DROP CONSTRAINT uq_video_pilot_budget_operation",
        )
    )
    asyncio.run(
        _execute(
            url,
            "ALTER TABLE video_pilot_budget_operations "
            "ADD CONSTRAINT uq_video_pilot_budget_operation UNIQUE (id)",
        )
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(
        _execute(
            url,
            "ALTER TABLE video_pilot_budget_operations "
            "DROP CONSTRAINT uq_video_pilot_budget_operation",
        )
    )
    asyncio.run(
        _execute(
            url,
            "ALTER TABLE video_pilot_budget_operations "
            "ADD CONSTRAINT uq_video_pilot_budget_operation UNIQUE (slug, operation_id)",
        )
    )

    asyncio.run(
        _execute(
            url,
            "ALTER TABLE video_pilot_budget_operations "
            "DROP CONSTRAINT ck_video_pilot_budget_operation_status",
        )
    )
    asyncio.run(
        _execute(
            url,
            "ALTER TABLE video_pilot_budget_operations "
            "ADD CONSTRAINT ck_video_pilot_budget_operation_status CHECK (true)",
        )
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(
        _execute(
            url,
            "ALTER TABLE video_pilot_budget_operations "
            "DROP CONSTRAINT ck_video_pilot_budget_operation_status",
        )
    )
    asyncio.run(
        _execute(
            url,
            "ALTER TABLE video_pilot_budget_operations "
            "ADD CONSTRAINT ck_video_pilot_budget_operation_status "
            "CHECK (status IN ('reserved', 'uncertain', 'settled', 'released'))",
        )
    )

    asyncio.run(
        _execute(url, "ALTER TABLE video_pilot_budgets DROP CONSTRAINT ck_video_pilot_budget_limit")
    )
    asyncio.run(
        _execute(
            url,
            "ALTER TABLE video_pilot_budgets "
            "ADD CONSTRAINT ck_video_pilot_budget_limit "
            "CHECK (limit_usd IN (5.000000, 25.000000, 1000.000000))",
        )
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0

    asyncio.run(
        _execute(url, "ALTER TABLE video_pilot_budgets DROP CONSTRAINT ck_video_pilot_budget_limit")
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(
        _execute(
            url,
            "ALTER TABLE video_pilot_budgets ADD CONSTRAINT ck_video_pilot_budget_limit "
            "CHECK (limit_usd IN (5.000000, 25.000000))",
        )
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode == 0

    # Port 1 on loopback cannot be this test's PostgreSQL. A connection failure
    # must never be treated as a compatible rollback state.
    unavailable = url.set(host="127.0.0.1", port=1)
    assert _run(migrate_command, cwd=rollback_root, url=unavailable).returncode != 0


def test_0133_image_checks_real_0134_rollback_schema_and_held_token(
    rollback_database: tuple[URL, Path],
) -> None:
    """Run the pre-compatibility image's real migrate guard on a disposable DB."""
    url, image_root = rollback_database
    migration = image_root / "migrations" / "versions" / f"{MIGRATION_0133}.py"
    migration.write_text(MIGRATION_0133_SOURCE, encoding="utf-8")
    _assert_success(_run(["-m", "alembic", "upgrade", MIGRATION_0133], cwd=image_root, url=url))
    command = _compose_migrate_arguments()
    _assert_success(_run([*command, "--status"], cwd=image_root, url=url))

    # The proposed 0134 migration adds exactly this nullable UUID column. The
    # pre-compatibility image has no 0134 Alembic file, as on application rollback.
    asyncio.run(_execute(url, "ALTER TABLE video_pilot_budgets ADD COLUMN admission_token uuid"))
    asyncio.run(
        _execute(
            url,
            "UPDATE alembic_version SET version_num = :revision",
            {"revision": MIGRATION_0134},
        )
    )
    status = _run([*command, "--status"], cwd=image_root, url=url)
    _assert_success(status)
    assert f"state=rollback-compatible current={MIGRATION_0134}" in status.stdout
    _assert_success(_run(command, cwd=image_root, url=url))

    asyncio.run(
        _execute(
            url,
            "UPDATE video_pilot_budgets SET admission_token = :token "
            "WHERE slug = 'story-rolling-suitcase-v2'",
            {"token": uuid4()},
        )
    )
    assert _run(command, cwd=image_root, url=url).returncode != 0
    asyncio.run(
        _execute(
            url,
            "UPDATE video_pilot_budgets SET admission_token = NULL "
            "WHERE slug = 'story-rolling-suitcase-v2'",
        )
    )
    asyncio.run(
        _execute(url, "ALTER TABLE video_pilot_budgets ALTER COLUMN admission_token TYPE text")
    )
    assert _run(command, cwd=image_root, url=url).returncode != 0
    asyncio.run(_execute(url, "ALTER TABLE video_pilot_budgets DROP COLUMN admission_token"))
    assert _run(command, cwd=image_root, url=url).returncode != 0
    asyncio.run(_execute(url, "UPDATE alembic_version SET version_num = '0135_unknown'"))
    assert _run(command, cwd=image_root, url=url).returncode != 0
