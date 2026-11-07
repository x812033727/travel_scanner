#!/usr/bin/env python3
"""screen-test.py OUT_DIR : the live-action screen test of 種田娶妻打天下 (owner 2026-11-07: remake as live action).

Writes OUT_DIR/portraits.json, OUT_DIR/figures.json and OUT_DIR/sets.json (Qwen-Image-Edit manifests for `h3r.sh images`),
their prompts, and the blank grey canvases they send as image 1.

Image 1 is a blank mid-grey canvas that passes on nothing but the backdrop; the person, the costume and the style are all
in the text. This is how 《恁祖媽今年18》 drew its live-action portraits. The first run of this test sent the 3D CG
portraits as image 1 to keep the costumes, and every picture came out a CG doll again (2026-11-07): an edit keeps the
style of image 1 whatever the text says.
Lessons written into every prompt:
- the base look carries no props and a calm closed-mouth face (CG portraits that smiled or wore a knife put the smile
  and the knife into every shot, e002-e004 r2);
- the style sentence names the series look (live action) and the negative names the other one (3D CG, anime).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

PROD = Path(__file__).resolve().parent.parent
cast = json.loads((PROD / "cast.json").read_text(encoding="utf-8"))
out = Path(sys.argv[1])
(out / "prompts").mkdir(parents=True, exist_ok=True)
(out / "base").mkdir(exist_ok=True)
by_id = {c["id"]: c for c in cast["characters"]}

STYLE = ("Style: a photorealistic live-action photograph for a Chinese historical costume drama, shot on a cinema camera with "
         "an 85mm lens, natural soft key light, realistic skin with fine pores and natural texture, realistic hair and fabric, "
         "shallow depth of field. Not a painting, not 3D CG, not a game render, not anime, not a cartoon, not a doll. The "
         "picture fills the whole frame edge to edge: no black bars, no border. Clean image with nothing written anywhere, "
         "no watermark, no logo.")
NEG = ("3D render, CGI, game character, doll, plastic skin, airbrushed, cartoon, anime, illustration, painting, smiling, grin, "
       "smirk, teeth, laughing, open mouth, text, watermark, logo, extra fingers, deformed hands, nudity, see-through clothing, "
       "sheer fabric, knife, sword, weapon, black bars, border")
BLANK = "image 1 is only a blank mid-grey canvas: take nothing from it but the plain grey backdrop. "

# props are taken out of the base look; the shots that need them write them in
PROPS = [r",? an old chopping knife tucked in the belt", r",? hugging a small woven straw rabbit", r" with an iron ruler at his belt",
         r",? seated behind a long table in a glass meeting room, scrolling on her phone", r", always eyeing people sideways"]


def appearance(cid, look=None):
    c = by_id[cid]
    text = next(l["appearance"] for l in c.get("shot_looks", []) if l["id"] == look) if look else c["appearance"]
    for p in PROPS:
        text = re.sub(p, "", text)
    return text


# Tang Xiaotang: the owner accepts a low neckline (2026-11-07), so the test draws her cast.json stand collar and a
# Tang-dynasty high-waisted ruqun side by side for the owner to choose.
TANG_QIXIONG = re.sub(r"a fitted peach-pink silk brocade ruqun with a high stand-up mandarin collar.*?see-through",
                      "a peach-pink silk brocade Tang-dynasty high-waisted ruqun: a light cross-collared short jacket open in "
                      "a soft V over a chest-high skirt tied above the bust with a ribbon, showing her collarbones and a low "
                      "neckline, thick opaque silk", appearance("tangxiaotang"))
PORTRAITS = [  # (job id, description)
    ("xuyan", appearance("xuyan")),
    ("xuyan-modern", appearance("xuyan", "modern")),
    ("tangxiaotang", appearance("tangxiaotang")),
    ("tangxiaotang-qixiong", TANG_QIXIONG),
    ("qinshuang", appearance("qinshuang") + ", her belt plain and bare"),
    ("aling", appearance("aling")),
    ("xiaohe", appearance("xiaohe") + ", a plain, simply dressed village child"),
    ("erniu", appearance("erniu")),
    ("zhaobutou", appearance("zhaobutou")),
    ("qianyuanwai", appearance("qianyuanwai")),
    ("laisan", appearance("laisan")),
    ("mianshiguan", appearance("mianshiguan")),
]
# the owner wants all three heroines with good figures: a three-quarter-length look for each, so the figure reads
FIGURES = [
    ("tangxiaotang-figure", TANG_QIXIONG.replace("petite curvy figure", "a petite curvy hourglass figure with a slim waist")),
    ("qinshuang-figure", appearance("qinshuang").replace(
        "a fitted dark brown cotton short jacket crossed at the collar",
        "a fitted dark brown cotton short jacket wrapped in a deep V to the chest over a dark inner wrap") +
        ", a tall athletic hourglass figure, toned and curvy, with long legs, her belt plain and bare"),
    ("aling-figure", appearance("aling").replace(
        "a plain grey-white cotton dress tailored close at the waist with a cloth sash",
        "a plain grey-white cotton cross-collared dress, the collar crossing in a soft V to the chest, tailored close at "
        "the bust and waist with a pale cloth sash, a long flowing skirt") + ", a tall slender figure with graceful curves"),
]
SETS = {s["id"]: s["prompt"] for s in cast["sets"]}
SETS.update({  # sets that only gen-dh names
    "xujia-zao": "the small kitchen of the same poor thatched farmhouse: a clay brick stove with an iron wok and a low fire mouth, a stack of firewood, a water crock with a wooden lid, a wooden ladle on a hook, a doorway to the yard",
    "xianya": "the gate and front hall of a small ancient Chinese county yamen: grey brick walls, red wooden pillars, a big drum on a stand, stone steps, constables' racks by the door",
    "shiji": "a busy dirt market street in an ancient Chinese county town: wooden stalls under cloth awnings, baskets of vegetables and grain, bamboo poles, low tiled shops on both sides",
})
SET_IDS = ["xujia-yuan", "xujia-zao", "xianya", "xujia-wu", "liuxi-he", "shiji"]
SEEDS = (37001, 37002)


def canvas(name, w, h):
    path = out / "base" / name
    if not path.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x808080:s={w}x{h}", "-frames:v", "1",
                        str(path)], check=True)
    return f"base/{name}"


FEET = r",? (and )?(cloth shoes|black leather shoes|leather boots|boots|shoes)\b"  # named feet pull a head-and-shoulders frame out to full body (xuyan 37001/37002)


def jobs(items, frame, w, h, base):
    out_jobs = []
    for jid, desc in items:
        if frame is HEAD:
            desc = re.sub(FEET, "", desc)
        (out / "prompts" / f"{jid}.txt").write_text(BLANK + frame.format(desc=desc) + " " + STYLE, encoding="utf-8")
        out_jobs += [{"id": f"{jid}-{s}", "reference_images": [base], "prompt_file": f"prompts/{jid}.txt",
                      "negative_file": "prompts/negative.txt", "width": w, "height": h, "seed": s, "latent": "empty"}
                     for s in SEEDS]
    return out_jobs


(out / "prompts" / "negative.txt").write_text(NEG, encoding="utf-8")
grey_p, grey_s = canvas("grey-portrait.png", 864, 1152), canvas("grey-set.png", 1312, 736)
HEAD = ("A tight head-and-shoulders casting portrait: the frame ends just below the collarbones and the face fills the upper "
        "half of the frame, large and sharp. Front view, looking at the camera, calm neutral expression, mouth closed, not "
        "smiling. Plain mid-grey studio backdrop. Only the head, neck and shoulders are in the frame: no hands. The person "
        "is: {desc}. They are the only person in the frame.")
BODY = ("A three-quarter-length costume portrait from the top of the head to mid-thigh, standing in a relaxed elegant pose "
        "with her weight on one leg, facing the camera, so her figure and costume read clearly. Calm expression, mouth "
        "closed. Her hands rest at her sides, empty. Plain mid-grey studio backdrop with a soft rim light along her figure. "
        "She is: {desc}. She is the only person in the frame.")
PLACE = "A wide establishing photograph of a real location, empty of people: {desc}."
manifests = {"portraits": jobs(PORTRAITS, HEAD, 864, 1152, grey_p), "figures": jobs(FIGURES, BODY, 864, 1152, grey_p),
             "sets": jobs([(f"set-{s}", SETS[s]) for s in SET_IDS], PLACE, 1312, 736, grey_s)}
for name, js in manifests.items():
    (out / f"{name}.json").write_text(json.dumps({"jobs": js}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(", ".join(f"{len(v)} {k}" for k, v in manifests.items()), "->", out)
