#!/usr/bin/env python3
"""screen-test-yard-night.py OUT_DIR : set-xujia-yuan-ye-l2, the Xu yard at night, redrawn as an edit of the day yard l3.
NOT run here (no Colab in the writing session). Seeds 37009/37010 (e014 used 37007/37008), 2 jobs, one manifest
OUT_DIR/yard-night.json; prompts in OUT_DIR/prompts/. Check before running:
    python3 -I .agents/skills/minimax-h3-colab/scripts/check_images_manifest.py OUT_DIR/yard-night.json

Why (2026-11-15): e911 and e912 drafts kept growing racks of red-tasselled spears in the yard background even where no
person stands (e912 s22 retake, both seeds). Every shot says "the location shown in <Picture N> is the set, keeping its
layout and props", and the night yard picture it is given, set-xujia-yuan-ye-l1 (screen-test-e010.py), is a relight of
the day yard l2, so it still has what the e013 review took out of the day yard in l3 (screen-test-e013.py):
- the bundle of long poles leaning against the house at the far left edge (the spear racks grow there);
- the board at the yard wall with a long handle sticking up out of it, leaning on the wall (one more pole);
- a bright full moon sitting in the tree (the "dim moon behind cloud" of the e010 prompt came out as l2's sun);
- green-and-yellow fields beyond the wall, fruit all over the persimmon tree, a tiled house roof instead of thatch,
  and the blank board on the house wall turned into a plaque with fake characters in the lantern light.
This picture is an edit of refs-live/set-xujia-yuan-l3 (image 1), keeping its layout and camera position, with: deep
night, one blank paper lantern under the eaves as the main light, at most a faint moon glow behind thick cloud; nothing
leaning against any wall or fence (the long-handled board goes as well as l2's poles, which l3 already lost); no poles,
racks, spears, braziers or torch stands; no people; persimmons only high up; the harvested fields barely visible.
pilot.py takes the newest l-version of a set, so a pick saved as refs-live/set-xujia-yuan-ye-l2.png is used by every new
live prep that names set-xujia-yuan-ye-t1 (e911 and e912 s01-s35, e913 s33-s34); drafts already prepared keep l1.
Same templates, style and negative words as screen-test-e013.py / screen-test-e014.py.
"""
import json
import runpy
import shutil
import sys
import tempfile
from pathlib import Path

out = Path(sys.argv[1]); (out / "prompts").mkdir(parents=True, exist_ok=True)
here = Path(__file__).resolve().parent
LIVE = here.parent / "assets" / "refs-live"
full = Path(tempfile.mkdtemp(prefix="st-full-"))  # screen-test.py writes its own round-1 manifests; keep them out of OUT_DIR
# screen-test.py does its own `import sys` and writes its round-1 prompts and manifests under sys.argv[1]; point argv at
# the temp dir (as screen-test-e013.py and screen-test-e014.py do).
argv, sys.argv = sys.argv, ["screen-test.py", str(full)]
try:
    st = runpy.run_path(str(here / "screen-test.py"), run_name="screen_test_lib")
finally:
    sys.argv = argv
shutil.rmtree(full, ignore_errors=True)
day_l3 = LIVE / "set-xujia-yuan-l3.png"
assert day_l3.is_file(), "refs-live/set-xujia-yuan-l3.png is missing; set-xujia-yuan-ye-l2 is an edit of it"
assert not (LIVE / "set-xujia-yuan-ye-l2.png").exists(), "refs-live/set-xujia-yuan-ye-l2.png already exists; pick a new l-number"

SEEDS = (37009, 37010)
EMPTY = ("the place is completely empty: nobody anywhere, no person, no figure, no face, no statue, no silhouette, "
         "no shadow of a person and no animal anywhere in the picture")
BLANK_TEXT = ("nothing written, carved or painted anywhere: no characters, no calligraphy, no letters, no signs, no "
              "signboard, no plaque, no couplets, no banners, no posters, no paper notices, no scrolls")
NIGHT = "it is truly night: no daylight, no sunlight and no blue daytime sky anywhere"
NOPOLES = "no weapon rack, no spears, no poles, no sticks and no staffs leaning anywhere"
NOTHING_LEANS = "nothing leaning against any wall, fence, gate or tree"
NOFIRE = "no brazier, no fire bowl, no bonfire, no torch, no torch stand and no other lamp or flame"

old_lens = ("shot on a cinema camera with an 85mm lens, natural soft key light, realistic skin with fine pores and natural "
            "texture, realistic hair and fabric, shallow depth of field.")
