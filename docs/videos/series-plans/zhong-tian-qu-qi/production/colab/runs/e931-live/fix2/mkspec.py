"""e931 fix2: s20, s40, s22 once more, from the fix1 picks (fix1/review-picks.tsv: s20 9311202, s40 9311202, s22 9311202),
owner 2026-11-18 「該修就修，品質比較重要」. Written 2026-11-18, NOT run (paid Colab; the send script is the scratchpad's
e931f2.sh, session zt-live2 so it can run beside e930 fix3 on zt-live).
Same steps as fix1: retake.py from live/st1, with the d1 edits and fix1's edits of these three shots applied first, unchanged
from ../fix1/spec.json (this script checks that they rebuild fix1's prompt files byte for byte), then the fix2 edits below.
mkjobs.py for the absolute pictures, output_path and the scans, then preflight-prompts.py and h3r.sh check. Seeds
9311301/9311302 (fix<N> = 9311(N+1)xx), each shot bought at its d1/fix1 length.

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix2 spec.json
    python3 -I mkjobs.py <live>/fix2
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix2/colab-jobs.json
    bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix2/colab-jobs.json

Why, shot by shot, in plan.md (frames of the fix1 picks and of s21 9311101 checked 2026-11-18, scratchpad e931f2/*.jpg).
- s20: Xu Yan grins with teeth at 1.5-3.0 and 5.5-6.0 s in both seeds; the season's NOSMILE sentence did not hold (it held in
  e901 fix6 only with a medium close-up and no other motion). Now: no smile word at all (NOSMILE out too); his face in right
  profile, his eyes down on the covered bowl he is talking about, the face part by part (brows drawn together and low, mouth
  corners level and pulled flat, jaw firm, lips back into one straight line between words and after the last word, eyes on
  the bowl to the last frame). Tang Xiaotang drifted to the right two thirds and her buns touched the right edge after 5.5 s:
  s30 9311201 (the same hair and centre words) stayed dead centre because its right third was filled (Wang Erniu); here the
  right third gets the firewood stack and the bright gateway of the set picture, her head and shoulders the middle third with
  equal yard on both sides, headroom above the buns, and the camera holds still (the push carried her into the edge).
  Ribbons: two tails hung from a crossed tie; the band written as two flat snug turns with both ends under the turns.
- s40: Erniu stood in place the whole clip (c40: already charging in the first frame) and Xu Yan's arm reached to screen left,
  away from him. Now: first frame mid-stride with both feet off the path, body pitched forward; one action, the charge, in
  long heavy strides to the foot of the bank; the hoe's parts sentence of fix1 9311202 kept word for word (handle across his
  chest, blade end trailing at screen left, blade down, as 1202 drew it and as s39 carries it); Xu Yan in the left third
  turned to screen right, his right arm and hand reaching toward screen right at Erniu's back. "not smiling" goes:
  Erniu's face is fierce part by part, Xu Yan's alarmed part by part. Static camera (a push on a man running to the right
  edge crops him).
- s22: a two-leaf green shoot stood up in the middle of the bowl and grew taller (5 s on). Now the bowl is written from s21
  9311101's real frames: filled level to just below the rim with golden-brown unhusked seeds, about ten short thin pure
  white sprouts each one grain long lying flat on the seeds against their own grains, scattered evenly; the seeds and
  sprouts keep their size to the last frame. No negated noun. Tang Xiaotang centred as in s20. Xu Yan's closed-mouth
  warmth is kept (the pick review accepts it here).
"""
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
LIVE = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e931-dh/runpod/live")
ST1, FIX1DIR = LIVE / "st1", LIVE / "fix1"
FIX1 = json.loads((HERE.parent / "fix1" / "spec.json").read_text(encoding="utf-8"))["shots"]
PICK = {"s20": 9311202, "s40": 9311202, "s22": 9311202}  # fix1/review-picks.tsv
SHOTS = ("s20", "s40", "s22")


def norm(t):
    return re.sub(r"(<Picture \d+>(, | and )?)+( \(the same [^)]*\))?", "<P>", t)


