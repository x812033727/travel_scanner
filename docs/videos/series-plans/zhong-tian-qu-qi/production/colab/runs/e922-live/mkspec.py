"""Writes spec.json next to this file: e922 live d1 (e921-live/spec.json's way after its review).
Run: python3 -I mkspec.py

- Tang Xiaotang never shows her mouth (bible rule 3): her back shots (s01, s03, s05, s09 facing Wei Shaoqing; s12 walking
  out; s13, s15, s17, s20 at dinner) drop her three pictures and her identity sentence; the 'only' sentence says she is seen
  from behind and appears once. s25 does not list her (rule 1: three ids at most). s14 is her one face (silent): the softer
  face sentence of e907, the abacus out of her identity sentence (rule 20: it is only in the insert s19), e920 fix1's short
  ribbons, her long-ribbon profile angle-b dropped.
- s40, s41 send no person: her back on the boat, his back on the pier (r2.py: nobody named; NOBODY opens the motion).
- The unnamed backs and shoulders (rule 2) are named in the 'only' sentence so they are allowed in frame: Xu Yan's shoulder
  s23, the child's hand s26, the two women's backs s34, Qin Shuang's shoulder s36, Qin Shuang small in the doorway s38.
- Xu Yan from s27 on wears the old grey outer coat (script 角色表): his identity sentence says so.
- Xu Yan's smirking angle-b is sent nowhere (e921 review); Tang's long-ribbon angle-b nowhere; A-ling's "aloof piercing gaze"
  leaves her identity sentence everywhere (e921 s29/s31: it pulls her eyes to the lens; every shot of hers looks at someone).
- Sets (r2.py PLACES): the inn set-kezhan-l1 (kept: s01, s03, s05, s10, s12); its table top set-kezhan-table-l1 (s04, s07,
  s11); dinner set-xujia-wu-ye-l1 swapped for set-xujia-wu-l1 (s13, s14, s17, s20, s24, s25); the abacus prop-jinsuanpan-l1 in
  the set slot of s19, its clause replaced by e920's prop sentence; the corridor set-xujia-zoulang-l1 (s27, kept); her room
  set-xujia-tangfang-l1 (s28, s34, s37, kept), its table top set-xujia-tangfang-table-l1 (s29, s31); the night yard
  set-xujia-yuan-ye-l2 (s38, kept); the ferry landing set-dukou-ye-l1 swapped for set-dukou-l2 (s39, s41) and the boat
  set-chuan-ye-l1 for set-dukou-l2 (s40). Every swap is sent with an absolute path by prep922.sh. Close shots send none.
- The speaking gaze names the listener off screen, or the thing looked at.
- s35b (his thought) is the second half of the script's long c35, split after the system's two lines (r2.py BUY).
- No seed of this episode has been run. Seeds 9221101/9221102."""
import json
from pathlib import Path

L = "/home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"

TANG_BODY = ("keeps exactly the same face, hair and costume as the pictures: East Asian young woman of eighteen, dazzling glamorous "
             "beauty: big round sparkling eyes with long lashes, glossy peach-pink lips, rosy cheeks, luminous fair skin, petite curvy "
             "figure, hair in two looped buns tied with pink silk ribbons and pearl pins, a peach-pink silk brocade ruqun: a light "
             "cross-collared short jacket wrapped shut across the chest in a low closed V, its hem at the waist covering the top of a "
             "pleated skirt tied at the waist with a ribbon bow and a small gold ornament, thick opaque silk and flowing sleeves, a "
             "small gold abacus hanging at her waist; ")


def tang_id(first):
    return (f"Tang Xiaotang shown in <Picture {first}>, <Picture {first + 1}> and <Picture {first + 2}> (the same woman from "
            f"several angles) {TANG_BODY}")


TANG_PICS = ["tangxiaotang-portrait-l1.png", "tangxiaotang-angle-a-l1.png", "tangxiaotang-angle-b-l1.png"]
FACE = ["dazzling glamorous beauty: big round sparkling eyes with long lashes, glossy peach-pink lips, rosy cheeks,",
        "a delicate beauty: big round clear eyes with long lashes, soft peach-pink lips, light rosy cheeks,"]
