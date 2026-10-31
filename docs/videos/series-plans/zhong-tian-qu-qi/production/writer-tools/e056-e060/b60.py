import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from ztlib import *

chars = [ch("xuyan"), ch("aling"), ch("qinshuang"), ch("tangxiaotang"), ch("xiaohe"), ch("erniu"), ch("huxianling"), ch("changgonggong"),
         minor("jinjuntongling", "禁軍統領", "East Asian man of forty-five, square-jawed with a short black beard and hard eyes, black lamellar armour with a red cloak and a plumed iron helmet, riding a tall black horse", "Orus", "四十五歲的禁軍統領，男聲、低沉、短促、軍人口氣"),
         ch("xitong")]
e = Ep(60, chars)
S = e.shot
LATE = "In the farmhouse yard late at night, the small dirt yard of a poor thatched farmhouse in an ancient Chinese village, the long table cleared and the red lanterns burned low, the persimmon tree black against a bright full moon, the low mud wall, cold silver moonlight"
MORN = "At the yard gate of the farmhouse in bright morning light, the low mud wall and the rough wooden yard gate standing open onto the village track, a small green sedan chair set down on the track, villagers in rough brown and grey clothes crowding round, thatched roofs and the persimmon tree behind"
DAY = "In the farmhouse yard in the gold light of late afternoon, the small dirt yard of a poor thatched farmhouse in an ancient Chinese village, the low mud wall, the woodpile and the persimmon tree, a low table under the eaves with a bowl of water on it, long shadows"
DUSK = "In the farmhouse yard at sunset, the small dirt yard of a poor thatched farmhouse in an ancient Chinese village, the low mud wall and the yard gate, the persimmon tree, a low table under the eaves with a bowl of water on it, a blood-orange sky darkening to blue"
RING = "Above the farmhouse yard of the Xu family at night, the small thatched farmhouse and its dirt yard inside the low mud wall, hundreds of torches held by armoured horsemen in a great ring around the yard wall, the firelight lighting the thatched roofs of half the village, a black sky"
GATE = "At the yard gate of the farmhouse at night, the low mud wall and the open wooden yard gate, armoured imperial guards with torches on the track outside, orange firelight, a black sky"
OUT = "On the village track outside the yard gate of the farmhouse at night, ranks of armoured horsemen and foot guards holding torches, banners on poles, horses snorting, the low mud wall of the yard behind, orange firelight against a black sky"
INYARD = "In the farmhouse yard at night, the small dirt yard of a poor thatched farmhouse in an ancient Chinese village, the persimmon tree and the low mud wall, the yard gate open, the firelight of hundreds of torches beyond the wall turning the whole yard orange"
QIN = "Qin Shuang in her fitted dark brown cotton short jacket and wide leather belt, her high ponytail tied with black cord"
HU = "Magistrate Hu, pale and plump in his blue-green official robe and black gauze hat"
CH = "Eunuch Chang, an old pale beardless man in a dark teal palace robe with a folded moon-white palace gown held in both hands"
YOUNG = "a younger pale eunuch of about thirty in a deep purple robe and black gauze hat with a white horsetail whisk, his face long and cold with narrow upturned eyes"
MOON = "the cold moonlight and deep blue night stay unchanged"
FIRE = "the orange torchlight and black night stay unchanged"
SUN = "the low gold light stays unchanged"

# ── 哪裡都不去 ──
S("s", "Insert of the hairpin pressed into her palm, locked", LATE,
  "insert in the moonlight of a young man's hand catching a slender hand in a grey-white sleeve, pressing a plain wooden hairpin back into its palm and folding the fingers closed over it; Xu Yan speaks off screen",
  f"his fingers fold hers shut round the hairpin one by one and hold them there; {MOON}",
  [], [("xuyan", "妳哪裡都不去。", "畫外，很輕但很硬")], chapter="哪裡都不去",
  zh="【鉤子1／開頭】接第 59 集：月光下的插鏡，一隻年輕男人的手抓住一隻灰白袖子的纖手，把素木簪按回她掌心，把她的手指一根根合上；他把她的手指合攏在簪子上、握住不放（許硯畫外）")
S("s", "Two-shot, slow push in", LATE,
  "two-shot under the persimmon tree: Xu Yan on screen left holding A-ling's closed hand in both of his, A-ling on screen right with her long black hair loose over her shoulders, her phoenix eyes wet in the moonlight",
  f"she tries once to pull her hand back and he does not let go; {MOON}",
  ["xuyan", "aling"], [("aling", "你不知道，", "哽住"), ("aling", "我是誰。", "很輕")],
  zh="柿子樹下雙人鏡：許硯在左雙手握著阿令合起的手，阿令在右，黑長髮散在肩上，鳳眼在月光下濕了；她抽一下手，他不放")
