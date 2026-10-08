"""Original Sunny & Pip classroom renderer for elementary English.

English is embedded in every frame. The bottom 90 pixels stay clear for the
four optional translated captions. All quiz answers, names and highlights are
withheld until reveal_at. No remote assets or global renderer changes are used.
"""

from __future__ import annotations

import math
from functools import lru_cache

from PIL import Image

from elementary.objects import NEW_VISUALS, VALID_VISUALS, draw_object
from elementary.shared import preschool_visuals as shared

WIDTH, HEIGHT, SCALE = shared.WIDTH, shared.HEIGHT, shared.SCALE
Pen, _font = shared.Pen, shared._font
INK, TEAL, PAPER = "#3F514B", "#5B9E8C", "#FFF9EE"
COLORS, COUNT_VALUES = shared.COLORS, shared.COUNT_VALUES


@lru_cache(maxsize=1)
def _background():
    image = Image.new("RGB", (WIDTH*SCALE, HEIGHT*SCALE), PAPER)
    p = Pen(image)
    p.rect((28, 23, 1252, 623), "#F5EDDF", 32)
    p.rect((28, 23, 1252, 106), "#FFFDF7", 32)
    p.rect((29, 74, 1251, 106), "#FFFDF7")
    # Quiet classroom architecture: no printed letters, quantities or answers.
    p.rect((354, 148, 1149, 453), "#D9C6AA", 15)
    p.rect((364, 158, 1139, 443), "#DCE8DD", 10)
    p.rect((358, 444, 1150, 455), "#C5AE8C", 4)
    p.rect((77, 174, 239, 332), "#E7D6BA", 8)
    p.rect((85, 182, 231, 324), "#F6FBF2", 4)
    p.line([(157, 184), (157, 324)], "#E7D6BA", 6)
    p.line([(86, 251), (230, 251)], "#E7D6BA", 6)
    p.ellipse((101, 196, 130, 225), "#F1D998")
    p.rect((76, 331, 241, 340), "#C6B299", 4)
    p.line([(30, 459), (1250, 459)], "#E4D7C5", 2)
    p.rect((29, 490, 1251, 623), "#FFFDF7", 28)
    p.rect((29, 490, 1251, 560), "#FFFDF7")
    p.ellipse((56, 46, 85, 75), "#F1CC69")
    p.text((103, 61), "SUNNY & PIP", 19, INK, True, "lm")
    p.rect((270, 43, 412, 80), "#EDF3E7", 12)
    p.text((341, 62), "ENGLISH CLUB", 13, "#648875", True)
    p.rect((0, 624, WIDTH, HEIGHT), PAPER)
    p.line([(95, 644), (1185, 644)], "#E7E5D9", 1)
    return image


def _fit_text(text, max_width=1110, initial_size=46, minimum=24):
    size = initial_size
    while size > minimum and _font(size, True).getlength(text) > max_width*SCALE:
        size -= 1
    return size


def text_layout(text, max_width=1110, initial_size=46):
    """Return fitted line/size pairs, preserving word spacing and punctuation."""
    text = str(text)
    size = _fit_text(text, max_width, initial_size)
    if _font(size, True).getlength(text) <= max_width*SCALE:
        return [(text, size)]
    words = text.split(" ")
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}" if current else word
        if current and _font(size, True).getlength(candidate) > max_width*SCALE:
            lines.append((current, size))
            current = word
        else:
            current = candidate
    if current:
        lines.append((current, size))
    if len(lines) > 2 or any(_font(s, True).getlength(line) > max_width*SCALE for line, s in lines):
        raise ValueError(f"English picture text exceeds the two-line safe area: {text!r}")
    return lines


def _choice_art(p, value, x, y, width, t, action_elapsed=None):
    if value in NEW_VISUALS:
        draw_object(p, value, x, y-4, min(270, width-35), t)
    else:
        shared._choice_art(p, value, x, y, width, t, action_elapsed)


def _draw_choices(p, choices, target, t, revealed=False, labels=False, action_elapsed=None):
    values = [shared._choice_value(item) for item in choices]
    if not 2 <= len(values) <= 4:
        raise ValueError("Elementary choice scenes require two to four pictures")
    left, right, gap = 86, 1194, 22
    card_w = (right-left-gap*(len(values)-1))/len(values)
    for i, value in enumerate(values):
        x0 = left+i*(card_w+gap)
        cx = x0+card_w/2
        selected = revealed and value == target
        p.rect((x0, 168, x0+card_w, 469), "#E0DCCB", 24)
        p.rect((x0, 162, x0+card_w, 460), "#FFF3CE" if selected else "#FFFDF7",
               24, "#D2A64C" if selected else "#D7E1D2", 3 if selected else 1.5)
        _choice_art(p, value, cx, 304, card_w, t, action_elapsed if selected else None)
        if labels:
            label = value.replace("color_", "").replace("_", " ").capitalize()
            p.text((cx, 438), label, 21, INK, True)
        if selected:
            p.ellipse((cx-17, 145, cx+17, 179), TEAL)
            p.line([(cx-8,162), (cx-2,168), (cx+9,156)], "#FFFFFF", 3)


def _speech_pointer(p, speaker):
    """Show whose story turn it is; callers never use this before quiz reveal."""
    if speaker not in {"Sunny", "Pip"}:
        return
    x = 268 if speaker == "Sunny" else 1023
    p.rect((x-92, 156, x+92, 198), "#FFFCF3", 17, "#C7D9C5", 2)
    direction = -1 if speaker == "Sunny" else 1
    p.polygon([(x+direction*20,196), (x+direction*40,196), (x+direction*34,211)], "#FFFCF3")
    p.text((x,177), speaker, 20, INK, True)


