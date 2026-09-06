"""The migration tree must have one head, and only that head counts as current.

Migration numbers are picked when a branch is cut, so two branches cut on the same
day both take the next number. Each is green alone; the second one to merge gives
alembic two heads and ``expected_schema_revision()`` raises for every test module
that imports the app. This file runs as its own CI step, before ``alembic upgrade``
and before the rest of the suite, so that failure is the first line of the log and
names both revisions. A pull request checkout is the merge with its base, so the
check sees the tree the merge would produce, not the branch alone.
"""

import re
import types

from app.schema import (
    describe_heads,
    expected_schema_revision,
    migration_heads,
    migration_revisions,
    schema_is_current,
)

NUMBERED = re.compile(r"^(\d{4})_")


def test_the_migration_tree_has_exactly_one_head() -> None:
    heads = migration_heads()
    assert len(heads) == 1, (
        f"{len(heads)} alembic heads; renumber the later one so it revises the other:\n"
        + describe_heads(heads)
    )


def test_the_head_carries_the_highest_migration_number() -> None:
    """A new file numbered below the head would still be a second head, or worse,
    a renumber that left the old number in the ``revision`` string."""
    head = expected_schema_revision()
    assert len(head) <= 32  # alembic_version.version_num is VARCHAR(32)
    numbers = {}
    for script in migration_revisions():
        match = NUMBERED.match(script.revision)
        assert match, f"{script.revision} does not start with a four-digit number"
        numbers[script.revision] = int(match.group(1))
    assert numbers[head] == max(numbers.values()), (
        f"head {head} is not the highest-numbered migration: "
        f"{max(numbers, key=numbers.__getitem__)} is"
    )


def test_no_other_revision_counts_as_current() -> None:
    head = expected_schema_revision()
    others = [script.revision for script in migration_revisions() if script.revision != head]
    assert len(others) >= 40
    assert all(schema_is_current(revision) is False for revision in others)
    assert schema_is_current(head) is True
    assert schema_is_current(None) is False


def _script(revision: str, down_revision: str) -> types.SimpleNamespace:
    return types.SimpleNamespace(
        revision=revision,
        down_revision=down_revision,
        path=f"/repo/migrations/versions/{revision}.py",
    )


def test_a_double_head_is_reported_with_both_files_and_their_parents() -> None:
    message = describe_heads(
        [
            _script("0044_localized_names", "0043_trip_expenses"),
            _script("0044_trip_notes", "0043_trip_expenses"),
        ]
    )
    assert "0044_localized_names (revises 0043_trip_expenses) in 0044_localized_names.py" in message
    assert "0044_trip_notes (revises 0043_trip_expenses) in 0044_trip_notes.py" in message
