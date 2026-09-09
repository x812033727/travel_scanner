"""A run keeps its approved cumulative budget until an explicit administrator resume."""

from typing import Any

DEFAULT_MAX_CALLS = 80
MAX_CONFIGURED_CALLS = 1000


def run_call_limit(request: dict[str, Any] | None) -> int:
    value = (request or {}).get("max_calls", DEFAULT_MAX_CALLS)
    # Missing legacy snapshots retain the original limit; malformed stored caps
    # fail closed instead of granting another budget. Never permit unlimited calls.
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        return 0
    return min(value, MAX_CONFIGURED_CALLS)
