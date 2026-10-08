"""Original classroom props extending the shared Sunny & Pip artwork.

The four new identifiers draw pictures without printed labels. Shared preschool
assets stay in their own modules, so extending this course cannot change them.
"""

from __future__ import annotations

import math

from elementary.shared import preschool_objects as shared_objects
from elementary.shared import preschool_visuals as shared_visuals

NEW_VISUALS = frozenset({"sunny", "pip", "book", "pencil"})
VALID_VISUALS = shared_visuals.VALID_VISUALS | NEW_VISUALS


def draw_object(p, token, x, y, width, t=0, **kwargs):
    """Draw a picture centered on x/y, using the shared Pen coordinates."""
    if token in shared_objects.NEW_VISUALS:
        return shared_objects.draw_object(p, token, x, y, width, t, **kwargs)
    width = max(32, float(width))
    scale = width / 320
    if token == "sunny":
        shared_visuals._bear(p, x, y + 116 * scale, .92 * scale, "wave", t)
    elif token == "pip":
        shared_visuals._bird(p, x, y, 1.6 * scale, t)
    elif token == "book":
        # A single closed hardback with a visible spine and page block. The
        # cover is deliberately blank: the illustration cannot reveal a word.
        p.ellipse((x - 100*scale, y + 88*scale, x + 100*scale, y + 106*scale), "#DFE4D5")
        p.rect((x - 89*scale, y - 98*scale, x + 88*scale, y + 98*scale), "#667FA9", 8*scale, "#566C93", 2*scale)
        p.rect((x - 72*scale, y - 84*scale, x + 79*scale, y + 89*scale), "#FFFBEE", 4*scale, "#DAD5C7", 1.5*scale)
        for offset in (74, 80, 85):
            p.line([(x - 59*scale, y + offset*scale), (x + 74*scale, y + offset*scale)], "#DAD5C7", scale)
        p.rect((x - 90*scale, y - 105*scale, x + 84*scale, y + 74*scale), "#89ACC9", 7*scale, "#637C9C", 2*scale)
        p.line([(x - 66*scale, y - 102*scale), (x - 66*scale, y + 72*scale)], "#6388AA", 3*scale)
        p.rect((x - 47*scale, y - 78*scale, x + 60*scale, y + 48*scale), None, 3*scale, "#BBD4E2", 2*scale)
        p.polygon([(x + 39*scale, y + 80*scale), (x + 53*scale, y + 80*scale),
                   (x + 53*scale, y + 114*scale), (x + 46*scale, y + 107*scale),
                   (x + 39*scale, y + 114*scale)], "#E2A38E")
    elif token == "pencil":
        # One large diagonal pencil: eraser, metal ferrule, wooden tip and
        # graphite are separate shapes, with no printed letters on the shaft.
        p.ellipse((x - 96*scale, y + 77*scale, x + 107*scale, y + 98*scale), "#DFE4D5")
        angle = -.63
        def point(px, py):
            return (x + (px*math.cos(angle) - py*math.sin(angle))*scale,
                    y + (px*math.sin(angle) + py*math.cos(angle))*scale)
        def box_poly(a, b, c, d, color):
            p.polygon([point(a,b), point(c,b), point(c,d), point(a,d)], color)
        box_poly(-102,-20,81,20,"#D1A453")
        box_poly(-100,-17,81,-4,"#F5D987")
        box_poly(-100,-4,81,11,"#EDC15E")
        box_poly(-100,11,81,18,"#DBAD4D")
        box_poly(-119,-20,-98,20,"#D9B1B0")
        box_poly(-111,-20,-89,20,"#CED5D2")
        for offset in (-106, -99, -92):
            p.line([point(offset,-18),point(offset,18)], "#A9B4B0", 1.5*scale)
        p.polygon([point(80,-20),point(127,0),point(80,20)], "#E7C59D")
        p.polygon([point(111,-7),point(128,0),point(111,7)], "#525B56")
    else:
        raise ValueError(f"Unknown elementary object: {token!r}")
