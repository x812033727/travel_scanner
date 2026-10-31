NUM = 48
TITLE = "爹還活著"
TARGET_MINUTES = [1, 2]
YT_TITLE = "他把魏家銀票收進袖子，老兵深夜來報：她爹還活著｜種田娶妻打天下 第48集"
THUMB = ("將軍\n還活著", "s17")
CHARS = ["xuyan", "chuzhifu", "tangxiaotang", "dutie", "qinshuang", "xudalang", "weiguanjia", "xitong"]
MINOR = {
    "weiguanjia": {
        "id": "weiguanjia", "name": "魏家管家",
        "appearance": "East Asian man of fifty, plump and smooth-faced with heavy-lidded eyes and a thin trimmed moustache, a dark plum silk robe with a black satin collar and a black gauze cap, a string of dark sandalwood beads wound around one hand",
        "voice": {"provider": "gemini", "name": "Charon", "style": "標準國語，咬字清楚，台北人平常說話的語調；五十歲的魏家管家，男聲、低沉圓滑、居高臨下，從不提高聲音"},
    },
}

BACK = ("In the prefect's back hall in late afternoon light, a quiet side room with carved lattice windows, a low dark tea table "
        "with two celadon cups between two carved chairs, a folding screen painted with ink mountains, slanting golden light and "
        "floating dust")
YARD = ("In the back courtyard of the prefectural inn at night, a small stone-paved yard with a stone well, a thick red-lacquered "
        "wooden pillar holding up the eave of the guest-room gallery, warm lit paper windows along the gallery, a small wooden back "
        "gate in the far wall, a cold full moon over the tiled roofs")
ALLEY = ("In a narrow back alley of Qingzhou at night, damp grey brick walls close on both sides, one red paper lantern hanging from "
         "an eave, puddles on the flagstones, deep blue shadows")
NL = "the cold moonlight and deep blue night stay unchanged"

