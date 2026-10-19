"""Original animated storybook artwork for Sunny & Pip's preschool pilots.

Only Pillow is required. The bottom 90 pixels are intentionally free for CC.
No stock illustrations, generated images, or remote assets are used.
"""

from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

try:
    from .objects import NEW_VISUALS, draw_object
except ImportError:
    from objects import NEW_VISUALS, draw_object

WIDTH, HEIGHT = 1280, 720
SCALE = 2
INK = "#3F514B"
LINE = "#9D7959"
CREAM = "#F9DDB0"
MUZZLE = "#FFF2D7"
MINT = "#9BCDAB"
TEAL = "#5B9E8C"
PAPER = "#FFF9EE"
COLORS = {"red": "#EA776D", "blue": "#73ADE0", "yellow": "#F4CE64",
          "green": "#85B989", "color_orange": "#EBA255", "purple": "#A58BC4"}
COUNT_VALUES = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
VALID_VISUALS = frozenset(COLORS) | frozenset(COUNT_VALUES) | NEW_VISUALS | frozenset(
    {"hello", "goodbye", "wave", "happy", "sad", "stand", "sit", "clap"})


@lru_cache(maxsize=32)
def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    suffix = "-Bold" if bold else ""
    return ImageFont.truetype(
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans{suffix}.ttf", size * SCALE
    )


class Pen:
    def __init__(self, image: Image.Image):
        self.image = image
        self.d = ImageDraw.Draw(image)

    @staticmethod
    def box(box):
        return tuple(round(v * SCALE) for v in box)

    def ellipse(self, box, fill, outline=None, width=2):
        self.d.ellipse(self.box(box), fill, outline, round(width * SCALE))

    def rect(self, box, fill, radius=0, outline=None, width=2):
        self.d.rounded_rectangle(
            self.box(box), round(radius * SCALE), fill, outline, round(width * SCALE)
        )

    def line(self, points, fill, width=2, joint="curve"):
        xy = [(round(x * SCALE), round(y * SCALE)) for x, y in points]
        self.d.line(xy, fill, round(width * SCALE), joint=joint)

    def polygon(self, points, fill):
        self.d.polygon([(round(x * SCALE), round(y * SCALE)) for x, y in points], fill)

    def arc(self, box, start, end, fill, width=2):
        self.d.arc(self.box(box), start, end, fill, round(width * SCALE))

    def text(self, xy, text, size, fill=INK, bold=False, anchor="mm"):
        self.d.text(
            (round(xy[0] * SCALE), round(xy[1] * SCALE)),
            str(text), font=_font(size, bold), fill=fill, anchor=anchor,
        )


def _cloud(p, x, y, s=1):
    for dx, dy, r in [(-35, 5, 25), (-8, -8, 34), (29, 4, 26)]:
        p.ellipse((x+(dx-r)*s, y+(dy-r)*s, x+(dx+r)*s, y+(dy+r)*s), "#FFFDFA")
    p.rect((x-53*s, y+2*s, x+49*s, y+26*s), "#FFFDFA", 15*s)


@lru_cache(maxsize=1)
def _background():
    image = Image.new("RGB", (WIDTH*SCALE, HEIGHT*SCALE), PAPER)
    p = Pen(image)
    p.rect((28, 23, 1252, 623), "#F2F8E9", 34)
    p.rect((29, 24, 1251, 105), "#FFFDF7", 33)
    p.rect((29, 73, 1251, 106), "#FFFDF7")
    # Landscape remains intentionally quiet; learning objects occupy the foreground.
    p.ellipse((-170, 345, 590, 687), "#E1EDD0")
    p.ellipse((725, 370, 1400, 655), "#E9EBCF")
    p.ellipse((175, 427, 1080, 810), "#ECF0D8")
    p.rect((29, 491, 1251, 623), "#FFFDF7", 28)
    p.rect((29, 491, 1251, 560), "#FFFDF7")
    _cloud(p, 136, 196, 0.8)
    _cloud(p, 1127, 194, 1.1)
    # Small brand sun, distinct from the countable foreground objects.
    p.ellipse((57, 45, 86, 74), "#F1CC69")
    for a in range(0, 360, 45):
        rad = math.radians(a)
        p.line([(71.5+19*math.cos(rad), 59.5+19*math.sin(rad)),
                (71.5+23*math.cos(rad), 59.5+23*math.sin(rad))], "#D9B351", 2)
    p.text((104, 61), "SUNNY & PIP", 20, bold=True, anchor="lm")
    # Caption safe area is plain and uninterrupted.
    p.rect((0, 624, WIDTH, HEIGHT), PAPER)
    p.line([(95, 644), (1185, 644)], "#E7E5D9", 1)
    return image


