"""Writes spec.json next to this file: e921 live d1 (e920-live/spec.json's way after its review and its fix1 lessons).
Run: python3 -I mkspec.py

- Tang Xiaotang never shows her mouth (bible rule 3): her five back shots (s04, s07 facing Wei Shaoqing; s09, s34, s35
  facing Xu Yan) drop her three pictures and her identity sentence; the 'only' sentence says she is seen from behind and
  appears once. s12 is her one face (silent): the softer face sentence of e907, the abacus out of her identity sentence (it
  is not in this episode, bible rule 20), e920 fix1's short ribbons, and her long-ribbon profile angle-b dropped.
- The unnamed backs and shoulders (rule 2) and the henchmen are named in the 'only' sentence so they are allowed in frame:
  Xu Yan's back s10, s28, s37; Wei Shaoqing's back s15, s27, s32; one henchman s22, s24.
- Sets (r2.py PLACES): the shop at dusk set-xuji-pu-dusk-l1 (s01-s19), at nightfall set-xuji-pu-ye-l1 (s20 on), the back
  yard set-xuji-houyuan-ye-l1 (s29, s31), the counter top for the four paper inserts set-xuji-pu-cabinet-l1 (s03, s06,
  s11, s16); every swap is a NEW id with its own l1 (rule 19), sent with an absolute path by prep921.sh. Close shots and Xu
  Yan's medium shots facing screen left (s15, s27, s32) send no set picture.
- Xu Yan's smirking angle-b only where he may smile (s27, s32: the cold mouth corner); the serious and crowded shots drop it.
- The speaking gaze names the listener off screen, or the thing looked at.
- No seed of this episode has been run. Seeds 9211101/9211102.

After the independent review (writer-tools/e021-r2/review.md; r2.py 〈AFTER THE INDEPENDENT REVIEW〉, 2026-11-16):
- s14b and s22b are new shots (s14, s22 split in two). s14b sends no set and no angle-b; s22b sends no set and allows the
  one henchman, who lies on the floor.
- s15, s27, s32: the person sentence is the review's ("Xu Yan appears only once, facing us beyond the blurred sapphire-blue
  shoulder"); Xu Yan's smiling angle-b is sent nowhere (s27, s32 keep his portrait and angle-a).
- s23: the rabbit leaves Xiaohe's identity sentence (her sash is plain; the one rabbit is in her hands).
- s29: A-ling's front-facing portrait is dropped (angle-b and angle-a only; "order_pictures" puts angle-b first, applied by
  prep921.sh), the back yard with the blank board painted out (set-xuji-houyuan-ye-l2); the person sentence allows the hand
  and sleeve at the lower right edge. s29 and s31 lose "an aloof piercing gaze" from her identity sentence. s31 sends the
  free crop without the door, set-xuji-houyuan-ye-nodoor-l1.
- s21b has no talking sentence now (nospeak in r2.py: one shout written in the motion), so no speaking-gaze edit.
- s26 is the reverse into the shop and sends no set picture; s28b's person sentence lets the staff in from the left edge."""
import json
from pathlib import Path

L = "/home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"