SHOTS = [
    # ---------------- 後堂
    dict(ch="後堂", tag="鉤子1／開頭", insert=True, act=2, cam="Insert of the money draft in his hands, locked", set=BACK, chars=[],
         prompt="insert of the low dark tea table between two celadon cups, two hands in faded blue-grey sleeves folding the oblong paper "
                "money draft with its square red seal, the draft already folded once",
         motion="the hands fold the draft in half again, press the crease flat with one thumb and lift it off the table",
         zh="接第 47 集：兩只青瓷杯之間的深色茶几，青灰袖子的兩隻手把蓋紅印的長方銀票對摺，已經摺過一次；再對摺一次，拇指把摺線壓平，拿離桌面"),
    dict(tag="鉤子1", cam="Medium close-up, locked", set=BACK, chars=["xuyan"],
         lines=[("xuyan", "只辦馮學正。", "平靜，做了決定")],
         prompt="medium close-up of Xu Yan standing by the tea table on screen left in the slanting golden light, the folded draft between "
                "two fingers, his face calm and decided, his eyes on Prefect Chu off screen right",
         motion="he holds the folded draft up between two fingers for a beat, his eyes steady on the Prefect",
         zh="許硯中近景在左、站在茶几旁，斜斜的金光裡，兩根手指夾著摺好的銀票，臉平靜、拿定了主意，看著畫外右邊的知府；銀票舉著停一拍，眼神穩"),
    dict(tag="鉤子1／反轉", cam="Medium close-up, slow push in", set=BACK, chars=["xuyan"],
         lines=[("xuyan", "這張，", "收進袖子"), ("xuyan", "我留著。", "嘴角一勾")],
         prompt="medium close-up of Xu Yan on screen left, the folded draft held at the opening of his left sleeve, a small sly smile at "
                "one corner of his mouth, his eyes on Prefect Chu off screen right",
         motion="he slides the folded draft deep into his left sleeve and pats the sleeve flat once with his right hand",
         zh="【反轉】許硯中近景在左，摺好的銀票停在左袖口，嘴角一邊勾起一個有點賊的小笑，看著畫外右邊的知府；把銀票塞進左袖深處，右手在袖子上拍平一下"),
    dict(cam="Medium close-up, locked", set=BACK, chars=["chuzhifu"],
         lines=[("chuzhifu", "年輕人，", "挑眉"), ("chuzhifu", "沉得住氣。", "難得一笑")],
         prompt="medium close-up of Prefect Chu seated in the carved chair by the tea table on screen right, one thick brow lifting, the "
                "faint start of a smile under his long black beard, his eyes on Xu Yan off screen left",
         motion="he sets his celadon cup down on the table without a sound and strokes his beard once, the smile staying small",
         zh="褚知府中近景在右、坐在茶几旁的雕花椅上，一邊濃眉挑起，長鬚下隱約一個笑，看著畫外左邊的許硯；把青瓷杯無聲放回桌上，捋一下鬍子，笑意很淡"),
    dict(cam="Close-up, locked", set=BACK, chars=["xuyan"],
         lines=[("xuyan", "大人，", "笑"), ("xuyan", "也是。", "拱手")],
         prompt="close-up of Xu Yan's face on screen left in the slanting golden light, a cheeky grin back, his eyes on Prefect Chu off screen right",
         motion="he cups his hands together in front of his chest and bows his head a little, still grinning",
         zh="許硯特寫在左、斜金光裡，回一個有點皮的笑，看著畫外右邊的知府；雙手在胸前一拱，頭微微一低，還在笑"),
    dict(cam="Medium shot, locked", set=BACK, chars=["chuzhifu"],
         lines=[("chuzhifu", "榜，", "起身"), ("chuzhifu", "已經送出去了。", "背過身")],
         prompt="medium shot of Prefect Chu rising from the carved chair on screen right, the ink-mountain screen behind him, his crimson "
                "robe catching the slanting light",
         motion="he rises with both hands on the chair arms and turns away toward the lattice window, his hands clasping behind his back",
         zh="褚知府中景在右、從雕花椅站起來，背後是水墨山水屏風，緋袍接住斜光；雙手撐椅扶手站起，轉身面向格窗，雙手背到身後"),
    dict(tag="鉤子2", cam="Close-up, slow push in", set=BACK, chars=["xuyan"],
         lines=[("chuzhifu", "改不改得回來，", "畫外，慢"), ("chuzhifu", "明天就知道。", "畫外")],
         prompt="close-up of Xu Yan's face on screen left in the slanting golden light, the smile fading, his brows drawing together, his "
                "eyes on Prefect Chu's back off screen right; Prefect Chu speaks off screen",
         motion="his hand closes over the sleeve that hides the draft and his jaw tightens, his eyes not leaving the Prefect's back",
         zh="許硯特寫在左，斜金光裡，笑慢慢收起來、眉頭皺起，看著畫外右邊知府的背影；知府在畫外說；手握住藏銀票的那隻袖子，下顎繃緊"),
    # ---------------- 院子
    dict(ch="院子", cam="Two-shot, locked", set=YARD, chars=["tangxiaotang", "xuyan"], night=NL,
         lines=[("tangxiaotang", "你沒告魏家？", "壓低聲音，急")],
         prompt="two-shot by the stone well, Tang Xiaotang on screen right in her fitted peach-pink silk ruqun with the high stand-up collar "
                "fastened at her throat, catching Xu Yan by the sleeve, Xu Yan on screen left just in from the gallery, a paper lantern "
                "glowing on the well rim",
         motion="she tugs his sleeve to pull him round to face her and leans up close, her eyes wide",
         zh="井邊雙人鏡：唐小棠在右，合身桃粉綢襦裙、高立領扣到喉頭，一把拉住剛從迴廊走進院子的許硯的袖子，許硯在左，井沿上一盞紙燈籠；她扯他袖子把人拉過來面對自己，湊近，眼睛睜大"),
    dict(cam="Medium close-up, locked", set=YARD, chars=["xuyan"], night=NL,
         lines=[("xuyan", "現在告，", "壓低聲音"), ("xuyan", "拖死的是我們。", "冷靜")],
         prompt="medium close-up of Xu Yan by the stone well on screen left, lantern light warm on one side of his face, moonlight cool on "
                "the other, his left sleeve lifted a little between them, his eyes on Tang Xiaotang off screen right",
         motion="he taps two fingers on the sleeve where the draft is hidden and shakes his head once",
         zh="許硯中近景在左、井邊，燈籠的暖光照一邊臉、月光冷冷照另一邊，左袖在兩人之間微微抬起，看著畫外右邊的唐小棠；兩根手指在藏銀票的袖子上點兩下，搖一下頭"),
    dict(cam="Close-up, slow push in", set=YARD, chars=["xuyan"], night=NL,
         lines=[("xuyan", "這張紙，", "慢"), ("xuyan", "留到最值錢的時候。", "笑了")],
         prompt="close-up of Xu Yan's face on screen left in the lantern light, a slow knowing smile spreading, his eyes on Tang Xiaotang off "
                "screen right",
         motion="he leans in a little toward her and lifts one eyebrow, the smile widening",
         zh="許硯特寫在左、燈籠光裡，一個慢慢展開、心裡有數的笑，看著畫外右邊的唐小棠；身子往她那邊探一點，挑一邊眉，笑得更開"),
    dict(cam="Close-up, locked", set=YARD, chars=["tangxiaotang"], night=NL,
         lines=[("tangxiaotang", "本錢不花，", "眼睛一亮"), ("tangxiaotang", "利滾利。", "笑得很甜")],
         prompt="close-up of Tang Xiaotang's face on screen right in the warm lantern light, her high stand-up collar fastened at her throat, "
                "her big round eyes lighting up, her dimples deepening in a delighted grin, her eyes on Xu Yan off screen left",
         motion="she tilts her head and her grin spreads wide",
         zh="唐小棠特寫在右、暖暖的燈籠光裡，高立領扣到喉頭，大圓眼一亮，酒窩一深、笑開了，看著畫外左邊的許硯；頭一歪，笑得更開，髮髻上的珍珠簪一閃"),
    dict(cam="Medium close-up, locked", set=YARD, chars=["tangxiaotang"], night=NL,
         lines=[("tangxiaotang", "不過，", "眼珠一轉"), ("tangxiaotang", "利息分我三成。", "伸出三根手指")],
         prompt="medium close-up of Tang Xiaotang by the stone well on screen right in the lantern light, her high stand-up collar fastened "
                "at her throat, three fingers held up between them, a sly sweet smile, her eyes on Xu Yan off screen left",
         motion="she wiggles the three raised fingers at him and lifts her chin",
         zh="唐小棠中近景在右、井邊燈籠光裡，高立領扣到喉頭，在兩人之間舉起三根手指，笑得又甜又精，看著畫外左邊的許硯；三根手指朝他晃一晃，下巴一抬"),
    dict(insert=True, act=1, cam="Insert of the gold abacus at her waist, locked", set=YARD, chars=[], night=NL,
         prompt="insert of a small gold abacus hanging at a waist in peach-pink silk brocade, a slim hand with a pink silk cuff resting on it "
                "in the lantern light",
         motion="one fingertip flicks a single gold bead across the rod with a quick snap",
         zh="插鏡：桃粉綢緞腰間掛的小金算盤，粉色綢袖的纖手搭在上面、燈籠光裡；一根指尖把一顆金珠「啪」地撥過去"),
    dict(cam="Two-shot, slow push in", set=YARD, chars=["tangxiaotang", "xuyan"], night=NL,
         lines=[("xitong", "唐小棠好感，", "平板電子音，叮一聲"), ("xitong", "五十二。", "平板電子音")],
         prompt="two-shot by the stone well, Tang Xiaotang on screen right with her high stand-up collar fastened at her throat, bumping her "
                "shoulder against Xu Yan's arm with a pleased smile, Xu Yan on screen left, his eyes lifting to a point in the empty air in "
                "front of him; the system voice speaks off screen",
         motion="she bumps his arm with her shoulder and he sways a step, his eyes tracking slowly across the empty air as if reading",
         zh="井邊雙人鏡：唐小棠在右、高立領，得意地笑著用肩膀撞一下許硯的手臂，許硯在左，眼睛抬起看著面前的空中；她一撞，他晃一步，眼睛像讀字一樣慢慢掃過空中",
         ov=[("唐小棠 好感 +7 → 52", "affection")]),
    # ---------------- 敲門
    dict(ch="敲門", tag="鉤子3", insert=True, act=1, cam="Insert of the back gate, locked", set=YARD, chars=[], night=NL,
         prompt="insert of the small wooden back gate in the far wall of the yard, deep in shadow, a big sun-darkened weathered fist in a "
                "frayed padded army sleeve knocking on the planks",
         motion="the fist knocks three times hard on the planks and the gate shudders on its bar",
         zh="【鉤子3】插鏡：院子盡頭牆上的小木後門，在暗影裡，一隻曬黑粗糙的大拳頭、磨破的舊軍襖袖子，敲在門板上；用力敲三下，門在門閂上一震"),
    dict(act=3, cam="Wide shot, locked", set=YARD, chars=["qinshuang", "dutie", "xuyan"], night=NL,
         prompt="wide shot of the moonlit yard, Qin Shuang in her fitted dark brown short jacket and high ponytail pulling the back gate open "
                "on screen right, Du Tie standing in the gateway leaning on his wooden crutch, Xu Yan coming across the flagstones from "
                "screen left",
         motion="Qin Shuang slides the bar back and swings the gate open, and Du Tie limps one heavy step in over the threshold on his crutch",
         zh="月光下院子的全景：秦霜在右，合身深棕短褂、高馬尾，拉開後門，杜鐵拄著木拐站在門口，許硯從左邊穿過石板地走過來；秦霜抽開門閂把門拉開，杜鐵拄拐一步重重跨進門檻"),
    dict(cam="Medium close-up, locked", set=YARD, chars=["dutie"], night=NL,
         lines=[("dutie", "小將軍，", "壓低嗓子，喘"), ("dutie", "消息來了。", "粗啞")],
         prompt="medium close-up of Du Tie just inside the back gate on screen right, his weathered face sweaty from walking, his fierce tiger "
                "eyes bright, the crutch under his left arm, his eyes on Qin Shuang off screen left",
         motion="he takes a deep breath, shifts his weight onto the crutch and leans in toward her",
         zh="杜鐵中近景在右、剛進後門，風霜的臉上一層趕路的汗，虎目發亮，左腋下撐著拐杖，看著畫外左邊的秦霜；深吸一口氣，把重心移到拐杖上，往她湊近"),
    dict(cam="Close-up, locked", set=YARD, chars=["qinshuang"], night=NL,
         lines=[("qinshuang", "你說。", "聲音發緊")],
         prompt="close-up of Qin Shuang's face on screen left in the moonlight, her bold brows drawn tight, her almond eyes fixed hard on Du "
                "Tie off screen right, her lips pressed together",
         motion="her hand closes on the edge of the open gate and her knuckles whiten, her eyes not moving off him",
         zh="秦霜特寫在左、月光裡，劍眉擰緊，杏眼死盯著畫外右邊的杜鐵，嘴唇抿著；一隻手抓住開著的門邊，指節發白，眼睛一動不動"),
    dict(tag="中段鉤子", cam="Close-up, slow push in", set=YARD, chars=["dutie"], night=NL,
         lines=[("dutie", "將軍還活著，", "聲音發顫"), ("dutie", "在北疆鹽礦。", "一字一字")],
         prompt="close-up of Du Tie's weathered face on screen right, his tiger eyes wet and shining in the moonlight, his grizzled beard "
                "trembling, his eyes on Qin Shuang off screen left",
         motion="his chin trembles and he nods hard once, a tear running down his cheek",
         zh="【中段鉤子】杜鐵風霜的臉特寫在右，虎目在月光下濕亮，花白鬍子在抖，看著畫外左邊的秦霜；下巴發抖，用力點一下頭，一滴淚流進臉上的深紋"),
    dict(act=2, cam="Close-up, slow push in", set=YARD, chars=["qinshuang"], night=NL,
         prompt="close-up of Qin Shuang's face on screen left in the moonlight, her almond eyes going wide, her lips parting, her whole face "
                "frozen in disbelief, her eyes on Du Tie off screen right",
         motion="her breath catches, her eyes fill and she takes one stumbling half step back from the gate",
         zh="秦霜特寫在左、月光裡，杏眼一下睜大、嘴唇張開，整張臉愣住，看著畫外右邊的杜鐵；呼吸一停，眼眶一下滿了，踉蹌退半步"),
    dict(cam="Close-up, locked", set=YARD, chars=["qinshuang"], night=NL,
         lines=[("qinshuang", "誰……", "發抖"), ("qinshuang", "誰看見的？", "抓住他")],
         prompt="close-up of Qin Shuang's face on screen left in the moonlight, her wet almond eyes searching, her hand gripping Du Tie's "
                "padded sleeve at the frame edge, her eyes on Du Tie off screen right",
         motion="her grip tightens on the padded sleeve and she pulls it toward her",
         zh="秦霜特寫在左、月光裡，濕了的杏眼在找答案，一手抓住畫邊杜鐵的舊軍襖袖子，看著畫外右邊的杜鐵；手抓得更緊，把袖子往自己這邊扯"),
    dict(cam="Medium close-up, slow push in", set=YARD, chars=["dutie"], night=NL,
         lines=[("dutie", "我當年的伍長，", "粗啞"), ("dutie", "親眼看見。", "篤定")],
         prompt="medium close-up of Du Tie in the back gateway on screen right, leaning on his crutch, his free hand covering hers on his "
                "sleeve, his tiger eyes steady, his eyes on Qin Shuang off screen left",
         motion="he pats her hand twice with his big weathered palm and nods slowly",
         zh="杜鐵中近景在右、後門口拄著拐，空著的手蓋在她抓著袖子的手上，虎目很穩，看著畫外左邊的秦霜；大手在她手背上拍兩下，慢慢點頭"),
    dict(tag="爽點", cam="Wide shot, locked", set=YARD, chars=["dutie", "qinshuang", "xuyan"], night=NL,
         lines=[("dutie", "是許公子託我", "轉頭看許硯"), ("dutie", "去問的。", "粗啞")],
         prompt="wide shot of the moonlit yard, Du Tie leaning on his crutch in the back gateway on screen right, Qin Shuang standing frozen "
                "in the middle, Xu Yan a few steps behind her on screen left by the stone well",
         motion="Du Tie points past Qin Shuang at Xu Yan and she turns her head slowly to look back",
         zh="【爽點】月光下院子的全景：杜鐵在右、拄著拐站在後門口，秦霜愣在中間，許硯在她身後幾步、左邊井旁；杜鐵空著的手越過秦霜朝許硯一指，秦霜慢慢轉頭回望他"),
    dict(act=2, cam="Medium shot, slow pan left", set=YARD, chars=["qinshuang"], night=NL,
         prompt="medium shot of Qin Shuang in the moonlit yard, her high ponytail swinging, turning away from the back gate toward the red "
                "pillar of the gallery on screen left",
         motion="she spins on her heel and runs three long strides across the flagstones toward the red pillar, her ponytail whipping behind her",
         zh="秦霜中景、月光下的院子，高馬尾一甩，從後門轉身，面向左邊迴廊的紅柱；一個轉身，三大步跑過石板地衝向紅柱，馬尾在身後甩開"),
    # ---------------- 拳印
    dict(ch="拳印", tag="奇觀", act=2, cam="Medium shot, locked", set=YARD, chars=["qinshuang"], night=NL,
         prompt="medium shot of Qin Shuang at the thick red-lacquered pillar of the gallery, her right fist drawn back at her shoulder, her "
                "face turned to the pillar, her jaw clenched",
         motion="she drives her fist into the pillar with her whole body behind it, the wood cracking, then presses her forehead against "
                "the pillar beside her fist, her shoulders heaving without a sound",
         zh="【奇觀】秦霜中景、迴廊粗紅漆柱前，右拳收在肩後，臉對著柱子，咬緊牙；整個身子帶著一拳打進柱子，木頭裂開，然後額頭抵在拳頭旁邊的柱上，肩膀無聲地起伏"),
    dict(insert=True, act=2, cam="Insert of the fist mark in the pillar, slow push in", set=YARD, chars=[], night=NL,
         prompt="insert of the thick red-lacquered pillar in the moonlight, the lacquer cracked in a ring around a fist-shaped dent in the "
                "wood with small splinters standing up, a hand in a dark brown sleeve slowly sliding down the wood below it",
         motion="the hand slides slowly down the pillar beneath the dent and a flake of red lacquer drops away",
         zh="插鏡：月光下的粗紅漆柱，漆裂成一圈，中間是一個拳頭形的凹印，木刺翹起來，深棕袖子的手在凹印下面慢慢順著木頭滑下來；手慢慢滑下柱子，一片紅漆剝落"),
    dict(tag="奇觀", act=3, cam="Wide shot, slow push in", set=YARD, chars=["qinshuang", "xuyan"], night=NL,
         prompt="wide shot of the moonlit yard, Qin Shuang sitting on the flagstones at the foot of the red pillar on screen left with her "
                "knees drawn up and her face turned away, the fist dent in the pillar above her, Xu Yan walking slowly over from screen right",
         motion="Xu Yan walks over without a word, lowers himself down and sits beside her shoulder to shoulder with his back to the pillar",
         zh="【奇觀】月光下院子的全景：秦霜在左，抱膝坐在紅柱腳下的石板上，臉轉開，頭頂是柱上的拳印，許硯從右邊慢慢走過來；他一句話不說，慢慢坐下，跟她並肩背靠著柱子"),
    dict(insert=True, act=2, cam="Insert of the sugar in his palm, locked", set=YARD, chars=[], night=NL,
         prompt="insert of a man's open palm in a faded blue-grey sleeve held out in the moonlight, one small square lump of white sugar the "
                "size of a fingertip resting in the middle of it",
         motion="a hand in a dark brown sleeve reaches in slowly and picks the sugar lump up off his palm",
         zh="插鏡：月光下一隻攤開的手、青灰袖子，掌心正中一小塊指尖大的方白糖；深棕袖子的手慢慢伸進來，把糖從他掌心拿走"),
    dict(tag="顏值鏡頭", cam="Close-up, slow push in", set=YARD, chars=["qinshuang"], night=NL,
         lines=[("qinshuang", "三年了，", "哽住"), ("qinshuang", "我以為他……", "說不下去")],
         prompt="close-up of Qin Shuang's face on screen left in the moonlight, her head tipped back against the red pillar holding the tears "
                "in, her almond eyes wet and shining, her bold brows trembling",
         motion="she blinks hard and swallows, one tear sliding down to her jaw",
         zh="【顏值鏡頭】秦霜特寫在左、月光裡，仰頭靠著紅柱把眼淚忍住，杏眼濕亮，劍眉在抖；用力眨一下眼、嚥一下，一滴淚從眼角滑到下巴"),
    dict(cam="Medium close-up, locked", set=YARD, chars=["qinshuang"], night=NL,
         lines=[("qinshuang", "你就不會", "哽咽，瞪他"), ("qinshuang", "說句話？", "又氣又哭")],
         prompt="medium close-up of Qin Shuang sitting at the foot of the red pillar on screen left, the sugar lump between her fingers, "
                "glaring sideways through wet eyes at Xu Yan off screen right",
         motion="she jabs his arm with the back of her fist",
         zh="秦霜中近景在左、坐在紅柱腳下，指間捏著那塊糖，眼睛濕著斜瞪畫外右邊的許硯；用拳背戳一下他的手臂"),
    dict(act=2, cam="Close-up, slow push in", set=YARD, chars=["xuyan"], night=NL,
         prompt="close-up of Xu Yan's face on screen right in the moonlight, sitting against the red pillar, his eyes on Qin Shuang off "
                "screen left, lips remain closed",
         motion="he shakes his head once with a small gentle smile and nudges his chin toward the sugar in her hand",
         zh="許硯特寫在右、月光裡，背靠紅柱坐著，看著畫外左邊的秦霜，嘴閉著；笑著輕輕搖一下頭，下巴朝她手上的糖點一點"),
    dict(tag="顏值鏡頭", cam="Two-shot, locked", set=YARD, chars=["qinshuang", "xuyan"], night=NL,
         lines=[("qinshuang", "……甜的。", "哭著笑出來")],
         prompt="two-shot at the foot of the red pillar, Qin Shuang on screen left with the sugar lump in her mouth and wet shining eyes, Xu "
                "Yan on screen right sitting shoulder to shoulder with her, looking ahead at the moon, saying nothing",
         motion="she laughs through her tears and leans her shoulder against his",
         zh="【顏值鏡頭】紅柱腳下的雙人鏡：秦霜在左，嘴裡含著那塊糖、眼睛濕亮，許硯在右跟她並肩坐著，看著前面的月亮，一句話不說；她哭著笑出來，用手腕背擦一下眼睛，肩膀靠到他肩上"),
    dict(cam="Close-up, locked", set=YARD, chars=["xuyan"], night=NL,
         lines=[("xitong", "秦霜好感，", "平板電子音，叮一聲"), ("xitong", "五十五。", "平板電子音")],
         prompt="close-up of Xu Yan's face on screen right in the moonlight, his eyes lifting to a point in the empty air in front of him, a "
                "quiet small smile; the system voice speaks off screen",
         motion="his eyes track slowly across the empty air as if reading, then drop back to the moon, the smile staying quiet",
         zh="許硯特寫在右、月光裡，眼睛抬起看著面前的空中，一個安靜的小笑；眼睛像讀字一樣慢慢掃過空中，再落回月亮，笑還是很淡",
         ov=[("秦霜 好感 +3 → 55", "affection")]),
    # ---------------- 暗巷
    dict(ch="暗巷", tag="結尾", act=2, cam="Wide shot, locked", set=ALLEY, chars=["xudalang", "weiguanjia"], night=NL,
         prompt="wide shot down the alley, Xu Dalang in his old woven straw hat and blue cotton robe walking in from screen left, a plump "
                "steward in a dark plum silk robe waiting under the red lantern on screen right, winding sandalwood beads around his hand",
         motion="Xu Dalang hurries the last steps to the steward with a quick look back over his shoulder and bows low with his hands cupped",
         zh="【結尾】沿著暗巷拍的全景：許大郎戴舊草帽、藍布長衫，從左邊走進來，一個穿深紫綢袍的胖管家在右邊紅燈籠下等著，手上繞著檀木念珠；許大郎回頭看一眼，快步走完最後幾步，到管家面前彎腰拱手"),
    dict(tag="結尾", cam="Medium close-up, locked", set=ALLEY, chars=["xudalang"], night=NL,
         lines=[("xudalang", "那個姓秦的，", "壓低聲音，討好"), ("xudalang", "是秦烈山的女兒。", "笑著")],
         prompt="medium close-up of Xu Dalang bowing on screen left under the red lantern light, the old straw hat shading his eyes, a "
                "mild eager smile on his pale smooth face, his eyes on the steward off screen right",
         motion="he bows a little lower and rubs his cupped hands together, his smile staying fixed",
         zh="【結尾】許大郎中近景在左、紅燈籠光下彎著腰，舊草帽遮著眼睛，白淨的臉上一個殷勤的笑，看著畫外右邊的管家；腰再彎低一點，拱著的手搓兩下，笑容不動"),
    dict(tag="結尾", cam="Medium close-up, locked", set=ALLEY, chars=["weiguanjia"], night=NL,
         lines=[("weiguanjia", "消息準？", "慢條斯理")],
         prompt="medium close-up of the plump steward under the red lantern on screen right, in his dark plum silk robe and black gauze cap, "
                "his heavy-lidded eyes looking down at Xu Dalang off screen left, the sandalwood beads in his hand",
         motion="he slides one sandalwood bead along the string with his thumb, not hurrying",
         zh="【結尾】魏家管家中近景在右、紅燈籠下，深紫綢袍、黑紗帽，厚眼皮的眼睛往下看著畫外左邊的許大郎，手上掛著檀木念珠；拇指慢慢撥過一顆念珠，不急"),
    dict(tag="結尾", cam="Close-up, slow push in", set=ALLEY, chars=["xudalang"], night=NL,
         lines=[("xudalang", "我親耳聽見的。", "眼睛不看人")],
         prompt="close-up of Xu Dalang's face on screen left under the hat brim, his narrow eyes sliding sideways away from the steward, his "
                "smile pleasant and empty",
         motion="he gives a small quick nod and his eyes slide away down the dark alley",
         zh="【結尾】許大郎的臉特寫在左、帽簷下，細長的眼睛往旁邊滑開、不看管家，笑得和氣又空；很快點一下頭，眼睛滑向暗巷深處"),
    dict(tag="結尾", cam="Medium close-up, slow push in", set=ALLEY, chars=["weiguanjia"], night=NL,
         lines=[("weiguanjia", "魏府，", "低沉"), ("weiguanjia", "記你一功。", "居高臨下")],
         prompt="medium close-up of the plump steward on screen right under the red lantern, a thin satisfied smile under his trimmed "
                "moustache, one hand reaching into his plum silk sleeve, his eyes on Xu Dalang off screen left",
         motion="he draws a heavy blue silk pouch out of his sleeve and holds it out toward Xu Dalang",
         zh="【結尾】魏家管家中近景在右、紅燈籠下，修齊的鬍子下一個淡淡的滿意的笑，一手伸進紫綢袖子，看著畫外左邊的許大郎；從袖子裡掏出一個沉甸甸的藍綢錢袋，遞過去"),
    dict(tag="結尾", cam="Close-up, locked", set=ALLEY, chars=["weiguanjia"], night=NL,
         lines=[("weiguanjia", "秦家的丫頭，", "眯眼"), ("weiguanjia", "少爺會高興的。", "笑")],
         prompt="close-up of the plump steward's face on screen right under the red lantern, his heavy-lidded eyes narrowing to slits, a "
                "thin smile, his eyes on Xu Dalang off screen left",
         motion="his smile widens slowly and he lets the blue silk pouch swing once from his fingers",
         zh="【結尾】魏家管家的臉特寫在右、紅燈籠下，厚眼皮的眼睛瞇成一條縫，一個淡淡的笑，看著畫外左邊的許大郎；笑慢慢擴開，讓藍綢錢袋在指尖晃一下"),
    dict(tag="結尾", insert=True, act=2, cam="Insert of the silver pouch, locked", set=ALLEY, chars=[], night=NL,
         prompt="insert under the red lantern light, a plump hand with dark sandalwood beads wound around it pressing a heavy blue silk pouch "
                "of silver the size of a fist into an open hand in a blue cotton sleeve",
         motion="the pouch drops into the waiting palm with a heavy sag and the blue-sleeved fingers close tight around it",
         zh="【結尾】插鏡：紅燈籠光下，一隻纏著檀木念珠的胖手，把一個拳頭大、沉甸甸的藍綢銀袋塞進一隻藍布袖子的攤開的手；銀袋一沉落進掌心，藍袖子的手指緊緊收攏"),
    dict(tag="結尾", act=3, cam="Close-up, locked", set=ALLEY, chars=["xudalang"], night=NL,
         prompt="close-up of Xu Dalang's face on screen left under the old straw hat, the red lantern light on the weathered brim band and the "
                "one pale clean stripe where a cord was taken off, his narrow eyes lowered",
         motion="he tips the hat brim down over his eyes with two fingers and the corner of his mouth curls into a small private smile",
         zh="【結尾】最後一格：許大郎的臉特寫在左、舊草帽下，紅燈籠光照著舊帽簷上那一道拆掉繩子的淺色印子，細長的眼睛垂著；兩根手指把帽簷往下一壓，嘴角勾起一個只有自己知道的笑"),
]

