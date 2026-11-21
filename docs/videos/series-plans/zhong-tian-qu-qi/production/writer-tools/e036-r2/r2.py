"""Episode 36 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e036-r2/script.md
(c01-c38; the CG-era r2 script), including its sections 「這版改了什麼」 and 「2026-11-06 審稿後的修改」, which override the tables.
Every line is the script's, word for word; only the staging changes. 40 shots: one per script shot (sNN = cNN) plus two splits
that keep one visible action and one breath per shot (s11b: the third line of c11's thought / system / thought exchange, about
11 s of speech that a 10 s clip cannot hold; s12b: Xu Yan's answer after A-ling's line in c12; build-r2.py's `sid`).
Bible: production/r2-bible-e031-e040.md (arc 4 〈旱年〉: rules 1-43, 〈場景〉, 〈接點〉 35->36 (corrected 2026-11-20 from e935's cut)
and 36->37, the props (the gate and its crossbar, the bamboo tallies, A-ling's brush and register, the straw mats, Xu Yan's clay
oil lamp; Qin Shuang's chopper NOT written, rule 5), people, 〈小角色〉 (the refugees, the three spies: feet, hands and backs
only) and 原版必修 (e036: none; the yard by rule 42; the spies feet, hands, backs)) and r2-bible-e011-e060.md (accounts: no
affection change, Tang Xiaotang 45, Qin Shuang 41, A-ling 32; the grain lasts two months; one hoe of digging, one bowl of rice).
The sixth episode of arc 4: dusk at the village gate (day 160, the same moment as e035's last shot), the new channel from the
first day of digging (day 161) to half a month later (day 175, dusk), and the yard that night at the third watch.

Written from the start the way e035-r2/r2.py stands AFTER its independent review and its cut (writer-tools/e035-r2/
review-independent.md; colab/runs/e935-live/{picks-merged.tsv,fix1-fix4/plan.md,final-check.md}; PREP.md §7, §8) and the task
file's lessons:
- The pictures agree with the words: every place sentence follows the picture it sends; every crop is a free id made for this
  episode (live-action/free-e031-e040/{shanjiao_qu.sh,xujia_yuan_ye_e936.sh,cunkou_zha2_e936.sh}) or e035's crops of the same gate.
- The gate (e935 fix1 s34, fix3 s32: H3 swung the leaves back by itself twice): where the gate must stay shut (s01) the result is
  written first and twice: the two leaves closed from the first frame to the last, the firelight only through the gaps. After
  s02 the gate is swung back: no later shot sends a picture whose gate leaves are shut across the frame (s06, s07, s09, s12b send
  -wai, the gate's post only at the left edge).
- Qian Yuanwai (e934 s30/s32, e935 s23/s24: a front face meant to be sour or stunned smiled in every take; e934 fix4 and e935
  fix4 turned him into a back walking away over his recording, which worked): he speaks to the lens's side only where he shouts
  (s03, s04, s26: furious, written feature by feature) or sneers (s10, the script's 冷笑); c28's 「咬牙」 exit is his back from
  the start (s28: no picture, no name, the costume sentence; his line a recording).
- Xu Yan has no stubble word (e934 s33); the clean sentence's "clear and still" is replaced per shot (mkspec.py); no mud (e032
  fix3; the script's 「袍子下半截沾泥」 is pale dust on the hem); no negated nouns (rule 18); long things never touch in the first
  frame (the hoes, the crossbar, the brush and the paper).
- No collective noun (rule 34): the hundred refugees are eight walking in (s02), seven before the stone (s09); the forty diggers
  are eight (s13); six going home (s29); nine asleep on twelve mats (s31). "exactly N people" everywhere.
- OFFSCREEN_SPEECH = False (rule 15); rule 31: a line to someone out of frame is written "toward someone out of sight beyond the
  left/right edge of the frame", that side set only, the speaker the only person; GAZE_REFINE puts the same direction into the
  refine text. A look at a thing names the thing (the gateway, the paper, the top of the wall, the far hills).
- No blue light (rule 11): the panel of s29 is the editor's.
- No word "open" (rule 36): the gate leaves are "swung back".
- Tang Xiaotang (rules 3, 4, 20, 40): every line of hers is said from behind (the middle of the frame, head still, exactly two
  buns, her l1 cross-collared jacket, no outer coat, no stand-up collar: e935's alone() and TBACK) or over another picture (s05
  the gold abacus insert, rule 20's "only in an insert"; s16 A-ling at the table). Her pictures and identity sentence leave
  (mkspec.py). She has NO front face this episode (rule 40 allows two; the script gives her no silent reaction that needs one).
  Her over-the-shoulder backs (s06, s12b) and her small back (s01) are unnamed, with no picture.
- Qin Shuang (rule 5): her chopper is never written (extras.json takes it out of her cast sentence); c24's 「手按柴刀柄」 is her
  hand on her wide plain leather belt, c30's 「把柴刀往腰帶裡推緊」 is her pulling the belt tighter.
- A-ling (rule 22): her short knife belongs to e037 only; c37's 「按住袖裡的短匕」 is her right hand sliding into her left sleeve.
- Paper and brush (rules 7, 27, 38): the register is plain blank paper, soft at the lower edge; the brush tip is lifted just
  above it and never makes the stroke (c16, c17); the script's ledger in Qian Yuanwai's retainer's hands (c26) is not written
  (he slams his flat hand on the table instead). The bamboo tallies are "smooth and plain".

THE AXES (rules 29, 42: the pictures decide):
- The village gate (set-cunkou-zha2-l1, e935's paid edit, and its crops): the gate of two log leaves under a small tiled roof at
  the LEFT, the willow in the middle, the plank bridge over the dry ditch, the road to three houses at the RIGHT. The camera is
  inside the village (e935 s26-s35). 35->36 from e935's cut (bible 〈接點〉, corrected 2026-11-20): s34 Xu Yan before the closed
  gate, A-ling at his LEFT in the same row, Tang Xiaotang at his right a little behind, the two guards (dark teal, deep wine-red)
  one at each end of the crossbar, each holding a torch; s35 his right hand on the crossbar at the iron fitting of the seam.
  s01 is that moment: he lifts the crossbar. There is no gate tower: Qian Yuanwai stands on the low earthen mound beside the gate
  (e935 s31, the script's own fallback), a low angle against the gate's roof (s03, s04, s10).
- The new channel at the foot of the hills (set-shanjiao-qu-l1, round 4, 37044; the bible's 「不是第 34 集那條引水渠」): the dry
  channel runs straight from the foreground AWAY into the distance (the script's 「由右往左」 is depth in the picture); on its
  LEFT bank a long mound of dug earth and a heap of straw, beyond it the flat dry yellow field and a line of dark pines (the
  script's foot of the hills); a plank across the channel on a short upright in the middle distance; on the RIGHT bank dry grass
  and the green paddy (the three mu). The long account table stands on the flat ground of the left bank (Tang Xiaotang at its
  right end, A-ling at its left end); Qin Shuang comes along the paddy on the right bank (s21-s25: they talk on the right bank);
  the spies dig at the far end (渠尾).
- The yard by night (set-xujia-yuan-ye-dong2-l1, e931's): the house and its doorway at the LEFT with the woodpile against its
  front, the yard gate in the MIDDLE of the back wall, the bare tree right of the gate, the low back wall running RIGHT from the
  gate, the well in the front RIGHT. Rule 42: the row of straw mats lies along the foot of the RIGHT stretch of the back wall
  (the script's 「東牆」); Qin Shuang sits on the woodpile, crosses to that wall and crouches on its top facing the hills (her back
  to us); Xu Yan comes from the house door at the left to the middle; A-ling stops on the doorway's threshold; Tang Xiaotang
  grips his right sleeve (on his right). The script's 「井在左前、井沿蹬牆」 is the other way round: the well is in the front right,
  away from the wall, and she is already up on the wall top (s33).

PLACES (gen-dh SET takes the FIRST pattern in its list order that matches the prompt):
- The gate: every LOC opens "At the village entrance" -> dh-set-cunkou-t1 = pilot.py's newest set-cunkou (l1, the old palisade,
  never sent), which spec.json swaps for set-cunkou-zha2-men-l1 (s01, the shut gate), and after the independent review the free
  crops with no shut gate leaves -ding2 (s03, s04, s10), -wai2 (s02 until the paid open-gate picture -kai is picked, s06, s07,
  s12b), -dao (s08, s09, s12), -kong (s11, s11b) and -di (s05, the insert).
- The channel: the LOC carries " below the deep pool" (POOLMARK) only so gen-dh sends set-shentan (set-xinqu, which "new channel"
  would take, has no live picture and pilot.py would stop), which spec.json swaps; mkspec.py takes the words out of every d1
  prompt, as e034 / e035's fields. After the independent review the cleaned picture set-shanjiao-qu-jing-l1 (s13: the guard rail
  painted out, the upright board turned into a thin post) and its crops -zhuo2 (s14, s16, s18, s19, s20, s26, s27, s28), -tian2
  (s21, s24), the new dusk grade -xi2 (s29) and -xi2-zhuo (s30); -an (s23, s25) and -di (s15, s17, s22) as they were.
- The yard: every LOC opens "In the night yard of the Xu farmhouse" -> dh-set-xujia-yuan-ye-t1 = pilot.py's newest
  set-xujia-yuan-ye (l2, never sent), swapped for set-xujia-yuan-ye-dong2-l1 (s31) and the free crops -qiang (s32, s33, s35),
  -chai (s34), -shan2 (s36, review 建議 8), -wu (s37), -zhong (s38).
Shared files: none changed (build-r2.py's EN has every speaking name; gen-dh.mjs, pilot.py, cast.json untouched). The d1 prep
(colab/runs/e936/extras.json, colab/runs/e936-live/{mkspec.py,spec.json,PREP.md}, the scratchpad's tools/prep936.sh, rec936.sh
and e936d1.sh) was written 2026-11-20.
"""
EP = 936  # internal working number; the published slug is zhong-tian-qu-qi-e036-r2
SLUG = "zhong-tian-qu-qi-e036-r2"
EP_TITLE = "一鋤頭換一碗飯（重製版 r2）"
OUTLINE_SECONDS = 194.5  # script.md: about 194.5 s, 38 shots (12 + 18 + 8)
TARGET_MINUTES = [3, 4]
TITLE = "開門！一鋤頭換一碗飯，挖渠的流民裡混進三雙新鞋｜種田娶妻打天下 第36集（重製版）"
DESCRIPTION = "柵門外是一百多個鄰村的流民，錢員外在土台上喊：許硯，你瘋了！許硯抬起門閂：進來的人都有飯吃，但是每個人都要幹活。唐小棠撥完算盤——連上流民，糧只夠撐兩個月。那就挖一條渠，一鋤頭換一碗飯，誰也不白吃。阿令說名冊她來寫，字工整得像宮裡發出來的帖子；許硯只說：妳不想說，我就不問。秦霜卻盯上了渠尾三個人：逃荒的人草鞋都磨破了，哪來的新鞋？錢員外的米一夜跌了一半，半個月後渠挖到山腳。當夜三張草蓆空了，山上傳來鼓聲，一長串火把正往村子流下來。《種田娶妻打天下》第 36 集（重製版）。"
THUMB = ("三雙新鞋", "s22")
CHARACTERS = ["xuyan", "tangxiaotang", "aling", "qinshuang", "qianyuanwai", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: low strings at an orange dusk village gate turning warm and wide as the gate swings back, one heavy accent on a promise; then a brisk working rhythm of drums and hoes on a dry new channel, one soft guqin note for a quiet woman's brush, low suspense strings from a whisper about three strangers, one bright accent at dusk; then near silence and night insects in a dark yard, distant drums rising, one great accent held unresolved at the peak; ancient Chinese rural drama, no vocals"

# Places.
K1 = "At the village entrance of Liuxi at dusk five days after the swarm night"
DUSK = "a warm orange-red evening sky, the sun just gone below the far hills"
GATE_SHUT = ("the two closed gate leaves of upright logs under the small tiled roof, a narrow seam down the middle, the thick crossbar "
             "at waist height across both leaves held by a plain iron fitting at the seam")  # set-cunkou-zha2-l1 (e935 建議 1)
POOLMARK = " below the deep pool"  # mkspec.py takes it out of every channel shot in d1 (gen-dh's SET needs "deep pool")
Q1 = f"At the new channel at the foot of the hills outside Liuxi{POOLMARK} in the morning of the first days of the digging"
QDAY = "clear white morning light, a pale blue sky"
Q2 = f"At the new channel at the foot of the hills outside Liuxi{POOLMARK} at noon some days later"
QNOON = "hard white noon light from high above, short shadows"
Q3 = f"At the new channel at the foot of the hills outside Liuxi{POOLMARK} in the afternoon some days later"
QAFT = "bright afternoon light from the right, a pale blue sky"
Q4 = f"At the new channel at the foot of the hills outside Liuxi{POOLMARK} at sunset half a month after the digging began"
QXI = "warm low amber evening light from the right, the sky glowing orange above the far pines"  # -xi2 (review 建議 7)
CHANNEL = ("a freshly dug dry channel about knee-deep, wide and flat-bottomed, running straight from the foreground away into the distance, its bed bare "
           "cracked dry earth; on the left bank a long mound of dug brown earth and a heap of dry straw, beyond it a flat dry yellow "
           "field and a line of dark pines at the far left; a single plank laid across the channel on one thin wooden post in the "
           "middle distance; on the right bank a strip of dry grass and a green paddy of young rice")  # set-shanjiao-qu-l1
TABLE = "one long plain wooden table standing on the flat dry ground of the left bank"
N1 = "In the night yard of the Xu farmhouse at the third watch of the night half a month later"
NIGHT = "cool pale moonlight from above, the yard dark and still, a faint warm glow along the house wall at the left"
YARD = ("the farmhouse on the left with its dark doorway at the far left and split firewood stacked against its front, the yard gate "
        "under its small tiled roof in the middle of the back wall, a bare tree just right of the gate, the low earth-and-stone back "
        "wall running from the gate to the right edge, the round stone well with its wooden windlass in the front right, a wooden "
        "bucket in the middle of the yard, dark fields and far dark hills beyond the wall")  # set-xujia-yuan-ye-dong2-l1
LOC = {
    "kk_g": f"{K1}, by the gate; {DUSK}",
    "kk_in": f"{K1}, just inside the gate; {DUSK}",
    "kk_e": f"{K1}; {DUSK}",  # the insert s05: mkspec.py leaves only "Insert close-up" (rule 35)
    "q1": f"{Q1}: the channel exactly as in the picture: {CHANNEL}; {QDAY}",
    "q1_t": f"{Q1}, by the long plain wooden table on the left bank; {QDAY}",
    "q1_e": f"{Q1}; {QDAY}",  # the inserts s15, s17: only "Insert close-up"
    "q2_b": f"{Q2}, on the strip of dry grass along the right bank beside the green paddy; {QNOON}",
    "q2_e": f"{Q2}; {QNOON}",  # the inserts s22, s23
    "q3_t": f"{Q3}, by the long plain wooden table on the left bank; {QAFT}",
    "q4": f"{Q4}: the channel exactly as in the picture: {CHANNEL}; {QXI}",
    "q4_b": f"{Q4}, on the flat dry ground of the left bank; {QXI}",
    "ny": f"{N1}: the yard exactly as in the picture: {YARD}; {NIGHT}",
    "ny_w": f"{N1}, by the low earth-and-stone back wall on the right; {NIGHT}",
    "ny_c": f"{N1}, in the middle of the yard; {NIGHT}",
    "ny_d": f"{N1}, at the dark doorway of the farmhouse on the left; {NIGHT}",
}
LIGHT = {
    "dusk": "the orange-red evening light stays unchanged",
    "day": "the clear white morning light stays unchanged",
    "noon": "the hard white noon light stays unchanged",
    "aft": "the bright afternoon light stays unchanged",
    "xi": "the warm amber evening light stays unchanged",
    "night": "the cool moonlight stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_EVE = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow"  # scene 1 (e935 scene 3: no outer coat at dusk)
XU_DAY = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves rolled up to the elbows, pale dry dust on "
          "the lower half of the robe")  # scene 2 (the script's 沾泥: no mud, e032 fix3)
XU_COAT = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow with an old grey cloth outer coat worn loose over "
           "his shoulders")  # scene 3 (bible 〈人物〉: the outer coat by night)
