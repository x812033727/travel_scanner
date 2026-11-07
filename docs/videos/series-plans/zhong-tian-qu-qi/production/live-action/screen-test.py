#!/usr/bin/env python3
"""screen-test.py OUT_DIR : the live-action screen test of 種田娶妻打天下 (owner 2026-11-07: remake as live action).

Writes OUT_DIR/portraits.json and OUT_DIR/sets.json (Qwen-Image-Edit manifests for `h3r.sh images`) and their prompts.
Each job sends the current 3D CG picture as image 1 so the costume, hairstyle and set layout carry over, and asks for
the series look in cast.json (`look.style`: photorealistic live action). Lessons written into every prompt:
- the base look carries no props and a calm closed-mouth face (CG portraits that smiled or wore a knife put the smile
  and the knife into every shot, e002-e004 r2);
- the prompt names the series look and puts the other look in the negative (a portrait edit that copied old wording
  drifted to the wrong style, 2026-11-07).
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROD = HERE.parent
REFS = PROD / "assets" / "refs-dh"
cast = json.loads((PROD / "cast.json").read_text(encoding="utf-8"))
out = Path(sys.argv[1])
(out / "prompts").mkdir(parents=True, exist_ok=True)
style = cast["look"]["style"]
by_id = {c["id"]: c for c in cast["characters"]}

# props are taken out of the base look; the shots that need them write them in
PROPS = [r",? an old chopping knife tucked in the belt", r",? hugging a small woven straw rabbit", r" with an iron ruler at his belt",
         r",? seated behind a long table in a glass meeting room, scrolling on her phone"]


def appearance(cid: str, look: str | None = None) -> str:
    c = by_id[cid]
    text = next(l["appearance"] for l in c.get("shot_looks", []) if l["id"] == look) if look else c["appearance"]
    for p in PROPS:
        text = re.sub(p, "", text)
    return text


EXTRA = {  # what image 1 must not pass on
    "qinshuang": "Her wide leather belt is plain and bare, the same belt with nothing tucked into it. ",
    "xiaohe": "A plain, simply dressed village child. ",
}

CHARS = [  # (job id, cast id, shot look, CG picture)
    ("xuyan", "xuyan", None, "xuyan-portrait-t2.png"),
    ("xuyan-modern", "xuyan", "modern", "xuyan-modern-t1.png"),
    ("tangxiaotang", "tangxiaotang", None, "tangxiaotang-portrait-t2.png"),
    ("qinshuang", "qinshuang", None, "qinshuang-portrait-t1.png"),
    ("aling", "aling", None, "aling-portrait-t1.png"),
    ("xiaohe", "xiaohe", None, "xiaohe-portrait-t1.png"),
    ("erniu", "erniu", None, "erniu-portrait-t1.png"),
    ("zhaobutou", "zhaobutou", None, "zhaobutou-portrait-t1.png"),
    ("qianyuanwai", "qianyuanwai", None, "qianyuanwai-portrait-t1.png"),
    ("laisan", "laisan", None, "laisan-portrait-t1.png"),
    ("mianshiguan", "mianshiguan", None, "mianshiguan-portrait-t1.png"),
]
SETS = {s["id"]: s["prompt"] for s in cast["sets"]}
SETS.update({  # sets that only gen-dh names
    "xujia-zao": "the small kitchen of the same poor thatched farmhouse: a clay brick stove with an iron wok and a low fire mouth, a stack of firewood, a water crock with a wooden lid, a wooden ladle on a hook, a doorway to the yard",
    "xianya": "the gate and front hall of a small ancient Chinese county yamen: grey brick walls, red wooden pillars, a big drum on a stand, stone steps, constables' racks by the door",
    "shiji": "a busy dirt market street in an ancient Chinese county town: wooden stalls under cloth awnings, baskets of vegetables and grain, bamboo poles, low tiled shops on both sides",
})
SET_PICS = ["xujia-yuan", "xujia-zao", "xianya", "xujia-wu", "liuxi-he", "shiji"]
NEG = "3D render, CGI, computer graphics, game character, doll, plastic skin, cartoon, anime, illustration, smiling, grin, smirk, teeth, laughing, open mouth, " + cast["look"]["negative"]
SEEDS = (35001, 35002)


def job(jid, pic, prompt, w, h, seed):
    (out / "prompts" / f"{jid}.txt").write_text(prompt, encoding="utf-8")
    return {"id": f"{jid}-{seed}", "reference_images": [str(REFS / pic)], "prompt_file": f"prompts/{jid}.txt",
            "negative_file": "prompts/negative.txt", "width": w, "height": h, "seed": seed, "latent": "empty"}


(out / "prompts" / "negative.txt").write_text(NEG, encoding="utf-8")
portraits = []
for jid, cid, look, pic in CHARS:
    p = (f"Re-create the person in image 1 as a real live-action actor photographed for a period drama: the same costume "
         f"design, colours, hairstyle and accessories as image 1, as a real person, not a 3D render. {appearance(cid, look)}. "
         f"{EXTRA.get(jid, '')}"
         f"Half-body portrait from the top of the head to the chest, a little space above the head, facing the camera. "
         f"Calm, neutral expression: mouth fully closed with level lips, the corners of the mouth level, eyes steady and "
         f"looking into the lens. Hands out of frame. Plain light-grey studio backdrop, soft even front light. {style}.")
    portraits += [job(jid, pic, p, 864, 1152, s) for s in SEEDS]
sets = []
for sid in SET_PICS:
    p = (f"Re-create image 1 as a real location photographed for a period drama, keeping the same layout, the same "
         f"objects in the same places and the same time of day, as a real place, not a 3D render: {SETS[sid]}. "
         f"Empty of people. {style}.")
    sets += [job(f"set-{sid}", f"set-{sid}-t1.png", p, 1312, 736, s) for s in SEEDS]
(out / "portraits.json").write_text(json.dumps({"jobs": portraits}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / "sets.json").write_text(json.dumps({"jobs": sets}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"{len(portraits)} portraits, {len(sets)} sets -> {out}")