def _limb(p, a, b, s, fill=CREAM):
    p.line([a, b], LINE, 30*s)
    p.ellipse((b[0]-15*s, b[1]-15*s, b[0]+15*s, b[1]+15*s), LINE)
    p.line([a, b], fill, 24*s)
    p.ellipse((b[0]-12*s, b[1]-12*s, b[0]+12*s, b[1]+12*s), fill)


def _bear(p, x, ground, s=1.0, pose="neutral", t=0, face=None, sit_amount=None):
    """Draw Sunny with round cream ears and a teal knitted top."""
    sitting = float(pose == "sit") if sit_amount is None else max(0.0, min(1.0, sit_amount))
    clap = pose == "clap"
    wave = pose in {"hello", "goodbye", "wave"}
    face = face or (pose if pose in {"happy", "sad"} else "happy")
    bob = 2 * math.sin(t*2.4) * (1-sitting)
    if pose == "happy":
        bob += -4 * max(0, math.sin(t*2.6))
    y = ground + bob
    offset = 53*sitting

    def pt(px, py):
        return (x+px*s, y+(py+offset)*s)

    def box(a, b, c, d):
        return (x+a*s, y+(b+offset)*s, x+c*s, y+(d+offset)*s)

    p.ellipse((x-83*s, ground-10*s, x+83*s, ground+12*s), "#CDDEC0")
    if sitting or pose in {"stand", "sit"}:
        p.rect((x-94*s, ground-46*s, x+94*s, ground-30*s), "#B7A8C9", 6*s)
        p.rect((x-86*s, ground-31*s, x-75*s, ground+1*s), "#9585AA", 3*s)
        p.rect((x+75*s, ground-31*s, x+86*s, ground+1*s), "#9585AA", 3*s)
    def blend(a, b):
        return tuple(v+(w-v)*sitting for v, w in zip(a, b))
    for standing_leg, seated_leg in [
        ((-56,-63,-8,0),(-79,-41,-13,-2)),
        ((8,-63,56,0),(13,-41,79,-2)),
        ((-66,-24,-7,2),(-79,-27,-13,-2)),
        ((7,-24,66,2),(13,-27,79,-2)),
    ]:
        a,b,c,d = blend(standing_leg, seated_leg)
        p.ellipse((x+a*s, ground+b*s, x+c*s, ground+d*s), CREAM, LINE, 2.5*s)
    p.ellipse(box(*blend((-67,-149,67,-25),(-63,-156,63,-76))), TEAL, "#518876", 2.5*s)
    p.rect(box(*blend((-53,-106,53,-43),(-51,-117,51,-82))), TEAL, 9*s)
    hem = -43-40*sitting
    p.line([pt(-43+3*sitting, hem), pt(43-3*sitting, hem)], "#A3C9B5", 4*s)
    if sitting < .9:
        p.rect(box(*blend((-17,-94,17,-67),(-15,-121,15,-96))), "#B5D6BD", 5*s)

    if not clap:
        left = pt(-87, -82)
        right = pt(89, -81)
        if wave:
            right = pt(103 + 12*math.sin(t*4), -204 + 5*math.cos(t*4))
        _limb(p, pt(-53, -122), left, s)
        _limb(p, pt(53, -122), right, s)
        if wave:
            p.ellipse((right[0]-6*s, right[1]-6*s, right[0]+6*s, right[1]+6*s), "#E9BB91")

    # Ears and face sit above the sweater.
    p.ellipse(box(-89, -246, -29, -186), CREAM, LINE, 2.5*s)
    p.ellipse(box(29, -246, 89, -186), CREAM, LINE, 2.5*s)
    p.ellipse(box(-76, -233, -43, -199), "#EABB94")
    p.ellipse(box(43, -233, 76, -199), "#EABB94")
    p.ellipse(box(-84, -232, 84, -96), CREAM, LINE, 2.5*s)
    p.ellipse(box(-50, -169, 50, -105), MUZZLE)
    p.ellipse(box(-60, -160, -34, -145), "#EEB99B")
    p.ellipse(box(34, -160, 60, -145), "#EEB99B")
    blink = t % 5.1 < 0.15
    for side in (-1, 1):
        ex = side*31
        if blink:
            p.line([pt(ex-6, -175), pt(ex+6, -175)], INK, 3*s)
        elif face == "happy":
            p.arc(box(ex-8, -180, ex+8, -164), 195, 345, INK, 3*s)
        else:
            p.ellipse(box(ex-4, -181, ex+4, -169), INK)
        if face == "sad":
            p.line([pt(ex-side*8, -195), pt(ex+side*8, -189)], LINE, 3*s)
    p.ellipse(box(-9, -153, 9, -143), INK)
    p.line([pt(0, -144), pt(0, -135)], INK, 2*s)
    if face == "sad":
        p.arc(box(-17, -130, 17, -111), 205, 335, INK, 3*s)
        p.ellipse(box(47, -145, 54, -132), "#9EC9D1")
    else:
        p.arc(box(-22, -149, 22, -121), 20, 160, INK, 3*s)
    if clap:
        # Palms overlap at the center during every beat, visibly making contact.
        opening = 33 * (0.5 + 0.5*math.cos(t*4.4)) ** 2
        _limb(p, pt(-55, -108), pt(-8-opening, -88), s)
        _limb(p, pt(55, -108), pt(8+opening, -88), s)
        if opening < 2:
            for dx, dy in [(-24, -108), (0, -115), (24, -108)]:
                p.line([pt(dx, dy), pt(dx*1.18, dy-7)], "#D8A957", 2.5*s)


