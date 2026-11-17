"""Writes spec.json next to this file: e930 live d1 (e929-live/spec.json's way after its review, with the e924-e928 picks).
Run: python3 -I mkspec.py

- Tang Xiaotang never shows her mouth or her face (bible rule 3): her eight back shots (s02, s08, s13, s14, s20, s28, s29, s33)
  drop her three pictures and her identity sentence (it also names the abacus at her waist, rule 20); the 'only' sentence says
  she is seen from behind and appears once (s02 with Xu Yan before her, s08 with Qin Shuang beside her, s13 and s29 with her
  father before her). In s41 she is not a listed character (no picture is sent): the 'only' sentence names her as the young
  woman seen only from behind beside Xu Yan.
- Xu Yan's smirking angle-b nowhere (e921 review). In the close-ups s21, s21b gen-dh sent only angle-a and angle-b: his portrait
  goes first and angle-a second (e925 review 建議, e926-e929's XU_TWO). The wides s31, s41 send his portrait only.
- A-ling (bible rule 21): s09 wears the veil: aling-veil-portrait-l1 in place of her portrait, her two angle pictures dropped, and
  her cast sentence gets the veil. s38, s39, s41: the veil is blown off her face: her bare portrait (s39 had only the two angle
  pictures: her portrait first and angle-a second), never angle-b; s41 (a wide) her portrait only.
- No person sent: s17 (the ledger in two hands), s22 (the seed pouch in a hand), s32 (the torn halves). The set clause opens the
  sentence. Steward Zheng (s24) is sent with his l1 (tall and thin, the bible's two-shot whisper).
- The unnamed people the compositions describe (rules 2, 25) are named in the 'only' sentence so they are allowed in frame (s37 the
  woman at the well seen from behind, s36 the one horse). Where the composition already says "he/she is the only person in the
  frame", the appended 'only' sentence is cut down to its second half (e927 review 建議).
- The speaking gaze never names an unsent listener (e927 必改 5): the person spoken to off screen is "someone out of sight beyond the
  left/right edge of the frame", or the gaze names the place or thing looked at (the carriage, the bowl, the well).
- Every motion that opens a sentence after "never the mood. " is capitalised (e928 review 必改 1's fix).
- Sets (r2.py PLACES): scene 1 set-guangchang-pm-you-wu-l1 (s01-s04, s06), -pm-shu-l1 (s05); scenes 2-3 the free pictures of
  set-xujia-yuan-dong-l1: -dong-qing-l1 (the painted full yard: s31, s37, s41), -dong-men-l1 (s07, s08, s10, s35, s36, s40),
  -dong-jing-l1 (s09, s38, s39), -dong-wu-l1 (s11, s16, s19, s21, s21b), -dong-qiang-l1 (s12-s15, s18, s20, s23-s29, s33, s34),
  -dong-shu-l1 (s30), -dong-di-l1 (s17, s22, s32). gen-dh's set-guangchang-l1 and pilot.py's set-xujia-yuan-l3 are never sent.
  Every swap is sent with an absolute path by prep930.sh.
- No seed of this episode has been run. Seeds 9301101/9301102.
"""
import json
from pathlib import Path

L = "/home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
VIDEO = "/home/user/zt-work/docs/videos/zhong-tian-qu-qi-e030-r2/video.json"

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
ONLY_3 = "Only these 3 people are in the frame; no second copy of anyone appears."
NO_COPY = "No second copy of anyone appears."
ONE_TANG = "the young woman with the two high round buns appears only once"
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
GC = "set-guangchang-l1.png"
YD = "set-xujia-yuan-l3.png"  # pilot.py's newest set-xujia-yuan for gen-dh's dh-set-xujia-yuan-t1
VEIL_CAST = "an aloof piercing gaze, a veil of soft, finely woven pale grey gauze over her nose, mouth and chin"


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


def back(beyond, n=2):
    return (f"Only these {n} people are in the frame, the young woman with the buns seen only from behind and {beyond}; "
            f"{ONE_TANG}; no second copy of anyone appears.")


ids = [f"s{n:02d}" for n in range(1, 22)] + ["s21b"] + [f"s{n:02d}" for n in range(22, 42)]
shots = {sid: {} for sid in ids}

