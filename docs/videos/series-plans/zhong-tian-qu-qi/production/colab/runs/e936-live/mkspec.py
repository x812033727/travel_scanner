"""Writes spec.json next to this file: e936 live d1 (e935-live/spec.json's way; writer-tools/e036-r2/r2.py's FOOT and PLACES).
Run: python3 -I mkspec.py

- Style sentence (e935 §8, task file 2026-11-20): pilot.py's opening sentence now ends "with the look of a feature film." (it
  used to end "shot on a cinema camera.", which H3 drew as a camera on a tripod in e935 s22 / s23); every anchor here that
  follows it uses the new words, and prep936.sh asserts no "cinema camera" is left in any d1 prompt.
- Tang Xiaotang (bible rule 40): her five speaking back shots (s07, s14, s18, s27, s38) drop her three pictures and her identity
  sentence (it also names the gold abacus at her waist, rule 20); the 'only' sentence says she is seen from behind and appears
  once. She has no front face this episode. Her over-the-shoulder backs (s06, s12b) and her small back in s01 are not listed
  characters (no picture); the 'only' sentence names them as the young woman seen from behind. s05 (the gold abacus insert) and
  s16 (A-ling at the table) carry her voice only.
- Xu Yan's smirking angle-b nowhere (e921 review). The wides and backs (s01, s02, s09, s13, s29) send his portrait only. Where
  gen-dh sent only angle-a and angle-b (the close-up s11) his portrait goes first and angle-a second (e930's XU_TWO).
- A-ling never angle-b (e930); her back in s01 her portrait only. Qin Shuang never angle-b; her wide s31 and her back s33 her
  portrait only (gen-dh sends her portrait alone; retake.py cannot add pictures, so her angle-a is not sent anywhere). Qian
  Yuanwai never angle-b (e931); s28 is his back with no picture and no name (r2.py QIAN_BACK; e934 / e935 fix4).
- No person sent: the inserts s05 (the gold abacus), s15 (the bamboo tally), s17 (the paper and the brush tip), s22 (the feet),
  s23 (the hand on the hoe): no place sentence (rule 35), "Initial composition: <LOC>: insert close-up" becomes "Initial
  composition: Insert close-up"; their one picture (H3's reference mode needs 1-9) is a free crop written as the ground and the
  light only; the standard insert sentence becomes NOBODY_INS. s28 (Qian Yuanwai's back), s32 (the empty mats), s36 (the line of
  flames): the set clause opens the sentence.
- The channel (s13-s30): r2.py's LOC carries " below the deep pool" only so gen-dh's SET sends the pool picture, which this spec
  swaps for the channel pictures; the words leave the d1 prompt here (r2.POOLMARK -> ""), as e934 / e935's fields. Every later
  fix / retake spec of s13-s30 must carry the same replacement.
- 'Only' sentences: where the composition already says "... is the only person in the frame", the appended one is cut down to
  its second half (e927 review 建議). Where the composition describes unnamed people the 'only' sentence names them: Tang
  Xiaotang's backs (above), the guards (s01, s02), the refugees (s02, s08, s09), the man at the table (s14), the woman at the table
  (s16), the diggers (s13), the people going home (s29), the three far backs (s30), the sleepers (s31, s32), Qin Shuang's
  shoulder at the edge (s25).
- Shoes (extras_patch's wide-shot sentence): the refugees and diggers wear straw sandals beside Xu Yan's cloth shoes (s02, s09,
  s13, s29); s36 shows nobody (the sentence goes).
- The clean sentence ends "the air is clear and still, a clean natural film image" (CLEAR); replaced where the shot needs
  something in the air: the torches at the gate (s01, s02), the evening air at the gate (s03-s12b), the dust of the hoes (s13),
  the lamp's flame (s34, s38) and the night air (s31-s33, s35-s37); the calm day at the table keeps it.
- The speaking gaze never names an unsent listener (bible rule 31): r2.py's GAZE_REFINE (the same words in d1 and in the refine
  text). Every motion that opens a sentence after "never the mood. " is capitalised (e928 review 必改 1's fix).
- Sets (r2.py PLACES, after the independent review): the gate: e935's -men (s01, shut), -dao (s08 s09 s12), -kong (s11 s11b)
  and this episode's free -ding2 (s03 s04 s10), -wai2 (s02 until r2.KAI, then the paid -kai; s06 s07 s12b), -di (s05), swapped for
  gen-dh's / pilot.py's set-cunkou-l1 (never sent); the channel: the cleaned set-shanjiao-qu-jing-l1 (s13), -zhuo2, -tian2,
  -xi2, -xi2-zhuo, and -an, -di (shanjiao_qu.sh), swapped for pilot.py's newest set-shentan (never sent); the yard: e931's
  set-xujia-yuan-ye-dong2-l1 (s31) and this episode's free crops (xujia_yuan_ye_e936.sh; -shan2 for s36), swapped for pilot.py's newest set-xujia-yuan-ye (l2, never sent). Every swap is sent with an absolute
  path by prep936.sh.
- No seed of this episode has been run. Seeds 9361101/9361102.
"""
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROD = HERE.parents[2]
L = Path(PROD / "assets" / "refs-live")
VIDEO = str(PROD.parents[2] / "zhong-tian-qu-qi-e036-r2" / "video.json")
_spec = importlib.util.spec_from_file_location("r2_936_mkspec", PROD / "writer-tools" / "e036-r2" / "r2.py")
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
STYLE_END = "with the look of a feature film."
ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."
ONLY_2 = "Only these 2 people are in the frame; no second copy of anyone appears."
NO_COPY = "No second copy of anyone appears."
BESIDES_THEM = "Besides them, only the other people the composition names are in the frame; no second copy of anyone appears."
BESIDES_HIM = "Besides him, only the other people the composition names are in the frame; no second copy of anyone appears."
BESIDES_HER = "Besides her, only the other people the composition names are in the frame; no second copy of anyone appears."
ONE_TANG = "the young woman with the two high round buns appears only once"
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
NOBODY_OLD = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
NOBODY_INS = "Throughout the shot the framing stays as it is. The picture gives the ground and the light of the background only, never the mood. "
INSERT_CLAUSE = {
    "s05": "The bare earth shown in <Picture 1> gives only the ground and the light of the background.",
    "s15": "The cracked dry earth shown in <Picture 1> gives only the ground and the light of the background.",
    "s17": "The pale dry earth shown in <Picture 1> gives only the ground and the light of the background.",
    "s22": "The cracked dry earth shown in <Picture 1> gives only the ground and the light of the background.",
    "s23": "The dug brown earth shown in <Picture 1> gives only the ground and the light of the background.",
}
INSERT_LOC = {"s05": "kk_e", "s15": "q1_e", "s17": "q1_e", "s22": "q2_e", "s23": "q2_e"}
SHOES = "Every person in the frame wears dark cloth shoes on both feet."
SHOES_MIX = "Xu Yan wears dark cloth shoes and every other person in the frame wears worn straw sandals on both feet."
SHOES_GATE = ("Xu Yan and the two men at the gate wear dark cloth shoes and the eight people walking in wear worn straw sandals on "
              "both feet.")
