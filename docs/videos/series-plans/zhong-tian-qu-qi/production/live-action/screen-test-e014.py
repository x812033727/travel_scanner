#!/usr/bin/env python3
"""screen-test-e014.py OUT_DIR : the two references the e014 r2 review (writer-tools/e014-r2/review.md, 必改 1 and 建議 1)
asks to redraw before e014 is drafted; the coordinator decided both (2026-11-15). NOT run here (no Colab in the writing
session). Seeds 37007/37008 (e013 used 37005/37006), 4 jobs, one manifest OUT_DIR/e014.json; prompts in OUT_DIR/prompts/.
Check before running:
    python3 -I .agents/skills/minimax-h3-colab/scripts/check_images_manifest.py OUT_DIR/e014.json

- set-zhulin-fen-l3 (e014 s01-s09, and e013 s35-s42 if they are retaken): an edit of refs-live/set-zhulin-fen-l2
  (image 1), keeping its photographed dense night bamboo, the clearing and the camera position, with these changes: the
  metal fire bowl, its tall flames and the column of sparks go (Ref2VA copies "layout and props", and e912's drafts grew
  braziers even where no picture had one); the flat wooden board lying on the ground goes; one low earthen grave mound
  appears in the middle of the clearing (neither l2 seed drew it) with one short blank weathered plank stuck upright at its
  right front; the only fire is a small heap of paper offerings burning down on the bare ground in front of the mound.
- set-gongpeng-l2 (e014 s15-s42, and the base of a later night version for e015): an edit of refs-live/set-gongpeng-l1
  (image 1) that removes three things and keeps everything else, its light included: the dark wooden lattice grid lying
  on the floor (a second "bamboo mould" on the floor of the episode about the first one), the crossed sticks standing in
  the two vats, and the tied bundles of tall poles leaning at the far left (e911's spear racks grew in such places).
Same templates, style and negative words as screen-test-e013.py.
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
grove_l2 = LIVE / "set-zhulin-fen-l2.png"
shed_l1 = LIVE / "set-gongpeng-l1.png"
for f in (grove_l2, shed_l1):
    assert f.is_file(), f"refs-live/{f.name} is missing; the e014 pictures are edits of it"

SEEDS = (37007, 37008)
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

grove_rule = ("image 1 is a night photograph of the place: keep exactly its tall dense dark bamboo on both sides, the small "
              "clearing with its dry fallen bamboo leaves, the starry sky through the bamboo tops and the camera position; "
              "change only the things described here. ")
zhulin_l3 = (
    "the same small clearing deep inside a dense grove of tall living bamboo behind a poor ancient Chinese Song-dynasty "
    "village at night, a real night photograph: (1) the metal fire bowl in the middle, its tall flames and every rising spark "
    "are gone completely, no bowl, no basin, no brazier, no fire pit and no sparks anywhere; (2) the flat wooden board lying "
    "on the ground at the right is gone, there is only bare earth and fallen leaves there, no planks lying anywhere; (3) in "
    "the middle of the clearing, a little right of centre, one small low grave mound of bare packed brown earth, about knee "
    "high and about as long as a person, a few dry bamboo leaves on it; one short weathered wooden plank, knee high, stuck "
    "upright in the earth at the right front of the mound, its face completely blank plain grey wood; (4) in front of the "
    "mound, directly on the bare ground, one small low heap of plain paper offerings burning down, a few small flames and "
    "glowing embers no bigger than a washbasin, the only warm light, lighting the front of the mound, the plank and the "
    "nearest bamboo stalks orange; everywhere else cold faint blue starlight; no moon; nothing built anywhere: no building, "
    "no roof, no wall, no shrine, no tombstone, no lantern, no torch and no other light; "
    f"{NOPOLES}, only living bamboo growing straight up; {EMPTY}; {NIGHT}; {BLANK_TEXT}")
shed_rule = ("image 1 is a photograph of the place: keep exactly its thatch-and-timber roof and posts, the open right side, "
             "the low back and left walls, the tiled roofs and trees beyond them, the two big round wooden vats of milky white "
             "pulp, the squat stone mortar, the old wooden table at the right, the plants, the light and shadows and the "
             "camera position; change only the three things described here. ")
gongpeng_l2 = (
    "the same open-sided work shed of a poor ancient Chinese Song-dynasty farmhouse: (1) the dark wooden lattice grid lying "
    "on the floor is gone completely: the whole floor is plain packed earth, no mat, no grid, no lattice and no strips of "
    "wood lying anywhere on it; (2) the crossed sticks standing in the two vats are gone: the vats hold only the smooth milky "
    "white pulp, nothing standing in them; (3) the tied bundles of tall poles leaning at the far left are gone, leaving only "
    "the bare wall there; "
    f"{NOPOLES}; {EMPTY}; {BLANK_TEXT}")

grey = str(grey_s)
PICTURES = [  # (picture id, prompt body, base, night?, first shot)
    ("set-zhulin-fen-l3", grove_rule + st["PLACE"].format(desc=zhulin_l3), str(grove_l2), True, "e014 s01"),
    ("set-gongpeng-l2", shed_rule + st["PLACE"].format(desc=gongpeng_l2), str(shed_l1), False, "e014 s15"),
]
for pid, body, _, night, _ in PICTURES:
    assert EMPTY in body and BLANK_TEXT in body and NOPOLES in body, f"{pid}: the empty, nothing-written and no-poles sentences must be in"
    if night:
        assert NIGHT in body and "no moon" in body and "the only warm light" in body, \
            f"{pid}: a night picture must name its only light and rule out daylight and the moon"

NEG_SET = (st["NEG"] + ", people, person, crowd, figure, man, woman, child, silhouette, statue, mannequin, calligraphy, "
           "Chinese characters, inscription, couplet, banner, poster, signboard, plaque, writing, weapon rack, spear")
(out / "prompts" / "negative-set-e014.txt").write_text(
    NEG_SET + ", lattice, grid, mat on the floor, bamboo screen, sticks in the vats, poles, tripod", encoding="utf-8")
(out / "prompts" / "negative-night-e014.txt").write_text(
    NEG_SET + ", building, house, roof, temple, shrine, lantern, red lantern, tombstone, cartoon, illustration, painting, "
    "metal bowl, fire bowl, brazier, sparks, flying sparks, "
    "daylight, sunlight, blue sky, daytime, bright sky, moon, sun", encoding="utf-8")

jobs, summary = [], []
for pid, body, base, night, first in PICTURES:
    prompt = out / "prompts" / f"{pid}.txt"
    prompt.write_text(body + " " + SET_STYLE, encoding="utf-8")
    neg = out / "prompts" / ("negative-night-e014.txt" if night else "negative-set-e014.txt")
    jobs += [{"id": f"{pid}-{s}", "reference_images": [base], "prompt_file": str(prompt), "negative_file": str(neg),
              "width": 1312, "height": 736, "seed": s, "latent": "empty"} for s in SEEDS]
    summary.append({"picture": pid, "first_shot": first, "night": night, "seeds": list(SEEDS),
                    "base": "edit of " + Path(base).stem})
(out / "e014.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / "e014-pictures.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "e014.json")
