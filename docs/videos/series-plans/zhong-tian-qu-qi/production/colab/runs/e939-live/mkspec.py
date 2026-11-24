"""Writes spec.json next to this file: e939 live d1 (e938-live/spec.json's way; writer-tools/e039-r2/r2.py's FOOT and PLACES).
Run: python3 -I mkspec.py

- Style sentence (e935 §8): pilot.py's opening sentence ends "with the look of a feature film."; check939.py asserts no "cinema
  camera" is left in any d1 prompt.
- Tang Xiaotang is not in this episode: nothing of hers to drop or append.
- The horse (bible rule 41, 〈道具〉; e938 REVIEW 3 / fix6): every shot with the horse in the frame (s08, s09, s10, s11, s13) appends
  refs-live/prop-zaohongma-an-l1.png (the picked saddled chestnut: a folded dark grey-brown felt pad girthed with rope, no saddle
  horn, nothing bright) as the LAST picture with one sentence that makes it the one horse and points the saddle pad at the
  picture (fix6's lesson: H3 draws a high western saddle from any words when the picture is the bare-backed horse).
- The guard captain (bible 〈人物〉; r2.py MINOR "duizhang", no live portrait in gen-dh.mjs / pilot.py): his shots (s02, s03, s09)
  append refs-live/duizhang-portrait-l1.png with a sentence that fixes his face, helmet and armour only.
- Qin Shuang's spear (bible 〈道具〉): s34, s36, s39 append refs-live/prop-changqiang-l1.png.
- Xu Yan's smirking angle-b nowhere (e921 review). Where gen-dh sent only angle-a and angle-b (the close-ups s15, s25, s28, s29,
  s31, s33) his portrait goes first and angle-a second (e930's XU_TWO).
- A-ling never angle-b (e930); the two-riders shots and the wides (s08, s09, s10, s13) her portrait only. Qian Yuanwai never his
  angle-b (s38). Wang Erniu's angle-a out of the wide s36 (his portrait only). Doctor Bai, Elder Han, Diao Qi, Qin Shuang, little
  Xiaohe: their portraits only (gen-dh sends no angle).
- No person picture sent: the insert s19 (the medicine chest and the hands): no place sentence (rule 35), "Initial composition:
  <LOC>: insert close-up" becomes "Initial composition: Insert close-up"; its one picture is this episode's free -kong-bei crop
  written as the ground and the light only; the standard insert sentence becomes NOBODY_INS. s03 (the captain alone): the set
  clause opens the sentence and the facial-expression sentence (with its "never the mood. " separator) is written after the
  'only' sentence (e938's CAP_ALONE).
- The street, the road and the barn front (s01-s13, s36-s40): r2.py's LOC carries " below the deep pool" only so gen-dh's SET
  sends the pool picture, which this spec swaps for this episode's pictures; the words leave the d1 prompt here (r2.POOLMARK ->
  ""). Every later fix / retake spec of these shots must carry the same replacement.
- 'Only' sentences (the task file 2026-11-20: the count written twice, in the composition and here at the end): where the
  composition already says "... is the only person in the frame" the appended one is cut down to its second half; where the
  composition describes unnamed people, partial people or the horse the 'only' sentence names them.
- Shoes (extras_patch's wide-shot sentence): the riders' soft cloth shoes (s09, s13), the captain's and the guards' black boots
  (s09), Qin Shuang's leather boots and the others' cloth shoes or straw sandals (s36, s39).
- The clean sentence ends "the air is clear and still, a clean natural film image" (CLEAR); every shot replaces it: the cold night
  street, the torch far up the street, the dust of the road, the small candle flame, the grey first light, the morning air.
- The speaking gaze never names an unsent listener (bible rule 31): r2.py's GAZE_REFINE (the same words in d1 and in the refine
  text). Every motion that opens a sentence after "never the mood. " is capitalised (e928 review 必改 1's fix).
- Sets (r2.py PLACES): the sickroom: pilot.py's newest set-xujia-tangfang (l2) swapped for e938's -kong / -kong-chen crops and this
  episode's -kong-bei; the street, the road and the barn front: pilot.py's newest set-shentan (never sent) swapped for e938's
  set-yiguan-men-ye-men / -jie and the whole set-yiguan-men-ye-l1, e938's set-guandao-ye-shu and the whole set-guandao-ye-l1, the
  whole set-gucang-wai-l1 and this episode's -men / -tian / -qiang. Every swap is sent with an absolute path by check939.py.
- No seed of this episode has been run. Seeds 9391101/9391102.
"""
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROD = HERE.parents[2]
L = Path(PROD / "assets" / "refs-live")
VIDEO = str(PROD.parents[2] / "zhong-tian-qu-qi-e039-r2" / "video.json")
_spec = importlib.util.spec_from_file_location("r2_939_mkspec", PROD / "writer-tools" / "e039-r2" / "r2.py")
R2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R2)

