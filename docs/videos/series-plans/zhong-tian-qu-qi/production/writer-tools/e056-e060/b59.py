import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from ztlib import *

chars = [ch("xuyan"), ch("aling"), ch("qinshuang"), ch("tangxiaotang"), ch("xiaohe"), ch("erniu"), ch("shimujiang"),
         ch("hanbo"), ch("dutie"), ch("lengtie"), ch("xitong")]
e = Ep(59, chars)
S = e.shot
GATE = "At the yard gate of the farmhouse at dusk, the low mud wall and the rough wooden yard gate standing open onto the village track, a barred wooden cage cart hitched to a mule outside the gate, a deep orange sky over the thatched roofs"
YARD = "In the farmhouse yard in early evening, the small dirt yard of a poor thatched farmhouse in an ancient Chinese village, the low mud wall, the yard gate and the persimmon tree, red paper lanterns being strung along the eaves, the deep blue sky with the first stars"
FEAST = "In the farmhouse yard on a clear night, the small dirt yard of a poor thatched farmhouse in an ancient Chinese village, two wooden tables pushed end to end into one long table loaded with bowls of food, red paper lanterns strung along the eaves and the persimmon tree, the low mud wall and the yard gate, warm lantern light under a deep blue starry sky"
LATE = "In the farmhouse yard late at night, the small dirt yard of a poor thatched farmhouse in an ancient Chinese village, the long table cleared and the red lanterns burned low, the persimmon tree black against a bright full moon, the low mud wall, cold silver moonlight"
QIN = "Qin Shuang in her fitted dark brown cotton short jacket and wide leather belt, her high ponytail tied with black cord"
WARM = "the warm lantern light stays unchanged"
MOON = "the cold moonlight and deep blue night stay unchanged"
DUSK = "the orange dusk light stays unchanged"

# ── 先吃飯 ──
S("s", "Wide shot, locked", GATE,
  "wide shot at the yard gate: Wang Erniu on screen left shoving Leng Tie, bound with rope in his stained purple robe, into the barred cage cart outside, Du Tie on screen right leaning on his wooden crutch and swinging the barred door shut",
  f"Leng Tie stumbles into the cage, the barred door slams and Du Tie drops the iron bolt across it; {DUSK}",
  ["erniu", "lengtie", "dutie"], chapter="先吃飯", action=2,
  zh="【鉤子1／開頭】接第 58 集（隔天黃昏）：院門口全景，王二牛在左把綁著、紫袍髒污的冷鐵推進門外的木籠囚車，右邊拄木拐的杜鐵把柵門甩上；冷鐵一個踉蹌跌進籠裡，柵門砰地關上，杜鐵把鐵閂一落（無台詞）")
S("s", "Medium close-up, locked", GATE,
  "medium close-up of Du Tie on screen right by the cage cart, a big broad-shouldered old soldier leaning on a worn wooden crutch, his sun-darkened face hard, his eyes on Xu Yan off screen left",
  f"he slaps the bars of the cage once with his free hand; {DUSK}",
  ["dutie"], [("dutie", "人，我押去州府，", "粗啞"), ("dutie", "交給褚知府。", "篤定")],
  zh="杜鐵中近景在右、囚車旁，魁梧的老兵拄著磨舊的木拐，曬黑的臉很硬，看畫外左邊的許硯；空著的手往籠子柵欄上一拍")
S("s", "Close-up, locked", GATE,
  "close-up of Leng Tie's pale face on screen right behind the wooden bars of the cage, a cold smile, his narrow eyes on Xu Yan off screen left",
  f"he leans his face close to the bars and the smile thins; {DUSK}",
  ["lengtie"], [("lengtie", "明天，", "冰冷"), ("lengtie", "你們就知道了。", "笑")],
  zh="冷鐵的白臉特寫在右、木籠柵欄後面，冷笑，細眼看畫外左邊的許硯；臉湊近柵欄，笑容變薄")
