EP = 55
EP_TITLE = "鎖起來"
OUTLINE_SECONDS = 110
TARGET_MINUTES = [1, 2]
TITLE = "三個老婆好感都過六十，系統大獎他看一眼就鎖起來｜種田娶妻打天下 第55集"
DESCRIPTION = "河灘的火堆旁，秦霜問他常對著空氣笑，那裡有什麼。許硯看著火：「那裡有我想要的。一個家。」阿令的好感度從 59 跳到 61——三位妻子的好感都過了 60，系統開出大獎：火藥配方。有了它，再也沒人敢來抓他的家人；可它也能讓很多人死。許硯把配方設成封存，連自己都不打開。阿令問他在想什麼，他說：「能殺很多人的東西。先鎖著。」她看了他很久。回柳溪那天，全村敲鑼打鼓迎解元，當初笑他考三次沒中的錢員外被村民推到最前面，只好彎腰作揖。晚上院子裡，唐萬金的信差衝進門，唐小棠拆信唸到一半停住：「魏少卿帶著一幅畫像，進了相府。」阿令手裡的茶碗晃了一下。《種田娶妻打天下》第 55 集。"
THUMB = ("鎖起來", "s11")
CHARACTERS = ["xuyan", "aling", "qinshuang", "tangxiaotang", "hanbo", "xiaohe", "qianyuanwai", "xinchai", "xitong"]
MINOR = {
    "xinchai": {"id": "xinchai", "name": "信差", "appearance": "East Asian young man of twenty-five, lean and dusty from the road, a sweat-streaked face, a dark blue short jacket with a red courier's armband and cloth leggings, a leather letter pouch slung across his chest", "voice": {"provider": "gemini", "name": "Puck", "style": "標準國語，咬字清楚，台北人平常說話的語調；二十五歲的鏢局信差，男聲、跑得上氣不接下氣、說話又急又快"}},
}
MUSIC = "a warm low crackle of the campfire under a soft breathy xiao as he says a home, a small sweet bell for her affection, then a rising shimmering choir-like synth and bright golden strings swelling as the great prize opens, a deep ominous low drum and a dark brass chord at the word gunpowder, a held tense string while he weighs it, then a single cold metallic click and a clear blue glassy chime as it locks, a quiet tender guqin across the fire as she asks what he is thinking, a gentle warm swell on her first unturned gaze, then a joyful burst of village gongs, suona and drums at the village entrance, a cheeky bassoon and a comic woodblock as the landlord is pushed forward and bows, a bright abacus glockenspiel for the settled account, then a calm evening of soft plucked zither in the yard, a sudden hurried drum as the courier bursts in, a low creeping cello under the letter, cut on one trembling high string as the teacup shakes, ancient Chinese rural drama, no vocals"

LOC = {
    "fire": "On the pebble riverbank by the north ferry at night, a campfire of driftwood with sparks flying up, flat rocks around it to sit on, the dark river beyond, a sky full of stars",
    "gate": "At the Liuxi village entrance on a bright clear morning, an old weeping willow beside a mossy stone arch bridge over the stream, a dirt road winding up between timber houses, red cloth streamers tied to the willow branches, villagers crowding the road",
    "yard": "In the small dirt yard of the Xu farmhouse in the late afternoon, a low mud wall and a broken wooden gate, a woodpile and chopping block, a well with a wooden bucket, a persimmon tree with a low table and stools set out under it, warm slanting sunlight",
}
LIGHT = {"fire": "the warm firelight and the starry night stay unchanged", "yard": "the warm late-afternoon light stays unchanged"}

