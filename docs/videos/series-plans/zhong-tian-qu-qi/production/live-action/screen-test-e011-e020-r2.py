#!/usr/bin/env python3
"""screen-test-e011-e020-r2.py OUT_DIR : round 2 of the arc-2 screen test, three places only. NOT run; waits for the
owner's go-ahead to spend. Seeds 37003/37004 (round 1 used 37001/37002), 6 jobs, one manifest OUT_DIR/r2.json; prompts
go to OUT_DIR/prompts/<picture>-r2.txt beside round 1's, which this script leaves untouched.

Why each picture is redrawn (round 1 in OUT_DIR/out-b/, owner's picks in refs-live/README.md, 第 2 篇章):
- set-qianfu-houmen-ye: 37001 came out a close-up of two men with calligraphy on the wall behind them, 37002 a good
  empty alley with a man standing at the right. Now: the camera stands in the alley with a wide lens; the only door in
  the picture is the back gate; the left wall is solid with no doorway or niche that could read as a figure; no person,
  figure, statue or silhouette; walls bare and unmarked; the lantern blank.
- set-xuji-pu: both seeds drew a large signboard with calligraphy and side banners with writing (37002 also a man). Now
  the frame stops below the eaves so no signboard is in the picture at all; the only thing over the doorway is a plain
  red cloth draped along the lintel; no couplets, banners, papers or lanterns; the silk shop next door shows only its
  cloth, no signboard.
- set-gongpeng-ye: round 1 drew it from text on the grey canvas because the day shed was not yet picked. Now it is an
  edit of refs-live/set-gongpeng-l1.png (owner's pick, 37001), relit only: one nearly burnt-out candle on the table at
  the right is the only light, grey-blue pre-dawn sky in the opening at the upper right, no moon, no sun.
Two more changes against the round-1 failures, for these three pictures only:
- the style sentence is a wide-lens location photograph: screen-test.py's STYLE was written for portraits (85mm lens,
  skin pores, shallow depth of field, "every garment is ancient Chinese clothing") and 37001 of the back gate turned into
  a two-person close-up; SET_STYLE drops the skin, hair and garment words and the 85mm lens;
- the negative adds the things that came out: man, woman, silhouette, statue, calligraphy, Chinese characters, couplets,
  banners, posters, signboard (and moon / sunlight for the night pictures).
"""
import json
import re
import runpy
import shutil
import sys
import tempfile
from pathlib import Path

out = Path(sys.argv[1]); (out / "prompts").mkdir(parents=True, exist_ok=True); (out / "base").mkdir(exist_ok=True)
here = Path(__file__).resolve().parent
LIVE = here.parent / "assets" / "refs-live"
full = Path(tempfile.mkdtemp(prefix="st-full-"))  # screen-test.py writes its own round-1 manifests; keep them out of OUT_DIR
st = runpy.run_path(str(here / "screen-test.py"), run_name="screen_test_lib",
                    init_globals={"sys": type("S", (), {"argv": ["x", str(full)]})})
grey_s = out / "base" / "grey-set.png"
if not grey_s.is_file():
    shutil.copyfile(full / st["canvas"]("grey-set.png", 1312, 736), grey_s)
shutil.rmtree(full, ignore_errors=True)
day_shed = LIVE / "set-gongpeng-l1.png"
assert day_shed.is_file(), "refs-live/set-gongpeng-l1.png is missing; the night shed is an edit of the day shed"

SEEDS = (37003, 37004)
SONG = "a poor ancient Chinese Song-dynasty"
EMPTY = ("the place is completely empty: nobody anywhere, no person, no figure, no face, no statue, no silhouette, "
         "no shadow of a person and no animal anywhere in the picture")
BLANK_TEXT = ("nothing written, carved or painted anywhere: no characters, no calligraphy, no letters, no signs, no "
              "signboard, no plaque, no couplets, no banners, no posters, no paper notices, no scrolls")
NIGHT = "it is truly night: no daylight, no sunlight and no blue daytime sky anywhere"

old_lens = ("shot on a cinema camera with an 85mm lens, natural soft key light, realistic skin with fine pores and natural "
            "texture, realistic hair and fabric, shallow depth of field.")
assert st["STYLE"].startswith(st["ANCIENT"]) and old_lens in st["STYLE"], "screen-test.py's STYLE changed; update this script"
SET_STYLE = ("Ancient China, Song dynasty. " + st["STYLE"][len(st["ANCIENT"]):]
             .replace("for a Chinese historical costume drama", "of an empty location for a Chinese historical costume drama")
             .replace(old_lens, "shot on a cinema camera with a 24mm wide-angle lens at eye height, natural light, realistic "
                                "stone, plaster, wood and cloth textures, deep focus, everything sharp from front to back."))

