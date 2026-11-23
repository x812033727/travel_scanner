"""Writes spec.json next to this file: e938 live d1 (e937-live/spec.json's way; writer-tools/e038-r2/r2.py's FOOT and PLACES).
Run: python3 -I mkspec.py

- Style sentence (e935 §8): pilot.py's opening sentence ends "with the look of a feature film."; every anchor here that follows
  it uses those words, and prep938.sh asserts no "cinema camera" is left in any d1 prompt.
- Tang Xiaotang (bible rule 40): her five speaking back shots (s02, s04, s07, s16, s18) drop her three pictures and her identity
  sentence (it also names the gold abacus at her waist, rule 20); the 'only' sentence says she is seen from behind and appears
  once. She has no front face this episode. Owner 2026-11-22 (PR #2217, OWNER-CHECK-20261122.md): every back shot of hers also
  sends the two-bun hair reference as the LAST picture with one sentence that ties it to the hair only ("append_pictures":
  prep938.sh appends the picture, renumbers the header and puts the sentence after the set clause): by day (s02, s04, s07) the
  owner's own refs-live/tangxiaotang-back-shuangji-e929-w3.png, by night (s16, s18) its free night copy -w3-ye.png (e937 review
  建議 1).
- Qin Shuang's spear (bible 〈道具〉): the shots with the spear in the frame (s09 leaning by the door, s12, s16, s17) append
  refs-live/prop-changqiang-l1.png the same way, with a sentence that makes it the one spear of the shot.
- The horse (bible rule 41, 〈道具〉): every shot with the horse in the frame (s16, s18, s20, s21, s22, s25, s27, s27b, s29, s30)
  appends refs-live/prop-zaohongma-l1.png (the picked bare-backed chestnut, mane and tail the same red-brown; the saddle is written
  in the composition) with a sentence that makes it the one horse and fixes its coat and bridle only.
- The guard captain (bible 〈人物〉, first episode; r2.py MINOR "duizhang", in the frame's characters but with no live portrait in
  gen-dh.mjs / pilot.py): every shot of his (s23, s26, s27, s27b, s28, s32, s35, s37, s38) appends refs-live/duizhang-portrait-l1.png
  with a sentence that fixes his face, helmet and armour only (one face and one helmet the whole episode: 原版必修).
- Xu Yan's smirking angle-b nowhere (e921 review). The wides (s01, s19: kneeling, framed full figure) send his portrait only.
  Where gen-dh sent only angle-a and angle-b (the close-ups s06, s10, s11, s15) his portrait goes first and angle-a second
  (e930's XU_TWO).
- A-ling never angle-b (e930); the wides (s16, s20, s22, s27, s27b, s29, s32) her portrait only; where gen-dh sent only angle-a and
  angle-b (s33) her portrait first and angle-a second. Qin Shuang, little Xiaohe: their portraits only (gen-dh sends no angle).
- No person picture sent: the inserts s31 (the door seam and A-ling's hand) and s34 (the crossbows): no place sentence (rule 35),
  "Initial composition: <LOC>: insert close-up" becomes "Initial composition: Insert close-up"; their one picture is a free crop
  written as the ground and the light only; the standard insert sentence becomes NOBODY_INS. s24 (the young guard, unnamed) and the
  captain's shots alone (s23, s26, s28, s35, s37, s38): the set clause opens the sentence.
- The road, the gate and the street (s20-s38): r2.py's LOC carries " below the deep pool" only so gen-dh's SET sends the pool
  picture, which this spec swaps for this episode's pictures; the words leave the d1 prompt here (r2.POOLMARK -> ""). Every later
  fix / retake spec of these shots must carry the same replacement.
- 'Only' sentences (the task file 2026-11-20: one more person than written is common, so the count is written twice, in the
  composition and here at the end): where the composition already says "... is the only person in the frame" the appended
  one is cut down to its second half; where the composition describes unnamed people or the horse the 'only' sentence names them.
- Shoes (extras_patch's wide-shot sentence): Xu Yan's cloth shoes (s01, s19), Qin Shuang's leather boots and the women's soft cloth
  shoes (s16), A-ling's soft cloth shoes on the horse (s22, s27, s27b, s29), the guards' black boots (s27, s27b, s32).
- The clean sentence ends "the air is clear and still, a clean natural film image" (CLEAR); every shot replaces it: the grey
  morning air, the midday air, the warm late-afternoon air, the small flame, the night yard, the dust of the road, the torchlight,
  the cold street.
- The speaking gaze never names an unsent listener (bible rule 31): r2.py's GAZE_REFINE (the same words in d1 and in the refine
  text). Every motion that opens a sentence after "never the mood. " is capitalised (e928 review 必改 1's fix).
- Sets (r2.py PLACES): the sickroom: pilot.py's newest set-xujia-tangfang (l2) swapped for this episode's free -chen-chuang (s01,
  s04), -chen-men (s02), -chen-zhen (s03), -xi-zhen (s05, s11), -xi-chuang (s06, s07, s08, s10), -xi-men (s09), the night crops
  -men (s12, s13), -zhen (s14), -chuang (s15, s15b, s19); the night yard: pilot.py's newest set-xujia-yuan-ye (l2, never sent)
  swapped for set-xujia-yuan-ye-dong2-l1 (s16), -wu (s17), -zhong (s18); the road, the gate and the street: pilot.py's newest
  set-shentan (never sent) swapped for set-guandao-ye-ce (s20), -shu (s21), set-chengmen-ye-zha (s22, s27), -qiang (s23, s26), -men
  (s24, s28), -lu (s25), set-chengmen-ye-l1 (s27b), set-yiguan-men-ye-l1 (s29), -men (s30, s33, s36), -feng (s31), -jie (s32, s35,
  s37, s38), -di (s34). Every swap is sent with an absolute path by prep938.sh.
- No seed of this episode has been run. Seeds 9381101/9381102.
"""
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROD = HERE.parents[2]
L = Path(PROD / "assets" / "refs-live")
VIDEO = str(PROD.parents[2] / "zhong-tian-qu-qi-e038-r2" / "video.json")
_spec = importlib.util.spec_from_file_location("r2_938_mkspec", PROD / "writer-tools" / "e038-r2" / "r2.py")
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
HAIR_DAY = "tangxiaotang-back-shuangji-e929-w3.png"  # the owner's file (2026-11-22), by day
HAIR_NIGHT = "tangxiaotang-back-shuangji-e929-w3-ye.png"  # its free night copy (e937 review 建議 1)
HAIR_SENT = ("The back of the young woman's head looks exactly like <Picture N>: the same smooth black hair parted down the "
             "middle and gathered into just two round buns, one on each side, each wrapped with one short pink silk ribbon; that "
             "picture fixes the hairstyle only, never the place or the light.")