LAMP = "one small clay oil lamp with one flame"  # bible 〈道具〉 許硯的陶油燈
ALING_TIED = ("A-ling, in her plain grey-white cotton dress tailored close at the waist with a cloth sash, its long sleeves covering "
              "both wrists, bound tight at the wrists with strips of grey cloth, the hem of the skirt over grey cloth leg wraps, her "
              "long black hair pinned up with one plain wooden hairpin")
ALING_DUCK = f"{ALING_TIED}, one small bamboo whistle on a thin cord round her neck"  # 35->36 (e935 ALING_DUCK)
ALING = ("A-ling, in her plain grey-white cotton dress tailored close at the waist with a cloth sash, its long sleeves down over "
         "both wrists, her long black hair pinned up with one plain wooden hairpin")  # from s16 on: the sleeves let down
QIN = ("Qin Shuang, in her fitted dark brown cross-collared short jacket cinched with a wide plain leather belt, fitted black "
       "trousers and leather boots, her sleek high ponytail tied with black cord")  # rule 5: nothing in her belt
QIAN = ("Qian Yuanwai, short and portly with a round face and a thin eight-shaped moustache, in his dark gold silk robe woven "
        "with small round medallions, the front of the robe plain brocade, three gold rings on his fingers")
QIAN_BACK = ("one short portly man seen only from behind, in a dark gold silk robe woven with small round medallions and a small "
             "black cap")  # s28: no picture, no name (e934 / e935 fix4)
GUARDS_LR = ("two men in Song-dynasty cross-collared homespun short jackets, cloth head wraps and cloth shoes, the broad young man in "
             "a dark teal jacket at the left end and the wiry middle-aged man in a deep wine-red jacket at the right end")  # e935 s34 (review 建議 1)
ALING_HAIR = "the long rest of her black hair falling straight down her back to the waist"  # e935 s33 / s34 (review 建議 1)
GUARDS = ("two men in Song-dynasty cross-collared homespun short jackets, cloth head wraps and cloth shoes, a broad young man in a "
          "dark teal jacket and a wiry middle-aged man in a deep wine-red jacket")  # e935 s32-s34
REF8 = ("eight people in ragged Song-dynasty homespun clothes, cloth head wraps and worn straw sandals, cloth bundles on their "
        "backs, each a different colour and age: an old man with a short grey beard in a faded undyed hemp-beige jacket and a bent "
        "old woman in a faded deep plum jacket in front, a lean middle-aged man in a dark charcoal jacket, a young woman in a "
        "rust-red jacket holding a small boy by the hand, a boy of about ten in a mustard-yellow jacket, a stocky middle-aged man in "
        "a dull olive-green jacket and a thin young man in a faded ochre jacket")
TORCHES4 = ("the lean man in charcoal, the stocky man in olive-green, the thin young man in ochre and the boy in mustard-yellow each hold "
            "up one burning pine torch in one hand at walking height; the old man in front has both hands free, and the young woman's "
            "other hand holds the strap of her bundle")  # rule 37: each torch in a named hand (review 必改 2)
REF7 = ("seven people in ragged Song-dynasty homespun clothes, cloth head wraps and worn straw sandals, cloth bundles on their "
        "backs, each a different colour and age: an old man with a short grey beard and grey hair in a faded undyed hemp-beige "
        "jacket in front, a lean middle-aged man in a dark charcoal jacket, a stocky middle-aged man in a dull olive-green jacket, "
        "a young woman in a rust-red jacket, a thin young man in a faded ochre jacket, a bent old woman in a faded deep plum jacket "
        "and a middle-aged woman in a dark grey jacket with a faded indigo head cloth")
HOE = "one hoe with a plain wooden handle and a flat iron head"
NEAR3 = ("three people in Song-dynasty cross-collared homespun short jackets and cloth head wraps seen from behind, each a different "
         "colour and age and each holding one hoe: a lean young man in a rust-red jacket, a stocky middle-aged man in a dull "
         "olive-green jacket and an older man with a short grey beard in a faded undyed hemp-beige jacket")
FAR5 = ("five more people in Song-dynasty cross-collared homespun short jackets and cloth head wraps, each a different colour and "
        "age: a broad young man in a dark charcoal jacket and a boy of about fifteen in a mustard-yellow jacket digging with one hoe "
        "each, a thin man in a faded ochre jacket with one hoe, and up on the left bank a middle-aged woman in a dark grey jacket "
        "with a faded indigo head cloth and a young man in a faded deep plum jacket each lifting one round bamboo basket of earth")
MAN1 = "a lean young man in a Song-dynasty cross-collared rust-red homespun short jacket and a cloth head wrap"
WOMAN1 = ("one middle-aged woman seen only from behind, in a ragged dark grey homespun jacket and a faded indigo head cloth, the back "
          "of her head toward us the whole shot")
TALLY = "flat sliver of pale bamboo about a hand long, smooth and plain on both sides"
TALLIES = "flat slivers of pale bamboo, each about a hand long, smooth and plain"
BRUSH = "one slim brush with a plain bamboo handle and a soft black tip"
PAPER = ("a short stack of plain white paper lying flat at the lower edge of the frame, soft and out of focus, its top sheet blank "
         "and lit evenly from the front")
DISH = "one small flat dark stone dish"
ABACUS = "one plain dark wooden abacus, a flat dark wooden frame with round dark beads on thin rods"  # bible rule 20 (the table's)
GOLD_ABACUS = ("one long flat gold abacus, as long as her forearm, a thin gold frame: a long row of thin gold rods set close side "
               "by side across its width, one thin gold crossbar running along its whole length, small round gold beads above and "
               "below the crossbar on every rod")  # rule 20: the gold one only in an insert (e023 / e024's wording)
HOMEGOING = ("six people in Song-dynasty homespun short jackets and cloth head wraps seen from behind, each a different colour and "
             "each with one hoe carried on the shoulder: a rust-red jacket, a dull olive-green jacket, a faded undyed hemp-beige jacket, a "
             "dark charcoal jacket, a mustard-yellow jacket and a dark grey jacket")
SPIES3 = ("three men in ragged undyed homespun jackets and cloth head wraps seen only from behind, each with one hoe carried on "
          "the shoulder, walking away together, small")
SLEEPERS = ("a row of twelve straw mats laid side by side along the foot of the back wall from just right of the bare tree to the "
            "right corner, running behind the well, their heads to the wall, nine men in ragged homespun curled asleep on them under "
            "ragged blankets with their backs to us, the three mats in the middle of the row empty")  # review 必改 8  # rule 42 (the right stretch of the back wall); 原版: the three spies' mats
FIRELINE = "a long thin line of small orange flames moving down the dark hillside, far away"  # rule 37
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# rule 40 (e031 / e033 / e935 TBACK): Tang Xiaotang from behind, her l1 costume (rule 4), no outer coat
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
QIN_EDGE = ("at the right edge of the frame, cut by it, soft and out of focus, only one shoulder and upper arm of a young woman in a "
            "dark brown short jacket")
# set-only sides (the picture of each place, all the way to the edge)
SIDE_SKY = "the orange-red evening sky"
SIDE_FIELD = "the flat dry yellow field"
SIDE_NIGHT = "the deep blue night sky over the dark fields"
NOSMILE_QIAN = "not smiling: eyes bulging, brows knotted, the corners of his mouth dragged hard down"


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
GATE_BACK = ("behind him, soft, the corner of the gate's small tiled roof at the top left, a leaning log at the left edge, the willow and the "
             "plank bridge over the dry ditch in the orange-red evening light")  # -wai2 (review 必改 3)

# s02 (review 必改 1, 2; 建議 2): KAI = True once the paid open-gate picture set-cunkou-zha2-kai-l1 is picked (PREP.md §7); until
# then the free crop -wai2 (no gate leaves in it) and the gateway just beyond the left edge.
KAI = True  # set-cunkou-zha2-kai-l1 picked 2026-11-21 (seed 9361202; the coordinator ran it)
S02_WAI2 = (f"wide shot at standing eye height just inside the gateway, like the picture: the gateway itself just beyond the left edge of "
            f"the frame, the corner of its small tiled roof at the top left and the thick crossbar leaning upright at the left edge; "
            f"coming in from the left edge one after another along the dirt road past the willow and over the plank bridge, {REF8}, "
            f"faces gaunt and tired, not smiling; {TORCHES4}; in the left foreground, seen from behind and standing aside, {GUARDS}, "
            f"each holding up one burning pine torch in his outer hand; standing at the right by the short log fence, {XU_EVE}, framed "
            f"full figure, side-on to the people, his face in profile to screen left toward them, never the lens; {HANDS}; exactly eleven people")
