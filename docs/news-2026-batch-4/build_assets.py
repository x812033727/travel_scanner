"""Original hero illustrations and 2×2 diagrams for this batch, in the album's established style.

``build_assets.py [crypto|tech|ai]... [--svg-only]`` -- with no vertical named, every vertical
whose workspace holds research records. Reuses the drawing primitives, the palette and the
diagram layout of the three earlier batches and adds one hero composition per article.
``--svg-only`` writes the SVGs without rendering, and needs no browser to do it. Writes only
this batch's image directories under ``apps/web/public/guides`` and, inside each vertical's
workspace, ``manifest.json``, ``renders/`` with the ``.gitignore`` that keeps it and any
``__pycache__`` out of the repository, and the contact sheets.

``--slug=<slug>`` (repeatable) draws only those articles, for the weeks in which a vertical's
workspace holds research records whose articles have no drawing yet. A partial run leaves the
manifest and the contact sheets alone: both describe the whole vertical.

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
import math
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


def coin(x, y, r=52, color=ORANGE):
    """A token as an object of regulation: two plain rings, never a currency sign or a
    project's mark."""
    return circle(x, y, r, "#FFFFFF", color) + circle(x, y, r * 0.6, PALE, color)


def dashed(x1, y1, x2, y2, color=TEAL, width=12):
    """``line``, broken: something announced and not yet in force, or a date nobody has set."""
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-dasharray="26 22"/>'


def pending(x, y, r, color=ORANGE):
    """A milestone that has no date yet: the same node as the others, outlined in dashes."""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" stroke="{color}" stroke-width="8" stroke-dasharray="18 14"/>'


def sheet(x, y, w=220, h=270, color=BLUE, rows=4, broken=False):
    """``document`` in the vertical's own colour. ``broken`` draws the outline in dashes: a
    proposal, a recommendation, a rule that is not one yet."""
    dash = ' stroke-dasharray="22 16"' if broken else ""
    body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="#FFFFFF" stroke="{color}" stroke-width="6"{dash}/>'
    return body + "".join(line(x + 35, y + 55 + i * 44, x + w - 35 - (i % 2) * 30, y + 55 + i * 44, "#C4CCCC", 12) for i in range(rows))


def slot(x, y, size=120, color=BLUE, broken=False):
    """One provider. Dashed while it runs on a national regime or a transitional period."""
    dash = ' stroke-dasharray="20 14"' if broken else ""
    return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="22" fill="#FFFFFF" stroke="{color}" stroke-width="6"{dash}/>'


def arrow(x1, x2, y, color=BLUE, width=12, broken=False):
    shaft = dashed(x1, y, x2 - 14, y, color, width) if broken else line(x1, y, x2 - 14, y, color, width)
    return shaft + f'<path d="M{x2-36} {y-30} L{x2} {y} L{x2-36} {y+30}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


def tick(x, y, r=56, color=BLUE):
    """``check`` in the vertical's own colour: in force, authorised, done."""
    return circle(x, y, r, "#FFFFFF", color) + f'<path d="M{x-r*0.45} {y} l{r*0.33} {r*0.36} l{r*0.65} {-r*0.77}" stroke="{color}" fill="none" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'


def bank(x, y, w=320, color=BLUE):
    """A pediment on four columns: a chartered institution. Nobody's building in particular."""
    h = w * 0.78
    body = f'<path d="M{x} {y+h*0.3} L{x+w/2} {y} L{x+w} {y+h*0.3} Z" fill="{PALE}" stroke="{color}" stroke-width="8" stroke-linejoin="round"/>'
    body += line(x + 10, y + h * 0.4, x + w - 10, y + h * 0.4, color, 12)
    for i in range(4):
        cx = x + w * (0.17 + i * 0.22)
        body += line(cx, y + h * 0.5, cx, y + h * 0.86, color, 16)
    return body + line(x - 10, y + h, x + w + 10, y + h, color, 14)


def ward(x, y, s=1.0, color=BLUE):
    """``shield`` in the vertical's own colour."""
    return f'<path d="M{x} {y-200*s} L{x+180*s} {y-135*s} V{y} Q{x+180*s} {y+150*s} {x} {y+230*s} Q{x-180*s} {y+150*s} {x-180*s} {y} V{y-135*s} Z" fill="{PALE}" stroke="{color}" stroke-width="10" stroke-linejoin="round"/>'


def padlock(x, y, s=1.0, color=ORANGE):
    body = f'<path d="M{x-46*s} {y-10*s} V{y-60*s} a{46*s} {46*s} 0 0 1 {92*s} 0 V{y-10*s}" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round"/>'
    return body + rect(x - 75 * s, y - 10 * s, 150 * s, 120 * s, "#FFFFFF", color, 20) + circle(x, y + 40 * s, 14 * s, color, "none") + line(x, y + 50 * s, x, y + 78 * s, color, 10)


def letter(x, y, w=220, h=150, color=BLUE):
    """``envelope`` in the vertical's own colour: a public comment on its way in."""
    return rect(x, y, w, h, "#FFFFFF", color) + f'<path d="M{x+10} {y+12} L{x+w/2} {y+h*.57} L{x+w-10} {y+12}" fill="none" stroke="{color}" stroke-width="8" stroke-linejoin="round"/>'


def month(x, y, w=250, h=230, color=BLUE):
    """``calendar`` in the vertical's own colour: a deadline, a comment period."""
    body = rect(x, y, w, h, "#FFFFFF", color) + rect(x + 4, y + 4, w - 8, 54, PALE, "none", 18)
    body += line(x + 65, y - 18, x + 65, y + 22, color) + line(x + w - 65, y - 18, x + w - 65, y + 22, color)
    return body + "".join(circle(x + 55 + c * 70, y + 107 + r * 61, 10, color, "none") for c in range(3) for r in range(2))


def _taiwan_vasp_act(accent: str) -> str:
    # The regulator on the left, the seven kinds of provider it licenses on the right with the
    # stablecoin in the eighth slot, and underneath the article's spine: read, promulgated,
    # and a commencement date that is still open.
    other = second_colour(accent)
    b = scales(470, 400, other) + line(745, 400, 845, 400, accent)
    slots = [(880 + c * 130, 230 + r * 130) for r in range(2) for c in range(4)]
    b += "".join(rect(x, y, 100, 100, "#FFFFFF", accent if i % 2 == 0 else other, 20) for i, (x, y) in enumerate(slots[:7]))
    b += coin(slots[7][0] + 50, slots[7][1] + 50, 50, accent)
    b += line(400, 640, 800, 640, other, 10) + dashed(800, 640, 1200, 640, accent, 10)
    return b + circle(400, 640, 30, other, "none") + circle(800, 640, 30, accent, "none") + pending(1200, 640, 30, accent)


def _mica_transition(accent: str) -> str:
    # One date splits the picture: providers on national regimes to its left, in dashes, and
    # authorised ones to its right, each with its seal. The track underneath does the same.
    other = second_colour(accent)
    b = "".join(slot(250 + i * 160, 290, 120, other, broken=True) for i in range(3))
    for i in range(3):
        x = 910 + i * 160
        b += slot(x, 290, 120, accent) + circle(x + 92, 382, 22, PALE, accent)
    b += dashed(250, 560, 770, 560, other, 12) + arrow(830, 1350, 560, accent)
    return b + line(800, 235, 800, 610, INK, 10) + circle(800, 560, 28, INK, "none")


