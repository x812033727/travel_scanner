"""Episode 18 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e018-r2/script.md
(c01-c40 = s01-s40; the CG-era r2 script of PR #2024), including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and
「真人版的改動（2026-11-16）」, which override the tables. Every line is the script's, word for word; only the staging changes (the script's c37 is two shots here, s37 and s37b: its two
recordings run 11.4 s of speech, more than one 10 s clip holds; see BUY).
Bible: production/r2-bible-e011-e020.md (rules 1-18).

Live action from the first draft, written the way e017-r2/r2.py stands AFTER its independent review (review.md in ../e017-r2:
15 必改 and the 建議) and the e913-e916 picking lessons (colab/runs/e91{3,4,5,6}-live/{review-picks-a,review-picks-b,
picks-merged}.tsv, the e914/e915 notes of tasks/open/2026-11-07-zhong-tian-live-action-remake.md, refs-live/README.md):
- OFFSCREEN_SPEECH = False (bible rule 15): every shot with an off-screen line, a thought or a system line writes the silence
  of each person on screen (quiet(), SILENT_HE), after the action.
- Bible rule 18: nothing is negated by name; backgrounds say what is there. Paper is never read: the ledger page is held with
  its blank back to us and lit from our side (s06), folded (s05, s09); the ledgers are closed, their covers plain. A face that
  must not smile gets things it does, held after the last word.
- Hands and props are placed in the composition sentence (the first frame), each prop attached to its owner's named hand: the
  cloth bundle in Xu Yan's hands (s01) and under his left arm (s14), the silver in Tang Xiaotang's right hand (s04), the folded
  page in the bookkeeper's fingers (s05) and in Tang Xiaotang's right hand (s09), the brush in Xu Yan's right hand (s15), the
  bamboo strip in his right hand (s16), the third stone in Qin Shuang's right hand (s17), the box in Lai San's arms (s19-s23),
  the wire in Qian Yuanwai's right hand (s24), the rope already round Lai San's wrists (s30), the gavel block under Magistrate
  Hu's right hand (s32, s37), the closed ledger in Tang Xiaotang's arms (s31, s33). Contact between two people starts as a
  state in the first frame, never as a grab: Xu Yan's hand already on Qin Shuang's forearm (s21), Qin Shuang already holding
  Lai San against the wall (s28, s30), Qian Yuanwai's sleeved wrist already hooked over Xu Yan's forearm (s40).
- Gestures: no pointing finger (e916 s26 read as a rude gesture): Xu Yan's accusations (s33, s35) are an open hand, palm up.
- Tang Xiaotang never speaks on camera (bible rule 3): her six on-screen lines (s03, s04, s06, s09, s13) are said from behind
  her (TBACK, nospeak; spec.json drops her three face pictures and her identity sentence), always the only young woman with
  two buns, on one fixed side (the right foreground: she sits at the right of the tea table); s07 is Xu Yan's listening face
  with her line off screen. Her silent face (s01, s31, s33) gets e907's neutral face sentences in spec.json. Costume: the
  live portrait l1, cross-collared and closed, no outer coat (bible rule 4).
- The Qian bookkeeper has no portrait (script): only his back (s01, s04, s11) and his hands (s05, s12), never his face; his
  one line is s05's, off screen over his hands (MINOR voice, recorded).
- No weapon anywhere (bible rule 5): Qin Shuang's belt is empty (extras.json), s21's hand on the knife becomes her hand on the
  woodpile; the yamen men are left out of the hall altogether (rules 16-18: a written background man grows a blade or a
  staff; their 「威武」 is a sound); the gavel block is a flat oblong block of wood, never a mallet.
- Red hands (bible rule 12): an even orange-red from fingertips to wrists like dye, never blood or a wound; written as a state
  from the first frame of s26 (Qian Yuanwai) and s28 (Lai San), never as a change on screen. By day Qian Yuanwai's hands are
  inside his sleeves in every shot (s31-s40) and his cast sentence's gold rings go (spec.json).
- Magistrate Hu and Qian Yuanwai (two plump round-faced middle-aged men) are never in one frame (bible 同框撞臉).
- No more than three named faces in a shot (bible rule 1).
- Night is night: s15-s18 one small clay oil lamp on the work table; s19-s22 after it is blown out, the faint cool blue of a
  starless sky; the lane s23, s27-s30 lit only by the thin line of lantern light from the gap of the back gate; s24-s26 the
  lantern-lit passage inside the manor.
- Nobody is flipped in the edit: every speaker wears a cross collar; sides are written as screen left/right.
State at the junction (e017 r2.py s40): dawn of day 12 at the new frame; Xu Yan, soot and sweat on his face, the charred lantern
in his right hand. s01 is two days later in the teahouse: his face washed, the same lantern wrapped in an old blue cloth.
Places (the coordinator's decisions, 2026-11-16; listed again in script.md 〈真人版的改動〉; every picture looked at full size):
- the teahouse set-chalou-l1 (37002, e011-e020 screen test): the staircase along the left wall, a folding screen of four plain
  cream panels at the back with a small side table, the wide open window on the right with grey tiled roofs outside and a
  long bench under it, the square tea table with one brown clay teapot and two cups in the middle. The script's small table
  by the window is the bench under the window (the bookkeeper sits on it, his back to us). s01-s14.
- the new paper workshop at night: NO set picture (spec drop_set, s15-s22). set-zhifang-gujia-ye-l2 (37020) has the frame
  half up, a bonfire and two lanterns (e017's night: the wrong state two days later), set-zhifang-gujia-chen-l1 is dawn
  (bible rule 8: a day picture makes night day). The workshop is written plainly in WORK: the four pale pine posts of
  e017's dawn picture, the left half of the roof newly thatched, a plain work table in the middle, a low stack of split
  firewood at the front left, the bamboo fence with a gap on the right; one small clay oil lamp, then the dark.
- the lane behind the Qian manor at night: NO set picture (drop_set, s23, s27-s30); set-qianfu-houmen-ye-l1 (37004) is the
  passage INSIDE the back gate (a long white wall on the left, a covered walkway with glowing lanterns on the right, a round
  stone table in a small pavilion at the far end), which is exactly what Qin Shuang sees through the gap: s24 sends it
  (swap_pictures in place of set-qianfu-ting-l1, the hall, which gen-dh's "Qian manor" line gives). Its wall has a row of
  eave shadows that read as people (README): the text says the wall is smooth and evenly lit. Inserts s25, s26 send none.
- the yamen court hall set-xianya-gongtang-l1 (37001): a low platform at the back with one long desk and an armchair before a
  wall of plain white panels, a gilt-framed board above, thick dark red-brown pillars, tall lattice windows on both sides,
  grey stone tiles. s31-s38 send it (swap_pictures in place of set-xianya-l1, the gate, which gen-dh's "county yamen" line
  gives). The script's door on the left is not in the picture: the grey daylight comes from the windows.
- the side room set-xianya-ceting-l1 (37002): a long grey curtain in the doorway on the left, a long table and two armchairs
  against a plain grey wall, one tall lattice window on the right. s39-s40 (swap_pictures in place of set-xianya-l1).
- gen-dh.mjs, build-r2.py and cast.json are NOT changed: "teahouse" already maps to set-chalou; the three yamen and manor
  pictures go in through spec.json swap_pictures (applied by prep918.sh with absolute paths); the bookkeeper's voice is MINOR.
No screen test is needed: every place has a usable picture or is written without one.
"""
EP = 918  # internal working number; the published slug is zhong-tian-qu-qi-e018-r2
SLUG = "zhong-tian-qu-qi-e018-r2"
EP_TITLE = "一頁帳、一只錢箱、一雙紅手（重製版 r2）"
OUTLINE_SECONDS = 207.5  # script.md: 207.5 s, 40 shots (14 + 16 + 10); live: 41 (c37 split into s37 and s37b)
TARGET_MINUTES = [3, 4]
TITLE = "一雙紅手｜種田娶妻打天下 第18集（重製版）"
DESCRIPTION = "兩天後，縣城茶樓。強制任務只剩五日，賴三躲在錢府不出門。唐小棠用一兩銀子向錢府的帳房買下帳上一頁：收魏記，銀三百兩；紙坊起火前一天，付賴三，五兩。錢員外背後還有人出錢。許硯故意大聲說，賣紙的銀子跟造紙方子今晚都鎖進新紙坊的錢箱，帳房放下茶杯就走。當夜，箱面刷薑黃水、鎖扣抹草木灰水，裡面只有三塊石頭。賴三果然來偷，一路抱進錢府後門；秦霜從門縫看見錢員外親手撬開鎖扣，兩手從指尖紅到手腕，擦都擦不掉。巷口，秦霜按住賴三：人贓俱獲。隔天公堂上，錢員外反告許硯賣紙逃稅，兩手卻一直縮在袖子裡：天、天冷。側廳裡，他用手腕勾住許硯的袖子：放我一馬，告訴你誰推你下河。《種田娶妻打天下》第 18 集（重製版）。"
THUMB = ("一雙紅手", "s26")
CHARACTERS = ["xuyan", "tangxiaotang", "qinshuang", "laisan", "qianyuanwai", "huxianling", "zhangfang", "xitong"]
# The Qian bookkeeper (script: no portrait, back and hands only; bible: a voice to choose). Puck is used by no character of
# arc 2 (Xu Dalang has it from e041): a young, thin, nervous voice, distinct from Xu Yan (Umbriel), Lai San (Zubenelgenubi),
# Qian Yuanwai (Algenib) and Magistrate Hu (Iapetus).
MINOR = {
    "zhangfang": {"id": "zhangfang", "name": "錢府帳房",
                  "appearance": "East Asian man of about twenty-five, thin and narrow-shouldered, an ancient Chinese Song-dynasty clerk's plain dark blue cotton cross-collared long gown and a soft black square cloth cap, thin long fingers, cloth shoes; seen only from behind or as his hands",
                  "voice": {"provider": "gemini", "name": "Puck", "style": "標準國語，咬字清楚，台北人平常說話的語調；二十五歲的大戶人家帳房，男聲、年輕、瘦、緊張，壓著嗓子說話、很小聲、說得快"}},
}
MUSIC = "one cue per scene: a light playful suspense cue of plucked pipa and soft wood blocks in a grey teahouse room in the morning, one accent as a figure is read out, one beat of silence after a loud line; then a low held suspense cue of plucked double bass and soft low drums at night, one heavy accent on a pair of red hands and a soft chime; then a slow heavy cue of deep drums in a county court hall, one hard accent on a gavel block and one low note at the end that fades out; ancient Chinese rural drama, no vocals"