SHOTS = [
    dict(chapter="一個家", loc="fire", cam="Close-up, slow push in", chars=["xuyan"], night="fire", tag="鉤子1／開頭",
         comp="close-up of Xu Yan's face in the firelight, his eyes moving from the empty air to the flames, a quiet smile forming",
         lines=[("xuyan", "那裡有我想要的。", "看著火，很輕"), ("xuyan", "一個家。", "笑")],
         motion="after the last word he picks up a stick and nudges a log deeper into the fire",
         zh="接第 54 集：許硯特寫，火光裡，眼睛從面前的空氣移到火焰上，嘴角慢慢浮出一個安靜的笑；說完撿起一根柴，把一塊木頭推進火裡（他沒說出系統，說的是真話）"),
    dict(loc="fire", cam="Close-up, locked", chars=["aling"], night="fire", tag="鉤子1",
         comp="close-up of A-ling across the fire, the stick still in her hand, her phoenix eyes on Xu Yan off screen left, her cold face softening for an instant",
         lines=[("xitong", "阿令好感，六十一。", "平板電子音，叮一聲")],
         panel=[("阿令 好感 +2 → 61", "affection")],
         motion="her hand on the stick goes still and she lowers her eyes to the embers",
         zh="阿令特寫、火堆另一邊，手上還拿著那根柴，鳳眼看著畫外左邊的許硯，冷冷的臉軟了一瞬；拿柴的手停住，垂眼看炭（59 → 61）"),
    dict(loc="fire", cam="Two-shot, locked", chars=["qinshuang", "xuyan"], night="fire",
         comp="two-shot by the fire, Qin Shuang on screen left with her head back on Xu Yan's shoulder, her eyes half closed, Xu Yan on screen right",
         lines=[("qinshuang", "這算什麼答案……", "睏，嘟囔")],
         motion="she mumbles into his shoulder, her eyes drift shut and her breathing slows into sleep",
         zh="雙人鏡：火邊，秦霜在左又把頭靠回許硯肩上，眼睛半閉，許硯在右；她對著他的肩嘟囔一句，眼睛慢慢闔上，呼吸變慢睡著了"),
    dict(chapter="大獎", loc="fire", cam="Close-up, locked", chars=["xuyan"], night="fire", tag="鉤子2",
         comp="close-up of Xu Yan's face in the firelight, his eyes lifting to a fixed point in the empty air in front of him",
         lines=[("xitong", "三位妻子好感，", "平板電子音，叮一聲"), ("xitong", "全數突破六十。", "平板電子音")],
         panel=[("三位妻子好感：唐小棠 61｜秦霜 66｜阿令 61", "affection")],
         motion="his eyes track across the empty air as if reading and his brows rise slowly",
         zh="系統面板：許硯特寫，火光裡，眼睛抬起定在面前的空中；眼睛像在讀字一樣掃過去，眉毛慢慢揚起"),
    dict(loc="fire", cam="Close-up, slow push in", chars=["xuyan"], night="fire", tag="鉤子2",
         comp="close-up of Xu Yan's face with the dark river and the stars blurred far behind him, a warm golden glow blooming on his face from the empty air in front of him, brighter than the firelight, his eyes wide and his lips parted",
         lines=[("xitong", "解鎖大獎。", "平板電子音")],
         motion="the golden glow swells across his face and he leans back a little from it, squinting",
         zh="奇觀（一）：許硯特寫，一道比火光還亮的金光從他面前的空氣裡打到臉上，眼睛睜大；金光在他臉上暴漲，他微微往後仰、瞇起眼（面板本身不畫，金光當光源）"),
    dict(loc="fire", cam="Extreme close-up, locked", chars=["xuyan"], night="fire", tag="鉤子2",
         comp="extreme close-up of Xu Yan's eyes, a golden light reflected in them, his brows drawing slowly together",
         lines=[("xitong", "大獎：火藥配方。", "平板電子音，一字一頓")],
         panel=[("大獎：火藥配方", "task")],
         motion="his pupils narrow and his brows draw together hard",
         zh="許硯的眼睛大特寫，眼裡映著金光，眉頭慢慢收攏；瞳孔一縮，眉頭狠狠皺起"),
    dict(loc="fire", cam="Medium close-up, locked", chars=["xuyan"], night="fire",
         comp="medium close-up of Xu Yan by the fire, Qin Shuang asleep on his shoulder at the edge of the frame, the golden glow fading on his face, his hand tightening on his knee",
         lines=[("xuyan", "火藥……", "幾乎沒聲音")],
         motion="he swallows and his eyes drop from the empty air to the fire",
         zh="許硯中近景，秦霜靠在他肩上睡著（畫邊），臉上的金光慢慢退去，放在膝上的手收緊；低頭看自己膝上的手，慢慢握成拳"),
    dict(loc="fire", cam="Close-up, slow push in", chars=["xuyan"], night="fire", tag="鉤子3",
         comp="close-up of Xu Yan's face in the firelight, his jaw set, a hard light in his eyes, looking toward the tied escorts far down the dark bank",
         lines=[("xuyan", "有了它，", "低聲，咬牙"), ("xuyan", "誰還敢抓我的家人。", "狠")],
         motion="his eyes narrow on the tied men and his fist tightens until the knuckles whiten",
         zh="許硯特寫，火光裡，下顎咬緊，眼裡一道狠光，看著畫外左邊河灘遠處被綁的押解；眼睛瞇起來，拳頭握到指節發白"),
    dict(loc="fire", cam="Close-up, locked", chars=["xuyan"], night="fire", tag="鉤子3",
         comp="close-up of Xu Yan, the hardness leaving his face, his eyes dropping to Qin Shuang asleep on his shoulder at the edge of the frame",
         lines=[("xuyan", "可它也能，", "聲音沉下來"), ("xuyan", "讓很多人死。", "很輕")],
         motion="his fist slowly opens and he lets out a long breath",
         zh="許硯特寫，臉上的狠一點一點退掉，眼睛落到畫邊靠在他肩上睡著的秦霜；拳頭慢慢鬆開，長長吐一口氣"),
    dict(loc="fire", cam="Medium close-up, slow push in", chars=["xuyan"], night="fire", tag="轉折",
         comp="medium close-up of Xu Yan by the fire, his face calm and decided, his eyes back on the empty air in front of him",
         lines=[("xuyan", "封存。", "很定"), ("xuyan", "連我自己都不打開。", "一字一字")],
         motion="he lifts one hand and presses it flat on the empty air, as if closing a lid",
         zh="轉折：許硯中近景，火邊，臉很平靜、下了決定，眼睛回到面前的空中；舉起一隻手掌，平平地按在面前的空氣上，像蓋上一個蓋子"),
    dict(loc="fire", cam="Close-up, locked", chars=["xuyan"], night="fire", tag="轉折",
         comp="close-up of Xu Yan's face, a cold pale blue glint flashing across it from the empty air in front of him and fading",
         lines=[("xitong", "確認封存。", "平板電子音，喀一聲")],
         panel=[("火藥配方：已封存", "task")],
         motion="the blue glint snaps across his face once and fades, and his hand drops back to his knee",
         zh="奇觀（二）：許硯特寫，一道冷冷的淡藍光從面前的空氣閃過他的臉、然後熄掉；藍光「喀」一下掃過臉，熄掉，他的手落回膝上（剪接時疊上一把藍色的鎖）"),
    dict(chapter="先鎖著", loc="fire", cam="Wide shot, locked", chars=["xuyan", "qinshuang", "aling"], act=2, night="fire",
         comp="wide shot of the campfire under the stars, Xu Yan on a flat rock on screen left with Qin Shuang asleep against his shoulder, A-ling sitting across the fire on screen right watching him",
         motion="A-ling sets her stick down across her knees and keeps her eyes on him while sparks drift up between them",
         zh="星空下的篝火全景，許硯在左坐在平石上，秦霜靠在他肩上睡著，阿令在右、火堆另一邊看著他；阿令把柴橫放在膝上，眼睛一直看著他，火星在兩人之間往上飄"),
    dict(loc="fire", cam="Medium close-up, locked", chars=["aling"], night="fire", tag="鉤子4／中段鉤子",
         comp="medium close-up of A-ling across the fire on screen right, her phoenix eyes steady on Xu Yan off screen left",
         lines=[("aling", "你在想什麼？", "很輕")],
         motion="she tilts her head slightly, waiting",
         zh="中段鉤子：阿令中近景在右、火堆另一邊，鳳眼定定看著畫外左邊的許硯；頭微微一歪，等他回答"),
    dict(loc="fire", cam="Close-up, locked", chars=["xuyan"], night="fire", tag="鉤子4",
         comp="close-up of Xu Yan on screen left, his eyes on A-ling off screen right across the fire, his face honest and tired",
         lines=[("xuyan", "能殺很多人的東西。", "很低")],
         motion="he holds her gaze and does not look away",
         zh="許硯特寫在左，隔著火迎上畫外右邊阿令的目光，臉很坦白、很累；看著她，不移開眼睛"),
    dict(loc="fire", cam="Close-up, slow push in", chars=["xuyan"], night="fire", tag="鉤子4",
         comp="close-up of Xu Yan on screen left with Qin Shuang's sleeping head on his shoulder at the edge of the frame, a faint rueful smile, the sparks drifting up past his face, his eyes on A-ling off screen right",
         lines=[("xuyan", "先鎖著。", "淡淡的笑")],
         motion="he gives a small shrug of one shoulder, careful not to wake Qin Shuang",
         zh="許硯特寫在左，一個淡淡的、有點無奈的笑，看著畫外右邊的阿令；輕輕聳一下一邊的肩，小心不吵醒秦霜"),
    dict(loc="fire", cam="Close-up, slow push in", chars=["aling"], act=3, night="fire", tag="顏值鏡頭",
         comp="close-up of A-ling across the fire, the firelight glowing on her porcelain face and in her upturned phoenix eyes, her gaze held on Xu Yan off screen left",
         motion="for the first time she does not look away, and after a long moment the corner of her mouth moves very slightly",
         zh="顏值鏡頭：阿令特寫、火堆另一邊，火光映著白瓷般的臉和上挑的鳳眼，目光定在畫外左邊的許硯身上；她第一次沒有移開視線，看了很久，嘴角很輕地動了一下"),
    dict(loc="fire", cam="Medium close-up, locked", chars=["aling"], night="fire",
         comp="medium close-up of A-ling on screen right, her face cool again, picking up the stick from her knees",
         lines=[("aling", "鎖好。", "很輕，像答應")],
         motion="she lays the stick on the fire and the flames lick up around it",
         zh="阿令中近景在右，臉又回到冷淡，把膝上那根柴拿起來；把柴放進火裡，火舌往上捲"),
    dict(chapter="回柳溪", loc="gate", cam="Wide shot, slow pan right", chars=["xuyan", "tangxiaotang", "qinshuang"], act=3, tag="鉤子5",
         comp="wide shot of the village entrance, villagers in patched cotton crowding both sides of the dirt road beating gongs and drums under the willow hung with red streamers, and coming over the stone arch bridge Xu Yan with Tang Xiaotang in her high-collared peach-pink ruqun, Qin Shuang with the red-tasselled spear and A-ling leading the bay horse",
         motion="the drummers pound their drums and the gongs flash in the sun as the four of them step off the bridge onto the road",
         zh="柳溪村口全景：村民擠在土路兩邊敲鑼打鼓，老柳樹掛滿紅布條；石拱橋上走過來許硯、高領桃粉襦裙的唐小棠、扛著紅纓長槍的秦霜、牽著棗紅馬的阿令；鼓手用力擂鼓、銅鑼在太陽下一閃一閃，四個人從橋上走下土路"),
    dict(loc="gate", cam="Medium close-up, locked", chars=["hanbo"],
         comp="medium close-up of Elder Han at the front of the crowd under the willow, his long white beard, raising his polished bamboo walking staff high, his kind lined face beaming at Xu Yan off screen left",
         lines=[("hanbo", "咱們柳溪，", "蒼老，激動"), ("hanbo", "出了個解元！", "笑得鬍子抖")],
         motion="he shakes the staff over his head and the crowd behind him cheers",
         zh="韓伯中近景，站在柳樹下人群最前面，長長的白鬍子，把磨亮的竹杖高高舉起，滿是皺紋的慈祥的臉笑著看畫外左邊的許硯；把竹杖在頭上搖，後面的人群歡呼"),
    dict(loc="gate", cam="Medium shot, tracking", chars=["xiaohe", "xuyan"], tag="鉤子5",
         comp="medium shot on the dirt road, little Xiaohe in her patched lilac jacket running from screen right with her straw rabbit, Xu Yan on screen left crouching with his arms open",
         lines=[("xiaohe", "哥！", "奶聲奶氣，大喊")],
         motion="she runs the last few steps and throws herself into his arms, and he scoops her up and swings her round once",
         zh="土路中景：補丁淡紫小襖的小禾抱著草編兔子從右邊跑過來，許硯在左蹲下張開雙手；她跑完最後幾步撲進他懷裡，他一把抱起來轉一圈"),
    dict(loc="gate", cam="Two-shot, locked", chars=["xuyan", "xiaohe"],
         comp="two-shot on the road, Xu Yan holding little Xiaohe on his hip on screen left, Xiaohe on screen right with her arms around his neck, her gap-toothed grin",
         lines=[("xiaohe", "阿令姊姊說，", "得意"), ("xiaohe", "你一定會回來！", "笑")],
         motion="she squeezes his neck and bounces on his hip",
         zh="雙人鏡：許硯在左把小禾抱在腰上，小禾在右雙手環著他脖子，缺一顆門牙的大笑；她抱緊他的脖子，在他腰上一蹦一蹦"),
    dict(chapter="作揖", loc="gate", cam="Medium shot, locked", chars=["qianyuanwai"], act=2, tag="鉤子6",
         comp="medium shot of the crowd parting, Qian Yuanwai in his dark gold silk robe being shoved forward out of the villagers by many hands on screen right, his two servants hanging back behind him",
         motion="he stumbles out two steps into the open road, catches his balance and straightens his robe while the villagers laugh",
         zh="人群分開的中景：穿暗金綢袍的錢員外在右被一堆手從村民裡推出來，兩個家丁縮在後面；他踉蹌兩步跌到路中間，站穩，拉一拉袍子，村民哄笑"),
    dict(loc="gate", cam="Medium close-up, slow push in", chars=["qianyuanwai"], tag="鉤子6",
         comp="medium close-up of Qian Yuanwai on screen right, his round face forcing a sickly smile, sweat on his forehead, his small shrewd eyes on Xu Yan off screen left",
         lines=[("qianyuanwai", "解、解元老爺……", "陪笑，結巴")],
         motion="he rubs his ringed hands together and bobs his head",
         zh="錢員外中近景在右，圓臉擠出一個難看的笑，額頭冒汗，小眼睛看著畫外左邊的許硯；戴著金戒指的雙手搓來搓去，點頭哈腰"),
    dict(loc="gate", cam="Medium close-up, locked", chars=["xuyan"],
         comp="medium close-up of Xu Yan on screen left, little Xiaohe set down beside him, an easy smile, his eyes on Qian Yuanwai off screen right",
         lines=[("xuyan", "錢老爺，", "笑"), ("xuyan", "說好的磕頭——", "拖長音")],
         motion="he tilts his head and lets the words hang",
         zh="許硯中近景在左，小禾已經放下站在他旁邊，從容的笑，看著畫外右邊的錢員外；頭一歪，把話停在那裡"),
    dict(loc="gate", cam="Close-up, locked", chars=["qianyuanwai"],
         comp="close-up of Qian Yuanwai on screen right, his face going pale, his knees starting to bend",
         lines=[("qianyuanwai", "我、我……", "快哭了")],
         motion="his knees dip toward the ground and he glances back at the jeering crowd",
         zh="錢員外特寫在右，臉一下子發白，膝蓋開始彎；膝蓋往地上一沉，回頭看一眼起鬨的人群"),
    dict(loc="gate", cam="Close-up, slow push in", chars=["xuyan"],
         comp="close-up of Xu Yan on screen left, waving one hand lightly, a generous smile, his eyes on Qian Yuanwai off screen right",
         lines=[("xuyan", "免了。", "大方"), ("xuyan", "作個揖就好。", "笑")],
         motion="he flicks his hand to say get up, and folds his arms",
         zh="許硯特寫在左，輕輕揮一下手，大方地笑，看著畫外右邊的錢員外；手一揮叫他起來，雙手抱胸"),
    dict(loc="gate", cam="Wide shot, locked", chars=["qianyuanwai", "xuyan"], act=2, tag="鉤子6",
         comp="wide shot of the road under the willow, Qian Yuanwai on screen right bending deep at the waist in a formal bow with his hands clasped, Xu Yan standing on screen left with Xiaohe, the villagers cheering all around",
         motion="he bows low, holds it, and the villagers burst into cheers and a gong crashes",
         zh="柳樹下土路全景：錢員外在右雙手合抱、深深彎腰作揖，許硯帶著小禾站在左，村民圍著歡呼；他一揖到底停住，村民轟地叫好，一聲鑼響（爽點：當眾作揖）"),
    dict(loc="gate", cam="Close-up, locked", chars=["tangxiaotang"],
         comp="close-up of Tang Xiaotang in the crowd on screen right, her high stand-up collar fastened at the throat, her little gold abacus raised, her big round eyes sparkling with glee",
         lines=[("tangxiaotang", "這筆帳，", "甜甜的"), ("tangxiaotang", "總算算完了。", "得意")],
         motion="she flicks the abacus beads with a clack and laughs",
         zh="唐小棠特寫、人群裡在右，高領扣到喉嚨，舉著小金算盤，大圓眼睛開心得發亮；指尖把算盤珠「喀」地一撥，笑出來（接第 41 集「帳要最後才算」）"),
    dict(chapter="畫像", loc="yard", cam="Wide shot, locked", chars=["aling", "tangxiaotang", "xiaohe"], act=2, night="yard", tag="結尾",
         comp="wide shot of the farmhouse yard, the family gathered at the low table under the persimmon tree, A-ling pouring tea from a clay pot on screen left, Tang Xiaotang in her high-collared peach-pink ruqun beside her, little Xiaohe on a stool hugging her straw rabbit",
         motion="A-ling fills a tea bowl and hands it to Xiaohe, who takes it carefully in both hands",
         zh="結尾：許家院子全景，一家人圍坐在柿子樹下的矮桌，阿令在左從陶壺倒茶，高領桃粉襦裙的唐小棠在她旁邊，小禾坐在小凳上抱著草兔子；阿令倒滿一碗茶遞給小禾，小禾雙手小心接住"),
    dict(loc="yard", cam="Medium shot, tracking", chars=["xinchai"], night="yard", tag="結尾",
         comp="medium shot at the broken wooden gate, the courier in a dusty dark blue jacket with a red armband bursting in on screen left, a letter held up in his hand, sweat on his face",
         lines=[("xinchai", "唐小姐！", "喘"), ("xinchai", "京城急信！", "急")],
         motion="he shoulders the gate open, stumbles into the yard and thrusts the letter forward",
         zh="破木門口中景：穿滿是塵土的深藍短褂、紅臂章的信差從左邊衝進來，手上舉著一封信，滿臉是汗；他用肩撞開門，踉蹌進院子，把信往前一遞"),
    dict(loc="yard", cam="Medium close-up, locked", chars=["tangxiaotang"], night="yard", tag="結尾",
         comp="medium close-up of Tang Xiaotang at the table on screen right, her high stand-up collar fastened at the throat, breaking the seal of the letter, her smile fading",
         lines=[("tangxiaotang", "魏少卿……", "唸，愣住")],
         motion="she unfolds the letter and her eyes run down it, slowing",
         zh="唐小棠中近景在右、桌邊，高領扣到喉嚨，掰開信的封口，笑容慢慢收掉；攤開信，眼睛往下讀，越讀越慢"),
    dict(loc="yard", cam="Insert of the letter, locked", act=1, night="yard", tag="結尾",
         comp="insert of the letter held open in two slender hands with peach-pink silk sleeves, columns of faint blurred brush strokes that cannot be read, the fingers stopping halfway down",
         lines=[("tangxiaotang", "帶著一幅畫像，", "聲音低下去")],
         motion="The shot opens directly on this close insert from its very first frame; the fingers stop on one line and press down on it",
         zh="插鏡：兩隻桃粉綢袖的纖手攤開那封信，一列列糊開讀不出的毛筆畫（不寫字），手指停在一半；手指停在某一行上，按住"),
    dict(loc="yard", cam="Close-up, slow push in", chars=["tangxiaotang"], night="yard", tag="結尾",
         comp="close-up of Tang Xiaotang, her high stand-up collar fastened at the throat, her big round eyes lifting from the letter to A-ling off screen left, her face serious",
         lines=[("tangxiaotang", "進了相府。", "停住")],
         motion="she lowers the letter slowly and stops speaking",
         zh="唐小棠特寫，高領扣到喉嚨，大圓眼睛從信上抬起來看畫外左邊的阿令，臉很嚴肅；慢慢放下信，停住不唸了"),
    dict(loc="yard", cam="Insert of the tea bowl in her hand, locked", act=1, night="yard", tag="結尾",
         comp="insert of a slender hand in a grey-white sleeve holding a clay tea bowl above the low table, the tea in it still",
         motion="The shot opens directly on this close insert from its very first frame; the hand jerks once, the bowl tilts and the tea slops against its rim in a shaking ripple",
         zh="插鏡：一隻月白袖子的纖手端著一只陶茶碗在矮桌上方，碗裡的茶是靜的；手猛地一抖，碗一歪，茶撞上碗沿晃出一圈圈波紋"),
    dict(loc="yard", cam="Extreme close-up, locked", chars=["aling"], act=2, night="yard", tag="結尾",
         comp="extreme close-up of A-ling's face, pale and still, her phoenix eyes fixed on the letter in Tang Xiaotang's hands off screen right",
         motion="her lips press together and her eyes do not blink",
         zh="最後一格：阿令大特寫，臉又白又靜，鳳眼釘在畫外右邊唐小棠手上的信；嘴唇抿緊，眼睛一眨不眨"),
]

