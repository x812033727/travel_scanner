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
Live action (2026-11-09 prep, the e901-e903 live lessons, route-a.md and e003-r2 fix1-fix3): every visible face gets its
expression written part by part (brows, eyes, mouth corners, jaw, breath); every on-screen speaker is turned in profile
or three-quarter toward the listener, never the lens, the camera locked about 40-60 degrees off the eyeline or over the
listener's shoulder, speakers framed from the chest or waist up with space above the head (no frontal push-in on one
face); NOSMILE is the only smile word in the prompts (the allowed c05 awkward laugh, c18 Xiaohe's delight, c25 Tang
Xiaotang's slight smile and c27 Erniu's grin are written as face movements); the eye extreme close-ups use EYES; Tang
Xiaotang's costume is the portrait's (TANG: closed cross-collar jacket over a pleated skirt with a bow; no collar
sentence, which pilot.py refuses); the kitchen of scene 1 is e003's red-brick stove (KITCHEN, as e003 fix3 s38-s40);
no glow on a face outside the eye close-ups; the knife is A-ling's one KNIFE, as in e003.
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
    # 2026-11-07 independent review retakes: close-ups keep the set to one line (as e003-r2 fix3); the farmhouse room's
    # full shot names the crock by CROCK; the yard by day keeps its gate on the right.
    "kitchen_cu": "In the small earthen kitchen of the Xu farmhouse at night, lit only by the warm orange glow of the stove fire",
    # Live prep (2026-11-09): e003 live fix3 (cut review 二-9) settled the kitchen as the set picture and the chosen
    # e003 s33-s40 takes draw it: one red-brick stove, a black iron wok on top, the fire mouth at the front, split
    # firewood piled beside it. Scene 1 is the same kitchen the next instant, so every shot uses these two sentences.
    "kitchen_brick": "Inside the small earthen kitchen of the Xu farmhouse at night, one red-brick stove with a black iron wok on its top and its fire mouth at the front, split firewood stacked in a pile beside it, lit only by the warm orange glow of the stove fire",
    "kitchen_brick_door": "Inside the small earthen kitchen of the Xu farmhouse at night, the plank door on screen left with cold moonlight beyond it, one red-brick stove with a black iron wok on its top at the back right, its fire mouth glowing, split firewood piled beside it, lit by the warm orange glow of the stove fire",
    "kitchen_door_cu": "In the small earthen kitchen of the Xu farmhouse at night, at its plank doorway, cold moonlight outside and the warm orange glow of the stove fire from inside",
    "house_m": "Inside the poor thatched farmhouse of the Xu family on an autumn morning, earthen walls and a packed earth floor, the plank door on screen left, a big clay water vat by the back wall, a small clay stove on screen right, clear morning light slanting in from the door and window on the left",
    "house_cu": "Inside the poor thatched farmhouse of the Xu family on an autumn morning, clear morning light from the left",
    "yard_am_m": "In the dirt yard of the Xu farmhouse on a clear autumn morning, a bamboo fence, the house eaves along the back, a wooden table in the middle, the yard gate on screen right, warm morning sunlight from screen right",
    "yard_am_cu": "In the dirt yard of the Xu farmhouse on an autumn morning, warm morning sunlight from screen right",
    "yard_day_m": "In the dirt yard of the Xu farmhouse on a clear autumn day, a bamboo fence, a woodpile on screen left, the yard gate in the fence on screen right, bright slanting sunlight from screen right",
    "yard_day_cu": "In the dirt yard of the Xu farmhouse on an autumn day, bright slanting sunlight from screen right",
    "yard_night_cu": "In the dirt yard of the Xu farmhouse at night, at the cooking shelter, the house door on screen right about six paces from the stove, lit by the orange stove fire and cold moonlight",
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
# Live prep (2026-11-09): the owner's costume lock (2026-11-08) is the portrait's, written out as e003 fix3 s17 did; the
# CG phrase became "high-waisted ruqun" in pilot.py, and any collar sentence makes pilot.py stop.
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
VILL = "villagers in Song-dynasty cross-collared coarse cotton jackets and cloth head-wraps"
XU = "his blue-grey scholar's robe with both shoulders whole, his sleeves rolled up to the elbows"  # live: e003 fix3 二-14
# The one rolled red paper: always this phrase, never a flat sheet (2026-11-07 review, as e003-r2).
BELT = "the rolled red paper, rolled tight into a short plain blank tube, tucked into the left side of his belt"
ALING = "no shackles, her sleeves pulled down over her wrists"
KNIFE = "one short single-edged knife with a dull iron-grey blade about one and a half palms long and a plain wooden handle"  # e003's phrase
BOX = "one small wooden casket the size of a book, two palms wide and one palm deep, with a lid hinged at the back, in dark brown lacquer with one brass clasp, small enough to carry in one hand, plain, with no writing anywhere"  # same size in every shot (owner: the box grew and shrank)
GOLD = "five small yuanbao-shaped gold ingots, plain gold with no marks or writing"
WOK = "one big black iron wok about two and a half feet across with an ear handle on each side"
PIG = "one whole black-haired pig, dead and limp with its eyes closed, its four legs tied together with straw rope, no blood and no wound"
NIGHT = "red-eyed and tired"
# 2026-11-07 independent review: one phrase per prop in every shot it is in.
# The rice crock of s10-s11 (the review: s11 drew a different pot).
CROCK = "one squat brown clay rice crock as high as a small child's knee, with one round flat wooden lid"
# The stirring pole of s36-s37.
POLE = "one long plain wooden stirring pole taller than a man"
# The dark figure of s38 and s40: a grown man, never a child (the review: s40 drew a child).
FIGURE = "one thin grown man with narrow bony shoulders, in a grey-brown short jacket and an old cloth head-wrap, back-lit by the stove fire, his face in deep shadow"
# Live-action prep (2026-11-09), copied from e003-r2: a face that must not smile gets no smile word at all except this
# one ban (smile, smirk, grin, unsmiling, "no smile the whole shot" all came out as a smile in e901-e903 live).
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
# The eye extreme close-ups keep natural eyes ("a faint pale blue light in his pupils" drew glowing blue irises).
EYES = "his irises a natural dark brown from the first frame to the last, the whites of his eyes clear, only a tiny faint cold pale glint of reflected light in each pupil, like a catchlight"

