import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from ztlib import *

chars = [ch("xuyan"), ch("aling"), ch("lengtie"), ch("qinshuang"), ch("tangxiaotang"), ch("erniu"), ch("xitong")]
e = Ep(57, chars)
S = e.shot
GATE = "At the village entrance at nightfall, an old willow tree, a wooden plank bridge over the thin stream, a dusty track, the village's rough timber gate with a heavy wooden crossbar and a low log lookout platform above it, torches burning on poles, thatched roofs beyond, a deep blue sky with the last red line on the horizon"
LANE = "In a Liuxi village lane at night, a narrow dirt lane between mud-brick walls and low thatched eaves, a side passage opening off it, torches and cold moonlight"
FLOOD = "In a Liuxi village lane at night, a narrow lane between mud-brick walls and low thatched eaves flooded knee-deep with fast brown water, a side passage opening off it, cold moonlight on the water"
HEAD = "At the head of the irrigation channel above Liuxi village at night, the channel running down toward the thatched roofs, raw earth banks, a heavy wooden sluice board in a stone slot, cold moonlight and the orange glow of torches from the village below"
GRAN = "Outside the Liuxi village granary at night, a low timber barn with mud-plastered walls, its heavy plank door kicked open on grain sacks stacked to the beams inside, dry straw heaped against the wall, a dirt path along the back of the village, cold moonlight and torchlight"
LEVER = "At the head of the Liuxi village lane that runs down to the granary at night, a narrow dirt lane between mud-brick walls ending at the granary door, a tall wooden gate lever of the water race standing at the lane mouth, cold moonlight and torchlight"
QIN = "Qin Shuang in her fitted dark brown cotton short jacket and wide leather belt, her high ponytail tied with black cord"
LT = "Leng Tie in his deep purple palace eunuch's robe and black gauze hat"
KEEP = "the torchlight and deep blue night stay unchanged"

# ── 御膳房 ──
S("s01", "Wide shot, locked", GATE,
  f"wide shot of the open ground between the gate and the bridge: the thirty horsemen in purple and crimson livery on screen right with their swords half drawn, the block of village youths with lowered staffs behind the gate on screen left, A-ling in her plain grey-white dress walking out alone past Xu Yan into the torchlit gap between them",
  f"she walks past Xu Yan with slow even steps, her sleeve brushing his arm, and stops in the middle of the gap; {KEEP}",
  ["aling", "xuyan"], chapter="御膳房", action=3,
  zh="【鉤子1／開頭】接第 56 集：柵門與木橋之間的空地全景，右邊三十騎紫紅宮服、刀出鞘一半，左邊柵門後少年放低長棍；灰白衣裙的阿令獨自越過許硯，走進兩邊中間火光照著的空地；她步子慢而穩，袖子擦過他的手臂，停在正中間（無台詞）")
S("s02", "Medium close-up, slow push in", GATE,
  "medium close-up of A-ling on screen left standing between torchlight and darkness, one side of her moon-white face lit orange and the other in deep blue shadow, the wooden hairpin in her black hair, her phoenix eyes lifting coldly to Leng Tie off screen right",
  f"she lifts her chin and folds her hands at her sash; {KEEP}",
  ["aling"], [("aling", "公公。", "冷，很輕")],
  zh="顏值鏡頭：阿令中近景在左，站在火光與黑暗之間，月白的臉一半被火照成橘色、一半在深藍的影子裡，木簪挽髮，鳳眼冷冷抬起看畫外右邊的冷鐵；下巴一抬，雙手交疊在腰帶上")
S("s03", "Close-up, locked", GATE,
  "close-up of A-ling's face on screen left, her cold phoenix eyes dead level on Leng Tie off screen right, the torchlight flickering on one cheek",
  f"her lips barely move and her gaze never leaves him; {KEEP}",
  ["aling"], [("aling", "御膳房初一，", "一字一字"), ("aling", "煮什麼？", "冷")],
  zh="【鉤子1】阿令特寫在左，冷冷的鳳眼平平盯著畫外右邊的冷鐵，火光在一邊臉頰上跳；嘴唇幾乎不動，眼睛一刻不離")
