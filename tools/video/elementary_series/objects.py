"""Original elementary props and explicit, validated English learning cards.

Dynamic tokens are a small grammar, not a fallback for unknown artwork. The
same cookie geometry is used for every count at a given card width. Clock hands
use the displayed hour and minute, including the hour hand's minute offset.
"""
from __future__ import annotations

import math
import re
from functools import lru_cache

from elementary.objects import VALID_VISUALS as LEGACY_VISUALS
from elementary.objects import draw_object as legacy_object
from elementary.shared import preschool_visuals as shared

VALID_VISUALS = LEGACY_VISUALS
DAYS = frozenset("Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split())
PLACES = frozenset({"home", "school", "park", "library", "shop"})
INK, TEAL = "#3F514B", "#5B9E8C"


def parse_token(token: str) -> tuple[str, str]:
    """Validate a legacy identifier or one of the documented dynamic tokens."""
    if not isinstance(token, str):
        raise ValueError(f"Visual token must be a string: {token!r}")
    if token in LEGACY_VISUALS:
        return "legacy", token
    kind, separator, value = token.partition(":")
    valid = False
    if separator and kind in {"word", "sentence"}:
        valid = (bool(value.strip()) and value == value.strip() and len(value) <= 54
                 and all(32 <= ord(character) < 127 for character in value))
    elif separator and kind in {"number", "count"}:
        valid = bool(re.fullmatch(r"[1-9][0-9]*", value)) and 1 <= int(value) <= (100 if kind == "number" else 20)
    elif separator and kind == "clock":
        match = re.fullmatch(r"([01]?[0-9]|2[0-3]):([0-5][0-9])", value)
        valid = bool(match)
    elif separator and kind == "day":
        valid = value in DAYS
    elif separator and kind == "place":
        valid = value in PLACES
    if not valid:
        raise ValueError(f"Unknown elementary-series visual token: {token!r}")
    return kind, value


@lru_cache(maxsize=2048)
def text_layout(text: str, max_width: float, initial_size: int = 40,
                minimum: int = 22, max_lines: int = 3) -> list[tuple[str, int]]:
    """Fit whole words while retaining punctuation and spaces within each line."""
    text = str(text)
    if not text or "\n" in text or "\r" in text:
        raise ValueError(f"English picture text must be one nonempty paragraph: {text!r}")
    for size in range(initial_size, minimum - 1, -1):
        font = shared._font(size, True)
        lines, current = [], ""
        for word in text.split(" "):
            candidate = current + " " + word if current else word
            if current and font.getlength(candidate) > max_width * shared.SCALE:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        if (len(lines) <= max_lines
                and all(font.getlength(line) <= max_width * shared.SCALE for line in lines)):
            return [(line, size) for line in lines]
    raise ValueError(f"English picture text does not fit {max_lines} readable lines: {text!r}")


def _text(p, value, x, y, width, initial_size=40, minimum=22, max_lines=3):
    lines = text_layout(value, width, initial_size, minimum, max_lines)
    step = lines[0][1] * 1.42
    for index, (line, size) in enumerate(lines):
        p.text((x, y + (index - (len(lines)-1)/2) * step), line, size, INK, True)


@lru_cache(maxsize=128)
def cookie_layout(count: int, width: float) -> tuple[float, list[tuple[float, float]]]:
    """Five-column rows; count never changes cookie radius or spacing."""
    if not 1 <= count <= 20:
        raise ValueError("A count card needs one to twenty cookies")
    radius = min(24.0, width / 13.5)
    step = radius * 2.6
    rows = math.ceil(count/5)
    points = []
    for row in range(rows):
        columns = min(5, count - row*5)
        points.extend(((column-(columns-1)/2)*step, (row-(rows-1)/2)*step)
                      for column in range(columns))
    return radius, points


def _cookies(p, count, x, y, width):
    radius, points = cookie_layout(count, width)
    # A fixed tray means its silhouette cannot encode the answer differently
    # from the visible objects, and every option keeps equally sized cookies.
    half_width = radius * 6.5
    half_height = radius * 5.2
    p.rect((x-half_width, y-half_height, x+half_width, y+half_height),
           "#F4EEE0", 15, "#D6CCB7", 2)
    for dx, dy in points:
        cx, cy = x+dx, y+dy
        p.ellipse((cx-radius, cy-radius+2, cx+radius, cy+radius+2), "#C7A873")
        p.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), "#EBC589", "#CFA36E", 1.5)
        for dot_x, dot_y in ((-.34,-.35),(.31,-.31),(.38,.30),(-.28,.38),(0,.03)):
            dot_radius = radius*.10
            p.ellipse((cx+dot_x*radius-dot_radius, cy+dot_y*radius-dot_radius,
                       cx+dot_x*radius+dot_radius, cy+dot_y*radius+dot_radius), "#805844")