S("s", "Medium shot, locked", GATE,
  "medium shot of Wang Erniu banging his big palm flat against the bars of the cage cart on screen left, glaring at Leng Tie inside the cage on screen right",
  f"the bars rattle under his hand and he jabs a finger through them; {DUSK}",
  ["erniu"], [("erniu", "閉嘴！", "吼")],
  zh="王二牛在左，大手掌往囚車柵欄上一拍，瞪著右邊籠裡的人；柵欄被拍得嘩啦響，他一根手指從縫裡戳過去")
S("s", "Two-shot, slow push in", GATE,
  "two-shot just inside the yard gate: Xu Yan on screen left turning away from the cart toward A-ling on screen right, who stands very still watching the road beyond the gate, Xu Yan's left forearm wrapped in a strip of white cloth bandage",
  f"he steps in front of her so she has to look at him; {DUSK}",
  ["xuyan", "aling"], [("xuyan", "明天的事，", "放軟聲音"), ("xuyan", "明天再說。", "笑")],
  zh="院門內雙人鏡：許硯在左從囚車那邊轉身，走向右邊一動不動望著門外路口的阿令；他站到她面前，讓她不得不看他")
S("s", "Close-up, locked", GATE,
  "close-up of Xu Yan's face on screen left, a warm easy grin, his eyes on Aling off screen right",
  f"he tips his head toward the yard behind him; {DUSK}",
  ["xuyan"], [("xuyan", "先吃飯。", "輕鬆")],
  zh="【鉤子1】許硯特寫在左，溫暖輕鬆地笑，看畫外右邊的阿令；頭往身後的院子一偏")
S("s", "Close-up, slow push in", GATE,
  "close-up of A-ling's face on screen right in the orange dusk, her cold phoenix eyes softening for a moment, her eyes on Xu Yan off screen left",
  f"she lets out a slow breath and gives the smallest nod; {DUSK}",
  ["aling"], [("aling", "……嗯。", "很輕")],
  zh="阿令特寫在右、橘色的黃昏裡，冷冷的鳳眼軟了一下，看畫外左邊的許硯；慢慢吐一口氣，極輕地點一下頭")

# ── 不夠坐 ──
S("s", "Wide shot, slow pan right", YARD,
  "wide shot of the yard: one wooden table with a few stools and benches set out under the eaves, little Xiaohe in her patched lilac jacket running along it on screen left tapping each stool, the straw rabbit tucked under her arm",
  f"she hops from stool to stool, tapping each one with her finger as she counts; {WARM}",
  ["xiaohe"], [("xiaohe", "一、二、三、四……", "奶聲奶氣地數")], chapter="不夠坐",
  zh="院子全景：屋簷下一張木桌、幾張凳子和長凳，穿補丁淡紫小襖的小禾在左沿著桌子跑，草編兔子夾在腋下；她一張一張跳過去，用手指點著數")
S("s", "Medium close-up, locked", YARD,
  "medium close-up of little Xiaohe on screen centre by the table, her round face crumpling in dismay, one hand on the last stool, the straw rabbit hugged to her chest",
  f"she spins round toward the house with her mouth wide open; {WARM}",
  ["xiaohe"], [("xiaohe", "不夠坐！", "大喊")],
  zh="小禾中近景在中間、桌邊，圓臉一下子皺成一團，一手按著最後一張凳子，草編兔子抱在胸前；她轉身朝屋裡張大嘴大喊")
S("s", "Medium shot, locked", YARD,
  "medium shot of Carpenter Shi coming through the yard gate on screen right with a second wooden table on his shoulder, his grey stubbled face scowling, wood shavings on his leather apron",
  f"he swings the table down off his shoulder with a heavy thump beside the first one; {WARM}",
  ["shimujiang"], [("shimujiang", "吵什麼，", "粗啞，不耐煩"), ("shimujiang", "再拼一張。", "哼")],
  zh="石木匠在右，扛著第二張木桌從院門進來，花白鬍渣的臉板著，皮圍裙上沾著木屑；把桌子從肩上一甩，咚地放在第一張旁邊")
