"""Episode 22 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e022-r2/script.md
(c01-c41 = s01-s41; the CG-era r2 script), including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and
「真人版的改動（2026-11-16）」, which override the tables. Every line is the script's, word for word; only the staging changes.
Bible: production/r2-bible-e021-e030.md (rules 1-30, the 21->22 and 22->23 hand-overs, the picture table). The second episode
of arc 3 〈搶親〉: the next day at the county inn, dinner at the Xu house, Tang Xiaotang's empty room, the ferry landing.

Written from the start the way e021-r2/r2.py stands AFTER its independent review (../e021-r2/review.md), with the e920 and
e919 fix1 lessons (colab/runs/e920-live/fix1/mkspec.py, e919-live/fix1/mkspec.py):
- OFFSCREEN_SPEECH = False (rule 15): every shot with an off-screen line, a thought or a system line writes the silence of
  each person on screen (quiet(), SILENT_HE).
- Name only what should be drawn (e920 fix1: "books" drew books): the script's ten account books on her table are written as
  the room picture draws them, two low stacks of thin flat packets wrapped in plain pale brown cloth (PACKS; e021 review:
  the register became a grey cloth packet); her letter of divorce is rule 27's "one sheet of plain paper folded in three"
  (XIUSHU), only folded or its plain blank back, never its written face (rule 7). No word that grows text on paper.
- Rule 18: nothing negated by name. Hands in sleeves; every prop in a named hand from the first frame.
- Tang Xiaotang never speaks on camera (rule 3): every one of her lines on screen is from behind her (TBACK, nospeak; spec
  drops her pictures and identity sentence): s01, s03, s05, s09, s12 at the inn; s13, s15, s17, s20, s25 at dinner. Her one
  face is s14 (silent, the sweet smile with reddened eyes while Xiaohe speaks; l1 and angle-a only, the short ribbons).
  s40 on the boat is her back under the canopy (her thought; no picture, no name).
- The gold abacus (rule 20) only in the insert s19, the prop picture prop-jinsuanpan-l1 in the set slot and e920 fix1's
  long flat abacus sentence (the palm-sized wording drew a small upright one); never written on her elsewhere.
- No more than three named faces (rule 1): s13 Qin Shuang and A-ling with Tang's back; s25 Xu Yan, Qin Shuang, A-ling with
  Tang's back walking away (Xiaohe out of frame). Unnamed foregrounds get no picture (rule 2): Xu Yan's shoulder in s23, the
  two women's backs in s34, Qin Shuang's shoulder in s36, Qin Shuang small in the house doorway in s38, Xu Yan's back in s41.
- Smiles only where the script allows them: Wei Shaoqing s02, s06, s08, s10, s12 (rule 30; he wins this episode); Tang
  Xiaotang's one face s14 (the script's c13-c25 sweetness); Xiaohe s14; Xu Yan s18 (puzzled) and s33 (one laugh through
  the nose, eyes wet). Every other face is a set expression.
- Nobody is flipped (rule 9); sides are screen left/right.

THE AXES (rule 29: the set picture decides; the script's CG sides are re-placed where the live pictures differ):
- Inn (set-kezhan-l1): the window and the long bench under it on the LEFT, the square table in the middle with the clay
  teapot and two cups, the folding screen at the back, the closed double door in the RIGHT wall. Wei Shaoqing sits on the
  bench under the window (the script's carved chair is the picture's bench), looking screen right; Tang Xiaotang stands
  right of the table, her back to the door, looking screen left. The camera stays on the door side.
- Dinner (set-xujia-wu-ye-l1): the picture shows a mud-brick room, one candle on a small dark table, a window in the back
  wall, a big clay jar in the left corner; no doorway in it. Xu Yan and Xiaohe sit on the left of the table, Qin Shuang at
  its near left end, A-ling on the right; the doorway to the stove room is beyond the RIGHT edge (Tang comes and goes
  there), the dark passage to the bedrooms beyond the LEFT edge. The script's pair of red candles and oil lamp are the
  picture's one red candle. The word for that room is never written ("kitchen" would send the stove-room picture).
- Corridor (set-xujia-zoulang-l1): posts in the left foreground, the doors along the right wall (the script's c27 already).
- Her room (set-xujia-tangfang-l1): the door in the LEFT wall, the bed along the back wall under a small paper window that
  glows pale grey and is shut (the script's open window is not in the picture), the small table in the RIGHT foreground with
  two stacks and one candle. So Xu Yan is at the table on the right and Qin Shuang and A-ling come to the door on the left
  (the script's CG sides are swapped). The candle is hers, "burnt low" (bible rule 29); his oil lamp stays beside it.
- Night yard (set-xujia-yuan-ye-l2): the house door on the left, the yard gate in the middle of the back wall under its own
  little tiled roof, one round white paper lantern hanging there; Qin Shuang's 「燈籠就在屋簷下」 is that eave. The persimmon
  fruit is on the picture (accepted; the shot is fogged).
- Ferry landing (set-dukou-ye-l1): the old pier from the LEFT over the water, still water and fog on the right, far reeds;
  the picture has no boat, the boat is written ("one small boat with an arched woven-bamboo canopy", bible rule 23).
  The boat (set-chuan-ye-l1): the arched woven canopy, one paper lantern on a bamboo pole at the bow.

PLACES (the coordinator's decisions, 2026-11-16; every picture looked at full size; script.md 〈真人版的改動〉):
- Inn s01, s03, s05, s10, s12: set-kezhan-l1; the three inserts s04, s07, s11: the free crop set-kezhan-table-l1 (the
  table top, teapot and cups); close shots (s02, s06, s08, s09) none.
- Dinner s13, s14, s17, s24, s25: set-xujia-wu-ye-l1 (swapped for set-xujia-wu-l1); the insert s19: prop-jinsuanpan-l1 in
  the set slot (rule 20); close shots and s20 none.
- Corridor s27: set-xujia-zoulang-l1. Her room s28, s34, s37: set-xujia-tangfang-l1 (a placeholder link for the CG id in the
  refs-dh-e922 folder, as e909); the inserts s29, s31: the free crop set-xujia-tangfang-table-l1; close shots none.
- Yard s38: set-xujia-yuan-ye-l2. Ferry s39, s41: set-dukou-ye-l1 (swapped for set-dukou-l2); boat s40: set-chuan-ye-l1
  (swapped for set-dukou-l2: the boat prompt says "ferry landing" so gen-dh gives a set that has a live picture; pilot.py
  has no plain set-chuan-l1).
- gen-dh SET phrases: "county inn guest room", "Inside the farmhouse of the Xu family" (never the word for the stove
  room), "inside corridor of the Xu farmhouse", "first bedroom of the Xu farmhouse", "night yard of the Xu farmhouse",
  "ferry landing" (never "small ferry boat", which would take the CG boat id first).
- Inserts and shots with nobody named (s04, s07, s11, s19, s28, s29, s31, s40, s41) open their motion with NOBODY, so the
  clips-dh text holds "the set layout stays as it is. " once and the d1 prompt "never the mood. " once.
- Shared files: no code changed (every speaker is in build-r2.py's EN; no new gen-dh place; cast.json untouched). Two new
  free crops in refs-live (new ids with their own l1, rule 19; README paragraph).
"""
EP = 922  # internal working number; the published slug is zhong-tian-qu-qi-e022-r2
SLUG = "zhong-tian-qu-qi-e022-r2"
EP_TITLE = "她自己寫了休書，他提燈追到渡口（重製版 r2）"
OUTLINE_SECONDS = 205  # script.md: 205 s, 41 shots (12 + 14 + 12 + 3)
TARGET_MINUTES = [3, 4]
TITLE = "妻子寫休書，律上不算｜種田娶妻打天下 第22集（重製版）"
DESCRIPTION = "唐小棠一個人走進縣城客棧，把五錠金子倒在魏少卿桌上：這是我全部的家當，我拿它買我自己。魏少卿用摺扇把金子推回去：宰相府不缺金子，我要的是人。三日內，她自己到縣城碼頭上他回京的船，他就不再碰許家。傍晚回到柳溪，她帶回滷肉、給每個人夾菜，第一次叫許硯「相公」。她一回房，阿令低聲說：她今晚會走，子時有一班船。亥時末許硯去敲門，房裡沒人，帳冊疊得整整齊齊，上面壓著一封她自己落款的休書。許硯笑出一聲又紅了眼：妻子寫休書，律上不算。他撕了休書，提著燈籠追到渡口，小船剛離岸，船上的人抱著膝，沒有回頭。《種田娶妻打天下》第 22 集（重製版）。"
THUMB = ("妻子寫休書，律上不算", "s33")
CHARACTERS = ["xuyan", "tangxiaotang", "weishaoqing", "qinshuang", "aling", "xiaohe", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: cold sparse strings in a grey inn room, one light accent as gold is pushed back and one on a deadline; then a warm homely dinner cue that thins out to a low held note when a quiet warning is spoken, one soft accent at the end; then wind and a few celesta notes in an empty room at night, one accent on a firm word, one electronic sting, then a low drum pulse building; then a single long erhu note over fog at a river landing, one accent on a final cry before it fades; ancient Chinese rural drama, no vocals"

# Places (gen-dh SET phrases in the first words of each LOC; see the docstring).
BENCH = "a long low plain wooden bench under the window"
TABLE_INN = "the square dark-red wooden table"
TEA = "one brown clay teapot and two small clay cups"
INN = ("a wide window in the left wall with one dark wooden lattice shutter folded back, grey tiled roofs and a flat white overcast "
       f"sky beyond it, {BENCH}, a square dark-red wooden table in the middle of the room with {TEA} on it, a small square side "
       "table and a four-panel folding screen of plain cream panels against the dark back wall, a closed double door of dark wood "
       "in the right wall, dark wooden walls and a dark plank floor")
WU = ("rough mud-brick walls, dark beams and thatch overhead, a small square window in the back wall showing deep blue night, "
      "one large dark clay water jar in the left corner, loose dry straw on the earth floor, one low square dark wooden table in "
      "the middle with low wooden stools around it, one red candle burning in a small holder on the table among clay bowls and plates")
CORR = ("dark wooden posts along the left, a row of plain closed wooden doors along the right wall with small candles burning on "
        "iron brackets beside them, an uneven stone-paved floor, an open doorway at the far end with cold blue night beyond it")
ROOM = ("a plain dark plank door in the left wall, a narrow wooden bed along the back wall with a quilted pink cover lying smooth "
        "and flat and a quilted pink pillow, a small shut paper window above the bed glowing pale grey, a small square wooden table "
        "in the right foreground, rough cracked plaster walls")
PACKS = "two low neat stacks of thin flat packets wrapped in plain pale brown cloth"
CANDLE_LOW = "one short white candle burnt low"
YARD = ("the thatched house with its dark open doorway on the left, a woodpile against its wall, the yard gate of wooden planks in "
        "the middle of the back wall under its own little tiled roof, one round plain white paper lantern hanging from a hook under "
        "that little roof, a persimmon tree, a round stone well in the right foreground, a mud wall on the right, everything "
        "under thin drifting grey fog")
PIER = ("an old wooden pier on thin posts running out over the water from the left, a few tall bare wooden poles standing up "
        "along it, flat still dark water filling the right, a low line of reeds far off on the right fading into the fog")
LOC = {
    "inn": f"In the county inn guest room upstairs on an overcast late morning: {INN}; cold flat grey daylight from the window on the left, the room cool and dim",
    "inn_c": "In the county inn guest room upstairs on an overcast late morning, cold grey window light from the left",
    "inn_t": "In the county inn guest room upstairs, on the dark-red wooden table top in cold grey window light",
    "wu": f"Inside the farmhouse of the Xu family at nightfall: {WU}; warm candlelight on the faces near it, the corners dark",
    "wu_c": "Inside the farmhouse of the Xu family at nightfall, warm candlelight in a dark mud-brick room",
    "wu_t": "Inside the farmhouse of the Xu family at nightfall, under the low wooden table in warm candlelight",
    "corr": f"In the inside corridor of the Xu farmhouse late at night: {CORR}",
    "room": f"In the first bedroom of the Xu farmhouse late at night: {ROOM}",
    "room_c": "In the first bedroom of the Xu farmhouse late at night, dim warm candlelight against rough plaster walls",
    "room_t": "In the first bedroom of the Xu farmhouse late at night, on the small wooden table top in warm candlelight",
    "yard": f"In the night yard of the Xu farmhouse, cold grey-blue and foggy: {YARD}",
    "ferry": f"At the ferry landing of Liuxi at midnight in thick fog: {PIER}; everything cold grey-blue",
    "boat": "Out on the water just off the ferry landing of Liuxi at midnight in thick fog: flat still dark water and grey fog all around, tall reeds dim far off on the right",
}
LIGHT = {
    "inn": "the cold grey window light stays unchanged",
    "inn_t": "the cold grey light on the wood stays unchanged",
    "wu": "the warm candlelight and the dark corners stay unchanged",
    "wu_t": "the warm candlelight from above stays unchanged",
    "corr": "the warm candle glow and the cold blue night stay unchanged",
    "room": "the low warm candlelight stays unchanged",
    "yard": "the cold grey-blue fog and the warm lantern light stay unchanged",
    "ferry": "the thick cold grey-blue fog and the one warm lantern glow stay unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow"
# from s27 on (script 角色表): the old grey outer coat at night
XU_N = "Xu Yan, in an old plain grey cloth outer coat worn open over his faded blue-grey scholar's robe"
QIN = ("Qin Shuang, in her dark brown cross-collared short jacket, wide plain leather belt with nothing tucked in it and nothing "
       "hanging from it, black trousers, leather boots and high ponytail tied with black cord")
# her pictures: a small knot on the crown, the rest long and straight down her back (e021 review 建議)
ALING = ("A-ling, in her plain grey-white cotton dress with long sleeves covering her wrists, her black hair pinned up on the crown "
         "with one plain wooden hairpin, the rest falling long and straight down her back")
XIAOHE = ("little Xiaohe, in her patched lilac cotton jacket, her two little pigtails tied with red string, one small woven straw "
          "rabbit tucked in her sash")
# bible rule 30 with the portrait's jade (e020 review 必改 7)
WEI = ("Wei Shaoqing, in his sapphire-blue brocade robe woven with gold thread, a white jade pendant at his waist, a small green "
       "jade ornament at the front of his topknot")
FAN = "one folding fan of plain cream paper with a few large flakes of gold leaf"
# Tang Xiaotang's face shot (s14): the jacket only, no skirt, no bow (e021 review 建議)
TANG = "in her peach-pink cross-collared short jacket wrapped shut across her chest"
POUCH = "one small peach-pink silk pouch with a drawstring"
GOLD = "five small gold ingots, each shaped like a little boat"
LAMP = "one small clay oil lamp with a short warm flame"
LANTERN = "one round plain white paper lantern glowing warm"
# bible rule 27: the letter of divorce
XIUSHU = "one sheet of plain paper folded in three"
# e920 fix1 s37b: the long flat abacus of the prop picture (the palm-sized wording drew a small upright one)
ABACUS = ("one long flat gold abacus as long as her forearm: a long narrow rectangular gold frame, a long row of thin gold rods set "
          "close side by side across its width, one thin gold crossbar running along its whole length, small round gold beads above "
          "and below the crossbar on every rod")
# bible rule 23
BOAT = "one small dark wooden boat with an arched canopy of woven bamboo over its middle"
BOATMAN = "one boatman in a conical bamboo hat and a straw rain cape, seen only from behind"
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
# No person named on screen: opens their motion so the clips-dh text holds "the set layout stays as it is. " once and the
# d1 prompt "never the mood. " once (refine-prep.py splices a retake's motion between those and "One continuous shot.").
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# e916 fix1 / e918 review 必改 1 / e919 review 建議: two high round buns, a short ribbon round each, the nape bare.
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with all of her black hair gathered "
         "up into two round buns set high on her head, a short pink silk ribbon wrapped around each bun, the "
         "nape of her neck bare above a pink inner collar, and her light peach-pink silk shoulders; the back of her "
         "head toward us the whole time, her ear the furthest round her head we ever see")
HEADSTILL = "the young woman with the two high round buns keeps her head still, the back of her head toward us the whole shot"
# a young woman's back walking away (s12, s20, s25): she never turns
WALKAWAY = "she walks away from us, the back of her head toward us all the way, never turning"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def only_tang(side):
    """e915 s26/s41: a second Tang appeared beside her back. One person with buns, one fixed side."""
    return (f"she is the only young woman with two high round buns in the frame, and she stays in the {side} "
            f"foreground from the first frame to the last")


def inn_back(rest):
    """Tang Xiaotang at the inn, seen from behind (rule 3): the camera behind her on the door side looks across the table."""
    return (f"over-the-shoulder medium shot from close behind {TBACK}, standing at the right side of {TABLE_INN} in the right "
            f"foreground, framed from the waist up, facing across the table; {only_tang('right')}; {rest}")


def dinner_back(rest):
    """Tang Xiaotang at dinner, seen from behind (rule 3), standing at the near right of the low table."""
    return (f"over-the-shoulder medium shot from close behind {TBACK}, standing at the near right corner of the low table in the "
            f"right foreground, framed from the waist up, facing across the table; {only_tang('right')}; {rest}")


SHOTS = [
    # ---- scene 1: day 22, near noon, the county inn guest room (set-kezhan-l1). She comes in alone (21->22).
    dict(chapter="客棧", loc="inn", cam="Medium shot, tracking shot that follows the subject", chars=["tangxiaotang", "weishaoqing"], nospeak=["tangxiaotang"], night="inn",
         comp=f"medium shot from just inside the closed double door, following close behind {TBACK}, a small peach-pink silk pouch with a drawstring hanging from her left hand at her side, walking into the room toward the right side of {TABLE_INN} from the first frame; {only_tang('right')}; beyond the table on screen left {WEI}, sitting on {BENCH}, framed from the knees up, {FAN} closed in his right hand on his knee, his face three-quarter to screen right toward her, never the lens; cool and watchful: eyes narrowed, lips closed; {HANDS}; exactly two people, the young woman seen only from behind",
         lines=[("tangxiaotang", "魏公子，我一個人來的，有一筆帳想跟你談。", "聲音發緊、慢，不笑")],
         motion=f"the young woman walks three steps to the right side of the table and stops there, standing straight; {HEADSTILL}; she looks across the table at the man on the bench the whole shot; {quiet('Wei Shaoqing')}; he turns his head slowly to follow her",
         zh="中景、跟拍（送客棧圖：窗在左、門在右，第 29 條照圖改站位）：從房門口跟在唐小棠背後（兩顆高丸子、短粉緞帶、後頸露出），她左手提著桃粉小布袋走到方桌右邊停住，頭不動、一直看著魏少卿；畫左魏少卿坐在窗下長凳上（稿子的雕花椅照圖寫成長凳），摺扇合著擱在膝上，轉頭看她、嘴閉著。台詞 nospeak，剪接放錄音（拍法 3）；推門、闔門交給音效"),
    # He may smile (rule 30).
    dict(loc="inn_c", cam="Close-up, slow push in", chars=["weishaoqing"], night="inn",
         comp=f"close-up of {WEI}, sitting on the bench under the window, framed from the chest up with space above his head, {FAN} closed in his right hand, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; mocking: one brow raised, one corner of his mouth curling up, lips moving lazily between words; behind him the window and the flat white overcast sky over grey roof tiles, soft",
         lines=[("weishaoqing", "一個人來？許秀才捨得放妳出門？", "笑")],
         motion="Wei Shaoqing points the closed fan once at the far end of the bench across the table, then leans back against the window frame as he speaks; after the last word he lets the fan rest on his knee, smiling",
         zh="近景、慢推（不送場景圖）：魏少卿用合起的摺扇往桌子對面的長凳一點，身子往後靠在窗框上，輕蔑地笑著說（本鏡可以笑）；臉朝畫右的唐小棠（畫外）"),
    dict(loc="inn", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "weishaoqing"], nospeak=["tangxiaotang"], night="inn",
         comp=inn_back(f"{POUCH} in her left hand held just above the table top from the first frame; facing us beyond the table a little left of the middle {WEI}, sitting on {BENCH}, framed from the waist up with clear space above his head, the closed fan in his right hand, his face three-quarter to screen right looking up at her, never the lens; amused: eyes narrowed, lips closed; behind him the window and the grey overcast sky, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("tangxiaotang", "他不知道。這是我跟你之間的事，跟許家無關。", "聲音發緊，下巴抬起")],
         motion=f"the young woman sets the pouch down on the table top and straightens up, lifting her chin; {HEADSTILL}; she looks straight ahead at Wei Shaoqing the whole shot; {quiet('Wei Shaoqing')}; one corner of his mouth lifts",
         zh="過肩中景、慢推（送客棧圖）：前景右唐小棠的背影（她不坐），把布袋擱上桌、站直、下巴抬起；桌對面魏少卿坐在窗下長凳、抬眼看她、嘴閉著，嘴角一挑。台詞 nospeak"),
    # Insert: the gold (the table-top crop set-kezhan-table-l1). The fan is in his hand, not on the table (s02, s06).
    dict(loc="inn_t", cam="Insert close-up, slow push in", chars=[], night="inn_t",
         comp=f"insert close-up, the shot opens directly on a small hand in a peach-pink silk sleeve cuff holding {POUCH} upside down with its mouth open, a hand's height above the dark-red wooden table top from its very first frame; only the hand, its sleeve cuff, the pouch, the gold and the table top are in the frame; the brown clay teapot soft at the back",
         motion=NOBODY + f"{GOLD} tumble out of the pouch onto the table one after another and roll to a stop on the wood, one of them spinning on its spot before it settles; the pouch hangs empty and limp",
         zh="插鏡、慢推（第一格就是布袋：桃粉袖口的手倒提著布袋、袋口朝下；送客棧桌面的免費裁切 `set-kezhan-table-l1`）：五錠小船形金錠滾到桌上，一錠轉一下才停（稿子『停在摺扇邊』不寫：扇子在魏少卿手上，s02、s06 接戲）"),
    dict(loc="inn", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "weishaoqing"], nospeak=["tangxiaotang"], night="inn",
         comp=inn_back(f"in the soft foreground on the table top {GOLD} lying in a loose row, her two hands already flat on the table on either side of them from the first frame; facing us beyond the table a little left of the middle {WEI}, sitting on {BENCH}, framed from the waist up with clear space above his head, the closed fan in his right hand, his face three-quarter to screen right toward her, never the lens; idle: eyes half closed, lips closed; behind him the window and the grey overcast sky, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("tangxiaotang", "五錠金子，是我全部的家當。我拿它買我自己。", "慢，一字一句，不笑")],
         motion=f"the young woman leans forward over the table and pushes the gold ingots a little toward the man with both hands; {HEADSTILL}; she looks straight ahead at Wei Shaoqing the whole shot; {quiet('Wei Shaoqing')}; his eyes drop to the gold",
         zh="過肩中景、慢推（前景桌上是五錠金子；送客棧圖）：前景右唐小棠的背影兩手撐在桌上、往前傾、把金錠往魏少卿那邊推一推；桌對面魏少卿半垂著眼、嘴閉著，眼睛落到金子上。台詞 nospeak（稿子 c03–c05 不笑）"),
    dict(loc="inn_c", cam="Low-angle close-up, slow push in", chars=["weishaoqing"], night="inn",
         comp=f"low-angle close-up from the height of the table top, {WEI}, sitting on the bench under the window, framed from the chest up with space above his head, {FAN} closed in his right hand, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; lightly scornful: a short laugh in his eyes, one corner of his mouth up, lips moving lightly between words; behind him the window and the flat white overcast sky, soft",
         lines=[("weishaoqing", "宰相府缺妳這五錠金子？我要的，是人。", "輕飄飄")],
         motion="Wei Shaoqing taps the closed fan twice on the palm of his left hand as he speaks; after the last word he holds the fan still against his palm and looks up at her",
         zh="低角度近景（桌面高度往上拍）、慢推（不送場景圖）：魏少卿看著金子輕笑，合起的摺扇在左手心敲兩下，輕飄飄地說（本鏡可以笑）；臉朝畫右的唐小棠（畫外）"),
    dict(loc="inn_t", cam="Insert close-up, slow push in", chars=[], night="inn_t",
         comp=f"insert close-up, the shot opens directly on a man's right hand in a wide sapphire-blue brocade sleeve woven with gold thread holding {FAN} closed, its closed tip already resting against {GOLD} lying together on the dark-red wooden table top from its very first frame; at the far edge of the table a small hand in a peach-pink silk sleeve cuff resting flat on the wood; only the two hands, their sleeve cuffs, the fan, the gold and the table top are in the frame",
         motion=NOBODY + "the closed fan pushes the gold ingots slowly across the table until they bump against the small hand; the small hand jerks back a little and stays there",
         zh="插鏡、慢推（第一格就是扇尖抵著金錠；送客棧桌面裁切）：魏少卿的右手（寶藍織金袖口）用合起的摺扇把五錠金子慢慢推回桌子另一頭，抵到唐小棠的手；她的手縮一下（稿子的白玉戒指不寫：定妝照沒有）"),
    dict(loc="inn_c", cam="Medium close-up, slow push in", chars=["weishaoqing"], night="inn",
         comp=f"medium close-up of {WEI}, leaning forward over the table with his left elbow on the table top, framed from the chest up with space above his head, {FAN} half open in his right hand at his chest, his face three-quarter to screen right toward Tang Xiaotang off screen right, close to her, never the lens; a smile with an edge: eyes cold and narrowed, one corner of his mouth curled, lips moving slowly between words; behind him the window and the grey overcast sky, soft",
         lines=[("weishaoqing", "妳不回魏家，許家的鋪子、紙坊，一樣都別想安寧。", "笑裡帶刀")],
         motion="Wei Shaoqing leans his face a little closer toward her across the table as he speaks; after the last word he holds still, close, smiling coldly",
         zh="中近景、慢推（不送場景圖）：魏少卿左手肘撐在桌上往前探身，右手半開的摺扇在胸前（不遮嘴），臉湊近畫右的唐小棠（畫外），笑裡帶刀地說（本鏡可以笑）"),
    dict(loc="inn_c", cam="Over-the-shoulder close shot, slow push in", chars=["tangxiaotang", "weishaoqing"], nospeak=["tangxiaotang"], night="inn",
         comp=f"close over-the-shoulder shot from close behind {TBACK}, standing at the right side of the table in the right foreground, framed from the shoulders up; {only_tang('right')}; her right hand at the lower right edge of the frame already gripping the neck of {POUCH} on the table top from the first frame; facing us beyond her shoulder, soft, {WEI}, sitting back on the bench under the window, framed from the chest up, his face three-quarter to screen right toward her, never the lens; waiting: eyes half closed, lips closed; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "你要怎樣才肯不碰許家？說個日子。", "咬牙")],
         motion=f"the young woman's fingers tighten hard on the neck of the pouch, the silk bunching in her fist; {HEADSTILL}; {quiet('Wei Shaoqing')}; he lets the question hang, unmoving",
         zh="過肩近景、慢推（不送場景圖）：前景右唐小棠的背影（肩以上），右手在畫面右下角捏緊布袋的口、絲布皺成一團（咬唇從背後看不到，寫在手上）；她身後虛焦的魏少卿靠在長凳上、嘴閉著、不動。台詞 nospeak"),
    dict(loc="inn", cam="Medium shot, slow push in", chars=["weishaoqing"], night="inn",
         comp=f"medium shot across the table, the brown clay teapot and two small clay cups in the soft foreground on {TABLE_INN}: {WEI}, sitting back on {BENCH} on screen left, framed from the knees up with clear space above his head, {FAN} closed in his right hand, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; lazily sure of himself: eyes half closed, a slow smile, lips moving slowly between words; behind him the window and the grey overcast sky over the roofs",
         lines=[("weishaoqing", "三日。三日內妳自己到縣城碼頭，上我回京的船。", "拖長音")],
         motion="Wei Shaoqing flicks the fan open with one turn of his wrist and fans himself slowly as he speaks; after the last word he keeps fanning, slowly",
         zh="中景、慢推（前景是桌上的陶茶壺與兩個杯子；送客棧圖）：魏少卿靠回窗下長凳，手腕一甩把摺扇搖開、慢慢搧，拖長音地說（本鏡可以笑）；臉朝畫右的唐小棠（畫外）"),
    dict(loc="inn_t", cam="Insert close-up, slow push in", chars=[], night="inn_t",
         comp=f"insert close-up, the shot opens directly on two small hands in peach-pink silk sleeve cuffs at the near edge of the dark-red wooden table top, the left hand holding {POUCH} open at the table edge, the right fingertips already on the first of {GOLD} lying together on the wood from its very first frame; only the two hands, their sleeve cuffs, the pouch, the gold and the table top are in the frame",
         lines=[("tangxiaotang", "好。我上了船，你就不准再找許家。", "畫外，很輕")],
         motion=NOBODY + "the right fingers slide the gold ingots one at a time over the edge of the table into the open pouch until the table is bare, then both hands pull the drawstring tight",
         zh="插鏡、慢推（第一格就是金錠與布袋；送客棧桌面裁切）：唐小棠的手把五錠金子一錠一錠撥回布袋、拉緊袋口繩；嘴不入鏡，台詞畫外"),
    dict(loc="inn", cam="Medium shot, slow push in", chars=["weishaoqing", "tangxiaotang"], nospeak=["tangxiaotang"], night="inn",
         comp=f"medium shot from beside the near corner of the table, the corner of {TABLE_INN} in the soft foreground: on screen left {WEI}, sitting on {BENCH}, framed from the knees up, {FAN} open in his right hand, his face three-quarter to screen right toward the door, never the lens; satisfied: eyes half closed, a thin smile; on the right, further back, {TBACK}, already walking toward the closed double door in the right wall from the first frame, the pouch in her left hand; {only_tang('right back')}; {HANDS}; exactly two people, the young woman seen only from behind",
         lines=[("weishaoqing", "一言為定。三日之內，我在碼頭等妳。", "搖扇，得意")],
         motion=f"the young woman pulls one leaf of the double door open and steps out through it, and the door swings shut behind her; {WALKAWAY}; Wei Shaoqing fans himself slowly at the shut door as he speaks",
         zh="中景、慢推（前景是桌角；送客棧圖）：畫左魏少卿坐在窗下長凳搖扇，對著關上的門得意地說（本鏡可以笑）；右後唐小棠的背影提著布袋拉開右牆的雙扇門出去，門闔上；她一路背對鏡頭、不回頭（拍法 3）。剪接剪在門闔上的一半"),
    # ---- scene 2: dusk, dinner at the Xu house (set-xujia-wu-ye-l1). Tang comes and goes beyond the RIGHT edge.
    dict(chapter="晚飯", loc="wu", cam="Over-the-shoulder medium-wide shot, slow push in", chars=["tangxiaotang", "qinshuang", "aling"], nospeak=["tangxiaotang"], night="wu",
         comp=dinner_back(f"one big clay plate heaped with dark braised pork already set down on the middle of the table in her two hands from the first frame; across the table, facing us, on screen left {QIN}, sitting on a low stool, framed from the waist up, her face three-quarter to screen right, never the lens; suspicious: one brow raised, lips closed; a little right of the middle {ALING}, sitting on a low stool, framed from the waist up, her face three-quarter to screen left, never the lens; quiet and wary: eyes lowered, lips closed; the red candle burning between them; {HANDS}; exactly three people, the young woman in the foreground seen only from behind"),
         lines=[("tangxiaotang", "城裡帶回來的滷肉，今天加菜，大家多吃點。", "甜甜地，硬撐出來的甜")],
         motion=f"the young woman lets go of the plate and picks up a pair of chopsticks from the table; {HEADSTILL}; {quiet('Qin Shuang', 'her')}; {quiet('A-ling', 'her')}; Qin Shuang and A-ling look at each other once across the table, then back at the plate",
         zh="過肩中全景、慢推（送夜裡的屋內圖 `set-xujia-wu-ye-l1`：一支紅燭在桌上，稿子的『一對紅燭、一盞油燈』照圖寫一支）：前景右唐小棠的背影把一大盤滷肉放到桌中間、拿起筷子；桌對面畫左秦霜挑眉、阿令垂眼（不戴面巾），兩人對看一眼。台詞 nospeak。拍法 1：小禾、許硯不入鏡（三張臉以內）"),
    # Her one face (silent; spec: l1 and angle-a, the short ribbons). She may smile (script c13-c25); Xiaohe may smile.
    dict(loc="wu", cam="Low-angle medium shot, slow push in", chars=["xiaohe", "tangxiaotang"], night="wu",
         comp=f"low-angle medium two-shot from a child's eye height at the table: on screen left {XIAOHE}, kneeling up on a low stool at the table, framed from the waist up, a clay bowl in front of her, both cheeks puffed full of food, her face three-quarter to screen right toward the young woman, never the lens; delighted: eyes shining wide, lips moving around her food; on screen right Tang Xiaotang, {TANG}, leaning in from the right over the table, framed from the waist up, a pair of chopsticks in her right hand, her face three-quarter to screen left toward the little girl, never the lens; a sweet smile, the rims of her eyes red, lips closed; the red candle soft between them; {HANDS}; exactly two people",
         lines=[("xiaohe", "棠姐姐，今天是過年嗎？這麼多肉！", "嘴裡塞滿，眼睛發亮")],
         motion=f"Tang Xiaotang drops a big piece of braised pork into the little girl's bowl with her chopsticks, then pinches her cheek once with her left hand; {quiet('Tang Xiaotang', 'her')}; she keeps smiling with reddened eyes",
         zh="低角度中景（小禾的高度）、慢推（送屋內夜圖）：畫左小禾跪在凳子上、腮幫子塞得鼓鼓的、眼睛發亮地說（可以笑）；畫右唐小棠（**本集唯一一張臉**，不說話：甜笑、眼眶紅；只送 l1 與 angle-a、短緞帶）夾一大塊滷肉進小禾碗裡、捏一下她的臉"),
    dict(loc="wu_c", cam="Over-the-shoulder close shot, slow push in", chars=["tangxiaotang", "xiaohe"], nospeak=["tangxiaotang"], night="wu",
         comp=f"close over-the-shoulder shot from close behind {TBACK}, leaning a little over the low table in the right foreground, framed from the shoulders up; {only_tang('right')}; facing us beyond her shoulder a little left of the middle {XIAOHE}, kneeling up on a low stool, framed from the chest up, her face three-quarter to screen right looking up at her, never the lens; happy: cheeks full, eyes bright, lips closed and chewing; behind her the dark mud-brick wall in candlelight, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "不是過年，是棠姐姐今天收帳，收得特別順。", "笑著，甜")],
         motion=f"the young woman shakes her head once, slowly, and pushes the little girl's clay bowl a little closer to her with one hand; {HEADSTILL} apart from that one shake; {quiet('Xiaohe', 'her')}; the little girl keeps chewing, beaming",
         zh="過肩近景、慢推（不送場景圖）：前景右唐小棠的背影搖一下頭、把小禾的碗往她面前推近一點；小禾跪在凳子上抬頭看她、嚼著、笑。台詞 nospeak"),
    dict(loc="wu_c", cam="Close-up, slow push in", chars=["qinshuang"], night="wu",
         comp=f"close-up of {QIN}, sitting at the table, framed from the chest up with space above her head, a clay bowl at the lower edge with a pair of chopsticks reaching in from the right edge of the frame laying a big heap of green vegetables into it, her face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; suspicious: one brow raised, eyes narrowed, lips moving flatly between words; behind her the dark mud-brick wall in candlelight, soft",
         lines=[("qinshuang", "妳一早說進城收帳，怎麼到天黑才回來？", "挑眉，懷疑")],
         motion="Qin Shuang looks down at the greens piled in her bowl, sets her own chopsticks down on the table and raises one brow at the young woman beyond the right edge of the frame as she speaks; after the last word she keeps the brow raised",
         zh="近景、慢推（不送場景圖）：一雙筷子從畫右伸進來往秦霜碗裡放一大把青菜；秦霜盯著碗、放下筷子、挑起一邊眉毛看畫右的唐小棠（畫外），懷疑地說，不笑"),
    dict(loc="wu", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="wu",
         comp=dinner_back(f"a pair of chopsticks in her right hand; facing us beyond the table a little left of the middle {XU}, sitting on a low stool, framed from the waist up with clear space above his head, holding up in both hands one clay bowl, his face three-quarter to screen right toward her, never the lens; surprised: brows up, lips closed; behind him the dark mud-brick wall in candlelight, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("tangxiaotang", "好幾家，一家一家對，就晚了。相公，你最辛苦，多吃塊肉。", "避開，轉向許硯，笑得甜")],
         motion=f"the young woman reaches across the table and piles pork and greens into his bowl one chopstickful after another until it is heaped high; {HEADSTILL}; {quiet('Xu Yan')}; his eyes go from the growing heap to her and back",
         zh="過肩中景、慢推（送屋內夜圖）：前景右唐小棠的背影隔桌一筷一筷把肉和菜堆進許硯碗裡（避開秦霜的眼睛，轉向許硯）；桌對面許硯兩手捧碗、眉毛揚起、嘴閉著。台詞 nospeak"),
    # Xu Yan may smile (puzzled).
    dict(loc="wu_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="wu",
         comp=f"medium close-up of {XU}, sitting at the table, framed from the chest up with space above his head, holding up in both hands one clay bowl heaped high with pork and greens, candlelight on his face, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; baffled and amused: brows up, a bewildered grin, lips moving between words; behind him the dark mud-brick wall, soft",
         lines=[("xuyan", "妳今天叫我相公，又夾這麼多，到底什麼日子？", "摸不著頭腦")],
         motion="Xu Yan lifts the heaped bowl a little higher to show it as he speaks, then lets out one puzzled laugh after the last word",
         zh="中近景、慢推（不送場景圖）：許硯捧著堆成小山的碗舉高一點，摸不著頭腦地笑著問（本鏡可以笑）；臉朝畫右的唐小棠（畫外）"),
    # Insert: the abacus (rule 20: the prop picture in the set slot; mkspec replaces the set clause).
    dict(loc="wu_t", cam="Insert close-up, slow push in", chars=[], night="wu_t",
         comp=f"insert close-up under the table, the shot opens directly on a small hand in a peach-pink silk sleeve cuff resting on a peach-pink pleated silk skirt over her lap, beside {ABACUS} lying flat across her lap from its very first frame; only the hand, its sleeve cuff, the gold abacus and the folds of the skirt are in the frame",
         lines=[("tangxiaotang", "平常的日子。快吃，菜要涼了。", "畫外，笑著")],
         motion=NOBODY + "the hand suddenly clamps tight around the long gold abacus, the knuckles going pale, and holds on, trembling a little; the abacus stays flat across her lap",
         zh="插鏡（桌下）、慢推（第一格就是手與算盤；送算盤道具圖 `prop-jinsuanpan-l1` 當唯一一張圖，拍法 20）：唐小棠擱在膝上的手猛地握緊橫在膝上的長金算盤、指節發白（稿子『腰間』照道具圖的長算盤改成橫在膝上；e920 fix1 長算盤的寫法）；臉不入鏡，台詞畫外"),
    dict(loc="wu_c", cam="Medium shot, tracking shot that follows the subject", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="wu",
         comp=f"medium shot following close behind {TBACK}, standing up from the table, holding in both hands one empty dark clay soup pot from the first frame; {only_tang('middle')}; ahead of her the dark mud-brick wall and a dark open doorway at the right, soft; {HANDS}; exactly one person, the young woman seen only from behind",
         lines=[("tangxiaotang", "湯也熱好了，我去灶房盛一鍋來。", "笑，輕快")],
         motion=f"the young woman walks away from us toward the dark doorway at the right carrying the empty pot and goes out through it; {WALKAWAY}",
         zh="中景、跟拍（不送場景圖：圖上沒有門）：唐小棠的背影端起空湯鍋，往右邊暗暗的門口（灶房）走出去，一路背對鏡頭。台詞 nospeak"),
    dict(loc="wu_c", cam="Close-up, slow push in", chars=["aling"], night="wu",
         comp=f"close-up of {ALING}, sitting at the table, framed from the chest up with space above her head, her face three-quarter to screen left toward Xu Yan off screen left, never the lens; grave and quiet: brows level, eyes steady, lips moving softly between words; behind her only the dark mud-brick wall and the candlelight, soft",
         lines=[("aling", "她今晚會走。下午我在渡口洗衣，看見她問船家時辰。", "很輕")],
         motion="A-ling sets her clay bowl down softly and leans a little toward the left as she speaks, her eyes flicking once to the doorway beyond the right edge of the frame and back; after the last word she holds still",
         zh="近景、慢推（不送場景圖）：阿令（不戴面巾，拍法 21）把碗輕輕放下、往畫左的許硯（畫外）傾一點身，眼睛往畫右的灶房門口一瞟再回來，很輕地說，不笑"),
    dict(loc="wu_c", cam="Close-up, slow push in", chars=["xuyan"], night="wu",
         comp=f"close-up of {XU}, sitting at the table, framed from the chest up with space above his head, a pair of chopsticks held up in his right hand, his face three-quarter to screen right toward A-ling off screen right, never the lens; the smile gone: brows drawn together, eyes darkening, lips moving low between words; behind him only the dark mud-brick wall and the candlelight, soft",
         lines=[("xuyan", "她要走？她今天在城裡，到底見了誰？", "低，不笑")],
         motion="Xu Yan's chopsticks stop in mid-air and he lowers them slowly to the table as he speaks, his eyes moving from her to the doorway beyond the right edge of the frame; after the last word he keeps looking at the doorway",
         zh="近景、慢推（不送場景圖）：許硯筷子停在半空、慢慢放下，眼睛從阿令移向畫右的灶房門口，低聲問；笑容收掉"),
    dict(loc="wu_c", cam="Over-the-shoulder medium close-up, slow push in", chars=["aling"], night="wu",
         comp=f"over-the-shoulder medium close-up, the blurred dark shoulder of one young man seen only from behind in the soft left foreground, appearing only once; facing us a little right of the middle {ALING}, sitting at the table, framed from the chest up with space above her head, her face three-quarter to screen left toward him, never the lens; calm and certain: eyes level, lips moving evenly between words; behind her the dark mud-brick wall in candlelight, soft; {HANDS}; exactly two people, the man in the foreground seen only from behind",
         lines=[("aling", "見了誰，她沒說。開船的時辰，是子時那一班。", "平靜")],
         motion="A-ling shakes her head once, then taps two fingertips twice on the table top as she speaks; the man in the foreground keeps his head still, the back of his head toward us the whole shot",
         zh="過肩中近景、慢推（不送場景圖）：前景左虛焦的男子肩膀（不點名、不送圖，拍法 2）；阿令搖一下頭、手指在桌上點兩下，平靜地說"),
    dict(loc="wu", cam="Medium shot, slow push in", chars=["qinshuang"], night="wu",
         comp=f"medium shot, the red candle burning in the soft foreground on the low table: {QIN}, sitting on a low stool at the near left end of the table, framed from the waist up with clear space above her head, her face three-quarter to screen right toward the doorway beyond the right edge of the frame, never the lens; cold and angry: eyes narrowed, jaw tight, lips moving hard between words; behind her the dark mud-brick wall and the small dark window; {HANDS}; exactly one person",
         lines=[("qinshuang", "還能有誰？昨晚那個搖扇子的，說的就是三日。", "冷")],
         motion="Qin Shuang drops her chopsticks onto the table, folds her arms across her chest and glares toward the doorway beyond the right edge of the frame as she speaks; after the last word she keeps glaring",
         zh="中景、慢推（前景是桌上的紅燭；送屋內夜圖）：秦霜把筷子往桌上一擱、雙手抱胸、往畫右的灶房門口瞪一眼，冷冷地說，不笑"),
    dict(loc="wu", cam="Medium-wide shot, slow push in", chars=["tangxiaotang", "xuyan", "qinshuang", "aling"], nospeak=["tangxiaotang"], night="wu",
         comp=f"medium-wide shot from behind {TBACK}, in the middle foreground, standing just past the near side of the low table, a steaming dark clay soup pot already set down on the table beside her from the first frame; {only_tang('middle')}; at the table beyond her, all three seated on low stools and framed from the waist up: on screen left {XU}, his face turned toward her, never the lens; beside him {QIN}, her face turned toward her, never the lens; on screen right {ALING}, her face turned toward her, never the lens; all three watching her, unsmiling, lips closed; a dark open passage in the back left corner; {HANDS}; exactly four people, the young woman seen only from behind",
         lines=[("tangxiaotang", "湯來了。我今天走累了，先回房歇著。", "笑得勉強，尾音往下掉")],
         motion=f"the young woman unties a cloth strip from her sleeve and walks away from us past the table toward the dark passage in the back left corner; {WALKAWAY}; {quiet('Xu Yan')}; {quiet('Qin Shuang', 'her')}; {quiet('A-ling', 'her')}; their eyes follow her",
         zh="中全景、慢推（送屋內夜圖）：湯鍋第一格已經放在桌上；唐小棠的背影解下袖口的布條、往左後暗暗的走廊口走去，一路背對鏡頭；桌邊許硯、秦霜、阿令三張臉（拍法 1）嘴閉著、目光跟著她。台詞 nospeak；小禾不入鏡"),
    dict(loc="wu_c", cam="Close-up, slow push in", chars=["xuyan"], night="wu",
         comp=f"close-up of {XU}, sitting at the table, framed from the chest up with space above his head, his face three-quarter to screen left toward the dark passage beyond the left edge of the frame, never the lens; quietly resolved: brows drawn, eyes steady and dark, lips pressed shut; at the lower right edge a small child's hand in a patched lilac sleeve lifting from the table, and his right hand coming down over it; behind him only the dark mud-brick wall and the candlelight, soft",
         lines=[("xuyan", "子時才開船……等小禾睡了，我就去敲她的門。", "心裡話，低", "inner")],
         motion=f"Xu Yan's eyes follow the passage beyond the left edge of the frame while his right hand settles gently over the small hand on the table and keeps it there; {SILENT_HE}",
         zh="近景、慢推（不送場景圖）：許硯看著她走進畫左外的走廊，右手按住右下角正要抬起的小手（淡紫補丁袖口；不點名小禾、不送圖）；全程嘴閉著，心裡話畫外"),
    # ---- scene 3: late at night, the corridor and her room. Xu Yan in the old grey outer coat from here (script 角色表).
    dict(chapter="休書", loc="corr", cam="Medium shot, tracking shot that follows the subject", chars=["xuyan"], night="corr",
         comp=f"medium shot down the corridor, a dark wooden post in the soft left foreground: {XU_N}, framed from the knees up with clear space above his head, holding {LAMP} in his left hand, already standing before a closed plain wooden door in the right wall from the first frame, his face in profile to screen right toward the door, never the lens; gentle and uneasy: brows a little drawn, lips moving softly between words; {HANDS}; exactly one person",
         lines=[("xuyan", "小棠，睡了嗎？我有話跟妳說，就幾句。", "放輕聲音")],
         motion="Xu Yan knocks twice on the door with the knuckles of his right hand as he speaks, and the unlatched door swings in a finger's width at the touch; after the last word he frowns at the gap",
         zh="中景、跟拍（前景左虛焦走廊木柱；送走廊夜圖 `set-xujia-zoulang-l1`，門在右牆）：許硯外披舊灰外衣、左手提一盞小陶油燈，第一格已經站在右牆一扇關著的木門前，指節敲兩下、輕聲說；門沒閂、一碰就開了一條縫，他皺眉"),
    dict(loc="room", cam="Point-of-view shot, slow push in", chars=[], night="room",
         comp=f"point-of-view shot from the open doorway of the small bedroom, a man's left hand in a grey cloth sleeve holding {LAMP} coming in at the lower left edge of the frame from its very first frame: the bedroom empty of people, the bed with its smooth flat pink cover, the glowing paper window above it, and on the small table in the right foreground {PACKS}, {XIUSHU} lying on the nearer stack, {CANDLE_LOW} beside them",
         motion=NOBODY + "the lamp in the hand sways a little and its light slides across the plaster walls; the candle flame on the table leans in the draught from the door",
         zh="主觀（許硯從門口看進房間）、慢推（送唐小棠的房間圖 `set-xujia-tangfang-l1`：門在左、床在後牆、窗在床上方、小桌在右前，第 29 條照圖）：房裡沒人，床上粉被平平整整，窗是關著的（圖上是關的，稿子的開窗不寫）；小桌上兩疊素布小包（稿子的十本帳冊照圖寫，不寫帳冊）、最上面一張摺三摺的紙、一支快燒完的蠟燭（聖經：她走前點著）；畫左下許硯提燈的手伸進來"),
    dict(loc="room_t", cam="Insert close-up, slow push in", chars=[], night="room",
         comp=f"insert close-up, the shot opens directly on a man's right hand in a faded blue-grey sleeve cuff setting {LAMP} down on the small wooden table top from its very first frame, beside {PACKS}, {XIUSHU} lying on the nearer stack, {CANDLE_LOW} at the right; only the hand, its sleeve cuff, the lamp, the stacks, the folded paper, the candle and the table top are in the frame",
         motion=NOBODY + "the hand lets go of the lamp, moves to the folded paper and lifts it off the stack; the paper stays folded in three, its plain outside up",
         zh="插鏡、慢推（第一格就是小桌：手正把油燈放下；送房間桌面的免費裁切 `set-xujia-tangfang-table-l1`）：他放下油燈、拿起那張摺三摺的紙，紙一直摺著（打開不拍，拍法 7）"),
    dict(loc="room_c", cam="Close-up, slow push in", chars=["xuyan"], night="room",
         comp=f"close-up of {XU_N}, standing by the small table, framed from the chest up with space above his head, holding open in both hands at the lower edge of the frame {XIUSHU} now unfolded, its plain blank back toward us, opaque, the warm candlelight on his face from below, his face lowered toward the paper, never the lens; reading and stricken: brows drawing tighter and tighter, eyes moving down line by line, lips pressed shut; behind him the dark plaster wall, soft",
         lines=[("tangxiaotang", "今立休書：唐小棠自請離去，十本帳目，一筆一筆兩清。", "畫外，忍著哭")],
         motion=f"Xu Yan's eyes move slowly down the paper line by line and his brows knot tighter with every line; the paper stays still in his hands, its plain back toward us; {SILENT_HE}",
         zh="近景、慢推（不送場景圖）：許硯兩手拿著打開的紙（紙背朝鏡頭、空白不透光，拍法 7、17），燭光從下往上照臉，眼睛一行一行往下看、眉頭越皺越緊；全程嘴閉著，唐小棠念休書畫外"),
    dict(loc="room_t", cam="Insert close-up, slow push in", chars=[], night="room",
         comp="insert close-up, the shot opens directly on a man's thumb and fingers holding one corner of one sheet of plain paper just above the small wooden table top from its very first frame, the corner of the paper blank and plain, one small red thumbprint smudge on it and beside it one dried round water stain; only the fingers, the paper corner and the table top are in the frame",
         lines=[("tangxiaotang", "從此互不相欠。相公，你別來找我。", "畫外，聲音一抖")],
         motion=NOBODY + "the thumb moves slowly across the dried round water stain, and the paper trembles a little in the fingers",
         zh="插鏡、慢推（第一格就是紙的一角；送房間桌面裁切）：許硯的手指捏著紙角（空白，只有一團小紅指印與一圈乾掉的淚痕；筆畫不拍，拍法 7、27），拇指慢慢撫過淚痕，紙在指間發抖；台詞畫外"),
    dict(loc="room_c", cam="Medium shot, slow push in", chars=["qinshuang", "aling"], night="room",
         comp=f"medium shot at the open door in the left wall, the dark edge of the door frame in the soft left foreground: {QIN}, leaning one shoulder against the door frame, framed from the waist up with clear space above her head, her face three-quarter to screen right toward Xu Yan off screen right, never the lens; incredulous: eyes wide, brows up, lips moving sharply between words; just behind her shoulder {ALING}, framed from the chest up, her face three-quarter to screen right, never the lens; subdued: eyes lowered, lips closed; warm candlelight on both faces; {HANDS}; exactly two people",
         lines=[("qinshuang", "她寫休書？她是妻子，休的是誰啊？", "瞪眼")],
         motion=f"Qin Shuang glances at the paper in his hands beyond the right edge of the frame, folds her arms and huffs once in disbelief as she speaks; {quiet('A-ling', 'her')}; A-ling lowers her eyes",
         zh="中景、慢推（前景左是門框；不送場景圖）：門在左牆（照房間圖），秦霜靠在門框上、往畫右許硯手上的紙看一眼、抱起手臂、不敢相信地說；她肩後阿令（不戴面巾）垂下眼、嘴閉著；兩人不笑（原版必修）"),
    # He may laugh once (the script: 笑出一聲, eyes wet).
    dict(loc="room_c", cam="Close-up, slow push in", chars=["xuyan"], night="room",
         comp=f"close-up of {XU_N}, standing by the small table, framed from the chest up with space above his head, {XIUSHU} unfolded in his right hand at the lower edge of the frame, its plain blank back toward us, his face three-quarter to screen left toward Qin Shuang off screen left, never the lens; hurt and stubborn: the rims of his eyes red and wet, a short bitter laugh, lips moving between words",
         lines=[("xuyan", "妻子寫休書，律上不算，這張紙作不了數。", "眼眶紅，笑出一聲")],
         motion="Xu Yan lets out one short laugh through his nose and shakes his head once as he speaks, his eyes glistening; after the last word he looks down at the paper",
         zh="近景、慢推（不送場景圖）：許硯拿著休書（紙背朝鏡頭），眼眶紅，從鼻子裡笑出一聲、搖搖頭、眼睛濕了，朝畫左門口的秦霜（畫外）說（本鏡可以笑一聲）"),
    dict(loc="room", cam="Wide shot, slow push in", chars=["xuyan"], night="room",
         comp=f"wide shot from just inside the door, two young women seen only from behind blurred in the soft left foreground, appearing only once each: {XU_N}, standing by the small table on the right, framed from the knees up with clear space above his head, {XIUSHU} unfolded in both hands at his chest, its plain blank back toward us, {PACKS} and {CANDLE_LOW} on the table beside him, his face lowered to the paper, never the lens; grim: jaw set, lips pressed shut; {HANDS}; exactly three people, the two women in the foreground seen only from behind",
         motion=f"Xu Yan tears the paper in two with both hands, puts the halves together and tears them again, and lets the pieces drop onto the stacks on the table, one piece sliding off the edge to the floor; {SILENT_HE}; the two women in the foreground keep still",
         zh="全景、慢推（前景左是門口虛焦的兩個背影：秦霜、阿令，不點名、不送圖；送房間圖）：許硯在右邊小桌旁兩手把休書撕成兩半、再撕一次，碎紙落在桌上的素布小包上、一片滑下桌緣；沒有人說話"),
    # Long shot: the system and his thought. Rule 11: no blue light written; the panel is the cut's.
    dict(loc="room_c", cam="Close-up, slow push in", chars=["xuyan"], night="room",
         comp=f"close-up of {XU_N}, standing by the small table, framed from the shoulders up with a little space above his head, his face three-quarter to screen left, his eyes on a point in the air in front of him, never the lens; jolted, then set: brows drawn hard, eyes wide, jaw clenched; behind him only the dark plaster wall and the low candlelight, soft",
         lines=[("xitong", "叮。警告，唐小棠正在遠離。", "冷，宣布"),
                ("xitong", "休書撕了，人也不會自己走回來，宿主。", "冷"),
                ("xuyan", "不用妳說，我這就去把她追回來。", "心裡話，咬牙", "inner")],
         panel=[("警告，唐小棠正在遠離", "penalty")],
         motion=f"Xu Yan's head snaps up and his breath catches; he stays frozen a moment, then his jaw tightens and his eyes harden and settle, fixed ahead; {SILENT_HE}; he is listening and thinking, not speaking",
         zh="近景、慢推（長鏡；不送場景圖；拍法 11 不寫藍光，面板由剪接疊上）：許硯猛地抬頭、一口氣卡住，停一下，下巴一繃、眼神定下來；全程嘴閉著（系統兩句與心裡話都畫外）。稿子『抓起油燈又放下』不拍（一鏡一個動作；燈一直在小桌上）"),
    dict(loc="room_c", cam="Close-up, slow push in", chars=["aling"], night="room",
         comp=f"close-up of {ALING}, standing in the open door, framed from the chest up with space above her head, the blurred dark brown shoulder of one young woman seen only from behind at the left edge of the frame, appearing only once, her face three-quarter to screen right toward Xu Yan off screen right, never the lens; urgent but calm: eyes lifted and steady, lips moving softly between words; behind her the dark doorway, soft",
         lines=[("aling", "快去。船家說子時開船，現在已經亥時末了。", "很輕")],
         motion="A-ling lifts her eyes to him and tips her head once toward the dark doorway behind her as she speaks; after the last word she holds his gaze",
         zh="近景、慢推（不送場景圖）：阿令在門口抬眼看許硯（畫右外），頭往身後黑黑的門外一偏，很輕地說，不笑；畫左緣虛焦是秦霜的肩（不點名、不送圖）"),
    dict(loc="room", cam="Medium shot, tracking shot that follows the subject", chars=["qinshuang", "xuyan"], night="room",
         comp=f"medium two-shot in the small bedroom: on screen right {XU_N}, standing by the small table, framed from the waist up with clear space above his head, his face three-quarter to screen left toward her, never the lens; stunned: eyes wide, lips closed; on screen left {QIN}, already striding in from the door in the left wall from the first frame, framed from the waist up, her face three-quarter to screen right toward him, never the lens; fierce: brows down, eyes blazing, lips moving hard between words; {HANDS}; exactly two people",
         lines=[("qinshuang", "還愣著幹嘛？追啊！燈籠就在屋簷下！", "推他一把，吼")],
         motion=f"Qin Shuang shoves Xu Yan hard on the shoulder with her right hand, turning him toward the door at screen left, and jerks her chin at the doorway as she speaks; {quiet('Xu Yan')}; he stumbles one step toward the door",
         zh="中景、跟拍（送房間圖）：畫左秦霜第一格已經從左牆的門大步走進來，右手一把推在許硯肩上、把他往畫左的門口送、下巴往門外一抬，吼著說；畫右許硯愣住、被推得往門口踉蹌一步、嘴閉著。剪接剪在推肩的一半"),
    dict(loc="yard", cam="Wide shot, tracking shot that follows the subject", chars=["xuyan"], night="yard",
         comp=f"wide shot of the yard in thin grey fog: {XU_N}, framed full length, already running across the middle of the yard from the house door toward the yard gate from the first frame, {LANTERN} on its bamboo handle in his right hand, swinging, his face in profile to screen right, never the lens; desperate: brows drawn, mouth set; small in the dark house doorway at the left one young woman with a high ponytail in a dark brown jacket, seen dimly, appearing only once; {HANDS}; exactly two people",
         motion=f"Xu Yan runs through the open yard gate and out into the fog beyond it, the lantern light swinging on the gateposts; {SILENT_HE}; the young woman in the doorway stays where she is",
         zh="全景、跟拍（送夜院圖 `set-xujia-yuan-ye-l2`：屋門在左、院門在中間後牆、門上小瓦簷下掛一盞白紙燈籠，秦霜說的『屋簷下』就是這個簷）：許硯第一格已經提著點著的圓紙燈籠（空白、竹柄）跑過院子，衝出院門、進了霧裡；扯燈籠那一下交給 s37→s38 的剪接與音效。屋門口的秦霜很小、不點名、不送圖；沒有人說話"),
    # ---- the ferry landing at midnight (set-dukou-ye-l1; the boat written in the shot, rule 23)
    dict(chapter="渡口", loc="ferry", cam="Wide shot, tracking shot that follows the subject", chars=["xuyan"], nospeak=["xuyan"], night="ferry",
         comp=f"wide side-on shot along the pier, a weathered wooden post in the soft foreground: {XU_N}, framed full length, already running along the old planks of the pier toward its far end from the first frame, {LANTERN} on its bamboo handle in his right hand, his face in profile to screen right, never the lens; frantic: brows up, eyes straining ahead; far off on the right in the fog the dim dark shape of {BOAT}; {HANDS}; exactly one person",
         lines=[("xuyan", "小棠——！", "短喊，邊跑邊喊")],
         motion="Xu Yan runs flat out along the pier toward the right, the lantern swinging and its light jumping over the planks, and halfway he opens his mouth wide and shouts one long call toward the fog, then runs on with his lips parted, panting",
         zh="全景、跟拍（側面跟著跑；前景是棧橋的木樁；送渡口夜霧圖 `set-dukou-ye-l1`，圖上沒有船，船寫在鏡頭裡）：許硯右手提燈籠沿著舊木板往畫右狂奔，燈光在木板上跳，跑到一半張嘴喊一聲（nospeak：不給整鏡說話句，喊聲寫在動作裡）；畫右霧裡是小船的黑影"),
    # Her back on the boat; her thought (lips unseen). No picture, no name: the boat picture alone.
    dict(loc="boat", cam="Medium shot, slow push in", chars=[], night="ferry",
         comp=f"medium shot from the water's edge, the dark wet side of the boat and the drifting fog in the soft foreground: {BOAT}, just pushed off, its prow pointing away to the right into the fog, one round paper lantern glowing on a bamboo pole at the far end; at that far end {BOATMAN}, standing, both hands on one long bamboo pole; under the arched canopy, sitting low with her arms wrapped around her drawn-up knees, one young woman in a light peach-pink silk jacket with her black hair in two round buns set high on her head, a short pink silk ribbon wrapped around each bun, seen only from behind, her back to us; exactly two people, both seen only from behind",
         lines=[("tangxiaotang", "別回頭，唐小棠。回頭，就走不了了。", "心裡話，嘴閉著", "inner")],
         motion=NOBODY + "the boatman leans his weight on the pole and the boat glides slowly away from us into the fog; the young woman under the canopy lowers her head onto her knees and her shoulders shake once; she keeps her back to us the whole shot",
         zh="中景、慢推（前景是船舷與霧；送夜霧小船圖 `set-chuan-ye-l1`：拱形竹篷、船頭竹竿上一盞燈）：船夫（斗笠蓑衣，背影，不點名、不送圖）一撐篙，船滑進霧裡；竹篷下唐小棠抱著膝、背對鏡頭，把頭埋進膝蓋、肩膀抖一下（不送她的圖、不寫名字：背影只靠兩顆高丸子與桃粉衣；心裡話畫外）"),
    dict(loc="ferry", cam="Wide shot, slow push in", chars=[], night="ferry",
         comp=f"wide shot from behind on the pier, the old planks in the soft foreground: one young man in an old grey cloth outer coat seen only from behind, standing at the very end of the pier a little left of the middle, framed full length, holding {LANTERN} high above his head in his right hand; beyond him on the right {BOAT}, already ten metres out on the flat water, sliding into the thick fog, one small peach-pink figure sitting hunched under its canopy with her back to the pier; exactly three people, all seen only from behind",
         lines=[("xuyan", "休書我撕了！妳寫的不算，聽見沒有！", "背對鏡頭，喊，聲音發抖")],
         motion=NOBODY + "the young man holds the lantern higher, his shoulders heaving as he shouts toward the boat, the back of his head toward us the whole shot; the boat keeps sliding away into the fog, and the small figure on it never turns round",
         zh="全景、慢推（從棧橋後方拍，前景是棧橋木板；送渡口夜霧圖）：許硯的背影（不送圖，背影鏡不送臉）站在棧橋盡頭、燈籠高舉、胸口起伏，背對鏡頭喊；右邊小船在十來公尺外滑進白霧，船上那個桃粉色的小小背影抱著膝，沒有回頭（結尾；懸念交給第 23 集涉水）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e022-r2/script.md`（c01–c41 對應 s01–s41；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-16）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e021-e030.md`（拍法 1–30 條）。第 3 篇章〈搶親〉第二集。",
    "- 內部工作編號 922（`hailuo/{ff,clips}-dh-e922.json`、`colab/runs/e922/extras.json`、`colab/runs/e922-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e922-dh/`）；發布 slug `zhong-tian-qu-qi-e022-r2`。不放集數、不放片名卡；s01 接第 21 集隔天近午（聖經接點 21→22：唐小棠一個人推門進客棧，魏少卿坐在窗邊）；s41 交給第 23 集第一場（同一刻：許硯把燈籠插在岸邊泥裡涉水追船）。",
    "- 照第 21 集審稿後的寫法一開始就照做：`OFFSCREEN_SPEECH = False`；`quiet()` 只管嘴；背景寫在場的東西（拍法 18）；道具與接觸寫在第一格；只寫要畫出來的東西（e920 fix1：寫 books 就畫出書）：稿子的十本帳冊照房間圖寫成兩疊素布小包，休書照拍法 27 寫成「一張摺三摺的白紙」，只拍摺著或空白的紙背（拍法 7）。",
    "- **唐小棠不露嘴說話**（拍法 3）：她在畫面上的台詞全部從背後拍（s01、s03、s05、s09、s12 客棧；s13、s15、s17、s20、s25 晚飯；nospeak，spec 拿掉她的圖與身分句；兩顆高丸子、短粉緞帶、後頸露出、頭不動）；她唯一的臉是 **s14**（不說話：甜笑、眼眶紅，小禾說話；只送 l1 與 angle-a、短緞帶）。s40 船上只拍背影、不送圖。**小金算盤只在 s19 插鏡**（拍法 20：送道具圖、照 e920 fix1 寫長金算盤，橫在膝上）。",
    "- **一鏡最多三張臉**（拍法 1）：s13 秦霜、阿令加唐小棠背影（小禾、許硯不入鏡）；s25 許硯、秦霜、阿令加唐小棠背影（小禾不入鏡）。前景不點名、不送圖（拍法 2）：s23 許硯的肩、s34 門口兩個背影、s36 秦霜的肩、s38 屋門口小小的秦霜、s41 許硯的背影。秦霜腰帶空著（柴刀不寫，拍法 5）；阿令不戴面巾（拍法 21）；小禾兔子塞在腰帶。",
    "- **場景圖說了算**（拍法 29，協調者 2026-11-16 決定，每張放大看過）：客棧 `set-kezhan-l1`（窗與長凳在左、方桌在中、雙扇門在右牆；魏少卿坐窗下長凳）；晚飯 `set-xujia-wu-ye-l1`（土磚屋、桌上一支紅燭；灶房門在畫右外、往房間的走廊在畫左外）；走廊 `set-xujia-zoulang-l1`；唐小棠的房間 `set-xujia-tangfang-l1`（**門在左、小桌在右前、窗關著**，稿子的房門在右、開窗照圖改：許硯在右邊小桌旁，秦霜、阿令在左邊門口）；夜院 `set-xujia-yuan-ye-l2`（院門上的小瓦簷掛燈籠）；渡口 `set-dukou-ye-l1`（棧橋從左來、圖上沒有船）；小船 `set-chuan-ye-l1`。插鏡：客棧桌面 `set-kezhan-table-l1`、房間桌面 `set-xujia-tangfang-table-l1`（兩張都是免費裁切、新 id 自帶 l1）、算盤 `prop-jinsuanpan-l1`。近鏡不送場景圖。**不需要試鏡**。",
    "- 長鏡要買的秒數（BUY）：照 38 句錄音核過（`~/mokaair-work/videos/zhong-tian-qu-qi-e922-dh/audio`，faster-whisper 一次一支逐句聽寫；見 `r2.py` 的 BUY 註解）。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音長度＋0.5 秒為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯、唐小棠（l1 交領；只在 s14，l1 與 angle-a）、魏少卿、秦霜、阿令（l1，不戴面巾）、小禾的 l1 與 `ref2manifest` 給的角度圖；許硯帶笑的 angle-b 整集不送；唐小棠長緞帶的 angle-b 不送。場景見上面。",
    "- 共用檔：程式都沒改（說話的人都在 `build-r2.py` 的 `EN`；地方都用 `gen-dh.mjs` 已有的 SET 句；`pilot.py`、`cast.json` 不動；船夫不說話、沒有 `MINOR`）；`refs-live` 加兩張免費裁切（新 id）與 README 一段。",
    "- `colab/runs/e922/extras.json`（照第 21 集：畫面不放字幕那句；拿掉秦霜的柴刀；魏少卿外貌拿掉常帶冷笑與手上的扇子、玉冠改髮髻前一塊綠玉；小禾兔子塞在腰帶）與 `colab/runs/e922-live/spec.json`（`mkspec.py` 產生；種子 9221101／9221102）。",
    "- 免費準備：scratchpad `prep922.sh`（`DRY=1 … st1-ep.sh 922` → `pilot.py` → `retake.py` → `colab-jobs.json` 加 output_path、套 swap_pictures（絕對路徑）→ 逐鏡查送的場景圖與人物圖 → 精修用的分隔句 → `preflight-prompts.py` → 否定名詞與會長字的名詞掃描）。",
    "- 配樂：客棧冷的稀疏弦樂，s07 金子推回、s10「三日」各一個重音；晚飯暖的家常 cue，s21 阿令開口時抽掉只剩低音，s26 一個輕重音；房間風聲與鋼片琴，s33「律上不算」重音、s35 電子音，s37 起鼓點；渡口一把二胡長音，s41 喊完一個重音後收。音效見 script.md〈音樂與音效〉（s01 推門、闔門；s19 算盤珠被握住；s38 扯燈籠的鉤子聲交給剪接）。",
]

# Long shots: seconds to buy (filled in after the recordings; see the BUY comment below).
BUY = {}
