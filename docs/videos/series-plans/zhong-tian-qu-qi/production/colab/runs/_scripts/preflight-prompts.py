#!/usr/bin/env python3
"""preflight-prompts.py MANIFEST.json [MANIFEST.json ...] : read every prompt of a route-A manifest before it is paid for.

Each check is a mistake this season paid for at least once (lessons.md §11-§12):
- ERROR costume: the modern-suit picture with ancient-costume words in the text (e001-r2 s01-s02 drew the robe in the office);
- ERROR pictures: the header names a different number of <Picture N> than the job sends;
- warn prop: a prop baked into a base appearance (Erniu's carrying pole grew a jar on his back in e001-r2);
- warn shout: a quoted line of five characters or fewer ending in ！ (painted on screen as a subtitle, e053 s05);
- warn paper: a letter, note, scroll, notice or paper without blank / out of focus / folded shut / its back (fake text, e054-e056);
- warn collar: Tang Xiaotang in a close or medium shot without chin-up framing or the closed-garment sentence (e055 s39, e056 s27);
- warn unpictured: a character named in the composition with no picture of their own (e056 s21 drew a cartoon boy);
- warn crowd: a crowd, guards, riders or thugs with no dynasty clothing written (e055 s11 drew modern green uniforms);
- warn wine: wine bottles, wine cups or wine jars named (the e050 inn grew modern glass bottles; write pottery cups and clay jars);
- warn insert: an insert or extreme close-up that does not open directly on itself (opens on the empty set, e054 s03, e056 s04);
- warn skin: small bits written onto skin (wood chips on his hands came out as dark specks stuck to the skin, e003-r2 s06);
- warn smile: Tang Xiaotang "unsmiling" with no other expression written (she smiled anyway in both drafts, e005-r2 s39);
- warn glow: a blue glow "from the empty air" or "no panel drawn" outside an eye extreme close-up (the model drew a glowing panel with fake text, e004-r2 s03).
Exit 1 on any ERROR; warnings are for the reviewer to accept or fix before the batch.
"""
import json
import re
import sys
from pathlib import Path

ANCIENT = re.compile(r"(?<!no )(?<!no ancient clothing, no )\b(topknot|scholar's robe|cloth shoes|cross-collared|ruqun)", re.I)
PROP = re.compile(r"\b(carrying pole|a hoe\b|hoe or)", re.I)
SHOUT = re.compile(r"speaks a short Mandarin line, 「[^」]{1,5}！」")
PAPER = re.compile(r"\b(letter|note|scroll|notice|paper|résumé|document|ledger|signboard|plaque|banner with)\b", re.I)
PAPER_OK = re.compile(r"blank|out of focus|folded shut|its back|plain back|soft and blurred|edge-on|cannot be read|never seen|not readable|no stroke", re.I)
TANG_CLOSE = re.compile(r"(close-up|medium close-up|medium shot|two-shot)[^.]{0,120}Tang Xiaotang|Tang Xiaotang[^.]{0,60}(close-up|medium)", re.I)
TANG_OK = re.compile(r"chin up|from the chin|closed garment|one closed garment|no neckline", re.I)
CROWD = re.compile(r"\b(villagers|crowd|guards|soldiers|riders|horsemen|thugs|henchmen|assassins|youths|constables|runners|troops)\b", re.I)
CROWD_OK = re.compile(r"Song-dynasty|cross-collared|round-collared|futou|head-wraps?|ancient Chinese", re.I)
WINE = re.compile(r"\bwine (bottle|cup|jar|glass)s?\b|\bbottles?\b", re.I)
SKIN = re.compile(r"\b(wood chips|wood shavings|sawdust|splinters|specks?|flecks?|spots of (?:mud|dirt|blood|ash|soot)|mud spots|blood drops|drops of blood|soot marks?|smudges? of (?:dirt|soot|ash))\b[^.;]{0,40}\b(hands?|face|cheeks?|skin|arms?|forehead|knuckles|fingers)\b|\b(hands?|face|cheeks?|skin|arms?|forehead|knuckles|fingers)\b[^.;]{0,40}\b(wood chips|wood shavings|sawdust|splinters|specks|flecks|mud spots|blood drops|soot)\b", re.I)
GLOW = re.compile(r"glow from the empty air|no panel|panel drawn|glowing (?:screen|panel|window)|blue (?:glow|light) (?:from|in front of) (?:the )?(?:empty )?air", re.I)
SMILE_OK = re.compile(r"alarm|worr|fright|fear|anger|angry|furious|cold|stern|tears|crying|pale|shock|tense|frown", re.I)
INSERT = re.compile(r"^\s*(insert|extreme close-up)", re.I)
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
        if CROWD.search(comp) and not CROWD_OK.search(text):
            found.append(("warn", "crowd", CROWD.search(comp).group(0)))
        if WINE.search(text):
            found.append(("warn", "wine", WINE.search(text).group(0)))
        if SKIN.search(text):
            found.append(("warn", "skin", SKIN.search(text).group(0)[:60]))
        if GLOW.search(comp) and not re.search(r"extreme close-up of [^.]{0,30}eyes", comp, re.I):
            found.append(("warn", "glow", GLOW.search(comp).group(0)))
        if re.search(r"Tang Xiaotang[^.]{0,300}\bunsmiling\b", comp) and not SMILE_OK.search(comp):
            found.append(("warn", "smile", "Tang Xiaotang unsmiling with no other expression"))
        body = comp.split(":", 1)[-1]
        if INSERT.search(body) and "opens directly" not in text:
            found.append(("warn", "insert", "insert without 'opens directly on this ... from its very first frame'"))
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
