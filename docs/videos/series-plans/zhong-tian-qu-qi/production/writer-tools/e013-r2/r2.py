"""Episode 13 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e013-r2/script.md
(c01-c10 = s01-s10, c10b = s11, c11-c41 = s12-s42; the CG-era r2 script of PR #2024, brought over from main 2026-11-14),
including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and 「真人版的改動（2026-11-14）」, which override the
tables. Every line is the script's, word for word; only the staging changes. Bible: production/r2-bible-e011-e020.md (rules 1-17).

Live action from the first draft, written the way e012-r2/r2.py was written AFTER its independent review (review.md in
../e012-r2, 必改 11 and 建議 19 applied there) and with the e911 draft lessons (colab/runs/e911-live/{review-picks-a.tsv,
review-picks-b.tsv,pick-review.md,fix1/review-picks.tsv}):
- OFFSCREEN_SPEECH = False (bible rule 15): every shot with an off-screen line, a thought or a system line writes the silence
  of each person on screen (SILENT_*, quiet()), after the action.
- Weapon racks (e911 picks: red-tasselled spears and racks in the yard background even with nobody armed): every set
  description says there is no weapon rack and nothing long leaning anywhere (NORACK; the carpenter's lane keeps its plain
  green bamboo poles, which the plot needs in c30, and says they have no tips, blades or tassels).
- Red bead strings (e911 4/70): the persimmon tree is written with only a few fruits high up, nothing hanging below them,
  in the day yard too (the day picture set-xujia-yuan-l2 has a tree full of fruit); extras.json keeps "no strings of beads".
- Paper is blank and front-lit (bible rule 17): the account books' covers are plain, the last page is shown edge-on or by
  its blank side, the contract is one torn-out page whose only mark is the red thumbprint, the paper offerings are plain
  blank paper, the drawing on the board is only lines.
- Silent people written hard: every listener of a recorded line (Tang Xiaotang's eight lines, the carpenter's shout through
  the door, the thoughts, the system) says nothing, lips pressed together from the first frame to the last.
- Tang Xiaotang never speaks on camera (bible rule 3): her eight lines (c04, c07, c09, c10, c11, c20, c22, c31) are shot from
  close behind her (TBACK, `nospeak`, spec.json drops her three face pictures and her identity sentence) with the person she
  speaks to straight ahead of her, so that her head need not turn; c09 is an insert of her hand on the small gold abacus.
  Her silent face shots (c12, c24) get e907's neutral face sentences in spec.json. Costume: the live portrait (bible rule 4).
- The one weapon (bible rule 5): Qin Shuang's chopping knife only in c40-c41, written as one fixed object (KNIFE), in her
  RIGHT hand, edge toward his throat, never changing hands; already in her hand in c40 (the draw from the belt is not shot:
  her belt is written empty everywhere, extras.json drops the knife from her look). In c40-c41 Xu Yan is the unnamed young
  man seen from behind (no pictures sent), and the prompt says there is no other blade. Everywhere else NOBLADE.
- The carpenter's place: set-mujiang-fang-l1 is the lane with the workshop's dark wooden front and its workbench OUT under
  the eave (no interior). c24-c30 「工坊裡」 is restaged at that workbench under the eave; c27 turns the board to the sun.
- The bamboo grove: set-zhulin-fen-l1 has the grave in the middle with its blank marker on a post at the right, and an old
  hall far behind with a dark plaque and two unlit red lanterns. The text keeps that hall dark and unlit, its board blank,
  and writes that the only light is the paper fire (and, from c34, the one lantern in Xu Yan's hand).
- Night is night: c32-c33 the night yard (set-xujia-yuan-ye-l1, the moon behind clouds), no torches; c34-c41 the grove with
  no moon, cold starlight, the little paper fire and the one lantern. Qin Shuang carries no lantern and no fire striker (the
  script's 火摺子 is dropped: a thing at her waist is drawn as a scabbard).
- Nobody is flipped in the edit: every speaker wears a cross collar; sides are written as screen left/right.
- Smiles allowed (the script): c03 Qin Shuang's one-corner curl, c10b and c14 Xu Yan's wry closed-lip half-smile, c19 the
  carpenter's cold sneer, c31 Xu Yan's small closed-lip smile with the thumbs-up. Everywhere else NOSMILE.
State at the junction (e012 r2.py s35): the yard before dawn, Xu Yan standing alone in the middle in the old grey outer coat,
the torch he set upright in the mud at the corner of the round stone table on screen left, its flame a tiny dying glow.
s01 is sunrise in the same yard: the torch burnt out and cold, one wisp of smoke, Xu Yan where he stood.
Places: the day yard set-xujia-yuan-l2 (gen-dh "morning yard"), the night yard set-xujia-yuan-ye-l1 ("night yard of the Xu
farmhouse"), the carpenter's lane set-mujiang-fang-l1 ("carpenter's workshop") and the grove set-zhulin-fen-l1 ("bamboo
grove"); gen-dh's SET already maps all four. New person: Carpenter Shi (shimujiang-portrait-l1; build-r2.py's EN gets
"Carpenter Shi"; his voice in cast.json is Gacrux, not Alnilam, which e008's escort chief used).
"""
EP = 913  # internal working number; the published slug is zhong-tian-qu-qi-e013-r2
SLUG = "zhong-tian-qu-qi-e013-r2"
EP_TITLE = "木匠不肯（重製版 r2）"
OUTLINE_SECONDS = 210.5  # script.md: 210.5 s, 42 shots (66 + 101 + 43.5)
TARGET_MINUTES = [3, 4]
TITLE = "木匠不肯｜種田娶妻打天下 第13集（重製版）"
DESCRIPTION = "天亮了，秦霜牽著鏢局的馬去還；唐小棠抱著十本帳追出來，許硯又說晚上再對。十天要做一百張紙，得先有竹簾，全村只有村尾的石木匠會做，可他最恨秀才。門一拉開又甩上，窗裡飛出一把刨子：上個秀才騙了他三年工錢。許硯情急說是縣令要的，系統當場判定說謊：明日只能說真話。唐小棠一手按住門：紙賣出去分您一成，寫成契約按手印。許硯在木板上畫竹簾，還要在中間編一片柳葉，柳溪的紙對著光一看就認得。石木匠按了手印：明晚，給你一張。當夜秦霜帶著一包紙錢出門，許硯提燈跟進竹林，看見她跪在一座沒有名字的墳前。腳下枯枝一響，柴刀停在他喉前：你跟蹤我？《種田娶妻打天下》第 13 集（重製版）。"
THUMB = ("木匠不肯", "s16")
CHARACTERS = ["xuyan", "qinshuang", "tangxiaotang", "shimujiang", "xitong"]
MINOR = {}  # every speaker has a cast.json voice; nobody else speaks
MUSIC = "one cue per scene: a light quiet morning cue of soft plucked strings and a wooden flute in a farmhouse yard at sunrise, pausing for one beat under a dry remark; then a light playful comedy cue of pizzicato strings, wood blocks and a small drum, one low thud under a lie being caught and one small bright accent when a grumpy old craftsman gives in; then a quiet cold night cue of a low drone, soft wind and sparse low plucks, one deep low note at a lonely grave, the music dropping out completely at the snap of a twig, one sharp heavy hit as a knife is raised, ending in tense silence; ancient Chinese rural drama, no vocals"

# Scene headers of script.md. Scene 1 is the day yard picture (set-xujia-yuan-l2) at sunrise; scene 2 the carpenter's lane and
# its workbench under the eave (set-mujiang-fang-l1); scene 3 the night yard (set-xujia-yuan-ye-l1) and the bamboo grove
# (set-zhulin-fen-l1). Close shots use the short `_c` headers. No person's name in a place phrase.
NORACK = "no weapon rack, no spears and no poles or sticks leaning anywhere"
LANE_POLES = ("no weapon rack and no spear anywhere; the only long things leaning against the walls are plain green bamboo "
              "poles with no tips, no blades and no tassels")
