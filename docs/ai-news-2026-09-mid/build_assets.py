"""Original hero illustrations and 2×2 diagrams for this batch, in the album's established style.

Reuses the drawing primitives and diagram layout of the two earlier batches, adds one hero
composition per article, and renders with headless Chromium/Edge (CHROMIUM_BIN overrides).
``--svg-only`` writes the SVGs without rendering. Writes only this batch's seven image
directories, ``manifest.json`` and the contact sheets in this directory.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


art = _load("news_art", HERE.parent / "ai-news-2026-09/build_assets.py")
ytd = _load("news_art_ytd", HERE.parent / "ai-news-2026-ytd/build_assets.py")
rect, line, circle, label, document, check, envelope = art.rect, art.line, art.circle, art.label, art.document, art.check, art.envelope
chip, monitor, lock = ytd.chip, ytd.monitor, ytd.lock
CREAM, INK, TEAL, PALE, BLUE, ORANGE = art.CREAM, art.INK, art.TEAL, art.PALE, art.BLUE, art.ORANGE
LOCALES = ["zh-TW", "en", "ja", "ko", "zh-CN"]
CREDITS = {"zh-TW": "© Mokaair 製圖 2026", "zh-CN": "© Mokaair 制图 2026", "en": "© Mokaair Illustration 2026", "ja": "© Mokaair 作図 2026", "ko": "© Mokaair 제작 2026"}


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


def drawing(slug: str) -> str:
    if "gpt-live" in slug:
        b = phone(685, 205, 230, 430) + circle(800, 400, 70, "#FFFFFF", TEAL)
        b += wave(290, 420, 8, TEAL) + wave(1105, 420, 8, BLUE)
        b += rect(255, 250, 300, 80, "#FFFFFF", TEAL, 40) + rect(1045, 520, 300, 80, "#FFFFFF", BLUE, 40)
        b += line(300, 290, 500, 290, "#92BDB7", 10) + line(1090, 560, 1290, 560, "#9DBAD3", 10)
        return b + line(580, 420, 660, 420) + line(940, 420, 1020, 420, BLUE)
    if "google-assistant" in slug:
        b = phone(230, 215, 190, 350, INK) + rect(500, 285, 50, 60, PALE, "none", 10) + rect(500, 495, 50, 60, PALE, "none", 10)
        b += rect(465, 330, 120, 180, "#FFFFFF", INK, 50) + circle(525, 420, 34, PALE, "none")
        b += f'<path d="M240 690 L290 610 Q300 595 320 595 L540 595 Q560 595 570 610 L620 690 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        b += rect(335, 615, 190, 55, PALE, BLUE, 10) + line(230, 700, 630, 700, INK, 10)
        b += line(700, 450, 860, 450, ORANGE, 16) + f'<path d="M835 410 L885 450 L835 490" fill="none" stroke="{ORANGE}" stroke-width="16" stroke-linecap="round"/>'
        b += circle(1120, 440, 190, "#FFFFFF", BLUE) + sparkle(1120, 440, 120, BLUE) + sparkle(1265, 285, 34, ORANGE)
        return b
    if "threat-report" in slug:
        b = shield(800, 420) + lock(730, 420) + envelope(230, 300, 270, 180) + warning(365, 610)
        b += key(1050, 300) + document(1100, 420, 210, 250) + line(510, 420, 610, 420) + line(990, 520, 1085, 540)
        return b
    if "agents-api" in slug:
        b = rect(520, 215, 560, 420, "#FFFFFF", INK, 30) + rect(550, 250, 500, 60, PALE, "none", 14)
        b += circle(800, 420, 58, "#FFFFFF", TEAL) + "".join(circle(620 + i * 180, 560, 38, "#FFFFFF", BLUE) for i in range(3))
        b += "".join(line(800, 478, 620 + i * 180, 522, BLUE, 8) for i in range(3))
        b += document(210, 300, 210, 280) + line(430, 440, 505, 440) + chip(1180, 250, 200, 170) + check(1290, 620) + line(1095, 420, 1170, 360)
        return b
    if "deepseek" in slug:
        b = rect(210, 270, 300, 330, "#FFFFFF", "#9AA7A7") + line(260, 360, 460, 360, "#C4CCCC", 12) + line(260, 430, 420, 430, "#C4CCCC", 12) + line(260, 500, 440, 500, "#C4CCCC", 12)
        b += rect(1090, 230, 300, 400, "#FFFFFF", BLUE) + line(1140, 330, 1340, 330, BLUE, 12) + line(1140, 400, 1300, 400, BLUE, 12) + line(1140, 470, 1320, 470, BLUE, 12) + sparkle(1330, 580, 36, ORANGE)
        b += f'<path d="M530 435 C700 435 700 330 880 330 L1060 330" fill="none" stroke="{TEAL}" stroke-width="14" stroke-linecap="round"/>'
        b += f'<path d="M530 435 C700 435 700 560 880 560 L1060 560" fill="none" stroke="{ORANGE}" stroke-width="14" stroke-linecap="round" stroke-dasharray="30 22"/>'
        return b + circle(530, 435, 26, TEAL, "none") + circle(800, 445, 64, "#FFFFFF", TEAL) + line(770, 445, 830, 445, TEAL, 12)
    if "pace-the-frontier" in slug:
        b = rect(250, 170, 1100, 510, "#FFFFFF", TEAL)
        b += f'<path d="M310 620 C520 610 640 520 780 440 S1080 330 1290 340" fill="none" stroke="{BLUE}" stroke-width="14"/>'
        for x, y in [(560, 560), (860, 415), (1130, 350)]:
            b += line(x, y, x, y - 120, INK, 8) + f'<path d="M{x} {y-120} l80 26 l-80 26 Z" fill="{ORANGE}"/>' + circle(x, y, 18, INK, "none")
        return b + check(1240, 560) + line(310, 640, 1290, 640, "#B1CCC6", 6)
    if "siri" in slug:
        b = phone(640, 180, 320, 520, INK) + circle(800, 420, 110, "#FFFFFF", BLUE) + circle(800, 420, 64, "none", ORANGE) + circle(800, 420, 30, TEAL, "none")
        tiles = [(260, 250), (420, 250), (260, 410), (420, 410), (1060, 300), (1220, 300), (1060, 460), (1220, 460)]
        b += "".join(rect(x, y, 120, 120, PALE if i % 3 else "#E6F0F7", TEAL if i % 2 else BLUE, 28) for i, (x, y) in enumerate(tiles))
        return b + line(550, 420, 625, 420) + line(975, 420, 1045, 420, BLUE) + calendar_small(270, 580) + envelope(1090, 610, 220, 120)
    raise SystemExit(f"no drawing for {slug}")


def calendar_small(x, y):
    return rect(x, y, 250, 120, "#FFFFFF", TEAL, 18) + rect(x + 4, y + 4, 242, 36, PALE, "none", 14) + "".join(circle(x + 50 + c * 50, y + 80, 9, TEAL, "none") for c in range(4))


def main() -> None:
    (HERE / "renders").mkdir(exist_ok=True)
    research = sorted((json.loads(p.read_text(encoding="utf-8")) for p in (HERE / "research").glob("*.json")), key=lambda r: (r["event_date"], r["slug"]))
    manifest = []
    for item in research:
        slug = item["slug"]
        pack = json.loads((ROOT / "apps/api/app/guides/content" / f"{slug}.json").read_text(encoding="utf-8"))
        target = ROOT / "apps/web/public/guides" / slug
        target.mkdir(parents=True, exist_ok=True)
        for locale, doc in pack["locales"].items():
            suffix = "" if locale == "zh-TW" else "-" + locale.lower()
            localized = item.get("translations", {}).get(locale, {}) if locale != "zh-TW" else {}
            body = label(80, 100, "MOKAAIR  /  AI NEWS", 34, TEAL, "start") + label(1510, 100, item["event_date"], 28, BLUE, "end")
            body += drawing(slug) + label(800, 805, localized.get("hero_label", item["hero_label"]), 48, max_width=1400)
            body += label(1535, 868, CREDITS[locale], 20, "#5C6B6B", "end")
            hero_svg = target / f"hero{suffix}.svg"
            hero_svg.write_text(art.svg(doc["title"], doc["hero"]["alt"], body), encoding="utf-8")
            diagram_svg = target / f"diagram-1{suffix}.svg"
            diagram_svg.write_text(art.diagram(localized.get("diagram", item["diagram"]), locale), encoding="utf-8")
            if "--svg-only" in sys.argv:
                continue
            for kind, svg_file in (("hero", hero_svg), ("diagram-1", diagram_svg)):
                png = (HERE / "renders" / f"{slug}-{locale}-{kind}.png").resolve()
                art.render(svg_file, png)
                if kind == "hero":
                    with Image.open(png) as picture:
                        assert picture.size == (1600, 900), picture.size
                        picture.convert("RGB").save(target / f"hero{suffix}.jpg", quality=88, optimize=True, progressive=True)
            print("rendered", slug, locale, flush=True)
        manifest.append({"slug": slug, "title": item["title"], "event_date": item["event_date"], "url": f"https://mokaair.com/zh-TW/life/{slug}",
                         "locales": {loc: {"title": d["title"], "url": f"https://mokaair.com/{loc}/life/{slug}"} for loc, d in pack["locales"].items()}})
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if "--svg-only" in sys.argv:
        return
    for kind in ("hero", "diagram-1"):
        for locale in LOCALES:
            items = [m for m in manifest if locale in m["locales"]]
            for start in range(0, len(items), 4):
                sheet = Image.new("RGB", (1600, 960), CREAM)
                draw = ImageDraw.Draw(sheet)
                for j, entry in enumerate(items[start:start + 4]):
                    with Image.open(HERE / "renders" / f"{entry['slug']}-{locale}-{kind}.png") as picture:
                        sheet.paste(picture.resize((800, 450)), ((j % 2) * 800, (j // 2) * 480))
                    draw.text(((j % 2) * 800 + 15, (j // 2) * 480 + 456), entry["slug"] + " " + locale, fill=INK)
                sheet.save(HERE / f"{kind}-sheet-{start // 4 + 1}-{locale}.jpg", quality=90)


if __name__ == "__main__":
    main()
