"""Writes spec.json next to this file: e923 live d1 (e922-live/spec.json's way after its review).
Run: python3 -I mkspec.py

- Tang Xiaotang never shows her mouth (bible rule 3): her back shots (s03, s07, s10, s14, s17, s18, s20, s22, s24, s27 on the
  boat; s28, s29, s31, s33, s36 at the inn) drop her three pictures and her identity sentence; the 'only' sentence says she
  is seen from behind and appears once. Her silent faces s19, s37, s40: the softer face sentence of e907, the abacus out of
  her identity sentence (rule 20: only in the inserts s11, s15, s25), e920 fix1's short ribbons, her long-ribbon angle-b
  dropped.
- No person sent: s02, s06 (his legs, two hands), s11, s15, s25 (the abacus on her lap), s21 (the boat small at sunrise),
  s35, s39 (hands on the inn table). The set clause opens the sentence; the lap inserts get the long flat abacus clause
  (the coordinator's 2026-11-16 correction: the prop picture's abacus is as long as her forearm).
- The unnamed people the compositions describe (rule 2, 23, 25) are named in the 'only' sentence so they are allowed in
  frame: the two small figures on the boat s01, the boatman s04, s07, s08, s27, the small cuffed hand s13, her buns at the
  left edge s34. The elders' "old men" already gives ref2manifest's 'Besides them' sentence (s28, s29, s37, s40).
- Xu Yan in the old grey outer coat everywhere (his identity sentence); his smirking angle-b nowhere (e921 review).
- extras' "the air is clear and still" becomes the fog in the night shots on the water (s01-s18, e922 必改 2) and the thin
  mist at sunrise (s19-s27); the inn keeps it.
- The wide-shot shoes sentence leaves s01 (his feet under water) and s21 (two tiny seated figures).
- Sets (r2.py PLACES): ferry s01 set-dukou-ye-l1, s02 set-dukou-ye-shui-l1; the night boat s04, s07 set-chuan-ye-l1, its
  fog plate set-chuan-ye-wu-l1 for the close shots; sunrise s19, s21 set-chuan-chen-l1, the mist plate set-chuan-chen-wu-l1;
  the abacus prop-jinsuanpan-l1 in the set slot of s11, s15, s25; the inn in the afternoon set-kezhan-pm-l1 (s28, s29, s31,
  s36, s37, s40), its table crop set-kezhan-pm-table-l1 (s35, s39); close shots at the inn none. Every swap is sent with an
  absolute path by prep923.sh.
- The speaking gaze names the listener off screen, or the thing looked at.
- After the independent review (writer-tools/e023-r2/review.md, 2026-11-16; r2.py's docstring has the list): s31 and s36 put
  Xu Yan back at her right shoulder (his coat sentence, his angle-b dropped, a three-person 'only' sentence); s28's gaze is
  toward the people who have already come in (the elders stand inside the door). The two plates set-chuan-ye-wu-l1 and
  set-chuan-chen-wu-l1 were regraded under the same ids, so nothing here changes for them. The window crop
  set-kezhan-pm-chuang-l1 is not sent (s30, s32, s33, s34, s38 keep no set).
- No seed of this episode has been run. Seeds 9231101/9231102.
"""
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
# e922-live PROP_CLAUSE, the coordinator's long flat abacus
PROP_CLAUSE = ("The long gold abacus shown in <Picture 1> is the one abacus in this shot, as long as her forearm, keeping exactly "
               "its long flat shape, its long row of thin rods and its small round gold beads; it lies flat across her lap on the "
               "pleated silk skirt.")
XU_COAT = ["a faded blue-grey cotton scholar's robe patched at one elbow, cloth shoes",
           "an old plain grey cloth outer coat worn open over a faded blue-grey cotton scholar's robe patched at one elbow, cloth shoes"]
CLEAR = "the air is clear and still, a clean natural film image"
FOG = "the fog hangs thick and drifts slowly and evenly over the water, a clean natural film image"
MIST = "the thin mist drifts slowly and evenly over the water in the warm morning light, a clean natural film image"
SHOES = "Every person in the frame wears dark cloth shoes on both feet. "

DUKOU = "set-dukou-l2.png"
INN = "set-kezhan-l1.png"
PROP = "prop-jinsuanpan-l1.png"


def back(beyond, n=2):
    return (f"Only these {n} people are in the frame, the young woman with the buns seen only from behind and {beyond} facing us "
            f"beyond her; {ONE_TANG}; no second copy of anyone appears.")


