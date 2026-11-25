"""e935 fix3 (REVIEW 3 retakes, 2026-11-20): s32 s24 s25 s01 s30, two seeds each. Why, shot by shot, in plan.md.

    python3 -I mkspec.py                       # -> spec.json (5 shots, 10 jobs, 76 s)
    python3 -I mkjobs.py <live>/fix3           # -> <live>/fix3/prompts/*.txt, retake.json, colab-jobs.json

The base of every job is the take now in the cut, job and prompt exactly as sent (sha256 checked in mkjobs.py):
s32 d1 9351101, s24 d1 9351101, s25 d1 9351102, s01 fix1 9351211, s30 fix1 9351212. Seeds 935123x (e935refine.sh's SRC
table maps '123' to fix3), so ten jobs at most.

- s32 (review 2 SEVERE 1): the gate was wide open behind Xu Yan in both d1 takes; the d1 text never said the leaves are shut.
  The bible prop sentence goes in as the result from the first frame (two closed leaves of upright logs, a thin bright seam,
  the waist-high crossbar held across the seam by plain iron brackets), 'beyond the gate' goes, torchlight only through the
  gaps between the logs; the two gatemen stand still in front of the shut gate; Xu Yan's face by parts + NOSMILE.
- s24 (review 1 medium 3, review 2 medium 2 and 4): Qian Yuanwai laughed through the line. e934 fix3 s30 (the one take of
  him that did not smile): the face by parts in both the composition and the speaking sentence, small talking mouth shapes,
  'gritted teeth' out (it draws teeth), 'shrewd' out, angle-a dropped (fix4 of e934), the preamble's cinema camera out.
  Background: the field set crop of the dry furrows and the big tree only (fix3/set-hantian-yang-chen2-liu-gan.png, free),
  and the text says dry cracked earth behind him.
- s25 (review 1 slight 1, review 2 slight 3 and medium 4): A-ling smiled through the line; the cold face by parts (e934 fix3
  s15/s17), the one lift of the mouth only after her last word; the same dry crop and dry-earth sentence.
- s01, s30 (both reviews' motion item; the model pushed in neither): a real trajectory with an anticipation and a settle
  (motion-quality.md section two) and one camera move with its start and end framing, from a wider first framing so the push
  is visible. s01 also shows the old grey outer coat (he pulls it tighter; review 1 slight 14).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
LIVE = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e935-dh/runpod/live")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
BASE = {"s32": ("d1", 9351101), "s24": ("d1", 9351101), "s25": ("d1", 9351102), "s01": ("fix1", 9351211),
        "s30": ("fix1", 9351212)}
SEEDS = {"s32": [9351231, 9351232], "s24": [9351233, 9351234], "s25": [9351235, 9351236], "s01": [9351237, 9351238],
         "s30": [9351239, 9351230]}
DUR = {"s32": 6, "s24": 8, "s25": 6, "s01": 8, "s30": 10}  # the lengths bought before
CROP = "docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e935-live/fix3/set-hantian-yang-chen2-liu-gan.png"
CAM = ["shot on a cinema camera.", "with the look of a feature film."]
DRY = "beyond them only dry cracked brown earth in bare furrows under a thin low mist"


def basetext(sid):
    src, seed = BASE[sid]
    return (LIVE / src / "prompts" / f"ref-{sid}-{seed}.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert basetext(sid).count(s) == 1, (sid, s[:70])
    return s


ALING_FACE = ("her face cold and still: brows level and unmoving, eyes cool and half-lidded, the corners of her mouth flat "
              "and level, her cheeks still")
QIAN_FACE = ("the cheer already gone from his face in the first frame, sour and sulking: the corners of his mouth dragged down "
             "hard, his lower lip pushed out, his jaw tight, his eyes narrowed under the heavy brows, his cheeks heavy and flat")
S = {sid: {"base": f"{BASE[sid][0]} {sid}-{BASE[sid][1]}", "seeds": SEEDS[sid], "duration_seconds": DUR[sid],
           "replace": [], "pictures": None} for sid in BASE}

S["s32"]["replace"] = [
    [once("s32", CAM[0]), CAM[1]],
    [once("s32", "five days after the swarm night, by the gate;"), "five days after the swarm night, inside the shut gate;"],
    [once("s32", "his lips pressed shut, never the lens; grave, not smiling;"),
     f"his lips pressed shut, never the lens; grave: brows drawn, lips pressed together in one flat line, {NOSMILE};"],
    [once("s32", "beyond them, soft, at the gate, two men in Song-dynasty cross-collared homespun short jackets, cloth head "
                 "wraps and cloth shoes, a broad young man in a dark teal jacket and a wiry middle-aged man in a deep wine-red "
                 "jacket, standing one at each end of its thick crossbar,"),
     "beyond them, filling the whole background, the shut village gate as in <Picture 3>: two closed gate leaves of upright "
     "logs pressed together, a thin bright seam between them, the lower crossbar at waist height held across the seam by "
     "plain iron brackets, both leaves shut from the first frame to the last; in front of the shut gate, soft, two men in "
     "Song-dynasty cross-collared homespun short jackets, cloth head wraps and cloth shoes, a broad young man in a dark teal "
     "jacket and a wiry middle-aged man in a deep wine-red jacket, standing still one at each end of its thick crossbar,"],
    [once("s32", "the orange light of torches wavering beyond the gate;"),
     "orange torchlight wavering only through the narrow gaps between the gate's logs;"],
    [once("s32", "Her left hand grips the sleeve tighter and gives it one small shake, only her arm moving;"),
     "Her left hand grips the sleeve tighter and tugs it once toward her in one small firm shake, only her arm moving; Xu "
     "Yan's shoulder gives a little with the tug and settles, his face still turned toward the shut gate, both gate leaves "
     "staying shut and the crossbar staying in its brackets to the last frame;"],
]

S["s24"]["pictures"] = ["qianyuanwai-portrait-l1.png", CROP]  # angle-a dropped; the set is the dry crop
S["s24"]["replace"] = [
    [once("s24", "For the target video, <Picture 1>, <Picture 2> and <Picture 3> are referenced throughout."),
     "For the target video, <Picture 1> and <Picture 2> are referenced throughout."],
    [once("s24", CAM[0]), CAM[1]],
    [once("s24", "Qian Yuanwai shown in <Picture 1> and <Picture 2> (the same man from several angles) keeps"),
     "Qian Yuanwai shown in <Picture 1> keeps"],
    [once("s24", "small shrewd eyes,"), "small narrow eyes under heavy brows,"],
    [once("s24", "the location shown in <Picture 3> is the set, keeping its layout and props."),
     "the dry fields and the big old tree shown in <Picture 2> are the set, keeping their layout."],
    [once("s24", "on the grassy bank under the big old tree at the edge of the paddy;"),
     "on the grassy bank under the big old tree, the dry cracked fields of the drought spreading behind it;"],
    [once("s24", "sour and dark, not smiling: his face fallen, jaw clenched, lips moving through gritted teeth between words;"),
     f"{QIAN_FACE}, {NOSMILE};"],
    [once("s24", "behind him, soft, the trunk of the big old tree and the misty grassy bank in the soft grey-gold dawn light;"),
     f"behind him, soft, the trunk of the big old tree and {DRY}, in the soft grey-gold dawn light;"],
    [once("s24", "his lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes, his face looking "
                 "back over his right shoulder"),
     "his lips tight and moving hard with every syllable in small talking mouth shapes, the corners of his mouth dragged down "
     f"and his lower lip pushed out the whole time, {NOSMILE}, his face looking back over his right shoulder"],
    [once("s24", "Qian Yuanwai gives his sleeve one sharp shake, walks away toward the right edge of the frame and throws the "
                 "words back over his shoulder as he goes,"),
     "Qian Yuanwai shifts his weight onto his back foot, gives his right sleeve one sharp downward shake that snaps the silk, "
     "and walks off toward the right edge of the frame with heavy steps, throwing the words back over his shoulder as he "
     "goes, his face just as sour,"],
]

S["s25"]["pictures"] = ["aling-portrait-l1.png", "aling-angle-a-l1.png", CROP]
S["s25"]["replace"] = [
    [once("s25", CAM[0]), CAM[1]],
    [once("s25", "on the raised grassy bank at the edge of the flooded paddy;"),
     "on the raised grassy bank at the edge of the paddy, the dry cracked fields of the drought spreading behind her;"],
    [once("s25", "quiet and light, not smiling until the very end: brows level, lips moving softly between words;"),
     f"{ALING_FACE}, her lips moving only a little between words, the corners of her mouth level until after her last word;"],
    [once("s25", "behind her, soft, the grassy bank, the trunk of the big old tree and the misty water in the soft grey-gold "
                 "dawn light;"),
     f"behind her, soft, the grassy bank, the trunk of the big old tree and {DRY}, in the soft grey-gold dawn light;"],
    [once("s25", "her lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes, her face "
                 "three-quarter to screen left"),
     f"her lips moving evenly with every syllable in small natural talking mouth shapes, {ALING_FACE} the whole time she "
     "speaks, her face three-quarter to screen left"],
    [once("s25", "A-ling tips the long pole out toward the left as she speaks, and at the very end one corner of her mouth lifts "
                 "a little,"),
     "A-ling shifts her weight and swings the long pole out toward the left in one smooth weighted sweep as she speaks, its "
     "tip pointing on down the paddy, and only after her last word, in the final second of the shot, one corner of her mouth "
     "lifts a little,"],
]

S["s01"]["replace"] = [
    [once("s01", CAM[0]), CAM[1]],
    [once("s01", "medium shot across the small dark square table,"), "medium wide shot across the small dark square table,"],
    [once("s01", "A tiny dark speck darts against the window frame behind him; Xu Yan turns his head slowly from the window "
                 "back to the front, his eyes coming to rest on the empty air above the table at the right, and his fingers "
                 "tighten on the tabletop;"),
     "A tiny dark speck darts against the window frame behind him and his shoulders flinch once; Xu Yan draws a breath, "
     "turns his head from the window back to the front at a steady pace, reaches up with his right hand and pulls the old "
     "grey outer coat tighter across his shoulders, the cloth dragging and folding under his fingers, then leans his weight "
     "forward onto both forearms on the tabletop, his eyes settling on the empty air above the table at the right; the small "
     "flame on the table wavers and his shadow sways on the wall behind him;"],
    [once("s01", "The camera holds a static shot."),
     "The camera pushes in with large amplitude at slow speed, from a medium wide shot to a medium shot."],
]

S["s30"]["replace"] = [
    [once("s30", CAM[0]), CAM[1]],
    [once("s30", "close-up of Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, standing out under the wide "
                 "sky, framed from the chest up with space above his head,"),
     "medium shot of Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, standing out under the wide sky, "
     "framed from the waist up with space above his head,"],
    [once("s30", "Xu Yan's eyes move slowly from the kneeling people to the woman with the child, and his throat moves once as "
                 "he swallows;"),
     "A light evening wind lifts the loose strands on his forehead and stirs his sleeves; Xu Yan draws one slow deep breath, "
     "his chest and shoulders rising and settling; his eyes travel slowly from the kneeling people at the lower left to the "
     "woman with the child, his throat moves once as he swallows, and his right hand closes slowly into a fist at his side; "
     "the torchlight wavers across one side of his face;"],
    [once("s30", "The camera holds a static shot."),
     "The camera pushes in with large amplitude at slow speed, from a medium shot to a close-up."],
]

spec = {"base": "the take now in the cut, job and prompt as sent: " + ", ".join(f"{k} {v[0]} {v[1]}" for k, v in BASE.items()),
        "shots": S}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({sum(DUR[k] * len(v['seeds']) for k, v in S.items())} s)")
