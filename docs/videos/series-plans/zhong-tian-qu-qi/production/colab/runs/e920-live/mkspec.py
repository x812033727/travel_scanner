"""Writes spec.json next to this file: e920 live d1 (e919-live/spec.json's way after its review: e919-live/mkspec.py).
Run: python3 -I mkspec.py

- Tang Xiaotang never shows her mouth (bible rule 3): her twelve back shots (s02, s03, s06, s08, s14, s18, s22, s24, s25,
  s28, s31, s32) drop her three face pictures and her identity sentence; the 'only' sentence says she is seen from behind and
  appears once. s37b is her one silent face: e907's neutral face sentences, and the abacus leaves her waist (it is in her
  hands). The inserts s16, s37 are her hand only.
- The guild master (MINOR, no cast.json entry): extras.json puts in his portrait under the placeholder stem
  mianshiguan-portrait-t1 (pilot.py maps a one-word id only); swap_pictures here puts refs-live/hanghui-huizhang-portrait-l1
  in its place (prep920.sh, absolute paths). The prompt text is his own (extras.json "look").
- Sets: the roof s01-s03 and the street s04, s11 drop the set picture; the shop set-xuji-pu-l1 everywhere else (gen-dh
  "Xu family shop"). The inserts s16, s37: refs-live/prop-jinsuanpan-l1 (the gold abacus prop picture,
  live-action/screen-test-e020.py) in the set slot when it exists, its clause naming the prop; until then the free floor crop
  set-xuji-pu-floor-l1, and prep920.sh keeps the two shots in colab-jobs-wait.json.
- Xu Yan's smirking angle-b goes from the serious shots (preflight smile-ref: s01, s02, s03, s31, s32, s35) and from the
  crowded ones (s12, s24, s33); A-ling's angle-b from s18 and s33.
- Sun Zhanggui's cast sentence loses "(no jade balls)" in extras.json (a negated noun, bible rule 18)."""
import json
from pathlib import Path

L = "/home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
PROP = "prop-jinsuanpan-l1.png"
HAVE_PROP = (Path(L) / PROP).is_file()

TANG_ID = ("Tang Xiaotang shown in <Picture 1>, <Picture 2> and <Picture 3> (the same woman from several angles) keeps exactly the same "
           "face, hair and costume as the pictures: East Asian young woman of eighteen, dazzling glamorous beauty: big round sparkling eyes "
           "with long lashes, glossy peach-pink lips, rosy cheeks, luminous fair skin, petite curvy figure, hair in two looped buns tied "
           "with pink silk ribbons and pearl pins, a peach-pink silk brocade ruqun: a light cross-collared short jacket wrapped shut across "
           "the chest in a low closed V, its hem at the waist covering the top of a pleated skirt tied at the waist with a ribbon bow and a "
           "small gold ornament, thick opaque silk and flowing sleeves, a small gold abacus hanging at her waist; ")
TANG_PICS = ["tangxiaotang-portrait-l1.png", "tangxiaotang-angle-a-l1.png", "tangxiaotang-angle-b-l1.png"]
FACE = ["dazzling glamorous beauty: big round sparkling eyes with long lashes, glossy peach-pink lips, rosy cheeks,",
        "a delicate beauty: big round clear eyes with long lashes, soft peach-pink lips, light rosy cheeks,"]
# s37b: the abacus is in her hands, not at her waist
NEUTRAL_HANDS = ["flowing sleeves, a small gold abacus hanging at her waist", "flowing sleeves, her resting face composed, her lips closed"]
ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."
ONLY_2 = "Only these 2 people are in the frame; no second copy of anyone appears."
ONE_TANG = "the young woman with the two high round buns appears only once"
SPEAK_GAZE = "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"
SPEAK_GAZE_HE = "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person"
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
PROP_CLAUSE = ("The small gold abacus shown in <Picture 1> is the one abacus in this shot, keeping exactly its shape, its thin gold "
               "frame, its rods and its rows of small round gold beads; the location is the grey stone floor of a shop.")
GUILD_SWAP = {"mianshiguan-portrait-l1.png": "hanghui-huizhang-portrait-l1.png"}


