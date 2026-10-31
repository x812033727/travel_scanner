EP = 51
EP_TITLE = "跟他們走"
OUTLINE_SECONDS = 100
TARGET_MINUTES = [1, 2]
TITLE = "衙役衝進來抓她，他按住她的槍：跟他們走，我接妳｜種田娶妻打天下 第51集"
DESCRIPTION = "解元夜，州府衙役一腳踹開客棧房門：「罪臣之女秦霜，私逃軍籍，拿下！」秦霜抄起門邊的紅纓長槍，帶頭的衙役刀出鞘一半。許硯按住她握槍的手：「跟他們走。我接妳。」在這裡動手，她就真的成了逃犯。秦霜看了他三秒，把槍靠回桌邊，自己伸出雙手。系統彈出強制任務：三日內救回秦霜，失敗，秦霜好感清零。當夜，唐小棠拿唐家的銀子買下逮捕公文的抄本，還帶來京城的消息：魏少卿一個月前帶著一個畫師回了京城。天一亮，一匹快馬衝過州城長街，阿令從柳溪連夜趕到。她接過公文抄本，只看了一眼上面的朱印：「這印，是假的。」《種田娶妻打天下》第 51 集。"
THUMB = ("我接妳", "s07")
CHARACTERS = ["xuyan", "qinshuang", "tangxiaotang", "aling", "yayi", "xitong"]
MINOR = {
    "yayi": {"id": "yayi", "name": "衙役", "appearance": "East Asian man of thirty, lean and hard-faced with a thin moustache, a black yamen runner's tunic with red trim, a red sash and a black runner's cap, a saber at his hip", "voice": {"provider": "gemini", "name": "Alnilam", "style": "標準國語，咬字清楚，台北人平常說話的語調；三十歲的州府衙役，男聲、嗓門大、官腔，見了銀子就軟下來"}},
}
MUSIC = "a hard drum hit and a scrape of steel as the door is kicked in, a taut low string held under the spear, a single soft guqin note when his hand covers hers, a slow heartbeat drum for her three-second stare, a cold glassy chime and a falling brass for the forced task, a heavy march of low drums down the stairs, then a sly plucked pipa and woodblock for the silver on the table, a bright comic glockenspiel for the debt, a hushed uneasy reed at the letter from the capital, then galloping drums and a wide swelling dizi through the dawn mist as the horse rears, a cool guqin thread as she walks straight to him, cut to a single high string on the vermilion seal, ancient Chinese rural drama, no vocals"

LOC = {
    "room": "In the upstairs guest room of the prefectural inn at night, dark lattice windows, a round red lacquered table with a white teapot, a painted folding screen and a curtained bed, candlelight inside and orange torchlight pouring in from the open doorway",
    "stairs": "On the wooden staircase of the prefectural inn at night, the front hall below lit by red paper lanterns, square tables with abandoned wine cups, torchlight flickering on the steps",
    "hall": "In the front hall of the prefectural inn late at night, the long dark wooden counter with an abacus and a row of wine jars, empty square tables and benches with abandoned wine cups, red paper lanterns hanging from the beams, the wooden staircase in the background",
    "street": "On the long street of Qingzhou at dawn in thick morning mist, a broad stone-paved avenue between rows of two-storey timber shops with upturned eaves and closed shutters, unlit red lanterns, shop banners without writing hanging still, the grey city wall faint at the far end",
    "door": "On the long street of Qingzhou at dawn in thick morning mist, in front of the open wooden door of an inn, a stone step, closed timber shopfronts with upturned eaves on both sides, unlit red lanterns, pale grey light",
}
LIGHT = {
    "room": "the candle and torchlight stay unchanged",
    "hall": "the red lantern light stays unchanged",
    "dawn": "the grey dawn mist stays unchanged",
}

