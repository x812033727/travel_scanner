"""e933 fix1: the retakes of ../picks-merged.tsv (merge agent, 2026-11-19). NOT RUN: written and checked (mkjobs.py,
preflight-prompts.py, check_manifest.py, h3r.sh check), nothing is sent. Why, shot by shot, in plan.md.

    python3 -I mkspec.py                       # -> spec.json (9 shots, seeds 9331211/9331212 for every shot)
    python3 -I mkjobs.py <live>/fix1           # -> <live>/fix1/prompts/*.txt, retake.json, colab-jobs.json (18 jobs, 124 s)
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix1/colab-jobs.json

Seeds 9331211/9331212, not 9331201/9331202: those two (and 9331203-9331205) were the Qwen-Image-Edit seeds of set-shentan-l2
(refs-live/README.md), so a second file named 9331201 would be ambiguous. The base of every job is the d1 9331101 job and
prompt exactly as sent (e933-live/spec.json's d1 edits already in); each fix1 replace is asserted to be in that prompt exactly
once. Every shot is bought at its d1 length. Run on the Colab session zt-live3 only after the e934 d1 there has finished (one
job at a time per session, route-a 2026-11-09).

The rules followed (route-a.md, the task file's lessons, e932 fix1-fix3): positive descriptions, no negated object noun; a
face that must not smile is written as a concrete hard face part by part plus the season's NOSMILE sentence (e901 fix6), and
the words in the identity sentences that make a face smile go ("kind face", "warm eyes": e904 sweet/dimples); head counts as
numbers; where someone looks is a named target, never only "not the lens"; a hook's action is put where the framing shows it
(s05, s33, s34); two long things never touch in the first frame (e932 fix2: the rope of s05 ran into the ladder).

- s01 (A and B): Elder Han stood in both takes (1101 behind the kneelers with the staff in hand, 1102 among them leaning on
  it); e932's last shot and s02-s04 have him kneeling. d1 had already taken the staff out of his identity sentence
  here; "framed full figure" (drawn standing) goes, and so do "kind face" and "warm but firm eyes". Now he is kneeling upright from the first frame to
  the last, sitting back on his heels, heads level with the kneelers, bare flagstones between him and the altar table, the
  staff leaning on the table end; Xu Yan the one person on his feet; the eight kneelers in the right half, faces toward Xu Yan.
- s03 (A and B): Xu Yan looked straight into the lens in both takes (the line is a vow to the beam); 1101 pushed in to an eye
  close-up, 1102 warped the face. Now the camera is low at his left side, three-quarter profile, his face turned up to screen
  right toward the beam that crosses the top right corner, eyes past that corner far above the camera; framed chest-up and
  static the whole shot; the bow-and-lift (it brought the face round to the lens) is left out: he starts with his face up.
- s05 (B; the merge agent looked frame by frame: hook): in both takes the rope ran stiff and straight from the four men to the
  top of the ladder and the beam was out of the frame, so it read as people pulling a ladder. Now low wide shot with the
  whole beam across the upper frame from the first frame; the rope wrapped twice round the beam's right end; from that coil
  a thick, soft, sagging rope in one long slack curve to the four at the door; the ladder leans on the wall below the beam,
  apart from the rope; Carpenter Shi's hands on the coil on the beam; four on the rope written as a number.
- s07 (B; the merge agent looked: 1101 grins 0.6 s and 3.7 s and has two parallel timbers; 1102's beam is a timber with a
  crossbar and a wedge): one single plain squared beam, the only long wood in the frame; a strained face by its parts with
  the gritted teeth taken out (in d1 "teeth gritted" was drawn as a grin) plus NOSMILE.
- s22 (A; the merge agent zoomed the left edge of 1101: a complete wheel with rim and paddles, on day 4 when only the frame
  and axle exist; s28 "立起來" is day 10): the place sentence "by the half-built frames of the waterwheel" called up the wheel;
  now "by the low wooden frame and the bare axle on its trestle", and the space behind Erniu at the left is written as the
  bare axle, cut timbers and sky; the mallet held low at his side the whole shot (it vanished at 0.8 s); NOSMILE (1102 smiled).
- s33 (hook; A and B both flagged the face; the merge agent looked: both takes grin with crinkled eyes while shouting 「閘開了」
  0.4-1.3 s, 1102's gate is a raft dragged toward the lens, 1101's water only bursts at 7 s): the gate written as one upright
  board shutting a narrow stone channel, pond water banked behind it at the left, the dry channel running right to the wheel;
  he hauls the board straight up in the first two seconds and the water bursts through the gap under it and keeps rushing;
  a grim straining face by its parts (no teeth) plus NOSMILE.
- s34 (A and B, hook): both takes turned one to three paddles' worth and the twelve paddles look alike. New picture
  set-shentan-l4 (free: live-action/free-e031-e040/shentan_l4.py, the top paddle made pale new wood). The result first: one
  pale paddle at the top in the first frame; the wheel turns exactly half a turn, the pale paddle swinging over and down the
  left side to the very bottom (the water from the left pushes the bottom paddles right, so the top goes left), six paddles
  through the water, three seconds of steady turning, one second slowing, then two still seconds; the white water keeps
  pouring in to the last frame (both takes went calm after 4 s, which reads as "too little water", not s35's line).
- s35 (A; B kept 1102; the merge agent zoomed 1102: eyes straight into the lens 1.0-6.3 s, the same fault as s03): camera off
  his left shoulder, his face in profile to screen right bent toward the paddle, eyes on the wet wood between his hands;
  his shoulders shove forward twice.
- s36 (A and B): 1102 has two Elder Hans; 1101 smiles on 「祖宗的梁啊」 inside the line. "kind face" and "warm but firm eyes"
  go; exactly one person, alone; a grief-stricken face by its parts, corners of the mouth turned down, plus NOSMILE; the
  staff's foot resting on the stone by the last frame.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e933-dh/runpod/live/d1")
REFS = "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live/"
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = [9331211, 9331212]
DUR = {"s01": 6, "s03": 8, "s05": 6, "s07": 6, "s22": 6, "s33": 8, "s34": 6, "s35": 8, "s36": 8}  # the d1 lengths


def d1text(sid):
    return (D1 / "prompts" / f"ref-{sid}-9331101.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert d1text(sid).count(s) == 1, (sid, s[:70])
    return s


S = {sid: {"duration_seconds": DUR[sid], "replace": []} for sid in DUR}
HAN_ID = "a deeply lined kind face, a long white beard down to his chest, white hair in a neat small topknot, warm but firm eyes,"
HAN_ID_NEW = ("a deeply lined face, a long white beard down to his chest, white hair in a neat small topknot, grave steady eyes,")

# s01: Elder Han kneeling from the first frame to the last; Xu Yan the one person standing; the kneelers in the right half.
S["s01"]["replace"] = [
    [once("s01", HAN_ID), HAN_ID_NEW],
    [once("s01", "kneeling in two loose rows on the grey flagstones in the lower right foreground,"),
     "kneeling in two loose rows on the grey flagstones in the right half of the frame, in the lower right foreground,"],
    [once("s01", "their hands resting on their knees, their faces turned toward him, their lips closed, never the lens;"),
     "their hands resting on their knees, their faces turned toward Xu Yan, their lips closed, never the lens;"],
    [once("s01", "kneeling in the middle of the floor in front of them Elder Han, in his faded grey cotton cross-collared long "
                 "robe, his long white beard down to his chest, his white hair in a small topknot, framed full figure, his "
                 "bamboo walking staff leaning against the end of the altar table, his face turned back over his shoulder "
                 "toward Xu Yan, his lips pressed shut, never the lens;"),
     "in the clear middle of the floor in front of them Elder Han, in his faded grey cotton cross-collared long robe, his long "
     "white beard down to his chest, his white hair in a small topknot, already kneeling upright on both knees on the "
     "flagstones from the first frame and kneeling to the last frame, sitting back on his heels, his head at the same height "
     "as the kneeling people's heads, a clear stretch of bare grey flagstones between him and the altar table behind him, his "
     "two empty hands resting on his knees, his bamboo walking staff leaning against the end of the altar table, his face "
     "turned back over his shoulder toward Xu Yan, his lips pressed shut, grave: brows drawn, eyes steady, never the lens;"],
    [once("s01", "exactly ten people."),
     "exactly ten people: Xu Yan is the one person on his feet, and the other nine kneel on the flagstones from the first "
     "frame to the last."],
]

# s03: low at his left side, three-quarter profile up to the beam at the top right corner, static, chest-up.
S["s03"]["replace"] = [
    [once("s03", "low-angle close-up of Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves rolled "
                 "up to the elbows, his face pale and tired, kneeling, seen from just above the flagstones, framed from the "
                 "chest up, his head just lifting from a deep bow from the first frame, his face tipping up toward the dark "
                 "main beam above him, his eyes on it, never the lens;"),
     "low-angle close-up of Xu Yan from his left side, the camera below his chin and off to his left, in his faded blue-grey "
     "scholar's robe patched at one elbow, its sleeves rolled up to the elbows, his face pale and tired, kneeling, framed "
     "from the chest up the whole shot, his face in three-quarter profile turned up to screen right toward the thick dark "
     "main beam that crosses the top right corner of the frame, his eyes looking up past the top right corner of the frame "
     "at the beam, far above the camera, never the lens;"],
    [once("s03", "above and behind him, soft and out of focus, only the thick dark main beam across the top of the "
                 "candle-warmed back wall;"),
     "above him across the top right corner of the frame, soft but plainly one thick squared dark wooden beam, and behind "
     "him only the candle-warmed back wall;"],
    [once("s03", "his face tipped up toward the dark main beam above him, his eyes on it, never looking at the camera;"),
     "his face turned up to screen right toward the beam at the top right corner, his eyes on the beam, never looking at "
     "the camera;"],
    [once("s03", "Xu Yan lifts his head from the bow and looks up at the beam as he speaks,"),
     "Xu Yan holds his face up toward the beam at the top right and keeps his eyes on it as he speaks,"],
    [once("s03", "The camera pushes in with small amplitude at slow speed."), "The camera holds a static shot."],
]

# s05: the whole beam in the frame; the rope wrapped round the beam; a soft sagging rope; the ladder apart from it.
S["s05"]["replace"] = [
    [once("s05", "wide shot at about chest height, level, like the picture, the beam at the top of the frame:"),
     "low-angle wide shot from near the flagstones looking up, the whole thick dark main beam across the upper part of the "
     "frame from the first frame to the last:"],
    [once("s05", "one plain wooden ladder standing on the flagstones under the right end of the beam,"),
     "one plain wooden ladder leaning against the back wall under the right end of the beam,"],
    [once("s05", "both hands pulling tight the knot of one thick hemp rope round the end of the beam,"),
     "both hands on a coil of one thick, soft hemp rope wrapped twice round the right end of the beam just above his head, "
     "pulling its knot tight,"],
    [once("s05", "gruff and loud, not smiling: brows knotted, lips moving hard between shouted words;"),
     f"gruff and loud: brows knotted hard, eyes narrowed, jaw set, lips moving hard between shouted words, {NOSMILE};"],
    [once("s05", "from the beam the rope runs down and away to the left, where"),
     "from that coil on the beam the thick, soft hemp rope sags down to the left in one long slack curve to the four men "
     "near the doorway, where"],
    [once("s05", "the ladder stands well apart from the rope;"),
     "the rope runs from the beam itself, well apart from the ladder; four people in a row on the rope: Wang Erniu and the "
     "three men;"],
    [once("s05", "the four on the rope lean back and draw it taut;"),
     "the four on the rope lean back, and the sagging rope rises into one taut line from the coil on the beam down to their "
     "hands;"],
]

# s07: one plain squared beam, the only long wood in the frame; a strained face without teeth.
S["s07"]["replace"] = [
    [once("s07", "the long dark beam slanting up from his shoulder out of the upper right corner of the frame,"),
     "one single long thick squared dark timber beam, its surface plain and smooth along its whole length, the only long "
     "piece of wood in the frame, slanting up from his shoulder out of the upper right corner of the frame,"],
    [once("s07", "straining, not smiling: teeth gritted, brows knotted, lips moving hard between words;"),
     "straining under the weight: brows knotted hard, eyes narrowed, jaw clenched, his face flushed with effort, the cords "
     f"of his neck standing out, lips drawn tight and moving hard between words, {NOSMILE};"],
    [once("s07", "their shoulders under it,"), "their shoulders under that same one beam,"],
]

# s22: the half-built site written as the bare axle; the mallet low the whole shot; NOSMILE.
S["s22"]["replace"] = [
    [once("s22", "on the flat sandy bank by the half-built frames of the waterwheel;"),
     "on the flat sandy bank by the low wooden frame and the bare wooden axle on its trestle;"],
    [once("s22", "one wooden mallet with a plain wooden handle lowered at his right side from the first frame,"),
     "one wooden mallet with a plain wooden handle held low at his right side from the first frame to the last,"],
    [once("s22", "uneasy, not smiling: brows knotted, eyes darting, the skin of his face tight, lips moving low between words;"),
     f"uneasy and scared: brows knotted, eyes darting, the skin of his face tight, lips moving low between words, {NOSMILE};"],
    [once("s22", "their lips closed, never the lens; their hands hold only what is described here; exactly four people."),
     "their lips closed, never the lens; behind Wang Erniu at the left, soft, only the bare wooden axle lying on its low "
     "trestle, a pile of cut timbers on the sand and the pale sky; their hands hold only what is described here; exactly "
     "four people."],
]

# s33: an upright board in a stone channel, hauled straight up early; the water bursts under it; a grim face, no teeth.
S["s33"]["replace"] = [
    [once("s33", "both hands gripping the thick rope tied to the top of the small wooden sluice gate of three plain wet planks "
                 "before him from the first frame,"),
     "both hands gripping one thick rope from the first frame, the rope running straight up from the top edge of one upright "
     "sluice gate before him, a plain board of three wet planks standing upright in a narrow stone channel cut through the "
     "pond's stone edge, the board shutting the channel from side to side, the dark pond water banked up behind it at the "
     "left and the dry stone channel running away from it to the right toward the wheel,"],
    [once("s33", "straining, not smiling: teeth gritted, brows knotted, lips moving hard between words;"),
     "straining with all his weight: brows knotted hard, eyes narrowed, jaw clenched, the cords of his neck standing out, "
     f"his weathered face set and grim, lips moving hard between shouted words, {NOSMILE};"],
    [once("s33", "Carpenter Shi throws his weight back on the rope and the sluice gate is pulled up out of the gap: the pond "
                 "water rushes through it in a white surge along the stone toward the wheel at the right,"),
     "Carpenter Shi throws his weight back on the rope and in one heave hauls the upright board straight up out of the "
     "channel, its bottom edge rising high above the water within the first two seconds; at once the pond water bursts "
     "through the gap under the raised board in a white surge and rushes along the stone channel toward the wheel at the "
     "right, still rushing white to the last frame,"],
]

# s34: one pale paddle as the unit; exactly half a turn, the stop and two still seconds; the water white to the end.
S["s34"]["swap_pictures"] = {"set-shentan-l3.png": REFS + "set-shentan-l4.png"}
S["s34"]["replace"] = [
    [once("s34", "and the big wooden water wheel exactly as in the picture, standing in the pond against the far stone edge, "
                 "its twelve flat wooden paddles round its rim;"),
     "and the big wooden water wheel exactly as in the picture, standing in the pond against the far stone edge, its twelve "
     "flat wooden paddles round its rim: eleven of dark weathered wood and one of pale fresh-cut wood, much lighter than all "
     "the others, standing straight up at the very top of the wheel in the first frame;"],
    [once("s34", "In this shot the wheel turns only half a turn and then stops dead: the rushing water strikes the lowest "
                 "paddles, the big wheel creaks and swings slowly round half a turn, slows, and stops, and stays still to the "
                 "last frame while the water churns white under it,"),
     "In this shot the big wheel turns exactly half a turn and stops dead: the rushing water strikes the lowest paddles and "
     "the wheel creaks and turns slowly and steadily for three seconds, the pale paddle swinging over to the left and down "
     "the left side of the wheel to the very bottom, six paddles passing through the water; when the pale paddle reaches the "
     "bottom, in the water, the wheel slows over one second and stops dead, and for the last two seconds everything on the "
     "wheel stays still, the pale paddle at the bottom, while the white water keeps pouring in from the left and foaming "
     "white around the lowest paddles all the way to the last frame,"],
]

# s35: off his left shoulder, profile, eyes on the paddle between his hands.
S["s35"]["replace"] = [
    [once("s35", "close-up of Xu Yan, in his faded blue-grey scholar's robe"),
     "close-up of Xu Yan from his left side, the camera off his left shoulder, in his faded blue-grey scholar's robe"],
    [once("s35", "his face three-quarter to screen right toward the paddle under his hands, his eyes on it, never the lens;"),
     "his face in profile to screen right, bent toward the paddle under his hands, his eyes on the wet wood between his "
     "hands, never the lens;"],
    [once("s35", "his face three-quarter to screen right toward the paddle under his hands, his eyes on it, never looking at "
                 "the camera;"),
     "his face in profile to screen right, his eyes on the wet wood between his hands, never looking at the camera;"],
    [once("s35", "Xu Yan shoves hard against the paddle with both hands, and the wheel stays still,"),
     "his shoulders shove forward twice against the paddle with both hands, his eyes on the paddle the whole time, and the "
     "wheel stays still,"],
]

# s36: exactly one old man; grief by its parts; the staff's foot on the stone by the last frame.
S["s36"]["replace"] = [
    [once("s36", HAN_ID), HAN_ID_NEW],
    [once("s36", "a faded washed-out grey cotton long robe, leaning on a polished old bamboo walking staff;"),
     "a faded washed-out grey cotton long robe, with a polished old bamboo walking staff;"],
    [once("s36", "and he is the only person in the frame;"),
     "and he is the only person in the frame: exactly one person, Elder Han, alone, one white-bearded old man with one "
     "bamboo staff;"],
    [once("s36", "shaken, not smiling: his long white beard trembling, eyes wet, lips moving slowly and unsteadily between "
                 "words;"),
     "grief-stricken: the corners of his mouth turned down, his chin trembling under the long white beard, eyes wet and "
     "stunned, brows drawn up in the middle, his lips staying turned down on every word, moving slowly and unsteadily, "
     f"{NOSMILE};"],
    [once("s36", "Elder Han lowers the raised staff slowly until its foot rests on the stone as he speaks,"),
     "Elder Han lowers the raised staff slowly as he speaks, and by the last frame the foot of the staff rests on the stone "
     "and his hand rests on its top,"],
]

(HERE / "spec.json").write_text(json.dumps({"base": "d1 9331101 prompt and job", "seeds": SEEDS, "priority_1": list(DUR),
                                            "priority_2": [], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
