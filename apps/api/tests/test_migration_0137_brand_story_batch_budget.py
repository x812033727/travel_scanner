"""The October story budget migration seeds only the reviewed first batch."""

from __future__ import annotations

import importlib.util
import io
from pathlib import Path
from unittest.mock import patch

import pytest
from alembic.migration import MigrationContext
from alembic.operations import Operations

from app.video_budget.models import NEW_BRAND_STORY_SLUGS, PILOT_LIMIT_USD

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "migrations"
    / "versions"
    / "0137_brand_story_batch_budget.py"
)


def test_brand_story_accounts_seed_at_usd_25_without_touching_prior_exposure() -> None:
    spec = importlib.util.spec_from_file_location(SOURCE.stem, SOURCE)
    assert spec is not None and spec.loader is not None
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    assert migration.down_revision == "0136_video_languages_eight"
    assert len(migration.revision) <= 32
    assert set(migration.BRAND_STORIES) == NEW_BRAND_STORY_SLUGS
    assert PILOT_LIMIT_USD == 25

    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql", opts={"as_sql": True, "output_buffer": output}
    )
    with Operations.context(context):
        migration.upgrade()
    sql = output.getvalue()
    assert sql.count("INSERT INTO video_pilot_budgets") == len(NEW_BRAND_STORY_SLUGS)
    assert sql.count("ON CONFLICT (slug) DO NOTHING") == len(NEW_BRAND_STORY_SLUGS)
    assert "UPDATE video_pilot_budgets" not in sql
    assert "DELETE FROM video_pilot_budget_operations" not in sql

    inserts = []
    with patch.object(migration.op, "execute", side_effect=inserts.append):
        migration.upgrade()
    params = [insert.compile().params for insert in inserts]
    assert {row["slug"] for row in params} == NEW_BRAND_STORY_SLUGS
    assert all(row["limit_usd"] == PILOT_LIMIT_USD for row in params)

    with pytest.raises(RuntimeError, match="cannot be removed automatically"):
        migration.downgrade()
