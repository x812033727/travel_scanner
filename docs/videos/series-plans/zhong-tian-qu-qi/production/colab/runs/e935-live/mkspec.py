"""Writes spec.json next to this file: e935 live d1 (e934-live/spec.json's way, with e931/e933-live's Tang Xiaotang back shots
and her one front face; writer-tools/e035-r2/r2.py's FOOT and PLACES).
Run: python3 -I mkspec.py

- Tang Xiaotang (bible rule 40): her nine speaking back shots (s03, s09, s11b, s12b, s14, s23, s26, s28, s32) drop her three
  pictures and her identity sentence (the sentence also names the gold abacus at her waist, rule 20); the 'only' sentence says
  she is seen from behind and appears once. s11 is her one front face: her portrait and angle-a (angle-b dropped), her identity
  sentence without the gold abacus. Her over-the-shoulder backs (s04, s08, s18) and her small back in s34 are not listed
  characters (no picture); the 'only' sentence names them as the young woman seen from behind. s07 (the abacus insert) and s17b
  (the ducks) carry her voice only.
- Xu Yan's smirking angle-b nowhere (e921 review). The wides seen from behind (s26, s34) send his portrait only. Where gen-dh sent
  only angle-a and angle-b (the close-ups s02, s10, s27, s30) his portrait goes first and angle-a second (e930's XU_TWO).
- A-ling never angle-b (e930); her wides s16, s19, s20, s34 her portrait only; where gen-dh sent only her two angles (the close-up
  s17) her portrait first and angle-a second (e930 s39). Qian Yuanwai never angle-b (e931); his wide s22 his portrait only.
  Little Xiaohe: her portrait only (gen-dh sends no angle picture of her).
- No person sent: s07 (the abacus insert), s21 (the duck's bill insert), s35 (the hand on the crossbar insert): no place sentence
  (rule 35), "Initial composition: <LOC>: insert close-up" becomes "Initial composition: Insert close-up"; their one picture
  (H3's reference mode needs 1-9) is the free crop of the tabletop, the water, the gate's wood, written as the ground and the
  light only; the standard insert sentence becomes NOBODY_INS (the separator "never the mood. " stays once). s12 (four unnamed
  men at the cages), s17b (six ducks), s29 (twelve unnamed refugees): the set clause opens the sentence.
- The fields (s12-s25): r2.py's LOC carries " below the deep pool" only so gen-dh's SET sends the pool picture, which this spec
  swaps for the field pictures; the words leave the d1 prompt here (r2.POOLMARK -> ""), as e934's fields (e033 review 必改 7).
  Every later fix / retake spec of s12-s25 must carry the same replacement (e034 independent review 建議 6).
- 'Only' sentences: where the composition already says "... is the only person in the frame", the appended one is cut down to
  its second half (e927 review 建議), also where ref2manifest's crowd test wrote "Besides her, only the other people ..." over a
  composition that says she is alone (s19, s20: the flock of ducks). Where the composition describes unnamed people the 'only'
  sentence names them: Tang Xiaotang's backs (above), the man holding the pole (s16), the four men at the cages (s12), the man
  seen from behind (s33), the two men at the gate (s32, s34). s22 keeps ref2manifest's "Besides him, ..." (the two retainers).
- Shoes: extras_patch's wide-shot sentence stays where the people show cloth shoes; the refugees (s29) wear straw sandals.
- e034 independent review 必改 1: extras' clean sentence ends "the air is clear and still, a clean natural film image" (CLEAR);
  replaced where the shot needs something in the air: s14 (the wind tossing her ribbon, the swarm over the hills), s20-s25 (the
  dawn mist on the water), s26 (the evening breeze in the willow).
- The speaking gaze never names an unsent listener (e927 必改 5, bible rule 31): r2.py's GAZE_REFINE (the same words in d1 and in
  the refine text).
- Every motion that opens a sentence after "never the mood. " is capitalised (e928 review 必改 1's fix).
- Sets (r2.py PLACES): the room by night: e922's set-xujia-wu-ye-table-l1 (s01, s03, s04, s08, s09, s11b) and the free crops
  -chuang (s02, s02b, s06, s10), -qiang (s11), -zhuo (s07), -di (s05), swapped for gen-dh's/pilot.py's set-xujia-wu-l1 (the day
  room, never sent); the fields: the free grades and crops of set-hantian-yang-l1 (hantian_yang.sh), swapped for pilot.py's
  newest set-shentan (gen-dh's dh-set-shentan-t1, never sent); the gate: set-cunkou-l1 (s26, gen-dh's own pick, not swapped) and
  the free crops -kong (s27, s30), -men (s28, s29, s32, s34), -ding (s31), -dao (s33), -zha (s35). Every swap is sent with an
  absolute path by prep935.sh.
- No seed of this episode has been run. Seeds 9351101/9351102.
"""
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROD = HERE.parents[2]
L = Path(PROD / "assets" / "refs-live")
VIDEO = str(PROD.parents[2] / "zhong-tian-qu-qi-e035-r2" / "video.json")
_spec = importlib.util.spec_from_file_location("r2_935_mkspec", PROD / "writer-tools" / "e035-r2" / "r2.py")
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
NO_COPY = "No second copy of anyone appears."
BESIDES_THEM = "Besides them, only the other people the composition names are in the frame; no second copy of anyone appears."
BESIDES_HER = "Besides her, only the other people the composition names are in the frame; no second copy of anyone appears."
ONE_TANG = "the young woman with the two high round buns appears only once"
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
NOBODY_OLD = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
NOBODY_INS = "Throughout the shot the framing stays as it is. The picture gives the ground and the light of the background only, never the mood. "
INSERT_CLAUSE = {
    "s07": "The dark wooden tabletop shown in <Picture 1> gives only the ground and the light of the background.",
    "s21": "The misty water shown in <Picture 1> gives only the ground and the light of the background.",
    "s35": "The rough wood shown in <Picture 1> gives only the wood and the light of the background.",
}
INSERT_LOC = {"s07": "ye_e", "s21": "ch_e", "s35": "kk_e"}
SHOES = "Every person in the frame wears dark cloth shoes on both feet."
SANDALS = "Every person in the frame wears worn straw sandals on both feet."
CLEAR = "the air is clear and still, a clean natural film image"
WINDY = "the air is clear, a dry wind blowing, a clean natural film image"
MIST = "a thin white mist lying low over the water, a clean natural film image"
BREEZE = "a light evening breeze in the air, a clean natural film image"
INSERTS = ["s07", "s21", "s35"]
NOPERSON = ["s07", "s12", "s17b", "s21", "s29", "s35"]


