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
Live action (2026-11-08 prep, the e901/e902 live lessons): every visible face gets an expression written as brows, eyes,
mouth corners, jaw, throat and breath at the moment of the line; every on-screen speaker is turned in profile or
three-quarter toward the listener, with the camera locked about 30-45 degrees off the eyeline or over the listener's
shoulder (no frontal single-face push-in); NOSMILE is the only smile word in the prompts (the allowed c11 forced smile
c26 deliberate and c30 wry smiles are written as face movements; Qian Yuanwai's c11 one became a part-by-part scowl in e903 live fix1, the word grimace drew a grin); the eye
extreme close-ups use EYES; the fan is FAN, folded shut, and Qin Shuang's knife is CHOP in every shot it is in.
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
    # Live prep (2026-11-08): medium shots whose compositions grew with the expressions and the gaze keep the set to one
    # short line (route-a.md: the 1000-character cap).
    "yard_dusk_m": "In the dirt yard of the Xu farmhouse at dusk, the house eaves on screen left with strips of dried vegetables hanging under them, a wooden table in the middle, a stone well at the back right, dark orange sunset light from screen right casting very long shadows",
    # e903 live fix3 (2026-11-09, cut review 二-9): the kitchen as the set picture and the chosen s33-s38 takes draw it.
    "kitchen_brick": "Inside the small earthen kitchen of the Xu farmhouse at night, one red-brick stove with a black iron wok on its top and its fire mouth at the front, split firewood stacked in a pile beside it, lit only by the warm orange glow of the stove fire",
    "kitchen_s": "Inside the small earthen kitchen of the Xu farmhouse at night, a clay stove on screen right with its fire mouth facing left and the fire burning inside it, lit only by the warm orange glow of the stove fire",
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
# Live-action prep (2026-11-08), from e902 live fix1/fix2 (e002-r2/r2.py) and drama/WRITING.md 四、七、八: a face that must
# not smile gets no smile word at all except this one ban (smile, smirk, sneer, grin, unsmiling all came out as a warm
# smile; Qian Yuanwai's "smug smile", "sneer" and "forced smile" turned the villain friendly in e002 s27-s38).
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
# The eye extreme close-ups keep natural eyes ("a faint pale blue light in his pupils" drew glowing blue irises).
EYES = "his irises a natural dark brown from the first frame to the last, the whites of his eyes clear, only a tiny faint cold pale glint of reflected light in each pupil, like a catchlight"
# The villain's face (e002 fix1): mouth closed and turned down, eyes cold, brows low; never a smile word.
QIAN_FACE = "his face cold and hard: lips closed, the corners of his mouth pulled down, his eyes narrowed, cold and hard, his brows lowered"
# Qian Yuanwai's one fan, folded shut in every shot (e002 s38: opened, it grew a full face of calligraphy).
FAN = "one plain bamboo-ribbed folding fan with a blank face, folded shut"

SHOTS = [
    # ---- scene 1: the 字據, late afternoon (e002's same instant), low sun from the gate on the right. Axis: the Xu side
    # (Xu Yan, Tang Xiaotang, Qin Shuang) on screen left; Qian Yuanwai and the four servants on screen right by the gate.
    # 2026-11-07 fix4 (the last round, redesigned rather than reworded): s01 is the knife alone; s02 and s16 hold Qin
    # Shuang from the chest up (her portrait carries a knife at the belt); the grip on Tang Xiaotang stays in s02.
    dict(chapter="字據", loc="yard_late_cu", cam="Insert close-up, locked", chars=[], night="yard_late", act=3,
         comp=f"insert close-up of the upright wooden post of the yard gate, the shot opens directly on the post from its very first frame: {CHOP} driven into the left face of the post at chest height, the tip and the front third of the blade sunk deep inside the wood, the rest of the blade level in the air and the handle jutting out into the empty air toward screen left; only the post and the knife fill the frame; behind them only the out-of-focus bamboo fence of the same yard",
         lines=[],
         motion="the knife, just driven into the post, quivers hard, its handle shaking up and down in the empty air while a few pale splinters fall from the cut; the quiver slowly dies away and the knife stays buried in the post to the end",
         zh="門柱特寫、固定（第一格就是院門門柱；2026-11-07 第四輪重設計）：柴刀刀尖與前三分之一刀身已釘進門柱左面、刀柄朝左懸在空中，刀身猛顫、幾片木屑掉下，顫動慢慢停；畫面只有門柱與刀。家丁的手與唐小棠的袖子移出本鏡（兩輪都畫成家丁握刀柄），抓手臂留在 s02 右邊緣、s03 鬆手；音效「篤」接第 2 集 c40"),
    dict(loc="yard_late_cu", cam="Medium close-up, tracking", chars=["qinshuang"], night="yard_late",
         comp=f"medium close-up tracking with Qin Shuang as she strides in from screen left, framed from the chest up the whole shot, her belt below the frame, both hands empty, in profile toward the servant at the right edge, the camera about 40 degrees off her eyeline, her eyes on the back of his head, never the lens; her face hard: brows drawn down low, eyes narrowed, jaw set, mouth pressed into a flat line; on screen right the gate post with {CHOP} buried in it at her shoulder height, its handle toward screen left; beside the post one grey-clad servant seen only from behind, in {SERV1}, his right hand gripping a slender forearm in a peach-pink brocade sleeve at the bottom right corner; behind them only the bamboo fence of the same yard",
         lines=[("qinshuang", "放手。這一刀是故意偏的，下一刀不會。", "冷，不大聲")],
         motion=f"Qin Shuang strides from screen left to one step behind the servant, lifts her empty right hand and rests it on the knife handle, leaving the blade in the post; she says the line to the back of his head in profile, her nostrils flaring once and her eyes narrowing further on 「下一刀不會」; the servant keeps his back turned and his grip on the sleeve to the end; {NOSMILE}",
         zh="中近景、跟拍（由左往右；2026-11-07 第四輪重設計）：秦霜胸口以上、腰帶在畫面下緣外（定妝照腰間有刀），兩手空空從左大步走到家丁背後一步，右手搭上門柱上的刀柄不拔；右邊緣家丁背影抓著一截桃粉織錦袖子（唐小棠不入鏡，只見袖子）；冷、不笑。真人版（2026-11-08）：秦霜側臉朝畫右的家丁、鏡頭偏離視線約 40°，眼睛盯著他的後腦、不看鏡頭；眉往下壓成一直線、眼睛瞇起、下巴收緊、嘴抿成線，說「下一刀不會」時鼻翼一張、眼睛再瞇；從頭到最後一格都不笑（NOSMILE）"),
    dict(loc="yard_late_m", cam="Over-the-shoulder medium shot, slow push in", chars=["qinshuang", "tangxiaotang", "xiaohe"], night="yard_late", act=4,
         comp=f"over-the-shoulder shot from behind Qin Shuang: her right shoulder and high ponytail fill the left foreground, her belt empty; that shoulder is Qin Shuang, who appears nowhere else in the frame; on screen right one grey-clad servant seen only from the shoulders down, his head above the top of the frame, his right hand on the left forearm of Tang Xiaotang, {TANG}, glaring at him: brows drawn together and down, eyes narrowed, lips pressed tight, chin tucked; at the left, near the house door at the back left, little Xiaohe in her patched lilac jacket, hugging her small woven straw rabbit to her chest, frightened: eyes wide, brows drawn up, lips pressed together",
         lines=[],
         motion=f"the servant lets go and steps back one step; Tang Xiaotang shakes her sleeve free with a sharp breath through her nose, rubs her left forearm, glares at him and backs off past the left edge to stand behind Xu Yan off screen left; little Xiaohe runs back into the house door at the back left, hugging her rabbit; all lips stay closed; {NOSMILE}",
         zh="過肩（秦霜肩後拍家丁與唐小棠）、慢推：家丁（只露肩膀以下）鬆手退一步；唐小棠（t2）甩開袖子退到許硯身後，揉左前臂瞪家丁；小禾從許硯身後跑回左後屋門口；秦霜腰帶空著。表情（2026-11-08 真人版）：唐小棠瞪家丁：眉頭往中間往下皺、眼睛瞇起、嘴抿緊、收下巴，甩袖子時鼻子出一口氣；小禾害怕：眼睛睜大、眉毛往上皺、嘴抿著；從頭到最後一格都不笑（NOSMILE）"),
    # Live prep (2026-11-08): e002 fix1 s29 — "cold sneer" and a low frontal push drew the villain laughing with open teeth.
    dict(loc="yard_late_cu", cam="Low-angle close-up, locked", chars=["qianyuanwai"], night="yard_late",
         comp=f"low-angle close-up of Qian Yuanwai, the camera low below his chin looking up at him, his body and face turned three-quarter to screen left toward Qin Shuang off screen left, the camera about 35 degrees off his eyeline, in his dark gold silk robe with roundel patterns, {QIAN_FACE}, his teeth clenched behind his closed lips, a muscle jumping in his jaw, {FAN} in his right hand, three gold rings on his right hand; behind him only the yard gate and the autumn tree of the same yard",
         lines=[("qianyuanwai", "好個潑辣貨。來人，拿紙筆，三個都寫進字據！", "冷笑")],
         motion=f"he jabs the folded fan at Qin Shuang off screen left, speaking to her in three-quarter profile, eyes on her, never into the lens, his lips thin and closing between words, no teeth, his nostrils flaring on 「好個潑辣貨」; then he sweeps the fan toward the wooden table in the middle of the yard; {NOSMILE}",
         zh="低角度近景、固定（2026-11-08 真人版：原本慢推、寫「咬牙冷笑」；第 2 集 s29 同樣寫法兩支都露齒大笑）：錢員外（深金色團花錦袍、三枚金戒指）身體與臉四分之三側向畫左、朝畫外左邊的秦霜，鏡頭偏離視線約 35°，不看鏡頭；用合起的素面摺扇朝秦霜一點，再往院子中間的木桌一揮。表情（QIAN_FACE）：嘴閉著、嘴角往下、眼睛瞇起又冷又硬、眉頭壓低、牙咬在閉著的嘴裡、下顎一抽，說「好個潑辣貨」時鼻翼一張；從頭到最後一格都不笑（NOSMILE），不寫任何笑的字"),
    dict(loc="yard_late", cam="Insert close-up, slow push in", chars=[], night="yard_late", act=3,
         comp="insert close-up of the wooden table top, the shot opens directly on the table top from its very first frame: one sheet of plain pale yellow paper, completely blank, one ink brush and one small inkstone; the two hands of one grey-clad servant in grey coarse cotton cross-collared sleeves reaching in; only the hands and sleeves are in the frame, his face out of the frame; behind them only the out-of-focus dirt ground of the same yard",
         lines=[],
         motion="the hands smooth the blank sheet flat on the table, then pick up the brush and dip it in the inkstone",
         zh="手部特寫、慢推（第一格就是木桌桌面）：家丁的雙手（灰短褐袖口）把空白的淡黃紙在桌上攤平，拿起毛筆在硯台裡蘸墨"),
    # Live prep (2026-11-08): the medium-to-medium-close push became a locked side two-shot (they face each other across
    # the table), so neither face is pushed in on frontally (e002 live: frontal single pushes said the line into the lens).
    dict(loc="yard_late_m", cam="Medium shot, locked", chars=["xuyan", "qianyuanwai"], night="yard_late",
         comp=f"side medium shot across the wooden table, Xu Yan in {XU1}, {BELT}, on screen left and Qian Yuanwai at the right edge facing each other, one blank sheet of pale yellow paper on the table between them; Xu Yan in profile facing screen right, his face hard: brows drawn down, eyes narrowed on Qian, jaw set; Qian Yuanwai in profile facing screen left, {QIAN_FACE}, {FAN} in his right hand",
         lines=[("xuyan", "慢著。這張字據，錢員外最好別寫。", "聲音一沉")],
         motion=f"Xu Yan strides in from screen left to the table, slaps his right hand flat on the blank sheet and looks up at Qian on screen right, speaking to him in profile, eyes on him, never the lens, his lips pressing together between phrases; Qian's eyes narrow further and his lips stay closed; {NOSMILE}",
         zh="中景、固定（2026-11-08 真人版：原本中景推到中近景；改成兩人隔著桌子側面相對的雙人鏡，不對單張臉正面推近）：許硯（書生袍已乾、袖子捲到手肘）從左大步走到桌邊，右手啪地按住空白的紙，抬頭看錢員外；錢員外在畫右邊緣、側面朝畫左。表情：許硯聲音一沉：眉往下壓、眼睛瞇起盯著錢員外、下巴收緊，字句之間嘴抿著；錢員外 QIAN_FACE（嘴閉、嘴角往下、眼睛又冷又硬、眉壓低），聽到後眼睛再瞇；兩人從頭到最後一格都不笑（NOSMILE）"),
    # e903 live fix3 (2026-11-09, cut review 二-4: in the over-the-shoulder shot he pressed Xu Yan with an amiable smile
    # from 4.7 s to the last frame, the line running to the end so nothing can be trimmed; the fan turned white then
    # brown inside the shot): the side two-shot across the table of s06 (the design that held), both in profile and small
    # in the frame, the camera square to their eyelines; the face is QIAN_FACE plus a part-by-part scowl with no teeth;
    # the fan leaves the shot and is never named (s11 fix1: written tucked shut, it still came out open), so he slaps his
    # palm on the table instead; the blank sheet of s06 stays on the table.
    dict(loc="yard_late_m", cam="Medium shot, locked", chars=["qianyuanwai", "xuyan"], night="yard_late",
         comp="side medium shot across the wooden table, the camera square to their eyelines, both seen from the waist up and small in the frame; Xu Yan on screen left in profile facing screen right, his sleeves rolled up to the elbows, his face hard: brows drawn down, eyes on Qian, jaw set; Qian Yuanwai on screen right in profile facing screen left toward Xu Yan, never the lens, both hands empty, scowling: his brows knotted down hard, his eyes narrowed and cold, his lips pressed thin, the corners of his mouth pulled down, no teeth showing; one blank sheet of pale yellow paper flat on the table between them",
         lines=[("qianyuanwai", "怎麼？欠債還錢天經地義，你還想賴帳不成？", "逼問")],
         motion=f"Qian slaps his right palm flat on the table and leans over it toward Xu Yan, staying in profile, his eyes on him, never the lens, speaking through a clenched jaw, his lips closing thin between phrases, his brows clamping lower on 「賴帳不成」; Xu Yan does not move, his lips closed; {NOSMILE}",
         zh="側面雙人中景、固定（2026-11-09 真人版 fix3，成片審查二-4：d1 選的那支從 4.7 秒到最後一格都和氣地笑著逼問，台詞到鏡尾、剪不掉；扇子在鏡內從白色變淺褐）：改成跟 s06 一樣隔著桌子的側面雙人鏡，鏡頭垂直兩人的視線，兩人都是側臉、腰以上、在畫面裡小小的；錢員外在畫右側臉朝畫左看許硯、不看鏡頭。扇子整鏡拿掉、英文一個字都不寫（s11 fix1 寫了合著插腰帶，還是畫成打開的圓扇），拍桌改成右手掌往桌上一拍，再隔著桌子往許硯傾身；s06 那張空白的紙留在桌上。表情：嘴閉、嘴角往下、眉往下鎖緊、眼睛瞇起又冷、嘴唇抿薄、不露齒，說「賴帳不成」時眉再壓；許硯眉往下壓、看著他、嘴閉著不動；兩人從頭到最後一格都不笑（NOSMILE），不寫任何笑的字。台詞不變"),
    dict(loc="yard_late_cu", cam="Medium close-up, locked", chars=["xuyan"], night="yard_late",
         comp=f"medium close-up of Xu Yan standing at the wooden table, framed from the chest up with space above his head, his sleeves rolled up to the elbows, a little sweat on his brow, {BELT}, his body and face turned three-quarter to screen right toward Qian Yuanwai off screen right, the camera about 40 degrees off his eyeline, his eyes on Qian, never the lens; his face set: brows straight and low, eyes fixed and hard, jaw firm, lips pressing together between phrases; his right hand rests flat on one blank sheet of pale yellow paper on the table at the bottom edge of the frame, his left hand empty; behind him only the bamboo fence and the autumn tree of the same yard",
         lines=[("xuyan", "不賴帳。大衡律配婚篇，她們三個的名字記在縣衙名冊上。", "慢條斯理")],
         motion=f"he straightens up, his right hand staying flat on the blank pale yellow sheet, draws one slow breath in through his nose, and on 「大衡律配婚篇」 points his empty left hand out past the gate toward the county town, his face staying three-quarter toward Qian; {NOSMILE}",
         zh="近景反打、固定（2026-11-08 真人版：原本中近景推到近景，單人正面推近；改成胸口以上、鏡頭偏離他的視線約 40°）：許硯身體與臉四分之三側向畫右、朝畫外右邊的錢員外，不看鏡頭；直起身，手還按著紙，另一手指向院門外縣城。表情：眉毛平直壓低、眼睛定住發硬、下巴收緊、字句之間嘴抿著，說「大衡律配婚篇」前用鼻子慢慢吸一口氣；從頭到最後一格都不笑（NOSMILE）"),
    dict(loc="yard_late_m", cam="Medium shot, tracking", chars=["xuyan", "qianyuanwai"], night="yard_late",
         comp=f"medium shot, Xu Yan on screen left, his sleeves rolled up to the elbows, a little sweat on his brow, {BELT}, in profile facing screen right toward Qian Yuanwai, his face hard: brows drawn down, eyes locked on Qian, jaw set; Qian Yuanwai on screen right in profile facing him, {QIAN_FACE}; only these two men inside the yard; beyond the bamboo fence about five {VILL}, soft and out of focus, only their heads and shoulders over the fence",
         lines=[("xuyan", "官府配的人，你私自押走，就是搶官府的人。", "一字一句")],
         motion=f"Xu Yan rounds the corner of the table and takes one step toward Qian, staying on his left, speaking to him in profile, eyes on him, never the lens, biting off each word, his jaw tightening on 「搶官府的人」; Qian leans back a little, his eyes darting and his throat bobbing as he swallows, his lips staying closed; {NOSMILE}",
         zh="中景、跟拍（跟著許硯往右）：許硯繞過桌角朝錢員外走近一步（仍在他左邊），錢員外往後仰一下；背景籬笆外村民（虛焦）。真人版（2026-11-08）：兩人側面相對，許硯側臉看錢員外、不看鏡頭。表情：許硯一字一句：眉往下壓、眼睛釘住錢員外、下巴收緊，說「搶官府的人」時下巴再一緊；錢員外 QIAN_FACE，往後仰時眼睛亂飄、喉結一動、嘴閉著；兩人都不笑（NOSMILE）"),
    dict(loc="yard_late_cu", cam="Medium close-up, locked", chars=["qianyuanwai"], night="yard_late", act=3,
         comp=f"medium close-up of Qian Yuanwai on screen right, framed from the chest up, his body turned three-quarter to screen left toward Xu Yan off screen left, the camera about 35 degrees off his eyeline, never the lens, his right hand raised before his chest holding {FAN} into a slim closed bundle of ribs, uneasy, his face hard and closed: lips pressed shut, the corners of his mouth pulled down, his brows lowered and twitching, his small eyes darting sideways, a bead of sweat at his temple; directly behind him the shoulder-high bamboo fence and, beyond it, the heads and shoulders of about five {VILL}, soft and out of focus; in the soft out-of-focus left foreground one small hand in a peach-pink brocade cuff holding the small gold abacus with wooden beads",
         lines=[],
         motion=f"the small hand in the left foreground flicks one abacus bead; Qian, the folded fan held still in midair, glances back over his shoulder at the villagers whispering over the fence, turns back toward Xu Yan off screen left and swallows hard, his throat bobbing; the fan stays folded shut to the end; all lips stay closed; {NOSMILE}",
         zh="中近景、固定（2026-11-08 真人版：原本慢推、正面；改成四分之三朝畫外左邊的許硯、鏡頭偏約 35°；表情寫成嘴閉緊、嘴角往下、眉壓低又一抽、小眼睛往旁邊飄、太陽穴一滴汗，喉結一動；村民虛焦；不笑 NOSMILE）（2026-11-07 第四輪重設計，原雙人鏡）：錢員外胸口以上、右手合起的摺扇停在胸前半空（整鏡不打開）；身後就是齊肩的竹籬笆，籬笆外約五個村民只露頭肩；左前景虛焦一隻桃粉袖口的小手托著金算盤，撥一顆珠；錢員外回頭瞄一眼村民、轉回來喉結一動。唐小棠的臉不入鏡（定妝照露齒笑），點頭這一下拿掉"),
    # e903 live fix1 (2026-11-09, both d1 seeds failed review-picks-a: he grinned with his teeth the whole shot, the fan
    # was open, 1102 nearly faced the lens): "grimace", "stretched sideways" and "forcing" read as a smile, so the face is
    # a scowl written part by part with no smile word; the fan is already tucked shut in his belt from the first frame (no
    # tuck to write); a medium close-up from his right side about 45 degrees, his face in profile toward screen left,
    # like the s06 and s09 side shots that held. The line is unchanged.
    dict(loc="yard_late_cu", cam="Medium close-up, locked", chars=["qianyuanwai"], night="yard_late",
         comp=f"medium close-up of Qian Yuanwai alone on screen right, framed from the chest up with space above his small black cap, the camera at his right side about 45 degrees off his eyeline, his face in profile toward screen left facing Xu Yan off screen left, never the lens; {FAN}, already tucked into the front of his belt from the first frame, both hands empty; scowling: his brows knotted down hard, his eyes narrowed and cold, his lips pressed thin, the corners of his mouth pulled down, his jaw clenched, no teeth showing; behind him only the yard gate, soft and out of focus",
         lines=[("qianyuanwai", "行，人我不押。那你拿什麼還？房子、地，還有你？", "咬牙")],
         motion=f"he stays turned in profile toward Xu Yan off screen left, eyes on him, never the lens, and speaks through his clenched jaw, his lips closing thin between phrases; on 「還有你」 he jabs one finger toward him off screen left and his brows knot lower; the fan stays tucked shut in his belt to the end; {NOSMILE}",
         zh="中近景、固定（2026-11-09 真人版 fix1：d1 兩支都從頭到尾露齒大笑、扇子打開，1102 臉幾乎正對鏡頭；「grimace」「stretched sideways」「forcing」都被演成笑，全部拿掉）：只拍錢員外一人、胸口以上，鏡頭在他右邊約 45°，側臉朝畫左、看畫外左邊的許硯，不看鏡頭（比照 s06、s09 有效的側面鏡）；扇子第一格就合著插在腰帶前面，兩手空著，不寫收扇子的動作；說「還有你」時手指往許硯一戳、眉再往下鎖。表情改成逐部位寫的怒臉：眉往下鎖緊、眼睛瞇起又冷、嘴唇抿薄、嘴角往下、下巴咬緊、不露齒；從頭到最後一格都不笑（NOSMILE），不寫任何笑的字。台詞不變"),
    dict(loc="yard_late", cam="Reverse close-up, locked", chars=["xuyan"], night="yard_late",
         comp="reverse close-up of Xu Yan, his sleeves rolled up to the elbows, a little sweat on his brow, his body and face turned three-quarter to screen right toward Qian Yuanwai off screen right, the camera about 40 degrees off his eyeline, his eyes on Qian, never the lens; his face firm: brows straight and low, eyes holding Qian's, jaw set, lips pressing together between phrases; behind him only the bamboo fence of the same yard",
         lines=[("xuyan", "房子和地你先別急。給我三天，二十兩一文不少。", "穩")],
         motion=f"he lifts his hand off the blank sheet below the frame, draws a short breath through his nose, and on 「給我三天」 holds up three fingers toward Qian, giving one small firm nod on 「一文不少」; {NOSMILE}",
         zh="反打近景、固定（2026-11-08 真人版：原本慢推）：許硯四分之三側向畫右、朝畫外右邊的錢員外，鏡頭偏約 40°，不看鏡頭；把按著紙的手收回來，伸出三根手指。表情：眉毛平直壓低、眼睛盯住錢員外、下巴收緊、字句之間嘴抿著，說「給我三天」前鼻子短吸一口氣，「一文不少」時小小點一下頭；從頭到最後一格都不笑（NOSMILE）"),
    dict(loc="yard_late_m", cam="Medium shot, slow push in", chars=["qianyuanwai", "xuyan"], night="yard_late",
         comp=f"medium shot past one corner of the wooden table in the foreground, Qian Yuanwai standing behind the table with one ink brush in his right hand, bent over the pale yellow sheet lying flat on the table, soft and out of focus, nothing on it readable from the camera's side, his face turned down to the sheet and three-quarter toward Xu Yan, {QIAN_FACE}; Xu Yan with his sleeves rolled up at the left edge of the frame in profile facing Qian, watching the brush: jaw clenched, brows drawn together, lips pressed shut",
         lines=[("qianyuanwai", "三日後日落前還清二十兩，否則收房收地。", "念")],
         motion=f"Qian writes with the brush as he reads the words aloud to Xu Yan, his eyes going from the sheet to Xu Yan and back, never into the lens, his lips thin, the corners of his mouth pulled down; then he lays the brush on the inkstone; Xu Yan swallows, his throat bobbing, his lips staying closed; {NOSMILE}",
         zh="中景、慢推、前景木桌一角：錢員外抓起毛筆彎腰寫，邊寫邊念，寫完把筆擱在硯台上；紙面虛焦、看不到字；許硯在左邊緣。真人版（2026-11-08）：錢員外臉朝紙、四分之三朝許硯，眼睛在紙與許硯之間來回，不看鏡頭；許硯側面看筆。表情：錢員外 QIAN_FACE，嘴唇薄、嘴角往下；許硯咬牙、眉頭皺、嘴抿緊，嚥一下口水；兩人都不笑（NOSMILE）"),
    dict(loc="yard_late", cam="Insert close-up, slow push in", chars=["xuyan"], night="yard_late", act=3,
         comp="insert close-up of one bottom corner of the pale yellow sheet on the wooden table, the shot opens directly on the blank paper corner and one small box of red ink paste from its very first frame: only the plain blank corner, the written part outside the frame, and Xu Yan's right hand in his rolled-up blue-grey cuff; only the hand and the paper corner are in the frame, his face out of the frame; behind them only the out-of-focus dirt ground of the same yard",
         lines=[],
         motion="his thumb presses into the red ink paste, then presses down hard on the blank corner, leaving one red thumbprint, and lifts away",
         zh="手部特寫、慢推（第一格就是紙角與紅印泥）：只拍空白紙角（寫字的部分在畫面外）；許硯的拇指按進紅印泥，再重重按在紙角留下紅指印，拇指抬起"),
    # e903 live fix2 (2026-11-09, both fix1 seeds failed review-picks: the folded fan was wide open from the first frame
    # in both, one raised it to point, the servants showed their faces, 1202 turned square to the lens for 5.5-8.0 s; the
    # tracking shot turned him to the lens twice and the fan opened three times out of three): the prop and the sheet
    # leave the shot and are never named (the word alone draws one in); both hands clasped behind his back; the servants
    # are already out of the gate, the gate open on the empty path as in s16; locked, the camera behind his left
    # shoulder about 70 degrees off his eyeline; no walking; only a small jab of the index finger and a chin lift on
    # 「收房」; he speaks from the first second so the line ends before the last half second.
    dict(loc="yard_late_m", cam="Medium shot, locked", chars=["qianyuanwai"], night="yard_late",
         comp=f"medium shot from behind his left shoulder, the camera about 70 degrees off his eyeline, Qian Yuanwai standing still at the open yard gate on screen right, his back half turned to the camera, framed from the knees up, both hands clasped behind his back; his head turned back over his shoulder, his face in profile toward screen left, looking at Xu Yan off screen left, never the lens; {QIAN_FACE}, his lips thin, no teeth; beyond the open gate only the empty dirt path outside, nobody else in the frame",
         lines=[("qianyuanwai", "許秀才，三日後太陽一落，我帶人來收房。", "拖長音")],
         motion=f"he stays standing at the gate, his feet not moving, and starts speaking at once in the first second, drawling the line to Xu Yan off screen left with his face in profile, eyes on him, never the lens, his hands clasped behind his back; on 「收房」 he jabs his index finger once toward him and lifts his chin; the line ends well before the last half second; {NOSMILE}",
         zh="中景、固定（2026-11-09 真人版 fix2：fix1 兩支都從第一格就把摺扇整把打開、一支舉扇指人，家丁正面露臉，1202 在 5.5–8.0 秒轉成正面對鏡頭；追拍兩次都把他轉向鏡頭，扇子三次都打開）：扇子與字據整鏡拿掉，提示詞裡一個字都不寫（寫了這個字就會畫出來），字據已收好；雙手背在身後。家丁已出院門、不入鏡，門外小路空著，接 s16 的空門。固定機位，鏡頭在他左肩後方、偏離視線約 70°；他站在畫右院門口、半背向鏡頭，整段不走動，只把頭轉過肩、側臉朝畫左看畫外的許硯，不看鏡頭。說「收房」時只用食指朝他一點、下巴一抬。第一秒就開口，讓台詞在最後 0.5 秒前講完。表情：QIAN_FACE，嘴唇薄、嘴角往下、不露齒；從頭到最後一格都不笑（NOSMILE）。台詞不變"),
    dict(loc="yard_late_cu", cam="Medium close-up, locked", chars=["qinshuang"], night="yard_late",
         comp=f"medium close-up of Qin Shuang standing on screen left beside the upright wooden gate post on screen right, framed from the chest up the whole shot with her belt below the bottom edge of the frame, her face hard: brows drawn down straight, eyes narrowed, mouth a flat line; {CHOP} buried in the post at her shoulder height with its handle toward her, the one knife in the frame; her right hand open and empty, raised just beside the handle; beyond the post only the open gate and the empty dirt path outside, the visitors already gone",
         lines=[("qinshuang", "手印按了，三天後拿不出二十兩，這房子就沒了。", "冷")],
         motion=f"her empty right hand closes on the handle, wrenches the knife free of the post, turns it blade down and lowers it past the bottom edge of the frame to the right side of her belt; then she turns her head and shoulders three-quarter to screen left toward Xu Yan off screen left, the camera about 40 degrees off her eyeline, and says the line to him, eyes on him, never the lens, a short breath out through her nose on 「房子就沒了」; {NOSMILE}",
         zh="中近景、固定（2026-11-08 真人版：原本慢推；說話時頭與肩四分之三轉向畫外左邊的許硯、鏡頭偏約 40°、不看鏡頭；眉往下壓成直線、眼睛瞇起、嘴抿成線，說「房子就沒了」時鼻子出一口氣；不笑 NOSMILE）（2026-11-07 第四輪重設計，原全景）：秦霜胸口以上站在門柱左邊、腰帶在畫面下緣外；第一格右手空著、張開停在刀柄旁；她握住刀柄把柴刀從門柱拔下、刃朝下往下收出畫面（插回腰帶右邊），再回頭看畫外左邊的許硯；錢員外與家丁已經走了（出門留給 s15 的結尾與腳步聲），許硯不入鏡；冷（結尾）"),
    # ---- scene 2: the novice pack, the same yard at dusk (dark orange light from the right). Axis: Xu Yan sits at the left of
    # the table facing right, Tang Xiaotang across on the right; c26 he walks to the well at the back right, left of A-ling.
    # e903 live fix3 (2026-11-09, cut review 二-6 and 二-8: she said 「三天賺二十兩？」 square into the lens for about one
    # second from the first frame; at the cut to s18 two bowls and the abacus on the table vanished and the background
    # changed): the same side angle as the chosen s18 fix1 take (the camera square to the table line, the eaves on screen
    # left), she walks in from screen right already in profile facing screen left toward Xu Yan from the first frame; the
    # abacus stays at her waist and the tabletop stays bare, like s18; her costume is the portrait's, written out.
    dict(chapter="新手禮包", loc="yard_dusk_m", cam="Full shot, locked", chars=["tangxiaotang", "xuyan"], night="yard_dusk",
         comp="side full shot of the wooden table, the camera square to the table line about 60 degrees off her eyeline, both small in the frame; Tang Xiaotang on screen right in profile facing screen left toward Xu Yan from the first frame, never the lens, in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow, the small gold abacus hanging at her waist, worried: brows drawn together, eyes wide on him, lips pressed tight between words; Xu Yan standing on screen left in profile facing her, his sleeves rolled up to the elbows, his brows drawn together, his lips pressed; the bare tabletop between them",
         lines=[("tangxiaotang", "三天賺二十兩？你家米缸都快見底了。", "倒抽一口氣")],
         motion=f"Tang Xiaotang speaks at once, walking left to the table in profile, eyes on Xu Yan, never the lens, sucking in a sharp breath on 「二十兩」; she sits down on the right side of the bare table, the abacus staying at her waist; Xu Yan sits down across from her with a heavy breath out, his lips closed; {NOSMILE}",
         zh="側面全景、固定（2026-11-09 真人版 fix3，成片審查二-6、二-8：d1 選的那支第一格起約一秒正面對鏡頭講「三天賺二十兩？」；接 s18 時桌上的兩個碗與金算盤不見、背景也換了）：改成跟 s18 fix1 選定那支同一個側面方向（鏡頭垂直桌子的線、屋簷在畫左），鏡頭偏離她的視線約 60°；唐小棠第一格就是側臉朝畫左的許硯，從畫右走到桌邊、一邊走一邊開口，不看鏡頭；金算盤留在腰間、不放上桌，桌面空著，接 s18 的空桌；服裝照定妝照寫明：交領短襦闔上、百褶裙繫蝴蝶結。許硯在畫左側臉朝她，跟著坐下、重重出一口氣、嘴閉著。表情：唐小棠眉頭皺、眼睛睜大看他、字句之間嘴抿緊，「二十兩」倒抽一口氣；兩人都不笑（NOSMILE）。台詞不變"),
    # e903 live fix1 (2026-11-09, both d1 seeds failed review-picks-a: 1101 said the line square into the lens and smiled
    # at the end, 1102 grinned at 0 s and 3.8 s and smiled with closed lips at 5.8 s while still speaking, so nothing can be
    # trimmed): the side two-shot across the table like s06 (the camera square to their eyelines, both in profile, small
    # in the frame, the short push stopping on both); "strained" and "pulled together and up" played as a wry smile, so
    # the face is knotted brows, clenched jaw, lips flat between words and the last frame is lips flat, head lowered.
    # Tang Xiaotang's costume is the portrait's closed cross-collar jacket over the pleated skirt with its bow.
    dict(loc="yard_dusk_m", cam="Medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="yard_dusk",
         comp="side medium shot across the wooden table at table height, the camera square to their eyelines, both seen from the waist up and small in the frame; Xu Yan sitting on screen left in profile facing screen right, his sleeves rolled up to the elbows, his eyes hard on her, never the lens: brows knotted down, jaw clenched, lips pressed flat between words; Tang Xiaotang sitting on screen right in profile facing him, in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow, worried: brows drawn together, eyes on him, lips closed; the bare tabletop between them",
         lines=[("xuyan", "所以要找一門三天就能賺到二十兩的買賣。", "硬撐")],
         motion=f"Xu Yan puts both palms flat on the table, leans toward her in profile, eyes on her, never the lens, taps one finger once on 「三天」 and swallows before 「二十兩」; then his lips press flat and he lowers his head to the last frame; Tang Xiaotang's lips stay closed; the camera pushes in only a little and keeps both; {NOSMILE}",
         zh="側面雙人中景、慢推（短）（2026-11-09 真人版 fix1：d1 1101 正面直視鏡頭講整句、結尾笑；1102 視線對、但 0 秒與 3.8 秒露齒笑、5.8 秒還在講時閉嘴微笑，裁不掉）：改成跟 s06 一樣的側面雙人鏡，兩人隔著桌子坐、鏡頭在桌面高度、垂直他們的視線，兩人都是側臉、腰以上、在畫面裡小小的；慢推只推一點、停在兩人，不推到單張臉。許硯在畫左側臉朝畫右看唐小棠、不看鏡頭；雙手撐桌往前傾，「三天」手指點桌、「二十兩」前嚥口水，最後嘴抿平、頭低下到最後一格。拿掉 strained、pulled together and up（被演成苦笑），表情寫成眉往下鎖、下巴咬緊、字句之間嘴抿平、眼睛硬硬盯著她；唐小棠在畫右側臉朝畫左，穿定妝照的交領短襦闔上、百褶裙繫蝴蝶結，發愁：眉頭皺、看著他、嘴閉著；兩人都不笑（NOSMILE）。台詞不變"),
    # Live prep (2026-11-08): e002 fix1 s35 — EYES, the eyes only, the eyeline slightly right, one person once.
    dict(loc="yard_dusk", cam="Extreme close-up, slow push in", chars=["xuyan"], night="yard_dusk",
         comp=f"extreme close-up of Xu Yan's eyes only, the shot opens directly on his eyes from its very first frame and the frame never widens: his two eyes and brows fill the frame, {EYES}, his eyeline slightly to screen right, never into the lens; nothing else in the frame, one face only, no second figure, no double exposure",
         lines=[("xitong", "叮。新手禮包發放：肥皂配方一份。", "冷淡，叮一聲")],
         panel=[("新手禮包：肥皂配方", "panel")],
         motion="his eyes widen and his brows jump up, his pupils tighten and he blinks once, slowly, the frame holding only his eyes and brows to the last frame",
         zh="眼睛大特寫、慢推（第一格就是眼睛，整鏡只有兩隻眼睛與眉毛、不拉遠）：虹膜自然深褐、瞳孔裡只有一點很小的反光（EYES；2026-11-08 真人版，第 2 集 s13、s35 寫「淡藍光」四支都是亮藍虹膜），視線偏畫右、不看鏡頭，只有一張臉、沒有疊影；眼睛睜大、眉毛一跳、瞳孔一縮、慢慢眨一下"),
    dict(loc="yard_dusk_cu", cam="Close-up, slow push in", chars=["xuyan"], night="yard_dusk",
         comp="close-up of Xu Yan sitting at the wooden table, his sleeves rolled up to the elbows, his face warm in the dark orange dusk light from screen right, his body turned three-quarter to screen right, his eyes fixed on the open air just before his face, never the lens, eager: his brows raised high, his eyes wide, his lips parted a little; the bare wooden tabletop below the frame; behind him only the eaves and the dried vegetables of the same yard in the dark orange dusk",
         lines=[("xitong", "材料自備，工具自備。", "冷淡")],
         panel=[("材料自備・工具自備", "panel")],
         motion=f"he sits up straight and waits a moment, then reaches his right hand forward into the empty air before his face, closes it on nothing, looks at his empty hand, and his brows pull down into a frown, his mouth twisting to one side; his lips stay closed; {NOSMILE}",
         zh="近景、慢推（2026-11-08 真人版：拿掉臉上的淡藍光，只留暗橘夕光；身體四分之三朝畫右、眼睛看面前的空氣、不看鏡頭；先眉毛高揚、眼睛睜大、嘴微張地期待，抓空後眉往下壓、嘴歪向一邊；不笑 NOSMILE）：許硯往前坐直，等一下，伸手在空氣裡摸一下，什麼都沒有，皺眉"),
    dict(loc="yard_dusk_cu", cam="Close-up to big close-up, slow push in", chars=["xuyan"], night="yard_dusk",
         comp="close-up, closing in to a big close-up by the end, of Xu Yan sitting at the wooden table, his sleeves rolled up to the elbows, his body turned three-quarter to screen right, his eyes on the empty air before him, never the lens, a pained grimace: his brows drawn together, one corner of his mouth pulled down and twitching, his lips closed; behind him only the eaves of the same yard in the dark orange dusk",
         lines=[("xuyan", "送個方子就叫禮包，連一塊豬油都不給？", "心裡話，嘴閉著", "inner"),
                ("xitong", "嫌少可以退。退了就什麼都沒有。", "冷")],
         motion=f"the corner of his mouth twitches down in a pained grimace, he taps two fingers twice on the table, then rolls his eyes up, lets out a huff through his nose and leans back; his lips stay closed the whole shot; {NOSMILE}",
         zh="近景、慢推（近景推到大近景，長鏡買 8 秒；2026-11-08 真人版：身體四分之三朝畫右、看面前的空氣、不看鏡頭；眉頭皺、一邊嘴角往下抽，翻白眼時鼻子哼一聲；NOSMILE）：許硯嘴角抽一下（不笑），手指在桌上敲兩下，翻白眼往後一靠；心裡話，嘴閉著；系統冷冷回一句"),
    dict(loc="yard_dusk_cu", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "tangxiaotang"], nospeak=["tangxiaotang"], night="yard_dusk",
         comp=f"over-the-shoulder shot across the wooden table from behind Tang Xiaotang: her shoulder and the back of her head with its two looped buns and pink ribbons fill the right foreground, her face turned away from the camera, {TANG}; Xu Yan sitting on screen left, his body turned three-quarter toward her in the right foreground, his sleeves rolled up to the elbows, framed from the chest up with space above his head, sour and put out: his brows pulled down, his jaw clenched, his mouth pressed into a flat line, his eyes fixed on the empty air before his face, never the lens; behind him only the eaves and the dried vegetables of the same yard",
         lines=[("xuyan", "不退。有方子，總比什麼都沒有強。", "心裡話，嘴閉著", "inner"),
                ("tangxiaotang", "你發什麼呆？眼睛直直盯著空氣看。", "狐疑")],
         motion=f"first Xu Yan stares at the empty air, clenches his jaw and gives one small nod; then Tang Xiaotang raises her right hand and waves it slowly back and forth a hand's width before his eyes, tilting her head, the back of her head still toward us; he blinks twice, his brows jumping up, and turns his eyes to her; his lips stay closed the whole shot; {NOSMILE}",
         zh="過肩（唐小棠背後拍許硯）、慢推（2026-11-07 第四輪重設計，原雙人鏡；長鏡買 10 秒；2026-11-08 真人版：許硯身體四分之三朝右前景的她、眼睛盯著空氣不看鏡頭，眨眼時眉毛一跳；NOSMILE）：唐小棠背對鏡頭在右前景（丸子頭、立領），她的台詞是背影；許硯胸口以上、頭上留空，臭著臉盯著空氣、咬牙、輕輕點頭（心裡話，嘴閉著）；接著唐小棠舉右手在他眼前一掌寬處慢慢晃、歪頭，許硯眨兩下眼轉過來看她。重抽時拿掉許硯的定妝照與 angle-b、唐小棠的兩張 angle"),
    # e903 live fix3 (2026-11-09, cut review 二-5: he grinned with his teeth through the whole line in the close-up, the
    # line spanning the shot): "eager", "brows lifted" and "eyes wide and bright" played as a grin, so the face is written
    # intent, part by part; a side medium shot like the chosen s18 fix1 take, the camera about 60 degrees off his eyeline,
    # his face smaller; the light kept dim (the d1 pick was brighter and more golden than s22).
    dict(loc="yard_dusk_cu", cam="Medium shot, locked", chars=["xuyan"], night="yard_dusk",
         comp="side medium shot of Xu Yan alone, sitting at the left side of the wooden table, seen from the waist up and small in the frame with space above his head, in profile facing screen right toward Tang Xiaotang off screen right, the camera about 60 degrees off his eyeline, never the lens, his sleeves rolled up to the elbows, both shoulders of his robe whole and smooth; intent: brows drawn slightly together, eyes fixed on her, jaw firm, lips pressing together between phrases; the right side of the frame holds only the dim eaves in the fading dark orange dusk",
         lines=[("xuyan", "我在想一個買賣。我會做比皂角好洗十倍的肥皂。", "認真")],
         motion=f"he stays in profile toward her, eyes on her, never the lens, and with both hands shapes one small square block in the air above the table, giving one firm nod on 「好洗十倍」, his lips pressing together after the line; {NOSMILE}",
         zh="側面中景、固定（2026-11-09 真人版 fix3，成片審查二-5：d1 選的那支整句露齒笑、最後一格也笑，台詞橫跨整鏡、剪不掉）：近景改成側面中景，跟 s18 fix1 選定那支同方向，許硯腰以上、在畫面裡小小的、頭上留空，正側面朝畫右、看畫外右邊的唐小棠，鏡頭偏離視線約 60°，不看鏡頭；兩手在桌上比出一塊方方的東西，「好洗十倍」點一下頭。拿掉 eager、brows lifted、eyes wide and bright（被演成咧嘴笑），表情改成逐部位寫：眉頭微皺、眼睛定在她身上、下巴收緊、字句之間嘴抿著，講完嘴抿住；從頭到最後一格都不笑（NOSMILE）。袍子兩肩完整（成片審查二-14：肩膀破洞）；暮色寫暗一點（d1 比 s22 亮、偏金黃）。台詞不變"),
    dict(loc="yard_dusk", cam="Insert close-up, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="yard_dusk",
         comp="insert close-up of Tang Xiaotang's hand and the small gold abacus on the wooden table, the shot opens directly on the abacus from its very first frame: the palm-sized abacus with its gold frame and wooden beads lying on the table, her right forefinger on the beads, the cuff of her peach-pink brocade sleeve; only the hand, sleeve and abacus are in the frame, her face out of the frame above, her ruqun one closed garment from the high collar to the waist; behind it only the out-of-focus tabletop of the same yard",
         lines=[("tangxiaotang", "真比皂角好十倍，那就不愁沒有人買。", "畫外，精明")],
         motion="her right forefinger flicks one bead up and back down, then presses one bead and holds it; no mouth is in the frame",
         zh="算盤特寫、慢推（第一格就是算盤）：唐小棠右手食指把算盤珠撥上去又撥下來，最後按住一顆；只拍手，沒有嘴"),
    dict(loc="yard_dusk", cam="Extreme close-up, slow push in", chars=["xuyan"], night="yard_dusk",
         comp=f"extreme close-up of Xu Yan's eyes only, the shot opens directly on his eyes from its very first frame and the frame never widens: his two eyes and brows fill the frame, {EYES}, his eyeline slightly to screen right, never into the lens; nothing else in the frame, one face only, no second figure, no double exposure",
         lines=[("xitong", "好感度，開啟。", "冷淡，叮一聲")],
         panel=[("好感度：開啟", "panel")],
         motion="his eyes widen a little and his brows lift, then his eyes flick toward screen right, toward the well at the back right, the frame holding only his eyes and brows to the last frame",
         zh="眼睛大特寫、慢推（第一格就是眼睛，整鏡只有兩隻眼睛與眉毛、不拉遠）：虹膜自然深褐、瞳孔裡只有一點很小的反光（EYES，2026-11-08 真人版），只有一張臉、沒有疊影；眼睛微睜、眉毛一揚，眼珠往畫右（右後方井邊）一轉"),
    dict(loc="yard_dusk_m", cam="Medium shot, tracking", chars=["xuyan", "aling"], night="yard_dusk",
         comp=f"medium shot, Xu Yan on screen left, his sleeves rolled up to the elbows, {BELT}, putting on a tender look: his head tilted, his brows lifted and drawn together in the middle, his eyes soft and half-lidded, the corners of his mouth pressed up in a practised, too-sweet curve; at the back right A-ling standing by the stone well in her plain grey-white cotton dress, {ALING}, one wooden bucket full of water in her right hand, her head bowed, her eyes lowered, her brows drawn low and still, her lips pressed together, her jaw tight",
         lines=[("xuyan", "阿令，妳別怕。有我在，誰都帶不走妳。", "自以為深情")],
         motion="Xu Yan gets up, straightens his collar, walks to the well and reaches for the bucket in A-ling's hand, speaking to her in three-quarter profile, eyes on her, never the lens, his left hand laid on his chest on 「有我在」; she does not move and does not look up, her lips closed",
         zh="中景、跟拍（跟著許硯往右後的井邊）：許硯站起來整整衣襟，走到井邊伸手要接阿令（沒戴鐵鐐、袖子蓋住手腕）手上的水桶；阿令沒動；許硯笑得刻意（可以）。真人版（2026-11-08）：許硯四分之三側臉朝阿令說話、不看鏡頭，說「有我在」時左手按胸口。表情：許硯裝深情：歪頭、眉毛揚起往中間皺、眼睛半垂裝溫柔、嘴角刻意往上抿成太甜的弧（劇本允許的刻意笑，寫成臉怎麼動，提示詞不寫笑字）；阿令低頭垂眼、眉壓低不動、嘴抿緊、下巴繃著，不抬頭"),
    dict(loc="yard_well_cu", cam="Insert close-up, slow push in", chars=[], night="yard_dusk",
         comp="insert close-up at waist height beside the stone well, the shot opens directly on one wooden bucket full of water from its very first frame: the bucket hangs from a young woman's slender right hand in a plain grey-white cotton sleeve pulled down over her wrist, her fist closed around its handle; a man's open right hand in a rolled-up blue-grey sleeve reaches in from the left edge of the frame, still a forearm's length short of the handle; only the two hands, the sleeves and the bucket are in the frame, all faces above the frame; behind them only the stone well and the bamboo fence in the dim orange dusk light of the same yard",
         lines=[("xitong", "這叫空話，宿主。扣分。阿令好感 -5。", "冷")],
         panel=[("阿令 好感 0 → -5", "panel")],
         motion="in the first second her hand swings the bucket away to screen right, the water sloshing up to the rim and staying inside; his hand keeps reaching into the space where the bucket was and his fingers close on empty air; the bucket ends hanging at the right side of the frame, still in her hand, his empty hand at the left",
         zh="水桶特寫、慢推（2026-11-07 第四輪重設計，原阿令近景；三輪都沒拉開）：第一格就是阿令右手提著的滿桶水（灰白袖子蓋住手腕），許硯的手從左邊緣伸進來、還差一個前臂遠；第一秒她就把桶往右甩開，水晃到桶緣不灑出，許硯的手伸到原處抓空；最後桶在畫面右、他的空手在左。阿令的臉不入鏡，「冷冷看他一眼」拿掉"),
    dict(loc="yard_dusk", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="yard_dusk",
         comp="medium close-up, closing in to a close-up by the end, of Xu Yan, his sleeves rolled up to the elbows, his body turned three-quarter to screen right toward the well, never the lens, stung: his brows jerked up and together, his eyes squeezed half shut, his lips pressed shut; behind him only the stone well and the bamboo fence of the same yard",
         lines=[("tangxiaotang", "他怎麼了？像被雷劈了一樣。", "畫外，憋笑")],
         motion=f"he jerks back as if struck in the chest, sucking in a sharp breath through his nose, his left hand catching the rim of the well and his right hand pressing his chest; his lips stay closed; {NOSMILE}",
         zh="近景、慢推（中近景推到近景）：許硯胸口像被打了一下，往後一仰，左手扶住井沿，右手按著胸口；痛、不笑。表情（2026-11-08 真人版）：眉毛一跳往中間皺、眼睛擠成半閉、嘴抿死，鼻子猛吸一口氣；身體四分之三朝畫右的井、不看鏡頭；從頭到最後一格都不笑（NOSMILE）"),
    dict(loc="yard_dusk", cam="Medium shot, tracking", chars=["qinshuang", "xuyan"], night="yard_dusk",
         comp=f"medium shot, Qin Shuang, her face hard: brows drawn down straight, eyes narrowed, mouth a flat line, one bundle of about ten split logs tied with straw rope on her right shoulder, {CHOP} tucked in the right side of her belt, and Xu Yan on screen right, his sleeves rolled up, leaning on the rim of the stone well, wincing: brows drawn up, lips pressed shut",
         lines=[("qinshuang", "活該。話說得越好聽，越不能信。", "冷")],
         motion=f"Qin Shuang carries the bundle past Xu Yan in profile, gives him only one sidelong look out of the corner of her eye as she says the line, never into the lens, a short huff through her nose on 「活該」, and walks out of the frame on screen left toward the woodpile; Xu Yan winces, his lips closed; {NOSMILE}",
         zh="中景、跟拍（由右往左）：秦霜右肩扛一捆劈好的柴（草繩捆著約十根，柴刀在腰帶右邊）從扶著井沿的許硯身邊走過，看都沒看他，往左邊柴堆走出畫。真人版（2026-11-08）：秦霜側面走過，說話時只用眼角斜他一眼（說話要看對方的規則；「看都沒看」改成只斜一眼），不看鏡頭；柴刀照 CHOP 那一句插在腰帶右邊。表情：秦霜眉往下壓成直線、眼睛瞇起、嘴抿成線，「活該」時鼻子哼一聲；許硯皺眉往上、嘴抿死；兩人都不笑（NOSMILE）"),
    # Live prep (2026-11-08): the script's wry smile is allowed but written as face movements, with no smile word; he
    # turns three-quarter toward A-ling at the back right, the camera locked about 40 degrees off his eyeline.
    dict(loc="yard_dusk", cam="Close-up, locked", chars=["xuyan", "aling"], night="yard_dusk",
         comp="close-up of Xu Yan at the left of the frame, his sleeves rolled up to the elbows, his body and face turned three-quarter toward the back right, the camera about 40 degrees off his eyeline, watching A-ling, never the lens; rueful: his brows drawn up in the middle, his eyes tired, one corner of his mouth tugged up crookedly, not a happy face; behind him the stone well of the same yard, and far beyond it at the right A-ling's back, small, soft and out of focus, walking away with the bucket",
         lines=[("xuyan", "好，我記住了。這裡的人，用騙的騙不來。", "又痛又服氣")],
         motion="rubbing his chest, he straightens up, watches A-ling carry the bucket away, says the line after her with a slow shake of his head, and lets out a long sigh, his shoulders dropping",
         zh="近景、固定（2026-11-08 真人版：原本慢推、正面；改成許硯在畫左、身體與臉四分之三轉向右後方的阿令，鏡頭偏約 40°，不看鏡頭）：許硯揉著胸口直起身，看著阿令提水桶走開的背影（虛焦），嘆一口氣；苦笑（可以）（結尾）。表情：眉頭中間往上、眼神累、一邊嘴角歪歪地往上扯，不是開心的臉，說完慢慢搖頭、長嘆一口氣、肩膀一垮（劇本允許的苦笑，提示詞不寫笑字）"),
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
    dict(loc="kitchen_s", cam="Over-the-shoulder medium shot, slow push in", chars=["aling", "xuyan"], night="kitchen",
         comp=f"over-the-shoulder shot from behind Xu Yan, who stands two steps inside the kitchen: his left shoulder, his rolled-up sleeve and {LAMP}, held in his left hand in the left foreground, his face turned away from the camera; on screen right A-ling, {ALING}, on the low stool before the stove's fire mouth, her head bowed over {KNIFE} and the whetstone, her face in profile toward Xu Yan at the left, her eyelids lowered, her eyes on the blade, never the lens; her face closed and cold: brows drawn low and still, lips barely parting, jaw tight",
         lines=[("aling", "你不用對我客氣，我是官府送來的罪奴。", "很輕、很冷，第一次開口")],
         motion=f"A-ling keeps her eyes down and goes on pushing and drawing the knife along the stone, letting out one slow breath before 「罪奴」; Xu Yan stays standing with the lamp in his left hand, his lips closed; {NOSMILE}",
         zh="過肩（許硯肩後拍阿令）、慢推：許硯站著（還沒蹲），左手端油燈在前景左；阿令不抬頭，繼續推刀拉刀（第一次開口，輕、冷）；冷、不笑。真人版（2026-11-08）：阿令側臉朝畫左的許硯、眼皮垂著看刀、不看鏡頭（她要到 s35 才抬眼；自動補的「看著對方」與此衝突，以側臉朝他、垂眼為準）。表情：眉壓低不動、嘴唇只為說話微微張開、下巴繃緊，說「罪奴」前慢慢出一口氣；不笑（NOSMILE）"),
    dict(loc="kitchen_cu", cam="Medium shot, locked", chars=["xuyan"], night="kitchen",
         comp=f"medium shot from a low camera, Xu Yan standing beside the clay stove, framed from the knees up with space above his head, his sleeves rolled up to the elbows, {BELT}, {LAMP}, held in his left hand, his body and face turned three-quarter to screen right toward A-ling off screen right, the camera about 40 degrees off his eyeline, never the lens, earnest and sober: his brows lifted a little and drawn together, his eyes fixed on her, his lips firm between words; the flat top of the clay stove at the right of the frame at his waist height; behind him only the earthen wall and the firewood stacked against it in the same kitchen",
         lines=[("xuyan", "官府把妳配到許家，在這個家裡，妳就不是罪奴。", "誠懇")],
         motion=f"he sets the lamp down on the stove top at the right of the frame, where it stays standing with its small flame burning to the end; then he crouches down to her eye level, his face coming down to the middle of the frame and staying in it, his eyes on her, his voice softening on 「妳就不是罪奴」 with one slow nod; {NOSMILE}",
         zh="中景、固定、低機位（2026-11-08 真人版：身體與臉四分之三朝畫外右邊的阿令、鏡頭偏約 40°、不看鏡頭，「妳就不是罪奴」聲音放軟、慢慢點一下頭；NOSMILE）（2026-11-07 第四輪重設計，原中近景推近景：推近後燈出框、臉出框）：許硯膝蓋以上、頭上留空，左手端陶碗油燈，先把燈放到畫面右邊的灶台上（燈一直留在畫面裡亮著），再蹲下跟她一樣高，臉落到畫面中間；眉微揚、眉心收、嘴抿緊（誠懇）。重抽時拿掉許硯的定妝照與 angle-b"),
    dict(loc="kitchen_cu", cam="Medium close-up, locked", chars=["aling"], night="kitchen",
         comp=f"medium close-up from her left front, the camera about 40 degrees off her eyeline toward Xu Yan off screen left, A-ling sitting on the low stool before the fire mouth of the clay stove, {ALING}, framed from the top of her head down to the whetstone, her head bowed over her work; at the bottom of the frame {KNIFE} lies flat on one long wet grey whetstone on a low wooden bench before her at her waist height, her right hand on its handle and two fingers of her left hand pressing the blade; her face closed and cold: brows drawn low, eyelids lowered, lips pressed thin, jaw tight, her eyes down on the blade; behind her only the clay stove and its firelight in the same kitchen",
         lines=[("aling", "白天你也說得很好聽，後來怎麼樣了？", "冷")],
         motion=f"her hands stop in the middle of a stroke and stay pressing the knife flat on the whetstone to the end; she lifts her eyes, then her head, and looks at Xu Yan off screen left, her face three-quarter toward him, never the lens, her brows drawn low and straight, her eyes narrowing a little as they meet his, her lips thin between words; {NOSMILE}",
         zh="中近景、固定（2026-11-08 真人版：原本慢推；抬頭後臉四分之三朝畫外左邊的許硯、鏡頭偏約 40°、不看鏡頭；冷臉寫成眉壓低、眼皮垂、嘴抿薄、下巴繃緊，對上他的眼時眼睛微瞇；不笑 NOSMILE）（2026-11-07 第四輪重設計，原近景：兩支都把刀舉起來）：從她左前方拍，頭頂到磨石都在畫面裡；磨石放在她腰高的矮木凳上（同 s32、s33 選用片段），短刀平放在磨石上、兩手按著；推刀的手停住、刀一直平貼磨石，她先抬眼再抬頭，直視畫外左邊的許硯；冷"),
    # e903 live fix1 (2026-11-09, both d1 seeds failed review-picks-b: on 「我不該那樣說」 he turned his face to the lens
    # and the corners of his mouth rose; the line fills 0-6 s, so nothing can be trimmed): the camera at his left side
    # about 70 degrees off his eyeline, Xu Yan crouching in clean profile facing screen right toward A-ling off the right
    # frame edge the whole shot; his eyes stay on the stick and on the last phrase only his eyes lift toward the right
    # frame edge, the head does not turn; contrite written as brows, lips and mouth corners pulled down, no smile word.
    dict(loc="kitchen_cu", cam="Medium shot, locked", chars=["xuyan"], night="kitchen",
         comp="medium shot from his left side, the camera about 70 degrees off his eyeline, Xu Yan crouching in clean profile facing screen right toward A-ling off screen right for the whole shot, never the lens, framed from his knees up with space above his head, his sleeves rolled up to the elbows, contrite: brows drawn together, eyes lowered, lips tight between words, the corners of his mouth pulled down; one split stick of firewood lying on the packed earth floor right before his knees, inside the frame; the orange glow of the fire mouth on his face from screen right; behind him only the earthen wall of the same kitchen",
         lines=[("xuyan", "白天那句是空話，說來好聽的，我不該那樣說。", "老實認錯")],
         motion=f"he stays in profile, turned toward A-ling off screen right, rubs his nose, picks the stick up from the floor and looks down at it in his hands, turning it once; on 「我不該那樣說」 he lifts only his eyes toward the right frame edge, never toward the camera, his head not turning, a short sigh through his nose; the stick stays in his hands to the end; {NOSMILE}",
         zh="中景、固定（2026-11-09 真人版 fix1：d1 兩支都在說「我不該那樣說」時把臉轉成正面對鏡頭、嘴角上揚，台詞佔滿 0–6 秒、剪不掉；改成鏡頭在他左邊、偏離視線約 70°，許硯整鏡正側面朝畫右、朝畫外右邊的阿令，不看鏡頭；眼睛一直看手上的柴，說「我不該那樣說」時只抬眼往畫面右緣看、頭不轉、不朝鏡頭，鼻子輕嘆；表情逐部位寫：眉頭皺、眼睛垂、字句之間嘴抿緊、嘴角往下，不寫任何笑的字，NOSMILE；台詞不變）（2026-11-08 真人版：原本慢推）（2026-11-07 第四輪重設計，原近景）：許硯蹲著、膝蓋以上、頭上留空，第一格一根劈柴就躺在他膝前的地上（畫面內）；摸鼻子、往右下灶口看、撿起那根柴在手上轉一下，柴一直拿在手上；認錯、不笑。油燈不入鏡（上次寫了燈，燈跑到地上）。重抽時拿掉許硯的定妝照與 angle-b"),
    dict(loc="kitchen_cu", cam="Medium close-up, locked", chars=["aling"], night="kitchen",
         comp=f"medium close-up from her left front, the same framing as before: A-ling sitting on the low stool before the fire mouth of the clay stove, {ALING}, framed from the top of her head down to the whetstone, her head bowed, her face in profile toward Xu Yan off screen left, her eyes down on the blade, never the lens, her face closed and cold: brows drawn slightly together, lips tight, jaw set; at the bottom of the frame {KNIFE} lies flat on one long wet grey whetstone on a low wooden bench before her at her waist height; the fire burning only inside the stove mouth behind her at the right; behind her only the clay stove in the same kitchen",
         lines=[("aling", "那今晚這句呢？也是說來好聽的？", "冷，不看他")],
         motion=f"she turns the knife over on the whetstone with both hands, its edge outward, and strokes the other side along the stone, forward and back, her eyes staying on the blade the whole shot, a short cold breath out through her nose on 「也是說來好聽的」; the knife stays flat on the stone to the end; {NOSMILE}",
         zh="中近景、固定（2026-11-08 真人版：原本慢推；側臉朝畫外左邊的許硯、眼睛一直看刀、不看鏡頭（劇本「不看他」，自動補的「看著對方」以此為準）；眉頭微皺、嘴抿緊、下巴繃著，說「也是說來好聽的」時鼻子冷冷出一口氣；不笑 NOSMILE）（2026-11-07 第四輪重設計，原雙人中景：一支刀變大菜刀舉起、一支越軸）：同 s35 的機位與景別，只拍阿令（許硯在畫外左邊蹲著）；短刀在矮凳上的磨石翻面、磨另一面（刀刃朝外），眼睛一直看刀、刀一直平貼磨石；火只在她身後右邊的灶口裡"),
    # e903 live fix3 (2026-11-09, cut review 二-7 and 八-1: the episode's closing promise, he was nearly frontal with a
    # faint pleased smile at 1.6 s and on the last frame, the line running to the end; the stick vanished without being
    # fed in): a side medium shot from his left about 65 degrees off his eyeline, in profile toward A-ling off screen
    # right, smaller in the frame; "lifted in the middle" goes (no upward face word); the kitchen is written as the set
    # picture and the chosen s33-s37 takes show it (the red-brick stove with its black iron wok, the stacked firewood).
    dict(loc="kitchen_brick", cam="Medium shot, locked", chars=["xuyan"], night="kitchen_fire",
         comp="medium shot from his left side, the camera about 65 degrees off his eyeline, Xu Yan squatting on screen left in profile facing screen right toward A-ling off screen right, never the lens, framed from his knees up with space above his head, his sleeves rolled up to the elbows, both shoulders of his robe whole and smooth, one split stick of firewood in his right hand; earnest: brows drawn together, eyes steady on her, jaw firm, lips pressing together between phrases; the fire mouth of the red-brick stove at the right edge of the frame lighting his face",
         lines=[("xuyan", "這句不是。妳犯過什麼事，妳不說，我就不問。", "認真")],
         motion=f"he pushes the stick into the fire mouth until it is inside, the fire flares brighter, and still in profile, eyes on A-ling off screen right, never the lens, he speaks to her, giving one slow nod on 「我就不問」, his lips pressed together after the line; {NOSMILE}",
         zh="側面中景、固定（2026-11-09 真人版 fix3，成片審查二-7、八-1：第 3 集最後一句承諾，d1 選的那支臉幾乎正面、1.6 秒與最後一格嘴角帶淺笑，台詞到鏡尾、剪不掉；手上的柴沒塞進灶口就不見）：近景改成從他左邊拍的中景，鏡頭偏離視線約 65°，許硯蹲在畫左、正側面朝畫右、看畫外右邊的阿令，膝蓋以上、在畫面裡小一點，不看鏡頭；先把柴整根推進畫右紅磚灶的火口、火一亮，再說，「我就不問」慢慢點一下頭。拿掉「眉心往上」（不寫任何往上的臉部字），表情：眉頭皺、眼睛穩穩看她、下巴收緊、字句之間嘴抿著，講完嘴抿住；從頭到最後一格都不笑（NOSMILE）。灶房照場景圖與 s33–s37 選定片段寫（紅磚灶、黑鐵鍋、堆起的劈柴，kitchen_brick）；袍子兩肩完整（成片審查二-14）。台詞不變"),
    # e903 live fix3 (2026-11-09, cut review 二-9, 二-11 and 八-3: the low angle from the fire showed roof beams and a
    # lattice window, a different room, and her face came out rounder with heavier lipstick than s33-s37): the framing of
    # s35 and s37 (the chosen takes): a medium close-up from her left front about 45 degrees off her eyeline, the red-brick
    # stove and its fire mouth behind her, the one short knife lying flat on the whetstone on the low bench, her hands
    # resting on it; the same three A-ling pictures and the same set picture as s35/s37 (unchanged); natural, no make-up.
    dict(loc="kitchen_brick", cam="Medium close-up, locked", chars=["aling"], night="kitchen",
         comp=f"medium close-up from her left front, the same framing as before, the camera about 45 degrees off her eyeline: A-ling sitting on the low stool before the fire mouth of the red-brick stove, {ALING}, framed from the top of her head down to the whetstone, her face bare of make-up; at the bottom of the frame {KNIFE} lies flat on one long wet grey whetstone on a low wooden bench before her, both her hands resting on it; her face closed and cold: brows drawn low and straight, lips pressed together, jaw tight, her eyes down on the blade",
         lines=[("aling", "錢員外要的是人，你點個頭債就清了，為何不押我們？", "很輕")],
         motion=f"her hands stay still on the knife flat on the whetstone; she lifts her eyes, then her head, and looks at Xu Yan off screen left, her face three-quarter toward him, never the lens, guarded: eyes narrowing as they search his face, lips pressing together between words, her chin lifting a little on 「為何不押我們」; {NOSMILE}",
         zh="中近景、固定（2026-11-09 真人版 fix3，成片審查二-9、二-11、八-3：低角度從灶火高度往上拍，拍到屋樑與格子窗、像另一間房，阿令的臉也比 s33–s37 圓、口紅濃）：改用 s35、s37 選定片段的取景：從她左前方拍、鏡頭偏離視線約 45°，頭頂到磨石都在畫面裡，身後是紅磚灶與火口（kitchen_brick）；短刀（KNIFE）平放在矮木凳上的磨石上、兩手按著不動；臉素淨、不化妝。她先抬眼再抬頭，四分之三朝畫外左邊的許硯、不看鏡頭；戒備：眼睛微瞇打量他的臉、字句之間嘴抿著，「為何不押我們」時下巴微抬；從頭到最後一格都不笑（NOSMILE）。參考圖跟 s35、s37 一樣（阿令三張加灶房場景圖，不改）。台詞不變"),
    # e903 live fix3 (2026-11-09, cut review 二-9 and 八-3: a yellow mud stove and the night yard through a door behind
    # him, a different room from s31-s38): the kitchen written as the set picture and the chosen s33-s38 takes (the
    # red-brick stove with its black iron wok on top, the fire mouth at the front, the stacked split firewood), the camera
    # from his left side about 60 degrees off his eyeline, in profile; the push stops at a medium close-up.
    dict(loc="kitchen_brick", cam="Medium close-up, slow push in", chars=["xuyan"], night="kitchen_fire", act=3,
         comp="medium close-up from his left side, the camera about 60 degrees off his eyeline, Xu Yan squatting in profile facing screen right before the fire mouth of the red-brick stove at the right edge of the frame, its black iron wok on top, his sleeves rolled up to the elbows, both shoulders of his robe whole and smooth, one split stick of firewood held still in his right hand just before the fire mouth, his face turned to A-ling off screen right, never the lens, troubled: his brows knotted, his eyes darting down to the fire and back to her, his jaw working; behind him only the stacked split firewood",
         lines=[],
         motion=f"his lips part as if to answer, then press shut again and he swallows, his throat bobbing, the stick held still before the fire mouth; only then the fire pops and a burst of bright sparks flies out of the stove mouth, lighting up his face; the stick stays in his hand to the end; {NOSMILE}",
         zh="中近景、慢推（2026-11-09 真人版 fix3，成片審查二-9、八-3：d1 選的那支是土黃色泥灶、身後門外是夜裡的院子，跟 s31–s38 像兩間房）：灶房照場景圖與 s33–s38 選定片段寫：紅磚灶、灶上黑鐵鍋、火口在前、身後堆起的劈柴（kitchen_brick）；鏡頭在他左邊、偏離視線約 60°，許硯蹲著、正側面朝畫右的灶口，臉朝畫外右邊的阿令、不看鏡頭；慢推停在中近景。動作不變：右手拿一根柴停在灶口前（不放進去，第 4 集 c01 才放），張口要答又抿住、嚥口水，灶口啪地爆出一串火星照亮他的臉。表情：眉頭打結、眼睛往火瞄一下又回到她、下顎動了動；不笑（NOSMILE）；袍子兩肩完整（成片審查二-14）"),
]

