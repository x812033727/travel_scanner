EP = 53
EP_TITLE = "渡口截車"
OUTLINE_SECONDS = 120
TARGET_MINUTES = [1, 3]
TITLE = "囚車出城就要讓她消失，冷面老婆策馬狂追：衝！｜種田娶妻打天下 第53集"
DESCRIPTION = "囚車天沒亮就出了北門，押車的不是州府的人。阿令勒馬一個迴旋，一把把許硯拉上馬背：「抓緊。」許硯不會騎馬，只能抓著馬鞍大喊：「衝！」王二牛帶著柳溪的少年們連夜追來。北邊渡口的淺灘上，囚車停在河裡，押解頭目鄧押司拔刀，十幾個帶刀的人圍住囚籠。許硯不求打贏，只求把槍送到她手上——一桿紅纓長槍拋進籠裡。秦霜接槍、撬斷籠門，淺灘上水花炸開，兩把刀同時飛上半空落進河裡。許硯舉起追回令，對方猶豫了；鄧押司抓住阿令的馬韁：「我知道她是誰。」許硯打斷他：「她是誰，她自己說。」鄧押司退到水邊，從懷裡掏出一封信對秦霜晃：「放我走，給妳爹的信。」《種田娶妻打天下》第 53 集。"
THUMB = ("衝！", "s21")
CHARACTERS = ["xuyan", "aling", "erniu", "qinshuang", "dengyasi", "xitong"]
MINOR = {}
MUSIC = "galloping war drums from the first frame as the horse wheels in the dust, a breathless comic woodblock and squeaking reed when he clutches the saddle, a wide heroic dizi over the official road, a rowdy brass and clapping drums as the village lads catch up, a low tense string over the fresh cart ruts, then a cold heavy drone at the ford as a dozen sabers come out, a held breath and a single rising string as the spear flies over their heads, a crashing drum and splashing percussion as the cage breaks, a fierce fast pipa and erhu duel through the shallows, a proud bright horn on her glamour pose, a stern low brass under the recall order, a cold guqin note when he says she will tell it herself, then a slow menacing cello and a trembling high string as the letter is waved, cut on the held breath, ancient Chinese rural drama, no vocals"

LOC = {
    "road": "On the official road outside the north gate of Qingzhou at midday, a wide packed-earth road between dry fields and poplars, a stone milestone, deep cart ruts, the grey city wall and its gate tower behind, dust hanging in the pale sky",
    "ford": "At the shallow ford of the north ferry outside Qingzhou in the afternoon, a wide slow river running knee-deep over pebble shoals, a rough log raft tied to a post, reeds and sandbanks, a muddy cart track running down into the water, the far bank misty",
}
LIGHT = {}

