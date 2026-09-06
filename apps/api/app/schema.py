from collections.abc import Iterable
from functools import lru_cache
from pathlib import Path

from alembic.config import Config
from alembic.script import Script, ScriptDirectory


def _script_directory() -> ScriptDirectory:
    api_root = Path(__file__).resolve().parents[1]
    config = Config(str(api_root / "alembic.ini"))
    config.set_main_option("script_location", str(api_root / "migrations"))
    return ScriptDirectory.from_config(config)


def migration_revisions() -> list[Script]:
    """Every migration on disk, newest first."""
    return list(_script_directory().walk_revisions())


def migration_heads() -> list[Script]:
    """The revisions nothing else revises. A healthy tree has exactly one."""
    directory = _script_directory()
    return [directory.get_revision(head) for head in directory.get_heads()]


def describe_heads(heads: Iterable[Script]) -> str:
    """One line per head, naming the file and what it revises.

    Two branches cut on the same day both take the next migration number; each is
    fine alone and the second one to merge gives alembic two heads. The fix is a
    renumber, and it is obvious only if the message says which two files collided.
    """
    return "\n".join(
        f"  {script.revision} (revises {script.down_revision}) in {Path(script.path).name}"
        for script in heads
    )


@lru_cache
def expected_schema_revision() -> str:
    heads = migration_heads()
    if len(heads) != 1:
        raise RuntimeError(
            f"Expected exactly one database migration head, found {len(heads)}:\n"
            f"{describe_heads(heads)}\n"
            "Renumber the later migration so it revises the other one."
        )
    return heads[0].revision


def schema_is_current(current_revision: str | None) -> bool:
    return current_revision == expected_schema_revision()
