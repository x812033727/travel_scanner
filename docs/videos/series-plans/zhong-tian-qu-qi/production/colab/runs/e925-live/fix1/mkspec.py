"""e925 fix1: the five retakes of picks-merged.tsv (s06, s18, s27, s32, s33), merged from review-picks-a/b by the
coordinator. Same steps as e924 fix1: retake.py from live/st1 (the d1 edits of e925-live/spec.json are applied first),
mkjobs.py for the duration, the absolute picture paths, s27's added portrait, output_path and the scans, then
preflight-prompts.py. Seeds 9251201/9251202; s06, s18, s32 6 s, s27 5 s, s33 8 s (a31 7.36 s).

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

The episode's worst fault: a prompt that says "toward the young woman beyond the edge of the frame" draws half of her face
at that edge (s06, s08, s09, s15, s18, s33, s37 in d1). Every retake here looks "toward someone out of sight", says the
third of the frame on that side is only scenery all the way to the edge, and that the one person is the only person from
the first frame to the last; a silent person keeps the lips pressed together from the first frame to the last; no smile,
grin or laugh word anywhere (s18's "not smiling" goes).

Why each shot (coordinator's decisions, frames checked 2026-11-17):
- s33 (A and B RETAKE): her side face at the left edge 0-2.6 s (1101) and 0-3.5 s (1102), a31 7.36 s needs the whole 8 s,
  and Steward Zheng grins in both. Now he is alone, the left third only empty jetty planks, a bare post and fog, his gaze
  past the left edge, eyes red, mouth corners down; the boat torch upright in an iron holder, nobody holding it.
- s32 (B RETAKE; A 1102 to 3.792, his mouth moves in the last half second): in both takes Zheng talks through her line
  (1102 also smiles) and in 1102 her cheek shows in the first second. Of the two ways (her back dead centre, or only him
  listening) the steadiest is only him: a back shot keeps a second face in the frame for the model to make talk and two
  buns to multiply, and every back shot of this episode had its buns split. He listens, alone, the left third empty
  jetty, lips pressed together the whole shot, one slow nod; her line a30 plays off screen; the grip on his arm goes to
  the sound (s32 跑步與跳板).
- s06 (B RETAKE, A 1102 from 2.000): 1102's head and chin outline sit at the right edge until about 3.0 s; after it a05
  (4.76 s) has 3.58 s left, and from 2.000 the first 姓 of the stammer is already gone. Now Erniu alone, the right third
  only roof, beams and plaster wall.
- s18 (B RETAKE, A 1102 from 1.625): her side face to 1.5 s (1101) and 1.875 s (1102); after it the take's mouth moves
  only about 1.7 s against a16's 3.33 s of speech, and 1101 grins at 4.5 s. Now Erniu alone, the right third only the
  shed posts, railing and snow; the letter is a small sheet of plain paper folded twice into a flat rectangle with a dab
  of wax (B: 1102's turned into a Western envelope).
- s27 (B RETAKE, A 1101 0.5-4.5): in both takes the men's sticks vanish or are laid down and all three sit down calmly;
  nobody is struck. No stretch reads as a sweep. Now one move only (coordinator): Qin Shuang's long staff sweeps low across
  and two men in grey fall back onto the seat of their pants in the mud, sticks still in their hands (in d1 the sticks
  vanished). Her portrait is sent (mkjobs.py puts it first; she is drawn in a wide, s28's way); three people.

Fallbacks are in picks-merged.tsv.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ST1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e925-dh/runpod/live/st1")
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


OUT_R = "someone out of sight beyond the right edge of the frame"
OUT_L = "someone out of sight beyond the left edge of the frame"
EMPTY_R = ("the right third of the frame, all the way to its right edge, is only {} with nobody in it from the first frame to "
           "the last")
EMPTY_L = ("the left third of the frame, all the way to its left edge, is only empty weathered jetty planks, one bare wooden "
           "post and drifting fog, with nobody in it from the first frame to the last")
ONLY = "{} is the only person in the frame from the first frame to the last; no second copy of anyone appears."

S = {}

# s06: Erniu alone, stammering toward someone out of sight at the right.
S["s06"] = d1("s06")
S["s06"]["replace"] += [
    [span("s06", "low-angle close-up from the height of the stove", "no second copy of anyone appears."),
     "low-angle close-up from the height of the stove of Wang Erniu alone, in his coarse brown hemp short jacket with rolled "
     f"sleeves, framed from the chest up with space above his head, set a little left of the middle, his face three-quarter "
     f"to screen right toward {OUT_R}, never the lens; stunned: brows shot up, jaw dropping, lips moving between stammered "
     "words; behind him only the thatched roof and its rough wooden beams, soft; "
     + EMPTY_R.format("the thatched roof, its rough wooden beams and the plain plaster wall,") + ". "
     + ONLY.format("Wang Erniu")],
    ["his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her, "
     "never looking at the camera; Wang Erniu's jaw drops and he leans toward her as he stammers;",
     f"his face three-quarter to screen right toward {OUT_R}, his eyes on that empty space just past the edge, never looking "
     "at the camera; Wang Erniu's jaw drops and he leans a little toward screen right as he stammers, his whole head staying "
     "inside the frame;"],
]

# s18: Erniu alone with the folded paper, toward someone out of sight at the right.
S["s18"] = d1("s18")
S["s18"]["replace"] += [
    [span("s18", "medium shot of Wang Erniu", "no second copy of anyone appears."),
     "medium shot of Wang Erniu alone, in his coarse brown hemp short jacket with rolled sleeves, standing a little left of "
     "the middle by one long low plain wooden plank table, pale and bare, its bare top empty, framed from the waist up, "
     "already holding in his right hand from the first frame one small sheet of plain paper folded twice into a flat "
     "rectangle, plain and blank on the outside, one round dab of dark red wax on its fold; his face three-quarter to screen "
     f"right toward {OUT_R}, never the lens; earnest and serious: jaw set, brows level, lips moving between words; behind "
     "him the shed in the low gold light, soft; "
     + EMPTY_R.format("the wooden posts of the shed, the low wooden railing and the snow beyond it,")
     + "; his hands hold only the folded paper. " + ONLY.format("Wang Erniu")],
    ["his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her, "
     "never looking at the camera; Wang Erniu tucks the folded sheet into the front of his jacket",
     f"his face three-quarter to screen right toward {OUT_R}, his eyes on that empty space just past the edge, never looking "
     "at the camera, his face serious throughout; Wang Erniu tucks the folded paper into the front of his jacket"],
]

# s27: one move. Her portrait first (mkjobs.py), the set second.
QIN = span("s28", "Qin Shuang shown in <Picture 1> keeps", "leather boots")
S["s27"] = d1("s27")
S["s27"]["prepend_pictures"] = ["qinshuang-portrait-l1.png"]
S["s27"]["replace"] += [
    ["For the target video, <Picture 1> is referenced throughout.",
     "For the target video, <Picture 1> and <Picture 2> are referenced throughout."],
    ["The location shown in <Picture 1> is the set, keeping its layout and props.",
     f"{QIN}; the location shown in <Picture 2> is the set, keeping its layout and props."],
    [span("s27", "on the left three youths", "no second copy of anyone appears."),
     "on the left Qin Shuang, in her dark brown cross-collared short jacket and wide black leather belt, her high black "
     "ponytail, gripping one plain long wooden staff low in both hands; on the right, an arm's length in front of her, two "
     "men in grey cotton short jackets and black cloth head wraps standing side by side, each gripping one plain round "
     "wooden stick as long as his arm in both hands; everyone small in the frame, side-on, their lips closed; exactly three "
     "people. Only Qin Shuang and the two men in grey, all small and side-on, are in the frame; no second copy of anyone "
     "appears."],
    ["The pictures fix the place and the objects only, never the mood.",
     "Facial expressions follow the action described below, not the reference pictures: the pictures fix the face, hair "
     "and costume only, never the mood."],
    ["the three youths sweep their staves low across in one move, and two of the men in grey lose their sticks, which fly "
     "spinning out of their hands, and sit down hard in the mud,",
     "In one single move Qin Shuang swings her long staff low and hard across in front of her, from left to right, through "
     "the two men's shins; at the crack both men fall backward and drop hard onto the seat of their pants in the wet mud, "
     "each still gripping his stick,"],
]

# s32: Steward Zheng alone, silent, listening to someone out of sight at the left.
S["s32"] = d1("s32")
S["s32"]["replace"] += [
    [span("s32", "over-the-shoulder medium shot from close behind one young woman", "no second copy of anyone appears."),
     "medium shot of Steward Zheng alone, the old steward, tall and thin in his dark brown satin long robe, his grey hair in "
     "a small topknot bound with a black cloth band, a neat grey-white goatee, standing on the jetty planks at the foot of a "
     "short gangplank a little right of the middle, framed from the waist up with space above his head, his hands at his "
     f"sides, his face three-quarter to screen left toward {OUT_L}, never the lens, his eyes on that empty space just past "
     "the edge; grave and moved, silent: his eyes wet, his brows drawn together, the corners of his mouth turned down, his "
     f"lips pressed firmly together; {EMPTY_L}; behind him the bow of one long flat-bottomed wooden cargo boat sitting low in "
     "the water, piled high with bundles of green-purple sugarcane tied with straw rope, one torch fixed upright in an iron "
     "holder at its bow, nobody holding it, soft; his hands hold nothing. " + ONLY.format("Steward Zheng")],
    [span("s32", "the young woman grips his forearm with both hands", "and looks down at her,"),
     f"Steward Zheng says nothing in this shot and listens to {OUT_L}: his lips stay pressed together from the first frame "
     "to the last, no talking, no mouthing words; his eyes fill and he gives one slow small nod,"],
]

# s33: Steward Zheng alone, speaking toward someone out of sight at the left.
S["s33"] = d1("s33")
S["s33"]["replace"] += [
    [span("s33", "medium close-up of Steward Zheng", "no second copy of anyone appears."),
     "medium close-up of Steward Zheng alone, the old steward, tall and thin in his dark brown satin long robe, his grey hair "
     "in a small topknot bound with a black cloth band, a neat grey-white goatee, standing on the jetty planks a little right "
     "of the middle, framed from the chest up with space above his head, both hands already raised and clasped together "
     f"before his chest from the first frame, his face three-quarter to screen left toward {OUT_L}, never the lens; deeply "
     "moved: his eyes wet and red-rimmed, his brows drawn up, the corners of his mouth turned down, lips moving between "
     f"words; warm torchlight on his grey goatee; {EMPTY_L}; behind him the dark bow of one cargo boat piled with "
     "green-purple sugarcane, one torch fixed upright in an iron holder at its bow, nobody holding it, soft in the fog; his "
     "hands hold only each other. " + ONLY.format("Steward Zheng")],
    ["his face three-quarter to screen left toward the young woman beyond the left edge of the frame, his eyes on her, never "
     "looking at the camera; Steward Zheng bows over his clasped hands as he speaks, then lifts his eyes past her toward the "
     "young man behind her, beyond the left edge of the frame; after the last word he waits,",
     f"his face three-quarter to screen left toward {OUT_L}, his eyes on that empty space just past the edge, never looking at the camera, his "
     "face moved and grave throughout; Steward Zheng bows a little over his clasped hands as he speaks, then lifts his eyes a "
     "little higher past the left edge of the frame; after the last word his lips close and he waits,"],
]
S["s33"]["duration_seconds"] = 8
for sid in ("s06", "s18", "s32"):
    S[sid]["duration_seconds"] = 6
S["s27"]["duration_seconds"] = 5

(HERE / "spec.json").write_text(json.dumps({"seeds": [9251201, 9251202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
