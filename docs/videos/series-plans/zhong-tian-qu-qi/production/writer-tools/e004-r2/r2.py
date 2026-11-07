"""Episode 4 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e004-r2/script.md
(c01-c40 = s01-s40), including its section 「2026-11-06 審稿後的修改」, which overrides the tables (c09 「刀收了」 and the hand
on the sheath; c14 gains Xu Yan's inner line, Tang Xiaotang's new line and becomes a long shot; c23 and c25 「後天日落」;
c25 back on the scene's axis; c32 Erniu at the back right; c37 「柴燒完了，我進屋搬」 and the empty woodpile).

Same rules as e001-r2 to e003-r2: one visible action per shot written as a path, over-the-shoulder and reverse shots
for dialogue, whole sentences, one line per spoken line, default face serious (smiles only where the script allows: c05
an awkward laugh, c18 Xiaohe, c25 Tang Xiaotang a slight smile, c27 Erniu's grin). State: Xu Yan with his sleeves rolled
to the elbows and the rolled red paper in the left of his belt all episode, one stick of firewood in his right hand in
scene 1, the ladle c11, the small cracked iron pot c13-c15, the long stirring pole at night, red-eyed and tired, his arms
full of firewood c38-c39; A-ling without shackles, her sleeves over the red marks, the short knife across her knees
c01-c05 and in a dark brown leather sheath on the left of her belt from c06; Tang Xiaotang always t2 (high collar, closed
garment), the small wooden casket of five gold ingots c16-c25, no writing anywhere; Erniu's big black iron wok upside
down on his back c27-c28, his hands empty after; Qin Shuang's old chopping knife in the right of her belt, the whole dead
pig on her right shoulder c31-c32; the aunties, the villagers and the dark figure have no picture and are never shown by
the face (the figure is Lai San only from e005 on: never named here). Opens on the next instant after e003 c40.
"""
EP = 904  # internal working number; the published slug is zhong-tian-qu-qi-e004-r2
SLUG = "zhong-tian-qu-qi-e004-r2"
EP_TITLE = "新娘搬出一匣金子替他還債，他卻蓋上：這是妳的退路（重製版 r2）"
OUTLINE_SECONDS = 198.5  # script.md 2026-11-06: 44.5 + 82 + 49 + 23 s, 40 shots
TARGET_MINUTES = [3, 4]
TITLE = "新娘搬出一匣金子替他還債，他卻蓋上：這是妳的退路｜種田娶妻打天下 第4集（重製版）"
DESCRIPTION = "深夜灶房，許硯回答阿令：人不是東西，不能拿來押、也不能拿來抵，阿令好感 +3，還是負的。阿令說這話她聽過很多次，許硯說那就看著，做不到她的刀還在。第二天早上米缸只剩一碗米，系統開出材料：豬油、草木灰、大鍋，家裡的小鐵鍋卻裂了縫。唐小棠跑回去抱來一匣金錠要替他還債，許硯把匣子蓋上推回去：這是她要跑時的退路，債他自己賺，唐小棠好感 +10。白天村裡的嬸子送來草木灰，二牛跟打鐵的借來大鍋，最難湊的豬油，秦霜一個人扛來一整頭豬。當晚院子灶棚開鍋熬皂，許硯進屋搬柴時，一個黑影踩上板凳，把一桶水舉到鍋口上。《種田娶妻打天下》第 4 集（重製版）。"
THUMB = ("這是妳的退路", "s17")
CHARACTERS = ["xuyan", "aling", "tangxiaotang", "xiaohe", "erniu", "qinshuang", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: a slow quiet night suspense cue of low cello and soft guqin in the firelit kitchen, carried on from the last episode and dropping out to a single cold electronic blip on the system chime; a warm gentle guqin and soft strings in the farmhouse and the yard in the morning, one bright accent as the small casket opens and a drop-out to one cold blip on the second chime; a light playful comedy of woodblock, pipa and dizi in the sunny yard by day with one heavy hit as the pig is carried in; a low tense cue of drums and erhu by the stove at night, ending on one heavy hit as the dark figure turns; ancient Chinese rural drama, no vocals"

# Scene headers of script.md: the Xu kitchen (set-xujia-zao-t1) at night, the farmhouse room (set-xujia-wu-t1) and the
# yard (set-xujia-yuan-t1) the second morning, the yard by day, the yard's cooking shelter at night. gen-dh maps
# "kitchen" to the kitchen picture, "dirt yard"/"yard gate" to the yard and "Inside the poor thatched farmhouse" to the
# room (kitchen wins over yard, yard over room: the room's shots never name the yard, the yard's never the kitchen).
# Kitchen axis: the door on screen left, the stove on screen right with its fire mouth facing left (e003). Room: the
# door on the left, the rice crock in the back corner, the small stove on the right. Yard by day: the woodpile on the
# left, the table in the middle, the gate on the right. Night: the shelter post on the left, the stove and the wok in
# the middle, the house door on the right, the gate and fence at the back left (as e005 opens).
LOC = {
    "kitchen": "Inside the small earthen kitchen of the Xu farmhouse at night, packed earth walls and floor, the plank door on screen left with faint cold moonlight beyond it, a clay stove on screen right with its fire mouth facing left and a fire burning in it, firewood stacked against the wall, lit only by the warm orange glow of the stove fire and a small clay oil lamp",
    "house_door_night": "Inside the poor thatched farmhouse of the Xu family at night, just behind the half-open plank door, only darkness inside the house, a faint orange glow of a fire far outside the doorway",
    "house": "Inside the poor thatched farmhouse of the Xu family on an autumn morning, earthen walls and a packed earth floor, the plank door on screen left, a big clay water vat by the back wall, a clay rice crock with a wooden lid in the corner by the back wall, a small clay stove on screen right with one small iron pot on it, a low table with two stools, clear morning light slanting in from the door and window on the left",
    "yard_am": "In the dirt yard of the Xu farmhouse on a clear autumn morning, an autumn tree, a bamboo fence, a woodpile on screen left, the house eaves along the back, a wooden table in the middle, the yard gate in the fence on screen right, warm morning sunlight from screen right",
    "yard_day": "In the dirt yard of the Xu farmhouse on a clear autumn day, an autumn tree, a bamboo fence, a woodpile on screen left, a wooden table in the middle, the yard gate in the fence on screen right, bright slanting sunlight from screen right",
    "yard_night": "In the dirt yard of the Xu farmhouse on a clear autumn night, at the cooking shelter on the east side of the yard: one wooden shelter post on screen left, a clay stove in the middle with one big black iron wok on it giving off white steam, the house door on screen right about six paces from the stove, the bamboo fence and the yard gate at the back left, only a few broken twigs left beside the stove, lit by the warm orange glow of the stove fire and cold moonlight",
}
LIGHT = {
    "kitchen": "the warm orange firelight stays unchanged",
    "house_door_night": "the faint orange glow from outside stays unchanged",
    "kitchen_fire": "the warm orange firelight stays steady apart from that one flare",
    "house": "the slanting morning light stays unchanged",
    "yard_am": "the warm morning sunlight from the right stays unchanged",
    "yard_day": "the bright slanting sunlight from the right stays unchanged",
    "yard_night": "the warm orange firelight and the cold moonlight stay unchanged",
}

# Repeated wording (each prop is one object; the descriptions say "one" where it first appears).
TANG = "her peach-pink brocade ruqun one closed garment from the high stand-up collar to the waist"
VILL = "villagers in Song-dynasty cross-collared coarse cotton jackets and cloth head-wraps"
XU = "his blue-grey scholar's robe with his sleeves rolled up to the elbows"
BELT = "the rolled red paper tucked into the left side of his belt with its plain blank back outward"
ALING = "no shackles, her sleeves pulled down over her wrists"
KNIFE = "one short single-edged knife with an iron-grey blade about a hand and a half long and a wooden handle"
BOX = "one small wooden casket the size of a book, two palms wide and one palm deep, with a lid hinged at the back, in dark brown lacquer with one brass clasp, small enough to carry in one hand, plain, with no writing anywhere"  # same size in every shot (owner: the box grew and shrank)
GOLD = "five small yuanbao-shaped gold ingots, plain gold with no marks or writing"
WOK = "one big black iron wok about two and a half feet across with an ear handle on each side"
PIG = "one whole black-haired pig, dead and limp with its eyes closed, its four legs tied together with straw rope, no blood and no wound"
NIGHT = "red-eyed and tired"

SHOTS = [
    # ---- scene 1: the kitchen, the first night (the same instant as e003 c40), stove fire and the oil lamp on the stove
    # top, cold moonlight at the door. Axis: Xu Yan squatting on screen left facing right, A-ling on the stool before the
    # fire mouth on the right; c08 she walks to the door on the left, Xu Yan stays at the back right.
    dict(chapter="灶房", loc="kitchen", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="kitchen_fire",
         comp=f"medium close-up, closing in to a close-up by the end, of Xu Yan squatting before the fire mouth of the stove, {XU}, one stick of firewood in his right hand held at the fire mouth, the firelight on his face, unsmiling; behind him only the earthen wall of the same kitchen",
         lines=[("xuyan", "阿令，人不是東西，不能拿來押，也不能拿來抵。", "一字一字")],
         motion="he slowly pushes the stick into the fire mouth, the fire leaps up once, and he lifts his eyes to A-ling off screen right",
         zh="近景、慢推（中近景推到近景）：許硯蹲在灶口前，右手那根柴慢慢推進灶口，火往上竄一下，抬頭看阿令；火光照臉、不笑"),
    dict(loc="kitchen", cam="Over-the-shoulder medium shot, slow push in", chars=["aling", "xuyan"], night="kitchen",
         comp=f"over-the-shoulder shot from behind Xu Yan's shoulder and his rolled-up sleeve in the left foreground, A-ling on screen right sitting on a low stool before the fire mouth, {ALING}, {KNIFE} lying across her knees with its edge turned outward, her right hand on its wooden handle, cold and unsmiling",
         lines=[("xitong", "叮。阿令好感 +3。", "冷淡，叮一聲")],
         panel=[("阿令 好感 +3 → -2", "panel")],
         motion="A-ling's right hand on the knife handle slowly loosens, her fingers leave the handle and settle flat on her knee; all lips stay closed",
         zh="過肩（許硯肩後拍阿令，他的主觀）、慢推：阿令坐矮凳，短刀橫在膝上（刀刃朝外），袖子蓋住手腕；握刀柄的右手慢慢鬆開，手指放到膝上；不笑"),
    dict(loc="kitchen", cam="Close-up, slow push in", chars=["xuyan"], night="kitchen",
         comp=f"close-up of Xu Yan squatting, {XU}, his face lit by a faint pale blue glow from the empty air before him, no panel drawn, first a flash of delight, then his face falls, unsmiling; behind him only the earthen wall of the same kitchen",
         lines=[("xuyan", "才漲到負二，說到底還是負的啊。", "心裡話，嘴閉著，一喜又垮", "inner"),
                ("xitong", "負的也是宿主自己說空話扣的。", "冷")],
         motion="he clenches one fist on his knee, then opens it again and his shoulders slump; his lips stay closed",
         zh="近景、慢推（長鏡買 8 秒）：許硯臉被淡藍光照亮（不畫面板），先一喜、又垮下來，膝上握一下拳又鬆開，肩膀垮下來；心裡話，嘴閉著；系統冷冷回一句"),
    dict(loc="kitchen", cam="Reverse close-up, slow push in", chars=["aling"], night="kitchen",
         comp=f"reverse close-up of A-ling on the low stool, {ALING}, the short knife across her knees, frowning, unsmiling, her eyes on Xu Yan off screen left; behind her only the stove and its firelight in the same kitchen",
         lines=[("aling", "你臉上一下高興一下發苦，在想什麼？", "冷")],
         motion="she tilts her head, frowning at his face, and leans forward a little",
         zh="近景反打、慢推：阿令歪一下頭，皺眉看許硯臉上一下鬆一下垮，身子往前探一點；身後只有灶與火光；不笑"),
    dict(loc="kitchen", cam="Medium shot, slow push in", chars=["xuyan", "aling"], night="kitchen",
         comp=f"medium shot, Xu Yan before the stove, {XU}, {BELT}, with an awkward dry laugh, and A-ling at the right edge of the frame on the low stool, her sleeves pulled down over her wrists",
         lines=[("xuyan", "沒什麼，我是說……這灶火總算旺起來了。", "尷尬")],
         motion="Xu Yan hurries to his feet, pats the dust off the hem of his robe and points at the fire mouth; A-ling's lips stay closed",
         zh="中景、慢推：許硯趕緊站起來拍拍衣擺上的灰，指一指灶口；右邊緣阿令；尷尬（可以乾笑）"),
    dict(loc="kitchen", cam="Medium shot, slow push in", chars=["aling", "xuyan"], night="kitchen",
         comp=f"medium shot past the glowing fire mouth of the stove in the foreground, A-ling on screen right, {ALING}, the short knife in her right hand, one dark brown leather sheath on the left side of her belt, cold and unsmiling, and Xu Yan standing at the left edge of the frame, his sleeves rolled up",
         lines=[("aling", "人不是東西，這話我聽過很多次，沒一個做到。", "冷")],
         motion="A-ling slides the knife into the sheath on her belt, rises and brushes the dust off her skirt; Xu Yan's lips stay closed",
         zh="中景、慢推、前景灶火：阿令把短刀插回腰帶左邊的深褐皮鞘，站起身，拍掉裙上的灰；許硯站在左邊緣"),
    dict(loc="kitchen", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="kitchen",
         comp=f"reverse medium close-up, closing in to a close-up by the end, of Xu Yan standing, {XU}, {BELT}, earnest and unsmiling, his eyes on A-ling off screen right; behind him only the earthen wall and the firewood stacked against it in the same kitchen",
         lines=[("xuyan", "那妳就看著。我要是做不到，妳那把刀還在。", "認真")],
         motion="he takes half a step forward, looks at her and lifts his chin once toward the sheath at her waist off screen right",
         zh="反打近景、慢推（中近景推到近景）：許硯往前半步看著她，朝她腰間的刀鞘抬一下下巴；認真、不笑"),
    dict(loc="kitchen", cam="Full shot, tracking", chars=["aling", "xuyan"], nospeak=["xuyan"], night="kitchen",
         comp=f"full shot past the kitchen door frame in the foreground, A-ling at the doorway on screen left with her back to the room, {ALING}, the short knife in the dark brown leather sheath on the left of her belt; at the back right Xu Yan standing by the stove, a dark silhouette against the firelight, his face in shadow",
         lines=[("xuyan", "那妳也早點睡，刀別磨到天亮了。", "畫外，試探，遠一點")],
         motion="A-ling walks to the doorway with her back to Xu Yan, puts one hand on the door frame and stops there; all lips stay closed",
         zh="全景、跟拍（跟著阿令往左）、前景門框：阿令走到灶房門口，背對許硯，伸手扶住門框停一下；許硯在右後灶火邊、背光看不到嘴（台詞不對嘴）"),
    dict(loc="kitchen", cam="Close-up, slow push in", chars=["aling"], night="kitchen",
         comp=f"close-up of A-ling at the kitchen doorway, half turned back, {ALING}, the dark brown leather sheath at the left of her belt, unsmiling; behind her only the night outside the door and the cold moonlight",
         lines=[("aling", "刀收了。記住你說的，我會一直看著。", "很輕")],
         motion="she presses the sheath at her waist, half turns to glance back at Xu Yan off screen right, then steps over the threshold and out of the frame on screen left",
         zh="近景、慢推：阿令在門口，手按一下腰間刀鞘，半回頭看許硯一眼，說完跨出門檻往左走進夜裡出畫；身後是門外夜色與冷月光；不笑（結尾）"),
    # ---- scene 2: the second morning, morning light from the door and window on the left. c10-c15 the farmhouse room
    # (door left, Xu Yan left, Xiaohe right by the rice crock); c16-c25 the same yard at the wooden table (Xu Yan sits at
    # its left, Xiaohe beside him, Tang Xiaotang stands on the right).
    dict(chapter="米與金子", loc="house", cam="Full shot, tracking", chars=["xiaohe", "xuyan"], night="house",
         comp=f"full shot past the clay rice crock in the foreground, little Xiaohe in her patched lilac short jacket with red-string pigtails, her small straw rabbit tucked into her sash, squatting before the rice crock with one wooden ladle in her right hand, hurt and unsmiling; Xu Yan far off on screen left, {XU}",
         lines=[("xiaohe", "哥，米缸只剩一碗米了，煮完今天就沒了。", "委屈")],
         motion="Xiaohe lifts the crock's wooden lid, scrapes the ladle round its bottom, then lifts her head; Xu Yan's lips stay closed",
         zh="全景、跟拍（往後牆角）、前景米缸：小禾右手木勺蹲在米缸前，掀開木蓋，木勺刮缸底，抬頭；許硯在左邊遠處；委屈、不笑"),
    dict(loc="house", cam="Close-up, slow push in", chars=["xuyan"], night="house",
         comp=f"close-up of Xu Yan squatting by the clay rice crock, {XU}, {BELT}, one wooden ladle in his right hand, unsmiling; behind him only the earthen wall of the same farmhouse room",
         lines=[("xuyan", "一碗米也夠撐一天，今天先把做肥皂的東西湊齊。", "平穩")],
         motion="he squats down, takes the ladle from a small hand at the right edge, glances into the bottom of the crock and lays the ladle back inside",
         zh="近景、慢推：許硯走過來蹲下，從小禾手裡接過木勺，往缸底看一眼，把勺子放回缸裡；身後只有屋內土牆；不笑"),
    dict(loc="house", cam="Extreme close-up, slow push in", chars=["xuyan"], night="house",
         comp="extreme close-up of Xu Yan's eyes, the shot opens directly on his eyes from its very first frame, a faint pale blue light reflected in his pupils; nothing else in the frame",
         lines=[("xitong", "材料：豬油、草木灰、大鍋。", "冷淡")],
         panel=[("材料：豬油・草木灰・大鍋", "panel")],
         motion="his eyes flick up to the upper right and he blinks once, his lips staying closed",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：瞳孔映淡藍光（不畫面板），眼睛往右上一轉，眨一下"),
    dict(loc="house", cam="Insert close-up, slow push in", chars=["xuyan"], night="house", act=3,
         comp="insert close-up of the small clay stove, the shot opens directly on the small iron pot from its very first frame: one small black iron pot on the stove and Xu Yan's two hands in his rolled-up blue-grey cuffs gripping its rim; only the hands, cuffs and pot are in the frame, his face out of the frame; behind them only the window light of the same farmhouse room",
         lines=[("xuyan", "大鍋？家裡這口鍋，連粥都快煮不了。", "心裡話，嘴閉著，發愁", "inner"),
                ("xitong", "宿主缺的不只是鍋。", "冷")],
         motion="his hands lift the small pot off the stove, turn it upside down and hold it up to the window light; one crack across the bottom shows a thin line of light",
         zh="手部特寫、慢推（第一格就是小鐵鍋，長鏡買 8 秒）：許硯的兩手把小鐵鍋從灶上拿起來翻過來對著窗光，鍋底一道裂縫透出光；心裡話；系統冷冷一句"),
    dict(loc="house", cam="Medium shot, slow push in", chars=["tangxiaotang", "xuyan"], night="house",
         comp=f"medium shot past the plank door frame in the left foreground, Tang Xiaotang peeking in round the door frame on screen left, {TANG}, her small gold abacus at her waist, unsmiling; Xu Yan on screen right, {XU}, the small cracked iron pot held upside down in both hands",
         lines=[("xuyan", "缺錢又缺人手，這我比誰都清楚。", "心裡話，嘴閉著", "inner"),
                ("tangxiaotang", "鍋裂了，米也見底，說到底就是缺錢。等著別走！", "說話快")],
         motion="first Xu Yan looks down at the cracked pot and sighs, lips closed; then Tang Xiaotang leans in at the door frame, glances from the pot to him, her eyes darting",
         zh="中景、慢推、前景門框（長鏡買 8 秒）：先許硯低頭看鍋底裂縫，嘆一口氣（心裡話，嘴閉著）；唐小棠（t2）扶著門框探頭，看看裂鍋又看看他，眼睛一轉（她聽到小禾說米只剩一碗）"),
    dict(loc="house", cam="Full shot, slow push in", chars=["tangxiaotang", "xiaohe", "xuyan"], night="house",
         comp=f"full shot from inside the room past the wide-open plank door in the left foreground: outside on the sunny bare ground Tang Xiaotang, {TANG}, running toward the gate in the bamboo fence on the right; inside little Xiaohe at the doorway, her straw rabbit tucked into her sash; Xu Yan on screen right by the small clay stove, his sleeves rolled up, the cracked pot in his hands",
         lines=[("xiaohe", "小棠姐姐跑那麼快，是要去哪裡？", "歪頭"),
                ("xuyan", "不知道。她叫我們等，那就在院子等一下。", "無奈")],
         motion="Tang Xiaotang runs out through the gate off screen right; Xiaohe runs to the doorway and looks back; Xu Yan sets the pot on the stove and shakes his head",
         zh="全景、慢推，從屋內往外拍、前景敞開的屋門（長鏡買 8 秒）：唐小棠（t2）提起裙擺跑出院門往右出畫；小禾追到門口回頭問；許硯把鍋放回灶上、搖搖頭回答"),
    dict(loc="yard_am", cam="Full shot, slow push in", chars=["tangxiaotang", "xuyan", "xiaohe"], night="yard_am",
         comp=f"full shot past the wooden table in the foreground, Xu Yan sitting at the left end of the table, {XU}, and little Xiaohe standing beside him; Tang Xiaotang, {TANG}, hurrying in from the yard gate on screen right, carrying {BOX} in both hands",
         lines=[("tangxiaotang", "許硯，二十兩是吧？你看看這些夠不夠。", "精明")],
         motion="Tang Xiaotang reaches the table, sets the casket down with a thump and catches her breath; the others' lips stay closed",
         zh="全景、慢推、前景木桌：許硯坐木桌左邊、小禾站他旁邊；唐小棠（t2）從右邊院門快步走回來，兩手抱小木匣，往桌上一放，喘一口氣"),
    dict(loc="yard_am", cam="Insert close-up, slow push in", chars=["tangxiaotang"], night="yard_am", act=3,
         comp=f"insert close-up of the small wooden casket on the wooden table, the shot opens directly on the casket's brass clasp from its very first frame: {BOX}, and Tang Xiaotang's fingers in her peach-pink brocade cuff on the clasp; only the hand, cuff and casket are in the frame, her face out of the frame, her ruqun one closed garment from the high collar to the waist; behind it only the out-of-focus tabletop of the same yard",
         lines=[],
         motion=f"her fingers flick the brass clasp open and lift the lid; inside, {GOLD}, catch the sunlight and gleam",
         zh="手部特寫、慢推（第一格就是木匣的銅扣）：唐小棠的手指（桃粉織錦袖口）撥開銅扣、掀開匣蓋，裡面五錠元寶形小金錠在日光下一亮；沒有字"),
    dict(loc="yard_am", cam="Close-up, slow push in", chars=["xiaohe"], night="yard_am",
         comp="close-up of little Xiaohe with red-string pigtails and one front tooth missing, her patched lilac jacket, her small straw rabbit tucked into her sash, her eyes wide with delight; behind her only the bamboo fence of the same yard",
         lines=[("xiaohe", "好多金子！哥，我們有錢還債了！", "驚呼")],
         motion="she rises on tiptoe, grips the table edge with both hands, peers into the casket below the frame and bursts into a smile",
         zh="近景、慢推：小禾踮腳趴到桌邊，兩手扒著桌沿往匣裡看，眼睛睜大，笑出來（可以笑）；身後只有院子籬笆"),
    dict(loc="yard_am", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], night="yard_am",
         comp=f"over-the-shoulder shot past Xu Yan's shoulder in the left foreground, Tang Xiaotang on screen right across the wooden table framed from the chin up, {TANG}, offhand, a cool careless look as if it were nothing, lips pressed flat, never smiling, both hands on {BOX}, its hinged lid standing open behind it, {GOLD} inside",
         lines=[("tangxiaotang", "這點不過是零頭，拿去還，省得錢員外再上門。", "輕描淡寫")],
         motion="she pushes the casket across the table toward Xu Yan with both hands and lifts her chin",
         zh="過肩（許硯肩後拍唐小棠）、慢推（唐小棠下巴以上）：唐小棠兩手把木匣往許硯那邊一推，下巴一抬；輕描淡寫、不笑"),
    dict(loc="yard_am", cam="Insert close-up, slow push in", chars=["xuyan"], nospeak=["xuyan"], night="yard_am", act=3,
         comp="insert close-up of the small wooden casket on the wooden table, the shot opens directly on Xu Yan's hand on the casket lid from its very first frame: his right hand in his rolled-up blue-grey cuff resting on the half-open dark brown lacquered lid, the brass clasp, the gold ingots glinting inside; only the hand, cuff and casket are in the frame, no face and no mouth; behind it only the out-of-focus tabletop of the same yard",
         lines=[("xuyan", "這是妳的退路，我不能拿。", "畫外，溫和")],
         motion="his hand slowly closes the lid, snaps the brass clasp shut, then pushes the casket back across the table toward screen right",
         zh="手部特寫、慢推（第一格就是許硯的手按在木匣蓋上）：許硯的手（藍灰袖口捲著）把匣蓋慢慢蓋上，扣好銅扣，推回唐小棠面前；畫面上沒有嘴"),
    dict(loc="yard_am", cam="Reverse close-up, slow push in", chars=["tangxiaotang"], night="yard_am",
         comp=f"reverse close-up of Tang Xiaotang framed from the chin up, her high stand-up collar closed at her throat, {TANG}, stunned and unsmiling, her hand resting on the closed casket below the frame; behind her only the bamboo fence and the autumn tree of the same yard",
         lines=[("tangxiaotang", "你不要？二十兩壓在你身上，你還跟金子客氣？", "愣住")],
         motion="she freezes, then looks at Xu Yan off screen left properly for the first time and leans forward",
         zh="反打近景、慢推（唐小棠下巴以上）：唐小棠愣住，手停在木匣上，第一次認真看他，身子往前傾；身後只有籬笆與秋樹；不笑"),
    dict(loc="yard_am", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="yard_am",
         comp=f"medium close-up, closing in to a close-up by the end, of Xu Yan sitting at the wooden table, {XU}, {BELT}, unsmiling, his eyes on her off screen right; behind him only the bamboo fence and the autumn tree of the same yard",
         lines=[("xuyan", "妳說過在躲一個人。真到要跑那天，妳得有盤纏。", "認真")],
         motion="he draws his hand back from the casket, sits up straight and looks at her",
         zh="近景、慢推（中近景推到近景）：許硯把手從木匣上收回來，身子往後坐直，看著她；背景籬笆與秋樹；不笑"),
    dict(loc="yard_am", cam="Close-up, slow push in", chars=["tangxiaotang"], night="yard_am",
         comp=f"close-up of Tang Xiaotang framed from the chin up, her high stand-up collar closed at her throat, {TANG}, unsmiling, both hands on the closed casket below the frame; behind her only the bamboo fence of the same yard",
         lines=[("xuyan", "債是我欠的，我自己賺。後天日落前，夠了。", "畫外，認真")],
         motion="she slowly lowers her head, her fingers tightening on the casket lid; her lips stay closed",
         zh="近景、慢推（唐小棠下巴以上）：唐小棠兩手按在木匣上，慢慢低下頭，手指收緊；嘴閉著；許硯畫外"),
    dict(loc="yard_am", cam="Extreme close-up, slow push in", chars=["xuyan"], night="yard_am",
         comp="extreme close-up of Xu Yan's eyes, the shot opens directly on his eyes from its very first frame, a faint pale blue light reflected in his pupils; nothing else in the frame",
         lines=[("xitong", "叮。唐小棠好感 +10。", "冷淡，叮一聲")],
         panel=[("唐小棠 好感 +10 → 10", "panel")],
         motion="his eyes blink once and his gaze settles down and to the right on the bowed head off screen, his lips staying closed",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：瞳孔映淡藍光，眨一下，視線落在低著頭的唐小棠身上"),
    dict(loc="yard_am", cam="Medium shot, tracking", chars=["tangxiaotang", "xuyan", "xiaohe"], night="yard_am",
         comp=f"medium shot, Tang Xiaotang on screen right, {TANG}, {BOX}, its lid closed, held easily against her side in one arm, no bigger than a book, the corners of her mouth lifting in a slight smile; Xu Yan and little Xiaohe on screen left at the left end of the wooden table, the house eaves on screen right",
         lines=[("tangxiaotang", "那我先記在帳上。後天日落賺不到，我可要笑你。", "帶一點笑")],
         motion="Tang Xiaotang turns with the casket, walks two steps right, looks back left at Xu Yan, then walks out of the frame on screen right; the others' lips stay closed",
         zh="中景、跟拍（跟著唐小棠往右）：唐小棠（t2）抱起木匣轉身往右邊屋簷下走兩步，停下回頭往左看許硯，嘴角帶一點笑，說完往右出畫；許硯、小禾在左（結尾）"),
    # ---- scene 3: the same yard by day, late morning to afternoon, slanting light from the right. Axis: Xu Yan on the left
    # facing right; everyone from the gate comes in from the right. Never crosses the line.
    dict(chapter="湊材料", loc="yard_day", cam="Full shot, tracking", chars=["xuyan"], night="yard_day",
         comp=f"full shot past the bamboo fence in the foreground: on screen right three village women in Song-dynasty cross-collared coarse cotton short jackets, cloth head-wraps and cloth shoes, seen side-on or from behind, their faces never shown, each carrying one bamboo basket of grey-white plant ash; on screen left Xu Yan, {XU}, beside one wooden bucket",
         lines=[("xuyan", "多謝各位嬸子，有了這些草木灰，肥皂就成了一半。", "誠懇")],
         motion="the women tip the grey-white ash from their baskets into the bucket in a small puff; Xu Yan bends and hands the empty baskets back; the women's lips stay closed",
         zh="全景、跟拍、前景籬笆：右邊三個嬸子（側身、不拍正臉，宋式交領短打、布包頭）把竹籃裡的草木灰倒進許家的木桶，灰揚起一點；許硯彎腰接過空籃子遞還"),
    dict(loc="yard_day", cam="Full shot, slow push in", chars=["erniu", "xuyan"], night="yard_day",
         comp=f"full shot past the yard gate in the foreground, Wang Erniu in his coarse brown short jacket with rolled sleeves, {WOK} upside down on his back, both hands gripping its rim over his shoulders, grinning; Xu Yan on screen left, his sleeves rolled up",
         lines=[("erniu", "秀才！大鍋來了，我跟村頭打鐵的借來的！", "大嗓門")],
         motion="Erniu squeezes in at the gate, the wok clangs on the gate frame, and he twists sideways through, grinning; Xu Yan's lips stay closed",
         zh="全景、慢推、前景院門：二牛背上倒扣大黑鐵鍋、兩手從肩上抓鍋沿，從院門擠進來，鍋邊「噹」地撞上門框，歪身子硬擠過來，咧嘴笑（可以笑）；許硯在左"),
    dict(loc="yard_day", cam="Two-shot, tracking", chars=["xuyan", "erniu"], night="yard_day",
         comp="two-shot, Xu Yan on screen left, his sleeves rolled up, and Wang Erniu on screen right with the big black iron wok upside down on his back, both hands on its rim",
         lines=[("xuyan", "二牛，好兄弟，這口鍋的情我記下了。", "感激")],
         motion="the two of them lift the wok off Erniu's back and set it down with a thud; Xu Yan pats Erniu's shoulder; Erniu's lips stay closed",
         zh="雙人鏡、跟拍：許硯迎上去，兩人一起把大鍋從二牛背上卸下來放到地上，鍋底「咚」一聲；許硯拍二牛的肩膀"),
    dict(loc="yard_day", cam="Medium shot, slow push in", chars=["erniu"], night="yard_day",
         comp=f"medium shot of Wang Erniu, both hands empty, sweat beading on his forehead, sulking and unsmiling; behind him the bamboo fence with about five {VILL} showing only their upper bodies, pointing and whispering",
         lines=[("erniu", "可外頭的人都在笑，說你連熬油的豬都沒有。", "不服氣，小聲")],
         motion="he wipes the sweat off with the back of his hand, ducks low, glances at the fence and leans in toward Xu Yan off screen left",
         zh="中景、慢推：二牛（兩手空空、滿頭汗）用手背擦汗，壓低身子往籬笆外瞄一眼，湊近許硯；背景籬笆外村民指指點點；不服氣、不笑"),
    dict(loc="yard_day", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="yard_day",
         comp=f"reverse medium close-up, closing in to a close-up by the end, of Xu Yan, {XU}, {BELT}, unsmiling, looking down; behind him only the woodpile of the same yard",
         lines=[("xuyan", "他們說得沒錯，豬油是最難湊的那一樣。", "沉著")],
         motion="he looks down at the empty wok below the frame and reaches out to touch its cold rim once",
         zh="近景反打、慢推（中近景推到近景）：許硯低頭看那口空鍋，伸手摸一下冰冷的鍋沿；身後只有柴堆；不笑"),
    dict(loc="yard_day", cam="Low-angle full shot, slow push in", chars=["qinshuang"], night="yard_day", act=4,
         comp=f"low-angle full shot past the shoulders and cloth head-wraps of {VILL} outside the fence in the foreground, Qin Shuang at the yard gate in her dark brown cross-collared short jacket, wide leather belt with her old chopping knife in its right side, black trousers and leather boots, carrying on her right shoulder {PIG}, her right hand gripping the straw rope",
         lines=[],
         motion="the villagers at the fence gasp and shrink aside, and Qin Shuang strides in through the gate with the pig on her shoulder, every step landing heavy; all lips stay closed",
         zh="低角度全景、慢推、前景籬笆外村民的肩膀（布包頭）：村民驚呼往兩邊讓開，秦霜右肩扛一整頭黑毛死豬（閉眼、四腳草繩綁著、不見血）大步走進院門，每一步都很重"),
    dict(loc="yard_day", cam="Medium shot, slow push in", chars=["qinshuang", "xuyan", "erniu"], night="yard_day",
         comp="medium shot, Qin Shuang in the middle with the whole black pig on her right shoulder, her old chopping knife in the right side of her belt; Xu Yan on screen left, his sleeves rolled up; Wang Erniu at the back right, both hands empty",
         lines=[("qinshuang", "豬油要多少？這一頭夠不夠你熬？", "爽快")],
         motion="Qin Shuang drops the pig from her shoulder to the ground in a puff of dust, straightens and brushes off her hands; the others' lips stay closed",
         zh="中景、慢推：中秦霜屈膝把豬從肩上卸到地上，地面一震、塵土揚起，直起身拍拍手；左許硯、右後二牛"),
    dict(loc="yard_day", cam="Close-up, slow push in", chars=["xuyan"], night="yard_day",
         comp=f"close-up of Xu Yan, {XU}, dumbfounded; behind him only the woodpile of the same yard",
         lines=[("xuyan", "妳一個人，從哪裡扛回來的？", "傻眼")],
         motion="he steps half a step back, looks from the pig below the frame to Qin Shuang off screen right and points a finger at the pig",
         zh="近景、慢推：許硯往後退半步，看看地上的豬又看看她，手指指豬；身後只有柴堆；傻眼"),
    dict(loc="yard_day", cam="Reverse close-up, slow push in", chars=["qinshuang"], night="yard_day",
         comp="reverse close-up of Qin Shuang, a few pig bristles stuck on her right shoulder, her old chopping knife in the right side of her belt, with a scornful snort, unsmiling; behind her only the yard gate of the same yard",
         lines=[("qinshuang", "別問。你要是熬不出東西，下次扛的就是你。", "嗤一聲")],
         motion="she brushes the bristles off her shoulder and walks out of the frame on screen left, glancing back",
         zh="近景反打、慢推：秦霜（肩上沾豬毛）拍掉豬毛，轉身往畫面左的柴堆走，邊走邊回頭，說完出畫；身後只有院門；嗤一聲（不笑）"),
    dict(loc="yard_day", cam="Two-shot, slow push in", chars=["xuyan", "erniu"], night="yard_day",
         comp="two-shot, Xu Yan on screen left, his sleeves rolled up, and Wang Erniu on screen right, both hands empty; in the foreground on the ground the whole black pig, the big black iron wok and one wooden bucket of grey-white plant ash",
         lines=[("xuyan", "夠了。豬油、灶灰、大鍋都齊了，今晚就開鍋熬。", "定下來")],
         motion="Xu Yan looks over the pig, the wok and the ash, pushes his sleeves higher and slaps the wok rim with a clang; Erniu nods, lips closed",
         zh="雙人鏡、慢推：前景地上的豬、大鍋、一桶草木灰；許硯看看豬、大鍋和那桶灰，把袖子再捲高，拍一下鍋沿「噹」；二牛跟著點頭（結尾）"),
    # ---- transition: the second night at the cooking shelter on the east side of the yard (as e005 opens): post left,
    # stove and wok in the middle, house door right, gate and fence at the back left; firelight and cold moonlight.
    dict(chapter="夜裡", loc="yard_night", cam="Full shot, slow push in", chars=["xuyan", "erniu"], night="yard_night",
         comp=f"full shot past the stove fire in the foreground, Xu Yan in the middle standing at the big wok, {XU}, {NIGHT}, both hands on one long wooden stirring pole taller than a man; Wang Erniu squatting before the fire mouth of the stove; white steam rising from the wok",
         lines=[("erniu", "秀才，這鍋豬油加灶灰，真能洗衣服？", "憨，懷疑")],
         motion="Xu Yan stirs round and round; Erniu pushes a stick into the fire mouth, sparks fly up, and he looks up at Xu Yan, whose lips stay closed",
         zh="全景、慢推、前景灶火：許硯（累、眼睛發紅）兩手握長木棍一圈一圈攪鍋；二牛往灶口推一根柴，火星往上竄，抬頭看許硯；大鍋冒白氣"),
    dict(loc="yard_night", cam="Close-up, tracking", chars=["xuyan", "erniu"], night="yard_night",
         comp=f"close-up of Xu Yan at the wok, {XU}, {NIGHT}, both hands on the long stirring pole, white steam drifting past; at the left edge of the frame Wang Erniu getting to his feet; behind them only the bamboo fence in the dark of the same yard",
         lines=[("xuyan", "能。等天亮開了模你就知道。柴燒完了，我進屋搬。", "累，但有把握")],
         motion="Xu Yan yawns, glances at the bare twigs, leans the pole on the wok and walks right to the house door; Erniu, lips closed, yawns and leaves at the back left",
         zh="近景、跟拍（跟著許硯往右，長鏡買 8 秒）：許硯邊攪邊打呵欠，看一眼空了的柴堆，說完把木棍斜靠在鍋邊，往右邊屋門走去搬柴；左邊緣二牛站起來點頭打呵欠，往左後院門出畫（回家睡）"),
    dict(loc="yard_night", cam="Point-of-view full shot, slow push in", chars=[], night="yard_night", act=4,
         comp="point-of-view full shot through the narrow gap of the half-open house door, the dark door frame and a bundle of firewood edging the foreground: beyond the gap, about six paces away, the steaming big wok left unattended on the stove, one low wooden stool beside it, and one small thin dark figure clearly visible in the middle of the gap in a grey-brown short jacket and an old cloth head-wrap, back-lit by the stove fire, his face in deep shadow and never seen, one wooden bucket full of water in both hands",
         lines=[],
         motion="the dark figure creeps out of the shadow of the fence at the back left to the wok, steps up onto the stool and lifts the bucket with both hands over the mouth of the wok; no one speaks",
         zh="主觀（許硯在屋門內抱一捆柴，從門縫往外看）、慢推、前景門框：門縫外一個黑影（瘦小、灰褐短褐、舊布頭巾、背光、臉在暗處）從左後籬笆陰影摸到鍋邊，一腳踩上板凳，兩手把水桶舉到鍋口上方"),
    dict(loc="house_door_night", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="house_door_night",
         comp=f"medium close-up, closing in to a close-up by the end, of Xu Yan standing just inside the house door, facing the camera and looking out through the doorway, {XU}, {NIGHT}, one bundle of firewood in both arms, shocked and furious, staring out at the figure by the wok off screen, unsmiling; behind him only the darkness inside the house; no stove or wok in the frame",
         lines=[("xuyan", "誰在那裡！把水桶給我放下，別碰那口鍋！", "厲聲")],
         motion="the firewood in his arms crashes down to the floor and he braces one hand against the door",
         zh="近景、慢推（中近景推到近景）：許硯在屋門內，懷裡的柴嘩啦掉了一地，一手撐住門板；身後只有屋內的黑暗；驚怒、不笑（結尾，懸念到第 5 集）"),
    dict(loc="yard_night", cam="Close-up, slow push in", chars=[], night="yard_night", act=3,
         comp="close-up of one small thin dark figure standing on the low wooden stool by the steaming wok, in a grey-brown short jacket and an old cloth head-wrap, back to the stove fire, his face in deep shadow and never seen, one wooden bucket full of water raised in both hands; behind him only the steam and the firelight of the same cooking shelter",
         lines=[],
         motion="the figure jerks his head round toward the house door on screen right, the bucket in his hands already tipping and the water sloshing at its rim; the shot ends on that moment",
         zh="近景、慢推：黑影站在板凳上兩手舉著木水桶，背著灶火、臉在暗處；猛一回頭往右邊屋門看，水桶已經傾斜、水在桶口晃；收在這一刻"),
]

HEAD = [
    "- 重製版 r2：照 `docs/videos/zhong-tian-qu-qi-e004-r2/script.md`（c01–c40 對應 s01–s40；含「2026-11-06 審稿後的修改」）；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。",
    "- 內部工作編號 904（`hailuo/*-dh-e904.json`、`colab/runs/e904/`）；發布 slug `zhong-tian-qu-qi-e004-r2`。不放集數、不放片名卡；c01 直接接第 3 集 c40（許硯蹲在灶口前，手上一根柴）。",
    "- 狀態：許硯袖子捲到手肘、捲紅紙插腰帶左邊（全集），第一場右手一根柴，s11 木勺，s13–s15 裂了縫的小鐵鍋，過場長木棍、眼睛發紅，s38–s39 兩臂抱柴；阿令沒戴鐵鐐、袖子蓋住手腕，s01–s05 短刀橫在膝上，s06 起插在腰帶左邊的深褐皮鞘；唐小棠 t2，s16–s25 抱小木匣（五錠元寶形金錠，沒有字）；二牛 s27–s28 背上倒扣大黑鐵鍋，之後兩手空空；秦霜柴刀在腰帶右邊，s31–s32 右肩扛一整頭死豬（閉眼、草繩綁腳、不見血）。",
    "- 長鏡要買的秒數（`r2.py` 的 BUY）：s03、s13、s37 8 秒（script.md 長鏡清單）；s14 12 秒、s15 10 秒（長鏡清單寫 8，錄好的兩句加停頓要 10.6、9.8 秒）；s10、s35 8 秒（錄好的配音加半秒 6.6、6.5 秒，超過預設 6 秒）。其餘照 `gen-dh` 的 6 秒，眼睛大特寫 s12、s24 5 秒。",
]
FOOT = [
    "- 場景參考：第一場灶房 `set-xujia-zao-t1`（灶火與灶台上的油燈、門外冷月光，同第 3 集）；s10–s15 屋內 `set-xujia-wu-t1`（晨光從左邊門窗斜進來）；s16–s35 院子 `set-xujia-yuan-t1`（早上暖光 → 白天右側斜光）；過場院子東側灶棚（棚柱在左、土灶與大鍋在中間、屋門在右，照第 5 集），仍用院子的場景圖。近景背景都寫「同一個灶房／屋內／院子」。",
    "- 唐小棠一律用 `tangxiaotang-portrait-t2`（gen-dh 的 PORTRAIT 對照）；近景構圖寫「下巴以上」，中景以上寫「襦裙從立領到腰一件闔上」。",
    "- 沒有定妝照的人：嬸子三人側身或背對、不拍正臉（宋式交領粗布短打、布包頭、布鞋、竹籃）；村民只在籬笆外露上半身；黑影背光、臉在暗處，不寫賴三的名字也不用 `laisan` 的圖（第 5 集才揭曉）。",
    "- 阿令沒戴鐵鐐的定妝照：`aling-portrait-t1` 本身是沒有鐵鐐的半身像，照用，不另畫（script.md 清單 2 的「要補」不用做）。",
    "- 秦霜的 `cast.json` 造型寫著「柴刀插在腰帶」：本集 s31–s34 柴刀就在腰帶右邊，`colab/runs/e904/extras.json` 不拿掉這句（第 3 集的 extras 拿掉了）。",
    "- 二牛的 `cast.json` 造型寫著「empty-handed」：s27–s28 背上倒扣大鍋，`colab/runs/e904/extras.json` 把這兩個字從造型句拿掉，手上有沒有東西改由各鏡構圖寫（s29 起「both hands empty」）。",
    "- 配樂：灶房 suspense 慢段（接第 3 集，s02「叮」抽掉）、米與金子 warm（第 1 集屋內那首，s17 開匣一個亮的重音，s24「叮」抽掉）、湊材料 comedy（s31 扛豬進門一個重音）、夜裡 tension（s40 黑影回頭一個重音）；音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy so the recorded lines (+0.5 s each) fit within buy - 0.3 s, allowing the cut's 1.1x
# slow-down (script.md 長鏡清單: c03, c13, c14, c15, c37 8 s; the rest from the recorded audio, 2026-11-06).
BUY = {"s03": 8, "s10": 8, "s13": 8, "s14": 12, "s15": 10, "s35": 8, "s37": 8}
# Recorded need (wav + 0.5 s a line, 2026-11-06): s03 7.0, s13 7.2, s37 5.9 -> the script's 8; s14 10.6 (the review's
# added inner line plus Tang Xiaotang's longer line) -> 12, and s15 9.8 -> 10, instead of the script's 8; s10 6.6 and
# s35 6.5 -> 8. Within 0.4 s of buy - 0.3 and left at 6 (the cut's 1.1x covers them): s04 6.0, s36 5.8. The lines run
# at a median 3.5 zh characters a second.
