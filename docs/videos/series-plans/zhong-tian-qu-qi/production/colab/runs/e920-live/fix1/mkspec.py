"""e920 fix1: the retakes of picks-merged.tsv (s23, s33, s37b), merged from review-picks-a/b by the coordinator's picker.
Same steps as e919 fix1: retake.py from live/st1 (the d1 edits of e920-live/spec.json are applied first), mkjobs.py for the
duration, the swapped and absolute picture paths, output_path and the bible 拍法 18 negative-noun scan, then
preflight-prompts.py. Seeds 9201201/9201202, 6 s each (158 frames = 6.583 s; a21 4.56, a34 4.16, s37b silent).
Written under bible 拍法 15-18: what is in the frame written as what is there, no negative nouns; hands and props placed in
the first-frame composition; no smile written as concrete actions.

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

refine-prep.py carries a fix shot's motion text from "never the mood. " to "One continuous shot." into its refine prompt,
so every retake keeps both separators exactly once (mkjobs.py checks it), and the motion part repeats what the refine pass
must keep (the bundle, the empty right foreground, the long abacus and the short ribbons): the refine head comes from
clips-dh-e920.json and still carries the d1 wording.

Why each shot (frames checked by the coordinator's picker, 2026-11-16):
- s23 (picks-a 1101, picks-b RETAKE; retaken): both takes draw a stack of three or four blue thread-bound books with a white
  title slip (fake strokes, 1101 small, 1102 large). d1 wrote "one flat bundle of three books wrapped in one plain dark blue
  cotton cloth": the word books drew books. Now one square soft indigo cloth bundle, its four corners knotted on top, only
  the weave and the folds on its surface, hugged to his chest in both arms from the first frame; no word that can turn into
  a book is left. The st1 prompt of this extra had no "never the mood." sentence: it is put in (refine-prep needs it, and
  it also keeps the portrait's calm face from beating the clenched jaw).
- s33 (both RETAKE): both takes draw two A-lings, one large in the right foreground (behind the counter, where the d1 text
  put "the young woman behind the counter beyond the right edge") and one at the back door. Now Xu Yan stands alone, the
  right foreground is the bare near end of the counter with open floor behind it, his gaze goes to the far end of the
  counter (no woman named there), and the only woman is small at the back door. A-ling's two pictures are dropped and her
  name leaves the text (bible 拍法 2, as e918 fix2 s37): a woman two inches high in the back corner needs no face, and her
  sent face pictures are what pulled a full-size A-ling into the foreground; costume, bun and wooden hairpin identify her.
  Xu Yan keeps his two pictures, so "never the mood." stays.
- s37b (A: the coordinator's call, B: the prop differs; retaken): the episode's closing beat and her one face in the
  episode. 1101 is a calm open-eyed face with two long ribbons; 1102 a blank stare with a palm-sized upright abacus of three
  or four rods. d1 wrote "one small gold abacus the size of her palm (... five thin gold rods ...)": that drew the small
  upright one. Now the long flat gold abacus of prop-jinsuanpan-l1 (sent in the set picture's slot: a close-up against a
  plain wall needs no set picture, review 建議 18), held flat across her chest in both hands; the ribbons as in the back
  shots (a short ribbon wrapped round each bun); her profile picture angle-b, whose ribbon hangs longest, is dropped. The
  fear is written as actions: the colour drains from her face at once, inner brows squeezed up, lips pressed tight and
  trembling, both hands hugging the abacus to her chest.

Not retaken (judged, see picks-merged.tsv): the staging drifts both takes share (s10, s12, s35, s36) and the guild master's
book in s19, s21, s22 (no fake writing on it; post darkens the slips).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]
L = "/home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
PROP = f"{L}/prop-jinsuanpan-l1.png"
MOOD = ("Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the "
        "face, hair and costume only, never the mood. ")


def shot(sid, extra, dur=6, drop=(), swap=None):
    s = {k: v for k, v in D1SPEC[sid].items() if k in ("drop_pictures", "drop_set", "swap_pictures")}
    s["replace"] = D1SPEC[sid].get("replace", []) + extra
    if drop:
        s["drop_pictures"] = s.get("drop_pictures", []) + list(drop)
    if swap:
        s["swap_pictures"] = {**s.get("swap_pictures", {}), **swap}
    s["duration_seconds"] = dur
    return s


BUNDLE = ("one square bundle of soft dark indigo cotton cloth as wide as his chest, its four corners pulled up and tied "
          "together in one big soft knot on top, the cloth sagging into soft creases over its rounded shape, its surface "
          "plain woven indigo cotton with only the weave and the folds of the cloth on it")
ABACUS = ("one long flat gold abacus as long as her forearm, exactly as in <Picture 4>: a long narrow rectangular gold frame, "
          "a long row of thin gold rods set close side by side across its width, one thin gold crossbar running along its "
          "whole length, small round gold beads above and below the crossbar on every rod")
RIBBON = ("hair in two looped buns tied with pink silk ribbons and pearl pins",
          "hair in two round buns set high on her head, a short pink silk ribbon wrapped tight around each bun with its ends "
          "tucked into the bun, pearl pins, her neck and shoulders clear")

S = {
 "s23": shot("s23", [
   ["his right palm pressed flat on one flat bundle of three books wrapped in one plain dark blue cotton cloth and tied with "
    "a cloth strip, the cloth smooth and even on every side lying on the counter from the first frame;",
    "from the first frame hugging against his chest with both forearms " + BUNDLE + "; both his hands spread flat on the "
    "front of the soft cloth;"],
   ["their hands hold only what is described here. The guild master speaks",
    "their hands hold only what is described here. " + MOOD + "The guild master hugs the square indigo cloth bundle with "
    "its knotted corners against his chest in both arms from the first frame to the last. The guild master speaks"],
   ["presses his palm flat down on the blue cloth bundle as he speaks;",
    "squeezes the soft indigo cloth bundle tighter against his chest with both arms as he speaks, its knotted corners "
    "bobbing on top;"],
 ]),
 "s33": shot("s33", [
   ["A-ling shown in <Picture 4>, <Picture 5> and <Picture 6> (the same woman from several angles) keeps exactly the same "
    "face, hair and costume as the pictures: East Asian young woman of twenty, breathtaking cold beauty: long elegant brows, "
    "sharp upturned phoenix eyes lined with subtle smoky eyeliner, flawless porcelain skin, high cheekbones and soft red lips, "
    "tall and slender with a graceful neck and a slim waist, long glossy black hair pinned up with a single plain wooden "
    "hairpin and a few loose strands framing her face, a plain grey-white cotton dress tailored close at the waist with a "
    "cloth sash and long sleeves, an aloof piercing gaze; ", ""],
   ["medium shot: on screen left Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, standing in front of the "
    "long waist-high dark wooden counter, framed from the knees up with clear space above his head, his face three-quarter "
    "to screen right toward the young woman behind the counter beyond the right edge of the frame, never the lens; gentle "
    "and resolved: brows easing, lips moving evenly between words; in the soft background at the right, a plain dark wooden "
    "back door in the far corner of the white panelled wall, and A-ling, in her plain grey-white cotton dress with long "
    "sleeves covering her wrists, her black hair in a high bun with one plain wooden hairpin, small, the empty bucket in her "
    "right hand, her left hand already flat on the door from the first frame; their hands hold only what is described here; "
    "exactly two people.",
    "medium shot: Xu Yan stands alone on screen left in front of the long waist-high dark wooden counter that runs along the "
    "right wall, in his faded blue-grey scholar's robe patched at one elbow, framed from the knees up with clear space above "
    "his head, his face three-quarter to screen right toward the far end of the counter beyond the right edge of the frame, "
    "never the lens; gentle and resolved: brows easing, lips moving evenly between words; the right foreground is the bare "
    "near end of the counter, its flat dark top clear and the stone floor behind it open and empty; far back in the right "
    "corner of the room, small in the soft background, a plain dark wooden back door in the white panelled wall, and at it "
    "one slim young woman in a plain grey-white cotton dress with long sleeves, her black hair in a high bun with one plain "
    "wooden hairpin, an empty wooden bucket in her right hand, her left palm already flat on the door from the first frame; "
    "she is the only woman in the frame; their hands hold only what is described here; exactly two people."],
   ["his face three-quarter to screen right, his eyes on her, then turning to screen left toward the front doorway",
    "his face three-quarter to screen right, his eyes on the far end of the counter beyond the right edge of the frame, then "
    "turning to screen left toward the front doorway"],
   ["; in the background A-ling pushes the back door open and steps out, and the door swings shut behind her; A-ling says "
    "nothing in this shot: her lips stay pressed together from the first frame to the last, no talking, no mouthing words,",
    "; Xu Yan stays alone in front of the counter, the near end of the counter at the right edge of the frame bare and the "
    "floor behind it open; far back in the right corner the slim young woman in grey-white pushes the back door open with "
    "her left palm and steps through with her bucket, the door swings shut behind her and the back corner is empty,"],
 ], drop=["aling-portrait-l1.png", "aling-angle-a-l1.png"]),
 "s37b": shot("s37b", [
   list(RIBBON),
   ["flowing sleeves, her resting face composed, her lips closed", "flowing sleeves, her lips closed"],
   ["one small gold abacus the size of her palm (a thin flat gold frame, five thin gold rods, a thin gold crossbar, one "
    "small round gold bead above it and four below on every rod) clutched tight against her chest in both hands from the "
    "first frame,",
    ABACUS + ", held flat across her chest in both hands from the first frame, one hand near each end of it, her forearms "
    "pressed against it,"],
   ["the colour gone from her face: skin pale, eyes wide and fixed, brows drawn up, lips pressed together and trembling;",
    "frightened: her eyes wide and fixed on the doorway;"],
   ["the location shown in <Picture 4> is the set, keeping its layout and props.",
    "the long gold abacus shown in <Picture 4> is the one abacus in this shot, keeping exactly its long flat shape, its "
    "long row of rods and its small round gold beads."],
   ["Tang Xiaotang straightens up behind the counter, clutching the abacus tighter to her chest, her eyes fixed on the "
    "doorway;",
    "Tang Xiaotang stands behind the counter, the long gold abacus held flat across her chest in both hands, a short pink "
    "ribbon wrapped tight around each of her two high buns; in the first second the colour drains from her face all at once, "
    "her cheeks and lips turning pale; her inner brows squeeze up and together, her eyes widen and stay fixed on the doorway "
    "at screen left, her lips press tight together and tremble slightly; she hugs the long abacus tighter against her chest "
    "with both hands, her knuckles whitening, her shoulders drawing up; to the last frame her face stays pale, her brows "
    "squeezed up, her lips pressed and trembling;"],
 ], drop=["tangxiaotang-angle-b-l1.png"], swap={"set-xuji-pu-l1.png": PROP}),
}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9201201, 9201202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
