"""Writes spec.json next to this file: e919 live d1 (e918-live/spec.json's way after its review, with the e918 picking lessons:
picks-merged.tsv, fix1/mkspec.py, fix2/mkspec.py). Run: python3 -I mkspec.py

After the independent review (writer-tools/e019-r2/review.md, 2026-11-16; r2.py 〈AFTER THE INDEPENDENT REVIEW〉):
- 必改 3 / 建議: the hand inserts s11, s13 send the owners' sleeve crops (laisan-sleeve-l1, qianyuanwai-sleeve-l1: the portraits
  below the collar, no face), named only as cloth, no person's name in the identity sentence.
- 必改 4: s23 sends no picture of Qian Yuanwai and has no name (e918 fix2 s37's back-view way, untested yet): one costume
  sentence, the floor picture only.
- 必改 6, 7: s04 is Qin Shuang and Lai San with an unnamed kneeling back at the right edge; s37 is Qin Shuang alone.
- 必改 13: Qian Yuanwai's angle-b (a hanging knot behind a two-layer cap) goes everywhere; s09, s15, s17, s19 (angle-a + angle-b
  from gen-dh) swap to the portrait + angle-a.
- 必改 14, 15: set-xianya-steps-l2 for s28-s37; set-wuding-eave-l2 for s38 only, s39-s41 drop the set picture.
- 必改 17: s28 has no yamen hands."""
import json
from pathlib import Path

TANG_ID = ("Tang Xiaotang shown in <Picture 1>, <Picture 2> and <Picture 3> (the same woman from several angles) keeps exactly the same "
           "face, hair and costume as the pictures: East Asian young woman of eighteen, dazzling glamorous beauty: big round sparkling eyes "
           "with long lashes, glossy peach-pink lips, rosy cheeks, luminous fair skin, petite curvy figure, hair in two looped buns tied "
           "with pink silk ribbons and pearl pins, a peach-pink silk brocade ruqun: a light cross-collared short jacket wrapped shut across "
           "the chest in a low closed V, its hem at the waist covering the top of a pleated skirt tied at the waist with a ribbon bow and a "
           "small gold ornament, thick opaque silk and flowing sleeves, a small gold abacus hanging at her waist; ")
TANG_PICS = ["tangxiaotang-portrait-l1.png", "tangxiaotang-angle-a-l1.png", "tangxiaotang-angle-b-l1.png"]
LAI_ID = ("Lai San shown in <Picture 1> keeps exactly the same face, hair and costume as the pictures: East Asian young man of "
          "twenty-eight, small and thin, pointed chin, shifty eyes, a slight limp, an ancient Chinese Song-dynasty peasant's grey-brown "
          "hemp cross-collared short jacket and an old cloth head wrap; ")
QIAN_ID13 = ("Qian Yuanwai shown in <Picture 2>, <Picture 3> and <Picture 4> (the same man from several angles) keeps exactly the same "
             "face, hair and costume as the pictures: East Asian man of fifty, short and portly, round face, a thin eight-shaped moustache, "
             "small shrewd eyes, an ancient Chinese Song-dynasty rich landlord's dark gold silk cross-collared robe with roundel patterns "
             "and a small black cap, three gold rings on his fingers; ")
# e918 fix1 (s35, s37, s40): the portrait's tall round smooth cap (a small cap grew two hanging tails like an official's futou)
# and its round collar; by day before s12 and wherever his hands are out of the frame, no gold rings (his hands are hidden).
QIAN_COSTUME = "dark gold silk cross-collared robe with roundel patterns and a small black cap, three gold rings on his fingers;"
CAP = "tall round smooth black cap, plain and smooth all the way round down to its rim"
NEW_COSTUME = "dark gold silk round-collared robe with roundel patterns, a white inner collar at his neck, and a " + CAP
QIAN_HIDDEN = [QIAN_COSTUME, NEW_COSTUME + ", long wide sleeves, his hands hidden inside them;"]
QIAN_BEHIND = [QIAN_COSTUME, NEW_COSTUME + ", his hands out of sight behind his back;"]
QIAN_OUT = [QIAN_COSTUME, NEW_COSTUME + ", long wide sleeves, his hands below the frame;"]
QIAN_RINGS = [QIAN_COSTUME, NEW_COSTUME + ", three gold rings on his fingers;"]
FACE = ["dazzling glamorous beauty: big round sparkling eyes with long lashes, glossy peach-pink lips, rosy cheeks,",
        "a delicate beauty: big round clear eyes with long lashes, soft peach-pink lips, light rosy cheeks,"]