SHOTS = [
    dict(chapter="跟他們走", loc="room", cam="Insert of the spear at the doorframe, locked", act=1, night="room", tag="鉤子1／開頭",
         comp="insert of the doorframe beside the open door, a red-tasselled spear leaning against the wood, a young woman's hand in a fitted dark brown sleeve reaching into frame for the spear shaft",
         motion="The shot opens directly on this close insert from its very first frame; the hand closes on the shaft and yanks the spear off the doorframe in one fast move, the red tassel swinging out with the momentum",
         zh="接第 50 集：門邊靠著一桿紅纓長槍，一隻深棕袖子的手伸進來一把抄起，紅纓甩出去"),
    dict(loc="room", cam="Wide shot, locked", chars=["qinshuang", "xuyan", "yayi"], night="room", tag="鉤子1",
         comp="wide shot of the guest room, Qin Shuang on screen left in the middle of the room holding the red-tasselled spear level in both hands, Xu Yan in his faded blue-grey robe just behind her shoulder, and in the open doorway on screen right the yamen runner in black with a red sash in front of four more runners holding torches, his saber half drawn from its scabbard",
         lines=[("yayi", "敢拒捕？", "大吼"), ("yayi", "就地格殺！", "刀出鞘一半")],
         motion="he jerks the saber an inch further out as Qin Shuang drops into a low stance",
         zh="客棧上房全景：秦霜在左、房中間雙手平端紅纓長槍，許硯在她肩後；右邊門口，皂衣紅腰帶的衙役帶著四個舉火把的衙役堵住門，刀出鞘一半；衙役再把刀拔出一寸，秦霜重心後移、壓低身子，槍尖轉向門口"),
    dict(loc="room", cam="Insert of the hands on the spear shaft, locked", act=1, night="room", tag="鉤子1",
         comp="insert of the spear shaft gripped hard in a young woman's hand in a fitted dark brown sleeve, and a young man's hand in a faded blue-grey sleeve coming down from above toward her knuckles",
         motion="The shot opens directly on this close insert from its very first frame; the man's hand settles over hers and presses down, and her white-knuckled grip slowly stops pulling",
         zh="插鏡：槍桿上一隻深棕袖子的手握得發白，一隻青灰補丁袖的手從上面蓋下來，按住；她的手停住不再往前推"),
    dict(loc="room", cam="Two-shot, slow push in", chars=["xuyan", "qinshuang"], night="room", tag="鉤子1",
         comp="two-shot, Qin Shuang on screen left gripping the spear with her bold brows drawn down and her eyes on the door, Xu Yan on screen right close beside her, his hand on hers on the shaft, his face turned to her, his voice low and steady",
         lines=[("xuyan", "跟他們走。", "壓低聲音，很穩")],
         motion="he leans in a little closer and his hand tightens on hers once",
         zh="雙人鏡：秦霜在左握著槍、眉頭壓低瞪著門口，許硯在右貼在她身邊，手按著她的手，臉轉向她；他再靠近一點，手按緊一下"),
    dict(loc="room", cam="Close-up, locked", chars=["qinshuang"], night="room",
         comp="close-up of Qin Shuang's face on screen left in the candlelight, her bold straight brows drawn hard together, her almond eyes blazing at Xu Yan off screen right, her sleek high ponytail behind her",
         lines=[("qinshuang", "你說什麼？", "不敢相信，咬牙")],
         motion="she snaps her head round toward him and her jaw sets",
         zh="秦霜特寫在左，燭光下劍眉擰緊，杏眼冒火瞪著畫外右邊的許硯；她把頭一甩轉向他，下巴繃緊"),
    dict(loc="room", cam="Close-up, locked", chars=["xuyan"], night="room",
         comp="close-up of Xu Yan's face on screen right, his brows level, his eyes steady on Qin Shuang off screen left, torchlight from the door on one cheek",
         lines=[("xuyan", "在這裡動手，", "低聲，一字一字"), ("xuyan", "就真成逃犯了。", "很穩")],
         motion="he gives one small shake of the head, his eyes never leaving her",
         zh="許硯特寫在右，眉頭平、眼神定定看著畫外左邊的秦霜，門口的火光照著半邊臉；輕輕搖一下頭，眼睛不離開她"),
    dict(loc="room", cam="Medium close-up, slow push in", chars=["xuyan"], night="room", tag="鉤子2",
         comp="medium close-up of Xu Yan on screen right, his hand still over Qin Shuang's on the spear shaft at the bottom of the frame, his face softening, his eyes on her off screen left",
         lines=[("xuyan", "我接妳。", "很輕，像承諾")],
         motion="after the words he lets out a slow breath and nods once, firm and certain",
         zh="許硯中近景在右，手還按在畫面下緣的槍桿上，臉色柔下來，看著畫外左邊的秦霜；說完慢慢吐一口氣，重重點一下頭"),
    dict(loc="room", cam="Close-up, slow push in", chars=["qinshuang"], act=3, night="room", tag="轉折",
         comp="close-up of Qin Shuang's face on screen left, her blazing eyes fixed on Xu Yan off screen right, her lips pressed tight",
         motion="she holds his gaze for three long seconds, her breath slowing, then her shoulders drop a little and her fingers uncurl from the spear shaft",
         zh="轉折：秦霜特寫在左，冒火的眼睛定在畫外右邊的許硯身上，嘴唇抿緊；她看了他整整三秒，呼吸慢下來，肩膀一沉，手指從槍桿上鬆開"),
    dict(loc="room", cam="Medium shot, locked", chars=["qinshuang"], night="room", tag="轉折",
         comp="medium shot of Qin Shuang on screen left beside the round red lacquered table, the red-tasselled spear in one hand, her chin lifted, facing the open doorway and the torchlight on screen right",
         lines=[("qinshuang", "我自己走。", "冷，抬下巴")],
         motion="she leans the spear on the table with a clack, turns to the door and holds out both wrists",
         zh="秦霜中景在左、紅漆圓桌旁，一手拿著紅纓槍，下巴抬起，對著右邊有火光的門口；她把槍「喀」地靠在桌邊，轉身朝門口，自己伸出雙手"),
    dict(loc="room", cam="Insert of the chain at her wrists, locked", act=1, night="room",
         comp="insert of a young woman's two wrists held out together in fitted dark brown sleeves, a man's hands in black sleeves with red cuffs looping a dull iron chain toward them",
         motion="The shot opens directly on this close insert from its very first frame; the iron chain drops over her wrists and is pulled snug with one jerk, the links swinging and settling",
         zh="插鏡：一雙深棕袖子的手腕併在一起伸出來，一雙皂衣紅袖口的手把一條鐵鏈套上去，用力一拉，鐵環晃一下停住"),
    dict(chapter="押走", loc="room", cam="Close-up, locked", chars=["xuyan"], night="room", tag="鉤子3",
         comp="close-up of Xu Yan's face in the centre of the frame, the torchlit doorway blurred behind him, his eyes lifting to a fixed point in the empty air in front of him",
         lines=[("xitong", "強制任務：三日內救回秦霜。", "平板電子音，叮一聲"), ("xitong", "失敗：秦霜好感清零。", "平板電子音，冷冷的")],
         panel=[("強制任務：三日內救回秦霜", "task"), ("失敗：秦霜好感清零", "penalty")],
         motion="his eyes track sideways across the empty air as if reading, then his jaw clenches and his hand closes into a fist at his side",
         zh="系統面板：許硯特寫在中間，背後是糊開的火光門口，眼睛抬起定在面前的空中；眼睛像在讀字一樣掃過去，下顎一緊、身側的手握成拳"),
    dict(loc="stairs", cam="Wide shot, slow pan left", act=3, chars=["qinshuang"], tag="鉤子3",
         comp="wide shot from the top of the wooden staircase, Qin Shuang walking down the steps upright with her chained wrists in front of her between yamen runners holding torches, guests at the tables below frozen with their wine cups half raised, and at the street door at the far end of the hall a man in an old woven straw hat slipping out into the dark",
         motion="the runners lead her down three steps in weighted strides while the guests below turn their heads one by one, and the straw-hatted man ducks out through the door and is gone; the torchlight and red lantern glow stay unchanged",
         zh="從樓梯頂往下的全景：秦霜戴著鐵鏈、腰背挺直，被舉火把的衙役押著下樓；樓下宴席的客人酒杯舉到一半停住；大堂另一頭的街門，一個戴舊草帽的男人閃身溜出去（不點名）；衙役押著她往下走三階，客人一個個轉頭，草帽人消失在門外"),
    dict(loc="stairs", cam="Medium close-up, locked", chars=["qinshuang"], night="hall",
         comp="medium close-up of Qin Shuang on the staircase on screen left, the chain across her wrists, her head turned back over her shoulder to look up at Xu Yan off screen right at the top of the stairs, her eyes hard and bright",
         lines=[("qinshuang", "許硯。", "回頭，冷"), ("qinshuang", "說話算話。", "一字一字")],
         motion="the chain is tugged from behind and she holds his gaze one beat longer before turning away",
         zh="秦霜中近景在左、樓梯上，鐵鏈橫在手腕上，回頭往上看畫外右邊樓梯頂的許硯，眼神又硬又亮；她在台階上停住，後面的衙役一扯鐵鏈，她多看一拍才轉回去"),
    dict(loc="stairs", cam="Close-up, slow push in", chars=["xuyan"], night="hall",
         comp="close-up of Xu Yan at the top of the staircase on screen right, both hands gripping the wooden railing, his eyes on Qin Shuang off screen left below",
         lines=[("xuyan", "算話。", "低聲，咬牙")],
         motion="his hands squeeze the railing until it creaks, and he nods once to her",
         zh="許硯特寫在右、樓梯頂，雙手抓著木欄杆，眼睛跟著畫外左下的秦霜；手把欄杆捏得吱一聲，朝她點一下頭"),
    dict(chapter="唐家的錢", loc="hall", cam="Medium shot, locked", chars=["tangxiaotang", "yayi"], night="hall", tag="鉤子4",
         comp="medium shot at a square table, Tang Xiaotang in her peach-pink ruqun with its high stand-up collar fastened at the throat sitting on screen left with a sweet smile, setting a shining silver ingot on the table in front of the yamen runner standing on screen right in his black tunic and red sash",
         lines=[("tangxiaotang", "差大哥，", "甜甜的"), ("tangxiaotang", "公文抄一份給我。", "笑著，壓低聲音")],
         motion="she slides the ingot toward him with two fingers and taps it once",
         zh="大堂方桌：高領桃粉襦裙的唐小棠坐在左、笑得很甜，把一錠亮晃晃的銀子放在右邊站著的衙役面前；兩根手指把銀子推過去、點一下"),
    dict(loc="hall", cam="Medium close-up, locked", chars=["yayi"], night="hall",
         comp="medium close-up of the yamen runner on screen right in his black cap and tunic, his eyes sliding down to the silver ingot on the table, one hand hovering above it",
         lines=[("yayi", "這可是州府公文……", "眼睛盯著銀子，裝為難")],
         motion="he glances left and right over his shoulder, wets his lips, and his hand creeps a little closer to the silver",
         zh="衙役中近景在右，眼睛往下溜到桌上的銀子，一隻手懸在上面；他左右回頭看一眼，舔舔嘴唇，手又往銀子挪近一點"),
    dict(loc="hall", cam="Insert of the silver on the table, locked", act=1, night="hall",
         comp="insert of the dark wooden tabletop, one silver ingot already there and a slender hand in a peach-pink silk sleeve setting a second silver ingot down beside it",
         lines=[("tangxiaotang", "再加一錠。", "笑，不慌不忙")],
         motion="The shot opens directly on this close insert from its very first frame; the second ingot comes down with a heavy clack beside the first and the fingers slide both a little forward",
         zh="插鏡：深色桌面上已經有一錠銀子，一隻桃粉綢袖的纖手再放下第二錠，「喀」地一聲，手指把兩錠一起往前推"),
    dict(loc="hall", cam="Medium shot, locked", chars=["yayi"], night="hall",
         comp="medium shot of the yamen runner on screen right leaning over the square table, sweeping the two silver ingots into his sleeve with one hand and pulling a folded sheet of paper from his tunic with the other",
         lines=[("yayi", "天亮前，", "壓低聲音"), ("yayi", "您沒見過我。", "左右看一眼")],
         motion="he tucks the silver away, slaps the paper flat on the table and straightens up",
         zh="衙役中景在右，俯身在方桌上，一手把兩錠銀子掃進袖子，一手從衣襟掏出一張摺好的紙；收好銀子，紙「啪」地壓在桌上，站直往右邊走掉"),
    dict(loc="hall", cam="Two-shot, slow push in", chars=["tangxiaotang", "xuyan"], night="hall",
         comp="two-shot at the square table, Tang Xiaotang in her high-collared peach-pink ruqun on screen left holding up the folded paper between two fingers with a proud grin, Xu Yan sitting on screen right with his elbows on the table, his face still tight",
         lines=[("tangxiaotang", "逮捕公文的抄本，", "得意"), ("tangxiaotang", "唐家的錢買的。", "眨眼")],
         motion="she waves the paper once under his nose and sets it in front of him",
         zh="雙人鏡：高領桃粉襦裙的唐小棠在左，兩根手指夾著那張紙舉起來、得意地笑，許硯在右手肘撐桌、臉還繃著；她把紙在他鼻子前晃一下，放到他面前"),
    dict(loc="hall", cam="Close-up, locked", chars=["xuyan"], night="hall",
         comp="close-up of Xu Yan on screen right, the corner of his mouth lifting for the first time tonight, his eyes on Tang Xiaotang off screen left",
         lines=[("xuyan", "花了多少？", "苦笑")],
         motion="he lets out a short breath of a laugh and rubs the back of his neck",
         zh="許硯特寫在右，今晚第一次嘴角動了一下，看著畫外左邊的唐小棠；短短笑一口氣，摸摸後頸"),
    dict(loc="hall", cam="Close-up, slow push in", chars=["tangxiaotang"], night="hall",
         comp="close-up of Tang Xiaotang on screen left, her high stand-up collar fastened at the throat, her big round eyes sparkling, the small gold abacus raised beside her cheek, looking at Xu Yan off screen right",
         lines=[("tangxiaotang", "記帳上，", "甜"), ("tangxiaotang", "你慢慢還。", "笑出酒窩")],
         motion="she flicks two abacus beads with a fingertip and tilts her head",
         zh="唐小棠特寫在左，高領扣到喉嚨，大圓眼睛亮晶晶，小金算盤舉在臉旁，看著畫外右邊的許硯；指尖撥兩顆算盤珠，歪頭笑出酒窩"),
    dict(loc="hall", cam="Medium close-up, locked", chars=["tangxiaotang"], night="hall", tag="鉤子6",
         comp="medium close-up of Tang Xiaotang on screen left at the table, her high-collared peach-pink ruqun, her smile fading into a serious look, a small sealed letter in her hand, her eyes on Xu Yan off screen right",
         lines=[("tangxiaotang", "還有，", "收起笑，壓低聲音"), ("tangxiaotang", "爹在京城的人來信了。", "正經起來")],
         motion="she draws the letter from her sleeve, glances once toward the staircase, and breaks the wax seal with her thumb",
         zh="唐小棠中近景在左、桌邊，笑容收起來變認真，手裡一封封好的小信，看著畫外右邊的許硯；從袖裡抽出信，往樓梯瞄一眼，拇指掰開封蠟"),
    dict(loc="hall", cam="Insert of the letter, locked", act=1, night="hall", tag="鉤子6",
         comp="insert of a small letter opened flat on the table under the red lantern light, columns of faint blurred brush strokes that cannot be read, a slender finger in a peach-pink silk sleeve running down one column",
         lines=[("tangxiaotang", "魏少卿一個月前，", "低聲唸"), ("tangxiaotang", "帶著一個畫師回京了。", "皺眉")],
         motion="The shot opens directly on this close insert from its very first frame; the finger slides down the column and stops halfway, tapping twice",
         zh="插鏡：紅燈籠光下攤平在桌上的小信，一列列糊開讀不出的毛筆畫（不寫字），一根桃粉綢袖的手指往下滑，停在一半、點兩下"),
    dict(loc="hall", cam="Close-up, slow push in", chars=["xuyan"], night="hall", tag="鉤子6",
         comp="close-up of Xu Yan on screen right, his brows drawing down, his eyes narrowing at the letter on the table below the frame",
         lines=[("xuyan", "畫師？", "一愣"), ("xuyan", "他要畫誰？", "低聲，心裡一沉")],
         motion="he leans forward over the table and his fingers press flat on the letter's edge",
         zh="許硯特寫在右，眉頭往下壓、眼睛瞇起看畫面下方桌上的信；身子往桌上探，手指壓住信紙的邊"),
    dict(chapter="快馬", loc="street", cam="Wide shot, tracking", chars=["aling"], act=2, tag="鉤子5／中段鉤子",
         comp="wide shot down the misty empty long street, A-ling riding a bay horse at full gallop straight toward the frame, leaning low over its neck, the reins in both hands, the hem of her plain grey-white dress and loose strands of her black hair streaming behind her",
         motion="the horse's hooves strike the wet paving stones in heavy beats, mist swirling up around its legs, her body moving with each stride; the pale grey dawn mist stays unchanged",
         zh="中段鉤子／奇觀：晨霧裡空無一人的州城長街全景，阿令騎一匹棗紅馬全速朝鏡頭衝來，俯身貼著馬頸，雙手抓韁，月白粗布裙角和散開的髮絲往後飛；馬蹄重重踩在濕石板上，霧捲起來"),
    dict(loc="door", cam="Medium shot, locked", chars=["aling"], act=2, tag="鉤子5",
         comp="medium shot in front of the inn door, A-ling on the bay horse on screen left hauling back hard on the reins, the horse rearing up on its hind legs, her plain grey-white dress and sleeves flaring",
         motion="the horse rises high on its hind legs with its forelegs pawing the mist while she sits firm with her knees, then it comes down with a heavy thud and stamps once; the pale grey dawn mist stays unchanged",
         zh="客棧門前中景：阿令在左騎著棗紅馬猛勒韁繩，馬人立起來，月白裙袖揚起；馬前蹄在霧裡踢兩下，她夾緊膝蓋坐穩，馬重重落地、跺一下蹄"),
    dict(loc="door", cam="Medium close-up, locked", chars=["xuyan", "tangxiaotang"], night="dawn",
         comp="medium close-up in the open inn doorway on screen right, Xu Yan stepping out over the stone step with dark tired eyes, Tang Xiaotang in her high-collared peach-pink ruqun just behind his shoulder, both looking at the rider off screen left",
         lines=[("xuyan", "阿令？", "不敢相信")],
         motion="he stops on the step, his mouth falling open, and Tang Xiaotang leans out past his shoulder to look",
         zh="右邊開著的客棧門口，許硯跨出石階、眼下一圈黑，高領桃粉襦裙的唐小棠在他肩後，兩人看著畫外左邊的騎馬人；他停在台階上嘴巴張開，唐小棠從他肩後探出頭"),
    dict(loc="door", cam="Medium shot, tracking", chars=["aling"], act=3, tag="顏值鏡頭",
         comp="medium shot of A-ling swinging down from the saddle on screen left, her black hair pinned up with a single plain wooden hairpin, loose strands blown across her cold beautiful face, her phoenix eyes fixed on Xu Yan off screen right",
         motion="she lands lightly on both feet, drops the reins without looking back, and walks straight toward the inn door in long even strides, the wind tugging at her sleeves and the loose strands of hair; the pale grey dawn mist stays unchanged",
         zh="顏值鏡頭：阿令在左翻身下馬，木簪挽起的黑髮被風吹亂幾縷貼在清冷的臉上，鳳眼直直看著畫外右邊的許硯；她輕輕落地，韁繩一丟頭也不回，一步一步直直走向客棧門"),
    dict(loc="door", cam="Close-up, locked", chars=["aling"], night="dawn",
         comp="close-up of A-ling on screen left, a few loose strands of black hair across her cheek, her face cold and pale in the dawn mist, her eyes on Xu Yan off screen right",
         lines=[("aling", "人呢？", "很輕，很冷")],
         motion="she stops right in front of him and tucks the loose strand behind her ear with one finger",
         zh="阿令特寫在左，幾縷黑髮落在臉頰，晨霧裡的臉又冷又白，看著畫外右邊的許硯；她停在他面前，一根手指把那縷頭髮塞到耳後"),
    dict(loc="door", cam="Medium close-up, slow push in", chars=["xuyan"], night="dawn",
         comp="medium close-up of Xu Yan on screen right on the inn step, his face drawn, his eyes on A-ling off screen left",
         lines=[("xuyan", "州牢。", "低"), ("xuyan", "三天內要救出來。", "咬牙")],
         motion="he holds up three fingers and then closes them into a fist",
         zh="許硯中近景在右、客棧台階上，臉色疲憊，看著畫外左邊的阿令；舉起三根手指，再握成拳"),
    dict(loc="door", cam="Close-up, locked", chars=["tangxiaotang"], night="dawn",
         comp="close-up of Tang Xiaotang on screen right in the doorway, her high stand-up collar fastened at the throat, her big round eyes wide, her eyes on A-ling off screen left",
         lines=[("tangxiaotang", "柳溪到這裡，", "嚇一跳"), ("tangxiaotang", "妳騎了一夜？", "瞪大眼")],
         motion="her eyes dart to the sweating horse and back, and she presses one hand to her collar",
         zh="唐小棠特寫在右、門口，高領扣到喉嚨，大圓眼睛睜大，看看畫外左邊的阿令、又看看那匹冒汗的馬；手按一下領口"),
    dict(loc="door", cam="Medium close-up, locked", chars=["aling"], night="dawn",
         comp="medium close-up of A-ling on screen left, brushing the dust off one sleeve, her face calm and cool, her eyes on Tang Xiaotang off screen right",
         lines=[("aling", "鏢局半夜敲門。", "淡淡的"), ("aling", "小禾交給韓伯了。", "很短")],
         motion="she brushes the road dust off her sleeve with two quick strokes",
         zh="阿令中近景在左，拍掉袖子上的灰，臉很平靜很冷，看著畫外右邊的唐小棠；兩下拍掉路上的灰，手放下"),
    dict(loc="door", cam="Two-shot, locked", chars=["tangxiaotang", "aling"], night="dawn", tag="結尾",
         comp="two-shot by the inn step, Tang Xiaotang in her high-collared peach-pink ruqun on screen right holding out the folded paper, A-ling on screen left reaching for it",
         lines=[("tangxiaotang", "這是逮捕公文的抄本。", "遞過去")],
         motion="A-ling takes the paper between two fingers and unfolds it with one shake",
         zh="雙人鏡：客棧台階邊，高領桃粉襦裙的唐小棠在右遞出那張摺紙，阿令在左伸手接；阿令兩根手指夾過來，一抖攤開"),
    dict(loc="door", cam="Insert of the vermilion seal, slow push in", act=2, night="dawn", tag="結尾",
         comp="insert of the unfolded warrant copy held in a slender hand with a grey-white sleeve, columns of faint blurred brush strokes that cannot be read, and at the bottom a square vermilion seal impression of thick curving carved lines",
         motion="The shot opens directly on this close insert from its very first frame; a slender fingertip slides down past the columns and comes to rest on the red seal, pressing on one corner of it",
         zh="插鏡：一隻月白袖子的纖手拿著攤開的公文抄本，一列列糊開讀不出的毛筆畫（不寫字），下方一方粗線條盤曲的朱紅印；指尖往下滑過字列，停在紅印上，按住一角"),
    dict(loc="door", cam="Close-up, slow push in", chars=["aling"], night="dawn", tag="結尾",
         comp="close-up of A-ling's face on screen left, her eyes lowered to the paper below the frame, her long elegant brows drawing slightly together",
         lines=[("aling", "這印，", "很輕")],
         motion="her phoenix eyes narrow on the seal and her lips press into a thin line",
         zh="阿令特寫在左，垂眼看畫面下方的紙，細長的眉微微收攏；鳳眼一瞇盯著印，嘴唇抿成一條線"),
    dict(loc="door", cam="Extreme close-up, locked", chars=["aling"], night="dawn", tag="結尾",
         comp="extreme close-up of A-ling's face, her eyes lifting from the paper to Xu Yan off screen right, cold and certain",
         lines=[("aling", "是假的。", "冷，很篤定")],
         motion="her eyes rise slowly and hold on him without a blink",
         zh="最後一格：阿令大特寫，眼睛從紙上抬起來看畫外右邊的許硯，又冷又篤定；眼睛慢慢抬起、定住，不眨"),
]

