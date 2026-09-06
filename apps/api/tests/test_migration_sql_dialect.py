"""Guard the SQL that only ever runs on the production database.

``0001_initial`` builds the schema from the *current* models, so a fresh CI database
already has every column a later migration adds. Every backfill written as
``if "x" not in columns:`` is therefore dead code in CI and runs for the first time in
production. This file reads that SQL as text and rejects the operators that would fail
there — the cheapest stand-in for a database old enough to enter those branches.
"""

import re
from pathlib import Path

VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"

# json (not jsonb) columns: the containment and key-test operators do not resolve for
# them, and PostgreSQL raises at parse time, so an empty table is no protection.
JSONB_ONLY_OPERATORS = ("?", "?|", "?&", "@>", "<@")

JSON_COLUMNS = {
    "trip_plans": ("data",),
    "trip_plan_items": ("data",),
    "provider_configs": ("config",),
}


def statements_with_json_columns() -> list[tuple[str, str]]:
    found = []
    for path in sorted(VERSIONS.glob("0*.py")):
        source = path.read_text(encoding="utf-8")
        for table, columns in JSON_COLUMNS.items():
            if table not in source:
                continue
            for line in source.splitlines():
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if any(column in stripped for column in columns):
                    found.append((path.name, stripped))
    return found


def test_no_migration_uses_a_jsonb_operator_on_a_json_column() -> None:
    offenders = []
    for name, line in statements_with_json_columns():
        # Quoted literals hold regexes of their own ('...?$'), so read the SQL with
        # them blanked out. ``->`` and ``->>`` are fine on json; the key tests are not.
        sql = re.sub(r"'[^']*'", "''", line)
        if "::jsonb" in sql:
            continue  # an explicit cast is the sanctioned way to use these
        for operator in JSONB_ONLY_OPERATORS:
            if re.search(rf"\s{re.escape(operator)}\s", sql):
                offenders.append(f"{name}: {line}")
                break
    assert not offenders, (
        "these lines use a jsonb-only operator against a json column; they will fail "
        "at parse time on a production database old enough to run them:\n" + "\n".join(offenders)
    )


def test_the_notes_backfill_still_moves_the_brief_into_its_column() -> None:
    """The guard above must not be satisfiable by deleting the backfill."""
    source = (VERSIONS / "0042_trip_notes.py").read_text(encoding="utf-8")
    assert "UPDATE trip_plans" in source
    assert "SET notes = data ->> 'notes'" in source
    assert "nullif(trim(data ->> 'notes'), '')" in source