def _bird(p, x, y, s=1.0, t=0, facing=1):
    bob = 4*math.sin(t*3)
    y += bob
    def box(a, b, c, d):
        return (x+a*s, y+b*s, x+c*s, y+d*s)
    # Tail goes behind the body; beak changes direction for arrivals/departures.
    tail = -facing
    p.polygon([(x+tail*44*s, y+10*s), (x+tail*74*s, y-1*s),
               (x+tail*65*s, y+25*s), (x+tail*39*s, y+31*s)], "#80B79A")
    p.ellipse(box(-49, -47, 49, 47), MINT, "#6EA083", 2*s)
    p.ellipse(box(-29, -17, 35, 40), "#DDF0D8")
    flap = 13*math.sin(t*5)
    p.ellipse(box(-47, -2+flap, -4, 23+flap), "#7CB69C", "#6EA083", 1.5*s)
    ex = 19*facing
    if t % 4.5 < 0.16:
        p.line([(x+(ex-5)*s, y-15*s), (x+(ex+5)*s, y-15*s)], INK, 2*s)
    else:
        p.ellipse(box(ex-4, -22, ex+4, -12), INK)
    beakx = x + facing*44*s
    p.polygon([(beakx, y-16*s), (beakx+facing*23*s, y-9*s),
               (beakx, y-2*s)], "#D9A354")
    p.ellipse(box(ex-2, -5, ex+14, 5), "#E8B7A0")
    p.line([(x-16*s, y+43*s), (x-18*s, y+55*s)], "#C89B63", 3*s)
    p.line([(x+14*s, y+43*s), (x+16*s, y+55*s)], "#C89B63", 3*s)


def _ball(p, x, y, r, color, t=0, bounce=True):
    dy = -4*math.sin(t*2.2) if bounce else 0
    p.ellipse((x-r*.84, y+r*.9, x+r*.84, y+r*1.15), "#D8E3CA")
    p.ellipse((x-r, y-r+dy, x+r, y+r+dy), color)
    p.arc((x-r*.70, y-r*.70+dy, x+r*.63, y+r*.63+dy), 34, 137, "#FFFFFF", max(2, r*.032))
    p.ellipse((x-r*.47, y-r*.53+dy, x-r*.08, y-r*.29+dy), "#FFF6E9")