HORSE_PIC = "prop-zaohongma-an-l1.png"
HORSE_SENT = ("The horse shown in <Picture N> is the one horse in this shot, keeping exactly its deep red-brown coat, its mane and "
              "tail of the same red-brown, its plain dark bridle and exactly its folded dark grey-brown felt saddle pad and rope girth "
              "as the picture shows them; that picture fixes the horse only, never the place or the light.")
CAP_PIC = "duizhang-portrait-l1.png"
CAP_SENT = ("The guard captain looks exactly like <Picture N>: the same square face and short black beard, the same black lamellar "
            "armour with small red studs and the same round iron helmet with cheek flaps and a small tuft of red horsehair; that picture fixes "
            "his face, helmet and armour only, never the place or the light.")
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
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
NOBODY_OLD = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
NOBODY_INS = "Throughout the shot the framing stays as it is. The picture gives the ground and the light of the background only, never the mood. "
INSERT_CLAUSE = {"s19": "The pink quilted cover shown in <Picture 1> gives only the ground and the light of the background."}
INSERT_LOC = {"s19": "rx_x"}
SHOES = "Every person in the frame wears dark cloth shoes on both feet."
SHOES_BY = {
    "s09": "A-ling and Doctor Bai wear soft dark cloth shoes, and the guard captain and every guard wear black leather boots.",
    "s13": "A-ling and Doctor Bai wear soft dark cloth shoes.",
    "s36": "Qin Shuang wears her leather boots, Diao Qi wears worn straw sandals, and everyone else wears dark cloth shoes.",
    "s39": "Qin Shuang wears her leather boots and Diao Qi wears worn straw sandals.",
}
CLEAR = "the air is clear and still, a clean natural film image"
AIR = {
    "street": "the cold night air of an empty street, a clean natural film image",
    "torch": "the cold night air, the one torch flame far up the street wavering, a clean natural film image",
    "road": "the cold night air, the dust of the road drifting behind the hooves, a clean natural film image",
    "lamp": "the still night air, the small candle flame swaying, a clean natural film image",
    "still": "the still night air, a clean natural film image",  # the insert: no place word (rule 35)
    "morn": "the cold still air of first light, a clean natural film image",
    "barn": "the fresh still air of early morning, a clean natural film image",
}
AIR_BY = {**{s: "street" for s in ("s01", "s03", "s04", "s05", "s06", "s07", "s08")}, "s02": "torch", "s09": "torch",
          **{s: "road" for s in ("s10", "s11", "s12", "s13")},
          **{s: "lamp" for s in ("s14", "s15", "s16", "s17", "s18", "s20", "s21", "s22", "s23")}, "s19": "still",
          **{s: "morn" for s in ("s24", "s25", "s26", "s27", "s28", "s28b", "s29", "s29b", "s30", "s31", "s32", "s33", "s34", "s35")},
          **{s: "barn" for s in ("s36", "s37", "s38", "s39", "s40")}}
INSERTS = ["s19"]
CAP_ALONE = ["s03"]
NOPERSON = INSERTS + CAP_ALONE  # no person picture before the appended ones: the set clause opens the sentence
FACES = ("Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the face, "
         "hair and costume only, never the mood.")


def newest(sid_id):
    vs = [q for q in L.glob(f"set-{sid_id}-l*.png") if re.fullmatch(rf"set-{sid_id}-l\d+", q.stem)]
    return max(vs, key=lambda q: int(q.stem.rsplit("-l", 1)[1])).name


ST = newest("shentan")             # pilot.py's newest set-shentan for dh-set-shentan-t1 (" below the deep pool")
TF = newest("xujia-tangfang")      # pilot.py's newest set-xujia-tangfang for dh-set-xujia-tangfang-t1 ("first bedroom of the Xu farmhouse")
assert TF == "set-xujia-tangfang-l2.png" and ST == "set-shentan-l5.png", (TF, ST)


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


