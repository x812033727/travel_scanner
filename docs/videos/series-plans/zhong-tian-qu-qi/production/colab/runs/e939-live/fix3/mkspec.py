"""e939 fix3: the shots REVIEW 2 could not save by editing (../cut-notes.md, REVIEW 2, "剪接救不了"; ../cut-review.md items 5, 6, 18).
Why, shot by shot, in plan.md.

    python3 -I mkspec.py                       # -> spec.json (3 shots, seeds 9391501/9391502)
    python3 -I mkjobs.py <live>/fix3           # -> <live>/fix3/prompts/*.txt, retake.json, colab-jobs.json (6 jobs, 34 s)
    python3 -I <scratchpad>/tools/check939f3.py <live>/fix3   # check939.py's assertions, rewritten for these three shots

Bases (the job and prompt exactly as sent, sha256 checked by mkjobs.py):
- s32: d1 9391101, the take in the cut (picks-final.tsv). Same pictures, framing, camera (the slow push the pick has) and 6 s;
  only the face changes: frightened, the voice small, lips trembling, eyes wide and wet, NOSMILE (REVIEW 2: she reads excited,
  smiling at 203.0-204.0; the d1 words "scared and trying hard to remember" gave a bright, eager face).
- s39: fix1 9391302, the take in the cut. fix1's spear (upright, whole, head at the top) and static camera stay; the people of the
  village are written in the foreground as backs and shoulders crowding the left edge and the lower left corner (four of the
  s36 ten, the same clothes), the slack rope in the foreground is gone and the noose is written round his neck from the first
  frame to the last, and the stillness gets real motion (the four shift and lean, Diao Qi swallows and lifts his eyes once).
- s40b (new shot, 5 s bought, 1.5-2 s used after s40): the people of the village seen from behind turn their heads all at once
  toward the path at the right edge of the frame, where someone is coming (Xu Yan, who is not in the frame and not named:
  e940 brings him in). Nobody faces the camera, nobody speaks; no person picture, only the whole barn-front picture
  set-gucang-wai-l1 (s36's): its strip of trampled earth runs out at the lower right edge, the path. The job's fields come from
  the d1 s36 job; the prompt is written whole here, in the d1 shots' sentence order (style sentence, set clause, place and light,
  composition, count twice, the "never the mood. " separator in a place sentence as e934 fix4 / fix1 s38, motion, camera, "One
  continuous shot.", clean picture). Collective nouns stay out (check939: villagers, crowd): "people of the village".
Seeds: 93915xx is new for e939 (9391201-04 Qwen door, 93913xx fix1, 93914xx fix2 and its Qwen).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
LIVE = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e939-dh/runpod/live")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = [9391501, 9391502]


def basetext(rnd, sid, seed):
    return (LIVE / rnd / "prompts" / f"ref-{sid}-{seed}.txt").read_text(encoding="utf-8")


def once(base, s):
    assert basetext(*base).count(s) == 1, (base, s[:80])
    return s


S = {}

# s32 ------------------------------------------------------------------------------------------------------------------------
B32 = ("d1", "s32", 9391101)
S["s32"] = {"base": list(B32), "duration_seconds": 6, "replace": [
    [once(B32, "scared and trying hard to remember, not smiling: brows pinched, lips moving in a small careful voice between words;"),
     "frightened, not smiling: her eyes wide and wet with held-back tears, her brows drawn up together in the middle, her lips "
     "trembling and moving in a small, shaking voice between words, her shoulders drawn up and small, " + NOSMILE + ";"],
    [once(B32, "then touches her palm under her chin where a cord would tie, and the grey first light stays unchanged."),
     "then touches her palm under her chin where a cord would tie, her face staying frightened and her lips trembling to the "
     "last frame, and the grey first light stays unchanged."],
]}

# s39 ------------------------------------------------------------------------------------------------------------------------
B39 = ("fix1", "s39", 9391302)
FOLK4 = ("the backs of the heads and the shoulders of four people of the village crowding the left edge and the lower left "
         "corner of the frame, seen only from behind and soft, facing her: a thin middle-aged man in charcoal grey, a stout man "
         "of fifty in dark olive green, a middle-aged woman in dark grey with a faded indigo head cloth and a broad-backed man of "
         "about forty in an undyed hemp short jacket and a cloth head wrap")
S["s39"] = {"base": list(B39), "duration_seconds": 6, "replace": [
    [once(B39, "wide shot on the trampled earth before the barn, the slack neck rope crossing soft in the lower foreground:"),
     "wide shot on the trampled earth before the barn: in the foreground, " + FOLK4 + ";"],
    [once(B39, "her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; "
               "that side of the frame is only the trampled earth and the green rice field all the way to the edge, and no one "
               "else stands on that side;"),
     "her face three-quarter to screen left toward the four people of the village in the foreground at the left, never the lens;"],
    [once(B39, "one thick hemp rope looped round his neck, kneeling on the trampled earth,"),
     "one thick hemp rope looped round his neck, pulled tight round his neck as a noose from the first frame to the last, its "
     "loose end falling down over his chest, kneeling on the trampled earth at the right, clear of the four in the foreground,"],
    [once(B39, "exactly two people. Only these 2 people are in the frame;"),
     "exactly six people, the four people of the village in the foreground seen only from behind. Only Qin Shuang, Diao Qi "
     "and the four people of the village in the foreground seen from behind are in the frame;"],
    [once(B39, "her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, her eyes on "
               "that spot, never looking at the camera;"),
     "her face three-quarter to screen left toward the four people of the village in the foreground, her eyes on them, never "
     "looking at the camera;"],
    [once(B39, "the spear never turning and never shortening, to the last frame;"),
     "the spear never turning and never shortening, to the last frame; all through the shot the four people of the village in "
     "the foreground shift on their feet and lean in toward Diao Qi, one of them turning his head to the next, and Diao Qi "
     "swallows once and lifts his eyes to her for a moment, then lowers them, the noose round his neck;"],
    [once(B39, "Qin Shuang wears her leather boots and Diao Qi wears worn straw sandals."),
     "Qin Shuang wears her leather boots, Diao Qi wears worn straw sandals, and everyone else wears dark cloth shoes."],
]}

# s40b -----------------------------------------------------------------------------------------------------------------------
FOLK6 = ("an old man with a white topknot in a faded grey long robe, a thin middle-aged man in charcoal grey, a boy of fifteen in "
         "faded indigo, a stout man of fifty in dark olive green, a middle-aged woman in dark grey with a faded indigo head cloth "
         "and a broad-backed man of about forty in an undyed hemp short jacket and a cloth head wrap")
TEXT40B = (
    "For the target video, <Picture 1> is referenced throughout.\n\n"
    "integrated_multimodal_description: [Shot 1] Photorealistic live-action film footage of real actors in an ancient Chinese "
    "(Song-dynasty) period drama, with the look of a feature film. The location shown in <Picture 1> is the set, keeping its "
    "layout and props. Initial composition: Before the old plank barn at the edge of the Liuxi fields in the early morning of "
    "the next day: the place exactly as in the picture: the low old barn of grey weathered planks at the right under its "
    "pitched plank roof, its two plank door leaves swung back flat against its front on both sides of the dark doorway, a broad "
    "strip of trampled sun-warmed earth before it running out of the frame at the lower right edge, the path from the village, "
    "the flooded field of young green rice seedlings across the left half of the frame, small village houses and low blue "
    "hills far away, one big tree behind the barn; low warm golden morning sunlight from the right, long shadows across the "
    "trampled earth, a clear pale blue sky: medium-wide shot from behind six people of the village standing in a loose row "
    "across the frame on the trampled earth with their backs to the camera, facing the barn, framed from the waist up: " + FOLK6
    + ", all six seen only from behind, the backs of their heads and their shoulders toward the camera from the first frame; "
    "beyond them, soft, the grey plank barn and its dark doorway; at the lower right edge of the frame the empty path of "
    "trampled earth; their hands hold only what is described here; exactly six people, all seen only from behind. Only the six "
    "people of the village seen from behind are in the frame; no second copy of anyone appears. The picture fixes the place "
    "and its light only, never the mood. In the middle of the shot all six turn their heads at the same moment toward the path "
    "at the lower right edge of the frame, as if someone is coming along it, their shoulders following a little after their "
    "heads, and they stay turned toward the right edge of the frame to the last frame, every one of them still turned away "
    "from the camera, only the backs of their heads and at most the edge of a cheek in view; all six stay silent, and the low "
    "warm morning sunlight stays unchanged. The camera holds a static shot. One continuous shot. The picture is clean, with no "
    "subtitles, captions or text anywhere on screen; the fresh still air of early morning, a clean natural film image. Natural, "
    "realistic human motion of real actors, their heads and shoulders turning together.\n"
    "overall_soundscape: N/A\n"
    "non_diegetic_music: N/A")  # no trailing newline, as the d1 prompt files
S["s40b"] = {"base": ["d1", "s36", 9391101], "duration_seconds": 5, "pictures": ["set-gucang-wai-l1.png"], "text": TEXT40B}

(HERE / "spec.json").write_text(json.dumps({"seeds": SEEDS, "shots": S}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({sum(v['duration_seconds'] for v in S.values())} s per seed, "
      f"{2 * sum(v['duration_seconds'] for v in S.values())} s)")