SHOTS = [
    dict(chapter="抓緊", loc="road", cam="Wide shot, tracking", chars=["aling", "xuyan"], act=2, tag="鉤子1／開頭",
         comp="wide shot on the road by the stone milestone, A-ling on a bay horse on screen left wheeling it round in a tight circle, a red-tasselled spear strapped along the saddle, Xu Yan standing in the dust on screen right with his arms half raised",
         motion="the horse spins on its hind legs in one full turn, kicking up a ring of dust, and A-ling leans down from the saddle with her hand held out to him",
         zh="接第 52 集：官道里程碑旁的全景，阿令在左騎著棗紅馬原地一個迴旋，馬鞍邊綁著那桿紅纓長槍，許硯在右站在塵土裡、兩手半舉；馬後腿一轉繞一整圈，揚起一圈灰，阿令從馬上俯身朝他伸出手"),
    dict(loc="road", cam="Two-shot, locked", chars=["aling", "xuyan"], tag="鉤子1",
         comp="two-shot beside the horse, A-ling in the saddle on screen left gripping Xu Yan's wrist, Xu Yan on screen right with one foot in the stirrup, dust in the air",
         lines=[("aling", "上來。", "很短")],
         motion="she hauls him up by the wrist and he scrambles over the horse's back to sit behind her",
         zh="雙人鏡：馬邊，阿令在左坐在馬上抓住許硯的手腕，許硯在右一腳踩進馬鐙；她抓著手腕一把把他拉上去，他手忙腳亂地爬到她背後坐好"),
    dict(loc="road", cam="Medium close-up, locked", chars=["xuyan"], tag="鉤子1",
         comp="medium close-up of Xu Yan sitting behind A-ling on the horse, his hands clutching the back of the saddle, his eyes wide with panic, looking down at the ground",
         lines=[("xuyan", "等等，", "慌"), ("xuyan", "我不會騎馬！", "破音")],
         motion="the horse shifts under him and he grabs the saddle tighter, nearly sliding sideways",
         zh="許硯中近景，坐在阿令背後的馬上，雙手死抓著馬鞍後緣，眼睛睜大往下看地；馬一動，他差點滑下去，把馬鞍抓得更緊"),
    dict(loc="road", cam="Close-up, slow push in", chars=["aling"], tag="鉤子1",
         comp="close-up of A-ling on the horse, her head turned back over her shoulder toward Xu Yan, her cold face with the faintest twitch at the corner of her mouth, loose strands of black hair in the wind",
         lines=[("aling", "抓緊。", "淡淡的，嘴角一動")],
         motion="she turns forward again and snaps the reins once",
         zh="阿令特寫，坐在馬上回頭往後看許硯，冷冷的臉嘴角極輕地動了一下，幾縷黑髮被風吹起；她轉回去，韁繩一甩"),
    dict(loc="road", cam="Wide shot, tracking", chars=["aling", "xuyan"], tag="鉤子1",
         comp="wide shot down the official road, the bay horse carrying A-ling and Xu Yan bursting into a full gallop away from the city gate tower, dust boiling up behind it",
         lines=[("xuyan", "衝——！", "抓著馬鞍大喊")],
         motion="Xu Yan throws one arm in the air for a moment and grabs the saddle again as the horse stretches into its stride, hooves pounding the packed earth",
         zh="官道全景：載著阿令與許硯的棗紅馬從城門樓前衝出去，全速奔跑，身後捲起一大團灰；許硯一手往天上一舉又趕快抓回馬鞍，馬蹄重重踩在黃土路上"),
    dict(loc="road", cam="Medium shot, tracking", chars=["erniu"], tag="鉤子2",
         comp="medium shot of Wang Erniu riding a stocky mule up the road from screen left with four Liuxi youths on mules behind him, a carrying pole across his shoulder, his sun-tanned face grinning",
         lines=[("erniu", "硯哥！", "大嗓門"), ("erniu", "柳溪的兄弟來了！", "憨笑")],
         motion="he waves the carrying pole over his head, and the youths behind him whoop and kick their mules faster",
         zh="王二牛中景，騎著一頭壯騾子從左邊追上來，後面四個柳溪少年也騎著騾子，他肩上扛著扁擔，曬黑的臉咧嘴大笑；他把扁擔舉過頭頂揮，後面的少年吆喝著催騾子"),
    dict(loc="road", cam="Medium close-up, locked", chars=["erniu"],
         comp="medium close-up of Wang Erniu on the mule, sweat and dust on his honest open face, a sheepish grin, his eyes on Xu Yan off screen right",
         lines=[("erniu", "阿令姑娘騎太快，", "喘"), ("erniu", "我們追了一夜！", "抓頭")],
         motion="he scratches the back of his head with a big hand and laughs",
         zh="王二牛中近景，騎在騾上，憨厚的臉上全是汗和灰，傻笑，看著畫外右邊的許硯；大手抓抓後腦勺，哈哈笑"),
    dict(loc="road", cam="Insert of the cart ruts, slow push in", act=1, tag="鉤子2",
         comp="insert of the packed-earth road, two deep fresh cart ruts with crisp edges and a dragged line beside them, turning off the main road toward a track down to the river",
         lines=[("aling", "車轍是新的。", "冷靜")],
         motion="The shot opens directly on this close insert from its very first frame; a horse's hoof steps into frame beside the ruts and a little loose earth crumbles into them",
         zh="插鏡：黃土路上兩道很深、邊緣還很利落的新車轍，旁邊一道拖痕，從大路轉向往河邊的小路；一隻馬蹄踩進畫面，鬆土掉進車轍裡"),
    dict(loc="road", cam="Close-up, locked", chars=["aling"],
         comp="close-up of A-ling on the horse, her phoenix eyes narrowed down the track toward the river, the reins gathered short in her hand",
         lines=[("aling", "往渡口去了。", "很短")],
         motion="she pulls the horse's head toward the river track",
         zh="阿令特寫，坐在馬上，鳳眼瞇起看著往河邊的小路，韁繩收短；她把馬頭拉向河邊那條路"),
    dict(chapter="渡口", loc="ford", cam="Wide shot, slow pan right", chars=["qinshuang"], act=3, tag="鉤子3",
         comp="wide shot of the shallow ford, a prison cart with a heavy wooden cage stopped in the knee-deep water, its mule unhitched, Qin Shuang inside the cage gripping the bars, and a dozen thugs in black runner uniforms with sabers standing in the shallows around it",
         motion="the thugs splash forward to form a ring around the cage while Qin Shuang shakes the bars hard enough to rattle the whole cage",
         zh="渡口淺灘全景：一輛裝著粗木囚籠的囚車停在齊膝的河水裡，騾子已經卸下，秦霜在籠裡抓著木欄，十幾個穿皂衣、帶刀的打手站在淺水裡圍著；打手們踩著水圍成一圈，秦霜用力搖木欄，整個籠子都在晃"),
    dict(loc="ford", cam="Medium shot, locked", chars=["dengyasi"],
         comp="medium shot of Sergeant Deng standing in the shallows on screen right in front of the cage, his black uniform and red sash, an iron chain at his belt, his over-long saber half out of its scabbard, glaring toward Xu Yan off screen left",
         lines=[("dengyasi", "州府辦差，", "粗重陰沉"), ("dengyasi", "閒人滾開！", "吼")],
         motion="he rips the over-long saber the rest of the way out and points it at the bank",
         zh="鄧押司中景在右，站在囚籠前的淺水裡，皂衣紅腰帶、腰掛鐵鏈，過長的刀拔出一半，瞪著畫外左邊的騎馬人；把刀整把拔出來，指向岸邊"),
    dict(loc="ford", cam="Two-shot, locked", chars=["erniu", "xuyan"],
         comp="two-shot on the riverbank, Wang Erniu on his mule on screen left counting the sabers with his lips moving, Xu Yan on the bay horse behind A-ling on screen right, both looking at the ford off screen right",
         lines=[("erniu", "十幾把刀……", "吞口水"), ("erniu", "我們才幾個？", "小聲")],
         motion="he grips his carrying pole in both hands and swallows",
         zh="雙人鏡：河岸上，王二牛在左騎在騾上數刀，嘴唇跟著動，許硯在右坐在阿令背後的馬上，兩人都看著畫外右邊的淺灘；二牛雙手握緊扁擔，吞口水"),
    dict(loc="ford", cam="Medium close-up, slow push in", chars=["xuyan"], tag="鉤子3",
         comp="medium close-up of Xu Yan on the horse, his face steady now, one hand reaching down to the red-tasselled spear strapped along the saddle, his eyes on the cage off screen right",
         lines=[("xuyan", "不用打贏，", "低聲，很穩"), ("xuyan", "把槍送到她手上就好。", "解開綁繩")],
         motion="he yanks the knot loose and draws the spear free of its straps",
         zh="許硯中近景，坐在馬上，臉已經定下來，一手往下摸到綁在馬鞍邊的紅纓長槍，眼睛看著畫外右邊的囚籠；他一扯繩結，把槍從綁帶裡抽出來"),
    dict(loc="ford", cam="Close-up, locked", chars=["qinshuang"],
         comp="close-up of Qin Shuang behind the wooden bars of the cage, her bold straight brows lifting, her almond eyes lighting up, her eyes on Xu Yan off screen left, her hands on the bars",
         lines=[("qinshuang", "許硯！", "眼睛一亮")],
         motion="she presses forward against the bars and her grip tightens with a creak of wood",
         zh="秦霜特寫，在囚籠木欄後面，劍眉一揚，看見畫外左邊的許硯，杏眼一下亮起來，雙手抓著木欄；她往前貼上木欄，手一緊，木頭吱一聲"),
    dict(chapter="接槍", loc="ford", cam="Medium shot, slow push in", chars=["xuyan", "aling"], tag="鉤子4／中段鉤子",
         comp="medium shot of the bay horse plunging into the shallows, A-ling in front with the reins, Xu Yan behind her drawing back his arm with the red-tasselled spear raised high like a javelin",
         lines=[("xuyan", "秦霜——接著！", "大喊")],
         motion="he shifts his weight back, then whips his arm forward and hurls the spear in a high arc, the red tassel streaming",
         zh="中段鉤子：棗紅馬衝進淺水，阿令在前抓韁，許硯在她背後把紅纓長槍高高舉起、手臂往後拉；他重心後移，手臂一甩，把槍高高拋出去，紅纓拖成一條線"),
    dict(loc="ford", cam="Insert of the spear through the bars, locked", act=1, tag="鉤子4",
         comp="insert of the cage bars, a red-tasselled spear shaft flying in between two wooden bars and a young woman's hand in a fitted dark brown sleeve shooting out to catch it",
         motion="The shot opens directly on this close insert from its very first frame; the hand snaps shut on the shaft mid-flight and the tassel whips around the bar",
         zh="插鏡：囚籠的木欄，一桿紅纓槍從兩根木欄中間飛進來，一隻深棕袖子的手猛地伸出抓住；手在半空中一把握住槍桿，紅纓甩著繞過木欄"),
    dict(loc="ford", cam="Close-up, slow push in", chars=["qinshuang"], tag="鉤子4",
         comp="close-up of Qin Shuang inside the cage, the spear shaft in her hand, a fierce bright grin breaking across her face",
         lines=[("qinshuang", "來得正好。", "笑，咬牙")],
         motion="she spins the spear once in her hand so the point swings to the cage door",
         zh="秦霜特寫在籠裡，手握槍桿，臉上綻開一個又兇又亮的笑；她手腕一轉，槍尖轉向籠門"),
    dict(loc="ford", cam="Medium shot, locked", chars=["qinshuang"], act=2,
         comp="medium shot of the cage door, Qin Shuang inside jamming the spear shaft between the bars and the iron-hasped door, her weight thrown onto it",
         motion="she throws her whole weight onto the shaft, the wood groans and the door hasp snaps with a crack, the door swinging open",
         zh="囚籠門的中景，秦霜在裡面把槍桿插進木欄與鐵扣的籠門之間，整個人壓上去；她全身重量壓上槍桿，木頭呻吟一聲，門扣「喀」地斷開，籠門甩開"),
    dict(loc="ford", cam="Wide shot, slow pan right", chars=["qinshuang"], act=3, tag="鉤子5",
         comp="wide shot of the shallows around the broken cage, Qin Shuang leaping out of the open door into the knee-deep river with the spear swinging, the thugs around the cage raising their sabers",
         motion="she lands in a burst of white spray and sweeps the spear in a flat arc, and two sabers fly out of two thugs' hands at once and spin up into the air",
         zh="奇觀：破籠四周淺灘的全景，秦霜從打開的籠門躍出、跳進齊膝的河水，長槍掄起，籠邊的打手舉起刀；她落進水裡炸開一片白浪，一槍平掃，兩個打手手上的刀同時飛上半空"),
    dict(loc="ford", cam="Insert of the sabers falling into the river, locked", act=1,
         comp="insert of the river surface over the pebble shoal, two steel sabers tumbling down out of the sky toward the water",
         motion="The shot opens directly on this close insert from its very first frame; the two sabers plunge into the river one after the other with two sharp splashes and sink out of sight",
         zh="插鏡：淺灘上的河面，兩把鋼刀從天上翻滾著掉下來；兩把刀一前一後插進河裡，兩聲脆響的水花，沉下去不見"),
    dict(loc="ford", cam="Medium shot, tracking", chars=["erniu"], tag="鉤子5",
         comp="medium shot of Wang Erniu charging through the shallows with his carrying pole, two Liuxi youths with staves behind him, a thug in black turning toward him",
         lines=[("erniu", "看棍！", "大吼")],
         motion="he swings the carrying pole round in a big flat arc and sweeps the thug's legs from under him, the man toppling backward into the water",
         zh="王二牛中景，扛著扁擔衝過淺水，後面兩個拿棍子的柳溪少年，一個皂衣打手轉向他；他把扁擔掄一大圈，橫掃打手的腿，那人仰面倒進水裡"),
    dict(loc="ford", cam="Medium shot, slow push in", chars=["qinshuang"], act=3, tag="顏值鏡頭",
         comp="medium shot of Qin Shuang standing knee-deep in the river, her sleek high ponytail flinging an arc of bright water droplets behind her head, the red-tasselled spear angled low toward the thugs, her eyes brighter than the spearhead",
         motion="she snaps her head round and the ponytail whips a glittering arc of droplets through the sunlight, then she settles into stance with the spear perfectly still",
         zh="顏值鏡頭：秦霜站在齊膝的河水裡，高馬尾在腦後甩出一道亮晶晶的水弧，紅纓長槍斜斜指向打手，眼神比槍尖還亮；她一甩頭，馬尾甩出一道陽光下閃亮的水珠，然後穩穩站定，槍尖一動不動"),
    dict(loc="ford", cam="Wide shot, locked", chars=["qinshuang"], act=3,
         comp="wide shot of the ford, Qin Shuang in the middle of the shallows fighting three thugs at once with the spear, Liuxi youths with staves on the left bank side, splashes everywhere",
         motion="she flicks the spear butt into one man's chest and hooks the next man's ankle with the blade end, and both of them topple into the river one after the other",
         zh="渡口全景：秦霜在淺灘中間一槍對三個打手，左邊是拿棍子的柳溪少年，到處是水花；她槍尾一戳一個人的胸口，槍頭一勾下一個人的腳踝，兩人一個接一個倒進河裡（中段爽點：counter_kill）"),
    dict(chapter="追回令", loc="ford", cam="Medium shot, locked", chars=["xuyan"], tag="鉤子6",
         comp="medium shot of Xu Yan standing in the knee-deep water beside the bay horse, holding up a folded sheet of paper with a square red seal mark, his face set",
         lines=[("xuyan", "州府追回令！", "大聲"), ("xuyan", "誰還敢動？", "一字一字")],
         motion="he holds the paper high over his head and takes one step forward through the water",
         zh="許硯中景，站在棗紅馬旁齊膝的水裡，高舉一張蓋著方形紅印的摺紙（追回令），臉繃緊；他把紙舉過頭頂，踩著水往前一步"),
    dict(loc="ford", cam="Wide shot, locked", chars=["dengyasi"], act=2,
         comp="wide shot of the thugs standing in the river, half of them dripping from their falls, all staring at the paper held up off screen left, Sergeant Deng among them with his saber lowered",
         motion="the thugs lower their sabers and glance at one another, and two of them take a step back toward the far bank",
         zh="淺灘全景：河裡的打手，一半剛從水裡爬起來，全都盯著畫外左邊舉起來的那張紙，鄧押司在他們中間，刀放低了；打手們把刀放低、互看一眼，兩個往對岸退一步"),
    dict(loc="ford", cam="Two-shot, slow push in", chars=["dengyasi", "aling"], tag="鉤子6",
         comp="two-shot by the bay horse, Sergeant Deng on screen left seizing the horse's reins in his thick fist, A-ling in the saddle on screen right looking down at him coldly",
         lines=[("dengyasi", "我知道她是誰。", "陰笑，壓低聲音")],
         motion="he yanks the reins so the horse tosses its head, his eyes fixed up on A-ling",
         zh="雙人鏡：棗紅馬旁，鄧押司在左用粗手一把抓住馬韁，阿令在右坐在馬上冷冷往下看他；他扯一下韁繩，馬甩頭，他的眼睛往上盯著阿令"),
    dict(loc="ford", cam="Medium close-up, locked", chars=["xuyan"],
         comp="medium close-up of Xu Yan wading in on screen left, his eyes hard on Sergeant Deng off screen right, the recall order still in his hand",
         lines=[("xuyan", "她是誰，", "打斷，冷"), ("xuyan", "她自己說。", "一字一字")],
         motion="he steps in between Deng and the horse and plants himself there",
         zh="許硯中近景在左踩著水走過來，眼神很硬地盯著畫外右邊的鄧押司，手上還拿著追回令；他一步擠進鄧押司與馬之間，站定"),
    dict(loc="ford", cam="Close-up, slow push in", chars=["aling"],
         comp="close-up of A-ling in the saddle, her cold beautiful face, her phoenix eyes moving from Deng to the back of Xu Yan's head below her",
         lines=[("xitong", "阿令好感，五十九。", "平板電子音，叮一聲")],
         panel=[("阿令 好感 → 59", "affection")],
         motion="her hand on the reins loosens a little and her shoulders ease",
         zh="阿令特寫，坐在馬上，清冷的臉，鳳眼從鄧押司移到下方許硯的後腦勺；握韁的手鬆一點，肩膀放下來（他沒讓別人替她說出身分）"),
    dict(loc="ford", cam="Medium shot, locked", chars=["qinshuang", "dengyasi"],
         comp="medium shot in the shallows, Qin Shuang on screen left flicking the spearhead under Sergeant Deng's wrist on screen right, his hand still on the reins",
         lines=[("qinshuang", "手拿開。", "冷")],
         motion="the spear shaft cracks across his knuckles, he lets go of the reins and stumbles back two splashing steps",
         zh="淺水中景：秦霜在左把槍頭挑到右邊鄧押司的手腕下，他的手還抓著韁繩；槍桿往他指節一敲，他鬆開韁繩，踩著水往後退兩步"),
    dict(chapter="信", loc="ford", cam="Wide shot, slow pan left", chars=["dengyasi"], act=2, tag="結尾",
         comp="wide shot of the ford, Sergeant Deng backing away alone toward the log raft at the water's edge, his men scattered and dripping behind him, Qin Shuang and the others in the shallows on the left",
         motion="he backs off step by step through the water until his heel bumps the raft, then stops",
         zh="結尾：渡口全景，鄧押司一個人往水邊的木筏退，他的人濕淋淋地散在後面，秦霜與其他人在左邊淺水裡；他踩著水一步一步退，腳跟撞到木筏停住"),
    dict(loc="ford", cam="Medium close-up, slow push in", chars=["dengyasi"], tag="結尾",
         comp="medium close-up of Sergeant Deng by the raft on screen right, his bristling black beard, a crooked smile, one hand pulling a folded old letter out of the front of his uniform, his eyes on Qin Shuang off screen left",
         lines=[("dengyasi", "放我走，", "陰沉")],
         motion="he draws the letter out slowly and holds it up beside his face",
         zh="鄧押司中近景在右、木筏邊，絡腮鬍，嘴角一歪，一手從衣襟裡慢慢抽出一封摺舊的信，看著畫外左邊的秦霜；他慢慢抽出信，舉到臉旁"),
    dict(loc="ford", cam="Insert of the old letter, locked", act=1, tag="結尾",
         comp="insert of a thick hairy hand holding up a worn folded letter, its edges soft and yellowed, a dark wax seal on it, the river glinting behind",
         lines=[("dengyasi", "給妳爹的信。", "拖長音")],
         motion="The shot opens directly on this close insert from its very first frame; the hand waves the letter slowly from side to side",
         zh="插鏡：一隻粗毛的手舉著一封摺舊的信，邊角發軟發黃，一塊深色封蠟，後面河面閃著光；手慢慢把信左右晃"),
    dict(loc="ford", cam="Close-up, slow push in", chars=["qinshuang"], tag="結尾",
         comp="close-up of Qin Shuang in the river, her fierce face going pale, her almond eyes locked on Sergeant Deng off screen right, the spear point still raised",
         lines=[("qinshuang", "我爹的……", "聲音一啞"), ("qinshuang", "信？", "不敢相信")],
         motion="her lips part, and the spear point sinks an inch as her grip wavers",
         zh="秦霜特寫在河裡，兇悍的臉一下子發白，杏眼死盯著畫外右邊的信，槍尖還舉著；嘴唇微張，握槍的手一鬆，槍尖往下沉一寸"),
    dict(loc="ford", cam="Extreme close-up, locked", chars=["qinshuang"], tag="結尾",
         comp="extreme close-up of Qin Shuang's eyes and bold brows, torn and shining, Sergeant Deng speaking off screen right",
         lines=[("dengyasi", "要信，", "低笑"), ("dengyasi", "就放我走。", "一字一字")],
         motion="her brows draw together hard and her eyes flick from the letter to Deng and back",
         zh="最後一格：秦霜的眼睛與劍眉大特寫，又掙扎又發亮，鄧押司在畫外右邊說話；眉頭狠狠擰緊，眼睛在信與鄧押司之間來回一瞥"),
]