S("s", "Medium shot, locked", YARD,
  "medium shot of Elder Han stepping through the yard gate on screen left with his polished bamboo staff in one hand and a round clay wine jar hugged in the other arm, smiling through his long white beard",
  f"he lifts the jar a little to show it off and sets it on the table; {WARM}",
  ["hanbo"], [("hanbo", "酒我帶來了，", "笑呵呵"), ("hanbo", "自家釀的。", "得意")],
  zh="韓伯在左從院門進來，一手拄著磨亮的竹杖，一手抱著一個圓陶酒罈，白鬍子裡笑著；把酒罈舉一下給大家看，放到桌上")
S("s", "Wide shot, slow push in", YARD,
  "wide shot of the yard as everyone gets ready: Wang Erniu and Carpenter Shi pushing the two tables end to end into one long table, Tang Xiaotang hanging a red paper lantern on the eaves from a stool, Qin Shuang carrying a stack of bowls, Elder Han setting down a clay wine jar",
  f"the two tables bump together into one, the lantern swings up and glows, and the bowls clatter down; {WARM}",
  ["erniu", "shimujiang", "tangxiaotang"], action=3,
  zh="院子全景，大家忙著張羅：王二牛和石木匠把兩張桌子推成一張長桌，唐小棠站在凳子上把紅燈籠掛上屋簷，秦霜抱著一疊碗，韓伯放下一個陶酒罈；兩張桌子砰地合成一張，燈籠一掛亮起來，碗噹噹放下（無台詞）")
S("s", "High wide shot, tilt up", FEAST,
  "high wide shot rising from the long table: steaming bowls of braised pork, fish and greens down its length, then the whole yard full of people seated along both sides under the red lanterns, then the deep blue starry sky over the thatched roof",
  f"steam curls up off the bowls as the view climbs over the heads of the diners toward the stars; {WARM}",
  [], action=4,
  zh="奇觀：從長桌往上升的高角度全景：一路冒著熱氣的紅燒肉、魚和青菜，接著是紅燈籠下兩邊坐滿人的整個院子，最後是茅草屋頂上深藍的星空；碗上的熱氣往上捲，畫面越過大家的頭頂升向星空（無台詞）")

# ── 長桌 ──
S("s", "Two-shot, locked", FEAST,
  "two-shot at the long table: little Xiaohe kneeling up on the bench on screen left, reaching over with her chopsticks to drop a piece of braised pork into the rice bowl of A-ling, who sits beside her on screen right in her grey-white dress",
  f"Xiaohe drops the pork in and grins with her missing tooth; {WARM}",
  ["xiaohe", "aling"], [("xiaohe", "阿令姊姊，", "奶聲奶氣"), ("xiaohe", "妳也吃肉。", "笑")], chapter="長桌",
  zh="長桌雙人鏡：小禾在左跪在長凳上，伸筷子把一塊紅燒肉放進右邊坐在她旁邊的阿令碗裡，笑得燦爛；肉一放、筷子收回，露出缺了門牙的笑，阿令低頭看著碗")
S("s", "Medium close-up, locked", FEAST,
  "medium close-up of Elder Han at the head of the long table on screen left, white beard down to his chest, a small clay wine cup raised in his thin hand, his kind eyes on Xu Yan off screen right",
  f"he lifts the cup a little higher and smiles through his beard; {WARM}",
  ["hanbo"], [("hanbo", "解元公，", "蒼老溫和"), ("hanbo", "這杯敬你。", "舉杯")],
  zh="韓伯中近景在左、長桌主位，白鬍子垂到胸前，枯瘦的手舉著小陶酒杯，慈和的眼睛看畫外右邊的許硯；杯子再舉高一點，鬍子裡笑出來")
S("s", "Close-up, slow push in", FEAST,
  "close-up of Elder Han's lined face on screen left in the lantern light, shaking his head slowly in wonder, his eyes on Xu Yan off screen right",
  f"he chuckles and shakes his head; {WARM}",
  ["hanbo"], [("hanbo", "從河裡撈起來那天，", "感慨"), ("hanbo", "誰想得到。", "笑著搖頭")],
  zh="【第二季伏筆】韓伯滿是皺紋的臉特寫在左、燈籠光裡，不可思議地慢慢搖頭，看畫外右邊的許硯；笑一聲、搖搖頭")
