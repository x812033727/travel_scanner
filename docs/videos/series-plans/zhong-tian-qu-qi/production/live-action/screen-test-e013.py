#!/usr/bin/env python3
"""screen-test-e013.py OUT_DIR : the two references the e013 r2 review (writer-tools/e013-r2/review.md, 必改 1 and 9) asks
to redraw before e013 is drafted. NOT run; waits for the owner's go-ahead to spend. Seeds 37005/37006 (the arc-2 rounds
used 37001-37004), 4 jobs, one manifest OUT_DIR/e013.json; prompts in OUT_DIR/prompts/. Check before running:
    python3 -I .agents/skills/minimax-h3-colab/scripts/check_images_manifest.py OUT_DIR/e013.json

- set-zhulin-fen-l2 (s35-s42): l1 (37002, arc-2 round 1) came out as an illustration, not a photograph, with a large
  hall right behind the grave, a plaque with fake characters, two red lanterns, a heap of round stones for the grave and a
  signboard on a tall post for the marker: the hall and lanterns are where the original e013's extra lantern-carrying
  figure came from, and a plaque grows characters. Drawn again from the grey canvas (not an edit of l1, whose cartoon look
  an edit would keep): a photographed night clearing in dense bamboo, nothing built anywhere, one low mound of bare earth,
  one small blank weathered plank, and the only warm light a small fire of paper offerings burning on the ground in front
  of the mound (the shots keep it: s36-s42 all have the paper fire), cold starlight otherwise, no moon.
- set-xujia-yuan-l3 (s01-s12): an edit of refs-live/set-xujia-yuan-l2 (image 1), keeping its layout, house, gate, well,
  bucket, board, woodpile and camera position, with four changes: the bundle of long poles leaning at the far left edge
  goes (e911's red-tasselled spear racks grew there), the yellow flowering fields beyond the wall become harvested stubble,
  the persimmon tree keeps only about ten fruits high in its top branches, and the light is a low early sunrise.
  set-xujia-yuan-ye-l1 (the night yard, screen-test-e010.py) is an edit of l2 and still has the poles: e013 only uses it
  in s33 (a door-gap view of the middle of the yard) and s34 (a close-up), so it is left as it is here; a night version
  without the poles would be one more edit of l3 once l3 is picked.
Same templates, style and negative words as screen-test-e011-e020-r2.py (a wide-lens location style, no skin or garment
words; the negative adds people, figures, statues, writing, signboards and plaques).
"""
import json
import runpy
import shutil
import sys
import tempfile
from pathlib import Path

out = Path(sys.argv[1]); (out / "prompts").mkdir(parents=True, exist_ok=True); (out / "base").mkdir(exist_ok=True)
here = Path(__file__).resolve().parent
LIVE = here.parent / "assets" / "refs-live"
full = Path(tempfile.mkdtemp(prefix="st-full-"))  # screen-test.py writes its own round-1 manifests; keep them out of OUT_DIR
# screen-test.py does its own `import sys` and writes its round-1 prompts and manifests under sys.argv[1], so the
# init_globals trick of screen-test-e011-e020-r2.py does not keep them out of OUT_DIR; point argv at the temp dir instead.
argv, sys.argv = sys.argv, ["screen-test.py", str(full)]
try:
    st = runpy.run_path(str(here / "screen-test.py"), run_name="screen_test_lib")
finally:
    sys.argv = argv
grey_s = out / "base" / "grey-set.png"
if not grey_s.is_file():
    shutil.copyfile(full / st["canvas"]("grey-set.png", 1312, 736), grey_s)
shutil.rmtree(full, ignore_errors=True)
day_yard = LIVE / "set-xujia-yuan-l2.png"
assert day_yard.is_file(), "refs-live/set-xujia-yuan-l2.png is missing; set-xujia-yuan-l3 is an edit of it"

SEEDS = (37005, 37006)
EMPTY = ("the place is completely empty: nobody anywhere, no person, no figure, no face, no statue, no silhouette, "
         "no shadow of a person and no animal anywhere in the picture")
BLANK_TEXT = ("nothing written, carved or painted anywhere: no characters, no calligraphy, no letters, no signs, no "
              "signboard, no plaque, no couplets, no banners, no posters, no paper notices, no scrolls")
NIGHT = "it is truly night: no daylight, no sunlight and no blue daytime sky anywhere"
NOPOLES = "no weapon rack, no spears, no poles, no sticks and no staffs leaning anywhere"

old_lens = ("shot on a cinema camera with an 85mm lens, natural soft key light, realistic skin with fine pores and natural "
            "texture, realistic hair and fabric, shallow depth of field.")
assert st["STYLE"].startswith(st["ANCIENT"]) and old_lens in st["STYLE"], "screen-test.py's STYLE changed; update this script"
SET_STYLE = ("Ancient China, Song dynasty. " + st["STYLE"][len(st["ANCIENT"]):]
             .replace("for a Chinese historical costume drama", "of an empty location for a Chinese historical costume drama")
             .replace(old_lens, "shot on a cinema camera with a 24mm wide-angle lens at eye height, natural light, realistic "
                                "soil, bamboo, wood, plaster and stone textures, deep focus, everything sharp from front to back."))