SPEAR_PIC = "prop-changqiang-l1.png"
SPEAR_SENT = ("The long spear shown in <Picture N> is the one spear in this shot, keeping exactly its plain wooden shaft and its "
              "small plain iron spearhead; that picture fixes the spear only, never the place or the light.")
HORSE_PIC = "prop-zaohongma-l1.png"
HORSE_SENT = ("The horse shown in <Picture N> is the one horse in this shot, keeping exactly its deep red-brown coat, its mane and "
              "tail of the same red-brown and its plain brown bridle, with the saddle written above; that picture fixes the horse "
              "only, never the place or the light.")
CAP_PIC = "duizhang-portrait-l1.png"
CAP_SENT = ("The guard captain looks exactly like <Picture N>: the same square face and short black beard, the same black lamellar "
            "armour with small red studs and the same round iron helmet with cheek flaps and a small tuft of red horsehair; that picture fixes "
            "his face, helmet and armour only, never the place or the light.")
STYLE_END = "with the look of a feature film."
ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."
ONLY_2 = "Only these 2 people are in the frame; no second copy of anyone appears."
ONLY_3 = "Only these 3 people are in the frame; no second copy of anyone appears."
NO_COPY = "No second copy of anyone appears."
BESIDES_THEM = "Besides them, only the other people the composition names are in the frame; no second copy of anyone appears."
BESIDES_HER = "Besides her, only the other people the composition names are in the frame; no second copy of anyone appears."
ONE_TANG = "the young woman with the two high round buns appears only once"
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
NOBODY_OLD = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
NOBODY_INS = "Throughout the shot the framing stays as it is. The picture gives the ground and the light of the background only, never the mood. "
INSERT_CLAUSE = {
    "s31": "The dark wooden planks shown in <Picture 1> gives only the ground and the light of the background.",
    "s34": "The grey stone paving shown in <Picture 1> gives only the ground and the light of the background.",
}
INSERT_LOC = {"s31": "e_x", "s34": "e_x"}
SHOES = "Every person in the frame wears dark cloth shoes on both feet."
SHOES_BY = {
    "s01": "Xu Yan wears dark cloth shoes.",
    "s16": "Qin Shuang wears her leather boots, and A-ling and the young woman wear soft cloth shoes.",
    "s19": "Xu Yan wears dark cloth shoes.",
    "s22": "A-ling wears soft dark cloth shoes.",
    "s27": "A-ling wears soft dark cloth shoes and the guard captain wears black leather boots.",
    "s27b": "A-ling wears soft dark cloth shoes and the guard captain wears black leather boots.",
    "s29": "A-ling wears soft dark cloth shoes.",
    "s32": "The guard captain and every guard wear black leather boots and A-ling wears soft dark cloth shoes.",
}
CLEAR = "the air is clear and still, a clean natural film image"
AIR = {
    "morn": "the cold still air of early morning, a clean natural film image",
    "noon": "the still air of midday, a clean natural film image",
    "eve": "the warm still air of late afternoon, a clean natural film image",
    "lamp": "the still night air, the small flame on the table swaying, a clean natural film image",
    "yard": "the cool night air, a clean natural film image",
    "road": "the cold night air, the dust of the road drifting behind the hooves, a clean natural film image",
    "torch": "the cold night air, the torch flames wavering, a clean natural film image",
    "dust": "the cold night air, the torch flames wavering, dust billowing over the paving, a clean natural film image",
    "street": "the cold night air of an empty street, a clean natural film image",
    "still": "the cold still night air, a clean natural film image",  # the inserts: no place word (rule 35)
}
AIR_BY = {**{s: "morn" for s in ("s01", "s02", "s03")}, "s04": "noon",
          **{s: "eve" for s in ("s05", "s06", "s07", "s08", "s09", "s10", "s11")},
          **{s: "lamp" for s in ("s12", "s13", "s14", "s15", "s15b", "s19")},
          **{s: "yard" for s in ("s16", "s17", "s18")},
          **{s: "road" for s in ("s20", "s21")},
          **{s: "torch" for s in ("s22", "s23", "s24", "s25", "s26", "s28")}, **{s: "dust" for s in ("s27", "s27b")},
          **{s: "street" for s in ("s29", "s30", "s32", "s33", "s35", "s36", "s37", "s38")}, "s31": "still", "s34": "still"}
