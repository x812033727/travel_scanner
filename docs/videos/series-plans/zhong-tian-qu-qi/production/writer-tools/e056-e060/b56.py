import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from ztlib import *

chars = [ch("xuyan"), ch("aling"), ch("qinshuang"), ch("tangxiaotang"), ch("erniu"), ch("lengtie"),
         minor("shaonian", "瞭望少年", "East Asian boy of fifteen, skinny and sun-browned, a patched brown short jacket and a cloth headband, a bamboo whistle on a cord round his neck", "Puck", "十五歲的村裡瞭望少年，男聲、變聲期有點破音、喊起來又急又尖"),
         ch("xitong")]
e = Ep(56, chars)
S = e.shot
YARD = "In the farmhouse yard at night under a cold half moon, the small dirt yard of a poor thatched farmhouse in an ancient Chinese village, the low mud wall, the woodpile and the persimmon tree black against the sky, a low table under the eaves with one oil lamp and a clay basin, deep blue shadows and warm lamplight on the faces"
THR = "At the village threshing ground at dawn, a wide round patch of hard beaten earth, haystacks and a stone roller at its edge, thatched roofs behind, pale gold sunrise light low across the ground with dust hanging in it"
TOWER = "On the new log lookout tower at the edge of Liuxi village in clear afternoon light, a high platform of lashed logs with a rough rail and a bamboo ladder, a bronze gong hanging from a crossbeam, thatched roofs below, a dusty road winding away across brown fields toward the hills"
FOOT = "At the foot of the new log lookout tower at the edge of Liuxi village in clear afternoon light, the tall frame of lashed logs and its bamboo ladder rising behind, thatched roofs and a dusty road beyond, brown fields"
GATE = "At the village entrance at dusk under a deep orange sky, an old willow tree, a wooden plank bridge over the thin stream, a dusty track, the village's rough timber gate with a heavy wooden crossbar and a low log lookout platform above it, thatched roofs beyond, the first torches lit"
QIN = "Qin Shuang in a fitted black cotton jacket crossed at the collar and cinched with a wide leather belt, her high ponytail tied with a red cord"
DUSK = "the orange dusk light stays unchanged"

# ── 畫像 ──
S("s01", "Insert of the letter in the lamp flame, locked", YARD,
  "insert of the oil lamp on the low table, a slender hand in a grey-white sleeve holding the corner of an opened letter of plain paper covered in faint brush strokes down into the small flame, the paper catching and curling orange",
  f"the flame climbs the paper and the edge blackens and curls while the hand holds perfectly still; {NIGHT}",
  [], chapter="畫像", action=2,
  zh="【鉤子1／開頭】接第 55 集：矮桌上的油燈，一隻灰白袖子的手把拆開的信（一列列淡淡的毛筆畫，不寫字）一角湊進火苗，紙一下子著了，捲起橘色的邊；火往上爬，手一動不動（無台詞）")
S("s02", "Close-up, slow push in", YARD,
  "close-up of A-ling's face on screen right, moon-white skin lit orange from below by the burning letter in her hand, her phoenix eyes fixed on the flame, her lips pressed thin",
  f"her eyes lift from the flame to Xu Yan off screen left and her jaw sets; {NIGHT}",
  ["aling"], [("aling", "畫的是我。", "很輕，很平")],
  zh="【鉤子1】阿令特寫在右，手上燒著的信從下面把月白的臉照成橘色，鳳眼盯著火、唇抿成一線；眼睛從火上抬起來，看畫外左邊的許硯，下顎一緊")
S("s03", "Medium shot, locked", YARD,
  f"medium shot of {TANG} on screen left by the low table, the torn envelope still in her hand, her big round eyes wide, turning toward Aling off screen right",
  f"she takes one half step toward A-ling and the envelope crumples in her fist; {NIGHT}",
  ["tangxiaotang"], [("tangxiaotang", "魏少卿畫妳？", "愣住"), ("tangxiaotang", "他到底認得妳什麼？", "急")],
  zh="高領桃粉襦裙的唐小棠在左、矮桌邊，手上還捏著撕開的信封，大圓眼睛睜大，轉向畫外右邊的阿令；往前半步，信封在拳頭裡捏皺")
