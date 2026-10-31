NUM = 49
TITLE = "放榜"
TARGET_MINUTES = [1, 3]
YT_TITLE = "紅榜從最後一名唸起，遲遲沒有他，最後兩字全街安靜｜種田娶妻打天下 第49集"
THUMB = ("解元\n許硯", "s25")
CHARS = ["xuyan", "tangxiaotang", "qinshuang", "zhouyuanwai", "xudalang", "baobang", "xitong"]
MINOR = {
    "baobang": {
        "id": "baobang", "name": "報榜人",
        "appearance": "East Asian man of forty, stout with a ruddy round face and a deep barrel chest, a black herald's robe trimmed in red and a black cap with a red tassel, a long thin bamboo pointer in one hand",
        "voice": {"provider": "gemini", "name": "Iapetus", "style": "標準國語，咬字清楚，台北人平常說話的語調；四十歲的報榜人，男聲、宏亮、像唱名一樣拖長每個名次和名字"},
    },
}

GATE = ("Below the great city gate of Qingzhou in bright morning light, the grey brick gatehouse towering above, a long red paper "
        "results scroll hanging down the gate wall from the battlements almost to the ground, a wooden herald's platform at its foot on "
        "screen right, a dense crowd of examinees and townsfolk packed shoulder to shoulder below")
STREET = ("On the main street of Qingzhou in bright noon light, shop banners and strings of red lanterns on both sides, the street "
          "packed with cheering townsfolk")
QS = "Qin Shuang with a wide woven bamboo douli hat pulled low over her eyes, only her clean-lined jaw and pressed red lips showing under the brim"

