"""e918 fix1: the retakes of picks-merged.tsv (s35, s37, s40), merged from review-picks-a/b by the coordinator's picker.
Same steps as e917 fix1: retake.py from live/st1 (the d1 edits of e918-live/spec.json are applied first), mkjobs.py for
the duration, the absolute picture paths and output_path, preflight-prompts.py. Seeds 9181201/9181202. Written under
bible 拍法 18: what is in the frame written as what is there, no negative nouns; hands placed in the first-frame
composition; no smile written as concrete actions.

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

Why each shot (frames checked by the coordinator's picker, 2026-11-16):
- s35 (picks-a RETAKE, picks-b kept 1102): in both takes a skin-coloured hand comes out of the kneeling man's gold
  sleeve toward Xu Yan (1102 0.5-6.0 s: a hand out of the folded gold sleeve lying on top of his arm, 1101 the arm and
  hand reaching to Xu Yan's palm), and 1101 turns the head to profile after 3.8 s. The line is 「你的手怎麼一直不拿
  出來」, so his hand may not show before it. The foreground cap also grew two long black tails like an official's
  futou (the Qian pictures are not sent, 拍法 2, so the cap came from the text). So: the frame's bottom edge cuts
  the kneeling man at the shoulders (his arms stay below it), Xu Yan's own open hand is held level in the clear air
  above that shoulder, the man's head held facing away, and the cap written as a tall round smooth black cap, plain
  all the way round to its rim, the bare nape below it. Tall, not small: the portrait and s34/s36/s37 are tall.
- s37 (picks-a RETAKE, picks-b kept 1102 with a note): both takes stand straight facing the lens and grin with teeth
  while begging (1101 0.5/3.0/4.5 s, 1102 0.5/1.5 s), no sway, no bow; the hands joined at the belly. The d1 text
  had "pleading and sly" (sly reads as a grin). So: camera a little above and to his left (three-quarter to screen
  left, the stone floor behind him so the kneeling reads, unlike the eye-level s36), pale and pained written as brows,
  half-closed eyes, mouth corners down and lips over the teeth, one sway on his knees, the head bowed to the dais at
  the upper left, both forearms pressed across the belly with each cuff folded over the other sleeve.
- s40 (picks-b RETAKE, picks-a kept 1101 with a note): 1102 has a whole skin-coloured hand out of the gold sleeve
  gripping Xu Yan's arm 0.5-6.4 s; 1101 fingertips over Xu Yan's shoulder 1.0-6.4 s. Last shot of the episode, right
  after 「你的手怎麼一直不拿出來」. So picks-b's rewrite: the frame's bottom edge above both men's elbows, Qian's left
  arm along Xu Yan's right upper arm inside one continuous tube of gold silk whose end hangs out of the bottom of the
  frame, the pull done by bending that elbow; the cap written as in s35.

Not retaken: s20 (the lit candle at the lower left 0-1.4 s: a fixed 1.15x crop to the upper right removes it, see
picks-merged.tsv), s34/s36 (fingertips in the sleeve gap, small and in shadow: darken in the grade), s35's cap (done
inside the s35 retake).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]

CAP = "tall round smooth black cap, plain and smooth all the way round down to its rim"
CAP_ID = [" and a small black cap, wide sleeves, his hands hidden inside them;", " and a " + CAP + ", wide sleeves, his hands hidden inside them;"]


def shot(sid, extra, dur=None, keep=("drop_pictures", "drop_set", "swap_pictures"), **more):
    s = {k: v for k, v in D1SPEC[sid].items() if k in keep}
    s["replace"] = D1SPEC[sid].get("replace", []) + extra
    if dur:
        s["duration_seconds"] = dur
    s.update(more)
    return s


S = {
 "s35": shot("s35", [
   ["over-the-shoulder medium shot from close behind one portly man in a dark gold silk robe seen only from behind, "
    "appearing only once, kneeling in the right foreground, only the back of his tall rounded black cap, his thick neck "
    "and his right shoulder and wide sleeve showing, soft;",
    "over-the-shoulder medium shot from close behind one portly man in a dark gold silk robe seen only from behind, "
    "appearing only once, kneeling in the right foreground, the bottom edge of the frame cutting across his shoulders "
    "so both his arms stay below it: only the back of his head in a " + CAP + ", the bare back of his thick neck below the "
    "rim and the top of his right shoulder in dark gold silk showing, his head held facing away from us, soft;"],
   ["standing, framed from the waist up with clear space above his head, his right hand held out flat, palm up, toward "
    "the man's sleeves,",
    "standing, framed from the waist up with clear space above his head, his own right hand raised open at chest height, "
    "palm up, held level in the clear air above the kneeling man's shoulder, a hand's width of air between them,"],
   ["Besides him, only the back of the kneeling man's head, his shoulder and his sleeve in the foreground the composition "
    "describes is in the frame,",
    "Besides him, only the back of the kneeling man's head, his neck and the top of his shoulder in the foreground the "
    "composition describes is in the frame,"],
   ["Xu Yan moves his open hand from his side toward the man's joined sleeves; the kneeling man in the foreground keeps "
    "his head still, the back of his cap toward us the whole shot, his shoulders hunching;",
    "Xu Yan holds his open right hand level in the air above the kneeling man's shoulder, palm up, waiting; the kneeling "
    "man in the foreground keeps his head still and facing away from us, the back of his cap and his bare neck toward us "
    "the whole shot, his shoulders hunching up toward his ears;"],
   ["after the last word Xu Yan's eyes stay on the sleeves,",
    "after the last word Xu Yan's eyes stay lowered on the kneeling man, his open hand still held out level,"]], 6),
 "s37": shot("s37", [CAP_ID,
   ["and his small black cap, kneeling,", "and his " + CAP + ", kneeling,"],
   ["medium shot of Qian Yuanwai,", "medium shot from a little above him and a little to his left, looking slightly down "
    "on Qian Yuanwai, his body turned three-quarter to screen left,"],
   ["kneeling, framed from the waist up with clear space above his cap, both his hands pushed deep inside his long wide "
    "dark gold sleeves, the cuffs hanging well past his fingertips, the two sleeves joined in front of his belly, his "
    "hands hidden inside them the whole time, his face tipped up three-quarter to screen left toward the high dais above "
    "the top of the frame, never the lens; pleading and sly: brows drawn up, eyes fluttering half shut, mouth drooping "
    "between words; behind him only a dark red-brown pillar and the grey daylight.",
    "kneeling on both knees on the grey stone floor, framed from the waist up with the grey stone tiles of the floor "
    "behind him and clear space above his cap, his two forearms pressed together across his belly, both hands deep "
    "inside the long wide dark gold sleeves, each cuff folded over the other sleeve so only gold silk shows from the "
    "first frame to the last, his face three-quarter to screen left toward the high dais beyond the upper left of the "
    "frame, never the lens; pale and pained, like a man about to faint: brows pulled up and together, eyes half closed, "
    "the corners of his mouth pulled down, his lips closing over his teeth between words; behind him only a dark "
    "red-brown pillar, the stone floor and the grey daylight."],
   ["his face tipped up toward the high dais above the top of the frame, his eyes on it,",
    "his face three-quarter to screen left toward the high dais beyond the upper left of the frame, his eyes on it,"],
   ["Qian Yuanwai sways on his knees as if dizzy, presses his joined sleeves against his belly, then bows his head toward "
    "the dais; after the last word he stays bowed, his eyes sliding sideways,",
    "Qian Yuanwai sways once to one side on his knees as if dizzy and catches himself, presses his folded sleeves against "
    "his belly, then bows his head low toward the dais at the upper left, pleading in a weak whining voice with the "
    "corners of his mouth pulled down; after the last word he keeps his head bowed, his lips pressed together and pulled "
    "down at the corners, and his eyes slide sideways to the floor,"]], 6),
 "s40": shot("s40", [CAP_ID,
   ["framed from the chest up with space above his head, his face three-quarter to screen right toward the man,",
    "framed from the upper chest up with space above his head, the bottom edge of the frame cutting across both men just "
    "above the elbows, his face three-quarter to screen right toward the man,"],
   ["and his small black cap, framed from the chest up, leaning in close to him, his left forearm, in the long wide dark gold sleeve whose cuff "
    "hangs well past his fingertips, already laid over Xu Yan's right forearm from the first frame, the long cuff folded "
    "over Xu Yan's sleeve, gold silk lying on blue-grey cloth, his right hand hidden inside his right sleeve,",
    "and his " + CAP + ", framed from the upper chest up, leaning in close to him; his left arm rests along Xu Yan's "
    "right upper arm from the first frame, wrapped in one long continuous tube of dark gold silk from his shoulder to "
    "below the bottom edge of the frame, the silk smooth and unbroken all the way down, the sleeve end hanging out of "
    "the frame below; his other arm held against his own belly inside its wide gold sleeve, below the frame; the only "
    "skin showing on either man is the face and neck;"],
   ["Qian Yuanwai draws Xu Yan's forearm toward himself with his sleeve-covered forearm and leans in to his ear;",
    "Qian Yuanwai pulls Xu Yan toward himself by bending that silk-wrapped arm at the elbow and leans his round face in "
    "close to Xu Yan's ear;"]], 6),
}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9181201, 9181202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
