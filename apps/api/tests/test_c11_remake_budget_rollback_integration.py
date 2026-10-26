"""Exercise the 0139 image on the exact future C11 UCC remake account schema in PostgreSQL.

The test strips the 0140 migration from a disposable copy of the application,
upgrades that database with the pinned 0140 source, then runs the old 0139
migration command. The copy is today's application code, which activates the
C11 remake; the deployed 0139 image (#1870, 2edb6eaab) still held it.
"""

from __future__ import annotations

import ast
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
from app.migration_guard import (
    C11_REMAKE_PILOT_SLUG,
    C11_REMAKE_REVIEWED_FUTURE_REVISION,
    C20_PILOT_SLUG,
)
from app.video_budget.models import C_SERIES_PILOT_LIMITS_USD, PILOT_LIMITS_USD
from app.video_budget.service import is_preproduction_held

API_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = API_ROOT.parents[1]
ROLLBACK_HEAD = "0139_c20_zippo_pilot_budget"
FUTURE_HEAD = C11_REMAKE_REVIEWED_FUTURE_REVISION
FUTURE_SOURCE = r'''
"""Seed only the C11 UCC remake's USD 25 pilot account (owner approved 2026-10-26).

Revision ID: 0140_c11_ucc_remake_budget
Revises: 0139_c20_zippo_pilot_budget

An account alone admits no paid request; the application's activated-slug list decides.
"""

import re
from collections.abc import Sequence
from decimal import Decimal

import sqlalchemy as sa
from alembic import op

revision: str = "0140_c11_ucc_remake_budget"
down_revision: str | None = "0139_c20_zippo_pilot_budget"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SLUG = "story-everyday-ucc-c11-remake-20261025"
OWNERSHIP = "video_pilot_budget_0140_owned"
C20_SLUG = "story-everyday-zippo-c20-short-v8"
C20_OWNERSHIP = "video_pilot_budget_0139_owned"
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
    C20_SLUG: Decimal("25"),
}
HISTORICAL = (
    "story-everyday-moleskine-c03",
    "story-everyday-bubble-wrap-c04",
    "story-everyday-kincho-c05",
    "story-everyday-play-doh-c06",
)


def upgrade() -> None:
    if op.get_context().as_sql:
        raise RuntimeError("0140 requires online C11 remake account verification")
    bind = op.get_bind()
    bind.execute(sa.text(
        "LOCK TABLE video_pilot_budgets, video_pilot_budget_operations, "
        "video_pilot_budget_0139_owned IN SHARE ROW EXCLUSIVE MODE"
    ))
    accounts = bind.execute(sa.text(
        "SELECT slug, limit_usd, created_at FROM video_pilot_budgets"
    )).mappings().all()
    if len(accounts) != len(PRIOR_LIMITS) or {
        row["slug"]: Decimal(row["limit_usd"]) for row in accounts
    } != PRIOR_LIMITS:
        raise RuntimeError("0140 prior account inventory is not reviewed 0139")
    accounts_by_slug = {row["slug"]: row for row in accounts}
    holds = bind.execute(sa.text(
        "SELECT slug, category, provider, model, max_usd, actual_usd, "
        "status, attempts, receipt_ref, release_reason "
        "FROM video_pilot_budget_operations "
        "WHERE operation_id = 'pre-ledger-history'"
    )).mappings().all()
    if len(holds) != len(HISTORICAL) or {row["slug"] for row in holds} != set(HISTORICAL):
        raise RuntimeError("0140 historical C-series holds are missing")
    for row in holds:
        if (row["category"], row["provider"], row["model"], row["max_usd"],
                row["attempts"]) != (
                    "historical", "unattributed", "unattributed", Decimal("25"), 1
                ):
            raise RuntimeError("0140 historical C-series hold identity changed")
        actual = row["actual_usd"]
        status = row["status"]
        receipt = row["receipt_ref"]
        release_reason = row["release_reason"]
        if status == "uncertain":
            valid = actual is None and receipt is None and release_reason is None
        elif status == "settled":
            valid = actual is not None and bool(receipt)
        elif status == "released":
            valid = (actual is None and isinstance(release_reason, str)
                     and bool(re.fullmatch(
                         r"operator-no-charge evidence=[A-Za-z0-9][A-Za-z0-9._:/#-]{0,159}; \S.*",
                         release_reason,
                     )))
        else:
            valid = False
        if not valid:
            raise RuntimeError("0140 historical C-series hold outcome is invalid")
    owners = bind.execute(sa.text(
        "SELECT slug, account_created, account_created_at FROM video_pilot_budget_0139_owned"
    )).mappings().all()
    if (len(owners) != 1 or owners[0]["slug"] != C20_SLUG
            or owners[0]["account_created"] is not True
            or owners[0]["account_created_at"] != accounts_by_slug[C20_SLUG]["created_at"]):
        raise RuntimeError("0140 prior C20 ownership changed")
    prior_pk = sa.inspect(bind).get_pk_constraint(C20_OWNERSHIP)
    if (prior_pk.get("name") != "video_pilot_budget_0139_owned_pkey"
            or prior_pk.get("constrained_columns") != ["slug"]):
        raise RuntimeError("0140 prior C20 ownership primary key changed")
    if sa.inspect(bind).has_table(OWNERSHIP):
        raise RuntimeError("0140 ownership table already exists")
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
        "INSERT INTO video_pilot_budget_0140_owned "
        "(slug, account_created, account_created_at) "
        "VALUES (:slug, true, :created_at)"
    ), {"slug": SLUG, "created_at": row[0]})


def downgrade() -> None:
    raise RuntimeError("C11 remake ledger evidence cannot be erased automatically")
'''.lstrip("\n")
# The actual 0140 migration must be byte-for-byte this reviewed fixture, or the
# compatibility pair requires a fresh review and test before deployment.
FUTURE_SOURCE_SHA256 = "b6a8707dc220819ccfae8f54ca9c90a790d0eb1cea448f7f030da93fe94583f6"


