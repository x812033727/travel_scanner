NUM = 47
TITLE = "畫出來"
TARGET_MINUTES = [1, 2]
YT_TITLE = "冒名考生背出他的文章，他只問：那架水車你畫得出嗎｜種田娶妻打天下 第47集"
THUMB = ("畫不出\n水車", "s09")
CHARS = ["xuyan", "weixun", "fengxuezheng", "chuzhifu", "chengshanzhang", "tangxiaotang", "xitong"]
MINOR = {}

COURT = ("In the court hall of the Qingzhou prefecture in bright daylight, a raised dais at the back with a red-draped judge's desk "
         "and a tall painted screen of sea waves and a red sun behind it, rows of runners in black holding red-and-black staves along "
         "both side walls, a grey stone floor with two small writing desks side by side in the middle, the tall front doors open to a "
         "sunlit forecourt where examinees crowd behind a low wooden rail")
BACK = ("In the prefect's back hall in late afternoon light, a quiet side room with carved lattice windows, a low dark tea table "
        "with two celadon cups between two carved chairs, a folding screen painted with ink mountains, slanting golden light and "
        "floating dust")

SHOTS = [
    # ---------------- 刑杖
    dict(ch="刑杖", tag="鉤子1／開頭", act=2, cam="Wide shot, locked", set=COURT, chars=["xuyan"],
         prompt="wide shot from the side of the hall, Xu Yan in his faded blue-grey robe standing at the left writing desk on screen left, "
                "two runners on screen right with their red-and-black staves swung up high over their shoulders toward him, the long "
                "shadow of a staff lying across the white sheet on his desk, the crowd of examinees at the rail behind gasping",
         motion="the two runners heave their staves up to the top of the swing and the staves hang there for a beat while Xu Yan, not "
                "looking at them, lays his writing brush down flat on the desk with one steady hand",
         zh="接第 46 集：州府大堂側面的全景，許硯在左、站在左邊那張書案後；右邊兩個衙役照馮學正的令把紅黑刑杖高高掄到肩後，正要落下，一根刑杖的長影斜斜壓在他的白紙上；欄杆後的考生倒抽一口氣；許硯看都不看刑杖，寫完最後一筆，一隻手把毛筆平平放回桌上"),
    dict(tag="鉤子1", cam="Medium close-up, locked", set=COURT, chars=["xuyan"],
         lines=[("xuyan", "第三段的水車，", "不慌，一字一字"), ("xuyan", "你畫出來。", "盯著魏珣")],
         prompt="medium close-up of Xu Yan at the left writing desk on screen left, his face calm and his eyes sharp under level brows, one "
                "finger resting on the finished essay in front of him, his eyes on Wei Xun off screen right",
         motion="he lifts the finger off the essay and points it once across the floor toward Wei Xun off screen right, his gaze steady",
         zh="許硯中近景在左、書案後，臉一收、眉眼銳利，一根手指按在寫完的文章上，眼睛看著畫外右邊的魏珣；手指從紙上抬起，朝右邊一指"),
    dict(tag="鉤子1", cam="Close-up, slow push in", set=COURT, chars=["weixun"],
         lines=[("weixun", "畫……", "愣住"), ("weixun", "畫什麼？", "強撐著倨傲")],
         prompt="close-up of Wei Xun's face on screen right at the right writing desk, his haughty half-lidded phoenix eyes snapping wide "
                "open, his thin lips parting, his eyes on Xu Yan off screen left",
         motion="his chin jerks up a little and his eyes dart down to his own finished essay and back up, a muscle in his cheek twitching",
         zh="魏珣的臉在右、右邊書案後，半闔的鳳眼一下睜大、薄唇張開，看著畫外左邊的許硯；下巴一抬，眼睛飛快瞄一下自己寫完的卷子又抬回來"),
    dict(tag="鉤子1", cam="Medium close-up, locked", set=COURT, chars=["fengxuezheng"],
         lines=[("fengxuezheng", "咳，", "先清嗓子"), ("fengxuezheng", "胡鬧！", "尖聲"), ("fengxuezheng", "給我打！", "揮袖")],
         prompt="medium close-up of Examiner Feng standing beside the dais on screen right in his dark navy official robe and black gauze "
                "hat, his gaunt face sharp and cold, his drooping eyes narrowed at Xu Yan off screen left",
         motion="he clears his throat with a fist at his mouth, then flings his wide sleeve out toward the runners, his thin lips twisting",
         zh="馮學正中近景在右、站在高台旁，深藍官服、烏紗，乾瘦的臉冷下來，下垂的眼睛瞇著看畫外左邊的許硯；拳頭抵嘴清一下嗓子，大袖往衙役那邊一甩"),
    dict(cam="Medium shot, low angle, slow push in", set=COURT, chars=["chuzhifu"],
         lines=[("chuzhifu", "慢著。", "沉聲"), ("chuzhifu", "給他們紙。", "不怒自威")],
         prompt="medium shot from a low angle of Prefect Chu seated behind the red-draped judge's desk on the dais, the painted sea and red "
                "sun on the screen behind him, his square face composed, one hand raised flat with the palm out",
         motion="he lowers the raised hand slowly onto the desk and leans forward over it, his deep-set eyes moving from one writing desk "
                "to the other",
         zh="低角度：褚知府坐在高台的紅布公案後，背後是海浪紅日的屏風，方臉沉穩，一手平平舉起；手慢慢放回桌上、身子往前一傾，眼睛在兩張書案之間來回"),
    dict(cam="Close-up, locked", set=COURT, chars=["xuyan"],
         lines=[("xuyan", "字背得出來，", "平靜"), ("xuyan", "水車呢？", "嘴角一勾")],
         prompt="close-up of Xu Yan's face on screen left, the corner of his mouth lifting into a thin confident smile, his eyes on Wei Xun "
                "off screen right",
         motion="he tilts his head a little to one side and folds his arms across his chest, the smile staying",
         zh="許硯特寫在左，嘴角勾起一個有把握的淺笑，看著畫外右邊的魏珣；頭微微一偏、雙手抱胸"),
    # ---------------- 畫水車
    dict(ch="畫水車", insert=True, act=2, cam="Insert of the blank paper on the desk, locked", set=COURT, chars=[],
         prompt="insert of the right writing desk from above, a runner's hand in a black sleeve slapping one fresh blank sheet of white "
                "paper down beside an ink stone, a finished essay pushed to the edge",
         motion="the black-sleeved hand slaps the blank sheet flat and pulls away out of frame, the paper corner lifting once and settling",
         zh="插鏡：右邊書案的俯角，一隻黑袖子的手把一張全新的白紙「啪」地拍在硯台旁，寫好的卷子被推到桌邊；手抽走，紙角翹一下又落平"),
    dict(act=3, cam="Medium close-up, slow push in", set=COURT, chars=["weixun"],
         prompt="medium close-up of Wei Xun seated at the right writing desk on screen right, a brush in his long slender fingers held over "
                "the blank sheet, a bead of sweat at his temple, his phoenix eyes fixed on the empty paper, his lips pressed thin",
         motion="the brush tip hovers and trembles a finger's width above the paper, then he presses it down and drags it around in one "
                "slow wobbling curve, his shoulders hunching",
         zh="魏珣中近景在右、右邊書案後，修長的手指捏著筆懸在白紙上，太陽穴一滴汗，鳳眼死盯著空白的紙、嘴唇抿緊；筆尖抖了一下，按下去，慢慢拖出一道歪歪扭扭的弧，肩膀縮起來"),
    dict(tag="中段鉤子／奇觀", insert=True, act=2, cam="Overhead insert of Wei Xun's paper, locked", set=COURT, chars=[],
         prompt="overhead insert of the white sheet on the right writing desk, one lopsided wobbly ink circle in the middle of it with a "
                "blot where the brush stopped, nothing else drawn inside it, a pale hand with long slender fingers and a moon-white silk cuff "
                "holding the brush at the edge",
         motion="the brush lifts off the end of the circle and hangs over it, a drop of ink falling and spreading into a fat blot",
         zh="俯角插鏡：右邊書案的白紙上只有一個歪歪扭扭的墨圈，筆停的地方一團墨漬，圈裡什麼都沒有；月白錦袖、修長的手拿著筆停在紙邊；筆抬起懸著，一滴墨掉下來暈開"),
    dict(act=3, cam="Wide shot, slow pan right", set=COURT, chars=["xuyan"],
         prompt="wide shot from behind the low wooden rail, the crowd of examinees in the foreground on tiptoe craning their necks toward "
                "the hall, Xu Yan beyond them at the left writing desk on screen left drawing fast on a fresh white sheet",
         motion="the examinees push up onto their toes and lean over the rail one after another, while Xu Yan's brush sweeps across the "
                "paper in long sure strokes",
         zh="【奇觀】從欄杆後拍的全景：前景一排考生踮腳伸長脖子往堂裡看，遠處許硯在左邊書案後，在新的白紙上飛快地畫；考生一個接一個踮起來、趴到欄杆上，許硯的筆一長筆一長筆地掃過紙面"),
    dict(cam="Medium close-up, locked", set=COURT, chars=["xuyan"],
         lines=[("xuyan", "十二片葉板，", "邊畫邊說"), ("xuyan", "斜三分。", "篤定")],
         prompt="medium close-up of Xu Yan seated at the left writing desk on screen left, leaning over a white sheet with a brush in his "
                "right hand, his eyes on the paper and his brows drawn together in focus",
         motion="his brush flicks out one short angled stroke after another around the edge of the drawing, his wrist turning with each one",
         zh="許硯中近景在左、左邊書案後，俯身在白紙上，右手拿筆，眼睛盯著紙、眉頭專注地皺起；手腕一轉一轉，沿著圖的外圈一筆一筆點出斜斜的短筆"),
    dict(insert=True, act=3, cam="Overhead insert of Xu Yan's drawing, slow push in", set=COURT, chars=[],
         prompt="overhead insert of the white sheet on the left writing desk, an ink drawing of a big water wheel taking shape: a round rim, "
                "spokes from the hub and short angled paddles all slanting the same way, a hand in a faded blue-grey sleeve adding the last "
                "paddles with a brush",
         motion="the brush lays down the last three paddles one by one, each stroke slanting the same way as the others, and lifts away",
         zh="【奇觀】俯角插鏡：左邊書案的白紙上，一架大水車的墨圖成形：圓輪、輪軸放出去的輻條、一圈斜向同一邊的短葉板；青灰袖子的手一筆一筆補上最後三片葉板，筆抬走"),
    dict(cam="Medium close-up, locked", set=COURT, chars=["chengshanzhang"],
         lines=[("chengshanzhang", "沒錯，", "撫鬚，點頭"), ("chengshanzhang", "就是這架。", "篤定")],
         prompt="medium close-up of Headmaster Cheng seated on a side bench by the left wall of the hall on screen left, his silver beard on "
                "his chest and a rolled book scroll in his lap, his warm sharp eyes on the drawing off screen right",
         motion="he strokes his long silver beard down once with one hand and nods slowly, the scroll steady in his other hand",
         zh="程山長中近景在左、坐在大堂左牆邊的旁聽長凳上，銀白長鬚垂在胸前，書卷擱在膝上，溫潤銳利的眼睛看著畫外右邊的圖；一手順著長鬚往下捋，慢慢點頭"),
    dict(tag="中段鉤子", cam="Wide shot, slow push in", set=COURT, chars=["chuzhifu", "xuyan", "weixun"],
         lines=[("chuzhifu", "葉板，", "探身"), ("chuzhifu", "為何倒著裝？", "考問")],
         prompt="wide shot from the floor toward the dais, Xu Yan at the left writing desk on screen left and Wei Xun at the right writing "
                "desk on screen right in the foreground, Prefect Chu behind the red-draped judge's desk on the dais in the centre leaning "
                "forward on his elbows",
         motion="Prefect Chu points one finger down from the dais at Wei Xun's desk, and Wei Xun shrinks back on his stool",
         zh="從堂下往高台拍的全景：前景左邊書案後是許硯、右邊書案後是魏珣，褚知府在中間高台的公案後，雙肘撐桌往前探；知府一根手指從高台往下點著魏珣的書案，魏珣在凳子上往後縮"),
    dict(cam="Medium close-up, slow push in", set=COURT, chars=["xuyan"],
         lines=[("xuyan", "頭一回裝反了，", "老實說"), ("xuyan", "水車不轉。", "笑了一下")],
         prompt="medium close-up of Xu Yan standing up behind the left writing desk on screen left, holding his water wheel drawing up in "
                "both hands toward Prefect Chu off screen right, a rueful honest smile on his face",
         motion="he turns the drawing upside down in his hands and then back again, showing the paddles flipping the other way",
         zh="許硯中近景在左、從左邊書案後站起來，雙手把水車圖舉向畫外右邊的知府，臉上一個老實又有點自嘲的笑；把圖倒過來再翻回去，比給知府看葉板反過來的樣子"),
    dict(cam="Close-up, locked", set=COURT, chars=["xuyan"],
         lines=[("xuyan", "我小妹拿風車一比，", "想起來，聲音軟了"), ("xuyan", "我才翻過來。", "笑")],
         prompt="close-up of Xu Yan's face on screen left, his gaze going soft and far away at the memory of his little sister, a warm "
                "boyish grin tugging at one corner of his mouth, one hand lifted beside his cheek with the index finger raised",
         motion="he lifts one hand and twirls a finger in a small circle in the air like a spinning pinwheel, the smile widening",
         zh="許硯特寫在左，想起什麼眼神軟下來，一個溫的小笑，圖低低拿在胸前，看著畫外右邊的知府；抬起一隻手在空中轉一個小圈，像在比一支紙風車，笑得更開"),
    dict(cam="Medium close-up, locked", set=COURT, chars=["chengshanzhang"],
         lines=[("chengshanzhang", "考前，", "站起來"), ("chengshanzhang", "他在老夫書齋", "一字一句"), ("chengshanzhang", "畫過這架。", "作證")],
         prompt="medium close-up of Headmaster Cheng rising from the side bench by the left wall on screen left, the rolled book scroll in "
                "one hand, his long silver brows lifted, his eyes on Prefect Chu off screen right",
         motion="he rises to his feet with a hand on his knee and raises the rolled scroll toward the dais like a pointer, his beard swaying",
         zh="程山長中近景在左、從左牆邊的長凳站起來，一手拿書卷，銀白長眉揚起，看著畫外右邊高台上的知府；扶膝站起，把書卷朝高台一指，長鬚一晃"),
    dict(cam="Medium close-up, locked", set=COURT, chars=["chuzhifu"],
         lines=[("chuzhifu", "魏珣，", "轉頭"), ("chuzhifu", "你的水車呢？", "冷")],
         prompt="medium close-up of Prefect Chu behind the red-draped judge's desk on the dais, the painted red sun behind his black gauze "
                "hat, his thick brows lowering, his eyes turning down toward Wei Xun off screen right",
         motion="he turns his head slowly from left to right toward Wei Xun and taps one finger twice on the desk",
         zh="褚知府中近景在高台公案後，烏紗後面是屏風上的紅日，濃眉壓下來，眼睛轉向畫外右邊的魏珣；頭慢慢從左轉到右，一根手指在桌上敲兩下"),
    dict(tag="揭穿", cam="Close-up, slow push in", set=COURT, chars=["weixun"],
         lines=[("weixun", "我……", "慌，聲音發緊"), ("weixun", "我背的是……", "說溜嘴")],
         prompt="close-up of Wei Xun's face on screen right, sweat on his fair forehead, his phoenix eyes darting, his lips trembling, the "
                "brush still in his raised hand, his eyes on Prefect Chu off screen left",
         motion="he swallows hard, then his eyes go wide in horror at his own words and he clamps his free hand over his mouth",
         zh="魏珣的臉在右，白淨的額頭冒汗，鳳眼亂飄、嘴唇發抖，筆還舉在手上，看著畫外左邊的知府；用力嚥一下口水，說完自己嚇到眼睛瞪大，空著的手一把捂住嘴"),
    dict(insert=True, act=1, cam="Insert of the falling brush, locked", set=COURT, chars=[],
         prompt="insert of the right writing desk, a writing brush falling from long slender fingers in a moon-white silk cuff onto the white "
                "sheet with the lopsided ink circle",
         motion="the brush drops, bounces once on the paper and rolls across it, leaving a long black ink streak through the circle",
         zh="插鏡：右邊書案，毛筆從月白錦袖、修長的手指間掉下來，落在畫著歪墨圈的白紙上；彈一下、滾過去，在圈上拖出一道長長的黑墨痕"),
    dict(tag="爽點", cam="Close-up, locked", set=COURT, chars=["xuyan"],
         lines=[("xuyan", "背的？", "抓住了"), ("xuyan", "背誰的？", "笑，慢慢地")],
         prompt="close-up of Xu Yan's face on screen left, one eyebrow arching, a slow sharp smile spreading, his eyes on Wei Xun off screen right",
         motion="he leans in a little toward Wei Xun and lets the smile widen, his eyes not leaving him",
         zh="許硯特寫在左，一邊眉毛挑起，一個慢慢展開的銳利的笑，看著畫外右邊的魏珣；身子往魏珣那邊探一點，笑意更深，眼睛一直沒離開他"),
    # ---------------- 摺紙
    dict(ch="摺紙", cam="Medium close-up, slow push in", set=COURT, chars=["fengxuezheng"],
         lines=[("fengxuezheng", "咳，", "清嗓子，急"), ("fengxuezheng", "書生背書，", "硬撐"), ("fengxuezheng", "有何稀奇！", "拔高")],
         prompt="medium close-up of Examiner Feng beside the dais on screen right, his gaunt face going grey, a thin sheen of sweat on his "
                "high cheekbones, his drooping eyes shifting toward Prefect Chu off screen left",
         motion="he clears his throat hard and takes one quick step toward the dais, both hands cupped together in a stiff bow",
         zh="馮學正中近景在右、高台旁，乾瘦的臉灰下來，高顴骨上一層薄汗，下垂的眼睛往畫外左邊的知府飄；用力清一下嗓子，往高台搶一步，雙手一拱"),
    dict(cam="Wide shot, locked", set=COURT, chars=["xuyan", "weixun", "chuzhifu"],
         lines=[("tangxiaotang", "大人！", "畫外，清亮"), ("tangxiaotang", "民女有東西呈上！", "畫外")],
         prompt="wide shot from the dais toward the open front doors, Xu Yan at the left writing desk and Wei Xun at the right writing desk "
                "in the middle of the hall, Prefect Chu's crimson shoulder and black gauze hat at the bottom of the frame, the sunlit doorway "
                "beyond them; Tang Xiaotang speaks off screen from the doorway",
         motion="every head in the hall turns toward the bright doorway at once, Xu Yan rising half out of his seat and Wei Xun freezing",
         zh="從高台往大門拍的全景：大堂中間左邊書案後是許硯、右邊書案後是魏珣，畫面下緣是知府的緋色肩膀和烏紗，再過去是亮晃晃的大門；唐小棠在門口（畫外）喊；堂裡的人一起轉頭看門口，許硯半站起來，魏珣僵住"),
    dict(tag="顏值鏡頭", cam="Medium shot, slow push in", set=COURT, chars=["tangxiaotang"],
         lines=[("tangxiaotang", "那個魏家的人，", "甜但字字清楚"), ("tangxiaotang", "又來找馮大人了。", "揚眉")],
         prompt="medium shot of Tang Xiaotang standing in the open front doorway of the hall in the sunlight, in her fitted peach-pink silk "
                "ruqun with the high stand-up collar fastened at her throat, one arm raised high holding up a folded paper packet the size "
                "of a palm, the sun lighting her sweet profile, the small gold abacus swinging at her waist, her eyes on Examiner Feng off "
                "screen left",
         motion="she steps over the threshold with the packet held high and the gold abacus swings at her hip",
         zh="【顏值鏡頭】唐小棠站在大堂敞開的門口、陽光裡，合身的桃粉綢襦裙、高立領扣到喉頭，一手把一個巴掌大的摺紙包高高舉起，陽光照著她嬌俏的側臉，腰間的小金算盤一晃，眼睛看著畫外左邊的馮學正；她舉著紙包跨過門檻，綢袖順著舉高的手臂滑下來，金算盤在腰側晃一下停住"),
    dict(cam="Medium close-up, locked", set=COURT, chars=["tangxiaotang"],
         lines=[("tangxiaotang", "這是第二包，", "笑得很甜"), ("tangxiaotang", "我替他收了。", "眨眼")],
         prompt="medium close-up of Tang Xiaotang just inside the doorway on screen right, her high stand-up collar fastened at her throat, "
                "the folded paper packet held up beside her cheek between two fingers, her dimples showing in a sweet sly smile, her eyes on "
                "Examiner Feng off screen left",
         motion="she gives the packet a little shake beside her cheek and then holds it out at arm's length toward the dais",
         zh="唐小棠中近景在右、剛進門，高立領扣到喉頭，兩根手指夾著摺紙包舉在臉旁，酒窩一現、笑得又甜又精，看著畫外左邊的馮學正；紙包在臉旁輕輕一晃，再把手臂伸直遞向高台"),
    dict(insert=True, act=2, cam="Insert of the opened packet, locked", set=COURT, chars=[],
         prompt="insert of the red-draped judge's desk, two hands in wide crimson official sleeves unfolding a paper packet, inside it a "
                "stiff oblong paper money draft covered in columns of faint brush strokes with one square red seal stamp on it",
         motion="the crimson-sleeved hands peel the last fold open and smooth the draft flat on the red cloth, the red seal facing up",
         zh="插鏡：紅布公案上，緋色大袖的兩隻手打開紙包，裡面是一張硬挺的長方形銀票，一列列淡淡的毛筆畫（不寫字），蓋著一方紅印；手把最後一摺翻開，把銀票在紅布上抹平，紅印朝上"),
    dict(cam="Medium close-up, slow push in", set=COURT, chars=["chuzhifu"],
         lines=[("chuzhifu", "五百兩，", "唸出來，聲音一沉"), ("chuzhifu", "見榜付清。", "冷")],
         prompt="medium close-up of Prefect Chu behind the judge's desk on the dais, the paper money draft held up in both hands in front "
                "of his chest, his thick brows drawing down hard, his eyes lifting over the paper to Examiner Feng off screen right",
         motion="he lowers the draft slowly until his whole face shows above it, his jaw setting",
         zh="褚知府中近景在高台公案後，雙手把銀票舉在胸前，濃眉狠狠壓下來，眼睛從紙上抬起看畫外右邊的馮學正；銀票慢慢放低，整張臉露出來，下顎咬緊"),
    dict(tag="揭穿", cam="Close-up, locked", set=COURT, chars=["tangxiaotang"],
         lines=[("tangxiaotang", "這方印我認得，", "笑意收起"), ("tangxiaotang", "魏少卿的管家。", "冷冷地")],
         prompt="close-up of Tang Xiaotang's face on screen right, her high stand-up collar fastened at her throat, the sweet smile gone, her "
                "round eyes cold and level, her eyes on Prefect Chu off screen left",
         motion="her chin lifts a little and her lips press together after the words, her eyes hard and unblinking",
         zh="唐小棠特寫在右，高立領扣到喉頭，甜笑收起來，圓圓的眼睛冷而平，看著畫外左邊的知府；說完下巴微抬、嘴唇一抿，眼神硬、不眨"),
    dict(cam="Close-up, slow push in", set=COURT, chars=["fengxuezheng"],
         lines=[("fengxuezheng", "大人，", "腿軟"), ("fengxuezheng", "下官冤……", "聲音發抖")],
         prompt="close-up of Examiner Feng's face on screen right, all the colour drained from his gaunt face, his thin lips shaking, his "
                "black gauze hat crooked, his eyes on Prefect Chu off screen left",
         motion="his knees give and he sinks down out of the bow toward the floor, his hat wings trembling",
         zh="馮學正的臉在右，乾瘦的臉一點血色都沒有，薄唇發抖，烏紗歪了，看著畫外左邊的知府；膝蓋一軟，從作揖的姿勢往地上滑下去，帽翅直抖"),
    dict(cam="Medium shot, locked", set=COURT, chars=["chuzhifu"],
         lines=[("chuzhifu", "拿下！", "一拍驚堂木")],
         prompt="medium shot of Prefect Chu behind the red-draped judge's desk on the dais, one hand raised high holding a dark wooden "
                "gavel block, his square face stern",
         motion="he brings the gavel block down hard on the desk with a full swing of his arm, the paper money draft jumping on the red cloth",
         zh="褚知府中景在高台公案後，一手高舉黑木驚堂木，方臉一沉；整條手臂掄下來重重一拍，紅布上的銀票跳了一下"),
    dict(tag="爽點", act=3, cam="Wide shot, slow pan left", set=COURT, chars=["fengxuezheng", "weixun"],
         prompt="wide shot of the hall floor, two runners in black seizing Examiner Feng by both arms beside the dais on screen right, Wei "
                "Xun slumped over the right writing desk in the middle, his face hidden in his moon-white sleeve",
         motion="the runners haul Examiner Feng up off his knees and drag him away across the stone floor toward screen left, his black gauze "
                "hat tumbling off, while Wei Xun sinks lower over the desk",
         zh="【爽點】大堂地上的全景：右邊兩個黑衣衙役在高台旁一左一右架住馮學正，中間的魏珣趴在右邊書案上，月白袖子遮住臉；衙役把馮學正從地上拖起來、往左邊拖過石板地，烏紗掉了，魏珣趴得更低"),
    # ---------------- 後堂
    dict(ch="後堂", cam="Wide shot, locked", set=BACK, chars=["chuzhifu", "xuyan"],
         lines=[("chuzhifu", "都下去。", "低聲，揮手")],
         prompt="wide shot of the back hall, Prefect Chu seated in a carved chair by the low tea table on screen right, Xu Yan standing on "
                "screen left with his drawing rolled in one hand, two attendants in grey bowing near the door at the far left",
         motion="Prefect Chu flicks two fingers toward the door and the two attendants back out bowing and slide the door shut behind them",
         zh="後堂全景：褚知府坐在右邊茶几旁的雕花椅上，許硯站在左邊、一手捏著捲起的水車圖，左邊遠處門口兩個灰衣下人躬著身；知府兩根手指朝門一撥，下人躬著退出去、把門拉上"),
    dict(insert=True, act=2, cam="Insert of the money draft on the tea table, locked", set=BACK, chars=[],
         prompt="insert of the low dark tea table between two celadon cups, a hand in a wide crimson official sleeve laying the oblong paper "
                "money draft with its square red seal flat on the wood",
         motion="the crimson-sleeved hand lays the draft down and slides it slowly across the table between the two cups, then lifts away",
         zh="插鏡：兩只青瓷杯之間的深色茶几，緋色大袖的手把那張蓋紅印的長方銀票平放在木桌上；手推著它慢慢滑過兩只杯子之間，然後抬走"),
    dict(cam="Medium close-up, slow push in", set=BACK, chars=["chuzhifu"],
         lines=[("chuzhifu", "告到魏家，", "壓低聲音"), ("chuzhifu", "案子要送京城。", "句句是盤算")],
         prompt="medium close-up of Prefect Chu seated by the tea table on screen right, the slanting golden light on half of his square "
                "face, his voice low, his deep-set eyes on Xu Yan off screen left",
         motion="he leans in over the tea table and lowers his head toward Xu Yan, one finger resting on the edge of the money draft",
         zh="褚知府中近景在右、坐在茶几旁，斜斜的金色光照著半邊方臉，壓低聲音，深陷的眼睛看著畫外左邊的許硯；身子越過茶几湊近，一根手指按在銀票邊上"),
    dict(cam="Close-up, locked", set=BACK, chars=["xuyan"],
         lines=[("chuzhifu", "三年不結，", "畫外，慢"), ("chuzhifu", "你這屆就沒了。", "畫外")],
         prompt="close-up of Xu Yan's face on screen left in the slanting golden light, his jaw tight and his eyes narrowing as he thinks, his "
                "eyes on Prefect Chu off screen right; Prefect Chu speaks off screen",
         motion="his eyes drop from the Prefect's face down to the money draft on the table and back up, his lips pressing into a line",
         zh="許硯特寫在左，斜斜的金光裡，下顎繃緊、眼睛瞇起來在盤算，看著畫外右邊的知府；知府在畫外說；眼睛從知府的臉落到桌上的銀票，再抬回來，嘴唇抿成一線"),
    dict(cam="Medium close-up, locked", set=BACK, chars=["chuzhifu"],
         lines=[("chuzhifu", "只辦馮學正，", "往後一靠"), ("chuzhifu", "你明天，", "慢"), ("chuzhifu", "就是解元。", "一字一字")],
         prompt="medium close-up of Prefect Chu leaning back in the carved chair on screen right, both hands folded on his crimson robe, a "
                "faint knowing look in his steady eyes, his eyes on Xu Yan off screen left",
         motion="he settles back into the chair, lifts a celadon cup from the table and holds it under his chin without drinking",
         zh="褚知府中近景在右、往雕花椅背一靠，雙手交疊在緋袍上，沉穩的眼睛裡一點看透的意思，看著畫外左邊的許硯；坐回椅背，從桌上端起一只青瓷杯停在下巴前，不喝"),
    dict(tag="結尾", cam="Close-up, slow push in", set=BACK, chars=["xuyan"],
         lines=[("xitong", "選擇：扳倒魏家，", "平板電子音，叮一聲"), ("xitong", "或先拿解元。", "平板電子音")],
         prompt="close-up of Xu Yan's face on screen centre in the slanting golden light, his eyes lifting and fixing on a point in the empty "
                "air just in front of him, his jaw set; the system voice speaks off screen",
         motion="his eyes track slowly across the empty air as if reading, then drop down toward the table below the frame",
         zh="【結尾】系統面板：許硯的臉在中間、斜斜的金光裡，眼睛抬起定在面前的空中，下顎咬緊；眼睛像讀字一樣慢慢掃過空中，再往下落向畫面外的茶几",
         ov=[("選擇：扳倒魏家｜或先拿解元", "task")]),
    dict(tag="結尾", insert=True, act=3, cam="Insert of his hand over the money draft, locked", set=BACK, chars=[],
         prompt="insert of the low dark tea table, the oblong money draft with its square red seal lying between the two celadon cups, a hand "
                "in a faded blue-grey sleeve patched at the elbow hovering just above it, a crimson sleeve resting still at the far side of "
                "the table",
         motion="the blue-grey hand lowers slowly until the fingertips are a finger's width above the draft and stops there, the fingers "
                "curling",
         zh="【結尾】最後一格：深色茶几上，蓋紅印的銀票躺在兩只青瓷杯之間，一隻手肘打補丁的青灰袖子的手懸在上方，桌子另一頭緋色的袖子一動不動；手慢慢落下，指尖停在離銀票一指寬的地方，手指蜷起來"),
]