HEAD = [
    "- 開頭 10 秒：接第 52 集最後一格（杜鐵「出了城，人就沒了」、許硯捏緊喜報）：阿令勒馬一個迴旋、從馬上朝他伸手（0:00），「上來。」一把拉上馬背（0:02），「等等，我不會騎馬！」（0:04），「抓緊。」（0:07），棗紅馬衝出城門「衝——！」（0:09）——直接回答「追得上那輛囚車嗎？」：馬上就追",
    "- 顏值鏡頭：s22 秦霜立在齊膝的河水裡、高馬尾甩出一道水弧、紅纓長槍斜指（細綱的 glamour_shot；只寫馬尾甩出水珠，衣服不寫濕）；s04 阿令回頭「抓緊」、嘴角極輕地一動",
    "- 爽點：前半 rescue（s15–s19 槍拋進籠裡、秦霜接槍撬斷籠門躍出）、中段 counter_kill（s19–s23 一槍掃飛兩把刀、二牛掃倒打手、秦霜一個接一個挑落水裡；s24–s25 追回令一舉，對方猶豫）",
    "- 說話鏡頭：說話的人在畫面上的鏡頭，motion 第一句都是他說這句話、嘴唇下巴隨每個音節動；畫外台詞（s08、s32 插鏡，s34 秦霜的臉上鄧押司的話，系統三次）放在插鏡與臉部特寫上",
    "- H3 寫法：同第 51 集；打鬥一鏡一事（拋槍、接槍、撬門、躍出掃刀、刀落水、掃腿、顏值、對三人各一鏡）；水花寫在 motion，人物的衣服不寫濕（`look.negative` 有 wet clothes）",
    "- 鉤子（站主 10-16 規則）：見 brief.md 的鉤子表；相鄰兩個鉤子最多隔約 12 秒",
    "- 檢查：lint 0 錯誤（只剩 sources 那一條警告）、30 項結構檢查全過、分鏡讀取 0 陷阱、gen-dh 44 個鏡都有 dh-set 場景參照（官道 12、渡口淺灘 32）",
    "- 光：s01–s09 正午官道的白光與塵土；s10–s34 午後渡口的冷光、水面反光",
    "- 軸線：官道往畫面深處是城門樓、馬往遠處跑；渡口岸在左、囚車在右邊的淺水裡，許硯一行從左邊下水，鄧押司在右，最後他退到右邊的木筏",
]
FOOT = [
    "- 場景參考：s01–s09 用 `dh-set-guandao-t1`（含 `official road`，有圖；沿用清水縣官道那張，州城北門靠 prompt 的城門樓）；s10–s34 用 `dh-set-beidu-qiantan-t1`（含 `shallow ford`，**要畫**）。",
    "- 道具：紅纓長槍（第 51 集靠在客棧上房桌邊的那桿，s01 綁在阿令的馬鞍邊，s13 解下、s15 拋進籠裡，之後在秦霜手上）；棗紅馬（阿令連夜從柳溪騎來的那匹）；王二牛的扁擔；囚車與粗木囚籠、鐵扣（s10、s18）；追回令（第 52 集知府簽的，方形紅印，s24）；鄧押司過長的刀與腰上的鐵鏈；舊信與深色封蠟（s30–s32）。",
    "- 連戲：王二牛與四個柳溪少年是跟著阿令連夜從柳溪出來的（s06–s07「阿令姑娘騎太快，我們追了一夜」），他們騎騾子，第一次跟著許硯出村打仗（細綱的 general_payoffs）。押車的是鄧押司與十幾個穿皂衣的打手（魏家雇的，細綱第 52 集 state）；本集不點破誰雇的。鄧押司「我知道她是誰」指的是阿令，許硯打斷「她是誰，她自己說」——阿令聽見了（細綱 general_payoffs），系統跳到 59（細綱第 54 集 state 的阿令 59）；她的身分本集與第一季都不說破（第 60 集才揭）。強制任務「三日內救回秦霜」在第 54 集一開頭收。第 54 集從秦霜「信，我自己去拿」接。",
    "- 秒數：`gen-dh.mjs` 自動決定；打鬥的動作鏡多是兩拍（6 秒）。",
    "- 系統面板不由模型畫：s28 的好感度在剪接時疊上（affection）。",
    "- 新的參照圖還沒畫：鄧押司的定妝照（`refs-dh/dengyasi-portrait-t1.png`）與場景 `set-beidu-qiantan-t1.png`；官道（s01–s09）的鏡現在就能做。打手與柳溪少年只寫在 prompt（thugs、youths）。",
]

