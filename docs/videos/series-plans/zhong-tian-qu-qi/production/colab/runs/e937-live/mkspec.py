"""Writes spec.json next to this file: e937 live d1 (e936-live/spec.json's way; writer-tools/e037-r2/r2.py's FOOT and PLACES).
Run: python3 -I mkspec.py

- Style sentence (e935 §8): pilot.py's opening sentence ends "with the look of a feature film."; every anchor here that follows
  it uses those words, and prep937.sh asserts no "cinema camera" is left in any d1 prompt.
- Tang Xiaotang (bible rule 40): her three speaking back shots (s32, s34, s35) drop her three pictures and her identity sentence
  (it also names the gold abacus at her waist, rule 20); the 'only' sentence says she is seen from behind and appears once. She
  has no front face this episode. Her silent backs (s07, s09) are not listed characters (no picture). Owner 2026-11-22 (PR #2217,
  OWNER-CHECK-20261122.md): every back shot of hers (s07, s09, s32, s34, s35) also sends refs-live/tangxiaotang-back-shuangji-
  e929-w3.png, the two round buns seen from behind, as the LAST picture with one sentence that ties it to the hair only
  ("append_pictures": prep937.sh appends the picture, renumbers the header and puts the sentence after the set clause).
- Qin Shuang's spear (bible 〈道具〉, 2026-11-17 定要畫): the shots with the spear in a hand (s26 the raider's, s27, s36) append
  refs-live/prop-changqiang-l1.png the same way, with a sentence that makes it the one spear of the shot. s35 (a wide, the spear
  small) and s28 (only its head at the edge) do not.
- Xu Yan's smirking angle-b nowhere (e921 review). The wides (s04, s09b, s10, s35, s39) send his portrait only. Where gen-dh sent
  only angle-a and angle-b (the close-ups s03, s15, s16, s37, s38) his portrait goes first and angle-a second (e930's XU_TWO).
- Wang Erniu: where gen-dh sends erniu-angle-a with no portrait (the close-up s02) it becomes his portrait (e931-e933); the wides
  s01, s28 his portrait only. A-ling never angle-b (e930); the wide s31 her portrait only. Qin Shuang, Diao Qi, little Xiaohe:
  their portraits only (gen-dh sends no angle of them; Diao Qi has none).
- No person sent: the inserts s08 (Tang Xiaotang's hands on his sleeve) and s23 (the burning straw and Wang Erniu's foot): no
  place sentence (rule 35), "Initial composition: <LOC>: insert close-up" becomes "Initial composition: Insert close-up"; their
  one picture is a free crop written as the ground and the light only; the standard insert sentence becomes NOBODY_INS. s17 and
  s21 (the raiders as far shapes, no named person): the set clause opens the sentence.
- The channel (s10-s28, s35-s40): r2.py's LOC carries " below the deep pool" only so gen-dh's SET sends the pool picture, which
  this spec swaps for the channel pictures; the words leave the d1 prompt here (r2.POOLMARK -> ""). Every later fix / retake
  spec of these shots must carry the same replacement.
- 'Only' sentences (the task file 2026-11-20: one more person than written is common, so the count is written twice, in the
  composition and here at the end): where the composition already says "... is the only person in the frame" the appended
  one is cut down to its second half; where the composition describes unnamed people the 'only' sentence names them.
- Shoes (extras_patch's wide-shot sentence): Qin Shuang's leather boots named where she is in a wide (s04, s13, s35; e933's
  lesson); the refugees, fighters and raiders wear straw sandals beside the cloth shoes of the named (s01, s09b, s10, s13, s28,
  s31, s34, s35); s21 shows no feet that matter (the sentence goes).
- The clean sentence ends "the air is clear and still, a clean natural film image" (CLEAR); every shot of this night replaces
  it: the night air, the lamp's flame, the torchlight, the white lime powder, the steam of the bucket, the cold air of dawn.
- The speaking gaze never names an unsent listener (bible rule 31): r2.py's GAZE_REFINE (the same words in d1 and in the refine
  text). Every motion that opens a sentence after "never the mood. " is capitalised (e928 review 必改 1's fix).
- Sets (r2.py PLACES): the yard: e931's set-xujia-yuan-ye-dong2-l1 (s09b), e936's crops -zhong (s01), -qiang (s04, s05), -chai
  (s06, s09), -wu (s07) and this episode's -shu (s02, s03), -di (s08); the back gate set-xujia-houmen-ye-l1 (s31), -men (s29,
  s30), -xiang (s32, s33, s34): all swapped for pilot.py's newest set-xujia-yuan-ye (l2, never sent); the channel by night
  set-shanjiao-qu-ye2-l1 (s10, s13), -ye2-zhuo, -ye2-geng, -ye2-tian, -ye2-kong, -ye2-cao, at dawn set-shanjiao-qu-chen-l1
  (s35), -chen-tian, -chen-zhuo, -chen-geng: swapped for pilot.py's newest set-shentan (never sent). Every swap is sent with an
  absolute path by prep937.sh.
- No seed of this episode has been run. Seeds 9371101/9371102.
"""
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROD = HERE.parents[2]
L = Path(PROD / "assets" / "refs-live")
VIDEO = str(PROD.parents[2] / "zhong-tian-qu-qi-e037-r2" / "video.json")
_spec = importlib.util.spec_from_file_location("r2_937_mkspec", PROD / "writer-tools" / "e037-r2" / "r2.py")
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
HAIR_PIC = "tangxiaotang-back-shuangji-e929-w3.png"
HAIR_SENT = ("The back of the young woman's head looks exactly like <Picture N>: the same smooth black hair parted down the "
             "middle and gathered into just two round buns, one on each side, each wrapped with one short pink silk ribbon; that "
             "picture fixes the hairstyle only, never the place or the light.")