S("s04", "Insert of the clay basin, locked", YARD,
  "insert of a clay basin on the low table in the lamplight, the last burning scrap of the letter dropping into it and crumbling into grey ash, a wisp of smoke rising; Aling speaks off screen",
  f"the scrap falls, flares once and collapses into ash as the smoke curls up; {NIGHT}",
  [], [("aling", "送我走。", "畫外，平靜"), ("aling", "今晚就走。", "畫外")],
  zh="插鏡：油燈下的陶盆，信的最後一角掉進去，亮一下、塌成灰，一縷煙升起；阿令畫外說話")
S("s05", "Close-up, locked", YARD,
  "close-up of Xu Yan's face on screen left in the warm lamplight, his brows drawn down and his mouth set hard, his eyes on Aling off screen right",
  f"he shakes his head once, slowly, without looking away; {NIGHT}",
  ["xuyan"], [("xuyan", "不送。", "想都沒想")],
  zh="許硯特寫在左、暖燈下，眉頭壓低、嘴抿緊，看著畫外右邊的阿令；慢慢搖一下頭，眼睛不移開")
S("s06", "Medium close-up, locked", YARD,
  "medium close-up of A-ling on screen right by the persimmon tree, tall and slender in her grey-white dress, her hands folded hard at her sash, her cold phoenix eyes on Xu Yan off screen left",
  f"she draws a breath and her chin lifts a little; {NIGHT}",
  ["aling"], [("aling", "他們要的是我，", "冷"), ("aling", "不是許家。", "一字一字")],
  zh="阿令中近景在右、柿子樹旁，灰白衣裙，雙手緊緊交疊在腰帶上，冷冷的鳳眼看畫外左邊的許硯；吸一口氣，下巴抬一點")
S("s07", "Two-shot, slow push in", YARD,
  "two-shot across the dirt yard: Xu Yan on screen left rising from the bench by the low table and stepping toward A-ling on screen right under the persimmon tree, the oil lamp between them",
  f"he walks two weighted steps and stops an arm's length from her; {NIGHT}",
  ["xuyan", "aling"], [("xuyan", "畫的是妳，", "走過去"), ("xuyan", "那就是我家的事。", "很穩")],
  zh="院子雙人鏡：許硯在左從矮桌邊的長凳站起，走向右邊柿子樹下的阿令，油燈在兩人中間；沉沉走兩步，停在一臂遠，衣襬落定")
S("s08", "Close-up, slow push in", YARD,
  "close-up of A-ling's face on screen right under the dark persimmon branches, her phoenix eyes wavering for the first time, her lips parting, looking at Xu Yan off screen left",
  f"she turns on her heel and walks away into the dark doorway of the house, her sleeve trailing; {NIGHT}",
  ["aling"], action=2,
  zh="阿令特寫在右、柿子樹黑影下，鳳眼第一次晃了一下，嘴唇微張，看著畫外左邊的許硯；眼睛一垂，轉身走進黑暗的屋門，袖子拖過（無台詞）")
S("s09", "Medium shot, locked", YARD,
  "medium shot of Qin Shuang tying up her hair by the woodpile on screen left, a red cord held in her teeth, her bright almond eyes hard and steady",
  f"she pulls the red cord tight round her ponytail in one sharp tug; {NIGHT}",
  ["qinshuang"], [("qinshuang", "我不藏了。", "咬著繩子，鬆開"), ("qinshuang", "天亮，打穀場。", "利落")], chapter="分工",
  zh="秦霜在左、柴堆旁，正在綁頭髮，嘴裡咬著一條紅繩，杏眼又硬又定；猛一拉用紅繩把高馬尾綁緊，放下手")
