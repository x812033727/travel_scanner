"""Episode 21 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e021-r2/script.md
(c01-c37 = s01-s37, c28b = s28b; the CG-era r2 script), including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and
「真人版的改動（2026-11-16）」, which override the tables. Every line is the script's, word for word; only the staging changes.
Bible: production/r2-bible-e021-e030.md (rules 1-30, the 20->21 hand-over, the picture table). The first episode of arc 3
〈搶親〉; s01 continues e020 s38 at the same moment.

Written from the first draft the way e020-r2/r2.py stands AFTER its independent review (../e020-r2/review.md) and with the
e920 picking lessons (colab/runs/e920-live/picks-merged.tsv and fix1/mkspec.py; e919-live/fix1/mkspec.py):
- OFFSCREEN_SPEECH = False (rule 15): every shot with an off-screen line, a thought or a system line writes the silence of
  each person on screen (quiet(), SILENT_HE); quiet() governs the lips only (e020 review 必改 9).
- Rule 18 / e920 fix1: nothing is negated by name, and no object is named that should not appear ("books" drew books, so
  the papers are named by what they are: folded sheets, one thin grey cloth-bound booklet). Rule 27's fixed paper sentences:
  the chancellor's letter TIE, the Tang marriage paper HUNSHU (both only folded, outside up), the register MINGCE (closed,
  plain grey cover), the county paper RED (folded red paper) in an oiled-paper PACKET. The script's opened register with its
  red ring (c11) and the unfolded marriage paper with its seal frames (c06) are never filmed (rule 7): a finger on the closed
  cover, two fingers tapping the folded sheet.
- Hands and props in the first frame, in a named hand; contact as a state (s34 her hand already on his sleeve). No pointing
  finger at a person: Wei Shaoqing points with the closed fan (s20, s37), Sun Zhanggui an open palm (s02).
- Tang Xiaotang never speaks on camera (rule 3): her three lines (s04, s07, s34) and her silent s09 and s35 are from behind
  her across the counter (TBACK, nospeak; spec.json drops her three pictures and her identity sentence); her one face is
  s12 (silent: the colour drains while Wei Shaoqing's line plays off screen), with the short-ribbon sentence of e920 fix1
  and without her long-ribbon profile angle-b. The gold abacus (rule 20: inserts only) is not in this episode: c01's hug
  and c07's slap become her hands (s07 both palms slap the counter; the click is a sound effect), so no second abacus grows.
- No more than three named faces (rule 1): s01 Xu Yan, Wei Shaoqing, Sun Zhanggui (Tang Xiaotang, Erniu, Qin Shuang off
  screen); s10 Wei Shaoqing and Xiaohe with Xu Yan's unnamed back; s36 Erniu and Sun Zhanggui with Wei Shaoqing's unnamed
  back. Over-the-shoulder and silhouette foregrounds are unnamed and get no picture (rule 2): Xu Yan in s10, s28, s37; Wei
  Shaoqing in s15, s27, s32, s36 (e920 fix1: back views without a face picture avoid duplicates).
- The two henchmen (bible 小角色): plain black short jackets, black head wraps, cloth shoes, empty hands, side and back only,
  never a face (THUGS / THUG1). Qin Shuang's staff STAFF (rule 22's wording style), Erniu's door bar BAR; no blade anywhere
  (rule 5: the script's knife at Qin Shuang's belt is not written; extras.json removes it from her cast sentence).
- Xiaohe knocked down (原版必修 21): the push is split in two short shots (s21 the sweep of the arm, s21b already sitting on
  the floor crying 「哥！」), and every shot after it writes tears and the corners of her mouth pulled down.
- Smiles only where the script and rule 30 allow them: Sun Zhanggui s02 (陪笑); Wei Shaoqing s05, s08, s10, s13, s28, s33,
  s37 (冷笑、笑回來; rule 30 lets him smile, never in s19, where the smile freezes); Xu Yan's cold mouth corner s27, s32.
  Every other face is a set expression (brows, eyes, jaw).
- Nobody is flipped: every speaker wears a cross or round collar; sides are written as screen left/right.

THE AXIS (bible 接點 20->21, e020 review 必改 4-7): as in e020's closing scene, looking at the front doorway the counter is
on screen RIGHT. Wei Shaoqing, Sun Zhanggui, the doorway, the henchmen and Erniu are on the LEFT and look screen right; Xu
Yan in front of the counter and Tang Xiaotang behind it are on the RIGHT and look screen left. Reverse shots stay on the
shelf side of that line. The script's CG layout (counter left, door right) is mirrored throughout.

PLACES (the coordinator's decisions, 2026-11-16; every picture looked at full size; listed again in script.md 〈真人版的改動〉):
- Scene 1 (s01-s19, the last of the dusk): set-xuji-pu-dusk-l1 (e020 s34-s38's picture, so the cut does not jump).
- Scenes 2-3 in the shop (s20 on, nightfall): set-xuji-pu-ye-l1 (the arc-3 screen test 37033: the shop with the light
  changed, the counter along the right wall with two small brass oil lamps on it, a red glow beyond the doorway). The two
  lamps are written from s01 on (LAMPS): the script's oil lamps on the counter, lit at closing time.
- The back yard seen through the back door (s29, s31): set-xuji-houyuan-ye-l1 (the free crop of set-chouduan-ye-l1: brick
  well under a thatched roof, brick wall right, a stone path to one lantern). The back door itself is a plain dark door in
  the far right corner of the white panelled wall, where e020 s33 (and its fix1 retake) sent A-ling out; the bible's
  "end of the left-wall shelves" is not used, because the e020 footage already put it on the right.
- The paper inserts (s03, s06, s11, s16): set-xuji-pu-cabinet-l1 (the dark wooden cabinet top, e020's free crop) as the
  counter top; Ref2VA needs at least one picture, and the full shop would cut back to the wide view (e915 s08).
- Close shots send no set picture (e020 review 建議 18), nor Xu Yan's medium shots facing screen left (s15, s27, s32: the
  pictures show the doorway, and he has the counter and the white wall behind him).
- gen-dh SET takes the first pattern that the prompt matches: every shop prompt says "Xu family shop" and none of gen-dh's
  earlier words ("alley", "inn", "well pit", "city street"...); the yard prompts say "back yard behind the Xu family shop".
- The no-person inserts carry NOBODY at the head of their motion, so the clips-dh text holds "the set layout stays as it
  is. " once and the d1 prompt "never the mood. " once (refine-prep.py splices a retake's motion between those and "One
  continuous shot."; e920 s15, s16, s23, s37 had neither).
- Shared files: none changed (every speaker is in build-r2.py's EN; no new set; cast.json untouched).
"""
EP = 921  # internal working number; the published slug is zhong-tian-qu-qi-e021-r2
SLUG = "zhong-tian-qu-qi-e021-r2"
EP_TITLE = "宰相府的帖子，林二丫的名字（重製版 r2）"
OUTLINE_SECONDS = 191  # script.md: 191 s, 38 shots (19 + 9 + 10); s21b splits c21 (rule: the push in two short shots)
TARGET_MINUTES = [3, 4]
TITLE = "三日後，州府來拿冒名犯｜種田娶妻打天下 第21集（重製版）"
DESCRIPTION = "許記打烊前，宰相府的公子魏少卿搖著灑金摺扇跨進門：我的未婚妻，在你家？許硯擋在櫃檯前：我這裡只有我的妻子。魏少卿亮出宰相府的帖子、唐萬金親筆簽的婚書，再拿出縣衙配婚名冊的抄本：配給許硯的第三個叫林二丫，可林二丫兩年前就病死了，除非有人冒名。系統冷冷報出律條：冒名入冊，按律流放。許硯叫唐小棠拿出縣衙蓋印的婚書：配不配婚，是官府的事。打手推倒小禾，秦霜一棍掃倒一個，二牛抄起門閂堵住門口。魏少卿要走時推開後門，看見井邊打水的阿令：我們是不是在哪見過？他在門檻上回頭：三日後，州府來拿冒名犯。《種田娶妻打天下》第 21 集（重製版）。"
THUMB = ("三日後，州府來拿冒名犯", "s37")
CHARACTERS = ["xuyan", "tangxiaotang", "weishaoqing", "sunzhanggui", "qinshuang", "xiaohe", "erniu", "aling", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: low brooding suspense strings at dusk in a small shop, one heavy accent on a name, one on a firm reply; then a short sharp fight cue of drums, one hard accent on a staff striking, settling at once; then cold low held strings at night, one light accent on a question and one big accent on a final threat before it stops; ancient Chinese rural drama, no vocals"

# Places. gen-dh SET: "Xu family shop" for every shop prompt (dh-set-xuji-pu -> refs-live/set-xuji-pu-l1, swapped by spec.json).
COUNTER = "one long waist-high counter of plain dark wood with a thick flat top and a plain panelled front"
THE_COUNTER = "the long waist-high dark wooden counter"
LAMPS = "two small brass oil lamps with bare flames"
SHOP = ("tall dark wooden shelves along the left wall above a long low dark wooden cabinet, the wide open front doorway in the "
        "middle of the back wall between dark wooden lattice panels with the county town street beyond it, plain white "
        f"panelled walls on the right with {COUNTER} standing along them, {LAMPS} burning on its top, a floor of large grey "
        "stone tiles and dark wooden beams overhead")
SHELF_EMPTY = "the shelves standing completely bare"
EAVE = "one round plain paper lantern glowing warm orange under the eave beyond the doorway"
LOC = {
    "dusk": f"In the Xu family shop in the county town at dusk: {SHOP}; {SHELF_EMPTY}; the last low orange sunlight in thin bars across the grey floor, the street beyond the doorway turning deep blue with dusk, {EAVE}",
    "dusk_c": "In the Xu family shop in the county town at dusk, the shop dim and warm with the light of the oil lamps",
    "night": f"In the Xu family shop in the county town at nightfall: {SHOP}; {SHELF_EMPTY}; the shop lit only by the two oil lamps on the counter, their warm light on the faces near it, the far corners dim and blue, the street beyond the doorway dark blue with night, {EAVE}",
    "night_c": "In the Xu family shop in the county town at nightfall, the shop dim and warm with the light of the oil lamps",
    "insert": "In the Xu family shop in the county town, on the dark wooden counter top in warm oil-lamp light",
    "yard": "In the small back yard behind the Xu family shop at night: a round brick well with a wooden frame and crossbar under a short thatched roof on the right, a dark brick wall beside it, a narrow stone-paved path running away on the left between dark brick walls to one small glowing paper lantern at its far end, everything in deep blue moonlight",
}
LIGHT = {
    "dusk": "the last low sunlight, the blue dusk and the warm lamp light stay unchanged",
    "night": "the warm oil-lamp light and the dark blue night stay unchanged",
    "yard": "the deep blue moonlight and the one warm lantern stay unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow"
QIN = ("her dark brown cross-collared short jacket, wide plain leather belt with nothing tucked in it and nothing hanging from it, "
       "black trousers, leather boots and high ponytail tied with black cord")
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
ALING = "in her plain grey-white cotton dress with long sleeves covering her wrists, her black hair in a high bun with one plain wooden hairpin"
XIAOHE = ("little Xiaohe, in her patched lilac cotton jacket, her two little pigtails tied with red string, one small woven straw "
          "rabbit tucked in her sash")
ERNIU = "Wang Erniu, in his coarse brown hemp short jacket with the sleeves rolled up"
SUN = "Sun Zhanggui, in his green satin robe with a jade belt hook"
# bible rule 30 with the portrait's jade (e020 review 必改 7: a small green jade ornament at the front of his topknot)
WEI = ("Wei Shaoqing, in his sapphire-blue brocade robe woven with gold thread, a white jade pendant at his waist, a small green "
       "jade ornament at the front of his topknot")
WEI_BACK = ("one young man in a sapphire-blue brocade robe woven with gold thread seen only from behind, appearing only once")
XU_BACK = "one young man in a faded blue-grey robe seen only from behind, appearing only once"
FAN = "one folding fan of plain cream paper with a few large flakes of gold leaf"
THUGS = ("two burly men in plain black cross-collared short jackets, black cloth head wraps and black cloth shoes, their hands "
         "open at their sides, seen only from the side and from behind, their faces turned away in shadow")
THUG1 = ("one burly man in a plain black cross-collared short jacket, a black cloth head wrap and black cloth shoes, seen only from "
         "the side and from behind, his face turned away in shadow")
STAFF = "one long plain wooden staff taller than a man, smooth and round from end to end"
BAR = "one long square plain wooden door bar"
# bible rule 27 (fixed paper sentences; only folded, outside up, or closed)
TIE = "one folded sheet of stiff cream paper, its outside plain"
HUNSHU = "one folded sheet of cream paper with a thin gold edge, plain"
MINGCE = "one thin stitched booklet bound in plain grey cloth, its cover one even grey all over with only the weave of the cloth on it"
RED = "one folded sheet of plain red paper"
PACKET = "one small flat square packet of folded yellowish oiled paper"
BUCKET = "one plain wooden bucket with a rope handle"
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
# No person on screen (the inserts): this opens their motion so the clips-dh text holds "the set layout stays as it is. "
# once (gen-dh writes "keeps the first frame's set layout and props." there) and the d1 prompt "never the mood. " once.
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# e916 fix1 / e918 review 必改 1 / e919 review 建議: two high round buns, a short ribbon round each, the nape bare.
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with all of her black hair gathered "
         "up into two round buns set high on her head, a short pink silk ribbon wrapped around each bun, the "
         "nape of her neck bare above a pink inner collar, and her light peach-pink silk shoulders; the back of her "
         "head toward us the whole time, her ear the furthest round her head we ever see")
HEADSTILL = "the young woman with the two high round buns keeps her head still, the back of her head toward us the whole shot"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def only_tang(side):
    """e915 s26/s41: a second Tang appeared beside her back. One person with buns, one fixed side."""
    return (f"she is the only young woman in the frame and the only one with two high round buns, and she stays in the {side} "
            f"foreground from the first frame to the last")


def counter_back(rest):
    """Tang Xiaotang behind the counter, seen from behind (rule 3): the camera behind her looks across the counter."""
    return (f"over-the-shoulder medium shot from close behind {TBACK}, standing behind {THE_COUNTER} in the right "
            f"foreground, framed from the waist up, facing across the counter; {only_tang('right')}; {rest}")


SHOTS = [
    # ---- scene 1: day 21, the last of the dusk (set-xuji-pu-dusk-l1). The same moment as e020 s38: Wei Shaoqing over the
    # threshold, Sun Zhanggui at the left door post, the counter on the right with Xu Yan in front of it.
    dict(chapter="帖子與婚書", loc="dusk", cam="Medium-wide shot, slow push in", chars=["xuyan", "weishaoqing", "sunzhanggui"], night="dusk",
         comp=f"medium-wide shot from inside the shop at eye level, the near end of {THE_COUNTER} with {LAMPS} on it in the soft right foreground: {XU}, standing just in front of the counter on the right, framed from the knees up with clear space above his head, his face three-quarter to screen left toward the doorway, never the lens; firm and steady: brows level, eyes hard, jaw set, lips moving evenly between words; beyond him the wide front doorway at the back: in the middle of the doorway {WEI}, one step over the threshold, framed from the knees up, holding open in his right hand at his chest {FAN}, his face three-quarter to screen right toward the young man, never the lens; amused: eyes narrowed, lips closed; at the left door post {SUN}, standing aside, framed from the knees up, his face three-quarter to screen right, eyes half closed, lips closed; behind them the street deep blue with dusk and {EAVE}; {HANDS}; exactly three people",
         lines=[("xuyan", "我這裡只有我的妻子，沒有誰的未婚妻。", "擋在櫃檯前，很穩")],
         motion=f"Xu Yan takes one firm step toward the doorway and sweeps his left arm, the one on the screen-right side of his body, back toward the counter behind him; Wei Shaoqing stops, the open fan halted at his chest; {quiet('Wei Shaoqing')}; {quiet('Sun Zhanggui')}",
         zh="中全景、慢推（接第 20 集 s38 同一刻、同一條軸線：看門時櫃檯在畫右）：前景右是櫃檯一角與兩盞點著的小銅油燈；許硯在櫃檯前（畫右），往門口跨一步、左手（他身體畫右那一側）往後一攔護住櫃檯，臉朝畫左的門口，很穩地說；後面大門口魏少卿（寶藍織金錦袍、髮髻前一塊綠玉）剛跨過門檻、右手在胸前打開素米色紙幾片大金箔的摺扇，停住、嘴閉著；孫掌櫃在左邊門柱旁、嘴閉著。三張臉（拍法 1）：唐小棠、二牛、秦霜在畫外"),
    # Sun Zhanggui may smile (陪笑).
    dict(loc="dusk", cam="Medium shot, slow push in", chars=["sunzhanggui", "weishaoqing"], night="dusk",
         comp=f"medium shot at the wide front doorway at dusk, the dark door post in the soft left foreground: on screen left {SUN}, standing just inside the doorway, turned side-on, framed from the waist up with clear space above his head, his face three-quarter to screen right toward Xu Yan off screen right, never the lens; ingratiating: eyes creased, a thin fawning smile, lips moving smoothly between words; beside him in the middle of the doorway {WEI}, framed from the waist up, holding open in his right hand at his chest {FAN}, his face three-quarter to screen right, never the lens; haughty: chin lifted, eyes half closed, lips closed; behind them the street deep blue with dusk and {EAVE}; {HANDS}; exactly two people",
         lines=[("sunzhanggui", "許老闆，這位是宰相府的公子，魏少卿魏公子。", "笑咪咪")],
         motion=f"Sun Zhanggui bows a little and turns his left hand, the one on the screen-right side of his body nearest Wei Shaoqing, open and palm up toward him as he speaks; {quiet('Wei Shaoqing')}; after the last word Wei Shaoqing snaps the fan shut against his left palm",
         zh="中景、慢推（前景左虛焦門框）：孫掌櫃（綠緞袍、玉帶鉤）在門內畫左、側身，臉朝畫右的許硯（畫外），彎一下腰、左手（靠魏少卿那隻）掌心朝上往身旁的魏少卿一引，陪笑地說（本鏡可以笑）；魏少卿在門口正中、下巴微抬、嘴閉著，說完把摺扇『啪』地合在左掌"),
    # Insert: the chancellor's letter (rule 27). No person: the counter-top crop set-xuji-pu-cabinet-l1.
    dict(loc="insert", cam="Insert close-up, slow push in", chars=[], night="dusk",
         comp=f"insert close-up, the shot opens directly on a man's left hand in a wide sapphire-blue brocade sleeve woven with gold thread, already holding {TIE} a hand's height above the dark wooden counter top from its very first frame; only the hand, its sleeve cuff, the folded paper and the counter top are in the frame; the round brass base of a small oil lamp at the right edge, its warm light across the wood",
         lines=[("weishaoqing", "宰相府的帖子。她叫唐小棠，是我過了定的人。", "拖長音")],
         motion=NOBODY + "the hand slaps the folded paper flat onto the counter top, then two fingers press on it and push it slowly forward across the wood; the paper stays folded, its plain outside up",
         zh="插鏡、慢推（第一格就是手：寶藍織金袖口的左手已經拿著帖子在檯面上方一掌高；送木櫃面裁切 `set-xuji-pu-cabinet-l1` 當櫃檯面）：帖子照拍法 27 寫成一張摺著的硬米色紙、外面素的（稿子的紅封不寫）；『啪』地拍在櫃檯上，兩指按住往前推；紙一直摺著。魏少卿的台詞畫外"),
    # From behind her across the counter (rule 3): Wei Shaoqing's face takes it; she bumps the stool.
    dict(loc="dusk", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "weishaoqing"], nospeak=["tangxiaotang"], night="dusk",
         comp=counter_back(f"one tall plain wooden stool standing just behind her at the right edge of the frame; facing us beyond the counter a little left of the middle {WEI}, standing a few steps inside the shop, framed from the waist up with clear space above his head, the open fan in his right hand at his chest, his face three-quarter to screen right toward her, never the lens; smug: one brow raised, eyes narrowed, lips closed; behind him the doorway deep blue with dusk, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("tangxiaotang", "你怎麼找到這裡的？我躲了半年，誰都沒說。", "發抖")],
         motion=f"the young woman takes half a step back and bumps the tall stool behind her, which rocks on its legs; {HEADSTILL}; she looks straight ahead at Wei Shaoqing the whole shot; {quiet('Wei Shaoqing')}; one corner of his mouth curls",
         zh="【改背後拍】過肩中景、慢推：前景右唐小棠的背影在櫃檯後（兩顆高丸子、短粉緞帶、後頸露出），往後退半步碰到身後的高凳、高凳一晃；頭不動、一直看著魏少卿；櫃檯對面魏少卿挑眉瞇眼、嘴閉著，嘴角一勾。台詞 nospeak，剪接放錄音（原稿『抱著算盤』不寫：拍法 20 算盤只在插鏡）"),
    # He may smile (rule 30).
    dict(loc="dusk_c", cam="Medium close-up, slow push in", chars=["weishaoqing"], night="dusk",
         comp=f"medium close-up of {WEI}, standing a few steps inside the shop, framed from the chest up with space above his head, holding open in his right hand just below his chin {FAN}, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; contemptuous amusement: eyes narrowed, one corner of his mouth curling up, lips moving lazily between words; behind him the doorway and the street deep blue with dusk, {EAVE}, soft",
         lines=[("weishaoqing", "孫掌櫃在書院門口見過妳，早報給我了。", "笑")],
         motion="Wei Shaoqing flicks his eyes once to the door post at screen left, then lets them sweep slowly across the bare shelves before they come back to her; after the last word he fans himself once, smiling",
         zh="中近景、慢推（不送場景圖：近鏡背景虛焦，第 20 集審稿建議 18）：魏少卿右手把摺扇開在下巴下（不遮嘴：要對嘴），眼光往畫左門柱的孫掌櫃一瞟、再慢慢掃過空了的架子，朝畫右的唐小棠（畫外）輕蔑地說（本鏡可以笑）；說完搧一下"),
    # Insert: the Tang marriage paper, folded (rule 27): the script's unfolded sheet with seal frames is never filmed.
    dict(loc="insert", cam="Insert close-up, slow push in", chars=[], night="dusk",
         comp=f"insert close-up, the shot opens directly on a man's left hand in a wide sapphire-blue brocade sleeve woven with gold thread, already laying {HUNSHU} on the dark wooden counter top from its very first frame, beside the round brass base of a small oil lamp burning at the right edge; only the hand, its sleeve cuff, the folded paper, the lamp base and the counter top are in the frame; warm lamp light across the wood",
         lines=[("weishaoqing", "這是唐萬金親筆簽的婚書，她爹親手按的印。", "得意")],
         motion=NOBODY + "the hand smooths the folded sheet flat beside the lamp and taps it twice with two fingers; the sheet stays folded, its plain outside up, its thin gold edge catching the lamp light",
         zh="插鏡、慢推（送木櫃面裁切）：魏少卿的左手（寶藍織金袖口）第一格已經把唐家婚書放在油燈座旁（拍法 27：米色紙細金邊、摺著、只見紙背；稿子『甩開、透出紅印框』不拍，拍法 7），兩指點兩下。台詞畫外"),
    # From behind her: both palms slap the counter (the abacus is not written, rule 20; its click is a sound effect).
    dict(loc="dusk", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "weishaoqing"], nospeak=["tangxiaotang"], night="dusk",
         comp=counter_back(f"both her hands already raised a little above the counter top from the first frame; facing us beyond the counter a little left of the middle {WEI}, framed from the waist up with clear space above his head, the closed fan in his right hand, his face three-quarter to screen right toward her, never the lens; cool: eyes half closed, chin lifted, lips closed; behind him the doorway deep blue with dusk, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("tangxiaotang", "那是你們魏家逼我爹簽的，我爹不肯也得肯！", "眼眶紅，氣到發抖")],
         motion=f"the young woman slaps both palms flat down on the counter top and leans forward over them, her shoulders shaking; {HEADSTILL}; she looks straight ahead at Wei Shaoqing the whole shot; {quiet('Wei Shaoqing')}; he lifts his chin a little higher",
         zh="【改背後拍】過肩中景、慢推：前景右唐小棠背影，兩手第一格已經抬在檯面上方，兩掌『啪』地拍在櫃檯上、往前探身、肩膀發抖；頭不動、一直看著魏少卿；對面魏少卿半閉眼、下巴再抬一點、嘴閉著。稿子『把小金算盤拍在櫃檯上』改成兩掌（拍法 20：算盤只在插鏡；『喀』一聲交給音效）。台詞 nospeak，剪接放錄音"),
    dict(loc="dusk_c", cam="Close-up, slow push in", chars=["weishaoqing"], night="dusk",
         comp=f"close-up of {WEI}, framed from the chest up with space above his head, the fan half closed in his right hand just under his chin, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; sneering: nostrils flaring, eyes narrowed, one corner of his mouth curled, lips moving lazily between words; behind him only the doorway deep blue with dusk, soft",
         lines=[("weishaoqing", "逼的也是簽了。婚書只認字和印，不認委屈。", "笑出聲")],
         motion="Wei Shaoqing snorts once through his nose and taps the half-closed fan lightly under his chin as he speaks; after the last word he smiles thinly",
         zh="近景、慢推（不送場景圖）：魏少卿鼻子裡哼一聲，半合的扇子在下巴下輕敲，冷笑著說（本鏡可以笑）；身後只有暮色的門口"),
    # Over her back (silent): his thought. Her hand on the counter, his a finger's width from it.
    dict(loc="dusk", cam="Over-the-shoulder medium close-up, slow push in", chars=["tangxiaotang", "xuyan"], night="dusk",
         comp=counter_back(f"her right hand resting flat on the counter top; facing us across the counter a little left of the middle {XU}, standing in front of the counter, framed from the chest up with space above his head, his left hand resting on the counter top a finger's width from hers, his face three-quarter to screen right toward her, never the lens; grave and thinking: brows drawn together, eyes searching her, lips pressed together; behind him the dim shop in the dusk, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("xuyan", "宰相府……原來她說躲的那個人，就是他。", "心裡話", "inner")],
         motion=f"Xu Yan turns his face to her and lays his left hand on the counter a finger's width from hers; {SILENT_HE}; he is thinking, not speaking; {HEADSTILL}; she looks down at the counter the whole shot",
         zh="過肩中近景、慢推（從唐小棠背後越過櫃檯拍許硯；她不說話，照背影鏡的寫法）：許硯側過臉看她，左手輕輕放在櫃檯上、離她的手一指寬；全程嘴閉著（心裡話畫外）；她頭不動、低頭看櫃檯"),
    # Wide: Wei Shaoqing and Xiaohe; Xu Yan's unnamed back in the right foreground (rules 1, 2).
    dict(loc="dusk", cam="Wide shot, slow push in", chars=["weishaoqing", "xiaohe"], night="dusk",
         comp=f"wide shot from inside the shop toward the wide front doorway, the near end of {THE_COUNTER} with {LAMPS} on it in the soft right foreground, and in the soft right foreground {XU_BACK}, standing in front of the counter, only his shoulders and the back of his head with a cloth-tied topknot showing; in the middle {WEI}, a few steps inside the doorway, framed full length, holding up at the height of his face in his left hand {MINGCE}, the closed fan in his right hand, his face three-quarter to screen right toward the counter, never the lens; smug: eyes narrowed, one corner of his mouth curling, lips moving between words; at the back by the bare shelves on the left {XIAOHE}, small, holding a bamboo broom in both hands, her face turned toward him, eyes wide, lips closed; behind them the doorway deep blue with dusk and {EAVE}; {HANDS}; exactly three people, the young man in the foreground seen only from behind",
         lines=[("weishaoqing", "還有這個，縣衙配婚名冊的抄本，我託人抄出來的。", "慢條斯理")],
         motion=f"Wei Shaoqing lifts the grey booklet higher into the warm lamp light and gives it one shake as he speaks; {quiet('Xiaohe', 'her')}; Xiaohe's broom stops mid-sweep a little off the floor; the young man in the foreground stays still, the back of his head toward us the whole shot",
         zh="全景、慢推（前景右是櫃檯一角、油燈與許硯的背影，不點名、不送圖，拍法 2）：魏少卿在門內幾步、全身，左手把名冊抄本（拍法 27：薄線裝冊、素灰布面，面上只有布紋）舉到臉的高度、往燈光一抖，得意地說（本鏡可以笑）；後面左邊空架子旁小禾兩手拿竹掃帚、掃帚停在半空、抬頭看他、嘴閉著。唐小棠在畫外（三張臉以內）"),
    # Insert: the closed register under his finger (rule 7: the script's open page with the red ring is never filmed).
    dict(loc="insert", cam="Insert close-up, slow push in", chars=[], night="dusk",
         comp=f"insert close-up, the shot opens directly on a man's forefinger resting on the plain grey cover of {MINGCE}, lying closed on the dark wooden counter top from its very first frame; only the hand in its wide sapphire-blue brocade sleeve cuff, the closed grey booklet and the counter top are in the frame; warm oil-lamp light across the wood",
         lines=[("weishaoqing", "配給許硯的第三個，名冊上寫的是林二丫。", "一字一字")],
         motion=NOBODY + "the forefinger slides slowly down the closed grey cover, stops near its lower edge and taps the cover twice; the booklet stays closed",
         zh="插鏡、慢推（送木櫃面裁切）：第一格就是指尖按在合著的素灰布面名冊上，順著封面往下滑、停住、點兩下（稿子『攤開的名冊、紅圈』不拍：紙上的字一律不拍，拍法 7、27）。台詞畫外"),
    # Her one face (silent): e920 fix1's short ribbons, no long-ribbon angle-b; her hands below the frame (e919 fix1).
    dict(loc="dusk_c", cam="Close-up, slow push in", chars=["tangxiaotang"], night="dusk",
         comp=f"close-up of Tang Xiaotang {TANG}, standing behind the counter, framed from the chest up with space above her head, her hands below the bottom edge of the frame, her face three-quarter to screen left toward the doorway off screen left, never the lens; frightened: skin pale, eyes wide and fixed, inner brows squeezed up, lips pressed together and trembling; behind her only the plain white panelled wall in the dim dusk, the warm lamp glow on her cheek",
         lines=[("weishaoqing", "可林二丫，兩年前就病死了，墳都長草了。", "輕飄飄")],
         motion=f"in the first second the colour drains from her face, her cheeks and lips turning pale; she draws one sharp breath, her shoulders drawing up, her eyes fixed on the doorway; {quiet('Tang Xiaotang', 'her')}",
         zh="近景、慢推（不送場景圖；本集唯一她的臉，不說話）：唐小棠在櫃檯後、胸口以上、兩手在畫面下緣外（稿子『手往後攥緊凳面』不入鏡：手出畫最穩），朝畫左門口看；第一秒臉上血色一下退掉、倒抽一口氣、肩膀一縮、嘴抿著發抖、不笑。魏少卿的台詞畫外"),
    # Low angle: he leans across toward her (rule 30: he may sneer).
    dict(loc="dusk_c", cam="Low-angle medium close-up, slow push in", chars=["weishaoqing"], night="dusk",
         comp=f"low-angle medium close-up from the height of the counter top, the dark edge of the counter and the flame of one small brass oil lamp in the soft foreground: {WEI}, leaning over the counter toward screen right, framed from the chest up with space above his head, {MINGCE} closed in his left hand and the closed fan in his right, the lamp lighting his face from below, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; cold sneer: eyes narrowed, one corner of his mouth curled, lips moving low between words; behind him the dark beams of the shop, soft",
         lines=[("weishaoqing", "死人怎麼嫁人？除非有人冒了她的名。", "壓低聲音")],
         motion="Wei Shaoqing taps the closed booklet once against his right palm and leans closer toward screen right as he speaks; after the last word he holds still, smiling coldly",
         zh="低角度中近景、慢推（從櫃檯高度往上拍，前景虛焦櫃檯邊與一盞油燈的火；不送場景圖）：魏少卿越過櫃檯往畫右的唐小棠（畫外）湊，左手合著的名冊在右掌心敲一下，油燈從下面照臉，壓低聲音冷笑地說"),
    # The system's warning and the bickering (long shot). No blue light (rule 11): the panel is laid on in the cut.
    dict(loc="dusk_c", cam="Close-up, slow push in", chars=["xuyan"], night="dusk",
         comp=f"close-up of {XU}, standing in front of the counter, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes on a point in the air in front of him, never the lens; shocked: eyes narrowing, jaw clenched, brows drawn low; behind him only the plain white panelled wall and the warm glow of the oil lamps, soft",
         lines=[("xitong", "叮。冒名入冊，按律流放。", "冷，宣布"),
                ("xuyan", "流放？她一個姑娘家，要流放到哪裡去？", "心裡話", "inner"),
                ("xitong", "三千里。本系統只報律條，不報辦法。", "冷"),
                ("xuyan", "不用妳報辦法，辦法我自己想。", "心裡話，咬牙", "inner")],
         panel=[("冒名入冊，按律流放", "penalty")],
         motion=f"for the first two seconds Xu Yan's eyes narrow and his jaw tightens; then his brows knot and his eyes dart sideways, searching; from the seventh second his face hardens; from the tenth second he lets out one slow breath and his eyes settle, steady and resolved; {SILENT_HE}; he is listening and thinking, not speaking",
         zh="近景、慢推（長鏡；拍法 11：不寫藍光，面板由剪接疊上；不送場景圖、不送帶笑的角度圖 b）：許硯眼睛一縮、下巴繃緊；接著眉頭一擰、眼睛往旁邊找（心裡問流放到哪）；第七秒起臉一沉（系統回嘴）；第十秒起吐一口氣、眼神定下來；全程嘴閉著（系統與心裡話都畫外）"),
    # Over Wei Shaoqing's unnamed back (rule 2). Xu Yan turns to the counter beyond the right edge (Tang Xiaotang off screen).
    dict(loc="dusk_c", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="dusk",
         comp=f"over-the-shoulder medium shot from close behind {WEI_BACK}, in the left foreground, only the back of his head with a topknot and his shoulder showing, soft; facing us a little right of the middle {XU}, standing in front of {THE_COUNTER}, framed from the waist up with clear space above his head, his face turned three-quarter to screen right toward the far end of the counter beyond the right edge of the frame, never the lens; calm and decisive: brows level, eyes steady, lips moving evenly between words; behind him only the plain white panelled wall and the warm glow of the oil lamps, soft; {HANDS}; exactly two people, the man in the foreground seen only from behind",
         lines=[("xuyan", "小棠，把我們的婚書拿出來，縣衙蓋了印的那張。", "沉著")],
         motion="Xu Yan turns his head toward the far end of the counter at screen right and holds out his left hand, the one on the screen-right side of his body, open and palm up, as he speaks; the man in the foreground keeps his head still, the back of his head toward us the whole shot; after the last word Xu Yan keeps his hand out, waiting",
         zh="過肩中景、慢推（左右照真人軸線對調：前景左是魏少卿的後腦與肩，不點名、不送圖，拍法 2；不送場景圖：他身後是白色板牆與油燈光，圖上是大門）：許硯轉頭朝畫右櫃檯那頭（唐小棠在畫外），左手（他身體畫右那一側）掌心朝上一伸，沉著地說；說完手不收、等著（稿子『唐小棠點一下頭』交給 c16 她遞出婚書）"),
    # Insert: the county paper out of her oiled-paper packet into his palm (hands only).
    dict(loc="insert", cam="Insert close-up, slow push in", chars=[], night="dusk", act=2,
         comp=f"insert close-up, the shot opens directly on two hands above the dark wooden counter top from its very first frame: on the right a small hand in a light peach-pink silk sleeve cuff holding {PACKET}, its flap already folded open, and on the left a man's open palm held out flat in a faded blue-grey cotton sleeve cuff; only the two hands, their sleeve cuffs, the packet and the counter top are in the frame; warm oil-lamp light",
         lines=[],
         motion=NOBODY + f"the small hand draws {RED} out of the oiled packet and lays it in the open palm, and the palm closes gently round it; the red paper stays folded",
         zh="插鏡、慢推（送木櫃面裁切）：第一格就是兩隻手：畫右桃粉袖口的小手拿著摺成方形的黃油紙包（開口已經打開），畫左藍灰袖口的手掌攤平；她從油紙包抽出一張摺著的紅紙（縣衙婚書，只見紙背）放進他掌心，他的手輕輕握住（稿子『從淡杏外衣衣襟拿出』：真人版沒有外衣，拍法 4；無台詞）"),
    dict(loc="dusk", cam="Medium two-shot, slow push in", chars=["xuyan", "weishaoqing"], night="dusk",
         comp=f"medium two-shot across the near end of the counter, the dark counter top in the soft right foreground with {HUNSHU} lying on it: on screen right {XU}, standing in front of the counter, framed from the waist up with clear space above his head, {RED} in his left hand, the one on the screen-right side of his body nearest the counter, his face three-quarter to screen left toward the other man, never the lens; calm and hard: eyes level, jaw set, lips moving firmly between words; on screen left {WEI}, framed from the waist up, the open fan held still at his chest in his right hand, his face three-quarter to screen right toward him, never the lens; wary: eyes narrowed, lips closed; behind them the shop dim in the dusk; {HANDS}; exactly two people",
         lines=[("xuyan", "唐老爺簽的是兩家的私約，從來沒進過官府的名冊。", "一字一句")],
         motion=f"Xu Yan slaps the folded red paper down on the counter beside the cream sheet and presses it forward with his fingers as he speaks; {quiet('Wei Shaoqing')}; the fan stops moving",
         zh="中景雙人、慢推（前景右櫃檯上是唐家婚書）：畫右許硯左手（靠櫃檯那隻）把摺著的紅紙婚書『啪』地拍在唐家婚書旁、手指按著往前推，臉朝畫左一字一句地說；畫左魏少卿扇子停在胸前、瞇眼、嘴閉著（拍法 7：紙只見紙背、摺著）"),
    dict(loc="dusk", cam="Side two-shot medium close-up, slow push in", chars=["xuyan", "weishaoqing"], night="dusk",
         comp=f"side-on medium close-up of two men face to face in front of the counter, a foot apart, the warm glow of the oil lamps on the counter between them in the soft background: on screen right {XU}, framed from the chest up, his face in profile to screen left toward the other man, never the lens; unyielding: eyes level and unblinking, jaw set, lips moving firmly between words; on screen left {WEI}, framed from the chest up, the open fan held up in his right hand covering the lower half of his face, his face in profile to screen right toward him, never the lens; his eyes narrowed above the fan; {HANDS}; exactly two people",
         lines=[("xuyan", "縣衙的婚書在先，配不配婚，是官府的事，不是你家的事。", "寸步不讓")],
         motion=f"Xu Yan leans in an inch closer and speaks, his eyes fixed and unblinking; {quiet('Wei Shaoqing')}; above the fan Wei Shaoqing's eyes narrow further",
         zh="側面雙人中近景、慢推（兩人在櫃檯前面對面、鼻尖一尺，後面虛焦的油燈光在兩人之間）：畫右許硯側臉朝畫左，再湊近一寸、不眨眼、寸步不讓地說；畫左魏少卿摺扇遮住下半張臉、扇子上方瞇眼、嘴閉著"),
    # His smile freezes (rule 30: a losing beat, no smile).
    dict(loc="dusk_c", cam="Close-up, slow push in", chars=["weishaoqing"], night="dusk",
         comp=f"close-up of {WEI}, framed from the chest up with space above his head, the open fan just lowered from his face in his right hand, his face three-quarter to screen right toward Xu Yan off screen right, never the lens; his smile frozen and gone: jaw clenched, a muscle twitching at the corner of his jaw, eyes cold, the corners of his mouth pulled down, lips moving tightly between words; behind him only the doorway deep blue with dusk, soft",
         lines=[("weishaoqing", "說得好聽。冒名的人，我今天先帶走。", "笑沒了")],
         motion="Wei Shaoqing lowers the fan from his face, his jaw twitching, and snaps it shut with one flick of his right hand; then he speaks through tight lips; after the last word his eyes stay cold on him",
         zh="近景、慢推（不送場景圖；拍法 30：輸的一拍不笑）：魏少卿把扇子從臉上放下，笑容僵住、下顎一抽，扇子『啪』地合上，冷著臉說（結尾）"),
    # ---- scene 2: nightfall (set-xuji-pu-ye-l1). The henchmen come in from the doorway on the left.
    dict(chapter="一棍", loc="night", cam="Medium shot, slow push in", chars=["weishaoqing"], night="night",
         comp=f"medium shot just inside the wide front doorway at nightfall, the dark door post in the soft left foreground: {WEI}, standing a little left of the middle, framed from the waist up with clear space above his head, the closed fan in his right hand pointing toward the counter beyond the right edge of the frame, his face three-quarter to screen right, never the lens; cold: eyes hard, lips moving crisply between words; behind him in the doorway {THUGS}, stepping in over the threshold, soft; behind them the street dark blue with night and {EAVE}; {HANDS}",
         lines=[("weishaoqing", "來人，把櫃檯後那位唐姑娘請出來。", "扇子一指")],
         motion="Wei Shaoqing points the closed fan toward the counter at screen right as he speaks; behind him the two burly men step in over the threshold one after the other and stop just inside it",
         zh="中景、慢推（入夜，送 `set-xuji-pu-ye-l1`；前景左虛焦門框）：魏少卿用合起的摺扇往畫右外的櫃檯一指、冷著臉說；身後兩個打手（黑短打、黑布包頭、布鞋、兩手空著、只拍側面與背影、臉在暗處）從門口跨進來（小角色：不點名、不送圖）"),
    # The push, part one (原版必修 21: split in two short shots).
    dict(loc="night", cam="Wide shot, slow tracking shot", chars=["xiaohe"], night="night",
         comp=f"wide shot across the dim shop at night, a stack of plain wooden shutter boards leaning against the wall by the doorway in the soft left foreground: {THUGS}, walking from the doorway on the left toward the counter on the right; in the middle {XIAOHE}, standing in their path with a bamboo broom held across her body in both hands, framed full length, her face three-quarter to screen left toward the men, never the lens; scared but stubborn: brows drawn together, lips pressed tight; the counter with its two oil lamps at the right edge; {HANDS}",
         lines=[],
         motion=f"Xiaohe plants her feet and holds the broom out across the first man's path; he sweeps her aside with one swing of his forearm and she topples backward toward the floor, the broom flying from her hands; {quiet('Xiaohe', 'her')}",
         act=2,
         zh="全景、跟拍（前景左虛焦一疊靠牆的門板）：兩個打手從左邊門口往右邊櫃檯走；小禾（補丁淡紫短襖、紅繩小辮、草兔子塞在腰帶）兩手橫拿竹掃帚擋在他們前面、皺眉抿嘴；第一個打手手臂一撥，她往後倒、掃帚飛出去（原版必修：推倒那一下拆成兩鏡、拍短；無台詞）"),
    # The push, part two: she is already on the floor, crying (never a smile).
    dict(sid="s21b", loc="night_c", cam="Low-angle medium close-up, slow push in", chars=["xiaohe"], night="night",
         comp=f"low medium close-up at floor level: {XIAOHE}, already sitting on the grey stone floor from the first frame where she fell, framed from the waist up, both her hands flat on the floor at her sides, her face three-quarter to screen left, her eyes on the men who pushed her, never the lens; crying: tears welling and running down her cheeks, her chin trembling, the corners of her mouth pulled down; the bamboo broom lying on the floor beside her; behind her the dim shop and the warm glow of the lamps, soft",
         lines=[("xiaohe", "哥！", "短喊，嚇哭")],
         motion="Xiaohe cries out once, her shoulders shaking, then her face crumples into sobs, the corners of her mouth pulled down hard, tears running",
         zh="低角度中近景、慢推（不送場景圖）：小禾第一格已經跌坐在地上、兩手撐地、竹掃帚落在身旁，眼淚湧出、下巴發抖、嘴角往下拉，喊一聲『哥！』後抽泣（原版必修：被推後每鏡寫哭、不笑）"),
    # Qin Shuang's sweep: the staff already in her hands (the grab is in the cut between s21b and s22).
    dict(loc="night", cam="Low-angle medium-wide shot, slow push in", chars=["qinshuang"], night="night",
         comp=f"low-angle medium-wide shot at floor level, the whole action in the frame: on screen right Qin Shuang, {QIN}, already gripping {STAFF} low in both hands from the first frame, framed full length, her face three-quarter to screen left toward the man, never the lens; cold: eyes hard, brows level, jaw set; in the middle {THUG1}, striding toward the counter; {HANDS}; exactly two people",
         lines=[("qinshuang", "再碰她一下，你就躺著出這個門。", "冷")],
         motion="Qin Shuang sweeps the staff low along the floor into the back of the man's ankles; his feet fly up and he falls flat on his back on the stone floor; she presses the end of the staff down on his chest and holds it there, then speaks; after the last word the staff stays on his chest",
         zh="低角度中全景、慢推（整個動作留在畫面裡）：秦霜（腰帶空著，拍法 5：柴刀不寫）第一格已經兩手低握一根比人高的素木長棍（剪接在 s21b 與 s22 之間交代她抄起棍子），貼地一掃打在打手腳踝後，他兩腳離地、仰面摔在地上；她棍頭往下一壓抵住他胸口，冷冷地說"),
    dict(loc="night_c", cam="Close two-shot, slow push in", chars=["xuyan", "xiaohe"], night="night",
         comp=f"close two-shot near the floor: on screen left {XU}, down on one knee, framed from the chest up, both his hands on the little girl's shoulders, his face three-quarter to screen right toward her, never the lens; gentle and worried: brows drawn up, eyes soft, lips moving softly between words; on screen right {XIAOHE}, sitting up on the floor, framed from the chest up, the little straw rabbit already out of her sash and held against her chest in both hands, her face three-quarter to screen left toward him; tears on her cheeks, the corners of her mouth pulled down, lips closed; behind them the dim shop, soft; {HANDS}; exactly two people",
         lines=[("xuyan", "小禾，摔疼哪裡沒有？哥哥看看。", "放軟")],
         motion=f"Xu Yan helps her sit up and touches the back of her head once with his right hand as he speaks; {quiet('Xiaohe', 'her')}; she shakes her head and holds the rabbit tighter, sniffing",
         zh="近景雙人、慢推（不送場景圖）：許硯單膝蹲下、兩手扶著小禾的肩，摸一下她的後腦，放軟地說；小禾坐起、草兔子第一格已經從腰帶拿出來兩手按在胸前、臉上有淚、嘴角往下、嘴閉著，搖搖頭、把兔子按得更緊、吸鼻子"),
    dict(loc="night", cam="Medium shot, slow push in", chars=["qinshuang"], night="night",
         comp=f"medium shot in the dim shop at night: on screen right Qin Shuang, {QIN}, standing, {STAFF} in both hands, framed from the knees up with clear space above her head, her face three-quarter to screen left, never the lens; cold and steady: eyes hard, jaw set, lips pressed together; on screen left {THUG1}, charging toward her with his right fist raised; {HANDS}; exactly two people",
         lines=[("weishaoqing", "一個村姑拿根棍子，也想攔宰相府的人？", "冷笑")],
         motion=f"Qin Shuang turns her wrists and swings the staff round, and its end stops flat against the man's chest; he halts mid-charge and his fist drops; {quiet('Qin Shuang', 'her')}",
         zh="中景、慢推：畫右秦霜兩手握長棍、冷著臉；畫左第二個打手（只拍側背）舉拳衝過來；她手腕一轉，棍頭反過來抵住他胸口，他衝到一半停住、拳頭放下；秦霜嘴閉著（魏少卿的冷笑畫外）"),
    # Erniu does not smile (bible 原版必修 for him; the script: 不笑).
    dict(loc="night", cam="Medium shot, slow push in", chars=["erniu"], night="night",
         comp=f"medium shot at the wide front doorway at night, the black cloth shoes of a man lying on his back on the stone floor in the soft foreground: {ERNIU}, standing in the middle of the doorway, framed from the knees up with clear space above his head, {BAR} already held across his body in both hands from the first frame, one plain wooden shutter board leaning against the door post beside him, his face three-quarter to screen right toward the men, never the lens; fierce and serious: brows knotted, jaw set, eyes glaring, lips moving loudly between words; behind him the street dark blue with night and {EAVE}; {HANDS}",
         lines=[("erniu", "攔不攔得住，先問問我這根門閂！", "大嗓門，不笑")],
         motion="Wang Erniu thumps one end of the door bar down on the stone floor and plants himself across the doorway as he shouts; after the last word he lifts the bar across his chest again, glaring",
         zh="中景、慢推（前景虛焦：倒地打手的布鞋）：二牛站在大門正中，兩手第一格已經橫握一根方木門閂（稿子『先把門板靠上門框再抽門閂』：門板已經靠在門柱邊），把門閂一頭往地上一頓、堵住門口，大嗓門、皺眉咬牙地喊（不笑）"),
    dict(loc="night", cam="Medium close-up, slow push in", chars=["sunzhanggui", "weishaoqing"], night="night",
         comp=f"medium close-up at the doorway at night, the dark door post in the soft left foreground: on screen left {WEI}, framed from the chest up, the open fan stopped at his chest in his right hand, his face three-quarter to screen right, never the lens; his eyes flicking sideways, lips pressed together; just behind him on screen right {SUN}, bending close to his ear, framed from the chest up, one hand cupped beside his mouth, his face three-quarter to screen left toward the young man's ear, never the lens; uneasy: brows pinched, lips moving quickly and low between words; behind them the street dark blue with night, soft; {HANDS}; exactly two people",
         lines=[("sunzhanggui", "公子，這裡是縣城，鬧大了，州府那邊不好說話。", "壓低聲音")],
         motion=f"Sun Zhanggui leans to the young man's ear and whispers, his hand cupped beside his mouth; {quiet('Wei Shaoqing')}; Wei Shaoqing's eyes flick to screen right toward the staff and the door bar and back; the fan stays still",
         zh="中近景、慢推（前景左虛焦門框）：畫左魏少卿扇子停在胸前、眼睛往畫右的棍子與門閂一掃再回來、嘴閉著；他身後畫右孫掌櫃彎腰湊到他耳邊、一手遮在嘴邊、皺眉壓低聲音說"),
    # Over Wei Shaoqing's unnamed back. His cold mouth corner is the script's.
    dict(loc="night_c", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="night",
         comp=f"over-the-shoulder medium shot from close behind {WEI_BACK}, in the left foreground, only the back of his head with a topknot and his shoulder showing, soft; facing us a little right of the middle {XU}, standing at the near end of {THE_COUNTER}, framed from the waist up with clear space above his head, his face three-quarter to screen left toward the man, never the lens; cool and hard: eyes level, one corner of his mouth lifting coldly, lips moving evenly between words; on the counter top beside him {HUNSHU} and {RED}; behind him {LAMPS} on the counter and the plain white panelled wall, soft; {HANDS}; exactly two people, the man in the foreground seen only from behind",
         lines=[("xuyan", "魏公子，要講律，去官府講；要動手，門在那邊。", "嘴角一點冷笑")],
         motion="Xu Yan taps the folded red paper on the counter once with his left forefinger, then lifts his chin toward the doorway at screen left as he speaks; the man in the foreground keeps his head still, the back of his head toward us the whole shot; after the last word Xu Yan holds his gaze",
         zh="過肩中景、慢推（前景左魏少卿的後腦與肩，不點名、不送圖；不送場景圖）：許硯第一格已經站在櫃檯這頭（稿子『把小禾交到秦霜身後再走回來』在剪接裡省掉），左手食指在紅紙婚書上點一下，再往畫左的門口一抬下巴，嘴角一點冷笑地說"),
    # His smile comes back (rule 30). Xu Yan's unnamed dark shoulder in the right foreground.
    dict(loc="night_c", cam="Medium close-up, slow push in", chars=["weishaoqing"], night="night",
         comp=f"medium close-up of {WEI}, standing in the shop at night, framed from the chest up with space above his head, holding together in his left hand from the first frame {HUNSHU}, {TIE} and {MINGCE}, the closed fan in his right hand; in the soft right foreground the dark shoulder of {XU_BACK}; his face three-quarter to screen right toward him, never the lens; his smile coming back: eyes narrowed, the corners of his mouth curling up, lips moving lazily between words; behind him the doorway dark blue with night, soft; {HANDS}; exactly two people, the young man in the foreground seen only from behind",
         lines=[("weishaoqing", "好，那就照你說的，去官府講。", "笑回來")],
         motion="Wei Shaoqing slides the papers away into his wide left sleeve, then flicks the fan open with his right hand and speaks, smiling; the young man in the foreground stays still, the back of his head toward us the whole shot",
         zh="中近景、慢推（不送場景圖；前景右許硯的暗肩，不點名、不送圖）：魏少卿左手第一格已經把唐家婚書、帖子、名冊三樣疊在一起拿著，收進左袖，右手『唰』地打開扇子，笑回到臉上地說（本鏡可以笑）（結尾）"),
    # ---- scene 3: the bucket at the back door. No line.
    dict(sid="s28b", chapter="後門", loc="night", cam="Medium shot, slow tracking shot", chars=["weishaoqing"], night="night", act=3,
         comp=f"medium shot in the shop at night, the rounded end of {STAFF} held level in the soft left foreground: {WEI}, standing in front of the counter, framed from the knees up with clear space above his head, the open fan in his right hand, his face three-quarter to screen right; alert: head lifting, eyes narrowing; beyond him in the far right corner of the white panelled wall one plain dark wooden back door, closed; {LAMPS} on the counter beside him; {HANDS}",
         lines=[],
         motion=f"Wei Shaoqing stops and turns his head toward the back door at the right, then walks slowly toward it, fanning himself, his back turning to us; the end of the staff in the foreground swings round to follow him; {quiet('Wei Shaoqing')}",
         zh="中景、跟拍（前景左虛焦是秦霜長棍的棍尖，人在畫外）：後門外『咚』一聲（音效），魏少卿停住、轉頭看畫右遠角那扇素木後門（第 20 集 s33 阿令出去的那扇），一邊搖扇一邊往那裡走、背轉過去；棍尖跟著他轉（無台詞）"),
    # His point of view through the back door: the free crop set-xuji-houyuan-ye-l1. The fan tip pushes the door.
    dict(loc="yard", cam="Point-of-view medium shot, slow push in", chars=["aling"], night="yard", act=2,
         comp=f"point-of-view shot through a back door being pushed open, the dark edge of the plain wooden door in the soft left foreground, the tip of a closed folding fan of plain cream paper pressing against it from the lower left edge of the frame: beyond it A-ling, {ALING}, standing at the round brick well on the right, framed from the knees up, both her hands on the well rope, {BUCKET} just set on the brick rim of the well, her face turned down toward the bucket, never the lens; still and wary: eyes lowered, lips closed; behind her the brick wall in deep blue shadow and the narrow stone path running away on the left to the small glowing lantern; {HANDS}",
         lines=[],
         motion=f"the door swings slowly open, pushed by the fan tip; A-ling's hands stop on the rope; she goes still, her head turning a little toward the doorway, her eyes still lowered, as if she feels someone watching; {quiet('A-ling', 'her')}",
         zh="主觀（魏少卿推開後門往外看）、慢推（送免費裁切的後院夜圖 `set-xuji-houyuan-ye-l1`：磚井、木架、草頂、右邊磚牆、左邊石板小路盡頭一盞燈籠）：前景左虛焦是門板邊，一把合起的素米色紙摺扇的扇尖從左下把門推開；阿令（灰白布裙、木簪，沒戴面巾，拍法 21）在畫右井邊、兩手抓著井繩、木桶剛擱上井沿，手停住、頭微微轉向門口、眼睛仍垂著（不看鏡頭）（無台詞）"),
    dict(loc="night_c", cam="Medium close-up, slow push in", chars=["weishaoqing"], night="night",
         comp=f"medium close-up of {WEI}, standing in the open back door of the shop at night, framed from the chest up with space above his head, the closed fan in his right hand still resting against the door edge, his body leaning out through the doorway, his face in profile to screen right toward the yard beyond the right edge of the frame, never the lens; intrigued: peach-blossom eyes narrowing, his smile half gone, lips moving slowly between words; behind him the dim shop and the warm lamp glow, soft; the cold blue night light from the yard on his face",
         lines=[("weishaoqing", "等等，井邊那位姑娘，我們是不是在哪見過？", "笑收掉一半")],
         motion="Wei Shaoqing stops the fan in mid-air, narrows his eyes and takes one step forward through the doorway as he speaks; after the last word he holds still, staring",
         zh="中近景、慢推（不送場景圖）：魏少卿在推開的後門邊、扇子還抵著門板、身子往門外探，側臉朝畫右的後院，扇子停在半空、桃花眼瞇起、往前一步，笑收掉一半地問；說完盯著不動"),
    dict(loc="yard", cam="Medium shot, slow push in", chars=["aling"], night="yard", act=3,
         comp=f"medium shot in the small back yard at night: A-ling, {ALING}, standing at the round brick well, framed from the waist up with clear space above her head, {BUCKET} held in her right hand just above the brick rim of the well, her face three-quarter to screen left toward the back door off screen left, never the lens; cold and guarded: eyes lowered, brows level, lips pressed together; behind her the brick wall in deep blue shadow and the lantern glow far down the narrow path, soft; {HANDS}",
         lines=[],
         motion=f"A-ling sets the bucket down on the well rim, lowers her eyes and pulls her left sleeve down over her wrist with her right hand, then turns away and walks off into the dark shadow along the brick wall, her back to us; {quiet('A-ling', 'her')}",
         zh="中景、慢推（送後院夜圖；稿子的近景改中景：她要走出去）：阿令把木桶放在井沿，垂下眼，右手把左袖往下拉蓋住手腕，轉身走進磚牆的影子裡、背對我們（原版建議：只轉身走、不甩頭）（無台詞）"),
    # Over Wei Shaoqing's unnamed shoulder; his cold half-smile is the script's.
    dict(loc="night_c", cam="Medium shot, slow tracking shot", chars=["xuyan"], night="night",
         comp=f"medium shot at the back door of the shop at night: {XU}, standing with his back to one plain dark wooden back door in the white panelled wall, framed from the waist up with clear space above his head, his left hand behind him already on the edge of the half-open door, his face three-quarter to screen left toward the man in the foreground, never the lens; cold amusement: eyes hard, the corners of his mouth lifting a little, lips moving evenly between words; in the soft left foreground the sapphire-blue brocade shoulder and the back of the head of {WEI_BACK}; {HANDS}; exactly two people, the man in the foreground seen only from behind",
         lines=[("xuyan", "魏公子，看這邊。我家的人，你一個都不認得。", "嘴角帶笑、眼神冷")],
         motion="Xu Yan pulls the back door shut behind him with his left hand and squares his shoulders in front of it as he speaks; the man in the foreground keeps his head still, the back of his head toward us the whole shot",
         zh="中景、跟拍（不送場景圖；前景左魏少卿的肩與後腦，不點名、不送圖）：許硯擋在後門前，左手第一格已經在半開的門邊，反手把後門闔上、站定，嘴角帶笑、眼神冷地說"),
    dict(loc="night_c", cam="Close-up, slow push in", chars=["weishaoqing"], night="night",
         comp=f"close-up of {WEI}, framed from the chest up with space above his head, the closed fan in his right hand at his chest, his face three-quarter to screen right toward Xu Yan off screen right, never the lens; amused and dangerous: eyes narrowed, one corner of his mouth curling, lips moving lazily between words; behind him the dim shop, soft",
         lines=[("weishaoqing", "不認得？那我回去，慢慢想。", "瞇眼")],
         motion="Wei Shaoqing gives one short laugh through his nose, turns the closed fan half a circle in his palm and speaks; after the last word his eyes stay narrowed on him",
         zh="近景、慢推（不送場景圖）：魏少卿短短笑一聲（鼻子裡），扇子在手心轉半圈，瞇眼地說（本鏡可以笑）"),
    # From behind her: her hand already on his sleeve (contact as a state).
    dict(loc="night", cam="Over-the-shoulder medium close-up, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="night",
         comp=counter_back(f"her right hand already holding the edge of his left sleeve across the counter from the first frame; facing us across the counter a little left of the middle {XU}, standing in front of the counter, framed from the chest up with space above his head, his face three-quarter to screen right toward her, never the lens; worried: brows drawn together, eyes on her, lips pressed together; behind him the dim shop and the dark blue doorway, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("tangxiaotang", "他說要去官府講，許硯，我們拿什麼擋？", "小聲")],
         motion=f"the young woman tugs at his sleeve and leans a little over the counter toward him; {HEADSTILL}; she looks straight ahead at him the whole shot; {quiet('Xu Yan')}; his eyes soften",
         zh="【改背後拍】過肩中近景、慢推：前景右唐小棠背影，右手第一格已經隔著櫃檯抓著許硯的左袖，拉一下、往前探；頭不動、看著他；對面許硯皺眉、嘴閉著、眼神放軟。台詞 nospeak，剪接放錄音"),
    dict(loc="night", cam="Over-the-shoulder medium close-up, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="night",
         comp=counter_back(f"both her hands held out open, palms up, just above the counter; facing us across the counter a little left of the middle {XU}, standing in front of the counter, framed from the chest up with space above his head, {RED} held in both his hands, his face three-quarter to screen right toward her, never the lens; steady and gentle: eyes calm, brows level, lips moving low between words; behind him the dim shop and the dark blue doorway, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("xuyan", "先別怕。他要走官府，就得照律來，不能搶。", "低，很穩")],
         motion=f"Xu Yan lays the folded red paper in her open hands as he speaks, and she draws it in against her chest; {HEADSTILL}; she looks straight ahead at him the whole shot",
         zh="過肩中近景、慢推（從唐小棠背後拍；左右照軸線，稿子『前景左』改右）：許硯兩手拿著摺好的紅紙婚書（第一格已經從櫃檯拿起摺好），放進她攤開的兩手裡，低而穩地說；她把婚書收到胸前（油紙包在剪接外）；頭不動"),
    # Wide: Erniu and Sun Zhanggui; Wei Shaoqing's unnamed back walks to the threshold (rules 1, 2). No line.
    dict(loc="night", cam="Wide shot, slow push in", chars=["erniu", "sunzhanggui"], night="night", act=3,
         comp=f"wide shot from inside the shop toward the wide front doorway at night: in the middle {WEI_BACK}, walking toward the doorway, fanning himself, only his back and the back of his head with a topknot showing; ahead of him {THUGS}, stepping out over the threshold, the second one limping; at the left door post {ERNIU}, framed from the knees up, {BAR} upright in his right hand, his face three-quarter to screen right toward the men, never the lens; grim: brows knotted, lips pressed together; just outside the doorway on the left {SUN}, standing back, small, his face toward the doorway, lips closed; beyond them the street dark blue with night and {EAVE}; {HANDS}",
         lines=[],
         motion=f"the two burly men step out into the street first, the second one limping; the young man in blue walks to the threshold and stops on it; Wang Erniu steps one pace aside, the bar held upright; {quiet('Wang Erniu')}; {quiet('Sun Zhanggui')}",
         zh="全景、慢推（看大門）：中間魏少卿的背影一路搖扇走到門檻（不點名、不送圖，拍法 2）；兩個打手先出門、第二個一跛一跛；左邊門柱旁二牛右手直握門閂、讓開一步、皺眉；門外左邊孫掌櫃退在一旁。唐小棠、秦霜、小禾在畫外（三張臉以內）（無台詞）"),
    # The ending: on the threshold he turns back (rule 30: he may sneer). Xu Yan's unnamed shoulder in the right foreground.
    dict(loc="night", cam="Low-angle medium close-up, slow push in", chars=["weishaoqing"], night="night",
         comp=f"low-angle medium close-up from the height of the threshold: {WEI}, standing on the threshold of the wide front doorway at night, framed from the waist up with clear space above his head, his body turned toward the street and his head turned back over his shoulder toward the shop, the closed fan in his right hand; the dark shoulder of {XU_BACK} in the soft right foreground; his face three-quarter to screen right, looking past the young man's shoulder toward the counter beyond the right edge of the frame, never the lens; cold sneer: eyes narrowed, one corner of his mouth curling, lips moving slowly between words; behind him the street dark blue with night and {EAVE} glowing behind his head; {HANDS}; exactly two people, the young man in the foreground seen only from behind",
         lines=[("weishaoqing", "三日後，州府來拿冒名犯。許老闆，記得開門。", "回頭，一字一字")],
         motion="Wei Shaoqing points the closed fan past the young man's shoulder toward the counter beyond the right edge of the frame and speaks one word at a time; after the last word he lowers the fan and holds the look, smiling coldly",
         zh="低角度中近景、慢推（門檻高度往上拍；送入夜鋪子圖，正是看大門的視線）：魏少卿站在門檻上、身子朝街、回頭，用合起的摺扇越過前景右許硯的暗肩（不點名、不送圖）指向畫右外的櫃檯與唐小棠，一字一字冷笑地說（本鏡可以笑）；身後藍色夜街與屋簷下的燈籠逆光（結尾；懸念交給第 22 集）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e021-r2/script.md`（c01–c37 對應 s01–s37，c28b 是 s28b；c21 拆成 s21、s21b；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-16）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e021-e030.md`（拍法 1–30 條）。第 3 篇章〈搶親〉第一集。",
    "- 內部工作編號 921（`hailuo/{ff,clips}-dh-e921.json`、`colab/runs/e921/extras.json`、`colab/runs/e921-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e921-dh/`）；發布 slug `zhong-tian-qu-qi-e021-r2`。不放集數、不放片名卡；s01 接第 20 集 s38 同一刻、同一條軸線（**看大門時櫃檯在畫右**：魏少卿、孫掌櫃、門口、打手、二牛在畫左、朝畫右看；許硯在櫃檯前、唐小棠在櫃檯後，在畫右、朝畫左看；CG 稿的左右整集對調）。s37 交給第 22 集第一場（隔天近午，客棧上房）。",
    "- 照第 20 集審稿後的寫法一開始就照做：`OFFSCREEN_SPEECH = False`；`quiet()` 只管嘴；背景寫在場的東西（拍法 18）；道具與接觸寫在第一格；不用手指指人（魏少卿用合起的扇子指）；紙照拍法 27 每鏡同一句：帖子＝摺著的硬米色紙、唐家婚書＝摺著的米色紙細金邊、名冊抄本＝合著的薄冊素灰布面、縣衙婚書＝摺著的紅紙、油紙包；稿子 c06 甩開的婚書與 c11 攤開的名冊都不拍（拍法 7）。",
    "- **唐小棠不露嘴說話**：c04、c07、c34 三句與不說話的 c09、c35 都從她背後越過櫃檯拍（nospeak，spec 拿掉她三張圖與身分句；兩顆高丸子、短粉緞帶、後頸露出、頭不動）；她唯一的臉是 c12（不說話、臉色退掉；短緞帶、不送長緞帶的側面圖 angle-b；兩手在畫面外）。**小金算盤不入鏡**（拍法 20 只在插鏡）：c01 抱著與 c07 拍在櫃檯上改成她的兩掌，『喀』交給音效。",
    "- **一鏡最多三張臉**：c01 許硯、魏少卿、孫掌櫃（唐小棠、二牛、秦霜在畫外）；c10 魏少卿、小禾加前景許硯背影；c36 二牛、孫掌櫃加魏少卿背影。過肩與剪影前景都不點名、不送圖：許硯 c10、c28、c37，魏少卿 c15、c27、c32、c36。兩個打手只拍側面與背影、臉在暗處、空手；秦霜長棍、二牛門閂每鏡同一句；秦霜腰帶空著（柴刀不寫，拍法 5）。**小禾被推倒拆成 s21、s21b 兩鏡**，之後每鏡寫淚與嘴角往下（原版必修）。",
    "- 場景（協調者 2026-11-16 決定，每張放大看過）：第一場 s01–s19 黃昏送 `set-xuji-pu-dusk-l1`（接第 20 集 s34–s38）；第二、三場入夜送 `set-xuji-pu-ye-l1`（篇章試鏡 37033：只改光，右牆前櫃檯上兩盞小銅油燈、門外紅光）；後院 s29、s31 送免費裁切 `set-xuji-houyuan-ye-l1`；四支紙的插鏡（s03、s06、s11、s16）送木櫃面裁切 `set-xuji-pu-cabinet-l1` 當檯面；近鏡與許硯朝畫左的中景（s15、s27、s32）不送場景圖。後門寫在右邊白板牆的遠角（第 20 集 s33 阿令出去的那扇；聖經寫『左牆木架盡頭』，但第 20 集已經拍在右邊）。**不需要試鏡**。",
    "- 長鏡要買的秒數（BUY）：照 36 句錄音核過（`~/mokaair-work/videos/zhong-tian-qu-qi-e921-dh/audio`，faster-whisper 一次一支逐句聽寫；見 `r2.py` 的 BUY 註解）：**s14（系統、心裡話、系統、心裡話四句約 12.4 秒，一支裝得下、不拆）買 12 秒**；s02（孫掌櫃開頭一聲笑、約 6.5 秒）、s10（約 6.3 秒）、s22（先掃倒再說）、s28（先收紙開扇再說）、s37（一字一字約 6.4 秒）買 8 秒；其餘 6 秒。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音長度＋0.5 秒為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯、唐小棠（l1 交領；只在 s12）、魏少卿、孫掌櫃、秦霜、小禾、二牛、阿令（l1，沒戴面巾，拍法 21）的 l1 與有的角度圖；許硯帶笑的 angle-b 只留在 s27、s32（嘴角冷笑）。場景見上面。",
    "- 共用檔：都沒改（說話的人都在 `build-r2.py` 的 `EN`；沒有新場景；`gen-dh.mjs`、`pilot.py`、`cast.json` 不動；打手不說話、沒有 `MINOR`）。",
    "- `colab/runs/e921/extras.json`（照第 20 集：畫面不放字幕那句；拿掉秦霜的柴刀；魏少卿外貌拿掉常帶冷笑與手上的扇子、玉冠改髮髻前一塊綠玉；小禾兔子塞在腰帶；二牛不寫空手；孫掌櫃拿掉否定名詞）與 `colab/runs/e921-live/spec.json`（`mkspec.py` 產生；種子 9211101／9211102）。",
    "- 免費準備：scratchpad `prep921.sh`（`DRY=1 … st1-ep.sh 921` → `pilot.py` → `retake.py` → `colab-jobs.json` 加 output_path、套 swap_pictures（絕對路徑）→ 逐鏡查送的場景圖與人物圖 → 精修用的分隔句（clips-dh 的『the set layout stays as it is. 』、d1 的『never the mood. 』與『One continuous shot.』各一次）→ `preflight-prompts.py` → 否定名詞與會長字的名詞掃描）。",
    "- 配樂：第一場低沉的 suspense，c11『林二丫』、c18『官府的事』各一個重音；第二場短促的打鬥 cue，c22 一棍一個重音、c28 收住；第三場冷的低音弦，c30『見過？』一個輕的重音、c37 一個大重音後收。音效見 script.md〈音樂與音效〉（c04 高凳、c07 算盤『喀』改成兩掌拍櫃檯、c28b 水桶『咚』）。",
]

# Long shots: seconds to buy. Measured 2026-11-16 against the 36 recordings (~/mokaair-work/videos/zhong-tian-qu-qi-e921-dh/audio;
# wave length and silencedetect -35 dB; e013's test: a shot holds (buy - 0.3) x 1.1 s of speech, half a second between lines,
# so 6 s holds 6.27 s, 8 s 8.47 s and 12 s 12.87 s). faster-whisper medium read every take back, one clip per process,
# numpy input (scratchpad fw921.txt; audio/README-retakes.txt).
# 12 s: s14 (the system a14 2.40 + Xu Yan's thought a15 3.28 + the system a16 2.49 + his thought a17 2.75 + 3 x 0.5 =
#       12.42 s; one clip, no split; the script's long-shot list buys 12 too). His beats follow the lines: a15 from about
#       2.9 s, a16 from about 6.7 s, a17 from about 9.7 s (the motion's "seventh" and "tenth second").
# 8 s:  s02 (a02 6.46 s: Sun Zhanggui opens with a short laugh, then the fan snaps shut after the line), s10 (a10 6.31 s),
#       s22 (a24 3.12 s after the sweep and the fall, about 2.5 s of action first), s28 (a30 3.86 s after the papers go into
#       the sleeve and the fan opens), s37 (a36 6.40 s, said one word at a time).
# 6 s:  every other line (0.37-6.06 s of speech; the tightest s06 a06 6.06 s over the insert, s12 a12 5.89 s, s26 a28
#       5.61 s); the silent shots s16, s21, s28b, s29, s31, s36 take gen-dh's 6 s.
# Re-recorded once (first takes in audio/take1/): a11 (名冊 heard 名字), a17 (報 missing), a18 (縣衙 heard 信仰, an extra 一),
# a26 (一個 heard 你個). The retakes read right (a17 with a trailing 啊 that whisper may add); see README-retakes.txt.
BUY = {"s02": 8, "s10": 8, "s14": 12, "s22": 8, "s28": 8, "s37": 8}