SHOTS = [
    # ---------------- 紅榜
    dict(ch="紅榜", tag="鉤子1／開頭", act=2, cam="Medium close-up, locked", set=GATE, chars=["xudalang"],
         prompt="medium close-up of Xu Dalang in the crowd on screen right, his old straw hat on his head, his hand pushing a heavy blue silk "
                "pouch the size of a fist into the front fold of his blue cotton robe, his narrow eyes darting left and right",
         motion="he tucks the pouch deep into his robe and pats it flat, then his head jerks up toward the top of the gate wall",
         zh="接第 48 集：許大郎中近景在右、擠在人群裡，戴舊草帽，手把拳頭大的藍綢銀袋塞進藍布長衫的前襟，細長的眼睛左右亂瞄；銀袋塞深、拍平，然後頭猛地抬起看城牆頂"),
    dict(tag="鉤子1／奇觀", act=2, cam="Wide shot, low angle, slow tilt down", set=GATE, chars=[],
         prompt="wide shot from a low angle up the grey brick gate wall, the long red paper scroll unrolling down from the battlements in one "
                "long fall, the packed crowd's raised faces and hands at the bottom of the frame",
         motion="the red scroll drops and unrolls down the wall with a heavy flap, swinging once and settling flat against the bricks as "
                "the crowd surges forward",
         zh="【鉤子1／奇觀】低角度沿著灰磚城牆往上拍的全景：長長的紅紙榜從城垛上一口氣滾下來，畫面下緣是擠滿的人群仰起的臉和手；紅榜「啪」地垂下、沿牆展開，晃一下貼平在磚上，人群往前湧（無台詞）"),
    dict(tag="鉤子1", cam="Medium close-up, low angle, locked", set=GATE, chars=["baobang"],
         lines=[("baobang", "第八十名——", "宏亮，拖長音"), ("baobang", "青州，陳大有！", "唱名")],
         prompt="medium close-up from a low angle of the herald standing on the wooden platform on screen right, in his red-trimmed black "
                "robe and tasselled cap, his ruddy round face lifted, the bamboo pointer raised to the bottom of the red scroll beside him",
         motion="he fills his barrel chest with air and taps the pointer on the lowest name on the scroll",
         zh="低角度：報榜人中近景在右、站在木台上，紅邊黑袍、紅纓帽，紅潤的圓臉仰起，竹竿舉到旁邊紅榜的最底下；吸飽一口氣，竹竿點在最下面那個名字上"),
    dict(cam="Wide shot, locked", set=GATE, chars=["xuyan", "tangxiaotang", "qinshuang"],
         lines=[("tangxiaotang", "從最後一名", "踮腳"), ("tangxiaotang", "唸起？", "急")],
         prompt=f"wide shot of the crowd below the gate, Xu Yan in his faded blue-grey robe on screen left, Tang Xiaotang in her fitted "
                f"peach-pink silk ruqun with the high stand-up collar fastened at her throat in the middle on tiptoe, {QS}, on screen right, "
                f"all three looking up toward the red scroll beyond the right edge of the frame",
         motion="Tang Xiaotang bounces up on her toes twice and grabs Xu Yan's sleeve with both hands",
         zh="城門下人群的全景：許硯在左，高領桃粉襦裙的唐小棠在中間踮腳，戴斗笠的秦霜在右，三人都抬頭看畫外右邊的紅榜；唐小棠踮兩下，雙手抓住許硯的袖子"),
    dict(cam="Close-up, locked", set=GATE, chars=["xuyan"],
         lines=[("xuyan", "八十個名字，", "故作輕鬆"), ("xuyan", "慢慢等。", "吞口水")],
         prompt="close-up of Xu Yan's face on screen left in the bright morning light, a relaxed smile pasted on, his eyes on the red scroll "
                "off screen right",
         motion="he swallows once and the smile stays a little too still, his eyes not leaving the scroll",
         zh="許硯特寫在左、早晨的亮光裡，臉上掛著一個硬撐的輕鬆笑，看著畫外右邊的紅榜；嚥一下口水，笑容僵得有點太穩，眼睛沒離開過紅榜"),
    # ---------------- 打賭
    dict(ch="打賭", tag="鉤子2", cam="Medium shot, slow pan right", set=GATE, chars=["zhouyuanwai"],
         lines=[("zhouyuanwai", "喲，", "拖長音"), ("zhouyuanwai", "許秀才也來看榜？", "假笑")],
         prompt="medium shot of Zhou Yuanwai squeezing through the crowd on screen right in his soy-brown longevity silk robe and black "
                "skullcap, the lidded porcelain teacup in one hand and the green jade thumb ring glinting, his small eyes on Xu Yan off "
                "screen left",
         motion="he shoulders two townsfolk aside and strolls up scraping the cup lid slowly over the rim",
         zh="周員外中景在右，醬色團壽綢袍、瓜皮小帽，從人群裡擠過來，一手端著蓋碗，碧玉扳指一閃，小眼睛看著畫外左邊的許硯；用肩膀頂開兩個路人，一邊慢慢刮著碗蓋一邊晃過來"),
    dict(tag="鉤子2", cam="Medium close-up, locked", set=GATE, chars=["zhouyuanwai"],
         lines=[("zhouyuanwai", "他要是中了，", "大聲，讓人都聽見"), ("zhouyuanwai", "我倒著走！", "拍胸")],
         prompt="medium close-up of Zhou Yuanwai on screen right, his long narrow face smug, his chin raised and his hooked nose in the air, "
                "his eyes on Xu Yan off screen left",
         motion="he slaps his chest with his free hand and turns his head to the crowd around him with a sneer",
         zh="周員外中近景在右，長臉一副得意，下巴抬高、鷹鉤鼻朝天，看著畫外左邊的許硯；空著的手拍一下胸口，轉頭對周圍的人冷笑"),
    dict(cam="Close-up, locked", set=GATE, chars=["xuyan"],
         lines=[("xuyan", "員外，", "笑嘻嘻"), ("xuyan", "鞋帶先綁緊。", "指他的鞋")],
         prompt="close-up of Xu Yan's face on screen left among the jostling townsfolk, one eyebrow cocked high and a cheeky lopsided grin "
                "showing his teeth, his hands tucked into his sleeves, his eyes on Zhou Yuanwai off screen right",
         motion="he points one finger down toward Zhou Yuanwai's feet and raises his eyebrows",
         zh="許硯特寫在左、擠來擠去的路人之間，一邊眉毛挑得老高、歪著嘴笑，雙手攏在袖子裡，看著畫外右邊的周員外；一根手指往下指周員外的腳，眉毛一挑"),
    dict(cam="Close-up, slow push in", set=GATE, chars=["tangxiaotang"],
         lines=[("tangxiaotang", "說好了，", "甜甜一笑"), ("tangxiaotang", "倒著走一條街。", "眨眼")],
         prompt="close-up of Tang Xiaotang's face in the middle of the frame, her high stand-up collar fastened at her throat, a sweet "
                "dangerous smile with dimples, her eyes on Zhou Yuanwai off screen right",
         motion="she holds up one finger and draws a long straight line in the air with it",
         zh="唐小棠特寫在中間，高立領扣到喉頭，一個甜得危險的酒窩笑，看著畫外右邊的周員外；舉起一根手指，在空中畫一條長長的直線"),
    dict(cam="Medium close-up, locked", set=GATE, chars=["qinshuang"],
         lines=[("qinshuang", "大家都聽見了。", "冷，嘴角一勾")],
         prompt=f"medium close-up of {QS}, on screen right in the crowd, her arms folded, townsfolk crowding behind her, her face turned "
                f"toward Zhou Yuanwai off screen right",
         motion="the corner of her red lips curls up and she tilts the douli brim up a finger's width with one knuckle",
         zh="戴斗笠的秦霜中近景在右、人群裡，斗笠壓低只露下巴和紅唇，雙手抱胸，身後擠著路人，臉朝畫外右邊的周員外；紅唇一邊勾起，用一個指節把斗笠帽簷頂高一指"),
    # ---------------- 劃掉
    dict(ch="劃掉", insert=True, act=2, cam="Insert of the red scroll, slow tilt up", set=GATE, chars=[],
         prompt="insert of the red paper results scroll on the gate wall, columns of faint black brush strokes in rows, the tip of a long "
                "thin bamboo pointer sliding up from row to row",
         motion="the pointer slides steadily up the scroll, tapping each row once as it passes",
         zh="插鏡：城牆上的紅紙榜，一行行淡淡的黑色毛筆畫（不寫字），一根細長竹竿的尖端一行一行往上滑；竹竿穩穩往上，每一行點一下"),
    dict(tag="鉤子3", act=3, cam="Wide shot, locked", set=GATE, chars=["xuyan"],
         prompt="wide shot below the gate, two runners in black pushing through the crowd toward a white paper notice pasted on the gate "
                "wall beside the red scroll on screen right, one with a big brush dripping red ink, Xu Yan in the crowd on screen left "
                "turning to watch them",
         motion="the crowd parts for the runners, the one with the brush steps up to the white notice, and Xu Yan turns his whole body to watch",
         zh="【鉤子3】城門下的全景：兩個黑衣衙役擠過人群，走向右邊紅榜旁貼在城牆上的一張白紙告示（考官榜），一個手上拿著滴紅墨的大筆，許硯在左邊人群裡轉身看；人群讓開，拿筆的那個走到白告示前，許硯整個人轉過去看"),
    dict(tag="爽點", insert=True, act=2, cam="Insert of the examiners' notice, locked", set=GATE, chars=[],
         prompt="insert of the white paper notice on the grey brick wall, columns of faint black brush strokes, a big brush in a black sleeve "
                "pressing down at the top of one column",
         motion="the brush drags one thick red line straight down through that whole column and lifts off, a red drip running from the end",
         zh="【爽點】插鏡：灰磚牆上的白紙告示，一列列淡淡的黑色毛筆畫，黑袖子的手拿大筆按在其中一列的頂端；大筆從上到下拖出一道粗粗的紅線劃掉整列，筆抬起，紅墨從尾端流下一滴"),
    dict(tag="爽點", cam="Close-up, locked", set=GATE, chars=["tangxiaotang"],
         lines=[("tangxiaotang", "劃的是……", "瞇眼看"), ("tangxiaotang", "馮學正！", "笑出來")],
         prompt="close-up of Tang Xiaotang's face on screen right, her high stand-up collar fastened at her throat, squinting hard toward "
                "the notice beyond the right edge of the frame, her round eyes going wide with glee",
         motion="she claps both hands over her mouth and bounces once on her toes",
         zh="【爽點】唐小棠特寫在右，高立領扣到喉頭，瞇眼使勁看畫外右邊的告示，圓眼一下睜大、樂了；雙手一捂嘴，原地蹦一下"),
    dict(cam="Medium close-up, locked", set=GATE, chars=["zhouyuanwai"],
         lines=[("zhouyuanwai", "劃、劃一個考官，", "笑僵了"), ("zhouyuanwai", "算什麼。", "嘴硬")],
         prompt="medium close-up of Zhou Yuanwai on screen right, his smug smile gone stiff, a bead of sweat on his long face, the lidded "
                "teacup rattling a little in his hand, his eyes darting toward the notice on the wall beyond the frame",
         motion="he lifts the teacup to his lips to hide his face and gulps, the lid clinking against the rim",
         zh="周員外中近景在右，得意的笑僵掉，長臉上一滴汗，手上的蓋碗微微發抖，眼睛飄向畫外右邊的告示；把蓋碗舉到嘴邊擋臉，猛喝一口，碗蓋碰得叮叮響"),
    dict(insert=True, act=1, cam="Insert of the rattling teacup, locked", set=GATE, chars=[],
         prompt="insert of a lidded porcelain teacup in a thin hand with a green jade thumb ring and a soy-brown silk cuff",
         motion="the hand jerks and the cup lid clatters against the rim, slopping a drop of tea over the edge",
         zh="插鏡：一隻戴碧玉扳指、醬色綢袖的瘦手端著蓋碗；手在抖，碗蓋碰著碗沿喀喀響"),
    dict(cam="Close-up, slow push in", set=GATE, chars=["xuyan"],
         lines=[("xuyan", "考官劃了，", "低聲"), ("xuyan", "那榜呢？", "笑收起來")],
         prompt="close-up of Xu Yan's face on screen left, the grin gone, his brows drawing together, his eyes lifting toward the top of the "
                "red scroll beyond the right edge of the frame",
         motion="his right hand moves to his left sleeve where the folded draft is hidden and grips it",
         zh="許硯特寫在左，笑收起來、眉頭皺起，眼睛往上看向畫面右邊外紅榜的頂端；手移到藏著銀票的左袖上，握緊"),
    # ---------------- 前三
    dict(ch="前三", cam="Medium close-up, low angle, locked", set=GATE, chars=["baobang"],
         lines=[("baobang", "第十名——", "拖長"), ("baobang", "州城，林世安！", "唱名")],
         prompt="medium close-up from a low angle of the herald on the wooden platform on screen right, the bamboo pointer climbing into the "
                "upper rows of the red scroll, his cap tassel swinging",
         motion="he slides the pointer up one more row and taps it hard",
         zh="低角度：報榜人中近景在右、木台上，竹竿爬到紅榜上半部，帽上的紅纓一晃；竹竿再往上滑一行，用力一點"),
    dict(cam="Medium close-up, low angle, slow push in", set=GATE, chars=["baobang"],
         lines=[("baobang", "第三名——", "更響"), ("baobang", "青州，李守正！", "唱名")],
         prompt="medium close-up from a low angle of the herald on the wooden platform on screen right, the bamboo pointer high up near the "
                "top of the red scroll, sweat shining on his ruddy face",
         motion="he stretches up on his toes to reach the pointer higher and taps it on the scroll",
         zh="低角度：報榜人中近景在右、木台上，竹竿已經舉到紅榜快到頂的地方，紅潤的臉上發亮的汗；踮腳把竹竿伸高，點在紅榜上"),
    dict(act=2, cam="Close-up, locked", set=GATE, chars=["tangxiaotang"],
         prompt="close-up of Tang Xiaotang's face on screen right, her high stand-up collar fastened at her throat, her eyes huge and fixed "
                "on the scroll off screen right, the tip of one finger caught between her teeth",
         motion="she bites down harder on her fingernail and rises up onto her toes, her eyes not blinking",
         zh="唐小棠特寫在右，高立領扣到喉頭，眼睛瞪得好大盯著畫外右邊的紅榜，一根手指尖咬在牙齒間；指甲咬得更用力，踮起腳，眼睛一眨不眨"),
    dict(cam="Wide shot, slow push in", set=GATE, chars=["baobang"],
         lines=[("baobang", "第二名——", "拖長"), ("baobang", "州城，趙文遠！", "唱名")],
         prompt="wide shot over the heads of the packed crowd toward the herald on the wooden platform on screen right, the red scroll "
                "towering above him with only the top line left, the bamboo pointer at the second line from the top",
         motion="he taps the pointer twice on the scroll, and a ripple of murmurs runs through the crowd as heads turn to one another",
         zh="越過人群的頭頂往木台拍的全景：報榜人在右，紅榜在他上方高高聳著、只剩最上面一行，竹竿點在第二行；竹竿點兩下，人群一陣低語，大家轉頭互看"),
    dict(tag="中段鉤子", cam="Medium shot, locked", set=GATE, chars=["zhouyuanwai"],
         lines=[("zhouyuanwai", "哈哈哈！", "放聲大笑"), ("zhouyuanwai", "前三都沒有他！", "得意忘形")],
         prompt="medium shot of Zhou Yuanwai in the crowd on screen right, laughing with his head thrown back, the lidded teacup raised high "
                "in one hand, townsfolk edging away from him",
         motion="he slaps his thigh with his free hand, laughing so hard the tea slops over the cup rim",
         zh="【中段鉤子】周員外中景在右、人群裡，仰頭大笑，一手把蓋碗舉得老高，旁邊的路人往外躲；空著的手拍大腿，笑到茶從碗沿潑出來"),
    dict(tag="中段鉤子", cam="Close-up, slow push in", set=GATE, chars=["tangxiaotang"],
         lines=[("tangxiaotang", "快唸啊……", "小小聲，快哭了")],
         prompt="close-up of Tang Xiaotang's face on screen right, her high stand-up collar fastened at her throat, her lower lip trembling, "
                "her bitten fingernail at her lips, her eyes on the herald off screen right",
         motion="she squeezes her eyes shut for a moment and then forces them open again",
         zh="【中段鉤子】唐小棠特寫在右，高立領扣到喉頭，下唇在抖，咬過的指甲還在嘴邊，看著畫外右邊的報榜人；用力閉一下眼，再硬撐著睜開"),
    dict(act=2, cam="Close-up, locked", set=GATE, chars=["xudalang"],
         prompt="close-up of Xu Dalang's face on screen right in the crowd, half shaded by his old straw hat, the corner of his mouth starting "
                "to lift, his eyes on Xu Yan off screen left",
         motion="his hand drifts up to rest over the pouch hidden in his robe and the smile creeps a little wider",
         zh="許大郎特寫在右、人群裡，舊草帽遮住半張臉，嘴角開始往上翹，看著畫外左邊的許硯；手慢慢移到藏在衣襟裡的銀袋上，笑意悄悄擴大"),
    dict(cam="Close-up, locked", set=GATE, chars=["qinshuang"],
         lines=[("qinshuang", "你不緊張？", "壓低聲音")],
         prompt=f"close-up of {QS}, on screen right, her face turned toward Xu Yan off screen left, her hand gripping his sleeve at the frame "
                f"edge",
         motion="her grip tightens on his sleeve and she gives it a short tug",
         zh="戴斗笠的秦霜特寫在右，斗笠壓低只露下巴和紅唇，臉轉向畫外左邊的許硯，一手抓著畫邊他的袖子；手抓得更緊，扯一下"),
    dict(cam="Close-up, slow push in", set=GATE, chars=["xuyan"],
         lines=[("xuyan", "緊張。", "老實"), ("xuyan", "手心全是汗。", "苦笑")],
         prompt="close-up of Xu Yan's face on screen left, a crooked honest grin, his eyes on Qin Shuang off screen right",
         motion="he lifts one open palm into the frame and wipes it down the front of his robe",
         zh="許硯特寫在左，一個歪歪的老實笑，看著畫外右邊的秦霜；把一隻攤開的手心舉進畫面，在長衫前襟上抹一下"),
    # ---------------- 解元
    dict(ch="解元", insert=True, act=1, cam="Insert of the pointer on the top line, locked", set=GATE, chars=[],
         prompt="insert of the very top line of the red paper scroll, faint black brush strokes, the tip of a long thin bamboo pointer coming "
                "to rest on it",
         motion="the pointer tip lands on the top line and stops dead",
         zh="插鏡：紅紙榜最上面那一行，淡淡的黑色筆畫，細長竹竿的尖端落在上面；竹竿尖一落，定住不動"),
    dict(tag="爽點", cam="Medium close-up, low angle, slow push in", set=GATE, chars=["baobang"],
         lines=[("baobang", "解元——", "停一拍，最響")],
         prompt="medium close-up from a low angle of the herald on the wooden platform on screen right, the bamboo pointer at the very top "
                "line of the red scroll, his chest swelling, his round face shining",
         motion="he draws in a huge breath, holds the pointer still on the top line and lifts his chin",
         zh="【爽點】低角度：報榜人中近景在右、木台上，竹竿點在紅榜最上面那一行，胸口鼓起來，圓臉發亮；吸一大口氣，竹竿停在第一行不動，下巴一抬"),
    dict(tag="爽點", cam="Wide shot, slow push in", set=GATE, chars=["xuyan", "tangxiaotang", "qinshuang"],
         lines=[("baobang", "清水縣柳溪，", "畫外，一字一字"), ("baobang", "許硯！", "畫外，炸開")],
         prompt=f"wide shot of the packed crowd below the gate gone completely still, every face turned up, Xu Yan standing frozen on screen "
                f"left, Tang Xiaotang with her high stand-up collar beside him, {QS}, on screen right; the herald speaks off screen",
         motion="for a beat nobody moves, then the heads around Xu Yan turn one by one to stare at him",
         zh="【爽點】城門下擠滿的人群全景，全部一動不動、每張臉都仰著，許硯愣在左邊，高立領的唐小棠在他旁邊，戴斗笠的秦霜在右；報榜人在畫外唸；有一拍誰都沒動，然後許硯身邊的人一個一個轉頭盯著他"),
    dict(cam="Close-up, locked", set=GATE, chars=["xuyan"],
         lines=[("xuyan", "……我？", "不敢相信")],
         prompt="close-up of Xu Yan's face on screen left, his eyes wide and his mouth falling open, the red scroll blurred behind him",
         motion="he points one finger slowly at his own chest, his mouth still open",
         zh="許硯特寫在左，眼睛睜大、嘴巴掉下來，身後糊開的紅榜；一根手指慢慢指著自己胸口，嘴還張著"),
    dict(tag="爽點／奇觀", act=2, cam="Wide shot, low angle, slow pull out", set=GATE, chars=[],
         prompt="wide shot from a low angle of the whole crowd below the great gate erupting, examinees and townsfolk throwing their caps "
                "into the air, arms raised, the red scroll hanging bright on the grey wall above them",
         motion="the crowd bursts into cheering at once, dozens of caps flying up into the sunlight and tumbling back down",
         zh="【爽點／奇觀】低角度：城門下整片人群炸開，考生和路人把帽子往天上丟、手臂舉高，紅榜在上方灰牆上亮著；整片人一起歡呼，幾十頂帽子飛進陽光裡再翻落（無台詞）"),
    dict(cam="Medium close-up, locked", set=GATE, chars=["tangxiaotang", "xuyan"],
         lines=[("tangxiaotang", "中了！", "尖叫"), ("tangxiaotang", "解元！", "抱住他手臂跳")],
         prompt="medium close-up of Tang Xiaotang on screen right, her high stand-up collar fastened at her throat, flinging both arms around "
                "Xu Yan's arm, Xu Yan on screen left still stunned",
         motion="she jumps up and down hugging his arm, her pink silk ribbons bouncing",
         zh="唐小棠中近景在右，高立領扣到喉頭，雙手一把抱住許硯的手臂，許硯在左還愣著；她抱著他的手臂跳上跳下，粉色絲帶一直彈"),
    dict(cam="Close-up, locked", set=GATE, chars=["qinshuang"],
         lines=[("qinshuang", "我就知道。", "嘴角翹起來")],
         prompt="close-up of Qin Shuang on screen right in the cheering crowd, a wide woven bamboo douli hat pulled low over her eyes, only "
                "her clean-lined jaw and red lips showing, her lips curving into a proud smile, her face turned toward Xu Yan off screen left",
         motion="she lifts one hand under the brim and quickly brushes the corner of her eye with a knuckle",
         zh="戴斗笠的秦霜特寫在右、歡呼的人群裡，斗笠壓低只露下巴和紅唇，嘴角彎成一個驕傲的笑，臉朝畫外左邊的許硯；一隻手伸到帽簷下，用指節飛快抹一下眼角"),
    dict(tag="升級", cam="Close-up, slow push in", set=GATE, chars=["xuyan"],
         lines=[("xitong", "鄉試任務完成。", "平板電子音，叮一聲"), ("xitong", "獎勵：活字印刷。", "平板電子音")],
         prompt="close-up of Xu Yan's face on screen centre, his eyes lifting to a point in the empty air in front of him, a dazed smile "
                "beginning; the system voice speaks off screen",
         motion="his eyes track slowly across the empty air as if reading and the smile spreads",
         zh="【升級】系統面板：許硯的臉在中間，眼睛抬起看著面前的空中，一個還有點傻的笑慢慢出來；眼睛像讀字一樣慢慢掃過空中，笑開了",
         ov=[("任務完成：鄉試中舉｜獎勵：活字印刷", "reward")]),
    dict(tag="升級", cam="Medium close-up, locked", set=GATE, chars=["xuyan"],
         lines=[("xuyan", "活字……", "自言自語"), ("xuyan", "得找個刻字匠。", "撓頭")],
         prompt="medium close-up of Xu Yan in the cheering crowd on screen left, Tang Xiaotang's pink sleeve still hooked on his arm at the "
                "frame edge, his brows knitting in thought",
         motion="he scratches the back of his head with his free hand, thinking hard",
         zh="【升級】許硯中近景在左、歡呼的人群裡，唐小棠的粉袖還勾在他手臂上，眉頭皺起來在想；空著的手抓抓後腦"),
    dict(act=2, cam="Close-up, locked", set=GATE, chars=["xudalang"],
         prompt="close-up of Xu Dalang's face on screen right in the cheering crowd, the smile frozen stiff under his old straw hat, his hand "
                "pressed flat over the pouch in his robe",
         motion="his hand clenches on the robe over the pouch and he tugs the hat brim down and turns away into the crowd",
         zh="許大郎特寫在右、歡呼的人群裡，舊草帽下的笑僵住，一手平按在衣襟裡的銀袋上；手揪緊衣襟，把帽簷往下一拉，轉身鑽進人群"),
    # ---------------- 倒著走
    dict(ch="倒著走", tag="爽點", cam="Wide shot, slow push in", set=STREET, chars=["zhouyuanwai", "tangxiaotang"],
         lines=[("zhouyuanwai", "借過……", "紅著臉"), ("zhouyuanwai", "借過……", "小聲")],
         prompt="wide shot down the long busy street, Zhou Yuanwai walking backwards toward the camera through the laughing crowd in his "
                "soy-brown robe, Tang Xiaotang in her peach-pink ruqun with the high stand-up collar walking after him on screen right "
                "counting on her fingers",
         motion="Zhou Yuanwai takes careful backward steps, bumping into a fruit basket and stumbling, while the crowd on both sides points and laughs",
         zh="【爽點】沿著長街拍的全景：周員外穿著醬色綢袍，在一路笑的人群裡倒著往鏡頭走，高領桃粉襦裙的唐小棠在右邊跟在後面扳手指數；周員外小心地倒退，撞到一籃水果踉蹌一下，兩邊的人指著他笑"),
    dict(cam="Medium close-up, slow pan left", set=STREET, chars=["tangxiaotang"],
         lines=[("tangxiaotang", "才走一半，", "笑得很甜"), ("tangxiaotang", "員外加油！", "揮手")],
         prompt="medium close-up of Tang Xiaotang walking along the street on screen right, her high stand-up collar fastened at her throat, "
                "her cheeks rosy, waving one hand like a cheerleader, her eyes on Zhou Yuanwai off screen left",
         motion="she skips two steps forward and waves her hand high over her head",
         zh="唐小棠中近景在右、走在街上，高立領扣到喉頭，臉頰紅撲撲，像在加油一樣揮手，看著畫外左邊的周員外；往前小跳兩步，把手揮過頭頂"),
    dict(cam="Close-up, locked", set=STREET, chars=["zhouyuanwai"],
         lines=[("zhouyuanwai", "我……", "漲紅臉"), ("zhouyuanwai", "我走就是了！", "咬牙")],
         prompt="close-up of Zhou Yuanwai's long narrow face on screen left, flushed deep red to the ears, his skullcap knocked crooked, his "
                "eyes on Tang Xiaotang off screen right",
         motion="he grits his teeth, jams the crooked skullcap straight with one hand and takes another stiff step backwards",
         zh="周員外的長臉特寫在左，紅到耳根，瓜皮帽被撞歪，看著畫外右邊的唐小棠；咬牙，一手把歪掉的帽子按正，又僵硬地倒退一步"),
    dict(cam="Two-shot, locked", set=STREET, chars=["qinshuang", "xuyan"],
         lines=[("qinshuang", "一條街，", "抱胸"), ("qinshuang", "一步都不能少。", "冷冷地笑")],
         prompt=f"two-shot at the roadside, {QS}, on screen left with her arms folded, Xu Yan beside her on screen right laughing, both "
                f"of them turned toward the left where the squire is walking backwards down the street",
         motion="Xu Yan doubles over laughing with a hand on his knee while Qin Shuang stays still with her arms folded",
         zh="路邊雙人鏡：戴斗笠的秦霜在左、雙手抱胸，許硯在右笑著，兩人都看著畫外左邊的周員外；許硯笑到彎腰、手撐膝蓋，秦霜抱胸一動不動"),
    # ---------------- 遊街
    dict(ch="遊街", tag="奇觀", act=3, cam="Wide shot, high angle, slow push in", set=STREET, chars=["xuyan"],
         prompt="wide shot from a high angle over the main street, a procession of drummers and musicians with gongs and red banners "
                "leading a white horse through the packed crowd, Xu Yan riding the white horse with a big red silk flower tied across his "
                "chest, the crowd pressing in from both sides",
         motion="the drummers strike their drums and gongs together, the white horse steps forward, and petals and confetti rain down "
                "from the upper windows",
         zh="【奇觀】高角度俯瞰大街：鑼鼓隊、吹打手舉著紅旗在前面開路，後面一匹白馬穿過擠滿的人群，許硯騎在白馬上、胸前繫一朵大紅綢花，兩邊的人潮往裡擠；鼓和鑼一起敲下去，白馬往前走，樓上的窗戶灑下花瓣與彩紙"),
    dict(tag="顏值鏡頭", cam="Medium close-up, slow push in", set=STREET, chars=["xuyan"],
         lines=[("xuyan", "各位，", "笑得眼睛彎彎"), ("xuyan", "同喜同喜！", "拱手")],
         prompt="medium close-up of Xu Yan riding the white horse in the middle of the frame, the big red silk flower on his chest, petals "
                "falling around him in the noon sun, his eyes curved into crescents in a wide happy grin",
         motion="he cups his hands and bows from the saddle to one side of the street and then the other",
         zh="【顏值鏡頭】許硯中近景在中間、騎在白馬上，胸前一朵大紅綢花，正午的陽光裡花瓣在他身邊飄，笑得眼睛彎成月牙；在馬上拱手，往街的這邊鞠一下、再往那邊鞠一下"),
    dict(tag="顏值鏡頭", cam="Medium shot, locked", set=STREET, chars=["tangxiaotang"],
         lines=[("tangxiaotang", "許硯——", "跳著喊"), ("tangxiaotang", "這邊！", "揮手")],
         prompt="medium shot of Tang Xiaotang in the crowd at the roadside on screen right, her fitted peach-pink silk ruqun with the high "
                "stand-up collar fastened at her throat, jumping and waving both arms, the pink silk ribbons in her looped buns flying, "
                "her face lit up with joy",
         motion="she jumps high with both arms waving and her pink ribbons fly up and fall back",
         zh="【顏值鏡頭】唐小棠中景在右、路邊人群裡，合身桃粉綢襦裙、高立領扣到喉頭，跳著揮兩隻手，髮髻上的粉色絲帶翻飛，整張臉都亮了；她雙手揮著高高跳起，粉絲帶飛上去又落下"),
    dict(tag="結尾", act=2, cam="Medium shot, slow pan right", set=STREET, chars=["qinshuang", "xuyan"],
         prompt=f"medium shot beside the white horse, {QS}, walking at the horse's shoulder on screen left, Xu Yan in the saddle above her "
                f"on screen right with the red silk flower on his chest",
         motion="Qin Shuang reaches up and closes her hand around the reins below the horse's chin, and the horse slows to a stop",
         zh="【結尾】白馬旁的中景：戴斗笠的秦霜在左、走在馬肩旁，許硯在右、坐在她上方的馬鞍上，胸前紅綢花；秦霜伸手握住馬下巴底下的韁繩，馬慢慢停下"),
    dict(tag="結尾", cam="Close-up, locked", set=STREET, chars=["xuyan"],
         lines=[("xuyan", "怎麼了？", "低頭，笑還沒收")],
         prompt="close-up of Xu Yan's face from a low angle on screen right, looking down from the saddle, his grin fading into a question, "
                "his eyes on Qin Shuang off screen left below him",
         motion="he leans down a little over the horse's neck toward her",
         zh="【結尾】低角度：許硯的臉特寫在右，從馬鞍上低頭看，笑慢慢收成疑問，看著畫外左下的秦霜；身子在馬脖子上方往她那邊低一點"),
    dict(tag="結尾", cam="Close-up, slow push in", set=STREET, chars=["qinshuang"],
         lines=[("qinshuang", "今晚，", "仰頭，聲音很輕"), ("qinshuang", "我有話跟你說。", "眼睛濕了")],
         prompt="close-up of Qin Shuang's face from a high angle on screen left, her wide douli hat pushed back off her brow so her whole "
                "face shows, her bold brows soft, her almond eyes wet and shining as she looks up at Xu Yan off screen right, her hand on "
                "the reins",
         motion="she looks up at him without blinking and her fingers tighten on the reins",
         zh="【結尾】最後一格：高角度：秦霜的臉特寫在左，寬斗笠推到額頭後面、整張臉露出來，劍眉軟下來，杏眼濕亮，仰頭看著畫外右上的許硯，手握著韁繩；她仰著頭不眨眼，手指把韁繩握緊"),
]

