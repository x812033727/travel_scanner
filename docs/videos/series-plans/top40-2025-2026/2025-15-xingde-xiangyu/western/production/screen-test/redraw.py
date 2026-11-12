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
         "a tall vertical view of the back seat of a long pearl-white luxury sedan, seen from the dashboard between the two empty front seats "
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
ROUNDS = {"s7": "sets", "s8": "sets", "a5": "people"}


def jobs_for(name: str, work: Path) -> list[dict]:
    jobs = []
    if ROUNDS[name] == "sets":
        for pos, (sid, _was, text) in enumerate(SETS[name]):
            prompt = art.SET_NEW.format(p=text, real=build.REAL)
            for t, take in enumerate(("a", "b")):
                jid = f"{sid}-{take}"
                seed = 750000 + (0 if name == "s7" else 100) + pos * 10 + t
                jobs.append(build.job(jid, f"{name} {sid} {take}", [art.CANVAS[art.SETV]], prompt, art.SETV, seed, f"{name}-{jid}.png"))
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
    a = ap.parse_args(argv)
    work = art.work_dir(a.work)
    if a.list or not a.rounds:
        total = 0
        for r in ROUNDS:
            n = 2 * (len(SETS[r]) if r in SETS else len(PEOPLE))
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
