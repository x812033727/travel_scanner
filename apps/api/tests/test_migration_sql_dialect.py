"""Guard the SQL that only ever runs on the production database.

``0001_initial`` builds the schema from the *current* models, so a fresh CI database
already has every column a later migration adds. Every backfill written as
``if "x" not in columns:`` is therefore dead code in CI and runs for the first time in
production. This file reads that SQL as text and rejects the operators that would fail
there — the cheapest stand-in for a database old enough to enter those branches.

The columns it watches come from the models, not from a list kept by hand: the list this
file started with named three tables when the models had forty-two with a ``JSON``
column, and ``0052`` wrote ``food_merchants.names_json`` — correctly, as it happens —
without this test reading a line of it.
"""

import re
from collections.abc import Iterable
from pathlib import Path

from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import JSONB

import app.models  # noqa: F401  (registers every table on Base.metadata)
from app.db import Base

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"

# json (not jsonb) columns: the containment, key-test, concatenation and key-deletion
# operators do not resolve for them, and PostgreSQL raises at parse time, so an empty
# table is no protection. ``->`` and ``->>`` are fine on json; so is every ``json_*``
# function. ``jsonb_set(config, ...)`` fails the same way the operators do.
JSONB_ONLY_OPERATORS = ("?", "?|", "?&", "@>", "<@", "||", "-")


def json_columns() -> dict[str, tuple[str, ...]]:
    """Every ``JSON`` column in the models, by table — ``JSONB`` columns are not json."""
    found: dict[str, tuple[str, ...]] = {}
    for table in Base.metadata.sorted_tables:
        columns = tuple(
            column.name
            for column in table.columns
            if isinstance(column.type, JSON) and not isinstance(column.type, JSONB)
        )
        if columns:
            found[table.name] = columns
    return found


JSON_COLUMNS = json_columns()


def statements_with_json_columns(
    sources: Iterable[tuple[str, str]],
) -> list[tuple[str, str, str]]:
    """``(file, column, line)`` for every non-comment line that names a json column of a
    table the file mentions."""
    found = []
    for name, source in sources:
        for table, columns in JSON_COLUMNS.items():
            if table not in source:
                continue
            for line in source.splitlines():
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                for column in columns:
                    if re.search(rf"\b{re.escape(column)}\b", stripped):
                        found.append((name, column, stripped))
    return found


def migration_sources() -> list[tuple[str, str]]:
    return [
        (path.name, path.read_text(encoding="utf-8")) for path in sorted(VERSIONS.glob("0*.py"))
    ]


def _misuses(column: str, line: str) -> bool:
    """Whether ``line`` applies a jsonb-only operator or function to ``column`` itself."""
    name = re.escape(column)
    # Quoted literals hold regexes of their own ('...?$'), so read the SQL with them
    # blanked out.
    sql = re.sub(r"'[^']*'", "''", line)
    # ``column::jsonb`` and ``CAST(column AS jsonb)`` are the sanctioned way to use these
    # operators: what follows them is jsonb, not this column.
    sql = re.sub(rf"\b{name}\b\s*::\s*jsonb\b", "<jsonb>", sql, flags=re.I)
    sql = re.sub(rf"\bCAST\(\s*{name}\s+AS\s+jsonb\s*\)", "<jsonb>", sql, flags=re.I)
    if re.search(rf"\bjsonb_\w+\(\s*{name}\b", sql, flags=re.I):
        return True
    # Only an operator with this column as one of its operands counts: ``name || ' x'`` on
    # a line that also reads ``names_json`` is text concatenation, and ``data ->> 'k'`` is
    # the json operator, not ``-``.
    for operator in JSONB_ONLY_OPERATORS:
        symbol = re.escape(operator)
        if re.search(rf"\b{name}\b\s*{symbol}\s", sql) or re.search(
            rf"\s{symbol}\s*\b{name}\b", sql
        ):
            return True
    return False


def offenders_in(sources: Iterable[tuple[str, str]]) -> list[str]:
    return [
        f"{name}: {line}"
        for name, column, line in statements_with_json_columns(sources)
        if _misuses(column, line)
    ]


def test_the_column_list_comes_from_the_models_and_is_not_empty() -> None:
    """The guard below must not be satisfiable by the derivation quietly finding nothing."""
    assert len(JSON_COLUMNS) >= 40, JSON_COLUMNS
    assert sum(len(columns) for columns in JSON_COLUMNS.values()) >= 60
    assert JSON_COLUMNS["trip_plans"] == ("data",)
    assert JSON_COLUMNS["provider_configs"] == ("config",)
    assert "names_json" in JSON_COLUMNS["food_merchants"]


def test_no_migration_uses_a_jsonb_operator_on_a_json_column() -> None:
    offenders = offenders_in(migration_sources())
    assert not offenders, (
        "these lines use a jsonb-only operator against a json column; they will fail "
        "at parse time on a production database old enough to run them:\n" + "\n".join(offenders)
    )


def test_the_guard_reads_every_json_column_not_just_the_three_it_started_with() -> None:
    fake = (
        "9999_fake.py",
        """
def upgrade() -> None:
    op.execute("UPDATE food_merchants SET names_json = names_json || '{}'::jsonb")
    op.execute("DELETE FROM hotspot_localizations WHERE aliases ? 'old'")
    op.execute("UPDATE trip_plans SET data = data - 'plus_code'")
    op.execute("UPDATE provider_configs SET config = jsonb_set(config, '{a}', '1')")
    op.execute("SELECT id FROM travel_hotspots WHERE '{\\"x\\": 1}' <@ metadata_json")
""",
    )
    offenders = offenders_in([fake])
    assert len(offenders) == 5, offenders
    assert all(line.startswith("9999_fake.py: ") for line in offenders)


def test_the_guard_accepts_the_sanctioned_shapes() -> None:
    fine = (
        "9998_fine.py",
        """
def upgrade() -> None:
    # A jsonb operator on the column cast to jsonb: the shape 0032 and 0068 use.
    op.execute("UPDATE trip_plans SET data = (data::jsonb - 'plus_code_global')::json "
               "WHERE data::jsonb ? 'plus_code_global'")
    op.execute("UPDATE provider_configs SET config = jsonb_set(config::jsonb, '{a}', '1')::json")
    op.execute("UPDATE food_merchants SET names_json = CAST(:names AS json) "
               "WHERE names_json IS NULL OR TRIM(names_json::text) IN :empty")
    op.execute("UPDATE trip_plans SET notes = nullif(trim(data ->> 'notes'), '')")
    op.execute("UPDATE food_merchants SET name = name || ' (closed)' WHERE names_json IS NULL")
    op.execute("UPDATE trip_plans SET data = CAST(data AS jsonb) - 'k' WHERE (data ->> 'k') = '1'")
""",
    )
    assert offenders_in([fine]) == []


def test_the_notes_backfill_still_moves_the_brief_into_its_column() -> None:
    """The guard above must not be satisfiable by deleting the backfill."""
    source = (VERSIONS / "0042_trip_notes.py").read_text(encoding="utf-8")
    assert "UPDATE trip_plans" in source
    assert "SET notes = data ->> 'notes'" in source
    assert "nullif(trim(data ->> 'notes'), '')" in source