HEAD = [
    "- 開頭 10 秒：接第 50 集最後一格（門被踹開、衙役擠滿樓梯「罪臣之女秦霜，拿下！」）：秦霜抄起門邊長槍（0:00），衙役刀出鞘一半「敢拒捕？就地格殺！」（0:01），許硯的手按住她握槍的手（0:05），「跟他們走」（0:06），「你說什麼？」「在這裡動手，就真成逃犯了」（0:08–0:14）——直接回答「解元護得住一個罪臣之女嗎？」：他選了不動手的護法",
    "- 鉤子（站主 10-16 規則）：見下表【鉤子N】；中段鉤子是阿令從晨霧裡騎快馬衝進長街（s24–s26）；結尾收在阿令「這印，」「是假的。」",
    "- 顏值鏡頭：s27 阿令翻身下馬、木簪挽起的黑髮被風吹亂，看都不看旁人直直走向許硯；s20 唐小棠撥算盤笑出酒窩。是臉與動作，不停在身體",
    "- 爽點：前半 reversal（s08–s09 秦霜看了他三秒，自己伸出雙手：客棧裡沒流一滴血，她沒被坐實逃犯）、後半 hidden_power（s15–s19 唐小棠用唐家的銀子買下公文抄本；s31–s34 阿令一眼看出印是假的）",
    "- 說話鏡頭：說話的人在畫面上的鏡頭，motion 第一句都是他說這句話、嘴唇下巴隨每個音節動；畫外台詞（唐小棠在插鏡上唸信、系統兩句）放在插鏡與臉部特寫上，prompt 寫明 off screen",
    "- H3 寫法（storyboard-rules 2026-10-28 節，lessons §2、§6、§7）：motion 寫軌跡、一鏡一事、沒有 camera 字；夜景與晨霧每鏡補光線不變的句子；插鏡 motion 開頭寫 `The shot opens directly on this close insert from its very first frame`（lessons §6：只給場景圖的插鏡會先畫一段空景）；畫外的人不寫局部身體",
    "- 光：s01–s14 夜、燭光加門口的火把；s15–s23 深夜大堂的紅燈籠；s24–s36 灰白的晨霧",
    "- 軸線：上房門在右、秦霜與許硯在左；樓梯從畫面上方往左下走，許硯在樓梯頂（右上），秦霜回頭往右上看；大堂唐小棠在左、衙役在右，許硯坐在她右邊；長街阿令從遠處朝鏡頭衝來，客棧門在右，阿令在左、許硯與唐小棠在右邊門口",
]
FOOT = [
    "- 場景參考：s01–s11 用 `dh-set-kezhan-t1`（含 `upstairs guest room`，州城客棧樓上客房沿用縣城客棧上房，有圖）；s12–s23 用 `dh-set-zhou-kezhan-t1`（含 `prefectural inn`，**要畫**）；s24–s36 用 `dh-set-zhou-jie-t1`（含 `long street of Qingzhou`，**要畫**）。",
    "- 道具：紅纓長槍（s01–s09，靠在桌邊；第 53 集許硯把它拋進囚籠）；鐵鏈（s10–s13）；兩錠銀子與公文抄本（s15–s19，抄本之後在唐小棠手上，s32 交給阿令）；京城來信（s22–s23，字是糊開的筆畫）；棗紅馬（s24–s26）；朱紅印（s33，粗線條，不畫字）。",
    "- 連戲：開場照第 50 集細綱的結尾（客棧二樓、衙役擠滿樓梯、許大郎站在人群最後面）接；許大郎只在 s12 當一個戴舊草帽、從街門溜出去的背影（不點名、不給參照圖）。秦霜被押往州牢（細綱 conflict）；系統的強制任務「三日內救回秦霜」（s11）由第 52–53 集收。京城來信只說魏少卿一個月前帶著一個畫師回京（s01-t12 的 setup），許硯問「他要畫誰？」不回答；第 55 集信差帶來「畫像進了相府」，第 58 集才收。阿令為什麼看得懂州府的印，本集不解釋（第 52 集的 hook：許硯沒問）；她騎夜路來是因為唐小棠用許記的鏢局連夜送信到柳溪，小禾交給韓伯（第 55 集回柳溪時小禾在韓伯身邊）。",
    "- 秒數：`gen-dh.mjs` 自動決定（說話約 3 秒以上或兩拍 6 秒，其他 5 秒）；最長的說話鏡是 s11（系統兩句）。",
    "- 系統面板不由模型畫：s11 的面板文字在剪接時疊上（task、penalty）。",
    "- 新的參照圖還沒畫：`refs-dh/set-zhou-kezhan-t1.png`、`refs-dh/set-zhou-jie-t1.png`；衙役是小角色、沒有定妝照（外貌只寫在 video.json）。",
]

