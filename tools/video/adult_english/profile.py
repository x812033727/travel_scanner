"""One source-bound renderer for university and workplace English courses."""
from __future__ import annotations

from pathlib import Path

from elementary.profile import ElementaryRenderer
from adult_english.shared import PRESCHOOL, audio


class AdultEnglishRenderer(ElementaryRenderer):
    name = "sunny-pip-adult-english-v1"
    version = 1

    def source_paths(self) -> dict[str, Path]:
        directory = Path(__file__).resolve().parent
        sources = {}
        for package in ("adult_english", "elementary_series", "elementary"):
            for name in ("visuals.py", "objects.py", "profile.py", "shared.py"):
                sources[f"{package}/{name}"] = directory.parent / package / name
        sources["adult_english/config.py"] = directory / "config.py"
        for name in ("visuals.py", "objects.py", "build.py", "audio.py"):
            sources[f"preschool/{name}"] = PRESCHOOL / name
        from adult_english.objects import FONT_PATHS
        sources.update({f"fonts/{path.name}": path for path in FONT_PATHS})
        return sources

    def render_frame(self, episode: dict, scene: dict, t: float, duration: float):
        from adult_english.visuals import render_frame
        return render_frame(episode, scene, t, duration)


RENDERER = AdultEnglishRenderer()


def renderer_for(episode: dict):
    course, season, stage = episode.get("course"), episode.get("season"), episode.get("stage")
    if (course not in {"university", "workplace"} or type(season) is not int
            or not 1 <= season <= 4 or type(stage) is not int or stage != season
            or "grade" in episode):
        raise audio.PipelineError(f"{episode.get('id', '?')}: expected an adult course with matching season/stage 1–4 and no grade")
    return RENDERER
