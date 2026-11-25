"""Writes spec.json next to this file: e929 live d1 (e928-live/spec.json's way after its review, with the e924-e927 picks).
Run: python3 -I mkspec.py

- Tang Xiaotang never shows her mouth or her face (bible rule 3): her nine speaking back shots (s02, s14, s16, s24, s26, s27, s30,
  s33, s35) drop her three pictures and her identity sentence (it also names the abacus at her waist, rule 20); the 'only'
  sentence says she is seen from behind and appears once (s27 with Xu Yan and the six customers, s30 with Wei Shaoqing beyond her,
  s35 with Xu Yan before her).
- Xu Yan's smirking angle-b nowhere (e921 review). In the close-ups s04, s29 gen-dh sent only angle-a and angle-b: his portrait goes
  first and angle-a second (e925 review 建議, e926-e928's XU_TWO). The wides and the platform medium (s01, s05, s12) send his
  portrait only (e928 s39 after its review: four pictures, Hu, Wei, Xu Yan, the set).
- No person sent: s10 (the sheet against the sun), s11 (the yellow sheet), s15 (the ledger and a hand), s21 (the silver and a hand),
  s28 (the chest and a hand). The set clause opens the sentence.
- The unnamed people the compositions describe (rules 2, 25) are named in the 'only' sentence so they are allowed in frame, with
  their counts (the kneeling man's back, the eight townspeople, the six customers, the hands). Where the composition already says
  "he/she is the only person in the frame", the appended 'only' sentence is cut down to its second half (e927 review 建議).
- The five inserts never say "open" (e926 review 必改 1): "the very first frame is already a close view of".
- The speaking gaze never names an unsent listener (e927 必改 5): the person spoken to off screen is "someone out of sight beyond the
  left/right edge of the frame", or the gaze names the place looked at (the square, the platform, the earth below it).
- s34's 「囡囡！」 is five characters or fewer ending in ！ (preflight's shout warning: painted as a subtitle, e053 s05): the d1 text
  quotes it without the ！ and says it is cried out. The recording and the subtitles keep 「囡囡！」.
- Every motion that opens a sentence after "never the mood. " is capitalised (e928 review 必改 1's fix, here for every shot).
- Sets (r2.py PLACES): noon: set-guangchang-tai-zhong-l1 (s01), -zuo-l1 (s02, s14, s26), -shu-l1 (s03, s04, s06-s09, s13, s16-s19,
  s22, s24, s25), -tai-l1 (s05, s12), -you-wu-l1 (s20, s23), and the new free pictures prop-liuye-zhi-xin-l1 (s10),
  prop-huangzhi-l1 (s11), set-guangchang-di-l1 (s15), set-guangchang-an-l1 (s21); afternoon (the bible's free grade):
  set-guangchang-pm-zuo-l1 (s27, s29), -pm-di-l1 (s28), -pm-tai-l1 (s30), -pm-shu-l1 (s31), -pm-you-wu-l1 (s32-s35). gen-dh's
  set-guangchang-l1 is never sent. Every swap is sent with an absolute path by prep929.sh.
- After the independent review (writer-tools/e029-r2/review.md, 2026-11-17): s27's 'only' sentence no longer counts her as named
  and says she is the only young woman in the frame (必改 5); s35 Xu Yan "one step before her in the right third" (必改 6); s30 Wei
  "beyond her right shoulder" (建議 1); s20 the hands "gripping his shoulders" (建議 4); s25's gaze "toward the square below at the
  lower right" (建議 5). The rest of the review is in r2.py (video.json) and prop-huangzhi-l1 (redone, same id).
- No seed of this episode has been run. Seeds 9291101/9291102.
"""
import json
from pathlib import Path

L = "/home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
VIDEO = "/home/user/zt-work/docs/videos/zhong-tian-qu-qi-e029-r2/video.json"

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
BESIDES_THEM = "Besides them, only the other people the composition names are in the frame; no second copy of anyone appears."
NO_COPY = "No second copy of anyone appears."
ONE_TANG = "the young woman with the two high round buns appears only once"
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
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
    return (f"Only these {n} people are in the frame, the young woman with the buns seen only from behind and {beyond}; "
            f"{ONE_TANG}; no second copy of anyone appears.")