MUSIC = ("a creeping low string as the cousin hides the silver, a huge drum hit and a rushing swell as the red scroll unrolls down the "
         "gate wall, a ceremonial gong and the herald's sing-song over a ticking woodblock that climbs with every rank, a sly bassoon for "
         "the squire's bet and a bright comic sting for 'all of you heard it', a sharp drum stab as the red brush strikes the examiner's "
         "name, the ticking tightening and the strings rising unbearably through the top three, cutting to dead silence on 'jieyuan', then "
         "an explosion of drums, suona and cymbals as the crowd erupts, a glassy chime and a bright fanfare for the reward, a comic tuba "
         "waddle for the squire walking backwards, a festive parade of gongs, drums and suona, and under it all a soft warm guqin that "
         "slows and falls quiet on her wet eyes and 'tonight', ancient Chinese drama, no vocals")

YT_DESC = ("放榜這天一早，紅榜從州城城門頂一口氣滾下來，報榜人從最後一名唸起：「第八十名——」"
           "周員外擠過人群冷笑：「他要是中了，我倒著走！」唐小棠甜甜一笑：「說好了，倒著走一條街。」"
           "唸到一半，州府衙役當眾在考官榜上，把馮學正的名字一筆劃掉。可前一晚改過的榜到底有沒有改回來，誰也不知道——"
           "第十名、第三名、第二名都沒有許硯，周員外笑出聲，唐小棠的指甲都快咬斷了。最後一個：「解元——清水縣柳溪，許硯！」"
           "整條街靜了一下，然後炸開。系統：鄉試任務完成，獎勵活字印刷——但要找到刻字匠才做得出來。"
           "周員外在全街的笑聲裡倒著走了一整條街。解元遊街，許硯戴著紅花騎白馬，秦霜走到馬邊拉住韁繩，仰頭看他，眼睛是濕的：「今晚，我有話跟你說。」"
           "《種田娶妻打天下》第 49 集。")


