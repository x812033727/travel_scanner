"""e939 fix2 stage 2 (H3): s16 and s17 with Qwen-painted set pictures (the girl already in the bed, head at the right), s20
standing (fix2 prep agent, 2026-11-24). Copied from ../../e938-live/fix6 (its s29 s30 s32 picture swap). Stage 1 (Qwen) was run
and picked first: <scratchpad>/e939f2-qwen.sh STEP=a / pick-a (step b, a painted s16 first frame, was rejected: s16 fell back to
the picture swap). Why and in what order: plan.md.

    python3 -I mkspec.py                       # -> spec.json (3 shots; seeds 9391411/9391412 for s17 s20, 9391421/9391422 for s16)
    python3 -I mkjobs.py <live>/fix2           # -> <live>/fix2/prompts/*.txt, retake.json, colab-jobs.json (6 jobs, 36 s)
    python3 -I <scratchpad>/tools/check939f2.py <live>/fix2   # check939f1.py's assertions for s16 s17 s20 (all reference mode)
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix2/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix2/colab-jobs.json

s17 s20 (reference mode, the fix1 9391302 job the cut uses as base): Xu Yan stands, both feet on the floor, bending over the bed,
never on its edge (both fix1 seeds sat him down); the girl's head on the pillow at the right (s14 s18 s24 s27; both fix1 s17 seeds
put it at the left with Doctor Bai at her feet). s17 sends set-xujia-tangfang-kong-chuang-xiaohe-l1 (stage 1: the same empty
-kong-chuang room with the girl painted in, head on the pillow at the right) in the set picture's place: fix1 s16 showed the set
picture decides what is in the bed (an empty bed in the picture -> an empty bed in both seeds, twice). Coat, black chest, no smile,
eyes shut: fix1's, kept.

s16 (reference mode on the fix1 9391301 job, the set picture swapped for -kong-men-xiaohe: the girl asleep in the bed, head at
the right; 2026-11-24 after the coordinator rejected all four Qwen 1b first frames, see plan.md): Doctor Bai and A-ling already
inside from the first frame with the door shut behind them, one chest on his back, three people, one A-ling.
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

# s16: stage 1b (Qwen: Doctor Bai and A-ling painted into -kong-men-xiaohe, 9391407-9391410) was rejected by the coordinator
# (07 nobody added; 08 two young women, no Doctor Bai; 09 10 the two look pasted in, studio-lit, and the shut door became an open
# blue night doorway), so s16 takes the fallback of plan.md: reference mode on the fix1 9391301 job (Doctor Bai's portrait, A-ling's
# portrait and angle, as fix1 sent) with the set picture swapped for -kong-men-xiaohe (1a 9391403: the girl asleep in the bed,
# head on the pillow at the right, the door shut). The fix1 text kept the girl out of focus with her head beyond the right edge;
# now she lies in the frame as the picture shows her. Three people, "only" twice; one A-ling written hard (fix1 1302 drew two).
MEN_OLD = "set-xujia-tangfang-kong-men-l1.png"
MEN_NEW = "set-xujia-tangfang-kong-men-xiaohe-l1.png"
GIRL_OLD = ("and at the right, soft and out of focus, the foot of the bed with the pink quilted cover drawn up over the small shape "
            "of a little girl of eight asleep in the bed, only the small rounded shape of her body under the quilt in the frame, her "
            "head on the pillow at the pillow end beyond the right edge of the frame, lying still; their hands hold only what is "
            "described here; exactly two people standing in the room, with the little girl asleep in the bed behind them, out of "
            "focus. Only these 2 people stand in the frame, with the little girl asleep under the quilt in the bed at the right; no "
            "second copy of anyone appears.")
GIRL_NEW = ("and at the right the wooden bed with the little girl of eight asleep in it under the pink quilted cover, exactly as in "
            "<Picture 4>, her head on the small pink pillow at the right end of the bed inside the frame, her eyes shut, one folded "
            "damp white cloth on her forehead, lying still; their hands hold only what is described here; exactly three people: the "
            "old man and the young woman standing by the door, and the little girl asleep in the bed. Only these 3 people are in the "
            "frame: one Doctor Bai, one A-ling and one sleeping girl; A-ling is one woman, in the frame once, only at his side by the "
            "door, the only young woman in the room; no second copy of anyone appears.")
S["s16"] = {"mode": "reference", "base": ["fix1", 9391301], "seeds": [9391421, 9391422], "duration_seconds": 6,
            "swap_pictures": {MEN_OLD: MEN_NEW}, "replace": [
    [once("s16", "the location shown in <Picture 4> is the set, keeping its layout and props."),
     "the location shown in <Picture 4> is the set, keeping its layout and props, with the little girl asleep in its bed exactly "
     "as the picture shows her, her head on the pillow at the right end of the bed, and the plank door at the left shut."],
    [once("s16", "just inside the door, already in from the first frame, A-ling,"),
     "just inside the door, both already in the room from the first frame with the door shut behind them, A-ling,"],
    [once("s16", "toward the bed beyond the right edge of the frame, never the lens;"),
     "toward the sleeping girl in the bed at the right, never the lens;"],
    [once("s16", GIRL_OLD), GIRL_NEW],
    [once("s16", "his eyes on the bed beyond the right edge of the frame, never looking at the camera;"),
     "his eyes on the sleeping girl in the bed at the right, never looking at the camera;"],
    [once("s16", "the little girl in the bed sleeps on, still, and the small flame"),
     "the little girl in the bed sleeps on, still, her head on the pillow at the right, only these three people are in the room "
     "to the last frame, and the small flame"],
]}

(HERE / "spec.json").write_text(json.dumps({"shots": S}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({2 * sum(v['duration_seconds'] for v in S.values())} s)")
