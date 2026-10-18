"""Bind each season to its artwork and every shared rendering dependency."""
from __future__ import annotations

from pathlib import Path

from elementary.profile import ElementaryRenderer, RENDERER as FIRST_SEASON_RENDERER
from elementary_series.shared import PRESCHOOL, audio


class ElementarySeriesRenderer(ElementaryRenderer):
    name = "sunny-pip-elementary-complete-v2"
    version = 2

    def source_paths(self) -> dict[str, Path]:
        directory = Path(__file__).resolve().parent
        elementary = directory.parent / "elementary"
        return {
            **{f"elementary_series/{name}": directory / name for name in
               ("visuals.py", "objects.py", "profile.py", "shared.py")},
            **{f"elementary/{name}": elementary / name for name in
               ("visuals.py", "objects.py", "profile.py", "shared.py")},
            **{f"preschool/{name}": PRESCHOOL / name for name in
               ("visuals.py", "objects.py", "build.py")},
        }

    def render_frame(self, episode: dict, scene: dict, t: float, duration: float):
        from elementary_series.visuals import render_frame
        return render_frame(episode, scene, t, duration)


RENDERER = ElementarySeriesRenderer()


def renderer_for(episode: dict):
    season = episode.get("season")
    if type(season) is not int or not 1 <= season <= 6:
        raise audio.PipelineError(f"{episode.get('id', '?')}: expected elementary season 1–6")
    return FIRST_SEASON_RENDERER if season == 1 else RENDERER
