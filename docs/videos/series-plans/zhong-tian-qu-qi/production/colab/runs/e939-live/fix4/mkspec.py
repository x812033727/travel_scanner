"""e939 fix4: s40b rewritten (../cut-review-2.md major 2: in fix3 s40b the people of the village barely turn and Xu Yan never comes;
the ending reads "they look at the barn", not "everyone turns to Xu Yan"). Why in plan.md.

    python3 -I mkspec.py                       # -> spec.json (1 shot, seeds 9391601/9391602)
    python3 -I mkjobs.py <live>/fix4           # -> <live>/fix4/prompts/*.txt, retake.json, colab-jobs.json (2 jobs, 10 s)
    python3 -I <scratchpad>/tools/check939f4.py <live>/fix4   # check939.py's assertions, rewritten for this shot

The beat (bible 〈接點〉 39->40: everyone turns to Xu Yan, who has just arrived; e040 s1 he steps between Qin Shuang and the people
of the village, facing left): the same six of s36 (the same clothes, ages and places) stand with their backs to the camera; early
in the shot they turn their heads together toward screen right, and Xu Yan walks into the frame from the right edge along the
strip of trampled earth (the path in set-gucang-wai-l1), stops, and looks at them, serious, not smiling, facing left, silent.
His portrait and angle-a are sent (check939: both, portrait first); the set is the whole barn-front picture (s36's).
Costume: the morning costume of the episode, s24-s35 (his faded blue-grey robe patched at one elbow, the lime powder on its
lower half, topknot with a cloth band). The grey outer coat is not written: it has been on A-ling's shoulders since s23 (s26
「這件外衣是你蓋的」, check939 asserts no coat on him in the morning), and e040 picks him up from here.
The job's fields come from the d1 s35 job (Xu Yan's pictures from it); the prompt is written whole, in the d1 shots' order
(style, identity, set clause, place and light, composition, count twice, the facial-expression sentence with "never the mood. ",
motion, silence, camera, "One continuous shot.", clean picture). 5 s bought, about 2-3 s used. Static camera.
Seeds: 93916xx is new for e939 (93912xx Qwen door, 93913xx fix1, 93914xx fix2, 93915xx fix3).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = [9391601, 9391602]
XU_ID = ("Xu Yan shown in <Picture 1> and <Picture 2> (the same man from several angles) keeps exactly the same face, hair and "
         "costume as the pictures: East Asian young man of twenty-five, clean-cut handsome with thick brows, double-lidded bright "
         "eyes, straight nose and a firm mouth, tall and lean with broad shoulders, black hair gathered up into a topknot on the "
         "crown and tied with a cloth band, a few strands falling over his forehead, a faded blue-grey cotton scholar's robe "
         "patched at one elbow, cloth shoes; ")
FOLK6 = ("an old man with a white topknot in a faded grey long robe, a thin middle-aged man in charcoal grey, a boy of fifteen in "
         "faded indigo, a stout man of fifty in dark olive green, a middle-aged woman in dark grey with a faded indigo head cloth "
         "and a broad-backed man of about forty in an undyed hemp short jacket and a cloth head wrap")
TEXT40B = (
    "For the target video, <Picture 1>, <Picture 2> and <Picture 3> are referenced throughout.\n\n"
    "integrated_multimodal_description: [Shot 1] Photorealistic live-action film footage of real actors in an ancient Chinese "
    "(Song-dynasty) period drama, with the look of a feature film. " + XU_ID + "the location shown in <Picture 3> is the set, "
    "keeping its layout and props. Initial composition: Before the old plank barn at the edge of the Liuxi fields in the early "
    "morning of the next day: the place exactly as in the picture: the low old barn of grey weathered planks at the right under "
    "its pitched plank roof, its two plank door leaves swung back flat against its front on both sides of the dark doorway, a "
    "broad strip of trampled sun-warmed earth before it running out of the frame at the right edge, the path from the village, "
    "the flooded field of young green rice seedlings across the left half of the frame, small village houses and low blue "
    "hills far away, one big tree behind the barn; low warm golden morning sunlight from the right, long shadows across the "
    "trampled earth, a clear pale blue sky: medium-wide shot from behind six people of the village standing in a loose row "
    "across the left and middle of the frame on the trampled earth with their backs to the camera, framed from the waist up: "
    + FOLK6 + ", all six seen only from behind, the backs of their heads and their shoulders toward the camera from the first "
    "frame; the right part of the frame clear: the strip of trampled earth running in from the right edge, empty in the first "
    "frame; beyond them, soft, the grey plank barn and its dark doorway; Xu Yan, in his faded blue-grey scholar's robe patched "
    "at one elbow, pale white lime powder dusted over the lower half of the robe, his black hair in its topknot tied with a "
    "cloth band, comes into the frame from the right edge along the strip of trampled earth after the first second, framed "
    "from the knees up, his face three-quarter to screen left toward the six people of the village, never the lens; grave and "
    "steady, not smiling: jaw set, brows level and drawn together, lips pressed shut, " + NOSMILE + "; their hands hold only "
    "what is described here; exactly seven people, the six people of the village seen only from behind. Only Xu Yan and the six "
    "people of the village seen from behind are in the frame; no second copy of anyone appears. Facial expressions follow the "
    "action described below, not the reference pictures: the pictures fix the face, hair and costume only, never the mood. "
    "At the start all six turn their heads together toward the right edge of the frame, clearly and at the same moment, their "
    "shoulders turning after their heads, every one of them still turned away from the camera, only the backs of their heads "
    "and at most the edge of a cheek in view; Xu Yan walks in from the right edge along the strip of trampled earth with quick "
    "steady steps, stops a few paces from them in the right part of the frame, and stands looking at them, his face "
    "three-quarter to screen left, grave, to the last frame; the six stay turned toward him to the last frame; Xu Yan says "
    "nothing in this shot: his lips stay pressed together from the first frame to the last, no talking, no mouthing words; the "
    "six stay silent, and the low warm morning sunlight stays unchanged. The camera holds a static shot. One continuous shot. "
    "The picture is clean, with no subtitles, captions or text anywhere on screen; the fresh still air of early morning, a clean "
    "natural film image. Natural, realistic human motion and acting of real actors: Xu Yan keeps the identity, hair and costume "
    "of his reference pictures, while his face acts the emotion written above; the pictures are neutral studio portraits, never "
    "copy their blank expression.\n"
    "overall_soundscape: N/A\n"
    "non_diegetic_music: N/A")  # no trailing newline, as the d1 prompt files
S = {"s40b": {"base": ["d1", "s35", 9391101], "duration_seconds": 5,
              "pictures": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-gucang-wai-l1.png"], "text": TEXT40B}}

(HERE / "spec.json").write_text(json.dumps({"seeds": SEEDS, "shots": S}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(S), "shot ->", HERE / "spec.json", f"({sum(v['duration_seconds'] for v in S.values())} s per seed, "
      f"{2 * sum(v['duration_seconds'] for v in S.values())} s)")
