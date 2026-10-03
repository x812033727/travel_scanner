"""Test-session environment.

The integration suite registers one account per test through the real
`/auth/register` endpoint, and the whole suite runs from a single client IP
against one Redis. The product cap of 30 registrations per IP per hour is the
right number for production and the wrong one for a test run that is now past
30: the last module to register got a 429 in CI, with nothing wrong in it.

The per-source read limit is off here for the same reason, from the other end:
one address making thousands of reads is exactly what the suite looks like, and
exactly what the limit exists to notice. The tests that cover it build their own
application and set their own mode, so nothing is lost by leaving it off for
everyone else.

The planner budget is here for the second reason rather than the first. It is
metered per address as well as per account, and one address is what the suite
looks like -- so a run that ever reaches the planner with a key configured would
start handing itself catalogue plans, and the failure would read as a planning
bug rather than as a limit doing its job.

`setdefault` keeps an explicit environment override in charge, and the value
must be in place before `app.config.get_settings()` is first called, which is
why it lives here rather than in a fixture.
"""

from __future__ import annotations

import os

import pytest

from tests import sharding

os.environ.setdefault("AUTH_REGISTER_IP_LIMIT", "500")
os.environ.setdefault("PUBLIC_READ_RATE_LIMIT_MODE", "off")
os.environ.setdefault("AI_PLANNER_IP_BUDGET", "10000")
os.environ.setdefault("AI_PLANNER_USER_BUDGET", "1000")


# `--shard INDEX/TOTAL` runs one part of the suite, a whole file at a time; ci.yml runs
# the parts as parallel jobs. sharding.py says how files are placed.
def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--shard",
        default=None,
        metavar="INDEX/TOTAL",
        help="run only shard INDEX (from 1) of TOTAL, split by test file",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    value = config.getoption("--shard")
    if not value:
        return
    try:
        index, total = sharding.parse_shard(value)
    except ValueError as error:
        raise pytest.UsageError(str(error)) from None
    files = [item.nodeid.split("::", 1)[0] for item in items]
    mine = set(sharding.assign(files, total, sharding.load_durations())[index - 1])
    kept = [item for item, file in zip(items, files, strict=True) if file in mine]
    deselected = [item for item, file in zip(items, files, strict=True) if file not in mine]
    if deselected:
        config.hook.pytest_deselected(items=deselected)
    items[:] = kept
