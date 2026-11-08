"""Episode 2 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e002-r2/script.md
(c01-c40 = s01-s40, plus c13b = s13b), including its section 「2026-11-06 審稿後的修改」, which overrides the tables.

Same rules as e001-r2: one visible action per shot written as a path, over-the-shoulder and reverse shots for dialogue,
whole sentences, one line per spoken line, no smile where the script does not allow one (c03, c15, c17, c21, c27).
Live action (2026-11-08, e901 expression review): every visible face gets an expression written as brows, eyes, mouth
corners, jaw, throat and breath at the moment of the line, "not a happy/friendly smile" where a smile must not read as
happy; Qin Shuang cold and A-ling guarded by the script, but still a specific face; no calm/neutral wording. State: Xu Yan half-dry with wet cuffs c03-c14, dry with sleeves rolled and sweat from c15
(no wood chips on skin, 2026-11-07 review); the rolled red paper in the left of his belt from c03; A-ling without shackles from c01's unlocking,
her sleeves over the red marks; Qin Shuang's old chopping knife in the right of her belt (drawn c17, back c21, held
c38, thrown c40); Tang Xiaotang always t2 (high collar, closed garment); the loan note folded into a strip, back to the
camera; the grey-clad servants and the villagers have no picture and are never shown by the face.
"""
EP = 902  # internal working number; the published slug is zhong-tian-qu-qi-e002-r2
SLUG = "zhong-tian-qu-qi-e002-r2"
EP_TITLE = "三個新娘沒一個肯嫁，債主上門要拿人抵（重製版 r2）"
OUTLINE_SECONDS = 212  # script.md 2026-11-06: 79.5 + 55.5 + 77 s, 41 shots
TARGET_MINUTES = [3, 4]
TITLE = "三個新娘沒一個肯嫁，債主上門要拿人抵｜種田娶妻打天下 第2集（重製版）"
DESCRIPTION = "配婚令一走，許硯想跟三個新娘坐下來談，結果一個都不肯嫁：秦霜要他先把柴堆劈完，唐小棠只要許家的戶籍不要相公，阿令搖頭走開。午後許硯劈柴，斧頭卡在木頭裡拔不出來，秦霜單手一刀把木頭劈成兩半、連卡住的斧頭都劈了出來，兩人約好三天後看他賺的錢。日頭偏西，錢員外帶著家丁上門，要先收「月息三分」的利錢，被唐小棠用大衡律「只准兩分」當眾拆穿，只好不要利錢、改逼本錢二十兩。唐小棠望一眼大路，忽然說現在就嫁，原來她在躲一個比錢員外更可怕的人。許硯拿不出二十兩，錢員外翻臉要拿人抵，家丁抓住唐小棠往外拖，一把舊柴刀從畫面左邊飛向院門。《種田娶妻打天下》第 2 集（重製版）。"
THUMB = ("拿人來抵", "s38")
CHARACTERS = ["xuyan", "qinshuang", "aling", "tangxiaotang", "xiaohe", "erniu", "zhaobutou", "qianyuanwai", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: a light playful comedy of woodblock, pipa and dizi in the sunny yard near noon, dropping out to a single cold electronic blip on the system line; the same bright comedy at the woodpile in the afternoon with one heavy hit as the log splits; a tense cue of low drums and erhu when the moneylender arrives in the late afternoon, dropping out to a single deep hit on the system chime; a low suspense cello as the knife flies, stopping in midair; ancient Chinese rural drama, no vocals"

# Scene headers of script.md: the same Xu family yard all episode (set-xujia-yuan-t1), three lights.
# Axis: the woodpile on screen left, the house door at the back left, the gate on screen right, the well at the back right.
LOC = {
    "yard": "In the dirt yard of the Xu farmhouse near noon on a clear autumn day, an autumn tree, a bamboo fence, a woodpile on screen left, the house door at the back left, the yard gate in the fence on screen right, a stone well at the back right, bright sunlight from overhead and slightly right casting short shadows",
    "yard_pm": "In the dirt yard of the Xu farmhouse in the early afternoon on a clear autumn day, an autumn tree, a bamboo fence, a woodpile with a wooden chopping block on screen left, the house door at the back left, the yard gate in the fence on screen right, a stone well at the back right, warm slanting afternoon sunlight from screen right casting longer shadows",
    "yard_late": "In the dirt yard of the Xu farmhouse in the late afternoon on a clear autumn day, the sun low in the west, an autumn tree, a bamboo fence, a woodpile on screen left, the house eaves at the back left, a wooden table in the middle, the yard gate in the fence on screen right, a stone well at the back right, low golden sunlight slanting in from the gate on screen right casting long shadows",
    # 2026-11-07 review retakes (fix2): close-ups and inserts keep the set to one line.
    "yard_cu": "In the dirt yard of the Xu farmhouse near noon, bright sunlight from overhead",
    "yard_pm_cu": "In the dirt yard of the Xu farmhouse in the early afternoon, warm slanting sunlight from screen right",
    "yard_late_s": "In the dirt yard of the Xu farmhouse in the late afternoon, an autumn tree, a bamboo fence, the house eaves at the back left, the yard gate in the fence on screen right, a stone well at the back right, low golden sunlight slanting in from the gate on screen right casting long shadows",
    "yard_late_cu": "In the dirt yard of the Xu farmhouse in the late afternoon, low golden sunlight from screen right",
    # fix3: medium shots with long prop phrases keep the set to one short line (route-a.md: the 1000-character cap).
    "yard_m": "In the dirt yard of the Xu farmhouse near noon on a clear autumn day, the woodpile and the bamboo fence behind, bright sunlight from overhead casting short shadows",
    "yard_pm_m": "In the dirt yard of the Xu farmhouse in the early afternoon, the woodpile and the bamboo fence behind, warm slanting sunlight from screen right",
    "yard_late_m": "In the dirt yard of the Xu farmhouse in the late afternoon, the bamboo fence and the yard gate on screen right, low golden sunlight slanting in from screen right",
}
LIGHT = {
    "yard": "the bright near-noon sunlight stays unchanged",
    "yard_pm": "the warm slanting afternoon light from the right stays unchanged",
    "yard_late": "the low late-afternoon sunlight from the right stays unchanged",
}

# Repeated wording (each prop is one object; the descriptions say "one" where it first appears).
TANG = "her peach-pink brocade ruqun one closed garment from the high stand-up collar to the waist"
SERV = "grey coarse cotton cross-collared short jackets, cloth head-wraps and cloth shoes, both hands empty"
VILL = "villagers in Song-dynasty cross-collared coarse cotton jackets and cloth head-wraps"
# 2026-11-07 independent review (fix2): each prop is one body-scale phrase, word for word the same in every shot.
# 2026-11-07 fix3: written positively (the "not a wide square cleaver" tail went), the size kept body-scale.
KNIFE = "one old chopping knife with a narrow iron blade as long as a forearm, a thick back, a bright edge and a black-cloth-wrapped wooden handle"
# fix3: the axe, the tossed log, the fan and the loan note, each one phrase copied into every redesigned shot.
AXE = "the one axe with a wooden handle as long as an arm and a dark iron head"
TOSS = "one arm-thick split firewood log of pale wood as long as a forearm"
FAN = "one plain bamboo-ribbed folding fan with a blank face"
IOU = "the one loan note folded into a narrow strip as long as his hand, its plain blank back toward the camera"
LOG = "round log of pale wood with grey bark, as thick as a man's thigh and as long as a man's forearm"
BLOCK = "the knee-high round wooden chopping block"
SHACKLES = "old Chinese iron shackles: two thick hand-forged dark iron rings joined by a short iron chain and one square iron padlock, not hinged police handcuffs"
# e902 live fix1 (2026-11-08), copied word for word from e001-r2/r2.py (its fix5-fix7): a face that must not smile gets no
# smile word at all except this one ban (smile, smirk, sneer, grin, half-smile all came out as a warm happy smile; Qian
# Yuanwai's "smug smile", "thin sneer" and "sneer" turned the villain friendly in s27, s29, s31). The eye extreme
# close-ups keep natural eyes: "a faint pale blue light reflected in his pupils" drew glowing blue irises in s13 and s35.
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
EYES = "his irises a natural dark brown from the first frame to the last, the whites of his eyes clear, only a tiny faint cold pale glint of reflected light in each pupil, like a catchlight"
# The villain's face (fix1): mouth closed and turned down, eyes cold, brows low; never a smile word.
QIAN_FACE = "his face cold and hard: lips closed, the corners of his mouth pulled down, his eyes narrowed, cold and hard, his brows lowered"

SHOTS = [
    # ---- scene 1: the yard, who will marry (near noon). Axis: Xu Yan left facing right; the three women right
    # (Qin Shuang nearest, Tang Xiaotang middle, A-ling at the back by the well).
    dict(chapter="誰肯嫁", loc="yard_cu", cam="Insert close-up, slow push in", chars=["aling"], night="yard",
         comp=f"insert close-up of A-ling's two wrists in her grey-white cotton sleeves, the shot opens directly on her wrists and the shackles from its very first frame: {SHACKLES}, one ring locked round each wrist; the right hand of Constable Zhao, who stays off screen, reaches in from the upper right in a black uniform cuff, pinching one black iron key; only the hands and sleeves are in the frame, all faces out of the frame; behind them only the out-of-focus dirt ground",
         lines=[("zhaobutou", "鐐銬是官府的，得帶回去交差。", "畫外，不耐煩")],
         motion="the hand turns the key in the square padlock; the lock opens, both iron rings spring open and fall off her wrists with the chain to the dirt; her bare wrists show a faint red band round each and a pale old scar inside the right wrist; only then A-ling pulls both sleeves down over them",
         zh="手部特寫、慢推（第一格就是阿令手腕與鐵鐐：手工鍛的粗鐵環兩個、鐵鍊、方鐵鎖，不是現代手銬）：趙捕頭（畫外）黑公服袖口的右手轉鑰匙開方鎖，兩個鐵環彈開、連鍊子從手腕掉到泥地；露出紅勒痕與右手腕內側淡白舊疤，然後阿令才拉下袖子蓋住"),
    dict(loc="yard", cam="Full shot, tracking", chars=["zhaobutou", "erniu"], night="yard", act=5,
         comp=f"full shot through the bamboo fence in the foreground: on screen right Constable Zhao seen from behind in his black constable's cap and black uniform, his sword in its black scabbard at his left hip, and {SHACKLES} lying open on the dirt at his feet; at the back left Wang Erniu in his coarse brown jacket with rolled sleeves, both hands empty; outside the fence about five {VILL}, only their upper bodies showing",
         lines=[],
         motion="Zhao bends, picks the shackles up from the dirt and slings them over his right shoulder, his sword staying sheathed at his left hip; only then he strides out through the gate on screen right as the villagers part to both sides; Erniu waves to Xu Yan off screen left with a sheepish, sympathetic wince, his brows raised and drawn up in the middle and his mouth pulled to one side, and follows him out; all lips stay closed",
         zh="全景、跟拍（往右）、前景籬笆：趙捕頭（黑捕快帽）背影彎腰撿起泥地上的鐵鐐甩上右肩，佩刀一直在左腰刀鞘裡；然後才大步出院門，籬笆外村民往兩邊讓開；二牛（兩手空空）朝左邊的許硯擺手，跟著出院門。表情（2026-11-08 真人版）：二牛擺手時替許硯捏把冷汗（眉毛上揚往中間皺、嘴歪向一邊，同情的苦臉）"),
    # live-action prep (2026-11-07, preflight `four`): four named faces drew a stranger in crowded shots, so A-ling, last in
    # the row and silent here, stands just past the right frame edge; he still walks up to and addresses all three.
    dict(loc="yard", cam="Medium shot, tracking", chars=["xuyan", "qinshuang", "tangxiaotang"], night="yard",
         comp=f"medium shot, Xu Yan on screen left in his blue-grey scholar's robe, half-dry with the cuffs still wet, one roll of red paper rolled shut in his right hand with its plain blank back outward; on screen right Qin Shuang and Tang Xiaotang standing in a row: Qin Shuang nearest with her arms folded and {KNIFE} tucked in the right side of her belt, Tang Xiaotang beside her, {TANG}; beyond them A-ling stays off screen past the right frame edge",
         lines=[("xuyan", "三位姑娘，配婚令來得突然，成親的事，我們能不能坐下來談？", "陪笑")],
         motion="Xu Yan tucks the rolled red paper into the left side of his belt, rubs his hands together and walks up to the women, stopping before them, with a stiff ingratiating smile: the corners of his mouth pulled up tight, his brows raised and drawn up in the middle, his eyes darting from one woman to the other, not a happy smile; Qin Shuang stares at him, her eyes narrowed and her mouth set hard; Tang Xiaotang looks him over with her head tilted, one eyebrow raised, appraising; the women stay still and their lips stay closed",
         zh="中景、跟拍（往右）：許硯（半乾、袖口濕）把捲紅紙塞進腰帶左邊，搓著手走到三個女子面前陪笑（笑得不自在）；秦霜抱胸，三人沒動；阿令（排最後）在畫面右邊緣外，畫面裡只有秦霜與唐小棠。表情（2026-11-08 真人版）：許硯陪笑是硬擠的笑（嘴角往上扯緊、眉毛上揚往中間皺、眼睛在兩人之間飄，不是開心的笑）；秦霜瞇眼盯他、嘴抿緊；唐小棠歪頭、挑一邊眉上下打量他"),
    dict(loc="yard", cam="Over-the-shoulder medium shot, slow push in", chars=["qinshuang", "xuyan"], night="yard",
         comp=f"over-the-shoulder shot from behind Xu Yan's shoulder and its wet cuff in the left foreground, Qin Shuang facing the camera on screen right with her arms folded, {KNIFE} tucked in the right side of her belt, impatient: brows drawn down, mouth set hard, her eyes on him",
         lines=[("qinshuang", "談什麼？你先說說，你拿什麼養活三個人？", "不耐煩")],
         motion="Qin Shuang jerks her chin toward the woodpile off screen left and takes one step forward, closing in on Xu Yan, her eyes narrowing to slits on 「拿什麼養活三個人」 with a sharp impatient breath through her nose, no smile; his shoulder flinches back",
         zh="過肩（許硯肩後拍秦霜）、慢推：秦霜抱胸，下巴往左邊柴堆一抬，往前跨一步逼近；許硯的肩往後縮。表情（2026-11-08 真人版）：說「拿什麼養活三個人」時眼睛瞇起、鼻子不耐煩地出一口氣，不笑"),
    # e902 live fix1 (2026-11-08): both seeds said the line straight into the lens and smiled (a frontal single close-up
    # with a push in). Locked, the camera ~40 degrees off his eyeline, his body and face three-quarter to screen right
    # toward Qin Shuang off screen right; NOSMILE the only smile word.
    dict(loc="yard", cam="Medium close-up, locked", chars=["xuyan"], night="yard",
         comp="medium close-up of Xu Yan framed from the chest up with clear space above his head, in his blue-grey scholar's robe, half-dry with the cuffs still wet, the rolled red paper tucked into the left side of his belt with its plain blank back outward, his body and face turned three-quarter to screen right toward Qin Shuang off screen right, the camera about 40 degrees off his eyeline, his eyes on a point just outside the right frame edge, never the lens, honest and earnest: his brows drawn up a little in the middle, his eyes open and direct on her, his lips pressed between phrases; behind him only the bamboo fence and the autumn tree of the same yard",
         lines=[("xuyan", "現在是拿不出來，可是三天之內，我一定想出辦法。", "老實")],
         motion=f"he pats his sleeve pocket, which hangs flat and empty, with a sheepish wince, his lips pressed together for a beat; then he spreads both empty hands open toward her, and on 「我一定想出辦法」 his jaw firms and he gives one earnest nod, his face in three-quarter profile toward her, his eyes holding hers, never into the lens, his lips pressed between phrases, {NOSMILE}",
         zh="近景、固定（2026-11-08 真人版 fix1 視線重拍：原本單人正面、中近景推到近景，兩支都正對鏡頭講、帶笑，也沒拍袖袋、攤手）：胸口以上、頭上留空；鏡頭偏離他的視線約 40°，許硯身體與臉四分之三側向畫右、朝畫外右邊的秦霜，眼睛看畫框右緣外一點，不看鏡頭；拍拍扁扁的袖袋，攤開兩手朝她；老實、認真：眉頭中間微微往上、眼睛直直看秦霜，字句之間嘴抿著；拍袖袋時尷尬地一皺臉、嘴抿一下，說「我一定想出辦法」時下巴收緊、認真點一下頭；從頭到最後一格都不笑（NOSMILE）"),
    # fix3 redesign: locked full shot from the first frame with the log already in her hand (both drafts lost the walk to the
    # pile and the pull: a log out of nowhere, a knee-long blade, her face out of frame); two steps between them.
    dict(loc="yard_m", cam="Full shot, locked", chars=["qinshuang", "xuyan"], night="yard",
         comp=f"full shot with the camera held still, both of them whole from head to cloth shoes with space above their heads the whole shot, two steps apart on the dirt: on screen left Xu Yan in his half-dry blue-grey scholar's robe with the cuffs still wet, facing right; on screen right Qin Shuang facing him, the woodpile just behind her, her face cold: brows level, mouth set hard, {KNIFE} small at her side, tucked in the right side of her belt, and {TOSS} already in her right hand, held low",
         lines=[("qinshuang", "想辦法不如先動手。把這堆柴劈完，再來跟我談嫁。", "冷")],
         motion="Qin Shuang, her chin raised and her eyes narrowed hard on him, swings the log underhand and lets it go low toward Xu Yan's feet; it lands on the dirt, rolls twice and stops against the toe of his left cloth shoe, where it stays on the ground to the end; Xu Yan hops half a step back, his eyes going wide and his brows jumping up in alarm, his lips closed; the knife stays tucked in her belt",
         zh="全景、固定（fix3 重設計：第一格秦霜已經在柴堆前、右手拿著一根手臂粗的木柴；兩人相距兩步、頭到腳都在畫面裡）：秦霜冷著臉，把木柴往許硯腳前低低一丟，滾兩圈停在他左腳鞋尖、留在地上；許硯往後跳半步；柴刀一直插在腰帶右邊。表情（2026-11-08 真人版）：秦霜下巴抬起、眼睛瞇著盯他；許硯往後跳時眼睛睜大、眉毛一跳"),
    # live-action prep (2026-11-07, preflight `headroom`): he bends down and straightens up during Tang's line, so the
    # framing writes the space above his head.
    dict(loc="yard", cam="Low-angle close-up, slow push in", chars=["xuyan"], night="yard",
         comp="low-angle close-up of Xu Yan in his half-dry scholar's robe with the cuffs still wet, framed with clear space above his head so that his whole head stays inside the frame as he bends down and straightens up, one log lying at his feet at the lower edge of the frame; behind him only the autumn tree and the sky above the same yard",
         lines=[("tangxiaotang", "她要你劈柴，我這邊倒是簡單多了。", "畫外，輕快")],
         motion="he looks down at the log at his feet, his brows drawing up in dismay, and swallows hard; he bends down, picks it up and hugs it to his chest, then sets his jaw and gives one short resigned nod toward Qin Shuang off screen, the corners of his mouth pulled down; his lips stay closed",
         zh="低角度近景、慢推（從腳邊的木柴帶到臉）：許硯低頭看木柴、嚥口水，彎腰撿起抱在胸前，朝秦霜點一下頭；唐小棠畫外說話；頭上留空，彎腰再站直時整個頭都在畫面裡。表情（2026-11-08 真人版）：看木柴時眉頭往上皺、用力嚥口水，點頭前下巴一咬、嘴角往下，認命"),
    dict(loc="yard", cam="Medium shot, tracking", chars=["tangxiaotang", "xuyan"], night="yard",
         comp=f"medium shot, Tang Xiaotang in {TANG}, one small palm-sized gold abacus with wooden beads on her left palm and her right forefinger flicking its beads, and Xu Yan on screen left hugging the log",
         lines=[("tangxiaotang", "我只要你許家的戶籍，相公這兩個字就免了。", "談生意的口氣")],
         motion="flicking the abacus beads, Tang Xiaotang walks from screen right round to Xu Yan and stops one step to his right, tilting her head to look at him, one eyebrow raised and her eyes measuring him like goods on a counter, brisk and businesslike, her lips closed between words, no smile; Xu Yan turns his head to follow her, blinking, his brows drawing together in confusion, his lips closed",
         zh="中景、跟拍（由右往左）：唐小棠（t2，襦裙從立領到腰一件闔上）左手托金算盤、右手食指撥珠，繞到許硯右側一步，歪頭看他。表情（2026-11-08 真人版）：唐小棠挑一邊眉、眼睛像在估價一樣打量他，談生意的乾脆、不笑；許硯眨眼、眉頭皺起，搞不懂"),
    # live-action prep (2026-11-07, preflight `headroom`): he speaks while leaning forward, so the framing writes the
    # space above his head.
    dict(loc="yard", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="yard",
         comp=f"over-the-shoulder shot from behind Tang Xiaotang's shoulder and her looped bun with its pink ribbon in the right foreground, {TANG}, and Xu Yan facing the camera on screen left hugging the log, dumbfounded: his eyes wide, his brows shot up, his mouth hanging open between words, framed with clear space above his head so that his whole head stays inside the frame as he leans forward",
         lines=[("xuyan", "只要戶籍不要人？那跟成親到底差在哪裡？", "傻眼")],
         motion="Xu Yan shifts the log into his left arm, points at himself with his right forefinger and leans forward toward her, his brows climbing higher on 「差在哪裡」 with a disbelieving shake of his head, no smile",
         zh="過肩（唐小棠肩後拍許硯）、慢推：許硯把木柴換到左手，右手指指自己，往前探身；傻眼；頭上留空，探身時整個頭都在畫面裡。表情（2026-11-08 真人版）：眼睛瞪大、眉毛揚起、嘴張著；說「差在哪裡」眉毛揚得更高、不可置信地搖頭，不笑"),
    # fix3 redesign: her portrait and angle-b grin, so the line plays from behind her (nospeak): the abacus click and
    # Xu Yan's wary face carry the shot; both drafts smiled through the line and showed no abacus.
    dict(loc="yard_cu", cam="Over-the-shoulder close shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="yard",
         comp=f"over-the-shoulder close shot from behind Tang Xiaotang: the back of her head with its two looped buns and pink silk ribbons and her right shoulder fill the right foreground, her face turned away from the camera toward Xu Yan the whole shot, {TANG}; one small palm-sized gold abacus with wooden beads raised on her left palm beside her shoulder, its beads toward Xu Yan; on screen left one step away Xu Yan facing the camera in his half-dry blue-grey scholar's robe, hugging the log, wary: brows drawn together, lips closed; behind him only the bamboo fence",
         lines=[("tangxiaotang", "差多了。戶籍是一張紙，相公是要天天看見的。", "精明")],
         motion="her right forefinger flicks one bead up with a sharp click, then she tips her head slightly to one side, still facing Xu Yan; Xu Yan blinks at the abacus, his eyes narrowing warily and flicking from the abacus to her, and hugs the log tighter, his lips pressed into a thin line",
         zh="過肩近景（唐小棠背後）、慢推（fix3 重設計：她的定妝照與 angle-b 都在笑，兩稿從頭笑到尾；改拍她的後腦與肩、她說話不露嘴）：唐小棠左手把金算盤托到肩旁，右手食指「嗒」地撥上一顆珠，頭微微一歪；許硯面向鏡頭抱著木柴，眉頭皺起、嘴閉著。表情（2026-11-08 真人版）：眼睛警覺地瞇起、在算盤與她之間來回，嘴抿成一條線"),
    # e902 live fix1 (2026-11-08): both seeds opened frontal, grinning 「那妳呢」 into the lens, and smiled again at the
    # well. The walk is gone: the shot opens on him already one step before her at the well, in profile toward her, the
    # log already at his feet; a locked side two-shot; NOSMILE the only smile word.
    dict(loc="yard", cam="Medium two-shot, locked", chars=["xuyan", "aling"], night="yard",
         comp="medium two-shot from the side by the stone well, the shot opens on this state from its very first frame: Xu Yan in his half-dry scholar's robe standing one step before A-ling, in profile facing screen right toward her, his hands empty, the log already set down on the dirt at his feet; A-ling on screen right by the stone well in her plain grey-white cotton dress, her sleeves pulled down over her wrists, facing him with her head slightly bowed; nobody else in the frame",
         lines=[("xuyan", "那妳呢？妳願不願意，留下來跟我過日子？", "小心")],
         motion=f"Xu Yan stays where he stands and asks gently, his face in profile toward her, his eyes on her face, never into the lens, gentle and careful: his brows drawn up softly in the middle, his eyes careful and hopeful, a hesitant breath before 「妳願不願意」, his lips pressed between phrases, {NOSMILE}; A-ling keeps her head slightly bowed, her eyes lowered to the ground, her lips pressed thin, her face closed and guarded; A-ling's lips stay closed",
         zh="雙人中景、側面、固定（2026-11-08 真人版 fix1 視線重拍：原本跟拍走到井邊，兩支 0–1.5 秒都正對鏡頭咧嘴講「那妳呢」，到井邊又笑著問）：拿掉走位，第一格許硯就站在井邊阿令前一步，側臉朝畫右面向她，兩手空著、木柴已放在腳邊泥地上；阿令在畫面右邊井旁，袖子蓋住手腕，微低頭面向他。許硯站著不動、輕聲問，側臉朝她、眼睛在她臉上，不看鏡頭：眉頭往上微皺、眼神小心又帶一點期待，說「妳願不願意」前先吸一口氣，字句之間嘴抿著，從頭到最後一格都不笑（NOSMILE）；阿令微低頭、眼睛看地、嘴抿薄，臉是關上的、戒備，嘴閉著"),
    dict(loc="yard_cu", cam="Medium close-up to close-up, slow push in", chars=["aling"], night="yard", act=4,
         comp="medium close-up, closing in to a close-up by the end, of A-ling in her plain grey-white cotton dress with her wooden hairpin, her face cold and still: brows level, eyes steady, lips pressed thin, her sleeves pulled down over her wrists, her eyes on Xu Yan off screen left; behind her only the stone well and the bamboo fence",
         lines=[],
         motion="she lifts her eyes to Xu Yan off screen left once, a flicker of wariness tightening the corners of her eyes and her jaw, and shakes her head slightly, her lashes lowering; only then she turns and walks away to the far side of the well, pulling her right sleeve down over her wrist as she goes; her lips stay closed",
         zh="近景、慢推（中近景推到近景）：阿令看許硯一眼，輕輕搖頭，轉身往井的另一邊走開，邊走邊把右手袖子再往下拉；冷、不笑。表情（2026-11-08 真人版）：抬眼看許硯一下，眼角與下巴一緊、帶一點戒心，搖頭時垂下眼"),
    dict(loc="yard", cam="Extreme close-up, slow push in", chars=["xuyan"], night="yard",
         # e902 live fix1 (2026-11-08): the blue-light phrase drew solid glowing blue irises in both seeds (one looked into
         # the lens, the other cut to a wide at 5.75 s): EYES, the eyes only, the eyeline slightly right.
         comp=f"extreme close-up of Xu Yan's eyes only, the shot opens directly on his eyes from its very first frame and the frame never widens: his two eyes and brows fill the frame, {EYES}, his eyeline slightly to screen right, never into the lens; nothing else in the frame",
         lines=[("xuyan", "一個要柴，一個要戶籍，一個搖頭，這任務做不完。", "心裡話，嘴閉著", "inner")],
         motion="his eyes follow A-ling off screen to the right, then flick aside; his brows draw together and his lower lids tighten in dismay, and he shuts his eyes for one long weary blink; the frame holds only his eyes and brows to the last frame",
         zh="眼睛大特寫、慢推（第一格就是眼睛，整鏡只有兩隻眼睛與眉毛、不拉遠）：虹膜是自然深褐色、瞳孔裡只有一點很小的反光（2026-11-08 真人版 fix1：原寫「瞳孔映淡藍光」，兩支虹膜整個亮藍，一支看鏡頭、一支硬切全景），視線偏畫右、不看鏡頭；眼睛跟著阿令的背影往右移，再一瞟，皺眉；心裡話。表情（2026-11-08 真人版）：皺眉、下眼瞼一緊，沮喪地長長閉一下眼"),
    # c13b (2026-11-06 review): split from c13; its own id keeps s14-s40 unchanged.
    # live-action prep (2026-11-07, preflight `four`): the three out-of-focus women made four named people in one shot;
    # they move off screen right and his eyeline carries the beat, resting on each of them in turn (worded without
    # "the three women", which makes gen-dh send all three brides' pictures).
    dict(sid="s13b", loc="yard", cam="Medium close-up, slow push in", chars=["xuyan"], night="yard",
         comp="medium close-up of Xu Yan in his half-dry blue-grey scholar's robe with the cuffs still wet, the rolled red paper tucked into the left side of his belt with its plain blank back outward, framed alone; the brides stand off screen to the right, all three of them; behind him only the bamboo fence and the autumn tree of the same yard",
         lines=[("xitong", "做不完就抹殺。建議宿主別浪費時間。", "冷")],
         motion="Xu Yan turns round toward screen right and his eyes stop on three points off screen right one after another, near, middle and far, his brows drawn up in the middle; on 「抹殺」 his eyes go wide and his throat bobs as he swallows hard, then his shoulders slump and the corners of his mouth pull down in dread; his lips stay closed",
         zh="中近景、慢推（2026-11-06 審稿新鏡）：許硯轉身一個一個看向畫面右邊外的三個女子（真人版準備：三個女子移到畫外，視線一近一中一遠停三下），肩膀垮下來；嘴閉著；系統畫外（冷的「嘀」）。表情（2026-11-08 真人版）：眉頭往上皺；聽到「抹殺」眼睛睜大、喉嚨一動用力嚥口水，然後肩膀垮下、嘴角往下，害怕"),
    # live-action prep (2026-11-07, preflight `four`): four named people in the wide; A-ling walked off past the well in
    # s12, so she stays off screen here and the shot keeps Qin Shuang, Tang Xiaotang and Xu Yan's exit to the woodpile.
    dict(loc="yard", cam="Full shot, slow push in", chars=["xuyan", "qinshuang", "tangxiaotang"], night="yard",
         comp=f"full shot past a wooden eave post in the foreground: on screen left the woodpile, with Qin Shuang walking back to stand beside it with her arms folded; at the back left Tang Xiaotang walking back under the eaves, {TANG}; A-ling stays off screen, gone past the well; in the middle Xu Yan in his half-dry robe with the cuffs still wet, one axe with a wooden handle and an iron head leaning against the wall beside him",
         lines=[("xuyan", "做不完也得做。秦姑娘要柴，我就先把柴劈了。", "豁出去")],
         motion="Xu Yan draws a deep breath, his jaw setting and his brows pulling down in grim resolve, his lips pressed, no smile, and rolls up both sleeves, grabs the axe from the wall by its handle in his right hand, blade down, swings it onto his right shoulder and walks toward the woodpile on screen left; Qin Shuang watches him with one eyebrow raised in doubt, her mouth set hard; Tang Xiaotang tilts her head, her eyes following him with curiosity; the others' lips stay closed",
         zh="全景、慢推、前景屋簷柱子：秦霜回左邊柴堆抱胸、唐小棠（t2）回左後屋簷下、阿令已走到井的另一邊、在畫外（真人版準備：一鏡最多三個有名字的人）；許硯深吸一口氣捲起袖子，從牆邊抄起斧頭扛上右肩，往左邊柴堆走。表情（2026-11-08 真人版）：許硯吸氣時下巴一咬、眉往下壓，豁出去、不笑；秦霜挑一邊眉、不信，嘴抿緊；唐小棠歪頭好奇地看他"),
    # ---- scene 2: the woodpile, early afternoon (slanting light from the right). Axis: Xu Yan left of the
    # chopping block facing right; Xiaohe squatting lower left; Qin Shuang comes from the fence on the right.
    dict(chapter="柴堆", loc="yard_pm", cam="Full shot, slow truck right", chars=["xuyan", "xiaohe"], night="yard_pm",
         comp=f"full shot past the woodpile in the foreground, Xu Yan in the middle beside {BLOCK}, his blue-grey scholar's robe dry now, his sleeves rolled up to the elbows and sweat on his forehead, both hands on the axe handle, and one {LOG} standing upright on {BLOCK}; little Xiaohe squatting at the lower left, her small straw rabbit tucked into her sash, beaming: a wide open-mouthed grin, her eyes shining",
         lines=[("xiaohe", "哥哥加油！劈開了，秦霜姐姐就肯嫁你了！", "大聲")],
         motion="Xu Yan, his jaw clenched and his brows knotted with effort, swings the axe up over his head with both hands and chops down on the log; the axe bites halfway in with a thud and sticks fast, and his eyes go wide in dismay; Xiaohe claps her hands hard; Xu Yan's lips stay closed",
         zh="全景、橫移（由左往右）、前景柴堆：許硯（衣服已乾、袖子捲到手肘、額頭有汗）舉斧劈下，斧頭卡進木頭一半；左下蹲著的小禾用力拍手（可以笑）。表情（2026-11-08 真人版）：許硯咬緊牙、皺眉使力，斧頭卡住時眼睛一瞪；小禾張嘴大笑、眼睛發亮"),
    # fix3 redesign: locked, low and wide enough for the whole body, the block and the log (the push-in lifted the axe out
    # with his hands, and the log merged into a flat stump).
    # e902 live fix1 (2026-11-08): both seeds smiled (one grinning frontally the whole shot, one grinning at 4.5 s with
    # his forehead out of the frame and the log lying flat). He turns three-quarter to Xiaohe off screen left, the camera
    # ~35 degrees off his eyeline; the strain written as gritted teeth and flushed cheeks, NOSMILE the only smile word.
    dict(loc="yard_pm_m", cam="Medium full shot, locked", chars=["xuyan"], night="yard_pm",
         comp=f"medium full shot held still and low at block height, his whole body with his whole head and clear space above it, the block and the log in frame the whole shot: at the lower center {BLOCK} with one {LOG} standing upright on top of it, the log narrower and paler than the block, the iron head of {AXE} buried halfway into its top, the handle slanting up; Xu Yan behind the block, turned three-quarter to screen left toward Xiaohe off screen left, the camera about 35 degrees off his eyeline, his robe dry, sleeves rolled to the elbows, sweat on his forehead, both hands gripping the axe handle, straining: teeth gritted, brows knotted, cheeks flushed",
         lines=[("xuyan", "小禾，不是哥劈不開，是斧頭自己卡住了。", "咬牙，尷尬")],
         motion=f"he heaves up on the handle with both hands, then plants his right cloth shoe on the edge of the block beside the log and heaves again; the axe head stays buried in the top of the log and the log stays standing upright on the block to the end; he speaks to Xiaohe off screen left in three-quarter profile, his eyes sliding to her, never into the lens, through gritted teeth, his face flushing red, the cords of his neck standing out with the strain, his whole head staying inside the frame, {NOSMILE}",
         zh="中全景、固定、低機位（fix3 重設計：兩稿推鏡後斧頭跟著手往上像拔出來了、木頭變成扁木墩；2026-11-08 真人版 fix1：兩支都在笑，一支正面咧嘴、一支額頭出畫、木頭躺平）：整個人、木墩與直立的木頭都在畫面裡，整顆頭在畫面裡、頭上留空；許硯身體與臉四分之三側向畫左、朝畫外左邊的小禾，鏡頭偏離他的視線約 35°；雙手拔斧柄，右腳踩上木墩邊再拔，斧頭一直卡在直立木頭的頂端、木頭一直立在木墩上；對小禾說話時眼睛往她那邊飄、不看鏡頭，咬著牙、臉漲紅、脖子青筋浮起，苦撐；從頭到最後一格都不笑（NOSMILE）"),
    # fix3 redesign: the knife is already drawn when the shot opens (both drafts had it in her hand from frame one; the draw
    # happens off camera between s16 and s17); Xu Yan on the left with empty hands, the axe left in the log.
    dict(loc="yard_pm_m", cam="Over-the-shoulder medium shot, slow push in", chars=["qinshuang", "xuyan"], night="yard_pm",
         comp=f"over-the-shoulder shot from behind Xu Yan: his right shoulder and the back of his head at the left edge of the frame, his hands empty at his sides; in the left foreground {BLOCK} with one {LOG} standing upright on it and the iron head of {AXE} buried in its top, the handle sticking up; on screen right by the bamboo fence Qin Shuang facing the camera, {KNIFE} already drawn and hanging in her right hand at her side, its blade pointing down at the dirt",
         lines=[("qinshuang", "斧頭卡住怪斧頭，你們讀書人都是這樣說話的？", "嗤笑")],
         motion="Qin Shuang straightens up from the fence and strides over to stop just behind the block, facing Xu Yan, her eyes half-lidded and one eyebrow cocked high as she looks him up and down; on 「讀書人」 one corner of her mouth curls up in a contemptuous half-smile, lips thin, no teeth, not a friendly smile, and she gives a short snort through her nose; the knife stays hanging in her right hand with its blade down the whole way; the axe stays buried in the log, and Xu Yan's hands stay empty at his sides",
         zh="過肩（許硯肩後拍秦霜）、慢推（fix3 重設計：兩稿第一格刀就在手上，乾脆從「刀已抽出」開始，抽刀在 s16 與 s17 之間的畫外）：秦霜右手垂著已出鞘的柴刀（刃朝下），從籬笆邊直起身大步走到木墩後；斧頭一直卡在木頭裡，許硯兩手空空在左；嗤笑（可以）。表情（2026-11-08 真人版）：嗤笑寫成臉：眼皮半垂、一邊眉挑高上下打量他，說到「讀書人」一邊嘴角往上撇（嘴唇薄、不露牙，不是友善的笑），鼻子哼一聲"),
    # fix3 redesign: the push starts from its own state (Xu Yan at the block, her palm already on his chest), camera held
    # still with both faces in frame; the knife only hangs in her hand (it vanished and changed shape when it turned).
    dict(loc="yard_pm_m", cam="Medium shot, locked", chars=["xuyan", "qinshuang"], night="yard_pm",
         comp=f"medium shot with the camera held still and space above both heads the whole shot: {BLOCK} at the lower center with one {LOG} standing upright on it and the iron head of {AXE} buried in its top; Xu Yan standing directly behind the block, his sleeves rolled up, sweat on his forehead, both hands empty; Qin Shuang close beside him on screen right, her face cold: brows level, mouth set hard, her left palm already pressed flat on his chest, {KNIFE} hanging in her right hand at her side with its blade pointing down",
         lines=[("qinshuang", "讓開。手腕要沉，力氣從腰上來，不是從嘴上來。", "冷")],
         motion="Xu Yan, his brows shooting up in indignation, opens his mouth to argue and shuts it, his cheeks reddening and his lips pressing tight; Qin Shuang's left hand shoves his chest and he stumbles one step aside to screen left, staying in frame; she steps into his place behind the block and leans forward over the log, her eyes narrowed and fixed on it, her jaw set; the knife stays hanging in her right hand, blade down, to the end; his hands stay empty and his lips closed",
         zh="中景、固定（fix3 重設計：第一格許硯就站在木墩後、秦霜左手已經按在他胸口）：許硯張口又閉上；秦霜左手一推，他往左踉蹌一步、留在畫面裡；她站進他的位置、往木頭前傾；柴刀一直垂在她右手（刃朝下），不轉刀。表情（2026-11-08 真人版）：許硯眉毛一揚想爭、又閉嘴，臉發紅、嘴抿緊；秦霜眼睛瞇起盯著木頭、下巴收緊"),
    dict(loc="yard_pm", cam="Low-angle full shot, locked", chars=["qinshuang"], night="yard_pm", act=3,
         # e902 live fix1 (2026-11-08): both seeds had her pull the stuck axe out and split the log with it, the knife
         # unused, against s20's 「單手一刀，連卡住的斧頭都劈出來了」. Her left hand stays empty and off the axe; the
         # knife comes down beside the axe head, the log splits and the axe falls whole; she ends holding only the knife.
         comp=f"low-angle full shot, the camera held still with her whole body and the whole block inside the frame from head to feet: Qin Shuang standing behind one {LOG} standing upright on {BLOCK} with the axe stuck halfway into its top, the axe handle sticking out toward screen left, {KNIFE} in her right hand, her left hand empty at her side",
         lines=[],
         motion="Qin Shuang, her eyes narrowed and locked on the log and her jaw clenched, keeps her empty left hand at her side, never touching the axe; the axe stays buried in the top of the log; she raises the knife in her right hand over her right shoulder, twists at the waist and chops the knife down into the top of the log right beside the stuck axe head with a sharp breath out through pressed lips; only then the log splits into two halves that fall apart to both sides, and the axe, never touched by her, drops whole to the dirt; she ends holding only the knife in her right hand; her lips stay closed",
         zh="低角度全景、固定（整個動作留在畫面裡，木墩上是 c15 那一截木頭）：秦霜左手空著垂在身側、整鏡不碰斧頭，斧頭一直卡在木頭頂端；右手單手舉刀過肩、腰一擰，一刀劈在卡住的斧頭旁邊；然後木頭才裂成兩半往兩邊倒，斧頭完整掉到泥地；最後她手上只有柴刀（2026-11-08 真人版 fix1：兩支都是她把斧頭拔出來、用斧頭劈開，刀沒用上，跟 s20「單手一刀，連卡住的斧頭都劈出來了」衝突）。表情（2026-11-08 真人版）：眼睛瞇起盯死木頭、咬緊牙，劈下時抿著嘴短促出一口氣"),
    # fix3 redesign: the halves and the axe stay below the frame (s19 shows them); a chest-up close-up of him standing,
    # pointing down out of frame (the drafts crouched, drew a whole log, pointed at the log, lost his head).
    dict(loc="yard_pm_cu", cam="Close-up, slow push in", chars=["xuyan"], night="yard_pm",
         comp="close-up of Xu Yan standing upright, framed from the chest up with space above his head the whole shot, his sleeves rolled up and sweat on his forehead, stunned: mouth agape, eyes wide, brows raised, his eyes cast down at the ground below the bottom edge of the frame; behind him only the woodpile",
         lines=[("xuyan", "單手一刀，連卡住的斧頭都劈出來了？", "看傻")],
         motion="he stares down at the ground below the frame, blinks twice and swallows hard, sways back half a step and points down past the bottom edge of the frame with his right forefinger, his hands holding nothing; he stays standing upright to the end",
         zh="近景、慢推（fix3 重設計：胸口以上、站著；兩半木頭與斧頭留在畫面下緣外，s19 已拍到）：許硯張嘴瞪眼往下看，身子往後一晃半步，右手食指往畫面下方指；手上什麼都沒拿、一直站著。表情（2026-11-08 真人版）：眨兩下眼、用力嚥口水"),
    # fix3 redesign: the knife is back in her belt when the shot opens and her arms stay folded (the knife became an axe in
    # her hand, she picked the axe up herself); only Xiaohe touches the axe. Locked full shot, the axe on the dirt between them.
    dict(loc="yard_pm", cam="Full shot, locked", chars=["xiaohe", "qinshuang"], night="yard_pm",
         comp=f"full shot with the camera held still: on screen right Qin Shuang standing still, whole from head to boots, her arms folded across her chest, both hands empty, {KNIFE} tucked in the right side of her belt, her eyes on the girl, brows level, lips closed in a hard line; on the dirt in the middle of the frame {AXE} lying flat and whole; little Xiaohe at the left edge, grinning, her small straw rabbit tucked into her sash",
         lines=[("xiaohe", "秦霜姐姐好厲害！妳教我好不好？", "崇拜，笑")],
         motion="Xiaohe runs in from the left to the axe, grips its handle with both hands, drags it up off the dirt and hugs the handle to her chest, the iron head hanging at her knees with its blade pointing down at the dirt, away from her face; she looks up at Qin Shuang with a wide adoring grin, her eyes shining and her brows lifted high; Qin Shuang keeps her arms folded and stands still to the end, looking down at the girl, one eyebrow lifting a little and the hard line of her mouth easing, lips closed, no smile",
         zh="全景、固定（fix3 重設計：第一格柴刀已插回秦霜腰帶右邊、她兩手抱胸不動；斧頭只讓小禾碰）：小禾從左跑到泥地上的斧頭前，兩手抓斧柄拖起來抱在胸前（刃朝下、朝外），仰頭看秦霜；秦霜抱胸站著、嘴閉著（插回柴刀移到畫外）。表情（2026-11-08 真人版）：小禾仰頭咧嘴笑、眼睛發亮、眉毛揚高，崇拜；秦霜低頭看她，一邊眉微微一挑、抿緊的嘴角鬆一點，不笑"),
    # fix3 redesign: her portrait smirks and both drafts smiled; the shot is from behind her at a child's height (nospeak),
    # Xiaohe facing the camera, the block in frame so the axe stays visible where it is leaned.
    dict(loc="yard_pm_m", cam="Over-the-shoulder medium shot, slow push in", chars=["qinshuang", "xiaohe"], nospeak=["qinshuang"], night="yard_pm",
         comp=f"over-the-shoulder shot from behind Qin Shuang, low at a child's height: her back, her high ponytail and her right shoulder fill the right foreground, her face turned away from the camera toward Xiaohe the whole shot, {KNIFE} tucked in the right side of her belt; facing the camera little Xiaohe, a few pale wood chips caught in her hair, looking up at her with shining eyes, lips closed, hugging {AXE} by its handle, the iron head at her knees with its blade pointing down at the dirt; {BLOCK} on the left; behind them only the woodpile",
         lines=[("qinshuang", "等妳長到柴墩這麼高再說。妳哥嘛，還差得遠。", "語氣軟一點")],
         motion="Qin Shuang crouches to Xiaohe's height, brushes the girl's hair clean with her left hand, lifts the axe out of her arms and leans it, blade down, against the side of the block, where it stays in frame to the end; Xiaohe pushes her lips out in a small disappointed pout, her brows dipping, then on 「妳哥嘛」 her eyes crinkle and she presses her lips together to hold back a giggle; Xiaohe's lips stay closed",
         zh="過肩中景（秦霜背後、小孩高度）、慢推（fix3 重設計：秦霜定妝照斜嘴笑、兩稿都在笑；改拍她的背影、她說話不露嘴）：秦霜蹲下拍掉小禾頭上的木屑，從她懷裡拿走斧頭、刃朝下靠在左邊木墩旁，留在畫面裡；小禾面向鏡頭、嘴閉著。表情（2026-11-08 真人版）：小禾先失望地嘟嘴、眉毛往下，聽到「妳哥嘛」眼睛一彎、抿嘴忍笑"),
    dict(loc="yard_pm", cam="Reverse close-up, slow push in", chars=["xuyan"], night="yard_pm",
         comp="reverse close-up of Xu Yan, his sleeves rolled up and sweat on his forehead, defiant: his chin lifted, his brows drawn down, his eyes narrowed with a stubborn glint, his jaw set, no smile, his eyes on Qin Shuang off screen right; behind him only the woodpile and the house door of the same yard",
         lines=[("xuyan", "劈柴我不行，可是讓柴多賣幾文錢，我比誰都行。", "不服氣")],
         motion="he bends and picks up half a split log, weighs it in his hand, then straightens up and looks at her, and on 「我比誰都行」 he lifts his chin a notch and gives one firm, confident nod",
         zh="近景反打、慢推：許硯彎腰撿起半截木柴，在手上掂一掂，直起身看秦霜；不服氣。表情（2026-11-08 真人版）：下巴抬起、眉往下壓、眼睛瞇起帶著不服的光、下巴咬住，不笑；說「我比誰都行」時下巴再抬一點、有把握地點一下頭"),
    # e902 live fix1 (2026-11-08): both seeds smiled with the face toward the lens, and one moved the knife from her hand
    # to her back. Locked, she stands in profile toward Xu Yan off screen left, the camera ~40 degrees off her eyeline,
    # the knife tucked in her belt to the end; NOSMILE the only smile word.
    dict(loc="yard_pm", cam="Medium shot, locked", chars=["qinshuang"], night="yard_pm",
         comp=f"medium shot of Qin Shuang standing in profile facing screen left toward Xu Yan off screen left, the camera about 40 degrees off her eyeline, her eyes on him, never the lens, her face cold: brows drawn down and level, eyes narrowed and hard, mouth set hard, both hands empty, {KNIFE} tucked in the right side of her belt, where it stays from the first frame to the last; behind her only the bamboo fence and the woodpile of the same yard",
         lines=[("qinshuang", "那就做給我看。三天後，我再來聽你嘴上這套。", "冷")],
         motion=f"she speaks to him in profile, her eyes on him, her mouth set hard and closing between words; then she turns away to screen right and takes two steps toward the fence, stops, and glances back over her shoulder at Xu Yan off screen left out of the corner of her eye, a sidelong look with narrowed eyes, one eyebrow lifting in challenge, her mouth set hard; her hands stay empty and the knife stays in her belt; {NOSMILE}",
         zh="中景、固定（2026-11-08 真人版 fix1 視線重拍：原本慢推，兩支秦霜都在笑、臉朝鏡頭，一支柴刀從手上跳到背後）：秦霜側臉朝畫左、面向畫外左邊的許硯，鏡頭偏離她的視線約 40°，眼睛看他、不看鏡頭；兩手空著，柴刀一直插在腰帶右邊；冷臉：眉往下壓、平，眼睛瞇起發硬，嘴抿緊；說完轉身往右邊籬笆走兩步，停下，回頭斜眼看許硯，眼睛瞇起、一邊眉挑起像在下戰帖；從頭到最後一格都不笑（NOSMILE）"),
    dict(loc="yard_pm", cam="Medium close-up to close-up, slow push in", chars=["xuyan"], night="yard_pm",
         comp="medium close-up, closing in to a close-up by the end, of Xu Yan, his sleeves rolled up and sweat on his forehead, his face earnest: brows set straight, eyes fixed and direct, jaw firm, no grin, his eyes on Qin Shuang off screen right; behind him only the woodpile of the same yard",
         lines=[("xuyan", "好，一言為定。三天後，妳自己來看我賺的錢。", "認真")],
         motion="he tosses the half log back onto the woodpile, dusts off his palms and straightens up to face her, and on 「一言為定」 he gives one slow resolute nod, his eyes never leaving hers",
         zh="近景反打、慢推（中近景推到近景）：許硯把半截木柴丟回柴堆，拍掉木屑，直起身看秦霜；認真、不笑。表情（2026-11-08 真人版）：眉毛定住、眼睛直直看著她、下巴收緊，不咧嘴；說「一言為定」時慢慢點一下頭，眼睛不離開她"),
    # ---- scene 3: Qian Yuanwai at the gate, late afternoon, the sun low in the west (light from the gate on the right).
    # Axis: the Xu side on screen left; Qian and the four servants in from the gate, on screen right.
    dict(chapter="錢員外", loc="yard_late", cam="Full shot, tracking", chars=["xiaohe"], night="yard_late",
         comp="full shot past the yard gate in the foreground, little Xiaohe, frightened: face pale, eyes wide, brows drawn up, no smile, one wooden bucket half full of water in her right hand, her small straw rabbit tucked into her sash; far out on the road beyond the gate a distant group of blurred figures in Song-dynasty clothing, too far off for any face to be seen",
         lines=[("xiaohe", "哥！錢員外帶著好多人，往我們家來了！", "慌，喘")],
         motion="Xiaohe carries the bucket to the gateway and looks out; her eyes go wide and her mouth drops open in fright; the bucket drops with a thump and water splashes, and she turns and runs back into the yard toward screen left, panting, her brows drawn up in fear",
         zh="全景、跟拍（先往右再往左）、前景院門：小禾提半桶水走到院門口往外看，水桶「咚」地丟在地上、水濺出來，轉身往左跑回院子；門外大路上遠遠一群人影（虛焦）。表情（2026-11-08 真人版）：臉色發白、眼睛睜大、眉頭往上皺；往外一看嚇得張嘴，跑回來時喘著、眉頭皺著，不笑"),
    # e902 live fix1 (2026-11-08): both seeds laughed warmly into the lens (the villain played friendly, as Zhao in e001),
    # with six to eight servants and the villagers inside the yard. Locked, his body three-quarter toward Xu Yan off
    # screen left; his face only QIAN_FACE and NOSMILE (no smile, smirk or sneer word); exactly four servants.
    # fix1: the set line is the short yard_late_m (the gate on screen right) so the prompt stays under 1000 characters.
    dict(loc="yard_late_m", cam="Full shot, locked", chars=["qianyuanwai"], night="yard_late",
         comp=f"full shot past the bamboo fence and the shoulders of {VILL} in the foreground, the villagers staying outside the fence; Qian Yuanwai on screen right stepping in at the yard gate, turned three-quarter to screen left toward Xu Yan off screen left, the camera about 35 degrees off his eyeline, three gold rings on his right hand, {FAN} in his right hand, {QIAN_FACE}; behind him exactly four grey-clad servants seen only from the shoulders down, in {SERV}, faces out of frame",
         lines=[("qianyuanwai", "許秀才，聽說你從河裡爬回來了，命真大啊。", "拖長音，油滑")],
         motion=f"fanning himself slowly, Qian Yuanwai steps over the threshold into the yard and drawls to Xu Yan off screen left in three-quarter profile, eyes on him, never into the lens, his lips closing between phrases, the corners of his mouth pulled down, his eyes cold and hard, his brows lowered, no teeth, never laughing; on 「命真大啊」 one eyebrow climbs; {NOSMILE}; exactly four servants file in behind him and stand in a row; the villagers stay outside the fence and shrink back",
         zh="全景、固定、前景籬笆與村民肩膀（布包頭）（2026-11-08 真人版 fix1：兩支錢員外都面向鏡頭和氣大笑，反派演成好人；家丁六到八個；村民跑進院子）：錢員外（深金色團花錦袍、三枚金戒指、素面摺扇）搖著扇跨進院門，身體與臉四分之三側向畫左、朝畫外左邊的許硯，鏡頭偏離他的視線約 35°，眼睛看許硯、不看鏡頭；剛好四個家丁、不多，只露肩膀以下跟進來排成一排；村民一直在籬笆外、往後縮。表情：臉只寫冷硬：嘴閉著、嘴角往下拉、眼睛瞇起又冷又硬、眉頭壓低，不露齒、不笑出聲，說「命真大啊」時一邊眉往上挑；從頭到最後一格都不笑（NOSMILE），不寫任何笑的字"),
    dict(loc="yard_late", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "qianyuanwai", "xiaohe"], night="yard_late",
         comp="over-the-shoulder shot from behind Qian Yuanwai's shoulder and his folding fan in the right foreground, Xu Yan facing the camera on screen left, his robe dry, his sleeves rolled up, holding back his anger: jaw clenched, brows pulled down hard, eyes narrowed and fixed on Qian, nostrils flared, no smile, little Xiaohe running up behind him",
         lines=[("xuyan", "錢員外，欠你的錢我記得，不必帶這麼多人來。", "壓著火")],
         motion="Xu Yan reaches back, pulls Xiaohe behind him and steps forward to shield her; his lips pressed thin between words; Xiaohe grabs the hem of his robe and peeks out, her eyes wide and frightened, her brows drawn up, her lips closed",
         zh="過肩（錢員外肩後拍許硯）、慢推：許硯伸手把小禾拉到身後、往前一步擋住；小禾抓住他的衣角。表情（2026-11-08 真人版）：許硯壓著火：咬緊牙、眉往下壓、眼睛瞇起盯著錢員外、鼻翼張開，說話之間嘴抿成線，不笑；小禾從他身後探頭，眼睛睜大、眉頭往上皺、害怕"),
    # e902 live fix1 (2026-11-08): both seeds laughed with open teeth from start to end and neither was low (one also
    # grew a black object beside the fan). The camera low below his chin looking up, locked, his body three-quarter toward
    # Xu Yan off screen left; QIAN_FACE and NOSMILE, no smile or sneer word (his picture is neutral: the words did it).
    dict(loc="yard_late", cam="Low-angle close-up, locked", chars=["qianyuanwai"], night="yard_late",
         comp=f"low-angle close-up of Qian Yuanwai, the camera low below his chin looking up at him, his body and face turned three-quarter to screen left toward Xu Yan off screen left, the camera about 35 degrees off his eyeline, {QIAN_FACE}, his lips pressed thin, his chin jutting, no teeth, the open folding fan with its blank face in his right hand, nothing else in his hands; behind him only the yard gate and the autumn tree of the same yard",
         lines=[("qianyuanwai", "本錢二十兩，月息三分，今天先把利錢交出來。", "冷笑")],
         motion=f"he snaps the fan shut with his right hand and taps it twice on his left palm, then his left hand draws one loan note folded into a long strip from his right sleeve and flicks it at Xu Yan off screen left, its plain blank back facing outward; he speaks to Xu Yan off screen left in three-quarter profile, eyes on him, never into the lens, his lips thin and closing between words, the corners of his mouth pulled down, no teeth, his eyes hardening and his chin jutting forward on 「利錢交出來」; {NOSMILE}",
         zh="低角度近景、固定（2026-11-08 真人版 fix1：兩支錢員外從頭到尾和氣地露齒大笑，也不是低機位；一支最後手上多一個黑色物件）：鏡頭在他下巴下方往上拍；身體與臉四分之三側向畫左、朝畫外左邊的許硯，鏡頭偏離他的視線約 35°，眼睛看許硯、不看鏡頭；右手收扇、敲兩下左手心，左手從右袖抽出摺成長條的借據一抖（背面朝鏡頭），手上只有扇子和借據。表情：嘴閉緊抿薄、嘴角往下拉、眼睛瞇起又冷又硬、眉頭壓低、下巴往前頂，不露齒；說「利錢交出來」時眼神一硬、下巴往前一頂；從頭到最後一格都不笑（NOSMILE），不寫任何笑的字"),
    # fix3 redesign: from behind the Xu side (nospeak): Tang Xiaotang is seen only from the back, so her garment front and
    # her smile (both drafts: open neckline, chest wrap, smiling) are out of sight; Qian Yuanwai faces the camera by the gate.
    dict(loc="yard_late_m", cam="Medium shot, tracking", chars=["tangxiaotang", "xuyan", "qianyuanwai"], nospeak=["tangxiaotang"], night="yard_late",
         comp=f"medium shot from behind the Xu side: Xu Yan at the left of the foreground seen from behind, his sleeves rolled up; Tang Xiaotang at the left edge seen from behind the whole shot, the back of her head with its two looped buns and pink ribbons toward the camera, her face turned away toward Qian Yuanwai the whole shot, {TANG}, the small gold abacus on her left palm in front of her; in the background on screen right by the yard gate Qian Yuanwai facing the camera in his dark gold silk robe, {FAN} closed in his right hand, {IOU} pinched in his left hand, eyes narrowed, lips closed",
         lines=[("tangxiaotang", "月息三分？員外這筆帳，算得也太狠了吧。", "精明")],
         motion="Tang Xiaotang walks in from the left, flicking the abacus beads with her right forefinger, her right elbow moving with each flick, and stops at Xu Yan's right; she tilts her head up toward Qian Yuanwai; Xu Yan stands still; on 「太狠了吧」 Qian Yuanwai's brows lower, his eyes narrow and his jaw tightens, his nostrils flaring, his lips staying closed",
         zh="中景、跟拍（fix3 重設計：從許家這一邊的背後拍，唐小棠整鏡只見後腦與背、說話不露嘴；兩稿都是低胸開襟又在笑）：唐小棠撥著算盤從左走進來、站到許硯右邊，抬頭看錢員外；背景右邊院門旁的錢員外面向鏡頭，右手合扇、左手捏摺成長條的借據（背面朝鏡頭）、嘴閉著。表情（2026-11-08 真人版）：錢員外聽到「太狠了吧」眉往下壓、眼睛瞇起、下巴一緊、鼻翼張開，嘴閉著"),
    # e902 live fix1 (2026-11-08): one seed had the right contempt for 2 s and then laughed openly, the other smiled
    # into the lens. Locked, his body three-quarter toward Tang Xiaotang off screen left; his eyes travel down her;
    # QIAN_FACE and NOSMILE, no sneer word.
    dict(loc="yard_late", cam="Reverse close-up, locked", chars=["qianyuanwai"], night="yard_late",
         comp=f"reverse close-up of Qian Yuanwai, his body and face turned three-quarter to screen left toward Tang Xiaotang off screen left, the camera about 35 degrees off his eyeline, contemptuous: chin raised, eyelids half lowered as he looks down his nose at her, {QIAN_FACE}, the closed fan in his right hand and the folded loan note in his left hand with its plain blank back toward the camera; behind him only the yard gate of the same yard",
         lines=[("qianyuanwai", "男人算帳，輪不到妳這個丫頭來插嘴。", "輕蔑")],
         motion=f"he smacks the closed fan once onto his left palm, and his half-lidded eyes travel slowly down Tang Xiaotang off screen left, from her silk sleeves down to her shoes, with open contempt; he speaks to her in three-quarter profile, eyes on her, never into the lens, his lips thin and closing between words, the corners of his mouth pulled down, no teeth, with a scornful huff through his nose; {NOSMILE}",
         zh="反打近景、固定（2026-11-08 真人版 fix1：一支 0–2 秒垂眼斜看的輕蔑是對的，2.5 秒起開口大笑；另一支正面對鏡頭笑）：錢員外身體與臉四分之三側向畫左、朝畫外左邊的唐小棠，鏡頭偏離他的視線約 35°，眼睛看她、不看鏡頭；扇子啪地敲左手掌心（借據捏在左手），半垂的眼睛從唐小棠的袖子慢慢往下打量到鞋。表情：下巴抬起、眼皮半垂從鼻尖往下看，嘴閉著、嘴唇薄、嘴角往下拉，眼神冷硬、眉頭壓低，不露齒，鼻子哼一聲；從頭到最後一格都不笑（NOSMILE），不寫任何笑的字"),
    dict(loc="yard_late", cam="Insert close-up, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="yard_late",
         comp="insert close-up of Tang Xiaotang's hands and the small gold abacus, the shot opens directly on the abacus from its very first frame: the palm-sized abacus with its gold frame and wooden beads on her left palm, her right forefinger on the beads, the cuffs of her peach-pink brocade sleeves; only the hands, sleeves and abacus are in the frame, her face out of the frame above, her ruqun one closed garment from the high collar to the waist",
         lines=[("tangxiaotang", "大衡律只准兩分，多收的那一分，按律全要退。", "畫外，又快又脆")],
         motion="her right forefinger clicks the beads up row after row in quick snaps, and the last bead stops with one sharp click; no mouth is in the frame",
         zh="算盤特寫、慢推（第一格就是算盤）：唐小棠右手食指噼啪撥珠，一排一排推上去，最後一顆「嗒」地停住；只拍手，沒有嘴"),
    # fix3 redesign: Qian Yuanwai alone (Tang Xiaotang's shoulder removed), knees up, the villagers soft behind the fence;
    # three beats only: glance back, the fan taps the palm once, one step forward; the note one folded strip.
    dict(loc="yard_late_m", cam="Medium shot, slow push in", chars=["qianyuanwai"], night="yard_late",
         comp=f"medium shot of Qian Yuanwai standing alone in the yard in front of the bamboo fence, framed from the knees up with space above his head the whole shot, facing the camera just right of center, portly in his dark gold silk robe with roundel patterns, three gold rings on his right hand, teeth gritted, jaw clenched, brows drawn down, unsmiling the whole shot; {FAN} closed in his right hand; {IOU} pinched in his left hand; beyond the fence behind him three {VILL} whispering to one another, only their upper bodies above the fence, soft and out of focus",
         lines=[("qianyuanwai", "好，利錢算我不要。本錢二十兩，一文都不能少。", "咬牙")],
         motion="his face darkens, his cheek twitching and his nostrils flaring; he turns his head and glances back over his shoulder at the whispering villagers, turns back with a hard glare, taps the closed fan once against his left palm beside the loan note, and takes one step forward; the loan note stays folded in his left hand to the end",
         zh="中景、慢推（fix3 重設計：拿掉唐小棠的肩，只拍錢員外一人、膝蓋以上；籬笆外三個村民虛焦）：錢員外臉一沉，回頭瞄一眼籬笆外交頭接耳的村民，轉回來用合起的扇子在左手掌心敲一下，往前跨一步；借據摺成長條捏在左手、背面朝鏡頭；咬牙、不笑。表情（2026-11-08 真人版）：臉一沉、臉頰一抽、鼻翼張開，轉回來狠狠瞪一眼"),
    # e902 live fix1 (2026-11-08): both seeds had her smile into the lens for 0-4.5 s and say 「我嫁你」 smiling ("turns
    # to face him squarely" turned her to the lens). One shot still (a split adds a 42nd id that the live stage-1, the
    # picks and the cut do not carry): a side two-shot, she in profile toward him the whole shot; NOSMILE.
    dict(loc="yard_late", cam="Two-shot, locked", chars=["xuyan", "tangxiaotang"], night="yard_late",
         comp=f"two-shot from the side, both faces in profile toward each other, nobody facing the lens: Xu Yan on screen left in three-quarter profile facing screen right, his sleeves rolled up to the elbows and sweat on his forehead, and Tang Xiaotang on screen right framed from the chin up, her high stand-up collar closed at her throat, {TANG}, in profile facing screen left toward Xu Yan the whole shot, her brows drawn together, her lips pressed, her jaw set",
         lines=[("xuyan", "二十兩……我現在一文也拿不出來。", "咬牙"), ("tangxiaotang", "許硯，我改主意了。我嫁你，現在就嫁。", "爽快")],
         motion=f"first Xu Yan, jaw clenched, his brows knotted and his eyes strained, looks to Qian Yuanwai off screen right and spreads his empty hands while her lips stay closed; then Tang Xiaotang, her head in profile toward him the whole shot, flicks her eyes to the road past the gate for an instant, her eyes widening, bites her lip, hangs the abacus back at her waist and looks straight into his face, chin up, brows set, jaw set, her eyes bright and direct on him, never into the lens, her lips pressed between words, a brisk decisive nod on 「現在就嫁」, while his brows shoot up in surprise and his lips stay closed; {NOSMILE}",
         zh="雙人鏡、側面、固定（唐小棠下巴以上，長鏡買 10 秒；2026-11-08 真人版 fix1：兩支唐小棠 0–4.5 秒正面對鏡頭微笑、8.5 秒笑著說「我嫁你」。審稿建議拆成兩鏡，但拆鏡會多出第 42 個鏡號，真人版的 stage 1、挑片表與剪接都對不上，這輪仍是一鏡）：兩人側臉相對、沒有人面向鏡頭；先是許硯四分之三側臉朝畫右，咬牙看畫外的錢員外、攤開空手說話；接著唐小棠整鏡側臉朝畫左面向許硯，眼睛往院門外的大路一瞟、一睜，咬嘴唇，把算盤掛回腰間，直視他的臉說話，不看鏡頭。表情：許硯咬牙、眉頭打結、眼神吃力；唐小棠下巴抬起、眉毛定住、下巴收緊、眼睛發亮直視他，字句之間嘴抿著，說「現在就嫁」時乾脆點一下頭；許硯聽了眉毛一揚、愣住；從頭到最後一格都不笑（NOSMILE）"),
    dict(loc="yard_late", cam="Extreme close-up, slow push in", chars=["xuyan"], night="yard_late",
         # e902 live fix1 (2026-11-08): the blue-light phrase drew glowing blue irises in both seeds; one was a frontal
         # face, the other laid a second full-length Xu Yan over the frame from 2.0 s (double exposure). EYES, the eyes
         # only, the eyeline slightly right, one person once.
         comp=f"extreme close-up of Xu Yan's eyes only, the shot opens directly on his eyes from its very first frame and the frame never widens: his two eyes and brows fill the frame, {EYES}, his eyeline slightly to screen right, never into the lens; nothing else in the frame, one face only, no second figure, no double exposure",
         lines=[("xitong", "叮。唐小棠，同意成婚，待蓋印。", "冷淡，叮一聲")],
         panel=[("唐小棠：同意成婚（待蓋印）", "panel")],
         motion="his eyes widen and his brows shoot up in disbelief, and he blinks once, slowly, the frame holding only his eyes and brows to the last frame",
         zh="眼睛大特寫、慢推（第一格就是眼睛，整鏡只有兩隻眼睛與眉毛、不拉遠）：虹膜是自然深褐色、瞳孔裡只有一點很小的反光（2026-11-08 真人版 fix1：原寫「瞳孔映淡藍光」，兩支虹膜亮藍，一支是正面整張臉，一支 2.0 秒後疊出另一個許硯全身），視線偏畫右、不看鏡頭，只有一張臉、沒有分身、沒有疊影；眼睛睜大、眨一下（周圍的聲音變小，面板剪接時疊上）。表情（2026-11-08 真人版）：眼睛睜大、眉毛一揚，不敢相信"),
    dict(loc="yard_late_cu", cam="Medium close-up to close-up, slow push in", chars=["tangxiaotang", "xuyan"], night="yard_late",
         comp=f"medium close-up, closing in to a close-up by the end, of Tang Xiaotang framed from the chin up, her high stand-up collar closed at her throat, {TANG}, frightened: face pale, eyes wide, brows lifted and drawn together, lips trembling, no smile the whole shot; at the left edge of the frame only Xu Yan's ear and a little of his hair; nobody else is in the frame; behind her only the bamboo fence",
         lines=[("tangxiaotang", "別誤會。我在躲一個人，他比錢員外可怕得多。", "很輕，第一次露出害怕")],
         motion="she rises on tiptoe to his ear and shields her mouth with one hand, her eyes darting out toward the gate and back, her brows pinched with fear and her throat bobbing as she swallows",
         zh="近景、慢推（中近景推到近景，下巴以上）：唐小棠踮腳湊到許硯耳邊、手擋著嘴，眼神往院門外飄一下又收回；臉色發白、害怕。表情（2026-11-08 真人版）：眉頭因害怕擠在一起、喉嚨一動嚥口水"),
    # e902 live fix1 (2026-11-08): the gaze was right in both seeds, but both smiled warmly (one with teeth at 4.0 s).
    # Locked, in profile toward her off screen right, the camera ~40 degrees off his eyeline; grave, NOSMILE.
    dict(loc="yard_late", cam="Reverse close-up, locked", chars=["xuyan"], night="yard_late",
         comp="reverse close-up of Xu Yan in profile facing screen right toward Tang Xiaotang off screen right, the camera about 40 degrees off his eyeline, his sleeves rolled up, grave and protective: brows drawn together, eyes softening with concern, jaw firm, lips pressed between phrases, his eyes on her, never the lens; behind him only the eaves of the house of the same yard",
         lines=[("xuyan", "好，我不問。妳嫁進許家，就是許家的人。", "低聲")],
         motion=f"he looks at her pale face, gives one single slow nod, and leans a little toward her, lowering his voice, his face in profile toward her, his eyes on her, never into the lens, his brows drawn together, his jaw firm, his lips pressed between phrases; {NOSMILE}",
         zh="反打近景、固定（2026-11-08 真人版 fix1：兩支視線都對，但都是溫暖的微笑，一支 4.0 秒還露齒）：許硯側臉朝畫右、面向畫外右邊的唐小棠，鏡頭偏離他的視線約 40°，眼睛看她、不看鏡頭；看著她發白的臉，慢慢點一下頭，側身壓低聲音。表情：凝重、護著她：眉頭皺在一起、眼神放軟帶著擔心、下巴收緊，字句之間嘴抿著；從頭到最後一格都不笑（NOSMILE）"),
    # fix3 redesign: three named people only (Qin Shuang's hand and A-ling move out: Qin was drawn twice, her knife came out
    # drawn); Tang Xiaotang peeks from behind Xu Yan so his shoulder hides her mouth; the note goes to a servant's hand
    # reaching in at the right edge (the drafts gave it to a woman).
    dict(loc="yard_late_m", cam="Medium full shot, slow push in", chars=["xuyan", "tangxiaotang", "qianyuanwai"], night="yard_late",
         comp=f"medium full shot, exactly three people, each framed from the knees up with space above their heads: on screen left Xu Yan facing right, his sleeves rolled up and sweat on his forehead, grim: brows drawn together, lips pressed; Tang Xiaotang standing close behind him, frightened, peeking past his shoulder, his shoulder covering her mouth and chin the whole shot, only her wide eyes, her brows and her looped buns showing, {TANG}; on screen right Qian Yuanwai facing left, {FAN} closed in his right hand, {IOU} pinched in his left hand; behind them only the bamboo fence and the yard gate",
         lines=[("qianyuanwai", "許秀才拿不出二十兩，那就拿人來抵！", "翻臉，狠")],
         motion="Qian glares at Xu Yan, his brows slammed down and his eyes hard and bulging, while Xu Yan pats his empty sleeve pocket with his lips closed, his jaw clenching and his nostrils flaring; Qian's upper lip curls back from his teeth in a vicious sneer, not a smile, and he holds the loan note out to his right, where one grey-clad servant's hand in a grey coarse cotton cuff reaches in from the right frame edge and takes it; Qian jabs the fan at Tang Xiaotang, and she shrinks lower behind Xu Yan's shoulder, her eyes going wider with fear",
         zh="中全景、慢推（fix3 重設計：只留三個有名字的人；秦霜的手與阿令移出本鏡——兩稿秦霜出現兩次、柴刀出鞘；唐小棠躲在許硯身後，只露眼睛與丸子頭，嘴被他的肩擋住）：錢員外瞪許硯；許硯摸空袖袋、嘴閉著；錢員外冷笑，左手把摺成長條的借據往右遞，右邊緣伸進一隻灰布袖口的家丁的手接走；扇子往唐小棠一指，她往許硯身後縮。表情（2026-11-08 真人版）：錢員外翻臉：眉往下砸、眼睛瞪得又硬又凸，上唇往上掀露出牙、狠狠冷笑（不是笑）；許硯摸袖袋時咬牙、鼻翼張開；唐小棠眼睛睜得更大、害怕"),
    dict(loc="yard_late", cam="Medium shot, tracking", chars=["tangxiaotang"], night="yard_late",
         comp=f"medium shot, one grey-clad servant with his back to the camera in a grey coarse cotton cross-collared short jacket, a cloth head-wrap and cloth shoes, his face never seen, and Tang Xiaotang facing the camera, {TANG}, panicked: face pale, eyes wide, brows lifted and drawn together, mouth open in a cry, no smile the whole shot",
         lines=[("tangxiaotang", "放手！你這雙髒手，別碰我的袖子！", "掙扎，驚叫")],
         motion="the servant strides up, grabs her left forearm with his right hand and drags her toward the gate on screen right, her wrist never bent backward; she leans back and struggles, her eyes blazing with fear and disgust, her nose wrinkled, her heels dragging two furrows through the dirt",
         zh="中景、跟拍（往右，院門方向）：家丁背影抓住唐小棠的左前臂往院門拖（手腕不反折）；她往後掙、腳跟拖出兩道痕（剪在掙到一半）。表情（2026-11-08 真人版）：唐小棠眼睛又怕又嫌惡、皺起鼻子"),
    # fix3 redesign (third failure: a hand always carried the knife in): an insert of the gate post, the knife alone,
    # arriving and burying itself in the post's left face (e003 s01 opens on that state). The cut ends while it is still
    # in the air, as the script says; the thunk opens e003.
    dict(loc="yard_late_cu", cam="Insert close-up, locked", chars=[], night="yard_late", act=3,
         comp="insert close-up of the upright wooden post of the yard gate, the shot opens directly on the post from its very first frame: the weathered post stands in the right half of the frame, its left face catching the low golden light; the left half of the frame is empty sunlit air with only the out-of-focus bamboo fence of the same yard behind it; the frame holds only the post, the fence and the knife",
         lines=[],
         motion=f"{KNIFE} comes spinning in alone from the left frame edge, end over end through the empty air, and its blade tip drives into the left face of the post at chest height with a thunk, the front third of the blade buried deep and the handle jutting out toward screen left, quivering",
         zh="門柱插入鏡、固定（fix3 重設計，第三次失敗：三輪都是一隻手拿著刀伸進畫面）：第一格就是院門門柱，左半邊是空的；柴刀自己從左邊緣翻轉飛進來，刀尖「篤」地釘進門柱左面、刀柄朝左顫動。剪接收在柴刀還在半空（釘進去之前），「篤」接第 3 集 s01；家丁與唐小棠留在 s39"),
]

