"""e911 fix1: retakes merged from review-picks-a/b (union: s02 s09 s13 s14 s16 s18), same steps as e910 fix1.

retake.py starts from st1, so the d1 edits of e911-live/spec.json for these shots (s02, s14) are applied first.
The episode's lessons, written into every retake:
- weapons: d1 already said "no sword / no scabbard / no spear" and Constable Zhao and the runners still wore sheathed
  blades and red-tasselled spears stood behind them. So: every shot framed from the chest up (waists below the frame
  edge), both hands of every person written (where, holding what), each extra man written as clothes plus one torch with
  "no spear, no sword, no scabbard, no blade of any kind" on him, and the words "constable", "yamen runner" and "runner"
  are gone (Zhao Butou's identity sentence and his comp). His portrait is chest-up with no waist, so it stays.
  Background people are cut where the storyboard does not need them (s13, s14, s16): dark farmhouse wall, torches
  held off screen.
- paper: no sheet front toward the lens. s09 shows only the blank backs; s18 shows the open sheet from its back, the two
  sentences picks-a traced the sparkles to are gone ("the torchlight shining through the back of the paper so the red
  glows", "the empty square seal outline catches the light"), and so is the seal outline itself: plain blank red paper,
  no characters, no seal, no gold, no glitter. (The seal now lives only in the lines of s17/s19/s30.)
- s14: Magistrate Hu's mouth shut and still, no smile, hands inside his sleeves below the frame.
- s02: the direction both reviewers asked for: all three backs to the camera, the young man runs out of the LEFT edge,
  the women turn only their heads left. Xu Yan's three face pictures go (picks-a), so his costume sentence goes first
  (retake.py exits otherwise) and he is written unnamed, from behind.
- red bead strings (seed glitch, d1 s01 s04 s28 s34): "no hanging beads, no bead curtains, no strings of red beads".
s18 keeps its set picture: retake.py cannot send a job with no pictures; the text keeps the yard out of focus.
"""
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]
ST1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e911-dh/runpod/live/st1/prompts")

LINES = ["Facial expressions follow the action and lines described below,", "Facial expressions follow the action described below,"]
BEADS = ["no strings of beads and no glitch effects anywhere.",
         "no strings of beads, no hanging beads, no bead curtains, no strings of red beads and no glitch effects anywhere."]
NOSHARP = ("no blade, no knife, no sword, no scabbard, no sheathed weapon at anyone's waist and no spear anywhere in the frame; "
           "every runner wears a plain black cloth sash with nothing hanging from it and holds only one burning torch, his other hand empty")
NOARMS = "no spear, no sword, no scabbard, no blade of any kind"
BACKDROP = ("behind them only the dark earth wall of the farmhouse, soft and out of focus, and the warm light of torches held "
            "off screen; no other person, no poles, no spears, no racks and no weapons anywhere")
TORCH = "holding one burning torch up beside his shoulder in his right hand, his left hand open and empty, resting flat on the front of his robe at chest height"
PAPER = "plain blank red paper, no characters, no seal, no gold, no glitter"
ZHAO_ID = ["an ancient Chinese Song-dynasty constable's soft black futou cap and a plain black round-collared constable's robe",
           "an ancient Chinese Song-dynasty soft black futou cap and a plain black round-collared cotton robe"]

xu_sentence = re.search(r"Xu Yan shown in <Picture 1>, <Picture 2> and <Picture 3> \(the same man from several angles\)[^;]*; ",
                        (ST1 / "ref-s02.txt").read_text(encoding="utf-8")).group(0)