def back(beyond):
    return (f"Only these 2 people are in the frame, the young woman with the buns seen only from behind and {beyond} facing us "
            f"beyond her; {ONE_TANG}; no second copy of anyone appears.")


def tang_back(only_old, only_new, alone=False):
    # alone: she is the only cast.json person, so her identity sentence opened the anchor and the next clause must start the
    # sentence instead
    first = [TANG_ID + "the location", "The location"] if alone else [TANG_ID, ""]
    return {"replace": [first, [only_old, only_new]], "drop_pictures": list(TANG_PICS)}


def add(sid, key, value):
    shots[sid].setdefault(key, []).append(value) if key == "replace" else shots[sid].__setitem__(key, value)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + list(names)


def besides(pr, what):
    return (f"Besides {pr}, only {what} the composition describes are in the frame; no second copy of anyone appears.")


ids = [f"s{n:02d}" for n in range(1, 38)] + ["s37b", "s38"]
shots = {sid: {} for sid in ids}

# Tang Xiaotang from behind.
for sid in ["s02", "s03", "s24", "s31", "s32"]:
    shots[sid] = tang_back(ONLY_2, back("Xu Yan"))
shots["s18"] = tang_back(ONLY_2, back("A-ling"))
shots["s25"] = tang_back(ONLY_2, (f"Only these 2 people are in the frame, the young woman with the buns seen only from behind and "
                                  f"little Xiaohe beside her; {ONE_TANG}; no second copy of anyone appears."))
shots["s06"] = tang_back(ONLY_SHE, (f"Besides her, seen only from behind the whole shot, only the three customers across the counter "
                                    f"and the people behind them the composition describes are in the frame; {ONE_TANG}; no second "
                                    f"copy of anyone appears."), True)
shots["s14"] = tang_back(ONLY_SHE, (f"Besides her, seen only from behind the whole shot, only the two customers by the shelves are in "
                                    f"the frame; {ONE_TANG}; no second copy of anyone appears."), True)
shots["s28"] = tang_back(ONLY_SHE, (f"She is the only person in the frame, seen only from behind the whole shot; {ONE_TANG}; no second "
                                    f"copy of anyone appears."), True)
# s08 has no 'only' sentence (crowd); its identity sentence opens the anchor; the once-sentence goes in with "add".
shots["s08"] = {"replace": [[TANG_ID + "the location", "The location"]], "drop_pictures": list(TANG_PICS),
                "add": (f"The young woman with the buns is seen only from behind the whole shot; {ONE_TANG}; no second copy of "
                        f"anyone appears.")}
# s22: her sentence goes and the guild master's (put in by extras_patch.py, lower case after hers) opens the anchor.
shots["s22"] = {"replace": [[TANG_ID + "the guild master", "The guild master"],
                            [ONLY_SHE, back("the guild master")]],
                "drop_pictures": list(TANG_PICS), "swap_pictures": dict(GUILD_SWAP)}
# Her one silent face.
shots["s37b"] = {"replace": [list(FACE), list(NEUTRAL_HANDS)]}

# The guild master's portrait (placeholder stem -> his live portrait).
for sid in ["s19", "s21", "s23"]:
    shots[sid]["swap_pictures"] = dict(GUILD_SWAP)

# The unnamed backs, crowds and hands the compositions describe.
add("s07", "replace", [ONLY_SHE, besides("her", "the one woman seen from behind holding the basket")])
add("s09", "replace", [ONLY_HE, besides("him", "the shoulders and backs of the townspeople around him")])
add("s10", "replace", [ONLY_SHE, besides("her", "the backs and shoulders of the few townspeople in the doorway")])
add("s13", "replace", [ONLY_SHE, besides("her", "the soft queue on the street behind her")])
add("s20", "replace", [ONLY_HE, besides("him", "the back of the thin man's head and his shoulder in the foreground")])
add("s35", "replace", [ONLY_HE, besides("him", "the back of the tall man's head and his shoulder in the foreground")])
add("s38", "replace", [ONLY_2, ("Only these 2 people and the young man seen only from behind in the foreground are in the frame; "
                                "no second copy of anyone appears.")])