ORDER = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 17, 8, 13, 18, 20, 19, 14, 15, 16] + list(range(21, 38))
assert sorted(ORDER) == list(range(38))
SHOTS = [SHOTS[i] for i in ORDER]

MUSIC = ("a hard drum hit and a held breath of silence as the staves hang in the air, a cold low guqin note under his calm 'draw it', a "
         "sly plucked pipa as the haughty boy's brush wobbles, a warm rising dizi theme as the water wheel paddles appear stroke by stroke "
         "before the craning crowd, a light comic woodblock for the lopsided circle, a sudden comic sting when the boy blurts out 'I "
         "memorised', a soft music-box pluck as he remembers his little sister's pinwheel, a bright brass flourish as the girl lifts the "
         "packet in the sunlit doorway, a deep drum and gong as the gavel falls and the examiner is dragged away, then a hushed back room "
         "of low strings and a ticking temple block under the prefect's offer, a glassy electronic chime for the choice, ending on one long "
         "suspended high string over his hovering hand, ancient Chinese drama, no vocals")

YT_DESC = ("州府大堂上，魏珣當堂把許硯的文章一字不差默了出來，馮學正冷笑「誣告考官，杖三十」，刑杖已經舉起。許硯放下筆：「第三段的水車，你畫出來。」"
           "褚知府准了。許硯三筆兩筆畫出十二片葉板，堂下考生踮腳伸長脖子看；魏珣握著筆，白紙上只畫出一個歪歪扭扭的圓。"
           "知府再問葉板為什麼倒著裝，魏珣脫口而出「我背的是……」。許硯說得出來：頭一回裝反了，是小妹拿紙風車一比才翻過來；程山長起身作證，考前他就在書齋畫過這架水車。"
           "馮學正還想硬撐，唐小棠從堂外舉著一個摺紙包走進來：考前遞摺紙給馮學正的那個魏家家僕，她記住了臉；那人又送來第二包，被她截下。紙包裡是一張蓋了私印的銀票，五百兩，見榜付清；"
           "那方印，唐小棠認得——是魏少卿的管家。馮學正當堂被拿下。後堂裡，褚知府屏退左右，把銀票推到許硯面前：告到魏家，案子送京城三年不結；只辦馮學正，你明天就是解元。"
           "《種田娶妻打天下》第 47 集。")