S("s10", "Medium close-up, locked", YARD,
  f"medium close-up of {TANG} on screen right by the low table, the small gold abacus lifted in one hand, her chin up with a sharp businesslike look",
  f"she flicks the beads across in one sweep and snaps it to her palm; {NIGHT}",
  ["tangxiaotang"], [("tangxiaotang", "許記鏢局的車，", "一秒變精明"), ("tangxiaotang", "我排一條傳信線。", "篤定")],
  zh="唐小棠中近景在右、矮桌邊，一手舉著小金算盤，下巴抬起、一臉精明；算盤珠子一撥到底，往掌心一拍")
S("s11", "Medium shot, slow push in", YARD,
  "medium shot of Wang Erniu leaning over the low mud wall of the yard on screen right, a carrying pole on his shoulder, his honest square face eager, looking at Xu Yan off screen left",
  f"he slaps the top of the mud wall with his big hand and pushes himself upright; {NIGHT}",
  ["erniu"], [("erniu", "我帶人搭瞭望台！", "大嗓門")],
  zh="王二牛在右、趴在院子矮土牆上，肩上扛著扁擔，方臉一臉熱切，看畫外左邊的許硯；大手往牆頭一拍，撐起身子")

# ── 方陣 ──
S("s12", "Wide shot, slow push in", THR,
  f"wide shot of the threshing ground at sunrise: sixty village youths in rough brown and grey short jackets standing in a square block of straight rows, each holding a long wooden staff upright, {QIN} standing alone in front of them on screen centre holding a red-tasselled spear, the low sun behind her throwing her long shadow toward the frame",
  "she plants the butt of the spear in the earth and the whole block of youths straightens at once",
  ["qinshuang"], chapter="方陣", action=3,
  zh="【鉤子2】顏值鏡頭：日出的打穀場全景，六十個穿粗布短褂的村裡少年排成方方正正的方陣，每人直握一根長棍；換上合身黑色勁裝、寬皮帶、高馬尾綁紅繩的秦霜獨自站在陣前中間，手握紅纓槍，低低的太陽在她背後，影子長長拉向鏡頭；她把槍尾往地上一頓，整個方陣同時挺直（無台詞）")
S("s13", "Medium close-up, low angle, locked", THR,
  f"medium close-up from a low angle of {QIN} on screen centre, the red-tasselled spear upright beside her, the sunrise rim-lighting her face and ponytail, her eyes on the youths off screen",
  "she draws a breath and snaps her head round toward the ranks",
  ["qinshuang"], [("qinshuang", "棍——", "拉長，號令"), ("qinshuang", "頓地！", "一聲斷喝")],
  zh="秦霜中近景、低角度在中間，紅纓槍立在身旁，日出的光勾出她的臉和馬尾，看著畫外的少年們；吸一口氣，頭猛地轉向隊伍")
S("s14", "Wide shot, locked", THR,
  "wide shot of the square block of sixty youths on the threshing ground, every long staff slamming down onto the hard earth at the same instant, a sheet of pale dust bursting up along every row in the low gold light",
  "sixty staffs hit the ground together and the dust rolls up in one wave and hangs glowing in the sun",
  [], action=3,
  zh="奇觀：打穀場上六十人的方陣，每一根長棍在同一瞬間砸在硬土上，一排排塵土同時揚起，浮在金色的低光裡（無台詞）")
S("s15", "Two-shot, locked", THR,
  f"two-shot at the edge of the threshing ground: Xu Yan on screen left with his mouth open in surprise, {TANG} on screen right beside him, the drilling ranks blurred in the dust behind them on screen right",
  "Xu Yan turns to her with his eyebrows high and points toward the ranks",
  ["xuyan", "tangxiaotang"], [("xuyan", "這些人……", "看傻了"), ("xuyan", "什麼時候練成陣的？", "不敢相信")],
  zh="打穀場邊雙人鏡：許硯在左、嘴張著，高領桃粉襦裙的唐小棠在右，右邊背景是塵土裡操練的隊伍；許硯許硯轉頭看她、眉毛挑高，往隊伍一指")
