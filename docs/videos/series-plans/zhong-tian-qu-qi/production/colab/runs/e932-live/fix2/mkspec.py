"""e932 fix2: s01 only, the second retake of the cold open (Qin Shuang knocks Erniu's hoe away with the carrying pole).
NOT RUN: written and checked (mkjobs.py, preflight-prompts.py, check_manifest.py), nothing is sent. Why, in plan.md.

    python3 -I mkspec.py                       # -> spec.json (two variants, A and B, two seeds each)
    python3 -I mkjobs.py <live>/fix2           # -> <live>/fix2/prompts/*.txt, retake.json, colab-jobs.json (4 jobs, 20 s)
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix2/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix2/colab-jobs.json

What went wrong in fix1 9321202 (fix1/review-picks.tsv): the camera behind Erniu put the raised hoe handle and the carrying
pole on one line from the first frame ("its end already under the raised hoe handle"), so after the jerk the two shafts read
as one long pole held by both; the iron blade came off the handle and floated in the upper left 1.3-2.3 s; about nineteen
retainers. The fix is the picture, not one more sentence:
- the camera moves to the side of the two (the s02 axis: Erniu LEFT facing right, Qin Shuang RIGHT facing left, the bank of
  sacks behind them), so the two shafts are seen across, never end on; the first frame keeps them far apart (the hoe straight
  up above his head, the pole low at her hip, its end down near the earth), and they meet at one single point at a sharp angle;
- the result goes first, right after the style sentence (the model weighs the first sentences most): the whole hoe, handle and
  blade in one piece, out of the top of the frame; his two hands spread and empty above his head; the pole level across her
  chest;
- Erniu is named and sent with his pictures (erniu-portrait-l1, erniu-angle-a-l1 as in s02): a side shot shows his profile,
  so the d1 round crew-cut stranger is fixed by the pictures, not by "only the back of his head";
- the camera holds a static shot (fix1's slow push pushed him out of the left edge after 3.0 s);
- A: eye level, the s02 set crop set-shangyou-ba-fx-lu-l1, exactly fourteen retainers far and small and soft beyond the bank,
  the row ending just right of the middle; B: low angle against the hazy sky, set-shangyou-ba-fx-ding-l1 (the dam's sky crop,
  e031 s34/s36's low shots), only the near end of the retainers' row at the right edge, and the action written as three
  beats (first moment / at once / for the rest of the shot).
The axis follows r2.py THE AXES (Liuxi side LEFT, the dam RIGHT; from s02 on Erniu left of Qin Shuang) and the hoe still
leaves to the LEFT, where Xu Yan pulls it out of the earth in s04 (it lands out of the frame). The task suggested Erniu on
the right; that would flip the axis against the picked s02 (9321101: Erniu left, Qin Shuang right), so it is not used.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ST1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e932-dh/runpod/live/st1")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
REFS = "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live/"
PEOPLE = [REFS + "qinshuang-portrait-l1.png", REFS + "erniu-portrait-l1.png", REFS + "angles/erniu-angle-a-l1.png"]

s01 = (ST1 / "prompts" / "ref-s01.txt").read_text(encoding="utf-8")
s02 = (ST1 / "prompts" / "ref-s02.txt").read_text(encoding="utf-8")


def between(text, start, end):
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j]


# the header and the identity sentences of Qin Shuang (Picture 1), Wang Erniu (Pictures 2 and 3) and the set (Picture 4),
# exactly as st1 s02 has them (s02 sends the same three people pictures and the s02 set crop)
HEAD = s02[: s02.index("Initial composition: ")]
STYLE_END = "shot on a cinema camera. "
assert HEAD.count(STYLE_END) == 1 and HEAD.count("<Picture 4> is the set") == 1, "st1 s02 header changed"
FACES = between(s01, "Facial expressions follow the action", "never the mood. ") + "never the mood. "
SILENT = between(s01, "Everyone in the frame says nothing in this shot", " Every person in the frame wears")
TAIL = s01[s01.index("One continuous shot."):]
SHOES = "Qin Shuang wears her leather boots and every other person in the frame dark cloth shoes on both feet."  # d1 s01

PLACE = ("In the bamboo valley upstream of the dry Liuxi stream on the first afternoon of the drought, at the Qian family's "
         "dam, on the narrow stone-edged earth path at the foot of the bank of brown hemp sacks; hazy white afternoon "
         "sunlight, dust in the hot air: ")
ERNIU = ("on the left third of the frame Wang Erniu, in his coarse brown cross-collared short jacket with the sleeves rolled "
         "up, his black hair tied up in one small round topknot on the crown of his head, his face tanned dark from the sun, "
         "facing screen right, one hoe with a plain wooden handle and an iron blade raised straight up above his head in both "
         "hands, both fists together at the lower end of the handle just above his head, the handle standing upright and the "
         "iron blade at its top, the whole hoe inside the frame with clear sky above its blade; his face in profile to screen "
         "right, never the lens; furious, not smiling: brows knotted, jaw clenched, his lips pressed shut, " + NOSMILE + "; ")
QIN = ("on the right third of the frame, one long step away from him with clear air between them, Qin Shuang, in her fitted "
       "dark brown cross-collared short jacket cinched with a wide plain black leather belt, black trousers and leather boots, "
       "her high ponytail tied with black cord, facing screen left toward him, one plain wooden carrying pole as long as she "
       "is tall, smooth and round to its ends, held low in both her hands at her right hip, its far end down near the earth "
       "between them, the carrying pole low and the hoe high, the two shafts far apart in the first frame; her face in "
       "profile to screen left, never the lens; cold and fast, not smiling: brows level, eyes hard, lips closed; ")
RESULT = ("This shot is one blow, and it ends like this: the whole hoe, wooden handle and iron blade together in one piece, "
          "has tumbled end over end up out of the top of the frame at the upper left; Wang Erniu stands with his two hands "
          "spread wide and empty above his head; Qin Shuang holds her carrying pole level across her chest in both hands. "
          "The carrying pole and the hoe handle are two separate shafts that touch at one single point for one instant. ")

V = {
    "A": {
        "seeds": [9321301, 9321302],
        "pictures": PEOPLE + [REFS + "set-shangyou-ba-fx-lu-l1.png"],
        "result": RESULT,
        "composition": (
            PLACE + "medium wide shot at standing eye height, the camera to the side of the two of them on the path, both "
            "side-on to us and seen whole from head to boots in the lower two thirds of the frame, clear sky and bamboo "
            "hill in the upper third above them; " + ERNIU + QIN +
            "far behind them, soft and small, the bank of brown hemp sacks rising at the right and beyond its top the muddy "
            "pond, where a short row of exactly fourteen men stands in the shallow water from the right edge of the frame to "
            "just right of the middle, the fourteenth man just right of the middle and beyond him only bare muddy water and "
            "the bamboo hill; the fourteen men are in identical Song-dynasty black cross-collared short jackets, black "
            "trousers with white cloth leg wraps below the knee and black cloth head wraps, each holding one plain wooden "
            "staff upright, small and out of focus, their faces three-quarter to screen left toward the two; the narrow "
            "muddy ditch at the left; their hands hold only what is described here; exactly sixteen people; exactly one "
            "hoe, his, and exactly one carrying pole, hers. Qin Shuang and Wang Erniu each appear once; no second copy of "
            "anyone appears. "),
        "action": (
            "Qin Shuang shifts her weight onto her back foot and sweeps the carrying pole up in one fast arc from low at "
            "her right hip to high above his head: its end strikes the middle of the upright hoe handle once from the "
            "right with a hard knock, the two wooden shafts crossing at one single point at a sharp angle for one instant; "
            "the whole hoe, wooden handle and iron blade together in one piece, flips out of his hands and tumbles end over "
            "end up and away to the upper left, out of the frame past the top edge in a moment; his two hands stay up above "
            "his head, fingers spread, empty; Qin Shuang draws the carrying pole back down and holds it level across her "
            "chest in both hands to the last frame; the fourteen men far away stay where they are; "),
    },
    "B": {
        "seeds": [9321303, 9321304],
        "pictures": PEOPLE + [REFS + "set-shangyou-ba-fx-ding-l1.png"],
        "result": RESULT,
        "composition": (
            PLACE + "low-angle medium wide shot from just above the earth of the path, the camera to the side of the two of "
            "them, looking up at both side-on against the hazy white sky and the steep green bamboo hills, both seen whole "
            "from head to boots in the lower two thirds of the frame, the wide pale sky filling the upper third above them; "
            + ERNIU + QIN +
            "behind them, low along the bottom of the frame, the round lumpy top of the bank of brown hemp sacks; at the "
            "far right edge, small and soft beyond the top of the bank, the black head wraps, shoulders and upright wooden "
            "staffs of the near end of a row of the Qian family's men in Song-dynasty black cross-collared short jackets and "
            "black cloth head wraps, the rest of their row beyond the right edge of the frame; their hands hold only what "
            "is described here; Qin Shuang and Wang Erniu are the only two people in the foreground; exactly one hoe, his, "
            "and exactly one carrying pole, hers. Qin Shuang and Wang Erniu each appear once; no second copy of anyone "
            "appears. "),
        "action": (
            "In the first moment Qin Shuang dips the end of the carrying pole toward the earth and shifts her weight onto "
            "her back foot; in one fast upward sweep its end strikes the middle of the upright hoe handle once from the "
            "right with a hard knock, the two wooden shafts crossing at one single point at a sharp angle for one instant; "
            "at once the whole hoe, wooden handle and iron blade together in one piece, spins end over end high into the "
            "pale sky and leaves the frame past the top edge at the upper left; for the rest of the shot Wang Erniu stands "
            "frozen with his two hands spread wide and empty above his head, his face turned up after it, and Qin Shuang "
            "holds the carrying pole level across her chest in both hands, her eyes on him; the men at the right edge stay "
            "where they are; "),
    },
}
for v in V.values():
    v["camera"] = "The camera holds a static shot."

spec = {"shot": "s01", "duration_seconds": 5, "st1_job": "s01", "head_from": "st1 s02", "style_end": STYLE_END,
        "head": HEAD, "faces": FACES, "silent": SILENT, "shoes": SHOES, "tail": TAIL, "variants": V}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("2 variants x 2 seeds ->", HERE / "spec.json")