MUSIC = ("a quiet back room of low strings as he folds the draft, a sly plucked pipa wink as it disappears into his sleeve, a slow "
         "uneasy cello under 'whether it can be changed back', then a warm lantern-lit yard of soft guqin and a comic abacus-like woodblock "
         "for the girl's 'interest on interest', a glassy chime for the affection, three heavy knocks and a held low drone at the back gate, "
         "a trembling erhu as the old soldier says the general is alive, a single hard drum hit for the fist in the pillar, then a hushed "
         "moonlit theme of breathy xiao and soft strings as they sit side by side and she laughs through her tears, a gentle chime, then a "
         "cold creeping low string and a muffled heartbeat drum in the dark alley, a dull clink for the silver, cut on the cousin's small "
         "smile, ancient Chinese drama, no vocals")

YT_DESC = ("州府後堂，褚知府給了許硯兩條路。許硯把那張蓋著魏家私印的銀票摺好收進袖子：「只辦馮學正，這張我留著。」"
           "知府難得一笑：「年輕人，沉得住氣。」可榜已經送出去了，改不改得回來，明天才知道。"
           "回到客棧院子，唐小棠急著問他為什麼不告魏家；許硯說現在告，拖死的是自己，這張紙要留到最值錢的時候。唐小棠撥了一下金算盤：「本錢不花，利滾利。」"
           "深夜，老兵杜鐵敲開後門：「將軍還活著，在北疆鹽礦。」——是許硯託他去問的。秦霜衝到院子一拳打在柱子上，木頭上留下一個拳印；"
           "許硯坐到她身邊，一句話都不說，只遞給她一塊白糖。同一個夜裡，暗巷的紅燈籠下，族兄許大郎對魏家管家彎下腰：「那個姓秦的，是秦烈山的女兒。」"
           "管家把一袋銀子塞進他手裡。《種田娶妻打天下》第 48 集。")