INSERTS = ["s31", "s34"]
CAP_ALONE = ["s23", "s26", "s28", "s35", "s37", "s38"]
NOPERSON = INSERTS + ["s24"] + CAP_ALONE  # no person picture before the appended ones: the set clause opens the sentence


def newest(sid_id):
    vs = [q for q in L.glob(f"set-{sid_id}-l*.png") if re.fullmatch(rf"set-{sid_id}-l\d+", q.stem)]
    return max(vs, key=lambda q: int(q.stem.rsplit("-l", 1)[1])).name


ST = newest("shentan")             # pilot.py's newest set-shentan for dh-set-shentan-t1 (" below the deep pool")
YY = newest("xujia-yuan-ye")       # pilot.py's newest set-xujia-yuan-ye for dh-set-xujia-yuan-ye-t1 ("night yard of the Xu farmhouse")
TF = newest("xujia-tangfang")      # pilot.py's newest set-xujia-tangfang for dh-set-xujia-tangfang-t1 ("first bedroom of the Xu farmhouse")
assert YY == "set-xujia-yuan-ye-l2.png" and TF == "set-xujia-tangfang-l2.png", (YY, TF)


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


def append_pic(sid, pic, sentence):
    shots[sid].setdefault("append_pictures", []).append([pic, sentence])