def SB_HEAD(total, st, du):
    def at(s):
        t = int(st[s]); return f"{t // 60}:{t % 60:02d}"
    return [
        f"{len(SHOTS)} 個鏡頭、四段（刑杖／畫水車／摺紙／後堂），估計約 {total:.0f} 秒（照 lint 估法；真人語速通常再長一成左右）；細綱 110 秒",
        "預算：片段 %d 支（靜圖 0 張），沒有「切素材」鏡。片段走路線 A（Colab H3 Ref2VA 三段式，沒有首格）；秒數見 `hailuo/clips-dh-e047.json`（`gen-dh.mjs` 算），首格清單只當參照圖清單" % len(SHOTS),
        f"開頭 10 秒：接第 46 集的最後一格，刑杖掄到最高（0:00），許硯放下筆「第三段的水車，你畫出來」（{at('s02')}），魏珣「畫……畫什麼？」（{at('s03')}），馮學正「給我打！」（{at('s04')}）；中段鉤子：許硯畫出葉板（{at('s11')}），魏珣的白紙上只有一個歪圓（{at('s14')}），「為何倒著裝？」魏珣說溜嘴「我背的是……」（{at('s16')}），許硯說出為什麼倒著裝（{at('s19')}–{at('s20')}）；轉折：程山長作證（{at('s21')}）、唐小棠呈上摺紙、銀票上的私印（{at('s23')}–{at('s28')}）；結尾收在知府的交換條件、許硯的手懸在銀票上",
        f"鉤子：【鉤子1】s01–s04 0:00、【鉤子2】s05–s08 {at('s05')}、【鉤子3】s09–s14 {at('s09')}、【鉤子4 中段】s15–s18 {at('s15')}、【鉤子5】s19–s21 {at('s19')}、【鉤子6】s22–s25 {at('s22')}、【鉤子7】s26–s31 {at('s26')}、【結尾】s32–s38 {at('s32')}–{int(total) // 60}:{int(total) % 60:02d}",
        "顏值鏡頭：s24 唐小棠（大堂門口的陽光裡把摺紙高高舉起，陽光照著她的側臉，金算盤在腰間一晃）；是臉與動作，不停在身體。許硯在 s02、s06 平日嘻笑的臉一收",
        "爽點：前半 face_slap（s14 魏珣只畫得出歪圓、s16「我背的是……」說溜嘴、s17「背的？背誰的？」）、中段 betrayer_punished（s26–s31 銀票上的私印、馮學正當堂被拿下）",
        "說話鏡頭：說話的人在畫面上的鏡頭，motion 第一句都是他說這句話、嘴唇下巴隨每個音節動；畫外台詞（s23 唐小棠在門外、s35 知府、s37 系統）放在別人的反應鏡上，prompt 寫明 off screen",
        "H3 寫法：motion 寫軌跡、一鏡一事、沒有 camera 字；構圖段寫景別、誰在左右、道具與大小（摺紙包巴掌大）；表情用正面的字；插鏡（s07、s11、s14、s18、s26、s33、s38）motion 開頭寫 `The shot opens directly on this close insert from its very first frame`（lessons §6：只有場景圖的插鏡會先畫一段空景）；畫外的人不寫局部身體；紙上不寫字：文章與銀票只寫 `columns of faint brush strokes`，水車圖是畫不是字",
        "光：s01–s31 大堂白天的亮光（大門外的陽光）；s32–s38 後堂斜斜的午後金光",
        "軸線：大堂從大門往高台看，許硯的書案在左、魏珣的書案在右，知府在中間高台上，馮學正站在高台右邊，程山長坐在左牆邊的旁聽長凳；唐小棠從大門（鏡頭背後）進來，反打時她在右、看畫外左邊的高台；後堂知府在右、許硯在左，茶几在兩人之間",
    ]


