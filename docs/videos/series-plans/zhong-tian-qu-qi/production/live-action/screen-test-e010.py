#!/usr/bin/env python3
"""screen-test-e010.py OUT_DIR : the four live-action references e010 r2 needs, which have no live picture yet (NOT run;
waits for the owner's go-ahead to spend, two seeds each like e007-e009):
- huxianling: Magistrate Hu's head-and-shoulders portrait (new in the live version; s35, s37, s39);
- set-xujia-menwai: the village road outside the Xu yard gate at night (s22, s32-s40);
- set-xujia-zoulang-chen: the Xu corridor in the morning (s01-s06). Image 1 is e009's night corridor
  (set-xujia-zoulang-l1) mirrored left-right, so the doors stand on the left wall and the open end on the right as the
  e010 script has them; a set with no person and no cross collar may be mirrored (route-a.md, e004 s20). Only the light
  changes: night to early morning sun through the open house door;
- set-xujia-yuan-ye: the Xu yard at night (s19-s31). Image 1 is the yard every episode uses (set-xujia-yuan-l2, a sunny
  day with a yellow rape field beyond the fence: e909 s01 at night came out too bright with the field glowing); only the
  light changes, plus one blank lantern under the eaves.
Every place prompt says the place is empty of people (e009: the first two rounds of Tang Xiaotang's room drew a woman
sitting in it). Same templates, style, negative prompt, grey canvas and seeds as screen-test.py; writes OUT_DIR/e010.json.
The magistrate's costume words are the ones colab/runs/e910/extras.json puts into every shot of him."""
import json, re, runpy, subprocess, sys
from pathlib import Path
out = Path(sys.argv[1]); (out / "prompts").mkdir(parents=True, exist_ok=True); (out / "base").mkdir(exist_ok=True)
here = Path(__file__).resolve().parent
LIVE = here.parent / "assets" / "refs-live"
st = runpy.run_path(str(here / "screen-test.py"), run_name="screen_test_lib", init_globals={"sys": type("S", (), {"argv": ["x", str(out / "_full")]})})
# cast.json's "his cheeks shaking when he smiles" would put a smile on the portrait and on every shot of him
hu = st["appearance"]("huxianling").replace(
    "a black official gauze hat and a blue-green seventh-rank official robe with bulging sleeves, his cheeks shaking when he smiles",
    "an ancient Chinese Song-dynasty county magistrate's black gauze futou hat with two short stiff flat wings and a blue-green "
    "round-collared seventh-rank official robe with wide sleeves")
assert "smile" not in hu and "Song-dynasty" in hu, "cast.json's Magistrate Hu sentence changed; update screen-test-e010.py and extras.json"
EMPTY = "the place is completely empty: no person, no figure, no face and no animal anywhere in the picture"
menwai = ("the packed-earth village road just outside the bamboo fence and the plain shut wooden yard gate of a poor ancient Chinese "
          "Song-dynasty thatched farmhouse at night: the fence and the gate on the left, the low thatched roof of the farmhouse behind "
          "the fence, the road running away to the right between dark harvested fields toward a few dark village roofs; deep night with "
          "no moon, the sky black, lit only by warm flickering orange light coming in from beyond the right edge of the picture as if "
          "from torches out of sight; no torch, no lantern and no fire inside the picture; nothing written anywhere; " + EMPTY)
edit_rule = ("image 1 is a photograph of the place: keep exactly its layout, walls, doors, roof, floor, props and camera position; "
             "the only change is the light and time of day described here. ")
zoulang_chen = ("the same inside corridor of a poor ancient Chinese Song-dynasty farmhouse early in the morning: the plain wooden doors "
                "with no writing on them along the left-hand wall, the open end of the corridor on the right now an open house door "
                "with a sunlit packed-earth yard beyond its threshold; low warm early-morning sunlight streaming in through that "
                "doorway and slanting along the floor from the right, long soft shadows; no candle burning anywhere; " + EMPTY)
yuan_ye = ("the same yard of a poor ancient Chinese Song-dynasty thatched farmhouse at deep night near midnight: the moon hidden behind "
           "clouds, the sky black, the fields beyond the wall dark with no colour; one blank paper lantern with no writing hanging under "
           "the eaves of the house and glowing warm, the only light, the house door shut and every window dark; no daylight anywhere; "
           + EMPTY)


def mirrored(src, name):
    path = out / "base" / name
    if not path.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", "hflip", "-frames:v", "1", str(path)], check=True)
    return f"base/{name}"


items = [("huxianling", st["BLANK"] + st["HEAD"].format(desc=re.sub(st["FEET"], "", hu)), 864, 1152, st["canvas"]("grey-portrait.png", 864, 1152)),
         ("set-xujia-menwai", st["BLANK"] + st["PLACE"].format(desc=menwai), 1312, 736, st["canvas"]("grey-set.png", 1312, 736)),
         ("set-xujia-zoulang-chen", edit_rule + st["PLACE"].format(desc=zoulang_chen), 1312, 736,
          mirrored(LIVE / "set-xujia-zoulang-l1.png", "zoulang-l1-mirrored.png")),
         ("set-xujia-yuan-ye", edit_rule + st["PLACE"].format(desc=yuan_ye), 1312, 736, str(LIVE / "set-xujia-yuan-l2.png"))]
(out / "prompts" / "negative.txt").write_text(st["NEG"], encoding="utf-8")
(out / "prompts" / "negative-set.txt").write_text(st["NEG"] + ", people, person, crowd, figure", encoding="utf-8")  # sets only
jobs = []
for jid, body, w, h, base in items:
    (out / "prompts" / f"{jid}.txt").write_text(body + " " + st["STYLE"], encoding="utf-8")
    ref = base if base.startswith("/") else str(out / base)
    neg = "negative-set.txt" if jid.startswith("set-") else "negative.txt"
    jobs += [{"id": f"{jid}-{s}", "reference_images": [ref], "prompt_file": str(out / "prompts" / f"{jid}.txt"),
              "negative_file": str(out / "prompts" / neg), "width": w, "height": h, "seed": s, "latent": "empty"} for s in st["SEEDS"]]
(out / "e010.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "e010.json")