BRIEF = """
# 《種田娶妻打天下》第 51 集〈跟他們走〉

## 故事前提

第 50 集收在州城客棧的解元夜：秦霜剛把玉佩放進許硯手心、說出她爹是秦烈山，門板就被一腳踹開，州府衙役擠滿樓梯：「罪臣之女秦霜，私逃軍籍，拿下！」許大郎站在人群最後面。第 51 集從同一個畫面接下去：秦霜一把抄起門邊的紅纓長槍，帶頭的衙役刀出鞘一半：「敢拒捕？」「就地格殺！」許硯的手從上面蓋住她握槍的手：「跟他們走。」秦霜猛一轉頭：「你說什麼？」許硯：「在這裡動手，」「就真成逃犯了。」「我接妳。」（細綱的 hook。）秦霜看了他整整三秒，手指從槍桿上鬆開，把槍靠回桌邊，自己伸出雙手：「我自己走。」（細綱的 turn。）鐵鏈套上她的手腕，系統彈出：「強制任務：三日內救回秦霜。」「失敗：秦霜好感清零。」衙役押著她下樓，滿堂客人的酒杯停在半空，一個戴舊草帽的人從街門溜出去。秦霜在樓梯上回頭：「許硯。」「說話算話。」他抓著欄杆：「算話。」

當夜的大堂，唐小棠把一錠銀子推到一個衙役面前：「差大哥，」「公文抄一份給我。」衙役眼睛盯著銀子：「這可是州府公文……」第二錠「喀」地落下：「再加一錠。」衙役把銀子掃進袖子、把一張摺紙壓在桌上：「天亮前，」「您沒見過我。」唐小棠把抄本放到許硯面前：「逮捕公文的抄本，」「唐家的錢買的。」許硯今晚第一次笑：「花了多少？」「記帳上，」「你慢慢還。」她收起笑，從袖裡抽出一封信：「爹在京城的人來信了。」「魏少卿一個月前，」「帶著一個畫師回京了。」許硯皺眉：「畫師？」「他要畫誰？」（s01-t12 的 setup：魏少卿回京城對誰說了什麼，第 58 集收。）

天一亮，晨霧裡一匹棗紅馬衝過空無一人的州城長街（細綱的 mid_hook 與奇觀），阿令在客棧門前猛勒韁繩，馬人立起來。許硯跨出門口：「阿令？」她翻身下馬，木簪挽起的黑髮被風吹亂，看都不看旁人，直直走向他（細綱的顏值鏡頭）：「人呢？」「州牢。」「三天內要救出來。」唐小棠瞪大眼：「柳溪到這裡，」「妳騎了一夜？」阿令拍掉袖子的灰：「鏢局半夜敲門。」「小禾交給韓伯了。」唐小棠遞出抄本：「這是逮捕公文的抄本。」阿令一抖攤開，指尖停在下方那方朱印上，鳳眼一瞇：「這印，」——眼睛抬起來看許硯：「是假的。」（細綱的 cliffhanger，reveal，「阿令怎麼一眼看出印是假的？」）

本集細綱：`docs/videos/series-plans/zhong-tian-qu-qi/season-01.json` 第 51 集（100 秒，第一季第六章第一集，調性權謀＋甜寵）。hook 是「跟他們走」「我接妳」（line，0:00–0:19）；mid_hook 是阿令從柳溪連夜騎快馬趕到（s24–s27）；衝突是動手就坐實私逃、不動手秦霜就被押進州牢（s02、s06）；turn 是秦霜看了他三秒、自己伸出雙手（s08–s09），系統彈出強制任務（s11），唐小棠拿唐家的錢買來公文抄本（s15–s19）；cliffhanger 是阿令只看一眼朱印「這印，是假的」（s32–s36）。satisfaction 兩個都入鏡：reversal（s08–s09）、hidden_power（s15–s19、s33–s36）。general_payoffs 全部入鏡：客棧裡沒流一滴血、秦霜沒被坐實逃犯（s08–s13）；唐萬金在京城的眼線來信、魏少卿一個月前帶著一個畫師回京（s22–s24）。setup s01-t12：s22–s24。

## 鉤子（站主 10-16：開場、結尾之外中段還要兩三個以上）

| 鉤子 | 鏡 | 內容 |
| --- | --- | --- |
| 【鉤子1】開場 | s01–s06 | 秦霜抄槍、衙役刀出鞘「就地格殺！」，許硯按住她的手「跟他們走」「在這裡動手，就真成逃犯了」 |
| 【鉤子2】 | s07 | 「我接妳。」（她會聽嗎？） |
| 轉折 | s08–s10 | 秦霜看了他三秒、自己伸出雙手、鐵鏈套上 |
| 【鉤子3】 | s11–s14 | 強制任務「三日內救回秦霜」「失敗：秦霜好感清零」；押下樓時戴草帽的人溜走；「說話算話」 |
| 【鉤子4】 | s15–s21 | 唐小棠用銀子買公文抄本、「記帳上，你慢慢還」 |
| 【鉤子5】 | s22–s24 | 京城來信：魏少卿帶著一個畫師回京（他要畫誰？） |
| 【鉤子6】中段鉤子 | s25–s30 | 晨霧裡快馬衝進長街、馬人立，阿令連夜從柳溪趕到「人呢？」 |
| 【結尾】 | s32–s36 | 抄本上的朱印，「這印，」「是假的。」（她怎麼一眼看出來？） |

## 角色

- 許硯（xuyan）：s02 在秦霜肩後；s03–s07 按住她的手「跟他們走」「在這裡動手，就真成逃犯了」「我接妳」；s11 看強制任務面板（只拍臉與眼睛）；s14 樓梯頂「算話」；s19「花了多少？」；s23「畫師？他要畫誰？」；s26「阿令？」；s29「州牢。三天內要救出來。」
- 秦霜（qinshuang）：s01–s02 抄槍、壓低身子；s05「你說什麼？」；s08 看了他三秒、手鬆開（細綱的 turn）；s09「我自己走」、自己伸出雙手；s12–s13 戴鐵鏈下樓、回頭「許硯。說話算話。」本集之後她在州牢裡，第 53 集才再出場。
- 唐小棠（tangxiaotang）：s15–s18 用兩錠銀子買公文抄本；s19「逮捕公文的抄本，唐家的錢買的」；s21「記帳上，你慢慢還」；s22–s23 唸京城來信；s27–s30 客棧門口；s32 把抄本交給阿令。她出現的每一個 prompt 都寫 high stand-up collar。
- 阿令（aling）：s25–s27 晨霧裡騎快馬衝進長街、勒馬、翻身下馬（中段鉤子、顏值鏡頭）；s28「人呢？」；s31「鏢局半夜敲門。小禾交給韓伯了。」；s33–s36 看朱印「這印，是假的。」為什麼看得出來本集不說。
- 衙役（yayi，小角色，聲音 Alnilam，外貌只寫在 video.json）：s02「敢拒捕？就地格殺！」；s16–s18 收銀子賣抄本。押秦霜的其他衙役只寫在 prompt 裡（runners）。
- 系統（xitong）：s11 強制任務與懲罰（設定的規則三：強制任務失敗會被罰），面板文字在 `overlays.json`。
- 許大郎：只在 s12 當一個戴舊草帽、從大堂街門溜出去的背影，不點名、不列 characters、沒有台詞（第 50 集細綱：他把秦霜賣給了魏家）。

## 地點（固定的地點字）

- 州城客棧樓上客房（夜）：`In the upstairs guest room of the prefectural inn at night`（s01–s11，`dh-set-kezhan-t1`：格子窗、紅漆圓桌與白茶壺、屏風、帳子床），燭光加門口的火把。
- 州城客棧樓梯與大堂（夜）：`On the wooden staircase of the prefectural inn at night`、`In the front hall of the prefectural inn late at night`（s12–s23，`dh-set-zhou-kezhan-t1`）。
- 州城長街與客棧門口（清晨晨霧）：`On the long street of Qingzhou at dawn in thick morning mist`（s24–s36，`dh-set-zhou-jie-t1`）；客棧門口的鏡頭也以這句開頭，不寫 `prefectural inn`，才不會被客棧大堂搶走。

## 站主觀點

站主 2026-10-16 的要求：女生要火辣漂亮，濃顏系的五官與妝、合身剪裁；不露、不濕身、鏡頭不停在身體部位；每集至少一個顏值鏡頭；結尾收在最高點；不被黃標；每集開場、結尾之外中段再兩三個以上鉤子。本集的顏值鏡頭是 s27（阿令翻身下馬、被風吹亂的黑髮、直直走向許硯）與 s21（唐小棠撥算盤笑出酒窩）。沒有任何人受傷：刀只出鞘一半、槍沒有刺出去，鐵鏈只拍手腕的插鏡。系統面板不由模型畫，prompt 裡沒有面板、文字或 UI。公文、來信與朱印都寫成「糊開讀不出的筆畫」「粗線條盤曲的朱紅印」，字由台詞說出來（gen-dh 的首格提示詞固定有 No text, no letters）。

分鏡照 `storyboard-rules.md` 2026-10-28 起的 H3 寫法，片段走 H3 Ref2VA（`production/colab/ref2manifest.mjs`），每鏡 prompt 的構圖段寫清楚景別、誰在左右、手上道具；表情用正面的字；說話的人在畫面上時 motion 第一句寫他說這句話；motion 寫軌跡、一鏡一事；運鏡只在 `camera`；秒數由 `gen-dh.mjs` 決定，`video.json` 不寫 buy_seconds。本集沒有靜圖、沒有切素材鏡。橫式 16:9，3D 國漫（gen-dh.mjs）；角色外觀照 `production/cast.json` 逐字照抄。
"""