SB_FOOT = [
    "場景參考：s01–s31 用 `dh-set-zhoufu-tang-t1`（含 `court hall of the Qingzhou prefecture`）；s32–s38 用 `dh-set-zhoufu-houtang-t1`（含 `prefect's back hall`）。兩張都還沒畫（registry 🎨）。每句 prompt 都避開 `examination hall`、`courtyard` 這類別的場景字。",
    "道具：許硯寫完的文章與水車圖（s01–s16，之後捲起拿在手上 s32）；魏珣的白紙、歪墨圈、掉下來的筆（s07–s08、s14、s18）；衙役的紅黑刑杖（s01）；黑木驚堂木（s30）；巴掌大的摺紙包與裡面蓋紅印的銀票（s24–s28、s33、s38）；程山長的書卷（s13、s17）；兩只青瓷杯（s32–s38）。",
    "連戲：開場照第 46 集的結尾（魏珣默完「一字不差」、馮學正「杖三十」、衙役喊堂威、刑杖舉起，刑杖的影子落在許硯還在寫的紙上）接，s01 刑杖在最高點、影子還壓在紙上，許硯寫完最後一筆才放下筆，s02 前 3 秒就是細綱的 hook。第 46 集兩人都已默完全文，所以 s07 是給魏珣一張新的白紙、s09 許硯也在新紙上畫。s19–s20 的「裝反了」「小妹拿風車一比」照第 34 集（小禾的紙風車、十二片葉板翻過來）；s10「十二片葉板，斜三分」照第 33 集的台詞；s21 程山長作證照第 43 集（他拿治旱考許硯、許硯在書齋畫過水車）。s24–s28 的摺紙包接第 43 集的中段鉤子（馮學正從魏家家僕手裡收了一張摺紙）：第 43 集唐小棠在考場外認出那身魏家的衣服、記住了那個家僕的臉（「我記住你了」），第一包（「清水縣，許硯」）馮學正在彌封房燒了；這是同一個家僕來付尾款的第二包，被唐小棠截下。s28 唐小棠認得管家的印，因為她被逼許給魏少卿（m04，第一季已揭）。秦霜本集不出場（細綱沒有她），在堂外等。第 48 集從許硯把銀票摺好收進袖子接。",
    "短線 s01-t11（調包卷子的考官背後是魏家的誰？）在 s26–s28 收：銀票上的私印是魏少卿的管家。宰相、魏家要秦家玉佩的事（m03、m05、m11）一句都不碰。",
    "系統面板不由模型畫：s37 的選擇在剪接時疊上（task）。",
    "新的參照圖還沒畫：魏珣、馮學正、褚知府、程山長的定妝照（`refs-dh/weixun-portrait-t1.png`、`fengxuezheng-portrait-t1.png`、`chuzhifu-portrait-t1.png`、`chengshanzhang-portrait-t1.png`）與兩張場景圖（`set-zhoufu-tang-t1.png`、`set-zhoufu-houtang-t1.png`）；本集每一鏡都要其中一張，畫好之前不能開拍。",
]


