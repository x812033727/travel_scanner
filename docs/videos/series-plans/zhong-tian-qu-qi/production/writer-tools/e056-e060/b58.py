import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from ztlib import *

chars = [ch("xuyan"), ch("lengtie"), ch("qinshuang"), ch("aling"), ch("tangxiaotang"), ch("erniu"), ch("xitong")]
e = Ep(58, chars)
S = e.shot
LEVER = "At the head of the Liuxi village lane that runs down to the granary at night, a narrow dirt lane between mud-brick walls ending at the granary door, a tall wooden gate lever of the water race standing at the lane mouth, cold moonlight and torchlight"
FLOODL = "In the Liuxi village lane before the granary at night, a narrow lane between mud-brick walls running down to the open granary door, fast brown water surging along it knee-deep, cold moonlight and torchlight on the water"
WHEEL = "At the big wooden water wheel beside the deep pool above Liuxi village at night, the wheel of twelve paddle boards with bamboo scoops on its rim standing in its stone race, a wooden gate board in the race, black-green water, mossy boulders, an old willow leaning over the pool, cold moonlight"
GRAN = "Outside the Liuxi village granary at night, a low timber barn with mud-plastered walls, its heavy plank door open on grain sacks stacked to the beams inside, dry straw heaped against the wall, cold moonlight and torchlight"
WETG = "Outside the Liuxi village granary at night, a low timber barn with mud-plastered walls and its heavy plank door open on grain sacks stacked inside, shin-deep brown water swirling across the ground before the door, drifting white steam, cold moonlight and lantern light"
INSIDE = "Inside the Liuxi village granary at night, a low timber barn with grain sacks stacked to the beams and woven baskets along the walls, straw on the packed earth floor, a single candle burning on an upturned basket, the plank door open to the dark"
QIN = "Qin Shuang in her fitted dark brown cotton short jacket and wide leather belt, her high ponytail tied with black cord"
LT = "Leng Tie in his soaked deep purple palace eunuch's robe"
KEEP = "the torchlight and deep blue night stay unchanged"
CANDLE = "the warm candlelight stays unchanged"

# ── 閘把 ──
S("s", "Close-up, locked", LEVER,
  "close-up of Xu Yan's face on screen left at the lane mouth, sweat and lime dust on his skin, his eyes hard and level on Leng Tie off screen right, the dark lever post just behind his shoulder",
  f"his eyes stay on Leng Tie while his right shoulder turns a fraction toward the post; {KEEP}",
  ["xuyan"], [("xuyan", "都不選。", "一字一字")], chapter="閘把",
  zh="【鉤子1／開頭】接第 57 集：許硯特寫在左、巷口，臉上是汗和石灰粉，眼神硬而平地盯著畫外右邊的冷鐵，暗色的閘把木柱就在他肩後；眼睛不離冷鐵，右肩往木柱微微一轉")
S("s", "Insert of the hand on the lever, locked", LEVER,
  "insert of a young man's hand in a faded blue-grey sleeve reaching back and closing round the worn wooden bar of the tall gate lever, the lane and torchlight blurred beyond",
  f"the hand grips the bar and wrenches it down hard in one move, the wood creaking; {KEEP}",
  [], action=1,
  zh="插鏡：一隻青灰舊袖的手往後一伸，握住高高閘把那根磨亮的木桿，後面糊開的是巷子和火光；手一握、猛地往下扳，木頭吱嘎一聲（無台詞）")
S("s", "Wide shot, locked", WHEEL,
  "wide shot of the water wheel in the moonlight: the wooden gate board in the race jerking up out of the water, black water pouring through the gap into the race, the big wheel lurching and spinning faster and faster, its bamboo scoops flinging silver water",
  f"the gate board flies up, the water floods the race and the wheel picks up speed with a deep groan; {NIGHT}",
  [], action=3,
  zh="水車全景、月光下：水道裡的木閘板猛地從水裡抽起來，黑水從缺口灌進水道，大水車一頓、越轉越快，竹筒甩出一串串銀色的水；閘板飛起，水灌滿水道，水車低吼著加速（無台詞）")
