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


_DRAWINGS: dict[str, object] = {}


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
        target = PUBLIC / "guides" / slug
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