S("s16", "Medium close-up, slow push in", THR,
  f"medium close-up of {QIN} on screen right walking along the front row, the spear on her shoulder, dust settling around her boots, her eyes on Xu Yan off screen left with a small proud lift of her chin",
  "she stops, swings the spear down from her shoulder and plants it beside her",
  ["qinshuang"], [("qinshuang", "秦家的陣，", "淡淡的驕傲"), ("qinshuang", "頭一回拿出來。", "嘴角一勾")],
  zh="中段爽點：秦霜中近景在右，扛著槍沿第一排走，塵土落在靴邊，看畫外左邊的許硯、下巴微微一抬；停下，槍從肩上一甩、往身旁一插")
S("s17", "Close-up, locked", THR,
  "close-up of Xu Yan's face on screen centre in the sunrise, his eyes lifting and fixing on a point in the empty air in front of him, a slow grin starting; the system voice speaks off screen",
  "his eyes track across the empty air as if reading and the grin widens",
  ["xuyan"], [("xitong", "許家護村隊，", "平板電子音，叮一聲"), ("xitong", "六十人。", "平板電子音")],
  zh="系統面板：許硯的臉在中間、日出的光裡，眼睛抬起定在面前的空中，慢慢笑開；眼睛像讀字一樣掃過空中，笑得更開",
  panel=[{"text": "許家護村隊：六十人｜隊列：方陣", "kind": "panel"}])
S("s18", "Medium shot, slow pan right", THR,
  f"medium shot at the far edge of the threshing ground: {TANG} on screen left handing a folded note up to the first of two escort riders in dark blue jackets sitting on brown horses on screen right",
  "the rider tucks the note into his jacket, wheels his horse and kicks it into a canter toward screen right",
  ["tangxiaotang"], [("tangxiaotang", "二十里一站，", "交代"), ("tangxiaotang", "消息半天就到。", "拍拍馬脖子")],
  zh="打穀場遠端：唐小棠在左，把一張摺好的紙條遞給右邊騎棕馬、深藍短褂的壯碩鏢師，後面還等著一騎；鏢師把紙條塞進懷裡，掉轉馬頭從右邊跑出畫面")

# ── 瞭望台 ──
S("s19", "Wide shot, tilt up", FOOT,
  "wide shot at the foot of the tower: Wang Erniu and four village lads on screen left hauling on two ropes, a last heavy log swinging upright into the top of the tall frame of lashed logs, a skinny boy waiting on the platform above",
  "the lads heave together, the log thuds into its notch at the top and the boy above whoops and ties it off",
  ["erniu"], [("erniu", "一、二——", "吆喝"), ("erniu", "起！", "使盡全力")], chapter="瞭望台",
  zh="瞭望台腳下全景：王二牛和四個村裡小伙子在左拉兩條繩，最後一根粗木頭甩直、卡進高高的木架頂端，一個瘦小的少年在上面平台等著；大家一起使力，木頭「咚」地卡進榫口，上面的少年歡呼一聲把它綁牢")
S("s20", "Medium close-up, locked", TOWER,
  "medium close-up of the lookout boy on the platform on screen centre, skinny and sun-browned with a cloth headband, one hand shading his eyes as he stares far down the road",
  "his hand drops, his eyes go wide and he grabs the bamboo whistle hanging at his neck",
  ["shaonian"], [("shaonian", "那是……", "瞇眼，愣住")],
  zh="【鉤子3】瞭望少年中近景在中間、平台上，瘦、曬黑、綁頭巾，一手遮眼望著畫外右邊的路；手一放，眼睛瞪大，一把抓起胸前的竹哨")
