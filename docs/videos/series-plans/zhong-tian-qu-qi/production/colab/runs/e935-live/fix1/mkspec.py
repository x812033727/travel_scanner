"""e935 fix1: the retakes of ../picks-merged.tsv (merge agent, 2026-11-20). Why, shot by shot, in plan.md.

    python3 -I mkspec.py                       # -> spec.json (5 shots, seeds 9351211/9351212 for every shot)
    python3 -I mkjobs.py <live>/fix1           # -> <live>/fix1/prompts/*.txt, retake.json, colab-jobs.json (10 jobs, 76 s)
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix1/colab-jobs.json

As e934 fix1: the base of every job is the d1 9351101 job and prompt exactly as sent, so ../mkspec.py's d1 edits (PREP.md
section 6: the pool words out of the field shots, Tang Xiaotang's back-shot sentences, the clear-air sentence per shot, the
'only' sentences) are already in it; mkjobs.py asserts each of those d1 edits is in the base before anything is replaced. Each
fix1 replace is asserted to be in that prompt exactly once. Every shot is bought at its d1 length. Seeds 9351211/9351212
(e935 used 93512xx only for the gate picture, 9351201-9351204).

- s01 (B RETAKE; A picked 1102 with a cut, the merge agent looked: in both takes the 'small dark shapes' grew into an animal,
  a bear cub in 1101, a long-eared rabbit in 1102; neither looks back at the window in the first frame; 1102 has the window
  at his right): the shapes become tiny specks smaller than a fingertip; the window is placed at the upper left behind him as
  in the picture; the look back is written as the first frame's result; a tired face by parts + NOSMILE; static camera.
- s17b (A and B): the ducks' first two seconds are written duck by duck (two to the left, two away, two bills down), then the
  one beat: all six snap their heads to the bank at the right and freeze; medium shot so all six stay whole; static camera.
- s23 (A and B): Qian Yuanwai talked and smiled in both takes, the ducks were brown mallards, 1102 has a film camera rig behind
  him (the preamble's 'shot on a cinema camera' drawn as an object): the preamble phrase becomes 'with the look of a feature
  film' for this shot; 'shrewd' and 'smug' go; a slack sour face + NOSMILE; the nospeak sentence gains 'his jaw still' and a
  silent-for-him clause; three white ducks with orange bills on the water at the left; Tang's hair wound into the two buns;
  static camera.
- s30 (A and B picked 1102 with a plaque of two text-like marks behind him that moves with the push, so a fixed blur box will
  not hold): 'by the gate' goes from both places (the gate brought its plaque); the sky crop is written as the colour of the
  background only; behind him only the sky over the hills and the willow at the left; static camera. 1102 stays the fallback.
- s34 (A and B): the gate opened in both takes and the women walked ahead: the shut gate is written as the result first, the
  two gatemen stand still at the ends of the crossbar, torchlight only through the gaps between the logs, Tang behind his
  right shoulder and A-ling behind his left; static camera (the push went through the gate line).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e935-dh/runpod/live/d1")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = [9351211, 9351212]
DUR = {"s01": 8, "s17b": 6, "s23": 8, "s30": 10, "s34": 6}  # the d1 lengths
STATIC = "The camera holds a static shot."
PUSH = "The camera pushes in with small amplitude at slow speed."


def d1text(sid):
    return (D1 / "prompts" / f"ref-{sid}-9351101.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert d1text(sid).count(s) == 1, (sid, s[:70])
    return s


S = {sid: {"duration_seconds": DUR[sid], "replace": []} for sid in DUR}

S["s01"]["replace"] = [
    [once("s01", "its one small flame soft and out of focus in the right foreground: sitting on a low round stool at the left "
                 "side of the table,"),
     "its one small flame soft and out of focus in the right foreground, the small window high in the back wall at the upper "
     "left of the frame behind him as in <Picture 3>: sitting on a low round stool at the left side of the table,"],
    [once("s01", "his face already turned over his left shoulder toward the small window in the back wall from the first frame, "
                 "never the lens;"),
     "in the first frame his head is already turned back over his left shoulder toward the small window behind him at the "
     "upper left, the back of his head and the side of his face toward us, his eyes on the window, never the lens;"],
    [once("s01", "behind him the small window, dark blue with night, small dark shapes thumping against its wooden frame one "
                 "after another;"),
     "behind him at the upper left the small window, only the dark blue night beyond it, a few tiny dark specks darting past "
     "its wooden frame, each speck smaller than a fingertip;"],
    [once("s01", "tense and tired, not smiling: brows drawn, lips pressed shut;"),
     f"tense and tired: brows drawn, eyes heavy, lips pressed together in one flat line, {NOSMILE};"],
    [once("s01", "One small dark shape thumps against the window frame behind him, and Xu Yan turns his eyes from the window "
                 "back to the empty air before him and his fingers tighten on the tabletop;"),
     "A tiny dark speck darts against the window frame behind him; Xu Yan turns his head slowly from the window back to the "
     "front, his eyes coming to rest on the empty air above the table at the right, and his fingers tighten on the tabletop;"],
    [once("s01", PUSH), STATIC],
]

S["s17b"]["replace"] = [
    [once("s17b", "close-up low over the water: six white farm ducks with orange bills and orange feet on the still shallow "
                  "water of the paddy among sparse young green rice seedlings, already facing every which way from the first "
                  "frame;"),
     "medium shot low over the water: six white farm ducks with orange bills and orange feet scattered on the still shallow "
     "water of the paddy among sparse young green rice seedlings, all six whole in the frame; for the first two seconds the six "
     "ducks face different ways: two toward the left edge of the frame, two turned away from the camera, two with their bills "
     "down in the water;"],
    [once("s17b", "At the same moment all six ducks turn their heads the same way, toward the bank at the right, and hold "
                  "still,"),
     "Then, in the same instant, all six ducks snap their heads up and turn them sharply toward the bank at the right edge of "
     "the frame, necks stretched, and freeze that way to the last frame,"],
    [once("s17b", PUSH), STATIC],
]

S["s23"]["replace"] = [
    [once("s23", "shot on a cinema camera."), "with the look of a feature film."],
    [once("s23", "small shrewd eyes,"), "small narrow eyes under heavy brows,"],
    [once("s23", "combed smooth and gathered up into just two round buns set high on her head,"),
     "combed smooth and gathered up into just two round buns set high on her head, every strand wound up inside the two buns,"],
    [once("s23", "his lips pressed shut, never the lens; his smug look draining away, not smiling;"),
     "his lips pressed together in one flat line, never the lens; his face slowly going slack and sour: the corners of his "
     f"mouth pulled down, his cheeks slack and heavy, {NOSMILE};"],
    [once("s23", "behind them, soft, the trunk of the big old tree and the misty water of the paddy in the soft grey-gold dawn "
                 "light;"),
     "behind them, soft, only the trunk of the big old tree and the misty water of the paddy in the soft grey-gold dawn light; "
     "on the water at the left, three white farm ducks with white feathers and orange bills;"],
    [once("s23", "Qian Yuanwai says nothing in this shot: his lips stay pressed together from the first frame to the last, no "
                 "talking, no mouthing words;"),
     "Qian Yuanwai says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, "
     "no talking, no mouthing words; this is a silent shot for him, only his eyes moving from her hand to the water;"],
    [once("s23", PUSH), STATIC],
]

S["s30"]["replace"] = [
    [once("s30", "the location shown in <Picture 3> is the set, keeping its layout and props."),
     "the evening sky shown in <Picture 3> gives only the colour of the background."],
    [once("s30", "five days after the swarm night, by the gate;"), "five days after the swarm night, under the wide evening sky;"],
    [once("s30", "standing by the gate, framed"), "standing out under the wide sky, framed"],
    [once("s30", "behind him, soft, only the orange-red evening sky over the far hills;"),
     "behind him, soft, only the orange-red evening sky above the dark line of the far hills and the dark trailing branches "
     "of one willow at the left edge of the frame, clear sky all around his head and shoulders;"],
    [once("s30", "moved and heavy, not smiling: eyes wet, brows drawn, lips pressed shut;"),
     f"moved and heavy: eyes wet, brows drawn, lips pressed together in one flat line, {NOSMILE};"],
    [once("s30", PUSH), STATIC],
]

S["s34"]["replace"] = [
    [once("s34", "wide shot from behind at standing eye height toward the gate, like the picture:"),
     "wide shot from behind at standing eye height toward the shut gate, like the picture: the two round-log gate leaves stay "
     "shut from the first frame to the last, the waist-high crossbar lying across both leaves in its iron brackets;"],
    [once("s34", "already walking toward the gate's thick crossbar from the first frame;"),
     "already walking toward the gate's thick crossbar from the first frame, and he stops one step before it, the gate still "
     "shut;"],
    [once("s34", "one step behind him on his right one young woman seen only from behind,"),
     "one step behind him at his right shoulder, at the right edge of the trio, one young woman seen only from behind,"],
    [once("s34", "half a step behind him A-ling,"), "half a step behind him at his left shoulder A-ling,"],
    [once("s34", "already stepping aside one to each end of the crossbar,"), "standing still one at each end of the crossbar,"],
    [once("s34", "beyond the gate's logs the orange light of torches wavering;"),
     "orange torchlight wavering through the narrow gaps between the gate's logs;"],
    [once("s34", "Xu Yan walks step by step up to the crossbar and stops before it, the two women following behind him;"),
     "By the end of the shot Xu Yan stands one step before the crossbar of the shut gate, the young woman with the buns behind "
     "his right shoulder and A-ling behind his left shoulder, both still behind him; he walks step by step up to it and stops, "
     "the two women following behind him;"],
    [once("s34", "grave, not smiling, their lips closed,"), f"grave, {NOSMILE}, their lips closed,"],
    [once("s34", PUSH), STATIC],
]

spec = {"base": "d1 9351101 prompt and job of each shot", "seeds": SEEDS, "shots": S}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({sum(DUR.values()) * len(SEEDS)} s)")