SPEAR_PIC = "prop-changqiang-l1.png"
SPEAR_SENT = ("The long spear shown in <Picture N> is the one spear in this shot, keeping exactly its plain wooden shaft and its "
              "small plain iron spearhead; that picture fixes the spear only, never the place or the light.")
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
    "s08": "The packed dark earth shown in <Picture 1> gives only the ground and the light of the background.",
    "s23": "The cracked dry earth shown in <Picture 1> gives only the ground and the light of the background.",
}
INSERT_LOC = {"s08": "ny_e", "s23": "q2_e"}
SHOES = "Every person in the frame wears dark cloth shoes on both feet."
SHOES_BY = {
    "s01": "Wang Erniu wears dark cloth shoes and the four men on the mats wear worn straw sandals on both feet.",
    "s04": "Xu Yan wears dark cloth shoes and Qin Shuang wears her leather boots.",
    "s09b": "Xu Yan wears dark cloth shoes and the six men wear worn straw sandals on both feet.",
    "s10": "Xu Yan wears dark cloth shoes and the four men with the sacks wear worn straw sandals on both feet.",
    "s13": "Qin Shuang wears her leather boots and every other person in the frame wears worn straw sandals on both feet.",
    "s28": "Wang Erniu wears dark cloth shoes and Diao Qi wears worn straw sandals over his black leg wraps.",
    "s31": "A-ling wears soft cloth shoes and the eight raiders wear worn straw sandals on both feet.",
    "s34": "The young woman wears soft cloth shoes and the six raiders wear worn straw sandals on both feet.",
    "s35": ("Xu Yan and the young woman wear cloth shoes, Qin Shuang wears her leather boots and the three men wear worn straw "
            "sandals on both feet."),
}
CLEAR = "the air is clear and still, a clean natural film image"
AIR = {
    "night": "the cool night air, a clean natural film image",
    "lamp": "the cool night air, the small lamp flame swaying, a clean natural film image",
    "torch": "the cold night air, the torch flames wavering, a clean natural film image",
    "powder": "fine white lime powder drifting in the cold night air, a clean natural film image",
    "flame": "the cold night air, the small flames in the straw dancing, a clean natural film image",
    "steam": "the cold night air, the steam from the hot water curling, a clean natural film image",
    "dawn": "the cold still air of dawn, a thin drift of pale powder low over the field, a clean natural film image",
    "dawn2": "the cold still air of dawn, a clean natural film image",
}
AIR_BY = {**{s: "night" for s in ("s01", "s02", "s05", "s08", "s09b", "s10", "s11", "s12", "s13", "s14", "s15", "s16", "s16b", "s19",
                                  "s20", "s29", "s30", "s33")},
          **{s: "lamp" for s in ("s03", "s04", "s06", "s07", "s09")},
          **{s: "torch" for s in ("s17", "s18", "s31", "s34")},
          **{s: "powder" for s in ("s21", "s22", "s24", "s25", "s26", "s27", "s28")},
          "s23": "flame", "s32": "steam",
          **{s: "dawn" for s in ("s35", "s36", "s37")}, **{s: "dawn2" for s in ("s38", "s39", "s40")}}
