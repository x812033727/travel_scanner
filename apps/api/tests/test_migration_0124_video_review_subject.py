"""0124 adds the subject to a review's identity without touching a review.

Guard and offline SQL tests run without a database. The PostgreSQL test creates a
temporary review table in the 0115 shape, shadowing the shared table in its own connection,
so it exercises the real index and constraint statements without touching shared rows.
"""

from __future__ import annotations

import importlib.util
import io
import os
from collections.abc import AsyncIterator
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import cast
from unittest.mock import Mock, call
from uuid import uuid4

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import Table
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError

from app.db import engine
from app.models import VideoReview

MIGRATION = "0124_video_review_subject"
REVIEWS = "video_reviews"
OLD_UNIQUE = "uq_video_review_content_revision"
NO_SUBJECT = "uq_video_review_no_subject"
SUBJECT = "uq_video_review_subject"
POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


def load_migration() -> ModuleType:
    file = Path(__file__).resolve().parents[1] / "migrations" / "versions" / f"{MIGRATION}.py"
    spec = importlib.util.spec_from_file_location(f"migration_{MIGRATION}", file)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(connection: Connection, direction: str) -> None:
    with Operations.context(MigrationContext.configure(connection)):
        getattr(load_migration(), direction)()


def test_the_migration_builds_the_indexes_the_model_declares() -> None:
    migration = load_migration()
    table = cast(Table, VideoReview.__table__)
    declared = {index.name: index for index in table.indexes}
    assert [column.name for column in declared[NO_SUBJECT].columns] == list(
        migration.OLD_IDENTITY
    )
    assert [column.name for column in declared[SUBJECT].columns] == list(
        migration.SUBJECT_IDENTITY
    )
    for name, where in ((NO_SUBJECT, "subject IS NULL"), (SUBJECT, "subject IS NOT NULL")):
        index = declared[name]
        assert index.unique is True
        assert str(index.dialect_options["postgresql"]["where"]) == where
        assert str(index.dialect_options["sqlite"]["where"]) == where
    assert OLD_UNIQUE not in {constraint.name for constraint in table.constraints}


def test_current_model_shape_needs_no_schema_changes(monkeypatch: pytest.MonkeyPatch) -> None:
    migration = load_migration()
    operations = Mock()
    monkeypatch.setattr(migration, "op", operations)
    monkeypatch.setattr(migration, "_offline", lambda: False)
    monkeypatch.setattr(migration, "_indexes", lambda: {NO_SUBJECT, SUBJECT})
    monkeypatch.setattr(migration, "_uniques", set)
    migration.upgrade()
    assert operations.mock_calls == []


def test_the_new_indexes_exist_before_the_old_constraint_goes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    migration = load_migration()
    operations = Mock()
    monkeypatch.setattr(migration, "op", operations)
    monkeypatch.setattr(migration, "_offline", lambda: False)
    monkeypatch.setattr(migration, "_indexes", set)
    monkeypatch.setattr(migration, "_uniques", lambda: {OLD_UNIQUE})
    migration.upgrade()
    # Every existing row satisfies the new indexes, so they go in while the old one still holds.
    assert [entry[0] for entry in operations.mock_calls] == [
        "create_index",
        "create_index",
        "drop_constraint",
    ]
    names = [entry.args[0] for entry in operations.create_index.call_args_list]
    assert names == [NO_SUBJECT, SUBJECT]
    assert operations.drop_constraint.call_args == call(OLD_UNIQUE, REVIEWS, type_="unique")


