#!/usr/bin/env python3
"""Humor-gate wave 2 (QA-2026-11-04, round 3): one new or redrawn shot for each of the four episodes
that still had one reviewer saying the core gag was not on screen. A new id is added after its template
job (same reference images); an existing id is replaced and its old outputs move to the next free .oldN.
  python3 redo4.py"""
import copy
import json
import os
from pathlib import Path

W = Path("/root/mokaair-work/videos")
PAW = " All of the animal's limbs are furry animal paws with no human fingers, no human hands, no human skin."
NOBODY = " The background is empty: no people, no other animals, no duplicate of the character."
TAIL = " Photorealistic live-action photograph, vertical 9:16 frame. No readable text, no watermark, no logos."
H = "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\nintegrated_multimodal_description: [Shot 1] live-action. "
T = " One continuous shot.\noverall_soundscape: N/A\nnon_diegetic_music: N/A\n"
GUARD = " The character stays the same animal in the same clothes for the whole shot; its paws stay furry animal paws; no new character enters."
# slug: [(id, template id, first-frame prompt, clip prompt, has_character)]
WAVE = {
 "raccoon-mischief-e01": [(
  # Two reviewers: a raccoon behind a table hugging a blue cloth does not read as a vase.
  "s03b-vase", "s03-vase",
  "Medium shot of a small wooden side table in a cozy sunlit living room; standing on top of the table is Doudou the young raccoon himself pretending to be the vase: his whole body from the neck down is wrapped tightly in a smooth glossy dark blue cloth so it bulges into the round fat shape of a big ceramic vase with a narrow neck, no arms and no legs visible, only his black-masked raccoon face sticking out of the top like the vase's opening, three red flowers standing upright behind his ears like flowers in a vase; frozen wide eyes.",
  "The young raccoon shown in <Picture 1> stays perfectly still as the vase; only his eyes slide slowly sideways once and back, and a single red petal falls from the flowers. The camera holds a static shot.", True)],
 "influencer-piglet-e02": [(
  # Viewer A: the frosted face looks cold, not like a sneeze is coming.
  "s05b-inhale", "s04-boyfriend",
  "Extreme close-up of the capybara boyfriend's face under a blue sky, his eyebrows and whiskers frosted white with ice crystals, his head tipped far back, eyes squeezed shut, nostrils flared wide open, mouth half open, the moment right before a huge sneeze.",
  "The capybara shown in <Picture 1> tips his head even further back, his flared nostrils twitch and widen, his cheeks puff, he sucks in a long breath, then his head snaps forward in a huge sneeze that blows a cloud of ice crystals toward the camera. The camera holds a static shot.", True)],
 "influencer-piglet-e03": [(
  # Both reviewers in round 1, viewer A since: he never plugs the hole.
  "s04-boyfriend", "s04-boyfriend",
  "Medium close shot on a grey rooftop of the capybara boyfriend himself, soaking wet, standing on a short ladder and hugging the side of a big round stainless steel water tank, his round furry belly pressed flat over a hole in the tank, thin jets of water spraying out sideways all around the edges of his belly, water pouring off his green bucket hat, his grey T-shirt soaked, a strained deadpan face.",
  "The capybara shown in <Picture 1> presses his belly harder against the tank; the jets of water spray out around him, one jet squirts straight into his face and he does not flinch, blinking slowly. The camera holds a static shot.", True)],
 "shechu-hell-e03": [(
  # Viewer A: the stapler is never pushed off; the thud has no picture.
  "s08-stapler", "s04-toy",
  "Close insert of the corner of a plain grey office desk next to a dark keyboard, a plain pale office wall right behind it: a plain grey metal stapler is falling from above, caught in mid-air just above the desk.",
  "The plain grey stapler falls into the frame from above, hits the desk next to the keyboard with a hard bounce, spins once and stops. The camera holds a static shot.", False)],
}


def park(f):
    if not f.exists():
        return
    n = 1
    while Path(f"{f}.old{n if n > 1 else ''}").exists():
        n += 1
    os.rename(f, f"{f}.old{n if n > 1 else ''}")


for slug, shots in WAVE.items():
    w = W / slug / "colab"
    ff = json.loads((w / "ff.json").read_text())
    clips = json.loads((w / "clips.json").read_text())
    for sid, tid, ffp, clip, char in shots:
        tj = next(j for j in ff["jobs"] if j["id"] == tid)
        lead = tj["prompt"].split(". ", 1)[0]
        prompt = lead + ". " + ffp + (PAW + NOBODY if char else " No animals and no people anywhere in the picture.") + TAIL
        if sid == tid:
            tj.update(prompt=prompt, seed=11)
            for f in (w / "ff" / f"{sid}.png", w / "clips" / f"{sid}.mp4", w / f"{sid}.detached.json"):
                park(f)
        else:
            nj = copy.deepcopy(tj)
            nj.update(id=sid, prompt=prompt, seed=11, output_name=f"{sid}.png")
            ff["jobs"].insert(ff["jobs"].index(tj) + 1, nj)
            tc = next(c for c in clips["jobs"] if c["id"] == tid)
            nc = copy.deepcopy(tc)
            nc.update(id=sid, title=sid, reference_images=[f"ff/{sid}.png"], prompt_file=f"prompts/{sid}.txt", output_name=f"{sid}.mp4",
                      output_path=str(w / "clips" / f"{sid}.mp4"))
            clips["jobs"].insert(clips["jobs"].index(tc) + 1, nc)
        (w / "prompts" / f"{sid}.txt").write_text(H + clip + (GUARD if char else "") + T)
    (w / "ff.json").write_text(json.dumps(ff, indent=1))
    (w / "clips.json").write_text(json.dumps(clips, indent=1))
    print(slug, [s[0] for s in shots])
