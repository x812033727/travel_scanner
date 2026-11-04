#!/usr/bin/env python3
"""Mark shots for a redo: new first-frame prompt (+ guards), new clip prompt, and delete the old outputs.
  python3 redo.py   (edits ff.json/prompts in each workdir from REDO below)"""
import json, os
from pathlib import Path
W = Path("/root/mokaair-work/videos")
PAW = " All of the animal's limbs are furry animal paws with no human fingers, no human hands, no human skin."
NOBODY = " The background is empty: no people, no other animals, no duplicate of the character."
H = "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\nintegrated_multimodal_description: [Shot 1] live-action. "
T = " One continuous shot.\noverall_soundscape: N/A\nnon_diegetic_music: N/A\n"
CLIPGUARD = " The character stays the same animal in the same clothes for the whole shot; its paws stay furry animal paws; no new character enters."
REDO = {
 "raccoon-mischief-e04": {
  "s03-hands": ("Medium shot of a living room wall where a wall clock used to hang: there is NO clock anywhere in the picture, only a pale round mark on the wallpaper. Doudou the young raccoon himself in his yellow hoodie stands pressed flat against the wall inside that pale round mark, his red cape spread out behind him like a round clock face, one arm pointing straight up and the other pointing to the side like the hands of a clock, a frozen serious face.",
                "The young raccoon shown in <Picture 1> stays pressed flat against the wall, arms held stiffly like clock hands; one arm ticks forward a tiny step. The camera holds a static shot."),
  "s05-spin": ("Medium shot of the same living room wall with NO clock anywhere: Doudou the young raccoon himself pressed flat against the wall, red cape spread behind him like a clock face, one arm pointing up, the other arm starting to swing around like a clock hand.",
               "The young raccoon shown in <Picture 1> swings one arm in a full fast circle like a clock hand spinning, then twists awkwardly and freezes. The camera holds a static shot.")},
 "raccoon-mischief-e01": {
  "s01-crash": ("Medium shot of the cozy living room: on the wooden floor lie the smashed pieces of one big blue ceramic vase, flowers and water spilled everywhere; there is no other vase anywhere in the room; on the sofa Doudou the young raccoon himself in his yellow hoodie and red cape is frozen mid superhero take-off pose, one arm stretched forward.",
                "The last shard of the vase spins twice on the floor and stops; the young raccoon shown in <Picture 1> does not move at all, not even blinking. The camera holds a static shot.")},
}
for slug, shots in REDO.items():
    w = W / slug / "colab"
    ff = json.loads((w / "ff.json").read_text())
    for sid, spec in shots.items():
        if spec is None:
            continue
        ffp, clip = spec
        for j in ff["jobs"]:
            if j["id"] == sid:
                lead = j["prompt"].split(". ", 1)[0] if j["prompt"].startswith("image 1") else ""
                j["prompt"] = (lead + ". " if lead else "") + ffp + PAW + NOBODY + " Photorealistic live-action photograph, vertical 9:16 frame. No readable text, no watermark, no logos."
                j["seed"] = 3
        (w / "prompts" / f"{sid}.txt").write_text(H + clip + CLIPGUARD + T)
        for f in (w / "ff" / f"{sid}.png", w / "clips" / f"{sid}.mp4", w / f"{sid}.detached.json"):
            if f.exists():
                os.rename(f, str(f) + ".old")
    (w / "ff.json").write_text(json.dumps(ff, indent=1))
    print(slug, [s for s, v in shots.items() if v])
