"""e931 fix1: the retakes of picks-merged.tsv, merged from review-picks-a/b by the merge agent (2026-11-18). NOT RUN: these
are written and checked (retake.py, mkjobs.py, preflight-prompts.py, h3r.sh check), nothing is sent.
Same steps as e930 fix1: retake.py from live/st1 (the d1 edits of e931-live/spec.json are applied first, then these), mkjobs.py
for the duration, the absolute picture paths, output_path and the scans, then preflight-prompts.py. Seeds 9311201/9311202
(episode, 12, seed), each shot bought at its d1 length.

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1            # writes colab-jobs.json (all 12) and colab-jobs-p1.json (the 6 of priority 1)
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

Priority 1 (both reviewers flagged; cutting cannot save them): s30, s31, s22. Priority 2 (the owner decides): s06, s20, s40.
Why, shot by shot, in plan.md. The rules followed (route-a.md, e92x-e930 fix1): positive descriptions, no negated object noun;
Tang Xiaotang's hair in the words of the takes that kept two clean buns (e931 s19 1101 and e930 fix1 s29 1201); no smile word
except the season's NOSMILE sentence and the d1 "not smiling"; nobody named who is not in the frame.

- s30 (A and B): five or six lumps of buns with pink ribbon ends hanging, in both takes; Xu Yan's sweep crossed behind her head.
  Now: e930 fix1 s29's hair sentence (ribbon wound tight with its ends tucked in, every strand up so the nape shows clear to
  the collar), she stands dead centre from the first frame to the last, his hand stays in the left third clear of her head.
- s31 (A and B): both takes walked toward the camera (the independent review's must-fix 5: along the bed, away from us), four
  to six villagers. The d1 text already said "walking away from us", but it also gave Erniu and Xu Yan faces in profile with
  their portraits sent: the model turned the line round to show the faces. Now: their two portraits dropped (from behind
  nobody needs a face; route-a: no face picture, no face), nobody named, seven backs walking away up the bed, the front man
  points ahead; nobody speaks in the clip: Erniu's line is the recording zq931a33 (2.79 s), laid in by the editor.
- s22 (A and B): multi-lump buns; her head turned and her cheek showed (1102 from 3.3 s, 1101 from 4.5 s) when asked to
  "lean in"; the sprouts grew as long green shoots in white rice, unlike s21's golden seeds with white tips. Now: the s30 hair
  sentence; her clasped hands rise to her chest instead of a lean (only her forearms move); the bowl in s21's words; Xu Yan's
  "faint pleased smile" becomes bright soft eyes with lips pressed together.
- s06, s20 (priority 2; A and B both called the buns medium): the same hair sentence; Xu Yan smiled while speaking in both
  takes of both shots: NOSMILE replaces "not smiling" / "a faint warm look".
- s40 (priority 2; A and B split): 1101 had the right hoe but three extra shouts before the line; 1102 a pick (one point, one
  broad blade). Now: the hoe written by its parts like the one on his shoulder in s39/s41, his roar becomes a set jaw, the
  line shouted once and then lips pressed; Xu Yan's lips pressed together until his line.
Fallbacks are in ../picks-merged.tsv.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ST1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e931-dh/runpod/live/st1")
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
P1 = ("s22", "s30", "s31")
P2 = ("s06", "s20", "s40")


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


S = {sid: d1(sid) for sid in P1 + P2}

# Tang Xiaotang's hair (e930 fix1 s29 1201, e931 s19 1101 kept two clean buns) and her place, for every back shot retaken here.
HAIR_OLD = "one short pink silk ribbon wrapped around each bun, the nape of her neck bare and clear above a pink inner collar,"
HAIR_NEW = ("one short pink silk ribbon wound tight round the base of each bun with its ends tucked in; every strand is up in the "
            "two buns, so the bare nape of her neck shows smooth and clear from the hairline all the way down to the pink inner "
            "collar,")
for sid in ("s06", "s20", "s22", "s30"):
    S[sid]["replace"] += [[once(sid, HAIR_OLD), HAIR_NEW]]
    for ground in ("cracked earth", "packed earth"):
        old = f"standing on the {ground} of the yard, in the middle of the frame,"
        if old in d1text(sid):
            S[sid]["replace"] += [[once(sid, old),
                                   f"standing on the {ground} of the yard, dead centre of the frame from the first frame to "
                                   f"the last,"]]
            break
    else:
        raise SystemExit(f"{sid}: no standing clause")

# s30: his sweep stays on his side of the frame.
S["s30"]["replace"] += [
    [once("s30", "Xu Yan sweeps his flat right hand once toward the yard gate at the right of the frame as he speaks;"),
     "Xu Yan sweeps his flat right hand once out to his side toward the yard gate as he speaks, his hand staying in the left "
     "third of the frame, clear of her head;"],
]

# s22: the bowl in s21's words, his face without a smile word, her hands instead of a lean.
S["s22"]["replace"] += [
    [once("s22", "one red clay bowl holding a layer of rice grains, each grain with one tiny white sprout held in both his hands "
                 "at his chest,"),
     "one red clay bowl holding a layer of plump golden-brown unhusked rice seeds, a few of them each showing one tiny white "
     "sprout tip no longer than the seed itself, held in both his hands at his chest,"],
    [once("s22", "warm: a faint pleased smile, his lips pressed together;"),
     "warm: his eyes bright and soft, his brows lifted a little, his lips pressed together;"],
    [once("s22", "She leans in a little toward the bowl in his hands, only her shoulders moving;"),
     "Her clasped hands rise from her waist to her chest in delight, only her forearms moving;"],
]

# s31: seven backs walking away up the bed, nobody named, no face pictures, nobody speaking in the clip (recording a33).
S["s31"]["drop_pictures"] += ["erniu-portrait-l1.png", "xuyan-portrait-l1.png"]
VILLAGERS = span("s31", "five more people in Song-dynasty cross-collared homespun short jackets",
                 "each with one bamboo basket on the back and one wooden spade in hand,")
S["s31"]["replace"] += [
    [span("s31", "Wang Erniu shown in <Picture 1> and <Picture 2>", "cloth shoes; "), ""],
    [once("s31", "the location shown in <Picture 6> is the set"), "The location shown in <Picture 6> is the set"],
    [span("s31", "wide shot at standing eye height, like the picture,", "the only hoe in the frame is Wang Erniu's."),
     "wide shot at standing eye height from behind the walkers, like the picture, the camera on the dry bed behind them: from "
     "the first frame all seven people walk away from us up the dry cracked bed toward its far end, on the cracked mud plates "
     "to the right of the plank walk, in a loose line, all framed full figure, small, their backs to us the whole shot: at the "
     "front, furthest from us, a big broad-shouldered young man in a coarse brown cross-collared short jacket with the sleeves "
     "rolled up and a cloth sash, his black hair in a topknot, one hoe with a plain wooden handle and an iron blade on his "
     "right shoulder; just behind him a tall lean young man in a faded blue-grey scholar's robe, its sleeves rolled up to the "
     "elbows, dust on its hem, his black hair in a topknot tied with a cloth band; behind them, nearer to us, "
     + VILLAGERS[:-1] + ";" +
     " all seven seen from behind, the backs of their heads toward us; ahead of them the long dry bed runs straight away to "
     "its far end between the willows and village roofs on the left bank and the grass bank and the field on the right; their "
     "hands hold only what is described here; exactly seven people; the only hoe in the frame is the one on the front man's "
     "shoulder."],
    [once("s31", "Only Wang Erniu, Xu Yan and the five other people the composition describes, each in a different colour, are "
                 "in the frame; no second copy of anyone appears."),
     "Only the seven people the composition describes, each in a different colour and all seen from behind, are in the "
     "frame; no second copy of anyone appears."],
    [once("s31", "Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix "
                 "the face, hair and costume only, never the mood."),
     "The picture fixes the stream bed and its banks only, never the mood."],
    [span("s31", "Wang Erniu speaks a short Mandarin line", "no talking, no mouthing words,"),
     "The seven of them walk steadily away from us up the cracked mud of the stream bed toward its far end, growing smaller, "
     "the backs of their heads toward us the whole shot; the big young man at the front lifts his free left hand once and "
     "points ahead up the stream bed as they walk; all seven walk on in silence, their faces turned ahead up the stream bed,"],
    [span("s31", "Natural, realistic human motion", "never copy their blank expression."),
     "Natural, realistic human motion of real actors walking: each person keeps the hair and clothing written above from the "
     "first frame to the last."],
]

# s06, s20: Xu Yan without a smile, in the season's NOSMILE words.
S["s06"]["replace"] += [
    [once("s06", "calm and level, not smiling: steady eyes, brows level, lips moving evenly between words;"),
     f"calm and level: steady eyes, brows level, lips moving evenly between words, {NOSMILE};"],
]
S["s20"]["replace"] += [
    [once("s20", "quietly hopeful: a faint warm look in his eyes, lips moving evenly between words;"),
     f"quietly hopeful and steady: eyes bright, brows level, lips moving evenly between words, {NOSMILE};"],
]

# s40: the hoe by its parts, one shout, lips pressed after it.
S["s40"]["replace"] += [
    [once("s40", "one hoe with a plain wooden handle and an iron blade raised above his head in both hands, not smiling: mouth "
                 "wide in a roar, brows knotted, never the lens;"),
     "one farm hoe raised above his head in both hands: a long straight wooden handle with one flat, broad, square iron blade "
     "set at a right angle across its top end, the same hoe he carries on his shoulder, not smiling: jaw clenched, brows "
     "knotted, eyes fixed ahead, never the lens;"],
    [once("s40", "his mouth wide in a shout, not smiling, never the lens;"),
     "his lips pressed together until his line, not smiling, never the lens;"],
    [once("s40", "Wang Erniu charges on toward the bank of sacks at the right, the hoe held high, as he shouts;"),
     "Wang Erniu charges on toward the bank of sacks at the right, the hoe held high, shouting his line once and then running "
     "on with his jaw clenched and his lips pressed together;"],
]

DUR = {"s06": 6, "s20": 6, "s22": 8, "s30": 8, "s31": 6, "s40": 6}  # the d1 lengths (r2.py BUY)
for sid in S:
    S[sid]["duration_seconds"] = DUR[sid]

(HERE / "spec.json").write_text(json.dumps({"seeds": [9311201, 9311202], "priority_1": list(P1), "priority_2": list(P2),
                                            "shots": S}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
