"""Writes spec.json next to this file: e932 live d1 (e931-live/spec.json's way, with e032's own independent review applied:
writer-tools/e032-r2/review.md, the 6 必改 and the 建议 the coordinator took; r2.py's FOOT and PLACES).
Run: python3 -I mkspec.py

- No Tang Xiaotang, no A-ling in this episode: none of e931's back-shot rewriting is needed.
- Xu Yan's smirking angle-b nowhere (e921 review). The wides s10, s11, s36 send his portrait only. Where gen-dh sent only angle-a
  and angle-b (the upside-down close-ups s26, s26b) his portrait goes first and angle-a second (e930's XU_TWO).
- Wang Erniu: where gen-dh sends erniu-angle-a with no portrait (the close-ups s03, s06, s18) it becomes his portrait (e931 s25,
  s39). The wides s10, s20, s23, s25 his portrait only (r2.py FOOT names s10, s23; s20 and s25 are wides of small full figures
  too). Qin Shuang: gen-dh sends only her portrait in every shot (refs-dh has no angle crop of her), so every shot of hers sends
  qinshuang-portrait-l1 only; r2.py FOOT is corrected to say so. Elder Han and Carpenter Shi: their portraits only.
- The inserts s16 (the hands and the pick at the bottom of the shaft, review 必改 2) and s25b (the hanging hand, review 建議):
  r2.py wants no picture at all, but the H3 reference mode takes 1-9 pictures (check_manifest.py: "reference_images must list
  1-9 images"; h3r.sh check and preflight refuse an empty list). So each sends ONE neutral picture (coordinator, 2026-11-18):
  s25b the free close crop of the dry earth set-jingkeng-di-l1, s16 the free set-jingkeng-jingdi-l1 (jingkeng_jingdi.py: only
  -di's soil colour, damp and dark, seeded grain, a narrow warm orange gradient along the top edge; no furrows, no pit mouth, no
  bricks, nobody: the review's danger in s16 was -kou's brick pit seen from above, which grows "a head out of the ground", and
  -di's bright orange furrows would grow a lit field), and the sentence that would make it the place is rewritten: the set clause
  becomes "The dry earth shown in <Picture 1> gives only the colour and grain of the soil." and the standard insert sentence
  "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood." becomes
  "Throughout the shot the framing stays as it is. The picture gives the colour of the earth only, never the mood." (the
  separator "never the mood. " stays once). Both lose d1's place sentence (bible rule 35, e931 s18/s21): "Initial composition:
  <J1>, ...; <JE>: " becomes "Initial composition: " and the composition opens on the camera or on the light. prep932.sh scans
  both for "well pit", "field", "village" (and the other place words).
- No person sent in s32 (the beam): the set clause opens the sentence.
- 'Only' sentences: where the composition already says "... is the only person in the frame", the appended one is cut down to
  its second half (e927 review 建議). Where the composition describes unnamed people (the over-the-shoulder backs s05, s08, s13,
  s15, s28, s29; the man over Qin Shuang's shoulder s23-s26b; the villagers s10, s11, s20, s22, s33, s34) the 'only' sentence
  names them so they are allowed in the frame and not counted out. s01, s32, s36 keep ref2manifest's "Besides ..., only the other
  people the composition names" sentence.
- Wides with Qin Shuang (s01, s10, s20, s23, s25): extras_patch's shoes sentence ("Every person in the frame wears dark cloth shoes
  on both feet.") would take her leather boots away; it names her boots there.
- Elder Han kneels without his staff in s34-s36 (r2.py HAN_NOSTAFF): his cast sentence loses "leaning on a polished old bamboo
  walking staff" there.
- The speaking gaze never names an unsent listener (e927 必改 5, bible rule 31): r2.py's GAZE_REFINE (the same words in d1 and in
  the refine text).
- Every motion that opens a sentence after "never the mood. " is capitalised (e928 review 必改 1's fix).
- Sets (r2.py PLACES): the flipped dam set-shangyou-ba-fx (s01) and its crops -fx-lu (s02, s04, s07, s08, s10), -fx-shan (s03,
  s06), -fx-jiao (s05), -fx-ding (s09); the pits at dawn set-jingkeng-chen (s11), -kou-chen (s12, s14, s15), -dui-chen (s13); at
  dusk set-jingkeng (s20, gen-dh's own pick, not swapped), -kou (s17, s18, s19, s22), -dui (s23, s25), -tian (s24, s26, s26b),
  -di (s21; and the insert s25b), -jingdi (the insert s16); the hall at dusk set-citang-huang (s36), -huang-men (s27, s28, s30, s31, s37),
  -huang-qiang (s29), -huang-liang (s32), -huang-tang (s33), -huang-zuo (s34), -huang-zuo2 (s35). gen-dh's/pilot.py's
  set-liuxi-he-l1 and set-citang-l1 are never sent; set-citang-huang-zhuo-l1 is not sent (review 必改 6). Every swap is sent with
  an absolute path by prep932.sh.
- No seed of this episode has been run. Seeds 9321101/9321102.
"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROD = HERE.parents[2]
L = str(PROD / "assets" / "refs-live")
VIDEO = str(PROD.parents[2] / "zhong-tian-qu-qi-e032-r2" / "video.json")
_spec = importlib.util.spec_from_file_location("r2_932_mkspec", PROD / "writer-tools" / "e032-r2" / "r2.py")
R2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R2)

ONLY_HE = "He is the only person in the frame; no second copy of anyone appears."
ONLY_SHE = "She is the only person in the frame; no second copy of anyone appears."
ONLY_2 = "Only these 2 people are in the frame; no second copy of anyone appears."
ONLY_3 = "Only these 3 people are in the frame; no second copy of anyone appears."
NO_COPY = "No second copy of anyone appears."
SET_CLAUSE = "the location shown in <Picture 1> is the set, keeping its layout and props."
SOIL_CLAUSE = "The dry earth shown in <Picture 1> gives only the colour and grain of the soil."
NOBODY_OLD = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
NOBODY_SOIL = "Throughout the shot the framing stays as it is. The picture gives the colour of the earth only, never the mood. "
SHOES = "Every person in the frame wears dark cloth shoes on both feet."
SHOES_QIN = "Qin Shuang wears her leather boots and every other person in the frame dark cloth shoes on both feet."
STAFF = ", leaning on a polished old bamboo walking staff"
LX = "set-liuxi-he-l1.png"   # pilot.py's newest set-liuxi-he for gen-dh's dh-set-liuxi-he-t1
JK = "set-jingkeng-l1.png"   # pilot.py's newest set-jingkeng for dh-set-jingkeng-t1
CT = "set-citang-l1.png"     # pilot.py's newest set-citang for dh-set-citang-t1
INSERTS = ["s16", "s25b"]


def add(sid, pair):
    shots[sid].setdefault("replace", []).append(pair)


def drop(sid, *names):
    shots[sid]["drop_pictures"] = shots[sid].get("drop_pictures", []) + [n for n in names if n not in shots[sid].get("drop_pictures", [])]


video = json.load(open(VIDEO, encoding="utf-8"))
scenes = {sc["id"]: sc for sc in video["scenes"]}
ids = [sc["id"] for sc in video["scenes"]]
assert len(ids) == 39, len(ids)
shots = {sid: {} for sid in ids}

# The inserts: no place sentence (rule 35), the one neutral picture is the colour of the soil only, never the place.
LOC_EC = R2.LOC["jk_ec"]
LOC_ET = R2.LOC["jk_et"]
add("s16", [f"Initial composition: {LOC_EC}: high-angle close shot", "Initial composition: High-angle close shot"])
add("s25b", [f"Initial composition: {LOC_ET}: low orange evening light", "Initial composition: Low orange evening light"])
for sid in INSERTS:
    add(sid, [SET_CLAUSE, SOIL_CLAUSE.replace("dry earth", "damp earth") if sid == "s16" else SOIL_CLAUSE])
    add(sid, [NOBODY_OLD, NOBODY_SOIL])
# No person sent (s32): the set clause opens the sentence.
add("s32", [SET_CLAUSE, "T" + SET_CLAUSE[1:]])

# The unnamed the compositions describe are named in the 'only' sentence.
for sid, edge, who in (("s05", "right", "man"), ("s15", "right", "man"), ("s28", "right", "man"),
                       ("s08", "left", "man"), ("s13", "left", "man"), ("s29", "left", "man")):
    old = ONLY_SHE if sid == "s08" else ONLY_HE
    pr = "her" if sid == "s08" else "him"
    add(sid, [old, f"Besides {pr}, only the one {who} seen from behind at the {edge} edge of the frame the composition describes is in "
                   f"the frame; no second copy of anyone appears."])
add("s10", [ONLY_3, "Only Qin Shuang, Xu Yan, Wang Erniu and the five other people the composition describes, each in a different "
                    "colour, are in the frame; no second copy of anyone appears."])
add("s11", [ONLY_2, "Only Elder Han, Xu Yan and the five other people the composition describes, each in a different colour, are in "
                    "the frame; no second copy of anyone appears."])
add("s20", [ONLY_2, "Only Wang Erniu, Qin Shuang and the two other men the composition describes are in the frame; no second copy of "
                    "anyone appears."])
add("s22", [ONLY_3, "Only Qin Shuang, Xu Yan, Wang Erniu and the one man in a dull olive-green jacket the composition describes are in "
                    "the frame; no second copy of anyone appears."])
for sid in ("s23", "s25"):
    add(sid, [ONLY_2, "Only Qin Shuang, Wang Erniu and the limp man over her shoulder, seen only from behind, are in the frame; no "
                      "second copy of anyone appears."])
add("s24", [ONLY_SHE, "Besides her, only the limp man over her shoulder the composition describes, his face not seen, is in the frame; "
                      "no second copy of anyone appears."])
for sid in ("s26", "s26b"):
    add(sid, [ONLY_HE, "Besides him, only the dark brown jacket back of the one who carries him is in the frame; no second copy of "
                       "anyone appears."])
add("s33", [ONLY_HE, "Besides him, only the eight kneeling people the composition describes, each in a different colour, are in the "
                     "frame; no second copy of anyone appears."])
add("s34", [ONLY_HE, "Besides him, only the two kneeling people the composition describes are in the frame; no second copy of anyone "
                     "appears."])
SPECIAL_ONLY = {"s05", "s08", "s13", "s15", "s28", "s29", "s10", "s11", "s20", "s22", "s23", "s24", "s25", "s26", "s26b", "s33", "s34"}
BESIDES = {"s01", "s32", "s36"}  # ref2manifest's crowd test already wrote "Besides her/them, only the other people ..."
for sid in ids:
    sc = scenes[sid]
    if sid in SPECIAL_ONLY or sid in BESIDES or len(sc["data"]["characters"]) != 1:
        continue
    if "is the only person in the frame" in sc["data"]["prompt"]:
        add(sid, [ONLY_SHE if sc["data"]["characters"][0] == "qinshuang" else ONLY_HE, NO_COPY])

# The wides with Qin Shuang: her boots.
for sid in ("s01", "s10", "s20", "s23", "s25"):
    add(sid, [SHOES, SHOES_QIN])
# Elder Han kneels without his staff (s34-s36).
for sid in ("s34", "s35", "s36"):
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
XU_ALL = ["s04", "s05", "s07", "s09", "s10", "s11", "s12", "s14", "s15", "s21", "s22", "s27", "s28", "s31", "s36", "s37"]
XU_TWO = ["s26", "s26b"]  # gen-dh sent angle-a and angle-b only (the close-ups)
XU_WIDE = ["s10", "s11", "s36"]
for sid in XU_ALL:
    drop(sid, "xuyan-angle-b-l1.png")
for sid in XU_WIDE:
    drop(sid, "xuyan-angle-a-l1.png")
ER_WIDE = ["s10", "s20", "s23", "s25"]
for sid in ER_WIDE:
    drop(sid, "erniu-angle-a-l1.png")

SWAP = {sid: {} for sid in ids}
PLACE = {
    LX: {"set-shangyou-ba-fx-l1.png": ["s01"], "set-shangyou-ba-fx-lu-l1.png": ["s02", "s04", "s07", "s08", "s10"],
         "set-shangyou-ba-fx-shan-l1.png": ["s03", "s06"], "set-shangyou-ba-fx-jiao-l1.png": ["s05"],
         "set-shangyou-ba-fx-ding-l1.png": ["s09"]},
    JK: {"set-jingkeng-chen-l1.png": ["s11"], "set-jingkeng-kou-chen-l1.png": ["s12", "s14", "s15"],
         "set-jingkeng-dui-chen-l1.png": ["s13"], "set-jingkeng-l1.png": ["s20"],
         "set-jingkeng-kou-l1.png": ["s17", "s18", "s19", "s22"], "set-jingkeng-dui-l1.png": ["s23", "s25"],
         "set-jingkeng-tian-l1.png": ["s24", "s26", "s26b"], "set-jingkeng-di-l1.png": ["s21", "s25b"], "set-jingkeng-jingdi-l1.png": ["s16"]},
    CT: {"set-citang-huang-l1.png": ["s36"], "set-citang-huang-men-l1.png": ["s27", "s28", "s30", "s31", "s37"],
         "set-citang-huang-qiang-l1.png": ["s29"], "set-citang-huang-liang-l1.png": ["s32"],
         "set-citang-huang-tang-l1.png": ["s33"], "set-citang-huang-zuo-l1.png": ["s34"],
         "set-citang-huang-zuo2-l1.png": ["s35"]},
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
for sid in ["s03", "s06", "s18"]:
    SWAP[sid]["erniu-angle-a-l1.png"] = "erniu-portrait-l1.png"
for sid, sw in SWAP.items():
    if sw:
        shots[sid]["swap_pictures"] = sw
for v in shots.values():
    for k in v.get("swap_pictures", {}).values():
        assert (Path(L) / k).is_file(), k

spec = {
    "_note": ("e932 live d1 (e931-live's way, with e032's independent review applied; written by mkspec.py). No Tang Xiaotang or "
              "A-ling. The inserts s16, s25b have no place sentence and send one neutral picture only (s16 the damp dark "
              "set-jingkeng-jingdi-l1, s25b the dry-earth crop set-jingkeng-di-l1), written as the colour of the soil, never the place (H3's reference mode needs 1-9 pictures; "
              "r2.py's 'no picture' cannot be sent). No person sent in s32. Xu Yan's angle-b nowhere; the wides s10, s11, s36 his "
              "portrait only; s26, s26b his portrait then angle-a. Wang Erniu's close-ups s03, s06, s18 his portrait; the wides "
              "s10, s20, s23, s25 his portrait only. Qin Shuang her portrait only (no angle crop exists in refs-dh). Sets: see "
              "mkspec.py (dawn -chen pictures s11-s15, the golden set-jingkeng family s17-s26b, the hall at dusk -huang). No "
              "off-screen sentence (r2.py OFFSCREEN_SPEECH = False). Seeds 9321101/9321102."),
    "seeds": [9321101, 9321102],
    "shots": shots,
}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(sum(1 for v in shots.values() if v), "shots edited of", len(shots))