def _sec_cftc_interpretation(accent: str) -> str:
    # Two commissions, one release, and it is in force: the only solid tick of the batch.
    other = second_colour(accent)
    b = line(410, 310, 670, 400, other, 10) + line(410, 550, 670, 460, accent, 10)
    b += circle(330, 310, 84, "#FFFFFF", other) + circle(330, 310, 30, other, "none")
    b += circle(330, 550, 84, "#FFFFFF", accent) + circle(330, 550, 30, accent, "none")
    b += sheet(680, 255, 270, 350, INK, rows=6)
    return b + arrow(985, 1110, 430, other) + tick(1215, 430, 84, other)


def _sec_regulation_crypto_assets(accent: str) -> str:
    # A proposal, so the rule itself is drawn in dashes; comments arrive from the left and the
    # comment period runs on the right.
    other = second_colour(accent)
    b = letter(215, 265, 220, 150, other) + letter(215, 470, 220, 150, other)
    b += arrow(465, 610, 340, other) + arrow(465, 610, 545, other)
    b += sheet(645, 225, 310, 410, accent, rows=8, broken=True)
    return b + arrow(990, 1090, 430, accent, broken=True) + month(1120, 320, 250, 230, other)


def _eba_psd2_mica(accent: str) -> str:
    # Two regimes and the services that fall under both: the overlap is the opinion's subject.
    other = second_colour(accent)
    b = rect(710, 245, 180, 390, PALE, "none", 0)
    b += f'<rect x="330" y="245" width="560" height="390" rx="36" fill="none" stroke="{other}" stroke-width="8"/>'
    b += f'<rect x="710" y="245" width="560" height="390" rx="36" fill="none" stroke="{accent}" stroke-width="8"/>'
    b += rect(405, 370, 230, 140, "#FFFFFF", other, 18) + line(419, 415, 621, 415, other, 22) + line(440, 470, 530, 470, "#C4CCCC", 12)
    b += chain(965, 385, 2, accent, 110, 50)
    return b + coin(800, 440, 56, accent)


def _genius_act_occ(accent: str) -> str:
    # The chartering regulator's draft: a bank, a rule in dashes, and a token that stands on
    # its reserves, bar for bar.
    other = second_colour(accent)
    b = bank(215, 290, 350, other) + arrow(610, 700, 430, other)
    b += sheet(725, 245, 260, 360, accent, rows=6, broken=True)
    b += coin(1240, 300, 62, accent) + line(1200, 395, 1280, 395, INK, 10) + line(1200, 425, 1280, 425, INK, 10)
    return b + "".join(rect(1130, 460 + i * 62, 220, 46, PALE, other, 14) for i in range(3))


def _stablecoin_aml(accent: str) -> str:
    # A checkpoint on the track: most transfers pass, one is held. The rule is a draft, so the
    # checkpoint's own base line is dashed.
    other = second_colour(accent)
    b = line(215, 400, 600, 400, other, 12) + arrow(1000, 1390, 400, other)
    b += coin(330, 400, 50, accent) + coin(500, 400, 50, accent) + coin(1130, 400, 50, accent)
    b += ward(800, 400, 0.9, other) + padlock(800, 370, 0.8, accent)
    b += dashed(800, 607, 800, 660, accent, 10) + dashed(800, 660, 1010, 660, accent, 10)
    return b + coin(1075, 660, 44, accent) + warning(1200, 655, 48)


def _fdic_genius_act(accent: str) -> str:
    # Deposits sit inside the insurer's shield; the token and the draft rule about it sit
    # outside, joined to the bank by a dashed line.
    other = second_colour(accent)
    b = bank(200, 300, 330, other) + line(560, 430, 640, 430, other, 12)
    b += ward(800, 420, 0.85, other) + "".join(rect(715, 330 + i * 62, 170, 44, "#FFFFFF", other, 12) for i in range(3))
    b += dashed(965, 430, 1075, 430, accent, 12)
    return b + sheet(1090, 295, 220, 270, accent, rows=4, broken=True) + coin(1395, 430, 52, accent)


def _ncua_genius_act(accent: str) -> str:
    # A credit union is its members: a ring of them round one institution, and the draft that
    # would let its subsidiary issue a token.
    other = second_colour(accent)
    b = circle(450, 430, 190, "none", "#C4CCCC")
    for i in range(8):
        angle = math.radians(i * 45 - 90)
        b += circle(round(450 + 190 * math.cos(angle)), round(430 + 190 * math.sin(angle)), 34, "#FFFFFF", other)
    b += rect(385, 365, 130, 130, PALE, other, 26) + arrow(680, 790, 430, other)
    b += sheet(820, 250, 250, 350, accent, rows=6, broken=True)
    return b + dashed(1100, 430, 1190, 430, accent, 12) + coin(1275, 430, 66, accent)


def _jfsa_working_group(accent: str) -> str:
    # A council's table, the report it produced, and the legislation that report asks for --
    # which does not exist yet, so it is drawn in dashes.
    other = second_colour(accent)
    b = circle(400, 430, 105, PALE, other)
    for i in range(6):
        angle = math.radians(i * 60 - 90)
        b += circle(round(400 + 190 * math.cos(angle)), round(430 + 190 * math.sin(angle)), 36, "#FFFFFF", other)
    b += arrow(640, 740, 430, other) + sheet(770, 265, 240, 330, other, rows=6)
    return b + arrow(1040, 1140, 430, accent, broken=True) + sheet(1170, 265, 240, 330, accent, rows=6, broken=True)


def _jfsa_cybersecurity(accent: str) -> str:
    # A chain with one link flagged, the defence in the middle, and the keys it protects.
    other = second_colour(accent)
    b = chain(185, 365, 3, other, 110, 50) + warning(560, 300, 46)
    b += line(680, 420, 615, 420, other, 12)
    b += ward(800, 420, 0.9, other) + padlock(800, 395, 0.85, accent)
    return b + line(985, 420, 1050, 420, other, 12) + key(1120, 360, accent) + sheet(1090, 440, 250, 180, other, rows=3)


def _crypto_index(accent: str) -> str:
    # Four jurisdictions feeding one reading list. Each panel holds one plain object of this
    # batch's vocabulary -- a law, a bank, a licence, a lock -- and none of them is a flag.
    other = second_colour(accent)
    panels = [(230, 215), (470, 215), (230, 455), (470, 455)]
    b = "".join(rect(x, y, 200, 200, "#FFFFFF", accent if i in (0, 3) else other, 28) for i, (x, y) in enumerate(panels))
    b += "".join(line(270, 270 + i * 45, 390 - (i % 2) * 30, 270 + i * 45, "#C4CCCC", 12) for i in range(3)) + pending(385, 375, 18, accent)
    b += bank(505, 262, 130, other)
    b += circle(330, 555, 52, PALE, other) + line(330, 607, 312, 640, other, 10) + line(330, 607, 348, 640, other, 10)
    b += padlock(570, 545, 0.6, accent)
    b += "".join(line(690, y, 860, 430, "#C4CCCC", 8) for y in (315, 555))
    b += sheet(890, 215, 430, 440, INK, rows=0)
    for i in range(4):
        y = 290 + i * 95
        b += circle(950, y, 16, accent if i % 2 == 0 else other, "none") + line(995, y, 1255 - (i % 2) * 50, y, "#C4CCCC", 14)
    return b


# --- the tech vertical (batch 4.2) ----------------------------------------------------------
# Devices are outlines of a category -- a slab, a square with a strap, a bud on a stem -- and
# never a particular product's silhouette, camera layout or interface.


def curve(x1, y1, cx, cy, x2, y2, color=TEAL, width=10, broken=False):
    """One quadratic stroke: a cable on the sea floor. ``broken`` is one that is not lit yet."""
    dash = ' stroke-dasharray="26 22"' if broken else ""
    return f'<path d="M{x1} {y1} Q{cx} {cy} {x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{dash}/>'


