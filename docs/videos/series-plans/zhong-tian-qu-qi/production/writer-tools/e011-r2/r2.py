"""Episode 11 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e011-r2/script.md
(c01-c35 = s01-s35; the CG-era r2 script of PR #2024, brought over from main 2026-11-14), including its sections
「這版改了什麼」, 「2026-11-06 審稿後的修改」 and 「真人版的改動（2026-11-14）」, which override the tables. Every line is the
script's, word for word; only the staging changes. Bible: production/r2-bible-e011-e020.md.

Live action from the first draft (owner 2026-11-11: 「之後都用真人版」), written the way e010-r2/r2.py wrote it, with the
lessons of e905-e910 (route-a.md, e909-live pick-review.md, the task file's 2026-11-12/11-14 notes):
- Over-the-shoulder shots: the foreground person is never named and is not in `chars`, so no picture of them is sent
  (e909 fix1/fix2: a second Tang Xiaotang or A-ling appeared whenever the foreground person's pictures went in). The
  foreground is "one young man / one plump official ... seen only from behind, appearing only once".
- Tang Xiaotang never speaks on camera (as e010): her two lines (c06 the certificates, c14 the statute) are shot from close
  behind her (TBACK), `nospeak`, the recording laid in; spec.json must drop her three face pictures and her identity
  sentence there (e908 fix1, e909 s09/s12, e910 s23/s30). Her silent face shots (c02, c23, c27, c29, c34) get e907's
  neutral face sentences in spec.json and a written frightened face here (she smiles otherwise). Costume: the live
  portrait (tangxiaotang-portrait-l1, cross-collared jacket wrapped shut), not the script's t2 high collar; the script's
  light apricot night outer jacket is left out, as e010. The abacus is e010's ABACUS (plain dark wood, no inlay).
- Qin Shuang: the script's 「柴刀插腰帶右邊」 is not shown (extras.json drops it, as e910): plain belt, NOBLADE in every shot
  of her. She holds e010's one plain wooden stick in her RIGHT hand throughout (e010 c28 took it from a villager).
- A-ling: no dagger is shown anywhere (e010 c31). The script's c01 「左袖口露出一點匕首的刃光」 and c04 「用拇指把刃口推回袖子」
  become: c01 both hands empty; c04 her left hand rises to the cuff of her right sleeve and stops there, then lowers - the
  viewer reads it with Xu Yan's off-screen line 「刀別出來」. Both long sleeves down over both wrists in every shot; the scar
  is not shown this episode.
- At most three named people on screen (Ref2VA holds three portraits). Changed against the script: c05 Qin Shuang and
  Tang Xiaotang are left out (they step aside off screen; c06 she comes from beside the fence); c06 Qin Shuang is left
  out; c11 Constable Zhao is left out (Magistrate Hu and the runners beyond the right edge); c23 Xu Yan's line is off
  screen and the three women are the picture (Wang Erniu's shoulder in the foreground unnamed); c34 only the three women
  (Xu Yan and the magistrate off screen right); c35 only Xu Yan and the magistrate (the three women behind are left out).
  Wang Erniu is never named: the eight villagers and he are stick tips behind the fence (e010 c29 put them there).
- Qian Yuanwai and Magistrate Hu never share a frame (r2 bible): c24 is the magistrate with one plump hand from the right
  edge, Qian's face never in the picture, as e010 c34.
- The certificates: three folded plain red paper certificates, only their plain red backs showing (CERTS); c18-c19 the
  open one is a blank red sheet with one empty square vermilion seal outline and no characters at all (e909: fake text
  on any paper; the original e011 drew a 囍 pattern in the seal).
- Night is night: deep night, sky black, the moon half hidden behind cloud (the live night-yard picture has a moon); the yard lit by one blank lantern under the eaves and the torches, every
  torch in one person's hand (e910: the window paper and the yard came out daylight-bright in e909).
- No blue glow and no panel written (e904 s03); c28 is his reaction only, the panel is an overlay.
- Nobody is flipped in the edit: everyone wears a cross collar or a crossed robe; sides are written as screen left/right.
State at the junction (e010 r2.py s36-s40): Xu Yan in the old grey outer coat over his robe, both hands empty, standing in
the open gateway with his arms spread; Qin Shuang (stick, right hand, tip down) and Tang Xiaotang (abacus) behind him in
the gateway; A-ling in the dark house doorway at the back left; about six runners went round the back of the house (s32);
Magistrate Hu outside the gate, the money pouch drawn into his sleeve (s34). Here: the pouch is in his LEFT sleeve.
Places: the night yard has its live picture (refs-live/set-xujia-yuan-ye-l1, drawn for e010; gen-dh's SET maps "night yard
of the Xu farmhouse" to it). Every person has a live portrait (huxianling-portrait-l1 drawn for e010). No new picture, no
new voice, no new SET or EN entry is needed for this episode.
"""
EP = 911  # internal working number; the published slug is zhong-tian-qu-qi-e011-r2
SLUG = "zhong-tian-qu-qi-e011-r2"
EP_TITLE = "名冊帶了嗎（重製版 r2）"
OUTLINE_SECONDS = 179  # script.md: 179 s, 35 shots (114.5 + 64.5)
TARGET_MINUTES = [3, 4]
TITLE = "名冊帶了嗎｜種田娶妻打天下 第11集（重製版）"
DESCRIPTION = "胡縣令一聲令下，從後門繞進屋的衙役抓住阿令的袖子往外拖。許硯喊住手，叫阿令別出手；唐小棠從懷裡掏出三份婚書。許硯舉著婚書問：名冊，您帶來了嗎？已入冊的妻，要拿人得有州府海捕文書。縣令說他就是王法，唐小棠當場背出戶婚律；縣令回頭問趙捕頭，趙捕頭支吾：那三份婚書，是他前天親手蓋的印。抓她，就是承認縣衙把欽犯配了婚。縣令慌了，喝令退後；錢員外在他耳邊出主意，縣令改口：人不抓，名冊送州府核查。系統警告：名冊一查，三人身分全曝光。縣令湊到許硯耳邊：交出她一個，名冊就不查。《種田娶妻打天下》第 11 集（重製版）。"
THUMB = ("名冊帶了嗎", "s19")
CHARACTERS = ["xuyan", "aling", "qinshuang", "tangxiaotang", "zhaobutou", "huxianling", "qianyuanwai", "xitong"]
MINOR = {}  # every speaker has a cast.json voice (Magistrate Hu: Iapetus, as e010); runners, servants and villagers are silent
MUSIC = "one cue per scene, continuing e010's last cue: a low dark suspense cue of low cello, deep drums and plucked strings in the torchlit yard at night, dropping out for one beat when the young man asks for the register and one heavy hit when the constable admits the seal, easing off as the magistrate waves his men back; then an even lower, quieter suspense cue of low drones and a slow heartbeat drum, one red warning hit under the system's warning, only the low drone left under the final whisper and one last soft hit; ancient Chinese rural drama, no vocals"