INSERTS = ["s08", "s23"]
NOPERSON = INSERTS + ["s17", "s21"]


def newest(sid_id):
    vs = [q for q in L.glob(f"set-{sid_id}-l*.png") if re.fullmatch(rf"set-{sid_id}-l\d+", q.stem)]
    return max(vs, key=lambda q: int(q.stem.rsplit("-l", 1)[1])).name


ST = newest("shentan")       # pilot.py's newest set-shentan for dh-set-shentan-t1 (the channel's " below the deep pool")
YY = newest("xujia-yuan-ye")  # pilot.py's newest set-xujia-yuan-ye for dh-set-xujia-yuan-ye-t1 ("night yard of the Xu farmhouse")
assert YY == "set-xujia-yuan-ye-l2.png", YY


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


def append_pic(sid, pic, sentence):
    shots[sid].setdefault("append_pictures", []).append([pic, sentence])


def back(beyond, n=2):
    return (f"Only these {n} people are in the frame, the young woman with the buns seen only from behind and {beyond}; "
            f"{ONE_TANG}; no second copy of anyone appears.")


video = json.load(open(VIDEO, encoding="utf-8"))
scenes = {sc["id"]: sc for sc in video["scenes"]}
ids = [sc["id"] for sc in video["scenes"]]
assert len(ids) == 42, len(ids)
shots = {sid: {} for sid in ids}
CHANNEL = ids[ids.index("s10"):ids.index("s29")] + ids[ids.index("s35"):]
assert CHANNEL[0] == "s10" and len(CHANNEL) == 26, CHANNEL

# Tang Xiaotang from behind: her identity sentence and her three pictures leave; the hair reference joins every back of hers.
TANG_BACK = {
    "s32": [BESIDES_HER, "Only the young woman with the buns seen only from behind and the one raider as a dark shape the composition "
                         f"describes are in the frame; {ONE_TANG}; no second copy of anyone appears."],
    "s34": [BESIDES_HER, "Only the young woman with the buns seen only from behind and the six raiders as dark running shapes the "
                         f"composition describes are in the frame; {ONE_TANG}; no second copy of anyone appears."],
    "s35": [BESIDES_THEM, "Only Xu Yan, Qin Shuang, the young woman with the buns seen only from behind and the three men with hoes "
                          f"the composition describes are in the frame; {ONE_TANG}; no second copy of anyone appears."],
}
for sid, onl in TANG_BACK.items():
    add(sid, [TANG_ID, ""])
    add(sid, onl)
    drop(sid, *TANG_PICS)
for sid in ("s32", "s34"):  # alone: her identity sentence opened the prompt; the set clause now does (before the drop renumbers)
    add(sid, [f"{STYLE_END} the location shown in <Picture 4>", f"{STYLE_END} The location shown in <Picture 4>"])
for sid in ("s07", "s09"):  # her silent backs, unlisted
    add(sid, [ONLY_HE, back("Xu Yan one step beyond her in the left third of the frame")])
for sid in ("s07", "s09", "s32", "s34", "s35"):
    append_pic(sid, HAIR_PIC, HAIR_SENT)
for sid in ("s26", "s27", "s36"):
    append_pic(sid, SPEAR_PIC, SPEAR_SENT)

# No person sent: the set clause opens the sentence; the inserts lose the place sentence (rule 35).
for sid in NOPERSON:
    add(sid, [SET_CLAUSE, INSERT_CLAUSE[sid] if sid in INSERTS else "T" + SET_CLAUSE[1:]])
