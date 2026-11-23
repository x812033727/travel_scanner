"""Episode 37 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e037-r2/script.md
(c01-c40; the CG-era r2 script), including its sections 「這版改了什麼」 and 「2026-11-06 審稿後的修改」, which override the tables.
Every line is the script's, word for word; only the staging changes. 42 shots: one per script shot (sNN = cNN) plus two splits
that keep one visible action and one voice per shot (s09b: c09's exit, Xu Yan and the men with hoes striding out through the
yard gate after the lamp is handed over, the script's 2026-11-06 addition; s16b: Xu Yan's thought after the system line of c16,
about 9.5 s of speech with the pause, past what a 10 s clip holds with room to cut).
Bible: production/r2-bible-e031-e040.md (arc 4 〈旱年〉: rules 1-43, 〈場景〉, 〈接點〉 36->37 (written 2026-11-20 and checked
against e936's cut 2026-11-23), the props (Xu Yan's clay oil lamp, the lime sacks and the shallow pits, Qin Shuang's spear,
Diao Qi's saber, the bucket of hot water, A-ling's sheathed short knife (rule 22), Xiaohe's straw rabbit; Qin Shuang's chopper
NOT written, rule 5), people (Diao Qi's first episode: ragged tunic, no armour, the old scar), 〈小角色〉 (the raiders: backs,
silhouettes and far shapes; the fighters and the women and children) and 原版必修 (e037: Xu Yan never grins at 「小禾？小禾！」))
and r2-bible-e011-e060.md (accounts: Qin Shuang +7 -> 48; Tang Xiaotang 45, A-ling 32; the guard-the-village task set and done).
The seventh episode of arc 4: the same third watch as e036's last shot (day 175) in the Xu yard, the head of the new channel from
the fourth watch to just before dawn, the back gate at the same hour, and the channel at the first grey of dawn.

Written from the start the way e036-r2/r2.py stands AFTER its independent review, its cut and its final check
(writer-tools/e036-r2/{review.md,review-independent.md}; colab/runs/e936-live/PREP.md §1-§8; e935-live/PREP.md §8), the task
file's lessons and the owner's rules of 2026-11-21 to 23 (PR #2217, production/OWNER-CHECK-20261122.md):
- 36->37 from e936's cut (scratchpad e937prep/tail/sheet*.jpg): the yard gate in the picture already stands half swung back
  (its plank leaf against the left post) and is written so in every shot that shows it; e936 s36 / s38 show a FULL moon, so no
  picture here shows a crescent (the paid night channel's crescent is painted out: shanjiao_qu_ye_clean.py; the back gate
  picture has a full moon); the refugees' straw mats lie in the middle of the yard between the bare tree and the well (e936 s31,
  as cut), not along the back wall.
- The pictures agree with the words: every place sentence follows the picture it sends; every crop is a free id made for this
  episode (live-action/free-e031-e040/{shanjiao_qu_ye_e937.sh,xujia_houmen_e937.sh,xujia_yuan_ye_e937.sh}) or e036's crops of
  the same yard. The night channel is the cleaned -ye2 (no guard rail, no flat upright board, no skyline bumps: the e936 reviews'
  -jing2 cleaning done again on the paid night picture), not -ye.
- No "cinema camera" (e935 §8); no stubble word for Xu Yan; no mud (the script's lime on his robe is pale white powder); no
  negated nouns (rule 18; the spear is "the shaft bare below the head", not "no tassel"); long things never touch in the first
  frame (the hoes, the bamboo poles, the spear and the saber); doors written shut or swung back every time (the yard gate swung
  back, the back gate's plank door standing ajar inward, as both pictures show).
- One more person than written is common: every frame says "exactly N people" in the composition and mkspec.py writes the
  'only' sentence again at the end of the prompt (task file 2026-11-20).
- No collective noun (rule 34): the four hundred raiders are a long thin line of small far flames (rule 37), six dark running
  shapes, eight in the alley; the sixty fighters are three to nine named-by-colour men; the forty women and children are two
  women behind Xiaohe. "exactly N people" everywhere.
- OFFSCREEN_SPEECH = False (rule 15); rule 31: a line to someone out of frame is written "toward someone out of sight beyond the
  left/right edge of the frame", that side set only, the speaker the only person; a look at a thing names the thing (the field,
  the far hills, the alley). GAZE_REFINE puts the same direction into the refine text.
- No blue light (rule 11): the panels of s03, s37, s38 are the editor's.
- Tang Xiaotang (rules 3, 4, 20, 40): every line of hers is said from behind (s32, s34, s35) or over an insert of her hands (s08);
  her silent backs (s07, s09) are unlisted; l1 cross-collared jacket, no outer coat, no stand-up collar (the script's 淡杏外衣
  and t2 go). She has NO front face this episode. Owner 2026-11-22 (PR #2217): every back shot of hers also sends the hair
  reference refs-live/tangxiaotang-back-shuangji-e929-w3.png (two round buns from behind; mkspec.py adds it), so she grows no
  single bun and no long loose hair down her back.
- Kneeling is framed to the knees (owner 2026-11-22): Diao Qi's surrender (s28) and Xu Yan on one knee catching Xiaohe (s39) are
  framed full figure; s40 is a crouch, not a kneel.
- Qin Shuang (rule 5): her chopper is never written (the script's c05 「手按柴刀柄」 and c13 「解下柴刀塞給壯丁」 go; the owner's
  2026-11-21 note that the old chopper sentence draws a sword does not arise). From s26 on she holds one spear (bible 〈道具〉),
  sent with its prop picture prop-changqiang-l1 where it is in her hand (mkspec.py).
- A-ling (rule 22): her short knife never leaves its sheath ("one short knife sheathed in plain dark wood, grip and sheath one
  closed piece of dark wood as long as her hand", in her right hand); she strikes the raider's wrist with the end of the sheath.
- The raiders (bible 〈小角色〉, rule 5): plain wooden sticks; one blade only, Diao Qi's; one spear only (the raider's in s26, then
  Qin Shuang's). Wang Erniu reports, shouts and binds: never smiling (written feature by feature every shot).
- Xu Yan does not grin at 「小禾？小禾！」 (原版必修): brows knotted hard, eyes wide, mouth open.

THE AXES (rules 29, 42: the pictures decide):
- The yard by night (set-xujia-yuan-ye-dong2-l1, e931's; e936's crops): the house and its dark doorway at the LEFT with the
  woodpile against its front, the yard gate in the MIDDLE of the back wall (its plank leaf swung back against the left post), the
  bare tree right of the gate, the low back wall running RIGHT, the round well in the front RIGHT; the straw mats between the
  tree and the well (e936 as cut). Wang Erniu runs in through the gate toward us; Qin Shuang drops down from the right stretch of
  the back wall beside the well; Xu Yan stands in the middle with the lamp, Tang Xiaotang at his right (e936 s38). The script's
  「院門在右、東牆在左、井在左前」 is turned the picture's way.
- The head of the new channel by night (set-shanjiao-qu-ye2-l1, the cleaned paid night picture): the dry channel runs from the
  foreground AWAY into the distance; on its LEFT bank the long low ridge of dug earth with the heap of dry straw on it (the
  script's 土埂 and 草堆), beyond the ridge the flat dry field running to the line of dark pines at the far LEFT (the foot of the
  hills: the raiders come out of the pines across the field); the plank across the channel on a thin post in the middle distance
  (the script's 閘板 in the lines; no flat board is written, it grows writing); the right bank and the dark paddy (the village
  side). The defenders hold the ridge facing LEFT across the field: the shallow pits are dug in the field just before the ridge,
  the lime sacks lie along the ridge; the front row crouches on the ridge (Qin Shuang at the left, Xu Yan at her right), the
  second row stands behind it, the third row behind them. The script's axis (raiders from the left, defenders at the right
  facing left) holds.
- The back gate by night (set-xujia-houmen-ye-l1): the long low stone wall from the far left into the frame, the narrow plank
  door at the RIGHT standing ajar inward with warm light inside, split logs against the wall left of it, the dark alley running
  away to the LEFT, a full moon. A-ling and Tang Xiaotang hold the doorway facing LEFT down the alley; the raiders come up the
  alley from the left.
- The channel at dawn (set-shanjiao-qu-chen-l1: the cleaned night picture lifted to grey-blue with a pale band low over the
  pines): the same layout.

PLACES (gen-dh SET takes the FIRST pattern in its list order that matches the prompt):
- The yard and the back gate: every LOC holds "night yard of the Xu farmhouse" -> dh-set-xujia-yuan-ye-t1 = pilot.py's newest
  set-xujia-yuan-ye (l2, never sent), which spec.json swaps for e931's set-xujia-yuan-ye-dong2-l1 and its crops (-zhong, -shu,
  -qiang, -chai, -wu, -di) and for the back gate set-xujia-houmen-ye-l1 and its crops (-men, -xiang). The back gate's LOC reads
  "the back gate in the wall of the night yard of the Xu farmhouse": gen-dh's own back-gate pattern would send set-houmen,
  which has no live picture (pilot.py would stop).
- The channel: the LOC carries " below the deep pool" (POOLMARK) only so gen-dh sends set-shentan ("new channel" would take
  set-xinqu: no live picture), swapped for set-shanjiao-qu-ye2-l1 / -chen-l1 and their crops; mkspec.py takes the words out of
  every d1 prompt (e934-e936's way). Every later fix of s10-s28 and s35-s40 must carry the same replacement.
Shared files: build-r2.py's EN gains "diaoqi": "Diao Qi" (he speaks on screen for the first time; a new key only, every older
episode rebuilds byte for byte). gen-dh.mjs, pilot.py, cast.json untouched. The d1 prep (colab/runs/e937/extras.json,
colab/runs/e937-live/{mkspec.py,spec.json,PREP.md}, the scratchpad's tools/prep937.sh, rec937-slow.sh and e937d1.sh) was
written 2026-11-23.
"""
EP = 937  # internal working number; the published slug is zhong-tian-qu-qi-e037-r2
SLUG = "zhong-tian-qu-qi-e037-r2"
EP_TITLE = "石灰陣，四百流寇過不了一道土埂（重製版 r2）"
OUTLINE_SECONDS = 199.5  # script.md: about 199.5 s, 40 shots (9 + 19 + 12)
TARGET_MINUTES = [3, 4]
TITLE = "四百人下山！石灰陣一聲「扔」，秦霜奪槍挑飛刁七的刀｜種田娶妻打天下 第37集（重製版）"
DESCRIPTION = "三更，二牛撞進院子：山上下來四百人，村裡肯拿鋤頭的才六十個。系統下了守村任務：婦孺一個不能少。許硯不守村口，守渠頭那道土埂：糖坊剩的石灰三步埋一袋，坑挖到膝蓋、鋪上乾草，絆一跤就夠。秦霜說陣她來排，許硯說他照著打，一個字都不改——而且不退。天快亮，刁七帶著火把衝下山，秦霜一聲「扔」，白煙吞掉火把；她從流寇手上奪下一桿長槍，一挑把刁七的刀挑飛。後門，唐小棠一桶滾水潑出去，阿令放倒一個。婦孺一個不少，可撲進許硯懷裡的小禾，臉燙得嚇人。《種田娶妻打天下》第 37 集（重製版）。"
THUMB = ("石灰陣", "s21")
CHARACTERS = ["xuyan", "tangxiaotang", "aling", "qinshuang", "erniu", "xiaohe", "diaoqi", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: tense low drums in a dark moonlit farmyard, one hard accent on a task announced; then low steady drums coming closer over a dry channel at night, everything cut to breath on a whispered wait, one huge accent on a shouted throw and one sharp accent on a spear flick; then short urgent drums at a dark back gate, easing after a distant shout, a warm victory melody at a grey dawn, all cut away to one low note at the end; ancient Chinese rural drama, no vocals"

# Places.
N1 = "In the night yard of the Xu farmhouse at the third watch of the same night"
NIGHT = "cool pale moonlight from above, the yard dark and still, a faint warm glow along the house wall at the left"
YARD = ("the farmhouse on the left with its dark doorway at the far left and split firewood stacked against its front, the yard gate "
        "under its small tiled roof in the middle of the back wall with its plank leaf swung back inward against the left post, a "
        "bare tree just right of the gate, the low earth-and-stone back wall running from the gate to the right edge, the round "
        "stone well with its wooden windlass in the front right, a row of straw mats laid side by side on the ground between the bare "
        "tree and the well, a wooden bucket in the middle of the yard, dark fields and far dark hills beyond the wall")  # -ye-dong2-l1 (e936 s31 as cut)
POOLMARK = " below the deep pool"  # mkspec.py takes it out of every channel shot in d1 (gen-dh's SET needs "deep pool")
Q1 = f"At the new channel at the foot of the hills outside Liuxi{POOLMARK} in the fourth watch of the same night"
Q2 = f"At the new channel at the foot of the hills outside Liuxi{POOLMARK} in the last dark hour of the night"
QNIGHT = "cold pale moonlight, the deep blue night sky full of small stars"
Q3 = f"At the new channel at the foot of the hills outside Liuxi{POOLMARK} at the first grey of dawn"
QDAWN = "cold grey-blue light just before sunrise, the sky pale grey-white low over the far pines, a thin drift of pale lime powder low over the field"
CHANNEL = ("a freshly dug dry channel about knee-deep, wide and flat-bottomed, running straight from the foreground away into the "
           "distance, its bed bare cracked dry earth; on its left bank a long low ridge of dug brown earth with a heap of dry straw on "
           "it, and beyond the ridge a flat dry field running to a line of dark pines at the far left; a single plank laid across the "
           "channel on one thin wooden post in the middle distance; on the right bank a strip of dry grass and a dark paddy of young rice")  # -ye2
H1 = "At the narrow back gate in the wall of the night yard of the Xu farmhouse at the same hour"
HMOON = "cold pale light of the full moon high above, the alley in deep shadow, warm light from inside the doorway"
BACKGATE = ("a long low wall of rough dark stone running from the far left into the frame, the narrow plank door in it at the right "
            "standing ajar inward with warm light inside, split logs stacked against the wall just left of the door, the dark alley "
            "running away to the left along the wall under bare trees")  # set-xujia-houmen-ye-l1
LOC = {
    "ny": f"{N1}: the yard exactly as in the picture: {YARD}; {NIGHT}",
    "ny_g": f"{N1}, just inside the yard gate; {NIGHT}",
    "ny_w": f"{N1}, by the low earth-and-stone back wall on the right; {NIGHT}",
    "ny_c": f"{N1}, in the middle of the yard; {NIGHT}",
    "ny_e": f"{N1}; {NIGHT}",  # the insert s08: mkspec.py leaves only "Insert close-up" (rule 35)
    "q": f"{Q1}: the channel exactly as in the picture: {CHANNEL}; {QNIGHT}",
    "q_r": f"{Q1}, on the long ridge of dug earth along the left bank; {QNIGHT}",
    "q_f": f"{Q1}, on the flat dry field just before the long ridge of dug earth; {QNIGHT}",
    "q2_r": f"{Q2}, on the long ridge of dug earth along the left bank; {QNIGHT}",
    "q2_f": f"{Q2}, on the flat dry field before the long ridge of dug earth; {QNIGHT}",
    "q2_e": f"{Q2}; {QNIGHT}",  # the insert s23
    "hm": f"{H1}: the place exactly as in the picture: {BACKGATE}; {HMOON}",
    "hm_d": f"{H1}, beside the narrow plank door; {HMOON}",
    "hm_x": f"{H1}, in the doorway looking down the dark alley; {HMOON}",
    "q3": f"{Q3}, on the long ridge of dug earth along the left bank; {QDAWN}",
}
LIGHT = {
    "night": "the cool moonlight stays unchanged",
    "dawn": "the cold grey-blue dawn light stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_COAT = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow with an old grey cloth outer coat worn loose over "
           "his shoulders")  # bible 〈人物〉: the outer coat by night
XU_LIME = f"{XU_COAT}, pale white lime powder dusted over the lower half of the robe"  # c35 on (the script's 石灰白粉; no mud)
LAMP = "one small clay oil lamp with one flame"  # bible 〈道具〉 許硯的陶油燈
QIN = ("Qin Shuang, in her fitted dark brown cross-collared short jacket cinched with a wide plain leather belt, fitted black "
       "trousers and leather boots, her sleek high ponytail tied with black cord")  # rule 5: nothing in her belt
SPEAR = "one long spear: a plain wooden shaft taller than she is, a small plain iron spearhead, the shaft bare below the head"  # bible 〈道具〉 (rule 18: no "no tassel")
RAID_SPEAR = "one long spear: a plain wooden shaft taller than a man, a small plain iron spearhead, the shaft bare below the head"
ALING = ("A-ling, in her plain grey-white cotton dress tailored close at the waist with a cloth sash, its long sleeves down over "
         "both wrists, her long black hair pinned up with one plain wooden hairpin")
KNIFE = "one short knife sheathed in plain dark wood, grip and sheath one closed piece of dark wood as long as her hand"  # rule 22
ERNIU = "Wang Erniu, in his coarse brown short jacket with rolled sleeves"
DIAOQI = ("Diao Qi, tall and powerfully built, in his ragged rough earth-brown tunic with frayed cuffs and black leg wraps, the "
          "long pale old scar from his left brow down across his left cheekbone")
SABER = "one long single-edged broad-backed saber"  # bible 〈道具〉 刁七的刀 (only s18-s28)
XIAOHE = ("little Xiaohe, eight years old, in her patched lilac cotton jacket, two little pigtails tied with red string")
HOE = "one hoe with a plain wooden handle and a flat iron head"
POLE = "one long bamboo pole"
SACK = "one round hemp sack of lime, its neck tied with cord"
STICK = "one plain wooden stick"
BUCKET = "one wooden bucket bound with iron hoops, full of steaming hot water"
FIRELINE = "a long thin line of small orange flames streaming out of the pines, far away"  # rule 37 (the picture has pines, no hillside)
SMOKE = "thick white powdery smoke"  # rule 37 (not fog)
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
NOSMILE_ERNIU = "not smiling: brows knotted hard, eyes wide, jaw tight"
MEN4 = ("four men in ragged homespun, each a different colour and age, a lean young man in a rust-red jacket, an older man with a "
        "short grey beard in a faded undyed hemp-beige jacket, a stocky man in a dull olive-green jacket and a thin man in a faded "
        "ochre jacket")
MEN6 = ("six men in ragged homespun, each a different colour and age, a lean young man in a rust-red jacket, an older man with a "
        "short grey beard in a faded undyed hemp-beige jacket, a stocky man in a dull olive-green jacket, a thin man in a faded "
        "ochre jacket, a broad young man in a dark charcoal jacket and a boy of about fifteen in a mustard-yellow jacket")
RAIDER = "one raider in a ragged undyed homespun tunic and a cloth head wrap"
# rule 40 (e031 / e033 / e935 / e936 TBACK): Tang Xiaotang from behind, her l1 costume (rule 4), no outer coat
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with every strand of her black hair "
         "combed smooth and gathered up into just two round buns set high on her head, one bun on each side, one short pink "
         "silk ribbon wrapped around each bun, the nape of her neck bare and clear above a pink inner collar, and her light "
         "peach-pink silk shoulders; the back of her head facing straight away from us the whole time, her head still, her ear "
         "the furthest round her head we ever see")