def SB_HEAD(total, st, du):
    def at(s):
        t = int(st[s]); return f"{t // 60}:{t % 60:02d}"
    end = f"{int(total) // 60}:{int(total) % 60:02d}"
    return [
        f"{len(SHOTS)} 個鏡頭、五段（後堂／院子／敲門／拳印／暗巷），估計約 {total:.0f} 秒（照 lint 估法；真人語速通常再長一成左右）；細綱 110 秒",
        "預算：片段 %d 支（靜圖 0 張），沒有「切素材」鏡。片段走路線 A（Colab H3 Ref2VA 三段式，沒有首格）；秒數見 `hailuo/clips-dh-e048.json`（`gen-dh.mjs` 算），首格清單只當參照圖清單" % len(SHOTS),
        f"開頭 10 秒：接第 47 集的最後一格，手把銀票對摺（0:00），「只辦馮學正」（{at('s02')}），收進袖子「這張，我留著」（{at('s03')}），知府「年輕人，沉得住氣」（{at('s04')}）；中段鉤子：杜鐵「將軍還活著，在北疆鹽礦」（{at('s19')}）；轉折：唐小棠看懂他的盤算（{at('s08')}–{at('s14')}）、秦霜一拳打在柱上、許硯遞糖（{at('s25')}–{at('s32')}）；結尾收在暗巷，許大郎告密、管家把銀袋塞進他手裡",
        f"鉤子：【鉤子1】s01–s06 0:00、【鉤子2】s07 {at('s07')}、【鉤子3】s15–s18 {at('s15')}、【鉤子4 中段】s19–s24 {at('s19')}、【鉤子5】s25–s27 {at('s25')}、【鉤子6】s28–s33 {at('s28')}、【結尾】s34–s41 {at('s34')}–{end}",
        "顏值鏡頭：s29 秦霜（仰頭靠著紅柱忍淚，月光照著濕亮的杏眼）、s32（嘴裡含著那塊糖，哭著笑出來）；是臉與表情，不停在身體",
        "爽點：前半 reversal（s01–s04 觀眾以為他要告魏家，他把銀票收進袖子留著）、中段 rescue（s19–s23 他託杜鐵找到了秦霜爹的下落）",
        "說話鏡頭：說話的人在畫面上的鏡頭，motion 第一句都是他說這句話、嘴唇下巴隨每個音節動；畫外台詞（s07 知府、s14 與 s33 系統）放在別人的反應鏡上，prompt 寫明 off screen",
        "H3 寫法：motion 寫軌跡、一鏡一事、沒有 camera 字；夜景 s08–s41 的 motion 都補 `the cold moonlight and deep blue night stay unchanged`；插鏡（s01、s13、s15、s26、s28、s40）motion 開頭寫 `The shot opens directly on this close insert from its very first frame`；道具寫大小（白糖指尖大、銀袋拳頭大）；畫外的人不寫局部身體；沒有血：拳印是木頭裂開、漆剝落",
        "光：s01–s07 後堂斜斜的午後金光；s08–s33 客棧院子的夜，月光加燈籠的暖光；s34–s41 暗巷的夜，一盞紅燈籠",
        "軸線：後堂知府在右、許硯在左；院子井在中間、迴廊紅柱在左、後門在右，唐小棠在許硯右邊，杜鐵從右邊後門進來、秦霜在左看他，坐在柱下時秦霜在左、許硯在右；暗巷許大郎從左邊進來、管家在右邊燈籠下",
    ]


