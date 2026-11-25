"""e935 fix4 (coordinator 2026-11-20, quality first): s24 as a back shot with the line on the recording, s06 with window paper
and a torn hole. Why in plan.md.

    python3 -I mkspec.py                       # -> spec.json (2 shots, 4 jobs, 28 s)
    python3 -I mkjobs.py <live>/fix4           # -> <live>/fix4/prompts/*.txt, retake.json, colab-jobs.json

Each prompt is written whole here (the outer frame and the closing sentences are the d1 ones); the job (mode, size, seconds)
is the d1 9351101 job. Seeds 935124x (e935refine.sh's SRC table maps '124' to fix4).

- s24 (fix3 9351234 still looks into the lens 3-7 s and grins in two frames): e934 fix4 s32's way -- no face picture, no name,
  a costume sentence; his back square to the camera from the first frame, a sharp sleeve fling, then he strides off along the
  bank; the spoken line goes (a25 plays as the recording, voice_off s24); the only picture is fix3's free dry crop.
- s06 (fix3 kept the open window darkened): the window in the back wall is written as pale blank paper on a wooden lattice
  with a fist-sized torn hole in its lower right corner, Xu Yan pushing the balled grey cloth into the hole; the set picture
  is the plain brick wall crop (-qiang) instead of -chuang (whose open window with the night view is what the takes drew).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
CROP = "docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e935-live/fix3/set-hantian-yang-chen2-liu-gan.png"
REFS = "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live/"
HEAD3 = "For the target video, <Picture 1>, <Picture 2> and <Picture 3> are referenced throughout.\n\n"
STYLE = ("integrated_multimodal_description: [Shot 1] Photorealistic live-action film footage of real actors in an ancient "
         "Chinese (Song-dynasty) period drama, with the look of a feature film. ")
TAIL = "\noverall_soundscape: N/A\nnon_diegetic_music: N/A\n"
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"

S24 = ("For the target video, <Picture 1> is referenced throughout.\n\n" + STYLE +
       "The one man in this shot is a short, portly man of fifty, filmed from behind him, in an ancient Chinese Song-dynasty "
       "rich landlord's dark gold silk cross-collared robe woven with small round medallions, with long wide sleeves and a "
       "black belt, and a small round black cap; the location shown in <Picture 1> is the set, keeping its layout: the big old "
       "tree and the dry furrowed fields behind it. Initial composition: On the three small fields of Liuxi at dawn the next "
       "morning, on the grassy bank under the big old tree, the dry cracked fields of the drought spreading beyond it; soft "
       "grey-gold dawn light, a thin white mist lying low over the ground: medium-wide shot from behind him on the grassy "
       "bank, framed from the knees up with clear space above his cap: the portly man stands left of the middle of the frame "
       "with his broad back square to the camera from the first frame, the back of his cap, the back of his thick neck and "
       "his rounded shoulders in dark gold silk toward the camera, his head facing straight away from the camera toward the "
       "trunk of the big old tree at the right; he is the only person in the frame; stung and sulking: his shoulders hunched "
       "up stiff, his fists clenched at his sides, his head jutting forward; in front of him, soft, the grassy bank running "
       "away to the trunk of the big old tree, and beyond it only dry cracked brown earth in bare furrows reaching to the far "
       "hills under a thin low mist; their hands hold only what is described here. No second copy of anyone appears. The "
       "picture fixes the place and its light only, never the mood. The portly man stands still for a breath, his shoulders "
       "rising; then he flings his right wide sleeve out hard to the side and back with one sharp angry shake that snaps the "
       "silk, and strides away from the camera with quick heavy steps along the grassy bank toward the big old tree, his "
       "broad back square to the camera the whole shot, his fists clenched at his sides, his stiff shoulders jerking with "
       "each step, the back of his cap toward the camera; by the end of the shot he has walked well into the distance in the "
       "right third of the frame, smaller against the trunk of the tree, still walking away, and the soft grey-gold dawn "
       "light stays unchanged. The camera holds a static shot. One continuous shot. The picture is clean, with no subtitles, "
       "captions or text anywhere on screen; a thin white mist lying low over the ground, a clean natural film image. "
       "Natural, realistic human motion of a real actor: the weight of his heavy body moves with each angry step, and the "
       "gold silk folds and swings over his back and sleeves." + TAIL)

XU = ("Xu Yan shown in <Picture 1> and <Picture 2> (the same man from several angles) keeps exactly the same face, hair and "
      "costume as the pictures: East Asian young man of twenty-five, clean-cut handsome with thick brows, double-lidded bright "
      "eyes, straight nose and a firm mouth, tall and lean with broad shoulders, black hair gathered up into a topknot on the "
      "crown and tied with a cloth band, a few strands falling over his forehead, a faded blue-grey cotton scholar's robe "
      "patched at one elbow, cloth shoes; ")
S06 = (HEAD3 + STYLE + XU +
       "the earthen brick wall shown in <Picture 3> is the wall of the room, its bricks and its warm light. Initial "
       "composition: Inside the farmhouse of the Xu family late at night on the tenth day of the drought, by the small window "
       "in the back wall; the one small warm flame on the table the only light, the corners of the room deep in shadow: "
       "medium shot by the small window in the earthen brick back wall: the small square window is covered with pale "
       "off-white window paper pasted over a plain wooden lattice, the paper blank and smooth, faintly lit on the inside by "
       "the warm flame and dark behind it, and in the lower right corner of the window a ragged hole the size of a fist torn "
       "through the paper, black night showing through the hole; Xu Yan, in his faded blue-grey scholar's robe patched at one "
       "elbow with an old grey cloth outer coat worn loose over his shoulders, dark shadows under his eyes, standing side-on "
       "at the window, framed from the waist up, his right hand already holding a balled-up piece of old grey cloth against "
       "the torn hole from the first frame, his face turned three-quarter to screen right over his shoulder toward someone "
       "out of sight beyond the right edge of the frame, never the lens; that side of the frame is only the earthen brick wall "
       "in the warm light of the one small flame all the way to the edge, and he is the only person in the frame; gentle and "
       f"steady: brows easing, lips moving softly between words, {NOSMILE}; their hands hold only what is described here. No "
       "second copy of anyone appears. Facial expressions follow the action and lines described below, not the reference "
       "pictures: the pictures fix the face, hair and costume only, never the mood. Xu Yan speaks a short Mandarin line, "
       "「別怕，哥把洞堵上，蝗蟲進不來」, his lips moving evenly with every syllable in small natural talking mouth shapes, "
       f"{NOSMILE}, his face turned three-quarter to screen right over his shoulder toward someone out of sight beyond the "
       "right edge of the frame, his eyes on that spot, never looking at the camera; as he speaks his fingers push the grey "
       "cloth into the torn hole bit by bit, the paper around the hole crinkling and giving under his knuckles, until the "
       "cloth fills the hole and he presses it flat once with his palm, the rest of the window paper staying whole and blank, "
       "and the warm light of the one small flame stays unchanged. The camera pushes in with small amplitude at slow speed. "
       "One continuous shot. The picture is clean, with no subtitles, captions or text anywhere on screen; the air is clear "
       "and still, a clean natural film image. Natural, realistic human motion and acting of real actors: each person keeps "
       "the identity, hair and costume of their reference pictures, while every visible face acts the emotion written above "
       "and changes with it; the pictures are neutral studio portraits, never copy their blank expression." + TAIL)

S = {"s24": {"base": "d1 s24-9351101", "seeds": [9351241, 9351242], "duration_seconds": 8, "text": S24, "pictures": [CROP]},
     "s06": {"base": "d1 s06-9351101", "seeds": [9351243, 9351244], "duration_seconds": 6, "text": S06,
             "pictures": [REFS + "xuyan-portrait-l1.png", REFS + "angles/xuyan-angle-a-l1.png", REFS + "set-xujia-wu-ye-qiang-l1.png"]}}
(HERE / "spec.json").write_text(json.dumps({"base": "d1 jobs; prompts written whole", "shots": S}, ensure_ascii=False, indent=1)
                                + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", "(28 s)")
