"""Original hero illustrations and one diagram per article for the AI workflow tutorial series.

``build_assets.py [--svg-only] [--slug=<slug>]...`` -- every article whose research record
exists under ``research/``, or only the ones named. Reuses the drawing primitives, the palette
and the credit line of the news batches (``docs/ai-news-2026-09``, ``docs/ai-news-2026-ytd``,
``docs/news-2026-batch-4``) so the series stays in the album's style, and adds what a tutorial
needs that a news piece does not:

* no date on the hero (a tutorial has ``news_date: null``; its currency is the ``checked_on``
  of its sources, which the caption of every diagram states);
* two diagram layouts instead of the news batches' fixed 2×2 -- ``flow`` draws three to five
  steps left to right joined by arrows, which is what a workflow is, and ``grid`` keeps the 2×2
  for the articles that compare four things (the research record's ``diagram.layout`` picks).

Writes only this series' image directories under ``apps/web/public/guides`` and, in this
workspace, ``manifest.json``, ``renders/`` (ignored) and the contact sheets. Rendering goes
through ``app.guides.pack_ingest`` like the news batches: ``chromium_binary()`` finds the
headless shell, ``fit_bytes`` keeps a hero at 1600×900 under the byte cap the site enforces.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from series import (  # noqa: E402
    CONTENT,
    EYEBROW,
    HUB,
    LOCALE,
    PUBLIC,
    RESEARCH,
    ROOT,
    SLUGS,
    WORKSPACE,
    load,
)

from app.guides.pack_ingest import (  # noqa: E402
    HERO_MAX_BYTES,
    HERO_SIZE,
    IMAGE_HARD_CAP,
    check_svg,
    chromium_binary,
    errors,
    fit_bytes,
    render_svg,
)

art = load("news_art", ROOT / "docs/ai-news-2026-09/build_assets.py")
ytd = load("news_art_ytd", ROOT / "docs/ai-news-2026-ytd/build_assets.py")
batch4 = load("news_art_batch4", ROOT / "docs/news-2026-batch-4/build_assets.py")
rect, line, circle, label, document, check, envelope = art.rect, art.line, art.circle, art.label, art.document, art.check, art.envelope
chip, monitor, lock = ytd.chip, ytd.monitor, ytd.lock
arrow, dashed, sheet, slot, tick, pending, gear, bubble, cylinder, hexagon, outline = (
    batch4.arrow, batch4.dashed, batch4.sheet, batch4.slot, batch4.tick, batch4.pending, batch4.gear,
    batch4.bubble, batch4.cylinder, batch4.hexagon, batch4.outline,
)
CREAM, INK, TEAL, PALE, BLUE, ORANGE = art.CREAM, art.INK, art.TEAL, art.PALE, art.BLUE, art.ORANGE
ACCENT, OTHER = TEAL, BLUE
CREDIT = "© Mokaair 製圖 2026"
_CHROME: str | None = None


def chrome() -> str:
    global _CHROME
    if _CHROME is None:
        _CHROME = chromium_binary()
    return _CHROME


# --- the drawing vocabulary the series adds ------------------------------------------------
# Never a logo, a wordmark or a screenshot (BRIEF.md). A model is a hexagon, a step is a card,
# a hand-off is an arrow, a check is a tick, a guard is a lock; products are named in text.


def model(x, y, r=60, color=TEAL, fill="#FFFFFF"):
    """A model: the hexagon the news batch drew for one, with a small core."""
    return hexagon(x, y, r, color, fill) + circle(x, y, r * 0.28, color, "none")


def card(x, y, w, h, color=TEAL, fill="#FFFFFF", rows=0):
    """A step or a record: a rounded card with optional text lines."""
    body = rect(x, y, w, h, fill, color, 20)
    for i in range(rows):
        body += line(x + 28, y + 40 + i * 34, x + w - 28 - (i % 2) * 40, y + 40 + i * 34, "#C4CCCC", 10)
    return body


def fork(x, y, color=TEAL):
    """One input splitting into two paths."""
    return line(x, y, x + 90, y, color, 12) + line(x + 90, y, x + 170, y - 90, color, 12) + line(x + 90, y, x + 170, y + 90, color, 12)


def merge(x, y, color=TEAL):
    """Two paths joining into one."""
    return line(x, y - 90, x + 80, y, color, 12) + line(x, y + 90, x + 80, y, color, 12) + line(x + 80, y, x + 170, y, color, 12)


def brace(x, y, h, color=INK):
    """A curly brace-like bracket marking a group."""
    return f'<path d="M{x} {y} q -30 0 -30 30 v {h / 2 - 45} q 0 15 -15 15 q 15 0 15 15 v {h / 2 - 45} q 0 30 30 30" fill="none" stroke="{color}" stroke-width="8" stroke-linecap="round"/>'


# --- one composition per article, filled in as the articles are written -------------------
# Keyed by the whole slug. Every composition is drawn in the accent and the album's other
# colour, at hero scale (1600×900, content between y=200 and y=700, x=200 to x=1400).


def _placeholder(accent: str) -> str:
    """Only for ``--svg-only`` previews before an article has its own drawing; ``drawing()``
    refuses it for a real build so no article ships with a placeholder."""
    return model(800, 450, 90, accent)


def larrow(x1, x2, y, color=TEAL, width=12, broken=False):
    """``arrow`` pointing left: a hand-off back the way it came (a retry, a review)."""
    shaft = dashed(x1 + 14, y, x2, y, color, width) if broken else line(x1 + 14, y, x2, y, color, width)
    return shaft + f'<path d="M{x1 + 36} {y - 30} L{x1} {y} L{x1 + 36} {y + 30}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


def loop(x, y, r, color=TEAL, width=10):
    """A three-quarter circle with a head: a step that runs again until a check passes."""
    arc = f'<path d="M{x + r} {y} A{r} {r} 0 1 1 {x} {y - r}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
    return arc + f'<path d="M{x - 28} {y - r - 26} L{x + 4} {y - r} L{x - 26} {y - r + 30}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


def clock(x, y, r=60, color=TEAL):
    """A dial with two hands: latency."""
    return circle(x, y, r, "#FFFFFF", color) + line(x, y, x, y - r * 0.6, color, 10) + line(x, y, x + r * 0.45, y + r * 0.2, color, 10) + circle(x, y, 7, color, "none")


def coin(x, y, r=50, color=TEAL):
    """Two rings: cost."""
    return circle(x, y, r, PALE, color) + circle(x, y, r * 0.62, "#FFFFFF", color)


def cloud(x, y, w=460, h=300, color=TEAL):
    """One outline of four bumps on a flat base: a model that runs somewhere else."""
    return (
        f'<path d="M{x + w * 0.2} {y + h} H{x + w * 0.8} A{h * 0.26} {h * 0.26} 0 0 0 {x + w * 0.8} {y + h * 0.55} '
        f'A{h * 0.33} {h * 0.33} 0 0 0 {x + w * 0.5} {y + h * 0.28} A{h * 0.36} {h * 0.36} 0 0 0 {x + w * 0.2} {y + h * 0.55} '
        f'A{h * 0.26} {h * 0.26} 0 0 0 {x + w * 0.2} {y + h} Z" fill="#FFFFFF" stroke="{color}" stroke-width="8" stroke-linejoin="round"/>'
    )


def terminal(x, y, w=320, h=260, color=TEAL):
    """A command window: a title bar, a prompt chevron and a few lines of output."""
    body = rect(x, y, w, h, "#FFFFFF", color, 24) + line(x, y + 56, x + w, y + 56, color, 6)
    body += "".join(circle(x + 34 + i * 30, y + 28, 9, PALE if i else color, "none") for i in range(3))
    body += f'<path d="M{x + 36} {y + 96} l 26 22 l -26 22" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
    return body + "".join(line(x + 84 + (i % 2) * 10, y + 118 + i * 40, x + w - 50 - (i % 2) * 60, y + 118 + i * 40, "#C4CCCC", 10) for i in range(3))


def meter(x, y, w, h, ratio, color=TEAL):
    """A bar with a filled part: a confidence score, a budget, a cap."""
    return rect(x, y, w, h, "#FFFFFF", color, h / 2) + f'<rect x="{x + 6}" y="{y + 6}" width="{max(0, (w - 12) * ratio)}" height="{h - 12}" rx="{(h - 12) / 2}" fill="{color}"/>'


def redacted(x, y, w=110, h=130, color=TEAL):
    """A sheet whose lines are blacked out: what stays on the machine."""
    body = sheet(x, y, w, h, color, rows=0)
    return body + "".join(rect(x + 20, y + 34 + i * 30, w - 40 - (i % 2) * 22, 16, INK, "none", 6) for i in range(3))


# --- one composition per article -------------------------------------------------------------


def _basics(accent: str) -> str:
    # A conversation, then a row of steps, then a step that runs on a loop: the three layers
    # the article names -- chat, workflow, agent.
    other = OTHER
    b = bubble(230, 340, 280, 190, accent)
    b += "".join(line(275, 395 + i * 40, 470 - (i % 2) * 70, 395 + i * 40, "#C4CCCC", 10) for i in range(3))
    b += arrow(545, 640, 450, INK, 8)
    for i in range(3):
        x = 645 + i * 165
        b += card(x, 375, 110, 150, accent if i % 2 == 0 else other, PALE if i % 2 == 0 else "#FFFFFF", rows=2)
        if i < 2:
            b += arrow(x + 118, x + 158, 450, INK, 6)
    b += arrow(1100, 1180, 450, INK, 8)
    return b + loop(1300, 450, 120, accent, 10) + model(1300, 450, 72, other)


def _split_tasks(accent: str) -> str:
    # One task card cut four ways, each piece handed to a different model.
    other = OTHER
    b = card(230, 290, 250, 320, accent, PALE, rows=6)
    for i, y in enumerate((255, 385, 515, 645)):
        colour = accent if i % 2 == 0 else other
        b += line(480, 450, 700, y, "#C4CCCC", 8)
        b += card(700, y - 45, 220, 90, colour, "#FFFFFF", rows=1)
        b += arrow(930, 1010, y, INK, 6) + model(1090, y, 46, colour)
    return b


def _cost_quality_latency(accent: str) -> str:
    # Three corners -- a coin, a tick, a clock -- and a marker that can only sit closer to one
    # of them at a time.
    other = OTHER
    b = f'<path d="M 800 250 L 400 640 L 1200 640 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    b += "".join(dashed(x, y, 780, 520, "#C4CCCC", 6) for x, y in ((800, 250), (400, 640), (1200, 640)))
    b += coin(800, 250, 56, accent) + tick(400, 640, 56, other) + clock(1200, 640, 56, accent)
    return b + circle(780, 520, 30, accent, "none") + circle(780, 520, 12, "#FFFFFF", "none")


def _unified_api(accent: str) -> str:
    # One program, one adapter, one bar every model plugs into: change the string, not the code.
    other = OTHER
    b = card(230, 300, 300, 300, accent, "#FFFFFF", rows=6) + arrow(545, 640, 450, INK, 8)
    b += rect(650, 385, 190, 130, PALE, accent, 30) + line(840, 415, 900, 415, accent, 12) + line(840, 485, 900, 485, accent, 12)
    b += rect(900, 240, 44, 420, "#FFFFFF", INK, 16)
    for i, y in enumerate((300, 450, 600)):
        colour = accent if i % 2 == 0 else other
        b += line(944, y, 1080, y, colour, 10) + model(1150, y, 54, colour)
    return b


def _routing_cascade(accent: str) -> str:
    # Three models each a size up, a confidence bar under each; the hand-off to the next is
    # dashed because it only happens when the bar comes up short.
    other = OTHER
    steps = ((380, 560, 50, 0.35), (780, 480, 72, 0.6), (1200, 380, 98, 0.9))
    b = arrow(215, 312, 560, INK, 8)
    for i, (x, y, r, ratio) in enumerate(steps):
        colour = accent if i % 2 == 0 else other
        b += model(x, y, r, colour) + meter(x - 90, y + r + 40, 180, 34, ratio, colour)
        if i < 2:
            nx, ny, nr, _ = steps[i + 1]
            b += dashed(x + r + 20, y - 10, nx - nr - 24, ny + 8, INK, 8)
            b += f'<path d="M{nx - nr - 60} {ny - 14} L{nx - nr - 22} {ny + 8} L{nx - nr - 64} {ny + 26}" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
    return b


def _structured_handoff(accent: str) -> str:
    # Two models and, between them, the sheet both must agree on -- braces round its lines, a
    # tick before it crosses -- and a dashed way back for the retry when it does not.
    other = OTHER
    b = model(330, 450, 80, accent) + arrow(425, 590, 450, INK, 8)
    b += sheet(610, 285, 380, 330, other, rows=0) + brace(690, 340, 220, other)
    b += f'<path d="M910 340 q 30 0 30 30 v 65 q 0 15 15 15 q -15 0 -15 15 v 65 q 0 30 -30 30" fill="none" stroke="{other}" stroke-width="8" stroke-linecap="round"/>'
    b += "".join(line(720, 380 + i * 46, 880 - (i % 2) * 50, 380 + i * 46, "#C4CCCC", 10) for i in range(4))
    b += tick(960, 590, 44, accent) + arrow(1010, 1150, 450, INK, 8) + model(1250, 450, 80, other)
    b += f'<path d="M800 615 V690 H330 V545" fill="none" stroke="{other}" stroke-width="8" stroke-dasharray="26 22" stroke-linecap="round"/>'
    return b + f'<path d="M304 572 L330 540 L356 572" fill="none" stroke="{other}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'


def _cross_review(accent: str) -> str:
    # Two models each hand in a sheet; a third above holds the balance and marks the score.
    other = OTHER
    b = model(330, 520, 62, accent) + arrow(400, 505, 520, INK, 8) + sheet(520, 400, 200, 240, accent, rows=4)
    b += model(1270, 520, 62, other) + larrow(1095, 1200, 520, INK, 8) + sheet(880, 400, 200, 240, other, rows=4)
    b += line(800, 345, 800, 385, INK, 8) + line(620, 385, 980, 385, INK, 10)
    b += f'<path d="M580 385 q 40 50 80 0" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    b += f'<path d="M940 385 q 40 50 80 0" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    return b + model(800, 270, 70, accent, PALE) + tick(800, 470, 34, accent)


def _coding_agents(accent: str) -> str:
    # Three command windows in a row -- plan, change, review -- with the file each hands on
    # riding under the arrow, and a tick where the review comes out clean.
    other = OTHER
    b = ""
    for i, x in enumerate((230, 640, 1050)):
        b += terminal(x, 290, 320, 270, accent if i % 2 == 0 else other)
        if i < 2:
            b += arrow(x + 328, x + 402, 400, INK, 8) + sheet(x + 330, 440, 70, 84, other if i % 2 == 0 else accent, rows=1)
    return b + tick(1210, 640, 36, accent)


def _mcp_shared_tools(accent: str) -> str:
    # One gear -- the tool server -- three models wired to it, a card stating the contract and
    # a lock on the wire: one server, the least access it needs.
    other = OTHER
    b = ""
    for i, (x, y) in enumerate(((380, 290), (380, 610), (1240, 450))):
        colour = accent if i % 2 == 0 else other
        b += line(x, y, 800, 450, colour, 10) + model(x, y, 60, colour)
    b += gear(800, 450, 84, accent) + card(590, 575, 200, 110, other, "#FFFFFF", rows=2)
    return b + lock(960, 400)


def _local_cloud(accent: str) -> str:
    # A machine on the left with its own model and a lock, a dashed line the raw data never
    # crosses -- the sheet that does is blacked out -- and a cloud on the right with the model
    # that finishes the job.
    other = OTHER
    b = rect(230, 270, 430, 360, "#FFFFFF", INK, 28) + model(360, 420, 60, accent) + lock(490, 470)
    b += dashed(800, 230, 800, 670, INK, 8) + arrow(670, 880, 500, INK, 8) + redacted(690, 320, 100, 120, other)
    return b + cloud(900, 300, 460, 300, other) + model(1130, 480, 64, other)


def _tracing_evals(accent: str) -> str:
    # Each step drops a record onto one strip -- the trace -- and two runs of the same test set
    # stand side by side as bars.
    other = OTHER
    b = rect(230, 520, 670, 50, PALE, INK, 25)
    for i, x in enumerate((230, 470, 710)):
        colour = accent if i % 2 == 0 else other
        b += card(x, 250, 190, 140, colour, "#FFFFFF", rows=2)
        b += dashed(x + 95, 396, x + 95, 515, "#C4CCCC", 6) + circle(x + 95, 545, 16, colour, "none")
        if i < 2:
            b += arrow(x + 196, x + 264, 320, INK, 6)
    b += line(1040, 660, 1380, 660, INK, 8) + line(1040, 260, 1040, 660, INK, 8)
    for x, h, colour, fill in ((1075, 190, other, "#FFFFFF"), (1140, 250, accent, PALE), (1240, 140, other, "#FFFFFF"), (1305, 230, accent, PALE)):
        b += rect(x, 660 - h, 55, h, fill, colour, 10)
    return b


def _failures_guardrails(accent: str) -> str:
    # Three hazards, each with its guard: a loop with a counter on it, a fan-out with a budget
    # bar under it, and a sheet fenced off with a lock so what it says stays data.
    other = OTHER
    b = loop(400, 430, 110, INK, 8) + model(400, 430, 58, accent)
    b += rect(455, 240, 90, 70, "#FFFFFF", other, 16) + line(478, 275, 522, 275, other, 10)
    b += "".join(line(730, 430, 920, y, "#C4CCCC", 8) + model(950, y, 30, other) for y in (270, 380, 490, 600))
    b += circle(730, 430, 18, INK, "none") + meter(690, 660, 300, 34, 0.45, accent)
    return b + outline(1120, 260, 280, 330, accent, 36) + sheet(1160, 300, 200, 250, other, rows=4) + lock(1250, 600)


def _hub(accent: str) -> str:
    # The whole series in one line: a request, split three ways across different models,
    # gathered back into one result and checked.
    other = OTHER
    b = bubble(230, 370, 210, 140, accent)
    for i, y in enumerate((300, 440, 580)):
        colour = accent if i % 2 == 0 else other
        b += line(445, 440, 640, y, "#C4CCCC", 8) + line(755, y, 940, 440, "#C4CCCC", 8) + model(700, y, 50, colour)
    b += card(945, 365, 230, 150, accent, PALE, rows=3)
    return b + arrow(1185, 1275, 440, INK, 8) + tick(1335, 440, 52, other)


_DRAWINGS: dict[str, object] = {
    HUB: _hub,
    "ai-workflow-basics": _basics,
    "ai-workflow-split-tasks-across-models": _split_tasks,
    "ai-workflow-cost-quality-latency": _cost_quality_latency,
    "ai-workflow-unified-api-layer": _unified_api,
    "ai-workflow-model-routing-cascade": _routing_cascade,
    "ai-workflow-structured-handoff": _structured_handoff,
    "ai-workflow-cross-review-judge": _cross_review,
    "ai-workflow-coding-agents-division": _coding_agents,
    "ai-workflow-mcp-shared-tools": _mcp_shared_tools,
    "ai-workflow-local-and-cloud-mix": _local_cloud,
    "ai-workflow-tracing-evals": _tracing_evals,
    "ai-workflow-failures-and-guardrails": _failures_guardrails,
}


def drawing(slug: str, accent: str) -> str:
    if slug not in _DRAWINGS:
        raise SystemExit(f"no drawing for {slug}; add one to _DRAWINGS in {Path(__file__).name}")
    return _DRAWINGS[slug](accent)


# --- the build ------------------------------------------------------------------------------


def hero_svg_text(item: dict, doc: dict) -> str:
    """Eyebrow, the drawing, the hero label and the credit -- no date, the one visible
    difference from a news hero."""
    body = label(80, 100, EYEBROW, 34, ACCENT, "start")
    body += drawing(item["slug"], ACCENT)
    body += label(800, 805, item["hero_label"], 48, max_width=1400)
    body += label(1535, 868, CREDIT, 20, "#5C6B6B", "end")
    return art.svg(doc["title"], doc["hero"]["alt"], body)


def diagram_svg_text(data: dict) -> str:
    """``grid``: the album's 2×2, card for card. ``flow``: the same cards laid left to right and
    joined by arrows, three to five of them, sized to fit the row."""
    nodes = data["nodes"]
    layout = data.get("layout", "grid")
    body = label(800, 102, data["title"], 46, max_width=1440)
    if layout == "grid":
        if len(nodes) != 4:
            raise SystemExit(f"{data['title']}: a grid diagram has four nodes, not {len(nodes)}")
        positions = ((110, 180), (850, 180), (110, 500), (850, 500))
        for i, ((x, y), (heading, detail)) in enumerate(zip(positions, nodes)):
            colour = ACCENT if i % 2 == 0 else OTHER
            body += rect(x, y, 640, 245, "#FFFFFF", colour)
            body += circle(x + 63, y + 66, 23, colour, "none")
            body += label(x + 360, y + 91, heading, 44, max_width=510) + label(x + 320, y + 168, detail, 32, "#5C6B6B", max_width=580)
    elif layout == "flow":
        n = len(nodes)
        if not 3 <= n <= 5:
            raise SystemExit(f"{data['title']}: a flow diagram has three to five nodes, not {n}")
        gap = 70
        width = (1440 - gap * (n - 1)) / n
        y, h = 300, 330
        for i, (heading, detail) in enumerate(nodes):
            x = 80 + i * (width + gap)
            colour = ACCENT if i % 2 == 0 else OTHER
            body += rect(x, y, width, h, "#FFFFFF", colour)
            body += circle(x + 50, y + 54, 20, colour, "none") + label(x + 50, y + 66, str(i + 1), 30, "#FFFFFF")
            body += label(x + width / 2, y + 150, heading, 40 if n <= 4 else 34, max_width=width - 40)
            body += label(x + width / 2, y + 240, detail, 28 if n <= 4 else 24, "#5C6B6B", max_width=width - 40)
            if i < n - 1:
                body += arrow(x + width + 8, x + width + gap - 8, y + h / 2, INK, 8)
    else:
        raise SystemExit(f"{data['title']}: layout is grid or flow, not {layout!r}")
    body += label(1540, 865, CREDIT, 20, "#5C6B6B", "end")
    return art.svg(data["title"], data["caption"], body)


def write_svg(path: Path, text: str) -> None:
    problems = errors(check_svg(text))
    if problems:
        raise SystemExit(f"{path.name}: " + "; ".join(str(p) for p in problems))
    path.write_text(text, encoding="utf-8")


def only_slugs() -> set[str]:
    return {a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--slug=")}


def build() -> list[dict]:
    records = sorted(RESEARCH.glob("*.json"))
    renders = WORKSPACE / "renders"
    renders.mkdir(exist_ok=True)
    ignore = WORKSPACE / ".gitignore"
    if not ignore.exists():
        ignore.write_text("renders/\n__pycache__/\n", encoding="utf-8")
    order = {slug: i for i, slug in enumerate((HUB, *SLUGS))}
    research = sorted((json.loads(p.read_text(encoding="utf-8")) for p in records), key=lambda r: order.get(r["slug"], 99))
    only = only_slugs()
    if only:
        research = [item for item in research if item["slug"] in only]
    manifest = []
    for item in research:
        slug = item["slug"]
        if slug not in order:
            raise SystemExit(f"{slug} is not in series.SLUGS")
        pack = json.loads((CONTENT / f"{slug}.json").read_text(encoding="utf-8"))
        doc = pack["locales"][LOCALE]
        target = PUBLIC / slug
        target.mkdir(parents=True, exist_ok=True)
        hero_svg = target / "hero.svg"
        write_svg(hero_svg, hero_svg_text(item, doc))
        diagram_svg = target / "diagram-1.svg"
        write_svg(diagram_svg, diagram_svg_text(item["diagram"]))
        if "--svg-only" not in sys.argv:
            for kind, svg_file in (("hero", hero_svg), ("diagram-1", diagram_svg)):
                png = (renders / f"{slug}-{kind}.png").resolve()
                render_svg(svg_file, png, chromium=chrome())
                if kind == "hero":
                    with Image.open(png) as picture:
                        assert picture.size == HERO_SIZE, picture.size
                        jpeg = target / "hero.jpg"
                        size = fit_bytes(picture, jpeg, HERO_MAX_BYTES, "JPEG", hard_cap=IMAGE_HARD_CAP)
                        assert size == HERO_SIZE, size
                        written = jpeg.stat().st_size
                        if written > HERO_MAX_BYTES:
                            print(f"WARN {jpeg.name}: {written} bytes at the quality floor, over {HERO_MAX_BYTES}; simplify the drawing", flush=True)
            print("rendered", slug, flush=True)
        manifest.append({"slug": slug, "title": item["title"], "url": f"https://mokaair.com/zh-TW/life/{slug}"})
    if not only:
        (WORKSPACE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def sheets(manifest: list[dict]) -> None:
    """Four articles to a sheet, per kind: an agent cannot see what it drew, so someone reads
    these before the series ships."""
    for kind in ("hero", "diagram-1"):
        for start in range(0, len(manifest), 4):
            sheet_img = Image.new("RGB", (1600, 960), CREAM)
            draw = ImageDraw.Draw(sheet_img)
            for j, entry in enumerate(manifest[start:start + 4]):
                with Image.open(WORKSPACE / "renders" / f"{entry['slug']}-{kind}.png") as picture:
                    sheet_img.paste(picture.resize((800, 450)), ((j % 2) * 800, (j // 2) * 480))
                draw.text(((j % 2) * 800 + 15, (j // 2) * 480 + 456), entry["slug"], fill=INK)
            sheet_img.save(WORKSPACE / f"{kind}-sheet-{start // 4 + 1}.jpg", quality=90)


def main() -> None:
    manifest = build()
    if not manifest:
        print("nothing to draw:" if only_slugs() else "no research records yet:", WORKSPACE, flush=True)
        return
    if "--svg-only" not in sys.argv and not only_slugs():
        sheets(manifest)


if __name__ == "__main__":
    main()