def append_pic(sid, pic, sentence):
    shots[sid].setdefault("append_pictures", []).append([pic, sentence])


video = json.load(open(VIDEO, encoding="utf-8"))
scenes = {sc["id"]: sc for sc in video["scenes"]}
ids = [sc["id"] for sc in video["scenes"]]
assert len(ids) == 42, len(ids)
shots = {sid: {} for sid in ids}
STREET_ROAD = ids[:ids.index("s14")]
BARN = ids[ids.index("s36"):]
OUTSIDE = STREET_ROAD + BARN
assert len(STREET_ROAD) == 13 and len(BARN) == 5, (STREET_ROAD, BARN)

HORSE_SH = ["s08", "s09", "s10", "s11", "s13"]
for sid in HORSE_SH:
    append_pic(sid, HORSE_PIC, HORSE_SENT)
CAP_SH = ["s02", "s03", "s09"]
for sid in CAP_SH:
    append_pic(sid, CAP_PIC, CAP_SENT)
SPEAR_SH = ["s34", "s36", "s39"]
for sid in SPEAR_SH:
    append_pic(sid, SPEAR_PIC, SPEAR_SENT)

# No person picture: the set clause opens the sentence; the insert loses the place sentence (rule 35).
for sid in NOPERSON:
    add(sid, [SET_CLAUSE, INSERT_CLAUSE[sid] if sid in INSERTS else "T" + SET_CLAUSE[1:]])
for sid in INSERTS:
    add(sid, [f"Initial composition: {R2.LOC[INSERT_LOC[sid]]}: insert close-up", "Initial composition: Insert close-up"])
    add(sid, [NOBODY_OLD, NOBODY_INS])

# The street, the road and the barn front: the pool words gen-dh's SET needed leave the d1 prompt.
for sid in OUTSIDE:
    add(sid, [R2.POOLMARK, ""])

# 'Only' sentences: the unnamed, the partial people and the horse the compositions describe are named here (written twice).
add("s02", [BESIDES_HIM, "Only Doctor Bai seen from behind in the foreground, the guard captain, the six crossbowmen and the one guard "
                         "with the torch, the nine people the composition describes, are in the frame; no second copy of anyone appears."])
add("s03", [BESIDES_THEM, "Only the guard captain and the two crossbowmen behind him the composition describes are in the frame; no "
                          f"second copy of anyone appears. {FACES}"])
for sid in ("s08", "s10"):
    add(sid, [ONLY_2, "Only these 2 people and the one horse are in the frame, A-ling in front and Doctor Bai tied on behind her; no "
                      "second copy of anyone or of the horse appears."])
add("s13", [ONLY_2, "Only these 2 people and the one horse are in the frame, A-ling in front and Doctor Bai tied on behind her, small "
                    "on the road; no second copy of anyone or of the horse appears."])
add("s09", [BESIDES_THEM, "Only A-ling and Doctor Bai on the one horse, and far up the street the guard captain, the six crossbowmen "
                          "and the one guard with the torch, the ten people and the horse the composition describes, are in the frame; "
                          "no second copy of anyone or of the horse appears."])
add("s11", [ONLY_SHE, "Besides her, only the white hair, the shut eyes and the two hands of the old man tied on behind her, and the one "
                      "horse, are in the frame; no second copy of anyone or of the horse appears."])
add("s12", [ONLY_HE, "Besides him, only the back of the young woman's head in the lower left foreground the composition describes is in "
                     "the frame; no second copy of anyone appears."])
add("s27", [ONLY_HE, "Besides him, only the back of the young woman's head and her shoulder at the left edge of the frame the "
                     "composition describes are in the frame; no second copy of anyone appears."])
add("s36", [BESIDES_THEM, "Only the ten people the composition describes are in the frame: Diao Qi kneeling, the young man in rust-red "
                          "holding the rope, the broad-backed man in undyed hemp, the five others at the edge of the field, Wang Erniu "
                          "and Qin Shuang; no second copy of anyone appears."])
add("s37", [BESIDES_HIM, "Besides him, only the two men of the village seen from behind in the foreground the composition describes are "
                         "in the frame; no second copy of anyone appears."])
add("s38", [BESIDES_HIM, "Besides him, only the two men of the village at the edges of the frame the composition describes are in the "
                         "frame; no second copy of anyone appears."])