S("s", "Medium close-up, locked", GRAN,
  f"medium close-up of {LT} in the granary doorway on screen right, the torch still raised over the grain sacks, his head snapping round toward the roar coming down the lane",
  f"his eyes widen and the torch hand hesitates in the air; {KEEP}",
  ["lengtie"], [("lengtie", "什麼聲音？", "一愣，聲音發緊")],
  zh="冷鐵中近景在右、糧倉門口，火把還舉在糧袋上，頭猛地轉向畫外左邊的巷子；眼睛一睜，舉火把的手停在半空")
S("s", "Wide shot, slow push in", FLOODL,
  "wide shot down the lane: a wall of brown water as high as a man's knees roaring down between the walls toward the granary door on screen right, Xu Yan on screen left pressing A-ling flat against the mud-brick wall with one arm",
  f"the water thunders past them, spray flying off the walls, and races on toward the door; {KEEP}",
  ["xuyan", "aling"], action=3,
  zh="奇觀：巷子往下看的全景，一道及膝高的濁水牆在兩牆之間轟隆衝向右邊的糧倉門口，許硯在左用一隻手臂把阿令壓在泥磚牆上；水從他們身邊衝過，牆上濺起水花，一路衝向倉門（無台詞）")
S("s", "Medium shot, locked", WETG,
  f"medium shot of {LT} in the granary doorway on screen right as the surge hits his legs, his feet sliding out from under him, the torch flying out of his hand",
  f"the water knocks his legs sideways, he flails and the torch spins away over the water; {KEEP}",
  ["lengtie"], action=2,
  zh="冷鐵在右、糧倉門口，濁水撞上他的腿，腳底一滑，火把從手裡飛出去；水把他的腿掃歪，他手亂揮，火把在水面上翻著飛走（無台詞）")
S("s", "Insert of the torch hitting the water, locked", WETG,
  "insert of a burning torch slapping down onto the swirling brown water before the granary door, the flame dying with a hiss in a burst of white steam",
  f"the torch hits, the flame snuffs out and a thick puff of white steam rolls up; {KEEP}",
  [], action=2,
  zh="奇觀：插鏡，一支燒著的火把啪地落在糧倉門前打轉的濁水上，火「嗤」地熄滅，冒起一大團白煙；火把一落、火一滅，白煙滾上來（無台詞）")
S("s", "Two-shot, locked", WETG,
  f"two-shot in the doorway: Xu Yan on screen left lunging in and catching the dagger wrist of {LT} on screen right with both hands, the short blade slicing Xu Yan's sleeve open along the left forearm",
  f"the blade rips the cloth, Xu Yan grits his teeth and twists the wrist back against the door post; {KEEP}",
  ["xuyan", "lengtie"], [("xuyan", "放手！", "咬牙")],
  zh="門口雙人鏡：許硯在左撲上去，雙手扣住右邊冷鐵拿短刀的手腕，刀刃把許硯的袖子沿著左前臂劃開（只拍裂開的袖子）；布一裂，許硯咬牙把那隻手腕往門柱上扭")
S("s", "Insert of the spear pinning the sleeve, locked", WETG,
  "insert of a red-tasselled spear streaking in from screen left and driving through a soaked deep purple sleeve into the wooden door post, pinning the arm flat",
  f"the spearhead thuds into the post, the red tassel whips and the pinned arm jerks once and stops; {KEEP}",
  [], action=1,
  zh="開場爽點：插鏡，一桿紅纓槍從左邊破空而來，穿過濕透的深紫袖子釘進木門柱，把那隻手臂釘死；槍頭「篤」地釘進柱子，紅纓一甩，被釘住的手臂一抽、不動了（無台詞）")
