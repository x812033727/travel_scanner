"""e921 fix1: the retakes of picks-merged.tsv (s28, s36, s37), merged from review-picks-a/b by the coordinator's picker.
Same steps as e920 fix1: retake.py from live/st1 (the d1 edits of e921-live/spec.json are applied first), mkjobs.py for the
duration, the swapped and absolute picture paths, output_path and the bible 拍法 18 negative-noun scan, then
preflight-prompts.py. Seeds 9211201/9211202; s28 and s37 8 s (192 frames; a30 4.32 after the fan beat, a36 6.88), s36 6 s
(158 frames = 6.583 s, silent).

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

refine-prep.py carries a fix shot's motion text from "never the mood. " to "One continuous shot." into its refine prompt,
so every retake keeps both separators exactly once (mkjobs.py checks it), and the motion part repeats what the refine pass
must keep (the closed fan, the gathered topknot and the deep blue back, the low doorway framing).

Why each shot (frames checked by the coordinator's picker, 2026-11-16):
- s28 (A and B both 1101; retaken, coordinator's must): both takes flick the fan open at about 6.6 s and its whole face is
  brush calligraphy (fake writing, 7-8 s in full view, in 1101 and 1102 alike), while the line runs 4.38-7.84 s, so no cut
  keeps the line and loses the fan. Now the fan stays closed the whole shot: from the first frame a slim stick of dark
  bamboo ribs pressed together in his right hand, tapped twice into his open left palm after the papers go into his robe.
  The words that drew the writing (open, flick) are gone, and the fan's face is never named.
- s36 (A 1102, B 1101; retaken): the episode's exit. 1101 puts Wei Shaoqing's back in the middle of the frame with long
  hair down his back and a purplish robe, 1102 hides him behind the henchmen after 1 s. No picture of him was sent (bible
  拍法 2, as e918 fix2): the text alone named "a topknot" and the model added hair down the back. His hair is now written
  as his reference portrait has it (combed tight up from the nape into one round high topknot with the small green jade
  ornament, the nape bare, the robe's whole back clear from collar to hem), the robe as a deep royal blue, and the
  henchmen step out ahead on either side so his back stays in view. Still no picture of him.
- s37 (A and B both 1101; retaken): the closing line and the hook into e922 (storyboard: 結尾；懸念交給第 22 集). Both takes
  stand him inside the shop at eye level with shelves behind him, and in both a full-size man in black slides in from the
  right at 0.75-1.25 s (it reads as a henchman, not Xu Yan's shoulder). The set picture (the shop interior seen toward the
  door) and the long interior preamble drew him inside: both are gone (drop_set, close shot). The first frame now writes the
  low camera at floor height inside the threshold, tilted up, him on the raised threshold between the two door posts with
  the lintel above and the night street behind; the shoulder is a blue-grey cotton shoulder filling the lower right corner
  from the first frame.

Not retaken (judged, see picks-merged.tsv): the night-market backgrounds of s21b/s22b/s23, the satchel prop of s10/s11/s13,
the hanging tags and wall plaques (post blurs them), s34's sleeve grab, s35's tuck and s33's fan turn.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]

FAN = ("one closed folding fan held upright in his right hand like a short slim stick, its dark bamboo ribs pressed tight "
       "together")
WEI_BACK = ("his black hair combed smooth and tight up from the nape and gathered into one neat round topknot high on the "
            "crown of his head with a small green jade ornament at its front, the back of his neck bare above his collar, "
            "the whole back of his robe clear from the collar down to the hem; his long robe a deep royal-blue silk brocade, "
            "the deep pure blue of lapis, woven with blue cloud scrolls and gold-thread scrolls across both shoulders")
NIGHT_SHOP = ("In the Xu family shop in the county town at nightfall: tall dark wooden shelves along the left wall above a long "
              "low dark wooden cabinet, the wide open front doorway in the middle of the back wall between dark wooden "
              "lattice panels with the county town street beyond it, plain white panelled walls on the right with one long "
              "waist-high counter of plain dark wood with a thick flat top and a plain panelled front standing along them, "
              "two small brass oil lamps on tall round bases with teardrop flames burning on its top, a floor of large grey "
              "stone tiles and dark wooden beams overhead; the shelves standing completely bare; the shop lit only by the "
              "two oil lamps on the counter, their warm light on the faces near it, the far corners dim and blue, the street "
              "beyond the doorway dark blue with night, one round red paper lantern glowing beyond the doorway: "
              "low-angle medium close-up from the height of the threshold: ")


def d1(sid):
    return {k: v for k, v in D1SPEC[sid].items() if k in ("drop_pictures", "drop_set", "swap_pictures", "replace")}


S = {}

S["s28"] = d1("s28")
S["s28"]["replace"] = S["s28"].get("replace", []) + [
    ["holding flat against his chest in his left hand from the first frame one neat stack of folded cream papers, the closed "
     "fan in his right hand;",
     "holding flat against his chest in his left hand from the first frame one neat stack of cream papers folded shut, and "
     "from the first frame " + FAN + ";"],
    ["Wei Shaoqing slips the stack of papers into the front fold of his robe at his chest, his left hand coming out empty and "
     "resting on his chest; then he flicks the fan open with his right hand and speaks, smiling;",
     "Wei Shaoqing slips the stack of folded papers into the front fold of his robe at his chest, his left hand coming out "
     "empty and turning palm up in front of his chest; then he taps the closed fan lightly into his left palm twice and "
     "speaks, smiling; the fan stays one slim closed stick of dark bamboo ribs in his right hand from the first frame to the "
     "last;"],
]
S["s28"]["duration_seconds"] = 8

S["s36"] = d1("s36")
S["s36"]["replace"] = S["s36"].get("replace", []) + [
    ["in the middle one young man in a sapphire-blue brocade robe woven with gold thread seen only from behind, appearing "
     "only once, walking toward the doorway, fanning himself, only his back and the back of his head with a topknot showing;",
     "in the middle of the doorway one slender young man seen only from behind, appearing only once, walking toward the "
     "threshold, fanning himself with his right hand at his shoulder: " + WEI_BACK + ";"],
    ["ahead of him two burly men", "ahead of him on either side of the doorway two burly men"],
    ["the young man in blue walks to the threshold and stops on it;",
     "the young man in deep royal blue walks up the middle to the threshold and stops on it, the two burly men stepping out "
     "on either side of him so his whole back stays in view: his neat high round topknot with the green jade ornament, his "
     "bare nape and the deep blue back of his robe clear from collar to hem;"],
]
S["s36"]["duration_seconds"] = 6

S["s37"] = {"replace": D1SPEC["s37"]["replace"] + [
    [NIGHT_SHOP,
     "At the wide front doorway of the Xu family shop at nightfall: low-angle medium close-up, the camera low near the "
     "stone floor just inside the shop and tilted up at the doorway: "],
    ["standing side-on on the threshold of the wide front doorway at night, framed from the waist up with clear space above "
     "his head, his left shoulder toward the street, his face turned back toward the shop, the closed fan in his right hand; "
     "the dark shoulder of one young man seen only from behind, appearing only once, a dark silhouette against the lamp "
     "light in the soft right foreground;",
     "standing side-on high on the raised dark wooden threshold of the wide front doorway at night, seen from below, the two "
     "dark wooden door posts rising on either side of him to the top of the frame and the dark lintel beam above his head, "
     "framed from the waist up with clear space above his head, his left shoulder toward the street, his face turned back "
     "down toward the shop, " + FAN + "; from the first frame to the last the soft dark shoulder of one young man in a "
     "blue-grey cotton robe, seen only from behind, appearing only once, fills the lower right corner of the frame, a dark "
     "silhouette against the lamp light;"],
    ["Wei Shaoqing points the closed fan past the young man's shoulder",
     "Wei Shaoqing stays standing on the raised threshold, seen from below against the dark blue night street, and points "
     "the closed fan down past the young man's shoulder"],
], "drop_set": True, "duration_seconds": 8}

(HERE / "spec.json").write_text(json.dumps({"seeds": [9211201, 9211202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
