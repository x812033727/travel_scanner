"""e938 fix1: the retakes of ../picks-merged.tsv (merge + fix1 agent, 2026-11-23). Why, shot by shot, in plan.md.

    python3 -I mkspec.py                       # -> spec.json (10 shots, seeds 9381301/9381302 for every shot)
    python3 -I mkjobs.py <live>/fix1           # -> <live>/fix1/prompts/*.txt, retake.json, colab-jobs.json (20 jobs, 118 s)
    python3 -I <scratchpad>/tools/check938f1.py <live>/fix1   # check938.py's assertions, rewritten for these ten shots
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix1/colab-jobs.json

As e937 fix1: the base of every job is the d1 9381101 job and prompt exactly as sent (mkjobs.py checks the sha256 and that every
d1 edit of ../spec.json for the shot is in it). That base already carries what prep938.sh added and retake.py would not: the
append_pictures (the spear prop s12, the horse prop s20 s22 s27 and the captain's portrait s27, last, with their sentence after
the set clause and the header renumbered), the pool-word removal (s20-s27), the clear-air sentence and the shoes; the d1 job's
reference_images are sent unchanged except where a shot here says otherwise (s12 adds A-ling's portrait as picture 2; s22 s27
swap the gate crop for the wider free crop set-chengmen-ye2-zha2-l1). Each replace is asserted to be in the d1 prompt exactly once.
Every shot is bought at its d1 length (= r2.py BUY). Every shot is a static camera (s01: the push took his knees out of the frame).
Seeds 9381201/9381202 were the coordinator's Qwen edits: 93813xx is new for e938.

Coordinator's list (the union of A and B plus judgement): s01, s05, s11, s12, s14, s15, s15b (the empty bed), s22 + s27 (the
barrier between the horse and the side door). Added after looking: s20 (the horse trots and stops; the one open-road gallop).
Not added (picks-merged.tsv says why): s03, s18, s24, s26.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live/d1")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = [9381301, 9381302]
DUR = {"s01": 6, "s05": 6, "s11": 6, "s12": 8, "s14": 6, "s15": 6, "s15b": 6, "s20": 5, "s22": 5, "s27": 5}  # d1 = BUY
STATIC = "The camera holds a static shot."
PUSH = "The camera pushes in with small amplitude at slow speed."
CANDLE = "the one white candle on the low stool at the foot of the bed unlit"


def d1text(sid):
    return (D1 / "prompts" / f"ref-{sid}-9381101.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert d1text(sid).count(s) == 1, (sid, s[:80])
    return s


def girl(where):
    """The girl asleep in the bed behind the speaker, out of focus (原版必修: she is in the bed the whole scene). Not named: no
    picture of hers is sent in these shots, and naming her would ask for her face."""
    return (f"{where} a little girl of eight with two little pigtails asleep in it, lying on her back in the bed under the pink "
            "quilted cover, her head on the pink pillow, her face flushed red, one folded damp white cloth across her forehead, "
            "her eyes shut")


S = {sid: {"duration_seconds": DUR[sid], "replace": []} for sid in DUR}

# s01: A and B, both seeds failed: the room mirrored (pillow left), two girls in the bed (1102), squatting not kneeling, the cloth
# on her chest, the candle lit by day. The coordinator: two people, one child (twice); pillow at screen right; both knees and
# shins on the floor in a wide that does not push; the cloth already on her forehead in the first frame; the candle out by day.
S["s01"]["replace"] = [
    [once("s01", f"the room grey and still, {CANDLE}: wide shot at the bedside, one shallow wooden basin of water on the floor "
                 "soft in the lower foreground:"),
     f"the room grey and still, {CANDLE}, its wick dark and cold, the grey daylight from the small window the only light in the "
     "room: wide shot at the bedside from a low camera at the height of the bed, square to the bed, the whole bed across the "
     "frame with its pillow end at screen right and its foot at screen left, one shallow wooden basin of water on the floor by "
     "the foot of the bed at screen left:"],
    [once("s01", "one folded damp white cloth across her forehead, a small woven straw rabbit lying beside her pillow, her eyes shut,"),
     "one folded damp white cloth already lying across her forehead from the first frame, a small woven straw rabbit lying "
     "beside her pillow, the only child in the bed, her eyes shut,"],
    [once("s01", "kneeling on the clear floor at the near side of the bed by its pillow end, Xu Yan,"),
     "kneeling upright on the clear floor at the near side of the bed by its pillow end at screen right, Xu Yan,"],
    [once("s01", "framed full figure with both knees on the floor, his right hand already holding one folded damp white cloth, "
                 "freshly wrung, just above her forehead from the first frame,"),
     "framed full figure with both knees on the floor, both his knees and both his shins flat on the floorboards, his whole "
     "body from his head to his feet inside the frame from the first frame to the last, his right hand already holding a "
     "second folded damp white cloth, freshly wrung, a hand's breadth above her forehead from the first frame,"],
    [once("s01", "exactly two people. Only these 2 people are in the frame; no second copy of anyone appears."),
     "exactly two people: Xu Yan kneeling and one little girl alone in the bed. Only these 2 people are in the frame, Xu Yan "
     "kneeling on the floor and little Xiaohe, the only child, lying alone in the bed; no second copy of anyone appears."],
    [once("s01", "Xu Yan lays the cloth gently across her forehead and smooths it down with his palm as he speaks;"),
     "Xu Yan lays the fresh cloth gently on her forehead and smooths it down with his palm as he speaks, staying on both knees "
     "to the last frame;"],
    [once("s01", PUSH), STATIC],
]

# s05: both seeds drew a small table by the pillow with a burning candle (late afternoon). A: in a chin-up close-up the stool is
# out of frame, so the candle clause only grows a table candle: drop it; the background is the pillow, the bed head, a bare wall.
S["s05"]["replace"] = [
    [once("s05", f"the room dim and warm, {CANDLE}: close-up of little Xiaohe"), "the room dim and warm: close-up of little Xiaohe"],
    [once("s05", "behind her, soft, only the pink pillow, the dark wooden bed head and the plaster wall in the warm orange light;"),
     "behind her, soft, only the pink pillow filling the space on both sides of her head, the dark wooden bed head and the bare "
     "plaster wall in the warm orange light;"],
    [once("s05", PUSH), STATIC],
]

# s11: the pillow end of the bed is behind him and the pillow is empty (B; the coordinator). The candle clause dropped as in s05
# (1101 drew it lit by the pillow).
S["s11"]["replace"] = [
    [once("s11", f"the room dim and warm, {CANDLE}: close-up of Xu Yan"), "the room dim and warm: close-up of Xu Yan"],
    [once("s11", "he is the only person in the frame; grim,"),
     "exactly two people: Xu Yan, and the little girl asleep in the bed behind him, soft and out of focus; grim,"],
    [once("s11", "behind him, soft, only the pillow end of the bed, the bed head and the plaster wall in the warm orange light; "
                 "their hands hold only what is described here. No second copy of anyone appears."),
     girl("behind him, soft and out of focus, the pillow end of the bed with") + ", the bed head and the plaster wall in the "
     "warm orange light; their hands hold only what is described here. Only these 2 people are in the frame, Xu Yan in focus "
     "and the little girl asleep in the bed behind him, out of focus; no second copy of anyone appears."],
    [once("s11", "Xu Yan's clenched fist slowly loosens at his side;"),
     "Xu Yan's clenched fist slowly loosens at his side while the little girl in the bed behind him sleeps on, still;"],
    [once("s11", PUSH), STATIC],
]

# s12: the bed in the frame and empty; 1101 an extra grey figure at the left edge, 1102 the door open and a second Qin Shuang.
# The coordinator: the door shut, A-ling inside by the door, only two clear people. The over-the-shoulder man (Xu Yan's shoulder)
# is gone: it was the extra figure; Qin Shuang speaks to him beyond the right edge. A-ling, clear in d1 1101 and in the next shot,
# is named and pictured (her portrait as picture 2, the d1 pictures renumbered by mkjobs.py).
AL_ID = ("A-ling shown in <Picture 2> keeps exactly the same face, hair and costume as the pictures: East Asian young woman of "
         "twenty, breathtaking cold beauty: long elegant brows, sharp upturned phoenix eyes lined with subtle smoky eyeliner, "
         "flawless porcelain skin, high cheekbones, tall and slender with a graceful neck and a slim waist, long glossy black hair "
         "pinned up with a single plain wooden hairpin and a few loose strands framing her face, a plain grey-white cotton dress "
         "tailored close at the waist with a cloth sash and long sleeves, an aloof piercing gaze; ")
S["s12"]["pictures"] = ["qinshuang-portrait-l1.png", "aling-portrait-l1.png", "set-xujia-tangfang-kong-men-l1.png",
                        "prop-changqiang-l1.png"]
S["s12"]["replace"] = [
    [once("s12", "For the target video, <Picture 1>, <Picture 2> and <Picture 3> are referenced throughout."),
     "For the target video, <Picture 1>, <Picture 2>, <Picture 3> and <Picture 4> are referenced throughout."],
    [once("s12", "the location shown in <Picture 2> is the set, keeping its layout and props. The long spear shown in <Picture 3>"),
     AL_ID + "the location shown in <Picture 3> is the set, keeping its layout and props. The long spear shown in <Picture 4>"],
    [once("s12", "medium shot over a shoulder: at the right edge of the frame, cut by it, soft and out of focus, only one shoulder "
                 "and upper arm of a man in an old grey cloth outer coat, toward us the whole shot; beyond it, in the left half of "
                 "the frame, Qin Shuang,"),
     "medium shot of the corner by the door: in the left half of the frame, Qin Shuang,"],
    [once("s12", "her face three-quarter to screen right toward the man at the right edge, never the lens;"),
     "her face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, never the lens;"],
    [once("s12", "behind her at the far left, soft and out of focus, a young woman in grey-white standing still with her back to "
                 "the shut plank door, only her head and shoulders, listening, her lips closed; their hands hold only what is "
                 "described here; exactly three people, the one at the edge seen only in part, the young woman by the door soft. "
                 "Besides her, only the shoulder of the man at the right edge of the frame and the young woman in grey-white by "
                 "the shut door the composition describes are in the frame; no second copy of anyone appears."),
     "behind her at the far left, inside the room by the shut plank door, A-ling, in her plain grey-white cotton dress tailored "
     "close at the waist with a long grey cloth sash, its long sleeves down over both wrists, her long black hair pinned up with "
     "one plain wooden hairpin, standing still with her back to the shut plank door, framed from the waist up, her face "
     "three-quarter to screen right toward Qin Shuang, never the lens, listening, cold and still, not smiling, her lips closed; "
     "at the right behind them, soft and out of focus, the foot of the bed, the pink quilt drawn over the small shape of the "
     "little girl asleep in the bed; their hands hold only what is described here; exactly two people standing in the room, Qin "
     "Shuang and A-ling, with the little girl asleep in the bed behind them, soft. Only Qin Shuang and A-ling stand in the frame, "
     "with the little girl asleep under the quilt in the bed behind them; no second copy of anyone appears."],
    [once("s12", "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person, "
                 "never looking at the camera; Qin Shuang glances back once over her shoulder at the young woman by the door and "
                 "turns back,"),
     "turned toward someone out of sight beyond the right edge of the frame, face three-quarter to screen right, never looking "
     "at the camera; Qin Shuang glances back once over her shoulder at A-ling by the door and turns back,"],
    [once("s12", PUSH), STATIC],
]

# s14: the bed head and pillow behind him, the bed empty (B); 1101 smiles and the whip comes back into his hand (B). The
# coordinator: no smile; the whip handed over does not come back.
S["s14"]["replace"] = [
    [once("s14", "steady, not smiling: brows level, eyes calm, lips moving evenly between words;"),
     f"steady and grave: brows level, eyes calm, lips moving evenly between words, {NOSMILE};"],
    [once("s14", "behind him, soft, the dark wooden bed head and the plaster wall in the warm small light;"),
     girl("behind him, soft and out of focus, the pillow end of the bed with") + ", the dark wooden bed head and the plaster "
     "wall in the warm small light;"],
    [once("s14", "exactly two people, the one at the edge seen only from behind. Besides him, only the back of the young woman's "
                 "head at the left edge of the frame the composition describes is in the frame;"),
     "exactly three people, the one at the edge seen only from behind and the little girl asleep in the bed behind him, out of "
     "focus. Besides him, only the back of the young woman's head at the left edge of the frame and the little girl asleep in "
     "the bed behind him, out of focus, are in the frame;"],
    [once("s14", "Xu Yan presses the bamboo handle of the whip into the young woman's hand at the left edge and lets go as he speaks,"),
     "Xu Yan presses the bamboo handle of the whip into the young woman's hand at the left edge and lets go of it as he speaks; "
     "her hand closes on the handle and the whip goes with her hand, his right hand drops empty to his side and stays empty to "
     "the last frame,"],
    [once("s14", PUSH), STATIC],
]

# s15, s15b: the bed behind him and empty (B). The text said "behind him only the wall and the window"; the picture (-kong-chuang)
# is the bed, so the bed is written, with the girl asleep in it. s15b 1101 smiles (B): NOSMILE.
for sid, mood in (("s15", "uneasy, not smiling: brows tight, lips pressed shut;"),
                  ("s15b", "quietly certain, not smiling: brows easing, lips pressed shut;")):
    S[sid]["replace"] = [
        [once(sid, f"he is the only person in the frame; {mood}"),
         "exactly two people: Xu Yan, and the little girl asleep in the bed behind him, soft and out of focus; "
         + (mood if sid == "s15" else f"quietly certain: brows easing, lips pressed shut in one flat line, {NOSMILE};")],
        [once(sid, "behind him, soft, only the plaster wall and the dark blue window; their hands hold only what is described "
                   "here. No second copy of anyone appears."),
         girl("behind him, soft and out of focus, the bed under the dark blue window with") + ", the pillow at the right; "
         "their hands hold only what is described here. Only these 2 people are in the frame, Xu Yan in focus and the little "
         "girl asleep in the bed behind him, out of focus; no second copy of anyone appears."],
        [once(sid, PUSH), STATIC],
    ]
S["s15"]["replace"].append([once("s15", "his throat moves as he swallows once;"),
                            "his throat moves as he swallows once, while the little girl in the bed behind him sleeps on, still;"])
S["s15b"]["replace"].append([once("s15b", "his eyes still on the door;"),
                             "his eyes still on the door, while the little girl in the bed behind him sleeps on, still;"])

# s20: both seeds trot, 1101 stands still from 2.0 s, 1102 nearly stops at 3.0 s (A, B). The only open-road gallop of the ride.
S["s20"]["replace"] = [
    [once("s20", "already galloping in from the right edge from the first frame, seen side-on,"),
     "already at a flat-out gallop from the first frame, coming in at the right edge, seen side-on, its legs stretched long, its "
     "mane and tail streaming flat behind it,"],
    [once("s20", "The horse gallops across the frame from right to left along the path at the foot of the poplars and on toward "
                 "the left edge, dust billowing behind it,"),
     "The horse gallops flat out across the whole frame from right to left along the path at the foot of the poplars, its "
     "hooves pounding, never slowing, reaching the left edge as the shot ends, dust billowing behind it,"],
    [once("s20", PUSH), STATIC],
]

# s22 + s27, one camera: in d1 the horse stood on our side of the barrier, the side door open to it (A; B s27). In the picture the
# side door is on our side of the barrier and the road runs back along the foot of the wall beyond it (s27b writes it so, and s27b
# 1101 lands the horse on the side-door side). So the horse is written beyond the barrier, on that road, and the barrier between
# the horse and the side door, twice. The wider free crop -zha2 leaves room beyond the stakes. s27 is seen side-on (rule 41
# allows side or side-rear; side-rear needs a camera on the road side looking at the door, a picture we do not have).
CAPTAIN = ("the guard captain, a middle-aged man with a square face and a short black beard, in black iron lamellar armour with "
           "small red studs, a round iron helmet with cheek flaps that leaves his whole face bare and a small tuft of red horsehair "
           "on its crown, framed full figure, small, already flinching back from the first frame, his face toward the horse, never "
           "the lens, his mouth wide in alarm;")
HORSE = ("one chestnut-red horse, its mane and tail the same deep red-brown as its body, a plain dark leather bridle and an old "
         "plain brown leather saddle on a folded dark cloth,")
SIDE = ("at the left the swung-out small side door of studded planks on the paving on our side of the barrier, with one torch "
        "fixed upright in an iron holder beside it, nobody holding it; the long waist-high barrier of crossed wooden stakes "
        "running across the middle of the frame from the foot of that torch out to the right edge, standing between the horse "
        "and the side door; beyond the barrier, on the road along the foot of the long city wall, on the far side of the stakes "
        "from the side door, ")
for sid in ("s22", "s27"):
    S[sid]["swap_pictures"] = {"set-chengmen-ye2-zha-l1.png": "set-chengmen-ye2-zha2-l1.png"}
S["s22"]["replace"] = [
    [once("s22", "wide shot at the barrier, like the picture: at the left edge the swung-out small side door of studded planks with "
                 "one torch fixed upright in an iron holder beside it, nobody holding it; the long waist-high barrier of crossed "
                 "wooden stakes standing across the paved road in front of the side door; on the road side of the barrier, " + HORSE
                 + " already reined in hard three steps short of the barrier from the first frame, seen side-on with its head "
                 "toward the left,"),
     "wide shot at the barrier from the side-door side, like the picture: " + SIDE + HORSE + " already reined in hard three steps "
     "short of the barrier from the first frame, seen side-on with its head toward the left, its legs seen through the crossed "
     "stakes,"],
    [once("s22", "Besides her, only the one horse is in the frame;"),
     "Besides her, only the one horse is in the frame, the horse beyond the barrier and the side door on our side of it;"],
    [once("s22", "The horse tosses its head and stamps its forefeet on the spot,"),
     "Beyond the barrier the horse tosses its head hard and stamps its forefeet on the spot,"],
    [once("s22", PUSH), STATIC],
]
S["s27"]["replace"] = [
    [once("s27", "wide shot from behind and a little to the side at the barrier, the whole charge inside the frame: at the left the "
                 "swung-out small side door of studded planks with one torch fixed upright in an iron holder beside it, nobody "
                 "holding it; the long waist-high barrier of crossed wooden stakes standing across the paved road before it; on "
                 "the road side of the barrier, " + HORSE + " already charging at full gallop away from us toward the barrier at "
                 "the left from the first frame, seen from behind and a little to the side, its head toward the left,"),
     "wide shot at the barrier from the side-door side, the same place as the shot before, the whole charge inside the frame: "
     + SIDE + HORSE + " already at a flat-out gallop from the first frame, coming in from the right edge and charging toward the "
     "left straight at the barrier where it meets the wall by the torch, seen side-on, its head toward the left, its legs "
     "stretched long, its mane flying,"],
    [once("s27", "beyond the barrier, by the side door, " + CAPTAIN),
     "on our side of the barrier, at its near end by the torch and the side door, " + CAPTAIN],
    [once("s27", "Only A-ling on the horse, the guard captain behind the barrier and the one horse are in the frame;"),
     "Only A-ling on the horse beyond the barrier, the guard captain on our side of it by the side door and the one horse are in "
     "the frame;"],
    [once("s27", "The horse pounds across the paving straight toward the barrier, closing in stride by stride, still two strides "
                 "short of the stakes with all four hooves on the ground as the shot ends, while the guard captain throws himself "
                 "aside;"),
     "The horse pounds flat out along the road straight at the barrier, its head low, its mane flying, closing in stride by "
     "stride, still two strides short of the stakes with all four hooves on the ground as the shot ends, while the guard "
     "captain throws himself aside toward the left;"],
    [once("s27", PUSH), STATIC],
]

(HERE / "spec.json").write_text(json.dumps({"seeds": SEEDS, "shots": S}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({sum(DUR.values())} s per seed, {2 * sum(DUR.values())} s)")