TANG_ID = ("Tang Xiaotang shown in <Picture 1>, <Picture 2> and <Picture 3> (the same woman from several angles) keeps exactly the same "
           "face, hair and costume as the pictures: East Asian young woman of eighteen, dazzling glamorous beauty: big round sparkling eyes "
           "with long lashes, glossy peach-pink lips, rosy cheeks, luminous fair skin, petite curvy figure, hair in two looped buns tied "
           "with pink silk ribbons and pearl pins, a peach-pink silk brocade ruqun: a light cross-collared short jacket wrapped shut across "
           "the chest in a low closed V, its hem at the waist covering the top of a pleated skirt tied at the waist with a ribbon bow and a "
           "small gold ornament, thick opaque silk and flowing sleeves, a small gold abacus hanging at her waist; ")
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
ONE_TANG = "the young woman with the two high round buns appears only once"
SPEAK_GAZE = "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"
SPEAK_GAZE_HE = "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person"
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
SET_SRC = "set-xuji-pu-l1.png"
DUSK, NIGHT, TOP = "set-xuji-pu-dusk-l1.png", "set-xuji-pu-ye-l1.png", "set-xuji-pu-cabinet-l1.png"
# the back yard: l2 = l1 with the blank board on the well frame painted out; the crop without the door for s31 (refs-live/README.md)
YARD, YARD_NODOOR = "set-xuji-houyuan-ye-l2.png", "set-xuji-houyuan-ye-nodoor-l1.png"
XU_ONCE = "Xu Yan appears only once, facing us beyond the blurred sapphire-blue shoulder; no second copy of anyone appears."
ALING_GAZE = [", a plain grey-white cotton dress tailored close at the waist with a cloth sash and long sleeves, an aloof piercing gaze;",
              ", a plain grey-white cotton dress tailored close at the waist with a cloth sash and long sleeves;"]


def back(beyond):
    return (f"Only these 2 people are in the frame, the young woman with the buns seen only from behind and {beyond} facing us "
            f"beyond her; {ONE_TANG}; no second copy of anyone appears.")


def tang_back(beyond):
    return {"replace": [[TANG_ID, ""], [ONLY_2, back(beyond)]], "drop_pictures": list(TANG_PICS)}


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + list(names)


def besides(pr, what):
    return f"Besides {pr}, only {what} the composition describes are in the frame; no second copy of anyone appears."


ids = ([f"s{n:02d}" for n in range(1, 15)] + ["s14b"] + [f"s{n:02d}" for n in range(15, 22)] + ["s21b", "s22", "s22b"]
       + [f"s{n:02d}" for n in range(23, 29)] + ["s28b"] + [f"s{n:02d}" for n in range(29, 38)])
shots = {sid: {} for sid in ids}

# Tang Xiaotang from behind.
for sid in ["s04", "s07"]:
    shots[sid] = tang_back("Wei Shaoqing")
for sid in ["s09", "s34", "s35"]:
    shots[sid] = tang_back("Xu Yan")
# Her one face.
shots["s12"] = {"replace": [FACE, NO_ABACUS, RIBBON], "drop_pictures": ["tangxiaotang-angle-b-l1.png"]}

# The unnamed backs and the henchmen the compositions describe.
add("s10", [ONLY_2, ("Only these 2 people and the young man seen only from behind in the foreground are in the frame; "
                     "no second copy of anyone appears.")])
for sid in ["s15", "s27", "s32"]:
    add(sid, [ONLY_HE, XU_ONCE])  # review 必改: never a second Xu Yan in the foreground
for sid in ["s28", "s37"]:
    add(sid, [ONLY_HE, besides("him", "the dark shoulder of the young man in the foreground")])
for sid in ["s22", "s22b", "s24"]:
    add(sid, [ONLY_SHE, besides("her", "the one burly man in black")])

