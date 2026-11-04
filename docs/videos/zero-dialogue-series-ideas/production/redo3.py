#!/usr/bin/env python3
"""Humor-gate redo wave (QA-2026-11-04): redraw the shots whose gag was not on screen.
  python3 redo3.py   (rewrites ff.json/prompts in each workdir; old outputs move to the next free .oldN)"""
import json
import os
from pathlib import Path

W = Path("/root/mokaair-work/videos")
PAW = " All of the animal's limbs are furry animal paws with no human fingers, no human hands, no human skin."
NOBODY = " The background is empty: no people, no other animals, no duplicate of the character."
H = "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\nintegrated_multimodal_description: [Shot 1] live-action. "
T = " One continuous shot.\noverall_soundscape: N/A\nnon_diegetic_music: N/A\n"
CLIPGUARD = " The character stays the same animal in the same clothes for the whole shot; its paws stay furry animal paws; no new character enters."
REDO = {
 "wangjia-couple-e02": {
  # Reviewers: the buzz cut does not read; she looked like an ordinary Shiba in a head scarf.
  "s05-buzz": ("Medium shot of a living room doorway in the morning: Zhenzhu the Shiba herself stands upright in her pink floral dress; the top of her head is shaved almost bare in a very short buzz cut, the pale shaved skin of her scalp clearly visible between tiny short bristles, a startling contrast with her fluffy cheeks; a few fluffy pink tufts of shaved-off fur lie on the floor around her feet; a plain grey electric hair clipper rests on the little table beside her; she wears a proud satisfied smile.",
               "The Shiba shown in <Picture 1> proudly rubs the top of her shaved buzz-cut head with one paw and strikes a proud pose toward the camera; a tuft of fluffy pink fur drifts down to the floor. The camera holds a static shot."),
 },
 "raccoon-mischief-e04": {
  # The watch shot was cut for a human-looking hand; without it the clock-hand spin has no reason.
  "s04-watch": ("Close-up of Mama raccoon herself in her green sweater and pearl necklace, her dark grey furry raccoon forearm raised in front of her chest with a plain round wristwatch strapped on it, white face with only two black hands and no numbers, the watch face turned toward the camera; her paw is a small dark furry raccoon paw with short black claws, curled closed; she glances down at the watch.",
                "The mother raccoon shown in <Picture 1> looks down at the wristwatch on her furry forearm, then slowly lifts her eyes to look off screen to the side; her brow furrows suspiciously and one eye narrows. The camera holds a static shot."),
 },
 "shechu-hell-e03": {
  # The relief beat had people in the background; the shadow shot drew a black blob and kept him smiling.
  "s05-relax": ("Medium shot of A-Jin the Golden Retriever himself at a grey office desk with a plain beige wall right behind him and nothing else in the background, leaning far back in his office chair in his white shirt and crooked blue tie, both furry hind paws up on the desk, front paws folded behind his head, eyes closed, a smug relieved grin.",
                "The Golden Retriever shown in <Picture 1> lets out a long relieved breath, sinks deeper into the chair with a smug grin and wiggles his hind paws on the desk. The camera holds a static shot."),
  "s06-shadow": ("Close-up of A-Jin the Golden Retriever himself leaning back in his office chair in his white shirt and crooked blue tie, a plain beige wall behind him, the upper half of his face already in the soft shadow of something above him, his smug grin starting to stiffen, eyes rolled up toward the ceiling.",
                 "The Golden Retriever shown in <Picture 1> stops grinning: his smile slowly droops into a horrified frown, his ears flatten against his head and his eyes stare straight up in terror as the soft shadow darkens over his face. The camera holds a static shot."),
 },
}


def park(f):
    if not f.exists():
        return
    n = 1
    while Path(f"{f}.old{n if n > 1 else ''}").exists():
        n += 1
    os.rename(f, f"{f}.old{n if n > 1 else ''}")


for slug, shots in REDO.items():
    w = W / slug / "colab"
    ff = json.loads((w / "ff.json").read_text())
    for sid, (ffp, clip) in shots.items():
        for j in ff["jobs"]:
            if j["id"] == sid:
                lead = j["prompt"].split(". ", 1)[0] if j["prompt"].startswith("image 1") else ""
                j["prompt"] = (lead + ". " if lead else "") + ffp + PAW + NOBODY + " Photorealistic live-action photograph, vertical 9:16 frame. No readable text, no watermark, no logos."
                j["seed"] = 5
        (w / "prompts" / f"{sid}.txt").write_text(H + clip + CLIPGUARD + T)
        for f in (w / "ff" / f"{sid}.png", w / "clips" / f"{sid}.mp4", w / f"{sid}.detached.json"):
            park(f)
    (w / "ff.json").write_text(json.dumps(ff, indent=1))
    print(slug, list(shots))