def _count(p, token, x, y, width, t=0, layout="row", highlight=None):
    n = COUNT_VALUES[token]
    radius = min(63, width / (n*2.65))
    step = radius*2.65
    triangle = layout == "triangle" and n == 3
    positions = [(x, y-radius*1.15), (x-radius*1.35, y+radius*1.15), (x+radius*1.35, y+radius*1.15)] if triangle else [(x+(i-(n-1)/2)*step, y) for i in range(n)]
    tray_h = radius*(2.65 if triangle else 1.45)
    tray_w = min(width/2, (n*2.65-.45)*radius/2+20) if not triangle else radius*2.8
    p.ellipse((x-tray_w, y-tray_h+9, x+tray_w, y+tray_h+13), "#D5DEC8")
    p.ellipse((x-tray_w, y-tray_h, x+tray_w, y+tray_h), "#FFFDF6", "#C8D8C6", 3)
    p.ellipse((x-tray_w+9, y-tray_h+9, x+tray_w-9, y+tray_h-9), "#F3EEE0", "#E2DBC8", 2)
    for i, (cx, cy) in enumerate(positions):
        if highlight == i:
            p.ellipse((cx-radius-9,cy-radius-9,cx+radius+9,cy+radius+9), "#FFE29B", "#CF9A3F", 3)
        p.ellipse((cx-radius,cy-radius+4,cx+radius,cy+radius+4), "#C1A678")
        p.ellipse((cx-radius,cy-radius,cx+radius,cy+radius), "#EBC589", "#CFA36E", 2)
        for dx,dy,rr in [(-.38,-.32,.10),(.23,-.42,.11),(.43,.15,.09),(-.23,.39,.10),(-.04,-.01,.11)]:
            p.ellipse((cx+(dx-rr)*radius,cy+(dy-rr)*radius,cx+(dx+rr)*radius,cy+(dy+rr)*radius), "#805844")


def _movement(pose, elapsed):
    progress = max(0.0, min(1.0, elapsed/1.45))
    progress = progress*progress*(3-2*progress)
    return progress if pose == "sit" else 1-progress


def _falling_blocks(p, t):
    progress = max(0.0, min(1.0, t/1.0))
    progress = progress*progress*(3-2*progress)
    # A small, harmless tower tumbles beside Sunny, away from the character.
    for i, color in enumerate(("#80B4D0", "#E5B85F", "#DFA098")):
        x = 335 + (i-1)*65*progress
        y = (419-i*48)*(1-progress) + (419-abs(i-1)*7)*progress
        angle = ((i-1)*.28+.13)*progress
        points=[]
        for dx,dy in [(-22,-22),(22,-22),(22,22),(-22,22)]:
            points.append((x+dx*math.cos(angle)-dy*math.sin(angle), y+dx*math.sin(angle)+dy*math.cos(angle)))
        p.polygon(points, color)
        p.line(points+[points[0]], "#B09166", 2)
        p.line([points[0], points[2]], "#FFFFFF", 1)


def _choice_value(choice):
    if isinstance(choice, dict):
        return str(choice.get("visual", choice.get("value", choice.get("id", "hello"))))
    return str(choice)


def _choice_art(p, value, x, y, width, t, action_elapsed=None):
    if value in COLORS:
        _ball(p, x, y, min(66, width*.27), COLORS[value], t)
    elif value in COUNT_VALUES:
        _count(p, value, x, y, width-24, t)
    elif value in {"happy", "sad"}:
        _bear(p, x, y+103, .70, value, t)
    elif value in {"stand", "sit", "clap"}:
        amount = _movement(value, action_elapsed) if value in {"stand", "sit"} and action_elapsed is not None else None
        _bear(p, x, y+100, .70, value, t, sit_amount=amount)
    elif value in NEW_VISUALS:
        draw_object(p, value, x, y-5, min(280, width-24), t)
    elif value in {"hello", "goodbye", "wave"}:
        _bear(p, x-20, y+101, .64, value, t)
        bird_x = x+(55 if value == "hello" else 90)
        _bird(p, bird_x, y-2, .42, t, -1 if value == "hello" else 1)
    else:
        raise ValueError(f"Unknown preschool visual token: {value!r}")


