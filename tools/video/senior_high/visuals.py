"""Slate-and-petrol English Lab notebook for all six senior-high seasons.

English remains fixed in the picture; y=630–719 is plain translated-CC space.
Quiz frames before reveal depend only on the options and neutral common prompt.
Reading aids are backgrounds, never word-timing or grammar-answer claims.
"""
from __future__ import annotations

from functools import lru_cache

from PIL import Image, ImageDraw

from elementary.shared import preschool_visuals as shared
from senior_high.objects import INK, TEAL, VALID_VISUALS, draw_object, parse_token, positioned_text

WIDTH, HEIGHT, SCALE = shared.WIDTH, shared.HEIGHT, shared.SCALE
Pen = shared.Pen
PAPER, WHITE, NAVY = "#F0EEE7", "#FEFCF6", "#26333F"
MUTED, LINE, LIGHT_TEAL = "#6D7B80", "#D8DFDF", "#E6EEEF"


@lru_cache(maxsize=1)
def _background():
    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), PAPER)
    p = Pen(image)
    p.rect((0, 0, WIDTH, 99), NAVY)
    p.rect((42, 30, 82, 70), "#527581", 10)
    # An original small open-book mark replaces oversized preschool figures.
    p.polygon([(50, 40), (61, 44), (61, 62), (50, 58)], "#EEF1ED")
    p.polygon([(74, 40), (63, 44), (63, 62), (74, 58)], "#C4D4D8")
    p.line([(62, 44), (62, 63)], "#FFFFFF", 1)
    p.text((99, 45), "ENGLISH LAB", 24, "#FFFFFF", True, "lm")
    p.text((100, 72), "SUNNY & PIP  /  SENIOR HIGH", 11, "#CED8DB", False, "lm")
    p.line([(42, 479), (1238, 479)], "#D4DBDB", 1)
    p.rect((30, 493, 1250, 620), WHITE, 14)
    p.rect((30, 506, 34, 607), TEAL, 2)
    # The subtitle reserve has no illustrations, ruling or learning text.
    p.rect((0, 630, WIDTH, HEIGHT), PAPER)
    return image


def _fit_text(text, width, initial_size=21, minimum=14):
    for size in range(initial_size, minimum - 1, -1):
        if shared._font(size, True).getlength(text) <= width * SCALE:
            return size
    raise ValueError(f"Senior-high heading does not fit: {text!r}")


def english_strip_layout(text):
    """Keep actual glyphs inside y=507–589, leaving response dots at y=599."""
    return positioned_text(str(text), 1100, 548, 42, 26, 3, 82, 9)


def _english_strip(p, text, guided=False):
    positioned = english_strip_layout(text)
    if guided:
        # Draw EVERY word background before ANY glyph. A later line can never
        # paint over the descenders above, even if font metrics change.
        for line, size, y in positioned:
            font = shared._font(size, True)
            box = font.getbbox(line, anchor="mm")
            left = 640 - font.getlength(line) / (2 * SCALE)
            offset = 0
            for word in line.split(" "):
                x = left + font.getlength(line[:offset]) / SCALE
                width = font.getlength(word) / SCALE
                p.rect((x - 3, y + box[1] / SCALE - 3,
                        x + width + 3, y + box[3] / SCALE + 3), LIGHT_TEAL, 4)
                offset += len(word) + 1
    for line, size, y in positioned:
        p.text((640, y), line, size, INK, True)


def _notebook(p, visual, t):
    # A desk notebook with quiet ruled margins keeps the sentence the focus.
    p.rect((70, 173, 1143, 466), "#D9DEDD", 10)
    p.rect((64, 164, 1137, 457), WHITE, 10, "#CED7D9", 1.5)
    p.line([(139, 164), (139, 457)], "#BCAD97", 1.5)
    for y in (200, 243, 378, 423):
        p.line([(149, y), (1107, y)], "#E9EEEE", 1)
    for y in (201, 271, 341, 411):
        p.ellipse((87, y - 5, 97, y + 5), "#DCE3E2")
        p.arc((56, y - 8, 96, y + 8), 160, 375, "#899EA2", 2)
    p.text((165, 193), "TEXT EXAMPLE", 12, MUTED, True, "lm")
    kind, _ = parse_token(visual)
    if kind in {"sentence", "word"}:
        draw_object(p, visual, 635, 317, 918, t)
    else:
        draw_object(p, visual, 635, 319, 300, t)
    # A slim mechanical pencil and memo tab, no answer-bearing decoration.
    p.rect((1173, 200, 1190, 406), "#405764", 4)
    p.rect((1176, 211, 1180, 392), "#73939C", 2)
    p.rect((1173, 195, 1190, 213), "#BCC6C9", 3)
    p.polygon([(1173, 405), (1190, 405), (1181.5, 426)], "#C8AE8A")
    p.polygon([(1178, 418), (1185, 418), (1181.5, 429)], INK)
    p.rect((1150, 442, 1214, 449), "#C8B58A", 3)