S("s", "Medium close-up, locked", FEAST,
  "medium close-up of little Xiaohe on the bench on screen centre, her smile fading as she hears the words, hugging her straw rabbit tight to her chest",
  f"she pulls the rabbit in close, sidles along the bench toward Aling and glances at the dark yard gate; {WARM}",
  ["xiaohe"], action=2,
  zh="【第二季伏筆】小禾中近景在中間、長凳上，聽到那句話笑容慢慢沒了，把草編兔子抱得緊緊的；她把兔子抱進懷裡，沿著長凳往阿令那邊挪，往黑漆漆的院門看一眼（無台詞、沒有人提）")
S("s", "Insert of the hands on the rabbit, locked", FEAST,
  "insert under the edge of the long table of a little girl's small hand clutching a woven straw rabbit, a slender hand in a grey-white sleeve settling gently over it",
  f"the slender hand closes softly round the small one and holds it; {WARM}",
  [], action=2,
  zh="插鏡：長桌邊緣下，一隻小女孩的小手緊抓著草編兔子，一隻灰白袖子的纖手輕輕覆上去；纖手輕輕握住那隻小手，不放（阿令看見了；無台詞）")
S("s", "Medium close-up, locked", FEAST,
  "medium close-up of Du Tie on the bench on screen right, his crutch leaning on the table, his weathered face working with emotion, his tiger eyes wet, his eyes on Qin Shuang off screen left",
  f"he raises his wine cup in a big scarred hand; {WARM}",
  ["dutie"], [("dutie", "秦家的陣，", "聲音發顫"), ("dutie", "二十年沒見了。", "眼眶紅")],
  zh="杜鐵中近景在右、長凳上，木拐靠在桌邊，風霜的臉在發抖，虎目濕了，看畫外左邊的秦霜；一隻帶疤的大手舉起酒杯")
S("s", "Close-up, locked", FEAST,
  f"close-up of {QIN} on screen left at the table, her bright eyes shining in the lantern light, her chin lifted, her eyes on Du Tie off screen right",
  f"she lifts her cup to him and holds it there; {WARM}",
  ["qinshuang"], [("qinshuang", "杜叔，", "壓住哽咽"), ("qinshuang", "等我爹出來，再喝。", "笑")],
  zh="秦霜特寫在左、桌邊，明亮的眼睛在燈籠光裡閃著，下巴抬起，看畫外右邊的杜鐵；把酒杯舉向他、停在那裡")
S("s", "Medium shot, locked", FEAST,
  "medium shot of Wang Erniu on the bench on screen right with his cheeks stuffed full of braised pork, chopsticks waving, leaning across the table",
  f"he points his chopsticks down the table, still chewing; {WARM}",
  ["erniu"], [("erniu", "明天那些宮裡的——", "滿嘴肉，含糊")],
  zh="王二牛在右、長凳上，兩頰塞滿紅燒肉，揮著筷子，探過桌子對大家說；一邊嚼一邊用筷子往桌上指")
S("s", "Medium close-up, locked", FEAST,
  f"medium close-up of {TANG} on the bench on screen left, smiling very sweetly at Wang Erniu off screen right while her shoulder dips as she kicks under the table",
  f"her sweet smile never moves as her foot jabs out under the table; {WARM}",
  ["tangxiaotang"], [("tangxiaotang", "吃你的肉。", "笑得很甜，桌下一腳")],
  zh="唐小棠中近景在左、長凳上，對畫外右邊的王二牛笑得很甜，肩膀一沉，桌子底下踢了一腳；甜笑一動不動，腳在桌下一戳（大家都知道明天，卻沒人說破）")
