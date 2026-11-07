"""Episode 5 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e005-r2/script.md
(c01-c40 = s01-s40), including its section 「2026-11-06 審稿後的修改」, which overrides the tables (c01 「那一鍋是我們全家的命，
你敢倒試試！」, Qin Shuang following Xu Yan out into the shadow of the eaves and the long pole leaning on the wok; c02 the knife
flying in from her dark eaves; c04 「女俠饒命，小的賴三，只是路過想喝口水。」; c12 the pole snatched from the wok rim; the
knife always in the right of her belt with its black-wrapped handle and gleaming edge; the pine mould three feet by one
foot, three rows of ten; the dawn light from the back left; c35 Xu Yan picking up one white bar).

Same rules as e001-r2 to e004-r2: one visible action per shot written as a path, over-the-shoulder and reverse shots
for dialogue, whole sentences, one line per spoken line, default face serious (smiles only where the script allows: c04
Lai San's fawning grin, c27 and c30 Xiaohe, c35 Tang Xiaotang). State: Xu Yan with his sleeves rolled to the elbows all
episode, his hands empty in scene 1 apart from the bucket c05 and the long stirring pole c12, red-eyed and tired from
c15, a few loose strands over his forehead from c23, one white bar of soap from c35 (dropped c37, picked up c38); Qin
Shuang's old chopping knife in the right of her belt c01, flying into the post c02 (her belt empty c03-c07), back in
the right of her belt from c08, an old grey outer coat over her shoulders c23-c26; Lai San (picture laisan) with his
right sleeve pinned c02-c07 and torn from c08, the stirring pole c12-c21, asleep by the fence until c34; A-ling without
shackles, her sleeves over the red marks, only a sleeve in the door gap c14, a thin stick c18-c20; Tang Xiaotang always
t2 (high collar, closed garment, chin-up close-ups), the abacus under her left arm c28-c39; Xiaohe's straw rabbit in her
left arm c27, under her arm from c30. No skin bits (the script's 「手上沾著灰／白色皂屑」 c29, c32 are left out: they render as
growths), no glow outside the eye extreme close-up c36, no writing anywhere. Opens on the next instant after e004 c40:
the bucket already tipping over the wok.
"""
EP = 905  # internal working number; the published slug is zhong-tian-qu-qi-e005-r2
SLUG = "zhong-tian-qu-qi-e005-r2"
EP_TITLE = "半夜倒水壞鍋，天亮第一塊肥皂（重製版 r2）"
OUTLINE_SECONDS = 207.5  # script.md 2026-11-06: 71 + 61.5 + 75 s, 40 shots
TARGET_MINUTES = [3, 4]
TITLE = "半夜倒水壞鍋，天亮第一塊肥皂｜種田娶妻打天下 第5集（重製版）"
DESCRIPTION = "第二天夜裡，賴三摸進許家院子，正要把一桶水倒進熬肥皂的大鍋，秦霜一刀把他的袖子釘在棚柱上。賴三招出是錢員外指使，秦霜要剁他手指，許硯卻不打、不送官，罰他攪鍋到天亮。後半夜阿令出來陪許硯撥火，問他為什麼給害他的人留路，聽完回屋，好感 +3；天快亮時秦霜出來，看他一夜沒闔眼只為了不糟蹋她扛來的豬，好感 +5，接手顧鍋。第三天清晨開模，一百五十塊雪白肥皂成功，唐小棠定價一塊三錢，許硯送一塊給錢員外「洗洗手」。正要鬆一口氣，系統下強制任務：今日午時前婚書蓋印——許硯這才想起還沒成親，而縣衙午時就關門。《種田娶妻打天下》第 5 集（重製版）。"
THUMB = ("今天這婚，非成不可", "s40")
CHARACTERS = ["xuyan", "qinshuang", "laisan", "aling", "tangxiaotang", "xiaohe", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: a low tense cue of drums and erhu at the cooking shelter in the yard at night, one heavy hit as the chopping knife thunks into the post; a low quiet night cue of soft guqin and low cello by the stove fire late at night until dawn, one soft light chime on each affection line; a warm gentle guqin and soft strings in the yard at sunrise, dropping out on the system chime to one low heavy hit and ending on a low suspense cue; ancient Chinese rural drama, no vocals"

# Scene headers of script.md: all three scenes in the Xu yard (set-xujia-yuan-t1). Scenes 1-2 at the cooking shelter on
# the east side of the yard, written the way e004's last shots wrote it so gen-dh maps "dirt yard" to the yard picture
# (never "kitchen", "lean-to" or "workshop", which map to other sets); scene 3 at the long board under the persimmon tree.
# Axis, scenes 1-2: the shelter posts on screen left (Lai San's side), the stove and the wok in the middle, the house
# door and eaves on screen right (Xu Yan, Qin Shuang, A-ling come out of it). Scene 3: the board across the middle, the
# house door on screen right, the yard gate deep at the back left, the shelter at the back left. The close shots use
# the short `_c` locations (one line, so the set does not pull a close-up wide) and end on a same-place background.
LOC = {
    "night": "In the dirt yard of the Xu farmhouse on a clear windless autumn night, at the cooking shelter on the east side of the yard: two wooden shelter posts on screen left, a clay stove in the middle with one big black iron wok on it giving off white steam, a woodpile, a bamboo fence and a persimmon tree, the house door and eaves on screen right, lit from below by the warm orange glow of the stove fire and by cold moonlight from the upper right",
    "night_c": "At the cooking shelter in the dirt yard of the Xu farmhouse on an autumn night, lit by the warm orange stove fire and cold moonlight",
    "late": "In the dirt yard of the Xu farmhouse late on a clear autumn night, at the cooking shelter on the east side of the yard: two wooden shelter posts on screen left, a clay stove in the middle with the big black iron wok on it giving off white steam, one low stool before the stove, a woodpile and a bamboo fence, the house door on screen right, the moon low in the west, lit by the warm orange glow of the stove fire and cold moonlight",
    "late_c": "At the cooking shelter in the dirt yard of the Xu farmhouse late at night, lit by the warm orange stove fire and low cold moonlight",
    "dawn": "In the dirt yard of the Xu farmhouse just before dawn on a clear autumn day, at the cooking shelter on the east side of the yard: two wooden shelter posts on screen left, a clay stove in the middle with the big black iron wok giving off white steam and a low fire, one low stool before it, a bamboo fence, the house door on screen right, the sky paling at the horizon, cold blue dawn light from the back left",
    "dawn_c": "At the cooking shelter in the dirt yard of the Xu farmhouse at dawn, cold blue dawn light from the back left and a low stove fire",
    "sun": "In the dirt yard of the Xu farmhouse at sunrise on a clear autumn morning: one long wooden board laid across two wooden blocks under a persimmon tree in the middle, the cooking shelter with its clay stove and the big black iron wok at the back left, the yard gate in the bamboo fence deep at the back left, the house door on screen right, warm low sunrise light from screen left casting long shadows",
    "sun_c": "In the dirt yard of the Xu farmhouse at sunrise, warm low sunlight from screen left",
}
LIGHT = {
    "night": "the warm orange firelight and the cold moonlight stay unchanged",
    "late": "the warm orange firelight and the low cold moonlight stay unchanged",
    "late_fire": "the warm orange firelight stays steady apart from that one flare",
    "dawn": "the cold blue dawn light from the back left and the low stove fire stay unchanged",
    "sun": "the warm low sunrise light from the left stays unchanged",
}

# Repeated wording (each prop is one object; the descriptions say "one" where it first appears).
XU = "his blue-grey scholar's robe with his sleeves rolled up to the elbows"
NIGHT = "red-eyed with faint shadows under his eyes, tired"
HAIR = "a few loose strands of hair fallen over his forehead"
LAI = "his grey-brown short jacket and old cloth head-wrap"
QIN = "her dark brown cross-collared short jacket, wide leather belt, black trousers, leather boots and high ponytail"
KNIFE = "her old chopping knife in the right side of her belt"
CHOP = "one old chopping knife, single-edged with a broad back, its wooden handle wrapped in black cloth and its edge gleaming"
POLE = "one long wooden stirring pole taller than a man"
BUCKET = "one wooden bucket full of water"
ALING = "no shackles, her sleeves pulled down over her wrists"
TANG = "her peach-pink brocade ruqun one closed garment from the high stand-up collar to the waist"
HE = "little Xiaohe in her patched lilac short jacket with red-string pigtails and one front tooth missing"
GOURD = "one brown water gourd with a wooden stopper"
MOULD = "one long plain pine soap mould about three feet long and one foot wide, turned upside down"
SOAP_ST1 = "snow-white square bars of soap, each palm-sized and one finger thick with square corners, opaque and not glowing"  # s27 (picked)
# 2026-11-07 independent review of the stage-1 drafts (colab/runs/e905/review-picks.tsv): five RETAKE shots, one phrase
# per prop word for word in them (s08, s25 -> colab/runs/e905/fix2; s28, s31, s33 -> fix3). The phrases above stay in the
# picked shots.
# The soap (s31 drew a big long brick; s33's board read as white piano keys).
SOAP = "a snow-white square bar of soap the size of a palm and one finger thick"
# Tang Xiaotang's collar (s31: all four drafts drew a neckband over an open chest).
TANG_SHUT = "her peach-pink brocade ruqun one closed garment from the high stand-up collar buttoned at the throat to the waist"
COLLAR = "framed from the chin up, her face filling the frame, the top of her high stand-up collar buttoned to the throat at the bottom edge, one closed garment, no opening below the collar"
# s28, s31, s33: every draft laughed with her teeth showing; a concrete face, not just "unsmiling".
TANG_CALC = "serious and calculating the whole time, lips closed between words, the corners of her mouth level, brows slightly lowered, eyes narrowed, no smile and no teeth at any moment"

SHOTS = [
    # ---- scene 1: the cooking shelter, the second night (the instant after e004 c40), stove firelight from below and
    # cold moonlight from the upper right. Axis: posts on the left (Lai San), wok in the middle, house door on the right.
    dict(chapter="灶棚", loc="night", cam="Full shot, slow push in", chars=["laisan", "xuyan", "qinshuang"], nospeak=["xuyan"], night="night",
         comp=f"full shot past the bamboo fence in the foreground: in the middle Lai San in {LAI}, standing on one low wooden stool by the steaming wok, his back to the stove fire and his face in shadow, {BUCKET} raised in both hands over the wok; {POLE} leaning against the rim of the wok; nobody else by the wok; deep on screen right the house door, firewood scattered on the floor just inside its threshold",
         lines=[("xuyan", "那一鍋是我們全家的命，你敢倒試試！", "畫外，厲聲，人在遠處")],
         motion=f"Lai San tips the bucket over the wok; the house door on screen right bursts open, Xu Yan kicks the firewood aside and runs out into the firelight, and Qin Shuang, {KNIFE}, follows him out into the shadow of the eaves; all lips stay closed",
         zh="全景、慢推、前景竹籬笆：賴三（背對灶火、臉在暗處）站在板凳上，兩手把木水桶舉到鍋口、桶口往下傾；長木棍斜靠在鍋邊；右邊深處屋門猛地推開，許硯踢開門檻內一地的柴衝出來，秦霜（柴刀插在腰帶右邊）跟出來閃進屋簷陰影；許硯太遠、看不到嘴（台詞不對嘴）"),
    dict(loc="night_c", cam="Insert close-up, locked", chars=["laisan"], night="night", act=3,
         comp="insert close-up of the wooden shelter post, the shot opens directly on Lai San's raised right hand and his grey-brown sleeve from its very first frame: his right hand gripping the rim of the raised wooden bucket, his grey-brown cotton sleeve and one section of the wooden post beside it; only the hand, sleeve, bucket rim and post are in the frame, his face out of the frame; behind them only the dark of the same cooking shelter",
         lines=[],
         motion=f"{CHOP} flies in from the dark eaves on screen right and thunks through the sleeve into the post; the arm jerks and the bucket tilts, spilling only a few drops on the ground",
         zh="手部特寫、固定（第一格就是舉桶的灰褐袖子）：賴三舉桶的右手與袖子、一截棚柱；舊柴刀（單刃寬背、木柄纏黑布、刃口發亮）從右邊屋簷暗處飛進來，「咚」地把袖子釘在棚柱上；手臂被扯住，水桶一歪，只濺出幾滴到地上、沒進鍋"),
    dict(loc="night", cam="Medium shot, tracking", chars=["qinshuang", "laisan"], night="night",
         comp=f"medium shot, Qin Shuang stepping out of the shadow of the eaves on screen right, {QIN}, the right side of her belt empty, cold and unsmiling; at the left edge of the frame Lai San's raised arm, his grey-brown sleeve pinned to the wooden post by the chopping knife",
         lines=[("qinshuang", "半夜摸進來倒水，你是嫌命太長了？", "冷")],
         motion="Qin Shuang strides out of the shadow toward screen left, rolling up her right sleeve as she walks, and stops one step before the wok, her eyes fixed on Lai San; his lips stay closed",
         zh="中景、跟拍（由右往左）：秦霜（腰帶右邊空著）從屋簷陰影大步走出來，邊走邊捲右手袖子，停在鍋前一步，盯著左邊的賴三；左邊緣賴三被釘住的手臂；冷"),
    dict(loc="night_c", cam="Medium close-up to close-up, slow push in", chars=["laisan"], night="night",
         comp=f"medium close-up, closing in to a close-up by the end, of Lai San, {LAI}, small and thin with a pointed chin, his right arm pinned above his head by the sleeve, his left hand still gripping the bucket's handle, panicked with a fawning forced grin; behind him only the wooden shelter post of the same cooking shelter",
         lines=[("laisan", "女俠饒命，小的賴三，只是路過想喝口水。", "慌，陪笑")],
         motion="he yanks his pinned right sleeve twice without freeing it, hunches his neck and squeezes out a fawning grin",
         zh="近景、慢推（中近景推到近景）：賴三右手臂被釘在頭頂、左手還抓著水桶提把，猛扯兩下右袖扯不動，脖子一縮擠出陪笑（本鏡可以陪笑）；身後只有棚柱"),
    dict(loc="night", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "laisan"], night="night",
         comp=f"over-the-shoulder shot from behind Lai San's shoulder and his old cloth head-wrap in the left foreground, Xu Yan on screen right, {XU}, cold and unsmiling",
         lines=[("xuyan", "口渴喝水，用得著扛一整桶站上板凳？", "冷")],
         motion="Xu Yan stops before the stool, takes the wooden bucket out of Lai San's left hand with both hands, turns to set it on the ground, then looks up at him; Lai San's lips stay closed",
         zh="過肩（賴三肩後拍許硯）、慢推：許硯走到板凳前，伸雙手把水桶從賴三左手拿下來，轉身放到地上，再抬頭看他；冷、不笑"),
    dict(loc="night", cam="Medium close-up, slow push in", chars=["laisan", "qinshuang"], night="night",
         comp=f"medium close-up, Lai San on screen left pinned to the wooden post by his sleeve, and Qin Shuang on screen right, {QIN}, her left hand gripping his collar and her right hand on the handle of the chopping knife stuck in the post, cold and unsmiling",
         lines=[("qinshuang", "少廢話。誰叫你來的？不說，我先剁你一根手指。", "兇，逼問")],
         motion="Qin Shuang yanks his collar down with her left hand so he drops into a half-crouch on the stool, and her right hand tightens on the knife handle; Lai San's lips stay closed",
         zh="中近景、慢推：秦霜左手揪住賴三衣領往下一拽，賴三被拽得半蹲在板凳上；右手握緊釘在柱上的刀柄"),
    dict(loc="night_c", cam="Low-angle close-up, slow push in", chars=["laisan"], night="night",
         comp=f"low-angle close-up from below the stool of Lai San, {LAI}, hunching his neck, his collar gripped by one hand in a dark brown cuff at the top edge of the frame, terrified and close to tears; behind him only the wooden post and the dark of the same cooking shelter",
         lines=[("laisan", "是錢員外！他說這鍋要是成了，你們就還得出錢。", "哭腔")],
         motion="his eyes dart right to the hand gripping the knife handle, and his whole body gives a shudder",
         zh="低角度近景（從板凳下往上拍）、慢推：賴三縮著脖子、衣領被畫面上緣秦霜的左手揪著，眼睛往右瞟一下握刀的手，整個人一抖；哭腔"),
    dict(loc="night", cam="Medium shot, slow push in", chars=["laisan", "qinshuang", "xuyan"], night="night",
         comp=f"medium shot, Lai San on screen left by the wooden shed post, both his hands empty, his right sleeve still pinned to the post by {CHOP}, its blade sunk deep into the post and its handle sticking out toward Qin Shuang; Qin Shuang in the middle, her right hand gripping that handle, the right side of her belt empty, unsmiling; Xu Yan on screen right, {XU}, unsmiling",
         lines=[("xuyan", "果然是他。秦霜，刀收好，人別打。", "冷靜")],
         motion="Qin Shuang's right hand wrenches the knife out of the post; only then Lai San's sleeve rips open along the forearm as his arm drops; she slides the knife into her belt on the right, blade down; Xu Yan turns to her; the others' lips stay closed",
         zh="中景、慢推（e905 fix2）：賴三在左、兩手空空，右袖還被舊柴刀釘在棚柱上（刀身深深吃進柱子，裹黑布的刀柄朝秦霜伸出）；秦霜在中間右手握住刀柄把柴刀從柱上拔出來，賴三的右袖這才沿前臂撕開、手臂垂下；秦霜把刀刃朝下插進腰帶右邊；右邊許硯轉頭看秦霜說話，其他人嘴閉著"),
    dict(loc="night", cam="Over-the-shoulder medium shot, slow push in", chars=["qinshuang", "xuyan", "laisan"], night="night",
         comp=f"over-the-shoulder shot from behind Xu Yan's shoulder and his rolled-up sleeve in the left foreground, Qin Shuang on screen right, {QIN}, {KNIFE}, her left hand gripping Lai San's collar, frowning, defiant and unsmiling; Lai San at the back left by the post, his torn sleeve hanging",
         lines=[("qinshuang", "他要毀你的鍋，你還替他求情？", "不服")],
         motion="Qin Shuang lets go of the collar and Lai San drops onto the stool; she turns round and glares at Xu Yan; Lai San's lips stay closed",
         zh="過肩（許硯肩後拍秦霜）、慢推：秦霜鬆開衣領，賴三跌坐在板凳上；秦霜轉過身來瞪許硯；不服、皺眉"),
    dict(loc="night", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "qinshuang"], night="night",
         comp=f"reverse over-the-shoulder shot from behind Qin Shuang's shoulder and high ponytail in the right foreground, Xu Yan on screen left, {XU}, unsmiling",
         lines=[("xuyan", "妳打傷他，明天錢員外就帶衙役來，說我們行兇。", "壓低聲音")],
         motion="Xu Yan takes one step forward, lowers his voice and jerks his chin toward the village off screen right; Qin Shuang's lips stay closed",
         zh="反打（秦霜肩後拍許硯）、慢推：許硯往前一步、壓低聲音，用下巴朝畫面右外（村口方向）一指"),
    dict(loc="night_c", cam="Medium close-up to close-up, slow push in", chars=["qinshuang"], night="night",
         comp=f"medium close-up, closing in to a close-up by the end, of Qin Shuang, {QIN}, {KNIFE}, unsmiling; behind her only the wooden shelter post of the same cooking shelter",
         lines=[("qinshuang", "那就這樣放他走？我扛回來那頭豬，豬油白熬了？", "不甘")],
         motion="she flicks her hand, steps back one pace and folds her arms across her chest",
         zh="近景、慢推（中近景推到近景）：秦霜甩一下手、退開一步，雙手抱胸；不笑"),
    dict(loc="night", cam="Medium shot, tracking", chars=["xuyan", "laisan"], night="night",
         comp=f"medium shot, the shot opens directly on Xu Yan's right hand gripping {POLE} leaning against the rim of the steaming wok from its very first frame; Xu Yan, {XU}, unsmiling; Lai San sitting on the low stool at the left, his torn sleeve hanging",
         lines=[("xuyan", "不放。罰他攪鍋，一圈都不准停，攪到天亮。", "冷，定下來")],
         motion="Xu Yan snatches up the pole, takes two steps, shoves it into Lai San's arms, grabs the back of his collar and pushes him to stand before the wok; Lai San's lips stay closed",
         zh="中景、跟拍（第一格是許硯抓住鍋邊長木棍的手）：許硯一把抓起斜靠在鍋邊的長木棍（比人高、木色），走兩步塞進賴三懷裡，抓住他後領推到鍋前站好"),
    dict(loc="night_c", cam="Medium close-up to close-up, slow push in", chars=["laisan"], night="night",
         comp=f"medium close-up, closing in to a close-up by the end, of Lai San, {LAI}, his torn right sleeve hanging, both arms round the long wooden stirring pole, dismayed; behind him only the white steam of the big wok in the same cooking shelter",
         lines=[("laisan", "攪到天亮？那我這雙手明天還要不要了？", "哀號")],
         motion="he looks down at the bubbling wok, then at his own trembling hands, and his face crumples",
         zh="近景、慢推（中近景推到近景）：賴三抱著攪棍，低頭看翻滾的鍋，再看看自己發抖的手，臉垮下來；身後是冒白氣的鍋"),
    dict(loc="night", cam="Point-of-view full shot, locked", chars=["laisan", "qinshuang", "xuyan"], nospeak=["qinshuang"], night="night",
         comp="point-of-view full shot from inside the house through the narrow gap of the door, the dark door frame in the foreground: beyond it in the middle Lai San with the long stirring pole in his arms by the steaming wok; Qin Shuang seen from behind, her back to the door; Xu Yan squatting before the stove with his back to the door; at the right edge of the frame one grey-white cotton sleeve at the edge of the door",
         lines=[("qinshuang", "手斷了也得攪。天亮前停一下，我就剁一根。", "背影，冷")],
         motion="Lai San starts stirring round the wok; Xu Yan pushes one stick into the fire mouth; the grey-white sleeve at the door nudges the gap a little wider and stops; all lips stay closed",
         zh="主觀（屋門內往外看）、固定、前景門框：門縫外賴三抱著攪棍開始繞鍋攪；秦霜背影；許硯背對門口蹲在灶前添一根柴；右邊緣一隻灰白布袖（阿令）把門縫輕輕推大一點又停住；秦霜背影的台詞不對嘴（結尾）"),
    # ---- scene 2: the same shelter late at night (the moon low in the west, firelight) c15-c22, then just before dawn
    # (cold blue light from the back left, a low fire) c23-c26. Xu Yan on the low stool before the stove (middle right),
    # A-ling squats on the far side of the stove (left), Lai San at the wok and later by the fence.
    dict(chapter="顧鍋", loc="late", cam="Full shot, slow push in", chars=["laisan", "xuyan"], night="late",
         comp=f"full shot past the woodpile in the foreground: in the middle Lai San, {LAI}, his torn right sleeve hanging, walking round the steaming wok with the long stirring pole in his arms, nodding off; on screen right Xu Yan sitting on the low stool before the stove, {XU}, {NIGHT}, one thin stick of firewood in his hand",
         lines=[("xuyan", "手別停，鍋底一黏，這一整鍋就廢了。", "累，平穩")],
         motion="Lai San's head droops and his hands slow; Xu Yan taps the wok rim twice with the stick, and Lai San jerks awake and stirs faster again; Lai San's lips stay closed",
         zh="全景、慢推、前景柴堆：賴三抱攪棍繞鍋、睏得點頭，手慢下來；許硯坐灶前矮凳（眼睛發紅）用柴枝敲兩下鍋沿，賴三一驚、手又快起來"),
    dict(loc="late_c", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="late",
         comp=f"medium close-up, closing in to a close-up by the end, of Xu Yan sitting on the low stool, {XU}, {NIGHT}, unsmiling; behind him only the stove fire of the same cooking shelter",
         lines=[("xuyan", "系統，你只會派任務，不會幫忙添柴嗎？", "心裡話，嘴閉著，累", "inner")],
         motion="he rubs one eye with the back of his hand, gives one big yawn and looks at the fire mouth; then his lips stay closed",
         zh="近景、慢推（中近景推到近景）：許硯（眼睛發紅、眼下發青）用手背揉一下眼睛，打一個呵欠，往灶口看；心裡話，嘴閉著"),
    dict(loc="late_c", cam="Close-up, slow push in", chars=["xuyan"], night="late_fire",
         comp=f"close-up of Xu Yan on the low stool, {XU}, {NIGHT}, startled for a moment, unsmiling; behind him only the stove fire of the same cooking shelter",
         lines=[("xitong", "添柴不在服務範圍。宿主，火小了。", "冷淡，嫌棄，懶")],
         motion="he freezes, looks down at the fire mouth burning low, grabs two sticks of firewood and pushes them in, and sparks fly up; his lips stay closed",
         zh="近景、慢推：許硯愣一下，低頭看灶口火變小，趕緊抓起兩根柴推進去，火星往上竄；嘴閉著（script 寫「眼裡映一點淡藍光」：近景不寫光，只寫反應）"),
    dict(loc="late", cam="Medium shot, tracking", chars=["aling"], night="late",
         comp=f"medium shot, A-ling in her grey-white cotton dress with a plain wooden hairpin, {ALING}, unsmiling, at the house door on screen right; at the right edge of the frame one knee in a blue-grey robe by the stove",
         lines=[("aling", "你不打他，也不送官，就罰他攪鍋？", "冷，低")],
         motion="A-ling walks out of the house door, round the woodpile, squats on the far side of the stove, picks up one thin stick to poke the fire and looks at the seated man at the right edge",
         zh="中景、跟拍：阿令（灰白布裙、木簪、沒戴鐵鐐）從右邊屋門走出來，繞過柴堆，在灶的另一邊蹲下，右手撿一根細柴撥火，看著許硯；右邊緣許硯的膝蓋"),
    dict(loc="late", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "aling"], night="late",
         comp=f"over-the-shoulder shot from behind A-ling's shoulder and her plain wooden hairpin in the left foreground, Xu Yan on screen right on the low stool before the stove, {XU}, {NIGHT}, unsmiling",
         lines=[("xuyan", "打一頓，他還是錢府的人。讓他看著鍋成，他才會怕。", "累，平穩")],
         motion="Xu Yan sets one piece of firewood into the fire mouth and settles it, and only then looks up at her; A-ling's lips stay closed",
         zh="過肩（阿令肩後拍許硯）、慢推：許硯把一塊柴架進灶口、擺好，才抬頭看她；累、不笑"),
    dict(loc="late", cam="Over-the-shoulder medium shot, slow push in", chars=["aling", "xuyan"], night="late",
         comp=f"reverse over-the-shoulder shot from behind Xu Yan's shoulder in the right foreground, A-ling on screen left squatting by the stove, {ALING}, one thin stick of firewood in her right hand, unsmiling",
         lines=[("aling", "連要害你的人，你也給他留一條路。", "低，不解")],
         motion="her hand stops poking the fire; she turns her head to Lai San dozing by the wok off screen left, then turns back to Xu Yan; his lips stay closed",
         zh="反打（許硯肩後拍阿令）、慢推：阿令撥火的手停住，轉頭看鍋邊打瞌睡的賴三，再轉回來看許硯"),
    dict(loc="late_c", cam="Medium close-up to close-up, slow push in", chars=["xuyan", "laisan"], night="late",
         comp=f"medium close-up, closing in to a close-up by the end, of Xu Yan rising from the low stool by the wok, {XU}, {NIGHT}, unsmiling; at the left edge of the frame Lai San's hands in grey-brown sleeves round the long stirring pole; behind them only the white steam of the same cooking shelter",
         lines=[("xuyan", "他也是被人使喚的。真要算帳，我去找錢員外算。", "平靜")],
         motion="Xu Yan stands, glances into the wok, takes the pole out of Lai San's arms and stirs two rounds himself; Lai San drops back to sit by the bamboo fence; Lai San's lips stay closed",
         zh="近景、慢推（中近景推到近景）：許硯站起來往鍋裡看一眼，把攪棍從賴三懷裡接過來自己攪兩圈；賴三往後一坐、坐到籬笆邊"),
    dict(loc="late", cam="Low-angle medium shot, slow push in", chars=["aling", "xuyan"], night="late",
         comp=f"low-angle medium shot of A-ling squatting by the stove, {ALING}, unsmiling; in the background Xu Yan stirring the wok with the long pole, {NIGHT}",
         lines=[("xitong", "阿令，好感加三。", "冷淡")],
         panel=[("阿令 好感 +3 → 1", "panel")],
         motion="A-ling stands, brushes the dust off her hands and walks right to the house door; at the threshold she looks back at him once, and only then steps inside and out of the frame; all lips stay closed",
         zh="低角度中景、慢推：阿令站起身，拍掉手上的灰，往右邊屋門走，到門檻回頭看他一眼，才走進屋裡離開畫面；背景許硯攪鍋；嘴閉著、不笑"),
    dict(loc="dawn", cam="Full shot, slow push in", chars=["qinshuang", "xuyan", "laisan"], night="dawn",
         comp=f"full shot past the bamboo fence in the foreground: on screen right Qin Shuang at the house door, one old grey cloth outer coat draped over her shoulders, {KNIFE}, her high ponytail a little messy; in the middle Xu Yan sitting before the stove stirring the wok with the long pole, {XU}, {NIGHT}, {HAIR}; on screen left Lai San asleep against the bamboo fence",
         lines=[("qinshuang", "你一夜都沒闔眼？鍋又不會自己長腳跑掉。", "剛睡醒，皺眉")],
         motion=f"Qin Shuang pushes the door open and steps out, sees Xu Yan still at the stove, grabs {GOURD} from beside the door and tosses it to him; Xu Yan's lips stay closed",
         zh="全景、慢推、前景籬笆、天邊發白：秦霜（肩披舊灰布外衣、馬尾有點亂）推開屋門出來，看到許硯還坐在灶前攪鍋（額前散髮），從門邊抓起水葫蘆（褐色、木塞）朝他一拋；左邊賴三靠籬笆睡著"),
    dict(loc="dawn_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"medium close-up of Xu Yan on the low stool, {XU}, {NIGHT}, {HAIR}, his left hand on the long stirring pole, unsmiling; behind him only the low stove fire of the same cooking shelter",
         lines=[("xuyan", "火一斷，豬油就白熬了。妳扛來的豬，不能糟蹋。", "累，認真")],
         motion="his left hand lets go of the pole and his right hand catches the brown water gourd flying in; he pulls out the wooden stopper and takes one drink",
         zh="中近景、慢推：許硯左手放開攪棍、右手接住水葫蘆，拔開木塞喝一口；累、眼睛發紅"),
    dict(loc="dawn_c", cam="Medium close-up to close-up, slow push in", chars=["qinshuang"], night="dawn",
         comp=f"medium close-up, closing in to a close-up by the end, of Qin Shuang standing, one old grey cloth outer coat draped over her shoulders, {QIN}, her high ponytail a little messy, lips pressed together with the corners of her mouth turned down, brows drawn, a stubborn face, not smiling; at the left edge only Xu Yan's hand reaching in from off screen, in a rolled-up blue-grey sleeve, holding {POLE}; behind her only the wooden shelter post of the same cooking shelter",
         lines=[("qinshuang", "哼，算你還有點良心。喝完水，換我來顧。", "嘴硬")],
         motion="she turns her face aside, steps to the stove and with her right hand pulls the long wooden stirring pole out of Xu Yan's hand off screen at the left edge, then holds it upright beside her; she stays standing, stubborn, not smiling",
         zh="近景、慢推（中近景推到近景，e905 fix2）：秦霜（肩披舊灰布外衣、馬尾有點亂）別開臉，走到灶前右手把長攪棍從畫面左緣許硯手裡抽走，豎著拿在身邊；一直站著；抿嘴、嘴角往下、皺眉、嘴硬，不笑"),
    dict(loc="dawn_c", cam="Close-up, slow push in", chars=["xuyan", "qinshuang"], night="dawn",
         comp=f"close-up of Xu Yan, {XU}, {NIGHT}, {HAIR}, unsmiling; behind him, soft and out of focus, Qin Shuang seen from behind stirring the wok in the same cooking shelter",
         lines=[("xitong", "秦霜，好感加五。", "冷淡")],
         panel=[("秦霜 好感 +5 → 5", "panel")],
         motion="he nods, stoppers the water gourd and sets it beside the stove, stands up from the low stool, and only then looks up at Qin Shuang's back as she stirs; all lips stay closed",
         zh="近景、慢推：許硯點點頭，把水葫蘆塞好放在灶邊，站起來讓出矮凳，抬頭看秦霜攪鍋的背影（背景虛焦）；嘴閉著（結尾）"),
    # ---- scene 3: the same yard at sunrise, warm low light from the left, long shadows. The long board across the
    # middle under the persimmon tree, the house door on the right, the yard gate deep at the back left.
    dict(chapter="開模", loc="sun", cam="Full shot, tracking", chars=["xuyan", "qinshuang", "xiaohe"], night="sun",
         comp=f"full shot past persimmon branches in the foreground: Xu Yan, {XU}, {NIGHT}, and Qin Shuang, no outer coat now, {KNIFE}, carrying {MOULD} between them, one at each end; four more moulds stacked under the persimmon tree; little Xiaohe at the house door on screen right, hugging her straw rabbit in her left arm, smiling",
         lines=[("xiaohe", "哥，天亮了！快打開，我要看肥皂長什麼樣子！", "雀躍")],
         motion="Xu Yan and Qin Shuang carry the mould to the long board and bend together to set it down; Xiaohe runs from the house door to the board and rises on tiptoe; the others' lips stay closed",
         zh="全景、跟拍、前景柿子樹枝：許硯和秦霜（外衣已脫）一人一頭抬著倒扣的松木長木模，走到長木板邊同時彎腰放下；樹下疊著另外四個；小禾抱草兔從右邊屋門跑到木板邊踮腳（可以笑）"),
    dict(loc="sun", cam="Medium shot, tracking", chars=["tangxiaotang"], night="sun",
         comp=f"medium shot of Tang Xiaotang at the house door on screen right, {TANG_SHUT}, her small gold abacus hanging at her waist, {TANG_CALC}; the long wooden board on screen left",
         lines=[("tangxiaotang", "先說好，要是沒成，柴錢豬油錢都記你帳上。", "精明")],
         motion="Tang Xiaotang walks out of the door, unhooking the small gold abacus from her waist with both hands and tucking it under her left arm, then stops at the long board; serious, calculating, no smile",
         zh="中景、跟拍（e905 fix3）：唐小棠（t2，襦裙從立領扣到喉嚨、到腰一件闔上）推開屋門走出來，邊走邊用兩手把腰間的小金算盤取下夾在左腋下，走到長木板邊停住；整鏡嚴肅、在盤算：話與話之間嘴閉著、嘴角平、眉微壓、瞇眼，不笑不露齒"),
    dict(loc="sun_c", cam="Insert close-up, slow push in", chars=["xuyan"], nospeak=["xuyan"], night="sun",
         comp="low-angle insert close-up of the long wooden board, the shot opens directly on the long pine soap mould and Xu Yan's two hands from its very first frame: his two hands in his rolled-up blue-grey cuffs gripping both ends of the long mould turned upside down on the board; only the hands, cuffs and mould are in the frame, no face and no mouth; behind them only the warm sunrise light of the same yard",
         lines=[("xuyan", "記吧。要是成了，這一鍋就是我們還債的本錢。", "畫外，篤定")],
         motion=f"his hands lift the mould straight up, and three rows of thirty {SOAP_ST1} slide out onto the board, lit by the morning sun",
         zh="低角度手部特寫、慢推（第一格就是木模與許硯的兩隻手）：許硯兩手抓住木模兩端往上一提，三排共三十塊雪白方塊滑出來排在木板上，晨光照在上面；畫面上沒有嘴（script 的「手上沾著灰」不寫：皮膚上的小點會畫成黑點）"),
    dict(loc="sun_c", cam="Medium close-up, slow push in", chars=["xiaohe"], night="sun",
         comp=f"medium close-up of {HE}, her small straw rabbit tucked under her arm, one wooden basin of clear water before her, wide-eyed and smiling; behind her only the persimmon tree of the same yard",
         lines=[("xiaohe", "哥你看，會起泡泡！手搓兩下就滑滑的！", "笑")],
         motion="she picks up one white bar of soap in both hands, dips it in the basin and rubs it twice; a big puff of white foam rises and bubbles float into the sunlight",
         zh="中近景、慢推：小禾（草兔夾在腋下）兩手抓起一塊白皂浸進木盆搓兩下，一大團白泡沫冒起來、泡泡飄進陽光；睜大眼睛（可以笑）"),
    dict(loc="sun_c", cam="Close-up, slow push in", chars=["tangxiaotang"], night="sun",
         comp=f"close-up of Tang Xiaotang {COLLAR}, her peach-pink brocade ruqun; serious and shrewd, eyes narrowed in appraisal, lips closed between words, no smile and no teeth at any moment; the small gold abacus under her left arm; behind her only the persimmon tree of the same yard",
         lines=[("tangxiaotang", "又白又香。一塊賣三錢，縣城的太太會搶著要。", "精明")],
         motion=f"her right hand lifts {SOAP} under her nose and she sniffs it, left fingertips flicking three abacus beads; eyes narrowed, no smile",
         zh="近景、慢推（下巴以上，臉填滿畫面，e905 fix3）：畫面下緣是扣到喉嚨的立領頂端，一件闔上、領下沒有開口；唐小棠右手拿一塊雪白方皂（巴掌大、一指厚）湊到鼻下聞，左手指尖撥過左腋下算盤的三顆算珠；嚴肅、精明、瞇眼打量，不笑"),
    dict(loc="sun", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="sun",
         comp=f"over-the-shoulder shot from behind Tang Xiaotang's looped buns and pink silk ribbons in the left foreground, {TANG}; Xu Yan on screen right, {XU}, {NIGHT}, {HAIR}, unsmiling",
         lines=[("xuyan", "三錢？一斗米才幾十文，妳這價會不會太高？", "皺眉")],
         motion="Xu Yan walks over wiping his hands on the hem of his robe, stops and frowns; Tang Xiaotang's lips stay closed",
         zh="過肩（唐小棠肩後拍許硯）、慢推：許硯一邊用衣襬擦手一邊走過來，停步皺眉；累（script 的「手上沾著白色皂屑」不寫，只留擦手的動作）"),
    dict(loc="sun_c", cam="Over-the-shoulder close-up, slow push in", chars=["tangxiaotang", "xuyan"], night="sun",
         comp=f"reverse over-the-shoulder shot from behind Xu Yan's right shoulder in the right foreground, Tang Xiaotang on screen left in a close-up {COLLAR}, her peach-pink brocade ruqun; calm and certain, steady eyes, lips closed between words, no smile and no teeth at any moment; on the long wooden board before her only one row of identical soap bars, each {SOAP}; behind her only the persimmon tree of the same yard",
         lines=[("tangxiaotang", "便宜的東西沒人當寶。貴，她們才捨得拿出來炫耀。", "篤定")],
         motion=f"first she sets {SOAP} on the board in line with the others, then looks up at Xu Yan, no smile; his lips stay closed",
         zh="反打（許硯右肩後拍唐小棠）、慢推（唐小棠下巴以上，立領扣到喉嚨，e905 fix3）：一開始她把一塊雪白方皂（巴掌大、一指厚）放上木板、跟一排一樣的方皂對齊，才抬眼看許硯說話；木板上只有那排方皂；平靜、篤定、眼神穩，話與話之間嘴閉著，不笑"),
    dict(loc="sun", cam="Two-shot, tracking", chars=["xuyan", "laisan"], night="sun",
         comp=f"two-shot, Xu Yan, {XU}, {NIGHT}, one small piece of soap trimmed from the mould's edge, half the size of a bar and wrapped in one green leaf, in his right hand; Lai San, {LAI}, his torn sleeve hanging and his head-wrap askew, just getting up from beside the bamboo fence and limping toward the yard gate deep at the back left",
         lines=[("xuyan", "這塊帶回去給錢員外，叫他好好洗洗手。", "淡淡，帶刺")],
         motion="Xu Yan catches up, presses the leaf-wrapped soap into Lai San's hands and pats his shoulder; Lai San hugs the soap, hunches his neck and limps out through the yard gate and out of the frame; his lips stay closed",
         zh="雙人鏡、跟拍：許硯追上賴三，把綠葉包的碎皂（木模邊角削下來的，比整塊小一半）塞進他手裡，拍拍他的肩；賴三兩手抱著皂、縮著脖子一跛一跛溜出院門出畫"),
    dict(loc="sun", cam="Medium shot, slow push in", chars=["tangxiaotang", "aling", "xuyan"], night="sun",
         comp=f"medium shot, Tang Xiaotang on screen left, {TANG}, standing before one bamboo basket, smiling; at the back right A-ling, {ALING}, with empty bamboo baskets; at the right edge of the frame Xu Yan by the long board, {XU}",
         lines=[("tangxiaotang", "一共一百五十塊，賣得完，二十兩就還得上了！", "高興")],
         motion="Tang Xiaotang puts the leaf-wrapped bars into the basket one by one, counting; A-ling passes over an empty basket; Xu Yan picks up one white bar from the board",
         zh="中景、慢推：唐小棠把綠葉包好的白皂一塊塊放進竹籃、邊放邊數（可以笑）；阿令從屋裡拿出空籃疊好遞過來；許硯從木板上拿起一塊白皂捏在指間"),
    dict(loc="sun_c", cam="Extreme close-up, slow push in", chars=["xuyan"], night="sun",
         comp="extreme close-up of Xu Yan's eyes, the shot opens directly on his eyes from its very first frame, his eyes just beginning to crease into a smile; nothing else in the frame",
         lines=[("xitong", "叮。強制任務：成婚。今日午時前，婚書蓋印。", "冷，叮一聲")],
         panel=[("強制任務：成婚／今日午時前，婚書蓋印／成婚 0/3", "task")],
         motion="the eyes hold that beginning smile; only then a very faint pale red reflection appears in his pupils, and the smile drains out of his eyes as they widen and go still",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：許硯眼角剛要笑，才在瞳孔裡映出一點很淡的紅色反光，那一點笑收掉、眼睛睜大定住；周圍的聲音一下變小（剪接）"),
    dict(loc="sun_c", cam="Close-up, slow push in", chars=["xuyan"], night="sun",
         comp=f"close-up of Xu Yan, {XU}, {NIGHT}, {HAIR}, his face pale, unsmiling, one white bar of soap held between the fingers of his raised right hand; behind him only the persimmon tree of the same yard",
         lines=[("xuyan", "成婚……我只顧著熬鍋，把成親給忘了。", "心裡話，嘴閉著，發愣", "inner")],
         motion="the white bar slips from his fingers and drops out of the frame onto the board with a smack; his hand stays frozen in mid-air; his lips stay closed",
         zh="近景、慢推：許硯臉色發白，那塊白皂從他指間滑掉，「啪」地落在木板上；手停在半空；心裡話，嘴閉著"),
    dict(loc="sun_c", cam="Close-up, slow push in", chars=["xuyan"], night="sun",
         comp=f"close-up of Xu Yan, {XU}, {NIGHT}, his face pale, one bead of sweat at his temple, unsmiling; behind him only the persimmon tree of the same yard",
         lines=[("xitong", "本系統沒忘。忘了的，是宿主。", "冷，懶，句尾往下壓")],
         motion="he slowly bends down out of the frame, picks up the white bar and straightens back up with it in his hand; his lips stay closed",
         zh="近景、慢推：許硯（額角一滴汗）慢慢彎腰撿起那塊白皂，直起身；嘴閉著"),
    dict(loc="sun", cam="Two-shot, tracking", chars=["xuyan", "tangxiaotang"], night="sun",
         comp=f"two-shot, Xu Yan on screen left, {XU}, his face pale, one white bar of soap in his hand; Tang Xiaotang on screen right framed from the chin up, her high stand-up collar closed at her throat, {TANG}, the small gold abacus under her left arm, her eyes wide, unsmiling",
         lines=[("tangxiaotang", "今天是配婚令第三天，縣衙午時就關門了！", "驚")],
         motion="seeing his face, Tang Xiaotang grabs his sleeve with her right hand, and the abacus under her arm drops onto the board; Xu Yan's lips stay closed",
         zh="雙人鏡、跟拍（唐小棠近景下巴以上）：唐小棠看他臉色不對，伸右手一把抓住他的袖子，夾在腋下的算盤掉在木板上；眼睛瞪大，不笑"),
    dict(loc="sun", cam="Low-angle full shot, slow push in", chars=["xuyan", "tangxiaotang", "qinshuang", "aling", "xiaohe"], night="sun",
         comp=f"low-angle full shot past a row of white bars of soap on the long board in the foreground: Xu Yan in the middle, {XU}, {NIGHT}, his face pale, and Tang Xiaotang, {TANG}, still gripping his sleeve; behind them Qin Shuang, {KNIFE}, A-ling, {ALING}, and little Xiaohe with her straw rabbit",
         lines=[("xuyan", "離午時只剩三個時辰，今天這婚，非成不可。", "咬牙，下定決心")],
         motion="Xu Yan looks up at the new sun and grits his teeth; behind him Qin Shuang, A-ling and Xiaohe turn to him one by one, lips closed",
         zh="低角度全景、慢推、前景木板上一排白皂：許硯抬頭看剛升起的太陽，咬牙；唐小棠還抓著他的袖子；後面秦霜、阿令、小禾一個個轉頭看他（結尾，懸念到第 6 集）"),
]