S("s21", "Close-up, locked", TOWER,
  "close-up of the lookout boy on screen right, the bamboo whistle between his lips, his cheeks puffed out, the bronze gong blurred behind him",
  "he blows the whistle hard twice, his cheeks puffing and his shoulders jerking with each blast",
  [], action=2,
  zh="【鉤子3／中段鉤子】少年特寫在右，竹哨含在嘴裡、兩頰鼓起，後面糊開的銅鑼；用力吹兩聲，臉頰一鼓、肩膀跟著一抽（無台詞，竹哨聲）")
S("s22", "Wide shot, slow push in", TOWER,
  "wide shot over the rail of the platform looking down the dusty road, the lookout boy speaks off screen: far off where it leaves the hills, a long column of horsemen in deep purple and crimson palace livery riding toward the village, a pale cloud of dust rising behind them",
  "the column winds slowly along the road and the dust cloud swells behind it",
  [], [("shaonian", "好多馬……", "畫外，倒吸一口氣")],
  zh="從平台欄杆往下看那條土路的全景：遠遠在路出山的地方，一長列穿深紫與絳紅宮服的騎馬人往村子來，後面揚起一團淡淡的塵土；隊伍沿路慢慢彎過來，塵土越滾越大（少年畫外）")
S("s23", "Medium shot, locked", TOWER,
  "medium shot of the lookout boy leaning over the rail on screen right, one arm flung out pointing down the road, his eyes on Xu Yan off screen left",
  "he leans further over the rail, pointing hard, his headband tails flapping",
  ["shaonian"], [("shaonian", "縣城來了一隊人，", "破音，急"), ("shaonian", "穿宮裡的衣服！", "尖叫")],
  zh="少年在右、整個人探出欄杆，一隻手臂往路上一指，朝畫外左邊下面的人喊；身子再探出去，用力指，頭巾的尾巴甩動")
S("s24", "Medium shot, slow push in", FOOT,
  f"medium shot at the foot of the tower: an escort rider in a dark blue jacket reining in a lathered horse on screen right while two village lads grab its bridle, the rider leaning down to hand a folded note to {TANG} on screen left",
  "she snatches the note, flicks it open and reads, her eyes racing down the page",
  ["tangxiaotang"], [("tangxiaotang", "他們在縣城打聽，", "唸，越唸越慢"), ("tangxiaotang", "不說話的女人。", "抬頭")],
  zh="瞭望台腳下：右邊一個深藍短褂的鏢師勒住滿身汗的馬，俯身把摺好的紙條遞給左邊的唐小棠（傳信線第一次用上）；她一把抓過、一彈打開，眼睛飛快往下讀")
S("s25", "Close-up, locked", FOOT,
  "close-up of A-ling's face on screen right at the foot of the tower, her cold phoenix eyes turning slowly toward the road off screen right, her lips pressed thin",
  "her fingers close on her sleeve over the hidden blade and her breath stops",
  ["aling"], action=2,
  zh="阿令特寫在右、瞭望台下，冷冷的鳳眼慢慢轉向畫外右邊的路，唇抿緊；手指隔著袖子扣住藏著的刀，呼吸一停（無台詞）")
S("s26", "Medium close-up, locked", FOOT,
  "medium close-up of Xu Yan on screen left at the foot of the tower, his face hard, his eyes on Tang Xiaotang off screen right",
  "he steps forward and holds out his hand for the note",
  ["xuyan"], [("xuyan", "多少人？", "沉聲")],
  zh="許硯中近景在左、瞭望台下，臉一沉，看著畫外右邊的唐小棠；往前一步伸手要紙條")
S("s27", "Close-up, locked", FOOT,
  f"close-up of {TANG} on screen right, the note crushed in her hand, her rosy face gone pale and serious, her eyes on Xu Yan off screen left",
  "she holds the note out toward Xu Yan off screen left and swallows",
  ["tangxiaotang"], [("tangxiaotang", "三十騎。", "壓低聲音")],
  zh="唐小棠特寫在右，紙條捏在手裡，紅潤的臉白了、一臉正經，看畫外左邊的許硯；把紙條塞進他手裡，嚥一口口水")
