"""Read the main worker's registration without adopting or starting a video.

An active auto.json is persisted work, not a heartbeat. External/imported producers keep
their own work directories, so absence here says nothing about existing review media.
"""

from __future__ import annotations

import json
import stat
from pathlib import Path

from app.video_reviews.schemas import WorkerState
from app.video_reviews.storage import valid_slug

MAX_STATE_BYTES = 256 * 1024
REGISTERED_STATES: dict[str, WorkerState] = {
    "active": "registered",
    "done": "done",
    "blocked": "blocked",
    "dropped": "dropped",
}


def worker_state(work_dir: str | None, slug: str) -> WorkerState:
    """A bounded, read-only view of canonical auto.json and existing STOP markers."""
    if not work_dir or not valid_slug(slug):
        return "unavailable"
    try:
        base = Path(work_dir).resolve(strict=True)
        if not base.is_dir():
            return "unavailable"
        entry = base / slug
        try:
            project_info = entry.lstat()
        except FileNotFoundError:
            return "not_adopted"
        # automatedVideos uses Dirent.isDirectory(), which excludes symlink entries,
        # including a link to another directory inside the same work base.
        if (
            stat.S_ISLNK(project_info.st_mode)
            or entry.is_junction()
            or not stat.S_ISDIR(project_info.st_mode)
        ):
            return "unavailable"
        project = entry.resolve(strict=True)
        if not project.is_relative_to(base):
            return "unavailable"
        path = (project / "auto.json").resolve()
        if not path.is_relative_to(project):
            return "unavailable"
        try:
            info = path.stat()
        except FileNotFoundError:
            return "not_adopted"
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_STATE_BYTES:
            return "unavailable"
        with path.open("rb") as source:
            raw = source.read(MAX_STATE_BYTES + 1)
        if len(raw) > MAX_STATE_BYTES:
            return "unavailable"
        state = json.loads(raw)
        if not isinstance(state, dict) or state.get("slug") != slug:
            return "unavailable"
        status = state.get("status")
        if not isinstance(status, str) or status not in REGISTERED_STATES:
            return "unavailable"
        result = REGISTERED_STATES[status]
        # Keep a recorded failure/drop visible even when the whole work base is stopped.
        if result in ("blocked", "dropped"):
            return result
        for directory in (base, project):
            stop = (directory / "STOP").resolve()
            if not stop.is_relative_to(directory):
                return "unavailable"
            if stop.exists():
                return "stopped"
        return result
    except (OSError, ValueError, RuntimeError):
        # A missing/unreadable mount or a partial state file is not evidence of no worker.
        return "unavailable"