# Tang Xiaotang from behind: her identity sentence and her three pictures leave.
ALONE = f"She is the only person in the frame, seen only from behind; {ONE_TANG}; no second copy of anyone appears."
for sid, onl in [
    ("s02", [ONLY_2, back("Xu Yan one step before her in the right third of the frame")]),
    ("s08", [ONLY_2, back("Qin Shuang half a step beyond her in the left third of the frame")]),
    ("s13", [ONLY_2, back("Tang Wanjin one step beyond her in the right third of the frame")]),
    ("s14", [ONLY_SHE, ALONE]),
    ("s20", [ONLY_SHE, ALONE]),
    ("s28", [ONLY_SHE, ALONE]),
    ("s29", [ONLY_2, back("Tang Wanjin half a step beyond her in the right third of the frame")]),
    ("s33", [ONLY_SHE, ALONE]),
]:
    add(sid, [TANG_ID, ""])
    add(sid, onl)
    drop(sid, *TANG_PICS)
for sid in ["s14", "s20", "s28", "s33"]:  # the set clause now opens the sentence (renumbered to 1 by the drop)
    add(sid, ["cinema camera. the location shown in <Picture 4>", "cinema camera. The location shown in <Picture 4>"])

# No person sent: the set clause opens the sentence.
NOPERSON = ["s17", "s22", "s32"]
for sid in NOPERSON:
    add(sid, [SET_CLAUSE, "T" + SET_CLAUSE[1:]])

# The unnamed the compositions describe, and s41's young woman from behind (no picture).
add("s36", [ONLY_SHE, "She is the only person in the frame, beside the one horse the composition describes; no second copy of anyone appears."])
add("s37", [ONLY_HE, "Besides him, only the one woman seen from behind beside the well in the foreground the composition describes is in "
                     "the frame; no second copy of anyone appears."])
add("s41", [ONLY_3, f"Only A-ling, Wei Shaoqing, Xu Yan and the one young woman seen only from behind beside him are in the frame; "
                    f"{ONE_TANG}; no second copy of anyone appears."])
# the composition already says it (e927 review 建議: no doubled 'only' sentence)
for sid in ["s01", "s03", "s04", "s05", "s06", "s10", "s12", "s15", "s16", "s18", "s19", "s21", "s21b", "s23", "s26", "s27", "s30",
            "s34", "s40"]:
    add(sid, [ONLY_HE, NO_COPY])
for sid in ["s09", "s11", "s38", "s39"]:
    add(sid, [ONLY_SHE, NO_COPY])

# Lines not said into a face on screen: the speaking gaze names the place looked at, or someone out of sight.
GAZE_HE = "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person"
GAZE_SHE = "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"
LEFT = "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"
RIGHT = "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"
for sid, g in [
    ("s01", LEFT), ("s03", LEFT), ("s04", RIGHT), ("s05", LEFT),
    ("s06", "his face three-quarter to screen right toward the carriage at the right edge of the frame, his eyes on it"),
    ("s10", RIGHT),
    ("s12", "his eyes on the chipped rim of the bowl in his hands"),
    ("s15", LEFT), ("s16", RIGHT), ("s18", LEFT), ("s19", RIGHT), ("s23", LEFT), ("s26", LEFT), ("s27", RIGHT), ("s30", LEFT),
    ("s34", "his eyes on the earth at his feet, his face turning away toward the right edge of the frame"),
    ("s40", "his face three-quarter to screen right toward the well beyond the right edge of the frame, his eyes on it"),
]:
    add(sid, [GAZE_HE, g])
for sid, g in [
    ("s11", "her face turned up three-quarter to screen right toward someone out of sight beyond the upper right edge of the frame, her eyes on that spot"),
    ("s36", "her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, her eyes on that spot"),
]:
    add(sid, [GAZE_SHE, g])

# A-ling's veil (rule 21): only s09 wears it.
add("s09", ["an aloof piercing gaze", VEIL_CAST])

# Every motion that opens a sentence after "never the mood. " starts with a capital.
video = json.load(open(VIDEO, encoding="utf-8"))
for sc in video["scenes"]:
    sid, mo = sc["id"], sc["data"]["motion"]
    if mo.startswith("Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "):
        mo = mo.split("never the mood. ", 1)[1]
    if mo[:1].islower():
        head = mo[:24]
        add(sid, [f"never the mood. {head}", f"never the mood. {head[0].upper()}{head[1:]}"])

