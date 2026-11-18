"""e932 fix1: the retakes of picks-merged.tsv, merged from review-picks-a/b by the merge agent (2026-11-18). NOT RUN: these
are written and checked (retake.py, mkjobs.py, preflight-prompts.py, check_manifest.py, h3r.sh check), nothing is sent.
Same steps as e931 fix1: retake.py from live/st1 (the d1 edits of e932-live/spec.json are applied first, then these), mkjobs.py
for the duration, the absolute picture paths, output_path and the scans, then preflight-prompts.py. Seeds 9321201/9321202
(episode, 12, seed), each shot bought at its d1 length.

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1            # writes colab-jobs.json (all 6 jobs)
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

All three are priority 1 (cutting cannot save them). Why, shot by shot, in plan.md. The rules followed (route-a.md, e930/e931
fix1): positive descriptions, no negated object noun; the head count written as a number and where the row ends; a back shot
written as the back of the head and the topknot of Wang Erniu's final look (erniu-portrait-l1: black hair in one small round
topknot on the crown); no smile word except the d1 "not smiling" and the season's NOSMILE sentence, with a concrete hard face
written next to it; nobody named who is not in the frame.

- s01 (A and B): the big man in the lower left showed a round, crew-cut side face 0.3-3.2 s (not Erniu's long face and
  topknot; A: in 1102 a full profile), the retainers stood in a row of 25 or more running out of the frame (e931 s41: about
  14), and the hoe was not knocked away (1101 it became a long pole in Qin Shuang's hands; 1102 he shouldered it again). Now:
  his back square to us, his topknot written, only the back of his head and his ear rims; "a short row of exactly fourteen"
  that ends a little left of the middle with bare water and the bamboo hill beyond the last man; the result of the jerk
  written first: the hoe leaves his hands and flies out past the upper left corner (nothing left in the frame for the model to
  hand over), his empty hands stay up, the pole stays in her two hands. The hoe lands out of the frame; s04 pulls it out of
  the earth, which still reads.
- s19 (A; B picked 1102, the coordinator looked frame by frame): Wang Erniu smiles in both takes while Qin Shuang speaks
  (1101 an open laugh 0-3 s; 1102 a closed smile 1.4-2.9 s right over her line, Qin Shuang herself smiling at 2.4 s), with
  Xu Yan lying senseless at the bottom of the pit. d1 had only "his lips pressed shut, not smiling". Now: a hard worried face
  written by its parts plus NOSMILE for him, NOSMILE for her too; the two of them one behind the other on the same rope, both
  facing the pit at the left, and he hauls with her.
- s25 (A and B): 1101 has two Qin Shuangs from the first frame; in 1102 they walk toward the camera, Qin Shuang leaves the
  frame at 4.1-5.5 s and the end is Erniu alone, smiling (4.4/4.5 s on). The usable 4.1-4.4 s cannot hold a22+a23 (about
  5.4-5.6 s with the pause). Now: the camera to the side of the row, the two walkers side-on in the middle distance, whole and
  small to the last frame, walking from the right half toward the left; "the only woman in the frame"; exactly two walking;
  Erniu's face by its parts plus NOSMILE.
Fallbacks are in ../picks-merged.tsv and fix1/review-picks.tsv.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ST1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e932-dh/runpod/live/st1")
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
P1 = ("s01", "s19", "s25")
P2 = ()


def d1(sid):
    return json.loads(json.dumps({k: v for k, v in D1SPEC[sid].items()
                                  if k in ("drop_pictures", "drop_set", "swap_pictures", "replace")}))


def d1text(sid):
    text = (ST1 / "prompts" / f"ref-{sid}.txt").read_text(encoding="utf-8")
    for old, new in D1SPEC[sid].get("replace", []):
        assert old in text, (sid, old[:60])
        text = text.replace(old, new)
    return text


def once(sid, s):
    assert d1text(sid).count(s) == 1, (sid, s[:60])
    return s


S = {sid: d1(sid) for sid in P1 + P2}
for sid in S:
    S[sid].setdefault("replace", [])

# s01: Erniu's back with his topknot, fourteen retainers in a short row, the hoe flies out of the frame.
S["s01"]["replace"] += [
    [once("s01", "one big young man seen only from behind, turned a little away from us toward the right, in a coarse brown "
                 "cross-collared short jacket with the sleeves rolled up,"),
     "one big young man seen only from behind, his broad back square to us, in a coarse brown cross-collared short jacket "
     "with the sleeves rolled up, his black hair tied up in one small round topknot on the crown of his head,"],
    [once("s01", "the back of his head toward us the whole shot;"),
     "the back of his head and his topknot toward us from the first frame to the last, only the back of his head and the rims "
     "of his ears in view the whole shot;"],
    [once("s01", "from just right of the middle of the frame away to the left, the nearest at the right the tallest and the "
                 "farther ones smaller and smaller, fourteen men in identical"),
     "a short row of exactly fourteen men from just right of the middle of the frame away to the left, the nearest at the "
     "right the tallest and the farther ones smaller and smaller, the row ending with the fourteenth man a little left of the "
     "middle of the frame and beyond him only bare muddy water and the bamboo hill; the fourteen men are in identical"],
    [once("s01", "Qin Shuang jerks the carrying pole sharply upward: the hoe is knocked out of the young man's hands, flies up "
                 "and away to the left and drops blade first, sticking in the earth of the path at the left edge of the frame;"),
     "Qin Shuang jerks the carrying pole sharply upward under the hoe handle: the hoe leaves the young man's hands and flies "
     "away up out of the frame past the upper left corner, and his two empty hands stay up above his head; the carrying pole "
     "stays in Qin Shuang's two hands the whole shot;"],
]

# s19: a hard worried face for him (and NOSMILE for both), one behind the other on the same rope, both hauling.
S["s19"]["replace"] += [
    [once("s19", "medium shot at the rim of the near well pit, both framed from the waist up, side-on to us, the rope running "
                 "taut from the dark pit at the left:"),
     "medium shot at the rim of the near well pit, both framed from the waist up, side-on to us, the two of them one behind "
     "the other along the same rope, both facing screen left, the rope running taut from the dark pit at the left:"],
    [once("s19", "both hands already on the rope, his face in profile to screen left, his lips pressed shut, not smiling, "
                 "never the lens;"),
     "both hands already on the rope, his face in profile to screen left toward the dark pit, not smiling: his face hard with "
     f"worry, brows drawn together, jaw clenched, lips pressed together in one flat line, {NOSMILE}, never the lens;"],
    [once("s19", "commanding, not smiling: brows drawn, eyes hard, lips moving fast between words;"),
     f"commanding and urgent: brows drawn, eyes hard, lips moving fast between words, {NOSMILE};"],
    [once("s19", "Qin Shuang braces her boots on the earth and leans back hard on the rope as she speaks;"),
     "Qin Shuang braces her boots on the earth and leans back hard on the rope as she speaks, and Wang Erniu in front of her "
     "leans back hard with her, the two of them hauling the rope toward the right;"],
]

# s25: side-on, small, whole in the frame to the last frame; one woman; Erniu's face by its parts.
S["s25"]["replace"] += [
    [once("s25", "wide shot from a little above standing eye height, like the picture, along the row of earth heaps: Qin "
                 "Shuang,"),
     "wide shot from a little above standing eye height, the camera to the side of the row of earth heaps, the two walkers "
     "side-on to us in the middle distance, whole and small in the frame from the first frame to the last: Qin Shuang, the "
     "only woman in the frame,"],
    [once("s25", "striding toward the left edge of the frame, her face in profile to screen left, her lips pressed shut, "
                 "never the lens;"),
     "walking steadily from the right half of the frame toward the left, side-on to us, her face in profile to screen left, "
     "her lips pressed shut, never the lens;"],
    [once("s25", "one bamboo water tube with a rope handle in his right hand, his lips pressed shut, not smiling, never the "
                 "lens;"),
     "one bamboo water tube with a rope handle in his right hand, side-on to us, his face in profile to screen left, his eyes "
     "on the man she carries, not smiling: brows knotted with worry, lips pressed together in one flat line, "
     f"{NOSMILE}, never the lens;"],
    [once("s25", "exactly three people, the man over her shoulder seen only from behind."),
     "exactly three people: two walking, Qin Shuang with the man over her right shoulder and Wang Erniu behind her, the man "
     "over her shoulder seen only from behind."],
    [once("s25", "The two of them walk on at the same pace toward the left;"),
     "The two of them walk on slowly at the same pace toward the left, side-on to us, both staying whole in the frame in the "
     "middle distance to the last frame;"],
]

DUR = {"s01": 5, "s19": 6, "s25": 8}  # the d1 lengths (r2.py BUY)
for sid in S:
    S[sid]["duration_seconds"] = DUR[sid]

(HERE / "spec.json").write_text(json.dumps({"seeds": [9321201, 9321202], "priority_1": list(P1), "priority_2": list(P2),
                                            "shots": S}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