def outline(x, y, w, h, color=BLUE, rx=36):
    """A dashed frame round things that are counted as one."""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="{color}" stroke-width="6" stroke-dasharray="22 16"/>'


def pylon(x, y, color=TEAL, h=360):
    """A transmission tower: the grid, as opposed to ``tower``'s radio mast."""
    body = line(x - 70, y + h, x, y, color, 12) + line(x + 70, y + h, x, y, color, 12)
    for share, half in ((0.22, 95), (0.45, 70)):
        level = y + h * share
        body += line(x - half, level, x + half, level, color, 10)
        body += line(x - half, level, x - half, level + 26, color, 8) + line(x + half, level, x + half, level + 26, color, 8)
    return body + line(x - 48, y + h * 0.72, x + 48, y + h * 0.72, color, 10)


def _iphone_duo(accent: str) -> str:
    # The same device twice: closed, a narrow slab with its spine on the left; open, one wide
    # panel with the fold down the middle, a hinge at each end of it and a cell in each half.
    other = second_colour(accent)
    b = rect(275, 270, 210, 340, "#FFFFFF", other, 34) + rect(305, 298, 158, 284, PALE, "none", 18) + line(290, 310, 290, 570, other, 10)
    b += arrow(560, 700, 440, other)
    b += rect(760, 250, 580, 380, "#FFFFFF", accent, 34) + rect(784, 274, 532, 332, PALE, "none", 18)
    b += dashed(1050, 268, 1050, 612, accent, 8) + circle(1050, 250, 15, accent, "none") + circle(1050, 630, 15, accent, "none")
    return b + rect(835, 515, 150, 56, "#FFFFFF", other, 14) + rect(1115, 515, 150, 56, "#FFFFFF", other, 14)


def _apple_september_hardware(accent: str) -> str:
    # Three categories on one shelf -- a phone, a watch with a pulse across its face, a pair of
    # buds -- and nothing that belongs to a particular model.
    other = second_colour(accent)
    b = phone(250, 235, 230, 420, INK)
    b += rect(705, 210, 130, 95, PALE, other, 22) + rect(705, 575, 130, 95, PALE, other, 22) + rect(650, 295, 240, 290, "#FFFFFF", accent, 60)
    b += f'<path d="M690 440 L735 440 L762 385 L792 495 L818 440 L850 440" fill="none" stroke="{accent}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
    for x in (1105, 1275):
        b += rect(x - 19, 395, 38, 170, "#FFFFFF", other, 19) + circle(x, 370, 52, "#FFFFFF", other) + circle(x, 370, 18, other, "none")
    return b


def _eu_cra_reporting(accent: str) -> str:
    # A clock starts running, a report goes to one platform, and the platform passes it on to
    # the national teams: the article's flow, left to right.
    other = second_colour(accent)
    b = circle(330, 430, 125, "#FFFFFF", other) + line(330, 430, 330, 345, other, 12) + line(330, 430, 400, 430, other, 12) + circle(330, 430, 13, other, "none")
    b += arrow(490, 600, 430, other) + sheet(635, 295, 220, 270, accent, rows=4) + warning(835, 305, 42)
    b += arrow(890, 1000, 430, accent)
    b += "".join(line(1100, 430, x, y, "#C4CCCC", 8) for x, y in ((1300, 285), (1350, 430), (1300, 575)))
    b += circle(1100, 430, 74, PALE, accent) + circle(1100, 430, 24, accent, "none")
    return b + "".join(circle(x, y, 42, "#FFFFFF", other) for x, y in ((1300, 285), (1350, 430), (1300, 575)))


def _taiwan_sovereign_ai_corpus(accent: str) -> str:
    # Books on the left, the licence they pass through, and the corpus they end up in.
    other = second_colour(accent)
    b = rect(245, 500, 300, 64, "#FFFFFF", other, 12) + rect(270, 428, 270, 64, PALE, other, 12) + rect(235, 356, 300, 64, "#FFFFFF", other, 12)
    b += line(285, 372, 285, 404, other, 8) + line(320, 444, 320, 476, other, 8) + line(295, 516, 295, 548, other, 8)
    b += arrow(585, 665, 460, other) + certificate(695, 290, 240, 320, accent) + arrow(975, 1055, 460, accent)
    b += rect(1085, 275, 320, 340, "#FFFFFF", accent, 36)
    for r in range(3):
        for c in range(3):
            b += rect(1115 + c * 95, 305 + r * 95, 70, 70, PALE if (r + c) % 2 == 0 else "#FFFFFF", other if (r + c) % 2 == 0 else accent, 14)
    return b


def _taiwan_6g_spectrum(accent: str) -> str:
    # A mast on the ground, a satellite above it, a dashed link between the two layers -- and
    # on the right a plan drawn in dashes with an open date: a seminar, not a decision.
    other = second_colour(accent)
    b = line(215, 645, 1000, 645, "#C4CCCC", 10) + tower(390, 405, accent, 240)
    b += rect(640, 268, 100, 50, PALE, other, 8) + rect(870, 268, 100, 50, PALE, other, 8) + line(740, 293, 760, 293, other, 8) + line(850, 293, 870, 293, other, 8)
    b += rect(760, 250, 90, 86, "#FFFFFF", other, 16)
    b += dashed(500, 420, 730, 340, other, 8) + dashed(805, 360, 805, 610, other, 8)
    return b + sheet(1110, 300, 240, 300, accent, rows=5, broken=True) + pending(1350, 300, 36, accent)


def _taiwan_matsu_cable(accent: str) -> str:
    # The main island's shore, three cables across the strait -- one with a fault on it, one
    # not yet lit -- and the four townships joined to each other by microwave.
    other = second_colour(accent)
    b = rect(200, 290, 170, 320, PALE, other, 44)
    b += curve(370, 360, 700, 250, 1046, 415, other) + curve(370, 430, 700, 520, 1046, 430, other) + curve(370, 500, 700, 700, 1046, 445, accent, broken=True)
    b += warning(704, 470, 44)
    nodes = ((1090, 430), (1230, 275), (1370, 430), (1230, 585))
    b += "".join(dashed(x1, y1, x2, y2, accent, 8) for (x1, y1), (x2, y2) in zip(nodes, nodes[1:] + nodes[:1]))
    return b + "".join(circle(x, y, 44, PALE, other) for x, y in nodes)


def _apple_eu_business_terms(accent: str) -> str:
    # Several sets of terms become one, and what that one charges for core technology is the
    # thin slice of the pie: a twentieth, drawn to scale.
    other = second_colour(accent)
    b = sheet(215, 245, 180, 230, other, rows=3) + sheet(275, 325, 180, 230, other, rows=3) + sheet(335, 405, 180, 230, other, rows=3)
    b += arrow(560, 670, 440, other) + sheet(705, 275, 250, 330, accent, rows=6) + arrow(990, 1090, 440, accent)
    return b + circle(1255, 440, 130, "#FFFFFF", accent) + f'<path d="M1255 440 L1255 310 A130 130 0 0 1 1295.2 316.4 Z" fill="{accent}" stroke="{accent}" stroke-width="6" stroke-linejoin="round"/>'