S("s04", "Close-up, locked", GATE,
  f"close-up of {LT} on screen right, his pale face frozen in a thin courtly smile, his narrow eyes flickering once toward Aling off screen left",
  f"the smile stays fixed while his eyes dart down and back up; {KEEP}",
  ["lengtie"], [("lengtie", "貴人考咱家？", "尖細，乾笑")],
  zh="冷鐵特寫在右，深紫宮服、黑紗宮帽，白臉上僵著一個薄薄的宮裡式微笑，細眼往畫外左邊的阿令一閃；笑容不動，眼睛往下一飄又抬回來")
S("s05", "Medium close-up, locked", GATE,
  f"medium close-up of {LT} on screen right, the white horsetail whisk across his arm, his chin lifted with put-on confidence, his eyes on Aling off screen left",
  f"he flicks the whisk lightly over his sleeve; {KEEP}",
  ["lengtie"], [("lengtie", "初一嘛，", "拿腔拿調"), ("lengtie", "八寶鴨。", "得意")],
  zh="冷鐵中近景在右，白拂塵搭在臂上，下巴抬起、裝得很篤定，看著畫外左邊的阿令；拂塵在袖子上輕輕一甩")
S("s06", "Two-shot, locked", GATE,
  f"two-shot behind the timber gate: Xu Yan on screen left and {QIN} on screen right holding her red-tasselled spear, both glancing at each other, the torchlit gap and A-ling's back beyond them",
  f"Qin Shuang's hand slides down the spear shaft into a fighting grip; {KEEP}",
  ["xuyan", "qinshuang"], [("qinshuang", "八寶鴨？", "低聲，冷笑")],
  zh="柵門後雙人鏡：許硯在左、握紅纓槍的秦霜在右，兩人對看一眼，後面是火光照著的空地和阿令的背影；秦霜的手沿著槍桿滑下，換成出手的握法")
S("s07", "Close-up, slow push in", GATE,
  "close-up of A-ling's face on screen left, her phoenix eyes narrowing to ice, her lips pressed thin, her eyes on Leng Tie off screen right",
  f"her eyes narrow further and her voice drops; {KEEP}",
  ["aling"], [("aling", "初一齋戒，", "冷"), ("aling", "御膳房不見葷。", "一字一字")],
  zh="阿令特寫在左，鳳眼瞇成冰，唇抿緊，冷鐵在畫外右邊；眼睛再瞇一點，聲音往下沉")
S("s08", "Extreme close-up, locked", GATE,
  "extreme close-up of A-ling's eyes and the bridge of her nose in the torchlight, her long lashes still, her gaze on Leng Tie off screen right",
  f"she does not blink once; {KEEP}",
  ["aling"], [("aling", "假的。", "冷冷地")],
  zh="前半爽點：阿令的眼睛與鼻樑大特寫，火光裡長睫毛一動不動，看著畫外右邊的冷鐵；一下都不眨")
S("s09", "Close-up, locked", GATE,
  f"close-up of {LT} on screen right, the courtly smile dropping off his pale face all at once, his narrow eyes going flat and cold",
  f"his face goes blank and his head tilts a fraction; {KEEP}",
  ["lengtie"], [("lengtie", "可惜了。", "聲音一下子變低、冰冷")],
  zh="冷鐵特寫在右，白臉上的宮裡式笑容一下子全掉了，細眼變得又平又冷；臉一空，頭微微一歪（露餡，聲音從尖細變冰冷）")
S("s09b", "Close-up, locked", GATE,
  "close-up of Xu Yan's face on screen left behind the gate, his eyes snapping wide, his eyes on Leng Tie off screen right",
  f"he lunges forward a step, one hand flying out toward the gap; {KEEP}",
  ["xuyan"], [("xuyan", "阿令，", "急"), ("xuyan", "退後！", "大喊")],
  zh="許硯特寫在左、柵門後，眼睛猛地睜大，看畫外右邊的冷鐵；往前撲一步，一隻手往空地伸出去")
