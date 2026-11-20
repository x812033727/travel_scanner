"""Episode 35 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e035-r2/script.md
(c01-c35; the CG-era r2 script), including its sections 「這版改了什麼」 and 「2026-11-06 審稿後的修改」, which override the tables.
Every line is the script's, word for word; only the staging changes. 40 shots: one per script shot (sNN = cNN) plus five
splits that keep one visible action per shot (s02b, s11b, s12b, s17b, s20b; build-r2.py's `sid`, as e031's s21b / s29b).
Bible: production/r2-bible-e031-e040.md (arc 4 〈旱年〉: rules 1-43, 〈場景〉, 〈接點〉 34->35 and 35->36, the props (the ducks and
cages, A-ling's pole and whistle, the gate and its crossbar, the wooden abacus), people, 〈小角色〉 (the refugees, the refugee
woman: Erinome, from behind only) and 原版必修 (e035: the fields round the three mu stay dry, no orchard in blossom)) and
r2-bible-e011-e060.md (accounts: Tang Xiaotang +3 -> 45; the main line 天下歸心 百分之一 -> 百分之二; ducks 3000 x 30 wen = 90
liang, 45 paid, 45 on credit). The fifth episode of arc 4: the swarm night of the tenth day (the Xu room), two days later in
the afternoon, that evening and the next dawn (the three fields), five days after the swarm night at dusk (the village gate).

Written from the start the way e034-r2/r2.py stands AFTER its independent review (writer-tools/e034-r2/review-independent.md,
必改 1-4, 建議 1-12) and the general lessons of the e033 and e034 reviews:
- The pictures agree with the words (e033 必改 1, 2; e034 必改 2, 3): every place sentence follows the picture it sends, every
  crop is a new free id made for this episode (live-action/free-e031-e040/{xujia_wu_ye_crops.sh,hantian_yang.sh,cunkou_crops.sh}).
- The clean sentence's "the air is clear and still" fights a shot that needs something in the air (e034 必改 1): mkspec.py
  replaces it per shot (s14: the wind tossing her ribbon and the swarm over the hills; s20-s25: the dawn mist on the water;
  s26: the evening breeze in the willow).
- Long things are never touching in the first frame (e032 fix2): A-ling's long pole and the man's hands (s16), the pole and the
  whistle cord (s17, s25).
- No collective noun (e033 必改 8, rule 34): the ducks are "white farm ducks" near and "a long unbroken white line" far, never a
  number; the refugees are twelve people one by one; "exactly N people"; no "crowd", "hundreds", "villagers".
- A shot with nobody's feet has no shoes sentence (e033 必改 6); the refugees wear straw sandals (mkspec.py).
- No mud (e032 fix3; e034's decision): the script's 「坐在泥裡、袍子沾泥」 (c13, c15) is the grassy bank and a loosened topknot.
- OFFSCREEN_SPEECH = False (rule 15); rule 31: a line to someone out of frame is written "toward someone out of sight beyond the
  left/right edge of the frame", that side set only, the speaker the only person; GAZE_REFINE puts the same direction into the
  refine text. A look at a thing names the thing (the window, the ducks, the pole, the gate, the far paddy).
- No blue light (rule 11): the panels of s01, s11, s27, s30 are the editor's.
- No word "open" (rule 36): the cage lids "are lifted"; the gate is never opened in this episode (e036 c01 lifts the bar).
- Tang Xiaotang (rules 3, 4, 40): every line of hers is said from behind (the middle of the frame, head still, exactly two buns,
  her l1 cross-collared jacket, no outer coat, no stand-up collar: e031/e033's alone() and TBACK) or over another picture (s07
  the abacus insert, s17b the ducks); her pictures and identity sentence leave there (mkspec.py). Her one front face is s11
  (the +3 reaction, silent, lips pressed, a small smile at the very end; bible rule 40's suggested place), next to the medium back
  shot s11b (a different size, rule 40). The paper ledger of c12 / c23 is not written (rules 7, 27, 38: from behind it is not
  seen anyway). The abacus is the plain dark wooden one, only in the insert s07 and held in s03, s08-s11b (rule 20).

THE AXES (rules 29, 42: the pictures decide):
- The Xu room by night (set-xujia-wu-ye-l1, e922's: earthen brick walls, a small window in the back wall at the LEFT, black with
  night; one small dark square table in the middle-right with one small flame on it; a big clay jar in the left corner; loose
  straw on the floor; the door off screen right). Bible rule 42: Xu Yan sits at the LEFT side of the table facing screen right;
  Tang Xiaotang comes in from the right, off screen; little Xiaohe crouches under the table. The window is behind Xu Yan at the
  left: the locusts are "small dark shapes" thumping against its frame (the script's paper-window shadows: rule 42) and the
  hole of c05 is in its lower corner (s06 presses the cloth into it). Her back shots look past her (at the right side of the
  table) to Xu Yan at the left side (set-xujia-wu-ye-table-l1: the window top left, the table and its flame in the middle).
- The three fields two days later (set-hantian-yang-l1, round 2, 37039: set-hantian-l1 with the paddy in FRONT of the low ridge
  flooded and planted, sparse young seedlings in still water across the whole foreground; the dry cracked field beyond the
  ridge; houses and far hills at the LEFT and middle; the big old tree at the RIGHT with a raised grassy bank running from its
  foot along the right side of the paddy). The script's 「田埂在左、田在右；白線由左往右」 is the other way round in the picture:
  the people, the cages and the ducks start on the grassy bank at the RIGHT and the white line pushes LEFT across the water;
  Qian Yuanwai stands further along the same bank under the tree (the script's 「右邊田埂」). North (the swarm, 「蝗蟲又過山了」)
  is the far hills, which Tang Xiaotang faces from behind (s14).
- The village gate (set-cunkou-l1, round 2, 37040: a free-standing palisade gate of upright logs with crossed braces, one thick
  horizontal crossbar and a small tiled roof at the LEFT; a weeping willow in the middle; a plank bridge over a dry stone-lined
  ditch; a dirt road curving away to three small mud-brick houses at the RIGHT; dry fields and far hills; an orange-red evening
  sky). The picture has NO gate tower and no fences: the script's own fallback (〈五張清單〉 2: 「沒有的話，c31 錢員外改站在柵門旁
  的土台上」) puts Qian Yuanwai up on a low earthen mound beside the gate (s31, a low angle against the gate's roof); the gate's
  "crossbar" is the bar of the script (門閂). Inside the village is the camera's side and the road at the right; outside is past
  the gate at the left, where the refugees stand (s29) -- the bible's 〈接點〉 35->36 direction (gate left, road right).

PLACES (gen-dh SET takes the FIRST pattern in its list order that matches the prompt):
- The room: every LOC opens "Inside the farmhouse" -> dh-set-xujia-wu-t1 = pilot.py's newest set-xujia-wu (the DAY room, l1),
  which spec.json swaps for set-xujia-wu-ye-table-l1 (s01, s03, s04, s08, s09, s11b) and the free crops -chuang (s02, s02b, s06,
  s10), -qiang (s11), -zhuo (s07, the abacus insert), -di (s05). No "yard", "mud wall", "kitchen" or "pool" in a room prompt.
- The fields: as e034's fields, the LOC carries " below the deep pool" (POOLMARK) only so gen-dh sends set-shentan-l3, which
  spec.json swaps; mkspec.py takes the words out of every d1 prompt (the picture shows no pool). The afternoon under the swarm:
  the free brown grade set-hantian-yang-zong-l1 (s12) and its crops -zong-liu (s12b, s16), -zong-an (s13, s17), -zong-tian (s14),
  -zong-geng (s15, s18), -zong-shui (s17b); that evening the orange grade -xi (s19); the next dawn the misty grade -chen (s20) and
  -chen-liu (s20b, s22, s23, s24), -chen-shui (s21, the insert), -chen-an (s25).
- The gate: every LOC opens "At the village entrance" -> dh-set-cunkou-t1 = set-cunkou-l1 (s26, not swapped), and the free crops
  -kong (s27, s30), -men (s28, s29, s32, s34), -ding (s31), -dao (s33), -zha (s35, the insert).
Shared files: none changed (build-r2.py's EN has every speaking name on screen; the refugee woman's voice is MINOR, her line a
recording; gen-dh.mjs, pilot.py, cast.json untouched). The d1 prep (colab/runs/e935/extras.json, colab/runs/e935-live/
{mkspec.py,spec.json,PREP.md}, the scratchpad's tools/prep935.sh, rec935.sh and e935d1.sh) was written 2026-11-20.
e034 is cut but may still change: s01 follows the last 15 s of e934-live.mp4 (PREP.md) and must be checked again once it is final.
"""
EP = 935  # internal working number; the published slug is zhong-tian-qu-qi-e035-r2
SLUG = "zhong-tian-qu-qi-e035-r2"
EP_TITLE = "鴨子大軍（重製版 r2）"
OUTLINE_SECONDS = 193  # script.md: about 193 s, 35 shots (11 + 14 + 10)
TARGET_MINUTES = [3, 4]
TITLE = "三千隻鴨子，一聲短哨！蝗群壓境，柳溪三畝保住了｜種田娶妻打天下 第35集（重製版）"
DESCRIPTION = "蝗群壓過山頭的那一夜，蝗蟲一下一下撞在許家的窗上。許硯兌換了當初笑最大聲的鴨群治蝗法——唐小棠推門進來：鴨子？你說要幾隻？三千隻，三個縣的鴨子全要。一隻三十文，九十兩，銀子差一半。那就拿許記的字號去賒。「拿全家的信用，押在我一個人的判斷上？」「押。」兩天後，三千隻鴨子從竹籠裡湧出來，到處亂跑，還站到許硯頭上；阿令只說：給我一根長竹竿，再給我一天。隔天清晨，一聲短哨，一條白線湧進田裡，錢員外笑不出來了。五天後傍晚，鄰村的田全被啃光，柳溪那三畝是青的——天下歸心，百分之一到百分之二。流民擠在村口，錢員外喊：關門！糧不夠！許硯的手按在門閂上。《種田娶妻打天下》第 35 集（重製版）。"
THUMB = ("三千隻鴨子！", "s20")
CHARACTERS = ["xuyan", "tangxiaotang", "xiaohe", "aling", "qianyuanwai", "liumin", "xitong"]
# 〈小角色〉 (bible): the refugee woman has no portrait and no on-screen speech; only her voice (Erinome, the bible's choice).
MINOR = {
    "liumin": {"id": "liumin", "name": "流民婦人",
               "appearance": "East Asian village woman of about thirty, thin and worn, a faded blue head cloth, a ragged grey-brown homespun jacket, a small child on her hip; seen only from behind",
               "voice": {"provider": "gemini", "name": "Erinome", "style": "標準國語，咬字清楚，台北人平常說話的語調；三十歲的逃荒婦人，女聲、沙啞疲憊，帶著哭腔哀求，句尾發抖"}},
}
MUSIC = "one cue per scene: a low tense drone under the dry rasp of insects against a window by one small flame at night, turning tender on a single word of trust, one soft chime; then a scrappy comic tune of plucked strings and woodblocks as white ducks scatter everywhere, falling silent for a quiet woman, a wide soaring melody at a misty dawn as a white line of ducks sweeps into a green paddy, one low note under a sour landlord; then a warm wide harvest melody at an orange dusk village gate, cut off by a shout, low strings rising and held unresolved; ancient Chinese rural drama, no vocals"

# Places.
H1 = "Inside the farmhouse of the Xu family late at night on the tenth day of the drought"
NIGHT = "the one small warm flame on the table the only light, the corners of the room deep in shadow, the small window black with night"
ROOM = ("earthen brick walls, a small window in the back wall at the left, one small dark square table in the middle with one small "
        "flame on it, a big clay jar in the left corner, loose straw on the packed-earth floor")
