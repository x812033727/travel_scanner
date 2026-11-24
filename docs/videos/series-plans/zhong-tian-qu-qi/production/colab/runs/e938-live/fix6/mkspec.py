"""e938 fix6 stage 2 (H3): s29 s30 s32 with the saddled horse picture, and s22 from a painted first frame (fix6 prep agent,
2026-11-24). Stage 1 (Qwen: the saddled horse prop-zaohongma-an-l1, the s22 first frame) must have been run and picked first:
<scratchpad>/e938f6-qwen.sh, STEP=a / pick-a / b / pick-b. Why and in what order: plan.md.

    python3 -I mkspec.py                       # -> spec.json (4 shots; seeds 9381811/9381812 for s29 s30 s32, 9381821/9381822 for s22)
    python3 -I mkjobs.py <live>/fix6           # -> <live>/fix6/prompts/*.txt, retake.json, colab-jobs.json (8 jobs, 44 s)
    python3 -I <scratchpad>/tools/check938f6.py <live>/fix6   # check938.py's assertions for s29 s30 s32 (reference mode)
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix6/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix6/colab-jobs.json

s29 s30 s32 (reference mode, the d1 9381101 job as base, as fix5): the horse prop picture is swapped for the saddled one, and the
text stops describing the saddle in its own words (fix5 showed H3 draws a western saddle from any wording when the picture is a
bare horse): it points at the picture. s32 is a static wide that holds all nine people and the horse to the last frame (both fix5
takes pushed in to the captain's waist). The rest is the d1 take the cut uses.

s22 (first_frame mode, one picture: the Qwen frame fitted to 960x544): the prompt anchors on <Picture 1> and only moves what fix2
9381401 asked for: reined in, standing on the spot, four hooves on the paving, head toss, not smiling, static.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live/d1")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
STATIC = "The camera holds a static shot."
PUSH = "The camera pushes in with small amplitude at slow speed."
SADDLE_OLD = "an old plain brown leather saddle on a folded dark cloth"
SADDLE_NEW = "its low flat old saddle of dark brown leather on a folded dark cloth exactly as in its picture"
PROP_OLD = "and its plain dark bridle, with the saddle written above;"
PROP_NEW = ("and its plain dark bridle, and exactly its saddle, the folded dark cloth under it and its dark iron stirrup as the "
            "picture shows them;")


def d1text(sid):
    return (D1 / "prompts" / f"ref-{sid}-9381101.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert d1text(sid).count(s) == 1, (sid, s[:80])
    return s


S = {}
for sid, dur in (("s29", 5), ("s30", 6), ("s32", 6)):
    S[sid] = {"mode": "reference", "base": ["d1", 9381101], "seeds": [9381811, 9381812], "duration_seconds": dur,
              "swap_pictures": {"prop-zaohongma-l1.png": "prop-zaohongma-an-l1.png"},
              "replace": [[once(sid, SADDLE_OLD), SADDLE_NEW], [once(sid, PROP_OLD), PROP_NEW]]}
S["s32"]["replace"] += [
    [once("s32", "wide shot up the street toward its far end at the left, the square stone hitching post soft in the right foreground:"),
     "wide shot up the street toward its far end at the left, held this wide from the first frame to the last, all nine people "
     "and the horse inside the frame the whole shot, the square stone hitching post soft in the right foreground:"],
    [once("s32", PUSH), STATIC],
]

S22 = (
    "For the target video, <Picture 1> is referenced throughout.\n\n"
    "integrated_multimodal_description: [Shot 1] Photorealistic live-action film footage of real actors in an ancient Chinese "
    "(Song-dynasty) period drama, with the look of a feature film. The first frame shown in <Picture 1> stays exactly as it is: "
    "its framing, the night gate of the county town, the swung-out small side door of studded planks at the left with its one "
    "torch fixed upright in an iron holder, nobody holding it, the long waist-high barrier of crossed wooden stakes across the "
    "lower part of the frame nearest to the camera, and beyond it the young woman in grey-white on the one chestnut-red horse with its low flat dark "
    "leather saddle, two horse-lengths back from the barrier, a strip of empty paving clear between the stakes and its hooves, "
    "the long city wall behind them, preserving her appearance, her plain grey-white dress, the horse, the saddle and the set "
    "layout. Initial composition: Before the gate of the county town in the second watch of the same night, at the barrier of "
    "crossed stakes; cold blue moonlight, the torch by the side door the only warm light: wide shot from a low camera on the "
    "side-door side of the barrier, as in the first frame: the barrier nearer to the camera than the horse, standing between the "
    "horse and the side door; beyond it, on the road along the foot of the long city wall, the one horse already reined in to a "
    "standstill from the first frame, seen side-on with its head toward the left, with the young woman in grey-white in the saddle, framed full figure, "
    "her face in profile to screen left toward the gate, never the lens, cold and still, her lips pressed shut in one flat line, "
    f"{NOSMILE}; she is the only person in the frame. Besides her, only the one horse is in the frame, the horse beyond the "
    "barrier and the side door on our side of it; no second copy of anyone or of the horse appears. Facial expressions follow "
    "the action described below, not the first frame alone: the first frame fixes the face, hair and costume, never the mood. "
    "Beyond the barrier the horse stays on the same spot from the first frame to the last and does not walk; it tosses its head "
    "hard and stamps its forefeet where it stands, snorting, all four hooves staying on the paving, the strip of empty paving "
    "staying clear between the stakes and its hooves, while the young woman holds the reins tight, and the cool moonlight stays unchanged. "
    "The young woman says nothing in this shot: her lips stay pressed together from the first frame to the last, no talking, no mouthing "
    "words. The camera holds a static shot. One continuous shot. The picture is clean, with no subtitles, captions or text "
    "anywhere on screen; the cold night air, the torch flame wavering, a clean natural film image. Natural, realistic human "
    "motion of a real actor and a real horse; face, hair, costume and the horse stay as in the first frame.\n"
    "overall_soundscape: N/A\n"
    "non_diegetic_music: N/A"
)
S["s22"] = {"mode": "first_frame", "base": ["fix2", 9381401], "seeds": [9381821, 9381822], "duration_seconds": 5,
            "first_frame": "first-frames/s22-ff.png", "prompt": S22}

(HERE / "spec.json").write_text(json.dumps({"shots": S}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({2 * sum(v['duration_seconds'] for v in S.values())} s)")