S("s", "Medium close-up, locked", FEAST,
  "medium close-up of Wang Erniu on screen right jolting on the bench with a yelp, one hand grabbing his shin under the table, his cheeks still full of pork",
  f"he hunches over, rubs his shin and stuffs another piece of pork into his mouth; {WARM}",
  ["erniu"], [("erniu", "哎喲！", "痛"), ("erniu", "我吃，我吃。", "含糊")],
  zh="王二牛中近景在右，在長凳上痛得一彈、叫一聲，一手抓住桌下的小腿，兩頰還塞著肉；縮起來揉小腿，再塞一塊肉進嘴裡（喜劇）")
S("s", "Two-shot, locked", FEAST,
  f"two-shot at the long table: {TANG} on screen left and {QIN} on screen right, each lifting a piece of braised pork in her chopsticks toward the bowl between them at the same moment",
  f"both pairs of chopsticks reach out at the same instant and both women freeze; {WARM}",
  ["tangxiaotang", "qinshuang"], action=2,
  zh="【鉤子／中段鉤子】長桌雙人鏡：唐小棠在左、秦霜在右，同時用筷子夾起一塊紅燒肉伸向兩人中間的碗；兩雙筷子同一瞬間伸出去，兩個人都僵住（無台詞）")
S("s", "Insert of the chopsticks over the bowl, locked", FEAST,
  "insert of a rice bowl on the table in the lantern light, two pairs of chopsticks crossed in midair just above it, each holding a glistening piece of braised pork, neither moving",
  f"the two pieces of pork hover and the chopsticks tremble against each other; {WARM}",
  [], action=2,
  zh="中段爽點：插鏡，燈籠光下桌上的一碗飯，兩雙筷子在碗上方半空交叉，各夾著一塊油亮的紅燒肉，誰也不動；兩塊肉懸著，筷子互相抵得發抖（無台詞）")
S("s", "Two-shot, slow push in", FEAST,
  f"two-shot: {TANG} on screen left and {QIN} on screen right glaring at each other across the bowl, their chopsticks still locked",
  f"they lean in toward each other, neither letting go; {WARM}",
  ["tangxiaotang", "qinshuang"], [("tangxiaotang", "我先夾的。", "甜甜地"), ("qinshuang", "我手比較快。", "挑眉")],
  zh="雙人鏡：唐小棠在左、秦霜在右，隔著碗互瞪，筷子還卡在一起；兩人往彼此再靠一點，誰都不放")
S("s", "Close-up, locked", FEAST,
  "close-up of Xu Yan's face on screen centre, sitting between the two women, sweat on his forehead, his eyes darting left and right",
  f"he swallows hard and gives a weak grin; {WARM}",
  ["xuyan"], [("xuyan", "我……", "冒汗"), ("xuyan", "兩塊都吃？", "陪笑")],
  zh="許硯特寫在中間，坐在兩個女人中間，額頭冒汗，眼睛左右亂飄；用力嚥一下口水，擠出一個弱弱的笑")
S("s", "Wide shot, locked", FEAST,
  "wide shot down the length of the long table under the lanterns: everyone bursting into laughter at once, Wang Erniu pounding the table, Elder Han wiping his eyes, Carpenter Shi's scowl cracking, little Xiaohe giggling with both hands over her mouth",
  f"the laughter rolls down the table, bowls rattling as Erniu thumps it; {WARM}",
  ["erniu", "hanbo", "xiaohe"], action=3,
  zh="長桌全景、燈籠下：大家同時笑翻，王二牛拍桌子，韓伯擦眼淚，石木匠的臭臉也繃不住，小禾兩手摀著嘴咯咯笑；笑聲一路滾過長桌，二牛一拍，碗噹噹響（無台詞）")
S("s", "Medium close-up, slow push in", FEAST,
  "medium close-up of A-ling across the table on screen right, the only one not laughing aloud, setting her rice bowl down slowly, her phoenix eyes lifting to Xu Yan off screen left",
  f"she sets the bowl down with both hands and looks straight at him; {WARM}",
  ["aling"], [("aling", "謝謝你。", "很輕，第一次不帶刺")],
  zh="【中段鉤子】阿令中近景在右、桌子對面，全桌只有她沒笑出聲，慢慢放下飯碗，鳳眼抬起看畫外左邊的許硯；雙手把碗放下，直直看著他（第一句不帶刺的話）")