def test_reviewed_future_source_is_pinned_and_c11_remake_stays_held() -> None:
    assert hashlib.sha256(FUTURE_SOURCE.encode("utf-8")).hexdigest() == FUTURE_SOURCE_SHA256
    assignments: dict[str, ast.expr] = {}
    for statement in ast.parse(FUTURE_SOURCE).body:
        if isinstance(statement, ast.Assign) and len(statement.targets) == 1:
            target = statement.targets[0]
            if isinstance(target, ast.Name):
                assignments[target.id] = statement.value
        elif isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
            assert statement.value is not None
            assignments[statement.target.id] = statement.value
    assert ast.literal_eval(assignments["revision"]) == FUTURE_HEAD
    assert ast.literal_eval(assignments["down_revision"]) == ROLLBACK_HEAD
    assert ast.literal_eval(assignments["SLUG"]) == C11_REMAKE_PILOT_SLUG
    assert ast.literal_eval(assignments["OWNERSHIP"]) == "video_pilot_budget_0140_owned"
    prior = assignments["PRIOR_LIMITS"]
    assert isinstance(prior, ast.Dict)
    limits: dict[str, Decimal] = {}
    for key, value in zip(prior.keys, prior.values, strict=True):
        assert key is not None and isinstance(value, ast.Call)
        slug = C20_PILOT_SLUG if isinstance(key, ast.Name) else ast.literal_eval(key)
        assert value.args and isinstance(slug, str)
        limits[slug] = Decimal(ast.literal_eval(value.args[0]))
    assert limits == {
        **PILOT_LIMITS_USD,
        **C_SERIES_PILOT_LIMITS_USD,
        C20_PILOT_SLUG: Decimal("25"),
    }
    # Activated with its 0140 account (owner decision 2026-10-26).
    assert not is_preproduction_held(C11_REMAKE_PILOT_SLUG)
    assert is_preproduction_held(C20_PILOT_SLUG)


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


async def _fetch(
    url: URL, statement: str, parameters: dict[str, object] | None = None
) -> list[tuple[object, ...]]:
    engine = create_async_engine(url)
    try:
        async with engine.connect() as connection:
            result = await connection.execute(sa.text(statement), parameters or {})
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