POOLMARK = " below the deep pool"  # mkspec.py takes it out of every field shot in d1 (gen-dh's SET needs "deep pool")
F2 = f"On the three small fields of Liuxi{POOLMARK} in the afternoon two days after the swarm night"
ZONG = "a dull brown half-light, the sun a pale disc high in a dull brown sky"
F3 = f"On the three small fields of Liuxi{POOLMARK} at sunset the same day"
XI = "low warm orange evening light"
F4 = f"On the three small fields of Liuxi{POOLMARK} at dawn the next morning"
CHEN = "soft grey-gold dawn light, a thin white mist lying low over the water"
FIELD = ("the flooded paddy of sparse young green rice seedlings in still shallow water across the front, a low dark ridge across "
         "the middle, the dry cracked bare field beyond it, a row of small houses and far hills at the left, a big old tree at the "
         "right with a raised grassy bank running from its foot along the right side of the paddy; only this one paddy is green, "
         "the fields beyond the ridge dry and bare")  # 原版必修 e035
K1 = "At the village entrance of Liuxi at dusk five days after the swarm night"
DUSK = "a warm orange-red evening sky, the sun just gone below the far hills"
GATE = ("a free-standing palisade gate of upright logs with crossed braces, one thick horizontal wooden crossbar across it and a "
        "small tiled roof on top, at the left")
ENTRANCE = (f"{GATE}, a weeping willow in the middle, a plank bridge over a dry stone-lined ditch, a dirt road curving away to three "
            "small earthen-walled houses at the right, dry fields and far hills beyond")
LOC = {
    "ye": f"{H1}: the room exactly as in the picture: {ROOM}; {NIGHT}",
    "ye_c": f"{H1}, by the small dark square table; {NIGHT}",
    "ye_w": f"{H1}, by the small window in the back wall; {NIGHT}",
    "ye_e": f"{H1}; {NIGHT}",  # the insert s07: mkspec.py leaves only "Insert close-up" (rule 35)
    "zg": f"{F2}: the field exactly as in the picture: {FIELD}; {ZONG}",
    "zg_b": f"{F2}, on the raised grassy bank at the edge of the flooded paddy; {ZONG}",
    "zg_e": f"{F2}; {ZONG}",
    "xi": f"{F3}: the field exactly as in the picture: {FIELD}; {XI}",
    "ch": f"{F4}: the field exactly as in the picture: {FIELD}; {CHEN}",
    "ch_b": f"{F4}, on the raised grassy bank at the edge of the flooded paddy; {CHEN}",
    "ch_t": f"{F4}, on the grassy bank under the big old tree at the edge of the paddy; {CHEN}",
    "ch_e": f"{F4}; {CHEN}",  # the insert s21: mkspec.py leaves only "Insert close-up"
    "kk": f"{K1}: the entrance exactly as in the picture: {ENTRANCE}; {DUSK}",
    "kk_g": f"{K1}, by the palisade gate; {DUSK}",
    "kk_e": f"{K1}; {DUSK}",  # the insert s35: mkspec.py leaves only "Insert close-up"
}
LIGHT = {
    "night": "the warm light of the one small flame stays unchanged",
    "zong": "the dull brown half-light stays unchanged",
    "xi": "the low orange evening light stays unchanged",
    "chen": "the soft grey-gold dawn light stays unchanged",
    "dusk": "the orange-red evening light stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_COAT = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow with an old grey cloth outer coat worn loose over "
           "his shoulders, dark shadows under his eyes")  # bible 〈人物〉: the outer coat by night
XU_DAY = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves rolled up to the elbows"
XU_MESSY = f"{XU_DAY}, his topknot knocked askew, a few strands of black hair fallen across his forehead"  # c13-c18 (no mud)
XU_EVE = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow"
XIAOHE = ("little Xiaohe, an eight-year-old girl in her patched lilac cotton jacket, her two little pigtails tied with red string, "
          "one front tooth missing, a small woven straw rabbit tucked into the cloth sash at her waist")
ALING_DUCK = ("A-ling, in her plain grey-white cotton dress tailored close at the waist with a cloth sash, its long sleeves covering "
              "both wrists, bound tight at the wrists with strips of grey cloth, the hem of the skirt over grey cloth leg wraps, her "
              "long black hair pinned up with one plain wooden hairpin, one small bamboo whistle on a thin cord round her neck")
POLE = "one long plain bamboo pole about twice her height"  # bible 〈道具〉: one
QIAN = ("Qian Yuanwai, short and portly with a round face and a thin eight-shaped moustache, in his dark gold silk robe woven "
        "with small round medallions, the front of the robe plain brocade, three gold rings on his fingers")
RETAINERS = ("two men in identical Song-dynasty black cross-collared short jackets, black cloth head wraps and cloth shoes, their "
             "hands empty at their sides")
ABACUS = "one plain dark wooden abacus, a flat dark wooden frame with round dark beads on thin rods"  # bible rule 20
CAGES = "a long row of big round woven bamboo cages stacked two high along the bank"
MEN4 = ("four men in Song-dynasty cross-collared homespun short jackets, cloth head wraps and cloth shoes, each a different colour "
        "and age: a lean young man in a rust-red jacket, a stocky middle-aged man in a dull olive-green jacket, an older man with a "
        "short grey beard in a faded undyed hemp-beige jacket and a broad young man in a dark charcoal jacket")
MAN1 = "a lean young man in a Song-dynasty cross-collared rust-red homespun short jacket, a cloth head wrap and cloth shoes"
GUARDS = ("two men in Song-dynasty cross-collared homespun short jackets, cloth head wraps and cloth shoes, a broad young man in a "
          "dark teal jacket and a wiry middle-aged man in a deep wine-red jacket")
REFUGEES = ("ten people in ragged Song-dynasty homespun clothes, cloth head wraps and worn straw sandals, cloth bundles on their "
            "backs, each a different colour and age: an old man with a short grey beard in a faded undyed hemp-beige jacket and a "
            "bent old woman in a faded deep plum jacket kneeling in the front row, a lean middle-aged man in a dark charcoal jacket, "
            "a young woman in a rust-red jacket holding a small boy by the hand, a boy of about ten in a mustard-yellow jacket, a "
            "stocky middle-aged man in a dull olive-green jacket, a thin young man in a faded maroon jacket, a stooped grey-haired "
            "man in a dark brown jacket and a middle-aged woman in a dark grey jacket with a faded indigo head cloth")
TORCHES = "six of the standing people each hold up one burning pine torch in one hand, at walking height"  # rule 37
WOMAN_BACK = ("one woman seen only from behind, a faded blue head cloth over her hair and a ragged grey-brown homespun jacket, a small "
              "child held on her hip, its face hidden against her shoulder, the back of her head toward us the whole shot")
SWARM = ("a low dark brown band made of countless tiny dark specks pressing over the far hills, its leading edge breaking up into "
         "scattered specks")  # bible 〈道具〉 蝗群 (e034's wording)
LOCUST = "one small brown locust"
DUCKS = "white farm ducks with orange bills and orange feet"
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# rule 40 (e031 / e033 TBACK): Tang Xiaotang from behind, her l1 costume (rule 4), no outer coat
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with every strand of her black hair "
         "combed smooth and gathered up into just two round buns set high on her head, one bun on each side, one short pink "
         "silk ribbon wrapped around each bun, the nape of her neck bare and clear above a pink inner collar, and her light "
         "peach-pink silk shoulders; the back of her head facing straight away from us the whole time, her head still, her ear "
         "the furthest round her head we ever see")
TBACK_SMALL = ("one young woman seen only from behind, appearing only once, her black hair in just two round buns set high on her "
               "head tied with short pink silk ribbons, in a light peach-pink silk jacket and skirt")
HEADSTILL = "the young woman with the two high round buns keeps her head still, facing straight away from us, the back of her head toward us the whole shot"
TANG_EDGE = ("at the right edge of the frame, cut by it, soft and out of focus, only the back of a young woman's head with two round "
             "buns tied with short pink silk ribbons and one light peach-pink silk shoulder, toward us the whole shot")
# rule 40: the one silent front face (s11), her l1 costume (rule 4; e031 s21b's wording)
TANG_FACE = ("Tang Xiaotang, a young woman of eighteen with a round soft face and big round eyes, in her peach-pink silk "
             "cross-collared short jacket closed at the neck, her black hair in two round buns tied with short pink ribbons")
# rule 2: over-the-shoulder backs, unnamed, no picture
BACK_XU = ("at the left edge of the frame, cut by it, soft and out of focus, only the back of one shoulder in a faded blue-grey "
           "robe and the back of a man's topknot, toward us the whole shot")
# set-only sides (the picture of each place, all the way to the edge)
SIDE_WALL = "the earthen brick wall in the warm light of the one small flame"
SIDE_DARK = "the dark earthen brick wall"
SIDE_SKY = "the orange-red evening sky"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def only_tang():
    return "she is the only young woman with two high round buns in the frame"


def alone(rest, where, frame="framed from the waist up", shot="medium shot", lead=""):
    """Tang Xiaotang from behind, in the middle of the frame (not at an edge: the pickers' cheek at the frame edge)."""
    return f"{shot} from close behind{lead} {TBACK}, {where} in the middle of the frame, {frame}, facing straight away from us; {only_tang()}; {rest}"


def off(side, what, he="he"):
    """A line to someone outside the frame: the gaze, that side set only, and the only person (rule 31)."""
    edge = f"the {side} edge of the frame"
    return (f"toward someone out of sight beyond {edge}, never the lens; that side of the frame is only {what} all the way to the "
            f"edge, and {he} is the only person in the frame")


BEYOND_XU = "one step beyond her in the left third of the frame, his whole figure clear of her head and shoulders"
ROOM_BACK = "behind them, soft, the earthen brick wall and the small window black with night in the warm light of the one small flame"
TWO_BACK = "exactly two people, the young woman in the middle seen only from behind"