for sid in INSERTS:
    add(sid, [f"Initial composition: {R2.LOC[INSERT_LOC[sid]]}: insert close-up", "Initial composition: Insert close-up"])
    add(sid, [NOBODY_OLD, NOBODY_INS])

# The channel: the pool words gen-dh's SET needed leave the d1 prompt.
for sid in CHANNEL:
    if sid not in INSERTS:
        add(sid, [R2.POOLMARK, ""])

# The unnamed the compositions describe are named in the 'only' sentence (written twice: composition and here).
add("s01", [BESIDES_HIM, "Only Wang Erniu and the four men on the mats the composition describes, each in a different colour, are "
                         "in the frame; no second copy of anyone appears."])
add("s06", [ONLY_HE, "Besides him, only the young woman with the high ponytail seen from behind at the right edge of the frame the "
                     "composition describes is in the frame; no second copy of anyone appears."])
add("s09b", [BESIDES_HIM, "Only Xu Yan and the six men with hoes the composition describes, each in a different colour, are in the "
                          "frame; no second copy of anyone appears."])
add("s10", [BESIDES_HIM, "Only Xu Yan and the four men with the sacks the composition describes, each in a different colour, are in "
                         "the frame; no second copy of anyone appears."])
add("s13", [BESIDES_HER, "Only Qin Shuang and the six men in three rows the composition describes, each in a different colour, are "
                         "in the frame; no second copy of anyone appears."])
for sid in ("s14", "s25"):
    pr = "her" if sid == "s14" else "him"
    add(sid, [ONLY_SHE if sid == "s14" else ONLY_HE,
              f"Besides {pr}, only the shoulder of the man at the right edge of the frame the composition describes is in the frame; "
              "no second copy of anyone appears."])
add("s36", [ONLY_SHE, "Besides her, only the shoulder of the man at the left edge of the frame the composition describes is in the "
                      "frame; no second copy of anyone appears."])
add("s17", [BESIDES_THEM, "Only the three heads and the six running shapes the composition describes are in the frame; no second "
                          "copy of anyone appears."])
add("s18", [BESIDES_HIM, "Besides him, only the three running shapes with torches the composition describes are in the frame; no second "
                     "copy of anyone appears."])
add("s20", [BESIDES_HER, "Besides her, only the three men with sacks the composition describes are in the frame; no second copy of "
                      "anyone appears."])
add("s21", [BESIDES_THEM, "Only the six dark shapes the composition describes are in the frame; no second copy of anyone appears."])
add("s26", [BESIDES_HER, "Besides her, only the one raider seen from behind the composition describes is in the frame; no second copy "
                      "of anyone appears."])
add("s31", [BESIDES_HER, "Only A-ling and the eight raiders as dark shapes the composition describes are in the frame; no second copy "
                         "of anyone appears."])
add("s33", [BESIDES_HER, "Besides her, only the one raider seen from behind the composition describes is in the frame; no second copy "
                      "of anyone appears."])
add("s28", [ONLY_2, "Only these 2 people, Wang Erniu and the kneeling Diao Qi, are in the frame, with only the head of a spear at the left "
                    "edge; no second copy of anyone appears."])
add("s39", [BESIDES_THEM, "Only Xu Yan, little Xiaohe and the two women on the bank the composition describes are in the frame; no "
                          "second copy of anyone appears."])
SPECIAL_ONLY = set(TANG_BACK) | {"s01", "s06", "s07", "s09", "s09b", "s10", "s13", "s14", "s17", "s18", "s20", "s21", "s25", "s26",
                                 "s28", "s31", "s33", "s36", "s39"}
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
add("s21", [SHOES + " ", ""])
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
XU_TWO = ["s03", "s15", "s16", "s37", "s38"]  # gen-dh sent angle-a and angle-b only (the close-ups)
XU_WIDE = ["s04", "s09b", "s10", "s35", "s39"]
for sid in XU:
    if sid not in XU_TWO:
        drop(sid, "xuyan-angle-b-l1.png")