S("s", "Medium close-up, locked", WETG,
  f"medium close-up of {QIN} on screen left, soaked to the knees, both hands still on the spear shaft driven into the door post, her fierce eyes on Leng Tie off screen right",
  f"she leans her weight onto the shaft and her lips curl into a cold smile; {KEEP}",
  ["qinshuang"], [("qinshuang", "動一下，", "冷"), ("qinshuang", "試試看。", "嘴角一勾")],
  zh="秦霜中近景在左，水濕到膝蓋，雙手還握著釘進門柱的槍桿，狠狠的眼睛看畫外右邊的冷鐵；把重心壓上槍桿，嘴角勾起一個冷笑")
S("s", "Close-up, slow push in", WETG,
  "close-up of A-ling's face on screen left, a short dagger held level in her hand near the bottom of the frame, its point toward Leng Tie off screen right, her phoenix eyes ice-cold",
  f"she presses the blade one inch forward and her eyes do not move; {KEEP}",
  ["aling"], [("aling", "你答錯的，", "很輕"), ("aling", "不只一題。", "冷")],
  zh="阿令特寫在左，一把短匕平握在畫面下緣，刀尖朝著畫外右邊的冷鐵，鳳眼冷得像冰；刀往前一寸，眼睛一動不動")
S("s", "Close-up, locked", WETG,
  f"close-up of {LT} on screen right, his arm pinned to the door post, a dagger point at the edge of the frame under his jaw, his narrow eyes on Aling off screen left",
  f"he lifts his chin away from the blade and a thin smile cuts across his face; {KEEP}",
  ["lengtie"], [("lengtie", "好一個……", "冰冷"), ("lengtie", "不說話的女人。", "冷笑")],
  zh="冷鐵特寫在右，手臂被釘在門柱上，畫邊一把刀尖抵在他下巴下，細眼看畫外左邊的阿令；下巴往後一抬避開刀，臉上劃過一個薄薄的笑")
S("s", "Wide shot, locked", FLOODL,
  "wide shot of the lane: Wang Erniu and a dozen village youths hauling six soaked black-clad assassins up out of the water and binding their wrists with hemp rope against the wall",
  f"the youths yank the men up and loop the ropes tight; {KEEP}",
  ["erniu"], [("erniu", "綁起來！", "吼"), ("erniu", "一個都別跑！", "大嗓門")],
  zh="中段前爽點：巷子全景，王二牛和十幾個少年把六個濕透的黑衣刺客從水裡拖起來，靠著牆用麻繩綁手；少年把人拽起來、繩子一勒，二牛把最後一個結拉緊")

# ── 令牌 ──
S("s", "Wide shot, slow pan right", WETG,
  "wide shot of the granary doorway: villagers in rough brown and grey clothes lifting the bottom sacks up out of the wet, Wang Erniu on screen right slapping the top of the tall dry pile of grain sacks inside the door with a huge grin",
  f"he pats the sacks twice and turns round grinning; {KEEP}",
  ["erniu"], [("erniu", "一袋都沒少！", "大笑")], chapter="令牌",
  zh="糧倉門口全景：穿粗布衣的村民把最底下的麻袋從水裡抬起來，王二牛在右拍著門裡高高一堆乾的糧袋，笑得合不攏嘴；拍兩下、轉身大笑（糧倉保住）")
S("s", "Medium shot, locked", WETG,
  f"medium shot of {TANG} on screen left by the granary door, lime dust still on her sleeves, pointing with a teasing smile at Xu Yan's slashed sleeve beyond the frame",
  f"she wags her pointing finger and bites back a laugh; {KEEP}",
  ["tangxiaotang"], [("tangxiaotang", "村裡沒人受傷，", "笑"), ("tangxiaotang", "就你一個。", "調侃")],
  zh="唐小棠在左、糧倉門旁，袖子上還有石灰，笑著指向畫外許硯被劃開的袖子；手指搖一搖，憋著笑（村民沒有一人受傷）")
S("s", "Medium shot, locked", WETG,
  f"medium shot of Xu Yan wading up on screen left to the pinned {LT} on screen right, one hand clamped over his slashed sleeve, a paper lantern held up in the other",
  f"he holds the lantern up to Leng Tie's face; {KEEP}",
  ["xuyan", "lengtie"], [("xuyan", "誰派你來的？", "喘著，冷")],
  zh="許硯在左，涉水走到右邊被釘住的冷鐵面前，一手按著被劃開的袖子，另一手舉起紙燈籠；把燈籠舉到冷鐵臉前")
