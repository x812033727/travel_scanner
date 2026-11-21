#!/usr/bin/env python3
"""Till the Verdict model-voice pilot (owner 2026-11-12, cap 6 CU): Ref2VA hero drafts only, 544x960, 6 s each.

  voicepilot.py st1 [--work DIR]    write the manifest and prompts (run `H3_PROFILE=hero bootstrap.sh patch` first)

The owner switched on-screen dialogue to the model's own voice (the draft's audio track). Before the season is shot this
answers three questions with seven drafts taken from the reviewed storyboards (2026-11-12):
  1. Does H3 speak the written English line, in a General American accent?
  2. Is the same character's voice the same across shots and seeds? Nora speaks in four drafts (e001 c07 twice with two
     seeds, e001 c44, e003 c27); every Nora prompt carries the same voice sentence, and so on for Grant and Peg.
  3. A short shout with its words in the prompt (e002 c13 "Help! Somebody!"): are the words said, and do they burn in as text?
Only the portrait is referenced; the set is described in words (the sets for e002 and e003 are not drawn yet).
Work dir: $VIDEO_WORKDIR/_series/till-the-verdict/voicepilot. Standard library only; run with python3 -I.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402  (FACES_RULE)

REFS = HERE.parent / "assets" / "refs"
DRAFT = (544, 960)
TAIL = ("One continuous shot, the whole time at this framing; natural, realistic live-action human motion. Faces, hair and costumes match their "
        "reference pictures, and every visible face acts the expression written above. Nothing written anywhere in the frame: no subtitles, no captions, no text.")

VOICE = {
    "nora": "Her voice is a soft, steady, unhurried woman's voice in her early thirties with a General American accent, clear diction.",
    "grant": "His voice is a warm, smooth, even man's voice in his late thirties with a General American accent, like a keynote speaker.",
    "peg": "Her voice is a quick, blunt, dry woman's voice in her sixties with a General American accent.",
}
LOOK = {
    "pregnant": ("nora", "a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, a gentle oval face, "
                 "five months pregnant with a visible rounded belly, long dark chestnut hair loose past her shoulders, a loose cream cable-knit sweater dress"),
    "night-coat": ("nora", "a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, a gentle oval face, "
                   "five months pregnant, long dark chestnut hair loose and wet from rain, a loose cream cable-knit sweater dress under an open camel wool coat, her clothes clean"),
    "hospital": ("nora", "a 31-year-old white Irish-American woman, slender, fair skin with faint freckles across the nose, soft grey-green eyes, a gentle oval face, pale and tired, "
                 "long dark chestnut hair loose and slightly tangled, a plain light blue hospital gown under a cream cardigan, no makeup"),
    "rain": ("grant", "a 37-year-old white American man, good-looking in a polished way, sandy-blond hair side-parted and damp, clean-shaven, "
             "thin round metal-rim glasses with drops on the lenses, a light stone-colored suit with a wet collar"),
    "visit": ("peg", "a 62-year-old white American woman, short permed grey hair, a sharp lined face, tortoiseshell reading glasses on her face, "
              "a long brown wooden-bead necklace, a washed-out oatmeal cardigan over a plain blouse, dark slacks"),
}
NAME = {"nora": "Nora", "grant": "Grant", "peg": "Peg"}
PORTRAIT = {"nora": "nora-portrait.jpg", "grant": "grant-portrait.jpg", "peg": "peg-portrait.jpg"}

# (id, look, seed, composition, speech, action) — from the 2026-11-12 storyboards.
SHOTS = [
    ("e001-c07-a", "pregnant", 731000,
     "A medium close-up in a minimal bedroom of a glass house on a bluff: Nora sits up against the plain white wall at the head of a low bed, from her chest to a hand's width above her head; "
     "the right edge of the frame is a floor-to-ceiling glass wall with drizzle and a grey sea; in the lower right foreground a clear drinking glass about the size of her fist, half full of clear water, "
     "stands on the nightstand, untouched for the whole shot. Cold blue-grey overcast morning light. She is the only person in the frame.",
     "Nora speaks a short English line, \"My pill tastes sweet today.\", low and puzzled, to herself, her face three-quarter toward the glass of water at lower right, never looking at the camera, "
     "her brows drawn together and her eyes narrowed, no smile at any moment, until the last frame, her lips, jaw and cheeks moving clearly with every syllable.",
     "First she bites down on a tiny white pill, smaller than a fingernail (a medicine pill, not a device), and stops halfway through the bite; then she speaks; after the line her lips close "
     "and her eyes stay on the glass. The camera pushes in slowly from her chest to her shoulders."),
    ("e001-c07-b", "pregnant", 731001, None, None, None),  # same as a, second seed
    ("e001-c44", "pregnant", 731002,
     "A close-up of Nora in the same bedroom at night: her face in the upper third of the frame, the warm light of a wall lamp above the bed falling on her face from above; behind her only an out-of-focus "
     "white door and a camel coat. In her right palm, at the bottom of the frame, a white tissue opened at one corner. She is the only person in the frame.",
     "Nora speaks a short English line, \"The score line's too faint. That's not right.\", very quietly, as if she has just understood something, her face three-quarter down toward her palm, "
     "never looking at the camera, her brows knitted tight and her eyes narrowed on her palm, her lips pressing together between the two sentences, no smile at any moment, until the last frame, "
     "her lips, jaw and cheeks moving clearly with every syllable.",
     "After the line her fingers fold the tissue closed and her lips close. The camera pushes in slowly from her chest to her face."),
    ("e003-c27", "hospital", 731003,
     "A close-up of Nora half sitting up in a hospital bed in a single room at dawn: her face in the upper third of the frame, cold dawn light falling in stripes through window blinds behind her; "
     "the corner of a bedside table at lower right with an empty clear plastic cup lying on its side at its edge. She is the only person in the frame; the man she speaks to is off-frame right.",
     "Nora speaks a short English line, \"Your phone died? Then what's that?\", cold and very quiet, her face three-quarter toward the man off-frame right, her eyes on him, never looking at the camera, "
     "her brows pressed low, eyes narrowed, mouth corners turned down, her breathing slow, no smile at any moment, until the last frame, her lips, jaw and cheeks moving clearly with every syllable.",
     "Before the line her eyes drop to his suit off-frame right, stop, and rise to his face; after the line she lifts her chin slightly and her lips close. The camera holds a static shot."),
    ("e002-c13", "night-coat", 731004,
     "A close-up of Nora at night in heavy rain beside a black lamppost at the top of two stone steps outside a glass house: her face in the upper third of the frame with room above her head, "
     "the lamppost on screen right against her left shoulder, its lamp flickering on her face; behind her only black night and falling rain. Rain runs down her long hair; her coat is clean. "
     "She is the only person in the frame.",
     "Nora shouts a short English line, \"Help! Somebody!\", toward the dark driveway off-frame lower left, her face three-quarter toward lower left, never looking at the camera, eyes wide, brows shot up, "
     "mouth wide open, jaw dropped, neck tight, chest heaving, no smile at any moment, until the last frame, her lips, jaw and cheeks moving clearly with every syllable.",
     "First she looks up at the flickering lamp, then turns her face to the driveway and shouts; after the shout her mouth closes and she breathes hard. The camera pushes in slowly from her chest to her face."),
    ("e003-c12", "rain", 731005,
     "A close-up of Grant sitting on the edge of a hospital bed at dawn: his face in the upper third of the frame, cold dawn light in stripes through window blinds behind him; in the lower left foreground "
     "his two hands, in light stone suit cuffs with clear glass cufflinks, hold a woman's hand; only her hand is in frame. He is the only person whose face is in the frame.",
     "Grant speaks a short English line, \"We're still young, Nor. We'll try again.\", warm and smooth like a keynote, his face three-quarter toward the woman off-frame left, his eyes on her, never looking at the camera, "
     "his brows lifted in the middle, head tilted a little, chin tucked, mouth corners level and never turning up, no teeth, not a happy smile, no smile at any moment, until the last frame, "
     "his lips, jaw and cheeks moving clearly with every syllable.",
     "He leans toward her as he speaks; after the line he gives one small nod and his lips close, still leaning, still holding her hand. The camera pushes in slowly from his chest to his face."),
    ("e001-c36", "visit", 731006,
     "A medium close-up of Peg from inside the front door of a glass house, the door frame on both sides of the foreground, room above her head: warm white light from the hallway on her face, "
     "behind her a blue-grey evening driveway and drizzle. A flat plain beige canvas tote bag with no print hangs from her left shoulder. She is the only person in the frame; the woman she speaks to is off-frame left, inside the house.",
     "Peg speaks a short English line, \"Soup's in the fridge. Salt it yourself.\", dry, like a complaint, her face three-quarter toward the woman off-frame left, her eyes looking at her over the top of her glasses, "
     "never looking at the camera, brows flat and stern, mouth corners turned down, a short sniff before she speaks, no smile at any moment, until the last frame, her lips, jaw and cheeks moving clearly with every syllable.",
     "She turns half back toward the house and lifts her chin toward it; after the line she starts to turn away and her lips close. The camera pushes in slowly."),
]


def work_dir(flag: str | None) -> Path:
    base = Path(os.environ.get("VIDEO_WORKDIR") or Path.home() / "mokaair-work" / "videos")
    return Path(flag).expanduser().resolve() if flag else base / "_series" / "till-the-verdict" / "voicepilot"


def st1(work: Path) -> dict:
    (work / "st1" / "prompts").mkdir(parents=True, exist_ok=True)
    jobs, last = [], None
    for sid, look, seed, comp, speech, action in SHOTS:
        if comp is None:
            comp, speech, action = last
        last = (comp, speech, action)
        who, appearance = LOOK[look]
        name = NAME[who]
        prompt = ("For the target video, <Picture 1> is referenced throughout.\n\n"
                  f"integrated_multimodal_description: [Shot 1] Live-action, a modern American prestige TV drama, vertical 9:16 frame. "
                  f"{name}: {appearance}, shown in <Picture 1>, keeps exactly the same face as the picture. "
                  f"Initial composition: {comp} {build.FACES_RULE} {speech} {VOICE[who]} {action} {TAIL}\n"
                  "overall_soundscape: only the spoken line and quiet room tone\nnon_diegetic_music: N/A\n")
        pf = work / "st1" / "prompts" / f"{sid}.txt"
        pf.write_text(prompt, encoding="utf-8")
        jobs.append({"id": sid, "title": f"till-the-verdict voice pilot {sid}", "inference_mode": "reference",
                     "reference_images": [str(REFS / PORTRAIT[who])], "prompt_file": f"prompts/{sid}.txt",
                     "prompt_sha256": hashlib.sha256(pf.read_bytes()).hexdigest(), "duration_seconds": 6,
                     "width": DRAFT[0], "height": DRAFT[1], "output_path": str(work / "st1" / "out" / f"{sid}.mp4"), "seed": seed})
    return {"jobs": jobs}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("round", choices=["st1"])
    ap.add_argument("--work")
    a = ap.parse_args(argv)
    work = work_dir(a.work)
    work.mkdir(parents=True, exist_ok=True)
    manifest = st1(work)
    out = work / "st1" / "st1.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{out}: {len(manifest['jobs'])} jobs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