def newest(sid_id):
    vs = [q for q in L.glob(f"set-{sid_id}-l*.png") if re.fullmatch(rf"set-{sid_id}-l\d+", q.stem)]
    return max(vs, key=lambda q: int(q.stem.rsplit("-l", 1)[1])).name


WU = newest("xujia-wu")      # pilot.py's newest set-xujia-wu for gen-dh's dh-set-xujia-wu-t1 ("Inside the farmhouse")
ST = newest("shentan")       # pilot.py's newest set-shentan for dh-set-shentan-t1 (the fields' " below the deep pool")
CK = newest("cunkou")        # pilot.py's newest set-cunkou for dh-set-cunkou-t1 ("At the village entrance")
assert WU == "set-xujia-wu-l1.png" and CK == "set-cunkou-l1.png", (WU, CK)


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
assert len(ids) == 40, len(ids)
shots = {sid: {} for sid in ids}
FIELD = ids[ids.index("s12"):ids.index("s26")]
assert FIELD[0] == "s12" and FIELD[-1] == "s25" and len(FIELD) == 17, FIELD

# Tang Xiaotang from behind: her identity sentence and her three pictures leave.
XU_BEYOND = "Xu Yan one step beyond her in the left third of the frame"
ALONE = f"She is the only person in the frame, seen only from behind; {ONE_TANG}; no second copy of anyone appears."
TANG_BACK = {
    "s03": [ONLY_2, back(XU_BEYOND)],
    "s09": [ONLY_2, back(XU_BEYOND)],
    "s11b": [ONLY_2, back(XU_BEYOND)],
    "s12b": [ONLY_2, back(XU_BEYOND)],
    "s14": [ONLY_SHE, ALONE],
    "s23": [ONLY_2, back("Qian Yuanwai one step beyond her in the right third of the frame")],
    "s26": [ONLY_2, f"Only these 2 people are in the frame, both seen from behind: the young woman with the buns and Xu Yan one step "
                    f"to her left; {ONE_TANG}; no second copy of anyone appears."],
    "s28": [ONLY_2, back(XU_BEYOND)],
    "s32": [BESIDES_THEM, f"Only Xu Yan, the young woman with the buns seen only from behind and the two men at the gate the "
                          f"composition describes are in the frame; {ONE_TANG}; no second copy of anyone appears."],
}
for sid, onl in TANG_BACK.items():
    add(sid, [TANG_ID, ""])
    add(sid, onl)
    drop(sid, *TANG_PICS)
