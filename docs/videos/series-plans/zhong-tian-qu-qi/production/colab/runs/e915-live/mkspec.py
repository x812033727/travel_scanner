"""Writes spec.json next to this file: e915 live d1 (e914-live/spec.json's way). Run: python3 -I mkspec.py"""
import json
from pathlib import Path

TANG_ID = ("Tang Xiaotang shown in <Picture 1>, <Picture 2> and <Picture 3> (the same woman from several angles) keeps exactly the same "
           "face, hair and costume as the pictures: East Asian young woman of eighteen, dazzling glamorous beauty: big round sparkling eyes "
           "with long lashes, glossy peach-pink lips, rosy cheeks, luminous fair skin, petite curvy figure, hair in two looped buns tied "
           "with pink silk ribbons and pearl pins, a peach-pink silk brocade ruqun: a light cross-collared short jacket wrapped shut across "
           "the chest in a low closed V, its hem at the waist covering the top of a pleated skirt tied at the waist with a ribbon bow and a "
           "small gold ornament, thick opaque silk and flowing sleeves, a small gold abacus hanging at her waist; ")
TANG_PICS = ["tangxiaotang-portrait-l1.png", "tangxiaotang-angle-a-l1.png", "tangxiaotang-angle-b-l1.png"]
FACE = ["dazzling glamorous beauty: big round sparkling eyes with long lashes, glossy peach-pink lips, rosy cheeks,",
        "a delicate beauty: big round clear eyes with long lashes, soft peach-pink lips, light rosy cheeks,"]
NEUTRAL = [FACE, ["flowing sleeves, a small gold abacus hanging at her waist",
                  "flowing sleeves, a small gold abacus hanging at her waist, her resting face composed, her lips closed"]]
ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."
ONLY_2 = "Only these 2 people are in the frame; no second copy of anyone appears."
BESIDES_HER = "Besides her, only the other people the composition names are in the frame; no second copy of anyone appears."
SPEAK_GAZE = "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"
SPEAK_GAZE_HE = "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person"


def besides(pr, what):
    return (f"Besides {pr}, only {what} in the foreground the composition describes is in the frame, belonging to someone whose face "
            f"is out of the frame; no second copy of anyone appears.")


def tang_back(only_old, only_new, alone=False):
    # alone: she is the only named person, so her identity sentence opened the anchor and the set clause after it must
    # start the sentence instead
    first = [TANG_ID + "the location", "The location"] if alone else [TANG_ID, ""]
    return {"replace": [first, [only_old, only_new]], "drop_pictures": list(TANG_PICS)}


shots = {f"s{n:02d}": {} for n in range(1, 43)}
# Tang Xiaotang's eight lines (bible rule 3): from behind her with the person she speaks to in front of her ...
BACK2 = "Only these 2 people are in the frame, the young woman seen only from behind; no second copy of anyone appears."
for sid in ["s01", "s37", "s41"]:
    shots[sid] = tang_back(ONLY_2, BACK2)
shots["s07"] = tang_back(ONLY_SHE, "She is the only person in the frame, seen only from behind the whole shot; no second copy of anyone appears.", True)
for sid in ["s20", "s26"]:  # among the villagers on the ridge (the builder's crowd sentence)
    shots[sid] = tang_back(BESIDES_HER, "Besides her, seen only from behind, only the other people the composition names are in the "
                                        "frame; no second copy of anyone appears.", True)
# ... or an insert of her hand (s02 with Xu Yan's hands, s05 alone). She is in chars only so her recording is not marked 畫外.
shots["s02"] = tang_back(ONLY_SHE, "Only hands are in the frame: the young man's two hands and her one hand in a peach-pink silk "
                                   "sleeve; no second copy of anyone appears.", True)
shots["s05"] = tang_back(ONLY_SHE, "Only her one hand in a peach-pink silk sleeve is in the frame; no second copy of anyone appears.", True)
# Her silent face (s36, s42): e907's neutral face sentences.
for sid in ["s36", "s42"]:
    shots[sid] = {"replace": NEUTRAL}
# Unnamed backs in the foreground (no pictures sent): her back (s06), Erniu's shoulder (s24), Lai San's back (s39).
shots["s06"] = {"replace": [[ONLY_HE, besides("him", "the back of the young woman's head and her shoulders")]]}
shots["s24"] = {"replace": [[ONLY_SHE, besides("her", "the broad shoulder of the young man at the right edge")]]}
shots["s39"] = {"replace": [[ONLY_HE, besides("him", "the back of the thin young man's head and his shoulder")]]}
# Lines not said into a face: Elder Han to the fields (s15) and to the sky (s29); Qin Shuang to the plank (s32), turned away (s34).
shots["s15"] = {"replace": [[SPEAK_GAZE_HE, "his face in three-quarter profile toward the fields off screen left, his eyes on the fields"]]}
shots["s29"] = {"replace": [[SPEAK_GAZE_HE, "his face in three-quarter profile, his eyes lifted to the sky"]]}
shots["s32"] = {"replace": [[SPEAK_GAZE, "her face in three-quarter profile, her eyes lowered to the blank plank"]]}
# s33, s34: close shots against bamboo; the grove picture (with its fire and the board on the ground) is not sent (the e913 yard
# lesson). s34 also speaks turned away.
shots["s33"] = {"drop_set": True}
shots["s34"] = {"drop_set": True, "replace": [[SPEAK_GAZE, "her face turned away toward the dark bamboo, her eyes on the bamboo"]]}