ids = [f"s{n:02d}" for n in range(1, 36)]
shots = {sid: {} for sid in ids}

# Tang Xiaotang from behind, speaking: her identity sentence and her three pictures leave.
ALONE = f"She is the only person in the frame, seen only from behind; {ONE_TANG}; no second copy of anyone appears."
for sid, onl in [
    ("s02", [ONLY_SHE, ALONE]),
    ("s14", [ONLY_SHE, ALONE]),
    ("s16", [ONLY_SHE, ALONE]),
    ("s24", [ONLY_SHE, ALONE]),
    ("s26", [ONLY_SHE, ALONE]),
    # e029 review 必改 5: she is not a "named" person, and she is the only young woman (the customers are each an age)
    ("s27", [ONLY_2, "Only Xu Yan, the young woman seen only from behind and the six customers the composition describes are in "
                     f"the frame; she is the only young woman in the frame; {ONE_TANG}; no second copy of anyone appears."]),
    ("s30", [ONLY_2, back("Wei Shaoqing small on the platform beyond her right shoulder")]),
    ("s33", [ONLY_SHE, ALONE]),
    ("s35", [ONLY_2, back("Xu Yan one step before her in the right third of the frame")]),  # e029 review 必改 6
]:
    add(sid, [TANG_ID, ""])
    add(sid, onl)
    drop(sid, *TANG_PICS)
for sid in ["s02", "s14", "s16", "s24", "s26", "s33"]:  # the set clause now opens the sentence (renumbered to 1 by the drop)
    add(sid, ["cinema camera. the location shown in <Picture 4>", "cinema camera. The location shown in <Picture 4>"])

# No person sent: the set clause opens the sentence.
NOPERSON = ["s10", "s11", "s15", "s21", "s28"]
for sid in NOPERSON:
    add(sid, [SET_CLAUSE, "T" + SET_CLAUSE[1:]])

# The unnamed people the compositions describe, with their counts.
add("s01", [ONLY_3, only("these 3 named people and the back of the kneeling man the composition describes")])
for sid in ["s05", "s12"]:
    add(sid, [ONLY_3, only("these 3 named people, the back of the kneeling man and the eight townspeople the composition describes")])
add("s18", [BESIDES_THEM, ONLY_2])
add("s20", [ONLY_HE, besides("him", "the two hands gripping his shoulders")])  # e029 review 建議 4
add("s23", [ONLY_HE, besides("him", "the two black-sleeved hands at the edges")])
# the composition already says it (e927 review 建議: no doubled 'only' sentence)
for sid in ["s03", "s04", "s06", "s07", "s08", "s09", "s13", "s17", "s19", "s22", "s25", "s29", "s31", "s32", "s34"]:
    add(sid, [ONLY_HE, NO_COPY])

# The inserts never say "open" (e926 review 必改 1).
for sid in NOPERSON:
    add(sid, ["the shot opens directly on", "the very first frame is already a close view of"])

# Lines not said into a face on screen: the speaking gaze names the place looked at, or someone out of sight.
SPEAK_GAZE_HE = "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person"
LEFT = "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"
RIGHT = "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"
UP_LEFT = "his face turned up three-quarter to screen left toward the platform beyond the upper left edge of the frame, his eyes on it"
for sid, g in [
    ("s01", "his face three-quarter to screen left toward the square below the platform, his eyes on it"),
    ("s03", LEFT), ("s06", LEFT), ("s07", RIGHT), ("s08", LEFT), ("s13", LEFT),
    ("s17", "his face three-quarter to screen left toward someone out of sight beyond the lower left edge of the frame, his eyes on that spot"),
    ("s19", "his face three-quarter to screen right toward someone out of sight beyond the lower right edge of the frame, his eyes on that spot"),
    ("s20", UP_LEFT),
    ("s22", "his face turned down three-quarter to screen right toward the earth below the platform beyond the lower right edge of the frame, his eyes on it"),
    ("s23", UP_LEFT),
    ("s25", "his face three-quarter to screen right toward the square below at the lower right, his eyes on it"),  # e029 review 建議 5
    ("s31", LEFT), ("s34", LEFT),
]:
    add(sid, [SPEAK_GAZE_HE, g])

