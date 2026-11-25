#!/usr/bin/env python3
"""screen-test-e015.py OUT_DIR : the three e015 pictures: set-gongpeng-ye-l2 (the work shed just before dawn, s01-s08),
set-qiutian-l2 (the autumn field before ploughing, s19-s26) and set-shiqiao-l2 (the stone bridge with room for the barrier,
s36-s42 and e016 s01). The coordinator decided them (2026-11-15; the last two after the independent review,
writer-tools/e015-r2/review.md 必改 2 and 3). NOT run here (no Colab in the writing session). Seeds 37011/37012 (e014 used
37007/37008, the night yard 37009/37010), 6 jobs, one manifest OUT_DIR/e015.json; prompts in OUT_DIR/prompts/.
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
there.

set-qiutian-l2 (review.md 必改 2): l1 is already ploughed all over (raised ridges with the stubble on their tops) under a
noon blue sky, so the scene's spectacle (three men scrape one short strip, then one woman turns a long furrow) cannot show.
An edit of l1 keeping the camera, the willow on the right-hand ridge, the farmhouses and the hills: the field flat and never
ploughed, short stubble in rows on firm dry earth, soft late-afternoon light from the left. The sunset shots after the
ploughing (s27-s30) do not send it (drop_set).
set-shiqiao-l2 (review.md 必改 3): l1 has a low plank footbridge on short posts across the water in the right foreground,
the same "long timber on short legs" shape as the barrier log the story needs, on the same side as Lai San; and its path
runs off along the left bank without reaching the bridge. An edit of l1 keeping the arch bridge, the bamboo, the far
houses and the misty light: the path comes from the left foreground to a small flat stone landing at the near foot of the
bridge, right of the middle, left clear for the barrier (the log and its trestles are written in each shot, so the
picture also serves e016 and later bridge scenes); open misty water with stones and reeds at the right, the footbridge gone.
Neither has an older episode to match (first used in e015). Same templates, style and negative words as screen-test-e014.py / screen-test-yard-night.py.
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

field_rule = ("image 1 is a photograph of the place: keep exactly the camera position, the big willow with yellow autumn leaves on "
              "the raised grass ridge along the right side, the low tiled farmhouses and the blue hills far off; change only the "
              "things described here. ")
qiutian_l2 = (
    "the same autumn rice field outside a poor ancient Chinese Song-dynasty village after the rice harvest, a real photograph: "
    "(1) the whole field is flat and level: hard, dry, dark earth that has never been ploughed, with no furrows, no ridges and "
    "no turned soil anywhere; short cut rice stubble stands in straight even rows on the flat ground, the soil between the "
    "rows flat, firm and finely cracked; (2) the light is soft warm late-afternoon sunlight slanting low from the left, long "
    "soft shadows of the stubble, a pale warm sky with a little haze, no harsh noon light; (3) the raised grass ridge along "
    "the right side stays a little higher than the field, bare grass along its top; "
    f"no plough, no tools, no carts, no animals; {NOPOLES}; {EMPTY}; {BLANK_TEXT}")
bridge_rule = ("image 1 is a photograph of the place: keep exactly the old grey stone arch bridge over the misty water, the green "
               "bamboo on both banks, the tiled houses on the far bank, the low cold golden morning sun at the upper right and the "
               "thin mist on the water; change only the things described here. ")
shiqiao_l2 = (
    "the same old stone arch bridge into an ancient Chinese Song-dynasty county town in the early morning, a real photograph, "
    "the camera standing on the near bank: (1) the stone-paved path runs from the left foreground straight to the near foot "
    "of the arch bridge, right of the middle, and ends on a small flat empty stone landing at the foot of the bridge, wide "
    "enough for a cart, with nothing standing on it; (2) the low plank footbridge on short posts across the water at the "
    "right is gone completely: on the right beyond the landing only open misty water, with round stones and green reeds "
    "along the bank; (3) the bridge's stone railings plain and unmarked; "
    f"{NOTHING_LEANS.replace('wall, post or vat', 'wall, railing or tree')}; {NOPOLES}; {EMPTY}; {BLANK_TEXT}")
DAY = [("set-qiutian-l2", field_rule + st["PLACE"].format(desc=qiutian_l2), LIVE / "set-qiutian-l1.png", "e015 s19"),
       ("set-shiqiao-l2", bridge_rule + st["PLACE"].format(desc=shiqiao_l2), LIVE / "set-shiqiao-l1.png", "e015 s36")]
for did, dbody, dbase, _ in DAY:
    assert dbase.is_file(), f"refs-live/{dbase.name} is missing; {did} is an edit of it"
    assert not (LIVE / f"{did}.png").exists(), f"refs-live/{did}.png already exists; pick a new l-number"
    for must in (EMPTY, BLANK_TEXT, NOPOLES):
        assert must in dbody, f"{did}: '{must[:40]}...' must be in the prompt"

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
(out / "prompts" / "negative-day-e015.txt").write_text(
    NEG_SET + ", plank footbridge, footbridge, boardwalk, jetty, second bridge, log barrier, furrows, ploughed rows, ridges of "
    "soil, plough, tractor, cart, cattle, harsh noon light, cartoon, illustration, painting", encoding="utf-8")
for did, dbody, dbase, first in DAY:
    dprompt = out / "prompts" / f"{did}.txt"
    dprompt.write_text(dbody + " " + SET_STYLE, encoding="utf-8")
    jobs += [{"id": f"{did}-{s}", "reference_images": [str(dbase)], "prompt_file": str(dprompt),
              "negative_file": str(out / "prompts" / "negative-day-e015.txt"),
              "width": 1312, "height": 736, "seed": s, "latent": "empty"} for s in SEEDS]
    summary.append({"picture": did, "night": False, "seeds": list(SEEDS), "base": "edit of " + dbase.stem, "first_shot": first})
(out / "e015.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / "e015-pictures.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "e015.json")
