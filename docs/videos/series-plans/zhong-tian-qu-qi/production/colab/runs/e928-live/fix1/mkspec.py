"""e928 fix1: the three retakes of picks-merged.tsv (s03, s07, s26), merged from review-picks-a/b by the coordinator.
Same steps as e926 fix1: retake.py from live/st1 (the d1 edits of e928-live/spec.json are applied first where a shot keeps
them; retake.py on those edits alone reproduces the d1 prompts byte for byte), mkjobs.py for the duration, the absolute
picture paths (the d1 swaps), output_path and the scans, then preflight-prompts.py. Seeds 9281201/9281202, all three 6 s.

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

Why each shot (coordinator's decisions, frames checked 2026-11-17):
- s07 (A and B RETAKE; the story is reversed): both takes tie the grey strip round A-ling's own wrists (1101 she knots her
  own white-sleeved wrists, 1102 her two wrists are bound and held up), then push in to her face; Lai San's hands never
  appear. Now B's shot: from behind and a little above the man sitting on the wet stones, his two wrists in checked
  grey-brown cuffs crossed behind his back with the strip round them, two slender hands in long grey-white sleeves reaching
  down from the upper edge and knotting it; her own wrists free; the camera still (no push). Nobody is named and no person
  picture is sent (as d1's s03b): A-ling's face is not in the frame, his face is turned away; the set only. a04 4.60 s is
  laid over off screen, 6 s bought.
- s26 (A RETAKE; B 1102 0.000-4.500 as the fallback): in both takes Xu Yan stands on the torchlit side of the bars, between
  the two spoked lock wheels of set-dalao-l1, and reads as locked in; 1102 also looks into the lens. Now the set picture is
  set-dalao-bi-l1 (the same bars and torchlit room, no lock), the camera on the cold dark outer side at an angle, the gate
  running from the middle of the frame to the right edge, Xu Yan at the left on the near side of the bars, side-on facing
  screen right, peering between two bars, only the dark wall from him to the left edge, never the lens; the camera still
  (a push would carry the lens toward the bars and the inside).
- s03 (B RETAKE; A's 1102 0.000-3.000 checked at 6 and 24 frames a second and not taken): his hands are clasped over his
  head with no stick until about 2.1 s, when a stick grows out of them; it swings down in front of him four or five steps
  from her and never reaches the stones beside her; she does not move. That does not read as a blow that misses her. Now the
  man stands one step beyond her down the lane, backlit and facing her, the stick plain in both fists from the first frame
  to the last, it cracks onto the stones one arm's length to her right and bounces in his hands; she stands still, her back
  to us to the last frame (both takes turned her to the lens after 4 s); nobody is hit; the camera still.
Fallbacks are in picks-merged.tsv.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ST1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e928-dh/runpod/live/st1")
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


STATIC = "The camera holds a static shot."
PUSH = "The camera pushes in with small amplitude at slow speed."
S = {}

# s03: the man one step beyond her, the stick in his fists throughout, it lands one arm's length to her right; she stays.
S["s03"] = d1("s03")
S["s03"]["replace"] += [
    [span("s03", "wide shot down the lane at standing eye height, like the picture:", "exactly two people."),
     "medium-wide shot down the lane at standing eye height, like the picture, the camera level and still: in the left "
     "foreground on the wet stones A-ling, in her plain grey-white cotton dress with long sleeves covering her wrists, her "
     "black hair in a high bun with one plain wooden hairpin, a veil of soft, finely woven pale grey gauze over her nose, "
     "mouth and chin, tied behind both ears, falling to just below her jaw, her back three-quarter to us from the first "
     "frame to the last, facing down the lane, framed full figure, one short knife sheathed in plain dark wood, grip and "
     "sheath one closed piece of dark wood as long as her hand held low in her right hand at her side, never the lens; "
     "calm and cold: eyes on the man before her; one step beyond her down the lane, right of centre, facing her and us, one "
     "broad man in a plain black cross-collared short jacket, a black cloth head wrap and cloth shoes, the small warm light "
     "far down the lane behind him, his face dark in shadow, framed full figure, gripping one plain wooden stick as long as "
     "his arm, smooth and round to its ends, in both fists, already raised over his right shoulder in the first frame, the "
     "whole stick plain to see in his two fists from the first frame to the last; their hands hold only what is described "
     "here; exactly two people."],
    ["The man brings his stick down in one hard stroke and A-ling sways aside, so the stick comes down a full arm's length "
     "to her right and cracks onto the empty wet stones;",
     "The man swings the stick down in one hard stroke, still gripping it in both fists, and it cracks onto the empty wet "
     "stones a full arm's length to her right and bounces once in his hands; A-ling stands still, her feet planted, her "
     "back to us;"],
    [PUSH, STATIC],
]

# s07: from behind and above the seated man, his wrists crossed behind his back; two grey-white sleeved hands tie the knot.
st1_s07 = (ST1 / "prompts" / "ref-s07.txt").read_text(encoding="utf-8")
cast = st1_s07[st1_s07.index("A-ling shown in <Picture 1> and <Picture 2>"):
               st1_s07.index("keeping its layout and props.") + len("keeping its layout and props.")]
comp = st1_s07[st1_s07.index("close-up of A-ling,"):st1_s07.index("never the mood.") + len("never the mood.")]
act = st1_s07[st1_s07.index("A-ling pulls the two ends"):st1_s07.index(" and the cold moonlight")]
S["s07"] = {
    "drop_pictures": ["aling-angle-a-l1.png", "aling-angle-b-l1.png"],
    "swap_pictures": {"set-chouduan-l1.png": "set-chouduan-ye-xiang-l2.png"},
    "replace": [
        [cast, "The location shown in <Picture 3> is the set, keeping its layout and props."],
        [comp,
         "close shot from behind and a little above one thin man sitting on the wet stones, the camera high behind his back "
         "looking down, level and still: the back of his checked grey-brown hemp short jacket and his old cloth head wrap fill "
         "the lower half of the frame, his head turned away from us down the lane; his two thin wrists in checked grey-brown "
         "sleeve cuffs are crossed behind his back at the small of his back, a strip of grey cloth wound round them; two "
         "slender hands in long grey-white cotton sleeves reach down into the frame from its upper edge and already grip the "
         "two ends of the strip from the first frame, the grey-white cuffs loose round their own bare wrists; below them only "
         "the dark wet stones; their hands hold only what is described here; exactly one man seen from behind and two "
         "grey-white sleeved hands; no second copy of anyone appears. Throughout the shot the set layout stays as it is. The "
         "pictures fix the place and the objects only, never the mood."],
        [act,
         "The two grey-white sleeved hands pull the two ends of the strip hard and tie one tight knot round the man's crossed "
         "wrists behind his back, the grey-white cuffs still loose round their own bare wrists; the man's head stays turned "
         "away down the lane,"],
        [PUSH, STATIC],
    ],
}

# s26: the unlocked set picture; from the cold outer side at an angle, Xu Yan at the left on the near side of the bars.
S["s26"] = d1("s26")
S["s26"]["swap_pictures"] = {"set-dalao-l1.png": "set-dalao-bi-l1.png"}
S["s26"]["replace"] += [
    ["a gate of thick square dark bars filling the frame from edge to edge, and beyond the bars",
     "a gate of thick square dark bars, and beyond the bars"],
    [span("s26", "wide shot at standing eye height, like the picture:", "he is the only person in the frame;"),
     "wide shot from the cold dark side of the jail gate, at an angle, at standing eye height, the camera level and still: "
     "the gate of thick square dark bars runs from the middle of the frame away to the right edge, and beyond the bars the "
     "torchlit pale stone room; on the left of the frame, on the near side of the bars in the cold blue night, Xu Yan, in "
     "an old plain grey cotton outer coat over his faded blue-grey scholar's robe, one small clay oil lamp in his left "
     "hand, its small flame cupped behind his right palm, framed from the knees up, side-on to us facing screen right, "
     "pressed against the left end of the bars, half his face peering between two bars toward the torchlit room from the "
     "first frame, never the lens; tense and watchful: brows drawn, eyes narrowed, lips pressed shut; from him to the left "
     "edge of the frame only the dark night wall; he stays on the dark near side of the bars the whole shot; he is the only "
     "person in the frame;"],
    [PUSH, STATIC],
]

for sid in S:
    S[sid]["duration_seconds"] = 6

(HERE / "spec.json").write_text(json.dumps({"seeds": [9281201, 9281202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
