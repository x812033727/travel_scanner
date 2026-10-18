"""Source-bound elementary artwork profile; no mutation of shared renderers."""
from __future__ import annotations

from pathlib import Path

from elementary.shared import PRESCHOOL, build


class ElementaryRenderer:
    name = "sunny-pip-elementary-season-one-v1"
    version = 1

    def source_paths(self) -> dict[str, Path]:
        directory = Path(__file__).resolve().parent
        return {
            **{f"elementary/{name}": directory / name for name in
               ("visuals.py", "objects.py", "profile.py", "shared.py")},
            **{f"preschool/{name}": PRESCHOOL / name for name in
               ("visuals.py", "objects.py", "build.py")},
        }

    def fingerprint(self, fps: int, library: dict | None = None) -> str:
        return build.fingerprint({
            "profile": self.name, "profile_version": self.version,
            "sources": {name: build.file_sha256(path) for name, path in self.source_paths().items()},
            "fps": fps, "render_version": build.RENDER_VERSION,
            "resolution": [1280, 720], "output_fps": 30, "crf": 22,
            "render_library": library or build.render_library(),
        })

    def recorded_fingerprint(self, record: dict, fps: int) -> str | None:
        library = record.get("render_library")
        if (record.get("renderer_profile") != self.name
                or record.get("renderer_version") != build.RENDER_VERSION
                or not isinstance(library, dict) or library.get("name") != "Pillow"
                or not library.get("version")):
            return None
        return self.fingerprint(fps, library)

    def render_frame(self, episode: dict, scene: dict, t: float, duration: float):
        from elementary.visuals import render_frame
        return render_frame(episode, scene, t, duration)


RENDERER = ElementaryRenderer()
