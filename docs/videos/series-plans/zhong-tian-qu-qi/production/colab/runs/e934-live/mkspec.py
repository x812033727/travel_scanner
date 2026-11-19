"""Writes spec.json next to this file: e934 live d1 (e933-live/spec.json's way; writer-tools/e034-r2/r2.py's FOOT and PLACES).
Run: python3 -I mkspec.py

- No Tang Xiaotang this episode (no back shot, no collar sentence).
- Xu Yan's smirking angle-b nowhere (e921 review). The wide s19 sends his portrait only. Where gen-dh sent only angle-a and
  angle-b (the close-ups s08, s09, s33) his portrait goes first and angle-a second (e930's XU_TWO).
- A-ling never angle-b (e930); her wide s14 her portrait only; where gen-dh sent only her two angles (the close-ups s36, s38)
  her portrait first and angle-a second (e930 s39). Qian Yuanwai never angle-b (e931); his wide s30 his portrait only.
  Qin Shuang, little Xiaohe, Elder Han, Carpenter Shi: their portraits only (gen-dh sends no angle picture of them).
- Elder Han holds no staff in s21, s22, s27, s28, s29 (r2.py HAN_NOSTAFF: the staff leans on the stone edge by the gate, lies on
  the grass, or is out of the frame): his cast sentence loses "leaning on a polished old bamboo walking staff" there.
- No person sent: s03 (the pinwheel insert: no place sentence, one sky crop written as the colour of the sky only, bible rule
  35, as e933 s27), s23 (the wheel turning), s24 (the top of the wheel), s26 (the channel: four unnamed villagers running, no
  picture), s40 (the swarm: three unnamed backs at the bottom edge). The set clause opens the sentence.
- The field and channel shots (s26-s40): r2.py's LOC carries "deep pool" only so gen-dh's SET sends the pool picture, which this
  spec swaps for the field and channel pictures; the words leave the d1 prompt here (r2.POOLMARK, r2.XQ_GEN -> r2.XQ_LIVE), so
  nothing asks for a pool the picture does not show (e033 review 必改 7: the place sentence where the picture puts it).
- 'Only' sentences: where the composition already says "... is the only person in the frame", the appended one is cut down to
  its second half (e927 review 建議). Where the composition describes unnamed people the 'only' sentence names them: the small
  hand at the corner (s01), the over-the-shoulder backs (s05 left, s06 upper right), the girl's legs across his shoulders (s39),
  the three backs (s40). s12, s15, s19, s27, s30 keep ref2manifest's "Besides ..., only the other people the composition names"
  sentence (the composition counts them); s26 has none (no person sent) and the composition says "exactly four people".
- Wides with Qin Shuang (s12, s19): extras_patch's shoes sentence would take her leather boots away; it names her boots there.
  e933 review 必改 6: a wide whose people show no feet gets no shoes sentence: s23 (nobody), s40 (backs cut at the shoulders).
- The speaking gaze never names an unsent listener (e927 必改 5, bible rule 31): r2.py's GAZE_REFINE (the same words in d1 and in
  the refine text).
- Every motion that opens a sentence after "never the mood. " is capitalised (e928 review 必改 1's fix); s03, s23, s24, s26, s40
  (no person) open with r2.py's NOBODY sentence, so the separator is there once.
- Sets (r2.py PLACES): noon and afternoon set-shentan-l3 (s12, s19; gen-dh's own pick = pilot.py's newest, not swapped), -an-l3
  (s04, s06, s07, s13, s14, s15, s20, s21), -bian-l3 (s01, s08, s09, s17), -lun-l3 (s05), -tian-l3 (s02, s11, s16; s03 as the sky
  only), -shi-l3 (s10, s18); sunset -xi-an-l3 (s22), -xi-l3 (s23), -xi-ye-l3 (s24), -xi-lun-l3 (s25), the channel
  set-shentan-qu-xi-l1 (s26); the fields set-hantian-geng-l1 (s27, s29, s34, s35), -tian-l1 (s28, s33), -liu-l1 (s30, s31, s32),
  -di-l1 (s36), grey -hui-tian-l1 (s37, s38), -hui-geng-l1 (s39), -hui-l1 (s40). Every swap is sent with an absolute path by
  prep934.sh.
- No seed of this episode has been run. Seeds 9341101/9341102.
"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROD = HERE.parents[2]
L = str(PROD / "assets" / "refs-live")
VIDEO = str(PROD.parents[2] / "zhong-tian-qu-qi-e034-r2" / "video.json")
_spec = importlib.util.spec_from_file_location("r2_934_mkspec", PROD / "writer-tools" / "e034-r2" / "r2.py")
R2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R2)

ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."
NO_COPY = "No second copy of anyone appears."
BESIDES_THEM = "Besides them, only the other people the composition names are in the frame; no second copy of anyone appears."
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
SKY_CLAUSE = "The pale sky shown in <Picture 1> gives only the colour of the background."
NOBODY_OLD = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
NOBODY_SKY = "Throughout the shot the framing stays as it is. The picture gives the colour of the sky only, never the mood. "
SHOES = "Every person in the frame wears dark cloth shoes on both feet."
SHOES_QIN = "Qin Shuang wears her leather boots and every other person in the frame dark cloth shoes on both feet."
STAFF = ", leaning on a polished old bamboo walking staff"
ST = "set-shentan-l3.png"    # pilot.py's newest set-shentan for dh-set-shentan-t1 (every LOC opens with or carries "deep pool")
INSERTS = ["s03"]
NOPERSON = ["s03", "s23", "s24", "s26", "s40"]
FIELD = [f"s{n:02d}" for n in range(27, 41)]


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


video = json.load(open(VIDEO, encoding="utf-8"))
scenes = {sc["id"]: sc for sc in video["scenes"]}
ids = [sc["id"] for sc in video["scenes"]]
assert len(ids) == 40, len(ids)
shots = {sid: {} for sid in ids}

# No person sent: the set clause opens the sentence; the insert s03 is the colour of the sky only, no place sentence (rule 35).
for sid in NOPERSON:
    add(sid, [SET_CLAUSE, SKY_CLAUSE if sid in INSERTS else "T" + SET_CLAUSE[1:]])
add("s03", [f"Initial composition: {R2.LOC['nn_e']}: insert close-up", "Initial composition: Insert close-up"])
add("s03", [NOBODY_OLD, NOBODY_SKY])

# The field and the channel: the pool words gen-dh's SET needed leave the d1 prompt.
for sid in FIELD:
    add(sid, [R2.POOLMARK, ""])
add("s26", [R2.XQ_GEN, R2.XQ_LIVE])

# The unnamed the compositions describe are named in the 'only' sentence.
add("s01", [ONLY_HE, "Besides him, only the small hand holding the pinwheel at the lower left corner of the frame the composition "
                     "describes is in the frame; no second copy of anyone appears."])
for sid, edge in (("s05", "left"), ("s06", "upper right")):
    add(sid, [ONLY_HE, f"Besides him, only the one man seen from behind at the {edge} edge of the frame the composition describes is in "
                       f"the frame; no second copy of anyone appears."])
add("s39", [ONLY_HE, "Besides him, only the small girl's two legs across his shoulders at the top edge of the frame the composition "
                     "describes are in the frame; no second copy of anyone appears."])
add("s40", [BESIDES_THEM, "Only the three people seen from behind at the bottom edge of the frame the composition describes are in "
                          "the frame; no second copy of anyone appears."])
SPECIAL_ONLY = {"s01", "s05", "s06", "s39"}
for sid in ids:
    sc = scenes[sid]
    if sid in SPECIAL_ONLY or len(sc["data"]["characters"]) != 1:
        continue
    if "is the only person in the frame" in sc["data"]["prompt"]:
        add(sid, [ONLY_SHE if sc["data"]["characters"][0] in ("qinshuang", "xiaohe", "aling") else ONLY_HE, NO_COPY])

# The wides with Qin Shuang: her boots. The wides whose people show no feet: no shoes sentence (e933 必改 6).
for sid in ("s12", "s19"):
    add(sid, [SHOES, SHOES_QIN])
for sid in ("s23", "s40"):
    add(sid, [SHOES + " ", ""])
# Elder Han holds no staff (s21, s22, s27, s28, s29).
for sid in ("s21", "s22", "s27", "s28", "s29"):
    add(sid, [STAFF, ""])

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
XU_TWO = ["s08", "s09", "s33"]  # gen-dh sent angle-a and angle-b only (the close-ups)
XU_WIDE = ["s19"]
for sid in XU:
    if sid not in XU_TWO:
        drop(sid, "xuyan-angle-b-l1.png")
for sid in XU_WIDE:
    drop(sid, "xuyan-angle-a-l1.png")
AL = [sid for sid in ids if "aling" in scenes[sid]["data"]["characters"]]
AL_TWO = ["s36", "s38"]
for sid in AL:
    if sid not in AL_TWO:
        drop(sid, "aling-angle-b-l1.png")
drop("s14", "aling-angle-a-l1.png")
QI = [sid for sid in ids if "qianyuanwai" in scenes[sid]["data"]["characters"]]
for sid in QI:
    drop(sid, "qianyuanwai-angle-b-l1.png")
drop("s30", "qianyuanwai-angle-a-l1.png")

SWAP = {sid: {} for sid in ids}
PLACE = {
    ST: {"set-shentan-l3.png": ["s12", "s19"],
         "set-shentan-an-l3.png": ["s04", "s06", "s07", "s13", "s14", "s15", "s20", "s21"],
         "set-shentan-bian-l3.png": ["s01", "s08", "s09", "s17"], "set-shentan-lun-l3.png": ["s05"],
         "set-shentan-tian-l3.png": ["s02", "s03", "s11", "s16"], "set-shentan-shi-l3.png": ["s10", "s18"],
         "set-shentan-xi-an-l3.png": ["s22"], "set-shentan-xi-l3.png": ["s23"], "set-shentan-xi-ye-l3.png": ["s24"],
         "set-shentan-xi-lun-l3.png": ["s25"], "set-shentan-qu-xi-l1.png": ["s26"],
         "set-hantian-geng-l1.png": ["s27", "s29", "s34", "s35"], "set-hantian-tian-l1.png": ["s28", "s33"],
         "set-hantian-liu-l1.png": ["s30", "s31", "s32"], "set-hantian-di-l1.png": ["s36"],
         "set-hantian-hui-tian-l1.png": ["s37", "s38"], "set-hantian-hui-geng-l1.png": ["s39"], "set-hantian-hui-l1.png": ["s40"]},
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
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e934 live d1 (e933-live's way; written by mkspec.py). No Tang Xiaotang. No person sent in s03 (the pinwheel insert: no "
              "place sentence, one sky crop written as the colour of the sky only), s23, s24 (the wheel), s26 (the channel), s40 (the "
              "swarm). Xu Yan's angle-b nowhere; the wide s19 his portrait only; s08, s09, s33 his portrait then angle-a. "
              "A-ling never angle-b; s14 her portrait only; s36, s38 her portrait then angle-a. Qian Yuanwai never angle-b; s30 his "
              "portrait only. Sets: see mkspec.py (the pool at noon and afternoon set-shentan-l3 and crops, the free sunset -xi, the "
              "channel -qu-xi, the fields set-hantian crops and the grey -hui); the pool words leave the field and channel prompts. "
              "No off-screen sentence (r2.py OFFSCREEN_SPEECH = False). Seeds 9341101/9341102."),
    "seeds": [9341101, 9341102],
    "shots": shots,
}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
