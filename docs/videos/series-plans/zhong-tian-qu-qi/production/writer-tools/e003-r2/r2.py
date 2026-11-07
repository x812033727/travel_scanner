"""Episode 3 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e003-r2/script.md
(c01-c40 = s01-s40), including its section 「2026-11-06 審稿後的修改」, which overrides the tables (c22 gains Xu Yan's
inner line and becomes a long shot; c15 draws the fan from the belt; the per-shot state lines).

Same rules as e001-r2 and e002-r2: one visible action per shot written as a path, over-the-shoulder and reverse shots
for dialogue, whole sentences, one line per spoken line, default face serious (smiles only where the script allows: c11
a forced smile, c26 a deliberate smile, c30 a wry smile). State: Xu Yan dry with his sleeves rolled to the elbows and
the rolled red paper in the left of his belt all episode, red ink on his right thumb
c14-c16 (wiped clean from c17), the clay oil lamp in his left hand c31-c34 (on the stove from c34); Qin Shuang's old
chopping knife in the gate frame c01-c16 (her belt empty in c02, c03, c16), pulled out and back in the right of her
belt in c16, a bundle of firewood on her right shoulder in c29; A-ling without shackles, her sleeves over the red marks,
the bucket c26-c30, one short knife and a whetstone c31-c40; Tang Xiaotang always t2 (high collar, closed garment); the
new 字據 never readable (blank sheet, out of focus, blank corner, folded); the grey-clad servants and the villagers have
no picture and are never shown by the face. Opens on the next instant after e002 c40: the knife thunks into the gate frame.
"""
EP = 903  # internal working number; the published slug is zhong-tian-qu-qi-e003-r2
SLUG = "zhong-tian-qu-qi-e003-r2"
EP_TITLE = "要拿新娘抵債？窮秀才一條律擋回去，字據改成三天還錢（重製版 r2）"
OUTLINE_SECONDS = 187  # script.md 2026-11-06: 74 + 68 + 45 s, 40 shots
TARGET_MINUTES = [3, 4]
TITLE = "要拿新娘抵債？窮秀才一條律擋回去，字據改成三天還錢｜種田娶妻打天下 第3集（重製版）"
DESCRIPTION = "秦霜的柴刀釘進門框，家丁鬆開唐小棠。錢員外惱羞成怒，要把三個新娘都寫進字據抵債，許硯按住白紙，搬出大衡律配婚篇：官府配的人，私自押走就是搶官府的人。錢員外不敢押人，改逼許硯限期還錢，字據寫成「三日後日落前還清二十兩，否則收房收地」，許硯按了手印。傍晚，唐小棠替他發愁，系統發下新手禮包：肥皂配方一份，材料工具自備；好感度隨即開啟。許硯急著討好，對阿令說「有我在，誰都帶不走妳」，被系統判成空話，阿令好感 -5。夜裡許硯在灶房遇到磨刀的阿令，認了白天說的是空話，阿令問他：錢員外要的是人，為何不押我們？《種田娶妻打天下》第 3 集（重製版）。"
THUMB = ("搶官府的人", "s09")
CHARACTERS = ["xuyan", "qinshuang", "aling", "tangxiaotang", "xiaohe", "qianyuanwai", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: a tense cue of low drums and erhu in the yard in the late afternoon, opening on one heavy hit as the knife thunks into the gate frame and dropping low while the moneylender reads out the note; a light playful comedy of woodblock, pipa and dizi in the yard at dusk, dropping out to a single cold electronic blip on each system line and one sharp electric hit on the deduction; a slow quiet night suspense cue of low cello and soft guqin in the firelit kitchen, ending on one low note; ancient Chinese rural drama, no vocals"

# Scene headers of script.md: the Xu yard (set-xujia-yuan-t1) late afternoon then dusk, the Xu kitchen
# (set-xujia-zao-t1) at night. gen-dh maps "dirt yard"/"yard gate" to the yard picture and "kitchen" to the kitchen one.
# Axis in the yard: the house door at the back left, the gate on screen right, the well at the back right, the table in
# the middle. In the kitchen: the door on screen left, the stove on screen right with its fire mouth facing left.
LOC = {
    "yard_late": "In the dirt yard of the Xu farmhouse in the late afternoon on a clear autumn day, the sun low in the west, an autumn tree, a bamboo fence, a woodpile on screen left, the house door at the back left, a wooden table in the middle, the yard gate in the fence on screen right, a stone well at the back right, low golden sunlight slanting in from the gate on screen right casting long shadows",
    "yard_dusk": "In the dirt yard of the Xu farmhouse at dusk on a clear autumn day, the sun about to set, an autumn tree, a bamboo fence, the house eaves on screen left with strips of dried vegetables hanging under them, a wooden table in the middle, the yard gate in the fence on screen right, a stone well at the back right, dark orange sunset light slanting in from screen right casting very long shadows",
    "kitchen": "Inside the small earthen kitchen of the Xu farmhouse at night, packed earth walls and floor, the plank door on screen left with faint cold moonlight beyond it, a clay stove on screen right with its fire mouth facing left and a fire burning in it, firewood stacked against the wall, lit only by the warm orange glow of the stove fire and a small clay oil lamp",
    # 2026-11-07 review retakes (fix3): close-ups keep the set to one line; the kitchen shots name the one lamp by LAMP.
    "yard_late_m": "In the dirt yard of the Xu farmhouse in the late afternoon, a bamboo fence, the house door at the back left, the wooden table in the middle, the yard gate on screen right, low golden sunlight from the gate on screen right casting long shadows",
    "yard_late_cu": "In the dirt yard of the Xu farmhouse in the late afternoon, low golden sunlight from screen right",
    "yard_dusk_cu": "In the dirt yard of the Xu farmhouse at dusk, dark orange sunset light from screen right",
    "yard_well_cu": "In the dirt yard of the Xu farmhouse at dusk, beside the stone well by the bamboo fence, dim dark orange sunset light from screen right",
    "kitchen_m": "Inside the small earthen kitchen of the Xu farmhouse at night, packed earth walls and floor, the plank door on screen left with faint cold moonlight beyond it, a clay stove on screen right with its fire mouth facing left and the fire burning inside that fire mouth, firewood stacked against the wall, lit only by the warm orange glow of the stove fire",
    "kitchen_door": "Inside the small earthen kitchen of the Xu farmhouse at night, seen from its open doorway, a clay stove on screen right with its fire mouth facing left and the fire burning inside it, lit only by the warm orange glow of the stove fire",
    "kitchen_cu": "In the small earthen kitchen of the Xu farmhouse at night, lit only by the warm orange glow of the stove fire",
}
LIGHT = {
    "yard_late": "the low late-afternoon sunlight from the right stays unchanged",
    "yard_dusk": "the dark orange sunset light from the right stays unchanged",
    "kitchen": "the warm orange firelight stays unchanged",
    "kitchen_fire": "the warm orange firelight stays steady apart from that one flare",
}

# Repeated wording (each prop is one object; the descriptions say "one" where it first appears).
TANG = "her peach-pink brocade ruqun one closed garment from the high stand-up collar to the waist"
SERV = "grey coarse cotton cross-collared short jackets, cloth head-wraps and cloth shoes, both hands empty"
VILL = "villagers in Song-dynasty cross-collared coarse cotton jackets and cloth head-wraps"
XU1 = "his blue-grey scholar's robe dry now, his sleeves rolled up to the elbows, a little sweat on his brow"
# The one rolled red paper: always this phrase, never a flat sheet in his hand (2026-11-07 review).
BELT = "the rolled red paper, rolled tight into a short plain blank tube, tucked into the left side of his belt"
ALING = "no shackles, her sleeves pulled down over her wrists"
# A-ling's one short knife, the same phrase in every shot it is in (s31-s33, s35, s37, s39; e004 too).
KNIFE = "one short single-edged knife with a dull iron-grey blade about one and a half palms long and a plain wooden handle"
# Xu Yan's one lamp (s31, s33, s34, s36): an open clay bowl, never a glass lantern.
LAMP = "one small open clay bowl oil lamp the size of a palm, a single wick burning in its shallow bowl of oil"
# Qin Shuang's old chopping knife (s01, s16).
CHOP = "one old chopping knife with a foot-long dark iron blade and a black-cloth-wrapped wooden handle"
# The grey-clad servants have no picture: only backs, shoulders down or hands (2026-11-07 review).
SERV1 = "a grey coarse cotton cross-collared short jacket, a cloth head-wrap and cloth shoes"

SHOTS = [
    # ---- scene 1: the 字據, late afternoon (e002's same instant), low sun from the gate on the right. Axis: the Xu side
    # (Xu Yan, Tang Xiaotang, Qin Shuang) on screen left; Qian Yuanwai and the four servants on screen right by the gate.
    dict(chapter="字據", loc="yard_late_cu", cam="Insert close-up, locked", chars=["tangxiaotang"], night="yard_late", act=3,
         comp=f"insert close-up of the upright wooden post of the yard gate, the shot opens directly on the gate post from its very first frame with {CHOP} already stuck deep in the post, its blade quivering, its handle sticking out toward screen left; one inch below the blade one grey-clad servant's right hand in a grey coarse cotton cross-collared cuff grips Tang Xiaotang's left forearm in its peach-pink brocade sleeve; that one hand holds only the sleeve, and no hand touches the knife; only that one hand, her forearm, the post and the knife are in the frame, all faces out of the frame, her ruqun one closed garment from the high collar to the waist; behind them only the bamboo fence of the same yard",
         lines=[],
         motion="the knife stuck in the gate post quivers hard, its handle shaking toward screen left; the servant's fingers on the peach-pink sleeve freeze stiff and stay there; the knife stays in the post the whole shot and no hand reaches for it",
         zh="門框特寫、固定（第一格就是院門門柱，柴刀已釘在上面、刀身在顫、刀柄朝左；音效「篤」接第 2 集 c40）：一隻家丁的手（灰短褐袖口）抓著唐小棠的左前臂（桃粉織錦袖子），刀刃離手指一寸；家丁的手指一僵；沒有手碰刀（2026-11-07 審片：原片段有手握著刀）"),
    dict(loc="yard_late_m", cam="Medium shot, tracking", chars=["qinshuang", "tangxiaotang"], night="yard_late",
         comp=f"medium shot, Qin Shuang striding in from the bamboo fence on screen left, a cold hard stare, her mouth a flat line, the right side of her wide leather belt empty, her old chopping knife stuck in the wooden gate post on screen right with its handle toward screen left; at the right edge one grey-clad servant seen only from behind, his back, shoulders and the back of his head-wrap toward the camera, in {SERV1}, his face turned away the whole shot, his right hand still gripping the left forearm of Tang Xiaotang, {TANG}",
         lines=[("qinshuang", "放手。這一刀是故意偏的，下一刀不會。", "冷，不大聲")],
         motion="Qin Shuang strides from the fence to one step behind the servant and rests her right hand on the knife handle in the gate frame without pulling it out; the others' lips stay closed",
         zh="中景、跟拍（由左往右）：秦霜（腰帶空著）從籬笆邊大步走到家丁背後一步，右手搭上門框上的刀柄不拔；右邊緣家丁背影還抓著唐小棠（t2）的左前臂；冷、不笑"),
    dict(loc="yard_late_m", cam="Over-the-shoulder medium shot, slow push in", chars=["qinshuang", "tangxiaotang", "xiaohe"], night="yard_late", act=4,
         comp=f"over-the-shoulder shot from behind Qin Shuang: her right shoulder and high ponytail fill the left foreground, her belt empty; that shoulder is Qin Shuang, who appears nowhere else in the frame; on screen right one grey-clad servant seen only from the shoulders down, his head above the top of the frame, his right hand on the left forearm of Tang Xiaotang, {TANG}, glaring, brows drawn together, lips pressed tight, not smiling the whole shot; at the left, a few steps from the house door at the back left, little Xiaohe in her patched lilac jacket, hugging her small woven straw rabbit to her chest",
         lines=[],
         motion="the servant lets go and steps back one step; Tang Xiaotang shakes her sleeve free, rubs her left forearm, glares at him and backs off past the left edge to stand behind Xu Yan off screen left; little Xiaohe runs back into the house door at the back left, hugging her rabbit; all lips stay closed",
         zh="過肩（秦霜肩後拍家丁與唐小棠）、慢推：家丁（只露肩膀以下）鬆手退一步；唐小棠（t2）甩開袖子退到許硯身後，揉左前臂瞪家丁；小禾從許硯身後跑回左後屋門口；秦霜腰帶空著"),
    dict(loc="yard_late", cam="Low-angle close-up, slow push in", chars=["qianyuanwai"], night="yard_late",
         comp="low-angle close-up of Qian Yuanwai in his dark gold silk robe with roundel patterns, gritting his teeth in a cold sneer, one plain bamboo-ribbed folding fan with a blank face and no writing, closed, in his right hand, three gold rings on his right hand; behind him only the yard gate and the autumn tree of the same yard",
         lines=[("qianyuanwai", "好個潑辣貨。來人，拿紙筆，三個都寫進字據！", "冷笑")],
         motion="he jabs the closed fan at Qin Shuang off screen left, then sweeps it toward the wooden table in the middle of the yard",
         zh="低角度近景、慢推：錢員外（深金色團花錦袍、三枚金戒指）咬牙冷笑，用合起的素面摺扇朝秦霜一點，再往院子中間的木桌一揮"),
    dict(loc="yard_late", cam="Insert close-up, slow push in", chars=[], night="yard_late", act=3,
         comp="insert close-up of the wooden table top, the shot opens directly on the table top from its very first frame: one sheet of plain pale yellow paper, completely blank, one ink brush and one small inkstone; the two hands of one grey-clad servant in grey coarse cotton cross-collared sleeves reaching in; only the hands and sleeves are in the frame, his face out of the frame; behind them only the out-of-focus dirt ground of the same yard",
         lines=[],
         motion="the hands smooth the blank sheet flat on the table, then pick up the brush and dip it in the inkstone",
         zh="手部特寫、慢推（第一格就是木桌桌面）：家丁的雙手（灰短褐袖口）把空白的淡黃紙在桌上攤平，拿起毛筆在硯台裡蘸墨"),
    dict(loc="yard_late", cam="Medium shot to medium close-up, slow push in", chars=["xuyan", "qianyuanwai"], night="yard_late",
         comp=f"medium shot, closing in to a medium close-up by the end, Xu Yan in {XU1}, {BELT}, beside the wooden table with one blank sheet of pale yellow paper on it; Qian Yuanwai at the right edge of the frame",
         lines=[("xuyan", "慢著。這張字據，錢員外最好別寫。", "聲音一沉")],
         motion="Xu Yan strides in from screen left to the table, slaps his right hand flat on the blank sheet and looks up at Qian on screen right; Qian's lips stay closed",
         zh="中景、慢推（中景推到中近景）：許硯（書生袍已乾、袖子捲到手肘、手背沾木屑）從左大步走到桌邊，右手啪地按住空白的紙，抬頭看錢員外"),
    dict(loc="yard_late", cam="Over-the-shoulder medium shot, slow push in", chars=["qianyuanwai", "xuyan"], night="yard_late",
         comp="over-the-shoulder shot from behind Xu Yan's shoulder and his rolled-up sleeve in the left foreground, Qian Yuanwai facing the camera on screen right across the wooden table, the closed blank folding fan in his right hand",
         lines=[("qianyuanwai", "怎麼？欠債還錢天經地義，你還想賴帳不成？", "逼問")],
         motion="Qian smacks the fan down on the table, leans forward and pushes his face close to Xu Yan's",
         zh="過肩（許硯肩後拍錢員外）、慢推：錢員外把扇子往桌上一拍，身子往前傾，臉湊近許硯"),
    dict(loc="yard_late_cu", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="yard_late",
         comp=f"medium close-up, closing in to a close-up by the end, of Xu Yan standing at the wooden table, his sleeves rolled up to the elbows, a little sweat on his brow, {BELT}, a calm level look, his mouth set firm, his eyes on Qian Yuanwai off screen right; his right hand rests flat on one blank sheet of pale yellow paper on the table at the bottom edge of the frame, his left hand empty; behind him only the bamboo fence and the autumn tree of the same yard",
         lines=[("xuyan", "不賴帳。大衡律配婚篇，她們三個的名字記在縣衙名冊上。", "慢條斯理")],
         motion="he straightens up, his right hand staying flat on the blank pale yellow sheet, lifts his eyes and points his empty left hand out past the gate toward the county town",
         zh="近景反打、慢推（中近景推到近景）：許硯直起身，手還按著紙，抬眼直視錢員外，另一手指向院門外縣城；穩、不笑"),
    dict(loc="yard_late", cam="Medium shot, tracking", chars=["xuyan", "qianyuanwai"], night="yard_late",
         comp=f"medium shot, Xu Yan on screen left, his sleeves rolled up to the elbows, a little sweat on his brow, {BELT}, and Qian Yuanwai on screen right, only these two men inside the yard; in the background outside the bamboo fence, on its far side, about five {VILL}, seen only from the chest up over the top of the fence, the fence between them and the yard",
         lines=[("xuyan", "官府配的人，你私自押走，就是搶官府的人。", "一字一句")],
         motion="Xu Yan rounds the corner of the table and takes one step toward Qian, staying on his left; Qian leans back a little and his lips stay closed",
         zh="中景、跟拍（跟著許硯往右）：許硯繞過桌角朝錢員外走近一步（仍在他左邊），錢員外往後仰一下；背景籬笆外村民"),
    dict(loc="yard_late_m", cam="Two-shot, slow push in", chars=["qianyuanwai", "tangxiaotang"], night="yard_late", act=3,
         comp=f"two-shot, Qian Yuanwai in the foreground on screen right, the closed fan stopped in midair in his right hand, and at the back left Tang Xiaotang, {TANG}, a shrewd level look with her lips pressed together, not smiling the whole shot, the small gold abacus with wooden beads on her left palm, only these two inside the yard; outside the bamboo fence, on its far side, about five {VILL}, seen only from the chest up over the top of the fence, whispering together",
         lines=[],
         motion="Tang Xiaotang flicks one abacus bead and nods at Qian; Qian glances at the villagers watching over the fence and swallows hard; all lips stay closed",
         zh="雙人鏡、慢推：前景錢員外扇子停在半空；後左唐小棠（t2）撥一下金算盤、朝他點頭；錢員外瞄一眼籬笆外交頭接耳的村民，喉結動一下"),
    dict(loc="yard_late", cam="Close-up, slow push in", chars=["qianyuanwai"], night="yard_late",
         comp="close-up of Qian Yuanwai squeezing out a stiff forced smile, the closed blank folding fan in his right hand; behind him only the yard gate of the same yard",
         lines=[("qianyuanwai", "行，人我不押。那你拿什麼還？房子、地，還有你？", "咬牙")],
         motion="he tucks the closed fan into his belt, forces a smile and jabs one finger at Xu Yan off screen left",
         zh="近景、慢推：錢員外把扇子收起插進腰帶，硬擠出一個笑（可以假笑），手指往許硯一點"),
    dict(loc="yard_late", cam="Reverse close-up, slow push in", chars=["xuyan"], night="yard_late",
         comp="reverse close-up of Xu Yan, his sleeves rolled up to the elbows, a little sweat on his brow, steady and unsmiling, his eyes on Qian Yuanwai off screen right; behind him only the bamboo fence of the same yard",
         lines=[("xuyan", "房子和地你先別急。給我三天，二十兩一文不少。", "穩")],
         motion="he lifts his hand off the blank sheet below the frame and holds up three fingers",
         zh="反打近景、慢推：許硯把按著紙的手收回來，伸出三根手指；穩"),
    dict(loc="yard_late", cam="Medium shot, slow push in", chars=["qianyuanwai", "xuyan"], night="yard_late",
         comp="medium shot past one corner of the wooden table in the foreground, Qian Yuanwai standing behind the table with one ink brush in his right hand, the pale yellow sheet lying flat on the table soft and out of focus, nothing on it readable from the camera's side; Xu Yan with his sleeves rolled up at the left edge of the frame",
         lines=[("qianyuanwai", "三日後日落前還清二十兩，否則收房收地。", "念")],
         motion="Qian bends over the sheet and writes with the brush as he reads aloud, then lays the brush on the inkstone; Xu Yan's lips stay closed",
         zh="中景、慢推、前景木桌一角：錢員外抓起毛筆彎腰寫，邊寫邊念，寫完把筆擱在硯台上；紙面虛焦、看不到字；許硯在左邊緣"),
    dict(loc="yard_late", cam="Insert close-up, slow push in", chars=["xuyan"], night="yard_late", act=3,
         comp="insert close-up of one bottom corner of the pale yellow sheet on the wooden table, the shot opens directly on the blank paper corner and one small box of red ink paste from its very first frame: only the plain blank corner, the written part outside the frame, and Xu Yan's right hand in his rolled-up blue-grey cuff; only the hand and the paper corner are in the frame, his face out of the frame; behind them only the out-of-focus dirt ground of the same yard",
         lines=[],
         motion="his thumb presses into the red ink paste, then presses down hard on the blank corner, leaving one red thumbprint, and lifts away",
         zh="手部特寫、慢推（第一格就是紙角與紅印泥）：只拍空白紙角（寫字的部分在畫面外）；許硯的拇指按進紅印泥，再重重按在紙角留下紅指印，拇指抬起"),
    dict(loc="yard_late", cam="Medium shot, tracking", chars=["qianyuanwai"], night="yard_late",
         comp=f"medium shot, Qian Yuanwai standing by the wooden table holding the written sheet in both hands with its plain blank back toward the camera, the closed blank folding fan tucked into the front of his belt; behind him at the right edge the grey-clad servants seen only from the shoulders down, their heads above the top of the frame, in {SERV}",
         lines=[("qianyuanwai", "許秀才，三日後太陽一落，我帶人來收房。", "拖長音")],
         motion="Qian folds the sheet twice into his left sleeve, walks toward the gate on screen right, looks back, and only then pulls the fan from his belt with his right hand and points it at Xu Yan off screen left",
         zh="中景、跟拍（跟著錢員外往右）：錢員外把字據對摺兩次收進左袖，轉身往院門走，到門口回頭，右手從腰帶抽出摺扇往許硯一指；家丁只露肩膀以下"),
    dict(loc="yard_late_m", cam="Full shot, slow push in", chars=["qinshuang", "xuyan", "qianyuanwai"], night="yard_late",
         comp=f"full shot past the wooden gate post on screen right in the foreground, {CHOP} still stuck in the post with its handle toward screen left; Qian Yuanwai and the grey-clad servants in {SERV}, all seen only from behind, walking out through the gate; on screen left Qin Shuang, the right side of her wide leather belt empty, a cold hard look, and Xu Yan, his sleeves rolled up, {BELT}, his right thumb stained red with ink paste",
         lines=[("qinshuang", "手印按了，三天後拿不出二十兩，這房子就沒了。", "冷")],
         motion="Qian and the servants walk out of the gate and the frame; only then Qin Shuang pulls the knife from the post with her right hand, blade down, slides it into the right of her belt and looks back at Xu Yan, her mouth barely moving; his lips stay closed",
         zh="全景、慢推、前景門框上的柴刀：錢員外與家丁（背影）走出院門離開畫面；秦霜走過來右手拔下柴刀（刃朝下）插回腰帶右邊，回頭看許硯（右手拇指沾紅印泥）；冷（結尾）"),
    # ---- scene 2: the novice pack, the same yard at dusk (dark orange light from the right). Axis: Xu Yan sits at the left of
    # the table facing right, Tang Xiaotang across on the right; c26 he walks to the well at the back right, left of A-ling.
    dict(chapter="新手禮包", loc="yard_dusk", cam="Full shot, slow push in", chars=["tangxiaotang", "xuyan"], night="yard_dusk",
         comp=f"full shot past strips of dried vegetables hanging under the eaves in the foreground, Tang Xiaotang on screen right, {TANG}, the small gold abacus hanging at her waist, worried: her brows knitted upward and her lips pressed tight, not smiling the whole shot, and Xu Yan on screen left, his sleeves rolled up to the elbows, {BELT}, both hands empty, his thumbs clean",
         lines=[("tangxiaotang", "三天賺二十兩？你家米缸都快見底了。", "倒抽一口氣")],
         motion="Tang Xiaotang walks to the table, unhooks the abacus from her waist, sets it down and sits; Xu Yan sits down across from her, his lips closed",
         zh="全景、慢推、前景屋簷下的菜乾：唐小棠（t2）走到木桌邊，把金算盤從腰間解下放在桌上，坐下；許硯（拇指印泥已擦乾淨）跟著坐到對面；發愁、不笑"),
    dict(loc="yard_dusk", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="yard_dusk",
         comp=f"over-the-shoulder shot from behind Tang Xiaotang's shoulder and her looped bun with its pink ribbon in the right foreground, her ruqun one closed garment from the high collar to the waist, and Xu Yan facing the camera on screen left across the wooden table, his sleeves rolled up to the elbows, {BELT}, putting on a brave face: a strained forced look, his jaw tight and his brows drawn together",
         lines=[("xuyan", "所以要找一門三天就能賺到二十兩的買賣。", "硬撐")],
         motion="Xu Yan leans forward on both hands on the tabletop and taps one finger on the table",
         zh="過肩（唐小棠肩後拍許硯）、慢推：許硯雙手撐著桌面往前坐，手指在桌上點一下；硬撐、不笑"),
    dict(loc="yard_dusk", cam="Extreme close-up, slow push in", chars=["xuyan"], night="yard_dusk",
         comp="extreme close-up of Xu Yan's eyes, the shot opens directly on his eyes from its very first frame, a faint pale blue light reflected in his pupils; nothing else in the frame",
         lines=[("xitong", "叮。新手禮包發放：肥皂配方一份。", "冷淡，叮一聲")],
         panel=[("新手禮包：肥皂配方", "panel")],
         motion="his eyes light up, his pupils tighten and he blinks once; his lips stay closed",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：瞳孔映淡藍光（不畫面板），眼睛一亮、瞳孔一縮、眨一下"),
    dict(loc="yard_dusk_cu", cam="Close-up, slow push in", chars=["xuyan"], night="yard_dusk",
         comp="close-up of Xu Yan sitting at the wooden table, his sleeves rolled up to the elbows, his face warm in the dark orange dusk light from screen right with only a faint pale reflection on it, his eyes fixed on the open air before his face, expectant, his brows raised; the bare wooden tabletop below the frame; behind him only the eaves and the dried vegetables of the same yard in the dark orange dusk",
         lines=[("xitong", "材料自備，工具自備。", "冷淡")],
         panel=[("材料自備・工具自備", "panel")],
         motion="he sits up straight and waits a moment, then reaches his right hand forward into the empty air before his face, closes it on nothing, looks at his empty hand and frowns; his lips stay closed",
         zh="近景、慢推：許硯往前坐直，臉被淡藍光照亮，等一下，伸手在空氣裡摸一下，什麼都沒有，皺眉"),
    dict(loc="yard_dusk_cu", cam="Close-up to big close-up, slow push in", chars=["xuyan"], night="yard_dusk",
         comp="close-up, closing in to a big close-up by the end, of Xu Yan sitting at the wooden table, his sleeves rolled up to the elbows, a pained grimace, one corner of his mouth pulled down and twitching, his lips closed; behind him only the eaves of the same yard in the dark orange dusk",
         lines=[("xuyan", "送個方子就叫禮包，連一塊豬油都不給？", "心裡話，嘴閉著", "inner"),
                ("xitong", "嫌少可以退。退了就什麼都沒有。", "冷")],
         motion="the corner of his mouth twitches down in a pained grimace, he taps two fingers twice on the table, then rolls his eyes up and leans back; his lips stay closed the whole shot",
         zh="近景、慢推（近景推到大近景，長鏡買 8 秒）：許硯嘴角抽一下（不笑），手指在桌上敲兩下，翻白眼往後一靠；心裡話，嘴閉著；系統冷冷回一句"),
    dict(loc="yard_dusk", cam="Two-shot, slow push in", chars=["xuyan", "tangxiaotang"], night="yard_dusk",
         comp=f"two-shot across the wooden table, the same sides as before: Xu Yan sitting on screen left facing right, his sleeves rolled up to the elbows, still looking put out, his jaw tight, and Tang Xiaotang sitting on screen right facing left, framed from the chin up, her high stand-up collar closed at her throat, {TANG}, puzzled: her brows drawn into a frown and her head tilted, not smiling the whole shot; behind them only the eaves and the dried vegetables of the same yard",
         lines=[("xuyan", "不退。有方子，總比什麼都沒有強。", "心裡話，嘴閉著", "inner"),
                ("tangxiaotang", "你發什麼呆？眼睛直直盯著空氣看。", "狐疑")],
         motion="first Xu Yan stares at the empty air, clenches his jaw and nods once; only then Tang Xiaotang waves her right hand before his eyes, frowns and tilts her head, and he blinks and looks at her, his lips closed",
         zh="雙人鏡、慢推（唐小棠下巴以上，2026-11-06 長鏡買 8 秒）：先是許硯盯著空氣咬牙、輕輕點頭（心裡話，嘴閉著）；接著唐小棠伸手在他眼前晃、歪頭看他，許硯眨眼回神"),
    dict(loc="yard_dusk_cu", cam="Reverse close-up, slow push in", chars=["xuyan"], night="yard_dusk",
         comp="reverse close-up of Xu Yan alone, sitting at the left side of the wooden table and facing screen right, his sleeves rolled up to the elbows, earnest: his brows lifted and his eyes bright, his mouth set firm, his eyes on her across the table off screen right; he is the only person in the frame, and the right side of the frame holds only the soft out-of-focus eaves in the dark orange dusk; behind him only the eaves of the same yard",
         lines=[("xuyan", "我在想一個買賣。我會做比皂角好洗十倍的肥皂。", "認真")],
         motion="he turns his head to her and with both hands shapes one small square block in the air above the table",
         zh="近景反打、慢推：許硯回過神轉頭看她，兩手在桌上比出一塊方方的東西；認真"),
    dict(loc="yard_dusk", cam="Insert close-up, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="yard_dusk",
         comp="insert close-up of Tang Xiaotang's hand and the small gold abacus on the wooden table, the shot opens directly on the abacus from its very first frame: the palm-sized abacus with its gold frame and wooden beads lying on the table, her right forefinger on the beads, the cuff of her peach-pink brocade sleeve; only the hand, sleeve and abacus are in the frame, her face out of the frame above, her ruqun one closed garment from the high collar to the waist; behind it only the out-of-focus tabletop of the same yard",
         lines=[("tangxiaotang", "真比皂角好十倍，那就不愁沒有人買。", "畫外，精明")],
         motion="her right forefinger flicks one bead up and back down, then presses one bead and holds it; no mouth is in the frame",
         zh="算盤特寫、慢推（第一格就是算盤）：唐小棠右手食指把算盤珠撥上去又撥下來，最後按住一顆；只拍手，沒有嘴"),
    dict(loc="yard_dusk", cam="Extreme close-up, slow push in", chars=["xuyan"], night="yard_dusk",
         comp="extreme close-up of Xu Yan's eyes, the shot opens directly on his eyes from its very first frame, a faint pale blue light reflected in his pupils; nothing else in the frame",
         lines=[("xitong", "好感度，開啟。", "冷淡，叮一聲")],
         panel=[("好感度：開啟", "panel")],
         motion="his eyes light up, then flick toward the back right, toward the well; his lips stay closed",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：瞳孔映淡藍光，眼睛一亮，眼珠往右後（井邊）一轉"),
    dict(loc="yard_dusk", cam="Medium shot, tracking", chars=["xuyan", "aling"], night="yard_dusk",
         comp=f"medium shot, Xu Yan on screen left, his sleeves rolled up to the elbows, {BELT}, wearing a deliberate tender smile, and at the back right A-ling standing by the stone well in her plain grey-white cotton dress, {ALING}, one wooden bucket full of water in her right hand",
         lines=[("xuyan", "阿令，妳別怕。有我在，誰都帶不走妳。", "自以為深情")],
         motion="Xu Yan gets up, straightens his collar, walks to the well and reaches for the bucket in A-ling's hand; she does not move, her lips closed",
         zh="中景、跟拍（跟著許硯往右後的井邊）：許硯站起來整整衣襟，走到井邊伸手要接阿令（沒戴鐵鐐、袖子蓋住手腕）手上的水桶；阿令沒動；許硯笑得刻意（可以）"),
    dict(loc="yard_well_cu", cam="Close-up, slow push in", chars=["aling"], night="yard_dusk",
         comp=f"close-up of A-ling standing by the stone well in her plain grey-white cotton dress with her wooden hairpin, {ALING}, a cold steady stare, her mouth closed, one wooden bucket full of water hanging from her right hand at her side; at the left edge of the frame a man's reaching hand in a rolled-up blue-grey sleeve, a hand's width short of the bucket handle; behind her only the stone well and the bamboo fence in the dim orange dusk light of the same yard",
         lines=[("xitong", "這叫空話，宿主。扣分。阿令好感 -5。", "冷")],
         panel=[("阿令 好感 -5 → -5", "panel")],
         motion="A-ling pulls the bucket aside to her right with her right hand; the reaching hand closes on empty air and never touches the bucket or her; she gives Xu Yan off screen left one cold look; her lips stay closed",
         zh="近景、慢推：阿令把水桶往旁邊一拉，許硯的手（左邊緣）撲空；阿令冷冷看他一眼；冷、不笑"),
    dict(loc="yard_dusk", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="yard_dusk",
         comp="medium close-up, closing in to a close-up by the end, of Xu Yan, his sleeves rolled up to the elbows, pained and unsmiling; behind him only the stone well and the bamboo fence of the same yard",
         lines=[("tangxiaotang", "他怎麼了？像被雷劈了一樣。", "畫外，憋笑")],
         motion="he jerks back as if struck in the chest, his left hand catching the rim of the well and his right hand pressing his chest; his lips stay closed",
         zh="近景、慢推（中近景推到近景）：許硯胸口像被打了一下，往後一仰，左手扶住井沿，右手按著胸口；痛、不笑"),
    dict(loc="yard_dusk", cam="Medium shot, tracking", chars=["qinshuang", "xuyan"], night="yard_dusk",
         comp="medium shot, Qin Shuang, cold, one bundle of about ten split logs tied with straw rope on her right shoulder, her old chopping knife back in the right side of her belt, and Xu Yan on screen right, his sleeves rolled up, leaning on the rim of the stone well",
         lines=[("qinshuang", "活該。話說得越好聽，越不能信。", "冷")],
         motion="Qin Shuang carries the bundle past Xu Yan without a glance and walks out of the frame on screen left toward the woodpile; his lips stay closed",
         zh="中景、跟拍（由右往左）：秦霜右肩扛一捆劈好的柴（草繩捆著約十根，柴刀在腰帶右邊）從扶著井沿的許硯身邊走過，看都沒看他，往左邊柴堆走出畫"),
    dict(loc="yard_dusk", cam="Close-up, slow push in", chars=["xuyan", "aling"], night="yard_dusk",
         comp="close-up of Xu Yan, his sleeves rolled up to the elbows, with a wry pained smile; behind him only the stone well of the same yard, and far behind it A-ling's back, soft and out of focus, walking away with the bucket",
         lines=[("xuyan", "好，我記住了。這裡的人，用騙的騙不來。", "又痛又服氣")],
         motion="rubbing his chest, he straightens up, watches A-ling carry the bucket away and lets out a long sigh",
         zh="近景、慢推：許硯揉著胸口直起身，看著阿令提水桶走開的背影（虛焦），嘆一口氣；苦笑（可以）（結尾）"),
    # ---- scene 3: the kitchen at night, the stove fire and Xu Yan's oil lamp, faint moonlight at the door. Axis: Xu Yan in
    # from the door on the left, A-ling on the stool before the fire mouth on the right; c34 on he squats on her left.
    dict(chapter="灶房", loc="kitchen_door", cam="Full shot from behind, tracking", chars=["xuyan", "aling"], nospeak=["xuyan"], night="kitchen",
         comp=f"full shot from the kitchen doorway right behind Xu Yan, the dark wooden door frame on both sides in the foreground: Xu Yan seen from behind standing on the threshold, his sleeves rolled up to the elbows, {LAMP}, held in his left hand; ahead of him inside the kitchen on screen right the clay stove, and A-ling, {ALING}, sitting on a low stool before its fire mouth with her back to the door, {KNIFE} in her right hand, one long wet grey whetstone on the floor before her",
         lines=[("xuyan", "這麼晚還沒睡？灶火我來看著就好。", "放輕聲音")],
         motion="Xu Yan pushes the half-open plank door wider with his right hand, steps in across the threshold and walks two steps toward the stove and A-ling, the lamp in his left hand; she keeps her back to him; his face is never seen",
         zh="全景、從許硯背後跟拍、鏡頭在灶房門口、前景門框（2026-11-07 審片重寫）：許硯背影站在門檻上（左手端陶碗油燈）右手推開門，跨過門檻往灶與阿令走兩步；阿令背對門坐灶口前矮凳，右手握短刀、面前一塊濕的灰磨石，沒有回頭；台詞是背影"),
    dict(loc="kitchen_cu", cam="Insert close-up, slow push in", chars=["aling"], night="kitchen", act=3,
         comp=f"insert close-up of A-ling's hands, the shot opens directly on {KNIFE} on one long wet grey whetstone from its very first frame: her right hand on the wooden handle and two fingers of her left hand pressing the blade, its edge turned outward, her grey-white cotton sleeves covering her wrists; only the hands, sleeves, knife and whetstone are in the frame, her face out of the frame; behind them only the firelit earthen floor of the same kitchen",
         lines=[],
         motion="the knife pushes forward along the whetstone and draws back, the blade flashing wet in the firelight",
         zh="手部特寫、慢推（第一格就是短刀與磨石）：阿令右手握木柄、左手兩指壓刀身（刀刃朝外），袖子蓋住手腕；短刀在磨石上推過去、拉回來，刀身一閃水光；短刀一律用 KNIFE 那一句"),
    dict(loc="kitchen_m", cam="Over-the-shoulder medium shot, slow push in", chars=["aling", "xuyan"], night="kitchen",
         comp=f"over-the-shoulder shot from behind Xu Yan, who stands two steps inside the kitchen: his left shoulder, his rolled-up sleeve and {LAMP}, held in his left hand in the left foreground; on screen right A-ling, {ALING}, sitting on the low stool before the fire mouth of the clay stove, her head bowed over {KNIFE} and the whetstone, a cold closed look, her eyes down",
         lines=[("aling", "你不用對我客氣，我是官府送來的罪奴。", "很輕、很冷，第一次開口")],
         motion="A-ling keeps her eyes down and goes on pushing and drawing the knife along the stone; Xu Yan stays standing with the lamp in his left hand, his lips closed",
         zh="過肩（許硯肩後拍阿令）、慢推：許硯站著（還沒蹲），左手端油燈在前景左；阿令不抬頭，繼續推刀拉刀（第一次開口，輕、冷）；冷、不笑"),
    dict(loc="kitchen_cu", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="kitchen",
         comp=f"medium close-up, closing in to a close-up by the end, of Xu Yan standing beside the clay stove, his sleeves rolled up to the elbows, {BELT}, {LAMP}, held in his left hand, a soft earnest look, his brows lifted a little, his eyes on A-ling off screen right; the flat top of the clay stove at the right edge of the frame; behind him only the earthen wall and the firewood stacked against it in the same kitchen",
         lines=[("xuyan", "官府把妳配到許家，在這個家裡，妳就不是罪奴。", "誠懇")],
         motion="he sets the lamp down on the stove top at the right edge, and only then squats down to her height, his eyes staying on her",
         zh="反打近景、慢推（中近景推到近景）：許硯站著、左手端油燈，先把油燈放到灶台上，才蹲下來跟她一樣高；誠懇、不笑"),
    dict(loc="kitchen_cu", cam="Close-up, slow push in", chars=["aling"], night="kitchen",
         comp=f"close-up of A-ling sitting before the fire mouth of the clay stove, her sleeves pulled down over her wrists, {KNIFE} in her right hand, a cold steady stare; behind her only the clay stove and its firelight in the same kitchen",
         lines=[("aling", "白天你也說得很好聽，後來怎麼樣了？", "冷")],
         motion="the hand pushing the knife stops, and she lifts her eyes to Xu Yan off screen left",
         zh="近景、慢推：阿令推刀的手停下，抬眼看許硯；冷"),
    dict(loc="kitchen_cu", cam="Close-up, slow push in", chars=["xuyan"], night="kitchen",
         comp=f"close-up of Xu Yan squatting beside the clay stove, his sleeves rolled up to the elbows, contrite: his eyes lowered, his brows drawn together, his mouth tight; {LAMP} now standing on the stove top at the right edge of the frame; behind him only the earthen wall of the same kitchen",
         lines=[("xuyan", "白天那句是空話，說來好聽的，我不該那樣說。", "老實認錯")],
         motion="he rubs his nose, looks down at the fire mouth, picks up one stick of firewood and turns it once in his hand",
         zh="近景、慢推：許硯（蹲著，陶碗油燈已在灶台上，不是玻璃燈）摸摸鼻子，低頭往灶口看，撿起一根柴在手上轉一下；認錯、不笑"),
    dict(loc="kitchen_m", cam="Medium shot, slow push in", chars=["aling", "xuyan"], night="kitchen",
         comp=f"medium shot, the clay stove on screen right with its fire mouth facing left and the fire burning only inside that fire mouth, its glow spilling across the bare packed earth floor; A-ling on the low stool just left of the fire mouth, her sleeves pulled down over her wrists, {KNIFE} in her right hand on the whetstone, a cold closed look, and Xu Yan squatting at the left edge of the frame, his sleeves rolled up",
         lines=[("aling", "那今晚這句呢？也是說來好聽的？", "冷，不看他")],
         motion="A-ling turns the knife over and hones the other side, its edge outward, without looking at him; Xu Yan's lips stay closed",
         zh="中景、慢推：土灶在畫面右、灶口朝左、火只在灶口裡（不是地上的火堆）；阿令把短刀翻過來磨另一面（刀刃朝外），眼睛沒看他；許硯蹲在左邊緣"),
    dict(loc="kitchen", cam="Reverse close-up, slow push in", chars=["xuyan"], night="kitchen_fire",
         comp="reverse close-up of Xu Yan squatting, his sleeves rolled up to the elbows, one stick of firewood in his hand, earnest and unsmiling, the firelight on his face; behind him only the earthen wall of the same kitchen",
         lines=[("xuyan", "這句不是。妳犯過什麼事，妳不說，我就不問。", "認真")],
         motion="he feeds the stick into the fire mouth, the fire flares up brighter, and he turns his head to A-ling off screen right",
         zh="反打近景、慢推：許硯把手上的柴添進灶口，火一下子亮起來，他轉頭看阿令；認真"),
    dict(loc="kitchen_cu", cam="Low-angle close-up, slow push in", chars=["aling"], night="kitchen",
         comp=f"low-angle close-up, the shot opens directly on A-ling's face and shoulders filling the frame from its very first frame, seen from the height of the stove fire, A-ling sitting on the low stool, her sleeves pulled down over her wrists, a cold level stare; {KNIFE} in her right hand at the bottom edge of the frame; the fire stays inside the stove mouth beside her at the right edge, its orange glow lighting her face from below; behind her only the dark roof beams of the same kitchen; her face fills most of the frame for the whole shot",
         lines=[("aling", "錢員外要的是人，你點個頭債就清了，為何不押我們？", "很輕")],
         motion="she lays the short knife flat across her knees, its edge turned away from Xu Yan off screen left, and turns on the stool to face him squarely; the camera stays close on her face",
         zh="低角度近景（灶火高度）、慢推（第一格就是臉與肩、整鏡不拉遠）：阿令把短刀橫放在膝上（刀刃朝外側、不朝許硯），轉過身正對許硯；火只在她身旁的灶口裡，照亮她的臉；冷（結尾，懸念到第 4 集）"),
    dict(loc="kitchen_cu", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="kitchen_fire", act=3,
         comp="medium close-up, closing in to a close-up by the end, of Xu Yan squatting before the fire mouth of the clay stove at the right edge of the frame, his sleeves rolled up to the elbows, one split stick of firewood held still in his right hand just before the fire mouth, his face turned to A-ling off screen right, a troubled look, his brows drawn together; the fire burning inside the stove mouth; behind him only the earthen wall of the same kitchen",
         lines=[],
         motion="his lips part as if to answer, then close again, the stick held still before the fire mouth; only then the fire pops and a burst of bright sparks flies out of the stove mouth, lighting up his face; the stick stays in his hand to the end",
         zh="近景、慢推（中近景推到近景）：許硯右手拿一根柴停在灶口前（不放進去，第 4 集 c01 才放），張口要答又停住；然後灶口啪地爆出一串火星照亮他的臉"),
]

HEAD = [
    "- 重製版 r2：照 `docs/videos/zhong-tian-qu-qi-e003-r2/script.md`（c01–c40 對應 s01–s40；含「2026-11-06 審稿後的修改」）；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。",
    "- 內部工作編號 903（`hailuo/*-dh-e903.json`、`colab/runs/e903/`）；發布 slug `zhong-tian-qu-qi-e003-r2`。不放集數、不放片名卡；c01 直接接第 2 集 c40（柴刀釘進門框）。",
    "- 狀態：許硯衣服已乾、袖子捲到手肘、捲紅紙插腰帶左邊，第一場手背沾木屑，s14–s16 右手拇指沾紅印泥（第二場已擦乾淨），第三場 s31–s34 左手端陶油燈（s34 放上灶台）；秦霜的舊柴刀 s01–s16 釘在門框（s02、s03、s16 腰帶空著），s16 拔回腰帶右邊，s29 右肩扛一捆柴；阿令沒戴鐵鐐、袖子蓋住手腕，s26–s30 提水桶，第三場磨一把短刀；字據一律空白紙、虛焦、只拍空白紙角或摺起來。",
    "- 長鏡要買的秒數（`r2.py` 的 BUY）：s21 8 秒（script.md 長鏡清單）；s22 10 秒（長鏡清單寫 8，錄好的兩句加停頓要 8.4 秒）；s04、s07、s08、s11、s13、s15 8 秒（錄好的配音每句加半秒超過 6 秒）。其餘照 `gen-dh` 的 5／6 秒。",
]
FOOT = [
    "- 場景參考：第一、二場在院子 `set-xujia-yuan-t1`（日頭偏西的低光 → 傍晚暗橘光，屋簷下曬菜乾）；第三場在灶房 `set-xujia-zao-t1`（灶火與油燈的暖橘光、門外一點冷月光）。近景背景都寫「同一個院子／同一個灶房」。",
    "- 唐小棠一律用 `tangxiaotang-portrait-t2`（gen-dh 的 PORTRAIT 對照）；近景構圖寫「下巴以上」，中景以上寫「襦裙從立領到腰一件闔上」。",
    "- 灰衣家丁與村民沒有定妝照：家丁只拍背影、肩膀以下或手（灰色交領粗布短褐、布包頭、布鞋）；村民只在籬笆外露上半身（宋式交領短打、布包頭）。",
    "- 阿令沒戴鐵鐐的定妝照：`aling-portrait-t1` 本身是沒有鐵鐐的半身像，照用，不另畫（script.md 清單 2 的「要補」不用做）。",
    "- 秦霜的 `cast.json` 造型寫著「柴刀插在腰帶」：`colab/runs/e903/extras.json` 把這句從每鏡的造型句拿掉，柴刀在哪裡改由各鏡構圖寫（s02、s03、s16 腰帶空著，s29 在腰帶右邊）。",
    "- 配樂：字據 tension（s01 刀釘門框一個重音、s13 念字據時壓低）、新手禮包 comedy（s19、s20、s25 系統句抽掉，s27 扣分一個重音）、灶房 suspense 慢段（s40 低音收尾）；音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy so the recorded lines (+0.5 s each) fit within buy - 0.3 s, allowing the cut's 1.1x
# slow-down (script.md 長鏡清單: c21, c22 8 s; the rest from the recorded audio, 2026-11-06).
BUY = {"s04": 8, "s07": 8, "s08": 8, "s11": 8, "s13": 8, "s15": 8, "s21": 8, "s22": 10}
# Recorded need (wav + 0.5 s a line): s04 6.9, s07 6.7, s08 6.9, s11 7.4, s13 7.5, s15 6.7 (Qian Yuanwai and the law lines
# run slow, 3.6 zh characters a second) -> 8; s22 8.4 (the review's added inner line) -> 10 instead of the script's 8;
# s21 7.9 stays 8. Within 0.4 s of buy - 0.3 and left at 6 (the cut's 1.1x covers them): s12 5.9, s30 5.8, s39 6.1.