def _windows_project_zenith(accent: str) -> str:
    # A developer machine with its tools already listed on screen, and beside it the memory it
    # must have and the bandwidth line it has to clear.
    other = second_colour(accent)
    b = monitor(215, 250, 560, 330)
    for c in range(3):
        for r in range(4):
            b += line(280 + c * 165, 325 + r * 52, 385 + c * 165 - (r % 2) * 30, 325 + r * 52, accent if c == 1 else other, 12)
    b += rect(890, 290, 470, 120, "#FFFFFF", accent, 24) + "".join(rect(915 + i * 108, 318, 88, 64, PALE, accent, 10) for i in range(4))
    return b + arrow(890, 1360, 545, other) + line(1190, 470, 1190, 620, INK, 10) + circle(1190, 545, 24, INK, "none")


def _pixel_drop(accent: str) -> str:
    # One update, four gates -- model, region, language, pairing -- and at the far end the one
    # watch some of it is limited to.
    other = second_colour(accent)
    b = phone(235, 235, 230, 420, INK)
    b += "".join(rect(272 + c * 85, 325 + r * 85, 66, 66, "#FFFFFF", accent if (r + c) % 2 == 0 else other, 14) for r in range(2) for c in range(2))
    for x in (610, 765, 920, 1075):
        b += line(x, 265, x, 385, other, 14) + line(x, 495, x, 615, other, 14)
    return b + arrow(520, 1160, 440, accent) + pending(1290, 440, 92, accent) + circle(1290, 440, 54, PALE, accent)


def _apple_m6_m5_ultra(accent: str) -> str:
    # One chip on its own and one made of two joined edge to edge, over a staircase of memory.
    other = second_colour(accent)
    b = chip(285, 245, 230, 190) + chip(760, 245, 220, 190) + chip(1075, 245, 220, 190) + rect(980, 300, 95, 80, PALE, accent, 10)
    for i, h in enumerate((36, 64, 98, 136)):
        b += rect(300 + i * 270, 670 - h, 200, h, PALE if i % 2 == 0 else "#FFFFFF", other if i % 2 == 0 else accent, 12)
    return b


def _nvidia_cuda_q(accent: str) -> str:
    # Many error-prone physical qubits counted as one logical qubit, and the ruler underneath:
    # the release estimates how much hardware that takes -- it does not run anything.
    other = second_colour(accent)
    b = outline(200, 235, 390, 290, accent)
    for r in range(3):
        for c in range(4):
            x, y = 250 + c * 95, 290 + r * 90
            b += pending(x, y, 28, other) if (r * 4 + c) % 3 == 1 else circle(x, y, 28, "#FFFFFF", other)
    b += arrow(640, 770, 380, accent) + circle(935, 380, 125, "#FFFFFF", accent) + circle(935, 380, 60, PALE, accent)
    b += sheet(1150, 245, 230, 280, other, rows=5)
    b += rect(215, 590, 1170, 64, "#FFFFFF", INK, 14)
    return b + "".join(line(215 + i * 65, 593, 215 + i * 65, 593 + (36 if i % 3 == 0 else 20), INK, 6) for i in range(1, 18))


def _nvidia_mediatek(accent: str) -> str:
    # Two chip companies and the money passing between them; on the right, the two documents
    # that describe the same deal in different words.
    other = second_colour(accent)
    b = chip(240, 335, 230, 190) + arrow(520, 700, 430, accent) + coin(610, 340, 48, accent) + chip(770, 335, 230, 190)
    return b + sheet(1095, 235, 200, 250, accent, rows=4) + sheet(1195, 405, 200, 250, other, rows=4)


def _nvidia_vera_rubin(accent: str) -> str:
    # The four levels the power is managed at: chip, rack, hall, grid. The last link runs both
    # ways, so it is dashed and has a node at each end.
    other = second_colour(accent)
    b = chip(230, 340, 190, 180) + arrow(465, 535, 430, other)
    b += rect(565, 265, 200, 340, "#FFFFFF", INK, 20) + "".join(rect(590, 292 + i * 76, 150, 50, PALE, other, 10) for i in range(4))
    b += arrow(795, 865, 430, other) + rect(895, 320, 250, 285, "#FFFFFF", accent, 16)
    b += "".join(rect(925 + c * 70, 352 + r * 80, 48, 48, PALE, accent, 8) for r in range(3) for c in range(3))
    b += dashed(1165, 488, 1262, 488, accent, 10) + circle(1165, 488, 12, accent, "none") + circle(1262, 488, 12, accent, "none")
    return b + pylon(1335, 265, other, 380)


def _tech_index(accent: str) -> str:
    # Four kinds of story feeding one reading list: a chip, a screen, a mast, a lock.
    other = second_colour(accent)
    panels = [(230, 215), (470, 215), (230, 455), (470, 455)]
    b = "".join(rect(x, y, 200, 200, "#FFFFFF", accent if i in (0, 3) else other, 28) for i, (x, y) in enumerate(panels))
    b += rect(285, 270, 90, 90, PALE, other, 16) + rect(309, 294, 42, 42, "#FFFFFF", accent, 8)
    b += "".join(line(x, 290 + i * 25, x + 17, 290 + i * 25, other, 7) for i in range(3) for x in (265, 378))
    b += rect(505, 255, 130, 90, "#FFFFFF", INK, 14) + rect(517, 267, 106, 58, PALE, "none", 8) + line(570, 345, 570, 372, INK, 10) + line(535, 376, 605, 376, INK, 10)
    b += line(295, 625, 330, 535, other, 10) + line(365, 625, 330, 535, other, 10) + line(312, 585, 348, 585, other, 8) + circle(330, 535, 11, other, "none")
    b += f'<path d="M285 510 A45 45 0 0 1 375 510" fill="none" stroke="{other}" stroke-width="8" stroke-linecap="round"/>'
    b += padlock(570, 545, 0.6, accent)
    b += "".join(line(690, y, 860, 430, "#C4CCCC", 8) for y in (315, 555))
    b += sheet(890, 215, 430, 440, INK, rows=0)
    for i in range(4):
        y = 290 + i * 95
        b += circle(950, y, 16, accent if i % 2 == 0 else other, "none") + line(995, y, 1255 - (i % 2) * 50, y, "#C4CCCC", 14)
    return b


def cylinder(x, y, w=260, h=300, color=TEAL):
    """A database: a can with its lid drawn as an ellipse and two seams down the body."""
    ry = w * 0.18
    body = f'<path d="M{x} {y+ry} V{y+h-ry} A{w/2} {ry} 0 0 0 {x+w} {y+h-ry} V{y+ry}" fill="#FFFFFF" stroke="{color}" stroke-width="8"/>'
    body += f'<ellipse cx="{x+w/2}" cy="{y+ry}" rx="{w/2}" ry="{ry}" fill="{PALE}" stroke="{color}" stroke-width="8"/>'
    return body + "".join(f'<path d="M{x} {y+ry+i*90} A{w/2} {ry} 0 0 0 {x+w} {y+ry+i*90}" fill="none" stroke="{color}" stroke-width="6"/>' for i in (1, 2))


def bubble(x, y, w=150, h=100, color=BLUE):
    """A speech bubble: a rounded box with a tail at the lower left."""
    return rect(x, y, w, h, "#FFFFFF", color, 30) + f'<path d="M{x+34} {y+h-4} L{x+22} {y+h+34} L{x+70} {y+h-4}" fill="#FFFFFF" stroke="{color}" stroke-width="6" stroke-linejoin="round"/>'


def magnifier(x, y, r=70, color=TEAL):
    """A lens and its handle: tracing a figure back to where it came from."""
    return circle(x, y, r, "#FFFFFF", color) + line(x + r * 0.72, y + r * 0.72, x + r * 1.7, y + r * 1.7, color, 18)