SB_FOOT = [
    "場景參考：s01–s07 用 `dh-set-zhoufu-houtang-t1`（含 `prefect's back hall`）；s08–s33 用 `dh-set-zhou-kezhan-yuan-t1`（含 `back courtyard of the prefectural inn`，排在 `courtyard`、`prefectural inn` 前面）；s34–s41 用 `dh-set-xiaoxiang-t1`（含 `back alley`）。後堂與客棧院子兩張還沒畫（registry 🎨），暗巷有圖。",
    "道具：蓋紅印的銀票（s01–s03，之後在許硯左袖裡，s07、s09 手按著）；青瓷杯（s04）；井沿的紙燈籠（s08）；唐小棠的小金算盤（s13）；杜鐵的木拐（s16–s23）；紅柱上的拳印（s25–s27）；指尖大的方白糖（s28–s32，柳溪自家做的白糖）；管家的檀木念珠與拳頭大的藍綢銀袋（s34–s40）；許大郎舊草帽上拆掉繩子的印子（s41）。",
    "連戲：開場照第 47 集的結尾（手懸在銀票上方）接，s01 手落下把銀票摺起來。s06–s07 知府「榜已經送出去了，改不改得回來，明天就知道」是第 49 集的衝突（前一晚改過的榜到底有沒有改回來）。s16 杜鐵是第 44 集答應替許硯打聽秦將軍下落的老兵；s17 叫秦霜「小將軍」照第 44 集。s23 交代消息是許硯託人問的（秦霜好感的理由）。s25 打的是迴廊的柱子，第 49、50 集不再回到這個院子。s34–s41 許大郎告密的內容（秦霜的身分）是他在第 45 集樓梯轉角偷聽到的（s37「我親耳聽見的」）；管家就是第 47 集銀票私印的主人、魏少卿的管家。",
    "m05（原主是怎麼落水的）：只留第 42 集起的那個提示——s41 帽簷上拆掉繩子的淺色印子，拍印子、不說它是什麼；許大郎為什麼出賣他們（細綱的 question）全集不答，留到第二季。秦家玉佩（m11）不出現。",
    "系統面板不由模型畫：s14、s33 的好感在剪接時疊上（affection）。",
    "新的參照圖還沒畫：褚知府、杜鐵、許大郎的定妝照（`refs-dh/chuzhifu-portrait-t1.png`、`dutie-portrait-t1.png`、`xudalang-portrait-t1.png`）與兩張場景圖（`set-zhoufu-houtang-t1.png`、`set-zhou-kezhan-yuan-t1.png`）。魏家管家（weiguanjia）沒有定妝照，照 e042 的掌櫃只寫在 prompt 與 video.json。",
]