HEAD = [
    "- 重製版 r2：照 `docs/videos/zhong-tian-qu-qi-e005-r2/script.md`（c01–c40 對應 s01–s40；含「2026-11-06 審稿後的修改」）；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。",
    "- 內部工作編號 905（`hailuo/*-dh-e905.json`、`colab/runs/e905/`）；發布 slug `zhong-tian-qu-qi-e005-r2`。不放集數、不放片名卡；c01 直接接第 4 集 c40（黑影回頭、水桶已經傾斜）。",
    "- 狀態：許硯袖子捲到手肘（全集），第一場兩手空空（s05 拿過水桶、s12 起攪棍），s15 起眼睛發紅、眼下發青，s23 起額前散髮，s35 拿起一塊白皂、s37 掉、s38 撿起；秦霜柴刀 s01 插在腰帶右邊，s02 飛出釘柱（s03–s07 腰帶空著），s08 起插回腰帶右邊，s23–s26 肩披舊灰布外衣；賴三（`laisan`）s02–s07 右袖被釘、s08 起破口垂下，s12–s21 抱攪棍，之後靠籬笆睡到 s34；阿令沒戴鐵鐐、袖子蓋住手腕，s14 只露一隻袖子，s18–s20 細柴；唐小棠 t2，s28–s39 算盤夾在左腋下；小禾 s27 左臂抱草兔，s30 起夾在腋下。",
    "- 皮膚上不寫小東西：script 的「手上沾著灰」（c29）、「手上沾著白色皂屑」（c32 與角色表）不寫（會畫成黑點），只留捲袖與 s32 用衣襬擦手；額角一滴汗（s38）照寫。",
    "- 長鏡要買的秒數（`r2.py` 的 BUY）：script.md 長鏡清單沒有超過 6 秒的鏡（6 秒整的照 `gen-dh` 買 6 秒）；s07、s24、s32、s37 8 秒（錄好的配音加半秒 6.2、6.4、6.8、6.5 秒，超過預設 6 秒）；s29 6 秒（畫外台詞的手部特寫，`gen-dh` 會給 5 秒）。其餘照 `gen-dh` 的 6 秒；眼睛大特寫 s36 兩拍動作，`gen-dh` 給 6 秒。",
    "- 系統句：近景、中景只寫反應（s17 script 的「眼裡映一點淡藍光」不寫；s22、s26、s38 只寫動作）；只有眼睛大特寫 s36 寫「瞳孔裡一點很淡的紅色反光」。",
]
FOOT = [
    "- 場景參考：全集都在院子 `set-xujia-yuan-t1`。第一、二場在院子東側灶棚（兩根棚柱在左、土灶與大鍋在中間、屋門在右，照第 4 集最後幾鏡的寫法，提示詞寫 dirt yard 對到院子的場景圖）：灶火橘光由下往上、冷月光從右上 → 後半夜月亮偏西 → 天快亮冷藍晨光從左後方；第三場柿子樹下的長木板，日出暖光從左邊低低照進來。近景背景都寫「同一個灶棚／院子」。",
    "- 灶棚夜景版不用補：script 清單 2 寫「灶棚若場景圖裡沒有，開拍前補一張」；第 4 集已經用同一張院子場景圖加文字拍過灶棚，照用。",
    "- 唐小棠一律用 `tangxiaotang-portrait-t2`（gen-dh 的 PORTRAIT 對照）；近景構圖寫「下巴以上」，中景以上寫「襦裙從立領到腰一件闔上」。",
    "- 賴三用 `laisan-portrait-t1`（gen-dh 的 DH 名單與預設 portrait 已有 `laisan`，不用另加對照）；第 4 集的黑影就是他，本集 s04 他自己報名字。",
    "- 阿令沒戴鐵鐐的定妝照：`aling-portrait-t1` 本身是沒有鐵鐐的半身像，照用，不另畫（script.md 清單 2 的「要補」不用做）。s14 門縫的袖子不放她的圖、不寫她的名字。",
    "- 秦霜的 `cast.json` 造型寫著「柴刀插在腰帶」：s03–s07 腰帶空著，`colab/runs/e905/extras.json` 把這句從每鏡的造型句拿掉（同第 3 集），柴刀在哪裡由各鏡構圖寫。小禾的「hugging a small woven straw rabbit」改成夾在腋下（s30 起），s27 由構圖寫左臂抱著。",
    "- 配樂：灶棚 tension（s02 柴刀釘柱一個重音）、顧鍋 quiet night（s22、s26 好感各一個輕的提示音）、開模 warm（s36「叮」音樂抽掉、留一個重音，s40 換 suspense 收尾）；音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy so the recorded lines (+0.5 s each) fit within buy - 0.3 s, allowing the cut's 1.1x
# slow-down (script.md 長鏡清單: no shot over 6 s, the 6-second ones c01, c12, c14, c21, c23, c27, c28, c34, c40 bought at
# 6, which gen-dh already does; the rest from the recorded audio, 2026-11-06).
BUY = {"s07": 8, "s24": 8, "s29": 6, "s32": 8, "s37": 8}
# Recorded need (wav + 0.5 s a line, 2026-11-06): s07 6.2, s24 6.4, s32 6.8, s37 6.5 -> 8. s29 (the off-screen insert) 4.6
# would get gen-dh's 5 and is bought at 6 like every other speaking shot. Within 0.4 s of buy - 0.3 and left at 6 (the
# cut's 1.1x covers them): s04 5.9, s06 5.8. s36, the eye extreme close-up, needs 4.75 and gets gen-dh's 6 (its motion has
# two beats: the smile, then the red reflection), not 5. The lines run at a median 3.7 zh characters a second.
