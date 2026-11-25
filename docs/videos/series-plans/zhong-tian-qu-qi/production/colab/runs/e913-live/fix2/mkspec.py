"""e913 fix2: the grove retakes s35 s37 s38 s42 (picks-merged.tsv), shot on the redrawn set-zhulin-fen-l3
(live-action/screen-test-e014.py: an edit of l2 without the metal fire bowl, its sparks and the board on the ground, with a
low earth grave mound, a small upright blank plank and a small heap of paper burning on the bare earth). Seeds
9131301/9131302. NOT built yet: the picture is not in refs-live. When it is, run
/tmp/claude-0/-home-user/e6a64eea-98ea-5986-b96b-5cdbc5d1572e/scratchpad/prep913fix2.sh (a copy of the steps is in its
header). retake.py cannot swap a reference picture (it only drops: drop_angles, drop_pictures, drop_set), so the script
re-runs live-action/pilot.py for these four shots only, from the CG stage-1 manifests in ../a/st1, into
live/fix2/st1-l3: pilot.py maps every set picture to its newest l-version, so the four jobs get set-zhulin-fen-l3 and
their prompts come out byte-identical to live/st1 (checked: pilot.py reproduces live/st1's s35 s37 s38 s42 exactly while
l2 is the newest). retake.py then runs from st1-l3 with this spec.json, as fix1 runs from st1.

Why (both reviews of d1): s42 both takes have the old picture's metal brazier and no grave, the lantern drawn as a candle
dish; s37 both takes hang coloured bead strings across the frame and give him a metal oil lamp; s35 both takes walk him to
the grave before Qin Shuang is there (s36 has her kneeling at it); s38 no grave in the frame, she squats, smiles (picks-a
kept 1102 2.625-6.583 as the fallback).

Rewrites (fix1's rule, bible 拍法 18: background and props written as what is there, no negative nouns):
- the grove headers lose NORACK and the list of buildings/roofs/doorways/lanterns/lit windows (1102 of s37 drew a roofed
  building and two lights anyway): only dense dark bamboo stalks growing straight up into black night;
- the lantern is "one round white paper lantern held by its bamboo handle" (d1 drew metal lamps and candle dishes);
- s35 has no grave and no clearing in the frame (picks-a: the header put the grave in a shot that wants him alone and
  hidden): a narrow path between bamboo, a faint orange glow far off whose source the stalks hide;
- s38 kneels upright in profile on screen left with the mound and its blank plank filling the right of the frame;
- s42 is e914 s01's first frame (writer-tools/e014-r2/r2.py s01, "the same framing at the same instant"): from behind
  him pressed against a bamboo stalk on screen left, the lantern in his left hand lighting her face, his right hand
  raised open beside his head below the line of her eyes; Qin Shuang a little right of the middle, eyes still a little
  red-rimmed, the knife level in her right hand (the screen-left side of her body), edge one finger from the left side of
  his neck, blunt back to the lens; far behind her the mound and the paper fire burnt low. The knife is written by its
  shape (a narrow dark iron blade two fingers wide) instead of "not a broad cleaver, not a sword" (s41 1102 drew a broad
  cleaver under that sentence);
- no smile is written as things they do; extras' artefact nouns go as in fix1. All four bought at 6 s.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]

EXTRAS = [", and no neon lines, no glowing streaks, no light rain, no strings of beads and no glitch effects anywhere.",
          "; the air is clear and still, a clean natural film image."]
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame,"
LANTERN = ["one blank paper lantern with no writing and a small burning candle inside",
           "one round white paper lantern held by its bamboo handle, a small candle glowing inside its plain white paper"]
BACK = ("behind them only dense dark bamboo stalks growing straight up and fading into black night, their edges touched by "
        "cold blue starlight")
GROVE_C = ["no weapon rack, no spears and no poles or sticks leaning anywhere; behind them only dense dark bamboo and black "
           "night: no building, no roof, no doorway, no lantern and no lit window anywhere in the background; the only warm "
           "light is the little fire of burning blank paper low on the ground",
           BACK + "; the only warm light is the little fire of burning blank paper low on the bare earth"]
NOBLADE = ["; no blade, no knife, no sword, no scabbard and no weapon of any kind anywhere in the frame", ""]
GROVE_FULL = ("In the bamboo grove behind the village at night: dense tall bamboo on both sides, a narrow dirt path, a small "
              "clearing, in the clearing a small low earthen grave mound with one plain blank wooden marker board on a post "
              "beside it, no characters on it, dry fallen bamboo leaves on the ground, beyond the clearing only more dense "
              "bamboo fading into black; nothing built anywhere: no building, no roof, no doorway, no lantern hanging anywhere "
              "and no lit window; no weapon rack, no spears and no poles or sticks leaning anywhere, only living bamboo "
              "growing straight up; deep night with no moon, a sky full of cold stars, cold blue starlight, a light wind in "
              "the bamboo leaves, no daylight anywhere")
PATH = ("In the bamboo grove behind the village at night, deep inside the dense bamboo: a narrow dirt path covered with dry "
        "fallen bamboo leaves winding between tall living bamboo stalks growing straight up on both sides, the stalks "
        "fading into black night; far off beyond the stalks on screen right only a faint warm orange glow low on the "
        "ground, its source hidden behind the bamboo; deep night with no moon, a sky full of cold stars, cold blue "
        "starlight, a light wind in the bamboo leaves")

S = {
 "s35": {"replace": D1SPEC["s35"]["replace"] + [
   [GROVE_FULL, PATH], EXTRAS, NOBLADE, LANTERN,
   ["He is the only person in the frame and the only person in the whole grove; nobody else, no second lantern and no other "
    "light anywhere among the bamboo; no second copy of anyone appears.",
    "He is the only person in the frame and the only person on the path; his shaded lantern and the faint far glow are the "
    "only lights; no second copy of anyone appears."],
   ["tense: eyes wide, lips closed, no smile; the one lantern in his hand is the only lantern; nobody else anywhere in the grove.",
    "tense: eyes wide, jaw tight, lips pressed together, every few steps he holds his breath and listens."],
   ["Xu Yan creeps from one bamboo stalk to the next, stops to listen, then moves on toward screen right;",
    "Xu Yan creeps from one bamboo stalk to the next, keeping behind them, stops once with his shoulder against a stalk to "
    "listen toward the far glow, then moves on toward screen right, the glow staying far off and small;"]],
  "duration_seconds": 6},
 "s37": {"replace": [
   [GROVE_C[0] + " and the one lantern in the young man's hand", GROVE_C[1] + " and the one paper lantern in the young man's hand"],
   EXTRAS,
   ["the lantern held low at his left hip,",
    "one round white paper lantern held low by its bamboo handle at his left hip, a small candle glowing inside its plain "
    "white paper,"],
   ["holding his breath, lips closed the whole shot.",
    "holding his breath, lips pressed together the whole shot, his right palm flat against the bamboo stalk."],
   ["he is thinking, not speaking; " + NOSMILE,
    "he is thinking, not speaking; he swallows once, his throat moving, his eyes glistening and his lips pressed together "
    "to the last frame,"]],
  "duration_seconds": 6},
 "s38": {"replace": [
   GROVE_C, EXTRAS, NOBLADE, ["burning plain blank paper with no writing,", "burning plain blank paper,"],
   ["kneeling in front of the small grave mound on screen right, framed from the chest up with space above her head, her "
    "face in profile toward screen right toward the grave, never the lens;",
    "kneeling upright on both knees on the bare earth in profile on screen left, the low earthen grave mound with its small "
    "blank upright weathered plank filling the right side of the frame, framed from the waist up with space above her head, "
    "her face in profile toward screen right toward the grave, never the lens; the little fire of plain blank paper burns "
    "directly on the bare earth between her knees and the mound;"],
   ["grieving: eyes wet and lowered, brows drawn, lips trembling and moving softly between words, no smile;",
    "grieving and resolute: eyes wet and lowered, brows drawn together, her chin trembling, lips moving softly between "
    "words and pressed together between them;"],
   ["behind her only bamboo shadows", "behind her only dark bamboo stalks fading into black night"],
   ["Qin Shuang feeds one small square of plain blank paper into the little fire, lets it go and bows her head; " + NOSMILE,
    "Qin Shuang feeds one small square of plain blank paper into the little fire, lets it go and bows her head; after the "
    "last word she bows her head lower and presses her lips together, her eyes glistening, still kneeling upright to the "
    "last frame,"]],
  "duration_seconds": 6},
 "s42": {"replace": D1SPEC["s42"]["replace"] + [
   [GROVE_C[0] + " and the one lantern in the young man's hand", GROVE_C[1] + " and the one paper lantern in the young man's hand"],
   EXTRAS, LANTERN,
   ["and his right hand raised open beside his head, his face never in the frame;",
    "and his right hand raised open and empty beside his head on screen right, below the line of her eyes, not covering "
    "her face or the knife, his face never in the frame;"],
   ["framed from the chest up with space above her head, her face three-quarter to screen left toward him, never the lens; "
    "low and cold: eyes locked on him, brows down, lips moving low between words, no smile;",
    "framed from the chest up with space above her head, her eyes still a little red-rimmed, her face three-quarter to "
    "screen left toward him, never the lens; low and cold: eyes locked on him, brows drawn down, jaw clenched, lips moving "
    "low between words and pressed shut between them;"],
   ["a thick blunt back and a nicked cutting edge, not a broad cleaver, not a sword,",
    "two fingers wide, a thick blunt back and a nicked cutting edge,"],
   ["far behind her the small grave with the little paper fire still burning; no other blade, knife, sword, scabbard or "
    "weapon anywhere in the frame; the young man's hands hold only the lantern; exactly two people.",
    "far behind her, small and soft, the low earthen grave mound with its small blank upright plank and the little heap of "
    "blank paper burnt low on the bare earth in front of it, its last flames glowing dull orange; the knife in her right "
    "hand is the only metal in the frame; the young man's left hand holds only the paper lantern; exactly two people."],
   ["the young man's raised hand trembles; he keeps the back of his head toward us the whole shot; " + NOSMILE,
    "the young man's raised hand trembles; he keeps the back of his head toward us the whole shot; after the last word "
    "she holds still, jaw clenched, lips pressed shut, eyes locked on him to the last frame,"]],
  "duration_seconds": 6},
}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9131301, 9131302], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
