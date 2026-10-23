"""One source-bound junior-high renderer for all six newly produced seasons."""
from __future__ import annotations

from pathlib import Path

from elementary.profile import ElementaryRenderer
from junior_high.shared import PRESCHOOL, audio


class JuniorHighRenderer(ElementaryRenderer):
    name = "sunny-pip-junior-high-v1"
    version = 1

    def source_paths(self) -> dict[str, Path]:
        directory = Path(__file__).resolve().parent
        sources = {}
        for package in ("junior_high", "elementary_series", "elementary"):
            for name in ("visuals.py", "objects.py", "profile.py", "shared.py"):
                sources[f"{package}/{name}"] = directory.parent / package / name
        for name in ("visuals.py", "objects.py", "build.py", "audio.py"):
            sources[f"preschool/{name}"] = PRESCHOOL / name
        from junior_high.objects import FONT_PATHS
        sources.update({f"fonts/{path.name}": path for path in FONT_PATHS})
        return sources

    def render_frame(self, episode: dict, scene: dict, t: float, duration: float):
        from junior_high.visuals import render_frame
        return render_frame(episode, scene, t, duration)


RENDERER = JuniorHighRenderer()


def renderer_for(episode: dict):
    season = episode.get("season")
    if type(season) is not int or not 1 <= season <= 6:
        raise audio.PipelineError(f"{episode.get('id', '?')}: expected junior-high season 1–6")
    return RENDERER
