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
