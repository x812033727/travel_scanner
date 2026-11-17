"""e924 fix1: the retakes of picks-merged.tsv (s17, s34, s35), merged from review-picks-a/b by the coordinator's picker.
Same steps as e923 fix1: retake.py from live/st1 (the d1 edits of e924-live/spec.json are applied first), mkjobs.py for the
duration, the absolute picture paths, output_path and the scans, then preflight-prompts.py. Seeds 9241201/9241202, all 6 s
(158 frames = 6.583 s; s17 carries a18 4.24 s from behind, s34 a33 3.88 s from behind, s35 a34 4.96 s lip-synced).

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

refine-prep.py carries a fix shot's motion text from "never the mood. " to "One continuous shot." into its refine prompt, so
both separators stay exactly once (mkjobs.py checks it).

Why each shot (coordinator's decisions, frames checked by the coordinator's picker, 2026-11-17):
- s17 (A and B both RETAKE): 1101 puts her on the left (the axis is her on the right, as s04, s32, s34) with her cheek
  showing, and a hanging wooden board with three fake characters behind him the whole shot, under a stall frame of posts;
  1102 has her right but Xu Yan talks through her line (the take's babble 0.54-6.54 s) and her buns split into four.
  Now: from the first frame her back in the right foreground, facing straight away from us, head still, every strand in
  just two round buns, one ribbon each; she lifts her right sleeve and waves it once; Xu Yan listens in silence, lips
  pressed together the whole shot ("pleased with himself" goes, it read as a cue to talk); behind him only plain bare
  wooden shop fronts and smooth bare posts and the stone street (no word for anything hung up: the scan in mkjobs.py).
- s34 (A RETAKE, B 1102): 1101 puts her on the left (across the axis of s32/s35); 1102 has her right but four buns and two
  hanging braids over the nape; in neither does she hold his sleeve. Now her back in the right foreground, facing straight
  away from us, just two round buns, the nape bare and clear; her right hand grips the cuff of his left sleeve from the
  first frame and pulls once; he glances down at the pouch and back to her, lips pressed together (a33 is hers).
  "the open front" becomes "the front" (the open-word scan).
- s35 (B RETAKE, A 1101 from 1.166): in both takes her cheek and ear sit at the right edge (1101 turns to a side face
  about 4.5 s; 1102 also grows extra bowls of sugar). Her buns at the right edge (review 必改 9) are gone: the right third
  is only the soft pale plank door and the sunlit street, he is the only person, one bowl in his hands, his eyes lift past
  the right edge toward the upper floor across the street as the script says.

Fallbacks (picks-merged.tsv): s17 9241102 0.500-5.000 (last resort; his mouth moves), s34 9241102 0.750-6.584,
s35 9241101 1.166-6.584 (crop the right edge for her cheek).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]


def d1(sid):
    return json.loads(json.dumps({k: v for k, v in D1SPEC[sid].items()
                                  if k in ("drop_pictures", "drop_set", "swap_pictures", "replace")}))


BACK_OLD = ("over-the-shoulder medium shot from close behind one young woman seen only from behind, appearing only once: the "
            "back of her head with all of her black hair gathered up into two round buns set high on her head, a short pink "
            "silk ribbon wrapped around each bun, the nape of her neck bare above a pink inner collar,")
BACK_NEW = ("from the first frame, an over-the-shoulder medium shot from close behind one young woman seen only from behind, "
            "appearing only once: the back of her head with every strand of her black hair combed smooth and gathered up into "
            "just two round buns set high on her head, one bun on each side, one short pink silk ribbon wrapped around each "
            "bun, the nape of her neck bare and clear above a pink inner collar,")
TOWARD = ["the back of her head toward us the whole time,",
          "the back of her head facing straight away from us the whole time, her head still,"]
STILL = ["keeps her head still, the back of her head toward us the whole shot;",
         "keeps her head still, facing straight away from us, the back of her head toward us the whole shot;"]

S = {}

S["s17"] = d1("s17")
S["s17"]["replace"] += [
    [BACK_OLD, BACK_NEW],
    TOWARD,
    ["pleased with himself: one brow up, lips pressed shut; behind him the stone paving and the street, soft;",
     "listening to her in silence with a quiet knowing look: one brow up, his lips pressed together and still; behind him "
     "only plain bare wooden shop fronts with smooth bare wooden posts, and the grey stone-paved street, soft;"],
    ["the young woman lifts her silk sleeve and waves it once in front of her face;",
     "the young woman lifts her right silk sleeve to the height of her shoulder and waves it once, her head perfectly still;"],
    STILL,
    ["Xu Yan says nothing in this shot: his lips",
     "Xu Yan says nothing in this shot and listens to her: his lips"],
]
S["s17"]["duration_seconds"] = 6

S["s34"] = d1("s34")
S["s34"]["replace"] += [
    ["at the open front of the Xu shop:", "at the front of the Xu shop:"],
    [BACK_OLD, BACK_NEW],
    TOWARD,
    ["her right hand already holding his left sleeve from the first frame;",
     "her right arm reaching forward and her right hand already gripping the cuff of his left sleeve, on the right side of "
     "the frame, from the first frame;"],
    ["grim, not smiling: jaw set, lips pressed shut;", "grim, not smiling: jaw set, his lips pressed together;"],
    ["the young woman tugs his sleeve once, hard;",
     "the young woman pulls his left sleeve toward her once, hard, her hand gripping the cuff the whole shot;"],
    STILL,
    ["his eyes drop to the cloth pouch in his hand and come back to her,",
     "he glances down at the cloth pouch in his right hand and then lifts his eyes back to her,"],
]
S["s34"]["duration_seconds"] = 6

S["s35"] = d1("s35")
S["s35"]["replace"] += [
    ["at the open front of the Xu shop:", "at the front of the Xu shop:"],
    ["his face three-quarter to screen right and tilted up past her toward the upper floor of the shop across the street, "
     "never the lens;",
     "his face three-quarter to screen right and tilted up toward the upper floor of the shop across the street beyond the "
     "right edge of the frame, never the lens;"],
    ["at the right edge of the frame, soft and cut off, the back of a young woman's head with two round buns set high, a "
     "short pink silk ribbon around each, appearing only once; behind him the pale plank door, soft;",
     "behind him the pale plank door, soft, and the right third of the frame is only the soft out-of-focus pale plank door "
     "and the sunlit stone street;"],
    ["Besides him, only the back of the young woman's head at the right edge the composition describes are in the frame; "
     "no second copy of anyone appears.",
     "He is the only person in the frame, and the one bowl in the frame is the bowl in his hands; no second copy of anyone "
     "appears."],
    ["his face three-quarter to screen right and tilted up past her toward the upper floor of the shop across the street, "
     "his eyes on it,",
     "his face three-quarter to screen right and tilted up toward the upper floor of the shop across the street, his eyes "
     "on it,"],
]
S["s35"]["duration_seconds"] = 6

(HERE / "spec.json").write_text(json.dumps({"seeds": [9241201, 9241202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
