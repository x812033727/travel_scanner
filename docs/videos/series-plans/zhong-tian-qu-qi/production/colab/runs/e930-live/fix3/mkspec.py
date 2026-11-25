"""e930 fix3: s07 retake (Qin Shuang stops Tang Wanjin at the yard gate), owner 2026-11-18 「該修就修，品質比較重要」.
Same steps as fix1: retake.py from live/st1 (s07 has no d1 text edit, only its set swap, so st1's ref-s07.txt is the d1 prompt
byte for byte, checked 2026-11-18 with cmp), mkjobs.py for the absolute pictures, output_path and the scans, then
preflight-prompts.py and h3r.sh check. Seeds 9301401/9301402 (fix<N> = 93014xx), bought at the d1 length (6 s, 960x544 Ref2VA).
Written 2026-11-18, NOT run (paid Colab; the send script is the scratchpad's e930f3.sh).

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix3 spec.json
    python3 -I mkjobs.py <live>/fix3
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix3/colab-jobs.json
    bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix3/colab-jobs.json

Why (cut-review.md 中等 1, review3-plan.md, frames of d1 9301101/9301102 checked 2026-11-18, scratchpad e930f3/*.jpg):
- Both d1 takes stand the two side by side facing the camera in front of the gate, Qin Shuang's left hand holding Tang
  Wanjin's left hand or wrist from the first frame to the last (1102 her arm through his), her face turned to him with the
  corners of her mouth up (32.4, 34.0, 36.85 s of the cut). Her line is 「小棠，這位老爺是誰？一進門就東張西望」: a stranger
  being stopped at the gate, read as a close pair. REVIEW 3's 1.42x crop takes the hands out but the first ~1 s still shows
  her forearm and glove reaching over, and the smile stays.
- What the d1 text asked for and why it failed: "her left arm already held out across his way" = an arm reaching toward
  him (the model closed it on his hand); "blunt and wary, not smiling: brows level" = a negated smile with a neutral face
  (task log e911 fix2, e912 on: a negated smile does not hold, write the concrete cold action); "facing us" for him and
  "half a step before him and a little to the side" for her = two people shoulder to shoulder facing the lens, which reads
  as a pair.
- Now (positive, concrete, no smile word, no negated noun): the two FACE EACH OTHER across one full step of bare earth, she
  three-quarter to screen right, he three-quarter to screen left; both her hands are busy on her own side, away from him (left
  palm flat on the left gatepost at shoulder height = the script's 「撐著門板」 and s08's "one hand on the swung-back plank
  gate", right fist on her hip at the belt); his two arms straight down at his sides, his hands at his thighs; the cold face
  part by part (brows pressed low and drawn together, eyes narrowed and hard, the mouth pressed flat between words and back
  into a tight line after the last word, chin level); framed from mid-thigh up, closer than d1's knees-up (task log e901
  fix6: faces in a wide two-shot are too small to hold an expression; mid-thigh keeps her fist on her hip and his hands at
  his thighs in frame). One motion: his slow head turn over the yard that ends on her (the d1
  action, which the line 「東張西望」 answers); she holds her stance and only speaks.
- Continuity: s06 ends on the square at afternoon (he flings his sleeve toward the carriage at screen right); s07/s08 are
  the yard at dusk by the gate (set-xujia-yuan-dong-men2-l1: the gate in the back wall, the house corner at left, the bare tree
  at right, the low sun from the upper right behind, long shadows to the lower left). s08 has Qin Shuang in the left third
  by the gate, so she stays on the left here and he on the right (the d1 sides). The Initial composition's place and light
  sentence is the d1 one, unchanged.
- Pictures as d1: qinshuang-portrait-l1, tangwanjin-portrait-l1, set-xujia-yuan-dong-men2-l1 (the swap of e930-live/spec.json).
  Her original voice line stays the same sentence (the cut uses the clip's own voice).
- Camera: the d1 slow push goes; the camera holds a static shot (a mid-thigh two-shot pushed in crops the heads and the hands, and a static
  frame keeps the step of earth between them readable). The fix3 check in mkjobs.py asserts this.
Fallback if both seeds fail again: keep REVIEW 3's crop of 9301101 (picks-merged.tsv), write KEEP, never RETAKE.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ST1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e930-dh/runpod/live/st1")
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]
SID = "s07"


def d1text():
    text = (ST1 / "prompts" / f"ref-{SID}.txt").read_text(encoding="utf-8")
    for old, new in D1SPEC[SID].get("replace", []):
        assert old in text, old[:60]
        text = text.replace(old, new)
    return text


def span(start, end):
    """The exact d1 text from start through end (end included), checked to be there once."""
    text = d1text()
    i = text.index(start)
    j = text.index(end, i) + len(end)
    assert text.count(text[i:j]) == 1
    return text[i:j]


def once(s):
    assert d1text().count(s) == 1, s[:60]
    return s


TWJ = ("Tang Wanjin, a little plump, with a round ruddy face, a short black moustache and a short black goatee, a small gold crown "
       "on his topknot, in his deep purple silk robe woven all over with small gold ingot shapes, a string of small gold keys at "
       "his waist")
QIN = ("Qin Shuang, in her fitted dark brown cross-collared short jacket cinched with a wide plain black leather belt, black "
       "trousers and leather boots, her high ponytail tied with black cord")
assert TWJ in d1text() and QIN in d1text()

COMP = (
    "medium two-shot at standing eye height just inside the yard gate, the two of them framed from mid-thigh up, both their heads with space above them, the gate and "
    "its small tiled roof soft behind them: they stand face to face across one full step of bare packed earth, a clear gap of "
    "low golden evening light between her shoulder and his from the first frame to the last; "
    f"on the left {QIN}, standing square in his way before the weathered left gatepost, her body and face three-quarter to "
    "screen right toward him, never the lens, her left palm pressed flat against the gatepost at the height of her shoulder, "
    "her left elbow bent, her right fist planted on her hip at her belt, her chin level; her face cold and "
    "guarded: her brows pressed low and drawn together, her eyes narrowed and hard, fixed on his face, her mouth pressed flat "
    "between words, her jaw firm; "
    f"on the right {TWJ}, already a step inside the gate from the first frame, standing still, his body three-quarter to "
    "screen left toward her, both his arms straight down at his sides, his hands loose against his thighs, his head turned "
    "toward screen right, looking the yard over, his lips pressed shut, his brows raised, his eyes sweeping, never the lens; "
    "her hands stay on the gatepost and on her hip, his hands stay at his sides; their hands hold only what is described "
    "here; exactly two people."
)

S = {SID: json.loads(json.dumps({k: v for k, v in D1SPEC[SID].items() if k in ("drop_pictures", "drop_set", "swap_pictures")}))}
S[SID]["replace"] = [
    [span("medium shot at standing eye height just inside the yard gate, the gate swung back behind them:",
          "lips moving clearly between words; their hands hold only what is described here; exactly two people."),
     COMP],
    [once("turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person, never "
          "looking at the camera;"),
     "turned toward him, her face three-quarter to screen right toward him, her eyes on his face, her left palm on the "
     "gatepost and her right fist on her hip the whole line, never looking at the camera, her mouth pressing back into a tight "
     "flat line after the last word;"],
    [once("Tang Wanjin slowly turns his head from screen right to screen left, looking the yard over;"),
     "Tang Wanjin slowly turns his head from screen right to screen left, looking the yard over, and his eyes settle on her "
     "face, his arms still at his sides;"],
    [once("The camera pushes in with small amplitude at slow speed."), "The camera holds a static shot."],
]
S[SID]["duration_seconds"] = 6  # the d1 length (r2.py BUY has no s07: 6 s)

(HERE / "spec.json").write_text(json.dumps({"seeds": [9301401, 9301402], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shot ->", HERE / "spec.json", f"(composition {len(COMP)} chars)")