HEAD = [
    "- 開頭 10 秒：接第 54 集最後一格（秦霜「你常對著那裡笑，那裡有什麼？」、阿令轉頭等、許硯嘴唇剛張開）：許硯看著火「那裡有我想要的。一個家。」（0:00），阿令的好感 59 → 61（0:04），秦霜「這算什麼答案……」靠著他睡著（0:07）——直接回答「他會說出系統的祕密嗎？」：不說，但說的是真話",
    "- 鉤子（站主 10-16 規則）：見 brief.md 的鉤子表",
    "- 顏值鏡頭：s16 阿令在火堆另一邊，火光映著鳳眼，第一次沒有移開視線、嘴角很輕地動了一下（細綱的 glamour_shot）；s28 唐小棠撥算盤笑；是臉與動作，不停在身體",
    "- 爽點：開場 level_up（s02–s06 三位妻子好感都過 60、大獎火藥配方）、中段 face_slap（s22–s27 錢員外被村民推到最前面、當眾作揖）",
    "- 奇觀：細綱寫「面板上大獎箱打開金光暴漲、卷軸只有『火藥』兩字清楚、一把藍色的鎖喀地扣上」；面板與字不由模型畫，所以片段只拍許硯的臉被面前空氣裡的金光照亮（s05）與一道淡藍光閃過（s11），箱子、卷軸與鎖由剪接疊上（overlays 的 task 面板）",
    "- 說話鏡頭：說話的人在畫面上的鏡頭，motion 第一句都是他說這句話；畫外台詞（s32 插鏡上唐小棠的話、系統五句）放在插鏡與臉部特寫上",
    "- H3 寫法：同第 51 集；系統的金光、藍光寫成照在臉上的光，不寫任何面板或字",
    "- 光：s01–s17 夜裡河灘的篝火與星空；s18–s28 柳溪村口晴朗的早上；s29–s35 許家院子傍晚斜斜的暖光",
    "- 軸線：火堆邊許硯在左（秦霜靠在他肩上、更左）、阿令在右；村口石橋在後、許硯一行從橋上走下來，韓伯與錢員外在右、許硯在左；院子矮桌阿令在左、唐小棠在右，信差從左邊的破木門衝進來",
]
FOOT = [
    "- 場景參考：s01–s17 用 `dh-set-hetan-t1`（含 `campfire`，**要畫**）；s18–s28 用 `dh-set-cunkou-t1`（含 `village entrance`，有圖；那張是月夜，本集是早上，靠 prompt 的 bright clear morning）；s29–s35 用 `dh-set-xujia-yuan-t1`（含 `dirt yard`，有圖）。",
    "- 道具：火堆、秦霜靠在他肩上睡著（s03–s15）；系統的金光與藍光（s05、s11）；紅布條、銅鑼、鼓（s18、s26）；韓伯的竹杖；小禾的草編兔子；錢員外的金戒指與兩個家丁；唐小棠的小金算盤；信差的信（s30–s33）；阿令的陶茶碗（s29、s34）。",
    "- 連戲：細綱的地點依序是河灘篝火、柳溪村口、許家院子；從州城回柳溪的路程與押鄧押司回州府都跳過（第 54 集 s28「明早押回州府」交代）。好感：三人都過 60（唐小棠 61、秦霜 66、阿令 61），s04 的面板列出三個數字。火藥配方照設定的規則二只給方法、而且許硯封存，第一季不再打開（大獎留給後面的季）。錢員外作揖收第 41 集的賭約「這次中了，你來磕頭」，許硯把磕頭免了改成作揖（細綱：彎腰作揖）。信是唐萬金在京城的眼線寄的：「魏少卿帶著一幅畫像，進了相府」（第 51 集 s30「帶著一個畫師回京」的下一步）；畫像畫的是誰、他對相府說了什麼，本集不說（第 56 集阿令自己說「畫的是我」，第 58 集才收 s01-t12）。阿令為什麼選了柳溪（第二季 s02-t03）與她的身分都不碰。王二牛、杜鐵本集不出場。第 56 集從阿令把信湊到燈上燒了「畫的是我」接。",
    "- 秒數：`gen-dh.mjs` 自動決定。",
    "- 系統面板不由模型畫：s02、s04 的好感、s06 的大獎、s11 的封存在剪接時疊上（affection、task）。",
    "- 新的參照圖還沒畫：場景 `set-hetan-t1.png`（s01–s17）；村口與院子（s18–s35）的鏡現在就能做。信差是小角色、沒有定妝照（外貌只寫在 video.json）。",
]

