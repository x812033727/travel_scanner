"""Links that open a video's Google Drive backup from the admin (owner, 2026-11-18).

The worker looks up the Drive ids of a backed-up video's folder and of its ``final.mp4`` with
``rclone lsjson --stat`` and reports them (``POST /video/automation/backup/{slug}/drive``); they
are kept in ``video_projects.backup["drive"]`` with the folder they were read for. A link is
offered only while that folder is still the video's, so a moved or renamed folder shows no
stale link until the worker reads the new ids. No imports from the app: the review page's
summaries read it too.
"""

from __future__ import annotations

from typing import Any

FOLDER_URL = "https://drive.google.com/drive/folders/{id}"
FILE_URL = "https://drive.google.com/file/d/{id}/view"
# The states whose folder holds a checked copy, so its ids are worth reading.
BACKED_UP = frozenset({"done", "partial"})


def drive_record(record: Any, folder: str | None) -> dict[str, Any] | None:
    """The stored ids when they were read for ``folder``, else None."""
    if not isinstance(record, dict) or not folder:
        return None
    drive = record.get("drive")
    if not isinstance(drive, dict) or drive.get("folder") != folder:
        return None
    return drive if isinstance(drive.get("folder_id"), str) else None


def drive_links(record: Any, folder: str | None) -> tuple[str | None, str | None]:
    """``(folder_url, final_url)`` for the folder, either None when unknown."""
    drive = drive_record(record, folder)
    if drive is None:
        return None, None
    final = drive.get("final_file_id")
    return (
        FOLDER_URL.format(id=drive["folder_id"]),
        FILE_URL.format(id=final) if isinstance(final, str) and final else None,
    )


def needs_drive_ids(record: Any, folder: str | None) -> bool:
    """A backed-up video whose ids for ``folder`` the site does not have yet."""
    return (
        isinstance(record, dict)
        and record.get("state") in BACKED_UP
        and drive_record(record, folder) is None
    )