S("s10", "Insert of the dagger sliding from the sleeve, locked", GATE,
  "insert of a deep purple silk sleeve in the torchlight, a short dagger with a black grip sliding out of the cuff into a pale hand; Leng Tie speaks off screen",
  f"the blade slips out and the fingers close round the grip in one smooth move; {KEEP}",
  [], [("lengtie", "一個不留。", "畫外，冰冷")], chapter="出鞘",
  zh="插鏡：火光裡一截深紫綢袖，一把黑柄短刀從袖口滑進一隻白手；刀滑出來、手指一握（冷鐵畫外）")
S("s11", "Wide shot, locked", GATE,
  "wide shot of the bridge: the thirty assassins on screen right ripping off their purple outer robes to black tunics underneath and leaping down from their horses, blades drawn, charging across the plank bridge toward the gate on screen left",
  f"the robes fly, boots hit the planks and the black-clad assassins surge forward in a rush; {KEEP}",
  [], action=3,
  zh="木橋全景：右邊三十個刺客扯掉紫色外袍、底下是黑衣，從馬上跳下來，拔刀衝過木板橋撲向左邊的柵門；外袍飛起，靴子踩上橋板，黑衣人一湧而上（無台詞）")
S("s12", "Medium close-up, low angle, locked", GATE,
  f"medium close-up from a low angle of {QIN} on screen left at the front of the youths, the spear levelled, her eyes blazing toward the charging men beyond the frame",
  f"she drops into a stance and thrusts the spear forward; {KEEP}",
  ["qinshuang"], [("qinshuang", "頂住！", "斷喝")],
  zh="秦霜中近景、低角度在左、少年隊伍最前面，槍放平，眼睛冒火看著畫外右邊衝來的人；她一沉身、把槍往前一送")
S("s13", "Wide shot, slow push in", GATE,
  "wide shot at the gate: the front rank of village youths lowering their long staffs into a bristling hedge, the black-clad assassins crashing into it and being thrown back, staffs cracking against blades in the torchlight",
  f"the hedge of staffs absorbs the charge, bends and shoves the first men back off their feet; {KEEP}",
  [], action=3,
  zh="柵門全景：第一排少年把長棍壓成一道棍牆，黑衣刺客撞上來被頂回去，棍子在火光裡磕在刀上；棍牆吃下這一衝，一彎、一推，把最前面的人推倒（無台詞）")
S("s14", "Medium shot, locked", GATE,
  "medium shot of Wang Erniu in the front rank on screen left, his staff braced crosswise against the blade of one of the assassins, his square face red and straining, his feet dug into the dirt",
  f"he roars and shoves the blade back with his whole weight; {KEEP}",
  ["erniu"], [("erniu", "一步都不許退！", "吼")],
  zh="王二牛在左、第一排，長棍橫著頂住一個刺客的刀，方臉漲紅使勁，兩腳踩進土裡；他大吼一聲，用全身的重量把刀推回去")
S("s15", "Two-shot, locked", GATE,
  f"two-shot behind the front rank: Xu Yan on screen left grabbing A-ling's wrist and pulling her back behind him, {QIN} on screen right turning her head to him",
  f"he pulls A-ling behind his shoulder in one step and jerks his chin toward the village; {KEEP}",
  ["xuyan", "qinshuang", "aling"], [("xuyan", "放他們進村。", "急，壓低聲音")],
  zh="第一排後面的雙人鏡：許硯在左一把抓住阿令的手腕把她拉到身後，右邊的秦霜轉頭看他；他一步把阿令拉到肩後，下巴往村裡一揚")
S("s16", "Medium close-up, locked", GATE,
  f"medium close-up of {QIN} on screen right, her eyes snapping to Xu Yan off screen left and then back to the fight, a fierce grin starting",
  f"she lifts the spear high overhead as a signal; {KEEP}",
  ["qinshuang"], [("qinshuang", "退——", "拉長號令"), ("qinshuang", "進巷！", "斷喝")],
  zh="秦霜中近景在右，眼睛先看畫外左邊的許硯、再回到戰場，嘴角揚起一個狠狠的笑；把槍高高舉起當號令")

