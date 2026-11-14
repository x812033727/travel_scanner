"""Episode 10 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e010-r2/script.md
(c01-c40 = s01-s40), including its sections 「這版改了什麼」 and 「2026-11-06 審稿後的修改」, which override the tables (c10
「身上沒盤纏」, c22 「就我們幾個人」, c27 「看見火把往你家來」; c28 Qin Shuang takes one stick from a villager; about sixteen
torches, each in one person's hand; Qian Yuanwai and Magistrate Hu never share a frame except the c34 hands).

Live action from the first draft (owner 2026-11-11: 「之後都用真人版」), written the way e009-r2/r2.py wrote it, plus what
the e909 live pick review found (colab/runs/e909-live/{review-picks-a,review-picks-b}.tsv, pick-review.md, fix1, fix2):
- Over-the-shoulder shots: the foreground person is never named and is not in `chars`, so no picture of them is sent
  (e909: a second Tang Xiaotang or a second A-ling appeared whenever the foreground person's face pictures went in; fix1
  s27/s28 and fix2 s25/s26 took them out). The foreground is written as "one young man / one young woman ... seen only from
  behind, the back of the head toward us the whole time, no cheek, no profile and no lips at any moment, appearing only once".
- Tang Xiaotang never speaks on camera this episode: both her on-screen lines (c23 scared, c30 small voice) are shot from
  behind her, `nospeak`, the recording laid in, and `colab/runs/e910-live/spec.json` drops her three face pictures and her
  identity sentence there (e908 fix1, e909 s09/s12). Her face only in c36, silent, with e907's neutral face sentences in
  spec.json. With both lines recorded her voice does not jump between recording and clip voice inside the episode.
  Costume: the live portrait (tangxiaotang-portrait-l1, cross-collared short jacket wrapped shut), not the script's t2 high
  collar (no live t2); the script's night outer jacket in light apricot is left out, so the back view matches c36 and the
  portrait (owner to confirm). Her abacus is plain dark wood with no carving or inlay on the frame or beam (e909 s14: the
  beam grew a row of gold glyphs).
- Qin Shuang: the script's 「柴刀插腰帶右邊（本集不拔刀）」 is not shown. Her cast sentence loses the knife (extras.json), her belt
  is written plain with nothing tucked in it, and every shot of her says no blade anywhere (e906: a knife written sheathed
  was drawn in her hand anyway). From c28 she holds one plain wooden stick in her RIGHT hand (STICK), c36 tip down.
- A-ling: the scar is the pale, long-healed kind (e909: it came out red in every take; fix1/fix2 wrote "thin long-healed
  scar, pale whitish and never red"), and is shown only in the c06 insert, where she pulls her sleeve over it; every other
  shot of her writes both long sleeves down over both wrists. c31 the dagger is not shown at all: both hands empty, then
  drawn into her sleeves, no blade anywhere. The bundle is one grey-blue cotton bundle with its strap knotted in front of
  her right shoulder (c01-c13), untied in c14, on the ground in c18.
- The bedding of e009 is fixed to one colour (e909: the bedroll turned purple, cream and pink from shot to shot): a flat
  grey-blue coarse cloth bedding mat and one thick plain dark indigo quilt, the same dark indigo all over with no trim.
- Point-of-view shots (c18, c22) name nobody and send no picture of the one looking; c22 says nobody is on the wall in
  the foreground. Xiaohe's hands in c18 are unnamed hands from the edge.
- Insert close-ups open directly on their subject (c06 wrist, c14 knot, c34 money pouch); c34 is two hands only, Qian
  Yuanwai's an ordinary skin tone (the script), no writing on the pouch or the curtain.
- Night is night: the yard and the road are written "deep night, the sky black, no daylight anywhere", the yard lit only
  by one lantern, the road only by torches (e909: the window paper and the yard came out daylight-bright).
- At most three named people on screen (c07 and c36 have three). Crowds are written in Song-dynasty clothing; every
  torch is held in one person's hand. No drawn blade anywhere; the constable's sword is not written.
- Nobody is flipped in the edit: everyone wears a cross collar (Tang, Qin, A-ling, Xiaohe) or a crossed robe; axes are
  written with screen left/right in every shot (e904, e908: hflip makes a left-over-right collar).
- c26: the script's 「畫面上緣是許硯正從牆頭爬下來的腿」 is dropped (e909: extra legs in a doorway read as a second person).
State: morning (c01-c18) Xu Yan slept in his clothes on the corridor floor: robe creased, a few strands out of his topknot
(XU_DAY). Night (c19-c40) an old grey cloth outer coat over his robe, both hands empty (XU_NIGHT; c20 he ties its sash).
Xiaohe has a grey smear of stove ash on her right cheek c07-c08 (wiped in c08), clean from c09.
Places: the corridor in the morning has its own live picture (refs-live/set-xujia-zoulang-chen-l1, not yet drawn: the
e909 picture is night, with the doors on the other side); the yard in the morning uses set-xujia-yuan (live l2); the yard
at night has its own picture (set-xujia-yuan-ye-l1, not yet drawn: l2 is a sunny day with a yellow rape field); the village
road outside the yard gate at night is new (set-xujia-menwai-l1, not yet drawn). gen-dh.mjs's SET table maps the place
phrases "morning corridor of the Xu farmhouse", "night yard of the Xu farmhouse" and "village road outside the Xu yard
gate" to them. Magistrate Hu has no live portrait yet (huxianling-portrait-l1). All four are in
live-action/screen-test-e010.py; pilot.py stops on every shot that needs one until the file exists (FOOT lists them).
"""
EP = 910  # internal working number; the published slug is zhong-tian-qu-qi-e010-r2
SLUG = "zhong-tian-qu-qi-e010-r2"
EP_TITLE = "留住阿令，火把圍屋（重製版 r2）"
OUTLINE_SECONDS = 226  # script.md: 226 s, 40 shots (95.5 + 79 + 51.5)
TARGET_MINUTES = [3, 5]
TITLE = "留住阿令，火把圍屋｜種田娶妻打天下 第10集（重製版）"
DESCRIPTION = "第五天清晨，阿令背著包袱從房裡出來，要走。系統下任務：留住阿令。她說她多待一天，許家就多一分險，來找她的人不是為了錢。小禾端著早飯跑來，聽到「出遠門」就哭了：娘出遠門的時候也是這樣說的。許硯蹲下來說，找她的人要是來了，就讓他們先過這個家；他不知道那些人是誰，只知道她在婚書上是許家的人。阿令自己解開包袱，留了下來。當夜，秦霜從院牆翻回來：路上有火把，三十來個衙役家丁往村裡來。她在牆頭數出隊形，叫二牛帶來的八個村民蹲在籬笆後，誰都不許先打。火把圍到院門外，錢員外把一袋銀子塞進官轎；胡縣令下轎，抬手一指：拿下那個不說話的女人。《種田娶妻打天下》第 10 集（重製版）。"
THUMB = ("火把圍屋", "s32")
CHARACTERS = ["xuyan", "aling", "xiaohe", "qinshuang", "tangxiaotang", "erniu", "zhaobutou", "qianyuanwai", "huxianling", "xitong"]
MINOR = {}  # every speaker has a cast.json voice (Magistrate Hu: Iapetus, as the CG e010); villagers, runners, servants and bearers are silent
MUSIC = "one cue per scene: a warm gentle cue of soft strings, guzheng and dizi through the sunlit morning corridor and yard, dropping out for one beat under the system's jab and a soft chime when the favour rises; a tense cue of low taiko and plucked strings at night in the lantern-lit yard, one hit when the line of torches appears, the drum beats growing denser as the villagers are placed; a low dark suspense cue of low cello and deep drums outside the gate in the torchlight, one heavy hit as the magistrate steps out of the sedan and one big hit on the last command; ancient Chinese rural drama, no vocals"

