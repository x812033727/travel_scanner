"""Load the existing standalone preschool tools through one explicit bridge.

Those tools retain their original top-level imports for CLI compatibility. New
course modules use the elementary package namespace, keeping artwork names apart.
Artwork imports stay lazy so integrity checks need no optional image libraries.
"""
from __future__ import annotations

import importlib
from pathlib import Path
import sys

PRESCHOOL = Path(__file__).resolve().parent.parent / "preschool"
if str(PRESCHOOL) not in sys.path:
    sys.path.insert(0, str(PRESCHOOL))


def _load(name: str):
    module = importlib.import_module(name)
    if Path(module.__file__).resolve() != (PRESCHOOL / f"{name}.py").resolve():
        raise ImportError(f"Shared pipeline module name is occupied: {name}")
    return module


audio = _load("audio")
build = _load("build")
player = _load("player")
verify = _load("verify_series")
package = _load("package_series")


def __getattr__(name: str):
    artwork = {"preschool_visuals": "visuals", "preschool_objects": "objects"}
    if name in artwork:
        return _load(artwork[name])
    raise AttributeError(name)