def _chatgpt_storage_scale(accent: str) -> str:
    # Many requests converging on one database, and underneath the article's spine: the same
    # service drawn in dashes as the old version and in a solid line as the rewrite.
    other = second_colour(accent)
    b = "".join(line(215, y, 560, 430, "#C4CCCC", 6) for y in range(250, 631, 38))
    b += cylinder(590, 265, 260, 330, accent)
    b += dashed(960, 300, 1180, 300, other, 14) + arrow(1180, 1260, 300, other, 14) + line(1260, 300, 1385, 300, accent, 14)
    b += circle(960, 300, 16, other, "none") + circle(1385, 300, 16, accent, "none")
    # Four bars, each a step taller: the growth the post describes as tenfold a year.
    return b + "".join(rect(975 + i * 105, 640 - h, 80, h, PALE if i % 2 == 0 else "#FFFFFF", other if i % 2 == 0 else accent, 12) for i, h in enumerate((40, 90, 160, 250)))


def _openai_astral(accent: str) -> str:
    # Three tools on the left, the larger product they are to join on the right, and between
    # them an arrow still drawn in dashes with an open node on it: announced, not yet closed.
    other = second_colour(accent)
    b = "".join(slot(230, 235 + i * 150, 120, other) + line(262, 295 + i * 150, 320 - i * 14, 295 + i * 150, "#C4CCCC", 12) for i in range(3))
    b += arrow(420, 800, 440, accent, broken=True) + pending(610, 440, 46, accent)
    return b + outline(860, 225, 520, 440, accent) + monitor(940, 285, 360, 240)


def _gpt_live_1_api(accent: str) -> str:
    # A handset with sound coming off it, wired to the panel that answers: the model lives
    # behind the call, not in a setting the caller can see.
    other = second_colour(accent)
    b = phone(250, 235, 230, 420, INK) + wave(535, 330, 4, other, 26)
    b += "".join(line(295, 330 + i * 60, 435 - (i % 2) * 40, 330 + i * 60, "#C4CCCC", 12) for i in range(4))
    b += line(480, 560, 700, 560, other, 12) + line(700, 560, 700, 440, other, 12) + arrow(700, 820, 440, other)
    b += rect(850, 245, 520, 400, "#FFFFFF", accent, 36) + bubble(1030, 400, 160, 110, accent)
    return b + wave(1060, 320, 5, other, 24)


def _chatgpt_financial_services(accent: str) -> str:
    # Stacked sources on the left, one figure traced back through a lens, and the four things
    # the announcement is about along the bottom: data, templates, permissions, contact.
    other = second_colour(accent)
    b = "".join(sheet(230 + i * 60, 245 + (2 - i) * 60, 200, 230 - (2 - i) * 30, other if i < 2 else accent, rows=3) for i in range(3))
    b += rect(430, 420, 40, 30, "#FFFFFF", accent, 6) + line(470, 435, 900, 435, accent, 6)
    b += magnifier(960, 400, 80, accent)
    return b + "".join(rect(700 + i * 110, 570, 80, 80, PALE if i % 2 == 0 else "#FFFFFF", other if i % 2 == 0 else accent, 16) for i in range(4))


def hexagon(x, y, r=52, color=TEAL, fill="#FFFFFF"):
    """One cell of a honeycomb: a community, a hub, many hands on one platform."""
    points = " ".join(f"{x + r * c},{y + r * s}" for c, s in ((0.866, 0.5), (0, 1), (-0.866, 0.5), (-0.866, -0.5), (0, -1), (0.866, -0.5)))
    return f'<polygon points="{points}" fill="{fill}" stroke="{color}" stroke-width="7" stroke-linejoin="round"/>'


def _nvidia_hugging_face(accent: str) -> str:
    # An open platform drawn as a honeycomb, the chip company it has agreed to join, and the
    # deal between them still a dashed line into a dashed ring: agreed, not closed, no date.
    other = second_colour(accent)
    # Pointy-top cells sit side by side at 0°, 60°, 120°... and r√3 apart, so the ring's six
    # share an edge each with the centre instead of crossing it.
    cells = [(430, 440)] + [(430 + 118 * c, 440 + 118 * s) for c, s in ((1, 0), (0.5, 0.866), (-0.5, 0.866), (-1, 0), (-0.5, -0.866), (0.5, -0.866))]
    b = "".join(hexagon(x, y, 64, accent if i == 0 else other, PALE if i == 0 else "#FFFFFF") for i, (x, y) in enumerate(cells))
    b += arrow(660, 900, 440, accent, broken=True)
    return b + pending(1150, 440, 200, accent) + chip(1030, 350, 240, 180)


def _openai_funding(accent: str) -> str:
    # Investors on the left paying into one round, and on the right the timeline the money
    # actually arrives along: two tranches done, the third still a dashed node.
    other = second_colour(accent)
    b = "".join(coin(300, y, 50, other if i % 2 == 0 else accent) + line(352, y, 560, 440, "#C4CCCC", 8) for i, y in enumerate((300, 440, 580)))
    b += rect(560, 300, 280, 280, "#FFFFFF", accent, 40) + "".join(rect(600 + c * 90, 340 + r * 90, 60, 60, PALE, other, 12) for r in range(2) for c in range(2))
    b += arrow(870, 960, 440, other) + line(960, 440, 1380, 440, other, 10)
    return b + tick(1010, 440, 46, accent) + tick(1190, 440, 46, accent) + pending(1370, 440, 46, accent)


def _openai_s1(accent: str) -> str:
    # A draft under lock on the left, and on the right the clock nobody has set: the filing is
    # confidential, the timetable undecided.
    other = second_colour(accent)
    b = sheet(300, 245, 260, 330, accent, rows=5, broken=True) + padlock(560, 470, 0.9, other)
    b += dashed(700, 430, 960, 430, accent, 12)
    b += pending(1150, 430, 150, accent) + line(1150, 430, 1150, 340, other, 12) + line(1150, 430, 1225, 470, other, 12) + circle(1150, 430, 14, other, "none")
    return b + "".join(circle(1150 + 118 * c, 430 + 118 * s, 8, other, "none") for c, s in ((0, -1), (1, 0), (0, 1), (-1, 0)))


def gear(x, y, r=60, color=BLUE):
    """A cog: the part under the surface that was swapped."""
    body = "".join(line(x + (r + 4) * c, y + (r + 4) * s, x + (r + 26) * c, y + (r + 26) * s, color, 16)
                   for c, s in ((1, 0), (0.707, 0.707), (0, 1), (-0.707, 0.707), (-1, 0), (-0.707, -0.707), (0, -1), (0.707, -0.707)))
    return body + circle(x, y, r, "#FFFFFF", color) + circle(x, y, r * 0.38, PALE, color)


def _gemini_38_live(accent: str) -> str:
    # A voice in a speech bubble, and beside it the four kinds of account the launch names:
    # two doors drawn solid, two still dashed -- announced together, open to different degrees.
    other = second_colour(accent)
    b = bubble(230, 265, 480, 300, accent) + wave(370, 415, 8, other, 30)
    b += arrow(770, 880, 440, other)
    for i, (x, y) in enumerate(((930, 250), (1150, 250), (930, 470), (1150, 470))):
        b += slot(x, y, 180, accent if i < 2 else other, broken=i >= 2)
        b += rect(x + 50, y + 50, 80, 80, PALE if i < 2 else "#FFFFFF", "none", 16)
    return b


def _gpt_55_instant(accent: str) -> str:
    # The model under the chat window swapped like a cog, and beside it a checklist with half
    # its rows ticked: what the release notes put numbers to, and what they left blank.
    other = second_colour(accent)
    b = bubble(230, 250, 440, 330, accent) + gear(450, 405, 62, other)
    b += arrow(720, 830, 440, other) + sheet(880, 245, 300, 380, accent, rows=0)
    for i in range(5):
        y = 305 + i * 68
        b += (tick(935, y, 22, accent) if i < 3 else pending(935, y, 22, other)) + line(985, y, 1140 - (i % 2) * 30, y, "#C4CCCC", 12)
    return b


