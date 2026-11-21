#!/usr/bin/env python3
"""Till the Verdict: redraws after the 2026-11-12 reference audit (../review/2026-11-12-ref-audit-e001-e020.md).

  redraw.py --list                       rounds, images, CU
  redraw.py s7|s8|a5 [--work DIR]        write <work>/<round>.json
  redraw.py s7 s8 a5 --into s4 [--work]  write the three rounds as one manifest (<work>/s4.json), so a chain that is already
                                         waiting for s4.json runs them on the machine it has open

Twenty read-only agents compared the storyboards of episodes 1-20 with the pictures picked from art.py's a12, s1-s3 and
p1. Most set pictures broke the layout their own prompt asked for (a two-storey living room, a greenhouse nursery, a motel
room with no entry door, a hospital bed against the wall with an IV bag hanging, the sea and the sun outside the land-side
front door), and the bedroom has no picture of its north half at all. These rounds redraw the sets episodes 1-10 need, with
the layout spelled out where the model went wrong, and fix three people. Sets are new pictures on a grey canvas (latent
empty, vertical 1088x1920, two seeds); people are one-change edits (latent image1) of the picked picture in ../assets/refs.
Standard library only; run with python3 -I.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import art  # noqa: E402  (work_dir, copy_ref, SET_NEW, FIX, CANVAS, SETV, BUST, FULLV, CU_PER_IMAGE)
import build  # noqa: E402

NOBODY = "Nobody is in the frame; nothing written anywhere."
HOUSE = "a modern single-storey glass house on a grassy bluff above grey Puget Sound water"

# (id, plan set number it replaces or "new", prompt)
SETS = {
    "s7": [
        ("bed-north-sconce", "new (north half of #2)",
         "a tall vertical view of a minimal bedroom in a modern glass house, seen from beside the head of the bed looking toward the foot of the bed "
         "and the bedroom door: on the LEFT of the frame one floor-to-ceiling glass wall from floor to ceiling, black at night with rain streaks "
         "running down it; the low bed with white sheets and a thin grey blanket running away from the camera along the glass; in the far RIGHT "
         "corner a plain white bedroom door standing half open into the room, a camel wool coat hanging on a hook on the inside of the door, beyond "
         "it a dim hallway with a low warm-yellow night light near the floor; plain white walls, a pale grey floor, no mirror. Light: night; warm "
         f"white light from a small wall lamp just behind the camera falls across the bed; the glass is black. {NOBODY}"),
        ("liv-gold-a", "#21",
         "a tall vertical view inside a single-storey glass-walled modern house on a bluff, looking from the entry toward the sea: a flat white "
         "ceiling just above the top of the glass, no staircase, no upper floor, no balcony, nothing outside the glass but sea and sky; pale oak "
         "floor, a low grey sofa on the left of the frame, a long pale wood dining table on the right of the frame, a row of low pale oak cabinets "
         "under the floor-to-ceiling glass wall facing the sea at the back with a white porcelain vase on their left end; heavy opaque "
         "charcoal-grey curtains, thick matte fabric, already hung from ceiling to floor over the glass at the dining-table end on the right, that "
         "half of the room dim; two short grey two-step ladders standing indoors on the oak floor in front of the bare glass behind the sofa. "
         f"Light: low golden sunset light pouring in through the uncurtained sea-side glass on the left across the floor. {NOBODY}"),
        ("liv-east-gold", "new (reverse of #21)",
         "a tall vertical view inside a single-storey glass-walled modern house, looking from the sea-side glass toward the entry: a flat white "
         "ceiling, pale oak floor, the long pale wood dining table on the LEFT of the frame, the low grey sofa on the RIGHT with its back to the "
         "camera, heavy opaque charcoal-grey curtains closed over the glass at the table end on the left, that corner dim; the glass wall on the "
         "entry side bare, and through it a gravel forecourt and a drive curving down a gold grassy bluff, no sea ahead. Light: one wide beam of "
         f"low red-gold sunset light from behind the camera across the floor and the sofa back. {NOBODY}"),
        ("door-in-day", "#7",
         f"a tall vertical view from inside the pale oak entry of {HOUSE}, toward its front door: the pale oak entry floor in the foreground, "
         "a tall black steel-framed glass front door, closed, hinged on its left, an ordinary black lever handle on its right edge, plain glass "
         "walls on both sides of it; OUTSIDE beyond the glass a plain doormat, two wide grey stone steps down to a gravel forecourt, one tall slim "
         "modern black lamppost standing on the grass just left of the steps, unlit, the gravel drive curving away down the bluff to the lower "
         "right, grass and dark firs; no sea and no other building outside the door. Light: grey overcast afternoon, drizzle, raindrops on the "
         f"glass, cool blue inside, no lamps on. {NOBODY}"),
        ("door-in-gold", "#24",
         f"a tall vertical view from inside the pale oak entry of {HOUSE}, toward its front door: the pale oak entry floor in the foreground, "
         "the tall black steel-framed glass front door standing open, swung inward against the wall on the left, a brand-new brushed-steel "
         "deadbolt and lever handle on the black steel door frame, bright and unscratched, plain glass walls on both sides; OUTSIDE a plain "
         "doormat, two wide grey stone steps down to a gravel forecourt, one tall slim modern black lamppost on the grass just left of the steps, "
         "unlit, the gravel drive curving away down the bluff to the lower right, grass and dark firs; no sea, no sun and no other building "
         "outside the door. Light: low sunset light from behind the camera (the sea side) through the whole house, the forecourt and the drive "
         f"outside glowing gold-orange. {NOBODY}"),
        ("nur-day", "#9",
         "a tall vertical view from the doorway of a small half-finished nursery in a modern glass house: a flat plain white ceiling with one "
         "plain round white ceiling light, switched off; solid plain white side walls; a white crib on the left of the frame, a wooden rocking "
         "chair on the right with a small empty knitting basket on its seat; the whole far wall one single floor-to-ceiling window in a slim black "
         "steel frame, plain glass from floor to ceiling and wall to wall onto the grey sea, no glass roof, no small panes, no low wall and no "
         f"sill; pale oak floor. Light: soft cold blue overcast afternoon, drizzle on the glass. {NOBODY}"),
    ],
    "s8": [
        ("room-night", "#16",
         "a tall vertical view of a quiet single hospital room: the head of an adjustable hospital bed with low silver side rails and its back "
         "section raised stands against the LEFT wall, the bed reaching out into the room toward the right, open floor on both long sides of "
         "the bed; plain white sheets and a plain white pillow, no print; a small nightstand beside the bed at mattress height with a clear "
         "plastic cup; on the RIGHT wall a window with closed blinds and a plain chair under it; an empty IV stand with nothing hanging from it "
         "against the left wall behind the bed head; the open door in the right wall at the foot end of the bed, the pale hallway through it; "
         "plain pale grey walls, a plain headwall with no outlets, stickers or buttons, no signs anywhere. Light: night; the blinds are black; "
         f"one small warm white lamp on the nightstand; cold white light from the hallway slanting in through the open door. {NOBODY}"),
        ("hall", "#15",
         "a tall vertical view down a long windowless hospital corridor, from the corridor floor a few steps out of the elevator (no elevator "
         "in view): pale green-grey walls, a row of closed doors with plain blank panels and no signs beside them, linoleum floor, white "
         "fluorescent ceiling lights, a nurses' station counter halfway along on the right, and at the far end a blank pale green-grey wall with "
         "no door in it, one ceiling light just above it and a long wooden bench against the left wall right under that light, no signs, no "
         "number displays. Light: only the white fluorescent ceiling lights; the last light above the blank end wall is dimmer than the others. "
         f"{NOBODY}"),
        ("gcar-day", "#19",
         "a tall vertical view of the back seat of a pearl-white full-size four-door luxury sedan (not a limousine), seen from the dashboard between the two empty front seats "
         "looking back: one single row of cream leather rear seats, the rear window right behind their headrests, a wide centre armrest console "
         "with a closed plain lid between the two seats, a plain roof lining with no sunroof, tinted side windows, no screens, no badges, logos "
         "or emblems anywhere, the top of the steering wheel at the lower right corner. Light: grey overcast noon through the tinted windows; "
         f"blurred grey sea outside the right window and dark firs outside the left. {NOBODY}"),
        ("mroom-night", "#32",
         "a tall vertical view of a modest old roadside motel room seen from the foot of the beds, looking up the narrow aisle between them: two "
         "twin beds side by side, the left bed under two faded floral quilts, the right bed under one thin plain pale blanket, their dark wooden headboards against the far wall, a nightstand between the "
         "headboards with a small bedside lamp with a pale yellow shade at the top centre of the frame; on the LEFT wall the entry door near the "
         "camera and a window with heavy curtains drawn almost closed, one narrow vertical gap between them, a small table and two chairs under "
         "the window; on the RIGHT wall near the far end the bathroom door, closed, plain, no sign on it; dark green carpet, cream walls, no "
         "mirror in view, no readable letters. Light: night; the bedside lamp is the only lamp, warm; a thin red neon glow through the curtain "
         f"gap falls on the left bed; nothing outside the window can be seen. {NOBODY}"),
        ("drive-foot", "new (#28 bottom)",
         "a tall vertical view of the gravel shoulder of a two-lane coast road at the foot of a grassy bluff, seen from the shoulder on the land "
         "side: the coast road running off to the left of the frame along grey Puget Sound water, a narrow asphalt drive climbing to the right "
         "up the grassy bluff, a low wooden guardrail, wind-bent grass and dark firs, a modern single-storey glass house small at the top right "
         "against the sky. Light: low red-gold sunset light from the upper right, the sun itself hidden behind the bluff, the sea on the left in shadow-gold, the asphalt a little damp. Nobody is in the frame; no cars; "
         "nothing written anywhere."),
    ],
}
# (id, refs file in ../assets/refs, size, what stays, the one change)
PEOPLE = [
    ("nurse-kim-fix", "nurse-kim-portrait.jpg", art.BUST, "the face, hair, scrubs, framing, the plain grey backdrop and the lighting",
     "her mouth corners level and relaxed, lips together, no smile."),
    ("grant-rain-fix", "grant-portrait.jpg", art.BUST, "the face, the expression, the suit and shirt, the framing, the plain grey backdrop and the lighting",
     "his sandy-blond hair is darker and damp from rain with a few strands loose, a light fog and fine water drops are on the lenses of his "
     "glasses, and his shirt collar is damp."),
    ("nora-discharge-coat", "nora-discharge.jpg", art.FULLV,
     "the face, hair, the cream sweater dress, the slippers, the pose, the framing, the plain grey backdrop and the lighting",
     "she wears a camel wool coat with deep pockets, worn open, over the dress."),
]
# p4: p2 drew both cars as stretch limousines and put a stranger's face over the tote; same plan sentences, the shape spelled out.
SEDAN = ("a modern four-door luxury sedan of ordinary length, not a limousine and not stretched: two side windows on each side, "
         "a long bonnet, a short boot")
PROPS = [
    ("grant-car", art.WIDE,
     f"Nobody is in the frame. a pearl-white full-size four-door luxury sedan (not a limousine) with tinted rear windows, no badge, number plate out of frame: {SEDAN}; parked at a "
     "wet grey curb on an overcast Pacific Northwest street, seen straight from the side, the whole car in the frame, grey-blue overcast "
     "daylight, wet asphalt, the windows dark, plain grey wall behind it, no signs."),
    ("black-car", art.WIDE,
     f"Nobody is in the frame. a black full-size four-door luxury sedan (not a limousine) with no badge, number plate out of frame: {SEDAN}; parked at a wet grey curb on an "
     "overcast Pacific Northwest street, seen straight from the side, the whole car in the frame, grey-blue overcast daylight, wet asphalt, "
     "the windows dark, plain grey wall behind it, no signs."),
    ("canvas-tote", art.BUST,
     "a plain beige canvas tote bag with no print, hanging from her left shoulder, soft and half full: on an older woman's left shoulder over a "
     "washed-out oatmeal cardigan, seen from the side from her shoulder to her knees; the top edge of the frame cuts across her shoulder, so "
     "her neck, head and face are not in the frame at all; the bottom of the tote reaches her hip."),
]
# f1 (owner 2026-11-12 「該修就修」): the small fixes first listed for batch 2 that episodes 1-10 or the whole season use.
# (id, refs file, size, what stays, the one change)
FIXES = [
    ("nora-portrait-freckles", "nora-portrait.jpg", art.BUST, "the face, eyes, hair, sweater, expression, framing, the plain grey backdrop and the lighting",
     "her forehead is smooth and clear with no spots; her faint freckles are only across the bridge of her nose and the tops of her cheeks."),
    ("grant-portrait-lapel", "grant-portrait.jpg", art.BUST, "the face, glasses, hair, suit, shirt, expression, framing, the plain grey backdrop and the lighting",
     "the small dark rectangle on his left lapel is gone; both lapels are plain, bare fabric."),
    ("peg-portrait-pendant", "peg-portrait.jpg", art.BUST, "the face, glasses, hair, cardigan, expression, framing, the plain grey backdrop and the lighting",
     "her long brown wooden-bead necklace ends in plain beads with no pendant, no loop and no ring-shaped piece."),
    ("peg-coat-pendant", "peg-coat.jpg", art.BUST, "the face, glasses, hair, coat, expression, framing, the plain grey backdrop and the lighting",
     "her long brown wooden-bead necklace ends in plain beads with no pendant, no loop and no ring-shaped piece."),
    ("door-out-gold-lock", "set-glass-house-door-out-gold.jpg", art.SETV, "the house, the door, the steps, the lamppost, the camera position and the light",
     "the brushed-steel lock plate and handle on the door frame are completely plain and smooth, with no mark, number or letter on them."),
    ("bus-stop-notice", "set-bus-stop.jpg", art.SETV, "the shelter, the bench, the harbor, the cranes, the camera position and the light",
     "the paper notice on the shelter's glass is gone; that glass panel is plain clear glass like the others; the containers across the water carry no readable markings."),
    ("bedroom-am-nightstand", "set-glass-house-bedroom-am.jpg", art.SETV, "the room, the bed, the glass wall, the sea, the camera position and the light",
     "the small nightstand between the bed and the glass is pale oak instead of dark wood, with only a clear glass of water, a small flat white saucer and a white tissue box on it."),
    ("nora-hospital-freckles", "nora-hospital.jpg", art.BUST, "the face, eyes, hair, gown, cardigan, expression, framing, the plain grey backdrop and the lighting",
     "her forehead is smooth and clear with no spots; her faint freckles are only across the bridge of her nose and the tops of her cheeks."),
    ("ambulance-end-wall", "set-ambulance.jpg", (816, 1440), "the stretcher, the pillow, the rails, the side walls, the ceiling light, the camera position and the light",
     "the far end of the cabin is a plain dark padded wall with no window and no lights outside."),
]
# s9 (after looking at s7/s8, 2026-11-12): the model kept putting the sea and the sun outside the land-side door and the east
# glass, drew the car from the wrong end (or as a cut-away on grey), and the road shoulder from above. Retried with the land
# filling the glass and the camera spelled out; two picks get one-change edits (an IV bag, a wall screen).
LAND = ("outside, filling the glass: a gravel forecourt, a gravel drive curving away down a grassy slope to the lower right, and a dense "
        "wall of dark fir trees under a grey sky; land only, no water anywhere, the sea is behind the camera")
S9 = [
    ("liv-east-gold", "a tall vertical view inside a single-storey glass-walled modern house with a flat white ceiling just above the glass, "
     "looking from the sea-side glass toward the entry: pale oak floor, the long pale wood dining table on the LEFT of the frame, the low grey "
     "sofa on the RIGHT with its back to the camera, heavy opaque charcoal-grey curtains closed over the glass at the table end on the left; "
     f"the entry-side glass wall bare, {LAND}. Light: one wide beam of low red-gold sunset light from behind the camera across the floor and "
     f"the sofa back; the forecourt outside glowing gold. {NOBODY}"),
    ("door-in-day", f"a tall vertical view from inside the pale oak entry of a modern single-storey glass house toward its front door: the pale "
     "oak entry floor in the foreground, a tall black steel-framed glass front door, CLOSED, hinged on its left, an ordinary black lever handle "
     "on its right edge, plain glass walls on both sides; just outside the door a plain doormat on a stone landing and two wide grey stone "
     f"steps down, one tall slim modern black lamppost on the grass just left of the steps, unlit; {LAND}. Light: grey overcast afternoon, "
     f"drizzle, raindrops on the glass, cool blue inside, no lamps on. {NOBODY}"),
    ("door-in-gold", "a tall vertical view from inside the pale oak entry of a modern single-storey glass house toward its front door: the "
     "pale oak entry floor in the foreground, the tall black steel-framed glass front door standing open, swung inward against the wall on the "
     "left, a brand-new brushed-steel deadbolt and lever handle on the black steel door frame, bright and unscratched; just outside a plain "
     f"doormat on a stone landing and two wide grey stone steps down, one tall slim modern black lamppost on the grass just left of the steps, "
     f"unlit; {LAND}. Light: low sunset light from behind the camera through the house, the forecourt, the drive and the firs outside lit "
     f"gold-orange; no sun in the frame. {NOBODY}"),
    ("gcar-day", "a photograph taken inside a pearl-white luxury sedan, the camera on the dashboard between the two front seats, looking "
     "BACKWARD at the rear bench: the tops of the two empty front seats at the lower left and lower right edges of the frame, between them "
     "and filling the middle of the frame one cream leather rear bench seat for two with a wide centre armrest console with a closed plain "
     "lid, the rear window behind the rear headrests, tinted side windows, a plain roof lining with no sunroof, no badges or logos. Light: "
     "grey overcast noon; blurred grey sea outside the right side window and dark firs outside the left. The car's interior fills the whole "
     "frame; nothing outside the car but the view through its windows. Nobody is in the frame; nothing written anywhere."),
    ("drive-foot", "a tall vertical photograph taken at eye level from the gravel shoulder of a two-lane coast road at sea level, at the foot "
     "of a tall grassy bluff: in the foreground the wet gravel shoulder and the asphalt road running off to the LEFT along grey Puget Sound "
     "water; on the right a narrow asphalt drive leaves the road and climbs steeply up the grassy bluff; a low wooden guardrail; wind-bent "
     "grass and dark firs; at the very top right, small against the sky, a modern single-storey glass house. Light: low red-gold sunset light "
     "from the upper right behind the bluff, the sun itself hidden. Nobody is in the frame; no cars; nothing written anywhere."),
]
S9_EDITS = [
    ("room-night-iv", "s8-room-night-a.png", art.SETV, "the room, the bed, the window, the lamp, the camera position and the light",
     "the IV stand is a bare metal pole with nothing hanging from it: no bags, no tubes."),
    ("hall-screen", "s8-hall-b.png", art.SETV, "the corridor, the doors, the nurses' station, the bench, the camera position and the light",
     "the small wall-mounted screen near the ceiling at the top right is gone; that wall is plain."),
]

# p7 (after p5/p6): both sedans came out as limousines a third time ("not a limousine" did not help), so they are drawn from a
# three-quarter front view, the shape a stretch car cannot fake; Peg's portrait kept its pendant in both takes; the road
# shoulder was drawn from above twice. The six p6 jobs a lost connection left undone run again here (from p6.json).
SEDAN3 = ("seen from a three-quarter front angle at eye level, the whole car in the frame: a modern four-door executive sedan of ordinary "
          "length, exactly two doors on the visible side, a short distance between the front and rear wheels, a long bonnet, a short boot")
P7 = [
    ("grant-car", art.WIDE, f"Nobody is in the frame. a pearl-white full-size four-door luxury sedan with tinted rear windows, no badge, number "
     f"plate out of frame, {SEDAN3}; parked at a wet grey curb on an overcast street, plain grey wall behind it, grey-blue overcast daylight, wet asphalt, no signs."),
    ("black-car", art.WIDE, f"Nobody is in the frame. a black full-size four-door luxury sedan with no badge, number plate out of frame, "
     f"{SEDAN3}; parked at a wet grey curb on an overcast street, plain grey wall behind it, grey-blue overcast daylight, wet asphalt, no signs."),
    ("drive-foot", art.SETV, "a tall vertical photograph taken standing on the gravel shoulder of a quiet two-lane coast road at the waterline, "
     "the camera at road level looking slightly UP: the road runs away to the LEFT beside grey Puget Sound water; on the right a steep grassy "
     "bluff rises high above the camera, a narrow paved driveway climbing it diagonally from the road toward the upper right; at the top of "
     "the bluff, high in the frame and small against the sky, a modern single-storey glass house; a low wooden guardrail along the road, "
     "dark firs on the bluff. Light: low red-gold sunset light from the upper right, the sun hidden behind the bluff. Nobody is in the frame; "
     "no cars; nothing written anywhere."),
]
P7_EDITS = [
    ("peg-portrait-pendant", "peg-portrait.jpg", art.BUST, "the face, glasses, hair, cardigan, expression, framing, the plain grey backdrop and the lighting",
     "the round pendant at the end of her wooden-bead necklace is removed; the beads simply continue as one plain loop with nothing hanging from it."),
]

# l1: the plan's 「改自」 light versions, made from the redrawn bases (art.py's s4 read the old ones). The plan's sentences
# still describe the old layouts, so each edit only says what changes; two seeds each (owner: quality first).
# (plan #, id, base picture in the work dir — "{room}" is the picked hospital-room edit, what changes)
L1 = [
    (3, "bed-night", "s7-bed-north-sconce-b.png",
     "the wall lamp is switched off. Light: deep night; the glass wall on the left is black with rain streaks; the only light is a low "
     "warm-yellow night light in the hallway outside the half-open door at the back right, falling into the room; the room is mostly dark blue shadow."),
    (6, "liv-tv", "s1-set-glass-house-living-liv-day-v-a.png",
     "night: every glass wall is black with drizzle; a warm white floor lamp beside the sofa is the only lamp; a slim flat black TV stands on "
     "the low pale oak cabinets in front of the sea-side glass, facing the sofa, its screen a soft plain white glow with nothing on it."),
    (17, "room-dawn", "{room}",
     "dawn after rain, overcast; the bed lamp is off; cold grey-blue light through the blinds falls across the bed in thin slanting stripes; "
     "the hallway light through the door is dim."),
    (18, "room-noon", "{room}",
     "bright white noon light through the blinds falls across the bed in steep, sharp stripes; the bed lamp is off."),
    (22, "liv-gold-b", "s7-liv-gold-a-a.png",
     "heavy charcoal-grey curtains now also hang over the glass behind the sofa; the two short ladders stand at the next bare panel, behind "
     "the right half of the sofa. Light: deeper amber sunset; only a few narrow strips of gold leak in between the curtains; the room is dimmer."),
    (25, "nur-gold", "s7-nur-day-b.png",
     "a grey two-step ladder stands in front of the window; the ceiling light is switched on. Light: the last low golden sunset light "
     "through the big window."),
    (33, "mroom-dark", "s8-mroom-night-a.png",
     "the bedside lamp is switched off and the bathroom door stays closed with no light behind it. Light: dark; only a thin red neon glow "
     "through the curtain gap falls across the left bed and the nightstand; the rest is deep shadow."),
]

# a4's lettering edit on Dr. Brandt failed twice (the coat kept an embroidered name), so she is drawn new, with the coat spelled out.
BRANDT = ("a 48-year-old white German-American woman, short silver-blond bob, rectangular glasses, a completely plain white doctor's coat "
          "with no embroidery, no name, no badge, no logo and nothing in its pockets, over navy scrubs")
PICK: dict[str, str | None] = {}
ROUNDS = {"s7": "sets", "s8": "sets", "a5": "people", "p4": "props", "f1": "fixes", "s9": "retry", "p7": "retry2", "l1": "light"}


def jobs_for(name: str, work: Path) -> list[dict]:
    jobs = []
    if ROUNDS[name] == "sets":
        for pos, (sid, _was, text) in enumerate(SETS[name]):
            prompt = art.SET_NEW.format(p=text, real=build.REAL)
            for t, take in enumerate(("a", "b")):
                jid = f"{sid}-{take}"
                seed = 750000 + (0 if name == "s7" else 100) + pos * 10 + t
                jobs.append(build.job(jid, f"{name} {sid} {take}", [art.CANVAS[art.SETV]], prompt, art.SETV, seed, f"{name}-{jid}.png"))
    elif ROUNDS[name] == "props":
        for pos, (pid, size, text) in enumerate(PROPS):
            prompt = f"{art.PROP_HEAD} {art.PROP_BLANK} {text} {art.PROP_CLEAN}"
            for t, take in enumerate(("a", "b")):
                jid = f"prop-{pid}-{take}"
                jobs.append(build.job(jid, f"p4 {pid} {take}", [art.CANVAS[size]], prompt, size, 761000 + pos * 10 + t, f"p4-{jid}.png"))
    elif ROUNDS[name] == "retry":
        for pos, (sid, text) in enumerate(S9):
            prompt = art.SET_NEW.format(p=text, real=build.REAL)
            for t, take in enumerate(("a", "b")):
                jobs.append(build.job(f"{sid}-{take}", f"s9 {sid} {take}", [art.CANVAS[art.SETV]], prompt, art.SETV, 750500 + pos * 10 + t, f"s9-{sid}-{take}.png"))
        for pos, (eid, src, size, keep, change) in enumerate(S9_EDITS):
            prompt = f"Edit image 1: keep {keep} exactly the same. Change only this: {change} {build.REAL}"
            for t, take in enumerate(("a", "b")):
                jobs.append(build.job(f"{eid}-{take}", f"s9 {eid} {take}", [src], prompt, size, 750600 + pos * 10 + t, f"s9-{eid}-{take}.png", latent="image1"))
    elif ROUNDS[name] == "light":
        room = PICK.get("room")
        if not room:
            sys.exit("redraw.py: l1 needs --room <picked hospital-room edit, e.g. s9-room-night-iv-a.png>")
        for n, lid, base, change in L1:
            src = base.format(room=room)
            if not (work / src).is_file():
                sys.exit(f"redraw.py: {src} is not in {work}")
            prompt = art.SET_EDIT.format(p=change, real=build.REAL)
            for t, take in enumerate(("a", "b")):
                jobs.append(build.job(f"{lid}-{take}", f"l1 #{n} {lid} {take}", [src], prompt, art.SETV, 740000 + n * 10 + 5 + t, f"l1-{lid}-{take}.png", latent="image1"))
    elif ROUNDS[name] == "retry2":
        p6 = work / "p6.progress.json"
        if p6.is_file():
            done = {j["id"] for j in json.loads(p6.read_text(encoding="utf-8"))["jobs"] if j["status"] == "completed"}
            jobs += [j for j in json.loads((work / "p6.json").read_text(encoding="utf-8"))["jobs"] if j["id"] not in done]
        for pos, (pid, size, text) in enumerate(P7):
            if size == art.SETV:
                prompt = art.SET_NEW.format(p=text, real=build.REAL)
            else:
                prompt = f"{art.PROP_HEAD} {art.PROP_BLANK} {text} {art.PROP_CLEAN}"
            for t, take in enumerate(("a", "b")):
                jobs.append(build.job(f"{pid}-{take}", f"p7 {pid} {take}", [art.CANVAS[size]], prompt, size, 762000 + pos * 10 + t, f"p7-{pid}-{take}.png"))
        for pos, (eid, ref, size, keep, change) in enumerate(P7_EDITS):
            src = art.copy_ref(work, ref)
            prompt = f"Edit image 1: keep {keep} exactly the same. Change only this: {change} {build.REAL}"
            for t, take in enumerate(("a", "b")):
                jobs.append(build.job(f"{eid}-{take}", f"p7 {eid} {take}", [src], prompt, size, 762100 + pos * 10 + t, f"p7-{eid}-{take}.png", latent="image1"))
    elif ROUNDS[name] == "fixes":
        prompt = f"{build.BLANK} {build.PORTRAIT_FRAME}She is: {BRANDT}. She is the only person in the frame. {build.REAL}"
        for t, take in enumerate(("a", "b")):
            jobs.append(build.job(f"dr-brandt-{take}", f"f1 dr-brandt {take}", [art.CANVAS[art.BUST]], prompt, art.BUST, 717500 + t, f"f1-dr-brandt-{take}.png"))
        for pos, (fid, ref, size, keep, change) in enumerate(FIXES):
            src = art.copy_ref(work, ref)
            prompt = f"Edit image 1: keep {keep} exactly the same. Change only this: {change} {build.REAL}"
            for t, take in enumerate(("a", "b")):
                jid = f"{fid}-{take}"
                jobs.append(build.job(jid, f"f1 {fid} {take}", [src], prompt, size, 717000 + pos * 10 + t, f"f1-{jid}.png", latent="image1"))
    else:
        for pos, (pid, ref, size, keep, change) in enumerate(PEOPLE):
            src = art.copy_ref(work, ref)
            prompt = f"Edit image 1: keep {keep} exactly the same. Change only this: {change} {build.REAL}"
            for t, take in enumerate(("a", "b")):
                jid = f"{pid}-{take}"
                jobs.append(build.job(jid, f"a5 {pid} {take}", [src], prompt, size, 716000 + pos * 10 + t, f"a5-{jid}.png", latent="image1"))
    return jobs


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("rounds", nargs="*")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--into")
    ap.add_argument("--work")
    ap.add_argument("--room", help="l1: the picked hospital-room picture in the work dir")
    a = ap.parse_args(argv)
    PICK["room"] = a.room
    work = art.work_dir(a.work)
    if a.list or not a.rounds:
        total = 0
        for r in ROUNDS:
            n = 2 * (len(SETS[r]) if r in SETS else len(PROPS) if r == "p4" else len(FIXES) + 1 if r == "f1" else len(S9) + len(S9_EDITS) if r == "s9" else 3 + len(P7) + len(P7_EDITS) if r == "p7" else len(L1) if r == "l1" else len(PEOPLE))
            total += n
            print(f"{r:4} {n:3} images {n * art.CU_PER_IMAGE:5.2f} CU")
        print(f"all  {total:3} images {total * art.CU_PER_IMAGE:5.2f} CU")
        return 0
    work.mkdir(parents=True, exist_ok=True)
    for size, rel in art.CANVAS.items():
        if not (work / rel).is_file():
            build.write_png(work / rel, size)
    all_jobs = []
    for r in a.rounds:
        jobs = jobs_for(r, work)
        all_jobs += jobs
        if not a.into:
            (work / f"{r}.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            print(f"{work / f'{r}.json'}: {len(jobs)} jobs")
    if a.into:
        out = work / f"{a.into}.json"
        out.write_text(json.dumps({"jobs": all_jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{out}: {len(all_jobs)} jobs ({' '.join(a.rounds)}), about {len(all_jobs) * art.CU_PER_IMAGE:.2f} CU")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
