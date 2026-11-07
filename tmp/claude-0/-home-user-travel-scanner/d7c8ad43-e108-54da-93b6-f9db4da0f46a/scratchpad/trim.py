import json, sys
path = sys.argv[1]
d = json.load(open(path, encoding="utf-8"))
R = {
 "c01": [("looking from inside toward the two lattice doors in the middle of the frame; their paper panels and the courtyard beyond are dark", "looking toward the two lattice doors in the middle of the frame, their paper panels dark"),
         ("Warm red candlelight from off screen on his face. ", "Warm red candlelight from off screen on his face. "),
         ("the plain brass lock on their inner side", "the lock on their inner side")],
 "c02": [(" Calm, level gaze; she does not smile", " Calm gaze; she does not smile"),
         ("of thirty unlabelled drawers, as tall as her shoulders and wider than her outstretched arms", "of thirty unlabelled drawers, as tall as her shoulders"),
         ("On screen right the round bronze mirror and the empty reclining chair in shadow. ", "On screen right the empty reclining chair in shadow. ")],
 "c04": [("his grey jacket shoulder and the back of his very short white hair, soft, in the foreground at the right of the frame; his face is not seen", "his grey shoulder and very short white hair, soft, in the foreground at the right of the frame, face unseen"),
         ("of thirty drawers with brass ring pulls and no labels, the cabinet as tall as her shoulders", "of thirty unlabelled drawers, as tall as her shoulders")],
 "c06": [("Then she rises slowly and steadily, back straight, and folds both hands in front of her waist, face calm and grave, not smiling.", "Then she rises slowly, back straight, and folds her hands at her waist, face grave, not smiling."),
         ("the small brass key in his right hand; his face is not seen", "the small brass key in his right hand, face unseen")],
 "c18": [("stands in front of the old medicine cabinet, hands folded, watching him", "stands by the medicine cabinet, hands folded, watching him"),
         ("End: the key hidden under the base, his hands empty, half bowed toward her.", "End: the key under the base, his hands empty, bowed toward her.")],
 "c21": [(" under warm paper-shaded lamps, the courtyard beyond the pillars dark; a red-brown", ", warm paper-shaded lamps, the courtyard dark; a red-brown"),
         ("in her moon-white high-collared cotton shirt and navy ankle-length skirt sits", "in her moon-white shirt and navy skirt sits"),
         ("Yuetang listens, grave, not smiling, mouth closed", "Yuetang listens, grave, mouth closed")],
 "c24": [(" seen low, the armrest of the long bench in the foreground; the courtyard beyond the pillars dark.", " seen low, the bench armrest in the foreground; the courtyard dark."),
         ("bangs and blazer shoulders damp, her navy pleated skirt below the knee and dry,", "bangs and blazer shoulders damp, pleated skirt below the knee and dry,"),
         ("three small brass bells on a faded red cord at its front zip", "three small brass bells at its front zip"),
         ("On the bench in the foreground, in shadow, only the folded hands and navy skirt hem of a seated young woman;", "On the foreground bench, in shadow, only a seated young woman's folded hands and skirt hem;")],
}
for k, reps in R.items():
    p = d["shots"][k]["prompt"]
    for a, b in reps:
        assert a in p, (k, a)
        p = p.replace(a, b)
    d["shots"][k]["prompt"] = p
for k, s in d["shots"].items():
    print(k, len(s["prompt"]))
open(path, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