NEUTRAL = [FACE, ["flowing sleeves, a small gold abacus hanging at her waist",
                  "flowing sleeves, a small gold abacus hanging at her waist, her resting face composed, her lips closed"]]
ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."
ONLY_2 = "Only these 2 people are in the frame; no second copy of anyone appears."
S01_ONLY = "Besides them, only the other people the composition names are in the frame; no second copy of anyone appears."
SPEAK_GAZE = "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"
SPEAK_GAZE_HE = "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person"
FACES = ("Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the face, hair "
         "and costume only, never the mood.")
ACTING = ("Natural, realistic human motion and acting of real actors: each person keeps the identity, hair and costume of their "
          "reference pictures, while every visible face acts the emotion written above and changes with it; the pictures are "
          "neutral studio portraits, never copy their blank expression.")
HANDS = "Only hands move in this shot; the frame stays on the hands and what they hold from the first frame to the last."
ONE_TANG = "the young woman with the two high round buns appears only once"
BACK2 = (f"Only these 2 people are in the frame, the young woman with the buns seen only from behind and Xu Yan facing us beyond her; "
         f"{ONE_TANG}; no second copy of anyone appears.")
L = "/home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
# review 必改 3: the sleeves' cloth, no face (refs-live/README.md, last paragraph)
LAI_CLOTH = "The two thin hands come out of grey-brown hemp cuffs of the cloth shown in <Picture 1>; "
QIAN_CLOTH = ("the two plump hands with three gold rings come out of the dark gold silk sleeves with roundel patterns shown in "
              "<Picture 2>; the arms leave the frame at the bottom edge; ")
# review 必改 4 (e918 fix2 s37): s23's identity clause becomes a costume sentence, no name, no picture of him
QIAN_ID_S23 = (QIAN_ID13.replace("<Picture 2>, <Picture 3> and <Picture 4>", "<Picture 1>, <Picture 2> and <Picture 3>")
               + "the location")
S23_MAN = ("The one man in this shot is a short, portly man in a dark gold silk round-collared robe with roundel patterns, a white "
           "inner collar, long wide sleeves bunched at his elbows, and a " + CAP + "; the location")
S23_ACTING = ("Natural, realistic human motion of a real actor: the weight of his heavy body sinks with each breath, and the gold "
              "silk folds over his back and shoulders.")
QIAN_PICS = ["qianyuanwai-portrait-l1.png", "qianyuanwai-angle-a-l1.png", "qianyuanwai-angle-b-l1.png"]


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


shots = {f"s{n:02d}": {} for n in range(1, 42)}

# Tang Xiaotang's five on-screen lines (bible rule 3): from behind her; the 'only' sentence says so and that she appears once.
shots["s18"] = tang_back(ONLY_SHE, f"She is the only person in the frame, seen only from behind the whole shot; {ONE_TANG}; no second "
                                   f"copy of anyone appears.", True)
# review 必改 17: no yamen hands in s28, the box already in her hands
shots["s28"] = tang_back(ONLY_SHE, f"She is the only person in the frame, seen only from behind the whole shot; {ONE_TANG}; no second "
                                   f"copy of anyone appears.", True)
for sid in ["s36", "s39", "s41"]:
    shots[sid] = tang_back(ONLY_2, BACK2)                 # Xu Yan facing us beyond her
# Her silent face (s06, s07, s20, s38): e907's neutral face sentences.
for sid in ["s06", "s07", "s20", "s38"]:
    shots[sid] = {"replace": [list(NEUTRAL[0]), list(NEUTRAL[1])]}

# The hand inserts: only the cloth of the owners' sleeves (review 必改 3, 建議 for s11), no face, no name; no set picture.
shots["s11"] = {"drop_set": True,
                "replace": [[LAI_ID, LAI_CLOTH],
                            [ONLY_HE, "Only the two thin hands and the two slim hands in dark brown sleeves holding their wrists are "
                                      "in the frame; no second copy of anyone appears."],
                            [FACES + " ", ""], [ACTING, HANDS]],
                "swap_pictures": {"laisan-portrait-l1.png": "laisan-sleeve-l1.png"}}
shots["s13"] = {"drop_set": True, "drop_pictures": ["qianyuanwai-angle-a-l1.png", "qianyuanwai-angle-b-l1.png"],
                "replace": [[LAI_ID, LAI_CLOTH], [QIAN_ID13, QIAN_CLOTH],
                            [ONLY_2, "Only the four hands and their sleeves are in the frame; no second copy of anyone appears."],
                            [FACES + " ", ""], [ACTING, HANDS]],
                "swap_pictures": {"laisan-portrait-l1.png": "laisan-sleeve-l1.png",
                                  "qianyuanwai-portrait-l1.png": "qianyuanwai-sleeve-l1.png"}}
