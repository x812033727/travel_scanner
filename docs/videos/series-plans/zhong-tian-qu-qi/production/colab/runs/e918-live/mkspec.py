"""Writes spec.json next to this file: e918 live d1 (e917-live/spec.json's way after its review, with the e913-e916 lessons).
Run: python3 -I mkspec.py"""
import json
from pathlib import Path

TANG_ID = ("Tang Xiaotang shown in <Picture 1>, <Picture 2> and <Picture 3> (the same woman from several angles) keeps exactly the same "
           "face, hair and costume as the pictures: East Asian young woman of eighteen, dazzling glamorous beauty: big round sparkling eyes "
           "with long lashes, glossy peach-pink lips, rosy cheeks, luminous fair skin, petite curvy figure, hair in two looped buns tied "
           "with pink silk ribbons and pearl pins, a peach-pink silk brocade ruqun: a light cross-collared short jacket wrapped shut across "
           "the chest in a low closed V, its hem at the waist covering the top of a pleated skirt tied at the waist with a ribbon bow and a "
           "small gold ornament, thick opaque silk and flowing sleeves, a small gold abacus hanging at her waist; ")
TANG_PICS = ["tangxiaotang-portrait-l1.png", "tangxiaotang-angle-a-l1.png", "tangxiaotang-angle-b-l1.png"]
XU_ID = ("Xu Yan shown in <Picture 1>, <Picture 2> and <Picture 3> (the same man from several angles) keeps exactly the same face, "
         "hair and costume as the pictures: East Asian young man of twenty-five, clean-cut handsome with thick brows, double-lidded "
         "bright eyes, straight nose and a firm mouth, tall and lean with broad shoulders, black hair gathered up into a topknot on the "
         "crown and tied with a cloth band, a few strands falling over his forehead, a faded blue-grey cotton scholar's robe patched at "
         "one elbow, cloth shoes; ")
QIAN_ID = ("Qian Yuanwai shown in <Picture 1>, <Picture 2> and <Picture 3> (the same man from several angles) keeps exactly the same "
           "face, hair and costume as the pictures: East Asian man of fifty, short and portly, round face, a thin eight-shaped moustache, "
           "small shrewd eyes, an ancient Chinese Song-dynasty rich landlord's dark gold silk cross-collared robe with roundel patterns "
           "and a small black cap, three gold rings on his fingers; ")
RINGS = [", three gold rings on his fingers;", ", wide sleeves, his hands hidden inside them;"]
FACE = ["dazzling glamorous beauty: big round sparkling eyes with long lashes, glossy peach-pink lips, rosy cheeks,",
        "a delicate beauty: big round clear eyes with long lashes, soft peach-pink lips, light rosy cheeks,"]
NEUTRAL = [FACE, ["flowing sleeves, a small gold abacus hanging at her waist",
                  "flowing sleeves, a small gold abacus hanging at her waist, her resting face composed, her lips closed"]]
ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."
ONLY_2 = "Only these 2 people are in the frame; no second copy of anyone appears."
SPEAK_GAZE = "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"
SPEAK_GAZE_HE = "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person"
FACES = ("Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the face, hair "
         "and costume only, never the mood.")
ACTING = ("Natural, realistic human motion and acting of real actors: each person keeps the identity, hair and costume of their "
          "reference pictures, while every visible face acts the emotion written above and changes with it; the pictures are "
          "neutral studio portraits, never copy their blank expression.")
HANDS = "Only hands move in this shot; the frame stays on the hands and what they hold from the first frame to the last."
# review.md 必改 1: e916 fix1's hair (two high round buns, short ribbons), as r2.py TBACK.
ONE_TANG = "the young woman with the two high round buns appears only once"
BACK2 = (f"Only these 2 people are in the frame, the young woman with the buns seen only from behind and Xu Yan facing us across the "
         f"table; {ONE_TANG}; no second copy of anyone appears.")


def besides(pr, what):
    return (f"Besides {pr}, only {what} the composition describes is in the frame, belonging to someone whose face is out of "
            f"the frame; no second copy of anyone appears.")


