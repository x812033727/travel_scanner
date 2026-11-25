"""Writes spec.json next to this file: e931 live d1 (e930-live/spec.json's way after its review, with e031's own review).
Run: python3 -I mkspec.py

- Tang Xiaotang (bible rule 40): her six back shots (s05, s06, s19, s20, s22, s30) drop her three pictures and her identity
  sentence (it also names the abacus at her waist, rule 20); the 'only' sentence says she is seen from behind and appears once.
  In the wides s04, s24 she is not a listed character (no picture is sent): the 'only' sentence names her as the young woman
  seen only from behind. s21b is her one front face: her portrait and angle-a (angle-b dropped), her identity sentence without
  the abacus.
- Xu Yan's smirking angle-b nowhere (e921 review). Where gen-dh sent only angle-a and angle-b (the close-ups s13, s15, s28, s29,
  s29b) his portrait goes first and angle-a second (e930's XU_TWO). The wides s04, s07, s08, s24, s31, s40 send his portrait only
  (s24 is in `chars` after the e031 review 建議).
- A-ling (rule 21): s01 her bare portrait and angle-a (the gauze is written as the thing, on its tie over her left ear); s03, s04
  wear the veil: aling-veil-portrait-l1 in place of her portrait, both angle pictures dropped, and her cast sentence gets the
  veil. At night (s07-s17) her bare portrait, never angle-b; the wides s07, s08 her portrait only; s11, s12 (gen-dh sent only
  the two angle pictures) her portrait first and angle-a second.
- Wang Erniu: gen-dh sends erniu-angle-a only where it sends no portrait (s25, s39): it becomes his portrait. The wides s24, s31,
  s40 his portrait only. Qian Yuanwai: never angle-b.
- No person sent: s18 (the twig), s21 (the bowl in two hands), s32 (the dam, all small and far, unnamed), s41 (Erniu's back and
  the twelve men, unnamed). The set clause opens the sentence. The two inserts s18, s21 lose the courtyard's place sentence in d1
  (bible rule 35, review 建議): "Initial composition: <H0>: " becomes "Initial composition: " and the composition opens on the
  light. video.json keeps H0 only so gen-dh's SET sends the yard picture (swapped below).
- 'Only' sentences: where the composition already says "... is the only person in the frame", the appended one is cut down to
  its second half (e927 review 建議). Where the composition describes unnamed people (the over-the-shoulder backs s10, s26, s27,
  s35; the villagers s31, s33) the 'only' sentence names them so they are allowed in the frame and not counted out.
- The speaking gaze never names an unsent listener (e927 必改 5, bible rule 31): r2.py's GAZE_REFINE (the same words in d1 and in
  the refine text); s40's replaces only Wang Erniu's (Xu Yan shouts at him, in the frame).
- Every motion that opens a sentence after "never the mood. " is capitalised (e928 review 必改 1's fix).
- Sets (r2.py PLACES): yard dusk -dong-qing2 (s04), -dong-jing (s01, s03), -dong-men2 (s02, s05), -dong-wu2 (s06); yard night
  -ye-dong2 (s07, s08), -ye-dong-jing (s09-s17); yard three months later -han (s24), -han-jing (s19), -han-wu (s20, s22, s23,
  s26, s28, s29, s29b, s30), -han-qiang (s21b, s27), -han-men (s25), -han-shu (s18), -han-di2 (s21); the dry stream set-ganxi
  (s31); the flipped dam set-shangyou-ba-fx (s32, s41) and its crops -fx-shan (s33, s39), -fx-ding (s34, s36), -fx-jiao (s35),
  -fx-tang (s37), -fx-lu (s38, s40). gen-dh's/pilot.py's set-xujia-yuan-l3, set-xujia-yuan-ye-l2 and set-liuxi-he-l1 are never
  sent. Every swap is sent with an absolute path by prep931.sh.
- No seed of this episode has been run. Seeds 9311101/9311102.
"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROD = HERE.parents[2]
L = str(PROD / "assets" / "refs-live")
VIDEO = str(PROD.parents[2] / "zhong-tian-qu-qi-e031-r2" / "video.json")
_spec = importlib.util.spec_from_file_location("r2_931_mkspec", PROD / "writer-tools" / "e031-r2" / "r2.py")
R2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R2)

TANG_BODY = ("keeps exactly the same face, hair and costume as the pictures: East Asian young woman of eighteen, dazzling glamorous "
             "beauty: big round sparkling eyes with long lashes, glossy peach-pink lips, rosy cheeks, luminous fair skin, petite curvy "
             "figure, hair in two looped buns tied with pink silk ribbons and pearl pins, a peach-pink silk brocade ruqun: a light "
             "cross-collared short jacket wrapped shut across the chest in a low closed V, its hem at the waist covering the top of a "
             "pleated skirt tied at the waist with a ribbon bow and a small gold ornament, thick opaque silk and flowing sleeves, a "
             "small gold abacus hanging at her waist; ")
TANG_ID = f"Tang Xiaotang shown in <Picture 1>, <Picture 2> and <Picture 3> (the same woman from several angles) {TANG_BODY}"
TANG_PICS = ["tangxiaotang-portrait-l1.png", "tangxiaotang-angle-a-l1.png", "tangxiaotang-angle-b-l1.png"]
ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."
ONLY_2 = "Only these 2 people are in the frame; no second copy of anyone appears."
ONLY_3 = "Only these 3 people are in the frame; no second copy of anyone appears."
NO_COPY = "No second copy of anyone appears."
ONE_TANG = "the young woman with the two high round buns appears only once"
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
YD = "set-xujia-yuan-l3.png"      # pilot.py's newest set-xujia-yuan for gen-dh's dh-set-xujia-yuan-t1
YE = "set-xujia-yuan-ye-l2.png"   # pilot.py's newest set-xujia-yuan-ye for dh-set-xujia-yuan-ye-t1
LX = "set-liuxi-he-l1.png"        # pilot.py's newest set-liuxi-he for dh-set-liuxi-he-t1
VEIL_CAST = ("an aloof piercing gaze, a veil of soft, finely woven pale grey gauze over her nose, mouth and chin, falling down to "
             "the middle of her chest")
H0 = R2.H0


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


def back(beyond, n=2):
    return (f"Only these {n} people are in the frame, the young woman with the buns seen only from behind and {beyond}; "
            f"{ONE_TANG}; no second copy of anyone appears.")


video = json.load(open(VIDEO, encoding="utf-8"))
scenes = {sc["id"]: sc for sc in video["scenes"]}
ids = [sc["id"] for sc in video["scenes"]]
assert len(ids) == 43, len(ids)
shots = {sid: {} for sid in ids}

# Tang Xiaotang from behind: her identity sentence and her three pictures leave.
ALONE = f"She is the only person in the frame, seen only from behind; {ONE_TANG}; no second copy of anyone appears."
TANG_BACK = {
    "s05": [ONLY_2, back("Xu Yan one step beyond her in the left third of the frame")],
    "s06": [ONLY_2, back("Xu Yan one step beyond her in the left third of the frame")],
    "s19": [ONLY_SHE, ALONE],
    "s20": [ONLY_2, back("Xu Yan one step beyond her in the left third of the frame")],
    "s22": [ONLY_2, back("Xu Yan one step beyond her in the left third of the frame")],
    "s30": [ONLY_3, back("Xu Yan in the left third and Wang Erniu in the right third of the frame, one step beyond her", 3)],
}
for sid, onl in TANG_BACK.items():
    add(sid, [TANG_ID, ""])
    add(sid, onl)
    drop(sid, *TANG_PICS)
add("s19", ["cinema camera. the location shown in <Picture 4>", "cinema camera. The location shown in <Picture 4>"])
# her one front face: the abacus out of her cast sentence (rule 20), angle-b out
add("s21b", [", a small gold abacus hanging at her waist; ", "; "])
drop("s21b", "tangxiaotang-angle-b-l1.png")
# the wides where she is a small back with no picture
add("s04", [ONLY_3, f"Only Wei Shaoqing, A-ling, Xu Yan and the one young woman seen only from behind in the middle foreground are in "
                    f"the frame; {ONE_TANG}; no second copy of anyone appears."])
add("s24", [ONLY_2, f"Only Wang Erniu, Xu Yan and the one young woman seen only from behind on his right are in the frame; "
                    f"{ONE_TANG}; no second copy of anyone appears."])

# No person sent: the set clause opens the sentence.
NOPERSON = ["s18", "s21", "s32", "s41"]
for sid in NOPERSON:
    add(sid, [SET_CLAUSE, "T" + SET_CLAUSE[1:]])
# rule 35: the inserts have no place sentence; the composition opens on the light and the subject
add("s18", [f"Initial composition: {H0}: bright hazy", "Initial composition: Bright hazy"])
add("s21", [f"Initial composition: {H0}: hazy low", "Initial composition: Hazy low"])

# The unnamed the compositions describe are named in the 'only' sentence.
add("s10", [ONLY_HE, "Besides him, only the one woman seen from behind at the right edge of the frame the composition describes is in "
                     "the frame; no second copy of anyone appears."])
for sid, edge in (("s26", "right"), ("s27", "left"), ("s35", "right")):
    add(sid, [ONLY_HE, f"Besides him, only the one man seen from behind at the {edge} edge of the frame the composition describes is in "
                       f"the frame; no second copy of anyone appears."])
add("s31", [ONLY_2, "Only Wang Erniu, Xu Yan and the five other people the composition describes, each in a different colour, are "
                    "in the frame; no second copy of anyone appears."])
add("s33", [ONLY_HE, "Besides him, only the white-haired old man and the boy behind him the composition describes are in the frame; "
                     "no second copy of anyone appears."])
SPECIAL_ONLY = set(TANG_BACK) | {"s04", "s24", "s10", "s26", "s27", "s35", "s31", "s33", "s21b"}
# ref2manifest's crowd test (EXTRAS) already wrote "Besides him/them, only the other people the composition names ..." here
BESIDES = {"s32", "s34", "s36", "s37", "s38", "s41"}
# the composition already says it (e927 review 建議: no doubled 'only' sentence)
for sid in ids:
    sc = scenes[sid]
    if sid in SPECIAL_ONLY or sid in BESIDES or len(sc["data"]["characters"]) != 1:
        continue
    if "is the only person in the frame" in sc["data"]["prompt"]:
        her = sc["data"]["characters"][0] in ("aling", "tangxiaotang")
        add(sid, [ONLY_SHE if her else ONLY_HE, NO_COPY])
add("s21b", [ONLY_SHE, NO_COPY])

# Lines not said into a face on screen: r2.py's direction sentences (the same in the refine text).
for sid, (pr, g) in R2.GAZE_REFINE.items():
    old = R2.GAZE_GEN[pr]
    if sid == "s40":  # Xu Yan shouts at Wang Erniu in the frame: only Erniu's gaze changes
        old = "「還我們水！」, his lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes, " + old
        g = "「還我們水！」, his lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes, " + g
    add(sid, [old, g])

# A-ling's veil (rule 21): only s03, s04 wear it.
for sid in ("s03", "s04"):
    add(sid, ["an aloof piercing gaze", VEIL_CAST])

# Every motion that opens a sentence after "never the mood. " starts with a capital.
for sc in video["scenes"]:
    sid, mo = sc["id"], sc["data"]["motion"]
    if mo.startswith("Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "):
        mo = mo.split("never the mood. ", 1)[1]
    if mo[:1].islower():
        head = mo[:24]
        # no person sent and no NOBODY opener (s32, s41): the motion follows the 'Besides them' sentence instead
        lead = "never the mood. " if sc["data"]["characters"] or sc["data"]["motion"].startswith("Throughout") else "no second copy of anyone appears. "
        add(sid, [f"{lead}{head}", f"{lead}{head[0].upper()}{head[1:]}"])

# Pictures.
XU_ALL = ["s04", "s05", "s06", "s07", "s08", "s10", "s13", "s15", "s16", "s20", "s22", "s23", "s24", "s26", "s28", "s29", "s29b",
          "s30", "s31", "s35", "s38", "s40"]
XU_TWO = ["s13", "s15", "s28", "s29", "s29b"]  # gen-dh sent angle-a and angle-b only (close-ups)
XU_WIDE = ["s04", "s07", "s08", "s24", "s31", "s40"]
for sid in XU_ALL:
    if sid not in XU_TWO:
        drop(sid, "xuyan-angle-b-l1.png")
for sid in XU_WIDE:
    drop(sid, "xuyan-angle-a-l1.png")
AL_ALL = ["s01", "s03", "s04", "s07", "s08", "s09", "s11", "s12", "s14", "s16", "s17"]
AL_TWO = ["s11", "s12"]
for sid in AL_ALL:
    if sid not in AL_TWO:
        drop(sid, "aling-angle-b-l1.png")
for sid in ["s03", "s04", "s07", "s08"]:
    drop(sid, "aling-angle-a-l1.png")
for sid in ["s24", "s31", "s40"]:  # Wang Erniu in the wides: his portrait only
    drop(sid, "erniu-angle-a-l1.png")
for sid in ["s34", "s36", "s37"]:
    drop(sid, "qianyuanwai-angle-b-l1.png")

SWAP = {sid: {} for sid in ids}
PLACE = {
    YD: {"set-xujia-yuan-dong-qing2-l1.png": ["s04"], "set-xujia-yuan-dong-jing-l1.png": ["s01", "s03"],
         "set-xujia-yuan-dong-men2-l1.png": ["s02", "s05"], "set-xujia-yuan-dong-wu2-l1.png": ["s06"],
         "set-xujia-yuan-han-l1.png": ["s24"], "set-xujia-yuan-han-jing-l1.png": ["s19"],
         "set-xujia-yuan-han-wu-l1.png": ["s20", "s22", "s23", "s26", "s28", "s29", "s29b", "s30"],
         "set-xujia-yuan-han-qiang-l1.png": ["s21b", "s27"], "set-xujia-yuan-han-men-l1.png": ["s25"],
         "set-xujia-yuan-han-shu-l1.png": ["s18"], "set-xujia-yuan-han-di2-l1.png": ["s21"]},
    YE: {"set-xujia-yuan-ye-dong2-l1.png": ["s07", "s08"],
         "set-xujia-yuan-ye-dong-jing-l1.png": ["s09", "s10", "s11", "s12", "s13", "s14", "s15", "s16", "s17"]},
    LX: {"set-ganxi-l1.png": ["s31"], "set-shangyou-ba-fx-l1.png": ["s32", "s41"],
         "set-shangyou-ba-fx-shan-l1.png": ["s33", "s39"], "set-shangyou-ba-fx-ding-l1.png": ["s34", "s36"],
         "set-shangyou-ba-fx-jiao-l1.png": ["s35"], "set-shangyou-ba-fx-tang-l1.png": ["s37"],
         "set-shangyou-ba-fx-lu-l1.png": ["s38", "s40"]},
}
seen = set()
for gen, pics in PLACE.items():
    for pic, sids in pics.items():
        for sid in sids:
            assert sid not in seen, sid
            seen.add(sid)
            SWAP[sid][gen] = pic
assert seen == set(ids), sorted(set(ids) ^ seen)
for sid in XU_TWO:
    SWAP[sid]["xuyan-angle-a-l1.png"] = "xuyan-portrait-l1.png"
    SWAP[sid]["xuyan-angle-b-l1.png"] = "angles/xuyan-angle-a-l1.png"
for sid in AL_TWO:
    SWAP[sid]["aling-angle-a-l1.png"] = "aling-portrait-l1.png"
    SWAP[sid]["aling-angle-b-l1.png"] = "angles/aling-angle-a-l1.png"
for sid in ["s03", "s04"]:
    SWAP[sid]["aling-portrait-l1.png"] = "aling-veil-portrait-l1.png"
for sid in ["s25", "s39"]:
    SWAP[sid]["erniu-angle-a-l1.png"] = "erniu-portrait-l1.png"
for sid, sw in SWAP.items():
    shots[sid]["swap_pictures"] = sw
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e931 live d1 (e930-live's way after its review, with e031's review applied; written by mkspec.py). Tang Xiaotang "
              "never speaks on camera: her six back shots (s05, s06, s19, s20, s22, s30) drop her three pictures and her identity "
              "sentence; s04, s24 name her only as the young woman seen from behind; s21b is her one front face (portrait and "
              "angle-a, no abacus; cut, not retaken, if neither seed keeps two buns and closed lips). No person sent in s18, s21, "
              "s32, s41; the inserts s18, s21 have no place sentence. A-ling: s01 her bare portrait and angle-a (the gauze written "
              "as the thing); s03, s04 the veil portrait, no angles; at night her bare portrait, never angle-b. Xu Yan's angle-b "
              "nowhere; the wides his portrait only. Sets: see mkspec.py (the dam is the flipped set-shangyou-ba-fx-l1 and its "
              "crops). No off-screen sentence (r2.py OFFSCREEN_SPEECH = False). Seeds 9311101/9311102."),
    "seeds": [9311101, 9311102],
    "shots": shots,
}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
