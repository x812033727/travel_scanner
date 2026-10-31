NUM = 50
TITLE = "拿下秦霜"
TARGET_MINUTES = [2, 3]
YT_TITLE = "退婚人家跪著來賠罪，解元慶功宴上衙役卻衝進來抓她｜種田娶妻打天下 第50集"
THUMB = ("拿下\n秦霜", "s48")
CHARS = ["zhouyuanwai", "xuyan", "qinshuang", "tangxiaotang", "xudalang", "chengshanzhang", "zhanggui", "yayi", "xitong"]
MINOR = {
    "zhanggui": {
        "id": "zhanggui", "name": "客棧掌櫃",
        "appearance": "East Asian man of forty-five, thin with a pinched face and a wispy moustache, a grey-brown cotton robe with black over-sleeves and a black skullcap, standing behind an inn counter",
        "voice": {"provider": "gemini", "name": "Iapetus", "style": "標準國語，咬字清楚，台北人平常說話的語調；四十五歲的客棧掌櫃，男聲、油滑、報價時嗓門拔高，被拆穿就陪笑"},
    },
    "yayi": {
        "id": "yayi", "name": "衙役",
        "appearance": "East Asian man of thirty-five, burly with a hard square face and a short black beard, a black yamen runner's uniform with a red sash and a black cap, a coiled iron chain at his belt, a burning pine torch in one hand",
        "voice": {"provider": "gemini", "name": "Alnilam", "style": "標準國語，咬字清楚，台北人平常說話的語調；三十五歲的州府衙役頭，男聲、粗聲大嗓、官腔十足、吼著下令"},
    },
}

DOOR = ("At the open front door of the prefectural inn in Qingzhou at dusk, the wide doorway hung with red silk for the celebration, "
        "red paper lanterns just lit along the eaves, three stone steps down to the street, the warm glow of the busy hall inside")
HALL = ("In the front hall of the prefectural inn in Qingzhou on a festive night, every red paper lantern lit, round banquet tables "
        "crowded with guests, wine cups and dishes, the long dark wooden counter on screen right, the wooden staircase up to the guest "
        "rooms on screen left")
ROOM = ("In the upstairs guest room of the prefectural inn at night, a plain wooden room lit by one small oil lamp on a low table, a "
        "paper window glowing cold blue with moonlight, a wooden bed with a blue curtain at the back, a long iron-tipped spear leaning "
        "against the wall beside the door on screen left")
QS = "Qin Shuang with a wide woven bamboo douli hat pulled low over her eyes, only her clean-lined jaw and pressed red lips showing under the brim"
LAMP = "the warm oil-lamp glow and the cold blue moonlight at the window stay unchanged"