# Lines not said into a face on screen: the speaking gaze names the listener off screen or the thing looked at.
for sid, g in [
    ("s01", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her"),
    ("s09", "his face lifted toward the crowd, his eyes on them"),
    ("s34", "his face three-quarter to screen left, his eyes on the shop past the big young man"),
    ("s36", "his face three-quarter to screen left toward Xu Yan off screen left, his eyes on him"),
    ("s38", "his eyes on the counter beyond the left edge of the frame, over the young man's shoulder"),
    ("s04", "his face three-quarter to screen left toward the crowd, his eyes on them"),
    ("s11", "his face three-quarter to screen left toward the queue, his eyes on it"),
    ("s19", "his face three-quarter to screen right toward the counter beyond the right edge of the frame, his eyes on it"),
    ("s21", "his face three-quarter to screen left toward Xu Yan off screen left, his eyes on him"),
    ("s23", "his face three-quarter to screen right toward the young woman beyond the right edge of the frame, his eyes on her"),
    ("s29", "his face turned back three-quarter to screen right, his eyes on the counter beyond the right edge of the frame"),
    ("s33", "his face three-quarter to screen right, his eyes on her, then turning to screen left toward the front doorway"),
]:
    add(sid, "replace", [SPEAK_GAZE_HE, g])
for sid, g in [
    ("s10", "her face in profile to screen left toward the street outside the doorway, her eyes on it"),
    ("s13", "her face three-quarter to screen left toward Xu Yan off screen left, her eyes on him"),
    ("s17", "her face turned toward the counter beyond the right edge of the frame, her eyes on it"),
    ("s30", "her face three-quarter to screen right toward Tang Xiaotang off screen right, her eyes on her"),
]:
    add(sid, "replace", [SPEAK_GAZE, g])

# Profile pictures: the serious Xu Yan shots (smile-ref) and the crowded ones.
for sid in ["s01", "s02", "s03", "s12", "s24", "s31", "s32", "s33", "s35"]:
    drop(sid, "xuyan-angle-b-l1.png")
drop("s18", "aling-angle-b-l1.png")
drop("s33", "aling-angle-b-l1.png")

# Sets: the roof (e919 review 必改 15: no 3D roof picture in the close shots) and the street drop the set picture.
for sid in ["s01", "s02", "s03", "s04", "s11"]:
    shots[sid]["drop_set"] = True
# The inserts: the abacus prop picture once picked, else the free floor crop (its set clause unchanged).
for sid in ["s16", "s37"]:
    if HAVE_PROP:
        shots[sid]["swap_pictures"] = {"set-xuji-pu-l1.png": PROP}
        add(sid, "replace", [SET_CLAUSE, PROP_CLAUSE])
    else:
        shots[sid]["swap_pictures"] = {"set-xuji-pu-l1.png": "set-xuji-pu-floor-l1.png"}
        add(sid, "replace", [SET_CLAUSE, "T" + SET_CLAUSE[1:]])  # no person in the shot: the clause opens the sentence
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e920 live d1 (e919-live's way after its review, written by mkspec.py). Tang Xiaotang never shows her mouth: twelve "
              "back shots drop her three face pictures and her identity sentence; s37b is her silent face (neutral sentences, the "
              "abacus in her hands). The guild master's portrait goes in under the placeholder stem mianshiguan-portrait-t1 "
              "(extras.json) and is swapped for hanghui-huizhang-portrait-l1 (prep920.sh, absolute paths). Sets: no picture on "
              "the roof (s01-s03) and the street (s04, s11); set-xuji-pu-l1 in the shop; the inserts s16, s37 send the gold "
              "abacus prop picture prop-jinsuanpan-l1 when it exists (" + ("it does" if HAVE_PROP else "it does NOT yet: the "
              "floor crop set-xuji-pu-floor-l1 stands in and prep920.sh holds both shots in colab-jobs-wait.json") + "). The "
              "speaking gaze names the listener off screen or the thing looked at. No off-screen sentence is in these prompts "
              "(r2.py OFFSCREEN_SPEECH = False). Seeds 9201101/9201102."),
    "have_prop": HAVE_PROP,
    "seeds": [9201101, 9201102],
    "shots": shots,
}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots), "| prop picture:", "yes" if HAVE_PROP else "not yet")
