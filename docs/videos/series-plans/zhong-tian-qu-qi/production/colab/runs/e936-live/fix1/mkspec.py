"""e936 fix1: the retakes of ../picks-merged.tsv (merge agent, 2026-11-20). Why, shot by shot, in plan.md.

    python3 -I mkspec.py                       # -> spec.json (9 shots, seeds 9361211/9361212 for every shot)
    python3 -I mkjobs.py <live>/fix1           # -> <live>/fix1/prompts/*.txt, retake.json, colab-jobs.json (18 jobs, 124 s)
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix1/colab-jobs.json

As e935 fix1: the base of eight jobs is the d1 9361101 job and prompt exactly as sent (mkjobs.py checks the sha256 and that
every d1 edit of ../spec.json for the shot is in it); each fix1 replace is asserted to be in that prompt exactly once. s04 is
written whole (e935 fix4 s24's way, e934 fix4 s32): Qian Yuanwai's back, no face picture, no name, the line on the recording
a03. Every shot is bought at its d1 length (= writer-tools/e036-r2/r2.py BUY, not changed). Seeds 9361211/9361212 (e936 used
93612xx only for the gate picture, 9361201-9361204). No prompt carries 'shot on a cinema camera' (d1 already says 'with the
look of a feature film').

Must (coordinator): s01 s04 s18 s28 s31. Added by the merge agent after looking: s11b (background jumps from s11's sky to a
pavilion with lanterns and torches), s12b (the push takes her head out of frame / 1101 turns her cheek), s20 (grin, fake writing
on a booklet, 1101 looks away from A-ling), s26 (no slam on the table, a smiling frame at 7.25 s).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e936-dh/runpod/live/d1")
REFS = "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live/"
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = [9361211, 9361212]
DUR = {"s01": 6, "s04": 8, "s11b": 6, "s12b": 6, "s18": 6, "s20": 6, "s26": 10, "s28": 8, "s31": 6}  # d1 = r2.py BUY
STATIC = "The camera holds a static shot."
PUSH = "The camera pushes in with small amplitude at slow speed."
SKYBACK = ("only the orange-red evening sky above the dark line of the far hills and the dark trailing branches of one willow "
           "at the left edge of the frame, clear sky all around his head and shoulders")


def d1text(sid):
    return (D1 / "prompts" / f"ref-{sid}-9361101.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert d1text(sid).count(s) == 1, (sid, s[:70])
    return s


S = {sid: {"duration_seconds": DUR[sid], "replace": []} for sid in DUR}

S["s01"]["replace"] = [
    [once("s01", "closed from the first frame to the last, the warm orange light"),
     "shut tight from the first frame to the last, the seam between the two leaves a thin dark line to the last frame, the warm "
     "orange light"],
    [once("s01", "already standing close before the crossbar with both hands gripping it from the first frame;"),
     "already standing still close before the crossbar with both hands gripping it from the first frame, his feet planted;"],
    [once("s01", "her black hair in just two round buns set high on her head tied with short pink silk ribbons,"),
     "every strand of her black hair combed smooth and wound up inside just two round buns set high on her head tied with short "
     "pink silk ribbons, the nape of her neck bare and clear above her collar,"],
    [once("s01", "grave, not smiling, their lips closed,"), f"grave, {NOSMILE}, their lips closed,"],
    [once("s01", "Xu Yan braces his feet and lifts the thick crossbar up out of its iron fitting with both hands, its weight "
                 "dragging his shoulders down, and holds it level across his body, while the two gate leaves stay closed;"),
     "By the middle of the shot Xu Yan has lifted the whole thick crossbar clear up out of its iron fitting to the height of his "
     "chest, holding it level across his body in both hands, and he stands still holding it, the two gate leaves untouched in "
     "front of him and shut tight to the last frame; he braces his feet and lifts the bar up to his chest with both hands, its "
     "weight dragging his shoulders down;"],
    [once("s01", PUSH), STATIC],
]

S["s11b"]["replace"] = [
    [once("s11b", "the location shown in <Picture 3> is the set, keeping its layout and props."),
     "the evening sky shown in <Picture 3> gives only the colour of the background."],
    [once("s11b", "five days after the swarm night, just inside the gate;"),
     "five days after the swarm night, under the wide evening sky;"],
    [once("s11b", "standing just inside the gate, framed"), "standing out under the wide sky, framed"],
    [once("s11b", "resolved, not smiling: eyes steadying, brows level, lips pressed shut;"),
     f"resolved: eyes steadying, brows level, lips pressed together in one flat line, {NOSMILE};"],
    [once("s11b", "the wavering orange light of torches on one side of his face;"),
     "a warm orange glow of the sunset on one side of his face;"],
    [once("s11b", "behind him, soft, only the orange-red evening sky over the far hills;"), f"behind him, soft, {SKYBACK};"],
    [once("s11b", PUSH), STATIC],
]

S["s12b"]["replace"] = [
    [once("s12b", "only the back of a young woman's head with two round buns tied with short pink silk ribbons and one light "
                  "peach-pink silk shoulder, toward us the whole shot;"),
     "only the round back of a young woman's head, every strand of her black hair wound up inside two round buns tied with short "
     "pink silk ribbons, and one light peach-pink silk shoulder, the back of her head toward us and her head still the whole "
     "shot, staying at the right edge of the frame from the first frame to the last;"],
    [once("s12b", "his face three-quarter to screen right toward the young woman in the foreground, never the lens;"),
     "his face turned well to screen right in three-quarter profile toward the young woman in the foreground, his eyes on her "
     "face beyond the edge of the frame, never the lens;"],
    [once("s12b", "decided, not smiling: brows level, eyes clear, lips moving firmly between words;"),
     f"decided: brows level, eyes clear, the corners of his mouth level, lips moving firmly between words, {NOSMILE};"],
    [once("s12b", PUSH), STATIC],
]

S["s18"]["replace"] = [
    [once("s18", "medium shot from close behind one young woman seen only from behind, appearing only once:"),
     "medium-wide shot from behind at seated eye height, the whole length of the table in the frame, one young woman seen only "
     "from behind, appearing only once, seated in the exact centre of the frame from the first frame to the last:"],
    [once("s18", "her right hand resting on one plain dark wooden abacus, a flat dark wooden frame with round dark beads on thin "
                 "rods before her;"),
     "her right hand resting on one plain dark wooden abacus, a flat dark wooden frame with round dark beads on thin rods before "
     "her at the right end of the table, the abacus staying under her right hand the whole shot;"],
    [once("s18", "her face lowered to the paper, her lips closed, not smiling, never the lens;"),
     f"her face lowered to the paper, her lips closed, {NOSMILE}, never the lens, her left hand resting flat beside the paper, "
     "her hands holding only the brush;"],
    [once("s18", "Her right hand stops still on the beads of the abacus, only her arm moving;"),
     "The young woman with the buns stays seated in the middle of the frame from the first frame to the last, her back to us, "
     "her head still, the only young woman with two high round buns in the frame; her right hand stops still on the beads of "
     "the abacus, only her arm moving;"],
    [once("s18", PUSH), STATIC],
]

S["s20"]["replace"] = [
    [once("s20", "the slim brush laid across the small dark stone dish, the blank plain white paper soft at the lower edge,"),
     "the slim brush laid across the small dark stone dish and one single sheet of blank plain white paper the only things on "
     "the bare tabletop,"],
    [once("s20", "Xu Yan straightens up from the paper and speaks softly to her, his face three-quarter to screen left toward "
                 "her, a faint easy look in his eyes,"),
     "Xu Yan straightens up from the paper and speaks softly to her, his face three-quarter to screen left toward her, his eyes "
     f"on her face, his brows easing and his eyes gentle, the corners of his mouth level, {NOSMILE},"],
    [once("s20", PUSH), STATIC],
]

S["s26"]["replace"] = [
    [once("s26", "furious and disbelieving, not smiling: eyes bulging, brows knotted, the corners of his mouth dragged hard "
                 "down, lips moving fast and hard between words;"),
     "furious and disbelieving: eyes bulging, brows knotted, the corners of his mouth dragged hard down, his cheeks slack and "
     f"heavy, lips moving fast and hard between words, {NOSMILE};"],
    [once("s26", "Qian Yuanwai slams his flat right hand down on the tabletop as he speaks, and the slivers of bamboo in the "
                 "basket jump,"),
     "In the middle of the line his flat right hand comes down hard on the tabletop beside the basket with one loud slam, and "
     "the slivers of bamboo in the basket bounce up and fall back; his hand stays pressed flat on the table to the end of the "
     "line,"],
    [once("s26", PUSH), STATIC],
]

S["s28"]["replace"] = [
    [once("s28", "one short portly man seen only from behind,"),
     "exactly one person in the frame, one short portly man seen only from behind,"],
    [once("s28", "already turned away from the long plain wooden table at the left edge from the first frame,"),
     "already turned away from the long plain wooden table at the left edge from the first frame, both his hands empty, the "
     "table and its bench standing empty with nobody at them, its top bare,"],
    [once("s28", "ahead of him the flat dry yellow field and the line of dark pines; he is the only person in the frame;"),
     "ahead of him only the open flat dry yellow field and the line of dark pines far away, open bare ground all the way to "
     "them; he is the only person in the frame;"],
    [once("s28", "He flings his wide right sleeve hard out to the side and strides away from us across the dry field toward the "
                 "far pines, getting smaller, his back toward us the whole shot,"),
     "By the end of the shot he has walked far out across the dry field toward the far pines, much smaller, alone, still walking "
     "away; he flings his wide right sleeve hard out to the side once, both hands empty, and keeps striding away from us across "
     "the open field, alone, getting much smaller, his back toward us the whole shot, the only person in the frame,"],
    [once("s28", PUSH), STATIC],
]

S["s31"]["replace"] = [
    [once("s31", "already risen to her feet off the woodpile from the first frame, standing in the yard at the left;"),
     "small in the frame, already risen to her feet off the woodpile from the first frame, standing in the yard at the left, "
     "seen from the side, her face turned away toward the back wall;"],
    [once("s31", "running behind the well, their heads to the wall, nine men in ragged homespun curled asleep on them under "
                 "ragged blankets with their backs to us, the three mats in the middle of the row empty;"),
     "all of them right at the foot of the wall, their heads to the wall, nine men in ragged homespun lying curled on their "
     "sides asleep under ragged blankets, facing the wall, only their backs and the backs of their heads toward us, eyes unseen, "
     "and the three mats in the middle of the row clearly visible, flat and bare; the round stone well stands alone in the "
     "front right with bare open ground all around it;"],
    [once("s31", "Qin Shuang turns her head toward the back wall and walks step by step across the yard toward it, her "
                 "footfalls light;"),
     "Qin Shuang walks step by step across the middle of the yard toward the back wall, her face toward the wall, her footfalls "
     "light, while the nine men lie still asleep on their mats along the wall;"],
    [once("s31", PUSH), STATIC],
]

HEAD1 = "For the target video, <Picture 1> is referenced throughout.\n\n"
STYLE = ("integrated_multimodal_description: [Shot 1] Photorealistic live-action film footage of real actors in an ancient "
         "Chinese (Song-dynasty) period drama, with the look of a feature film. ")
TAIL = "\noverall_soundscape: N/A\nnon_diegetic_music: N/A"
S04 = (HEAD1 + STYLE +
       "The one man in this shot is a short, portly man of fifty, filmed from behind him, in an ancient Chinese Song-dynasty "
       "rich landlord's dark gold silk cross-collared robe woven with small round medallions, with long wide sleeves and a "
       "black belt, and a small round black cap; the corner of the gate's small tiled roof and the evening sky shown in "
       "<Picture 1> are the set, keeping their layout. Initial composition: At the village entrance of Liuxi at dusk five "
       "days after the swarm night, up on the low earthen mound beside the gate; a warm orange-red evening sky, the sun just "
       "gone below the far hills: low-angle medium shot from behind and below him, framed from the waist up with clear sky "
       "above his cap: the portly man stands in the middle of the frame with his broad back square to the camera from the "
       "first frame, the back of his cap, the back of his thick neck and his rounded shoulders in dark gold silk toward the "
       "camera, his head facing straight away from the camera toward the village beyond; he is the only person in the frame; "
       "scornful and urgent: his shoulders hunched up stiff, his head jutting forward; above him, soft, the dark corner of the "
       "gate's small tiled roof at the upper left and the orange-red evening sky all around; their hands hold only what is "
       "described here. No second copy of anyone appears. The picture fixes the place and its light only, never the mood. "
       "The portly man leans forward over the edge of the mound toward the village and sweeps his flat right hand out from the "
       "left across to the right in one wide stroke, his wide sleeve swinging, then jabs the hand forward twice toward the "
       "village, his shoulders heaving, his broad back square to the camera the whole shot, the back of his cap toward the "
       "camera to the last frame, and the orange-red evening light stays unchanged. " + STATIC + " One continuous shot. The "
       "picture is clean, with no subtitles, captions or text anywhere on screen; a light evening breeze in the air, a clean "
       "natural film image. Natural, realistic human motion of a real actor: the weight of his heavy body moves as he leans "
       "and sweeps his arm, and the gold silk folds and swings over his back and sleeves." + TAIL)
S["s04"] = {"duration_seconds": DUR["s04"], "text": S04, "pictures": [REFS + "set-cunkou-zha2-ding2-l1.png"]}

spec = {"base": "d1 9361101 prompt and job of each shot (s04: written whole, the d1 job)", "seeds": SEEDS, "shots": S}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({sum(DUR.values()) * len(SEEDS)} s)")
