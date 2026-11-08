"""Episode 1 remake (r2): the writer spec for build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e001-r2/script.md (c01-c38 = s01-s38).

Rules from camera-feel-study-20261105 and motion-quality.md §2: every shot has one visible action written as a path
(start, wind-up, weighted main move, settle); dialogue shots are over-the-shoulder or reverse shots with the eyes on the
other person; whole sentences, one line per shot; default face is serious, smiling only where the script says so.

2026-11-05 rewrite to the eleven-item storyboard (script.md): costume, props, who is where, everyone's action, the state
(Xu Yan soaked c04-c11, half-dry with damp sleeves from c12; A-ling in iron shackles; Erniu empty-handed), the paper
written as its blank back, who leaves the frame (c12, c15, c20, c32), one camera move. Line emotions stay as recorded
(the voice cache keys on them; script.md re-records c29 only).
"""
EP = 901  # internal working number; the published slug is zhong-tian-qu-qi-e001-r2 (build-r2.py)
EP_TITLE = "官差踹門送三個老婆（重製版 r2）"
OUTLINE_SECONDS = 220  # script.md: about 3 min 40 s, the sum of its shots' seconds
TARGET_MINUTES = [3, 4]
TITLE = "農學碩士穿越成窮秀才，官差踹門送來三個老婆｜種田娶妻打天下 第1集（重製版）"
DESCRIPTION = "面試官說：「種田的就別來了。」農學碩士許硯在雨夜被一道閃電劈進柳溪，醒來成了負債二十兩的窮秀才，腦子裡還多了一個「良緣系統」。王二牛把他從河裡拖上岸；家裡的妹妹小禾只剩半碗粥，錢員外的人說下次要把米缸搬走。近午，趙捕頭一腳踹開院門，帶著縣太爺的配婚令：二十五歲未婚，官府配妻三名，今日成親。許硯背出大衡律配婚第七條「三日為期」，逼得官差改口三天；被配來的是嘴硬的秦霜、戴鐵鐐的罪奴阿令，還有自己坐轎來的千金唐小棠。系統：任務，三日內與三人成婚——失敗，抹殺。《種田娶妻打天下》第 1 集（重製版）。"
THUMB = ("三個老婆", "s23")
CHARACTERS = ["xuyan", "mianshiguan", "erniu", "xiaohe", "zhaobutou", "qinshuang", "aling", "tangxiaotang", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: a cold tense pulse in the rainy office and street; a soft misty bamboo flute at the river at dawn; a warm gentle guqin and soft strings inside the farmhouse; a bright playful comedy of woodblock, pipa and suona in the yard, dropping out to a single deep hit on each system chime, and a low suspense cello on the last look; ancient Chinese rural drama, no vocals"

# Scene headers of script.md: place, time and light, the axis (where the door, the gate, the river are).
LOC = {
    "office": "In a glass-walled modern office meeting room at night, a long glass table under cold white lights, the night city lights blurred out of focus beyond the dark windows",
    # inserts keep the set to one line so the wide room is not painted (e901 live fix2: s01 table top, s20 gate, s26 chain);
    # "meeting room" still picks the modern style and no set picture, "dirt yard" still picks set-xujia-yuan-t1
    "desk": "In a modern office meeting room at night, on a long glass table under cold white lights",
    "yardin": "In the dirt yard of the Xu farmhouse near noon on a clear autumn day, bright sunlight from overhead and slightly right",
    "street": "On a rain-soaked modern city street at night in heavy rain, wet asphalt reflecting the streetlights, sheets of rain falling under the streetlights",
    "under": "Under the murky green-brown water of the Liuxi stream at dawn, shafts of grey light from the surface above, silt drifting",
    "river": "On the reedy mud bank of the Liuxi stream at foggy autumn dawn, the shallow brown water on screen left and the mud bank on screen right, tall reeds, mist on the water, a dirt path to the village in the distance on screen right, cool grey light from behind on the left",
    "house": "Inside the poor thatched farmhouse of the Xu family on an autumn morning, earthen walls and a packed earth floor, the plank door on screen left, a big clay water vat on screen right, a clay rice crock in the corner by the back wall, a low table with two stools, clear morning light slanting in from the door and window on the left",
    # close-ups keep the set to one line (storyboard-shot-spec 近景被拍成全景); the wording still picks set-xujia-wu-t1
    "crock": "Inside the poor thatched farmhouse of the Xu family on an autumn morning, in the corner by the earthen back wall, soft morning light from the left",
    "yard": "In the dirt yard of the Xu farmhouse near noon on a clear autumn day, an autumn tree, a bamboo fence, a woodpile on screen left, the house door at the back left, the yard gate in the fence on screen right, a stone well at the back right, bright sunlight from overhead and slightly right casting short shadows",
}
LIGHT = {
    "river": "the cool grey dawn mist stays unchanged",
    "house": "the slanting morning light stays unchanged",
    "yard": "the bright near-noon sunlight stays unchanged",
}

# 2026-11-07 review (reshoot s02, s12, s13, s15, s16, s35): one identical phrase per prop and costume, every shot.
# Xiaohe's toy is a straw rabbit in her sash, never in her hands in this episode (cast.json says "hugging"; extras.json rewrites it).
RABBIT = "a small straw-woven rabbit, plaited from pale yellow straw, tucked into her waist sash"
XIAOHE = f"little Xiaohe in her patched lilac cotton jacket with red-string pigtails, {RABBIT}"
ROBE = "his blue-grey scholar's robe half-dry, the sleeves still damp"
CROCK = "one squat brown clay rice crock as high as a small child's knee, with one round flat wooden lid"
# 2026-11-07 live-action pick (e901-live review-picks.tsv): the rabbit moved into her hands, onto Xu Yan's belt and grew into
# a big doll on the floor (s12, s14), so the retakes say where it stays in one identical phrase.
RABBIT_STAYS = "the small pale-yellow straw rabbit stays tucked in the front of her waist sash from the first frame to the last"
# Qin Shuang's knife came out in her right hand in s23, s24 and s38 of the live drafts: one phrase for every shot where her
# belt is in the frame (the script never has her draw it in this episode).
KNIFE = "her old chopping knife tucked in the right side of her belt, where it stays from the first frame to the last"
# e901 live cut review (2026-11-08, item 19): s08b-s11 came out only damp. There was no shared phrase for the soaked state:
# each river shot said "soaked through" in its own words, against reference pictures of a dry robe that the live prompt
# says the costume keeps. One identical phrase in every river shot where his robe or hair shows (s05, s06, s08b-s11);
# live-action/pilot.py reads its first words and lets the costume go wet there.
SOAKED = "his blue-grey scholar's robe soaked dark through with river water, the heavy wet cloth clinging flat to his shoulders, chest and arms, water streaming from his sleeves, his hair dripping wet and plastered to his forehead and cheeks"
# e901 live cut review (item 2): "a faint pale blue light reflected in his pupils" drew solid glowing blue irises in s08 and
# s36. The eye extreme close-ups (system lines on recorded voice) keep natural eyes and at most a faint cold glint.
EYES = "his irises a natural dark brown from the first frame to the last, the whites of his eyes clear, only a tiny faint cold pale glint of reflected light in each pupil, like a catchlight"

SHOTS = [
    # ---- opening: the interview (night, rain). Axis: the interviewer on the right (only a hand), Xu Yan on the left facing right.
    # c01: the interviewer's portrait is the shot's only picture (ref2manifest needs one; the office has no set picture); only her hand is in frame.
    dict(chapter="面試", loc="desk", cam="Insert at table height, static", chars=["mianshiguan"], nospeak=["mianshiguan"],
         # live pick (2026-11-07) and fix1: her face and chin came into the frame above the table, the sheet ended face up
         # with printed lines, and another take only stroked the paper. Redesign (storyboard-shot-spec 同一鏡改字兩次還是錯):
         # an insert at table height of the table top alone, the hand coming in from the top edge (her side of the table) and
         # pushing the face-down résumé toward the camera, to the near edge, in one push. The frame ends at the table surface.
         comp="insert shot from just above table height, angled down onto the glass table top, the shot opens directly on this insert from its very first frame: the bare glass table surface fills the whole frame from edge to edge, the top edge of the frame on the far part of the table itself; one résumé lies face down near the top of the frame with its plain blank back up, a single sheet of white paper",
         lines=[("mianshiguan", "農學碩士？我們要的是會寫程式的，種田的就別來了。", "畫外，冷淡，不耐煩")],
         motion="one right hand in a charcoal-grey suit sleeve enters from the top edge of the frame, lays its flat palm on the face-down résumé and in one firm push slides it across the glass to the near table edge at the bottom of the frame; then the hand draws back out through the top edge",
         zh="桌面插入鏡、桌面高度、固定（第一格就是桌面；畫面上緣就是遠端桌面，桌面以上都在畫外）：履歷背面朝上、一張白紙；面試官一隻手（深灰西裝袖）從畫面上緣伸進來，手掌平按履歷一推，履歷朝鏡頭滑到近端桌邊，手從上緣收回，履歷仍背面朝上（面試官在畫外說話；2026-11-07 真人版第二輪挑片後改鏡頭設計）"),
    dict(loc="office", cam="Medium shot to medium close-up, slow push in", chars=["xuyan"], looks={"xuyan": "modern"},
         comp="medium shot, closing in to a medium close-up by the end, of Xu Yan in a dark modern suit, white shirt and dark tie, seated at the long glass table on screen left, facing right, the résumé face down on the glass in front of him with its plain back up, his eyes on the interviewer off screen right; he opens with a small polite smile that fades as he speaks, and from then on controlled anger: his jaw clenched tight, his brows drawn down and level, his eyes hard and unblinking, his lips pressed flat between words, no smile again to the end of the shot",
         lines=[("xuyan", "種田怎麼了？全世界的人，每天都要吃飯。", "壓著火，很穩")],
         motion="his polite smile fades as he speaks and his jaw sets hard; only then he draws the résumé back across the glass, squares it and folds it once, plants both palms, pushes his chair back and stands, his jaw still tight",
         zh="中近景、慢推（中景推到中近景）：許硯（現代西裝）開口時禮貌的笑慢慢收掉，變成壓著火（咬緊牙、眉壓低、眼神硬、之後不再笑）；然後才把履歷抽回來對齊摺好，推開椅子站起來（2026-11-07 審稿重寫）"),
    dict(loc="street", cam="Full shot from behind, tracking", chars=["xuyan"], looks={"xuyan": "modern"}, nospeak=["xuyan"],
         comp="full shot from behind of Xu Yan in his dark modern suit, soaked through, walking away from the camera down the middle of the wet street, rain streaks falling close across the foreground, the street otherwise empty",
         lines=[("xuyan", "算了，這些話說了也沒人聽。", "低聲自嘲")],
         motion="his heavy wet footfalls splash in the puddles as he walks and tugs his tie loose with one hand; he slows, stops and tilts his head back toward the sky, and a jagged bolt of lightning cracks down from the sky and floods the whole street white; he speaks with his back turned, his face never seen",
         zh="雨夜街道全景、從背後跟拍、前景雨絲：許硯（西裝濕透）邊走邊扯鬆領帶，停步抬頭，一道閃電劈下把整條街照白（台詞是背影，不對嘴）"),
    # ---- scene 1: Liuxi stream, first dawn. Axis: the river on the left, the bank and the village path on the right; Xu Yan left, Erniu to his right.
    dict(chapter="柳溪", loc="under", cam="Extreme close-up, slow push in", chars=["xuyan"],
         comp="extreme close-up of Xu Yan's face under the murky green-brown water, the shot opens directly on his face from its very first frame, eyes closed, his long black hair loose and spreading around his face, the collar of his soaked blue-grey scholar's robe at the lower edge; behind him only murky water and drifting silt",
         lines=[("xitong", "良緣系統，綁定成功。", "冷淡，懶得理人，叮一聲")],
         panel=[("良緣系統綁定成功", "panel")],
         motion="his eyes snap wide open and his body jolts; a burst of silver bubbles rushes from his mouth and streams up toward the light, and one hand shoots up past his face clawing toward the surface, his hair whipping in the water",
         zh="水下大特寫、慢推：古裝的許硯在混濁綠褐色河水裡猛然睜眼，一串氣泡從嘴邊往上衝，手往上抓"),
    dict(loc="river", cam="Full shot, tracking", chars=["erniu", "xuyan"], night="river",
         comp=f"full shot through tall reeds in the foreground, Wang Erniu knee-deep in the shallow water, his coarse brown trousers soaked to the knees, both hands empty, bending over the limp Xu Yan, who lies half under the water, {SOAKED}",
         lines=[("erniu", "許秀才！你可別死啊，還有氣就給我咳出來！", "又急又喘")],
         motion="Erniu's big sun-tanned hand grabs the collar of Xu Yan's robe and heaves him up out of the water in a burst of spray; Erniu walks backward toward screen right with heavy dragging steps, hauling Xu Yan through the shallows and up onto the mud bank, and settles back on his heels, breathing hard",
         zh="全景、跟拍、前景蘆葦：一隻曬黑的大手揪住許硯的衣領往上拽，水花四濺；二牛（褲管濕、兩手空空）倒退著把他拖上泥岸，鏡頭跟著往右"),
    dict(loc="river", cam="High-angle close-up, slow push in", chars=["xuyan"], night="river",
         comp=f"high-angle close-up of Xu Yan lying on his back among flattened reeds on the mud bank, {SOAKED}, dazed; behind him only reeds and wet mud",
         lines=[("xuyan", "咳……這裡是哪裡？你又是誰？", "嗆咳，迷糊")],
         motion="his chest heaves; he rolls onto his side and coughs up a mouthful of water, braces one palm in the mud and pushes his upper body halfway up, then turns his head toward Erniu off screen right and squints",
         zh="俯拍近景、慢推：許硯仰躺在蘆葦裡，側身咳出一口水，撐起半個身子，轉頭看畫面右邊"),
    dict(loc="river", cam="Low-angle medium close-up, slow push in", chars=["erniu"], night="river",
         comp="low-angle medium close-up of Wang Erniu crouching on the mud bank on screen right, his face dripping with water, his trousers soaked to the knees, both hands empty, his eyes on Xu Yan off screen left",
         lines=[("erniu", "我二牛啊！這裡是柳溪，你半夜掉進河裡，差點把我嚇死。", "憨笑，鬆一口氣")],
         motion="he wipes the water off his face with the back of his hand, slaps his own chest once with a flat palm, lets out a big breath and breaks into a relieved grin",
         zh="低角度中近景、慢推：二牛蹲著，用手背抹掉臉上的水，拍一下胸口，鬆一口氣笑出來"),
    dict(loc="river", cam="Extreme close-up, slow push in", chars=["xuyan"], night="river",
         comp=f"extreme close-up of Xu Yan's eyes, the shot opens directly on his eyes from its very first frame, wet lashes and brows, {EYES}; nothing else in the frame",
         lines=[("xitong", "宿主許硯，柳溪村秀才。目前負債，二十兩銀子。", "冷淡，念到負債時帶一點嫌棄")],
         panel=[("宿主：許硯（秀才）／負債：二十兩", "panel")],
         motion="his eyes flick to the left, then to the right, then back again, searching the empty air for where the voice is coming from, and his brows slowly draw together, his lips remaining closed the whole time",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：濕髮貼在眼角，虹膜維持自然深褐色、瞳孔裡只有一點很淡的冷色反光（2026-11-08 真人版成片審查：原寫法畫成整個虹膜發藍光），許硯的眼睛左右轉、找聲音從哪來，眉頭皺起，嘴閉著（面板剪接時疊上；2026-11-06 審稿拆鏡，原片剪前 5 秒照用）"),
    # c08b (2026-11-06 review): split from c08; its own id keeps s09-s38 and the line ids unchanged.
    dict(sid="s08b", loc="river", cam="Medium close-up, slow push in", chars=["xuyan"], night="river",
         comp=f"medium close-up of Xu Yan sitting on the mud bank, {SOAKED}, looking down at himself; behind him only the reeds and the mist over the river; nobody else in the frame",
         lines=[("xuyan", "誰在說話？宿主……說的是我嗎？", "心裡話，困惑", "inner"), ("xitong", "本系統。宿主就是你，別東張西望。", "冷淡，嫌棄")],
         motion="Xu Yan looks down at his soaked scholar's sleeves, lifts both hands in front of him and slowly turns them over to stare at his palms, water dripping from the cuffs; his lips stay closed the whole time",
         zh="中近景、慢推（2026-11-06 審稿新鏡）：許硯坐在泥地上全身濕透，低頭看自己濕透的書生袖子，再把兩手翻過來看掌心，袖口滴水；身後只有蘆葦和河霧；兩句都嘴閉著"),
    dict(loc="river", cam="Medium close-up, slow push in", chars=["xuyan", "erniu"], night="river",
         comp=f"medium close-up of Xu Yan sitting on the mud bank on screen left, {SOAKED}, and only the shoulder and arm of Wang Erniu in his coarse brown jacket at the right edge of the frame, Erniu's face out of the frame",
         lines=[("xuyan", "二十兩……我是不是欠了誰的錢？", "試探")],
         motion="Xu Yan pushes himself upright with one palm in the mud, glances at the empty air in front of him, then turns his head to Erniu at the right edge; Erniu's shoulder shifts as he leans closer",
         zh="中近景、慢推：許硯（濕透）撐著地坐直，先看一眼面前的空氣，再轉頭看右邊只露肩膀的二牛"),
    dict(loc="river", cam="Over-the-shoulder medium close-up, locked", chars=["erniu", "xuyan"], night="river",
         comp=f"over-the-shoulder shot from behind Xu Yan's shoulder and the back of his head in the left foreground, {SOAKED}; Wang Erniu crouching and facing the camera on screen right, his eyes on Xu Yan",
         lines=[("erniu", "錢員外的啊。他說這個月再不還，就拿你家的地抵。", "壓低聲音")],
         motion="Erniu's grin fades; he glances back over his shoulder toward the village path off to screen right, turns back and hunches lower, leaning in close to Xu Yan; Xu Yan stays still, listening",
         zh="過肩（許硯肩後拍二牛）：二牛的笑收起來，回頭往畫面右邊村子的方向看一眼，再轉回來壓低身子"),
    dict(loc="river", cam="Full shot, slow push in", chars=["xuyan", "erniu"], night="river",
         comp=f"full shot through reeds in the foreground, Xu Yan on screen left, {SOAKED}, and Wang Erniu on screen right, his trousers wet to the knees, both hands empty, the misty dirt path to the village winding away into the distance on screen right; on screen left at the bank, one old straw-coloured straw hat with a torn corner on its brim hangs by a thin red cord from a wooden post, part of the background",
         lines=[("xuyan", "先回家吧。我總得知道，自己現在過的是什麼日子。", "吸一口氣")],
         motion="Xu Yan grips Erniu's shoulder and hauls himself to his feet, water dripping from his robe and sleeves; he steadies his weight, looks down the misty path toward the village on screen right and takes the first step along it, Erniu turning with him",
         zh="全景、慢推、前景蘆葦：許硯扶著二牛的肩站起來，衣服往下滴水，望向右邊遠處的村路，邁出第一步（左邊岸上木樁掛著一頂繫紅繩的舊草帽，不特別帶到）"),
    # ---- scene 2: the Xu farmhouse, first morning. Axis: the door on the left; Xu Yan enters from the left, Xiaohe by the water vat on the right.
    # live pick (2026-11-07): the rabbit came out of the ladle into her hands, one draft opened on two Xiaohes, and the
    # cry was not in the prompt. She now speaks it on screen (the cut uses the model's voice), written in the motion after
    # the ladle drops; nospeak only keeps build-r2.py from putting the speaking sentence first.
    dict(chapter="許家", loc="house", cam="Full shot, slow push in", chars=["xiaohe", "xuyan", "erniu"], night="house", nospeak=["xiaohe"],
         comp=f"full shot of the room: Wang Erniu stepping in through the half-open plank door on screen left, both his hands holding Xu Yan up, one arm round his back and one gripping his arm; Xu Yan, {ROBE}, leaning on him; on screen right by the water vat exactly one little Xiaohe, the same eight-year-old girl the whole shot, in her patched lilac cotton jacket with red-string pigtails, her back half turned to the door, one wooden ladle in her right hand from the very first frame and her left hand empty; {RABBIT_STAYS}",
         lines=[("xiaohe", "哥哥！", "愣住，然後哭出來")],
         motion="Erniu helps Xu Yan over the threshold on screen left; Xiaohe turns from the vat toward the door and freezes, eyes wide; only then the ladle drops from her hand and bounces once on the floor, and then little Xiaohe speaks a short Mandarin line, 「哥哥！」, her lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes, startled, about to cry",
         zh="屋內全景、慢推，木門在畫面左：二牛兩手扶著許硯（衣服半乾、袖子濕）跨進門檻，肩上背上什麼都沒有；水缸邊的小禾（只有一個、八歲；草編兔子一直塞在腰帶前面、手上只有木勺）轉向畫面左邊的門、愣住，然後木勺才從手裡掉下、在地上彈一下，她才張嘴喊「哥哥！」（對嘴；2026-11-07 審稿重寫，同日真人版挑片再改）"),
    dict(loc="house", cam="Two-shot, tracking", chars=["xiaohe", "xuyan", "erniu"], night="house", nospeak=["xiaohe"],
         comp=f"two-shot in the same bare farmhouse room as before, earthen walls and a packed earth floor, no bed: Xu Yan on screen left just inside the plank door, {ROBE}; {XIAOHE}, on screen right by the big clay water vat, her face crumpling, about to cry; at the door on screen left only the half of Wang Erniu's body in his coarse brown jacket, the rest outside",
         lines=[("xiaohe", "我以為你回不來了，我一個人找了你一整晚。", "哭腔")],
         motion="Xiaohe runs from the vat and throws herself into Xu Yan, hugging his waist with her face buried in his robe and hidden to the end, her shoulders shaking as she sobs into the cloth; he rocks back half a step; Erniu's lips stay closed",
         zh="雙人鏡、跟拍，同一間屋（沒有床），木門在畫面左：小禾（草編兔子塞在腰帶上）從水缸邊跑過來抱住許硯的腰、臉埋在他衣服裡一直看不到、肩膀發抖在哭（不笑）；許硯退半步；二牛在門口只露半身（2026-11-07 審稿重寫）"),
    # live pick (2026-11-07): one draft hung the rabbit on Xu Yan's belt and lost the hug; the other spoke from the first
    # second, then turned Xiaohe into a toddler and the rabbit into a big doll on the floor. Lips closed for four seconds,
    # then the line (written in the motion, so nospeak keeps build-r2.py from putting it first); one eight-year-old Xiaohe.
    dict(loc="house", cam="Close-up, slow push in", chars=["xuyan", "xiaohe"], night="house", nospeak=["xuyan"],
         comp=f"close-up of Xu Yan in his blue-grey scholar's robe, half-dry with damp sleeves, looking down, framed with clear space above his head so that his whole head stays inside the frame as he crouches; exactly one little Xiaohe, the same eight-year-old girl the whole shot, at the lower edge of the frame, her arms around his waist and her face pressed into his robe, {RABBIT_STAYS}; behind them only the earthen wall",
         lines=[("xuyan", "她叫我哥哥……原來這副身體，還有個妹妹。", "心裡話，愣住", "inner"), ("xuyan", "別哭了，哥哥回來了，哥哥在這裡。", "放軟")],
         motion="for the first four seconds his lips stay closed while he slowly crouches to her height, her arms still around him, his hand pausing above her head before it settles gently on her hair; only then Xu Yan speaks a short Mandarin line, 「別哭了，哥哥回來了，哥哥在這裡」, his lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes",
         zh="近景、慢推：許硯慢慢蹲到她的高度（小禾一直抱著他、只有一個、八歲；草編兔子一直塞在她腰帶前面），手在她頭頂上方停一下才輕輕摸下去；前四秒心裡話嘴閉著，然後才說「別哭了……」（2026-11-07 真人版挑片重寫；頭上留空）"),
    dict(loc="house", cam="Over-the-shoulder medium close-up, slow push in", chars=["xiaohe", "xuyan"], night="house",
         comp=f"over-the-shoulder shot from behind Xu Yan's damp shoulder in the left foreground, {XIAOHE}, both hands empty, facing the camera on screen right and looking up at him, frightened: her eyes red and wet, her brows drawn up in the middle, her lower lip trembling, no smile the whole shot; the plank door on screen left behind is empty, Wang Erniu off screen outside the door",
         lines=[("xiaohe", "錢員外的人今天又來過了，說下次要把米缸搬走。", "害怕")],
         motion="she lifts her tear-streaked face to him and wipes her eyes with her empty sleeve, then turns her head to glance at the rice crock in the corner by the back wall, her hands staying empty at her sides",
         zh="過肩（許硯肩後拍小禾）：小禾（草編兔子塞在腰帶上、兩手空空）眼睛紅、害怕、不笑，抬起臉用袖子擦眼睛，轉頭看後牆角的米缸（二牛已退到門外；2026-11-07 審稿：兔子不在手上）"),
    dict(loc="crock", cam="High-angle insert close-up, locked", chars=[], act=3,
         comp=f"high-angle insert close-up looking straight down into {CROCK}, the shot opens directly on this close-up from its very first frame with the wooden lid still on, a young man's hand in the damp cuff of a faded blue-grey cotton sleeve gripping the lid; only the hand, the sleeve and the crock are in the frame; under the lid the crock is almost empty: a thin layer of rice only just covering the very bottom, the bare brown clay bottom showing through in the middle, the rice far below the rim, the clay walls bare and dry",
         lines=[],
         motion="the hand lifts the wooden lid away out of the frame, showing the nearly empty crock; only then two fingers reach down to the bottom and stir the thin layer, and a few grains slide over the bare clay",
         zh="手部特寫、俯拍（第一格就是蓋著木蓋的米缸）：許硯的手（書生袍濕袖口）掀開木蓋，缸幾乎是空的：缸底只鋪一層薄米、中間露出陶土底、米離缸口很遠；然後手指才伸到缸底撥一下，幾粒米滑過陶土（2026-11-07 審稿重寫）"),
    dict(loc="house", cam="Medium close-up, slow push in", chars=["xuyan"], night="house",
         comp="medium close-up of Xu Yan standing beside the rice crock in the back corner on screen left, his robe half-dry with damp sleeves, the wooden lid in his hand, his eyes on the crock; behind him only the earthen wall and the rice crock in the corner",
         lines=[("xuyan", "都快見底了，還有什麼好搬的。小禾，家裡還有吃的嗎？", "苦笑")],
         motion="he lowers the wooden lid back onto the crock with a soft knock, lets out a long sigh that drops his shoulders, and turns his head with a rueful smile to Xiaohe off screen right",
         zh="中近景、慢推：許硯放下木蓋，嘆口氣、苦笑，轉頭看畫面右邊的小禾"),
    dict(loc="house", cam="Two-shot, slow push in", chars=["xiaohe", "xuyan"], night="house",
         comp=f"two-shot at the low table, Xu Yan seated on a stool on screen left, his robe half-dry with damp sleeves, and little Xiaohe on screen right holding one clay bowl half full of thin porridge in both hands, {RABBIT}; on the low table in front of Xu Yan already stands a second clay bowl, empty, so two clay bowls are on the table by the end",
         lines=[("xiaohe", "還有半碗粥，哥你先吃，我不餓。", "懂事")],
         motion="Xiaohe walks carefully from the stove with small steps so nothing spills, rises onto her tiptoes and pushes the bowl across the low table to Xu Yan with both hands, then settles back on her heels; Xu Yan looks from the bowl up to her, his lips closed",
         zh="雙人鏡、慢推：小禾雙手捧著半碗稀粥從灶邊小心走過來，踮腳把碗推到矮桌上他面前；矮桌上另放一個空陶碗（c19 倒粥用）"),
    dict(loc="house", cam="Close-up of the bowls, slow pull out to Xu Yan's close-up", chars=["xuyan"], night="house",
         comp="close-up of two clay bowls on the low table: right in front of Xu Yan on screen left his own clay bowl, filled with thin porridge; on the screen-right side of the table, set for Xiaohe off screen right, the second clay bowl, empty, its brown clay inside dry; widening to a close-up of Xu Yan seated behind them on screen left, his sleeves damp, little Xiaohe off screen right",
         lines=[("xuyan", "一人一半。從今天起，哥不會再讓你餓肚子。", "認真")],
         motion="Xu Yan lifts his own full bowl, tilts it over the empty bowl and pours half the porridge into it, so the second bowl now holds half; he sets his bowl down, slides the second bowl across the table to Xiaohe off screen right and lifts his eyes to her",
         zh="碗的特寫慢慢拉到許硯近景：開頭許硯面前是他那碗盛著稀粥的碗、桌子右邊小禾的位置是乾的空碗；許硯端起自己那碗，倒一半到空碗裡，放下自己的碗，把倒好的那碗推給畫面右邊的小禾，抬頭看她（2026-11-08 真人版成片審查：粥從空碗倒出來，寫清楚哪碗滿、哪碗空）"),
    # ---- scene 3: the yard, near noon. Axis: the Xu side (Xu Yan, Xiaohe, Erniu) on the left; Zhao and the brides come in by the gate on the right.
    dict(chapter="配婚令", loc="yardin", cam="Insert, static", chars=["zhaobutou"], nospeak=["zhaobutou"], night="yard",
    # live pick (2026-11-07) and fix1: nobody ever kicked the gate; it was pushed open toward the camera from the yard side
    # or left out, villagers stood inside the fence and the house sign grew writing. Redesign (同一鏡改字兩次還是錯): the
    # beat splits. This shot is only the kick, an insert of the shut gate from inside the yard; his boot and lower leg are all
    # of him on screen and his shout is off screen in the recorded voice (nospeak). His walk in is s21's opening; the
    # villagers and Xiaohe at the door leave the episode with the wide shot.
         comp="insert shot of the yard gate from inside the yard, the shot opens directly on this insert from its very first frame: the shut wooden yard gate of weathered grey planks fills the whole frame, a strip of the bamboo fence at each side, bright lane sunlight showing through the thin gaps between the planks",
         lines=[("zhaobutou", "許硯！縣太爺的配婚令，出來接令！", "粗聲")],
         motion="a hard kick from outside bursts the gate inward toward the foreground with a loud bang and it slams against the bamboo fence at the side; in the sunlit gap a black cloth boot and the hem of a black robe stamp down onto the threshold; Constable Zhao shouts from outside the gate",
         zh="院門插入鏡、固定（從院子裡往外拍；第一格就是關著的院門填滿畫面）：院門被人從外面一腳踹開，往裡朝鏡頭彈開、撞到籬笆，門口只露出一隻黑布靴和黑袍下襬踩在門檻上；趙捕頭在門外喊（畫外、用已錄的台詞）。他走進院子交給 s21；村民與屋門口的小禾隨全景一起拿掉（2026-11-07 真人版第二輪挑片後改鏡頭設計）"),
    dict(loc="yard", cam="Low-angle medium shot, tracking", chars=["zhaobutou"], night="yard",
         comp="low-angle medium shot of Constable Zhao walking across the dirt yard from the gate on screen right, the black scabbard on his left hip, the roll of red paper in his hands with its plain blank back toward the camera",
         lines=[("zhaobutou", "凡男子二十五歲未婚者，官府配妻三名，今日成親。", "念告示")],
         motion="as he walks he snaps the red paper open with a crack and holds it up before him, its plain blank back facing outward, the paper shivering in the wind, and he slides his eyes sideways to the house door off screen left",
         zh="低角度中景、跟拍：趙捕頭邊走邊唰地展開紅紙（背面朝鏡頭），紙在風裡抖一下，斜眼看畫面左邊的屋門"),
    dict(loc="yard", cam="Over-the-shoulder medium shot, slow push in", chars=["zhaobutou", "xuyan"], night="yard", nospeak=["xuyan"],
         comp="over-the-shoulder shot from behind Xu Yan in the doorway in the left foreground, his back to the camera, his blue-grey scholar's robe half-dry, both hands empty, the door frame beside him bare weathered grey wood and the house wall beside it bare brown mud, and Constable Zhao in the yard on screen right, the red paper in his hand with its plain blank back toward the camera",
         lines=[("xuyan", "等一下，今天就成親？我連自己都快養不活了。", "慌")],
         motion="Constable Zhao strides fast across the yard toward the doorway, the red paper flapping in his swinging fist, his heavy boots kicking up dust, while Xu Yan hurries down off the doorstep toward him, raising one open hand to stop him as he speaks with his back turned, his mouth unseen; Zhao plants his feet and halts an arm's length away, his shoulders squared",
         zh="過肩（許硯肩後拍趙捕頭）、慢推：趙捕頭大步走過來、紅紙甩動，停在一臂外；許硯從門檻跨下來抬手攔他（許硯背對鏡頭說話）；門框是光禿風化的灰木頭、屋牆是光禿的黃泥（2026-11-08 真人版成片審查：門框上長出寫「福」的紅紙）"),
    dict(loc="yard", cam="Full shot, slow push in", chars=["zhaobutou", "qinshuang", "aling"], night="yard",
         comp=f"full shot of the yard toward the gate on screen right, Constable Zhao in the middle of the yard, and in the gateway behind him two young women: Qin Shuang in front, {KNIFE}, and A-ling behind her with her head bowed and her eyes on the ground, iron shackles on both wrists joined by a short iron chain",
         lines=[("zhaobutou", "那是你的事。人我帶來了，一個都不能少。", "冷笑")],
         motion="Zhao gives a cold smirk and takes one big step to the side, sweeping his arm toward the gateway so the two women stand revealed; Qin Shuang lifts her chin, both her hands empty at her sides; A-ling keeps her head bowed and her eyes on the ground from the first frame to the last; both women keep their lips closed",
         zh="全景、慢推：趙捕頭冷笑著往旁邊讓開一大步，露出院門口的秦霜（前；柴刀一直插在腰帶右邊、兩手空著）與低著頭、戴鐵鐐的阿令（後；整鏡一直低頭看地上，抬眼留給 s38；2026-11-08 真人版成片審查）"),
    dict(loc="yard", cam="Medium shot, tracking", chars=["qinshuang", "xuyan"], night="yard",
         comp=f"medium shot of Qin Shuang in the yard, her arms folded, {KNIFE}, her face scornful, and Xu Yan standing at the left edge of the frame, partly cut off, his robe half-dry",
         lines=[("qinshuang", "就這身板？風大一點，都能把你吹回河裡。", "不屑")],
         motion="Qin Shuang strides up with her arms folded and walks half a circle around Xu Yan, looking him up and down from head to feet with a cool tilt of her head, and stops facing him; Xu Yan turns his head to follow her, his lips closed",
         zh="中景、跟拍：秦霜雙手抱胸大步上前，繞著許硯走半圈上下打量他"),
    dict(loc="yard", cam="Close-up, slow push in", chars=["xuyan"], night="yard",
         comp="close-up of Xu Yan on screen left, his blue-grey robe half-dry and his sleeves still wet, his eyes on Qin Shuang off screen right; behind him only the sunlit yard and the bamboo fence",
         lines=[("xuyan", "昨晚已經掉進去一次了，謝謝提醒。", "自嘲，乾笑")],
         motion="he lifts his still-wet sleeve and shakes it out with a flick of the wrist, a few drops of water falling, and gives a short dry laugh",
         zh="近景、慢推：許硯抬起還濕的袖子甩一甩，水滴下來，乾笑一聲"),
    dict(loc="yardin", cam="Insert, static", chars=["aling", "zhaobutou"], nospeak=["zhaobutou"], night="yard",
    # live pick (2026-11-07) and fix1: a bare blade showed in one take; in the other the hilt pointed at A-ling and never
    # touched the chain. Redesign (同一鏡改字兩次還是錯): an insert of her wrists and the chain; only the scabbard's far tip
    # comes in from screen left (Zhao's side, as in s23-s28) and taps the chain twice. His line is off screen in the recorded
    # voice (nospeak); s27 still has Xu Yan look down at the shackles and back up at Zhao.
         comp="insert shot of A-ling's two wrists in front of her waist, the shot opens directly on this insert from its very first frame: her still hands hang together against her grey-white cotton dress, iron shackles on both wrists joined by a short iron chain hanging in a slack loop between them, the frame cut at her waist above and her thighs below",
         lines=[("zhaobutou", "這個是罪奴阿令，配給你，算便宜你了。", "輕蔑")],
         motion="the iron-capped tip of a dark black-lacquered wooden scabbard slides in from the left edge of the frame and taps the iron chain twice, so the chain swings and rattles between her wrists; then the tip draws back out to the left; Constable Zhao speaks from off screen left",
         zh="阿令雙腕插入鏡、固定（第一格就是她腰前的雙手與鐵鐐鐵鍊，畫面上到腰、下到大腿）：一截深色木刀鞘（黑漆、鐵鞘尖）從畫面左邊伸進來，鞘尖在鐵鍊上點兩下，鐵鍊晃動作響，再從左邊收回；拿刀鞘的人在畫外；趙捕頭在畫面左邊外說話（畫外、用已錄的台詞）（2026-11-07 真人版第二輪挑片後改鏡頭設計）"),
    dict(loc="yard", cam="Over-the-shoulder medium close-up, slow push in", chars=["xuyan", "zhaobutou"], night="yard",
         comp="over-the-shoulder shot from behind Constable Zhao's shoulder and black hat in the right foreground, Xu Yan facing the camera on screen left, frowning, his eyes on Zhao",
         lines=[("xuyan", "她犯了什麼罪，要戴著鐵鐐來？", "皺眉，低聲")],
         motion="Xu Yan's brows draw together; he takes one deliberate step forward, his eyes dropping to A-ling off screen right and the shackles on her wrists, then lifting back to Zhao",
         zh="過肩（趙捕頭肩後拍許硯）、慢推：許硯皺眉往前一步，看一眼阿令的鐵鐐，再看回趙捕頭"),
    dict(loc="yard", cam="Low-angle close-up, slow push in", chars=["zhaobutou"], night="yard",
         comp="low-angle close-up of Constable Zhao wearing exactly one soft black constable's cap, a single cap on his head, his narrow eyes sliding sideways to Xu Yan off screen left, the corners of his mouth turned down, the opened red paper gripped in his right fist at his chest with its plain blank back toward the camera; behind him only the bright sky and the autumn branches",
         lines=[("zhaobutou", "她犯什麼罪，輪不到你一個窮秀才來問。", "冷笑")],
         motion="with his left hand he shoves the sheathed sword back into his belt at his left hip with a hard click, his right fist keeping hold of the red paper, then leans his upper body forward toward Xu Yan off screen left, looming over him",
         zh="低角度近景、慢推：趙捕頭（頭上只有一頂黑色軟捕快帽）左手把刀鞘插回腰間，右手一直握著展開的紅紙（背面朝鏡頭），往前探身逼近許硯，斜眼、嘴角下撇（2026-11-08 真人版成片審查：帽子疊成兩頂）"),
    dict(loc="yard", cam="Close-up, slow push in", chars=["xuyan"], night="yard",
    # live pick (2026-11-07): one draft only touched the lower edge and the paper stayed up with faint strokes on it; the
    # other grabbed it. The palm goes flat on its top edge and pushes it down out of the frame; the sheet is blank red.
         comp="close-up of Xu Yan in the yard, his sleeves still damp, calm and steady, a faint smile at the corner of his mouth, his eyes on Zhao off screen right, framed with clear space above his head; at the right edge of the frame the top half of the opened red paper held up by Constable Zhao off screen right, a sheet of plain blank red with its back toward the camera; behind him only the bamboo fence and the autumn tree",
         lines=[("xuyan", "問不得也罷。大衡律配婚第七條：三日為期，不得強押成親。", "不疾不徐")],
         motion="Xu Yan shifts his weight forward and takes half a step closer, lifts his right hand, lays his open palm flat on the top edge of the blank red paper and calmly presses it straight down until it leaves the bottom of the frame, his palm flat on it the whole way, a slight steady smile on his face",
         zh="近景、慢推：許硯沒退，往前半步，抬起右手、整個手掌平貼在紅紙上緣，把紅紙從趙捕頭面前穩穩按下去、按出畫面下緣；紅紙是空白的紅、背面朝鏡頭；臉上很穩、嘴角有一點笑（2026-11-07 真人版挑片重寫）"),
    dict(loc="yard", cam="Two-shot, slow push in", chars=["zhaobutou", "qinshuang"], night="yard",
         comp="two-shot, Constable Zhao in the foreground on screen left, his mouth half open, and Qin Shuang behind him on screen right with her arms folded, both looking toward Xu Yan off screen left",
         lines=[("qinshuang", "喲，窮秀才不只會讀書，還會背律條。", "有點意外")],
         motion="Zhao's mouth opens, then shuts with nothing said, and he shifts back half a step, his lips closed; behind him Qin Shuang lets her folded arms drop and raises one eyebrow at Xu Yan off screen left",
         zh="雙人鏡、慢推：前面的趙捕頭嘴張開又閉上、退半步；後面的秦霜放下抱胸的手，挑眉看許硯"),
    dict(loc="yard", cam="Medium shot, tracking", chars=["zhaobutou", "xuyan"], night="yard",
         comp="medium shot, Constable Zhao on screen right facing Xu Yan on screen left, the red paper already rolled into one tight tube from the very first frame, gripped in Zhao's right fist with only its plain blank back showing, the yard gate behind Zhao on screen right",
         lines=[("zhaobutou", "哼，那就三天。三天後不成親，你自己去跟縣太爺說。", "找台階下"), ("zhaobutou", "第三個在後頭轎子裡，嬌貴得很，你自己去接。", "往院門外一指，不耐煩")],
         motion="Zhao slaps the rolled red paper hard against Xu Yan's chest with his fist still around it, Xu Yan's two hands close on it there and only then Zhao lets go; from then on it stays rolled in Xu Yan's hands, his lips closed; Zhao turns and walks toward the gate on screen right, and half way there he looks back over his shoulder and points his thumb out past the gate",
         zh="中景、跟拍：紅紙從第一格就是捲好的一卷、握在趙捕頭右拳裡；他連拳帶紙往許硯胸口一拍，許硯雙手在胸口握住了他才放手，之後紙一直捲著在許硯手裡（2026-11-08 真人版成片審查：紅紙沒人拿、平紙一格變紙筒）；趙捕頭轉身往院門走，走到一半回頭用拇指往院門外一指"),
    dict(loc="yard", cam="Full shot, tracking", chars=["tangxiaotang", "zhaobutou"], night="yard",
         comp="full shot through the yard gate in the foreground, a small sedan chair set down in the lane outside with a plain blank curtain, Tang Xiaotang stepping out of it in her peach-pink brocade ruqun, one closed garment from the high stand-up collar to the waist, smiling, and Constable Zhao walking out through the gate toward her",
         lines=[("tangxiaotang", "讓一讓、讓一讓！我也是來配婚的，我叫唐小棠。", "甜，輕快")],
         motion="the curtain sweeps aside and Tang Xiaotang gathers her skirt in one hand and steps out, walking briskly in through the gate and waving the other hand high, her ribbons bouncing with each step; Constable Zhao strides past her out through the gate and leaves the frame",
         zh="全景、跟拍、前景院門：轎簾一掀，唐小棠（高立領、襦裙從立領到腰一件闔上）提著裙子跨出來，邊走進院門邊揮手；趙捕頭從她旁邊出院門離開畫面"),
    dict(loc="yard", cam="Close-up, slow push in", chars=["qinshuang"], night="yard",
         comp="close-up of Qin Shuang, her eyes cutting sideways to screen right, scornful; behind her only the bamboo fence and the sunlit yard",
         lines=[("qinshuang", "穿綢緞的千金小姐，也來湊這個數？", "嗤笑")],
         motion="she turns her head toward Tang Xiaotang off screen right, her eyes running from the silk sleeves down to the shoes, and she gives a short scornful snort through her nose, one corner of her mouth lifting",
         zh="近景、慢推：秦霜轉頭，眼睛從唐小棠的綢緞袖子掃到鞋，嗤一聲"),
    # live pick (2026-11-07): both drafts said the first line to the camera and turned to Qin Shuang for 「你就是許秀才吧？」
    # with Xu Yan nowhere in the frame. He is the over-the-shoulder in the right foreground (Tang is off screen right of
    # him in s35), she turns from Qin Shuang on the left to him; three named people.
    dict(loc="yard", cam="Over-the-shoulder medium close-up, slow push in", chars=["tangxiaotang", "qinshuang", "xuyan"], night="yard",
         comp=f"over-the-shoulder shot from behind Xu Yan's right shoulder and the back of his head in the right foreground, his blue-grey robe half-dry; in the middle Tang Xiaotang facing the camera, framed from the chest up with clear space above her head so that her whole head stays inside the frame as she leans in; on screen left a step away Qin Shuang with her arms folded, {KNIFE}, her mouth set in a flat line the whole shot",
         lines=[("tangxiaotang", "千金也到了年紀，官府的名冊上一樣有我。", "對秦霜，甜甜地頂回去"), ("tangxiaotang", "我爹說，嫁秀才比嫁商人體面。你就是許秀才吧？", "轉向許硯，笑")],
         motion="for the first line Tang Xiaotang turns her face to Qin Shuang on screen left with a sweet smile; for the second line she turns away from Qin Shuang to Xu Yan in the right foreground, leans in toward him with her head tilted and looks up into his face; Qin Shuang watches her sideways, cool, her lips closed; Xu Yan stays still with his back to us",
         zh="過肩（許硯右肩後拍）、慢推（唐小棠胸口以上、頭上留空）：前景右許硯的肩與後腦、中間唐小棠、左邊秦霜（抱胸、柴刀插在腰帶右邊）；唐小棠第一句轉向左邊的秦霜笑一下，第二句「你就是許秀才吧？」轉離秦霜、湊近前景的許硯歪頭看他；秦霜嘴閉著、不笑（2026-11-07 真人版挑片重寫）"),
    dict(loc="yard", cam="Medium shot, slow push in", chars=["xuyan", "erniu"], night="yard",
         comp=f"medium shot, Xu Yan in the front of the frame in the middle of the yard, {ROBE}, the rolled red paper in his right hand with only its plain blank back showing, stunned and blank: his eyes wide and unfocused, his brows raised, his mouth slack, no smile the whole shot; behind him Wang Erniu coming in from screen left, his trousers dry, both hands empty, grinning broadly; only Erniu smiles",
         lines=[("xuyan", "我是許硯……可我還沒想好，要怎麼養活三個人。", "愣住，老實答"), ("erniu", "秀才，一口氣三個老婆，你這是要發了啊！", "壓低聲音，樂")],
         motion="Xu Yan blinks, still blank and unsmiling, gives Tang Xiaotang off screen right a stiff nod and answers her, the red paper in his right hand; only then Erniu leans in to his ear, one hand cupped by his mouth, grinning, Xu Yan's lips closed",
         zh="中景、慢推：許硯愣住、發呆、不笑（眼睛睜大失焦、眉上揚、嘴微張），右手握著捲起的紅紙，對唐小棠僵硬地點頭（先許硯說話）；然後二牛從左後湊到他耳邊、用手擋著嘴咧嘴笑（只有二牛在笑；二牛說話時許硯嘴閉著；2026-11-07 審稿重寫）"),
    dict(loc="yard", cam="Extreme close-up, slow push in", chars=["xuyan"], night="yard",
         comp=f"extreme close-up of Xu Yan's eyes, the shot opens directly on his eyes from its very first frame, {EYES}; nothing else in the frame",
         lines=[("xitong", "叮。任務：三日內，與三人成婚。", "冷淡，像在念公告")],
         panel=[("任務：三日內與三人成婚", "task")],
         motion="his pupils contract sharply, his eyes widen and he blinks once, slowly, his lips remaining closed",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：虹膜維持自然深褐色、瞳孔裡只有一點很淡的冷色反光（2026-11-08 真人版成片審查）；瞳孔一縮，眨了一下（面板剪接時疊上，周圍的聲音一下子變小）"),
    dict(loc="yard", cam="Close-up, slow push in", chars=["xuyan"], night="yard",
         comp="close-up of Xu Yan's face, the colour drained from it, unsmiling, his eyes fixed on the empty air in front of him, the rolled red paper in his right hand hanging at his side; behind him only the bamboo fence and the autumn tree out of focus",
         lines=[("xitong", "失敗，抹殺。", "冷淡，輕描淡寫"), ("xuyan", "抹……殺？", "聲音發乾"), ("xitong", "字面意思。建議宿主，別浪費時間。", "冷淡，帶一點嫌棄")],
         panel=[("失敗：抹殺", "penalty")],
         motion="his lips tremble, his throat bobs as he swallows hard, and he takes half a step back as if struck; his lips stay closed while the system voice speaks",
         zh="近景、慢推：許硯臉色發白，嘴唇動了動、喉結滾一下，往後退半步（說「抹……殺？」時對嘴，系統說話時嘴閉著）"),
    # live pick (2026-11-07): both drafts lined the women up side by side, A-ling looked up from the first frame and Qin
    # Shuang held her knife. Four named people were on screen, so the shot is now his point of view (he is off screen and
    # his line is a thought, lips closed): the brides one behind another, A-ling last by the well, looking up at the end.
    dict(loc="yard", cam="Medium shot, slow push in", chars=["qinshuang", "tangxiaotang", "aling"], night="yard",
         comp=f"medium shot, the point of view of Xu Yan off screen: the brides facing the camera, one behind another in a line running back into the yard, each a step further back and a little to the right so every face shows: nearest, on screen left, Qin Shuang, arms folded, {KNIFE}; behind her, in the middle, Tang Xiaotang, her ruqun one closed garment from the high collar to the waist; furthest back, on screen right by the stone well, A-ling with her head bowed, iron shackles on both wrists joined by a hanging iron chain; behind them only the bamboo fence and the autumn tree",
         lines=[("xuyan", "三天，娶三個……好，那就娶給你看。", "心裡話，吸一口氣，下定決心", "inner")],
         motion="all their lips stay closed the whole shot; Qin Shuang looks straight ahead, cool and level; Tang Xiaotang tilts her head, curious; at the back by the well A-ling keeps her head bowed and her eyes on the ground, and only in the last second she slowly raises her eyes and looks straight into the lens",
         zh="中景、慢推（結尾；許硯的主觀，許硯在畫外、心裡話）：三個女子由前到後站成一列往院子裡排、一個比一個後退一步偏右，臉都看得到：最前秦霜（抱胸、柴刀一直插在腰帶右邊）、中間唐小棠、最後阿令在右後井邊，一直低著頭；到最後一秒阿令才慢慢抬眼直直看鏡頭（看許硯）；都嘴閉著（2026-11-07 真人版挑片重寫：一鏡最多三個有名字的人）"),
]

HEAD = [
    "- 重製版 r2：照 `script.md`（c01–c38 對應 s01–s38）與 `camera-feel-study-20261105.md`；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。",
    "- 2026-11-05 照分鏡十一項重寫：服裝與狀態（許硯 c04–c11 濕透、c12 起半乾袖子濕；阿令全集戴鐵鐐）、道具（紅紙、履歷都寫背面）、離場（c12、c15、c20、c32）、說話近景改慢推並補身體動作；台詞只改 c29。",
    "- 內部工作編號 901（工作資料夾 `zhong-tian-qu-qi-e901-dh`、`hailuo/*-dh-e901.json`）；發布 slug `zhong-tian-qu-qi-e001-r2`。",
    "- 只做到第二段 1312×736（站主 2026-11-05），剪接放大成 1920×1080。",
    "- 長鏡要買的秒數照 `script.md` 長鏡清單：s01 8 秒；s08、s14、s31、s34、s35 10 秒；s37 8 秒（`gen-dh` 只算 5／6 秒，買的時候照這張）。",
]
FOOT = [
    "- 場景參考：河邊 `set-liuxi-he-t1`、屋內 `set-xujia-wu-t1`、院子 `set-xujia-yuan-t1`；開場辦公室與街道沒有場景圖。",
    "- s01 只拍面試官的手：辦公室沒有場景圖，參照圖只能用面試官的定妝照，構圖寫明臉與身體不入鏡。",
    "- 唐小棠用 `tangxiaotang-portrait-t2`（gen-dh 的 PORTRAIT 對照）；她的鏡頭構圖都寫成下巴以上或「襦裙從立領到腰一件闔上」（第 56 集的教訓）。",
]
BRIEF = "見 `docs/videos/zhong-tian-qu-qi-e001-r2/brief.md`（工作編號 901 的資料夾只放產物）。"

# Long shots (script.md 長鏡清單): seconds to buy, so the lines fit without slowing past 1.1x.
BUY = {"s01": 8, "s08": 6, "s08b": 8, "s14": 10, "s31": 11, "s34": 11, "s35": 12, "s37": 8}