houmen = (
    "a narrow alley behind a rich ancient Chinese Song-dynasty manor at deep night, seen with a wide lens from inside the "
    "alley at eye height: the alley paved with dark stone slabs; on the left a high solid plastered wall, smooth and bare, "
    "with no door, no window, no niche and no opening in it, running away to the mouth of the alley at the far left, which "
    "opens onto a dark empty street; on the right the manor's own high plastered wall with its back gate, the only door in "
    "the picture: two black wooden doors standing half open, plain, with nothing pasted or painted on them; through the gap "
    "between the doors a glimpse of the back courtyard: a round stone table and, under the eaves of a covered walkway, one "
    "plain paper lantern with nothing on it, glowing warm; the walls plain and unmarked on both sides, the same dull grey "
    "plaster from top to bottom; no moon, an overcast black sky; the lantern's glow spilling out through the gap of the "
    f"doors onto the alley stones is the only light, the rest of the alley dark and still; {EMPTY}; {NIGHT}; {BLANK_TEXT}")
xuji_pu = (
    "the open front of a small new shop on a stone-paved street of an ancient Chinese Song-dynasty county town on an early "
    "winter morning, seen straight on from the street at eye height and framed low: the top edge of the picture is the "
    "wooden lintel over the doorway, below the eaves, so no signboard is in the picture at all; a plain red cloth with "
    "nothing on it is draped along the lintel, solid red from end to end; the wooden door panels all taken down so the whole "
    "front stands open; inside, a wooden counter on the left with a tall stool behind it, two rows of empty wooden shelves "
    "along the right, a plain back door at the back, bare plank walls with nothing hung on them; no lanterns anywhere; at the "
    "right edge the open front of the silk shop next door, only bolts of plain coloured cloth hanging at its door, no "
    "signboard, no banner; the stone slabs in front white with frost; low clear early-winter sunlight from the right; "
    f"no shopkeeper, no customer; {EMPTY}; {BLANK_TEXT}")
gongpeng_ye = (
    "the same open-sided papermaking work shed, the same roof, posts, back wall, tubs, stone mortar, mats and table in the "
    "same places, now late at night just before dawn: on the old wooden table at the right one short candle almost burnt "
    "down to a stub, its small yellow flame the only light, a little warm glow on the tabletop and the nearest post; the "
    "two soaking tubs at the front left and the stone mortar in the middle dim and dark, deep shadows under the roof and "
    "along the back wall; through the opening at the upper right and above the back wall the sky a cold grey-blue just "
    "before dawn, no moon, no stars, no sun; no sunlight, no bright patches and no sharp sun shadows on the floor, the "
    f"walls or the roof beams; no lantern, no fire other than the one candle; {EMPTY}; {NIGHT}; {BLANK_TEXT}")
edit_rule = ("image 1 is a photograph of the place: keep exactly its layout, posts, tubs, mortar, table, roof, back wall, "
             "floor, plants and camera position; the only change is the light and time of day described here, so the whole "
             "picture becomes a dark night picture. ")

grey = str(grey_s)
PICTURES = [  # (picture id, prompt body, base, night?, first episode)
    ("set-qianfu-houmen-ye", st["BLANK"] + st["PLACE"].format(desc=houmen), grey, True, 18),
    ("set-xuji-pu", st["BLANK"] + st["PLACE"].format(desc=xuji_pu), grey, False, 20),
    ("set-gongpeng-ye", edit_rule + st["PLACE"].format(desc=gongpeng_ye), str(day_shed), True, 15),
]
for pid, body, _, night, _ in PICTURES:
    assert EMPTY in body and BLANK_TEXT in body, f"{pid}: the empty-place and nothing-written sentences must be in"
    if night:
        assert NIGHT in body and "no moon" in body and "only light" in body, \
            f"{pid}: a night picture must name its only light and rule out daylight and the moon"
    else:
        assert not re.search(r"\b(lanterns?|candles?)\b(?! anywhere)", body.replace("no lanterns", "")), f"{pid}: a day lantern"

NEG_SET = (st["NEG"] + ", people, person, crowd, figure, man, woman, child, silhouette, statue, mannequin, calligraphy, "
           "Chinese characters, inscription, couplet, banner, poster, signboard, plaque, writing")
(out / "prompts" / "negative-set-r2.txt").write_text(NEG_SET, encoding="utf-8")
(out / "prompts" / "negative-night-r2.txt").write_text(
    NEG_SET + ", daylight, sunlight, blue sky, daytime, bright sky, moon, sun", encoding="utf-8")

jobs, summary = [], []
for pid, body, base, night, ep in PICTURES:
    prompt = out / "prompts" / f"{pid}-r2.txt"
    prompt.write_text(body + " " + SET_STYLE, encoding="utf-8")
    neg = out / "prompts" / ("negative-night-r2.txt" if night else "negative-set-r2.txt")
    jobs += [{"id": f"{pid}-r2-{s}", "reference_images": [base], "prompt_file": str(prompt), "negative_file": str(neg),
              "width": 1312, "height": 736, "seed": s, "latent": "empty"} for s in SEEDS]
    summary.append({"picture": f"{pid}-l1", "first_episode": ep, "night": night, "seeds": list(SEEDS),
                    "base": "edit of set-gongpeng-l1" if base == str(day_shed) else "grey canvas"})
(out / "r2.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / "r2-pictures.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "r2.json")
