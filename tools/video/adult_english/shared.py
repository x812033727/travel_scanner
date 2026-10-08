"""Reuse checked media tools through an explicit, lazy dependency bridge."""
from __future__ import annotations

import importlib

from elementary.shared import PRESCHOOL, audio, build, package, player, verify
from adult_english.config import document_course


def load_source_for_course(path, course: str | None = None) -> dict:
    source = audio.load_source(path, None)
    document_course(source, course)
    return source


def require_output_course(output, course: str) -> None:
    """Existing measured checkpoints can only be resumed by their own course."""
    path = output / "lessons.resolved.json"
    if path.exists():
        document_course(audio.read_json(path), course, allow_empty=True)


def __getattr__(name: str):
    modules = {
        "elementary_visuals": "elementary.visuals",
        "elementary_objects": "elementary.objects",
        "elementary_series_visuals": "elementary_series.visuals",
        "elementary_series_objects": "elementary_series.objects",
    }
    if name in modules:
        return importlib.import_module(modules[name])
    if name in {"preschool_visuals", "preschool_objects"}:
        from elementary import shared
        return getattr(shared, name)
    raise AttributeError(name)


def contains_authored_fields(authored, measured) -> bool:
    """Measurements may add fields but cannot substitute any authored value."""
    if isinstance(authored, dict):
        return isinstance(measured, dict) and all(
            key in measured and contains_authored_fields(value, measured[key])
            for key, value in authored.items())
    if isinstance(authored, list):
        return isinstance(measured, list) and len(authored) == len(measured) and all(
            contains_authored_fields(left, right) for left, right in zip(authored, measured))
    return type(authored) is type(measured) and authored == measured