CLEAR = "the air is clear and still, a clean natural film image"
TORCHY = "the warm evening air, the torch flames wavering, a clean natural film image"
BREEZE = "a light evening breeze in the air, a clean natural film image"
DUSTY = "fine yellow dust rising from the hoes into the dry air, a clean natural film image"
LAMPY = "the cool night air, the small lamp flame swaying, a clean natural film image"
NIGHTAIR = "the cool night air, a clean natural film image"
INSERTS = ["s05", "s15", "s17", "s22", "s23"]
NOPERSON = INSERTS + ["s28", "s32", "s36"]


def newest(sid_id):
    vs = [q for q in L.glob(f"set-{sid_id}-l*.png") if re.fullmatch(rf"set-{sid_id}-l\d+", q.stem)]
    return max(vs, key=lambda q: int(q.stem.rsplit("-l", 1)[1])).name


CK = newest("cunkou")        # pilot.py's newest set-cunkou for dh-set-cunkou-t1 ("At the village entrance")
ST = newest("shentan")       # pilot.py's newest set-shentan for dh-set-shentan-t1 (the channel's " below the deep pool")
YY = newest("xujia-yuan-ye")  # pilot.py's newest set-xujia-yuan-ye for dh-set-xujia-yuan-ye-t1 ("night yard of the Xu farmhouse")
assert CK == "set-cunkou-l1.png" and YY == "set-xujia-yuan-ye-l2.png", (CK, YY)


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
CHANNEL = ids[ids.index("s13"):ids.index("s31")]
assert CHANNEL[0] == "s13" and CHANNEL[-1] == "s30" and len(CHANNEL) == 18, CHANNEL