def _copy_0139_image_tree(destination: Path) -> Path:
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
    name = f"test_c11_rollback_{uuid4().hex[:16]}"
    url = base.set(database=name)
    asyncio.run(_database_ddl(base, f'CREATE DATABASE "{name}"'))
    try:
        yield url, _copy_0139_image_tree(tmp_path / "rollback-api")
    finally:
        asyncio.run(_database_ddl(base, f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)'))


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="local PostgreSQL required")
def test_real_0140_c11_remake_account_allows_only_reviewed_0139_rollback(
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
    print(f"ROLLBACK_SOURCE_SHA256 0140={FUTURE_SOURCE_SHA256} guard={guard_digest}")

    _assert_success(_run(["-m", "alembic", "upgrade", ROLLBACK_HEAD], cwd=rollback_root, url=url))
    accounts_before = asyncio.run(
        _fetch(url, "SELECT slug, limit_usd, created_at FROM video_pilot_budgets ORDER BY slug")
    )
    holds_before = asyncio.run(
        _fetch(
            url,
            "SELECT id, slug, status, max_usd FROM video_pilot_budget_operations "
            "WHERE operation_id = 'pre-ledger-history' ORDER BY slug",
        )
    )
    c20_owner_before = asyncio.run(
        _fetch(
            url,
            "SELECT slug, account_created, account_created_at FROM video_pilot_budget_0139_owned",
        )
    )
    assert len(accounts_before) == 17
    assert len(holds_before) == 4
    assert len(c20_owner_before) == 1 and c20_owner_before[0][0] == C20_PILOT_SLUG
    assert asyncio.run(_fetch(url, "SELECT version_num FROM alembic_version")) == [(ROLLBACK_HEAD,)]

    # Install the future revision only in a disposable tree, then remove it so
    # every following command runs the old 0139 application's real entry point.
    fixture_revision = rollback_root / "migrations" / "versions" / f"{FUTURE_HEAD}.py"
    fixture_revision.write_bytes(source_bytes)
    try:
        asyncio.run(
            _execute(
                url,
                "INSERT INTO video_pilot_budgets(slug, limit_usd) VALUES (:slug, 25)",
                {"slug": C11_REMAKE_PILOT_SLUG},
            )
        )
        assert (
            _run(["-m", "alembic", "upgrade", FUTURE_HEAD], cwd=rollback_root, url=url).returncode
            != 0
        )
        asyncio.run(
            _execute(
                url,
                "DELETE FROM video_pilot_budgets WHERE slug=:slug",
                {"slug": C11_REMAKE_PILOT_SLUG},
            )
        )
        asyncio.run(
            _execute(
                url,
                "UPDATE video_pilot_budget_operations SET status='reserved' "
                "WHERE slug='story-everyday-moleskine-c03' "
                "AND operation_id='pre-ledger-history'",
            )
        )
        assert (
            _run(["-m", "alembic", "upgrade", FUTURE_HEAD], cwd=rollback_root, url=url).returncode
            != 0
        )
        asyncio.run(
            _execute(
                url,
                "UPDATE video_pilot_budget_operations SET status='uncertain' "
                "WHERE slug='story-everyday-moleskine-c03' "
                "AND operation_id='pre-ledger-history'",
            )
        )
        asyncio.run(_execute(url, "UPDATE video_pilot_budget_0139_owned SET account_created=false"))
        assert (
            _run(["-m", "alembic", "upgrade", FUTURE_HEAD], cwd=rollback_root, url=url).returncode
            != 0
        )
        asyncio.run(_execute(url, "UPDATE video_pilot_budget_0139_owned SET account_created=true"))
        assert asyncio.run(_fetch(url, "SELECT version_num FROM alembic_version")) == [
            (ROLLBACK_HEAD,)
        ]
        assert asyncio.run(_fetch(url, "SELECT to_regclass('video_pilot_budget_0140_owned')")) == [
            (None,)
        ]
        _assert_success(_run(["-m", "alembic", "upgrade", FUTURE_HEAD], cwd=rollback_root, url=url))
        assert (
            _run(
                ["-m", "alembic", "downgrade", ROLLBACK_HEAD], cwd=rollback_root, url=url
            ).returncode
            != 0
        )
        assert asyncio.run(_fetch(url, "SELECT version_num FROM alembic_version")) == [
            (FUTURE_HEAD,)
        ]
    finally:
        fixture_revision.unlink()
    assert not fixture_revision.exists()
    assert asyncio.run(_fetch(url, "SELECT version_num FROM alembic_version")) == [(FUTURE_HEAD,)]
    assert (
        asyncio.run(
            _fetch(
                url,
                "SELECT slug, limit_usd, created_at FROM video_pilot_budgets "
                "WHERE slug <> :slug ORDER BY slug",
                {"slug": C11_REMAKE_PILOT_SLUG},
            )
        )
        == accounts_before
    )
    assert (
        asyncio.run(
            _fetch(
                url,
                "SELECT id, slug, status, max_usd FROM video_pilot_budget_operations "
                "WHERE operation_id = 'pre-ledger-history' ORDER BY slug",
            )
        )
        == holds_before
    )
    assert (
        asyncio.run(
            _fetch(
                url,
                "SELECT slug, account_created, account_created_at "
                "FROM video_pilot_budget_0139_owned",
            )
        )
        == c20_owner_before
    )
    account = asyncio.run(
        _fetch(
            url,
            "SELECT slug, limit_usd, created_at FROM video_pilot_budgets WHERE slug=:slug",
            {"slug": C11_REMAKE_PILOT_SLUG},
        )
    )
    c11_owner = asyncio.run(
        _fetch(
            url,
            "SELECT slug, account_created, account_created_at FROM video_pilot_budget_0140_owned",
        )
    )
    assert len(account) == len(c11_owner) == 1
    assert account[0][0] == c11_owner[0][0] == C11_REMAKE_PILOT_SLUG
    assert Decimal(str(account[0][1])) == Decimal("25")
    assert c11_owner[0][1] is True and c11_owner[0][2] == account[0][2]

    # The old image must preserve later evidence. This operation is disposable test data.
    asyncio.run(
        _execute(
            url,
            "INSERT INTO video_pilot_budget_operations "
            "(id, slug, operation_id, category, provider, model, max_usd, status, attempts) "
            "VALUES (:id, :slug, 'later-uncertain', 'speech', 'test', 'test', 1, 'uncertain', 1)",
            {"id": uuid4(), "slug": C11_REMAKE_PILOT_SLUG},
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
    _assert_success(_run(ready_arguments, cwd=rollback_root, url=url))
    held = _run(
        [
            "-c",
            "import asyncio\nfrom decimal import Decimal\n"
            "from app.db import SessionFactory, engine\n"
            "from app.video_budget import service\n"
            f"slugs=({C20_PILOT_SLUG!r},)\n"
            "async def check():\n"
            " async with SessionFactory() as session:\n"
            "  for slug in slugs:\n"
            "   try:\n"
            "    await service.reserve(session, slug=slug, operation_id='must-refuse', "
            "category='speech', provider='test', model='test', max_usd=Decimal('1'))\n"
            "   except service.BudgetError as error:\n"
            "    assert error.code == 'video_budget_preproduction_hold', error.code\n"
            "   else:\n"
            "    raise AssertionError('everyday-story paid dispatch was admitted')\n"
            " await engine.dispose()\n"
            "asyncio.run(check())",
        ],
        cwd=rollback_root,
        url=url,
    )
    _assert_success(held)

    # Unknown revisions, ledger drift, missing ownership, damaged PK and
    # unavailable DB must all refuse the old image's Compose migrate command.
    asyncio.run(_execute(url, "UPDATE alembic_version SET version_num='0140_unreviewed_test'"))
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    assert _run(ready_arguments, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(
        _execute(url, "UPDATE alembic_version SET version_num=:revision", {"revision": FUTURE_HEAD})
    )
    for slug in (C11_REMAKE_PILOT_SLUG, C20_PILOT_SLUG):
        asyncio.run(
            _execute(
                url,
                "UPDATE video_pilot_budgets SET limit_usd=5 WHERE slug=:slug",
                {"slug": slug},
            )
        )
        assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
        asyncio.run(
            _execute(
                url,
                "UPDATE video_pilot_budgets SET limit_usd=25 WHERE slug=:slug",
                {"slug": slug},
            )
        )
    for ownership_table in ("video_pilot_budget_0139_owned", "video_pilot_budget_0140_owned"):
        asyncio.run(_execute(url, f"UPDATE {ownership_table} SET account_created=false"))
        assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
        asyncio.run(_execute(url, f"UPDATE {ownership_table} SET account_created=true"))
    asyncio.run(
        _execute(
            url,
            "UPDATE video_pilot_budget_0140_owned SET account_created_at=now() + interval '1 day'",
        )
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(
        _execute(
            url,
            "UPDATE video_pilot_budget_0140_owned SET account_created_at="
            "(SELECT created_at FROM video_pilot_budgets WHERE slug=:slug)",
            {"slug": C11_REMAKE_PILOT_SLUG},
        )
    )
    asyncio.run(
        _execute(
            url,
            "ALTER TABLE video_pilot_budget_0140_owned "
            "DROP CONSTRAINT video_pilot_budget_0140_owned_pkey",
        )
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(
        _execute(
            url,
            "ALTER TABLE video_pilot_budget_0140_owned "
            "ADD CONSTRAINT video_pilot_budget_0140_owned_pkey PRIMARY KEY (slug)",
        )
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode == 0
    asyncio.run(
        _execute(
            url,
            "UPDATE video_pilot_budget_operations SET status='reserved' "
            "WHERE slug='story-everyday-moleskine-c03' "
            "AND operation_id='pre-ledger-history'",
        )
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(
        _execute(
            url,
            "UPDATE video_pilot_budget_operations SET status='uncertain' "
            "WHERE slug='story-everyday-moleskine-c03' "
            "AND operation_id='pre-ledger-history'",
        )
    )
    asyncio.run(_execute(url, "DROP INDEX ix_video_pilot_budget_operations_slug"))
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
    asyncio.run(
        _execute(
            url,
            "CREATE INDEX ix_video_pilot_budget_operations_slug "
            "ON video_pilot_budget_operations (slug)",
        )
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode == 0
    unavailable = url.set(host="127.0.0.1", port=1)
    assert _run(migrate_command, cwd=rollback_root, url=unavailable).returncode != 0

    asyncio.run(
        _execute(
            url,
            "DELETE FROM video_pilot_budget_operations WHERE slug=:slug",
            {"slug": C11_REMAKE_PILOT_SLUG},
        )
    )
    asyncio.run(
        _execute(
            url, "DELETE FROM video_pilot_budgets WHERE slug=:slug", {"slug": C11_REMAKE_PILOT_SLUG}
        )
    )
    assert _run(migrate_command, cwd=rollback_root, url=url).returncode != 0