BRIEF = """
# 《種田娶妻打天下》第 55 集〈鎖起來〉

## 故事前提

第 54 集收在河灘的火堆旁：秦霜抹掉眼淚，指著許硯眼前的空氣：「你常對著那裡笑。那裡有什麼？」阿令也停下撥火，轉過頭來等他回答。第 55 集從他的回答開始：他看著火，「那裡有我想要的。」「一個家。」（細綱的 hook；他沒說出系統，但這是真話——第二季第 70 集系統的「說謊扣分」從這種地方來。）火堆另一邊的阿令手停住，系統：阿令好感六十一。秦霜嘟囔一句「這算什麼答案……」，靠在他肩上睡著了。

系統接著跳出：「三位妻子好感，」「全數突破六十。」「解鎖大獎。」一道比火光還亮的金光打在他臉上（細綱的奇觀）：「大獎：火藥配方。」許硯握緊拳：「火藥……」他看著河灘遠處被綁的押解：「有了它，」「誰還敢抓我的家人。」再低頭看靠在肩上的秦霜：「可它也能，」「讓很多人死。」（細綱的 conflict。）他把手掌平按在面前的空氣上：「封存。」「連我自己都不打開。」一道淡藍光閃過：「確認封存。」（細綱的 turn。）

阿令隔著火看他很久：「你在想什麼？」（細綱的 mid_hook。）「能殺很多人的東西。」「先鎖著。」她第一次沒有移開視線，嘴角很輕地動了一下（細綱的顏值鏡頭），然後把柴放進火裡：「鎖好。」

回柳溪那天，村口的老柳樹掛滿紅布條，全村敲鑼打鼓。韓伯舉著竹杖：「咱們柳溪，」「出了個解元！」小禾撲進他懷裡：「哥！」「阿令姊姊說，」「你一定會回來！」錢員外被村民推到最前面：「解、解元老爺……」許硯笑：「錢老爺，」「說好的磕頭——」錢員外膝蓋一軟：「我、我……」「免了。」「作個揖就好。」錢員外一揖到底，全村叫好（細綱的 satisfaction：face_slap）。唐小棠撥算盤：「這筆帳，」「總算算完了。」

晚上的院子，阿令在柿子樹下倒茶。信差撞開破木門：「唐小姐！」「京城急信！」唐小棠拆信唸：「魏少卿……」「帶著一幅畫像，」「進了相府。」她停住，抬眼看阿令。阿令手裡的茶碗晃了一下（細綱的 cliffhanger，reveal，「畫像上畫的是誰？」）。

本集細綱：`season-01.json` 第 55 集（110 秒，第一季第六章第五集，調性甜寵＋感人，lead_arc wins）。satisfaction：level_up（s02–s06）、face_slap（s22–s27）。general_payoffs 全部入鏡：三位妻子好感都過 60（s02、s04）；得到大獎火藥配方、許硯選擇封存（s06、s10–s11）；以解元身分回到柳溪、錢員外當眾作揖（s18–s27）。

## 鉤子（站主 10-16：開場、結尾之外中段還要兩三個以上）

| 鉤子 | 鏡 | 內容 |
| --- | --- | --- |
| 【鉤子1】開場 | s01–s03 | 「那裡有我想要的。一個家。」阿令好感 61 |
| 【鉤子2】 | s04–s07 | 「全數突破六十」「解鎖大獎」金光打在臉上；「大獎：火藥配方」 |
| 【鉤子3】 | s08–s09 | 「有了它，誰還敢抓我的家人」「可它也能，讓很多人死」 |
| 轉折 | s10–s11 | 「封存。連我自己都不打開。」「確認封存。」 |
| 【鉤子4】中段鉤子 | s13–s17 | 阿令「你在想什麼？」「能殺很多人的東西。先鎖著。」她第一次沒有移開視線 |
| 【鉤子5】 | s18–s21 | 全村敲鑼迎解元；小禾撲進懷裡 |
| 【鉤子6】 | s22–s28 | 錢員外被推出來「說好的磕頭——」「免了，作個揖就好」 |
| 【結尾】 | s29–s35 | 信差「京城急信」「魏少卿帶著一幅畫像，進了相府」；阿令的茶碗晃了一下 |

## 角色

- 許硯（xuyan）：s01「那裡有我想要的。一個家。」；s04–s06 看系統面板（只拍臉、金光、眼睛）；s07「火藥……」；s08–s09「有了它，誰還敢抓我的家人」「可它也能，讓很多人死」；s10「封存。連我自己都不打開」；s14–s15「能殺很多人的東西。先鎖著」；s20–s21 抱小禾；s24、s26 對錢員外「說好的磕頭——」「免了，作個揖就好」。
- 阿令（aling）：s02 好感 61；s12–s13「你在想什麼？」；s16 顏值鏡頭；s17「鎖好」；s18 牽著棗紅馬回村；s29 倒茶；s34–s35 茶碗晃了一下、臉發白（不說為什麼）。
- 秦霜（qinshuang）：s03「這算什麼答案……」，靠著他睡著；s18 扛著紅纓長槍回村。
- 唐小棠（tangxiaotang）：s18 回村；s28「這筆帳，總算算完了」；s31–s33 拆信唸「魏少卿……帶著一幅畫像，進了相府」。每一個 prompt 都寫 high stand-up collar。
- 韓伯（hanbo）：s19「咱們柳溪，出了個解元！」
- 小禾（xiaohe）：s20「哥！」；s21「阿令姊姊說，你一定會回來！」（第 51 集阿令把她交給韓伯）。
- 錢員外（qianyuanwai）：s22 被村民推出來；s23「解、解元老爺……」；s25「我、我……」；s27 一揖到底。
- 信差（xinchai，小角色，聲音 Puck，外貌只寫在 video.json）：s30「唐小姐！京城急信！」
- 系統（xitong）：s02 阿令好感 61；s04「三位妻子好感，全數突破六十」；s05「解鎖大獎」；s06「大獎：火藥配方」；s11「確認封存」（`overlays.json`）。

## 地點（固定的地點字）

- 河灘篝火（夜）：同第 54 集，`On the pebble riverbank by the north ferry at night, a campfire of driftwood`（`dh-set-hetan-t1`）。
- 柳溪村口（早上）：`At the Liuxi village entrance on a bright clear morning`（`dh-set-cunkou-t1`：老柳樹、長青苔的石拱橋、溪、土路往上通到木屋），加紅布條與敲鑼打鼓的村民。
- 許家院子（傍晚）：`In the small dirt yard of the Xu farmhouse in the late afternoon`（`dh-set-xujia-yuan-t1`），柿子樹下擺了矮桌與小凳。

## 站主觀點

站主 2026-10-16 的要求：女生要火辣漂亮，濃顏系的五官與妝、合身剪裁；不露、不濕身、鏡頭不停在身體部位；每集至少一個顏值鏡頭；結尾收在最高點；不被黃標；每集開場、結尾之外中段再兩三個以上鉤子。本集的顏值鏡頭是 s16（阿令第一次不移開視線）。火藥只是一個名字：沒有任何爆炸、配方內容不出現、許硯封存它（不黃標、也守住系統的代價規則）。系統面板、大獎箱、卷軸、鎖都不由模型畫：prompt 只寫照在臉上的金光與藍光。信不寫字。小禾撲進懷裡、被抱起來轉一圈，安全。

分鏡照 `storyboard-rules.md` 2026-10-28 起的 H3 寫法（同第 51 集）；秒數由 `gen-dh.mjs` 決定；本集沒有靜圖、沒有切素材鏡。角色外觀照 `production/cast.json` 逐字照抄。
"""

