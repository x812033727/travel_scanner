#!/usr/bin/env python3
"""screen-test-e020.py OUT_DIR : the prop reference picture of Tang Xiaotang's small gold abacus (小金算盤) for e020 live
(colab/runs/e920-live). NOT run here (Colab Qwen-Image-Edit, paid). Seeds 37031/37032 (e019 used none; e017 37023/37024),
2 jobs, one manifest OUT_DIR/abacus.json; prompts in OUT_DIR/prompts/. The manifest is meant for
~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-e020/. Check before running:
    python3 -I .agents/skills/minimax-h3-colab/scripts/check_images_manifest.py OUT_DIR/abacus.json
The pick is filed as refs-live/prop-jinsuanpan-l1.png; colab/runs/e920-live/mkspec.py then puts it in the set slot of the two
abacus inserts s16 and s37, and prep920.sh moves those two shots from colab-jobs-wait.json into colab-jobs.json.

Why: the abacus is a story prop of e020 (it falls in s16 and again in s37, is hugged in s37b and carried into e021 c01) and
it has NO picture: the live portrait tangxiaotang-portrait-l1 has a gold knot ornament at her waist, not an abacus. The e917
lesson (the lantern frame with the copper plate came out in five shapes; "下次出現這個道具前先畫道具參考圖") and the e015
plough (words alone did not move it; a picture did) say: picture first.

The picture: a one-change edit (refs-live/README.md: Qwen edits work when they change one thing) of a free crop of the
shop picture set-xuji-pu-l1 (crop=448:252:0:400: the top of the long low dark wooden cabinet under the left-wall shelves,
the place the shots happen in), with ONE object added: the small gold abacus lying flat on the cabinet top, seen from a
little above, filling about a third of the width. The positive prompt says only what is there (bible 拍法 18); the things
to keep out are in the negative file.
"""
import json
import subprocess
import sys
from pathlib import Path

out = Path(sys.argv[1]); (out / "prompts").mkdir(parents=True, exist_ok=True)
LIVE = Path(__file__).resolve().parent.parent / "assets" / "refs-live"
SEEDS = (37031, 37032)
PID, BASE, CROP = "prop-jinsuanpan-l1", "set-xuji-pu-l1", "crop=448:252:0:400,scale=1312:736:flags=lanczos"

KEEP = ("image 1 is a photograph of a dark wooden shop cabinet: keep the cabinet, its top, its panelled front, the shelves "
        "and the wall behind it, the grey tiles and the light exactly as they are, and add only the one object described "
        "here. ")
DESC = ("Lying flat on the top of the long low dark wooden cabinet, in the middle of the frame and a little toward the "
        "front edge, seen from a little above, is one small gold abacus the size of a woman's palm: a thin flat rectangular "
        "frame of polished gold, five thin gold rods running across it, and on each rod a short row of small round gold "
        "beads, a thin gold crossbar dividing the beads into an upper row of one bead and a lower row of four on every rod; "
        "the gold warm and softly gleaming against the dark wood; it is the only object on the cabinet top.")
STYLE = ("Style: a photorealistic live-action photograph of a real prop on a film set of a Chinese historical costume drama, "
         "shot on a cinema camera, real polished gold and real dark wood, everything sharp; a clean natural film image that "
         "fills the whole frame edge to edge.")
NEG = ("3D render, CGI, game render, plastic, cartoon, anime, illustration, painting, text, writing, calligraphy, Chinese "
       "characters, letters, numbers, inscription, engraving, watermark, logo, border, people, person, hand, fingers, "
       "coins, silver, ingot, jewellery, necklace, knot, tassel, pendant, ribbon, box, book, paper, wooden abacus, large "
       "abacus, second abacus, two abacuses, broken frame, bent rods, scattered beads")

src = LIVE / f"{BASE}.png"
assert src.is_file(), f"refs-live/{BASE}.png is missing; {PID} is an edit of a crop of it"
assert not (LIVE / f"{PID}.png").exists(), f"refs-live/{PID}.png already exists; pick a new l-number"
base = out / f"{BASE}-cabinet.png"  # the free crop (not filed in refs-live: only the edit is)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", CROP, str(base)], check=True)
body = KEEP + DESC + " " + STYLE
for bad in (" no ", " not ", "without", "never", "nobody", "nothing", " gone"):
    assert bad not in body.lower(), f"{PID}: the positive prompt has '{bad.strip()}' (write what is there)"
prompt = out / "prompts" / f"{PID}.txt"
prompt.write_text(body, encoding="utf-8")
neg = out / "prompts" / f"negative-{PID}.txt"
neg.write_text(NEG, encoding="utf-8")
jobs = [{"id": f"{PID}-{s}", "reference_images": [str(base)], "prompt_file": str(prompt), "negative_file": str(neg),
         "width": 1312, "height": 736, "seed": s, "latent": "empty"} for s in SEEDS]
(out / "abacus.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / "abacus-pictures.json").write_text(json.dumps([{"picture": PID, "seeds": list(SEEDS), "base": f"edit of {BASE} {CROP}",
                                                       "first_shot": "e020 s16, s37 (inserts)"}], ensure_ascii=False, indent=1)
                                          + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "abacus.json")