SHOTS = [
    # ---------------- 跪
    dict(ch="跪", tag="鉤子1／開頭", cam="Medium close-up, locked", set=DOOR, chars=["qinshuang"],
         lines=[("qinshuang", "許硯，", "停下腳步"), ("qinshuang", "我……", "話到嘴邊")],
         prompt=f"medium close-up of {QS}, on screen right at the foot of the inn steps in the dusk, the red silk of the doorway behind her, "
                f"her face turned toward Xu Yan off screen left",
         motion="she stops on the bottom step and lifts one hand toward the brim of her hat, about to push it back",
         zh="接第 49 集：戴斗笠的秦霜中近景在右、客棧台階下，黃昏，背後是門口掛的紅綢，臉朝畫外左邊的許硯；她在最下面一級台階停住，一隻手抬到帽簷，正要把斗笠推開"),
    dict(tag="鉤子1", act=3, cam="Wide shot, slow push in", set=DOOR, chars=["zhouyuanwai", "xuyan", "qinshuang"],
         prompt=f"wide shot of the inn doorway, Zhou Yuanwai in his soy-brown longevity silk robe kneeling on the top step in the middle "
                f"with his daughter and four servants kneeling in a row beside him, red lacquered gift boxes held up in their hands, Xu Yan "
                f"in his blue-grey robe with the red silk flower still on his chest stopping short on screen left, {QS}, on screen right",
         motion="the whole row bows forward together until their foreheads nearly touch the step, the gift boxes raised high over their heads",
         zh="客棧門口的全景：周員外穿醬色團壽綢袍跪在最上面一級台階正中，女兒和四個家丁在他旁邊跪成一排，手上高舉紅漆禮盒；許硯胸前還掛著紅綢花，在左邊猛地停住，戴斗笠的秦霜在右；整排人一起往前拜，額頭快碰到台階，禮盒舉過頭頂（無台詞）"),
    dict(tag="鉤子1／爽點", cam="Medium close-up, low angle, locked", set=DOOR, chars=["zhouyuanwai"],
         lines=[("zhouyuanwai", "解元老爺，", "諂媚，聲音發抖"), ("zhouyuanwai", "是我們瞎了眼！", "磕頭")],
         prompt="medium close-up from a low angle of Zhou Yuanwai kneeling on the top step on screen right, his long narrow face red with "
                "shame and a fawning smile, a red lacquered gift box held up in both hands, his eyes on Xu Yan off screen left",
         motion="he lifts the gift box higher and bobs his head down twice in quick bows",
         zh="【鉤子1／爽點】低角度：周員外中近景在右、跪在最上面一級台階，長臉羞紅、擠出一個諂媚的笑，雙手舉著紅漆禮盒，看著畫外左邊的許硯；禮盒再舉高，連著點頭鞠兩下"),
    dict(cam="Close-up, locked", set=DOOR, chars=["xuyan"],
         lines=[("xuyan", "……員外？", "愣住")],
         prompt="close-up of Xu Yan's face on screen left in the dusk lantern light, his brows shooting up and his mouth half open, the red "
                "silk flower at the bottom of the frame, his eyes on Zhou Yuanwai off screen right",
         motion="he blinks twice and leans back half a step",
         zh="許硯特寫在左、黃昏的燈籠光裡，眉毛一下揚起、嘴半張，紅綢花在畫面下緣，看著畫外右邊的周員外；眨兩下眼，往後仰半步"),
    dict(cam="Medium close-up, slow push in", set=DOOR, chars=["zhouyuanwai"],
         lines=[("zhouyuanwai", "當年那門親，", "低頭"), ("zhouyuanwai", "是小老兒糊塗。", "陪笑")],
         prompt="medium close-up of Zhou Yuanwai kneeling on the step on screen right, his black skullcap in his hands now, his head bowed, "
                "his daughter's lilac sleeve beside him at the frame edge, his small eyes flicking up at Xu Yan off screen left",
         motion="he wrings the skullcap in both hands and bows lower",
         zh="周員外中近景在右、跪在台階上，瓜皮帽已經拿在手上，低著頭，畫邊是女兒的淡紫袖子，小眼睛往上偷瞄畫外左邊的許硯；雙手絞著帽子，腰彎得更低"),
    dict(act=2, cam="Medium shot, locked", set=DOOR, chars=[],
         prompt="medium shot of Zhou Yuanwai's daughter kneeling on the inn step, a quiet young woman of nineteen in a modest lilac cotton "
                "jacket with a high collar, her hair in a simple bun, a red lacquered gift box in her hands, her eyes lowered, her cheeks pink "
                "with embarrassment",
         motion="she lifts the gift box a little higher with both hands and lowers her head further, not looking up",
         zh="周員外的女兒中景、跪在客棧台階上，十九歲、安靜，一件高領的素淡紫棉襖，頭髮挽成簡單的髻，雙手捧著紅漆禮盒，眼睛垂著、臉頰羞紅；雙手把禮盒再捧高一點，頭垂得更低，不抬眼"),
    dict(insert=True, act=2, cam="Overhead insert of the gift boxes, locked", set=DOOR, chars=[],
         prompt="overhead insert of three red lacquered gift boxes with their lids lifted on the stone step, one holding a ginseng root on red "
                "silk, one holding two silver ingots, one holding a pale green jade ruyi sceptre",
         motion="a servant's hands lift the last lid away and the silver ingots catch the lantern light",
         zh="俯角插鏡：石階上三個掀開蓋子的紅漆禮盒，一盒紅綢上一支人參、一盒兩錠銀元寶、一盒一柄淡綠玉如意；家丁的手把最後一個蓋子掀開，銀元寶接住燈籠光"),
    dict(cam="Close-up, slow push in", set=DOOR, chars=["tangxiaotang"],
         lines=[("tangxiaotang", "人參、銀子、玉如意，", "眼睛發亮，飛快"), ("tangxiaotang", "少說三百兩。", "小聲")],
         prompt="close-up of Tang Xiaotang's face on screen left, popping in at Xu Yan's shoulder, her high stand-up collar fastened at her "
                "throat, her big round eyes sparkling as she counts, her eyes on the gift boxes below the frame",
         motion="her fingers tick off the boxes in the air one, two, three and her eyebrows shoot up",
         zh="唐小棠的臉特寫在左，從許硯肩後冒出來，高立領扣到喉頭，圓圓的大眼睛閃著光在算，看著畫面下方的禮盒；手指在空中一個一個點過去，一、二、三，眉毛一下揚起"),
    dict(ch="舊帳", cam="Two-shot, locked", set=DOOR, chars=["xuyan", "zhouyuanwai"],
         lines=[("xuyan", "員外，", "上前"), ("xuyan", "請起。", "伸手扶")],
         prompt="two-shot on the inn steps, Xu Yan on screen left stepping up to Zhou Yuanwai who kneels on screen right, Xu Yan's hand "
                "reaching for Zhou Yuanwai's elbow",
         motion="Xu Yan takes him by the elbow and lifts him up off his knees onto his feet",
         zh="客棧台階上的雙人鏡：許硯在左走上前，周員外在右跪著，許硯伸手扶他的手肘；一把扶住手肘，把他從地上拉起來站好"),
    dict(tag="爽點", cam="Close-up, locked", set=DOOR, chars=["xuyan"],
         lines=[("xuyan", "那筆舊帳，", "平靜，笑"), ("xuyan", "跟我算不著。", "一字一字")],
         prompt="close-up of Xu Yan's face on screen left in the lantern light, a calm easy smile, his eyes level on Zhou Yuanwai off screen right",
         motion="he lets go of the elbow and dusts his own hands lightly together once",
         zh="【爽點】許硯特寫在左、燈籠光裡，一個淡定的笑，眼睛平平看著畫外右邊的周員外；放開他的手肘，兩手輕輕拍一下"),
    dict(cam="Close-up, locked", set=DOOR, chars=["zhouyuanwai"],
         lines=[("zhouyuanwai", "那……", "傻住"), ("zhouyuanwai", "這禮？", "捧著盒子")],
         prompt="close-up of Zhou Yuanwai's long narrow face on screen right, blinking in confusion, the red gift box held against his chest, "
                "his eyes on Xu Yan off screen left",
         motion="he looks down at the box in his arms and back up at Xu Yan, his mouth working",
         zh="周員外的長臉特寫在右，傻愣愣地眨眼，紅禮盒抱在胸前，看著畫外左邊的許硯；低頭看手上的盒子，再抬頭看許硯，嘴巴張張合合"),
    dict(cam="Medium close-up, locked", set=DOOR, chars=["xuyan"],
         lines=[("xuyan", "禮，", "拱手"), ("xuyan", "請帶回去。", "客氣但不留")],
         prompt="medium close-up of Xu Yan on the inn step on screen left, cupping his hands in a polite bow, the red silk flower on his chest, "
                "his eyes on Zhou Yuanwai off screen right",
         motion="he bows with his cupped hands and then sweeps one open hand out toward the street",
         zh="許硯中近景在左、客棧台階上，拱手客氣地一揖，胸前紅綢花，看著畫外右邊的周員外；拱手一揖，再攤開一隻手往街上一比"),
    dict(cam="Close-up, slow push in", set=DOOR, chars=["tangxiaotang"],
         lines=[("tangxiaotang", "三百兩……", "心疼"), ("tangxiaotang", "不收？", "噘嘴")],
         prompt="close-up of Tang Xiaotang's face on screen left, her high stand-up collar fastened at her throat, her lips pushed out in a big "
                "pout, her eyes following the gift boxes as the servants carry them back down the steps",
         motion="she clutches the gold abacus at her waist with both hands and her shoulders droop",
         zh="唐小棠特寫在左，高立領扣到喉頭，嘴噘得老高，眼睛跟著家丁捧下台階的禮盒；雙手抓著腰間的小金算盤，肩膀垮下來"),
    dict(cam="Two-shot, locked", set=DOOR, chars=["qinshuang", "tangxiaotang"],
         lines=[("qinshuang", "心疼？", "斜眼，憋笑")],
         prompt=f"two-shot on the inn steps, {QS}, on screen left leaning toward Tang Xiaotang, Tang Xiaotang in her peach-pink ruqun with "
                f"the high stand-up collar on screen right still clutching her abacus",
         motion="Qin Shuang bumps Tang Xiaotang with her elbow and Tang Xiaotang huffs and bumps her back",
         zh="客棧台階上的雙人鏡：戴斗笠的秦霜在左，往唐小棠那邊湊，高領桃粉襦裙的唐小棠在右，還抓著算盤；秦霜用手肘撞她一下，唐小棠哼一聲撞回去"),
    # ---------------- 賀禮
    dict(ch="賀禮", cam="Wide shot, locked", set=DOOR, chars=["chengshanzhang", "xuyan", "zhouyuanwai"],
         lines=[("chengshanzhang", "解元郎，", "笑，走上台階"), ("chengshanzhang", "老夫來遲了。", "溫潤")],
         prompt="wide shot of the inn doorway, Headmaster Cheng in his blue-grey scholar's robe and black square cap climbing the steps from "
                "the street on screen right with a book scroll in one hand, a young servant with two long gift boxes behind him, Zhou "
                "Yuanwai and his servants shuffling aside with their boxes, Xu Yan on the top step on screen left",
         motion="Zhou Yuanwai backs away bowing down the steps, while Headmaster Cheng climbs up past him toward Xu Yan",
         zh="客棧門口的全景：程山長穿青灰儒衫、戴方巾，一手拿書卷，從右邊街上走上台階，身後一個小書童捧著兩個長禮盒，周員外和家丁捧著盒子往旁邊退，許硯在左邊最上面一級；周員外一邊鞠躬一邊倒退下台階，程山長從他身邊走上來"),
    dict(cam="Medium close-up, locked", set=DOOR, chars=["chengshanzhang"],
         lines=[("chengshanzhang", "這是知府大人", "示意書童"), ("chengshanzhang", "託老夫送來的。", "笑")],
         prompt="medium close-up of Headmaster Cheng on the top step on screen right, his silver beard on his chest, turning to beckon the "
                "servant beside him, his eyes on Xu Yan off screen left",
         motion="he beckons with two fingers and takes one long gift box from the servant into both hands",
         zh="程山長中近景在右、最上面一級台階，銀白長鬚垂在胸前，轉身招呼旁邊的書童，看著畫外左邊的許硯；兩根手指一招，從書童手上接過一個長禮盒雙手捧著"),
    dict(insert=True, act=1, cam="Insert of the prefect's gift, locked", set=DOOR, chars=[],
         prompt="insert of a long dark wooden gift box opened in two hands in wide blue-grey sleeves, a fine writing brush with a white jade "
                "handle and a black inkstone resting on yellow silk inside",
         motion="the lid slides back and the jade brush handle gleams in the lantern light",
         zh="插鏡：青灰寬袖的兩隻手打開一個深色長木盒，黃綢上躺著一支白玉桿的好毛筆和一方黑硯；盒蓋滑開，玉筆桿在燈籠光裡一亮"),
    dict(tag="伏筆", cam="Medium close-up, slow push in", set=DOOR, chars=["chengshanzhang"],
         lines=[("chengshanzhang", "老夫送你一句：", "收起笑"), ("chengshanzhang", "樹大招風。", "眼神銳利")],
         prompt="medium close-up of Headmaster Cheng on screen right, the smile gone from his face, his warm sharp eyes narrowing, his long "
                "silver brows drawn down, his eyes on Xu Yan off screen left",
         motion="he holds the gift box out at arm's length and keeps hold of it a beat longer before letting go",
         zh="【伏筆】程山長中近景在右，笑容收起，溫潤銳利的眼睛瞇起來，銀白長眉壓低，看著畫外左邊的許硯；把禮盒伸直手臂遞出去，多握了一拍才放"),
    dict(cam="Medium close-up, locked", set=DOOR, chars=["xuyan"],
         lines=[("xuyan", "學生，", "鄭重"), ("xuyan", "記下了。", "深深一揖")],
         prompt="medium close-up of Xu Yan on screen left holding the long gift box against his chest, his face serious now, his eyes on "
                "Headmaster Cheng off screen right",
         motion="he bows deeply over the box and straightens slowly",
         zh="許硯中近景在左，把長禮盒抱在胸前，臉正經起來，看著畫外右邊的程山長；捧著盒子深深一揖，慢慢直起身"),
    # ---------------- 慶功宴
    dict(ch="慶功宴", tag="奇觀", cam="Wide shot, high angle, slow push in", set=HALL, chars=["tangxiaotang", "xuyan"],
         lines=[("tangxiaotang", "今晚，", "站上長凳，揮手"), ("tangxiaotang", "唐家請客！", "大聲")],
         prompt="wide shot from a high angle over the packed hall, round banquet tables full of laughing guests raising wine cups, Tang "
                "Xiaotang in her fitted peach-pink silk ruqun with the high stand-up collar fastened at her throat standing up on a bench in "
                "the middle with one arm raised, Xu Yan below her at the table",
         motion="every guest lifts a wine cup toward her at once and a cheer ripples across the tables",
         zh="【奇觀】高角度俯瞰擠滿的大堂：一張張圓宴桌坐滿笑著舉杯的客人，高領桃粉襦裙的唐小棠站上中間的長凳、舉起一隻手，許硯坐在她下面的桌邊；所有客人一起朝她舉杯，一陣歡呼傳過一桌桌"),
    dict(tag="鉤子4", cam="Medium close-up, locked", set=HALL, chars=["xudalang"],
         lines=[("xudalang", "堂弟，", "笑得很親熱"), ("xudalang", "大哥敬你！", "舉杯")],
         prompt="medium close-up of Xu Dalang at a banquet table on screen right under the red lanterns, his old straw hat pushed back on his "
                "head, a full wine cup raised, a warm friendly smile that does not reach his narrow eyes, his eyes on Xu Yan off screen left",
         motion="he rises halfway from the bench and lifts the wine cup high toward Xu Yan",
         zh="【鉤子4】許大郎中近景在右、紅燈籠下的宴桌邊，舊草帽推到腦後，舉著一杯滿滿的酒，笑得很親熱、細長的眼睛裡卻沒有笑，看著畫外左邊的許硯；從長凳上半站起來，把酒杯朝許硯高高一舉"),
    dict(cam="Medium close-up, locked", set=HALL, chars=["xuyan"],
         lines=[("xuyan", "大哥，", "笑"), ("xuyan", "乾了！", "仰頭")],
         prompt="medium close-up of Xu Yan at the banquet table on screen left, his face flushed and happy, a wine cup raised, his eyes on Xu "
                "Dalang off screen right",
         motion="he clinks the cup toward Xu Dalang across the table and tips it back in one swallow",
         zh="許硯中近景在左、宴桌邊，臉喝得紅紅的、很開心，舉著酒杯，看著畫外右邊的許大郎；隔著桌子朝許大郎碰一下，仰頭一口喝乾"),
    dict(cam="Medium close-up, locked", set=HALL, chars=["zhanggui"],
         lines=[("zhanggui", "解元老爺，", "陪笑，拔高嗓門"), ("zhanggui", "今晚不收錢！", "拍櫃檯")],
         prompt="medium close-up of the innkeeper behind the long dark counter on screen right, thin with a pinched face and a wispy "
                "moustache, black over-sleeves, beaming a fawning smile at Xu Yan off screen left, a wine jar under one arm",
         motion="he slaps the counter with his free hand and bows so low his skullcap nearly slips",
         zh="客棧掌櫃中近景在右、長櫃檯後，瘦、尖臉、稀鬍子、黑套袖，對著畫外左邊的許硯陪著諂媚的笑，一隻手臂夾著酒罈；空著的手一拍櫃檯，腰彎到瓜皮帽差點滑下來"),
    dict(act=2, cam="Close-up, slow push in", set=HALL, chars=["xudalang"],
         prompt="close-up of Xu Dalang's face on screen right behind the rim of his raised wine cup, his narrow eyes sliding sideways over the "
                "rim toward Qin Shuang off screen left",
         motion="he drinks slowly and his eyes stay fixed past the cup, the smile gone",
         zh="許大郎的臉特寫在右，在舉起的酒杯沿後面，細長的眼睛越過杯沿往旁邊滑，看著畫外左邊的秦霜；慢慢喝，眼睛一直越過杯子盯著，笑沒了"),
    dict(cam="Medium close-up, slow push in", set=HALL, chars=["qinshuang"],
         lines=[("qinshuang", "上樓。", "低聲"), ("qinshuang", "我有話說。", "眼睛不看人")],
         prompt="medium close-up of Qin Shuang at the banquet table on screen left, her wide douli hat hanging down her back on its cord so her "
                "whole face shows, her bold brows drawn together, her eyes lowered, her face turned toward Xu Yan off screen right",
         motion="she sets her wine cup down untouched and rises from the bench",
         zh="秦霜中近景在左、宴桌邊，寬斗笠用繩子掛在背後、整張臉露出來，劍眉皺著，眼睛垂著，臉朝畫外右邊的許硯；把一口沒喝的酒杯放下，從長凳上站起來"),
    dict(cam="Close-up, locked", set=HALL, chars=["tangxiaotang"],
         lines=[("tangxiaotang", "上樓？", "眨眼"), ("tangxiaotang", "這麼早？", "笑得很賊")],
         prompt="close-up of Tang Xiaotang's face on screen right at the banquet table, her high stand-up collar fastened at her throat, one "
                "eyebrow raised and a sly teasing smile with dimples, her eyes on Qin Shuang off screen left",
         motion="she props her chin on one hand and wiggles her eyebrows",
         zh="唐小棠特寫在右、宴桌邊，高立領扣到喉頭，挑起一邊眉毛、酒窩一現笑得很賊，看著畫外左邊的秦霜；一手托著下巴，眉毛挑了挑"),
    # ---------------- 玉佩
    dict(ch="玉佩", act=3, cam="Wide shot, locked", set=ROOM, chars=["qinshuang", "xuyan"], night=LAMP,
         prompt="wide shot of the guest room, Qin Shuang on screen left just inside the door with her back to it, her douli hat hanging down "
                "her back, Xu Yan on screen right beside the low table with the oil lamp, the spear leaning by the door beside her",
         motion="Qin Shuang pushes the door shut behind her with her shoulder, slides the bolt across, and turns to face him",
         zh="客房全景：秦霜在左、剛進門背靠著門，斗笠掛在背後，許硯在右、站在點著油燈的矮桌旁，長槍靠在她旁邊的門邊；秦霜用肩膀把門頂上，插上門閂，轉身面對他"),
    dict(cam="Medium close-up, locked", set=ROOM, chars=["qinshuang"], night=LAMP,
         lines=[("qinshuang", "那塊玉，", "深吸一口氣"), ("qinshuang", "給我看看。", "伸手")],
         prompt="medium close-up of Qin Shuang by the door on screen left in the warm lamplight, her high ponytail over one shoulder, her "
                "almond eyes steady, one hand held out palm up toward Xu Yan off screen right",
         motion="she takes one deep breath and holds her open hand out further",
         zh="秦霜中近景在左、門邊，暖暖的燈光裡，高馬尾垂到一邊肩上，杏眼很穩，一隻手掌心朝上伸向畫外右邊的許硯；深吸一口氣，把攤開的手再伸出去一點"),
    dict(cam="Close-up, locked", set=ROOM, chars=["xuyan"], night=LAMP,
         lines=[("xuyan", "妳那天，", "輕聲"), ("xuyan", "臉色都變了。", "看著她")],
         prompt="close-up of Xu Yan's face on screen right in the warm lamplight, his brows lifting gently, his eyes on Qin Shuang off screen left",
         motion="his right hand moves slowly to his left sleeve and rests there",
         zh="許硯特寫在右、暖暖的燈光裡，眉毛輕輕揚起，看著畫外左邊的秦霜；右手慢慢移到左袖上，停在那裡"),
    dict(insert=True, act=2, cam="Insert of the jade pendant, locked", set=ROOM, chars=[], night=LAMP,
         prompt="insert in the lamplight, a hand in a faded blue-grey sleeve drawing a small oval white jade pendant about the size of a walnut "
                "out of the left sleeve on its red cord, a woman's open palm in a fitted dark brown sleeve waiting just below it",
         motion="the hand lifts the pendant out, it swings once on its cord catching the lamplight, and he lowers it into her open palm",
         zh="插鏡：燈光裡，一隻青灰袖子的手從左袖裡抽出一塊核桃大的橢圓白玉佩，繫著紅繩，下面是一隻深棕袖子攤開等著的手；玉在繩上晃一下、接住燈光，他把玉放進她的手心"),
    dict(tag="顏值鏡頭", cam="Two-shot, slow push in", set=ROOM, chars=["qinshuang", "xuyan"], night=LAMP,
         lines=[("qinshuang", "這是我爹的。", "很輕")],
         prompt="two-shot by the low table in the lamplight, Qin Shuang on screen left laying the walnut-sized white jade pendant into Xu "
                "Yan's open palm with both hands, her head bowed, the candle-like lamp glow on her lowered profile, Xu Yan on screen right "
                "looking down at her",
         motion="she presses the pendant into his palm, her hands cupped around his",
         zh="【顏值鏡頭】矮桌旁的雙人鏡、燈光裡：秦霜在左，雙手把核桃大的白玉佩放進許硯攤開的手心，低著頭，燈光照著她低下的側臉，許硯在右低頭看她；她把玉按進他掌心，雙手包著他的手停了一拍"),
    dict(tag="中段鉤子", cam="Close-up, slow push in", set=ROOM, chars=["qinshuang"], night=LAMP,
         lines=[("qinshuang", "我爹，", "抬起頭"), ("qinshuang", "是秦烈山。", "一字一字")],
         prompt="close-up of Qin Shuang's face on screen left in the warm lamplight, lifting her head, her bold brows softened, her almond "
                "eyes gentler than ever and shining, her eyes on Xu Yan off screen right",
         motion="she raises her chin and looks straight at him without blinking",
         zh="【中段鉤子】秦霜的臉特寫在左、暖暖的燈光裡，抬起頭，劍眉軟下來，杏眼從來沒這麼柔、閃著光，看著畫外右邊的許硯；下巴抬起，直直看著他，不眨眼"),
    dict(cam="Close-up, locked", set=ROOM, chars=["xuyan"], night=LAMP,
         lines=[("xuyan", "我知道。", "溫和"), ("xuyan", "妳說，我聽。", "點頭")],
         prompt="close-up of Xu Yan's face on screen right in the lamplight, his face gentle and steady, his eyes on Qin Shuang off screen left",
         motion="he nods once slowly and his fingers close over the jade in his palm",
         zh="許硯特寫在右、燈光裡，臉溫和又穩，看著畫外左邊的秦霜；慢慢點一下頭，手指把掌心的玉握住"),
    dict(cam="Medium close-up, locked", set=ROOM, chars=["qinshuang"], night=LAMP,
         lines=[("qinshuang", "他貼身戴了二十年，", "回憶"), ("qinshuang", "從不離身。", "聲音發緊")],
         prompt="medium close-up of Qin Shuang on screen left in the lamplight, one hand pressed flat over her own heart, her eyes drifting "
                "down toward the jade below the frame",
         motion="her hand presses against her chest and curls into a fist",
         zh="秦霜中近景在左、燈光裡，一隻手平按在自己心口，眼睛垂到畫外右邊許硯手上的玉；手按著胸口，手指慢慢收成拳"),
    dict(tag="轉折", cam="Close-up, slow push in", set=ROOM, chars=["qinshuang"], night=LAMP,
         lines=[("qinshuang", "怎麼會在你手裡，", "抬眼"), ("qinshuang", "我也不知道。", "搖頭")],
         prompt="close-up of Qin Shuang's face on screen left, her brows knitting in confusion, her eyes on Xu Yan off screen right, searching his face",
         motion="she shakes her head slowly, her eyes not leaving his face",
         zh="【轉折】秦霜特寫在左，眉頭困惑地皺起來，眼睛在畫外右邊許硯的臉上找答案；慢慢搖頭，眼睛一直沒離開他的臉"),
    dict(cam="Medium close-up, slow push in", set=ROOM, chars=["xuyan"], night=LAMP,
         lines=[("xuyan", "它就躺在舊書箱裡，", "老實"), ("xuyan", "誰放的，我不記得。", "皺眉")],
         prompt="medium close-up of Xu Yan by the low table on screen right, looking down at the white jade pendant in his open palm, his brows "
                "knitting, the oil lamp beside him",
         motion="he turns the pendant over in his palm with his thumb",
         zh="許硯中近景在右、矮桌旁，低頭看著攤在掌心的白玉佩，眉頭皺起，油燈在旁邊；拇指把玉在掌心翻一面，皺眉盯著它"),
    dict(insert=True, act=2, cam="Insert of their hands over the jade, locked", set=ROOM, chars=[], night=LAMP,
         prompt="insert in the lamplight, a man's hand in a faded blue-grey sleeve closed loosely around the white jade pendant, a woman's hand "
                "in a dark brown sleeve resting on top of it",
         motion="his fingers turn over and fold her hand inside his together with the jade",
         zh="插鏡：燈光裡，一隻青灰袖子的男人的手鬆鬆握著白玉佩，一隻深棕袖子的女人的手蓋在上面；他的手指翻過來，把她的手連同玉一起包進掌心"),
    dict(cam="Medium close-up, locked", set=ROOM, chars=["xuyan"], night=LAMP,
         lines=[("xuyan", "等見到他，", "看著她"), ("xuyan", "親手還他。", "篤定")],
         prompt="medium close-up of Xu Yan on screen right in the lamplight, holding Qin Shuang's hand and the jade together in both of his, a "
                "quiet sure smile, his eyes on Qin Shuang off screen left",
         motion="he gives her hand one firm squeeze",
         zh="許硯中近景在右、燈光裡，兩手把秦霜的手和玉一起握著，一個安靜篤定的笑，看著畫外左邊的秦霜；用力握一下她的手"),
    dict(tag="顏值鏡頭", cam="Close-up, locked", set=ROOM, chars=["qinshuang"], night=LAMP,
         lines=[("qinshuang", "……嗯。", "眼眶紅了，笑")],
         prompt="close-up of Qin Shuang's face on screen left in the warm lamplight, her eyes wet and shining, a small soft smile under her bold "
                "brows, her eyes on Xu Yan off screen right",
         motion="she nods once and the smile grows, a tear catching the lamplight on her lashes",
         zh="【顏值鏡頭】秦霜特寫在左、暖暖的燈光裡，眼睛濕亮，劍眉下一個柔柔的小笑，看著畫外右邊的許硯；點一下頭，笑意加深，睫毛上一顆淚接住燈光"),
    dict(tag="短線收", cam="Close-up, slow push in", set=ROOM, chars=["xuyan"], night=LAMP,
         lines=[("xitong", "支線完成：", "平板電子音，叮一聲"), ("xitong", "玉佩的主人。", "平板電子音")],
         prompt="close-up of Xu Yan's face on screen right in the lamplight, his eyes lifting to a point in the empty air in front of him; the "
                "system voice speaks off screen",
         motion="his eyes track slowly across the empty air as if reading, then return to Qin Shuang",
         zh="【短線收】系統面板：許硯特寫在右、燈光裡，眼睛抬起看著面前的空中；眼睛像讀字一樣慢慢掃過空中，再回到秦霜身上",
         ov=[("支線完成：玉佩的主人｜秦烈山", "task")]),
    # ---------------- 拿下
    dict(ch="拿下", tag="結尾／奇觀", act=3, cam="Wide shot, slow pan left", set=HALL, chars=["tangxiaotang"],
         prompt="wide shot across the banquet hall, the front doors on screen right flung open and a file of runners in black with burning "
                "pine torches pouring in, the guests at the round tables freezing with their wine cups in the air, Tang Xiaotang in her "
                "peach-pink ruqun with the high stand-up collar rising from her bench in the middle",
         motion="the runners stream in between the tables toward the staircase on screen left, torches flaring, and every guest's cup stops halfway",
         zh="【結尾／奇觀】橫過宴席大堂的全景：右邊大門被推開，一列舉著松明火把的黑衣衙役湧進來，圓桌邊的客人一個個僵住、酒杯停在半空，高領桃粉襦裙的唐小棠在中間從長凳上站起來；衙役從桌子之間往左邊的樓梯衝，火把一閃一閃，每個人的酒杯都停在一半"),
    dict(tag="結尾", insert=True, act=1, cam="Insert of a wine cup stopped in the air, locked", set=HALL, chars=[],
         prompt="insert of a guest's hand holding a small wine cup frozen halfway to his mouth over the banquet table, orange torchlight "
                "sweeping across it",
         motion="the wine trembles in the cup and a drop spills over the rim onto the tablecloth",
         zh="【結尾】插鏡：宴桌上方一隻客人的手，小酒杯停在送到嘴邊的一半，橘色的火把光掃過；杯裡的酒一顫，一滴灑出杯沿落在桌布上"),
    dict(tag="結尾", cam="Close-up, locked", set=HALL, chars=["tangxiaotang"],
         lines=[("tangxiaotang", "你們做什麼？", "臉色發白，大聲")],
         prompt="close-up of Tang Xiaotang's face in the middle of the frame, her high stand-up collar fastened at her throat, orange torchlight "
                "flickering across her pale face, her wide eyes turned toward the stairs beyond the left edge of the frame",
         motion="she grabs the edge of the table and leans forward toward the stairs",
         zh="【結尾】唐小棠的臉特寫在中間，高立領扣到喉頭，橘色火光在她發白的臉上跳，眼睛瞪大看著畫外左邊的衙役；抓住桌邊，身子往樓梯那邊探"),
    dict(tag="結尾", act=2, cam="Wide shot, low angle, locked", set=HALL, chars=[],
         prompt="wide shot from a low angle up the wooden staircase on screen left, a crush of runners in black with burning pine torches "
                "climbing it two steps at a time, smoke rolling under the beams",
         motion="the runners pound up the stairs shoulder to shoulder, torches swinging, and the leading one reaches the top landing",
         zh="【結尾】低角度沿著左邊的木樓梯往上拍的全景：一群舉著松明火把的黑衣衙役一次跨兩級擠上樓，煙在梁下翻滾；衙役肩擠著肩咚咚咚衝上去，火把晃，帶頭的一個衝到樓梯口（無台詞）"),
    dict(tag="結尾", cam="Close-up, slow push in", set=ROOM, chars=["qinshuang"], night=LAMP,
         lines=[("qinshuang", "樓梯……", "臉色一變，壓低聲音"), ("qinshuang", "有人。", "手按住他")],
         prompt="close-up of Qin Shuang's face on screen left in the lamplight, her head snapping toward the door, her eyes narrowing like a "
                "soldier's, her lips parted, orange light beginning to flicker in the gap under the door beyond her",
         motion="she turns her head sharply toward the door and holds her breath",
         zh="【結尾】秦霜特寫在左、燈光裡，頭猛地轉向門口，眼睛像軍人一樣瞇起來，嘴唇微張，身後門縫底下開始閃出橘色的光；猛一轉頭看門，屏住呼吸"),
    dict(tag="結尾", act=1, cam="Medium shot, locked", set=ROOM, chars=["qinshuang", "xuyan"], night="the cold blue moonlight at the window stays unchanged",
         prompt="medium shot of the guest room door from inside, Qin Shuang and Xu Yan by the low table on screen right with their hands still "
                "together, the bolted door on screen left",
         motion="the door bursts inward off its bolt with a crash of splinters and both of them spin toward it",
         zh="【結尾】從房裡拍門的中景：秦霜和許硯在右、矮桌旁，手還握在一起，左邊是閂上的門；門「砰」地被踹開、門閂碎裂，兩人一起轉身"),
    dict(tag="結尾", cam="Medium close-up, low angle, locked", set=ROOM, chars=["yayi"],
         lines=[("yayi", "罪臣之女秦霜，", "吼")],
         prompt="medium close-up from a low angle of the burly runner leader standing in the broken doorway on screen left, a burning pine "
                "torch held high, the iron chain at his belt, more torches crowding behind him, his eyes on Qin Shuang off screen right",
         motion="he thrusts the torch forward into the room and steps over the broken bolt",
         zh="【結尾】低角度：魁梧的衙役頭中近景在左、站在破開的門口，高舉松明火把，腰間掛鐵鏈，身後擠著更多火把，看著畫外右邊的秦霜；把火把往房裡一伸，跨過碎掉的門閂"),
    dict(tag="結尾", cam="Medium close-up, low angle, slow push in", set=ROOM, chars=["yayi"],
         lines=[("yayi", "私逃軍籍，", "官腔"), ("yayi", "拿下！", "揮手")],
         prompt="medium close-up from a low angle of the runner leader in the doorway on screen left, unhooking the iron chain from his belt with "
                "his free hand, the torch flaring, his eyes on Qin Shuang off screen right",
         motion="he swings the chain off his belt and flings his torch arm toward her, ordering the men behind him forward",
         zh="【結尾】低角度：衙役頭中近景在左、門口，空著的手從腰上解下鐵鏈，火把一亮，看著畫外右邊的秦霜；鐵鏈一甩，舉火把的手朝她一揮，叫後面的人上"),
    dict(tag="結尾", act=2, cam="Close-up, locked", set=ROOM, chars=["qinshuang"], night="the cold blue moonlight at the window stays unchanged",
         prompt="close-up of Qin Shuang's face on screen right in the orange torchlight, her face gone hard and white, her almond eyes flicking "
                "sideways to the spear by the door off screen left",
         motion="her eyes snap to the spear and her weight shifts onto her front foot",
         zh="【結尾】秦霜特寫在右、橘色火光裡，臉一下變得又硬又白，杏眼往畫外左邊門邊的長槍一瞟；眼睛釘在槍上，重心移到前腳"),
    dict(tag="結尾", cam="Medium close-up, locked", set=ROOM, chars=["xuyan"], night="the cold blue moonlight at the window stays unchanged",
         lines=[("xuyan", "慢著！", "一步擋在她前面")],
         prompt="medium close-up of Xu Yan on screen right stepping in front of Qin Shuang with one arm thrown out sideways, the orange "
                "torchlight on his face, his brows drawn down hard, his eyes on the runner leader off screen left",
         motion="he takes one hard step forward and plants his feet, his outflung arm shielding her",
         zh="【結尾】許硯中近景在右，一步擋到秦霜前面、一隻手臂往旁邊張開，橘色火光照在臉上，眉頭狠狠壓下，看著畫外左邊的衙役頭；用力跨前一步站穩，張開的手臂護著她"),
    dict(tag="結尾", act=3, cam="Wide shot, slow push in", set=HALL, chars=["xudalang"],
         prompt="wide shot from the top landing down the crowded wooden staircase, runners in black with torches packed on every step, and at "
                "the very bottom of the stairs, behind them all, Xu Dalang in his old straw hat standing still among the frozen guests",
         motion="the runners push upward step by step while Xu Dalang at the bottom does not move at all",
         zh="【結尾】從樓梯口往下拍擠滿人的木樓梯全景：每一級都擠著舉火把的黑衣衙役，最下面、在所有人後面，戴舊草帽的許大郎站在僵住的客人之間；衙役一級一級往上擠，最下面的許大郎一動不動"),
    dict(tag="結尾", act=3, cam="Close-up, slow push in", set=HALL, chars=["xudalang"],
         prompt="close-up of Xu Dalang's face on screen centre at the foot of the stairs, orange torchlight flickering over it, the old straw "
                "hat brim with its pale stripe where a cord was taken off, his narrow eyes cold and lifted toward the room upstairs, no smile",
         motion="he lifts his chin a little toward the top of the stairs and his eyes do not blink",
         zh="【結尾】最後一格：許大郎的臉特寫在中間、樓梯腳下，橘色火光在臉上晃，舊帽簷上那道拆掉繩子的淺色印子，細長的眼睛冷冷地往上看樓上的房間，沒有笑；下巴微微往樓上一抬，眼睛不眨"),
]