def _draw_choices(p, choices, target, t, revealed=False, action_elapsed=None):
    values = [shared._choice_value(item) for item in choices]
    if not 2 <= len(values) <= 3:
        raise ValueError("Senior-high choices require two or three options")
    if len(set(values)) != len(values):
        raise ValueError("Senior-high choices must be distinct")
    left, right, gap = 64, 1216, 22
    card_width = (right - left - gap * (len(values) - 1)) / len(values)
    for index, value in enumerate(values):
        x0 = left + index * (card_width + gap)
        x = x0 + card_width / 2
        selected = revealed and value == target
        p.rect((x0 + 3, 175, x0 + card_width + 3, 466), "#D9DEDD", 10)
        p.rect((x0, 167, x0 + card_width, 458),
               "#E7EFF0" if selected else WHITE, 10,
               TEAL if selected else "#CED7D9", 3 if selected else 1.5)
        p.rect((x0 + 19, 183, x0 + 51, 215), TEAL if selected else "#ECEFEC", 7)
        p.text((x0 + 35, 199), chr(65 + index), 17, "#FFFFFF" if selected else INK, True)
        p.line([(x0 + 19, 230), (x0 + card_width - 19, 230)], "#DFE5E3", 1)
        # Inherited object helpers have their own vertical dimensions. Limit
        # their width separately from sentence cards so clocks/count trays stay
        # below the option header and above the card's bottom edge.
        kind, _ = parse_token(value)
        art_width = card_width - 38 if kind in {"word", "sentence"} else min(240, card_width - 38)
        art_y = 347 if kind == "day" else 339  # Calendar binding rings rise above its page.
        draw_object(p, value, x, art_y, art_width, t, max_height=192,
                    action_elapsed=action_elapsed if selected else None)
        if selected:
            p.ellipse((x0 + card_width - 49, 184, x0 + card_width - 21, 212), TEAL)
            p.line([(x0 + card_width - 43, 198), (x0 + card_width - 37, 203),
                    (x0 + card_width - 28, 192)], "#FFFFFF", 2.5)


def _scene_canvas(episode_fields, mode, visual, target, values, revealed, guided,
                  text, t=0, action_elapsed=None):
    """Paint a semantic phase once; the caller adds only time-dependent motion."""
    image = _background().copy()
    p = Pen(image)
    number, title_en, season, grade = episode_fields
    title = f"{number:02d}  /  {title_en}"
    p.text((1237, 47), title, _fit_text(title, 804), "#FFFFFF", True, "rm")
    p.text((1237, 74), f"SEASON {season:02d}  /  GRADE {grade}",
           11, "#CED8DB", False, "rm")
    badge = "READ ALOUD" if guided else {
        "demo": "LISTEN & NOTICE", "repeat": "PRACTICE", "review": "PUT IT TOGETHER",
        "quiz": "LISTEN & CHOOSE",
    }.get(mode, "LISTEN & NOTICE")
    p.text((65, 131), badge, 14, TEAL, True, "lm")
    p.line([(1019, 131), (1215, 131)], "#D3DCDE", 3)
    if values:
        _draw_choices(p, values, target, t, mode == "quiz" and revealed, action_elapsed)
    else:
        _notebook(p, visual, t)
    _english_strip(p, text, guided)
    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


@lru_cache(maxsize=16)
def _static_canvas(episode_fields, mode, visual, target, values, revealed, guided, text):
    # Sixteen native RGB frames consume at most ~43 MiB. Every text and reveal
    # state is in the key; reused scenes cannot inherit another scene's answer.
    return _scene_canvas(episode_fields, mode, visual, target, values, revealed, guided, text)


def render_frame(episode: dict, scene: dict, t: float, scene_duration: float = 20) -> Image.Image:
    """Return one 1280×720 frame, validating tokens and every rendered text box."""
    t = max(0.0, float(t))
    mode = str(scene.get("mode", "demo"))
    visual = str(scene.get("visual", scene.get("target", "hello")))
    target = str(scene.get("target", visual))
    values = tuple(shared._choice_value(item) for item in scene.get("choices", []))
    kinds = [parse_token(token)[0] for token in [visual, target, *values]]
    if mode == "quiz" and (not values or target not in values):
        raise ValueError("A senior-high quiz requires its target among two or three choices")
    reveal_at = float(scene.get("reveal_at", 12))
    demo_start = float(scene.get("demo_start", 5))
    revealed = mode != "quiz" or t >= reveal_at
    guided = bool(scene.get("guided_reading")) and revealed and t >= demo_start
    if mode == "quiz":
        text = str(scene.get("demo", "Well done!")) if revealed else "Listen and choose."
    elif t < demo_start and scene.get("instruction", {}).get("en"):
        text = str(scene["instruction"]["en"])
    else:
        text = str(scene.get("english", scene.get("demo", "Hello!")))
    episode_fields = (int(episode.get("number", 1)), episode.get("title_en", "English Lab"),
                      int(episode.get("season", 1)), int(episode.get("grade", 10)))
    arguments = (episode_fields, mode, visual, target, values, revealed, guided, text)
    if all(kind in {"word", "sentence", "number", "count", "clock", "day"} for kind in kinds):
        image = _static_canvas(*arguments).copy()
    else:
        image = _scene_canvas(*arguments, t, t - reveal_at)
    # Native-size motion avoids repainting/resampling unchanged glyphs on every
    # video frame. The progress bar describes elapsed scene time, not speech.
    d = ImageDraw.Draw(image)
    fraction = min(1.0, t / max(1.0, scene_duration))
    end = round(1019 + 196 * fraction)
    d.line([(1019, 131), (end, 131)], TEAL, 3)
    d.ellipse((end - 3, 128, end + 3, 134), TEAL)
    if mode == "repeat" or (mode == "quiz" and not revealed):
        phase = int(t * .65) % 3
        for index in range(3):
            center = 625 + index * 15
            d.ellipse((center - 3, 599, center + 3, 605),
                      TEAL if phase == index else "#D2DDDF")
    else:
        d.line([(614, 602), (666, 602)], "#BCCFD2", 2)
    return image
