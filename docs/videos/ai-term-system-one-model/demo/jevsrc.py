"""Load selected definitions verbatim from the repo's apps/api/app/ai/jev.py without importing
the module (which needs redis and app.config). Only the named top-level nodes are executed."""
import ast
import re
from typing import Any, Literal
from pydantic import BaseModel, Field

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # the repository root
JEV = ROOT / "apps/api/app/ai/jev.py"
WANTED = {
    "USD_PER_INPUT_TOKEN", "_CJK", "estimate_tokens",
    "ChoiceQuestion", "ScoreQuestion", "NoulQuestion", "JevQuestion",
    "ChoiceAnswer", "ScoreAnswer", "NoulAnswer", "JevAnswer", "Tier", "route",
}


CLIENT = WANTED | {
    "SYSTEM_ONE_PATH", "VENDOR_MAX_REQUEST_TOKENS", "VENDOR_MAX_STATE_TOKENS", "MAX_CHOICE_OPTIONS",
    "MIN_SCORE_LEVELS", "MAX_SCORE_LEVELS", "JevError", "JevAuthError", "JevRequestInvalid",
    "JevRequestTooLarge", "_ANSWER_TYPES", "JevClient", "_vendor_message",
}


def load(wanted: set | None = None) -> dict:
    tree = ast.parse(open(JEV, encoding="utf-8").read())
    keep = []
    for node in tree.body:
        names = set()
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names = {node.name}
        elif isinstance(node, ast.Assign):
            names = {t.id for t in node.targets if isinstance(t, ast.Name)}
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names = {node.target.id}
        if names & (wanted or WANTED):
            keep.append(node)
    import asyncio, random
    from collections.abc import Mapping
    import httpx
    from pydantic import ValidationError
    ns: dict = {"re": re, "Any": Any, "Literal": Literal, "BaseModel": BaseModel, "Field": Field,
                "asyncio": asyncio, "random": random, "Mapping": Mapping, "httpx": httpx,
                "ValidationError": ValidationError, "__name__": "jevsrc"}
    exec(compile(ast.Module(body=keep, type_ignores=[]), JEV, "exec"), ns)
    missing = (wanted or WANTED) - set(ns)
    assert not missing, missing
    return ns