def SB_HEAD(total, st, du):
    def at(s):
        t = int(st[s]); return f"{t // 60}:{t % 60:02d}"
    end = f"{int(total) // 60}:{int(total) % 60:02d}"
    return [
        f"{len(SHOTS)} 個鏡頭、七段（紅榜／打賭／劃掉／前三／解元／倒著走／遊街），估計約 {total:.0f} 秒（照 lint 估法；真人語速通常再長一成左右）；細綱 120 秒",
        "預算：片段 %d 支（靜圖 0 張），沒有「切素材」鏡。片段走路線 A（Colab H3 Ref2VA 三段式，沒有首格）；秒數見 `hailuo/clips-dh-e049.json`（`gen-dh.mjs` 算），首格清單只當參照圖清單" % len(SHOTS),
        f"開頭 10 秒：接第 48 集的最後一格，許大郎把銀袋塞進懷裡、抬頭（0:00），紅榜從城牆頂滾下來（{at('s02')}），報榜人「第八十名——」（{at('s03')}），唐小棠「從最後一名唸起？」（{at('s04')}）；中段鉤子：前三都沒有他、周員外笑出聲、唐小棠咬指甲（{at('s19')}–{at('s23')}）；轉折：考官榜上劃掉馮學正（{at('s12')}–{at('s14')}），「解元——清水縣柳溪，許硯！」整條街靜了一下然後炸開（{at('s28')}–{at('s31')}）；結尾收在秦霜拉住韁繩「今晚，我有話跟你說」",
        f"鉤子：【鉤子1】s01–s05 0:00、【鉤子2】s06–s10 {at('s06')}、【鉤子3】s11–s17 {at('s11')}、【鉤子4 中段】s18–s26 {at('s18')}、【鉤子5】s27–s31 {at('s27')}、【鉤子6】s32–s36 {at('s32')}、【鉤子7】s37–s40 {at('s37')}、【結尾】s41–s46 {at('s41')}–{end}",
        "顏值鏡頭：s42 許硯（戴紅花騎白馬，笑得眼睛彎彎）、s43 唐小棠（在人群裡跳著揮手，粉色絲帶翻飛）、s46 秦霜（斗笠推到額後，仰頭，濕亮的杏眼）；是臉與動作，不停在身體",
        "爽點：前半 betrayer_punished（s12–s14 考官榜上馮學正的名字被紅筆劃掉）、中段 public_vindication（s28–s32「解元——清水縣柳溪，許硯！」整條街炸開）、後半 level_up（s34–s35 鄉試任務完成、獎勵活字印刷）",
        "說話鏡頭：說話的人在畫面上的鏡頭，motion 第一句都是他說這句話、嘴唇下巴隨每個音節動；畫外台詞（s29 報榜人唸名字、s34 系統）放在別人的反應鏡上，prompt 寫明 off screen",
        "H3 寫法：motion 寫軌跡、一鏡一事、沒有 camera 字；秦霜每一鏡寫斗笠（第 42 集的那段字），s46 才把斗笠推到額後露出整張臉；唐小棠每一鏡寫高立領；插鏡（s11、s13、s16、s27）motion 開頭寫 `The shot opens directly on this close insert from its very first frame`；紅榜、考官榜只寫 `columns of faint black brush strokes`，不寫字；看紅榜、看告示寫成 `beyond the right edge of the frame`，不寫 off screen（shot_reading 會把物件後面的 off screen 讀成畫外的人）",
        "光：s01–s36 城門下早晨的亮光；s37–s46 大街正午的陽光、花瓣與彩紙",
        "軸線：城門下紅榜與報榜人的木台在右、許硯一行在左（許硯左、唐小棠中、秦霜右），周員外從右邊擠過來，考官榜貼在紅榜旁（右）；大街上周員外倒著往鏡頭走、唐小棠在右跟著，秦霜與許硯在路邊看向左；遊街時秦霜在馬的左邊、許硯在右上的馬鞍上",
    ]