# Scene 1: the teahouse (set-chalou-l1). Scene 2: the new paper workshop at night (no set picture: spec drop_set), then the lane
# behind the Qian manor (no set picture: drop_set) and, through the gap of the back gate, the passage inside it
# (set-qianfu-houmen-ye-l1 swapped in for set-qianfu-ting-l1). Scene 3: the yamen court hall (set-xianya-gongtang-l1 swapped in
# for set-xianya-l1) and its side room (set-xianya-ceting-l1, likewise). Close shots use the short `_c` headers.
# No person's name in a place phrase. gen-dh SET takes the FIRST pattern in its list order that the whole prompt matches: the
# teahouse prompts never say "county yamen", "Qian manor", "ferry", "stream", "willow", "reeds" or "alley"; the workshop prompts
# say "new timber frame" and never "at dawn", "Qian manor", "teahouse", "county yamen", "stream" or "alley"; the lane and
# passage prompts say "Qian manor" and never "Qian manor gate", "alley", "county yamen" or "teahouse"; the hall prompts say
# "county yamen" and never "Qian manor", "teahouse", "ferry landing" or "alley".
TEA = ("dark wooden walls and dark floorboards, a dark wooden staircase rising along the left wall, a folding screen of four "
       "plain cream-white panels against the back wall with one small square side table in front of it, one wide open window on "
       "the right with its lattice shutter folded back, grey tiled roofs of the town and a pale grey sky outside it, one long "
       "plain wooden bench under the window, and in the middle one square dark wooden tea table with one round brown clay "
       "teapot and two small clay cups on it")
# Two nights after e017's dawn: the frame of e017 s36-s40 (four pale peeled pine posts) now half thatched. No set picture.
WORK = ("four tall round posts of freshly peeled pale pine joined by crossbeams, the left half of the roof newly thatched with "
        "golden straw and the right half still open to the black sky; a swept stone floor; one plain square wooden work table in "
        "the middle; a low stack of split firewood at the front left, as high as a crouching man's shoulders; on the right a low "
        "fence of plain bamboo stakes with one narrow gap in it; beyond everything only the dark")
LAMP = "one small clay oil lamp, a shallow dish with one small steady flame, standing on the work table"
DARKBLUE = "the lamp is out: only the faint cool blue light of the overcast night sky, faces and hands just visible"
LANE = ("a narrow stone-paved lane between two high plain whitewashed walls under dark tiled eaves, the mouth of the lane at the "
        "left; in the wall on the right two tall black wooden gate leaves standing a hand's width apart, one thin upright line of "
        "warm lantern light coming out through the gap and falling across the stones; the sky black and starless")
# set-qianfu-houmen-ye-l1 as picked (37004), what is beyond the gate: the passage inside the back gate.
INNER = ("a long straight stone-paved passage, on the left a long smooth white wall evenly lit from top to bottom under dark "
         "tiled eaves, on the right a covered walkway of dark wooden pillars with round white paper lanterns with blank faces glowing "
         "under its eaves, at the far end a small open pavilion with one round stone table, the black night sky above")
# set-xianya-gongtang-l1 as picked (37001).
HALL = ("a floor of large grey stone tiles, thick round dark red-brown wooden pillars, tall dark wooden lattice windows along "
        "both sides, at the back a low dark wooden platform with two red steps at its front, on it one long dark wooden desk and "
        "one dark wooden armchair before a wall of plain white panels, one gilt-framed board above the panels with a plain "
        "blank face")
# set-xianya-ceting-l1 as picked (37002).
SIDE = ("a plain grey plastered back wall, a doorway on the left hung with a long plain grey cloth curtain, one long dark wooden "
        "table against the back wall with one dark wooden armchair at each end, one tall narrow lattice window on the right, a "
        "floor of grey stone tiles")
LOC = {
    "tea": f"In the upstairs private room of a teahouse in the county town on a grey overcast autumn morning: {TEA}; soft grey daylight from the open window on the right",
    "tea_c": "In the upstairs private room of a teahouse on a grey overcast morning, dark wooden walls, soft grey daylight from the open window on the right",
    "work": f"At the new timber frame of the papermaking workshop beside the Xu farmhouse late at night, two nights later: {WORK}; {LAMP}, its small warm light the only light, deep dark night all around",
    "work_c": f"At the new timber frame of the papermaking workshop late at night, deep dark night, the only light the small warm flame of {LAMP}",
    "dark": f"At the new timber frame of the papermaking workshop beside the Xu farmhouse late at night: {WORK}; {DARKBLUE}",
    "dark_c": f"At the new timber frame of the papermaking workshop late at night, {DARKBLUE}",
    "lane": f"In the lane behind the Qian manor late at night: {LANE}; deep dark night, the only light the thin warm line from the gap and the faint cool blue of the night",
    "inner": f"Inside the back courtyard of the Qian manor late at night, seen through the gap of its back gate: {INNER}; the warm light of the lanterns",
    "inner_c": "In the back courtyard of the Qian manor late at night, the warm light of round white lanterns with blank faces",
    "hall": f"In the court hall of the county yamen on a grey overcast morning: {HALL}; soft even grey daylight from the tall lattice windows",
    "hall_c": "In the court hall of the county yamen on a grey overcast morning, dark red-brown pillars and plain white panels, soft grey daylight",
    "side": f"In the side room of the county yamen on a grey overcast morning: {SIDE}; soft grey daylight from the window on the right",
    "side_c": "In the side room of the county yamen on a grey overcast morning, a plain grey wall, soft grey daylight from the window on the right",
}
LIGHT = {
    "tea": "the soft grey daylight from the window stays unchanged",
    "work": "the small warm lamp flame and the deep night stay unchanged",
    "work_out": "the deep dark night around him stays unchanged",
    "dark": "the faint cool blue night light stays unchanged",
    "lane": "the thin warm line of light from the gap and the deep night stay unchanged",
    "inner": "the warm lantern light and the deep night stay unchanged",
    "hall": "the soft grey daylight stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object).
XU = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, his face washed clean"
XU_COAT = "Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe"
# s31 on: the dark red silk pouch inside his robe (script; not taken out this episode).
XU_POUCH = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, a small rounded bulge at the left breast of his "
            "robe where a pouch is tucked inside, one small corner of dark red silk showing at the edge of the collar")
BUNDLE = "one bundle the size of two hands wrapped in an old plain blue cotton cloth and tied with string"
QIN = ("her dark brown cross-collared short jacket, wide plain leather belt with nothing tucked in it and nothing hanging from it, "
       "black trousers, leather boots and high ponytail tied with black cord")
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
GOLD = "the small gold abacus hanging at her right hip, still"
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with two looped buns tied with pink "
         "silk ribbons and pearl pins, two long pink silk ribbons hanging from the buns down over her shoulders, a pink inner "
         "collar at the nape of her neck and her light peach-pink silk shoulders; the back of her head toward us the whole time, "
         "her ear the furthest round her head we ever see, only hair, ribbons and shoulders, her face turned fully away")


def only_tang(side):
    """e915 s26/s41: a second Tang appeared beside her back. One person with buns and ribbons, one fixed side."""
    return (f"she is the only young woman in the frame and the only one with buns and pink ribbons, and she stays in the {side} "
            f"foreground from the first frame to the last")


# The bookkeeper: never a face (script). His back by the window, or his hands.
CLERK_BACK = ("one thin young man in a plain dark blue cotton long gown and a soft black square cloth cap seen only from behind, "
              "appearing only once, sitting on the bench under the window with his back to us and his face turned to the window, "
              "only the back of his cap, his neck and his narrow shoulders showing")
CLERK_SLEEVE = "a plain dark blue cotton sleeve"
SILVER = "one small rough lump of silver the size of a thumb tip"
SLIP = "one sheet of thick opaque plain paper folded twice into a small flat slip, only its plain blank outside showing"
CLERK_LEDGER = "one thread-bound ledger lying closed on the bench, its cover plain blank dark blue cloth"
TEAPOT = "the round brown clay teapot"
# The trap (script: a dark brown box about a forearm and a half long and half a forearm high, one brass hasp on the lid).
BOX = ("one dark brown wooden box as long as a forearm and a half and half a forearm high, its lid shut, one small plain brass "
       "hasp on the front of the lid")
TURMERIC = "one small clay bowl of bright yellow liquid"
ASHWATER = "one small clay bowl of cloudy grey-white water"
BRUSH = "one small flat brush with a short wooden handle"
STRIP = "one thin flat strip of bamboo as long as a finger"
STONE = "one fist-sized stone wrapped in a square of plain grey cloth"
WIRE = "one thin bent iron wire as long as a finger"
# bible rule 12: an even orange-red like dye, never blood, never a wound; written as a state from the first frame.
RED = ("stained an even bright orange-red from the fingertips to the wrists like a dye soaked into the skin, smooth and even, "
       "the skin unbroken, clean of any wound")
ROPE = "one plain hemp rope as thick as a finger"
LAI = ("Lai San, the thin small young man in his grey-brown hemp cross-collared short jacket and old cloth head wrap, his left "
       "foot dragging in a limp")
QIAN = "Qian Yuanwai, in his dark gold silk cross-collared robe with roundel patterns and wide sleeves and his small black cap"
SLEEVES_IN = ("both his hands pushed deep inside his wide dark gold sleeves, the two sleeves joined in front of his belly, his "
              "hands hidden inside them the whole time")
