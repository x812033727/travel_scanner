"""e911 fix2: s21 again (Magistrate Hu, picked 9111101). He grins from 4.25 s, but his line a18 is 5.04 s and the shot must
hold about 5.3 s, so the cut would freeze 0.87 s. Same action (half a step back, right hand clutching the left sleeve,
stammering the line); the face written hard: no smile and no grin at any moment to the last frame, mouth a flat line between
words, cold eyes. Plus the fix1 lessons: framed from the chest up with the waist below the frame edge, both hands written,
no weapon racks, poles or spears anywhere behind him, no hanging beads. Same steps as fix1 (retake.py from st1, 8 s).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
BEADS = ["no strings of beads and no glitch effects anywhere.",
         "no strings of beads, no hanging beads, no bead curtains, no strings of red beads and no glitch effects anywhere."]
S = {
 "s21": {"replace": [
   ["framed from the chest up with space above his head,",
    "framed from the chest up with space above his head, his waist below the bottom edge of the frame,"],
   ["panicking: eyes round, brows shooting up, mouth stammering between words, no smile;",
    "cornered but hard: cold, narrowed eyes, brows drawn down, his mouth a flat tight line between words, the corners of his mouth turned down, no smile and no grin; his right hand clutches his bulging left sleeve in front of his chest, his left hand inside that wide sleeve, nothing else in his hands;"],
   ["no torch on a stand, in the ground or on a wall, no brazier.",
    "no torch on a stand, in the ground or on a wall, no brazier, no weapon racks, no poles, no spears and no weapons anywhere; on him no spear, no sword, no scabbard, no blade of any kind."],
   ["no smile at any moment, not even at the end of the shot, until the last frame,",
    "between the words his mouth closes back into the same flat hard line; no smile and no grin at any moment, his lips never curling up, his cheeks never lifting, his teeth never bared in a grin, not even after the line ends, until the last frame,"],
   BEADS]},
}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9111301, 9111302], "shots": S}, ensure_ascii=False, indent=1), encoding="utf-8")