# ── 渠水 ──
S("s17", "Wide shot, slow pan left", LANE,
  "wide shot down the lane: the block of village youths stepping back in good order with their staffs still levelled, the black-clad assassins walking in after them between the mud-brick walls, each holding a torch up high in his fist, dark figures visible under each flame, no torch floating on its own",
  f"the youths give ground one step at a time and the assassins follow at a walking pace, torches held up in their fists, coming only a short way down the lane; {KEEP}",
  [], chapter="渠水", action=3,
  zh="村道全景：少年方陣棍還放平、一步一步整齊後退，黑衣刺客跟著走進兩邊泥磚牆之間、每人手裡高舉一支火把；少年一步步讓，刺客用走路的速度跟進一小段（無台詞）")
S("s17b", "Medium close-up, locked", LANE,
  f"medium close-up of {LT} at the back of his men on screen right in the lane, the short dagger in his hand, his cold eyes on the retreating youths beyond the frame",
  f"he jerks the dagger forward to drive his men on; {KEEP}",
  ["lengtie"], [("lengtie", "追！", "冰冷"), ("lengtie", "一個都別放！", "一字一頓")],
  zh="冷鐵中近景在右、村道裡他手下的後面，手握短刀，冷眼盯著前面後退的少年；短刀往前一揮，催手下往前衝")
S("s18", "Medium shot, locked", LANE,
  f"medium shot of {TANG} on top of a mud-brick wall on screen right, a red paper lantern on a long bamboo pole in both hands, the lane below her lit by the torches held up in the assassins' fists",
  f"she hoists the red lantern high over her head and waves it twice; {KEEP}",
  ["tangxiaotang"], [("tangxiaotang", "老人孩子都在祠堂，", "大喊"), ("tangxiaotang", "放水！", "尖聲")],
  zh="高領桃粉襦裙的唐小棠站在右邊的泥磚牆頂上，雙手握著一根長竹竿、頂上一盞紅紙燈籠，下面是村道與刺客手裡舉著的火把；她把紅燈籠高高舉過頭頂揮兩下")
S("s19", "Medium close-up, locked", HEAD,
  "medium close-up of Xu Yan on screen left at the heavy wooden sluice board, both hands on its top beam, his eyes fixed downhill on the red lantern glowing far below among the roofs",
  f"he sets his feet, drags in a breath and heaves the board upward with his whole back; {NIGHT}",
  ["xuyan"], [("xuyan", "開閘！", "咬牙")],
  zh="許硯中近景在左、厚重的木閘板前，雙手扣住板頂的橫木，眼睛看著畫外右邊下方遠遠的紅燈籠；兩腳一站、吸一口氣，用整個背把閘板往上拔")
S("s20", "Insert of the sluice board, locked", HEAD,
  "insert of the heavy wooden sluice board grinding up out of its stone slot, black water bursting out underneath it in a white roaring sheet",
  f"the board lurches up a hand's width and the water explodes through the gap and races away downhill; {NIGHT}",
  [], action=2,
  zh="插鏡：厚木閘板從石槽裡磨著往上抬，底下的黑水一下子衝出來，翻成一片白；閘板一抬一掌寬，水從縫裡炸開往坡下衝（無台詞）")
S("s21", "Wide shot, locked", FLOOD,
  "wide shot of the lane as a knee-deep surge of brown water roars down it between the walls, the black-clad assassins staggering and grabbing at the walls, torches spinning out of their hands",
  f"the water slams into their legs, two men go down and torch after torch drops into the flood; {KEEP}",
  [], action=3,
  zh="奇觀：村道全景，一道及膝的濁水從兩牆之間轟地衝下來，黑衣刺客站不穩、伸手抓牆，火把從手裡甩出去；水撞上他們的腿，兩個人摔倒，火把一支接一支掉進水裡（無台詞）")
