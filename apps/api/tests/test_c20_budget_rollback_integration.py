"""Exercise the 0138 image on the exact future C20 account schema in PostgreSQL.

The 0139 source exists only in this disposable test tree. The release image in
this PR still has Alembic head 0138 and refuses every everyday-story paid call.
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
from app.migration_guard import C20_PILOT_SLUG, C20_REVIEWED_FUTURE_REVISION
from app.video_budget.models import C_SERIES_PILOT_LIMITS_USD, PILOT_LIMITS_USD

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires a local PostgreSQL service"
)

API_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = API_ROOT.parents[1]
ROLLBACK_HEAD = "0138_story_everyday_budget"
FUTURE_HEAD = C20_REVIEWED_FUTURE_REVISION
FUTURE_SOURCE = '''
"""Add only the held C20 short-v8 pilot account after 0138 compatibility ships."""

from collections.abc import Sequence
from decimal import Decimal

import sqlalchemy as sa
from alembic import op

revision: str = "0139_c20_zippo_pilot_budget"
down_revision: str | None = "0138_story_everyday_budget"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SLUG = "story-everyday-zippo-c20-short-v8"
OWNERSHIP = "video_pilot_budget_0139_owned"
PRIOR_LIMITS = {
    "story-rolling-suitcase": Decimal("25"),
    "story-conveyor-belt-sushi": Decimal("25"),
    "story-rolling-suitcase-v2": Decimal("25"),
    "story-conveyor-belt-sushi-v2": Decimal("5"),
    "story-five-lego-legoland": Decimal("5"),
    "story-five-costco-hot-dog": Decimal("5"),
    "story-five-adidas-puma-brothers": Decimal("5"),
    "story-five-ajinomoto-chip-film": Decimal("5"),
    "story-five-pringles-vat-case": Decimal("5"),
    "story-everyday-moleskine-c03": Decimal("25"),
    "story-everyday-bubble-wrap-c04": Decimal("25"),
    "story-everyday-kincho-c05": Decimal("25"),
    "story-everyday-play-doh-c06": Decimal("25"),
    "story-everyday-dr-martens-c07": Decimal("25"),
    "story-everyday-oxo-c10": Decimal("25"),
    "story-everyday-frixion-c15": Decimal("25"),
}
HISTORICAL = (
    "story-everyday-moleskine-c03",
    "story-everyday-bubble-wrap-c04",
    "story-everyday-kincho-c05",
    "story-everyday-play-doh-c06",
)


def upgrade() -> None:
    if op.get_context().as_sql:
        raise RuntimeError("0139 requires online C20 account verification")
    bind = op.get_bind()
    bind.execute(sa.text(
        "LOCK TABLE video_pilot_budgets, video_pilot_budget_operations "
        "IN SHARE ROW EXCLUSIVE MODE"
    ))
    accounts = bind.execute(sa.text(
        "SELECT slug, limit_usd FROM video_pilot_budgets"
    )).all()
    if len(accounts) != len(PRIOR_LIMITS) or {
        slug: Decimal(limit) for slug, limit in accounts
    } != PRIOR_LIMITS:
        raise RuntimeError("0139 prior account inventory is not reviewed 0138")
    holds = bind.execute(sa.text(
        "SELECT slug, category, provider, model, max_usd, status, attempts "
        "FROM video_pilot_budget_operations "
        "WHERE operation_id = 'pre-ledger-history'"
    )).all()
    if len(holds) != len(HISTORICAL) or {row[0] for row in holds} != set(HISTORICAL):
        raise RuntimeError("0139 historical C-series holds are missing")
    if any(row[1:5] != ("historical", "unattributed", "unattributed", Decimal("25"))
           or row[5] not in ("uncertain", "settled", "released") or row[6] != 1
           for row in holds):
        raise RuntimeError("0139 historical C-series hold identity changed")
    if sa.inspect(bind).has_table(OWNERSHIP):
        raise RuntimeError("0139 ownership table already exists")
    if bind.execute(sa.text(
        "SELECT 1 FROM video_pilot_budgets WHERE slug = :slug"
    ), {"slug": SLUG}).first() is not None:
        raise RuntimeError("0139 C20 account predates reviewed migration")
    op.create_table(
        OWNERSHIP,
        sa.Column("slug", sa.String(80), primary_key=True),
        sa.Column("account_created", sa.Boolean(), nullable=False),
        sa.Column("account_created_at", sa.DateTime(timezone=True), nullable=False),
    )
    row = bind.execute(sa.text(
        "INSERT INTO video_pilot_budgets(slug, limit_usd, created_at) "
        "VALUES (:slug, 25.000000, now()) RETURNING created_at"
    ), {"slug": SLUG}).one()
    bind.execute(sa.text(
        "INSERT INTO video_pilot_budget_0139_owned "
        "(slug, account_created, account_created_at) "
        "VALUES (:slug, true, :created_at)"
    ), {"slug": SLUG, "created_at": row[0]})


def downgrade() -> None:
    raise RuntimeError("C20 ledger evidence cannot be erased automatically")
'''.lstrip("\n")
# The later 0139 migration must be byte-for-byte this reviewed fixture, or the
# compatibility pair requires a fresh review and test before deployment.
FUTURE_SOURCE_SHA256 = "209f225ca2c38b25d7e962cd0c6fd4e44f379daf953f3248128d2ba1e9a452a5"


def _base_url() -> URL:
    url = make_url(get_settings().database_url)
    assert url.drivername == "postgresql+asyncpg"
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


def _run(arguments: list[str], *, cwd: Path, url: URL) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["DATABASE_URL"] = url.render_as_string(hide_password=False)
    environment["PYTHONPATH"] = str(cwd)
    return subprocess.run(
        [sys.executable, *arguments],
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )


def _assert_success(result: subprocess.CompletedProcess[str]) -> None:
    assert result.returncode == 0, f"stdout={result.stdout[-2000:]} stderr={result.stderr[-2000:]}"


def _compose_migrate_arguments() -> list[str]:
    compose = (REPO_ROOT / "docker-compose.prod.yml").read_text(encoding="utf-8")
    service = compose.split("\n  migrate:\n", 1)[1].split("\n  api:\n", 1)[0]
    match = re.search(r"(?m)^    command: (\[[^\n]+\])$", service)
    assert match
    command: list[str] = json.loads(match.group(1))
    assert command == ["python", "-m", "app.migration_guard"]
    return command[1:]


def _copy_0138_image_tree(destination: Path) -> Path:
    destination.mkdir()
    shutil.copytree(
        API_ROOT / "app",
        destination / "app",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )

    def without_future_revision(directory: str, names: list[str]) -> set[str]:
        ignored = {name for name in names if name == "__pycache__" or name.endswith(".pyc")}
        if Path(directory).name == "versions":
            ignored |= {
                name
                for name in names
                if name[:4].isdigit() and int(name[:4]) > int(ROLLBACK_HEAD[:4])
            }
        return ignored

    shutil.copytree(
        API_ROOT / "migrations", destination / "migrations", ignore=without_future_revision
    )
    shutil.copy2(API_ROOT / "alembic.ini", destination / "alembic.ini")
    assert not (destination / "migrations" / "versions" / f"{FUTURE_HEAD}.py").exists()
    return destination


@pytest.fixture
def rollback_database(tmp_path: Path) -> Iterator[tuple[URL, Path]]:
    base = _base_url()
    name = f"test_c20_rollback_{uuid4().hex[:16]}"
    url = base.set(database=name)
    asyncio.run(_database_ddl(base, f'CREATE DATABASE "{name}"'))
    try:
        yield url, _copy_0138_image_tree(tmp_path / "rollback-api")
    finally:
        asyncio.run(_database_ddl(base, f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)'))


def test_real_0139_c20_account_allows_only_reviewed_0138_rollback(
    rollback_database: tuple[URL, Path],
) -> None:
    url, rollback_root = rollback_database
    migrate_command = _compose_migrate_arguments()
    source_bytes = FUTURE_SOURCE.encode("utf-8")
    assert hashlib.sha256(source_bytes).hexdigest() == FUTURE_SOURCE_SHA256
    actual_migration = API_ROOT / "migrations" / "versions" / f"{FUTURE_HEAD}.py"
    if actual_migration.exists():
        assert actual_migration.read_bytes().replace(b"\r\n", b"\n") == source_bytes
    guard_digest = hashlib.sha256(
        (rollback_root / "app" / "migration_guard.py").read_bytes()
    ).hexdigest()
    print(f"ROLLBACK_SOURCE_SHA256 0139={FUTURE_SOURCE_SHA256} guard={guard_digest}")

    _assert_success(_run(["-m", "alembic", "upgrade", ROLLBACK_HEAD], cwd=rollback_root, url=url))
    before = asyncio.run(
        _fetch(
            url,
            "SELECT slug, operation_id, status, max_usd, actual_usd "
            "FROM video_pilot_budget_operations ORDER BY slug, operation_id",
        )
    )
    assert len(before) == 4
    assert asyncio.run(_fetch(url, "SELECT version_num FROM alembic_version")) == [(ROLLBACK_HEAD,)]

    # Install 0139 only in the throwaway tree, upgrade, then remove the file so
    # the following process really runs the old 0138 application's migrate path.
    fixture_revision = rollback_root / "migrations" / "versions" / f"{FUTURE_HEAD}.py"
    fixture_revision.write_bytes(source_bytes)
    try:
        _assert_success(_run(["-m", "alembic", "upgrade", FUTURE_HEAD], cwd=rollback_root, url=url))
    finally:
        fixture_revision.unlink()
    assert not fixture_revision.exists()
    assert asyncio.run(_fetch(url, "SELECT version_num FROM alembic_version")) == [(FUTURE_HEAD,)]
    accounts = {
        str(slug): Decimal(str(limit))
        for slug, limit in asyncio.run(
            _fetch(url, "SELECT slug, limit_usd FROM video_pilot_budgets")
        )
    }
    assert accounts == {
        **PILOT_LIMITS_USD,
        **C_SERIES_PILOT_LIMITS_USD,
        C20_PILOT_SLUG: Decimal("25.000000"),
    }
    assert asyncio.run(
        _fetch(url, "SELECT slug, account_created FROM video_pilot_budget_0139_owned")
    ) == [(C20_PILOT_SLUG, True)]

    # Later paid operations must survive application rollback. This row is test
    # data only; the 0138 service itself must refuse any C20 paid reservation.
    asyncio.run(
        _execute(
            url,
            "INSERT INTO video_pilot_budget_operations "
            "(id, slug, operation_id, category, provider, model, max_usd, status, attempts) "
            "VALUES (:id, :slug, 'later-uncertain', 'speech', 'test', 'test', 1, 'uncertain', 1)",
            {"id": uuid4(), "slug": C20_PILOT_SLUG},
        )
    )
    operations = asyncio.run(
        _fetch(
            url,
            "SELECT slug, operation_id, status FROM video_pilot_budget_operations ORDER BY slug",
        )
    )
    assert len(operations) == 5
    migrated = _run(migrate_command, cwd=rollback_root, url=url)
    _assert_success(migrated)
    expected_status = f"state=rollback-compatible current={FUTURE_HEAD} expected={ROLLBACK_HEAD}"
    assert expected_status in migrated.stdout
    status = _run([*migrate_command, "--status"], cwd=rollback_root, url=url)
    _assert_success(status)
    assert expected_status in status.stdout
    assert asyncio.run(_fetch(url, "SELECT version_num FROM alembic_version")) == [(FUTURE_HEAD,)]
    assert (
        asyncio.run(
            _fetch(
                url,
                "SELECT slug, operation_id, status "
                "FROM video_pilot_budget_operations ORDER BY slug",
            )
        )
        == operations
    )

    ready_arguments = [
        "-c",
        "import asyncio, httpx\nfrom app.main import app\n"
        "async def check():\n"
        " async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), "
        "base_url='http://test') as client:\n"
        "  response = await client.get('/ready'); "
        "assert response.status_code == 200, response.text; "
        f"assert response.json()['schema'] == '{FUTURE_HEAD}'\n"
        "asyncio.run(check())",
    ]
    ready = _run(ready_arguments, cwd=rollback_root, url=url)
    _assert_success(ready)
    held = _run(
        [
            "-c",
            "import asyncio\nfrom decimal import Decimal\n"
            "from app.db import SessionFactory, engine\n"
            "from app.video_budget import service\n"
            f"slug={C20_PILOT_SLUG!r}\n"
            "async def check():\n"
            " async with SessionFactory() as session:\n"
            "  try:\n"
            "   await service.reserve(session, slug=slug, operation_id='must-refuse', "
            "category='speech', provider='test', model='test', max_usd=Decimal('1'))\n"
            "  except service.BudgetError as error:\n"
            "   assert error.code == 'video_budget_preproduction_hold', error.code\n"
            "  else:\n"
            "   raise AssertionError('C20 paid dispatch was admitted')\n"
            " await engine.dispose()\n"
            "asyncio.run(check())",
        ],
        cwd=rollback_root,
        url=url,
    )
    _assert_success(held)

    # Exercise the real Compose command against damaged future-state contracts.
    asyncio.run(_execute(url, "UPDATE alembic_version SET version_num='0139_unreviewed_test'"))
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    assert _run(ready_arguments, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(
        _execute(
            url,
            "UPDATE alembic_version SET version_num=:revision",
            {"revision": FUTURE_HEAD},
        )
    )
    asyncio.run(
        _execute(
            url,
            "UPDATE video_pilot_budgets SET limit_usd=5 WHERE slug=:slug",
            {"slug": C20_PILOT_SLUG},
        )
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(
        _execute(
            url,
            "UPDATE video_pilot_budgets SET limit_usd=25 WHERE slug=:slug",
            {"slug": C20_PILOT_SLUG},
        )
    )
    asyncio.run(_execute(url, "UPDATE video_pilot_budget_0139_owned SET account_created=false"))
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(_execute(url, "UPDATE video_pilot_budget_0139_owned SET account_created=true"))
    asyncio.run(
        _execute(
            url,
            "UPDATE video_pilot_budget_0139_owned SET account_created_at=now() + interval '1 day'",
        )
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(
        _execute(
            url,
            "UPDATE video_pilot_budget_0139_owned SET account_created_at="
            "(SELECT created_at FROM video_pilot_budgets WHERE slug=:slug)",
            {"slug": C20_PILOT_SLUG},
        )
    )
    asyncio.run(
        _execute(
            url,
            "ALTER TABLE video_pilot_budget_0139_owned "
            "DROP CONSTRAINT video_pilot_budget_0139_owned_pkey",
        )
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(
        _execute(
            url,
            "ALTER TABLE video_pilot_budget_0139_owned "
            "ADD CONSTRAINT video_pilot_budget_0139_owned_pkey PRIMARY KEY (slug)",
        )
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode == 0
    unavailable = url.set(host="127.0.0.1", port=1)
    assert _run(migrate_command, cwd=rollback_root, url=unavailable).returncode != 0
    asyncio.run(
        _execute(
            url,
            "DELETE FROM video_pilot_budget_operations WHERE slug=:slug",
            {"slug": C20_PILOT_SLUG},
        )
    )
    asyncio.run(
        _execute(url, "DELETE FROM video_pilot_budgets WHERE slug=:slug", {"slug": C20_PILOT_SLUG})
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