# Scene headers of script.md. Scene 1: the corridor in the morning (A-ling's door on screen left, the house door to the yard
# at the right end, low sun from the right), then the yard in the morning (the cookhouse doorway on screen left, the stone
# table in the middle, the house door at the back left, the yard gate on screen right). Scene 2: the yard at night near
# midnight (the yard wall and gate on screen right, the house door at the back left, one blank lantern under the eaves).
# Scene 3: the village road outside the yard gate at night (the fence and the gate on screen left, the road running off to
# screen right, torchlight only). Close shots use the short `_c` headers. No person's name in a place phrase.
LOC = {
    "hall": "In the morning corridor of the Xu farmhouse: packed-earth walls and rough timber posts, a row of plain wooden doors with no writing on them along the left-hand wall, at the right end of the corridor the open house door with the sunlit yard beyond its threshold, a packed-earth floor; low warm early-morning sunlight slanting in from the right along the floor, long soft shadows",
    "hall_c": "In the morning corridor of the Xu farmhouse, low warm morning sunlight slanting in from the right",
    "yard": "In the morning yard of the Xu farmhouse in autumn: a packed-earth yard, a bamboo fence, one persimmon tree, a bamboo drying pole, the low cookhouse doorway on screen left, one round stone table in the middle, the house door at the back left, the plain wooden yard gate on screen right; a clear autumn morning, warm low sunlight, long shadows",
    "yard_c": "In the morning yard of the Xu farmhouse, warm low autumn morning sunlight",
    "nyard": "In the night yard of the Xu farmhouse near midnight: the packed-earth yard, the packed-earth yard wall capped with grey roof tiles on screen right with the plain wooden yard gate in it, the bamboo fence, the house door at the back left, one blank paper lantern with no writing hanging under the eaves; deep night, the moon hidden behind clouds, the sky black, the only light the warm glow of the one lantern, no daylight anywhere, every window dark",
    "nyard_c": "In the night yard of the Xu farmhouse, deep night, the sky black, lit only by the warm glow of one blank paper lantern under the eaves",
    "road": "On the village road outside the Xu yard gate at night: a packed-earth road, the bamboo fence and the plain wooden yard gate of the Xu farmhouse on screen left, the road running away to screen right between dark fields; deep night with no moon, the sky black, lit only by flickering orange torchlight on faces and the fence, no daylight anywhere",
    "road_c": "On the village road outside the Xu yard gate at night, the sky black, lit only by flickering orange torchlight",
    "roadfar": "Looking out over the top of the yard wall along the village road outside the Xu yard gate at night: a packed-earth road between dark fields running toward a few dark village roofs; deep night with no moon, the sky black, no daylight anywhere",
    "gate": "On the village road outside the Xu yard gate at night, looking in through the open gateway, lit only by flickering orange torchlight from screen right, the sky black",
}
LIGHT = {
    "morn": "the low warm morning sunlight from the right stays unchanged",
    "day": "the warm autumn morning sunlight stays unchanged",
    "night": "the deep night and the one warm lantern glow stay unchanged, the sky stays black",
    "torch": "the flickering orange torchlight stays the only light, the sky stays black",
}

# Repeated wording (each prop is one object; the descriptions say "one" where it first appears).
XU_DAY = "his faded blue-grey scholar's robe with one small sewn cloth patch at one elbow, slept in and creased all over, a few loose strands of hair fallen from his topknot"
XU_NIGHT = "an old plain grey cloth outer coat over his faded blue-grey scholar's robe, both hands empty"
HE = "little Xiaohe in her patched lilac short jacket with red-string pigtails and one front tooth missing, a small woven straw rabbit tucked into her sash"
ASH = "a faint grey smear of stove ash across her right cheek"
ALING = "A-ling in her plain grey-white cotton dress with long sleeves and one plain wooden hairpin, no shackles"
SLEEVES = "her long sleeves down over both wrists, no wrist showing"
BUNDLE = "one cloth bundle of plain grey-blue cotton on her back, its strap knotted in front of her right shoulder"
SCAR = "one thin long-healed scar, pale whitish and never red, across the inside of her left wrist"
QIN = "her dark brown cross-collared short jacket, wide plain leather belt with nothing tucked in it, black trousers, leather boots and high ponytail tied with black cord"
NOBLADE = "no blade, no knife, no sword, no scabbard and no weapon of any kind anywhere in the frame"
NOSHARP = "no blade, no knife, no sword and no spear anywhere in the frame, only plain wooden sticks"
STICK = "one plain straight wooden stick about as long as her arm"
STAFF = "one thick rough wooden staff taller than a man"
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
ABACUS = "one plain wooden abacus as long as her forearm, its frame and beam plain dark wood with no carving, no inlay, no marks and no writing"
# e908 fix1 / e909 s09: her back with no name and no face pictures (spec.json drops them); the ribbons, the pink inner collar
# and the light peach-pink written in (route-a.md 2026-11-12: without the pictures they came out short, white and orange).
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with two looped buns tied with pink "
         "silk ribbons and pearl pins, two long pink silk ribbons hanging from the buns down over her shoulders, a pink inner "
         "collar at the nape of her neck and her light peach-pink silk shoulders; the back of her head toward us the whole time, "
         "her ear the furthest round her head we ever see, no cheek, no profile and no lips at any moment")
HIM_BACK = ("one young man seen only from behind, appearing only once: only his {what} and the back of his black topknot, his face "
            "never in the frame")
HER_BACK = ("the back of her head toward us the whole time, no cheek, no profile and no lips at any moment, appearing only once")
BEDDING = "one flat bedding mat of grey-blue coarse cloth on the earth floor"
QUILT = "one thick quilt of plain dark indigo coarse cloth, the same dark indigo all over with no trim and no border"
BOWL = "one plain brown pottery bowl of rice porridge"
VILLAGERS = "eight village men in ancient Chinese Song-dynasty coarse hemp cross-collared short jackets, cloth head wraps and cloth shoes, each holding one plain wooden stick"
ZHAO = "in his black futou cap and plain black round-collared constable's robe"
RUNNERS = "about eleven yamen runners in ancient Chinese Song-dynasty plain black round-collared robes, black caps and cloth shoes, each holding one burning torch in his right hand"
SERVANTS = "about eighteen household servants in ancient Chinese Song-dynasty black cross-collared short jackets, cloth head wraps and cloth shoes, four of them holding one torch each, the rest empty-handed or holding plain wooden clubs"
TORCH = "every burning torch held in one person's hand, none floating, none stuck in the ground"
QIAN = "short and portly, in his dark gold silk robe with roundel patterns, his hands an ordinary natural skin tone"
HU = "in his black official gauze hat and blue-green seventh-rank official robe"
SEDAN = "one official sedan chair of dark lacquered wood with a plain dark blue cloth curtain, no writing and no emblem anywhere on it"
POUCH = "one heavy dark red silk money pouch with no writing on it"
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
ONCE = "each person appears only once, nobody else behind them"


def him(what):
    return HIM_BACK.format(what=what)