def _english_strip(p, text, guided=False):
    lines = text_layout(text)
    positions = [550] if len(lines) == 1 else [531, 567]
    for (line, size), y in zip(lines, positions):
        if guided:
            # Word cards are a visual reading aid, not a claim of word-level
            # synchronization. Draw the full sentence once to keep its exact
            # spaces and punctuation, including contractions, intact.
            font = _font(size, True)
            x0 = 640-font.getlength(line)/(2*SCALE)
            offset = 0
            for word in line.split(" "):
                x = x0+font.getlength(line[:offset])/SCALE
                w = font.getlength(word)/SCALE
                p.rect((x-3, y-size*.65, x+w+3, y+size*.67), "#F1F4E7", 6)
                offset += len(word)+1
        p.text((640,y), line, size, INK, True)


def render_frame(episode: dict, scene: dict, t: float, scene_duration: float = 20) -> Image.Image:
    """Render one 1280×720 RGB frame with source-independent quiz waiting."""
    t = max(0.0, float(t))
    mode = str(scene.get("mode", "demo"))
    visual = str(scene.get("visual", scene.get("target", "hello")))
    target = str(scene.get("target", visual))
    choices = scene.get("choices") or []
    for token in [visual, target, *[shared._choice_value(c) for c in choices]]:
        if token not in VALID_VISUALS:
            raise ValueError(f"Unknown elementary visual token: {token!r}")
    reveal_at = float(scene.get("reveal_at", 12))
    demo_start = float(scene.get("demo_start", 5))
    revealed = mode != "quiz" or t >= reveal_at
    image = _background().copy()
    p = Pen(image)
    title = f"{int(episode.get('number', 1)):02d}  /  {episode.get('title_en', 'English Club')}"
    p.text((1210, 61), title, _fit_text(title, 744, 19, 13), INK, False, "rm")
    guided = bool(scene.get("guided_reading")) and revealed and t >= demo_start
    badge = "READ TOGETHER" if guided else {
        "demo": "LISTEN & LEARN", "repeat": "YOUR TURN",
        "review": "LET'S REMEMBER", "quiz": "LISTEN & POINT",
    }.get(mode, "LET'S LEARN")
    p.text((74, 130), badge, 14, "#658978", True, "lm")
    speaker = str(scene.get("story_speaker", "")) if mode != "quiz" else ""
    if choices:
        _draw_choices(p, choices, target, t, revealed=mode == "quiz" and revealed,
                      labels=mode == "review", action_elapsed=t-reveal_at)
    elif mode == "quiz" and not revealed:
        shared._bear(p, 492, 464, 1.04, "neutral", t)
        shared._bird(p, 824, 335, 1.02, t, -1)
    elif visual in NEW_VISUALS:
        if visual in {"sunny", "pip"}:
            draw_object(p, visual, 652, 331, 360, t)
        else:
            shared._bear(p, 260, 460, .87, "neutral", t)
            shared._bird(p, 1048, 279, .66, t, -1)
            draw_object(p, visual, 738, 313, 350, t)
    elif visual in COLORS:
        shared._bear(p, 282, 460, .92, "wave", t)
        shared._bird(p, 1058, 299, .62, t, -1)
        shared._ball(p, 758, 314, 118, COLORS[visual], t)
    elif visual in COUNT_VALUES:
        shared._bear(p, 234, 460, .83, "neutral", t)
        shared._bird(p, 1114, 255, .47, t, -1)
        shared._count(p, visual, 788, 318, 595, t, scene.get("layout", "row"))
    elif visual in {"stand", "sit", "clap", "happy", "sad"}:
        action_start = reveal_at if mode == "quiz" else demo_start
        amount = shared._movement(visual, t-action_start) if visual in {"stand", "sit"} else None
        shared._bear(p, 570, 463, 1.08, visual, t, sit_amount=amount)
        shared._bird(p, 875, 333, .96, t, -1)
    elif visual in {"hello", "goodbye", "wave"}:
        shared._bear(p, 491, 463, 1.08, visual, t)
        drift = min(t/max(1,scene_duration),1)*76 if visual == "goodbye" else 0
        shared._bird(p, 844+drift, 322-.2*drift, 1.02, t, 1 if visual == "goodbye" else -1)
    else:
        shared._bear(p, 256, 460, .88, "neutral", t)
        shared._bird(p, 1080, 282, .55, t, -1)
        draw_object(p, visual, 770, 308, 405, t)
    if speaker:
        _speech_pointer(p, speaker)
    if t < demo_start and scene.get("instruction", {}).get("en"):
        text = str(scene["instruction"]["en"])
    elif mode == "quiz":
        text = str(scene.get("demo", scene.get("english", "Well done!"))) if revealed else "Listen and point."
    else:
        text = str(scene.get("english", scene.get("demo", "Hello!")))
    _english_strip(p, text, guided=guided)
    if mode == "repeat" or (mode == "quiz" and not revealed):
        phase = int(t*.65) % 3
        for i in range(3):
            cx = 625+i*15
            p.ellipse((cx-3, 599, cx+3, 605), TEAL if phase == i else "#D8E5D3")
    else:
        p.line([(602, 602), (678, 602)], "#E4CB8F", 3)
    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
