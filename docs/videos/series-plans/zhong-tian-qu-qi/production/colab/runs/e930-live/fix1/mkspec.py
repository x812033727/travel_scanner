"""e930 fix1: the three retakes of picks-merged.tsv (s29, s32, s41), merged from review-picks-a/b by the coordinator.
Same steps as e929 fix1: retake.py from live/st1 (the d1 edits of e930-live/spec.json are applied first; retake.py on those
edits alone reproduces the d1 prompts byte for byte, checked 2026-11-17), mkjobs.py for the duration, the absolute picture
paths (the d1 swaps, s32's now to the cleaned earth picture), output_path and the scans, then preflight-prompts.py. Seeds
9301201/9301202 (e929 fix1's 9291201/9291202 convention: episode, 12, seed), each shot bought at its d1 length.

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

Why (coordinator's merge of the two reviews, frames checked 2026-11-17):
- s29 (A and B RETAKE): in both takes Tang Xiaotang grew two thin braids tied with pink cord below her buns and stood left
  of centre (1102 squeezed to the left edge, 1102 also several lumps and her ear and cheek at 3.7 s); Tang Wanjin smiled
  through the whole line in both (the script's c25-c29: no smile); 1101's background had stools and baskets, 1102 a
  thatched shed and posts, not the low mud wall and field of set-xujia-yuan-dong-qiang-l1. The d1 text asked for "softened
  and tender, not smiling: brows raised, eyes wet": a negated smile and a soft face. Now the reviewers' positive rewrite:
  she stands dead centre from the first frame to the last, every strand up in the two buns so the bare nape shows clear
  down to the pink inner collar, the ribbon wound tight with its ends tucked in (no hanging word at all); only the mud wall
  and the field between her and the left edge; his face grief-stricken (mouth corners down, jaw set, brows drawn together
  and raised in the middle, red wet eyes, one tear); the speaking gaze is "toward her" (she is in frame). The action, the
  line and the two pictures (his portrait, -qiang-l1) are the d1 ones.
- s32 (A 1102 0-2.0 s, B 1102 0-1.5 s, both called it severe): after ~1.3-1.5 s the two tumbling halves became one small
  leaf-shaped scrap on the earth. set-xujia-yuan-dong-di-l1, the only picture sent, holds a pale leaf-shaped stone chip at
  its lower left (and a smaller one upper left): the model landed the paper as that chip. Now the halves already lie flat
  on the earth apart from the first frame (no tumbling, nothing for them to turn into), each a separate rectangle of paper
  the whole clip, only their torn edges stirring; the picture is set-xujia-yuan-dong-di2-l1 (clean_di.py: the two chips
  painted out) and is named as the earth only, no set, place or layout words (a prop-only insert carries no location
  words); the "real actors" header and the people tail go (nobody is in this insert).
- s41 (A and B RETAKE; the last shot of arc 3, handed over to e031): 1101 swapped A-ling for Tang Xiaotang walking in large
  from the right foreground at ~3.4 s, Xu Yan facing the camera; 1102 had no Tang Xiaotang for 3 s, then she rose in from the
  lower edge, small like a child, left of Xu Yan, with braids. The hand-over (r2-bible-e021-e030.md, 接點 30->31, coordinator
  2026-11-17): the gate in the middle of the back wall, A-ling at the front right by the well looking left at the gate, Wei
  Shaoqing in the gate looking right toward the well, Xu Yan and Tang Xiaotang in the middle of the yard backs to camera, she
  on his right. Now: locked-off camera that holds still (the d1 slow push goes); the same four people in the same places
  from the first frame to the last, nobody walking into or out of the frame; Xu Yan and the young woman the same size,
  shoulder to shoulder, backs to us, she at his right shoulder; Wei half turned toward the well. Pictures as d1 (A-ling's,
  Wei's and Xu Yan's portraits, -qing2-l1); she has no picture and is never named.
Fallbacks are in picks-merged.tsv.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ST1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e930-dh/runpod/live/st1")
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


def once(sid, s):
    assert d1text(sid).count(s) == 1, (sid, s[:60])
    return s


S = {sid: d1(sid) for sid in ("s29", "s32", "s41")}

# s29: Tang Xiaotang dead centre, the nape clear to the collar; Tang Wanjin grieving; only wall and field behind them.
S["s29"]["replace"] += [
    [span("s29", "medium shot from close behind one young woman seen only from behind",
          "exactly two people, the young woman in the middle seen only from behind."),
     "medium shot from close behind one young woman seen only from behind, appearing only once, standing dead centre of "
     "the frame from the first frame to the last, framed from the waist up: the back of her head with every strand of her "
     "black hair combed smooth and gathered up into just two round buns set high on her head, one bun on each side, one "
     "short pink silk ribbon wound tight round the base of each bun with its ends tucked in; every strand is up in the two "
     "buns, so the bare nape of her neck shows smooth and clear from the hairline all the way down to the pink inner "
     "collar, above her light peach-pink silk shoulders; the back of her head faces straight away from us the whole time, "
     "her head still, her ear the furthest round her head we ever see, standing on the packed earth of the yard; she is "
     "the only young woman with two high round buns in the frame; both her arms raised a little before her chest; between "
     "her and the left edge of the frame only the low mud-and-stone wall and the golden field beyond it; half a step "
     "beyond her in the right third of the frame, his whole figure clear of her head and shoulders, Tang Wanjin, a little "
     "plump, with a round ruddy face, a short black moustache and a short black goatee, a small gold crown on his topknot, "
     "in his deep purple silk robe woven all over with small gold ingot shapes, a string of small gold keys at his waist, "
     "standing, framed from the waist up, facing her, his face three-quarter toward her, never the lens, both his hands "
     "already holding one thick stack of plain blank paper sheets stitched along one edge with cord out against her arms "
     "from the first frame; his face grief-stricken and tender: the corners of his mouth turned down, his jaw set hard "
     "between words, his brows drawn together and raised in the middle, his eyes red-rimmed and wet with tears, one tear on "
     "his round cheek; beyond them, soft, only the low cracked mud-and-stone wall and the golden field in the low evening "
     "sun, from the left edge of the frame to the right edge; she stays dead centre of the frame the whole shot; their "
     "hands hold only what is described here; exactly two people, the young woman dead centre seen only from behind."],
    [once("s29", "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person, "
                 "never looking at the camera;"),
     "turned toward her, his face three-quarter toward her, his eyes on her, the corners of his mouth staying turned down "
     "and his eyes wet through the whole line, never looking at the camera;"],
]

# s32: the two halves already lie apart on the earth, each a separate rectangle; the picture is the earth only.
HEAD_OLD = "film footage of real actors in an ancient Chinese (Song-dynasty) period drama, shot on a cinema camera."
HEAD_NEW = "film footage for an ancient Chinese (Song-dynasty) period drama, shot on a cinema camera."
TAIL_NEW = ("Natural, realistic stillness of the paper on the earth: the two torn halves keep their shape and stay where they lie "
            "from the first frame to the last.")
S["s32"]["swap_pictures"] = {"set-xujia-yuan-l3.png": "set-xujia-yuan-dong-di2-l1.png"}
S["s32"]["replace"] += [
    [HEAD_OLD, HEAD_NEW],
    [span("s32", "Natural, realistic human motion", "never copy their blank expression."), TAIL_NEW],
    [span("s32", "The location shown in <Picture 1> is the set", "never the mood."),
     "The packed yellow earth shown in <Picture 1> is the ground under the paper, keeping its look. Initial composition: "
     "Warm golden low evening light from the right: insert close-up looking straight down at the packed yellow earth, the "
     "very first frame is already a close view of two torn halves of one sheet of cream paper with a thin gold edge, "
     "lying flat on the earth side by side with a strip of bare earth between them, only their plain blank backs showing: "
     "each half is its own separate rectangle of paper with three straight edges and one rough torn edge, the two torn "
     "edges facing each other, the two halves the same size; the earth fills the frame to every edge; only the two torn "
     "halves and the earth around them are in the frame. The picture fixes the earth only, never the mood."],
    [once("s32", "The two torn halves turn over slowly in the air and settle onto the earth, only their plain backs showing,"),
     "The two torn halves lie still on the earth where they are, apart, each one the same separate rectangle of cream paper "
     "from the first frame to the last, only their rough torn edges lifting and stirring a little in the evening breeze, "
     "their plain backs showing,"],
]

# s41: four people fixed in place, locked-off camera, Xu Yan and the young woman the same size, she at his right shoulder.
S["s41"]["replace"] += [
    [once("s41", "wide shot at standing eye height, like the picture:"),
     "wide shot at standing eye height, like the picture, the camera locked off: from the first frame to the last the "
     "same four people stand in the same four places, already there in the first frame, and nobody walks into or out of "
     "the frame:"],
    [once("s41", "half turned back toward the yard, frozen,"), "half turned toward the well at the front right, frozen,"],
    [span("s41", "in the middle of the yard, small, side by side with their backs to us, facing the yard gate:",
          "and on his right one young woman seen only from behind, appearing only once:"),
     "in the middle of the yard, small and both the same size, standing shoulder to shoulder with their backs to us, both "
     "facing the yard gate: on the left Xu Yan, the back of his head and his topknot toward us, in his faded blue-grey "
     "scholar's robe patched at one elbow, its sleeves down, and at his right shoulder, the same distance from the camera "
     "as he is, the top of her buns at the height of his ear, one young woman seen only from behind, appearing only once:"],
    [once("s41", "one short pink silk ribbon wrapped around each bun, the nape of her neck bare and clear above a pink inner "
                 "collar,"),
     "one short pink silk ribbon wound tight round the base of each bun with its ends tucked in; every strand is up in the "
     "two buns, so the bare nape of her neck shows smooth and clear from the hairline all the way down to the pink inner "
     "collar,"],
    [once("s41", "Nobody moves; only the loose strip"),
     "Nobody walks into or out of the frame and all four stay in their places; only the loose strip"],
    [once("s41", "the back of her head toward us the whole shot, and the low golden evening sunlight stays unchanged."),
     "the back of her head toward us the whole shot, standing at Xu Yan's right shoulder, and the low golden evening "
     "sunlight stays unchanged."],
    [once("s41", "The camera pushes in with small amplitude at slow speed."),
     "The camera is locked off and holds still the whole shot."],
]

DUR = {"s29": 6, "s32": 5, "s41": 8}  # the d1 lengths (r2.py BUY)
for sid in S:
    S[sid]["duration_seconds"] = DUR[sid]

(HERE / "spec.json").write_text(json.dumps({"seeds": [9301201, 9301202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