S("s", "Close-up, locked", WETG,
  "close-up of Leng Tie's pale face on screen right in the lantern light, water dripping from his black gauze hat, a mocking smile, his eyes on Xu Yan off screen left",
  f"he tilts his head and the smile widens; {KEEP}",
  ["lengtie"], [("lengtie", "宮裡。", "陰柔，嘲弄")],
  zh="冷鐵的白臉特寫在右、燈籠光裡，水從黑紗帽上滴下來，嘲弄地笑，看畫外左邊的許硯；頭一歪，笑得更開")
S("s", "Medium close-up, locked", WETG,
  f"medium close-up of {QIN} on screen left holding up a short black-gripped dagger between two fingers, her brows raised in contempt, her eyes on Leng Tie off screen right",
  f"she twirls the dagger once and tosses it into the water; {KEEP}",
  ["qinshuang"], [("qinshuang", "宮裡的公公，", "冷笑"), ("qinshuang", "袖子裡藏刀？", "不屑")],
  zh="秦霜中近景在左，兩根手指夾著一把黑柄短刀舉起來（從冷鐵袖子裡搜的），眉毛一挑、一臉不屑，看畫外右邊的冷鐵；刀在指間一轉，丟進水裡")
S("s", "Medium shot, locked", WETG,
  f"medium shot of {QIN} kneeling in the shallow water on screen left, gripping Leng Tie's black leather boot by the heel and wrenching it off his foot",
  f"she braces her knee and drags the boot off in one hard pull, water pouring out of it; {KEEP}",
  ["qinshuang"], [("qinshuang", "靴子裡，", "察覺"), ("qinshuang", "有東西。", "篤定")],
  zh="秦霜在左、跪在淺水裡，抓住冷鐵黑皮靴的靴跟，一把把靴子扯下來；膝蓋一頂、猛一拽，靴子裡的水嘩地倒出來")
S("s", "Insert of the boot and the token, locked", WETG,
  "insert in the lantern light of a black leather boot held sole-up in a woman's hands in a black sleeve, a neat row of iron studs hammered into the sole in a cloud-scroll pattern, a small dark iron token sliding out of the boot shaft into her palm",
  f"she tips the boot, the studs glint and the token slides out and drops into her palm with a clink; {KEEP}",
  [], action=2,
  zh="【中段鉤子／第二季伏筆】插鏡、燈籠光下：一隻黑袖的手把黑皮靴靴底朝上捧著，靴底整整齊齊一排雲紋鐵釘（跟第 57 集水裡那隻一樣），一塊小小的黑鐵令牌從靴筒裡滑出來掉進她掌心；靴子一斜，鐵釘一閃，令牌「叮」地落進手心（無台詞、沒有人提鐵釘）")
S("s", "Insert of the token in his palm, locked", WETG,
  "insert of a small dark iron token the size of a palm lying in a young man's palm under the lantern, one deep-carved emblem on its face, his thumb turning it over to show a raised square seal on the back; Xu Yan speaks off screen",
  f"the thumb rubs the carved face once and flips the token over onto its seal; {KEEP}",
  [], [("xuyan", "魏。", "畫外，低聲唸"), ("xuyan", "背面，", "畫外，翻過來"), ("xuyan", "相府的印。", "畫外，聲音一沉")],
  zh="中段揭密：插鏡，燈籠下一隻年輕男人的手掌心躺著一塊巴掌大的黑鐵令牌，正面一個深刻的記號（不寫字），拇指把它翻過來，背面是一方凸起的方印；拇指摸一下正面、翻到印的那面（許硯畫外唸出「魏」與「相府的印」）")