@lru_cache(maxsize=128)
def clock_angles(value: str) -> tuple[float, float]:
    """Radians from the rightward axis, with twelve o'clock pointing up."""
    parse_token("clock:"+value)
    hour, minute = map(int, value.split(":"))
    return ((hour % 12 + minute/60) * math.tau/12 - math.pi/2,
            minute * math.tau/60 - math.pi/2)


def _clock(p, value, x, y, width):
    radius = min(96, width*.33)
    cy = y-17
    p.ellipse((x-radius-7,cy-radius-7,x+radius+7,cy+radius+7), "#E1BF83")
    p.ellipse((x-radius,cy-radius,x+radius,cy+radius), "#FFFDF5", "#C7B28C", 2)
    for hour in range(1,13):
        angle = hour*math.tau/12-math.pi/2
        p.text((x+radius*.79*math.cos(angle), cy+radius*.79*math.sin(angle)),
               str(hour), max(12,round(radius*.16)), INK, True)
    hour_angle, minute_angle = clock_angles(value)
    p.line([(x,cy), (x+radius*.48*math.cos(hour_angle),cy+radius*.48*math.sin(hour_angle))],
           "#4C766B", max(4,radius*.055))
    p.line([(x,cy), (x+radius*.65*math.cos(minute_angle),cy+radius*.65*math.sin(minute_angle))],
           "#5C7397", max(3,radius*.035))
    p.ellipse((x-5,cy-5,x+5,cy+5), INK)
    p.rect((x-65,cy+radius+10,x+65,cy+radius+49), "#EDF2E8", 9)
    p.text((x,cy+radius+30), value, 24, INK, True)


def _calendar(p, value, x, y, width):
    card_width = min(width*.91, 340)
    p.rect((x-card_width/2,y-102,x+card_width/2,y+91), "#FFFDF4", 14, "#D1D8C9", 2)
    p.rect((x-card_width/2,y-102,x+card_width/2,y-48), "#94B8A4", 14)
    p.rect((x-card_width/2,y-78,x+card_width/2,y-48), "#94B8A4")
    for dx in (-card_width*.25, card_width*.25):
        p.rect((x+dx-5,y-113,x+dx+5,y-82), "#718875", 4)
    _text(p, value, x, y+10, card_width-20, 34, 20, 1)
    p.line([(x-card_width*.32,y+56),(x+card_width*.32,y+56)], "#E5DDC9", 2)


