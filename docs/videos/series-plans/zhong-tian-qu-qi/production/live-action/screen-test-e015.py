#!/usr/bin/env python3
"""screen-test-e015.py OUT_DIR : set-gongpeng-ye-l2, the work shed just before dawn, for e015 s01-s08. The coordinator decided
it (2026-11-15, writer-tools/e015-r2/r2.py). NOT run here (no Colab in the writing session). Seeds 37011/37012 (e014 used
37007/37008, the night yard 37009/37010), 2 jobs, one manifest OUT_DIR/e015.json; prompts in OUT_DIR/prompts/.
Check before running:
    python3 -I .agents/skills/minimax-h3-colab/scripts/check_images_manifest.py OUT_DIR/e015.json

Why: the night shed in refs-live, set-gongpeng-ye-l1 (screen-test-e011-e020-r2.py), is a relight of the OLD day shed l1, so it
still has what the e014 review took out of the day shed in l2 (screen-test-e014.py): the dark wooden lattice grid lying on
the floor (a second bamboo mould on the floor of the episode about the first hundred sheets), the crossed sticks standing in
the vats and the tied A-frames of tall poles leaning at the far left (e911's spear racks grew in such places). e015's whole
first scene (8 shots, s01-s08) is in this shed before dawn, so the night picture is redrawn as an edit of the day shed
set-gongpeng-l2 (image 1), keeping its layout and camera position, with:
- the light: deep night just before dawn, one short candle burnt down almost to a stub on the old table at the right as the
  only warm light, the open right side and the sky above the back wall cold grey-blue, no sun, no moon;
- the two tall A-frames of poles still leaning at the far left in l2 and the one stirring stick left in a vat go too, leaving
  the bare wall and smooth pulp (l2 kept them, README: "桶裡還有一根攪棒");
- nothing else added: the paper stack, the pinned sheet and the mould are written in each shot (a picture with paper in it
  grows writing).
pilot.py takes the newest l-version of a set, so a pick saved as refs-live/set-gongpeng-ye-l2.png is used by every new live
prep that names dh-set-gongpeng-ye-t1 ("night work shed" in gen-dh.mjs SET, added for e015); prep915.sh stops until it is
there. Same templates, style and negative words as screen-test-e014.py / screen-test-yard-night.py.
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
# the temp dir (as screen-test-e013.py, screen-test-e014.py and screen-test-yard-night.py do).
argv, sys.argv = sys.argv, ["screen-test.py", str(full)]
try:
    st = runpy.run_path(str(here / "screen-test.py"), run_name="screen_test_lib")
finally:
    sys.argv = argv
shutil.rmtree(full, ignore_errors=True)
day_l2 = LIVE / "set-gongpeng-l2.png"
assert day_l2.is_file(), "refs-live/set-gongpeng-l2.png is missing; set-gongpeng-ye-l2 is an edit of it"
assert not (LIVE / "set-gongpeng-ye-l2.png").exists(), "refs-live/set-gongpeng-ye-l2.png already exists; pick a new l-number"

SEEDS = (37011, 37012)
EMPTY = ("the place is completely empty: nobody anywhere, no person, no figure, no face, no statue, no silhouette, "
         "no shadow of a person and no animal anywhere in the picture")
BLANK_TEXT = ("nothing written, carved or painted anywhere: no characters, no calligraphy, no letters, no signs, no "
              "signboard, no plaque, no couplets, no banners, no posters, no paper notices, no scrolls")
NIGHT = "it is truly night: no daylight, no sunlight and no blue daytime sky anywhere"
NOPOLES = "no weapon rack, no spears, no poles, no sticks and no staffs leaning anywhere"
NOTHING_LEANS = "nothing leaning against any wall, post or vat"
NOFIRE = "no brazier, no fire bowl, no lantern, no torch and no other lamp or flame than the one candle"

old_lens = ("shot on a cinema camera with an 85mm lens, natural soft key light, realistic skin with fine pores and natural "
            "texture, realistic hair and fabric, shallow depth of field.")
assert st["STYLE"].startswith(st["ANCIENT"]) and old_lens in st["STYLE"], "screen-test.py's STYLE changed; update this script"
SET_STYLE = ("Ancient China, Song dynasty. " + st["STYLE"][len(st["ANCIENT"]):]
             .replace("for a Chinese historical costume drama", "of an empty location for a Chinese historical costume drama")
             .replace(old_lens, "shot on a cinema camera with a 24mm wide-angle lens at eye height, natural light, realistic "
                                "soil, thatch, wood, plaster and stone textures, deep focus, everything sharp from front to back."))

edit_rule = ("image 1 is a photograph of the place by day: keep exactly its layout, the timber roof and posts, the open right "
             "side, the low back and left walls, the tiled roofs and trees beyond them, the two big round wooden vats of milky "
             "white pulp at the front left, the squat stone mortar in the middle, the old wooden table at the right, the plants "
             "and the camera position; change only the things described here, so the whole picture becomes a dark night "
             "picture. ")
gongpeng_ye_l2 = (
    "the same open-sided papermaking work shed of a poor ancient Chinese Song-dynasty farmhouse, late at night just before "
    "dawn, a real night photograph: (1) the sunlight and every sun patch and sharp sun shadow are gone; (2) on the old wooden "
    "table at the right one short white candle burnt down almost to a stub stands in a small plain clay dish, its small "
    "yellow flame the only warm light: a little warm glow on the tabletop, the nearest post and the floor beside the table, "
    "everything else falling off into deep blue-black shadow under the roof; (3) through the open right side and above the "
    "back wall the sky is a cold grey-blue just before dawn, the roofs and trees beyond the wall dark shapes against it, no "
    "moon, no stars, no sun; (4) the tall wooden A-frames of poles leaning at the far left are gone completely, leaving only "
    "the bare earthen wall there; (5) the stick standing in the vat is gone: both vats hold only smooth milky white pulp, "
    "dim in the dark; (6) the floor stays plain packed earth, smooth and empty; "
    f"{NOTHING_LEANS}; {NOPOLES}; {NOFIRE}; {EMPTY}; {NIGHT}; {BLANK_TEXT}")
body = edit_rule + st["PLACE"].format(desc=gongpeng_ye_l2)
for must in (EMPTY, BLANK_TEXT, NOPOLES, NOTHING_LEANS, NOFIRE, NIGHT, "the only warm light", "no moon"):
    assert must in body, f"set-gongpeng-ye-l2: '{must[:40]}...' must be in the prompt"

NEG_SET = (st["NEG"] + ", people, person, crowd, figure, man, woman, child, silhouette, statue, mannequin, calligraphy, "
           "Chinese characters, inscription, couplet, banner, poster, signboard, plaque, writing, weapon rack, spear")
(out / "prompts" / "negative-night-shed.txt").write_text(
    NEG_SET + ", lattice, grid, mat on the floor, bamboo screen, sticks in the vats, poles, tripod, A-frame, bundle of poles, "
    "leaning poles, staff, brazier, fire bowl, lantern, red lantern, torch, second candle, oil lamp, sparks, "
    "moon, full moon, sun, sunrise, daylight, sunlight, blue sky, daytime, bright sky, sun patches, "
    "cartoon, illustration, painting", encoding="utf-8")
pid = "set-gongpeng-ye-l2"
prompt = out / "prompts" / f"{pid}.txt"
prompt.write_text(body + " " + SET_STYLE, encoding="utf-8")
jobs = [{"id": f"{pid}-{s}", "reference_images": [str(day_l2)], "prompt_file": str(prompt),
         "negative_file": str(out / "prompts" / "negative-night-shed.txt"),
         "width": 1312, "height": 736, "seed": s, "latent": "empty"} for s in SEEDS]
summary = [{"picture": pid, "night": True, "seeds": list(SEEDS), "base": "edit of set-gongpeng-l2",
            "first_shot": "e015 s01", "used_by": "dh-set-gongpeng-ye-t1 ('night work shed') in e015 s01-s08"}]
(out / "e015.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / "e015-pictures.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "e015.json")
