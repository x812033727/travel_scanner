"""e043 stage-1 patch on top of ref2manifest.mjs output (run after it, before h3r check).

gen-dh has no id for the registrar (video.json speaker `shuli`), the proctor (`xunkao`) or the Wei
servant, so their shots get only the set picture and the faces turn cartoon (lessons.md §8, route-a §5).
This puts each one's portrait in front as <Picture 1>, renumbers the set, and pastes the portrait's
look into an anchor clause. Wide shots get a shoes line (bare feet, lessons §9).

    python3 -I patch_st1.py <st1-dir> <refs-dh-dir>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ST1, REFS = Path(sys.argv[1]), Path(sys.argv[2])
EXPR = ("Facial expressions follow the action and lines described below, not the reference pictures: "
        "the pictures fix the face, hair and costume only, never the mood.")
CAST = {
    "s15": ("registrar", "The registrar", "East Asian man of forty-five, sallow and thin with a long upper lip, a thin moustache and a small goatee, "
            "a tall black scholar's cap, a dark green clerk's robe with a white inner collar, a brush tucked behind one ear; "
            "realistic human proportions and a normal-sized nose and eyes"),
    "s17": None,  # same as s15, filled below
    "s21": ("weijiapu", "The stooping servant", "East Asian man of thirty-five, thin and slightly stooping, a narrow sallow clean-shaven face with a pointed chin, "
            "sly narrow eyes, a plain grey-green cotton servant's livery jacket with a crossed collar and a dark sash, "
            "a small black cloth cap over the bun on top of his head; realistic human proportions and a normal-sized nose and eyes"),
    "s27": ("xunkao", "The proctor", "East Asian man of forty-five, stocky and thick-necked, a heavy square jaw with short black stubble, "
            "small hard eyes under thick straight brows, a plain dark charcoal-grey official robe with a round collar, "
            "a soft black futou cap with two ribbons hanging at the back; realistic human proportions and a normal-sized nose and eyes"),
}
CAST["s17"] = CAST["s15"]
SHOES = {"s07", "s14", "s20", "s21", "s32"}
SHOES_LINE = "Every person in the frame wears dark cloth shoes on both feet."


def picture_list(n: int) -> str:
    names = [f"<Picture {i}>" for i in range(1, n + 1)]
    return names[0] if n == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def portrait(pid: str) -> Path:
    found = sorted(REFS.glob(f"{pid}-portrait-t*.png"))
    if not found:
        sys.exit(f"missing {pid}-portrait-t*.png in {REFS}")
    return found[-1]


for manifest in sorted(ST1.glob("ref-e043-part*.json")):
    data = json.loads(manifest.read_text(encoding="utf-8"))
    for job in data["jobs"]:
        sid = job["id"]
        if sid not in CAST and sid not in SHOES:
            continue
        pfile = ST1 / job["prompt_file"]
        text = pfile.read_text(encoding="utf-8")
        if sid in CAST and "patched-e043" not in job:
            pid, who, look = CAST[sid]
            n = len(job["reference_images"])
            if n > 1:  # mid-sentence after another character's anchor
                who = who[0].lower() + who[1:]
            n = len(job["reference_images"])  # the set is last; the new portrait goes right before it
            job["reference_images"] = job["reference_images"][:-1] + [str(portrait(pid))] + job["reference_images"][-1:]
            head = re.match(r"For the target video, (.+?) (is|are) referenced throughout\.", text)
            assert head, sid
            text = text.replace(head.group(0), f"For the target video, {picture_list(n + 1)} are referenced throughout.", 1)
            old_set = f"the location shown in <Picture {n}> is the set"
            assert old_set in text, (sid, old_set)
            text = text.replace(old_set, f"{who} shown in <Picture {n}> keeps exactly the same face, hair and costume as the picture: {look}; "
                                f"the location shown in <Picture {n + 1}> is the set", 1)
            if EXPR not in text:
                text = text.replace("no second copy of anyone appears.", "no second copy of anyone appears. " + EXPR, 1)
            job["patched-e043"] = pid
        if sid in SHOES and SHOES_LINE not in text:
            text = text.replace(" The camera ", f" {SHOES_LINE} The camera ", 1)
        pfile.write_text(text, encoding="utf-8")
        job["prompt_sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
        print(sid, "patched", [Path(p).name for p in job["reference_images"]])
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
