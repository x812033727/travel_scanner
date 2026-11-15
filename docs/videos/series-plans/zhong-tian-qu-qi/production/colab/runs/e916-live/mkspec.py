"""Writes spec.json next to this file: e916 live d1 (e915-live/spec.json's way, with the e913-e915 picking lessons).
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
LAI_ID = ("Lai San shown in <Picture 1> keeps exactly the same face, hair and costume as the pictures: East Asian young man of "
          "twenty-eight, small and thin, pointed chin, shifty eyes, a slight limp, an ancient Chinese Song-dynasty peasant's grey-brown "
          "hemp cross-collared short jacket and an old cloth head wrap; ")
XU_ID = ("Xu Yan shown in <Picture 1>, <Picture 2> and <Picture 3> (the same man from several angles) keeps exactly the same face, "
         "hair and costume as the pictures: East Asian young man of twenty-five, clean-cut handsome with thick brows, double-lidded "
         "bright eyes, straight nose and a firm mouth, tall and lean with broad shoulders, black hair gathered up into a topknot on the "
         "crown and tied with a cloth band, a few strands falling over his forehead, a faded blue-grey cotton scholar's robe patched at "
         "one elbow, cloth shoes; ")
FACE = ["dazzling glamorous beauty: big round sparkling eyes with long lashes, glossy peach-pink lips, rosy cheeks,",
        "a delicate beauty: big round clear eyes with long lashes, soft peach-pink lips, light rosy cheeks,"]
NEUTRAL = [FACE, ["flowing sleeves, a small gold abacus hanging at her waist",
                  "flowing sleeves, a small gold abacus hanging at her waist, her resting face composed, her lips closed"]]
ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."
ONLY_2 = "Only these 2 people are in the frame; no second copy of anyone appears."
ONLY_3 = "Only these 3 people are in the frame; no second copy of anyone appears."
BESIDES_HER = "Besides her, only the other people the composition names are in the frame; no second copy of anyone appears."
SPEAK_GAZE = "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"
SPEAK_GAZE_HE = "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person"
FACES = ("Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the face, hair "
         "and costume only, never the mood.")
ACTING = ("Natural, realistic human motion and acting of real actors: each person keeps the identity, hair and costume of their "
          "reference pictures, while every visible face acts the emotion written above and changes with it; the pictures are "
          "neutral studio portraits, never copy their blank expression.")
HANDS = "Only hands move in this shot; the frame stays on the hands and what they hold from the first frame to the last."
SHOES = "Every person in the frame wears dark cloth shoes on both feet."
BOOTS = "Qin Shuang wears her black leather boots and everyone else wears dark cloth shoes, on both feet."
ONE_TANG = "the young woman with the two buns and pink ribbons appears only once"


def besides(pr, what):
    return (f"Besides {pr}, only {what} in the foreground the composition describes is in the frame, belonging to someone whose face "
            f"is out of the frame; no second copy of anyone appears.")


def tang_back(only_old, only_new, alone=False):
    # alone: she is the only named person, so her identity sentence opened the anchor and the set clause after it must
    # start the sentence instead
    first = [TANG_ID + "the location", "The location"] if alone else [TANG_ID, ""]
    return {"replace": [first, [only_old, only_new]], "drop_pictures": list(TANG_PICS)}


def lai_back(only_old, only_new, alone=False):
    first = [LAI_ID + "the location", "The location"] if alone else [LAI_ID, ""]
    return {"replace": [first, [only_old, only_new]], "drop_pictures": ["laisan-portrait-l1.png"]}


shots = {f"s{n:02d}": {} for n in range(1, 43)}

# Tang Xiaotang's fourteen lines (bible rule 3): from behind her, the 'only' sentence saying so and that she appears once
# (e915 s26/s41: a second Tang beside her back), or an insert of her hand(s). She is always the first named person here.
BACK2 = f"Only these 2 people are in the frame, the young woman seen only from behind; {ONE_TANG}; no second copy of anyone appears."
BACK3 = f"Only these 3 people are in the frame, the young woman seen only from behind; {ONE_TANG}; no second copy of anyone appears."
ALONE = f"She is the only person in the frame, seen only from behind the whole shot; {ONE_TANG}; no second copy of anyone appears."
CROWD = (f"Besides her, seen only from behind, only the other people the composition names are in the frame; {ONE_TANG}; no second "
         "copy of anyone appears.")
for sid in ["s06", "s24", "s26"]:
    shots[sid] = tang_back(ONLY_2, BACK2)
for sid in ["s16", "s42"]:
    shots[sid] = tang_back(ONLY_3, BACK3)
for sid in ["s03", "s20"]:
    shots[sid] = tang_back(ONLY_SHE, ALONE, True)
for sid in ["s29", "s32", "s33", "s37"]:  # the scholars (and the far carriage) beyond her
    shots[sid] = tang_back(BESIDES_HER, CROWD, True)
# review.md 必改 5 (the e915 s08 lesson: an insert that sends the set picture opens on the empty set and cuts inside the clip):
# the four hand inserts send no set picture; one picture of the hands' owner stays, named only as the owner.
def owner_insert(id_sentence, who, keep_drop, only_new):
    return {"drop_set": True, "drop_pictures": keep_drop,
            "replace": [[id_sentence, who], [ONLY_HE if "Xu Yan" in who else ONLY_SHE, only_new],
                        [FACES + " ", ""], [ACTING, HANDS]]}


TANG_ANGLES = ["tangxiaotang-angle-a-l1.png", "tangxiaotang-angle-b-l1.png"]
XU_DROP = ["xuyan-portrait-l1.png", "xuyan-angle-b-l1.png"]
shots["s27"] = owner_insert(TANG_ID, "The hand and sleeve belong to Tang Xiaotang shown in <Picture 1>, whose face stays out of the frame; ",
                            TANG_ANGLES, "Only her one hand in a peach-pink silk sleeve is in the frame; no second copy of anyone appears.")
shots["s38"] = owner_insert(TANG_ID, "The hands, sleeves and sash belong to Tang Xiaotang shown in <Picture 1>, whose face stays out of "
                                     "the frame; the frame shows only her waist, her hands and the table edge; ",
                            TANG_ANGLES, "Only her two hands in peach-pink silk sleeves are in the frame; no second copy of anyone appears.")
shots["s12"] = owner_insert(XU_ID, "The hands and sleeves belong to Xu Yan shown in <Picture 2>, whose face stays out of the frame; ",
                            XU_DROP, "Only his two hands and forearms are in the frame; no second copy of anyone appears.")
# Her silent face (s01, s07, s11, s18, s34, s39): e907's neutral face sentences.
for sid in ["s01", "s07", "s11", "s18", "s34", "s39"]:
    shots[sid] = {"replace": [list(NEUTRAL[0]), list(NEUTRAL[1])]}

# Lai San gives no face this episode: his two lines from behind him (picture and identity sentence dropped).
shots["s02"] = lai_back(ONLY_2, "Only these 2 people are in the frame, the thin young man seen only from behind; no second copy of anyone appears.")
shots["s08"] = lai_back(ONLY_HE, "He is the only person near the camera, seen only from behind the whole shot; besides him only the two small "
                                 "far figures the composition describes are in the frame; no second copy of anyone appears.", True)

# Unnamed backs, shoulders and hands in the foreground (no pictures sent).
LAI_FG = "the back of the thin young man's head and his shoulders"
shots["s01"]["replace"].append([ONLY_2, "Besides these 2 people, only the back of the thin young man's head and his shoulders in the "
                                        "foreground the composition describes is in the frame, his face out of the frame; no second copy "
                                        "of anyone appears."])
shots["s07"]["replace"].append([ONLY_2, "Besides these 2 people, only the back of the thin young man in the right foreground and one hand "
                                        "in a grey sleeve on the log, which the composition describes, are in the frame, their faces out "
                                        "of the frame; no second copy of anyone appears."])
shots["s05"] = {"replace": [[ONLY_HE, besides("him", "the back of the young woman's head and her shoulders") .replace(
    "no second copy", f"{ONE_TANG}; no second copy")]]}
shots["s10"] = {"replace": [[ONLY_HE, besides("him", "the back of the old man's head and his shoulder")]]}
shots["s14"] = {"replace": [[ONLY_HE, besides("him", "the back of the young woman's head and her shoulder")]]}
shots["s21"] = {"replace": [[ONLY_SHE, besides("her", "the back of the young woman with the pink ribbons and her shoulders").replace(
    "no second copy", f"{ONE_TANG}; no second copy")]]}
# s25 is a clean close-up of Xu Yan now (review 建議): no foreground back to admit.
shots["s28"] = {"replace": [[ONLY_HE, besides("him", "the one slender hand in a peach-pink sleeve at the left edge")]]}
shots["s36"] = {"replace": [[ONLY_HE, besides("him", "the peach-pink shoulder and one pink ribbon of the young woman at the right edge")]]}

# Lines not said into a face.
shots["s09"] = {"replace": [[SPEAK_GAZE_HE, "his face lowered to the bamboo mat in his hands, his eyes on the mat"]]}
shots["s19"] = {"replace": [[SPEAK_GAZE, "her face in three-quarter profile toward the water ahead, her eyes on the rock and the white water"]]}
shots["s40"] = {"replace": [[SPEAK_GAZE, "her face in three-quarter profile up the river, her eyes on the smoke over the village"]]}
# s35: inside the carriage; the academy picture is not sent (Sun Zhanggui's portrait stays), and he speaks to the driver off screen.
shots["s35"] = {"drop_set": True, "replace": [[SPEAK_GAZE_HE, "his face turned toward the front of the carriage on screen left, his eyes sliding back to the street through the gap"]]}
# review.md 建議 (s36): he speaks to her on his right while his eyes stay on the carriage at the left.
shots["s36"]["replace"].append([SPEAK_GAZE_HE, "his head turned toward her on his right only a little, speaking low out of the side of his mouth, his eyes staying on the carriage down the street at the left"])
# review.md 必改 16 (s40): a medium shot on the raft against the sky; the landing picture is not sent (Qin Shuang's portrait stays).
shots["s40"]["drop_set"] = True
# review.md 必改 16 (s39): the raft going upstream has its bow on screen right, so it gets the mirrored raft picture. retake.py
# cannot swap a picture; prep916.sh applies "swap_pictures" to colab-jobs.json after retake.py (the prompt text is the same).
shots["s39"]["swap_pictures"] = {"set-zhufa-ye-l2.png": "set-zhufa-ye-l2-flip.png"}

# s31: the brush insert. The academy picture is not sent (e915 s08: an insert opened on the set picture and cut inside the clip);
# Xu Yan's side picture xuyan-angle-a-l1 stays as the only picture, named only as the owner of the hand and sleeve.
shots["s31"] = {"drop_set": True, "drop_pictures": ["xuyan-portrait-l1.png", "xuyan-angle-b-l1.png"],
                "replace": [[XU_ID, "The hand and sleeve belong to Xu Yan shown in <Picture 2>, whose face stays out of the frame; "],
                            [ONLY_HE, "Only his right hand and sleeve are in the frame; no second copy of anyone appears."],
                            [FACES + " ", ""], [ACTING, HANDS]]}

# ref2manifest's shoe sentence against Qin Shuang's leather boots (e915 review 必改 7).
for sid in ["s13", "s34", "s39"]:
    shots[sid].setdefault("replace", []).append([SHOES, BOOTS])

# The crowded shots (seven or eight pictures): Xu Yan's profile picture goes (e014/e015), and where Tang Xiaotang is small and
# three-quarter (s18, s34, s39) her profile too.
shots["s01"]["drop_pictures"] = ["xuyan-angle-b-l1.png"]
shots["s07"]["drop_pictures"] = ["xuyan-angle-b-l1.png"]
for sid in ["s18", "s34", "s39"]:
    shots[sid]["drop_pictures"] = ["xuyan-angle-b-l1.png", "tangxiaotang-angle-b-l1.png"]

spec = {
    "_note": ("e916 live d1 (e915-live/spec.json's way, written by mkspec.py). Tang Xiaotang's fourteen lines never show her mouth: "
              "s03, s06, s16, s20, s24, s26, s29, s32, s33, s37, s42 from behind her and s27, s38 inserts of her hands (nospeak, "
              "recordings laid in): her three face pictures and her identity sentence go, and the 'only' sentence says she is seen "
              "from behind and appears only once (e915 s26/s41). s01, s07, s11, s18, s34, s39 are her silent face shots: e907's "
              "neutral face sentences. Lai San gives no face: s02, s08 drop his picture and identity sentence; s01, s07 admit his "
              "unnamed back. s05, s10, s14, s21, s28, s36: the 'only person' sentence admits the unnamed back, shoulder or hand. "
              "s09 (Carpenter Shi, eyes on the mat), s19, s40 (Qin Shuang, eyes ahead), s35 (Sun Zhanggui to the driver), s36 (to her, eyes "
              "on the carriage): the speaking gaze is not a listener. After review.md: the hand inserts send no set picture, only "
              "the owner of the hands (s12, s31 xuyan-angle-a-l1; s27, s38 tangxiaotang-portrait-l1) and lose the face sentences; "
              "s35 and s40 send no set picture; s39 sends the mirrored raft picture (swap_pictures, applied by prep916.sh); s25 is a "
              "clean close-up. s13, s34, s39: the shoe sentence keeps Qin "
              "Shuang's boots. s01, s07 (seven pictures) drop Xu Yan's profile; s18, s34, s39 (eight) drop his and Tang Xiaotang's "
              "profiles. No off-screen sentence is in these prompts (r2.py OFFSCREEN_SPEECH = False). Seeds 9161101/9161102."),
    "seeds": [9161101, 9161102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
