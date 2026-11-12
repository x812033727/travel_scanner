#!/usr/bin/env python3
"""Till the Verdict Do Us Part, first batch of reference pictures (episodes 1-10): Qwen-Image-Edit manifests, no spending.

  art.py --list                                     every round, its image count, the picks it reads and an estimated CU
  art.py <round> [--pick key=a|b ...] [--work DIR] [--placeholders]
                                                    write <work>/<round>.json

Rounds (the owner approved this batch on 2026-11-12, cap 35 CU; each round <= 12 images):
  a1 a2      people, head-and-shoulders portraits on a grey canvas (build.py r1, 1248x1664), costume looks as latent image1
             edits of the locked portrait in ../assets/refs/, and Nora's first full-body pictures (1088x1920, image 1 the
             locked portrait, latent empty: art-plan-people.md 〈怎麼畫〉)
  a3         Bev, the installer lead, and Sienna's full body from the picked Sienna portrait (--pick sienna=a|b)
  a4         fixes after a1+a2 (drawn together as a12): Sienna's portrait and Nora's hospital gown redrawn, made-up lettering
             edited off the picked Dr. Brandt and deputy (--pick dr-brandt= deputy=); run before a3
  s1 s2 s3   sets used in episodes 1-10, vertical 1088x1920 on a grey canvas (vpilot.py set); s1 also edits the existing
             vertical morning bedroom (#1, vpilot set-bedroom-v-a) into its night version
  s4         「改自」 light/state versions, latent image1 on the picked bases (--pick liv-day= room-night= liv-gold-a= nur-day= mroom-night=)
  s5         「改自」 of the s4 versions (one seed each, so nothing to pick; run after s4 is accepted)
  s6         priority 3 sets of episodes 1-2 and 10: the owner may drop this round (--pick door-in-day= liv-day=)
  p1 p2      props marked P1/P2 that episodes 1-10 need, two seeds each (art-plan-props.md 共用的寫法)
  p3         the factory vase (ep. 1 TV ad) as an exactly-one-change edit of the picked No. 1 (--pick forever-no1=a|b)

Sources: ../cast.json (subject sentences of people: it wins over the plan's copy), ../art-plan-people.md (templates, order,
seeds from 714000), ../art-plan-sets.md and ../art-plan-props.md (prompts are read from their tables at build time, so a fix
in the plan reaches the next manifest). Two seeds per item; a 「改自」 set version gets one seed (art-plan-sets.md 估價).
Output names are <round>-<id>.png (the image tool turns "/" into "-"); a later round reads the picked take from the work dir.
Work dir defaults to $VIDEO_WORKDIR/_series/till-the-verdict/art (~/mokaair-work/videos/... when unset); --output-dir of
`h3.sh images` should be that same folder. Bases from ../assets/refs/ are copied into <work>/refs/.
Standard library only; run with python3 -I.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402  (same folder: REAL, BLANK, PORTRAIT_FRAME, NO_TEXT_SET, bust, job, write_png)

PROD = HERE.parent
REFS = PROD / "assets" / "refs"
SETS_PLAN = PROD / "art-plan-sets.md"
PROPS_PLAN = PROD / "art-plan-props.md"

BUST = (1248, 1664)
FULLV = (1088, 1920)
SETV = (1088, 1920)
WIDE = (1920, 1088)
CU_PER_IMAGE = 0.27
CANVAS = {BUST: "base/grey-portrait.png", FULLV: "base/grey-set-v.png", WIDE: "base/grey-set.png"}

# ---------------------------------------------------------------- people (art-plan-people.md)

# 〔LOOK〕〔FULL〕〔FACE1〕 of the plan; BLANK, PORTRAIT_FRAME (〔BUST〕) and REAL come from build.py word for word.
LOOK = ("Edit image 1: keep the face, skin, hairstyle unless this look changes it, the framing, the plain grey backdrop and the lighting "
        "exactly the same. Change only what differs in this look:")
LOOK_TAIL = "Calm neutral expression, mouth closed, not smiling; nothing in the hands."
FULL = ("A full-length casting photograph in a vertical frame: the whole figure from the top of the head to the soles of the shoes is in the frame, "
        "standing straight on a plain mid-grey studio floor, front view, looking at the camera, calm neutral expression, mouth closed, not smiling. "
        "Plain mid-grey seamless studio backdrop. Arms relaxed at the sides, both hands open and empty, holding nothing: no bag, no props. "
        "The face is clearly lit and sharp.")
FACE1 = ("Take only the face, identity, eyes, skin and age from image 1: exactly the same person. "
         "The hair, clothes and shoes are only as written here; take nothing else from image 1.")
# Words build.bust() misses that still pull a portrait to full length (plan 〈怎麼畫〉: 「外貌句刪」).
BUST_EXTRA = ("pants", "khakis", "forearms", "fingers", "wrist", "tool belt")

# Plan-documented edits of the cast.json sentence; the builder stops if the text it edits is gone from cast.json.
REWRITE = {
    # bust() would drop the whole uniform (the same clause names trousers): keep only the shirt.
    "deputy": [("a tan shirt and dark green trousers of a plain sheriff's deputy uniform", "a tan shirt of a plain sheriff's deputy uniform")],
    # a performance note, not a look: casting pictures are flat-faced (plan row night-coat).
    "nora:night-coat": [(", pain only in her face and posture", "")],
}

# Plan order (優先 P0, 第一次露臉說話的集 1-10); seeds 714000 + 2 x position + take, so they never move between rounds.
# kind: new = grey canvas bust; look = latent image1 edit of a refs portrait; full = first full body (image 1 the portrait,
# latent empty); full-pick = first full body from a portrait picked in an earlier round.
PEOPLE = [
    ("cole", "cole", None, "He", "new", None, "a1"),
    ("nora-night-coat", "nora", "night-coat", "She", "full", "nora-portrait.jpg", "a1"),
    ("nora-hospital", "nora", "hospital", "She", "look", "nora-portrait.jpg", "a1"),
    ("dr-brandt", "dr-brandt", None, "She", "new", None, "a1"),
    ("nurse-kim", "nurse-kim", None, "She", "new", None, "a1"),
    ("grant-rain", "grant", "rain", "He", "look", "grant-portrait.jpg", "a2"),
    ("on-call-doctor", "on-call-doctor", None, "He", "new", None, "a2"),
    ("nora-discharge", "nora", "discharge", "She", "full", "nora-portrait.jpg", "a2"),
    ("fisk", "fisk", None, "He", "new", None, "a2"),
    ("sienna", "sienna", None, "She", "new", None, "a2"),
    ("deputy", "deputy", None, "She", "new", None, "a2"),
    ("sienna-full", "sienna", None, "She", "full-pick", "sienna", "a3"),
    ("installer-lead", "installer-lead", None, "He", "new", None, "a3"),
    ("bev", "bev", None, "She", "new", None, "a3"),
]
# a4 (after looking at a1+a2, 2026-11-12): the a12 run drew Sienna with the full-body template and no face, and the
# hospital gown came out as V-neck pale blue scrubs (Nurse Kim's colour), so both are redrawn; cast.json now says a patient gown.
PEOPLE += [
    ("sienna", "sienna", None, "She", "new", None, "a4"),
    ("nora-hospital", "nora", "hospital", "She", "look", "nora-portrait.jpg", "a4"),
]
# One-change edits of a picked take that carries made-up lettering (a reference picture with letters teaches the clip to write).
FIX = ("Edit image 1: keep the face, hair, glasses, expression, clothes, framing, the plain grey backdrop and the lighting exactly the same. "
       "Change only one thing:")
FIXES = [
    ("dr-brandt", "the white doctor's coat is completely plain: no embroidered letters, no name, no logo and no pen on it, smooth plain white fabric where they were."),
    ("deputy", "the badge is a plain smooth gold six-pointed star with no letters, words or engraving; the shoulder patch is a plain dark green shield shape "
     "with no letters; the small name bar above the pocket is a blank plain brass bar. Nothing written anywhere."),
]
# Not drawn: the dispatcher (voice only, cast.json extras), the other installer (backs only), Nora `pregnant` full body
# (選 in the plan: the vertical pilot kept her face and shape from the portrait alone).


def load_cast() -> dict:
    cast = json.loads((PROD / "cast.json").read_text(encoding="utf-8"))
    who = {c["id"]: c["appearance"] for c in cast["characters"]}
    who.update({e["id"]: e["appearance"] for e in cast["extras"]})
    for c in cast["characters"]:
        for s in c.get("shot_looks", []):
            who[f"{c['id']}:{s['id']}"] = s["appearance"]
    return who


def appearance(cast: dict, pid: str, look: str | None) -> str:
    key = f"{pid}:{look}" if look else pid
    text = cast[key]
    for old, new in REWRITE.get(key, []):
        if old not in text:
            sys.exit(f"art.py: cast.json `{key}` no longer contains {old!r}; check art-plan-people.md and update REWRITE")
        text = text.replace(old, new)
    return text


def bust(text: str) -> str:
    keep = [p for p in re.split(r",\s*", build.bust(text)) if not any(re.search(rf"\b{w}\b", p) for w in BUST_EXTRA)]
    return ", ".join(keep)


# ---------------------------------------------------------------- sets (art-plan-sets.md)

SET_NEW = "image 1 is only a blank mid-grey canvas: take nothing from it. {p} Every sign, label, paper and screen is plain and blank. {real}"
SET_EDIT = ("Keep the style of image 1 and keep its room, camera position, layout and every object exactly as they are; "
            "change only the light, weather and the things described here: {p} {real}")
SET_ROUNDS = {
    "s1": [2, 5, 7, 9, 12, 14],
    "s2": [15, 16, 19, 20, 21, 24],
    "s3": [27, 28, 29, 30, 31, 32],
    "s4": [3, 6, 17, 18, 22, 25, 33],
    "s5": [23, 26],
    "s6": [8, 10, 11, 13, 34],
}
OPTIONAL = {"s6": "priority 3; the owner may drop it"}
# #1 (the morning bedroom) exists as the vertical pilot's take a: in assets/refs/ once copied there, else in the vpilot work dir.
BEDROOM = ["set-glass-house-bedroom.jpg", "set-glass-house-bedroom-bed-am.jpg", "set-bedroom-v-a.jpg"]


def table_rows(path: Path, first: str, cells: int) -> list[list[str]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(first, line):
            parts = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(parts) == cells:
                rows.append(parts)
    return rows


def load_sets() -> dict[int, dict]:
    out = {}
    for n, prio, sid, version, first, _uses, prompt, _layout, _round in table_rows(SETS_PLAN, r"^\| \d+ \|", 9):
        code = re.search(r"`([^`]+)`", version)
        base = re.search(r"改自 #(\d+)", version)
        ep = re.match(r"\d+", first)
        out[int(n)] = {"n": int(n), "prio": prio, "id": sid.strip("`"), "ver": code.group(1) if code else "", "prompt": prompt,
                       "base": int(base.group(1)) if base else None, "first": int(ep.group(0)) if ep else 999,
                       "exists": "已有" in version}
    return out


def set_takes(row: dict) -> tuple[str, ...]:
    return ("a",) if row["base"] else ("a", "b")


def set_job_id(row: dict, take: str) -> str:
    return f"set-{row['id']}-{row['ver']}-v-{take}"


def set_round_of(n: int) -> str | None:
    return next((r for r, ns in SET_ROUNDS.items() if n in ns), None)


def check_sets(sets: dict[int, dict]) -> None:
    """Every set version first used in episodes 1-10 (priority 1-3) is in exactly one round, after its base."""
    wanted = {n for n, r in sets.items() if r["first"] <= 10 and r["prio"] in {"1", "2", "3"} and not r["exists"]}
    listed = [n for ns in SET_ROUNDS.values() for n in ns]
    if sorted(listed) != sorted(wanted):
        sys.exit(f"art.py: SET_ROUNDS {sorted(listed)} != plan rows first used in episodes 1-10 {sorted(wanted)}")
    order = list(SET_ROUNDS)
    for n in listed:
        row = sets[n]
        if not row["ver"] or not row["prompt"]:
            sys.exit(f"art.py: art-plan-sets.md row #{n} has no version code or prompt")
        if row["base"] and row["base"] != 1 and order.index(set_round_of(row["base"])) >= order.index(set_round_of(n)):
            sys.exit(f"art.py: #{n} is drawn on #{row['base']}, which is not in an earlier round")


# ---------------------------------------------------------------- props (art-plan-props.md)

PROP_HEAD = ("Style: a photorealistic live-action photograph for a modern American prestige TV drama, a prop reference still shot on a cinema camera "
             "with a 50mm lens, soft even light, realistic materials and texture, the whole prop sharp. Not a painting, not 3D CG, not a cartoon. "
             "The picture fills the whole frame edge to edge: no black bars, no border.")
PROP_BLANK = "image 1 is only a blank canvas: take nothing from it but the plain backdrop."
PROP_TAIL = "The prop and the body parts named above are the only things in the frame."
PROP_TAIL_EMPTY = "Nobody is in the frame."
PROP_CLEAN = "Clean image with nothing written anywhere, no watermark, no logo, no signature."
# (id, size, round, base prop id for an exactly-one-change edit). Plan rounds 1-2 minus what first appears after episode 10
# (real-pill: 11); forever-vase (P1, ep. 1 on the TV ad) is an edit of forever-no1, so No. 1 is drawn here too.
# Left out: receipt (P2, ep. 5) is folded in episodes 5 and 9 and written as text; its picture is an edit of light-box (ep. 41).
PROPS = [
    ("half-pill", BUST, "p1", None),
    ("knit-hat", BUST, "p1", None),
    ("keepsake", BUST, "p1", None),
    ("nora-suitcase", BUST, "p1", None),
    ("peg-suitcase", BUST, "p1", None),
    ("forever-no1", BUST, "p1", None),
    ("grant-car", WIDE, "p2", None),
    ("black-car", WIDE, "p2", None),
    ("ledger", BUST, "p2", None),
    ("peg-ring", BUST, "p2", None),
    ("canvas-tote", BUST, "p2", None),
    ("camel-coat", BUST, "p2", None),
    ("forever-vase", BUST, "p3", "forever-no1"),
]


def load_props(cast_props: dict[str, str]) -> dict[str, dict]:
    rows = table_rows(PROPS_PLAN, r"^\| P\d \|", 7)
    out = {}
    for pos, (prio, pid, _why, _first, _uses, cell, _hands) in enumerate(rows):
        key = re.search(r"`([^`]+)`", pid).group(1)
        if key in out:
            continue  # furnace-no3 has three rows; none of them is in this batch
        prompts = re.findall(r"`([^`]+)`", cell)
        out[key] = {"prio": prio, "pos": pos, "prompt": max(prompts, key=len) if prompts else ""}
    for pid, _size, _round, _base in PROPS:
        row = out.get(pid)
        if not row or row["prio"] not in {"P1", "P2"} or not row["prompt"]:
            sys.exit(f"art.py: art-plan-props.md has no P1/P2 row with a prompt for `{pid}`")
        sentence = cast_props.get(pid)
        if sentence and sentence not in row["prompt"]:
            sys.exit(f"art.py: the plan's prompt for `{pid}` does not contain the cast.json prop sentence {sentence!r}; update the plan row")
    return out


# ---------------------------------------------------------------- rounds

def rounds() -> dict[str, dict]:
    """round -> {kind, items, images, picks}: everything --list prints, without touching the disk."""
    sets = load_sets()
    check_sets(sets)
    out: dict[str, dict] = {}
    for r in ("a1", "a2", "a3"):
        items = [p for p in PEOPLE if p[6] == r]
        picks = sorted({p[5] for p in items if p[4] == "full-pick"})
        out[r] = {"kind": "people", "items": [p[0] for p in items], "images": 2 * len(items), "picks": picks, "after": []}
    items = [p[0] for p in PEOPLE if p[6] == "a4"]
    out["a4"] = {"kind": "fix", "items": items + [f"{i} (fix)" for i, _ in FIXES], "images": 2 * (len(items) + len(FIXES)),
                 "picks": [i for i, _ in FIXES], "after": []}
    for r, ns in SET_ROUNDS.items():
        rows = [sets[n] for n in ns]
        picks = sorted({sets[row["base"]]["ver"] for row in rows if row["base"] and row["base"] != 1 and len(set_takes(sets[row["base"]])) > 1})
        after = sorted({set_round_of(row["base"]) for row in rows if row["base"] and row["base"] != 1 and len(set_takes(sets[row["base"]])) == 1})
        out[r] = {"kind": "sets", "items": [f"#{row['n']} {row['ver']}" for row in rows], "images": sum(len(set_takes(row)) for row in rows),
                  "picks": picks, "after": after, "rows": ns}
    for r in ("p1", "p2", "p3"):
        items = [p for p in PROPS if p[2] == r]
        out[r] = {"kind": "props", "items": [p[0] for p in items], "images": 2 * len(items), "picks": sorted({p[3] for p in items if p[3]}), "after": []}
    return out


def need(path: Path, size: tuple[int, int], placeholders: bool, hint: str) -> None:
    if path.is_file() and path.stat().st_size:
        # a grey stand-in from an earlier --placeholders run compresses to a few KB; a real picture is far larger
        if not placeholders and path.stat().st_size < 50_000:
            sys.exit(f"art.py: {path} looks like a placeholder from a dry run; delete it and draw the real picture first")
        return
    if not placeholders:
        sys.exit(f"art.py: {path} is missing; {hint} (or pass --placeholders for an offline check)")
    build.write_png(path, size, grey=96)
    print(f"placeholder: {path}")


def copy_ref(work: Path, name: str) -> str:
    src = REFS / name
    if not src.is_file():
        sys.exit(f"art.py: {src} is missing")
    (work / "refs").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, work / "refs" / name)
    return f"refs/{name}"


def picked(pick: dict[str, str], key: str) -> str:
    take = pick.get(key)
    if take not in {"a", "b"}:
        sys.exit(f"art.py: this round reads the owner's pick: pass --pick {key}=a or --pick {key}=b")
    return take


def people_round(name: str, work: Path, pick: dict[str, str], placeholders: bool) -> list[dict]:
    cast = load_cast()
    jobs = []
    for pos, (item, pid, look, pron, kind, src, r) in enumerate(PEOPLE):
        if r != name:
            continue
        text = appearance(cast, pid, look)
        if kind == "new":
            refs, size, latent = [CANVAS[BUST]], BUST, "empty"
            prompt = f"{build.BLANK} {build.PORTRAIT_FRAME}{pron} is: {bust(text)}. {pron} is the only person in the frame. {build.REAL}"
        elif kind == "look":
            refs, size, latent = [copy_ref(work, src)], BUST, "image1"
            prompt = f"{LOOK} {bust(text)}. {LOOK_TAIL} {pron} is the only person in the frame. {build.REAL}"
        else:
            if kind == "full":
                ref = copy_ref(work, src)
            else:
                ref = drawn(work, src, picked(pick, src), placeholders)
            refs, size, latent = [ref], FULLV, "empty"
            prompt = f"{FULL} {FACE1} {pron} is: {text}. {pron} is the only person in the frame. {build.REAL}"
        for t, take in enumerate(("a", "b")):
            jid = f"{item}-{take}"
            jobs.append(build.job(jid, f"{item} {take}", refs, prompt, size, 714000 + 2 * pos + t, f"{name}-{jid}.png", latent=latent))
    return jobs


def drawn(work: Path, item: str, take: str, placeholders: bool) -> str:
    """The picked take of a person from whichever people round drew it last (a4 redraws win; a12 was a1+a2 in one run)."""
    for r in ("a4", "a2", "a1", "a12"):
        name = f"{r}-{item}-{take}.png"
        if (work / name).is_file():
            need(work / name, BUST, placeholders, "")
            return name
    need(work / f"a4-{item}-{take}.png", BUST, placeholders, f"draw {item} first, or pick the other take with --pick {item}=")
    return f"a4-{item}-{take}.png"


def fix_round(work: Path, pick: dict[str, str], placeholders: bool) -> list[dict]:
    """a4: fixes after looking at a1+a2 (2026-11-12). Redraws come from PEOPLE; text edits change one thing on a picked take."""
    jobs = [j for j in people_round("a4", work, pick, placeholders)]
    for pos, (item, change) in enumerate(FIXES):
        ref = drawn(work, item, picked(pick, item), placeholders)
        prompt = f"{FIX} {change} {build.REAL}"
        for t, take in enumerate(("a", "b")):
            jid = f"{item}-fix-{take}"
            jobs.append(build.job(jid, f"{item} fix {take}", [ref], prompt, BUST, 715000 + 2 * pos + t, f"a4-{jid}.png", latent="image1"))
    return jobs


def bedroom_base(work: Path, placeholders: bool) -> str:
    dest = work / "refs" / "set-bedroom-v-a.png"
    for nm in BEDROOM:
        if (REFS / nm).is_file():
            return copy_ref(work, nm)
    vpilot = Path(os.environ.get("VIDEO_WORKDIR") or Path.home() / "mokaair-work" / "videos") / "_series" / "till-the-verdict" / "vpilot" / "set-bedroom-v-a.png"
    if vpilot.is_file():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(vpilot, dest)
    need(dest, SETV, placeholders, "copy the vertical pilot's set-bedroom-v-a (Drive _共用/製作檔/till-the-verdict/vpilot/) into assets/refs/ first")
    return "refs/set-bedroom-v-a.png"


def sets_round(name: str, work: Path, pick: dict[str, str], placeholders: bool) -> list[dict]:
    sets = load_sets()
    check_sets(sets)
    jobs = []
    for n in SET_ROUNDS[name]:
        row = sets[n]
        if row["base"] is None:
            refs, latent, tpl = [CANVAS[SETV]], "empty", SET_NEW
        else:
            base = sets[row["base"]]
            if row["base"] == 1:
                ref = bedroom_base(work, placeholders)
            else:
                takes = set_takes(base)
                take = takes[0] if len(takes) == 1 else picked(pick, base["ver"])
                ref = f"{set_round_of(base['n'])}-{set_job_id(base, take)}.png"
                need(work / ref, SETV, placeholders, f"draw round {set_round_of(base['n'])} first")
            refs, latent, tpl = [ref], "image1", SET_EDIT
        prompt = tpl.format(p=row["prompt"], real=build.REAL)
        for t, take in enumerate(set_takes(row)):
            jid = set_job_id(row, take)
            jobs.append(build.job(jid, f"#{n} {row['id']} {row['ver']} {take}", refs, prompt, SETV, 740000 + n * 10 + t, f"{name}-{jid}.png", latent=latent))
    return jobs


def props_round(name: str, work: Path, pick: dict[str, str], placeholders: bool) -> list[dict]:
    cast = json.loads((PROD / "cast.json").read_text(encoding="utf-8"))
    plan = load_props({p["id"]: p["prompt"] for p in cast["props"]})
    jobs = []
    for pid, size, r, base in PROPS:
        if r != name:
            continue
        body = plan[pid]["prompt"]
        # a car is a scene: the plan's prompt already opens with "Nobody is in the frame." (the tail's first sentence then goes)
        tail = "" if body.startswith(PROP_TAIL_EMPTY) else f"{PROP_TAIL} "
        if base:
            bsize = next(p[1] for p in PROPS if p[0] == base)
            ref = f"{next(p[2] for p in PROPS if p[0] == base)}-prop-{base}-{picked(pick, base)}.png"
            need(work / ref, bsize, placeholders, f"draw the round with {base} first")
            refs, latent = [ref], "image1"
            prompt = f"{PROP_HEAD} {body} {tail}{PROP_CLEAN}"
        else:
            refs, latent = [CANVAS[size]], "empty"
            prompt = f"{PROP_HEAD} {PROP_BLANK} {body} {tail}{PROP_CLEAN}"
        for t, take in enumerate(("a", "b")):
            jid = f"prop-{pid}-{take}"
            jobs.append(build.job(jid, f"{pid} {take}", refs, prompt, size, 760000 + plan[pid]["pos"] * 10 + t, f"{name}-{jid}.png", latent=latent))
    return jobs


def work_dir(flag: str | None) -> Path:
    if flag:
        return Path(flag).expanduser().resolve()
    return Path(os.environ.get("VIDEO_WORKDIR") or Path.home() / "mokaair-work" / "videos") / "_series" / "till-the-verdict" / "art"


def list_rounds() -> None:
    total = opt = 0
    print(f"{'round':6} {'images':>6} {'CU':>6}  items  [reads]")
    for r, info in rounds().items():
        reads = " ".join([f"--pick {k}=" for k in info["picks"]] + [f"after {a}" for a in info["after"]]) or "-"
        note = f"  [{OPTIONAL[r]}]" if r in OPTIONAL else ""
        print(f"{r:6} {info['images']:>6} {info['images'] * CU_PER_IMAGE:>6.2f}  {', '.join(info['items'])}  [{reads}]{note}")
        if r in OPTIONAL:
            opt += info["images"]
        else:
            total += info["images"]
    print(f"total  {total:>6} {total * CU_PER_IMAGE:>6.2f}  (without the optional rounds)")
    print(f"all    {total + opt:>6} {(total + opt) * CU_PER_IMAGE:>6.2f}  (with them; approved cap 35 CU)")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("round", nargs="?", choices=["a1", "a2", "a3", "a4", *SET_ROUNDS, "p1", "p2", "p3"])
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--work")
    ap.add_argument("--pick", action="append", default=[], help="key=a|b: a person, a set version code or a prop id, e.g. sienna=b, liv-day=a")
    ap.add_argument("--placeholders", action="store_true", help="grey stand-ins for picked takes that are not drawn yet (offline check)")
    a = ap.parse_args(argv)
    if a.list:
        list_rounds()
        return 0
    if not a.round:
        ap.error("give a round or --list")
    pick = dict(p.split("=", 1) for p in a.pick)
    work = work_dir(a.work)
    work.mkdir(parents=True, exist_ok=True)
    for size, rel in CANVAS.items():
        if not (work / rel).is_file():
            build.write_png(work / rel, size)
    kind = rounds()[a.round]["kind"]
    if kind == "fix":
        jobs = fix_round(work, pick, a.placeholders)
    else:
        jobs = {"people": people_round, "sets": sets_round, "props": props_round}[kind](a.round, work, pick, a.placeholders)
    if len(jobs) > 12:
        sys.exit(f"art.py: {a.round} has {len(jobs)} images; a round takes at most 12")
    out = work / f"{a.round}.json"
    out.write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{out}: {len(jobs)} jobs, about {len(jobs) * CU_PER_IMAGE:.2f} CU")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