LOC = {
    "yard": f"In the morning yard of the Xu farmhouse at sunrise in late autumn: the packed-earth yard still churned with last night's footprints, the house door at the back left with a woodpile beside it, one round stone table in the middle, the dark persimmon tree with half its leaves fallen and only a few fruits high in its branches, nothing hanging below them, the stone well with its wooden windlass at the front right, the packed-earth yard wall capped with grey roof tiles on screen right with the plain wooden yard gate in it, nothing written on any board or wall; {NORACK}; the fields beyond the wall harvested and bare; a clear cold autumn sunrise, low cool golden sunlight slanting in from the right, long shadows",
    "yard_c": f"In the morning yard of the Xu farmhouse at sunrise, low cool golden autumn sunlight from the right; {NORACK}",
    "lane": f"In the lane at the end of the village outside the carpenter's workshop in the late morning: a packed-earth lane running away into the distance on screen left between earthen walls, on screen right the dark wooden front of the carpenter's workshop under a thatched eave with its plain wooden door, one window with a rolled bamboo blind, one plain wooden board on the wall with nothing on it, a heavy plain wooden workbench under the eave, a heap of pale wood shavings on the ground by the door; no sign and no writing anywhere; {LANE_POLES}; a clear autumn late morning, warm sunlight slanting in from the left, soft shadows",
    "lane_c": f"In the lane outside the carpenter's workshop in the late morning, warm sunlight from the left; {LANE_POLES}",
    "bench": f"At the heavy plain wooden workbench under the thatched eave of the carpenter's workshop at the end of the village: the dark wooden wall behind it with a saw, a wooden hand plane and a chalk line reel hanging on it, a rolled bamboo blind in the window, a bundle of plain green bamboo poles leaning at the right end; on the bench one long planed wooden board, a small box of charcoal sticks and a wooden mallet, pale wood shavings at its near edge; nothing written on any board or wall; {LANE_POLES}; warm late-morning autumn sunlight from the left",
    "bench_c": f"At the workbench under the eave of the carpenter's workshop, warm late-morning sunlight from the left; {LANE_POLES}",
    "nyard": f"In the night yard of the Xu farmhouse at the second watch: the packed-earth yard, the packed-earth yard wall capped with grey roof tiles on screen right with the plain wooden yard gate in it, the house door at the back left with a woodpile beside it, the dark persimmon tree with only a few fruits high in its branches, nothing hanging below them, one blank paper lantern with no writing hanging under the eaves, nothing written on any board or wall; {NORACK}; deep night, the moon hidden behind clouds, the sky black, lit only by the warm glow of the one lantern, no torch anywhere, no daylight anywhere",
    "nyard_c": "In the night yard of the Xu farmhouse at the second watch, deep night, the sky black, lit only by the warm glow of one blank paper lantern under the eaves, no torch anywhere",
    "grove": f"In the bamboo grove behind the village at night: dense tall bamboo on both sides, a narrow dirt path, a small clearing, in the clearing a small low earthen grave mound with one plain blank wooden marker board on a post beside it, no characters on it, dry fallen bamboo leaves on the ground, the low dark roofs of an old empty hall far behind the clearing, its doorway dark, every lantern there dark and unlit, its board blank; {NORACK}, only living bamboo growing straight up; deep night with no moon, a sky full of cold stars, cold blue starlight, a light wind in the bamboo leaves, no daylight anywhere",
    "grove_c": f"In the bamboo grove behind the village at night, deep night with no moon, cold blue starlight; {NORACK}",
}
LIGHT = {
    "morn": "the low cool golden sunrise light from the right stays unchanged",
    "day": "the warm late-morning sunlight from the left stays unchanged",
    "night": "the deep night and the one warm lantern glow stay unchanged, the sky stays black",
    "grove": "the deep night and the cold blue starlight stay unchanged, the sky stays black, no daylight",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object).
XU = "Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe"
XU2 = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, the sleeves down to his wrists"
TIRED = "his eyes red-rimmed and bloodshot after a night without sleep"
QIN = "her dark brown cross-collared short jacket, wide plain leather belt with nothing tucked in it and nothing hanging from it, black trousers, leather boots and high ponytail tied with black cord"
CARP = ("Carpenter Shi, in his faded brown cross-collared short work jacket with the sleeves rolled up and his worn brown "
        "leather apron, one plain wooden stick through his grey topknot")
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
GOLD = "the small gold abacus hanging at her waist"
LEDGERS = "a tall stack of ten thread-bound account books with plain dark blue cloth covers, nothing written on any cover"
LEDGER = "one thread-bound account book with a plain dark blue cloth cover, nothing written on it"
INKBOX = "one small round red lacquered box no bigger than a coin purse"
HORSE = "one brown horse with a plain leather saddle and reins"
PLANE = "one carpenter's wooden hand plane, a smooth rectangular block of pale wood"
LANTERN = "one blank paper lantern with no writing, a small candle burning inside it"
NOBLADE = "no blade, no knife, no sword, no scabbard and no weapon of any kind anywhere in the frame"
# bible rule 5: the plot's knife, one fixed object, only in c40-c41 (s41-s42), always in her RIGHT hand.
KNIFE = ("one old chopping knife with a short plain wooden handle and a dark iron blade only a little longer than a palm, "
         "a thick blunt back and a nicked cutting edge, not a broad cleaver, not a sword")
ONLYKNIFE = "no other blade, knife, sword, scabbard or weapon anywhere in the frame; the young man's hands hold only the lantern"
OUT_TORCH = ("one burnt-out torch standing upright in the mud at the corner of the round stone table, nobody holding it, its "
             "head blackened and cold, one thin wisp of grey smoke rising from it, no flame")
PAPERFIRE = "one small fire of burning plain blank paper with no writing, glowing warm orange low on the ground"
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with two looped buns tied with pink "
         "silk ribbons and pearl pins, two long pink silk ribbons hanging from the buns down over her shoulders, a pink inner "
         "collar at the nape of her neck and her light peach-pink silk shoulders; the back of her head toward us the whole time, "
         "her ear the furthest round her head we ever see, no cheek, no profile and no lips at any moment")
HER_BACK = ("one young woman seen only from behind, appearing only once: only the back of her head with two looped buns tied with "
            "pink silk ribbons and her light peach-pink silk shoulder, soft and dark, her head turned fully away from us, her ear, "
            "cheek and profile never visible, her face never in the frame")
HE_BACK = ("one young man seen only from behind, appearing only once: only the back of his black topknot and his shoulder in an "
           "old plain grey cloth coat, soft and dark, his head turned fully away from us, his ear, cheek and profile never "
           "visible, his face never in the frame")
HE_BACK2 = ("one young man seen only from behind, appearing only once: only the back of his black topknot and his shoulder in a "
            "faded blue-grey robe, soft and dark, his head turned fully away from us, his ear, cheek and profile never visible, "
            "his face never in the frame")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
SILENT_SHE = "She says nothing in this shot: her lips stay pressed together from the first frame to the last, her jaw still, no talking, no mouthing words"
HEADSTILL = "she keeps her head still and never turns it, the back of her head toward us the whole shot"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return (f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, "
            f"no mouthing words, no smile at any moment")