def fix1text(sid):
    text = (ST1 / "prompts" / f"ref-{sid}.txt").read_text(encoding="utf-8")
    for old, new in FIX1[sid]["replace"]:
        assert old in text, (sid, old[:60])
        text = text.replace(old, new)
    picked = (FIX1DIR / "prompts" / f"ref-{sid}-{PICK[sid]}.txt").read_text(encoding="utf-8")
    # retake.py renumbers the pictures after drop_pictures; everything else must be fix1's prompt byte for byte (mkjobs.py
    # checks the built fix2 prompts against fix1's files exactly, with the fix2 edits undone)
    assert norm(text) == norm(picked), f"{sid}: st1 + fix1 edits do not rebuild fix1's {PICK[sid]} prompt"
    return text


def once(sid, s):
    assert fix1text(sid).count(s) == 1, (sid, s[:60])
    return s


S = {sid: json.loads(json.dumps(FIX1[sid])) for sid in SHOTS}
for sid in SHOTS:
    S[sid]["replace"] = [list(p) for p in FIX1[sid]["replace"]]


# --- s20, s22: Tang Xiaotang dead centre (the right third filled as s30 9311201's was), the ribbons as flat bands -------------
BUNS_OLD = ("gathered up into just two round buns set high on her head, one bun on each side, one short pink silk ribbon wound "
            "tight round the base of each bun with its ends tucked in;")
BUNS_NEW = ("gathered up into just two big round buns set high on her head, one bun on each side, one short pink silk ribbon "
            "wound tight round the base of each bun with its ends tucked in, each ribbon lying flat as one narrow pink band of "
            "two snug turns, both its ends tucked under the turns, the round black outline of each bun clean above its band;")
CENTRE_OLD = ("standing on the cracked earth of the yard, dead centre of the frame from the first frame to the last, framed from "
              "the waist up, facing straight away from us;")
CENTRE_NEW = ("standing on the cracked earth of the yard, dead centre of the frame from the first frame to the last, her head "
              "and shoulders filling the middle third of the frame with the same width of yard at her left and at her right, "
              "the tops of her two buns a hand's width below the top edge of the frame the whole shot, framed from the waist "
              "up, facing straight away from us;")
RIGHT_OLD = "beyond them, soft, the dark doorway and the split firewood against the farmhouse wall in the hazy afternoon sun;"
RIGHT_NEW = ("in the right third of the frame, beyond her right shoulder and level with Xu Yan, the stack of split firewood "
             "against the farmhouse wall and the bright empty gateway of the yard with the cracked field beyond it, so that she "
             "stands exactly between Xu Yan in the left third and the firewood and gateway in the right third; beyond them, "
             "soft, the dark doorway of the farmhouse in the hazy afternoon sun;")
PUSH = "The camera pushes in with small amplitude at slow speed."
for sid in ("s20", "s22"):
    S[sid]["replace"] += [[once(sid, BUNS_OLD), BUNS_NEW], [once(sid, CENTRE_OLD), CENTRE_NEW], [once(sid, RIGHT_OLD), RIGHT_NEW],
                          [once(sid, PUSH), "The camera holds a static shot."]]

# --- s20: Xu Yan's face in profile, on the bowl, cold and intent, part by part; no smile word -------------------------------
S["s20"]["replace"] += [
    [once("s20", "his face three-quarter to screen right toward her, never the lens; quietly hopeful and steady: eyes bright, "
                 "brows level, lips moving evenly between words, no smile at any moment, not even at the end of the shot, until "
                 "the last frame;"),
     "his face in right profile, turned toward screen right, his eyes lowered to the covered bowl in his hands, never the "
     "lens; intent and serious, a farmer checking his seed: his brows drawn a little together and low over his eyes, his eyes "
     "steady on the bowl, the corners of his mouth level and pulled flat, his jaw firm, his lips parting only as far as each "
     "word needs and pressing back together into one straight flat line between words;"],
    [once("s20", "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person, "
                 "never looking at the camera; Xu Yan holds the covered bowl out a little toward her as he speaks;"),
     "his face in right profile, his eyes on the covered bowl, never looking at the camera; Xu Yan holds the covered bowl out a "
     "little toward her as he speaks, and after his last word his lips close into one straight flat line, his jaw firm, his "
     "eyes still on the bowl to the last frame;"],
]