def _openai_broadcom_chip(accent: str) -> str:
    # A model (a speech bubble) wired to the chip made for it, the chip still inside a dashed
    # frame -- engineering samples in a lab -- and the rack it is planned for drawn in dashes.
    other = second_colour(accent)
    b = bubble(215, 320, 260, 180, other) + line(475, 410, 620, 410, other, 12)
    b += outline(620, 250, 380, 340, accent) + chip(690, 320, 240, 200)
    b += arrow(1020, 1140, 420, accent, broken=True)
    b += f'<rect x="1160" y="245" width="220" height="360" rx="20" fill="#FFFFFF" stroke="{other}" stroke-width="6" stroke-dasharray="22 16"/>'
    return b + "".join(rect(1185, 275 + i * 80, 170, 52, PALE, "none", 10) for i in range(4))


def _chatgpt_ads(accent: str) -> str:
    # The four levels an ad is bought through, small to large, and on the right the chat and
    # the ad kept apart by a dashed line: the announcement's own claim, drawn as a gap.
    other = second_colour(accent)
    b = "".join(rect(230 + i * 70, 590 - (60 + i * 55), 60 + i * 55, 60 + i * 55, "#FFFFFF" if i % 2 else PALE, accent if i % 2 == 0 else other, 16 + i * 4) for i in range(4))
    b += arrow(690, 800, 440, other)
    b += bubble(840, 280, 240, 160, accent) + "".join(line(880, 320 + i * 34, 1040 - (i % 2) * 40, 320 + i * 34, "#C4CCCC", 10) for i in range(3))
    b += dashed(1130, 250, 1130, 640, INK, 8)
    b += rect(1180, 300, 210, 140, PALE, other, 14) + line(1285, 440, 1285, 620, other, 12) + line(1240, 620, 1330, 620, other, 12)
    return b + rect(1205, 325, 80, 90, "#FFFFFF", other, 10) + line(1305, 345, 1365, 345, other, 10) + line(1305, 385, 1350, 385, other, 10)


def _frontier_governance(accent: str) -> str:
    # One document answering two overlapping sets of rules, and the three-step scale it grades
    # risk on -- the top step still dashed, because the framework calls its levels exploratory.
    other = second_colour(accent)
    b = sheet(230, 245, 260, 340, accent, rows=6)
    b += line(490, 415, 600, 415, "#C4CCCC", 10)
    b += circle(730, 415, 120, "none", other) + circle(870, 415, 120, "none", accent) + circle(800, 415, 20, INK, "none")
    b += line(1010, 415, 1120, 415, "#C4CCCC", 10)
    b += rect(1150, 500, 220, 110, PALE, other, 14) + rect(1150, 380, 220, 110, "#FFFFFF", accent, 14)
    return b + f'<rect x="1150" y="260" width="220" height="110" rx="14" fill="#FFFFFF" stroke="{accent}" stroke-width="6" stroke-dasharray="22 16"/>'


# --- batch 4.5: the news since 2026-09-16 ---------------------------------------------------


def _eu_kids_act(accent: str) -> str:
    # Three doors, small to large: the first a dashed frame (no account before 13), the second
    # ajar with a padlock beside it (a guardian's mini account), the third open. On the right a
    # ticked sheet still inside a dashed outline: design duties, in a proposal.
    other = second_colour(accent)
    b = f'<rect x="230" y="360" width="150" height="260" rx="20" fill="#FFFFFF" stroke="{other}" stroke-width="6" stroke-dasharray="22 16"/>'
    b += rect(450, 300, 190, 320, "#FFFFFF", accent, 20) + rect(480, 330, 70, 290, PALE, "none", 12) + padlock(640, 470, 0.6, other)
    b += rect(740, 240, 230, 380, "#FFFFFF", accent, 20) + rect(770, 270, 200, 350, PALE, "none", 12)
    b += arrow(1010, 1100, 430, other)
    return b + outline(1120, 240, 300, 380, other) + sheet(1165, 285, 210, 290, accent, rows=5) + tick(1345, 320, 40, accent)


def _chatgpt_sponsored_agents(accent: str) -> str:
    # A chat bubble with a smaller bubble nested inside it -- the sponsored conversation that
    # opens beside the chat -- a dashed line keeping the two apart, and a three-step funnel:
    # plan, region and test decide who sees an ad at all.
    other = second_colour(accent)
    b = bubble(230, 250, 520, 340, accent) + bubble(420, 380, 260, 150, other)
    b += "".join(line(280, 320 + i * 36, 560 - (i % 2) * 60, 320 + i * 36, "#C4CCCC", 10) for i in range(2))
    b += dashed(830, 240, 830, 640, INK, 8)
    for i, width in enumerate((440, 320, 200)):
        x = 1160 - width / 2
        b += rect(x, 280 + i * 120, width, 90, "#FFFFFF" if i % 2 else PALE, accent if i % 2 == 0 else other, 16)
    return b


def _firefox_smart_window_mistral(accent: str) -> str:
    # A browser window drawn as an outline, a slot cut into its right edge with a hexagon
    # sliding in, and two more hexagons waiting beside it: the model as a part that can be
    # swapped, not a brand.
    other = second_colour(accent)
    b = rect(230, 240, 720, 420, "#FFFFFF", INK, 24) + line(230, 310, 950, 310, INK, 6)
    b += "".join(circle(270 + i * 34, 275, 10, other if i == 0 else PALE, "none") for i in range(3))
    b += rect(270, 350, 420, 40, PALE, "none", 12) + rect(270, 420, 560, 40, PALE, "none", 12) + rect(270, 490, 340, 40, PALE, "none", 12)
    b += slot(870, 400, 130, accent, broken=False) + hexagon(935, 465, 52, accent, PALE)
    b += arrow(1180, 1040, 465, other)
    return b + hexagon(1250, 400, 52, other, "#FFFFFF") + hexagon(1250, 540, 52, accent, "#FFFFFF")


def _google_cc_family_agent(accent: str) -> str:
    # A house drawn as an outline, one node at its centre -- the agent's own account -- and
    # lines from it to six small dots on the frame, the members; one line carries a tick,
    # because acting needs a member's permission.
    other = second_colour(accent)
    b = f'<path d="M 800 230 L 1150 410 L 1150 660 L 450 660 L 450 410 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    points = ((450, 530), (600, 660), (800, 660), (1000, 660), (1150, 530), (800, 230))
    for i, (x, y) in enumerate(points):
        b += line(800, 470, x, y, other if i % 2 else accent, 8)
        b += circle(x, y, 18, "#FFFFFF", other if i % 2 else accent)
    b += tick(700, 565, 34, accent)
    return b + circle(800, 470, 70, PALE, accent) + circle(800, 470, 26, accent, "none")


def _taiwan_matsu_cable_tm4(accent: str) -> str:
    # The main island as a rounded block, Matsu as a small square, three cables arched across
    # the strait -- the third now solid -- a microwave tower beside them and three dots in an
    # arc above: the orbits of the satellites the announcement lists as the last layer.
    other = second_colour(accent)
    b = rect(230, 280, 260, 380, PALE, accent, 40) + rect(1180, 400, 130, 130, PALE, accent, 20)
    for i, lift in enumerate((150, 90, 30)):
        b += curve(490, 470, 835, 470 - lift * 2, 1180, 470, accent if i % 2 == 0 else other, 12)
    b += tower(1385, 430, other, 110)
    b += "".join(circle(700 + i * 130, 240 - (i == 1) * 30, 14, other, "none") for i in range(3))
    return b + f'<path d="M 660 260 Q 830 150 1000 260" fill="none" stroke="{other}" stroke-width="4" stroke-dasharray="14 14"/>'


