"""Read the main worker's registration without adopting or starting a video.

An active auto.json is persisted work, not a heartbeat. External/imported producers keep
their own work directories, so absence here says nothing about existing review media.
"""

from __future__ import annotations

import json
import stat
from pathlib import Path
from typing import NamedTuple

from app.video_reviews.schemas import WorkerState
from app.video_reviews.storage import valid_slug

MAX_STATE_BYTES = 256 * 1024
REGISTERED_STATES: dict[str, WorkerState] = {
    "active": "registered",
    "done": "done",
    "blocked": "blocked",
    "dropped": "dropped",
}


class WorkerView(NamedTuple):
    """What one bounded read of auto.json says: the registration, and when the worker cleared
    the video's work files (``tidied_at``, as written; None while it has not, or when the value
    is not a string). A cleared video has no cut, narration or takes left to make a dub from."""

    state: WorkerState
    tidied_at: str | None


UNAVAILABLE = WorkerView("unavailable", None)
NOT_ADOPTED = WorkerView("not_adopted", None)


def worker_view(work_dir: str | None, slug: str) -> WorkerView:
    """A bounded, read-only view of canonical auto.json and existing STOP markers."""
    if not work_dir or not valid_slug(slug):
        return UNAVAILABLE
    try:
        base = Path(work_dir).resolve(strict=True)
        if not base.is_dir():
            return UNAVAILABLE
        entry = base / slug
        try:
            project_info = entry.lstat()
        except FileNotFoundError:
            return NOT_ADOPTED
        # automatedVideos uses Dirent.isDirectory(), which excludes symlink entries,
        # including a link to another directory inside the same work base.
        if (
            stat.S_ISLNK(project_info.st_mode)
            or entry.is_junction()
            or not stat.S_ISDIR(project_info.st_mode)
        ):
            return UNAVAILABLE
        project = entry.resolve(strict=True)
        if not project.is_relative_to(base):
            return UNAVAILABLE
        path = (project / "auto.json").resolve()
        if not path.is_relative_to(project):
            return UNAVAILABLE
        try:
            info = path.stat()
        except FileNotFoundError:
            return NOT_ADOPTED
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_STATE_BYTES:
            return UNAVAILABLE
        with path.open("rb") as source:
            raw = source.read(MAX_STATE_BYTES + 1)
        if len(raw) > MAX_STATE_BYTES:
            return UNAVAILABLE
        state = json.loads(raw)
        if not isinstance(state, dict) or state.get("slug") != slug:
            return UNAVAILABLE
        status = state.get("status")
        if not isinstance(status, str) or status not in REGISTERED_STATES:
            return UNAVAILABLE
        result = REGISTERED_STATES[status]
        # Read before the early return below: a blocked video may have been cleared too.
        tidied = state.get("tidied_at")
        tidied_at = tidied if isinstance(tidied, str) and tidied else None
        # Keep a recorded failure/drop visible even when the whole work base is stopped.
        if result in ("blocked", "dropped"):
            return WorkerView(result, tidied_at)
        for directory in (base, project):
            stop = (directory / "STOP").resolve()
            if not stop.is_relative_to(directory):
                return UNAVAILABLE
            if stop.exists():
                return WorkerView("stopped", tidied_at)
        return WorkerView(result, tidied_at)
    except (OSError, ValueError, RuntimeError):
        # A missing/unreadable mount or a partial state file is not evidence of no worker.
        return UNAVAILABLE


def worker_state(work_dir: str | None, slug: str) -> WorkerState:
    """The registration alone, for callers that do not need the tidy date."""
    return worker_view(work_dir, slug).state