NO_ABACUS = ["flowing sleeves, a small gold abacus hanging at her waist", "flowing sleeves"]
# e920 fix1 s37b: the ribbons as in the back shots
RIBBON = ["hair in two looped buns tied with pink silk ribbons and pearl pins",
          "hair in two round buns set high on her head, a short pink silk ribbon wrapped tight around each bun with its ends "
          "tucked into the bun, pearl pins, her neck and shoulders clear"]
ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."
ONLY_2 = "Only these 2 people are in the frame; no second copy of anyone appears."
ONLY_3 = "Only these 3 people are in the frame; no second copy of anyone appears."
ONE_TANG = "the young woman with the two high round buns appears only once"
SPEAK_GAZE = "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"
SPEAK_GAZE_HE = "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person"
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
# e920-live/mkspec.py PROP_KEEP with e920 fix1's long flat abacus
PROP_CLAUSE = ("The long gold abacus shown in <Picture 1> is the one abacus in this shot, keeping exactly its long flat shape, its "
               "long row of thin rods and its small round gold beads; it lies across her lap on the pleated silk skirt.")
ALING_GAZE = [", a plain grey-white cotton dress tailored close at the waist with a cloth sash and long sleeves, an aloof piercing gaze;",
              ", a plain grey-white cotton dress tailored close at the waist with a cloth sash and long sleeves;"]
XU_COAT = ["a faded blue-grey cotton scholar's robe patched at one elbow, cloth shoes",
           "an old plain grey cloth outer coat worn open over a faded blue-grey cotton scholar's robe patched at one elbow, cloth shoes"]

INN, INN_TOP = "set-kezhan-l1.png", "set-kezhan-table-l1.png"
WU, WU_NIGHT = "set-xujia-wu-l1.png", "set-xujia-wu-ye-l1.png"
PROP = "prop-jinsuanpan-l1.png"
ROOM, ROOM_TOP = "set-xujia-tangfang-l1.png", "set-xujia-tangfang-table-l1.png"
DUKOU, DUKOU_NIGHT, BOAT = "set-dukou-l2.png", "set-dukou-ye-l1.png", "set-chuan-ye-l1.png"


def back(beyond, n=2):
    return (f"Only these {n} people are in the frame, the young woman with the buns seen only from behind and {beyond} facing us "
            f"beyond her; {ONE_TANG}; no second copy of anyone appears.")


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


def besides(pr, what):
    return f"Besides {pr}, only {what} the composition describes are in the frame; no second copy of anyone appears."


ids = [f"s{n:02d}" for n in range(1, 36)] + ["s35b"] + [f"s{n:02d}" for n in range(36, 42)]
shots = {sid: {} for sid in ids}

# Tang Xiaotang from behind: her identity sentence and her three pictures leave.
for sid, first, only in [
    ("s01", 1, [ONLY_2, back("Wei Shaoqing")]),
    ("s03", 1, [ONLY_2, back("Wei Shaoqing")]),
    ("s05", 1, [ONLY_2, back("Wei Shaoqing")]),
    ("s09", 1, [ONLY_2, back("Wei Shaoqing")]),
    ("s12", 2, [ONLY_2, ("Only these 2 people are in the frame, Wei Shaoqing on the bench and the young woman with the buns seen "
                         f"only from behind walking to the door; {ONE_TANG}; no second copy of anyone appears.")]),
    ("s13", 1, [ONLY_3, back("Qin Shuang and A-ling", 3)]),
    ("s15", 1, [ONLY_2, back("little Xiaohe")]),
    ("s17", 1, [ONLY_2, back("Xu Yan")]),
    ("s20", 1, [ONLY_SHE, f"She is the only person in the frame, seen only from behind; {ONE_TANG}; no second copy of anyone appears."]),
]:
    add(sid, [tang_id(first), ""])
    add(sid, only)
    drop(sid, *TANG_PICS)
# Her one face (silent).
shots["s14"] = {"replace": [FACE, NO_ABACUS, RIBBON]}
drop("s14", "tangxiaotang-angle-b-l1.png")
# s25 does not list her (three ids at most): her back is allowed in the 'only' sentence.
add("s25", [ONLY_3, ("Only these 3 people and the young woman with the buns seen only from behind are in the frame; "
                     f"{ONE_TANG}; no second copy of anyone appears.")])

# The unnamed backs, shoulders and hands the compositions describe.
add("s23", [ONLY_SHE, besides("her", "the blurred shoulder of the man in the foreground")])
add("s26", [ONLY_HE, besides("him", "the small child's hand at the lower right edge")])
# s34: the composition says "exactly three people, the two women in the foreground seen only from behind"; no person sentence is added
add("s36", [ONLY_SHE, besides("her", "the blurred shoulder at the left edge")])
add("s38", [ONLY_HE, besides("him", "the small dim young woman in the house doorway")])