SHOTS = [
    # ---- scene 1: the swarm night of the tenth day, the Xu room (34->35: the same night as e034 s40).
    dict(chapter="許家屋內，蝗群壓境的夜", loc="ye_c", cam="Medium shot, slow push in", chars=["xuyan"], night="night",
         comp=f"medium shot across the small dark square table, its one small flame soft and out of focus in the right foreground: sitting on a low round stool at the left side of the table, {XU_COAT}, framed from the waist up, both forearms resting on the tabletop, his face already turned over his left shoulder toward the small window in the back wall from the first frame, never the lens; behind him the small window, black with night, small dark shapes thumping against its wooden frame one after another; tense and tired, not smiling: brows drawn, lips pressed shut; he is the only person in the frame; {HANDS}",
         lines=[("xitong", "叮。兌換：鴨群治蝗法。", "冷，宣布"), ("xitong", "當初笑得最大聲的，也是宿主。", "冷")],
         panel=[("兌換：鴨群治蝗法", "reward")],
         motion=f"one small dark shape thumps against the window frame behind him, and Xu Yan turns his eyes from the window back to the empty air before him and his fingers tighten on the tabletop; {SILENT_HE}",
         zh="中景、慢推（送 e922 的 `set-xujia-wu-ye-table-l1`：左上是窗、中間小方桌與桌上一朵火；前景右是虛焦的那朵火，稿子『前景是桌上的油燈』照圖寫成桌上一朵火、不寫蠟燭，聖經拍法 42）：**接點 34→35**：第 34 集 s40 是日落轉灰的田邊、三個背影望著遠山上的蝗群（`e934-live.mp4` 最後 7 秒，**第 34 集定版後再核**）；本鏡同一夜、許家屋內（聖經〈接點〉34→35）。許硯披舊灰外衣（聖經：夜裡加外衣）坐在桌**左側**圓凳上、面向畫右（拍法 42），第一格已經回頭望身後左上的窗；窗外黑暗裡一個個小黑影撞上窗框（稿子『窗紙上蝗蟲的影子』改成拍法 42 的寫法，加音效）；一個小黑影撞上來，他眼睛從窗回到面前的空氣、手指在桌上收緊（稿子『抬頭看窗』在第一格完成）。系統兩句都是錄音、**全程嘴閉著**；面板剪接時疊，**不寫淡藍光**（拍法 11）。長鏡"),
    dict(loc="ye_c", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU_COAT}, sitting at the table, framed from the chest up with space above his head, his face three-quarter to screen right, his eyes on the empty air before him, never the lens; he is the only person in the frame; rueful, not smiling: brows drawn, lips pressed shut; behind him, soft, the earthen brick wall and the small window black with night, a small dark shape thumping against its frame; {HANDS}",
         lines=[("xuyan", "我認錯。鴨子現在是我的救命恩人。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan rubs one flat hand slowly down over his face and lets out a long breath; {SILENT_HE}",
         zh="近景、慢推（送本集免費做的 `set-xujia-wu-ye-chuang-l1`：土磚牆與窗，稿子『身後只有土牆與窗紙的亂影』）：本集的鬥嘴，回系統 s01；許硯抹一把臉、吐一口氣（一個動作），心裡話是錄音、**全程嘴閉著**。稿子 c02 一鏡裡先心裡話再開口說，嘴從閉到開模型對不準，拆成本鏡（閉嘴）與 s02b（開口）"),
    dict(sid="s02b", loc="ye_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"medium close-up of {XU_COAT}, sitting at the table, framed from the waist up, both forearms on the tabletop, his eyes already steady from the first frame, his face three-quarter to screen right, his eyes on the empty air before him, never the lens; he is the only person in the frame; resolved, not smiling: eyes narrowing, brows level, lips moving low and slow between words; behind him, soft, the earthen brick wall and the small window black with night; {HANDS}",
         lines=[("xuyan", "鴨子……得要很多很多的鴨子才行。", "低聲")],
         motion="Xu Yan's eyes settle and narrow and his hands close slowly into loose fists on the tabletop as he speaks low to himself",
         zh="中近景、慢推（送 `-chuang-l1`；跟 s02 不同景別）：稿子 c02 的後半：眼睛一定，低聲自語；手在桌上慢慢握成拳。拆鏡：s02 心裡話閉嘴、本鏡開口（台詞一句一筆，不拆半句）"),
    dict(loc="ye_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="night",
         comp=alone(f"{ABACUS} held under her left arm from the first frame; {BEYOND_XU}, {XU_COAT}, sitting at the left side of the small dark square table with its one small flame, framed from the waist up, his face lifted three-quarter to screen right toward her, his lips pressed shut, never the lens; startled, not smiling; {ROOM_BACK}; she stays in the middle of the frame the whole shot; {HANDS}; {TWO_BACK}",
                    "already standing on the packed-earth floor at the right side of the table,"),
         lines=[("tangxiaotang", "鴨子？你要鴨子做什麼？你說要幾隻？", "快")],
         motion=f"she steps up to the edge of the table, only her legs and her free arm moving; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `set-xujia-wu-ye-table-l1`）：唐小棠背影在畫面正中、頭不動、剛好兩顆丸子（拍法 40：說話從背後、放錄音、nospeak）、l1 交領短襦，**不寫淡杏外衣與高立領**（拍法 4）；左腋下夾一把素木算盤（聖經拍法 20：帳桌那把是木算盤）；第一格已經進門站在桌右側（稿子『推門、反手關門、快步走到桌邊』在第一格完成；推門關門交給音效，剪接照稿子剪在關門一半改成剪在她站定），往桌邊再跨一步；許硯坐在桌左側、在她前方一步的畫左三分之一，仰頭看她、嘴閉著（→ 答在 s04）"),
    dict(loc="ye_c", cam="Medium shot over the shoulder, slow push in", chars=["xuyan"], night="night",
         comp=f"medium shot over a shoulder: {TANG_EDGE}; beyond it, in the left half of the frame at the far side of the small dark square table, {XU_COAT}, already standing from the first frame, framed from the waist up, both flat hands planted on the tabletop, leaning toward the young woman in the foreground, his face three-quarter to screen right toward her, never the lens; urgent and sure, not smiling: brows level, eyes bright, lips moving fast between words; behind him, soft, the earthen brick wall and the small window black with night; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("xuyan", "三千隻。鴨子吃蝗蟲，三個縣的鴨子全要。", "一口氣")],
         motion="Xu Yan leans further over the table toward her as he speaks",
         zh="過肩中景、慢推（送 `-table-l1`）：前景右是虛焦、被畫框切掉的雙丸子後腦與桃粉肩頭（不點名、不送圖，拍法 2；稿子『唐小棠右肩後』）；許硯第一格已經站起來、兩手平掌撐在桌上（稿子『站起來』在第一格完成），再往她傾身、一口氣說（答 s03）"),
    dict(loc="ye_c", cam="Low-angle medium shot, slow push in", chars=["xiaohe"], night="night",
         comp=f"low-angle medium shot at a small child's height under the small dark square table: {XIAOHE}, crouching on the straw-strewn floor beneath the tabletop, framed from the waist up, the underside of the tabletop and its two dark legs around her, her face three-quarter to screen left toward the small window beyond the left edge of the frame, her eyes on it, never the lens; she is the only person in the frame; frightened, not smiling: eyes wide, brows up, lips moving fast between words; behind her, soft, the loose straw on the floor and the dark brick wall; {HANDS}",
         lines=[("xiaohe", "哥，牠們在咬窗戶，紙破了一個洞！", "有點怕")],
         motion="Little Xiaohe shrinks back under the table and stretches her flat right hand out toward the window as she speaks",
         zh="低角度中景（小禾的高度）、慢推（送本集免費做的 `set-xujia-wu-ye-di-l1`：桌腳與鋪乾草的地）：小禾蹲在桌下、草兔子塞在腰帶上（第 33、34 集的寫法），往後縮、右手平掌往畫左外的窗一伸（單指會讀錯，拍法 32），怕怕地說；臉在畫面上、沒有人擋（原版建議）。稿子『身後窗紙破洞、一隻蝗蟲的腳伸進來』不拍（窗在她背後畫左外；皮膚與小東西會長錯，拍法 12；洞交給台詞與 s06 塞布）"),
    dict(loc="ye_w", cam="Medium shot, slow push in", chars=["xuyan"], night="night",
         comp=f"medium shot by the small window in the back wall: {XU_COAT}, standing side-on at the window, framed from the waist up, his right palm already pressing a balled-up piece of old grey cloth into the lower corner of the window frame from the first frame, his face turned three-quarter to screen right over his shoulder {off('right', SIDE_WALL)}; gentle, not smiling: brows easing, lips moving softly between words; beside him the small window, black with night; {HANDS}",
         lines=[("xuyan", "別怕，哥把洞堵上，蝗蟲進不來。", "放軟")],
         motion="Xu Yan presses the cloth flat into the corner once more with his palm as he speaks over his shoulder",
         zh="中景、慢推（送 `-chuang-l1`）：許硯在後牆左邊的窗旁（拍法 42：窗在後牆左邊；稿子『窗在右後』照圖），右手掌第一格已經把團起來的舊灰布塞在窗框下角（稿子『走到窗邊、團布、塞洞』在第一格完成），再用手掌壓一下，回頭朝畫右外看不到的人（桌下的小禾，不點名）放軟地說（那一側到邊緣只有土牆）"),
    dict(loc="ye_e", cam="Insert close-up, slow push in", chars=[], night="night",
         comp=f"insert close-up from a little above, the very first frame is already a close view of {ABACUS} lying on the dark wooden tabletop, two small fair hands with light peach-pink silk cuffs resting on its beads; far below, soft and out of focus, only the dark wooden tabletop and the warm light of the one small flame fill the background to every edge; only the abacus and the two hands are in the frame",
         lines=[("tangxiaotang", "一隻三十文，三千隻是九十兩，銀子差一半。", "撥算盤，悶")],
         motion=NOBODY + "the fingers push the round beads quickly up and down along their rods, then stop still",
         zh="插鏡、慢推（第一格就是素木算盤與兩隻桃粉袖口的手，拍法 10、35；不寫地點句，送本集免費做的桌面裁切 `set-xujia-wu-ye-zhuo-l1` 只當桌面與光；聖經拍法 20、35 列的『第 35 集算盤』插鏡）：稿子 c07 是唐小棠下巴以上撥算盤說話的近景，真人版她不露嘴說話（拍法 3、40），改成算盤插鏡、她的話放錄音（畫外）；手指飛快撥珠、停住（不寫單指，拍法 32）"),
    dict(loc="ye_c", cam="Medium shot over the shoulder, slow push in", chars=["xuyan"], night="night",
         comp=f"medium shot over a shoulder: {TANG_EDGE}; beyond it, in the left half of the frame at the far side of the small dark square table, {XU_COAT}, standing, framed from the waist up, {ABACUS} lying on the tabletop before him, his right hand already resting flat on it from the first frame, his face three-quarter to screen right toward the young woman in the foreground, never the lens; calm and level, not smiling: brows level, lips moving evenly between words; behind him, soft, the earthen brick wall and the small window black with night; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("xuyan", "那就拿許記的字號，去三個縣賒。", "平穩")],
         motion="Xu Yan taps the abacus once with his flat right hand and lifts his eyes to her as he speaks",
         zh="過肩中景、慢推（送 `-table-l1`，同 s04 的機位）：許硯第一格已經走回桌邊、右手平掌放在算盤上（稿子『走回來』在第一格完成；『手指點一下』改平掌一拍，拍法 32），抬眼看她、平穩地說"),
    dict(loc="ye_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="night",
         comp=alone(f"her right hand already lifted off the tabletop from the first frame; {BEYOND_XU}, {XU_COAT}, standing at the far side of the small dark square table, {ABACUS} lying on the tabletop between them, framed from the waist up, his face three-quarter to screen right toward her, his lips pressed shut, never the lens; steady, not smiling; {ROOM_BACK}; she stays in the middle of the frame the whole shot; {HANDS}; {TWO_BACK}",
                    "standing at the near side of the table,"),
         lines=[("tangxiaotang", "拿全家的信用，押在我一個人的判斷上？", "不敢信")],
         motion=f"her right hand comes up and presses flat against her chest, only her arm moving; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-table-l1`）：稿子 c09 是反打她的正臉，真人版照拍法 40 從背後拍：她背影在正中、頭不動，右手第一格已經從算盤上收回來，按到胸前（只動手臂）；許硯在她前方一步的畫左三分之一、看著她、嘴閉著（→ 答在 s10）"),
    dict(loc="ye_c", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU_COAT}, standing by the table, framed from the chest up with space above his head, his face three-quarter to screen right {off('right', SIDE_WALL)}; steady and sure, not smiling: eyes calm, brows level, lips moving evenly between words; behind him, soft, the earthen brick wall and the small window black with night; {HANDS}",
         lines=[("xuyan", "押。妳的帳，三十天一筆都沒錯過。", "乾脆")],
         motion="Xu Yan gives one firm nod as he speaks",
         zh="近景、慢推（送 `-chuang-l1`；稿子『身後只有土牆與油燈光』）：許硯點一下頭，朝畫右外看不到的人（唐小棠，不點名）乾脆地說（答 s09）；**不笑、很穩**"),
    dict(loc="ye_c", cam="Close-up, slow push in", chars=["tangxiaotang"], night="night",
         comp=f"close-up of {TANG_FACE}, standing by the table, framed from the chest up with space above her head, {ABACUS} held against her chest in both arms from the first frame, her face three-quarter to screen left {off('left', SIDE_DARK, he='she')}; moved: her big round eyes welling and shining, her lips pressed together; behind her, soft, only the dark earthen brick wall in the warm light of the one small flame; {HANDS}",
         lines=[("xitong", "叮。唐小棠，好感加三。", "冷，宣布")],
         panel=[("唐小棠 好感 +3 → 45", "affection")],
         motion=f"Tang Xiaotang sniffs once and hugs the abacus closer, and at the very end the corners of her pressed lips lift into a small smile; {quiet('Tang Xiaotang', 'her')}",
         zh="近景、慢推（送本集免費做的 `set-xujia-wu-ye-qiang-l1`：桌右邊的暗土磚牆；送 `tangxiaotang-portrait-l1` 與 angle-a）：**本集唯一一鏡唐小棠的正臉**（拍法 40：不說話的正臉每集最多兩鏡，聖經建議用在『第 35 集好感 +3 的反應』）：她兩手把算盤抱在胸前、眼眶一熱，吸一下鼻子，最後嘴閉著、嘴角小小揚起（稿子『本鏡最後可以笑』）；系統是錄音、她**全程嘴閉著**；朝畫左外看不到的人（許硯，不點名）。面板剪接時疊（← 因為 s10）。稿子 c11 的後半『好。天一亮我就去』拆到 s11b 從背後說（下一鏡不同景別：近景正臉→中景背影，拍法 40）"),
    dict(sid="s11b", loc="ye_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="night",
         comp=alone(f"{ABACUS} already held against her chest in both arms from the first frame; {BEYOND_XU}, {XU_COAT}, standing at the far side of the small dark square table, framed from the waist up, his face three-quarter to screen right toward her, his lips pressed shut, never the lens; warm, not smiling: his eyes softening; {ROOM_BACK}; she stays in the middle of the frame the whole shot; {HANDS}; {TWO_BACK}",
                    "standing at the near side of the table,"),
         lines=[("tangxiaotang", "好。天一亮我就去，收割以後一併還。", "下巴一抬")],
         motion=f"she hugs the abacus tighter to her chest, only her arms moving; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-table-l1`）：稿子 c11 的後半：唐小棠背影、頭不動，兩手把算盤抱得更緊，說『天一亮就去』（錄音；第一場結尾）；『下巴一抬』從背後看不到、交給語氣；許硯看著她、眼神放軟、嘴閉著。好感面板在 s11"),
    # ---- scene 2: the three fields, two days later (the afternoon under the swarm), that evening, the next dawn.
    dict(chapter="柳溪三畝田，兩天後到隔天清晨", loc="zg", cam="Wide shot, slow push in", chars=[], night="zong",
         comp=f"wide shot at standing eye height along the raised grassy bank at the right of the paddy, like the picture: on the bank in the right foreground {CAGES}, their lids already lifted from the first frame; beside them, small, framed full figure, {MEN4}, each lifting the lid of one more cage, their lips closed, never the lens; {DUCKS} already pouring out of the cages from the first frame and spilling down the bank into the shallow water of the paddy at the left; {HANDS}; exactly four people",
         motion=NOBODY + "more and more white ducks squeeze out of the cages and tumble down the bank into the water, scattering every way across the paddy",
         zh="全景、慢推（人眼高、照圖；送本集免費做的棕色調色 `set-hantian-yang-zong-l1`：`set-hantian-yang-l1` 先塗掉遠處三根小竿（同第 34 集 `set-hantian-l1`），再壓暗、去飽和、偏棕——蝗群壓在天上的半明半暗）：**兩天後下午**（時間跳在 s11b→s12 這一刀，由一排竹籠交代鴨子到了，稿子〈離開這場〉）。田埂照圖在**右邊**大樹下那道長草的高田埂（稿子寫田埂在左、田在右：圖上相反，拍法 29），一排疊兩層的大竹籠、籠蓋第一格已經掀開（寫 lifted，不寫 open，拍法 36），四個村民（鐵鏽紅、暗橄欖綠、短灰鬚的本色麻、炭灰；稿子『六個男人』照拍法 34 寫看得見的四個）再掀一個；白鴨嘎嘎擠出來、滾下田埂、在水田裡四散。三千隻交給音效與台詞（不寫數字，拍法 34）。稿子 c12 拆兩鏡：本鏡鴨子出籠、s12b 唐小棠報帳（一鏡一個動作）。無台詞"),
    dict(sid="s12b", loc="zg_b", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="zong",
         comp=alone(f"her hands empty at her sides from the first frame; {BEYOND_XU}, {XU_DAY}, standing on the grassy bank, framed from the waist up, his face three-quarter to screen right toward her, his lips pressed shut, never the lens; listening, not smiling; behind them, soft, white ducks scattering across the shallow water of the paddy and the big old tree in the dull brown half-light; she stays in the middle of the frame the whole shot; {HANDS}; {TWO_BACK}",
                    "standing on the raised grassy bank,"),
         lines=[("tangxiaotang", "三個縣的鴨子都到了，四十五兩現銀，四十五兩賒帳。", "喘，下巴抬著")],
         motion=f"her right arm swings out and her flat right hand sweeps toward the ducks on the water, only her arm moving; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-zong-liu-l1`：大樹、長草田埂與水田）：唐小棠背影在正中、頭不動（拍法 40），右手平掌往水田裡的鴨子一揮（只動手臂）報帳；許硯在她前方一步的畫左三分之一、袖子捲起、嘴閉著。稿子『手裡一本摺起的帳冊、拍拍帳冊』不寫（紙與冊子會長字，拍法 7、27、38；從背後也看不到）。錢：付四十五兩、賒四十五兩（設定〈錢〉）"),
    dict(loc="zg_b", cam="Medium shot, slow push in", chars=["xuyan"], night="zong",
         comp=f"medium shot at the edge of the grassy bank by the water: {XU_MESSY}, already sitting down hard on the grass at the edge of the paddy from the first frame, framed from the waist up, one white farm duck with an orange bill and orange feet standing on top of his head, its wings spread, both his hands raised halfway toward it, his face tipped up toward the duck, never the lens; flustered, not smiling: eyes wide, brows high, lips pressed shut; a few white ducks rushing past him along the bank; he is the only person in the frame; {HANDS}",
         lines=[("xiaohe", "哥，你看，鴨子都騎到你頭上去了！", "笑到打嗝")],
         motion=f"the duck on his head flaps its wings and Xu Yan's raised hands hover, afraid to grab it; {SILENT_HE}",
         zh="中景、慢推（送 `-zong-an-l1`：水邊的長草田埂與大樹樹幹）：許硯第一格已經被撞倒、跌坐在水田邊的草上（稿子『被撞倒』在第一格完成，剪接照稿子從鴨子跳上頭開始），**一隻白鴨站在他頭頂上、張著翅膀**（原版建議：鴨子真的站在跌坐的許硯頭上），他兩手舉到一半、要抓又不敢；**不笑**、一臉狼狽。稿子『坐在泥裡、袍子沾泥』不寫泥（第 32 集 fix3；第 34 集決定完全不寫泥），改寫髮髻撞歪、幾縷頭髮垂到額前。小禾的話是畫外錄音（笑到打嗝），許硯嘴閉著"),
    dict(loc="zg_b", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="zong",
         comp=alone(f"her left hand already raised to the back of her head from the first frame, holding down one short pink ribbon tossing in the wind; far ahead of her over the dry field and the houses, {SWARM}; she stays in the middle of the frame the whole shot; she is the only person in the frame; {HANDS}",
                    "standing on the raised grassy bank, facing the far hills,"),
         lines=[("tangxiaotang", "鴨子不聽話，到處亂跑，蝗蟲又過山了！", "急")],
         motion=f"her right arm swings up and her flat right hand stretches out toward the far hills, only her arm moving; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-zong-tian-l1`：棕色的天、遠山與一條田）：稿子 c14 是她下巴以上回頭看北邊的近景，真人版從背後拍（拍法 40）：她背對我們、面向北邊的遠山，左手第一格已經按住被風吹亂的一條粉緞帶，右手平掌往遠山一伸（只動手臂）；遠山上一條**無數小黑點組成的褐黑色帶子**壓過來（聖經〈道具〉蝗群列、第 34 集 s40 同一句；不是煙）。整句**不笑**（原版建議）——從背後本來就看不到笑"),
    dict(loc="zg_b", cam="Medium shot, slow push in", chars=["xuyan"], night="zong",
         comp=f"medium shot on the grassy bank: {XU_MESSY}, already back on his feet from the first frame, framed from the waist up, his face three-quarter to screen left toward the white ducks scattering every way across the shallow water, his eyes on them, never the lens; he is the only person in the frame; out of breath, not smiling: chest heaving, brows drawn, lips moving between panting words; behind him, soft, the paddy with white ducks scattered across it, the low ridge, the dry field and the houses in the dull brown half-light; {HANDS}",
         lines=[("xuyan", "誰能讓三千隻鴨子，往同一個方向走？", "喘")],
         motion="Xu Yan brushes down the front of his robe with both hands as he speaks, his eyes on the ducks",
         zh="中景、慢推（送 `-zong-geng-l1`：水田、田埂、乾田、小屋與遠山）：許硯第一格已經爬起來站好（頭上的鴨子已經飛走：稿子『爬起來、鴨子飛走』在第一格完成），頭髮亂，兩手拍一下袍子前襟，看著四散的鴨子喘著問（→ 答在 s16）；**不笑**"),
    dict(loc="zg_b", cam="Wide shot, slow push in", chars=["aling"], night="zong",
         comp=f"wide shot on the raised grassy bank at the right of the paddy, both framed full figure: at the left {ALING_DUCK}, already arrived along the bank from the first frame, her right hand reaching out toward {POLE} held upright in both hands by {MAN1}, who stands at the right, the pole well apart from her, his lips closed, never the lens; her face three-quarter to screen right toward the pole, her eyes on it, never the lens; quiet and even, not smiling: brows level, lips moving softly between words; behind them, soft, the big old tree and white ducks scattered across the paddy in the dull brown half-light; {HANDS}; exactly two people",
         lines=[("aling", "給我一根長竹竿，再給我一天。", "很輕")],
         motion=f"A-ling takes the pole out of the man's hands and stands it upright beside her as she speaks; {quiet('The man', 'his')}",
         zh="全景、慢推（送 `-zong-liu-l1`）：阿令（送 `aling-portrait-l1`，沒戴鐵鐐，就是稿子要先畫的 t2，**不用另畫**；不戴面巾、木簪）第一格已經沿田埂走到、袖口已經用灰布條紮緊、裙下綁腿、脖子上細繩掛一支小竹哨（稿子『邊走邊紮袖口』在第一格完成；聖經〈人物〉：定妝照沒有綁腿與紮袖，畫不出來就接受）；一個村民（鐵鏽紅）兩手豎著一根約兩人高的竹竿、跟她分開；她伸手把竹竿拿過來、豎在身邊，很輕地說（答 s15）。跟拍改慢推；『其他人讓開』不拍（只寫兩個人）"),
    dict(loc="zg_b", cam="Close-up, slow push in", chars=["aling"], night="zong", act=3,
         comp=f"close-up of {ALING_DUCK}, standing on the grassy bank, framed from the chest up with space above her head, the small bamboo whistle already held between her lips from the first frame, {POLE} standing upright beside her, its upper end rising past the top edge of the frame, well apart from the whistle's cord, her face three-quarter to screen left toward the ducks on the water beyond the left edge of the frame, her eyes on them, never the lens; she is the only person in the frame; blank and cool, not smiling; behind her, soft, the grassy bank, the trunk of the big old tree and white ducks milling on the water in the dull brown half-light; {HANDS}",
         motion="A-ling blows one short sharp blast on the whistle, her cheeks hollowing once, and holds still; she says nothing in this shot: her lips stay closed round the whistle from the first frame to the last, no talking, no mouthing words",
         zh="近景、慢推（送 `-zong-an-l1`）：阿令面無表情，小竹哨第一格已經含在嘴裡（稿子『含進嘴裡』在第一格完成），短短吹一聲（音效短哨）；竹竿立在身邊、竿頂出框、跟哨繩分開。稿子 c17 一鏡裡還有『前面幾隻鴨子同時回頭』與唐小棠的畫外話：近景裡鴨子在她身後虛焦、讀不出回頭，拆到 s17b 的鴨子特寫，唐小棠的話跟著過去。本鏡無台詞"),
    dict(sid="s17b", loc="zg_e", cam="Close-up low over the water, slow push in", chars=[], night="zong",
         comp=f"close-up low over the water: six {DUCKS} on the still shallow water of the paddy among sparse young green rice seedlings, already facing every which way from the first frame; beyond them, soft, only the water and the seedlings in the dull brown half-light; only the six ducks are in the frame",
         lines=[("tangxiaotang", "她連鴨子都會趕？她到底是什麼人？", "小聲，不敢信")],
         motion=NOBODY + "at the same moment all six ducks turn their heads the same way, toward the bank at the right, and hold still",
         zh="近景（貼水面）、慢推（送本集免費做的 `set-hantian-yang-zong-shui-l1`：水與稀疏的秧）：稿子 c17 的『前面幾隻鴨子同時回頭』：六隻白鴨在水田的秧間各朝一邊，**同時**把頭轉向右邊的田埂（阿令那邊）、定住；近景寫五到八隻（聖經〈道具〉鴨群列）。唐小棠的話是畫外錄音（小聲、不敢信；→ 答在 s18）"),
    dict(loc="zg_b", cam="Medium shot over the shoulder, slow push in", chars=["xuyan"], night="zong",
         comp=f"medium shot over a shoulder: {TANG_EDGE}; beyond it, in the left half of the frame on the grassy bank, {XU_MESSY}, standing, framed from the waist up, his face three-quarter to screen right toward the young woman in the foreground, never the lens; calm and firm, not smiling: brows level, lips moving evenly between words; behind him, soft, the shallow water of the paddy with white ducks on it, the low ridge and the dry field in the dull brown half-light; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("xuyan", "不問。她說給她一天，我們就等一天。", "搖頭")],
         motion="Xu Yan shakes his head once, slowly, as he speaks",
         zh="過肩中景、慢推（送 `-zong-geng-l1`）：前景右虛焦的雙丸子後腦與桃粉肩頭（不點名，拍法 2；稿子『唐小棠右肩後』）；許硯搖一下頭、平穩地說（答 s17b；← 因為第 31 集「好，不問」）。稿子『看著阿令的背影』『伸手按一下唐小棠的肩』不拍（一鏡一個動作；伸手到前景的肩會碰到虛焦的人）；**不笑**"),
    dict(loc="xi", cam="Wide shot, slow push in", chars=["aling"], night="xi", act=3,
         comp=f"wide shot at standing eye height, like the picture, in the low orange evening light: on the raised grassy bank at the right of the paddy, small, framed full figure, {ALING_DUCK}, alone, {POLE} already held out low over the water in both hands from the first frame, her face toward the ducks, never the lens; on the shallow water before her a loose flock of {DUCKS} swimming after the tip of the pole; she is the only person in the frame; {HANDS}",
         motion=f"A-ling sweeps the pole slowly round to the left and the whole flock turns on the water and follows its tip; {quiet('A-ling', 'her')}",
         zh="全景、慢推（送本集免費做的橘色調色 `set-hantian-yang-xi-l1`）：**同一天傍晚**（時間跳在 s18→s19 這一刀、用光交代，稿子場頭）：阿令一個人在右邊田埂上，兩手把竹竿低低伸到水面上，一群白鴨（約一百隻，不寫數字）跟著竿頭；竿子往左一擺、整群鴨子轉向跟著（稿子『短吹一聲、竿子一擺；再吹一聲、鴨子停下』只留一個動作，哨聲交給音效）。交代她練了一整天。無台詞"),
    dict(loc="ch", cam="Wide shot, slow push in", chars=["aling"], night="chen",
         comp=f"wide shot from low over the water, like the picture, in the soft grey-gold dawn light with a thin white mist on the water: in the near foreground, soft, a few sparse young green rice seedlings, {LOCUST} clinging to the nearest leaf; on the raised grassy bank at the right, small, framed full figure, {ALING_DUCK}, {POLE} already pointing out over the paddy toward the left from the first frame, the small bamboo whistle between her lips, never the lens; a long unbroken white line of {DUCKS}, packed close side by side, already pouring down off the bank into the shallow water from the first frame, stretching back along the bank toward the big old tree; she is the only person in the frame; {HANDS}",
         motion=f"the white line of ducks pushes steadily forward across the water toward the left, and the locust springs up off the seedling; {quiet('A-ling', 'her')}",
         zh="全景（低角度、貼水面）、慢推（送本集免費做的晨霧調色 `set-hantian-yang-chen-l1`）：**隔天清晨**、灰金光、水上一層薄霧（時間跳在 s19→s20）。前景虛焦的稀疏青秧、最近的一株上停著一隻褐色小蝗蟲；右邊田埂上阿令竹哨含在嘴裡、長竿第一格已經往左指向水田；**一條白線**（鴨子一隻挨一隻）第一格已經從田埂湧進水田、往左推進，秧上的蝗蟲被驚起（稿子『白線從左往右』：圖上田埂在右，照圖由右往左，拍法 29）。三千隻交給白線與音效（拍法 34）。稿子 c20 的小禾數鴨子拆到 s20b（一鏡一個動作、小孩在遠景裡讀不出數數）。無台詞"),
    dict(sid="s20b", loc="ch_b", cam="Medium close-up, slow push in", chars=["xiaohe"], night="chen",
         comp=f"medium close-up of {XIAOHE}, standing on the grassy bank, framed from the chest up with space above her head, her face three-quarter to screen left toward the white ducks on the water beyond the left edge of the frame, her eyes on them, never the lens; she is the only person in the frame; delighted and amazed: eyes wide and shining, a wide gap-toothed smile, lips moving eagerly between words; behind her, soft, the big old tree and the grassy bank in the soft grey-gold dawn mist; {HANDS}",
         lines=[("xiaohe", "一、二、三……好多鴨鴨，數不完了！", "數鴨子")],
         motion="Little Xiaohe bobs her flat right hand along through the air, counting the ducks one by one, as she speaks",
         zh="中近景、慢推（送 `-chen-liu-l1`：大樹與田埂，晨霧）：稿子 c20 的小禾：在田埂上看著畫左外水田裡的鴨子，右手平掌在空中一下一下點著數（不寫單指，拍法 32），數不完、開心地說（**本鏡可以笑**、缺門牙）"),
    dict(loc="ch_e", cam="Insert close-up, slow push in", chars=[], night="chen",
         comp=f"insert close-up at water level, the very first frame is already a close view of one young green rice seedling standing in the still shallow water with {LOCUST} clinging to its leaf, the orange bill and white head of one farm duck right beside it; far beyond, soft and out of focus, only the pale misty water fills the background to every edge; only the seedling, the locust and the duck's head are in the frame",
         motion=NOBODY + "the duck's bill darts forward and snaps the locust off the leaf, and the seedling sways",
         zh="插鏡、慢推（第一格就是鴨嘴與秧上的蝗蟲，拍法 10、35；不寫地點句，送本集免費做的 `set-hantian-yang-chen-shui-l1` 只當水面）：一株青秧上一隻褐色小蝗蟲，旁邊一隻白鴨的橘嘴；鴨嘴一啄把蝗蟲叼走、秧苗晃一下（聖經〈道具〉：近景插鏡是稻秧上的褐色小蝗蟲，**不畫成煙**）。無台詞"),
    dict(loc="ch_t", cam="Wide shot, slow push in", chars=["qianyuanwai"], night="chen",
         comp=f"wide shot at standing eye height along the grassy bank toward the big old tree at the right, like the picture: on the bank under the tree, framed full figure, {QIAN}, his hands clasped behind his back, already stopped at the edge of the bank from the first frame, his face three-quarter to screen left toward the ducks on the water below the bank, never the lens; sneering: a thin cold smile, eyes narrowed, lips moving in a slow drawl between words; one step behind him {RETAINERS}, their lips closed, never the lens; on the shallow water at the left, the long white line of ducks moving across the paddy in the misty dawn light; {HANDS}; exactly three people",
         lines=[("qianyuanwai", "鴨子治蝗？許秀才，你這是要笑死全縣的人。", "冷笑，拖長音")],
         motion=f"Qian Yuanwai gives one scornful sniff and tips his chin up as he speaks; {quiet('The two men behind him', 'their', plural=True)}",
         zh="全景（人眼高、照圖）、慢推（送 `-chen-liu-l1`：大樹、田埂與水田）：錢員外第一格已經背著手沿田埂走到大樹下、停在田埂邊（稿子『從右邊田埂走來』在第一格完成），身後一步兩個錢家家丁（黑短打、黑布包頭、空手；聖經〈小角色〉：家丁只在遠景，所以本鏡用全景，不用稿子的低角度中景）；看著田埂下水裡的鴨子，鼻子一哼、下巴一抬、拖長音地說（**本鏡可以冷笑**；家丁嘴閉著）（→ 答在 s23）。胸前沒有吊牌（錦袍前襟素面，原版必修建議）"),
    dict(loc="ch_t", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "qianyuanwai"], nospeak=["tangxiaotang"], night="chen",
         comp=alone(f"her hands at her sides from the first frame; one step beyond her in the right third of the frame, his whole figure clear of her head and shoulders, {QIAN}, standing on the grassy bank under the big old tree, framed from the waist up, his face three-quarter to screen left toward her, his lips pressed shut, never the lens; his smug look draining away, not smiling; behind them, soft, the trunk of the big old tree and the misty water of the paddy in the soft grey-gold dawn light; she stays in the middle of the frame the whole shot; {HANDS}; {TWO_BACK}",
                    "standing on the grassy bank,"),
         lines=[("tangxiaotang", "員外睜大眼看，鴨子走過的地方，一隻蝗蟲都沒剩。", "下巴一抬")],
         motion=f"her right arm swings out and her flat right hand stretches toward the water at the left where the ducks have passed, only her arm moving; {quiet('Qian Yuanwai')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-chen-liu-l1`）：稿子 c23 是錢員外肩後拍唐小棠正臉的過肩，真人版照拍法 40 反過來：唐小棠背影在正中、頭不動，右手平掌往畫左水田裡鴨子走過的地方一伸（只動手臂）；錢員外在她前方一步的畫右三分之一、大樹下，得意慢慢退掉、嘴閉著（答 s22）。稿子『帳冊夾在腋下』不寫（拍法 38）"),
    dict(loc="ch_t", cam="Medium shot, slow push in", chars=["qianyuanwai"], night="chen",
         comp=f"medium shot on the grassy bank under the big old tree, framed from the waist up: {QIAN}, already turning away to the right from the first frame, his face looking back over his right shoulder toward the paddy beyond the lower left edge of the frame, never the lens; he is the only person in the frame; sour and dark, not smiling: his face fallen, jaw clenched, lips moving through gritted teeth between words; behind him, soft, the trunk of the big old tree and the misty grassy bank in the soft grey-gold dawn light; {HANDS}",
         lines=[("qianyuanwai", "哼，三畝田保住又怎樣，鄰村的人可要餓死了。", "臉一沉")],
         motion="Qian Yuanwai gives his sleeve one sharp shake, walks away toward the right edge of the frame and throws the words back over his shoulder as he goes",
         zh="中景、慢推（送 `-chen-liu-l1`）：錢員外臉一沉、甩一下袖子往畫右走，邊走邊從**右肩**回頭朝畫左下外的水田撂一句（第 33 集獨立審稿必改 3、第 34 集 s32 同一件事：往右走、從靠鏡頭那側的右肩回頭）；**不笑**。稿子『笑容沒了、往後退一步』在第一格完成；『家丁跟著走』不拍（家丁只在遠景，s22 已交代）"),
    dict(loc="ch_b", cam="Medium close-up, slow push in", chars=["aling"], night="chen",
         comp=f"medium close-up of {ALING_DUCK}, standing on the grassy bank, framed from the waist up, the small bamboo whistle already out of her mouth and resting on its cord at her chest from the first frame, {POLE} upright in her right hand, its upper end rising past the top edge of the frame, her face three-quarter to screen left toward the ducks on the water beyond the left edge of the frame, her eyes on them, never the lens; she is the only person in the frame; quiet and light, not smiling until the very end: brows level, lips moving softly between words; behind her, soft, the grassy bank, the trunk of the big old tree and the misty water in the soft grey-gold dawn light; {HANDS}",
         lines=[("aling", "夠了，這片吃乾淨了。往下一片。", "很輕，像在叫人")],
         motion="A-ling tips the long pole out toward the left as she speaks, and at the very end one corner of her mouth lifts a little",
         zh="中近景（腰以上，竿要看得見，拍法 32）、慢推（送本集免費做的 `set-hantian-yang-chen-an-l1`：水邊的田埂與大樹樹幹）：阿令第一格竹哨已經拿下、掛在胸前（稿子『拿下竹哨』在第一格完成），朝畫左外水裡的鴨子很輕地說（像在叫人；原版建議：對鴨群說『往下一片』），長竿往左一擺指下一片（稿子『往右』：鴨群照圖往左推進，下一片在同一個方向）；最後一格嘴角一挑（**全集唯一一下的笑**）；『再把哨子含回去』不拍（一鏡一個動作）。第二場結尾"),
    # ---- scene 3: the village gate, five days after the swarm night, dusk.
    dict(chapter="柳溪村口，五天後傍晚", loc="kk", cam="Wide shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="dusk",
         comp=f"wide shot at standing eye height, like the picture: by the palisade gate at the left, both framed full figure, small, both already arrived along the dirt road from the right from the first frame and seen from behind: {TBACK_SMALL}, her right hand resting on one upright log of the gate, and one step to her left {XU_EVE}, seen from behind, his face toward the fields beyond the gate, his lips pressed shut; far beyond the gate, among the dry brown fields, one small square paddy of young green rice and a short row of white ducks resting on its ridge; {HANDS}; exactly two people, both seen from behind",
         lines=[("tangxiaotang", "五天了，蝗蟲過境，鄰村的田全被啃光了。", "鬆一口氣")],
         motion=f"Xu Yan lifts his flat right hand to shade his eyes against the last light, looking out past the gate, as the willow's long fronds stir in the evening air; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="全景、慢推（人眼高、照圖；送 `set-cunkou-l1`：左邊有小瓦頂的木柵門、中間垂柳、乾溝上的木板橋、土路彎到右邊三間泥磚屋、橘紅天）：**五天後傍晚**（時間跳在 s25→s26：從蝗群那夜算起五天，稿子〈離開這場〉）。許硯與唐小棠第一格已經從右邊村道走到柵門邊、**兩人都是背影**（唐小棠不送圖、只寫雙丸子與桃粉衣，拍法 40；她的話是錄音），唐小棠右手扶著柵門的一根圓木往外看，許硯抬手平掌遮在眉上望出去（一個動作；shot_reading：全景只有看會白買素材）；遠處乾黃的田裡一小塊青田、田埂上一排休息的白鴨（原版必修：只有柳溪那塊是綠的）。圖上**沒有門樓、柵門兩邊沒有籬笆**（見 s31）。稿子『前景是柵門的粗木』照圖：柵門在畫左"),
    dict(loc="kk_g", cam="Close-up, slow push in", chars=["xuyan"], night="dusk",
         comp=f"close-up of {XU_EVE}, standing by the gate, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes on the far green paddy beyond the left edge of the frame, never the lens; he is the only person in the frame; relieved, not smiling: brows easing, lips pressed shut; behind him, soft, only the orange-red evening sky over the far hills and a few long willow fronds at the edge; {HANDS}",
         lines=[("xitong", "叮。蝗災擋下，柳溪的田保住。", "冷，宣布")],
         panel=[("蝗災擋下，柳溪的田保住", "task")],
         motion=f"Xu Yan lets out one long slow breath, his shoulders easing; {SILENT_HE}",
         zh="近景、慢推（送本集免費做的 `set-cunkou-kong-l1`：遠山上的橘紅天、左緣幾縷柳條；稿子『身後只有橘紅的天』）：許硯看著畫左外遠處的青田，慢慢吐一口氣（原版建議：鬆一口氣，不是驚嚇）；系統是錄音、**全程嘴閉著**；面板剪接時疊，**不寫淡藍光**"),
    dict(loc="kk_g", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="dusk",
         comp=alone(f"her left hand already holding his right sleeve from the first frame; {BEYOND_XU}, {XU_EVE}, standing, framed from the waist up, his face three-quarter to screen right toward her, his lips pressed shut, never the lens; quiet, not smiling; beyond them, soft, the palisade gate under its small tiled roof and the willow in the orange-red evening light; she stays in the middle of the frame the whole shot; {HANDS}; {TWO_BACK}",
                    "standing on the dirt road inside the gate,"),
         lines=[("tangxiaotang", "你看柵門外頭，鄰村的人，在朝你拜。", "小聲")],
         motion=f"her left hand tugs once at his sleeve and her flat right hand points toward the gate, only her arms moving, and Xu Yan turns his face toward the gate at the left; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送本集免費做的 `set-cunkou-men-l1`：柵門、交叉的斜撐與橫木、柳樹樹幹、木板橋）：唐小棠背影在正中、頭不動，左手第一格已經拉著許硯的右袖，扯一下、右手平掌往柵門一指（只動手臂），壓低聲音說；許硯在她前方一步的畫左三分之一、嘴閉著，轉頭往畫左的柵門看（稿子『唐小棠在左、許硯在右』：從她背後拍，許硯在她前方偏左，靠柵門那側）"),
    dict(loc="kk_g", cam="Wide shot, point of view, slow push in", chars=[], night="dusk",
         comp=f"point-of-view wide shot past the palisade gate, its upright logs soft and out of focus along the left edge of the frame: beyond it, on the dirt road and the dry ground by the willow, framed full figure, {REFUGEES}; the two in the front row already kneeling from the first frame, their foreheads lowered toward the ground; {TORCHES}; in the right foreground, close to us, {WOMAN_BACK}; {HANDS}; exactly twelve people",
         lines=[("liumin", "許秀才，行行好，給孩子一口吃的吧！", "哭腔")],
         motion=NOBODY + "the people behind press forward a step, the torch flames wavering, and the woman with the child pushes one step closer toward the gate",
         zh="全景（主觀：許硯越過柵門看出去）、慢推（送 `-men-l1`）：柵門的圓木虛焦在左緣；門外土路與柳樹旁的乾地上十個鄰村流民（破舊粗布衣、布包頭、磨破的草鞋、背包袱，每人衣色年紀不同；稿子『約一百人』照拍法 34 寫看得見的十個，一百交給台詞與音效），前排兩個老人第一格已經跪下磕頭；**六支火把，每支拿在一個人手裡**（拍法 37）；右前景一個抱孩子的婦人只拍背影（褪色藍頭巾、灰褐粗布衣，孩子臉埋在她肩上；聖經〈小角色〉：Erinome，放錄音）往柵門擠一步。人數＝十個加婦人與孩子＝十二。布鞋句換成草鞋（mkspec）。稿子『隔著柵欄的木條』：圖上柵門兩邊沒有籬笆，照圖越過柵門的邊（→ 答在 s35；懸念 → 第 36 集第一場）"),
    dict(loc="kk_g", cam="Close-up, slow push in", chars=["xuyan"], night="dusk",
         comp=f"close-up of {XU_EVE}, standing by the gate, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes already on the kneeling people beyond the left edge of the frame from the first frame, never the lens; he is the only person in the frame; moved and heavy, not smiling: eyes wet, brows drawn, lips pressed shut; the wavering orange light of torches on one side of his face; behind him, soft, only the orange-red evening sky over the far hills; {HANDS}",
         lines=[("xitong", "叮。天下歸心，百分之一到百分之二。", "冷，宣布"), ("xuyan", "不只是田保住了……原來人心，也算在裡面。", "心裡話，錄得近、輕", "inner")],
         panel=[("天下歸心，百分之一到百分之二", "task")],
         motion=f"Xu Yan's eyes move slowly from the kneeling people to the woman with the child, and his throat moves once as he swallows; {SILENT_HE}",
         zh="近景、慢推（送 `-kong-l1`）：許硯的眼睛從跪著的人慢慢移到抱孩子的婦人（畫左外，不寫人），喉嚨動一下；半邊臉上是火把的橘光；系統與心裡話都是錄音、**全程嘴閉著**（原版建議：不對著村民大笑）；面板『天下歸心，百分之一到百分之二』跟系統念的一字不差（← 因為 s29）。**不寫淡藍光**。長鏡"),
    dict(loc="kk_g", cam="Low-angle medium shot, slow push in", chars=["qianyuanwai"], night="dusk",
         comp=f"low-angle medium shot of {QIAN}, seen from below, framed from the waist up, already standing up on a low earthen mound beside the palisade gate from the first frame, high against the sky, his face three-quarter to screen right, looking down toward someone out of sight beyond the lower right edge of the frame, never the lens; that side of the frame is only {SIDE_SKY} all the way to the edge, and he is the only person in the frame; furious and loud, not smiling: eyes bulging, brows knotted, his mouth wide, lips moving hard between shouted words; behind him, soft, the small tiled roof of the gate against the orange-red evening sky; {HANDS}",
         lines=[("qianyuanwai", "關門！糧不夠！誰敢開門，全村一起餓！", "大喊")],
         motion="Qian Yuanwai chops his flat right hand down through the air and thrusts it toward the gate's crossbar as he shouts",
         zh="低角度中景、慢推（送本集免費做的 `set-cunkou-ding-l1`：柵門的小瓦頂與橘紅天）：**圖上沒有門樓**：照稿子〈五張清單〉2 的備案，錢員外站在**柵門旁的土台上**（台詞不變），低角度、映在天上，朝畫右下外看不到的人（守門的村民，不點名）大喊、右手平掌往下一劈再指向門閂（稿子『一拍欄杆』：圖上沒有欄杆）。稿子『身後兩個家丁』不寫（家丁只在遠景、側背，拍法 34）；**不笑**。聖經〈接點〉35→36 寫的門樓照圖改（PREP.md）"),
    dict(loc="kk_g", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="dusk",
         comp=alone(f"her left hand already gripping his right sleeve from the first frame; {BEYOND_XU}, {XU_EVE}, standing, framed from the waist up, his face three-quarter to screen left toward the gate, his lips pressed shut, never the lens; grave, not smiling; beyond them, soft, at the palisade gate, {GUARDS}, standing one at each end of its thick crossbar, side-on to us, their faces turned toward Xu Yan, their lips closed, never the lens; the orange light of torches wavering beyond the gate; she stays in the middle of the frame the whole shot; {HANDS}; exactly four people, the young woman in the middle seen only from behind",
                    "standing on the dirt road inside the gate,"),
         lines=[("tangxiaotang", "上百張嘴……許硯，你先別急著答應。", "小聲，不笑")],
         motion=f"her left hand grips the sleeve tighter and gives it one small shake, only her arm moving; {quiet('Xu Yan and the two men', 'their', plural=True)}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-men-l1`）：唐小棠背影在正中、頭不動，左手第一格已經抓著許硯的袖子不放，再抓緊、晃一下（只動手臂；稿子『臉發白』『看看門外又看看他』從背後看不到，交給語氣）；許硯在畫左三分之一朝柵門、嘴閉著；柵門邊兩個守門的村民（暗青、深酒紅）站在門閂兩頭、側身回頭看許硯、嘴閉著（三張臉：許硯與兩個不具名的村民，拍法 1）。「糧只夠撐兩個月」留給第 36 集（稿子）"),
    dict(loc="kk_g", cam="Medium shot over the shoulder, slow push in", chars=["aling"], night="dusk",
         comp=f"medium shot over a shoulder: {BACK_XU}; beyond it, at the right, {ALING_DUCK}, her hands empty at her sides, standing on the dirt road, framed from the waist up, already stopped half a step behind the man in the foreground from the first frame, her face three-quarter to screen left toward his back, her eyes on it, never the lens; quiet and steady, not smiling: brows level, lips moving softly between words; behind her, soft, the dirt road curving away to the three small houses in the orange-red evening light; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("aling", "開不開門，你定。我們都聽你的。", "很輕")],
         motion="A-ling gives one small nod as she speaks, her eyes staying on his back",
         zh="過肩中景、慢推（送本集免費做的 `set-cunkou-dao-l1`：土路與右邊三間泥磚屋）：前景左是虛焦的藍灰肩背與髮髻（不點名、不送圖，拍法 2）；阿令第一格已經從右邊村道走到他身後半步停下（稿子的跟拍改慢推），樣子跟第二場一樣：袖口布條紮緊、綁腿、竹哨掛在脖子上、空手（稿子 2026-11-06 審稿後的修改；接第 36 集 c01），看著他的背、輕輕點一下頭說；**不笑**"),
    dict(loc="kk_g", cam="Wide shot from behind, slow push in", chars=["xuyan", "aling"], night="dusk", act=3,
         comp=f"wide shot from behind at standing eye height toward the palisade gate, like the picture: in the middle {XU_EVE}, framed full figure, seen from behind, already walking toward the gate's thick crossbar from the first frame; one step behind him on his right {TBACK_SMALL}, her hands empty; half a step behind him {ALING_DUCK}, seen from behind; at the gate, {GUARDS}, already stepping aside one to each end of the crossbar, side-on to us, their lips closed, never the lens; beyond the gate's logs the orange light of torches wavering; {HANDS}; exactly five people",
         motion=f"Xu Yan walks step by step up to the crossbar and stops before it, the two women following behind him; {quiet('Xu Yan and A-ling', 'their', plural=True)}; {HEADSTILL}",
         zh="全景（從背後）、慢推（送 `-men-l1`；稿子的跟拍往左改慢推）：許硯從人群裡一步一步走到門閂前停下；唐小棠鬆開袖子跟在他右後（背影，不送圖），阿令在他身後半步（背影）；兩個守門的村民第一格已經往門閂兩頭讓開、側身；柵門的圓木外火把的橘光一閃一閃（稿子 2026-11-06 審稿後的修改：接第 36 集 c01 的站位）。剪接照稿子剪在伸手的一半。無台詞"),
    dict(loc="kk_e", cam="Insert close-up, slow push in", chars=[], night="dusk",
         comp="insert close-up, the very first frame is already a close view of a man's right hand in a faded blue-grey cotton sleeve resting flat on the thick horizontal wooden crossbar of the palisade gate, the rough upright logs behind it; through the narrow gaps between the logs, soft and out of focus, the wavering orange light of torches; only the hand, the sleeve and the wood of the gate are in the frame",
         lines=[("xuyan", "開了，糧不夠分；不開，門外是人命。", "心裡話，錄得近、輕", "inner")],
         motion=NOBODY + "the fingers close one by one round the crossbar and grip it, and the hand stays still there, the bar not moving",
         zh="插鏡、慢推（第一格就是門閂特寫，拍法 10、35；不寫地點句，送本集免費做的 `set-cunkou-zha-l1`：柵門的圓木與粗橫木，只當木頭與光）：許硯的右手（藍灰書生袍袖口，不點名）按在粗木門閂上，手指一根一根收緊、停住，**沒有拉**；柵欄縫裡透進火把的橘光；心裡話是錄音，嘴不入鏡（本集結尾；懸念 → 第 36 集第一場：許硯兩手抬起門閂）。剪接照稿子從手按上門閂開始"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e035-r2/script.md`（c01–c35 對應 s01–s35，加五個拆鏡 s02b、s11b、s12b、s17b、s20b，共 40 鏡；含「這版改了什麼」「2026-11-06 審稿後的修改」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e031-e040.md`（拍法 1–43 條、〈場景〉〈接點〉〈道具〉〈小角色〉），帳照 `r2-bible-e011-e060.md`。**第 4 篇章〈旱年〉第五集**。",
    "- 內部工作編號 935（`hailuo/{ff,clips}-dh-e935.json`；`colab/runs/e935/extras.json`、`colab/runs/e935-live/spec.json`、工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e935-dh/`）；發布 slug `zhong-tian-qu-qi-e035-r2`。不放集數、不放片名卡；**s01 接第 34 集成片 `e934-live.mp4` 的最後一鏡**（s40 日落轉灰的田邊、三個背影望著遠山上的蝗群）：同一夜、許家屋內——**第 34 集還會再修，定版後再核一次 s01**；s35 交給第 36 集（同一刻：許硯兩手抬起門閂）。",
    "- 照第 33、34 集審稿的通則一開始就照做：參考圖跟文字一致（每張圖都照圖寫站位；本集的新圖都是免費裁切與調色、新 id）；長東西第一格不相連（阿令的竹竿）；不寫 crowd、hundreds、villagers，寫實際人數（流民十二人、鴨子寫成白線與五到八隻）；沒有人看得到腳的鏡不加布鞋句、流民寫草鞋；不寫泥；`OFFSCREEN_SPEECH = False`、對畫外的人說話寫「朝畫左／右外看不到的人」；不寫 open、不寫否定名詞；extras 的「air is clear and still」逐鏡換掉（mkspec）。",
    "- **人物**：**唐小棠**（拍法 3、4、40）：說話的九鏡（s03、s09、s11b、s12b、s14、s23、s26、s28、s32）一律從背後拍（畫面正中、正背對、頭不動、剛好兩顆丸子；l1 交領短襦，**不寫 t2 高立領、不寫淡杏外衣**），s07（算盤插鏡）與 s17b（鴨子）她的話是畫外錄音；過肩前景的雙丸子後腦（s04、s08、s18）與全景小背影（s34）不點名、不送圖；**本集唯一一鏡正臉是 s11**（好感 +3 的反應、不說話、嘴閉著、最後嘴角小小揚起），下一鏡 s11b 是中景背影（不同景別）。木算盤（拍法 20）在 s03、s07–s11b；帳冊不寫。**阿令**送 `aling-portrait-l1`（沒戴鐵鐐：稿子要先畫的 `aling-portrait-t2` 就是它，**不用另畫**），不戴面巾、木簪；s16 起袖口灰布條紮緊、綁腿、竹哨掛在脖子上、一根約兩人高的竹竿（s33、s34 空手）。**許硯**夜裡披舊灰外衣（s01–s11b）；第二場袖子捲起，s13 起髮髻撞歪（**不寫泥**）；第三場乾淨的同一件袍子、空手。**小禾**八歲、草兔子塞在腰帶（s05 桌下、s13 畫外、s20b）。**錢員外** s22–s24、s31，胸前沒有吊牌，家丁兩人只在 s22 全景。**流民婦人**只拍背影（s29，Erinome，`MINOR`）。秦霜、二牛本集不入鏡（稿子）。",
    "- **軸線（照圖）**：屋內照 `set-xujia-wu-ye-l1`（拍法 42）：窗在後牆**左**、小方桌在中間偏右、門在畫外右；許硯坐桌**左側**朝畫右，唐小棠從右邊進來站桌右側，小禾在桌下。田照 `set-hantian-yang-l1`：水田在前、田埂後是乾裂的地、左邊小屋遠山、**右邊大樹下一道長草的高田埂**——稿子『田埂在左、白線由左往右』照圖反過來：人、竹籠、鴨子從右邊田埂出發，白線往**左**推進水田；錢員外在同一道田埂的大樹下。村口照 `set-cunkou-l1`：柵門在**左**（小瓦頂、交叉斜撐、一根粗橫木＝門閂）、中間垂柳與木板橋、土路彎到右邊三間泥磚屋；**圖上沒有門樓、沒有籬笆**：錢員外照稿子的備案站在柵門旁的土台上（s31）；村裡是鏡頭這側與右邊村道，流民在柵門外左邊（聖經〈接點〉35→36：柵門左、村道右）。",
    "- **時間與光**：第一場夜、只有桌上一朵火（拍法 8；稿子的油燈照圖寫成『桌上那一朵火』、不寫蠟燭）；第二場兩天後下午，蝗群壓在天上的棕色半明半暗（本集免費做的 `-yang-zong`）→ 同日傍晚橘光（`-yang-xi`，s19）→ 隔天清晨灰金光、水上薄霧（`-yang-chen`，s20–s25）；第三場五天後傍晚橘紅天（`set-cunkou-l1` 本來的光）加流民手上的火把。時間跳都在剪點（s11b→s12、s18→s19、s19→s20、s25→s26），不在鏡頭裡變光。",
    "- **原版必修**（聖經第 35 集）：四周旱地變成整片春天水田、背景開花的果樹 → 田的場景句寫『只有這一塊水田是綠的，田埂後面的地乾裂光禿』（`set-hantian-yang-l1` 只有田埂前那塊灌水插秧；不寫 blossom 的否定句）。原版建議：s27 鬆一口氣不是驚嚇；s30 心裡話嘴閉著不對村民笑；s14 整句不笑（從背後）；s13 鴨子真的站在跌坐的許硯頭上；錢員外胸前沒有吊牌；s05 小禾中景、臉在畫面上；s25 對鴨群說『往下一片』、鴨群在田裡。",
    "- 要買的秒數（BUY，錄音前照第 34 集的估法與實測：一句 6 秒的鏡放得下約 5.9 秒人聲、8 秒約 7.3 秒；第 34 集量到許硯約 3.5–4 字／秒、小禾 3.3–3.6、阿令慢；唐小棠（Laomedeia）本篇第一次大量用，照稿子『快、精明』估 4 字／秒，c09 慢下來）：s30 買 10 秒（系統 14 字加心裡話 15 字）；s01、s07、s09、s12b、s22、s23、s24、s29、s35 買 8 秒（系統兩句；18 字以上；慢、哭腔；結尾的鉤子）；s12、s17、s19、s21 買 5 秒（沒有台詞的鏡、插鏡）；其餘 6 秒（說話的鏡、畫外的話蓋在上面的鏡、兩拍的動作：s20 白線推進、s34 走到門閂前）。**錄音後照 `span935.sh` 量人聲長度重核**（PREP.md §4）。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音的人聲長度為準。",
    "- **田（s12–s25）表上的提示詞帶「below the deep pool」**：只為了讓 `gen-dh` 的 `SET` 選到深潭那張圖（再由 `spec.json` 換成田的圖），d1 由 `mkspec.py` 拿掉（`R2.POOLMARK`→空）；**之後每個 fix／retake spec 都要帶同一組替換**，不然模型會在田裡畫出潭（第 34 集獨立審稿建議 6）。屋內的提示詞帶「Inside the farmhouse」讓 `SET` 選到 `set-xujia-wu`（白天那張），`spec.json` 一律換成夜版與它的裁切。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯 l1、angle-a（帶笑的 angle-b 整集不送；全景背影 s26、s34 只送 l1）；唐小棠只有 s11 送 l1 與 angle-a（angle-b 不送），其他有她的鏡她的三張圖都拿掉；阿令 l1、angle-a（angle-b 不送；全景只送 l1）；錢員外 l1、angle-a（angle-b 不送；全景 s22 只送 l1）；小禾只送 l1（`retake.py` 只能換或拿掉圖、不能加圖）。過肩前景的背影（s04、s08、s18 雙丸子；s33 許硯）、s34 唐小棠的小背影、s07 的兩隻手、s35 的手、四個開籠的村民、拿竹竿的村民、守門的兩人、流民與抱孩子的婦人、家丁都不送圖、不點名。",
    "- **場景圖**：屋內送 e922 的 `set-xujia-wu-ye-table-l1`（s01、s03、s04、s08、s09、s11b）與本集免費做的裁切 `set-xujia-wu-ye-chuang-l1`（s02、s02b、s06、s10）、`-qiang-l1`（s11）、`-zhuo-l1`（s07 插鏡，只當桌面）、`-di-l1`（s05）；田送本集免費做的 `set-hantian-yang-zong-l1`（s12）與 `-zong-liu-l1`（s12b、s16）、`-zong-an-l1`（s13、s17）、`-zong-tian-l1`（s14）、`-zong-geng-l1`（s15、s18）、`-zong-shui-l1`（s17b），`-yang-xi-l1`（s19），`-yang-chen-l1`（s20）與 `-chen-liu-l1`（s20b、s22、s23、s24）、`-chen-shui-l1`（s21 插鏡，只當水面）、`-chen-an-l1`（s25）；村口送 `set-cunkou-l1`（s26）與本集免費做的 `set-cunkou-kong-l1`（s27、s30）、`-men-l1`（s28、s29、s32、s34）、`-ding-l1`（s31）、`-dao-l1`（s33）、`-zha-l1`（s35 插鏡，只當木頭與光）。`set-xujia-wu-l1`（白天）、`set-xujia-wu-ye-l1` 整張、`set-hantian-yang-l1` 本身（地平線三根小竿沒塗）、`set-shentan-*` 不送。",
    "- **本集新做的圖**（2026-11-20，`live-action/free-e031-e040/`，各跑兩次逐位元一樣，寫進 refs-live README）：`xujia_wu_ye_crops.sh`（夜裡屋內四張裁切）、`hantian_yang.sh`（先用 `hantian_yang_clean.py` 塗掉 `set-hantian-yang-l1` 遠處三根小竿——跟第 34 集 `set-hantian-l1` 同三根、位置偏幾個像素——再調三種光：棕色半明半暗 `-zong`、傍晚橘 `-xi`、清晨灰金加薄霧 `-chen`，與它們的裁切）、`cunkou_crops.sh`（村口五張裁切）。**不花錢**；沒有付費圖。稿子要畫的 `aling-portrait-t2` 由 refs-live 的 `aling-portrait-l1`（沒戴鐵鐐）取代。",
    "- **還缺、先用最接近的圖**（不花錢、註明在這裡）：(1) **門樓**：`set-cunkou-l1` 沒有門樓、柵門兩邊沒有籬笆：錢員外站在柵門旁的土台上（稿子的備案）；流民在柵門外的土路上，柵門擋不住人的問題交給剪接與台詞（第 36 集也用這張圖）。(2) **竹籠、鴨子、竹竿、竹哨、算盤、火把**是文字加在圖上。(3) **田的季節**：`set-hantian-yang-l1` 的大樹與遠處的樹是金黃與紅的秋葉（第 34 集同一張母圖；聖經〈時間線〉〈場景〉已照實寫），文字只寫「the big old tree」；稿子『背景樹是新綠葉』做不到，不寫葉色。(4) **屋內**是 e922 的圖，偏 CG（README 記過），右上屋頂破洞在 `-table` 裁掉了。(5) **鴨群**三千隻只寫白線；兩支都畫成一團白霧或白布就 fix 加「each duck clearly a separate white bird」。付費改圖的建議見 `colab/runs/e935-live/PREP.md`〈還缺〉（都不擋 d1）。",
    "- 共用檔：沒有改（`build-r2.py` 的 `EN` 已有每個在畫面上說話的名字；流民婦人不在 `chars`，台詞是錄音，不需要 `EN`，她的聲音在本檔 `MINOR`）；`gen-dh.mjs`、`pilot.py`、`cast.json` 不動。對畫外說話、對窗、鴨子、竹竿、田說話的鏡，精修文字的通用說話視線由本檔結尾的 `live_clips()` 換成 d1 的方向句（`GAZE_REFINE`）；唐小棠的背影鏡：立領句拿掉、名字換成「從背後看的年輕女子」（同第 31、33 集），正臉 s11 只拿掉立領句。",
    "- **自審**（2026-11-20，`writer-tools/e035-r2/review.md`，不是獨立審稿）；給獨立審查者的提示在 scratchpad `e935prep/review-prompt.md`，由協調者派。",
    "- **d1 前置**（2026-11-20，`colab/runs/e935-live/PREP.md`）：`colab/runs/e935/extras.json`、`colab/runs/e935-live/{mkspec.py,spec.json}`（種子 9351101／9351102）、scratchpad `tools/prep935.sh`、`tools/rec935.sh`（錄音）、`e935d1.sh`（Colab session `zt-live3`，**沒跑**）。",
    "- 配樂：第一場低沉緊張的 drone 底下一直有蝗蟲撲窗的沙沙聲，s10「押」之後轉溫柔，s11「叮」一個輕的重音；第二場亂糟糟的喜劇曲（鴨子亂跑），s16 阿令出場時停，s20 白線湧進田時起一段寬闊的旋律，s22 錢員外一句底下一聲低音；第三場溫暖寬闊的旋律，s31 錢員外一喊全部收掉、換低沉的 strings，s35 停在最高點不收。音效見 script.md〈音樂與音效〉。",
]

# Seconds to buy. Estimated as e934 (before its recordings; e934's recheck changed nothing): a 6 s shot holds about 5.9 s of
# speech, 8 s about 7.3 s; e934's lines ran Xu Yan 3.5-4 characters a second, little Xiaohe 3.3-3.6, A-ling slow (as Elder
# Han); Tang Xiaotang (Laomedeia) estimated at 4 (quick), slower in c09.
# 10 s: s30 (system 14 + thought 15 with a pause).
# 8 s: s01 (two system lines, 20), s07 (Tang 18, muffled, the beads), s09 (Tang 16, slow and small), s12b (Tang 21), s22
#      (Qian Yuanwai 17, drawled), s23 (Tang 20), s24 (Qian Yuanwai 18 walking off), s29 (the refugee woman 14, weeping, an unmeasured
#      voice), s35 (the thought 14, the hook's held tail).
# 5 s: s12 (the cages), s17 (the whistle), s19 (the flock turning), s21 (the insert).
# 6 s: every other shot (gen-dh's default for a line spoken on screen; written out where the line is a recording over the
#      shot -- s02, s11, s13, s17b, s27 -- or the motion has two beats -- s20, s34 -- so gen-dh's 5 s default never applies).
BUY = {"s30": 10,
       "s01": 8, "s07": 8, "s09": 8, "s12b": 8, "s22": 8, "s23": 8, "s24": 8, "s29": 8, "s35": 8,
       "s12": 5, "s17": 5, "s19": 5, "s21": 5,
       "s02": 6, "s11": 6, "s13": 6, "s17b": 6, "s20": 6, "s27": 6, "s34": 6}


# ---- the refine text (as e031, e033): hailuo/clips-dh-e935.json column 0 is the motion text refine-prep.py sends with a picked
# d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era "Tang Xiaotang's high stand-up collar stays
# closed at her throat." and names her in "<names> shown in <Picture 1>"; in a back shot that draws the collar back and turns
# her face to the lens. Her back shots: the sentence goes and her name becomes "the young woman seen only from behind", with
# someone else: "keep the same face, hair, costume and props as the first frame, the young woman's back to us"; alone: "keeps
# the same hair, costume and props as the first frame, her back to us" (e031). FRONT_TANG (s11, her one front face) keeps her
# name and only loses the collar sentence. Column 1 is recomputed. prep935.sh hands stage 1 the anchor form (anchor_form(),
# e028 review 必改 1; rule 39).
COLLAR = "Tang Xiaotang's high stand-up collar stays closed at her throat. "
FRONT_TANG = {"s11"}
# rule 31 (e030 review 建議 10): gen-dh's speaking gaze names "the person he/she is speaking to", who is not in the frame of these
# shots (or is a thing: the window, the ducks, the pole); the refine text gets d1's direction. anchor_form() puts gen-dh's words
# back for stage 1.
GAZE_GEN = {"he": "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person",
            "she": "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"}
_R = "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"
_DUCKS_SHE = "her face three-quarter to screen left toward the ducks on the water beyond the left edge of the frame, her eyes on them"
# sid -> (pronoun, the direction sentence)
GAZE_REFINE = {
    "s02b": ("he", "his face three-quarter to screen right, his eyes on the empty air before him"),
    "s05": ("she", "her face three-quarter to screen left toward the small window beyond the left edge of the frame, her eyes on it"),
    "s06": ("he", "his face turned three-quarter to screen right over his shoulder toward someone out of sight beyond the right edge of the frame, his eyes on that spot"),
    "s10": ("he", _R),
    "s15": ("he", "his face three-quarter to screen left toward the white ducks scattering across the water, his eyes on them"),
    "s16": ("she", "her face three-quarter to screen right toward the long bamboo pole, her eyes on it"),
    "s20b": ("she", "her face three-quarter to screen left toward the white ducks on the water beyond the left edge of the frame, her eyes on them"),
    "s22": ("he", "his face three-quarter to screen left toward the ducks on the water below the bank, his eyes on them"),
    "s24": ("he", "his face looking back over his right shoulder toward the paddy beyond the lower left edge of the frame, his eyes on it"),
    "s25": ("she", _DUCKS_SHE),
    "s31": ("he", "his face three-quarter to screen right, looking down toward someone out of sight beyond the lower right edge of the frame, his eyes on that spot"),
}
BACK_NAME = "the young woman seen only from behind"


def live_clips(path):
    import hashlib
    import json
    import re
    clips = json.load(open(path, encoding="utf-8"))
    for key, row in clips.items():
        text = row[0]
        sid = key.split("-", 1)[1]
        if COLLAR in text:
            text = text.replace(COLLAR, "")
            if sid not in FRONT_TANG:
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
        if sid in GAZE_REFINE:
            pr, gaze = GAZE_REFINE[sid]
            assert text.count(GAZE_GEN[pr]) >= 1, (key, "speaking gaze")
            text = text.replace(GAZE_GEN[pr], gaze, 1)
        assert "stand-up collar" not in text, key
        row[0] = text
        row[1] = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    open(path, "w", encoding="utf-8").write(json.dumps(clips, ensure_ascii=False, separators=(",", ":")))


# e928 review 必改 1 (rule 39): ref2manifest.mjs (stage 1) strips gen-dh's refine anchor with ANCHOR_FF, and the back-shot wording
# live_clips() writes no longer matches it. prep935.sh hands stage 1 the anchor form of the live file (this), then puts the
# live file back; the refine text (clips-dh) keeps live_clips()'s wording.
def anchor_form(text):
    text = text.replace(", the young woman's back to us; the set layout stays as it is.", "; the set layout stays as it is.")
    text = text.replace("keeps the same hair, costume and props as the first frame, her back to us; the set layout stays as it is.",
                        "keeps the same face, hair, costume and props as the first frame; the set layout stays as it is.")
    assert "back to us; the set layout" not in text
    for pr, g in sorted(set(GAZE_REFINE.values()), key=lambda x: len(x[1]), reverse=True):
        text = text.replace(g, GAZE_GEN[pr])
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