SHOTS = [
    # ---- scene 1: the corridor in the morning (A-ling's door on screen left, the house door at the right end), then the yard.
    dict(chapter="要走", loc="hall", cam="Wide shot, slow push in", chars=["xuyan", "aling"], night="morn", act=4,
         comp=f"wide shot along the corridor past the wooden threshold of the house door in the foreground, both small in the frame: on the floor by the nearest door on screen left Xu Yan, {XU_DAY}, lying on {BEDDING} under {QUILT}, his face three-quarter to screen left toward that door, never the lens; groggy: eyes heavy, brows knitted, lips closed; behind him the plain wooden door on screen left; {ALING}, {BUNDLE}, {SLEEVES}, standing in that doorway; {ONCE}",
         lines=[],
         motion=f"Xu Yan sits up on the bedding; the door behind him creaks open and A-ling steps out, steps over the edge of his quilt and walks off toward the sunlit house door on screen right without stopping; nobody speaks; all lips stay closed; {NOSMILE}",
         zh="全景、慢推、前景屋門門檻：晨光；許硯在阿令房門外（畫左）的地鋪上（灰藍粗布鋪蓋、深藍厚被，沒有滾邊），衣服睡皺；他坐起來，身後的門打開，阿令（沒戴鐵鐐、背灰藍布包袱、袖子蓋住手腕）跨過他的被子往畫右的屋門走；沒有人說話。live：走廊用晨景新圖（門在左牆、屋門在右端）"),
    dict(loc="hall", cam="Over-the-shoulder medium shot, tracking", chars=["xuyan"], night="morn",
         comp=f"over-the-shoulder medium shot from close behind one young woman's left shoulder: in the left foreground only her grey-white cotton shoulder with the strap of a grey-blue cloth bundle across it and the back of her head with long black hair pinned up by one plain wooden hairpin, {HER_BACK}; on screen right Xu Yan, {XU_DAY}, standing at his full height, framed from the knees up with clear space above his head, his face three-quarter to screen left toward her, never the lens; urgent: brows drawn together, eyes fixed on her, lips firm between words; nobody else in the corridor",
         lines=[("xuyan", "一早就背包袱，妳昨晚說的不是夢話？", "追問，不笑")],
         motion=f"Xu Yan throws the quilt off, gets up to his full height, his whole head staying in the frame, strides round in front of her on screen right and throws his right arm out across the corridor to bar the way; {NOSMILE}",
         zh="過肩（阿令左肩後拍許硯）、跟拍：前景左只有阿令的肩、包袱帶與後腦木簪（不點名、不送她的參考圖，只出現一次）；許硯掀被站起（膝以上、頭上留空），大步繞到她前面（畫右）抬右手攔住走廊；不笑"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"close-up of Xu Yan, framed from the chest up with space above his head, {XU_DAY}, standing in the corridor, his face three-quarter to screen right toward the young woman in front of him, never the lens; first his eyes sharpening and his brows drawing together, later one short breath out through the nose and his chin tucking in, lips closed the whole shot; at the right edge of the frame, soft and out of focus, only one young woman's grey-white shoulder and the back of her head with its plain wooden hairpin, {HER_BACK}; nobody else",
         lines=[("xitong", "叮。任務：留住阿令。", "冷淡，宣布"),
                ("xuyan", "怎麼留？我總不能把人綁起來。", "心裡話，嘴閉著，為難", "inner"),
                ("xitong", "綁起來叫押人。人不是東西，宿主自己說的。", "冷，嫌棄")],
         panel=[("任務：留住阿令", "task")],
         motion=f"the blurred young woman at the right edge gives one small nod; Xu Yan's eyes steady and his brows draw together; he stays silent and still, thinking; near the end he lets out one breath through his nose and tucks his chin in; his lips stay closed the whole shot; {NOSMILE}",
         zh="近景、慢推（長鏡，買 10 秒）：前景右虛焦只有阿令的肩與後腦（只出現一次），她先點一下頭；許硯眼神一定、眉頭皺起；系統（面板）→ 心裡話 → 系統吐槽；最後他吐一口氣、下巴一收；全程嘴閉著、不笑"),
    dict(loc="hall", cam="Over-the-shoulder medium shot, slow push in", chars=["aling"], night="morn",
         comp=f"over-the-shoulder medium shot from close behind {him('creased faded blue-grey shoulder')}, in the left foreground; on screen right {ALING}, {BUNDLE}, {SLEEVES}, standing, framed from the waist up with space above her head, her face three-quarter to screen left toward him, never the lens; resolved and cool: brows level, eyes lifting steadily to his, lips firm between words, no smile; nobody else",
         lines=[("aling", "不是夢話。我在這裡多待一天，你們就多一分險。", "淡，篤定")],
         motion=f"A-ling pulls the bundle strap tight across her chest with both hands, then lifts her eyes to him; {NOSMILE}",
         zh="反打（許硯肩後拍阿令）、慢推：前景左只有許硯的肩與髮髻（不點名、不送他的參考圖）；阿令兩手拉緊包袱帶、抬眼看他說話，不笑；袖子蓋住手腕"),
    dict(loc="hall", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="morn",
         comp=f"over-the-shoulder medium shot from close behind one young woman's left shoulder: in the left foreground only her grey-white cotton shoulder with the strap of a grey-blue cloth bundle across it and the back of her head with its plain wooden hairpin, {HER_BACK}; on screen right Xu Yan, {XU_DAY}, standing at his full height in the open house door at the right end of the corridor, framed from the knees up with clear space above his head, the sunlit yard behind him, his face three-quarter to screen left toward her, never the lens; puzzled and pressing: brows drawn up, eyes searching hers, lips moving between words, no smile; nobody else",
         lines=[("xuyan", "什麼險？錢員外的債都還清了，誰還能來？", "不解，追問")],
         motion=f"Xu Yan takes one step forward and braces his right hand flat on the frame of the house door, blocking the way out; {NOSMILE}",
         zh="過肩（阿令左肩後拍許硯）、慢推：前景左阿令的肩與後腦（只出現一次）；許硯站在走廊右端的屋門口（身後是陽光下的院子），往前一步、右手撐住門框擋路說話，不笑"),
    dict(loc="hall_c", cam="Insert close-up, slow push in", chars=[], night="morn",
         comp=f"insert close-up, the shot opens directly on one young woman's left wrist and the grey-white cotton cuff of her sleeve from its very first frame, the inside of the wrist turned toward us showing {SCAR}; only the wrist, the cuff and her right hand are in the frame, no face; morning light on the cotton",
         lines=[("aling", "來找我的人，不是為了錢。他們會找到這裡。", "低")],
         motion="her right hand takes hold of the left cuff and pulls the sleeve down over the wrist until the scar is covered, then both hands lower; the scar never shows again",
         zh="插鏡、慢推（第一格就是手腕）：阿令左手腕內側一道發白的舊疤（不是紅的）；右手把左袖往下一拉蓋住；嘴不入鏡，阿令畫外低聲（剪接放錄音）；之後各鏡都寫「袖子蓋住手腕」"),
    dict(chapter="院子", loc="yard", cam="Wide shot, tracking", chars=["xiaohe", "xuyan", "aling"], night="day",
         comp=f"wide shot past a bamboo drying pole hung with one plain undyed cloth shirt in the foreground, everyone small in the frame: on screen left {HE}, {ASH}, coming out of the low cookhouse doorway with {BOWL} in both hands, her face three-quarter to screen right toward the house door, never the lens; alarmed: brows shooting up, eyes wide, lips moving between words; at the house door at the back left Xu Yan, {XU_DAY}, standing, and beside him {ALING}, {BUNDLE}, {SLEEVES}, standing; {ONCE}",
         lines=[("xiaohe", "嫂嫂要去哪？早飯都煮好了，有妳的那碗！", "急")],
         motion=f"Xiaohe sees the bundle, sets the bowl down on the round stone table with a clack and runs toward the house door; Xu Yan's and A-ling's lips stay closed; {NOSMILE}",
         zh="全景、跟拍、前景晾衣竿上一件素色布衣：小禾（臉頰一抹灶灰）雙手端一碗粥從灶房（畫左）出來，看到包袱，把碗往石桌一放、跑過去；左後屋門口許硯、阿令（背包袱）站著、嘴閉著"),
    dict(loc="yard", cam="Low-angle medium shot, slow push in", chars=["aling", "xiaohe"], night="day",
         comp=f"low-angle medium shot at a child's eye height: on screen left {ALING}, {BUNDLE}, {SLEEVES}, squatting down so her eyes are level with the child's, framed with space above her head, her face three-quarter to screen right toward the child, never the lens; gentle but holding back: brows soft, eyes lowered to the child, lips moving softly between words, no smile; on screen right {HE}, {ASH}, standing, her face three-quarter to screen left up toward A-ling, never the lens; stubborn and close to tears: lower lip trembling, eyes wide and wet, lips closed; {ONCE}",
         lines=[("aling", "小禾乖，嫂嫂出趟遠門，妳跟哥哥好好吃飯。", "放輕")],
         motion=f"A-ling squats down level with Xiaohe and wipes the ash off the girl's cheek with her right thumb, the cheek clean afterwards; Xiaohe's lips stay closed; {NOSMILE}",
         zh="低角度中景（小禾的高度）、慢推：阿令蹲下跟小禾平視，用右手拇指擦掉她臉頰的灶灰，放輕說話、不笑；小禾快哭、嘴閉著"),
    dict(loc="yard_c", cam="Close-up, slow push in", chars=["xiaohe"], night="day",
         comp=f"close-up of {HE}, her cheeks clean, framed from the chest up with space above her head, her face three-quarter to screen right toward the young woman in front of her, never the lens; crying: face crumpling, brows pulled up in the middle, tears running down, mouth wide open in sobs between words; at the right edge only one grey-white cotton shoulder of that young woman, out of focus, {HER_BACK}",
         lines=[("xiaohe", "妳騙人！娘出遠門的時候，也是這樣說的！", "哭出來")],
         motion=f"Xiaohe flings both arms round the neck of the young woman at the right edge, tears spilling, and wails; {NOSMILE}",
         zh="近景、慢推：小禾（臉已擦乾淨）一把抱住畫右阿令的脖子（阿令只露虛焦的肩、不點名），眼淚掉下來、張嘴哭喊"),
    dict(loc="yard_c", cam="Close-up, slow push in", chars=["aling"], night="day",
         comp=f"close-up of {ALING}, {BUNDLE}, {SLEEVES}, squatting, framed from the chest up with space above her head, one little girl's arms wrapped round her neck and only the top of the child's small head with two red-string pigtails at the bottom edge of the frame, the child's face never seen; A-ling's face three-quarter to screen left, eyes lowered past the child's head, never the lens; moved and holding it in: eyes trembling once, brows easing, lips pressed shut; nobody else",
         lines=[("xuyan", "妳一個人，身上沒盤纏，能走到哪裡去？", "低，問")],
         motion=f"A-ling's right hand stops on the child's back; her eyes tremble once and she slowly tightens her arms round the girl; her lips stay closed; {NOSMILE}",
         zh="近景、慢推：蹲著的阿令被小禾抱住脖子（畫面下緣只有小禾的頭頂與紅繩小辮，不點名）；手停在小禾背上、眼睛顫一下、慢慢收緊手臂；嘴閉著；許硯畫外（剪接放錄音）"),
    dict(loc="yard", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="day",
         comp=f"over-the-shoulder medium shot from close behind one squatting young woman's left shoulder: in the left foreground only her grey-white cotton shoulder, the back of her head with its plain wooden hairpin, and the small head of a little girl with two red-string pigtails hugging her neck, both seen from behind, the backs of their heads toward us the whole time, no cheek, no profile and no lips at any moment, each appearing only once; on screen right Xu Yan, {XU_DAY}, squatting down level with them, framed from the chest up with space above his head, his face three-quarter to screen left toward them, never the lens; very steady: brows level, eyes calm and firm on her, lips moving between words, no smile; nobody else",
         lines=[("xuyan", "找妳的人要是來了，就讓他們先過這個家。", "很穩")],
         motion=f"Xu Yan squats down level with the two of them, his whole head staying in the frame, and rests his forearms on his knees; {NOSMILE}",
         zh="過肩（阿令左肩後拍許硯）、慢推：前景左只有阿令的肩、木簪與抱著她的小禾後腦（都不點名、只出現一次）；許硯也蹲下來跟她們平視，很穩地說，不笑"),
    dict(loc="yard", cam="Over-the-shoulder medium shot, slow push in", chars=["aling"], night="day",
         comp=f"over-the-shoulder medium shot from close behind {him('creased faded blue-grey shoulder')}, squatting in the left foreground; on screen right {ALING}, {BUNDLE}, {SLEEVES}, squatting, framed from the chest up with space above her head, a little girl clinging round her neck with only the back of the child's small head with two red-string pigtails under A-ling's chin, the child's face never seen; A-ling's face three-quarter to screen left toward him, never the lens; searching and wary: brows drawn slightly together, eyes lifting to his, lips moving between words, no smile; nobody else",
         lines=[("aling", "你知不知道，他們是什麼人？", "低，盯著他")],
         motion=f"A-ling lifts her chin from the child's head and raises her eyes to him; {NOSMILE}",
         zh="反打（許硯肩後拍阿令）、慢推：前景左只有許硯的肩與髮髻（不點名）；阿令下巴從小禾頭上抬起、抬頭看他說話，不笑"),
    dict(loc="yard_c", cam="Close-up, slow push in", chars=["xuyan"], night="day",
         comp=f"close-up of Xu Yan, squatting, framed from the chest up with space above his head, {XU_DAY}, his face three-quarter to screen right toward A-ling off screen right, never the lens; certain: brows level, eyes steady on her, lips moving firmly between words, no smile; behind him only the sunlit packed-earth yard and the bamboo fence",
         lines=[("xuyan", "不知道。我只知道妳在婚書上，是許家的人。", "平靜，篤定")],
         motion=f"Xu Yan reaches his right hand out toward screen right and lays it on the knot of a grey-blue cloth bundle strap at the right edge of the frame; {NOSMILE}",
         zh="近景、慢推：許硯蹲著，伸右手按住畫右緣的包袱結說話，平靜篤定、不笑"),
    dict(loc="yard_c", cam="Insert close-up, slow push in", chars=[], night="day", act=3,
         comp="insert close-up, the shot opens directly on the knot of a grey-blue cloth bundle strap in front of a young woman's right shoulder from its very first frame: one man's hand in a creased blue-grey cuff resting on the knot; only the hands, the cuffs, the knot and the grey-white cotton of her dress are in the frame, no face",
         lines=[],
         motion="a slender hand in a grey-white cuff, the sleeve down over its wrist, comes up and rests on top of the man's hand for a moment; then it unties the knot by itself and the grey-blue bundle slides down out of the frame to the ground",
         zh="手部特寫、慢推（第一格就是包袱結）：許硯的手（藍灰袖口）按在結上；阿令的手（灰白袖口、袖子蓋住手腕）覆上來、停一下，自己解開，包袱滑落出畫（無台詞）"),
    dict(loc="yard_c", cam="Close-up, slow push in", chars=["aling"], night="day",
         comp=f"close-up of {ALING}, {SLEEVES}, nothing on her back any more, squatting, framed from the chest up with space above her head, holding a little girl against her shoulder, only the back of the child's small head with two red-string pigtails in the lower left, the child's face never seen; A-ling's face three-quarter to screen left toward the child, never the lens; softening for the first time: brows easing, eyes warm and lowered, voice soft, lips moving gently between words, no smile",
         lines=[("aling", "好，不走。小禾，把我那碗粥端來。", "很輕，第一次軟下來")],
         motion=f"A-ling pats the sobbing child's back gently with her right hand; {NOSMILE}",
         zh="近景、慢推：阿令（包袱已落地）摟著還在抽噎的小禾（只露後腦），手輕拍她的背，聲音第一次軟下來；不笑"),
    dict(loc="yard_c", cam="Close-up, slow push in", chars=["xuyan"], night="day",
         comp=f"close-up of Xu Yan, {XU_DAY}, framed from the chest up with clear space above his head the whole time, his face three-quarter to screen right toward A-ling off screen right, never the lens; relieved: shoulders dropping, a long breath out, brows easing, lips closed",
         lines=[("xitong", "叮。阿令，好感加四。", "冷淡，報數")],
         panel=[("阿令 好感 +4 → 15", "panel")],
         motion=f"Xu Yan lets out a long breath, then pushes on his knees and slowly comes up from his squat to stand, the frame rising with him so his whole head stays in the frame; his lips stay closed; {NOSMILE}",
         zh="近景、慢推：許硯鬆一口氣，手撐膝蓋慢慢站起來（頭一直在畫面裡）；嘴閉著；系統（面板）"),
    # Xiaohe may smile here (the script: 破涕為笑).
    dict(loc="yard", cam="Medium shot, tracking", chars=["xiaohe"], night="day",
         comp=f"medium shot of {HE}, her cheeks clean, framed from the knees up with space above her head, at the round stone table with {BOWL} in both hands, her face three-quarter to screen left toward the house door, never the lens; laughing through tears: eyes still wet and red, sniffling, a big gap-toothed smile breaking out between words",
         lines=[("xiaohe", "我去端！嫂嫂說話算話，不能偷跑喔！", "帶著鼻音，破涕為笑")],
         motion="Xiaohe wipes her eyes with her sleeve, runs to the round stone table, picks up the bowl in both hands and turns back, calling out",
         zh="中景、跟拍：小禾用袖子抹眼淚，跑到石桌捧起粥碗、回頭喊（本鏡可以笑）"),
    dict(loc="yard", cam="Point-of-view shot, slow push in", chars=["aling"], night="day",
         comp=f"point-of-view shot looking down a little at the house door: {ALING}, {SLEEVES}, sitting on the wooden threshold of the house door, framed from the knees up with space above her head, the grey-blue cloth bundle lying on the ground by her feet; her face three-quarter to screen right where the bowl comes in, never the lens; quiet: brows soft, eyes lowered to the bowl, lips closed, no smile; from the right edge of the frame two small hands in patched lilac sleeves hold out {BOWL}, the child herself outside the frame; nobody else",
         lines=[("xitong", "任務，完成。", "冷，宣布")],
         panel=[("任務，完成", "task")],
         motion=f"A-ling takes the bowl with both hands and holds it on her knees; her lips stay closed; {NOSMILE}",
         zh="主觀（許硯看阿令）、慢推：不送許硯的圖；阿令坐在屋門門檻上、包袱在腳邊地上；畫右伸進兩隻小手（淡紫補丁袖）遞粥碗（小禾不入鏡）；阿令雙手接過、捧在膝上；嘴閉著；系統（面板）"),
    # ---- scene 2: the yard at night, near the third watch (the wall and gate on screen right, the house door at the back left).
    dict(chapter="火把", loc="nyard", cam="Wide shot, tracking", chars=["qinshuang"], night="night",
         comp=f"wide shot past one blank paper lantern with no writing hanging under the eaves in the foreground, the yard dark: Qin Shuang, {QIN}, small in the frame, dropping down from the top of the yard wall on screen right, her face in profile toward the house door at the back left, never the lens; urgent: brows drawn, eyes sharp, lips moving fast between words; the house door shut at the back left; {NOBLADE}; nobody else in the yard",
         lines=[("qinshuang", "都起來，路上有火把，往村裡來了。", "壓低聲音，急")],
         motion="Qin Shuang swings over the top of the wall on screen right, drops and lands on bent knees, straightens and strides fast to the house door at the back left and knocks on it twice with her fist",
         zh="全景、跟拍、前景屋簷下的空白燈籠（長鏡，買 8 秒）：深夜、天全黑、只有燈籠光；秦霜從院牆（畫右）翻下、屈膝落地，快步到左後屋門拍兩下，壓低聲音說；腰帶上沒有刀、畫面無兵器"),
    dict(loc="nyard", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="night",
         comp=f"over-the-shoulder medium shot from close behind one tall young woman's left shoulder: in the right foreground only her dark brown shoulder and the back of her head with a high ponytail tied with black cord, {HER_BACK}; on screen left Xu Yan, {XU_NIGHT}, stepping out through the house door at his full height, framed from the waist up with clear space above his head, his face three-quarter to screen right toward her, never the lens; suddenly wide awake: brows up, eyes sharp, lips moving fast between words, no smile; the warm lantern glow on his face; nobody else",
         lines=[("xuyan", "多少人？是衝著我們家來的？", "一下清醒")],
         motion=f"Xu Yan pushes the house door open and steps out, tying the sash of the grey outer coat as he comes, his eyes on her; {NOSMILE}",
         zh="過肩（秦霜肩後拍許硯）、慢推：前景右只有秦霜的肩與高馬尾（不點名）；許硯推門出來（書生袍外披舊灰布外衣、邊走邊繫衣帶），一下清醒地問"),
    dict(loc="nyard_c", cam="Medium close-up, slow push in", chars=["qinshuang"], night="night",
         comp=f"medium close-up from inside the yard: Qin Shuang, {QIN}, clinging to the top of the yard wall, her chest above the grey roof tiles along its top, both forearms on the tiles, framed from the waist up with space above her head, at first her back to us looking out over the wall, then her face turned back over her left shoulder in profile toward screen left, never the lens; calm and exact: brows level, eyes narrowed, lips moving evenly between words, no smile; behind her only the black night sky with a faint orange glow low on the horizon; {NOBLADE}; nobody else",
         lines=[("qinshuang", "三十來個，衙役家丁都有，只有這條路通我們家。", "冷靜")],
         motion=f"Qin Shuang pulls herself up so her chest is above the wall top and looks out, then turns her head back over her left shoulder toward screen left; {NOSMILE}",
         zh="中近景、慢推（長鏡，買 8 秒）：秦霜攀上院牆、雙臂搭在牆頭瓦片上往外看，再回頭朝畫左冷靜地說；身後只有夜空與遠處一點橘光；畫面無兵器"),
    dict(loc="roadfar", cam="Point-of-view shot, slow push in", chars=[], night="torch",
         comp="point-of-view shot looking out over the grey roof tiles along the top of a yard wall in the foreground, far out along the dark road: a line of about sixteen burning torches coming slowly closer at walking pace, each torch held up by one person; at the front one constable with one torch, behind him two rows of yamen runners in ancient Chinese Song-dynasty plain black round-collared robes and black caps, each with one torch, at the back a loose group of household servants in Song-dynasty black cross-collared short jackets and cloth head wraps, four of them with torches; all of them small and far away; nobody on the wall, no person and no hands in the foreground",
         lines=[("xitong", "警告，三十人，一刻鐘後到。", "冷，報數"),
                ("xuyan", "就我們幾個人……有幾成勝算？", "心裡話，嘴閉著，沉", "inner"),
                ("xitong", "系統只報人數，不報勝算。", "冷，嫌棄")],
         panel=[("警告，三十人，一刻鐘後到", "penalty")],
         motion="the line of torches moves slowly along the road toward us at walking pace, the flames flickering; nothing else moves",
         zh="主觀（許硯攀上牆頭看出去）、慢推、前景牆頭瓦片（長鏡，買 8 秒）：遠處村路一列火把約十六支、每支拿在一個人手裡，最前一支（捕頭）、衙役兩列（黑公服）、後面家丁散著；人走路的速度；畫面裡沒有許硯、不送他的圖；系統（面板）→ 心裡話 → 系統"),
    # Converted: Tang Xiaotang's scared line from behind her (her on-screen speaking shots are all from behind this episode).
    dict(loc="nyard", cam="Medium shot, tracking", chars=["tangxiaotang", "qinshuang"], nospeak=["tangxiaotang"], night="night",
         comp=f"medium shot following from behind: {TBACK}; she runs from the house door to the foot of the yard wall, her elbows holding something against her chest out of sight; up on the top of the wall above her, small against the black sky, Qin Shuang, {QIN}, crouching on the roof tiles, her face in profile toward the road on screen right, never the lens, lips closed, no smile; {NOBLADE}; exactly two people in the frame, nobody else",
         lines=[("tangxiaotang", "三十個對我們五個，怎麼算都打不過啊。", "怕，聲音發抖")],
         motion=f"the young woman runs to the foot of the wall and stops, tipping her head back to look up at the top of the wall, the back of her head still toward us; up on the wall Qin Shuang keeps watching the road; Qin Shuang's lips stay closed; {NOSMILE}",
         zh="【改背後拍】中景、跟拍：從背後跟唐小棠從屋門跑到牆下（只有後腦、雙丸子頭、兩條長粉緞帶垂過肩、粉色內領、淡桃粉衣肩，臉與嘴不入鏡；算盤抱在胸前看不到）；她仰頭看牆頭；牆頭上秦霜蹲著看路、嘴閉著。台詞 nospeak，剪接放錄音；spec.json 拿掉她三張臉部參考圖。稿子是正面中景、臉發白"),
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["qinshuang"], night="night",
         comp=f"close-up of Qin Shuang, {QIN}, crouching on the top of the yard wall, framed from the chest up with space above her head, her face in profile toward screen right, eyes on the far road, never the lens; certain: eyes narrowed, brows level, lips moving crisply between words, no smile; behind her only the black night sky; the warm lantern glow from below on one side of her face and a faint orange glow from screen right; {NOBLADE}",
         lines=[("qinshuang", "前面十二把火排兩列，是衙役；後面散的是家丁。", "篤定")],
         motion=f"Qin Shuang narrows her eyes and points her right forefinger out toward screen right, ticking it along once for each far torch as she counts; {NOSMILE}",
         zh="近景、慢推：牆頭上的秦霜（身後只有夜空），瞇眼，右手食指朝畫右遠處的火把一支一支點著數，篤定地說"),
    dict(loc="nyard", cam="Over-the-shoulder medium close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"over-the-shoulder medium close-up along the top of the yard wall: in the right foreground only one tall young woman's dark brown shoulder and the back of her head with a high ponytail tied with black cord, {HER_BACK}; on screen left Xu Yan, {XU_NIGHT}, both hands gripping the roof tiles on top of the wall, his chest above the wall top, framed from the chest up with space above his head, his face three-quarter to screen right toward her, never the lens; stunned: brows shooting up, eyes wide on her, lips moving low between words, no smile; behind them only the black night sky; nobody else",
         lines=[("xuyan", "隔這麼遠，妳數得出隊形？妳打過仗？", "壓低聲音，愣住")],
         motion=f"Xu Yan turns his head from the road to her and stares; {NOSMILE}",
         zh="過肩（秦霜肩後拍許硯）、慢推：牆頭並排，前景右只有秦霜的肩與馬尾（不點名）；許硯兩手搭牆頭，轉頭看她、愣住，壓低聲音問"),
    dict(loc="nyard", cam="Low-angle medium shot, slow push in", chars=["qinshuang"], night="night",
         comp=f"low-angle medium shot at the foot of the yard wall: Qin Shuang, {QIN}, dropping down from the top of the wall and landing on bent knees, then straightening to her full height, framed with clear space above her head the whole time, her face three-quarter to screen left toward the man still up on the wall off screen, never the lens; curt and closed: brows level, eyes hard, lips moving briefly between words, no smile; behind her the dark earth wall; {NOBLADE}; nobody else in the frame, no legs and no hands at the top edge",
         lines=[("qinshuang", "看過。衙役沒拿到人之前，不敢先動手。", "不多說")],
         motion=f"Qin Shuang drops from the wall, lands on bent knees, straightens up and dusts off her palms against each other; {NOSMILE}",
         zh="低角度中景、慢推：秦霜從牆頭跳下、屈膝落地、站起拍掉手上的灰，不多說。live：稿子「畫面上緣是許硯爬下來的腿」拿掉（第 9 集門口多出的腿讀成第二個人）"),
    dict(loc="nyard", cam="Wide shot, tracking", chars=["erniu"], night="night",
         comp=f"wide shot past the bamboo fence in the foreground, the yard lit only by the lantern: the yard gate on screen right bursting open and Wang Erniu, in his coarse brown short jacket with rolled sleeves, {STAFF} on his right shoulder, running in out of breath, his face three-quarter to screen left toward the house door, never the lens; urgent and loud: brows up, eyes wide, mouth wide between words, chest heaving; behind him {VILLAGERS}, the last one carrying a second stick on his shoulder; {NOSHARP}; each person appears only once",
         lines=[("erniu", "許兄弟！看見火把往你家來，我叫了八個漢子！", "大嗓門，喘")],
         motion=f"the yard gate bangs open; Wang Erniu runs in panting and shouts toward the house, the eight men crowding in behind him with their sticks; {NOSMILE}",
         zh="全景、跟拍、前景籬笆（長鏡，買 8 秒）：院門被推開，二牛（褐短打、袖子捲起、右肩扛一根比人高的粗木棍）喘著跑進來喊；八個村民（宋式交領粗布短打、布包頭、布鞋，每人一根木棍，最後一個多扛一根）跟進來；沒有刀"),
    dict(loc="nyard", cam="Medium shot, slow push in", chars=["qinshuang", "erniu"], night="night",
         comp=f"medium shot in the yard: on screen left Qin Shuang, {QIN}, framed from the knees up with space above her head, her face three-quarter to screen right toward Wang Erniu, never the lens; commanding: brows level, eyes hard, lips moving crisply between words, no smile; on screen right Wang Erniu, in his coarse brown short jacket with rolled sleeves, {STAFF} in both hands, his face three-quarter to screen left toward her, never the lens; listening hard, lips closed; behind him two of the village men in Song-dynasty coarse hemp cross-collared short jackets and cloth head wraps, one with a second plain wooden stick on his shoulder; {NOSHARP}",
         lines=[("qinshuang", "二牛，八個人蹲籬笆後，棍子舉高。", "下令")],
         motion=f"Qin Shuang presses Wang Erniu's shoulder down with her left hand and points at the bamboo fence with her right, then takes the spare wooden stick from the village man behind him into her right hand; Erniu's and the men's lips stay closed; {NOSMILE}",
         zh="中景、慢推：秦霜左手壓低二牛的肩、右手往籬笆一指，再從多扛一根的村民手上拿過一根木棍（右手，之後一直在右手）；二牛、村民嘴閉著"),
    dict(loc="nyard", cam="Medium shot, slow push in", chars=["erniu"], night="night",
         comp=f"medium shot along the inside of the bamboo fence: Wang Erniu, in his coarse brown short jacket with rolled sleeves, and the eight village men in Song-dynasty coarse hemp cross-collared short jackets and cloth head wraps crouching low in a row behind the fence, each gripping one plain wooden stick upright, framed with space above their heads; Erniu nearest on screen left, his face three-quarter to screen right toward the voice off screen, never the lens; teeth clenched, jaw set, brows drawn down, no smile; every man's lips closed; {NOSHARP}",
         lines=[("qinshuang", "記住，誰都不許先打。他們先動手，我們才有理。", "低，下令")],
         motion=f"the men crouch down one after another and raise their sticks upright one by one behind the fence; Wang Erniu gives one firm nod; all lips stay closed; {NOSMILE}",
         zh="中景、慢推：二牛和八個村民蹲在籬笆後、握緊木棍一根根豎起來；咬牙、不笑；二牛點一下頭；秦霜畫外下令（剪接放錄音）"),
    # Converted: Tang Xiaotang's close-up line (script c30, 下巴以上) from behind her; Xu Yan answers off screen.
    dict(loc="nyard_c", cam="Close shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="night",
         comp=f"close shot from close behind {TBACK}, filling the left half of the frame, her elbows holding something against her chest out of sight; past her, out of focus in the dim lantern light, one tall young woman with a high ponytail tied with black cord, seen from behind, crouching by the bamboo fence beside a row of upright wooden sticks; nobody faces us",
         lines=[("tangxiaotang", "半刻鐘就排好了……她到底是什麼人？", "小聲"),
                ("xuyan", "不知道。但今晚，我們只能聽她的。", "低，篤定")],
         motion=f"the young woman in front keeps watching the woman by the fence; when a man's voice answers from off screen on the left she turns her head only a little toward screen left, her ear the furthest round her head we ever see, the back of her head still toward us; {NOSMILE}",
         zh="【改背後拍】近景、慢推（長鏡，買 8 秒）：從唐小棠背後拍（只有後腦、丸子頭、長緞帶與肩，臉與嘴不入鏡），遠處虛焦是蹲在籬笆邊排人的秦霜背影（不點名）；許硯畫外回話時她頭只往畫左偏一點。兩句都放錄音；spec.json 拿掉她三張臉部參考圖。稿子是下巴以上近景"),
    dict(loc="nyard", cam="Medium shot, slow push in", chars=["aling"], night="night",
         comp=f"medium shot past the edge of the half-open house door in the foreground: inside the dark doorway {ALING}, {SLEEVES}, both hands empty, standing in the shadow, framed from the knees up with space above her head, only a little warm lantern light on one side of her face, her face three-quarter to screen right toward the yard gate, never the lens; still and alert: eyes fixed, brows level, lips closed, no smile; {NOBLADE}; nobody else",
         lines=[("xuyan", "阿令，妳待在屋裡，不管聽到什麼都別出來。", "低")],
         motion=f"A-ling listens, gives one small nod, steps back into the dark and draws both hands up inside her sleeves; her lips stay closed; {NOSMILE}",
         zh="中景、慢推、前景半開的屋門：屋門內暗處的阿令（只有燈籠光照到半邊臉），聽完點頭、退進暗處、雙手縮進袖口；匕首不拍、畫面無兵器；許硯畫外（剪接放錄音）"),
    # ---- scene 3: the village road outside the yard gate (the gate on screen left, the column comes from screen right).
    dict(chapter="院門外", loc="road", cam="Wide shot, slow push in", chars=["zhaobutou"], night="torch",
         comp=f"wide shot past a row of upright wooden stick tips poking up behind the bamboo fence in the foreground: walking up the road from screen right Constable Zhao, {ZHAO}, one burning torch in his right hand, at the front, his face three-quarter to screen left toward the yard gate, never the lens; harsh: brows down, eyes narrowed, mouth wide between words; behind him {RUNNERS}, in two rows, and behind them {SERVANTS}; about thirty people and about sixteen torches in all, {TORCH}; no drawn blade and no sword in anyone's hand",
         lines=[("zhaobutou", "圍起來！前後門都給我堵住，一個都別放跑！", "粗聲")],
         motion=f"the column walks up at walking pace and halts outside the gate; Constable Zhao sweeps his left hand out and shouts; then about six runners with their torches peel off and hurry along the fence toward the back of the house; {NOSMILE}",
         zh="全景、推軌、前景籬笆後豎著的木棍尖（長鏡，買 8 秒）：趙捕頭（黑幞頭、黑圓領公服）右手一支火把走在最前，後面衙役兩列（約十一人十一支）、家丁散著（約十八人四支）；人走路的速度停在院門外；趙捕頭左手一揮喊；約六個衙役沿籬笆往屋後走；每支火把拿在一個人手裡；不寫佩刀、畫面沒有拔出的刀"),
    dict(loc="road", cam="Medium shot, tracking", chars=["qianyuanwai"], night="torch",
         comp=f"medium shot at the back of the column on the road: Qian Yuanwai, {QIAN}, climbing down from one black horse, framed from the knees up with space above his head, his face three-quarter to screen left toward the sedan, never the lens; one household servant in a Song-dynasty black cross-collared short jacket and cloth head wrap taking the horse's reins, the horse staying at the back right; on screen left {SEDAN}, set down on the road, its curtain closed, nobody seen inside; fawning: brows lifted, eyes eager, an oily ingratiating smile between words; {ONCE}",
         lines=[("xuyan", "騎馬跟在後面的，是錢員外。", "低，畫外"),
                ("qianyuanwai", "大人，人就在裡面，這一趟辛苦您了。", "陪笑")],
         motion="Qian Yuanwai lands on the ground, tugs his robe straight and trots to the side of the sedan, bowing toward its curtain, his whole head staying in the frame; while a man's voice speaks from off screen his lips stay closed, then he speaks to the curtain",
         zh="中景、跟拍（長鏡，買 8 秒）：隊伍後面錢員外從黑馬下來、一個家丁接過韁繩（馬在右後），整袍子、小跑到官轎（轎簾放著、素色沒有字）旁彎腰；先許硯畫外（錢員外嘴閉著），再錢員外陪笑說（本鏡可以陪笑）；胡縣令不入鏡"),
    dict(loc="road_c", cam="Insert close-up, slow push in", chars=[], night="torch",
         comp=f"insert close-up, the shot opens directly on {POUCH} from its very first frame, held in one plump hand with gold rings in a dark gold silk sleeve with roundel patterns, the hand an ordinary natural skin tone; beside it the plain dark blue cloth curtain of a sedan chair with a narrow gap, no writing on it; only the hands, the sleeves, the pouch and the curtain are in the frame, no face",
         lines=[("tangxiaotang", "那袋子少說五十兩，買的是我們一家。", "咬牙小聲")],
         motion="the plump hand pushes the pouch into the gap in the curtain; a hand in a wide blue-green official sleeve comes out through the gap, takes the pouch and draws it back inside the sleeve; the curtain falls shut",
         zh="手部特寫、慢推（第一格就是錢袋）：錢員外的胖手（金戒指、深金團花錦袍袖口、一般膚色）把暗紅綢錢袋塞進轎簾縫，一隻藍綠官袍袖的手接過去收進袖子；唐小棠畫外咬牙小聲（剪接放錄音）"),
    # Magistrate Hu may put on a fake smile here (the script).
    dict(loc="road", cam="Low-angle medium shot, slow push in", chars=["huxianling"], night="torch",
         comp=f"low-angle medium shot by the sedan: Magistrate Hu, {HU}, stepping out of {SEDAN} as its curtain is lifted, framed from the knees up with clear space above his head, his face three-quarter to screen left toward the yard gate, never the lens; pompous: chin raised, eyes narrowed, a fake official smile with his plump cheeks quivering between words; on either side only the bodies of the sedan bearers from the shoulders down, in Song-dynasty cross-collared short jackets, their heads out of the frame; nobody else",
         lines=[("huxianling", "錢員外放心，本官心裡有數，今晚就辦。", "官腔，拖長音")],
         motion="the curtain is lifted; Magistrate Hu steps out of the sedan, plants his feet and straightens his official hat with both hands, his whole head staying in the frame",
         zh="低角度中景、慢推：轎簾掀開，胡縣令（黑官帽、藍綠七品官袍）跨出轎子、雙手扶正官帽，官腔拖長音（本鏡可以假笑、臉頰跟著抖）；轎夫只露肩以下；錢員外已退到轎後、不入鏡"),
    dict(loc="gate", cam="Medium shot, slow push in", chars=["xuyan", "qinshuang", "tangxiaotang"], night="torch",
         comp=f"medium shot through the frame of the plain wooden yard gate in the foreground: Xu Yan, {XU_NIGHT}, at the front in the gateway, framed from the knees up with space above his head, his face three-quarter to screen right toward the officials off screen right, never the lens; steady: brows level, eyes hard, lips moving firmly between words, no smile; behind him on screen left Qin Shuang, {QIN}, {STICK} in her right hand with its tip down, her face toward screen right, lips closed, no smile; behind him on screen right Tang Xiaotang {TANG}, holding {ABACUS} against her chest, frightened: face pale, eyes wide, lips pressed shut; {ONCE}; no blade, no knife and no sword anywhere in the frame",
         lines=[("xuyan", "三更半夜，縣太爺親自下鄉，找的是誰？", "擋在前面，很穩")],
         motion=f"Xu Yan lays a hand on Tang Xiaotang's shoulder and eases her back behind him, then pulls the gate wide open, steps out and spreads both arms across the gateway; Qin Shuang's and Tang Xiaotang's lips stay closed; {NOSMILE}",
         zh="中景、慢推、前景院門門框（長鏡，買 8 秒）：許硯（披舊灰外衣、兩手空空）先按唐小棠的肩讓她退到身後，再拉開院門走出來、張開雙臂擋在門口；身後秦霜（右手一根木棍、刀尖朝地、腰帶上沒刀）、唐小棠（定妝照交領、抱木算盤、臉發白）嘴閉著；一鏡三人"),
    dict(loc="road", cam="Over-the-shoulder medium shot, tracking", chars=["huxianling"], night="torch",
         comp=f"over-the-shoulder medium shot from close behind {him('outstretched arm in an old grey cloth sleeve')}, in the left foreground; on screen right Magistrate Hu, {HU}, walking up a few steps toward the gate and stopping, framed from the knees up with space above his head, his face three-quarter to screen left toward the young man, never the lens; the pleasant look dropping off his face: cheeks going slack, eyes narrowing coldly, mouth turning flat between words; behind him two yamen runners in Song-dynasty plain black round-collared robes and black caps, each holding one burning torch; {ONCE}; no blade anywhere",
         lines=[("huxianling", "許硯，有人告你許家私藏欽犯。", "收起笑，冷")],
         motion="Magistrate Hu walks a few steps closer in the torchlight and stops; his face goes cold and stays cold to the last frame",
         zh="過肩（許硯肩後拍胡縣令）、跟拍：前景左只有許硯張開的手臂與髮髻（不點名）；胡縣令在火把光裡走近幾步停下，笑收起來，冷冷地說；身後兩個衙役各拿一支火把"),
    dict(loc="road", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="torch",
         comp=f"over-the-shoulder medium shot from close behind one plump official's right shoulder: in the right foreground only the back of his black official gauze hat and his blue-green official robe shoulder, his face never in the frame, appearing only once; on screen left Xu Yan, {XU_NIGHT}, standing at his full height in the gateway with both arms still spread across it, framed from the waist up with space above his head, his face three-quarter to screen right toward the official, never the lens; unyielding: brows level, eyes steady, jaw set, lips moving firmly between words, no smile; behind him the dark yard; nobody else in the gateway",
         lines=[("xuyan", "欽犯？我家只有一個妹妹、三個剛過門的媳婦。", "不退")],
         motion=f"Xu Yan does not step back and keeps his arms out; he jerks his head once back toward the yard behind him; {NOSMILE}",
         zh="反打（胡縣令肩後拍許硯）、慢推：前景右只有胡縣令的官帽後腦與肩（不點名）；許硯不退、手臂沒放下，回頭朝院子一偏頭，不笑"),
    dict(loc="road_c", cam="Close-up, slow push in", chars=["huxianling"], night="torch",
         comp=f"close-up of Magistrate Hu, {HU}, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes sliding past the young man's shoulder off screen left toward the house beyond, never the lens; cold: the corners of his mouth pressing down, eyes narrowed, lips moving coldly between words; behind him only orange torchlight and darkness",
         lines=[("huxianling", "三個媳婦？本官今晚要的，只有一個。", "冷")],
         motion=f"Magistrate Hu's eyes slide past the shoulder toward the house; the corners of his mouth press down and his head and shoulders tip forward a little toward the gate, his whole head staying in the frame; {NOSMILE}",
         zh="近景、慢推：胡縣令眼睛越過許硯的肩往屋門看，嘴角往下一壓，頭肩往前一探（不寫 leans），冷冷地說"),
    dict(loc="road", cam="Low-angle over-the-shoulder shot, slow push in", chars=["xuyan", "aling"], night="torch",
         comp=f"low-angle over-the-shoulder shot: in the right foreground only one official's raised right arm in a wide blue-green official sleeve, its hand pointing past the gate, the rest of him outside the frame; in the middle Xu Yan, {XU_NIGHT}, standing in the gateway with his arms spread, his face three-quarter to screen right toward the official, never the lens; alarmed: brows snapping together, eyes wide, lips closed; far behind him, small and out of focus in the dark open house door across the yard, {ALING}, {SLEEVES}, lips closed; yamen runners in Song-dynasty plain black round-collared robes surging in from the right edge, each holding one burning torch; {TORCH}; no blade anywhere",
         lines=[("huxianling", "來人！拿下那個不說話的女人！", "一指，狠")],
         motion=f"the official's arm jabs toward the house; the runners with their torches surge toward the gate at a fast walk; far off in the doorway A-ling lifts her eyes; Xu Yan's lips stay closed; {NOSMILE}",
         zh="低角度過肩、慢推：前景右只有胡縣令抬起的官袍袖與右手（不點名、嘴不入鏡，台詞放錄音）往屋門一指；中間許硯擋在院門；遠處虛焦屋門內的阿令抬起眼睛；衙役舉著火把（每支一人）快走往院門湧（結尾，懸念接第 11 集）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e010-r2/script.md`（c01–c40 對應 s01–s40；含「這版改了什麼」與「2026-11-06 審稿後的修改」：c10「身上沒盤纏」、c22「就我們幾個人」、c27「看見火把往你家來」；c28 秦霜從村民手上拿一根木棍；火把約十六支、每支一人；錢員外與胡縣令只在 c34 以手同畫面）；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。",
    "- 內部工作編號 910（`hailuo/*-dh-e910.json`、`colab/runs/e910/`、`colab/runs/e910-live/`）；發布 slug `zhong-tian-qu-qi-e010-r2`。不放集數、不放片名卡；s01 接第 9 集 s38（門外地鋪，天亮）。",
    "- 第 9 集挑片與審片的教訓一開始就寫進來：過肩鏡前景的人一律不點名、不放進 chars、不送參考圖（第 9 集分身、s27/s28 側臉）；唐小棠兩句台詞（s23、s30）都從背後拍、nospeak 放錄音、spec.json 拿掉她三張臉部參考圖，整集不露嘴說話（她的聲音全集都是錄音，不會一鏡錄音一鏡原聲）；s36 不說話的她用第 7 集的中性外貌句。",
    "- 兵器：秦霜的柴刀不拍（extras.json 從造型句拿掉，腰帶寫「什麼都沒插」，每鏡寫畫面無兵器），s28 起右手一根木棍；阿令 s31 的匕首不拍、雙手空著縮進袖口；趙捕頭不寫佩刀；衙役家丁只有火把與木棍。舊傷只在 s06 插鏡出現、寫成發白的舊疤（不是紅的），之後每鏡寫「袖子蓋住手腕」。",
    "- 顏色寫死：地鋪是灰藍粗布、被子是深藍粗布同一色沒有滾邊（第 9 集鋪蓋變紫紅、米白、粉紅）；阿令包袱灰藍、帶子在右肩前打結；錢袋暗紅、沒有字；轎簾深藍素色。",
    "- 夜就是夜：院子與村路都寫「深夜、天全黑、沒有任何日光」，院子只有一盞燈籠、村路只有火把（第 9 集窗紙與院子亮得像白天）。主觀鏡（s18、s22）不點名、不送看的人的圖；s22 寫明牆頭前景沒有人。s26 稿子「上緣許硯爬下來的腿」拿掉（第 9 集門口多出的腿）。",
    "- 唐小棠：服裝用真人定妝照 `tangxiaotang-portrait-l1`（交領），不寫稿子 t2 高立領（真人版沒有 t2）；稿子夜裡外披的淡杏色外衣**沒寫**（背影描述與定妝照一致；要不要加由站主決定）。算盤寫成素木框、橫樑沒有雕花鑲嵌（第 9 集 s14 橫樑長出金色字形）。",
    "- 交領角色都不能水平翻轉：每鏡用畫左畫右寫死誰在哪；過肩鏡寫明從誰的哪一邊肩後拍。",
    "- 長鏡要買的秒數（BUY）：稿子長鏡清單 c03 買 10，c19、c21、c22、c27、c30、c32、c33、c36 買 8；其餘照第 8 集的估法（見 `r2.py` 的 BUY 註解）。還沒錄音，草稿用模型自己的聲音會在句中停頓，這是下限。",
]
FOOT = [
    "- **還沒有真人參考圖、pilot.py 會停的**（`live-action/screen-test-e010.py` 已寫好、**未執行**，等站主同意花錢）：",
    "  - 胡縣令定妝照 `huxianling-portrait-l1`（s35、s37、s39；新角色，CG 版有 t1，真人版沒有）。",
    "  - 院門外村路（夜）`set-xujia-menwai-l1`（s22、s32–s40；任何版本都沒有）。",
    "  - 許家走廊（晨）`set-xujia-zoulang-chen-l1`（s01–s06）：第 9 集的 `set-xujia-zoulang-l1` 是夜景、三扇門在右牆；本集是早上、阿令房門在左、屋門在右端。",
    "  - 許家院子（夜）`set-xujia-yuan-ye-l1`（s19–s31）：`set-xujia-yuan-l2` 是晴天白日、有黃色油菜花田，第 9 集 s01 夜戲用它，夜色偏亮、籬笆縫露出亮黃花田。",
    "  - `gen-dh.mjs` 的 SET 表已加這三個地點（地點詞：morning corridor of the Xu farmhouse／night yard of the Xu farmhouse／village road outside the Xu yard gate）；圖畫好後存成 `refs-live/<名字>-l1.png`，pilot.py 照檔名自動找到，不用改。",
    "- 白天的院子（s07–s18）用 `set-xujia-yuan-l2`。",
    "- `st1-ep.sh 910` 的 ref2manifest 要 `refs-dh/set-xujia-{menwai,zoulang-chen,yuan-ye}-t1.png`（CG 版永遠不會畫）：免費檢查用 `runpod/refs-dh-e910/`（refs-dh 的連結，三個佔位連結指到 CG 的 `set-xujia-wu-t1.png`），`REFS=… VIDEO_JSON=docs/videos/zhong-tian-qu-qi-e010-r2/video.json DRY=1`；佔位圖只在 CG 那一層，pilot.py 換真人圖時照檔名找 `-l1`，找不到就停。",
    "- 真人圖到了以後：`live-action/pilot.py <runpod>/a/st1 <runpod>/live/st1 s01 … s40` → `retake.py <runpod>/live/st1 <runpod>/live/d1 colab/runs/e910-live/spec.json` → colab-jobs.json 加 output_path → `preflight-prompts.py <runpod>/live/d1/retake.json`。",
    "- 有真人定妝照：許硯、阿令（沒戴鐵鐐；舊傷由 prompt 寫）、許小禾、秦霜、唐小棠（只有 l1 交領版）、王二牛、趙捕頭、錢員外。村民、衙役、家丁、轎夫不用參考圖，寫宋式衣著。",
    "- 本集沒有新的有聲配角：胡縣令用 `cast.json` 的 Iapetus（跟 CG 版第 10 集一樣）；村民、衙役、家丁、轎夫都不說話。",
    "- `cast.json` 的造型句：秦霜「柴刀插在腰帶」、二牛「empty-handed」由 `extras.json` 拿掉；小禾的草兔改成塞在腰帶上；胡縣令的官服由 `extras.json` 換成宋代寫法（跟 `screen-test-e010.py` 同一句）（黑紗幞頭、藍綠圓領七品官袍），「笑起來臉頰會抖」拿掉（只有 s35 寫假笑）。",
    "- 配樂：走廊與院子 warm（第 1 集屋內那首；s03 系統吐槽停一拍、s16 叮）、夜裡院子 tension（s22 火把一個重音、鼓點越來越密）、院門外低沉 suspense（s35 下轎、s40 大重音）；音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy. script.md 長鏡清單: c03 at 10; c19, c21, c22, c27, c30, c32, c33, c36 at 8. Not in the list, by
# e008's estimate (zh characters with punctuation stripped / 3.7 + 0.5 s, plus the shot's own action, against buy - 0.3 s at
# the cut's 1.1x): the lines of 14 characters or more with an action before or after them get 8 (s02 15 + getting up and
# striding round, s04 19 + the strap, s05 16 + the step, s06 17 recorded + the sleeve, s07 16 + the bowl and the run, s08 17 +
# the thumb, s09 16 + the hug, s10 15 recorded + the arms, s11 17 + squatting, s13 17 + the hand, s17 14 + the run and the
# turn, s23 16 recorded + the run, s24 19 + counting, s26 15 + the drop, s29 18 recorded + the sticks, s31 17 recorded + the
# nod and step back, s34 15 recorded + the hand-over, s35 15 + stepping out, s38 18), and so does s28 (13 + three actions:
# the shoulder, the point, taking the stick). The rest stay at gen-dh's 5 or 6 (s12 11, s15 12, s16 and s18 system lines,
# s20 11, s25 14 with a head turn only, s37 12, s39 14, s40 12). The live drafts speak with the model's own voice, which
# pauses mid-line (route-a.md 2026-11-07), so these are a floor; re-check against the recorded or drafted voice before stage 1.
BUY = {"s02": 8, "s03": 10, "s04": 8, "s05": 8, "s06": 8, "s07": 8, "s08": 8, "s09": 8, "s10": 8, "s11": 8, "s13": 8,
       "s17": 8, "s19": 8, "s21": 8, "s22": 8, "s23": 8, "s24": 8, "s26": 8, "s27": 8, "s28": 8, "s29": 8, "s30": 8,
       "s31": 8, "s32": 8, "s33": 8, "s34": 8, "s35": 8, "s36": 8, "s38": 8}