def person(x, y, color=BLUE):
    """A figure reduced to a head and a rounded body."""
    return circle(x, y, 34, "#FFFFFF", color) + f'<path d="M {x - 62} {y + 150} v -50 a 62 62 0 0 1 124 0 v 50 Z" fill="{PALE}" stroke="{color}" stroke-width="6"/>'


def _fca_p2p_crackdown(accent: str) -> str:
    # A notice with a prohibition sign, two figures joined by a dashed two-way arrow -- trade
    # between persons -- and a timeline underneath with two dots: the day of the operation and
    # the day it was announced, a week apart.
    other = second_colour(accent)
    b = sheet(240, 240, 240, 320, accent, rows=4)
    b += circle(400, 300, 40, "#FFFFFF", other) + line(372, 272, 428, 328, other, 10)
    b += person(720, 330, accent) + person(1180, 330, other)
    b += dashed(810, 400, 1090, 400, INK, 8)
    b += f'<path d="M 830 380 L 800 400 L 830 420 Z M 1070 380 L 1100 400 L 1070 420 Z" fill="{INK}"/>'
    b += line(560, 640, 1360, 640, "#C4CCCC", 8) + dashed(760, 640, 1160, 640, other, 8)
    return b + circle(760, 640, 22, accent, "none") + circle(1160, 640, 22, other, "none")


def clock(x, y, r=60, color=BLUE):
    return circle(x, y, r, "#FFFFFF", color) + line(x, y, x, y - r * 0.6, color, 8) + line(x, y, x + r * 0.45, y, color, 8)


def _apple_att_eu(accent: str) -> str:
    # A prompt dialog split down the middle -- one half drawn solid, the other dashed, the
    # second version -- and two lines from it: one to a row of five small squares, the
    # countries where only the new version may be shown, one to a clock, the year after which
    # a developer may ask again.
    other = second_colour(accent)
    b = rect(330, 240, 300, 260, "#FFFFFF", accent, 24)
    b += f'<rect x="630" y="240" width="300" height="260" rx="24" fill="#FFFFFF" stroke="{other}" stroke-width="6" stroke-dasharray="22 16"/>'
    b += line(630, 240, 630, 500, INK, 6)
    b += "".join(line(370, 300 + i * 40, 590, 300 + i * 40, "#C4CCCC", 10) for i in range(3)) + rect(370, 430, 100, 40, PALE, "none", 10)
    b += "".join(line(670, 300 + i * 40, 890, 300 + i * 40, "#C4CCCC", 10) for i in range(3)) + rect(670, 430, 100, 40, PALE, "none", 10) + rect(790, 430, 100, 40, "#FFFFFF", other, 10)
    b += line(480, 500, 480, 600, INK, 6) + line(880, 500, 880, 600, INK, 6)
    b += "".join(rect(280 + i * 90, 600, 70, 70, PALE if i % 2 == 0 else "#FFFFFF", accent, 14) for i in range(5))
    return b + clock(880, 660, 60, other)


def _fca_perimeter_guidance(accent: str) -> str:
    # A document on the left and a timeline on the right with four nodes: the first two solid
    # -- Parliament's rules and the guidance published -- the last two dashed, the application
    # window and the regime's commencement still ahead.
    other = second_colour(accent)
    b = sheet(240, 240, 260, 340, accent, rows=6)
    b += line(600, 450, 1380, 450, "#C4CCCC", 8)
    for i, x in enumerate((660, 880, 1100, 1320)):
        colour = accent if i % 2 == 0 else other
        if i < 2:
            b += circle(x, 450, 26, colour, "none")
        else:
            b += f'<circle cx="{x}" cy="450" r="26" fill="#FFFFFF" stroke="{colour}" stroke-width="6" stroke-dasharray="12 10"/>'
        b += rect(x - 60, 520 if i % 2 == 0 else 320, 120, 60, "#FFFFFF" if i < 2 else PALE, colour, 12)
    return b


def _astra_for_law(accent: str) -> str:
    # A magnifier over a stack of documents, light to dark -- sources that can be opened and
    # checked -- and four small squares in a row underneath: model, index, the selected firms,
    # the data terms.
    other = second_colour(accent)
    b = "".join(rect(560 + i * 40, 250 + i * 40, 320, 240, PALE if i == 2 else "#FFFFFF", accent if i % 2 == 0 else other, 20) for i in range(3))
    b += "".join(line(680, 370 + i * 36, 830, 370 + i * 36, "#C4CCCC", 10) for i in range(3))
    b += magnifier(990, 300, 80, other)
    return b + "".join(rect(560 + i * 130, 600, 90, 70, "#FFFFFF" if i % 2 else PALE, accent if i % 2 == 0 else other, 14) for i in range(4))


def _cftc_passive_software(accent: str) -> str:
    # A letter with a round stamp -- a staff no-action letter -- a phone whose screen is split
    # into an ordinary area and a shaded regulated area, and three blocks wired to the phone
    # underneath: the registered firms the software hands orders to.
    other = second_colour(accent)
    b = letter(240, 300, 300, 200, accent) + circle(490, 330, 40, "none", other) + circle(490, 330, 14, other, "none")
    b += phone(760, 180, 240, 440, INK)
    b += line(782, 400, 978, 400, INK, 6) + rect(782, 406, 196, 154, other, "none", 12)
    b += "".join(line(730 + i * 200, 660, 880, 620, "#C4CCCC", 8) for i in range(3))
    b += "".join(rect(660 + i * 200, 660, 140, 60, "#FFFFFF", accent if i % 2 == 0 else other, 12) for i in range(3))
    return b


def _anthropic_pace_metrics(accent: str) -> str:
    # Three gauges side by side, each needle at a different mark, and a question mark drawn
    # as an outline above them: numbers a lab measured about itself, still awaiting a reader
    # from outside.
    other = second_colour(accent)
    b = ""
    for i, (x, angle) in enumerate(((420, 150), (800, 60), (1180, 120))):
        colour = accent if i % 2 == 0 else other
        b += f'<path d="M {x - 150} 620 A 150 150 0 0 1 {x + 150} 620" fill="none" stroke="{colour}" stroke-width="16" stroke-linecap="round"/>'
        b += f'<path d="M {x - 110} 620 A 110 110 0 0 1 {x + 110} 620" fill="none" stroke="{PALE}" stroke-width="12" stroke-linecap="round"/>'
        rad = math.radians(angle)
        b += line(x, 620, x - 120 * math.cos(rad), 620 - 120 * math.sin(rad), INK, 10) + circle(x, 620, 16, INK, "none")
    return b + f'<path d="M 760 290 q 0 -60 70 -60 q 70 0 70 55 q 0 35 -40 55 q -30 15 -30 40" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>' + circle(830, 415, 10, INK, "none")


