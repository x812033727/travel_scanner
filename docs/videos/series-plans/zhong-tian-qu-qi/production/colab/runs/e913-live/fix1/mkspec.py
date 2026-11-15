"""e913 fix1: retakes of the yard and the carpenter's lane (s05 s08 s15 s22 s27 s29), merged from review-picks-a/b
(picks-merged.tsv); the grove retakes (s35 s37 s38 s42) wait for set-zhulin-fen-l3 and are fix2. Same steps as e912 fix1:
retake.py from st1 (the d1 edits of e913-live/spec.json are applied first; none of these six has one), mkjobs.py for the
duration and output_path, preflight-prompts.py. Seeds 9131201/9131202.

Why each shot (both reviews; s15, s27, s29 were RETAKE for one reviewer, picks-merged.tsv has the frame checks):
- s05, s08: Xu Yan grins with his teeth through the line in all four takes; red-tasselled spears (s05 1101), two drawn
  swords on the house wall (s08 1101), bead strings and a spear rack filling the frame (both 1102).
- s15: both takes laugh the line first and pick up the plane after it (s16/s17 need the plane already in his hand).
- s22, s27, s29: Carpenter Shi laughs with his teeth in all six takes (the script: distrust, a glare, a grudging twitch);
  s27 grew a red-handled axe (1101) and a knife (1102) on the wall, s29 a narrow plank with an arrow on it.

The lesson both reviewers reached on their own (bible 拍法 18, from this draft): the negative nouns in the prompts were
drawn. Every yard prompt said "no weapon rack, no spears and no poles or sticks leaning anywhere" and nearly every yard
take grew spears or a rack, though set-xujia-yuan-l3 has none; the carpenter's TOOLS sentence listed "no knife, no sword,
no axe" and s27 drew an axe and a knife; extras.json's "no strings of beads" sat in every prompt and s02 s04 s05 s08 s11
(1102), s34 (1101) and s37 (both) hung bead strings across the frame. So in these six prompts:
- the background is written as what is there: bare earthen walls with nothing mounted on them or leaning against them,
  empty packed earth along their foot; the lane's bamboo poles smooth and round to their cut ends; the carpenter's wall
  with exactly one hand saw and one wooden hand plane on it. NORACK, LANE_POLES, NOBLADE, TOOLS and NOTBLIND go.
- the extras.json sentence keeps "no subtitles, captions or text" (the picture-clean rule) and loses the five artefact
  nouns (neon lines, glowing streaks, light rain, strings of beads, glitch effects), replaced by clear still air. Only the
  fix prompts change; extras.json and the shot clips are left as they are.
- no smile is never written as a negative: each face that must not smile gets things it does (lips pressed flat, brows
  knotted, a snort or grunt through the nose, a look away), and the late-grin window after the last word is held by an
  action (e912 fix1 lesson). The five no-smile shots are bought at 6 s instead of 8 (duration_seconds, applied by
  mkjobs.py): s22 a23 3.80 s, s27 a28 3.64 s, s29 a30 4.68 s, s05 a05 3.12 s, s08 a09 4.24 s. s15 keeps 8 (the pick-up
  takes the first two seconds, then a15's 3.24 s line).
- s15: the pick-up is written before the line, inside the speaking sentence ("First ... then Xu Yan speaks").
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]

EXTRAS = [", and no neon lines, no glowing streaks, no light rain, no strings of beads and no glitch effects anywhere.",
          "; the air is clear and still, a clean natural film image."]
NORACK = ["no weapon rack, no spears and no poles or sticks leaning anywhere",
          "the house wall and the yard wall are bare earthen walls with nothing mounted on them and nothing leaning against "
          "them, the ground along their foot empty packed earth"]
LANE = ["no weapon rack and no spear anywhere; the only long things leaning against the walls are plain green bamboo poles "
        "with no tips, no blades and no tassels",
        "the only long things leaning against the walls are a few plain green bamboo poles, smooth and round up to their cut "
        "ends; the earthen walls of the lane are bare"]
NOSIGN = ["no sign and no writing anywhere", "every board and wall plain and unmarked"]
NOBLADE = ["; no blade, no knife, no sword, no scabbard and no weapon of any kind anywhere in the frame", ""]
TOOLS = ["the only tools in sight are a hand saw hanging flat on the wall and a wooden plane; no knife, no sword, no axe, no "
         "scabbard and no weapon of any kind; nobody holds any tool except as described",
         "the only tools in sight are one hand saw hanging flat on the wall and one wooden hand plane"]
NOTBLIND = ["the board is a flat planed plank with charcoal lines on it, not a screen and not a blind",
            "the board is one wide flat planed plank as wide as his shoulders, with a drawn rectangle of dense fine parallel "
            "charcoal lines on its face and one small willow leaf drawn in their middle"]
WALL = ["behind him only the dark wooden wall with tools hanging on it",
        "behind him only the dark wooden wall with one hand saw hanging flat on it and one wooden hand plane on a peg beside it"]
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame,"


def shot(sid, extra, dur=None):
    s = {"replace": D1SPEC[sid].get("replace", []) + extra}
    if dur:
        s["duration_seconds"] = dur
    return s


S = {
 "s05": shot("s05", [NORACK, NOBLADE, EXTRAS,
   ["evasive: brows up, a sheepish look, lips moving between words, no smile; behind him only the yard wall and the gate",
    "evasive and tired: brows pinched together, his eyes sliding away toward the gate, jaw tight, lips pressed into a flat "
    "line between words, his cheeks still; his left hand hangs empty at his side; behind him only the bare earthen yard "
    "wall and the plain wooden gate"],
   ["Xu Yan backs away two steps toward the gate, waving one hand toward the young woman off screen left as he speaks; " + NOSMILE,
    "Xu Yan backs away two steps toward the gate, waving his right hand at waist height toward the young woman off screen "
    "left while he speaks, as if brushing the matter aside; after the last word he presses his lips flat, lets out one "
    "tired breath through his nose and turns his eyes to the gate, his brows pinched to the last frame,"]], 6),
 "s08": shot("s08", [NORACK, NOBLADE, EXTRAS,
   ["with a stack of plain blue cloth-covered account books on it",
    "with a tall stack of ten thread-bound account books on it, their covers plain unbroken dark blue cloth"],
   ["earnest: brows lifted, eyes wide, lips moving between words, no smile; behind him only the house wall, the woodpile and the morning light",
    "earnest and practical: brows level and drawn slightly together, eyes steady on her, jaw set, lips moving firmly "
    "between words and pressed flat between them, his cheeks still; behind him only the bare earthen house wall with its "
    "small lattice window and the woodpile stacked below it, and the morning light"],
   ["Xu Yan leans over the stone table and traces a square frame in the air above it with both hands; " + NOSMILE,
    "Xu Yan leans over the stone table and, while he speaks, traces a square frame the size of a bamboo mould in the air "
    "above it with both hands; after the last word he taps the top book once with two fingers and straightens, his brows "
    "drawn together and his lips pressed flat to the last frame,"]], 6),
 "s15": shot("s15", [LANE, NOSIGN, EXTRAS, TOOLS,
   ["half exasperated, half amused: one brow cocked, a wry closed-lipped half-smile, teeth never showing, lips moving between words;",
    "wry and exasperated: one brow cocked, one corner of his mouth tucked in, lips together between words, a short breath "
    "out through his nose, his cheeks still; at the first frame he is already bending down over the heap of shavings by the door;"],
   ["Xu Yan speaks a short Mandarin line,",
    "First, in the first two seconds, Xu Yan picks one carpenter's wooden hand plane, a smooth rectangular block of pale "
    "wood, up out of the heap of shavings, weighs it once in his right palm and straightens up; only then, holding the "
    "plane against his chest, eyeing the shut door sideways, Xu Yan speaks a short Mandarin line,"],
   ["Xu Yan bends down, picks one carpenter's wooden hand plane, a smooth rectangular block of pale wood up out of the shavings, weighs it in his hand and straightens up, eyeing the door sideways,",
    "the plane stays in his right hand against his chest from the moment he picks it up to the last frame; after the last "
    "word he cocks his head at the door and presses his lips together,"]]),
 "s22": shot("s22", [LANE, EXTRAS,
   ["distrustful: brow knotted, lips moving between words, no smile;",
    "sour and distrustful: brows knotted low, one eye narrowed, the corners of his mouth pulled down, lips tight and barely "
    "parting on each curt word, pressed flat between words;"],
   ["his eye flicks from one of them to the other and he snorts, his whole face staying in the gap of the door; " + NOSMILE,
    "his eye flicks from one of them to the other while he speaks; after the last word he snorts once through his nose, "
    "presses his lips flat, scowls and turns his face away from them toward the dark inside, his hand starting to pull the "
    "door shut, his face staying in the gap of the door,"]], 6),
 "s27": shot("s27", [LANE, EXTRAS, NOTBLIND, WALL, TOOLS,
   ["puzzled and suspicious: brows knotted tight, eyes narrowed, lips moving between words, no smile;",
    "puzzled and gruff: brows knotted tight, eyes narrowed, the corners of his mouth pulled down, lips moving curtly "
    "between words and pressed shut between them;"],
   ["Carpenter Shi presses one thick finger on the drawing on the board, then lifts his eyes and glares toward the young man off screen left; " + NOSMILE,
    "Carpenter Shi presses one thick finger on the small willow leaf in the middle of the board, then lifts only his eyes "
    "and glares from under his knotted brows toward the young man off screen left; after the last word he grunts through "
    "his nose, pushes the board an inch away with that finger and keeps glaring, his mouth pressed into a hard flat line "
    "to the last frame,"]], 6),
 "s29": shot("s29", [LANE, EXTRAS, NOTBLIND, WALL, TOOLS,
   ["holding the long planed board up close to his face", "holding the wide planed board up close to his face in both hands"],
   ["grudgingly won over: his knotted brows slowly loosening, one corner of his mouth twitching once, never a smile, teeth never showing, lips moving between words;",
    "grudgingly won over: his knotted brows slowly loosening, his lips pursed, one corner of his mouth twitching down once, "
    "lips moving low between words and pressed together between them;"],
   ["Carpenter Shi lifts the board close to his face and studies the drawing; his brows slowly loosen and one corner of his mouth twitches once,",
    "Carpenter Shi lifts the board close to his face in both hands and studies the dense fine lines and the small willow "
    "leaf in their middle; his brows slowly loosen, he purses his lips, grunts once through his nose and gives one slow "
    "small nod; after the last word he lowers the board, clicks his tongue and looks away sideways at the bamboo poles, "
    "his lips pressed together to the last frame,"]], 6),
}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9131201, 9131202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