S("s", "Medium close-up, slow push in", WETG,
  f"medium close-up of {TANG} on screen right hurrying up with a lantern, lime dust still on her pink sleeves, her face sharp and grim, her eyes on Xu Yan off screen left",
  f"she stops beside him and lowers the lantern; {KEEP}",
  ["tangxiaotang"], [("tangxiaotang", "魏少卿回京，", "咬牙"), ("tangxiaotang", "告訴了他爹。", "冷")],
  zh="唐小棠中近景在右，提著燈籠快步走來，粉袖上還有石灰，臉又尖又沉，看畫外左邊的許硯；在他身邊停下，放低燈籠（s01-t12 收：魏少卿回京把阿令的下落告訴了宰相）")
S("s", "Group shot, locked", WETG,
  f"group shot before the granary door: Wang Erniu on screen left with a coil of rope over his shoulder, his honest face screwed up in confusion, {TANG} in the middle with her lantern, {QIN} on screen right with one hand on the spear still pinning Leng Tie to the post",
  f"Erniu scratches the back of his head and looks from one woman to the other; {KEEP}",
  ["erniu", "tangxiaotang", "qinshuang"], [("erniu", "相府？", "一臉茫然"), ("erniu", "那是多大的官？", "小聲")],
  zh="倉門前三人鏡：王二牛在左、肩上一捆繩子，老實的臉皺成一團，中間是提燈籠的唐小棠，右邊的秦霜一手還按著釘住冷鐵的槍；二牛抓抓後腦勺，看看這個、看看那個（喜劇）")
S("s", "Close-up, locked", WETG,
  f"close-up of {TANG} on screen right, the lantern under her chin, her big round eyes flat and serious, her eyes on Wang Erniu off screen left",
  f"she holds up one finger; {KEEP}",
  ["tangxiaotang"], [("tangxiaotang", "最大的。", "一字一字")],
  zh="唐小棠特寫在右，燈籠在下巴下，大圓眼睛又平又正經，看畫外左邊的王二牛；豎起一根手指")
S("s", "Medium close-up, locked", WETG,
  "medium close-up of Xu Yan on screen left turning the iron token in his fingers, his brows drawn down, his eyes on Leng Tie off screen right",
  f"he closes his fist round the token; {KEEP}",
  ["xuyan"], [("xuyan", "扮成宮裡的人來殺，", "想通了"), ("xuyan", "再推給宮裡。", "冷")],
  zh="許硯中近景在左，手指轉著鐵令牌，眉頭壓低，看畫外右邊的冷鐵；拳頭把令牌一握")
S("s", "Close-up, locked", WETG,
  f"close-up of {LT} on screen right, still pinned to the post, giving a small mocking nod, his eyes on Xu Yan off screen left",
  f"he dips his chin once in a mock bow; {KEEP}",
  ["lengtie"], [("lengtie", "解元公，", "冰冷"), ("lengtie", "聰明。", "嘲弄")],
  zh="冷鐵特寫在右，還被釘在柱上，嘲弄地輕輕點一下頭，看畫外左邊的許硯；下巴一點，像假裝行禮")
S("s", "Close-up, slow push in", WETG,
  "close-up of A-ling's face on screen right in the lantern light, the wooden hairpin in her hair, her eyes lowered to the iron token below the frame",
  f"her lashes lift and her voice comes out very quiet; {KEEP}",
  ["aling"], [("aling", "宰相，", "很輕"), ("aling", "要我死。", "平靜得可怕")],
  zh="阿令特寫在右、燈籠光裡，木簪挽髮，眼睛垂著看畫外左邊許硯拳頭裡的令牌；睫毛一抬，聲音很輕")
S("s", "Two-shot, locked", WETG,
  "two-shot before the granary door: Xu Yan on screen left turning to A-ling on screen right, the token still in his fist, water swirling round their shins",
  f"he steps closer to her and squares his shoulders between her and the lane; {KEEP}",
  ["xuyan", "aling"], [("xuyan", "那他得先，", "很穩"), ("xuyan", "過許家這關。", "篤定")],
  zh="倉門前雙人鏡：許硯在左轉向右邊的阿令，令牌還握在拳頭裡，水在小腿邊打轉；他往她靠一步，肩膀一挺，擋在她和巷子之間")