# e023 review 必改 10: s31, s36 keep Xu Yan at her right shoulder, as s29
BACK_XU_WEI = ("Only these 3 people are in the frame, the young woman with the buns seen only from behind, Xu Yan at her right "
               f"shoulder and Wei Shaoqing facing us beyond her; {ONE_TANG}; no second copy of anyone appears.")


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


def besides(pr, what):
    return f"Besides {pr}, only {what} the composition describes are in the frame; no second copy of anyone appears."


ids = [f"s{n:02d}" for n in range(1, 14)] + ["s13b"] + [f"s{n:02d}" for n in range(14, 41)]
shots = {sid: {} for sid in ids}

# Tang Xiaotang from behind: her identity sentence and her three pictures leave.
BOATMAN_TOO = ("Only Xu Yan, the young woman with the buns seen only from behind and the boatman seen only from behind are in the "
               f"frame; {ONE_TANG}; no second copy of anyone appears.")
for sid, first, only in [
    ("s03", 1, [ONLY_2, back("Xu Yan in the water")]),
    ("s07", 4, [ONLY_2, BOATMAN_TOO]),
    ("s10", 1, [ONLY_2, back("Xu Yan")]),
    ("s14", 1, [ONLY_2, back("Xu Yan")]),
    ("s17", 1, [ONLY_SHE, f"She is the only person in the frame, seen only from behind; {ONE_TANG}; no second copy of anyone appears."]),
    ("s18", 1, [ONLY_2, back("Xu Yan")]),
    ("s20", 1, [ONLY_2, back("Xu Yan")]),
    ("s22", 1, [ONLY_SHE, f"She is the only person in the frame, seen only from behind; {ONE_TANG}; no second copy of anyone appears."]),
    ("s24", 1, [ONLY_2, back("Xu Yan")]),
    ("s27", 1, [ONLY_SHE, ("Only the young woman with the buns and the boatman, both seen only from behind, are in the frame; "
                           f"{ONE_TANG}; no second copy of anyone appears.")]),
    ("s28", 2, None),  # "old men": ref2manifest's 'Besides them' sentence stays
    ("s29", 1, None),
    ("s31", 1, [ONLY_3, BACK_XU_WEI]),
    ("s33", 1, [ONLY_2, back("Wei Shaoqing")]),
    ("s36", 1, [ONLY_3, BACK_XU_WEI]),
]:
    add(sid, [tang_id(first), ""])
    if only:
        add(sid, only)
    drop(sid, *TANG_PICS)
# Her silent faces.
for sid in ["s19", "s37", "s40"]:
    for pair in (FACE, NO_ABACUS, RIBBON):
        add(sid, pair)
    drop(sid, "tangxiaotang-angle-b-l1.png")

# The unnamed people the compositions describe.
add("s01", [ONLY_HE, besides("him", "the two small figures on the boat far off in the fog")])
add("s04", [ONLY_HE, besides("him", "the boatman seen only from behind at the bow")])
add("s08", [ONLY_HE, besides("him", "the boatman seen only from behind, soft at the bow,")])
add("s13", [ONLY_HE, "He is the only person in the frame; only a small hand in a peach-pink sleeve cuff rests at the lower right edge."])
add("s34", [ONLY_HE, besides("him", "the back of the young woman's head at the left edge")])