# --- s22: the bowl as s21 9311101 shows it; the sprouts keep their size ----------------------------------------------------
S["s22"]["replace"] += [
    [once("s22", "one red clay bowl holding a layer of plump golden-brown unhusked rice seeds, a few of them each showing one "
                 "tiny white sprout tip no longer than the seed itself, held in both his hands at his chest,"),
     "one red clay bowl filled level to just below its rim with plump golden-brown unhusked rice seeds, held in both his hands "
     "at his chest, about ten short thin pure-white sprouts scattered evenly over the seeds, each sprout as long as one rice "
     "grain and as thin as a thread, lying flat on the seeds against its own grain, the surface of the seeds flat and level "
     "from rim to rim,"],
    [once("s22", "Her clasped hands rise from her waist to her chest in delight, only her forearms moving;"),
     "Her clasped hands rise from her waist to her chest in delight, only her forearms moving; the golden seeds and their short "
     "white sprouts lie still and flat in the bowl, each sprout keeping its one-grain length from the first frame to the "
     "last;"],
]

# --- s40: the charge from the first frame, the hoe of fix1 9311202 word for word, Xu Yan reaching to screen right -------------
HOE = ("a long straight wooden handle with one flat, broad, square iron blade set at a right angle across its top end, the same "
       "hoe he carries on his shoulder")
S["s40"]["replace"] += [
    [once("s40", "framed full figure, already running hard toward the right from the first frame, one farm hoe raised above his "
                 f"head in both hands: {HOE}, not smiling: jaw clenched, brows knotted, eyes fixed ahead, never the lens;"),
     "framed full figure in the middle of the frame, already in a full sprint toward screen right in the first frame: caught "
     "mid-stride with both feet off the path, his body pitched far forward, his front knee driving up and his rear foot kicked "
     f"up behind him, one farm hoe gripped in both hands across his chest: {HOE}, the blade end trailing behind him at screen "
     "left with the blade pointing down; his face fierce: jaw clenched, brows knotted, eyes fixed ahead on the bank of sacks, "
     "never the lens;"],
    [once("s40", "framed full figure, his right arm already stretched out after him, his lips pressed together until his line, "
                 "not smiling, never the lens;"),
     "framed full figure in the left third of the frame, his body and face turned toward screen right after Wang Erniu, his "
     "right arm already stretched straight out toward screen right, his right hand reaching palm out toward Wang Erniu's back, his "
     "left arm at his side; alarmed: his brows drawn up and together, his eyes wide on Wang Erniu's back, his lips pressed "
     "together until his line, never the lens;"],
    [once("s40", "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person, "
                 "never looking at the camera;"),
     "his face in right profile toward Wang Erniu's back, his eyes on him, never looking at the camera;"],
    [once("s40", "Wang Erniu charges on toward the bank of sacks at the right, the hoe held high, shouting his line once and then "
                 "running on with his jaw clenched and his lips pressed together;"),
     "Wang Erniu charges on toward the bank of sacks at the right in long, heavy strides, his feet pounding the path and "
     "kicking up dust, his body leaning forward, the hoe gripped across his chest, shouting his line once and then running on "
     "with his jaw clenched and his lips pressed together, reaching the foot of the bank by the end of the shot;"],
    [once("s40", "Xu Yan stays where he is, his arm still reaching,"),
     "Xu Yan stays planted where he is, his right arm still stretched toward screen right after Wang Erniu,"],
    [once("s40", PUSH), "The camera holds a static shot."],
]

DUR = {"s20": 6, "s40": 6, "s22": 8}  # the d1/fix1 lengths
for sid in S:
    S[sid]["duration_seconds"] = DUR[sid]
    text = fix1text(sid)
    for old, new in S[sid]["replace"][len(FIX1[sid]["replace"]):]:
        assert text.count(old) == 1, (sid, old[:60])
        text = text.replace(old, new)

(HERE / "spec.json").write_text(json.dumps({"seeds": [9311301, 9311302], "base": {k: f"fix1 {v}" for k, v in PICK.items()},
                                            "shots": S}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
