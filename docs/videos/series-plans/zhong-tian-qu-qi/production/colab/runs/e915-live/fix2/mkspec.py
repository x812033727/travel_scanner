"""e915 fix2: the curved-beam plough (曲轅犁), after both cut reviews (cut-review.md 嚴重 1, cut-review-2.md 中等 1).
Retakes s21 (must) and s26 (cheap and clearly wrong); s25 only with `--with-s25` (see below). Seeds 9151301/9151302.
Built like fix1 (e915-live/fix1, e914-live/fix1): retake.py from live/st1, the d1 edits (../spec.json) and the fix1 edits
(../fix1/spec.json) applied first, then the edits below; mkjobs.py sets duration_seconds, swaps the pictures and writes
output_path; preflight-prompts.py; mkjobs.py also scans every prompt for negated object nouns (bible 拍法 18).

    python3 -I mkspec.py [--with-s25]
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix2 spec.json
    python3 -I mkjobs.py <live>/fix2
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix2/colab-jobs.json

<live> = /root/mokaair-work/videos/zhong-tian-qu-qi-e915-dh/runpod/live. The scratchpad's q-e915fix2.sh runs these and
the drafts; it stops before any Colab call if refs-live/prop-quyuanli-l1.png is not there yet.

Why a picture and not more words: fix1 already wrote the plough whole (a beam "bent in a gentle arc like a drawn bow", a
"small leaf-shaped dark iron ploughshare no bigger than a man's palm ... the only metal on the whole plough"), and both
fix1 takes still drew a straight beam with a crescent iron blade bigger than a head hanging off a board (s21 9151201,
the cut). The model has no picture of this tool, and the noun "ploughshare" pulls the big blade. So the prop gets a
reference picture first (live-action/screen-test-plough.py, Qwen-Image-Edit of set-qiutian-l2: the plough standing
side-on on a flat stubble field), filed as refs-live/prop-quyuanli-l1.png once picked, and the shots send it. The words
follow the picture: "share" (not ploughshare), "small rounded ... dull dark iron about the size of a man's hand", the
beam's arc said to be plainly visible, the wood "weathered brown" and matte (the s26 far view read a pale shining strip
as a sword at her waist).

- s21 (must; both reviews): the set picture set-qiutian-l2 (a field of ridged rows, the source of the "already ploughed"
  rows in s13 s19 s20 s24 s25) is swapped for the prop picture, and its set clause becomes the prop clause; the field
  stays in the text (fix1's flat stubble), and the prop picture is the same field. First frame: who carries which end
  with which hand, written by screen side. They walk side-on from screen right to screen left, so their LEFT shoulders
  face the camera: Erniu in front (screen left) carries the share end on his left shoulder, left hand on the beam
  just behind the share; Carpenter Shi behind (screen right) the handle end on his left shoulder, left hand round the
  handle; right hands empty; the plough hangs between their near shoulders in full view, the beam bowing down between
  them. They set it down standing side-on, the arc and the small share in view. 8 s as fix1 (a21 4.68 s at line_at
  0.8; the plough set down at c7.1 is the sfx; review 1 would end it at 5.75 anyway).
- s26 (cheap, 6 s; review 2: the far view reads as a sword): the far figure is Qin Shuang (fix1's fix held) but the
  bright straight thing at her side reads as a blade and the plough trails behind her (review 1 輕微 10). The prop
  picture goes in as <Picture 1> by swapping Tang Xiaotang's portrait (fix1 dropped all three Tang pictures; now only
  her two angle crops are dropped and the portrait slot carries the prop, so Qin stays the set slot's swap, <Picture 2>).
  The far sentence puts the plough in front of her, low on the ground, the arc running down to the share in the soil,
  her two hands on the short handle at her waist, pushing; the wood dark weathered brown. 6 s (a25 3.96 s; cut ends at
  4.5).
- s25 (NOT in fix2 unless --with-s25): the fix1 pick 9151201 is right in what matters (she alone behind the plough, both
  hands, the furrow, the soil curling) and its beam is bowed; only the share is a large dark blade, low in the frame and
  half in the soil. 8 s is the dearest shot of the three, and review 1 accepts it, review 2 suggests acceptance. If the
  new s21 makes the big share look like a different tool, run it later with --with-s25 (2 more jobs, 8 s): the set
  picture (fix1 dropped it) is swapped for the prop picture instead.

Rules (bible 拍法 18, fix1): props and background written as what is there; no object noun is negated in the prompts
(mkjobs.py fails on one); the things to keep out of the prop picture are in its negative file.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
FIX1 = json.loads((HERE.parent / "fix1" / "spec.json").read_text(encoding="utf-8"))["shots"]
REFS = "/home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
PROP = f"{REFS}/prop-quyuanli-l1.png"
WITH_S25 = "--with-s25" in sys.argv[1:]

FIX1_PLOUGH = ("one new curved-beam plough made of plain brown wood: one long smooth wooden beam bent in a gentle arc like a "
               "drawn bow, a short flat wooden sole at its low front end, one smooth polished wooden handle rising at the back, "
               "and fitted snugly on the sole's front tip one small leaf-shaped dark iron ploughshare no bigger than a man's "
               "palm, rounded and smooth all round like a leaf, the only metal on the whole plough")
PROP_CLAUSE = ("the curved-beam plough shown in <Picture {n}> is the one plough in this shot, keeping exactly its shape, its "
               "plain weathered brown wood and its small dull dark iron share.")
SHARE = "one small rounded share of dull dark iron about the size of a man's hand"


def shot(sid, extra, **more):
    s = {k: v for k, v in FIX1[sid].items() if k != "replace"}
    s["replace"] = FIX1[sid].get("replace", []) + extra
    s.update(more)
    return s


S = {
 "s21": shot("s21", [
   ["the location shown in <Picture 4> is the set, keeping its layout and props.", PROP_CLAUSE.format(n=4)],
   ["carrying between them on their shoulders, level and seen side-on, " + FIX1_PLOUGH + ",",
    "carrying between them, level and seen exactly side-on in front of their bodies, the curved-beam plough shown in "
    "<Picture 4>, all of it plain weathered brown wood, matte: one long wooden beam bowing down between them in one smooth "
    "deep arc like a drawn bow, its curve plain to see against the field, a short plain wooden handle at its back end, and "
    "at its front end " + SHARE + ", the only metal on the whole plough; Wang Erniu in front on screen left carries the "
    "front end, the end with the small iron share, on his left shoulder, his left hand gripping the beam just behind the "
    "share; Carpenter Shi behind him on screen right carries the back end on his left shoulder, his left hand wrapped "
    "round the short wooden handle; both men's left shoulders face the camera, so the whole plough hangs between them in "
    "full view from the share to the handle,"],
   ["their hands on the plough on their shoulders, nothing else in their hands;",
    "each man's left hand on the plough and his right hand swinging empty at his side, nothing else in their hands;"],
   ["lower the plough together and set its flat sole level on the dark earth, the small leaf-shaped iron tip resting on "
    "the soil;",
    "lift the plough down off their shoulders together and stand it on the dark earth beside them, still seen side-on: "
    "its long beam arching in one smooth curve, the short handle at the back toward Carpenter Shi and the small rounded "
    "iron share at the front resting on the soil;"]],
   swap_pictures={"set-qiutian-l2.png": PROP}),
 "s26": shot("s26", [
   ["she appears only once, small and far off out in the field.",
    "she appears only once, small and far off out in the field. " + PROP_CLAUSE.format(n=1)[0].upper()
    + PROP_CLAUSE.format(n=1)[1:]],
   ["below in the field far ahead on screen left, small but clear in the middle distance, Qin Shuang in her dark brown "
    "cross-collared short jacket, wide leather belt, black trousers and black leather boots, her long black high ponytail "
    "swinging, walks alone behind one new curved-beam plough with a long wooden beam curved like a drawn bow, both hands "
    "on its wooden handle, pushing it forward, a dark wave of fresh soil curling off its small iron share and one single "
    "long fresh furrow trailing behind her across the flat stubble; she is the only person out in the field;",
    "below in the field far ahead on screen left, small but clear in the middle distance and seen from the side, Qin "
    "Shuang in her dark brown cross-collared short jacket, wide plain dark leather belt, black trousers and black leather "
    "boots, her long black high ponytail swinging, walks toward screen left directly behind the curved-beam plough, the "
    "plough low on the ground in front of her: its long dark weathered brown wooden beam curving down in one smooth arc "
    "to the small rounded dull iron share sunk in the soil at its front end, her two hands on the short dark wooden handle "
    "at its back end at her waist, arms straight, pushing it ahead of her; a dark wave of fresh soil curls off the share "
    "and one single long fresh furrow trails behind her across the flat stubble; she is the only person out in the "
    "field, her two hands on the handle and her belt plain dark leather;"]],
   # fix1 dropped all three Tang pictures; keep the portrait slot (<Picture 1>) and swap it for the prop, so the text's
   # <Picture 4> (Qin, swapped in for the set picture by fix1) is renumbered to <Picture 2> by retake.py.
   drop_pictures=["tangxiaotang-angle-a-l1.png", "tangxiaotang-angle-b-l1.png"],
   swap_pictures={"tangxiaotang-portrait-l1.png": PROP,
                  "set-qiutian-l2.png": f"{REFS}/qinshuang-portrait-l1.png"}),
}
if WITH_S25:
    S["s25"] = shot("s25", [
        ["the location shown in <Picture 2> is the set, keeping its layout and props.", PROP_CLAUSE.format(n=2)],
        ["walking directly behind one new curved-beam plough, the plough out in front of her body toward screen left: one "
         "long wooden beam curved like a drawn bow, a short flat wooden sole, one small smooth leaf-shaped dark iron share "
         "as big as a palm on the sole's tip sunk into the earth, and one smooth polished wooden handle rising at the back "
         "toward her;",
         "walking directly behind the curved-beam plough shown in <Picture 2>, the plough low on the ground out in front "
         "of her body toward screen left, all of it plain weathered brown wood, matte: one long wooden beam curving down "
         "in one smooth arc like a drawn bow, its curve plain to see, to " + SHARE + " at its front end, sunk into the "
         "earth, and one short plain wooden handle at its back end rising toward her;"],
        ["its small iron share bites into the hard earth", "its small rounded iron share bites into the hard earth"]],
        swap_pictures={"set-qiutian-l2.png": PROP})
    S["s25"].pop("drop_set", None)
(HERE / "spec.json").write_text(json.dumps({"seeds": [9151301, 9151302], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", sorted(S))
