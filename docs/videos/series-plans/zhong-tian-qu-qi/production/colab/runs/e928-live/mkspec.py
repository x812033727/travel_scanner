"""Writes spec.json next to this file: e928 live d1 (e927-live/spec.json's way after its review, with the e924-e926 picks).
Run: python3 -I mkspec.py

- Tang Xiaotang never shows her mouth or her face (bible rule 3): her five speaking back shots (s08, s11, s16, s21, s34) drop her
  three pictures and her identity sentence (it also names the abacus at her waist, rule 20); the 'only' sentence says she is seen
  from behind and appears once (s08, s16: Xu Yan beyond her, e926's back()).
- A-ling wears the veil (bible rule 21): every shot of her sends aling-veil-portrait-l1 in place of her portrait and drops her two
  angle pictures (they have no veil; a picture beats the text). In the close-ups s02, s07, s12 gen-dh sent only the two angles:
  angle-a becomes the veil portrait, angle-b is dropped. extras.json adds the veil to her cast sentence and takes the red lips out.
- Xu Yan's smirking angle-b nowhere (e921 review; prep's smile-ref warning on s08). In the close-ups s15, s23, s25, s32 gen-dh sent
  only angle-a and angle-b: his portrait goes first and angle-a second (e925 review 建議, e926/e927's XU_TWO).
- No person sent: s03b (one man and a sleeved hand), s04 (the sticks), s10 (a hand and the silver), s28 (the food box and a hand).
  The set clause opens the sentence.
- The unnamed people the compositions describe (rules 2, 25) are named in the 'only' sentence so they are allowed in frame, with
  their counts (the young woman's back in s01, the men with sticks, the sleeved hands, the backs in the foreground, the townspeople).
  Where the composition already says "he/she is the only person in the frame", the appended 'only' sentence is cut down to its
  second half (e927 review 建議: the same sentence twice).
- The three inserts never say "open" (e926 review 必改 1): "the very first frame is already a close view of".
- The speaking gaze never names an unsent listener (e927 必改 5): the person spoken to off screen is "someone out of sight beyond the
  left/right edge of the frame", or the gaze names the thing looked at.
- Sets (r2.py PLACES): the lane set-chouduan-ye-xiang-l2 (s01-s07, s03b); the yamen steps set-xianya-steps-l2 (s08, s09, s11-s17, s15b)
  and set-xianya-steps-shi-l1 (s10); the court hall set-xianya-gongtang-dais-l1 (s18, s20, s22) and -floor-l1 (s19, s21, s23-s25);
  the jail set-dalao-l1 as gen-dh sends it (s26, s27, s31), set-dalao-di-l1 (s28), set-dalao-bi-l1 (s29, s30, s32); the square
  set-guangchang-tai-l1 (s33, s39), -zuo-l1 (s34), -shu-l1 (s35, s36, s38), -you-l1 (s37). gen-dh's set-chouduan-l1, set-xianya-l1
  and set-guangchang-l1 are never sent. Every swap is sent with an absolute path by prep928.sh.
- No seed of this episode has been run. Seeds 9281101/9281102.
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
TANG_ID = f"Tang Xiaotang shown in <Picture 1>, <Picture 2> and <Picture 3> (the same woman from several angles) {TANG_BODY}"
TANG_PICS = ["tangxiaotang-portrait-l1.png", "tangxiaotang-angle-a-l1.png", "tangxiaotang-angle-b-l1.png"]
ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."
ONLY_2 = "Only these 2 people are in the frame; no second copy of anyone appears."
BESIDES_HIM = "Besides him, only the other people the composition names are in the frame; no second copy of anyone appears."
BESIDES_HER = "Besides her, only the other people the composition names are in the frame; no second copy of anyone appears."
BESIDES_THEM = "Besides them, only the other people the composition names are in the frame; no second copy of anyone appears."
NO_COPY = "No second copy of anyone appears."
ONE_TANG = "the young woman with the two high round buns appears only once"
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."

CD = "set-chouduan-l1.png"
YA = "set-xianya-l1.png"
DL = "set-dalao-l1.png"
GC = "set-guangchang-l1.png"


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


def only(what):
    return f"Only {what} are in the frame; no second copy of anyone appears."


def besides(pr, what):
    return f"Besides {pr}, only {what} the composition describes are in the frame; no second copy of anyone appears."


def back(beyond, n=2):
    return (f"Only these {n} people are in the frame, the young woman with the buns seen only from behind and {beyond} "
            f"beyond her; {ONE_TANG}; no second copy of anyone appears.")


ids = ["s01", "s02", "s03", "s03b"] + [f"s{n:02d}" for n in range(4, 16)] + ["s15b"] + [f"s{n:02d}" for n in range(16, 40)]
shots = {sid: {} for sid in ids}

# Tang Xiaotang from behind, speaking: her identity sentence and her three pictures leave.
ALONE = f"She is the only person in the frame, seen only from behind; {ONE_TANG}; no second copy of anyone appears."
for sid, onl in [
    ("s08", [ONLY_2, back("Xu Yan at the edge of the top step")]),
    ("s11", [ONLY_SHE, ALONE]),
    ("s16", [ONLY_2, back("Xu Yan close by")]),
    ("s21", [ONLY_SHE, ALONE]),
    ("s34", [ONLY_SHE, ALONE]),
]:
    add(sid, [TANG_ID, ""])
    add(sid, onl)
    drop(sid, *TANG_PICS)
for sid in ["s11", "s21", "s34"]:  # the set clause now opens the sentence (renumbered to 1 by the drop)
    add(sid, ["cinema camera. the location shown in <Picture 4>", "cinema camera. The location shown in <Picture 4>"])

# No person sent: the set clause opens the sentence.
NOPERSON = ["s03b", "s04", "s10", "s28"]
for sid in NOPERSON:
    add(sid, [SET_CLAUSE, "T" + SET_CLAUSE[1:]])

# The unnamed people the compositions describe, with their counts.
add("s01", [BESIDES_HIM, besides("him", "the soft back of the young woman in the left foreground and the two men with sticks")])
add("s02", [BESIDES_HER, ONLY_SHE])
add("s03", [ONLY_SHE, besides("her", "the one man with the stick")])
add("s05", [ONLY_HE, besides("him", "the one grey-white sleeved hand at the left edge")])
add("s06", [BESIDES_THEM, besides("them", "the two men lying on the stones further down the lane")])
add("s07", [ONLY_SHE, besides("her", "the two tied wrists at the lower edge")])
add("s13", [ONLY_HE, besides("him", "the soft back of the young woman's shoulder in the right foreground")])
add("s14", [ONLY_SHE, besides("her", "the soft back of the young man in the left foreground")])
add("s18", [ONLY_HE, besides("him", "the soft back of the kneeling man in the foreground")])
add("s29", [ONLY_HE, besides("him", "the soft shoulder of the thin man at the left edge")])
add("s32", [ONLY_HE, besides("him", "the one black-sleeved forearm at the lower edge")])
add("s33", [ONLY_2, only("these 2 named people, the back of the kneeling man and the eight townspeople the composition describes")])
add("s37", [ONLY_HE, besides("him", "the soft shoulder of the townsman in the foreground")])
add("s39", [ONLY_HE, besides("him", "the eight townspeople in the foreground")])
# the composition already says it (e927 review 建議: no doubled 'only' sentence)
for sid, sent in [("s12", ONLY_SHE), ("s15", ONLY_HE), ("s15b", ONLY_HE), ("s19", ONLY_HE), ("s23", ONLY_HE), ("s24", ONLY_SHE), ("s25", ONLY_HE),
                  ("s26", ONLY_HE), ("s30", ONLY_HE), ("s35", ONLY_HE), ("s36", ONLY_HE), ("s38", ONLY_HE)]:
    add(sid, [sent, NO_COPY])

# The inserts never say "open" (e926 review 必改 1).
for sid in ["s04", "s10", "s28"]:
    add(sid, ["the shot opens directly on", "the very first frame is already a close view of"])

# Lines not said into a face on screen: the speaking gaze names the listener off screen, or the thing looked at.
SPEAK_GAZE_HE = "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person"
for sid, g in [
    ("s05", "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
    ("s17", "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
    ("s18", "his face three-quarter to screen left toward the kneeling man below the desk, his eyes on him"),
    ("s19", "his face three-quarter to screen right toward someone out of sight beyond the upper right edge of the frame, his eyes on that spot"),
    ("s20", "his face three-quarter to screen left toward the floor below the desk, his eyes on it"),
    ("s22", "his face three-quarter to screen left toward the floor below the desk, his eyes on it"),
    ("s23", "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
    ("s25", "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
    ("s32", "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"),
    ("s35", "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
    ("s36", "his face three-quarter to screen right toward the middle of the platform below, his eyes on it"),
    ("s38", "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
]:
    add(sid, [SPEAK_GAZE_HE, g])

# A-ling: the veil portrait for her portrait, her angle pictures dropped (s02, s07, s12: angle-a becomes the veil portrait).
ALING_ALL = ["s02", "s03", "s06", "s07", "s09", "s12", "s14", "s24"]
ALING_TWO = ["s02", "s07", "s12"]
for sid in ALING_ALL:
    if sid in ALING_TWO:
        drop(sid, "aling-angle-b-l1.png")
    else:
        drop(sid, "aling-angle-a-l1.png", "aling-angle-b-l1.png")

# Xu Yan: his smirking angle-b nowhere; where he has only the two angle pictures, his portrait first and angle-a second.
XU_ALL = ["s08", "s13", "s15", "s15b", "s16", "s17", "s23", "s25", "s26", "s31", "s32", "s33", "s39"]
XU_TWO = ["s15", "s23", "s25", "s32"]  # gen-dh sent angle-a and angle-b only (close-ups)
for sid in XU_ALL:
    if sid not in XU_TWO:
        drop(sid, "xuyan-angle-b-l1.png")

# Sets.
SWAP = {}
for sid in ["s01", "s02", "s03", "s03b", "s04", "s05", "s06", "s07"]:
    SWAP[sid] = {CD: "set-chouduan-ye-xiang-l2.png"}
for sid in ["s08", "s09", "s11", "s12", "s13", "s14", "s15", "s15b", "s16", "s17"]:
    SWAP[sid] = {YA: "set-xianya-steps-l2.png"}
SWAP["s10"] = {YA: "set-xianya-steps-shi-l1.png"}
for sid in ["s18", "s20", "s22"]:
    SWAP[sid] = {YA: "set-xianya-gongtang-dais-l1.png"}
for sid in ["s19", "s21", "s23", "s24", "s25"]:
    SWAP[sid] = {YA: "set-xianya-gongtang-floor-l1.png"}
for sid in ["s26", "s27", "s31"]:
    SWAP[sid] = {}  # set-dalao-l1 as gen-dh sends it
SWAP["s28"] = {DL: "set-dalao-di-l1.png"}
for sid in ["s29", "s30", "s32"]:
    SWAP[sid] = {DL: "set-dalao-bi-l1.png"}
for sid in ["s33", "s39"]:
    SWAP[sid] = {GC: "set-guangchang-tai-l1.png"}
SWAP["s34"] = {GC: "set-guangchang-zuo-l1.png"}
for sid in ["s35", "s36", "s38"]:
    SWAP[sid] = {GC: "set-guangchang-shu-l1.png"}
SWAP["s37"] = {GC: "set-guangchang-you-l1.png"}
for sid in XU_TWO:
    SWAP[sid]["xuyan-angle-a-l1.png"] = "xuyan-portrait-l1.png"
    SWAP[sid]["xuyan-angle-b-l1.png"] = "angles/xuyan-angle-a-l1.png"
for sid in ALING_ALL:
    if sid in ALING_TWO:
        SWAP[sid]["aling-angle-a-l1.png"] = "aling-veil-portrait-l1.png"
    else:
        SWAP[sid]["aling-portrait-l1.png"] = "aling-veil-portrait-l1.png"
assert sorted(SWAP) == sorted(ids), sorted(set(ids) - set(SWAP))
for sid, sw in SWAP.items():
    if sw:
        shots[sid]["swap_pictures"] = sw
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e928 live d1 (e927-live's way after its review, written by mkspec.py). Tang Xiaotang never shows her mouth or her "
              "face: her five speaking back shots (s08, s11, s16, s21, s34) drop her three pictures and her identity sentence. "
              "A-ling wears the veil: aling-veil-portrait-l1 for her portrait, her angle pictures dropped. No person sent in s03b, "
              "s04, s10, s28. Sets: set-chouduan-ye-xiang-l2 (s01-s07, s03b), set-xianya-steps-l2 (s08, s09, s11-s17, s15b), "
              "set-xianya-steps-shi-l1 (s10), set-xianya-gongtang-dais-l1 (s18, s20, s22), -floor-l1 (s19, s21, s23-s25), "
              "set-dalao-l1 (s26, s27, s31), set-dalao-di-l1 (s28), set-dalao-bi-l1 (s29, s30, s32), set-guangchang-tai-l1 (s33, "
              "s39), -zuo-l1 (s34), -shu-l1 (s35, s36, s38), -you-l1 (s37) (prep928.sh swaps with absolute paths). Xu Yan's angle-b "
              "nowhere (s15, s23, s25, s32 send his portrait then angle-a). The three inserts never say 'open'. No off-screen "
              "sentence (r2.py OFFSCREEN_SPEECH = False). Seeds 9281101/9281102."),
    "seeds": [9281101, 9281102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
