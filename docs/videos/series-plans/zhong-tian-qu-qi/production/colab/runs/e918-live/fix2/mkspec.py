"""e918 fix2: s37 once more, as a shot of Qian Yuanwai's back. Same flow as fix1: retake.py from live/st1, mkjobs.py for the
duration, the absolute picture paths and output_path, the bible 拍法 18 negative-noun scan, then preflight-prompts.py.
Seeds 9181301/9181302, 6 s (a36 is 5.92 s; a 6 s job is 158 frames = 6.583 s).

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix2 spec.json
    python3 -I mkjobs.py <live>/fix2
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix2/colab-jobs.json

Why (coordinator, 2026-11-16): fix1's s37 (9181201, 9181202) and d1's fallback 9181102 all grin with teeth while he begs
(1202: 0.00-1.75, 2.88-4.13, a flash of teeth 5.50-5.75; 1201: 0.25-2.00, 3.00-4.13, 5.63-6.50; the longest stretch with no
grin is 1.1 s, a36 needs 5.92 s). a36 is an off-screen line (畫外), so the mouth need not be seen: the face leaves the shot.
- From behind him and a little above: his back on the stone floor of the court hall, the tall round smooth black cap, the
  gold robe over his back and both shoulders, the upper body bowing forward toward the dais at the top of the frame, once,
  then lower a second time; both hands in front of his belly, covered from the camera by his own back.
- Bible 拍法 2 (an over-the-shoulder foreground is not named and gets no picture: s35 fix1 1202 drew his back with no face from
  text alone): Qian's three pictures are dropped and his name is out of the prompt (the identity clause is replaced by a
  costume sentence); the only picture is the court-hall floor, set-xianya-gongtang-floor-l1, as in s31/s33 (absolute path).
- The spoken-line sentence is gone (the recording plays off screen; 拍法 15); nothing in the text asks for a face.
- 拍法 18: everything written as what is there; no negated nouns (mkjobs.py scans for them).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FLOOR = ("/home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live/"
         "set-xianya-gongtang-floor-l1.png")
CAP = "tall round smooth black cap, plain and smooth all the way round down to its rim"

R = [
 ["Qian Yuanwai shown in <Picture 1>, <Picture 2> and <Picture 3> (the same man from several angles) keeps exactly the same "
  "face, hair and costume as the pictures: East Asian man of fifty, short and portly, round face, a thin eight-shaped "
  "moustache, small shrewd eyes, an ancient Chinese Song-dynasty rich landlord's dark gold silk cross-collared robe with "
  "roundel patterns and a small black cap, three gold rings on his fingers; the location",
  "The one man in this shot is seen only from behind: a short, portly man in an ancient Chinese Song-dynasty rich "
  "landlord's dark gold silk cross-collared robe with roundel patterns and long wide sleeves, and a " + CAP + "; the location"],
 ["medium shot of Qian Yuanwai, in his dark gold silk cross-collared robe with roundel patterns and wide sleeves and his small "
  "black cap, kneeling, framed from the waist up with clear space above his cap, both his hands pushed deep inside his long "
  "wide dark gold sleeves, the cuffs hanging well past his fingertips, the two sleeves joined in front of his belly, his hands "
  "hidden inside them the whole time, his face tipped up three-quarter to screen left toward the high dais above the top of "
  "the frame, never the lens; pleading and sly: brows drawn up, eyes fluttering half shut, mouth drooping between words; "
  "behind him only a dark red-brown pillar and the grey daylight.",
  "medium shot from close behind the portly man and a little above him, looking down over his back toward the far end of "
  "the hall: he kneels on both knees in the middle of the grey stone floor, seen only from behind, framed from his knees up "
  "with clear space above his cap; the back of his " + CAP + " and the bare back of his thick neck below its rim, his broad "
  "back and both rounded shoulders in dark gold silk with roundel patterns fill the middle of the frame, his long wide gold "
  "sleeves hanging straight down along both sides of his body to the floor; his forearms and hands rest together against his "
  "belly in front of him, covered from the camera by his own broad back and shoulders; the back hem of his robe spreads over "
  "the stone tiles behind his knees; his head faces the far end of the hall and the high dais beyond the top of the frame; "
  "around him only the large grey stone tiles of the floor, and beyond him two thick round dark red-brown pillars and the "
  "tall dark lattice windows above a low white panel in the soft grey daylight."],
 ["He is the only person in the frame; no second copy of anyone appears.",
  "He is the only person in the frame, his back toward us; no second copy of anyone appears."],
 ["Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the face, "
  "hair and costume only, never the mood. ", ""],
 ["Qian Yuanwai speaks a short Mandarin line, 「大人，老夫頭暈得很，求您午後再審」, his lips, jaw and cheeks moving clearly "
  "with every syllable in natural talking mouth shapes, turned toward the person he is speaking to, face in profile or "
  "three-quarter profile, eyes on that person, never looking at the camera; Qian Yuanwai sways on his knees as if dizzy, "
  "presses his joined sleeves against his belly, then bows his head toward the dais; after the last word he stays bowed, his "
  "eyes sliding sideways,",
  "The kneeling man sways once to one side as if dizzy and steadies himself, then bows his whole upper body forward from the "
  "hips toward the dais, the top of his cap tipping toward the far end of the hall, rises halfway, and bows forward a second "
  "time, lower and slower, and stays there bowed low over his knees, his rounded shoulders trembling; the back of his cap, "
  "his neck and his broad gold back stay toward us the whole shot, his head toward the dais,"],
 ["Natural, realistic human motion and acting of real actors: each person keeps the identity, hair and costume of their "
  "reference pictures, while every visible face acts the emotion written above and changes with it; the pictures are "
  "neutral studio portraits, never copy their blank expression.",
  "Natural, realistic human motion of a real actor: the weight of his heavy body moves with each bow, and the gold silk "
  "folds and slides over his back and shoulders."],
]
S = {"s37": {
    "replace": R,
    "drop_pictures": ["qianyuanwai-portrait-l1.png", "qianyuanwai-angle-a-l1.png", "qianyuanwai-angle-b-l1.png"],
    "swap_pictures": {"set-xianya-l1.png": FLOOR},
    "duration_seconds": 6,
}}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9181301, 9181302], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shot ->", HERE / "spec.json")
