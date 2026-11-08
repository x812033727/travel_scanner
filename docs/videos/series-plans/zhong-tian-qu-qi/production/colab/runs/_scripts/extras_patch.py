"""Stage-1 patch for one episode, on top of ref2manifest.mjs output (generalises e043/patch_st1.py).

gen-dh only knows the main cast, so a supporting role (video.json `characters` id with no entry in
gen-dh's DH set: a registrar, a proctor, a runner) gets no portrait and turns cartoon (lessons §8).
For every shot whose `characters` holds such an id, this puts the role's portrait right before the
set picture, renumbers the set and pastes the role's look into an anchor clause. Wide shots
(camera starts with "Wide") get a shoes line (bare feet, lessons §9).

    python3 -I extras_patch.py <st1-dir> <refs-dh-dir> <video.json> <extras.json>

extras.json: {"<character id>": {"portrait": "<file stem in refs-dh>", "who": "The registrar", "look": "East Asian man ..."}}
"""
import hashlib
import json
import re
import sys
from pathlib import Path

st1, refs, video, extras = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), json.loads(Path(sys.argv[4]).read_text(encoding="utf-8"))
EXPR = ("Facial expressions follow the action and lines described below, not the reference pictures: "
        "the pictures fix the face, hair and costume only, never the mood.")
SHOES = "Every person in the frame wears dark cloth shoes on both feet."
scenes = {s["id"]: s for s in json.loads(video.read_text(encoding="utf-8"))["scenes"]}
# "_replace": {old: new} applied to every prompt (longest first); "_add_all": one sentence put before
# " The camera " in every shot whose prompt the replacements touched. e050: wine jars -> clay jars,
# because "wine jar" painted modern bottles in the e042 inn and the owner asked to avoid them.
REPL = extras.pop("_replace", {})
ADD_ALL = extras.pop("_add_all", "")


def header(n: int) -> str:
    if n == 1:
        return "For the target video, <Picture 1> is referenced throughout."
    names = [f"<Picture {i}>" for i in range(1, n + 1)]
    return f"For the target video, {', '.join(names[:-1])} and {names[-1]} are referenced throughout."


for manifest in sorted(st1.glob("ref-e*-part*.json")):
    data = json.loads(manifest.read_text(encoding="utf-8"))
    for job in data["jobs"]:
        sid, scene = job["id"], scenes[job["id"]]
        roles = [c for c in scene["data"].get("characters", []) if c in extras]
        wide = scene["data"].get("camera", "").lower().startswith("wide")
        pfile = st1 / job["prompt_file"]
        text = pfile.read_text(encoding="utf-8")
        touched = False
        for old in sorted(REPL, key=len, reverse=True):
            if old in text:
                text = text.replace(old, REPL[old]); touched = True
        if touched and ADD_ALL and ADD_ALL not in text and " The camera " in text:
            text = text.replace(" The camera ", f" {ADD_ALL} The camera ", 1)
        if not roles and not wide and not touched:
            continue
        done = set(job.get("extras_patched", []))
        for role in roles:
            if role in done:
                continue
            conf = extras[role]
            portrait = refs / f"{conf['portrait']}.png"
            if not portrait.is_file():
                sys.exit(f"{sid}: missing {portrait}")
            n = len(job["reference_images"])
            job["reference_images"] = job["reference_images"][:-1] + [str(portrait)] + job["reference_images"][-1:]
            text = re.sub(r"For the target video, .+? (is|are) referenced throughout\.", header(n + 1), text, count=1)
            old = f"the location shown in <Picture {n}> is the set"
            if old not in text:
                sys.exit(f"{sid}: no set clause {old!r}")
            who = conf["who"] if n == 1 else conf["who"][0].lower() + conf["who"][1:]
            text = text.replace(old, f"{who} shown in <Picture {n}> keeps exactly the same face, hair and costume as the picture: {conf['look']}; "
                                     f"the location shown in <Picture {n + 1}> is the set", 1)
            if EXPR not in text:
                text = text.replace("no second copy of anyone appears.", "no second copy of anyone appears. " + EXPR, 1)
            done.add(role)
        if wide and SHOES not in text and " The camera " in text:
            text = text.replace(" The camera ", f" {SHOES} The camera ", 1)
        pfile.write_text(text, encoding="utf-8")
        job["prompt_sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
        job["extras_patched"] = sorted(done)
        print(sid, "patched", roles, "wide" if wide else "", [Path(p).name for p in job["reference_images"]])
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