def tang_back(only_old, only_new, alone=False):
    # alone: she is the only named person, so her identity sentence opened the anchor and the set clause after it must
    # start the sentence instead
    first = [TANG_ID + "the location", "The location"] if alone else [TANG_ID, ""]
    return {"replace": [first, [only_old, only_new]], "drop_pictures": list(TANG_PICS)}


def add(sid, key, value):
    shots[sid].setdefault(key, []).append(value) if key == "replace" else shots[sid].__setitem__(key, value)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + list(names)


shots = {f"s{n:02d}": {} for n in range(1, 41)}
shots["s37b"] = {}  # the script's c37 split in two (r2.py): s37 Qian Yuanwai asks, s37b Magistrate Hu grants it

# Tang Xiaotang's five on-screen lines (bible rule 3): from behind her; the 'only' sentence says so and that she appears once.
for sid in ["s03", "s06", "s13"]:
    shots[sid] = tang_back(ONLY_2, BACK2)                 # Xu Yan facing us across the table
shots["s04"] = tang_back(ONLY_SHE, f"Besides her, seen only from behind, only the thin man on the bench the composition describes is "
                                   f"in the frame, also seen only from behind with his face turned to the window; {ONE_TANG}; "
                                   f"no second copy of anyone appears.", True)
shots["s09"] = tang_back(ONLY_SHE, f"She is the only person in the frame, seen only from behind the whole shot; {ONE_TANG}; no second "
                                   f"copy of anyone appears.", True)
# Her silent face (s01, s31, s33): e907's neutral face sentences.
for sid in ["s01", "s31", "s33"]:
    shots[sid] = {"replace": [list(NEUTRAL[0]), list(NEUTRAL[1])]}

# The bookkeeper's hands (s05, s12): no person picture at all, the set is the one picture; hands only.
for sid in ["s05", "s12"]:
    shots[sid] = {"replace": [["shot on a cinema camera. the location shown in <Picture 1>", "shot on a cinema camera. The location shown in <Picture 1>"],
                              [ACTING, "Only one thin hand and its dark green sleeve are in the frame; its owner's face is never seen; "
                                       "no second copy of anyone appears. " + HANDS]]}

# The unnamed backs, heads and hands the compositions describe.
add("s01", "replace", [ONLY_2, "Only these 2 people and the one thin man on the bench by the window, seen only from behind, are in "
                               "the frame; no second copy of anyone appears."])
add("s08", "replace", [ONLY_HE, besides("him", "the back of the young woman's head and her shoulders in the foreground")])
add("s17", "replace", [ONLY_SHE, besides("her", "the back of the young man's head and his shoulder in the foreground")])
add("s19", "replace", [ONLY_HE, "Besides him, only the tops of the two heads behind the woodpile the composition describes are in "
                                "the frame, their faces hidden; no second copy of anyone appears."])
add("s21", "replace", [ONLY_SHE, besides("her", "the one hand in a grey cloth sleeve at the right edge")])
add("s23", "replace", [ONLY_HE, "Besides him, only the two small dark figures far back by the left wall are in the frame, too small "
                                "and dark to make out; no second copy of anyone appears."])
add("s35", "replace", [ONLY_HE, besides("him", "the back of the kneeling man's head, his shoulder and his sleeve in the foreground")])

# The hand inserts: one picture of the hand's owner, named only as the owner (e917 s20, s21). s16 Xu Yan's angle-a.
shots["s16"] = {"drop_set": True, "drop_pictures": ["xuyan-portrait-l1.png", "xuyan-angle-b-l1.png"],
                "replace": [[XU_ID, "The hand and sleeve belong to Xu Yan shown in <Picture 2>, whose face stays out of the frame; "],
                            [ONLY_HE, "Only his one hand and sleeve are in the frame; no second copy of anyone appears."],
                            [FACES + " ", ""], [ACTING, HANDS]]}