_add = {
 4: [dict(loc="fire", cam="Close-up, locked", chars=["aling"], night="fire",
          comp="close-up of A-ling across the fire on screen right, her phoenix eyes narrowing slightly on Xu Yan off screen left as he squints at nothing",
          motion="she lowers the stick and leans forward a little to watch him more closely",
          act=2, zh="阿令特寫在右、火堆另一邊，鳳眼微微瞇起，看著畫外左邊對著空氣瞇眼的許硯；她放下柴，身子往前一點看得更仔細（她看得到他的樣子，看不到面板）")],
 6: [dict(loc="fire", cam="Insert of his hand on his knee, locked", act=1, night="fire",
          comp="insert of a young man's hand in a faded blue-grey sleeve resting on his knee in the firelight, the fingers spread",
          motion="The shot opens directly on this close insert from its very first frame; the hand lifts off the knee and comes down on it again as a hard fist",
          zh="插鏡：火光裡一隻青灰袖子的手放在膝上，手指張開；手指慢慢收攏，握成一個硬拳")],
 7: [dict(loc="fire", cam="Wide shot, locked", act=2, night="fire",
          comp="wide shot down the dark pebble bank away from the campfire, Sergeant Deng and his thugs tied in a row against a driftwood log, their faces sullen in the far edge of the firelight",
          motion="one of the tied thugs tugs at his rope and Sergeant Deng shoves him with his shoulder to stop",
          zh="從篝火往河灘遠處的全景：鄧押司和他的打手被綁成一排靠著一根漂流木，臉在火光的邊緣陰沉沉的；一個打手扯繩子，鄧押司用肩膀撞他一下叫他停（許硯看著的那串人）")],
 8: [dict(loc="fire", cam="Close-up, slow push in", chars=["qinshuang"], act=2, night="fire",
          comp="close-up of Qin Shuang asleep on Xu Yan's shoulder, her tear-stained cheek in the firelight, her lashes resting, the jade pendant held loosely in her hand",
          motion="she stirs in her sleep and presses her cheek closer against his shoulder, her fingers tightening on the jade",
          zh="秦霜特寫，靠在許硯肩上睡著，火光照著有淚痕的臉頰，睫毛垂著，手裡鬆鬆地握著那塊玉；她在睡夢裡動一下，臉頰往他肩上貼緊，握玉的手指收緊")],
 17: [dict(loc="gate", cam="Medium close-up, locked", chars=["qinshuang"],
          comp="medium close-up of Qin Shuang on the road with the red-tasselled spear on her shoulder, looking around at the cheering crowd with her bold brows raised and a wry grin",
          lines=[("qinshuang", "這陣仗，", "挑眉"), ("qinshuang", "比州城還熱鬧。", "笑")],
          motion="she shifts the spear on her shoulder and swings her elbow toward Xu Yan off screen right",
          zh="秦霜中近景，在土路上扛著紅纓長槍，挑著劍眉看周圍歡呼的人群，嘴角一勾；把肩上的槍挪一下，用手肘頂一下畫外右邊的許硯")],
 20: [dict(loc="gate", cam="Two-shot, slow push in", chars=["aling", "xiaohe"],
          comp="two-shot on the road, A-ling on screen left crouching beside the bay horse, little Xiaohe on screen right running from Xu Yan's arms to her",
          lines=[("xiaohe", "阿令姊姊！", "撲過去")],
          motion="Xiaohe throws her arms around A-ling's neck and A-ling, after a moment, lays one hand gently on the little girl's head",
          zh="雙人鏡：土路上，阿令在左蹲在棗紅馬旁，小禾在右從許硯懷裡跑過來撲向她；小禾抱住阿令的脖子，阿令頓了一下，把一隻手輕輕放在她頭上")],
 28: [dict(loc="yard", cam="Medium close-up, locked", chars=["xiaohe"], night="yard",
          comp="medium close-up of little Xiaohe on her stool at the low table, the tea bowl in both hands, her round face tilted up at Xu Yan off screen right",
          lines=[("xiaohe", "哥，", "奶聲奶氣"), ("xiaohe", "解元是什麼？", "好奇")],
          motion="she sips the tea, scrunches her nose and sets the bowl down",
          zh="小禾中近景，坐在矮桌邊的小凳上，雙手捧著茶碗，圓臉仰起來看畫外右邊的許硯；啜一口茶，皺皺鼻子，把碗放下"),
      dict(loc="yard", cam="Medium close-up, slow push in", chars=["xuyan"], night="yard",
          comp="medium close-up of Xu Yan at the low table under the persimmon tree, smiling down at Xiaohe off screen left",
          lines=[("xuyan", "就是以後，", "笑"), ("xuyan", "沒人敢欺負妳。", "摸她的頭")],
          motion="he reaches over and ruffles her hair",
          zh="許硯中近景，坐在柿子樹下的矮桌邊，笑著低頭看畫外左邊的小禾；伸手揉揉她的頭髮")],
}
_new = []
for _i, _x in enumerate(SHOTS):
    _new.append(_x)
    _new += _add.get(_i, [])