BRIEF = """
# 《種田娶妻打天下》第 53 集〈渡口截車〉

## 故事前提

第 52 集收在州府大堂：杜鐵撞進來，「囚車天沒亮就出了北門」「押車的不是州府的人」「出了城，人就沒了」。第 53 集直接上路：北門外的官道上，阿令勒馬原地一個迴旋，從馬上朝許硯伸手：「上來。」一把把他拉上馬背（細綱的 hook）。許硯死抓著馬鞍：「等等，」「我不會騎馬！」阿令回頭，嘴角極輕地一動：「抓緊。」棗紅馬衝出城門，許硯一手往天上一舉：「衝——！」王二牛騎著騾子、帶著四個柳溪少年追上來：「硯哥！」「柳溪的兄弟來了！」「阿令姑娘騎太快，」「我們追了一夜！」阿令看路上的新車轍：「車轍是新的。」「往渡口去了。」

北邊渡口的淺灘上，囚車停在齊膝的河水裡，秦霜在粗木籠裡搖著木欄，十幾個穿皂衣、帶刀的打手圍成一圈。押解頭目鄧押司把過長的刀整把拔出：「州府辦差，」「閒人滾開！」王二牛吞口水：「十幾把刀……」「我們才幾個？」（細綱的衝突。）許硯解下綁在馬鞍邊的紅纓長槍：「不用打贏，」「把槍送到她手上就好。」秦霜看見他：「許硯！」棗紅馬衝進淺水，許硯把槍高高拋出去：「秦霜——接著！」（細綱的 mid_hook，0:55 左右）秦霜在籠裡一把接住：「來得正好。」她用槍桿撬斷籠門，躍進河裡炸開一片白浪，一槍平掃，兩把刀同時飛上半空落進河裡（細綱的奇觀）。王二牛掄扁擔掃倒一個：「看棍！」秦霜立在齊膝的河水裡，高馬尾甩出一道水弧（細綱的顏值鏡頭），一槍對三個，一個接一個挑落水裡。

許硯站在水裡高舉追回令：「州府追回令！」「誰還敢動？」打手們把刀放低、互看一眼。鄧押司一把抓住阿令的馬韁：「我知道她是誰。」許硯一步擠進他和馬之間：「她是誰，」「她自己說。」（細綱的 turn。）馬上的阿令握韁的手鬆了一點，系統：阿令好感五十九。秦霜一槍敲在鄧押司的指節上：「手拿開。」鄧押司一路退到水邊的木筏，從衣襟裡慢慢抽出一封摺舊的信：「放我走，」「給妳爹的信。」秦霜的臉一下子白了：「我爹的……」「信？」鄧押司在畫外低笑：「要信，」「就放我走。」秦霜的眉頭狠狠擰緊（細綱的 cliffhanger，choice，「秦霜要放走仇人，換爹的信嗎？」）。

本集細綱：`season-01.json` 第 53 集（120 秒，第一季第六章第三集，調性沙場＋權謀，lead_arc wins）。satisfaction 兩個都入鏡：rescue（s15–s19）、counter_kill（s19–s23）。general_payoffs 全部入鏡：秦霜被救出（s17–s19）；王二牛和柳溪少年們第一次跟著許硯出村打仗（s06–s07、s12、s21）；阿令聽見許硯拒絕從別人嘴裡聽她的身分（s26–s28）。

## 鉤子（站主 10-16：開場、結尾之外中段還要兩三個以上）

| 鉤子 | 鏡 | 內容 |
| --- | --- | --- |
| 【鉤子1】開場 | s01–s05 | 阿令迴旋拉他上馬「抓緊」，「我不會騎馬！」「衝——！」 |
| 【鉤子2】 | s06–s09 | 王二牛帶柳溪少年追上來；新車轍「往渡口去了」 |
| 【鉤子3】 | s10–s14 | 囚車停在淺灘、十幾把刀；「不用打贏，把槍送到她手上就好」 |
| 【鉤子4】中段鉤子 | s15–s17 | 槍拋進籠裡、秦霜接住「來得正好」 |
| 【鉤子5】 | s19–s23 | 撬斷籠門躍出、兩把刀飛上天；二牛「看棍！」；秦霜一槍對三個 |
| 【鉤子6】 | s24–s28 | 追回令「誰還敢動？」；鄧押司「我知道她是誰」，許硯「她是誰，她自己說」 |
| 【結尾】 | s30–s34 | 「放我走，給妳爹的信」「要信，就放我走」 |

## 角色

- 許硯（xuyan）：s01–s05 被阿令拉上馬「我不會騎馬！」「衝——！」；s13「不用打贏，把槍送到她手上就好」；s15 拋槍；s24「州府追回令！誰還敢動？」；s27「她是誰，她自己說」。
- 阿令（aling）：s01–s04 迴旋、拉他上馬「上來」「抓緊」；s08–s09 看車轍「往渡口去了」；s15 騎馬衝進淺水；s26 被鄧押司抓住馬韁；s28 聽見許硯的話，好感 59。
- 王二牛（erniu）：s06–s07 帶柳溪少年追上來；s12「十幾把刀……我們才幾個？」；s21「看棍！」掃倒打手。外貌照 cast.json（扁擔就是外貌裡的 carrying pole）。
- 秦霜（qinshuang）：s10 在籠裡搖木欄；s14「許硯！」；s16–s19 接槍、撬門、躍出；s22 顏值鏡頭；s23 一槍對三個；s29「手拿開」；s33–s34「我爹的……信？」。
- 鄧押司（dengyasi）：s11「州府辦差，閒人滾開！」；s26「我知道她是誰」；s30–s34 退到木筏、掏出信「放我走，給妳爹的信」「要信，就放我走」。外貌照 cast.json（過長的刀、鐵鏈）。
- 系統（xitong）：s28 阿令好感 59（`overlays.json`）。
- 群眾：十幾個穿皂衣帶刀的打手（thugs）、四個柳溪少年（youths），只寫在 prompt。

## 地點（固定的地點字）

- 州城北門官道（正午）：`On the official road outside the north gate of Qingzhou at midday`（`dh-set-guandao-t1`）。
- 北邊渡口淺灘（午後）：`At the shallow ford of the north ferry outside Qingzhou in the afternoon`（`dh-set-beidu-qiantan-t1`）：齊膝的河水流過卵石灘、繫在木樁上的粗木筏、蘆葦與沙洲、一條泥車道伸進水裡、對岸起霧。

## 站主觀點

站主 2026-10-16 的要求：女生要火辣漂亮，濃顏系的五官與妝、合身剪裁；不露、不濕身、鏡頭不停在身體部位；每集至少一個顏值鏡頭；結尾收在最高點；不被黃標；每集開場、結尾之外中段再兩三個以上鉤子。打鬥照不黃標：沒有血、沒有人被刺中——刀被挑飛落進河裡、人被掃倒跌進水裡、槍尾戳胸口、槍桿敲指節。秦霜的顏值鏡頭只寫馬尾甩出的水珠與眼神，衣服不寫濕、鏡頭不停在身上。追回令與信都不寫字（方形紅印、深色封蠟）。系統面板不由模型畫。

分鏡照 `storyboard-rules.md` 2026-10-28 起的 H3 寫法（同第 51 集）；秒數由 `gen-dh.mjs` 決定；本集沒有靜圖、沒有切素材鏡。角色外觀照 `production/cast.json` 逐字照抄。
"""