S("s", "Close-up, locked", LATE,
  "close-up of Xu Yan's face on screen left in the moonlight, his eyes steady and warm, his eyes on Aling off screen right",
  f"he shakes his head slowly and a small smile comes; {MOON}",
  ["xuyan"], [("xuyan", "妳是阿令。", "很穩"), ("xuyan", "許家的阿令。", "笑")],
  zh="許硯特寫在左、月光裡，眼神又定又暖，看畫外右邊的阿令；慢慢搖頭，笑了一下")
S("s", "Medium close-up, slow push in", LATE,
  "medium close-up of A-ling on screen right in the moonlight, her loose black hair over her shoulders, the wooden hairpin in her hand, a tear sliding down her porcelain cheek",
  f"she gathers her hair up in one hand and slides the wooden hairpin back through it, pinning it up; {MOON}",
  ["aling"], action=3,
  zh="阿令中近景在右、月光裡，黑長髮散在肩上，手上拿著木簪，一滴淚滑過瓷白的臉頰；她一手把頭髮攏起來，把木簪重新插回去、挽好（她留下）（無台詞）")

# ── 縣令 ──
S("s", "Close-up, locked", LATE,
  "close-up of A-ling's face on screen right with her hair pinned up again, the tear drying on her cheek, her eyes on Xu Yan off screen left",
  f"she draws a breath and her voice steadies; {MOON}",
  ["aling"], [("aling", "明天，", "很輕"), ("aling", "別擋在我前面。", "倔")],
  zh="阿令特寫在右，頭髮重新挽好，淚痕還在臉上，看畫外左邊的許硯；吸一口氣，聲音穩下來")
S("s", "Close-up, locked", LATE,
  "close-up of Xu Yan's face on screen left in the moonlight, a lopsided grin, his eyes on Aling off screen right",
  f"he shrugs one shoulder; {MOON}",
  ["xuyan"], [("xuyan", "好，", "笑"), ("xuyan", "那我站旁邊。", "耍賴")],
  zh="許硯特寫在左、月光裡，歪嘴一笑，看畫外右邊的阿令；聳一邊肩膀（甜）")
S("s", "Wide shot, locked", MORN,
  f"wide shot at the yard gate: {HU} climbing out of the green sedan chair on screen right with two yamen runners behind him carrying gift baskets, villagers crowding the track, Xu Yan standing in the open yard gate on screen left",
  "the magistrate hurries up the track with his robe hitched up, bowing as he comes",
  ["huxianling", "xuyan"], chapter="縣令", action=3,
  zh="早上院門口全景：穿青綠官袍、戴烏紗的胡縣令從右邊的綠呢小轎裡鑽出來，後面兩個衙役捧著禮籃，村民擠滿小路，許硯站在左邊開著的院門口；縣令提著袍子一路小跑上來，邊走邊作揖（無台詞）")
S("s", "Medium close-up, locked", MORN,
  f"medium close-up of {HU} on screen right bowing low again and again with both palms pressed together, a huge fawning smile shaking his double chin, his eyes on Xu Yan off screen left",
  "he bows so deep his gauze hat nearly slips and he grabs it",
  ["huxianling"], [("huxianling", "解元公！", "拖長音，諂媚"), ("huxianling", "下官來給您請安！", "陪笑")],
  zh="胡縣令中近景在右，雙手合掌一鞠再鞠，諂媚的大笑讓雙下巴直抖，看畫外左邊的許硯；鞠得太低烏紗帽差點掉，他一把扶住")
S("s", "Medium close-up, locked", MORN,
  "medium close-up of Xu Yan in the yard gate on screen left with his arms folded, his face perfectly deadpan, his eyes on Magistrate Hu off screen right",
  "he tilts his head and raises one eyebrow",
  ["xuyan"], [("xuyan", "胡大人上回來，", "面無表情"), ("xuyan", "是來抓人的。", "淡淡地")],
  zh="許硯中近景在左、院門口，雙手抱胸，臉上一點表情都沒有，看畫外右邊的胡縣令；頭一歪、一邊眉毛挑起")
S("s", "Close-up, locked", MORN,
  f"close-up of {HU} on screen right, sweat beading on his plump forehead, his fawning smile frozen, his eyes on Xu Yan off screen left",
  "he dabs at his forehead with his big sleeve and laughs too loudly",
  ["huxianling"], [("huxianling", "誤會，", "冒汗"), ("huxianling", "都是誤會！", "乾笑")],
  zh="胡縣令特寫在右，白胖的額頭冒出汗珠，諂媚的笑僵住，看畫外左邊的許硯；用大袖子擦額頭，笑得太大聲")
S("s", "Medium shot, locked", MORN,
  f"medium shot on the track: {HU} backing away on screen right between his two yamen runners, his plump face drained white, his eyes fixed on Aling in the yard off screen left",
  "he stumbles backward into the runners and flaps a sleeve at them",
  ["huxianling"], [("huxianling", "這、這位……", "臉一白"), ("huxianling", "下官告退！", "結巴")],
  zh="小路上：胡縣令在右，夾在兩個衙役中間往後退，白胖的臉一下子沒了血色，眼睛盯著畫外左邊院子裡的阿令；往後撞到衙役，甩袖子叫他們走（他當初收錢要抓的就是她）")
