"""Writes spec.json next to this file: e913 live d1 (e912-live/spec.json's way). Run: python3 -I mkspec.py"""
import json
from pathlib import Path

TANG_ID = ("Tang Xiaotang shown in <Picture 1>, <Picture 2> and <Picture 3> (the same woman from several angles) keeps exactly the same "
           "face, hair and costume as the pictures: East Asian young woman of eighteen, dazzling glamorous beauty: big round sparkling eyes "
           "with long lashes, glossy peach-pink lips, rosy cheeks, luminous fair skin, petite curvy figure, hair in two looped buns tied "
           "with pink silk ribbons and pearl pins, a peach-pink silk brocade ruqun: a light cross-collared short jacket wrapped shut across "
           "the chest in a low closed V, its hem at the waist covering the top of a pleated skirt tied at the waist with a ribbon bow and a "
           "small gold ornament, thick opaque silk and flowing sleeves, a small gold abacus hanging at her waist; ")
TANG_PICS = ["tangxiaotang-portrait-l1.png", "tangxiaotang-angle-a-l1.png", "tangxiaotang-angle-b-l1.png"]
NEUTRAL = [["dazzling glamorous beauty: big round sparkling eyes with long lashes, glossy peach-pink lips, rosy cheeks,",
            "a delicate beauty: big round clear eyes with long lashes, soft peach-pink lips, light rosy cheeks,"],
           ["flowing sleeves, a small gold abacus hanging at her waist",
            "flowing sleeves, a small gold abacus hanging at her waist, her resting face composed and unsmiling"]]
ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."


def besides(pr, what):
    return (f"Besides {pr}, only {what} in the foreground the composition describes is in the frame, belonging to someone whose face "
            f"is out of the frame; no second copy of anyone appears.")


shots = {f"s{n:02d}": {} for n in range(1, 43)}
for sid in ["s04", "s10", "s12", "s21", "s23"]:  # Tang Xiaotang's lines, from behind her (s07 and s09 are inserts of her hands)
    shots[sid] = {"replace": [[TANG_ID, ""], ["Only these 2 people are in the frame", "Only these 2 people are in the frame, the young woman seen only from behind"]],
                  "drop_pictures": TANG_PICS}
for sid in ["s13", "s25"]:  # her silent face
    shots[sid] = {"replace": NEUTRAL}
shots["s03"] = {"replace": [[ONLY_SHE, besides("her", "the back of the young man's head and his shoulder")]]}
shots["s16"] = {"replace": [[ONLY_HE, besides("him", "the hand holding the wooden plane")]]}
shots["s20"] = {"replace": [[ONLY_HE, besides("him", "the back of the young man's head and his shoulder")]]}
# s32 (review.md 必改 4): both from behind; only she is named, the young man beside her is unnamed with no picture.
shots["s32"] = {"replace": [[TANG_ID, ""],
                            [ONLY_SHE, "Besides her, only the young man seen only from behind walking beside her, whose face is out of the "
                                       "frame, is in the frame; the young woman is seen only from behind; no second copy of anyone appears."]],
                "drop_pictures": TANG_PICS}
# s35 (review.md 必改 3): one man alone in the grove (the original e013 grew a second lantern-carrying figure here).
shots["s35"] = {"replace": [[ONLY_HE, "He is the only person in the frame and the only person in the whole grove; nobody else, no second "
                                      "lantern and no other light anywhere among the bamboo; no second copy of anyone appears."]]}
# s01 (review.md 建議 s01): she speaks over her shoulder with her eyes on the gate, not turned to him (s03 is the look back).
shots["s01"] = {"replace": [["turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person",
                             "facing the way she walks, her face in three-quarter profile, her eyes on the gate ahead, not on him"]]}
for sid in ["s41", "s42"]:  # the knife: Xu Yan unnamed, from behind
    shots[sid] = {"replace": [[ONLY_SHE, besides("her", "the young man seen from behind with the lantern")]]}

spec = {
    "_note": ("e913 live d1 (e912-live/spec.json's way, written by mkspec.py). s04, s10, s12, s21, s23 and s32 are Tang Xiaotang's "
              "lines shot from behind her (nospeak, recordings laid in): her three face pictures and her identity sentence go (e908 fix1, "
              "e909 s09/s12, e910 s23/s30, e912 s06/s14/s29); s07 and s09, her other two lines, are inserts of her hands with no picture of her; in s32 the young man beside her "
              "is unnamed too (review.md 必改 4). s13 and s25 are her silent face shots: e907's neutral face sentences (as e912 "
              "s02/s05/s17/s24). s03, s16, s20, s41 and s42: ref2manifest's 'only person' sentence is rewritten to admit the unnamed "
              "back, shoulder or hand the composition describes (s41-s42: Xu Yan from behind with no picture, bible rule 5 for the "
              "knife shots). s35: the only person in the whole grove (review.md 必改 3). s01: her eyes on the gate, not on him "
              "(review.md 建議). No off-screen sentence is in these "
              "prompts (r2.py OFFSCREEN_SPEECH = False). Seeds 9131101/9131102."),
    "seeds": [9131101, 9131102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
