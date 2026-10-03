"""Split the suite across CI jobs by test file: `pytest --shard 2/4`.

The api job ran the whole suite in one process and took 23 of its 25 minutes in
pytest (CI run 37111019702, 2026-10-03). ci.yml now runs it as several shards, each
in its own job with its own PostgreSQL, Redis and S3 companion, so no test shares a
database with a test running at the same moment.

Whole files go to one shard, never single tests: module-scoped fixtures and the
modules that import each other's fixtures then run exactly as they do unsharded.
Files are placed longest first on the shard with the least estimated time, using
the per-file seconds in shard_durations.json; a file that is not listed there is
estimated at the median of the ones that are, so a new test file never needs the
JSON updated before it can run. Every shard collects the same items and computes
the same assignment, so each file runs in exactly one shard.

To refresh the estimates after the suite has grown or moved, run the suite with a
JUnit report and rewrite the JSON from it:

    RUN_INTEGRATION_TESTS=1 uv run pytest --junitxml=/tmp/junit.xml
    uv run python tests/sharding.py /tmp/junit.xml > tests/shard_durations.json
"""

from __future__ import annotations

import json
import statistics
import sys
import xml.etree.ElementTree as ElementTree
from collections import defaultdict
from pathlib import Path

DURATIONS_FILE = Path(__file__).with_name("shard_durations.json")


def parse_shard(value: str) -> tuple[int, int]:
    """`"2/4"` -> `(2, 4)`; the index counts from 1, as the matrix in ci.yml does."""
    index_text, sep, total_text = value.partition("/")
    try:
        if not sep:
            raise ValueError
        index, total = int(index_text), int(total_text)
    except ValueError:
        raise ValueError(f"--shard takes INDEX/TOTAL, such as 2/4, not {value!r}") from None
    if total < 1 or not 1 <= index <= total:
        raise ValueError(f"--shard {value}: INDEX must be between 1 and TOTAL")
    return index, total


def load_durations(path: Path = DURATIONS_FILE) -> dict[str, float]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {str(name): float(seconds) for name, seconds in data.items()}


def assign(files: list[str], total: int, durations: dict[str, float]) -> list[list[str]]:
    """Each file in exactly one of `total` shards, longest first onto the lightest shard."""
    known = [durations[name] for name in files if name in durations]
    fallback = statistics.median(known) if known else 1.0
    shards: list[list[str]] = [[] for _ in range(total)]
    load = [0.0] * total
    for name in sorted(set(files), key=lambda name: (-durations.get(name, fallback), name)):
        lightest = min(range(total), key=lambda shard: (load[shard], shard))
        shards[lightest].append(name)
        load[lightest] += durations.get(name, fallback)
    return shards


def durations_from_junit(paths: list[Path], root: Path) -> dict[str, float]:
    """Seconds per test file, summed over every testcase in the given JUnit reports.

    pytest's default report names a test by a dotted `classname`
    (`tests.test_x.TestY`) rather than by file, so the longest prefix of it that is an
    existing `.py` file under `root` is the file.
    """
    seconds: dict[str, float] = defaultdict(float)
    for path in paths:
        # A report pytest just wrote on this machine, not data from elsewhere.
        for case in ElementTree.parse(path).iter("testcase"):  # noqa: S314
            parts = case.get("classname", "").split(".")
            for end in range(len(parts), 0, -1):
                candidate = "/".join(parts[:end]) + ".py"
                if (root / candidate).is_file():
                    seconds[candidate] += float(case.get("time") or 0)
                    break
    return {name: round(value, 1) for name, value in sorted(seconds.items())}


if __name__ == "__main__":
    reports = [Path(argument) for argument in sys.argv[1:]]
    if not reports:
        sys.exit("usage: python tests/sharding.py JUNIT.xml [JUNIT.xml ...]")
    root = Path(__file__).resolve().parent.parent
    print(json.dumps(durations_from_junit(reports, root), indent=2, ensure_ascii=False))