# Xu Yan: his smirking angle-b nowhere; where he has only the two angle pictures, his portrait first and angle-a second.
XU_ALL = ["s02", "s04", "s16", "s19", "s21", "s21b", "s31", "s35", "s41"]
XU_TWO = ["s21", "s21b"]  # gen-dh sent angle-a and angle-b only (close-ups)
for sid in XU_ALL:
    if sid not in XU_TWO:
        drop(sid, "xuyan-angle-b-l1.png")
for sid in ["s31", "s41"]:  # wides: his portrait only
    drop(sid, "xuyan-angle-a-l1.png")
# A-ling: the veil portrait in s09; her bare portrait (never angle-b) in s38, s39, s41.
drop("s09", "aling-angle-a-l1.png", "aling-angle-b-l1.png")
drop("s38", "aling-angle-b-l1.png")
drop("s41", "aling-angle-a-l1.png", "aling-angle-b-l1.png")

# Sets.
SWAP = {}
for sid in ["s01", "s02", "s03", "s04", "s06"]:
    SWAP[sid] = {GC: "set-guangchang-pm-you-wu-l1.png"}
SWAP["s05"] = {GC: "set-guangchang-pm-shu-l1.png"}
PLACE = {
    "set-xujia-yuan-dong-qing-l1.png": ["s31", "s37", "s41"],
    "set-xujia-yuan-dong-men-l1.png": ["s07", "s08", "s10", "s35", "s36", "s40"],
    "set-xujia-yuan-dong-jing-l1.png": ["s09", "s38", "s39"],
    "set-xujia-yuan-dong-wu-l1.png": ["s11", "s16", "s19", "s21", "s21b"],
    "set-xujia-yuan-dong-qiang-l1.png": ["s12", "s13", "s14", "s15", "s18", "s20", "s23", "s24", "s25", "s26", "s27", "s28", "s29",
                                         "s33", "s34"],
    "set-xujia-yuan-dong-shu-l1.png": ["s30"],
    "set-xujia-yuan-dong-di-l1.png": ["s17", "s22", "s32"],
}
for pic, sids in PLACE.items():
    for sid in sids:
        assert sid not in SWAP, sid
        SWAP[sid] = {YD: pic}
for sid in XU_TWO:
    SWAP[sid]["xuyan-angle-a-l1.png"] = "xuyan-portrait-l1.png"
    SWAP[sid]["xuyan-angle-b-l1.png"] = "angles/xuyan-angle-a-l1.png"
SWAP["s09"]["aling-portrait-l1.png"] = "aling-veil-portrait-l1.png"
SWAP["s39"]["aling-angle-a-l1.png"] = "aling-portrait-l1.png"
SWAP["s39"]["aling-angle-b-l1.png"] = "angles/aling-angle-a-l1.png"
assert sorted(SWAP) == sorted(ids), sorted(set(ids) ^ set(SWAP))
for sid, sw in SWAP.items():
    shots[sid]["swap_pictures"] = sw
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e930 live d1 (e929-live's way after its review, written by mkspec.py). Tang Xiaotang never shows her mouth or her "
              "face: her eight back shots (s02, s08, s13, s14, s20, s28, s29, s33) drop her three pictures and her identity "
              "sentence; s41 names her only as the young woman seen from behind. No person sent in s17, s22, s32. A-ling: s09 the "
              "veil portrait, no angles; s38, s39, s41 her bare portrait, never angle-b. Xu Yan's angle-b nowhere (s21, s21b send "
              "his portrait then angle-a; s31, s41 his portrait only). Sets: scene 1 set-guangchang-pm-you-wu-l1 (s01-s04, s06), "
              "-pm-shu-l1 (s05); the yard set-xujia-yuan-dong-qing-l1 (s31, s37, s41) and its crops -men-l1 (s07, s08, s10, s35, "
              "s36, s40), -jing-l1 (s09, s38, s39), -wu-l1 (s11, s16, s19, s21, s21b), -qiang-l1 (s12-s15, s18, s20, s23-s29, s33, "
              "s34), -shu-l1 (s30), -di-l1 (s17, s22, s32) (prep930.sh swaps with absolute paths). No off-screen sentence (r2.py "
              "OFFSCREEN_SPEECH = False). Seeds 9301101/9301102."),
    "seeds": [9301101, 9301102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