MUSIC = ("a soft held breath of guqin as she starts to speak, cut by a comic brass stab when the whole row drops to its knees, a sly "
         "bassoon grovel for the squire, a bright comic woodblock as the girl tallies the gifts, a calm warm pipa for 'that old debt is "
         "not mine to settle', a stately guqin for the old headmaster that darkens on 'a tall tree catches the wind', a loud festive "
         "banquet of drums, suona and clinking cups, a thin uneasy string under the cousin's toast, then a hushed lamplit room of breathy "
         "xiao and soft strings as she lays the jade in his palm and names her father, swelling gently and tenderly on 'give it back to him "
         "yourself', a glassy chime, then a sudden crash of drums and gongs as torches flood the hall, a racing low drum up the staircase, "
         "a splintering hit on the door, a brutal brass shout on 'seize her', ending on one cold sustained low string over the cousin's "
         "unsmiling face, ancient Chinese drama, no vocals")

YT_DESC = ("放榜當晚，秦霜那句話還沒出口，客棧門口先跪了一排人：當年退了原主婚事的周員外，拉著女兒、捧著人參銀子玉如意：「解元老爺，是我們瞎了眼！」"
           "唐小棠眼睛一亮：少說三百兩。許硯把周員外扶起來：「那筆舊帳，跟我算不著。禮，請帶回去。」"
           "程山長送來自己和褚知府的賀禮，只留了一句話：「樹大招風。」慶功宴上，族兄許大郎笑著敬酒，眼睛卻一直越過杯沿看著秦霜。"
           "樓上客房，秦霜要了那塊玉，在燈下放進許硯手心：「這是我爹的。我爹，是秦烈山。」他貼身戴了二十年，從不離身——可為什麼會在原主的書箱裡，她也不知道。"
           "許硯握住她的手：「等見到他，親手還他。」話音剛落，樓下的酒杯一個個停住，舉著火把的衙役擠滿樓梯，門板被一腳踹開：「罪臣之女秦霜，私逃軍籍，拿下！」"
           "人群最後面，站著許大郎。《種田娶妻打天下》第 50 集，第一季第五章完。")