def _draw_choices(p, choices, target, t, revealed=False, labels=False, action_elapsed=None):
    values = [_choice_value(item) for item in choices]
    count = len(values)
    if not count:
        return
    left, right, gap = 307, 1190, 22
    card_w = (right-left-gap*(count-1))/count
    for i, value in enumerate(values):
        x0 = left + i*(card_w+gap)
        cx = x0+card_w/2
        selected = revealed and value == target
        color = "#FFFDF7" if not selected else "#FFF3CC"
        outline = "#E0E6D4" if not selected else "#D7AE54"
        p.rect((x0, 163, x0+card_w, 457), "#DCE6CC", 26)
        p.rect((x0, 158, x0+card_w, 451), color, 26, outline, 3 if selected else 1.5)
        _choice_art(p, value, cx, 308, card_w, t if (selected or value in NEW_VISUALS) else .7,
                    action_elapsed=action_elapsed if selected else None)
        if labels:
            label = value.replace("color_", "").replace("_", " ").capitalize()
            p.text((cx, 421), label, 22, bold=True)
        if selected:
            p.ellipse((cx-17, 129, cx+17, 163), TEAL)
            p.line([(cx-8, 146), (cx-2, 152), (cx+9, 140)], "#FFFFFF", 3)


def _fit_text(text, max_width=1130, initial_size=50):
    size = initial_size
    while size > 25 and _font(size, True).getlength(text) > max_width*SCALE:
        size -= 1
    return size