# ── 包紮 ──
S("s", "Medium close-up, locked", WETG,
  f"medium close-up of {QIN} on screen left wrenching her spear out of the door post, her eyes on Xu Yan off screen right",
  f"she yanks the spear free and swings it up onto her shoulder; {KEEP}",
  ["qinshuang"], [("qinshuang", "今晚，", "利落"), ("qinshuang", "我守村口。", "篤定")],
  zh="秦霜中近景在左，把槍從門柱上拔出來，看畫外右邊的許硯；一把拔出、甩上肩")
S("s", "Close-up, locked", WETG,
  f"close-up of {TANG} on screen right, the lantern in one hand, the small gold abacus in the other, her eyes on Xu Yan off screen left",
  f"she flicks one bead across with her thumb; {KEEP}",
  ["tangxiaotang"], [("tangxiaotang", "鏢局的人，", "精明"), ("tangxiaotang", "我連夜調回來。", "篤定")],
  zh="唐小棠特寫在右，一手燈籠、一手小金算盤，看畫外左邊的許硯；拇指撥過一顆珠子")
S("s", "Wide shot, locked", INSIDE,
  "wide shot of the quiet granary interior by the candle: Xu Yan sitting on a grain sack on screen left holding out his left arm with the sleeve slashed open, A-ling kneeling beside him on screen right with a strip of clean white cloth, the stacked sacks rising to the beams around them",
  f"he tries to pull his arm back and she catches his wrist and pulls it back to her; {CANDLE}",
  ["xuyan", "aling"], [("xuyan", "小傷，", "不好意思"), ("xuyan", "我自己來——", "想縮手")], chapter="包紮",
  zh="糧倉裡安靜的全景、燭光旁：許硯在左坐在糧袋上，伸著袖子被劃開的左臂，阿令在右跪在他身邊，手上一條乾淨的白布；他想把手縮回去，她扣住他的手腕拉回來")
S("s", "Close-up, slow push in", INSIDE,
  "close-up of A-ling's face on screen right, head bowed over the bandage, the candlelight warm on her long lashes and porcelain skin, a loose strand of black hair at her cheek",
  f"her eyes stay down on her work as she winds the cloth round once; {CANDLE}",
  ["aling"], [("aling", "別動。", "很輕，不抬頭")],
  zh="顏值鏡頭：阿令特寫在右，低頭包紮，燭光暖暖地落在她的長睫毛和瓷白的皮膚上，一縷黑髮垂在頰邊；眼睛一直看著手上，白布繞一圈")
S("s", "Insert of her thumb on his palm, locked", INSIDE,
  "insert in the candlelight of a young man's open palm resting on a grain sack, thick farmer's calluses across it and dried mud in the creases, a slender thumb in a grey-white sleeve slowly brushing across the calluses",
  f"the thumb moves slowly across the hard skin and stops; {CANDLE}",
  [], action=2,
  zh="【第二季伏筆】插鏡、燭光下：一隻年輕男人攤開的手掌放在糧袋上，掌心一層厚厚的種田繭、紋路裡卡著乾泥，一根灰白袖子的纖細拇指慢慢撫過那些繭；拇指慢慢滑過硬皮、停住（無台詞）")
S("s", "Extreme close-up, locked", INSIDE,
  "extreme close-up of A-ling's lips and lowered lashes in the candlelight, her face very still",
  f"her lips barely move; {CANDLE}",
  ["aling"], [("aling", "原來是真的。", "自言自語，幾乎聽不見")],
  zh="【第二季伏筆】阿令的唇與垂下的睫毛大特寫、燭光裡，臉一動不動；嘴唇幾乎沒動")
S("s", "Close-up, locked", INSIDE,
  "close-up of Xu Yan's face on screen left in the candlelight, his eyebrows lifting in surprise, his eyes on Aling off screen right",
  f"he leans down a little to catch her eye; {CANDLE}",
  ["xuyan"], [("xuyan", "什麼是真的？", "愣住")],
  zh="許硯特寫在左、燭光裡，眉毛一挑、意外，看畫外右邊的阿令；身子往下一點想對上她的眼睛")