assert st["STYLE"].startswith(st["ANCIENT"]) and old_lens in st["STYLE"], "screen-test.py's STYLE changed; update this script"
SET_STYLE = ("Ancient China, Song dynasty. " + st["STYLE"][len(st["ANCIENT"]):]
             .replace("for a Chinese historical costume drama", "of an empty location for a Chinese historical costume drama")
             .replace(old_lens, "shot on a cinema camera with a 24mm wide-angle lens at eye height, natural light, realistic "
                                "soil, thatch, wood, plaster and stone textures, deep focus, everything sharp from front to back."))

edit_rule = ("image 1 is a photograph of the place at sunrise: keep exactly its layout, the thatched house with its thatch "
             "roof, its dark doorway, its lattice window and the small plain board on its wall, the woodpile stacked in front "
             "of the house, the yard gate with its small tiled roof, the yard walls, the persimmon tree's trunk and branches, "
             "the wooden bucket, the two small pots and the flat stones by the wall, the stone well with its windlass, the "
             "packed-earth floor with its flagstones, the stream and far hills, and the camera position; change only the "
             "things described here. ")
yuan_ye_l2 = (
    "the same yard of a poor ancient Chinese Song-dynasty thatched farmhouse in late autumn at deep night near midnight, "
    "a real night photograph: (1) the sun and the sunrise are gone: the sky is black with thick dark clouds, at most a "
    "faint pale glow of a hidden moon behind the clouds at the upper right, no moon disc visible; (2) one plain white "
    "paper lantern, completely blank with no writing, hangs under the eaves at the right front corner of the house beside "
    "the gate and glows warm, the only real light: it lights the house wall, the woodpile, the gate and the near ground "
    "warm orange, and everything else falls off into deep blue-black darkness; the house door stays a dark doorway and "
    "the window is dark; (3) the wooden board with the long handle leaning against the yard wall at the right is gone "
    "completely, leaving only the bare wall and the ground there; (4) the persimmon tree keeps only about ten dark orange "
    "fruits, all high in its top branches, nothing hanging lower and no fruit lying on the roof; (5) beyond the wall the "
    "harvested fields of pale rice stubble are barely visible in the dark, no yellow flowers, no green crops, the stream "
    "a faint dull gleam; (6) the small board on the house wall stays completely blank plain dark wood; "
    f"{NOTHING_LEANS}; {NOPOLES}; {NOFIRE}; {EMPTY}; {NIGHT}; {BLANK_TEXT}")

body = edit_rule + st["PLACE"].format(desc=yuan_ye_l2)
for must in (EMPTY, BLANK_TEXT, NOPOLES, NOTHING_LEANS, NOFIRE, NIGHT, "the only real light", "no moon disc visible"):
    assert must in body, f"set-xujia-yuan-ye-l2: '{must[:40]}...' must be in the prompt"

NEG_SET = (st["NEG"] + ", people, person, crowd, figure, man, woman, child, silhouette, statue, mannequin, calligraphy, "
           "Chinese characters, inscription, couplet, banner, poster, signboard, plaque, writing, weapon rack, spear")
(out / "prompts" / "negative-night-yard.txt").write_text(
    NEG_SET + ", spear rack, red tassel, halberd, pole, poles, bundle of poles, leaning poles, sticks, staff, broom, rake, "
    "hoe, shovel, flag, brazier, fire bowl, bonfire, torch, torch stand, red lantern, second lantern, sparks, "
    "full moon, bright moon, moon disc, moonlit sky, sun, sunrise, daylight, sunlight, blue sky, daytime, bright sky, "
    "yellow flowers, rapeseed field, green crops, tiled house roof, cartoon, illustration, painting", encoding="utf-8")

pid = "set-xujia-yuan-ye-l2"
prompt = out / "prompts" / f"{pid}.txt"
prompt.write_text(body + " " + SET_STYLE, encoding="utf-8")
jobs = [{"id": f"{pid}-{s}", "reference_images": [str(day_l3)], "prompt_file": str(prompt),
         "negative_file": str(out / "prompts" / "negative-night-yard.txt"),
         "width": 1312, "height": 736, "seed": s, "latent": "empty"} for s in SEEDS]
summary = [{"picture": pid, "night": True, "seeds": list(SEEDS), "base": "edit of set-xujia-yuan-l3",
            "used_by": "set-xujia-yuan-ye-t1 in e911 s01-s35, e912 s01-s35, e913 s33-s34 (new preps only)"}]
(out / "yard-night.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / "yard-night-pictures.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "yard-night.json")
