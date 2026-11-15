"""Writes spec.json next to this file: e914 live d1 (e913-live/spec.json's way). Run: python3 -I mkspec.py"""
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
                  "flowing sleeves, a small gold abacus hanging at her waist, her resting face composed and unsmiling"]]
ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."
ONLY_2 = "Only these 2 people are in the frame; no second copy of anyone appears."
ONLY_3 = "Only these 3 people are in the frame; no second copy of anyone appears."
SPEAK_GAZE = "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"
SPEAK_GAZE_HE = "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person"


def besides(pr, what):
    return (f"Besides {pr}, only {what} in the foreground the composition describes is in the frame, belonging to someone whose face "
            f"is out of the frame; no second copy of anyone appears.")


shots = {f"s{n:02d}": {} for n in range(1, 43)}
# Tang Xiaotang's lines from behind her with Xu Yan in front of her (s16 is an insert of her hand).
for sid in ["s20", "s24", "s40", "s42"]:  # s42: a two-shot like s40 (review.md 必改 11)
    shots[sid] = {"replace": [[TANG_ID, ""], [ONLY_2, "Only these 2 people are in the frame, the young woman seen only from behind; "
                                                       "no second copy of anyone appears."]],
                  "drop_pictures": TANG_PICS}
shots["s26"] = {"replace": [[TANG_ID, ""], [ONLY_SHE, "She is the only person in the frame, seen only from behind the whole shot; "
                                                       "no second copy of anyone appears."]],
                "drop_pictures": TANG_PICS}
# Her silent face: e907's neutral face sentences (s15, s18); s22 is her one allowed smile, so only the face half.
for sid in ["s15", "s18"]:
    shots[sid] = {"replace": NEUTRAL}
shots["s22"] = {"replace": [FACE]}
# The knife shots from behind Xu Yan (unnamed, no pictures; bible rule 5).
for sid in ["s01", "s05"]:
    shots[sid] = {"replace": [[ONLY_SHE, besides("her", "the young man seen from behind with the lantern")]]}
# The reverse over Qin Shuang's shoulder (unnamed, no pictures).
shots["s06"] = {"replace": [[ONLY_HE, besides("him", "the back of the young woman's head and her shoulder")]]}
# s07: she says it with her eyes on the ground, not on him (e913 s01's fix for the speaking sentence's gaze).
shots["s07"] = {"replace": [[SPEAK_GAZE, "her face in three-quarter profile, her eyes lowered to the ground, not on him"]]}
# s42 (review.md 必改 11): only his portrait and one angle (the profile adds weight to the face of the closing shot only).
shots["s42"]["drop_pictures"] = TANG_PICS + ["xuyan-angle-b-l1.png"]
# s30 (review.md 必改 5): he says it over his shoulder walking away, his eyes ahead, not turned to the young man.
shots["s30"] = {"replace": [[SPEAK_GAZE_HE, "his face in three-quarter profile toward the open side, eyes ahead"]]}
# s39 (review.md 建議): three people, the one in the foreground unnamed from behind (the builder's generic sentence let an
# extra person in at e913 s35).
shots["s39"] = {"replace": [["Besides them, only the other people the composition names are in the frame; no second copy of anyone appears.",
                             besides("them", "the back of the young woman's head and her shoulder")]]}
# s12, s14 (review.md 建議): A-ling's profile picture lost her hairpin (refs-live README); she is three-quarter in both.
for sid in ["s12", "s14"]:
    shots[sid] = {"drop_pictures": ["aling-angle-b-l1.png"]}

spec = {
    "_note": ("e914 live d1 (e913-live/spec.json's way, written by mkspec.py). s20, s24, s26 and s40 are Tang Xiaotang's lines shot "
              "from behind her (nospeak, recordings laid in): her three face pictures and her identity sentence go; s16 is an insert of "
              "her hand on the wooden abacus with no picture of her; s42 is a two-shot like s40 (review.md 必改 11). s15 and s18 are "
              "her silent face shots: e907's neutral face sentences; s22 (her one allowed smile, bowed over the abacus) only the face "
              "half. s01, s05 and s06: ref2manifest's 'only person' sentence is rewritten to admit the unnamed back the composition "
              "describes (s01, s05: Xu Yan from behind with no picture, bible rule 5 for the knife shots; s06: Qin Shuang's back). "
              "s07: her eyes on the ground, not on him; s30: his eyes ahead as he walks off (必改 5); s39: the generic 'other people' "
              "sentence replaced by the unnamed back (建議); s12, s14: A-ling's profile picture dropped (建議). No off-screen sentence is in these prompts (r2.py OFFSCREEN_SPEECH = False). "
              "Seeds 9141101/9141102."),
    "seeds": [9141101, 9141102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