def _openai_misalignment_reports(accent: str) -> str:
    # An upright document carrying six small squares in two rows -- the six reports -- and
    # beside it a stepped arrow climbing to a magnifier: published first, explained step by
    # step afterwards.
    other = second_colour(accent)
    b = sheet(360, 230, 340, 440, accent, rows=0)
    b += "".join(rect(400 + (i % 3) * 95, 300 + (i // 3) * 110, 70, 70, PALE if i % 2 == 0 else "#FFFFFF", accent if i % 2 == 0 else other, 12) for i in range(6))
    b += line(400, 540, 660, 540, "#C4CCCC", 10) + line(400, 590, 600, 590, "#C4CCCC", 10)
    b += f'<path d="M 800 640 h 90 v -80 h 90 v -80 h 90 v -80 h 60" fill="none" stroke="{other}" stroke-width="12" stroke-linejoin="round" stroke-linecap="round"/>'
    b += f'<path d="M 1110 380 l 30 20 l -30 20" fill="none" stroke="{other}" stroke-width="12" stroke-linejoin="round" stroke-linecap="round"/>'
    return b + magnifier(1240, 380, 80, accent)


def _app_store_bundles_multiseat(accent: str) -> str:
    # Five equal blocks in a ring, each tied by a line to one receipt in the middle -- several
    # subscriptions sold as one purchase -- and on the right three figures over one shared
    # disc: one purchase used by several people.
    other = second_colour(accent)
    b = ""
    for i in range(5):
        rad = math.radians(-90 + i * 72)
        x, y = 470 + 200 * math.cos(rad), 450 + 200 * math.sin(rad)
        b += line(470, 450, x, y, "#C4CCCC", 8) + rect(x - 40, y - 40, 80, 80, PALE if i % 2 == 0 else "#FFFFFF", accent if i % 2 == 0 else other, 14)
    b += sheet(410, 385, 120, 130, accent, rows=3)
    b += "".join(person(960 + i * 150, 330, other if i % 2 else accent) for i in range(3))
    return b + circle(1110, 600, 60, PALE, accent) + circle(1110, 600, 20, accent, "none")


# slug -> its composition. Keyed by the whole slug: two of this batch's slugs share a topic
# word (the two JFSA pieces, the four GENIUS Act rules), so a substring match as batch 3 used
# would hand one article another's picture.
_DRAWINGS = {
    "crypto-news-taiwan-vasp-act-20260630": _taiwan_vasp_act,
    "crypto-news-mica-transition-ends-20260701": _mica_transition,
    "crypto-news-sec-crypto-interpretation-20260323": _sec_cftc_interpretation,
    "crypto-news-sec-regulation-crypto-assets-20260821": _sec_regulation_crypto_assets,
    "crypto-news-eba-psd2-mica-20260212": _eba_psd2_mica,
    "crypto-news-genius-act-occ-20260302": _genius_act_occ,
    "crypto-news-stablecoin-aml-20260410": _stablecoin_aml,
    "crypto-news-fdic-genius-act-20260410": _fdic_genius_act,
    "crypto-news-ncua-genius-act-20260518": _ncua_genius_act,
    "crypto-news-jfsa-working-group-20260216": _jfsa_working_group,
    "crypto-news-jfsa-cybersecurity-20260723": _jfsa_cybersecurity,
    "crypto-news-2026-index": _crypto_index,
    "tech-news-iphone-duo-20260909": _iphone_duo,
    "tech-news-apple-september-hardware-20260909": _apple_september_hardware,
    "tech-news-eu-cra-reporting-20260911": _eu_cra_reporting,
    "tech-news-taiwan-sovereign-ai-corpus-20260915": _taiwan_sovereign_ai_corpus,
    "tech-news-taiwan-6g-spectrum-20260910": _taiwan_6g_spectrum,
    "tech-news-taiwan-matsu-cable-20260623": _taiwan_matsu_cable,
    "tech-news-apple-eu-business-terms-20260818": _apple_eu_business_terms,
    "tech-news-windows-project-zenith-20260904": _windows_project_zenith,
    "tech-news-pixel-drop-20260915": _pixel_drop,
    "tech-news-apple-m6-m5-ultra-20260825": _apple_m6_m5_ultra,
    "tech-news-nvidia-cuda-q-20260914": _nvidia_cuda_q,
    "tech-news-nvidia-mediatek-20260831": _nvidia_mediatek,
    "tech-news-nvidia-vera-rubin-20260915": _nvidia_vera_rubin,
    "tech-news-2026-index": _tech_index,
    "ai-news-chatgpt-storage-scale-20260911": _chatgpt_storage_scale,
    "ai-news-openai-astral-20260319": _openai_astral,
    "ai-news-gpt-live-1-api-20260910": _gpt_live_1_api,
    "ai-news-chatgpt-financial-services-20260910": _chatgpt_financial_services,
    "ai-news-nvidia-hugging-face-20260903": _nvidia_hugging_face,
    "ai-news-openai-funding-20260331": _openai_funding,
    "ai-news-openai-s1-20260608": _openai_s1,
    "ai-news-gemini-38-live-20260915": _gemini_38_live,
    "ai-news-gpt-55-instant-20260505": _gpt_55_instant,
    "ai-news-openai-broadcom-chip-20260624": _openai_broadcom_chip,
    "ai-news-chatgpt-ads-20260505": _chatgpt_ads,
    "ai-news-frontier-governance-20260528": _frontier_governance,
    # batch 4.5
    "tech-news-eu-kids-act-20260917": _eu_kids_act,
    "ai-news-chatgpt-sponsored-agents-20260916": _chatgpt_sponsored_agents,
    "ai-news-firefox-smart-window-mistral-20260916": _firefox_smart_window_mistral,
    "ai-news-google-cc-family-agent-20260918": _google_cc_family_agent,
    "tech-news-taiwan-matsu-cable-tm4-20260918": _taiwan_matsu_cable_tm4,
    "crypto-news-fca-p2p-crypto-crackdown-20260917": _fca_p2p_crackdown,
    "tech-news-apple-att-eu-20260916": _apple_att_eu,
    "crypto-news-fca-perimeter-guidance-20260916": _fca_perimeter_guidance,
    "ai-news-astra-for-law-20260917": _astra_for_law,
    "crypto-news-cftc-passive-software-20260917": _cftc_passive_software,
    "ai-news-anthropic-pace-metrics-20260917": _anthropic_pace_metrics,
    "ai-news-openai-misalignment-reports-20260917": _openai_misalignment_reports,
    "tech-news-app-store-bundles-multiseat-20260916": _app_store_bundles_multiseat,
}


def drawing(slug: str, accent: str) -> str:
    """The hero composition of one article. One entry per article, added as it is written --
    an original drawing per article is the point, so an unknown slug stops the run rather than
    quietly reusing someone else's picture."""
    if slug not in _DRAWINGS:
        raise SystemExit(f"no drawing for {slug}; add one to _DRAWINGS in {Path(__file__).name}")
    return _DRAWINGS[slug](accent)


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
    only = only_slugs()
    if only:
        research = [item for item in research if item["slug"] in only]
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
    if not only:
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


def only_slugs() -> set[str]:
    """The articles named with ``--slug=``, or nothing for the whole vertical."""
    return {a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--slug=")}


def main() -> None:
    named = [a for a in sys.argv[1:] if not a.startswith("--")]
    unknown = [name for name in named if name not in BY_NAME]
    if unknown:
        raise SystemExit(f"unknown vertical {unknown}; one of " + ", ".join(BY_NAME))
    for slug in only_slugs():
        vertical_of(slug)  # a mistyped slug is named here, not skipped in silence below
    chosen = [BY_NAME[name] for name in named] if named else list(VERTICALS)
    for vertical in chosen:
        manifest = build(vertical)
        if not manifest:
            print("nothing to draw:" if only_slugs() else "no research records yet:", vertical.workspace, flush=True)
            continue
        if "--svg-only" not in sys.argv and not only_slugs():
            sheets(vertical, manifest)


if __name__ == "__main__":
    main()