# Tang Xiaotang from behind: her identity sentence and her three pictures leave.
XU_BEYOND = "Xu Yan one step beyond her in the left third of the frame"
TANG_BACK = {
    "s07": [ONLY_2, back(XU_BEYOND)],
    "s14": [ONLY_SHE, back("the man at the left side of the table the composition describes, his face in profile")],
    "s18": [ONLY_2, back("A-ling one step beyond her in the left third of the frame")],
    "s27": [ONLY_SHE, f"She is the only person in the frame, seen only from behind; {ONE_TANG}; no second copy of anyone appears."],
    "s38": [ONLY_2, back(XU_BEYOND)],
}
for sid, onl in TANG_BACK.items():
    add(sid, [TANG_ID, ""])
    add(sid, onl)
    drop(sid, *TANG_PICS)
for sid in ("s14", "s27"):  # alone: her identity sentence opened the prompt; the set clause now does (before the drop renumbers)
    add(sid, [f"{STYLE_END} the location shown in <Picture 4>", f"{STYLE_END} The location shown in <Picture 4>"])
# the shots where she is an unlisted back with no picture
for sid in ("s06", "s12b"):
    add(sid, [ONLY_HE, f"Besides him, only the young woman seen from behind at the right edge of the frame the composition describes "
                       f"is in the frame; {ONE_TANG}; no second copy of anyone appears."])
add("s01", [BESIDES_THEM, f"Only Xu Yan, A-ling, the young woman with the buns seen only from behind and the two men at the gate the "
                          f"composition describes are in the frame; {ONE_TANG}; no second copy of anyone appears."])

# No person sent: the set clause opens the sentence; the inserts lose the place sentence (rule 35).
for sid in NOPERSON:
    add(sid, [SET_CLAUSE, INSERT_CLAUSE[sid] if sid in INSERTS else "T" + SET_CLAUSE[1:]])
for sid in INSERTS:
    if sid != "s22":  # s22 opens "low-angle insert close-up" (below)
        add(sid, [f"Initial composition: {R2.LOC[INSERT_LOC[sid]]}: insert close-up", "Initial composition: Insert close-up"])
    add(sid, [NOBODY_OLD, NOBODY_INS])
add("s22", [f"Initial composition: {R2.LOC['q2_e']}: low-angle insert close-up", "Initial composition: Low-angle insert close-up"])

# The channel: the pool words gen-dh's SET needed leave the d1 prompt.
for sid in CHANNEL:
    if sid not in INSERTS:  # the inserts lost their whole place sentence above
        add(sid, [R2.POOLMARK, ""])

# The unnamed the compositions describe are named in the 'only' sentence.
add("s02", [BESIDES_HIM, "Only Xu Yan, the two men at the gate and the eight people walking in the composition describes, each in a "
                         "different colour, are in the frame; no second copy of anyone appears."])
