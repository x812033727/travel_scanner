"""Reuse checked audio/media tools without modifying earlier course modules."""
from __future__ import annotations

import importlib

from elementary.shared import PRESCHOOL, audio, build, package, player, verify


def __getattr__(name: str):
    modules = {
        "elementary_visuals": "elementary.visuals",
        "elementary_objects": "elementary.objects",
    }
    if name in modules:
        return importlib.import_module(modules[name])
    if name in {"preschool_visuals", "preschool_objects"}:
        from elementary import shared
        return getattr(shared, name)
    raise AttributeError(name)
