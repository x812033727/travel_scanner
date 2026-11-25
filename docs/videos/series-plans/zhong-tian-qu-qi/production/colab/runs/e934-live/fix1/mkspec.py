"""e934 fix1: the retakes of ../picks-merged.tsv (merge agent, 2026-11-19). NOT RUN: written and checked (mkjobs.py,
preflight-prompts.py, check_manifest.py, h3r.sh check), nothing is sent. Why, shot by shot, in plan.md.

    bash hui_kong.sh <refs-live>/set-hantian-hui-l1.png <refs-live>/set-hantian-hui-kong-l1.png   # free, s37's sky
    python3 -I mkspec.py                       # -> spec.json (4 shots, seeds 9341211/9341212 for every shot)
    python3 -I mkjobs.py <live>/fix1           # -> <live>/fix1/prompts/*.txt, retake.json, colab-jobs.json (8 jobs, 64 s)
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix1/colab-jobs.json

The base of every job is the d1 9341101 job and prompt exactly as sent, so e934-live/mkspec.py's d1 edits are already in it
(PREP.md section 6: POOLMARK out of every field shot, the clear-air and shoes sentences per shot, the staff out of Elder Han's
s28 sentence, the GAZE_REFINE direction sentences); mkjobs.py asserts each of those d1 edits is in the base before anything
is replaced, and that no pool word is in a field shot. Each fix1 replace is asserted to be in that prompt exactly once. Every
shot is bought at its d1 length. Seeds 9341211/9341212 (nothing else of e934 uses 93412xx).

The rules followed (route-a.md, the task file's lessons, e933 fix1/fix2): positive descriptions, no negated object noun; a face
that must not smile is a concrete hard or grieving face part by part plus the season's NOSMILE sentence, and the words in the
identity sentences that make a face smile go ("kind face", "warm but firm eyes", "shrewd"); a mouth that must stay shut gets
no action sentence that opens it (s09: "lets out one long breath" goes, the action is written the way s08's is, whose two
takes kept the mouth shut); head counts as numbers; where someone looks is a named target in the frame (the upper right
corner, the field beyond the lower left edge), never only "not the lens"; the action's result is written first, then its path.

- s09 (A RETAKE; B picked 1102 but asked for a retake if the mouth reads; the merge agent zoomed the mouth every 0.25 s: 1102
  parts its lips at 4.0-5.0 s and talks from 6.0 s, readable): the breath goes; he shuts his eyes a moment, then turns his
  face toward the boulder and the corners of his mouth press down (s08's wording); a grieving-tired face by parts + NOSMILE;
  static camera (the slow push in 10 s took both takes to a half-face close-up by 6 s).
- s28 (A and B): Elder Han smiled through 「給您磕個頭」 in both takes and never bowed. The identity loses "kind face" and
  "warm but firm eyes" (e933 fix1 s36, picked); a grief face by parts, the corners of the mouth down on every word, NOSMILE,
  "brows lifted" gone; framed from the knees up with grass in front of him so the bow stays in the frame; the bow written as
  its result first (by the last word bent forward from the waist, hands slid forward onto the grass, head lowered); the
  speaking gaze no longer holds his face "lifted"; static camera.
- s32 (A and B): Qian Yuanwai faced the lens and grinned in both takes and walked only after the line. "small shrewd eyes"
  goes from the identity; from the first frame he is walking away to the right with his back three-quarter to the camera and
  his head turned back over his right shoulder, his eyes down to the lower left toward the field; "gritted teeth" (drawn as a
  grin in e933) becomes a sour face by parts + NOSMILE; the sleeve shake in the first second; the result (by the last word he
  is in the right third of the frame, still looking back) first; static camera.
- s37 (B RETAKE, A accepted 1101; the merge agent looked: both takes stand her on the field with the horizon at her waist, the
  pinwheel held up, the hand toward the left or the lens, while s34 and s39 have her on Xu Yan's shoulders and the north is at
  the right in s38/s40): the field picture set-hantian-hui-tian-l1 is swapped for the sky-only crop set-hantian-hui-kong-l1
  (hui_kong.sh, free), written as the colour of the sky only; the place sentence puts her high over the fields seen from far
  below with the grey sky filling the frame to its bottom edge; the pinwheel is lowered out of the frame in her left hand (the
  d1 "lowered ... its vanes still" was drawn held up); her right arm's result is written first: stretched out straight toward
  the upper right corner of the frame, her eyes on that corner; NOSMILE.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/runpod/live/d1")
REFS = "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live/"
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = [9341211, 9341212]
DUR = {"s09": 10, "s28": 8, "s32": 8, "s37": 6}  # the d1 lengths
STATIC = "The camera holds a static shot."
PUSH = "The camera pushes in with small amplitude at slow speed."


def d1text(sid):
    return (D1 / "prompts" / f"ref-{sid}-9341101.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert d1text(sid).count(s) == 1, (sid, s[:70])
    return s


S = {sid: {"duration_seconds": DUR[sid], "replace": []} for sid in DUR}

# s09: no breath; s08's way of writing a shut mouth; static.
S["s09"]["replace"] = [
    [once("s09", "resigned, not smiling: brows level, lips pressed shut;"),
     f"resigned and worn: brows level, eyes heavy, jaw still, lips pressed together in one flat line, {NOSMILE};"],
    [once("s09", "Xu Yan lets out one long breath and turns his face toward the big grey boulder beyond the right edge of the "
                 "frame;"),
     "Xu Yan shuts his eyes for a moment, then turns his face slowly toward the big grey boulder beyond the right edge of the "
     "frame and the corners of his mouth press down;"],
    [once("s09", PUSH), STATIC],
]

# s28: a grieving face, the bow as its result, framed so the bow stays in; static.
HAN_ID = "a deeply lined kind face, a long white beard down to his chest, white hair in a neat small topknot, warm but firm eyes,"
HAN_ID_NEW = "a deeply lined face, a long white beard down to his chest, white hair in a neat small topknot, grave steady eyes,"
S["s28"]["replace"] = [
    [once("s28", HAN_ID), HAN_ID_NEW],
    [once("s28", "medium close-up of Elder Han,"), "medium shot of Elder Han,"],
    [once("s28", "kneeling on the grassy ridge, framed from the waist up,"),
     "kneeling on the grassy ridge, framed from his knees up with a stretch of grass in front of him at the right for the "
     "bow,"],
    [once("s28", "grave and heavy, not smiling: eyes wet, brows lifted, lips moving slowly and heavily between words;"),
     "grief-stricken and heavy: eyes wet and red, brows drawn up together in the middle, the corners of his mouth turned "
     f"down, his chin trembling under the white beard, his lips staying turned down on every word, {NOSMILE};"],
    [once("s28", "his face lifted three-quarter to screen right toward someone out of sight beyond the upper right edge of the "
                 "frame, his eyes on that spot, never looking at the camera;"),
     "his face three-quarter to screen right, his eyes on the spot beyond the upper right edge of the frame as he starts to "
     "bow, never looking at the camera;"],
    [once("s28", "Elder Han bends slowly forward from the waist toward the ground to bow as he speaks,"),
     "By the last word Elder Han has bowed low: his body bent forward from the waist, his two hands slid forward off his "
     "knees onto the grass in front of him, his head lowered toward the ground, all of him still in the frame; he starts to "
     "bend forward slowly with the first words and keeps going down as he speaks,"],
    [once("s28", PUSH), STATIC],
]

# s32: walking away from the first frame, looking back over his right shoulder at the field; a sour face; static.
S["s32"]["replace"] = [
    [once("s32", "small shrewd eyes,"), "small narrow eyes under heavy brows,"],
    [once("s32", "already turning away to the right from the first frame, his face looking back over his right shoulder toward "
                 "the field beyond the lower left edge of the frame, never the lens;"),
     "already walking away toward the right edge of the frame from the first frame, his back three-quarter to the camera, "
     "his head turned back over his right shoulder, his face in profile looking back down toward the field beyond the lower "
     "left edge of the frame, never the lens;"],
    [once("s32", "sour and dark, not smiling: his face fallen, jaw clenched, lips moving through gritted teeth between words;"),
     "sour and dark: his face fallen, brows pulled down hard, the corners of his mouth pulled down, jaw clenched, lips tight "
     f"and moving hard between words, {NOSMILE};"],
    [once("s32", "his face looking back over his right shoulder toward the field beyond the lower left edge of the frame, his "
                 "eyes on it, never looking at the camera;"),
     "his head turned back over his right shoulder, his eyes on the field beyond the lower left edge of the frame, looking "
     "back down to the lower left, never looking at the camera;"],
    [once("s32", "Qian Yuanwai gives his sleeve one sharp shake, walks away toward the right edge of the frame and throws the "
                 "words back over his shoulder as he goes,"),
     "By the last word Qian Yuanwai has walked on into the right third of the frame, his back still three-quarter to the "
     "camera and his head still turned back over his right shoulder: in the first second he gives his right sleeve one sharp "
     "shake behind him, then he keeps walking slowly and steadily toward the right edge and throws the words back over his "
     "shoulder as he goes,"],
    [once("s32", PUSH), STATIC],
]

# s37: the sky only; high over the fields; the pinwheel lowered out of the frame; the right arm to the upper right corner.
S["s37"]["swap_pictures"] = {"set-hantian-hui-tian-l1.png": REFS + "set-hantian-hui-kong-l1.png"}
S["s37"]["replace"] = [
    [once("s37", "the location shown in <Picture 2> is the set, keeping its layout and props."),
     "the darkening grey sky shown in <Picture 2> gives only the colour of the background."],
    [once("s37", "On the three small dry fields of Liuxi as the sunset dies on the tenth day of the drought, on the low grassy "
                 "ridge at the edge of the dry cracked furrows;"),
     "High over the three small dry fields of Liuxi as the sunset dies on the tenth day of the drought, seen from far below "
     "against the wide sky;"],
    [once("s37", "seen from below, high against the sky, framed from the chest up with space above her head,"),
     "seen from far below, sitting up high, framed from the chest up with space above her head, the darkening grey sky "
     "filling the whole frame behind her from the top edge to the bottom edge,"],
    [once("s37", "a little pinwheel of four plain white paper vanes on a thin bamboo stick already lowered in her left hand from "
                 "the first frame, its vanes still,"),
     "her left arm down at her side from the first frame, her left hand below the bottom edge of the frame holding the little "
     "paper pinwheel down there, out of sight,"],
    [once("s37", "her face lifted three-quarter to screen right toward the far hills beyond the upper right edge of the frame, "
                 "her eyes on them, never the lens;"),
     "her face lifted three-quarter to screen right toward the upper right corner of the frame, her eyes on the upper right "
     "corner of the frame, never the lens;"],
    [once("s37", "frightened, not smiling: eyes wide, lips moving uncertainly between words;"),
     f"frightened: eyes wide and fixed on the upper right corner, brows drawn up, lips moving uncertainly between words, "
     f"{NOSMILE};"],
    [once("s37", "her face lifted three-quarter to screen right toward the far hills beyond the upper right edge of the frame, "
                 "her eyes on them, never looking at the camera;"),
     "her face lifted three-quarter to screen right toward the upper right corner of the frame, her eyes on that corner, "
     "never looking at the camera;"],
    [once("s37", "Little Xiaohe stretches her flat right hand out toward the far hills at the upper right as she speaks,"),
     "By the middle of the line Little Xiaohe's right arm is stretched out straight toward the upper right corner of the "
     "frame, her flat right hand reaching past that corner: she lifts it up and out to the upper right as she speaks,"],
]

spec = {"base": "d1 9341101 prompt and job of each shot", "seeds": SEEDS, "shots": S}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({sum(DUR.values()) * len(SEEDS)} s)")