add("s08", [ONLY_HE, "Besides him, only the two people seen from behind in the left foreground the composition describes are in the "
                     "frame; no second copy of anyone appears."])
add("s09", [ONLY_HE, "Besides him, only the seven people the composition describes, each in a different colour, are in the frame; no "
                     "second copy of anyone appears."])
add("s13", [BESIDES_HIM, "Only Xu Yan and the eight people the composition describes, each in a different colour, are in the frame; "
                         "no second copy of anyone appears."])
add("s16", [ONLY_SHE, "Besides her, only the one woman seen from behind in the right foreground the composition describes is in the "
                      "frame; no second copy of anyone appears."])
add("s22", [BESIDES_THEM, "Only the six pairs of feet the composition describes are in the frame."])
add("s25", [ONLY_HE, "Besides him, only the shoulder of the young woman at the right edge of the frame the composition describes is "
                     "in the frame; no second copy of anyone appears."])
add("s29", [BESIDES_HIM, "Only Xu Yan and the six people walking away the composition describes, each in a different colour, are in "
                         "the frame; no second copy of anyone appears."])
add("s30", [BESIDES_THEM, "Only Xu Yan, Qin Shuang and the three far men seen from behind the composition describes are in the frame; "
                          "no second copy of anyone appears."])
add("s31", [BESIDES_HER, "Only Qin Shuang and the nine sleeping men the composition describes are in the frame; no second copy of "
                         "anyone appears."])
add("s32", [BESIDES_THEM, "Only the two sleeping men and the one hand the composition describes are in the frame; no second copy of "
                          "anyone appears."])
SPECIAL_ONLY = set(TANG_BACK) | {"s01", "s02", "s06", "s08", "s09", "s12b", "s13", "s16", "s22", "s25", "s29", "s30", "s31", "s32"}
for sid in ids:
    sc = scenes[sid]
    if sid in SPECIAL_ONLY or len(sc["data"]["characters"]) != 1:
        continue
    if "is the only person in the frame" in sc["data"]["prompt"]:
        her = sc["data"]["characters"][0] in ("aling", "tangxiaotang", "qinshuang")
        add(sid, [ONLY_SHE if her else ONLY_HE, NO_COPY])

# Shoes.
add("s02", [SHOES, SHOES_GATE])
for sid in ("s09", "s13", "s29"):
    add(sid, [SHOES, SHOES_MIX])
add("s36", [SHOES + " ", ""])
# The clean sentence: torches, the evening air, dust, the lamp, the night.
for sid in ("s01", "s02"):
    add(sid, [CLEAR, TORCHY])
for sid in ("s03", "s04", "s06", "s07", "s08", "s09", "s10", "s11", "s11b", "s12", "s12b"):
    add(sid, [CLEAR, BREEZE])
add("s13", [CLEAR, DUSTY])
for sid in ("s34", "s38"):
    add(sid, [CLEAR, LAMPY])
for sid in ("s31", "s32", "s33", "s35", "s36", "s37"):
    add(sid, [CLEAR, NIGHTAIR])

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
XU_TWO = ["s11"]  # gen-dh sent angle-a and angle-b only (the close-up)
XU_WIDE = ["s01", "s02", "s09", "s13", "s29"]
for sid in XU:
    if sid not in XU_TWO:
        drop(sid, "xuyan-angle-b-l1.png")
for sid in XU_WIDE:
    drop(sid, "xuyan-angle-a-l1.png")
AL = [sid for sid in ids if "aling" in scenes[sid]["data"]["characters"]]
AL_WIDE = ["s01"]
for sid in AL:
    drop(sid, "aling-angle-b-l1.png")
for sid in AL_WIDE:
    drop(sid, "aling-angle-a-l1.png")
QI = [sid for sid in ids if "qianyuanwai" in scenes[sid]["data"]["characters"]]
for sid in QI:
    drop(sid, "qianyuanwai-angle-b-l1.png")