# Scene headers of script.md. Both scenes: the night yard of the Xu farmhouse (the yard wall with the yard gate on screen
# right, the house door at the back left, the bamboo fence along the left with the villagers crouched behind it, the
# round stone table in the middle, one blank lantern under the eaves). Officials come from screen right facing left; the
# Xu household is on the left facing right. Close shots use the short `_c` header. No person's name in a place phrase.
LOC = {
    "nyard": "In the night yard of the Xu farmhouse near midnight: the packed-earth yard, the packed-earth yard wall capped with grey roof tiles on screen right with the plain wooden yard gate standing open in it, the bamboo fence along the left, one round stone table in the middle, the house door at the back left with a woodpile beside it, the persimmon tree, the stone well with its wooden windlass at the front right, one blank paper lantern with no writing hanging under the eaves, nothing written on any board or wall; deep night, a pale moon half hidden behind cloud, the sky black, lit only by the warm glow of the one lantern and flickering orange torchlight, no daylight anywhere",
    "nyard_c": "In the night yard of the Xu farmhouse, deep night, the sky black, lit only by flickering orange torchlight and the glow of one blank paper lantern under the eaves",
    "door": "In the night yard of the Xu farmhouse, at the open house door at the back left: deep night, the sky black, the dark room inside the doorway lit only by the flicker of a torch held by someone out of sight inside, the yard lit by torchlight",
}
LIGHT = {
    "night": "the deep night, the flickering torchlight and the one lantern glow stay unchanged, the sky stays black",
}

# Repeated wording (each prop is one object; the descriptions say "one" where it first appears).
XU = "Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe"
CERTS = "three folded marriage certificates of plain red paper, folded shut, only their plain red backs showing, no writing visible"
OPEN_CERT = ("one open marriage certificate of plain red paper, the sheet blank with no characters and no writing anywhere on it, "
             "only one square vermilion seal outline near its lower right corner, the square empty inside with no character and "
             "no pattern in it")
ALING = "A-ling in her plain grey-white cotton dress with long sleeves and one plain wooden hairpin, no shackles"
SLEEVES = "her long sleeves down over both wrists, no wrist showing, both hands empty"
QIN = "her dark brown cross-collared short jacket, wide plain leather belt with nothing tucked in it, black trousers, leather boots and high ponytail tied with black cord"
STICK = "one plain straight wooden stick about as long as her arm in her right hand"
NOBLADE = "no blade, no knife, no sword, no scabbard and no weapon of any kind anywhere in the frame"
NOSHARP = "no blade, no knife, no sword and no spear anywhere in the frame, only torches and plain wooden sticks"
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
ABACUS = "one plain wooden abacus as long as her forearm, its frame and beam plain dark wood with no carving, no inlay, no marks and no writing"
TANG_FEAR = "frightened: face pale, eyes wide, lips pressed shut, no smile"
# e908 fix1 / e909 s09 / e910 s23: her back with no face pictures (spec.json drops them).
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with two looped buns tied with pink "
         "silk ribbons and pearl pins, two long pink silk ribbons hanging from the buns down over her shoulders, a pink inner "
         "collar at the nape of her neck and her light peach-pink silk shoulders; the back of her head toward us the whole time, "
         "her ear the furthest round her head we ever see, no cheek, no profile and no lips at any moment")
HIM_BACK = ("one young man seen only from behind, appearing only once: only his {what} and the back of his black topknot, his face "
            "never in the frame")
HU_BACK = ("one plump official seen only from behind, appearing only once: only the back of his black gauze futou hat and his "
           "blue-green official robe shoulder, his face never in the frame")
ZHAO = "in his black futou cap and plain black round-collared constable's robe, no sword written"
HU = "in his black official gauze hat and blue-green seventh-rank official robe"
RUNNERS = "yamen runners in ancient Chinese Song-dynasty plain black round-collared robes, black caps and cloth shoes"
TORCH = "every burning torch held in one person's hand, none floating, none stuck in the ground"
STICKTIPS = "a row of upright plain wooden stick tips poking up behind the bamboo fence"
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
ONCE = "each person appears only once, nobody else behind them"


def him(what):
    return HIM_BACK.format(what=what)


