"""e929 fix1: the two paper inserts of picks-merged.tsv (s10, s11), merged from review-picks-a/b by the coordinator.
Same steps as e928 fix1: retake.py from live/st1 (the d1 edits of e929-live/spec.json are applied first; retake.py on
those edits alone reproduces the d1 prompts byte for byte), mkjobs.py for the duration, the absolute picture paths (the
d1 swap of the square to the paper prop picture), output_path and the scans, then preflight-prompts.py. Seeds
9291201/9291202, both 6 s, each sends only its own paper prop picture.

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

Why (coordinator's decisions, frames checked 2026-11-17):
- s11 (A RETAKE, B 1102 1.667-5.167 with the same fault called severe): in both takes the background is a snowy busy
  market (eaves, stalls, people, a hanging pennant), a place that is not the noon square, and the yellowish sheet is a
  small square that floats up into it and fills the frame only at 3.3-3.9 s; it reads as a flat sheet pasted on. The d1
  text told the model "The location shown in <Picture 1> is the set" with only the paper picture sent, "In the town
  square ... on a cold clear winter day" and "the set layout stays as it is", so it invented a set (and snow) behind the
  paper. Now A's rewrite: the picture is named as the paper prop, the town-square clause and the set-layout sentence go,
  the sheet fills the frame from the first frame and reaches past all four edges, against the low slanting winter sun,
  only the sun's glow coming through the paper itself; the "real actors" header and the people tail go (nobody is in
  this shot). The action is the d1 one (lumps, fibres and dark specks in the light, nothing else; the slow push).
- s10 (A 1101 2.250-6.583, B 1101 1.708-6.583; both takes start or cut into a snowy market or palace yard, 1102 hard-cuts
  at 3.75 s; the usable picture is 4.33 s, the recorded line a09-p84 has 4.85 s of voice): the same rewrite with the
  white willow-leaf sheet; the action is the d1 one (the faint willow leaf clearer in the light).
Both are bought at 6 s, room for a09-p84 (4.85 s of voice) and a10-p79 (3.47 s). Fallbacks are in picks-merged.tsv.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ST1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e929-dh/runpod/live/st1")
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]


def d1(sid):
    return json.loads(json.dumps({k: v for k, v in D1SPEC[sid].items()
                                  if k in ("drop_pictures", "drop_set", "swap_pictures", "replace")}))


def d1text(sid):
    text = (ST1 / "prompts" / f"ref-{sid}.txt").read_text(encoding="utf-8")
    for old, new in D1SPEC[sid].get("replace", []):
        assert old in text, (sid, old[:60])
        text = text.replace(old, new)
    return text


def span(sid, start, end):
    """The exact d1 text from start through end (end included), checked to be there once."""
    text = d1text(sid)
    i = text.index(start)
    j = text.index(end, i) + len(end)
    assert text.count(text[i:j]) == 1, sid
    return text[i:j]


HEAD_OLD = "film footage of real actors in an ancient Chinese (Song-dynasty) period drama, shot on a cinema camera."
HEAD_NEW = "film footage for an ancient Chinese (Song-dynasty) period drama, shot on a cinema camera."
TAIL_NEW = "Natural, realistic motion of the paper in the light: the sheet keeps the look of its reference picture."
LEAD = ("The sheet of paper shown in <Picture 1> is the prop, keeping its look. Initial composition: Against the low "
        "slanting winter sun: insert close-up, the very first frame is already filled edge to edge by one sheet of ")
BACK = ("behind the sheet only the bright glow of the low sun shows through the paper itself; ")
END = "The picture fixes the paper only, never the mood."

S = {}
for sid in ("s10", "s11"):
    S[sid] = d1(sid)
    S[sid]["replace"] += [
        [HEAD_OLD, HEAD_NEW],
        [span(sid, "Natural, realistic human motion", "never copy their blank expression."), TAIL_NEW],
    ]

S["s10"]["replace"].append(
    [span("s10", "The location shown in <Picture 1> is the set", "never the mood."),
     LEAD + "plain blank white paper against the sun: the sheet reaches past all four edges of the frame from the first "
     "frame to the last, so the whole picture is the glowing white paper, the sunlight coming through it from behind, one "
     "faint willow-leaf shape in the middle, two soft wavy bands of paper fibre running across the sheet behind it as part "
     "of the paper itself, the soft fibres of the paper glowing in the light; " + BACK +
     "only the glowing sheet is in the frame. " + END])
S["s11"]["replace"].append(
    [span("s11", "The location shown in <Picture 1> is the set", "never the mood."),
     LEAD + "rough blank yellowish paper against the sun: the sheet reaches past all four edges of the frame from the "
     "first frame to the last, so the whole picture is the dull yellowish paper, the sunlight coming through it from "
     "behind dull and uneven, only soft lumps in the pulp, a few short pale hair-thin fibres lying apart from each other "
     "and small dark specks scattered through it, plain all over; " + BACK +
     "only the dull yellowish sheet is in the frame. " + END])

for sid in S:
    S[sid]["duration_seconds"] = 6

(HERE / "spec.json").write_text(json.dumps({"seeds": [9291201, 9291202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