SWAP = {sid: {} for sid in ids}
# s02: the paid open-gate picture -kai once r2.KAI (review 建議 2), the free -wai2 until then (必改 1)
PLACE = {  # after the independent review (必改 1, 3, 7; 建議 3, 5, 7, 8, 9)
    CK: {"set-cunkou-zha2-men-l1.png": ["s01"], "set-cunkou-zha2-ding2-l1.png": ["s03", "s04", "s10"],
         "set-cunkou-zha2-di-l1.png": ["s05"],
         "set-cunkou-zha2-wai2-l1.png": (["s06", "s07", "s12b"] if R2.KAI else ["s02", "s06", "s07", "s12b"]),
         **({"set-cunkou-zha2-kai-l1.png": ["s02"]} if R2.KAI else {}), "set-cunkou-zha2-dao-l1.png": ["s08", "s09", "s12"],
         "set-cunkou-zha2-kong-l1.png": ["s11", "s11b"]},
    ST: {"set-shanjiao-qu-jing-l1.png": ["s13"],
         "set-shanjiao-qu-zhuo2-l1.png": ["s14", "s16", "s18", "s19", "s20", "s26", "s27", "s28"],
         "set-shanjiao-qu-an-l1.png": ["s23", "s25"], "set-shanjiao-qu-di-l1.png": ["s15", "s17", "s22"],
         "set-shanjiao-qu-tian2-l1.png": ["s21", "s24"], "set-shanjiao-qu-xi2-l1.png": ["s29"],
         "set-shanjiao-qu-xi2-zhuo-l1.png": ["s30"]},
    YY: {"set-xujia-yuan-ye-dong2-l1.png": ["s31"], "set-xujia-yuan-ye-dong2-qiang-l1.png": ["s32", "s33", "s35"],
         "set-xujia-yuan-ye-dong2-chai-l1.png": ["s34"], "set-xujia-yuan-ye-dong2-shan2-l1.png": ["s36"],
         "set-xujia-yuan-ye-dong2-wu-l1.png": ["s37"], "set-xujia-yuan-ye-dong2-zhong-l1.png": ["s38"]},
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
for sid, sw in SWAP.items():
    if sw:
        shots[sid]["swap_pictures"] = sw
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (L / k).is_file(), k

spec = {
    "_note": ("e936 live d1 (e935-live's way; written by mkspec.py). Tang Xiaotang from behind in s07, s14, s18, s27, s38 (pictures "
              "and identity sentence dropped); no front face of hers; unlisted backs s01, s06, s12b; her voice over s05 (the gold "
              "abacus insert) and s16. No person sent in the inserts s05, s15, s17, s22, s23 (no place sentence, one crop written as "
              "the ground and the light only), s28 (Qian Yuanwai's back, unnamed), s32, s36. Xu Yan's angle-b nowhere; s01, s02, s09, "
              "s13, s29 his portrait only; s11 his portrait then angle-a. A-ling never angle-b; s01 her portrait only. Qian Yuanwai "
              "never angle-b. Qin Shuang: her portrait only (gen-dh sends no angle of hers). The channel prompts lose ' below the "
              "deep pool' (every later fix of s13-s30 must too). The clean sentence's 'clear and still' replaced at the gate "
              "(torches, the evening breeze), s13 (dust) and the yard (the lamp, the night air). Straw sandals beside Xu Yan's cloth "
              "shoes (s02, s09, s13, s29). After the independent review: no shut gate leaves after s01 (-ding2, -wai2), the cleaned channel "
              "picture (-jing, -zhuo2, -tian2, -xi2), -shan2. Sets: see mkspec.py. No off-screen sentence (r2.py OFFSCREEN_SPEECH = False). Seeds "
              "9361101/9361102."),
    "seeds": [9361101, 9361102],
    "shots": shots,
}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
