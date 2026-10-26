"""The channel intro and outro the site's worker builds with, read from its work volume.

``node tools/video/cli.mjs branding --install DIR`` copies a package into
``<work>/_branding/<hash>/`` and points ``_branding/current.json`` at it (a series:
``_branding/series/<series>/current.json``; tools/video/core/branding.mjs). The media stay out of
git (docs/videos/BRANDING.md), so a tool on another machine, a cloud container first of all, had
no bookends unless someone copied them by hand: three cloud cuts came out without an intro or an
outro on 2026-10-19. The API mounts the work volume read-only, and ``branding --pull`` fetches the
current package through here. Nothing here writes, and only files a current.json names are served.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

# currentBrandingFile in tools/video/core/branding.mjs: the only series with its own bookends.
SERIES = frozenset({"sothatswhy"})
FPS = 30
# validateBranding: a bookend is 1 to 30 seconds.
MAX_FRAMES = FPS * 30
_SHA256 = re.compile(r"^[0-9a-f]{64}$")

Reason = Literal["not_installed", "disabled", "broken"]


class BrandingUnavailable(Exception):
    """Why there is no package to hand out: none installed (or no volume), switched off, or
    a current.json the tool itself would refuse."""

    def __init__(self, reason: Reason, detail: str = "") -> None:
        super().__init__(detail or reason)
        self.reason: Reason = reason


@dataclass(frozen=True)
class Clip:
    sha256: str
    frames: int
    path: Path
    size: int


@dataclass(frozen=True)
class Package:
    series: str | None
    id: str
    hash: str
    installed_at: str | None
    intro: Clip
    outro: Clip


def _current_file(root: Path, series: str | None) -> Path:
    if series is None:
        return root / "_branding" / "current.json"
    return root / "_branding" / "series" / series / "current.json"


def _clip(value: object, *, base: Path, branding_dir: Path, role: str) -> Clip:
    if not isinstance(value, dict):
        raise BrandingUnavailable("broken", f"{role} is missing")
    file, sha256, frames = value.get("file"), value.get("sha256"), value.get("frames")
    if not isinstance(file, str) or not file.strip():
        raise BrandingUnavailable("broken", f"{role} has no file")
    if not isinstance(sha256, str) or not _SHA256.match(sha256.lower()):
        raise BrandingUnavailable("broken", f"{role} has no SHA-256")
    if isinstance(frames, bool) or not isinstance(frames, int) or not 0 < frames <= MAX_FRAMES:
        raise BrandingUnavailable("broken", f"{role} needs 1-{MAX_FRAMES} frames")
    try:
        path = (base / file).resolve()
        inside = path.is_relative_to(branding_dir.resolve()) and path.is_file()
        size = path.stat().st_size if inside else 0
    except OSError:
        inside, size = False, 0
    if not inside:
        raise BrandingUnavailable("broken", f"{role} is not a file under _branding")
    return Clip(sha256=sha256.lower(), frames=frames, path=path, size=size)


def current_package(work_dir: str | None, series: str | None = None) -> Package:
    """The package the worker's next first build pins, as its current.json names it."""
    if series is not None and series not in SERIES:
        raise BrandingUnavailable("not_installed", f"no series {series}")
    if not work_dir:
        raise BrandingUnavailable("not_installed")
    root = Path(work_dir)
    file = _current_file(root, series)
    try:
        text = file.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise BrandingUnavailable("not_installed") from error
    except OSError as error:
        raise BrandingUnavailable("broken", "current.json cannot be read") from error
    try:
        value = json.loads(text)
    except ValueError as error:
        raise BrandingUnavailable("broken", "current.json is not JSON") from error
    if isinstance(value, dict) and value.get("enabled") is False:
        raise BrandingUnavailable("disabled")
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise BrandingUnavailable("broken", "current.json needs schema_version 1")
    package_id, digest = value.get("id"), value.get("hash")
    if not isinstance(package_id, str) or not package_id.strip():
        raise BrandingUnavailable("broken", "current.json has no id")
    if not isinstance(digest, str) or not _SHA256.match(digest):
        raise BrandingUnavailable("broken", "current.json has no hash")
    branding_dir = root / "_branding"
    installed_at = value.get("installed_at")
    return Package(
        series=series,
        id=package_id.strip(),
        hash=digest,
        installed_at=installed_at if isinstance(installed_at, str) else None,
        intro=_clip(value.get("intro"), base=file.parent, branding_dir=branding_dir, role="intro"),
        outro=_clip(value.get("outro"), base=file.parent, branding_dir=branding_dir, role="outro"),
    )


def current_file(work_dir: str | None, sha256: str) -> Path | None:
    """An intro or outro of a current package (the channel's or a series'), by its SHA-256."""
    for series in (None, *sorted(SERIES)):
        try:
            package = current_package(work_dir, series)
        except BrandingUnavailable:
            continue
        for clip in (package.intro, package.outro):
            if clip.sha256 == sha256:
                return clip.path
    return None
