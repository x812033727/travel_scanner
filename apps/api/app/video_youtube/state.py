"""The shape of ``video_projects.youtube_sync``: one video's request and its steps. Pure functions.

::

    {
      "status": "queued" | "running" | "done" | "failed",
      "request": {mode, visibility, publish_at, title, description, video_id,
                  review_id, package_sha256, accept_private_lock},
      "steps": [{"id": "upload" | "details" | "captions" | "thumbnail",
                 "state": "pending" | "running" | "done" | "failed" | "skipped",
                 "detail": str, "at": iso | null}],
      "progress": {"sent": int, "total": int} | null,     # the mp4 upload
      "error": str | null,
      "queued_at", "started_at", "finished_at", "lease_until": iso | null,
      "attempts": int
    }

A run holds a lease it renews while it works; a run whose lease ran out (the API restarted
mid-upload) reads as interrupted, and the owner retries it. Every step is safe to run again:
the upload resumes its session, the details are rewritten whole, captions skip the languages
the video already has, and the thumbnail is set again.
"""

from __future__ import annotations

import copy
from datetime import UTC, datetime
from typing import Any

from app.video_youtube.requests import as_dict

STEPS_BY_MODE = {
    "upload": ("upload", "details", "captions", "thumbnail"),
    "studio": ("details", "captions", "thumbnail"),
}
# What the owner's request keeps; the page reads all of it back to fill the form again.
PUBLIC_REQUEST_FIELDS = (
    "mode",
    "visibility",
    "publish_at",
    "title",
    "description",
    "video_id",
    "accept_private_lock",
)


def now_text(now: datetime | None = None) -> str:
    return (now or datetime.now(UTC)).isoformat()


def parse_time(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def new_state(request: dict[str, Any]) -> dict[str, Any]:
    """A queued run of ``request``, every step of its mode still to do."""
    steps = [
        {"id": step, "state": "pending", "detail": "", "at": None}
        for step in STEPS_BY_MODE[str(request["mode"])]
    ]
    return {
        "status": "queued",
        "request": dict(request),
        "steps": steps,
        "progress": None,
        "error": None,
        "queued_at": now_text(),
        "started_at": None,
        "finished_at": None,
        "lease_until": None,
        "attempts": 0,
    }


def retried(state: dict[str, Any]) -> dict[str, Any]:
    """The same request queued again: done steps stay done, the rest start over."""
    result = copy.deepcopy(state)
    for step in result.get("steps", []):
        if step.get("state") != "done":
            step.update(state="pending", detail="", at=None)
    result.update(status="queued", error=None, queued_at=now_text(), finished_at=None)
    result["lease_until"] = None
    return result


def running(state: dict[str, Any] | None, now: datetime | None = None) -> bool:
    """Whether a run holds this video now: queued or running, with a lease that has not lapsed.

    A queued run has no lease yet; it counts as held for a minute after it was queued, which is
    how long the task it launched has to pick it up.
    """
    if not state or state.get("status") not in ("queued", "running"):
        return False
    moment = now or datetime.now(UTC)
    lease = parse_time(state.get("lease_until"))
    if lease is not None:
        return lease > moment
    queued = parse_time(state.get("queued_at"))
    return queued is not None and (moment - queued).total_seconds() < 60


def interrupted(state: dict[str, Any] | None, now: datetime | None = None) -> bool:
    """A run that says it is going but holds no lease: the API restarted under it."""
    if not state or state.get("status") not in ("queued", "running"):
        return False
    return not running(state, now)


def step(state: dict[str, Any], step_id: str) -> dict[str, Any] | None:
    return next((item for item in state.get("steps", []) if item.get("id") == step_id), None)


def public_state(
    state: dict[str, Any] | None, now: datetime | None = None
) -> dict[str, Any] | None:
    """What the page may see: no lease, no attempt bookkeeping, and an ``interrupted`` flag."""
    if not state:
        return None
    request = as_dict(state.get("request"))
    return {
        "status": state.get("status"),
        "interrupted": interrupted(state, now),
        "request": {key: request.get(key) for key in PUBLIC_REQUEST_FIELDS if key in request},
        "steps": [
            {key: item.get(key) for key in ("id", "state", "detail", "at")}
            for item in state.get("steps", [])
            if isinstance(item, dict)
        ],
        "progress": state.get("progress"),
        "error": state.get("error"),
        "queued_at": state.get("queued_at"),
        "started_at": state.get("started_at"),
        "finished_at": state.get("finished_at"),
    }