def BRIEF(st, du, total):
    def at(s):
        t = int(st[s]); return f"{t // 60}:{t % 60:02d}"
    return f"""# 《種田娶妻打天下》第 47 集〈畫出來〉

## 故事前提

第 46 集收在州府大堂：魏珣寫完最後一字，筆往桌上一拍「一字不差」，馮學正冷笑「誣告考官」「杖三十」，衙役舉起刑杖。第 47 集從同一個畫面接下去：兩根紅黑刑杖掄到最高點（s01），許硯看都不看，把毛筆平平放回桌上，抬手一指魏珣：「第三段的水車，」「你畫出來。」（s02，細綱的 hook，0:02 就回答了上一集的問題「對方也一字不差，他怎麼證明是自己寫的？」——背得出字，背不出那段經歷）。魏珣鳳眼一睜「畫……畫什麼？」；馮學正「咳，胡鬧！給我打！」；褚知府一抬手「慢著。」「給他們紙。」；許硯抱胸一笑：「字背得出來，」「水車呢？」

衙役在魏珣桌上拍下一張新的白紙。魏珣的筆尖懸在紙上直抖；欄杆外的考生一個接一個踮腳伸長脖子（s09，細綱的奇觀），許硯邊畫邊說「十二片葉板，」「斜三分。」，白紙上一架水車一筆一筆成形（s11）。程山長撫鬚「沒錯，就是這架。」知府轉頭：「魏珣，」「你的水車呢？」——魏珣的白紙上只有一個歪歪扭扭的墨圈（s14，細綱的 mid_hook 前半）。知府再問：「葉板，」「為何倒著裝？」魏珣慌了「我……我背的是……」，說完自己捂住嘴；許硯慢慢笑開：「背的？」「背誰的？」魏珣的筆從指間掉下來，在歪圈上拖出一道墨痕（first_half face_slap：魏珣當堂露餡。）許硯把圖倒過來又翻回去：「頭一回裝反了，」「水車不轉。」「我小妹拿風車一比，」「我才翻過來。」（細綱的 mid_hook 後半與 turn：說出為什麼倒著裝、講出柳溪的事。）程山長站起來作證：「考前，」「他在老夫書齋」「畫過這架。」

馮學正還想硬撐「書生背書，有何稀奇！」，門口一聲「大人！民女有東西呈上！」——唐小棠站在大門的陽光裡，把一個巴掌大的摺紙包高高舉起（s24，細綱的顏值鏡頭）：「那個魏家的人，」「又來找馮大人了。」「這是第二包，」「我替他收了。」知府打開紙包，裡面是一張蓋了紅印的銀票：「五百兩，」「見榜付清。」唐小棠甜笑一收：「這方印我認得，」「魏少卿的管家。」（payoff s01-t11：調包卷子的考官背後是魏少卿的管家。）馮學正腿一軟「大人，下官冤……」，知府一拍驚堂木「拿下！」，衙役把他拖出大堂，魏珣趴在書案上把臉埋進袖子（midpoint betrayer_punished）。

後堂裡，知府揮手「都下去。」，把銀票推到兩只茶杯中間，壓低聲音：「告到魏家，」「案子要送京城。」「三年不結，」「你這屆就沒了。」往椅背一靠：「只辦馮學正，」「你明天，」「就是解元。」系統：「選擇：扳倒魏家，」「或先拿解元。」收在許硯的手懸在銀票上方一指寬的地方（細綱的 cliffhanger，choice：「扳倒魏家，還是先拿解元？」；第 48 集從許硯把銀票摺好收進袖子接）。

本集細綱：`docs/videos/series-plans/zhong-tian-qu-qi/season-01.json` 第 47 集（110 秒，第一季第五章，調性權謀＋爽，lead_arc wins）。hook 是許硯放下筆「第三段的水車，你畫出來」（0:00–0:05，line）；mid_hook 是許硯畫出葉板、魏珣只畫出歪圓、許硯說得出為什麼倒著裝（{at('s09')}–{at('s21')}，歪圓在 {at('s14')}）；衝突是背得出字背不出經歷，而馮學正背後的人還沒露面（s22–s28）；turn 是程山長作證（s21）與唐小棠呈上截下的摺紙、銀票上的魏家私印（s23–s28）；cliffhanger 是知府屏退左右的交換條件（s32–s38，choice）。satisfaction：first_half face_slap（s14、s16–s18）、midpoint betrayer_punished（s26–s31）。general_payoffs 全部入鏡：魏珣當堂露餡（s14、s16–s18）、馮學正收魏家銀票調包的證據到手、出錢的是魏少卿的管家（s26–s28）。本集觀眾跟許硯知道的一樣多（第 43 集觀眾已看過調包），authoring.md：一集只選一種。

## 鉤子（站主 10-16：開場、結尾之外中段還要兩三個以上）

| 鉤子 | 鏡 | 約略時間 | 內容 |
| --- | --- | --- | --- |
| 【鉤子1】開場 | s01–s04 | 0:00–{at('s05')} | 刑杖掄到最高，許硯放下筆「第三段的水車，你畫出來」，馮學正「給我打！」（他要證明什麼？） |
| 【鉤子2】 | s05–s08 | {at('s05')}–{at('s09')} | 知府「給他們紙」，「字背得出來，水車呢？」，魏珣的筆懸在白紙上直抖 |
| 【鉤子3】 | s09–s14 | {at('s09')}–{at('s15')} | 葉板一筆一筆成形，考生踮腳看，「魏珣，你的水車呢？」——白紙上只有一個歪圓 |
| 【鉤子4】中段鉤子 | s15–s18 | {at('s15')}–{at('s19')} | 「葉板，為何倒著裝？」「我背的是……」，「背的？背誰的？」筆掉了 |
| 【鉤子5】 | s19–s21 | {at('s19')}–{at('s22')} | 「頭一回裝反了」「我小妹拿風車一比」，程山長作證「考前他在老夫書齋畫過這架」 |
| 【鉤子6】 | s22–s25 | {at('s22')}–{at('s26')} | 「有何稀奇！」門口「大人！」唐小棠舉著摺紙「那個魏家的人，又來找馮大人了」（包裡是什麼？） |
| 【鉤子7】 | s26–s31 | {at('s26')}–{at('s32')} | 「五百兩，見榜付清」「這方印我認得，魏少卿的管家」，「拿下！」 |
| 【結尾】 | s32–s38 | {at('s32')}–{int(total)//60}:{int(total)%60:02d} | 「都下去」，「告到魏家，三年不結」「只辦馮學正，你明天就是解元」，手懸在銀票上（扳倒魏家，還是先拿解元？） |

## 角色

- 許硯（xuyan）：s02「第三段的水車，你畫出來」；s06「字背得出來，水車呢？」；s10 邊畫邊說「十二片葉板，斜三分」；s17「背的？背誰的？」；s19–s20 講裝反了與小妹的風車；s35 聽知府開條件（只拍臉）；s37 看系統的選擇（只拍眼睛）。s01、s09、s15、s23、s32 在畫面裡不說話。
- 魏珣（weixun）：s03「畫……畫什麼？」；s08 握筆抖、s14 白紙上的歪圓；s16「我……我背的是……」說溜嘴；s18 筆掉下來；s31 趴在書案上。外貌照 cast.json（月白錦袍、紫香囊），還沒有定妝照。
- 馮學正（fengxuezheng）：s04「咳，胡鬧！給我打！」；s22「咳，書生背書，有何稀奇！」；s29「大人，下官冤……」；s31 被衙役架走。開口前先清嗓子（cast.json 的聲音說明）。
- 褚知府（chuzhifu）：s05「慢著。給他們紙」；s13「魏珣，你的水車呢？」；s15「葉板，為何倒著裝？」；s27「五百兩，見榜付清」；s30「拿下！」；後堂 s32–s36 屏退左右、開條件。謹慎但不糊塗：在大堂只辦眼前的證據，交換條件只在後堂說。
- 程山長（chengshanzhang）：坐在左牆邊旁聽（第 46 集唐小棠與秦霜請來的）。s12「沒錯，就是這架」；s21「考前，他在老夫書齋畫過這架」作證。
- 唐小棠（tangxiaotang）：s23 在門外喊（畫外）；s24 顏值鏡頭、舉起摺紙「那個魏家的人，又來找馮大人了」；s25「這是第二包，我替他收了」；s28「這方印我認得，魏少卿的管家」。她出現的每一個 prompt 都寫高立領。
- 系統（xitong）：沒有身體，只有聲音與剪接時疊上的面板（`overlays.json`：s37 選擇）。
- 衙役、旁聽的考生、後堂的下人：背景，只寫在 prompt 裡（runners、examinees、attendants），沒有台詞。秦霜在堂外，本集不出場（細綱沒有她）。

## 地點（固定的地點字）

- 州府大堂（白天）：`In the court hall of the Qingzhou prefecture in bright daylight`（s01–s31，新場景 `dh-set-zhoufu-tang-t1`，還沒畫）：後方高台、紅布公案、海浪紅日的屏風（不寫匾額，畫面不能有字）、兩排拿紅黑刑杖的衙役、石板地中間兩張並排的小書案、敞開的大門外是陽光下的前庭與欄杆後的考生。
- 州府後堂（午後）：`In the prefect's back hall in late afternoon light`（s32–s38，新場景 `dh-set-zhoufu-houtang-t1`，還沒畫）：雕花格窗、深色矮茶几、兩只青瓷杯、兩張雕花椅、水墨山水屏風、斜斜的金光。
- 站位（軸線）：見分鏡表開頭。

## 站主觀點

站主 2026-10-16 的要求：女生要火辣漂亮，濃顏系的五官與妝、合身剪裁；不露、不濕身、鏡頭不停在身體部位；每集至少一個顏值鏡頭；結尾收在最高點；不被黃標；每集開場、結尾之外中段再兩三個以上鉤子。本集的顏值鏡頭是 s24（唐小棠在大門的陽光裡高舉摺紙，照的是側臉與舉手的動作），另有細綱指定的許硯 s02（嘻笑的臉一收、眉眼銳利）。唐小棠每一鏡都寫高立領。沒有人被打：刑杖舉起沒有落下（s01），馮學正只被架走（s31）。紙上不畫字：文章、銀票只寫成一列列淡淡的筆畫，銀票上的印是一方紅印、沒有能讀的字；水車圖是畫。系統面板不由模型畫，s37 只拍許硯的眼睛。

分鏡照 `storyboard-rules.md` 2026-10-28 起的 H3 寫法（與第 42 集同）：說話的人在畫面上時 motion 第一句寫他說這句話；motion 寫軌跡、一鏡一事；表情寫成正面的字；道具寫大小；畫外的人不寫局部身體；運鏡只在 `camera`，motion 裡沒有 camera 字；`locked` 就是鎖定；秒數由 `gen-dh.mjs` 決定，`video.json` 不寫 buy_seconds。本集沒有靜圖、沒有切素材鏡。角色外觀照 `production/cast.json` 逐字照抄。
"""