SB_FOOT = [
    "場景參考：s01–s36 用 `dh-set-chengmen-t1`（含 `city gate`；沿用第 42 集的州城城門那張，紅榜與木台靠 prompt 寫出來；registry：只寫 city gate，不寫 city wall，也不在同一句寫 `main street of Qingzhou`）；s37–s46 用 `dh-set-zhou-jie-t1`（含 `main street of Qingzhou`，還沒畫）。",
    "道具：許大郎的藍綢銀袋（s01、s24、s36，藏在衣襟裡）；紅紙榜（s02–s31）；報榜人的細長竹竿（s03、s11、s18–s28）；考官榜白紙告示與滴紅墨的大筆（s12–s13）；周員外的蓋碗與碧玉扳指（s06、s15–s16、s22）；許硯左袖裡的銀票（s17 手按著，第 48 集收進去的）；秦霜的寬竹斗笠（每一鏡）；白馬、大紅綢花、鑼鼓、花瓣彩紙（s41–s46）。",
    "連戲：開場照第 48 集的結尾（暗巷裡銀袋落進許大郎手心）接：s01 是第二天早上，他把同一個銀袋塞進懷裡，抬頭就是紅榜。前一晚知府說「改不改得回來，明天就知道」（第 48 集 s06–s07），所以 s17「考官劃了，那榜呢？」與 s18–s26 前三都沒有他時，誰都不知道榜改回來了沒有。s12–s13 劃掉的是考官榜（另一張白紙），不是紅榜；馮學正第 47 集已被拿下。報榜人照第 42、43 集書吏與馮學正的唸法報「清水縣柳溪，許硯」（細綱寫「柳溪許硯」）；唸的其他名字（陳大有、林世安、李守正、趙文遠）是本集編的，不再出現。周員外的賭約照細綱（中了我倒著走），唐小棠把它加碼成「一條街」（s09），s37–s40 兌現。s35「得找個刻字匠」照系統的規則（獎勵只給方法，材料與人要自己找）。第 50 集從客棧門口跪了一排人接（秦霜那句話還沒出口）。",
    "m05：s01、s24、s36 只拍許大郎和他藏在懷裡的銀袋（第 48 集他向魏家告密收的錢），s36 許硯中了以後他的笑僵住、轉身鑽進人群；他為什麼這樣做全集不說。",
    "系統面板不由模型畫：s34 的任務完成與獎勵在剪接時疊上（reward）。",
    "新的參照圖還沒畫：周員外、許大郎的定妝照（`refs-dh/zhouyuanwai-portrait-t1.png`、`xudalang-portrait-t1.png`）與大街的場景圖（`set-zhou-jie-t1.png`）。報榜人（baobang）沒有定妝照，照 e042 的掌櫃只寫在 prompt 與 video.json。",
]