S("s28", "Two-shot, slow push in", FOOT,
  f"two-shot at the foot of the tower: Xu Yan on screen left turning to {QIN} on screen right, the spear on her shoulder",
  "he jabs one finger toward the village gate and she nods once and swings the spear down",
  ["xuyan", "qinshuang"], [("xuyan", "方陣排到村口，", "下令"), ("xuyan", "橋後面。", "很快")],
  zh="瞭望台下雙人鏡：許硯在左轉向右邊扛著槍的秦霜；他一根手指往村口一指，她點一下頭，槍從肩上放下")

# ── 村口 ──
S("s29", "Wide shot, locked", GATE,
  "wide shot of the village entrance at dusk: thirty horsemen in deep purple and crimson palace livery reining in on the dusty track beyond the plank bridge on screen right, the block of village youths with long staffs drawn up behind the timber gate on screen left, Xu Yan and Qin Shuang in front of them",
  f"the horses stamp and toss their heads as the column halts in a rolling cloud of dust; {DUSK}",
  ["xuyan", "qinshuang"], [("qinshuang", "穩住，", "低聲"), ("qinshuang", "誰都不許動。", "冷")], chapter="村口",
  zh="村口黃昏全景：右邊木板橋外的土路上，三十騎深紫與絳紅宮服的人馬勒住，左邊木柵門後是拿長棍的少年方陣，許硯與秦霜站在最前面；馬跺腳甩頭，隊伍停在滾起的塵土裡")
S("s30", "Medium shot, slow pan right", GATE,
  "medium shot of Leng Tie at the head of the column of riders on screen right, a lean pale beardless man in a deep purple palace eunuch's robe and black gauze hat, swinging down from his horse, a white horsetail whisk in one hand",
  f"his boots hit the dust, he flicks the whisk over the crook of his arm in one practised move and looks up at Xu Yan off screen left; {DUSK}",
  ["lengtie"], action=3,
  zh="冷鐵在右、隊伍最前面，精瘦、白臉無鬚、深紫宮服、黑紗宮帽，從馬上翻身下來，手裡一柄白拂塵；靴子落地，拂塵熟練地往臂彎一甩，抬眼看畫外左邊的許硯（第一次出場的動作；無台詞）")
S("s31", "Medium close-up, locked", GATE,
  "medium close-up of Leng Tie on screen right unrolling a long scroll of yellow silk in both hands, the whisk tucked in his elbow, his narrow knife-like eyes on Xu Yan off screen left over the top of it",
  f"the yellow silk unrolls with a soft snap and he lifts his chin; {DUSK}",
  ["lengtie"], [("lengtie", "奉旨——", "尖細，拿腔拿調"), ("lengtie", "接人。", "拖長音")],
  zh="冷鐵中近景在右，雙手展開一卷長長的黃綾，拂塵夾在臂彎，刀一樣的細眼從黃綾上緣看畫外左邊的許硯；黃綾「啪」地輕輕展開，下巴一抬")
S("s32", "Close-up, locked", GATE,
  "close-up of Xu Yan's face on screen left at the village gate, his brows drawn down and his jaw tight, his eyes on Leng Tie off screen right",
  f"he steps forward half a pace and squares his shoulders; {DUSK}",
  ["xuyan"], [("xuyan", "接誰？", "冷")],
  zh="許硯特寫在左、村口，眉頭壓低、下顎咬緊，看畫外右邊的冷鐵；往前半步，肩膀一挺")