S("s22", "Insert of the torches in the water, locked", FLOOD,
  "insert of burning torches falling onto the rushing brown water, each flame hissing out in a puff of white steam",
  f"one torch after another hits the water and dies with a hiss, steam curling up; {KEEP}",
  [], action=2,
  zh="插鏡：燒著的火把掉在湍急的濁水上，火一碰水就「嗤」地熄滅，冒出一團白汽；一支接一支掉下去、熄掉，白汽捲起（無台詞）")
S("s22b", "Medium close-up, slow push in", FLOOD,
  f"medium close-up of {LT} on screen right, the brown water swirling round his legs, the purple robe soaked dark, his eyes narrowing as he looks back over his shoulder",
  f"he glances down at the water, then turns and slips away into the dark side passage behind him; {KEEP}",
  ["lengtie"], [("lengtie", "水？", "一愣"), ("lengtie", "……走後面。", "低聲")],
  zh="冷鐵中近景在右，濁水在他腿邊打轉，紫袍濕成深色，回頭一看、眼睛瞇起；低頭看一眼水，轉身溜進背後漆黑的岔巷（他帶人繞去糧倉）")
S("s23", "Low insert of a boot in the water, locked", FLOOD,
  "low insert at water level of a fallen assassin's black leather boot kicking up out of the brown water, the sole turned to the torchlight showing a neat row of iron studs hammered in a cloud-scroll pattern",
  f"the boot kicks once, the studs glint, and it scrambles back under the water; {KEEP}",
  [], action=1,
  zh="【第二季伏筆】貼水面的低角度插鏡：一個摔倒的刺客，黑皮靴從濁水裡踢起來，靴底轉向火光，上面整整齊齊釘著一排雲紋鐵釘；靴子一踢，鐵釘一閃，又掙扎著沒進水裡（無台詞、沒有人提）")
S("s28", "Medium shot, locked", FLOOD,
  "medium shot of Wang Erniu splashing up the flooded lane on screen right, his staff in one fist, the other arm thrown back pointing behind him, his eyes on Xu Yan off screen left",
  f"he skids to a stop in the water and stabs his finger toward the back of the village; {KEEP}",
  ["erniu"], [("erniu", "糧倉！", "大喊"), ("erniu", "有人繞過去了！", "急")],
  zh="【鉤子／中段鉤子】王二牛在右，從淹水的村道濺著水跑上來，一手抓棍、另一隻手往後指，看畫外左邊的許硯；在水裡煞住，手指往村子後面猛戳")
S("s29", "Wide shot, slow pan right", GRAN,
  "wide shot of the dirt path along the back of the village: six black-clad assassins running hard, each holding a burning torch up high in his fist, dark figures visible under each flame, toward the low timber granary on screen right, the flooded lane glinting far behind them",
  f"they run along the path at a running man's pace, each torch held up in a fist, and the lead man, already near the door, kicks at the plank door; {KEEP}",
  [], action=3,
  zh="【中段鉤子】村子後面的土路全景：六個黑衣刺客、每人手裡高舉一支火把，朝右邊低矮的木造糧倉狂奔，遠遠後面是淹水閃光的村道；他們用人跑步的速度沿路跑過去、火把舉在手裡，已經跑到門前的領頭一腳踹向木板門（無台詞）")
S("s30", "Close-up, locked", FLOOD,
  "close-up of Xu Yan's face on screen centre, lime dust on his cheek, water dripping from his hair, his eyes wide with alarm, turned toward the back of the village",
  f"his breath catches and his jaw sets hard; {KEEP}",
  ["xuyan"], [("xuyan", "那是全村，", "倒吸一口氣"), ("xuyan", "過冬的糧。", "咬牙")],
  zh="許硯特寫在中間，臉頰沾著石灰粉，頭髮滴水，驚覺地看向畫外右邊村子後面；呼吸一停，下顎咬死")