def test_downgrade_refuses_shared_identities_before_any_schema_change(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    migration = load_migration()
    operations = Mock()
    operations.get_bind.return_value.execute.return_value.scalar.return_value = 1
    monkeypatch.setattr(migration, "op", operations)
    monkeypatch.setattr(migration, "_offline", lambda: False)
    with pytest.raises(RuntimeError, match="several subjects share a review identity"):
        migration.downgrade()
    operations.create_unique_constraint.assert_not_called()
    operations.drop_index.assert_not_called()


@pytest.mark.parametrize("direction", ["upgrade", "downgrade"])
def test_offline_sql_does_not_inspect_a_database(
    direction: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    migration = load_migration()
    monkeypatch.setattr(
        migration.sa,
        "inspect",
        lambda _connection: pytest.fail("offline SQL must not inspect a database"),
    )
    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": output}
    )
    with Operations.context(context):
        getattr(migration, direction)()
    sql = output.getvalue()
    if direction == "upgrade":
        assert (
            f"CREATE UNIQUE INDEX {NO_SUBJECT} ON {REVIEWS} "
            "(project_id, gate, content_sha256, revision) WHERE subject IS NULL"
        ) in sql
        assert (
            f"CREATE UNIQUE INDEX {SUBJECT} ON {REVIEWS} "
            "(project_id, gate, subject, content_sha256, revision) WHERE subject IS NOT NULL"
        ) in sql
        assert sql.index(f"CREATE UNIQUE INDEX {SUBJECT}") < sql.index(
            f"DROP CONSTRAINT {OLD_UNIQUE}"
        )
    else:
        assert "HAVING count(*) > 1 LIMIT 1" in sql
        assert "RAISE EXCEPTION 'several subjects share a review identity" in sql
        assert sql.index("RAISE EXCEPTION") < sql.index(f"ADD CONSTRAINT {OLD_UNIQUE}")
        assert sql.index(f"ADD CONSTRAINT {OLD_UNIQUE}") < sql.index(f"DROP INDEX {SUBJECT}")
        assert f"DROP INDEX {NO_SUBJECT}" in sql


def test_offline_mode_uses_the_operations_context(monkeypatch: pytest.MonkeyPatch) -> None:
    migration = load_migration()
    monkeypatch.setattr(migration.op, "get_context", lambda: SimpleNamespace(as_sql=True))
    assert migration._offline() is True


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def postgres_engine() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


def _names(connection: Connection) -> tuple[set[str], set[str]]:
    inspector = sa.inspect(connection)
    indexes = {str(index["name"]) for index in inspector.get_indexes(REVIEWS)}
    uniques = {str(constraint["name"]) for constraint in inspector.get_unique_constraints(REVIEWS)}
    return indexes, uniques


def _exercise(connection: Connection) -> None:
    with connection.begin() as transaction:
        try:
            connection.execute(
                sa.text(
                    f"CREATE TEMPORARY TABLE {REVIEWS} ("
                    "id uuid PRIMARY KEY, project_id uuid NOT NULL, gate varchar(20) NOT NULL, "
                    "subject varchar(40), content_sha256 varchar(64) NOT NULL, "
                    "revision integer NOT NULL DEFAULT 0, summary varchar(500) NOT NULL, "
                    "status varchar(20) NOT NULL, choice varchar(40), "
                    f"CONSTRAINT {OLD_UNIQUE} UNIQUE (project_id, gate, content_sha256, revision)) "
                    "ON COMMIT DROP"
                )
            )
            project, manifest = uuid4(), "a" * 64
            insert = sa.text(
                f"INSERT INTO {REVIEWS} (id, project_id, gate, subject, content_sha256, "
                "revision, summary, status, choice) VALUES (:id, :project_id, :gate, :subject, "
                ":sha, :revision, :summary, :status, :choice)"
            )
            existing = [
                {"gate": "look", "subject": "bride", "status": "approved", "choice": "B"},
                {"gate": "final", "subject": None, "status": "pending", "choice": None},
            ]
            for row in existing:
                connection.execute(
                    insert,
                    {
                        **row, "id": uuid4(), "project_id": project, "sha": manifest,
                        "revision": 0, "summary": row["gate"],
                    },
                )
            snapshot = sa.text(
                f"SELECT gate, subject, content_sha256, revision, summary, status, choice "
                f"FROM {REVIEWS} ORDER BY gate"
            )
            before = connection.execute(snapshot).all()

            run(connection, "upgrade")
            run(connection, "upgrade")
            indexes, uniques = _names(connection)
            assert {NO_SUBJECT, SUBJECT} <= indexes and OLD_UNIQUE not in uniques
            assert connection.execute(snapshot).all() == before

            def add(gate: str, subject: str | None, revision: int = 0) -> None:
                connection.execute(
                    insert,
                    {
                        "id": uuid4(), "project_id": project, "gate": gate, "subject": subject,
                        "sha": manifest, "revision": revision, "summary": "new",
                        "status": "pending", "choice": None,
                    },
                )

            # A second character of the same manifest is its own review now ...
            add("look", "groom")
            # ... while a subject, or a gate without one, still allows only one.
            for gate, subject in (("look", "bride"), ("final", None)):
                with pytest.raises(IntegrityError):
                    with connection.begin_nested():
                        add(gate, subject)
            add("final", None, 1)

            with pytest.raises(RuntimeError, match="several subjects share a review identity"):
                run(connection, "downgrade")
            assert {SUBJECT, NO_SUBJECT} <= _names(connection)[0]

            # Only the fixture's added rows are removed to exercise the safe reverse path.
            connection.execute(sa.text(f"DELETE FROM {REVIEWS} WHERE summary = 'new'"))
            run(connection, "downgrade")
            indexes, uniques = _names(connection)
            assert OLD_UNIQUE in uniques
            assert not {NO_SUBJECT, SUBJECT} & indexes
            assert connection.execute(snapshot).all() == before
        finally:
            transaction.rollback()


@POSTGRES
@pytest.mark.usefixtures("postgres_engine")
@pytest.mark.asyncio(loop_scope="module")
async def test_postgresql_existing_reviews_new_identity_and_downgrade() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(_exercise)
