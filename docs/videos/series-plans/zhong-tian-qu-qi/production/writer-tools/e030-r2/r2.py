"""Episode 30 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e030-r2/script.md
(c01-c41 = s01-s41; the CG-era r2 script), including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and
「真人版的改動（2026-11-17）」, which override the tables. Every line is the script's, word for word; only the staging changes.
Bible: production/r2-bible-e021-e030.md (rules 1-30, the 29->30 and 30->31 hand-overs, the props, people and picture tables) and
r2-bible-e011-e060.md (the 30->31 hand-over into arc 4: e031 opens on the same moment at the well, then the same persimmon tree
three months on). The tenth and LAST episode of arc 3 〈搶親〉: the town square in the afternoon of the thirtieth day of the
contest (the same moment as e029 s35), then the Xu yard at the end of the same day, the sun low.

Written from the start the way e029-r2/r2.py stands AFTER its independent review (../e029-r2/review.md: the 8 必改 and the
建議 the coordinator took), with what the pickers caught in e924-e928 and the lessons in the task file:
- OFFSCREEN_SPEECH = False (rule 15): every shot with an off-screen line, a thought or a system line writes the silence of each
  person on screen (quiet(), SILENT_HE); no word that invites a smile on a listener unless the script lets him smile.
- A line said to someone outside the frame is written "toward someone out of sight beyond the left/right edge of the frame",
  that side is set only (earth, plank doors, wall, field, firewood, sky) all the way to the edge, and the speaker is the only
  person in the frame. No person who is not in the first frame is named or described anywhere, in the prompts or in the refine
  text (e925 lesson; e927 必改 5; e928 必改 3; e029 必改 4). A look at a place names the place ("the yard gate beyond the left
  edge", "the well beyond the right edge", "the carriage at the right edge").
- Tang Xiaotang never speaks on camera and never shows her face (rule 3; e024-e029): her five lines on screen (s02, s08, s14, s28,
  s33) and her affection shot (s20, the system's line) are from behind, in the middle of the frame, "facing straight away from
  us", head still, exactly two round buns (TBACK; nospeak; spec drops her pictures and identity sentence). In the last wide (s41)
  she is small, from behind, beside Xu Yan. The script's 高立領, 「下巴以上」 and 「襦裙從立領到腰一件闔上」 are CG wording and are
  not used (rule 4). Her abacus is not shot (rule 20: only in inserts; c33's two beads are the sound effect 「喀」).
- Wei Shaoqing (rule 30): the fan is always closed (FAN); c05's 「摺扇打開」, c10's 「打開的摺扇掩在鼻子下」, c23's 「啪地收扇」 are
  not shot. Rule 30 marks e030's 撤婚 and 認出阿令 as losing shots: s26, s30, s34, s37, s40 are NOSMILE; the script's own smiles
  (c05 「本鏡可以笑」, c10 嫌棄的笑, c15 冷笑, c23 笑得很僵) are kept.
- Tang Wanjin (tangwanjin-portrait-l1): crying in scene 1, never laughing when he names the salt boats and the pledge (原版必修:
  s25-s29 NOSMILE); his gold keys written as the bible says; c35 「本鏡可以笑」 kept. Steward Zheng (zhengbo-portrait-l1, tall and
  thin): the bible's two-shot whisper (s24: 「鄭伯畫成高瘦後可以跟唐萬金同鏡」), his right hand raised beside his mouth hiding his
  lips (nospeak; the recording plays), his little brush never written (rule 7). Never with Magistrate Hu (not in this episode).
- A-ling (rule 21): the veil from s09 on, with aling-veil-portrait-l1 in place of her portrait and no angle pictures (spec); s38,
  s39 and s41 send her bare portrait: the veil already blown to her left ear from the first frame ("the veil hangs from her left
  ear only, blown out to her left side, her whole face bare"); the lift of the veil is the cut s37 -> s38. In s37 she is the
  unnamed back in the right foreground (rule 2), veil cords behind her ears, no picture.
- Name only what should be drawn (rules 7, 17, 27, 28): the ledger STACK (its pages blank; c17's 格線與小紅圈 not drawn), the
  marriage document DOC (rule 27: folded cream paper with a thin gold edge, only its plain back; torn: HALVES), the chipped bowl
  BOWL, the seed pouch SEEDS, the bucket BUCKET, one chestnut-red horse HORSE (rule 26). No word "open" anywhere; no hung thing
  named; the yard picture's hanging leaves, its blank wall board and the red mark on the door lintel are painted out (below).
- The low wooden table and bench under the tree (c12, c13, c17, c18, c24) are not on the yard picture and are not drawn: Tang
  Wanjin stands throughout, the ledger in his hands (c17 the insert of his hands, the earth far below, as e029 s15 after its
  review), the bowl in his hands (s12) and out of the frame after (s13). e031's 「唐萬金在樹後的矮木桌邊（被樹幹擋住）」 is off
  screen anyway. The chickens of c07 are a sound.
- One visible action per shot, props and contacts in the first frame; the script's follows, pans and the 越軸 walks are slow
  push-ins (c25: he is already before Wei Shaoqing; c29: already before his daughter; c31: the document already in his hands).
- No blue light (rule 11): the panels of s20, s21 are the editor's.

AFTER THE INDEPENDENT REVIEW (review.md in this folder: the 5 必改 all applied as written, the cheap 建議 the coordinator took;
2026-11-17, the coordinator deciding for the owner; where this differs from the paragraphs above and below, this wins):
- s38, s39, s41 (必改 1): the veil is the thing itself, VEIL_BLOWN "a long strip of soft, half-transparent pale grey gauze hangs
  from a thin grey tie looped over her left ear only, its free end blown out past her left cheek and shoulder in the wind, her
  nose, mouth and chin bare from the first frame" (her bare portrait has no veil; she faces screen left, so the left ear is the
  one toward us); s38 and s41's motion "the loose strip of pale grey gauze" (VEIL_LOOSE).
- s38 (必改 2): a medium shot from the waist up, "the round stone rim of the well along the bottom of the frame", her hand on the
  bucket's rope handle "standing on the rim from the first frame"; cam "Medium shot, slow push in". s09 the same (建議 7), and its
  veil "falling down to the middle of her chest" (VEIL; mkspec.py's cast sentence too; "hanging" would trip the hung-object scan).
- s17, s22, s32 (必改 3): no place sentence in d1. LOC["yard_e"] is only Y0 now, kept in video.json so that gen-dh's SET
  ("courtyard") still sends the yard picture that spec.json swaps for -di-l1; mkspec.py strips "Y0: " from each of the three
  d1 prompts, which then open on INSERT_LIGHT and "insert close-up seen from (slightly) above, looking down", and the background
  is "only packed yellow earth ... to every edge" (no person, no setting word). s32 "a hand's width above packed yellow earth; the
  earth fills the frame to every edge".
- s37 (必改 4): the woman at the well is only "the back of one grey-white cotton shoulder and the back of a high black bun with one
  plain wooden hairpin, turned fully away from us toward the yard gate, the back of her head toward us the whole shot", cut by
  the right edge; no ear, no veil tie. Wei "the back of his head toward us".
- s41 (必改 5): "facing the yard gate: on the left Xu Yan, ..., and on his right one young woman seen only from behind, ..."; A-ling
  "her body turned toward the yard gate, her face in left profile, her eyes on the gate"; the yard layout cut to one sentence
  (LOC["yard_k"]: "the farmhouse on the left, the yard gate in the middle of the back wall, the well in the front right").
- 建議 taken: the orange balls on the thatch painted out (1): set-xujia-yuan-dong-qing2-l1 and its crops -men2-l1, -wu2-l1 replace
  -qing-l1, -men-l1, -wu-l1 (refs-live/README.md; the orange flowers in the field beyond the gate stay: flowers, low in the
  frame); s20 from the waist up, her hands clasped behind her back, the fingers twisting once (2); s24 Steward Zheng at the left
  of the frame, his cupped hand between his mouth and Tang Wanjin's ear, Tang Wanjin "mild and at ease" (3); s25 the ledger in his
  left hand, tucked up under his left arm (4); s08 the ledger in her right arm, her left hand to Qin Shuang (5); s31 the closed
  fan down at Wei's side (6); s06 CARRIAGE_DOOR (8); s27 "his flat right hand, fingers together and palm down" (9; "open" is
  banned); the refine text's generic speaking gaze replaced by d1's (10): GAZE_REFINE in live_clips(), put back by anchor_form()
  so stage 1 reads gen-dh's wording. Not taken: the optional -qiang-shu crop for Tang Wanjin (15). BUY unchanged (11, 12).
- The horse (13): text only this episode. After the e930 picks, crop the cleanest head-and-neck frame of s36 as
  prop-zaohongma-head-l1; full-body horse pictures (chestnut for e038/e051/e053, Wei's white horse for e031) are a screen-test
  item for arc 4, the owner decides then (r2-bible-e021-e030.md, the remake task).
- Recordings: the clip voice stays primary; the cut uses a28-p79 for s28; backups a17-p75 (s18), a29-p84 (s29), a23-p126 (s23,
  from 1.20 s, after the 哈哈); a31 the original. Hear a28-p79, a23-p126, a29-p84 before refining.

THE AXES (rule 29: the set picture decides; set-xujia-yuan-dong-l1, painted clean as -dong-qing-l1):
- Scene 1, the square in the afternoon (e029 s32-s35): Tang Wanjin came from the carriage on the RIGHT and faces screen left;
  Xu Yan and Tang Xiaotang face screen right toward him; Wei Shaoqing stands to Tang Wanjin's right and looks screen left.
- Scenes 2-3, the yard (the picture: house and firewood on the LEFT, the gate in the middle of the back wall, the bare tree just
  right of it behind the wall, the low wall and leaning planks on the RIGHT, the well in the FRONT RIGHT; the low sun at the upper
  right, shadows to the lower left). Xu Yan and Tang Xiaotang stand left of the middle (before the house and the firewood); Tang
  Wanjin in the middle by the tree; Wei Shaoqing on the right by the low wall; A-ling at the well in the front right; Qin Shuang
  at the gate. So Tang Wanjin looks screen left to his daughter and Xu Yan and screen right to Wei; Xu Yan looks screen right;
  Wei looks screen left; at the end Wei, at the gate, looks screen right to the well and A-ling looks screen left to the gate.
  e031's first shot (the bible: the well in the front right, Wei at the gate) takes this over. The gate is in the MIDDLE of the
  back wall (the picture; the bible's "後牆中偏右" is corrected in its 30->31 hand-over).

PLACES (the coordinator's decisions, 2026-11-17; every picture looked at full size; script.md 〈真人版的改動〉): gen-dh's SET
phrase "town square" gives set-guangchang-l1 and "courtyard" gives set-xujia-yuan-l3 (pilot.py's newest); spec.json swaps them
for the pictures below with absolute paths.
- Scene 1, e029's afternoon crops: set-guangchang-pm-you-wu-l1 (the long building on the carriage side: s01-s04, s06) and
  -pm-shu-l1 (the bare tree and the sky: s05, low angle).
- Scenes 2-3: set-xujia-yuan-dong-qing-l1 = set-xujia-yuan-dong-l1 (arc 3's pick, the bare persimmon tree; never sent before)
  with three things painted out with Pillow (the blank dark board on the house wall right of the doorway, a small red mark on the
  door lintel, the two leaves hanging from the branches like tags: hung things grow characters), and five free crops of it:
  -dong-men-l1 (the gate under its small tiled roof, the house corner and the tree: s07, s08, s10, s35, s36, s40), -dong-jing-l1
  (the well and the leaning planks: s09, s38, s39), -dong-wu-l1 (the house door, the window and the firewood: s11, s16, s19,
  s21), -dong-qiang-l1 (the low wall and the golden field: s12-s15, s18, s23-s29, s33, s34), -dong-shu-l1 (the bare branches
  against the glowing sky, the sun at the right: s30, low angle) and -dong-di-l1 (the earth and the evening shadows: the
  inserts s17, s22, s32). The wides s31, s37, s41 send -dong-qing-l1 itself. Commands in refs-live/README.md.
- Inserts and shots with nobody named (s17, s22, s32) open their motion with NOBODY.
- Shared files: none changed (build-r2.py's EN has every name: "A-ling", "Qin Shuang", "little Xiaohe", "Steward Zheng",
  "Tang Wanjin"); e910-e929 rebuild byte for byte. refs-live gets ten new free pictures (new ids, own l1; rule 19: the seven
  above and, after the review, -qing2-l1, -men2-l1, -wu2-l1) and README paragraphs. After the review the shots send -qing2-l1
  (s31, s37, s41), -men2-l1 (s07, s08, s10, s35, s36, s40) and -wu2-l1 (s11, s16, s19, s21, s21b) in place of -qing, -men, -wu.
"""
EP = 930  # internal working number; the published slug is zhong-tian-qu-qi-e030-r2
SLUG = "zhong-tian-qu-qi-e030-r2"
EP_TITLE = "這門親退了，井邊的面巾（重製版 r2）"
OUTLINE_SECONDS = 219  # script.md: about 218.5 s, 41 shots (6 + 30 + 5)
TARGET_MINUTES = [3, 4]
TITLE = "這門親退了，井邊的面巾｜種田娶妻打天下 第30集（重製版）"
DESCRIPTION = "唐萬金哭著追到廣場，停在一步外：囡囡，妳躲在一個窮秀才後頭做什麼？魏少卿叫他岳父，說許家的牆是泥糊的。傍晚，大車停在許家院門外，小禾端來一碗缺了角的井水，倒是真的甜。魏少卿亮出唐萬金親筆簽的婚書，許硯不爭，只請唐老爺先看一本帳——被人賠本壓價，三十天還贏人家兩倍？帳是小棠做的。鄭伯在他耳邊一句「京裡那筆鹽船的帳」，唐萬金的笑收得乾乾淨淨：八條鹽船，這張婚書就是抵押。他把婚書撕成兩半：八條船不要了，女兒要。魏少卿走到院門口，一陣風吹起井邊阿令的面巾——你……怎麼會在這裡？《種田娶妻打天下》第 30 集（重製版）。"
THUMB = ("婚書撕成兩半", "s31")
CHARACTERS = ["xuyan", "tangxiaotang", "tangwanjin", "weishaoqing", "zhengbo", "qinshuang", "xiaohe", "aling", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: warm uneasy strings on a town square in the afternoon, one pause when a father glares; then a warm homely cue in a farm yard at sunset turning bright and a little sweet, cut off at a whisper, low strings, one big accent when paper is torn, back to the warm cue; then only the wind, one faint high note when a veil lifts and one deep heavy accent at the end; ancient Chinese rural drama, no vocals"

# Places. gen-dh SET takes the FIRST pattern in its list order that the whole prompt matches: scene 1 says "town square", the
# yard says "courtyard" (never "kitchen", "lean-to", "stream", "night", "well pit", "back gate", "village").
PM = "warm golden low afternoon sun from the upper right behind, long shadows stretching far to the left across the earth"
Y0 = "In the courtyard of the Xu farmhouse at the end of the same cold clear early-winter day, the sun low in the west"
YARD = ("a courtyard of packed earth: on the left a low thatched mud-and-stone farmhouse with a dark doorway, a small lattice "
        "window and split firewood stacked against its wall; in the middle of the low mud-and-stone back wall a yard gate of "
        "weathered planks under a small tiled roof; one bare leafless tree just behind the wall at its right, a golden "
        "field beyond; one round stone well with a wooden windlass in the front right")
DUSK = "low golden evening sun from the upper right behind, long shadows stretching toward the lower left across the earth"
LOC = {
    "pm_r": f"In the town square of the county town in the afternoon of the same cold clear winter day, on the packed pale earth at the edge of the square before the long low tiled building with its plank doors; {PM}",
    "pm_c": "In the town square of the county town in the afternoon of the same cold clear winter day, the bare branches of a tree and the low tiled roofs against the clear sky, warm golden low afternoon sun from the right",
    "yard": f"{Y0}: {YARD}; {DUSK}",
    "yard_m": f"{Y0}, by the yard gate of weathered planks under its small tiled roof in the low mud-and-stone back wall, the corner of the thatched farmhouse at its left, the bare tree and the golden field beyond; {DUSK}",
    "yard_j": f"{Y0}, beside the round stone well with its wooden windlass in the front right of the yard, a few planks leaning against the low mud-and-stone wall behind it; {DUSK}",
    "yard_w": f"{Y0}, before the thatched mud-and-stone farmhouse on the left of the yard, its dark doorway, a small lattice window and split firewood stacked against its wall; {DUSK}",
    "yard_q": f"{Y0}, before the low mud-and-stone wall of the yard with the golden field beyond it, warm golden low evening sun from the right",
    "yard_s": f"{Y0}, the bare branches of a tree against the glowing evening sky, the low golden sun behind them at the right",
    "yard_e": Y0,  # review 必改 3: kept only so gen-dh's SET ("courtyard") sends the yard picture; spec.json strips it from d1
    "yard_k": f"{Y0}: the yard exactly as in the picture: the farmhouse on the left, the yard gate in the middle of the back wall, the well in the front right; {DUSK}",
}
LIGHT = {
    "pm": "the warm low afternoon sunlight stays unchanged",
    "dusk": "the low golden evening sunlight stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_D = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves down"
WEI = ("Wei Shaoqing, in his sapphire-blue brocade robe woven with gold thread, a white jade pendant at his waist, a small green "
       "jade ornament at the front of his topknot")
FAN = "one closed folding fan in his right hand, its dark bamboo ribs pressed tight together like a short slim stick"
ZHENG = ("Steward Zheng, tall and thin with a slight stoop, a long lined face, a neat grey-white goatee and a thin moustache, grey "
         "hair in a small topknot bound with a black cloth band, in his dark brown satin long robe")
TWJ = ("Tang Wanjin, a little plump, with a round ruddy face, a short black moustache and a short black goatee, a small gold crown "
       "on his topknot, in his deep purple silk robe woven all over with small gold ingot shapes, a string of small gold keys at "
       "his waist")
QIN = ("Qin Shuang, in her fitted dark brown cross-collared short jacket cinched with a wide plain black leather belt, black "
       "trousers and leather boots, her high ponytail tied with black cord")
XIAOHE = ("little Xiaohe, eight years old, in her patched lilac cotton jacket, two little pigtails tied with red string, a small "
          "woven straw rabbit tucked into the cloth sash at her waist")
ALING = ("A-ling, in her plain grey-white cotton dress with long sleeves covering her wrists, her black hair in a high bun with "
         "one plain wooden hairpin")
VEIL = ("a veil of soft, finely woven pale grey gauze over her nose, mouth and chin, tied behind both ears, falling down to the "
        "middle of her chest")  # review 建議 7: the veil portrait's veil reaches her chest
# review 必改 1: bible rule 21's "the veil hangs from her left ear only" named no thing (her bare portrait has no veil): the gauze
# itself, on its tie over her left ear (the ear toward the camera when she faces screen left)
VEIL_BLOWN = ("a long strip of soft, half-transparent pale grey gauze hangs from a thin grey tie looped over her left ear only, its "
              "free end blown out past her left cheek and shoulder in the wind, her nose, mouth and chin bare from the first frame")
VEIL_LOOSE = "the loose strip of pale grey gauze"
CARRIAGE = "the black lacquered carriage body and the head and neck of one horse at the right edge"
# review 建議 8 (s06): one "at the right edge", the door the carriage's
CARRIAGE_DOOR = ("the black lacquered carriage body with its door already swung back, and beyond it the head and neck of one "
                 "horse")
STACK = "one thick stack of plain blank paper sheets stitched along one edge with cord"
DOC = "one folded sheet of cream paper with a thin gold edge, plain, only its plain back showing"
HALVES = "two torn halves of one sheet of cream paper with a thin gold edge, only their plain backs showing"
BOWL = "one rough brown clay bowl with one small chip broken out of its rim, full of clear well water"
SEEDS = "one small plain cloth pouch, its neck loosened, full of plump golden rice grains"
BUCKET = "one round wooden bucket of well water with a rope handle"
HORSE = "one chestnut-red horse with a plain leather bridle"
HANDS = "their hands hold only what is described here"
# review 必改 3: the inserts' d1 composition opens on the light and the subject (spec.json strips LOC["yard_e"] before it)
INSERT_LIGHT = "warm golden low evening light from the right"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# e924 fix1's back-of-head wording, as e925-e929
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with every strand of her black hair "
         "combed smooth and gathered up into just two round buns set high on her head, one bun on each side, one short pink "
         "silk ribbon wrapped around each bun, the nape of her neck bare and clear above a pink inner collar, and her light "
         "peach-pink silk shoulders; the back of her head facing straight away from us the whole time, her head still, her ear "
         "the furthest round her head we ever see")
HEADSTILL = "the young woman with the two high round buns keeps her head still, facing straight away from us, the back of her head toward us the whole shot"
# set-only sides (the picture of each place, all the way to the edge)
SIDE_SQ = "the packed pale earth and the plank doors"
SIDE_WALL = "the low mud-and-stone wall and the golden field"
SIDE_HOUSE = "the mud-and-stone wall of the farmhouse and the split firewood"
SIDE_SKY = "the bare branches and the glowing evening sky"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def only_tang():
    return "she is the only young woman with two high round buns in the frame"


def alone(rest, where, frame="framed from the waist up", shot="medium shot", lead=""):
    """Tang Xiaotang from behind, in the middle of the frame (not at an edge: the pickers' cheek at the frame edge)."""
    return f"{shot} from close behind{lead} {TBACK}, {where} in the middle of the frame, {frame}, facing straight away from us; {only_tang()}; {rest}"


def off(side, what, he="he"):
    """A line to someone outside the frame: the gaze, that side set only, and the only person (e925, e927-e929 必改)."""
    edge = f"the {side} edge of the frame"
    return (f"toward someone out of sight beyond {edge}, never the lens; that side of the frame is only {what} all the way to the "
            f"edge, and {he} is the only person in the frame")


SHOTS = [
    # ---- scene 1: the thirtieth day of the contest, the afternoon, the edge of the town square (29->30: the same moment as e029 s35).
    dict(chapter="廣場邊，大車旁", loc="pm_r", cam="Medium shot, slow push in", chars=["tangwanjin"], night="pm",
         comp=f"medium shot on the packed pale earth at the edge of the square: {TWJ}, already stopped from the first frame, framed from the knees up, his arms still spread a little from his run, his face three-quarter to screen left {off('left', SIDE_SQ)}; tearful and out of breath, not smiling: wet red eyes, tears on his round cheeks, brows pulled up, chest heaving, lips moving between gasping words; behind him, soft, {CARRIAGE} and the long low tiled building in the warm afternoon sun",
         lines=[("tangwanjin", "囡囡，妳躲在一個窮秀才後頭做什麼？", "喘，帶哭腔")],
         motion="Tang Wanjin slowly lowers his spread arms to his sides as he speaks, still breathing hard",
         zh="中景、慢推（送午後調色的瓦屋裁切 `set-guangchang-pm-you-wu-l1`，同第 29 集 s32–s35）：唐萬金第一格已經停在一步外、兩手還張著一點，邊喘邊慢慢放下手、帶哭腔朝畫左外看不到的人說（那一側到邊緣只有黃土地與木板門、畫面裡只有他；不點名、不描述女兒與許硯）；身後虛焦是畫右緣的黑漆車廂與一匹馬的頭頸（拍法 26）。哭相、不笑。稿子『前景攤桌上的空糖箱、看看女兒再看看許硯』不拍（一鏡一個動作；接點 29→30：同一刻）"),
    dict(loc="pm_r", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="pm",
         comp=alone(f"{STACK} tucked under her left arm, her right hand already gripping the left sleeve of the young man before her from the first frame; one step beyond her in the right third of the frame, his upper body clear of her head and shoulders, {XU_D}, standing, framed from the waist up, his back three-quarter to us, facing screen right toward the far side of the square, his shoulders squared, his lips pressed shut; beyond them, soft, the long low tiled building and its plank doors in the warm afternoon sun; she stays in the middle of the frame the whole shot, her right arm reaching out to his left sleeve; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "standing on the packed pale earth,"),
         lines=[("tangxiaotang", "他不是窮秀才，他是我拜過堂的相公。", "小聲")],
         motion=f"her right hand pulls his left sleeve once toward her, only her arm moving; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送瓦屋裁切）：同第 29 集 s35 審稿後的構圖——唐小棠背影在畫面正中、頭不動，帳本夾在左臂下、右手抓著前面許硯的左袖；許硯在她前方一步、畫面右三分之一、上半身不跟她的頭與肩重疊、背對四分之三朝畫右、嘴閉著。她右手把他的袖子往自己這邊拉一下（只動手臂）（nospeak，拍法 3）。稿子『近景下巴以上、從許硯肩後探出臉、眼眶紅』改背影（她整集不露臉）"),
    dict(loc="pm_r", cam="Close-up, slow push in", chars=["tangwanjin"], night="pm",
         comp=f"close-up of {TWJ}, framed from the chest up with space above his head, his right sleeve already raised to his wet eyes from the first frame, his face three-quarter to screen left {off('left', SIDE_SQ)}; hurt turning hard, not smiling: red-rimmed eyes, brows pressed down, jaw set, lips moving hard between words; behind him, soft, {CARRIAGE} in the warm afternoon sun",
         lines=[("tangwanjin", "你就是那個窮秀才？憑什麼娶我女兒？", "瞪著許硯")],
         motion="Tang Wanjin drags his purple sleeve once across his eyes and lowers it, glaring, as he speaks",
         zh="近景、慢推（送瓦屋裁切）：唐萬金右袖第一格已經舉在眼邊，用紫袖抹一下眼淚、放下、瞪著朝畫左外看不到的人說（不點名許硯；那一側到邊緣只有黃土地與木板門）；不笑。稿子『抬起胖手指往許硯一戳』不拍（一鏡一個動作；單根手指會被讀成不雅的手勢）"),
    dict(loc="pm_r", cam="Medium close-up, slow push in", chars=["xuyan"], night="pm",
         comp=f"medium close-up of {XU_D}, standing on the packed pale earth, framed from the chest up with space above his head, his two hands already joined in a cupped salute before his chest from the first frame, his face three-quarter to screen right {off('right', SIDE_SQ)}; steady and level, polite but unbowed, not smiling: calm eyes, brows level, lips moving evenly between words; behind him, soft, the long low tiled building in the warm afternoon sun; {HANDS}",
         lines=[("xuyan", "晚輩許硯。窮是真的，婚書是縣衙蓋了印的。", "不卑不亢")],
         motion="Xu Yan gives one short bow over his joined hands and straightens as he speaks",
         zh="中近景、慢推（送瓦屋裁切）：許硯第一格已經兩手拱在胸前，一揖、直起身，不卑不亢地朝畫右外看不到的人說（唐萬金，不點名；那一側到邊緣只有黃土地與木板門）。稿子『畫面右邊緣是唐萬金的紫袖』『攤開兩隻空手』不拍（不描述畫外的人；一鏡一個動作）"),
    dict(loc="pm_c", cam="Low-angle medium close-up, slow push in", chars=["weishaoqing"], night="pm",
         comp=f"low-angle medium close-up of {WEI}, already standing on the packed earth from the first frame, framed from the chest up with space above his head, {FAN} held before his chest, his face three-quarter to screen left {off('left', 'the bare branches and the clear sky')}; smooth and smug: a thin easy smile, eyes half lidded, lips moving lazily between words; behind him the bare branches of a tree and the low tiled roofs against the clear sky in the warm afternoon light",
         lines=[("weishaoqing", "岳父，他家的牆是泥糊的，您去看一眼就明白。", "笑，本鏡可以笑")],
         motion="Wei Shaoqing dips his head in one small bow toward the left edge of the frame as he speaks",
         zh="低角度中近景、慢推（送午後調色的禿樹裁切 `set-guangchang-pm-shu-l1`；稿子『身後只有偏西的天』）：魏少卿第一格已經站在台下的地上、合著的扇子拿在胸前，朝畫左外看不到的人（唐萬金，不點名）微微欠身、笑著說（稿子『本鏡可以笑』）。稿子『摺扇打開、用扇子往許硯那邊一點』不拍（拍法 30：扇子一直合著；一鏡一個動作）；『從台階走下來』在第一格已經完成"),
    dict(loc="pm_r", cam="Medium shot, slow push in", chars=["tangwanjin"], night="pm",
         comp=f"medium shot on the packed pale earth at the edge of the square: {TWJ}, standing, framed from the knees up, his face three-quarter to screen right toward the carriage at the right edge of the frame, never the lens; at the right edge {CARRIAGE_DOOR}; he is the only person in the frame; decided and stiff, not smiling: chin up, brows down, lips moving firmly between words; behind them, soft, the long low tiled building in the warm afternoon sun",
         lines=[("tangwanjin", "好，帶路！我倒要看看，我囡囡住的是什麼地方。", "一甩袖")],
         motion="Tang Wanjin flings his wide purple sleeve once toward the carriage as he speaks",
         zh="中景、慢推（送瓦屋裁切）：唐萬金面朝畫右緣的大車（只見黑漆車廂與一匹馬的頭頸，車門第一格已經拉開，拍法 26），一甩紫袖、朝大車說（本場結尾）。稿子『前景車輪』『車門邊鄭伯的手與袖口拉著車門』『抬腳踩上車凳』不拍（不描述畫面邊緣多出來的手；一鏡一個動作）；剪在甩袖的一半，接院子"),
    # ---- scene 2: the same day, the sun low, the Xu yard (set-xujia-yuan-dong-qing-l1 and its crops).
    dict(chapter="許家院子，傍晚", loc="yard_m", cam="Medium shot, slow push in", chars=["qinshuang", "tangwanjin"], night="dusk",
         comp=f"medium shot at standing eye height just inside the yard gate, the gate swung back behind them: on the right {TWJ}, already a step inside the gate from the first frame, framed from the knees up, facing us, his head turned toward screen right, looking the yard over, his lips pressed shut, never the lens; on the left, half a step before him and a little to the side, {QIN}, framed from the knees up, her left arm already held out across his way from the first frame, her face three-quarter to screen right toward him, never the lens; blunt and wary, not smiling: brows level, eyes narrowed, lips moving clearly between words; {HANDS}; exactly two people",
         lines=[("qinshuang", "小棠，這位老爺是誰？一進門就東張西望。", "擋在門邊")],
         motion=f"Tang Wanjin slowly turns his head from screen right to screen left, looking the yard over; {quiet('Tang Wanjin')}",
         zh="中景、慢推（人眼高；送免費新圖 `set-xujia-yuan-dong-men2-l1`：院門、小瓦簷、屋角、禿樹；草頂橘點已塗掉）：唐萬金第一格已經跨進院門一步、面朝我們，頭從畫右慢慢轉到畫左把院子看一遍（嘴閉著）；畫左秦霜（深褐短衣、寬皮帶上什麼都沒插：柴刀照聖經不寫）在他半步前、左臂第一格已經橫在他前面擋著，眼睛盯著他說（她問的是唐小棠，眼睛看的是這位老爺）。稿子『前景竹籬笆、推開破木門、井邊阿令的背影、母雞拍翅』不拍（院子圖是泥牆與院門；一鏡一個動作；母雞交給音效）"),
    dict(loc="yard_m", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "qinshuang"], nospeak=["tangxiaotang"], night="dusk",
         comp=alone(f"{STACK} held against her chest in her right arm from the first frame, her left arm already reaching out to the sleeve of the woman beside the gatepost; half a step beyond her in the left third of the frame, her whole figure clear of the young woman's head and shoulders, {QIN}, standing, framed from the waist up, one hand on the swung-back plank gate, her face three-quarter toward her, never the lens, her lips pressed shut; beyond them, soft, the yard gate under its small tiled roof and the golden field in the low evening sun; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "standing on the packed earth just inside the yard gate,"),
         lines=[("tangxiaotang", "秦姐姐，這是我爹，從江南追到這裡來的。", "小聲")],
         motion=f"her left hand tugs once at the sleeve of the woman beside the gatepost, only her arm moving; {quiet('Qin Shuang', 'her')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送院門裁切）：唐小棠背影在畫面正中、頭不動，右臂抱著帳本，左手拉一下畫左秦霜的袖子（只動手臂；審稿建議 5：帳本換手，不必越過身體）；秦霜在她前方半步、畫面左三分之一、不跟她的頭與肩重疊，一手扶著拉開的院門、看著她、嘴閉著（nospeak，拍法 3）。稿子『從父親身後跨進門』在第一格已經完成；『秦霜點頭退開半步』不拍（一鏡一個動作）"),
    dict(loc="yard_j", cam="Medium shot, slow push in", chars=["aling"], night="dusk",
         comp=f"medium shot of {ALING}, {VEIL}, standing beside the round stone well, framed from the waist up, the round stone rim of the well along the bottom of the frame, her right hand already on the rope handle of {BUCKET} standing on the rim from the first frame, her face three-quarter to screen left, her eyes lowered, never the lens; she is the only person in the frame; cool and watchful, not smiling: steady narrow eyes above the veil, brows level; behind her the low mud-and-stone wall and a few planks leaning against it in the low evening sun; {HANDS}",
         motion=f"A-ling's right hand eases the bucket a little closer along the well's stone rim as her eyes lift once toward the yard gate beyond the left edge of the frame and drop back to the bucket; {quiet('A-ling', 'her')}, her lips still under the veil",
         zh="中景、慢推（腰以上、井沿在畫面下緣，審稿建議 7；送免費新圖 `set-xujia-yuan-dong-jing-l1`：井、木轆轤、靠在泥牆上的幾片木板；拍法 29 井在前右）：阿令（面巾第一格已經戴著、垂到胸口中間，送 `aling-veil-portrait-l1`、不送角度圖，拍法 21）右手扶著井沿上一只木桶的繩把，把桶沿著井沿往身邊挪近一點、同時眼睛往畫左外的院門抬一下又垂回水桶（腰以上的中景只有看，shot_reading 讀成 motion.look；挪桶是同一拍、對物的動作）（無台詞，嘴閉著）。稿子『從腰間抽出面巾拉上來、在腦後繫好、轉過身去』不拍：參考圖壓過文字，面巾第一格就戴著（拍法 19、21）；『瞄到一角寶藍錦袍』不寫（不描述畫外的人）"),
    dict(loc="yard_m", cam="Medium shot, slow push in", chars=["weishaoqing"], night="dusk",
         comp=f"medium shot of {WEI}, already a step inside the yard gate from the first frame, framed from the waist up, {FAN} raised before his chest, the swung-back plank gate and the golden field behind him, his face three-quarter to screen right {off('right', 'the low mud-and-stone wall and the bare tree')}; sneering and fastidious: a thin disdainful smile, nose wrinkled, eyes half lidded, lips moving slowly between drawled words",
         lines=[("weishaoqing", "岳父請看，泥牆茅草，這就是他的家。", "嫌棄，拖長音，本鏡可以笑")],
         motion="Wei Shaoqing sweeps the tip of the closed fan slowly across the yard before him as he speaks",
         zh="中景、慢推（送院門裁切）：魏少卿第一格已經跨進院門一步，合著的扇子往院子慢慢一掃，嫌棄地拖長音朝畫右外看不到的人說（唐萬金，不點名；那一側到邊緣只有泥牆與禿樹；稿子『可以帶嫌棄的笑』）。稿子『打開的摺扇掩在鼻子下』不拍（拍法 30：扇子一直合著，打開的扇面會長字）；前景柴堆不拍（真人圖的柴堆在屋前、畫左）"),
    dict(loc="yard_w", cam="Low-angle medium shot, slow push in", chars=["xiaohe"], night="dusk",
         comp=f"medium shot at a child's height before the thatched farmhouse: {XIAOHE}, already stopped on the packed earth from the first frame, framed from the knees up, {BOWL} held in both her hands at her chest, the dark doorway behind her, her face turned up three-quarter to screen right {off('upper right', 'the mud-and-stone wall of the farmhouse and the firewood', he='she')}; bright and eager: wide shining eyes, a big gap-toothed smile, lips moving brightly between words; {HANDS}",
         lines=[("xiaohe", "伯伯，喝碗井水，我們家的井水是甜的！", "踮腳，本鏡可以笑")],
         motion="little Xiaohe rises up on her toes and lifts the bowl high toward the upper right with both hands as she speaks",
         zh="低角度中景（小禾的高度）、慢推（送免費新圖 `set-xujia-yuan-dong-wu2-l1`：屋門、小格窗、柴堆；草頂橘點已塗掉）：小禾第一格已經從屋門跑出來站住、兩手捧著缺一角的粗陶碗，踮起腳把碗舉高、笑著朝畫右上外看不到的人說（唐萬金，不點名；那一側到邊緣只有屋牆與柴堆）（稿子『本鏡可以笑』）。稿子『從屋門跑出來、右邊唐萬金低頭』只拍踮腳舉碗（一鏡一個動作；畫面裡只有她）"),
    dict(loc="yard_q", cam="Close-up, slow push in", chars=["tangwanjin"], night="dusk",
         comp=f"close-up of {TWJ}, standing, framed from the chest up with space above his head, {BOWL} already held in both his hands at his chin from the first frame, his eyes on the chipped rim, never the lens; he is the only person in the frame; wary turning surprised, not smiling: brows drawn at first, then lifting, eyes widening a little, lips moving slowly between words; behind him, soft, the low mud-and-stone wall and the golden field in the low evening light; {HANDS}",
         lines=[("tangwanjin", "碗缺了一角，這井水倒是真的甜。", "愣了一下")],
         motion="Tang Wanjin takes one small sip from the chipped bowl and his brows lift in surprise as he speaks",
         zh="近景、慢推（送免費新圖 `set-xujia-yuan-dong-qiang-l1`：泥牆與牆外的田）：唐萬金第一格已經兩手捧著缺角陶碗在下巴前，看著碗沿缺口，喝一小口、眉毛一挑、愣住地說（不笑）。稿子『身後虛焦是光禿的柿子樹』改泥牆（樹在圖上的牆後）；『皺眉看碗沿』在第一格交代"),
    dict(loc="yard_q", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "tangwanjin"], nospeak=["tangxiaotang"], night="dusk",
         comp=alone(f"{STACK} held against her chest in her left arm from the first frame; one step beyond her in the right third of the frame, his whole figure clear of her head and shoulders, {TWJ}, standing, framed from the waist up, facing her, his face three-quarter toward her, never the lens, both his hands empty; softened and coaxing, not smiling: brows raised, eyes pleading, lips moving gently between words; beyond them, soft, the low mud-and-stone wall and the golden field in the low evening sun; she stays in the middle of the frame the whole shot; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "standing on the packed earth of the yard,"),
         lines=[("tangwanjin", "囡囡，跟爹回江南，爹不罵妳。", "放軟")],
         motion=f"Tang Wanjin reaches his right hand out toward her as he speaks; she stays where she is; {HEADSTILL}",
         zh="中景（從背後）、慢推（送泥牆裁切）：唐小棠背影在畫面正中、頭不動、左臂抱著帳本；唐萬金在她前方一步、畫面右三分之一、不跟她重疊，放軟地朝她伸出右手說（不笑）（nospeak，拍法 3）。稿子『把碗放上矮木桌』『她往後退一小步』不拍：圖上沒有矮木桌（不寫）；一鏡一個動作（下一鏡稿子寫她『不退』）"),
    dict(loc="yard_q", cam="Close-up from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="dusk",
         comp=alone(f"{STACK} held against her chest in both arms from the first frame, only its pale edge showing at her sides; beyond her, soft, the low mud-and-stone wall and the golden field in the low evening sun; {HANDS}",
                    "standing on the packed earth of the yard,", frame="framed from the shoulders up", shot="close-up"),
         lines=[("tangxiaotang", "爹，我不回去。這裡是我的家。", "眼眶紅，不退")],
         motion=f"her shoulders draw up and square, and she holds her ground, only her shoulders moving; {HEADSTILL}",
         zh="近景（從背後）、慢推（送泥牆裁切）：唐小棠後腦與肩在畫面正中、頭不動，兩臂抱著帳本，肩膀一挺、站穩（只動肩）（nospeak，拍法 3）。稿子『下巴以上、眼眶紅、下巴抬著、抿一下嘴』改背影（她整集不露臉）"),
    dict(loc="yard_q", cam="Low-angle medium close-up, slow push in", chars=["weishaoqing"], night="dusk",
         comp=f"low-angle medium close-up of {WEI}, already standing by the low mud-and-stone wall from the first frame, framed from the chest up with space above his head, {FAN}, {DOC} already in his left hand from the first frame, held before his chest, his face three-quarter to screen left {off('left', SIDE_WALL)}; cold and sure: a cold thin smile, eyes narrowed, lips moving coolly between words; behind him, soft, the golden field in the low evening light; {HANDS}",
         lines=[("weishaoqing", "婚書在此，岳父親筆簽的，她說了不算。", "冷笑")],
         motion="Wei Shaoqing raises the folded sheet in his left hand toward the left edge of the frame as he speaks, its plain back toward us",
         zh="低角度中近景、慢推（送泥牆裁切）：魏少卿第一格已經站在院子右邊的泥牆邊，左手已經拿著摺好的婚書（米色紙、細金邊、只見紙背，拍法 27），往畫左外看不到的人（唐萬金，不點名）舉起、冷笑地說（稿子『冷笑』）。稿子『從寶藍袖裡抽出、一抖打開一半』不拍（一鏡一個動作；不寫 open；拍法 27 只見紙背）；柴堆在真人圖的畫左，他站在畫右的泥牆邊（拍法 29）"),
    dict(loc="yard_w", cam="Medium shot, slow push in", chars=["xuyan"], night="dusk",
         comp=f"medium shot of {XU_D}, standing on the packed earth before the thatched farmhouse, framed from the waist up, {STACK} already held in both his hands at his chest from the first frame, his face three-quarter to screen right {off('right', SIDE_HOUSE)}; calm and courteous, not smiling: steady eyes, brows level, lips moving evenly between words; behind him, soft, the dark doorway and the mud-and-stone wall of the farmhouse in the low evening light; {HANDS}",
         lines=[("xuyan", "唐老爺，回不回江南先別急，先看一本帳。", "平穩，有禮")],
         motion="Xu Yan holds the stack of paper out toward the right edge of the frame with both hands, his head bowing a little, as he speaks",
         zh="中景、慢推（送屋前裁切）：許硯第一格已經兩手拿著帳本（縫邊的空白紙疊），雙手遞向畫右外看不到的人（唐萬金，不點名；那一側到邊緣只有屋牆與柴堆）、微微低頭、有禮地說。稿子『從柿子樹前走到兩人中間、唐小棠把帳本遞到他手上』在第一格已經完成（一鏡一個動作；畫面裡只有他）"),
    dict(loc="yard_e", cam="Insert close-up, slow push in", chars=[], night="dusk",
         comp=f"{INSERT_LIGHT}: insert close-up seen from slightly above, looking down, the very first frame is already a close view of the edge of {STACK}, held level in two plump hands in deep purple silk sleeve cuffs woven with small gold ingot shapes, one plain gold ring on the right hand, its top sheet blank and pale; far below, soft and out of focus, only packed yellow earth with long evening shadows fills the background to every edge; only the stack of blank sheets, the two hands and their sleeve cuffs are in the frame",
         lines=[("tangwanjin", "每批編號，記買家……一筆都不漏。", "喃喃")],
         motion=NOBODY + "The right hand turns the blank pages over one after another, faster and faster, the paper fluttering",
         zh="插鏡、慢推（第一格就是從稍上方往下看的帳本，審稿必改 3：d1 不寫院子的地點句、背景只有黃土地鋪到四邊；送免費新圖 `set-xujia-yuan-dong-di-l1`：黃土地與傍晚的長影子，遠遠虛焦）：紫袖、一枚金戒指的胖手把空白的頁一頁頁翻、越翻越快（唐萬金畫外的台詞放錄音）。稿子『矮木桌上攤開的帳本、格線與小紅圈』不拍：圖上沒有矮木桌，帳本拿在他手上（同第 29 集 s15 審稿後的寫法，只送土地圖會把帳本放到地上）；紙上的記號會長字（拍法 7）；『手指順著一欄往下滑』不拍（一鏡一個動作；不寫單根手指）"),
    dict(loc="yard_q", cam="Close-up, slow push in", chars=["tangwanjin"], night="dusk",
         comp=f"close-up of {TWJ}, standing, framed from the chest up with space above his head, {STACK} already raised before his face in both hands from the first frame, his face three-quarter to screen left {off('left', SIDE_WALL)}; astonished, not smiling: brows shooting up his forehead, narrow eyes going wide, mouth slack between words; behind him, soft, the golden field in the low evening light; {HANDS}",
         lines=[("tangwanjin", "被人賠本壓價，三十天還贏人家兩倍？", "眉毛挑到額頭")],
         motion="Tang Wanjin lowers the stack of paper from before his face, his brows shooting up and his narrow eyes going wide, as he speaks",
         zh="近景、慢推（送泥牆裁切）：唐萬金第一格已經把帳本舉在臉前，放下來，眉毛一路挑到額頭、瞇著的眼整個睜開，朝畫左外看不到的人（女兒，不點名）說（不笑）。稿子『坐在長凳上』改站著（圖上沒有長凳）"),
    dict(loc="yard_w", cam="Medium close-up, slow push in", chars=["xuyan"], night="dusk",
         comp=f"medium close-up of {XU_D}, standing before the thatched farmhouse, framed from the chest up with space above his head, his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, never the lens; both sides of the frame are only the mud-and-stone wall of the farmhouse and the split firewood all the way to the edges, and he is the only person in the frame; modest and warm, not smiling: steady eyes softening, brows level, lips moving evenly between words; behind him, soft, the dark doorway in the low evening light",
         lines=[("xuyan", "帳是小棠做的，價是她定的，三十天的功勞都是她的。", "平穩")],
         motion="Xu Yan turns his head once toward the left edge of the frame as he speaks, his eyes softening",
         zh="中近景、慢推（送屋前裁切）：許硯先朝畫右外看不到的人（唐萬金）說，再轉頭往畫左外看一眼（唐小棠，不點名；兩側到邊緣都只有屋牆與柴堆），眼神放軟（不笑）。稿子『畫面左邊緣是唐小棠的肩』『拱手』不拍（不描述畫外的人；一鏡一個動作；不寫矮木桌）"),
    dict(loc="yard_q", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="dusk",
         comp=alone(f"both her hands already clasped behind her back at her waist from the first frame, nothing in them; beyond her, soft, the low mud-and-stone wall and the golden field glowing in the low evening sun; {HANDS}",
                    "standing on the packed earth of the yard,"),
         lines=[("xitong", "叮。唐小棠，好感加六，突破四十。", "冷，宣布")],
         panel=[("唐小棠 好感 +6 → 42", "affection"), ("突破四十", "affection")],
         motion=f"her clasped fingers twist together once behind her back and her shoulders lift a little, only her hands and shoulders moving; {HEADSTILL}; {quiet('the young woman', 'her')}",
         zh="中景（從背後、腰以上，審稿建議 2）、慢推（送泥牆裁切）：唐小棠背影在畫面正中、頭不動，兩手第一格已經背在身後腰間，手指在背後害羞地絞一下、肩膀輕輕一提（只動手與肩）；全程嘴閉著（系統畫外，面板「唐小棠 好感 +6 → 42」「突破四十」由剪接疊上，拍法 11）。稿子『主觀近景、臉頰紅、梨渦笑』改背影（她整集不露臉，同第 25 集好感那一鏡）；帳本 s16 已在許硯手上，她兩手空著"),
    dict(loc="yard_w", cam="Close-up, slow push in", chars=["xuyan"], night="dusk",
         comp=f"close-up of {XU_D}, framed from the chest up with space above his head, his face three-quarter to screen right, his eyes level on a spot beyond the right edge of the frame, never the lens; he is the only person in the frame; quiet and dry: steady eyes, brows level, lips pressed shut; behind him, soft, the dark doorway and the mud-and-stone wall of the farmhouse in the low evening light",
         lines=[("xitong", "開箱獎勵：高產糧種一小袋，六十日可收。", "冷，宣布"),
                ("xitong", "功勞送人，倒是送對了一次。", "冷")],
         panel=[("開箱獎勵：高產糧種一小袋，六十日可收", "reward")],
         motion=f"Xu Yan's eyes settle on that spot and his brows lift a little, then level again; {SILENT_HE}; he is listening, not speaking",
         zh="近景、慢推（送屋前裁切；拍法 11 不寫藍光，稿子『臉被面前的淡藍光照亮』不照用）：許硯聽系統兩句，眼神一定、眉毛輕輕一抬又放平，全程嘴閉著；面板「開箱獎勵：高產糧種一小袋，六十日可收」由剪接疊上。稿子 c21 三句錄音加起來 10.11 秒（超過約 10 秒），拆成 s21（系統兩句）與 s21b（心裡話），同第 28 集 s15／s15b"),
    dict(sid="s21b", loc="yard_w", cam="Close-up, slow push in", chars=["xuyan"], night="dusk",
         comp=f"close-up of {XU_D}, framed from the chest up with space above his head, his face three-quarter to screen right, his eyes lowered a little, never the lens; he is the only person in the frame; quiet and certain: steady eyes, brows level, lips pressed shut; behind him, soft, the dark doorway and the mud-and-stone wall of the farmhouse in the low evening light",
         lines=[("xuyan", "不是送她的，本來就是她算出來的。", "心裡話，錄得近、輕", "inner")],
         motion=f"one corner of Xu Yan's mouth twitches once and is pressed straight again; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（送屋前裁切）：許硯的心裡話（錄音，嘴閉著），嘴角動一下又壓住（稿子）；本集的鬥嘴。從 c21 拆出（見 s21）"),
    dict(loc="yard_e", cam="Insert close-up, slow push in", chars=[], night="dusk",
         comp=f"{INSERT_LIGHT}: insert close-up seen from slightly above, looking down, the very first frame is already a close view of a man's right hand in a faded blue-grey sleeve cuff, held low at his side, palm up, {SEEDS} lying on the palm; far below, soft and out of focus, only packed yellow earth fills the background to every edge; only the hand, its sleeve cuff and the pouch are in the frame",
         act=3,
         motion=NOBODY + "The fingers slowly close over the little pouch until it is hidden in the hand",
         zh="插鏡、慢推（第一格就是從稍上方往下看的掌心；送土地裁切，審稿必改 3：d1 不寫地點句，背景只有黃土地鋪到四邊、遠遠虛焦）：許硯藍灰袖口的右手垂在身側、掌心朝上，一個鬆開袋口的小素布袋、滿滿飽滿的金黃稻穀，手指慢慢合起把它握住（無台詞）。稿子『收進右袖』不拍（一鏡一個動作；剪接交代）"),
    dict(loc="yard_q", cam="Medium close-up, slow push in", chars=["weishaoqing"], night="dusk",
         comp=f"medium close-up of {WEI}, standing by the low mud-and-stone wall, framed from the chest up with space above his head, {FAN} held still in mid-air before his chest from the first frame, {DOC} in his left hand at his side, his face three-quarter to screen left {off('left', SIDE_WALL)}; strained: a stiff forced smile, eyes hard and darting, lips moving tightly between words; behind him, soft, the golden field in the low evening light; {HANDS}",
         lines=[("weishaoqing", "鄉下鋪子的小帳而已，岳父何必當真？", "笑得很僵")],
         motion="Wei Shaoqing takes one small step toward the left edge of the frame as he speaks",
         zh="中近景、慢推（送泥牆裁切）：魏少卿合著的扇子第一格停在胸前半空、左手拿著婚書，往畫左外看不到的人（唐萬金）走一小步、笑得很僵地說（稿子『笑得很僵』）。稿子『啪地收扇』不拍（拍法 30：扇子一直合著；收扇聲交給音效）"),
    dict(loc="yard_q", cam="Close-up, slow push in", chars=["tangwanjin", "zhengbo"], nospeak=["zhengbo"], night="dusk",
         comp=f"close-up of two men by the low mud-and-stone wall: in the middle {TWJ}, standing, framed from the chest up, {STACK} held at his chest in both hands, his face mild and at ease from the first frame, his eyes on the paper, never the lens; at the left of the frame, close behind Tang Wanjin's right shoulder and bent down to his right ear, {ZHENG}, framed from the chest up, his right hand already cupped against the side of his own mouth from the first frame, the cupped hand between his mouth and Tang Wanjin's ear, his lips hidden behind it, his eyes lowered, never the lens; behind them, soft, the golden field in the low evening light; {HANDS}; exactly two people",
         lines=[("zhengbo", "老爺，京裡那筆鹽船的帳，今天能算了。", "貼耳壓低，錄得很近、很輕")],
         motion=f"the warmth drains from Tang Wanjin's face, his brows press down and his narrow eyes turn cold and slide toward the right edge of the frame; {quiet('Tang Wanjin')}; Steward Zheng's cupped hand stays between his mouth and Tang Wanjin's ear, his lips hidden behind it",
         zh="近景（雙人）、慢推（送泥牆裁切）：唐萬金第一格還對著帳本、臉上平和自在（不寫笑，免得一開始就大笑退不乾淨；審稿建議 3）；鄭伯（高瘦、灰白山羊鬚，送 `zhengbo-portrait-l1`）在畫左、貼在他右肩後、彎到他右耳邊，右手第一格已經攏成半圈貼在自己嘴邊、擋在他的嘴與唐萬金的耳朵之間、嘴唇藏在手後（nospeak，耳語放錄音；不寫成舉在嘴邊，免得演成喊話或吃東西）；唐萬金臉上的和氣一下退光、眉頭壓低、瞇眼變冷、往畫右（魏少卿那邊）一滑，嘴閉著。聖經：鄭伯畫成高瘦後可以跟唐萬金同鏡耳語（稿子的『只露手與袖口』照聖經放寬）。稿子『坐著、慢慢把帳本闔上』不拍（圖上沒有長凳；一鏡一個動作）；袖口的小毛筆不寫（會長字）"),
    dict(loc="yard_q", cam="Medium shot, slow push in", chars=["tangwanjin", "weishaoqing"], night="dusk",
         comp=f"medium shot by the low mud-and-stone wall, both men framed from the waist up, side-on to us: on the left {TWJ}, already standing one step before the other man from the first frame, {STACK} held in his left hand at his side, facing screen right, never the lens; grim, every trace of warmth gone, not smiling: brows pressed down, eyes cold, lips moving hard between words; on the right {WEI}, {FAN}, {DOC} in his left hand, facing screen left, never the lens, his lips pressed shut, not smiling; behind them, soft, the golden field in the low evening light; {HANDS}; exactly two people",
         lines=[("tangwanjin", "五年前，你爹說借我八條鹽船，一條都沒還。", "笑全收了")],
         motion=f"Tang Wanjin tucks the stack of paper up under his left arm as he speaks; {quiet('Wei Shaoqing')}",
         zh="中景、慢推（送泥牆裁切）：唐萬金第一格已經走到魏少卿一步外（畫左、側面朝畫右），把左手垂著拿的帳本往左腋下一夾（審稿建議 4：不越過身體）、笑全收了地說（不笑，原版必修）；魏少卿在畫右、側面朝畫左、拿著合著的扇子與婚書、嘴閉著、不笑。稿子『從長凳站起來、穿過院子（越軸跟拍）』在第一格已經完成（一鏡一個動作）"),
    dict(loc="yard_q", cam="Close-up, slow push in", chars=["weishaoqing"], night="dusk",
         comp=f"close-up of {WEI}, standing by the low mud-and-stone wall, framed from the chest up with space above his head, {DOC} held in his left hand, his face three-quarter to screen left {off('left', SIDE_WALL)}; brittle and defiant, not smiling: a frozen contemptuous curl of the lip, chin raised, eyes hard, lips moving sharply between words; behind him, soft, the golden field in the low evening light; {HANDS}",
         lines=[("weishaoqing", "宰相府跟你借幾條船，那又如何？", "抬下巴，乾笑")],
         motion="Wei Shaoqing draws the folded sheet back against his chest as he speaks, his chin up",
         zh="近景、慢推（送泥牆裁切）：魏少卿下巴抬著、把婚書往自己胸前收，朝畫左外看不到的人（唐萬金）說；輕蔑僵在臉上、不寫笑（拍法 30：第 30 集是他輸的集，NOSMILE；『乾笑』交給錄音）。稿子『身後柴堆與泥牆』照真人圖改泥牆與牆外的田"),
    dict(loc="yard_q", cam="Close-up, slow push in", chars=["tangwanjin"], night="dusk",
         comp=f"close-up of {TWJ}, framed from the chest up with space above his head, {STACK} under his left arm, his right hand already raised before his chest from the first frame, his face three-quarter to screen right {off('right', SIDE_WALL)}; bitter and grieved, not smiling: jaw clenched, teeth set, eyes red-rimmed, lips moving hard between words; behind him, soft, the golden field in the low evening light",
         lines=[("tangwanjin", "船扣在你家，這張婚書，就是押給你們的抵押。", "咬牙，眼眶紅")],
         motion="Tang Wanjin thrusts his flat right hand, fingers together and palm down, toward the right edge of the frame as he speaks",
         zh="近景、慢推（送泥牆裁切）：唐萬金咬著牙、眼眶發紅，右手手掌攤平、四指併攏、掌心朝下，往畫右外看不到的人（魏少卿手上的婚書）一送（審稿建議 9：兩指併攏仍可能畫成比 V；不寫 open）、說（不笑，原版必修：說抵押時仰頭大笑是錯）。稿子『前景右虛焦是魏少卿手上的米白婚書』不拍（不寫畫面邊緣的別人的手）"),
    dict(loc="yard_q", cam="Close-up from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="dusk",
         comp=alone(f"both her hands empty at her sides; beyond her, soft, the low mud-and-stone wall and the golden field in the low evening sun; {HANDS}",
                    "standing on the packed earth of the yard,", frame="framed from the shoulders up", shot="close-up"),
         lines=[("tangxiaotang", "抵押……爹，你簽字不是為了賣我？", "發抖")],
         motion=f"her right hand comes up toward her mouth, only her arm moving, her shoulders trembling a little; {HEADSTILL}",
         zh="近景（從背後）、慢推（送泥牆裁切）：唐小棠後腦與肩在畫面正中、頭不動，右手往嘴邊抬起（只動手臂）、肩膀微微發抖（nospeak，拍法 3）。稿子『下巴以上、一滴淚滑下臉頰、眼睛看畫外右邊的爹』改背影；『站在柿子樹旁』照真人圖（樹在牆後）不寫"),
    dict(loc="yard_q", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "tangwanjin"], nospeak=["tangxiaotang"], night="dusk",
         comp=alone(f"both her arms raised a little before her chest; half a step beyond her in the right third of the frame, his whole figure clear of her head and shoulders, {TWJ}, standing, framed from the waist up, facing her, his face three-quarter toward her, never the lens, both his hands already holding {STACK} out against her arms from the first frame; softened and tender, not smiling: brows raised, eyes wet, lips moving gently between words; beyond them, soft, the low mud-and-stone wall and the golden field in the low evening sun; she stays in the middle of the frame the whole shot; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "standing on the packed earth of the yard,"),
         lines=[("tangwanjin", "傻囡囡，爹不簽，他們就要動妳。", "放軟")],
         motion=f"Tang Wanjin presses the stack of paper into her arms and her arms close round it as he speaks; {HEADSTILL}",
         zh="中景（從背後）、慢推（送泥牆裁切）：唐小棠背影在畫面正中、頭不動；唐萬金在她前方半步、畫面右三分之一、不跟她重疊，第一格已經兩手把帳本遞到她臂前，塞進她懷裡、她兩臂抱住，放軟地說（不笑）（nospeak，拍法 3）。稿子『他轉身走回女兒這邊（越軸）』在第一格已經完成；『用胖手輕拍她的丸子頭』『抽一下鼻子』不拍（一鏡一個動作；碰她的頭會讓她轉頭露臉）"),
    dict(loc="yard_s", cam="Low-angle medium close-up, slow push in", chars=["weishaoqing"], night="dusk",
         comp=f"low-angle medium close-up of {WEI}, standing, framed from the chest up with space above his head, {FAN} held at his side, {DOC} already raised high in his left hand from the first frame, its plain back toward us, his face three-quarter to screen left {off('left', SIDE_SKY)}; every trace of ease gone, not smiling: jaw tight, eyes hard and wide, the corners of his mouth pulled down, lips moving sharply between words; behind him the bare branches of a tree against the glowing evening sky; {HANDS}",
         lines=[("weishaoqing", "唐萬金，你敢為了一個女兒，跟宰相府翻臉？", "輕佻全沒了")],
         motion="Wei Shaoqing thrusts the folded sheet forward toward the left edge of the frame as he speaks",
         zh="低角度中近景、慢推（送免費新圖 `set-xujia-yuan-dong-shu-l1`：禿枝映著傍晚發亮的天，太陽在畫右）：魏少卿婚書第一格已經高高舉著，往畫左外看不到的人（唐萬金）一送、輕佻全沒了地說（拍法 30：NOSMILE，嘴角往下）。稿子『收起的摺扇指著唐萬金、往前一步』不拍（一鏡一個動作）"),
    dict(loc="yard", cam="Wide shot, slow push in", chars=["tangwanjin", "weishaoqing", "xuyan"], night="dusk",
         comp=f"wide shot at standing eye height, like the picture: in the middle of the yard before the low mud-and-stone wall {TWJ}, standing, framed full figure, side-on to us facing screen right, {DOC} already gripped in both his fists from the first frame, his face red and furious, not smiling, lips moving in a shout between words, never the lens; a step before him on the right {WEI}, standing, framed full figure, side-on facing screen left, his left hand empty and half raised, one closed folding fan held down at his side in his right hand, its dark bamboo ribs pressed tight together like a short slim stick, his lips pressed shut, not smiling, never the lens; further back on the left before the thatched farmhouse {XU_D}, standing, framed full figure, small, facing them, his lips pressed shut, never the lens; {HANDS}; exactly three people",
         lines=[("tangwanjin", "八條船，我不要了！女兒，我要！", "用喊的")],
         motion=f"Tang Wanjin tears the folded sheet in two with one hard pull as he shouts; {quiet('Wei Shaoqing and Xu Yan', 'their', plural=True)}",
         zh="全景、慢推（人眼高、照圖；送免費新圖 `set-xujia-yuan-dong-qing2-l1`：整個院子，板子、門楣紅點、兩片掛著的葉子與草頂的橘色圓點已塗掉）：院子中間泥牆前，唐萬金（側面朝畫右）第一格已經兩手攥著婚書，一扯撕成兩半、喊著說；魏少卿在他前方一步（畫右、側面朝畫左）、左手空著半舉、右手合著的扇子垂在身側（審稿建議 6：s30 到 s34 扇子不消失）、嘴閉著；許硯在畫左後方屋前、小小的、嘴閉著（三人，拍法 1）。稿子『大步走到魏少卿面前、一把搶過婚書、往風裡一甩』在第一格已經完成或交給下一鏡（一鏡一個動作）；左往右的搖鏡改慢推；前景柿子樹枝不拍"),
    dict(loc="yard_e", cam="Insert close-up, slow push in", chars=[], night="dusk",
         comp=f"{INSERT_LIGHT}: insert close-up seen from above, looking down, the very first frame is already a close view of {HALVES}, tumbling down a hand's width above packed yellow earth, lit gold by the low evening sun; the earth fills the frame to every edge; only the two torn halves and the earth below them are in the frame",
         act=3,
         motion=NOBODY + "The two torn halves turn over slowly in the air and settle onto the earth, only their plain backs showing",
         zh="插鏡、慢推（第一格就是從上方往下看、離黃土地一掌高的撕開婚書；送土地裁切；審稿必改 3：d1 不寫地點句，土鋪滿四邊）：撕成兩半的米色細金邊婚書在斜陽裡翻、慢慢落到土上，只見紙背（拍法 27；無台詞）。稿子『一截寶藍錦袖掠過』不拍（不寫邊緣別人的手）"),
    dict(loc="yard_q", cam="Close-up from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="dusk",
         comp=alone(f"{STACK} held against her chest in her left arm from the first frame; beyond her, soft, the low mud-and-stone wall and the golden field in the low evening sun; {HANDS}",
                    "standing on the packed earth of the yard,", frame="framed from the shoulders up", shot="close-up"),
         lines=[("tangxiaotang", "魏公子，賭約你輸了。撤婚，不許再提冒名。", "擦掉眼淚")],
         motion=f"the back of her right wrist comes up to her eyes once and goes down again, only her arm moving; {HEADSTILL}",
         zh="近景（從背後）、慢推（送泥牆裁切）：唐小棠後腦與肩在畫面正中、頭不動，右手腕背往眼睛抹一下、放下（只動手臂）（nospeak，拍法 3；同第 25 集的抹淚）。稿子『下巴一抬、撥過兩顆算珠「喀」一聲』不拍：算盤只在插鏡入鏡（拍法 20），一鏡一個動作；『喀』交給音效"),
    dict(loc="yard_q", cam="Close-up, slow push in", chars=["weishaoqing"], night="dusk",
         comp=f"close-up of {WEI}, standing by the low mud-and-stone wall, framed from the chest up with space above his head, {FAN} squeezed in his right fist, his face three-quarter to screen left, his eyes lowered, never the lens; he is the only person in the frame; beaten and bitter, not smiling: jaw clenched hard, the corners of his mouth pulled down, lips moving tightly between words; behind him, soft, the golden field in the low evening light",
         lines=[("weishaoqing", "……撤。商會那三位老人，我會去說。", "咬牙")],
         motion="Wei Shaoqing turns his face away toward the right edge of the frame as he speaks, the closed fan tightening in his fist",
         zh="近景、慢推（送泥牆裁切）：魏少卿咬緊牙、扇子捏在拳裡，把臉別開往畫右、咬牙說（拍法 30：撤婚是他輸的鏡，NOSMILE）。稿子『腳邊是碎婚書』不拍（近景看不到腳）"),
    dict(loc="yard_m", cam="Medium shot, slow push in", chars=["tangwanjin", "xuyan"], night="dusk",
         comp=f"medium shot near the yard gate, both men framed from the waist up: on the left {XU_D}, standing, side-on to us facing screen right, never the lens, his lips pressed shut, not smiling; on the right {TWJ}, standing, side-on facing screen left, his right hand already raised beside the young man's shoulder from the first frame, never the lens; beaming now: a broad warm smile, eyes crinkled, lips moving heartily between words; behind them, soft, the yard gate under its small tiled roof and the golden field in the low evening sun; {HANDS}; exactly two people",
         lines=[("tangwanjin", "女婿，車後那匹棗紅馬留給你，算見面禮！", "拍肩，本鏡可以笑")],
         motion=f"Tang Wanjin claps his right hand down on Xu Yan's shoulder and Xu Yan sways a little as he speaks; {quiet('Xu Yan')}",
         zh="中景、慢推（送院門裁切）：許硯在畫左、唐萬金在畫右（都側面），唐萬金一掌拍在許硯肩上、許硯晃一下，笑著說（稿子『本鏡可以笑』）；許硯嘴閉著。稿子『另一手往籬笆外的大車一指』不拍（一鏡一個動作；身後是院門，台詞交代車）"),
    dict(loc="yard_m", cam="Medium shot, slow push in", chars=["qinshuang"], night="dusk",
         comp=f"medium shot in the yard gate: {QIN}, standing, framed from the waist up, the reins of {HORSE} already wound round her right hand from the first frame, the horse's head and neck beside her at the right of the frame; her face three-quarter to screen left {off('left', 'the plank gate and the corner of the thatched farmhouse', he='she')}; easy and pleased: a faint easy smile, bright eyes, lips moving brightly between words; behind them, soft, the golden field in the low evening sun; {HANDS}; exactly one person and one horse",
         lines=[("qinshuang", "好馬，腳力夠。許硯，這匹我替你養。", "接過韁繩，本鏡可以淡淡地笑")],
         motion="Qin Shuang strokes the horse's neck once with her left hand as she speaks",
         zh="中景、慢推（送院門裁切）：秦霜站在院門口，右手第一格已經繞著一匹棗紅馬的韁繩，馬的頭頸在她畫面右側（拍法 26：一匹、秦霜右手、馬在她畫右），左手摸一下馬脖子、朝畫左外看不到的人（許硯，不點名）說（稿子『可以淡淡地笑』）（本場結尾）。稿子『籬笆外解開拴在大車後的韁繩、大車在右後』不拍（一鏡一個動作；拍法 26 不拍四匹馬與大車；馬鞍的裝飾不寫）"),
    # ---- scene 3: the same yard, the wind rising.
    dict(chapter="許家井邊，起風", loc="yard", cam="Wide shot, slow push in", chars=["weishaoqing"], nospeak=["weishaoqing"], night="dusk",
         comp=f"wide shot at standing eye height, like the picture: at the very right edge of the frame, cut by it, soft and out of focus beside the round stone well, only the back of one grey-white cotton shoulder and the back of a high black bun with one plain wooden hairpin, turned fully away from us toward the yard gate, the back of her head toward us the whole shot; in the middle of the yard {WEI}, framed full figure, small, his back to us, the back of his head toward us, walking stiffly toward the yard gate in the back wall, {FAN}; {HANDS}; exactly two people",
         lines=[("weishaoqing", "唐家的事算了，這筆帳，我回京再算。", "背對院子，咬牙")],
         motion=f"Wei Shaoqing walks stiffly up to the yard gate and stops before it, his back to us the whole shot; the woman in the foreground stays still",
         zh="全景、慢推（人眼高、照圖；送塗過的整個院子）：魏少卿背對我們、小小的，僵著背往後牆的院門走、在門前停住（背影說話，nospeak，台詞放錄音）；右緣被畫框切掉、虛焦的只有井邊一個灰白的肩背與高髻的後面、木簪，整個人轉向院門、後腦朝我們（不點名、不送圖，拍法 2；審稿必改 4：不寫耳朵與面巾細繩，免得轉成側臉露出臉頰；阿令這時還戴著面巾、背對）。稿子『一陣風把乾柿葉捲過院子』交給音效（一鏡一個動作）；稿子『左前景阿令的肩』照真人圖改右前景（井在前右，拍法 29）"),
    dict(loc="yard_j", cam="Medium shot, slow push in", chars=["aling"], night="dusk",
         comp=f"medium shot of {ALING}, standing beside the round stone well, framed from the waist up, the round stone rim of the well along the bottom of the frame, {VEIL_BLOWN}, her right hand already gripping the rope handle of {BUCKET} standing on the rim from the first frame, her face three-quarter to screen left, never the lens; she is the only person in the frame; cold and still, not smiling: level unblinking eyes, lips closed; behind her the low mud-and-stone wall and a few planks leaning against it in the low evening sun; {HANDS}",
         motion=f"A-ling lifts the bucket off the well's stone rim with her right hand; only {VEIL_LOOSE} and a few strands of her hair stir in the wind, her dress still; {quiet('A-ling', 'her')}",
         zh="中景、慢推（腰以上、井沿在畫面下緣、手與桶第一格就在框裡，審稿必改 2；送井的裁切）：阿令（送沒戴面巾的 `aling-portrait-l1`，拍法 21：送面巾圖面巾會一直戴著）第一格那條長長的半透明灰紗已經只掛在左耳的細繩上、被風吹到左頰與左肩外、整張臉露出來（審稿必改 1：面巾寫成實物，圖上沒有），右手把井沿上的木桶提起來；只有面巾和幾縷頭髮在動、衣服不動（無台詞，嘴閉著）。掀開的那一下交給 s37→s38 的剪接（聖經拍法 21）"),
    dict(loc="yard_j", cam="Close-up, slow push in", chars=["aling"], night="dusk",
         comp=f"close-up of {ALING}, framed from the shoulders up, {VEIL_BLOWN}, a few loose strands of black hair blown across her cheek, her face three-quarter to screen left, her eyes lowered, never the lens; she is the only person in the frame; cold and unreadable, not smiling: still eyes, brows level, lips closed; behind her, soft, the low mud-and-stone wall in the low evening sun",
         motion=f"A-ling's eyes rise slowly and fix on the yard gate beyond the left edge of the frame, unblinking; {quiet('A-ling', 'her')}",
         zh="近景、慢推（送井的裁切）：阿令沒有面巾的臉（灰紗只掛在左耳的細繩上、吹到左頰外，審稿必改 1 寫成實物），幾縷黑髮吹過臉頰，不眨眼，眼睛慢慢抬起、直直看向畫左外的院門（無台詞，嘴閉著）。稿子『看向畫外右邊的院門』照真人圖改畫左（井在前右、院門在後中，拍法 29）"),
    dict(loc="yard_m", cam="Close-up, slow push in", chars=["weishaoqing"], night="dusk",
         comp=f"close-up of {WEI}, standing in the yard gate, his body half turned back toward the yard from the first frame, framed from the chest up with space above his head, {FAN} loose in his fingers, his face three-quarter to screen right toward the well beyond the right edge of the frame, never the lens; that side of the frame is only the low mud-and-stone wall all the way to the edge, and he is the only person in the frame; stunned, not smiling: his peach-blossom eyes going wide, his face draining, lips parting tightly between words; behind him, soft, the plank gate and the golden field in the low evening sun",
         lines=[("weishaoqing", "你……怎麼會在這裡？", "整個人僵住，聲音發緊，不要喊")],
         motion="Wei Shaoqing's eyes go wide and his whole body freezes as he speaks, the closed fan slipping a little down through his fingers",
         zh="近景、慢推（送院門裁切；稿子『身後只有門外的斜陽』）：魏少卿在院門口半轉回身，桃花眼瞪大、整個人僵住、收起的扇子在指間往下滑一點，望著畫右外的井（不點名、不描述阿令；那一側到邊緣只有泥牆）、聲音發緊地說（拍法 30：認出阿令是他輸的鏡，NOSMILE；結尾懸念）"),
    dict(loc="yard_k", cam="Wide shot, slow push in", chars=["aling", "weishaoqing", "xuyan"], night="dusk",
         comp=f"wide shot at standing eye height, like the picture: in the right foreground beside the round stone well {ALING}, standing, framed full figure, {BUCKET} held low in her right hand, {VEIL_BLOWN}, her body turned toward the yard gate, her face in left profile, her eyes on the gate, her lips closed, never the lens; far back in the yard gate in the middle of the back wall, small, {WEI}, framed full figure, half turned back toward the yard, frozen, his lips pressed shut, never the lens; in the middle of the yard, small, side by side with their backs to us, facing the yard gate: on the left {XU_D}, and on his right {TBACK}, {STACK} held against her chest, {only_tang()}; {HANDS}; exactly four people",
         motion=f"nobody moves; only {VEIL_LOOSE}, a few strands of A-ling's hair and the hems of their clothes stir in the wind; {quiet('A-ling, Wei Shaoqing and Xu Yan', 'their', plural=True)}; {HEADSTILL}",
         zh="全景、慢推（人眼高、照圖；送塗過的整個院子；本集、也是第 3 篇章最後一鏡，接點 30→31）：右前景井邊的阿令（送沒戴面巾的 `aling-portrait-l1`）右手提著一桶水、灰紗只掛在左耳的細繩上吹到左頰外（審稿必改 1）、身體轉向院門、左側臉、眼睛看著院門（審稿必改 5：不寫三分之四正臉）；後牆中間院門口小小的魏少卿半轉身、僵著；院子中間背對我們、小小的：左邊許硯、他右邊唐小棠的背影（剛好兩顆丸子、抱著帳本）望著院門（審稿必改 5：黏錯的句子拆開，接點 30→31 唐小棠在許硯右邊；院子格局縮成一句「照圖：屋在左、院門在後牆中間、井在前右」）；風吹動面巾、頭髮與衣角，四個人都不動、嘴都閉著（無台詞）。稿子『柿子樹下、轉過頭』照真人圖改：樹在牆後、他們在院子中間背對鏡頭（她不露臉）；樹後的唐萬金、籬笆外的鄭伯與秦霜、屋門口的小禾都不寫（不描述畫外的人）；『乾葉滾過兩人之間』交給音效"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e030-r2/script.md`（c01–c41 對應 s01–s41；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-17）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e021-e030.md`（拍法 1–30 條）。第 3 篇章〈搶親〉第十集、**篇章最後一集**。",
    "- 內部工作編號 930（`hailuo/{ff,clips}-dh-e930.json`、`colab/runs/e930/extras.json`、`colab/runs/e930-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e930-dh/`）；發布 slug `zhong-tian-qu-qi-e030-r2`。不放集數、不放片名卡；s01 接第 29 集 s35（接點 29→30：同一刻，唐萬金停在一步外）；s41 交給第 31 集（接點 30→31：同一刻，井在前右、阿令右手一桶水、面巾掛在左耳，魏少卿在後牆院門口）。",
    "- 照第 29 集審稿後的寫法一開始就照做：`OFFSCREEN_SPEECH = False`；背影、耳語、系統與心裡話的鏡，每張朝鏡頭的臉都寫不說話、嘴閉著；**對畫外的人說話寫「朝畫左／右外看不到的人」，那一側到邊緣只有景、畫面裡只有他一個人，不點名、不描述不在畫裡的人**（提示詞與精修文字都一樣）；掛著的東西不點名；不寫 open；道具與接觸寫在第一格；紙一律空白、婚書只見紙背；寫人數。",
    "- **唐小棠不露嘴說話、不露臉**（拍法 3）：她的五句（s02、s08、s14、s28、s33）與好感那一鏡（s20）全從背後拍、畫面正中、正背對鏡頭、頭不動、剛好兩顆丸子；最後的全景（s41）小小的背影；spec 拿掉她的圖與身分句。算盤本集不拍（拍法 20：只在插鏡；s33 的「喀」是音效）。",
    "- **魏少卿**扇子一直合著（拍法 30）；s26、s30、s34、s37、s40 不笑（撤婚、認出阿令是他輸的鏡）。**唐萬金**第一場哭、s25–s29 不笑（原版必修：說抵押時仰頭大笑），s35 可以笑。**鄭伯**照聖經跟唐萬金同鏡耳語（s24，高瘦，手擋著嘴、錄音）。**阿令**：s09 起戴面巾（送 `aling-veil-portrait-l1`），s38、s39、s41 第一格面巾已吹到左耳那一邊（送沒面巾的定妝照；拍法 21）。",
    "- **場景圖說了算**（拍法 29，協調者 2026-11-17 決定，每張放大看過）：廣場沿用第 29 集午後的 `-pm-you-wu-l1`、`-pm-shu-l1`；院子是聖經挑定的 `set-xujia-yuan-dong-l1`（柿子樹光禿；井在前右、院門在後牆中間、屋與柴堆在左），**免費修圖與裁切七張**：`set-xujia-yuan-dong-qing-l1`（塗掉屋牆上的空白木板、門楣的小紅點、樹上兩片像吊牌的葉子）與它的 `-men-l1`、`-jing-l1`、`-wu-l1`、`-qiang-l1`、`-shu-l1`、`-di-l1`（見 refs-live README）；**審稿後**再塗掉草頂上十顆橘色小圓球成 `set-xujia-yuan-dong-qing2-l1`，重裁 `-men2-l1`、`-wu2-l1`，全景、院門口、屋前各鏡改送這三張（新 id；牆外麥田的橘色小花照舊）。圖上沒有柿子樹下的矮木桌與長凳：不寫，唐萬金站著、帳本與碗拿在手上。**不需要試鏡**。",
    "- 長鏡要買的秒數（BUY）：照錄音核過（見 `r2.py` 的 BUY 註解）：s10、s15、s21、s30、s41 買 8 秒；插鏡 s17、s22、s32、心裡話 s21b、懸念句 s40 與無台詞的 s09、s38、s39 買 5 秒；其餘 6 秒。稿子 c21 三句錄音 10.11 秒，拆成 s21／s21b。**s28 剪接用降調的新檔** `audio/zq930a28-p79.wav`（唐小棠背影、放的就是錄音；formant 保留，325→257 Hz，帶上下文聽寫 r1.00；`video.json` 的台詞 id 照舊）。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音的人聲長度為準。",
    "- **獨立審稿後的修改**（`writer-tools/e030-r2/review.md`，協調者 2026-11-17 代站主決定；必改 5 條全照改）：(1) s38、s39、s41 面巾寫成實物：一條長長的半透明灰紗只掛在左耳的細繩上、尾端被風吹到左頰與左肩外，鼻口下巴第一格就露著；(2) s38（與 s09）改腰以上中景、井沿在畫面下緣、手與桶第一格就在框裡；(3) s17、s22、s32 插鏡的 d1 不寫院子地點句（`mkspec.py` 拿掉；`video.json` 只為了讓 gen-dh 送院子圖而留著），改從（稍）上方往下拍、背景只有黃土地鋪到四邊；(4) s37 井邊的女子只留被右緣切掉的肩背與髻的後面、整個人轉向院門，不寫耳朵與面巾細繩；(5) s41 句子拆開：左邊許硯、他右邊唐小棠的背影，阿令身體轉向院門、左側臉。建議照收：草頂橘點塗掉（新圖三張）、s20 腰以上兩手背後一絞、s24 鄭伯在畫左手攏在嘴與唐萬金耳朵之間、s25 帳本左手夾左腋、s08 帳本換右臂左手拉袖、s31 扇子垂在魏少卿身側、s06 車門句、s27 攤平的手掌、精修文字的說話視線換成 d1 的方向句。",
    "- **錄音**：片中原聲為主；s28 剪接用 `zq930a28-p79.wav`；備援 s18 `a17-p75`、s29 `a29-p84`、s23 `a23-p126`（從 1.20 秒起放，切掉「哈哈」）、s31 留原錄。精修前人耳聽 a28-p79、a23-p126、a29-p84 三支。",
    "- **馬**：本集只用文字寫一匹（s36）。挑片後從 s36 選定那支截一格最乾淨的馬頭頸，存成 `prop-zaohongma-head-l1`；全身的馬（棗紅、白）是第 4 篇章試鏡的項目，站主到時候決定。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯（l1、angle-a；帶笑的 angle-b 整集不送；全景只送 l1）、唐萬金 l1、魏少卿 l1、鄭伯 l1、秦霜 l1、小禾 l1、阿令（s09 面巾 `aling-veil-portrait-l1`、不送角度圖；s38、s39、s41 `aling-portrait-l1`）。唐小棠整集不送圖。s37 前景井邊的女子背影不送圖。場景見上面。",
    "- 共用檔：沒有改（`build-r2.py` 的 `EN` 已有每個名字）；e910–e929 照位元組重建不變。`gen-dh.mjs`、`pilot.py`、`cast.json` 不動；`refs-live` 加十張免費圖（都是新 id；審稿後的三張 `-qing2-l1`、`-men2-l1`、`-wu2-l1` 另寫一段）與 README 段落。鄭伯的微胖、唐萬金的笑眼、魏少卿的笑與玉冠、小禾抱著草兔子由 `colab/runs/e930/extras.json` 換掉（阿令的面巾不放 extras：只有 s09 戴，由 spec 逐鏡加）；精修文字的 CG 立領句與唐小棠的名字由本檔結尾的 `live_clips()` 在 build 後從 `clips-dh-e930.json` 換掉。",
    "- `colab/runs/e930/extras.json`（照第 29 集）與 `colab/runs/e930-live/spec.json`（`mkspec.py` 產生；種子 9301101／9301102）。",
    "- 免費準備：scratchpad `prep930.sh`（照 `prep929.sh` 審稿後的順序：先把精修句拆成錨點的形式給第一段、再把 live 文字放回；`DRY=1 … st1-ep.sh 930` → `pilot.py` → `retake.py` → `colab-jobs.json` 加 output_path、套 swap_pictures（絕對路徑）→ 逐鏡查送的場景圖與人物圖 → 精修用的分隔句 → `preflight-prompts.py` → 否定名詞、會長字的名詞、掛著的東西、open、『畫外的年輕女子』、『點名的畫外人』與精修句外漏掃描）。",
    "- 配樂：第一場溫暖又不安的弦（接第 29 集），s03 一個停頓；院子暖的家常 cue，s17–s21 轉甜，s24 耳語整段收掉，s25–s30 低沉的弦，s31 撕婚書一個大重音、回到暖 cue；第三場只剩風聲，s38 一個極輕的高音，s40 一個沉的大重音。音效見 script.md〈音樂與音效〉（另外：母雞拍翅、算盤「喀」、扇子收起、乾葉滾過土，都交給音效）。",
]

# Long shots: seconds to buy. Measured 2026-11-17 against the 37 kept recordings (~/mokaair-work/videos/zhong-tian-qu-qi-e930-dh/audio;
# wave length and silencedetect -35 dB speech span, scratchpad span930.sh; e013's test as e928, e929: a shot holds (buy - 0.3) x 1.1 s
# of speech, half a second between lines, so 5 s holds 5.17 s, 6 s 6.27 s, 8 s 8.47 s). faster-whisper medium read every take back,
# one clip per process, numpy input, once plain and once with the previous line and the line as context (audio/fw930.txt,
# fw930-retake.txt, fw930-pitch.txt; audio/README-retakes.txt). c21's three recordings run 3.35 + 0.5 + 2.28 + 0.5 + 3.48 = 10.11 s
# (over about 10 s): split into s21 (the system's two lines, 6.13 s) and s21b (his thought, 3.48 s), as e928 c15. No other shot runs
# over about 10 s.
# 8 s: s10 (a09 Wei Shaoqing's drawl, 7.64 s), s15 (a14 6.44 s), s30 (a30 6.32 s), s21 (6.13 s: the script's 長鏡 c21, two system
#      lines and the panel), s41 (the episode's and the arc's last shot: the hook needs a held tail, as e923-e929).
# 6 s: every other speaking shot; the tightest: s05 (a05 6.20 s), s23 (a23 5.92 s), s35 (a34 5.80 s), s34 (a33 5.76 s), s37 (a36
#      5.76 s), s25 (a25 retake 5.64 s), s01 (a01 retake 5.40 s).
# 5 s: the inserts s17 (a16 4.08 s), s22, s32; s21b (a22 3.48 s); s40 (a37 2.72 s: the hook line, the shot is the freeze); the
#      no-line shots s09, s38, s39.
# The cut uses audio/zq930a28-p79.wav for s28 (Tang Xiaotang from behind: the recording is what plays; take1 325 Hz sat 4.4
# semitones over her same-scene a08 203, a13 253, a32 238; the retake was no better, 326 Hz): rubberband=pitch=0.79:formant=preserved,
# 257 Hz, 3.77 s, context r1.00. video.json keeps the line id zq930a28 (a line has no file field). The on-screen speakers' clip
# voices are primary; backups lowered or raised with formants kept, if a recording is ever used: zq930a17-p75 (Tang Wanjin, 233 ->
# 178 Hz), zq930a29-p84 (205 -> 174), zq930a31-p71 (243 -> 177; his shout next to her a32 238), zq930a23-p126 (Wei Shaoqing 82 ->
# 116 Hz); each read r1.00 in context except a23 (its leading 哈哈, in every take, r0.86).
BUY = {"s10": 8, "s15": 8, "s21": 8, "s30": 8, "s41": 8, "s17": 5, "s22": 5, "s32": 5, "s21b": 5, "s40": 5, "s09": 5, "s38": 5, "s39": 5}


# ---- the refine text (e022 review 必改 12, as e023-e029): hailuo/clips-dh-e930.json column 0 is the motion text
# refine-prep.py sends with a picked d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era "Tang
# Xiaotang's high stand-up collar stays closed at her throat." and names her in "<names> shown in <Picture 1>"; in a back shot
# that draws the collar back and turns her face to the lens. Her shots are all back shots: the sentence goes and her name becomes
# "the young woman seen only from behind", and "keeps the same face, hair, costume and props" of a back shot alone becomes
# "keeps the same hair, costume and props as the first frame, her back to us" (with someone else: "..., the young woman's back to
# us"). Column 1 is recomputed. prep930.sh hands stage 1 the anchor form (anchor_form(), e028 review 必改 1).
COLLAR = "Tang Xiaotang's high stand-up collar stays closed at her throat. "
# review 建議 10: gen-dh's speaking gaze names "the person he/she is speaking to", who is not in the frame of these shots; the
# refine text gets d1's direction (colab/runs/e930-live/mkspec.py, the same words). anchor_form() puts gen-dh's words back for
# stage 1, whose d1 prompts mkspec.py edits from them.
GAZE_GEN = {"he": "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person",
            "she": "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"}
_L = "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"
_R = "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"
GAZE_REFINE = {
    "s01": _L, "s03": _L, "s04": _R, "s05": _L,
    "s06": "his face three-quarter to screen right toward the carriage at the right edge of the frame, his eyes on it",
    "s10": _R, "s12": "his eyes on the chipped rim of the bowl in his hands",
    "s15": _L, "s16": _R, "s18": _L, "s19": _R, "s23": _L, "s26": _L, "s27": _R, "s30": _L,
    "s34": "his eyes on the earth at his feet, his face turning away toward the right edge of the frame",
    "s40": "his face three-quarter to screen right toward the well beyond the right edge of the frame, his eyes on it",
    "s11": "her face turned up three-quarter to screen right toward someone out of sight beyond the upper right edge of the frame, her eyes on that spot",
    "s36": "her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, her eyes on that spot",
}
BACK_NAME = "the young woman seen only from behind"


def live_clips(path):
    import hashlib
    import json
    import re
    clips = json.load(open(path, encoding="utf-8"))
    for key, row in clips.items():
        text = row[0]
        if COLLAR in text:
            text = text.replace(COLLAR, "")
            m = re.search(r"\[Shot 1\] 3D CG\. (.+?) shown in <Picture 1> (keeps?) ", text)
            names = [n for n in m.group(1).split(" and ") if n != "Tang Xiaotang"]
            who = " and ".join(names + [BACK_NAME])
            who = who[0].upper() + who[1:]
            verb = "keep" if names else "keeps"
            text = text.replace(m.group(0), f"[Shot 1] 3D CG. {who} shown in <Picture 1> {verb} ", 1)
            if names:
                text = text.replace("keep the same face, hair, costume and props as the first frame", "keep the same face, hair, costume and props as the first frame, the young woman's back to us", 1)
            else:
                text = text.replace("keeps the same face, hair, costume and props as the first frame", "keeps the same hair, costume and props as the first frame, her back to us", 1)
            assert "back to us as the first frame" not in text and ("back to us" in text), key
            assert "Tang Xiaotang" not in text, (key, "her name is left in a back shot's refine text")
        sid = key.split("-", 1)[1]
        if sid in GAZE_REFINE:
            pr = "she" if sid in ("s11", "s36") else "he"
            assert text.count(GAZE_GEN[pr]) == 1, (key, "speaking gaze")
            text = text.replace(GAZE_GEN[pr], GAZE_REFINE[sid])
        text = text.replace("Constable Zhao", "Zhao Butou")
        assert "stand-up collar" not in text and "onstable" not in text, key
        row[0] = text
        row[1] = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    open(path, "w", encoding="utf-8").write(json.dumps(clips, ensure_ascii=False, separators=(",", ":")))


# e928 review 必改 1: ref2manifest.mjs (stage 1 of prep930.sh) strips gen-dh's refine anchor with ANCHOR_FF, and the back-shot
# wording live_clips() writes no longer matches it. prep930.sh hands stage 1 the anchor form of the live file (this), then puts
# the live file back; the refine text (clips-dh) keeps live_clips()'s wording.
def anchor_form(text):
    text = text.replace(", the young woman's back to us; the set layout stays as it is.", "; the set layout stays as it is.")
    text = text.replace("keeps the same hair, costume and props as the first frame, her back to us; the set layout stays as it is.",
                        "keeps the same face, hair, costume and props as the first frame; the set layout stays as it is.")
    assert "back to us; the set layout" not in text
    for g in sorted(set(GAZE_REFINE.values()), key=len, reverse=True):
        text = text.replace(g, GAZE_GEN["she" if g.startswith("her ") else "he"])
    return text


def anchor_form_file(src, dst):
    import json
    clips = json.load(open(src, encoding="utf-8"))
    for row in clips.values():
        row[0] = anchor_form(row[0])
    open(dst, "w", encoding="utf-8").write(json.dumps(clips, ensure_ascii=False, separators=(",", ":")))


if __name__ == "r2spec":
    import atexit
    import os
    atexit.register(live_clips, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hailuo", f"clips-dh-e{EP}.json"))