# --- reorder (mid hook earlier: the letter moves to the inn door after A-ling arrives) ---
_S = SHOTS
_S[19] = dict(_S[19], lines=[("xuyan", "好，", "笑出來"), ("xuyan", "我還。", "認真")],
              motion="he lets out a short breath of a laugh, rubs the back of his neck and nods",
              zh="許硯特寫在右，今晚第一次笑出來，看著畫外左邊的唐小棠；短短笑一口氣，摸摸後頸，點頭")
_S[20] = dict(_S[20], zh="唐小棠特寫在左，高領扣到喉嚨，大圓眼睛亮晶晶，小金算盤舉在臉旁，看著畫外右邊的許硯；指尖撥兩顆算盤珠，歪頭笑出酒窩")
_S[21] = dict(_S[21], chapter="朱印", loc="door", night="dawn",
              comp="medium close-up of Tang Xiaotang in the inn doorway on screen right, her high-collared peach-pink ruqun, her smile gone serious, a small sealed letter in her hand, her eyes on Xu Yan off screen left",
              motion="she draws the letter from her sleeve and breaks the seal with her thumb",
              zh="唐小棠中近景在右、客棧門口，高領桃粉襦裙，笑容收起來變認真，手裡一封封好的小信，看著畫外左邊的許硯；從袖裡抽出信，往霧裡的街上瞄一眼，拇指掰開封蠟")