# The crowded shots (seven or eight pictures): Xu Yan's profile picture goes (e014 s42 after its review: the profile adds weight
# to one face only), and in s36 and s42 Tang Xiaotang's profile too (she is three-quarter in both): six pictures each.
for sid in ["s09", "s18"]:
    shots[sid]["drop_pictures"] = ["xuyan-angle-b-l1.png"]
for sid in ["s36", "s42"]:
    shots[sid]["drop_pictures"] = ["xuyan-angle-b-l1.png", "tangxiaotang-angle-b-l1.png"]

# review.md (2026-11-15) after the independent review:
FACES = "Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the face, hair and costume only, never the mood."
ACTING = ("Natural, realistic human motion and acting of real actors: each person keeps the identity, hair and costume of their "
          "reference pictures, while every visible face acts the emotion written above and changes with it; the pictures are "
          "neutral studio portraits, never copy their blank expression.")
HANDS = "Only hands move in this shot; the frame stays on the paper and the hands from the first frame to the last."
# 建議 (s02, s05, s08): the inserts of hands drop the two face sentences, which send the model looking for a face.
for sid in ["s02", "s05"]:
    shots[sid]["replace"] += [[FACES + " ", ""], [ACTING, HANDS]]
shots["s08"] = {"replace": [[ACTING, HANDS]]}
# 必改 7 (s09, s25, s31): ref2manifest's shoe sentence against Qin Shuang's leather boots.
SHOES = "Every person in the frame wears dark cloth shoes on both feet."
for sid in ["s09", "s25", "s31"]:
    shots[sid].setdefault("replace", []).append([SHOES, "Qin Shuang wears her black leather boots and everyone else wears dark cloth shoes, on both feet."])
# 必改 11 (s24): the axis is turned; Erniu's shoulder and open hand are at the left edge now.
shots["s24"] = {"replace": [[ONLY_SHE, besides("her", "the broad shoulder and open hand of the young man at the left edge")]]}
# 必改 2: s27, s29, s30 are after the ploughing (furrows, sunset): the unploughed field picture is not sent. s28 keeps it:
# nobody is named in it, so the set is its only picture and Ref2VA needs one (retake.py stops with no picture left); its
# text writes the furrows and the sunset over the picture's flat field and soft late light.
for sid in ["s27", "s29", "s30"]:
    shots[sid]["drop_set"] = True
# 必改 12 (s29): his staff already lies on the earth at the first frame (his cast sentence has it in his hand).
shots["s29"]["replace"] += [["leaning on a polished old bamboo walking staff", "his polished old bamboo walking staff laid on the earth beside him"]]
# 建議 (s40): a low close-up against mist and bridge stone; the bridge picture is not sent.
shots["s40"] = {"drop_set": True}

spec = {
    "_note": ("e915 live d1 (e914-live/spec.json's way, written by mkspec.py). Tang Xiaotang's eight lines never show her mouth: "
              "s01, s07, s20, s26, s37, s41 from behind her and s02, s05 inserts of her hand (nospeak, recordings laid in): her three "
              "face pictures and her identity sentence go, and the 'only' sentence says she is seen from behind (or that only hands "
              "are in the frame). s36 and s42 are her silent face shots: e907's neutral face sentences. s06, s24, s39: the 'only "
              "person' sentence admits the unnamed back or shoulder the composition describes (her back, Erniu's shoulder, Lai San's "
              "back). s15, s29 (Elder Han), s32, s34 (Qin Shuang): the speaking sentence's gaze is the fields, the sky, the plank and "
              "the bamboo, not a listener. s09, s18, s36, s42 (seven or eight pictures): Xu Yan's profile picture is dropped, in s36 and "
              "s42 Tang Xiaotang's too. After review.md: s02, s05, s08 (hands only) lose the face sentences; s09, s25, s31 the shoe "
              "sentence keeps Qin Shuang's boots; s24's foreground hand is at the left edge; s27, s29, s30 and s40 send no set picture (s28 has no other picture); "
              "s29's staff lies on the earth. s33, s34: the grove picture is dropped (close shots against bamboo; r2.py docstring). "
              "No off-screen sentence is in these prompts (r2.py OFFSCREEN_SPEECH = False). Seeds 9151101/9151102."),
    "seeds": [9151101, 9151102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