SHOTS = [
    # ---- scene 1: the kitchen, the first night (the same instant as e003 c40), stove fire, cold moonlight at the door.
    # Axis: Xu Yan squatting on screen left facing right, A-ling on the stool before the fire mouth on the right; c08 she
    # walks to the door on the left, Xu Yan stays at the back right.
    # 2026-11-07 second review (review-picks.tsv): s01 s05 s09 s11 s19 s21 s23 s30 s32 s40 rewritten so the scripted
    # action is the shot's main event and its end state is written; framing wide enough to keep the face and the prop in.
    # Live prep (2026-11-09): the set is e003's red-brick stove (kitchen_brick); speakers locked, profile or three-quarter
    # toward the listener; faces part by part; NOSMILE.
    dict(chapter="灶房", loc="kitchen_brick", cam="Medium close-up, locked", chars=["xuyan"], night="kitchen_fire",
         comp=f"medium close-up framed from the chest up with space above his head, the shot opens directly on Xu Yan from its very first frame: Xu Yan squatting on screen left, {XU}, his body and face in three-quarter profile toward screen right, the camera about 45 degrees off his eyeline, never the lens; the glowing fire mouth of the red-brick stove low in the right foreground in front of him, one stick of firewood in his right hand with its far end resting in the fire mouth; the firelight on his face, grave: brows level and still, eyes lowered to the fire, jaw set, lips pressed firm between words",
         lines=[("xuyan", "阿令，人不是東西，不能拿來押，也不能拿來抵。", "一字一字")],
         motion=f"his right hand pushes the stick into the fire mouth until its end disappears into the flames and the flames flare up once; only then he lifts his eyes to A-ling off screen right and says the line to her slowly, his face still grave; {NOSMILE}",
         zh="近景、固定（胸口以上；2026-11-07 第二次獨立審片重寫）：許硯蹲在畫面左、面向右，灶口就在他面前右下、裡面有火，右手一根柴一端搭在灶口；他把柴往前推進灶口、柴頭沒進火裡，火往上竄一下，然後才抬眼往右看阿令；火光照臉；眉平、嘴抿緊、整鏡不笑。live prep 2026-11-09：慢推改固定、頭上留空，四分之三側臉朝畫右、鏡頭偏離視線約 45°、不看鏡頭；灶寫成第 3 集選定片段的紅磚灶（kitchen_brick）；拿掉 no smile 字樣、改 NOSMILE"),
    dict(loc="kitchen_brick", cam="Over-the-shoulder medium shot, locked", chars=["aling", "xuyan"], night="kitchen",
         comp=f"over-the-shoulder shot from behind Xu Yan's shoulder and his rolled-up sleeve in the left foreground, A-ling on screen right sitting on a low stool before the fire mouth of the red-brick stove, {ALING}, {KNIFE} lying across her knees with its edge turned outward, her right hand on its wooden handle, her face in three-quarter profile toward Xu Yan in the left foreground, eyes on him, never the lens; cold and wary: brows level and low, eyes narrowed, lips closed in a flat line, jaw still",
         lines=[("xitong", "叮。阿令好感 +3。", "冷淡，叮一聲")],
         panel=[("阿令 好感 +3 → -2", "panel")],
         motion=f"A-ling's right hand on the knife handle slowly loosens, her fingers leave the handle and settle flat on her knee, her eyes staying on him; all lips stay closed; {NOSMILE}",
         zh="過肩（許硯肩後拍阿令，他的主觀）、固定：阿令坐矮凳，短刀橫在膝上（刀刃朝外），袖子蓋住手腕；握刀柄的右手慢慢鬆開，手指放到膝上；不笑。live prep 2026-11-09：慢推改固定；阿令四分之三側臉朝前景的許硯、不看鏡頭；冷而提防：眉平壓低、眼睛瞇、嘴抿成一線、下巴不動；刀用第 3 集同一句 KNIFE；紅磚灶；NOSMILE"),
    dict(loc="kitchen_brick", cam="Medium close-up, locked", chars=["xuyan"], night="kitchen",
         comp="medium close-up of Xu Yan squatting on screen left, framed from the chest up with space above his head, his blue-grey scholar's robe with both shoulders whole, his sleeves rolled up, his body three-quarter toward screen right, his eyes on the empty air before his face, never the lens; first a flash of hope: brows jumping up, eyes widening; then his face falls: brows sinking and drawing together, eyes dropping, the corners of his mouth pulled down, lips closed; behind him only the split firewood pile of the same kitchen",
         lines=[("xuyan", "才漲到負二，說到底還是負的啊。", "心裡話，嘴閉著，一喜又垮", "inner"),
                ("xitong", "負的也是宿主自己說空話扣的。", "冷")],
         motion=f"he clenches one fist on his knee, then opens it again and his shoulders slump with a breath out; his lips stay closed the whole shot; {NOSMILE}",
         zh="中近景、固定（長鏡買 8 秒）：許硯先一喜、又垮下來，膝上握一下拳又鬆開，肩膀垮下來；心裡話，嘴閉著；系統冷冷回一句。live prep 2026-11-09：拿掉臉上的淡藍光與「不畫面板」（preflight glow：模型畫出發光面板與假字；第 3 集 s20 同樣拿掉），只留灶火；身體四分之三朝畫右、看面前空氣、不看鏡頭；一喜：眉毛一跳、眼睛睜大；垮：眉往下皺、垂眼、嘴角往下、嘴閉；慢推改固定；NOSMILE"),
    dict(loc="kitchen_brick", cam="Reverse medium close-up, locked", chars=["aling"], night="kitchen",
         comp=f"reverse medium close-up of A-ling on the low stool, framed from the chest up with space above her head, {ALING}, the short knife across her knees, her body and face three-quarter to screen left toward Xu Yan off screen left, the camera about 40 degrees off her eyeline, never the lens; suspicious: brows drawn together and low, eyes narrowed on his face, lips pressed flat between words; behind her only the red-brick stove and its glowing fire mouth of the same kitchen",
         lines=[("aling", "你臉上一下高興一下發苦，在想什麼？", "冷")],
         motion=f"she tilts her head, frowning at his face, and leans forward a little, eyes on him; {NOSMILE}",
         zh="近景反打、固定：阿令歪一下頭，皺眉看許硯臉上一下鬆一下垮，身子往前探一點；身後只有灶與火光；不笑。live prep 2026-11-09：慢推改固定中近景、頭上留空；四分之三側臉朝畫左的許硯、鏡頭偏離視線約 40°、不看鏡頭；狐疑：眉頭往中間往下皺、眼睛瞇著盯他的臉、字句之間嘴抿平；身後是紅磚灶；NOSMILE"),
    dict(loc="kitchen_brick", cam="Medium shot, locked", chars=["xuyan", "aling"], night="kitchen",
         comp=f"medium shot framed wide, with clear space above Xu Yan's head so his whole head stays in frame after he stands up: Xu Yan crouching on screen left before the glowing fire mouth of the red-brick stove, {XU}, in profile facing screen right toward A-ling, the camera about 60 degrees off his eyeline, never the lens, flustered: brows raised high, eyes darting away and back to her, a short embarrassed huff; A-ling at the right edge of the frame on the low stool, her sleeves pulled down over her wrists, in profile toward him, a cold flat stare: brows level, eyes narrowed, lips closed",
         lines=[("xuyan", "沒什麼，我是說……這灶火總算旺起來了。", "尷尬")],
         motion="Xu Yan hurries up from his crouch to stand facing A-ling in profile, his whole head inside the frame, brushes the hem of his robe with one hand, then points one finger at the fire mouth from an arm's length away, and he stays standing to the end of the shot; A-ling's lips stay closed",
         zh="中景、固定（2026-11-07 第二次獨立審片：景框留夠頭頂空間，站起來後整顆頭都在畫面裡）：許硯從蹲著趕緊站起來、臉朝阿令，一手拍拍衣擺，再站著用一根手指隔一臂遠指一指灶口，鏡尾站著；右邊緣阿令冷冷看著。live prep 2026-11-09：慢推改固定；許硯正側臉朝畫右的阿令、鏡頭偏離視線約 60°、不看鏡頭；尷尬（稿子可乾笑）只寫成臉怎麼動、不寫笑字：眉毛高揚、眼神閃開又回來、鼻子短短出一口氣；阿令側臉朝他、眉平眼瞇、嘴閉；紅磚灶"),
    dict(loc="kitchen_brick", cam="Medium shot, locked", chars=["aling", "xuyan"], night="kitchen",
         comp=f"medium shot past the glowing fire mouth of the red-brick stove in the foreground, framed with space above A-ling's head so her whole head stays inside the frame after she stands, A-ling on screen right, {ALING}, the short knife in her right hand, one dark brown leather sheath on the left side of her belt, in profile facing screen left toward Xu Yan, the camera about 50 degrees off her eyeline, never the lens, cold and flat: brows level, eyelids lowered, lips pressed thin between words, jaw still; Xu Yan standing at the left edge of the frame in profile facing her, his sleeves rolled up, brows drawn together, lips closed",
         lines=[("aling", "人不是東西，這話我聽過很多次，沒一個做到。", "冷")],
         motion=f"A-ling slides the knife into the sheath on her belt, rises and brushes the dust off her skirt, her eyes on Xu Yan; Xu Yan's lips stay closed; {NOSMILE}",
         zh="中景、固定、前景灶火：阿令把短刀插回腰帶左邊的深褐皮鞘，站起身，拍掉裙上的灰；許硯站在左邊緣。live prep 2026-11-09：慢推改固定、留頭頂空間（她站起來）；阿令正側臉朝畫左的許硯、鏡頭偏離視線約 50°、不看鏡頭；冷淡：眉平、眼皮垂、字句之間嘴抿薄、下巴不動；許硯側臉朝她、皺眉、嘴閉；紅磚灶；NOSMILE"),
    dict(loc="kitchen_brick", cam="Medium close-up, locked", chars=["xuyan"], night="kitchen",
         comp=f"reverse medium close-up of Xu Yan standing, framed from the chest up with space above his head, {XU}, {BELT}, his body and face three-quarter to screen right toward A-ling off screen right, the camera about 45 degrees off his eyeline, never the lens; earnest: brows drawn a little together, eyes steady on her and unblinking, jaw firm, lips pressing together between phrases; behind him only the split firewood pile and the earthen wall of the same kitchen",
         lines=[("xuyan", "那妳就看著。我要是做不到，妳那把刀還在。", "認真")],
         motion=f"he takes half a step forward toward her, eyes on her, and on 「刀還在」 lifts his chin once toward the sheath at her waist off screen right; {NOSMILE}",
         zh="反打中近景、固定：許硯往前半步看著她，朝她腰間的刀鞘抬一下下巴；認真：眉頭微收、眼神定定不眨、嘴抿緊。live prep 2026-11-09：中近景推到近景改成固定中近景、頭上留空（CG 草稿 4.4 秒起笑）；四分之三側臉朝畫右的阿令、鏡頭偏離視線約 45°、不看鏡頭；身後柴堆與土牆；NOSMILE"),
    dict(loc="kitchen_brick_door", cam="Full shot, tracking", chars=["aling", "xuyan"], nospeak=["xuyan"], night="kitchen",
         comp=f"full shot past the kitchen door frame in the foreground, A-ling at the doorway on screen left with her back to the room, {ALING}, the short knife in the dark brown leather sheath on the left of her belt; at the back right Xu Yan standing by the red-brick stove, a dark silhouette against the firelight, his face in shadow",
         lines=[("xuyan", "那妳也早點睡，刀別磨到天亮了。", "畫外，試探，遠一點")],
         motion="A-ling walks to the doorway with her back to Xu Yan, puts one hand on the door frame and stops there; all lips stay closed",
         zh="全景、跟拍（跟著阿令往左）、前景門框：阿令走到灶房門口，背對許硯，伸手扶住門框停一下；許硯在右後灶火邊、背光看不到嘴（台詞不對嘴）。live prep 2026-11-09：場景句換成同一間紅磚灶灶房（kitchen_brick_door：門在畫左、紅磚灶與黑鐵鍋在右後）"),
    dict(loc="kitchen_door_cu", cam="Medium close-up, locked", chars=["aling"], night="kitchen",
         comp=f"medium close-up from inside the kitchen, the camera directly behind A-ling looking out through the open plank door at the moonlit night; the shot opens directly on A-ling's head and shoulders from its very first frame: A-ling standing on the threshold with her back to the camera, {ALING}, the dark brown leather sheath at the left of her belt, her left hand on the door frame; beyond her, filling the doorway, only the dark night outside and bare ground silvered by cold moonlight; the warm firelight from the stove behind the camera on her shoulders",
         lines=[("aling", "刀收了。記住你說的，我會一直看著。", "很輕")],
         motion=f"she presses the sheath at her waist once and turns only her head over her right shoulder into clean profile facing screen right, toward Xu Yan at the stove behind her off screen right, never turning further toward the lens: brows level, eyes cool, lips pressed thin between words; then she steps over the threshold into the dark night and walks out of the frame on screen left, leaving the moonlit doorway empty; {NOSMILE}",
         zh="中近景、固定（2026-11-07 第二次獨立審片：鏡頭在灶房裡、在她身後，從敞開的門往外看月夜）：阿令站在門檻上背對鏡頭，門外是夜色與冷月光照的地面；手按一下腰間刀鞘，從右肩半回頭、側臉說話，然後跨出門檻走進夜裡、往畫面左出畫，鏡尾只剩月光照著的門口（結尾）。live prep 2026-11-09：慢推改固定、鏡頭在她正後方；只轉頭到正側臉朝畫右（許硯在她身後右邊灶旁），不再往鏡頭轉（CG 草稿 02 面向鏡頭、嘴角帶笑）；眉平、眼神冷、字句之間嘴抿薄；NOSMILE"),
    # ---- scene 2: the second morning, morning light from the door and window on the left. c10-c15 the farmhouse room
    # (door left, Xu Yan left, Xiaohe right by the rice crock); c16-c25 the same yard at the wooden table (Xu Yan sits at
    # its left, Xiaohe beside him, Tang Xiaotang stands on the right).
    dict(chapter="米與金子", loc="house_m", cam="Full shot, tracking", chars=["xiaohe", "xuyan"], night="house",
         comp=f"full shot past {CROCK} in the foreground in the back corner, little Xiaohe in her patched lilac short jacket with red-string pigtails, her straw rabbit tucked into her sash, squatting before the crock, one wooden ladle already in her right hand from the very first frame, aggrieved: her lower lip pushed out, her brows drawn up in the middle, her eyes wet; Xu Yan far off on screen left, {XU}, {BELT}, brows drawn together, lips closed",
         lines=[("xiaohe", "哥，米缸只剩一碗米了，煮完今天就沒了。", "委屈")],
         motion=f"Xiaohe lifts the crock's wooden lid with her left hand, scrapes the ladle round its bottom, then lifts her head and turns her face in three-quarter profile to Xu Yan on screen left, eyes on him; Xu Yan's lips stay closed; {NOSMILE}",
         zh="全景、跟拍（往後牆角）、前景米缸（CROCK：矮胖陶米缸、小孩膝蓋高、圓木蓋）：小禾第一格右手就拿著木勺，蹲在米缸前，左手掀開木蓋，木勺刮缸底，抬頭看左邊的許硯；委屈：下唇噘起、眉心往上皺、眼眶濕。live prep 2026-11-09：拿掉 no smile 字樣、改 NOSMILE；小禾說話時四分之三側臉朝畫左的許硯；許硯的臉也寫：皺眉、嘴閉"),
    dict(loc="house_cu", cam="Medium close-up, locked", chars=["xuyan"], night="house",
         comp=f"medium close-up of Xu Yan beside {CROCK}, framed from the chest up with space above his head, its wooden lid already off and leaning against its side, its open mouth at the bottom edge of the frame, {XU}, his body three-quarter to screen right toward little Xiaohe off screen right, the camera about 45 degrees off his eyeline, never the lens; steady: brows level, eyes calm, jaw relaxed, mouth set firm between words; her small hand in a patched lilac sleeve reaching in at the right edge of the frame holding out one wooden ladle, the rest of her off screen right; behind him only the earthen wall of the same farmhouse room",
         lines=[("xuyan", "一碗米也夠撐一天，今天先把做肥皂的東西湊齊。", "平穩")],
         motion=f"he crouches down by the crock, takes the ladle from the small hand in the lilac sleeve, looks down into the open crock and lowers the ladle into it, its handle left standing up out of the crock's mouth in view to the end of the shot, his face still steady; {NOSMILE}",
         zh="中近景、固定（2026-11-07 第二次獨立審片：米缸蓋已經掀開靠在缸邊）：右邊緣小禾的小手（淡紫袖子）把木勺遞進畫面；許硯蹲下，從她手裡接過木勺，低頭看進敞開的缸裡，把勺子放回缸裡，鏡尾勺柄從缸口露出來；身後只有屋內土牆。live prep 2026-11-09：近景慢推改固定中近景、頭上留空（CG 兩版全程笑）；四分之三側臉朝畫右的小禾、鏡頭偏離視線約 45°、不看鏡頭；平穩：眉平、眼神穩、下巴放鬆、字句之間嘴抿緊；NOSMILE"),
    dict(loc="house", cam="Extreme close-up, slow push in", chars=["xuyan"], night="house",
         comp=f"extreme close-up of Xu Yan's eyes only, the shot opens directly on his eyes from its very first frame and the frame never widens: his two eyes and brows fill the frame, {EYES}, his eyeline slightly to screen right, never into the lens; nothing else in the frame, one face only, no second figure, no double exposure",
         lines=[("xitong", "材料：豬油、草木灰、大鍋。", "冷淡")],
         panel=[("材料：豬油・草木灰・大鍋", "panel")],
         motion="his eyes flick up to the upper right and he blinks once, the frame holding only his eyes and brows to the last frame; his lips stay closed",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：眼睛往右上一轉，眨一下。live prep 2026-11-09：照第 3 集 s19 寫法：只有兩隻眼睛與眉毛、不拉遠，EYES（自然深褐虹膜），視線偏畫右、不看鏡頭，只有一張臉、沒有疊影（第 3 集 s25 有疊影）"),
    dict(loc="house_cu", cam="Insert close-up, slow push in", chars=["xuyan"], night="house", act=3,
         comp="insert close-up of the small clay stove, the shot opens directly on the small iron pot from its very first frame: one small black iron pot on the stove and Xu Yan's two hands in his rolled-up blue-grey cuffs gripping its rim; only the hands, cuffs and pot are in the frame, his face out of the frame; behind them only the bright window of the same farmhouse room",
         lines=[("xuyan", "大鍋？家裡這口鍋，連粥都快煮不了。", "心裡話，嘴閉著，發愁", "inner"),
                ("xitong", "宿主缺的不只是鍋。", "冷")],
         motion="his hands lift the small pot off the stove, turn it upside down and hold its bottom up before the bright window; only then one long crack across the bottom shines bright with window light coming through it, and he holds the pot there, the bright crack clearly in view to the end of the shot",
         zh="手部特寫、慢推（第一格就是小鐵鍋，長鏡買 8 秒）：許硯的兩手把小鐵鍋從灶上拿起來翻過來對著窗，然後鍋底一道長裂縫才透出亮亮的窗光，一直舉著、鏡尾裂縫清楚看得到（2026-11-07 獨立審片）；心裡話；系統冷冷一句"),
    # e904 live fix1 (2026-11-09, review-picks-a: both d1 seeds had her smiling through her line, near frontal, standing
    # inside beside him; "shrewd" and "eyes darting" drew a playful smile). Redesigned like e903 fix1 s18: a side two-shot,
    # the camera square to their eyelines, she leans in at the door frame on the left in profile, he looks at the pot.
    dict(loc="house_m", cam="Side two-shot medium, locked", chars=["tangxiaotang", "xuyan"], night="house",
         comp=f"side two-shot medium, the camera square to the line between them, both in profile, seen from the waist up and small in the frame with space above their heads: on screen left the plank door frame, Tang Xiaotang outside it leaning in round the frame so only her upper body shows, {TANG}, her gold abacus at her waist, in pure profile facing screen right toward Xu Yan, never the lens, brows knotted, eyes narrowed and calculating, mouth corners pulled down, lips pressed flat between words; on screen right Xu Yan in pure profile facing screen left, his sleeves rolled up, the small cracked iron pot held upside down in both hands, its crack upward, brows knotted, eyes down on the pot, lips closed; behind them only the bright window and the earthen wall of the same farmhouse room",
         lines=[("xuyan", "缺錢又缺人手，這我比誰都清楚。", "心裡話，嘴閉著", "inner"),
                ("tangxiaotang", "鍋裂了，米也見底，說到底就是缺錢。等著別走！", "說話快")],
         motion=f"for the first half Xu Yan turns the upside-down pot in his hands and looks at the crack, lips closed, and Tang Xiaotang leans in at the door frame and looks from the pot to him; in the second half she says her line to him fast, still in profile, then pulls back behind the door frame and is gone; Xu Yan keeps his eyes on the pot, lips closed; both stay in profile, neither faces the camera; {NOSMILE}",
         zh="側面雙人中景、固定（2026-11-09 真人版 fix1，review-picks-a：d1 兩支唐小棠整句都在笑、臉偏正面，1102 還直視鏡頭；兩支她都站進屋裡、沒有扶門框；「精明」「眼睛一轉」被演成俏皮的笑，全部拿掉）：照第 3 集 s18 的改法，鏡頭垂直兩人視線，兩人都是正側臉、腰以上、在畫面裡小小的；畫左是門框，唐小棠在門外只探出上半身、正側臉朝畫右；畫右許硯正側臉朝畫左、低頭看翻過來的裂鍋（裂縫朝上）。前半許硯轉著鍋看裂縫、嘴閉（心裡話），唐小棠看看鍋又看看他；後半她才快快說完台詞、縮回門外。表情：眉頭打結、眼睛瞇著盤算、嘴角往下、字句之間嘴抿平；兩人都不看鏡頭、從頭到最後一格都不笑（NOSMILE）。長度不變 12 秒，台詞不變"),
    dict(loc="house_m", cam="Full shot, locked", chars=["tangxiaotang", "xiaohe", "xuyan"], night="house",
         comp=f"full shot from inside the room past the wide-open plank door in the left foreground, everyone small in the frame: outside on the sunny bare ground Tang Xiaotang seen from behind, {TANG}, running toward the gate in the bamboo fence on the right; inside little Xiaohe at the doorway, her straw rabbit tucked into her sash, puzzled: her head tilted, brows raised, lips parted; Xu Yan on screen right by the small clay stove, his sleeves rolled up, the cracked pot in his hands, resigned: brows lifted in the middle, a small breath out",
         lines=[("xiaohe", "小棠姐姐跑那麼快，是要去哪裡？", "歪頭"),
                ("xuyan", "不知道。她叫我們等，那就在院子等一下。", "無奈")],
         motion=f"Tang Xiaotang runs out through the gate off screen right; Xiaohe runs to the doorway and turns back in three-quarter profile to Xu Yan; Xu Yan, in three-quarter profile toward her, sets the pot on the stove and shakes his head; {NOSMILE}",
         zh="全景、固定，從屋內往外拍、前景敞開的屋門（長鏡買 8 秒）：唐小棠背影提起裙擺跑出院門往右出畫；小禾追到門口回頭問；許硯把鍋放回灶上、搖搖頭回答。live prep 2026-11-09：慢推改固定、人都小小的；唐小棠只拍背影（TANG 照定妝照）；小禾歪頭、眉毛揚、嘴微張，回頭時四分之三側臉朝許硯；許硯無奈：眉心往上、輕輕出一口氣，四分之三側臉朝她；NOSMILE"),
    dict(loc="yard_am_m", cam="Full shot, locked", chars=["tangxiaotang", "xuyan", "xiaohe"], night="yard_am",
         comp=f"full shot past the wooden table in the foreground, everyone small in the frame: Xu Yan sitting at the left end of the table, his sleeves rolled up, brows raised, lips closed, and little Xiaohe standing beside him, eyes wide; Tang Xiaotang, {TANG}, hurrying in from the yard gate on screen right in profile facing screen left toward Xu Yan, never the lens, carrying {BOX} in both hands, brisk and shrewd: chin up, eyes sharp on him, lips pressed between words",
         lines=[("tangxiaotang", "許硯，二十兩是吧？你看看這些夠不夠。", "精明")],
         motion=f"Tang Xiaotang reaches the table, sets the casket down on the tabletop with a thump, catches her breath and says the line to Xu Yan in profile, the casket standing on the table to the end of the shot; the others' lips stay closed; {NOSMILE}",
         zh="全景、固定、前景木桌：許硯坐木桌左邊、小禾站他旁邊；唐小棠從右邊院門快步走回來，兩手抱小木匣，往桌上一放，然後才喘一口氣，鏡尾木匣在桌上；精明：下巴抬、眼神利。live prep 2026-11-09：慢推改固定、人都小小的；服裝照定妝照（TANG），拿掉「立領每一格都扣到喉嚨」（pilot.py 會擋）；她側臉朝畫左的許硯、不看鏡頭（CG 草稿帶笑說話）；許硯眉毛揚、嘴閉，小禾眼睛睜大；NOSMILE"),
    dict(loc="yard_am_cu", cam="Insert close-up, slow push in", chars=["tangxiaotang"], night="yard_am", act=3,
         comp=f"insert close-up, the shot opens directly on the brass clasp of the casket on the wooden table from its very first frame: {BOX}, its lid shut, and Tang Xiaotang's right hand in her peach-pink brocade cuff resting on the clasp; only the one hand, the cuff and the casket are in the frame, no face and no body in the frame the whole shot; behind it only the out-of-focus tabletop of the same yard",
         lines=[],
         motion=f"her fingers flick the brass clasp open and lift the lid back on its hinge; only then, inside, {GOLD}, catch the sunlight and gleam",
         zh="手部特寫、慢推（第一格就是木匣的銅扣，整鏡只有手與木匣、沒有臉，2026-11-07 獨立審片）：唐小棠的手指（桃粉織錦袖口）撥開銅扣、掀開匣蓋，然後裡面五錠元寶形小金錠才在日光下一亮；沒有字"),
    dict(loc="yard_am_cu", cam="Medium close-up, locked", chars=["xiaohe"], night="yard_am",
         comp="medium close-up of little Xiaohe framed from the chest up with space above her head, red-string pigtails and one front tooth missing, her patched lilac jacket, her small straw rabbit tucked into her sash, her face three-quarter to screen left toward Xu Yan off screen left, the camera about 40 degrees off her eyeline, never the lens; overjoyed: eyes wide and shining, brows high, mouth open wide in delight, her cheeks lifting; behind her only the bamboo fence of the same yard",
         lines=[("xiaohe", "好多金子！哥，我們有錢還債了！", "驚呼")],
         motion="she rises on tiptoe, grips the table edge with both hands and peers into the casket below the frame, then turns her bright face to Xu Yan off screen left and says the line to him, bouncing once on her toes",
         zh="中近景、固定：小禾踮腳趴到桌邊，兩手扒著桌沿往匣裡看，眼睛睜大，開心（稿子可以笑）；身後只有院子籬笆。live prep 2026-11-09：近景慢推改固定中近景、頭上留空；四分之三側臉朝畫左的許硯、鏡頭偏離視線約 40°、不看鏡頭；開心只寫成臉怎麼動、不寫笑字：眼睛睜大發亮、眉毛高揚、嘴張大、臉頰往上"),
    # e904 live fix1 (2026-11-09, review-picks-a: both d1 seeds said the whole line with a sweet smile, uncuttable; 1101 had
    # seven or eight ingots; "offhand" drew the smile). Redesigned as a side two-shot across the table, both in profile.
    dict(loc="yard_am_cu", cam="Side two-shot medium, locked", chars=["tangxiaotang", "xuyan"], night="yard_am",
         comp=f"side two-shot medium across the wooden table, the camera square to the table at table height, both in profile, seen from the waist up and small in the frame with space above their heads: Xu Yan sitting on screen left in pure profile facing screen right, his sleeves rolled up, brows drawn down, lips closed; Tang Xiaotang on screen right leaning over the table in pure profile facing screen left toward him, {TANG}, never the lens, one eyebrow raised, eyelids half lowered, chin lifted, mouth corners level and pressed flat between words, bored and indifferent; between them on the tabletop {BOX}, lid open, exactly five small yuanbao-shaped gold ingots inside, plain gold with no marks or writing; behind them only the bamboo fence of the same sunny yard",
         lines=[("tangxiaotang", "這點不過是零頭，拿去還，省得錢員外再上門。", "輕描淡寫")],
         motion=f"she pushes the open casket across the tabletop with both hands until it stops in front of Xu Yan, says the line to him in profile, then draws her hands back, lifts her chin once and holds still; Xu Yan looks at the casket, lips closed; both stay in profile, neither faces the camera; exactly five ingots in the casket to the end of the shot; {NOSMILE}",
         zh="側面雙人中景、固定（2026-11-09 真人版 fix1，review-picks-a：d1 兩支她整句都甜甜地笑著講、裁不掉；1101 匣裡七八錠金子，接不上 s17 的五錠；「offhand」被演成笑，拿掉）：鏡頭垂直桌子、桌面高度，許硯坐畫左正側臉朝畫右，唐小棠在畫右俯身、正側臉朝畫左，兩人腰以上、在畫面裡小小的；不拍她四分之三的臉。木匣開著、裡面剛好五錠元寶形小金錠。她兩手把木匣推到許硯面前、說完台詞、把手收回、下巴抬一下就停住。表情：一邊眉毛挑、眼皮半垂、下巴抬、嘴角平、字句之間嘴抿平，冷淡無聊；兩人都不看鏡頭、從頭到最後一格都不笑（NOSMILE）。台詞不變"),
    dict(loc="yard_am", cam="Insert close-up, slow push in", chars=["xuyan"], nospeak=["xuyan"], night="yard_am", act=3,
         comp="insert close-up of the small wooden casket on the wooden table, the shot opens directly on Xu Yan's hand on the casket lid from its very first frame: his right hand in his rolled-up blue-grey cuff resting on the half-open dark brown lacquered lid, the brass clasp, the gold ingots glinting inside; only the hand, cuff and casket are in the frame, no face and no mouth; behind it only the out-of-focus tabletop of the same yard",
         lines=[("xuyan", "這是妳的退路，我不能拿。", "畫外，溫和")],
         motion="his hand slowly closes the lid, snaps the brass clasp shut, then pushes the casket back across the table toward screen right",
         zh="手部特寫、慢推（第一格就是許硯的手按在木匣蓋上）：許硯的手（藍灰袖口捲著）把匣蓋慢慢蓋上，扣好銅扣，推回唐小棠面前；畫面上沒有嘴"),
    dict(loc="yard_am_cu", cam="Reverse medium close-up, locked", chars=["tangxiaotang"], night="yard_am",
         comp=f"reverse medium close-up of Tang Xiaotang across the wooden table, her whole face in the upper part of the frame from her hair buns down to her collar, {TANG}, her face three-quarter to screen left toward Xu Yan off screen left, the camera about 40 degrees off her eyeline, never the lens; frozen in disbelief: eyes wide, brows raised and drawn together, lips parted, the corners of her mouth level; both her hands resting on {BOX}, the casket at the bottom edge of the frame, its lid closed; behind her only the bamboo fence and the autumn tree of the same yard",
         lines=[("tangxiaotang", "你不要？二十兩壓在你身上，你還跟金子客氣？", "愣住")],
         motion=f"she stays frozen, both hands resting on the closed casket the whole shot, and leans forward a little over the table, looking hard at Xu Yan off screen left, her face staying stunned; {NOSMILE}",
         zh="反打中近景、固定（2026-11-07 第二次獨立審片：臉從髮髻到領口整張在畫面上半，兩手按著闔上的木匣在畫面下緣）：唐小棠整鏡愣住，兩手一直放在闔上的木匣上，身子往前傾一點，定定看著左邊的許硯；身後只有籬笆與秋樹；愣住：眼睛睜大、眉毛上挑又皺在一起、嘴微張、嘴角平。live prep 2026-11-09：慢推改固定（CG 兩版後半都咧嘴大笑）；四分之三側臉朝畫左、鏡頭偏離視線約 40°、不看鏡頭；服裝照定妝照（TANG），拿掉立領句；NOSMILE"),
    dict(loc="yard_am_cu", cam="Medium close-up, locked", chars=["xuyan"], night="yard_am",
         comp=f"medium close-up of Xu Yan sitting at the wooden table, framed from the chest up with space above his head, {XU}, {BELT}, his body and face three-quarter to screen right toward Tang Xiaotang off screen right, the camera about 45 degrees off his eyeline, never the lens; earnest: brows drawn a little together, eyes steady on her, jaw firm, lips pressing together between phrases; behind him only the bamboo fence and the autumn tree of the same yard",
         lines=[("xuyan", "妳說過在躲一個人。真到要跑那天，妳得有盤纏。", "認真")],
         motion=f"he draws his hand back from the casket, sits up straight and looks at her, eyes on her the whole line; {NOSMILE}",
         zh="中近景、固定：許硯把手從木匣上收回來，身子往後坐直，看著她；背景籬笆與秋樹；認真：眉頭微收、眼神定、字句之間嘴抿緊。live prep 2026-11-09：中近景推到近景改成固定中近景、頭上留空（CG 選的那支全程嘴角帶笑）；四分之三側臉朝畫右的唐小棠、鏡頭偏離視線約 45°、不看鏡頭；NOSMILE"),
    dict(loc="yard_am_cu", cam="Medium close-up, locked", chars=["tangxiaotang"], night="yard_am",
         comp=f"medium close-up of Tang Xiaotang across the wooden table, her whole face in the upper part of the frame from her hair buns down to her collar, {TANG}, her face three-quarter to screen left toward Xu Yan off screen left, never the lens; quietly moved: eyes glistening, brows drawn softly together, lips closed in a straight line, the corners of her mouth level, her throat moving once as she swallows; both her hands on the lid of {BOX}, the casket standing on the tabletop at the bottom edge of the frame, its lid closed; behind her only the bamboo fence of the same yard",
         lines=[("xuyan", "債是我欠的，我自己賺。後天日落前，夠了。", "畫外，認真")],
         motion=f"she slowly lowers her head, her face staying in frame and her lips staying closed, while her fingers tighten on the casket lid under her hands; {NOSMILE}",
         zh="中近景、固定（2026-11-07 第二次獨立審片：臉從髮髻到領口在畫面上半，兩手按著闔上的木匣在畫面下緣）：唐小棠慢慢低下頭（臉一直在畫面裡），按在匣蓋上的手指收緊；嘴閉著；動容：眼眶發亮、眉頭輕皺、嘴閉成一直線、嘴角平；許硯畫外。live prep 2026-11-09：慢推改固定（CG 兩版都在笑）；四分之三側臉朝畫左、不看鏡頭；加一下吞嚥；服裝照定妝照（TANG），拿掉立領句；NOSMILE"),
    dict(loc="yard_am", cam="Extreme close-up, slow push in", chars=["xuyan"], night="yard_am",
         comp=f"extreme close-up of Xu Yan's eyes only, the shot opens directly on his eyes from its very first frame and the frame never widens: his two eyes and brows fill the frame, {EYES}, his eyeline slightly down to screen right, never into the lens; nothing else in the frame, one face only, no second figure, no double exposure",
         lines=[("xitong", "叮。唐小棠好感 +10。", "冷淡，叮一聲")],
         panel=[("唐小棠 好感 +10 → 10", "panel")],
         motion="his eyes blink once and his gaze settles down and to the right on the bowed head off screen, the frame holding only his eyes and brows to the last frame; his lips stay closed",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：眨一下，視線落在低著頭的唐小棠身上。live prep 2026-11-09：照第 3 集 s19 寫法：只有兩隻眼睛與眉毛、不拉遠，EYES，視線偏右下、不看鏡頭，只有一張臉、沒有疊影"),
    dict(loc="yard_am", cam="Medium shot, tracking", chars=["tangxiaotang", "xuyan", "xiaohe"], night="yard_am",
         comp=f"medium shot, everyone small in the frame: Tang Xiaotang on screen right, {TANG}, {BOX}, its lid closed, held easily against her side in one arm, no bigger than a book, teasing: one brow raised, eyes bright on Xu Yan, the corners of her mouth lifting a little; Xu Yan and little Xiaohe on screen left at the left end of the wooden table, watching her, lips closed; the house eaves on screen right",
         lines=[("tangxiaotang", "那我先記在帳上。後天日落賺不到，我可要笑你。", "帶一點笑")],
         motion="Tang Xiaotang turns with the casket, walks two steps right, looks back left over her shoulder at Xu Yan in three-quarter profile and says the line to him, then walks on under the house eaves and out of the frame on screen right; the shot ends with her gone; the others' lips stay closed",
         zh="中景、跟拍（跟著唐小棠往右）：唐小棠抱起木匣轉身往右邊屋簷下走兩步，停下回頭往左看許硯，說完沿屋簷下往右出畫，鏡尾她已不在畫面裡（2026-11-07 獨立審片）；許硯、小禾在左（結尾）。live prep 2026-11-09：稿子允許的一點笑只寫成臉怎麼動（一邊眉毛挑、眼睛亮亮看許硯、嘴角稍稍上揚），不寫笑字（CG 選的那支露齒笑）；回頭時四分之三側臉朝許硯；服裝照定妝照（TANG），拿掉立領句；人在畫面裡小小的"),
    # ---- scene 3: the same yard by day, late morning to afternoon, slanting light from the right. Axis: Xu Yan on the left
    # facing right; everyone from the gate comes in from the right. Never crosses the line.
    dict(chapter="湊材料", loc="yard_day", cam="Full shot, tracking", chars=["xuyan"], night="yard_day",
         comp=f"full shot past the bamboo fence in the foreground: on screen right three village women in Song-dynasty cross-collared coarse cotton short jackets, cloth head-wraps and cloth shoes, seen side-on or from behind, their faces never shown, each carrying one bamboo basket of grey-white plant ash; on screen left Xu Yan, {XU}, beside one wooden bucket, in profile facing screen right toward the women, never the lens, sincere: brows lifted in the middle, eyes warm on them, a small bow of his head",
         lines=[("xuyan", "多謝各位嬸子，有了這些草木灰，肥皂就成了一半。", "誠懇")],
         motion=f"the women tip the grey-white ash from their baskets into the bucket in a small puff; Xu Yan bends and hands the empty baskets back, says the line to them in profile; the women's lips stay closed; {NOSMILE}",
         zh="全景、跟拍、前景籬笆：右邊三個嬸子（側身、不拍正臉，宋式交領短打、布包頭）把竹籃裡的草木灰倒進許家的木桶，灰揚起一點；許硯彎腰接過空籃子遞還。live prep 2026-11-09：許硯側臉朝畫右的嬸子、不看鏡頭；誠懇：眉心往上、眼神溫和、輕輕點頭；NOSMILE"),
    dict(loc="yard_day_m", cam="Full shot, locked", chars=["erniu", "xuyan"], night="yard_day",
         comp=f"full shot past the yard gate in the foreground, both small in the frame: Wang Erniu standing just outside the gate in his coarse brown short jacket with rolled sleeves, {WOK} upside down on his back, held only by the fingers of both hands hooked over its rim at his shoulders, the wok the one thing he carries, his face three-quarter to screen left toward Xu Yan, never the lens, proud and loud: his mouth open wide showing his teeth, cheeks bunched up, eyes crinkled; Xu Yan inside the yard on screen left, {XU}, watching him, brows raised, lips closed",
         lines=[("erniu", "秀才！大鍋來了，我跟村頭打鐵的借來的！", "大嗓門")],
         motion="Erniu starts outside the gate and steps in sideways; only then the wok's rim bangs on the gate frame with a clang, and he twists sideways through into the yard, calling the line to Xu Yan; Xu Yan's lips stay closed",
         zh="全景、固定、前景院門（2026-11-07 獨立審片：沒有扁擔、沒有棍子）：二牛先在院門外，背上倒扣大黑鐵鍋、兩手手指從肩上勾住鍋沿，側身擠進來，然後鍋邊才「噹」地撞上門框，歪身子硬擠進院子；許硯在左。live prep 2026-11-09：慢推改固定、兩人小小的；稿子可以咧嘴，只寫成臉怎麼動（嘴張大露牙、臉頰擠起、眼角瞇），不寫笑字；二牛四分之三側臉朝畫左的許硯、不看鏡頭（CG 選的那支先面向鏡頭）；許硯眉毛揚、嘴閉"),
    dict(loc="yard_day", cam="Two-shot, locked", chars=["xuyan", "erniu"], night="yard_day",
         comp=f"two-shot, both seen from the waist up with space above their heads, Xu Yan on screen left, {XU}, {BELT}, in profile facing screen right toward Erniu, never the lens, grateful: brows lifted in the middle, eyes warm on him, lips pressing together between words; Wang Erniu on screen right turned three-quarters toward Xu Yan, his face clearly in view, puffing and proud: chest heaving, chin up, eyes bright, mouth closed, {WOK} upside down on his back, held by his fingers hooked over its rim",
         lines=[("xuyan", "二牛，好兄弟，這口鍋的情我記下了。", "感激")],
         motion=f"Erniu swings the wok off his back and sets it down on the ground with a thud, Xu Yan steadying its rim; only then Xu Yan pats Erniu's shoulder and says the line to him; Erniu's lips stay closed, his face in full view; {NOSMILE}",
         zh="雙人鏡、固定（2026-11-07 獨立審片：看得到二牛的臉）：二牛把大鍋從背上卸下來「咚」一聲放到地上，許硯扶著鍋沿；然後許硯拍二牛的肩膀。live prep 2026-11-09：跟拍改固定、兩人腰以上、頭上留空；許硯正側臉朝畫右的二牛、不看鏡頭；感激：眉心往上、眼神溫和、字句之間嘴抿（CG 選的那支許硯全程笑）；二牛四分之三朝許硯（不再朝鏡頭）、喘氣、下巴抬、眼睛亮、嘴閉；NOSMILE"),
    dict(loc="yard_day", cam="Medium shot, locked", chars=["erniu"], night="yard_day",
         comp=f"medium shot of Wang Erniu framed from the waist up with space above his head, both hands empty, sweat beading on his forehead, his face three-quarter to screen left toward Xu Yan off screen left, the camera about 45 degrees off his eyeline, never the lens; sulking: brows pulled down, lower lip pushed out, eyes sliding to the fence and back; behind him the bamboo fence with about five {VILL} showing only their upper bodies, soft and out of focus, pointing and whispering",
         lines=[("erniu", "可外頭的人都在笑，說你連熬油的豬都沒有。", "不服氣，小聲")],
         motion=f"he wipes the sweat off with the back of his hand, ducks his head low, glances at the fence and leans in toward Xu Yan off screen left, saying the line low to him; {NOSMILE}",
         zh="中景、固定：二牛（兩手空空、滿頭汗）用手背擦汗，壓低身子往籬笆外瞄一眼，湊近許硯；背景籬笆外村民指指點點（虛焦）。live prep 2026-11-09：慢推改固定、腰以上、頭上留空；四分之三側臉朝畫左的許硯、鏡頭偏離視線約 45°、不看鏡頭；不服氣：眉往下壓、下唇噘、眼睛往籬笆瞄又回來；NOSMILE"),
    dict(loc="yard_day_cu", cam="Medium close-up, locked", chars=["xuyan"], night="yard_day",
         comp=f"reverse medium close-up of Xu Yan from the chest up with space above his head, {XU}, {BELT}, {WOK} standing empty on the ground in front of him, its rim running across the bottom edge of the frame, his body three-quarter to screen right toward Erniu off screen right, the camera about 45 degrees off his eyeline, never the lens; composed: brows level, eyes lowered to the wok and then lifting to Erniu on the line, mouth set firm between words, jaw calm; his face stays in the upper part of the frame the whole shot; behind him only the woodpile of the same yard",
         lines=[("xuyan", "他們說得沒錯，豬油是最難湊的那一樣。", "沉著")],
         motion=f"he looks down at the empty wok and reaches out with his right hand to touch its cold rim once, then lifts his eyes to Erniu off screen right for the line, his face staying in frame and composed; {NOSMILE}",
         zh="中近景反打、固定（2026-11-07 第二次獨立審片：胸口以上、空鍋的鍋沿橫在畫面下緣，臉整鏡在畫面上半）：許硯低頭看那口空鍋，伸右手摸一下冰冷的鍋沿；身後只有柴堆。live prep 2026-11-09：慢推改固定；四分之三側臉朝畫右的二牛、鏡頭偏離視線約 45°、不看鏡頭，先看鍋、說話時抬眼看二牛；沉著：眉平、字句之間嘴抿緊、下巴放鬆（CG 01 最後笑）；NOSMILE"),
    dict(loc="yard_day", cam="Low-angle full shot, slow push in", chars=["qinshuang"], night="yard_day", act=4,
         comp=f"low-angle full shot past the shoulders and cloth head-wraps of {VILL} outside the fence in the foreground, Qin Shuang at the yard gate in her dark brown cross-collared short jacket, wide leather belt with her old chopping knife in its right side, black trousers and leather boots, carrying on her right shoulder {PIG}, her right hand gripping the straw rope, her face set: brows level and low, eyes fixed ahead on the yard, lips pressed in a flat line, jaw firm",
         lines=[],
         motion=f"the villagers at the fence gasp and shrink aside, and Qin Shuang strides in through the gate with the pig on her shoulder, every step landing heavy; all lips stay closed; {NOSMILE}",
         zh="低角度全景、慢推、前景籬笆外村民的肩膀（布包頭）：村民驚呼往兩邊讓開，秦霜右肩扛一整頭黑毛死豬（閉眼、四腳草繩綁著、不見血）大步走進院門，每一步都很重。live prep 2026-11-09：秦霜的臉逐部位寫：眉平壓低、眼睛直盯院子、嘴抿成一線、下巴收緊；NOSMILE"),
    dict(loc="yard_day_m", cam="Medium full shot, locked", chars=["qinshuang", "xuyan", "erniu"], night="yard_day",
         comp=f"medium full shot framed from the heads down to the feet with space above their heads, the bare dirt ground at Qin Shuang's feet across the bottom of the frame, Qin Shuang in the middle, her old chopping knife tucked in the right side of her belt, carrying on her right shoulder {PIG}, her face three-quarter to screen left toward Xu Yan, never the lens, brisk and bold: chin up, eyes level on him, lips pressed between words; Xu Yan on screen left, {XU}, staring: mouth fallen open, eyes wide, brows shot up; Wang Erniu at the back right, both hands empty, eyes wide, lips closed",
         lines=[("qinshuang", "豬油要多少？這一頭夠不夠你熬？", "爽快")],
         motion=f"Qin Shuang bends her knees and lowers the pig off her right shoulder onto the ground at her feet, a puff of dust rising; the pig stays lying there in plain view at the bottom of the frame while she straightens up, brushes her two empty hands together and says the line to Xu Yan; the others' lips stay closed; {NOSMILE}",
         zh="中全景、固定（2026-11-07 第二次獨立審片：拍到腳，地面在畫面下緣，豬放下後一直留在畫面裡）：中秦霜屈膝，把豬從右肩卸到腳邊地上，塵土揚起；豬閉著眼、四腳綁著草繩，一直躺在畫面下緣；她直起身，兩手空空互拍掉灰，柴刀一直插在腰帶右邊；左許硯、右後二牛。live prep 2026-11-09：慢推改固定；秦霜四分之三側臉朝畫左的許硯、不看鏡頭；爽快：下巴抬、眼神平平看他、字句之間嘴抿；許硯傻眼：嘴張開、眼睛睜大、眉毛挑高；二牛眼睛睜大、嘴閉；NOSMILE"),
    dict(loc="yard_day_cu", cam="Medium close-up, locked", chars=["xuyan"], night="yard_day",
         comp=f"medium close-up of Xu Yan from the chest up with space above his head, {XU}, his body three-quarter to screen right toward Qin Shuang off screen right, the camera about 45 degrees off his eyeline, never the lens; dumbfounded: mouth hanging open between words, eyes wide, brows shot up; the frame holds only Xu Yan and, behind him, the woodpile of the same yard",
         lines=[("xuyan", "妳一個人，從哪裡扛回來的？", "傻眼")],
         motion=f"he takes half a step back, his eyes going down to the black pig on the ground below the frame and up to Qin Shuang off screen right, and he points one finger down at the pig below the frame; {NOSMILE}",
         zh="中近景、固定（2026-11-07 獨立審片：前景沒有任何粉色的東西）：許硯往後退半步，看看畫外地上的黑豬又看看她，手指往下指豬；身後只有柴堆；傻眼：嘴張開、眼睛睜大、眉毛挑高。live prep 2026-11-09：近景慢推改固定中近景、頭上留空；四分之三側臉朝畫右的秦霜、鏡頭偏離視線約 45°、不看鏡頭；NOSMILE"),
    dict(loc="yard_day_cu", cam="Reverse medium close-up, locked", chars=["qinshuang"], night="yard_day",
         comp="reverse medium close-up of Qin Shuang framed from the chest up with space above her head, her belt below the frame, in her dark brown cross-collared short jacket, a few black pig bristles on the cloth of her right shoulder, her face three-quarter to screen left toward Xu Yan off screen left, the camera about 40 degrees off her eyeline, never the lens; scornful: one corner of her mouth pulled down, eyes narrowed, chin up, a short snort through her nose; behind her only the yard gate of the same yard",
         lines=[("qinshuang", "別問。你要是熬不出東西，下次扛的就是你。", "嗤一聲")],
         motion=f"she snorts, brushes the bristles off her shoulder with one hand and says the line to Xu Yan off screen left, eyes on him; only then she turns and walks out of the frame on screen left; {NOSMILE}",
         zh="中近景反打、固定：秦霜（衣服肩上沾幾根黑豬毛）嗤一聲，拍掉豬毛，看著畫左的許硯說話，然後才轉身往左出畫；身後只有院門；不屑：一邊嘴角往下、眯眼、下巴抬。live prep 2026-11-09：近景慢推改固定中近景、頭上留空、腰帶在畫面下緣外（不寫柴刀，免得刀跑到手上或肩後：CG 02 肩後多一把大刀）；四分之三側臉朝畫左、鏡頭偏離視線約 40°、不看鏡頭；拿掉「回頭說話」（先說完再轉身出畫）；NOSMILE"),
    dict(loc="yard_day", cam="Two-shot, locked", chars=["xuyan", "erniu"], night="yard_day",
         comp="two-shot, both small in the frame with space above their heads, Xu Yan on screen left, his blue-grey scholar's robe with both shoulders whole, his sleeves rolled up, in profile facing screen right toward Erniu, never the lens, decided: brows level, eyes firm on him, jaw set; Wang Erniu on screen right, both hands empty, in three-quarter profile toward Xu Yan, eager: eyes wide, lips closed; in the foreground on the ground the whole black pig, the big black iron wok and one wooden bucket of grey-white plant ash",
         lines=[("xuyan", "夠了。豬油、灶灰、大鍋都齊了，今晚就開鍋熬。", "定下來")],
         motion=f"Xu Yan looks over the pig, the wok and the ash, pushes his sleeves higher, slaps the wok rim with a clang and says the line to Erniu; Erniu nods, lips closed; {NOSMILE}",
         zh="雙人鏡、固定：前景地上的豬、大鍋、一桶草木灰；許硯看看豬、大鍋和那桶灰，把袖子再捲高，拍一下鍋沿「噹」；二牛跟著點頭（結尾）。live prep 2026-11-09：慢推改固定、兩人小小的；許硯正側臉朝畫右的二牛、不看鏡頭；定下來：眉平、眼神堅定、下巴收；二牛四分之三朝許硯、眼睛睜大、嘴閉；NOSMILE"),
    # ---- transition: the second night at the cooking shelter on the east side of the yard (as e005 opens): post left,
    # stove and wok in the middle, house door right, gate and fence at the back left; firelight and cold moonlight.
    dict(chapter="夜裡", loc="yard_night", cam="Full shot, locked", chars=["xuyan", "erniu"], night="yard_night",
         comp=f"full shot past the stove fire in the foreground, both small in the frame: Xu Yan in the middle standing at the big wok, {XU}, {NIGHT}, both hands on {POLE}, his eyes heavy on the wok, lips closed; Wang Erniu squatting before the fire mouth of the stove, his face three-quarter up toward Xu Yan, never the lens, puzzled: brows knitted, head tilted, lips pressing between words",
         lines=[("erniu", "秀才，這鍋豬油加灶灰，真能洗衣服？", "憨，懷疑")],
         motion=f"Xu Yan stirs round and round; Erniu pushes one broken twig into the fire mouth, sparks fly up, and he looks up at Xu Yan and says the line to him; Xu Yan's lips stay closed; {NOSMILE}",
         zh="全景、固定、前景灶火：許硯（累、眼睛發紅）兩手握長木棍一圈一圈攪鍋；二牛往灶口推一根碎枝，火星往上竄，抬頭看許硯（皺眉、歪頭）；灶邊地上只剩幾根碎枝、沒有柴堆（2026-11-07 獨立審片）；大鍋冒白氣。live prep 2026-11-09：慢推改固定、兩人小小的；二牛說話時四分之三側臉往上朝許硯、不看鏡頭；許硯眼皮重、看鍋、嘴閉；NOSMILE"),
    dict(loc="yard_night", cam="Medium shot, tracking", chars=["xuyan", "erniu"], night="yard_night",
         comp=f"medium shot framed with space above their heads, Xu Yan at the big wok in the middle, {XU}, {NIGHT}, his face three-quarter to screen left toward Erniu, never the lens, tired but sure: heavy eyelids, eyes steady on Erniu, mouth set between words, both hands on {POLE}; at the left edge Wang Erniu getting up before the fire mouth, his eyes drooping, lips closed",
         lines=[("xuyan", "能。等天亮開了模你就知道。柴燒完了，我進屋搬。", "累，但有把握")],
         motion=f"Xu Yan says the line to Erniu, glances at the few twigs, leans the pole against the wok's rim and walks off right toward the house door, seen from behind; Erniu yawns and walks out of the yard gate at the back left, lips closed; the pole stays leaning on the rim; {NOSMILE}",
         zh="中景、跟拍（跟著許硯往右，長鏡買 8 秒；2026-11-07 獨立審片：近景拍不到院門，改中景）：許硯看一眼灶邊只剩的幾根碎枝，說完把木棍斜靠在鍋沿，背對鏡頭往右邊屋門走；二牛站起來打呵欠，往左後院門走出去（回家睡）；鏡尾：木棍靠在鍋沿、許硯背影在右邊屋門、二牛走出院門。live prep 2026-11-09：許硯不再邊說邊打呵欠（嘴要對台詞），只有二牛打呵欠；許硯說話時四分之三側臉朝畫左的二牛、不看鏡頭（CG 01 開頭在笑）；累但有把握：眼皮重、眼神穩、字句之間嘴抿；頭上留空；NOSMILE"),
    dict(loc="yard_night", cam="Point-of-view full shot, slow push in", chars=[], night="yard_night", act=4,
         comp=f"point-of-view full shot through the narrow gap of the half-open house door, the dark door frame and a bundle of firewood edging the foreground: beyond the gap, about six paces away, the steaming big wok left unattended on the stove, one low wooden stool beside it, and, clearly visible in the middle of the gap, {FIGURE}, one wooden bucket full of water in both hands",
         lines=[],
         motion="the dark figure creeps out of the shadow of the fence at the back left to the wok, steps up onto the stool and lifts the bucket with both hands over the mouth of the wok, his face staying a dark shadow with the fire behind him; no one speaks",
         zh="主觀（許硯在屋門內抱一捆柴，從門縫往外看）、慢推、前景門框：門縫外一個黑影（瘦的成年男人、灰褐短褐、舊布頭巾、背光、臉在暗處）從左後籬笆陰影摸到鍋邊，一腳踩上板凳，兩手把水桶舉到鍋口上方。live prep 2026-11-09：動作句加「臉一直是暗的、火在他身後」（CG 選的那支側臉被灶火照亮）"),
    dict(loc="house_door_night", cam="Medium close-up, locked", chars=["xuyan"], night="house_door_night",
         comp=f"medium close-up of Xu Yan standing just inside the house door, framed from the chest up with space above his head, {XU}, {NIGHT}, one bundle of firewood in both arms, his body and face three-quarter to screen left toward the doorway and the figure by the wok off screen left, the camera about 45 degrees off his eyeline, never the lens; shocked and furious: brows slammed down, eyes wide and glaring, nostrils flared, jaw clenched between words; behind him only the darkness inside the house; no stove or wok in the frame",
         lines=[("xuyan", "誰在那裡！把水桶給我放下，別碰那口鍋！", "厲聲")],
         motion=f"the firewood in his arms crashes down to the floor all at once and he braces one hand against the door frame, shouting the line out through the doorway at the figure; {NOSMILE}",
         zh="中近景、固定：許硯在屋門內，懷裡的柴嘩啦一下掉了一地，一手撐住門框；身後只有屋內的黑暗；驚怒（結尾，懸念到第 5 集）。live prep 2026-11-09：中近景推到近景、「臉朝鏡頭往外看」改成固定中近景、頭上留空，四分之三側臉朝畫左的門口與鍋邊的黑影（第 40 鏡黑影回頭往右看屋門，接得上）、鏡頭偏離視線約 45°、不看鏡頭；驚怒逐部位寫：眉往下壓、眼睛睜大瞪著、鼻翼張、字句之間咬牙；柴寫成一下子全掉（CG 選的那支慢慢滑下）；NOSMILE"),
    dict(loc="yard_night_cu", cam="Low-angle medium shot, slow push in", chars=[], night="yard_night", act=3,
         comp=f"low-angle medium shot, the shot opens directly on the man from its very first frame, framed from his shins up so the top of the low wooden stool under his feet shows at the bottom edge of the frame: {FIGURE}, standing upright on the stool beside the big wok, his head high above the wok's rim, one wooden bucket full of water held level in both hands above the mouth of the wok; the orange glow of the stove fire and the white steam rising behind him, so his face and the front of his body stay a dark silhouette; the frame stays this close the whole shot",
         lines=[],
         motion="he holds the full bucket above the wok's mouth, then snaps his head round to look right at the house door; the bucket only tilts a little in his hands, the water sloshing up to its rim and staying inside the bucket; he freezes like that and the shot ends on that moment",
         zh="近景偏中景、低角度、慢推（2026-11-07 第二次獨立審片：拍到小腿、板凳頂在畫面下緣，看得出他站在板凳上；只倒一點、不倒進鍋，接第 5 集 c01）：黑影（FIGURE）站在鍋邊板凳上，兩手把裝滿水的木桶平舉在鍋口上方，灶火與白氣在他身後、臉與身前是黑的剪影；然後猛一回頭往右看屋門，水桶只是傾斜、水在桶口晃、留在桶裡；定在這一刻收"),
]

HEAD = [
    "- 重製版 r2：照 `docs/videos/zhong-tian-qu-qi-e004-r2/script.md`（c01–c40 對應 s01–s40；含「2026-11-06 審稿後的修改」）；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。",
    "- 內部工作編號 904（`hailuo/*-dh-e904.json`、`colab/runs/e904/`）；發布 slug `zhong-tian-qu-qi-e004-r2`。不放集數、不放片名卡；c01 直接接第 3 集 c40（許硯蹲在灶口前，手上一根柴）。",
    "- 狀態：許硯袖子捲到手肘、捲紅紙插腰帶左邊（全集），第一場右手一根柴，s11 木勺，s13–s15 裂了縫的小鐵鍋，過場長木棍、眼睛發紅，s38–s39 兩臂抱柴；阿令沒戴鐵鐐、袖子蓋住手腕，s01–s05 短刀橫在膝上，s06 起插在腰帶左邊的深褐皮鞘；唐小棠 t2，s16–s25 抱小木匣（五錠元寶形金錠，沒有字）；二牛 s27–s28 背上倒扣大黑鐵鍋，之後兩手空空；秦霜柴刀在腰帶右邊，s31–s32 右肩扛一整頭死豬（閉眼、草繩綁腳、不見血）。",
    "- 真人版前置（live prep 2026-11-09，照第 1–3 集真人版與 route-a.md 的教訓）：每張露臉的臉都逐部位寫（眉、眼、嘴角、下巴、呼吸）；每一句露嘴的台詞，說話的人側臉或四分之三側臉朝聽的人、不看鏡頭，鏡頭固定、偏離視線約 40–60°，或用過肩；說話的人取胸口或腰以上、頭上留空，不對單張臉正面推近；提示詞裡唯一的笑字是 NOSMILE 那一句（s05 乾笑、s18 小禾開心、s25 唐小棠一點笑、s27 二牛咧嘴都寫成臉怎麼動）；眼睛大特寫用 EYES（自然深褐虹膜、只有一張臉、沒有疊影）；臉上不打淡藍光；唐小棠服裝照定妝照（TANG：交領短襦闔上、百褶裙繫蝴蝶結），不寫立領；第一場灶房一律是第 3 集定下的紅磚灶（kitchen_brick）；阿令的短刀用第 3 集同一句 KNIFE；許硯的袍子兩肩完整（e904-live spec 另把定妝句的補丁改成只在手肘）。",
    "- 長鏡要買的秒數（`r2.py` 的 BUY）：s03、s13、s37 8 秒（script.md 長鏡清單）；s14 12 秒、s15 10 秒（長鏡清單寫 8，錄好的兩句加停頓要 10.6、9.8 秒）；s10、s35 8 秒（錄好的配音加半秒 6.6、6.5 秒，超過預設 6 秒）。其餘照 `gen-dh` 的 6 秒，眼睛大特寫 s12、s24 5 秒。",
]
FOOT = [
    "- 場景參考：第一場灶房 `set-xujia-zao-t1`（真人版照第 3 集 fix3 選定片段寫成紅磚灶、灶上黑鐵鍋、火口在前、旁邊堆劈柴，門外冷月光）；s10–s15 屋內 `set-xujia-wu-t1`（晨光從左邊門窗斜進來）；s16–s35 院子 `set-xujia-yuan-t1`（早上暖光 → 白天右側斜光）；過場院子東側灶棚（棚柱在左、土灶與大鍋在中間、屋門在右，照第 5 集），仍用院子的場景圖。近景背景都寫「同一個灶房／屋內／院子」。",
    "- 唐小棠一律用 `tangxiaotang-portrait-t2`（gen-dh 的 PORTRAIT 對照）；真人版（live prep 2026-11-09）構圖一律寫 TANG（定妝照的交領短襦闔上、百褶裙繫蝴蝶結），不寫立領或「一件闔上」（pilot.py 會擋，也會被換成 high-waisted）。",
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