def SB_HEAD(total, st, du):
    def at(s):
        t = int(st[s]); return f"{t // 60}:{t % 60:02d}"
    end = f"{int(total) // 60}:{int(total) % 60:02d}"
    return [
        f"{len(SHOTS)} 個鏡頭、六段（跪／舊帳／賀禮／慶功宴／玉佩／拿下），估計約 {total:.0f} 秒（照 lint 估法；真人語速通常再長一成左右）；細綱 140 秒（第五章最後一集，至少 120 秒）",
        "預算：片段 %d 支（靜圖 0 張），沒有「切素材」鏡。片段走路線 A（Colab H3 Ref2VA 三段式，沒有首格）；秒數見 `hailuo/clips-dh-e050.json`（`gen-dh.mjs` 算），首格清單只當參照圖清單" % len(SHOTS),
        f"開頭 10 秒：接第 49 集的「今晚我有話跟你說」，秦霜在客棧台階下「許硯，我……」（0:00），客棧門口跪了一排人（{at('s02')}），周員外「解元老爺，是我們瞎了眼！」（{at('s03')}），許硯「……員外？」（{at('s04')}）；中段鉤子：「這是我爹的」「我爹，是秦烈山」（{at('s31')}–{at('s32')}）；轉折：「那筆舊帳，跟我算不著」（{at('s10')}）、玉佩為什麼在原主手裡她也不知道（{at('s35')}）；結尾收在門板被踹開、「罪臣之女秦霜，私逃軍籍，拿下！」、許大郎站在人群最後面",
        f"鉤子：【鉤子1】s01–s05 0:00、【鉤子2】s06–s14 {at('s06')}、【鉤子3】s15–s19 {at('s15')}、【鉤子4】s20–s26 {at('s20')}、【鉤子5】s27–s30 {at('s27')}、【鉤子6 中段】s31–s36 {at('s31')}、【鉤子7】s37–s40 {at('s37')}、【結尾】s41–s52 {at('s41')}–{end}",
        "顏值鏡頭：s31 秦霜（燈下把玉佩放進他手心，低下的側臉）、s32（劍眉下的眼睛第一次這麼柔）、s39（眼眶紅了、睫毛上一顆淚的笑）；是臉與表情，不停在身體",
        "爽點：開場 face_slap（s02–s14 當年退婚的周家跪著賠罪，許硯「那筆舊帳，跟我算不著」，禮不收）、中段 identity_reveal（s31–s36 秦霜親口說出自己是秦烈山的女兒，玉佩是她爹的）",
        "說話鏡頭：說話的人在畫面上的鏡頭，motion 第一句都是他說這句話、嘴唇下巴隨每個音節動；畫外台詞只有 s40 系統，放在許硯的臉上，prompt 寫明 off screen",
        "H3 寫法：motion 寫軌跡、一鏡一事、沒有 camera 字；客房的夜景 motion 補 `the warm oil-lamp glow and the cold blue moonlight at the window stay unchanged`（火把進門之後只補月光那半句）；插鏡（s07、s17、s30、s37、s42）motion 開頭寫 `The shot opens directly on this close insert from its very first frame`；唐小棠每一鏡寫高立領；秦霜在門口戴斗笠（s01–s14），宴席上斗笠掛在背後、露出整張臉（s25 起）；玉佩寫大小（核桃大）、背面的字不拍",
        "光：s01–s19 客棧門口的黃昏與剛點的紅燈籠；s20–s26 宴席滿堂紅燈籠；s27–s40 客房一盞油燈加窗上的冷月光；s41–s52 火把的橘光衝進大堂、樓梯與客房",
        "軸線：客棧門口許硯在左、跪著的周家在右（台階上），程山長從右邊街上走上來；宴席唐小棠在中間長凳上，許大郎在右、許硯在左，秦霜在許硯左邊；客房門與長槍在左、矮桌與油燈在右，秦霜先在門邊（左）、許硯在桌旁（右），之後兩人都在桌旁（秦霜左、許硯右）；衙役從左邊的門進來，大堂的大門在右、樓梯在左",
    ]