S("s", "Two-shot, locked", INSIDE,
  "two-shot by the candle: A-ling on screen right pulling the knot of the bandage tight with one sharp tug, Xu Yan on screen left wincing with his teeth gritted",
  f"she yanks the knot, he flinches, and the corner of her mouth lifts very slightly; {CANDLE}",
  ["aling", "xuyan"], [("aling", "別動。", "淡淡地，沒回答"), ("xuyan", "嘶……輕點。", "齜牙咧嘴")],
  zh="燭光雙人鏡：阿令在右猛一拉把繃帶的結綁緊，許硯在左齜牙咧嘴；她一拉，他一縮，她的嘴角極輕地往上一動（她沒有回答那個問題）")
S("s", "Close-up, locked", INSIDE,
  "close-up of Xu Yan's face on screen centre in the candlelight, his eyes lifting to a point in the empty air in front of him, a slow surprised smile; the system voice speaks off screen",
  f"his eyes track across the empty air as if reading and the smile grows; {CANDLE}",
  ["xuyan"], [("xitong", "阿令好感，", "平板電子音，叮一聲"), ("xitong", "六十四。", "平板電子音")],
  zh="系統面板：許硯的臉在中間、燭光裡，眼睛抬起看著面前的空中，慢慢意外地笑開；眼睛像讀字一樣掃過空中，笑容變大",
  panel=[{"text": "阿令 好感 +3 → 64", "kind": "affection"}])

# ── 明天 ──
S("s", "Close-up, locked", INSIDE,
  "close-up of Xu Yan's face on screen left in the candlelight, a wry lopsided grin, his eyes on Aling off screen right",
  f"he lifts his bandaged arm a little to show it off; {CANDLE}",
  ["xuyan"], [("xuyan", "擋了一整晚，", "小聲嘀咕"), ("xuyan", "才三分？", "委屈")],
  zh="許硯特寫在左、燭光裡，歪著嘴笑，看畫外右邊的阿令；把包好的手臂抬一點給她看")
S("s", "Close-up, slow push in", INSIDE,
  "close-up of A-ling's face on screen right in the candlelight, one eyebrow lifting a fraction, her lips pressed against a smile, her eyes on Xu Yan off screen left",
  f"she tilts her head a little and waits; {CANDLE}",
  ["aling"], [("aling", "嫌少？", "淡淡地")],
  zh="阿令特寫在右、燭光裡，一邊眉毛抬一點，嘴唇抿著不讓自己笑，看畫外左邊的許硯；頭微微一歪，等他回答")
S("s", "Medium shot, locked", INSIDE,
  "medium shot of Xu Yan on a grain sack on screen left shaking his head fast with both hands raised, A-ling kneeling beside him on screen right turning away to hide a smile",
  f"he waves both hands and she turns her face toward the candle; {CANDLE}",
  ["xuyan", "aling"], [("xuyan", "不嫌，", "連忙"), ("xuyan", "不嫌。", "笑")],
  zh="許硯在左坐在糧袋上，雙手舉起拚命搖頭，右邊跪著的阿令轉過臉藏笑；他兩手一揮，她把臉轉向燭光")
S("s", "Wide shot, locked", FLOODL,
  f"wide shot of the lane as the water drains away: {LT} with his wrists bound behind him being marched up the lane by Wang Erniu and two youths with staffs, Xu Yan and A-ling standing by the granary door on screen right",
  f"they march him three steps and he suddenly plants his feet and stops; {KEEP}",
  ["lengtie", "erniu"], chapter="明天", action=3,
  zh="水退下去的巷子全景：雙手反綁的冷鐵被王二牛和兩個拿棍的少年押著往巷子上走，許硯與阿令站在右邊糧倉門口；押了三步，他突然兩腳一站、停住（無台詞）")