SHOTS = [
    # ---- scene 1: the Xu yard at sunrise (the gate on screen right, the house door at the back left).
    dict(chapter="天亮", loc="yard", cam="Wide shot, slow push in", chars=["xuyan", "qinshuang"], night="morn",
         comp=f"wide shot past {OUT_TORCH} in the left foreground: in the middle of the yard {XU}, standing exactly where he stood all night, framed full length with clear space above his head, {TIRED}, his face three-quarter to screen right, never the lens; weary: shoulders slack, eyes heavy, lips closed; on screen left Qin Shuang, {QIN}, leading {HORSE} by the reins from the woodpile toward the yard gate on screen right, her face in profile toward screen right, never the lens; brisk: brows level, chin up, lips moving between words, no smile; {NOBLADE}; exactly two people and one horse, nobody else",
         lines=[("qinshuang", "馬我去還鏢局，中午就回來。", "爽快，不回頭")],
         motion=f"Qin Shuang leads the horse past Xu Yan toward the gate on screen right without turning her head, the hooves sinking into the mud; Xu Yan turns his head to follow her; {quiet('Xu Yan')}",
         zh="全景、慢推（第一格接第 12 集 s35：同一個院子，天亮了）：左前景石桌角那支插在泥裡的火把已熄、焦黑、冒一縷煙；許硯（舊灰外衣、眼睛布滿血絲）還站在院子中間；秦霜（腰帶什麼都沒插）牽著鏢局的棕馬從左邊柴堆往畫右院門走，不回頭說話；許硯轉頭看她、嘴閉著"),
    dict(loc="yard", cam="Medium shot, slow push in", chars=["xuyan"], night="morn",
         comp=f"medium shot: {XU}, framed from the knees up with clear space above his head, {TIRED}, turning toward the yard gate off screen right, his face three-quarter to screen right, never the lens; worried: brows drawn together, eyes on the woman leaving, lips moving between words, no smile; behind him only the house wall, the woodpile and the low morning sun; {NOBLADE}",
         lines=[("xuyan", "妳一個人去？路上要是碰到錢家的人呢？", "擔心，叫住她")],
         motion=f"Xu Yan takes one step toward the gate and raises one hand to call her back; {NOSMILE}",
         zh="中景、慢推：許硯（舊灰外衣、眼睛布滿血絲）轉向畫右的院門，往前追一步、抬手叫住她說話；不笑"),
    # Qin Shuang may curl one corner of her mouth here (the script).
    dict(loc="yard", cam="Over-the-shoulder medium shot, slow push in", chars=["qinshuang"], night="morn",
         comp=f"over-the-shoulder medium shot from close behind {HE_BACK}, in the left foreground; on screen right at the open yard gate Qin Shuang, {QIN}, holding the reins of {HORSE} beside her, framed from the knees up with clear space above her head, her face three-quarter to screen left looking back at him, never the lens; brisk and teasing: brows lifted, one corner of her mouth curling up a little, never a grin, teeth never showing, lips moving between words; beyond the gate only the bright village road; {NOBLADE}; exactly two people and one horse",
         lines=[("qinshuang", "碰到就叫他們讓路。你去睡一覺，眼睛紅得像兔子。", "回頭一眼，嘴角一勾")],
         motion="Qin Shuang glances back at him over her shoulder, then tugs the reins once and leads the horse out through the gate to screen right; the young man in the foreground keeps his head still, the back of his head toward us the whole shot",
         zh="過肩中景、慢推：前景左只有許硯的後腦與舊灰外衣肩（頭整個轉開、不點名、不送圖）；畫右院門口秦霜牽著馬回頭看他一眼說話（本鏡可以嘴角一勾，不露牙），拉一下韁繩牽馬跨出院門"),
    # Converted: Tang Xiaotang's line from close behind her (bible rule 3); Xu Yan straight ahead of her.
    dict(loc="yard", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="morn",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, in the left foreground, the top edges of {LEDGERS} showing past her arms in front of her chest; facing us straight ahead of her a step away in the middle of the yard {XU}, framed from the waist up with clear space above his head, {TIRED}, his eyes on her face just left of the lens, never the lens; caught out: brows rising, eyes guilty, lips closed; behind him the yard gate on screen right and the low morning sun; {NOBLADE}; exactly two people",
         lines=[("tangxiaotang", "你說過陪我對帳，這十本今天總該對了。", "追上來，不給退路")],
         motion=f"the young woman hurries up to him from the house door and stops, lifting the stack of account books a little higher in front of her with both arms; {HEADSTILL}; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中景、慢推：前景左只有唐小棠的後腦、雙丸子頭、兩條長粉緞帶、淡桃粉衣肩（臉與嘴不入鏡），十本藍布面帳冊抱在胸前只露上緣；她從屋門小跑到許硯面前停下、帳冊往上一托，頭始終不轉；許硯在她正前方、心虛、嘴閉著。台詞 nospeak，剪接放錄音；spec.json 拿掉她三張臉部參考圖"),
    dict(loc="yard", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="morn",
         comp=f"over-the-shoulder medium shot from close behind {HER_BACK}, the top edges of a stack of blue cloth-covered account books showing past her arm, in the left foreground; on screen right {XU}, framed from the waist up with clear space above his head, {TIRED}, half turned away toward the yard gate on screen right and looking back at her, his face three-quarter to screen left toward her, never the lens; evasive: brows up, a sheepish look, lips moving between words, no smile; behind him only the yard wall and the gate; {NOBLADE}",
         lines=[("xuyan", "今天得先找木匠，帳晚上再對。", "推託，邊走邊揮手")],
         motion=f"Xu Yan backs away two steps toward the gate on screen right, waving one hand at her as he speaks; the woman in the foreground keeps her head still; {NOSMILE}",
         zh="過肩中景、慢推：前景左只有唐小棠的後腦與肩（頭整個轉開、不點名、不送圖）；許硯在畫右往院門倒退兩步、回頭朝她揮手說話；不笑"),
    # A thought and the system: his silence written (bible rule 15). No blue light (bible rule 11).
    dict(loc="yard_c", cam="Close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"close-up of {XU}, framed from the chest up with space above his head, {TIRED}, standing still in the yard, his face three-quarter to screen right, never the lens; at first stopped short, then exasperated: eyes rolling up to the sky, then shutting for a moment, a long breath out, lips closed the whole shot; behind him only the packed-earth yard wall in the low morning light",
         lines=[("xitong", "晚上對？宿主這是第三次推這十本帳。", "冷，嫌棄"),
                ("xuyan", "這次是真的忙，紙做不出來，我就成睜眼瞎了。", "嘴硬，有點委屈", "inner")],
         motion=f"Xu Yan stops mid-step; his eyes roll up toward the sky; then he shuts his eyes for a moment and lets out a long breath; {SILENT_HE}; he is thinking, not speaking; {NOSMILE}",
         zh="近景、慢推（身後只有院牆與晨光）：許硯腳步一停、眼睛往上一翻，再閉一下眼、吐一口氣；全程嘴閉著（系統吐槽與心裡話都是畫外，剪接放錄音）。不寫藍光"),
    # Converted: Tang Xiaotang's line from close behind her at the stone table; Xu Yan across the table.
    dict(loc="yard", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="morn",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, standing at the round stone table in the left foreground; facing us straight ahead of her across the table {XU}, framed from the waist up with clear space above his head, {TIRED}, his eyes on her face just left of the lens, never the lens; sheepish: brows up, lips closed; behind him only the yard wall and the morning sun; {NOBLADE}; exactly two people",
         lines=[("tangxiaotang", "找木匠做什麼？家裡的門好好的，又沒壞。", "叉腰，不解")],
         motion=f"the young woman drops {LEDGERS} onto the stone table with a thump and sets one hand on her hip; {HEADSTILL}; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中景、慢推、前景石桌：前景左只有唐小棠的後腦與肩；她把一摞帳冊「咚」地放上石桌、一手叉腰，頭始終不轉；許硯在桌子對面正對我們、嘴閉著。台詞 nospeak，剪接放錄音；spec.json 拿掉她三張臉部參考圖"),
    dict(loc="yard", cam="Medium shot, slow push in", chars=["xuyan"], night="morn",
         comp=f"medium shot over the round stone table in the foreground with a stack of plain blue cloth-covered account books on it: {XU}, framed from the waist up with clear space above his head, {TIRED}, standing behind the table, his face three-quarter to screen left toward the young woman off screen left, never the lens; earnest: brows lifted, eyes wide, lips moving between words, no smile; behind him only the house wall, the woodpile and the morning light; {NOBLADE}",
         lines=[("xuyan", "十天內要造出一百張紙，得先有竹簾。", "認真")],
         motion=f"Xu Yan leans over the stone table and traces a square frame in the air above it with both hands; {NOSMILE}",
         zh="中景、慢推、前景石桌與帳冊：許硯站在石桌後，朝畫左外的唐小棠說話，兩手在桌上比出一個方框（竹簾的大小）；不笑（稿子是唐小棠肩後的過肩；真人版前一鏡已經是她的背，這鏡改單人）"),
    # Converted: her line over an insert of her hand on the small gold abacus (no face).
    dict(loc="yard_c", cam="Insert close-up, slow push in", chars=[], night="morn",
         comp="insert close-up, the shot opens directly on one small gold abacus hanging from a ribbon at the waist of a peach-pink pleated skirt and one slender hand in a peach-pink silk sleeve resting on it, from its very first frame; only the hand, the sleeve, the small abacus and the cloth are in the frame, no face; low golden morning light",
         lines=[("tangxiaotang", "我賣肥皂那天聽人說，全村只有石木匠會做竹簾。", "想起來，篤定")],
         motion="two fingers flick two beads of the small gold abacus across, pause, then flick one more; then the hand lets go of the abacus and drops out of the frame",
         zh="【改插鏡】插鏡、慢推（第一格就是腰間的小金算盤）：唐小棠的手撥兩下小金算盤，停一下再撥一顆，手放開出畫；臉不入鏡，台詞剪接放錄音（稿子是她下巴以上的近景）"),
    # Converted: from close behind her; she wags one finger beside her head (no pointing: an arm out to the side turns the head).
    dict(loc="yard", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="morn",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, standing at the round stone table in the left foreground; facing us straight ahead of her across the table {XU}, framed from the waist up with clear space above his head, {TIRED}, his eyes on her face just left of the lens, never the lens; listening, then dismayed: brows sinking, lips closed; behind him only the yard wall and the morning light; {NOBLADE}; exactly two people",
         lines=[("tangxiaotang", "可他最恨秀才，上一個上門的，被他拿刨子轟出來。", "不笑，數落")],
         motion=f"the young woman raises her right hand beside her head and wags one finger from side to side; {HEADSTILL}; Xu Yan's shoulders slump and his eyes slide toward the yard gate off screen right; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中景、慢推：前景左只有唐小棠的後腦與肩；她在頭旁豎起一根手指搖一搖（不往村尾一指：手往側邊伸頭會轉），頭始終不轉；許硯聽著肩膀一垮、眼睛往畫右的院門一瞄、嘴閉著。台詞 nospeak，剪接放錄音"),
    # Xu Yan may give a wry closed-lip half-smile here (the script: 苦笑).
    dict(loc="yard_c", cam="Close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"close-up of {XU}, framed from the chest up with space above his head, {TIRED}, his face three-quarter to screen left toward the young woman off screen left, never the lens; rueful: brows up, a wry closed-lipped half-smile, teeth never showing, lips moving between words; behind him only the packed-earth yard wall",
         lines=[("xuyan", "他最恨秀才？那我上門，不是送去挨罵嗎？", "苦笑")],
         motion="Xu Yan rubs the back of his neck with one hand and glances toward the yard gate off screen right, then looks back at her as he speaks",
         zh="近景、慢推（身後只有院牆）：許硯抓抓後頸、往畫右的院門看一眼，再轉回來對畫左外的唐小棠說（本鏡可以苦笑，嘴閉著的半笑、不露牙）"),
    # Converted: from close behind her; she takes one book and the ink box, then steps up to him.
    dict(loc="yard", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="morn",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, standing at the round stone table in the left foreground with the stack of plain blue cloth-covered account books on it; facing us straight ahead of her across the table {XU}, framed from the waist up with clear space above his head, {TIRED}, his eyes on her face just left of the lens, never the lens; resigned: brows easing, a small tired nod, lips closed; behind him only the yard wall and the morning light; {NOBLADE}; exactly two people",
         lines=[("tangxiaotang", "所以我跟你去。談價錢的事，你別開口。", "胸有成竹")],
         motion=f"the young woman lifts the top account book off the stack and tucks it under her left arm, slips {INKBOX} into her right sleeve and steps up to the table's edge in front of him; {HEADSTILL}; Xu Yan nods once; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中景、慢推：前景左只有唐小棠的後腦與肩；她從那摞帳冊最上面抽一本夾在左臂下，把小圓紅印泥盒塞進右袖，往前一步站到桌邊，頭始終不轉；許硯點一下頭、嘴閉著（結尾）。稿子的「繞過石桌走到他身邊」不拍（側走頭會轉）。台詞 nospeak，剪接放錄音"),
    # ---- scene 2: the carpenter's lane (the door on screen right, the lane running away on screen left).
    # The carpenter's shout through the shut door: both on screen silent. Tang's silent face: neutral sentence in spec.json.
    dict(chapter="木匠", loc="lane", cam="Wide shot, slow pan right", chars=["xuyan", "tangxiaotang"], night="day",
         comp=f"wide shot past a pile of firewood at the edge of the lane in the left foreground, keeping them in the frame as they walk from screen left to screen right: {XU2}, walking up to the shut plain wooden door of the workshop on screen right, framed full length with clear space above his head, his face in profile toward screen right, never the lens; hopeful, lips closed; two steps behind him Tang Xiaotang {TANG}, {LEDGER} tucked under her left arm, {GOLD}, her face three-quarter to screen right, never the lens; wary: brows drawn, lips closed, no smile; {NOBLADE}; exactly two people in the lane",
         lines=[("shimujiang", "秀才的話不值錢，別來敲我的門！", "隔著門吼，粗啞很衝")],
         motion=f"Xu Yan raises his hand and knocks twice on the door; the door opens a finger's width and slams shut again, a puff of sawdust bursting from the frame, and he jerks his head back; {quiet('Xu Yan and Tang Xiaotang', 'their', True)}",
         zh="全景、慢慢往右搖（不寫 tracking）、前景巷口一堆柴：許硯（第二場起脫下外衣）走到木門前，唐小棠（臂彎夾一本藍布帳冊、腰間小金算盤、不笑）在他身後兩步；許硯敲門兩下，門縫拉開一指寬又「砰」地甩上、門框噴出木屑，他往後一仰（剪在甩門的一瞬）；兩人整鏡不說話不動嘴；石木匠在門裡吼（畫外，剪接放錄音）"),
    dict(loc="lane_c", cam="Insert close-up, low angle, slow push in", chars=[], night="day", act=3,
         comp="insert low-angle close-up, the shot opens directly on the packed-earth lane with a heap of pale wood shavings, a man's black cloth shoes and the hem of a faded blue-grey robe, from its very first frame; only the ground, the shavings, the shoes and the hem are in the frame, no face; warm late-morning sunlight",
         lines=[],
         motion=f"{PLANE} comes tumbling down from above on screen right and thumps into the heap of shavings beside the shoes, shavings scattering up; the shoes jerk back half a step",
         zh="插鏡、低角度、慢推（第一格就是巷子泥地、刨花堆與許硯的布鞋、藍灰袍下襬）：一把木刨子從右上方翻著掉下來，砸進鞋邊的刨花堆、刨花濺起，鞋往後一縮（無台詞；窗板彈開那一下在畫外，音效交代）"),
    # Xu Yan may give a wry closed-lip half-smile here (the script: 又好氣又好笑).
    dict(loc="lane", cam="Medium shot, slow push in", chars=["xuyan"], night="day",
         comp=f"medium shot: {XU2}, in the sunny lane, framed from the knees up with clear space above his head, his face three-quarter to screen right toward the shut door on screen right, never the lens; half exasperated, half amused: one brow cocked, a wry closed-lipped half-smile, teeth never showing, lips moving between words; behind him only the sunny lane and the earthen wall; {NOBLADE}",
         lines=[("xuyan", "我還沒開口呢，您怎麼就知道我要說什麼？", "又好氣又好笑")],
         motion=f"Xu Yan bends down, picks {PLANE} up out of the shavings, weighs it in his hand and straightens up, eyeing the door sideways",
         zh="中景、慢推：許硯彎腰從刨花堆撿起刨子、掂一掂、直起身，斜眼看畫右的門說話（本鏡可以又好氣又好笑，嘴閉著的半笑、不露牙）"),
    dict(loc="lane", cam="Medium shot, slow push in", chars=["shimujiang"], night="day",
         comp=f"medium shot past one man's hand in a faded blue-grey sleeve holding {PLANE} in the left foreground, its owner outside the frame: in the open doorway of the workshop on screen right {CARP}, framed from the knees up with clear space above his head, his face three-quarter to screen left toward the young man off screen left, never the lens; bitter and furious: brows slammed down, jaw clenched, eyes narrowed, teeth gritted between words, no smile; behind him only the dark inside of the workshop; {NOBLADE}; only one person seen in full",
         lines=[("shimujiang", "上個秀才叫我修書院，騙了我三年工錢！", "咬牙，舊恨")],
         motion=f"Carpenter Shi yanks the door wide open, plants himself in the doorway and jabs one thick finger out toward the lane; the hand with the plane in the foreground stays still; {NOSMILE}",
         zh="中景、慢推、前景許硯手上的刨子（只露手與藍灰袖）：石木匠一把拉開木門站在門口（畫右）、皮圍裙，瞪著畫左外的許硯，粗手指往巷子一戳，咬牙說；不笑"),
    dict(loc="lane_c", cam="Close-up, slow push in", chars=["xuyan"], night="day",
         comp=f"close-up of {XU2}, framed from the chest up with space above his head, hugging {PLANE} against his chest, his face three-quarter to screen right toward the man in the doorway off screen right, never the lens; flustered: eyes darting, brows up, lips moving fast between words, no smile; behind him only the earthen wall of the lane",
         lines=[("xuyan", "這回不一樣，是縣令大人要的！", "情急，脫口而出")],
         motion=f"Xu Yan's eyes dart left and right hunting for an excuse, one hand flicks out pointing off toward screen left, and he blurts it out; then he freezes, mouth half open; {NOSMILE}",
         zh="近景、慢推（身後只有巷子土牆）：許硯抱著刨子、眼珠亂轉找藉口，一手往畫左（縣城方向）一指脫口而出，說完嘴張著僵住；慌、不笑"),
    # The system twice over his eyes: he says nothing (bible rule 15); no blue light (bible rule 11).
    dict(loc="lane_c", cam="Extreme close-up, locked", chars=["xuyan"], night="day",
         comp="extreme close-up, the shot opens directly on Xu Yan's eyes and brows from its very first frame: only his eyes, his brows and the top of his nose are in the frame, his mouth below the frame; his face three-quarter to screen right, never the lens; warm late-morning sunlight on his skin",
         lines=[("xitong", "叮。判定：說謊。懲罰：明日只能說真話。", "冷，宣判"),
                ("xitong", "宿主連木匠都騙，真是一點都不挑。", "冷，嫌棄")],
         panel=[("判定：說謊", "penalty"), ("懲罰：明日只能說真話", "penalty")],
         motion=f"his eyes fly wide and his brows jump; then he squeezes his eyes shut and screws up his face as if jolted; his mouth stays below the frame; he says nothing; {NOSMILE}",
         zh="大特寫、固定（第一格就是許硯的眼睛與眉毛，嘴不入鏡）：眼睛一瞪、眉毛一跳，接著像被電到一樣緊閉眼、皺臉；系統兩句畫外，面板兩行疊上（吐槽那句不出面板）。不寫藍光"),
    dict(loc="lane_c", cam="Close-up, slow push in", chars=["xuyan"], night="day",
         comp=f"close-up of {XU2}, framed from the chest up with space above his head, hugging {PLANE} against his chest, his face three-quarter to screen right, never the lens; sulky: one eye opening, the corners of his mouth pulled down, lips closed the whole shot; behind him only the earthen wall of the lane",
         lines=[("xuyan", "不騙一句，他連門都不讓我進啊。", "委屈，嘀咕", "inner")],
         motion=f"Xu Yan opens one eye, the corners of his mouth pull down and he hugs the plane tighter; {SILENT_HE}; he is thinking, not speaking; {NOSMILE}",
         zh="近景、慢推：許硯睜開一隻眼、嘴角往下撇、抱緊刨子；嘴一直閉著（心裡話，剪接放錄音）"),
    # The carpenter may sneer here (the script: 冷笑).
    dict(loc="lane", cam="Over-the-shoulder medium shot, slow push in", chars=["shimujiang"], night="day",
         comp=f"over-the-shoulder medium shot from close behind {HE_BACK2}, in the left foreground; in the doorway of the workshop on screen right {CARP}, one hand on the edge of the door, framed from the knees up with clear space above his head, his face three-quarter to screen left toward the young man, never the lens; scornful: eyes narrowed, a cold sneer at one corner of his mouth, teeth barely showing, lips moving between words; behind him only the dark inside of the workshop; {NOBLADE}",
         lines=[("shimujiang", "縣令要的？那就叫縣令自己來敲門。", "冷笑，反問")],
         motion="Carpenter Shi starts pushing the door shut toward screen left as he speaks; the young man in the foreground bends a little and sets the wooden plane down on a wooden block beside the door, his head never turning toward us",
         zh="過肩中景、慢推：前景左只有許硯的後腦與藍灰袍肩（不點名、不送圖）；石木匠在門口（畫右）一手扶門板，瞇眼冷笑說（本鏡可以冷笑），一邊把門往左推要關；前景許硯把刨子放到門邊木墩上，頭不轉"),
    # Converted: from close behind her; the door straight ahead of her so that her arm reaches straight forward.
    dict(loc="lane", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "shimujiang"], nospeak=["tangxiaotang"], night="day",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, stepping up to the half-shut wooden door straight ahead of her; in the gap of the door facing us Carpenter Shi, in his faded brown cross-collared work jacket and leather apron, framed from the chest up with space above his head, his face three-quarter to screen left toward her, never the lens; taken aback and wary: brows up, eyes narrowed, lips pressed shut; behind him only the dark inside of the workshop; {NOBLADE}; exactly two people",
         lines=[("tangxiaotang", "石師傅，先別關。紙賣出去，進帳分您一成。", "很穩，不笑")],
         motion=f"her right arm reaches straight forward and her palm presses flat against the closing door; the door stops; {HEADSTILL}; {quiet('Carpenter Shi')}",
         zh="【改背後拍】過肩中景、慢推：前景左只有唐小棠的後腦與肩；門在她正前方，她右手直直往前、手掌按住正要關上的門板，門停住，頭始終不轉；門縫裡的石木匠愣住、嘴閉著。稿子三人（許硯在左），真人版許硯在畫左外。台詞 nospeak，剪接放錄音"),
    dict(loc="lane_c", cam="Close-up, slow push in", chars=["shimujiang"], night="day",
         comp="close-up through the gap of a wooden door open only a hand's width: one narrowed suspicious eye, the grey stubble and the deep frown lines of Carpenter Shi, his face three-quarter to screen left toward the two of them off screen left, never the lens; distrustful: brow knotted, lips moving between words, no smile; behind him only the dark inside of the workshop",
         lines=[("shimujiang", "空口白話，秀才家的人最會說。", "不信，哼一聲")],
         motion=f"his eye flicks from one of them to the other and he snorts, his whole face staying in the gap of the door; {NOSMILE}",
         zh="近景、慢推：門只開一掌寬，門縫裡石木匠一隻瞇著的眼和灰鬍渣，從許硯瞪到唐小棠（都在畫左外），哼一聲說；不笑"),
    # Converted: from close behind her; the last page edge-on, the ink box up.
    dict(loc="lane", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "shimujiang"], nospeak=["tangxiaotang"], night="day",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, standing at the wooden door straight ahead of her, open only a hand's width; in the gap facing us Carpenter Shi's narrowed eye, grey stubble and the edge of his leather apron, his face three-quarter to screen left toward her, never the lens; suspicious, lips pressed shut; {NOBLADE}; exactly two people",
         lines=[("tangxiaotang", "那就寫成契約按手印。紙，就用我帳冊最後一頁。", "精明，不給退路")],
         motion=f"the young woman holds {LEDGER}, open at its last page, straight up in front of her toward the gap, the page turned edge-on so nothing on it can be seen, then raises {INKBOX} in her other hand beside it; {HEADSTILL}; {quiet('Carpenter Shi')}",
         zh="【改背後拍】過肩中景、慢推：前景左只有唐小棠的後腦與肩；門縫在她正前方，她把帳冊翻到最後一頁直直舉向門縫（紙側對鏡頭、看不到字），再舉起小圓紅印泥盒，頭始終不轉；門縫裡石木匠一隻眼、嘴閉著。台詞 nospeak，剪接放錄音"),
    dict(loc="lane", cam="Medium shot, slow push in", chars=["shimujiang"], night="day",
         comp=f"medium shot: {CARP}, standing in the wide-open doorway of the workshop on screen right, framed from the knees up with clear space above his head, his face three-quarter to screen left toward the young man off screen left, never the lens; testing: chin up, brows raised, eyes hard, lips moving between words, no smile; behind him only the dark inside of the workshop; {NOBLADE}",
         lines=[("shimujiang", "一成先不說。竹簾要多密，你畫得出來？", "考人")],
         motion=f"Carpenter Shi pulls the door wide open, folds his arms and lifts his chin, then unfolds one arm and holds out one open calloused palm; {NOSMILE}",
         zh="中景、慢推：石木匠把門整個拉開，雙手抱胸、下巴抬高，再放下一手攤開粗手掌說；不笑"),
    # The workbench under the eave (the live picture has no interior). Tang's silent face: neutral sentence in spec.json.
    dict(loc="bench", cam="Medium shot, slow push in", chars=["xuyan", "shimujiang", "tangxiaotang"], night="day",
         comp=f"medium shot past pale wood shavings on the near edge of the workbench in the foreground: on screen left {XU2}, framed from the waist up with clear space above his head, his face three-quarter to screen right toward the carpenter, never the lens; eager: brows lifted, eyes on the board, lips moving between words, no smile; on screen right across the bench {CARP}, leaning in, his face three-quarter to screen left, lips pressed shut, no smile; at the far left end of the bench behind Xu Yan, Tang Xiaotang {TANG}, {GOLD}, writing with a small brush in an open account book, the page edge-on to us, her eyes on the page, lips closed, no smile; {NOBLADE}; exactly three people",
         lines=[("xuyan", "我畫給您看。一寸寬，要排二十根細竹絲。", "有把握")],
         motion=f"Xu Yan picks up a charcoal stick, pulls the long planed board toward him and bends over it to draw; Carpenter Shi leans in to look; Tang Xiaotang writes; {quiet('Carpenter Shi and Tang Xiaotang', 'their', True)}",
         zh="中景、慢推、前景工作台上的刨花（真人場景圖只有屋簷下的工作台，「工坊裡」改成簷下工作台）：許硯（左）拿起炭條、把刨平的長木板拉到面前彎腰畫，說話；石木匠（右）探頭看、嘴閉著；唐小棠在許硯身後工作台左端低頭拿小毛筆寫字（紙側對鏡頭）、嘴閉著、不笑"),
    dict(loc="bench_c", cam="Insert close-up, high angle, slow push in", chars=[], night="day",
         comp="insert high-angle close-up, the shot opens directly on the long planed wooden board on the workbench and one man's right hand in a faded blue-grey cuff holding a black charcoal stick, from its very first frame; only the hand, the cuff, the charcoal and the board are in the frame, no face; warm sunlight",
         lines=[("xuyan", "中間這裡，再用細絲編一片柳葉。", "點著木板")],
         motion="the charcoal draws a rectangular frame on the board and fills it with many fine close parallel lines, then draws one small willow leaf in the middle; only lines, no characters, no writing anywhere on the board",
         zh="插鏡、俯拍、慢推（第一格就是木板特寫）：許硯的右手（藍灰袖口）拿炭條在刨平的木板上畫一個木框、框裡一條條很密的細線，最後在正中間畫一片小柳葉；只有線條沒有字；台詞畫外，剪接放錄音"),
    dict(loc="bench_c", cam="Close-up, slow push in", chars=["shimujiang"], night="day",
         comp=f"close-up of {CARP}, bending over the workbench, framed from the chest up with space above his head, his face three-quarter to screen left, never the lens; puzzled and suspicious: brows knotted tight, eyes narrowed, lips moving between words, no smile; behind him only the dark wooden wall with tools hanging on it",
         lines=[("shimujiang", "編柳葉做什麼？紙上又不能畫畫。", "皺眉，不解")],
         motion=f"Carpenter Shi presses one thick finger on the drawing on the board, then lifts his eyes and glares toward the young man off screen left; {NOSMILE}",
         zh="近景、慢推（身後只有掛工具的木牆）：石木匠彎腰湊近木板，粗手指按在柳葉上，抬眼瞪畫左外的許硯說；不笑"),
    dict(loc="bench_c", cam="Close-up, slow push in", chars=["xuyan"], night="day",
         comp=f"close-up of {XU2}, framed from the chest up with space above his head, holding up the long planed board, his face three-quarter to screen right toward the carpenter off screen right, never the lens; earnest and sure: brows level, eyes bright, lips moving between words, no smile; behind him only the sunny lane",
         lines=[("xuyan", "抄出來的紙，對著光就看得到柳葉。柳溪的紙，一看就認得。", "認真，有把握")],
         motion=f"Xu Yan tilts the board up toward the sunlight from screen left and taps the little leaf twice with the charcoal stick; {NOSMILE}",
         zh="近景、慢推：許硯把木板轉向畫左來的陽光，用炭條點兩下柳葉，對畫右外的石木匠說；認真、不笑（稿子是門口的光）"),
    dict(loc="bench_c", cam="Close-up, slow push in", chars=["shimujiang"], night="day",
         comp=f"close-up of {CARP}, framed from the chest up with space above his head, holding the long planed board up close to his face, his face three-quarter to screen left, never the lens; grudgingly won over: his knotted brows slowly loosening, one corner of his mouth twitching once, never a smile, teeth never showing, lips moving between words; behind him only the dark wooden wall with tools hanging on it",
         lines=[("shimujiang", "這麼密，還藏一片葉子……有點意思。", "不情願地服氣")],
         motion="Carpenter Shi lifts the board close to his face and studies the drawing; his brows slowly loosen and one corner of his mouth twitches once",
         zh="近景、慢推：石木匠把木板拿到臉前細看，眉頭慢慢鬆開、嘴角抽一下（不笑、不露牙）說。稿子角落唐小棠寫字的手不拍"),
    dict(loc="bench_c", cam="Insert close-up, slow push in", chars=[], night="day", act=3,
         comp=f"insert close-up, the shot opens directly on the top of the workbench from its very first frame: one page torn out of an account book lying flat, its visible side completely blank, thick and opaque, lit from the front by warm sunlight, no characters, no writing and no marks on it; beside it {INKBOX} standing open, full of red ink paste; one rough calloused thumb of an older man; only the thumb, the paper, the box and the wood are in the frame, no face",
         lines=[],
         motion="the thumb dips into the red ink paste, presses down hard on the blank page and lifts away, leaving one red thumbprint, the only mark on the paper",
         zh="插鏡、慢推（第一格就是工作台上撕下的一頁帳冊紙，看得到的那面整張空白、正面打光、不透光）：旁邊打開的小圓紅印泥盒；石木匠的粗拇指沾紅印泥、用力按下、抬起，留下一個紅手印，紙上只有這一個印（無台詞）"),
    dict(loc="bench", cam="Medium shot, slow push in", chars=["shimujiang"], night="day",
         comp=f"medium shot: {CARP}, at the right end of the workbench beside the bundle of plain green bamboo poles, framed from the knees up with clear space above his head, his face three-quarter to screen left toward the young man off screen left, never the lens; gruff: brows down, jaw set, lips moving between words, no smile; behind him only the dark wooden wall; {NOBLADE}",
         lines=[("shimujiang", "明晚，給你一張。少一根絲，你拿回來砸我。", "粗聲，答應了")],
         motion=f"Carpenter Shi wipes the red ink off his thumb onto his leather apron, turns, pulls one long plain green bamboo pole out of the bundle and thumps its end on the ground once; {NOSMILE}",
         zh="中景、慢推：石木匠在工作台右端，把拇指上的紅印泥抹在皮圍裙上，轉身從那捆竹竿裡抽出一根長竹竿往地上一頓，粗聲說；不笑"),
    # Converted: from behind both as they walk away down the lane; she taps the book, he turns his face to her in profile.
    # Xu Yan may smile here, lips closed (the script gives her a wink; live gives him the smile).
    dict(loc="lane", cam="Medium two-shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="day",
         comp=f"medium two-shot from behind as the two of them walk away from us along the sunny lane toward the distance on screen left: on the left {TBACK}, {LEDGER} tucked under her left arm; on the right {XU2}, seen from behind at first, then his face turning to her in profile toward screen left, never the lens; pleased: a small closed-lipped smile, lips closed the whole shot; {NOBLADE}; exactly two people",
         lines=[("tangxiaotang", "契約我夾在帳冊裡。以後請人，都照這個規矩。", "小聲，得意")],
         motion=f"as they walk she pats the account book under her arm twice; he turns his face to her in profile and gives her a thumbs-up beside his shoulder; she keeps her head facing forward, the back of her head toward us the whole shot; {quiet('Xu Yan')}",
         zh="【改背後拍】雙人中景、慢推（從背後拍兩人沿巷子往畫左遠處走）：左是唐小棠的後腦與肩，邊走邊拍兩下臂下的帳冊，頭始終朝前；右許硯轉頭側臉看她、在肩旁比一下大拇指（本鏡可以嘴閉著笑）、不說話（結尾）。稿子是兩人往門口走的跟拍、唐小棠得意眨眼。台詞 nospeak，剪接放錄音"),
    # ---- scene 3: the night yard, then the bamboo grove (the grave on screen right, Xu Yan hiding on screen left).
    # Point of view: no person and no hand in the foreground (bible rule 2).
    dict(chapter="竹林", loc="nyard", cam="Point-of-view medium shot, slow push in", chars=["qinshuang"], night="night", act=4,
         comp=f"point-of-view shot through the narrow gap of a half-open dark wooden house door, the dark door edges soft in the foreground on both sides, nobody in the foreground, no hand; out in the yard Qin Shuang, {QIN}, one small bundle of dark blue cloth tucked under her left arm, walking from screen left to screen right through the warm glow of the lantern, framed full length, her face in profile toward screen right, never the lens; tense and quiet: brows drawn, lips closed, no smile; {NOBLADE}; she is the only person in the yard, carrying no lantern",
         lines=[],
         motion="Qin Shuang glances back toward the house for a moment, then pulls the yard gate on screen right open and slips out; the gate swings shut behind her",
         zh="主觀（許硯從門縫往外看）、慢推、前景虛掩的門縫（前景沒有人、沒有手）：秦霜（左臂夾一個小藍布包、不提燈籠、腰帶什麼都沒插）由左往右走過燈籠光，回頭看一眼屋子，拉開院門閃身出去，院門盪回來（無台詞；稿子的火摺子不拍）"),
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU}, standing in the dark just inside the house door, framed from the chest up with space above his head, one thin strip of warm lantern light from the gap of the door falling across one of his eyes, his face three-quarter to screen right, never the lens; uneasy and resolved: brows drawn, eyes narrowed, lips closed; behind him only the dark room",
         lines=[("xuyan", "這麼晚帶著紙錢出門，我得跟去看看。", "低，起疑", "inner")],
         motion=f"Xu Yan reaches up and takes {LANTERN} down from a hook beside the door, cups his right sleeve around it to hide the light, and pushes the door open; {SILENT_HE}; he is thinking, not speaking; {NOSMILE}",
         zh="近景、慢推（身後只有屋裡的暗處）：許硯（外披舊灰外衣）站在門內，門縫的一道燈籠光橫過一隻眼；他從門邊掛鉤取下一盞空白紙燈籠、用右袖半遮燭光、推門跟出去；嘴一直閉著（心裡話，剪接放錄音）"),
    dict(loc="grove", cam="Wide shot, slow pan right", chars=["xuyan"], night="grove", act=4,
         comp=f"wide shot past a row of bamboo stalks in the foreground, keeping him in the frame as he moves from screen left to screen right: only Xu Yan is in the frame, {XU}, {LANTERN} in his left hand with his right sleeve cupped around it so only a little light leaks out, crouching low between the bamboo stalks, framed full length with space above his head, his face in profile toward screen right, never the lens; tense: eyes wide, lips closed, no smile; the one lantern in his hand is the only lantern; {NOBLADE}; nobody else anywhere in the grove",
         lines=[],
         motion=f"Xu Yan creeps from one bamboo stalk to the next, stops to listen, then moves on toward screen right; {SILENT_HE}",
         zh="全景、慢慢往右搖（由左往右）、前景一排竹竿：竹林裡只有許硯一個人，左手提燈籠、右袖遮著光、壓低身子在竹竿之間往前躲，停一下聽再往前；燈籠只透一點光（無台詞）"),
    # Nobody named: she is small, from behind (bible rule 2; the original e013 had an extra figure with a lantern here).
    dict(loc="grove", cam="Extreme wide high-angle shot, slow push in", chars=[], night="grove", act=4,
         comp=f"extreme wide high-angle shot looking down into the small clearing: the small earthen grave mound with its blank wooden marker board, and kneeling in front of it with her back to us one young woman in a dark brown short jacket with a high ponytail, small in the frame, seen only from behind, her face never visible; in front of her {PAPERFIRE}; nobody else anywhere, no lantern, no torch, no other light; {NOBLADE}",
         lines=[],
         motion="the kneeling woman bows slowly until her forehead touches the ground, then straightens up; ash from the burning paper drifts up in the wind",
         zh="大全景、高角度、慢推（稿子是慢慢往下降；gen-dh 不認升降，寫成推近）：空地上一座小土墳、空白木牌；只有秦霜一個人背對鏡頭跪在墳前（小、不點名、不送圖），面前一小堆紙錢火；她慢慢磕頭到地、再直起身，紙灰被風吹得往上飄；沒有燈籠、沒有別的人影（無台詞）"),
    dict(loc="grove_c", cam="Close-up, slow push in", chars=["xuyan"], night="grove",
         comp=f"close-up of {XU}, half hidden behind one thick bamboo stalk, framed from the chest up with space above his head, the faint glow of the lantern held low behind him lighting only his chin, his face three-quarter to screen right toward the clearing off screen right, never the lens; stunned and moved: eyes wide, brows drawn up, holding his breath, lips closed the whole shot; behind him only bamboo stalks and darkness",
         lines=[("xuyan", "沒有名字的墳，她半夜一個人來燒紙。", "很輕，心裡一沉", "inner")],
         motion=f"Xu Yan draws the lantern behind his back with his left hand and presses his right hand against the bamboo stalk, holding his breath; {SILENT_HE}; he is thinking, not speaking; {NOSMILE}",
         zh="近景、慢推（身後只有竹竿與暗處）：許硯半躲在一根粗竹後，燈籠的一點光只照到下巴；左手把燈籠往身後藏、右手按住竹子、屏住呼吸；嘴一直閉著（心裡話，剪接放錄音）、不笑"),
    dict(loc="grove_c", cam="Medium close-up, slow push in", chars=["qinshuang"], night="grove",
         comp=f"medium close-up of Qin Shuang, {QIN}, kneeling in front of the small grave mound on screen right, framed from the chest up with space above her head, her face in profile toward screen right toward the grave, never the lens; the warm glow of {PAPERFIRE} on her face from below and cold blue starlight from above; grieving: eyes wet and lowered, brows drawn, lips trembling and moving softly between words, no smile; her high ponytail down her back; behind her only bamboo shadows; {NOBLADE}",
         lines=[("qinshuang", "再等等。我一定會把他找回來。", "很輕，對著墳，壓著哽咽")],
         motion=f"Qin Shuang feeds one small square of plain blank paper into the little fire, lets it go and bows her head; {NOSMILE}",
         zh="中近景、慢推（身後只有竹影）：秦霜跪在墳前（墳在畫右）側臉，下面紙錢火的暖光、上面星光的冷藍；她把一張空白紙錢送進火裡、放手、低下頭，很輕地說；不笑"),
    dict(loc="grove_c", cam="Insert close-up, locked", chars=[], night="grove", act=3,
         comp="insert close-up, the shot opens directly on the dark ground of the bamboo grove strewn with dry fallen bamboo leaves and one dry bamboo twig, from its very first frame; only the ground, the leaves, the twig, one old black cloth shoe and the hem of a faded blue-grey robe are in the frame, no face; cold blue starlight and a faint warm glow",
         lines=[],
         motion="the cloth shoe comes down from screen left onto the twig; the twig snaps in two and the foot freezes where it is",
         zh="插鏡、固定（第一格就是竹林落葉地）：一隻舊布鞋（藍灰袍下襬入鏡）從左邊踩下，乾竹枝「啪」地斷成兩截，腳僵住（無台詞）"),
    dict(loc="grove_c", cam="Close-up, slow push in", chars=["qinshuang"], night="grove", act=3,
         comp=f"close-up of Qin Shuang, {QIN}, kneeling, framed from the chest up with space above her head, at first her face in profile toward screen right toward the grave, never the lens; the warm glow of the little paper fire on her face from below; at first tearful, then cold: eyes wet, then hard and narrowed, lips closed the whole shot; behind her only the grave and the little fire; {NOBLADE}",
         lines=[],
         motion=f"Qin Shuang whips her head round toward screen left at the sound, a glint of tears in her eyes, and the next instant her eyes turn cold and hard; {SILENT_SHE}; {NOSMILE}",
         zh="近景、慢推（身後只有墳與紙錢火）：秦霜猛地回頭（轉向畫左），眼裡淚光一閃，下一瞬眼神冷下來；嘴一直閉著、不笑（無台詞）"),
    # The knife (bible rule 5): one fixed object in her RIGHT hand, already drawn; Xu Yan unnamed from behind (no pictures).
    dict(loc="grove", cam="Medium shot, locked", chars=["qinshuang"], night="grove", act=4,
         comp=f"medium shot from just behind one young man seen only from behind, appearing only once, half hidden behind bamboo stalks on screen left in the foreground: only the back of his black topknot, his shoulder in an old plain grey cloth coat and {LANTERN} held low in his left hand, his face never in the frame; on screen right a few steps away, beside the small grave and its little paper fire, Qin Shuang, {QIN}, springing up from her knees with {KNIFE} in her right hand, its edge forward, framed full length with space above her head, her face three-quarter to screen left toward him, never the lens; fierce: eyes cold and hard, jaw set, lips closed, no smile; the whole movement stays inside the frame; {ONLYKNIFE}; exactly two people",
         lines=[],
         motion=f"Qin Shuang springs up and takes two fast steps toward him, the knife raised in her right hand, never changing hands; the young man stumbles back and his back hits a bamboo stalk, the lantern swinging in his left hand, his head never turning toward us; {quiet('Qin Shuang', 'her')}",
         zh="中景、固定（整個動作留在畫面裡）：前景左只有許硯的後腦、舊灰外衣肩與左手低提的燈籠（不點名、不送圖）；畫右墳邊秦霜一躍而起，右手已經握著舊柴刀（短木柄、刀身比手掌長一點、刀背厚、刃口有缺口；從腰帶拔刀那一下不拍，音效交代），兩步撲向他；他往後一退、背撞上竹竿、燈籠一晃；兩人嘴都閉著；畫面裡沒有別的刀"),
    dict(loc="grove_c", cam="Over-the-shoulder close two-shot, slow push in", chars=["qinshuang"], night="grove",
         comp=f"over-the-shoulder close two-shot from close behind one young man seen only from behind, appearing only once, his back to a thick bamboo stalk on screen left: only the back of his black topknot, his shoulder in an old plain grey cloth coat, {LANTERN} in his left hand lighting her face from below and his right hand raised open beside his head, his face never in the frame; facing us a little right of the middle Qin Shuang, {QIN}, framed from the chest up with space above her head, her face three-quarter to screen left toward him, never the lens; low and cold: eyes locked on him, brows down, lips moving low between words, no smile; {KNIFE} held level in her right hand, its sharp edge stopped one finger's width from the side of his throat, its blunt back outward, not touching his skin; far behind her the small grave with the little paper fire still burning; {ONLYKNIFE}; exactly two people",
         lines=[("qinshuang", "你跟蹤我？從院子一路跟到這裡？", "低而冷")],
         motion=f"Qin Shuang leans in a little closer, the knife level and unmoving in her right hand at his throat; the young man's raised hand trembles; he keeps the back of his head toward us the whole shot; {NOSMILE}",
         zh="過肩雙人近景、慢推（真人版改從許硯背後拍：前景左只有他的後腦、舊灰外衣肩、左手燈籠照亮她的下巴、右手張開舉在頭旁，不點名、不送圖）：秦霜正對我們（畫面中偏右），右手平舉舊柴刀、刃口停在他喉側一指寬、刀背朝外、不碰皮膚，身子往前壓一點，低而冷地說；遠處墳前紙錢還在燒；畫面裡沒有別的刀（結尾，懸念接第 14 集：更鼓三聲）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e013-r2/script.md`（c01–c10 對應 s01–s10、c10b 對應 s11、c11–c41 對應 s12–s42；2026-11-06 的 r2 稿，2026-11-14 從 main 帶進來；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-14）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e011-e020.md`（拍法 1–17 條）。",
    "- 內部工作編號 913（`hailuo/{ff,clips}-dh-e913.json`、`colab/runs/e913/extras.json`、`colab/runs/e913-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e913-dh/`）；發布 slug `zhong-tian-qu-qi-e013-r2`。不放集數、不放片名卡；s01 接第 12 集 s35（同一個院子，天亮了：s34 扶正的那支火把已熄、冒一縷煙，許硯還站在原地）。",
    "- 照第 12 集獨立審稿（`writer-tools/e012-r2/review.md`）改過的寫法一開始就照做：`OFFSCREEN_SPEECH = False`；畫外句、心裡話、系統句與錄音鏡，畫面上每個人寫「says nothing… no mouthing words, no smile」；紙一律空白、正面打光、不透光（帳冊封面素藍布、最後一頁側對鏡頭、契約只看得到空白那面與紅手印、紙錢是空白紙、木板上只有線）；過肩前景頭整個轉開。",
    "- 第 11 集草稿教訓（e911 picks）：每個場景句都寫沒有兵器架、沒有槍、沒有靠著的長桿（石木匠的巷子例外：竹竿是劇情要的，寫成沒有尖、沒有刃、沒有纓的青竹竿）；柿子樹果子只在高處、下面什麼都沒掛（白天院子圖也是滿樹果子）。",
    "- 唐小棠八句台詞（s04、s07、s09、s10、s12、s21、s23、s32）都不露嘴：七句從她背後拍、對方站在她正前方、頭始終不轉，s09 改成她撥小金算盤的手的插鏡；nospeak 放錄音，spec.json 拿掉她三張臉部參考圖與身分句。她不說話的臉（s13、s25）寫戒備或專注、用第 7 集的中性外貌句。",
    "- 兵器：秦霜的柴刀只在 s41–s42（c40–c41）入鏡，一把固定描述的舊柴刀、永遠在她右手、刃口朝喉、刀背朝外；拔刀那一下不拍（腰帶全集寫什麼都沒插，extras.json 拿掉造型句的柴刀）；這兩鏡許硯不點名、不送圖、從背後拍，寫明畫面裡沒有別的刀。其他鏡一律沒有刀。稿子的火摺子不拍。",
    "- 石木匠家：真人場景圖 `set-mujiang-fang-l1` 是巷子加木匠鋪門面、屋簷下一張工作台，沒有屋內；「工坊裡」c24–c30（s25–s31）改在簷下工作台，c27 對著陽光。竹林：`set-zhulin-fen-l1` 墳在中間、空白木牌在右、遠處一座舊屋（匾與兩盞紅燈籠），提示詞寫那邊全暗、燈籠不亮、匾空白，竹林裡的光只有紙錢火與許硯手上那一盞燈籠。",
    "- 交領角色都不能水平翻轉：每鏡用畫左畫右寫死誰在哪；過肩鏡寫明從誰背後拍。",
    "- 長鏡要買的秒數（BUY）：照 36 句錄音核過（`~/mokaair-work/videos/zhong-tian-qu-qi-e913-dh/audio`，見 `r2.py` 的 BUY 註解）。",
]
FOOT = [
    "- **參考圖都有了**（`assets/refs-live/`）：許硯、秦霜、唐小棠（l1 交領）、石木匠（`shimujiang-portrait-l1`，第 2 篇章試鏡，站主照建議選 37002；沒有角度圖）；場景 `set-xujia-yuan-l2`（白天院子）、`set-xujia-yuan-ye-l1`（夜院）、`set-mujiang-fang-l1`、`set-zhulin-fen-l1`。pilot.py 不會停。",
    "- `gen-dh.mjs` 的 SET 不用加：carpenter's workshop、bamboo grove 兩行 CG 時期就有，morning yard、night yard of the Xu farmhouse 也已登記。`build-r2.py` 的 EN 加了 shimujiang（Carpenter Shi）；第 910–912 集重建逐位元相同。",
    "- 新的有聲配角：石木匠，`cast.json` 的聲音從 Alnilam 改成 Gacrux（第 8 集宗鏢頭用 Alnilam；Gacrux 只有第 5 篇章的周員外用，兩人不同篇章），style 照舊（五十五歲、粗啞低沉、脾氣硬）。",
    "- `colab/runs/e913/extras.json`（照 e912：畫面不放字幕、不要霓虹線、珠串與故障效果；拿掉秦霜造型句的柴刀；石木匠的造型句改成宋式交領短工衣、皮圍裙不寫木屑）與 `colab/runs/e913-live/spec.json`（唐小棠八句的鏡拿掉她三張臉部參考圖與身分句；s13、s25 用中性外貌句；過肩與插手的鏡把「只有他一人」改成容許描述裡的背影或手；種子 9131101／9131102）。",
    "- 免費準備：`DRY=1 REFS=~/mokaair-work/videos/zhong-tian-qu-qi-e913-dh/runpod/refs-dh-e913 VIDEO_JSON=docs/videos/zhong-tian-qu-qi-e013-r2/video.json st1-ep.sh 913`（refs-dh-e913 是 refs-dh-e912 的複本：三張夜裡與走廊的佔位連結照舊，石木匠、木匠家、竹林、白天院子都是 refs-dh 本來就有的連結）→ `pilot.py runpod/a/st1 runpod/live/st1 s01…s42` → `retake.py runpod/live/st1 runpod/live/d1 colab/runs/e913-live/spec.json` → `colab-jobs.json` 加 output_path → `preflight-prompts.py`。草稿等 Colab 空出來再拍。",
    "- 配樂：第一場清晨輕 cue（s06 吐槽停一拍）；第二場喜劇輕快 cue（s18 判定說謊一個低音、s29 服氣一個小重音）；第三場安靜冷的 cue（s36 墳一個低音、s39 枯枝斷時音樂停、s41 拔刀一個重音）。音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy. script.md 長鏡清單: c06 and c17 at 8. Filled in after the recordings (see below).
BUY = {}