SHOTS = _new

SHOTS[3] = {k: v for k, v in SHOTS[3].items() if k != "chapter"}
SHOTS[4] = dict(SHOTS[4], chapter="大獎")

_m = {1:1,2:2,3:3,4:4,5:5,6:7,7:8,8:10,9:12}
_m.update({i: i + 4 for i in range(10, 19)}); _m.update({i: i + 5 for i in range(19, 22)}); _m.update({i: i + 6 for i in range(22, 30)}); _m.update({i: i + 8 for i in range(30, 36)})
import re as _re
_f = lambda t: _re.sub(r"s(\d\d)(?!\d)", lambda m: "s%02d" % _m[int(m.group(1))] if int(m.group(1)) in _m else m.group(0), t)
HEAD = [_f(x) for x in HEAD]
FOOT = [_f(x) for x in FOOT]
BRIEF = _f(BRIEF)
BRIEF = BRIEF.replace("一道比火光還亮的金光打在他臉上（細綱的奇觀）：", "一道比火光還亮的金光打在他臉上（細綱的奇觀），火堆另一邊的阿令瞇起眼看他對著空氣瞇眼：")
BRIEF = BRIEF.replace("許硯握緊拳：「火藥……」他看著河灘遠處被綁的押解：", "許硯低聲：「火藥……」膝上的手握成拳。他看著河灘遠處被綁成一排的押解：")
BRIEF = BRIEF.replace("再低頭看靠在肩上的秦霜：", "再低頭看靠在肩上、在睡夢裡握緊玉佩的秦霜：")
BRIEF = BRIEF.replace("回柳溪那天，村口的老柳樹掛滿紅布條，全村敲鑼打鼓。", "回柳溪那天，村口的老柳樹掛滿紅布條，全村敲鑼打鼓。秦霜扛著槍挑眉：「這陣仗，」「比州城還熱鬧。」")
BRIEF = BRIEF.replace("「你一定會回來！」錢員外", "「你一定會回來！」又撲向阿令：「阿令姊姊！」阿令頓了一下，把手輕輕放在她頭上。錢員外")
BRIEF = BRIEF.replace("晚上的院子，阿令在柿子樹下倒茶。", "傍晚的院子，阿令在柿子樹下倒茶。小禾問：「哥，」「解元是什麼？」許硯揉她的頭：「就是以後，」「沒人敢欺負妳。」")
BRIEF = BRIEF.replace("| 【鉤子2】 | s04–s08 |", "| 【鉤子2】 | s04–s09 |")
HEAD = [x.replace("- 鉤子（站主 10-16 規則）：見 brief.md 的鉤子表", "- 鉤子（站主 10-16 規則）：見 brief.md 的鉤子表；中段鉤子（阿令「你在想什麼？」）在 0:41：火堆戲占前四成，後面是回村與信，兩段各有自己的鉤子；相鄰兩個鉤子最多隔約 12 秒") for x in HEAD]
HEAD.insert(8, "- 檢查：lint 0 錯誤（只剩 sources 那一條警告）、30 項結構檢查全過、分鏡讀取 0 陷阱、gen-dh 43 個鏡都有 dh-set 場景參照（河灘篝火 21、村口 13、院子 9）")
BRIEF = BRIEF.replace("- 阿令（aling）：s02 好感 61；", "- 阿令（aling）：s02 好感 61；s06 看他對著空氣瞇眼；").replace("s22 牽著棗紅馬回村；", "s22 牽著棗紅馬回村；s27 小禾撲過來，她把手放在小禾頭上；")
BRIEF = BRIEF.replace("s22 扛著紅纓長槍回村。", "s22 扛著紅纓長槍回村；s23「這陣仗，比州城還熱鬧」；s13 在睡夢裡握緊玉佩。")
BRIEF = BRIEF.replace("（第 51 集阿令把她交給韓伯）。", "（第 51 集阿令把她交給韓伯）；s27「阿令姊姊！」；s36「哥，解元是什麼？」")
BRIEF = BRIEF.replace("「免了，作個揖就好」。\n- 阿令", "「免了，作個揖就好」；s37「就是以後，沒人敢欺負妳」。\n- 阿令")