# Lines not said into a face on screen: the speaking gaze names the listener off screen or the thing looked at.
for sid, g in [
    ("s02", "his face three-quarter to screen right toward the young man beyond the right edge of the frame, his eyes on him"),
    ("s05", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her"),
    ("s08", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her"),
    ("s10", "his face three-quarter to screen right toward the counter and the young man in the foreground, his eyes on them"),
    ("s13", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her"),
    ("s15", "his face turned three-quarter to screen right toward the far end of the counter beyond the right edge of the frame, his eyes on it"),
    ("s19", "his face three-quarter to screen right toward the young man beyond the right edge of the frame, his eyes on him"),
    ("s20", "his face three-quarter to screen right toward the counter beyond the right edge of the frame, his eyes on it"),
    ("s25", "his face three-quarter to screen right toward the men beyond the right edge of the frame, his eyes on them"),
    ("s30", "his face in profile to screen right toward the yard beyond the right edge of the frame, his eyes on it"),
    ("s33", "his face three-quarter to screen right toward the young man beyond the right edge of the frame, his eyes on him"),
    ("s37", "his eyes on the counter beyond the right edge of the frame, over the young man's shoulder"),
]:
    add(sid, [SPEAK_GAZE_HE, g])
add("s28b", [ONLY_HE, "He is the only person in the frame; the staff comes in from beyond the left edge; no second copy of anyone appears."])
# s23: the one rabbit is in her hands (review 必改)
add("s23", ["a small woven straw rabbit tucked into the cloth sash at her waist", "a plain cloth sash at her waist"])
# s29: the point of view (review 必改); s29, s31 without the gaze that pulls her eyes to the lens
add("s29", [ONLY_SHE, "She is the only person in the frame, with only the hand and sleeve at the lower right edge besides her; no second copy of anyone appears."])
for sid in ["s29", "s31"]:
    add(sid, ALING_GAZE)
drop("s29", "aling-portrait-l1.png")
shots["s29"]["order_pictures"] = ["aling-angle-b-l1.png", "aling-angle-a-l1.png", YARD]

# Xu Yan's smirking profile picture only where he may smile.
for sid in ["s01", "s09", "s14", "s14b", "s15", "s17", "s18", "s23", "s27", "s32", "s34", "s35"]:
    drop(sid, "xuyan-angle-b-l1.png")  # after the review: nowhere

# Sets.
DUSK_SET = ["s01", "s02", "s04", "s07", "s09", "s10", "s17", "s18"]
NIGHT_SET = ["s20", "s21", "s22", "s24", "s25", "s28b", "s34", "s35", "s36", "s37"]
NO_SET = ["s05", "s08", "s12", "s13", "s14", "s14b", "s15", "s19", "s21b", "s22b", "s23", "s26", "s27", "s28", "s30", "s32",
          "s33"]
INSERTS = ["s03", "s06", "s11", "s16"]
for sid in DUSK_SET:
    shots[sid]["swap_pictures"] = {SET_SRC: DUSK}
for sid in NIGHT_SET:
    shots[sid]["swap_pictures"] = {SET_SRC: NIGHT}
shots["s29"]["swap_pictures"] = {SET_SRC: YARD}
shots["s31"]["swap_pictures"] = {SET_SRC: YARD_NODOOR}
for sid in NO_SET:
    shots[sid]["drop_set"] = True
for sid in INSERTS:
    shots[sid]["swap_pictures"] = {SET_SRC: TOP}
    add(sid, [SET_CLAUSE, "T" + SET_CLAUSE[1:]])  # no person in the shot: the clause opens the sentence
assert sorted(DUSK_SET + NIGHT_SET + NO_SET + INSERTS + ["s29", "s31"]) == sorted(ids)
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e921 live d1 (e920-live's way after its review and fix1, written by mkspec.py). Tang Xiaotang never shows her "
              "mouth: five back shots drop her three pictures and her identity sentence; s12 is her one silent face (softer face "
              "sentence, no abacus, short ribbons, no angle-b). Sets: set-xuji-pu-dusk-l1 (s01-s19), set-xuji-pu-ye-l1 (s20 on), "
              "set-xuji-houyuan-ye-l2 (s29; the blank board painted out), the crop without the door set-xuji-houyuan-ye-nodoor-l1 (s31), set-xuji-pu-cabinet-l1 for the four paper inserts (s03, s06, s11, s16); close "
              "shots and Xu Yan's medium shots facing screen left send none (prep921.sh swaps with absolute paths). The unnamed "
              "backs and the henchmen are allowed in the 'only' sentence. The speaking gaze names the listener off screen. No "
              "off-screen sentence is in these prompts (r2.py OFFSCREEN_SPEECH = False). After the independent review: s14b and s22b "
              "added (s14, s22 split), the review's person sentences for s15, s27, s32, s28b, s29, Xu Yan's angle-b nowhere, "
              "s29 angle-b and angle-a only (order_pictures, applied by prep921.sh), one rabbit in s23, s26 without a set. "
              "Seeds 9211101/9211102."),
    "seeds": [9211101, 9211102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
