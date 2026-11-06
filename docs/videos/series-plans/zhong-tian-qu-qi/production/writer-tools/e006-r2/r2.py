"""Episode 6 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e006-r2/script.md
(c01-c40 = s01-s40), including its section 「2026-11-06 審稿後的修改」, which overrides the tables (c01 A-ling walking to
the threshold, Xiaohe running into the house with her rabbit and Qin Shuang going to lean on the persimmon tree behind
Xu Yan; c13 one stack of red paper and one roll of red cord; c18 Qin Shuang stuffing the leftover paper and cord into
the bottom of the basket before she hooks it on; c25 the documents tucked under his left arm and c30 pulled out from
there; the knife always in the right of her belt with its black-wrapped handle and gleaming edge, c06 her hand pressing
its handle).

Same rules as e001-r2 to e005-r2: one visible action per shot written as a path, over-the-shoulder and reverse shots
for dialogue, whole sentences, one line per spoken line, default face serious (smiles only where the script allows: c13
Xiaohe, c14 Erniu's grin, c16 the beginning of Xu Yan's smile, c24 and c38-c40 the cold sneers, c32 Tang Xiaotang).
State: Xu Yan red-eyed with a few loose strands over his forehead all episode, his sleeves still rolled to the elbows
as e005 left them, one white bar of soap c01, the red cloth tied across his chest from c15, the three folded marriage
documents in his hand c18-c24 and under his left arm c25-c30, the soap basket in his right hand from c35; Tang Xiaotang
always t2 (high collar, closed garment, chin-up close-ups), the abacus on the board c01, at her chest c02-c29 and at her
waist from c30, the stamped documents folded in her arms from c32; Qin Shuang's old chopping knife in the right of her
belt all episode, never drawn, the soap basket on her arm c18-c34; A-ling without shackles, her sleeves over the red
marks, empty-handed; one small red papercut flower in each bride's hair from c15; Xiaohe's straw rabbit in her left arm
c01, c13; Erniu's one wooden-handled iron hoe on his right shoulder c14-c18 (his base look, not `pole`). No skin bits (the
script's 「手上沾皂屑」 c01 is left out: only his palms brushing together), no glow outside the eye extreme close-ups c11
and c17, no writing anywhere: the documents folded or their plain blank backs to the camera, the seal a red blot, the
notice edge-on. Opens on the next instant after e005 c40: Tang Xiaotang still gripping his sleeve by the soap board.
"""
EP = 906  # internal working number; the published slug is zhong-tian-qu-qi-e006-r2
SLUG = "zhong-tian-qu-qi-e006-r2"
EP_TITLE = "三個新娘三個條件，聘禮是三塊肥皂（重製版 r2）"
OUTLINE_SECONDS = 215  # script.md 2026-11-06: 63.5 + 32 + 82.5 + 37 s, 40 shots
TARGET_MINUTES = [3, 4]
TITLE = "三個新娘三個條件，聘禮是三塊肥皂｜種田娶妻打天下 第6集（重製版）"
DESCRIPTION = "第三天清晨，系統要許硯午時前把婚書蓋印。三個新娘各開一個條件：唐小棠要管全家的帳，秦霜夜裡去哪不准問也不准跟，阿令要分房、不准問她的過去；許硯被系統一句「反正你也沒得挑」堵住，全部答應。小禾當司儀、二牛作證，四人在院子裡拜了堂，系統卻說婚書沒蓋印不算，一家人趕到縣衙。趙捕頭要聘禮，許硯家裡什麼都沒有，低頭看到秦霜籃子裡的白皂，拿三塊包上紅紙當聘禮；趙捕頭一聞就收，午時鼓響前蓋了印，成婚三比三，良緣面板開啟：阿令 1、秦霜 5、唐小棠 10。回村路上經過縣城市集，整條街被錢員外封了：「買許家貨者，欠錢府一兩」。錢員外在茶樓上舉杯：「許秀才，明日日落見。」《種田娶妻打天下》第 6 集（重製版）"
THUMB = ("聘禮是三塊肥皂", "s27")
CHARACTERS = ["xuyan", "tangxiaotang", "qinshuang", "aling", "xiaohe", "erniu", "zhaobutou", "qianyuanwai", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: a light playful comedy of woodblock, pipa and dizi in the sunny yard, carried on through the wedding bows and stopping dead on one heavy hit when the system says it does not count; a fast tense cue of drums and erhu at the county yamen gate, one heavy hit as the seal comes down with the noon drum, turning bright after it; a low suspense cue of low cello and soft guqin on the boarded-up market street, ending on one low note; ancient Chinese rural drama, no vocals"

# Scene headers of script.md: the yard (set-xujia-yuan-t1) at sunrise and in the morning; the county yamen gate and the
# county market street have no set picture of their own in the script, so they use the season-1 pictures
# set-xianya-t1 and set-shiji-t1 (refs-dh). gen-dh maps "county yamen" to dh-set-xianya-t1 and "market street" to
# dh-set-shiji-t1; "teahouse" (one word) would map to dh-set-chalou-t1 and comes first in its table, so the market's
# two-storey building is always written "tea house". The yamen text follows the picture (the vermilion double gate with
# brass studs, two stone lions, the drum on its stand on the left) plus the script's five steps, small table and blank
# lintel; the market text follows the picture (the flagstone street, stalls both sides, the two-storey building with a
# railing on the right) with the script's boarded stalls. Axis, scene 1: the board under the persimmon tree centre left,
# the house door on the right, Xu Yan moving left to right. Wedding: Xu Yan left, the brides right, Xiaohe on the bench
# at the back in the middle, the yard gate deep on the right. Yamen: the gate at the top right of the steps, the family
# coming up from the bottom left. Market: the family entering from the left, the tea house upstairs at the upper right.
LOC = {
    "dawn": "In the dirt yard of the Xu farmhouse at sunrise on a clear autumn morning: one long wooden board on two blocks under a persimmon tree centre left with rows of white soap bars on it, the cooking shelter at the back left, one bamboo drying pole across the middle of the yard with one strip of red cloth on it, the house door on screen right, warm low sunrise light from screen left, long shadows",
    "dawn_c": "In the dirt yard of the Xu farmhouse at sunrise, warm low sunlight from screen left",
    "morn": "In the dirt yard of the Xu farmhouse on a clear autumn morning: one small wooden table in the middle of the yard, one wooden bench at the back in the middle before a persimmon tree, a bamboo fence, the yard gate in the fence deep on screen right, warm morning sunlight from screen left a little higher than at sunrise",
    "morn_c": "In the dirt yard of the Xu farmhouse in the morning, warm sunlight from screen left",
    "yamen": "At the gate of the county yamen just before noon on a clear autumn day: the vermilion double gate with brass studs half open at the top of five stone steps, two stone lions on carved plinths beside it, a plain lintel board with no writing, one big drum on a wooden drum stand by the gate on screen left with one small wooden table beside it, a flagstone forecourt, the sun overhead and short shadows under everyone's feet",
    "yamen_c": "At the vermilion gate of the county yamen at noon, bright overhead sunlight",
    "market": "On the market street of the county town on a clear autumn afternoon: a flagstone street with two rows of stalls along both sides, every stall boarded shut with nailed planks, their awnings and signboards plain and blank, one two-storey tea house on screen right with a red-lacquered railing along its upper floor, light from the upper right a little to the west, shadows falling to the left",
    "market_c": "On the market street of the county town in the afternoon, light from the upper right",
}
LIGHT = {
    "dawn": "the warm low sunrise light from the left stays unchanged",
    "morn": "the warm morning sunlight from the left stays unchanged",
    "yamen": "the bright overhead noon sunlight stays unchanged",
    "market": "the afternoon light from the upper right stays unchanged",
}

# Repeated wording (each prop is one object; the descriptions say "one" where it first appears).
XU = "his patched blue-grey scholar's robe with his sleeves rolled up to the elbows"
RED = "red-eyed and tired after a sleepless night"
HAIR = "a few loose strands of hair fallen over his forehead"
SASH = "one strip of red cloth tied diagonally across his chest"
TANG = "her peach-pink brocade ruqun one closed garment from the high stand-up collar to the waist"
CHIN = "framed from the chin up, her high stand-up collar closed at her throat"
QIN = "her dark brown cross-collared short jacket, wide leather belt, black trousers, leather boots and high ponytail"
KNIFE = "her old chopping knife in the right side of her belt"
CHOP = "her old chopping knife in the right side of her belt, its wooden handle wrapped in black cloth and its edge gleaming"
ALING = "no shackles, her sleeves pulled down over her wrists"
FLOWER = "one small red papercut flower"
HE = "little Xiaohe in her patched lilac short jacket with red-string pigtails and one front tooth missing"
ERNIU = "Wang Erniu in his coarse brown short jacket with rolled sleeves"
HOE = "one wooden-handled iron hoe"
BASKET = "one bamboo basket full of snow-white bars of soap, each wrapped in one green leaf"
SOAP = "snow-white square bars of soap, each palm-sized and one finger thick with square corners, opaque and not glowing"
DOCS = "three marriage documents, each one long strip of red paper folded shut with its plain blank back toward the camera"
ZHAO = "Constable Zhao in his black constable's hat and plain black official uniform, wiry and narrow-eyed, an iron ruler and a sword in a black scabbard on the left of his belt"
QIAN = "Qian Yuanwai, short and portly with a round face, in his dark gold roundel-patterned silk robe, three gold rings on his fingers"
CUP = "one small plain white glazed pottery cup"
PACKS = "three small packets wrapped in plain blank red paper and tied with red cord"

SHOTS = [
    # ---- scene 1: the yard at sunrise, the next instant after e005 c40, warm low light from the left. Axis: the soap
    # board centre left, Qin Shuang to the persimmon tree on the left, A-ling to the house door threshold on the right.
    dict(chapter="條件", loc="dawn", cam="Medium shot, tracking", chars=["xuyan", "tangxiaotang", "qinshuang", "aling", "xiaohe"], night="dawn",
         comp=f"medium shot past a row of white soap bars on the board in the foreground: Xu Yan in the middle, {XU}, red-eyed, one white bar of soap in his right hand; Tang Xiaotang beside him, {TANG}, her right hand gripping his sleeve, her small gold abacus on the board; behind them Qin Shuang, {KNIFE}, A-ling, {ALING}, and little Xiaohe hugging her straw rabbit",
         lines=[("xuyan", "三位，今天午時前，得跟我進縣衙蓋婚書。", "急，認真")],
         motion="Xu Yan sets the bar down, Tang Xiaotang lets go; A-ling sits at the door, Xiaohe runs in, Qin Shuang leans on the tree; he walks off brushing his palms",
         zh="中景、跟拍、前景木板上一排白皂（接第 5 集 c40）：許硯（眼睛發紅、額前散髮）把手上那塊白皂放回木板，唐小棠的手從他袖子上滑開；後面阿令走到右邊屋門檻坐下，小禾抱草兔跑回屋裡，秦霜走到左邊柿子樹下倚著；許硯轉身朝她們走過去，邊走邊拍兩下手掌（script 的「手上沾皂屑」不寫）"),
    dict(loc="dawn_c", cam="Medium close-up to close-up, slow push in", chars=["tangxiaotang"], night="dawn",
         comp=f"medium close-up, closing in to a close-up by the end, of Tang Xiaotang {CHIN}, {TANG}, her chin raised, unsmiling; behind her only the persimmon tree of the same yard",
         lines=[("tangxiaotang", "嫁可以，先講條件。往後家裡的帳，全歸我管。", "抬著下巴，不笑")],
         motion="she bends, picks the small gold abacus up off the board below the frame, straightens hugging it to her chest and lifts her chin at Xu Yan off screen right",
         zh="近景、慢推（中近景推到近景，下巴以上）：唐小棠彎腰從木板上撿起小金算盤，直起身抱在胸前，抬下巴看許硯；不笑"),
    dict(loc="dawn", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="dawn",
         comp=f"over-the-shoulder shot from behind Tang Xiaotang's looped buns and pink silk ribbons in the left foreground, {TANG}; Xu Yan on screen right, {XU}, {RED}, {HAIR}, unsmiling",
         lines=[("xuyan", "全部的帳？連我買一支筆，也要跟妳報？", "挑眉，不信")],
         motion="Xu Yan stops, points a finger at his own chest and raises one eyebrow; Tang Xiaotang's lips stay closed",
         zh="過肩（唐小棠肩後拍許硯）、慢推：前景左唐小棠的丸子頭與粉緞帶；許硯停步，伸手指了指自己的胸口，眉毛一挑"),
    dict(loc="dawn_c", cam="Over-the-shoulder close-up, slow push in", chars=["tangxiaotang", "xuyan"], night="dawn",
         comp=f"reverse over-the-shoulder shot from behind Xu Yan's shoulder in the right foreground, Tang Xiaotang on screen left {CHIN}, {TANG}, the small gold abacus hugged to her chest, shrewd and unsmiling; behind her only the persimmon tree of the same yard",
         lines=[("tangxiaotang", "一支筆兩文錢，記清楚了，才不會再欠二十兩。", "精明，不笑")],
         motion="her fingertip flicks one bead of the abacus with a click, and only then she lifts her eyes to him; Xu Yan's lips stay closed",
         zh="反打（許硯肩後拍唐小棠）、慢推（下巴以上）：唐小棠右手指尖撥一顆算珠「啪」一聲，再抬眼看他；算盤抱在胸前，不笑"),
    dict(loc="dawn", cam="Medium shot, tracking", chars=["xuyan", "qinshuang"], night="dawn",
         comp=f"medium shot of Xu Yan, {XU}, {RED}, {HAIR}, unsmiling; deep on screen left Qin Shuang leaning against the persimmon tree, {KNIFE}",
         lines=[("xuyan", "行，帳歸妳管。秦霜，換妳了，妳的條件呢？", "投降，無奈")],
         motion="Xu Yan raises both hands in surrender, lowers them, turns and walks toward Qin Shuang at the persimmon tree; her lips stay closed",
         zh="中景、跟拍：許硯舉起兩手做投降狀，放下手轉身，走向倚著柿子樹的秦霜（畫面左深處）"),
    dict(loc="dawn_c", cam="Low-angle medium close-up, slow push in", chars=["qinshuang"], night="dawn",
         comp=f"low-angle medium close-up from the roots of the persimmon tree of Qin Shuang, {QIN}, {CHOP}, unsmiling; behind her only the persimmon branches and the sky of the same yard",
         lines=[("qinshuang", "我夜裡要去哪裡，你別問，也別跟著。", "冷，不笑")],
         motion="she pushes her back off the trunk and stands straight, her right hand pressing the knife handle at her belt once, her eyes on Xu Yan off screen right",
         zh="低角度中近景、慢推（從樹根往上拍）：秦霜背離開樹幹、站直，右手按一按腰帶右邊的柴刀柄（木柄纏黑布、刃口發亮），看著許硯；不笑"),
    dict(loc="dawn", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "qinshuang"], night="dawn",
         comp=f"over-the-shoulder shot from behind Qin Shuang's shoulder and high ponytail in the left foreground, Xu Yan on screen right, {XU}, {RED}, {HAIR}, frowning",
         lines=[("xuyan", "要是妳出了事，我總得知道上哪去找妳。", "皺眉，擔心")],
         motion="Xu Yan frowns and takes one step forward toward her; Qin Shuang's lips stay closed",
         zh="過肩（秦霜肩後拍許硯）、慢推：前景左秦霜的肩與高馬尾；許硯皺眉往前一步"),
    dict(loc="dawn_c", cam="Medium close-up to close-up, slow push in", chars=["qinshuang"], night="dawn",
         comp=f"medium close-up, closing in to a close-up by the end, of Qin Shuang, {QIN}, {KNIFE}, cold and unsmiling; behind her only the persimmon tree of the same yard",
         lines=[("qinshuang", "真出了事，你也找不到。答不答應？", "冷")],
         motion="she turns her back on him, flicks her high ponytail back with one hand, then turns half her face back over her shoulder",
         zh="近景、慢推（中近景推到近景）：秦霜轉身背對許硯，抬手把高馬尾往後一甩，再側過半張臉；冷、不笑"),
    dict(loc="dawn", cam="Medium shot, tracking", chars=["qinshuang", "xuyan", "aling"], night="dawn",
         comp=f"medium shot, on screen left Qin Shuang seen from behind, {QIN}; Xu Yan in the middle, {XU}, {RED}, {HAIR}; on screen right A-ling sitting on the threshold of the house door, {ALING}, unsmiling",
         lines=[("xuyan", "好，妳夜裡去哪，我不問也不跟。", "嘆氣，點頭"),
                ("aling", "分房睡。我的過去，你一個字都不准問。", "冷，不笑")],
         motion="first Xu Yan nods and walks to the door; then A-ling rises, walks past him to the fence and looks back",
         zh="中景、跟拍（長鏡）：左邊秦霜的背影；許硯嘆一口氣、點頭，對秦霜的背影說完，往右走到門檻邊；阿令（沒戴鐵鐐）站起來，從他身邊走過去，停在籬笆前回頭；先許硯說、再阿令說"),
    dict(loc="dawn_c", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"medium close-up, closing in to a close-up by the end, of Xu Yan, {XU}, {RED}, {HAIR}, unsmiling; behind him only the persimmon tree of the same yard",
         lines=[("xuyan", "三個條件，沒有一條是對我有利的。", "心裡話，嘴閉著，累", "inner")],
         motion="he turns his head to look over the brides' backs off screen, then presses his right hand to his temple and rubs it once; his lips stay closed",
         zh="近景、慢推（中近景推到近景）：許硯轉頭看三個人各自的背影，右手按住太陽穴揉一下；心裡話，嘴閉著"),
    dict(loc="dawn_c", cam="Extreme close-up, slow push in", chars=["xuyan"], night="dawn",
         comp="extreme close-up of Xu Yan's eyes, the shot opens directly on his eyes from its very first frame, red-rimmed and tired, a very faint pale reflection in his pupils; nothing else in the frame",
         lines=[("xitong", "建議宿主答應。反正你也沒得挑。", "冷，嫌棄")],
         motion="his eyelid twitches once and his brows knit, his lips staying closed",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：瞳孔裡一點很淡的反光（不畫面板）；許硯眼皮跳一下，眉頭一皺"),
    dict(loc="dawn", cam="Full shot, slow push in", chars=["aling", "xuyan"], night="dawn",
         comp=f"full shot past the bamboo drying pole in the foreground: on screen right A-ling before the bamboo fence, {ALING}, unsmiling; in the middle Xu Yan, {XU}, {RED}, {HAIR}",
         lines=[("xuyan", "阿令，分房、不問，我都答應。小禾，拿紅紙來拜堂！", "下定決心，喊")],
         motion="Xu Yan nods to A-ling, walks to the drying pole, pulls the red cloth off it and turns to shout toward the house door on the right; A-ling turns back to the fence",
         zh="全景、慢推、前景晾衣竿（長鏡）：許硯朝籬笆前的阿令點一下頭，往院子中間走，伸手扯下晾衣竿上的一塊紅布，轉身朝右邊屋門喊；阿令轉回去看籬笆外（結尾）"),
    # ---- transition: the same yard in the morning, the light a little higher. Axis: Xu Yan left, the brides right,
    # Xiaohe on the bench at the back in the middle before the persimmon tree, the yard gate deep on the right.
    dict(chapter="拜堂", loc="morn", cam="Low-angle medium shot, slow push in", chars=["xiaohe"], night="morn",
         comp=f"low-angle medium shot of {HE}, hugging her straw rabbit in her left arm, one stack of plain blank red paper and one roll of red cord in her right hand, smiling; behind her the persimmon tree and the sky",
         lines=[("xiaohe", "一拜天地！二牛哥快進來，你是證人！", "喊，雀躍")],
         motion="Xiaohe runs out, puts the red paper and cord on the small table, climbs onto the bench and cups her hands round her mouth toward the yard gate on the right",
         zh="低角度中景、慢推：小禾（左臂抱草兔、右手拿一疊紅紙一捲紅繩）從屋裡跑出來，把紅紙紅繩放在小桌上，爬上板凳站好，兩手圈在嘴邊朝右邊院門外喊（可以笑）"),
    dict(loc="morn", cam="Medium shot, tracking", chars=["erniu"], night="morn",
         comp=f"medium shot of {ERNIU}, {HOE} on his right shoulder, grinning",
         lines=[("erniu", "我王二牛作證，許秀才今天娶三個媳婦！", "憨笑，大嗓門")],
         motion="Erniu jogs in through the yard gate with the hoe on his shoulder, stops, plants the hoe on the ground with a thud and pats his chest with his left hand",
         zh="中景、跟拍：二牛右肩扛一把木柄鐵鋤頭從院門小跑進來，站定，把鋤頭往地上一拄，左手拍拍胸口（可以憨笑）"),
    dict(loc="morn", cam="Full shot, slow push in", chars=["xuyan", "aling", "qinshuang", "tangxiaotang", "xiaohe", "erniu"], nospeak=["xiaohe"], night="morn",
         comp=f"full shot past the bamboo fence in the foreground: on screen left Xu Yan, {XU}, {SASH}; on screen right A-ling, Qin Shuang and Tang Xiaotang, {TANG}, each with {FLOWER} in her hair; at the back in the middle little Xiaohe standing on the bench, too far for her mouth to be seen; at the back right Wang Erniu leaning on his hoe",
         lines=[("xiaohe", "夫妻對拜！拜完了，就是一家人了！", "畫外，喊，雀躍（人在畫面深處，看不到嘴）")],
         motion="the four of them bow to each other together and straighten up again; Erniu nods hard beside them; all lips stay closed",
         zh="全景、慢推、前景竹籬笆：左許硯（胸前斜綁紅布）；右阿令、秦霜、唐小棠（襦裙從立領到腰一件闔上），髮上各別一朵小紅紙花；中後小禾站在板凳上（太遠、看不到嘴，台詞不對嘴）；右後二牛拄著鋤頭；四人一起彎腰對拜再直起身，二牛用力點頭"),
    dict(loc="morn_c", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"medium close-up, closing in to a close-up by the end, of Xu Yan, {XU}, {SASH}, {RED}, {HAIR}; behind him only the persimmon tree of the same yard",
         lines=[("xuyan", "堂都拜完了，這下任務總該算完成了吧？", "心裡話，嘴閉著，鬆一口氣", "inner")],
         motion="he straightens up, lets out one long breath, his shoulders drop and the corners of his mouth just begin to lift; his lips stay closed",
         zh="近景、慢推（中近景推到近景）：許硯（胸前紅布）直起身，長出一口氣，肩膀一鬆，嘴角剛要往上；心裡話，嘴閉著"),
    dict(loc="morn_c", cam="Extreme close-up, slow push in", chars=["xuyan"], night="morn",
         comp="extreme close-up of Xu Yan's eyes, the shot opens directly on his eyes from its very first frame, red-rimmed, just beginning to crease into a smile; nothing else in the frame",
         lines=[("xitong", "婚書未蓋印，不算。宿主剛才那叫彩排。", "冷")],
         motion="the eyes hold that beginning smile; only then a very faint pale red reflection appears in his pupils, and the smile stiffens and drains out of his eyes",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：眼角剛要笑，才在瞳孔裡映出一點很淡的紅色反光（不畫面板），那一點笑僵住、收掉"),
    dict(loc="morn", cam="Full shot, tracking", chars=["xuyan", "tangxiaotang", "qinshuang", "aling", "xiaohe", "erniu"], night="morn",
         comp=f"full shot, Xu Yan in the middle, {SASH}, by the small wooden table with three marriage documents of red paper folded shut on it beside leftover red paper and one roll of red cord; one bamboo basket of leaf-wrapped white soap on the ground; on the right Tang Xiaotang, {TANG}, Qin Shuang, {KNIFE}, and A-ling, each with a red papercut flower in her hair; Xiaohe on the bench and Wang Erniu with his hoe at the back",
         lines=[("xuyan", "婚書沒蓋印不算！走，現在就進縣衙！", "急，喊")],
         motion="Xu Yan grabs the documents and runs for the gate, the women after him, Qin Shuang stuffing leftover paper into her basket; Xiaohe waves",
         zh="全景、跟拍：許硯一把抓起小桌上三份摺好的婚書（紙背朝鏡頭），拉起衣襬往右邊院門跑；三個女人跟著跑，秦霜經過小桌時順手把剩下的紅紙和一捲紅繩塞進籃底，再挎起那籃白皂；小禾在板凳上揮手、二牛拄著鋤頭目送（結尾）"),
    # ---- scene 2: the county yamen gate just before noon (set-xianya-t1), the sun overhead, short shadows. Axis: the
    # gate at the top right of the five steps, Constable Zhao there all scene; the family coming up from the bottom left.
    dict(chapter="縣衙", loc="yamen", cam="High-angle full shot, tracking", chars=["xuyan", "tangxiaotang", "qinshuang", "aling", "zhaobutou"], night="yamen",
         comp=f"high-angle full shot past the drum stand and its big drum in the foreground: at the bottom Xu Yan, {SASH}, the red documents folded shut in his hand, running up the stone steps with Tang Xiaotang, {TANG}, Qin Shuang with the basket on her arm and A-ling behind him; at the top before the half-open gate Constable Zhao in his black constable's hat and black uniform",
         lines=[("zhaobutou", "站住！再一刻就是午時，縣衙要關門了。", "不耐煩")],
         motion="Xu Yan dashes up the steps with the women behind him; at the top Constable Zhao swings his iron ruler across to bar the way",
         zh="俯拍全景、跟拍、前景鼓架與大鼓：許硯（胸前紅布、手拿三份婚書）衝上石階，三個女人跟在後（秦霜挎著籃）；台階頂紅門前，趙捕頭右手把鐵尺一橫攔住"),
    dict(loc="yamen", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "zhaobutou"], night="yamen",
         comp=f"over-the-shoulder shot from behind Constable Zhao's shoulder and black constable's hat in the right foreground, Xu Yan on screen left one step below, {XU}, {SASH}, {RED}, out of breath, holding up {DOCS} in both hands",
         lines=[("xuyan", "趙捕頭，三份婚書都寫好了，就差一個官印。", "喘，急")],
         motion="Xu Yan pulls up one step below, panting, and raises the folded documents in both hands; Constable Zhao's lips stay closed",
         zh="過肩（趙捕頭肩後拍許硯）、慢推：許硯在下一階煞住，喘著氣，雙手把摺好的婚書遞上去（紅紙背面朝鏡頭）"),
    dict(loc="yamen", cam="Over-the-shoulder medium shot, slow push in", chars=["zhaobutou", "xuyan"], night="yamen",
         comp=f"reverse over-the-shoulder shot from behind Xu Yan's shoulder in the left foreground, {ZHAO} on screen right one step above, eyeing him sideways, unsmiling",
         lines=[("zhaobutou", "成親要聘禮，聘禮呢？沒聘禮，這印不能蓋。", "斜眼，公事公辦")],
         motion="Constable Zhao takes the folded documents between two fingers of his left hand, flips through their plain blank backs and looks down sideways; Xu Yan's lips stay closed",
         zh="反打（許硯肩後拍趙捕頭）、慢推：趙捕頭左手兩指夾過婚書翻了翻（紙背朝鏡頭，看不到字），斜眼往下看"),
    dict(loc="yamen_c", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="yamen",
         comp=f"medium close-up, closing in to a close-up by the end, of Xu Yan, {XU}, {SASH}, {RED}, his face pale, unsmiling; behind him only the vermilion gate of the same county yamen",
         lines=[("xuyan", "聘禮……我家米缸都快見底了，哪來的聘禮？", "臉色發白，慌")],
         motion="he pats the empty front of his robe with both hands, then turns out both cuffs and finds nothing",
         zh="近景、慢推（中近景推到近景）：許硯兩手拍拍空空的衣襟，再翻一下兩邊袖口，什麼都沒有；臉色發白"),
    dict(loc="yamen", cam="Two-shot, slow push in", chars=["tangxiaotang", "xuyan", "qinshuang"], night="yamen",
         comp=f"two-shot, Tang Xiaotang in front {CHIN}, {TANG}, {FLOWER} by her pink ribbon, leaning to Xu Yan's ear, anxious and unsmiling; Xu Yan beside her, {SASH}; behind them Qin Shuang, {KNIFE}, {BASKET} on her left arm",
         lines=[("tangxiaotang", "午時鼓就要響了，你快想辦法！", "急，壓低聲音")],
         motion="Tang Xiaotang tugs his sleeve and leans to his ear; behind, Qin Shuang grips her knife handle and steps forward, and Xu Yan presses her wrist, his hand brushing her basket",
         zh="雙人鏡、慢推（唐小棠近景下巴以上）：唐小棠扯一下他的袖子、湊到他耳邊；後面秦霜右手按住腰帶右邊的刀柄往前一步，許硯反手按住她的手腕，手背碰到她臂彎裡的竹籃；不笑"),
    dict(loc="yamen_c", cam="Low-angle close-up, slow push in", chars=["zhaobutou"], night="yamen",
         comp=f"low-angle close-up from below the steps of {ZHAO}, {DOCS} in his left hand, with a cold sneer; behind him only the vermilion gate of the same county yamen",
         lines=[("zhaobutou", "拿不出聘禮，就等期滿，自己去跟縣太爺說。", "冷笑")],
         motion="he pushes the documents down into a hand reaching up at the bottom edge of the frame, then lifts his chin",
         zh="低角度近景（從台階下往上拍）、慢推：趙捕頭把婚書往下一推，退回許硯手裡，下巴一抬（可以冷笑）"),
    dict(loc="yamen_c", cam="Medium shot to close-up, slow push in", chars=["xuyan"], night="yamen",
         comp=f"medium shot, closing in to a close-up by the end, of Xu Yan, {XU}, {SASH}, {RED}, {DOCS} in his hand; at the bottom edge of the frame {BASKET} on an arm in a dark brown sleeve; behind him only the vermilion gate of the same county yamen",
         lines=[("xuyan", "等等，聘禮我有。不是金銀，是縣城沒見過的東西。", "愣一下，眼睛一亮")],
         motion="he tucks the documents under his left arm and looks down at the basket; he freezes, and only then his eyes light up and his right hand lifts out three bars",
         zh="近景、慢推（中景推到近景，長鏡）：許硯把退回的婚書夾到左腋下，低頭看見畫面下緣秦霜臂彎竹籃裡綠葉包的白皂，愣一下，眼睛一亮，伸右手從籃裡拿起三塊"),
    dict(loc="yamen_c", cam="Insert close-up, locked", chars=["xuyan"], night="yamen", act=3,
         comp=f"insert close-up of the small wooden table by the drum stand, the shot opens directly on three white bars of soap on the table from its very first frame: three {SOAP}, three squares of plain blank red paper, one roll of red cord, and Xu Yan's two hands in his rolled-up blue-grey cuffs; only the hands, cuffs, soap and paper are in the frame, his face out of the frame; behind them only the stone steps of the same county yamen",
         lines=[],
         motion="his hands wrap each white bar in one square of red paper, tie one turn of red cord round it in a knot, and set the three red packets in a row",
         zh="手部特寫、固定（第一格就是鼓架旁小木桌上的三塊白皂）：許硯的兩手（藍灰袖口）把三塊白皂各包上一張紅紙，繞一圈紅繩打結，排成三個紅紙包（無台詞）"),
    dict(loc="yamen", cam="Two-shot, tracking", chars=["xuyan", "zhaobutou"], night="yamen",
         comp=f"two-shot, Xu Yan on screen left, {XU}, {SASH}, {PACKS} held out in both hands; {ZHAO} on screen right one step above",
         lines=[("xuyan", "三塊香皂，一位夫人一塊，請捕頭收下。", "恭敬，誠懇")],
         motion="Xu Yan steps up one stair and bows a little, holding out the packets; Constable Zhao reaches out his right hand and takes one; Zhao's lips stay closed",
         zh="雙人鏡、跟拍：許硯捧著三個紅紙包走上一階，微微彎腰遞上；趙捕頭伸右手拿起一個"),
    dict(loc="yamen_c", cam="Medium close-up to close-up, slow push in", chars=["zhaobutou"], night="yamen",
         comp=f"medium close-up, closing in to a close-up by the end, of {ZHAO}, one small packet in plain blank red paper in his right hand, unsmiling; behind him only the vermilion gate of the same county yamen",
         lines=[("zhaobutou", "這是香的？比我家婆娘的胭脂還香。", "愣住")],
         motion="he lifts the packet to his nose and sniffs, pauses, sniffs again, and only then his narrow eyes go wide",
         zh="近景、慢推（中近景推到近景）：趙捕頭把紅紙包湊到鼻下聞，停一下，再聞一次，細眼瞪大"),
    dict(loc="yamen_c", cam="Medium close-up, slow push in", chars=["tangxiaotang"], night="yamen",
         comp=f"medium close-up of Tang Xiaotang {CHIN}, {TANG}, {FLOWER} by her pink ribbon, the small gold abacus hugged to her chest, shrewd and unsmiling; behind her only the stone steps of the same county yamen",
         lines=[("tangxiaotang", "這是洗手的香皂，一塊三錢，三塊就是九錢。", "很精，報價")],
         motion="she steps forward and flicks the beads of the abacus at her chest once with her fingertips",
         zh="中近景、慢推（下巴以上）：唐小棠往前一步，把胸前的算盤一撥；不笑、很精"),
    dict(loc="yamen", cam="Medium shot, tracking", chars=["zhaobutou", "xuyan", "tangxiaotang"], night="yamen",
         comp=f"medium shot, {ZHAO} in the middle, {PACKS} in his hands; at the left edge of the frame Xu Yan, {SASH}, the documents folded shut under his left arm, and Tang Xiaotang, {TANG}, the abacus at her chest",
         lines=[("zhaobutou", "九錢的聘禮，我收了。婚書拿來，我給你們蓋印。", "收下，公事公辦")],
         motion="Constable Zhao tucks the packets into his robe, picks up one square brass seal, holds out his left hand; Xu Yan hands up the documents; Tang Xiaotang hangs up her abacus",
         zh="中景、跟拍：趙捕頭把三個紅紙包塞進懷裡，轉身從門內小桌上拿起一方銅印（右手、方形、黃銅色），轉回來伸左手要婚書；許硯從腋下抽出婚書遞上；唐小棠在左邊緣把算盤掛回腰間"),
    dict(loc="yamen_c", cam="High-angle insert close-up, locked", chars=["zhaobutou"], night="yamen",
         comp="high-angle insert close-up of the small wooden table, the shot opens directly on one opened red marriage document and one square brass seal from its very first frame: Constable Zhao's right hand in a black official cuff holding the square brass seal over the red document laid open with its plain blank back toward the camera, one wide plain red sheet with nothing on it; only the hand, cuff, seal and paper are in the frame; behind them only the flagstones of the same county yamen",
         lines=[("xitong", "強制任務完成。成婚，三比三。", "冷淡，宣布")],
         panel=[("強制任務完成／成婚 3/3", "task")],
         motion="the seal comes down hard on the red paper and lifts again, leaving one square red blot with no characters in it",
         zh="手部特寫、俯拍、固定（第一格就是攤開的紅紙與銅印）：趙捕頭的右手（黑公服袖口）把方銅印重重蓋下、再提起，空白紅紙上留下一個方形朱紅印框（印文不畫）；遠處午時鼓「咚」（音效）"),
    dict(loc="yamen", cam="Three-shot, slow push in", chars=["tangxiaotang", "qinshuang", "aling"], night="yamen",
         comp=f"three-shot at the top of the stone steps: on screen left Tang Xiaotang, {TANG}, hugging three red documents folded shut in both arms, smiling; in the middle Qin Shuang, {KNIFE}, the basket on her left arm, her face turned away; on screen right A-ling, {ALING}, looking down the steps; each with {FLOWER} in her hair",
         lines=[("xitong", "良緣面板開啟，三位夫人的好感可見。", "冷淡")],
         panel=[("良緣面板開啟／阿令 好感 1／秦霜 好感 5／唐小棠 好感 10", "panel")],
         motion="the three each step down one stair; Tang Xiaotang hugs the documents tighter, Qin Shuang shifts the basket to her right arm and A-ling lowers her eyes; all lips stay closed",
         zh="三人鏡、慢推、台階頂正午光：左唐小棠兩手抱著蓋好印、摺起的三份婚書（可以笑）；中秦霜別開臉，把竹籃換到右臂；右阿令看著石階下，垂下眼；三人髮上都別著小紅紙花，各往下走一步"),
    dict(loc="yamen_c", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="yamen",
         comp=f"medium close-up, closing in to a close-up by the end, of Xu Yan, {XU}, {SASH}, {RED}, unsmiling; behind him only the vermilion gate of the same county yamen",
         lines=[("xuyan", "阿令才一分？我還以為她開始信我了。", "心裡話，嘴閉著，失落", "inner")],
         motion="he stares at a point just before him, then his eyes slide right to A-ling off screen right, and he scratches the back of his head; his lips stay closed",
         zh="近景、慢推（中近景推到近景）：許硯（胸前紅布）看著眼前，眼睛滑向畫面右的阿令，抓了抓後腦；心裡話，嘴閉著（script 的「看著眼前的空氣」只寫反應，不寫光）"),
    dict(loc="yamen_c", cam="Medium close-up, slow push in", chars=["aling", "tangxiaotang"], nospeak=["tangxiaotang"], night="yamen",
         comp=f"medium close-up of A-ling, {ALING}, {FLOWER} by her wooden hairpin, unsmiling; behind her, soft and out of focus, Tang Xiaotang, {TANG}, on the stone steps of the same county yamen",
         lines=[("tangxiaotang", "印蓋好了，順路去市集，把這籃肥皂賣掉。", "畫外，盤算")],
         motion="A-ling senses his gaze, glances sideways at Xu Yan off screen left, then turns and walks down the stone steps first and out of the frame; all lips stay closed",
         zh="中近景、慢推：阿令察覺他在看，斜他一眼，轉身先走下石階出畫；背景虛焦唐小棠（台詞在畫外、不對嘴）（結尾）"),
    # ---- scene 3: the county market street in the afternoon (set-shiji-t1), light from the upper right, shadows to the
    # left. Axis: the family enters from the left; the tea house and Qian Yuanwai upstairs at the upper right.
    dict(chapter="市集", loc="market", cam="Full shot, tracking", chars=["xuyan", "tangxiaotang", "qinshuang", "aling"], night="market",
         comp=f"full shot past one overturned empty bamboo basket on the flagstones in the foreground: walking in from screen left Xu Yan, {XU}, {SASH}, Tang Xiaotang, {TANG}, Qin Shuang with the basket of leaf-wrapped soap on her arm, and A-ling last; about six passers-by in Song-dynasty cross-collared coarse cotton jackets, cloth head-wraps and cloth shoes, far off and out of focus, giving them a wide berth",
         lines=[("tangxiaotang", "怎麼回事？大白天的，整條街的攤子都封了？", "驚，不笑")],
         motion="Qin Shuang hands the basket to Xu Yan, who takes it in his right hand; the four walk into the street, and Tang Xiaotang stops and stares at the boarded stalls",
         zh="全景、跟拍、前景石板上翻倒的空竹籃（長鏡）：秦霜把竹籃遞給許硯，許硯右手接過；四人走進街口，阿令走在最後，唐小棠停步看著兩排釘死的攤子；路人（宋式交領粗布短打、布包頭、布鞋）遠遠繞開、虛焦"),
    dict(loc="market_c", cam="Medium shot, slow push in", chars=["xuyan"], night="market",
         comp=f"medium shot from the side of a boarded-up stall, Xu Yan, {XU}, {SASH}, the basket of leaf-wrapped soap in his right hand, before one nailed plank with one paper notice pasted on it, the notice seen almost edge-on so no writing can be read, only its edge and one red handprint showing; behind him only the boarded stalls of the same market street",
         lines=[("xuyan", "「買許家貨者，欠錢府一兩。」他連這招都想得出來。", "照著念，冷")],
         motion="Xu Yan walks up to the plank, presses the curling notice flat with his left hand and looks down at it",
         zh="中景、慢推、鏡頭在告示側面（長鏡）：許硯右手提竹籃走到木板前，左手把翹起的告示壓平，低頭看；告示幾乎側邊入鏡，只看得到紙緣與一個紅手印，字不入鏡"),
    dict(loc="market_c", cam="Close-up, slow push in", chars=["tangxiaotang"], night="market",
         comp=f"close-up of Tang Xiaotang {CHIN}, {TANG}, {FLOWER} by her pink ribbon, unsmiling; behind her only the boarded stalls of the same market street",
         lines=[("tangxiaotang", "你看茶樓上，靠著欄杆喝酒的，就是錢員外。", "壓低聲音")],
         motion="she presses the abacus at her waist and lifts her chin toward the tea house at the upper right, her eyes on Xu Yan off screen left",
         zh="近景、慢推（下巴以上）：唐小棠把腰間的算盤按緊，抬下巴朝右上的茶樓一指，眼睛看著許硯；不笑"),
    dict(loc="market", cam="Low-angle medium shot, slow push in", chars=["qianyuanwai"], night="market",
         comp=f"low-angle medium shot from the street up at the upper floor of the two-storey tea house: {QIAN}, his elbows on the red-lacquered railing, {CUP} pinched in his right hand, with a cold sneer; behind him two thin servants in Song-dynasty cross-collared coarse short jackets and cloth head-wraps standing still; he is the only portly man in the frame",
         lines=[("qianyuanwai", "聽說許秀才做了香皂？可惜啊，沒人敢買。", "拖長音，冷笑")],
         motion="Qian Yuanwai leans forward over the railing to look down, turning the cup in his fingers; the servants' lips stay closed",
         zh="低角度中景、慢推（從街上往上拍茶樓二樓）：錢員外（矮胖、深金色團花錦袍、金戒指）手肘靠著紅漆欄杆，右手捏白色小杯（寫陶杯，不寫酒杯），身子往前探、轉一轉杯子；身後兩個瘦家丁（宋式交領粗布短打、布包頭）站著不動（可以冷笑）"),
    dict(loc="market", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "qianyuanwai"], nospeak=["xuyan"], night="market",
         comp=f"over-the-shoulder shot from behind Xu Yan's shoulder and topknot in the lower left foreground, the basket of soap in his right hand; at the upper right, small behind the red-lacquered railing of the tea house, {QIAN}",
         lines=[("xuyan", "錢員外，字據寫的是三日後日落。你急什麼？", "冷靜，頂回去")],
         motion="Xu Yan sets the basket down on the flagstones and lifts his head toward the upper floor; Qian Yuanwai's lips stay closed",
         zh="過肩（許硯肩後拍茶樓上的錢員外）、慢推：許硯把竹籃往地上一放，抬頭看樓上；許硯背對鏡頭、看不到嘴（台詞不對嘴）"),
    dict(loc="market_c", cam="Low-angle medium close-up to close-up, slow push in", chars=["qianyuanwai"], night="market",
         comp=f"low-angle medium close-up, closing in to a close-up by the end, of {QIAN}, {CUP} in his right hand, the red-lacquered railing in the foreground, with a cold sneer; behind him only the upper floor of the same tea house on the market street",
         lines=[("qianyuanwai", "我不急，我就看你一天能不能變出二十兩。", "冷笑，拖長音"),
                ("qianyuanwai", "許秀才，明日日落見。", "冷笑")],
         motion="between his lines he raises the cup to the street below and drains it, pauses half a beat, and only then turns away from the railing",
         zh="低角度近景、慢推（中近景推到近景，長鏡）：錢員外把杯子朝樓下一舉，仰頭喝乾，停半拍，轉身離開欄杆；兩句之間停半拍（結尾，懸念到第 7 集）"),
]