SB_FOOT = [
    "場景參考：s01–s19 用 `dh-set-zhou-kezhan-t1`（含 `prefectural inn`；門口與台階靠 prompt 寫，registry：州城客棧大堂、樓梯、慶功宴都是這張）；s20–s26、s41–s44、s51–s52 也是 `dh-set-zhou-kezhan-t1`；s27–s40、s45–s50 用 `dh-set-kezhan-t1`（含 `upstairs guest room`，排在 `prefectural inn` 前面；registry：50 給玉佩用這張）。`zhou-kezhan` 還沒畫（registry 🎨），`kezhan` 有圖。",
    "道具：周家的紅漆禮盒（人參、兩錠銀元寶、玉如意，s02–s13）；許硯胸前的紅綢花（s02–s12，接第 49 集的遊街）；唐小棠的小金算盤（s13–s14）；程山長的書卷與知府送的白玉桿毛筆、黑硯（s15–s19）；酒杯（s20–s26、s42）；核桃大的白玉佩與紅繩（s28–s38；第 41 集從原主書箱的油布包裡翻出來，第 42 集起收在許硯左袖）；門邊的長槍（s27 起；s49 秦霜瞟一眼，第 51 集她抄起這支槍）；松明火把與衙役頭腰上的鐵鏈（s41–s52）；許大郎舊草帽上拆掉繩子的印子（s52）。",
    "連戲：開場照第 49 集的結尾（遊街時秦霜拉住韁繩「今晚，我有話跟你說」）接：s01 是同一天的黃昏，兩人走回客棧，她剛開口，s02 門口先跪了一排人，那句話被打斷，留到 s31–s32 才說。周員外是第 42 集「當年退婚，退得真對」、第 49 集倒著走一條街的那位；女兒就是當年那門親的姑娘（不點名、不說話）。s10「那筆舊帳，跟我算不著」：退婚的是原主，許硯是穿越來的，所以這句話一語雙關。s16 程山長帶來褚知府的賀禮（細綱的 general_payoff：程山長與褚知府送來賀禮），s18「樹大招風」是第 51 集以後的伏筆。s21–s24 許大郎敬酒、眼睛越過杯沿盯著秦霜（細綱的衝突：慶功宴人多眼雜，許大郎已經把秦霜賣給了魏家）。s32 之前許硯已經從杜鐵那裡知道秦霜是秦烈山的女兒（第 44 集），所以 s33 他說「我知道」；這集第一次是她親口說。s34「他貼身戴了二十年」與 s35「怎麼會在你手裡，我也不知道」照細綱的 turn。s38「等見到他，親手還他」接第 48 集「將軍還活著，在北疆鹽礦」。第 51 集從秦霜抄起門邊的長槍、許硯按住她的手接。",
    "短線 s01-t10（秦霜為什麼一見那塊玉佩就變了臉？，第 44 集 setup）在 s31–s36 收：玉佩是她爹秦烈山的貼身之物。玉佩到底是什麼（m11，第三季揭：秦家的鎮北調兵令）、原主是怎麼撿到它的（m05，第二季揭）一句都不說：秦霜不知道，許硯說「它就躺在舊書箱裡，誰放的，我不記得」（s36，第 44 集他已經答過「舊書箱裡翻出來的」），背面的字不拍。秦家為什麼被定罪（m03）也不碰。",
    "m05：s21–s24 許大郎敬酒、盯著秦霜，s51–s52 他站在衙役後面、樓梯最下面，冷冷看著樓上（第 48 集他把秦霜的身分賣給魏家）；他和原主落水的關係全集不說，只留帽簷上的印子。衙役是真是假本集不說（第 51 集阿令才看出公文的印是假的）。",
    "系統面板不由模型畫：s40 的支線完成在剪接時疊上（task）。",
    "新的參照圖還沒畫：周員外、許大郎、程山長的定妝照（`refs-dh/zhouyuanwai-portrait-t1.png`、`xudalang-portrait-t1.png`、`chengshanzhang-portrait-t1.png`）與州城客棧的場景圖（`set-zhou-kezhan-t1.png`，e042 起就缺）。衙役（yayi）沒有定妝照，照 e042 的掌櫃只寫在 prompt 與 video.json；周員外的女兒、程山長的書童、家丁、客人、衙役群只寫在 prompt。",
]