for sid in ("s14",):  # alone: her identity sentence opened the prompt; the set clause now does
    add(sid, ["cinema camera. the location shown in <Picture 4>", "cinema camera. The location shown in <Picture 4>"])  # before the drop renumbers it
# her one front face: the gold abacus out of her cast sentence (rule 20), angle-b out
add("s11", [", a small gold abacus hanging at her waist; ", "; "])
drop("s11", "tangxiaotang-angle-b-l1.png")
# the shots where she is an unlisted back with no picture
for sid in ("s04", "s08", "s18"):
    add(sid, [ONLY_HE, f"Besides him, only the young woman seen from behind at the right edge of the frame the composition describes "
                       f"is in the frame; {ONE_TANG}; no second copy of anyone appears."])
add("s34", [BESIDES_THEM, f"Only Xu Yan, A-ling, the young woman with the buns seen only from behind and the two men at the gate the "
                          f"composition describes are in the frame; {ONE_TANG}; no second copy of anyone appears."])

# No person sent: the set clause opens the sentence; the inserts lose the place sentence (rule 35).
for sid in NOPERSON:
    add(sid, [SET_CLAUSE, INSERT_CLAUSE[sid] if sid in INSERTS else "T" + SET_CLAUSE[1:]])
for sid in INSERTS:
    add(sid, [f"Initial composition: {R2.LOC[INSERT_LOC[sid]]}: insert close-up", "Initial composition: Insert close-up"])
    add(sid, [NOBODY_OLD, NOBODY_INS])

# The fields: the pool words gen-dh's SET needed leave the d1 prompt.
for sid in FIELD:
    if sid not in INSERTS:  # the insert s21 lost its whole place sentence above
        add(sid, [R2.POOLMARK, ""])

# The unnamed the compositions describe are named in the 'only' sentence.
add("s12", [BESIDES_THEM, "Only the four men the composition describes, each in a different colour, are in the frame; no second copy "
                          "of anyone appears."])
add("s16", [ONLY_SHE, "Besides her, only the one man holding the pole the composition describes is in the frame; no second copy of "
                      "anyone appears."])
add("s33", [ONLY_SHE, "Besides her, only the one man seen from behind at the left edge of the frame the composition describes is in "
                      "the frame; no second copy of anyone appears."])
for sid in ("s19", "s20"):  # ref2manifest's crowd test read the flock; the composition says she is alone
    add(sid, [BESIDES_HER, NO_COPY])
SPECIAL_ONLY = set(TANG_BACK) | {"s04", "s08", "s18", "s16", "s33", "s19", "s20", "s11"}
for sid in ids:
    sc = scenes[sid]
    if sid in SPECIAL_ONLY or len(sc["data"]["characters"]) != 1:
        continue
    if "is the only person in the frame" in sc["data"]["prompt"]:
        her = sc["data"]["characters"][0] in ("aling", "tangxiaotang", "xiaohe")
        add(sid, [ONLY_SHE if her else ONLY_HE, NO_COPY])
add("s11", [ONLY_SHE, NO_COPY])

# Shoes: the refugees wear straw sandals.
add("s29", [SHOES, SANDALS])
# The clean sentence (e034 review 必改 1): the wind and the swarm, the dawn mist, the evening breeze.
add("s14", [CLEAR, WINDY])
for sid in ("s20", "s20b", "s21", "s22", "s23", "s24", "s25"):
    add(sid, [CLEAR, MIST])
add("s26", [CLEAR, BREEZE])

# Lines not said into a face on screen: r2.py's direction sentences (the same in the refine text).
for sid, (pr, g) in R2.GAZE_REFINE.items():
    add(sid, [R2.GAZE_GEN[pr], g])

# Every motion that opens a sentence after "never the mood. " starts with a capital.
for sc in video["scenes"]:
    sid, mo = sc["id"], sc["data"]["motion"]
    if mo.startswith(NOBODY_OLD):
        mo = mo[len(NOBODY_OLD):]
    if mo[:1].islower():
        head = mo[:24]
        add(sid, [f"never the mood. {head}", f"never the mood. {head[0].upper()}{head[1:]}"])

# Pictures.
XU = [sid for sid in ids if "xuyan" in scenes[sid]["data"]["characters"]]
XU_TWO = ["s02", "s10", "s27", "s30"]  # gen-dh sent angle-a and angle-b only (the close-ups)
XU_WIDE = ["s26", "s34"]
for sid in XU:
    if sid not in XU_TWO:
        drop(sid, "xuyan-angle-b-l1.png")
for sid in XU_WIDE:
    drop(sid, "xuyan-angle-a-l1.png")