S("s24", "Medium shot, locked", LANE,
  f"medium shot of {TANG} on the wall top on screen left with two village women in headscarves, all three hurling open cloth sacks down into the mouth of the side passage below on screen right, white lime powder pouring out",
  f"the sacks fly and burst and a white cloud billows up from the passage mouth; {KEEP}",
  ["tangxiaotang"], [("tangxiaotang", "石灰！", "大喊"), ("tangxiaotang", "封巷口！", "又急又脆")],
  zh="唐小棠在左、牆頭上，旁邊兩個包頭巾的村婦，三人把打開的布袋往右邊下方的岔巷口砸，白色石灰倒出來；布袋飛出去、炸開，巷口騰起一團白霧")
S("s25", "Wide shot, slow push in", LANE,
  "wide shot of the lane as a thick white wall of lime smoke rolls across the mouth of the side passage, black-clad assassins coughing and stumbling back out of it, the line of men broken into separate knots",
  f"the smoke boils across the passage and the men reel away from it, the line splitting apart; {KEEP}",
  [], action=3,
  zh="奇觀：村道全景，濃濃一道白色石灰煙牆翻過岔巷口，黑衣刺客咳著、踉蹌退出來，原本一條線的人被拆成好幾團；煙翻滾著封住岔巷，人被逼開、隊伍斷開（無台詞）")
S("s25b", "Medium close-up, locked", LANE,
  f"medium close-up of {TANG} on the wall top on screen left, white lime dust all over her pink sleeves and her looped buns, coughing and waving her hand in front of her face",
  f"she coughs twice and flaps the white cloud away from her nose; {KEEP}",
  ["tangxiaotang"], [("tangxiaotang", "咳……", "嗆到"), ("tangxiaotang", "撒太多了。", "揮手，好氣又好笑")],
  zh="唐小棠中近景在左、牆頭上，粉色袖子和丸子頭全是白石灰，一邊咳一邊在臉前揮手；咳兩聲，把鼻子前的白霧搧開（喜劇）")
S("s26", "Medium close-up, locked", FLOOD,
  f"medium close-up of {QIN} on screen left standing knee-deep in the water with her spear levelled, lime dust drifting past her, her fierce eyes fixed on the broken knots of men down the lane",
  f"she spins the spear once and points it forward; {KEEP}",
  ["qinshuang"], [("qinshuang", "拆成三段了，", "冷笑"), ("qinshuang", "一段一段吃！", "下令")],
  zh="中段爽點：秦霜中近景在左，站在及膝的水裡、槍放平，石灰粉從身邊飄過，狠狠的眼睛看著畫外右邊被拆散的幾團人；槍一轉、往前一指")
S("s27", "Wide shot, locked", FLOOD,
  "wide shot of a knot of five black-clad assassins pinned against a mud-brick wall by a ring of village youths, a dozen long staffs pressing them flat to the wall, their blades knocked down into the water",
  f"the staffs shove in together and the men drop their blades and raise their hands; {KEEP}",
  [], action=3,
  zh="全景：五個黑衣刺客被一圈少年頂在泥磚牆上，十幾根長棍把他們壓得貼牆，刀被打落水裡；長棍一齊往前一頂，刺客丟刀舉手（無台詞）")
S("s31", "Two-shot, locked", FLOOD,
  "two-shot in the flooded lane: A-ling on screen right already turning toward the back of the village, a short dagger in her hand, Xu Yan on screen left catching up beside her",
  f"she starts forward and he falls into step with her, both wading fast; {KEEP}",
  ["aling", "xuyan"], [("aling", "我去。", "冷，已經在走"), ("xuyan", "一起。", "跟上")],
  zh="淹水的村道雙人鏡：阿令在右、已經轉向村子後面，手上一把短匕，許硯在左追到她身邊；她往前走，他跟上並肩，兩人快步涉水")