SHOTS = [
    # ---- scene 1: the night yard, the arrest (the gate on screen right, the house door at the back left).
    dict(chapter="抓人", loc="door", cam="Medium close-up, slow push in", chars=["aling"], night="night",
         comp=f"medium close-up past the dark wooden frame of the house door in the foreground, the shot opens directly on {ALING}, standing on the threshold inside the doorway, framed from the chest up with space above her head, {SLEEVES}, half her face lit by the far torchlight from the yard, her face three-quarter to screen right toward the yard gate, never the lens; startled and cold: eyes snapping wide, brows drawing together, lips pressed shut, no smile; out of the dark room behind her comes one hand in a plain black round-collared sleeve; {NOBLADE}",
         lines=[],
         motion=f"the black-sleeved hand shoots out of the dark room, grips the right sleeve of her dress and yanks it backward; A-ling is pulled half round toward the dark, her empty left hand hanging at her side; her lips stay closed; {NOSMILE}",
         zh="中近景、慢推、前景屋門門框（第一格就是阿令）：阿令站在門檻內，半邊臉被院子的火光照亮；黑公服袖的手從暗屋裡一把抓住她的右袖往後扯，她被扯得半轉身；兩手空著、袖子蓋住手腕、畫面無兵器（稿子的刃光不拍）"),
    dict(loc="nyard", cam="Medium shot, slow push in", chars=["xuyan", "qinshuang", "tangxiaotang"], night="night",
         comp=f"medium shot past the edge of the open plain wooden yard gate in the foreground on screen right: {XU}, standing in the gateway with both arms spread across it, framed from the knees up with space above his head, at first his back to us facing out to the road, then turning round; behind him inside the gate on screen left Qin Shuang, {QIN}, {STICK} with its tip down, her face three-quarter to screen left toward the house door, alert: brows drawn, eyes sharp, lips closed; beside her Tang Xiaotang {TANG}, holding {ABACUS} against her chest, her face three-quarter to screen left, {TANG_FEAR}; {NOBLADE}; {ONCE}",
         lines=[("xuyan", "住手！", "短喊，急")],
         motion=f"at a sound from the house Xu Yan whips round to face screen left, drops his arms and breaks into a run into the yard toward the house door; Qin Shuang and Tang Xiaotang turn their heads after him, their lips closed; {NOSMILE}",
         zh="中景、慢推、前景右院門門板：許硯張著雙臂擋在院門口，聽到屋門那邊的拉扯聲猛地回身，手臂放下往院子裡衝，張嘴喊；身後左邊秦霜（右手木棍、刀尖朝地、沒有刀）、唐小棠（定妝照交領、抱木算盤、臉發白）跟著回頭、嘴閉著；一鏡三人"),
    dict(loc="nyard", cam="Wide shot, tracking", chars=["xuyan", "aling"], night="night",
         comp=f"wide shot past a bamboo drying pole hung with one plain undyed cloth shirt in the foreground, everyone small in the frame: at the house door at the back left two {RUNNERS}, one gripping {ALING}'s right arm with his right hand and holding one burning torch in his left, the other pressing her right shoulder and holding one burning torch in his other hand, dragging her out over the threshold; {SLEEVES}; on screen right {XU}, running across the yard from the gate past the round stone table, his face three-quarter to screen left toward them, never the lens; furious: brows slammed down, eyes blazing, jaw set, mouth wide between words; {TORCH}; {NOBLADE}",
         lines=[("xuyan", "她是我許家的人，誰准你們進屋拿人！", "壓著火")],
         motion=f"Xu Yan runs past the stone table to the house door and clamps his right hand on the wrist of the runner gripping her arm, forcing it down; the runner lurches sideways and his torch swings; the runners' and A-ling's lips stay closed; {NOSMILE}",
         zh="全景、跟拍、前景晾衣竿上一件素色布衣：左後屋門口兩個衙役（各一支火把：一個左手火把、右手抓阿令右臂，一個按她右肩）把她拖出門檻；許硯從院門跑過石桌，右手扣住抓人的那隻手腕往下壓，衙役身子一歪、火把晃"),
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["aling"], night="night",
         comp=f"close-up of {ALING}, framed from the chest up with space above her head, her long sleeves down over both wrists, one black-sleeved hand gripping her right upper arm at the right edge of the frame; behind her only the dark doorway; her face three-quarter to screen right toward the young man off screen right, never the lens; cold and coiled: eyes narrowing, jaw tight, then her brows easing a little, lips closed the whole shot; {NOBLADE}",
         lines=[("xuyan", "阿令，刀別出來。妳一拔刀，他們就有理了。", "低，急")],
         motion=f"A-ling's empty left hand rises to the cuff of her right sleeve and stops there; her eyes go to the young man off screen right; then the hand lowers slowly back to her side, still empty; her lips stay closed; {NOSMILE}",
         zh="近景、慢推（身後只有屋門的暗處）：阿令右臂被畫右的黑袖手抓著；她空著的左手抬到右袖口停住，眼睛轉向畫右外的許硯，手又慢慢放下（匕首不拍，靠許硯畫外這句讓觀眾懂）；嘴閉著；許硯畫外（剪接放錄音）"),
    dict(loc="nyard", cam="Wide shot, dolly in", chars=["zhaobutou", "huxianling"], night="night",
         comp=f"wide shot past {STICKTIPS} in the foreground: through the open yard gate on screen right Constable Zhao, {ZHAO}, one burning torch in his right hand, stepping into the yard first, and behind him Magistrate Hu, {HU}, stepping over the threshold, his face three-quarter to screen left toward the house door, never the lens; arrogant: chin up, eyes narrowed, mouth wide between words; behind them about five {RUNNERS} coming in through the gate and about four more coming round the back of the house at the back left, each holding one burning torch, at walking pace; household servants in Song-dynasty black cross-collared short jackets and cloth head wraps crowding outside the gate; {TORCH}; {NOSHARP}",
         lines=[("huxianling", "許硯，你一個書生攔得住幾個？給我一併拿下！", "官腔，拉高")],
         motion=f"Magistrate Hu steps over the threshold and flings his right hand out toward the house door on screen left; the runners fan out along both sides of the yard at walking pace; Constable Zhao's lips stay closed; {NOSMILE}",
         zh="全景、推軌、前景籬笆後豎著的木棍尖（長鏡，買 8 秒）：趙捕頭（右手火把，不寫佩刀）先進院門，胡縣令（黑官帽、藍綠官袍）跨過門檻，右手往屋門一甩；約五個衙役從院門、約四個從屋後繞回來（每人一支火把）；家丁堵在院門外。live：稿子這鏡的秦霜、唐小棠拿掉（一鏡最多三人，她們讓到畫外籬笆邊）"),
    # Converted: Tang Xiaotang's line from behind her (her on-screen speaking shots are all from behind this episode).
    dict(loc="nyard", cam="Over-the-shoulder medium shot, tracking", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="night",
         comp=f"over-the-shoulder medium shot following from close behind {TBACK}, filling the left foreground, her left elbow pressing a plain wooden abacus against her side; on screen right {XU}, standing at his full height by the house door, framed from the waist up with clear space above his head, letting go of a runner's wrist and turning toward her, his face three-quarter to screen left toward her, never the lens; urgent: brows drawn, eyes on her hands, lips closed; {NOBLADE}; exactly two people in the frame, nobody else",
         lines=[("tangxiaotang", "婚書在這，三份都蓋了縣衙的印。", "快、壓低")],
         motion=f"the young woman hurries up to him from beside the fence, pulls one small oiled-paper packet, folded shut, out from inside her jacket with her right hand and holds it out to him, the back of her head still toward us; Xu Yan turns to her and holds out his open right hand; his lips stay closed; {NOSMILE}",
         zh="【改背後拍】過肩中景、跟拍：前景左只有唐小棠的後腦、雙丸子頭、兩條長粉緞帶、粉色內領、淡桃粉衣肩（臉與嘴不入鏡，左肘夾著算盤）；她從籬笆邊快步到許硯身邊，右手從衣襟裡掏出油紙包遞過去；畫右許硯鬆開衙役的手腕、轉身伸出右手，嘴閉著。台詞 nospeak，剪接放錄音；spec.json 拿掉她三張臉部參考圖。稿子的秦霜拿掉"),
    dict(loc="nyard_c", cam="Insert close-up, slow push in", chars=[], night="night", act=3,
         comp=f"insert close-up, the shot opens directly on one man's open right hand, palm up, in a faded blue-grey cuff under an old grey cloth sleeve, from its very first frame; one slender hand in a peach-pink silk sleeve lays {CERTS} into his palm; only the two hands, the sleeves and the red paper are in the frame, no face; flickering orange torchlight",
         lines=[],
         motion="the slender hand sets the three folded red certificates into the open palm and withdraws; the man's fingers close firmly round them; the paper stays folded shut, its plain red back toward us",
         zh="手部特寫、慢推（第一格就是許硯攤開的右手）：唐小棠的手（桃粉袖口）把三份摺起的紅紙婚書放進他掌心，他握緊；紙摺著、紙背朝鏡頭、看不到字（無台詞）"),
    dict(loc="nyard", cam="Low-angle over-the-shoulder shot, slow push in", chars=["xuyan", "aling"], night="night",
         comp=f"low-angle over-the-shoulder shot from close behind {HU_BACK}, in the right foreground; on screen left {XU}, standing at his full height in front of the house door, framed from the knees up with clear space above his head, {CERTS} in his right hand, his face three-quarter to screen right toward the official, never the lens; very steady: brows level, eyes hard on him, lips moving firmly between words, no smile; half a step behind him on screen left {ALING}, {SLEEVES}, her arms still held by two {RUNNERS}, her eyes on the back of his head, lips closed; {NOBLADE}",
         lines=[("xuyan", "大人，她是我的妻。名冊，您帶來了嗎？", "很穩")],
         motion=f"Xu Yan steps forward in front of A-ling and lifts the folded certificates in his right hand to his chest; A-ling's lips stay closed; {NOSMILE}",
         zh="低角度過肩（胡縣令右肩後）、慢推：前景右只有胡縣令的官帽後腦與肩（不點名、不送他的圖）；許硯往前跨一步擋到阿令前面，右手把三份摺起的婚書舉到胸前說話；身後半步阿令還被兩個衙役架著、看著他的後腦、嘴閉著"),
    # Magistrate Hu may sneer here (the script).
    dict(loc="nyard", cam="Over-the-shoulder medium shot, slow push in", chars=["huxianling"], night="night",
         comp=f"over-the-shoulder medium shot from close behind {him('old grey cloth shoulder, the folded red paper raised in his right hand')}, in the left foreground; on screen right Magistrate Hu, {HU}, framed from the knees up with space above his head, the torchlight striking up from under his chin, his face three-quarter to screen left toward the young man, never the lens; scornful: one corner of his mouth curling in a cold sneer, eyes narrowed, nostrils flaring between words; two {RUNNERS} behind him, each holding one burning torch; {NOSHARP}",
         lines=[("huxianling", "名冊？捉拿欽犯，還要什麼名冊！", "嗤笑")],
         motion="Magistrate Hu snorts and flings his wide sleeve out, pointing past the young man toward screen left",
         zh="反打（許硯肩後拍胡縣令）、慢推：前景左只有許硯的肩、髮髻與舉著的紅紙背面（不點名）；胡縣令嗤一聲、一甩寬袖往畫左指（本鏡可以冷笑）；身後兩個衙役各一支火把"),
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU}, framed from the chest up with space above his head, the edge of {CERTS} at the bottom of the frame in his right hand, his face three-quarter to screen right toward the official off screen right, never the lens; certain: brows level, eyes unblinking, lips moving clearly between words, no smile; behind him only the dark house doorway",
         lines=[("xuyan", "她入了配婚名冊，是官府親手配給我的妻。", "篤定")],
         motion=f"Xu Yan lifts the folded certificates a little higher, into the bottom of the frame; {NOSMILE}",
         zh="近景、慢推（身後只有屋門的暗處）：許硯把婚書往上一舉（畫面下緣），直視畫右說話，不笑"),
    dict(loc="nyard", cam="Low-angle wide shot, slow push in", chars=["xuyan", "aling"], night="night",
         comp=f"low-angle wide shot past the corner of the round stone table in the foreground: in the middle {XU}, holding {CERTS} up in his right hand, his face three-quarter to screen right toward the officials off screen right, never the lens; cold and deliberate: brows level, eyes hard, lips moving word by word, no smile; at the back left {ALING}, {SLEEVES}, held by two {RUNNERS}, lips closed; on screen right only the backs and torches of a line of {RUNNERS}, each holding one burning torch; {TORCH}; {NOBLADE}",
         lines=[("xuyan", "已入冊的妻，要拿人，得有州府海捕文書。", "一字一字")],
         motion=f"Xu Yan steps toward screen right holding the certificates up; the two nearest runners shrink back half a step; everyone else's lips stay closed; {NOSMILE}",
         zh="低角度全景、慢推、前景石桌桌角：許硯舉著婚書往右跨一步，前排兩個衙役被逼得往後縮半步；左後阿令被兩個衙役架著。live：稿子的胡縣令、趙捕頭不點名入鏡（一鏡最多三人），畫右只有衙役的背與火把"),
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["huxianling"], night="night",
         comp=f"close-up of Magistrate Hu, {HU}, framed from the chest up with space above his head, his face three-quarter to screen left toward the young man off screen left, never the lens; caught out: eyes widening, mouth pressed tight, a bead of sweat at his temple, no smile; behind him only flickering torchlight and darkness",
         lines=[("xuyan", "大人手上，有州府蓋了印的文書嗎？", "畫外，逼問")],
         motion=f"Magistrate Hu's right hand clamps over his bulging left sleeve and he swallows hard; his lips stay closed; {NOSMILE}",
         zh="近景、慢推（身後只有火把光）：胡縣令眼睛撐大、嘴抿住，右手按緊鼓起的左袖（錢袋在裡面），吞一口口水；嘴閉著；許硯畫外（剪接放錄音）"),
    dict(loc="nyard", cam="Medium shot, slow push in", chars=["huxianling", "zhaobutou"], night="night",
         comp=f"medium shot: Magistrate Hu, {HU}, in front, framed from the knees up with clear space above his head, his face three-quarter to screen left toward the young man off screen left, never the lens; flustered and blustering: cheeks quivering, eyes bulging, mouth wide between words, no smile; one step behind him on screen right Constable Zhao, {ZHAO}, one burning torch in his right hand, his face lowered, eyes on the ground, lips closed; {NOSHARP}",
         lines=[("huxianling", "胡說八道！本官就是王法，要什麼文書！", "惱羞，拔高")],
         motion=f"Magistrate Hu stamps one foot and jabs his forefinger toward screen left, his cheeks quivering; Constable Zhao lowers his head further; {NOSMILE}",
         zh="中景、慢推：胡縣令一跺腳、手指往畫左戳、臉頰肉在抖；身後一步趙捕頭（右手火把）低頭、嘴閉著"),
    # Converted: Tang Xiaotang's statute from behind her, the magistrate's face taking it.
    dict(loc="nyard", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "huxianling"], nospeak=["tangxiaotang"], night="night",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, filling the left foreground, a plain wooden abacus held against her chest out of sight; on screen right Magistrate Hu, {HU}, framed from the waist up with space above his head, his face three-quarter to screen left toward her, never the lens; thrown: eyes widening, mouth falling half open, brows jerking up, lips closed, no smile; {NOSHARP}; exactly two people in the frame, nobody else",
         lines=[("tangxiaotang", "戶婚律第十二條：已入冊者，非州府文書，不得拘拿。", "一個字都不卡")],
         motion=f"the young woman steps out to the front and lifts her chin, the back of her head still toward us; the magistrate leans back a little, his eyes going wide; his lips stay closed; {NOSMILE}",
         zh="【改背後拍】過肩中景、慢推：前景左只有唐小棠的後腦與肩（臉與嘴不入鏡，算盤抱在胸前看不到）；她走到前面、下巴一抬背出律條；畫右胡縣令眼睛撐大、嘴半張、嘴閉著。台詞 nospeak，剪接放錄音；spec.json 拿掉她三張臉部參考圖。稿子是唐小棠正面中景"),
    # Qin Shuang may give a small wry curl of the mouth here (the script).
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["qinshuang"], night="night",
         comp=f"close-up of Qin Shuang, {QIN}, framed from the chest up with space above her head, {STICK}, her face in profile toward screen left where the young woman beside her stands off screen, never the lens; dry: eyes sliding sideways, one corner of her mouth curling a little, lips moving low between words; behind her only the bamboo fence in the torchlight; {NOBLADE}",
         lines=[("qinshuang", "背得這麼熟，比縣衙裡的人還清楚。", "低聲")],
         motion="Qin Shuang glances sideways toward screen left and taps the wooden stick once into her left palm",
         zh="近景、慢推（身後只有籬笆）：秦霜斜眼看畫左外的唐小棠，木棍在左掌心敲一下，低聲說（本鏡可以嘴角一勾）；畫面無兵器"),
    dict(loc="nyard", cam="Medium shot, slow push in", chars=["huxianling", "zhaobutou"], night="night",
         comp=f"medium shot: Magistrate Hu, {HU}, on screen left, framed from the knees up with space above his head, turning to his right, his face in profile toward screen right toward the constable, never the lens; rattled: brows knotted, eyes darting, mouth moving low and fast between words, no smile; on screen right Constable Zhao, {ZHAO}, one burning torch in his right hand, his face three-quarter to screen left toward the magistrate, uneasy, lips closed; {NOSHARP}",
         lines=[("huxianling", "趙捕頭，大衡律裡，真有這一條？", "急，壓低")],
         motion=f"Magistrate Hu grabs Constable Zhao's left sleeve and hauls him close; Zhao stumbles half a step toward him, his torch swinging; Zhao's lips stay closed; {NOSMILE}",
         zh="中景、慢推：胡縣令轉身一把揪住趙捕頭的袖子拉到身邊壓低聲音問；趙捕頭被拉得歪半步、火把晃、嘴閉著"),
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["zhaobutou"], night="night",
         comp=f"close-up of Constable Zhao, {ZHAO}, framed from the chest up with space above his head, one burning torch in his right hand at the edge of the frame, his face three-quarter to screen left toward the magistrate, never the lens; cornered: eyes sliding away, brows pinched, lips moving hesitantly between words, no smile; behind him only torchlight and darkness",
         lines=[("zhaobutou", "有……而且那三份婚書，是小的前天親手蓋的印。", "支吾")],
         motion=f"Constable Zhao's eyes slide away and his left hand presses the iron ruler at his belt down; he stammers, then lowers his head; {NOSMILE}",
         zh="近景、慢推（身後只有火把光）：趙捕頭眼睛往旁邊躲，左手把腰間鐵尺往下按，支支吾吾；不寫佩刀"),
    dict(loc="nyard_c", cam="Insert close-up, slow push in", chars=[], night="night", act=3,
         comp=f"insert close-up, the shot opens directly on {OPEN_CERT} from its very first frame, held open by two hands in faded blue-grey cuffs; only the hands, the cuffs and the red paper are in the frame, no face; the torchlight shining through the back of the paper so the red glows",
         lines=[],
         motion="the two hands smooth the red sheet open and turn it toward us; the empty square seal outline catches the light; nothing is written on the sheet",
         zh="手部特寫、慢推（第一格就是婚書）：許硯兩手攤開一份紅紙婚書轉向鏡頭；紙上沒有字，右下角一方空的朱紅方印框（框裡不畫字、不畫囍）；火光從紙背透過來（無台詞）"),
    dict(loc="nyard", cam="Low-angle medium shot, slow push in", chars=["xuyan", "aling"], night="night",
         comp=f"low-angle medium shot: {XU}, holding {OPEN_CERT} high over his head in both hands, its face turned toward screen right, framed from the knees up with clear space above the paper, his face three-quarter to screen right toward the officials off screen right, never the lens; pressing: brows drawn down, eyes fixed, lips moving firmly between words, no smile; the torchlight through the paper casting a red glow on his face; behind him on screen left {ALING}, {SLEEVES}, lips closed; {NOBLADE}",
         lines=[("xuyan", "縣衙蓋印配的婚，大人現在說她是欽犯？", "逼問")],
         motion=f"Xu Yan raises the open certificate high in both hands and takes one step toward screen right; A-ling's lips stay closed; {NOSMILE}",
         zh="低角度中景、慢推：許硯兩手把攤開的婚書高舉過頭（印框朝畫右），往右走一步，紅光落在臉上；身後左邊阿令嘴閉著"),
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU}, framed from the chest up with space above his head, the edge of the open red certificate held up beside his face, its blank red back toward us, his face three-quarter to screen right toward the official off screen right, never the lens; slow and hard: eyes not blinking, brows level, lips moving slowly and clearly between words, no smile; behind him only the bamboo fence and torchlight",
         lines=[("xuyan", "抓她，就是承認縣衙把欽犯配了婚。州府先辦的是誰？", "慢、清楚")],
         motion=f"Xu Yan pushes the red certificate a little further toward screen right, his eyes never leaving the official; {NOSMILE}",
         zh="近景、慢推：許硯把婚書（紙背朝鏡頭）再往畫右推近一點，眼睛不眨，慢、清楚地說"),
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["huxianling"], night="night",
         comp=f"close-up of Magistrate Hu, {HU}, framed from the chest up with space above his head, a red glow from the paper on his face, his face three-quarter to screen left toward the young man off screen left, never the lens; panicking: eyes round, brows shooting up, mouth stammering between words, no smile; behind him only torchlight",
         lines=[("huxianling", "這、這是……本官也是被人蒙在鼓裡！", "結巴")],
         motion=f"Magistrate Hu takes half a step back, his whole head staying in the frame, his right hand clutching his bulging left sleeve; {NOSMILE}",
         zh="近景、慢推：胡縣令眼睛撐圓、往後退半步（頭一直在畫面裡），右手抓緊左袖，結結巴巴、不笑"),
    dict(loc="nyard", cam="Wide shot, slow push in", chars=["huxianling", "aling"], night="night",
         comp=f"wide shot past {STICKTIPS} in the foreground: on screen right Magistrate Hu, {HU}, among {RUNNERS}, each holding one burning torch, his face three-quarter to screen left toward the house door, never the lens; panicked: face slack with fright, eyes wide, mouth wide between words, his hat knocked a little askew, no smile; at the back left by the house door {ALING}, {SLEEVES}, held by two runners, lips closed; {TORCH}; {NOSHARP}",
         lines=[("huxianling", "都給我退後！人先別碰，聽見沒有！", "慌，揮袖")],
         motion=f"Magistrate Hu flaps both wide sleeves hard at the runners twice; the two runners let go of A-ling's arms and back away toward screen right; A-ling's lips stay closed; {NOSMILE}",
         zh="全景、慢推、前景籬笆後的木棍尖：胡縣令朝衙役兩隻寬袖用力連揮兩下、官帽歪了一點、臉慌；左後屋門前兩個衙役鬆開阿令、退到院子右邊"),
    dict(loc="nyard", cam="Medium shot, tracking", chars=["qinshuang", "tangxiaotang", "aling"], night="night",
         comp=f"medium shot past one burly young man's brown shoulder and upright wooden stick behind the bamboo fence in the left foreground, seen only from behind, appearing only once; at the house door: on screen left Qin Shuang, {QIN}, {STICK}, her left hand drawing Tang Xiaotang {TANG}, an abacus hugged to her chest, into place beside her in the middle; on screen right {ALING}, {SLEEVES}, walking in from screen right to stand at the right of the door; all three framed from the knees up with space above their heads, their faces three-quarter to screen right toward the young man off screen right, never the lens; Qin Shuang wary: brows drawn, lips closed; Tang Xiaotang {TANG_FEAR}; A-ling cool: eyes steady, lips closed; {NOBLADE}; exactly three women",
         lines=[("xuyan", "阿令，跟她們站在屋門口，誰叫都別動。", "回頭，低")],
         motion=f"A-ling rubs her right arm through her sleeve and walks to the right of the house door; Qin Shuang draws Tang Xiaotang into the middle; the three stand side by side; all lips stay closed; {NOSMILE}",
         zh="中景、跟拍、前景籬笆後一個壯漢的肩與木棍（二牛，不點名、不送圖）：屋門前秦霜（左，右手木棍）拉唐小棠（中，抱算盤、臉發白）站好，阿令（右）揉一下右臂走過來站定；三人嘴閉著。live：許硯這句改畫外（稿子他在畫面裡回頭，一鏡四人），剪接放錄音（結尾）"),
    # ---- scene 2: the same yard, the register (the three women at the house door: Qin left, Tang middle, A-ling right).
    dict(chapter="名冊", loc="nyard_c", cam="Close-up, slow push in", chars=["huxianling"], night="night",
         comp=f"close-up of Magistrate Hu, {HU}, framed from the chest up with space above his head, his face three-quarter to screen left, never the lens; scheming: eyes sliding sideways, then slowly brightening, brows lifting, lips closed; at the right edge of the frame only one plump hand with gold rings in a dark gold silk sleeve with roundel patterns, an ordinary natural skin tone, resting on his right shoulder, its owner outside the frame, no second face; behind him only torchlight and darkness",
         lines=[("qianyuanwai", "大人，人抓不了，就查她們三個的來歷。", "畫外，壓低")],
         motion=f"the plump hand settles on the magistrate's shoulder; Magistrate Hu tilts his ear toward screen right to listen, his eyes rolling once and lighting up; his lips stay closed",
         zh="近景、慢推（身後只有火把光）：胡縣令；畫右緣只有一隻胖手（金戒指、深金團花錦袍袖口、一般膚色）搭在他右肩，錢員外的臉不入鏡（兩人不同框）；他側耳聽、眼珠一轉亮起來、嘴閉著；錢員外畫外（剪接放錄音）"),
    # Magistrate Hu may put on a fake smile here (the script).
    dict(loc="nyard", cam="Medium close-up, slow push in", chars=["huxianling"], night="night",
         comp=f"medium close-up of Magistrate Hu, {HU}, framed from the waist up with clear space above his head, his face three-quarter to screen left toward the young man off screen left, never the lens; smug again: chin raised, eyes half closed, a fake official smile with his plump cheeks quivering between words; behind him two {RUNNERS}, each holding one burning torch; {NOSHARP}",
         lines=[("huxianling", "好，人本官不抓。那就送州府，核查名冊！", "拖長音")],
         motion="Magistrate Hu straightens his hat with both hands, his whole head staying in the frame, flicks one wide sleeve and lifts his chin",
         zh="中近景、慢推：胡縣令雙手扶正官帽、一甩寬袖、抬下巴，拖長音（本鏡可以假笑）"),
    dict(loc="nyard", cam="Medium shot, tracking", chars=["huxianling"], night="night",
         comp=f"medium shot: Magistrate Hu, {HU}, framed from the knees up with clear space above his head, walking two steps toward screen left; at the left edge only {him('old grey cloth shoulder')}; the magistrate's face three-quarter to screen left past that shoulder toward the house door, never the lens; sly: eyes narrowed, mouth twisting between words, no smile; {NOSHARP}",
         lines=[("huxianling", "冒名頂替騙婚，那是你許家的罪，算不到本官頭上。", "陰")],
         motion=f"Magistrate Hu walks two steps closer and jabs a finger past the shoulder at the edge toward the house door, once, twice; {NOSMILE}",
         zh="中景、跟拍：胡縣令往前走兩步，手指越過畫左緣許硯的肩（不點名）往屋門前一點一點，陰陰地說"),
    dict(loc="nyard", cam="Medium shot, slow push in", chars=["qinshuang", "tangxiaotang"], night="night",
         comp=f"medium shot past one blank paper lantern with no writing hanging under the eaves in the foreground: at the house door on screen left Qin Shuang, {QIN}, {STICK}, and in the middle Tang Xiaotang {TANG}, her fingers on {ABACUS} held against her chest, both framed from the knees up with space above their heads, their faces three-quarter to screen right toward the yard, never the lens; at the right edge only one young woman's grey-white cotton shoulder, appearing only once; Tang Xiaotang {TANG_FEAR}; Qin Shuang shaken: eyes dropping, jaw tight, lips closed, no smile; {NOBLADE}",
         lines=[],
         motion=f"Tang Xiaotang's fingers freeze on the abacus beads and the colour drains from her face; Qin Shuang's knuckles whiten on the stick and her eyes drop to the ground; both lips stay closed; {NOSMILE}",
         zh="中景、慢推、前景屋簷下空白燈籠：屋門前秦霜（左）、唐小棠（中）；畫右緣只有阿令的肩（不點名）；唐小棠手指僵在算珠上、臉一下白了；秦霜握棍的指節發白、眼睛往下垂；都不笑、嘴閉著（無台詞）"),
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU}, framed from the chest up with space above his head, his face three-quarter to screen right, never the lens; first stunned: brows knitting, eyes flicking toward the house door on screen left and back; later his jaw clenching once and his eyes hardening, lips closed the whole shot; behind him only the bamboo fence in the torchlight",
         lines=[("xitong", "警告：名冊一查，三人身分全曝光。", "冷，警告"),
                ("xuyan", "三個人都有事？我娶進門的，到底是誰？", "心裡話，嘴閉著，沉", "inner"),
                ("xitong", "宿主現在才問，晚了兩天。", "冷，嫌棄")],
         panel=[("警告：名冊一查，三人身分全曝光", "penalty")],
         motion=f"Xu Yan's brows knit; his eyes flick toward screen left and come back; he stays silent and still, thinking; near the end he clenches his jaw once; his lips stay closed the whole shot; {NOSMILE}",
         zh="近景、慢推（長鏡，買 10 秒）：許硯眉頭一皺，眼睛往畫左屋門一偏又轉回來，最後咬一下牙；全程嘴閉著；系統（紅框面板）→ 心裡話 → 系統吐槽。不寫藍光、不寫面板（第 4 集 s03 畫出假字面板）"),
    dict(loc="nyard", cam="Point-of-view medium shot, slow push in", chars=["qinshuang", "tangxiaotang", "aling"], night="night",
         comp=f"point-of-view shot from the middle of the yard looking at the house door: three women standing side by side at the door, framed from the knees up with space above their heads: on screen left Qin Shuang, {QIN}, {STICK}; in the middle Tang Xiaotang {TANG}, holding {ABACUS}; on screen right {ALING}, {SLEEVES}; their faces three-quarter to screen right, eyes just past the lens, never into it; Qin Shuang guarded, Tang Xiaotang {TANG_FEAR}, A-ling still, lips closed; nobody in the foreground, no hands at the edges; {NOBLADE}; exactly three women",
         lines=[("xuyan", "晚也得問。可今晚，先不能讓她們被帶走。", "心裡話，嘴閉著，沉", "inner")],
         motion=f"Tang Xiaotang pulls the abacus up tight against her chest with both arms and steps half a step back against the door frame; Qin Shuang turns her face half away; A-ling lowers her eyes; all lips stay closed; {NOSMILE}",
         zh="主觀（許硯看屋門前）、慢推：不送許硯的圖、前景沒有人；三人並排：左秦霜、中唐小棠（臉發白）、右阿令；唐小棠兩手把算盤抱緊、往後退半步靠到門框，秦霜把臉轉開一半，阿令垂眼；嘴閉著；許硯心裡話"),
    dict(loc="nyard", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="night",
         comp=f"over-the-shoulder medium shot from close behind {HU_BACK}, in the right foreground; on screen left {XU}, standing at his full height, framed from the waist up with clear space above his head, {CERTS} gripped in his right fist, his face three-quarter to screen right toward the official, never the lens; defiant: brows level, eyes hard, jaw set, lips moving firmly between words, no smile; behind him the dark yard; nobody else",
         lines=[("xuyan", "大人要查就查。婚書上那方印，州府一樣看得見。", "不退")],
         motion=f"Xu Yan steps forward and lifts his right fist with the folded certificates to his chest; {NOSMILE}",
         zh="過肩（胡縣令肩後拍許硯）、慢推：前景右只有胡縣令的官帽後腦與肩（不點名）；許硯往前一步，把攥著婚書的右手抬到胸前說話，不笑"),
    # Magistrate Hu may put on an ingratiating smile here (the script).
    dict(loc="nyard", cam="Over-the-shoulder medium shot, tracking", chars=["huxianling"], night="night",
         comp=f"over-the-shoulder medium shot from close behind {him('old grey cloth shoulder and arm')}, in the left foreground; on screen right Magistrate Hu, {HU}, framed from the waist up with clear space above his head, his face three-quarter to screen left toward the young man, never the lens; oily: the anger smoothed off his face, a smile that does not reach his narrowed eyes, lips moving softly between words; behind him only torchlight; {NOSHARP}",
         lines=[("huxianling", "許秀才，何必兩敗俱傷？本官給你一條路。", "換成笑臉")],
         motion="Magistrate Hu's face changes to a smile; he walks one step closer and pats the young man's arm in the foreground twice with his plump hand",
         zh="反打（許硯肩後拍胡縣令）、跟拍：前景左只有許硯的肩與手臂（不點名）；胡縣令換一種笑，走近一步，用胖手拍拍他的手臂（本鏡可以陪笑）"),
    dict(loc="nyard", cam="Medium two-shot, slow push in", chars=["xuyan", "huxianling"], night="night",
         comp=f"medium two-shot, both framed from the waist up with clear space above their heads: on screen left {XU}, {CERTS} in his right hand, his face three-quarter to screen right, eyes fixed straight ahead past the official, never the lens; rigid: jaw set, brows low, lips closed; on screen right Magistrate Hu, {HU}, stepping in close beside him and bending a little toward his ear, one hand cupped by his mouth, his whole head staying in the frame, his face in profile toward the young man, never the lens; conspiratorial: eyes narrowed, lips moving low between words, no smile; {NOSHARP}; exactly two people",
         lines=[("huxianling", "名冊上那個不說話的，是本官要的人。", "耳語")],
         motion=f"Magistrate Hu steps in to the young man's side, cups one hand by his mouth and murmurs at his ear; Xu Yan does not turn his head and his lips stay closed; {NOSMILE}",
         zh="雙人中景、慢推：許硯（左，右手婚書）眼睛看前面、不轉頭、嘴閉著；胡縣令（右）湊到他耳邊、一手攏在嘴邊壓低聲音說（頭一直在畫面裡）"),
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["huxianling"], night="night",
         comp=f"close-up of Magistrate Hu, {HU}, framed from the chest up with space above his head, his face in profile toward screen left close to a young man's ear, and at the left edge only that young man's ear and temple with black hair, soft and out of focus, his face never in the frame, appearing only once; sly and cold: one eye narrowed, lips moving in a whisper between words, no smile; behind them only torchlight",
         lines=[("huxianling", "另外兩個，照樣是你的妻，本官不碰。", "耳語，陰")],
         motion=f"Magistrate Hu whispers; at the end his eyes slide once toward screen left, toward the house door; {NOSMILE}",
         zh="近景、慢推：胡縣令側臉湊在畫左緣虛焦的耳朵與鬢角旁（許硯，不點名）耳語，說完眼珠往屋門那邊一滑。稿子是大特寫（嘴與一隻眼），改近景"),
    dict(loc="nyard", cam="Medium shot, slow push in", chars=["qinshuang", "tangxiaotang", "aling"], night="night",
         comp=f"medium shot past {STICKTIPS} in the foreground: at the house door the three women side by side, framed from the knees up with space above their heads, their faces three-quarter to screen right toward the middle of the yard off screen right, never the lens: on screen left Qin Shuang, {QIN}, {STICK}; in the middle Tang Xiaotang {TANG}, holding {ABACUS}; on screen right {ALING}, {SLEEVES}; Qin Shuang tense: brows drawn, eyes hard; Tang Xiaotang {TANG_FEAR}; A-ling alert: eyes lifting, lips closed; {NOBLADE}; exactly three women",
         lines=[],
         motion=f"all three take half a step forward together and stop; Qin Shuang plants the stick tip on the ground, Tang Xiaotang presses the abacus to her chest, A-ling raises her eyes; all lips stay closed; {NOSMILE}",
         zh="中景、慢推、前景籬笆後的木棍尖：屋門前三人（左秦霜、中唐小棠、右阿令）一起往前半步又停住，秦霜木棍拄地、唐小棠算盤按在胸口、阿令抬起眼，看著畫右外的院子中間；都不笑、嘴閉著（無台詞）。稿子是全景連許硯與胡縣令（五人），改三人"),
    dict(loc="nyard", cam="Medium shot, slow push in", chars=["xuyan", "huxianling"], night="night",
         comp=f"medium shot past {CERTS} gripped in a man's right fist in the foreground: {XU}, framed from the chest up with space above his head, his face three-quarter to screen right, eyes fixed ahead, never the lens; holding it in: brows pressed down, eyes locked, jaw clenched, lips closed; bent at his ear on screen right Magistrate Hu, {HU}, his face in profile toward him, lips moving slowly in a whisper, no smile; behind them only the dark yard and torchlight; {NOSHARP}; exactly two people",
         lines=[("huxianling", "交出她一個，名冊就不查。", "耳語，慢")],
         motion=f"Magistrate Hu whispers the last words slowly at his ear; Xu Yan's right fist tightens on the certificates until his knuckles whiten, his eyes stay fixed; his lips stay closed; {NOSMILE}",
         zh="中景、慢推、前景是許硯右拳握著的三份婚書（紅紙背）：胡縣令在他耳邊慢慢說完；許硯指節發白、眼睛定住、眉頭壓下、嘴閉著（結尾，懸念接第 12 集「不換」）。稿子背景虛焦的三人拿掉（一鏡最多三人）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e011-r2/script.md`（c01–c35 對應 s01–s35；2026-11-06 的 r2 稿，2026-11-14 從 main 帶進來；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-14）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e011-e020.md`。",
    "- 內部工作編號 911（`hailuo/*-dh-e911.json`、`colab/runs/e911/`、`colab/runs/e911-live/`，都還沒建）；發布 slug `zhong-tian-qu-qi-e011-r2`。不放集數、不放片名卡；s01 接第 10 集 s40 同一刻（胡縣令一指之後，屋裡的衙役抓住阿令）。",
    "- 第 9、10 集的教訓一開始就寫進來：過肩鏡前景的人一律不點名、不放進 chars、不送參考圖；唐小棠兩句台詞（s06、s14）都從背後拍、nospeak 放錄音、spec.json 拿掉她三張臉部參考圖，整集不露嘴說話；她不說話的臉（s02、s23、s27、s29、s34）寫驚慌、用第 7 集的中性外貌句。",
    "- 一鏡最多三個有名字的人：稿子 s05、s11、s23、s34、s35 超過，改法見各鏡（s23 許硯改畫外）。錢員外與胡縣令只在 s24 以手同畫面。二牛不點名，只拍籬笆後的棍尖與一個壯漢的背。",
    "- 兵器：秦霜的柴刀不拍（extras.json 從造型句拿掉，同 e910），右手一根木棍；阿令的匕首整集不拍（稿子 s01 刃光、s04 推回袖裡改成左手停在右袖口、再放下），兩袖蓋住手腕；趙捕頭不寫佩刀；衙役家丁只有火把與木棍。",
    "- 紙上沒有字：三份婚書摺著、只露紅紙背；s18、s19 攤開的那份寫成空白紅紙、右下一方空的朱紅印框（原版第 11 集畫成「囍」字，第 9 集任何紙都長假字）。",
    "- 夜就是夜：深夜、天全黑、月亮半藏在雲後（真人夜院圖有月亮），院子只有屋簷下一盞空白燈籠與火把（每支一人）。s28 不寫藍光、不寫面板。",
    "- 交領角色都不能水平翻轉：每鏡用畫左畫右寫死誰在哪；過肩鏡寫明從誰的哪一邊肩後拍。",
    "- 長鏡要買的秒數（BUY）：稿子長鏡清單 s28 買 10；其餘照第 8 集的估法（見 `r2.py` 的 BUY 註解）。還沒錄音，草稿用模型自己的聲音會在句中停頓，這是下限。",
]
FOOT = [
    "- **參考圖都有了**（`assets/refs-live/`）：許硯、阿令、秦霜、唐小棠（l1 交領）、趙捕頭、胡縣令（`huxianling-portrait-l1`，第 10 集畫的）、錢員外（只拍手）；場景 `set-xujia-yuan-ye-l1`（第 10 集畫的夜院）。本集不用試鏡，pilot.py 不會停。",
    "- `gen-dh.mjs` 的 SET 表與 `build-r2.py` 的 EN 表都不用加：地點詞只有 night yard of the Xu farmhouse（第 10 集已登記）；說話的人都在 EN 表裡。",
    "- 開拍前要另外做（本稿不動共用檔）：`colab/runs/e911/extras.json`（照 e910：秦霜拿掉柴刀、胡縣令官服換宋代寫法、「笑起來臉頰會抖」拿掉、畫面不放字幕）；`colab/runs/e911-live/spec.json`（s06、s14 拿掉唐小棠三張臉部參考圖與身分句；s02、s23、s27、s29、s34 用中性外貌句）。",
    "- `st1-ep.sh 911` 的 ref2manifest 免費檢查：`REFS=… VIDEO_JSON=docs/videos/zhong-tian-qu-qi-e011-r2/video.json DRY=1`；夜院佔位用 `runpod/refs-dh-e910/` 的 `set-xujia-yuan-ye-t1` 連結（同第 10 集）。之後 `live-action/pilot.py <runpod>/a/st1 <runpod>/live/st1 s01 … s35` → `retake.py … colab/runs/e911-live/spec.json` → `preflight-prompts.py`。",
    "- 本集沒有新的有聲配角：胡縣令 Iapetus、趙捕頭、錢員外照 `cast.json`；衙役、家丁、村民都不說話。",
    "- 配樂：接第 10 集最後那首低沉 suspense（s08 停一拍、s17 一個重音、s22 收），第二場更低的 suspense（s28 紅框重音、s35 只留低音、最後一拍收）；音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy. script.md 長鏡清單: c28 at 10. The rest by e008's estimate (zh characters with punctuation
# stripped / 3.7 + 0.5 s, plus the shot's own action, against buy - 0.3 s at the cut's 1.1x): the lines of 14 characters
# or more, or 13 recorded with an action, get 8 (s03 15 + the run and the wrist, s04 16 recorded + the hand, s05 18 +
# stepping in, s06 13 recorded + the hand-over, s08 14 + the step, s10 17, s11 16 + the step, s12 14 recorded + the
# swallow, s13 15 + the stamp, s14 20 recorded, s15 14 + the tap, s17 18 + the ruler, s19 16 + the raise, s20 21, s22 13 +
# the two sleeve flaps and the runners backing off, s23 15 recorded + the walk, s24 15 recorded, s25 15 + the hat, s26 20 +
# the walk, s29 16 recorded, s30 19, s31 16 + the pat, s32 15 + stepping in, s33 14). The rest stay at gen-dh's 5 or 6 (s01
# and s27 action only, s02 the shout, s07 and s18 inserts, s09 12, s16 12, s21 13, s34 action only, s35 10). The live
# drafts speak with the model's own voice, which pauses mid-line (route-a.md 2026-11-07), so these are a floor; re-check against the recorded or drafted voice before stage 1.
BUY = {"s03": 8, "s04": 8, "s05": 8, "s06": 8, "s08": 8, "s10": 8, "s11": 8, "s12": 8, "s13": 8, "s14": 8, "s15": 8,
       "s17": 8, "s19": 8, "s20": 8, "s22": 8, "s23": 8, "s24": 8, "s25": 8, "s26": 8, "s28": 10, "s29": 8, "s30": 8,
       "s31": 8, "s32": 8, "s33": 8}