video = json.load(open(VIDEO, encoding="utf-8"))
scenes = {sc["id"]: sc for sc in video["scenes"]}
ids = [sc["id"] for sc in video["scenes"]]
assert len(ids) == 40, len(ids)
shots = {sid: {} for sid in ids}
OUTSIDE = ids[ids.index("s20"):]
assert OUTSIDE[0] == "s20" and len(OUTSIDE) == 20, OUTSIDE

# Tang Xiaotang from behind: her identity sentence and her three pictures leave; the hair reference joins every back of hers.
TANG_BACK = {
    "s02": [ONLY_2, "Only these 2 people are in the frame, the young woman with the buns seen only from behind and Xu Yan one step "
                    f"beyond her; {ONE_TANG}; no second copy of anyone appears."],
    "s04": [ONLY_3, "Only these 3 people are in the frame, the young woman with the buns seen only from behind, little Xiaohe asleep "
                    f"in the bed and Xu Yan by the bedpost; {ONE_TANG}; no second copy of anyone appears."],
    "s07": [ONLY_2, "Only these 2 people are in the frame, the young woman with the buns seen only from behind and little Xiaohe in "
                    f"the bed; {ONE_TANG}; no second copy of anyone appears."],
    "s16": [ONLY_3, "Only these 3 people and the one horse are in the frame, the young woman with the buns seen only from behind, Qin "
                    f"Shuang beside her and A-ling at the horse; {ONE_TANG}; no second copy of anyone or of the horse appears."],
    "s18": [ONLY_2, "Only these 2 people and the one horse are in the frame, the young woman with the buns seen only from behind and "
                    f"A-ling riding away on the horse; {ONE_TANG}; no second copy of anyone or of the horse appears."],
}
for sid, onl in TANG_BACK.items():
    add(sid, [TANG_ID, ""])
    add(sid, onl)
    drop(sid, *TANG_PICS)
add("s07", [f"{STYLE_END} little Xiaohe shown in", f"{STYLE_END} Little Xiaohe shown in"])
for sid in ("s02", "s04", "s07"):
    append_pic(sid, HAIR_DAY, HAIR_SENT)
for sid in ("s16", "s18"):
    append_pic(sid, HAIR_NIGHT, HAIR_SENT)
for sid in ("s09", "s12", "s16", "s17"):
    append_pic(sid, SPEAR_PIC, SPEAR_SENT)
HORSE_SH = ["s16", "s18", "s20", "s21", "s22", "s25", "s27", "s27b", "s29", "s30"]
for sid in HORSE_SH:
    append_pic(sid, HORSE_PIC, HORSE_SENT)
CAP_SH = ["s23", "s26", "s27", "s27b", "s28", "s32", "s35", "s37", "s38"]
for sid in CAP_SH:
    append_pic(sid, CAP_PIC, CAP_SENT)

# No person picture: the set clause opens the sentence; the inserts lose the place sentence (rule 35).
for sid in NOPERSON:
    add(sid, [SET_CLAUSE, INSERT_CLAUSE[sid] if sid in INSERTS else "T" + SET_CLAUSE[1:]])
for sid in INSERTS:
    kind = "low-angle insert close-up" if sid == "s34" else "insert close-up"
    add(sid, [f"Initial composition: {R2.LOC[INSERT_LOC[sid]]}: {kind}", "Initial composition: Insert close-up" + (", low-angle" if sid == "s34" else "")])
    add(sid, [NOBODY_OLD, NOBODY_INS])