S("s", "Medium shot, slow pan right", MORN,
  f"medium shot on the track: Wang Erniu on screen left with one big friendly hand on the back of {HU}, steering him back toward the green sedan chair on screen right, laughing villagers lining the way",
  "Erniu gives the magistrate a cheerful shove and the villagers laugh and clap",
  ["erniu", "huxianling"], [("erniu", "大人，", "大嗓門，笑"), ("erniu", "慢走——", "拉長音")],
  zh="小路上：王二牛在左，一隻大手熱情地推著胡縣令的背，把他往右邊的綠呢小轎送，兩旁村民哈哈笑；二牛開心地一推，村民又笑又拍手")
S("s", "Medium shot, locked", MORN,
  "medium shot of little Xiaohe running out of the yard gate on screen left with a live brown hen flapping in her arms, her red-string pigtails bouncing",
  "she holds the squawking hen out at arm's length as its wings beat in her face",
  ["xiaohe"], [("xiaohe", "大人，", "奶聲奶氣，喊"), ("xiaohe", "您的雞忘了！", "認真")],
  zh="小禾在左從院門跑出來，懷裡一隻活的棕母雞拍著翅膀，紅繩小辮一跳一跳；她把咯咯叫的母雞伸長手臂遞出去，雞翅膀拍到她臉上")
S("s", "Wide shot, locked", MORN,
  f"wide shot on the track: {HU} scrambling backward into the green sedan chair on screen right as the brown hen flaps in after him, the runners hoisting the poles, the villagers doubled over laughing on screen left",
  "the hen lands in his lap, he yelps, the curtain drops and the bearers trot off fast down the track",
  ["huxianling"], action=3,
  zh="前半爽點：小路全景，胡縣令手忙腳亂退進右邊的綠呢小轎，那隻母雞跟著撲進去，轎夫抬起轎桿，左邊村民笑彎了腰；母雞落到他腿上，他叫一聲，轎簾一落，轎夫一溜小跑抬走了（無台詞）")

# ── 配婚令 ──
S("s", "Medium shot, locked", DAY,
  f"medium shot at the low table under the eaves: Xu Yan on screen left lifting the lid of a small wooden box and taking out a folded red paper decree and a folded marriage document, {TANG} on screen right leaning over to look",
  f"he unfolds the red paper and holds it up to the light; {SUN}",
  ["xuyan", "tangxiaotang"], [("tangxiaotang", "配婚令？", "愣住")], chapter="配婚令",
  zh="屋簷下的矮桌：許硯在左掀開一個小木盒，拿出一張摺好的紅紙配婚令和一份摺好的婚書，高領桃粉襦裙的唐小棠在右湊過來看；他把紅紙打開，舉到光下")
S("s", "Medium close-up, locked", DAY,
  f"medium close-up of {TANG} on screen right, her big round eyes wide with disbelief, pointing at the red paper beyond the frame",
  f"she jabs her finger toward it twice; {SUN}",
  ["tangxiaotang"], [("tangxiaotang", "拿這張紙，", "不敢相信"), ("tangxiaotang", "擋宮裡的人？", "提高聲音")],
  zh="唐小棠中近景在右，大圓眼睛睜得不敢相信，指著畫外那張紅紙；手指戳兩下")
S("s", "Close-up, slow push in", DAY,
  "close-up of Xu Yan's face on screen left in the gold light, looking down at the red paper in his hands, a faint fond smile",
  f"his thumb smooths the old crease in the paper; {SUN}",
  ["xuyan"], [("xuyan", "當初這張紙，", "想起第一天"), ("xuyan", "把她送進許家。", "很輕")],
  zh="許硯特寫在左、金色的光裡，低頭看著手上的紅紙，淡淡地笑了一下；拇指撫平紙上的舊摺痕（呼應第 1 集）")
S("s", "Medium shot, locked", DAY,
  "medium shot of Wang Erniu striding in through the yard gate on screen right with a long staff over his shoulder, a line of village youths with staffs filing in behind him",
  f"he slams the butt of his staff into the dirt and grins; {SUN}",
  ["erniu"], [("erniu", "六十個人，", "大嗓門"), ("erniu", "全到了！", "得意")],
  zh="王二牛在右，扛著長棍大步走進院門，後面一排拿棍的村裡少年跟進來；他把棍尾往泥地一頓，咧嘴笑")
S("s", "Two-shot, locked", DAY,
  f"two-shot in the yard: {QIN} on screen right with her spear on her shoulder, turning to Xu Yan on screen left, the woodpile behind them",
  f"she drops the spear from her shoulder into her hand; {SUN}",
  ["qinshuang", "xuyan"], [("qinshuang", "真打起來呢？", "直接"), ("xuyan", "不打。", "馬上")],
  zh="院子雙人鏡：秦霜在右扛著槍，轉向左邊的許硯，後面是柴堆；她把槍從肩上放到手裡")