S("s", "Close-up, locked", FEAST,
  "close-up of Xu Yan's face on screen left, frozen with his chopsticks halfway to his mouth, his eyes wide, his eyes on Aling off screen right",
  f"the chopsticks stop in midair and his mouth falls open; {WARM}",
  ["xuyan"], [("xuyan", "妳剛剛……", "愣住"), ("xuyan", "說什麼？", "不敢相信")],
  zh="許硯特寫在左，筷子停在送到嘴邊的半路，眼睛睜大，看畫外右邊的阿令；筷子停在半空，嘴張開")
S("s", "Close-up, locked", FEAST,
  "close-up of A-ling's face on screen right, turning her face away toward the lanterns, a faint flush on her porcelain cheek",
  f"she picks up her bowl again and hides behind it; {WARM}",
  ["aling"], [("aling", "沒什麼。", "別開臉")],
  zh="阿令特寫在右，把臉轉向燈籠那邊，瓷白的臉頰泛起一點點紅；又把碗端起來躲在碗後面")
S("s", "Medium close-up, locked", FEAST,
  f"medium close-up of {TANG} on screen left bouncing on the bench and pointing across the table at Aling off screen right, her big round eyes sparkling with glee",
  f"she bounces twice and claps her hands together; {WARM}",
  ["tangxiaotang"], [("tangxiaotang", "她說謝謝你！", "興奮，大聲")],
  zh="唐小棠中近景在左，在長凳上彈了一下，手指越過桌子指著畫外右邊的阿令，大圓眼睛亮晶晶；彈兩下、雙手一拍")
S("s", "Group shot, locked", FEAST,
  "group shot down the table: little Xiaohe standing up on the bench on screen left with her arms up, Wang Erniu and Elder Han beside her, all of them turning toward Xu Yan at the far end",
  f"Xiaohe throws her arms wide and the others raise their cups; {WARM}",
  ["xiaohe", "erniu", "hanbo"], [("xiaohe", "謝謝你——", "拉長音，起鬨")],
  zh="長桌三人鏡：小禾在左站上長凳、雙手舉高，旁邊是王二牛和韓伯，大家轉向桌子另一頭的許硯；小禾兩手一張，大家舉起杯子起鬨")
S("s", "Close-up, slow push in", FEAST,
  "close-up of Xu Yan's face on screen centre in the lantern light, his eyes lifting to a point in the empty air in front of him, a dazed happy smile; the system voice speaks off screen",
  f"his eyes track across the empty air as if reading and the smile spreads slowly; {WARM}",
  ["xuyan"], [("xitong", "阿令好感，", "平板電子音，叮一聲"), ("xitong", "六十八。", "平板電子音")],
  zh="系統面板：許硯的臉在中間、燈籠光裡，眼睛抬起看著面前的空中，傻傻地開心笑；眼睛像讀字一樣掃過空中，笑容慢慢擴開",
  panel=[{"text": "阿令 好感 +4 → 68", "kind": "affection"}])
S("s", "Wide shot, slow pull out", FEAST,
  "wide shot of the whole yard from above the gate: the long table full of family and villagers under the red lanterns, little Xiaohe still standing on the bench, the starry sky over the roof; the system voice speaks off screen",
  f"little Xiaohe hops down off the bench and the diners settle back to eat; {WARM}",
  ["xiaohe"], [("xitong", "主線：天下歸心，", "平板電子音，叮一聲"), ("xitong", "百分之三。", "平板電子音")],
  zh="系統面板：從院門上方往下拍整個院子的全景，紅燈籠下坐滿人的長桌，小禾還站在長凳上，屋頂上是星空；燈籠在微風裡晃，大家坐回去吃飯",
  panel=[{"text": "主線　天下歸心：2% → 3%", "kind": "panel"}])