# The road, the gate and the street: the pool words gen-dh's SET needed leave the d1 prompt.
for sid in OUTSIDE:
    if sid not in INSERTS:
        add(sid, [R2.POOLMARK, ""])

# The unnamed the compositions describe (and the horse) are named in the 'only' sentence (written twice: composition and here).
# no person picture before the appended portrait: stage 1 wrote no facial-expression sentence, which every acted face needs (and
# which carries the "never the mood. " separator the refine prep splits on): it is written here, after the 'only' sentence.
FACES = ("Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the face, "
         "hair and costume only, never the mood.")
for sid in ("s23", "s26", "s28", "s38"):
    add(sid, [BESIDES_THEM, f"{NO_COPY} {FACES}"])
add("s24", [BESIDES_THEM, NO_COPY])  # unlisted: its motion already opens with r2.py's NOBODY sentence
for sid in ("s35", "s37"):
    add(sid, [BESIDES_THEM, "Only the guard captain and the two crossbowmen behind him the composition describes are in the frame; no "
                            f"second copy of anyone appears. {FACES}"])
add("s27", [BESIDES_HER, "Only A-ling on the horse, the guard captain behind the barrier and the one horse are in the frame; no second "
                         "copy of anyone or of the horse appears."])
add("s27b", [BESIDES_HER, "Only A-ling on the horse, the guard captain on the paving and the one horse are in the frame; no second copy "
                          "of anyone or of the horse appears."])
add("s32", [BESIDES_HER, "Only the guard captain, the six crossbowmen, the one guard with the torch and A-ling seen from behind at the "
                         "right edge, the nine the composition describes, are in the frame; no second copy of anyone appears."])
add("s12", [ONLY_SHE, "Besides her, only the shoulder of the man at the right edge of the frame and the young woman in grey-white beyond "
                      "the doorway the composition describes are in the frame; no second copy of anyone appears."])
add("s14", [ONLY_HE, "Besides him, only the back of the young woman's head at the left edge of the frame the composition describes is in "
                     "the frame; no second copy of anyone appears."])
add("s36", [ONLY_SHE, "Besides her, only the two hands holding the crossbow in the foreground the composition describes are in the "
                      "frame; no second copy of anyone appears."])
for sid in ("s20", "s21", "s22", "s25", "s29", "s30"):
    add(sid, [ONLY_SHE, "Besides her, only the one horse is in the frame; no second copy of anyone or of the horse appears."])
SPECIAL_ONLY = set(TANG_BACK) | {"s12", "s14", "s20", "s21", "s22", "s23", "s24", "s25", "s26", "s27", "s27b", "s28", "s29", "s30",
                                 "s32", "s35", "s36", "s37", "s38"}
for sid in ids:
    sc = scenes[sid]
    if sid in SPECIAL_ONLY or len(sc["data"]["characters"]) != 1:
        continue
    pt = sc["data"]["prompt"]
    if "is the only person in the frame" in pt:
        her = sc["data"]["characters"][0] in ("aling", "tangxiaotang", "qinshuang", "xiaohe")
        add(sid, [ONLY_SHE if her else ONLY_HE, NO_COPY])

# Shoes.
for sid, s in SHOES_BY.items():
    add(sid, [SHOES, s])
# The clean sentence.
assert set(AIR_BY) == set(ids), sorted(set(ids) ^ set(AIR_BY))
for sid, k in AIR_BY.items():
    add(sid, [CLEAR, AIR[k]])

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
XU_TWO = ["s06", "s10", "s11", "s15"]  # gen-dh sent angle-a and angle-b only (the close-ups)
XU_WIDE = ["s01", "s19"]
for sid in XU:
    if sid not in XU_TWO:
        drop(sid, "xuyan-angle-b-l1.png")
for sid in XU_WIDE:
    drop(sid, "xuyan-angle-a-l1.png")