def BRIEF(st, du, total):
    def at(s):
        t = int(st[s]); return f"{t // 60}:{t % 60:02d}"
    end = f"{int(total) // 60}:{int(total) % 60:02d}"
    return f"""# 《種田娶妻打天下》第 50 集〈拿下秦霜〉

## 故事前提

第 49 集收在解元遊街：秦霜走到馬邊拉住韁繩，仰頭看許硯，眼睛是濕的：「今晚，我有話跟你說。」第 50 集從同一天的黃昏接下去：兩人走回州城客棧，秦霜在台階下停住，手抬到帽簷「許硯，」「我……」（s01）——客棧門口先跪了一排人（s02，細綱的 hook）：當年退了原主婚事的周員外，拉著女兒和家丁，高舉紅漆禮盒：「解元老爺，」「是我們瞎了眼！」（s03）上一集的問題「秦霜要告訴他什麼？」在 0:00 先被打斷，留到樓上客房才答（{at('s31')}）。

許硯愣住「……員外？」周員外絞著帽子：「當年那門親，」「是小老兒糊塗。」女兒捧著禮盒低著頭；禮盒掀開，人參、兩錠銀元寶、一柄玉如意，唐小棠眼睛發亮：「人參、銀子、玉如意，」「少說三百兩。」許硯把周員外扶起來：「員外，」「請起。」「那筆舊帳，」「跟我算不著。」（細綱的 turn 前半；退婚的是原主，不是他。）「禮，」「請帶回去。」（opening face_slap。）唐小棠心疼得噘嘴「三百兩……」「不收？」秦霜手肘撞她：「心疼？」

程山長帶著書童走上台階：「解元郎，」「老夫來遲了。」「這是知府大人」「託老夫送來的。」——白玉桿的毛筆和一方黑硯（general_payoff：程山長與褚知府送來賀禮）。他收起笑：「老夫送你一句：」「樹大招風。」許硯深深一揖「學生，」「記下了。」

慶功宴，滿堂紅燈籠，唐小棠站上長凳：「今晚，」「唐家請客！」（細綱的奇觀前半：客棧燈火通明。）許大郎舉杯：「堂弟，」「大哥敬你！」許硯一口乾掉「大哥，」「乾了！」掌櫃拍櫃檯「解元老爺，」「今晚不收錢！」——許大郎喝酒時，細長的眼睛一直越過杯沿盯著秦霜（細綱的衝突：人多眼雜，許大郎已經把秦霜賣給了魏家）。秦霜放下酒杯：「上樓。」「我有話說。」唐小棠托著下巴眨眼「上樓？」「這麼早？」

樓上客房，一盞油燈。秦霜閂上門：「那塊玉，」「給我看看。」許硯的手按到左袖上：「妳那天，」「臉色都變了。」（接第 44 集她一把抓起玉佩又放下。）許硯從左袖抽出那塊核桃大的白玉佩，放進她攤開的手心（s30）；她看清了，雙手把玉放回他的手心（s31，細綱的顏值鏡頭）：「這是我爹的。」抬起頭：「我爹，」「是秦烈山。」（{at('s32')}，細綱的 mid_hook；midpoint identity_reveal。）許硯「我知道。」「妳說，我聽。」「他貼身戴了二十年，」「從不離身。」「怎麼會在你手裡，」「我也不知道。」（細綱的 turn 後半。）許硯翻著那塊玉：「它就躺在舊書箱裡，」「誰放的，我不記得。」他把她的手連同玉一起握住：「等見到他，」「親手還他。」秦霜眼眶紅了：「……嗯。」系統：「支線完成：」「玉佩的主人。」（payoff s01-t10：秦霜為什麼一見那塊玉佩就變了臉——那是她爹的。）

樓下的大門被推開，一列舉著火把的衙役湧進來，滿堂的酒杯一個個停在半空（s41–s42，細綱的奇觀後半）；唐小棠站起來「你們做什麼？」衙役擠滿樓梯衝上去；樓上秦霜猛地轉頭「樓梯……」「有人。」客房的門被一腳踹開，門閂碎裂，衙役頭舉著火把跨進來：「罪臣之女秦霜，」「私逃軍籍，」「拿下！」秦霜的眼睛往門邊的長槍一瞟，許硯一步擋在她前面「慢著！」——樓梯最下面、所有衙役後面，站著戴舊草帽的許大郎，冷冷地往樓上看，沒有笑（細綱的 cliffhanger，danger：「解元護得住一個罪臣之女嗎？」；第 51 集從秦霜抄起門邊長槍、許硯按住她的手「跟他們走，我接妳」接）。

本集細綱：`docs/videos/series-plans/zhong-tian-qu-qi/season-01.json` 第 50 集（140 秒，第一季第五章最後一集，調性爽＋感人＋權謀＋喜劇，lead_arc mixed）。hook 是秦霜那句話還沒出口、客棧門口先跪了一排人、「解元老爺，是我們瞎了眼」（0:00–{at('s04')}，image）；mid_hook 是夜裡秦霜把玉佩放在他掌心「這是我爹的」「我爹是秦烈山」（{at('s31')}–{at('s32')}）；衝突是慶功宴人多眼雜、許大郎已經把秦霜賣給了魏家（s21–s24、s51–s52）；turn 是許硯沒收周家的禮「那筆舊帳，跟我算不著」（s10–s12）與秦霜說出玉佩是她爹的貼身之物、為什麼在原主手裡她也不知道（s34–s36）；cliffhanger 是門板被踹開、衙役擠滿樓梯「罪臣之女秦霜，私逃軍籍，拿下！」、許大郎站在人群最後面（s41–s52，danger）。satisfaction：opening face_slap（s02–s14）、midpoint identity_reveal（s31–s36）。general_payoffs 全部入鏡：當年退原主婚的周家跪著賠罪（s02–s11）、秦霜親口說出自己是秦烈山的女兒、玉佩是她爹的（s31–s35）、程山長與褚知府送來賀禮（s15–s18）。觀眾比許硯多知道一點（許大郎告密，第 48 集），authoring.md：一集只選一種。

## 鉤子（站主 10-16：開場、結尾之外中段還要兩三個以上）

| 鉤子 | 鏡 | 約略時間 | 內容 |
| --- | --- | --- | --- |
| 【鉤子1】開場 | s01–s05 | 0:00–{at('s06')} | 「許硯，我……」話沒說完，門口跪了一排人，「解元老爺，是我們瞎了眼！」「當年那門親，是小老兒糊塗」 |
| 【鉤子2】 | s06–s14 | {at('s06')}–{at('s15')} | 禮盒「少說三百兩」，「那筆舊帳，跟我算不著」「禮，請帶回去」「三百兩……不收？」 |
| 【鉤子3】 | s15–s19 | {at('s15')}–{at('s20')} | 程山長送來知府的賀禮，「老夫送你一句：樹大招風」（風從哪裡來？） |
| 【鉤子4】 | s20–s26 | {at('s20')}–{at('s27')} | 「今晚，唐家請客！」許大郎敬酒，眼睛越過杯沿盯著秦霜，「上樓。我有話說」 |
| 【鉤子5】 | s27–s30 | {at('s27')}–{at('s31')} | 閂上門，「那塊玉，給我看看」，玉佩從袖子裡抽出來 |
| 【鉤子6】中段鉤子 | s31–s36 | {at('s31')}–{at('s37')} | 「這是我爹的」「我爹，是秦烈山」「他貼身戴了二十年」「怎麼會在你手裡，我也不知道」 |
| 【鉤子7】 | s37–s40 | {at('s37')}–{at('s41')} | 「它就躺在舊書箱裡」，「等見到他，親手還他」「……嗯」，支線完成 |
| 【結尾】 | s41–s52 | {at('s41')}–{end} | 火把湧進大堂、酒杯停住、衙役擠滿樓梯，門被踹開「罪臣之女秦霜，私逃軍籍，拿下！」「慢著！」，樓梯最下面的許大郎（解元護得住一個罪臣之女嗎？） |

## 角色

- 許硯（xuyan）：s02 在門口停住（不說話）；s04「……員外？」；s09「員外，請起」；s10「那筆舊帳，跟我算不著」；s12「禮，請帶回去」；s19「學生，記下了」；s22「大哥，乾了！」；s27 在客房；s29「妳那天，臉色都變了」；s33「我知道。妳說，我聽」；s36「它就躺在舊書箱裡，誰放的，我不記得」；s38「等見到他，親手還他」；s40 看系統面板；s50「慢著！」。胸前的紅綢花一直戴到門口那場（接遊街）。
- 秦霜（qinshuang）：s01「許硯，我……」；s14「心疼？」；s25「上樓。我有話說」；s28「那塊玉，給我看看」；s31「這是我爹的」；s32「我爹，是秦烈山」；s34「他貼身戴了二十年，從不離身」；s35「怎麼會在你手裡，我也不知道」；s39「……嗯」；s45「樓梯……有人」；s49 瞟門邊的長槍。在門口戴斗笠，宴席起斗笠掛在背後。
- 唐小棠（tangxiaotang）：s08「人參、銀子、玉如意，少說三百兩」；s13「三百兩……不收？」；s20 站上長凳「今晚，唐家請客！」；s26「上樓？這麼早？」；s43「你們做什麼？」每個 prompt 都寫高立領。
- 周員外（zhouyuanwai）：s02 帶著女兒和家丁跪在門口；s03「解元老爺，是我們瞎了眼！」；s05「當年那門親，是小老兒糊塗」；s11「那……這禮？」；s15 捧著禮盒退下台階。女兒（十九歲、高領素淡紫棉襖）只寫在 prompt（s02、s06），不說話、不進 characters。
- 程山長（chengshanzhang）：s15「解元郎，老夫來遲了」；s16「這是知府大人託老夫送來的」；s18「老夫送你一句：樹大招風」。
- 許大郎（xudalang）：s21「堂弟，大哥敬你！」；s24 喝酒時眼睛越過杯沿盯著秦霜；s51–s52 站在樓梯最下面、衙役後面，冷冷地往上看（收尾，不笑）。
- 客棧掌櫃（zhanggui）：e042 起的配角，外貌照 e042 的 video.json，聲音 Iapetus。s23「解元老爺，今晚不收錢！」
- 衙役頭（yayi）：本集才有的配角，沒有定妝照，外貌只寫在 video.json 與 prompt（三十五歲、魁梧、方臉、短黑鬍、黑衣紅腰帶、黑帽、腰掛鐵鏈、舉松明火把）；聲音 Alnilam（registry 的建議值）。s47「罪臣之女秦霜」；s48「私逃軍籍，拿下！」
- 系統（xitong）：沒有身體，只有聲音與剪接時疊上的面板（`overlays.json`：s40 支線完成）。
- 家丁、書童、宴席的客人、衙役群：背景，只寫在 prompt 裡（servants、guests、runners），沒有台詞。

## 地點（固定的地點字）

- 州城客棧門口（黃昏）：`At the open front door of the prefectural inn in Qingzhou at dusk`（s01–s19，`dh-set-zhou-kezhan-t1`，還沒畫）：寬大的門口掛著慶賀的紅綢、屋簷下剛點的紅燈籠、三級石階下到街上、裡面熱鬧的大堂透出暖光。
- 州城客棧大堂（夜，慶功宴）：`In the front hall of the prefectural inn in Qingzhou on a festive night`（s20–s26、s41–s44、s51–s52，同一張）：滿堂紅燈籠、一張張坐滿客人的圓宴桌、右邊長櫃檯、左邊上客房的木樓梯。
- 州城客棧樓上客房（夜）：`In the upstairs guest room of the prefectural inn at night`（s27–s40、s45–s50，沿用 `dh-set-kezhan-t1`）：樸素的木房間、矮桌上一盞小油燈、窗紙透著冷藍月光、後面一張掛藍帳的木床、左邊門旁的牆上靠著一支鐵頭長槍。
- 站位（軸線）：見分鏡表開頭。

## 站主觀點

站主 2026-10-16 的要求：女生要火辣漂亮，濃顏系的五官與妝、合身剪裁；不露、不濕身、鏡頭不停在身體部位；每集至少一個顏值鏡頭；結尾收在最高點；不被黃標；每集開場、結尾之外中段再兩三個以上鉤子。本集的顏值鏡頭是 s31–s32（秦霜在燈下把玉佩放進他手心、低下的側臉；抬頭時劍眉下的眼睛第一次這麼柔）與 s39（眼眶紅了的笑）；拍的是臉與手，不停在身體。唐小棠每一鏡都寫高立領；周員外的女兒寫高領素淡的棉襖。沒有人打到人：門被踹開、衙役頭解下鐵鏈，第 50 集收在「拿下！」與「慢著！」，沒有動手。玉佩背面的字不拍、禮盒與賀禮上沒有字。系統面板不由模型畫，s40 只拍許硯的眼睛。

分鏡照 `storyboard-rules.md` 2026-10-28 起的 H3 寫法（與第 42 集同）：說話的人在畫面上時 motion 第一句寫他說這句話；motion 寫軌跡、一鏡一事；表情寫成正面的字；道具寫大小；畫外的人不寫局部身體；夜景補光線不變的句子；運鏡只在 `camera`；`locked` 就是鎖定；秒數由 `gen-dh.mjs` 決定。本集沒有靜圖、沒有切素材鏡。角色外觀照 `production/cast.json` 逐字照抄。
"""