# ── 糧倉 ──
S("s32", "Wide shot, locked", LEVER,
  "wide shot down the lane: Xu Yan, A-ling and Wang Erniu splashing to a halt at the lane mouth on screen left beside the tall wooden gate lever of the water race, the granary door at the far end on screen right glowing with torchlight",
  f"the three stop dead, Xu Yan's shoulder against the lever post, their eyes on the granary door; {KEEP}",
  ["xuyan", "aling", "erniu"], chapter="糧倉", action=3,
  zh="村道往下看的全景：許硯、阿令、王二牛濺著水停在左邊巷口，旁邊立著水車水道高高的木閘把，巷子盡頭右邊的糧倉門口被火把照亮；三人煞住，許硯的肩靠著閘把的木柱，眼睛盯著糧倉門（e058 開閘的伏筆）")
S("s33", "Medium shot, slow push in", GRAN,
  f"medium shot of {LT} stepping out of the open granary door on screen right, a burning torch in one hand and the short dagger in the other, the stacked grain sacks behind him, his eyes on Xu Yan off screen left",
  f"he strolls out two unhurried steps and stops in the doorway; {KEEP}",
  ["lengtie"], [("lengtie", "解元公，", "冰冷低沉"), ("lengtie", "來得正好。", "一字一頓")],
  zh="冷鐵在右，從打開的糧倉門裡走出來，一手火把、一手短刀，背後是堆到梁的糧袋，看畫外左邊的許硯；不慌不忙走兩步，停在門口")
S("s34", "Medium close-up, locked", LEVER,
  "medium close-up of Xu Yan on screen left at the lane mouth, the lever post beside his shoulder, his chest heaving, his eyes hard on Leng Tie off screen right",
  f"he straightens and lifts his chin; {KEEP}",
  ["xuyan"], [("xuyan", "你的人，", "喘著"), ("xuyan", "都泡在水裡了。", "冷")],
  zh="許硯中近景在左、巷口，閘把的木柱在他肩旁，胸口起伏，眼神硬硬地盯著畫外右邊的冷鐵；他站直、下巴一抬")
S("s34b", "Medium shot, locked", LEVER,
  "medium shot of Wang Erniu at the lane mouth on screen centre edging one step forward with his staff raised, his square face furious, Leng Tie speaks off screen",
  f"his foot comes down in the water and he freezes mid-step, the staff still raised; {KEEP}",
  ["erniu"], [("lengtie", "再一步，", "畫外，冰冷"), ("lengtie", "我就扔。", "畫外")],
  zh="王二牛在中間、巷口，舉著長棍往前挪一步，方臉一臉怒氣，冷鐵畫外說話；腳踩進水裡，整個人僵在半步，棍子還舉著")
S("s35", "Close-up, locked", GRAN,
  "close-up of Leng Tie's pale face on screen right in the torchlight, the corner of his mouth lifting very slightly, his narrow eyes unmoved",
  f"he slowly raises the torch beside his face; {KEEP}",
  ["lengtie"], [("lengtie", "那就燒。", "淡淡地")],
  zh="冷鐵的白臉特寫在右、火把光裡，嘴角極輕地一勾，細眼一點都沒動；他慢慢把火把舉到臉旁")
S("s35b", "Close-up, locked", LEVER,
  "close-up of A-ling's face on screen right at the lane mouth, torchlight from the granary on her moon-white face, her eyes cold and steady on Leng Tie off screen right",
  f"she draws a slow breath and lowers the dagger to her side; {KEEP}",
  ["aling"], [("aling", "你要的，", "平靜"), ("aling", "是我。", "冷")],
  zh="阿令特寫在右、巷口，糧倉的火光照在月白的臉上，眼睛冷而定地看著畫外右邊的冷鐵；慢慢吸一口氣，把短匕垂到身側")
S("s36", "Insert of the torch over the grain sacks, locked", GRAN,
  "insert of a burning torch held a hand's width above stacked grain sacks and loose dry straw in the granary doorway, sparks drifting down from the flame; Leng Tie speaks off screen",
  f"the torch dips lower and a spark floats down and settles on the straw; {KEEP}",
  [], [("lengtie", "交出她，", "畫外，冰冷")],
  zh="【結尾】插鏡：一支火把舉在糧倉門口堆著的糧袋與乾稻草上方一掌高，火星從火苗往下飄；火把再低一點，一顆火星飄下來落在稻草上（冷鐵畫外）")