AL = [sid for sid in ids if "aling" in scenes[sid]["data"]["characters"]]
AL_TWO = ["s33"]
AL_WIDE = ["s16", "s20", "s22", "s27", "s27b", "s29", "s32"]
for sid in AL:
    if sid not in AL_TWO:
        drop(sid, "aling-angle-b-l1.png")
for sid in AL_WIDE:
    drop(sid, "aling-angle-a-l1.png")

SWAP = {sid: {} for sid in ids}
PLACE = {
    TF: {"set-xujia-tangfang-chen-chuang-l1.png": ["s01", "s04"], "set-xujia-tangfang-chen-men-l1.png": ["s02"],
         "set-xujia-tangfang-chen-zhen-l1.png": ["s03"], "set-xujia-tangfang-xi-zhen-l1.png": ["s05", "s11"],
         "set-xujia-tangfang-xi-chuang-l1.png": ["s06", "s07", "s08", "s10"], "set-xujia-tangfang-xi-men-l1.png": ["s09"],
         "set-xujia-tangfang-men-l1.png": ["s12", "s13"], "set-xujia-tangfang-zhen-l1.png": ["s14"],
         "set-xujia-tangfang-chuang-l1.png": ["s15", "s15b", "s19"]},
    YY: {"set-xujia-yuan-ye-dong2-l1.png": ["s16"], "set-xujia-yuan-ye-dong2-wu-l1.png": ["s17"],
         "set-xujia-yuan-ye-dong2-zhong-l1.png": ["s18"]},
    ST: {"set-guandao-ye-ce-l1.png": ["s20"], "set-guandao-ye-shu-l1.png": ["s21"],
         "set-chengmen-ye-zha-l1.png": ["s22", "s27"], "set-chengmen-ye-qiang-l1.png": ["s23", "s26"],
         "set-chengmen-ye-men-l1.png": ["s24", "s28"], "set-chengmen-ye-lu-l1.png": ["s25"], "set-chengmen-ye-l1.png": ["s27b"],
         "set-yiguan-men-ye-l1.png": ["s29"], "set-yiguan-men-ye-men-l1.png": ["s30", "s33", "s36"],
         "set-yiguan-men-ye-feng-l1.png": ["s31"], "set-yiguan-men-ye-jie-l1.png": ["s32", "s35", "s37", "s38"],
         "set-yiguan-men-ye-di-l1.png": ["s34"]},
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
    for k, _ in v.get("append_pictures", []):
        assert (L / k).is_file(), k

spec = {
    "_note": ("e938 live d1 (e937-live's way; written by mkspec.py). Tang Xiaotang from behind in s02, s04, s07, s16, s18 (pictures and "
              "identity sentence dropped); no front face of hers; every back of hers appends the owner's hair reference "
              "tangxiaotang-back-shuangji-e929-w3 by day (s02 s04 s07) and its night copy -w3-ye by night (s16 s18). The spear prop "
              "appended in s09, s12, s16, s17; the horse prop prop-zaohongma-l1 in s16, s18, s20, s21, s22, s25, s27, s27b, s29, s30; "
              "the guard captain's portrait duizhang-portrait-l1 in s23, s26, s27, s27b, s28, s32, s35, s37, s38. 'append_pictures' "
              "= [file, sentence]: prep938.sh appends the picture last, puts the sentence (N = its number) after the set clause and "
              "renumbers the header. No person picture in the inserts s31, s34 (no place sentence), s24 and the captain's shots alone. "
              "Xu Yan's angle-b nowhere; wides s01, s19 his portrait only; close-ups s06, s10, s11, s15 his portrait then angle-a. "
              "A-ling never angle-b; wides her portrait only; s33 her portrait then angle-a. The road, gate and street prompts lose "
              "' below the deep pool' (every later fix must too). The clean sentence's 'clear and still' replaced in every shot. "
              "Shoes per wide. Sets: see mkspec.py. No off-screen sentence (r2.py OFFSCREEN_SPEECH = False). Seeds 9381101/9381102."),
    "seeds": [9381101, 9381102],
    "shots": shots,
}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
