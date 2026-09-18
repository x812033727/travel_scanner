"""The fixed values of the AI workflow tutorial series, in one place (the way ``verticals.py`` holds
the news verticals'). ``check_article.py`` and ``build_assets.py`` import from here.

Twelve articles and a hub, zh-TW only, registered as the ``ai-workflow`` series under the
``ai-coding`` topic. ``display_order`` follows the news verticals' convention of "hub one below
the band": the hub is 399, the articles 400-411 in the order of ``SLUGS``.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps/api"))
CONTENT = ROOT / "apps/api/app/guides/content"
PUBLIC = ROOT / "apps/web/public/guides"
WORKSPACE = ROOT / "docs/ai-workflow-series"
RESEARCH = WORKSPACE / "research"

SERIES = "ai-workflow"
HUB = "ai-workflow-tutorials"
HUB_TITLE = "多模型 AI 工作流教學：從拆任務到串接不同模型"
TOPICS = ("ai", "tutorial", "ai-coding")
ORDER_BASE = 400
HUB_ORDER = ORDER_BASE - 1
EYEBROW = "MOKAAIR  /  AI WORKFLOW"
LOCALE = "zh-TW"
SLUGS = (
    "ai-workflow-basics",
    "ai-workflow-split-tasks-across-models",
    "ai-workflow-cost-quality-latency",
    "ai-workflow-unified-api-layer",
    "ai-workflow-model-routing-cascade",
    "ai-workflow-structured-handoff",
    "ai-workflow-cross-review-judge",
    "ai-workflow-coding-agents-division",
    "ai-workflow-mcp-shared-tools",
    "ai-workflow-local-and-cloud-mix",
    "ai-workflow-tracing-evals",
    "ai-workflow-failures-and-guardrails",
)
#: Articles the assignment marks 入門: no code block is required of them.
INTRO = SLUGS[:3]


def order_of(slug: str) -> int:
    if slug == HUB:
        return HUB_ORDER
    return ORDER_BASE + SLUGS.index(slug)


def load(name: str, path: Path):
    """Import one of the earlier batches' scripts by path, so their helpers are reused rather
    than copied (the news batch does the same for the AI batches' drawing primitives)."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    # Registered before it runs: ``verticals.py`` declares a dataclass, and ``dataclasses``
    # looks the defining module up in ``sys.modules`` while decorating it.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
