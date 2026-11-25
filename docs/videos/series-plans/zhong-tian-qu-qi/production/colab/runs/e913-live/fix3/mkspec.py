"""e913 fix3: the pick-stage review's retakes (pick-review.md 一): s06 and s41 (must reshoot), s11 and s40 (optional in the
review, taken by the coordinator). Seeds 9131401/9131402. Built by
/root/mokaair-work/videos/zhong-tian-qu-qi-e913-dh/runpod/live/prep913fix3.sh (fix2's prep913fix2.sh, four shots):
live-action/pilot.py re-runs these four shots from the CG stage 1 (runpod/a/st1) into live/fix3/st1-fix3, so the grove
shots s40 s41 get set-zhulin-fen-l3 (pilot.py maps every set picture to its newest l-version; d1 sent l2) and s06 s11
come out byte-identical to live/st1 (set-xujia-yuan-l3 is already the newest); retake.py then runs from st1-fix3 with
this spec.json (the d1 edits of ../spec.json first), and mkjobs.py sets duration_seconds and output_path.

Why (pick-review.md 嚴重 1-2, 中等 5 and 11):
- s06: both d1 takes put two weapon racks with red-tasselled spears round his head for the whole 10 s; the root is the
  set picture (set-xujia-yuan-l3 has a board and a pole leaning by the well where s02 s06 s11 grew the racks) plus the
  negative nouns in the prompt. So: no set picture (drop_set; the review: a close-up has no use for it) and the
  background written as what is there: a low woven bamboo fence below his shoulders, a cut stubble field and the sunrise
  sky filling the upper half of the frame round his head. Bought at 10 s as st1 (a06 3.29 + a07 4.60 + 0.5 = 8.39 s).
- s11: a row of red-tasselled spears on screen right and a toothy laugh from 0.5 s on (the script allows a closed-mouth
  rueful half smile). No set picture either (the same pole), the house wall written as fix1 s08's success (bare earthen
  wall, small lattice window, woodpile), the neck scratch put first with his lips pressed together, the half smile
  written as what the mouth does. Bought at 8 s as st1, not the review's 6: a12 is 5.20 s and the scratch comes first.
- s40: two warm lights deep in the bamboo and the paper fire on top of the grave (l2). Now l3, the bamboo written as
  stalks fading into black, the paper fire on the bare earth in front of the stone-heaped mound, her hands on her knees.
- s41: l2's pointed sand heap with a candle on top, a plank with a line of fake writing, a tall cylinder lantern plus a
  candle dish in his other hand, a wide bright path and a blue sky; s42 (fix2 9131302) has l3's low mound of piled earth
  and stones, an upright blank plank, the paper fire on the ground and one round white paper lantern hanging low. So
  s41 is written to s42: the same mound, plank, fire and lantern, and the knife drawn as s42 drew it (a dark iron blade
  about three fingers wide with a squared tip), in her right hand on the screen-left side of her body.
Rules (bible 拍法 18, fix1 and fix2): backgrounds and props written as what is there, no negative nouns (NORACK, the
grove's list of buildings and lights, NOBLADE and extras.json's five artefact nouns go); no smile written as things the
face does; the hands and the props they hold placed in the first-frame composition sentence.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]

EXTRAS = [", and no neon lines, no glowing streaks, no light rain, no strings of beads and no glitch effects anywhere.",
          "; the air is clear and still, a clean natural film image."]
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame,"
BACK = ("behind them only dense dark bamboo stalks growing straight up and fading into black night, their edges touched by "
        "cold blue starlight, the spaces between the far stalks pure black")
GROVE_C = ["no weapon rack, no spears and no poles or sticks leaning anywhere; behind them only dense dark bamboo and black "
           "night: no building, no roof, no doorway, no lantern and no lit window anywhere in the background; the only warm "
           "light is the little fire of burning blank paper low on the ground",
           BACK + "; the only warm light is the little fire of burning blank paper on the bare earth"]
NOBLADE = ["; no blade, no knife, no sword, no scabbard and no weapon of any kind anywhere in the frame", ""]
GROVE_FULL = ("In the bamboo grove behind the village at night: dense tall bamboo on both sides, a narrow dirt path, a small "
              "clearing, in the clearing a small low earthen grave mound with one plain blank wooden marker board on a post "
              "beside it, no characters on it, dry fallen bamboo leaves on the ground, beyond the clearing only more dense "
              "bamboo fading into black; nothing built anywhere: no building, no roof, no doorway, no lantern hanging anywhere "
              "and no lit window; no weapon rack, no spears and no poles or sticks leaning anywhere, only living bamboo "
              "growing straight up; deep night with no moon, a sky full of cold stars, cold blue starlight, a light wind in "
              "the bamboo leaves, no daylight anywhere")
GRAVE = ("in a small patch of bare earth strewn with dry fallen bamboo leaves, tall living bamboo stalks crowding close "
         "all round it, the low grave mound of piled earth and stones with one small upright blank weathered plank at its "
         "head, and in front of the mound a small heap of blank paper burning directly on the bare earth")
GROVE41 = ("In the bamboo grove behind the village at night, deep inside the dense bamboo: " + GRAVE + "; the bamboo leaves "
           "close overhead, cold blue starlight filtering down through them, a light wind in the leaves")
YARD_LIGHT = "In the morning yard of the Xu farmhouse at sunrise, low cool golden autumn sunlight from the right; no weapon rack, no spears and no poles or sticks leaning anywhere:"

S = {
 "s06": {"replace": [
   [YARD_LIGHT, "At the edge of the Xu farmhouse yard at sunrise, low cool golden autumn sunlight from screen right:"],
   ["close-up of Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe, framed from the chest "
    "up with space above his head, his eyes red-rimmed and bloodshot after a night without sleep, standing still in the "
    "yard, his face three-quarter to screen right, never the lens; at first stopped short, then exasperated: eyes rolling "
    "up to the sky, then shutting for a moment, a long breath out, lips closed the whole shot; behind him only the "
    "packed-earth yard wall in the low morning light.",
    "close-up of Xu Yan, in his old plain grey cloth outer coat over his faded blue-grey scholar's robe, framed from the "
    "chest up with clear space above his topknot, his eyes red-rimmed and bloodshot after a night without sleep, standing "
    "still, both arms hanging at his sides below the bottom of the frame, his face three-quarter to screen right, never the "
    "lens; at first stopped short, then exasperated: eyes rolling up to the sky, then shutting, one long breath out through "
    "his nose, lips pressed together the whole shot; behind him only a low woven fence of thin pale bamboo stakes tied with "
    "twine, soft and out of focus, its top below the line of his shoulders, and beyond it an open field of cut stubble and a "
    "wide pale sunrise sky that fills the whole upper half of the frame around his head; the cool golden light from screen "
    "right rims his cheek."],
   ["Xu Yan stops mid-step; his eyes roll up toward the sky; then he shuts his eyes for a moment and lets out a long breath;",
    "Xu Yan stops mid-step; his eyes roll up once toward the sky; then he closes his eyes and lets out one long slow breath "
    "through his nose, his shoulders sinking; then he opens his eyes, brows drawn together, tired and stubborn;"],
   ["he is thinking, not speaking; " + NOSMILE,
    "he is thinking, not speaking; after he opens his eyes he keeps his brows drawn together, his jaw set and his lips "
    "pressed flat to the last frame,"],
   EXTRAS],
  "drop_set": True, "duration_seconds": 10},
 "s11": {"replace": [
   [YARD_LIGHT, "In the morning yard of the Xu farmhouse at sunrise, low cool golden autumn sunlight from screen right:"],
   ["close-up of Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe, framed from the chest "
    "up with space above his head, his eyes red-rimmed and bloodshot after a night without sleep, his face three-quarter to "
    "screen left toward the young woman off screen left, never the lens; rueful: brows up, a wry closed-lipped half-smile, "
    "teeth never showing, lips moving between words; behind him only the packed-earth yard wall.",
    "close-up of Xu Yan, in his old plain grey cloth outer coat over his faded blue-grey scholar's robe, framed from the "
    "chest up with space above his head, his eyes red-rimmed and bloodshot after a night without sleep, his right hand "
    "already raised to the back of his neck, his left arm hanging at his side below the bottom of the frame, his face "
    "three-quarter to screen left toward the young woman off screen left, never the lens; wry and rueful: brows lifted, one "
    "corner of his mouth tucked in, lips together between words, teeth showing only while forming a word; behind him only "
    "the bare earthen house wall with its small lattice window and the stacked woodpile below it, soft and out of focus; "
    "the wall is completely bare and smooth."],
   ["Xu Yan speaks a short Mandarin line,",
    "First, with his lips pressed together, Xu Yan scratches the back of his neck with his right hand and glances once "
    "toward the yard gate off screen right; then he lowers the hand to his side, looks back at her and speaks a short "
    "Mandarin line,"],
   ["Xu Yan rubs the back of his neck with one hand and glances toward the yard gate off screen right, then looks back at "
    "her as he speaks,",
    "after the last word he presses his lips together in a small closed-mouth half smile, one corner of his mouth tucked "
    "in, and gives one small tired shake of his head,"],
   EXTRAS],
  "drop_set": True, "duration_seconds": 8},
 "s40": {"replace": [
   GROVE_C, NOBLADE, EXTRAS,
   ["kneeling, framed from the chest up",
    "kneeling, both hands resting empty on her knees, framed from the chest up"],
   ["beside her on screen right the grave mound and the little paper fire, the rest only dark bamboo",
    "just beside her on screen right the small heap of blank paper burning directly on the bare earth at the height of her "
    "knees, and behind the fire the low grave mound of piled earth and stones with its one small upright blank plank; the "
    "rest of the frame dense dark bamboo stalks fading into black night"],
   [NOSMILE, "her jaw set, her eyes held on the dark bamboo at screen left to the last frame,"]],
  "duration_seconds": 6},
 "s41": {"replace": D1SPEC["s41"]["replace"] + [
   [GROVE_FULL, GROVE41], EXTRAS,
   ["medium shot from just behind one young man seen only from behind, appearing only once, half hidden behind bamboo "
    "stalks on screen left in the foreground: only the back of his black topknot, his shoulder in an old plain grey cloth "
    "coat and one blank paper lantern with no writing and a small burning candle inside held low in his left hand, his face "
    "never in the frame; on screen right a few steps away, beside the small grave and its little paper fire, the shot opens "
    "with Qin Shuang,",
    "medium shot, locked off, the whole action inside the frame: in the left foreground, from close behind, one young man "
    "seen only from behind, appearing only once, standing beside a thick bamboo stalk at the left edge of the frame: only the "
    "back of his black topknot and the shoulders of his old plain grey cloth coat, his face never in the frame, one round "
    "white paper lantern hanging from its bamboo handle low in his left hand, a small candle glowing inside its plain white "
    "paper, his right arm hanging empty at his side; on screen right a few steps away, beside the low grave mound of piled "
    "earth and stones with its one small upright blank plank and the small heap of blank paper burning on the bare earth "
    "in front of it, the shot opens with Qin Shuang,"],
   ["already half risen from her knees, one old chopping knife with a short plain wooden handle and a dark iron blade only "
    "a little longer than a palm, a thick blunt back and a nicked cutting edge, not a broad cleaver, not a sword held low at "
    "her side in her right hand, which is the hand on the screen-left side of her body, nearest him, framed full length "
    "with space above her head, her face three-quarter to screen left toward him, never the lens; fierce: eyes cold and "
    "hard, jaw set, lips closed, no smile; the whole movement stays inside the frame; no other blade, knife, sword, "
    "scabbard or weapon anywhere in the frame; the young man's hands hold only the lantern; exactly two people.",
    "already half risen from her knees, framed full length with space above her head, her face three-quarter to screen "
    "left toward him, never the lens; cold and fierce: brows drawn down, eyes locked on him, jaw set, lips pressed shut; in "
    "her right hand, which is the hand on the screen-left side of her body, nearest him, one old chopping knife with a "
    "short plain wooden handle and a dark iron blade about three fingers wide and a little longer than a palm, a thick "
    "blunt back and a squared tip, held low at her side, her left hand empty; behind her only dense dark bamboo stalks "
    "fading into black night; the paper fire on the bare earth in front of the mound and his one paper lantern are the "
    "only lights; the knife in her right hand is the only metal in the frame; the young man's left hand holds only the "
    "paper lantern; exactly two people."],
   ["Qin Shuang comes fully up and takes two fast steps toward him, the knife raised in her right hand on the screen-left "
    "side of her body, the same hand the whole shot; the young man stumbles back against a bamboo stalk beside him, the "
    "lantern swinging in his left hand, his head never turning toward us;",
    "Qin Shuang springs up to her full height and takes two fast steps toward him, the knife rising level in the same right "
    "hand on the screen-left side of her body; the young man jerks back and his shoulders hit the bamboo stalk beside him, "
    "the lantern swinging once in his left hand, the back of his head toward us the whole shot;"],
   ["no talking, no mouthing words, no smile at any moment,",
    "no talking, no mouthing words, her brows drawn down and her eyes locked on him to the last frame,"]],
  "duration_seconds": 6},
}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9131401, 9131402], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
