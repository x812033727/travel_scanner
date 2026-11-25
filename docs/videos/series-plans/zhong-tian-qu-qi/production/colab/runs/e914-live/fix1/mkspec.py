"""e914 fix1: the retakes of picks-merged.tsv (s24, s30, s32), merged from review-picks-a/b. Same steps as e913 fix1:
retake.py from live/st1 (the d1 edits of e914-live/spec.json are applied first: s24 loses Tang Xiaotang's identity
sentence and her three face pictures, s30's speaking gaze is replaced), mkjobs.py for the duration and output_path,
preflight-prompts.py. Seeds 9141201/9141202. The prompts were already written under bible 拍法 18 (r2.py: no negative
nouns, the clean-air extras sentence), so only the sentences that failed are rewritten here.

Why each shot (both reviews; s32 was RETAKE for picks-b only, the coordinator's frame check agreed):
- s24 (both): Tang Xiaotang turns her head toward Xu Yan from about 2-3.6 s in all four takes (cheek, eye, ear-ring and
  nose line), the open account book grows lines of fake writing on both pages, Xu Yan closes the book instead of her,
  and the push-in drifts her out of frame after 5 s. Her line (a25, 6.52 s) needs almost the whole 8 s.
  Rewrite: she is held by her own work from the first frame to the last (head bowed over the abacus, right hand flicking
  beads in a steady rhythm), so nothing in the shot gives her a reason to look at him: Xu Yan no longer points or taps,
  he sits still with his hands on his knees and watches her hands. Every book is closed, only plain blue cloth covers;
  the one she finishes lies shut by her right hand and she slides it onto the stack without lifting her head. The
  camera holds a static shot (the push-in carried her out of frame). Bought at 8 s (a25 6.52 s).
- s30 (both): no mat in any take: 1101 carries a long bamboo pole on his shoulder, 1102 a thick wooden bar with a cross
  head (like a pick) that he raises like a weapon after 5.75 s. A flat mat on a shoulder is seen edge-on and reads as a
  pole, so the mat is now carried flat across both forearms in front of his chest like a tray (the coordinator's
  wording, picks-a/b both asked for the flat shape), already in his arms at the first frame; "papermaking mould" (a
  noun the model drew as a bar or a frame of beams) is never written, only the mat's shape. The STICKS sentence ("the
  only long things anyone holds are plain wooden tools") invited a long thing into his hands and goes. "teeth gritted
  between words" (a mouth shape with teeth) becomes lips drawn tight and the corners pulled down; after the last word a
  snort and he keeps walking. The speaking gaze is written with "turned toward ... eyes on" the open side (preflight
  gaze warning of d1). Bought at 6 s instead of 8: a31 is 4.44 s, the mat is already up at the first frame, the storyboard
  cuts s30 in the middle of his turn, and Carpenter Shi laughed in all six e913 takes and both e914 s32 takes (bible 拍法
  18: the laugh-prone shots are bought short).
- s32 (picks-b RETAKE, picks-a kept 1101 for now; coordinator's frame check: both takes grin with the teeth through
  the whole line, the face square to the lens, the mould a long beam with a handle over his right shoulder in 1101 and a
  rake-like bar in 1102): RETAKE. The mat is the same flat tray across his forearms at his waist; he has already stopped
  and turned his head back over his right shoulder at the first frame. The script's "corner of the mouth eases" is not
  written as a mouth movement (it became a grin in both takes): his face stays gruff (brows knotted, eyes narrowed, the
  corners of the mouth turned down, lips barely parting), and the giving-in is carried by actions after the last word:
  one huff through the nose, one curt nod, then he lowers the mat and stands it upright in front of him, both hands on
  its top edge (the script's 放下來兩手扶著). Bought at 6 s (a33 4.56 s).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]

MAT = ("a flat rectangular mat of thin split bamboo strips laid close side by side, as wide as his shoulders and as deep as "
       "his forearm is long, edged with a thin plain wooden border, pale straw-coloured all over, one small willow-leaf shape "
       "woven into its middle in the same pale strips")
STICKS = "the only long things anyone holds are plain wooden tools, smooth and round to their ends"
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC = "The camera holds a static shot."


def shot(sid, extra, dur=None):
    s = {k: v for k, v in D1SPEC[sid].items() if k != "replace"}
    s["replace"] = D1SPEC[sid].get("replace", []) + extra
    if dur:
        s["duration_seconds"] = dur
    return s


S = {
 "s24": shot("s24", [
   ["her face turned fully away, seated behind the old wooden table in the right foreground;",
    "her face turned fully away, seated behind the old wooden table in the right foreground, her head bowed forward over "
    "the abacus from the first frame to the last, her eyes down on the beads, the crown of her head and her two buns "
    "toward the lens;"],
   ["on the table one plain wooden abacus with a smooth dark wooden frame and round dark wooden beads, the stack of plain "
    "blue cloth-covered account books on screen right at her right hand, and one open account book lying flat whose pages "
    "are blank;",
    "on the table directly in front of her one plain wooden abacus with a smooth dark wooden frame and round dark wooden "
    "beads; on screen right beside her right hand a neat stack of closed thread-bound account books, their covers plain "
    "unbroken dark blue cloth, and lying shut on the table just beside the abacus one more closed account book with the "
    "same plain dark blue cloth cover facing up; every book on the table is closed, only blue cloth covers showing;"],
   ["his eyes on the book and then on her face just right of the lens, never the lens; mild and honest, lips pressed shut;",
    "his eyes resting on her busy hands at the abacus just right of the lens, never the lens; mild and honest: brows "
    "relaxed and level, eyes calm, lips pressed together, both his hands resting flat on his knees;"],
   [STICKS, "his hands hold nothing and hers touch only the abacus and the books"],
   ["Xu Yan taps one place on the open book; she flicks two beads with her right hand (on screen right), then closes the "
    "book and lays it on top of the stack on screen right;",
    "From the first frame to the last her head stays bowed over the abacus and her right hand (on screen right) keeps "
    "working it, flicking the beads up and down in a steady quick rhythm like someone adding a long column; near the end, "
    "without lifting her head, that hand slides the closed blue book from beside the abacus onto the top of the stack on "
    "screen right and goes straight back to the beads; Xu Yan sits still on his stool and watches her hands;"],
   [PUSH, STATIC]]),
 "s30": shot("s30", [
   ["his face in three-quarter profile toward the open side, eyes ahead",
    "his face turned toward the open side in three-quarter profile, his eyes on the open side ahead of him"],
   ["never the lens; furious: brows slammed down, jaw clenched, eyes hard, teeth gritted between words;",
    "never the lens; at the first frame he already holds " + MAT + ", carried flat across both his forearms in front of "
    "his chest like a tray, the flat side facing up; furious: brows slammed down, jaw clenched, eyes hard, lips drawn "
    "tight between words, the corners of his mouth pulled hard down;"],
   [STICKS, "in his arms only the flat bamboo mat, carried level like a tray"],
   ["Carpenter Shi's face darkens; he heaves the mould up onto his left shoulder, the shoulder away from the camera, in one "
    "swing, turns toward the open side and strides off, saying it over his shoulder with his eyes ahead;",
    "Carpenter Shi's face darkens; holding the bamboo mat flat across both forearms like a tray, he turns toward the open "
    "side on screen right and strides off with long hard steps, saying it with his chin jutting and his eyes ahead;"],
   ["after the last word the lips press flat and the jaw sets, the brows stay drawn, held to the last frame,",
    "after the last word he snorts once hard through his nose, his lips press flat and his jaw sets, and he keeps "
    "striding toward the light without looking back, the mat level across his forearms, the brows drawn to the last frame,"]],
   6),
 "s32": shot("s32", [
   ["at the edge of the open side with the papermaking mould on his left shoulder, the shoulder away from the camera, his "
    "body still facing the open side on screen right, framed from the chest up with space above his head, looking back "
    "over his right shoulder toward the young man off screen left, his face three-quarter to screen left, never the lens; "
    "grudging: a snort, then one corner of his mouth easing a little, his lips closed between words, lips moving between "
    "words;",
    "standing still at the edge of the open side, holding " + MAT + ", flat across both forearms at his waist like a tray, "
    "its near edge just at the bottom of the frame, his body still facing the open side on screen right, framed from the "
    "chest up with space above his head, at the first frame his head already turned back over his right shoulder toward "
    "the young man off screen left, his face three-quarter to screen left, his eyes on screen left past the lens, never "
    "the lens; gruff and grudging: brows still knotted low, eyes narrowed and hard, the corners of his mouth turned down, "
    "lips tight and barely parting on each low word, pressed together between words;"],
   ["Carpenter Shi stops, looks back over his right shoulder and snorts; then he swings the mould down off his left "
    "shoulder and holds it upright in front of him with both hands,",
    "before the line he snorts once through his nose; after the last word he lets out one short huff through his nose and "
    "gives one small curt nod, lips pressed together, then lowers the bamboo mat and stands it upright on the ground in "
    "front of him, both hands resting on its top edge, his eyes staying on screen left and his brows knotted to the last "
    "frame,"]],
   6),
}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9141201, 9141202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