HEAD = [
    "- 重製版 r2：照 `docs/videos/zhong-tian-qu-qi-e006-r2/script.md`（c01–c40 對應 s01–s40；含「2026-11-06 審稿後的修改」）；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。",
    "- 內部工作編號 906（`hailuo/*-dh-e906.json`、`colab/runs/e906/`）；發布 slug `zhong-tian-qu-qi-e006-r2`。不放集數、不放片名卡；c01 直接接第 5 集 c40（唐小棠還抓著許硯的袖子、許硯手上一塊白皂）。",
    "- 狀態：許硯眼睛發紅、額前散髮（全集），袖子照第 5 集捲到手肘，s01 一塊白皂，s15 起胸前斜綁紅布，s18–s24 手拿三份婚書、s25–s30 夾在左腋下，s35 起右手提竹籃；唐小棠 t2，算盤 s01 在木板上、s02–s29 抱在胸前、s30 起掛腰間，s32 起抱著蓋好印的婚書；秦霜柴刀插在腰帶右邊（全集不出鞘），s18–s34 挎竹籃；阿令沒戴鐵鐐、袖子蓋住手腕、兩手空空；s15 起三人髮上各一朵小紅紙花；小禾 s01、s13 左臂抱草兔；二牛 s14–s18 右肩扛一把木柄鐵鋤頭（基本 look，不用 `pole`）。",
    "- 皮膚上不寫小東西：script 的「手上沾皂屑」（c01 與角色表）不寫，只留拍兩下手掌；系統句只有眼睛大特寫 s11（淡反光）、s17（淡紅反光）寫瞳孔裡的光，s33 只寫反應。",
    "- 長鏡要買的秒數（`r2.py` 的 BUY）：s09 10 秒、s12、s25、s35、s36 8 秒（script.md 長鏡清單）；s40 12 秒（長鏡清單寫 8，錄好的兩句加停頓要 10.5 秒）、s38 10 秒（錢員外拖長音，錄好加半秒 8.5 秒）、s14 8 秒（6.5 秒）；s26、s31 兩個插鏡 6 秒。其餘照 `gen-dh` 的 6 秒，眼睛大特寫 s11 5 秒、s17 6 秒（兩拍動作）。",
    "- 紙一律沒有字：婚書摺著或紙背朝鏡頭，s31 蓋印只拍一片空白紅紙與方形紅印，告示 s36 側邊入鏡只見紙緣與紅手印；招牌、匾額空白。",
]
FOOT = [
    "- 場景參考：第一場與過場院子 `set-xujia-yuan-t1`（日出暖光從左 → 早上暖光稍高）；第二場縣衙門口用第一季的 `set-xianya-t1`（提示詞寫 county yamen；照圖寫朱紅大門、銅釘、兩隻石獅、左邊鼓架大鼓，加 script 的五級石階、小木桌、空白匾額），正午光、影子短；第三場市集用 `set-shiji-t1`（提示詞寫 market street；兩層樓一律寫 tea house 兩個字，寫成一個字 teahouse 會被 gen-dh 對到 `set-chalou-t1`）。近景背景都寫「同一個院子／縣衙／市集」。",
    "- script 清單 2 建議補 `set-xianya-menkou-t1`、`set-xiancheng-shiji-t1`：本集不畫新場景圖，照用第一季那兩張（交辦）。",
    "- 唐小棠一律用 `tangxiaotang-portrait-t2`（gen-dh 的 PORTRAIT 對照）；近景構圖寫「下巴以上」，中景以上寫「襦裙從立領到腰一件闔上」。",
    "- 阿令沒戴鐵鐐的定妝照：`aling-portrait-t1` 本身是沒有鐵鐐的半身像，照用，不另畫（script.md 清單 2 的「要補」不用做）。",
    "- 趙捕頭 `zhaobutou-portrait-t1`、錢員外 `qianyuanwai-portrait-t1`（gen-dh 的 DH 名單已有）；兩個家丁與路人沒有圖：宋式交領粗布短打、布包頭、布鞋，路人遠景虛焦；錢員外寫「畫面裡唯一的胖子」。錢員外手上的白瓷小酒杯寫成白色陶杯（不寫 wine cup）。",
    "- 秦霜的 `cast.json` 造型寫著「柴刀插在腰帶」：本集柴刀全集在腰帶右邊，`colab/runs/e906/extras.json` 不拿掉這句（同第 4 集）。二牛的「empty-handed」拿掉（s14–s18 扛鋤頭，同第 4 集扛鍋）。小禾的「hugging a small woven straw rabbit」照用（s01、s13 都是抱著）。",
    "- 配樂：條件與拜堂 comedy 同一首（s17「不算」音樂一頓、一個重音）、縣衙 tension 快（s31 蓋印與午時鼓一個重音後轉亮）、市集 suspense（s40 收在低音）；音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy so the recorded lines (+0.5 s each) fit within buy - 0.3 s, allowing the cut's 1.1x
# slow-down (script.md 長鏡清單: c09 10, c12, c25, c35, c36, c40 8; the rest from the recorded audio, 2026-11-06).
BUY = {"s09": 10, "s12": 8, "s14": 8, "s25": 8, "s26": 6, "s31": 6, "s35": 8, "s36": 8, "s38": 10, "s40": 12}
# Recorded need (wav + 0.5 s a line, 2026-11-06): s09 9.1 -> the script's 10; s12 6.1, s25 5.2, s35 5.1, s36 5.8 -> the
# script's 8; s40 10.5 (two drawled lines) -> 12 instead of the script's 8; s38 8.5 (Qian Yuanwai's drawl: the first take
# ran 10.6 s for 18 characters and was re-recorded once, 8.0 s) -> 10; s14 6.5 -> 8. s26 (the wordless insert) and s31
# (the system line over the seal insert, 3.0) would get gen-dh's 5 and are bought at 6 like every other shot. Within
# 0.4 s of buy - 0.3 and left at 6 (the cut's 1.1x covers them): s02 6.0, s03 5.7, s05 5.7, s15 5.7, s21 5.8, s28 5.9.
# The eye extreme close-up s11 needs 3.0 and gets gen-dh's 5; s17 needs 3.6 and gets gen-dh's 6 (its motion has two
# beats: the smile, then the red reflection, as e005 s36). The lines run at a median 3.7 zh characters a second.