TBACK_SMALL = ("one young woman seen only from behind, appearing only once, her black hair in just two round buns set high on her "
               "head tied with short pink silk ribbons, in a light peach-pink silk jacket and skirt")
HEADSTILL = "the young woman with the two high round buns keeps her head still, facing straight away from us, the back of her head toward us the whole shot"
XU_EDGE = ("at the right edge of the frame, cut by it, soft and out of focus, only one shoulder and upper arm of a man in an old grey "
           "cloth outer coat, toward us the whole shot")
XU_EDGE_L = XU_EDGE.replace("at the right edge", "at the left edge")
QIN_EDGE = ("at the right edge of the frame, cut by it, soft and out of focus, only the back of a young woman's head with a sleek "
            "high black ponytail and one shoulder in a dark brown short jacket, toward us the whole shot")
SIDE_TREE = "the dark bare branches of the tree against the night sky"
SIDE_WALL = "the low earth-and-stone wall in the moonlight"


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
TWO_BACK = "exactly two people, the young woman in the middle seen only from behind"

SHOTS = [
    # ---- scene 1: the Xu yard, the third watch, the same moment as e036's last shot (36->37).
    dict(chapter="許家院子，四百人", loc="ny_g", cam="Wide shot, slow push in", chars=["erniu"], night="night",
         comp=f"wide shot inside the yard toward the yard gate, like the picture: the plank gate leaf swung back inward against the left gate post from the first frame to the last, the gateway clear in the middle of the back wall; {ERNIU}, {HOE} gripped in his right hand with its iron head low by his feet, already through the gateway and running into the yard toward us from the first frame, framed full figure, his eyes toward someone out of sight beyond the left edge of the frame, never the lens; frightened and urgent, {NOSMILE_ERNIU}, mouth wide between shouted words, breathing hard; at the right, beside the bare tree, {MEN4}, already sitting bolt upright on their straw mats from the first frame, side-on, their faces turned toward him, their lips closed; {HANDS}; exactly five people",
         lines=[("erniu", "四百人！山上下來四百人，火把數都數不完！", "大嗓門，嚇到了，喘")],
         motion=f"Wang Erniu runs three steps toward us and stops short, panting, and thrusts his flat left hand back toward the far hills behind the wall as he shouts; {quiet('the four men on the mats', 'their', plural=True)}",
         zh="中遠景（朝院門）、慢推（送第 36 集的免費裁切 `set-xujia-yuan-ye-dong2-zhong-l1`：木桶、光禿的樹、院門）：**接點 36→37（照第 36 集成片 `e936-live.mp4` 最後 15 秒與 s31）**：同一刻，二牛從**後牆中間的院門**衝進來、朝鏡頭跑（拍法 42）；**院門的門扇在圖上本來就往內推開、靠在左門柱**（聖經〈接點〉36→37 的備案一：照圖寫，結果寫在第一格到最後一格，任務檔『門要明寫關著或推開』）；稿子『肩膀撞開門板、門板撞上籬笆彈回』改成第一格已經衝進門（一鏡一個動作）。他跑三步停住、喘、左手平掌往後朝牆外的山一揮（稿子『指向山』：單指會讀錯，拍法 32），大嗓門喊（答第 36 集 s38）；**不笑**逐部位寫（二牛報壞消息常笑，聖經〈人物〉）。畫右樹旁四個流民被驚得坐起（第 36 集成片：草蓆在樹與井之間的院子中段；稿子『九個』照拍法 34 寫看得見的四個，每人衣色年紀不同）。許硯的油燈光不寫（燈要寫在手上）"),
    dict(loc="ny_c", cam="Close-up, slow push in", chars=["erniu"], night="night",
         comp=f"close-up of {ERNIU}, standing in the yard, framed from the chest up with space above his head, his two hands already gripping the wooden handle of his hoe before his chest from the first frame, the handle running down out of the bottom of the frame, his face three-quarter to screen left {off('left', SIDE_TREE)}; afraid and grim, {NOSMILE_ERNIU}, breathing hard, lips moving between words; behind him, soft, only the dark bare branches of the tree against the night sky; {HANDS}",
         lines=[("erniu", "咱們連流民裡肯拿鋤頭的，才六十個。", "喘，壓不住慌")],
         motion="Wang Erniu's two hands tighten on the hoe handle until the hoe shakes, and he draws one hard breath as he speaks",
         zh="近景、慢推（送本集免費做的 `set-xujia-yuan-ye-dong2-shu-l1`：光禿的樹枝映夜空、右邊遠山、左下院門瓦簷；稿子『身後只有柿子樹的枝葉』）：二牛兩手攥緊鋤頭柄、柄往下出畫（長桿只露一段，拍法 32），攥到鋤頭發抖、喘一口氣，朝畫左外看不到的人（許硯，不點名、不寫人，拍法 31）說；不笑"),
    dict(loc="ny_c", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU_COAT}, standing in the middle of the yard, framed from the chest up with space above his head, {LAMP} held low in his left hand at the bottom edge, its small flame lighting one side of his face from below, his face three-quarter to screen right, his eyes already lifted to the far dark hills beyond the right edge of the frame from the first frame, never the lens; he is the only person in the frame; grave and still, not smiling: brows drawn, eyes fixed, lips pressed shut; behind him, soft, only the dark bare branches of the tree against the night sky; {HANDS}",
         lines=[("xitong", "叮。守村任務：婦孺一個不能少。", "冷，宣布")],
         panel=[("守村任務：婦孺一個不能少", "task")],
         motion=f"Xu Yan lowers the lamp slowly toward his waist, its flame swaying, his eyes staying on the far hills; {SILENT_HE}",
         zh="近景、慢推（送 `-shu-l1`）：許硯（夜裡外披舊灰外衣，聖經〈人物〉）左手一盞陶油燈（一朵火，聖經〈道具〉；接第 36 集 s38），燈從下面照半邊臉；眼睛第一格已經抬向畫右外的遠山（第 36 集 s38 他朝畫右上望牆頭與山）；把油燈慢慢放低（一個動作）；系統是錄音、**全程嘴閉著**；**不寫淡藍光**（拍法 11），面板『守村任務：婦孺一個不能少』剪接時疊、跟系統念的一字不差"),
    dict(loc="ny_w", cam="Wide shot, slow push in", chars=["xuyan", "qinshuang"], night="night",
         comp=f"wide shot by the low earth-and-stone back wall on the right: at the right, {QIN}, already dropped down off the top of the wall from the first frame and crouching low on the packed earth before the wall beside the round stone well, framed full figure, her face turned to screen left toward him, her lips closed, not smiling, never the lens; at the left, {XU_COAT}, {LAMP} held in his left hand, standing, framed full figure, already turned toward her from the first frame, his face three-quarter to screen right toward her, never the lens; firm and clear, not smiling: brows level, eyes sharp, lips moving clearly between words; behind them, soft, the low wall and the dark fields beyond it; {HANDS}; exactly two people",
         lines=[("xuyan", "不守村口。下山的路，最後都得走渠頭那道土埂。", "很穩，定下來")],
         motion=f"Qin Shuang rises from her crouch to her full height in one smooth move, and Xu Yan lifts his flat right hand toward the far hills beyond the wall as he speaks; {quiet('Qin Shuang', 'her')}",
         zh="中遠景、慢推（送第 36 集的 `set-xujia-yuan-ye-dong2-qiang-l1`：後牆右段、牆外暗田、右下井的轆轤）：秦霜第一格已經從後牆右段的牆頭跳下、蹲在井旁的牆前（稿子『從東牆頭往下一跳、落在井沿旁蹲穩』：跳的那一下在第一格完成，拍法 32；井在前右，拍法 42），站起來（一個動作）；許硯在左、提油燈、已經轉向她，右手平掌朝牆外的山一抬（稿子『抬手往山腳一指』），很穩地說；秦霜嘴閉著、不笑"),
    dict(loc="ny_w", cam="Close-up, slow push in", chars=["qinshuang"], night="night",
         comp=f"close-up of {QIN}, standing before the low back wall, framed from the chest up with space above her head, her face three-quarter to screen left {off('left', SIDE_WALL, he='she')}; sharp and sure, not smiling: eyes bright and narrowed, brows level, lips moving firm between words; behind her, soft, only the low wall and the dark fields beyond it; {HANDS}",
         lines=[("qinshuang", "四百人，也得一個一個走那道土埂。陣我來排。", "眼睛一亮，篤定")],
         motion="Qin Shuang's eyes dart once over her shoulder toward the far hills beyond the wall and come back as she speaks",
         zh="近景、慢推（送 `-qiang-l1`；稿子『身後只有東牆與月光』照圖寫後牆）：秦霜眼神往肩後牆外的山一瞥、再轉回來（稿子『眼睛一亮、往山看一眼、轉回來』，一個動作），朝畫左外看不到的人（許硯，不點名）說（← 因為 s04）；稿子『手按柴刀柄』不寫（拍法 5：柴刀不寫；近景也看不到手）；不笑"),
    dict(loc="ny_c", cam="Medium shot over the shoulder, slow push in", chars=["xuyan"], night="night",
         comp=f"medium shot over a shoulder: {QIN_EDGE}; beyond it, in the left half of the frame, {XU_COAT}, {LAMP} held in his left hand, standing in the yard, framed from the waist up, his face three-quarter to screen right toward the young woman in the foreground, never the lens; steady and certain, not smiling: brows level, eyes calm, lips moving evenly between words; behind him, soft, the split firewood stacked against the house front and the dark window; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("xuyan", "陣妳排，怎麼打我照妳的，一個字都不改。", "一字一句，很穩")],
         motion="Xu Yan gives one firm nod and holds the lamp out a little before him, its small flame lighting the ground between them, as he speaks",
         zh="過肩中景、慢推（送第 36 集的 `set-xujia-yuan-ye-dong2-chai-l1`：屋前柴堆、格子窗）：前景右是虛焦、被畫框切掉的高馬尾後腦與深褐肩頭（秦霜，不點名、不送圖，拍法 2）；許硯點一下頭、把油燈往前一遞照亮兩人中間的地（一個動作），一字一句地說（好感 +7 的原因，c36 回收）"),
    dict(loc="ny_c", cam="Medium shot from behind, slow push in", chars=["xuyan"], night="night",
         comp=alone(f"{BEYOND_XU}, {XU_COAT}, {LAMP} held in his left hand, standing, framed from the waist up, his face three-quarter to screen right toward her, never the lens; urgent and steady, not smiling: brows drawn, lips moving quickly between words; behind them, soft, the dark doorway of the house and the split firewood beside it; she stays in the middle of the frame the whole shot; {HANDS}; {TWO_BACK}",
                    "standing in the middle of the yard,"),
         lines=[("xuyan", "小棠，婦孺都進屋，妳跟阿令守後門。", "急，壓低，很穩")],
         motion=f"Xu Yan lays his flat right hand on her left shoulder and presses once as he speaks; {HEADSTILL}",
         zh="中景（從背後）、慢推（送第 36 集的 `set-xujia-yuan-ye-dong2-wu-l1`：屋左的黑門洞與柴堆）：唐小棠背影在畫面正中、頭不動、剛好兩顆丸子（拍法 40；l1 交領短襦，不寫 t2 高立領與淡杏外衣，拍法 4；她不說話，不點名、不送她的臉部圖，mkspec 加雙丸子背影參考圖）；許硯在她前方畫左三分之一、提油燈，右手平掌按一下她的肩（一個動作；稿子『回頭看一眼屋門口的阿令』不拍：阿令不入鏡，屋門洞在他身後），急而穩地說"),
    dict(loc="ny_e", cam="Insert close-up, slow push in", chars=[], night="night",
         comp="insert close-up, the very first frame is already a close view of two small fair hands in light peach-pink silk cuffs gripping the cuff of a faded blue-grey sleeve under the edge of an old grey cloth outer coat, holding on tight; far below, soft and out of focus, only packed dark earth in a faint warm glow fills the background to every edge; only the two hands and the sleeve are in the frame",
         lines=[("tangxiaotang", "那你呢？你一個書生，打算站在哪裡？", "擔心，眉頭皺著")],
         motion=NOBODY + "the two small hands tighten on the sleeve cuff, tug it once and hold on",
         zh="插鏡、慢推（**第一格就是兩手抓袖口**，拍法 10、35；不寫地點句，送本集免費做的 `set-xujia-yuan-ye-dong2-di-l1`（院子暖光裡的地）只當地面與光）：稿子 c08 是唐小棠下巴以上近景說話；真人版她不露嘴說話（拍法 3、40），改成她兩手（桃粉袖口）抓住許硯舊灰外衣下藍灰袖口、抓緊扯一下的插鏡，她的話是錄音（畫外；接第 36 集 s38 她抓他右袖；→ 答在 s09）"),
    dict(loc="ny_c", cam="Medium shot from behind, slow push in", chars=["xuyan"], night="night",
         comp=alone(f"{BEYOND_XU}, {XU_COAT}, standing, framed from the waist up, {LAMP} already held out in his left hand toward her from the first frame, his face three-quarter to screen right toward her, never the lens; resolved, not smiling: brows level, eyes steady, lips moving firmly between words; behind them, soft, the split firewood stacked against the house front and the yard gate in the dark; she stays in the middle of the frame the whole shot; {HANDS}; {TWO_BACK}",
                    "standing in the middle of the yard,"),
         lines=[("xuyan", "我站渠頭。石灰是我的主意，我得在那裡。", "乾脆，不容商量")],
         motion=f"Xu Yan presses the lamp into her two hands and lets go, and her two hands close round it, only her arms moving; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-chai-l1`：柴堆、院門）：唐小棠背影在正中（不點名、不送臉部圖）；許硯第一格已經把油燈遞到她面前，塞進她兩手、放手（一個動作；稿子『輕輕扳開她的手指』交給 s08 的抓袖子），乾脆地說（答 s08）。稿子後半『轉身往院門走、九個流民抓鋤頭跟上』拆到 s09b"),
    dict(sid="s09b", loc="ny", cam="Wide shot, slow push in", chars=["xuyan"], night="night", act=3,
         comp=f"wide shot from the middle of the yard toward the yard gate, like the picture: {YARD}; walking away from us toward the gateway, {XU_COAT}, seen from behind, framed full figure, already halfway across the yard from the first frame, the back of his head toward us; just behind him, seen from behind, {MEN6}, each already carrying {HOE} on his shoulder from the first frame, the hoes well apart; {HANDS}; exactly seven people",
         motion="Xu Yan and the six men stride on across the yard and out through the gateway one after another, their backs toward us the whole shot; nobody speaks, every mouth stays closed",
         zh="全景、慢推（照圖；送第 31 集的 `set-xujia-yuan-ye-dong2-l1`：院門在後牆中間、門扇推開靠左柱、樹、井在前右、草蓆在樹與井之間）：**拆鏡**：稿子 c09 後半與 2026-11-06 審稿補的『九個流民拿鋤頭跟著許硯往院門跑』：許硯背影第一格已經走到院子一半，六個流民（背影，每人衣色年紀不同；稿子『九個』照拍法 34）扛著鋤頭跟在後面（鋤頭第一格就扛在肩上、彼此分開），一個接一個走出院門（第一場結尾，切渠頭）。無台詞"),
    # ---- scene 2: the head of the new channel, the fourth watch to just before dawn.
    dict(chapter="新渠渠頭，石灰陣", loc="q", cam="Wide shot, slow push in", chars=["xuyan"], night="night",
         comp=f"wide shot from the near end of the channel at standing eye height, like the picture: walking along the top of the long ridge of dug earth, three men in Song-dynasty homespun short jackets and cloth head wraps, each a different colour and age, a stocky middle-aged man in a dull olive-green jacket, a broad young man in a dark charcoal jacket and a boy of about fifteen in a mustard-yellow jacket, each carrying {SACK} in both arms; walking among them along the ridge, {XU_COAT}, framed full figure, his face three-quarter to screen left down at the ridge, never the lens; firm, not smiling: lips moving clearly between words; in the near part of the ridge, a lean young man in a rust-red jacket already kneeling from the first frame over a shallow hole with his sack in both hands; {HANDS}; exactly five people",
         lines=[("xuyan", "糖坊剩的石灰，三步埋一袋，袋口朝上。", "交代，壓低聲音")],
         motion="the kneeling man sets his sack down into the shallow hole with its tied neck pointing up, and Xu Yan points his flat right hand down at the next spot three steps on as he speaks",
         zh="全景、慢推（照圖；送本集免費做的 `set-shanjiao-qu-ye2-l1`：第 4 篇章試鏡第五輪付費的夜景 `-ye` 照第 36 集的清理再做一次——左邊護欄、渠中段直立平木板、地平線的方塊塗掉，**細月也塗掉**（第 36 集是滿月）；乾渠往深處、左岸一長道土埂與一堆乾草、土埂外一片乾地延到遠處松樹、渠中段木板架在細樁上、右岸暗秧田）：**第二場的格局**：稿子的『土埂』是圖上左岸那道新土堆，守的人在土埂上面向左邊的乾地（流寇從畫左遠處的松樹那頭過乾地衝來）。四更月光。三個壯丁抱著石灰麻袋沿土埂走（稿子『約二十人』照拍法 34），近處一個鐵鏽紅短打的第一格已經跪在淺洞前，把麻袋放進洞、袋口朝上；許硯走在中間，右手平掌往下指三步外的下一個位置（單指會讀錯），交代地說（石灰的來處：糖坊剩的，稿子）"),
    dict(loc="q_f", cam="Medium shot, slow push in", chars=["erniu"], night="night",
         comp=f"medium shot on the flat dry field just before the long ridge of dug earth, the edge of a freshly dug shallow pit soft in the lower foreground: {ERNIU}, already standing in the knee-deep pit from the first frame, {HOE} in both hands, framed from the knees up, his face lowered three-quarter to screen right toward the pit, never the lens; he is the only person in the frame; puzzled, not smiling: brows drawn together in doubt, lips moving between words; behind him, soft, the flat dry field and the line of dark pines under the night sky; {HANDS}",
         lines=[("erniu", "坑才挖到膝蓋，這麼淺有什麼用？", "不解")],
         motion="Wang Erniu drives the hoe once into the floor of the pit, stops, straightens his back and looks down at the pit as he speaks",
         zh="中景、慢推（送本集免費做的 `set-shanjiao-qu-ye2-zhuo-l1`：乾地、遠處松樹、右下土埂的一角）：淺坑挖在土埂前的乾地（流寇那一側）；二牛第一格已經站在膝蓋深的坑裡，一鋤頭下去、停、直起腰看坑（一個動作），不解地說（→ 答在 s12）；不笑"),
    dict(loc="q_f", cam="Low-angle medium shot, slow push in", chars=["xuyan", "erniu"], night="night",
         comp=f"low-angle medium shot at ground height, the mouth of a shallow pit soft in the foreground: at the left, {XU_COAT}, already crouching at the edge of the pit from the first frame with an armful of dry straw, framed from the waist up, his face lifted three-quarter to screen right toward Wang Erniu, never the lens; calm, a faint easy look in his eyes, lips moving evenly between words; at the right, a step behind the pit, {ERNIU}, standing, {HOE} planted upright beside him with both hands resting on top of its handle, framed from the waist up, his face lowered toward Xu Yan, his lips closed, not smiling, never the lens; behind them, soft, the long ridge of dug earth and the heap of dry straw; {HANDS}; exactly two people",
         lines=[("xuyan", "不用深，夜裡衝過來的人，絆一跤就夠了。", "輕鬆，篤定")],
         motion=f"Xu Yan spreads the dry straw across the mouth of the pit and pats it flat with his flat hand as he speaks, and Wang Erniu nods once slowly; {quiet('Wang Erniu')}",
         zh="低角度中景（貼著地面）、慢推（送本集免費做的 `set-shanjiao-qu-ye2-geng-l1`：土埂與乾草堆）：許硯第一格已經蹲在坑邊、懷裡一把乾草，鋪在坑口、用手掌拍平（一個動作；稿子『抬頭看二牛』寫成臉已經朝他），說（答 s11；稿子『可以淡淡一笑』寫成眼神放鬆，不寫笑字）；二牛在後面拄著鋤頭（兩手搭柄頂、立著，跟乾草分開）、點頭、嘴閉著、不笑"),
    dict(loc="q_r", cam="Wide shot, slow push in", chars=["qinshuang"], night="night",
         comp=f"wide shot from the near end of the long ridge of dug earth at standing eye height, the flat dry field beyond it at the left and the line of dark pines far away: on the ridge, facing the field at the left, three rows of men in Song-dynasty homespun short jackets and cloth head wraps, each a different colour and age: in front, crouching low on the ridge, a lean young man in a rust-red jacket, a broad young man in a dark charcoal jacket and a thin man in a faded ochre jacket, each holding {POLE} pointed out over the field, the poles well apart; behind them, standing, a stocky man in a dull olive-green jacket and a boy of about fifteen in a mustard-yellow jacket, each holding {SACK} against his chest; at the back, an older man with a short grey beard in a faded undyed hemp-beige jacket holding {STICK}; standing among them just behind the front row, {QIN}, framed full figure, her face three-quarter to screen left toward the men, never the lens; commanding, not smiling: brows level, eyes sharp, lips moving loud and clear between words; {HANDS}; exactly seven people",
         lines=[("qinshuang", "前排蹲下，我不喊，誰都不准動。", "嗓門亮")],
         motion=f"Qin Shuang bends and presses one man's bamboo pole lower with her flat hand as she speaks; {quiet('the men', 'their', plural=True)}",
         zh="全景、慢推（送 `set-shanjiao-qu-ye2-l1`）：三列：前排三人蹲在土埂上握長竹竿（竹竿第一格就各自分開，長桿第一格分開）、第二排兩人抱石灰袋、第三排一人拿素木棍（稿子『約二十人』『約六十人』照拍法 34 寫看得見的六個，每人衣色年紀不同）；秦霜在前排後面，彎腰用手掌把一根竹竿壓低（一個動作），嗓門亮地說。**稿子『解下腰帶右邊的柴刀塞給第三排一個空手的壯丁』不拍**（拍法 5、聖經〈道具〉：她空手排陣）"),
    dict(loc="q_r", cam="Medium shot over the shoulder, slow push in", chars=["qinshuang"], night="night",
         comp=f"medium shot over a shoulder: {XU_EDGE}; beyond it, in the left half of the frame, {QIN}, standing in the front row on the long ridge of dug earth, framed from the waist up, her face three-quarter to screen left toward the dark field, her eyes on the field, never the lens; cold, not smiling: eyes narrowed, jaw set, lips moving short and hard between words; behind her, soft, the flat dry field and the line of dark pines under the night sky; {HANDS}; exactly two people, the one at the edge seen only in part",
         lines=[("qinshuang", "你下去，站到後頭，這裡會死人。", "冷，不看他")],
         motion="Qin Shuang, her eyes staying on the field, jabs her right elbow back toward the man at the right edge as she speaks",
         zh="過肩中景、慢推（送 `-ye2-zhuo-l1`）：**機位反過來**：稿子是秦霜肩後拍許硯（她在前景說話＝背影＋錄音），改成許硯肩後拍她（前景右是虛焦的舊灰外衣肩，不點名、不送圖，拍法 2），她站在畫左、許硯在她右邊（場頭軸線），臉朝畫左的乾地、不看他，右手肘往後一頂（一個動作），冷冷地說（→ 答在 s15）；這樣她的嘴在畫面上、台詞是片中原聲"),
    dict(loc="q_r", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU_COAT}, standing on the long ridge of dug earth, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes on the dark field beyond the left edge of the frame, never the lens; he is the only person in the frame; quietly stubborn, not smiling: brows level, eyes steady, lips moving low and even between words; behind him, soft, only the dry channel, the plank across it and the dark paddy in the moonlight; {HANDS}",
         lines=[("xuyan", "我說過照妳的陣打，可我得看著它打完。", "低聲，不退")],
         motion="Xu Yan, instead of stepping back, leans his weight forward and plants himself half a step further on as he speaks, his eyes on the field",
         zh="近景、慢推（送本集免費做的 `set-shanjiao-qu-ye2-tian-l1`：渠、木板、暗秧田；稿子『身後只有渠岸與月光』：他面向左，身後是渠與右岸）：許硯沒退，重心往前、多站上半步（一個動作），眼睛看著畫左外的乾地（看的是地方，不寫人，拍法 31），低聲說（答 s14：不退）；不笑"),
    dict(loc="q_r", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU_COAT}, standing on the long ridge of dug earth, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes on the dark field beyond the left edge of the frame, never the lens; he is the only person in the frame; uneasy, not smiling: brows tight, lips pressed shut; behind him, soft, only the dry channel, the plank across it and the dark paddy in the moonlight; {HANDS}",
         lines=[("xitong", "宿主不會打架，站在前排的用處是當靶子。", "冷，毒舌")],
         motion=f"Xu Yan swallows once, his throat moving, his eyes still on the field; {SILENT_HE}",
         zh="近景、慢推（送 `-ye2-tian-l1`）：稿子 c16 系統句：許硯吞一口口水（一個動作），系統是錄音、**全程嘴閉著**；不寫淡藍光（拍法 11；系統的鬥嘴不出面板）。稿子 c16 系統 16 字＋心裡話 15 字約 9.5 秒加停頓，10 秒片段放不下剪點：拆成本鏡與 s16b"),
    dict(sid="s16b", loc="q_r", cam="Medium close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"medium close-up of {XU_COAT}, standing on the long ridge of dug earth, framed from the waist up, both his hands resting at his sides from the first frame, his face three-quarter to screen left, his eyes on the dark field beyond the left edge of the frame, never the lens; he is the only person in the frame; quietly resolved, not smiling: brows level, lips pressed shut; behind him, soft, only the dry channel and the dark paddy in the moonlight; {HANDS}",
         lines=[("xuyan", "當靶子也好，至少她不用回頭找我。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan's two hands close slowly into fists at his sides and loosen again; {SILENT_HE}",
         zh="中近景（腰以上：手要在框裡，拍法 32）、慢推（送 `-ye2-tian-l1`；跟 s16 不同景別）：**拆鏡**：稿子 c16 的心裡話：兩手握拳又鬆開（一個動作）；心裡話是錄音、**全程嘴閉著**、不笑（系統的鬥嘴由他回嘴）"),
    dict(loc="q2_f", cam="Low-angle extreme wide shot, slow push in", chars=[], night="night", act=3,
         comp=f"low-angle extreme wide shot from just behind the long ridge of dug earth, the tops of three head-wrapped heads of crouching men soft and dark along the bottom edge of the frame, seen only from behind; beyond the ridge the flat dry field runs to the line of dark pines at the far left, and {FIRELINE}; nearer, coming across the field toward us, six running men seen only as small dark shapes, each holding up one burning torch in one hand at running speed; only the three heads, the field, the pines, the six running men and the small far flames are in the frame",
         motion=NOBODY + "the long line of small flames streams on out of the pines and the six running torches come on across the field, dust rising behind them, while the three heads in the foreground stay still",
         zh="低角度大全景、慢推（送 `-ye2-zhuo-l1`）：天快亮前。前景下緣三個蹲著的人的頭頂（背影）；遠處松樹那頭流出一長串小火光（拍法 37：不寫人數；圖上沒有山坡，寫成從松樹流出來），近一點六個奔跑的黑影各舉一支火把（每支一人、奔跑的速度，拍法 37）過乾地揚起塵土；守的人不動。鼓聲停、只剩腳步聲交給音效。無台詞"),
    dict(loc="q2_f", cam="Medium shot, slow push in", chars=["diaoqi"], night="night",
         comp=f"medium shot on the flat dry field, a few wisps of dry straw soft in the lower foreground: {DIAOQI}, {SABER} gripped in his right hand, already running toward the ridge at the right at full speed from the first frame, framed from the waist up, his face three-quarter to screen right toward the ridge, never the lens; savage, not smiling: brows crushed down, eyes wild, mouth wide in a roar between words; behind him, dark and soft, three running men seen only as shapes, each holding up one burning torch, the torchlight flaring orange on one side of his face; {HANDS}; exactly four people, the three behind him seen only as dark shapes",
         lines=[("diaoqi", "衝過去！柳溪的糧，全是咱們的！", "粗啞，吼")],
         motion="Diao Qi swings the saber forward over his head as he runs on and roars",
         zh="中景、慢推（送 `-ye2-zhuo-l1`；稿子的跟拍改慢推）：**刁七第一次出場**：送 `diaoqi-portrait-l1`（左眉骨斜到左顴骨一道淡色舊疤、破布短褐、黑綁腿；**不穿皮甲**：extras 把 `cast.json` 的皮甲句換掉，聖經〈人物〉、原版必修），右手一把單刃厚背長刀（聖經〈道具〉：只在 s18–s28，寫畫面側）；第一格已經朝右邊的土埂全速衝，長刀往前一揮、吼（一個動作）；身後三個舉火把的黑影（每支一人）"),
    dict(loc="q2_r", cam="Medium close-up, slow push in", chars=["qinshuang"], night="night",
         comp=f"medium close-up of {QIN}, crouching low in the front row on the long ridge of dug earth, framed from the waist up, her face three-quarter to screen left, her eyes on the firelight coming across the field beyond the left edge of the frame, never the lens; she is the only person in the frame; utterly still and cold, not smiling: eyes narrowed, brows level, lips barely moving between words; a faint orange glimmer of far torchlight on one side of her face; behind her, soft, only the dry channel and the dark paddy in the moonlight; {HANDS}",
         lines=[("qinshuang", "等，讓他們踩上坑，再等三步。", "極輕")],
         motion="Qin Shuang lifts her left hand flat, palm down, and holds it there pressing the air down slowly as she whispers",
         zh="中近景（腰以上：手勢要在框裡，拍法 32）、慢推（送 `-ye2-tian-l1`；稿子『身後只有蹲著的前排與月光』：前排的人不寫，拍法 31）：秦霜蹲在前排（許硯左邊，不入鏡），盯著畫左外越來越近的火光（寫火光，不寫人），左手平掌往下壓住（一個動作），極輕地說；配樂全部收掉"),
    dict(loc="q2_r", cam="Low-angle medium shot, slow push in", chars=["qinshuang"], nospeak=["qinshuang"], night="night",
         comp=f"low-angle medium shot from a little below, against the deep blue night sky: {QIN}, already risen to her feet on the long ridge from the first frame, framed from the waist up, her left hand already raised high and flat from the first frame, her face three-quarter to screen left toward the field, never the lens; fierce, not smiling: brows down, mouth wide on one shouted word; just behind her, three men in Song-dynasty homespun short jackets and cloth head wraps, a stocky man in a dull olive-green jacket, a boy of about fifteen in a mustard-yellow jacket and a young man in a faded deep plum jacket, each holding {SACK} up over his head in both hands; {HANDS}; exactly four people",
         lines=[("qinshuang", "扔！", "短喊")],
         motion="Qin Shuang chops her flat left hand down and shouts, and the three men hurl their sacks forward over her toward the field",
         zh="低角度中景（略仰）、慢推（送本集免費做的 `set-shanjiao-qu-ye2-kong-l1`：松樹頂上的夜空）：秦霜第一格已經站起來、左手平掌高舉，往下一劈、短喊（製作端寫成張嘴喊，不放進畫面描述：`nospeak`，構圖寫嘴張開喊一個字，preflight 的短喊警告因此為 0）；身後第二排三人（每人衣色不同）把石灰袋往前砸過去。剪接剪在石灰袋出手的一半（稿子〈剪接〉）"),
    dict(loc="q2_f", cam="Wide shot, slow push in", chars=[], night="night", act=3,
         comp=f"wide shot from the ridge over the flat dry field, the tips of three long bamboo poles soft in the lower right foreground: across the field, bursts of {SMOKE} billow up one after another and swallow the torches; six raiders seen only as dark staggering shapes in the smoke, two of them dropping waist-deep into hidden pits as the straw over the pits gives way, their torches falling to the ground; the line of dark pines far behind; only the pole tips, the smoke, the six dark shapes and the field are in the frame",
         motion=NOBODY + "the thick white powdery smoke rolls higher and wider across the field, one torch after another dims and goes out inside it, and the dark shapes reel and stumble",
         zh="全景、慢推（送 `-ye2-zhuo-l1`）：從土埂上看乾地：一團一團白色石灰煙炸開往上翻（拍法 37：`thick white powdery smoke`，不寫 fog），把火把吞進去，煙裡六個流寇黑影東倒西歪，兩個踩破坑上的乾草掉進坑裡、火把落地；火光一盞接一盞熄掉（整個動作留在畫面裡）。前景右下三根竹竿尖。稿子『土埂邊埋的石灰袋被踩破』：袋子埋在土埂上，這鏡只看到乾地，交給 s20 砸出去的袋子與音效。無台詞"),
    dict(loc="q2_f", cam="Medium shot, slow push in", chars=["diaoqi"], night="night",
         comp=f"medium shot in {SMOKE} on the field, the smoke soft in the foreground: {DIAOQI}, {SABER} still in his right hand, already bent over in the smoke from the first frame, his left hand pressed over his eyes, framed from the waist up, a thick coat of white powder over his face and hair, his face toward the right of the frame, never the lens; he is the only person in the frame; choking and furious, not smiling: brows crushed, mouth wide, coughing between words; behind him only the white smoke and the dark field; {HANDS}",
         lines=[("diaoqi", "什麼鬼東西！眼睛睜不開了！", "咳，眼睛睜不開")],
         motion="Diao Qi staggers one step back coughing and swings the saber blindly through the smoke as he shouts",
         zh="中景、慢推（送 `-ye2-zhuo-l1`）：刁七在白煙裡第一格已經彎著腰、左手捂眼，臉與頭髮一層白粉（一大片，不寫細點，拍法 12），往後退一步、長刀亂揮（一個動作）、咳著喊；不笑"),
    dict(loc="q2_e", cam="Insert close-up, slow push in", chars=[], night="night",
         comp="insert close-up from a little above, the very first frame is already a close view of a heap of dry straw with one burning torch lying across it, small flames already licking up through the straw tips; a man's foot in a dark cloth shoe under a brown trouser leg comes down hard on the flames; far below, soft and out of focus, only cracked dry earth fills the background to every edge; only the straw, the torch and the foot are in the frame",
         lines=[("erniu", "渠頭的草著了！差點燒到閘板！", "大喊")],
         motion=NOBODY + "the foot stamps down on the burning straw three times until the flames go out, and thin pale wisps curl up from the straw",
         zh="插鏡、慢推（**第一格就是草堆上的火把**，拍法 10、35；不寫地點句，送本集免費做的 `set-shanjiao-qu-ye2-cao-l1`（乾草堆近景）只當地面與光）：稿子『火把從畫左飛進來落在草堆』在第一格完成（火把已經躺在草上、草尖冒火）；二牛的腳（布鞋、褐褲腳，不點名）踩下、連踩三腳踩熄（一個動作；『用鋤頭挑進渠溝』不拍）。二牛的話是畫外錄音（給第 40 集『差點燒了咱們的渠頭』；台詞的『閘板』是圖上渠上的木板，不寫平木板：會長字）"),
    dict(loc="q2_r", cam="Medium shot, slow push in", chars=["erniu"], night="night",
         comp=f"medium shot beside the heap of dry straw on the long ridge of dug earth: {ERNIU}, {HOE} in his right hand with its iron head down by his feet, standing, framed from the waist up, already turned from the first frame, his face three-quarter to screen left {off('left', 'the long ridge of dug earth and white powder drifting in the air')}; breathless and fierce, {NOSMILE_ERNIU}, mouth wide between shouted words, breathing hard; behind him, soft, the long ridge and the straw; {HANDS}",
         lines=[("erniu", "火把全滅了！衝在前頭的，全掉進坑裡了！", "喘，大嗓門")],
         motion="Wang Erniu sweeps his flat left hand out toward the white powder drifting beyond the ridge as he shouts",
         zh="中景、慢推（送 `-ye2-geng-l1`：土埂與乾草堆）：二牛第一格已經把冒煙的火把甩掉、轉向前排（稿子『把火把甩進渠溝、回頭』在第一格完成），左手平掌往白煙那頭一掃（稿子『抬手指向白煙』），朝畫左外看不到的人喘著大喊（前排不寫，拍法 31）；**不笑**"),
    dict(loc="q2_f", cam="Medium shot over the shoulder, slow push in", chars=["diaoqi"], night="night",
         comp=f"medium shot over a shoulder: {XU_EDGE}; beyond it, in the left half of the frame, {DIAOQI}, already bursting out of the {SMOKE} from the first frame, framed from the waist up, a thick coat of white powder over his face, his eyes squeezed narrow and streaming, {SABER} raised high in his right hand, his face toward the man at the right edge, never the lens; murderous, not smiling: brows crushed, mouth wide in a roar between words; behind him only the white smoke and the dark field; {HANDS}; exactly two people, the one at the edge seen only in part",
         lines=[("diaoqi", "我刁七爺的刀，不砍書生，給我讓開！", "吼")],
         motion="Diao Qi lunges forward at the man at the right edge with the saber raised as he roars, and the man at the edge stays where he is",
         zh="過肩中景、慢推（送 `-ye2-zhuo-l1`；稿子的跟拍改慢推）：前景右是虛焦的舊灰外衣肩（許硯，不點名、不送圖，拍法 2；前排右端）；刁七第一格已經從白煙裡衝出來，臉上白粉、眼睛瞇著流淚（稿子『眼睛通紅』：不寫紅眼，拍法 12），高舉長刀撲向前景的人、吼；許硯不退（肩不動）。秦霜在許硯左邊，不入鏡（s26 才進）"),
    dict(loc="q2_r", cam="Medium shot, slow push in", chars=["qinshuang"], night="night",
         comp=f"medium shot on the long ridge of dug earth, the whole action inside the frame: at the right, {QIN}, standing in the front row, framed from the knees up, her face three-quarter to screen left, never the lens; cold and fast, not smiling: eyes narrowed, lips pressed shut; at the left, {RAIDER}, seen only from behind, already lunging at her with {RAID_SPEAR} thrust forward in both hands from the first frame; {HANDS}; exactly two people, the raider seen only from behind",
         motion="Qin Shuang twists aside from the spearhead, seizes the shaft in her right hand and wrenches it back, and the raider pitches forward onto the earth while the spear comes away in her right hand; nobody speaks",
         zh="中景（膝以上）、慢推（送 `-ye2-geng-l1`）：整個動作留在畫面裡：一個流寇（背影、破布短褐、布包頭）第一格已經挺著一桿長槍刺過來；秦霜側身讓開槍頭、右手抓住槍桿往後一拽，流寇撲倒，長槍落進她右手（一個連續動作）。長槍照聖經〈道具〉（素木桿比人高、小素鐵槍頭，**不寫 no tassel**：寫槍頭下的木桿是光的，拍法 18），mkspec 加送道具圖 `prop-changqiang-l1`。剪接剪在長槍落進她手裡（稿子〈剪接〉）。沒有人說話"),
    dict(loc="q2_r", cam="Medium shot, slow push in", chars=["qinshuang", "diaoqi"], night="night",
         comp=f"medium shot on the long ridge of dug earth, the whole action inside the frame: at the right, {QIN}, {SPEAR} held low and level in her right hand from the first frame, framed from the waist up, her face three-quarter to screen left toward him, never the lens; calm and cold, not smiling: eyes level, lips moving evenly between words; at the left, {DIAOQI}, a thick coat of white powder over his face, {SABER} raised over his head in his right hand, framed from the waist up, his face three-quarter to screen right toward her, never the lens; stunned, not smiling, his lips closed; {HANDS}; exactly two people",
         lines=[("qinshuang", "刀放下了。再動一下，槍頭就進你喉嚨。", "平靜，冷")],
         motion=f"Qin Shuang's spearhead whips up under the saber and knocks it out of his hand up out of the top of the frame, and the spearhead stops still just before his throat as she speaks; {quiet('Diao Qi')}",
         zh="中景、慢推（送 `-ye2-geng-l1`；加送 `prop-changqiang-l1`）：秦霜右手長槍第一格低平端著（跟長刀分開：長桿第一格分開），槍頭往上一挑、把刁七的長刀挑出畫面上方，槍尖停在他喉嚨前（一個連續動作；稿子『在空中翻一圈插進土埂』交給 s28 前景的插刀）；平靜地說；刁七嘴閉著、愣住、不笑（許硯不入鏡）。剪接從槍頭往上挑開始"),
    dict(loc="q2_r", cam="Wide shot, slow push in", chars=["erniu", "diaoqi"], night="night",
         comp=f"wide shot on the long ridge of dug earth, {SABER} standing stuck point-down in the earth soft in the lower foreground: in the middle, {DIAOQI}, already kneeling on the earth from the first frame, framed full figure with both knees on the ground, both his hands raised empty at his shoulders, a thick coat of white powder over his face, his face lowered, his lips closed, not smiling, never the lens; the small iron head of a long spear reaching in from the left edge, held still just before his throat; just behind him, {ERNIU}, standing, a coil of thick hemp rope in his hands, the rope already looped twice round the kneeling man's shoulders from the first frame, framed full figure, his face lifted three-quarter to screen left, never the lens; fierce and loud, {NOSMILE_ERNIU}, mouth wide between shouted words; {HANDS}; exactly two people",
         lines=[("erniu", "綁了！把刁七押去穀倉關起來！", "大嗓門")],
         motion=f"Wang Erniu hauls the rope tight with both hands and knots it behind the kneeling man's back, then lifts his face and shouts; {quiet('Diao Qi')}",
         zh="中遠景、慢推（全身：**跪姿拍到膝蓋**，站主 2026-11-22；送 `-ye2-geng-l1`）：前景長刀插在土裡（s27 挑飛的那把）；刁七第一格已經跪下、兩手舉在肩旁；二牛在他身後、麻繩第一格已經在他肩上繞兩圈，拉緊打結、抬頭大喊（一個動作）；秦霜只露從畫左伸進來的槍頭停在他喉前（不點名，不寫人）；刁七嘴閉著、不笑；二牛不笑（第二場結尾：喊聲傳到後門，切第三場）"),
    # ---- scene 3: the back gate at the same hour, then the channel at the first grey of dawn.
    dict(chapter="許家後門，再到天快亮的渠頭", loc="hm_d", cam="Medium shot, slow push in", chars=["aling", "xiaohe"], night="night",
         comp=f"medium shot at the narrow plank door standing ajar inward in the stone wall, the door's edge soft in the right foreground: {LAMP} standing on the ground just inside the doorway in the warm light; at the left of the doorway, {ALING}, {KNIFE} in her right hand held down at her side, standing side-on, framed from the waist up, her face in profile to screen left toward the dark alley, her eyes on it, her lips closed, not smiling, never the lens; at the right, peeking out round the edge of the door at waist height, {XIAOHE}, framed from the chest up, her small hand already clutching a fold of A-ling's skirt from the first frame, her face three-quarter to screen left, looking up toward the alley, never the lens; frightened, close to tears, not smiling: brows tilted up, lips trembling between words; {HANDS}; exactly two people",
         lines=[("xiaohe", "哥哥呢？哥哥是不是在外面打仗？", "快哭了")],
         motion=f"little Xiaohe tugs the fold of the skirt once and leans out to look down the alley as she speaks; {quiet('A-ling', 'her')}",
         zh="中景、慢推（送本集免費做的 `set-xujia-houmen-ye-men-l1`：往內半開的窄木板門、門內暖光、門左的柴堆；母圖 `set-xujia-houmen-ye-l1` 是滿月，接第 36 集）：門內地上一盞陶油燈（唐小棠那盞，稿子）；阿令在門口左邊側身、右手握一把**不出鞘的短刀**（聖經拍法 22 的固定句：刀鞘與刀柄一整塊深色木頭、一掌長；本篇只在這場），看著巷子、嘴閉著；小禾（抱草兔子：extras 照第 33 集寫成兔子塞在腰間布帶）從門邊探頭、拉一下阿令的裙角、往巷子看，快哭地說（→ 答在 s30）。唐小棠在門內、不入鏡（她的桶在 s32）"),
    dict(loc="hm_d", cam="Medium close-up, slow push in", chars=["aling"], night="night",
         comp=f"medium close-up of {ALING}, {KNIFE} in her right hand held down at her side, standing beside the narrow plank door, framed from the waist up, her face in profile to screen left, her eyes on the dark alley beyond the left edge of the frame, never the lens; she is the only person in the frame; cold and watchful, not smiling: eyes narrowed, brows level, lips moving low between words; the warm light from the doorway on one side of her face; behind her, soft, the rough stone wall and the stacked split logs in the moonlight; {HANDS}",
         lines=[("aling", "哥哥在渠頭。妳進去，把門閂上。", "低聲，沒回頭")],
         motion="A-ling, never turning her eyes from the alley, lifts her flat left hand back toward the doorway behind her in one small firm motion as she speaks low",
         zh="中近景（腰以上：手勢要在框裡）、慢推（送 `-men-l1`；稿子『身後只有泥牆與柿子樹』照圖：石牆與柴堆）：阿令不回頭、眼睛盯著巷子，左手平掌往身後的門口一擺（稿子『把小禾的頭按回門裡』：小禾不入鏡、不寫人，拍法 31），低聲說（答 s29）；不笑"),
    dict(loc="hm", cam="Wide shot, slow push in", chars=["aling"], night="night",
         comp=f"wide shot from beside the narrow plank door, like the picture: {BACKGATE}; the edge of the door soft in the right foreground; down the dark alley along the wall, eight raiders in ragged undyed homespun tunics and cloth head wraps, seen only as dark shapes against their own torchlight, already running up the alley toward the door from the first frame, three of them each holding up one burning torch, the man in front raising {STICK} over his head; at the right, just outside the doorway, {ALING}, {KNIFE} in her right hand, standing side-on, framed full figure, her face in profile to screen left toward them, never the lens; cold, not smiling: eyes narrowed, lips moving short and low between words; {HANDS}; exactly nine people, the eight raiders seen only as dark shapes",
         lines=[("aling", "進來一個，我就放倒一個。", "冷")],
         motion="the eight raiders slow and stop five steps from the door, and A-ling takes one step forward to meet them as she speaks",
         zh="全景、慢推（照圖；送 `set-xujia-houmen-ye-l1`：石牆從畫左遠處延進來、窄木板門在右往內半開、門左柴堆、黑巷子往左、光禿的樹、滿月）：巷子裡八個流寇（剪影、破布短褐；稿子照拍法 34 寫看得見的八個），三支火把每支一人，最前面一人舉一根素木棍（稿子『舉刀』：刀只寫刁七那一把，聖經〈小角色〉）；跑到離門五步停下，阿令往前站一步（稿子『短匕在指間翻一下』不拍：刀不出鞘），冷冷地說"),
    dict(loc="hm_x", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="night",
         comp=alone(f"{BUCKET} already swung back low in both her hands from the first frame, steam rising from it; beyond her, three steps down the dark alley, {RAIDER} seen only as a dark shape with his face in shadow, already rushing at the doorway from the first frame; beyond him the dark alley along the stone wall in the moonlight; she stays in the middle of the frame the whole shot; {HANDS}; exactly two people, the young woman in the middle seen only from behind, the raider only a dark shape",
                    "standing in the doorway of the narrow plank door, looking out down the dark alley,"),
         lines=[("tangxiaotang", "滾出去！許家的門，你們進不來！", "尖叫，咬著唇")],
         motion=f"she swings the bucket forward with both arms and the hot water flies out in one steaming sheet over the raider, who reels back with his arms over his face, only her arms moving; {HEADSTILL}",
         zh="中景（從背後）、慢推（送本集免費做的 `set-xujia-houmen-ye-xiang-l1`：從門口看出去的黑巷子、石牆、柴堆）：稿子 c32 唐小棠『咬著唇、不笑』正面潑水說話；真人版從背後拍（拍法 40：背影在正中、頭不動、兩顆丸子，l1 短襦，**不寫淡杏外衣**；mkspec 拿掉她的臉部圖、加雙丸子背影參考圖）：一只鐵箍木桶（冒熱氣）第一格已經往後盪低，兩手往前一甩、整桶熱水潑在衝到門前的流寇身上（他是黑影、臉在暗處：流寇近景只拍背影剪影），他捂著臉往後倒（一個動作；稿子『空桶往地上一放』交給 s34 前景的空桶）。她的話是錄音（尖叫）"),
    dict(loc="hm_x", cam="Medium shot, slow push in", chars=["aling"], night="night",
         comp=f"medium shot in the dark alley just outside the narrow plank door, the whole action inside the frame: at the right, {ALING}, {KNIFE} in her right hand, framed from the knees up, her face three-quarter to screen left, never the lens; cold and quick, not smiling, her lips closed; at the left, {RAIDER}, seen only from behind, already lunging at her with {STICK} raised over his head from the first frame; behind them the dark alley along the stone wall; {HANDS}; exactly two people, the raider seen only from behind",
         lines=[("erniu", "刁七綁了！你們的頭子綁了！", "很遠，大喊")],
         motion=f"A-ling ducks low under the stick and cracks the end of the dark wooden sheath across his wrist, and the stick drops from his hand to the ground; {quiet('A-ling', 'her')}",
         zh="中景（膝以上）、慢推（送 `-xiang-l1`）：整個動作留在畫面裡：第二個流寇（背影）第一格已經舉著木棍撲上來；阿令矮身閃過，用**刀鞘的一端**敲在他手腕上、木棍落地（拍法 22：不見刃；稿子『一腳把人踹回巷子』不拍，一鏡一個動作）；阿令嘴閉著。遠處二牛的喊聲是畫外錄音（加距離感；→ s34 流寇才跑）"),
    dict(loc="hm_x", cam="Wide shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="night",
         comp=alone(f"the empty wooden bucket bound with iron hoops standing on the ground beside her feet; her right hand already resting on the edge of the door frame at the right from the first frame; beyond her, down the dark alley, six raiders in ragged undyed homespun tunics seen only from behind as dark shapes, already turned and running away from the first frame, two of them each carrying one burning torch, and one torch lying burning on the ground of the alley; she stays in the middle of the frame the whole shot; {HANDS}; exactly seven people, the young woman in the middle seen only from behind, the six raiders only dark running shapes",
                    "standing in the doorway of the narrow plank door, looking out down the dark alley,", frame="framed from the knees up", shot="wide shot"),
         lines=[("tangxiaotang", "他們跑了……一個都沒進來。", "發抖，鬆一口氣")],
         motion=f"her right hand grips the door frame tight and her shoulders shake once as the six dark shapes run off down the alley, only her arm moving; {HEADSTILL}",
         zh="中遠景（從背後、膝以上）、慢推（送 `-xiang-l1`）：唐小棠背影在正中（稿子『站在門口、手還在發抖、退一步扶住門框』：從背後拍，右手第一格已經搭在門框上、抓緊、肩膀一抖）；腳邊是潑空的木桶（稿子『前景是地上的空木桶』）；巷子裡六個流寇背影轉身逃（每人一個黑影；兩支火把被帶走、一支扔在地上，三支對上 s31），她的話是錄音（← 因為 s33）"),
    dict(loc="q3", cam="Wide shot, slow push in", chars=["tangxiaotang", "xuyan", "qinshuang"], nospeak=["tangxiaotang"], night="dawn",
         comp=f"wide shot at standing eye height on the long ridge of dug earth at the first grey of dawn: a burnt-out torch lying on the earth soft in the near foreground, a thin pale curl rising from it; in the middle of the frame, seen only from behind, {TBACK_SMALL}, {LAMP} in her right hand, already stopped on the ridge from the first frame, framed full figure, facing straight away from us; a few steps beyond her, facing her, {XU_LIME}, framed full figure, his face toward her, his lips closed, never the lens; tired, not smiling; beside him at the right, {QIN}, {SPEAR} upright in her right hand with its butt on the earth, framed full figure, her face toward the young woman, her lips closed, never the lens; behind them on the ridge, three men in Song-dynasty homespun short jackets and cloth head wraps, a lean young man in a rust-red jacket, a broad young man in a dark charcoal jacket and a boy of about fifteen in a mustard-yellow jacket, each holding up {HOE}, the hoes well apart; beyond them the flat field under a thin drift of pale lime powder and the line of dark pines; {HANDS}; exactly six people",
         lines=[("tangxiaotang", "婦孺都在，一個不少，我數了兩遍。", "鬆一口氣，篤定")],
         motion=f"the three men lift their hoes high and cheer, and the young woman lifts her flat left hand out to the side toward the bank behind her, only her arm moving; {quiet('Xu Yan and Qin Shuang', 'their', plural=True)}; {HEADSTILL}",
         zh="全景、慢推（送本集免費做的 `set-shanjiao-qu-chen-l1`：清理過的夜景提亮成天快亮的灰藍、松樹上方一條灰白）：天快亮的渠頭：前景地上一支熄掉、冒一縷白的火把；唐小棠小背影在正中（不寫淡杏外衣；手提那盞油燈），第一格已經走到許硯面前停下，左手往身後的渠岸一擺（稿子『回頭指一下身後的人』：從背後拍不回頭）；許硯（袍子下半截一層石灰白粉，不寫泥）、秦霜（右手長槍、槍尾著地）面向她、嘴閉著；後面三個壯丁舉鋤頭歡呼（稿子『約四十個婦孺』不入鏡：s39 小禾從婦孺裡鑽出來，畫面上兩個婦人代表，拍法 34）。她的話是錄音。歡呼聲照站主 2026-11-21 用本集錄音倒放做（`crowd-murmur.py 37`）"),
    dict(loc="q3", cam="Medium shot over the shoulder, slow push in", chars=["qinshuang"], night="dawn",
         comp=f"medium shot over a shoulder at the first grey of dawn: {XU_EDGE_L}; beyond it, in the right half of the frame, {QIN}, standing on the long ridge of dug earth, {SPEAR} upright in her right hand with its head up and its butt just off the ground, framed from the waist up, a broad smear of pale powder across one cheek, her face three-quarter to screen left toward the man at the left edge, never the lens; quiet and serious, not smiling: eyes steady, brows level, lips moving softly between words; behind her, soft, the dry channel, the plank across it and the paddy in the grey light; {HANDS}; exactly two people, the one at the edge seen only in part",
         lines=[("qinshuang", "你一個字都沒改我的陣，也一步都沒退。", "聲音放輕，不笑")],
         motion="Qin Shuang thumps the butt of the spear down once on the earth and looks at him as she speaks softly",
         zh="過肩中景、慢推（送本集免費做的 `set-shanjiao-qu-chen-tian-l1`：渠、木板、秧田；加送 `prop-changqiang-l1`）：前景左是虛焦的舊灰外衣肩（許硯，不點名、不送圖）；秦霜右手長槍直立、臉頰一大片淡淡的白粉（不寫細點，拍法 12），槍尾往地上一頓（一個動作；稿子『槍尖朝下』改成槍頭朝上直立再頓地：槍頭朝下會碰到地、長桿第一格要分開），看著他、放輕聲音說（不笑；好感 +7 的原因）"),
    dict(loc="q3", cam="Close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"close-up of {XU_LIME}, standing on the long ridge of dug earth at the first grey of dawn, framed from the chest up with space above his head, a smear of pale powder on his cheek, his face three-quarter to screen right {off('right', 'the pale grey-white sky over the dry channel')}; worn out, a faint tired smile, eyes soft, lips moving gently between words; behind him, soft, only the pale grey-white sky low over the far pines; {HANDS}",
         lines=[("xuyan", "陣是妳排的，我只負責站著別跑。", "累，淡淡一笑"), ("xitong", "叮。秦霜好感，加七。", "冷")],
         panel=[("秦霜 好感 +7 → 48", "affection")],
         motion="Xu Yan wipes the powder off his cheek with the back of his right hand and gives her a small tired smile as he speaks, then his lips close",
         zh="近景、慢推（送本集免費做的 `set-shanjiao-qu-chen-zhuo-l1`：灰白天下的乾地與松樹；稿子『身後只有天邊的灰白』）：許硯用手背抹掉臉上的灰、對她淡淡一笑（稿子：累、淡淡一笑，這鏡可以笑），朝畫右外看不到的人（秦霜，不點名）說（答 s36），說完嘴閉著，系統是錄音；**不寫淡藍光**（拍法 11）；面板『秦霜 好感 +7 → 48』剪接時疊（系統念加值、總值只在面板，聖經〈好感帳〉）"),
    dict(loc="q3", cam="Close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"close-up of {XU_LIME}, standing on the long ridge at the first grey of dawn, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes already turned back along the ridge beyond the left edge of the frame from the first frame, never the lens; he is the only person in the frame; spent and quiet, not smiling: brows easing, lips pressed shut; behind him, soft, only the dry channel and the paddy in the grey light; {HANDS}",
         lines=[("xitong", "叮。任務完成。", "冷，宣布")],
         panel=[("任務完成", "task")],
         motion=f"Xu Yan lets out one long slow breath, his shoulders sinking; {SILENT_HE}",
         zh="近景、慢推（送 `-chen-tian-l1`；稿子『身後只有渠岸』）：許硯第一格已經回頭望向畫左外的土埂（稿子『回頭看一眼所有人』：寫地方，不寫人），慢慢吐一口氣、肩膀放下（一個動作）；系統是錄音、**全程嘴閉著**；面板『任務完成』跟系統念的一字不差"),
    dict(loc="q3", cam="Wide shot, slow push in", chars=["xuyan", "xiaohe"], nospeak=["xiaohe"], night="dawn",
         comp=f"wide shot on the long ridge of dug earth at the first grey of dawn: at the right, {XU_LIME}, already down on one knee on the earth from the first frame with both arms spread wide, framed full figure with his knee on the ground, his face three-quarter to screen left toward her, his lips closed, never the lens; tired, a soft look in his eyes; at the left, {XIAOHE}, already running toward him from the first frame, framed full figure, small, her face three-quarter to screen right toward him, never the lens; mouth wide on one shouted word; behind them, soft, two women in faded homespun jackets and head cloths, one in dark grey and one in rust-red, standing on the bank, seen side-on; {HANDS}; exactly four people",
         lines=[("xiaohe", "哥哥！", "短喊")],
         motion=f"little Xiaohe runs three steps and throws herself into his arms with a cry, and Xu Yan catches her; {quiet('Xu Yan')}",
         zh="中遠景（全身：**跪姿拍到膝蓋**，站主 2026-11-22）、慢推（送本集免費做的 `set-shanjiao-qu-chen-geng-l1`：灰白光裡的土埂；稿子的跟拍改慢推）：許硯第一格已經單膝跪下、張開兩手；小禾（草兔子塞在腰間）第一格已經從婦孺裡跑出來，跑三步撲進他懷裡（一個動作）、短喊（`nospeak`，構圖寫嘴張開喊一個字：稿子『短喊寫成張嘴喊』）；許硯嘴閉著、接住她；背景兩個婦人（婦孺的代表，拍法 34）。剪接剪在撲進懷裡的一半"),
    dict(loc="q3", cam="Medium close-up, slow push in", chars=["xuyan", "xiaohe"], night="dawn",
         comp=f"medium close-up at the first grey of dawn: {XU_LIME}, crouching low on the long ridge, framed from the chest up, holding in his arms {XIAOHE}, already limp from the first frame, her head fallen back over his left arm, her eyes closed, her arms limp at her sides, her whole face deep red with fever, strands of hair stuck to her forehead; his face lowered to her, never the lens; terrified, not smiling: brows knotted hard together, eyes wide, lips moving fast between words; behind them, soft, only the long ridge and the pale grey sky; {HANDS}; exactly two people",
         lines=[("xuyan", "小禾？小禾！妳的臉怎麼燙成這樣？", "慌")],
         motion=f"Xu Yan cradles the back of her head in his left hand and lays his right palm on her forehead, then jerks the hand back as he speaks; {quiet('little Xiaohe', 'her')}",
         zh="中近景、慢推（送 `-chen-geng-l1`；稿子『從中近景推到近景』）：許硯蹲著（不是跪，胸以上）抱住小禾，她第一格已經軟下來：頭往後仰在他左臂上、眼睛閉著、手臂垂下、整張臉燒得通紅（一大片，不寫細點）、額前髮絲黏著；他左手托住後腦、右手掌按她額頭、猛地縮回（一個動作），慌張地說（本集結尾；懸念 → 第 38 集第一場：病房，小禾躺在床上）。**原版必修**：許硯喊『小禾？小禾！』時咧嘴笑 → 不笑：眉頭擠緊、眼睛睜大、嘴張開（聖經〈原版必修〉）。配樂全部收掉，只剩一個低音"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e037-r2/script.md`（c01–c40 對應 s01–s40，加兩個拆鏡 s09b、s16b，共 42 鏡；含「這版改了什麼」「2026-11-06 審稿後的修改」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e031-e040.md`（拍法 1–43 條、〈場景〉〈接點〉〈道具〉〈小角色〉），帳照 `r2-bible-e011-e060.md`。**第 4 篇章〈旱年〉第 7 集**：約第一七五天夜三更（許家院子，接第 36 集同一刻）→ 四更到天快亮前（新渠渠頭；許家後門同一時間）→ 天快亮（渠頭）。",
    "- 內部工作編號 937（`hailuo/{ff,clips}-dh-e937.json`；`colab/runs/e937/extras.json`、`colab/runs/e937-live/spec.json`、工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e937-dh/`）；發布 slug `zhong-tian-qu-qi-e037-r2`。不放集數、不放片名卡；**s01 接第 36 集定版成片 `e936-live.mp4`（200.84 秒）的最後一鏡**（s38 許硯在畫左提油燈朝右上望、唐小棠背影抓他右袖；s36 滿月；s31 草蓆在樹與井之間）；s40 交給第 38 集（同一個清晨，病房）。",
    "- 照第 36 集的審稿、成片審查與終驗的教訓一開始就照做：參考圖跟文字一致（本集的新圖都是免費清理、裁切與調色、新 id；渠的夜景用清掉護欄、直立木板、地平線方塊與細月的 `-ye2`）；門寫明推開或半開（院門、後門照圖）；許硯不寫鬍渣；風格句不寫 cinema camera；不寫 crowd、hundreds，寫實際人數，`exactly N` 寫在構圖、`only` 句再寫一次（多一人常見）；不寫泥（石灰寫白粉）；`OFFSCREEN_SPEECH = False`、對畫外的人說話寫「朝畫左／右外看不到的人」；不寫 open、不寫否定名詞；長東西第一格分開（鋤頭、竹竿、長槍、長刀）。",
    "- **站主 2026-11-21～23 規則**（PR #2217，`production/OWNER-CHECK-20261122.md`）：品質優先；唐小棠背影鏡加送雙丸子背影參考圖 `refs-live/tangxiaotang-back-shuangji-e929-w3.png`（mkspec）；跪姿拍到膝蓋（s28、s39 全身）；人群聲（s35 歡呼、流寇喊殺）用本集錄音倒放 `colab/runs/_scripts/crowd-murmur.py 37`；音效用 `zhongtian-music-library/_sfx-zhongtian-real-20261121/`；柴刀本集不寫（舊柴刀句會畫成劍的問題不會出現）。",
    "- **人物**：**唐小棠**（拍法 3、4、20、40）：說話的 s32、s34、s35 從背後拍、s08 是她兩手抓袖子的插鏡（錄音），不說話的 s07、s09 背影不點名；l1 交領短襦，**不寫 t2 高立領、不寫淡杏外衣**；**本集沒有她的正臉**。**秦霜**：柴刀不寫（拍法 5；稿子 c13 交柴刀不拍）；s26 起一桿長槍（送道具圖 `prop-changqiang-l1`）。**阿令**：第三場右手一把不出鞘的短刀（拍法 22），用刀鞘敲手腕。**二牛**：報壞消息、喊、綁人，每鏡逐部位寫不笑。**刁七**（第一次出場）：送 `diaoqi-portrait-l1`，破布短褐、黑綁腿、舊疤，**不穿皮甲**（extras）；長刀只在 s18–s28。**小禾**：s29 探頭、s39 撲進懷裡、s40 發燒昏倒。流寇只拍背影、剪影、遠處黑影；刀只有刁七一把、槍只有一桿。",
    "- **軸線（照圖）**：院子照 `set-xujia-yuan-ye-dong2-l1`（拍法 42）：屋與屋門在**左**、柴堆在屋前、院門在後牆**中間**（門扇推開靠左柱）、井在前右、草蓆在樹與井之間；二牛從院門朝鏡頭跑進來、秦霜從後牆右段跳下。渠頭照清理過的夜景 `set-shanjiao-qu-ye2-l1`：乾渠往深處、**左岸那道新土堆＝稿子的土埂**（上面一堆乾草），土埂外的乾地延到**左邊遠處松樹**（流寇從那裡過乾地衝來）；守的人在土埂上**面向左**，淺坑挖在土埂前的乾地；前排秦霜在左、許硯在她右邊。後門照 `set-xujia-houmen-ye-l1`：窄木板門在**右**、往內半開，巷子往**左**；唐小棠與阿令在門口面向左、流寇從左邊巷子來。",
    "- **時間與光**：第一場夜三更冷月光加油燈（第 36 集同一刻）；第二場四更到天快亮前，冷月光、滿天小星（圖上的細月已塗掉：第 36 集是滿月），s17 起流寇的火把橘光、s21 起白色石灰煙；第三場後門同一時間、滿月（圖上）、門內暖光、三支火把；s35 起天快亮的灰藍（本集免費做的 `-chen`）。時間跳都在剪點（s09b→s10、s16b→s17、s28→s29、s34→s35）。",
    "- **原版必修**：許硯喊『小禾？小禾！』不笑（s40：眉頭擠緊、眼睛睜大、嘴張開）。原版建議：唐小棠『那你站哪』不笑（s08 改插鏡）、後門提桶不笑（s32 從背後）；『火把全滅了』之後不再出現一隊亮著的火把（後門只有三支、另一條路）；刁七不穿皮甲。",
    "- 要買的秒數（BUY，錄音前照第 35、36 集實測估：一句 6 秒的鏡放得下約 5.9 秒人聲、8 秒約 7.3 秒；第 36 集量到許硯約 4 字／秒、唐小棠中位 3.4、阿令 3.4、秦霜約 3.7、系統 9 字約 2.4 秒；二牛、小禾、刁七照第 31–35 集估）：**8 秒** s04、s06、s09（許硯 18–20 字）、s05（秦霜 18 字兩句）、s24（二牛 17 字喊）、s27（秦霜 15 字＋挑槍的動作）、s37（許硯 13 字＋系統 9 字）；**5 秒** s09b、s17、s21（無台詞）、s20（『扔！』）、s39（『哥哥！』）；其他 6 秒。錄音後照 `span937.sh` 重核。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音的人聲長度為準。",
    "- **渠（s10–s28、s35–s40）表上的提示詞帶「below the deep pool」**：只為了讓 `gen-dh` 的 `SET` 選到深潭那張圖（再由 `spec.json` 換成渠的圖），d1 由 `mkspec.py` 拿掉；**之後每個 fix／retake spec 都要帶同一組替換**。院子與後門的提示詞帶「night yard of the Xu farmhouse」讓 `SET` 選到 `set-xujia-yuan-ye`（l2），`spec.json` 換成 `-ye-dong2`、`set-xujia-houmen-ye` 與它們的裁切（`gen-dh` 自己的後門字會選到沒有真人圖的 `set-houmen`）。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯 l1、angle-a（帶笑的 angle-b 整集不送；全景 s04、s09b、s10、s35、s39 只送 l1）；唐小棠她的三張臉部圖全集都拿掉（沒有正臉），背影鏡（s07、s09、s32、s34、s35）加送雙丸子背影參考圖；阿令、秦霜、二牛、小禾、刁七見 `colab/runs/e937-live/mkspec.py`；秦霜拿長槍的 s26、s27、s36 加送 `prop-changqiang-l1`。過肩前景的背影（s06 秦霜、s14、s25 許硯的肩、s36 許硯的肩）、流民、壯丁、流寇、婦人都不送圖。",
    "- **場景圖**：院子送第 31 集的 `set-xujia-yuan-ye-dong2-l1`（s09b）、第 36 集的 `-zhong`（s01）、`-qiang`（s04、s05）、`-chai`（s06、s09）、`-wu`（s07）與本集免費做的 `-shu`（s02、s03）、`-di`（s08 插鏡，只當地面）；渠送本集免費做的 `set-shanjiao-qu-ye2-l1`（s10、s13）、`-ye2-geng`（s12、s24、s26、s27、s28）、`-ye2-zhuo`（s11、s14、s17、s18、s21、s22、s25）、`-ye2-tian`（s15、s16、s16b、s19）、`-ye2-kong`（s20）、`-ye2-cao`（s23 插鏡）；後門送 `set-xujia-houmen-ye-l1`（s31）與本集免費做的 `-men`（s29、s30）、`-xiang`（s32、s33、s34）；天快亮的渠送 `set-shanjiao-qu-chen-l1`（s35）、`-chen-tian`（s36、s38）、`-chen-zhuo`（s37）、`-chen-geng`（s39、s40）。",
    "- **本集新做的圖**（2026-11-23，`live-action/free-e031-e040/`，各跑兩次逐位元一樣，寫進 refs-live README）：`shanjiao_qu_ye_clean.py`＋`shanjiao_qu_ye_e937.sh`（渠的夜景清理、五張裁切、天快亮的調色與三張裁切）、`xujia_houmen_e937.sh`（後門兩張裁切）、`xujia_yuan_ye_e937.sh`（夜院子兩張裁切）。**不花錢**；沒有付費圖。",
    "- **還缺、先用最接近的圖**（不花錢、註明在這裡）：(1) **渠頭沒有一道橫過渠的土埂、沒有閘板**：圖上左岸那道新土堆當土埂，台詞的『閘板』是渠上的木板（直立平木板已塗成細樁，平板會長字）。(2) **圖上沒有山**：流寇從松樹那頭來，火光寫成從松樹流出（拍法 37 的變體）。(3) 夜院子、後門偏 CG（第 31 集、試鏡第一輪的圖）。(4) 石灰袋、竹竿、木棍、鋤頭、長槍、長刀、麻繩、木桶、油燈、火把是文字加在圖上（長槍另送道具圖）。",
    "- 共用檔：`build-r2.py` 的 `EN` 加一個鍵 `diaoqi`（刁七第一次在畫面上說話；只加鍵，舊集逐位元重建不變）；`gen-dh.mjs`、`pilot.py`、`cast.json` 不動。對畫外說話、對地方說話的鏡，精修文字的通用說話視線由本檔結尾的 `live_clips()` 換成 d1 的方向句（`GAZE_REFINE`）；唐小棠的背影鏡：立領句拿掉、名字換成「從背後看的年輕女子」（同第 31、33、35、36 集）。",
    "- **自審**（2026-11-23，`writer-tools/e037-r2/review.md`，不是獨立審稿）；給獨立審查者的提示在 scratchpad `e937prep/review-prompt.md`，由協調者派。",
    "- **d1 前置**（2026-11-23，`colab/runs/e937-live/PREP.md`）：`colab/runs/e937/extras.json`、`colab/runs/e937-live/{mkspec.py,spec.json}`（種子 9371101／9371102）、scratchpad `tools/prep937.sh`、`tools/rec937-slow.sh`（錄音）、`e937d1.sh`（Colab，**沒跑**）。",
    "- 配樂：第一場緊張的低音鼓，s03 面板一個重音；第二場低沉鼓點越來越近，s19『等』全部收掉只剩呼吸，s20『扔』一個大重音，s27 挑刀一個重音；第三場後門短鼓點，s33 二牛的喊聲後轉輕，s35 起溫暖的勝利旋律，s40 全部收掉只剩一個低音。音效見 script.md〈音樂與音效〉，從 `zhongtian-music-library/_sfx-zhongtian-real-20261121/` 挑（站主 2026-11-21）；人群聲用 `crowd-murmur.py 37`。",
]

# Seconds to buy, estimated from e935 / e936's measured lines (e936 PREP §4): a 6 s shot holds about 5.9 s of speech, 8 s about
# 7.3 s; Xu Yan about 4 characters a second (thoughts 4-4.3), Tang Xiaotang median 3.4, A-ling 3.4, Qin Shuang about 3.7, the
# system 9 characters in about 2.4 s; Wang Erniu fast and loud (about 4.5), Xiaohe and Diao Qi first measured here.
# 8 s: s04 (Xu 20), s06 (Xu 17 in three phrases), s09 (Xu 16 in two sentences, with the hand-over), s05 (Qin 18 in two
#      sentences), s24 (Erniu 17 shouted in two), s27 (Qin 15 in two sentences after the flick), s37 (Xu 13 + system 9).
# 5 s: s09b, s17, s21 (no line), s20 (one shouted word), s39 (one shouted word).
# 6 s: every other spoken shot.
BUY = {"s04": 8, "s05": 8, "s06": 8, "s09": 8, "s24": 8, "s27": 8, "s37": 8,
       "s09b": 5, "s17": 5, "s20": 5, "s21": 5, "s39": 5,
       "s01": 6, "s02": 6, "s03": 6, "s07": 6, "s08": 6, "s10": 6, "s11": 6, "s12": 6, "s13": 6, "s14": 6, "s15": 6, "s16": 6,
       "s16b": 6, "s18": 6, "s19": 6, "s22": 6, "s23": 6, "s25": 6, "s26": 6, "s28": 6, "s29": 6, "s30": 6, "s31": 6, "s32": 6,
       "s33": 6, "s34": 6, "s35": 6, "s36": 6, "s38": 6, "s40": 6}


# ---- the refine text (as e031, e033, e935, e936): hailuo/clips-dh-e937.json column 0 is the motion text refine-prep.py sends
# with a picked d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era "Tang Xiaotang's high stand-up
# collar stays closed at her throat." and names her in "<names> shown in <Picture 1>"; in a back shot that draws the collar back
# and turns her face to the lens. Her back shots: the sentence goes and her name becomes "the young woman seen only from behind".
COLLAR = "Tang Xiaotang's high stand-up collar stays closed at her throat. "
FRONT_TANG = set()
GAZE_GEN = {"he": "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person",
            "she": "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"}
# sid -> (pronoun, the direction sentence): the listener is out of frame, or the speaker looks at a place
GAZE_REFINE = {
    "s01": ("he", "turned toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
    "s02": ("he", "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
    "s05": ("she", "her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, her eyes on that spot"),
    "s10": ("he", "turned three-quarter to screen left toward the ridge at his feet, his eyes on the next spot on the ridge"),
    "s11": ("he", "his face lowered three-quarter to screen right, his eyes on the pit before him"),
    "s14": ("she", "her face three-quarter to screen left, her eyes on the dark field, never on the man at the edge"),
    "s15": ("he", "his face three-quarter to screen left, his eyes on the dark field beyond the left edge of the frame"),
    "s18": ("he", "his face three-quarter to screen right, his eyes on the ridge ahead of him"),
    "s19": ("she", "her face three-quarter to screen left, her eyes on the firelight beyond the left edge of the frame"),
    "s22": ("he", "turned toward the right of the frame, his eyes on the white smoke before him"),
    "s24": ("he", "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
    "s28": ("he", "turned three-quarter to screen left, his eyes on the ridge beyond the left edge of the frame"),
    "s29": ("she", "turned three-quarter to screen left, her eyes on the dark alley"),
    "s30": ("she", "her face in profile to screen left, her eyes on the dark alley beyond the left edge of the frame"),
    "s37": ("he", "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"),
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
                names = [n for n in re.split(r", | and ", m.group(1)) if n != "Tang Xiaotang"]
                who = " and ".join(names + [BACK_NAME]) if len(names) < 2 else ", ".join(names) + f" and {BACK_NAME}"
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
# live_clips() writes no longer matches it. prep937.sh hands stage 1 the anchor form of the live file (this), then puts the
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