_S[22] = dict(_S[22], loc="door", night="dawn",
              comp="insert of a small letter held open in two slender hands with peach-pink silk sleeves, columns of faint blurred brush strokes that cannot be read, one fingertip running down a column in the grey dawn light",
              zh="插鏡：兩隻桃粉綢袖的纖手攤開一封小信，一列列糊開讀不出的毛筆畫（不寫字），晨光裡一根手指往下滑，停在一半、點兩下")
_S[23] = dict(_S[23], loc="door", night="dawn", cam="Two-shot, slow push in", chars=["xuyan", "aling"],
              comp="two-shot by the inn step, Xu Yan on screen right with his brows drawing down and his eyes narrowing toward Tang Xiaotang off screen right, A-ling on screen left beside him, her cold face turning toward the letter",
              motion="he leans toward the letter, and beside him A-ling's hand stops halfway up to her sleeve and stays there",
              zh="雙人鏡：客棧台階邊，許硯在右眉頭壓低、眼睛瞇起看畫外唐小棠手上的信，阿令在左站在他旁邊，冷冷的臉轉向那封信；他往信探過去，阿令抬到袖口的手停在半空不動（第 55 集「茶碗晃了一下」的前一拍）")
_S[13] = dict(_S[13], zh=_S[13]["zh"])
SHOTS = _S[:15] + [_S[16], _S[17], _S[18], _S[20], _S[19]] + _S[24:32] + [_S[21], _S[22], _S[23]] + _S[32:]