HEAD = [
    "- 重製版 r2：照 `docs/videos/zhong-tian-qu-qi-e002-r2/script.md`（c01–c40 對應 s01–s40，c13b 對應 s13b；含「2026-11-06 審稿後的修改」）；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。",
    "- 內部工作編號 902（`hailuo/*-dh-e902.json`、`colab/runs/e902/`）；發布 slug `zhong-tian-qu-qi-e002-r2`。不放集數、不放片名卡；c01 直接接第 1 集 c38。",
    "- 狀態：許硯第一場半乾袖口濕、c03 起捲紅紙插腰帶左邊，第二場起衣服已乾、袖子捲到手肘、額頭有汗；阿令 c01 卸下鐵鐐，之後袖子蓋住手腕的紅勒痕；秦霜的舊柴刀在腰帶右邊（c17 抽出、c21 插回、c38 按住、c40 飛出）；借據摺成長條、背面朝鏡頭。",
    "- fix3（2026-11-07，最後一輪，重設計不改字）：s06、s10、s16–s18、s20–s22、s30、s33、s38、s40 換鏡頭設計；跟稿子不同的地方：s17 柴刀在畫外已抽出、s21 在畫外已插回、s18 不轉刀；s10、s22、s30 說話的人背對鏡頭（nospeak）；s20 地上的木頭與斧頭留在畫外；s33 拿掉唐小棠的肩；s38 只留許硯、唐小棠、錢員外（秦霜的手與阿令移出，借據交給右邊緣伸進來的家丁的手）；s40 拍門柱插入鏡、柴刀釘進門柱，剪接收在釘進去之前。",
    "- 2026-11-08 真人版表情（第 1 集真人版表情審查、`storyboard-brief-for-planners.md` 第 5 項）：每個露臉的人每一鏡都寫表情，寫成眉、眼、嘴角、下巴、喉嚨、呼吸，寫在那句台詞的時刻；不是開心的笑寫「不是開心的笑」；秦霜冷、阿令戒備照劇本，但也寫成具體的臉。台詞、走位、鏡位、道具、連戲與秒數都沒改。",
    "- 2026-11-08 真人版 fix1（第 2 集真人版挑片 `colab/runs/e902-live/review-picks.tsv` 的 12 支 RETAKE：s05、s11、s13、s16、s19、s24、s27、s29、s31、s34、s35、s37）：照第 1 集 fix6／fix7，說話的單人鏡改成固定、鏡頭偏離視線 30–45°、四分之三側臉或側臉朝對方，s11、s34 改成側面雙人鏡；不能笑的臉除了 NOSMILE 那一句不寫任何笑的字；錢員外（s27、s29、s31）的臉只寫嘴閉著、嘴角往下、眼神冷硬、眉頭壓低（QIAN_FACE）；s13、s35 的眼睛改用 EYES（自然深褐虹膜）、只拍眼睛；s19 秦霜不碰斧頭、用柴刀劈開；s27 剛好四個家丁、s29 低機位。s34 這輪不拆鏡。",
    "- 長鏡要買的秒數（`r2.py` 的 BUY）：s34 10 秒（script.md 長鏡清單）；s03 8 秒（時間線 6.8 秒，超過預設 6 秒）。其餘照 `gen-dh` 的 5／6 秒。",
]
FOOT = [
    "- 場景參考：整集都在院子 `set-xujia-yuan-t1`；三種光：近午頂光（誰肯嫁）、午後右側斜光（柴堆）、日頭偏西的低光（錢員外）。近景背景都寫「同一個院子」。",
    "- 唐小棠一律用 `tangxiaotang-portrait-t2`（gen-dh 的 PORTRAIT 對照）；近景構圖寫「下巴以上」，中景以上寫「襦裙從立領到腰一件闔上」。",
    "- 灰衣家丁與村民沒有定妝照：家丁只拍背影、肩膀以下或手（灰色交領粗布短褐、布包頭、布鞋、兩手空空）；村民只在籬笆外露上半身（宋式交領短打、布包頭）。",
    "- 阿令沒戴鐵鐐的定妝照：`aling-portrait-t1` 本身沒有鐵鐐，照用；鐵鐐只在 s01 開鎖前出現。",
    "- 配樂：誰肯嫁 comedy 輕段（s13b 抽掉留冷的「嘀」）、柴堆 comedy（s19 劈開一個重音）、錢員外 tension（s35「叮」抽掉留重音）、s40 換 suspense 停在柴刀半空；音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy so the lines fit without slowing past 1.1x (script.md 長鏡清單: c34 10 s;
# the others from the builder's timeline, any shot longer than the default 6 s).
BUY = {"s03": 8, "s06": 8, "s27": 10, "s29": 10, "s30": 8, "s33": 10, "s34": 10, "s38": 8}  # s06, s27-s38: the recorded lines run longer than 6 s (錢員外 speaks slowly)