S("s", "Close-up, locked", DAY,
  "close-up of Xu Yan's face on screen left, serious now, his eyes on Qin Shuang off screen right",
  f"he folds the red paper once and holds it tight; {SUN}",
  ["xuyan"], [("xuyan", "打了，", "沉聲"), ("xuyan", "就是造反。", "一字一字")],
  zh="衝突：許硯特寫在左，正經起來，看畫外右邊的秦霜；把紅紙摺一摺、捏緊")
S("s", "Medium close-up, locked", DAY,
  "medium close-up of A-ling in the dark doorway of the house on screen right, the wooden hairpin in her black hair, her arms folded tight, her eyes on Xu Yan off screen left",
  f"she steps out of the doorway into the gold light; {SUN}",
  ["aling"], [("aling", "為了我，", "很輕"), ("aling", "不值得。", "冷")],
  zh="阿令中近景在右、屋門的暗處，木簪挽髮，雙臂抱得很緊，看畫外左邊的許硯；從門裡走出來，走進金色的光")
S("s", "Close-up, locked", DAY,
  "close-up of Xu Yan's face on screen left, a crooked confident grin coming back, his eyes on Aling off screen right",
  f"he tucks the red paper into the front of his robe and pats it; {SUN}",
  ["xuyan"], [("xuyan", "值不值，", "笑"), ("xuyan", "我說了算。", "篤定")],
  zh="許硯特寫在左，那個歪嘴的自信笑容回來了，看畫外右邊的阿令；把紅紙塞進衣襟、拍一拍")

# ── 火把 ──
S("s", "Insert of the bowl of water, locked", DUSK,
  "insert of a clay bowl of water on the low table in the red sunset light, the surface of the water trembling and rings spreading across it",
  "the rings grow sharper and the bowl begins to rattle against the table",
  [], chapter="火把", action=2,
  zh="插鏡：夕陽紅光裡，矮桌上一碗清水，水面在抖、一圈圈漣漪擴開；漣漪越來越密，碗開始在桌上喀喀作響（遠處的馬蹄聲像悶雷；無台詞）")
S("s", "Medium shot, locked", DUSK,
  "medium shot of Wang Erniu bursting in through the yard gate on screen right, out of breath, one arm flung back toward the village track, his eyes on Xu Yan off screen left",
  "he skids to a stop in the dirt, gulping air",
  ["erniu"], [("erniu", "來了！", "大喊"), ("erniu", "好多火把！", "喘")],
  zh="王二牛在右從院門衝進來，上氣不接下氣，一隻手臂往後指著村路，看畫外左邊的許硯；在泥地上煞住，大口喘氣")
S("s", "Wide shot, slow pull out", RING,
  "high wide shot from above the yard: hundreds of torches carried by armoured horsemen closing in a great glowing ring around the Xu family's small thatched farmhouse and yard, the firelight spreading over the roofs of half the village",
  f"the ring of torches tightens around the yard wall and the horses come to a stop shoulder to shoulder; {FIRE}",
  [], action=4,
  zh="【中段鉤子／奇觀】從院子上方往下的高角度全景：上百支火把由披甲騎兵拿著，圍成一個發亮的大圈，把許家小小的茅屋和院子圍住，火光照亮半個柳溪的屋頂；火把圈越收越緊，馬一匹挨一匹停住（無台詞）")
S("s", "Two-shot, locked", INYARD,
  f"two-shot by the persimmon tree: little Xiaohe on screen left clutching her straw rabbit and pressing into the side of {TANG} on screen right, who wraps an arm round her",
  f"Xiaohe buries her face in Tang Xiaotang's sleeve and Tang Xiaotang pulls her in close; {FIRE}",
  ["xiaohe", "tangxiaotang"], [("xiaohe", "姊姊，", "怕"), ("xiaohe", "好多人……", "小聲")],
  zh="柿子樹旁雙人鏡：小禾在左抱著草編兔子、往右邊唐小棠身上貼，唐小棠一隻手臂把她摟住；小禾把臉埋進唐小棠的袖子，唐小棠把她摟緊")
S("s", "Insert of the hooves, locked", GATE,
  "insert at ground level of iron-shod horse hooves stamping and pawing the dirt of the track in the torchlight, dust and sparks of firelight flying",
  f"a hoof strikes down hard and the dust jumps; {FIRE}",
  [], action=1,
  zh="插鏡：貼地拍火光裡釘了鐵掌的馬蹄在小路的泥土上跺、刨，塵土和火光的碎點飛起；一隻馬蹄重重踏下，塵土一跳（無台詞）")