S = {
 "s02": {"replace": D1SPEC["s02"]["replace"] + [
   [xu_sentence, ""],
   ["medium shot from inside the yard looking toward the open plain wooden yard gate: Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe, standing in the gateway with both arms spread across it, framed from the knees up with space above his head, at first his back to us facing out to the dark road;",
    "medium shot from inside the yard looking toward the open plain wooden yard gate, the camera behind all three people: in the far middle, in the gateway, one tall young man seen only from behind, in an old plain grey cloth outer coat over a faded blue-grey robe, his black hair in a topknot tied with a cloth band, both arms spread wide across the gateway, blocking it, his back to us, facing out to the dark road, his face never seen, framed from the knees up with space above his head;"],
   ["both facing the gate; when they turn, Tang Xiaotang frightened:",
    "both with their backs to us, facing the gate, Tang Xiaotang holding the abacus against her chest with both hands, Qin Shuang's left hand empty at her side; nobody faces the camera and nobody looks at the lens at any moment; when they turn their heads we see them only in profile, Tang Xiaotang frightened:"],
   ["at a sound from the house Xu Yan whips round to face screen left and shouts one short word, his mouth opening wide once, then drops his arms and breaks into a run past the two women toward the house door off screen left; Tang Xiaotang and Qin Shuang turn their heads toward the house door after him, their lips closed;",
    "at a sound from the house door off screen LEFT the young man drops his arms, turns toward screen left and runs toward screen LEFT, past the two women on their left side and out of the left edge of the frame, his face never toward the camera; nobody runs toward screen right and nobody runs toward the camera; Tang Xiaotang and Qin Shuang turn only their heads toward screen left after him, their bodies still facing the gate, their lips closed, never looking at the camera;"],
   LINES, BEADS],
  "drop_pictures": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "xuyan-angle-b-l1.png"]},
 "s09": {"replace": [
   ["only his old grey cloth shoulder, the folded red paper raised in his right hand and the back of his black topknot",
    "only his old grey cloth shoulder, his raised right hand holding three folded red papers shut with only their plain blank red backs toward the camera, " + PAPER + ", and the back of his black topknot"],
   ["framed from the knees up with space above his head, the torchlight striking up from under his chin",
    "framed from the chest up with space above his head, his waist below the bottom edge of the frame, the torchlight striking up from under his chin"],
   ["two yamen runners in ancient Chinese Song-dynasty plain black round-collared robes, black caps and cloth shoes behind him, each holding one burning torch; " + NOSHARP + ".",
    "behind him two men in ancient Chinese Song-dynasty plain black round-collared cotton robes and soft black cloth caps, seen from the chest up, their waists below the bottom edge of the frame, each man " + TORCH + "; on each man " + NOARMS + "; nobody holds anything but those two torches and the red papers; no poles, no spears, no racks and no weapons anywhere behind them."],
   ["Magistrate Hu snorts and flings his wide sleeve out, pointing past the young man toward screen left,",
    "Magistrate Hu snorts and flings his right wide sleeve out, pointing past the young man toward screen left with his right forefinger, his left hand clenched at his chest and holding nothing,"],
   BEADS]},
 "s13": {"replace": [
   ZHAO_ID,
   ["in front, framed from the knees up with clear space above his head,",
    "in front, framed from the chest up with clear space above his head, his waist and every waist below the bottom edge of the frame,"],
   ["one step behind him on screen right Constable Zhao, in his black futou cap and plain black round-collared constable's robe, a plain black cloth sash at his waist with nothing hanging from it, one burning torch in his right hand, his face lowered, eyes on the ground, lips closed; " + NOSHARP + ".",
    "one step behind him on screen right Zhao Butou, in his soft black futou cap and plain black round-collared cotton robe, seen from the chest up, " + TORCH + ", his face lowered, eyes on the ground, lips closed; on him " + NOARMS + "; Magistrate Hu holds nothing: his right hand jabs one forefinger and his left hand is clenched at his chest; " + BACKDROP + "."],
   ["Magistrate Hu stamps one foot and jabs his forefinger toward screen left, his cheeks quivering; Constable Zhao lowers his head further;",
    "Magistrate Hu's shoulders jerk as he stamps, and he jabs his right forefinger toward screen left, his cheeks quivering; Zhao Butou lowers his head further, the torch steady in his right hand;"],
   BEADS]},
 "s14": {"replace": D1SPEC["s14"]["replace"] + [
   ["framed from the waist up with space above his head,",
    "framed from the chest up with space above his head, his waist below the bottom edge of the frame, both his hands folded inside his wide sleeves in front of his belly below the frame, holding nothing,"],
   ["thrown: eyes widening, brows jerking up, his lips pressed together, no smile; he says nothing in this shot;",
    "thrown: eyes widening, brows jerking up, his lips pressed tightly shut, his mouth closed and still, no smile, no grin; he says nothing in this shot: his lips stay pressed shut from the first frame to the last, no talking, no mouthing words;"],
   [NOSHARP + "; exactly two people in the frame, nobody else.",
    "on him " + NOARMS + "; behind him only the dark earth wall of the farmhouse, soft and out of focus, and the warm light of torches held off screen; no other person, no poles, no spears, no racks and no weapons anywhere; exactly two people in the frame, nobody else."],
   ["his eyes going wide; his lips stay pressed together;",
    "his eyes going wide; his lips stay pressed shut and he never opens his mouth;"],
   LINES, BEADS],
  "drop_pictures": D1SPEC["s14"]["drop_pictures"]},
 "s16": {"replace": [
   ZHAO_ID,
   ["on screen left, framed from the knees up with space above his head,",
    "on screen left, framed from the chest up with space above his head, both men's waists below the bottom edge of the frame,"],
   ["his face in profile toward the constable, never the lens;", "his face in profile toward Zhao Butou, never the lens;"],
   ["on screen right Constable Zhao, in his black futou cap and plain black round-collared constable's robe, a plain black cloth sash at his waist with nothing hanging from it, one burning torch in his right hand, his face three-quarter to screen left toward the magistrate, uneasy, lips closed; " + NOSHARP + ".",
    "on screen right Zhao Butou, in his soft black futou cap and plain black round-collared cotton robe, holding one burning torch up beside his shoulder in his right hand, his left arm at his side with the hand open and empty, his face three-quarter to screen left toward the magistrate, uneasy, lips closed; on him " + NOARMS + "; Magistrate Hu holds nothing: his left hand is clenched at his chest and his right hand reaches for Zhao Butou's sleeve; " + BACKDROP + "."],
   ["Magistrate Hu grabs Constable Zhao's left sleeve and hauls him close; Zhao stumbles half a step toward him, his torch swinging; Zhao's lips stay closed;",
    "Magistrate Hu's right hand grabs the upper sleeve of Zhao Butou's left arm and hauls him close; Zhao Butou tips half a step toward him, the torch in his right hand swaying; his lips stay closed;"],
   BEADS]},
 "s18": {"replace": [
   ["insert close-up, the shot opens directly on one open marriage certificate of plain red paper, the sheet blank with no characters and no writing anywhere on it, only one square vermilion seal outline near its lower right corner, the square empty inside with no character and no pattern in it from its very first frame, held open by two hands in faded blue-grey cuffs under old grey cloth sleeves, the other two folded red certificates pinched against the back of the sheet by his left thumb; only the hands, the cuffs and the red paper are in the frame, no face; the torchlight shining through the back of the paper so the red glows.",
    "insert close-up, the shot opens directly on the plain blank back of one opened sheet of red paper from its very first frame, held up by two hands in faded blue-grey cuffs under old grey cloth sleeves, the front of the sheet turned away from the camera toward the yard, so we see only its plain back; " + PAPER + ", no envelope, flat matte paper with nothing on it; the other two folded red papers pinched against the sheet by his left thumb, folded shut; only the hands, the cuffs and the red paper are in the frame, no face; soft warm torchlight falls on the paper from the front, no light coming through it; the background is dark and softly out of focus, no fire bowls and no flames in the frame."],
   ["the two hands smooth the red sheet open and turn it toward us; the empty square seal outline catches the light; nothing is written on the sheet,",
    "the two hands smooth the red sheet open and lift it a little higher, its front always turned away from us, only its plain blank back toward the camera; the paper stays flat matte red with no sparkle, no shine and no specks; nothing is on it,"],
   BEADS]},
}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9111201, 9111202], "shots": S}, ensure_ascii=False, indent=1), encoding="utf-8")