def render_frame(episode: dict, scene: dict, local_t: float, scene_duration: float = 18) -> Image.Image:
    """Render one 1280×720 RGB frame; quiz answers are gated by reveal_at.

    Scene mode accepts demo, repeat, review and quiz. ``choices`` contains visual
    identifiers; for a quiz the target never receives an early visual cue.
    """
    t = max(0.0, float(local_t))
    mode = str(scene.get("mode", scene.get("kind", scene.get("type", "demo"))))
    visual = str(scene.get("visual", scene.get("target", "hello")))
    target = str(scene.get("target", visual))
    reveal_at = float(scene.get("reveal_at", 12))
    demo_start = float(scene.get("demo_start", 5))
    demo_duration = max(.3, float(scene.get("demo_duration", 3)))
    revealed = mode != "quiz" or t >= reveal_at
    choices = scene.get("choices") or []
    for token in [visual, target, *[_choice_value(c) for c in choices]]:
        if token not in VALID_VISUALS:
            raise ValueError(f"Unknown preschool visual token: {token!r}")
    image = _background().copy()
    p = Pen(image)
    episode_number = episode.get("number", 1)
    title = str(episode.get("title_en", episode.get("topic", "Let's learn!")))
    p.text((1211, 61), f"{int(episode_number):02d}  /  {title}", 20, anchor="rm")
    mode_labels = {"demo": "LISTEN & LEARN", "repeat": "YOUR TURN", "review": "LET'S REMEMBER", "quiz": "LISTEN & POINT"}
    badge = mode_labels.get(mode, "LET'S PLAY")
    p.text((73, 131), badge, 14, "#658978", True, "lm")

    if choices:
        _bear(p, 175, 442, .78, "wave" if mode == "review" else "neutral", t)
        _bird(p, 242, 231, .48, t, -1)
        _draw_choices(p, choices, target, t, revealed=mode == "quiz" and revealed,
                      labels=mode == "review", action_elapsed=t-reveal_at)
    elif mode == "quiz" and not revealed:
        # A neutral listening scene cannot accidentally perform the answer.
        _bear(p, 497, 464, 1.13, "neutral", t)
        _bird(p, 816, 332, 1.04, t, -1)
        p.arc((385, 135, 603, 206), 218, 322, "#B6CBA8", 3)
    elif visual in COLORS:
        _bear(p, 340, 458, .95, "wave", t)
        _bird(p, 1077, 230, .57, t, -1)
        _ball(p, 829, 312, 122, COLORS[visual], t)
    elif visual in COUNT_VALUES:
        _bear(p, 250, 454, .89, "neutral", t)
        _bird(p, 1119, 228, .51, t, -1)
        n = COUNT_VALUES[visual]
        count_start = reveal_at if mode == "quiz" or t >= reveal_at else demo_start
        highlight = min(n-1, int((t-count_start)/demo_duration*n)) if count_start <= t < count_start+demo_duration else None
        layout = scene.get("layout", "triangle" if scene.get("id") == "ep04-s09" else "row")
        _count(p, visual, 832, 321, 560, t, layout, highlight)
    elif visual in {"stand", "sit", "clap"}:
        action_start = reveal_at if mode == "quiz" else demo_start
        amount = _movement(visual, t-action_start) if visual in {"stand", "sit"} else None
        _bear(p, 641, 464, 1.12, visual, t, sit_amount=amount)
        _bird(p, 925, 356, .88, t, -1)
    elif visual in {"happy", "sad"}:
        _bear(p, 565, 465, 1.18, visual, t)
        _bird(p, 872, 335, .91, t, -1)
        if scene.get("id") == "ep02-s04":
            _falling_blocks(p, t)
    elif visual in NEW_VISUALS:
        _bear(p, 294, 459, .92, "neutral", t)
        _bird(p, 1083, 239, .48, t, -1)
        draw_object(p, visual, 796, 301, 420, t)
    elif visual in {"hello", "goodbye", "wave"}:
        _bear(p, 487, 462, 1.13, visual, t)
        drift = (min(t, scene_duration)/max(1, scene_duration))*110 if visual == "goodbye" else 0
        _bird(p, 841+drift, 320-0.22*drift, 1.07, t, 1 if visual == "goodbye" else -1)

    # The teacher's English instruction is also embedded into the picture.
    # All language tracks share this timing; the large target follows the instruction.
    instruction_en = scene.get("instruction", {}).get("en")
    if instruction_en and t < float(scene.get("demo_start", 5)):
        text = instruction_en
    elif mode == "quiz":
        text = str(scene.get("demo", scene.get("english", "Well done!"))) if revealed else str(scene.get("english", "Listen and point."))
    else:
        text = str(scene.get("english", scene.get("demo", "Hello!")))
    p.text((640, 549), text, _fit_text(text), INK, True)

    # Small, calm dots indicate space for speaking without displaying extra text.
    if mode == "repeat" or (mode == "quiz" and not revealed):
        phase = int(t*.65) % 3
        for i in range(3):
            cx = 625+i*15
            p.ellipse((cx-3, 593, cx+3, 599), TEAL if phase == i else "#D8E5D3")
    else:
        p.line([(602, 597), (678, 597)], "#E4CB8F", 3)
    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def _fixtures():
    output = Path("/workspace/preschool-pilot-output")
    output.mkdir(parents=True, exist_ok=True)
    cases = [
        (1, "Hello, friends!", {"mode": "demo", "visual": "hello", "english": "Hello!"}, 2.0),
        (2, "How do you feel?", {"mode": "demo", "visual": "sad", "english": "I'm sad."}, 2.0),
        (3, "Color play", {"mode": "demo", "visual": "red", "english": "Red."}, 2.0),
        (4, "One, two, three", {"mode": "demo", "visual": "three", "english": "One, two, three."}, 2.0),
        (5, "Let's move!", {"mode": "demo", "visual": "sit", "english": "Sit down."}, 2.0),
        (5, "Let's move!", {"mode": "demo", "visual": "clap", "english": "Clap your hands."}, math.pi/4.4),
        (3, "Color play", {"mode": "quiz", "visual": "blue", "target": "blue", "choices": ["red", "blue", "yellow"], "english": "Listen and point.", "demo": "Blue.", "reveal_at": 12}, 3.0),
        (3, "Color play", {"mode": "quiz", "visual": "blue", "target": "blue", "choices": ["red", "blue", "yellow"], "english": "Listen and point.", "demo": "Blue.", "reveal_at": 12}, 13.0),
    ]
    sheet = Image.new("RGB", (1280, 1440), PAPER)
    for i, (number, title, scene, t) in enumerate(cases):
        frame = render_frame({"number": number, "title_en": title}, scene, t)
        if i in {0, 3, 5, 6, 7}:
            frame.save(output / f"art-check-{i+1:02d}.png")
        sheet.paste(frame.resize((640, 360), Image.Resampling.LANCZOS), ((i%2)*640, (i//2)*360))
    sheet.save(output / "art-check.png")
    print(output / "art-check.png")


if __name__ == "__main__":
    _fixtures()