S("s33", "Close-up, slow push in", GATE,
  "close-up of Leng Tie's pale face on screen right, a thin smile on his lips that does not reach his narrow eyes, his eyes sliding toward Aling off screen left",
  f"his eyes move slowly and stop, and the thin smile sharpens; {DUSK}",
  ["lengtie"], [("lengtie", "宮裡走失的，", "陰柔"), ("lengtie", "一位貴人。", "笑")],
  zh="冷鐵的白臉特寫在右，嘴角一個薄薄的笑、細眼沒在笑，眼睛越過許硯、滑向他身後畫外左邊的某人；眼睛慢慢移、停住，那個笑更尖")
S("s34", "Close-up, locked", GATE,
  "close-up of A-ling's face on screen left behind the ranks of youths, half in torchlight, her phoenix eyes ice-cold and level on Leng Tie off screen right",
  f"she slips one step forward between two youths' staffs into the front rank, unblinking; {DUSK}",
  ["aling"], action=2,
  zh="阿令特寫在左、少年隊伍後面，半邊臉在火把光裡，鳳眼冷得像冰、平平看著畫外右邊的冷鐵；一眨不眨，從兩個少年的長棍之間往前一步站到第一排（無台詞）")
S("s35", "Medium close-up, locked", GATE,
  "medium close-up of Leng Tie on screen right rolling the yellow silk shut with one hand, his face suddenly cold and flat, his eyes on Xu Yan off screen left",
  f"he snaps the scroll closed and lets the whisk drop to his side; {DUSK}",
  ["lengtie"], [("lengtie", "抗旨者——", "笑意一收"), ("lengtie", "斬。", "冰冷")],
  zh="【結尾】冷鐵中近景在右，一手把黃綾捲起，臉一下子冷平下來，看畫外左邊的許硯；黃綾「啪」地收起，拂塵垂到身側")
S("s36", "Wide shot, locked", GATE,
  "wide shot of the thirty horsemen in purple and crimson livery on the track on screen right, every rider's right hand on his sword hilt, thirty blades sliding half out of their scabbards at the same instant, steel flashing orange in the dusk, the village youths behind the gate on screen left",
  f"thirty blades scrape half out together with one harsh ring and stop, the steel catching the last light; {DUSK}",
  [], action=2,
  zh="【結尾】最後一格：右邊土路上三十騎紫紅宮服，每個人右手按刀柄，三十把刀在同一瞬間出鞘一半，鋼刃映著黃昏的橘光，左邊柵門後是村裡少年；三十把刀一聲刺耳的摩擦同時拔到一半、停住（無台詞）")

e.write(
  music="a single low string and the crackle of burning paper under the girl's quiet confession, a warm tender guqin thread when he says it is his family's business, a bright martial build of war drums, bamboo flutes and stamping percussion as sixty staffs strike the ground at sunrise, a quick busy plucked pipa for the courier line, an anxious high whistle-like dizi and racing frame drum as the lookout boy spots the riders, then a slow ominous low brass and muted gong for the purple-robed column, a cold thin high string under the eunuch's put-on voice, and a sharp metallic hit that cuts dead on thirty blades half drawn, ancient Chinese rural drama, no vocals",
  title="畫像進了相府沒幾天，宮服人馬停在村口：抗旨者斬",
  description="唐萬金的信燒成了灰，阿令只說了一句：「畫的是我。」她要許硯今晚就送她走，許硯只回：「畫的是妳，那就是我家的事。」天一亮，秦霜不再藏，在打穀場把六十個村裡少年排成秦家的方陣，長棍同時頓地、塵土齊揚；唐小棠用許記鏢局排出一條傳信線，二十里一站；王二牛帶人立起瞭望台。下午，瞭望台上的少年吹響竹哨：縣城來了一隊穿宮服的人馬，正四處打聽「不說話的女人」。黃昏，三十騎停在村口，為首的公公展開一卷黃綾：「奉旨接人，抗旨者斬。」《種田娶妻打天下》第 56 集。",
  thumb={"headline": "奉旨\n接人", "tag": "種田娶妻打天下", "shot": "s31"})