# s25, s26 Qian Yuanwai's hands: his portrait only (the rings and the sleeves), no set picture.
for sid in ["s25", "s26"]:
    shots[sid] = {"drop_set": True, "drop_pictures": ["qianyuanwai-angle-a-l1.png", "qianyuanwai-angle-b-l1.png"],
                  "replace": [[QIAN_ID, "The two hands and sleeves belong to Qian Yuanwai shown in <Picture 1>, whose face stays out of the "
                                        "frame; "],
                              [ONLY_HE, "Only his two hands and his sleeves are in the frame; no second copy of anyone appears."],
                              [FACES + " ", ""], [ACTING, HANDS]]}

# No set picture: the new workshop at night (s15-s22: set-zhifang-gujia-ye-l2 is e017's half-raised frame with a bonfire) and
# the lane behind the manor (s23, s27-s30: set-qianfu-ting-l1 is the hall).
for sid in ["s15", "s17", "s18", "s19", "s20", "s21", "s22", "s23", "s27", "s28", "s29", "s30"]:
    shots[sid]["drop_set"] = True
# retake.py cannot swap a picture; prep918.sh applies "swap_pictures" to colab-jobs.json after retake.py (absolute paths; the
# prompt text is unchanged). gen-dh gives the hall of the manor for "Qian manor" and the gate for "county yamen".
shots["s24"]["swap_pictures"] = {"set-qianfu-ting-l1.png": "set-qianfu-houmen-ye-l1.png"}
# review.md 必改 3, 12, 13: free crops (refs-live/README.md, new set ids with their own l1, so pilot.py's newest-l lookup of
# set-chalou and set-xianya-gongtang is untouched): the inserts s05, s12 get the bench; the floor shots get the hall without
# its desk, armchair and board; Magistrate Hu's two shots get the dais with the board out of the frame.
for sid in ["s05", "s12"]:
    shots[sid]["swap_pictures"] = {"set-chalou-l1.png": "set-chalou-bench-l1.png"}
for sid in ["s31", "s33", "s34", "s35", "s36", "s37", "s38"]:
    shots[sid]["swap_pictures"] = {"set-xianya-l1.png": "set-xianya-gongtang-floor-l1.png"}
for sid in ["s32", "s37b"]:
    shots[sid]["swap_pictures"] = {"set-xianya-l1.png": "set-xianya-gongtang-dais-l1.png"}
for sid in ["s39", "s40"]:
    shots[sid]["swap_pictures"] = {"set-xianya-l1.png": "set-xianya-ceting-l1.png"}

# By day Qian Yuanwai's hands are inside his sleeves: his cast sentence loses the rings (s31, s34, s36, s39, s40; s35 shows only
# his back, unnamed).
for sid in ["s31", "s34", "s36", "s37", "s39", "s40"]:
    add(sid, "replace", list(RINGS))

# Lines not said into a face on screen.
add("s10", "replace", [SPEAK_GAZE_HE, "his face three-quarter to screen right toward Tang Xiaotang off screen right, his eyes on the bundle"])
add("s11", "replace", [SPEAK_GAZE_HE, "his face three-quarter to screen right toward the open window at the right, his eyes on it"])
add("s14", "replace", [SPEAK_GAZE_HE, "his face three-quarter to screen right toward Tang Xiaotang off screen right, his eyes on her"])
add("s15", "replace", [SPEAK_GAZE_HE, "his face lowered toward the box, his eyes on the lid"])
add("s18", "replace", [SPEAK_GAZE_HE, "his face three-quarter to screen right toward Qin Shuang off screen right, his eyes on her"])
add("s20", "replace", [SPEAK_GAZE_HE, "his face lowered toward the box in his arms, his eyes on it"])
add("s21", "replace", [SPEAK_GAZE, "her face three-quarter to screen right toward Xu Yan off screen right, her eyes on him"])
add("s22", "replace", [SPEAK_GAZE_HE, "his face three-quarter to screen left toward Qin Shuang off screen left, his eyes on her"])
add("s24", "replace", [SPEAK_GAZE_HE, "his face three-quarter to screen right toward the box, his eyes on it"])
add("s31", "replace", [SPEAK_GAZE_HE, "his face tipped up toward the high dais above the top of the frame, his eyes on it"])
add("s32", "replace", [SPEAK_GAZE_HE, "his face three-quarter to screen left toward Xu Yan off screen left below him, his eyes on him"])
add("s33", "replace", [SPEAK_GAZE_HE, "his face tipped up toward the high dais above the top of the frame, his eyes on it"])
add("s34", "replace", [SPEAK_GAZE_HE, "his face three-quarter to screen left toward Xu Yan off screen left, his eyes on him"])
add("s36", "replace", [SPEAK_GAZE_HE, "his face three-quarter to screen left toward Xu Yan off screen left, his eyes on him and then darting away"])
add("s37", "replace", [SPEAK_GAZE_HE, "his face tipped up toward the high dais above the top of the frame, his eyes on it"])
add("s37b", "replace", [SPEAK_GAZE_HE, "his face three-quarter to screen right toward Qian Yuanwai off screen right, his eyes on him"])