S("s", "Medium close-up, locked", FEAST,
  "medium close-up of Du Tie on screen right leaning over toward Xu Yan, his voice low under the noise of the table, his eyes on Xu Yan off screen left",
  f"he sets one heavy hand on the table and nods once; {WARM}",
  ["dutie"], [("dutie", "明天，", "壓低聲音"), ("dutie", "我也在。", "篤定")],
  zh="杜鐵中近景在右，在桌上的熱鬧聲裡往許硯靠過去，壓低聲音，看畫外左邊的許硯；一隻厚手往桌上一放，點一下頭")
S("s", "Medium close-up, locked", FEAST,
  "medium close-up of Carpenter Shi on screen left, his scowl back in place, a wood axe leaning against the bench beside him, his eyes on Xu Yan off screen right",
  f"he pats the axe handle without looking at it; {WARM}",
  ["shimujiang"], [("shimujiang", "我的斧頭，", "粗聲"), ("shimujiang", "也在。", "哼")],
  zh="石木匠中近景在左，臭臉又擺回來，一把斧頭靠在他身邊的長凳上，看畫外右邊的許硯；頭也不轉，拍拍斧柄")

# ── 木簪 ──
S("s", "Wide shot, locked", LATE,
  "wide shot of the quiet yard: Xu Yan alone at the cleared long table on screen left stacking empty bowls, A-ling standing under the persimmon tree on screen right in the moonlight, Xu Yan's left forearm wrapped in a strip of white cloth bandage",
  f"he sets one more bowl on the stack and looks up as she steps out of the shadow; {MOON}",
  ["xuyan", "aling"], chapter="木簪", action=3,
  zh="安靜的院子全景：許硯一個人在左、收空的長桌邊疊碗，阿令站在右邊柿子樹下的月光裡；他再疊上一個碗，抬頭，她從影子裡走出來（無台詞）")
S("s", "Medium close-up, locked", LATE,
  "medium close-up of A-ling under the persimmon tree on screen right, moonlight on her face, her hands folded at her sash, her eyes on Xu Yan off screen left",
  f"she takes one step toward him; {MOON}",
  ["aling"], [("aling", "許硯。", "很輕")],
  zh="阿令中近景在右、柿子樹下，月光落在她臉上，雙手交疊在腰帶上，看畫外左邊的許硯；往他走一步")
S("s", "Close-up, locked", LATE,
  "close-up of Xu Yan's face on screen left in the moonlight, looking up from the bowls, his eyes on Aling off screen right",
  f"he puts the last bowl down and straightens; {MOON}",
  ["xuyan"], [("xuyan", "嗯？", "抬頭")],
  zh="許硯特寫在左、月光裡，從碗堆上抬起頭，看畫外右邊的阿令；放下最後一個碗，站直")
S("s", "Close-up, slow push in", LATE,
  "close-up of A-ling's face on screen right in the moonlight, the wooden hairpin still in her black hair, a small rare softness at the corners of her mouth, her eyes on Xu Yan off screen left",
  f"her gaze drifts over the empty table and comes back to him; {MOON}",
  ["aling"], [("aling", "今天，", "很輕"), ("aling", "很好。", "幾乎笑了")],
  zh="阿令特寫在右、月光裡，木簪還在髮間，嘴角有一點難得的柔軟，看畫外左邊的許硯；眼光掃過空了的長桌，又回到他身上")
S("s", "Medium close-up, slow push in", LATE,
  "medium close-up of A-ling on screen right in the moonlight raising one hand to the plain wooden hairpin in her hair, her eyes lowered",
  f"she draws the hairpin out and her long black hair falls loose over her shoulders in one slow shining sweep; {MOON}",
  ["aling"], action=3,
  zh="顏值鏡頭：阿令中近景在右、月光裡，一隻手抬到髮間那根素木簪上，眼睛垂著；她把木簪抽出來，黑長髮慢慢地、亮亮地一下子瀉到肩上（無台詞）")
