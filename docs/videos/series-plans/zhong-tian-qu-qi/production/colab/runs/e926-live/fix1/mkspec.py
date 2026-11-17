"""e926 fix1: the three retakes of picks-merged.tsv (s28, s35, s40), merged from review-picks-a/b by the coordinator.
Same steps as e925 fix1: retake.py from live/st1 (the d1 edits of e926-live/spec.json are applied first; retake.py on
those edits alone reproduces the d1 prompts of s28, s35 and s40 byte for byte), mkjobs.py for the duration, the absolute
picture paths, output_path and the scans, then preflight-prompts.py. Seeds 9261201/9261202; s28 and s35 6 s, s40 8 s.

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

Why each shot (coordinator's decisions, frames checked 2026-11-17):
- s35 (B RETAKE; A 1102 0.000-3.667 as the fallback): in both takes the six customers are copies of Lai San (grey cloth head
  wrap, grey-brown checked short jacket, white cuffs), 1101 also has seven or eight of them and a grid of fake writing on
  the wall and the paving. Now six customers who are plainly six different people (each one's colour, cut and hair or
  head wrap written), the count fixed at eight, the camera at standing eye height and still; the customers side-on and
  from behind, never toward the lens; d1's "a small smile" goes (no smile word anywhere).
- s28 (A RETAKE; B 1101 3.250-5.084 as the fallback, he grins up to 3.0 s and through the cut): 1101 grins through the
  flip and the cakes stay stuck to the tilted top; 1102 never flips the table, the cakes pass through it, and a white cloth
  strip of fake writing hangs at the right. Now a cold, jaw-clenched face (d1's "not smiling" goes), the closed fan tucked
  in his belt, both hands on the table edge in the first frame, one heave flips the whole low table upside down on the
  paving with the cakes scattering, the whole table inside the frame from the first frame to the last; the doorway only
  red silk on a plain wooden beam, the walls bare; the camera still. "from the Xu shop" goes (nobody out of frame named).
- s40 (A RETAKE; B 1101 0.000-8.000 as the fallback): in 1101 the man lies flat on his back with his face up (s38 ends
  with him curled, back to the lens), the customers close in on him and all wear the same grey robe; in 1102 the camera
  tilts and rises and the houses lean. Now standing eye height, level, still; Xu Yan frozen at the left in the doorway,
  lips pressed shut, the shop behind him dim with only bare dark shelves; the man curled on his side in the lower middle
  with his back to the lens (s38); five customers in five different colours who step back to both sides, three right and
  two left, side-on and from behind. 8 s (a36 1.68 s, the episode's tail).
Fallbacks are in picks-merged.tsv.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ST1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e926-dh/runpod/live/st1")
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

# s28: one heave, the whole table upside down inside the frame, a cold face.
S["s28"] = d1("s28")
S["s28"]["replace"] += [
    ["looking across the street from the Xu shop: a two-storey wooden shop front with long swags of red silk draped over a "
     "plain bare wooden beam above its wide doorway and a long low dark table before it,",
     "looking across the street: a two-storey wooden shop front, long swags of red silk draped over one plain bare wooden "
     "beam above its wide doorway, the plain wooden walls and posts bare, a long low dark table before it,"],
    [span("s28", "low wide shot of Wei Shaoqing", "exactly two people."),
     "low wide shot of Wei Shaoqing, the camera at knee height and level, in his sapphire-blue brocade robe woven with gold "
     "thread, a white jade pendant at his waist, a small green jade ornament at the front of his topknot, standing behind "
     "the long low dark table before the shop, framed full figure with space above his head, the whole long low table "
     "across the lower half of the frame in front of him with bare paving on both sides of it, both of his hands already "
     "gripping the near edge of the table in the very first frame, one closed folding fan tucked upright into his belt "
     "from the first frame to the last, like a short slim stick, its dark bamboo ribs pressed tight together, the table "
     "piled with rough yellow bars of soap and small dark red sugar cakes; cold fury: a hard cold stare, brows drawn down, "
     "jaw clenched and teeth gritted behind lips pressed shut from the first frame to the last, the corners of his mouth "
     "pulled down; on the step behind him one thin young man of about twenty in a dark red cloth short jacket and a black "
     "cloth head wrap, side-on, his lips closed; their hands hold only what is described here; exactly two people."],
    ["Wei Shaoqing heaves the whole table over toward us in one move, and the soap bars and sugar slabs tumble and bounce "
     "across the grey stone paving; the young man in dark red jumps back one step;",
     "In one single heave Wei Shaoqing jerks the near edge of the table up and flips the whole table over forward: it turns "
     "right over and lands upside down on the grey stone paving in front of him, its legs in the air, the whole table "
     "inside the frame from the first frame to the last; the soap bars and sugar cakes slide off as it tips and scatter, "
     "bouncing and rolling across the paving; his face stays cold and his jaw clenched throughout; the young man in dark "
     "red jumps back one step;"],
    [PUSH, STATIC],
]

# s35: six customers who are six different people, eight in all, eye height, still.
S["s35"] = d1("s35")
S["s35"]["replace"] += [
    ["the paving before the Xu shop in soft shade: wide shot from the street of the Xu shop front:",
     "the paving before the Xu shop in soft shade, the plank doors, the walls and the stone paving plain and unmarked: wide "
     "shot from the street of the Xu shop front at standing eye height, the camera level and still, the horizon level:"],
    ["brisk and friendly: a small smile, lips moving between words;",
     "brisk and warm: eyes bright, brows lifted, lips moving between words;"],
    [span("s35", "on the right along the paving a line of six customers", "exactly eight people."),
     "on the right along the paving a line of exactly six customers, one behind another, small, framed full figure, "
     "side-on and from behind, their faces turned toward Xu Yan and away from the camera, never looking at the lens, their "
     "lips closed, each one plainly a different person in different Song-dynasty clothes: first a stout middle-aged man in "
     "a short dark green cotton jacket and a black cloth head wrap; second an old man with a white beard in a long dark "
     "brown cotton robe, his grey hair in a small topknot; third a woman in a long indigo cotton robe, her black hair "
     "coiled low at the nape with a wooden pin; fourth a young man in a short ochre-yellow cotton jacket and a dark blue "
     "cloth head wrap; fifth a woman in a short pale blue cotton jacket, her hair wrapped in a white cloth; sixth a tall man "
     "in a long beige cotton robe and a brown cloth head wrap; their hands hold only what is described here; exactly eight "
     "people: Xu Yan, Lai San and the six customers, the same eight from the first frame to the last."],
    ["the customers shuffle and look toward him, their lips closed,",
     "the six customers keep their line, each shuffling half a step forward, side-on and from behind, looking toward Xu "
     "Yan, never at the camera, their lips closed,"],
    [PUSH, STATIC],
]

# s40: level and still; the man curled with his back to the lens (s38); five customers in five colours step back.
S["s40"] = d1("s40")
S["s40"]["replace"] += [
    [span("s40", "wide shot down the street at standing eye height, like the picture:", "exactly seven people."),
     "wide shot down the street at standing eye height, like the picture, the camera level and still, the horizon level "
     "and every wall upright: at the left edge of the frame Xu Yan, in his faded blue-grey scholar's robe patched at one "
     "elbow, its sleeves down, framed full figure, standing frozen just outside the doorway, his face three-quarter to "
     "screen right toward the man on the ground, never the lens; shocked: eyes wide, brows raised, his lips pressed shut; "
     "behind him the shop inside the doorway is dim and empty, only bare dark wooden shelves; in the lower middle of the "
     "frame on the grey stone paving one man in a long plain grey cotton robe, his cloth head wrap pulled low over his "
     "brow, lying curled on his side with his back to the camera and his knees drawn up, his face turned away from us "
     "toward the shop and hidden; close around him five customers, each plainly a different person in different "
     "Song-dynasty clothes: a man in a short dark green cotton jacket and a black cloth head wrap, a woman in a long indigo "
     "cotton robe, her black hair coiled low at the nape, a man in a long brown cotton robe and a brown cloth head wrap, a "
     "young man in a short ochre-yellow cotton jacket and a dark blue cloth head wrap, and a woman in a short pale blue "
     "cotton jacket, her hair wrapped in a white cloth; all five small, framed full figure, side-on and from behind, their "
     "faces turned down toward the man on the ground, never toward the camera, their lips closed; their hands hold only "
     "what is described here; exactly seven people."],
    ["the customers back away from the man on the ground at a walking pace and the ring of bare paving grows;",
     "the five customers step backward away from the man on the ground toward the two sides of the street, three to screen "
     "right and two to screen left, side-on and from behind, their faces still turned toward him, and the ring of bare "
     "paving around him grows; the man on the ground stays curled on his side with his back to the camera, still, from the "
     "first frame to the last;"],
    [PUSH, STATIC],
]

for sid in ("s28", "s35"):
    S[sid]["duration_seconds"] = 6
S["s40"]["duration_seconds"] = 8

(HERE / "spec.json").write_text(json.dumps({"seeds": [9261201, 9261202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
