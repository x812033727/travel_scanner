"""The saved-count index must appear on an older shape and be a no-op on a fresh one."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations

from app.community.models import Collection, CollectionItem
from app.db import Base
from app.models import User


def migration():
    path = Path(__file__).parents[1] / "migrations/versions/0071_collection_item_lookup.py"
    spec = importlib.util.spec_from_file_location("collection_item_lookup_migration", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def indexes(connection):
    return {row["name"] for row in sa.inspect(connection).get_indexes("community_collection_items")}


@pytest.mark.parametrize("fresh_metadata", [False, True])
def test_upgrade_adds_the_reference_index_once_and_downgrade_removes_it(
    monkeypatch, fresh_metadata
):
    module = migration()
    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    engine = sa.create_engine("sqlite://")
    with engine.begin() as connection:
        Base.metadata.create_all(
            connection, tables=[User.__table__, Collection.__table__, CollectionItem.__table__]
        )
        if not fresh_metadata:
            # 0001 creates current metadata; an older database reaches 0071 without it.
            connection.execute(sa.text(f"DROP INDEX {module.INDEX}"))
            assert module.INDEX not in indexes(connection)
        with Operations.context(MigrationContext.configure(connection)):
            module.upgrade()
            assert module.INDEX in indexes(connection)
            module.upgrade()
            assert module.INDEX in indexes(connection)
            module.downgrade()
            assert module.INDEX not in indexes(connection)
            module.downgrade()
            assert module.INDEX not in indexes(connection)
    engine.dispose()


def test_the_model_carries_the_index_so_a_fresh_install_is_already_current():
    index = next(
        (
            item
            for item in CollectionItem.__table__.indexes
            if item.name == "ix_community_collection_item_reference"
        ),
        None,
    )
    assert index is not None
    assert [column.name for column in index.columns] == ["kind", "target"]