# s34: a quoted shout of five characters or fewer ending in ！ is painted as a subtitle (preflight warn shout, e053 s05).
add("s34", ["speaks a short Mandarin line, 「囡囡！」,", "speaks a short Mandarin line, 「囡囡」, crying it out,"])

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
XU_ALL = ["s01", "s03", "s04", "s05", "s07", "s09", "s12", "s18", "s27", "s29", "s35"]
XU_TWO = ["s04", "s29"]  # gen-dh sent angle-a and angle-b only (close-ups)
for sid in XU_ALL:
    if sid not in XU_TWO:
        drop(sid, "xuyan-angle-b-l1.png")
for sid in ["s01", "s05", "s12"]:  # three named people small in the frame: his portrait only (e928 s39 after its review)
    drop(sid, "xuyan-angle-a-l1.png")

# Sets.
SWAP = {}
SWAP["s01"] = {GC: "set-guangchang-tai-zhong-l1.png"}
for sid in ["s02", "s14", "s26"]:
    SWAP[sid] = {GC: "set-guangchang-zuo-l1.png"}
for sid in ["s03", "s04", "s06", "s07", "s08", "s09", "s13", "s16", "s17", "s18", "s19", "s22", "s24", "s25"]:
    SWAP[sid] = {GC: "set-guangchang-shu-l1.png"}
for sid in ["s05", "s12"]:
    SWAP[sid] = {GC: "set-guangchang-tai-l1.png"}
SWAP["s10"] = {GC: "prop-liuye-zhi-xin-l1.png"}
SWAP["s11"] = {GC: "prop-huangzhi-l1.png"}
SWAP["s15"] = {GC: "set-guangchang-di-l1.png"}
for sid in ["s20", "s23"]:
    SWAP[sid] = {GC: "set-guangchang-you-wu-l1.png"}
SWAP["s21"] = {GC: "set-guangchang-an-l1.png"}
for sid in ["s27", "s29"]:
    SWAP[sid] = {GC: "set-guangchang-pm-zuo-l1.png"}
SWAP["s28"] = {GC: "set-guangchang-pm-di-l1.png"}
SWAP["s30"] = {GC: "set-guangchang-pm-tai-l1.png"}
SWAP["s31"] = {GC: "set-guangchang-pm-shu-l1.png"}
for sid in ["s32", "s33", "s34", "s35"]:
    SWAP[sid] = {GC: "set-guangchang-pm-you-wu-l1.png"}
for sid in XU_TWO:
    SWAP[sid]["xuyan-angle-a-l1.png"] = "xuyan-portrait-l1.png"
    SWAP[sid]["xuyan-angle-b-l1.png"] = "angles/xuyan-angle-a-l1.png"
assert sorted(SWAP) == sorted(ids), sorted(set(ids) - set(SWAP))
for sid, sw in SWAP.items():
    shots[sid]["swap_pictures"] = sw
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e929 live d1 (e928-live's way after its review, written by mkspec.py). Tang Xiaotang never shows her mouth or her "
              "face: her nine speaking back shots (s02, s14, s16, s24, s26, s27, s30, s33, s35) drop her three pictures and her "
              "identity sentence. No person sent in s10, s11, s15, s21, s28. Sets: noon set-guangchang-tai-zhong-l1 (s01), "
              "-zuo-l1 (s02, s14, s26), -shu-l1 (s03, s04, s06-s09, s13, s16-s19, s22, s24, s25), -tai-l1 (s05, s12), -you-wu-l1 "
              "(s20, s23), prop-liuye-zhi-xin-l1 (s10), prop-huangzhi-l1 (s11), set-guangchang-di-l1 (s15), -an-l1 (s21); "
              "afternoon set-guangchang-pm-zuo-l1 (s27, s29), -pm-di-l1 (s28), -pm-tai-l1 (s30), -pm-shu-l1 (s31), -pm-you-wu-l1 "
              "(s32-s35) (prep929.sh swaps with absolute paths). Xu Yan's angle-b nowhere (s04, s29 send his portrait then "
              "angle-a; s01, s05, s12 his portrait only). The five inserts never say 'open'. No off-screen sentence (r2.py "
              "OFFSCREEN_SPEECH = False). Seeds 9291101/9291102."),
    "seeds": [9291101, 9291102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
