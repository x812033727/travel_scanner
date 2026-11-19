"""Writes spec.json next to this file: e933 live d1 (e932-live/spec.json's way, with e931-live's Tang Xiaotang back shot and the
e032 live lessons; writer-tools/e033-r2/r2.py's FOOT and PLACES).
Run: python3 -I mkspec.py

- Tang Xiaotang (bible rule 40): her one shot s17 is from behind: her three pictures and her identity sentence leave (the
  sentence also names the abacus at her waist, rule 20); the 'only' sentence says she is seen from behind and appears once. s19
  her back at the frame edge is not a listed character (no picture), named in the 'only' sentence as the young woman seen from
  behind. No front face this episode.
- Xu Yan's smirking angle-b nowhere (e921 review). The wides s01, s28 send his portrait only. Where gen-dh sent only angle-a and
  angle-b (the close-ups s02, s08, s30, s35) his portrait goes first and angle-a second (e930's XU_TWO).
- Wang Erniu: where gen-dh sends erniu-angle-a with no portrait (the close-up s14) it becomes his portrait (e931 s25, e932 s03).
  The wides s05, s24 his portrait only. Qin Shuang her portrait only (refs-dh has no angle crop of her). Elder Han, Carpenter
  Shi, little Xiaohe: their portraits only (gen-dh sends no angle picture of them). Qian Yuanwai never angle-b (e931); the wides
  s19, s39 his portrait only.
- Elder Han kneels without his staff (s01, s04; r2.py HAN_NOSTAFF, the staff leaning on the altar table): his cast sentence loses
  "leaning on a polished old bamboo walking staff" there.
- No person sent: s20 (the geomancer, a minor role with no portrait, bible 〈小角色〉), s27 (the insert of the pinwheel), s34 (the
  wheel). The set clause opens the sentence. The insert s27 loses the pool's place sentence (bible rule 35, e932 s16/s25b):
  "Initial composition: <D0>; <SUN>: insert close-up" becomes "Initial composition: Insert close-up"; its one picture (H3's
  reference mode needs 1-9) is the free sky crop set-shentan-gongdi-tian-l1, written as the colour of the sky only, never the
  place: the set clause becomes "The pale sky shown in <Picture 1> gives only the colour of the background." and the standard
  insert sentence becomes "Throughout the shot the framing stays as it is. The picture gives the colour of the sky only, never
  the mood." (the separator "never the mood. " stays once).
- 'Only' sentences: where the composition already says "... is the only person in the frame", the appended one is cut down to
  its second half (e927 review 建議). Where the composition describes unnamed people the 'only' sentence names them so they are
  allowed in the frame and not counted out: the kneeling villagers (s01), the over-the-shoulder backs (s09, s10), the young woman
  from behind and the geomancer (s17, s19), the geomancer's cut-off sleeve (s21, s25). s05, s06, s07, s12, s22, s24, s39 keep
  ref2manifest's "Besides ..., only the other people the composition names" sentence (crowds the composition counts).
- Wides with Qin Shuang (s12, s31): extras_patch's shoes sentence would take her leather boots away; it names her boots there.
- The speaking gaze never names an unsent listener (e927 必改 5, bible rule 31): r2.py's GAZE_REFINE (the same words in d1 and in
  the refine text).
- Every motion that opens a sentence after "never the mood. " is capitalised (e928 review 必改 1's fix); s20, s27, s34 (no person)
  open with r2.py's NOBODY sentence, so the separator is there once.
- Sets (r2.py PLACES): the hall at dusk set-citang-huang (s01), -huang-zuo2 (s02), -huang-liang (s03), -huang-zuo (s04); at night
  the free set-citang-ye2 (s05), -ye2-men (s06, s08, s10), -ye2-tang (s09), and the plain wall -huang-qiang (s07, s11); the deep
  pool on the fourth day set-shentan-gongdi (s12), -gongdi-an (s14, s16, s22, s24, s26), -gongdi-mu (s13, s17, s18), -gongdi-tian
  (s15, s23, s27), -gongdi-geng (s19, s20, s21, s25); the tenth dawn -chen (s28), -chen-an (s29), -chen-lun (s30); noon
  set-shentan (s34, gen-dh's own pick, not swapped), -an (s31, s32, s33, s36, s37), -lun (s35, s38), -geng (s39), -tian (s40).
  gen-dh's/pilot.py's set-citang-l1 is never sent, nor set-citang-ye-l1 (the beam still has its crack strokes). Every swap is
  sent with an absolute path by prep933.sh.
- No seed of this episode has been run. Seeds 9331101/9331102.
"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROD = HERE.parents[2]
L = str(PROD / "assets" / "refs-live")
VIDEO = str(PROD.parents[2] / "zhong-tian-qu-qi-e033-r2" / "video.json")
_spec = importlib.util.spec_from_file_location("r2_933_mkspec", PROD / "writer-tools" / "e033-r2" / "r2.py")
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
ONE_TANG = "the young woman with the two high round buns appears only once"
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
SKY_CLAUSE = "The pale sky shown in <Picture 1> gives only the colour of the background."
NOBODY_OLD = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
NOBODY_SKY = "Throughout the shot the framing stays as it is. The picture gives the colour of the sky only, never the mood. "
SHOES = "Every person in the frame wears dark cloth shoes on both feet."
SHOES_QIN = "Qin Shuang wears her leather boots and every other person in the frame dark cloth shoes on both feet."
STAFF = ", leaning on a polished old bamboo walking staff"
CT = "set-citang-l1.png"     # pilot.py's newest set-citang for gen-dh's dh-set-citang-t1
ST = "set-shentan-l1.png"    # pilot.py's newest set-shentan for dh-set-shentan-t1
INSERTS = ["s27"]
NOPERSON = ["s20", "s27", "s34"]


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


video = json.load(open(VIDEO, encoding="utf-8"))
scenes = {sc["id"]: sc for sc in video["scenes"]}
ids = [sc["id"] for sc in video["scenes"]]
assert len(ids) == 40, len(ids)
shots = {sid: {} for sid in ids}

# Tang Xiaotang from behind (s17): her identity sentence and her three pictures leave.
add("s17", [TANG_ID, ""])
add("s17", [ONLY_2, f"Only these 2 people are in the frame, the young woman with the buns seen only from behind and Carpenter Shi one "
                    f"step beyond her in the right third of the frame; {ONE_TANG}; no second copy of anyone appears."])
drop("s17", *TANG_PICS)

# No person sent: the set clause opens the sentence; the insert s27 is the colour of the sky only, no place sentence (rule 35).
for sid in NOPERSON:
    add(sid, [SET_CLAUSE, SKY_CLAUSE if sid in INSERTS else "T" + SET_CLAUSE[1:]])
add("s27", [f"Initial composition: {R2.LOC['gd_e']}: insert close-up", "Initial composition: Insert close-up"])
add("s27", [NOBODY_OLD, NOBODY_SKY])

# The unnamed the compositions describe are named in the 'only' sentence.
add("s01", [ONLY_2, "Only Xu Yan, Elder Han and the eight kneeling people the composition describes, each in a different colour, are in "
                    "the frame; no second copy of anyone appears."])
for sid, edge in (("s09", "left"), ("s10", "right")):
    add(sid, [ONLY_HE, f"Besides him, only the one man seen from behind at the {edge} edge of the frame the composition describes is in "
                       f"the frame; no second copy of anyone appears."])
add("s19", [ONLY_HE, f"Only Qian Yuanwai, the tall thin man in the yellow robe behind him and the young woman seen only from behind at the "
                     f"lower left edge of the frame are in the frame; {ONE_TANG}; no second copy of anyone appears."])
for sid, edge in (("s21", "right"), ("s25", "left")):
    add(sid, [ONLY_HE, f"Besides him, only the tall thin man cut by the {edge} edge of the frame the composition describes is in the frame; "
                       "no second copy of anyone appears."])
SPECIAL_ONLY = {"s01", "s09", "s10", "s17", "s19", "s21", "s25"}
BESIDES = {"s05", "s06", "s07", "s12", "s22", "s24", "s39"}
for sid in ids:
    sc = scenes[sid]
    if sid in SPECIAL_ONLY or sid in BESIDES or len(sc["data"]["characters"]) != 1:
        continue
    if "is the only person in the frame" in sc["data"]["prompt"]:
        add(sid, [ONLY_SHE if sc["data"]["characters"][0] in ("qinshuang", "xiaohe", "tangxiaotang") else ONLY_HE, NO_COPY])

# The wides with Qin Shuang: her boots.
for sid in ("s12", "s31"):
    add(sid, [SHOES, SHOES_QIN])
# Elder Han kneels without his staff (s01, s04).
for sid in ("s01", "s04"):
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
XU_ALL = ["s01", "s03", "s04", "s07", "s10", "s16", "s28", "s29", "s32"]
XU_TWO = ["s02", "s08", "s30", "s35"]  # gen-dh sent angle-a and angle-b only (the close-ups)
XU_WIDE = ["s01", "s28"]
for sid in XU_ALL:
    drop(sid, "xuyan-angle-b-l1.png")
for sid in XU_WIDE:
    drop(sid, "xuyan-angle-a-l1.png")
for sid in ["s05", "s24"]:
    drop(sid, "erniu-angle-a-l1.png")
for sid in ["s19", "s21", "s25", "s39", "s40"]:
    drop(sid, "qianyuanwai-angle-b-l1.png")
for sid in ["s19", "s39"]:
    drop(sid, "qianyuanwai-angle-a-l1.png")

SWAP = {sid: {} for sid in ids}
PLACE = {
    CT: {"set-citang-huang-l1.png": ["s01"], "set-citang-huang-zuo2-l1.png": ["s02"], "set-citang-huang-liang-l1.png": ["s03"],
         "set-citang-huang-zuo-l1.png": ["s04"], "set-citang-ye2-l1.png": ["s05"], "set-citang-ye2-men-l1.png": ["s06", "s08", "s10"],
         "set-citang-ye2-tang-l1.png": ["s09"], "set-citang-huang-qiang-l1.png": ["s07", "s11"]},
    ST: {"set-shentan-gongdi-l1.png": ["s12"], "set-shentan-gongdi-an-l1.png": ["s14", "s16", "s22", "s24", "s26"],
         "set-shentan-gongdi-mu-l1.png": ["s13", "s17", "s18"], "set-shentan-gongdi-tian-l1.png": ["s15", "s23", "s27"],
         "set-shentan-gongdi-geng-l1.png": ["s19", "s20", "s21", "s25"],
         "set-shentan-chen-l1.png": ["s28"], "set-shentan-chen-an-l1.png": ["s29"], "set-shentan-chen-lun-l1.png": ["s30"],
         "set-shentan-l1.png": ["s34"], "set-shentan-an-l1.png": ["s31", "s32", "s33", "s36", "s37"],
         "set-shentan-lun-l1.png": ["s35", "s38"], "set-shentan-geng-l1.png": ["s39"], "set-shentan-tian-l1.png": ["s40"]},
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
SWAP["s14"]["erniu-angle-a-l1.png"] = "erniu-portrait-l1.png"
for sid, sw in SWAP.items():
    if sw:
        shots[sid]["swap_pictures"] = sw
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e933 live d1 (e932-live's way, with e931-live's Tang Xiaotang back shot; written by mkspec.py). Tang Xiaotang s17 from "
              "behind (her pictures and identity sentence dropped); no front face. No person sent in s20 (the geomancer, no portrait), "
              "s27 (the pinwheel insert: no place sentence, one sky crop written as the colour of the sky only) and s34 (the wheel). "
              "Xu Yan's angle-b nowhere; the wides s01, s28 his portrait only; s02, s08, s30, s35 his portrait then angle-a. Wang "
              "Erniu's close-up s14 his portrait; the wides s05, s24 his portrait only. Qian Yuanwai never angle-b; the wides s19, s39 "
              "his portrait only. Sets: see mkspec.py (the hall at dusk -huang, at night the free -ye2; the pool -gongdi on the fourth "
              "day, the free dawn -chen and the noon crops on the tenth). No off-screen sentence (r2.py OFFSCREEN_SPEECH = False). "
              "Seeds 9331101/9331102."),
    "seeds": [9331101, 9331102],
    "shots": shots,
}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
