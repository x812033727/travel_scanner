"""The two host-side signals that a release is in progress, as the deploy script reads them.

``/root/deploy-travel-scanner.sh`` refuses with exit 3 while either holds (the full rules are
in ``ops/release/README.md``):

1. ``/root/travel-scanner-deploy.hold`` exists. A staged release driver writes it in
   ``prepare`` through ``ops/release/hold.py`` and removes it after its last phase; a person
   may also write one by hand. The first line is the reason, at most 600 bytes; the second
   is JSON with ``target``, ``release_dir``, ``owner``, ``phases`` and ``created_at``.
2. Some ``/root/mokaair-*/state.json`` was modified within 24 hours, holds ``"built_at"``,
   and holds neither ``"activated_at"`` nor ``"failed_at"``: a release that is prepared but
   not activated, whose containers a rebuild would invalidate.

The agent runs from ``/opt`` and cannot import ``ops/release/hold.py``, so this module reads
the same two-line file on its own, and matches the staged-release rule the way the script
does (substring checks on the file, not a parse, so a half-written file still counts).
The paths come from ``AgentConfig`` and never from a request.
"""

from __future__ import annotations

import json
import time
from datetime import UTC, datetime
from pathlib import Path

from deployment_agent.security import sanitize

HOLD_FIRST_LINE_LIMIT = 600  # bytes; what the deploy script prints
STAGED_RELEASE_WINDOW_SECONDS = 24 * 60 * 60
STAGED_RELEASE_STATE_GLOB = "mokaair-*/state.json"

HOLD_ACTIVE = "deployment_hold_active"
STAGED_RELEASE_IN_PROGRESS = "deployment_staged_release_in_progress"


def read_hold(hold_path: Path) -> tuple[str, dict[str, object]] | None:
    """The hold's first line (sanitised, 600 bytes) and its JSON record, or ``None``."""
    try:
        text = hold_path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return None
    except OSError as exc:
        return (f"hold file exists but could not be read ({exc.__class__.__name__})", {})
    lines = text.splitlines()
    first = (
        lines[0].encode("utf-8")[:HOLD_FIRST_LINE_LIMIT].decode("utf-8", errors="ignore")
        if lines
        else ""
    )
    record: dict[str, object] = {}
    if len(lines) > 1:
        try:
            loaded = json.loads(lines[1])
        except ValueError:
            loaded = None
        if isinstance(loaded, dict):
            record = loaded
    return sanitize(first, HOLD_FIRST_LINE_LIMIT), record


def hold_reason(hold_path: Path) -> str | None:
    hold = read_hold(hold_path)
    if hold is None:
        return None
    first, record = hold
    if first:
        return first
    owner = sanitize(str(record.get("owner") or ""), 64)
    release_dir = sanitize(str(record.get("release_dir") or ""), 200)
    if owner or release_dir:
        return f"deploy hold held by {owner or 'an unknown driver'} for {release_dir or 'an unknown release'}"
    return "deploy hold file present with no reason written in it"


def staged_release_reason(
    root: Path,
    *,
    now: float | None = None,
    window_seconds: int = STAGED_RELEASE_WINDOW_SECONDS,
) -> str | None:
    """Rule 1 of the deploy script: a release prepared but not activated in the last 24 h."""
    current = time.time() if now is None else now
    try:
        candidates = sorted(root.glob(STAGED_RELEASE_STATE_GLOB))
    except OSError:
        return None
    for state in candidates:
        try:
            modified = state.stat().st_mtime
            if current - modified > window_seconds:
                continue
            text = state.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if '"built_at"' in text and '"activated_at"' not in text and '"failed_at"' not in text:
            stamp = datetime.fromtimestamp(modified, tz=UTC).replace(microsecond=0).isoformat()
            return (
                f"a staged release is prepared but not activated: {sanitize(state.parent.name, 120)} "
                f"(state.json modified {stamp})"
            )
    return None


def release_in_progress(hold_path: Path, staged_root: Path) -> tuple[str, str] | None:
    """``(failure_code, reason)`` when the deploy script would refuse, else ``None``."""
    reason = hold_reason(hold_path)
    if reason:
        return HOLD_ACTIVE, reason
    reason = staged_release_reason(staged_root)
    if reason:
        return STAGED_RELEASE_IN_PROGRESS, reason
    return None