# Lines not said into a face on screen: the speaking gaze names the listener off screen, or the thing looked at.
for sid, g, he in [
    ("s01", "his face in profile to screen right toward the boat in the fog, his eyes on it", True),
    ("s05", "his face tilted up three-quarter to screen right toward the young woman above the right edge of the frame, his eyes on her", True),
    ("s08", "his face three-quarter to screen right toward the boatman at the bow, his eyes on him", True),
    ("s09", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her", True),
    ("s12", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her", True),
    ("s16", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her", True),
    ("s23", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her", True),
    ("s26", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her", True),
    ("s28", "his face three-quarter to screen right toward the people who have come in at the door, his eyes on the young woman", True),
    ("s30", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her", True),
    ("s32", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her", True),
    ("s34", "his face three-quarter to screen left toward the young woman at the left edge of the frame, his eyes on her", True),
    ("s37", "his face three-quarter to screen right toward the three old men by the screen, his eyes on them", True),
    ("s38", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, close, his eyes on her", True),
]:
    add(sid, [SPEAK_GAZE_HE if he else SPEAK_GAZE, g])

# Xu Yan in the old grey outer coat; his smirking angle-b nowhere.
XU = ["s01", "s03", "s04", "s05", "s07", "s08", "s09", "s10", "s12", "s13", "s13b", "s14", "s16", "s18", "s19", "s20", "s23",
      "s24", "s26", "s29", "s31", "s34", "s36", "s37", "s40"]
for sid in XU:
    add(sid, XU_COAT)
    drop(sid, "xuyan-angle-b-l1.png")

# Fog at night on the water, thin mist at sunrise (extras' clear-air sentence would fight them).
for n in range(1, 19):
    for sid in [f"s{n:02d}"] + (["s13b"] if n == 13 else []):
        add(sid, [CLEAR, FOG])
for n in range(19, 28):
    add(f"s{n:02d}", [CLEAR, MIST])
# The wide-shot shoes sentence: his feet are under water (s01); two tiny seated figures (s21).
for sid in ["s01", "s21"]:
    add(sid, [SHOES, ""])

# Sets.
SWAP = {"s01": {DUKOU: "set-dukou-ye-l1.png"}, "s02": {DUKOU: "set-dukou-ye-shui-l1.png"}}
for sid in ["s04", "s07"]:
    SWAP[sid] = {DUKOU: "set-chuan-ye-l1.png"}
for sid in ["s03", "s05", "s06", "s08", "s09", "s10", "s12", "s13", "s13b", "s14", "s16", "s17", "s18"]:
    SWAP[sid] = {DUKOU: "set-chuan-ye-wu-l1.png"}
for sid in ["s11", "s15", "s25"]:
    SWAP[sid] = {DUKOU: PROP}
for sid in ["s19", "s21"]:
    SWAP[sid] = {DUKOU: "set-chuan-chen-l1.png"}
for sid in ["s20", "s22", "s23", "s24", "s26", "s27"]:
    SWAP[sid] = {DUKOU: "set-chuan-chen-wu-l1.png"}
for sid in ["s28", "s29", "s31", "s36", "s37", "s40"]:
    SWAP[sid] = {INN: "set-kezhan-pm-l1.png"}
for sid in ["s35", "s39"]:
    SWAP[sid] = {INN: "set-kezhan-pm-table-l1.png"}
NO_SET = ["s30", "s32", "s33", "s34", "s38"]
for sid, sw in SWAP.items():
    shots[sid]["swap_pictures"] = sw
for sid in NO_SET:
    shots[sid]["drop_set"] = True
# no person in the shot: the set clause opens the sentence; the lap inserts' is the prop sentence
for sid in ["s02", "s06", "s21", "s35", "s39"]:
    add(sid, [SET_CLAUSE, "T" + SET_CLAUSE[1:]])
for sid in ["s11", "s15", "s25"]:
    add(sid, [SET_CLAUSE, PROP_CLAUSE])
assert sorted(list(SWAP) + NO_SET) == sorted(ids), sorted(set(ids) - set(list(SWAP) + NO_SET))
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e923 live d1 (e922-live's way after its review, written by mkspec.py). Tang Xiaotang never shows her mouth: fifteen "
              "back shots drop her three pictures and her identity sentence; s19, s37, s40 are her silent faces (softer face "
              "sentence, no abacus, short ribbons, no angle-b). No person sent in s02, s06, s11, s15, s21, s25, s35, s39. Sets: "
              "set-dukou-ye-l1 (s01), set-dukou-ye-shui-l1 (s02), set-chuan-ye-l1 (s04, s07), set-chuan-ye-wu-l1 (the night close "
              "shots), prop-jinsuanpan-l1 (s11, s15, s25), set-chuan-chen-l1 (s19, s21), set-chuan-chen-wu-l1 (the sunrise close "
              "shots), set-kezhan-pm-l1 (s28, s29, s31, s36, s37, s40), set-kezhan-pm-table-l1 (s35, s39); inn close shots none "
              "(prep923.sh swaps with absolute paths). Xu Yan's grey outer coat everywhere, his angle-b nowhere. Fog s01-s18, "
              "mist s19-s27. No off-screen sentence (r2.py OFFSCREEN_SPEECH = False). After the review: s31, s36 Xu Yan at her "
              "right shoulder (three people). Seeds 9231101/9231102."),
    "seeds": [9231101, 9231102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
