#!/usr/bin/env python3
"""screen-test-aling-loose.py OUT_DIR : one picture, A-ling with her hair let down (e917 s13 fix2), 2026-11-16.
NOT run here (no Colab in the writing session). Seeds 37027/37028, 2 jobs, one manifest OUT_DIR/aling-loose.json; prompts
in OUT_DIR/prompts/. The manifest is meant for ~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-aling-loose/.
Check before running:
    python3 -I .agents/skills/minimax-h3-colab/scripts/check_images_manifest.py OUT_DIR/aling-loose.json
(one warning is expected: the canvas is 3:4, 864x1152, the size of the angle picture itself, not the 16:9 set canvas.)

Why: in e917 s13 (A-ling just out of the fire, Xu Yan holding her forearm, a11 「阿令，簾子可以再做，你不行」) all three
drafts (d1 9171102, fix1 9171201/9171202) drew a high bun with a wooden pin on top of her head from the first frames to the
end, although the text asked for her hair let down: every A-ling picture has that bun (aling-portrait-l1, angles/aling-angle-a-l1,
angles/aling-angle-b-l1, looked at full size: a high knot on the crown, a pale wooden pin through it, the rest of the hair
hanging straight down her back), and the picture wins over the text (fix1 sent only aling-angle-a and still got the bun).
s12 and s14 around it came out with loose hair, so the cut jumps. The lesson of e016's ferry (r3) and e017's yard (r2,
README 第 16、17 集): a ONE-change edit of a good picture works, negative words alone do not remove a big thing. So this is an
edit of angles/aling-angle-a-l1 that keeps the face, the robe and sash, the grey studio backdrop, the light, the camera and
the pose, and changes only the hair: all of it hanging loose, parted in the middle, smooth over the top and back of the head,
two wet sections over the front of both shoulders to the chest, a few strands stuck to her cheek (fix1's s13 hair sentence).
The positive prompt is written only as what is there (bible 拍法 18); the bun, knot, pin and ornaments are in the negative
file.

The pick is filed as refs-live/angles/aling-loose-angle-a-l1.png: a new id, so nothing that maps A-ling's pictures changes
(pilot.py maps <id>-angle-a to the fixed path angles/<id>-angle-a-l1.png and its id pattern [a-z]+ cannot match
"aling-loose"; only sets take the newest l-version). colab/runs/e917-live/fix2 sends it in place of aling-angle-a-l1 for
s13 only (spec.json swap_pictures, absolute path); later episodes that need A-ling's hair down can swap it in the same way.
"""
import json
import sys
from pathlib import Path

out = Path(sys.argv[1]); (out / "prompts").mkdir(parents=True, exist_ok=True)
LIVE = Path(__file__).resolve().parent.parent / "assets" / "refs-live"
SEEDS = (37027, 37028)
PID, BASE, FIRST = "aling-loose-angle-a-l1", "angles/aling-angle-a-l1", "e917 s13"
W, H = 864, 1152  # the size of aling-angle-a-l1.png (3:4)

ONE = ("Image 1 is a photograph of a young woman: keep exactly everything in it - her face and every feature of it, her "
       "expression and her eyes looking to the left, her skin and make-up, the white cross-collared linen robe with "
       "its wide white sash tied at the waist, her pose and the three-quarter view of her, the camera position and the "
       "framing, the plain smooth grey studio backdrop and the soft even studio light. Change only one thing: her hair. All "
       "of her long glossy black hair hangs loose and long: a plain parting in the middle of her head, the hair lying flat "
       "and smooth over the top and the back of her head down to the nape, the round shape of her head clearly visible "
       "under the smooth hair, and from there every strand falls straight down in two wet sections, one over the front of "
       "each shoulder, down to her chest; the hair is wet and dark, clumped into long wet strands, and a few thin wet "
       "strands are stuck to her cheek. A real photograph, photorealistic live-action film portrait, natural skin texture, "
       "sharp focus, fills the whole frame edge to edge.")
NEG = ("3D render, CGI, game render, plastic, cartoon, anime, illustration, painting, text, writing, Chinese characters, "
       "watermark, logo, second person, extra people, black bars, border, bun, hair bun, double buns, hair knot, topknot, "
       "chignon, updo, high bun, ponytail, braid, tied-up hair, half-up hair, hairpin, hair stick, wooden pin, chopstick, "
       "hair ornament, hair clip, comb, ribbon, headband, hair band, crown, hat, veil, bangs, fringe, short hair, curly hair, "
       "fluffy dry hair")

src = LIVE / f"{BASE}.png"
assert src.is_file(), f"refs-live/{BASE}.png is missing; {PID} is an edit of it"
assert not (LIVE / "angles" / f"{PID}.png").exists(), f"refs-live/angles/{PID}.png already exists; pick a new l-number"
for bad in (" no ", " not ", "without", "never", "nobody", "nothing", " gone", " bun", " pin", "knot"):
    assert bad not in ONE.lower(), f"{PID}: the positive prompt has '{bad.strip()}' (write what is there)"
prompt = out / "prompts" / f"{PID}.txt"
prompt.write_text(ONE, encoding="utf-8")
neg = out / "prompts" / f"negative-{PID}.txt"
neg.write_text(NEG, encoding="utf-8")
jobs = [{"id": f"{PID}-{s}", "reference_images": [str(src)], "prompt_file": str(prompt), "negative_file": str(neg),
         "width": W, "height": H, "seed": s, "latent": "empty"} for s in SEEDS]
summary = [{"picture": PID, "file": f"refs-live/angles/{PID}.png", "seeds": list(SEEDS), "base": "edit of " + BASE,
            "first_shot": FIRST}]
(out / "aling-loose.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / "aling-loose-pictures.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "aling-loose.json")