S02_KAI = (f"wide shot at standing eye height toward the gateway, like the picture: the two gate leaves of upright logs under the small "
           f"tiled roof swung wide back inward, each standing at a right angle to the fence, the thick crossbar leaning upright against "
           f"the left gate post; through the clear gateway, on the dirt road coming toward us, {REF8}, faces gaunt and tired, not "
           f"smiling; {TORCHES4}; one beside each swung-back leaf, {GUARDS}, each holding up one burning pine torch in his outer hand, "
           f"grave, not smiling, their lips closed; standing beside the gateway at the right, {XU_EVE}, framed full figure, side-on to "
           f"the people, his face in profile to screen left toward them, never the lens; {HANDS}; exactly eleven people")

SHOTS = [
    # ---- scene 1: the village gate at dusk, the same moment as e035's last shot (35->36, e935's cut).
    dict(chapter="柳溪村口，開門", loc="kk_g", cam="Wide shot from behind, slow push in", chars=["xuyan", "aling"], nospeak=["xuyan"], night="dusk",
         comp=f"wide shot from behind at standing eye height toward the gate, like the picture: {GATE_SHUT} fill the back of the frame, closed from the first frame to the last, the warm orange light of torches showing only through the narrow gaps between the logs; in the middle {XU_EVE}, seen from behind, framed full figure, already standing close before the crossbar with both hands gripping it from the first frame; at his left in the same row {ALING_DUCK}, {ALING_HAIR}, seen from behind, her hands empty at her sides; one step behind him on his right {TBACK_SMALL}, her hands empty; at the two ends of the crossbar, side-on to us, {GUARDS_LR}, each holding up one burning pine torch in his outer hand at walking height, grave, not smiling, their lips closed, never the lens; {HANDS}; exactly five people",
         lines=[("xuyan", "進來的人都有飯吃，但是每個人都要幹活。", "很穩，對門外說")],
         motion=f"Xu Yan braces his feet and lifts the thick crossbar up out of its iron fitting with both hands, its weight dragging his shoulders down, and holds it level across his body, while the two gate leaves stay closed; {quiet('A-ling and the two men', 'their', plural=True)}; {HEADSTILL}",
         zh="中景（從背後）、慢推（人眼高、照圖；送 e935 的免費裁切 `set-cunkou-zha2-men-l1`：兩扇圓木門扇、鐵件扣住的齊腰門閂、左邊籬笆）：**接點 35→36（照第 35 集成片 `e935-live.mp4` 最後 15 秒）**：s34 許硯走到門閂前、**阿令在他左邊同一排**、唐小棠在他右後、兩個守門的村民（**暗青在左、深酒紅在右**）在門閂兩頭、各拿一支火把；s35 許硯右手按在門縫鐵件旁的門閂上。本鏡同一刻、同一站位：許硯第一格已經兩手握住門閂（稿子『兩手握住』在第一格），兩腳站穩、把門閂從鐵件裡抬起，重量把肩膀往下一拖、橫抱在身前（一個動作；稿子『轉身靠在門柱邊』交給 s02 第一格）。**兩扇門扇從第一格到最後一格關著**（第 35 集 fix1 s34、fix3 s32：H3 會自己把門打開，結果先寫），火光只從圓木縫透進來（稿子『柵欄縫透進火把的橘光』）。他背對鏡頭，台詞放錄音（nospeak；答第 35 集 s29 流民婦人）；唐小棠背影不點名、不送圖（拍法 40）；阿令照第 35 集：袖口紮緊、綁腿、竹哨、木簪下長髮披到腰（獨立審稿建議 1）。稿子『前景是柵欄的粗木條』照圖：柵門在畫面後方"),
    dict(loc="kk_g", cam="Wide shot, slow push in", chars=["xuyan"], night="dusk", act=3,
         comp=S02_KAI if KAI else S02_WAI2,
         motion=f"The people walk in one after another at walking pace, and the old man in front stops before Xu Yan and bows low with his two hands clasped before him; {quiet('Xu Yan')}",
         zh="全景、慢推（人眼高）：**獨立審稿必改 1、建議 2**：原本送 `-men`（門扇關著）、文字寫已推開，圖文打架。協調者定做付費開門圖 `set-cunkou-zha2-kai-l1`（Qwen 從 `set-cunkou-zha2-l1` 只改門扇推開；2026-11-21 協調者跑、選 9361202：兩扇往內推開、門閂靠左柱），**`KAI = True` 送它**；挑定前用的是免費裁切 `set-cunkou-zha2-wai2-l1`（沒有門扇：左上一角瓦簷、左緣斜靠的圓木＝靠在門柱邊的門閂、垂柳、木板橋、右邊兩間屋），寫成門口就在畫左外、人一個接一個從左緣沿土路走進來；開門圖挑定後 `KAI = True`，構圖換成 `S02_KAI`（從門裡看推開的兩扇門與門口）。八個流民（每人衣色年紀不同；稿子『約一百個』照拍法 34），**四支火把點名拿在炭灰、橄欖綠、赭黃、芥黃四人手上**（必改 2：要作揖的老人兩手空著、牽孩子的婦人另一手拉包袱帶），守門兩人在左緣前景背對各拿一支＝六支（拍法 37）；許硯在右邊短籬笆旁側身，前排老人走到他面前彎腰拱手。不笑、嘴閉著。無台詞"),
    dict(loc="kk_g", cam="Low-angle medium shot, slow push in", chars=["qianyuanwai"], night="dusk",
         comp=f"low-angle medium shot of {QIAN}, seen from below, framed from the waist up, already standing up on a low earthen mound beside the gate from the first frame, high against the sky, his face three-quarter to screen right, looking down toward someone out of sight beyond the lower right edge of the frame, never the lens; that side of the frame is only {SIDE_SKY} all the way to the edge, and he is the only person in the frame; furious and shrill, {NOSMILE_QIAN}, lips moving hard between shouted words; behind him, soft, the small tiled roof of the gate against the orange-red evening sky; {HANDS}",
         lines=[("qianyuanwai", "許硯，你瘋了！這是一百多張嘴！", "尖聲")],
         motion="Qian Yuanwai slaps his flat right hand down hard through the air and thrusts it down toward the gateway below him as he shouts",
         zh="低角度中景、慢推（送本集免費做的 `set-cunkou-zha2-ding2-l1`：只有小瓦頂與橘紅天，獨立審稿必改 3：`-ding` 下半是關著的門扇）：**圖上沒有門樓、沒有欄杆**（聖經〈接點〉35→36）：錢員外照第 35 集 s31 站在柵門旁的土台上，低角度映在天上，朝畫右下外看不到的人（門下的許硯，不點名）尖聲喊，右手平掌往下一拍、再往下指向門口（稿子『一掌拍在欄杆上、揚起一陣灰』：沒有欄杆，拍空氣）。稿子『身後兩個家丁（背影）』不寫（拍法 34：家丁只在遠景）。**不笑**逐部位寫（第 34、35 集錢員外正面常笑；喊的鏡第 35 集 s31 過關）"),
    dict(loc="kk_g", cam="Low-angle medium close-up, slow push in", chars=["qianyuanwai"], night="dusk",
         comp=f"low-angle medium close-up of {QIAN}, seen from below, framed from the chest up with space above his head, standing up on the low earthen mound beside the gate, already turned toward the village side from the first frame, his face three-quarter to screen right {off('right', SIDE_SKY)}; scornful and urgent, {NOSMILE_QIAN}, lips moving fast between words; behind him, soft, the small tiled roof of the gate and the orange-red evening sky; {HANDS}",
         lines=[("qianyuanwai", "他們吃光了糧，餓死的可是你們自己！", "煽動")],
         motion="Qian Yuanwai sweeps his flat right hand from the left across to the right and leans forward over the edge of the mound as he speaks",
         zh="低角度中近景、慢推（送 `-ding2-l1`；跟 s03 不同景別）：錢員外轉向門內的村民（畫右外，不點名、不寫人：拍法 31），右手平掌從左（流民那邊）一掃到右、身子往前探，煽動地說；**不笑**"),
    dict(loc="kk_e", cam="Insert close-up, slow push in", chars=[], night="dusk",
         comp=f"insert close-up from a little above, the very first frame is already a close view of {GOLD_ABACUS}, held flat in two small fair hands with light peach-pink silk cuffs at the waist of a light peach-pink silk skirt; far below, soft and out of focus, only bare dusty earth fills the background to every edge; only the abacus and the two hands are in the frame",
         lines=[("tangxiaotang", "糧倉裡的糧，連上流民，只夠撐兩個月。", "小聲，不笑")],
         motion=NOBODY + "the fingers push the last round gold bead along its rod and stop still, and the two hands hold the abacus still",
         zh="插鏡、慢推（第一格就是金算盤，拍法 10、35；不寫地點句，送本集免費做的 `set-cunkou-zha2-di-l1`（柵門前的土路）只當地面與光）：稿子 c05 是唐小棠中景說話、腰間小金算盤當前景；真人版她不露嘴說話（拍法 3、40），**金算盤只在插鏡**（拍法 20：前臂長的扁長金算盤），改成她兩手捧著算盤撥完最後一顆珠子、停住的插鏡，她的話放錄音（畫外）。稿子『抬頭拉一下許硯的袖子』不拍（一鏡一個動作）"),
    dict(loc="kk_in", cam="Medium shot over the shoulder, slow push in", chars=["xuyan"], night="dusk",
         comp=f"medium shot over a shoulder: {TANG_EDGE}; beyond it, in the left half of the frame, {XU_EVE}, standing just inside the gate, framed from the waist up, already turned to face the young woman in the foreground from the first frame, his face three-quarter to screen right toward her, never the lens; steady and sure, not smiling: brows level, eyes calm, lips moving evenly between words; {GATE_BACK}; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("xuyan", "兩個月夠了。兩個月，我們挖一條渠。", "很穩")],
         motion="Xu Yan lifts his flat right hand and sweeps it back toward the far hills beyond the gateway at the left as he speaks",
         zh="過肩中景、慢推（送本集免費做的 `set-cunkou-zha2-wai2-l1`（獨立審稿必改 3：`-wai` 左緣還有關著的右門扇）：左上一角瓦簷、左緣斜靠的圓木、垂柳、乾溝上的木板橋；**門扇在 s02 已推開，之後的鏡不送門扇關著的圖**）：前景右是虛焦、被畫框切掉的雙丸子後腦與桃粉肩頭（不點名、不送圖，拍法 2；稿子『唐小棠肩後』）；許硯第一格已經轉過身面向她（稿子『轉過身』在第一格），右手平掌往後朝門外遠處的山一揮（單指會讀錯，拍法 32），很穩地說"),
    dict(loc="kk_in", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="dusk",
         comp=alone(f"{BEYOND_XU}, {XU_EVE}, standing, framed from the waist up, his face three-quarter to screen right toward her, his lips pressed shut, never the lens; calm, not smiling; {GATE_BACK.replace('behind him', 'behind them')}; she stays in the middle of the frame the whole shot; {HANDS}; {TWO_BACK}",
                    "standing on the dirt road just inside the gate,"),
         lines=[("tangxiaotang", "挖渠？他們餓著肚子，渠能當飯吃嗎？", "眉頭一皺，壓著聲音")],
         motion=f"she takes half a step closer to him, only her legs moving; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-wai2-l1`）：稿子 c07 是唐小棠近景下巴以上說話，真人版照拍法 40 從背後拍：她背影在畫面正中、頭不動、剛好兩顆丸子（l1 交領短襦，不寫高立領），往前湊半步（只動腿；『眉頭一皺』交給語氣）；許硯在她前方一步的畫左三分之一、看著她、嘴閉著（→ 答在 s08）"),
    dict(loc="kk_in", cam="Low-angle medium shot, slow push in", chars=["xuyan"], night="dusk",
         comp=f"low-angle medium shot, a little from below: {XU_EVE}, already standing up on a low flat stone just inside the gate from the first frame, framed from the waist up, his face three-quarter to screen left toward the people in the left foreground, never the lens; firm and loud, not smiling: brows level, eyes bright, lips moving wide and clear between words; in the left foreground, soft and out of focus, seen only from behind, the shoulders and head-wrapped heads of two people in ragged homespun, a dark charcoal jacket and a rust-red jacket, standing still; behind him, soft, the three small earthen-walled houses and the far hills under the orange-red evening sky; {HANDS}; exactly three people, the two in the foreground seen only from behind",
         lines=[("xuyan", "渠挖到山腳，明年多二十畝田有水。", "提高聲音")],
         motion="Xu Yan raises his flat right hand high above his head for everyone to see as he speaks",
         zh="低角度中景（略仰）、慢推（送 e935 的免費裁切 `set-cunkou-zha2-dao-l1`：三間泥磚屋與遠山）：許硯第一格已經站上門邊一塊平石（稿子『往前走兩步、站上石頭』在第一格完成），右手平掌高高舉起讓大家看見，提高聲音說（答 s07）；前景左是虛焦的兩個流民的肩與包頭（炭灰、鐵鏽紅，背影、停下腳步）"),
    dict(loc="kk_in", cam="Wide shot, slow push in", chars=["xuyan"], night="dusk",
         comp=f"wide shot at standing eye height, like the picture: in the left half of the frame, seen from behind and side-on, {REF7}, standing in a loose half circle on the dry ground, faces turned toward the man on the stone, their lips closed, not smiling, the old man in front already stepped forward before the stone from the first frame; at the right of the frame, up on a low flat stone, {XU_EVE}, framed full figure, his face three-quarter to screen left toward them, never the lens; firm, not smiling: lips moving clear between words; behind, soft, the three small earthen-walled houses and the far hills under the orange-red evening sky; {HANDS}; exactly eight people",
         lines=[("xuyan", "一鋤頭換一碗飯，誰也不白吃，誰也不白餓。", "一字一句")],
         motion="The old man in front bows deeply to Xu Yan with his two hands clasped before him, and the two men behind him nod once",
         zh="全景、慢推（人眼高、照圖；送 `-dao-l1`，獨立審稿建議 3：`-wai` 那塊地是第 35 集 s29 流民在門外跪的地方）：畫左七個流民（背影、側臉，每人衣色年紀不同；稿子『約三十人』照拍法 34），前排白髮短鬚的老流民第一格已經走到石頭前，對許硯深深作揖，身後兩個男人跟著點一下頭；許硯在畫右的平石上、臉朝畫左、說話（2026-11-06 審稿：不寫鋤頭堆）。配樂重音在這句"),
    dict(loc="kk_g", cam="Low-angle medium shot, slow push in", chars=["qianyuanwai"], night="dusk",
         comp=f"low-angle medium shot of {QIAN}, seen from below, framed from the waist up, on the low earthen mound beside the gate, already turned half away to step down off it from the first frame, his face looking back over his right shoulder, down toward someone out of sight beyond the lower right edge of the frame, never the lens; that side of the frame is only {SIDE_SKY} all the way to the edge, and he is the only person in the frame; a cold sneer: eyes narrowed, one corner of his mouth curled, lips moving slow and hard between words; behind him, soft, the small tiled roof of the gate against the orange-red evening sky; {HANDS}",
         lines=[("qianyuanwai", "好！等你的糧吃光了，別來求我錢家！", "冷笑")],
         motion="Qian Yuanwai flings his wide right sleeve back and thrusts his flat right hand hard toward the gateway below him as he speaks",
         zh="低角度中景、慢推（送 `-ding2-l1`）：錢員外第一格已經轉身要下土台（稿子『甩袖轉身、往門樓梯口走、走一半』在第一格完成；沒有門樓與梯口），從右肩回頭、甩一下寬袖、右手平掌狠狠指向下面的門口，冷笑著說（稿子：冷笑，這鏡可以帶冷笑）。家丁不寫（拍法 34）"),
    dict(loc="kk_in", cam="Close-up, slow push in", chars=["xuyan"], night="dusk",
         comp=f"close-up of {XU_EVE}, standing just inside the gate, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes already on the gateway beyond the left edge of the frame from the first frame, never the lens; he is the only person in the frame; heavy and unsure, not smiling: brows drawn, lips pressed shut; the wavering orange light of torches on one side of his face; behind him, soft, only the orange-red evening sky over the far hills and a few long willow fronds at the edge; {HANDS}",
         lines=[("xuyan", "兩個月挖一條渠……我這輩子連水溝都沒挖過。", "心裡話，錄得近、輕", "inner"), ("xitong", "宿主上次也沒熬過皂。", "冷")],
         motion=f"Xu Yan lifts his right hand and presses the heel of his flat palm against the middle of his brow, lets out one long breath and his shoulders sink; {SILENT_HE}",
         zh="近景、慢推（送 e935 的免費裁切 `set-cunkou-zha2-kong-l1`：遠山上的橘紅天、左緣幾縷柳條；稿子『身後只有橘紅的天』）：許硯看著畫左外還在進人的門口，右手掌根按住眉心（稿子『拇指抹一下眉心』：單指會讀錯，拍法 32）、吐一口氣、肩膀垮下來；心裡話與系統都是錄音、**全程嘴閉著**；**不寫淡藍光**（拍法 11；系統的鬥嘴不出面板）。稿子 c11 三句約 11 秒人聲（照第 35 集實測：許硯心裡話 4–4.3 字／秒、系統 9 字 2.4 秒），10 秒的片段放不下：拆成本鏡（心裡話＋系統）與 s11b（心裡話第二句）"),
    dict(sid="s11b", loc="kk_in", cam="Medium close-up, slow push in", chars=["xuyan"], night="dusk",
         comp=f"medium close-up of {XU_EVE}, standing just inside the gate, framed from the waist up, his right hand already lowered from his brow from the first frame, his face three-quarter to screen left, his eyes on the gateway beyond the left edge of the frame, never the lens; he is the only person in the frame; resolved, not smiling: eyes steadying, brows level, lips pressed shut; the wavering orange light of torches on one side of his face; behind him, soft, only the orange-red evening sky over the far hills; {HANDS}",
         lines=[("xuyan", "也是，皂熬得出來，渠就挖得出來。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan draws one slow deep breath, his chest lifting, and squares his shoulders, his eyes settling on the gateway; {SILENT_HE}",
         zh="中近景、慢推（送 `-kong-l1`；跟 s11 不同景別）：稿子 c11 的第三句：許硯吸一口氣、挺起肩膀、眼神定下來（一個動作）；心裡話是錄音、**全程嘴閉著**、不笑"),
    dict(loc="kk_in", cam="Medium shot, slow push in", chars=["aling", "xuyan"], night="dusk",
         comp=f"medium shot just inside the gate: at the left, {ALING_TIED}, already stopped beside him from the first frame, framed from the waist up, the small bamboo whistle already in her right hand from the first frame, its thin cord lifted off over her head and gathered in her fingers, her face three-quarter to screen right toward him, never the lens; quiet and steady, not smiling: brows level, lips moving softly between words; at the right, {XU_EVE}, framed from the waist up, his face three-quarter to screen left toward her, his lips pressed shut, never the lens; listening, not smiling; behind them, soft, the three small earthen-walled houses and the far hills under the orange-red evening sky; {HANDS}; exactly two people",
         lines=[("aling", "名冊我來寫，一個人一行，配糧才不會亂。", "很輕")],
         motion=f"A-ling tucks the small whistle and its cord away into her left sleeve as she speaks; {quiet('Xu Yan')}",
         zh="中景、慢推（送 `-dao-l1`）：阿令（袖口紮緊、綁腿）第一格已經走到許硯左邊停下（照第 35 集成片：她在他左邊）、竹哨已經從脖子上取下握在右手（稿子『伸手解下脖子上的竹哨』在第一格完成），一邊說一邊把竹哨連細繩收進左袖（一個動作；之後各鏡不再寫竹哨，聖經〈道具〉）；許硯在右、看著她、嘴閉著。稿子 c12 的後半（許硯點頭、轉向唐小棠說話）拆到 s12b"),
    dict(sid="s12b", loc="kk_in", cam="Medium shot over the shoulder, slow push in", chars=["xuyan"], night="dusk",
         comp=f"medium shot over a shoulder: {TANG_EDGE}; beyond it, in the left half of the frame, {XU_EVE}, standing just inside the gate, framed from the waist up, his face three-quarter to screen right toward the young woman in the foreground, never the lens; decided, not smiling: brows level, eyes clear, lips moving firmly between words; {GATE_BACK}; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("xuyan", "好，明早天一亮，記名、發鋤頭、開工。", "乾脆")],
         motion="Xu Yan gives one firm nod and speaks",
         zh="過肩中景、慢推（送 `-wai2-l1`，同 s06 的機位）：稿子 c12 的後半：許硯點一下頭、對唐小棠（前景右的雙丸子背影，不點名、不送圖）乾脆地定下明早開工（第一場結尾；『轉頭看阿令、點頭、再轉向唐小棠』只留點頭，一鏡一個動作）"),
    # ---- scene 2: the new channel at the foot of the hills, the first days of digging to half a month later.
    dict(chapter="山腳新渠，開工到半個月", loc="q1", cam="Wide shot, slow push in", chars=["xuyan"], night="day",
         comp=f"wide shot from the near end of the channel at standing eye height, like the picture: in the near half of the channel bed, {NEAR3}, swinging their hoes into the dry earth; further down the channel bed and up on the banks, {FAR5}; in the channel bed just beyond the three near diggers, {XU_DAY}, framed full figure, standing with his hoe planted upright in the channel bed at his right side, his right hand resting on top of its handle, facing us three-quarter, his face toward the three diggers, never the lens; tired and loud, not smiling: brows up, breathing hard, lips moving wide between shouted words; {HANDS}; exactly nine people",
         lines=[("xuyan", "再往下挖一尺，渠底要比田低！", "喘，大聲")],
         motion="the hoes of the near diggers fall into the dry earth one after another, small puffs of yellow dust rising, and Xu Yan straightens his back and shouts down the channel to them",
         zh="大全景、慢推（照圖；送 `set-shanjiao-qu-l1`：乾渠從前景筆直往遠處延伸、左岸一長堆新土與一堆乾草、遠處一排深色松樹、中段一塊木板架在渠上、右岸乾草與一片青秧田；稿子的『推軌由右往左順著渠』照圖：渠是往畫面深處去的，改成從渠的近端慢推）：**山腳新渠**，開工頭幾天上午、白光（場頭；聖經：**不是第 34 集那條引水渠**、還沒放水：場景句寫溝底是乾裂的土，不寫否定句；渠照圖寫成約膝深、寬平底，獨立審稿必改 6；送清掉護欄與直立木板的 `set-shanjiao-qu-jing-l1`，必改 7、建議 6）。近處渠底三個人背對鏡頭揮鋤（鐵鏽紅、暗橄欖綠、本色麻），遠處與兩岸另外五個（每人一把鋤頭、左岸兩人抬竹筐；稿子『約四十個』照拍法 34 寫看得見的八個）；許硯在三人後面的渠底、袖子捲到手肘、袍子下半截一層淡淡的乾土（稿子『沾泥』：不寫泥，第 32 集 fix3），鋤頭立在身邊右側、右手搭在柄頂，直起腰、對著三人大聲喊（聽的人在畫裡）"),
    dict(loc="q1_t", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="day",
         comp=alone(f"{ABACUS} lying on the tabletop before her and one round bamboo basket full of {TALLIES} at her right elbow; her right hand already holding out one {TALLY} across the table from the first frame; beyond the table at the left, side-on to us, {MAN1}, {HOE} resting on his right shoulder held there by his right hand, well apart from the bamboo, his left hand lifted palm up toward the bamboo, his face in profile, his lips closed, not smiling, never the lens; behind them, soft, the flat dry yellow field, the mound of dug earth and the line of dark pines; she stays in the middle of the frame the whole shot; {HANDS}; {TWO_BACK}",
                    f"sitting on a low stool behind the right end of {TABLE},"),
         lines=[("tangxiaotang", "挖一丈記一碗，晚上憑籌領飯，不多不少。", "俐落")],
         motion=f"the man's left hand closes round the sliver of bamboo and takes it from her fingers, only her arm moving; {quiet('the man')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送本集免費做的 `set-shanjiao-qu-zhuo2-l1`：左岸平坦的乾黃地、新土堆、遠處松樹（清掉護欄的版本，獨立審稿必改 7））：唐小棠坐在長木帳桌右端、背影在畫面正中、頭不動、剛好兩顆丸子（拍法 40；說話放錄音）；桌上一把素木算盤（聖經拍法 20：帳桌那把是木算盤）、右肘邊一竹筐竹籌（素面竹片，聖經〈道具〉；拍法 38）；她右手第一格已經把一根竹籌遞過桌面，桌前左邊一個鐵鏽紅短打的流民漢子側身、右手扶著扛在肩上的鋤頭（跟竹籌分開）、左手接過竹籌（一個動作；稿子『撥一下算盤』拿掉）。漢子側臉、嘴閉著"),
    dict(loc="q1_e", cam="Insert close-up, slow push in", chars=[], night="day",
         comp=f"insert close-up from a little above, the very first frame is already a close view of a man's rough hand in a rust-red homespun sleeve holding one {TALLY}, pale dust in the creases of his fingers; far below, soft and out of focus, only cracked dry earth fills the background to every edge; only the hand and the sliver of bamboo are in the frame",
         motion=NOBODY + "the hand tucks the sliver of bamboo into the cloth sash at the bottom of the frame and pulls away downward out of the frame",
         zh="插鏡、慢推（**第一格就是竹籌特寫**，拍法 10、35；不寫地點句，送本集免費做的 `set-shanjiao-qu-di-l1`（乾裂的渠底）只當地面與光）：鐵鏽紅袖口的手（s14 那個漢子，不點名）握著一根素面竹籌，塞進腰帶、手往下抽出畫面（稿子『跳下渠溝』交給聲音）；稿子『指甲裡有泥』寫成指縫一層淡淡的乾土（不寫泥）。無台詞"),
    dict(loc="q1_t", cam="Medium shot, slow push in", chars=["aling"], night="day",
         comp=f"medium shot at the left end of {TABLE}: {ALING}, sitting on a low stool behind the table, framed from the waist up, {BRUSH} held upright in her right hand, its tip lifted just above the paper, {PAPER}, {DISH} on the tabletop at her right; her face lowered three-quarter to screen right toward the paper, her eyes on it, never the lens; calm and intent, not smiling, her lips closed; in the right foreground, soft and out of focus, {WOMAN1}, standing before the table; behind A-ling, soft, the flat dry yellow field and the line of dark pines; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("tangxiaotang", "下一個，姓名報給阿令姊，一人一行。", "俐落")],
         motion=f"A-ling dips the soft black tip of the brush into the small dark stone dish and lifts it back to just above the paper, and holds it there; {quiet('A-ling and the woman', 'their', plural=True)}",
         zh="中景、慢推（送 `-zhuo2-l1`）：帳桌左端，阿令（長袖放下、木簪；第一場的布條、綁腿、竹哨都收了，稿子〈角色〉）坐著、右手一支素竹桿毛筆；一疊白紙在畫面下緣虛焦、紙面空白（拍法 27、38）；桌前右前景一個流民婦人背影（深灰粗布衣、褪色靛藍頭巾）。阿令蘸一下（硯台寫成一個扁平的小黑石碟，不寫墨字），把筆尖提回紙面上方停住（拍法 38：**不拍落筆那一下**，筆畫會長成假字）。唐小棠的話是畫外錄音（她在畫外帳桌右端）；阿令、婦人嘴閉著"),
    dict(loc="q1_e", cam="Insert close-up, slow push in", chars=[], night="day",
         comp=f"insert close-up from a little above, the very first frame is already a close view of a young woman's slim fingers in a grey-white sleeve resting on the near corner of a short stack of blank plain white paper and the soft black tip of {BRUSH.replace('one slim brush', 'a slim brush')} held just above it at the top of the frame, the fingers and the brush tip sharply in focus; the paper itself soft and out of focus at the lower part of the frame, lit warmly from the side; far below, soft and out of focus, only pale dry earth fills the background to every edge; only the fingers, the brush tip and the soft paper are in the frame",
         motion=NOBODY + "the fingers smooth the corner of the blank top sheet flat once, and the brush tip stays lifted just above the paper",
         zh="插鏡、慢推（**第一格就是名冊特寫**，拍法 10、35；不寫地點句，送 `set-shanjiao-qu-di-l1` 只當地面與光）：稿子『一行行端正的小楷、虛焦』與『筆尖落下、寫完一行收筆』照拍法 7、38 改：對焦在阿令灰白袖口的指尖與筆尖、紙面空白而虛焦（獨立審稿建議 4），指尖把紙角撫平，筆尖停在紙上方、**不落筆**（筆畫會長成假字）；『工整』交給 s18 的台詞。無台詞"),
    dict(loc="q1_t", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "aling"], nospeak=["tangxiaotang"], night="day",
         comp=alone(f"her shoulders square to the table, facing straight away from us like the rest of her, her right hand resting on {ABACUS} before her; one step beyond her in the left third of the frame, at the left end of the same table, {ALING}, sitting, her whole figure clear of the young woman's head and shoulders, {BRUSH} upright in her right hand, its tip lifted just above the blank plain white paper soft at the lower edge, her face lowered to the paper, her lips closed, not smiling, never the lens; behind them, soft, the flat dry yellow field and the line of dark pines; she stays in the middle of the frame the whole shot; {HANDS}; {TWO_BACK}",
                    f"sitting behind the right end of {TABLE},"),
         lines=[("tangxiaotang", "這字……工整得像宮裡發出來的帖子。", "小聲，看呆了")],
         motion=f"her right hand stops still on the beads of the abacus, only her arm moving; {quiet('A-ling', 'her')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-zhuo2-l1`）：稿子 c18 是唐小棠下巴以上的近景，真人版從背後拍（拍法 40）：她肩膀正對桌子、跟全身一樣正背對（獨立審稿必改 4：拿掉往左傾身，免得轉成左側臉），右手按在算盤上、停住（一個動作；『眼睛睜大』交給語氣）；阿令在她前方左三分之一、低頭、筆尖停在紙上方（拍法 38）、嘴閉著（→ 答在 s19）。配樂：古琴一聲"),
    dict(loc="q1_t", cam="Medium close-up, slow push in", chars=["aling"], night="day",
         comp=f"medium close-up of {ALING}, sitting at the table, framed from the waist up, the slim brush in her right hand at the bottom of the frame, her face lowered three-quarter to screen right toward the blank paper below the frame, her eyes on it, never the lens; she is the only person in the frame; cool and calm, not smiling: brows level, eyes down, lips moving softly between words; behind her, soft, only the flat dry yellow field and the line of dark pines; {HANDS}",
         lines=[("aling", "字而已，寫得清楚，配糧才不會錯。", "淡淡的")],
         motion="A-ling lays the slim brush down across the small dark stone dish as she speaks, her eyes staying down on the paper",
         zh="中近景（腰以上：手的動作要在框裡，拍法 32）、慢推（送 `set-shanjiao-qu-zhuo2-l1`，獨立審稿建議 5：她坐在桌的遠側，身後是乾黃地與松樹；臉跟 s16 一樣朝畫右看紙）：阿令不抬頭，把筆擱在小石碟上（稿子『寫完一行才擱筆』：不拍寫字，拍法 38），淡淡地說（答 s18）；不笑"),
    dict(loc="q1_t", cam="Medium shot, slow push in", chars=["xuyan", "aling"], night="day",
         comp=f"medium shot at the left end of {TABLE}: at the right, {XU_DAY}, already standing at the end of the table from the first frame, bent a little over the paper, framed from the waist up, his hoe planted upright in the earth at his far right side, well apart from his hands; at the left, behind the table, {ALING}, sitting, the slim brush laid across the small dark stone dish, the blank plain white paper soft at the lower edge, her face lowered to the paper, never the lens; behind them, soft, the flat dry yellow field and the line of dark pines; {HANDS}; exactly two people",
         lines=[("xuyan", "是好字。妳不想說，我就不問。", "很輕")],
         motion=f"Xu Yan straightens up from the paper and speaks softly to her, his face three-quarter to screen left toward her, a faint easy look in his eyes, and A-ling lifts her eyes to him once and lowers them again to the paper; {quiet('A-ling', 'her')}",
         zh="中景、慢推（送 `-zhuo2-l1`）：許硯第一格已經從渠裡上來、站在帳桌左端俯身看紙（稿子『爬上岸、插鋤頭、俯身看』在第一格完成），鋤頭插在他右外側的土裡、跟手分開；他直起身、很輕地說（稿子：可以淡淡一笑，寫成眼神放鬆、不寫笑字），阿令抬眼看他一下、又低頭、嘴閉著（← 因為 s18；守第 31 集『好，不問』的約）"),
    dict(loc="q2_b", cam="Medium shot, slow push in", chars=["xuyan", "qinshuang"], night="noon",
         comp=f"medium shot on the strip of dry grass along the right bank, the green paddy behind: at the left, {XU_DAY}, standing, framed from the waist up, his hoe planted upright beside him at his left side, his face three-quarter to screen right toward her, his lips pressed shut, never the lens; at the right, {QIN}, already arrived along the edge of the paddy and stopped close beside him from the first frame, framed from the waist up, her face three-quarter to screen left toward him, never the lens; sharp and wary, not smiling: eyes narrowed, lips moving low between words; behind them, soft, the dry channel with its single plank and the green paddy of young rice; {HANDS}; exactly two people",
         lines=[("qinshuang", "你看渠尾那三個人，腳上的鞋是新的。", "壓低聲音")],
         motion=f"Qin Shuang bumps his shoulder with hers and tips her chin toward the far end of the channel beyond the left edge of the frame as she speaks low, and Xu Yan turns his eyes that way; {quiet('Xu Yan')}",
         zh="中景、慢推（送本集免費做的 `set-shanjiao-qu-tian2-l1`：右岸乾草、青秧田、渠上那塊木板（直立木板塗成細木樁，建議 6））：約第一六六天正午（換光就是換日子）。秦霜第一格已經沿著秧田邊走到許硯右邊停下（稿子『從右邊田埂走來』在第一格；**柴刀不寫**，聖經拍法 5、〈道具〉），肩膀碰他一下、下巴往畫左外的渠尾一點，壓低聲音說；許硯順著看過去、嘴閉著（稿子的跟拍改慢推）"),
    dict(loc="q2_e", cam="Low-angle insert close-up, slow push in", chars=[], night="noon",
         comp="low-angle insert close-up at ground height, the very first frame is already a close view of a row of six pairs of feet and shins below the knee on the cracked dry earth, ragged homespun trouser legs above them: three pairs in worn, frayed straw sandals and, in the middle of the row, three pairs in brand-new black cloth shoes with clean white soles; far beyond, soft and out of focus, only cracked dry earth fills the background to every edge; only the feet and shins are in the frame",
         lines=[("qinshuang", "逃荒的人草鞋都磨破了，哪來的新鞋？", "冷")],
         motion=NOBODY + "the three pairs of brand-new black cloth shoes step forward together, and the straw sandals follow one after another",
         zh="低角度插鏡、慢推（**第一格就是腳的特寫**，拍法 10、35；不寫地點句，送 `set-shanjiao-qu-di-l1` 只當地面與光）：渠底一排六雙腳（只拍小腿以下）：三雙磨破的草鞋、中間三雙嶄新的黑布鞋（白鞋底），新鞋一起往前踩一步、草鞋跟著動（聖經〈小角色〉：三個探子只拍腳、手、背影）。秦霜的話是畫外錄音（2026-11-06 審稿後的台詞；反問，→ 答在 s23）"),
    dict(loc="q2_e", cam="Insert close-up, slow push in", chars=[], night="noon",
         comp=f"insert close-up, the very first frame is already a close view of one man's right hand in a ragged undyed homespun sleeve gripping the plain wooden handle of one hoe in a reverse grip, the fist turned over, the thumb wrapped over the top of the handle, thick rough yellowish hardened skin across the web of the thumb and the base of the fingers, one long pale old scar across two knuckles; far below, soft and out of focus, only the mound of dug brown earth fills the background to every edge; only the hand, the sleeve and the hoe handle are in the frame",
         lines=[("qinshuang", "虎口全是繭，他們握慣的是刀，不是鋤頭。", "冷")],
         motion=NOBODY + "the hand loosens on the handle and closes again in the same reverse grip, then drives the hoe down hard into the earth below the frame",
         zh="插鏡、慢推（**第一格就是手的特寫**，拍法 10、35；不寫地點句，送 `set-shanjiao-qu-an-l1` 只當地面與光）：一隻握鋤頭的手（破本色粗布袖口）：反手、拇指扣在柄頂（稿子『像握刀柄』：不寫刀字，拍法 5、17）；虎口與指根一大片粗糙發黃的硬皮（原版建議：不是金色圓斑；不寫 calloused 一字，第 34 集掃描）、指節一道長的淡色舊疤（一整條、不寫小點，拍法 6、12）；手鬆開、又照樣反手握回去，把鋤頭砸進土裡。秦霜畫外錄音"),
    dict(loc="q2_b", cam="Medium close-up, slow push in", chars=["qinshuang"], night="noon",
         comp=f"medium close-up of {QIN}, standing on the strip of dry grass along the right bank, framed from the waist up, her eyes already drawn back from the far end of the channel from the first frame, her face turned three-quarter to screen left {off('left', 'the dry channel and its far bank', he='she')}; cold and grave, not smiling: eyes narrowed, brows drawn level, lips moving low and slow between words; behind her, soft, only the green paddy of young rice; {HANDS}",
         lines=[("qinshuang", "昨晚他們在問，那個不說話的女人住哪。", "一字一字")],
         motion="Qin Shuang's right hand settles flat on her wide leather belt as she leans her face a little closer toward that spot and speaks low, word by word",
         zh="中近景（腰以上：手按腰帶要在框裡）、慢推（送 `-tian2-l1`；稿子『身後只有渠岸與山腳』照站位：她在右岸、背後是秧田）：秦霜第一格已經把視線從渠尾收回，朝畫左外看不到的人（許硯，不點名）貼近一點、一字一字地說；右手平按在寬皮帶上（稿子『手按在柴刀柄上』：柴刀不寫，拍法 5）；不笑"),
    dict(loc="q2_b", cam="Medium close-up, slow push in", chars=["xuyan"], night="noon",
         comp=f"medium close-up of {XU_DAY}, standing on the bank, framed from the waist up, his face three-quarter to screen right toward the young woman at the right edge, never the lens; {QIN_EDGE}, toward us the whole shot; grave, not smiling: brows drawn, eyes steady, lips moving low between words; behind him, soft, only the mound of dug brown earth and the heap of dry straw across the channel; {HANDS}; exactly two people, the one at the edge seen only in part",
         lines=[("xuyan", "別聲張，妳盯住他們，夜裡也別鬆。", "低聲")],
         motion="Xu Yan's eyes move once toward the long table beyond the left edge of the frame and come back, and he lays his flat left hand lightly on her upper arm and presses once as he speaks low",
         zh="中近景、慢推（送 `-an-l1`：渠對岸的新土堆與乾草；稿子『身後只有渠岸』）：許硯不笑，眼神往畫左外的帳桌（阿令那頭，寫成桌子不寫人，拍法 31）一瞥又收回，左手平掌輕輕搭在秦霜的手臂上按一下、低聲說（← 因為 s24）；秦霜只露右緣虛焦的肩與上臂（深褐短衣；不點名、不送圖，拍法 2）"),
    dict(loc="q3_t", cam="Medium shot, slow push in", chars=["qianyuanwai"], night="aft",
         comp=f"medium shot across the near corner of {TABLE}, the corner soft in the lower right foreground with one round bamboo basket full of {TALLIES} on it: {QIAN}, already arrived at the table from the right from the first frame, standing, framed from the waist up, his face three-quarter to screen left, looking down toward someone out of sight beyond the lower left edge of the frame, never the lens; that side of the frame is only {SIDE_FIELD} all the way to the edge, and he is the only person in the frame; furious and disbelieving, {NOSMILE_QIAN}, lips moving fast and hard between words; behind him, soft, the flat dry yellow field and the line of dark pines; {HANDS}",
         lines=[("qianyuanwai", "一斗都沒人買？我錢家的米，一夜跌了一半！", "又急又不信")],
         motion="Qian Yuanwai slams his flat right hand down on the tabletop as he speaks, and the slivers of bamboo in the basket jump",
         zh="中景、慢推（送 `-zhuo2-l1`）：約第一七〇天午後。錢員外第一格已經從右邊大步走到帳桌前（稿子『大步走到』在第一格），朝畫左下外看不到的人（坐著的唐小棠，不點名）又急又不信地說，右手平掌往桌上一拍、竹筐裡的竹籌跳起來（稿子『一把抓過家丁手上的帳冊往桌上一拍』：帳冊是紙，不寫，拍法 7、27、38；家丁不寫，拍法 34）；**不笑**逐部位寫（→ 答在 s27）"),
    dict(loc="q3_t", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="aft",
         comp=alone(f"both her flat hands resting on the tabletop on either side of {ABACUS}; beyond the table only the flat dry yellow field and the line of dark pines all the way to the far edge; she is the only person in the frame; {HANDS}",
                    f"already risen to her feet from the first frame behind the right end of {TABLE},"),
         lines=[("tangxiaotang", "流民有工換飯，誰還買你貴三成的米？", "不慌")],
         motion=f"she presses both flat hands down on the tabletop and leans a little forward over the abacus, only her arms moving; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-zhuo2-l1`）：稿子 c27 是唐小棠下巴以上的近景，真人版從背後拍（拍法 40）：她第一格已經站起來，兩手平按桌面、往前傾一點（一個動作；稿子『把小金算盤往桌上一放』：金算盤只在插鏡，拍法 20）；**畫面裡只有她一個人**：錢員外不入鏡（第 35 集 s23：當聽者的錢員外正面兩支都張嘴、一直笑），她的話是錄音（答 s26；2026-11-06 審稿後的台詞『貴三成』；反問，→ 答在 s28）"),
    dict(loc="q3_t", cam="Wide shot from behind, slow push in", chars=[], night="aft",
         comp=f"wide shot from behind at standing eye height: {QIAN_BACK}, framed full figure, already turned away from the long plain wooden table at the left edge from the first frame, the back of his head and his broad back toward us the whole shot; ahead of him the flat dry yellow field and the line of dark pines; he is the only person in the frame; {HANDS}",
         lines=[("qianyuanwai", "許硯斷我財路，這筆帳我記下了！", "咬牙")],
         motion=NOBODY + "he flings his wide right sleeve hard out to the side and strides away from us across the dry field toward the far pines, getting smaller, his back toward us the whole shot",
         zh="中遠景（從背後）、慢推（送 `-zhuo2-l1`）：**錢員外只拍背影**（第 34 集 s32 fix4、第 35 集 s24 fix4：他的不笑正面三輪都笑，改成背影甩袖走開＋錄音才過；本集一開始就照這樣寫）：不送臉部圖、不點名，身分句換成服裝句（深金團花錦袍、小黑帽、矮胖）；第一格已經轉身背對鏡頭（稿子『張嘴想罵又閉上、抓回帳冊、轉身』在第一格完成；帳冊不寫），甩一下右寬袖、大步往遠處松樹走遠（稿子『往右邊走、走兩步回頭一指』改成一路走遠）；台詞是錄音（答 s27：無話可回，轉身走）。家丁不寫"),
    dict(loc="q4", cam="Wide shot from a little above, slow push in", chars=["xuyan"], night="xi",
         comp=f"wide shot from a little above, like the picture: the long dry channel now dug all the way to the line of dark pines at the far end; on the left bank, walking away toward the far end in a loose line, {HOMEGOING}; standing on the single plank laid across the channel in the middle distance, {XU_DAY}, framed full figure, small, his face three-quarter to screen left along the channel toward the far pines, never the lens; tired and quiet, not smiling, lips pressed shut; {HANDS}; exactly seven people",
         lines=[("xitong", "叮。以工代賑，達成。", "冷，宣布")],
         panel=[("以工代賑，達成", "task")],
         motion=f"Xu Yan turns his head slowly along the whole length of the channel and lets out one long slow breath, his shoulders easing; {SILENT_HE}",
         zh="全景（略俯）、慢推（送本集免費做的 `set-shanjiao-qu-xi2-l1`：清乾淨的圖重調成傍晚琥珀光、天上一層橘，獨立審稿建議 7）：約第一七五天傍晚（半個月）。渠已經挖到遠處那排松樹（稿子『挖到山腳』照圖）；左岸六個收工的人扛著鋤頭往遠處走（背影，每人衣色不同）；許硯站在渠中段那塊橫在渠上的木板上（稿子『渠頭的土埂』：圖上是木板；直立的木板已塗成一根細木樁，建議 6）、回頭看整條渠、慢慢吐一口氣；系統是錄音、**全程嘴閉著**；面板『以工代賑，達成』跟系統念的一字不差，剪接時疊，**不寫淡藍光**（拍法 11）"),
    dict(loc="q4_b", cam="Medium shot, slow push in", chars=["xuyan", "qinshuang"], night="xi",
         comp=f"medium shot on the flat dry ground of the left bank at sunset: at the left, {XU_DAY}, standing, framed from the waist up, his face three-quarter to screen right toward her, his lips pressed shut, never the lens; quiet, not smiling; at the right, {QIN}, already stepped up beside him from the first frame, framed from the waist up, her face three-quarter to screen left toward him, never the lens; cool and watchful, not smiling: eyes narrowed, lips moving short and firm between words; behind them, soft, the flat dry field and the line of dark pines, and far beyond them at the left, soft and out of focus, {SPIES3}; {HANDS}; exactly five people",
         lines=[("qinshuang", "渠通了，那三個人還沒走。今晚我守院子。", "淡淡的，篤定")],
         motion=f"Qin Shuang glances once toward the three far backs and pulls her wide leather belt tighter with both hands as she speaks, and Xu Yan gives one small nod; {quiet('Xu Yan')}",
         zh="中景、慢推（送本集免費做的 `set-shanjiao-qu-xi2-zhuo-l1`：傍晚的左岸平地與松樹，獨立審稿建議 9：三個背影要有地可走）：秦霜第一格已經走上來站在許硯右邊（稿子『走上土埂』在第一格），看一眼畫左遠處虛焦的三個背影（探子：本色破衣、扛鋤頭、一起走遠；聖經〈小角色〉只拍背影），兩手把寬皮帶勒緊（稿子『把柴刀往腰帶裡推緊』：柴刀不寫，拍法 5）、說；許硯點頭、嘴閉著（第二場結尾）"),
    # ---- scene 3: the Xu yard, the night of the same day, the third watch (36->37).
    dict(chapter="許家院子，半個月後的夜", loc="ny", cam="Low-angle wide shot, slow push in", chars=["qinshuang"], night="night",
         comp=f"low-angle wide shot from low beside the woodpile, like the picture: the ends of the split firewood stacked against the house front soft in the left foreground; {QIN}, framed full figure, already risen to her feet off the woodpile from the first frame, standing in the yard at the left; along the foot of the back wall at the right, {SLEEPERS}; {HANDS}; exactly ten people, Qin Shuang and the nine sleeping men",
         motion=f"Qin Shuang turns her head toward the back wall and walks step by step across the yard toward it, her footfalls light; {quiet('Qin Shuang', 'her')}",
         zh="低角度全景、慢推（照圖；送 e931 的免費圖 `set-xujia-yuan-ye-dong2-l1`：屋與屋門在左、柴堆靠在屋前、院門在後牆中間、院門右邊一棵光禿的樹、後牆往右延伸、井在前右、院子中間一隻木桶、牆外暗田遠山）：**拍法 42 改 CG 稿的格局**：稿子『井在左前、院門在右、東牆在左、柴堆在院門內側右』照真人圖：柴堆在左邊屋前，**草蓆在後牆右段（樹右邊到右牆角、井後面）牆下**一排十二張並排、頭朝牆（獨立審稿必改 8：頭尾相接放不下），九個流民背對鏡頭蜷著睡、中間三張空的（聖經〈道具〉草蓆；原版：三張空蓆）；秦霜第一格已經從柴堆上站起來（稿子『聽見一聲輕響、站起來』在第一格；輕響交給音效），轉頭、一步一步走向後牆。樹照圖寫光禿的樹（聖經〈場景〉晚春夜院子：接受光禿的樹）。冷月光。無台詞"),
    dict(loc="ny_w", cam="Close-up, point of view looking down, slow push in", chars=[], night="night",
         comp=f"point-of-view close-up looking down, the very first frame is already a close view of three empty straw mats lying side by side on the packed earth, their heads against the foot of the low earth-and-stone wall, each pressed flat with a shallow hollow in the middle where a body lay; the curled back of a sleeping man under a ragged blanket soft at the left edge and another soft at the right edge, both turned to the wall; a young woman's right hand in a dark brown sleeve coming in from the top of the frame and resting flat on the middle mat; {HANDS}; exactly two sleeping men, their backs toward us",
         lines=[("qinshuang", "三張蓆子空了，還是熱的，人剛走。", "壓低聲音")],
         motion=NOBODY + "the hand presses down flat on the empty mat and stays still there, the two sleeping men breathing slowly",
         zh="主觀（秦霜低頭看草蓆）、慢推（送本集免費做的 `set-xujia-yuan-ye-dong2-qiang-l1`：後牆右段、牆外暗田、右下井的轆轤）：第一格就是三張空蓆（中間壓出淺凹痕），左右緣兩個睡著的人的背（虛焦、臉朝牆）；秦霜的右手（深褐袖口，不點名）從畫面上方伸進來按在中間那張蓆上、停住。稿子『旁邊沒有鞋』不寫（拍法 18：不寫否定名詞）。秦霜的話是畫外錄音"),
    dict(loc="ny_w", cam="Low-angle medium shot from behind, slow push in", chars=["qinshuang"], nospeak=["qinshuang"], night="night",
         comp=f"low-angle medium shot from the yard: {QIN}, seen from behind, already crouching up on top of the low earth-and-stone back wall from the first frame, framed from the waist up, her back and the back of her head toward us, high against the deep blue night sky and the dark far hills; she is the only person in the frame; {HANDS}",
         lines=[("qinshuang", "鼓聲……是從山上傳下來的。", "很低，警覺")],
         motion=f"Qin Shuang's head snaps up toward the far dark hills beyond the wall, and she stays crouched there, still, her back toward us; {quiet('Qin Shuang', 'her')}",
         zh="低角度中景（從背後）、慢推（送 `-qiang-l1`）：秦霜第一格已經翻上後牆右段的牆頭蹲著、背對鏡頭（聖經〈接點〉36→37：背對鏡頭、面向牆外的山；稿子『一腳踩上牆下的井沿、一腳蹬牆、翻上牆頭』在第一格完成——井在前右、不在牆下，拍法 42；稿子的跟拍往上改慢推），猛地抬頭望向牆外的遠山（一個動作；遠處鼓聲交給音效）；她背對鏡頭，台詞放錄音（nospeak）"),
    dict(loc="ny_c", cam="Medium shot, slow push in", chars=["xuyan"], night="night",
         comp=f"medium shot in the middle of the yard: {XU_COAT}, {LAMP} held in his left hand, already arrived from the house door at the left from the first frame, framed from the waist up, the small flame lighting one side of his face, his face lifted three-quarter to screen right toward the top of the back wall beyond the upper right edge of the frame, his eyes on it, never the lens; he is the only person in the frame; tense, not smiling: brows drawn, eyes sharp, lips moving quick and low between words; behind him, soft, the split firewood stacked against the house front and the yard gate in the dark; {HANDS}",
         lines=[("xuyan", "鼓聲哪來的？那三個新鞋的人呢？", "急，壓低")],
         motion="Xu Yan stops short, the lamp flame swaying, and lifts his face toward the top of the wall as he speaks",
         zh="中景、慢推（送本集免費做的 `set-xujia-yuan-ye-dong2-chai-l1`：屋前柴堆、窗、院門）：許硯（夜裡外披舊灰外衣，聖經〈人物〉）左手一盞陶油燈（一朵火，聖經〈道具〉；第 36、37 集院子夜裡）第一格已經從畫左的屋門走到院子中間（稿子『快步走出來』在第一格；剪接照稿子從快步走出屋門開始，改成從停步開始），停住、燈火一晃，抬頭朝畫右上外的牆頭（寫牆頭，不寫秦霜，拍法 31）急問（→ 答在 s35）。燈光照半邊臉、不笑"),
    dict(loc="ny_w", cam="Low-angle medium shot, slow push in", chars=["qinshuang"], night="night",
         comp=f"low-angle medium shot from the yard of {QIN}, crouching on top of the low earth-and-stone back wall, framed from the waist up, high against the deep blue night sky and the dark far hills, her face already turned back over her left shoulder from the first frame, looking down {off('lower left', SIDE_NIGHT, he='she')}; cold, not smiling: eyes narrowed, brows level, lips moving short and hard between words; {HANDS}",
         lines=[("qinshuang", "翻牆走了。他們不是流民，是來探路的。", "冷")],
         motion="Qin Shuang speaks down over her left shoulder, then turns her face back toward the far dark hills beyond the wall",
         zh="低角度中景（從院子仰拍牆頭）、慢推（送 `-qiang-l1`）：秦霜蹲在牆頭，第一格已經回過頭、從**左肩**（獨立審稿必改 5）往畫左下外看不到的人（許硯，不點名；稿子『許硯在畫面下緣只露頭頂與燈光』不寫，拍法 31）冷冷地說，說完轉回去盯著山（答 s34）；不笑"),
    dict(loc="ny_w", cam="Wide shot, point of view, slow push in", chars=[], night="night",
         comp=f"point-of-view wide shot from the top of the back wall, the warm-lit top of the low earth-and-stone wall soft along the bottom edge of the frame: beyond it the dark fields and the far dark hills under the deep blue night sky, a few bare twigs at the top left; far away on the dark hillside, {FIRELINE}; only the wall top, the twigs, the fields, the hills and the small far flames are in the frame",
         motion=NOBODY + "the long thin line of small orange flames creeps on down the hillside, rounds a bend and stretches longer toward the foot of the hills",
         zh="主觀（從牆頭望向山）、慢推（送本集免費做的 `set-xujia-yuan-ye-dong2-shan2-l1`：16:9 的牆頭、暗田與遠山，左上幾根枯枝；獨立審稿建議 8：`-shan` 被拉長 1.33 倍、有樹幹與瓦頂）：前景下緣是牆頭（稿子『牆頭的土磚』照圖：土石矮牆）；遠山上一長串小火光往山腳流、拐一個彎越拉越長（拍法 37 的寫法：不寫人數、不寫拿火把的人）；鼓聲交給音效。剪接照稿子剪在火光拐彎的時候。無台詞"),
    dict(loc="ny_d", cam="Medium shot, slow push in", chars=["aling"], night="night",
         comp=f"medium shot at the dark doorway of the farmhouse: {ALING}, already stopped on the wooden threshold of the dark doorway from the first frame, framed from the waist up, her face three-quarter to screen right toward the far hills beyond the right edge of the frame, her eyes on them, never the lens; she is the only person in the frame; grave and still, not smiling, her lips closed; behind her the dark doorway; beside her, soft, the split firewood stacked against the house front in the faint warm glow; {HANDS}",
         motion=f"A-ling's right hand slides slowly into her left sleeve and stays there; {quiet('A-ling', 'her')}",
         zh="中景、慢推（送本集免費做的 `set-xujia-yuan-ye-dong2-wu-l1`：屋左邊的黑門洞與旁邊的柴堆）：阿令（長袖、木簪）第一格已經從屋裡出來、停在門檻上（稿子『走出來』在第一格；剪接照稿子從踏上門檻開始），看著畫右外遠山的火光，右手慢慢縮進左袖、停住（稿子『按住袖裡的短匕』：短刀只在第 37 集，聖經拍法 22，不寫刀字）；不笑、嘴閉著。無台詞"),
    dict(loc="ny_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="night",
         comp=alone(f"her left hand already gripping his right sleeve from the first frame; {BEYOND_XU}, {XU_COAT}, {LAMP} held in his left hand, standing, framed from the waist up, his face in profile to screen right, lifted toward the top of the back wall and the far hills, his lips pressed shut, never the lens; tense, not smiling; behind them, soft, the wooden bucket, the bare tree and the yard gate in the dark; she stays in the middle of the frame the whole shot; {HANDS}; {TWO_BACK}",
                    "standing in the middle of the yard,"),
         lines=[("tangxiaotang", "幾百支火把……全往我們村子來了？", "聲音發抖")],
         motion=f"her left hand grips his sleeve tighter and tugs it once toward her, only her arm moving, and Xu Yan's hand closes tighter round the lamp; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送本集免費做的 `set-xujia-yuan-ye-dong2-zhong-l1`：院子中間、木桶、樹、院門）：稿子 c38 唐小棠『抬頭看他、臉色發白』照拍法 40 從背後拍：她背影在畫面正中、頭不動（l1 交領短襦，**不寫淡杏外衣**，拍法 4），左手第一格已經抓住許硯的右袖（她在他右邊，聖經〈接點〉36→37），抓緊、晃一下（只動手臂）；許硯在畫左三分之一、提油燈、側臉朝畫右上望牆頭與遠山、握緊油燈、嘴閉著。她的話是錄音（本集結尾；懸念 → 第 37 集第一場：二牛撞開院門「四百人！」）。配樂停在最高點不收"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e036-r2/script.md`（c01–c38 對應 s01–s38，加兩個拆鏡 s11b、s12b，共 40 鏡；含「這版改了什麼」「2026-11-06 審稿後的修改」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e031-e040.md`（拍法 1–43 條、〈場景〉〈接點〉〈道具〉〈小角色〉），帳照 `r2-bible-e011-e060.md`。**第 4 篇章〈旱年〉第 6 集**：約第一六〇天傍晚（村口，接第 35 集同一刻）→ 第一六一～一七五天（山腳新渠）→ 第一七五天夜三更（許家院子）。",
    "- 內部工作編號 936（`hailuo/{ff,clips}-dh-e936.json`；`colab/runs/e936/extras.json`、`colab/runs/e936-live/spec.json`、工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e936-dh/`）；發布 slug `zhong-tian-qu-qi-e036-r2`。不放集數、不放片名卡；**s01 接第 35 集定版成片 `e935-live.mp4`（218.93 秒）的最後一鏡**（s34 許硯走到門閂前、阿令在他左邊同排、唐小棠右後、守門兩人各拿火把；s35 右手按門閂）；s38 交給第 37 集（同一刻：二牛撞開院門）。",
    "- 照第 35 集的審稿、挑片與修片的教訓一開始就照做：參考圖跟文字一致（本集的新圖都是免費裁切與調色、新 id）；柵門要關著的鏡（s01）結果先寫兩次，s02 之後不送門扇關著的圖；錢員外要喊的鏡正面（逐部位寫不笑）、咬牙退場的 s28 一開始就背影＋錄音；許硯不寫鬍渣；風格句不寫 cinema camera（`pilot.py` 已改，`mkspec.py` 的錨點也改）；不寫 crowd、hundreds、villagers，寫實際人數；不寫泥（『袍子沾泥』寫成淡淡的乾土）；`OFFSCREEN_SPEECH = False`、對畫外的人說話寫「朝畫左／右外看不到的人」；不寫 open、不寫否定名詞；extras 的「air is clear and still」逐鏡換掉（mkspec）；長東西第一格分開（鋤頭、門閂、毛筆與紙）。",
    "- **人物**：**唐小棠**（拍法 3、4、20、40）：說話的五鏡（s07、s14、s18、s27、s38）一律從背後拍（畫面正中、正背對、頭不動、剛好兩顆丸子；l1 交領短襦，**不寫 t2 高立領、不寫淡杏外衣**），s05（金算盤插鏡）與 s16（阿令寫名冊）她的話是畫外錄音；過肩前景的雙丸子後腦（s06、s12b）與 s01 的小背影不點名、不送圖；**本集沒有她的正臉**。**秦霜**：柴刀不寫（拍法 5；c24、c30 改成手按、勒緊寬皮帶）；s33 背對鏡頭在牆頭、台詞錄音。**阿令**：第一場照第 35 集（袖口紮緊、綁腿、竹哨），s12 把竹哨收進袖裡；第二場起長袖放下；c37『按住袖裡的短匕』只寫手縮進袖裡（拍法 22）。**錢員外**：s03、s04、s26 喊（逐部位寫不笑）、s10 冷笑、s28 背影＋錄音；家丁不寫（拍法 34）。**三個探子**只拍腳（s22）、手（s23）、背影（s30）、空蓆（s32）。",
    "- **軸線（照圖）**：村口照 `set-cunkou-zha2-l1`（第 35 集付費改的那張）：柵門在**左**、垂柳在中、木板橋與乾溝、土路往**右**到三間屋；鏡頭在村裡。**沒有門樓**：錢員外站在柵門旁的土台上（第 35 集 s31）。新渠照 `set-shanjiao-qu-l1`：乾渠從前景**筆直往遠處**延伸（稿子『由右往左』是深度）、**左岸**新土堆與乾草、平坦乾黃地與遠處松樹（稿子的山腳）、**右岸**乾草與青秧田；帳桌在左岸平地（唐小棠右端、阿令左端）；秦霜沿右岸秧田來、兩人在右岸說話。院子照 `set-xujia-yuan-ye-dong2-l1`（拍法 42）：屋與屋門在**左**、柴堆在屋前、院門在後牆中間、**草蓆在後牆右段牆下**、井在前右；秦霜在後牆右段牆頭背對鏡頭。",
    "- **時間與光**：第一場傍晚橘紅天加火把（第 35 集同一刻）；第二場開工頭幾天上午白光（s13–s20）→ 約第一六六天正午（s21–s25）→ 約第一七〇天午後（s26–s28）→ 約第一七五天傍晚斜陽（s29–s30，本集免費做的 `-xi`）；第三場夜三更冷月光。時間跳都在剪點（s12b→s13、s20→s21、s25→s26、s28→s29、s30→s31），不在鏡頭裡變光。",
    "- **原版必修**：第 36 集無必修；院子照拍法 42 改、三個探子只拍腳手背影（聖經〈原版必修〉）。原版建議：開門是橘紅傍晚（s01）；『不說話的女人』時許硯不笑、眼神往帳桌一瞥（s25）；唐小棠『幾百支火把』不笑（s38，從背後）、秦霜牆頭冷臉（s35）；名冊虛焦（s17：拍法 38 更嚴，紙面空白）；虎口的繭寫成粗糙發黃的硬皮、指節舊疤（s23）；三張空蓆（s32）；錢員外糧價跌有原因（s27）、說的時候不笑（s26）。",
    "- 要買的秒數（BUY，錄音前照第 35 集實測估：一句 6 秒的鏡放得下約 5.9 秒人聲、8 秒約 7.3 秒、10 秒約 9.2 秒；第 35 集量到許硯約 4 字／秒、唐小棠中位 3.4、阿令 3.4、錢員外 2.2–2.9、系統 9 字約 2.4 秒）：**s26、s11 買 10 秒**（錢員外 18 字；心裡話 19 字加系統 9 字約 7.3–7.7 秒）；s30（秦霜 16 字兩句、在畫面上說，獨立審稿必改 9）、s03、s04、s10、s24、s28、s35、s09 買 8 秒；s02、s31 買 6 秒（無台詞、兩拍）；s15、s17、s36、s37 買 5 秒（插鏡與無台詞）；其他說話鏡 6 秒。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音的人聲長度為準。",
    "- **新渠（s13–s30）表上的提示詞帶「below the deep pool」**：只為了讓 `gen-dh` 的 `SET` 選到深潭那張圖（再由 `spec.json` 換成新渠的圖；`new channel` 會選到 `set-xinqu`，真人版沒有那張、`pilot.py` 會停），d1 由 `mkspec.py` 拿掉（`R2.POOLMARK`→空）；**之後每個 fix／retake spec 都要帶同一組替換**，不然模型會在渠邊畫出潭。院子的提示詞帶「night yard of the Xu farmhouse」讓 `SET` 選到 `set-xujia-yuan-ye`（l2），`spec.json` 一律換成 `-ye-dong2` 與它的裁切。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯 l1、angle-a（帶笑的 angle-b 整集不送；全景與背影 s01、s02、s09、s13、s29 只送 l1）；唐小棠她的三張圖全集都拿掉（沒有正臉）；阿令 l1、angle-a（angle-b 不送；s01 背影只送 l1）；秦霜 l1、angle-a（angle-b 不送；s31 全景與 s33 背影只送 l1）；錢員外 l1、angle-a（angle-b 不送；s28 背影不送、不點名）。過肩前景的背影（s06、s12b 雙丸子；s25 秦霜的肩）、s01 唐小棠的小背影、守門兩人、流民、挖渠的人、探子、睡著的人都不送圖。",
    "- **場景圖**（獨立審稿後）：村口送第 35 集的免費裁切 `set-cunkou-zha2-men-l1`（s01，門關著）、`-dao-l1`（s08、s09、s12）、`-kong-l1`（s11、s11b）與本集免費做的 `-ding2-l1`（s03、s04、s10：只有瓦頂與天）、`-wai2-l1`（s02（付費開門圖 `-kai-l1` 挑定前）、s06、s07、s12b：沒有門扇）、`-di-l1`（s05 插鏡，只當地面）；新渠送本集免費做的清乾淨版 `set-shanjiao-qu-jing-l1`（s13：護欄塗掉、直立木板改成細木樁）與 `-zhuo2-l1`（s14、s16、s18、s19、s20、s26、s27、s28）、`-tian2-l1`（s21、s24）、`-xi2-l1`（s29）、`-xi2-zhuo-l1`（s30），未清的 `-an-l1`（s23、s25）、`-di-l1`（s15、s17、s22，插鏡只當地面）；院子送第 31 集的 `set-xujia-yuan-ye-dong2-l1`（s31）與本集免費做的 `-qiang-l1`（s32、s33、s35）、`-chai-l1`（s34）、`-shan2-l1`（s36）、`-wu-l1`（s37）、`-zhong-l1`（s38）。",
    "- **本集新做的圖**（2026-11-20，`live-action/free-e031-e040/`，各跑兩次逐位元一樣，寫進 refs-live README）：`shanjiao_qu.sh`（新渠四張裁切、傍晚調色與它的一張裁切）、`xujia_yuan_ye_e936.sh`（夜院子五張裁切）、`cunkou_zha2_e936.sh`（村口土路一張）。**不花錢**；沒有付費圖。",
    "- **還缺、先用最接近的圖**（不花錢、註明在這裡）：(1) **門樓**：圖上沒有，錢員外站土台（第 35 集同）。(2) **新渠的圖沒有山**：遠處是一排松樹，稿子的『山腳』照圖寫成松樹那頭；渠是往畫面深處去的，不是由右往左。(3) **夜院子偏 CG、暖光**（e931 的圖）：文字寫冷月光加屋牆一點暖光。(4) **柿子樹光禿**（聖經已定接受）。(5) 竹籌、算盤、金算盤、毛筆、紙、石碟、鋤頭、竹筐、草蓆、油燈、火把是文字加在圖上。",
    "- 共用檔：沒有改（`build-r2.py` 的 `EN` 已有每個在畫面上說話的名字）；`gen-dh.mjs`、`pilot.py`、`cast.json` 不動。對畫外說話、對牆頭、對紙說話的鏡，精修文字的通用說話視線由本檔結尾的 `live_clips()` 換成 d1 的方向句（`GAZE_REFINE`）；唐小棠的背影鏡：立領句拿掉、名字換成「從背後看的年輕女子」（同第 31、33、35 集）。",
    "- **自審**（2026-11-20，`writer-tools/e036-r2/review.md`，不是獨立審稿）；給獨立審查者的提示在 scratchpad `e936prep/review-prompt.md`，由協調者派。",
    "- **獨立審稿**（2026-11-20，`writer-tools/e036-r2/review-independent.md`）：必改 9 條全改（s02 不再送門扇關著的圖、火把點名誰拿、s02 之後的 `-ding`／`-wai` 換成沒有門扇的 `-ding2`／`-wai2`、s18 不傾身、s35 從左肩回頭、渠約膝深、`-zhuo` 的護欄塗掉、草蓆並排頭朝牆、BUY s30 8 秒）；建議 1、3–10 照改；建議 2（付費開門圖）協調者定做、本代理的 Colab 呼叫被自動權限擋下、`e936kai.sh` 備好；建議 11 等錄音；建議 12 記進聖經〈接點〉36→37。見 `colab/runs/e936-live/PREP.md` §7。",
    "- **d1 前置**（2026-11-20，`colab/runs/e936-live/PREP.md`）：`colab/runs/e936/extras.json`、`colab/runs/e936-live/{mkspec.py,spec.json}`（種子 9361101／9361102）、scratchpad `tools/prep936.sh`、`tools/rec936.sh`（錄音）、`e936d1.sh`（Colab，**沒跑**）。",
    "- 配樂：第一場低沉的 strings，s02 開門轉溫暖的弦樂，s09『一鋤頭換一碗飯』一個重音；第二場明快的勞動節奏（鼓與鋤頭聲），s18 古琴一聲，s21 起低沉的懸疑弦樂，s29 面板一個重音；第三場幾乎無聲只有蟲鳴，s33 遠處鼓聲，s36 火把一個大重音、停在最高點不收。音效見 script.md〈音樂與音效〉。",
]

# Seconds to buy, estimated from e935's measured lines (PREP §4 there): a 6 s shot holds about 5.9 s of speech, 8 s about 7.3 s,
# 10 s about 9.2 s; Xu Yan about 4 characters a second (thoughts 4-4.3), Tang Xiaotang median 3.4, A-ling 3.4, Qian Yuanwai
# 2.2-2.9, the system 9 characters in about 2.4 s; Qin Shuang (Autonoe) not measured in arc 4, estimated at 3.5-4.
# 10 s: s26 (Qian Yuanwai 18, urgent: 6.2-8.2 s), s11 (thought 19 + system 9 with a pause: 7.3-7.7 s, past an 8 s clip's 7.3).
# 8 s: s03 (Qian 13 shouted, two stops), s04 (Qian 15), s10 (Qian 15, sneered and drawled),
#      s30 (Qin 16 in two sentences on screen: 4.3-6.2 s at her measured 3.7 / 2.3-2.9 a second, review 必改 9), s24 (Qin 17 word by word), s28 (Qian 14, the back), s35 (Qin 17, cold, two sentences), s09 (Xu Yan 18 with stops).
# 6 s: s02, s31 (no line, two beats); every other spoken shot (gen-dh's default, written out for the recordings over a shot).
# 5 s: s15, s17 (the inserts), s36, s37 (no line).
BUY = {"s26": 10, "s11": 10,
       "s30": 8, "s03": 8, "s04": 8, "s10": 8, "s24": 8, "s28": 8, "s35": 8, "s09": 8,
       "s02": 6, "s31": 6, "s01": 6, "s05": 6, "s11b": 6, "s16": 6, "s22": 6, "s23": 6, "s29": 6, "s32": 6, "s33": 6,
       "s15": 5, "s17": 5, "s36": 5, "s37": 5}


# ---- the refine text (as e031, e033, e935): hailuo/clips-dh-e936.json column 0 is the motion text refine-prep.py sends with a
# picked d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era "Tang Xiaotang's high stand-up collar
# stays closed at her throat." and names her in "<names> shown in <Picture 1>"; in a back shot that draws the collar back and
# turns her face to the lens. Her back shots: the sentence goes and her name becomes "the young woman seen only from behind",
# with someone else: "keep the same face, hair, costume and props as the first frame, the young woman's back to us"; alone:
# "keeps the same hair, costume and props as the first frame, her back to us" (e031). FRONT_TANG is empty (no front face).
# Column 1 is recomputed. prep936.sh hands stage 1 the anchor form (anchor_form(), e028 review 必改 1; rule 39).
COLLAR = "Tang Xiaotang's high stand-up collar stays closed at her throat. "
FRONT_TANG = set()
# rule 31 (e030 review 建議 10): gen-dh's speaking gaze names "the person he/she is speaking to", who is not in the frame of these
# shots (or is a thing: the paper, the top of the wall); the refine text gets d1's direction. anchor_form() puts gen-dh's words
# back for stage 1.
GAZE_GEN = {"he": "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person",
            "she": "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"}
_LR = "his face three-quarter to screen right, looking down toward someone out of sight beyond the lower right edge of the frame, his eyes on that spot"
# sid -> (pronoun, the direction sentence)
GAZE_REFINE = {
    "s03": ("he", _LR),
    "s04": ("he", "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"),
    "s10": ("he", "his face looking back over his right shoulder, down toward someone out of sight beyond the lower right edge of the frame, his eyes on that spot"),
    "s19": ("she", "her face lowered three-quarter to screen right toward the blank paper below the frame, her eyes on it"),
    "s24": ("she", "her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, her eyes on that spot"),
    "s26": ("he", "his face three-quarter to screen left, looking down toward someone out of sight beyond the lower left edge of the frame, his eyes on that spot"),
    "s34": ("he", "his face lifted three-quarter to screen right toward the top of the back wall beyond the upper right edge of the frame, his eyes on it"),
    "s35": ("she", "her face turned back over her left shoulder, looking down toward someone out of sight beyond the lower left edge of the frame, her eyes on that spot"),
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
# live_clips() writes no longer matches it. prep936.sh hands stage 1 the anchor form of the live file (this), then puts the
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
