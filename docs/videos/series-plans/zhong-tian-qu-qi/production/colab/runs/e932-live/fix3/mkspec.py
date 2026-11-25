"""e932 fix3: the mud retake of s21, s26 and s26b. NOT RUN: written and checked (mkjobs.py, preflight-prompts.py,
check_manifest.py), nothing is sent. Why, in plan.md.

    python3 -I mkspec.py                       # -> spec.json (3 shots, their own two seeds each)
    python3 -I mkjobs.py <live>/fix3           # -> <live>/fix3/prompts/*.txt, retake.json, colab-jobs.json (6 jobs, 44 s)
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix3/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix3/colab-jobs.json

Run on the Colab session zt-live3 (pass --session zt-live3 when it is sent; the manifest is not bound to a session).

What went wrong (review3-plan.md sections 0 and 4; e932r3/img/gold_s21a.jpg, gold_s26.jpg, gold_s26b.jpg): the mud on
Xu Yan's face and robe (and on the carrier's jacket) came out as separate shiny gold-leaf flakes shaped like maple leaves,
with jagged edges; grading turned the colour grey-brown but kept the shape. In d1 the words that drew them were, all in
the shared XU_MUD of r2.py: "caked" (a crust that breaks into flakes) and "wet yellow mud", lit by "low orange evening
sun from the left" and "in the low orange light" (yellow mud under orange sun = gold). d1 had no spots/patches/flecks words.
The fix, the bible's rule (〈人物〉: the mud one broad area on the robe and the cheeks, never dots), written positively:
- the mud is one broad even coat of wet dark-brown mud paste, smooth and matte like the soil of the field, darker than
  his skin; the robe is soaked with one wide wet dark-brown stain; his hair matted with the same mud; his eyes, nose and
  lips left clean (the face must still read as Xu Yan);
- the light: the low sun stays at the left as in the scene, but Xu Yan is in soft even shade; s21 lies in the long
  shadow of the earth heap (no warm light in the frame); s26/s26b keep the warm sun only on the willow and the sky far
  behind him; the closing "the low orange evening light stays unchanged" becomes "the soft shade on his face";
- s26 and s26b: one carry for both, the one of s25 (fix1 9321202): he lies crosswise across the carrier's shoulders, his
  legs beyond the left edge, his head and one limp arm down past her shoulder in the right half of the frame, his face
  sideways to us, his cheek on the dark brown cloth of her shoulder (the picked s26 1101 and s26b 1102 were already a
  sideways face on the brown back; "slung head down ... face upside down" goes); her jacket written as plain even dark
  brown cloth; exactly one head and one face (s26b 1101 had two Xu Yan faces);
- the d1 actions, lines, pictures and seconds stay; NOSMILE for all three (s26 1101 lifted the corners of his mouth).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e932-dh/runpod/live/d1")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = {"s21": [9321401, 9321402], "s26": [9321403, 9321404], "s26b": [9321405, 9321406]}
DUR = {"s21": 8, "s26": 8, "s26b": 6}  # the d1 lengths (r2.py BUY; d1 colab-jobs.json)


def d1text(sid):
    return (D1 / "prompts" / f"ref-{sid}-9321101.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert d1text(sid).count(s) == 1, (sid, s[:60])
    return s


# the mud, the bible's way: one broad area, wet, dark brown, matte; written by what it is
MUD = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, one broad even coat of wet dark-brown mud paste "
       "over his forehead, cheeks and jaw, smooth and matte like the soil of the field and darker than his skin, his eyes, "
       "nose and lips left clean, the whole front of his robe and both sleeves soaked through with one wide wet dark-brown "
       "mud stain, the cloth dark and heavy with it, his hair matted with the same dark-brown mud")
XU_MUD = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, the robe, his arms and his face caked with wet "
          "yellow mud, his hair matted")
JM = "low orange evening sun from the left, long shadows to the right across the cracked furrows: "
LIGHT_END = "and the low orange evening light stays unchanged."
SHADE_END = "and the soft even shade on his face stays the same to the last frame."

# s26 and s26b: one carry, the one of s25 fix1 9321202 (across both shoulders, head and arms down at screen right)
CARRY = ("lying limp across the shoulders of the one who carries him, his body crosswise behind her neck, his legs beyond "
         "the left edge of the frame, his head and one limp arm down past her shoulder in the right half of the frame, his "
         "face turned sideways to us, his cheek resting on the dark brown cloth of her jacket's shoulder, her jacket plain "
         "even dark brown cloth all over")
BACK = ("behind him, soft and far, the wide evening sky and the long drooping branches of a willow, the warm low sun only "
        "on the willow and the sky far behind him; his face, his robe and the mud on them in soft even shade.")
SHADE_JM = ("the low evening sun far behind them at the left, warm only on the willow and the sky in the distance, soft even "
            "shade over the near figures: ")

S = {sid: {"seeds": SEEDS[sid], "duration_seconds": DUR[sid], "replace": []} for sid in SEEDS}

S["s21"]["replace"] = [
    [once("s21", JM),
     "the low evening sun far at the left behind the earth heap, the long cool shadow of the heap lying over the near side "
     "of the pit: "],
    [once("s21", XU_MUD), MUD],
    [once("s21", "nearly fainted, not smiling: slack face, brows loose, lips barely moving between breathy words;"),
     f"nearly fainted, not smiling: slack face, brows loose, lips barely moving between breathy words, {NOSMILE};"],
    [once("s21", "only the cracked dry yellow furrows with a few short dead stalks around his head and shoulders to every "
                 "edge, in the low orange evening light;"),
     "only the cracked dry furrows with a few short dead stalks around his head and shoulders to every edge, all of him and "
     "the earth around him in the same soft even shade light;"],
    [once("s21", LIGHT_END), SHADE_END],
]
S["s26"]["replace"] = [
    [once("s26", JM), SHADE_JM],
    [once("s26", XU_MUD), MUD],
    [once("s26", "slung head down over a shoulder, his muddy cheek against the dark brown cloth of a jacket's back, his face "
                 "upside down in the frame, his eyes half closed at first, never the lens; he is the only one whose face is "
                 "in the frame; dazed, not smiling: lips pressed shut; behind him, soft, the wide evening sky and the long "
                 "yellowed hanging branches of a willow in the low orange light."),
     f"{CARRY}; his eyes half closed at first, never the lens; his is the only face in the frame, exactly one head and one "
     f"face, his; dazed, not smiling: lips pressed shut, {NOSMILE}; {BACK}"],
    [once("s26", LIGHT_END), SHADE_END],
]
S["s26b"]["replace"] = [
    [once("s26b", JM), SHADE_JM],
    [once("s26b", XU_MUD), MUD],
    [once("s26b", "slung head down over a shoulder, his muddy cheek against the dark brown cloth of a jacket's back, his face "
                  "upside down in the frame, his eyes a narrow crack, never the lens; he is the only one whose face is in the "
                  "frame; a faint stubborn hope, not smiling: eyes a narrow crack, brows drawn a little, lips pressed shut; "
                  "behind him, soft, the wide evening sky and the long yellowed hanging branches of a willow in the low "
                  "orange light."),
     f"{CARRY}; his eyes a narrow crack, never the lens; his is the only face in the frame, exactly one head and one face, "
     f"his; a faint stubborn hope, not smiling: eyes a narrow crack, brows drawn a little, lips pressed shut, {NOSMILE}; "
     f"{BACK}"],
    [once("s26b", LIGHT_END), SHADE_END],
]

(HERE / "spec.json").write_text(json.dumps({"base": "d1 9321101 prompt and job", "shots": S}, ensure_ascii=False, indent=1)
                                + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
