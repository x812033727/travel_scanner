#!/usr/bin/env python3
"""screen-test-plough.py OUT_DIR : the prop reference picture of the curved-beam plough (曲轅犁) for the e015 live retakes
(colab/runs/e915-live/fix2). NOT run here. Seeds 37021/37022 (e017 used 37019/37020), 2 jobs, one manifest
OUT_DIR/plough.json; prompts in OUT_DIR/prompts/. The manifest is meant for
~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-plough/. Check before running:
    python3 -I .agents/skills/minimax-h3-colab/scripts/check_images_manifest.py OUT_DIR/plough.json
The pick is filed as refs-live/prop-quyuanli-l1.png (fix2's s21 and s26 send it; mkjobs.py and q-e915fix2.sh look for it).

Why: in s21 (d1 both takes, fix1 both takes) and in the s25/s26 far views the plough came out as a straight beam with a
crescent iron blade bigger than a head, although fix1 wrote the whole plough in words (a bow-curved beam, a palm-sized
leaf-shaped share, "the only metal on the whole plough"). Words alone do not move it; a picture of the prop does (the way
the sets fixed the places). Only e015 shows the plough: season-01.md and r2-bible-e011-e060.md name it only in e015, the
e016-e020 scripts (r2 and CG) never mention 犁, and later briefs (e033, e035, e040) only use "ploughed field" as a place word.
Still filed under refs-live so a later scene can send it.

The picture: an edit of set-qiutian-l2 (the e015 field, same willow on the ridge at the right, same hills), the field made
one flat stubble surface (the l2 rows are the source of the "already ploughed" fields of s13-s25), and in the foreground,
seen exactly side-on and filling most of the width, one Song-dynasty curved-beam plough standing on its sole: the beam
rising from the top of the short handle at the back (right) and curving forward and down in one smooth deep arc to a low
front end (left); a short flat wooden sole along the ground; at its front tip one small rounded dull dark iron share about
the size of a man's hand; plain weathered brown wood, matte, and dark iron. Same camera side as the shots (front to screen
left: s21 walks right to left, s25 and s26 push toward screen left). The shot's field is in it, so s21 can send it in the
set picture's slot.
The positive prompt says only what is there (bible 拍法 18); the things to keep out are in the negative file.
"""
import json
import sys
from pathlib import Path

out = Path(sys.argv[1]); (out / "prompts").mkdir(parents=True, exist_ok=True)
LIVE = Path(__file__).resolve().parent.parent / "assets" / "refs-live"
SEEDS = (37021, 37022)
PID, BASE = "prop-quyuanli-l1", "set-qiutian-l2"

STYLE = ("Ancient China, Song dynasty. Style: a photorealistic live-action photograph of a real farm tool on location for a "
         "Chinese historical costume drama, shot on a cinema camera at the height of the tool, natural light, real weathered "
         "wood, dull hand-forged iron, dry earth and straw textures, deep focus, everything sharp from front to back; a clean "
         "natural film image that fills the whole frame edge to edge.")
KEEP = ("image 1 is a photograph of the place: keep its big willow with yellow autumn leaves on the raised grass ridge at the "
        "right, the low tiled farmhouses and the blue hills far off and the pale sky; change the field and the foreground "
        "into what is described here. ")
DESC = (
    "A side-view photograph of one ancient Chinese farm tool standing in a harvested rice field: "
    "(1) the whole field is one flat level surface of hard dry dark earth with short pale cut rice stubble dotted evenly "
    "all over it like a close-cropped carpet, smooth and even to the ridge; "
    "(2) in the foreground, in the middle of the frame and filling most of its width, seen exactly from the side, stands "
    "one Song-dynasty curved-beam plough, its front pointing to the left: at the back on the right one short plain wooden "
    "handle rising at a slant to about waist height; from the top of that handle one long plain wooden beam runs forward "
    "to the left and curves down in one smooth deep arc like a drawn bow, its front end low near the ground, the curve "
    "plain to see against the dark earth and the pale sky; along the ground under the beam one short flat wooden sole "
    "lying level on the soil, joined to the foot of the handle; at the front tip of the sole one small rounded share of "
    "dull dark iron about the size of a man's hand, smooth and rounded like a leaf, its tip touching the soil; "
    "(3) every part is plain weathered mid-brown wood, matte, joined with wooden pegs, and the small share is the only "
    "iron, dull and dark; a simple sturdy village-made tool about as long as a man is tall; "
    "(4) soft warm late-afternoon sunlight slanting low from the left, the plough's long soft shadow lying on the stubble; "
    "the field quiet and deserted, the plough standing alone on it.")
NEG = ("3D render, CGI, game render, plastic, cartoon, anime, illustration, painting, diagram, text, writing, calligraphy, "
       "Chinese characters, letters, inscription, watermark, logo, black bars, border, people, person, hands, figure, "
       "silhouette, ox, cow, buffalo, horse, harness, yoke, rope, chain, cart, wheel, "
       "blade, large blade, crescent blade, axe, axe head, halberd, sword, knife, sickle, scythe, spear, weapon, saw teeth, "
       "serrated edge, big metal sheet, shiny metal, polished steel, chrome, straight beam, straight pole, "
       "furrows, ridges, ploughed rows, rows of stubble, stripes, water, mud, second plough, two ploughs")

src = LIVE / f"{BASE}.png"
assert src.is_file(), f"refs-live/{BASE}.png is missing; {PID} is an edit of it"
assert not (LIVE / f"{PID}.png").exists(), f"refs-live/{PID}.png already exists; pick a new l-number"
body = KEEP + DESC + " " + STYLE
for bad in (" no ", " not ", "without", "never", "nobody", "nothing", " gone"):
    assert bad not in body.lower(), f"{PID}: the positive prompt has '{bad.strip()}' (write what is there)"
prompt = out / "prompts" / f"{PID}.txt"
prompt.write_text(body, encoding="utf-8")
neg = out / "prompts" / f"negative-{PID}.txt"
neg.write_text(NEG, encoding="utf-8")
jobs = [{"id": f"{PID}-{s}", "reference_images": [str(src)], "prompt_file": str(prompt), "negative_file": str(neg),
         "width": 1312, "height": 736, "seed": s, "latent": "empty"} for s in SEEDS]
(out / "plough.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / "plough-pictures.json").write_text(json.dumps([{"picture": PID, "seeds": list(SEEDS), "base": "edit of " + BASE,
                                                       "first_shot": "e015 s21 (fix2)"}], ensure_ascii=False, indent=1)
                                          + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "plough.json")