def BRIEF(st, du, total):
    def at(s):
        t = int(st[s]); return f"{t // 60}:{t % 60:02d}"
    end = f"{int(total) // 60}:{int(total) % 60:02d}"
    return f"""# 《種田娶妻打天下》第 49 集〈放榜〉

## 故事前提

第 48 集收在半夜的暗巷：許大郎對魏家管家彎腰「那個姓秦的，是秦烈山的女兒」，管家把一袋銀子塞進他手裡。第 49 集從那袋銀子接下去：第二天一早，城門下擠滿看榜的人，許大郎把同一個銀袋塞進懷裡、拍平，猛地抬頭（s01）——一卷紅榜從城垛上一口氣滾下來，貼著灰磚牆垂到地（s02，細綱的 hook 與奇觀），報榜人吸飽一口氣：「第八十名——」「青州，陳大有！」（s03）。上一集的問題「族兄為什麼要出賣他們？」這集不答，只讓他的銀袋一直在畫面裡（s01、s24、s36）。唐小棠踮腳：「從最後一名」「唸起？」許硯硬撐著笑：「八十個名字，」「慢慢等。」

周員外擠過人群：「喲，」「許秀才也來看榜？」「他要是中了，」「我倒著走！」許硯笑嘻嘻指他的腳：「員外，」「鞋帶先綁緊。」唐小棠甜得危險：「說好了，」「倒著走一條街。」戴斗笠的秦霜：「大家都聽見了。」竹竿一行一行往上點；兩個衙役擠過人群，在紅榜旁的考官榜上一筆紅線劃掉一整列（s12–s13）——唐小棠「劃的是……」「馮學正！」（first_half betrayer_punished）；周員外笑僵「劃、劃一個考官，」「算什麼。」手上的蓋碗喀喀響。許硯按著袖裡的銀票：「考官劃了，」「那榜呢？」（細綱的衝突：前一晚改過的榜有沒有改回來，誰也不知道。）

「第十名——」「第三名——」唐小棠咬著指甲踮腳；「第二名——」「州城，趙文遠！」周員外仰頭大笑「哈哈哈！」「前三都沒有他！」唐小棠快哭了「快唸啊……」（{at('s19')}–{at('s23')}，細綱的 mid_hook）；人群裡的許大郎嘴角開始翹起來。秦霜扯他袖子「你不緊張？」許硯苦笑「緊張。」「手心全是汗。」

竹竿落在最上面一行：「解元——」整片人群靜下來，「清水縣柳溪，」「許硯！」（細綱的 turn）許硯指著自己「……我？」，整條街炸開，帽子飛上天（midpoint public_vindication）；唐小棠抱著他手臂跳「中了！」「解元！」秦霜在斗笠下抹一下眼角「我就知道。」系統：「鄉試任務完成。」「獎勵：活字印刷。」許硯抓抓頭：「活字……」「得找個刻字匠。」（second_half level_up；general_payoff：高中解元、鄉試任務完成、得活字印刷——要找刻字匠才做得出來。）許大郎的笑僵住，按著懷裡的銀袋鑽進人群。

大街上，周員外在全街的笑聲裡倒著走，撞到水果籃：「借過……」「借過……」唐小棠跟在後面數：「才走一半，」「員外加油！」「我……」「我走就是了！」秦霜抱胸：「一條街，」「一步都不能少。」（general_payoff：周員外當眾賭、真的倒著走了一條街。）解元遊街：鑼鼓隊開路，許硯戴大紅花騎白馬，笑得眼睛彎彎「各位，」「同喜同喜！」（細綱的顏值鏡頭），唐小棠在人群裡跳著揮手，粉色絲帶翻飛。秦霜走到馬邊伸手拉住韁繩，馬停下；許硯低頭「怎麼了？」秦霜把斗笠推到額後，仰頭看他，眼睛是濕的：「今晚，」「我有話跟你說。」（細綱的 cliffhanger，emotion：「秦霜要告訴他什麼？」；第 50 集從客棧門口跪了一排人接。）

本集細綱：`docs/videos/series-plans/zhong-tian-qu-qi/season-01.json` 第 49 集（120 秒，第一季第五章，調性爽＋喜劇，lead_arc wins）。hook 是許大郎把銀袋塞進懷裡、紅榜從城牆頂滾下來、「第八十名——」（0:00–{at('s04')}，image）；mid_hook 是唸到前三還沒有他、周員外笑出聲、唐小棠咬指甲（{at('s19')}–{at('s23')}）；衝突是前一晚改過的榜有沒有改回來（s17–s26）；turn 是考官榜上劃掉馮學正（s12–s14）與「解元——清水縣柳溪，許硯」整條街靜了一下然後炸開（s27–s31）；cliffhanger 是遊街時秦霜拉住韁繩「今晚，我有話跟你說」（s44–s46，emotion）。satisfaction：first_half betrayer_punished、midpoint public_vindication、second_half level_up。本集觀眾跟許硯一樣不知道榜改回來沒有（只多知道許大郎懷裡的銀袋），authoring.md：一集只選一種。

## 鉤子（站主 10-16：開場、結尾之外中段還要兩三個以上）

| 鉤子 | 鏡 | 約略時間 | 內容 |
| --- | --- | --- | --- |
| 【鉤子1】開場 | s01–s05 | 0:00–{at('s06')} | 銀袋塞進懷裡，紅榜從城牆頂滾下來，「第八十名——」，「從最後一名唸起？」 |
| 【鉤子2】 | s06–s10 | {at('s06')}–{at('s11')} | 周員外「他要是中了，我倒著走！」「員外，鞋帶先綁緊」「說好了，倒著走一條街」 |
| 【鉤子3】 | s11–s17 | {at('s11')}–{at('s18')} | 衙役在考官榜上一筆劃掉，「劃的是……馮學正！」「考官劃了，那榜呢？」 |
| 【鉤子4】中段鉤子 | s18–s26 | {at('s18')}–{at('s27')} | 「第十名」「第三名」「第二名」都不是他，「前三都沒有他！」「快唸啊……」，許大郎的笑 |
| 【鉤子5】 | s27–s31 | {at('s27')}–{at('s32')} | 竹竿落在第一行，「解元——」全街靜下來，「清水縣柳溪，許硯！」「……我？」帽子飛上天 |
| 【鉤子6】 | s32–s36 | {at('s32')}–{at('s37')} | 「中了！」「我就知道」，「鄉試任務完成，獎勵：活字印刷」「得找個刻字匠」，許大郎的笑僵住 |
| 【鉤子7】 | s37–s40 | {at('s37')}–{at('s41')} | 周員外倒著走「借過……借過……」「才走一半，員外加油！」「一步都不能少」 |
| 【結尾】 | s41–s46 | {at('s41')}–{end} | 鑼鼓遊街、白馬紅花，秦霜拉住韁繩「今晚，我有話跟你說」（她要告訴他什麼？） |

## 角色

- 許硯（xuyan）：s04 在人群裡（不說話）；s05「八十個名字，慢慢等」；s08「員外，鞋帶先綁緊」；s12 轉身看衙役；s17「考官劃了，那榜呢？」；s26「緊張。手心全是汗」；s29 愣住；s30「……我？」；s34 看系統面板；s35「活字……得找個刻字匠」；s41–s42 騎白馬遊街「各位，同喜同喜！」；s45「怎麼了？」
- 唐小棠（tangxiaotang）：s04「從最後一名唸起？」；s09「說好了，倒著走一條街」；s14「劃的是……馮學正！」；s20 咬指甲；s23「快唸啊……」；s32「中了！解元！」；s37–s38 跟著周員外數步「才走一半，員外加油！」；s43 在人群裡跳著揮手。每個 prompt 都寫高立領。
- 秦霜（qinshuang）：每一鏡戴斗笠（城裡怕被兵認出，照第 42 集）。s10「大家都聽見了」；s25「你不緊張？」；s33「我就知道」；s40「一條街，一步都不能少」；s44 拉住韁繩；s46 把斗笠推到額後「今晚，我有話跟你說」（收尾）。
- 周員外（zhouyuanwai）：s06「喲，許秀才也來看榜？」；s07「他要是中了，我倒著走！」；s15「劃、劃一個考官，算什麼」；s16 蓋碗喀喀響；s22「哈哈哈！前三都沒有他！」；s37「借過……借過……」倒著走；s39「我……我走就是了！」
- 許大郎（xudalang）：s01 把銀袋塞進懷裡（開場）；s24 嘴角翹起來、手按著銀袋；s36 笑僵住、鑽進人群。不說話。
- 報榜人（baobang）：本集才有的配角，沒有定妝照，外貌只寫在 video.json 與 prompt（四十歲、壯、紅潤圓臉、紅邊黑袍、紅纓帽、細長竹竿）；聲音 Iapetus（registry 的建議值）。s03「第八十名——青州，陳大有！」；s18「第十名——」；s19「第三名——」；s21「第二名——」；s28「解元——」；s29 畫外「清水縣柳溪，許硯！」
- 系統（xitong）：沒有身體，只有聲音與剪接時疊上的面板（`overlays.json`：s34 任務完成與獎勵）。
- 衙役、考生、路人、鑼鼓隊、吹打手：背景，只寫在 prompt 裡（runners、examinees、townsfolk、drummers、musicians），沒有台詞。

## 地點（固定的地點字）

- 州城城門下（早晨）：`Below the great city gate of Qingzhou in bright morning light`（s01–s36，沿用 `dh-set-chengmen-t1`；紅榜從城垛垂下、木台在右，靠 prompt 寫出來）。
- 州城大街（正午）：`On the main street of Qingzhou in bright noon light`（s37–s46，新場景 `dh-set-zhou-jie-t1`，還沒畫）：兩邊的旗幌招牌、一串串紅燈籠、擠滿歡呼的人。
- 站位（軸線）：見分鏡表開頭。

## 站主觀點

站主 2026-10-16 的要求：女生要火辣漂亮，濃顏系的五官與妝、合身剪裁；不露、不濕身、鏡頭不停在身體部位；每集至少一個顏值鏡頭；結尾收在最高點；不被黃標；每集開場、結尾之外中段再兩三個以上鉤子。本集的顏值鏡頭是 s42（許硯戴紅花騎白馬，笑得眼睛彎彎）與 s43（唐小棠在人群裡跳著揮手，粉色絲帶翻飛），收尾 s46 秦霜仰頭、濕亮的杏眼；拍的是臉與動作。唐小棠每一鏡都寫高立領；秦霜每一鏡都寫斗笠。紅榜與考官榜不畫字：只有一行行淡淡的筆畫，劃掉的是一道紅線。系統面板不由模型畫，s34 只拍許硯的眼睛。

分鏡照 `storyboard-rules.md` 2026-10-28 起的 H3 寫法（與第 42 集同）：說話的人在畫面上時 motion 第一句寫他說這句話；motion 寫軌跡、一鏡一事；表情寫成正面的字；道具寫大小；畫外的人不寫局部身體；運鏡只在 `camera`；`locked` 就是鎖定；秒數由 `gen-dh.mjs` 決定。本集沒有靜圖、沒有切素材鏡。角色外觀照 `production/cast.json` 逐字照抄。
"""