def _place(p, value, x, y, width, t):
    """Five original silhouettes, with no printed answer labels."""
    scale = min(width, 350)/320
    def box(a,b,c,d):
        return (x+a*scale,y+b*scale,x+c*scale,y+d*scale)
    def points(items):
        return [(x+a*scale,y+b*scale) for a,b in items]
    p.ellipse(box(-130,99,130,117), "#DBE4D4")
    if value == "park":
        for tx, ty, shade in ((-91,-32,"#92B793"),(96,-45,"#ADC69A")):
            p.rect(box(tx-9,ty,tx+9,105), "#B09067", 5*scale)
            sway = math.sin(t*1.8)*2
            p.ellipse(box(tx-42+sway,ty-57,tx+42+sway,ty+29), shade)
        p.rect(box(-67,25,67,41), "#BE9970", 4*scale)
        p.rect(box(-67,50,67,63), "#CFA77C", 4*scale)
        p.rect(box(-61,62,-51,103), "#788A75", 2*scale)
        p.rect(box(51,62,61,103), "#788A75", 2*scale)
        p.rect(box(-64,13,-56,60), "#788A75", 2*scale)
        p.rect(box(56,13,64,60), "#788A75", 2*scale)
        return
    if value == "home":
        p.rect(box(48,-95,72,-36), "#B7816D", 2*scale)
        p.polygon(points([(-126,-30),(0,-119),(126,-30)]), "#C78974")
        p.rect(box(-102,-30,102,107), "#F1D7AD", 3*scale)
        p.rect(box(-21,31,25,107), "#95AE9D", 4*scale)
        p.ellipse(box(11,66,16,71), "#5D776A")
        for left in (-81,43):
            p.rect(box(left,-11,left+41,32), "#DEEBE6", 2*scale, "#A49075", 2*scale)
            p.line(points([(left+20,-10),(left+20,31)]), "#A49075", 2*scale)
            p.line(points([(left,10),(left+40,10)]), "#A49075", 2*scale)
    elif value == "school":
        p.rect(box(-123,-34,123,107), "#E7C29D", 4*scale)
        p.rect(box(-37,-85,37,107), "#F6DCB5", 3*scale)
        p.polygon(points([(-49,-85),(0,-120),(49,-85)]), "#A6B8AF")
        p.ellipse(box(-19,-70,19,-32), "#FFF7E3", "#B7A180", 2*scale)
        p.line(points([(0,-61),(0,-51),(10,-51)]), INK, 2*scale)
        p.rect(box(-23,44,23,107), "#83A7A1", 4*scale)
        for left in (-105,-73,55,87):
            p.rect(box(left,-16,left+19,20), "#DCEBEC", 2*scale, "#B5A68C", scale)
        p.line(points([(91,-82),(91,-33)]), "#899483", 3*scale)
        flutter = math.sin(t*2)*3
        p.polygon(points([(93,-82),(124,-73+flutter),(93,-63)]), "#BBA2BC")
    elif value == "library":
        p.rect(box(-126,-51,126,106), "#E7DBC2", 3*scale)
        p.polygon(points([(-139,-51),(0,-118),(139,-51)]), "#9FAEBA")
        for left in (-111,-65,46,92):
            p.rect(box(left,-38,left+18,90), "#FFF9E9", 2*scale, "#CFC3A7", scale)
        p.rect(box(-33,22,33,106), "#829FA9", 3*scale)
        # An open-book pediment identifies the library without text.
        p.polygon(points([(-39,-83),(-8,-77),(0,-69),(0,-48),(-38,-58)]), "#FFF8E9")
        p.polygon(points([(39,-83),(8,-77),(0,-69),(0,-48),(38,-58)]), "#F0E7D4")
        p.line(points([(0,-69),(0,-49)]), "#9EAAAD", 2*scale)
    elif value == "shop":
        p.rect(box(-117,-64,117,107), "#E6D5B8", 4*scale)
        p.rect(box(-100,-8,-5,84), "#DEE8DF", 2*scale, "#AEAA92", 2*scale)
        p.rect(box(27,-8,96,107), "#98B1AA", 3*scale)
        p.rect(box(40,5,83,62), "#DFECE3", 2*scale)
        for i in range(6):
            left = -126+i*42
            p.polygon(points([(left+6,-75),(left+36,-75),(left+42,-27),(left,-27)]),
                      "#CD9888" if i%2 == 0 else "#FFF3DA")
            p.ellipse(box(left,-38,left+42,-15), "#CD9888" if i%2 == 0 else "#FFF3DA")
        p.rect(box(-71,36,-29,73), "#E3C387", 4*scale)
        p.arc(box(-62,18,-38,48),180,360,"#AB946D",3*scale)
    else:
        raise ValueError(f"Unknown place: {value!r}")


def draw_object(p, token, x, y, width, t=0, **kwargs):
    kind, value = parse_token(token)
    width = max(32, float(width))
    if kind == "legacy":
        return legacy_object(p, value, x, y, width, t, **kwargs)
    if kind in {"word", "sentence"}:
        _text(p, value, x, y, width-20,
              initial_size=50 if kind == "word" else 38, minimum=22)
    elif kind == "number":
        _text(p, value, x, y, width-20, 98, 36, 1)
    elif kind == "count":
        _cookies(p, int(value), x, y, width-12)
    elif kind == "clock":
        _clock(p, value, x, y, width)
    elif kind == "day":
        _calendar(p, value, x, y, width)
    elif kind == "place":
        _place(p, value, x, y, width, t)
    else:
        raise ValueError(f"Unsupported elementary card: {token!r}")