S("s", "Medium shot, slow push in", FLOODL,
  f"medium shot of {LT} on screen left with his hands bound, twisting round to look back at Xu Yan off screen right, Wang Erniu's big hand on his shoulder",
  f"he throws his head back and lets out a short cold laugh; {KEEP}",
  ["lengtie", "erniu"], [("lengtie", "相爺……", "回頭，大笑"), ("lengtie", "晚了一步。", "笑意冰冷")],
  zh="【結尾】冷鐵在左、雙手被綁，扭過身回頭看畫外右邊的許硯，王二牛的大手按在他肩上；他仰頭冷冷笑一聲")
S("s", "Close-up, locked", FLOODL,
  "close-up of Xu Yan's face on screen right by the granary door, his brows snapping together, his eyes on Leng Tie off screen left",
  f"he takes one step forward; {KEEP}",
  ["xuyan"], [("xuyan", "什麼意思？", "沉聲")],
  zh="【結尾】許硯特寫在右、糧倉門口，眉頭一下子擰緊，看畫外左邊的冷鐵；往前一步")
S("s", "Close-up, slow push in", FLOODL,
  "close-up of Leng Tie's pale face on screen left in the moonlight, water dripping from his jaw, a knowing smile, his narrow eyes sliding past Xu Yan toward Aling off screen right",
  f"the smile deepens as if he knows the hour already; {KEEP}",
  ["lengtie"], [("lengtie", "宮裡真的人，", "一字一頓"), ("lengtie", "後天就到。", "笑")],
  zh="【結尾／第二季伏筆】冷鐵的白臉特寫在左、月光裡，水從下巴滴下，一個什麼都知道的笑，細眼越過許硯滑向畫外右邊的阿令；笑得更深，像早就知道是哪個時辰")
S("s", "Close-up, locked", WETG,
  "close-up of A-ling's face on screen right by the granary door, the moonlight on her porcelain skin, her phoenix eyes going wide for the first time, the leftover strip of white cloth crushed in her hand at the bottom of the frame",
  f"her fingers crush the cloth and her eyes lift slowly toward the dark road beyond the village; {KEEP}",
  ["aling"], action=2,
  zh="【結尾】最後一格：阿令特寫在右、糧倉門口，月光落在瓷白的臉上，鳳眼第一次睜大，畫面下緣手裡捏著剩下的白布條；手指把布捏皺，眼睛慢慢抬向村外黑暗的路（無台詞）")

e.write(
  music="a heavy wooden creak and a deep surging roar of low strings and timpani as the lever is thrown and the water wheel spins up, a rushing torrent of strings and taiko as the water fills the lane, a sharp hiss and a single bright gong when the torch dies, a fast fierce pipa and frame drum for the spear and the blade, a tense low guqin and a ticking woodblock while the iron token is read, a bright comic plucked phrase for the big lad's question, then a warm intimate guzheng and soft xiao melody by candlelight for the bandage and her whisper, a twinkling chime for the system, and finally a cold laughing low reed and a single deep drum hit that stops on the woman's widened eyes, ancient Chinese rural drama, no vocals",
  title="刺客要燒全村的糧，他一拉水車閘門，整條渠衝了過來",
  description="冷鐵把火把舉到糧堆上：交出她，不然燒光全村的糧。許硯盯著他說：「都不選。」反手扳下身後水車的閘把。水車越轉越快，渠水像一堵牆衝進糧倉前的窄巷，冷鐵腳下一滑，火把落進水裡「嗤」地熄滅；秦霜一槍釘住他的袖子，阿令的短匕抵上他的喉嚨。從冷鐵靴筒裡搜出一塊令牌，正面刻著「魏」，背面是相府的印——魏少卿回京把阿令的下落告訴了他爹，宰相派人扮成宮人來殺，再推給宮裡。糧倉一袋都沒少。燭光下，阿令一言不發地替許硯包紮手臂：「別動。」冷鐵被押走前回頭大笑：「相爺晚了一步，宮裡真的人，後天就到。」《種田娶妻打天下》第 58 集。",
  thumb={"headline": "都不選", "tag": "種田娶妻打天下", "shot": "s01"})
