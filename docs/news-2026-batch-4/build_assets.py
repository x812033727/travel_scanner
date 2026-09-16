"""Original hero illustrations and 2×2 diagrams for this batch, in the album's established style.

``build_assets.py [crypto|tech|ai]... [--svg-only]`` -- with no vertical named, every vertical
whose workspace holds research records. Reuses the drawing primitives, the palette and the
diagram layout of the three earlier batches and adds one hero composition per article.
``--svg-only`` writes the SVGs without rendering, and needs no browser to do it. Writes only
this batch's image directories under ``apps/web/public/guides`` and, inside each vertical's
workspace, ``manifest.json``, ``renders/`` with the ``.gitignore`` that keeps it and any
``__pycache__`` out of the repository, and the contact sheets.

Rendering goes through ``app.guides.pack_ingest``: ``chromium_binary()`` finds the headless
shell this container installs under ``/opt/pw-browsers`` when there is rendering to do, and
``fit_bytes`` is what keeps a published hero at 1600×900 under the byte cap the site enforces.
Batch 3 carried its own browser discovery, inherited from a Windows workstation -- it globs
``%LOCALAPPDATA%\\ms-playwright`` and otherwise falls back to an Edge path under
``C:\\Program Files``, so it finds nothing here.

The three verticals share one album: same palette, same 2×2 layout, same credit line. What
differs is the eyebrow printed on every hero and the accent, which reaches the eyebrow, the
date and the diagram's cards.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from verticals import (  # noqa: E402
    BY_NAME,
    CONTENT,
    LOCALES,
    PUBLIC,
    ROOT,
    VERTICALS,
    suffix,
    vertical_of,
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


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Resolved from the repository root rather than from this file's neighbours, so the batch
# directory can be moved or run from a copy without losing the two earlier batches' primitives.
art = _load("news_art", ROOT / "docs/ai-news-2026-09/build_assets.py")
ytd = _load("news_art_ytd", ROOT / "docs/ai-news-2026-ytd/build_assets.py")
rect, line, circle, label, document, check, envelope = art.rect, art.line, art.circle, art.label, art.document, art.check, art.envelope
chip, monitor, lock = ytd.chip, ytd.monitor, ytd.lock
CREAM, INK, TEAL, PALE, BLUE, ORANGE = art.CREAM, art.INK, art.TEAL, art.PALE, art.BLUE, art.ORANGE
CREDITS = {"zh-TW": "© Mokaair 製圖 2026", "zh-CN": "© Mokaair 制图 2026", "en": "© Mokaair Illustration 2026", "ja": "© Mokaair 作図 2026", "ko": "© Mokaair 제작 2026"}
# Each vertical's accent is one of the album's own six colours, not a new one.
for _vertical in VERTICALS:
    assert _vertical.accent in (TEAL, BLUE, ORANGE), _vertical
_CHROME: str | None = None


def chrome() -> str:
    """The browser, found on first use and kept for the rest of the run. Resolved here rather
    than at import because ``--svg-only`` is documented to write the drawings without rendering
    them, and ``chromium_binary()`` raises when it finds nothing: at import that refusal reaches
    a machine with no browser before ``main()`` has read the flag that says it needs none."""
    global _CHROME
    if _CHROME is None:
        _CHROME = chromium_binary()
    return _CHROME


# --- the drawing vocabulary ---------------------------------------------------------------
# Never a logo, a wordmark, an icon set or a screenshot: the marks are not ours and a drawn
# interface is out of date the day it changes (BRIEF.md "圖像"). Products are named in text.


def phone(x, y, w=230, h=420, stroke=INK):
    return rect(x, y, w, h, "#FFFFFF", stroke, 36) + rect(x + 22, y + 50, w - 44, h - 110, PALE, "none", 16) + circle(x + w / 2, y + h - 32, 12, stroke, "none")


def wave(x, y, bars, color, gap=30):
    heights = [40, 90, 140, 90, 60, 120, 70, 40][:bars]
    return "".join(line(x + i * gap, y - h / 2, x + i * gap, y + h / 2, color, 14) for i, h in enumerate(heights))


def sparkle(x, y, r, color=BLUE):
    return f'<path d="M{x} {y-r} C{x+r*0.18} {y-r*0.18} {x+r*0.18} {y-r*0.18} {x+r} {y} C{x+r*0.18} {y+r*0.18} {x+r*0.18} {y+r*0.18} {x} {y+r} C{x-r*0.18} {y+r*0.18} {x-r*0.18} {y+r*0.18} {x-r} {y} C{x-r*0.18} {y-r*0.18} {x-r*0.18} {y-r*0.18} {x} {y-r} Z" fill="{color}"/>'


def key(x, y, color=ORANGE):
    return circle(x, y, 46, "#FFFFFF", color) + circle(x, y, 14, color, "none") + line(x + 46, y, x + 190, y, color, 18) + line(x + 150, y, x + 150, y + 42, color, 16) + line(x + 185, y, x + 185, y + 30, color, 16)


def shield(x, y, s=1.0):
    return f'<path d="M{x} {y-200*s} L{x+180*s} {y-135*s} V{y} Q{x+180*s} {y+150*s} {x} {y+230*s} Q{x-180*s} {y+150*s} {x-180*s} {y} V{y-135*s} Z" fill="{PALE}" stroke="{TEAL}" stroke-width="10"/>'


def warning(x, y, r=70):
    return f'<path d="M{x} {y-r} L{x+r*1.1} {y+r*0.8} L{x-r*1.1} {y+r*0.8} Z" fill="#F0DBC4" stroke="{ORANGE}" stroke-width="8" stroke-linejoin="round"/>' + line(x, y - r * 0.35, x, y + r * 0.25, ORANGE, 12) + circle(x, y + r * 0.52, 7, ORANGE, "none")


def calendar_small(x, y):
    return rect(x, y, 250, 120, "#FFFFFF", TEAL, 18) + rect(x + 4, y + 4, 242, 36, PALE, "none", 14) + "".join(circle(x + 50 + c * 50, y + 80, 9, TEAL, "none") for c in range(4))


# Added for the two new verticals. Same three primitives, same weights, no new colours.


def chain(x, y, count=3, color=TEAL, size=130, gap=70):
    """Linked blocks: a ledger, a protocol upgrade, a sequence of records."""
    body = ""
    for i in range(count):
        left = x + i * (size + gap)
        body += rect(left, y, size, size, "#FFFFFF", color, 22)
        if i:
            body += line(left - gap, y + size / 2, left, y + size / 2, color, 12)
    return body


def scales(x, y, color=TEAL, arm=180):
    """A balance: a regulator weighing something. Law, licensing, a ruling."""
    body = line(x, y - 150, x, y + 150, color, 14) + line(x - arm, y - 150, x + arm, y - 150, color, 14)
    body += line(x - 110, y + 150, x + 110, y + 150, color, 14) + circle(x, y - 150, 18, color, "none")
    for side in (-1, 1):
        edge = x + side * arm
        body += line(edge, y - 150, edge, y - 60, color, 8)
        body += f'<path d="M{edge-70} {y-60} L{edge+70} {y-60} L{edge+40} {y+10} L{edge-40} {y+10} Z" fill="{PALE}" stroke="{color}" stroke-width="8" stroke-linejoin="round"/>'
    return body


def certificate(x, y, w=260, h=320, color=TEAL):
    """A document with a seal: a licence, a registration, a filing."""
    body = rect(x, y, w, h, "#FFFFFF", color)
    body += "".join(line(x + 36, y + 60 + i * 46, x + w - 36 - (i % 2) * 40, y + 60 + i * 46, "#C4CCCC", 12) for i in range(4))
    return body + circle(x + w - 62, y + h - 62, 40, PALE, color) + line(x + w - 62, y + h - 22, x + w - 82, y + h + 30, color, 10) + line(x + w - 62, y + h - 22, x + w - 42, y + h + 30, color, 10)


def tower(x, y, color=BLUE, h=260):
    """A mast with two arcs: spectrum, a network, a standard being carried."""
    body = line(x - 70, y + h, x, y, color, 12) + line(x + 70, y + h, x, y, color, 12) + line(x - 45, y + h * 0.55, x + 45, y + h * 0.55, color, 10)
    for r in (70, 120):
        body += f'<path d="M{x-r} {y-r*0.55} A{r} {r} 0 0 1 {x+r} {y-r*0.55}" fill="none" stroke="{color}" stroke-width="9" stroke-linecap="round"/>'
    return body + circle(x, y, 16, color, "none")


def drawing(slug: str, accent: str) -> str:
    """The hero composition of one article. One branch per article, added as it is written --
    an original drawing per article is the point, so an unknown slug stops the run rather than
    quietly reusing someone else's picture."""
    raise SystemExit(f"no drawing for {slug}; add a branch to drawing() in {Path(__file__).name}")


