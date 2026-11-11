"""Episode 7 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e007-r2/script.md
(c01-c25, c25b, c25c, c26-c37 = s01-s25, s25b, s25c, s26-s37), including its sections 「這版改了什麼」 and 「2026-11-06 審稿後
的修改」, which override the tables (c06 「綢緞莊後巷的太太們只在早上開後門，不逛市集。」; c23 「前天夜裡」; c25 split into c25
the escape, c25b 「秦霜，城南悅來客棧天天要用，妳推二十塊去問問。」 and c25c the money box; c26 the inn servant setting the
empty basket back on the cart; the queue about twenty, the front eight sharp; the lintels, lanterns and boards blank).

Live action from the first draft (owner 2026-11-11: 「之後都用真人版」). This spec writes in what e004-e006 live paid for in
reshoots (route-a.md 2026-11-07 to 11-11, e905-live and e906-live fix specs, e906-live pick-review.md and cut-review*.md):
- Qin Shuang's blade: written as a "firewood machete" only where the script uses it (c07 she sheathes it, c10 she pats
  its handle); every other shot of hers says both her hands empty and no blade, no knife, no scabbard and no weapon
  anywhere in the frame, and her close shots are framed from the chest up so her belt is out of the frame.
- The soap: one phrase, a flat square white bar, palm-sized and one finger thick, flat like a small tile; baskets add no
  rolls and no cylinders (e905/e906: bars drawn as rolls, cabbages and long bricks).
- Every spoken line faces its listener (build-r2.py's gaze clause); every single face is three-quarter or profile toward
  someone named off screen, never the lens; every visible face written part by part with no smile word except the ban
  NOSMILE (c13 Xu Yan, c22 Tang Xiaotang and c24 Lai San's fawning grin are the script's allowed smiles, written as face
  movements). Tang Xiaotang's costume is the portrait's (TANG, as e004/e005: no collar sentence, which pilot.py refuses;
  the script's 「t2 高立領」 is the CG costume); her cool face is TANG_COOL.
- At most three named people on screen; the queue, the servant girl, the lady's hands and the inn servant have no
  picture and are written with Song-dynasty clothing. Sun Zhanggui is unnamed in c15 (a tiny out-of-focus figure, so no
  portrait is sent), a hand only in c32 (he speaks off screen), and pictured from c33.
- No writing anywhere: the red back door's lintel board blank, no lanterns, no signboards, the money box, abacus and
  ingot plain with no marks. The system panels are overlays (c01, c14, c25c, c30).
- Inserts open directly on their subject; the three eye extreme close-ups (c03, c30, c37) are e906 fix1's frame-filling
  two eyes with natural dark brown irises and a tiny catchlight (the script's 「瞳孔裡映著淡藍光」 draws glowing irises,
  an ERROR in preflight-prompts.py); a speaker who stands (c35) has headroom written; no "leans over" or "bends down".
- The axis is kept where the script's shoulders crossed it: scene 1 Xu Yan on the left at the cart and Tang Xiaotang
  on the right (she comes out of the house door on the right), so c05 is from behind her LEFT shoulder (right foreground,
  Xu Yan screen left) and c06 from behind his RIGHT shoulder (left foreground, Tang screen right); the script wrote both
  the other way round. Scenes 2-3 follow the script (table and Xu Yan on the left, Tang, Qin Shuang and Sun Zhanggui on
  the right).
State: Xu Yan rested (no red eyes, no loose strands, no red sash: a night has passed since e006), his robe with one small
elbow patch and both shoulders whole; Tang Xiaotang's abacus tied at her waist from c04, on the table from c13; Qin
Shuang's basket on her right shoulder c07-c10, the 20-bar basket onto the cart c25b, the cart and one empty basket back
c26; A-ling (no shackles) and Xiaohe (straw rabbit) only in c01. Opens the next morning after e006 c40 (the script: a
night has passed, the yard's first light tells it; nothing of e006 is re-told).
The back lane is written "the lane behind the county silk shop", which gen-dh maps to set-chouduan-t1 (drying silk on
poles, flagstones, a back gate); never "back alley" (set-xiaoxiang-t1, a night lane) or "teahouse" (set-chalou-t1): the
lane's tea stall is "tea stall". set-chouduan has no live-action picture yet (refs-live), nor has sunzhanggui: pilot.py
stops on those shots until the owner has them drawn.
"""
EP = 907  # internal working number; the published slug is zhong-tian-qu-qi-e007-r2
SLUG = "zhong-tian-qu-qi-e007-r2"
EP_TITLE = "市集封了走後巷，日落前賺到十八兩（重製版 r2）"
OUTLINE_SECONDS = 194  # script.md 2026-11-06: 53.5 + 82 + 58.5 s, 39 shots
TARGET_MINUTES = [3, 4]
TITLE = "市集封了走後巷，日落前賺到十八兩｜種田娶妻打天下 第7集（重製版）"
DESCRIPTION = "第四天天剛亮，系統下任務：今日日落前還清二十兩。市集被錢員外封了，許硯不知道去哪裡賣，系統還嫌他問錯對象；唐小棠說錢員外封得了攤子、封不了後門，一家人推車進縣城，到綢緞莊後巷敲有錢太太的後門：「洗一次，不香不要錢。」第一家夫人一口氣要二十塊，後巷排起長隊；賴三混在人群裡喊「這肥皂會爛手」，唐小棠當場洗手給大家摸，秦霜把他揪出來，許硯認出他就是前天夜裡攪了一夜鍋的賴三。秦霜推一筐去城南悅來客棧談下整批，已賺十八兩、還差二兩。太陽偏西時，在巷口看了一整天的魏記商行孫掌櫃放下一錠大銀：五十兩，買肥皂的方子。唐小棠一聽「魏記」就轉身藏起臉；系統冷冷地問：賣方子，還是賭日落？《種田娶妻打天下》第 7 集（重製版）。"
THUMB = ("五十兩買方子", "s36")
CHARACTERS = ["xuyan", "tangxiaotang", "qinshuang", "aling", "xiaohe", "laisan", "sunzhanggui", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: a light playful comedy of woodblock, pipa and dizi in the farmhouse yard at first light; an upbeat bustling market cue of pipa, yangqin and light hand drums in the sunny silk shop lane, dropping out dead when a man shouts in the queue and coming back on one bright hit as the washed hands are raised; a low suspense cue of low cello and soft guqin in the late afternoon lane, one heavy hit as the silver ingot lands on the table, ending on one low note; ancient Chinese rural drama, no vocals"

# Scene headers of script.md. Scene 1: the Xu yard (set-xujia-yuan-t1) at first light, the yard gate on screen left, the
# house door on screen right, the handcart in the middle with its shafts toward the gate, light from the left. Scenes 2-3:
# the lane behind the county silk shop (no set of its own in the script; gen-dh's "silk shop" -> set-chouduan-t1), the
# small table and Xu Yan on screen left, the red back door on screen right, the mouth of the lane deep in the background
# with its stone mounting block and a thatched tea stall; morning bands of sun from above, then the low orange sun of the
# late afternoon from the mouth of the lane, shadows stretching toward the camera. Close shots use the short `_c` headers
# and end on a same-place background.
LOC = {
    "dawn": "In the dirt yard of the Xu farmhouse at first light on a clear autumn morning: the yard gate in the bamboo fence on screen left, the house door on screen right, one wooden handcart with two spoked wheels and two long shafts standing in the middle of the yard with its shafts toward the gate, a woodpile by the fence at the back left, two hens pecking by the fence, dew on the packed earth, pale gold early-morning light from screen left, long soft shadows",
    "dawn_c": "In the dirt yard of the Xu farmhouse at first light, pale gold early-morning light from screen left",
    "lane": "In the lane behind the county silk shop on a clear autumn morning: one red-painted back door in a whitewashed wall on screen right under a plain blank lintel board, no lanterns, bamboo poles along the walls hung with lengths of plain-dyed silk drying in the air, a flagstone lane, one small plain wooden table with a wooden stool behind it on screen left, the mouth of the lane deep in the background with one stone mounting block and one thatched tea stall, sunlight slanting down into the lane from above in bright bands across the flagstones",
    "lane_c": "In the lane behind the county silk shop in the morning, bands of sunlight from above, plain-dyed silk drying behind",
    "dusk": "In the lane behind the county silk shop in the late afternoon: the small plain wooden table on screen left, lengths of plain-dyed silk drying on bamboo poles, the flagstone lane empty of customers, the mouth of the lane deep in the background with its stone mounting block, the low orange afternoon sun shining in from the mouth of the lane, long shadows stretching toward the camera",
    "dusk_c": "In the lane behind the county silk shop in the late afternoon, the low orange sun from the mouth of the lane",
    # Shorter headers for the busy medium and over-the-shoulder shots (as e006's `_m`), so the composition stays readable.
    "dawn_m": "In the dirt yard of the Xu farmhouse at first light: the yard gate in the bamboo fence on screen left, the house door on screen right, the wooden handcart in the middle, pale gold early-morning light from screen left",
    "lane_m": "In the lane behind the county silk shop in the morning: the red back door on screen right under a blank lintel board, plain-dyed silk drying on bamboo poles, flagstones, the mouth of the lane deep behind, bands of sunlight from above",
    "dusk_m": "In the lane behind the county silk shop in the late afternoon: plain-dyed silk drying on bamboo poles, flagstones, the mouth of the lane deep behind, the low orange sun from there and long shadows toward the camera",
}
LIGHT = {
    "dawn": "the pale gold early-morning light from the left stays unchanged",
    "lane": "the bands of morning sunlight from above stay unchanged",
    "dusk": "the low orange afternoon sun from the mouth of the lane stays unchanged",
}

# Repeated wording (each prop is one object; the descriptions say "one" where it first appears).
# Xu Yan: e906-live's robe phrase (both shoulders whole: the e904 cut review's torn shoulder), rested after a night's sleep.
XU = "his faded blue-grey scholar's robe with one small sewn cloth patch at one elbow and both shoulders whole, rested and clear-eyed"
# Tang Xiaotang: the portrait's costume (owner's lock 2026-11-08), as e004/e005; close shots framed from the chest up.
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
CHEST = "framed from the chest up with space above her head"
# e906 fix2/fix4: a concrete cool face, never "unsmiling" alone.
TANG_COOL = "cool and businesslike: brows level, eyes steady, lips pressed flat between words, no teeth at any moment"
ABACUS = "one small gold abacus no longer than her hand, plain with no marks or writing"
QIN = "her dark brown cross-collared short jacket, wide leather belt, black trousers, leather boots and high ponytail"
# e906 fix1/fix3/fix5: the only wording that kept the blade out of her hand.
EMPTY = "both her hands empty, no blade, no knife, no scabbard and no weapon anywhere in the frame"
# e905 fix1: "chopping knife" drew a square cleaver; c07 and c10 are the only shots that use it.
MACHETE = "her old firewood machete (a long narrow iron blade with a slightly hooked tip, black-cloth-wrapped wooden handle)"
ALING = "no shackles, her sleeves pulled down over her wrists"
HE = "little Xiaohe in her patched lilac short jacket with red-string pigtails and one front tooth missing"
LAI = "his grey-brown Song-dynasty cross-collared short jacket and old cloth head-wrap pulled down to his eyebrows"
LAI_PULLED = "his grey-brown Song-dynasty cross-collared short jacket, his old cloth head-wrap yanked askew so his eyebrows show"
SUN = "Sun Zhanggui, a lean man in his forties with a long narrow face, hollow cheeks and a thin grey-streaked beard, in a Song-dynasty green satin cross-collared robe, one green jade ring on his right thumb, both hands otherwise empty"
# The soap (script: 雪白方塊，掌心大、一指厚，邊角方正，每塊用一片綠葉包著), e905/e906-live's flat-tile phrase.
SOAP = "one flat square white bar of soap, palm-sized and one finger thick, flat like a small tile, wrapped in one green leaf with the white soap showing, plain with no marks or writing"
SOAP_BARE = "one flat square white bar of soap, palm-sized and one finger thick, flat like a small tile, plain with no marks or writing"
BASKET = "one bamboo basket no wider than her shoulders, full of flat square white bars of soap, each palm-sized and one finger thick, flat like a small tile, each wrapped in one green leaf, no rolls and no cylinders"
CRATE = "one plain wooden crate with its lid shut, no marks or writing"
CASHBOX = "one small wooden money box with a lid, as wide as a palm is long, plain wood with no marks or writing"
PURSE = "one cloth money pouch tied with a drawstring"
SILVER = "small lumps of plain broken silver"
INGOT = "one big silver yuanbao ingot shaped like a boat, as long as two palms side by side, plain silver-white with no marks or writing"
# The extras have no picture: their clothing carries the dynasty (route-a.md 2026-11-07: modern clothes otherwise).
MAID = "one young servant girl of fifteen in a Song-dynasty pale green cotton cross-collared jacket, her hair in two small side buns"
LADIES = "young women in plain-coloured Song-dynasty cross-collared silk jackets and long skirts, each holding one wooden washbasin"
LADY = "one young woman in a plain-coloured Song-dynasty cross-collared silk jacket holding one wooden washbasin"
PORTER = "one inn servant, a man in a Song-dynasty grey cotton cross-collared short jacket and a cloth head-wrap, seen only from behind"
# e906 fix1 s11: the eye extreme close-up that held (no glowing irises, no nose and mouth to double).
EYES = "extreme close-up filling the whole frame edge to edge with only Xu Yan's two eyes and brows, no nose and no mouth in the frame, the shot opens directly on his eyes from its very first frame, natural dark brown irises with a tiny catchlight, his gaze slightly off to screen left and never into the lens"
# e001 live fix6: the only smile word on a face that must not smile.
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"

SHOTS = [
    # ---- scene 1: the yard at first light (a night after e006 c40), light from the left. Axis: the gate on the left,
    # the house door on the right, the cart in the middle; Xu Yan on the left of the cart, Tang Xiaotang from the right.
    dict(chapter="出門", loc="dawn", cam="Wide shot, slow push in", chars=["xuyan", "aling", "xiaohe"], night="dawn",
         comp=f"wide shot past the bamboo fence and two hens in the foreground, everyone small in the frame: in the middle beside the handcart Xu Yan, {XU}, holding {BASKET.replace('her shoulders', 'his shoulders')} in both arms, {CRATE} already on the cart; his face in profile toward the cart, brows drawn together, lips closed; on screen right at the house door A-ling in her grey-white cotton dress, {ALING}, holding the hand of {HE}, who hugs her straw rabbit in her left arm; three people in the yard",
         lines=[("xitong", "任務：今日日落前，還清二十兩。", "冷，宣布")],
         panel=[("任務：今日日落前還清二十兩", "task")],
         motion=f"Xu Yan heaves the basket up onto the handcart and slides it beside the crate; at the house door A-ling squats to straighten Xiaohe's collar, takes her hand and leads her in through the door out of sight; two hens strut across the foreground; all lips stay closed",
         zh="全景、慢推、前景籬笆與兩隻雞：許硯（睡過一夜、不再紅眼）兩手抱一筐綠葉包的扁方白皂，扛上推車推到蓋著蓋的木箱旁；右邊屋門口阿令（沒戴鐵鐐）蹲下幫小禾（抱草兔）拉好衣領，牽她轉身進屋、離開畫面；兩隻雞從前景走過；畫面上的人都嘴閉著；系統念任務（面板）"),
    dict(loc="dawn_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"medium close-up of Xu Yan beside the handcart, framed from the chest up with space above his head, {XU}, both hands gripping a hemp rope drawn across the loaded basket, his face three-quarter to screen right toward the cart, never the lens; frustrated: brows knitted hard, eyes narrowed, lips pressed shut, jaw clenched; behind him only the woodpile of the same yard",
         lines=[("xuyan", "市集都被封了，你倒是說說，我該去哪裡賣？", "心裡話，嘴閉著，煩躁，問系統", "inner")],
         motion=f"he loops the hemp rope over the basket, braces one foot on the cart wheel and hauls the rope tight with one hard jerk, his head staying in the frame; his lips stay closed; {NOSMILE}",
         zh="近景、慢推（中近景推到近景）：許硯皺眉，兩手拉麻繩繞過竹筐，腳蹬車輪用力一勒；心裡話，嘴閉著。live：胸口以上頭上留空、四分之三側臉、不看鏡頭；煩躁逐部位寫（眉頭擰、瞇眼、嘴抿死、咬牙）"),
    dict(loc="dawn_c", cam="Extreme close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"{EYES}; his brows drawn together",
         lines=[("xitong", "宿主問錯對象了。本系統不負責擺攤。", "冷，懶得理")],
         motion="his eyes blink once and his brows knit tighter; nothing else moves",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：許硯眼睛一眨，眉頭擰得更緊。live：稿子的「瞳孔映淡藍光」不寫（真人版會畫成發光的藍瞳，preflight 擋），改第 6 集 fix1 的寫法：滿框只有兩隻眼與眉、深棕虹膜、一點眼神光、視線略偏畫左不看鏡頭"),
    dict(loc="dawn_m", cam="Medium shot, tracking", chars=["tangxiaotang", "xuyan"], night="dawn",
         comp=f"medium shot, both framed from the waist up with space above their heads: on screen right Tang Xiaotang {TANG}, stepping out of the house door with {ABACUS} in her hands, her face three-quarter to screen left toward Xu Yan, never the lens; {TANG_COOL}; on screen left by the handcart Xu Yan, {XU}, hauling on the hemp rope, his face in profile toward the cart, brows knitted, lips closed",
         lines=[("tangxiaotang", "別跟繩子賭氣了。錢員外封得了攤子，封不了後門。", "平靜，精明，不笑")],
         motion=f"Tang Xiaotang walks from the house door to the cart tying the abacus onto her waist sash, stops beside Xu Yan and presses her right hand down on the tight rope knot; Xu Yan's lips stay closed; {NOSMILE}",
         zh="中景、跟拍（長鏡）：唐小棠從畫右屋門走出來，邊走邊把小金算盤繫上腰帶，走到推車邊，伸右手按住勒得死緊的繩結；許硯在左邊推車旁拉繩、嘴閉著；不笑。live：服裝照定妝照（交領短襦闔上、百褶裙，稿子的 t2 高立領是 CG 服裝）；唐小棠四分之三朝畫左的許硯、不看鏡頭；冷靜公事公辦：眉平、眼神穩、字句之間嘴抿平、不露齒"),
    # Axis kept: Tang Xiaotang came in on the right, so from behind her LEFT shoulder (right foreground), Xu Yan on the left
    # (the script put her in the left foreground, across the line from c04).
    dict(loc="dawn_m", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="dawn",
         comp=f"over-the-shoulder medium shot from behind Tang Xiaotang's left shoulder: her shoulder and the back of her head with its two looped buns and pink silk ribbons in the right foreground, her face out of the frame; Xu Yan on screen left by the handcart, framed from the chest up with space above his head, {XU}, the hemp rope still in his hands, his face three-quarter to screen right toward her, never the lens; doubtful: one brow raised, eyes narrowed on her, lips pressed between words",
         lines=[("xuyan", "後門？妳是說，挨家挨戶去敲人家的後門？", "不信，挑眉")],
         motion=f"Xu Yan straightens up from the cart, the rope slackening one loop in his hands, and turns his head to her; Tang Xiaotang's lips stay closed; {NOSMILE}",
         zh="過肩（唐小棠肩後拍許硯）、慢推：許硯直起腰，手上的繩子鬆了一圈，轉頭看她；挑眉不信。live：軸線——c04 唐小棠在畫右、許硯在畫左，稿子寫「前景左：唐小棠」會越軸，改從她左肩後拍（肩與丸子頭在畫右前景、臉不入鏡），許硯在畫左、四分之三朝她、不看鏡頭"),
    dict(loc="dawn_c", cam="Over-the-shoulder medium close-up, slow push in", chars=["tangxiaotang", "xuyan"], night="dawn",
         comp=f"reverse over-the-shoulder medium close-up from behind Xu Yan's right shoulder: his shoulder and topknot in the left foreground, his face out of the frame; Tang Xiaotang on screen right {CHEST}, {TANG}, her right hand resting on the basket of soap on the cart at the bottom edge, her face three-quarter to screen left toward him, never the lens; {TANG_COOL}; behind her only the house wall of the same yard",
         lines=[("tangxiaotang", "綢緞莊後巷的太太們只在早上開後門，不逛市集。", "精明，篤定")],
         motion=f"she draws {SOAP} out of the basket, peels back one corner of its green leaf and holds it up between them at chest height; Xu Yan's lips stay closed; {NOSMILE}",
         zh="反打（許硯肩後拍唐小棠）、慢推（胸口以上）：唐小棠從竹筐抽出一塊扁方白皂，剝開一角綠葉，舉到兩人中間；不笑。live：軸線同 c05，改從許硯右肩後拍（肩在畫左前景），唐小棠在畫右（稿子寫反）；下巴以上改胸口以上（pilot.py 的真人版服裝）；白皂一律「扁方、掌心大、一指厚、像小磁磚」"),
    # The first of the two shots that use the blade (the script: she sheathes it). From c08 on it stays sheathed or out of
    # the frame.
    dict(loc="dawn_m", cam="Low-angle medium shot, slow push in", chars=["qinshuang"], night="dawn",
         comp=f"low-angle medium shot from beside the handcart wheel of Qin Shuang by the woodpile, framed from the knees up with clear space above her head, {QIN}, {MACHETE} held blade-down in her right hand just above the right side of her belt, one freshly split log at her feet beside {BASKET} on the ground, her face three-quarter to screen right toward Tang Xiaotang and Xu Yan off screen right, never the lens; cool and sceptical: brows level and low, eyes narrowed, lips pressed thin between words, jaw set",
         lines=[("qinshuang", "買的人怕欠錢府一兩，你送上門，他們就不怕了？", "冷，不以為然")],
         motion=f"Qin Shuang slides the machete blade-down into the right side of her wide leather belt, where it stays to the last frame, then grips the basket by its rim with both hands and swings it up onto her right shoulder, her head staying in the frame; {NOSMILE}",
         zh="低角度中景、慢推（從推車輪子邊往上拍）：秦霜在柴堆邊，右手把剛劈完柴的柴刀刀刃朝下插回腰帶右邊，再兩手抓起腳邊的竹筐甩上右肩；冷、不以為然。live：這是稿子真的要用刀的兩鏡之一，刀寫成第 5 集 fix1 的「舊柴刀（窄長鐵刃、刃尖微勾、木柄纏黑布）」，插回後寫「留在腰帶到最後一格」；膝以上、頭上留空；不寫彎腰（改「抓起甩上肩、頭留在畫面裡」）"),
    dict(loc="dawn_c", cam="Close-up, slow push in", chars=["tangxiaotang"], night="dawn",
         comp=f"close-up of Tang Xiaotang {CHEST}, {TANG}, {SOAP} in her right hand at chest height, her face three-quarter to screen left toward Qin Shuang off screen left, never the lens; {TANG_COOL}; behind her only the house wall of the same yard",
         lines=[("tangxiaotang", "不算買，算試洗。洗一次，不香不要錢。", "篤定，不笑")],
         motion=f"she lifts the bar toward Qin Shuang off screen left and gives it one small shake, then lowers it out of the bottom of the frame into the basket and pats the basket once; {NOSMILE}",
         zh="近景、慢推（胸口以上）：唐小棠把白皂舉到畫左外的秦霜眼前晃一下，再放回竹筐、拍一拍；篤定、不笑。live：四分之三朝畫左的秦霜、不看鏡頭；TANG_COOL＋NOSMILE"),
    dict(loc="dawn_m", cam="Medium shot, tracking", chars=["xuyan", "tangxiaotang"], night="dawn",
         comp=f"medium shot, both framed from the waist up with space above their heads: Xu Yan, {XU}, gripping both long shafts of the loaded handcart, the crate and the basket of soap on it, his face three-quarter to screen right toward Tang Xiaotang beside the cart, never the lens; decided: brows level, eyes steady on her, lips firm between words; Tang Xiaotang {TANG} walking beside the cart, {ABACUS} tied at her waist, her face in profile toward him; {TANG_COOL}",
         lines=[("xuyan", "先洗再付……好，就照妳說的，現在出發。", "想通，下定決心")],
         motion=f"Xu Yan pushes the handcart forward toward the yard gate on screen left and its wheel bumps once over the threshold; Tang Xiaotang walks alongside, her lips closed; {NOSMILE}",
         zh="中景、跟拍：許硯兩手握住推車把手往畫左院門推，車輪壓過門檻顛一下；唐小棠走在車旁、嘴閉著。live：許硯四分之三朝車旁的唐小棠說話、不看鏡頭；唐小棠服裝照定妝照"),
    # The second blade shot (the script: she pats its handle); sheathed, the blade staying in its sheath.
    dict(loc="dawn_m", cam="Wide shot, tracking", chars=["xuyan", "tangxiaotang", "qinshuang"], night="dawn",
         comp=f"wide shot through the open yard gate, the gate frame in the foreground, everyone small in the frame: Xu Yan, {XU}, pushing the loaded handcart out through the gate onto the dirt village road; Tang Xiaotang {TANG} walking on the far side of the cart, lips closed; on the near side Qin Shuang, {QIN}, the basket of soap on her right shoulder, {MACHETE} sheathed in the right side of her belt with only its black-cloth-wrapped handle showing, her face in profile toward Xu Yan, never the lens; cool and dry: brows level, eyes narrowed ahead, lips pressed thin between words",
         lines=[("qinshuang", "路上誰敢攔，我先跟他好好講講道理。", "冷，護短")],
         motion=f"the handcart rolls out of the yard gate onto the village road; Qin Shuang's free left hand pats the black-wrapped handle at her right hip once, the blade staying in its sheath, and she walks on; Xu Yan and Tang Xiaotang's lips stay closed; {NOSMILE}",
         zh="全景、跟拍、前景院門框：推車出院門上村路；唐小棠在車的另一邊；秦霜右肩扛竹筐走在近側，左手拍一拍插在腰帶右邊的柴刀柄（刀留在鞘裡）；嘴在說話，其他人嘴閉著（結尾）。live：稿子要的拍刀柄照寫，刀只露纏黑布的柄、刃不出鞘"),
    # ---- scene 2: the lane behind the county silk shop, morning to near noon, bands of sun from above. Axis: the small
    # table and Xu Yan on screen left, the red back door on screen right, the mouth of the lane deep in the background;
    # Tang Xiaotang at the table's right end (middle), Qin Shuang at the far end toward the mouth of the lane.
    dict(chapter="後巷", loc="lane", cam="Wide shot, tracking", chars=["tangxiaotang"], night="lane",
         comp=f"wide shot past lengths of drying silk in the foreground: Tang Xiaotang {TANG} walking through the hanging silk toward the shut red back door on screen right, {SOAP} in her right hand, her face in profile toward the door, never the lens; {TANG_COOL}; the only other person is the servant girl who will open the door, {MAID}",
         lines=[("tangxiaotang", "姐姐，我們是柳溪村許家，送肥皂來給夫人試洗。", "客氣，有禮")],
         motion=f"Tang Xiaotang parts the drying silk, steps up to the red back door and raps on it three times with her knuckles; the door opens a crack and the servant girl leans half out, her lips closed; {NOSMILE}",
         zh="全景、跟拍、前景晾著的綢布（長鏡）：唐小棠撥開晾著的綢布走到紅色後門前，屈指敲三下；門開一條縫，丫鬟探出半身（宋式淡青交領布衫、雙丫髻）、嘴閉著；門楣空白、沒有燈籠。live：場景寫 the lane behind the county silk shop（gen-dh 對到 set-chouduan-t1，不寫 back alley）；丫鬟沒有參考圖、寫明朝代服裝"),
    dict(loc="lane_c", cam="Insert close-up, locked", chars=[], night="lane", act=3,
         comp=f"insert close-up, the shot opens directly on two hands rubbing {SOAP_BARE} in a wooden washbasin of clear water from its very first frame: two slender hands of a lady, one white jade bangle on the left wrist, pale lilac silk cuffs; the basin held at its rim by the servant girl's two hands in pale green cotton cuffs at the bottom edge; only the hands, cuffs, basin, soap and water are in the frame, no face; behind them only the drying silk of the same silk shop lane",
         lines=[],
         motion="the hands rub the soap and thick white lather swells up over the rim of the basin, a few bubbles drifting up into a band of sunlight",
         zh="手部特寫、固定（第一格就是木盆裡搓皂的手）：夫人的兩手（白玉鐲、淡紫綢袖口）在丫鬟端著的木盆裡搓白皂，泡沫漫過盆沿，泡泡飄進陽光；臉不入鏡（無台詞）"),
    # Xu Yan may smile here (the script); written as face movements.
    dict(loc="lane_m", cam="Medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="lane",
         comp=f"medium shot by the small table, all framed from the waist up with space above their heads: on screen left Xu Yan sitting behind the table, {XU}, {CASHBOX} on the table at his hand, his face three-quarter to screen right toward Tang Xiaotang, never the lens; in the middle Tang Xiaotang {TANG}, holding in both arms one tied bundle of twenty flat square white bars of soap, four layers of five, bound with hemp string; {TANG_COOL}; on screen right {MAID}, seen from behind, her back to the camera, one heavy {PURSE} in her hand",
         lines=[("xuyan", "她家夫人一口氣要二十塊，錢都先付了。", "壓低聲音，忍不住高興")],
         motion="the servant girl presses the heavy money pouch into Xu Yan's palm, takes the tied bundle of soap from Tang Xiaotang's arms and carries it back through the red door; Xu Yan weighs the pouch once in his hand, his eyes bright and the corners of his mouth rising, and turns his face to Tang Xiaotang; Tang Xiaotang's lips stay closed",
         zh="中景、慢推（稿子寫中近景，三個人入鏡改中景、腰以上）：丫鬟（背影）把沉甸甸的布錢袋塞進許硯手心，再從唐小棠手上接過一疊麻繩捆好的二十塊白皂（四層、每層五塊）抱回門裡；許硯掂一下錢袋、轉頭看唐小棠（本鏡可以笑：只寫眼睛發亮、嘴角上揚）；唐小棠冷靜、嘴閉著"),
    dict(loc="lane_c", cam="Close-up, slow push in", chars=["xuyan"], night="lane",
         comp=f"close-up of Xu Yan behind the small table, framed from the chest up with space above his head, {XU}, the cloth money pouch in his right hand above {CASHBOX} with its lid open at the bottom edge, his face three-quarter to screen right, his eyes on the money box, never the lens; quietly relieved: brows easing, eyes steady, lips closed; behind him only the drying silk of the same silk shop lane",
         lines=[("xitong", "已賺，六兩。", "冷淡，報數")],
         panel=[("已賺 6 兩", "panel")],
         motion=f"he drops the money pouch into the money box, shuts the lid and rests his hand flat on it; his lips stay closed; {NOSMILE}",
         zh="近景、慢推：許硯把錢袋放進木錢箱、蓋上蓋子，手按在蓋上；嘴閉著；系統報數（面板）"),
    # Sun Zhanggui is a tiny unnamed figure here (no portrait sent): the script's 虛焦 in the tea stall.
    dict(loc="lane_m", cam="Wide shot, slow push in", chars=["tangxiaotang"], night="lane",
         comp=f"wide shot past the rim of one wooden washbasin in the foreground, everyone small in the frame: a queue of about twenty {LADIES}, stretching from the small table on screen left back to the mouth of the lane, the front eight sharp and the rest soft and out of focus; behind the table Tang Xiaotang {TANG}, a row of flat square white bars of soap on the table before her, her face in profile toward the queue, never the lens; {TANG_COOL}; far away at the mouth of the lane under the thatched tea stall one lean seated man in a green robe, tiny, soft and out of focus, watching",
         lines=[("tangxiaotang", "一人一塊，別擠。洗過不香的，盆拿回來退錢。", "俐落，招呼")],
         motion=f"the queue shuffles forward; Tang Xiaotang hands out one flat white bar after another and takes small lumps of silver in return; a few soap bubbles drift through the sunlight; every other lip stays closed; {NOSMILE}",
         zh="全景、慢推、前景木盆盆沿：約二十位捧木盆的小姐（宋式素色交領綢衫）排到巷口，前八人入鏡、後面虛焦；唐小棠在桌後一塊塊遞出白皂、收碎銀；泡泡在陽光裡飄；巷口茶棚下一個穿綠袍的瘦長身影（孫掌櫃，虛焦、不點名，不送他的參考圖）坐著看這邊"),
    dict(loc="lane_m", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="lane",
         comp=f"over-the-shoulder medium shot from behind Tang Xiaotang's left shoulder: her shoulder and the back of her head with its two looped buns and pink silk ribbons in the right foreground, her face out of the frame; Xu Yan on screen left sitting behind the small table, framed from the chest up with space above his head, {XU}, one string of copper coins in his right hand above the open money box, his face three-quarter to screen right toward her, never the lens; amazed: brows raised, eyes wide on her, lips pressed between words",
         lines=[("xuyan", "一個早上排成這樣，妳到底是跟誰學的？", "驚奇，好奇")],
         motion=f"Xu Yan sweeps the string of copper coins into the money box and turns sideways on his stool to look up at her; Tang Xiaotang's lips stay closed; {NOSMILE}",
         zh="過肩（唐小棠肩後拍許硯）、慢推：前景右唐小棠的肩與丸子頭，左許硯在桌後一把收進一串銅錢放進錢箱，側身看她；驚奇"),
    # The script's 「唐小棠不看他」 gives way to the gaze rule (every line faces its listener): her eyes drop to the abacus as
    # she flicks it and come back to him.
    dict(loc="lane_c", cam="Over-the-shoulder medium close-up, slow push in", chars=["tangxiaotang", "xuyan"], night="lane",
         comp=f"reverse over-the-shoulder medium close-up from behind Xu Yan's right shoulder: his shoulder and topknot in the left foreground, his face out of the frame; Tang Xiaotang on screen right at the end of the small table, {CHEST}, {TANG}, her right hand over {ABACUS} lying on the table at the bottom edge, her face three-quarter to screen left toward him, never the lens; {TANG_COOL}; behind her only the drying silk of the same silk shop lane",
         lines=[("tangxiaotang", "從小幫我爹算帳。有錢人最怕的，就是比別人慢。", "淡淡，不當一回事")],
         motion=f"her eyes drop to the abacus as her right fingertips sweep across it and flick three beads over with a click, then come back up to him; Xu Yan's lips stay closed; {NOSMILE}",
         zh="反打（許硯肩後拍唐小棠）、慢推（胸口以上）：唐小棠手指在桌上的算盤一掃，撥過三顆算珠；淡淡、不笑。稿子寫「不看他」，跟「每句台詞都看著對方說」的規則衝突：改成撥算盤時眼睛往下看、撥完抬回來看他"),
    dict(loc="lane_m", cam="Medium shot, tracking", chars=["laisan"], night="lane",
         comp=f"medium shot in the middle of the queue, framed from the waist up with space above their heads: Lai San in {LAI}, small and thin with a pointed chin, both hands empty, squeezed between {LADIES} before and behind him, his face three-quarter to screen left toward the table off screen left, never the lens; sly and loud: brows raised, eyes darting, mouth opening wide on each shout",
         lines=[("laisan", "別買了！這肥皂會爛手，我表姐的手都爛了！", "扯著嗓子喊，挑撥")],
         motion=f"Lai San cups one hand round his mouth and shouts over the queue, then ducks his head down behind the shoulder of the young woman in front of him, his head staying in the frame; the young women's lips stay closed as they turn their heads toward him; {NOSMILE}",
         zh="中景、跟拍（稿子的手持感改寫 tracking，handheld 會被讀成漂移）：賴三（頭巾壓到眉毛、兩手空空）擠在隊伍中間，一手攏在嘴邊大喊，喊完把頭縮到前面那位小姐的肩膀後面；其他人嘴閉著、轉頭看他"),
    dict(loc="lane_m", cam="High-angle wide shot, locked", chars=["tangxiaotang"], night="lane", act=3,
         comp=f"high-angle wide shot looking down on the lane, everyone small in the frame: the small table on screen left with Tang Xiaotang {TANG} behind it, one flat square white bar of soap held out in her right hand; the queue of {LADIES} filling the lane toward its mouth",
         lines=[],
         motion="half of the queue breaks up, the young women clutching their washbasins and backing away toward the mouth of the lane; Tang Xiaotang's outstretched hand stops in mid-air; all lips stay closed",
         zh="俯拍全景、固定：隊伍一下散了一半，小姐們抱著木盆往巷口退；唐小棠遞皂的手停在半空（無台詞）"),
    dict(loc="lane_c", cam="Medium close-up to close-up, slow push in", chars=["tangxiaotang"], night="lane",
         comp=f"medium close-up, closing in to a close-up by the end, of Tang Xiaotang {CHEST}, {TANG}, her face three-quarter to screen right toward the crowd off screen right, never the lens; cold and sharp: brows drawn down, eyes narrowed on the crowd, lips pressed flat between words, no teeth at any moment; behind her only the drying silk of the same silk shop lane",
         lines=[("tangxiaotang", "爛手？那我現在就洗給大家看，看清楚了。", "冷，瞇眼")],
         motion=f"her eyes narrow on the crowd; she raises her forearms to chest height and shoves her right sleeve up to the elbow with her left hand, then her left sleeve with her right; {NOSMILE}",
         zh="近景、慢推（中近景推到近景，胸口以上）：唐小棠眼睛一瞇看向人群，把右手袖口往小臂上一推，再推左手；冷、不笑不露齒"),
    dict(loc="lane_c", cam="Insert close-up, locked", chars=["tangxiaotang"], night="lane", act=3,
         comp=f"insert close-up, the shot opens directly on one wooden washbasin of clear water on the small table and Tang Xiaotang's two hands from its very first frame: her bare forearms with her peach-pink sleeves pushed up to the elbows, {SOAP_BARE} between her hands; only the hands, forearms, sleeves, basin and soap are in the frame, no face; behind them only the drying silk of the same silk shop lane",
         lines=[],
         motion="the two hands work the soap into thick white lather, rinse it off in the clear water and rise out of the basin clean and glistening",
         zh="手部特寫、固定（第一格就是桌上木盆與唐小棠兩手）：兩手（桃粉袖口推到小臂）把白皂搓出濃泡，在清水裡一沖，抬起來白白亮亮（無台詞）"),
    # Tang Xiaotang may smile here (the script); written as face movements.
    dict(loc="lane_m", cam="Low-angle medium shot, slow push in", chars=["tangxiaotang"], night="lane",
         comp=f"low-angle medium shot from table height of Tang Xiaotang {TANG}, framed from the waist up with space above her head, her clean wet hands raised before her chest, her sleeves pushed up to the elbows, her face three-quarter to screen right toward the crowd, never the lens; bright and triumphant: brows lifted, eyes shining, cheeks lifting, mouth opening wide between words; at the right edge {LADY}, lips closed",
         lines=[("tangxiaotang", "誰要摸摸看？又香又滑，哪裡爛了？", "笑，得意")],
         motion="she lifts her clean hands into a band of sunlight and turns them toward the crowd; the young woman at the right edge reaches out, touches the back of Tang Xiaotang's hand with one fingertip and nods; the young woman's lips stay closed",
         zh="低角度中景、慢推（從桌面高度往上拍）：唐小棠把洗好的雙手舉進一道陽光，轉向人群；畫右前排一位小姐伸手摸她的手背、點頭（嘴閉著）；本鏡唐小棠可以笑（寫成眉揚、眼睛發亮、臉頰往上、嘴張開）"),
    dict(loc="lane_m", cam="Medium shot, tracking", chars=["qinshuang", "laisan"], night="lane",
         comp=f"medium shot, both framed from the waist up with space above their heads: in the queue Lai San, {LAI}, hunched, his face three-quarter to screen left, cringing: shoulders up, eyes darting, lips closed; Qin Shuang, {QIN}, {EMPTY}, pushing through the young women behind him, her face in profile toward him, never the lens; grim: brows slammed down, eyes narrowed on him, lips closed",
         lines=[("xuyan", "這不是前天夜裡攪了一夜鍋的賴三嗎？手好了沒？", "畫外，慢慢說，揶揄")],
         motion=f"Qin Shuang shoulders through the queue, grabs the back of Lai San's collar with her left hand and drags him forward toward the table off screen left; Lai San hunches his neck; both their lips stay closed; {NOSMILE}",
         zh="中景、跟拍：秦霜（兩手空著、畫面裡沒有任何刀鞘兵器）從人群後擠進去，左手一把揪住賴三的後領，往畫左的桌前拖；賴三縮脖子；兩人嘴閉著（許硯的台詞在畫外）"),
    dict(loc="lane_c", cam="Medium close-up to close-up, slow push in", chars=["laisan"], night="lane",
         comp=f"medium close-up, closing in to a close-up by the end, of Lai San framed from the chest up with space above his head, {LAI_PULLED}, his collar gripped from behind by one hand in a dark brown cuff at the top edge of the frame, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; fawning and panicked: brows raised and drawn together in the middle, eyes darting, cheeks pushed up, lips stretched wide over clenched teeth",
         lines=[("laisan", "我、我是路過的！手好得很，好得很！", "心虛，陪笑")],
         motion="he squirms backward against the grip on his collar and waves both raised hands in the air before his chest",
         zh="近景、慢推（中近景推到近景）：賴三頭巾被扯歪、露出眉毛，陪笑著往後掙，兩手舉起來亂搖（本鏡可以陪笑，只寫臉怎麼動）；後領被畫面上緣深褐袖口的手揪著"),
    dict(loc="lane_m", cam="Wide shot, pan right", chars=["xuyan", "qinshuang", "laisan"], night="lane", act=4,
         comp=f"wide shot, everyone small in the frame: on screen left Xu Yan sitting behind the small table, {XU}; in the middle Qin Shuang, {QIN}, {EMPTY}, holding Lai San by the collar with her left hand, Lai San in {LAI_PULLED}; behind them a long queue of {LADIES}, longer than before, the front eight sharp and the rest soft and out of focus, stretching out past the mouth of the lane",
         lines=[],
         motion="Qin Shuang shoves Lai San away; he limps off toward the mouth of the lane and out of the frame; the young women cover their mouths with their sleeves and file back into the queue with their washbasins; all lips stay closed",
         zh="全景、往右搖：秦霜一推，賴三一跛一跛逃出巷口、出畫；小姐們掩袖，又捧著木盆排回來，隊伍比 c15 更長、排出巷口（前八人清楚、後面虛焦）；畫面上的人都嘴閉著（無台詞）"),
    dict(sid="s25b", loc="lane_m", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "qinshuang"], night="lane",
         comp=f"over-the-shoulder medium shot from behind Qin Shuang's left shoulder: her shoulder and high ponytail in the right foreground, her face out of the frame, {EMPTY}; Xu Yan on screen left sitting behind the small table, framed from the chest up with space above his head, {XU}, his face three-quarter to screen right looking up at her, never the lens; brisk and decided: brows level, eyes steady on her, lips firm between words; beside the table {BASKET}, and the empty handcart beyond it; behind them, soft and out of focus, the queue of young women in Song-dynasty silk jackets",
         lines=[("xuyan", "秦霜，城南悅來客棧天天要用，妳推二十塊去問問。", "吩咐，俐落")],
         motion=f"Qin Shuang nods, lifts the basket from beside the table onto the handcart and pushes the cart away toward the mouth of the lane and out of the frame; her lips stay closed; {NOSMILE}",
         zh="過肩中景（秦霜肩後拍許硯）、慢推：前景右秦霜的肩與馬尾；許硯在桌後抬頭對她說話；秦霜點頭，把桌邊一筐（二十塊）搬上推車，推著往巷口走、出畫；背景虛焦是排回來的隊伍；秦霜兩手不拿刀、畫面裡沒有兵器"),
    dict(sid="s25c", loc="lane_c", cam="Insert close-up, slow push in", chars=["xuyan"], night="lane",
         comp=f"insert close-up of the small table, the shot opens directly on the wooden money box from its very first frame: {CASHBOX} with its lid open, and Xu Yan's right hand in a blue-grey cuff holding a handful of {SILVER} above it; only the hand, cuff, money box and silver are in the frame, his face out of the frame; behind them only the flagstones of the same silk shop lane",
         lines=[("xitong", "已賺，十二兩。", "冷淡，報數")],
         panel=[("已賺 12 兩", "panel")],
         motion="his hand opens and the lumps of silver drop into the money box and settle on its bottom",
         zh="插鏡、手部特寫、慢推（第一格就是木錢箱）：許硯的手（藍灰袖口）把一把碎銀放進錢箱，碎銀落進箱底；系統報數（面板，這場的結尾）"),
    # ---- scene 3: the same lane at the hour of shen, the low orange sun from the mouth of the lane, shadows toward the
    # camera. Axis: the table and Xu Yan on screen left; Qin Shuang back at the table's right; Sun Zhanggui at the table
    # on screen right; Tang Xiaotang at the table (middle). The queue gone.
    dict(chapter="五十兩", loc="dusk", cam="Wide shot, tracking", chars=["qinshuang"], night="dusk",
         comp=f"wide shot past the stone mounting block at the mouth of the lane in the foreground, everyone small in the frame: Qin Shuang, {QIN}, {EMPTY}, pushing the wooden handcart in from the mouth of the lane toward the small table on screen left, her long shadow stretching toward the camera, her face in profile toward the table, never the lens; plain and matter-of-fact: brows level, eyes steady, lips firm between words; behind the cart {PORTER}, carrying one empty bamboo basket",
         lines=[("qinshuang", "悅來客棧二十塊全收了，放在客房裡，錢先給。", "平淡，交差")],
         motion=f"Qin Shuang pushes the handcart up to the table and stops beside it; behind her the inn servant sets the empty bamboo basket back onto the cart, turns and walks away out of the mouth of the lane; his lips stay closed; {NOSMILE}",
         zh="全景、跟拍、前景巷口石墩（長鏡）：斜陽照進巷子；秦霜（兩手只推車、沒有兵器）推著推車從巷口回來，客棧夥計（宋式灰布交領短打、布包頭，只拍背影）跟在車後，把空竹筐放回推車上，轉身往巷口外走出畫；秦霜停在桌邊"),
    dict(loc="dusk_c", cam="Insert close-up, locked", chars=["qinshuang"], night="dusk", act=3,
         comp=f"insert close-up of the small table, the shot opens directly on the tabletop from its very first frame: {ABACUS} lying on it, and Qin Shuang's right hand in a dark brown cuff holding {PURSE} above it; only the hand, cuff, money pouch, abacus and tabletop are in the frame, no face, no blade, no knife and no weapon anywhere in the frame; behind them only the flagstones of the same silk shop lane in the low orange sun",
         lines=[],
         motion="her hand slaps the money pouch down on the table; its mouth falls open and small lumps of silver roll out and knock against the abacus",
         zh="手部特寫、固定（第一格就是桌面與布錢袋）：秦霜的右手（深褐袖口）把錢袋往桌上一拍，袋口鬆開，碎銀滾出來撞到算盤（無台詞）"),
    dict(loc="dusk_m", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "qinshuang"], night="dusk",
         comp=f"over-the-shoulder medium shot from behind Qin Shuang's left shoulder: her shoulder and high ponytail in the right foreground, her face out of the frame, {EMPTY}; Xu Yan on screen left sitting behind the small table, framed from the chest up with space above his head, {XU}, the lumps of silver on the table before him, his face three-quarter to screen right toward her, never the lens; impressed and curious: brows raised, eyes on her, lips pressed between words",
         lines=[("xuyan", "二十塊，又是六兩。秦霜，妳是怎麼談下來的？", "佩服，好奇")],
         motion=f"Xu Yan sweeps the lumps of silver one by one back into the cloth pouch, then lifts his eyes to her; Qin Shuang's lips stay closed; {NOSMILE}",
         zh="過肩（秦霜肩後拍許硯）、慢推：前景右秦霜的肩與馬尾；許硯把碎銀一顆顆撥回錢袋，抬頭看她"),
    dict(loc="dusk_c", cam="Over-the-shoulder medium shot, slow push in", chars=["qinshuang", "xuyan"], night="dusk",
         comp=f"reverse over-the-shoulder medium shot from behind Xu Yan's right shoulder: his shoulder and topknot in the left foreground, his face out of the frame; Qin Shuang on screen right standing beside the table, framed from the chest up with space above her head so her belt and hips stay below the bottom edge of the frame, {QIN}, her face three-quarter to screen left toward him, never the lens; dry and blunt: brows level, eyes half-lidded, the corners of her mouth pulled down, lips firm between words; no blade, no knife, no scabbard and no weapon anywhere in the frame; behind her only the drying silk of the same silk shop lane in the low orange sun",
         lines=[("qinshuang", "我只說住店的客人身上都臭，他就自己掏錢了。", "淡淡，理所當然")],
         motion=f"Qin Shuang folds her arms across her chest and rests one shoulder against the bamboo drying pole beside the table; {NOSMILE}",
         zh="反打（許硯肩後拍秦霜）、慢推：前景左許硯的肩；秦霜雙手抱胸，肩膀往桌邊的晾竿一靠；不笑。live：胸口以上、腰帶在畫面下緣外（第 6 集 s23 這樣才沒有刀）；稿子寫「往桌邊一靠」，寫成肩膀靠在晾竿上，不寫 leans"),
    dict(loc="dusk_c", cam="Extreme close-up, slow push in", chars=["xuyan"], night="dusk",
         comp=f"{EYES}; his eyes lowered a little",
         lines=[("xitong", "已賺，十八兩。", "冷淡，報數，句後停半秒")],
         panel=[("已賺 18 兩", "panel")],
         motion="his eyes lower to the money pouch below the frame; nothing else moves",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：許硯的眼睛往下一垂，看手上的錢袋；系統報數（面板）。live：同 c03，不寫瞳孔裡的藍光"),
    dict(loc="dusk_c", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="dusk",
         comp=f"medium close-up, closing in to a close-up by the end, of Xu Yan sitting behind the small table, framed from the chest up with space above his head, {XU}, both hands gripping the edge of the table at the bottom of the frame, his face three-quarter to screen right, never the lens; tense: brows drawn together, eyes narrowed, lips closed the whole shot, jaw tight; behind him only the drying silk of the same silk shop lane in the low orange sun",
         lines=[("xuyan", "還差二兩，太陽還高，應該來得及。", "心裡話，嘴閉著，盤算", "inner")],
         motion=f"he lifts his eyes and squints up at the sun sinking toward the rooftops off screen right, and both hands tighten on the table edge, his head still; his lips stay closed; {NOSMILE}",
         zh="近景、慢推（中近景推到近景）：許硯抬眼瞇著看屋頂上偏西的太陽，兩手抓緊桌緣；心裡話，嘴閉著。live：只抬眼、頭不動"),
    # Sun Zhanggui's hand only; he speaks off screen (no portrait for an insert).
    dict(loc="dusk_c", cam="Low-angle insert close-up, slow push in", chars=[], night="dusk",
         comp=f"low-angle insert close-up at table height, the shot opens directly on a small heap of {SILVER} on the table from its very first frame: one thin bony man's hand in a green satin sleeve with one green jade ring on its thumb lowering {INGOT} beside the heap; only the hand, sleeve, ingot and silver are in the frame, no face; behind them only the low orange sun of the same silk shop lane; Sun Zhanggui speaks off screen",
         lines=[("sunzhanggui", "柳溪村做肥皂的許秀才，我在巷口看你一整天了。", "畫外，慢條斯理")],
         motion="the hand sets the big silver ingot down beside the heap with a thud, the small lumps of silver jump once, and the hand comes to rest flat on the ingot",
         zh="低角度手部特寫、慢推（第一格就是桌上碎銀堆）：一隻瘦手（綠緞袖口、拇指綠玉扳指）把一錠大銀（船形元寶、兩掌長、素銀沒有字）放在碎銀堆旁，碎銀跳一下；手停在銀錠上；孫掌櫃在畫外說話"),
    dict(loc="dusk_c", cam="Medium shot to medium close-up, slow push in", chars=["sunzhanggui"], night="dusk",
         comp=f"medium shot, closing in a little by the end, of {SUN}, standing at the small table on screen right, framed from the waist up with space above his head, one finger resting on {INGOT} on the table, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; composed and calculating: brows level, eyes half-lidded and steady, lips thin between words; behind him only the drying silk of the same silk shop lane in the low orange sun",
         lines=[("sunzhanggui", "在下魏記商行孫掌櫃。這肥皂的方子，賣給我吧。", "慢條斯理")],
         motion=f"he keeps one finger on the ingot and gives a small bow from the shoulders, his head staying in the frame; {NOSMILE}",
         zh="中近景、慢推（中景推到中近景）：孫掌櫃（瘦長臉、花白鬍、宋式綠緞交領袍、右拇指綠玉扳指；不胖、不圓臉、不拿玉球）站在桌邊（畫右），一根手指按著銀錠，微微欠身；不笑"),
    dict(loc="dusk_c", cam="Close-up, slow push in", chars=["tangxiaotang"], night="dusk", act=3,
         comp=f"close-up of Tang Xiaotang {CHEST}, {TANG}, her right hand frozen over {ABACUS} on the table at the bottom edge, her face three-quarter to screen right toward the man off screen right, never the lens; struck pale: brows lifting in alarm, eyes wide, lips pressed shut, no teeth; behind her only the drying silk of the same silk shop lane in the low orange sun",
         lines=[],
         motion=f"her fingers stop dead on the abacus; she presses her right hand flat to the collar of her jacket, then turns her shoulders and her face away from the man off screen right toward screen left, never toward the lens; her lips stay closed; {NOSMILE}",
         zh="近景、慢推（胸口以上）：唐小棠聽到「魏記」，撥算盤的手停住，右手按住衣領，轉身背對孫掌櫃（臉轉向畫左、不朝鏡頭）；臉色一白、嘴閉著（無台詞）。live：稿子的「按住高立領」改成按住衣領（真人版服裝是交領短襦）"),
    dict(loc="dusk_m", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "sunzhanggui"], night="dusk",
         comp=f"over-the-shoulder medium shot from behind Sun Zhanggui's left shoulder: his green satin shoulder and the tip of his grey-streaked beard in the right foreground, his face out of the frame; Xu Yan on screen left behind the small table, framed from the waist up with clear space above his head so his whole head stays in the frame after he stands, {XU}, the silver ingot on the table between them, his face three-quarter to screen right toward him, never the lens; wary and steady: brows drawn down, eyes level, lips firm between words, jaw set",
         lines=[("xuyan", "方子不是肥皂。掌櫃一開口就要買，總得出個價。", "冷靜，試探")],
         motion=f"Xu Yan's eyes go from the silver ingot up to Sun Zhanggui as he rises slowly to his feet behind the table, his whole head staying in the frame; Sun Zhanggui's lips stay closed; {NOSMILE}",
         zh="過肩（孫掌櫃肩後拍許硯）、慢推：前景右孫掌櫃的綠緞肩與花白鬍尖；許硯從桌後站起來，眼睛從銀錠抬到孫掌櫃；冷靜試探。live：站起來的鏡寫腰以上、頭上留夠空間"),
    dict(loc="dusk_m", cam="Over-the-shoulder medium shot, slow push in", chars=["sunzhanggui", "xuyan"], night="dusk",
         comp=f"reverse over-the-shoulder medium shot from behind Xu Yan's right shoulder: his shoulder and topknot in the left foreground, his face out of the frame; {SUN}, on screen right across the small table, framed from the waist up with space above his head, his fingertips on {INGOT} on the table, his face three-quarter to screen left toward Xu Yan, never the lens; smooth and cold: brows level, eyes half-lidded, lips thin between words",
         lines=[("sunzhanggui", "五十兩。還了債，你還剩三十兩過好日子。", "慢條斯理，篤定")],
         motion=f"Sun Zhanggui pushes the silver ingot one inch forward across the table with his fingertips and lifts his eyes to Xu Yan; Xu Yan's lips stay closed; {NOSMILE}",
         zh="反打（許硯肩後拍孫掌櫃）、慢推：前景左許硯的肩；孫掌櫃用指尖把銀錠往前推一寸；不笑"),
    dict(loc="dusk_c", cam="Extreme close-up, slow push in", chars=["xuyan"], night="dusk",
         comp=f"{EYES}; his eyes lowered toward the table",
         lines=[("xitong", "賣方子，還是賭日落？", "冷，句尾往下壓")],
         motion="his eyes drop to the silver ingot below the frame, then rise toward the low sun off screen right, and his brows lock; nothing else moves",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：許硯的眼睛往下看銀錠，再往上看下沉的太陽，眉頭鎖住（稿子的「下顎一緊」在滿框眼睛的鏡裡看不到）；系統問（結尾，懸念到第 8 集）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e007-r2/script.md`（c01–c25、c25b、c25c、c26–c37 對應 s01–s25、s25b、s25c、s26–s37；含「這版改了什麼」與「2026-11-06 審稿後的修改」）；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。",
    "- 內部工作編號 907（`hailuo/*-dh-e907.json`、`colab/runs/e907/`）；發布 slug `zhong-tian-qu-qi-e007-r2`。不放集數、不放片名卡；c01 是第 6 集 c40 之後過了一夜的第四天清晨（許硯不再紅眼、胸前紅布拿掉、髮上紙花不再寫）。",
    "- 真人版的寫法一開始就寫進來（第 4–6 集真人版重拍的教訓）：秦霜只有 c07（插刀）、c10（拍刀柄）兩鏡有刀，其他鏡一律「兩手空著、畫面裡沒有刀、鞘、兵器」，近景框到胸口；白皂一律「扁方、掌心大、一指厚、像小磁磚」，竹筐加「沒有圓條、沒有圓柱」；每句台詞都看著對方說、不看鏡頭；每張露臉的臉都逐部位寫表情，不能笑的鏡只用 NOSMILE 一句；唐小棠服裝照定妝照（交領短襦闔上、百褶裙），不寫高立領。",
    "- 一鏡最多三個有名字的人：c15 茶棚下的孫掌櫃不點名（虛焦小人，不送參考圖），c32 只拍手、畫外說話；排隊的小姐、丫鬟、夫人的手、客棧夥計沒有參考圖，衣服寫宋式。",
    "- 沒有字：紅色後門的門楣空白、不掛燈籠；錢箱、算盤、銀錠都素面沒有字；系統面板用 overlays（s01、s14、s25c、s30）。眼睛大特寫 s03、s30、s37 寫第 6 集 fix1 的滿框雙眼、深棕虹膜、一點眼神光，不寫稿子的「瞳孔映淡藍光」。",
    "- 軸線：第一場許硯在推車左、唐小棠從右邊屋門出來，所以 s05 從唐小棠左肩後拍（肩在畫右前景）、s06 從許硯右肩後拍（肩在畫左前景）——稿子 c05、c06 的前景左右寫反、會越軸，已改；第二、三場照稿子（桌子與許硯在畫左，唐小棠、秦霜、孫掌櫃在畫右）。",
    "- 長鏡要買的秒數（`r2.py` 的 BUY）：見 BUY 註解；還沒錄音，照稿子長鏡清單與台詞字數估。",
]
FOOT = [
    "- 場景參考：第一場院子 `set-xujia-yuan-t1`（真人版 `set-xujia-yuan-l2`）；第二、三場的綢緞莊後巷稿子沒有場景圖，提示詞寫 the lane behind the county silk shop，gen-dh 對到第一季的 `set-chouduan-t1`（竹竿晾綢布、石板路、一道後門）；不寫 back alley（會對到夜裡的 `set-xiaoxiang-t1`）、不寫 teahouse（會對到 `set-chalou-t1`），巷口茶棚寫 tea stall。**`set-chouduan` 沒有真人版（`refs-live/` 沒有 `set-chouduan-l1.png`）**，pilot.py 在後巷 27 鏡會停；要站主決定畫一張真人版後巷，或改成不送場景圖。",
    "- 孫掌櫃：`cast.json` 的外貌已是 r2 的瘦長臉、花白鬍、綠緞袍，但 `refs-dh/sunzhanggui-portrait-t1.png` 還是舊的胖圓臉拿玉球，**`refs-live/` 也沒有他**；s33、s35、s36 要等站主畫 `sunzhanggui-portrait-l1.png`（真人、瘦長臉）。`cast.json` 他的外貌有一句 narrow smiling eyes，`colab/runs/e907/extras.json` 換成不笑的寫法。",
    "- 賴三 `laisan-portrait-l1` 有真人定妝照（沒有角度圖）；阿令、小禾、唐小棠、秦霜、許硯都有真人定妝照與角度圖。",
    "- 唐小棠一律寫 TANG（定妝照的交領短襦闔上、百褶裙繫蝴蝶結），近景框到胸口；`pilot.py` 會把 `cast.json` 的高立領句換成真人版、拿掉 sweet 與 dimples。",
    "- 秦霜的 `cast.json` 造型寫著「柴刀插在腰帶」：`extras.json` 與 `pilot.py` 都把這句從造型句拿掉，刀只在 s07、s10 由構圖寫。",
    "- 配樂：院子 comedy、後巷 market cue（s18 喊爛手音樂抽掉，s22 舉手一個重音接回）、五十兩 suspense（s32 銀錠落桌一個重音，s37 收在低音）；音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy (script.md 長鏡清單: c04, c11, c26 at 8). Not recorded yet: the others from the line length at
# the series' median 3.7 zh characters a second + 0.5 s, against buy - 0.3 s with the cut's 1.1x: a line of 18 or more
# characters (with punctuation stripped) needs about 5.4-5.9 s and gets 8 when the shot also has a motion before or
# after it. Re-check against the recorded or drafted voice before stage 1. Estimated need (chars / 3.7 + 0.5): s06, s23,
# s25b 5.9 and s32 5.9 (the off-screen line over the insert, which gen-dh would buy at 5) -> 8; s07, s11, s17, s29, s33,
# s35 5.6 left at 6 (s11 is a script long shot at 8). The live drafts speak with the model's own voice, which pauses
# mid-line (route-a.md 2026-11-07), so these are a floor.
BUY = {"s04": 8, "s06": 8, "s11": 8, "s23": 8, "s25b": 8, "s26": 8, "s32": 8}
