"""Episode 29 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e029-r2/script.md
(c01-c35 = s01-s35; the CG-era r2 script), including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and
「真人版的改動（2026-11-17）」, which override the tables. Every line is the script's, word for word; only the staging changes.
Bible: production/r2-bible-e021-e030.md (rules 1-30, the 28->29 and 29->30 hand-overs, the props, people and picture tables).
The ninth episode of arc 3 〈搶親〉: the town square at noon on the thirtieth day (the same moment as e028 s39), then the same
square in the afternoon, when the Tang carriage arrives.

Written from the start the way e028-r2/r2.py stands AFTER its independent review (../e028-r2/review.md: the 13 必改 and the
建議 the coordinator took), with what the pickers caught in e924-e927 and the lessons in the task file (e921-e925):
- OFFSCREEN_SPEECH = False (rule 15): every shot with an off-screen line, a thought or a system line writes the silence of each
  person on screen (quiet(), SILENT_HE). Where Tang Xiaotang speaks from behind, every face toward the camera "says nothing ...
  lips pressed together"; no word that invites a smile on a listener unless the script lets him smile.
- A line said to someone outside the frame is written "toward someone out of sight beyond the left/right edge of the frame",
  that side is set only (sky, branches, roofs, earth) all the way to the edge, and the speaker is the only person in the frame.
  No person who is not in the first frame is named or described anywhere, in the prompts or in the refine text (e925 lesson;
  e927 必改 5; e928 必改 3): the gaze names a place ("the platform beyond the upper left edge", "the road beyond the right edge").
- Tang Xiaotang never speaks on camera and never shows her face (rule 3): her nine lines on screen (s02, s14, s16, s24, s26, s27,
  s30, s33, s35) are all from behind, in the middle of the frame, "facing straight away from us", head still, exactly two round
  buns (TBACK; nospeak; spec drops her pictures and identity sentence); her two off-screen lines (s15, s28) are inserts of her
  hand. The script's 高立領, 「下巴以上」 and 「襦裙從立領到腰一件闔上」 are CG wording and are not used (rule 4). Her abacus is not
  in this episode (rule 20). The script's c14 climb onto the platform is not shot: she stays below the platform's left side
  (set-guangchang-zuo-l1, as e028 s34) and raises the ledger toward the platform; the chest beside her is the sugar chest of c26.
- Magistrate Hu always wears the winged hat (HU); the gavel is GAVEL; he leaves at c25 (scene 1) and is never in a shot with Sun
  Zhanggui (s20, s23) nor in scene 2 with Tang Wanjin (bible 同框撞臉). The two rows of yamen men, their staves, the two men who
  take Hu down and the old woman's crowd are sounds or left out (rules 16, 17, 25); s23's two men are two plain black cotton
  sleeves gripping Sun's arms from the edges (no face, no office word).
- Wei Shaoqing (rule 30): the fan is always closed (FAN); c08's 「摺扇打開、搧兩下、翹腳」, c13's 「啪地收扇」 and c31's 「慢慢打開扇子」
  become taps of the closed fan. Rule 30 marks e029 as a losing episode: c22 (he drops Sun) is NOSMILE; the script's own smiles
  before the turn (c08 「本鏡可以笑」, c13 冷笑 half gone) and c31 (still sure of his father-in-law, 「本鏡可以笑」) are kept.
- Name only what should be drawn (rules 7, 17, 27, 28): the packets PACKET (plain white paper; the script's small red circle on the
  corner is not drawn: a mark on paper grows a character, and the ledger's 編號 is the line's), the cakes CAKE on TRAY, the yellow
  paper YPAPER, the ledger STACK (its pages blank; c15's 格線與紅圈 not drawn), the silver INGOT top-up (c21's underside with the
  square frame is not shown, as e028 s10), the strips STRIPS, the money POUCH. No word "open" anywhere; no hung thing named.
- c10 is the bible's one exception (rule 27): the sheet against the sun with the willow leaf, from the new free crop
  prop-liuye-zhi-xin-l1 (the paper only: the light stand, the camera rig, the crowd and the two hands of prop-liuye-zhi-l1 cut
  off; the remake task's follow-up "crop prop-liuye-zhi-l1 before e029"). c11's yellow sheet gets its own free picture
  prop-huangzhi-l1 (a leaf-free corner of the same sheet, tinted yellowish with Pillow, with lumpy fibres and dark specks):
  a paper insert with no picture of its own would take the square's set picture and grow a square behind it.
- Xu Yan: the script's sugar crumbs at his mouth (c03-c07) are not written (rule 12: nothing small on the skin); c04's 「抿一下嘴」
  stays. No blue light (rule 11): the panels (s29) are the editor's.
- The carriage (rule 26): "the black lacquered carriage body and the head and neck of one horse at the right edge", hooves as
  sounds; Steward Zheng (zhengbo-portrait-l1) only in s32, never with Tang Wanjin (the script; bible allows it, not needed).
  Tang Wanjin (tangwanjin-portrait-l1): crying, never laughing (原版必修); his gold keys written as the bible says.
- Counts written everywhere (rule 25): the square's eight townspeople each in their own clothes (TOWNS, as e028 after its review),
  the afternoon line six customers each in their own clothes (CUSTOMERS).
- One visible action per shot, props and contacts in the first frame; the script's pans, tracks, follows and the high-angle wides
  are slow push-ins at eye level (the pictures are level).

THE AXES (rule 29: the set picture decides; as e028's square):
- The square: the low stone platform in the middle with its steps toward us; the red desk at its back (Magistrate Hu behind it),
  the dark wooden armchair on its RIGHT (Wei Shaoqing), the plain wooden chest (the sealed sugar chest) on the ground at its LEFT;
  Xu Yan on the LEFT of the platform, Lai San kneeling in its middle front, Tang Xiaotang on the earth below its left side by the
  chest, Sun Zhanggui below its right side. Xu Yan looks screen right to the desk; Hu and Wei look screen left to Xu Yan; Lai San
  looks screen left to Tang Xiaotang and points to the lower right (Sun); Sun looks up to the upper left (the platform).
- The afternoon: the stall beside the chest on the LEFT; Wei still on the platform beside the armchair; the carriage comes in from
  the RIGHT (the long tiled building of set-guangchang-you-wu-l1); Tang Wanjin runs toward screen left; Tang Xiaotang and Xu Yan
  face screen right toward him.

PLACES (the coordinator's decisions, 2026-11-17; every picture looked at full size; script.md 〈真人版的改動〉): gen-dh's SET
phrase "town square" gives set-guangchang-l1; spec.json swaps it for the picture below with an absolute path.
- Noon (scene 1), e028's free pictures: set-guangchang-tai-l1 (the wide: s05, s12), -tai-zhong-l1 (the platform, made for e029:
  s01), -shu-l1 (the bare tree and the sky: the low-angle shots s03, s04, s06-s09, s13, s16-s19, s22, s24, s25), -zuo-l1 (below
  the platform's left, the chest: s02, s14, s26), -you-wu-l1 (below its right, the long building: s20, s23); and three new
  free pictures: set-guangchang-an-l1 (the red-draped desk with the dark block on it: s21), set-guangchang-di-l1 (the packed earth
  with tree shadows: s15), prop-liuye-zhi-xin-l1 (s10), prop-huangzhi-l1 (s11).
- Afternoon (scene 2): set-guangchang-pm-l1 = the bible's free grade of the painted set-guangchang-l1 (the yellow boards painted
  as e028 did; the painted full picture matches e028's crops to 0.01 of a level) and its crops by e028's commands:
  -pm-tai-l1 (s30), -pm-zuo-l1 (the stall: s27, s29), -pm-shu-l1 (s31), -pm-you-wu-l1 (the carriage side: s32-s35), -pm-di-l1
  (s28). The grade is the bible's; the warm low afternoon sun is in the text.
- Inserts and shots with nobody named (s10, s11, s15, s21, s28) open their motion with NOBODY.
- Shared files: build-r2.py's EN gets "tangwanjin": "Tang Wanjin" (he speaks on screen in s34; gen-dh.mjs already has the name);
  e910-e928 rebuild byte for byte. refs-live gets ten new free pictures (new ids, own l1; rule 19) and a README paragraph.
"""
EP = 929  # internal working number; the published slug is zhong-tian-qu-qi-e029-r2
SLUG = "zhong-tian-qu-qi-e029-r2"
EP_TITLE = "一張紙翻案，囡囡（重製版 r2）"
OUTLINE_SECONDS = 190  # script.md: about 189.5 s, 35 shots (26 + 9)
TARGET_MINUTES = [3, 4]
TITLE = "一張紙翻案，囡囡｜種田娶妻打天下 第29集（重製版）"
DESCRIPTION = "公審台上，賴三一口咬定是許家逼他下毒。許硯不辯，當眾把一塊許記的糖霜糕吃下去；再把包糖的白紙舉向正午的太陽，紙心浮出一片柳葉，那張毒糖糕的黃紙卻什麼都沒有。唐小棠翻出許記的帳：每一批糖都編了號，那包黃紙糖從沒賣過。賴三一急說溜了嘴，許硯只問一句：昨晚那個食盒，誰送的？孫掌櫃被推出來頂罪，封條撕下，糖霜糕一個下午就賣空。鬥商總帳，許記三百三十兩、魏記一百六十五兩。魏少卿卻說日落才算數，他岳父的車就快到了——一輛大車停在廣場邊，唐萬金哭著撲下來：囡囡！《種田娶妻打天下》第 29 集（重製版）。"
THUMB = ("紙心有一片柳葉", "s10")
CHARACTERS = ["xuyan", "tangxiaotang", "laisan", "sunzhanggui", "weishaoqing", "huxianling", "zhengbo", "tangwanjin", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: the low drum of a public trial on a town square at noon, one bright chime when a willow leaf shows in sunlit paper, then rising strings, one heavy beat when a man breaks, one big release when paper strips are torn; then a bright market cue in the afternoon, one big triumphant accent at a final tally, a one-beat stop when a carriage arrives, turning into warm uneasy strings; ancient Chinese rural drama, no vocals"

# Places. gen-dh SET takes the FIRST pattern in its list order that the whole prompt matches: every prompt says "town square"
# (never "yamen", "market street", "tavern", "examination").
SQ = ("a wide square of packed pale earth; in the middle one low square platform of grey stone slabs with a few steps up its "
      "front, one long desk draped in red cloth on it and one dark wooden armchair at its right side; one plain wooden chest "
      "standing on the ground at its left; two bare trees, and low tiled buildings and white walls all round")
NOON = "hard bright low winter sun from the upper right behind, long shadows falling to the left across the earth"
PM = "warm golden low afternoon sun from the upper right behind, long shadows stretching far to the left across the earth"
LOC = {
    "square": f"In the town square of the county town at noon on a cold clear winter day: {SQ}; {NOON}",
    "square_p": f"In the town square of the county town at noon on a cold clear winter day: the low square platform of grey stone slabs with a few steps up its front, one long desk draped in red cloth on it, one dark wooden armchair at its right side and one plain wooden chest on the ground at its left, the low tiled hall and white walls beyond; {NOON}",
    "square_c": "In the town square of the county town at noon on a cold clear winter day, the bare branches of a tree and the low tiled roofs against the clear blue sky, hard bright low winter sun from the right",
    "square_l": f"In the town square of the county town at noon on a cold clear winter day, on the packed pale earth below the left side of the low stone platform, one plain wooden chest beside it, the low tiled buildings beyond; {NOON}",
    "square_r": f"In the town square of the county town at noon on a cold clear winter day, on the packed pale earth below the right side of the low stone platform, the long low tiled building with its plank doors beyond; {NOON}",
    "square_e": "In the town square of the county town at noon on a cold clear winter day, low over the packed pale earth with the long thin shadows of bare branches across it, hard bright low winter sun",
    "square_d": "In the town square of the county town at noon on a cold clear winter day, close over the long desk draped in red cloth on the low stone platform, hard bright low winter sun",
    "square_s": "In the town square of the county town at noon on a cold clear winter day, up against the hard bright low winter sun in the clear blue sky",
    "pm": f"In the town square of the county town in the afternoon of the same cold clear winter day: {SQ}; {PM}",
    "pm_l": f"In the town square of the county town in the afternoon of the same cold clear winter day, on the packed pale earth beside the left side of the low stone platform and the plain wooden chest, the low tiled buildings beyond; {PM}",
    "pm_r": f"In the town square of the county town in the afternoon of the same cold clear winter day, on the packed pale earth at the edge of the square before the long low tiled building with its plank doors; {PM}",
    "pm_c": "In the town square of the county town in the afternoon of the same cold clear winter day, the bare branches of a tree and the low tiled roofs against the clear sky, warm golden low afternoon sun from the right",
    "pm_e": "In the town square of the county town in the afternoon of the same cold clear winter day, low over the packed pale earth, warm golden low afternoon sun",
}
LIGHT = {
    "noon": "the hard winter sunlight stays unchanged",
    "pm": "the warm low afternoon sunlight stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_D = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves down"
LAI_B = ("Lai San, small and thin, in his checked grey-brown cross-collared short jacket, a coarse grey cloth apron tied at his "
         "waist, an old cloth head wrap below his topknot, both his hands tied together before him at the wrists with a strip of "
         "his own grey cloth sash")
WEI = ("Wei Shaoqing, in his sapphire-blue brocade robe woven with gold thread, a white jade pendant at his waist, a small green "
       "jade ornament at the front of his topknot")
FAN = "one closed folding fan in his right hand, its dark bamboo ribs pressed tight together like a short slim stick"
HU = "in his black gauze futou hat with two short stiff flat wings and his blue-green round-collared official robe"
GAVEL = "one flat oblong block of dark polished wood the size of half a brick, plain on every side"
SUN = ("Sun Zhanggui, tall and lean with a long narrow face and a thin grey-streaked beard, in his green satin robe with a jade "
       "belt hook")
ZHENG = ("Steward Zheng, tall and thin with a slight stoop, a long lined face, a neat grey-white goatee and a thin moustache, grey "
         "hair in a small topknot bound with a black cloth band, in his dark brown satin long robe")
TWJ = ("Tang Wanjin, a little plump, with a round ruddy face, a short black moustache and a short black goatee, a small gold crown "
       "on his topknot, in his deep purple silk robe woven all over with small gold ingot shapes, a string of small gold keys at "
       "his waist")
CARRIAGE = "the black lacquered carriage body and the head and neck of one horse at the right edge"
INGOT = "one small silver ingot, its top smooth and plain"
STACK = "one thick stack of plain blank paper sheets stitched along one edge with cord"
YPAPER = "rough blank yellowish paper"
PACKET = "one small packet of plain blank white paper"
CAKE = "one small square white cake"
TRAY = "one round flat bamboo tray with one more small packet of plain blank white paper on it"
STRIPS = "two crossed strips of plain blank white paper pasted over its lid"
POUCH = "one plain brown cloth money pouch tied at its neck"
TANG_HAND = "a slender hand in a peach-pink silk sleeve cuff"
TOWNS = ("eight townspeople in Song-dynasty cotton robes and head cloths, standing in a loose line behind a rope, each dressed "
         "differently: an old man in a brown robe, a woman in a dull blue jacket and long skirt, a young man in a dark blue "
         "short jacket, a stout man in an indigo robe, a woman in a faded green jacket, a thin old woman in dark brown, a boy in a patched "
         "tan jacket and a man in an ochre robe")
CUSTOMERS = ("six customers in a short line facing us, each dressed differently: an old man in a brown robe, a woman in a dull "
             "blue jacket and long skirt, a stout man in an indigo robe, a woman in a faded green jacket, a boy in a patched tan "
             "jacket and a man in an ochre robe")
# the platform as it stands in scene 1 (hand-over 28->29: e028 s39), for the wides
STAGE = ("beyond them on the low stone platform, small: Magistrate Hu, " + HU + ", sitting behind the long desk draped in red "
         "cloth, his lips closed, never the lens; in the middle front of the platform the back of one small thin man in a checked "
         "grey-brown jacket kneeling, his tied hands lowered before him, unnamed; in the dark wooden armchair on the right of the "
         "platform Wei Shaoqing, small, in his sapphire-blue brocade robe, sitting back with his closed fan on his knee, his lips "
         "closed, never the lens")
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# e924 fix1's back-of-head wording, as e925-e928
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with every strand of her black hair "
         "combed smooth and gathered up into just two round buns set high on her head, one bun on each side, one short pink "
         "silk ribbon wrapped around each bun, the nape of her neck bare and clear above a pink inner collar, and her light "
         "peach-pink silk shoulders; the back of her head facing straight away from us the whole time, her head still, her ear "
         "the furthest round her head we ever see")
HEADSTILL = "the young woman with the two high round buns keeps her head still, facing straight away from us, the back of her head toward us the whole shot"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def only_tang():
    return "she is the only young woman with two high round buns in the frame"


def alone(rest, where, frame="framed from the waist up", shot="medium shot"):
    """Tang Xiaotang from behind, in the middle of the frame (not at an edge: the pickers' cheek at the frame edge)."""
    return f"{shot} from close behind {TBACK}, {where} in the middle of the frame, {frame}, facing straight away from us; {only_tang()}; {rest}"


SHOTS = [
    # ---- scene 1: the thirtieth day at noon, the town square (28->29: the same moment as e028 s39).
    dict(chapter="公審台上", loc="square_p", cam="Medium shot, slow push in", chars=["xuyan", "huxianling", "weishaoqing"], night="noon",
         comp=f"medium shot at standing eye height, like the picture, the low stone platform filling the frame: at the left end of the long desk draped in red cloth {XU_D}, standing, framed full figure, {PACKET} already folded back flat on his left palm from the first frame with {CAKE} on it, his face three-quarter to screen left toward the square below the platform, never the lens; calm and level, not smiling: steady eyes, lips moving evenly between words; on the desk {GAVEL} and {TRAY}; behind the desk Magistrate Hu, {HU}, sitting, framed from the waist up, his face turned toward Xu Yan, his lips closed, never the lens; in the middle front of the platform the back of one small thin man in a checked grey-brown jacket kneeling, his tied hands lowered before him, unnamed; in the dark wooden armchair on the right of the platform {WEI}, sitting back, small, his lips closed, never the lens; {HANDS}; exactly four people",
         lines=[("xuyan", "許記的糖有沒有毒，我先吃給大家看。", "平靜")],
         motion="Xu Yan lifts the white cake from the paper with his right hand and holds it up toward the square as he speaks; Magistrate Hu, the kneeling man and Wei Shaoqing stay still",
         zh="中景、慢推（人眼高、照圖；送免費圖 `set-guangchang-tai-zhong-l1`：台子、紅布案、木椅、木箱，第 28 集為本集做的；接點 28→29 同一刻）：許硯站在紅布案左端，左手掌上第一格已經攤著拆開的白紙包與一塊方方的白糖霜糕，右手拿起糖糕朝台下舉起、平靜地說；案上長方形驚堂木與一只圓竹盤（上面還有一包白紙包）；案後胡縣令（有帽翅的黑紗幞頭）、台中央賴三跪著的背影（不點名、不送圖）、台右木椅上的魏少卿都不動、嘴閉著。稿子『紙角一個小紅圈』不畫（紙上的記號會長字，拍法 7、27；『帳上有編號』由台詞說）；『走到公案前、打開紙包』在第一格已經完成（一鏡一個動作）"),
    dict(loc="square_l", cam="Close-up from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="noon",
         comp=alone(f"{STACK} already held against her chest in both arms from the first frame, only its pale edge showing at her sides; beyond her, soft, the edge of the low stone platform and the plain wooden chest beside it in the hard winter sun; {HANDS}",
                    "standing on the packed pale earth below the left side of the platform,", frame="framed from the shoulders up", shot="close-up"),
         lines=[("tangxiaotang", "你瘋啦？萬一那包也被人動過手腳呢？", "嚇白了臉")],
         motion=f"her arms hug the stack of paper tighter against her chest; {HEADSTILL}",
         zh="近景（從背後）、慢推（送 `set-guangchang-zuo-l1`：台子左下的地面與木箱，同第 28 集 s34）：唐小棠的後腦與肩在畫面正中、正背對鏡頭、頭不動、剛好兩顆丸子，兩臂把帳本（縫邊的空白紙疊）抱緊（nospeak，拍法 3；她的圖與身分句由 spec 拿掉）。稿子『下巴以上、抬頭、往前探身』改背影、頭不動"),
    dict(loc="square_c", cam="Close-up, slow push in", chars=["xuyan"], night="noon",
         comp=f"low-angle close-up of {XU_D}, standing on the platform, framed from the chest up with space above his head, his cheek already full from the first frame, his right hand lowering from his mouth, his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; that side of the frame is only the bare branches and the clear blue sky all the way to the edge, and he is the only person in the frame; calm and sure, not smiling: steady eyes, lips moving evenly between words; behind him the bare branches of a tree and the clear blue sky",
         lines=[("xuyan", "這包是封鋪那天從許記櫃上收走的，帳上有編號。", "嚼完")],
         motion="Xu Yan swallows the cake hard once and then speaks evenly",
         zh="低角度近景、慢推（送禿樹與晴空的裁切 `set-guangchang-shu-l1`）：許硯第一格嘴裡已經含著整塊糖糕、右手從嘴邊放下，用力吞一下再平靜地說，朝畫左外看不到的人（唐小棠，不點名；那一側到邊緣只有樹枝與晴空）。稿子『塞進嘴裡、嚼兩下、手背抹嘴』只拍吞下（一鏡一個動作）；嘴角的糖屑不寫（拍法 12：皮膚上不寫細小東西）"),
    dict(loc="square_c", cam="Close-up, slow push in", chars=["xuyan"], night="noon",
         comp=f"close-up of {XU_D}, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes level on a spot beyond the left edge of the frame, never the lens; he is the only person in the frame; cool and unbothered: eyes steady, brows level, lips pressed shut; behind him the bare branches of a tree and the clear blue sky",
         lines=[("xitong", "宿主當眾試毒。系統不提供解藥。", "冷"),
                ("xuyan", "我自己做的糖，用不著解藥。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan's eyes settle and he presses his lips together once; {SILENT_HE}; he is listening and thinking, not speaking",
         zh="近景、慢推（送禿樹與晴空的裁切；拍法 11 不寫藍光）：許硯眼神一定、抿一下嘴（稿子『抿一下嘴』照寫，糖屑不寫）；全程嘴閉著（系統一句、心裡話一句：本集的鬥嘴）"),
    dict(loc="square", cam="Wide shot, slow push in", chars=["huxianling", "weishaoqing", "xuyan"], night="noon",
         comp=f"wide shot at standing eye height, like the picture: in the soft foreground, seen from behind and out of focus, {TOWNS}, their arms already raised from the first frame; {STAGE}; on the left side of the platform {XU_D}, standing, framed full figure, his hands at his sides, his face three-quarter to screen right, never the lens; calm and well, not smiling: level eyes, lips pressed shut; {HANDS}; exactly twelve people",
         motion=f"the eight townspeople slowly lower their raised arms and fall still, their heads tipping up toward the platform; the people on the platform stay still; {quiet('Magistrate Hu, Wei Shaoqing and Xu Yan', 'their', plural=True)}",
         zh="全景、慢推（人眼高、照圖；送廣場寬景裁切 `set-guangchang-tai-l1`）：前景虛焦八個背對的鎮民（各穿不同的衣服，拍法 25）第一格舉著手，慢慢放下、靜下來、抬頭看台上；台上胡縣令在紅布案後、賴三跪著的背影、魏少卿坐在台右木椅上（同第 28 集 s39 的站位）、許硯站在台左，好好的，都不動、嘴閉著（無台詞）。稿子的高角度搖鏡改人眼高慢推（圖是平視）；衙役放低水火棍不拍（拍法 16、17；音效）"),
    dict(loc="square_c", cam="Low-angle close-up, slow push in", chars=["huxianling"], night="noon",
         comp=f"low-angle close-up of Magistrate Hu, {HU}, sitting behind the long desk draped in red cloth, framed from the chest up with clear space above his hat, his right hand already gripping {GAVEL} raised a hand's height above the red cloth from the first frame, his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; that side of the frame is only the bare branches and the clear blue sky all the way to the edge, and he is the only person in the frame; impatient, not smiling: brows pulled down, mouth drawn long between words; behind him the bare branches of a tree and the clear blue sky",
         lines=[("huxianling", "吃一塊算什麼！賴三指的是你，你還有何話說？", "不耐煩")],
         motion="Magistrate Hu brings the wooden block down hard on the desk with one loud knock and speaks",
         zh="低角度近景、慢推（送禿樹與晴空的裁切）：胡縣令（有帽翅的黑紗幞頭、藍綠官袍）右手第一格已經舉著驚堂木（長方形木塊，原版必修），一拍、不耐煩地朝畫左外看不到的人（許硯，不點名）說。稿子『額頭冒汗』不寫（拍法 12）"),
    dict(loc="square_c", cam="Low-angle medium shot, slow push in", chars=["xuyan"], night="noon",
         comp=f"low-angle medium shot of {XU_D}, standing on the platform, framed from the waist up with space above his head, one crumpled sheet of {YPAPER} already pinched by its top corner in his right hand from the first frame, held out at his side, his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, never the lens; that side of the frame is only the bare branches and the clear blue sky all the way to the edge, and he is the only person in the frame; cool and clear, not smiling: steady eyes, lips moving clearly between words; behind him the bare branches of a tree and the clear blue sky; {HANDS}",
         lines=[("xuyan", "人證會改口，紙不會。這張，是包那塊毒糖糕的紙。", "平")],
         motion="Xu Yan gives the crumpled yellowish sheet one sharp shake so it hangs straight down from his fingers as he speaks",
         zh="低角度中景、慢推（送禿樹與晴空的裁切）：許硯右手第一格已經捏著那張揉皺的粗黃紙（空白，拍法 27）的一角，一抖讓它垂直，朝畫右外看不到的人（胡縣令，不點名）說。稿子『撥掉糖屑、從右袖抽出、一抖展開』只拍一抖（一鏡一個動作；不寫 unfold／flick）；『畫面右邊緣跪著的賴三』不拍（畫面裡只有他）"),
    dict(loc="square_c", cam="Low-angle medium close-up, slow push in", chars=["weishaoqing"], night="noon",
         comp=f"low-angle medium close-up of {WEI}, sitting in a dark wooden armchair, framed from the chest up with space above his head, {FAN}, its tip already resting on his knee from the first frame, his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; that side of the frame is only the bare branches and the clear blue sky all the way to the edge, and he is the only person in the frame; lazy and mocking: a thin lazy smile, eyes half lidded, lips moving slowly between drawled words; behind him the bare branches of a tree and the clear blue sky",
         lines=[("weishaoqing", "一張皺巴巴的破紙，能翻什麼天？", "懶懶地，本鏡可以笑")],
         motion="Wei Shaoqing taps the closed fan twice on his knee as he speaks",
         zh="低角度中近景、慢推（送禿樹與晴空的裁切）：魏少卿坐在深色木椅上，合著的扇子在膝上敲兩下，懶懶地笑（稿子『本鏡可以笑』）朝畫左外看不到的人說。稿子『摺扇打開、翹腳搧扇子』不拍（拍法 30：扇子一直合著，打開的扇面會長字）；『雕花木椅』不寫『雕花』"),
    dict(loc="square_c", cam="Low-angle medium shot, slow push in", chars=["xuyan"], night="noon",
         comp=f"low-angle medium shot of {XU_D}, standing at the front edge of the platform, framed from the waist up with space above his head, one sheet of plain blank white paper already held up at head height in his right hand from the first frame, one small folded square of {YPAPER} pinched in his left hand at his side, his face turned up three-quarter to screen right toward the white sheet and the sun, never the lens; intent and calm, not smiling: eyes narrowed against the light, lips pressed shut; he is the only person in the frame; behind him the bare branches of a tree and the clear blue sky; {HANDS}",
         motion=f"Xu Yan lifts the white sheet up high toward the low sun at the upper right, the sunlight glowing through it; {SILENT_HE}",
         zh="低角度中景、慢推（送禿樹與晴空的裁切）：許硯站在台子前緣，右手第一格已經把一張攤平的白紙舉到頭高、左手捏著摺起的粗黃紙，把白紙高高舉向畫右上的低日，陽光透過紙（無台詞，嘴閉著）。稿子『紙角一個小紅圈』不畫；『台下的臉一張張抬起來』與往上搖鏡不拍（一鏡一個主體）；剪在紙舉到最高點，接 s10"),
    dict(loc="square_s", cam="Insert close-up, slow push in", chars=[], night="noon",
         comp="insert close-up, the shot opens directly on one sheet of plain blank white paper held up against the sun, from its very first frame: the sheet fills the frame, sunlight shining through it, one faint willow-leaf shape in the middle, the soft fibres of the paper glowing; only the glowing sheet is in the frame",
         lines=[("xuyan", "許記的包糖紙，對著太陽，紙心有一片柳葉。", "畫外")],
         motion=NOBODY + "the faint willow-leaf shape in the middle of the sheet slowly grows clearer as the sunlight strengthens through it, its thin veins showing one by one",
         zh="插鏡、慢推（第一格就是對著太陽的白紙；送免費新圖 `prop-liuye-zhi-xin-l1`：`prop-liuye-zhi-l1` 只取紙的部分，燈架、攝影機、人群與兩隻手都裁掉；聖經拍法 27 唯一的例外，照聖經的固定句寫、不送人）：紙心一片淡淡的柳葉隨著陽光越來越清楚、葉脈一條條浮出來（許硯畫外的台詞放錄音）。指尖照圖不畫就不寫（拍法 27）；剪接 s09 的手接手"),
    dict(loc="square_s", cam="Insert close-up, slow push in", chars=[], night="noon",
         comp=f"insert close-up, the shot opens directly on one sheet of {YPAPER} held up against the sun, from its very first frame: the sheet fills the frame, the sunlight coming through it dull and uneven, only lumpy fibres and small dark specks scattered through it, plain all over; only the dull yellowish sheet is in the frame",
         lines=[("xuyan", "這張黃紙什麼都沒有，是魏記鋪子用的粗紙。", "畫外")],
         motion=NOBODY + "the yellowish sheet trembles a little in the light, the lumpy fibres and dark specks showing and nothing else",
         zh="插鏡、慢推（第一格就是對著太陽的粗黃紙；送免費新圖 `prop-huangzhi-l1`：同一張紙沒有柳葉的一角，用 Pillow 調成偏黃、加疙瘩纖維與黑點）：紙裡只有疙瘩一樣的纖維與黑點、什麼形狀都沒有（許硯畫外的台詞放錄音）。稿子『許硯左手的指尖在紙角』不寫（拍法 27：指尖照圖不畫就不寫）"),
    dict(loc="square", cam="Wide shot, slow push in", chars=["huxianling", "weishaoqing", "xuyan"], night="noon",
         comp=f"wide shot at standing eye height, like the picture: in the soft foreground, seen from behind and out of focus, {TOWNS}; {STAGE}; on the left side of the platform {XU_D}, standing, framed full figure, one sheet of plain blank white paper held up high in his right hand, his face three-quarter to screen right, never the lens; calm, not smiling, his lips pressed shut; {HANDS}; exactly twelve people",
         motion=f"the thin old woman in dark brown raises her arm and points up at the white sheet, and the townspeople beside her lean their heads together; the people on the platform stay still; {quiet('Magistrate Hu, Wei Shaoqing and Xu Yan', 'their', plural=True)}",
         zh="全景、慢推（人眼高、照圖；送廣場寬景裁切）：前景虛焦八個背對的鎮民，穿深褐衣服的瘦老婦人舉手指著台上的白紙，旁邊的人湊在一起（人聲交給音效）；台上同 s05，許硯右手高舉白紙，都不動、嘴閉著（無台詞）。稿子的搖鏡改慢推"),
    dict(loc="square_c", cam="Close-up, slow push in", chars=["weishaoqing"], night="noon",
         comp=f"low-angle close-up of {WEI}, sitting in a dark wooden armchair, framed from the chest up with space above his head, {FAN}, already held up before his chest from the first frame, his left palm turned up below it, his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; that side of the frame is only the bare branches and the clear blue sky all the way to the edge, and he is the only person in the frame; a cold half smirk fading from his mouth, eyes narrowed, lips moving between clipped words; behind him the bare branches of a tree and the clear blue sky",
         lines=[("weishaoqing", "粗紙滿街都買得到，憑什麼算魏記的？", "冷笑")],
         motion="Wei Shaoqing taps the closed fan once into his left palm as he speaks",
         zh="低角度近景、慢推（送禿樹與晴空的裁切）：魏少卿合著的扇子在左掌心敲一下，冷笑收掉一半，朝畫左外看不到的人說。稿子『扇子停在半空、啪地收扇』不拍（拍法 30：扇子一直合著）"),
    dict(loc="square_l", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="noon",
         comp=alone(f"{STACK} already held in her right hand at her shoulder from the first frame; beyond her, soft, the edge of the low stone platform and the plain wooden chest beside it in the hard winter sun; {HANDS}",
                    "standing on the packed pale earth below the left side of the platform,"),
         lines=[("tangxiaotang", "紙買得到，帳本買不到。大人，看許記的帳！", "脆")],
         motion=f"her right arm raises the stack of paper high above her head toward the platform, only her arm moving; {HEADSTILL}",
         zh="中景（從背後）、慢推（送台子左下的地面與木箱 `set-guangchang-zuo-l1`）：唐小棠背影在畫面正中、頭不動，右手把帳本高舉過頭、朝台上（只動手臂）（nospeak，拍法 3）；畫面裡只有她。稿子『爬上台階、站到許硯右邊』不拍：上台就得轉身面向台下，她的臉會露出來；她留在台左下、木箱邊（第 28 集 s34 的位置；木箱就是 s26 的糖箱）"),
    dict(loc="square_e", cam="Insert close-up, slow push in", chars=[], night="noon",
         comp=f"insert close-up from a low side angle, the shot opens directly on the edge of {STACK}, held level in the sun above the packed pale earth, from its very first frame, its top sheet blank and pale, {TANG_HAND} already resting one fingertip near the top of the sheet; only the stack of blank sheets, the hand and its sleeve cuff are in the frame",
         lines=[("tangxiaotang", "許記每一批糖都編了號，誰買了幾塊，一筆不漏。", "畫外")],
         motion=NOBODY + "the fingertip slides slowly down the blank sheet and stops, then taps it twice",
         zh="插鏡、慢推（第一格就是側面斜拍的空白紙疊；送免費新圖 `set-guangchang-di-l1`：只有黃土地與禿枝的長影子）：桃粉袖口的手指順著空白的頁面往下滑、停住、點兩下（唐小棠畫外的台詞放錄音）。稿子『格線與一個個小紅圈』不畫（拍法 7：紙上的記號會長字；『編了號』由台詞說）"),
    dict(loc="square_c", cam="Close-up from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="noon",
         comp=alone(f"{STACK} already held flat against her chest in her left arm from the first frame, her right hand resting on top of it; beyond her, soft, the bare branches of a tree and the low tiled roofs against the clear blue sky; {HANDS}",
                    "standing on the packed pale earth,", frame="framed from the shoulders up", shot="close-up"),
         lines=[("tangxiaotang", "那包黃紙糖沒有批號，帳上根本沒賣過這一包！", "對賴三，不笑")],
         motion=f"her right hand claps down flat on the stack against her chest, only her hand moving; {HEADSTILL}",
         zh="近景（從背後）、慢推（送禿樹與晴空的裁切）：唐小棠後腦與肩在畫面正中、頭不動，右手往帳本上一拍（『啪』地闔上；只動手）（nospeak，拍法 3）。稿子『眼神一變、往畫外右下看』不拍（頭不動）"),
    dict(loc="square_c", cam="Low-angle close-up, slow push in", chars=["laisan"], night="noon",
         comp=f"low-angle close-up of {LAI_B}, kneeling, framed from the chest up with space above his head, his tied hands raised before his chest from the first frame, his face three-quarter to screen left toward someone out of sight beyond the lower left edge of the frame, never the lens; that side of the frame is only the bare branches and the clear blue sky all the way to the edge, and he is the only person in the frame; flustered and stammering, not smiling: brows up, eyes darting, lips moving fast between words; behind him the bare branches of a tree and the clear blue sky",
         lines=[("laisan", "那……那是邊角料，邊角料本來就不記帳！", "結巴")],
         motion="Lai San jerks forward on his knees and blurts the words out, his eyes darting",
         zh="低角度近景、慢推（送禿樹與晴空的裁切）：賴三跪著、綁著的手第一格已經舉在胸前，往前一挺、脫口而出，朝畫左下外看不到的人（唐小棠，不點名）說。稿子『太陽穴冒汗』不寫（拍法 12）"),
    dict(loc="square_c", cam="Medium shot, slow push in", chars=["xuyan", "laisan"], night="noon",
         comp=f"medium shot low on the platform, both men framed from the waist up: on the left {XU_D}, already crouched low from the first frame, his face at the same height as the other man's, side-on to us facing screen right, never the lens; low and sharp, not smiling: head tipped a little, eyes fixed, lips moving low between words; on the right {LAI_B}, kneeling, already leaning back away from him from the first frame, side-on to us facing screen left, never the lens, scared, his lips pressed shut; behind them the bare branches of a tree and the clear blue sky; {HANDS}; exactly two people",
         lines=[("xuyan", "邊角料不記帳，你怎麼知道？昨晚那個食盒，誰送的？", "壓低聲音")],
         motion=f"Xu Yan tips his head to one side as he speaks low into the other man's face; {quiet('Lai San')}",
         zh="中景、慢推（送禿樹與晴空的裁切）：左邊許硯第一格已經蹲低、跟跪著的賴三平視（側面朝畫右），歪一下頭壓低聲音問；右邊賴三第一格已經往後縮（側面朝畫左），嘴閉著。稿子『手指在台板上輕敲一下』不拍（一鏡一個動作；不寫單根手指）"),
    dict(loc="square_c", cam="Medium close-up, slow push in", chars=["laisan"], night="noon",
         comp=f"medium close-up of {LAI_B}, kneeling, framed from the chest up with space above his head, his tied hands already raised before his chest from the first frame, his face three-quarter to screen right toward someone out of sight beyond the lower right edge of the frame, never the lens; that side of the frame is only the bare branches and the clear blue sky all the way to the edge, and he is the only person in the frame; broken and desperate, not smiling: face crumpled, brows up, eyes wide and wet, lips moving hard in a cry between words; behind him the bare branches of a tree and the clear blue sky",
         lines=[("laisan", "是孫掌櫃！他提食盒送銀子，叫我咬許家！", "崩潰")],
         motion="Lai San thrusts both his tied hands out together toward the lower right edge of the frame as he cries out",
         zh="中近景、慢推（送禿樹與晴空的裁切）：賴三整張臉垮掉、不笑，綁著的兩手第一格已經舉在胸前，邊喊邊一起往畫右下外（台下人群裡的孫掌櫃，不點名）一戳（不寫單根手指）。稿子『指完整個人趴到台板上』不拍（一鏡一個動作；趴下會看不到臉）；剪在手戳出去的一半"),
    dict(loc="square_r", cam="Medium close-up, slow push in", chars=["sunzhanggui"], night="noon",
         comp=f"medium close-up of {SUN}, standing on the packed pale earth below the right side of the platform, framed from the chest up with space above his head, two hands in plain grey cotton sleeves reaching in from behind his shoulders, already pressed flat on his back from the first frame, unnamed; both his hands empty at his sides; his face turned up three-quarter to screen left toward the platform beyond the upper left edge of the frame, never the lens; pale and rattled, not smiling: eyes wide, brows drawn, lips moving fast between words; behind him the long low tiled building and its plank doors, soft; {HANDS}; exactly one person and two hands",
         lines=[("sunzhanggui", "胡說！小的只是送頓飯，什麼銀子？", "臉色發白")],
         motion="the two hands shove Sun Zhanggui one stumbling step forward as he speaks",
         zh="中近景、慢推（送免費圖 `set-guangchang-you-wu-l1`：一排瓦屋與木板門，同第 28 集 s37）：孫掌櫃（瘦長臉、花白鬍、綠緞袍、兩手空著）臉色發白，身後兩隻灰布袖的手（不點名、不給臉）第一格已經按在他背上，把他往前推一步；他抬頭朝畫左上外的台上說。稿子『往人群裡退』不拍（一鏡一個動作）；胡縣令不同鏡（原版必修）"),
    dict(loc="square_d", cam="Insert close-up, slow push in", chars=[], night="noon",
         comp=f"insert close-up, the shot opens directly on the red cloth over the long desk, from its very first frame, one man's right hand in a faded blue-grey sleeve cuff already holding {INGOT} a finger's width above the red cloth, {GAVEL} lying further along the cloth, soft; only the red cloth, the wooden block, the hand, its sleeve cuff and the ingot are in the frame",
         lines=[("xuyan", "這錠銀子是賴三收的，底下的戳，是魏記的。", "畫外")],
         motion=NOBODY + "the hand sets the silver ingot down on the red cloth and lets go of it, the ingot standing still and plain",
         zh="插鏡、慢推（第一格就是公案紅布上的手；送免費新圖 `set-guangchang-an-l1`：紅布案與案上的深色木塊）：許硯藍灰袖口的手把銀錠放上公案、放手（頂面平滑、沒有字，許硯畫外的台詞放錄音）。稿子『翻過來底面朝上、一個方形戳印框』不拍（拍法 27：魏記由台詞說；方框會長字，同第 28 集 s10）"),
    dict(loc="square_c", cam="Low-angle close-up, slow push in", chars=["weishaoqing"], night="noon",
         comp=f"low-angle close-up of {WEI}, already standing beside the dark wooden armchair from the first frame, framed from the chest up with space above his head, {FAN}, his face turned down three-quarter to screen right toward the earth below the platform beyond the lower right edge of the frame, never the lens; that side of the frame is only the bare branches and the clear blue sky all the way to the edge, and he is the only person in the frame; cold and blank, not smiling: eyes flat, the corners of his mouth pulled down, lips moving coldly between words; behind him the bare branches of a tree and the clear blue sky",
         lines=[("weishaoqing", "孫掌櫃，自己做的事，自己認了吧。", "冷，一點表情都沒有")],
         motion="Wei Shaoqing points the tip of the closed fan once down toward the lower right as he speaks",
         zh="低角度近景、慢推（送禿樹與晴空的裁切）：魏少卿第一格已經站在木椅旁，用合著的扇子往畫右下一指、冷冷地說，一點表情都沒有、嘴角往下（拍法 30：第 29 集是他輸的鏡，NOSMILE）。稿子『從椅子上站起來』在第一格已經完成（一鏡一個動作）"),
    dict(loc="square_r", cam="Medium shot, slow push in", chars=["sunzhanggui"], night="noon",
         comp=f"medium shot of {SUN}, standing on the packed pale earth before the platform, framed from the knees up, two hands in plain black cotton sleeves reaching in from the left and right edges of the frame, already gripping his two upper arms from the first frame, unnamed; his face turned up three-quarter to screen left toward the platform beyond the upper left edge of the frame, never the lens; beaten and set, not smiling: jaw clenched, eyes lowered, lips moving tightly between words; behind him the long low tiled building and its plank doors, soft; {HANDS}; exactly one person and two black-sleeved hands",
         lines=[("sunzhanggui", "是小的一個人的主意，跟少爺無關。", "跪下，咬牙")],
         motion="Sun Zhanggui's knees give way and he sinks down to kneel on the earth as he speaks, the two black-sleeved hands keeping their grip",
         zh="中景、慢推（送瓦屋與木板門的裁切）：孫掌櫃站在台前的黃土地上，畫左右緣兩隻黑袖的手（不點名、不給臉、沒有兵器，拍法 16、17）第一格已經抓住他兩條上臂，他膝蓋一軟跪下、咬牙說，抬頭朝畫左上外的台上。稿子『回頭看魏少卿、魏少卿已轉身』不拍（一鏡一個動作；不描述畫外的人）"),
    dict(loc="square_c", cam="Close-up from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="noon",
         comp=alone(f"both her hands holding {STACK} against her chest; beyond her, soft, the bare branches of a tree and the low tiled roofs against the clear blue sky; {HANDS}",
                    "standing on the packed pale earth,", frame="framed from the shoulders up", shot="close-up"),
         lines=[("tangxiaotang", "棄了一顆棋子，魏少卿自己乾乾淨淨。", "冷，小聲")],
         motion=f"her shoulders draw in a little and stay low; {HEADSTILL}",
         zh="近景（從背後）、慢推（送禿樹與晴空的裁切）：唐小棠後腦與肩在畫面正中、頭不動，肩膀收一下（冷、小聲）（nospeak，拍法 3）。稿子『嘴角一壓、側頭對許硯說』不拍（頭不動）"),
    dict(loc="square_c", cam="Low-angle close-up, slow push in", chars=["huxianling"], night="noon",
         comp=f"low-angle close-up of Magistrate Hu, {HU}, sitting behind the long desk draped in red cloth, framed from the chest up with clear space above his hat, his right hand already gripping {GAVEL} raised a hand's height above the red cloth from the first frame, his face three-quarter to screen right toward the middle of the platform below, never the lens; flustered and hasty, not smiling: brows up, eyes darting, mouth moving fast between words; behind him the bare branches of a tree and the clear blue sky; he is the only person in the frame",
         lines=[("huxianling", "孫掌櫃、賴三押下去！許記無罪，封條撕了！退堂！", "擦汗")],
         motion="Magistrate Hu brings the wooden block down on the desk with one knock as he speaks fast",
         zh="低角度近景、慢推（送禿樹與晴空的裁切）：胡縣令（有帽翅的黑紗幞頭）右手第一格已經舉著驚堂木，一拍、急急地宣判。稿子『用袖子擦汗、起身、兩個衙役擁著他從台後下去』不拍（拍法 12 不寫汗；一鏡一個動作；退堂交給音效與剪接，第二場他不入鏡）"),
    dict(loc="square_l", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="noon",
         comp=alone(f"her left arm holding {STACK} against her side; just beyond her right hip the plain wooden chest, {STRIPS}, her right hand already pinching the crossing point of the two strips from the first frame; beyond, soft, the edge of the low stone platform in the hard winter sun; {HANDS}",
                    "standing on the packed pale earth below the left side of the platform,"),
         lines=[("tangxiaotang", "封條我來撕。糖箱就在這兒，下午就在廣場賣！", "揚聲")],
         motion=f"her right hand tears the two crossed paper strips off the chest in one pull, and the torn white strips flutter away on the air; {HEADSTILL}",
         zh="中景（從背後）、慢推（送台子左下的地面與木箱）：唐小棠背影在畫面正中、頭不動，右手第一格已經捏住木箱上兩條交叉白紙封條的交叉處，一把撕下、紙條隨風飛走（nospeak，拍法 3；本場結尾，剪在紙條飛起來的時候）。稿子『許硯在她身後』不拍（畫面裡只有她）"),
    # ---- scene 2: the same afternoon, the edge of the square (set-guangchang-pm-l1, graded, and its crops).
    dict(chapter="廣場邊，午後", loc="pm_l", cam="Medium wide shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="pm",
         comp=alone(f"standing behind one long plain wooden table set up as a stall beside the plain wooden chest, its lid lifted off, her right hand already holding {PACKET} across the table to the first customer from the first frame; at her right, side-on to us, {XU_D}, standing, framed from the waist up, {POUCH} in his left hand, his face three-quarter to screen left toward the line, never the lens, a small closed-lip smile, his lips pressed shut; beyond the table {CUSTOMERS}, their lips closed; {HANDS}; exactly eight people, the young woman in the middle seen only from behind",
                    "behind the stall,", shot="medium wide shot"),
         lines=[("tangxiaotang", "最後一盒了！糖霜糕一人兩塊，賣完就沒有！", "揚聲，本鏡可以笑")],
         motion=f"the first customer takes the white packet from her hand and steps away out of the line; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中全景（從攤子後面拍）、慢推（送午後調色的 `set-guangchang-pm-zuo-l1`；聖經的 `set-guangchang-pm-l1` 照聖經的命令免費調色後再照第 28 集的裁法裁）：唐小棠背影在畫面正中、頭不動，站在木箱旁借來的長木桌後，右手第一格已經把一包白紙包遞過桌；她右邊許硯側身拿著布錢袋、閉嘴微笑；桌前六個客人排成一列面向我們（拍法 25：稿子『約二十人』寫實際入鏡的六人，各穿不同的衣服），第一個接過紙包走開（nospeak，拍法 3）。稿子從正面拍攤子會露她的臉，改從攤子後面拍；推軌改慢推"),
    dict(loc="pm_e", cam="Insert close-up, slow push in", chars=[], night="pm",
         comp=f"insert close-up, the shot opens directly on the bare pale wooden bottom inside the plain wooden chest, from its very first frame, {PACKET} lying alone on it, {TANG_HAND} already resting on the packet; only the inside of the chest, the packet, the hand and its sleeve cuff are in the frame",
         lines=[("tangxiaotang", "下午這一箱，三十兩，一塊都不剩。", "畫外")],
         motion=NOBODY + "the hand lifts the last white packet up and away out of the frame, leaving the wooden bottom of the chest bare",
         zh="插鏡、慢推（第一格就是糖箱的箱底；送午後調色的免費新圖 `set-guangchang-pm-di-l1`：黃土地）：桃粉袖口的手把最後一包拿起、拿出畫面，箱底空了（唐小棠畫外的台詞放錄音）。稿子『許硯的手把布錢袋口一束』不拍（一鏡一個動作；錢袋在 s29 交代）"),
    dict(loc="pm_l", cam="Close-up, slow push in", chars=["xuyan"], night="pm",
         comp=f"close-up of {XU_D}, framed from the chest up with space above his head, {POUCH}, plump and heavy, already held up at his chest in his right hand from the first frame, his face three-quarter to screen right, his eyes lowered to the pouch, never the lens; he is the only person in the frame; quietly moved: eyes a little wide, brows easing, lips pressed shut; behind him, soft, the long plain wooden table of the stall and the low tiled buildings in the warm afternoon sun",
         lines=[("xitong", "叮。鬥商總帳：許記三百三十兩，魏記一百六十五兩。任務完成。", "冷，宣布，一字一字念清楚")],
         panel=[("鬥商總帳：許記三百三十兩，魏記一百六十五兩", "task"), ("任務完成", "task")],
         motion=f"Xu Yan lets out one long slow breath and the corners of his mouth slowly lift into a small closed-lip smile; {SILENT_HE}; he is listening, not speaking",
         zh="近景、慢推（送午後的攤子裁切；拍法 11 不寫藍光）：許硯右手第一格已經提著鼓鼓的布錢袋，長長吐一口氣、嘴角慢慢往上（稿子『本鏡可以笑』，閉著嘴的笑）；全程嘴閉著（系統一句）。面板「鬥商總帳：許記三百三十兩，魏記一百六十五兩」「任務完成」由剪接一前一後疊上"),
    dict(loc="pm", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "weishaoqing"], nospeak=["tangxiaotang"], night="pm",
         comp=alone(f"{STACK} already held against her chest in her left arm from the first frame, her right hand at her side; beyond her, small and soft on the low stone platform, standing beside the dark wooden armchair, {WEI}, framed full figure, {FAN}, his face three-quarter toward her, never the lens, his lips pressed shut; the long desk on the platform bare and empty; she stays in the middle of the frame the whole shot, her shoulders square to us; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "standing on the packed pale earth before the platform,"),
         lines=[("tangxiaotang", "三百三十兩對一百六十五兩，魏公子，認不認？", "下巴一抬")],
         motion=f"her right hand comes up and settles on her hip, only her arm moving; {quiet('Wei Shaoqing')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送午後調色的寬景裁切 `set-guangchang-pm-tai-l1`）：唐小棠背影在畫面正中、頭不動，左臂抱著帳本，右手往腰上一插（稿子『下巴一抬』改手插腰：頭不動）；她前方遠處台上，魏少卿站在木椅旁、手拿合著的扇子、嘴閉著；台上的公案已經空了（胡縣令退堂）（nospeak，拍法 3）"),
    dict(loc="pm_c", cam="Close-up, slow push in", chars=["weishaoqing"], night="pm",
         comp=f"close-up of {WEI}, already standing on the platform from the first frame, framed from the chest up with space above his head, {FAN} held before his chest, his face three-quarter to screen left, never the lens; that side of the frame is only the bare branches and the sky all the way to the edge, and he is the only person in the frame; unhurried and sure of himself: a thin smile, eyes half lidded, lips moving slowly between words; behind him the bare branches of a tree and the low tiled roofs against the clear sky in the warm afternoon light",
         lines=[("weishaoqing", "日落才算第三十日。我岳父的車，就快到了。", "慢條斯理，本鏡可以笑")],
         motion="Wei Shaoqing's eyes slide once toward the right edge of the frame, toward the road, as he speaks, his head still",
         zh="近景、慢推（送午後調色的禿樹裁切 `set-guangchang-pm-shu-l1`）：魏少卿站在台上，眼睛往畫右（廣場邊的大路）一瞄，慢條斯理地笑著說（稿子『本鏡可以笑』）。稿子『慢慢打開扇子』不拍（拍法 30：扇子一直合著）"),
    dict(loc="pm_r", cam="Wide shot, slow push in", chars=["zhengbo"], night="pm",
         comp=f"wide shot at standing eye height on the packed pale earth at the edge of the square, {CARRIAGE}, already standing still from the first frame, its door already swung back; beside the carriage door {ZHENG}, standing on the earth, framed full figure, one hand still on the door, his face three-quarter to screen left, never the lens; steady and grave, not smiling, his lips pressed shut; he is the only person in the frame; behind them the long low tiled building and its plank doors in the warm afternoon sun",
         motion=f"Steward Zheng bows low and slow beside the carriage door; {SILENT_HE}",
         zh="全景、慢推（人眼高；送午後調色的瓦屋裁切 `set-guangchang-pm-you-wu-l1`）：拍法 26：畫右緣只見黑漆車廂與一匹馬的頭頸（四匹馬不一起入鏡、馬蹄聲交給音效）；車門第一格已經拉開，鄭伯站在車門旁、手還扶著門，深深一躬（無台詞，嘴閉著）。鄭伯照聖經寫高瘦、背微駝、灰白山羊鬚（`extras.json` 換掉 cast.json 的微胖）；袖口的小毛筆不寫（brush 會長字）。稿子『人群往兩邊閃開、從車轅跳下來』不拍（一鏡一個動作）；他跟唐萬金不同鏡（稿子）"),
    dict(loc="pm_r", cam="Close-up from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="pm",
         comp=alone(f"{STACK} already held against her chest in both arms from the first frame; beyond her, soft, the long low tiled building and its plank doors in the warm afternoon sun; {HANDS}",
                    "standing on the packed pale earth,", frame="framed from the shoulders up", shot="close-up"),
         lines=[("tangxiaotang", "那是唐家的車……駕車的是鄭伯。", "臉色一白")],
         motion=f"the stack of paper slips down in her arms and both her hands catch it against her chest; {HEADSTILL}",
         zh="近景（從背後）、慢推（送瓦屋裁切）：唐小棠後腦與肩在畫面正中、頭不動，帳本往下一滑、她兩手一把抱住（nospeak，拍法 3）。稿子『臉一白』由錄音的語氣交代"),
    dict(loc="pm_r", cam="Medium shot, slow push in", chars=["tangwanjin"], night="pm",
         comp=f"medium shot on the packed pale earth at the edge of the square: {TWJ}, already a step out from the carriage from the first frame, framed from the knees up, both his arms flung wide, his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; crying, not smiling: his face crumpled, tears running down his round cheeks, brows pulled up in grief, mouth wide in a sob; behind him, soft, the black lacquered carriage body at the right edge and the long low tiled building in the warm afternoon sun; he is the only person in the frame",
         lines=[("tangwanjin", "囡囡！", "哭著撲過來，短喊")],
         motion="Tang Wanjin stumbles forward toward the left edge of the frame with his arms flung wide, the gold keys at his waist swinging",
         zh="中景、慢推（送瓦屋裁切）：唐萬金（圓臉、短鬍、小金冠、紫袍滿金元寶、腰間一串金鑰匙）第一格已經下了車、兩手張開，哭著往畫左跌撞地奔、金鑰匙一路晃，短喊「囡囡！」（在畫面上說；`build-r2.py` 的 EN 補他的名字）。哭相、不是笑（原版必修）；胡縣令第二場不入鏡（同框撞臉）；鄭伯不同鏡。稿子『從車門跌撞出來』在第一格已經完成"),
    dict(loc="pm_r", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="pm",
         comp=alone(f"{STACK} tucked under her left arm, her right hand already gripping the left sleeve of the young man before her from the first frame; half a step beyond her and a little right of the middle, {XU_D}, standing, framed from the waist up, his back three-quarter to us, facing screen right toward the far side of the square, his shoulders squared; beyond them, soft, the long low tiled building and its plank doors in the warm afternoon sun; she stays in the middle of the frame the whole shot, close behind his left shoulder; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "standing on the packed pale earth,"),
         lines=[("tangxiaotang", "是我爹……他是來帶我回去的嗎？", "躲在他肩後，小聲")],
         motion=f"Xu Yan turns his head over his left shoulder and looks down at her once, steady and not smiling; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送瓦屋裁切）：唐小棠背影在畫面正中、頭不動，帳本夾在左臂下、右手第一格已經抓住前面許硯的左袖；許硯在她前方半步偏右、背對四分之三、挺著肩朝畫右（廣場那頭）；他回頭往左肩後看她一眼、不笑、嘴閉著（nospeak，拍法 3；本集最後一鏡，接點 29→30：第 30 集第一鏡唐萬金跑到一步外停住）。稿子『探出半張臉』不拍（她不露臉）；『再挺起肩膀對著奔過來的人』只留挺著的肩（不描述畫外的人）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e029-r2/script.md`（c01–c35 對應 s01–s35；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-17）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e021-e030.md`（拍法 1–30 條）。第 3 篇章〈搶親〉第九集。",
    "- 內部工作編號 929（`hailuo/{ff,clips}-dh-e929.json`、`colab/runs/e929/extras.json`、`colab/runs/e929-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e929-dh/`）；發布 slug `zhong-tian-qu-qi-e029-r2`。不放集數、不放片名卡；s01 接第 28 集 s39（接點 28→29：同一刻，不重播賴三那句，許硯平靜地舉起一塊糖糕）；s35 交給第 30 集（接點 29→30：同一刻，唐萬金跑到一步外停住）。",
    "- 照第 28 集審稿後的寫法一開始就照做：`OFFSCREEN_SPEECH = False`；唐小棠背影說話時，每張朝鏡頭的臉都寫不說話、嘴閉著；**對畫外的人說話寫「朝畫左／右外看不到的人」，那一側到邊緣只有景、畫面裡只有他一個人，不點名、不描述不在畫裡的人**（提示詞與精修文字都一樣）；掛著的東西不點名；不寫 open；道具與接觸寫在第一格；紙一律空白（s10 柳葉水印是聖經唯一的例外）；寫人數，鎮民、客人每人一套不同的衣服。",
    "- **唐小棠不露嘴說話、不露臉**（拍法 3）：她在畫面上的九句（s02、s14、s16、s24、s26、s27、s30、s33、s35）全從背後拍、畫面正中、正背對鏡頭、頭不動、剛好兩顆丸子；spec 拿掉她的圖與身分句；畫外兩句（s15、s28）是她的手的插鏡。稿子 c14『上台』不拍，她留在台左下、木箱邊。算盤本集沒有（拍法 20）。",
    "- **胡縣令每鏡都戴有帽翅的黑紗幞頭**，驚堂木是長方形木塊；跟孫掌櫃不同鏡（s20、s23 只有孫掌櫃）；第二場不入鏡（跟唐萬金不同框）。**魏少卿**扇子一直合著（拍法 30）；s22 頂罪那一鏡不笑（第 29 集是他輸的集）。衙役與兩排水火棍不拍（拍法 16、17；音效），s23 只有兩隻黑袖的手。",
    "- **場景圖說了算**（拍法 29，協調者 2026-11-17 決定，每張放大看過）：正午沿用第 28 集的廣場免費圖（`-tai-l1`、`-tai-zhong-l1`、`-shu-l1`、`-zuo-l1`、`-you-wu-l1`）；**新的免費圖十張**：`set-guangchang-an-l1`（紅布公案）、`-di-l1`（黃土地）、`prop-liuye-zhi-xin-l1`（柳葉水印紙只取紙）、`prop-huangzhi-l1`（粗黃紙）、午後 `set-guangchang-pm-l1`（聖經的調色）與它照第 28 集裁法的 `-pm-tai-l1`、`-pm-zuo-l1`、`-pm-shu-l1`、`-pm-you-wu-l1`、`-pm-di-l1`（見 refs-live README）。**不需要試鏡**。",
    "- 長鏡要買的秒數（BUY）：照錄音核過（見 `r2.py` 的 BUY 註解）。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音的人聲長度為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯（l1、angle-a；帶笑的 angle-b 整集不送）、賴三 l1、孫掌櫃 l1、魏少卿 l1、胡縣令 l1、鄭伯 l1、唐萬金 l1。唐小棠整集不送圖。鎮民、客人、推孫掌櫃的手、黑袖的手、跪著的背影都不送圖。場景見上面。",
    "- 共用檔：`writer-tools/e001-r2/build-r2.py` 的 `EN` 加一筆 `\"tangwanjin\": \"Tang Wanjin\"`（s34 唐萬金在畫面上說話；`gen-dh.mjs` 本來就有這個名字）；e910–e928 照位元組重建不變。`gen-dh.mjs`、`pilot.py`、`cast.json` 不動；`refs-live` 加十張免費圖（都是新 id）與 README 一段。鄭伯的微胖、唐萬金的笑眼、魏少卿的笑與玉冠由 `colab/runs/e929/extras.json` 換掉；精修文字的 CG 立領句與唐小棠的名字由本檔結尾的 `live_clips()` 在 build 後從 `clips-dh-e929.json` 換掉。",
    "- `colab/runs/e929/extras.json`（照第 28 集）與 `colab/runs/e929-live/spec.json`（`mkspec.py` 產生；種子 9291101／9291102）。",
    "- 免費準備：scratchpad `prep929.sh`（照 `prep928.sh` 審稿後的順序：先把精修句拆成錨點的形式給第一段、再把 live 文字放回；`DRY=1 … st1-ep.sh 929` → `pilot.py` → `retake.py` → `colab-jobs.json` 加 output_path、套 swap_pictures（絕對路徑）→ 逐鏡查送的場景圖與人物圖 → 精修用的分隔句 → `preflight-prompts.py` → 否定名詞、會長字的名詞、掛著的東西、open、『畫外的年輕女子』、『點名的畫外人』與精修句外漏掃描）。",
    "- 配樂：公審的低鼓延續，s10 柳葉一個亮的鈴音、之後上揚的弦，s19 崩潰一個重拍，s26 撕封條一個大的釋放；午後明亮的市集 cue，s29 總帳一個勝利重音，s32 大車到停一拍、轉成溫暖又不安的弦。音效見 script.md〈音樂與音效〉（另外：衙役放低水火棍、人群嗡嗡、台板與跪地、胡縣令退堂下台、馬蹄車輪，都交給音效）。",
]

# Long shots: seconds to buy. Measured 2026-11-17 against the 32 kept recordings (~/mokaair-work/videos/zhong-tian-qu-qi-e929-dh/audio;
# wave length and silencedetect -35 dB speech span, scratchpad span929.sh; e013's test as e928: a shot holds (buy - 0.3) x 1.1 s of
# speech, half a second between lines, so 5 s holds 5.17 s, 6 s 6.27 s, 8 s 8.47 s). faster-whisper medium read every take back, one
# clip per process, numpy input, once plain and once with the previous line and the line as context (audio/fw929.txt,
# fw929-retake.txt; audio/README-retakes.txt). No shot runs over about 10 s, so none is split (the longest: s25, a23 7.12 s).
# 8 s: s06 (a06 Magistrate Hu, 6.44 s), s25 (a23 Hu, 7.12 s), s31 (a29 Wei Shaoqing's slow drawl, 7.08 s), s29 (the system's tally,
#      5.42 s: the script's 長鏡 c29, the long breath, the slow smile and two panels one after the other), s35 (the episode's last
#      shot: the hook needs a held tail, as e923-e928).
# 6 s: every other speaking shot, and s10 (a09's retake 5.56 s) and s21 (a19's retake 5.28 s), inserts that would be 5 s. The
#      tightest: s07 (a07 5.92 s), s22 (a20 5.84 s), s04 (system 2.50 + 0.5 + his thought 2.60 = 5.60 s).
# 5 s: the inserts s11 (a10 4.20 s), s15 (a13 4.60 s), s28 (a26 4.16 s), and the one-action shots s09 (the sheet raised), s32 (the
#      bow), s34 (「囡囡！」 1.56 s). The wides s05, s12 keep gen-dh's 6.
BUY = {"s06": 8, "s25": 8, "s29": 8, "s31": 8, "s35": 8, "s10": 6, "s21": 6, "s15": 5, "s09": 5, "s32": 5, "s34": 5}


# ---- the refine text (e022 review 必改 12, as e023-e028): hailuo/clips-dh-e929.json column 0 is the motion text
# refine-prep.py sends with a picked d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era "Tang
# Xiaotang's high stand-up collar stays closed at her throat." and names her in "<names> shown in <Picture 1>"; in a back shot
# that draws the collar back and turns her face to the lens. Her shots are all back shots: the sentence goes and her name becomes
# "the young woman seen only from behind", and "keeps the same face, hair, costume and props" of a back shot alone becomes
# "keeps the same hair, costume and props as the first frame, her back to us" (with someone else: "..., the young woman's back to
# us"). Column 1 is recomputed. prep929.sh hands stage 1 the anchor form (anchor_form(), e028 review 必改 1).
COLLAR = "Tang Xiaotang's high stand-up collar stays closed at her throat. "
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
        text = text.replace("Constable Zhao", "Zhao Butou")
        assert "stand-up collar" not in text and "onstable" not in text, key
        row[0] = text
        row[1] = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    open(path, "w", encoding="utf-8").write(json.dumps(clips, ensure_ascii=False, separators=(",", ":")))


# e928 review 必改 1: ref2manifest.mjs (stage 1 of prep929.sh) strips gen-dh's refine anchor with ANCHOR_FF, and the back-shot
# wording live_clips() writes no longer matches it. prep929.sh hands stage 1 the anchor form of the live file (this), then puts
# the live file back; the refine text (clips-dh) keeps live_clips()'s wording.
def anchor_form(text):
    text = text.replace(", the young woman's back to us; the set layout stays as it is.", "; the set layout stays as it is.")
    text = text.replace("keeps the same hair, costume and props as the first frame, her back to us; the set layout stays as it is.",
                        "keeps the same face, hair, costume and props as the first frame; the set layout stays as it is.")
    assert "back to us; the set layout" not in text
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