# Lines not said into a face on screen: the speaking gaze names the listener off screen, or the thing looked at.
for sid, g, he in [
    ("s02", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her", True),
    ("s06", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her", True),
    ("s08", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, close, his eyes on her", True),
    ("s10", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her", True),
    ("s12", "his face three-quarter to screen right toward the shut door, his eyes on it", True),
    ("s16", "her face three-quarter to screen right toward the young woman beyond the right edge of the frame, her eyes on her", False),
    ("s18", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her", True),
    ("s21", "her face three-quarter to screen left toward the young man beyond the left edge of the frame, her eyes on him", False),
    ("s22", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her", True),
    ("s24", "her face three-quarter to screen right toward the doorway beyond the right edge of the frame, her eyes on it", False),
    ("s27", "his face in profile to screen right toward the door, his eyes on it", True),
    ("s32", "her face three-quarter to screen right toward the young man beyond the right edge of the frame, her eyes on him", False),
    ("s33", "his face three-quarter to screen left toward the young woman beyond the left edge of the frame, his eyes on her", True),
    ("s36", "her face three-quarter to screen right toward the young man beyond the right edge of the frame, her eyes on him", False),
]:
    add(sid, [SPEAK_GAZE_HE if he else SPEAK_GAZE, g])

# A-ling: the gaze sentence out everywhere she is sent.
for sid in ["s13", "s21", "s23", "s25", "s32", "s36"]:
    add(sid, ALING_GAZE)
# Xu Yan in the old grey outer coat from s27 on.
for sid in ["s27", "s30", "s33", "s34", "s35", "s35b", "s37", "s38", "s39"]:
    add(sid, XU_COAT)
# Xu Yan's smirking angle-b nowhere; A-ling's angle-b out of the crowded s25.
for sid in ["s17", "s18", "s22", "s25", "s26", "s27", "s30", "s33", "s34", "s35", "s35b", "s37", "s38", "s39"]:
    drop(sid, "xuyan-angle-b-l1.png")
drop("s25", "aling-angle-b-l1.png")

# Sets.
KEEP = ["s01", "s03", "s05", "s10", "s12", "s27", "s28", "s34", "s37", "s38"]
SWAP = {}
for sid in ["s04", "s07", "s11"]:
    SWAP[sid] = {INN: INN_TOP}
# s20 sends nothing else once her pictures go (Ref2VA needs one): the night room
for sid in ["s13", "s14", "s17", "s20", "s24", "s25"]:
    SWAP[sid] = {WU: WU_NIGHT}
SWAP["s19"] = {WU: PROP}
for sid in ["s29", "s31"]:
    SWAP[sid] = {ROOM: ROOM_TOP}
for sid in ["s39", "s41"]:
    SWAP[sid] = {DUKOU: DUKOU_NIGHT}
SWAP["s40"] = {DUKOU: BOAT}
NO_SET = ["s02", "s06", "s08", "s09", "s15", "s16", "s18", "s21", "s22", "s23", "s26", "s30", "s32", "s33", "s35", "s35b", "s36"]
for sid, sw in SWAP.items():
    shots[sid]["swap_pictures"] = sw
for sid in NO_SET:
    shots[sid]["drop_set"] = True
# no person in the shot: the set clause opens the sentence; s19's is the prop sentence
for sid in ["s04", "s07", "s11", "s28", "s29", "s31", "s40", "s41"]:
    add(sid, [SET_CLAUSE, "T" + SET_CLAUSE[1:]])
add("s19", [SET_CLAUSE, PROP_CLAUSE])
assert sorted(KEEP + list(SWAP) + NO_SET) == sorted(ids), sorted(set(ids) - set(KEEP + list(SWAP) + NO_SET))
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e922 live d1 (e921-live's way after its review, written by mkspec.py). Tang Xiaotang never shows her mouth: nine "
              "back shots drop her three pictures and her identity sentence, s25 does not list her; s14 is her one silent face "
              "(softer face sentence, no abacus, short ribbons, no angle-b). s40, s41 send no person. Sets: set-kezhan-l1 (s01, s03, "
              "s05, s10, s12), set-kezhan-table-l1 (s04, s07, s11), set-xujia-wu-ye-l1 (s13, s14, s17, s20, s24, s25), prop-jinsuanpan-l1 "
              "(s19), set-xujia-zoulang-l1 (s27), set-xujia-tangfang-l1 (s28, s34, s37), set-xujia-tangfang-table-l1 (s29, s31), "
              "set-xujia-yuan-ye-l2 (s38), set-dukou-ye-l1 (s39, s41), set-chuan-ye-l1 (s40); close shots none (prep922.sh swaps "
              "with absolute paths). Xu Yan's angle-b nowhere, A-ling's piercing gaze nowhere, Xu Yan's grey outer coat from s27. "
              "The unnamed backs are allowed in the 'only' sentence; the speaking gaze names the listener off screen. No "
              "off-screen sentence is in these prompts (r2.py OFFSCREEN_SPEECH = False). Seeds 9221101/9221102."),
    "seeds": [9221101, 9221102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