def BRIEF(st, du, total):
    def at(s):
        t = int(st[s]); return f"{t // 60}:{t % 60:02d}"
    end = f"{int(total) // 60}:{int(total) % 60:02d}"
    return f"""# 《種田娶妻打天下》第 48 集〈爹還活著〉

## 故事前提

第 47 集收在州府後堂：褚知府屏退左右，把蓋了魏家私印的銀票推到許硯面前——「告到魏家，案子送京城，三年不結」「只辦馮學正，你明天就是解元」，許硯的手懸在銀票上方。第 48 集從同一個畫面接下去：那隻手落下，把銀票對摺再對摺（s01），許硯抬頭：「只辦馮學正。」（s02）把銀票塞進左袖：「這張，」「我留著。」（s03，細綱的 hook，0:05 內回答了上一集的問題「扳倒魏家，還是先拿解元？」——先拿解元，底牌留著）。知府挑眉一笑：「年輕人，」「沉得住氣。」許硯拱手「大人，」「也是。」站起來背過身：「榜，」「已經送出去了。」「改不改得回來，」「明天就知道。」（留給第 49 集的懸念。）

夜裡客棧的後院，唐小棠一把拉住他的袖子：「你沒告魏家？」許硯點點藏銀票的袖子：「現在告，」「拖死的是我們。」「這張紙，」「留到最值錢的時候。」（細綱的衝突。）唐小棠眼睛一亮：「本錢不花，」「利滾利。」「不過，」「利息分我三成。」指尖撥過一顆金算珠（細綱的 turn 前半：唐小棠看懂了他的盤算）；系統：「唐小棠好感，」「五十二。」

後門被敲了三下。秦霜拉開門，老兵杜鐵拄著拐跨進來：「小將軍，」「消息來了。」秦霜「你說。」杜鐵的虎目濕了：「將軍還活著，」「在北疆鹽礦。」（{at('s19')}，細綱的 mid_hook。）秦霜愣住，抓住他的袖子「誰……」「誰看見的？」「我當年的伍長，」「親眼看見。」杜鐵指向許硯：「是許公子託我」「去問的。」（midpoint rescue：他替她找到了爹的下落。）秦霜轉身衝到迴廊的紅柱前，一拳打進柱子，木頭裂出一個拳印，額頭抵著柱子、肩膀無聲地起伏（細綱的奇觀）。她滑坐到柱腳，許硯走過去，一句話不說，坐在她旁邊，攤開手心——一塊指尖大的白糖。秦霜仰頭忍淚「三年了，」「我以為他……」（細綱的顏值鏡頭），斜瞪他「你就不會」「說句話？」，許硯只是笑著搖頭，朝她手上的糖點點下巴；她把糖含進嘴裡，哭著笑出來：「……甜的。」肩膀靠到他肩上；系統：「秦霜好感，」「五十五。」（細綱的 turn 後半。）

同一個夜裡，暗巷的紅燈籠下，許大郎回頭看一眼，快步走到一個胖管家面前彎腰：「那個姓秦的，」「是秦烈山的女兒。」管家撥著念珠：「消息準？」「我親耳聽見的。」「魏府，」「記你一功。」「秦家的丫頭，」「少爺會高興的。」一個拳頭大的藍綢銀袋落進許大郎手心；收在他用兩根手指把舊草帽往下一壓、帽簷上那道拆掉繩子的印子在燈籠光裡一閃、嘴角勾起的笑（細綱的 cliffhanger，reveal：「族兄為什麼要出賣他們？」；第 49 集從許大郎把銀袋塞進懷裡、抬頭看見紅榜從城牆頂滾下來接）。

本集細綱：`docs/videos/series-plans/zhong-tian-qu-qi/season-01.json` 第 48 集（110 秒，第一季第五章，調性權謀＋感人＋狗血，lead_arc wins）。hook 是許硯把銀票收進袖子「只辦馮學正」「這張我留著」（0:00–0:07，line）；mid_hook 是杜鐵深夜敲門「將軍還活著」「在北疆鹽礦」（{at('s15')}–{at('s20')}）；衝突是現在告魏家只會拖死自己、銀票留著總有一天要用（s06–s10）；turn 是唐小棠看懂他的盤算、撥一下算盤（s11–s13），與秦霜一拳打在柱上無聲地哭、許硯一句話不說只遞糖（s24–s32）；cliffhanger 是暗巷裡許大郎對魏家管家告密、管家把銀子塞進他手裡（s34–s41，reveal）。satisfaction：first_half reversal（s01–s04）、midpoint rescue（s19–s23）。general_payoffs 全部入鏡：唐小棠好感 52（s14，他沉得住氣，把籌碼留到最有用的時候）、秦霜好感 55（s33，他替她找到了爹的下落）、魏家的銀票成了許硯的底牌（s03、s10）。觀眾比許硯多知道一點（暗巷的告密），authoring.md：一集只選一種。

## 鉤子（站主 10-16：開場、結尾之外中段還要兩三個以上）

| 鉤子 | 鏡 | 約略時間 | 內容 |
| --- | --- | --- | --- |
| 【鉤子1】開場 | s01–s06 | 0:00–{at('s07')} | 銀票對摺，「只辦馮學正」「這張，我留著」，知府「年輕人，沉得住氣」「榜已經送出去了」 |
| 【鉤子2】 | s07 | {at('s07')}–{at('s08')} | 「改不改得回來，明天就知道」（榜改回來了沒有？） |
| 【鉤子3】 | s08–s14 | {at('s08')}–{at('s15')} | 「你沒告魏家？」「這張紙，留到最值錢的時候」「本錢不花，利滾利」，好感 52 |
| 【鉤子4】 | s15–s18 | {at('s15')}–{at('s19')} | 半夜三下敲門，杜鐵「小將軍，消息來了」（什麼消息？） |
| 【鉤子5】中段鉤子 | s19–s24 | {at('s19')}–{at('s25')} | 「將軍還活著，在北疆鹽礦」，「是許公子託我去問的」，秦霜轉身就跑 |
| 【鉤子6】 | s25–s33 | {at('s25')}–{at('s34')} | 一拳打進柱子，拳印；許硯坐下遞糖，「三年了，我以為他……」「……甜的」，好感 55 |
| 【結尾】 | s34–s41 | {at('s34')}–{end} | 暗巷，「那個姓秦的，是秦烈山的女兒」「魏府記你一功」，銀袋落進手心，帽簷的印子與笑（族兄為什麼要出賣他們？） |

## 角色

- 許硯（xuyan）：s02「只辦馮學正」；s03「這張，我留著」；s05「大人，也是」；s07 聽知府說榜（只拍臉）；s09「現在告，拖死的是我們」；s10「這張紙，留到最值錢的時候」；s14、s33 看好感面板；s27–s32 坐在秦霜旁邊遞糖，一句話不說（細綱；s31 被問「你就不會說句話？」也只是笑著搖頭）。
- 褚知府（chuzhifu）：s04「年輕人，沉得住氣」；s06「榜，已經送出去了」；s07 畫外「改不改得回來，明天就知道」。
- 唐小棠（tangxiaotang）：s08「你沒告魏家？」；s11「本錢不花，利滾利」；s12「不過，利息分我三成」；s13 撥金算珠；s14 用肩膀撞他。每個 prompt 都寫高立領。
- 杜鐵（dutie）：s15 敲門的拳頭；s16 拄拐進門；s17「小將軍，消息來了」；s19「將軍還活著，在北疆鹽礦」；s22「我當年的伍長，親眼看見」；s23「是許公子託我去問的」。左腿瘸、左腋下拄木拐（cast.json）。
- 秦霜（qinshuang）：s16 開門；s18「你說」；s20 愣住；s21「誰……誰看見的？」；s24 轉身跑；s25 一拳打在柱上；s27 坐在柱腳；s29「三年了，我以為他……」；s30「你就不會說句話？」；s32「……甜的」。本集在客棧裡，不戴斗笠。
- 許大郎（xudalang）：s34 走進暗巷彎腰；s35「那個姓秦的，是秦烈山的女兒」；s37「我親耳聽見的」；s40 接銀袋；s41 壓帽簷一笑（收尾）。
- 魏家管家（weiguanjia）：本集才有的配角，沒有定妝照，外貌只寫在 video.json 與 prompt（五十歲、胖、白淨、厚眼皮、修齊的小鬍子、深紫綢袍、黑紗帽、手上繞檀木念珠）；聲音 Charon（registry 的建議值：本集沒有馮學正）。s36「消息準？」；s38「魏府，記你一功」；s39「秦家的丫頭，少爺會高興的」（少爺是誰不點名）。
- 系統（xitong）：沒有身體，只有聲音與剪接時疊上的面板（`overlays.json`：s14 唐小棠好感、s33 秦霜好感）。

## 地點（固定的地點字）

- 州府後堂（午後）：`In the prefect's back hall in late afternoon light`（s01–s07，`dh-set-zhoufu-houtang-t1`，還沒畫；與第 47 集同一段字）。
- 州城客棧後院（夜）：`In the back courtyard of the prefectural inn at night`（s08–s33，新場景 `dh-set-zhou-kezhan-yuan-t1`，還沒畫）：石板小院、一口石井、撐著客房迴廊屋簷的粗紅漆木柱、迴廊上一排亮著暖光的紙窗、遠牆上一扇小木後門、屋瓦上一輪冷冷的滿月。
- 州城暗巷（夜）：`In a narrow back alley of Qingzhou at night`（s34–s41，沿用 `dh-set-xiaoxiang-t1`）：兩邊貼近的濕灰磚牆、屋簷下一盞紅紙燈籠、石板上的水窪、深藍的暗影。
- 站位（軸線）：見分鏡表開頭。

## 站主觀點

站主 2026-10-16 的要求：女生要火辣漂亮，濃顏系的五官與妝、合身剪裁；不露、不濕身、鏡頭不停在身體部位；每集至少一個顏值鏡頭；結尾收在最高點；不被黃標；每集開場、結尾之外中段再兩三個以上鉤子。本集的顏值鏡頭是 s29–s32（秦霜仰頭忍淚、含著糖哭著笑出來，月光照著濕亮的杏眼），拍的是臉與表情。唐小棠每一鏡都寫高立領。拳打在柱子上沒有血：只拍木頭裂開的拳印與剝落的漆（s25–s26）；秦霜的哭是無聲的。系統面板不由模型畫，s14、s33 只拍許硯看著空中的眼睛。銀票上沒有字（只有一方紅印）。

分鏡照 `storyboard-rules.md` 2026-10-28 起的 H3 寫法（與第 42 集同）：說話的人在畫面上時 motion 第一句寫他說這句話；motion 寫軌跡、一鏡一事；表情寫成正面的字；道具寫大小；畫外的人不寫局部身體；夜景補光線不變的句子；運鏡只在 `camera`；`locked` 就是鎖定；秒數由 `gen-dh.mjs` 決定。本集沒有靜圖、沒有切素材鏡。角色外觀照 `production/cast.json` 逐字照抄。
"""