_add = {
 4: [dict(loc="road", cam="Medium close-up, tracking", chars=["xuyan"],
          comp="medium close-up of Xu Yan bouncing on the galloping horse behind A-ling, both hands clamped on the saddle, his hair band flapping, his face half terrified and half laughing",
          lines=[("xuyan", "阿令，", "顛得說不清楚"), ("xuyan", "妳在哪學的騎馬？", "喊")],
          motion="he is jolted up off the saddle by a stride and lands back hard, clutching tighter",
          zh="許硯中近景，在狂奔的馬上坐在阿令背後一路顛，雙手死扣馬鞍，束髮帶亂飛，臉一半嚇壞一半在笑；馬一顛把他拋起來，他重重落回去，抓得更緊"),
     dict(loc="road", cam="Close-up, tracking", chars=["aling"],
          comp="close-up of A-ling leaning forward over the horse's neck at full gallop, her black hair streaming, her cold eyes fixed on the road ahead",
          lines=[("aling", "別說話，", "冷"), ("aling", "會咬到舌頭。", "頭也不回")],
          motion="she flicks the reins and leans lower as the horse lengthens its stride",
          zh="阿令特寫，全速奔馳中俯身貼著馬頸，黑髮往後飛，冷冷的眼睛盯著前方的路；她一抖韁繩，身子壓得更低，馬步子拉得更長（她不回答在哪學的）"),
     dict(loc="road", cam="Close-up, locked", chars=["xuyan"],
          comp="close-up of Xu Yan's face behind A-ling's shoulder on the galloping horse, dust in the air, his eyes lifting to a fixed point in the empty air in front of him",
          lines=[("xitong", "強制任務：救回秦霜。", "平板電子音，叮一聲"), ("xitong", "剩餘時間：兩天。", "平板電子音")],
          panel=[("強制任務：救回秦霜｜剩餘：兩天", "task")],
          motion="his eyes track across the empty air as if reading, and his jaw sets as he grips the saddle tighter",
          zh="系統面板：許硯的臉在阿令肩後，狂奔的馬上塵土飛揚，眼睛抬起定在面前的空中；眼睛像在讀字一樣掃過去，下顎繃緊，把馬鞍抓得更緊")],
 9: [dict(loc="ford", cam="Medium close-up, slow push in", chars=["dengyasi"],
          comp="medium close-up of Sergeant Deng in the shallows on screen right beside the cage, his bristling black beard, his gloomy hooded eyes on the far misty bank, one hand on the iron chain at his belt",
          lines=[("dengyasi", "天黑前過河。", "陰沉"), ("dengyasi", "到了對岸，就沒有這個人。", "低")],
          motion="he slaps the cage bars once with the flat of his hand and turns away toward the raft",
          zh="鄧押司中近景在右、囚籠旁的淺水裡，絡腮鬍，陰沉的眼睛看著對岸的霧，一手按著腰上的鐵鏈；他用手掌拍一下籠欄，轉身朝木筏走"),
     dict(loc="ford", cam="Close-up, locked", chars=["qinshuang"],
          comp="close-up of Qin Shuang behind the wooden bars of the cage, her bold brows drawn hard, her almond eyes blazing at Sergeant Deng off screen right",
          lines=[("qinshuang", "你們不是州府的人。", "咬牙，冷")],
          motion="she grips two bars and shoves her face close to the gap between them",
          zh="秦霜特寫，在囚籠木欄後，劍眉擰緊，杏眼冒火瞪著畫外右邊的鄧押司；雙手抓住兩根木欄，臉貼近欄縫")],
 16: [dict(loc="ford", cam="Close-up, slow push in", chars=["xuyan"],
          comp="close-up of Xu Yan on the horse in the shallows, his arm still extended from the throw, his face breaking into a fierce grin, his eyes on the cage off screen right",
          lines=[("xuyan", "接到了！", "大笑")],
          motion="he pumps his fist once and grabs the saddle again before he slips",
          zh="許硯特寫，在淺水裡的馬上，手臂還伸著沒收回來，臉上綻開一個狠狠的笑，看著畫外右邊的囚籠；握拳一揮，又趕快抓回馬鞍免得滑下去")],
 20: [dict(loc="ford", cam="Medium close-up, locked", chars=["erniu"],
          comp="medium close-up of Wang Erniu standing in the shallows with his carrying pole, water splashing at his knees, his honest face stunned and then delighted, looking down at the thug floundering in the river",
          lines=[("erniu", "硯哥，", "不敢相信"), ("erniu", "我打中了！", "憨笑大喊")],
          motion="he lifts the carrying pole over his head with both hands and shakes it",
          zh="王二牛中近景，站在淺水裡拿著扁擔，水花濺到膝蓋，憨厚的臉先愣住再樂開，低頭看著河裡掙扎的打手；雙手把扁擔舉過頭頂搖"),],
 22: [dict(loc="ford", cam="Close-up, slow push in", chars=["qinshuang"],
          comp="close-up of Qin Shuang in the river with the spear across her body, her bold brows level, her eyes cold and bright on Sergeant Deng off screen right",
          lines=[("qinshuang", "現在，", "冷笑"), ("qinshuang", "換我押你。", "一字一字")],
          motion="she levels the spear point toward him and takes one slow step through the water",
          zh="秦霜特寫在河裡，長槍橫在身前，劍眉放平，眼神又冷又亮地盯著畫外右邊的鄧押司；她把槍尖對準他，踩著水慢慢往前一步"),
     dict(loc="ford", cam="Close-up, locked", chars=["xuyan"],
          comp="close-up of Xu Yan beside the bay horse in the knee-deep water, river light on his face, his eyes lifting to a fixed point in the empty air in front of him",
          lines=[("xitong", "強制任務完成。", "平板電子音，叮一聲")],
          panel=[("強制任務完成：救回秦霜", "task")],
          motion="his eyes track across the empty air, and he lets out a long breath as his shoulders drop",
          zh="系統面板：許硯特寫，站在棗紅馬旁齊膝的水裡，河面的光映在臉上，眼睛抬起定在面前的空中；眼睛掃過去，長長吐一口氣，肩膀放下來")],
 32: [dict(loc="ford", cam="Medium close-up, slow push in", chars=["xuyan"],
          comp="medium close-up of Xu Yan in the shallows on screen left, his face grave and gentle, his eyes on Qin Shuang off screen right",
          lines=[("xuyan", "秦霜，", "很輕"), ("xuyan", "妳決定。", "很穩")],
          motion="he lowers the recall order to his side and steps back half a pace, leaving the choice to her",
          zh="許硯中近景在左、淺水裡，臉色凝重又溫和，看著畫外右邊的秦霜；把追回令放下到身側，往後退半步，把決定留給她")],
}
_new = []
for _i, _x in enumerate(SHOTS):
    _new.append(_x)
    _new += _add.get(_i, [])