# s23 (review 必改 4): no picture of him, no name; from above-front, the cap brim covering the face.
shots["s23"] = {"drop_pictures": list(QIAN_PICS),
                "replace": [[QIAN_ID_S23, S23_MAN], [FACES + " ", ""], [ACTING, S23_ACTING]]}

# The unnamed backs, heads and hands the compositions describe.
add("s01", "replace", [S01_ONLY, ONLY_2])
add("s02", "replace", [ONLY_HE, besides("him", "the back of the young man's head and his shoulder in the foreground")])
add("s08", "replace", [ONLY_SHE, besides("her", "the backs of the two townsmen's heads and shoulders at the bottom edge")])
add("s04", "replace", [ONLY_2, "Only these 2 people and the one portly man kneeling with his back to us at the right edge are in "
                               "the frame, his face out of the frame; no second copy of anyone appears."])
add("s12", "replace", [ONLY_HE, besides("him", "the two hands in black sleeves gripping his forearms at the edges")])
add("s14", "replace", [ONLY_HE, besides("him", "the one orange-red hand in the soft right foreground")])
add("s26", "replace", [ONLY_HE, besides("him", "the two hands in black sleeves gripping his upper arms at the edges")])
add("s27", "replace", [ONLY_HE, besides("him", "the one small hand in a pink sleeve at the right edge")])
add("s32", "replace", [ONLY_HE, besides("him", "the back of the young woman's head and her shoulder in the foreground")])

# Qian Yuanwai's costume sentence: the portrait's cap and collar; rings only where his hands are seen (s12, s23).
for sid in ["s01", "s02", "s09"]:
    add(sid, "replace", list(QIAN_HIDDEN))
for sid in ["s15", "s17", "s19"]:
    add(sid, "replace", list(QIAN_BEHIND))
add("s26", "replace", list(QIAN_OUT))
add("s12", "replace", list(QIAN_RINGS))

# Lines not said into a face on screen: the speaking gaze names the listener off screen or the thing looked at.
for sid, g in [
    ("s03", "his face three-quarter to screen right toward Qian Yuanwai off screen right, his eyes on him"),
    ("s05", "his face three-quarter to screen left, his eyes on the two men on the floor below him, moving from screen left to screen right"),
    ("s06", "his face tipped up toward the high dais, then turning three-quarter to screen right toward Qian Yuanwai off screen right, his eyes on him"),
    ("s09", "his face three-quarter to screen left toward Xu Yan off screen left, his eyes on him"),
    ("s10", "his face three-quarter to screen right toward Lai San kneeling beside him, his eyes on him"),
    ("s12", "his face three-quarter to screen left, his eyes on the hands that grip his arms, darting between them"),
    ("s14", "his face three-quarter to screen right, his eyes on Lai San off screen left and then on the hand in the right foreground"),
    ("s15", "his face three-quarter to screen left toward Xu Yan off screen left, his eyes on him"),
    ("s16", "his face lowered toward the bundle, his eyes on it, then lifting toward screen right"),
    ("s17", "his face three-quarter to screen left toward Xu Yan off screen left, his eyes on him"),
    ("s20", "his face tipped up toward the high dais above the top of the frame, his eyes on it"),
    ("s21", "his face tipped up toward the high dais above the top of the frame, his eyes on it"),
    ("s22", "his face turning from screen left to three-quarter to screen right toward Qian Yuanwai off screen right below him, his eyes on him"),
    ("s24", "his face three-quarter to screen right toward Qian Yuanwai off screen right below him, his eyes on him"),
    ("s26", "his head turned back over his left shoulder toward Xu Yan off screen right, his face three-quarter toward us, his eyes on him"),
    ("s30", "his face three-quarter to screen right toward Qin Shuang off screen right, his eyes on her"),
    ("s34", "his face three-quarter to screen left, his eyes on a point in the air in front of him"),
    ("s40", "his face tipped up toward the moon beyond the upper right of the frame, his eyes on it"),
]:
    add(sid, "replace", [SPEAK_GAZE_HE, g])
add("s04", "replace", [SPEAK_GAZE, "her face tipped up toward the high dais above the top of the frame, her eyes on it"])
add("s31", "replace", [SPEAK_GAZE, "her face three-quarter to screen right toward Xu Yan off screen right, her eyes on him"])
add("s37", "replace", [SPEAK_GAZE, "her head turned back over her left shoulder toward screen right, toward the others coming down "
                                   "the steps behind her off screen right, her eyes on them"])