# --- the build ------------------------------------------------------------------------------


def second_colour(accent: str) -> str:
    """The album's other colour beside an accent, for the date and the diagram's even cards.
    TEAL and BLUE are the pair batch 3 drew every diagram in, so the AI vertical keeps exactly
    the picture it has shipped since batch 1 and the two new verticals get their own accent
    against the same blue."""
    return TEAL if accent == BLUE else BLUE


def hero_svg_text(vertical, item: dict, doc: dict, localized: dict, locale: str) -> str:
    """The eyebrow and its colour are the only things the vertical changes: same cream ground,
    same 2×2 diagram beside it, same credit line, so the three verticals stay one album.
    ``diagram_svg_text`` writes its own credit, so only the hero adds one here."""
    date_colour = second_colour(vertical.accent)
    body = label(80, 100, vertical.eyebrow, 34, vertical.accent, "start")
    body += label(1510, 100, item["event_date"], 28, date_colour, "end")
    body += drawing(item["slug"], vertical.accent)
    body += label(800, 805, localized.get("hero_label", item["hero_label"]), 48, max_width=1400)
    body += label(1535, 868, CREDITS[locale], 20, "#5C6B6B", "end")
    return art.svg(doc["title"], doc["hero"]["alt"], body)


def diagram_svg_text(vertical, data: dict, locale: str) -> str:
    """``art.diagram``'s 2×2, card for card, with the vertical's accent where batch 3 hardcoded
    its own. The layout, the card size, the weights, the type sizes and the credit line are the
    album's and are not ours to change per vertical -- but batch 3 drew the cards ``TEAL`` and
    ``BLUE``, and TEAL is the AI vertical's accent, so reusing it verbatim drew every crypto and
    tech diagram in the AI vertical's colour while the vertical's own accent reached no further
    than the hero eyebrow. Half the batch's published images are this drawing."""
    accent, other = vertical.accent, second_colour(vertical.accent)
    positions = ((110, 180), (850, 180), (110, 500), (850, 500))
    body = label(800, 102, data["title"], 46, max_width=1440)
    for i, ((x, y), (heading, detail)) in enumerate(zip(positions, data["nodes"])):
        colour = accent if i % 2 == 0 else other
        body += rect(x, y, 640, 245, "#FFFFFF", colour)
        body += circle(x + 63, y + 66, 23, colour, "none")
        body += label(x + 360, y + 91, heading, 44, max_width=510) + label(x + 320, y + 168, detail, 32, "#5C6B6B", max_width=580)
    body += label(1540, 865, CREDITS[locale], 20, "#5C6B6B", "end")
    return art.svg(data["title"], data["caption"], body)