S("s", "Medium shot, low angle, locked", GATE,
  "medium shot from a low angle of the guard commander on a tall black horse on screen right outside the yard gate, black lamellar armour and a red cloak, a plumed iron helmet, his gloved hand on his sword hilt, his eyes on the yard off screen left",
  f"the horse stamps and he reins it round to face the gate; {FIRE}",
  ["jinjuntongling"], [("jinjuntongling", "禁軍奉旨，", "低沉，短促"), ("jinjuntongling", "請貴人出來！", "命令")],
  zh="禁軍統領低角度在右、院門外，騎一匹高大的黑馬，黑色鱗甲、紅披風、插羽鐵盔，戴手套的手按著刀柄，看畫外左邊的院子；馬一跺腳，他勒馬轉向院門")
S("s", "Two-shot, locked", INYARD,
  "two-shot in the firelit yard: A-ling on screen right taking a step toward the gate, Xu Yan on screen left catching her by the wrist without looking round",
  f"she pulls once against his grip and he holds on; {FIRE}",
  ["aling", "xuyan"], [("aling", "讓我出去。", "很輕")],
  zh="火光院子雙人鏡：阿令在右往院門跨一步，許硯在左頭也不回地扣住她的手腕；她掙一下，他不放")
S("s", "Close-up, locked", INYARD,
  "close-up of Xu Yan's face on screen left lit orange by the torches, calm and certain, his eyes on Aling off screen right",
  f"he lets go of her wrist gently and turns toward the gate; {FIRE}",
  ["xuyan"], [("xuyan", "我說過，", "很穩"), ("xuyan", "妳哪裡都不去。", "笑了一下")],
  zh="許硯特寫在左，臉被火把照成橘色，平靜而篤定，看畫外右邊的阿令；輕輕放開她的手腕，轉身面向院門")
S("s", "Medium close-up, locked", INYARD,
  f"medium close-up of {QIN} on screen right by the persimmon tree, the red-tasselled spear in her fist, her eyes on Xu Yan off screen left",
  f"she swings the spear down from her shoulder into both hands; {FIRE}",
  ["qinshuang"], [("qinshuang", "去吧，", "利落"), ("qinshuang", "我在你後面。", "篤定")],
  zh="秦霜中近景在右、柿子樹旁，手握紅纓槍，看畫外左邊的許硯；槍從肩上一甩，雙手握住")
S("s", "Medium shot, slow push in", GATE,
  "medium shot of Xu Yan walking out alone into the open yard gate on screen left, the folded red decree and the marriage document in one hand, the wall of torches and horses filling screen right",
  f"he walks three steady steps and stops square in the middle of the gateway; {FIRE}",
  ["xuyan"], action=3,
  zh="許硯在左，一個人走到開著的院門正中，一手拿著摺好的紅紙配婚令與婚書，右邊滿是火把與馬；他穩穩走三步，正正停在門口中間（無台詞）")
S("s", "Medium close-up, locked", GATE,
  "medium close-up of Xu Yan in the gateway on screen left, the torchlight hard on his face, his eyes on the guard commander off screen right",
  f"he lifts his chin and holds the papers at his side; {FIRE}",
  ["xuyan"], [("xuyan", "這裡，", "平靜"), ("xuyan", "沒有貴人。", "一字一字")],
  zh="許硯中近景在左、院門中間，火光硬硬地打在他臉上，看畫外右邊的禁軍統領；下巴一抬，紙拿在身側")
S("s", "Close-up, locked", OUT,
  "close-up of the guard commander's hard bearded face on screen right under his plumed helmet, his eyes narrowing on Xu Yan off screen left",
  f"he draws his sword an inch out of the scabbard; {FIRE}",
  ["jinjuntongling"], [("jinjuntongling", "抗旨，", "冷"), ("jinjuntongling", "是死罪。", "一字一字")],
  zh="禁軍統領插羽鐵盔下那張硬朗的鬍子臉特寫在右，眼睛瞇起盯著畫外左邊的許硯；刀從鞘裡抽出一寸")
S("s", "Medium close-up, low angle, slow push in", GATE,
  "medium close-up from a low angle of Xu Yan in the gateway on screen left raising the red decree high in one hand, the firelight blazing through the red paper, his eyes on the commander off screen right",
  f"he lifts the red paper up between himself and the torches; {FIRE}",
  ["xuyan"], [("xuyan", "這是官府發的，", "揚聲"), ("xuyan", "配婚令。", "一字一字")],
  zh="中段翻轉：許硯中近景、低角度在左、院門口，一手把紅紙配婚令高高舉起，火光透過紅紙，看畫外右邊的統領；他把紅紙舉在自己和火把之間")
S("s", "Close-up, locked", GATE,
  "close-up of Xu Yan's face on screen left beneath the raised red paper, his jaw set, his burning eyes fixed straight ahead past the paper",
  f"he does not blink; {FIRE}",
  ["xuyan"], [("xuyan", "她是我許家的人。", "很穩，很硬")],
  zh="許硯特寫在左、舉起的紅紙下，下顎咬緊，眼睛灼灼地盯著畫外右邊的統領；一下都不眨")