add("s40", [ONLY_HE, "He is the only person in focus; the soft shapes behind him stay faceless and blurred; no second copy of anyone "
                     "appears."])
SPECIAL_ONLY = {"s02", "s03", "s08", "s09", "s10", "s11", "s12", "s13", "s27", "s36", "s37", "s38", "s40"}
for sid in ids:
    sc = scenes[sid]
    if sid in SPECIAL_ONLY or len(sc["data"]["characters"]) != 1:
        continue
    pt = sc["data"]["prompt"]
    if "is the only person in the frame" in pt:
        her = sc["data"]["characters"][0] in ("aling", "qinshuang", "xiaohe")
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
XU_TWO = ["s15", "s25", "s28", "s29", "s31", "s33"]  # gen-dh sent angle-a and angle-b only (the close-ups)
for sid in XU:
    if sid not in XU_TWO:
        drop(sid, "xuyan-angle-b-l1.png")
AL = [sid for sid in ids if "aling" in scenes[sid]["data"]["characters"]]
AL_WIDE = ["s08", "s09", "s10", "s13"]
for sid in AL:
    drop(sid, "aling-angle-b-l1.png")
for sid in AL_WIDE:
    drop(sid, "aling-angle-a-l1.png")
drop("s38", "qianyuanwai-angle-b-l1.png")
drop("s36", "erniu-angle-a-l1.png")

SWAP = {sid: {} for sid in ids}
PLACE = {
    TF: {"set-xujia-tangfang-kong-zhen-l1.png": ["s14", "s18"],
         "set-xujia-tangfang-kong-chuang-l1.png": ["s15", "s17", "s20", "s21"],
         "set-xujia-tangfang-kong-men-l1.png": ["s16", "s22", "s23"],
         "set-xujia-tangfang-kong-bei-l1.png": ["s19"],
         "set-xujia-tangfang-kong-chen-zhen-l1.png": ["s24", "s28", "s29b", "s31", "s32"],
         "set-xujia-tangfang-kong-chen-chuang-l1.png": ["s25", "s27", "s28b", "s29", "s30", "s33", "s35"],
         "set-xujia-tangfang-kong-chen-men-l1.png": ["s26", "s34"]},
    ST: {"set-yiguan-men-ye-men-l1.png": ["s01", "s04", "s05", "s06", "s07", "s08"],
         "set-yiguan-men-ye-jie-l1.png": ["s02", "s03"], "set-yiguan-men-ye-l1.png": ["s09"],
         "set-guandao-ye-shu-l1.png": ["s10", "s11", "s12"], "set-guandao-ye-l1.png": ["s13"],
         "set-gucang-wai-l1.png": ["s36"], "set-gucang-wai-men-l1.png": ["s37", "s39"],
         "set-gucang-wai-tian-l1.png": ["s38"], "set-gucang-wai-qiang-l1.png": ["s40"]},
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
    for k, _ in v.get("append_pictures", []):
        assert (L / k).is_file(), k

spec = {
    "_note": ("e939 live d1 (e938-live's way; written by mkspec.py). No Tang Xiaotang this episode. The saddled horse "
              "prop-zaohongma-an-l1 appended in s08, s09, s10, s11, s13 (its felt pad written as in the picture: e938 fix6); the guard "
              "captain's portrait duizhang-portrait-l1 in s02, s03, s09; the spear prop in s34, s36, s39. 'append_pictures' = [file, "
              "sentence]: check939.py appends the picture last, puts the sentence (N = its number) after the set clause and renumbers "
              "the header. No person picture in the insert s19 (no place sentence) and the captain's s03. Xu Yan's angle-b nowhere; "
              "close-ups s15, s25, s28, s29, s31, s33 his portrait then angle-a. A-ling never angle-b; the two-riders shots and the "
              "wides her portrait only. Qian Yuanwai never angle-b; Wang Erniu's portrait only in the wide. The street, road and barn "
              "prompts lose ' below the deep pool' (every later fix must too). The clean sentence's 'clear and still' replaced in "
              "every shot. Shoes per wide. Sets: see mkspec.py. No off-screen sentence (r2.py OFFSCREEN_SPEECH = False). Seeds "
              "9391101/9391102."),
    "seeds": [9391101, 9391102],
    "shots": shots,
}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