zhulin = (
    "a real night photograph of a small clearing deep inside a dense grove of tall living bamboo behind a poor ancient "
    "Chinese Song-dynasty village, seen at eye height with a wide lens: tall dark green bamboo stalks crowding in on both "
    "sides and closing in behind the clearing, nothing beyond them but more bamboo fading into black; a narrow dirt path "
    "coming in from the left; in the middle of the clearing, a little right of centre, one small low grave mound of bare "
    "packed brown earth, about knee high, with a few dry bamboo leaves on it; one short weathered wooden plank, knee high, "
    "stuck upright in the earth at the right front of the mound, its face completely blank and plain grey wood; dry fallen "
    "bamboo leaves all over the ground; in front of the mound on the ground one small fire of burning plain paper offerings, "
    "a few flames and glowing embers no bigger than a washbasin, the only warm light, lighting the front of the mound, the "
    "plank and the nearest bamboo stalks orange; everywhere else cold faint blue starlight from a sky full of stars seen "
    "through the bamboo tops; no moon; nothing built anywhere: no building, no roof, no wall, no gate, no shrine, no pavilion, "
    "no tombstone, no lantern, no torch and no other light; "
    f"{NOPOLES}, only living bamboo growing straight up; {EMPTY}; {NIGHT}; {BLANK_TEXT}")
edit_rule = ("image 1 is a photograph of the place: keep exactly its layout, the thatched house with its door, window and "
             "woodpile, the yard gate with its small tiled roof, the yard walls, the stone well with its windlass, the wooden "
             "bucket, the wooden board against the wall, the persimmon tree's trunk and branches, the packed-earth floor with "
             "its flagstones, and the camera position; change only the four things described here. ")
yuan_l3 = (
    "the same yard of a poor ancient Chinese Song-dynasty thatched farmhouse in late autumn at sunrise: (1) the bundle of "
    "long poles leaning against the house at the far left edge is gone completely, leaving only the bare mud wall and the "
    "ground there; (2) the fields beyond the yard wall are harvested: pale brown rice stubble and bare brown earth, the "
    "stream and the far hills as before, no yellow flowers and no green crops anywhere; (3) the persimmon tree has lost "
    "most of its leaves and keeps only about ten orange fruits, all high in its top branches, nothing hanging lower down and "
    "nothing on the lower branches; (4) early sunrise: low warm golden sunlight from the right, long shadows across the yard, "
    f"a pale cool morning sky, no midday light and no strong blue sky; {NOPOLES}; {EMPTY}; {BLANK_TEXT}")

grey = str(grey_s)
PICTURES = [  # (picture id, prompt body, base, night?, first shot)
    ("set-zhulin-fen-l2", st["BLANK"] + st["PLACE"].format(desc=zhulin), grey, True, "e013 s35"),
    ("set-xujia-yuan-l3", edit_rule + st["PLACE"].format(desc=yuan_l3), str(day_yard), False, "e013 s01"),
]
for pid, body, _, night, _ in PICTURES:
    assert EMPTY in body and BLANK_TEXT in body and NOPOLES in body, f"{pid}: the empty, nothing-written and no-poles sentences must be in"
    if night:
        assert NIGHT in body and "no moon" in body and "the only warm light" in body, \
            f"{pid}: a night picture must name its only light and rule out daylight and the moon"

NEG_SET = (st["NEG"] + ", people, person, crowd, figure, man, woman, child, silhouette, statue, mannequin, calligraphy, "
           "Chinese characters, inscription, couplet, banner, poster, signboard, plaque, writing, weapon rack, spear")
(out / "prompts" / "negative-set-e013.txt").write_text(
    NEG_SET + ", yellow flowers, rapeseed field, green crops, midday sun", encoding="utf-8")
(out / "prompts" / "negative-night-e013.txt").write_text(
    NEG_SET + ", building, house, roof, temple, shrine, lantern, red lantern, tombstone, cartoon, illustration, painting, "
    "daylight, sunlight, blue sky, daytime, bright sky, moon, sun", encoding="utf-8")

jobs, summary = [], []
for pid, body, base, night, first in PICTURES:
    prompt = out / "prompts" / f"{pid}.txt"
    prompt.write_text(body + " " + SET_STYLE, encoding="utf-8")
    neg = out / "prompts" / ("negative-night-e013.txt" if night else "negative-set-e013.txt")
    jobs += [{"id": f"{pid}-{s}", "reference_images": [base], "prompt_file": str(prompt), "negative_file": str(neg),
              "width": 1312, "height": 736, "seed": s, "latent": "empty"} for s in SEEDS]
    summary.append({"picture": pid, "first_shot": first, "night": night, "seeds": list(SEEDS),
                    "base": "edit of set-xujia-yuan-l2" if base == str(day_yard) else "grey canvas"})
(out / "e013.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / "e013-pictures.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "e013.json")