# The crowded shots: Xu Yan's profile picture goes (e014-e017), and Tang Xiaotang's or Qian Yuanwai's profile beside it.
drop("s01", "xuyan-angle-b-l1.png", "tangxiaotang-angle-b-l1.png")
drop("s31", "xuyan-angle-b-l1.png", "tangxiaotang-angle-b-l1.png")
drop("s33", "xuyan-angle-b-l1.png", "tangxiaotang-angle-b-l1.png")
drop("s30", "xuyan-angle-b-l1.png")
for sid in ["s39", "s40"]:
    drop(sid, "xuyan-angle-b-l1.png", "qianyuanwai-angle-b-l1.png")

spec = {
    "_note": ("e918 live d1 (e917-live/spec.json's way after its review, written by mkspec.py). Tang Xiaotang never shows her mouth: "
              "s03, s06, s13 (Xu Yan across the table), s04 (at the window beside the bookkeeper) and s09 (alone) are from behind her "
              "(nospeak, recordings laid in): her three face pictures and her identity sentence go, and the 'only' sentence says she "
              "is seen from behind and appears once; s07 is Xu Yan's face with her line off screen. s01, s31, s33 are her silent face "
              "shots: e907's neutral face sentences. The bookkeeper has no picture: s05, s12 are his hands with the teahouse as the "
              "only picture, swapped for its bench crop set-chalou-bench-l1 (review 必改 3); s01, s04 admit his back (s11 is Xu Yan alone, 建議 4). No set picture for the workshop at night (s15-s22) and the lane (s23, "
              "s27-s30); s24 swaps the manor hall for set-qianfu-houmen-ye-l1 (the passage inside the back gate), the yamen gate for two crops of "
              "set-xianya-gongtang-l1 (review 必改 12, 13): the floor set-xianya-gongtang-floor-l1 for s31, s33-s38 and the dais "
              "set-xianya-gongtang-dais-l1 for Magistrate Hu's s32, s37b (the script's c37 is split into s37 and s37b), and s39-s40 for set-xianya-ceting-l1 (swap_pictures, applied by prep918.sh with "
              "absolute paths). Hand inserts: s16 (Xu Yan's angle-a), s25, s26 (Qian Yuanwai's portrait) send only the owner of the "
              "hands and lose the face sentences. By day (s31, s34, s36, s37, s39, s40) Qian Yuanwai's sentence loses the gold rings, his "
              "hands inside his sleeves. The speaking gaze names the listener off screen or the thing looked at (s10, s11, s14, s15, "
              "s18, s20-s22, s24, s31-s34, s36, s37, s37b). s01, s30, s31, s33, s39, s40 drop profile pictures. No off-screen sentence is in "
              "these prompts (r2.py OFFSCREEN_SPEECH = False). Seeds 9181101/9181102."),
    "seeds": [9181101, 9181102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
