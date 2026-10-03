from __future__ import annotations

from pathlib import Path

import pytest

from tests import sharding


def test_every_file_lands_in_exactly_one_shard() -> None:
    files = [f"tests/test_{number}.py" for number in range(23)]
    shards = sharding.assign(files, 4, {})
    placed = [name for shard in shards for name in shard]
    assert sorted(placed) == sorted(files)
    assert all(shards)


def test_the_assignment_is_the_same_whatever_order_files_are_collected_in() -> None:
    files = [f"tests/test_{number}.py" for number in range(10)]
    durations = {name: float(index % 4) for index, name in enumerate(files)}
    assert sharding.assign(files, 3, durations) == sharding.assign(files[::-1], 3, durations)


def test_long_files_are_spread_before_short_ones_fill_in() -> None:
    durations = {"tests/a.py": 100.0, "tests/b.py": 90.0, "tests/c.py": 10.0, "tests/d.py": 5.0}
    shards = sharding.assign(list(durations), 2, durations)
    assert shards == [["tests/a.py", "tests/d.py"], ["tests/b.py", "tests/c.py"]]


def test_an_unlisted_file_is_estimated_at_the_median() -> None:
    durations = {"tests/a.py": 10.0, "tests/b.py": 20.0, "tests/c.py": 30.0}
    shards = sharding.assign([*durations, "tests/new.py"], 2, durations)
    # c (30) and b (20) take one shard each, then a (10) and new (median 20) balance them.
    assert shards == [["tests/c.py", "tests/a.py"], ["tests/b.py", "tests/new.py"]]


@pytest.mark.parametrize("value", ["2", "0/4", "5/4", "a/b", "1/0"])
def test_a_malformed_shard_is_refused(value: str) -> None:
    with pytest.raises(ValueError):
        sharding.parse_shard(value)


def test_durations_are_summed_per_file_from_a_junit_report(tmp_path: Path) -> None:
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_x.py").write_text("")
    report = tmp_path / "junit.xml"
    report.write_text(
        "<testsuites><testsuite>"
        '<testcase classname="tests.test_x" name="a" time="1.25"/>'
        '<testcase classname="tests.test_x.TestY" name="b" time="2.5"/>'
        "</testsuite></testsuites>"
    )
    assert sharding.durations_from_junit([report], tmp_path) == {"tests/test_x.py": 3.8}