S("s", "Wide shot, locked", INYARD,
  f"wide shot of the yard from behind the gate: sixty village youths with long staffs stepping up into a square block filling the yard behind Xu Yan in the gateway, {QIN} at their front with her red-tasselled spear",
  f"the block steps forward as one and sixty staffs strike the dirt with a single crack; {FIRE}",
  ["qinshuang", "xuyan"], action=3,
  zh="中段爽點：從院門後拍院子全景，六十個拿長棍的村裡少年在門口的許硯身後站成方陣、填滿院子，秦霜握紅纓槍站在陣前；整個方陣一起往前一步，六十根長棍同時頓地「啪」一聲（無台詞）")
S("s", "Medium close-up, locked", INYARD,
  f"medium close-up of {QIN} at the front of the block on screen right, the spear upright, firelight on her fierce face, her eyes on the commander beyond the gate",
  f"she plants the spear butt in the dirt; {FIRE}",
  ["qinshuang"], [("qinshuang", "列陣——", "號令"), ("qinshuang", "站定！", "斷喝")],
  zh="秦霜中近景在右、方陣最前面，槍立著，火光打在她狠狠的臉上，看著院門外的統領；槍尾往泥地一頓")
S("s", "Close-up, slow push in", OUT,
  "close-up of the guard commander's face on screen right, his hard eyes moving slowly over the block of youths beyond the gate, a flicker of grudging respect",
  f"he lets the sword slide back into its scabbard and lifts his gloved hand; {FIRE}",
  ["jinjuntongling"], [("jinjuntongling", "收刀。", "低沉")],
  zh="禁軍統領特寫在右，硬硬的眼睛慢慢掃過門內的少年方陣，閃過一點不情願的佩服；刀滑回鞘裡，戴手套的手舉起來")
S("s", "Insert of the swords going back into their scabbards, locked", GATE,
  "insert of a row of armoured guards' gloved hands on their sword hilts in the torchlight, every blade sliding back into its scabbard at the same moment",
  f"the blades slide home together with one long scrape and a click; {FIRE}",
  [], action=1,
  zh="插鏡：火光裡一排披甲侍衛戴手套的手握著刀柄，每一把刀同時滑回鞘裡；刀一起入鞘，長長一聲摩擦、喀一聲（無台詞）")
S("s", "Close-up, locked", INYARD,
  f"close-up of {TANG} on screen left by the persimmon tree, little Xiaohe hugged against her side, her big round eyes wide, her eyes on the gate off screen right",
  f"she lets out a shaky breath; {FIRE}",
  ["tangxiaotang"], [("tangxiaotang", "他……", "不敢相信"), ("tangxiaotang", "收刀了？", "小聲")],
  zh="唐小棠特寫在左、柿子樹旁，小禾抱在她身側，大圓眼睛睜大，看畫外右邊的院門；抖抖地吐一口氣")

# ── 長公主殿下 ──
S("s", "Wide shot, locked", GATE,
  f"wide shot of the track outside the gate: the rows of armoured guards with torches parting down the middle, {CH} walking slowly up the gap toward the gate on screen centre, {YOUNG} walking at his elbow",
  f"the ranks step aside and the two eunuchs come up the gap, the old one's steps unsteady; {FIRE}",
  ["changgonggong"], chapter="長公主殿下", action=3,
  zh="【第二季伏筆】院門外小路全景：一排排拿火把的披甲侍衛從中間讓開，穿深青宮服、雙手捧著一件疊好的月白宮裝的常公公從空出的路慢慢走向院門，他身邊跟著一個三十歲上下、穿深紫宮服、戴黑紗帽、拿白拂塵的年輕白臉太監（跟冷鐵扮的假公公同一種深紫）；隊伍讓開，兩個太監走上來，老的那個腳步不穩（無台詞）")
S("s", "Medium shot, slow push in", GATE,
  f"medium shot of {CH} on screen right walking toward the gate, his kind round face trembling, his old eyes wet and fixed on someone in the yard beyond Xu Yan",
  f"he walks faster, the folded gown shaking in his hands; {FIRE}",
  ["changgonggong"], action=2,
  zh="常公公在右走向院門，慈和的圓臉在抖，老眼濕了，盯著許硯身後院子裡的某個人；他越走越快，手上疊好的宮裝跟著抖（無台詞）")
S("s", "Medium close-up, locked", GATE,
  "medium close-up of Xu Yan in the gateway on screen left stepping sideways into the old eunuch's path, the red paper still in his hand, his eyes on Eunuch Chang off screen right",
  f"he puts up his free hand to stop him; {FIRE}",
  ["xuyan"], [("xuyan", "公公，", "攔住"), ("xuyan", "她是——", "話沒說完")],
  zh="許硯中近景在左、院門口，往旁邊一步擋住老太監的路，紅紙還在手上，看畫外右邊的常公公；舉起空著的手要攔")
