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
t2, the abacus under her left arm c28-c39; Xiaohe's straw rabbit in her left arm c27, under her arm from c30. No skin
bits (the script's 「手上沾著灰／白色皂屑」 c29, c32 are left out: they render as growths), no glow anywhere, no writing
anywhere. Opens on the next instant after e004 c40: the bucket already tipping over the wok.
Live action (live prep 2026-11-10: what e904 live paid four reshoot rounds for, route-a.md 2026-11-09/10, e904-live
cut-review.md and cut-review-2.md, e004-r2's live prep 2026-11-09 and fix1-fix4, e003-r2's e903 live fixes): every
visible face written part by part (brows, eyes, mouth corners, jaw, breath) with no smile word (no sweet, shrewd,
offhand, teasing, wry, eager, grin, softly); NOSMILE is the only smile word, on every shot that must not smile (the
allowed c04 fawning, c27/c30 Xiaohe and c35 Tang are written as face movements); a still reaction close-up never lowers
the head or swallows. Tang Xiaotang smiles on almost every line she says on camera, so her four lines the script will
not let her smile on (c28, c31, c33, c39) are shot from behind her, her mouth out of the frame, nospeak (the recording
is laid); only c35 shows her face. Xu Yan's c34 barb (淡淡，帶刺) is the same: from behind his shoulder, nospeak.
Speakers in profile or three-quarter toward the listener, the camera 40-70 degrees off the eyeline or over the
listener's shoulder, never the lens, framed from the chest or waist up with space above the head, locked (no push-in on
one face). The axis: scenes 1-2 the posts and Lai San on screen left, the wok in the middle, the house door, Xu Yan and
whoever comes out of it on screen right (c09/c10 and c19/c20 say whose which shoulder; the script's c09/c10 shoulders
crossed the line and are turned round); scene 3 Tang Xiaotang left of Xu Yan across the board, the gate deep at the back
left. Never mirror a shot that shows a Song collar (hflip makes it left over right). The one eye extreme close-up (c36)
is a still from c37's first frame, not shot (the e904 eye close-ups double-exposed and dissolved). Props counted as
counted, sized by the body, one phrase each, no marks or writing. Night: the sky black, the doorway dark inside; a
hidden face has the fire on the far side. A turn at the end of a shot is a profile away from the camera and the light.
Tang Xiaotang's costume is the portrait's (TANG, as e004: no collar sentence, which pilot.py refuses).
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
# Live prep 2026-11-10 (route-a.md 2026-11-07 夜景鏡看窗、門外、天空; e904 live cut review 二-3, the kitchen door that
# opened on daylight): every night location writes the sky black and the doorway dark inside; the dawn sky pales only
# at the horizon.
LOC = {
    "night": "In the dirt yard of the Xu farmhouse on a clear windless autumn night, at the cooking shelter on the east side of the yard: two wooden shelter posts on screen left, a clay stove in the middle with one big black iron wok on it giving off white steam, a woodpile, a bamboo fence and a persimmon tree, the house door and eaves on screen right with only darkness inside the doorway, the night sky above black with no daylight anywhere, lit from below by the warm orange glow of the stove fire and by cold moonlight from the upper right",
    "night_c": "At the cooking shelter in the dirt yard of the Xu farmhouse on an autumn night, the dark night beyond, lit by the warm orange stove fire and cold moonlight",
    "late": "In the dirt yard of the Xu farmhouse late on a clear autumn night, at the cooking shelter on the east side of the yard: two wooden shelter posts on screen left, a clay stove in the middle with the big black iron wok on it giving off white steam, one low stool before the stove, a woodpile and a bamboo fence, the house door on screen right with only darkness inside the doorway, the night sky above black, the moon low in the west, lit by the warm orange glow of the stove fire and cold moonlight",
    "late_c": "At the cooking shelter in the dirt yard of the Xu farmhouse late at night, the dark night beyond, lit by the warm orange stove fire and low cold moonlight",
    "dawn": "In the dirt yard of the Xu farmhouse just before dawn on a clear autumn day, at the cooking shelter on the east side of the yard: two wooden shelter posts on screen left, a clay stove in the middle with the big black iron wok giving off white steam and a low fire, one low stool before it, a bamboo fence, the house door on screen right, dark inside, the sky paling only at the horizon behind the fence and still deep blue above, cold blue dawn light from the back left",
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
# Live prep 2026-11-10: XU and TANG are e004's live phrases (both shoulders whole, e904 cut review 三; the portrait's
# costume, the owner's lock of 2026-11-08: no collar sentence, which pilot.py refuses); props sized by the body and
# written plain with no marks or writing (e904 cut review 2 二-1: the ingots cast with characters; 二-8 the carried wok
# grew to an umbrella); counts written as counted (e904 fix2-fix4: five ingots drawn as four).
XU = "his blue-grey scholar's robe with both shoulders whole, his sleeves rolled up to the elbows"
NIGHT = "red-eyed with faint shadows under his eyes, tired"
HAIR = "a few loose strands of hair fallen over his forehead"
LAI = "his grey-brown Song-dynasty cross-collared short jacket and old cloth head-wrap"
QIN = "her dark brown cross-collared short jacket, wide leather belt, black trousers, leather boots and high ponytail"
KNIFE = "her old chopping knife in the right side of her belt"
CHOP = "one old chopping knife, single-edged with a broad back, its plain iron blade about as long as a forearm with no marks or writing, its wooden handle wrapped in black cloth and its edge gleaming"
POLE = "one long plain wooden stirring pole taller than a man"
BUCKET = "one wooden bucket full of water, no wider than his chest"
ALING = "no shackles, her sleeves pulled down over her wrists"
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
HE = "little Xiaohe in her patched lilac short jacket with red-string pigtails and one front tooth missing"
GOURD = "one brown water gourd with a wooden stopper, no longer than a forearm"
MOULD = "one long plain pine soap mould turned upside down, about as long as a man's arm from shoulder to fingertips and as wide as a forearm is long, plain wood with no marks or writing"
# The soap: one phrase in every shot (the script's 雪白方塊，掌心大、一指厚，邊角方正，不透明、不發光).
SOAP = "a snow-white square bar of soap the size of a palm and one finger thick with square corners, opaque and not glowing, plain with no marks or writing"
# s29 counted: three rows of ten (the CG s31 drew a long brick, s33 white piano keys).
SOAP_ROWS = "exactly thirty snow-white palm-sized bars of soap in exactly three rows of ten, one two three, each bar apart, plain with no marks or writing"
ABACUS = "one small gold abacus no longer than her hand, plain with no marks or writing"
SCRAP = "one small scrap of white soap half the size of a bar, wrapped in one green leaf, small enough to hide in one palm"
# e004-r2 / e003-r2: a face that must not smile gets no smile word at all except this one ban (smile, smirk, grin,
# unsmiling, "no smile the whole shot" all came out as a smile in e901-e904 live).
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"

SHOTS = [
    # ---- scene 1: the cooking shelter, the second night (the instant after e004 c40), stove firelight from below and
    # cold moonlight from the upper right. Axis: posts on the left (Lai San), wok in the middle, house door on the right.
    # live prep 2026-11-10: Lai San's face must stay hidden, so he is seen from behind with the fire on his far side
    # (e904 fix1/fix2 s38/s40: the fire lit the figure's face whenever it was on the camera's side); faces small.
    dict(chapter="灶棚", loc="night", cam="Full shot from behind him, slow push in", chars=["laisan", "xuyan", "qinshuang"], nospeak=["xuyan"], night="night",
         comp=f"full shot from behind Lai San, everyone small in the frame: in the middle Lai San in {LAI}, standing on one low wooden stool by the steaming wok, seen from behind, his back to the camera, facing the wok and the stove fire, so the fire is on his far side and his back is a dark silhouette rimmed with orange, his face never turned toward the camera; {BUCKET} raised in both hands over the mouth of the wok; {POLE} leaning against the rim of the wok; nobody else by the wok; deep on screen right the shut plank door of the house under its eaves, firewood scattered on the ground just inside its threshold",
         lines=[("xuyan", "那一鍋是我們全家的命，你敢倒試試！", "畫外，厲聲，人在遠處")],
         motion=f"Lai San tips the bucket over the wok, his face toward the fire; the door on the right bursts open, Xu Yan kicks the firewood aside and runs out, Qin Shuang, knife in her belt, behind him into the eaves' shadow; all lips stay closed",
         zh="全景、慢推、前景竹籬笆：賴三（背對灶火、臉在暗處）站在板凳上，兩手把木水桶舉到鍋口、桶口往下傾；長木棍斜靠在鍋邊；右邊深處屋門猛地推開，許硯踢開門檻內一地的柴衝出來，秦霜（柴刀插在腰帶右邊）跟出來閃進屋簷陰影；許硯太遠、看不到嘴（台詞不對嘴）。live prep 2026-11-10：賴三的臉要藏，改從他背後拍（全景、從背後慢推），他面向鍋與灶火、火在他另一側，背影是勾橘光的黑剪影、臉不朝鏡頭（第 4 集 fix1、fix2：火在鏡頭這側就照亮臉）；人都小小的；屋門關著、門內與夜空都是暗的"),
    # live prep 2026-11-10: the knife sized by the body and plain (e904 cut review 2 二-1: the ingots cast with marks).
    dict(loc="night_c", cam="Insert close-up, locked", chars=["laisan"], night="night", act=3,
         comp="insert close-up of the wooden shelter post, the shot opens directly on Lai San's raised right hand and his grey-brown sleeve from its very first frame: his right hand gripping the rim of the raised wooden bucket, his grey-brown cotton sleeve and one section of the wooden post beside it; only the hand, sleeve, bucket rim and post are in the frame, his face out of the frame; behind them only the dark night of the same cooking shelter",
         lines=[],
         motion="one old chopping knife with a black-wrapped handle and a plain blade as long as a forearm flies in from the dark eaves on the right and thunks through the sleeve into the post; the arm jerks, the bucket tilts, a few drops spill",
         zh="手部特寫、固定（第一格就是舉桶的灰褐袖子）：賴三舉桶的右手與袖子、一截棚柱；舊柴刀（單刃寬背、木柄纏黑布、刃口發亮）從右邊屋簷暗處飛進來，「咚」地把袖子釘在棚柱上；手臂被扯住，水桶一歪，只濺出幾滴到地上、沒進鍋。live prep 2026-11-10：柴刀用身體量（刀身約一條前臂長）、素鐵、沒有花紋或字（第 4 集審片二-1 金錠鑄字）；背景寫夜色"),
    # live prep 2026-11-10: her face part by part, profile toward Lai San on the left, NOSMILE; the night behind her dark.
    dict(loc="night", cam="Medium shot, tracking", chars=["qinshuang", "laisan"], night="night",
         comp=f"medium shot framed from the waist up with space above her head, Qin Shuang stepping out of the shadow of the eaves on screen right, {QIN}, the right side of her belt empty, in profile facing screen left toward Lai San, the camera about 50 degrees off her eyeline, never the lens; cold: brows level and low, eyes narrowed and fixed on him, lips pressed thin between words, jaw set; at the left edge of the frame Lai San's raised arm, his grey-brown sleeve pinned to the wooden post by the chopping knife; behind her only the dark doorway and the black night",
         lines=[("qinshuang", "半夜摸進來倒水，你是嫌命太長了？", "冷")],
         motion=f"Qin Shuang strides out of the shadow toward screen left, rolling up her right sleeve as she walks, and stops one step before the wok, her eyes on Lai San; his lips stay closed; {NOSMILE}",
         zh="中景、跟拍（由右往左）：秦霜（腰帶右邊空著）從屋簷陰影大步走出來，邊走邊捲右手袖子，停在鍋前一步，盯著左邊的賴三；左邊緣賴三被釘住的手臂；冷。live prep 2026-11-10：腰以上、頭上留空；正側臉朝畫左的賴三、鏡頭偏離視線約 50°、不看鏡頭；冷逐部位寫：眉平壓低、眼睛瞇著盯他、字句之間嘴抿薄、下巴收；身後只有暗的門口與夜色；拿掉 unsmiling、改 NOSMILE"),
    # live prep 2026-11-10: the allowed fawning grin written as face movements, no smile word; locked, not a push-in on
    # one face; three-quarter toward Qin Shuang on the right.
    dict(loc="night_c", cam="Medium close-up, locked", chars=["laisan"], night="night",
         comp=f"medium close-up of Lai San framed from the chest up with space above his head, {LAI}, small and thin with a pointed chin, his right arm pinned above his head by the sleeve to the wooden post, his left hand still gripping the bucket's handle, his face three-quarter to screen right toward Qin Shuang off screen right, the camera about 45 degrees off his eyeline, never the lens; panicked and fawning: brows raised and drawn together in the middle, eyes darting, cheeks pushed up, lips stretched wide over clenched teeth, neck hunched; behind him only the wooden shelter post of the same cooking shelter",
         lines=[("laisan", "女俠饒命，小的賴三，只是路過想喝口水。", "慌，陪笑")],
         motion="he yanks his pinned right sleeve twice without freeing it, hunches his neck into his shoulders and bobs his head to her as he says the line, his eyes darting",
         zh="近景、慢推（中近景推到近景）：賴三右手臂被釘在頭頂、左手還抓著水桶提把，猛扯兩下右袖扯不動，脖子一縮擠出陪笑（本鏡可以陪笑）；身後只有棚柱。live prep 2026-11-10：慢推改固定中近景、頭上留空（不對單張臉推近）；四分之三側臉朝畫右的秦霜、鏡頭偏離視線約 45°、不看鏡頭；稿子允許的陪笑只寫成臉怎麼動、不寫笑字：眉毛上揚往中間皺、眼睛亂瞟、臉頰擠起、嘴咧開咬著牙、縮脖子"),
    # live prep 2026-11-10: from behind Lai San's right shoulder (left foreground), Xu Yan on the right as in s08;
    # his face part by part; he straightens with his head in the frame; NOSMILE.
    dict(loc="night", cam="Over-the-shoulder medium shot, locked", chars=["xuyan", "laisan"], night="night",
         comp=f"over-the-shoulder medium shot from behind Lai San's right shoulder: his shoulder and his old cloth head-wrap in the left foreground, his face out of the frame; Xu Yan on screen right before the low stool, framed from the chest up with space above his head, {XU}, his face three-quarter to screen left, looking up at Lai San, eyes on his face in the left foreground, never the lens; cold: brows drawn down, eyes hard and steady, lips pressed firm between words, jaw set; behind him only the dark doorway of the house and the black night",
         lines=[("xuyan", "口渴喝水，用得著扛一整桶站上板凳？", "冷")],
         motion=f"Xu Yan takes the wooden bucket out of Lai San's left hand with both hands, sets it on the ground beside him and straightens up, his head staying in the frame, then looks up at him; Lai San's lips stay closed; {NOSMILE}",
         zh="過肩（賴三肩後拍許硯）、慢推：許硯走到板凳前，伸雙手把水桶從賴三左手拿下來，轉身放到地上，再抬頭看他；冷、不笑。live prep 2026-11-10：寫明從賴三右肩後拍、肩與頭巾在畫左前景、他的臉不入鏡，許硯在畫右（跟 s08 同一邊）；慢推改固定、胸口以上頭上留空，放下水桶後直起身整顆頭在畫面裡；四分之三朝畫左、抬眼看他、不看鏡頭；冷：眉往下壓、眼神硬而穩、字句之間嘴抿緊、下巴收；身後是暗的屋門與夜色；NOSMILE"),
    # live prep 2026-11-10: a side two-shot square to their eyelines (the e903 fix design that held), both faces part by
    # part, the knife handle named, NOSMILE.
    dict(loc="night", cam="Side medium shot, locked", chars=["laisan", "qinshuang"], night="night",
         comp=f"side medium shot, both seen from the waist up with space above their heads, the camera square to their eyelines: Lai San on screen left pinned to the wooden post by his sleeve, his face three-quarter to screen right toward her, terrified: brows shot up, eyes wide, lips closed and trembling; Qin Shuang on screen right, {QIN}, in profile facing screen left toward him, never the lens, her left hand gripping his collar and her right hand on the black-wrapped handle of the chopping knife stuck in the post above his arm; fierce: brows slammed down, eyes narrowed, nostrils flared, lips pulled tight between words; behind them only the dark of the same cooking shelter",
         lines=[("qinshuang", "少廢話。誰叫你來的？不說，我先剁你一根手指。", "兇，逼問")],
         motion=f"Qin Shuang yanks his collar down with her left hand so he drops into a half-crouch on the stool, and her right hand tightens on the knife handle; Lai San's lips stay closed; {NOSMILE}",
         zh="中近景、慢推：秦霜左手揪住賴三衣領往下一拽，賴三被拽得半蹲在板凳上；右手握緊釘在柱上的刀柄。live prep 2026-11-10：改成側面雙人中景、固定、鏡頭跟兩人視線成直角（第 3 集 fix 穩住的設計）、腰以上頭上留空；賴三在左、四分之三朝她，嚇壞：眉毛挑高、眼睛睜大、嘴閉著發抖；秦霜在右、正側臉朝他、不看鏡頭，兇：眉往下壓、瞇眼、鼻翼張、字句之間嘴拉緊；NOSMILE"),
    # live prep 2026-11-10: low-angle medium close-up (chest up), not a push-in on one face; tears written part by part.
    dict(loc="night_c", cam="Low-angle medium close-up, locked", chars=["laisan"], night="night",
         comp=f"low-angle medium close-up from below the stool, Lai San framed from the chest up with space above his head, {LAI}, hunching his neck, his collar gripped by one hand in a dark brown cuff at the top edge of the frame, his face three-quarter to screen right toward Qin Shuang above him, the camera about 45 degrees off his eyeline, never the lens; terrified and close to tears: brows pulled up in the middle, eyes wet and wide, lower lip trembling between words, chin quivering; behind him only the wooden post and the dark of the same cooking shelter",
         lines=[("laisan", "是錢員外！他說這鍋要是成了，你們就還得出錢。", "哭腔")],
         motion=f"his eyes dart right to the hand gripping the knife handle, and his whole body gives a shudder as he blurts the line up to her; {NOSMILE}",
         zh="低角度近景（從板凳下往上拍）、慢推：賴三縮著脖子、衣領被畫面上緣秦霜的左手揪著，眼睛往右瞟一下握刀的手，整個人一抖；哭腔。live prep 2026-11-10：慢推改固定、胸口以上頭上留空；四分之三朝畫右上方的秦霜、鏡頭偏離視線約 45°、不看鏡頭；哭腔逐部位寫：眉心往上皺、眼睛濕而睜大、字句之間下唇發抖、下巴顫；NOSMILE（只有 s04 可以陪笑）"),
    # live prep 2026-11-10: locked; three faces part by part, Xu Yan three-quarter toward Qin Shuang; NOSMILE.
    dict(loc="night", cam="Medium shot, locked", chars=["laisan", "qinshuang", "xuyan"], night="night",
         comp=f"medium shot, all three seen from the waist up with space above their heads: Lai San on screen left by the wooden post, both his hands empty, his right sleeve still pinned to the post by {CHOP}, its blade sunk deep into the post and its handle sticking out toward Qin Shuang, his eyes wide, lips closed; Qin Shuang in the middle, her right hand gripping that handle, the right side of her belt empty, in profile, brows level, lips closed; Xu Yan on screen right, {XU}, his face three-quarter to screen left toward Qin Shuang, the camera about 50 degrees off his eyeline, never the lens; calm: brows level, eyes steady on her, lips firm between words",
         lines=[("xuyan", "果然是他。秦霜，刀收好，人別打。", "冷靜")],
         motion=f"Qin Shuang wrenches the knife out of the post; only then Lai San's sleeve rips open along the forearm as his arm drops; she slides the knife into her belt on the right, blade down; the others' lips stay closed; {NOSMILE}",
         zh="中景、慢推（e905 fix2）：賴三在左、兩手空空，右袖還被舊柴刀釘在棚柱上（刀身深深吃進柱子，裹黑布的刀柄朝秦霜伸出）；秦霜在中間右手握住刀柄把柴刀從柱上拔出來，賴三的右袖這才沿前臂撕開、手臂垂下；秦霜把刀刃朝下插進腰帶右邊；右邊許硯轉頭看秦霜說話，其他人嘴閉著。live prep 2026-11-10：慢推改固定、腰以上頭上留空；許硯四分之三朝畫左的秦霜、鏡頭偏離視線約 50°、不看鏡頭；冷靜：眉平、眼神穩、字句之間嘴抿；賴三眼睛睜大嘴閉、秦霜側臉眉平嘴閉；柴刀素鐵沒有字；拿掉 unsmiling、改 NOSMILE"),
    # live prep 2026-11-10: the axis. The CG shot put Xu Yan's shoulder in the left foreground and Qin Shuang on the
    # right, across the line from s08 (Qin left of Xu): now from behind Xu Yan's LEFT shoulder in the right foreground,
    # Qin Shuang on screen left, Lai San behind her at the back left.
    dict(loc="night", cam="Over-the-shoulder medium shot, locked", chars=["qinshuang", "xuyan", "laisan"], night="night",
         comp=f"over-the-shoulder medium shot from behind Xu Yan's left shoulder: his shoulder, his rolled-up sleeve and the back of his head in the right foreground, his face out of the frame; Qin Shuang on screen left, framed from the waist up with space above her head, {QIN}, {KNIFE}, her left hand gripping Lai San's collar, her face three-quarter to screen right toward Xu Yan, eyes on his face in the right foreground, never the lens; defiant: brows knitted, eyes glaring, lips pressed hard between words, jaw jutting; Lai San at the back left by the post, his torn sleeve hanging, lips closed",
         lines=[("qinshuang", "他要毀你的鍋，你還替他求情？", "不服")],
         motion=f"Qin Shuang lets go of the collar and Lai San drops onto the stool; she turns round to Xu Yan and glares at him; Lai San's lips stay closed; {NOSMILE}",
         zh="過肩（許硯肩後拍秦霜）、慢推：秦霜鬆開衣領，賴三跌坐在板凳上；秦霜轉過身來瞪許硯；不服、皺眉。live prep 2026-11-10：軸線——原本許硯的肩在畫左前景、秦霜在畫右，跟 s08（秦霜在許硯左邊）越軸；改從許硯左肩後拍，肩在畫右前景、臉不入鏡，秦霜在畫左、四分之三朝前景的許硯、不看鏡頭，賴三在左後；慢推改固定；不服：眉頭皺、瞪眼、字句之間嘴抿緊、下巴往前；NOSMILE"),
    # live prep 2026-11-10: the reverse of s09 from behind Qin Shuang's RIGHT shoulder in the left foreground, Xu Yan on
    # screen right (the CG reverse crossed the line the same way).
    dict(loc="night", cam="Over-the-shoulder medium shot, locked", chars=["xuyan", "qinshuang"], night="night",
         comp=f"reverse over-the-shoulder medium shot from behind Qin Shuang's right shoulder: her shoulder and high ponytail in the left foreground, her face out of the frame; Xu Yan on screen right, framed from the chest up with space above his head, {XU}, his face three-quarter to screen left toward her, eyes on her face in the left foreground, never the lens; low and urgent: brows drawn together, eyes steady, lips pressed between words, jaw tight; behind him only the dark doorway and the black night",
         lines=[("xuyan", "妳打傷他，明天錢員外就帶衙役來，說我們行兇。", "壓低聲音")],
         motion=f"Xu Yan takes one step forward, lowers his voice, jerks his chin once toward the village off screen right and looks back at her; Qin Shuang's lips stay closed; {NOSMILE}",
         zh="反打（秦霜肩後拍許硯）、慢推：許硯往前一步、壓低聲音，用下巴朝畫面右外（村口方向）一指。live prep 2026-11-10：軸線同 s09——改從秦霜右肩後拍，肩與馬尾在畫左前景、臉不入鏡，許硯在畫右、四分之三朝她、不看鏡頭；慢推改固定、胸口以上頭上留空；壓低聲音：眉頭收、眼神穩、字句之間嘴抿、下巴繃；下巴一指後回頭看她；NOSMILE"),
    # live prep 2026-11-10: locked medium close-up, three-quarter toward Xu Yan on the right; resentment part by part.
    dict(loc="night_c", cam="Medium close-up, locked", chars=["qinshuang"], night="night",
         comp=f"medium close-up of Qin Shuang framed from the chest up with space above her head, {QIN}, {KNIFE}, her face three-quarter to screen right toward Xu Yan off screen right, the camera about 45 degrees off her eyeline, never the lens; resentful: brows pulled down hard, eyes narrowed, lips tight between words, the corners of her mouth pulled down; behind her only the wooden shelter post of the same cooking shelter",
         lines=[("qinshuang", "那就這樣放他走？我扛回來那頭豬，豬油白熬了？", "不甘")],
         motion=f"she flicks her hand, steps back one pace and folds her arms across her chest, her eyes on him; {NOSMILE}",
         zh="近景、慢推（中近景推到近景）：秦霜甩一下手、退開一步，雙手抱胸；不笑。live prep 2026-11-10：慢推改固定中近景、頭上留空；四分之三朝畫右的許硯、鏡頭偏離視線約 45°、不看鏡頭；不甘：眉用力往下壓、瞇眼、字句之間嘴抿緊、嘴角往下；NOSMILE"),
    # live prep 2026-11-10: Xu Yan in profile toward Lai San on the left; faces part by part; NOSMILE.
    dict(loc="night", cam="Medium shot, tracking", chars=["xuyan", "laisan"], night="night",
         comp=f"medium shot framed with space above their heads, the shot opens directly on Xu Yan's right hand gripping {POLE} leaning against the rim of the steaming wok from its very first frame; Xu Yan, {XU}, his face in profile toward screen left, never the lens; cold and decided: brows level and low, eyes hard, lips pressed firm between words; Lai San sitting on the low stool at the left, his torn sleeve hanging, eyes wide, lips closed",
         lines=[("xuyan", "不放。罰他攪鍋，一圈都不准停，攪到天亮。", "冷，定下來")],
         motion=f"Xu Yan snatches up the pole, takes two steps left, shoves it into Lai San's arms, grabs the back of his collar and pushes him to stand before the wok; Lai San's lips stay closed; {NOSMILE}",
         zh="中景、跟拍（第一格是許硯抓住鍋邊長木棍的手）：許硯一把抓起斜靠在鍋邊的長木棍（比人高、木色），走兩步塞進賴三懷裡，抓住他後領推到鍋前站好。live prep 2026-11-10：頭上留空；許硯正側臉朝畫左的賴三、不看鏡頭；冷而定：眉平壓低、眼神硬、字句之間嘴抿緊；賴三眼睛睜大、嘴閉；NOSMILE"),
    # live prep 2026-11-10: locked medium close-up toward Xu Yan on the right; only the eyes drop (no head lowering);
    # dismay part by part ("his face crumples" read as nothing written).
    dict(loc="night_c", cam="Medium close-up, locked", chars=["laisan"], night="night",
         comp=f"medium close-up of Lai San framed from the chest up with space above his head, {LAI}, his torn right sleeve hanging, both arms round the long wooden stirring pole, his face three-quarter to screen right toward Xu Yan off screen right, the camera about 45 degrees off his eyeline, never the lens; dismayed: brows pulled up in the middle, the corners of his mouth dragged down, lower lip trembling between words; behind him only the white steam of the big wok in the same cooking shelter",
         lines=[("laisan", "攪到天亮？那我這雙手明天還要不要了？", "哀號")],
         motion=f"his eyes drop to the bubbling wok, then to his own trembling hands, then back up to him as he wails the line; {NOSMILE}",
         zh="近景、慢推（中近景推到近景）：賴三抱著攪棍，低頭看翻滾的鍋，再看看自己發抖的手，臉垮下來；身後是冒白氣的鍋。live prep 2026-11-10：慢推改固定中近景、頭上留空；四分之三朝畫右的許硯、鏡頭偏離視線約 45°、不看鏡頭；只有眼睛往下看鍋、看手再抬回來，頭不低；臉垮逐部位寫：眉心往上皺、嘴角往下拉、字句之間下唇發抖；NOSMILE"),
    # live prep 2026-11-10: the night outside black; the fire beyond all three so no face is lit.
    dict(loc="night", cam="Point-of-view full shot, locked", chars=["laisan", "qinshuang", "xuyan"], nospeak=["qinshuang"], night="night",
         comp="point-of-view full shot from inside the dark house through the narrow gap of the door, the dark door frame in the foreground: beyond it in the middle Lai San with the long stirring pole in his arms by the steaming wok; Qin Shuang seen from behind, her back to the door; Xu Yan squatting before the stove with his back to the door; the stove fire is beyond all three, so their backs are dark and no face is lit; the night sky above the fence black; at the right edge of the frame one grey-white cotton sleeve at the edge of the door",
         lines=[("qinshuang", "手斷了也得攪。天亮前停一下，我就剁一根。", "背影，冷")],
         motion=f"Lai San stirs round the wok; Xu Yan pushes one stick into the fire mouth; the grey-white sleeve nudges the door gap wider; all lips stay closed; {NOSMILE}",
         zh="主觀（屋門內往外看）、固定、前景門框：門縫外賴三抱著攪棍開始繞鍋攪；秦霜背影；許硯背對門口蹲在灶前添一根柴；右邊緣一隻灰白布袖（阿令）把門縫輕輕推大一點又停住；秦霜背影的台詞不對嘴（結尾）。live prep 2026-11-10：灶火在三個人的另一側，背影都是暗的、沒有一張臉被照亮；籬笆上的夜空是黑的；NOSMILE"),
    # ---- scene 2: the same shelter late at night (the moon low in the west, firelight) c15-c22, then just before dawn
    # (cold blue light from the back left, a low fire) c23-c26. Xu Yan on the low stool before the stove (middle right),
    # A-ling squats on the far side of the stove (left), Lai San at the wok and later by the fence.
    # live prep 2026-11-10: Xu Yan three-quarter toward Lai San on the left; faces part by part; NOSMILE.
    dict(chapter="顧鍋", loc="late", cam="Full shot, slow push in", chars=["laisan", "xuyan"], night="late",
         comp=f"full shot past the woodpile in the foreground, both small in the frame: in the middle Lai San, {LAI}, his torn right sleeve hanging, walking round the steaming wok with the long stirring pole in his arms, nodding off, eyes drooping, lips closed; on screen right Xu Yan sitting on the low stool before the stove, {XU}, {NIGHT}, one thin stick of firewood in his hand, his face three-quarter to screen left toward Lai San, never the lens; tired and level: heavy eyelids, brows level, lips set between words",
         lines=[("xuyan", "手別停，鍋底一黏，這一整鍋就廢了。", "累，平穩")],
         motion=f"Lai San's head droops and his hands slow; Xu Yan taps the wok rim twice with the stick, and Lai San jerks awake and stirs faster again; Lai San's lips stay closed; {NOSMILE}",
         zh="全景、慢推、前景柴堆：賴三抱攪棍繞鍋、睏得點頭，手慢下來；許硯坐灶前矮凳（眼睛發紅）用柴枝敲兩下鍋沿，賴三一驚、手又快起來。live prep 2026-11-10：兩人小小的；許硯四分之三朝畫左的賴三、不看鏡頭；累而平穩：眼皮重、眉平、字句之間嘴抿；賴三眼皮垂、嘴閉；NOSMILE"),
    # live prep 2026-11-10: a thought in voice-over: the yawn goes (an open mouth under a thought reads as speaking, e904
    # cut review 二-5 s03); a side medium close-up about 60 degrees, his head still; NOSMILE.
    dict(loc="late_c", cam="Side medium close-up, locked", chars=["xuyan"], night="late",
         comp=f"side medium close-up of Xu Yan sitting on the low stool, framed from the chest up with space above his head, {XU}, {NIGHT}, his face in profile toward the fire mouth on screen left, the camera about 60 degrees off his eyeline, never the lens; worn out: heavy eyelids, brows drawn together, lips closed the whole shot; behind him only the dark of the same cooking shelter, the stove fire lighting his face from screen left",
         lines=[("xuyan", "系統，你只會派任務，不會幫忙添柴嗎？", "心裡話，嘴閉著，累", "inner")],
         motion=f"he rubs one eye with the back of his hand, rests the hand on his knee and stares at the fire mouth, his head still; his lips stay closed; {NOSMILE}",
         zh="近景、慢推（中近景推到近景）：許硯（眼睛發紅、眼下發青）用手背揉一下眼睛，打一個呵欠，往灶口看；心裡話，嘴閉著。live prep 2026-11-10：拿掉呵欠（心裡話時嘴張開會像在講話，第 4 集審片二-5 s03）；改側面中近景、固定、鏡頭偏離視線約 60°、正側臉朝畫左的灶口；累：眼皮重、眉頭皺、嘴整鏡閉著；揉完眼手放回膝上、頭不動；NOSMILE"),
    # live prep 2026-11-10: medium close-up so the hands and the fire mouth are in; startle part by part; NOSMILE.
    dict(loc="late_c", cam="Medium close-up, locked", chars=["xuyan"], night="late_fire",
         comp=f"medium close-up of Xu Yan on the low stool, framed from the chest up with space above his head and the glowing fire mouth at the lower left of the frame, {XU}, {NIGHT}, his face in three-quarter profile toward the fire mouth, never the lens; startled for a moment: brows jumping up, eyes widening, lips closed; behind him only the dark of the same cooking shelter",
         lines=[("xitong", "添柴不在服務範圍。宿主，火小了。", "冷淡，嫌棄，懶")],
         motion=f"he freezes, his eyes drop to the fire mouth burning low, he grabs two sticks of firewood and pushes them in, and sparks fly up; his lips stay closed; {NOSMILE}",
         zh="近景、慢推：許硯愣一下，低頭看灶口火變小，趕緊抓起兩根柴推進去，火星往上竄；嘴閉著（script 寫「眼裡映一點淡藍光」：近景不寫光，只寫反應）。live prep 2026-11-10：改固定中近景、頭上留空，灶口在畫面左下；四分之三朝灶口、不看鏡頭；愣一下：眉毛一跳、眼睛睜大、嘴閉；只有眼睛往下看灶口；NOSMILE"),
    # live prep 2026-11-10: her face part by part in profile toward Xu Yan at the right edge; the doorway dark.
    dict(loc="late", cam="Medium shot, tracking", chars=["aling"], night="late",
         comp=f"medium shot framed from the waist up with space above her head, A-ling in her grey-white cotton dress with a plain wooden hairpin, {ALING}, at the house door on screen right, the doorway behind her dark inside; at the right edge of the frame one knee in a blue-grey robe by the stove; once she squats, her face in profile toward screen right toward that seated man, the camera about 50 degrees off her eyeline, never the lens; cold and low: brows level, eyes cool, lips flat between words, jaw still",
         lines=[("aling", "你不打他，也不送官，就罰他攪鍋？", "冷，低")],
         motion=f"A-ling walks out of the dark doorway, round the woodpile, squats on the far side of the stove, picks up one thin stick to poke the fire and looks at the seated man at the right edge; {NOSMILE}",
         zh="中景、跟拍：阿令（灰白布裙、木簪、沒戴鐵鐐）從右邊屋門走出來，繞過柴堆，在灶的另一邊蹲下，右手撿一根細柴撥火，看著許硯；右邊緣許硯的膝蓋。live prep 2026-11-10：腰以上頭上留空；門內是暗的；蹲下後正側臉朝畫右的許硯、鏡頭偏離視線約 50°、不看鏡頭；冷而低：眉平、眼神冷、字句之間嘴抿平、下巴不動；拿掉 unsmiling、改 NOSMILE"),
    # live prep 2026-11-10: from behind A-ling's RIGHT shoulder (left foreground), Xu Yan on screen right: she is left
    # of the stove, he right (s18, s20); locked, his face part by part; NOSMILE.
    dict(loc="late", cam="Over-the-shoulder medium shot, locked", chars=["xuyan", "aling"], night="late",
         comp=f"over-the-shoulder medium shot from behind A-ling's right shoulder: her shoulder and her plain wooden hairpin in the left foreground, her face out of the frame; Xu Yan on screen right on the low stool before the stove, framed from the chest up with space above his head, {XU}, {NIGHT}, his face three-quarter to screen left toward her, eyes on her face in the left foreground, never the lens; tired and steady: heavy eyelids, brows level, lips pressed between words, jaw calm",
         lines=[("xuyan", "打一頓，他還是錢府的人。讓他看著鍋成，他才會怕。", "累，平穩")],
         motion=f"Xu Yan sets one piece of firewood into the fire mouth and settles it, and only then looks up at her; A-ling's lips stay closed; {NOSMILE}",
         zh="過肩（阿令肩後拍許硯）、慢推：許硯把一塊柴架進灶口、擺好，才抬頭看她；累、不笑。live prep 2026-11-10：寫明從阿令右肩後拍（她在灶左、他在灶右，同 s18、s20），肩與木簪在畫左前景、臉不入鏡；慢推改固定、胸口以上頭上留空；四分之三朝前景的她、不看鏡頭；累而穩：眼皮重、眉平、字句之間嘴抿、下巴放鬆；NOSMILE"),
    # live prep 2026-11-10: the reverse from behind Xu Yan's LEFT shoulder (right foreground), A-ling on screen left.
    dict(loc="late", cam="Over-the-shoulder medium shot, locked", chars=["aling", "xuyan"], night="late",
         comp=f"reverse over-the-shoulder medium shot from behind Xu Yan's left shoulder: his shoulder in the right foreground, his face out of the frame; A-ling on screen left squatting by the stove, framed from the chest up with space above her head, {ALING}, one thin stick of firewood in her right hand, her face three-quarter to screen right toward him, never the lens; puzzled and low: brows drawn together, eyes searching his face, lips flat between words",
         lines=[("aling", "連要害你的人，你也給他留一條路。", "低，不解")],
         motion=f"her hand stops poking the fire; she turns her head to Lai San dozing by the wok off screen left, then turns back to Xu Yan; his lips stay closed; {NOSMILE}",
         zh="反打（許硯肩後拍阿令）、慢推：阿令撥火的手停住，轉頭看鍋邊打瞌睡的賴三，再轉回來看許硯。live prep 2026-11-10：寫明從許硯左肩後拍，肩在畫右前景、臉不入鏡，阿令在畫左；慢推改固定、胸口以上頭上留空；四分之三朝他、不看鏡頭；不解：眉頭往中間皺、眼睛盯著他的臉、字句之間嘴抿平；NOSMILE"),
    # live prep 2026-11-10: he stands up in the shot, so a medium shot with room above his head (the face left the frame
    # while speaking, e004 s05, s19, s30); three-quarter toward A-ling off screen left; NOSMILE.
    dict(loc="late_c", cam="Medium shot, locked", chars=["xuyan", "laisan"], night="late",
         comp=f"medium shot of Xu Yan framed from the waist up with clear space above his head so his whole head stays in the frame after he stands, {XU}, {NIGHT}, by the steaming wok, his face three-quarter to screen left toward A-ling off screen left, the camera about 45 degrees off his eyeline, never the lens; calm: brows level, eyes steady, lips firm between words, jaw relaxed; at the left edge of the frame Lai San's hands in grey-brown sleeves round the long stirring pole; behind them only the white steam and the dark of the same cooking shelter",
         lines=[("xuyan", "他也是被人使喚的。真要算帳，我去找錢員外算。", "平靜")],
         motion=f"Xu Yan stands up from the low stool, glances into the wok, takes the pole out of Lai San's arms and stirs two rounds himself; Lai San drops back to sit by the bamboo fence, lips closed; {NOSMILE}",
         zh="近景、慢推（中近景推到近景）：許硯站起來往鍋裡看一眼，把攪棍從賴三懷裡接過來自己攪兩圈；賴三往後一坐、坐到籬笆邊。live prep 2026-11-10：他在鏡中站起來，改固定中景、腰以上、頭上留夠空間（第 4 集 s05、s19、s30 站起來臉出畫）；四分之三朝畫左的阿令、鏡頭偏離視線約 45°、不看鏡頭；平靜：眉平、眼神穩、字句之間嘴抿、下巴放鬆；NOSMILE"),
    # live prep 2026-11-10: a side low-angle shot square to her path, so the look back at the threshold is a profile and
    # never a turn to the lens (e904 s09, s25 turned to the camera at the end); the doorway dark; NOSMILE.
    dict(loc="late", cam="Low-angle side medium shot, locked", chars=["aling", "xuyan"], night="late",
         comp=f"low-angle side medium shot, the camera square to her path: A-ling squatting by the stove, {ALING}, her face in profile toward Xu Yan, never the lens; quiet: brows level, eyes on him, lips closed, the corners of her mouth level; in the background Xu Yan stirring the wok with the long pole, {NIGHT}, lips closed; on screen right the house door, dark inside",
         lines=[("xitong", "阿令，好感加三。", "冷淡")],
         panel=[("阿令 好感 +3 → 1", "panel")],
         motion=f"A-ling stands, brushes her hands, walks to the door, turns only her head into profile toward Xu Yan, not to the lens, and steps into the dark door; {NOSMILE}",
         zh="低角度中景、慢推：阿令站起身，拍掉手上的灰，往右邊屋門走，到門檻回頭看他一眼，才走進屋裡離開畫面；背景許硯攪鍋；嘴閉著、不笑。live prep 2026-11-10：改低角度側面中景、固定、鏡頭跟她走的方向成直角，門檻那一下回頭只轉頭到正側臉朝許硯、不往鏡頭轉（第 4 集 s09、s25 鏡尾轉向鏡頭）；門內是暗的；她的臉：眉平、眼睛看他、嘴閉、嘴角平；NOSMILE"),
    # live prep 2026-11-10: three faces part by part; Qin Shuang in profile toward Xu Yan on the left; the gourd sized.
    dict(loc="dawn", cam="Full shot, slow push in", chars=["qinshuang", "xuyan", "laisan"], night="dawn",
         comp=f"full shot past the bamboo fence in the foreground, everyone small in the frame: on screen right Qin Shuang at the house door, one old grey cloth outer coat draped over her shoulders, {KNIFE}, her high ponytail a little messy, her face in profile toward Xu Yan on screen left, never the lens; just woken and frowning: brows knitted, eyes narrowed, lips pressed between words; in the middle Xu Yan sitting before the stove stirring the wok with the long pole, {XU}, {NIGHT}, {HAIR}, lips closed; on screen left Lai San asleep against the bamboo fence, eyes closed",
         lines=[("qinshuang", "你一夜都沒闔眼？鍋又不會自己長腳跑掉。", "剛睡醒，皺眉")],
         motion=f"Qin Shuang steps out of the door, sees Xu Yan still at the stove, grabs {GOURD} from beside the door and tosses it to him; Xu Yan's lips stay closed; {NOSMILE}",
         zh="全景、慢推、前景籬笆、天邊發白：秦霜（肩披舊灰布外衣、馬尾有點亂）推開屋門出來，看到許硯還坐在灶前攪鍋（額前散髮），從門邊抓起水葫蘆（褐色、木塞）朝他一拋；左邊賴三靠籬笆睡著。live prep 2026-11-10：人都小小的；秦霜正側臉朝畫左的許硯、不看鏡頭，剛睡醒皺眉：眉頭皺、瞇眼、字句之間嘴抿；許硯嘴閉；賴三閉眼；天只在籬笆後的地平線發白、上面仍是深藍，門內是暗的；水葫蘆不比前臂長；NOSMILE"),
    # live prep 2026-11-10: a caring line (the kind e904 s26's thank-you grinned on): a side medium shot about 60 degrees
    # off his eyeline, his face smaller (e903 fix3/fix4: the design that held), no upward face word; NOSMILE.
    dict(loc="dawn_c", cam="Side medium shot, locked", chars=["xuyan"], night="dawn",
         comp=f"side medium shot of Xu Yan on the low stool, framed from the waist up with space above his head and small in the frame, {XU}, {NIGHT}, {HAIR}, his left hand on the long stirring pole, his face in profile toward Qin Shuang off screen right, the camera about 60 degrees off his eyeline, never the lens; tired and earnest: heavy eyelids, brows drawn a little together, eyes steady, lips pressing together between phrases, jaw firm; behind him only the low stove fire and the cold dawn of the same cooking shelter",
         lines=[("xuyan", "火一斷，豬油就白熬了。妳扛來的豬，不能糟蹋。", "累，認真")],
         motion=f"his left hand lets go of the pole and his right hand catches the brown water gourd flying in; he pulls out the stopper, takes one drink and lowers it; {NOSMILE}",
         zh="中近景、慢推：許硯左手放開攪棍、右手接住水葫蘆，拔開木塞喝一口；累、眼睛發紅。live prep 2026-11-10：這是一句心疼人的話（第 4 集 s26 道謝那句整句咧嘴笑），改側面中景、固定、腰以上、人小一點、鏡頭偏離視線約 60°（第 3 集 fix3、fix4 穩住的設計），正側臉朝畫右的秦霜、不看鏡頭；累而認真：眼皮重、眉頭微收、眼神穩、字句之間嘴抿、下巴收；不寫任何往上的臉部字；喝完放下水葫蘆再說；NOSMILE"),
    # live prep 2026-11-10: her 嘴硬 line is the kind that turns into a smile: a side medium shot about 60 degrees, the
    # face written down-turned part by part (no "stubborn face, not smiling"); NOSMILE.
    dict(loc="dawn_c", cam="Side medium shot, locked", chars=["qinshuang"], night="dawn",
         comp=f"side medium shot of Qin Shuang standing, framed from the waist up with space above her head, one old grey cloth outer coat draped over her shoulders, {QIN}, her high ponytail a little messy, in profile facing screen left toward Xu Yan, the camera about 60 degrees off her eyeline, never the lens; gruff: brows drawn down, eyes narrowed, lips pressed tight between words, the corners of her mouth pulled down, a short huff through her nose; at the left edge only Xu Yan's hand in a rolled-up blue-grey sleeve holding {POLE}; behind her only the wooden shelter post of the same cooking shelter",
         lines=[("qinshuang", "哼，算你還有點良心。喝完水，換我來顧。", "嘴硬")],
         motion=f"she glances aside and back at him, steps to the stove and with her right hand pulls the stirring pole out of Xu Yan's hand at the left edge, holding it upright beside her; {NOSMILE}",
         zh="近景、慢推（中近景推到近景，e905 fix2）：秦霜（肩披舊灰布外衣、馬尾有點亂）別開臉，走到灶前右手把長攪棍從畫面左緣許硯手裡抽走，豎著拿在身邊；一直站著；抿嘴、嘴角往下、皺眉、嘴硬，不笑。live prep 2026-11-10：嘴硬的台詞最容易變笑，改側面中景、固定、腰以上、鏡頭偏離視線約 60°，正側臉朝畫左的許硯、不看鏡頭；臉逐部位寫：眉往下、瞇眼、字句之間嘴抿緊、嘴角往下、鼻子哼一聲（拿掉 stubborn face, not smiling）；別開臉寫成眼睛往旁邊一瞟再回來；NOSMILE"),
    # live prep 2026-11-10: a still reaction: no nod (a head movement in a reaction shot became a closed-mouth smile, e904
    # fix1 s23); a side medium shot, he stands with his head in the frame and holds still; NOSMILE.
    dict(loc="dawn_c", cam="Side medium shot, locked", chars=["xuyan", "qinshuang"], night="dawn",
         comp=f"side medium shot of Xu Yan sitting on the low stool on screen left, framed from the waist up with clear space above his head so his whole head stays in the frame after he stands, {XU}, {NIGHT}, {HAIR}, in profile facing screen right, never the lens; his face: brows level, eyes on Qin Shuang's back, lips closed in a flat line, the corners of his mouth level; behind him on screen right, soft and out of focus, Qin Shuang seen from behind stirring the wok in the same cooking shelter",
         lines=[("xitong", "秦霜，好感加五。", "冷淡")],
         panel=[("秦霜 好感 +5 → 5", "panel")],
         motion=f"he stoppers the gourd, sets it by the stove and stands up, then holds still, eyes on her back, head level; lips closed; {NOSMILE}",
         zh="近景、慢推：許硯點點頭，把水葫蘆塞好放在灶邊，站起來讓出矮凳，抬頭看秦霜攪鍋的背影（背景虛焦）；嘴閉著（結尾）。live prep 2026-11-10：反應鏡不寫頭的動作，拿掉點頭（第 4 集 fix1 s23 一低頭就變閉嘴微笑）；改側面中景、固定、腰以上頭上留空，站起來後整顆頭在畫面裡，然後定住看她的背影；臉：眉平、嘴閉成一線、嘴角平；NOSMILE"),
    # ---- scene 3: the same yard at sunrise, warm low light from the left, long shadows. The long board across the
    # middle under the persimmon tree, the house door on the right, the yard gate deep at the back left.
    # live prep 2026-11-10: the allowed smile written as face movements; the mould sized by the body; the four other
    # moulds counted; Xu Yan and Qin Shuang's faces written.
    dict(chapter="開模", loc="sun", cam="Full shot, tracking", chars=["xuyan", "qinshuang", "xiaohe"], night="sun",
         comp=f"full shot past persimmon branches in the foreground, everyone small in the frame: Xu Yan, {XU}, {NIGHT}, and Qin Shuang, no outer coat now, {KNIFE}, carrying {MOULD} flat between them at waist height, one at each end, both looking at the board, lips closed; under the persimmon tree exactly four more moulds of the same size stacked one on another, one two three four; little Xiaohe at the house door on screen right, hugging her straw rabbit in her left arm, her face three-quarter to screen left toward Xu Yan, never the lens; delighted: eyes wide and shining, brows high, mouth open wide, cheeks lifting",
         lines=[("xiaohe", "哥，天亮了！快打開，我要看肥皂長什麼樣子！", "雀躍")],
         motion="Xu Yan and Qin Shuang carry the mould to the long board and bend together to set it down; Xiaohe runs from the house door to the board and rises on tiptoe; the others' lips stay closed",
         zh="全景、跟拍、前景柿子樹枝：許硯和秦霜（外衣已脫）一人一頭抬著倒扣的松木長木模，走到長木板邊同時彎腰放下；樹下疊著另外四個；小禾抱草兔從右邊屋門跑到木板邊踮腳（可以笑）。live prep 2026-11-10：木模用身體量（約一條手臂從肩到指尖長、一條前臂寬）、素木沒有字；樹下的四個寫成「正好四個、一二三四、疊在一起、一樣大」；小禾可以笑，只寫成臉怎麼動（眼睛睜大發亮、眉毛高、嘴張大、臉頰往上），不寫笑字，四分之三朝畫左的許硯；許硯、秦霜看木板、嘴閉"),
    # live prep 2026-11-10: 精明, not a smile, so her mouth leaves the shot: from the house doorway behind her as she walks
    # out (e904 fix3 s16: the design that held), nospeak, the recording laid; Xu Yan at the board facing her.
    dict(loc="sun", cam="Medium shot from behind her, tracking", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="sun",
         comp=f"medium shot from the house doorway behind Tang Xiaotang, both small in the frame: her back, the back of her head with its two looped buns and pink ribbons, and her shoulders in the right foreground, her face turned away from the camera the whole shot, {TANG}, {ABACUS} hanging at her waist; ahead of her at the long wooden board on screen left Xu Yan, {XU}, {NIGHT}, his face three-quarter to screen right toward her, never the lens; tired: heavy eyelids, brows drawn together, lips closed; behind him the persimmon tree of the same sunny yard",
         lines=[("tangxiaotang", "先說好，要是沒成，柴錢豬油錢都記你帳上。", "精明")],
         motion=f"Tang Xiaotang walks off to the board, tucking the abacus from her waist under her left arm, the back of her head to the camera; his lips stay closed; {NOSMILE}",
         zh="中景、跟拍（e905 fix3）：唐小棠（t2，襦裙從立領扣到喉嚨、到腰一件闔上）推開屋門走出來，邊走邊用兩手把腰間的小金算盤取下夾在左腋下，走到長木板邊停住；整鏡嚴肅、在盤算：話與話之間嘴閉著、嘴角平、眉微壓、瞇眼，不笑不露齒。live prep 2026-11-10：唐小棠在鏡頭上講話幾乎每句都笑（第 4 集 fix1、fix2），這句稿子不准笑，她的嘴不入鏡：從屋門口在她背後拍，她背對鏡頭走向木板，畫右前景是她的背、後腦兩個髮髻與粉色緞帶；許硯在左邊木板旁、四分之三朝她、眼皮重、皺眉、嘴閉；她的台詞照錄音放（nospeak）；服裝改 TANG（定妝照的交領短襦闔上、百褶裙繫蝴蝶結，拿掉立領句，pilot.py 會擋）；算盤不比她的手長、沒有字；拿掉 TANG_CALC 的笑字；NOSMILE"),
    # live prep 2026-11-10: the thirty bars counted as three rows of ten, plain; the mould the same phrase as s27.
    dict(loc="sun_c", cam="Insert close-up, slow push in", chars=["xuyan"], nospeak=["xuyan"], night="sun",
         comp=f"low-angle insert close-up of the long wooden board, the shot opens directly on the long pine soap mould and Xu Yan's two hands from its very first frame: {MOULD}, lying on the board, his two hands in his rolled-up blue-grey cuffs gripping both ends of it; only the hands, cuffs and mould are in the frame, no face and no mouth; behind them only the warm sunrise light of the same yard",
         lines=[("xuyan", "記吧。要是成了，這一鍋就是我們還債的本錢。", "畫外，篤定")],
         motion=f"his hands lift the mould straight up, and {SOAP_ROWS} slide out onto the board in the morning sun",
         zh="低角度手部特寫、慢推（第一格就是木模與許硯的兩隻手）：許硯兩手抓住木模兩端往上一提，三排共三十塊雪白方塊滑出來排在木板上，晨光照在上面；畫面上沒有嘴（script 的「手上沾著灰」不寫：皮膚上的小點會畫成黑點）。live prep 2026-11-10：三十塊照數的寫：正好三排、一二三、每排十塊、塊與塊分開、素白沒有字（第 4 集五錠常畫成四錠）；木模同 s27 一句（用身體量）"),
    # live prep 2026-11-10: the allowed smile as face movements, three-quarter toward Xu Yan off screen left.
    dict(loc="sun_c", cam="Medium close-up, slow push in", chars=["xiaohe"], night="sun",
         comp=f"medium close-up of {HE}, framed from the chest up with space above her head, her small straw rabbit tucked under her arm, one wooden basin of clear water before her, her face three-quarter to screen left toward Xu Yan off screen left, the camera about 40 degrees off her eyeline, never the lens; thrilled: eyes wide and shining, brows high, mouth open wide in delight, cheeks lifting; behind her only the persimmon tree of the same yard",
         lines=[("xiaohe", "哥你看，會起泡泡！手搓兩下就滑滑的！", "笑")],
         motion="she picks up one white bar of soap in both hands, dips it in the basin and rubs it twice; a big puff of white foam rises and bubbles float into the sunlight",
         zh="中近景、慢推：小禾（草兔夾在腋下）兩手抓起一塊白皂浸進木盆搓兩下，一大團白泡沫冒起來、泡泡飄進陽光；睜大眼睛（可以笑）。live prep 2026-11-10：胸口以上頭上留空；四分之三朝畫左的許硯、鏡頭偏離視線約 40°、不看鏡頭；可以笑，只寫成臉怎麼動：眼睛睜大發亮、眉毛高、嘴張大、臉頰往上，不寫笑字"),
    # live prep 2026-11-10: 精明, not a smile: from behind her right shoulder, her face out of the shot, nospeak; the
    # soap one phrase; the abacus plain.
    dict(loc="sun_c", cam="Medium shot from behind her right shoulder, locked", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="sun",
         comp=f"medium shot from behind Tang Xiaotang's right shoulder: her back, her right shoulder and the back of her head with its two looped buns and pink ribbons fill the left foreground, the whole of both buns inside the frame, her face turned away from the camera the whole shot, {TANG}, {ABACUS} under her left arm; before her on the long wooden board the white bars of soap lying in rows, each one {SOAP}; beyond the board the persimmon tree of the same sunny yard",
         lines=[("tangxiaotang", "又白又香。一塊賣三錢，縣城的太太會搶著要。", "精明")],
         motion=f"her right hand lifts one bar up to her face, the back of her head to the camera, and her left fingertips flick three abacus beads under her arm; {NOSMILE}",
         zh="近景、慢推（下巴以上，臉填滿畫面，e905 fix3）：畫面下緣是扣到喉嚨的立領頂端，一件闔上、領下沒有開口；唐小棠右手拿一塊雪白方皂（巴掌大、一指厚）湊到鼻下聞，左手指尖撥過左腋下算盤的三顆算珠；嚴肅、精明、瞇眼打量，不笑。live prep 2026-11-10：精明不准笑，她的嘴不入鏡：改中景、固定、從她右肩後拍，畫左前景是她的背、右肩與後腦兩個髮髻，臉整鏡不朝鏡頭；她把方皂拿到臉前聞（從背後看）、左手指尖撥三顆算珠；她的台詞照錄音放（nospeak）；拿掉立領句（COLLAR、TANG_SHUT，pilot.py 會擋）與 shrewd、no smile 字樣，改 TANG 與 NOSMILE；方皂與算盤都是同一句、沒有字"),
    # live prep 2026-11-10: from behind Tang Xiaotang's RIGHT shoulder (left foreground), Xu Yan on screen right (s31,
    # s33, s35, s39 keep her left of him); his face part by part; NOSMILE.
    dict(loc="sun", cam="Over-the-shoulder medium shot, locked", chars=["xuyan", "tangxiaotang"], night="sun",
         comp=f"over-the-shoulder medium shot from behind Tang Xiaotang's right shoulder: her looped buns and pink silk ribbons in the left foreground, her face turned away from the camera, {TANG}; Xu Yan on screen right across the long board, framed from the waist up with space above his head, {XU}, {NIGHT}, {HAIR}, his face three-quarter to screen left toward her, eyes on her, never the lens; doubtful: brows knitted, eyes narrowed, lips pressed between words",
         lines=[("xuyan", "三錢？一斗米才幾十文，妳這價會不會太高？", "皺眉")],
         motion=f"Xu Yan walks over wiping his hands on the hem of his robe, stops across the board from her and frowns; Tang Xiaotang's lips stay closed; {NOSMILE}",
         zh="過肩（唐小棠肩後拍許硯）、慢推：許硯一邊用衣襬擦手一邊走過來，停步皺眉；累（script 的「手上沾著白色皂屑」不寫，只留擦手的動作）。live prep 2026-11-10：寫明從唐小棠右肩後拍，髮髻在畫左前景、臉不朝鏡頭，許硯在畫右隔著木板（她在他左邊，同 s31、s33、s35、s39）；慢推改固定、腰以上頭上留空；四分之三朝她、不看鏡頭；懷疑：眉頭皺、瞇眼、字句之間嘴抿；TANG 換定妝照句；NOSMILE"),
    # live prep 2026-11-10: 篤定, not a smile: the CG reverse close-up on her face becomes the same over-the-shoulder
    # side as s32, from behind her right shoulder, her face out of the shot, nospeak (e904 fix4 s19); NOSMILE.
    dict(loc="sun", cam="Over-the-shoulder medium shot from behind her, locked", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="sun",
         comp=f"over-the-shoulder medium shot from behind Tang Xiaotang's right shoulder, the same side as the shot before: her back, her right shoulder and the back of her head with its two looped buns and pink ribbons in the left foreground, the whole of both buns inside the frame, her face turned away from the camera the whole shot, {TANG}; Xu Yan on screen right across the long board, framed from the waist up with space above his head, {XU}, {NIGHT}, his face three-quarter to screen left toward her, never the lens; listening: brows drawn together, eyes on her, lips closed; on the board between them the white bars of soap lying in rows",
         lines=[("tangxiaotang", "便宜的東西沒人當寶。貴，她們才捨得拿出來炫耀。", "篤定")],
         motion=f"her right hand sets one more white bar in line on the board, then she lifts her head toward Xu Yan, the back of her head to the camera; his lips stay closed; {NOSMILE}",
         zh="反打（許硯右肩後拍唐小棠）、慢推（唐小棠下巴以上，立領扣到喉嚨，e905 fix3）：一開始她把一塊雪白方皂（巴掌大、一指厚）放上木板、跟一排一樣的方皂對齊，才抬眼看許硯說話；木板上只有那排方皂；平靜、篤定、眼神穩，話與話之間嘴閉著，不笑。live prep 2026-11-10：篤定不准笑，她的嘴不入鏡：不再反打拍她的臉，改成跟 s32 同一邊、從她右肩後拍（第 4 集 fix4 s19 的做法），畫左前景是她的背與後腦髮髻；許硯在畫右隔著木板聽、皺眉、嘴閉；她把方皂放回木板對齊、再抬頭朝他；她的台詞照錄音放（nospeak）；拿掉立領句與 no smile 字樣，改 TANG 與 NOSMILE"),
    # live prep 2026-11-10: 淡淡，帶刺 is a barb that grins (e904 s26, e903 s30 wry): from behind Xu Yan's right shoulder,
    # his face out of the shot, nospeak, the recording laid; Lai San turns away from the camera to the gate; the scrap sized.
    dict(loc="sun", cam="Over-the-shoulder medium shot from behind him, locked", chars=["xuyan", "laisan"], nospeak=["xuyan"], night="sun",
         comp=f"over-the-shoulder medium shot from behind Xu Yan's right shoulder: his back, his shoulder and the back of his head with its topknot in the right foreground, his face turned away from the camera the whole shot, {XU}, {SCRAP} in his right hand; Lai San on screen left facing him, three-quarter toward him, never the lens, {LAI}, his torn sleeve hanging and his head-wrap askew, just up from beside the bamboo fence, cowed: neck hunched, eyes darting, lips closed; the yard gate in the bamboo fence deep at the back left",
         lines=[("xuyan", "這塊帶回去給錢員外，叫他好好洗洗手。", "淡淡，帶刺")],
         motion=f"Xu Yan presses the scrap into Lai San's hands and pats his shoulder; Lai San hugs it, turns away and limps out through the gate at the back left, lips closed; {NOSMILE}",
         zh="雙人鏡、跟拍：許硯追上賴三，把綠葉包的碎皂（木模邊角削下來的，比整塊小一半）塞進他手裡，拍拍他的肩；賴三兩手抱著皂、縮著脖子一跛一跛溜出院門出畫。live prep 2026-11-10：「淡淡，帶刺」這種話模型會演成斜嘴笑（第 4 集 s26、第 3 集 s30），許硯的嘴不入鏡：改過肩中景、固定、從許硯右肩後拍，畫右前景是他的背與後腦髮髻；賴三在畫左朝他、四分之三、不看鏡頭，縮脖子、眼睛亂瞟、嘴閉，接過碎皂後背向鏡頭轉身、一跛一跛走出左後的院門；許硯的台詞照錄音放（nospeak）；碎皂用手量（一個掌心藏得住）；跟拍改固定（不追）；NOSMILE"),
    # live prep 2026-11-10: the one Tang Xiaotang line the script lets her say lightly keeps her face, written as face
    # movements; A-ling's and Xu Yan's faces written; the soap one phrase.
    dict(loc="sun", cam="Medium shot, slow push in", chars=["tangxiaotang", "aling", "xuyan"], night="sun",
         comp=f"medium shot, all three seen from the waist up with space above their heads: Tang Xiaotang on screen left, {TANG}, standing before one bamboo basket, her face three-quarter to screen right toward Xu Yan, the camera about 45 degrees off her eyeline, never the lens, pleased: eyes bright, brows raised a little, the corners of her mouth lifting a little; at the back right A-ling, {ALING}, with empty bamboo baskets, lips closed, the corners of her mouth level; at the right edge of the frame Xu Yan by the long board, {XU}, lips closed",
         lines=[("tangxiaotang", "一共一百五十塊，賣得完，二十兩就還得上了！", "高興")],
         motion=f"Tang Xiaotang puts the leaf-wrapped bars into the basket one by one, counting; A-ling passes over an empty basket; Xu Yan picks up one of the white bars from the board; the others' lips stay closed",
         zh="中景、慢推：唐小棠把綠葉包好的白皂一塊塊放進竹籃、邊放邊數（可以笑）；阿令從屋裡拿出空籃疊好遞過來；許硯從木板上拿起一塊白皂捏在指間。live prep 2026-11-10：本集唯一稿子允許唐小棠帶笑的一句，保留她的臉，只寫成臉怎麼動（眼睛亮、眉毛微揚、嘴角稍稍上揚），不寫笑字；四分之三朝畫右的許硯、鏡頭偏離視線約 45°、不看鏡頭；阿令嘴閉、嘴角平；許硯嘴閉；腰以上頭上留空；TANG 換定妝照句；白皂同一句。注意：本場唐小棠其他四句都用錄音，這一句的模型原聲可能跟錄音差四到七個半音（第 4 集審片），剪接時請站主聽，必要時 voice_off 改用錄音"),
    # live prep 2026-11-10: the eye extreme close-up is not shot (e904 s12/s24 and e903 s19/s25: double exposure and
    # a dissolve every time): a still from s37's first frame, pushed in on the eyes in the cut, the red panel and the
    # chime laid by the edit. The text below is s37's opening face, so a CG or a fallback take would match; the
    # live chain (chain905live.sh) leaves s36 out of the jobs.
    dict(loc="sun_c", cam="Close-up, locked", chars=["xuyan"], night="sun",
         comp=f"close-up of Xu Yan's face from his brows to his chin, the shot opens directly on his face from its very first frame, {XU}, {NIGHT}, {HAIR}, his face pale, in three-quarter profile toward screen left, his eyes on the empty air before him, never the lens; stunned: brows drawn together, eyes wide and still, lips closed; behind him only the persimmon tree of the same yard",
         lines=[("xitong", "叮。強制任務：成婚。今日午時前，婚書蓋印。", "冷，叮一聲")],
         panel=[("強制任務：成婚／今日午時前，婚書蓋印／成婚 0/3", "task")],
         motion=f"he holds still, his eyes widening a little and going still; his lips stay closed; {NOSMILE}",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：許硯眼角剛要笑，才在瞳孔裡映出一點很淡的紅色反光，那一點笑收掉、眼睛睜大定住；周圍的聲音一下變小（剪接）。live prep 2026-11-10：【靜圖，不拍】眼睛大特寫第 3、4 集每次都疊影、溶接（e903 s19、s25，e904 s12、s24），改成取 s37 第一格（許硯臉色發白的臉）放大到眉眼、做約 4 秒慢推，紅色反光與面板、「叮」都由剪接疊上；「眼角剛要笑」拿掉（靜圖動不了，也是笑字）。真人工作不送這一鏡（chain905live.sh 的 IDS 不含 s36）；文字改成 s37 開頭那張臉，CG 或退路照它"),
    # live prep 2026-11-10: a medium close-up so the raised hand is in; shock part by part; head still; NOSMILE.
    dict(loc="sun_c", cam="Medium close-up, locked", chars=["xuyan"], night="sun",
         comp=f"medium close-up of Xu Yan framed from the chest up with space above his head, {XU}, {NIGHT}, {HAIR}, his face pale, in three-quarter profile toward screen left, his eyes on the empty air before him, the camera about 45 degrees off his eyeline, never the lens; stunned: brows drawn together, eyes wide and fixed, lips closed, jaw slack; {SOAP} held between the fingers of his raised right hand at chest height; behind him only the persimmon tree of the same yard",
         lines=[("xuyan", "成婚……我只顧著熬鍋，把成親給忘了。", "心裡話，嘴閉著，發愣", "inner")],
         motion=f"the white bar slips from his fingers and drops out of the frame with a smack; his hand stays frozen in mid-air, his head still; lips closed; {NOSMILE}",
         zh="近景、慢推：許硯臉色發白，那塊白皂從他指間滑掉，「啪」地落在木板上；手停在半空；心裡話，嘴閉著。live prep 2026-11-10：改固定中近景、胸口以上頭上留空，舉著的右手在胸前、方皂同一句；四分之三朝畫左、看面前空氣、鏡頭偏離視線約 45°、不看鏡頭；發愣逐部位寫：眉頭皺、眼睛睜大定住、嘴閉、下巴鬆；頭不動；這一鏡第一格也是 s36 的靜圖；拿掉 unsmiling、改 NOSMILE"),
    # live prep 2026-11-10: bending down in a close-up took the face out of the frame (e004 s05, s19, s30): a medium shot
    # with the board in the frame, he reaches down instead of bending out; NOSMILE.
    dict(loc="sun_c", cam="Medium shot, locked", chars=["xuyan"], night="sun",
         comp=f"medium shot of Xu Yan framed from the waist up with clear space above his head, the long wooden board across the bottom of the frame with one white bar of soap lying on it, {XU}, {NIGHT}, his face pale, one bead of sweat at his temple, in three-quarter profile toward screen left, never the lens; shaken: brows drawn together, eyes fixed, lips closed in a flat line; behind him only the persimmon tree of the same yard",
         lines=[("xitong", "本系統沒忘。忘了的，是宿主。", "冷，懶，句尾往下壓")],
         motion=f"he reaches down to the board, picks up the white bar and straightens up holding it before his chest, his whole head staying in the frame; his lips stay closed; {NOSMILE}",
         zh="近景、慢推：許硯（額角一滴汗）慢慢彎腰撿起那塊白皂，直起身；嘴閉著。live prep 2026-11-10：近景裡彎腰會讓臉出畫（第 4 集 s05、s19、s30），改固定中景、腰以上頭上留空、木板在畫面下緣、皂在板上，他伸手到木板撿起、直起身拿在胸前，整顆頭一直在畫面裡；四分之三朝畫左、不看鏡頭；驚：眉頭皺、眼睛定住、嘴閉成一線；拿掉 unsmiling、改 NOSMILE"),
    # live prep 2026-11-10: 驚 and the script's bold 不笑 (both CG drafts smiled anyway): from behind her right shoulder,
    # her face out of the shot, nospeak; Xu Yan on screen right as in s37-s38; the abacus the same phrase.
    dict(loc="sun", cam="Over-the-shoulder medium shot from behind her, locked", chars=["xuyan", "tangxiaotang"], nospeak=["tangxiaotang"], night="sun",
         comp=f"over-the-shoulder medium shot from behind Tang Xiaotang's right shoulder: her back, her right shoulder and the back of her head with its two looped buns and pink ribbons in the left foreground, the whole of both buns inside the frame, her face turned away from the camera the whole shot, {TANG}, {ABACUS} under her left arm; Xu Yan on screen right at the corner of the long board, framed from the waist up with space above his head, {XU}, one white bar of soap in his hand, his face pale, three-quarter to screen left toward her, never the lens; stunned: brows drawn together, eyes wide, lips closed",
         lines=[("tangxiaotang", "今天是配婚令第三天，縣衙午時就關門了！", "驚")],
         motion=f"Tang Xiaotang grabs his sleeve and the abacus slips from under her arm onto the board, the back of her head to the camera; his lips stay closed; {NOSMILE}",
         zh="雙人鏡、跟拍（唐小棠近景下巴以上）：唐小棠看他臉色不對，伸右手一把抓住他的袖子，夾在腋下的算盤掉在木板上；眼睛瞪大，不笑。live prep 2026-11-10：稿子粗體「不笑」，她的嘴不入鏡：改過肩中景、固定、從唐小棠右肩後拍，畫左前景是她的背與後腦髮髻；許硯在畫右（同 s37、s38 朝畫左）、拿著白皂、臉色發白、眉頭皺、眼睛睜大、嘴閉；她抓他袖子、算盤從腋下滑到木板上；她的台詞照錄音放（nospeak）；拿掉立領與 unsmiling，改 TANG 與 NOSMILE；算盤同一句"),
    # live prep 2026-11-10: five named people drew someone twice (e906 s01, preflight four): three on screen, A-ling and
    # Xiaohe out of the shot; Tang Xiaotang from behind (not speaking, but she would smile); Xu Yan's determination part
    # by part, no teeth word; he says it to her, three-quarter toward her, never the lens; NOSMILE.
    dict(loc="sun", cam="Low-angle full shot, slow push in", chars=["xuyan", "tangxiaotang", "qinshuang"], night="sun",
         comp=f"low-angle full shot past a row of white bars of soap on the long board in the foreground, everyone small in the frame: Xu Yan in the middle, {XU}, {NIGHT}, his face pale; Tang Xiaotang in the right foreground beside him, seen from behind, her back and the two looped buns with pink ribbons toward the camera, her face turned away the whole shot, {TANG}, still gripping his sleeve; behind them on screen left Qin Shuang, {KNIFE}, small and soft in the background, in profile, lips closed; the low sunrise on screen left",
         lines=[("xuyan", "離午時只剩三個時辰，今天這婚，非成不可。", "咬牙，下定決心")],
         motion=f"Xu Yan looks up at the low sun on screen left and sets his jaw, then turns his face to Tang Xiaotang; Qin Shuang turns her head to him, lips closed; his jaw clenched and brows set low between words; {NOSMILE}",
         zh="低角度全景、慢推、前景木板上一排白皂：許硯抬頭看剛升起的太陽，咬牙；唐小棠還抓著他的袖子；後面秦霜、阿令、小禾一個個轉頭看他（結尾，懸念到第 6 集）。live prep 2026-11-10：一鏡五個有名字的人會多畫人（e906 s01、preflight four），只留三人：許硯、唐小棠、秦霜，阿令與小禾不入鏡（下一集 c01 接）；唐小棠在右前景、背對鏡頭抓著他的袖子（她不說話也會笑）；秦霜在左後、小、側臉、嘴閉；許硯先抬頭看左邊的日頭、咬緊下巴，再轉向唐小棠說，四分之三、不看鏡頭；咬牙寫成下巴咬緊、眉壓低，不寫露牙；NOSMILE"),
]

HEAD = [
    "- 重製版 r2：照 `docs/videos/zhong-tian-qu-qi-e005-r2/script.md`（c01–c40 對應 s01–s40；含「2026-11-06 審稿後的修改」）；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。",
    "- 內部工作編號 905（`hailuo/*-dh-e905.json`、`colab/runs/e905/`）；發布 slug `zhong-tian-qu-qi-e005-r2`。不放集數、不放片名卡；c01 直接接第 4 集 c40（黑影回頭、水桶已經傾斜）。",
    "- 狀態：許硯袖子捲到手肘（全集），第一場兩手空空（s05 拿過水桶、s12 起攪棍），s15 起眼睛發紅、眼下發青，s23 起額前散髮，s35 拿起一塊白皂、s37 掉、s38 撿起；秦霜柴刀 s01 插在腰帶右邊，s02 飛出釘柱（s03–s07 腰帶空著），s08 起插回腰帶右邊，s23–s26 肩披舊灰布外衣；賴三（`laisan`）s02–s07 右袖被釘、s08 起破口垂下，s12–s21 抱攪棍，之後靠籬笆睡到 s34；阿令沒戴鐵鐐、袖子蓋住手腕，s14 只露一隻袖子，s18–s20 細柴；唐小棠 t2，s28–s39 算盤夾在左腋下；小禾 s27 左臂抱草兔，s30 起夾在腋下。",
    "- 皮膚上不寫小東西：script 的「手上沾著灰」（c29）、「手上沾著白色皂屑」（c32 與角色表）不寫（會畫成黑點），只留捲袖與 s32 用衣襬擦手；額角一滴汗（s38）照寫。",
    "- 長鏡要買的秒數（`r2.py` 的 BUY）：script.md 長鏡清單沒有超過 6 秒的鏡（6 秒整的照 `gen-dh` 買 6 秒）；s07、s24、s32、s37 8 秒（錄好的配音加半秒 6.2、6.4、6.8、6.5 秒，超過預設 6 秒）；s29 6 秒（畫外台詞的手部特寫，`gen-dh` 會給 5 秒）。其餘照 `gen-dh` 的 6 秒；眼睛大特寫 s36 兩拍動作，`gen-dh` 給 6 秒。",
    "- 系統句：近景、中景只寫反應（s17 script 的「眼裡映一點淡藍光」不寫；s22、s26、s38 只寫動作）；眼睛大特寫 s36 在真人版改成靜圖（見下一條），紅色反光由剪接疊上。",
    "- 真人版前置（live prep 2026-11-10，照第 4 集真人版四輪重拍、route-a.md 2026-11-09/10、e904-live 兩次成片審查、e004-r2 與 e003-r2 的 live 修正）：每張露臉的臉都逐部位寫（眉、眼、嘴角、下巴、呼吸），不寫任何笑字（sweet、shrewd、offhand、teasing、wry、eager、grin、softly 都不用），不准笑的鏡一律 NOSMILE（s04 賴三陪笑、s27／s30 小禾、s35 唐小棠只寫成臉怎麼動）；不動的反應鏡不低頭、不吞嚥（s26 拿掉點頭）；唐小棠稿子不准笑的四句（s28、s31、s33、s39）一律從她背後或右肩後拍、嘴不入鏡、`nospeak`、用錄音，只有 s35 露臉；許硯 s34「淡淡，帶刺」同樣從他右肩後拍、`nospeak`；說話的人側臉或四分之三朝聽的人、鏡頭偏離視線 40–70°、不看鏡頭、固定、頭上留空；軸線：第一、二場賴三與棚柱在左、鍋在中、屋門與許硯在右，s09／s10、s19／s20 寫明從誰的哪一邊肩後拍（原本 s09／s10 越軸，已改）；第三場唐小棠在許硯左邊；有宋式交領的鏡不准用鏡像修軸線；s36 眼睛大特寫不拍，取 s37 第一格做靜圖，真人工作不送；s40 只留三個有名字的人（阿令、小禾不入鏡）；道具照數寫、用身體量、同一句、沒有字；夜景天空與門內都是暗的，要藏的臉火在另一側；鏡尾回頭只轉到側臉、背向鏡頭與光。工作：`colab/runs/e905-live/spec.json`（種子 9051101、9051102，有許硯的鏡加袍子兩肩完整的替換），39 鏡 78 支。",
]
FOOT = [
    "- 場景參考：全集都在院子 `set-xujia-yuan-t1`。第一、二場在院子東側灶棚（兩根棚柱在左、土灶與大鍋在中間、屋門在右，照第 4 集最後幾鏡的寫法，提示詞寫 dirt yard 對到院子的場景圖）：灶火橘光由下往上、冷月光從右上 → 後半夜月亮偏西 → 天快亮冷藍晨光從左後方；第三場柿子樹下的長木板，日出暖光從左邊低低照進來。近景背景都寫「同一個灶棚／院子」。",
    "- 灶棚夜景版不用補：script 清單 2 寫「灶棚若場景圖裡沒有，開拍前補一張」；第 4 集已經用同一張院子場景圖加文字拍過灶棚，照用。",
    "- 唐小棠一律用 `tangxiaotang-portrait-t2`（gen-dh 的 PORTRAIT 對照）；真人版（live prep 2026-11-10）構圖一律寫 TANG（定妝照的交領短襦闔上、百褶裙繫蝴蝶結），不寫立領、「一件闔上」或「下巴以上」（pilot.py 會擋，也會被換成 high-waisted；CG 時期的 TANG_SHUT、COLLAR、TANG_CALC 已拿掉）。",
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
