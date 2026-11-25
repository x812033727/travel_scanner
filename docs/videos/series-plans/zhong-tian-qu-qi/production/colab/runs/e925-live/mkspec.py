"""Writes spec.json next to this file: e925 live d1 (e924-live/spec.json's way after its review, with the e921-e924 picks).
Run: python3 -I mkspec.py

- Tang Xiaotang never shows her mouth (bible rule 3), and in this episode never her face: her speaking back shots (s05, s07,
  s10, s11, s14 in the workshop; s19 on the jetty; s32, s36, s40 in scene 3) drop her three pictures and her identity sentence
  (it also names the abacus at her waist, rule 20); the 'only' sentence says she is seen from behind and appears once. Her
  silent back shots (s13, s16, s35, s38) never list her (no picture, never named).
- No person sent: s02, s12, s17, s39 (hands), s16, s38 (her back alone), s22, s31 (the boats, the youths), s23, s23b, s27,
  s29 (the Wei shop boy and the Wei men, unnamed, bible 〈小角色〉). The set clause opens the sentence.
- The unnamed people the compositions describe (rule 2, 25) are named in the 'only' sentence so they are allowed in frame, with
  their counts.
- Xu Yan's smirking angle-b nowhere (e921 review). Where gen-dh sent him only angle-a and angle-b (the close shots s15, s20,
  s40b), angle-b is swapped for his portrait l1 (two pictures of him, as in his other shots). His old grey outer coat at night
  (s20, s20b, s24, s34, s40, s40b; the script).
- extras' "the air is clear and still" becomes the drifting fog at night (s19-s40b); the workshop keeps it.
- The speaking gaze names the listener off screen, or the thing looked at.
- Sets (r2.py PLACES): the workshop s01 set-tangfang-l1 (gen-dh's, kept), every other scene-1 shot set-tangfang-jia-l1; the
  ferry landing (gen-dh's set-dukou-l2, pilot.py's newest, never sent): the wide shots s22, s31 set-dukou-ye-l1, the jetty
  set-dukou-ye-qiao-l1, the close shots and the muddy bank set-dukou-ye-wu-l1. Every swap is sent with an absolute path by
  prep925.sh.
- No seed of this episode has been run. Seeds 9251101/9251102.

AFTER THE INDEPENDENT REVIEW (writer-tools/e025-r2/review.md; 2026-11-17, the coordinator deciding for the owner; r2.py's
docstring has the whole list):
- s28 (必改 1): build-r2's "She is the only person in the frame" becomes the review's two-person sentence.
- The Wei shop boy is "the young man in dark red" in every 'only' sentence (s23, s23b, s29; 必改 2); s23 is a single file of
  nine small figures (建議); s31 six youths at the lower left and the three boatmen at the sterns (必改 4); s26 she is the only
  person (建議: the floating staff tips dropped).
- s25, s26, s30 (必改 6): Qin Shuang's angles/qinshuang-angle-a-l1 as <Picture 2> ("add_pictures": prep925.sh inserts it right
  after her portrait, absolute; the header, her identity sentence and the set clause are renumbered here). Not s28.
- s33 (必改 7): the jetty crop set-dukou-ye-qiao-l1 instead of the fog crop.
- Xu Yan's right-facing close-ups s15, s20, s40b (建議): his portrait first, angle-a second (angle-a -> portrait, angle-b ->
  angle-a; the swaps run in this order).
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
XU_COAT = ["a faded blue-grey cotton scholar's robe patched at one elbow, cloth shoes",
           "an old plain grey cloth outer coat worn loose over a faded blue-grey cotton scholar's robe patched at one elbow, cloth shoes"]
CLEAR = "the air is clear and still, a clean natural film image"
FOG = "the fog drifts slowly and evenly in the torchlight, a clean natural film image"

TF = "set-tangfang-l1.png"
DK = "set-dukou-l2.png"


def back(beyond, n=2):
    return (f"Only these {n} people are in the frame, the young woman with the buns seen only from behind and {beyond} "
            f"beyond her; {ONE_TANG}; no second copy of anyone appears.")


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


def only(what):
    return f"Only {what} are in the frame; no second copy of anyone appears."


ids = ([f"s{n:02d}" for n in range(1, 21)] + ["s20b", "s21", "s22", "s23", "s23b"] + [f"s{n:02d}" for n in range(24, 41)]
       + ["s40b"])
shots = {sid: {} for sid in ids}

# Tang Xiaotang from behind, speaking: her identity sentence and her three pictures leave.
ALONE = f"She is the only person in the frame, seen only from behind; {ONE_TANG}; no second copy of anyone appears."
for sid, onl in [
    ("s05", [ONLY_2, back("Wang Erniu facing us")]),
    ("s07", [ONLY_SHE, ALONE]),
    ("s10", [ONLY_SHE, ALONE]),
    ("s11", [ONLY_SHE, ALONE]),
    ("s14", [ONLY_2, back("Xu Yan sitting at her left")]),
    ("s19", [ONLY_2, back("Wang Erniu, small and also seen from behind, at the far end of the jetty")]),
    ("s32", [ONLY_2, back("Steward Zheng facing us")]),
    ("s36", [ONLY_2, back("Steward Zheng facing us")]),
    ("s40", [ONLY_2, back("Xu Yan crouching at her left")]),
]:
    add(sid, [tang_id(1), ""])
    add(sid, onl)
    drop(sid, *TANG_PICS)

# Her silent back shots with a named person (she is not listed: no picture, never named).
add("s13", [ONLY_HE, back("Xu Yan sitting at her left")])
add("s35", [ONLY_HE, back("Steward Zheng facing us")])

# The unnamed people the compositions describe, with their counts; no-person shots open with the set clause.
NOPERSON = ["s02", "s12", "s16", "s17", "s22", "s23", "s23b", "s27", "s29", "s31", "s38", "s39"]
for sid in NOPERSON:
    add(sid, [SET_CLAUSE, "T" + SET_CLAUSE[1:]])
add("s16", [" Initial composition:", f" {ALONE} Initial composition:"])
add("s38", [" Initial composition:", f" {ALONE} Initial composition:"])
add("s22", [" Initial composition:", " " + only("the three boatmen at the sterns, small and far, seen from behind,") + " Initial composition:"])
add("s23", [BESIDES_THEM, only("the young man in dark red and the eight men in grey running down the slope in one line, all small and side-on,")])
add("s23b", [BESIDES_THEM, only("the young man in dark red and the three men in grey on the slope behind him")])
add("s27", [BESIDES_THEM, only("the three youths and the three men in grey, all small and side-on,")])
add("s29", [" Initial composition:", " Only the young man in dark red is in the frame; no second copy of anyone appears. Initial composition:"])
add("s31", [BESIDES_THEM, only("the six youths at the lower left and the three boatmen at the sterns, all small,")])
# review 必改 1: the young man in dark red is not on chars, so build-r2 counts her alone
add("s28", [ONLY_SHE, "Only these 2 people are in the frame, Qin Shuang on the left and the thin young man in the dark red short jacket on the right; no second copy of anyone appears."])
# review 建議: s26's two floating staff tips are gone; she is alone
BESIDES_HER = "Besides her, only the other people the composition names are in the frame; no second copy of anyone appears."
add("s26", [BESIDES_HER, ONLY_SHE])
# review 必改 6: her angle-a (face three-quarter to screen left, as in these three) after her portrait, before the set
QIN_A = "angles/qinshuang-angle-a-l1.png"
for sid in ["s25", "s26", "s30"]:
    shots[sid]["add_pictures"] = [QIN_A]
    add(sid, ["For the target video, <Picture 1> and <Picture 2> are referenced throughout.",
              "For the target video, <Picture 1>, <Picture 2> and <Picture 3> are referenced throughout."])
    add(sid, ["Qin Shuang shown in <Picture 1> keeps", "Qin Shuang shown in <Picture 1> and <Picture 2> (the same woman from several angles) keeps"])
    add(sid, ["the location shown in <Picture 2> is the set", "the location shown in <Picture 3> is the set"])
# s01, s34 (two named people): ref2manifest's "Only these 2 people" stands.

# Lines not said into a face on screen: the speaking gaze names the listener off screen, or the thing looked at.
for sid, g in [
    ("s03", "his face three-quarter to screen right toward Wang Erniu off screen right, his eyes on him"),
    ("s04", "his face three-quarter to screen left toward Xu Yan off screen left, his eyes on him"),
    ("s06", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her"),
    ("s09", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her"),
    ("s15", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her"),
    ("s18", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her"),
    ("s21", "his face three-quarter to screen right toward the boat coming out of the fog, his eyes on it"),
    ("s24", "his face three-quarter to screen right toward Qin Shuang off screen right, his eyes on her"),
    ("s33", "his face three-quarter to screen left toward the young woman beyond the left edge of the frame, his eyes on her"),
    ("s37", "his face three-quarter to screen left toward the young woman beyond the left edge of the frame, his eyes on her"),
]:
    add(sid, [SPEAK_GAZE_HE, g])
for sid, g in [
    ("s26", "her face three-quarter to screen left toward the youths beyond the left edge of the frame, her eyes on them"),
    ("s30", "her face three-quarter to screen left toward the youths on the bank beyond the left edge of the frame, her eyes on them"),
]:
    add(sid, [SPEAK_GAZE_SHE, g])

# Xu Yan: his smirking angle-b nowhere; where he has only the two angle pictures, angle-b becomes his portrait.
XU_ALL = ["s01", "s03", "s08", "s13", "s14", "s15", "s20", "s20b", "s24", "s34", "s40", "s40b"]
XU_TWO = ["s15", "s20", "s40b"]  # gen-dh sent angle-a and angle-b only (close-ups)
for sid in XU_ALL:
    if sid not in XU_TWO:
        drop(sid, "xuyan-angle-b-l1.png")
# The grey outer coat at night.
for sid in ["s20", "s20b", "s24", "s34", "s40", "s40b"]:
    add(sid, XU_COAT)
# The drifting fog at night (extras' clear-air sentence would fight it).
NIGHT = ids[ids.index("s19"):]
for sid in NIGHT:
    add(sid, [CLEAR, FOG])

# Sets.
SWAP = {}
for sid in ids[ids.index("s02"):ids.index("s19")]:
    SWAP[sid] = {TF: "set-tangfang-jia-l1.png"}
for sid in ["s22", "s31"]:
    SWAP[sid] = {DK: "set-dukou-ye-l1.png"}
for sid in ["s19", "s21", "s24", "s26", "s30", "s32", "s33", "s34", "s35", "s36", "s37", "s38", "s39", "s40"]:
    SWAP[sid] = {DK: "set-dukou-ye-qiao-l1.png"}
for sid in ["s20", "s20b", "s23", "s23b", "s25", "s27", "s28", "s29", "s40b"]:
    SWAP[sid] = {DK: "set-dukou-ye-wu-l1.png"}
# review 建議: right-facing close-ups send his portrait first (as s20b); prep925.sh applies the swaps in this order
for sid in XU_TWO:
    SWAP.setdefault(sid, {})["xuyan-angle-a-l1.png"] = "xuyan-portrait-l1.png"
    SWAP[sid]["xuyan-angle-b-l1.png"] = "angles/xuyan-angle-a-l1.png"
KEEP_SET = ["s01"]  # gen-dh's own picture: set-tangfang-l1
for sid, sw in SWAP.items():
    shots[sid]["swap_pictures"] = sw
assert sorted(set(SWAP) | set(KEEP_SET)) == sorted(ids), sorted(set(ids) - set(SWAP) - set(KEEP_SET))
for v in shots.values():
    for k in list(v.get("swap_pictures", {}).values()) + v.get("add_pictures", []):
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e925 live d1 (e924-live's way after its review, written by mkspec.py). Tang Xiaotang never shows her mouth or her "
              "face: nine speaking back shots drop her three pictures and her identity sentence; four silent back shots never list "
              "her. No person sent in s02, s12, s16, s17, s22, s23, s23b, s27, s29, s31, s38, s39. Sets: set-tangfang-l1 (s01), "
              "set-tangfang-jia-l1 (s02-s18), set-dukou-ye-l1 (s22, s31), set-dukou-ye-qiao-l1 (the jetty), set-dukou-ye-wu-l1 "
              "(close shots and the bank; s33 the jetty after the review) (prep925.sh swaps with absolute paths). Xu Yan's angle-b "
              "nowhere (s15, s20, s40b send his portrait then angle-a); his grey outer coat at night. After the review: s28's two-person "
              "sentence; the young man in dark red; s31 six youths and three boatmen; Qin Shuang's angle-a in s25, s26, s30 "
              "(add_pictures, inserted after her portrait by prep925.sh). Fog at night s19-s40b. No off-screen sentence (r2.py "
              "OFFSCREEN_SPEECH = False). Seeds 9251101/9251102."),
    "seeds": [9251101, 9251102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