S("s", "Two-shot, locked", INYARD,
  f"two-shot inside the gate: {CH} on screen right walking straight past Xu Yan on screen left as if he were not there, Xu Yan turning on the spot to follow him with his eyes",
  f"the old eunuch brushes past his raised hand and Xu Yan swings round after him; {FIRE}",
  ["changgonggong", "xuyan"], action=2,
  zh="院門內雙人鏡：常公公在右，像沒看見一樣從左邊許硯身邊直直走過去，許硯在原地轉身，眼睛跟著他；老太監擦過他舉起的手，許硯一個轉身追著看（無台詞）")
S("s", "Close-up, slow push in", INYARD,
  "close-up of A-ling's face on screen left standing in the middle of the firelit yard, the plain wooden hairpin in her black hair, her porcelain face lit gold by the torches, her phoenix eyes on the old eunuch off screen right",
  f"her eyes go still and her chin lifts; {FIRE}",
  ["aling"], action=1,
  zh="阿令特寫在左，站在火光照亮的院子正中，素木簪挽髮，瓷白的臉被火把照成金色，鳳眼看著畫外右邊的老太監；眼神一定，下巴抬起（無台詞）")
S("s", "Medium shot, locked", INYARD,
  f"medium shot in the yard: {CH} on screen right dropping heavily to both knees in the dirt before A-ling on screen left and lifting the folded moon-white gown up to her in both hands",
  f"his knees hit the dirt and he raises the gown high, his head bowing low; {FIRE}",
  ["changgonggong", "aling"], [("changgonggong", "長公主殿下——", "哭腔，顫抖")],
  zh="【結尾】院子裡：常公公在右，撲通一聲雙膝跪在左邊阿令面前的泥地上，雙手把疊好的月白宮裝高高捧向她；膝蓋砸在土上，他把宮裝舉高，頭深深低下")
S("s", "High wide shot, locked", RING,
  "high wide shot from above the yard: the whole great ring of armoured guards around the yard dropping to one knee at the same instant, torches dipping in a wave that runs all the way around the circle",
  f"the wave of kneeling men races round the ring with a roll of clashing armour and the torches settle low; {FIRE}",
  [], action=3,
  zh="【結尾／奇觀】從院子上方的高角度全景：圍著院子的整圈披甲侍衛在同一瞬間單膝跪地，火把一路往下沉，像一道浪繞著整個圈跑一圈；跪下的浪繞圈衝過去，盔甲嘩啦一片，火把低低定住（無台詞）")
S("s", "Low insert of the kneeling boots, locked", GATE,
  "low insert at ground level of a row of armoured knees and black leather boots slamming down into the dirt of the track, the torchlight catching one boot heel turned up and its neat row of iron studs hammered in a cloud-scroll pattern",
  f"the knees thud down in a line and the studded heel glints once in the firelight; {FIRE}",
  [], action=1,
  zh="【第二季伏筆】貼地的低角度插鏡：一排披甲的膝蓋與黑皮靴砸進小路的泥土，火光照到一隻翻起的靴跟，上面整整齊齊一排雲紋鐵釘（跟第 57、58 集冷鐵那夥人的靴子一樣）；膝蓋一排落地，那隻釘靴跟在火光裡一閃（無台詞、沒有人提）")
S("s", "Medium close-up, locked", GATE,
  f"medium close-up of {YOUNG} on screen centre among the kneeling guards, sinking to one knee half a beat after everyone else, his head bowed but his narrow eyes lifted, watching Xu Yan off screen left instead of the princess",
  f"his knee comes down last and his cold eyes stay up, fixed on Xu Yan; {FIRE}",
  [], action=2,
  zh="【第二季伏筆】中近景在中間：跪著的侍衛中間，那個穿深紫宮服、拿白拂塵的年輕太監比所有人慢半拍才單膝跪下，頭低著，細長的眼睛卻抬著，看的不是公主，而是畫外左邊的許硯；他的膝蓋最後一個落地，冷冷的眼睛一直抬著盯住許硯（無台詞、不點名）")
S("s", "Two-shot, locked", INYARD,
  f"two-shot by the persimmon tree: {TANG} on screen left with her mouth fallen open, {QIN} on screen right with her spear slipping in her grip, both staring at A-ling beyond the frame",
  f"Qin Shuang's spear tip sags toward the dirt; {FIRE}",
  ["tangxiaotang", "qinshuang"], [("tangxiaotang", "長……", "張大嘴"), ("tangxiaotang", "長公主？", "不敢相信")],
  zh="柿子樹旁雙人鏡：唐小棠在左嘴張得大大的，秦霜在右，手上的槍差點握不住，兩人都盯著畫外的阿令；秦霜的槍尖往泥地垂下去")
S("s", "Medium close-up, locked", INYARD,
  "medium close-up of little Xiaohe on screen centre peeking out from behind Tang Xiaotang's sleeve, her straw rabbit hugged tight, her big eyes round with wonder",
  f"she tugs the sleeve and looks up; {FIRE}",
  ["xiaohe"], [("xiaohe", "長公主，", "小聲"), ("xiaohe", "是什麼？", "好奇")],
  zh="小禾中近景在中間，從唐小棠的袖子後面探出頭，草編兔子抱得緊緊的，大眼睛圓滾滾地發亮；扯一扯袖子、抬頭看")