S("s37", "Two-shot, locked", LEVER,
  "two-shot at the lane mouth: A-ling on screen right stepping forward toward the granary, Xu Yan on screen left throwing his arm out across her to stop her",
  f"she pushes against his arm once and he plants his feet and holds it there; {KEEP}",
  ["aling", "xuyan"], [("aling", "讓我過去。", "很輕"), ("xuyan", "站我後面。", "不放")],
  zh="【結尾】巷口雙人鏡：阿令在右往糧倉跨出去，許硯在左一手橫過她身前把她擋住；她推了一下他的手臂，他兩腳一站、手臂不動")
S("s38", "Close-up, slow push in", GRAN,
  "close-up of Leng Tie's face on screen right behind the raised torch, the flame between them lighting his cold narrow eyes, his eyes on Xu Yan off screen left",
  f"he tilts the torch toward the straw a little more; {KEEP}",
  ["lengtie"], [("lengtie", "不然，", "一字一頓"), ("lengtie", "燒光全村的糧。", "冰冷")],
  zh="【結尾】冷鐵特寫在右、舉起的火把後面，火苗照著他冷冷的細眼，看畫外左邊的許硯；火把再往稻草斜一點")
S("s39", "Close-up, locked", LEVER,
  "close-up of Xu Yan's face on screen left, his arm still out across Aling off screen right, sweat and lime dust on his face, the system voice speaks off screen",
  f"his jaw locks, his eyes flick to the lever post beside him and back to the torch; {KEEP}",
  ["xuyan"], [("xitong", "緊急任務：", "平板電子音，叮一聲"), ("xitong", "人與糧，", "平板電子音"), ("xitong", "都要保住。", "平板電子音")],
  panel=[{"text": "緊急任務：阿令與糧倉，都要保住", "kind": "task"}],
  zh="【結尾】最後一格（系統面板）：許硯特寫在左，手臂還橫在畫外右邊的阿令身前，臉上是汗和石灰粉，眼睛盯著畫外右邊的火把；下顎咬死，眼睛往身旁的閘把一閃、又回到火把上；系統畫外宣布緊急任務")

e.write(
  music="a held silence of low drone and crackling torches as the woman walks into the gap, a single cold high guqin note under her question, a sly reedy suona slide for the false eunuch's answer, then a sudden steel hit when the smile drops, a pounding war drum and clashing cymbals as the assassins charge the hedge of staffs, a rising roar of strings and timpani as the sluice opens and the water floods the lane, hissing white noise and frantic woodblocks in the lime smoke, a tense galloping frame drum toward the granary, then a slow menacing low string and a heartbeat drum that stop dead on the torch above the grain, ancient Chinese rural drama, no vocals",
  title="宮裡來人要接他老婆，她只問一句宮裡的事，對方答錯",
  description="三十騎宮服人馬停在村口，刀出鞘一半。阿令越過許硯走到最前面，只問了一句：「公公，御膳房初一煮什麼？」公公笑著答：「八寶鴨。」阿令冷冷地說：「初一齋戒，御膳房不見葷。假的。」笑容一掉，袖裡的刀就出來了——三十個人全是刺客。秦霜的少年方陣頂住正面，許硯把刺客放進村道，唐小棠在牆頭舉起紅燈籠，許硯拔起渠閘，渠水把村道淹成一條河，火把一支支熄在水裡；唐小棠帶村婦撒石灰封住巷口，刺客被拆成好幾段。可是一隊刺客繞過渠道，舉著火把衝向全村過冬的糧倉。糧倉前，刺客頭領冷鐵把火把舉到糧堆上：「交出她，不然燒光全村的糧。」《種田娶妻打天下》第 57 集。",
  thumb={"headline": "初一\n煮什麼", "tag": "種田娶妻打天下", "shot": "s03"})