AL = [sid for sid in ids if "aling" in scenes[sid]["data"]["characters"]]
AL_TWO = ["s17"]
AL_WIDE = ["s16", "s19", "s20", "s34"]
for sid in AL:
    if sid not in AL_TWO:
        drop(sid, "aling-angle-b-l1.png")
for sid in AL_WIDE:
    drop(sid, "aling-angle-a-l1.png")
QI = [sid for sid in ids if "qianyuanwai" in scenes[sid]["data"]["characters"]]
for sid in QI:
    drop(sid, "qianyuanwai-angle-b-l1.png")
drop("s22", "qianyuanwai-angle-a-l1.png")

SWAP = {sid: {} for sid in ids}
PLACE = {
    WU: {"set-xujia-wu-ye-table-l1.png": ["s01", "s03", "s04", "s08", "s09", "s11b"],
         "set-xujia-wu-ye-chuang-l1.png": ["s02", "s02b", "s06", "s10"], "set-xujia-wu-ye-qiang-l1.png": ["s11"],
         "set-xujia-wu-ye-zhuo-l1.png": ["s07"], "set-xujia-wu-ye-di-l1.png": ["s05"]},
    ST: {"set-hantian-yang-zong-l1.png": ["s12"], "set-hantian-yang-zong-liu-l1.png": ["s12b", "s16"],
         "set-hantian-yang-zong-an-l1.png": ["s13", "s17"], "set-hantian-yang-zong-tian-l1.png": ["s14"],
         "set-hantian-yang-zong-geng-l1.png": ["s15", "s18"], "set-hantian-yang-zong-shui-l1.png": ["s17b"],
         "set-hantian-yang-xi-l1.png": ["s19"], "set-hantian-yang-chen-l1.png": ["s20"],
         "set-hantian-yang-chen-liu-l1.png": ["s20b", "s22", "s23", "s24"], "set-hantian-yang-chen-shui-l1.png": ["s21"],
         "set-hantian-yang-chen-an-l1.png": ["s25"]},
    CK: {"set-cunkou-l1.png": ["s26"], "set-cunkou-kong-l1.png": ["s27", "s30"],
         "set-cunkou-men-l1.png": ["s28", "s29", "s32", "s34"], "set-cunkou-ding-l1.png": ["s31"], "set-cunkou-dao-l1.png": ["s33"],
         "set-cunkou-zha-l1.png": ["s35"]},
}
seen = set()
for gen, pics in PLACE.items():
    for pic, sids in pics.items():
        for sid in sids:
            assert sid not in seen, sid
            seen.add(sid)
            if pic != gen:
                SWAP[sid][gen] = pic
assert seen == set(ids), sorted(set(ids) ^ seen)
for sid in XU_TWO:
    SWAP[sid]["xuyan-angle-a-l1.png"] = "xuyan-portrait-l1.png"
    SWAP[sid]["xuyan-angle-b-l1.png"] = "angles/xuyan-angle-a-l1.png"
for sid in AL_TWO:
    SWAP[sid]["aling-angle-a-l1.png"] = "aling-portrait-l1.png"
    SWAP[sid]["aling-angle-b-l1.png"] = "angles/aling-angle-a-l1.png"
for sid, sw in SWAP.items():
    if sw:
        shots[sid]["swap_pictures"] = sw
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (L / k).is_file(), k

spec = {
    "_note": ("e935 live d1 (e934-live's way, with e931/e933-live's Tang Xiaotang back shots; written by mkspec.py). Tang Xiaotang "
              "from behind in s03, s09, s11b, s12b, s14, s23, s26, s28, s32 (pictures and identity sentence dropped); her one front "
              "face s11 (portrait and angle-a, no gold abacus); unlisted backs s04, s08, s18, s34. No person sent in the inserts s07, "
              "s21, s35 (no place sentence, one crop written as the ground and the light only), s12, s17b, s29. Xu Yan's angle-b "
              "nowhere; s26, s34 his portrait only; s02, s10, s27, s30 his portrait then angle-a. A-ling never angle-b; s16, s19, s20, "
              "s34 her portrait only; s17 her portrait then angle-a. Qian Yuanwai never angle-b; s22 his portrait only. The field "
              "prompts lose ' below the deep pool' (every later fix of s12-s25 must too). The clean sentence's 'clear and still' "
              "replaced in s14 (wind), s20-s25 (dawn mist), s26 (breeze). The refugees in straw sandals (s29). Sets: see mkspec.py. "
              "No off-screen sentence (r2.py OFFSCREEN_SPEECH = False). Seeds 9351101/9351102."),
    "seeds": [9351101, 9351102],
    "shots": shots,
}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
