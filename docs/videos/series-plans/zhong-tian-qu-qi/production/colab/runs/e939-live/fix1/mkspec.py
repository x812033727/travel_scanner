"""e939 fix1: the retakes of ../picks-merged.tsv (merge + fix1 agent, 2026-11-24). Why, shot by shot, in plan.md.

    python3 -I mkspec.py                       # -> spec.json (8 shots, seeds 9391301/9391302 for every shot)
    python3 -I mkjobs.py <live>/fix1           # -> <live>/fix1/prompts/*.txt, retake.json, colab-jobs.json (16 jobs, 100 s)
    python3 -I <scratchpad>/tools/check939f1.py <live>/fix1   # check939.py's assertions, rewritten for these eight shots
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix1/colab-jobs.json

As e938 fix1: the base of every job is the d1 9391101 job and prompt exactly as sent (mkjobs.py checks the sha256 and that every
d1 edit of ../spec.json for the shot is in it). That base already carries what prep939.sh / check939.py added and retake.py would
not: the append_pictures (the saddled horse head-right s11 s12, the captain's portrait s03, the spear s39, last, with their
sentence after the set clause and the header renumbered), the pool-word removal (s01-s13, s36-s40), the clear-air sentence and
the shoes (s39). The d1 job's reference_images are sent unchanged except where a shot here lists its own "pictures" (s11 adds
Doctor Bai's portrait as picture 3; s12 adds A-ling's portrait as picture 2; s38 sends only the field picture). Each replace is
asserted to be in the d1 prompt exactly once. Every shot is bought at its d1 length (= r2.py BUY). Every shot but the two riding
shots (s11 s12 keep the tracking camera: side-on at a gallop) is a static camera (e938 fix1: a push takes the knees, the bed or
the spear's head out of the frame; d1 s39 1102 pushed in and cut Diao Qi's knees).
Seeds 9391201-9391204 were the Qwen door picture: 93913xx is new for e939.

Union of the two pickers: s03 (B), s11 s12 (B), s16 (A and B), s38 s39 (A). Added after looking: s17 s20 (Xu Yan's grey outer
coat is missing in both seeds of both shots, between s14 s15 where it is large on screen and s23 where he lays it on A-ling;
s17 also draws the medicine chest as a brown sack). Not added (picks-merged.tsv says why): s21 s22 s26 (empty bedding behind,
the pillow end out of frame), s30 s32 (the toy rabbit drawn plush), s23 s35 (seated, not standing), s18 (hung cloth).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e939-dh/runpod/live/d1")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = [9391301, 9391302]
DUR = {"s03": 6, "s11": 6, "s12": 8, "s16": 6, "s17": 6, "s20": 6, "s38": 6, "s39": 6}  # d1 = BUY
STATIC = "The camera holds a static shot."
PUSH = "The camera pushes in with small amplitude at slow speed."
TRACK = "The camera is a tracking shot that follows the subject."
COAT = "an old grey cloth outer coat worn loose over his shoulders"
COAT2 = (COAT + ", a heavy coat of plain dark grey cloth, darker than his blue-grey robe, draped over both his shoulders and "
         "down his back to his knees, its wide grey front edges falling over the robe")
PAD = ("the folded dark grey-brown felt saddle pad lying flat and low on the horse's back in front of her, the front of the pad "
       "as flat and low as the rest of it, her hands with the reins resting low on the horse's neck")
CHEST = "the black lacquered wooden medicine chest, one square box with a lid, on its strap on his back"


def d1text(sid):
    return (D1 / "prompts" / f"ref-{sid}-9391101.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert d1text(sid).count(s) == 1, (sid, s[:80])
    return s


def girl(where):
    """The girl asleep in the bed (原版必修: she is in the bed when Doctor Bai comes in). Not named: no picture of hers is sent
    in s16, and naming her would ask for her face (e938 fix1)."""
    return (f"{where} the pink quilted cover drawn up over the small shape of a little girl of eight asleep in the bed, only the "
            "small rounded shape of her body under the quilt in the frame, her head on the pillow at the pillow end beyond the "
            "right edge of the frame, lying still")


AL_ID1 = ("A-ling shown in <Picture 2> keeps exactly the same face, hair and costume as the pictures: East Asian young woman of "
          "twenty, breathtaking cold beauty: long elegant brows, sharp upturned phoenix eyes lined with subtle smoky eyeliner, "
          "flawless porcelain skin, high cheekbones, tall and slender with a graceful neck and a slim waist, long glossy black hair "
          "pinned up with a single plain wooden hairpin and a few loose strands framing her face, a plain grey-white cotton dress "
          "tailored close at the waist with long sleeves, an aloof piercing gaze; ")
BAI_ID3 = ("Doctor Bai shown in <Picture 3> keeps exactly the same face, hair and costume as the pictures: East Asian old man of "
           "sixty-eight, lean and spare, white hair in a small topknot and a short white beard trimmed close at the chin, bright "
           "sharp eyes, a faded moon-white old long gown under a plain quilted cotton vest; ")

S = {sid: {"duration_seconds": DUR[sid], "replace": []} for sid in DUR}

# s03: B, both seeds: the captain grins from the first frame (1101 at 2x: 4.0, 4.7, 5.4 s a toothy smile; A saw it only before
# 2.6 s). The task file (e911 fix2): "not smiling" alone does not hold; write the hard face concretely, NOSMILE, twice. His face
# portrait stays (stern in the picture; it ties him to s02 s09); "shaken and humbled" (the embarrassed grin) is gone. A: from 5.3 s
# his face turns to the lens: three-quarter written to the last frame. Static.
S["s03"]["replace"] = [
    [once("s03", "shaken and humbled, not smiling: brows lifting, eyes lowered, lips moving low between words;"),
     "grim and stern, not smiling: jaw clenched hard, brows drawn together, the corners of his mouth pulled down, his lips tight "
     f"and moving low and hard between words, his teeth hidden behind his lips, {NOSMILE};"],
    [once("s03", "the guard captain lowers his raised right hand slowly and sweeps it down"),
     "his face staying grim, three-quarter to screen right to the last frame, the guard captain lowers his raised right hand "
     "slowly and sweeps it down"],
    [once("s03", PUSH), STATIC],
]

# s11: B, both seeds: a high western saddle front before her (the e938 fix6 problem), Doctor Bai with long loose white hair (s10
# s12 have his topknot), A-ling smiles (1102 all through), the sash hard to see. His portrait is sent (picture 3) and he is named,
# with the topknot, the beard and the chest; the pad is written flat and low twice (no saddle-horn noun: rule 18); NOSMILE.
S["s11"]["pictures"] = ["aling-portrait-l1.png", "aling-angle-a-l1.png", "baidaifu-portrait-l1.png", "set-guandao-ye-shu-l1.png",
                        "prop-zaohongma-an-r-l1.png"]
S["s11"]["replace"] = [
    [once("s11", "For the target video, <Picture 1>, <Picture 2>, <Picture 3> and <Picture 4> are referenced throughout."),
     "For the target video, <Picture 1>, <Picture 2>, <Picture 3>, <Picture 4> and <Picture 5> are referenced throughout."],
    [once("s11", "an aloof piercing gaze; the location shown in <Picture 3> is the set, keeping its layout and props. The horse "
                 "shown in <Picture 4>"),
     "an aloof piercing gaze; " + BAI_ID3 + "the location shown in <Picture 4> is the set, keeping its layout and props. The "
     "horse shown in <Picture 5>"],
    [once("s11", "a folded dark grey-brown felt saddle pad girthed with rope at a gallop toward the right,"),
     "a folded dark grey-brown felt saddle pad girthed with rope at a gallop toward the right, " + PAD + ","],
    [once("s11", "behind her shoulder, close and soft, the white hair and the squeezed-shut eyes of the old man tied on behind her, "
                 "and his two hands gripping her waist,"),
     "behind her shoulder, close and soft, Doctor Bai, the old man tied on behind her, his white hair tied up in a small topknot "
     "on his crown with a few strands blown loose, his short white beard trimmed close at the chin, his eyes squeezed shut, "
     f"{CHEST}, his face half hidden behind her shoulder, and his two hands gripping her waist,"],
    [once("s11", "cool and unhurried, not smiling: eyes level, brows still, lips moving evenly between words;"),
     "cool and unhurried, not smiling: eyes level, brows still, the corners of her mouth level, lips barely moving between "
     f"words, {NOSMILE};"],
    [once("s11", "exactly two people, the old man behind her seen only as his white hair, his shut eyes and his hands. Besides "
                 "her, only the white hair, the shut eyes and the two hands of the old man tied on behind her, and the one horse, "
                 "are in the frame;"),
     "exactly two people and one horse, Doctor Bai behind her half hidden by her shoulder. Only A-ling, Doctor Bai tied on "
     "behind her with the grey sash round both their waists, and the one horse with its flat felt pad are in the frame;"],
    [once("s11", "and it stretches out faster,"),
     "and it stretches out faster, the felt pad staying flat and low before her and the grey sash staying wound round both "
     "their waists,"],
]

# s12: A and B, both seeds: the young woman in front wears Doctor Bai's own beige quilted jacket (she was unnamed and unpictured:
# "only the shoulder and the back of the pinned-up head"), and B: the medicine chest is gone from his back. A-ling is named and
# pictured (picture 2), her dress written with its colour, side-on in front as d1 drew it; his chest on his back; she says nothing.
S["s12"]["pictures"] = ["baidaifu-portrait-l1.png", "aling-portrait-l1.png", "set-guandao-ye-shu-l1.png",
                        "prop-zaohongma-an-r-l1.png"]
S["s12"]["replace"] = [
    [once("s12", "For the target video, <Picture 1>, <Picture 2> and <Picture 3> are referenced throughout."),
     "For the target video, <Picture 1>, <Picture 2>, <Picture 3> and <Picture 4> are referenced throughout."],
    [once("s12", "a plain quilted cotton vest; the location shown in <Picture 2> is the set, keeping its layout and props. The "
                 "horse shown in <Picture 3>"),
     "a plain quilted cotton vest; " + AL_ID1 + "the location shown in <Picture 3> is the set, keeping its layout and props. "
     "The horse shown in <Picture 4>"],
    [once("s12", "at the right edge, cut by it and soft, only the shoulder and the back of the pinned-up head of the young woman "
                 "riding in front, turned forward toward the right;"),
     "at the right, riding in front, A-ling, in her plain grey-white cotton dress tailored close at the waist, a long dress of "
     "grey-white cotton quite unlike his moon-white gown and quilted vest, its long sleeves bound tight at both wrists with "
     "strips of grey cloth, dark cloth leg wraps below the hem of the dress, her long black hair pinned up with one plain "
     "wooden hairpin, riding toward the right, her face in profile to screen right, her eyes on the road ahead, her lips "
     "closed, cool and still, not smiling, never the lens;"],
    [once("s12", "the strap of the medicine chest across his chest,"), CHEST + ", its strap across his chest,"],
    [once("s12", "exactly two people and one horse, the one in front seen only as her shoulder and the back of her head. Besides "
                 "him, only the shoulder and the back of the head of the young woman in front at the right edge, and the top of "
                 "the one horse's mane, are in the frame;"),
     "exactly two people and one horse, A-ling in front in grey-white and Doctor Bai behind her in moon-white. Only A-ling, "
     "Doctor Bai tied on behind her and the top of the one horse's mane are in the frame;"],
    [once("s12", "at the end he lifts one eyelid and peeks past her shoulder, and the cool moonlight stays unchanged."),
     "at the last words he lifts one eyelid a crack to peek ahead past her shoulder; A-ling says nothing in this shot: her lips "
     "stay pressed together from the first frame to the last, no talking, no mouthing words, and the cool moonlight stays "
     "unchanged."],
]

# s16: A and B, both seeds: the bed at the right is empty (the -kong-men picture's bed is empty; 原版必修: the girl is in the bed
# when Doctor Bai comes in). 1101 also: the door open, two medicine chests (one on A-ling's back). The girl is written asleep under
# the quilt at the foot of the bed in frame, her head at the pillow end beyond the right edge (his eyes go there: 「病人在哪？」);
# not named; the door shut written twice; one chest, his; A-ling's back bare. Static (the track drifted the door open).
S["s16"]["replace"] = [
    [once("s16", "the plank door at the left shut behind them;"),
     "the plank door at the left shut behind them, its planks closed from the first frame to the last;"],
    [once("s16", "the black lacquered medicine chest on its strap on his back,"),
     CHEST + ", the one chest in the room,"],
    [once("s16", "the long grey sash draped over her left arm, her right arm under his elbow holding him up,"),
     "the long grey sash draped over her left arm, her right arm under his elbow holding him up, her back bare of any load, "
     "carrying nothing,"],
    [once("s16", "behind them, soft, the cracked plaster wall; their hands hold only what is described here; exactly two people. "
                 "Only these 2 people are in the frame;"),
     girl("behind them, soft, the cracked plaster wall, and at the right, soft and out of focus, the foot of the bed with") +
     "; their hands hold only what is described here; exactly two people standing in the room, with the little girl asleep in "
     "the bed behind them, out of focus. Only these 2 people stand in the frame, with the little girl asleep under the quilt "
     "in the bed at the right;"],
    [once("s16", "the small flame and the shadows stay unchanged."),
     "the plank door stays shut, the little girl in the bed sleeps on, still, and the small flame and the shadows stay "
     "unchanged."],
    [once("s16", TRACK), STATIC],
]

# s17: both seeds (A): Xu Yan's grey outer coat is not drawn (written, but the medium shot drops it; s14 s15 draw it large) and
# the medicine chest is a brown cloth sack (1102) or a brown wooden box (1101); Xu Yan sits (written standing). The coat written
# twice and heavier; the chest one black lacquered box; standing to the last frame. Static.
S["s17"]["replace"] = [
    [once("s17", COAT + ", standing beside the bed,"),
     COAT2 + ", standing upright on his feet beside the bed from the first frame to the last,"],
    [once("s17", "the medicine chest on his back,"), CHEST + ","],
    [once("s17", "and Doctor Bai sits down on the edge of the bed by the pillow;"),
     "and Doctor Bai sits down on the edge of the bed by the pillow; the grey outer coat stays on Xu Yan's shoulders to the last "
     "frame and Xu Yan stays standing;"],
    [once("s17", PUSH), STATIC],
]

# s20: both seeds: the grey outer coat not drawn (A); 1101 the girl looks up at him wide-eyed (A, B), both seeds a small coaxing
# smile at 2x (A; B 1102 at 5.5 s). Coat twice; the girl's eyes shut, frowning, swallowing; his face gentle and NOSMILE. Static.
S["s20"]["replace"] = [
    [once("s20", COAT + ", sitting on the near edge of the bed,"), COAT2 + ", sitting on the near edge of the bed,"],
    [once("s20", "coaxing, gentle, not smiling: brows soft, lips moving softly between words;"),
     f"coaxing, gentle and worried, not smiling: brows drawn together, lips moving softly between words, {NOSMILE};"],
    [once("s20", "her eyes half shut, frowning, swallowing;"),
     "her eyes shut tight from the first frame to the last, frowning, swallowing;"],
    [once("s20", "until the bowl is empty;"),
     "until the bowl is empty, little Xiaohe's eyes staying shut, and the grey outer coat stays on Xu Yan's shoulders to the "
     "last frame;"],
    [once("s20", PUSH), STATIC],
]

# s38: A (and the merge at 2x): both seeds grin (1101 2.5 and 5.0-5.5 s, 1102 5.7 s; B looked at 0.0/1.0/6.3 s only); 1101 a
# fourth man behind him. Owner rule: Qian Yuanwai never smiles; task file (e918 fix2, e934 fix4, e935 fix4): his face on screen
# while he talks grins every time; from behind, no face picture, unnamed, the line played as a recording (a38, voice_off) - first
# time right. His portrait and angle-a are dropped (the field picture only), a costume sentence instead, no face, mouth, eye or
# speaking words; the two men at the edges are dropped (1101's extra man stood between them); he is alone. Static.
CAP = "a tall round smooth black cap"
S["s38"]["pictures"] = ["set-gucang-wai-tian-l1.png"]
S["s38"]["replace"] = [
    [once("s38", "For the target video, <Picture 1>, <Picture 2> and <Picture 3> are referenced throughout."),
     "For the target video, <Picture 1> is referenced throughout."],
    [once("s38", "Qian Yuanwai shown in <Picture 1> and <Picture 2> (the same man from several angles) keeps exactly the same "
                 "face, hair and costume as the pictures: East Asian man of fifty, short and portly, round face, a thin "
                 "eight-shaped moustache, small narrow eyes under heavy brows, an ancient Chinese Song-dynasty rich landlord's "
                 "dark gold silk cross-collared robe woven with small round medallions and a small black cap, three gold rings "
                 "on his fingers; the location shown in <Picture 3> is the set, keeping its layout and props."),
     "The one man in this shot is a short, portly man of fifty, filmed from behind him, in an ancient Chinese Song-dynasty rich "
     "landlord's dark gold silk cross-collared robe woven with small round medallions, with long wide sleeves and a black belt, "
     f"and {CAP}, three gold rings on the fingers of his right hand; the location shown in <Picture 1> is the set, keeping its "
     "layout and props: the far ploughed fields, the small village houses and the pale morning sky."],
    [once("s38", "low-angle medium shot at the edge of the rice field: Qian Yuanwai, short and portly, in his dark gold silk "
                 "cross-collared robe woven with small round medallions, three gold rings on his fingers, already shoved his way "
                 "through to the front from the first frame, between two men of the village seen soft at the edges of the frame, "
                 "one in charcoal grey at the left and one in dark olive green at the right, framed from the waist up, his face "
                 "three-quarter to screen right toward someone out of sight beyond the right edge of the frame, never the lens; "
                 "that side of the frame is only the far ploughed fields and the edge of the rice field all the way to the edge, "
                 "and the only face seen whole is his; shrill and vicious, not smiling: eyes narrowed, mouth wide between shrill "
                 "words; behind him, soft, only the pale blue morning sky above the far fields and the small village houses; "
                 "their hands hold only what is described here; exactly three people, the two at the edges seen only from behind "
                 "and the side. Besides him, only the two men of the village at the edges of the frame the composition describes "
                 "are in the frame; no second copy of anyone appears. Facial expressions follow the action and lines described "
                 "below, not the reference pictures: the pictures fix the face, hair and costume only, never the mood."),
     "medium shot from behind him and a little to his left at the edge of the rice field, framed from the waist up with clear "
     f"space above his cap: the portly man stands in the left half of the frame with his broad back to the camera from the first "
     f"frame, the back of his cap, the back of his thick neck and his rounded shoulders in dark gold silk toward the camera, the "
     f"whole of him turned toward someone out of sight beyond the right edge of the frame; his head stays turned away from the "
     f"camera the whole shot; furious, his shoulders hunched and jerking forward; beyond him, soft, the far ploughed fields, the "
     f"small village houses and the pale blue morning sky; his hands hold only what is described here; he is the only person in "
     f"the frame. Only the portly man seen from behind is in the frame; no second copy of anyone appears. The picture fixes the "
     f"place and its light only, never the mood."],
    [once("s38", "Qian Yuanwai speaks a short Mandarin line, 「還等什麼？流寇就該吊死在田頭！」, his lips, jaw and cheeks moving "
                 "clearly with every syllable in natural talking mouth shapes, his face three-quarter to screen right toward "
                 "someone out of sight beyond the right edge of the frame, his eyes on that spot, never looking at the camera; "
                 "Qian Yuanwai thrusts his flat ringed right hand out toward the right as he shrieks, the gold rings flashing in "
                 "the morning sun,"),
     "The portly man thrusts his flat ringed right hand out toward the right at shoulder height and holds it there, his wide "
     "gold sleeve falling back from his wrist, the gold rings flashing in the morning sun, his back to the camera to the last "
     "frame,"],
    [once("s38", "Natural, realistic human motion and acting of real actors: each person keeps the identity, hair and costume of "
                 "their reference pictures, while every visible face acts the emotion written above and changes with it; the "
                 "pictures are neutral studio portraits, never copy their blank expression."),
     "Natural, realistic human motion of a real actor, his body and his wide sleeve moving with the thrust of his arm."],
    [once("s38", PUSH), STATIC],
]

# s39: A (and the merge): both seeds swing the spear at 0.4-0.8 s and from 0.8 s she holds half a shaft, the iron head down in
# the earth (B: "the spearhead down"); her face near the lens (A); 1102 pushes in and cuts his knees (B). The spear stands upright
# and whole the whole shot (the thump and the tip-across are gone); her face three-quarter to screen left twice; static.
S["s39"]["replace"] = [
    [once("s39", "the shaft bare below the head in her right hand,"),
     "the shaft bare below the head, standing upright in her right hand, its butt resting on the earth beside her right boot and "
     "its small iron spearhead high above her head, the full length of the shaft from the butt to the iron head always in the "
     "frame,"],
    [once("s39", "Qin Shuang brings the butt of the spear down on the earth with one hard thump and tips the shaft across in front "
                 "of the rope, holding it there as she speaks;"),
     "Qin Shuang lifts her chin as she speaks, her face staying three-quarter to screen left, never the lens, the long spear "
     "staying upright and whole in her right hand, its butt on the earth and its iron head at the top, the spear never turning "
     "and never shortening, to the last frame;"],
    [once("s39", PUSH), STATIC],
]

(HERE / "spec.json").write_text(json.dumps({"seeds": SEEDS, "shots": S}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({sum(DUR.values())} s per seed, {2 * sum(DUR.values())} s)")
