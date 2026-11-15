"""Writes spec.json next to this file: e917 live d1 (e916-live/spec.json's way, with the e913-e916 lessons).
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
QIN_ID = ("Qin Shuang shown in <Picture 1> keeps exactly the same face, hair and costume as the pictures: East Asian young woman of "
          "twenty-one, striking fierce heroic beauty: bold straight brows, bright almond eyes with a confident glint and sharp eyeliner, "
          "high nose bridge, full lips, glowing light honey-toned skin, tall athletic figure with a toned silhouette and a strong cinched "
          "waist, sleek high ponytail tied with black cord, a fitted dark brown cotton short jacket crossed at the collar and cinched with "
          "a wide leather belt over fitted black trousers and leather boots; ")
XU_ID = ("Xu Yan shown in <Picture 1>, <Picture 2> and <Picture 3> (the same man from several angles) keeps exactly the same face, "
         "hair and costume as the pictures: East Asian young man of twenty-five, clean-cut handsome with thick brows, double-lidded "
         "bright eyes, straight nose and a firm mouth, tall and lean with broad shoulders, black hair gathered up into a topknot on the "
         "crown and tied with a cloth band, a few strands falling over his forehead, a faded blue-grey cotton scholar's robe patched at "
         "one elbow, cloth shoes; ")
FACE = ["dazzling glamorous beauty: big round sparkling eyes with long lashes, glossy peach-pink lips, rosy cheeks,",
        "a delicate beauty: big round clear eyes with long lashes, soft peach-pink lips, light rosy cheeks,"]
NEUTRAL = [FACE, ["flowing sleeves, a small gold abacus hanging at her waist",
                  "flowing sleeves, a small gold abacus hanging at her waist, her resting face composed, her lips closed"]]
# A-ling's hair comes loose in the fire (script c11-c26): her sentence keeps the face and costume, the hair is let down.
ALING_HAIR = ["long glossy black hair pinned up with a single plain wooden hairpin and a few loose strands framing her face",
              "long glossy black hair, in this shot come loose from its pin and hanging straight down her back and over her right "
              "shoulder"]
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
    return (f"Besides {pr}, only {what} the composition describes is in the frame, belonging to someone whose face is out of "
            f"the frame; no second copy of anyone appears.")


def tang_back(only_old, only_new, alone=False):
    # alone: she is the only named person, so her identity sentence opened the anchor and the set clause after it must
    # start the sentence instead
    first = [TANG_ID + "the location", "The location"] if alone else [TANG_ID, ""]
    return {"replace": [first, [only_old, only_new]], "drop_pictures": list(TANG_PICS)}


def add(sid, key, value):
    shots[sid].setdefault(key, []).append(value) if key == "replace" else shots[sid].__setitem__(key, value)


shots = {f"s{n:02d}": {} for n in range(1, 41)}

# Tang Xiaotang's four lines (bible rule 3): from behind her; the 'only' sentence says so and that she appears once.
ALONE = f"She is the only person in the frame, seen only from behind the whole shot; {ONE_TANG}; no second copy of anyone appears."
CROWD = (f"Besides her, seen only from behind, only the other people the composition names are in the frame; {ONE_TANG}; no second "
         "copy of anyone appears.")
BACK2 = (f"Only these 2 people are in the frame, the young woman with the buns seen only from behind and A-ling a little right of the "
         f"middle; {ONE_TANG}; no second copy of anyone appears.")
shots["s10"] = tang_back(BESIDES_HER, CROWD, True)   # one villager beside her
shots["s31"] = tang_back(BESIDES_HER, CROWD, True)   # the villagers far beyond her
shots["s23"] = tang_back(ONLY_SHE, ALONE, True)
shots["s17"] = tang_back(ONLY_2, BACK2)              # A-ling beyond her
# Her silent face (s01, s18): e907's neutral face sentences.
for sid in ["s01", "s18"]:
    shots[sid] = {"replace": [list(NEUTRAL[0]), list(NEUTRAL[1])]}

# Qin Shuang's s04 line is said from behind her (the e916 Lai San way): her picture and identity sentence go.
shots["s04"] = {"replace": [[QIN_ID, ""], [ONLY_2, "Only these 2 people are in the frame, the young woman with the ponytail seen "
                                                   "only from behind; no second copy of anyone appears."]],
                "drop_pictures": ["qinshuang-portrait-l1.png"]}

# A-ling's loose hair (s11-s14, s17).
ALING_KEEP = ["keeps exactly the same face, hair and costume as the pictures: East Asian young woman of twenty,",
              "keeps exactly the same face and costume as the pictures, her hair let down in this shot: East Asian young woman of twenty,"]
for sid in ["s11", "s12", "s13", "s14", "s17"]:
    add(sid, "replace", list(ALING_KEEP))
    add(sid, "replace", list(ALING_HAIR))

# The shots at the burning hut send no set picture (the yard picture would put the yard behind them): only smoke and a glow.
for sid in ["s11", "s12", "s16"]:
    shots[sid]["drop_set"] = True

# The two hand inserts send no set picture (the e915 s08 lesson); one picture of the hand's owner, named only as the owner.
shots["s20"] = {"drop_set": True,
                "replace": [[QIN_ID, "The hand and sleeve belong to Qin Shuang shown in <Picture 1>, whose face stays out of the frame; "],
                            [ONLY_SHE, "Only her one hand and sleeve are in the frame; no second copy of anyone appears."],
                            [FACES + " ", ""], [ACTING, HANDS]]}
shots["s21"] = {"drop_set": True, "drop_pictures": ["xuyan-portrait-l1.png", "xuyan-angle-b-l1.png"],
                "replace": [[XU_ID, "The hand and sleeve belong to Xu Yan shown in <Picture 2>, whose face stays out of the frame; "],
                            ["Besides him, only the other people the composition names are in the frame; no second copy of anyone appears.",
                             "Only his one hand and sleeve are in the frame; no second copy of anyone appears."],
                            [FACES + " ", ""], [ACTING, HANDS]]}

# Unnamed backs and hands the composition describes.
add("s12", "replace", [ONLY_SHE, besides("her", "the two hands in blue-grey sleeves at the left edge")])
add("s25", "replace", [ONLY_HE, besides("him", "the back of the young man's head and his shoulders in the foreground")])
add("s26", "replace", [ONLY_HE, besides("him", "the one slender hand in a grey-white sleeve at the left edge")])
add("s29", "replace", [ONLY_SHE, besides("her", "the one hand in a blue-grey sleeve at the top right")])
add("s33", "replace", [ONLY_HE, besides("him", "the back of the young woman's head and her shoulder in the foreground")])

# Lines not said into a face.
add("s07", "replace", [SPEAK_GAZE_HE, "his face three-quarter to screen right toward the fire, his eyes on the smoke beyond the wall"])
add("s08", "replace", [SPEAK_GAZE_HE, "his face turned back over his left shoulder toward the village lane outside the gate, his eyes on the lane"])
add("s27", "replace", [SPEAK_GAZE_HE, "his face lowered toward the post hole at his feet, his eyes on the hole"])
add("s28", "replace", [SPEAK_GAZE_HE, "his face three-quarter to screen right toward the rising post, his eyes on it"])
add("s37", "replace", [SPEAK_GAZE_HE, "his face tipped up toward the crossbeams, his eyes on the new frame"])

# ref2manifest's shoe sentence against Qin Shuang's leather boots (e915 review 必改 7).
for sid in ["s01", "s06", "s15"]:
    add(sid, "replace", [SHOES, BOOTS])

# The crowded shots: Xu Yan's profile picture goes (e014-e016), and in s01 (eight pictures) Tang Xiaotang's too.
shots["s01"]["drop_pictures"] = ["xuyan-angle-b-l1.png", "tangxiaotang-angle-b-l1.png"]
for sid in ["s13", "s18"]:
    shots[sid]["drop_pictures"] = ["xuyan-angle-b-l1.png"]

spec = {
    "_note": ("e917 live d1 (e916-live/spec.json's way, written by mkspec.py). Tang Xiaotang's four lines never show her mouth: s10, "
              "s17, s23, s31 from behind her (nospeak, recordings laid in): her three face pictures and her identity sentence go, and "
              "the 'only' sentence says she is seen from behind and appears only once (e915 s26/s41). s01, s18 are her silent face "
              "shots: e907's neutral face sentences. s04: Qin Shuang's line from behind her, her picture and sentence dropped. s11-s14, "
              "s17: A-ling's hair is let down in her sentence (the fire). s11, s12, s16 (at the burning hut) send no set picture. s20, s21: "
              "the hand inserts send no set picture, only the owner of the hand (qinshuang-portrait-l1; xuyan-angle-a-l1) and lose the "
              "face sentences. s12, s25, s26, s29, s33: the 'only person' sentence admits the unnamed hands or back. s07, s08, s27, s28, "
              "s37: the speaking gaze is not a listener. s01, s06, s15: the shoe sentence keeps Qin Shuang's boots. s01 drops Xu Yan's "
              "and Tang Xiaotang's profiles, s13 and s18 Xu Yan's. No off-screen sentence is in these prompts (r2.py OFFSCREEN_SPEECH = "
              "False). Seeds 9171101/9171102."),
    "seeds": [9171101, 9171102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
