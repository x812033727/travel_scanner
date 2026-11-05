#!/usr/bin/env python3
"""preflight-prompts.py MANIFEST.json [MANIFEST.json ...] : read every prompt of a route-A manifest before it is paid for.

Each check is a mistake this season paid for at least once (lessons.md §11-§12):
- ERROR costume: the modern-suit picture with ancient-costume words in the text (e001-r2 s01-s02 drew the robe in the office);
- ERROR pictures: the header names a different number of <Picture N> than the job sends;
- warn prop: a prop baked into a base appearance (Erniu's carrying pole grew a jar on his back in e001-r2);
- warn shout: a quoted line of five characters or fewer ending in ！ (painted on screen as a subtitle, e053 s05);
- warn paper: a letter, note, scroll, notice or paper without blank / out of focus / folded shut / its back (fake text, e054-e056);
- warn collar: Tang Xiaotang in a close or medium shot without chin-up framing or the closed-garment sentence (e055 s39, e056 s27);
- warn unpictured: a character named in the composition with no picture of their own (e056 s21 drew a cartoon boy).
Exit 1 on any ERROR; warnings are for the reviewer to accept or fix before the batch.
"""
import json
import re
import sys
from pathlib import Path

ANCIENT = re.compile(r"(?<!no )(?<!no ancient clothing, no )\b(topknot|scholar's robe|cloth shoes|cross-collared|ruqun)", re.I)
PROP = re.compile(r"\b(carrying pole|a hoe\b|hoe or)", re.I)
SHOUT = re.compile(r"speaks a short Mandarin line, 「[^」]{1,5}！」")
PAPER = re.compile(r"\b(letter|note|scroll|notice|paper|résumé|document|ledger)\b", re.I)
PAPER_OK = re.compile(r"blank|out of focus|folded shut|its back|plain back|soft and blurred|edge-on|cannot be read|never seen|not readable|no stroke", re.I)
TANG_CLOSE = re.compile(r"(close-up|medium close-up|medium shot|two-shot)[^.]{0,120}Tang Xiaotang|Tang Xiaotang[^.]{0,60}(close-up|medium)", re.I)
TANG_OK = re.compile(r"chin up|from the chin|closed garment|one closed garment|no neckline", re.I)
NAMES = {"Xu Yan": "xuyan", "A-ling": "aling", "Qin Shuang": "qinshuang", "Tang Xiaotang": "tangxiaotang", "Xiaohe": "xiaohe",
         "Wang Erniu": "erniu", "Constable Zhao": "zhaobutou", "Qian Yuanwai": "qianyuanwai", "Leng Tie": "lengtie", "lookout boy": "shaonian"}


def check(manifest):
    root = Path(manifest).parent
    errors = warns = 0
    for job in json.loads(Path(manifest).read_text(encoding="utf-8"))["jobs"]:
        text = (root / job["prompt_file"]).read_text(encoding="utf-8")
        refs = [Path(r).name for r in job["reference_images"]]
        comp = text.split("Initial composition:", 1)[-1]
        found = []
        if any("-modern-" in r for r in refs) and ANCIENT.search(text):
            found.append(("ERROR", "costume", "modern-suit picture but the text describes the ancient costume"))
        m = re.search(r"For the target video, (.*?) (?:is|are) referenced throughout", text)
        if m and len(re.findall(r"<Picture \d+>", m.group(1))) != len(refs):
            found.append(("ERROR", "pictures", f"header names {len(re.findall(r'<Picture \\d+>', m.group(1)))}, job sends {len(refs)}"))
        if PROP.search(text):
            found.append(("warn", "prop", PROP.search(text).group(0)))
        if SHOUT.search(text):
            found.append(("warn", "shout", SHOUT.search(text).group(0)[-12:]))
        if PAPER.search(comp) and not PAPER_OK.search(comp):
            found.append(("warn", "paper", PAPER.search(comp).group(0)))
        if TANG_CLOSE.search(comp) and not TANG_OK.search(text):
            found.append(("warn", "collar", "Tang Xiaotang close/medium without chin-up framing or the closed-garment sentence"))
        for name, cid in NAMES.items():
            if re.search(rf"\b{name}\b(?! off screen)(?![^.]{{0,25}}off screen)", comp) and not any(r.startswith(cid + "-") for r in refs):
                found.append(("warn", "unpictured", name))
        for level, kind, what in found:
            print(f"{level:5} {job['id']:14} {kind:10} {what}")
            errors += level == "ERROR"
            warns += level == "warn"
    print(f"{manifest}: {errors} error(s), {warns} warning(s)")
    return errors


if __name__ == "__main__":
    sys.exit(1 if sum(check(m) for m in sys.argv[1:]) else 0)
