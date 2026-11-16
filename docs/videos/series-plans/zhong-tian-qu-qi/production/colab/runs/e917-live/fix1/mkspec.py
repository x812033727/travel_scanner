"""e917 fix1: the retakes of picks-merged.tsv (s13, s17, s21), merged from review-picks-a/b by the coordinator's
picker. Same steps as e916 fix1: retake.py from live/st1 (the d1 edits of e917-live/spec.json are applied first),
mkjobs.py for the duration, the absolute picture paths and output_path, preflight-prompts.py. Seeds 9171201/9171202.
Written under bible 拍法 18: backgrounds and props written as what is there, no negative nouns; hands and props placed
in the first-frame composition; no smile written as concrete actions.

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

Why each shot:
- s13 (both pickers RETAKE): in both takes A-ling has a knot and a wooden pin on the crown from 0.3 s to the end; the
  line (a11) runs the whole shot, so nothing can be cut round it. d1 sent her portrait (every A-ling picture has the
  high knot and pin, and the portrait's beat the text); s12 and s14, sent only aling-angle-a, came out with the hair
  loose in all four takes. So: aling-angle-a only (drop the portrait and angle-b), and the hair sentence is the two
  pickers' wording merged and written as what is there: a plain centre parting, the hair lying flat and smooth over
  the top and back of the head, two wet curtains over the front of both shoulders. Her hands are placed (empty, at
  her sides), Xu Yan's hold stays as d1 wrote it. The yard set picture stays swapped to set-xujia-yuan-huo-l1.
- s17 (picks-a RETAKE, picks-b kept 1101 with a note): 1101 puts a small copper cage (the lantern skeleton's look, a
  prop in the wrong hand) or gold box in A-ling's left hand, a tied bunch on her crown at 1.0 s, Tang Xiaotang's two
  buns turn into four flower clusters after 3.3 s and her head turns at 1.6 s, and its whole tub and clean fence do
  not read as burnt (the other nine burnt-workshop shots take the 1102 set: tub on its side burnt black, soot-black
  wall, charred posts, smoke). 1102 reads burnt and keeps Tang's head still, but A-ling's hair is tied back (the
  knot shows as she bends, 0.3-1.0 s) and the hairpin she picks up is two thin sticks like chopsticks. So: the
  burnt-workshop background written as the 1102 set looks (tub lying on its side burnt black, its staves split; the
  back wall soot-black from ground to top; tall charred posts with splintered tops; thin grey smoke), A-ling sent
  only by aling-angle-a with s13's hair sentence, her loose hair swinging forward as she bends, one single hairpin
  (one smooth stick of pale wood, one rounded end, one tapered end) lying alone on the ash in the first frame, her
  left hand open and empty at her side the whole shot; Tang's buns written as two round buns side by side with one
  ribbon each, her forehead lowered onto her knees (a reason for the head to stay down), and the abacus at her hip
  left out of this shot (a small gold thing near A-ling's hand is what 1101 drew).
- s21 (picks-b RETAKE, picks-a kept 1102 with a note): both takes press modern tread soles (ridged bars, a boot or
  trainer pattern) into the ash with no deep/shallow alternation, and this insert is the clue the audience reads;
  1101 also hangs white cloth or paper behind (the script: not one sheet left). The prints are written as flat
  cloth-soled shoes: one smooth rounded oval each, smooth flat floor, soft edges, alternating deep (a raised rim of
  ash round it) and faint; the background written as charred black poles and post feet on grey ash. 1102
  0.000-4.000 is the fallback.

Not retaken (judged, see picks-merged.tsv): the lantern skeleton changes look from shot to shot (copper cage in s20,
s26, s35; a ring with a plate in s39, s40; a small brass cylinder in s37): picked so that neighbours match, s39 and
s40 the same ring. The medium faults the pickers listed (a beat short, a gesture the other way) are accepted.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]

HAIR = ("parted plainly in the middle, the hair lying flat and smooth over the top and back of her head from the "
        "parting down to her shoulders, every strand hanging straight down in two curtains over the front of both "
        "shoulders to her chest")


def shot(sid, extra, dur=None, keep=("drop_pictures", "drop_set", "swap_pictures"), **more):
    s = {k: v for k, v in D1SPEC[sid].items() if k in keep}
    s["replace"] = D1SPEC[sid].get("replace", []) + extra
    if dur:
        s["duration_seconds"] = dur
    s.update(more)
    return s


S = {
 "s13": shot("s13", [
   ["the crown of her head smooth and bare, the wet hair falling loose over both shoulders and down her chest, a few "
    "strands stuck to her damp cheek",
    HAIR.replace("two curtains", "two wet curtains") + ", a few wet strands stuck to her damp cheek"],
   ["half turned away toward the smoke at the right, her face in profile to screen right, never the lens, lips closed;",
    "half turned away toward the smoke at the right, her face in profile to screen right, never the lens, lips closed, "
    "both of her own hands hanging open and empty at her sides;"]], 6,
   drop_pictures=["xuyan-angle-b-l1.png", "aling-portrait-l1.png", "aling-angle-b-l1.png"]),
 "s17": shot("s17", [
   ["the papermaking shed has burned down to its floor and the open pale morning sky is overhead; a few charred black "
    "posts snapped off at knee height stand up out of a floor of soft pale grey ash; long charred black bamboo poles lie "
    "across the ash; at the left one big round wooden tub burnt black, its staves split and leaning; the low stone back "
    "wall streaked black with soot from the ground to its top; a few thin wisps of white smoke rise straight up from the "
    "ash; beyond the open right side a low fence of plain bamboo stakes with one stretch knocked flat on the ground;",
    "the papermaking shed has burned down to its floor and the open pale morning sky is overhead; the floor is soft "
    "grey ash from edge to edge; at the left one big round wooden tub lying on its side, burnt black all over, its "
    "staves charred and split open; the stone back wall, as high as a man, soot-black from the ground to its top; "
    "several tall charred black posts with splintered tops stand up out of the ash; long charred black bamboo poles "
    "lie crossed on the ash; thin grey smoke rises from the ash in three or four places; beyond the back wall a fence "
    "of bamboo stakes scorched dark at its foot;"],
   ["the back of her head with two looped buns tied with pink silk ribbons and pearl pins, two long pink silk ribbons "
    "hanging from the buns down over her shoulders,",
    "the back of her head with all of her black hair gathered into two round smooth buns side by side high on the back "
    "of her head, one pink silk ribbon tied round each bun with its two long ends hanging down over her shoulders and "
    "one pearl pin in each bun,"],
   ["sitting on a low blackened stone step in the left foreground, hugging her knees, the small gold abacus hanging at "
    "her right hip;",
    "sitting on a low blackened stone step in the left foreground, both arms wrapped round her knees and her forehead "
    "lowered onto them;"],
   ["the crown of her head smooth and bare, the hair falling loose over both shoulders and down her chest", HAIR],
   ["bending over the ash with her right hand reaching down to it,",
    "bending over the ash, her loose hair swinging forward past her face, her right hand reaching down to one single "
    "plain wooden hairpin lying alone on the ash at her feet: one smooth stick of pale wood as long as her finger, "
    "rounded at one end and tapered at the other; her left hand hanging open and empty at her side;"],
   ["A-ling straightens up from the ash holding one plain wooden hairpin as long as a finger in her right hand and "
    "looks down at it;",
    "A-ling picks up the one hairpin with her right hand and straightens up, holding it across her open right palm and "
    "looking down at it, her left hand staying open and empty at her side;"]], 6,
   drop_pictures=["tangxiaotang-portrait-l1.png", "tangxiaotang-angle-a-l1.png", "tangxiaotang-angle-b-l1.png",
                  "aling-portrait-l1.png", "aling-angle-b-l1.png"]),
 "s21": shot("s21", [
   ["the shot opens directly on a line of shoe prints pressed into smooth grey ash from its very first frame, running "
    "away from the camera toward the open side at the right, every second print deep and the prints between them "
    "shallow;",
    "the shot opens directly on a line of footprints of flat cloth-soled shoes pressed into smooth grey ash from its "
    "very first frame, each print one plain smooth rounded oval with soft rounded edges and a smooth flat floor of the "
    "same fine grey ash, the line running away from the camera toward the open side at the right; the prints "
    "alternate: one sunk deep into the ash with a raised rim of ash round it, the next a faint shallow dent, then deep "
    "again, then faint again; beyond the prints long charred black bamboo poles lie on the ash and the feet of charred "
    "black posts stand in it;"],
   ["only the hand, the ash and the prints are in the frame;",
    "only the hand, the grey ash, the prints and the charred black wood are in the frame;"]], 6),
}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9171201, 9171202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
