"""e937 fix1: the retakes of ../picks-merged.tsv (merge + fix1 agent, 2026-11-23). Why, shot by shot, in plan.md.

    python3 -I mkspec.py                       # -> spec.json (10 shots, seeds 9371211/9371212 for every shot)
    python3 -I mkjobs.py <live>/fix1           # -> <live>/fix1/prompts/*.txt, retake.json, colab-jobs.json (20 jobs, 118 s)
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix1/colab-jobs.json

As e936 fix1: the base of every job is the d1 9371101 job and prompt exactly as sent (mkjobs.py checks the sha256 and that
every d1 edit of ../spec.json for the shot is in it). That base already carries what prep937.sh added and retake.py would not:
the append_pictures (the spear prop last, with its sentence after the set clause and the header renumbered: s26 s27 s27b s36),
the pool-word removal, the clear-air sentence and the shoes; the reference_images of the d1 job are sent unchanged. Each fix1
replace is asserted to be in the d1 prompt exactly once. Every shot is bought at its d1 length (= r2.py BUY). Every shot is a
static camera (the push took the foreground shoulder out in s14 s36, the fists out in s16b, the raider out in s26). No prompt
carries 'shot on a cinema camera' (d1 says 'with the look of a feature film').

Must (coordinator, the union of A and B): s14 (+ s36, the same bearded foreground head), s21, s26, s27, s27b.
Added after looking (coordinator listed them to weigh): s37 (grey-white sky behind him, the line in one breath before the
wipe), s10 (the rust-red man squatting from the first frame), s09b (the men go out through the gate), s16b (the fists open
inside the frame).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e937-dh/runpod/live/d1")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = [9371211, 9371212]
DUR = {"s09b": 5, "s10": 6, "s14": 6, "s16b": 6, "s21": 5, "s26": 6, "s27": 5, "s27b": 6, "s36": 6, "s37": 8}  # d1 = BUY
STATIC = "The camera holds a static shot."
PUSH = "The camera pushes in with small amplitude at slow speed."
POWDER = ("his face, his brows and his hair caked thick and grey-white with lime powder, the pale powder plain on his cheeks "
          "and forehead")


def d1text(sid):
    return (D1 / "prompts" / f"ref-{sid}-9371101.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert d1text(sid).count(s) == 1, (sid, s[:70])
    return s


S = {sid: {"duration_seconds": DUR[sid], "replace": []} for sid in DUR}


def back_of_head(side):
    return (f"only the back of one young man's head, his dark hair cropped short at the nape, and his shoulder in an old "
            f"grey cloth outer coat, his face turned away from us toward her, staying at the {side} edge of the frame from "
            f"the first frame to the last;")


S["s14"]["replace"] = [
    [once("s14", "only one shoulder and upper arm of a man in an old grey cloth outer coat, toward us the whole shot;"),
     back_of_head("right")],
    [once("s14", "Besides her, only the shoulder of the man at the right edge of the frame"),
     "Besides her, only the back of the head and the shoulder of the man at the right edge of the frame"],
    [once("s14", "cold, not smiling: eyes narrowed, jaw set, lips moving short and hard between words;"),
     f"cold: eyes narrowed, jaw set, brows level, lips moving short and hard between words, {NOSMILE};"],
    [once("s14", PUSH), STATIC],
]

S["s36"]["replace"] = [
    [once("s36", "only one shoulder and upper arm of a man in an old grey cloth outer coat, toward us the whole shot;"),
     back_of_head("left")],
    [once("s36", "Besides her, only the shoulder of the man at the left edge of the frame"),
     "Besides her, only the back of the head and the shoulder of the man at the left edge of the frame"],
    [once("s36", "a broad smear of pale powder across one cheek,"),
     "a broad smear of grey-white lime powder plain across her cheek and jaw,"],
    [once("s36", "quiet and serious, not smiling: eyes steady, brows level, lips moving softly between words;"),
     f"quiet and serious: eyes steady, brows level, lips moving softly between words, {NOSMILE};"],
    [once("s36", PUSH), STATIC],
]

S["s21"]["replace"] = [
    [once("s21", "across the field, bursts of thick white powdery smoke billow up one after another and swallow the torches; "
                 "six raiders seen only as dark staggering shapes in the smoke, two of them already sunk waist-deep in hidden "
                 "pits from the first frame, the broken straw around their waists, their torches lying on the ground;"),
     "in the middle of the field, from the first frame, two raiders seen only as dark shapes already sunk to the waist in two "
     "shallow pits, the broken straw ringed around their waists, their torches lying on the ground beside them, and four "
     "more dark shapes already stumbling and crouching low just behind them; one wide, low, dense cloud of thick white powdery "
     "smoke already lies over them from the first frame, a heavy white bank rolling outward along the ground, as wide as the "
     "field and twice the height of a man;"],
    [once("s21", "The thick white powdery smoke rolls higher and wider across the field and one torch after another dims and "
                 "goes out inside it,"),
     "The heavy white bank of powdery smoke rolls slowly outward along the ground, thicker and wider, swallowing the dark "
     "shapes, and the torches lying on the ground dim and go out inside it one after another,"],
    [once("s21", PUSH), STATIC],
]

S["s26"]["replace"] = [
    [once("s26", "standing in the front row, framed from the knees up, her face three-quarter to screen left, never the lens; "
                 "cold and fast, not smiling: eyes narrowed, lips pressed shut; at the left, one raider in a ragged undyed "
                 "homespun tunic and a cloth head wrap, seen only from behind, already lunging at her with one long spear: a "
                 "plain wooden shaft taller than a man, a small plain iron spearhead, the shaft bare below the head thrust "
                 "forward in both hands from the first frame, its spearhead still an arm's length short of her in the first "
                 "frame;"),
     "framed from the knees up, already turned side-on to him from the first frame with her right hand gripping the middle of "
     "one long spear: a plain wooden shaft taller than a man, a small plain iron spearhead, the spearhead already past her "
     "hip at the right, well behind her; her face three-quarter to screen left toward him, never the lens; cold and fast: "
     f"eyes narrowed, brows level, lips pressed into one flat line, {NOSMILE}; at the left, one raider in a ragged undyed "
     "homespun tunic and a cloth head wrap, seen only from behind, leaning toward her with both his hands still on the rear "
     "end of the same shaft; one spear in the frame, the two of them holding the one shaft between them; above them only the "
     "clear deep blue night sky full of small stars;"],
    [once("s26", "Qin Shuang twists aside from the spearhead, seizes the shaft in her right hand and wrenches it back, and the "
                 "raider pitches forward onto the earth while the spear comes away in her right hand;"),
     "Qin Shuang yanks the shaft hard back past her hip in one pull, and the raider is jerked off his feet, lets go and falls "
     "forward face down out of the bottom of the frame at the left, and the one spear stays in her right hand to the last "
     "frame;"],
    [once("s26", PUSH), STATIC],
]

S["s27"]["replace"] = [
    [once("s27", "medium shot on the long ridge of dug earth, the whole action inside the frame:"),
     "medium two-shot in profile on the long ridge of dug earth, the camera square to the line between them, the two of them "
     "face to face a long step apart and the whole action inside the frame, the straw heap and the dry channel soft behind "
     "them:"],
    [once("s27", "framed from the waist up, her face three-quarter to screen left toward him, never the lens; cold, not "
                 "smiling, her lips pressed shut;"),
     f"framed from the waist up, in profile facing screen left toward him, her eyes on him, never the lens; cold, her lips "
     f"pressed shut, {NOSMILE};"],
    [once("s27", "a thick coat of white powder over his face,"), POWDER + ","],
    [once("s27", "framed from the waist up, his face three-quarter to screen right toward her, never the lens; savage, not "
                 "smiling, his lips closed;"),
     f"framed from the waist up, in profile facing screen right toward her, his eyes on her, never the lens; savage, his lips "
     f"closed, {NOSMILE};"],
    [once("s27", "Qin Shuang's spearhead whips up under the saber and knocks it out of his hand up out of the top of the frame, "
                 "and his hand is left empty;"),
     "In one quick stroke Qin Shuang's spearhead flicks up under the saber, and the saber flies spinning out of his hand up "
     "out of the top of the frame; his right hand is left empty above his shoulder, the fingers spread, and the two of them stay face to "
     "face, still;"],
    [once("s27", PUSH), STATIC],
]

S["s27b"]["replace"] = [
    [once("s27b", "medium close-up on the long ridge of dug earth:"),
     "medium close-up in profile on the long ridge of dug earth, the camera square to the line between them:"],
    [once("s27b", "its small iron head already resting still a hand's breadth before his throat from the first frame, her face "
                  "three-quarter to screen left toward him, never the lens; calm and cold, not smiling:"),
     "its small iron head already held still in the air a full hand's breadth in front of his throat from the first frame, a "
     "clear gap of dark air between the spearhead and his throat to the last frame, in profile facing screen left toward him, "
     f"never the lens; calm and cold, {NOSMILE}:"],
    [once("s27b", "a thick coat of white powder over his face,"), POWDER + ","],
    [once("s27b", "his face three-quarter to screen right toward her, never the lens; stunned, not smiling, his lips closed;"),
     f"in profile facing screen right toward her, never the lens; stunned, his lips closed, {NOSMILE};"],
    [once("s27b", "Qin Shuang holds the spearhead perfectly still at his throat as she speaks,"),
     "Qin Shuang holds the spearhead perfectly still a hand's breadth from his throat as she speaks,"],
    [once("s27b", PUSH), STATIC],
]

S["s37"]["replace"] = [
    [once("s37", "close-up of Xu Yan,"), "close-up of Xu Yan from slightly below, against the sky,"],
    [once("s37", "behind him, soft, only the pale grey-white sky low over the far pines;"),
     "behind his head and shoulders only the pale grey-white dawn sky, filling the whole background to every edge of the "
     "frame;"],
    [once("s37", "Xu Yan wipes the powder off his cheek with the back of his right hand and gives her a small tired smile as "
                 "he speaks, then his lips close,"),
     "he says the whole line in one breath, his hands still at his sides while he speaks; only after the line ends does he "
     "wipe the powder off his cheek once with the back of his right hand and give her a small tired smile, his lips closed,"],
    [once("s37", PUSH), STATIC],
]

S["s10"]["replace"] = [
    [once("s10", "walking along the top of the long ridge of dug earth, three men"),
     "in the near part of the ridge, closest to us, a lean young man in a rust-red jacket squatting low on his heels from the "
     "first frame to the last, his knees bent high, his sack already resting in a shallow hole in the ridge before him with "
     "its tied neck pointing up, both his hands on it; beyond him, walking along the top of the long ridge of dug earth, three "
     "men"],
    [once("s10", "; in the near part of the ridge, a lean young man in a rust-red jacket already crouching low on his heels "
                 "from the first frame over a shallow hole with his sack in both hands;"), ";"],
    [once("s10", "the crouching man sets his sack down into the shallow hole with its tied neck pointing up, and Xu Yan points "
                 "his flat right hand down at the next spot three steps on as he speaks,"),
     "the squatting man stays down on his heels and presses his sack firmly into the shallow hole, its tied neck pointing up, "
     "and Xu Yan points his flat right hand, palm down and all five fingers together, at the next spot three steps on as he "
     "speaks,"],
    [once("s10", "firm, not smiling: lips moving clearly between words;"),
     f"firm: brows level, lips moving clearly between words, {NOSMILE};"],
    [once("s10", PUSH), STATIC],
]

S["s09b"]["replace"] = [
    [once("s09b", "wide shot from the middle of the yard toward the yard gate, like the picture:"),
     "wide shot from the front of the yard toward the yard gate, like the picture, the gate under its small tiled roof in the "
     "middle of the frame and its clear left half plain to see the whole shot:"],
    [once("s09b", "walking away from us toward the gateway, Xu Yan,"), "already at the gateway from the first frame, Xu Yan,"],
    [once("s09b", "seen from behind, framed full figure, already halfway across the yard from the first frame, the back of his "
                  "head toward us;"),
     "seen from behind, small in the frame, full figure, stepping into the clear left half of the gateway in the first frame, "
     "the back of his head toward us;"],
    [once("s09b", "just behind him, seen from behind, six men"),
     "between him and us, in one single file across the middle of the yard, every one of them small and full figure and well "
     "away from us, seen from behind, six men"],
    [once("s09b", "Xu Yan and the six men stride on across the yard and out through the gateway one after another, their backs "
                  "toward us the whole shot;"),
     "Xu Yan steps out through the gateway into the dark beyond the wall and the six men follow him out through the clear left "
     "half of the gateway one after another, their backs toward us the whole shot, until by the last frame only the last two "
     "men are still in the yard, at the gateway;"],
    [once("s09b", PUSH), STATIC],
]

S["s16b"]["replace"] = [
    [once("s16b", "framed from the waist up, both his hands resting at his sides from the first frame,"),
     "framed from the waist up with both his hands inside the frame in front of his waist the whole shot, already clenched "
     "into tight fists from the first frame,"],
    [once("s16b", "Xu Yan's two hands close slowly into fists at his sides and loosen again;"),
     "Xu Yan's two fists slowly loosen in front of his waist, the fingers uncurling one by one until both hands rest "
     "loose and relaxed, his hands staying inside the frame to the last frame;"],
    [once("s16b", "quietly resolved, not smiling: brows level, lips pressed shut;"),
     f"quietly resolved: brows level, lips pressed shut, {NOSMILE};"],
    [once("s16b", PUSH), STATIC],
]

spec = {"base": "d1 9371101 prompt and job of each shot (pictures as sent, append_pictures included)", "seeds": SEEDS,
        "shots": S}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({sum(DUR.values()) * len(SEEDS)} s)")
