"""e934 fix4: s32 Qian Yuanwai as a shot of his back (he walks off), the line played off screen. Why in plan.md.

    python3 -I mkspec.py                       # -> spec.json (1 shot, seeds 9341511/9341512)
    python3 -I mkjobs.py <live>/fix4           # -> <live>/fix4/prompts/*.txt, retake.json, colab-jobs.json (2 jobs, 16 s)

Base: fix1 9341211, job and prompt exactly as sent (sha256 checked by mkjobs.py); it is the take in the cut now.
Three rounds, six takes (fix1 1211/1212, fix2 1313/1314, fix3 1417/1418) never gave no-smile + walking off + the dry field
together: whenever his face is on screen while he talks, the model gives him a grin (fix3 plan.md lesson). The e918 fix2 s37
way (task file, 2026-11-16: "不送臉部圖、不點名，從身後拍…畫外放錄音——第一次就成功") is used here:
- his face pictures (portrait, angle-a) are dropped and his name is out of the draft prompt: a costume sentence instead;
  the only picture is the field set, cropped free of charge to its left 940 px (fix4/set-hantian-liu-zuo.png: furrows, far
  hills, the big old willow; the golden ripe field right of the trunk is cut away -- it is where fix2/fix3's "whole golden
  rice field" came from);
- he is seen from behind from the first frame to the last, flings his sleeve in the first second and strides off toward the
  willow; the spoken-line sentence is gone (a31 plays as a recording, voice_off s32);
- "never the mood. " stays once (refine-prep.py cuts the motion text there), in a sentence about the picture fixing the
  place; the motion text avoids "seen only from behind" / "back to us" (e934refine.sh step 3 allows those in s05 s06 only).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
LIVE = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/runpod/live")
BASE = ("fix1", 9341211)
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
CAP = "a tall round smooth black cap"


def basetext():
    return (LIVE / BASE[0] / "prompts" / f"ref-s32-{BASE[1]}.txt").read_text(encoding="utf-8")


def once(s):
    assert basetext().count(s) == 1, s[:70]
    return s


R = [
    [once("For the target video, <Picture 1>, <Picture 2> and <Picture 3> are referenced throughout."),
     "For the target video, <Picture 1> is referenced throughout."],
    [once("Qian Yuanwai shown in <Picture 1> and <Picture 2> (the same man from several angles) keeps exactly the same face, "
          "hair and costume as the pictures: East Asian man of fifty, short and portly, round face, a thin eight-shaped "
          "moustache, small narrow eyes under heavy brows, an ancient Chinese Song-dynasty rich landlord's dark gold silk "
          "cross-collared robe woven with small round medallions and a small black cap, three gold rings on his fingers; the "
          "location shown in <Picture 3> is the set, keeping its layout and props."),
     "The one man in this shot is a short, portly man of fifty, filmed from behind him, in an ancient Chinese Song-dynasty "
     "rich landlord's dark gold silk cross-collared robe woven with small round medallions, with long wide sleeves and a "
     f"black belt, and {CAP}; the location shown in <Picture 1> is the set, keeping its layout and props: the dry furrowed "
     "field on the left, the big old willow on the right, the far hills behind."],
    [once("medium shot on the grassy bank under the big old tree, framed from the waist up: Qian Yuanwai, short and portly with "
          "a round face and a thin eight-shaped moustache, in his dark gold silk robe woven with small round medallions, the "
          "front of the robe plain brocade, three gold rings on his fingers, already walking away toward the right edge of the "
          "frame from the first frame, his back three-quarter to the camera, his head turned back over his right shoulder, his "
          "face in profile looking back down toward the field beyond the lower left edge of the frame, never the lens; he is "
          "the only person in the frame; sour and dark: his face fallen, brows pulled down hard, the corners of his mouth "
          f"pulled down, jaw clenched, lips tight and moving hard between words, {NOSMILE}; behind him, soft, the trunk of the "
          "big old tree and the far hills in the low golden sunset light;"),
     "medium-wide shot from behind him on the grassy bank at the edge of the field, framed from the knees up with clear space "
     "above his cap: the portly man stands left of the middle of the frame with his broad back square to the camera from the "
     "first frame, the back of his cap, the back of his thick neck and his rounded shoulders in dark gold silk toward the "
     "camera, his head facing straight away from the camera toward the big old willow at the right; he is the only person in "
     "the frame; stung and furious: his shoulders hunched up stiff, his fists clenched at his sides, his head jutting forward; "
     "in front of him, soft, the grassy bank running away to the trunk of the big old willow at the right, and on the left "
     "the dry, cracked brown furrows of the empty field reaching to the far hills under the low golden sunset light;"],
    [once("Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the "
          "face, hair and costume only, never the mood. "),
     "The picture fixes the place and its light only, never the mood. "],
    [once("Qian Yuanwai speaks a short Mandarin line, 「哼，有水算什麼。田裡長不出糧，一樣得求我」, his lips, jaw and cheeks "
          "moving clearly with every syllable in natural talking mouth shapes, his head turned back over his right shoulder, "
          "his eyes on the field beyond the lower left edge of the frame, looking back down to the lower left, never looking "
          "at the camera; By the last word Qian Yuanwai has walked on into the right third of the frame, his back still "
          "three-quarter to the camera and his head still turned back over his right shoulder: in the first second he gives "
          "his right sleeve one sharp shake behind him, then he keeps walking slowly and steadily toward the right edge and "
          "throws the words back over his shoulder as he goes, and the low golden sunset light stays unchanged."),
     "In the first second the portly man flings his right wide sleeve out hard to the side and back with one sharp angry "
     "shake, then strides away from the camera with quick heavy steps along the grassy bank toward the big old willow at the "
     "right, his broad back square to the camera the whole shot, his fists clenched at his sides, his stiff shoulders jerking "
     "with each step, his head facing straight ahead away from the camera, the back of his cap toward the camera; by the end "
     "of the shot he has walked well into the distance in the right third of the frame, smaller against the trunk of the "
     "willow, still walking away, and the low golden sunset light stays unchanged."],
    [once("Natural, realistic human motion and acting of real actors: each person keeps the identity, hair and costume of "
          "their reference pictures, while every visible face acts the emotion written above and changes with it; the "
          "pictures are neutral studio portraits, never copy their blank expression."),
     "Natural, realistic human motion of a real actor: the weight of his heavy body moves with each angry step, and the gold "
     "silk folds and swings over his back and sleeves."],
]
SET = str(HERE / "set-hantian-liu-zuo.png")
S = {"s32": {"base": f"{BASE[0]} s32-{BASE[1]}", "seeds": [9341511, 9341512], "duration_seconds": 8, "replace": R,
             "reference_images": [SET]}}
(HERE / "spec.json").write_text(json.dumps({"base": "fix1 9341211 as sent", "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shot ->", HERE / "spec.json", "(16 s)")
