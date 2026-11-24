"""e939 fix2 stage 2 (H3): s16 from a Qwen-painted first frame, s17 with a Qwen-painted set picture (the girl already in the bed,
head at the right), s20 standing (fix2 prep agent, 2026-11-24). Copied from ../../e938-live/fix6 (s22 -> s16 first_frame; s29 s30
s32 -> s17 picture swap). Stage 1 (Qwen) must have been run and picked first: <scratchpad>/e939f2-qwen.sh, STEP=a / pick-a / b /
pick-b. Why and in what order: plan.md.

    python3 -I mkspec.py                       # -> spec.json (3 shots; seeds 9391411/9391412 for s17 s20, 9391421/9391422 for s16)
    python3 -I mkjobs.py <live>/fix2           # -> <live>/fix2/prompts/*.txt, retake.json, colab-jobs.json (6 jobs, 36 s)
    python3 -I <scratchpad>/tools/check939f2.py <live>/fix2   # check939f1.py's assertions for s17 s20 (reference mode)
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix2/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix2/colab-jobs.json

s17 s20 (reference mode, the fix1 9391302 job the cut uses as base): Xu Yan stands, both feet on the floor, bending over the bed,
never on its edge (both fix1 seeds sat him down); the girl's head on the pillow at the right (s14 s18 s24 s27; both fix1 s17 seeds
put it at the left with Doctor Bai at her feet). s17 sends set-xujia-tangfang-kong-chuang-xiaohe-l1 (stage 1: the same empty
-kong-chuang room with the girl painted in, head on the pillow at the right) in the set picture's place: fix1 s16 showed the set
picture decides what is in the bed (an empty bed in the picture -> an empty bed in both seeds, twice). Coat, black chest, no smile,
eyes shut: fix1's, kept.

s16 (first_frame mode, one picture: the Qwen frame fitted to 960x544, with the sleeping girl, Doctor Bai and A-ling already in it):
the storyboard has them inside from the first frame with the door shut behind them, so nobody comes through the door. Nobody is
named (no portrait is sent in first_frame mode; the first frame fixes the faces).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
F1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e939-dh/runpod/live/fix1")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SET_OLD = "set-xujia-tangfang-kong-chuang-l1.png"
SET_NEW = "set-xujia-tangfang-kong-chuang-xiaohe-l1.png"
HEAD = "his whole head and face staying inside the frame"


def f1text(sid):
    return (F1 / "prompts" / f"ref-{sid}-9391302.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert f1text(sid).count(s) == 1, (sid, s[:80])
    return s


S = {}
S["s17"] = {"mode": "reference", "base": ["fix1", 9391302], "seeds": [9391411, 9391412], "duration_seconds": 6,
            "swap_pictures": {SET_OLD: SET_NEW}, "replace": [
    [once("s17", "the location shown in <Picture 5> is the set, keeping its layout and props."),
     "the location shown in <Picture 5> is the set, keeping its layout and props, with little Xiaohe lying in its bed exactly as "
     "the picture shows her, her head on the pillow at the right end of the bed; she is the one girl of <Picture 3>, in the frame "
     "once."],
    [once("s17", "medium shot at the bedside: Xu Yan,"),
     "medium shot from the near side of the bed, the bed running across the frame under the small window as in <Picture 5>, its "
     "pillow end at the right and its slatted wooden foot end at the left: Xu Yan,"],
    [once("s17", "standing upright on his feet beside the bed from the first frame to the last, framed from the waist up, the one "
                 "white candle in a plain clay dish already lifted from the low stool and held up in his right hand from the first "
                 "frame, its small flame lighting the pillow,"),
     "standing upright on both feet on the floor at the left, by the foot end of the bed, from the first frame to the last, "
     f"framed from the waist up, {HEAD}, already bending forward from the waist over the bed from the first frame, the one white "
     "candle in a plain clay dish already lifted from the low stool and held out low in his right hand toward her face, its small "
     "flame lighting the pillow,"],
    [once("s17", "lying on her back in the bed under the pink quilted cover drawn up to her chest,"),
     "lying on her back in the bed under the pink quilted cover drawn up to her chest, her head on the pillow at the right end of "
     "the bed toward screen right and her feet toward the foot end at the left, exactly as she lies in <Picture 5>,"],
    [once("s17", "at the right, by the pillow end, Doctor Bai,"), "at the right, beside her head at the pillow end, Doctor Bai,"],
    [once("s17", "Xu Yan holds the candle down close beside the pillow so its small light falls on her flushed face, and Doctor Bai "
                 "sits down on the edge of the bed by the pillow; the grey outer coat stays on Xu Yan's shoulders to the last frame "
                 "and Xu Yan stays standing;"),
     "Xu Yan, still on his feet, bends a little lower and brings the candle close beside her face so its small light falls on her "
     "flushed face, and Doctor Bai sits down on the edge of the bed beside her head; the grey outer coat stays on Xu Yan's "
     "shoulders to the last frame and Xu Yan stays standing, both feet on the floor, from the first frame to the last, and her "
     "head stays on the pillow at the right;"],
]}
S["s20"] = {"mode": "reference", "base": ["fix1", 9391302], "seeds": [9391411, 9391412], "duration_seconds": 6,
            "swap_pictures": {}, "replace": [
    [once("s20", "sitting on the near edge of the bed, framed from the waist up, his left arm already under her shoulders"),
     "standing upright on both feet on the floor at the near side of the bed from the first frame to the last, bending forward "
     f"from the waist over her, framed from the waist up, {HEAD}, his left arm already under her shoulders"],
    [once("s20", "lying in the bed under the pink quilted cover,"),
     "lying in the bed under the pink quilted cover, her head toward the pillow at the right end of the bed,"],
    [once("s20", "and the grey outer coat stays on Xu Yan's shoulders to the last frame;"),
     "and the grey outer coat stays on Xu Yan's shoulders to the last frame and Xu Yan stays standing, both feet on the floor, "
     "bending over her, from the first frame to the last;"],
]}

S16 = (
    "For the target video, <Picture 1> is referenced throughout.\n\n"
    "integrated_multimodal_description: [Shot 1] Photorealistic live-action film footage of real actors in an ancient Chinese "
    "(Song-dynasty) period drama, with the look of a feature film. The first frame shown in <Picture 1> stays exactly as it is: "
    "its framing, the small bedroom by night, the shut plank door at the left, the cracked plaster wall, the low wooden stool with "
    "its one burning white candle, the old man in his faded moon-white long gown and quilted cotton vest with the one square black "
    "lacquered medicine chest on his back, the young woman in grey-white holding his arm, and at the right the wooden bed with the "
    "little girl asleep under the pink quilted cover, her head on the pillow at the right end, preserving their appearance, their "
    "costumes and the set layout. Initial composition: In the first bedroom of the Xu farmhouse in the third watch of the same "
    "night, by the plank door; the one small flame on the low stool at the foot of the bed the only warm light, the corners of the "
    "room deep in shadow: medium shot by the plank door, as in the first frame: the plank door at the left shut behind them, its "
    "planks closed from the first frame to the last; just inside the door, already in from the first frame, the young woman in "
    "her plain grey-white cotton dress, the long grey sash draped over her left arm, her right arm under his elbow holding him up, "
    "her back bare of any load, carrying nothing, her face toward him, her lips closed, not smiling, never the lens; beside her, "
    "the old man, lean, his white hair in a small topknot and his short white beard trimmed close at the chin, the black lacquered "
    "wooden medicine chest, one square box with a lid, on its strap on his back, the one chest in the room, unsteady on his feet, "
    "his face three-quarter to screen right toward the bed, never the lens; urgent and out of breath, not smiling: brows knotted, "
    "lips moving fast between words; at the right, the little girl asleep in the bed under the pink quilted cover, her head on "
    "the pillow at the right end, her eyes shut, lying still; exactly two people standing in the room, with the little girl asleep "
    "in the bed. Only these 2 people stand in the frame, with the little girl asleep under the quilt in the bed at the right; no "
    "second copy of anyone appears. Facial expressions follow the action and lines described below, not the first frame alone: "
    "the first frame fixes the faces, hair and costumes, never the mood. The old man speaks a short Mandarin line, "
    "「病人在哪？快把燈拿近一點」, his lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes, "
    "his face three-quarter to screen right, turned toward the bed, his eyes on the sleeping girl, never looking at the camera; "
    "the old man finds his feet, straightens and takes one step toward the bed as he speaks, the young woman letting go of his arm; "
    "the young woman says nothing in this shot: her lips stay pressed together from the first frame to the last, no talking, no "
    f"mouthing words, {NOSMILE}; the plank door stays shut, the little girl in the bed sleeps on, still, her eyes shut, and the "
    "small flame and the shadows stay unchanged. The camera holds a static shot. One continuous shot. The picture is clean, with "
    "no subtitles, captions or text anywhere on screen; the still night air, the small candle flame swaying, a clean natural film "
    "image. Natural, realistic human motion and acting of real actors: faces, hair and costumes stay as in the first frame, while "
    "every visible face acts the emotion written above and changes with it.\n"
    "overall_soundscape: N/A\n"
    "non_diegetic_music: N/A"
)
S["s16"] = {"mode": "first_frame", "base": ["fix1", 9391301], "seeds": [9391421, 9391422], "duration_seconds": 6,
            "first_frame": "first-frames/s16-ff.png", "prompt": S16}

(HERE / "spec.json").write_text(json.dumps({"shots": S}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({2 * sum(v['duration_seconds'] for v in S.values())} s)")