S("s", "Close-up, slow push in", INYARD,
  "close-up of A-ling's face on screen left in the centre of the firelit yard, her back straight, the wooden hairpin in her black hair, every flicker of the torchlight falling on her face, her phoenix eyes clear and commanding for the first time, looking down at the kneeling eunuch",
  f"she lifts her chin a fraction more and her gaze settles, regal and calm; {FIRE}",
  ["aling"], action=3,
  zh="顏值鏡頭：阿令特寫在左、火光院子的正中，背脊筆直，素木簪挽髮、灰白粗布裙，所有火光都落在她臉上，鳳眼第一次清亮而有威，往下看著跪著的老太監；下巴再抬一分，眼神定下來，從容得像長公主（無台詞）")
S("s", "Medium close-up, locked", INYARD,
  f"medium close-up of {CH} kneeling on screen right, tears running down his kind old face, the folded gown held up in his shaking hands, his eyes lifted to Aling off screen left",
  f"his shoulders shake as he bows his head over the gown; {FIRE}",
  ["changgonggong"], [("changgonggong", "奴才找您，", "哭腔"), ("changgonggong", "找得好苦。", "泣不成聲")],
  zh="【結尾】常公公中近景在右、跪著，眼淚順著慈和的老臉往下流，發抖的雙手捧著疊好的宮裝，抬眼看畫外左邊的阿令；他肩膀發抖，頭低到宮裝上")
S("s", "Close-up, locked", INYARD,
  "close-up of Xu Yan's face on screen right in the firelight, frozen, his eyes wide on Aling off screen left; the system voice speaks off screen",
  f"he does not breathe; his lips part and stay parted; {FIRE}",
  ["xuyan"], [("xitong", "身分揭曉：", "平板電子音，叮一聲"), ("xitong", "大衡長公主，", "平板電子音"), ("xitong", "蕭令儀。", "平板電子音")],
  zh="【結尾】系統面板：許硯特寫在右、火光裡，整個人僵住，眼睛睜大看著畫外左邊的阿令；他沒有呼吸，嘴唇張開、就那樣張著（m02 揭曉）",
  panel=[{"text": "身分揭曉｜阿令：大衡長公主　蕭令儀", "kind": "panel"}])
S("s", "Insert of the red decree in his hand, locked", INYARD,
  "insert of a young man's hand in a faded blue-grey sleeve holding the folded red decree raised in midair, stopped dead, the torchlight shining through the red paper, the kneeling figures blurred in the firelight behind",
  f"the hand stays frozen in the air and the red paper trembles very slightly; {FIRE}",
  [], action=2,
  zh="【結尾】最後一格：一隻青灰舊袖的手舉著摺好的紅紙配婚令停在半空，一動不動，火光透過紅紙，後面糊開的是火光裡跪著的人影；手僵在空中，紅紙輕輕地抖（無台詞；第一季完）")

e.write(
  music="a hushed aching xiao and guzheng in the moonlight as he closes her fingers round the hairpin, a cheeky bouncing comic pipa and woodblock for the fawning magistrate and a squawking brass-like sting for the hen, a warm reflective guqin over the old red decree in the gold afternoon, then a low distant thunder of taiko that grows into galloping war drums as the ring of torches closes, a cold heavy brass for the guard commander, a defiant rising erhu and strings as he holds up the red paper and sixty staffs crack the ground, a breath of silence when the swords go home, then a slow solemn palace melody of bells and sheng as the old eunuch walks up, a huge orchestral swell and a rolling wave of drums and cymbals as the whole ring kneels, a single trembling high string for the princess's gaze, a chime for the system, and a final deep drum hit and held strings that stop on the red paper frozen in his hand, ancient Chinese rural drama, no vocals",
  title="他擋門說她是許家的人，宮裡太監卻跪在冷面老婆面前",
  description="阿令把木簪放進許硯掌心，他又按回她手心：「妳哪裡都不去。」一早，當初收錢要抓阿令的胡縣令捧著禮籃來給解元請安，被村民笑著送出門，小禾還追出去塞給他一隻雞。下午，許硯從木盒裡拿出當初那張配婚令：「打了，就是造反。」日落，馬蹄聲像悶雷，上百支火把把許家小院圍成一圈。禁軍統領要「貴人」出來，許硯一個人走到門口，舉起配婚令：「她是我許家的人。」秦霜的方陣在他身後站定，六十根長棍同時頓地，統領看了一眼，抬手讓手下收刀。這時，捧著月白宮裝的老太監越過許硯，撲通跪在阿令面前，身後整圈禁軍齊齊單膝落地：「長公主殿下，奴才找您找得好苦。」許硯手裡的配婚令停在半空。《種田娶妻打天下》第 60 集，第一季完。",
  thumb={"headline": "長公主\n殿下", "tag": "種田娶妻打天下", "shot": "s39"})
