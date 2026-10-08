"""One source-bound senior-high renderer for all six newly produced seasons."""
from __future__ import annotations

from pathlib import Path

from elementary.profile import ElementaryRenderer
from senior_high.shared import PRESCHOOL, audio


class SeniorHighRenderer(ElementaryRenderer):
    name = "sunny-pip-senior-high-v1"
    version = 1

    def source_paths(self) -> dict[str, Path]:
        directory = Path(__file__).resolve().parent
        sources = {}
        for package in ("senior_high", "elementary_series", "elementary"):
            for name in ("visuals.py", "objects.py", "profile.py", "shared.py"):
                sources[f"{package}/{name}"] = directory.parent / package / name
        for name in ("visuals.py", "objects.py", "build.py", "audio.py"):
            sources[f"preschool/{name}"] = PRESCHOOL / name
        from senior_high.objects import FONT_PATHS
        sources.update({f"fonts/{path.name}": path for path in FONT_PATHS})
        return sources

    def render_frame(self, episode: dict, scene: dict, t: float, duration: float):
        from senior_high.visuals import render_frame
        return render_frame(episode, scene, t, duration)


RENDERER = SeniorHighRenderer()


def renderer_for(episode: dict):
    season = episode.get("season")
    if type(season) is not int or not 1 <= season <= 6:
        raise audio.PipelineError(f"{episode.get('id', '?')}: expected senior-high season 1–6")
    return RENDERER