def write_svg(path: Path, text: str) -> None:
    """Write one drawing, after the site's own SVG rules have passed on it: no script, no
    foreignObject, no external URL, nothing below 15 px. Batch 3 found those at import time."""
    problems = errors(check_svg(text))
    if problems:
        raise SystemExit(f"{path.name}: " + "; ".join(str(p) for p in problems))
    path.write_text(text, encoding="utf-8")


def build(vertical) -> list[dict]:
    workspace = ROOT / vertical.workspace
    records = sorted((workspace / "research").glob("*.json"))
    if not records:
        return []
    renders = workspace / "renders"
    renders.mkdir(exist_ok=True)
    ignore = workspace / ".gitignore"
    if not ignore.exists():
        # Two PNGs per locale per article -- roughly 130 of them for the tech vertical alone,
        # rewritten on every run, with the published copies under apps/web/public/guides. Every
        # earlier art workspace carries these two lines and the root .gitignore has no rule for
        # either; ``docs/ai-news-2026-09-mid/.gitignore`` is the file this copies. The contact
        # sheets beside them are what a person reads before the batch ships, so they are not
        # listed here.
        ignore.write_text("renders/\n__pycache__/\n", encoding="utf-8")
    research = sorted((json.loads(p.read_text(encoding="utf-8")) for p in records), key=lambda r: (r["event_date"], r["slug"]))
    manifest = []
    for item in research:
        slug = item["slug"]
        assert vertical_of(slug) is vertical, slug
        pack = json.loads((CONTENT / f"{slug}.json").read_text(encoding="utf-8"))
        target = PUBLIC / "guides" / slug
        target.mkdir(parents=True, exist_ok=True)
        for locale, doc in pack["locales"].items():
            s = suffix(locale)
            localized = item.get("translations", {}).get(locale, {}) if locale != "zh-TW" else {}
            hero_svg = target / f"hero{s}.svg"
            write_svg(hero_svg, hero_svg_text(vertical, item, doc, localized, locale))
            diagram_svg = target / f"diagram-1{s}.svg"
            write_svg(diagram_svg, diagram_svg_text(vertical, localized.get("diagram", item["diagram"]), locale))
            if "--svg-only" in sys.argv:
                continue
            for kind, svg_file in (("hero", hero_svg), ("diagram-1", diagram_svg)):
                png = (renders / f"{slug}-{locale}-{kind}.png").resolve()
                render_svg(svg_file, png, chromium=chrome())
                if kind == "hero":
                    with Image.open(png) as picture:
                        assert picture.size == HERO_SIZE, picture.size
                        jpeg = target / f"hero{s}.jpg"
                        # Quality first, then size. ``hard_cap`` is what keeps the hero at
                        # 1600×900 instead of being downscaled to fit, so the picture that
                        # comes back is always full size -- and may be over the guideline.
                        size = fit_bytes(picture, jpeg, HERO_MAX_BYTES, "JPEG", hard_cap=IMAGE_HARD_CAP)
                        assert size == HERO_SIZE, size
                        written = jpeg.stat().st_size
                        if written > HERO_MAX_BYTES:
                            # ``fit_bytes`` allows up to IMAGE_HARD_CAP here rather than lose
                            # 1600×900, which is what pack_ingest does with its own heroes: over
                            # the editorial guideline is a warning there
                            # (``hero_over_guideline``) and only IMAGE_HARD_CAP is an error, and
                            # check_article.py --assets now says exactly the same. So this is a
                            # line to read, not a refusal -- the writer refusing what the
                            # checker accepts is how the two come to disagree. These heroes are
                            # flat drawings that land around 60 KB, so one that does not is
                            # worth simplifying before the batch ships.
                            print(f"WARN {jpeg.name}: {written} bytes at the quality floor, over the "
                                  f"{HERO_MAX_BYTES} a hero is held to; simplify the drawing "
                                  f"(fewer strokes, larger flat areas) and render it again", flush=True)
            print("rendered", slug, locale, flush=True)
        manifest.append({"slug": slug, "title": item["title"], "event_date": item["event_date"], "url": f"https://mokaair.com/zh-TW/life/{slug}",
                         "locales": {loc: {"title": d["title"], "url": f"https://mokaair.com/{loc}/life/{slug}"} for loc, d in pack["locales"].items()}})
    (workspace / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def sheets(vertical, manifest: list[dict]) -> None:
    """Four articles to a sheet, one sheet per vertical, kind and locale: an agent cannot see
    what it drew, so someone reads these before the batch ships."""
    workspace = ROOT / vertical.workspace
    for kind in ("hero", "diagram-1"):
        for locale in LOCALES:
            items = [m for m in manifest if locale in m["locales"]]
            for start in range(0, len(items), 4):
                sheet = Image.new("RGB", (1600, 960), CREAM)
                draw = ImageDraw.Draw(sheet)
                for j, entry in enumerate(items[start:start + 4]):
                    with Image.open(workspace / "renders" / f"{entry['slug']}-{locale}-{kind}.png") as picture:
                        sheet.paste(picture.resize((800, 450)), ((j % 2) * 800, (j // 2) * 480))
                    draw.text(((j % 2) * 800 + 15, (j // 2) * 480 + 456), entry["slug"] + " " + locale, fill=INK)
                sheet.save(workspace / f"{kind}-sheet-{start // 4 + 1}-{locale}.jpg", quality=90)


def main() -> None:
    named = [a for a in sys.argv[1:] if not a.startswith("--")]
    unknown = [name for name in named if name not in BY_NAME]
    if unknown:
        raise SystemExit(f"unknown vertical {unknown}; one of " + ", ".join(BY_NAME))
    chosen = [BY_NAME[name] for name in named] if named else list(VERTICALS)
    for vertical in chosen:
        manifest = build(vertical)
        if not manifest:
            print("no research records yet:", vertical.workspace, flush=True)
            continue
        if "--svg-only" not in sys.argv:
            sheets(vertical, manifest)


if __name__ == "__main__":
    main()