SHOTS = _new

SHOTS[8] = dict(SHOTS[8], chapter="柳溪的兄弟")
_m = {1:1,2:2,3:3,4:4,5:5,6:9,7:10,8:11,9:12,10:13,11:16,12:17,13:18,14:19,15:20,16:21,17:22,18:24,19:25,20:26,21:27,22:29,23:30,24:33,25:34,26:35,27:36,28:37,29:38,30:39,31:40,32:41,33:42,34:44}
import re as _re
_f = lambda t: _re.sub(r"s(\d\d)(?!\d)", lambda m: "s%02d" % _m[int(m.group(1))] if int(m.group(1)) in _m else m.group(0), t)
HEAD = [_f(x) for x in HEAD]
FOOT = [_f(x) for x in FOOT]
BRIEF = _f(BRIEF)
HEAD[0] = HEAD[0] + "；之後馬上顛著問「阿令，妳在哪學的騎馬？」她只回「別說話，會咬到舌頭」（0:09–0:16，不回答），系統倒數「剩餘時間：兩天」（0:16）"
BRIEF = BRIEF.replace("棗紅馬衝出城門，許硯一手往天上一舉：「衝——！」", "棗紅馬衝出城門，許硯一手往天上一舉：「衝——！」他在馬上一路顛：「阿令，」「妳在哪學的騎馬？」阿令頭也不回：「別說話，」「會咬到舌頭。」（她不回答。）系統：「強制任務：救回秦霜。」「剩餘時間：兩天。」")
BRIEF = BRIEF.replace("秦霜在粗木籠裡搖著木欄，十幾個穿皂衣、帶刀的打手圍成一圈。", "秦霜在粗木籠裡搖著木欄，十幾個穿皂衣、帶刀的打手圍成一圈。鄧押司拍一下籠欄：「天黑前過河。」「到了對岸，就沒有這個人。」秦霜瞪著他：「你們不是州府的人。」")
BRIEF = BRIEF.replace("秦霜在籠裡一把接住：「來得正好。」", "秦霜在籠裡一把接住：「來得正好。」許硯握拳：「接到了！」")
BRIEF = BRIEF.replace("王二牛掄扁擔掃倒一個：「看棍！」", "王二牛掄扁擔掃倒一個：「看棍！」「硯哥，」「我打中了！」")
BRIEF = BRIEF.replace("一槍對三個，一個接一個挑落水裡。", "一槍對三個，一個接一個挑落水裡，槍尖對準鄧押司：「現在，」「換我押你。」系統：「強制任務完成。」")
BRIEF = BRIEF.replace("秦霜的臉一下子白了：「我爹的……」「信？」", "秦霜的臉一下子白了：「我爹的……」「信？」許硯放下追回令、退半步：「秦霜，」「妳決定。」")
BRIEF = BRIEF.replace("| 【鉤子1】開場 | s01–s05 | 阿令迴旋拉他上馬「抓緊」，「我不會騎馬！」「衝——！」 |", "| 【鉤子1】開場 | s01–s08 | 阿令迴旋拉他上馬「抓緊」，「我不會騎馬！」「衝——！」「妳在哪學的騎馬？」；系統倒數剩兩天 |")
BRIEF = BRIEF.replace("| 【鉤子3】 | s13–s18 |", "| 【鉤子3】 | s13–s18 |")
FOOT = [x.replace("強制任務「三日內救回秦霜」在第 54 集一開頭收。", "強制任務「三日內救回秦霜」在 s08 倒數、s32 完成（秦霜好感沒有清零）。") for x in FOOT]
FOOT = [x.replace("s28 的好感度在剪接時疊上（affection）。", "s08、s32 的強制任務與 s37 的好感度在剪接時疊上（task、affection）。") for x in FOOT]
BRIEF = BRIEF.replace("- 系統（xitong）：s37 阿令好感 59（`overlays.json`）。", "- 系統（xitong）：s08 強制任務倒數剩兩天、s32 強制任務完成、s37 阿令好感 59（`overlays.json`）。")
HEAD = [x.replace("（s08、s41 插鏡，s44 秦霜的臉上鄧押司的話，s37 系統）", "（s11、s41 插鏡，s44 秦霜的臉上鄧押司的話，s08、s32、s37 系統）") for x in HEAD]