# The crowded shots: the profile pictures go (e914-e918).
drop("s01", "xuyan-angle-b-l1.png", "qianyuanwai-angle-b-l1.png")
drop("s06", "xuyan-angle-b-l1.png", "tangxiaotang-angle-b-l1.png")
drop("s07", "tangxiaotang-angle-b-l1.png")
drop("s10", "xuyan-angle-b-l1.png")
drop("s20", "xuyan-angle-b-l1.png", "tangxiaotang-angle-b-l1.png")
drop("s29", "xuyan-angle-b-l1.png")
drop("s38", "xuyan-angle-b-l1.png", "tangxiaotang-angle-b-l1.png")
# review 必改 13: Qian Yuanwai's angle-b (a hanging knot behind a two-layer cap) is sent nowhere.
for sid in ["s02", "s12", "s26"]:
    drop(sid, "qianyuanwai-angle-b-l1.png")

# retake.py cannot swap a picture; prep919.sh applies "swap_pictures" to colab-jobs.json after retake.py (absolute paths; the
# prompt text is unchanged). gen-dh gives the yamen gate set-xianya-l1 for "county yamen" and set-wuding-l1 for the roof.
for sid in ["s01", "s02", "s03"]:
    shots[sid]["swap_pictures"] = {"set-xianya-l1.png": "set-xianya-ceting-l1.png"}
for sid in ["s04", "s06", "s07", "s08", "s09", "s10", "s12", "s14", "s15", "s16", "s17", "s18", "s19", "s20", "s21", "s23",
            "s25", "s26", "s27"]:
    shots[sid]["swap_pictures"] = {"set-xianya-l1.png": "set-xianya-gongtang-floor-l1.png"}
for sid in ["s05", "s22", "s24"]:
    shots[sid]["swap_pictures"] = {"set-xianya-l1.png": "set-xianya-gongtang-dais-l1.png"}
# review 必改 13: the close-ups that gen-dh gives angle-a + angle-b send the portrait + angle-a instead (in this order: the first
# swap frees the angle-a name for the second).
for sid in ["s09", "s15", "s17", "s19"]:
    shots[sid]["swap_pictures"] = {"qianyuanwai-angle-a-l1.png": "qianyuanwai-portrait-l1.png",
                                   "qianyuanwai-angle-b-l1.png": "angles/qianyuanwai-angle-a-l1.png",
                                   **shots[sid]["swap_pictures"]}
# Two new free crops (refs-live/README.md), as their review l2s: the gate without the empty red rack and with the red
# glyph block painted out (必改 14); the roof without the loaded persimmon tree, the full moon and the eave tiles (必改 15), sent
# only to the wide s38; s39-s41 send no roof picture.
for n in range(28, 38):
    shots[f"s{n}"]["swap_pictures"] = {"set-xianya-l1.png": "set-xianya-steps-l2.png"}
shots["s38"]["swap_pictures"] = {"set-wuding-l1.png": "set-wuding-eave-l2.png"}
for sid in ["s39", "s40", "s41"]:
    shots[sid]["drop_set"] = True
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e919 live d1 (e918-live/spec.json's way after its review and fixes, written by mkspec.py). Tang Xiaotang never shows "
              "her mouth: s18 (alone, the page held up toward the dais), s28 (alone, the box of silver), s36, s39, s41 (Xu Yan "
              "facing us beyond her) are from behind her (nospeak, recordings laid in): her three face pictures and her identity "
              "sentence go, and the 'only' sentence says she is seen from behind and appears once; s19 is Qian Yuanwai's face with "
              "her line off screen; s27 her hand only. s06, s07, s20, s38 are her silent face: e907's neutral face sentences. Hand "
              "inserts s11 (Lai San) and s13 (Lai San and Qian Yuanwai) send only the sleeve crops (no face, no name) and no set picture. Qian "
              "Yuanwai's sentence takes the portrait's tall round smooth cap and round collar (e918 fix1); the gold rings only where "
              "his hands are seen (s12; s23 is an unnamed costume sentence with no picture of him); his angle-b is sent nowhere "
              "(s09, s15, s17, s19: portrait + angle-a); s04 has his unnamed back, s37 is Qin Shuang alone (review 必改). Sets by swap_pictures (prep919.sh, absolute paths): set-xianya-ceting-l1 (s01-s03), "
              "set-xianya-gongtang-floor-l1 (the floor), set-xianya-gongtang-dais-l1 (Magistrate Hu s05, s22, s24), and two new "
              "crops: set-xianya-steps-l2 (s28-s37) and set-wuding-eave-l2 (s38; s39-s41 no set picture). The speaking gaze names the listener off "
              "screen or the thing looked at. Crowded shots drop the profile pictures. No off-screen sentence is in these prompts "
              "(r2.py OFFSCREEN_SPEECH = False). Seeds 9191101/9191102."),
    "seeds": [9191101, 9191102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