HEAD = [
    "- 開頭 10 秒：接第 50 集最後一格（門被踹開、衙役擠滿樓梯「罪臣之女秦霜，拿下！」）：秦霜抄起門邊長槍（0:00），衙役刀出鞘一半「敢拒捕？就地格殺！」（0:01），許硯的手按住她握槍的手（0:04），「跟他們走」（0:05），「你說什麼？」（0:06），「在這裡動手，就真成逃犯了」（0:08）——直接回答第 50 集的「解元護得住一個罪臣之女嗎？」：他選了不動手的護法",
    "- 鉤子（站主 10-16 規則）：【鉤子1】s01–s06 0:00、【鉤子2】s07 0:12、轉折 s08–s10 0:14、【鉤子3】s11–s14 0:20、【鉤子4】s15–s20 0:33、【鉤子5 中段】s21–s28 0:52、【鉤子6】s29–s31 1:13、【結尾】s32–s35 1:25–1:35；相鄰兩個鉤子最多隔 19 秒",
    "- 顏值鏡頭：s24 阿令翻身下馬、木簪挽起的黑髮被風吹亂，看都不看旁人直直走向許硯；s19 唐小棠撥算盤笑出酒窩。是臉與動作，不停在身體",
    "- 爽點：前半 reversal（s08–s09 秦霜看了他三秒，自己伸出雙手：客棧裡沒流一滴血，她沒被坐實逃犯）、後半 hidden_power（s15–s18 唐小棠用唐家的銀子買下公文抄本；s33–s35 阿令一眼看出印是假的）",
    "- 說話鏡頭：說話的人在畫面上的鏡頭，motion 第一句都是他說這句話、嘴唇下巴隨每個音節動；畫外台詞（s16、s30 唐小棠在插鏡上、s11 系統兩句）放在插鏡與臉部特寫上，prompt 寫明 off screen",
    "- H3 寫法（storyboard-rules 2026-10-28 節，lessons §2、§6、§7）：motion 寫軌跡、一鏡一事、沒有 camera 字；夜景與晨霧每鏡補光線不變的句子；插鏡 motion 開頭寫 `The shot opens directly on this close insert from its very first frame`（lessons §6：只給場景圖的插鏡會先畫一段空景）；畫外的人不寫局部身體",
    "- 檢查：lint 0 錯誤（只剩 sources 那一條警告）、30 項結構檢查全過、分鏡讀取 0 陷阱、gen-dh 35 個鏡都有 dh-set 場景參照（上房 11、客棧大堂與樓梯 9、長街 15）、沒有鏡頭被剝掉 camera 子句",
    "- 光：s01–s11 夜、燭光加門口的火把；s12–s20 深夜樓梯與大堂的紅燈籠；s21–s35 灰白的晨霧",
    "- 軸線：上房門在右、秦霜與許硯在左；樓梯從畫面上方往左下走，許硯在樓梯頂（右上），秦霜回頭往右上看；大堂唐小棠在左、衙役在右，許硯坐在她右邊；長街阿令從遠處朝鏡頭衝來，客棧門在右，阿令在左、許硯與唐小棠在右邊門口",
]
FOOT = [
    "- 場景參考：s01–s11 用 `dh-set-kezhan-t1`（含 `upstairs guest room`，州城客棧樓上客房沿用縣城客棧上房，有圖）；s12–s20 用 `dh-set-zhou-kezhan-t1`（含 `prefectural inn`，**要畫**）；s21–s35 用 `dh-set-zhou-jie-t1`（含 `long street of Qingzhou`，**要畫**；客棧門口的鏡頭也寫長街這句，不寫 prefectural inn）。",
    "- 道具：紅纓長槍（s01–s09，靠在桌邊；第 53 集許硯把它拋進囚籠）；鐵鏈（s10–s13）；兩錠銀子與公文抄本（s15–s18，抄本之後在唐小棠手上，s32 交給阿令）；京城來信（s29–s30，字是糊開的筆畫）；棗紅馬（s21–s24）；朱紅印（s33，粗線條，不畫字）。",
    "- 連戲：開場照第 50 集細綱的結尾（客棧二樓、衙役擠滿樓梯、許大郎站在人群最後面）接；許大郎只在 s12 當一個戴舊草帽、從街門溜出去的背影（不點名、不給參照圖）。秦霜被押往州牢（細綱 conflict）；系統的強制任務「三日內救回秦霜」（s11）由第 52–53 集收。京城來信只說魏少卿一個月前帶著一個畫師回京（s01-t12 的 setup），許硯問「他要畫誰？」不回答；s31 阿令抬到袖口的手停在半空，接第 55 集「畫像進了相府」時她手裡的茶碗晃了一下，第 58 集才收。阿令為什麼看得懂州府的印，本集不解釋（第 52 集的 hook：許硯沒問）；她連夜騎來是因為唐小棠用許記的鏢局送信到柳溪，小禾交給韓伯（第 55 集回柳溪時小禾在韓伯身邊）。第 52 集從阿令指著印文「真印的『州』字，這一筆是斷的」接。",
    "- 秒數：`gen-dh.mjs` 自動決定，本集每鏡都是兩拍動作或帶光線句，35 支都是 6 秒；最長的說話鏡是 s11（系統兩句，約 5.9 秒）。",
    "- 系統面板不由模型畫：s11 的面板文字在剪接時疊上（task、penalty）。",
    "- 新的參照圖還沒畫：`refs-dh/set-zhou-kezhan-t1.png`（s12–s20）、`refs-dh/set-zhou-jie-t1.png`（s21–s35）；畫好之前 `ref2manifest.mjs` 列出 24 鏡缺圖，只有 s01–s11 這 11 鏡現在就能做。衙役是小角色、沒有定妝照（外貌只寫在 video.json）。",
]
BRIEF = BRIEF.replace("""當夜的大堂，唐小棠把一錠銀子推到一個衙役面前：「差大哥，」「公文抄一份給我。」衙役眼睛盯著銀子：「這可是州府公文……」第二錠「喀」地落下：「再加一錠。」衙役把銀子掃進袖子、把一張摺紙壓在桌上：「天亮前，」「您沒見過我。」唐小棠把抄本放到許硯面前：「逮捕公文的抄本，」「唐家的錢買的。」許硯今晚第一次笑：「花了多少？」「記帳上，」「你慢慢還。」她收起笑，從袖裡抽出一封信：「爹在京城的人來信了。」「魏少卿一個月前，」「帶著一個畫師回京了。」許硯皺眉：「畫師？」「他要畫誰？」（s01-t12 的 setup：魏少卿回京城對誰說了什麼，第 58 集收。）

天一亮，晨霧裡一匹棗紅馬衝過空無一人的州城長街（細綱的 mid_hook 與奇觀），阿令在客棧門前猛勒韁繩，馬人立起來。許硯跨出門口：「阿令？」她翻身下馬，木簪挽起的黑髮被風吹亂，看都不看旁人，直直走向他（細綱的顏值鏡頭）：「人呢？」「州牢。」「三天內要救出來。」唐小棠瞪大眼：「柳溪到這裡，」「妳騎了一夜？」阿令拍掉袖子的灰：「鏢局半夜敲門。」「小禾交給韓伯了。」唐小棠遞出抄本：「這是逮捕公文的抄本。」""",
"""當夜的大堂，唐小棠把一錠銀子推到衙役面前：「差大哥，」「公文抄一份給我。」第二錠「喀」地落下：「再加一錠。」衙役把銀子掃進袖子、把一張摺紙壓在桌上：「天亮前，」「您沒見過我。」唐小棠把抄本放到許硯面前：「逮捕公文的抄本，」「唐家的錢買的。」她撥兩顆算盤珠：「記帳上，」「你慢慢還。」許硯今晚第一次笑出來：「好，」「我還。」

天一亮，晨霧裡一匹棗紅馬衝過空無一人的州城長街（細綱的 mid_hook 與奇觀，0:52），阿令在客棧門前猛勒韁繩，馬人立起來。許硯跨出門口：「阿令？」她翻身下馬，木簪挽起的黑髮被風吹亂，看都不看旁人，直直走向他（細綱的顏值鏡頭）：「人呢？」「州牢。」「三天內要救出來。」唐小棠瞪大眼：「柳溪到這裡，」「妳騎了一夜？」阿令拍掉袖子的灰：「鏢局半夜敲門。」「小禾交給韓伯了。」唐小棠收起笑，從袖裡抽出一封信：「還有，」「爹在京城的人來信了。」「魏少卿一個月前，」「帶著一個畫師回京了。」許硯皺眉：「畫師？」「他要畫誰？」站在他旁邊的阿令，抬到袖口的手停在半空（s01-t12 的 setup：魏少卿回京城對誰說了什麼，第 58 集收）。唐小棠遞出抄本：「這是逮捕公文的抄本。」""")
BRIEF = BRIEF.replace("hook 是「跟他們走」「我接妳」（line，0:00–0:19）；mid_hook 是阿令從柳溪連夜騎快馬趕到（s24–s27）；衝突是動手就坐實私逃、不動手秦霜就被押進州牢（s02、s06）；turn 是秦霜看了他三秒、自己伸出雙手（s08–s09），系統彈出強制任務（s11），唐小棠拿唐家的錢買來公文抄本（s15–s19）；cliffhanger 是阿令只看一眼朱印「這印，是假的」（s32–s36）。satisfaction 兩個都入鏡：reversal（s08–s09）、hidden_power（s15–s19、s33–s36）。general_payoffs 全部入鏡：客棧裡沒流一滴血、秦霜沒被坐實逃犯（s08–s13）；唐萬金在京城的眼線來信、魏少卿一個月前帶著一個畫師回京（s22–s24）。setup s01-t12：s22–s24。",
 "hook 是「跟他們走」「我接妳」（line，0:00–0:14）；mid_hook 是阿令從柳溪連夜騎快馬趕到（s21–s24，0:52–1:02）；衝突是動手就坐實私逃、不動手秦霜就被押進州牢（s02、s06）；turn 是秦霜看了他三秒、自己伸出雙手（s08–s09），系統彈出強制任務（s11），唐小棠拿唐家的錢買來公文抄本（s15–s18）；cliffhanger 是阿令只看一眼朱印「這印，是假的」（s32–s35，reveal）。satisfaction 兩個都入鏡：reversal（s08–s09）、hidden_power（s15–s18、s33–s35）。general_payoffs 全部入鏡：客棧裡沒流一滴血、秦霜沒被坐實逃犯（s08–s13）；唐萬金在京城的眼線來信、魏少卿一個月前帶著一個畫師回京（s29–s31）。setup s01-t12：s29–s31。")