HU = "in his black gauze futou hat with two short stiff flat wings and his blue-green round-collared official robe"
GAVEL = "one flat oblong block of dark polished wood the size of half a brick, plain on every side"
TLEDGER = "one thread-bound ledger held closed against her chest in both arms, its cover plain blank dark blue cloth"
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
HEADSTILL_TANG = "the young woman with the two buns and pink ribbons keeps her head still, the back of her head toward us the whole shot"
WOODPILE_TOPS = ("just the tops of two heads showing above the woodpile, dark and soft, one with a high ponytail and one with a "
                 "topknot, both still")


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return (f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, "
            f"no mouthing words, the face set and still")


SHOTS = [
    # ---- scene 1: the teahouse, day 14 in the morning (set-chalou-l1). Xu Yan sits at the left of the tea table facing right,
    # Tang Xiaotang at the right facing left; the bookkeeper on the bench under the window at the right, his back to us.
    dict(chapter="茶樓", loc="tea", cam="Medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="tea",
         comp=f"medium shot past {TEAPOT} on the tea table in the foreground: on screen left {XU}, sitting at the left side of the tea table, framed from the waist up with clear space above his head, {BUNDLE} held in both his hands just above the table, his face three-quarter to screen right toward the young woman, never the lens; grave: brows drawn, eyes on the bundle, lips closed; on screen right Tang Xiaotang {TANG}, {GOLD}, sitting at the right side of the table, framed from the waist up, {TEAPOT} in her right hand tilted over one small cup, her face three-quarter to screen left toward the bundle, never the lens; brows lifting a little, lips closed; far behind them at the right, small and soft, {CLERK_BACK}; {HANDS}",
         lines=[("xitong", "叮。強制任務，剩五日。", "冷，宣布")],
         panel=[("強制任務，剩五日", "task")],
         motion=f"Xu Yan sets the cloth bundle down on the table and folds back one corner of the blue cloth, and a few blackened bamboo strips show; Tang Xiaotang's pouring stops, the teapot held still; {quiet('Xu Yan and Tang Xiaotang', 'their', True)}; the man by the window stays still",
         zh="中景、慢推、前景是茶桌上的陶壺（送 `set-chalou-l1`：樓梯在左牆、後面四扇素白屏風、右邊大開窗外是灰瓦屋頂、窗下一張長木凳、中間方茶桌一壺兩杯）：畫左許硯（臉洗乾淨）兩手把舊藍布包好的燈籠骨架放上茶桌、掀開一角露出焦黑竹骨；畫右唐小棠右手提壺倒茶、倒到一半停住（中性臉、嘴閉著）；右後窗下長凳上帳房的背影（青布長衫、黑方巾，小、虛焦）；兩人嘴閉著（系統畫外，面板疊上）"),
    dict(loc="tea_c", cam="Close-up, slow push in", chars=["xuyan"], night="tea",
         comp=f"close-up of {XU}, framed from the chest up with space above his head, his right hand resting loosely curled on the tea table at the bottom of the frame, his face three-quarter to screen right, his eyes down on the table, never the lens; brooding and dry: brows knotted, the corners of his mouth pulled flat, lips pressed together; behind him only the plain cream-white panels of the folding screen",
         lines=[("xuyan", "兩天了，賴三躲在錢府不出門，我連人都見不到。", "悶，心裡話", "inner"),
                ("xitong", "宿主天天喝茶，倒是見得到茶。", "冷，毒舌"),
                ("xuyan", "今天不是來喝茶的，是來買東西的。", "不服，心裡回嘴", "inner")],
         motion=f"Xu Yan taps the table twice with the knuckles of his right hand and frowns; then one corner of his mouth twists in annoyance and he lifts his eyes toward screen right; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（身後只有空白的屏風）：許硯右手指節在桌上敲兩下、皺眉，再嘴角一撇、抬眼看畫右；全程嘴閉著（心裡話兩句與系統吐槽畫外，吐槽不出面板）（長鏡）"),
    # Tang Xiaotang's lines from behind her: she is always in the right foreground (her side of the table).
    dict(loc="tea", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="tea",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, sitting at the right side of the tea table in the right foreground, one small clay cup raised in her right hand in front of her face; {only_tang('right')}; facing us across the table a little left of the middle, {XU}, sitting, framed from the waist up with clear space above his head, both hands resting on the table beside the cloth bundle, his face three-quarter to screen right toward her, never the lens; alert: brows lifting, eyes narrowing, lips closed; behind him only the dark wooden staircase rising along the wall; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "靠窗那個青衫先生，就是錢府的帳房。", "壓低聲音")],
         motion=f"the young woman holds the cup in front of her face and tips her head a little toward the right; {HEADSTILL_TANG}; Xu Yan's eyes slide from her to the open window at the right edge of the room and back to her; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中景、慢推：前景右只有唐小棠的後腦、雙丸子頭粉緞帶與肩（右手舉茶杯擋在臉前，頭往右一偏）；對面畫面中偏左許硯坐著（身後是左牆的木樓梯），眼睛從她滑到畫右的窗（帳房，畫外）、再回到她；嘴閉著。台詞 nospeak，剪接放錄音"),
    dict(loc="tea", cam="Medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="tea",
         comp=f"medium shot from behind and a little to her left, at the open window on the right: {TBACK}, standing and bending a little in the left foreground, {SILVER} held between the fingers of her right hand just above the bench; {only_tang('left')}; on screen right beside her {CLERK_BACK}; on the bench beside him one small clay cup by his hip and {CLERK_LEDGER}; beyond them the open window, the grey tiled roofs and the pale grey sky; {HANDS}",
         lines=[("tangxiaotang", "先生，一兩銀子，換您帳上的一頁。", "甜，低聲")],
         motion=f"the young woman sets the lump of silver down softly on the bench beside the man's cup and draws her hand back; {HEADSTILL_TANG}; the man on the bench keeps his face to the window and does not move; he says nothing, his face never turning toward us",
         zh="【改背後拍】中景、從她左後方拍、慢推（窗邊）：前景左唐小棠的背影，第一格右手指間已經捏著一小塊碎銀，彎腰把它輕輕放在帳房的茶杯旁、收回手；畫右窗下長凳上帳房的背影（臉朝窗、永遠不轉過來），身旁一本合著的素藍布帳冊；窗外灰瓦。原稿的『窗邊小桌』照圖改成窗下長凳。台詞 nospeak，剪接放錄音"),
    # The bookkeeper's hands: the page is already torn and folded (paper is never read); one picture (the set) is all this job sends.
    dict(loc="tea_c", cam="Insert close-up, slow push in", chars=[], night="tea",
         comp=f"insert close-up, the shot opens directly on the plain wooden bench under the window from its very first frame: {CLERK_LEDGER}, and on its cover {SLIP}, held down under two thin long fingers of one hand in {CLERK_SLEEVE}; beside the ledger {SILVER} next to one small clay cup; only the hand, the sleeve, the ledger, the slip, the cup and the silver are in the frame, lit from our side by the grey daylight",
         lines=[("zhangfang", "只此一頁。出了這個門，我不認得姑娘。", "很小聲，緊張")],
         motion="the fingers push the folded slip across the bench toward the left edge and let go of it, then the same hand sweeps the lump of silver off the bench into the dark blue sleeve; the hand moves quickly and nervously",
         zh="插鏡、慢推（第一格就是窗下長凳；本鏡唯一送的圖是茶樓場景）：帳房（青布袖、瘦長手指）手指第一格已經壓著一張摺兩摺的素紙（只見空白的外面），放在合著的素藍布帳冊上；把紙推過長凳往畫左、放手，再把碎銀一把攏進袖子（原稿撕頁、摺紙兩拍並進第一格：紙一律不拍字）。帳房的話畫外"),
    # The page: held up toward Xu Yan, its blank back to us and lit from our side (bible rule 17).
    dict(loc="tea", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="tea",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, sitting at the right side of the tea table in the right foreground, holding up one unfolded sheet of thick opaque paper in both hands toward the young man, its writing turned to him so that we see only its plain blank back, lit from our side by the grey daylight, thick and opaque, nothing showing through it; {only_tang('right')}; facing us across the table a little left of the middle, {XU}, leaning in over the table, framed from the waist up with clear space above his head, his face three-quarter to screen right, his eyes reading the page, never the lens; intent: brows drawn together, eyes narrowing, lips closed; behind him only the dark wooden staircase; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "上個月十八，收魏記，銀三百兩。", "一字一字")],
         motion=f"the young woman holds the sheet steady toward him and taps one spot on its back once with her right forefinger; {HEADSTILL_TANG}; Xu Yan leans closer and his eyes move along one line of the page; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中景、慢推：前景右唐小棠的背影，兩手把攤開的帳頁舉向許硯（字朝他，我們只看得到空白的紙背，從我們這邊受光、不透光）；對面許硯湊過來，眼睛沿著一行讀；她不轉頭。台詞 nospeak，剪接放錄音"),
    # Her line off screen; his face takes it (bible rule 3).
    dict(loc="tea_c", cam="Close-up, slow push in", chars=["xuyan"], night="tea",
         comp=f"close-up of {XU}, framed from the chest up with space above his head, leaning forward over the table, his face three-quarter to screen right toward the page held up off screen right, never the lens; his eyes moving down one line, then lifting; the colour leaving his face: brows drawing together hard, eyes widening a little, lips parting and then pressing shut; behind him only the dark wooden staircase",
         lines=[("tangxiaotang", "紙坊起火前一天，付賴三，五兩。", "更低")],
         motion=f"Xu Yan's eyes move down to the next line of the page off screen right, stop, then lift slowly toward the young woman off screen right; his jaw tightens; {SILENT_HE}",
         zh="【改成許硯聽的臉】近景、慢推：許硯往前湊，眼睛往下移一行、停住、慢慢抬起看畫右的她（唐小棠那句畫外放錄音，拍法 3：反應給對面的人）；下巴一緊；全程嘴閉著"),
    dict(loc="tea", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="tea",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, sitting in the right foreground, soft; facing us across the table a little left of the middle, {XU}, framed from the waist up with clear space above his head, leaning forward, his left hand pressed flat on the blue cloth bundle on the table, his face three-quarter to screen right toward her, never the lens; sharp and urgent: brows knotted tight, eyes intent, lips moving quickly between words; behind him only the dark wooden staircase; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("xuyan", "魏記？就是書院街角，孫掌櫃那一家？", "壓低，急問")],
         motion=f"Xu Yan leans further in over the table, his left hand pressing down on the bundle; {HEADSTILL_TANG}; after the last word his brows stay knotted, eyes on her",
         zh="過肩中景、慢推：前景右唐小棠的丸子頭（不點名、不送圖）；對面許硯往前湊、左手按住桌上的布包，眉頭皺緊，急急地問；說完眉頭不鬆；不笑"),
    dict(loc="tea", cam="Medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="tea",
         comp=f"medium shot from behind and a little to her right: {TBACK}, sitting at the right side of the tea table in the right foreground, {SLIP} held in her right hand at her right side, her left hand holding open the cuff of her right sleeve; {only_tang('right')}; beyond her across the table only the empty chair, the dark wooden staircase and the dark wall; nobody else in the frame",
         lines=[("tangxiaotang", "就是那一家。錢員外背後，還有人在出錢。", "低，篤定")],
         motion=f"the young woman nods once and slides the folded slip into her right sleeve with her right hand, and smooths the sleeve down with her left; {HEADSTILL_TANG}",
         zh="【改背後拍】中景、從她右後方拍、慢推：前景右唐小棠的背影，右手第一格已經拿著摺好的帳頁，點一下頭，把它塞進右袖、左手把袖口撫平；畫面裡只有她一個人（許硯起身靠過來那一拍不拍）。台詞 nospeak，剪接放錄音"),
    dict(loc="tea_c", cam="Close-up, slow push in", chars=["xuyan"], night="tea",
         comp=f"close-up of {XU}, framed from the chest up with space above his head, his head lowered, the fingertips of his right hand resting on the blue cloth bundle at the bottom of the frame, his face three-quarter to screen right, his eyes on the bundle, never the lens; cold and level: brows drawn low, eyes hard, lips moving slowly and evenly between words; behind him only the plain cream-white panels of the folding screen",
         lines=[("xuyan", "錢府放的火，魏記出的錢，賴三拿的工錢。", "沉下聲音")],
         motion="Xu Yan's fingertips tap slowly on the cloth bundle, once on each name; after the last word his fingers go still and his jaw sets",
         zh="近景、慢推（身後只有空白屏風）：許硯低頭，右手指尖在布包上慢慢敲，一個名字一下，沉聲說；說完手指停住、下巴一緊；不笑"),
    dict(loc="tea", cam="Medium shot, slow push in", chars=["xuyan"], night="tea",
         comp=f"medium shot: on screen left {XU}, sitting at the tea table, framed from the waist up with clear space above his head, one small clay cup in his right hand just above the table, his face three-quarter to screen right toward the window, never the lens; loud and deliberate: brows raised, eyes wide and bright, mouth wide between words; far behind him at the right by the open window, small and soft, {CLERK_BACK}; {HANDS}",
         lines=[("xuyan", "賣紙的銀子跟造紙方子，今晚都鎖進新紙坊的錢箱！", "故意大聲")],
         motion="Xu Yan sets the cup down on the table with a knock and sits up straight, raising his voice toward the room; the man by the window goes still; after the last word Xu Yan's eyes slide sideways to the window and stay there",
         zh="中景、慢推：畫左許硯把茶杯往桌上一放、坐直，提高聲音；右後窗下長凳上帳房的背影（小、虛焦）一僵；說完眼睛斜到窗邊不動（唐小棠一愣那拍不拍，她在畫外）；不笑"),
    # The bookkeeper leaves: his hands only (no face; the staircase goes down toward the camera, so his walk is not shot).
    dict(loc="tea_c", cam="Insert close-up, slow push in", chars=[], night="tea", act=3,
         comp=f"insert close-up, the shot opens directly on the plain wooden bench under the window from its very first frame: one small clay cup standing on the bench and, beside it, {CLERK_LEDGER}; one thin hand in {CLERK_SLEEVE} still holding the cup by its rim; only the hand, the sleeve, the cup and the ledger are in the frame, lit by the grey daylight from the window",
         lines=[],
         motion="the hand sets the cup down hard so the tea jumps, snatches up the ledger and pulls away out of the frame to the left; the cup is left alone on the bench, rocking once",
         zh="插鏡、慢推（第一格就是窗下長凳；本鏡唯一送的圖是茶樓場景）：帳房的手把茶杯重重一放、茶濺一下，一把抓起合著的帳冊、往畫左抽出畫面；長凳上只剩茶杯晃一下（原稿的主觀全景改插鏡：樓梯往鏡頭這邊下，走下去一定露臉）（無台詞）"),
    dict(loc="tea", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="tea",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, sitting at the right side of the tea table in the right foreground, leaning toward the young man across the table, her hands on the table edge; {only_tang('right')}; facing us a little left of the middle, {XU}, sitting, framed from the waist up with clear space above his head, his face three-quarter to screen right toward her, his eyes coming back to her from the open window, never the lens; one brow lifting, eyes calm, lips closed; behind him only the dark wooden staircase; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "你故意說給他聽？我們哪來的錢箱？", "小聲，皺眉")],
         motion=f"the young woman leans further toward him across the table; {HEADSTILL_TANG}; Xu Yan turns his eyes from the window back to her and lifts one brow; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中景、慢推：前景右唐小棠的背影往許硯那邊湊；許硯眼睛從畫右的窗收回來看她、挑一下眉；嘴閉著。台詞 nospeak，剪接放錄音"),
    # Xu Yan may smile a little (script).
    dict(loc="tea_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="tea",
         comp=f"medium close-up of {XU}, framed from the chest up with generous clear space above his head, {BUNDLE} already tucked under his left arm, his right hand on the edge of the tea table, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; sly and sure: one brow raised, eyes bright, lips moving low and quick between words; behind him only the plain cream-white panels of the folding screen",
         lines=[("xuyan", "他賣帳給我們，也會把這句賣給錢府。今晚就有一只錢箱。", "壓低聲音，篤定")],
         motion="Xu Yan pushes himself up from the table with his right hand and stands, the bundle firm under his left arm, his head staying inside the frame; after the last word one corner of his mouth lifts a little and he glances at the stairs",
         zh="中近景、慢推（身後只有空白屏風，頭上留空）：許硯第一格布包已經夾在左腋下，右手撐桌站起來，壓低聲音說；說完嘴角微微一揚（本鏡可以笑一下）、瞄一眼樓梯（原稿綁布包那拍並進第一格）"),
    # ---- scene 2: the new workshop at night (no set picture). The table in the middle, the woodpile at the front left, the
    # fence gap on the right (Lai San comes in and goes out there).
    dict(chapter="錢箱", loc="work", cam="Medium shot, slow push in", chars=["xuyan", "qinshuang"], night="work",
         comp=f"medium shot past {LAMP} in the foreground: on screen left {XU_COAT}, standing at the left end of the work table, framed from the waist up with clear space above his head, {BRUSH} in his right hand over {BOX} on the table, {TURMERIC} beside the box, his face lowered toward the box, never the lens; focused: brows drawn, eyes on the lid, lips moving evenly between words; on screen right Qin Shuang, {QIN}, crouching at the right end of the table with her forearms on its edge, framed from the chest up, her face three-quarter to screen left toward the box, never the lens; doubtful: one brow raised, lips closed; {HANDS}; exactly two people",
         lines=[("xuyan", "箱面刷薑黃水，乾了看不出來，只是有點黃。", "邊刷邊說")],
         motion=f"Xu Yan dips the brush in the yellow bowl and strokes it along the lid of the box, once, twice, the wood turning faintly yellow; {quiet('Qin Shuang', 'her')}",
         zh="中景、慢推、前景是桌上的小陶油燈（不送場景圖：新紙坊夜景沒有對的圖，寫在文字裡——四根白松柱、左半邊新蓋草頂、中間木桌、左前一堆柴、右邊竹籬笆有個缺口）：畫左許硯（披舊灰外衣）右手拿小刷子蘸碗裡的薑黃水，在深褐木箱蓋上一下一下刷；畫右秦霜（腰帶空著）蹲在桌右、兩前臂靠在桌邊看著（挑一邊眉、嘴閉著）"),
    dict(loc="work_c", cam="Insert close-up, slow push in", chars=["xuyan"], nospeak=["xuyan"], night="work",
         comp=f"insert close-up, the shot opens directly on the small plain brass hasp on the front of the dark brown box from its very first frame: one hand in a grey cloth sleeve holding {STRIP} already wet at its tip, {ASHWATER} at the bottom right; only the hand, the sleeve, the hasp, the box front and the bowl are in the frame; the small warm lamp light from the left",
         lines=[("xuyan", "鎖扣抹草木灰水，誰要開鎖，手一定得碰到。", "低")],
         motion="the hand dips the bamboo strip into the grey-white water and smears it over the brass hasp, then a second time, the metal going dull and wet",
         zh="插鏡、慢推（第一格就是銅鎖扣；不送場景圖，只送許硯四分之三側面圖當手的主人）：一隻灰布袖的手拿一根手指長的小竹片，蘸碗裡灰白的草木灰水抹在銅鎖扣上，抹兩遍。台詞剪接放錄音（許硯畫外）"),
    dict(loc="work", cam="Over-the-shoulder medium shot, slow push in", chars=["qinshuang"], night="work",
         comp=f"over-the-shoulder medium shot from close behind one young man in an old grey cloth coat seen only from behind, appearing only once, standing in the left foreground, only the back of his head with a topknot and his left shoulder showing, soft and dark; facing us across the work table a little right of the middle, Qin Shuang, {QIN}, standing at the table, framed from the waist up with clear space above his head, {BOX} open in front of her, two fist-sized stones wrapped in squares of plain grey cloth already lying inside it and {STONE} held in her right hand above the box, {LAMP} at the left of the box, her face lowered toward the box, never the lens; impatient: brows drawn, mouth tight; behind her only the dark; {HANDS}; exactly two people, the young man in the foreground seen only from behind",
         lines=[("qinshuang", "一黃一灰，這兩樣就抓得到人？", "不耐")],
         motion="Qin Shuang sets the third wrapped stone into the box beside the other two and shuts the lid with both hands; then she lifts her head toward the young man in the foreground, frowning; after the last word her lips press into a hard line; the young man in the foreground keeps his head still, the back of his head toward us the whole shot",
         zh="過肩中景、慢推：前景左只有許硯的後腦（髮髻）與披外衣的左肩（不點名、不送圖）；秦霜在桌後畫面中偏右，箱裡第一格已經放了兩個布包石頭，右手拿第三個放進去、兩手蓋上蓋子，皺眉抬頭不耐地問；說完抿成一條線；不笑"),
    # Xu Yan may smile a little (script); the lamp goes out at the end (the cut falls before the dark).
    dict(loc="work_c", cam="Close-up, slow push in", chars=["xuyan"], night="work_out",
         comp=f"close-up of {XU_COAT}, framed from the chest up with space above his head, {BRUSH} in his right hand, the small warm flame of the oil lamp at the bottom left of the frame lighting his face from below, his face three-quarter to screen right toward Qin Shuang off screen right, never the lens; teasing and sure: one brow raised, eyes bright, lips moving lightly between words; behind him only one pale pine post and the dark",
         lines=[("xuyan", "抓不抓得到，今晚妳就知道。先躲到柴堆後面。", "賣關子")],
         motion="Xu Yan drops the brush into the bowl, then leans down toward the lamp; after the last word he blows the small flame out and the frame goes to cool blue darkness, his face still faintly visible; one corner of his mouth lifts a little",
         zh="近景、慢推：許硯把刷子丟進碗裡，彎身向畫左下的油燈，說完把燈吹熄、畫面掉進冷藍的暗（本鏡可以笑一下，賣關子）；原稿『一把拉著秦霜』那拍拿掉（兩人接觸），躲的動作交給 s19 的第一格"),
    dict(loc="dark", cam="Wide shot, slow push in", chars=["laisan"], night="dark", act=3,
         comp=f"wide shot past the low stack of split firewood in the left foreground, {WOODPILE_TOPS}: {LAI}, framed full length, already stepping in through the narrow gap in the bamboo fence at the right, hunched, his face three-quarter to screen left toward the work table, never the lens; furtive: eyes darting, lips pressed together; {BOX} standing alone on the work table in the middle; {HANDS}",
         lines=[],
         motion=f"Lai San limps to the table, dragging his left foot, glances left and right twice, bends and lifts the box off the table into his arms; {quiet('Lai San')}; the two heads behind the woodpile stay still",
         zh="全景、慢推、前景左是柴堆，後面只露兩個頭頂（一個高馬尾、一個髮髻，不點名、不送圖）：賴三第一格已經從畫右竹籬笆的缺口拐進來，一拐一拐（左腳拖著）走到桌前，左右看兩眼，彎腰把錢箱抱起來；只有冷藍的夜光（燈已熄）（無台詞）"),
    dict(loc="dark_c", cam="Medium shot, slow push in", chars=["laisan"], night="dark",
         comp=f"medium shot of {LAI}, framed from the knees up with clear space above his head, standing by the work table, {BOX} held in both his arms against his chest, the brass hasp facing us, his face lowered toward the box, never the lens; greedy: eyes narrowed, lips moving low and quick between words; behind him only the dark and one pale pine post; {HANDS}",
         lines=[("laisan", "鎖得這麼緊，裡面肯定是好東西。", "壓著嗓子")],
         motion="Lai San picks once at the brass hasp with his right forefinger, cannot open it, then hugs the box tighter to his chest and hefts it once to feel its weight; after the last word his eyes dart to the fence gap on the right",
         zh="中景、慢推（冷藍夜光）：賴三兩臂把錢箱抱在胸前、銅鎖扣朝鏡頭，右手食指摳一下鎖扣、打不開，抱緊、掂一掂，壓著嗓子說；說完眼睛瞟向畫右的籬笆缺口"),
    # Contact as a state: Xu Yan's hand already on her forearm. No knife (bible rule 5): her hand is on the woodpile.
    dict(loc="dark_c", cam="Close-up, slow push in", chars=["qinshuang"], night="dark",
         comp=f"close-up of Qin Shuang, {QIN}, crouching behind the stack of split firewood, framed from the chest up with space above her head, her right hand flat on top of the woodpile at the bottom of the frame as if to push herself up, one hand in a grey cloth sleeve reaching in from the right edge and already resting on her left forearm from the first frame, her face three-quarter to screen right toward the owner of that hand, never the lens; urgent and fierce: brows drawn hard, eyes blazing, lips moving fast and low between words; behind her only the dark",
         lines=[("qinshuang", "人就在眼前，你還不抓？他要跑了！", "壓低聲音，急")],
         motion="Qin Shuang starts to rise and is held by the hand on her forearm; she sinks back down and turns her head sharply toward the right; after the last word her eyes stay on the right and her jaw stays clenched",
         zh="近景、慢推（冷藍夜光）：秦霜蹲在柴堆後，右手按在柴堆頂上要撐起來（原稿『按上柴刀柄』改成按柴堆，拍法 5：刀不拍）；畫右緣伸進來一隻灰布袖的手（許硯，不點名）第一格就已經按在她左前臂上；她被按住、坐回去、猛轉頭朝畫右急急地說；說完咬著牙"),
    dict(loc="dark_c", cam="Close-up, slow push in", chars=["xuyan"], night="dark",
         comp=f"close-up of {XU_COAT}, crouching behind the stack of split firewood, framed from the chest up with space above his head, his face three-quarter to screen left toward Qin Shuang off screen left, never the lens; calm and intent: brows level, eyes narrowed, lips moving very softly between words; behind him only the dark",
         lines=[("xuyan", "讓他送回去，看是誰開的箱。跟上。", "很輕")],
         motion="Xu Yan shakes his head once, slowly, his eyes flicking to the dark at screen right where the man went and back to her; after the last word he nods once toward the right",
         zh="近景、慢推（冷藍夜光）：許硯蹲在柴堆後，慢慢搖一下頭，眼睛往畫右（賴三走的方向）一瞟、再回到畫左的她，很輕地說；說完朝畫右點一下頭；不笑"),
    # The lane behind the Qian manor (no set picture). The lane mouth on the left, the back gate on the right.
    dict(loc="lane", cam="Wide shot, slow push in", chars=["laisan"], night="lane", act=3,
         comp=f"wide shot down the lane past the corner of the whitewashed wall at the left edge: on screen right {LAI}, framed full length, small, standing at the two black gate leaves, {BOX} in his arms, his face turned to the gate, never the lens; furtive: shoulders hunched, lips pressed together; far back at the left by the foot of the left wall, two small dark figures pressed against the wall, too dark and small to make out; {HANDS}",
         lines=[],
         motion=f"Lai San knocks on the gate three times with his knuckles, the gap widens and he slips sideways through it, and the two leaves close to a hand's width again, the thin warm line of light still showing; the two small figures at the left creep along the wall toward the gate; {quiet('Lai San')}",
         zh="全景、慢推、前景左緣是巷口的白牆角（不送場景圖：錢府後巷沒有對的圖，寫在文字裡——巷口在左、右牆上兩扇黑木後門虛掩、門縫透出一線暖光）：賴三第一格已經抱著錢箱站在右邊後門前，用指節敲三下，門縫開大、他側身閃進去、門又掩回一條縫；遠處左牆根兩個看不清的小黑影貼牆往門邊摸（無台詞）"),
    # Through the gap: the passage inside the back gate (set-qianfu-houmen-ye-l1, swapped in). Qian Yuanwai at the stone table.
    dict(loc="inner", cam="Point-of-view medium-wide shot, slow push in", chars=["qianyuanwai", "laisan"], night="inner",
         comp=f"point-of-view medium-wide shot through the narrow gap between two black wooden gate leaves, their dark edges filling the left and right edges of the frame: beyond them at the round stone table in the middle distance, {QIAN}, standing beside the table, framed from the knees up with clear space above his head, half turned, {WIRE} in his right hand at the brass hasp of {BOX} lying on the table, his face three-quarter to screen right toward the box, half hidden behind the right gate leaf, never the lens; impatient and greedy: brows drawn, eyes narrowed on the box, lips moving between words; beside him on the left {LAI}, framed from the knees up, standing still with his empty hands at his sides, his face toward the box, lips pressed together; {HANDS}; nobody else in the frame",
         lines=[("qianyuanwai", "造紙的方子？我倒要看看，他藏了什麼寶貝。", "不耐")],
         motion=f"Qian Yuanwai twists the wire in the hasp until it springs open, then lifts the lid of the box with both hands; {quiet('Lai San')}; after the last word Qian Yuanwai leans over the open box",
         zh="主觀中全景、慢推（秦霜從門縫看進去，前景左右是兩片黑門板的邊；送 `set-qianfu-houmen-ye-l1`：左邊一整面白牆、右邊廊下一排亮著的白紙燈籠、遠處小亭一張圓石桌，正是後門裡面看進去的樣子；牆上的屋簷影子寫成牆面均勻受光）：錢員外站在石桌邊，右手拿一根鐵絲撬開銅鎖扣、兩手掀開箱蓋，臉被右邊門板擋一半；賴三站在左邊空著手、嘴閉著"),
    # Inserts at the box (no set picture; Qian Yuanwai's pictures only as the owner of the hands; his lines laid in).
    dict(loc="inner_c", cam="Insert close-up, slow push in", chars=["qianyuanwai"], nospeak=["qianyuanwai"], night="inner",
         comp=f"insert close-up, the shot opens directly on the open dark brown box from its very first frame: inside it three fist-sized bundles of plain grey cloth; two plump hands with three gold rings, in wide dark gold silk sleeves, already lifting one bundle out of the box, the skin of the hands faintly yellowish; only the hands, the sleeves, the box and the bundles are in the frame; warm lantern light",
         lines=[("qianyuanwai", "石頭？賴三，你被那個窮秀才耍了！", "畫外，怒")],
         motion="the plump hands pull the grey cloth open and it falls away from a plain grey stone; the hands freeze around it, then grip the stone hard",
         zh="插鏡、慢推（第一格就是打開的錢箱；不送場景圖，只送錢員外的圖當手的主人）：一雙戴金戒指的胖手（深金寬袖、手已微黃）第一格已經從箱裡拿起一個布包，布散開是一塊灰石頭，手一僵、握緊。台詞剪接放錄音（錢員外畫外）"),
    # Red as a state from the first frame (never a change on screen); dye, never blood.
    dict(loc="inner_c", cam="Insert close-up, slow push in", chars=["qianyuanwai"], nospeak=["qianyuanwai"], night="inner",
         comp=f"insert close-up, the shot opens directly on two plump open hands held palms up from its very first frame, three gold rings on the fingers, in wide dark gold silk sleeves, the palms and fingers {RED}, one plain grey stone resting in the right palm; only the hands, the sleeves and the stone are in the frame; warm lantern light",
         lines=[("qianyuanwai", "這手……怎麼紅了？擦都擦不掉！", "畫外，慌")],
         motion="the stone drops from the right hand and falls away below; the two hands rub hard against the dark gold silk of the robe below them, then turn palms up again, still the same even orange-red",
         zh="手部特寫、慢推（第一格就是一雙攤開的胖手：手掌與手指從指尖到手腕均勻的橘紅，像染料、皮膚完好不是傷不是血；紅寫成第一格的狀態，不演『慢慢變紅』）：石頭從右手掉出畫，兩手在錦袍上用力擦、再翻過來，還是一樣紅。台詞剪接放錄音（錢員外畫外）"),
    dict(loc="lane", cam="Medium close-up, slow push in", chars=["qinshuang", "xuyan"], night="lane",
         comp=f"medium close-up: on screen left Qin Shuang, {QIN}, pressed against the wall beside the gap of the back gate, framed from the chest up with space above her head, the thin warm line of light from the gap falling down one side of her face, her head turned over her right shoulder toward the young man behind her, her face three-quarter to screen right, never the lens; stunned: eyes wide, brows lifted, lips parted and then pressed shut; just behind her on screen right {XU_COAT}, framed from the chest up, leaning close, his face three-quarter to screen left toward her, never the lens; quiet and sure: brows level, eyes steady, lips moving very softly between words; the rest of the frame dark; {HANDS}; exactly two people",
         lines=[("xuyan", "薑黃碰上草木灰就變紅，一夜也洗不掉。", "很輕")],
         motion=f"Qin Shuang turns her head from the gap back toward Xu Yan; Xu Yan leans in and speaks low; {quiet('Qin Shuang', 'her')}; after the last word he nods once toward the gap",
         zh="中近景、慢推（後巷，不送場景圖）：畫左秦霜貼在後門縫邊的牆上，門縫那一線暖光照在半邊臉上，從門縫回頭看畫右身後的許硯（眼睛睜大、嘴閉著）；許硯湊近很輕地說；說完朝門縫點一下頭"),
    # Contact as a state: she already holds him against the wall. His hands are already red.
    dict(loc="lane", cam="Medium shot, slow push in", chars=["qinshuang", "laisan"], night="lane",
         comp=f"medium shot near the mouth of the lane: on screen left {LAI}, framed from the waist up with clear space above his head, already pressed face-first against the whitewashed wall, his left cheek on the wall, his left hand flat on the wall beside his face, {RED.replace('stained', 'the hand stained')}, his right arm held twisted behind his back; on screen right Qin Shuang, {QIN}, framed from the waist up, standing close behind him, her right hand gripping his right wrist behind his back and her left hand pressing his shoulder to the wall from the first frame, her face three-quarter to screen left toward the back of his head, never the lens; cold: brows level, eyes hard, lips moving crisply between words; the thin warm line of light from the gate far behind them; {HANDS}; exactly two people",
         lines=[("qinshuang", "別動。你這雙手，明天自己跟大人說去。", "冷")],
         motion=f"Lai San twists once against the wall and Qin Shuang presses him back flat with one push of her left hand; {quiet('Lai San')}; after the last word her lips press into a hard line",
         zh="中景、慢推（巷口，不送場景圖）：第一格秦霜已經把賴三按在左邊白牆上（她右手扭著他的右手腕在背後、左手壓他的肩；接觸寫成第一格的狀態，不演『閃出來撲上去』），賴三左頰貼牆、左手平貼在牆上、已經橘紅；他掙一下、被她一推又貼回去；秦霜冷冷地說；說完抿嘴"),
    dict(loc="lane", cam="Close-up, slow push in", chars=["laisan"], night="lane",
         comp=f"close-up of {LAI}, framed from the chest up with space above his head, his left cheek pressed against the whitewashed wall, his face pale, his left hand flat on the wall at the bottom of the frame, {RED.replace('stained', 'the hand stained')}, his eyes rolled down toward that hand, never the lens; terrified: brows drawn up, eyes wide, lips pressed together and trembling; the rest of the frame only the wall and the dark",
         lines=[("xitong", "叮。賴三，人贓俱獲。", "冷，宣布")],
         panel=[("賴三，人贓俱獲", "panel")],
         motion=f"Lai San strains once against the wall and cannot move; his eyes find his own orange-red hand and the fingers start to tremble; {SILENT_HE}",
         zh="近景、慢推（後巷）：賴三左頰貼著白牆、臉發白，左手平貼牆上在畫面下緣、已經橘紅，眼睛往下看到自己的手，手指抖起來；嘴閉著（系統畫外，面板疊上）"),
    dict(loc="lane", cam="Medium shot, slow push in", chars=["xuyan", "laisan", "qinshuang"], night="lane",
         comp=f"medium shot near the mouth of the lane: in the middle {LAI}, framed from the waist up, standing with his back against the whitewashed wall, both his wrists held together in front of his belly, {ROPE} already wound twice round them, both his hands {RED.replace('stained ', '')}; his face lowered, eyes on the rope, lips pressed together and trembling; on screen right Qin Shuang, {QIN}, framed from the waist up, her left hand holding his right shoulder to the wall, her face toward him, never the lens, lips closed, eyes hard; on screen left {XU_COAT}, framed from the waist up with clear space above his head, both hands on the two ends of the rope, his face three-quarter to screen right toward Qin Shuang, never the lens; cool and decided: brows level, eyes steady, lips moving evenly between words; {HANDS}; exactly three people",
         lines=[("xuyan", "帶他回去，明早一起上縣衙。他主子的手，也紅了。", "冷靜")],
         motion=f"Xu Yan pulls the two ends of the rope and ties them into one knot, tugging it tight; {quiet('Lai San and Qin Shuang', 'their', True)}; after the last word Xu Yan lets go of the rope and looks at the gate off screen right",
         zh="中景、慢推（巷口）：賴三背靠白牆、兩手腕併在身前，第一格麻繩已經繞了兩圈（兩手橘紅）；畫右秦霜左手按著他的右肩；畫左許硯（外衣）兩手拉住繩頭打一個結、拉緊，對秦霜說；說完放開繩子、看向畫右的後門；三人（秦霜、賴三嘴閉著）"),
    # ---- scene 3: day 15 in the morning, the court hall (set-xianya-gongtang-l1 swapped in). Magistrate Hu sits at the desk on
    # the platform at the back (his own shots s32, s37 face him); the floor shots s31, s33-s36 are framed below the platform
    # with the people on the floor facing up toward it. Hu and Qian Yuanwai are never in one frame.
    dict(chapter="公堂", loc="hall", cam="Wide shot, slow push in", chars=["xuyan", "tangxiaotang", "qianyuanwai"], night="hall",
         comp=f"wide shot across the stone floor below the platform, the magistrate's raised desk above the top of the frame: on screen left {XU_POUCH}, standing, framed full length with clear space above his head, his hands at his sides, his face three-quarter to screen right toward the kneeling man, never the lens; wary: brows drawn, eyes narrowed, lips closed; behind him at his left Tang Xiaotang {TANG}, {GOLD}, standing, framed full length, small, {TLEDGER}, her face three-quarter to screen right, never the lens; anxious: brows drawn up, lips closed; on screen right {QIAN}, kneeling on the stone floor, framed full length, {SLEEVES_IN}, his face tipped up toward the desk above the frame, never the lens; whining and righteous: brows raised, mouth drawn long between words; behind them only a dark red-brown pillar and the tall grey lattice windows; {HANDS}; exactly three people",
         lines=[("qianyuanwai", "大人，許硯賣紙進城，一文稅都沒交！", "拖長音，告狀")],
         motion=f"Qian Yuanwai bows forward once from the knees with his hands still inside his sleeves and comes up again, his face lifted toward the desk; {quiet('Xu Yan and Tang Xiaotang', 'their', True)}; after the last word he keeps his chin up, mouth turned down",
         zh="全景、慢推（送 `set-xianya-gongtang-l1`；公案在畫面上緣外、胡縣令不入鏡）：畫左許硯（懷裡錢袋只露左胸衣襟一角暗紅綢）、左後唐小棠抱著合起的素藍布帳冊（中性臉、嘴閉著）；畫右錢員外跪著，兩手整個縮在寬袖裡、袖口併在肚前，往前一拜再抬頭朝上面的公案拖長音告狀（原稿前景衙役的水火棍拿掉：衙役整場不拍，『威武』只留音效）"),
    dict(loc="hall", cam="Low-angle medium close-up, slow push in", chars=["huxianling"], night="hall",
         comp=f"low-angle medium close-up from below the platform: Magistrate Hu, {HU}, sitting behind the long dark desk, framed from the chest up with clear space above his hat, his right hand already resting flat on {GAVEL} on the desk, his face three-quarter to screen left toward Xu Yan off screen left below him, never the lens; pompous: chin raised, brows lifted, eyes half lidded, mouth drawn long between words; behind him only the plain white panels",
         lines=[("huxianling", "許硯，賣紙不交稅，你可知罪？", "官腔，拖長音")],
         motion="Magistrate Hu lifts the wooden block a hand's height and brings it down flat on the desk with one sharp knock; after the last word his chin stays up and his eyes stay half lidded",
         zh="低角度中近景、慢推（身後只有空白屏板）：胡縣令（黑紗幞頭兩片短硬平翅、藍綠圓領官袍）坐在公案後，右手第一格已經按在一塊扁長方的深色木塊上（驚堂木，不是槌），抬起一掌高往案上一拍，官腔拖長音問；說完下巴不放"),
    # No pointing finger: an open hand, palm up.
    dict(loc="hall", cam="Medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="hall",
         comp=f"medium shot below the platform: a little left of the middle {XU_POUCH}, standing, framed from the knees up with clear space above his head, his hands joined in front of his chest in a scholar's bow, his face tipped up toward the desk above the frame, never the lens; composed and firm: brows level, eyes steady, lips moving evenly between words; one step behind him on screen left Tang Xiaotang {TANG}, {GOLD}, standing, framed from the knees up, soft, {TLEDGER}, her face three-quarter to screen right, never the lens; tense: brows drawn, lips closed; behind them only a dark red-brown pillar and the tall grey lattice windows; {HANDS}; exactly two people",
         lines=[("xuyan", "學生知法。可學生也要告一樁，錢府縱火燒我紙坊。", "不卑不亢")],
         motion=f"Xu Yan bows his joined hands once toward the desk, then turns toward screen right and holds his right hand out flat, palm up, toward Qian Yuanwai off screen right; {quiet('Tang Xiaotang', 'her')}; after the last word he keeps his open hand out and his eyes on the right",
         zh="中景、慢推：許硯往前一步拱手朝上面的公案一拜，再轉身朝畫右（錢員外，畫外）攤開右手、掌心朝上（不用手指指人：e916 s26 豎一指讀成不雅手勢）；左後唐小棠抱帳冊（中性臉、嘴閉著）；說完手不收、眼睛看右"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["qianyuanwai"], night="hall",
         comp=f"close-up of {QIAN}, kneeling, framed from the chest up with space above his head, {SLEEVES_IN}, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; outraged: brows shooting up, eyes bulging, mouth wide between words; behind him only a dark red-brown pillar and the grey daylight",
         lines=[("qianyuanwai", "血口噴人！你說老夫放火，有人證嗎？", "拔高聲音")],
         motion="Qian Yuanwai jerks himself upright on his knees, and his joined sleeves shake in front of his belly; after the last word his jowls quiver and his mouth stays pulled down",
         zh="近景、慢推（身後只有柱子與灰光；原稿『一個衙役的黑袍』拿掉）：錢員外跪著猛地挺起身，兩隻併在肚前的袖子跟著抖（手一直在袖裡），拔高聲音；說完腮幫抖、嘴角往下"),
    dict(loc="hall", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="hall",
         comp=f"over-the-shoulder medium shot from close behind one portly man in a dark gold silk robe seen only from behind, appearing only once, kneeling in the right foreground, only the back of his small black cap, his thick neck and his right shoulder and wide sleeve showing, soft; facing us a step away a little left of the middle, {XU_POUCH}, standing, framed from the waist up with clear space above his head, his right hand held out flat, palm up, toward the man's sleeves, his face three-quarter to screen right looking down at the man, never the lens; cool and pointed: one brow raised, eyes hard, lips moving evenly between words; behind him only a dark red-brown pillar and the tall grey lattice windows; {HANDS}; exactly two people, the man in the foreground seen only from behind",
         lines=[("xuyan", "人證就在衙門外。錢員外，你的手怎麼一直不拿出來？", "冷，逼問")],
         motion="Xu Yan moves his open hand from the doorway at the left toward the man's joined sleeves; the kneeling man in the foreground keeps his head still, the back of his cap toward us the whole shot, his shoulders hunching; after the last word Xu Yan's eyes stay on the sleeves",
         zh="過肩中景、慢推：前景右只有錢員外跪著的後腦（小黑帽）、粗脖子與右肩寬袖（不點名、不送圖）；許硯在畫面中偏左往下看他，右手攤開、掌心朝上，從畫左的門口方向移到他的袖子（原稿『一指』改攤手）；說完眼睛盯著袖子；不笑"),
    # Qian Yuanwai's forced laugh is allowed (script).
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["qianyuanwai"], night="hall",
         comp=f"close-up of {QIAN}, kneeling, framed from the chest up with space above his head, {SLEEVES_IN}, hunched, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; caught and flustered: eyes darting, a stiff forced laugh pulling at his mouth, sweat on his upper lip; behind him only a dark red-brown pillar and the grey daylight",
         lines=[("qianyuanwai", "天、天冷……老夫一到秋天就怕冷。", "結巴，乾笑")],
         motion="Qian Yuanwai hugs his joined sleeves tighter into his belly and pulls his neck down into his collar; after the last word the forced laugh drops off his face and his eyes slide away",
         zh="近景、慢推：錢員外把併在肚前的兩隻袖子往懷裡一攏、縮脖子乾笑（本鏡可以乾笑），結巴地說；說完笑一下子掉下來、眼睛溜開；手始終在袖裡"),
    # The script's c37 (Qian Yuanwai's line off screen, then Magistrate Hu's, 9 s) is two shots: the two recordings run 11.4 s
    # of speech, more than a 10 s clip holds (r2.py BUY). s37: Qian Yuanwai asks on screen (his hands stay in his sleeves);
    # s37b: Magistrate Hu grants it. Hu and Qian Yuanwai stay in separate frames.
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["qianyuanwai"], night="hall",
         comp=f"close-up of {QIAN}, kneeling, framed from the chest up with space above his head, both his hands hidden inside his wide dark gold sleeves, the back of his left sleeve-covered wrist already pressed to his forehead, his face tipped up three-quarter to screen left toward the magistrate's raised desk above the frame, never the lens; pleading and sly: brows drawn up, eyes half closed, mouth drooping between words; behind him only a dark red-brown pillar and the grey daylight",
         lines=[("qianyuanwai", "大人，老夫頭暈得很，求您午後再審。", "急")],
         motion="Qian Yuanwai sways a little on his knees with his sleeve-covered wrist against his forehead, then lowers the wrist and bows his head toward the desk; after the last word he stays bowed, his eyes sliding sideways",
         zh="【原稿 c37 拆成兩鏡之一】近景、慢推：錢員外跪著，左手腕連手縮在袖裡、第一格就已經抵在額頭上，身子晃一下，放下手腕朝上面的公案低頭求（原稿這句是胡縣令鏡頭裡的畫外音；兩句錄音共 11.4 秒，一支 10 秒裝不下）；說完低著頭、眼睛往旁邊溜；手始終在袖裡"),
    dict(sid="s37b", loc="hall", cam="Low-angle medium close-up, slow push in", chars=["huxianling"], night="hall",
         comp=f"low-angle medium close-up from below the platform: Magistrate Hu, {HU}, sitting behind the long dark desk, framed from the chest up with clear space above his hat, his right hand resting on {GAVEL} on the desk, his face three-quarter to screen right toward Qian Yuanwai off screen right, never the lens; impatient and dismissive: brows lifted, eyes half lidded, mouth drawn long between words; behind him only the plain white panels",
         lines=[("huxianling", "准了。午後升堂，兩案一起審，都到側廳候著！", "官腔，打發")],
         motion="Magistrate Hu lifts the wooden block a little and sets it down lightly on the desk, then waves his left sleeve once toward the side door; after the last word he looks away and smooths his sleeve",
         zh="【原稿 c37 拆成兩鏡之二】低角度中近景、慢推（身後只有空白屏板）：胡縣令把驚堂木輕輕一放、左袖往側門一揮，官腔打發；說完別開眼撫袖"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"close-up of {XU_POUCH}, framed from the chest up with space above his head, his head turned toward screen right, his face three-quarter to screen right, his eyes following Qian Yuanwai off screen right as he goes out, never the lens; cold and knowing: eyes narrowing slowly, brows drawn low, lips pressed flat; behind him only a dark red-brown pillar and the grey lattice window",
         lines=[("xuyan", "他想拖到午後，好把那雙手洗乾淨。", "冷，心裡話", "inner")],
         motion=f"Xu Yan's eyes follow the man out toward screen right and narrow; his jaw tightens once; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推：許硯轉頭看錢員外退出去的方向（畫右，畫外），眼睛慢慢一瞇、下巴一緊；全程嘴閉著（心裡話畫外）。原稿畫面左後唐小棠抱帳冊往門口走那一拍拿掉（近景只留他一人）"),
    # The side room (set-xianya-ceting-l1 swapped in): the curtained doorway on the left, the table at the back.
    dict(chapter="側廳", loc="side", cam="Medium-wide shot, slow push in", chars=["xuyan", "qianyuanwai"], night="hall", act=2,
         comp=f"medium-wide shot: on screen right {XU_POUCH}, standing beside the long table at the back, framed full length with clear space above his head, his face three-quarter to screen left toward the doorway, never the lens; guarded: brows drawn, eyes narrowed, lips closed; on screen left {QIAN}, framed full length, already just inside the curtained doorway at the left, the long grey curtain still swinging behind his shoulder, {SLEEVES_IN}, hurrying toward the young man, his face three-quarter to screen right, never the lens; furtive: eyes darting, lips pressed tight; {HANDS}; exactly two people",
         lines=[],
         motion=f"Qian Yuanwai walks quickly across the room in three short steps, glancing back once at the curtain, and stops close in front of Xu Yan; {quiet('Xu Yan and Qian Yuanwai', 'their', True)}",
         zh="中全景、慢推（送 `set-xianya-ceting-l1`：左邊門口掛長灰布簾、後牆一張條桌兩把椅、右邊一扇窗）：畫右許硯站在條桌邊；畫左錢員外第一格已經進了布簾、簾子還在他肩後晃（原稿『用肩膀頂開門簾』並進第一格），兩手縮在袖裡，回頭看一眼簾子，快步三步到許硯面前；兩人嘴閉著（無台詞）"),
    # Contact as a state: his sleeved left wrist already hooked over Xu Yan's right forearm (both arms on the near side).
    dict(loc="side_c", cam="Medium close two-shot, slow push in", chars=["xuyan", "qianyuanwai"], night="hall",
         comp=f"medium close two-shot: on screen left {XU_POUCH}, framed from the chest up with space above his head, his face three-quarter to screen right toward the man, his eyes lowered to his own sleeve, never the lens; still and cold: brows drawn, lips pressed flat; on screen right {QIAN}, framed from the chest up, leaning in close to him, his left wrist, wrapped in the wide dark gold sleeve with the hand hidden inside it, already hooked over Xu Yan's right forearm from the first frame, his right hand hidden inside his right sleeve, his face three-quarter to screen left toward Xu Yan, never the lens; sly and desperate: eyes narrowed, brows lifted, lips moving low and fast between words; behind them only the plain grey wall; {HANDS}; exactly two people",
         lines=[("qianyuanwai", "放我一馬，告訴你誰推你下河。", "壓低聲音")],
         motion=f"Qian Yuanwai tugs Xu Yan's sleeve toward himself with his sleeved wrist and leans in to his ear; {quiet('Xu Yan')}, his eyes on the sleeve; after the last word Qian Yuanwai holds still, waiting",
         zh="近景雙人、慢推（身後只有灰牆）：畫左許硯低頭看自己的袖子（不笑、嘴閉著）；畫右錢員外湊近，左手腕連手縮在寬袖裡、第一格就已經勾在許硯的右前臂上（接觸寫成狀態；兩人靠鏡頭這側的手），往自己這邊一拉，貼著耳朵壓低聲音說；說完停住等他回答（結尾，懸念接第 19 集）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e018-r2/script.md`（c01–c40 對應 s01–s40；2026-11-06 的 r2 稿；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-16）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e011-e020.md`（拍法 1–18 條）。",
    "- 內部工作編號 918（`hailuo/{ff,clips}-dh-e918.json`、`colab/runs/e918/extras.json`、`colab/runs/e918-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e918-dh/`）；發布 slug `zhong-tian-qu-qi-e018-r2`。不放集數、不放片名卡；s01 接第 17 集 s40：兩天後的茶樓，許硯臉洗乾淨了，同一個燒剩的燈籠用舊藍布包著放上茶桌。",
    "- 照第 17 集審稿後的寫法一開始就照做：`OFFSCREEN_SPEECH = False`；背景寫在場的東西；道具寫在第一格、在主人那隻手；兩人接觸寫成第一格就已經的狀態（s21、s28、s30、s40）；紙只拍空白的背面或摺著（s05、s06、s09），帳冊合著、素封面；不用手指指人（s33、s35 改攤開手掌，e916 s26 的教訓）。",
    "- **唐小棠不露嘴說話**：她五句在畫面上的台詞（s03、s04、s06、s09、s13）從背後拍（nospeak，spec 拿掉她三張臉部參考圖與身分句），每鏡寫明「畫面裡唯一的年輕女子、唯一雙丸子頭粉緞帶的人」，固定在畫右前景（她坐茶桌右邊；s04 在窗邊，固定畫左前景）；s07 那句改成許硯聽的臉、她在畫外。她不說話的臉（s01、s31、s33）用第 7 集的中性外貌句。",
    "- **錢府帳房不給臉**：只拍背影（s01、s04、s11，臉朝窗）與手（s05、s12）；s05 一句畫外錄音，聲音 Puck（`r2.py` 的 `MINOR`，不改 `cast.json`）。s12 原稿的主觀全景（他從左邊樓梯下樓）改成手部插鏡：圖上的樓梯往鏡頭這邊下，走下去一定露臉。",
    "- **紅手**（拍法 12）：均勻的橘紅、像染料、皮膚完好，不是血也不是傷；寫成第一格就已經的狀態（s26 錢員外、s28 起賴三），不演『慢慢變紅』。白天 s31–s40 錢員外兩手整場縮在寬袖裡、袖口併在肚前，spec 拿掉他身分句的金戒指；s40 用袖子包著的手腕勾許硯的右前臂。胡縣令與錢員外不同框。",
    "- **不拍兵器與衙役**：秦霜腰帶空著，s21 原稿『右手按上柴刀柄』改成按在柴堆上；公堂整場不拍衙役（拍法 16–18：背景寫了人就會配刀或長棍），『威武』只留音效；驚堂木是扁長方的木塊。",
    "- 場景（協調者 2026-11-16 決定，每張放大看過）：茶樓 `set-chalou-l1`（s01–s14；原稿窗邊小桌照圖改成窗下長凳）；新紙坊夜景**不送圖**（s15–s22；`set-zhifang-gujia-ye-l2` 是第 17 集正在立、有篝火的狀態，`-chen-l1` 是天亮，寫在文字裡）；錢府後巷**不送圖**（s23、s27–s30）；門縫裡看進去的後院 s24 送 `set-qianfu-houmen-ye-l1`（它畫的正是後門裡面的走道、燈籠與石桌）；公堂 s31–s38 送 `set-xianya-gongtang-l1`；側廳 s39–s40 送 `set-xianya-ceting-l1`。三張後者由 spec 的 `swap_pictures` 換進去（`gen-dh.mjs` 不加行）。**不用試鏡**。",
    "- 長鏡要買的秒數（BUY）：照 39 句錄音核過（`~/mokaair-work/videos/zhong-tian-qu-qi-e918-dh/audio`，faster-whisper 逐句聽寫，a05、a21、a34 重錄一次，第一次的檔在 `audio/take1/`；見 `r2.py` 的 BUY 註解）：s02 買 10 秒（心裡話兩句加系統，約 10.1 秒）；**原稿 c37 拆成 s37（錢員外求午後再審，6 秒）與 s37b（胡縣令准了，8 秒）**——兩句錄音約 11.4 秒，一支 10 秒裝不下；s25（錢員外 7.1 秒）、s31（6.9 秒）、s36（結巴乾笑 6.4 秒）買 8 秒；其餘 6 秒。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音長度＋0.5 秒為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯、唐小棠（l1 交領）、秦霜、賴三（`laisan-portrait-l1`）、錢員外（l1＋角度圖）、胡縣令（`huxianling-portrait-l1`）。錢府帳房沒有圖。場景 `set-chalou-l1`、`set-qianfu-houmen-ye-l1`（s24）、`set-xianya-gongtang-l1`（s31–s38）、`set-xianya-ceting-l1`（s39–s40）；紙坊夜景與後巷不送場景圖。",
    "- `gen-dh.mjs`、`build-r2.py`、`cast.json` 都不改（`teahouse` 已對到 `set-chalou`；公堂、側廳、後院走道由 spec 的 swap_pictures 換圖；帳房聲音在 `MINOR`）。",
    "- `colab/runs/e918/extras.json`（照 e916：畫面不放字幕、空氣清澈那句；拿掉秦霜的柴刀；胡縣令的官帽官袍照 e910–e912 的寫法、拿掉『笑起來臉頰會抖』）與 `colab/runs/e918-live/spec.json`（`mkspec.py` 產生；種子 9181101／9181102）。",
    "- 免費準備：`prep918.sh`（`DRY=1 REFS=~/mokaair-work/videos/zhong-tian-qu-qi-e918-dh/runpod/refs-dh-e918 VIDEO_JSON=docs/videos/zhong-tian-qu-qi-e018-r2/video.json st1-ep.sh 918` → `pilot.py runpod/a/st1 runpod/live/st1 s01…s40` → `retake.py runpod/live/st1 runpod/live/d1 colab/runs/e918-live/spec.json` → `colab-jobs.json` 加 output_path、套 swap_pictures（絕對路徑）→ 查每張參考圖都是絕對路徑、沒有送錯場景圖 → `preflight-prompts.py` → 否定名詞掃描）。",
    "- 配樂：茶樓俏皮的懸疑小調（s06 唸帳一個重音、s11 大聲那句後停一拍）；紙坊與後巷壓著的懸疑曲（低音撥弦，s26 紅手一個重音、s29 叮）；縣衙沉的鼓（s32 驚堂木一個重音、s40 一個低音後收）。音效表見 script.md〈音樂與音效〉（s05 改成紙推過木凳、收碎銀；s12 茶杯重放、抓帳冊；s31 衙役的『威武』低聲留著，人不入鏡）。",
]