HEAD = [
    "- 重製版 r2：照 `docs/videos/zhong-tian-qu-qi-e003-r2/script.md`（c01–c40 對應 s01–s40；含「2026-11-06 審稿後的修改」）；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。",
    "- 內部工作編號 903（`hailuo/*-dh-e903.json`、`colab/runs/e903/`）；發布 slug `zhong-tian-qu-qi-e003-r2`。不放集數、不放片名卡；c01 直接接第 2 集 c40（柴刀釘進門框）。",
    "- 狀態：許硯衣服已乾、袖子捲到手肘、捲紅紙插腰帶左邊，第一場手背沾木屑，s14–s16 右手拇指沾紅印泥（第二場已擦乾淨），第三場 s31–s34 左手端陶油燈（s34 放上灶台）；秦霜的舊柴刀 s01–s16 釘在門框（s02、s03、s16 腰帶空著），s16 拔回腰帶右邊，s29 右肩扛一捆柴；阿令沒戴鐵鐐、袖子蓋住手腕，s26–s30 提水桶，第三場磨一把短刀；字據一律空白紙、虛焦、只拍空白紙角或摺起來。",
    "- 真人版前置（2026-11-08，照第 1、2 集真人版的教訓）：每張露臉的臉都寫成臉怎麼動（眉、眼、嘴角、下巴、喉嚨、呼吸）；每一句露嘴的台詞，說話的人側臉或四分之三側臉朝聽的人，單人鏡改成固定、鏡頭偏離視線 30–45°，或用過肩（不對單張臉正面推近）；提示詞裡唯一的笑字是 NOSMILE 那一句（c11 錢員外的假笑寫成咬牙硬擠的怪臉，c26 刻意的笑、c30 苦笑寫成嘴角與眉眼怎麼動）；錢員外的臉用 QIAN_FACE；眼睛大特寫用 EYES（自然深褐虹膜）；摺扇一律 FAN（合著），秦霜的柴刀一律 CHOP。",
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
