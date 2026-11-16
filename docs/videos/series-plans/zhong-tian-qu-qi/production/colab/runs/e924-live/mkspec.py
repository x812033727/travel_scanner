"""Writes spec.json next to this file: e924 live d1 (e923-live/spec.json's way after its review).
Run: python3 -I mkspec.py

- Tang Xiaotang never shows her mouth (bible rule 3), and in this episode never her face: her back shots (s04, s07, s12 in the
  shop; s09, s17, s30, s32, s34 on the street) drop her three pictures and her identity sentence (it also names the abacus
  at her waist, rule 20); the 'only' sentence says she is seen from behind and appears once. She has no face shot.
- No person sent: s08 (the abacus on the counter: the prop picture, the counter version of e923's prop sentence), s10, s13,
  s16 (hands), s11 (the Wei shop boy, unnamed, bible 〈小角色〉), s21, s24 (funnel mouths), s33 (two Wei men). The set clause
  opens the sentence.
- The unnamed people the compositions describe (rule 2, 25) are named in the 'only' sentence so they are allowed in frame:
  the shop boy across the street s01 (review 必改 1: she is not in s01), the six customers s02, the customers' shoulders
  s14, the two men across the street s29, her buns at the right edge s35 (必改 9); s12 the two customers beyond the counter; s09 the passers-by.
- Xu Yan's smirking angle-b nowhere (e921 review). Where gen-dh sent him only angle-a and angle-b (the close shots s15, s26,
  s31), angle-b is swapped for his portrait l1 instead of dropped (two pictures of him, as in his other shots). His old grey
  outer coat at night and first light in the workshop (s19, s20, s23, s26, s27, s28; the script).
- extras' "the air is clear and still" becomes the rising steam in the night workshop (s19-s23); the street, the shop and the
  workshop at first light keep it.
- The speaking gaze names the listener off screen, or the thing looked at.
- Sets (r2.py PLACES): street wide s01, s02, s29 set-xianjie-l1; the Xu shop front set-xianjie-xuji-l1; the Wei shop front
  set-xianjie-weiji-l1; its upper floor set-xianjie-lou-l1; the low counter in front of the Xu shop set-xianjie-shi-l1; the
  shop inside set-xuji-pu-l1 (gen-dh's, kept) and its counter top set-xuji-pu-cabinet-l1 (s13); the abacus prop-jinsuanpan-l1
  (s08); the workshop at night set-tangfang-ye-l1 (s19) and its crop set-tangfang-ye-jia-l1 (s20-s23); at first light
  set-tangfang-l1 (gen-dh's, kept: s27, s28) and its crop set-tangfang-jia-l1 (s24-s26). Every swap is sent with an absolute
  path by prep924.sh.
- After the independent review (writer-tools/e024-r2/review.md, 2026-11-16): s01 drops the young woman from its 'only'
  sentence (必改 1), s35 puts her buns at the right edge and his eyes past her (必改 9), s33's two men are just inside the
  doorway, small and side-on (建議). The funnel sentence (必改 3) is r2.py's SHED itself, so no replace is needed here;
  set-xianjie-lou-l1 was regraded under the same id (refs-live/README.md).
- No seed of this episode has been run. Seeds 9241101/9241102.
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
ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."
ONLY_2 = "Only these 2 people are in the frame; no second copy of anyone appears."
BESIDES_THEM = "Besides them, only the other people the composition names are in the frame; no second copy of anyone appears."
BESIDES_HIM = "Besides him, only the other people the composition names are in the frame; no second copy of anyone appears."
ONE_TANG = "the young woman with the two high round buns appears only once"
SPEAK_GAZE_HE = "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person"
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
# the abacus on the counter (s08): the prop picture already shows it lying on the shop's dark counter-cabinet
PROP_CLAUSE = ("The long gold abacus shown in <Picture 1> is the one abacus in this shot, as long as her forearm, keeping exactly "
               "its long flat shape, its long row of thin rods and its small round gold beads; it lies flat on the dark wooden "
               "counter top as in the picture.")
XU_COAT = ["a faded blue-grey cotton scholar's robe patched at one elbow, cloth shoes",
           "an old plain grey cloth outer coat worn open over a faded blue-grey cotton scholar's robe patched at one elbow, cloth shoes"]
CLEAR = "the air is clear and still, a clean natural film image"
STEAM = "the steam rises slowly and evenly in the firelight, a clean natural film image"

SHIJI = "set-shiji-l1.png"
PU = "set-xuji-pu-l1.png"
TF = "set-tangfang-l1.png"


def back(beyond, n=2):
    return (f"Only these {n} people are in the frame, the young woman with the buns seen only from behind and {beyond} facing us "
            f"beyond her; {ONE_TANG}; no second copy of anyone appears.")


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


def besides(pr, what):
    return f"Besides {pr}, only {what} the composition describes are in the frame; no second copy of anyone appears."


ids = [f"s{n:02d}" for n in range(1, 16)] + ["s15b"] + [f"s{n:02d}" for n in range(16, 37)]
shots = {sid: {} for sid in ids}

# Tang Xiaotang from behind: her identity sentence and her three pictures leave.
ALONE = f"She is the only person in the frame, seen only from behind; {ONE_TANG}; no second copy of anyone appears."
for sid, only in [
    ("s04", [ONLY_2, back("Xu Yan in the doorway")]),
    ("s07", [ONLY_2, back("Wang Erniu")]),
    ("s09", [ONLY_SHE, ("She is seen only from behind; besides her, only the few customers passing across the street the "
                        f"composition describes are in the frame; {ONE_TANG}; no second copy of anyone appears.")]),
    ("s12", [ONLY_SHE, ("Only the young woman with the buns seen only from behind and the two customers beyond the counter are in "
                        f"the frame; {ONE_TANG}; no second copy of anyone appears.")]),
    ("s17", [ONLY_2, back("Xu Yan")]),
    ("s30", [ONLY_SHE, ALONE]),
    ("s32", [ONLY_2, back("Xu Yan")]),
    ("s34", [ONLY_2, back("Xu Yan")]),
]:
    add(sid, [tang_id(1), ""])
    add(sid, only)
    drop(sid, *TANG_PICS)

# The unnamed people the compositions describe.
add("s01", [ONLY_HE, "Besides him, only the shop boy across the street the composition describes is in the frame; no second copy of anyone appears."])  # review 必改 1
add("s02", [ONLY_HE, besides("him", "the six customers in the line")])
add("s14", [ONLY_HE, besides("him", "the soft shoulders of the two customers in the foreground")])
add("s29", [BESIDES_HIM, besides("him", "the two men carrying sacks across the street")])
add("s35", [ONLY_HE, besides("him", "the back of the young woman's head at the right edge")])  # review 必改 9
for sid in ["s19", "s27", "s28"]:
    add(sid, [BESIDES_THEM, ONLY_2])
add("s33", [BESIDES_THEM, "Only the two men just inside the doorway across the street, small and side-on, are in the frame; no second copy of anyone appears."])

# Lines not said into a face on screen: the speaking gaze names the listener off screen, or the thing looked at.
for sid, g in [
    ("s03", "his face three-quarter to screen left toward the dark doorway, where Xu Yan is off screen inside, his eyes on it"),
    ("s05", "his face three-quarter to screen right toward the shop across the street, his eyes on it"),
    ("s06", "his face three-quarter to screen left looking down toward the Xu shop below, his eyes on it"),
    ("s14", "his face three-quarter to screen right toward the shop across the street, his eyes on it"),
    ("s18", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her"),
    ("s20", "his face three-quarter to screen left toward Wang Erniu off screen left, his eyes on him"),
    ("s22", "his face three-quarter to screen right toward Xu Yan off screen right, his eyes on him"),
    ("s23", "his face three-quarter to screen left toward Wang Erniu off screen left, his eyes on him"),
    ("s25", "his face three-quarter to screen right toward Xu Yan off screen right, his eyes on him"),
    ("s31", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her"),
    ("s35", "his face three-quarter to screen right and tilted up past her toward the upper floor of the shop across the street, his eyes on it"),
    ("s36", "his face three-quarter to screen left looking down toward the Xu shop below, his eyes on it"),
]:
    add(sid, [SPEAK_GAZE_HE, g])

# Xu Yan: his smirking angle-b nowhere; where he has only the two angle pictures, angle-b becomes his portrait.
XU_ALL = ["s01", "s04", "s05", "s14", "s15", "s15b", "s17", "s18", "s19", "s20", "s23", "s26", "s27", "s28", "s29", "s31", "s32",
          "s34", "s35"]
XU_TWO = ["s15", "s26", "s31"]  # gen-dh sent angle-a and angle-b only
for sid in XU_ALL:
    if sid not in XU_TWO:
        drop(sid, "xuyan-angle-b-l1.png")
# The grey outer coat in the workshop.
for sid in ["s19", "s20", "s23", "s26", "s27", "s28"]:
    add(sid, XU_COAT)
# The rising steam at night (extras' clear-air sentence would fight it).
for sid in ["s19", "s20", "s21", "s22", "s23"]:
    add(sid, [CLEAR, STEAM])

# Sets.
SWAP = {}
for sid in ["s01", "s02", "s29"]:
    SWAP[sid] = {SHIJI: "set-xianjie-l1.png"}
for sid in ["s03", "s05", "s14", "s15", "s15b", "s18", "s30", "s31", "s32", "s34", "s35"]:
    SWAP[sid] = {SHIJI: "set-xianjie-xuji-l1.png"}
for sid in ["s09", "s11", "s33"]:
    SWAP[sid] = {SHIJI: "set-xianjie-weiji-l1.png"}
for sid in ["s06", "s36"]:
    SWAP[sid] = {SHIJI: "set-xianjie-lou-l1.png"}
for sid in ["s10", "s16", "s17"]:
    SWAP[sid] = {SHIJI: "set-xianjie-shi-l1.png"}
SWAP["s08"] = {PU: "prop-jinsuanpan-l1.png"}
SWAP["s13"] = {PU: "set-xuji-pu-cabinet-l1.png"}
SWAP["s19"] = {TF: "set-tangfang-ye-l1.png"}
for sid in ["s20", "s21", "s22", "s23"]:
    SWAP[sid] = {TF: "set-tangfang-ye-jia-l1.png"}
for sid in ["s24", "s25", "s26"]:
    SWAP[sid] = {TF: "set-tangfang-jia-l1.png"}
for sid in XU_TWO:
    SWAP.setdefault(sid, {})["xuyan-angle-b-l1.png"] = "xuyan-portrait-l1.png"
KEEP_SET = ["s04", "s07", "s12", "s27", "s28"]  # gen-dh's own pictures: set-xuji-pu-l1, set-tangfang-l1
for sid, sw in SWAP.items():
    shots[sid]["swap_pictures"] = sw
# no person in the shot: the set clause opens the sentence; the abacus insert's is the prop sentence
for sid in ["s10", "s11", "s13", "s16", "s21", "s24", "s33"]:
    add(sid, [SET_CLAUSE, "T" + SET_CLAUSE[1:]])
add("s08", [SET_CLAUSE, PROP_CLAUSE])
assert sorted(set(SWAP) | set(KEEP_SET)) == sorted(ids), sorted(set(ids) - set(SWAP) - set(KEEP_SET))
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e924 live d1 (e923-live's way after its review, written by mkspec.py). Tang Xiaotang never shows her mouth or her "
              "face: eight back shots drop her three pictures and her identity sentence. No person sent in s08, s10, s11, s13, "
              "s16, s21, s24, s33. Sets: set-xianjie-l1 (s01, s02, s29), set-xianjie-xuji-l1, set-xianjie-weiji-l1, "
              "set-xianjie-lou-l1 (s06, s36), set-xianjie-shi-l1 (s10, s16, s17), set-xuji-pu-l1 (s04, s07, s12), "
              "set-xuji-pu-cabinet-l1 (s13), prop-jinsuanpan-l1 (s08), set-tangfang-ye-l1 (s19), set-tangfang-ye-jia-l1 "
              "(s20-s23), set-tangfang-jia-l1 (s24-s26), set-tangfang-l1 (s27, s28) (prep924.sh swaps with absolute paths). Xu "
              "Yan's angle-b nowhere (swapped for his portrait in s15, s26, s31); his grey outer coat in the workshop. Steam at "
              "night s19-s23. No off-screen sentence (r2.py OFFSCREEN_SPEECH = False). Seeds 9241101/9241102."),
    "seeds": [9241101, 9241102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
