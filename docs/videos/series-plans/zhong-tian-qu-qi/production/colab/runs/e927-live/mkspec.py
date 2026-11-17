"""Writes spec.json next to this file: e927 live d1 (e926-live/spec.json's way after its review, with the e921-e925 picks).
Run: python3 -I mkspec.py

- Tang Xiaotang never shows her mouth or her face (bible rule 3): her one speaking back shot (s05) drops her three pictures and
  her identity sentence (it also names the abacus at her waist, rule 20); the 'only' sentence says she is seen from behind and
  appears once.
- A-ling wears the veil (bible rule 21, the first episode with it): every shot of her sends aling-veil-portrait-l1 in place of
  her portrait and drops her two angle pictures (they have no veil; a picture beats the text). In the close-up s10 gen-dh sent
  only the two angles: angle-a becomes the veil portrait, angle-b is dropped. extras.json adds the veil to her cast sentence and
  takes the red lips out of it.
- Xu Yan's smirking angle-b nowhere (e921 review). In the close-ups s12, s19, s23 gen-dh sent only angle-a and angle-b (facing
  screen right): his portrait goes first and angle-a second (e925 review 建議, e926's XU_TWO; the swaps run in this order).
- No person sent: s04, s09, s22, s29, s35 (hands, the shadows), s13 (the two backs and the onlookers). The set clause opens the
  sentence.
- The unnamed people the compositions describe (rules 2, 25) are named in the 'only' sentence so they are allowed in frame, with
  their counts: the onlookers (s01, s13), the shoulder in black and the man on the ground (s02), the bearers (s03), the shoulder
  in sapphire brocade (s07), the young woman's back and the black-sleeved hand (s11), the young scholar's back (s14, s17), the
  two men with sticks (s37).
- The five inserts never say "open" (e926 review 必改 1): "the very first frame is already a close view of".
- The speaking gaze names the listener off screen, or the thing looked at; a line said to someone outside the frame (s12) is
  "toward someone out of sight beyond the right edge of the frame" (e925: never the young woman off screen).
- extras' "the air is clear and still" becomes still mist over the water at the bridge (s27-s33).
- Sets (r2.py PLACES): the street set-xianjie-weiji-l1 (s01, s03, s05), set-xianjie-xuji-l1 (s02, s04), set-xianjie-shi-l1
  (s06-s12), set-xianjie-l1 (s13); the court hall set-xianya-gongtang-floor-l1 (Xu Yan: s15, s19, s20, s22, s23) and
  set-xianya-gongtang-dais-l1 (Magistrate Hu: s14, s16-s18, s21, s24); the lane set-chouduan-ye-xiang-l1 (s25, s26, s34-s37); the
  bridge set-shiqiao-ye-l1 (s27), set-shiqiao-ye-dong-l1 (s28, s30, s31, s33), set-shiqiao-ye-shui-l1 (s29),
  set-shiqiao-ye-qiao-l1 (s32). gen-dh's set-shiji-l1, set-xianya-l1, set-chouduan-l1 and set-shiqiao-l2 are never sent. Every
  swap is sent with an absolute path by prep927.sh.
- No seed of this episode has been run. Seeds 9271101/9271102.
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
BESIDES_HIM = "Besides him, only the other people the composition names are in the frame; no second copy of anyone appears."
BESIDES_THEM = "Besides them, only the other people the composition names are in the frame; no second copy of anyone appears."
ONE_TANG = "the young woman with the two high round buns appears only once"
SPEAK_GAZE_HE = "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person"
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
CLEAR = "the air is clear and still, a clean natural film image"
MIST = "the thin mist lies still over the dark water, a clean natural film image"

SHIJI = "set-shiji-l1.png"
YA = "set-xianya-l1.png"
CD = "set-chouduan-l1.png"
SQ = "set-shiqiao-l2.png"


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


def only(what):
    return f"Only {what} are in the frame; no second copy of anyone appears."


def besides(pr, what):
    return f"Besides {pr}, only {what} the composition describes are in the frame; no second copy of anyone appears."


ids = [f"s{n:02d}" for n in range(1, 38)]
shots = {sid: {} for sid in ids}

# Tang Xiaotang from behind, speaking: her identity sentence and her three pictures leave.
add("s05", [TANG_ID, ""])
add("s05", [ONLY_SHE, f"She is the only person in the frame, seen only from behind; {ONE_TANG}; no second copy of anyone appears."])
drop("s05", *TANG_PICS)
add("s05", ["cinema camera. the location shown in <Picture 4>", "cinema camera. The location shown in <Picture 4>"])  # the sentence now opens with it (renumbered to 1 by the drop)

# No person sent: the set clause opens the sentence.
NOPERSON = ["s04", "s09", "s13", "s22", "s29", "s35"]
for sid in NOPERSON:
    add(sid, [SET_CLAUSE, "T" + SET_CLAUSE[1:]])

# The unnamed people the compositions describe, with their counts.
add("s01", [BESIDES_HIM, besides("him", "the two onlookers in the foreground")])
add("s02", [ONLY_HE, besides("him", "the man lying on the paving and the soft shoulder of the man in black in the foreground")])
add("s03", [BESIDES_HIM, besides("him", "the two men in black carrying the plank and the man lying on it, all small and soft,")])
add("s07", [ONLY_HE, besides("him", "the soft shoulder of the man in sapphire brocade in the foreground")])
add("s08", [BESIDES_HIM, ONLY_HE])
add("s11", [ONLY_HE, besides("him", "the soft back of the young woman's head in the foreground and the one black-sleeved hand at the right edge")])
add("s13", [BESIDES_THEM, only("the two men walking away and the four onlookers, all small,")])
add("s14", [ONLY_HE, besides("him", "the soft back of the young man in the foreground")])
add("s17", [ONLY_HE, besides("him", "the soft back of the young man in the foreground")])
add("s37", [BESIDES_THEM, besides("them", "the two men with sticks")])

# The inserts never say "open" (e926 review 必改 1).
for sid in ["s04", "s09", "s22", "s29", "s35"]:
    add(sid, ["the shot opens directly on", "the very first frame is already a close view of"])

# Lines not said into a face on screen: the speaking gaze names the listener off screen, or the thing looked at.
for sid, g in [
    ("s01", "his face three-quarter to screen left, his eyes on the paving beyond the lower left edge of the frame"),
    ("s03", "his face three-quarter to screen left toward Xu Yan off screen left, his eyes on him"),
    ("s08", "muttering to himself, his face turned toward screen right, his eyes on the street and the men in black by turns"),
    ("s12", "his face turned toward someone out of sight beyond the right edge of the frame, his eyes on that spot"),
    ("s15", "his face three-quarter to screen right toward the dais beyond the upper right edge of the frame, his eyes on it"),
    ("s16", "his face three-quarter to screen left toward the floor below the dais, his eyes on it"),
    ("s18", "his face three-quarter to screen left toward the floor below the dais, his eyes on it"),
    ("s20", "his face three-quarter to screen right toward the dais beyond the right edge of the frame, his eyes on it"),
    ("s21", "his face three-quarter to screen left toward the floor below the dais, his eyes on it"),
    ("s24", "his face three-quarter to screen left toward the far end of the hall beyond the left edge of the frame, his eyes on it"),
    ("s25", "muttering to himself, his head turned half back toward the far end of the lane, his eyes on it"),
    ("s28", "his face three-quarter to screen right toward Sun Zhanggui off screen right, his eyes on him"),
    ("s30", "his face three-quarter to screen left toward Lai San off screen left, his eyes on him"),
    ("s31", "his face three-quarter to screen right toward Sun Zhanggui off screen right, his eyes on him"),
    ("s33", "his face three-quarter to screen left toward Lai San off screen left, his eyes on him"),
    ("s34", "talking to himself, his face three-quarter to screen left, his eyes on the silver ingot in his hand"),
    ("s36", "his face turned toward the dark doorways beyond the right edge of the frame, his eyes on them"),
]:
    add(sid, [SPEAK_GAZE_HE, g])

# The bridge: still mist over the water instead of extras' clear air.
for sid in ["s27", "s28", "s29", "s30", "s31", "s32", "s33"]:
    add(sid, [CLEAR, MIST])

# A-ling: the veil portrait for her portrait, her angle pictures dropped (s10: angle-a becomes the veil portrait).
ALING_ALL = ["s10", "s26", "s32", "s37"]
drop("s10", "aling-angle-b-l1.png")
for sid in ["s26", "s32", "s37"]:
    drop(sid, "aling-angle-a-l1.png", "aling-angle-b-l1.png")

# Xu Yan: his smirking angle-b nowhere; where he has only the two angle pictures, his portrait first and angle-a second.
XU_ALL = ["s02", "s06", "s07", "s11", "s12", "s15", "s19", "s20", "s23"]
XU_TWO = ["s12", "s19", "s23"]  # gen-dh sent angle-a and angle-b only (close-ups facing screen right)
for sid in XU_ALL:
    if sid not in XU_TWO:
        drop(sid, "xuyan-angle-b-l1.png")

# Sets.
SWAP = {}
for sid in ["s01", "s03", "s05"]:
    SWAP[sid] = {SHIJI: "set-xianjie-weiji-l1.png"}
for sid in ["s02", "s04"]:
    SWAP[sid] = {SHIJI: "set-xianjie-xuji-l1.png"}
for sid in ["s06", "s07", "s08", "s09", "s10", "s11", "s12"]:
    SWAP[sid] = {SHIJI: "set-xianjie-shi-l1.png"}
SWAP["s13"] = {SHIJI: "set-xianjie-l1.png"}
for sid in ["s15", "s19", "s20", "s22", "s23"]:
    SWAP[sid] = {YA: "set-xianya-gongtang-floor-l1.png"}
for sid in ["s14", "s16", "s17", "s18", "s21", "s24"]:
    SWAP[sid] = {YA: "set-xianya-gongtang-dais-l1.png"}
for sid in ["s25", "s26", "s34", "s35", "s36", "s37"]:
    SWAP[sid] = {CD: "set-chouduan-ye-xiang-l1.png"}
SWAP["s27"] = {SQ: "set-shiqiao-ye-l1.png"}
for sid in ["s28", "s30", "s31", "s33"]:
    SWAP[sid] = {SQ: "set-shiqiao-ye-dong-l1.png"}
SWAP["s29"] = {SQ: "set-shiqiao-ye-shui-l1.png"}
SWAP["s32"] = {SQ: "set-shiqiao-ye-qiao-l1.png"}
for sid in XU_TWO:
    SWAP[sid]["xuyan-angle-a-l1.png"] = "xuyan-portrait-l1.png"
    SWAP[sid]["xuyan-angle-b-l1.png"] = "angles/xuyan-angle-a-l1.png"
SWAP["s10"]["aling-angle-a-l1.png"] = "aling-veil-portrait-l1.png"
for sid in ["s26", "s32", "s37"]:
    SWAP[sid]["aling-portrait-l1.png"] = "aling-veil-portrait-l1.png"
assert sorted(SWAP) == sorted(ids), sorted(set(ids) - set(SWAP))
for sid, sw in SWAP.items():
    shots[sid]["swap_pictures"] = sw
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e927 live d1 (e926-live's way after its review, written by mkspec.py). Tang Xiaotang never shows her mouth or her "
              "face: her one speaking back shot (s05) drops her three pictures and her identity sentence. A-ling wears the veil: "
              "aling-veil-portrait-l1 for her portrait, her angle pictures dropped (s10, s26, s32, s37). No person sent in s04, s09, "
              "s13, s22, s29, s35. Sets: set-xianjie-weiji-l1 (s01, s03, s05), set-xianjie-xuji-l1 (s02, s04), set-xianjie-shi-l1 "
              "(s06-s12), set-xianjie-l1 (s13), set-xianya-gongtang-floor-l1 (s15, s19, s20, s22, s23), set-xianya-gongtang-dais-l1 "
              "(s14, s16-s18, s21, s24), set-chouduan-ye-xiang-l1 (s25, s26, s34-s37), set-shiqiao-ye-l1 (s27), set-shiqiao-ye-dong-l1 "
              "(s28, s30, s31, s33), set-shiqiao-ye-shui-l1 (s29), set-shiqiao-ye-qiao-l1 (s32) (prep927.sh swaps with absolute "
              "paths). Xu Yan's angle-b nowhere (s12, s19, s23 send his portrait then angle-a). The five inserts never say 'open'. "
              "Still mist at the bridge. No off-screen sentence (r2.py OFFSCREEN_SPEECH = False). Seeds 9271101/9271102."),
    "seeds": [9271101, 9271102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
