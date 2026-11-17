"""Writes spec.json next to this file: e926 live d1 (e925-live/spec.json's way after its review, with the e921-e924 picks).
Run: python3 -I mkspec.py

- Tang Xiaotang never shows her mouth (bible rule 3), and in this episode never her face: her speaking back shots (s01, s07,
  s12 in the workshop; s21, s24 in the shop) drop her three pictures and her identity sentence (it also names the abacus at
  her waist, rule 20); the 'only' sentence says she is seen from behind and appears once. Her silent back shot s23 never
  lists her (no picture, never named).
- No person sent: s06, s18, s22, s31, s33, s36, s39 (hands), s25, s27 (the six customers, the clerk), s38 (the man in grey).
  The set clause opens the sentence.
- The unnamed people the compositions describe (rules 2, 25) are named in the 'only' sentence so they are allowed in frame,
  with their counts: the child's hands (s05), the foreground shoulders (s10, s11, s37), the clerk in dark red (s25-s28), the
  six customers (s25, s35, s40), the man in grey (s37, s38, s40).
- Xu Yan's smirking angle-b nowhere (e921 review). Where gen-dh sent him only angle-a and angle-b (the close-ups s15, s20,
  both facing screen right), his portrait goes first and angle-a second (e925 review 建議: angle-a -> portrait, angle-b ->
  angle-a; the swaps run in this order).
- extras' "the air is clear and still" becomes the rising steam under the workshop's roof (s01-s07, s10, s12, s13, s15-s17);
  the path at the railing, the shop, the street and the back room keep it.
- The speaking gaze names the listener off screen, or the thing looked at.
- Sets (r2.py PLACES): the workshop set-tangfang-l1 (gen-dh's, kept: s02, s17), its crop set-tangfang-jia-l1 (close shots), the
  new free crop set-tangfang-lu-l1 (s08, s09, s11, s14); the shop set-xuji-pu-l1 (gen-dh's, kept: s19-s21, s23, s24), the
  counter top set-xuji-pu-cabinet-l1 (s18, s22), the back room set-xuji-pu-houjian-l1 (s30-s34); the street set-xianjie-l1
  (s25, s40), the Wei shop front set-xianjie-weiji-l1 (s26-s29), the Xu shop front set-xianjie-xuji-l1 (s35, s37), the paving
  set-xianjie-shi-l1 (s36, s38, s39). gen-dh's set-shiji-l1 is never sent. Every swap is sent with an absolute path by
  prep926.sh.
- No seed of this episode has been run. Seeds 9261101/9261102.

After the independent review (writer-tools/e026-r2/review.md; 2026-11-17, the coordinator deciding for the owner; r2.py's
docstring AFTER THE INDEPENDENT REVIEW has the wording changes):
- 必改 1: the seven inserts (s06, s18, s22, s31, s33, s36, s39) replace r2.py's "the shot opens directly on" with "the very
  first frame is already a close view of": no d1 prompt says "open" (s18's stitched sheets read as a book opened).
- 必改 3 + 建議: s40 has five customers backing away (with the man in grey, s35's six); "exactly seven people" is r2.py's.
- 必改 8: s04 sends angles/xiaohe-angle-a-l1 after her portrait (add_pictures; prep926.sh inserts it with an absolute path);
  the header, her identity sentence and the set clause are renumbered here (e925-live's way for Qin Shuang).
- 建議 1: the back room s30-s34 sends the free brightened set-xuji-houjian-deng-l1 instead of the dark set-xuji-pu-houjian-l1.
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
ONE_TANG = "the young woman with the two high round buns appears only once"
SPEAK_GAZE_HE = "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person"
SPEAK_GAZE_SHE = "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
CLEAR = "the air is clear and still, a clean natural film image"
STEAM = "the steam rises slowly and evenly in the sunlight, a clean natural film image"

TF = "set-tangfang-l1.png"
PU = "set-xuji-pu-l1.png"
SHIJI = "set-shiji-l1.png"


def back(beyond, n=2):
    return (f"Only these {n} people are in the frame, the young woman with the buns seen only from behind and {beyond} "
            f"beyond her; {ONE_TANG}; no second copy of anyone appears.")


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


def only(what):
    return f"Only {what} are in the frame; no second copy of anyone appears."


def besides(pr, what):
    return f"Besides {pr}, only {what} the composition describes are in the frame; no second copy of anyone appears."


ids = [f"s{n:02d}" for n in range(1, 31)] + ["s30b"] + [f"s{n:02d}" for n in range(31, 41)]
shots = {sid: {} for sid in ids}

# Tang Xiaotang from behind, speaking: her identity sentence and her three pictures leave.
ALONE = f"She is the only person in the frame, seen only from behind; {ONE_TANG}; no second copy of anyone appears."
for sid, onl in [
    ("s01", [ONLY_SHE, ALONE]),
    ("s07", [ONLY_SHE, ALONE]),
    ("s12", [ONLY_2, back("Xu Yan by the stove facing us")]),
    ("s21", [ONLY_2, back("Xu Yan across the counter facing us")]),
    ("s24", [ONLY_SHE, ALONE]),
]:
    add(sid, [tang_id(1), ""])
    add(sid, onl)
    drop(sid, *TANG_PICS)

# Her silent back shot with a named person (she is not listed: no picture, never named).
add("s23", [ONLY_HE, back("Xu Yan across the counter facing us")])

# The unnamed people the compositions describe, with their counts; no-person shots open with the set clause.
NOPERSON = ["s06", "s18", "s22", "s25", "s27", "s31", "s33", "s36", "s38", "s39"]
for sid in NOPERSON:
    add(sid, [SET_CLAUSE, "T" + SET_CLAUSE[1:]])
add("s02", [BESIDES_THEM, ONLY_2])
add("s17", [BESIDES_THEM, ONLY_2])
add("s05", [ONLY_HE, besides("him", "the child's two small hands holding the bowl at the lower right edge")])
add("s10", [ONLY_HE, besides("him", "the soft shoulder of the thin man in the foreground")])
add("s11", [ONLY_HE, besides("him", "the soft shoulder of the big man in the foreground")])
add("s25", [BESIDES_THEM, only("the six customers in the line and the young man in dark red across the street, all small,")])
add("s26", [ONLY_HE, besides("him", "the young man in dark red by the door post")])
add("s27", [" Initial composition:", " Only the young man in dark red is in the frame; no second copy of anyone appears. Initial composition:"])
add("s28", [ONLY_HE, besides("him", "the young man in dark red on the step behind him")])
add("s35", [BESIDES_THEM, besides("them", "the six customers in the line")])
add("s37", [ONLY_HE, besides("him", "the man in grey and the soft shoulder of the woman in the foreground")])
add("s38", [" Initial composition:", " " + only("the man in grey and the two customers beside him,") + " Initial composition:"])
add("s40", [ONLY_HE, besides("him", "the man on the ground and the five customers backing away")])

# review 必改 1: no "open" in any d1 prompt; the inserts start on themselves in other words
INSERTS = ["s06", "s18", "s22", "s31", "s33", "s36", "s39"]
for sid in INSERTS:
    add(sid, ["the shot opens directly on", "the very first frame is already a close view of"])

# review 必改 8: her angle-a (face three-quarter to screen left, as in s04) after her portrait, before the set
XIAOHE_A = "angles/xiaohe-angle-a-l1.png"
shots["s04"]["add_pictures"] = [XIAOHE_A]
add("s04", ["For the target video, <Picture 1> and <Picture 2> are referenced throughout.",
            "For the target video, <Picture 1>, <Picture 2> and <Picture 3> are referenced throughout."])
add("s04", ["little Xiaohe shown in <Picture 1> keeps", "little Xiaohe shown in <Picture 1> and <Picture 2> (the same girl from several angles) keeps"])
add("s04", ["the location shown in <Picture 2> is the set", "the location shown in <Picture 3> is the set"])

# Lines not said into a face on screen: the speaking gaze names the listener off screen, or the thing looked at.
for sid, g in [
    ("s02", "his face three-quarter to screen left toward the middle of the shed, his eyes on it"),
    ("s03", "his face three-quarter to screen right toward Wang Erniu off screen right, his eyes on him"),
    ("s05", "his face three-quarter to screen right toward the child at the lower right edge of the frame, his eyes on her"),
    ("s09", "his face three-quarter to screen left toward the people in the shed beyond the left edge of the frame, his eyes on them"),
    ("s16", "his face three-quarter to screen right toward the path beyond the right edge of the frame, his eyes on it"),
    ("s17", "his face three-quarter to screen left toward the stone basin, his eyes on it"),
    ("s19", "his face three-quarter to screen right toward the counter beyond the right edge of the frame, his eyes on it"),
    ("s26", "his face three-quarter to screen left toward the Xu shop across the street, his eyes on it"),
    ("s29", "his face three-quarter to screen left toward the Xu shop across the street, his eyes on it"),
    ("s30b", "his face three-quarter to screen left toward the dark doorway, his eyes on it"),
    ("s32", "his face three-quarter to screen right toward the corner of the table beyond the right edge of the frame, his eyes on it"),
    ("s34", "his face three-quarter to screen left toward the dark doorway, his eyes on it"),
    ("s35", "his face three-quarter to screen right toward the line of customers, his eyes on them"),
]:
    add(sid, [SPEAK_GAZE_HE, g])
add("s04", [SPEAK_GAZE_SHE, "her face tilted up three-quarter to screen left toward the stove beyond the left edge of the frame, her eyes on it"])

# Xu Yan: his smirking angle-b nowhere; where he has only the two angle pictures, his portrait first and angle-a second.
XU_ALL = ["s02", "s03", "s05", "s12", "s13", "s14", "s15", "s20", "s21", "s23", "s35", "s37", "s40"]
XU_TWO = ["s15", "s20"]  # gen-dh sent angle-a and angle-b only (close-ups facing screen right)
for sid in XU_ALL:
    if sid not in XU_TWO:
        drop(sid, "xuyan-angle-b-l1.png")
# The rising steam under the workshop roof (extras' clear-air sentence would fight it).
for sid in ["s01", "s02", "s03", "s04", "s05", "s06", "s07", "s10", "s12", "s13", "s15", "s16", "s17"]:
    add(sid, [CLEAR, STEAM])

# Sets.
SWAP = {}
for sid in ["s01", "s03", "s04", "s05", "s06", "s07", "s10", "s12", "s13", "s15", "s16"]:
    SWAP[sid] = {TF: "set-tangfang-jia-l1.png"}
for sid in ["s08", "s09", "s11", "s14"]:
    SWAP[sid] = {TF: "set-tangfang-lu-l1.png"}
for sid in ["s18", "s22"]:
    SWAP[sid] = {PU: "set-xuji-pu-cabinet-l1.png"}
for sid in ["s30", "s30b", "s31", "s32", "s33", "s34"]:
    SWAP[sid] = {PU: "set-xuji-houjian-deng-l1.png"}  # review 建議 1: the free brightened back room
for sid in ["s25", "s40"]:
    SWAP[sid] = {SHIJI: "set-xianjie-l1.png"}
for sid in ["s26", "s27", "s28", "s29"]:
    SWAP[sid] = {SHIJI: "set-xianjie-weiji-l1.png"}
for sid in ["s35", "s37"]:
    SWAP[sid] = {SHIJI: "set-xianjie-xuji-l1.png"}
for sid in ["s36", "s38", "s39"]:
    SWAP[sid] = {SHIJI: "set-xianjie-shi-l1.png"}
for sid in XU_TWO:
    SWAP.setdefault(sid, {})["xuyan-angle-a-l1.png"] = "xuyan-portrait-l1.png"
    SWAP[sid]["xuyan-angle-b-l1.png"] = "angles/xuyan-angle-a-l1.png"
KEEP_SET = ["s02", "s17", "s19", "s20", "s21", "s23", "s24"]  # gen-dh's own pictures: set-tangfang-l1, set-xuji-pu-l1
for sid, sw in SWAP.items():
    shots[sid]["swap_pictures"] = sw
assert sorted(set(SWAP) | set(KEEP_SET)) == sorted(ids), sorted(set(ids) - set(SWAP) - set(KEEP_SET))
for v in shots.values():
    for k in list(v.get("swap_pictures", {}).values()) + v.get("add_pictures", []):
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e926 live d1 (e925-live's way after its review, written by mkspec.py). Tang Xiaotang never shows her mouth or her "
              "face: five speaking back shots (s01, s07, s12, s21, s24) drop her three pictures and her identity sentence; the "
              "silent back shot s23 never lists her. No person sent in s06, s18, s22, s25, s27, s31, s33, s36, s38, s39. Sets: "
              "set-tangfang-l1 (s02, s17), set-tangfang-jia-l1 (workshop close shots), set-tangfang-lu-l1 (s08, s09, s11, s14), "
              "set-xuji-pu-l1 (s19-s21, s23, s24), set-xuji-pu-cabinet-l1 (s18, s22), set-xuji-houjian-deng-l1 (s30-s34), "
              "set-xianjie-l1 (s25, s40), set-xianjie-weiji-l1 (s26-s29), set-xianjie-xuji-l1 (s35, s37), set-xianjie-shi-l1 "
              "(s36, s38, s39) (prep926.sh swaps with absolute paths). Xu Yan's angle-b nowhere (s15, s20 send his portrait then "
              "angle-a). s04 adds Xiaohe's angle-a. The seven inserts never say 'open'. Steam under the workshop roof. No off-screen sentence (r2.py OFFSCREEN_SPEECH = False). Seeds "
              "9261101/9261102."),
    "seeds": [9261101, 9261102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
