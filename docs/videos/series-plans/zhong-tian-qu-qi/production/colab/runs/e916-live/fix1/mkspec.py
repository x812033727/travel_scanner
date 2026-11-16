"""e916 fix1: the retakes of picks-merged.tsv (s26, s27, s32, s39, s42), merged from review-picks-a/b by the
coordinator's picker (frames pulled from both drafts of every disputed shot). Same steps as e915 fix1: retake.py from
live/st1 (the d1 edits of e916-live/spec.json are applied first), mkjobs.py for the duration, the absolute picture
paths and output_path, preflight-prompts.py. Seeds 9161201/9161202. Written under bible 拍法 18: backgrounds and props
written as what is there, no negative nouns; hands and props placed in the first-frame composition; no smile written as
concrete actions; Tang Xiaotang's back shots name her the only young woman with two buns and fix her side.

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

Why each shot:
- s26 (picks-a kept 1102 with a note, picks-b kept 1101): in both takes her raised forefinger is seen from behind as the
  back of a hand with one finger up in front of his chest, which reads as the middle finger (1102 worst: a fist with one
  finger up, dead centre). The gesture becomes an open right hand, palm toward him, waved side to side twice in front
  of her chest (擺手, "不用敲門"): no single raised finger at all, and her head stays still (a head shake would turn the
  face). After the wave he nods once with lips pressed flat (a concrete beat in place of a smile). 6 s (a25 5.68 s).
- s27 (picks-b RETAKE, picks-a kept 1102): checked frame by frame at 2.0 and 5.5 s: in 1102 the sheet overlaps the
  lantern's left third from about 1.75 s and the lantern's curved rib and shadow show through it (faint, but it is the
  "light through the paper" the review must-fix 6 forbids, and the episode's whole point is that this paper is thick).
  The sheet is placed in the left half from the first frame, the lantern at the right edge with a wide gap of dark air,
  the light catching only the sheet's right edge; the turn is a quarter turn and back, held in the left half. Static
  camera (the push let the sheet drift over the lantern). 6 s (a26 5.32 s).
- s32 (picks-a RETAKE, picks-b kept 1101): 1101 turns her head (cheek, nose) and a second hand comes down from above to
  pinch the sheet; 1102 turns the two buns into two long brown ponytails and the scholars bend flat over the table. The
  hair is written as two round buns high on the head, a short ribbon wrapped round each, the nape bare (the long hanging
  ribbons are what became ponytails); her left hand flat on the table and her right hand alone holding the sheet at
  shoulder height in front of her right shoulder, both placed in the first frame; she looks straight ahead across the
  table; the scholars stand upright and lean their heads in. 6 s (a30 4.52 s).
- s39 (both): all four takes pile four or five fat oilcloth bundles behind her: the mirrored set picture
  set-zhufa-ye-l2-flip (a full raft) beats the text "only one rolled-up empty oilcloth", and it breaks the 300 sheets
  sold out at the academy. The set picture is not sent (drop_set; five character pictures remain, so the job keeps
  pictures, and d1's relative swap_pictures entry is not carried over); the deck is written as bare bamboo end to end
  with one thin rolled-up empty oilcloth in the middle, her shoulder resting on it. 6 s (no line; storyboard 3.0 s).
- s42 (coordinator; both pickers chose 1102 with notes): the last image of the episode. In both takes the oilcloth
  packet sits against Xu Yan's arm and reads as his, and 1102 shows open flames at the far houses while s41 (1102) shows
  only black smoke. The packet is written hugged in her own left arm at the far left of the frame, on her side away from
  him; the smoke's base is hidden behind the dark roofs and the houses stand whole. 6 s (a39 4.08 s).

Not retaken (judged, see picks-merged.tsv): s07 (cart not turned, she stands on his left: the line plays, the turn is a
large move the model has not drawn in two takes), s08 (no limp and kick: the line carries the threat from behind, and a
kick from behind is a gamble), s33/s37 (purse and abacus on the table instead of at her waist: plausible for a seller at
her table, both takes of both shots do it, so the text alone is unlikely to move them; s38 ties them back at her waist).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]

PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC = "The camera holds a static shot."


def shot(sid, extra, dur=None, keep=("drop_pictures", "drop_set"), **more):
    s = {k: v for k, v in D1SPEC[sid].items() if k in keep}
    s["replace"] = D1SPEC[sid].get("replace", []) + extra
    if dur:
        s["duration_seconds"] = dur
    s.update(more)
    return s


S = {
 "s26": shot("s26", [
   ["her right hand raised at the height of her shoulder (on screen right) with one forefinger pointing up;",
    "her right hand (on screen right) raised open in front of her chest, the palm facing Xu Yan, all five fingers held "
    "together and straight;"],
   ["his eyes on her finger and then on her face, never the lens;",
    "his eyes on her open hand and then on her face, never the lens;"],
   ["the young woman wags her raised forefinger from side to side twice; Xu Yan's eyes follow the finger and then come "
    "back to her;",
    "the young woman waves her open right hand from side to side twice in front of her chest, palm toward him, a small "
    "brushing-off wave, then lowers it to her lap; Xu Yan's eyes follow the hand and then come back to her face, and he "
    "gives one slow nod with his lips pressed flat;"]], 6),
 "s27": shot("s27", [
   ["insert close-up, the shot opens directly on one slender hand in a peach-pink silk sleeve holding up one sheet of "
    "fresh plain white paper the size of a book page, thick and opaque, completely blank from its very first frame, the "
    "sheet held just to the left of one plain blank pale paper lantern hanging from a bamboo crossbar, a small candle "
    "burning inside it, the sheet lit warmly from the side by the lantern, thick and opaque, its plain matte face clean "
    "and even;",
    "insert close-up, the shot opens directly on one slender hand in a peach-pink silk sleeve rising from the lower left "
    "corner and holding up one sheet of fresh plain white paper the size of a book page in the left half of the frame, "
    "thick and opaque, completely blank from its very first frame; one round pale paper lantern with a small candle "
    "burning inside hangs from a bamboo crossbar at the right edge of the frame, a wide gap of dark night air between the "
    "lantern and the sheet; the lantern's warm light reaches the sheet from the side and catches only its right edge, "
    "the sheet's front face toward us evenly lit, plain, matte and white;"],
   ["the hand lifts the sheet a little higher beside the lantern and turns it slowly so the warm light slides across its "
    "plain blank face,",
    "the hand lifts the sheet a little higher and turns it slowly a quarter turn and back, the sheet staying in the left "
    "half of the frame and the lantern staying at the right edge with the dark gap between them the whole shot, so the "
    "warm light slides along its right edge and across its plain blank face,"],
   [PUSH, STATIC]], 6),
 "s32": shot("s32", [
   ["the back of her head with two looped buns tied with pink silk ribbons and pearl pins, two long pink silk ribbons "
    "hanging from the buns down over her shoulders, a pink inner collar at the nape of her neck and her light peach-pink "
    "silk shoulders;",
    "the back of her head with all of her black hair gathered up into two round buns set high on her head, a short pink "
    "silk ribbon wrapped around each bun and one pearl pin in each, the nape of her neck bare above a pink inner collar, "
    "and her light peach-pink silk shoulders;"],
   ["her right hand (on screen right) holding one blank sheet of fresh plain white paper up at shoulder height, the sun "
    "from the left grazing its edge, thick and opaque, plain matte white;",
    "looking straight ahead across the table at the scholars, her left hand (on screen left) resting flat on the "
    "tabletop, her right hand alone (on screen right) holding one sheet of thick plain white paper up at shoulder height "
    "in front of her right shoulder, its blank face toward the scholars, the morning sun from the left grazing its edge, "
    "thick and opaque, plain matte white; her own two hands are the only hands near the sheet;"],
   ["bending over the table shoulder to shoulder and craning to look;",
    "standing upright shoulder to shoulder on the far side of the table and leaning their heads in to look;"],
   ["the young woman holds the sheet a little higher and turns it once; the scholars push closer and crane their necks "
    "to look;",
    "the young woman holds the sheet steady at shoulder height with her right hand and tilts it a little toward the "
    "scholars, her left hand staying flat on the table; the scholars, still standing upright, lean their heads in closer "
    "to look;"]], 6),
 "s39": shot("s39", [
   ["its bow on screen right, only one rolled-up empty oilcloth lying in its middle,",
    "its bow on screen right, its deck bare green-yellow bamboo from end to end, the only things on it the three people, "
    "the lantern pole and one thin rolled-up empty oilcloth about as thick as an arm lying across its middle,"],
   ["small, curled up asleep against the one rolled-up empty oilcloth,",
    "small, sitting on the bare bamboo deck in the middle of the raft and asleep, her shoulder resting on the one thin "
    "rolled-up empty oilcloth,"]], 6, drop_set=True),
 "s42": shot("s42", [
   ["from behind the village houses on the right one thick column of black smoke rising and rolling into the pale dawn "
    "sky above the village, the red glow low on the far left horizon;",
    "from behind the village houses on the right one thick column of black smoke rising and rolling into the pale dawn "
    "sky above the village, its base hidden behind the dark roofs, the houses themselves standing whole, dark and still; "
    "the red dawn glow low on the far left horizon;"],
   ["one small square packet wrapped in brown oilcloth and tied with string, the size of a book held against her in her "
    "left arm, her right hand (on screen right) gripping the grey sleeve of the young man in front of her;",
    "her own left arm (on screen left) hugging one small square packet wrapped in brown oilcloth and tied with string, "
    "the size of a book, tight against her own chest at the far left of the frame, on her side away from him; her right "
    "hand (on screen right) reaching across to grip the grey sleeve of the young man in front of her;"]], 6),
}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9161201, 9161202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