BRIEF = BRIEF.replace("""| 【鉤子4】 | s15–s21 | 唐小棠用銀子買公文抄本、「記帳上，你慢慢還」 |
| 【鉤子5】 | s22–s24 | 京城來信：魏少卿帶著一個畫師回京（他要畫誰？） |
| 【鉤子6】中段鉤子 | s25–s30 | 晨霧裡快馬衝進長街、馬人立，阿令連夜從柳溪趕到「人呢？」 |
| 【結尾】 | s32–s36 | 抄本上的朱印，「這印，」「是假的。」（她怎麼一眼看出來？） |""",
"""| 【鉤子4】 | s15–s20 | 唐小棠用銀子買公文抄本、「記帳上，你慢慢還」 |
| 【鉤子5】中段鉤子 | s21–s28 | 晨霧裡快馬衝進長街、馬人立，阿令連夜從柳溪趕到「人呢？」 |
| 【鉤子6】 | s29–s31 | 京城來信：魏少卿帶著一個畫師回京（他要畫誰？）；阿令的手停在半空 |
| 【結尾】 | s32–s35 | 抄本上的朱印，「這印，」「是假的。」（她怎麼一眼看出來？） |""")
BRIEF = BRIEF.replace("s14 樓梯頂「算話」；s19「花了多少？」；s23「畫師？他要畫誰？」；s26「阿令？」；s29「州牢。三天內要救出來。」",
 "s14 樓梯頂「算話」；s20「好，我還」；s23「阿令？」；s26「州牢。三天內要救出來。」；s31「畫師？他要畫誰？」")
BRIEF = BRIEF.replace("s15–s18 用兩錠銀子買公文抄本；s19「逮捕公文的抄本，唐家的錢買的」；s21「記帳上，你慢慢還」；s22–s23 唸京城來信；s27–s30 客棧門口；s32 把抄本交給阿令。",
 "s15–s17 用兩錠銀子買公文抄本；s18「逮捕公文的抄本，唐家的錢買的」；s19「記帳上，你慢慢還」；s23、s27 客棧門口；s29–s30 唸京城來信；s32 把抄本交給阿令。")
BRIEF = BRIEF.replace("s25–s27 晨霧裡騎快馬衝進長街、勒馬、翻身下馬（中段鉤子、顏值鏡頭）；s28「人呢？」；s31「鏢局半夜敲門。小禾交給韓伯了。」；s33–s36 看朱印「這印，是假的。」",
 "s21–s24 晨霧裡騎快馬衝進長街、勒馬、翻身下馬（中段鉤子、顏值鏡頭）；s25「人呢？」；s28「鏢局半夜敲門。小禾交給韓伯了。」；s31 聽到「畫師」手停在半空；s33–s35 看朱印「這印，是假的。」")
BRIEF = BRIEF.replace("s02「敢拒捕？就地格殺！」；s16–s18 收銀子賣抄本。", "s02「敢拒捕？就地格殺！」；s15–s17 收銀子賣抄本。")
BRIEF = BRIEF.replace("本集的顏值鏡頭是 s27（阿令翻身下馬、被風吹亂的黑髮、直直走向許硯）與 s21（唐小棠撥算盤笑出酒窩）", "本集的顏值鏡頭是 s24（阿令翻身下馬、被風吹亂的黑髮、直直走向許硯）與 s19（唐小棠撥算盤笑出酒窩）")
BRIEF = BRIEF.replace("（s01–s11，`dh-set-kezhan-t1`", "（s01–s11，`dh-set-kezhan-t1`").replace("（s12–s23，`dh-set-zhou-kezhan-t1`）", "（s12–s20，`dh-set-zhou-kezhan-t1`）").replace("（s24–s36，`dh-set-zhou-jie-t1`）", "（s21–s35，`dh-set-zhou-jie-t1`）")