for sid in XU_WIDE:
    drop(sid, "xuyan-angle-a-l1.png")
ER_WIDE = ["s01", "s28"]
for sid in ER_WIDE:
    drop(sid, "erniu-angle-a-l1.png")
AL = [sid for sid in ids if "aling" in scenes[sid]["data"]["characters"]]
for sid in AL:
    drop(sid, "aling-angle-b-l1.png")
drop("s31", "aling-angle-a-l1.png")

SWAP = {sid: {} for sid in ids}
PLACE = {
    YY: {"set-xujia-yuan-ye-dong2-zhong-l1.png": ["s01"], "set-xujia-yuan-ye-dong2-shu-l1.png": ["s02", "s03"],
         "set-xujia-yuan-ye-dong2-qiang-l1.png": ["s04", "s05"], "set-xujia-yuan-ye-dong2-chai-l1.png": ["s06", "s09"],
         "set-xujia-yuan-ye-dong2-wu-l1.png": ["s07"], "set-xujia-yuan-ye-dong2-di-l1.png": ["s08"],
         "set-xujia-yuan-ye-dong2-l1.png": ["s09b"],
         "set-xujia-houmen-ye-men-l1.png": ["s29", "s30"], "set-xujia-houmen-ye-l1.png": ["s31"],
         "set-xujia-houmen-ye-xiang-l1.png": ["s32", "s33", "s34"]},
    ST: {"set-shanjiao-qu-ye2-l1.png": ["s10", "s13"],
         "set-shanjiao-qu-ye2-zhuo-l1.png": ["s11", "s14", "s17", "s18", "s21", "s22", "s25"],
         "set-shanjiao-qu-ye2-geng-l1.png": ["s12", "s24", "s26", "s27", "s28"],
         "set-shanjiao-qu-ye2-tian-l1.png": ["s15", "s16", "s16b", "s19"], "set-shanjiao-qu-ye2-kong-l1.png": ["s20"],
         "set-shanjiao-qu-ye2-cao-l1.png": ["s23"], "set-shanjiao-qu-chen-l1.png": ["s35"],
         "set-shanjiao-qu-chen-tian-l1.png": ["s36", "s38"], "set-shanjiao-qu-chen-zhuo-l1.png": ["s37"],
         "set-shanjiao-qu-chen-geng-l1.png": ["s39", "s40"]},
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
SWAP["s02"]["erniu-angle-a-l1.png"] = "erniu-portrait-l1.png"
for sid, sw in SWAP.items():
    if sw:
        shots[sid]["swap_pictures"] = sw
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (L / k).is_file(), k
    for k, _ in v.get("append_pictures", []):
        assert (L / k).is_file(), k

spec = {
    "_note": ("e937 live d1 (e936-live's way; written by mkspec.py). Tang Xiaotang from behind in s32, s34, s35 (pictures and "
              "identity sentence dropped); her silent backs s07, s09 unlisted; her voice over the insert s08; no front face of hers; "
              "every back of hers appends the owner's hair reference tangxiaotang-back-shuangji-e929-w3 (2026-11-22). The spear prop "
              "picture appended in s26, s27, s36. 'append_pictures' = [file, sentence]: prep937.sh appends the picture last, puts "
              "the sentence (N = its number) after the set clause and renumbers the header. No person sent in the inserts s08, s23 "
              "(no place sentence) and s17, s21. Xu Yan's angle-b nowhere; wides his portrait only; close-ups s03, s15, s16, s37, s38 "
              "his portrait then angle-a. Wang Erniu's angle-a becomes his portrait in s02; wides s01, s28 portrait only. A-ling "
              "never angle-b; s31 portrait only. The channel prompts lose ' below the deep pool' (every later fix must too). The "
              "clean sentence's 'clear and still' replaced in every shot (night air, lamp, torchlight, lime powder, steam, dawn). "
              "Shoes per wide (Qin Shuang's boots; straw sandals on the unnamed). Sets: see mkspec.py. No off-screen sentence "
              "(r2.py OFFSCREEN_SPEECH = False). Seeds 9371101/9371102."),
    "seeds": [9371101, 9371102],
    "shots": shots,
}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