S("s", "Insert of the hairpin in his palm, locked", LATE,
  "insert in the moonlight of a plain wooden hairpin being laid across a young man's open calloused palm by a slender hand in a grey-white sleeve",
  f"her fingers set the hairpin down and press his fingers closed over it, then let go; {MOON}",
  [], action=2,
  zh="插鏡、月光下：一隻灰白袖子的纖手把一根素木簪放進一隻攤開、有繭的年輕男人手掌心；她的手指把簪子放下，把他的手指按攏，然後放開（無台詞）")
S("s", "Close-up, slow push in", LATE,
  "close-up of A-ling's face on screen right with her black hair loose around it, the moonlight on her porcelain skin, her cold face gone soft, a sheen of tears in her phoenix eyes, her eyes on Xu Yan off screen left",
  f"her lips tremble once before she speaks; {MOON}",
  ["aling"], [("aling", "明天若我不在，", "很輕，壓著"), ("aling", "替我看著這個家。", "眼眶紅")],
  zh="【結尾】阿令特寫在右，黑長髮散在臉旁，月光落在瓷白的皮膚上，冷冷的臉軟了，鳳眼裡一層水光，看畫外左邊的許硯；嘴唇抖一下才開口")
S("s", "Close-up, locked", LATE,
  "close-up of Xu Yan's face on screen left in the moonlight, the hairpin clutched in his fist at the bottom of the frame, his eyes wide and stricken, his eyes on Aling off screen right",
  f"he steps forward with his hand reaching out; {MOON}",
  ["xuyan"], [("xuyan", "阿令——", "急")],
  zh="【結尾】許硯特寫在左、月光裡，畫面下緣拳頭裡握著木簪，眼睛睜大、整個人愣住，看畫外右邊的阿令；往前一步，手伸出去")
S("s", "Medium shot, locked", LATE,
  "medium shot of A-ling on screen right turning away from Xu Yan, her loose black hair swinging across her back, walking toward the dark doorway of the house in the moonlight",
  f"she turns with her hair swinging and walks three quick steps into the shadow of the doorway without looking back; {MOON}",
  ["aling"], action=3,
  zh="【結尾】最後一格：阿令在右，轉身離開許硯，散開的黑長髮甩過背，在月光裡往黑暗的屋門走；她一轉身、頭髮一甩，快步三步走進門口的陰影，沒有回頭（無台詞）")

e.write(
  music="a warm low drum and a closing iron bolt at dusk, a gentle tender guqin as he says to eat first, a bouncing playful plucked pipa and woodblocks while the little girl counts the chairs, a broad warm swell of erhu, dizi and soft strings as the two tables become one and the lanterns go up under the stars, a nostalgic slow erhu for the old soldier, a cheeky comic xylophone sting when two pairs of chopsticks freeze over one bowl and a burst of happy percussion on the laughter, a hushed single guzheng note for her thank-you, a twinkling chime for the system, then a slow aching xiao and guzheng duet in the moonlight that rises as her hair falls and stops on her turned back, ancient Chinese rural drama, no vocals",
  title="打退刺客那晚全家坐滿一桌，冷面老婆第一次說謝謝",
  description="冷鐵被關進囚車，杜鐵說要押去州府。宮裡的人明天就到，許硯轉身對阿令說：「明天的事，明天再說，先吃飯。」小禾數椅子數到一半大喊「不夠坐！」，石木匠扛來第二張桌子，兩張拼成一張長桌，燈籠一盞盞掛起來：許硯、三位妻子、小禾、王二牛、石木匠、韓伯、杜鐵，第一次坐滿一張飯桌。王二牛剛說到「明天那些宮裡的——」就被唐小棠在桌下踢了一腳。唐小棠和秦霜同時把一塊肉夾進許硯碗裡，兩雙筷子在半空停住，全桌笑翻；阿令放下碗：「謝謝你。」好感度跳到 68。夜裡，阿令拔下頭上的木簪放進他掌心：「明天若我不在，替我看著這個家。」她眼眶紅了，轉身要走。《種田娶妻打天下》第 59 集。",
  thumb={"headline": "謝謝你", "tag": "種田娶妻打天下", "shot": "s27"})