# Long shots: seconds to buy. Measured 2026-11-16 against the 39 recordings (~/mokaair-work/videos/zhong-tian-qu-qi-e918-dh/audio;
# wave length and silencedetect -35 dB; e013's test: a shot holds (buy - 0.3) x 1.1 s of speech, half a second between lines).
# faster-whisper medium read every take back (scratchpad fw918.txt): three were re-recorded once, a05 (靠窗 heard as 靠床, 青衫 as
# 秦山), a21 (他要跑了 heard as 他又跑了: a different meaning) and a34 (錢員外 heard as 秦雲外); the first takes are in audio/take1/.
# The new takes read 靠窗／青山 (a homophone), 他要跑了, 前院外 (qián right, yuán read as yuàn by whisper). The rest are homophones
# or tone guesses of whisper (錢府 潛伏, 紙坊 脂肪, 魏記 未計, 許硯 許燕, 縣衙 線牙, 五兩 無量: wǔ liǎng with the third-tone sandhi);
# a32 知法 heard as 執法 but its 知 is level (130 Hz flat, first tone); a35 keeps the stutter 天、天 (two bursts 0.18-0.44 and
# 0.72-0.86 s before 天冷).
# 10 s: s02, the script's long shot (thought a02 4.76 + system a03 2.59 + thought a04 3.04 + 2 x 0.5 = 11.39 s with the edge
# silences, 10.07 s of speech without them, under the 10.67 s a 10 s clip holds).
# The script's c37 (a36 5.92 + a37 6.16 + 0.5 = 12.58 s, 11.39 s of speech) is more than a 10 s clip holds: it is split into
# s37 (Qian Yuanwai asks, a36, 6 s) and s37b (Magistrate Hu grants it, a37 6.16 s after setting the block down: 8 s).
# 8 s: s25 (a24 7.08 s, Qian Yuanwai's slow angry line with long pauses), s31 (a30 6.88 s), s36 (a35 6.40 s, the stutter).
# Every other line is 2.42-6.08 s and fits 6 s (s30's a29 6.08 s, s32's a31 6.04 s the tightest: 5.41 and 5.51 s of speech).
BUY = {"s02": 10, "s25": 8, "s31": 8, "s36": 8, "s37b": 8}
