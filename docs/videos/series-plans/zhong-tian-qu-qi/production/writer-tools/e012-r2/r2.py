"""Episode 12 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e012-r2/script.md
(c01-c35 = s01-s35; the CG-era r2 script of PR #2024, brought over from main 2026-11-14), including its sections
「這版改了什麼」, 「2026-11-06 審稿後的修改」 and 「真人版的改動（2026-11-14）」, which override the tables. Every line is the
script's, word for word; only the staging changes. Bible: production/r2-bible-e011-e020.md (rules 1-16).

Live action from the first draft, written the way e011-r2/r2.py was written AFTER its independent review (review.md in
../e011-r2): its 16 必改 and the 建議 it adopted are applied here up front, together with the e910 pick lessons
(colab/runs/e910-live/{review-picks-a.tsv,review-picks-b.tsv,pick-review.md}):
- OFFSCREEN_SPEECH = False (bible rule 15): no "<X> speaks off screen" / "the system voice speaks off screen" is appended;
  every shot with an off-screen line, a thought or a system line writes the silence of each person on screen (SILENT_*),
  after the action (e910 s16, s31, s33: the person on screen moved their lips).
- Runners carry only torches (bible rule 16): NOSHARP names scabbards, a plain black sash with nothing hanging from it and
  the other hand empty; ZHAO has no ruler and no sword word (e910 s22, s32, s37, s40 drew sheathed swords). Torch counts are
  written (e910 s22: twenty-odd torches). Close shots: DARK (no torch on a stand, in the ground or on a wall, no brazier;
  e910 s39). The one exception is the plot's torch: a runner drops one in s25 and it is left stuck in the mud by the stone
  table, the only light of scene 3 (bible 12->13); it is written as dropped and unheld, the only one.
- Over-the-shoulder foregrounds are unnamed, not in `chars`, head turned fully away (HU_BACK, HER_BACK; e910 picks: ears,
  cheeks and noses came in). Far or edge figures are written in their own colours and counted (e910 s30: a far figure copied
  the foreground's pink and became a second Tang Xiaotang).
- Tang Xiaotang never speaks on camera: her three lines (c06, c14, c29) are shot from close behind her (TBACK), `nospeak`,
  the recording laid in; spec.json drops her three face pictures and her identity sentence there and the head never turns
  (e910 s30). Her silent face shots (c02, c05, c17, c24) get e907's neutral face sentences in spec.json and a written
  expression (frightened or focused, no smile; the original e012 had her smiling at 「三個都瞞不住」). Costume: the live
  portrait (cross-collared jacket wrapped shut), not the script's t2 high collar and apricot outer jacket (bible rule 4).
- Weapons: Qin Shuang's chopping knife is not shown (extras.json drops it), one plain wooden stick in her RIGHT hand
  (bible: e010-e012); c29's 「木棍換到左手、背小禾」 is not shot (she carries Xiaohe in off screen, see c29). A-ling's dagger
  is not shown: c03 「握著匕首柄的手指一根一根鬆開」 becomes her empty clenched fist opening at her side (e011 c04's way).
- At most three named people (Ref2VA): c05 A-ling out of frame (off screen right); c14 Tang from behind with Xiaohe and Qin;
  c25 Magistrate Hu, Constable Zhao and A-ling; c28 nobody named (Wang Erniu a small backlit figure at the gate, his shout
  laid in, the women and Xiaohe tiny dark figures far off); c29 restaged: from behind Tang Xiaotang at the house door, Xu Yan
  facing her with the certificates, A-ling coming up behind him and looking at him; Qin Shuang with the sleeping Xiaohe on her
  back has already gone in (the script's c29 has five people).
- Qian Yuanwai and Magistrate Hu never share a frame (bible): Qian only in c20-c21 at the gate; c13 the magistrate is only a
  plump hand in a blue-green sleeve from the right edge.
- Paper without writing (bible rule 7, e909): the banknote (tall, pale rice-yellow, thin black ruled border, one square red
  seal, no portrait, not green, not modern money) is always held by a written hand with its plain back toward us; the slip
  「事成，再付」 is shown only from its blank back (the script's faint ink shadows are dropped); certificates folded.
- No blue light and no panel (bible rule 11): c31 and c35's 「臉被藍光照亮」 become his reaction only; panels are overlays.
- Night is night: scenes 1-2 deep night, the moon hidden behind clouds, the lantern and the torches (e011's words);
  scene 3 (`dawn`) the end of the night: the sky just turning deep grey-blue, a thin waning moon low over the roof ridge at
  the back left, one dying torch. The same live night-yard picture (set-xujia-yuan-ye-l1) for all three scenes.
- Nobody is flipped in the edit: every speaker wears a cross collar; sides are written as screen left/right.
- Smiles allowed (the script): c04 the magistrate's cold sneer, c11 Xiaohe's gap-toothed grin, c21 Qian's dry forced laugh,
  c22 Xu Yan's faint wry curl, c31 Xu Yan's closed-lipped smile (frozen in c32). Everywhere else NOSMILE.
State at the junction (e011 r2.py s35): Xu Yan in the old grey outer coat, framed from the chest up, his own right fist at
the lower left gripping the three folded certificates, facing almost toward us, eyes on a point off screen right; Magistrate
Hu half a step behind his LEFT shoulder on screen right, bending to his left ear, face in profile toward screen left. The
three women at the house door (Qin left, Tang middle, A-ling right); the money pouch in the magistrate's LEFT sleeve.
Places: the night yard live picture (refs-live/set-xujia-yuan-ye-l1; gen-dh's SET maps "night yard of the Xu farmhouse").
Every person has a live portrait (xiaohe, erniu, qianyuanwai included). No new picture, no new voice, no new SET or EN entry.
"""
EP = 912  # internal working number; the published slug is zhong-tian-qu-qi-e012-r2
SLUG = "zhong-tian-qu-qi-e012-r2"
EP_TITLE = "一個都不交（重製版 r2）"
OUTLINE_SECONDS = 171.5  # script.md: 171.5 s, 35 shots (62 + 66.5 + 43)
TARGET_MINUTES = [3, 4]
TITLE = "一個都不交｜種田娶妻打天下 第12集（重製版）"
DESCRIPTION = "許硯直起身，正眼看著胡縣令：不換，她們三個，一個都不交。縣令冷笑說名冊明早送州府，被吵醒的小禾跑出屋門，唐小棠臉色發白：一查，三個都瞞不住。縣令甩袖要走，袖裡掉出一個暗紅綢錢袋，小禾撿起來：伯伯，你的袋子掉了！秦霜一棍擋住：當著大家點一點。錢記銀號的銀票五十兩，一張字條：事成，再付。二牛攔住想溜的錢員外，縣令只能說：不查了。臨走他嘀咕：錢是他給的，主意可不是……阿令聽見了。人散了，系統給了造紙術改良，緊接著下強制任務：十日內，白紙一百張；失敗，失去讀寫能力。《種田娶妻打天下》第 12 集（重製版）。"
THUMB = ("一個都不交", "s22")
CHARACTERS = ["xuyan", "aling", "qinshuang", "tangxiaotang", "xiaohe", "erniu", "zhaobutou", "huxianling", "qianyuanwai", "xitong"]
MINOR = {}  # every speaker has a cast.json voice; runners, servants and villagers are silent
MUSIC = "one cue per scene, continuing e011's last cue: a low dark suspense cue of low cello and deep drums in the torchlit yard at night, one warm swelling hit after the young man refuses the trade, one heavy hit as a money pouch drops into the mud, a light playful plucked figure under the little girl's line; then a tense but slightly playful cue of pizzicato strings and wood blocks, one heavy hit on the note's words, one releasing hit when the magistrate gives in, the music dropping out to wind alone for his muttered last words; then a quiet cue of wind, a soft low drone and faint crackling, one light chime under the reward and one deep heavy hit under the penalty before the end; ancient Chinese rural drama, no vocals"

# Scene headers of script.md. All three scenes: the night yard of the Xu farmhouse (the yard gate in the wall on screen right,
# the house door at the back left, the bamboo fence along the left with the villagers behind it, the round stone table in
# the middle, the well at the front right as the live picture has it). The officials are on the right facing left; the
# household at the house door faces right. Close shots use the short `_c` headers. No person's name in a place phrase.
LOC = {
    "nyard": "In the night yard of the Xu farmhouse before the fourth watch: the packed-earth yard trampled to mud, the packed-earth yard wall capped with grey roof tiles on screen right with the plain wooden yard gate standing open in it, the bamboo fence along the left, one round stone table in the middle, the house door at the back left with a woodpile beside it, the persimmon tree, the stone well with its wooden windlass at the front right, one blank paper lantern with no writing hanging under the eaves, nothing written on any board or wall; deep night, the moon hidden behind clouds, the sky black, lit only by the warm glow of the one lantern and flickering orange torchlight, no daylight anywhere",
    "nyard_c": "In the night yard of the Xu farmhouse, deep night, the sky black, lit only by flickering orange torchlight and the glow of one blank paper lantern under the eaves",
    "dawn": "In the night yard of the Xu farmhouse at the very end of the night, before dawn: the packed-earth yard trampled to mud, the yard wall capped with grey roof tiles on screen right with the plain wooden yard gate standing open in it, the bamboo fence along the left, one round stone table with round stone stools in the middle, the house door at the back left, the persimmon tree, the stone well with its wooden windlass at the front right, one blank paper lantern with no writing glowing dimly under the eaves, nothing written on any board or wall; the sky still dark but just turning deep grey-blue, one thin pale waning moon low over the roof ridge at the back left, cold blue-grey light, no sunshine and no daylight yet",
    "dawn_c": "In the night yard of the Xu farmhouse before dawn, the sky just turning deep grey-blue, lit only by cold blue-grey light and the small orange glow of one dying torch",
}
LIGHT = {
    "night": "the deep night, the flickering torchlight and the one lantern glow stay unchanged, the sky stays black",
    "dawn": "the cold grey-blue light before dawn and the one small dying torch flame stay unchanged, no sunrise",
}
# bible rule 15 (e011 review.md 必改 s24/s28/s29): no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object; the descriptions say "one" where it first appears).
XU = "Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe"
CERTS = "three folded marriage certificates of plain red paper, folded shut, only their plain red backs showing, no writing visible"
ALING = "A-ling in her plain grey-white cotton dress with long sleeves and one plain wooden hairpin, no shackles"
SLEEVES = "her long sleeves down over both wrists, no wrist showing, both hands empty"
QIN = "her dark brown cross-collared short jacket, wide plain leather belt with nothing tucked in it, black trousers, leather boots and high ponytail tied with black cord"
STICK = "one plain straight wooden stick about as long as her arm in her right hand"
NOBLADE = "no blade, no knife, no sword, no scabbard and no weapon of any kind anywhere in the frame"
NOSHARP = ("no blade, no knife, no sword, no scabbard, no sheathed weapon at anyone's waist and no spear anywhere in the frame; "
           "every runner wears a plain black cloth sash with nothing hanging from it and holds only one burning torch, his other "
           "hand empty")
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
ABACUS = "one plain wooden abacus as long as her forearm, its frame and beam plain dark wood with no carving, no inlay, no marks and no writing"
GOLD = "the small gold abacus stays hanging at her waist"
TANG_FEAR = "frightened: face pale, eyes wide, lips pressed shut, no smile"
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with two looped buns tied with pink "
         "silk ribbons and pearl pins, two long pink silk ribbons hanging from the buns down over her shoulders, a pink inner "
         "collar at the nape of her neck and her light peach-pink silk shoulders; the back of her head toward us the whole time, "
         "her ear the furthest round her head we ever see, no cheek, no profile and no lips at any moment")
# c07: the foreground at the house door is Tang Xiaotang, unnamed and with no pictures (bible rule 2).
HER_BACK = ("one young woman seen only from behind, appearing only once: only the back of her head with two looped buns tied with "
            "pink silk ribbons and her light peach-pink silk shoulder, soft and dark, her head turned fully away from us, her ear, "
            "cheek and profile never visible, her face never in the frame")
HU_BACK = ("one plump official seen only from behind, appearing only once: his head turned fully away from us toward the man he "
           "faces, only the back of his black gauze futou hat, the back of his neck and his left shoulder in a blue-green official "
           "robe, his ear, cheek and profile never visible, soft and dark")
HU_HAND = ("one plump hand in a wide blue-green official sleeve reaching in from the right edge of the frame, its owner outside "
           "the frame, no second face")
ZHAO = "in his black futou cap and plain black round-collared constable's robe, a plain black cloth sash at his waist with nothing hanging from it"
HU = "in his black official gauze hat and blue-green seventh-rank official robe"
RUNNERS = "yamen runners in ancient Chinese Song-dynasty plain black round-collared robes, black caps and cloth shoes"
VILLAGERS = ("village men in ancient Chinese Song-dynasty plain undyed hemp cross-collared short jackets, cloth head wraps and "
             "cloth shoes, each holding one plain wooden stick")
TORCH = "every burning torch held in one person's hand, none floating, none stuck in the ground"
STICKTIPS = "a row of upright plain wooden stick tips poking up behind the bamboo fence"
DARK = ("darkness and the orange flicker of torches held by people out of the frame; no torch on a stand, in the ground or on a "
        "wall, no brazier")
# The plot's torch (s25 on): dropped by a runner, left stuck in the mud beside the stone table, the only flame of scene 3.
DYING = "one burning torch stuck slantwise in the mud beside the round stone table, dropped and left behind, nobody holding it"
DYING_SMALL = "one torch stuck slantwise in the mud, nobody holding it, its flame small and dying"
DAWN_BACK = "the dim yard in the cold grey-blue light before dawn, nobody else in the yard; no other torch, no lantern on a stand, no brazier"
# The money pouch (e010 c34, in the magistrate's LEFT sleeve since e011), the banknote and the slip (bible: 〈錢〉, rule 7).
POUCH = "one palm-sized pouch of plain dark red silk tied with a drawstring, heavy, no writing and no pattern on it"
MUDDY = "the dark red silk pouch, smeared with mud"
NOTE = ("one tall narrow banknote of pale rice-yellow paper with a thin black ruled border and one square red seal, no portrait, "
        "not green, an old-style paper note")
SLIP = "one small folded slip of plain paper"
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
ONCE = "each person appears only once, nobody else behind them"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
SILENT_SHE = "She says nothing in this shot: her lips stay pressed together from the first frame to the last, her jaw still, no talking, no mouthing words"
SILENT_3 = "None of the three women says anything in this shot: all three keep their lips pressed together from the first frame to the last, no talking, no mouthing words"
SILENT_GIRL = "The little girl says nothing in this shot: her lips stay pressed together from the first frame to the last, no talking, no mouthing words"
# e011 s35's stance, repeated so that s01 opens on the same picture (e011 review.md 必改 s32/s35, bible 11->12).
WHISPER = ("Xu Yan facing almost toward us, turned only a little to screen right, his eyes fixed on a point off screen right "
           "beyond the lens, never the lens; Magistrate Hu, {hu}, half a step behind Xu Yan's left shoulder on screen right, bending "
           "his head to Xu Yan's left ear, his whole head staying in the frame, his face in profile toward screen left")
GIRL = "little Xiaohe, an eight-year-old girl, her hair tousled from sleep, the small straw rabbit tucked into her sash, small cloth shoes"


SHOTS = [
    # ---- scene 1: the night yard, the refusal (the gate on screen right, the house door at the back left).
    dict(chapter="不換", loc="nyard", cam="Medium two-shot, slow push in", chars=["xuyan", "huxianling"], night="night",
         comp=f"medium two-shot, the shot opens on the same moment as the shot before: {XU}, framed from the chest up with space above his head, his own right fist raised in front of his chest at the lower left of the frame, gripping {CERTS}, {WHISPER.format(hu=HU)}; Xu Yan steady and cold: brows level, eyes hard, lips moving low and firmly between words, no smile; Magistrate Hu sly, then thrown: his half-smile freezing and draining away, his lips pressed together; behind them only {DARK}; {NOSHARP}; exactly two people",
         lines=[("xuyan", "不換。她們三個，一個都不交。", "聲音不大，很定，「不換」後停半拍")],
         motion="Xu Yan slowly straightens up, lowers his right fist with the folded certificates to his side, takes half a step away toward screen left and turns toward the magistrate, meeting his eyes squarely, his face three-quarter to screen right; Magistrate Hu straightens too, his whole head staying in the frame, his smile freezing; the magistrate's lips stay closed; Xu Yan does not smile",
         zh="雙人中景、慢推（第一格接第 11 集 s35 同一刻）：許硯胸以上、自己的右拳在畫面左下握三份摺起的婚書，幾乎正對我們；胡縣令在他左肩後（畫右）湊在左耳邊；許硯慢慢直起身、握婚書的右拳放下、往畫左退半步、轉頭正眼看胡縣令說話（不笑）；胡縣令也直起身、臉上的笑僵住、嘴閉著"),
    # The system's three increases, one panel (the script's c02); the women's silence written (bible rule 15).
    dict(loc="nyard", cam="Medium shot, slow push in", chars=["qinshuang", "tangxiaotang", "aling"], night="night",
         comp=f"medium shot past one blank paper lantern with no writing hanging under the eaves in the foreground: at the house door the three women side by side, framed from the knees up with space above their heads, their faces three-quarter to screen right toward the young man in the middle of the yard off screen right, never the lens: on screen left Qin Shuang, {QIN}, {STICK}; in the middle Tang Xiaotang {TANG}, holding {ABACUS} against her chest, {GOLD}; on screen right {ALING}, {SLEEVES}; Qin Shuang moved: her brows easing, one corner of her mouth loosening a little, not a smile; Tang Xiaotang moved: her eyes suddenly wet and shining, lips pressed together, no smile; A-ling still: eyes slowly lifting, lips closed; {NOBLADE}; exactly three women",
         lines=[("xitong", "叮。阿令加三，秦霜加三，唐小棠加二。", "冷，一個一個念清楚")],
         panel=[("阿令 好感 +3 → 18", "panel"), ("秦霜 好感 +3 → 13", "panel"), ("唐小棠 好感 +2 → 17", "panel")],
         motion=f"Qin Shuang knocks the tip of her stick once on the ground; Tang Xiaotang hugs the abacus tighter to her chest; A-ling slowly raises her eyes toward screen right; {SILENT_3}; {NOSMILE}",
         zh="中景、慢推、前景屋簷下空白燈籠：屋門前三人（左秦霜右手木棍、中唐小棠抱素木算盤、右阿令兩袖蓋住手腕）；秦霜木棍往地上一頓、嘴角一鬆（不笑）；唐小棠把算盤抱緊、眼眶一熱、不笑；阿令慢慢抬眼；三人都不說話、嘴一直閉著；系統畫外（剪接放錄音），面板三行"),
    # Converted: no dagger (bible rule 5). Her empty fist opens.
    dict(loc="nyard_c", cam="Insert close-up, slow push in", chars=[], night="night", act=3,
         comp=f"insert close-up, the shot opens directly on one slender left hand at a young woman's side, clenched into a tight fist, her long grey-white cotton sleeve down over the wrist, the grey-white cotton of her dress behind it, from its very first frame; only the hand, the sleeve and the cloth of the dress are in the frame, no face; flickering orange torchlight; {NOBLADE}",
         lines=[],
         motion="the fingers of the fist slowly loosen one by one and the empty hand hangs open and relaxed at her side; the sleeve stays down over the wrist; nothing is in the hand",
         zh="插鏡、慢推（第一格就是手）：阿令垂在身側的左手握著拳、灰白長袖蓋住手腕；手指一根一根慢慢鬆開，空手垂下（稿子的匕首柄不拍，同第 11 集 s04；無台詞）"),
    # Magistrate Hu may sneer here (the script).
    dict(loc="nyard", cam="Medium shot, slow push in", chars=["huxianling"], night="night",
         comp=f"medium shot: Magistrate Hu, {HU}, framed from the knees up with clear space above his head, at first his face three-quarter to screen left toward the young man off screen left, then turning toward the whole yard, his eyes sweeping past the lens, never into it; scornful: a cold sneer at one corner of his mouth, eyes narrowed, mouth wide between words; behind him two {RUNNERS}, each holding one burning torch; {NOSHARP}",
         lines=[("huxianling", "好，有骨氣！名冊明早就送州府，看你護得住幾個！", "冷笑，說給全院聽")],
         motion="Magistrate Hu sneers, steps back one pace, turns toward the whole yard and flings one wide sleeve out, raising his voice",
         zh="中景、慢推：胡縣令冷笑退一步，轉身面向全院、寬袖一甩、提高聲音（本鏡可以冷笑）；身後兩個衙役各一支火把（腰間只有黑布帶）"),
    # A-ling is left out (at most three named; she stands off screen right). Tang's silent face: frightened.
    dict(loc="nyard", cam="Medium shot, tracking", chars=["xiaohe", "qinshuang", "tangxiaotang"], night="night",
         comp=f"medium shot past the dark wooden frame of the house door in the foreground on screen left: {GIRL}, running out of the dark doorway rubbing one eye and squeezing in between Qin Shuang, {QIN}, {STICK}, on screen left, and Tang Xiaotang {TANG}, holding {ABACUS} against her chest, {GOLD}, on screen right; the two women framed from the knees up with space above their heads, their faces three-quarter to screen right toward the yard, never the lens; the little girl looking up past them at the torches in the yard, her face three-quarter to screen right, never the lens; drowsy and puzzled: eyes half shut, brows knitted, mouth moving between words; Tang Xiaotang {TANG_FEAR}; Qin Shuang wary: brows drawn, lips closed; {NOBLADE}; exactly one small child and two women, nobody else",
         lines=[("xiaohe", "好吵喔……這些伯伯半夜來我們家做什麼？", "迷糊，剛睡醒")],
         motion="Xiaohe tugs at the hem of Tang Xiaotang's jacket with one hand and looks up at the torches; Tang Xiaotang's and Qin Shuang's lips stay closed; Tang Xiaotang and Qin Shuang do not smile",
         zh="中景、跟拍、前景屋門門框：小禾（頭髮睡亂、草兔塞在腰帶上、小布鞋）揉著眼睛從暗屋裡跑出來，鑽到秦霜（左，右手木棍）與唐小棠（右，抱素木算盤、臉發白）之間，拉住唐小棠的衣襬、抬頭看滿院的火把說話；兩人嘴閉著、不笑。live：阿令拿掉（一鏡最多三人，她在畫右外）"),
    # Converted: Tang Xiaotang's line from close behind her (bible rule 3), the little girl's face takes it.
    dict(loc="nyard", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xiaohe"], nospeak=["tangxiaotang"], night="night",
         comp=f"over-the-shoulder medium shot at a child's height from close behind {TBACK}, crouching low in the left foreground, a plain wooden abacus pressed under her left arm out of sight; facing us just beyond her, little Xiaohe, the eight-year-old girl with tousled hair, framed from the waist up with space above her head, her face lifted toward the young woman's face, never the lens; puzzled and sleepy: eyes blinking, brows knitted, lips closed; behind them only the dark house doorway; {NOBLADE}; exactly two people in the frame, nobody else",
         lines=[("tangxiaotang", "小禾乖，他們要查名冊……一查，我們三個都瞞不住。", "小聲，發抖")],
         motion=f"the young woman's two hands in peach-pink sleeves rest on the little girl's shoulders and draw her one small step closer, the fingers trembling; she keeps her head still and never turns it, the back of her head toward us the whole shot; Xiaohe blinks up at her; {SILENT_GIRL}; {NOSMILE}",
         zh="【改背後拍】過肩中景（小孩的高度）、慢推：前景左只有蹲著的唐小棠後腦、雙丸子頭、兩條長粉緞帶、粉色內領、淡桃粉衣肩（臉與嘴不入鏡，算盤夾在左臂下看不到）；她兩手搭在小禾肩上把她攬近一步、手指發抖，頭始終不轉；小禾正對我們、抬頭看她、眨眼、嘴閉著不說話。台詞 nospeak，剪接放錄音；spec.json 拿掉她三張臉部參考圖。稿子是唐小棠正面近景"),
    dict(loc="nyard", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="night",
         comp=f"over-the-shoulder medium shot from the house door past {HER_BACK}, in the left foreground; facing us in the middle of the yard on screen right {XU}, {CERTS} in his right fist, framed from the waist up with clear space above his head, his face three-quarter to screen left toward the women at the door, never the lens; low and steady: brows level, eyes calm and hard, lips moving low between words, no smile; behind him only {DARK}; {NOBLADE}",
         lines=[("xuyan", "他敢查，我就讓他不敢查。", "壓低，很穩")],
         motion=f"at first Xu Yan's face is turned to screen right toward the magistrate off screen right; he turns his head back toward the house door and speaks low; then he turns his head back to screen right and his eyes travel slowly down from a hat to a sleeve off screen right; the woman in the foreground keeps her head still; {NOSMILE}",
         zh="過肩中景、慢推：前景左只有唐小棠的後腦、丸子頭與淡桃粉衣肩（頭整個轉開、不點名、不送圖）；許硯在院子中間（畫右）、右拳握婚書，回頭朝屋門壓低聲音說，說完轉回畫右，眼睛把畫外的胡縣令從官帽一路掃到袖子；不笑"),
    dict(loc="nyard", cam="Wide shot, slow push in", chars=["huxianling", "zhaobutou"], night="night",
         comp=f"wide shot past {STICKTIPS} in the foreground: Magistrate Hu, {HU}, walking from the middle of the yard toward the open yard gate on screen right, his face in profile toward screen right toward his men, never the lens; loud and peevish: brows down, mouth wide between words, no smile; beside him Constable Zhao, {ZHAO}, one burning torch in his right hand, lips closed; ahead of them six {RUNNERS} gathering toward the gate at walking pace, each holding one burning torch; no more than eight torches in the frame; {TORCH}; {NOSHARP}",
         lines=[("huxianling", "收隊！明早天一亮，名冊就送州府！", "拉高，甩袖")],
         motion=f"Magistrate Hu takes two steps toward the gate and flings his LEFT wide sleeve out hard; Constable Zhao and the runners walk with him, their lips closed; {NOSMILE}",
         zh="全景、慢推、前景籬笆後的木棍尖：胡縣令從院子中間往畫右院門走兩步，左手寬袖用力一甩（剪在甩袖的一半）；趙捕頭（右手火把、腰間只有黑布帶）在他身邊；六個衙役（每人一支火把、另一手空著）往院門靠攏；火把不超過八支"),
    dict(loc="nyard_c", cam="Insert close-up, slow push in", chars=[], night="night", act=3,
         comp=f"insert close-up, the shot opens directly on the hem of one wide blue-green official sleeve and one black official boot on the trampled muddy ground, from its very first frame; only the sleeve, the boot and the mud are in the frame, no face; flickering orange torchlight",
         lines=[],
         motion=f"the wide sleeve swings hard; {POUCH} slides out of the cuff and drops into the mud beside the boot with a heavy thud; the boot does not stop and walks off out of the frame to screen right; the pouch lies still in the mud",
         zh="插鏡、慢推（第一格就是寬袖與官靴）：藍綠寬袖一甩，暗紅綢錢袋（巴掌大、束口繩、沒有字）從袖口滑出，掉進官靴旁的泥裡；官靴沒停、往畫右走出畫（無台詞）"),
    dict(loc="nyard", cam="Medium shot, tracking", chars=["xiaohe"], night="night",
         comp=f"medium shot tracking from screen left to screen right at a child's height: {GIRL}, running across the trampled mud of the yard from screen left toward {MUDDY} lying in the mud, framed full length with space above her head, her face three-quarter to screen right, never the lens; intent: eyes fixed on the pouch, lips closed; behind her only {DARK}; {NOBLADE}; she is the only child in the frame",
         lines=[("qinshuang", "小禾，回來！那邊都是官差！", "急")],
         motion=f"Xiaohe runs across the mud to the pouch, crouches and stretches out one hand to pick it up; {SILENT_GIRL}; {NOSMILE}",
         zh="中景、跟拍（由左往右，小孩的高度）：小禾跑過泥地，到錢袋旁蹲下伸手去撿（剪在蹲下的一半）；她嘴閉著不說話；秦霜畫外（剪接放錄音）。稿子的唐小棠的手不拍"),
    # Xiaohe may grin here (the script: she does not understand what is going on).
    dict(loc="nyard", cam="Low-angle medium shot, slow push in", chars=["xiaohe"], night="night",
         comp=f"low-angle medium shot from a child's height: little Xiaohe, the eight-year-old girl with tousled hair and the straw rabbit tucked into her sash, standing in the trampled mud in the middle of the yard, framed from the knees up with space above her head, holding {MUDDY} up high in both hands, her face three-quarter to screen right toward the official off screen right, never the lens; proud and innocent: a wide gap-toothed grin showing her one missing front tooth, eyes bright, mouth moving between words; far behind her, soft and out of focus, only {DARK}",
         lines=[("xiaohe", "伯伯，你的袋子掉了！好重喔！", "奶聲，得意")],
         motion="Xiaohe straightens up, turns toward screen right and holds the muddy pouch up high in both hands, grinning",
         zh="低角度中景（小孩的高度往上）、慢推：小禾站在泥地裡，兩手把沾泥的暗紅錢袋舉得高高的，轉向畫右外的胡縣令，缺門牙的嘴笑開說話（本鏡可以笑）；身後只有暗處與畫外人手上的火光"),
    dict(loc="nyard_c", cam="Medium close-up, slow push in", chars=["huxianling"], night="night",
         comp=f"medium close-up of Magistrate Hu, {HU}, framed from the chest up with space above his head, his face three-quarter to screen left toward the child off screen left, never the lens; alarmed: face suddenly ashen, sweat beading on his upper lip, eyes bulging, mouth tight between words, no smile; behind him only {DARK}",
         lines=[("huxianling", "小孩子胡鬧！快，把袋子拿過來！", "聲音發緊")],
         motion=f"Magistrate Hu whips round, lurches forward and thrusts his right hand out toward screen left, his whole head staying in the frame; {NOSMILE}",
         zh="中近景、慢推（身後只有暗處與畫外人手上的火光）：胡縣令臉一下灰了、上唇冒汗，猛回頭往前一撲、右手往畫左伸（頭一直在畫面裡）；不笑"),
    dict(loc="nyard", cam="Medium shot, slow push in", chars=["qinshuang", "xiaohe"], night="night",
         comp=f"medium shot: on screen right Qin Shuang, {QIN}, {STICK}, framed from the knees up with space above her head, her face three-quarter to screen right toward the official off screen right, never the lens; cold: eyes level and hard, jaw set, lips moving firmly between words, no smile; on screen left behind her little Xiaohe holding {MUDDY} against her chest, wide-eyed, lips closed; at the right edge {HU_HAND}; behind them only {DARK}; {NOBLADE}",
         lines=[("qinshuang", "大人別急。掉了什麼，當著大家點一點。", "冷")],
         motion=f"Qin Shuang steps quickly in front of the child and swings the stick across, blocking the plump reaching hand; then she plants the stick tip down into the mud; Xiaohe ducks behind her, her lips closed; {NOSMILE}",
         zh="中景、慢推：秦霜（畫右，右手木棍）兩步搶到小禾前面，木棍一橫擋住畫右緣伸進來的胖手（藍綠官袖，胡縣令的臉不入鏡），再把棍頭往泥裡一插；小禾（畫左）抱著錢袋躲到她身後、嘴閉著（結尾）"),
    # ---- scene 2: the same yard, the pouch.
    # Converted: Tang Xiaotang's line from close behind her; the banknote held up by both ends, its back toward us.
    dict(chapter="錢袋", loc="nyard", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xiaohe", "qinshuang"], nospeak=["tangxiaotang"], night="night",
         comp=f"over-the-shoulder medium shot at a crouching height from close behind {TBACK}, crouching low in the left foreground, a plain wooden abacus under her left arm out of sight; facing us just beyond her, little Xiaohe crouching in the mud, her face three-quarter to screen left toward the young woman, never the lens, wide-eyed, lips closed; standing behind them on screen right Qin Shuang, {QIN}, {STICK}, her face three-quarter to screen right watching the officials off screen right, never the lens, guarded, lips closed; behind them only {DARK}; {NOBLADE}; exactly three people in the frame, nobody else",
         lines=[("tangxiaotang", "錢記銀號的銀票，五十兩整。", "冷，帳房口氣")],
         motion=f"Xiaohe puts the muddy pouch into the young woman's two hands; the young woman unties the drawstring, draws out {NOTE} and holds it up by both ends at the height of her head against the torchlight, its plain back toward us; she keeps her head still and never turns it, the back of her head toward us the whole shot; Xiaohe's and Qin Shuang's lips stay closed; {NOSMILE}",
         zh="【改背後拍】過肩中景（蹲著的高度）、慢推：前景左只有蹲著的唐小棠後腦與肩（臉與嘴不入鏡）；小禾蹲在她前面、把錢袋放進她手裡；她解開束口繩、抽出一張豎長米黃銀票，兩手捏住兩端舉到頭的高度對著火光（紙背朝我們、看不到字），頭始終不轉；秦霜站在後面畫右擋著、看畫右外的官差，嘴閉著。台詞 nospeak，剪接放錄音；spec.json 拿掉她三張臉部參考圖"),
    dict(loc="nyard_c", cam="Insert close-up, slow push in", chars=[], night="night", act=3,
         comp=f"insert close-up, the shot opens directly on {NOTE} held up taut by two slender hands in peach-pink silk sleeves, one hand at each end, from its very first frame; only the two hands, the cuffs and the paper are in the frame, no face; its plain back toward us, the torchlight behind it glowing through the paper so only the faint shadow of the thin black border and of the one square red seal shows, no characters, no numbers and no writing anywhere",
         lines=[],
         motion="the two hands hold the banknote taut by both ends and do not let go; the paper stays still between the hands, the torchlight flickering behind it",
         zh="插鏡、慢推（第一格就是銀票）：唐小棠兩手（桃粉袖口）捏住一張豎長米黃銀票的兩端；紙背朝鏡頭，火光透過來，只看得到黑框線與一方紅印的影子、沒有字、沒有頭像；兩手捏緊不鬆手（無台詞）"),
    dict(loc="nyard", cam="Wide shot, slow push in", chars=["erniu"], night="night",
         comp=f"wide shot past the top of the bamboo fence in the foreground: just behind the fence Wang Erniu, holding one thick plain wooden stick in both hands, and eight {VILLAGERS}, crouching beside him; Wang Erniu's face three-quarter to screen right toward the yard, never the lens; angry: brows slammed down, eyes wide, mouth wide between words, no smile; the villagers' lips closed; exactly nine men behind the fence, nobody else; {NOBLADE}",
         lines=[("erniu", "錢記？那不是錢員外家開的銀號嗎！", "大嗓門，生氣")],
         motion=f"Wang Erniu springs up from behind the fence; the eight villagers stand up after him one by one and glance at one another; the villagers' lips stay closed; {NOSMILE}",
         zh="全景、慢推、前景籬笆：籬笆後二牛（兩手握粗木棍）一下站起來大聲說，八個村民（宋式粗布短打、布包頭、各一根木棍）跟著站起來、互看、嘴閉著；二牛生氣、不笑；籬笆後一共九人"),
    dict(loc="nyard", cam="Medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="night",
         comp=f"medium shot: in the middle of the yard {XU}, crouching on screen left, {CERTS} in his right hand, his face three-quarter to screen right toward the young woman, never the lens; level and sure: brows level, eyes on the pouch, lips moving between words, no smile; on screen right Tang Xiaotang {TANG}, crouching, {ABACUS} tucked under her left arm, {GOLD}, holding the dark red silk pouch in both hands, her face three-quarter to screen left toward him, never the lens; focused: brows drawn, eyes on the pouch, lips closed, no smile; behind them only {DARK}; {NOBLADE}; exactly two people",
         lines=[("xuyan", "就是他家的。袋子裡，還有一張字條。", "篤定")],
         motion=f"Xu Yan tucks the folded certificates into the front of his robe; Tang Xiaotang slips the folded banknote back into the pouch and hands it to him; he opens it and draws out {SLIP} between two fingers; Tang Xiaotang's lips stay closed; {NOSMILE}",
         zh="中景、慢推：許硯（畫左）蹲到唐小棠（畫右，算盤夾在左臂下、臉專注不笑）身邊，把三份婚書塞進懷裡騰出手；唐小棠把銀票摺好放回錢袋遞給他；許硯撐開袋口、兩根手指夾出一張摺起的小字條，說話；唐小棠嘴閉著"),
    dict(loc="nyard_c", cam="Insert close-up, slow push in", chars=[], night="night", act=3,
         comp=f"insert close-up, the shot opens directly on two fingers of a man's right hand in a faded blue-grey cuff under an old grey cloth sleeve, holding {SLIP}, from its very first frame; only the hand, the cuff and the paper are in the frame, no face; the slip's blank back toward us, the torchlight behind it, no writing, no characters and no marks visible on it",
         lines=[],
         motion="the fingers open the small slip and hold it still, its blank back toward us; nothing on the paper can be read",
         zh="插鏡、慢推（第一格就是字條）：許硯的手指（藍灰袖口、舊灰外衣袖）把小字條打開，紙背朝鏡頭，看不到任何字或墨影（稿子的淡淡墨影不拍；無台詞）"),
    dict(loc="nyard_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"medium close-up slowly becoming a close-up of {XU}, framed from the chest up with space above his head, holding the small open slip of paper beside his face, its blank back toward us, no writing visible, his face three-quarter to screen right, never the lens; deliberate: brows level, eyes on the slip, lips moving word by word, no smile; behind him only the bamboo fence in the torchlight; {NOBLADE}",
         lines=[("xuyan", "袋裡的字條寫著：事成，再付。", "唸給全院聽，一字一字")],
         motion=f"Xu Yan reads out word by word, then lifts his eyes from the slip to the official off screen right; {NOSMILE}",
         zh="中近景推到近景（身後只有籬笆）：許硯把字條拿在臉旁（紙背朝鏡頭、沒有字），一字一字唸給全院聽，唸完抬眼看畫右外的胡縣令；不笑"),
    dict(loc="nyard", cam="Medium two-shot, tracking", chars=["erniu", "qianyuanwai"], night="night",
         comp=f"medium two-shot at the open yard gate: on screen right Qian Yuanwai, his hands an ordinary natural skin tone, hunched and creeping toward the gate, his face three-quarter to screen left toward the big young man, never the lens; caught: eyes darting, mouth shut; on screen left Wang Erniu, holding one thick plain wooden stick in both hands, his face three-quarter to screen right toward Qian, never the lens; blunt and hard: brows down, eyes fixed on him, mouth moving between words, no smile; both framed from the knees up with clear space above their heads; beyond the gate only the dark road; {NOBLADE}; exactly two people, nobody else",
         lines=[("erniu", "錢員外，天還沒亮，您急著上哪去？", "大嗓門，逮到人")],
         motion=f"Wang Erniu takes two strides to the gate and swings the stick across the gateway, barring it; Qian Yuanwai nearly walks into it and freezes; Qian Yuanwai says nothing in this shot, his lips pressed together; {NOSMILE}",
         zh="雙人中景、跟拍（畫面裡沒有胡縣令）：院門邊，錢員外（畫右，深金團花錦袍、一般膚色）縮著脖子往門外溜；二牛（畫左）兩步走到院門前、木棍一橫攔住門口，說話（不笑，是逮到人，不是開心）；錢員外差點撞上、愣住、嘴閉著"),
    # Qian may give a dry forced laugh here (the script).
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["qianyuanwai"], night="night",
         comp=f"close-up of Qian Yuanwai, his hands an ordinary natural skin tone, framed from the chest up with space above his head, his face three-quarter to screen left toward the big young man off screen left, never the lens; guilty: sweat on his forehead, eyes darting, a dry forced laugh between words; behind him only the bamboo fence and the dark gateway",
         lines=[("qianyuanwai", "我、我是出來透透氣……透氣而已。", "心虛，乾笑")],
         motion="Qian Yuanwai wipes his forehead with his wide sleeve and edges half a step back, his whole head staying in the frame",
         zh="近景、慢推（身後只有籬笆與院門）：錢員外額頭冒汗、眼珠亂轉，用袖子擦汗、往後退半步（頭一直在畫面裡），乾笑著說（本鏡可以乾笑）"),
    # Xu Yan may give the faintest wry curl here (the script).
    dict(loc="nyard", cam="Low-angle over-the-shoulder shot, slow push in", chars=["xuyan"], night="night",
         comp=f"low-angle over-the-shoulder shot from close behind {HU_BACK}, in the right foreground; on screen left {XU}, standing at his full height, framed from the waist up with clear space above his head, the small slip between two fingers of his right hand and {MUDDY} in his left hand, his face three-quarter to screen right toward the official, never the lens; cool and pointed: brows level, eyes hard, the faintest wry curl at one corner of his mouth, lips moving between words; behind him only {DARK}; {NOSHARP}",
         lines=[("xuyan", "大人，錢府的銀票從您袖裡掉出來。這名冊，還查嗎？", "慢，帶一點壞")],
         motion="Xu Yan stands up and takes one step toward the official, stopping an arm's length away, the slip raised a little; the official in the foreground keeps still",
         zh="低角度過肩（胡縣令左肩後）、慢推：前景右只有胡縣令的官帽後腦、後頸與左肩（頭整個轉開、不點名、不送圖）；許硯站起來、右手兩指夾字條、左手拿錢袋，往前一步停在一臂外說話（本鏡可以嘴角一點壞笑）"),
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["huxianling"], night="night",
         comp=f"close-up of Magistrate Hu, {HU}, framed from the chest up with space above his head, his face three-quarter to screen left toward the young man off screen left, never the lens; cornered: face streaming with sweat, eyes darting left and right, teeth gritted between words, no smile; behind him only {DARK}",
         lines=[("huxianling", "不、不查了！今晚的事，本官全當沒來過。", "咬牙")],
         motion=f"Magistrate Hu's eyes dart left and right; he mops his forehead with his wide sleeve, his whole head staying in the frame, and grits his teeth; {NOSMILE}",
         zh="近景、慢推（身後只有暗處與畫外人手上的火光）：胡縣令滿臉汗、眼睛左右亂瞄，用寬袖擦額頭、咬牙擠出來；不笑"),
    dict(loc="nyard", cam="Medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="night",
         comp=f"medium shot: on screen right {XU}, framed from the knees up with clear space above his head, facing screen right toward the magistrate off screen right, his face three-quarter to screen right, never the lens; cool: brows level, eyes steady, lips moving evenly between words, no smile; one step behind him on screen left Tang Xiaotang {TANG}, {ABACUS} held against her chest, {GOLD}, her face three-quarter to screen right toward him, never the lens; focused: brows drawn, lips closed, no smile; behind them only {DARK}; {NOBLADE}; exactly two people",
         lines=[("xuyan", "錢袋我們替大人收著。名冊不查，它就不見光。", "淡淡的，對縣令")],
         motion=f"Xu Yan slips the slip back into the pouch, pulls the drawstring tight and, without turning his head, passes the pouch back with his left hand to Tang Xiaotang behind him; she takes it and hugs it against her chest together with the abacus and nods once; Tang Xiaotang's lips stay closed; {NOSMILE}",
         zh="中景、慢推：許硯（畫右）面向畫右外的胡縣令說話，把字條放回錢袋、束好口，頭不回、左手往後把錢袋交給身後一步的唐小棠（畫左）；她接過來跟算盤疊在一起抱在懷裡、點一下頭、嘴閉著、不笑"),
    # The plot's torch: one runner's torch dropped, left stuck in the mud by the stone table (written as already there).
    dict(loc="nyard", cam="Wide shot, slow push in", chars=["huxianling", "zhaobutou", "aling"], night="night",
         comp=f"wide shot past the corner of the round stone table in the foreground, {DYING}: on screen right Magistrate Hu, {HU}, hitching up his robe and hurrying toward the open yard gate, his face in profile toward screen right, never the lens, lips closed; behind him Constable Zhao, {ZHAO}, one burning torch in his right hand, half turned back toward the yard, waving his left arm, mouth wide between words, no smile; six {RUNNERS} filing out through the gate at walking pace, each holding one burning torch; in the middle of the yard {ALING}, {SLEEVES}, her face three-quarter to screen right toward the gate, never the lens, eyes narrowed, lips closed; except the one torch in the mud, every burning torch is held in one person's hand; no more than eight torches in the frame; {NOSHARP}",
         lines=[("zhaobutou", "收隊！火把都跟上，天亮前回縣城！", "不耐煩，喊")],
         motion=f"Magistrate Hu hurries out through the gate; Constable Zhao turns back and waves the men on; the runners file out one after another at walking pace, their torches swaying away; A-ling walks a few steps into the yard after them and stops; Magistrate Hu's and A-ling's lips stay closed; {NOSMILE}",
         zh="全景、慢推、前景石桌桌角：石桌旁泥裡插著一支衙役掉下、沒人撿的火把（稿子寫掉下來的那一下，改成已經插著）；畫右胡縣令提著袍子快步往院門走、嘴閉著；趙捕頭（右手火把、腰間只有黑布帶）回身揮手喊；六個衙役用走路的速度一個接一個出院門（每人一支火把）；阿令從屋門前跟到院子中間停下、看院門、嘴閉著；火把不超過八支"),
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["huxianling"], night="night",
         comp=f"close-up of Magistrate Hu, {HU}, standing under the open yard gate, framed from the chest up with space above his head, half turned back, his face three-quarter to screen left glancing back at the yard, never the lens; sour and muttering to himself: eyes narrowed, mouth twisting, lips moving low between words, no smile; behind him only the dark road beyond the gate and a few small torch flames moving away, each held up by a person too dark and small to make out",
         lines=[("huxianling", "錢是他給的，主意可不是……", "壓低，自言自語")],
         motion=f"Magistrate Hu glances back at the yard and mutters to himself, his whole head staying in the frame; then he turns and hurries away out of the frame to screen right; {NOSMILE}",
         zh="近景、慢推（身後只有院門外的夜路與遠去的火把）：胡縣令在院門下半轉身、回頭瞄院子一眼，壓低聲音自言自語，說完快步往畫右走出畫；不笑"),
    dict(loc="nyard_c", cam="Close-up, slow push in", chars=["aling"], night="night",
         comp=f"close-up of {ALING}, standing in the middle of the yard a few steps from the gate, framed from the chest up with space above her head, her long sleeves down over both wrists, her face three-quarter to screen right toward the yard gate, never the lens; sharp and quiet: eyes narrowing, brows drawn, lips moving very softly between words, no smile; behind her only the bamboo fence in the dark; {NOBLADE}",
         lines=[("aling", "他說主意不是錢員外的。背後還有人。", "很輕")],
         motion=f"A-ling's head snaps toward the gate on screen right and her eyes narrow; she takes half a step toward it and stops, speaking very softly to the young man standing off screen right; {NOSMILE}",
         zh="近景、慢推（身後只有籬笆）：阿令在院子中間、離院門幾步，猛地轉頭看畫右的院門、眼睛瞇起、往前半步又停，很輕地對畫右外的許硯說（許硯在她與院門之間）；不笑（結尾）"),
    # ---- scene 3: the same yard before dawn, the people gone (one dying torch, a thin moon at the back left).
    # Nobody named: Wang Erniu is a small backlit figure at the gate, his shout laid in (off screen in the prompt's sense).
    dict(chapter="人散了", loc="dawn", cam="Extreme wide high-angle shot, slow pull out", chars=[], night="dawn",
         comp=f"extreme wide high-angle shot looking down over the yard wall and the open yard gate on screen right: far off along the dark village road beyond the gate a long line of about fifteen small torch flames moving away to screen right, each held up by a person too small and dark to make out; at the yard gate one burly young man in a coarse brown short jacket, small and backlit, turning back toward the yard and raising one arm, his face too small and dark to see; eight small village men in Song-dynasty short jackets and cloth head wraps, sticks on their shoulders, walking out through the gate after the torches; inside the yard only {DYING_SMALL} beside the round stone table and a few small dark figures near the house door at the back left, too small to see faces; {NOBLADE}; nobody near the camera",
         lines=[("erniu", "許兄弟，我們先回去了，有事你就喊一聲！", "遠，大嗓門")],
         motion="the line of torches moves away along the road at walking pace; the young man at the gate waves once and follows the villagers out",
         zh="大全景、高角度、慢慢拉開（稿子是慢慢升高；gen-dh 不認 crane，寫成拉開）：院門外村路上一長串火把（約十五支，每支在一個人手上、人小到看不清）往畫右走遠；二牛（褐短打、小、背光，不點名、不送圖）在院門口回頭揮手、跟八個扛木棍的村民走出去；院子裡只剩石桌旁那支插在泥裡快熄的火把，屋門前幾個小小的暗影；二牛的喊聲剪接放錄音"),
    # Restaged (five people in the script): from close behind Tang Xiaotang at the house door; Qin Shuang has already carried
    # the sleeping Xiaohe in (the script's 秦霜背小禾、木棍換左手 is not shot). Tang's line laid in, her head never turning.
    dict(loc="dawn", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan", "aling"], nospeak=["tangxiaotang"], night="dawn",
         comp=f"over-the-shoulder medium shot from just inside the dark house door past its wooden frame and {TBACK}, standing on the threshold in the left foreground, the abacus and the dark red silk pouch held against her chest out of sight; facing us one step beyond her in the yard {XU}, framed from the waist up with clear space above his head, his face three-quarter to screen left toward her, never the lens; tired and gentle: eyes soft, lips closed, no smile; two steps behind him on screen right {ALING}, {SLEEVES}, framed from the knees up, her face three-quarter to screen left toward him, never the lens, eyes on him, lips closed; behind them {DAWN_BACK}; {NOBLADE}; exactly three people in the frame",
         lines=[("tangxiaotang", "錢袋跟婚書，我都鎖進錢箱裡。你也早點睡。", "低")],
         motion=f"Xu Yan takes the three folded red certificates from the front of his robe and holds them out; the young woman takes them with her right hand and lays them against the pouch at her chest; she keeps her head still and never turns it, the back of her head toward us the whole shot; A-ling stops behind him and looks at him; Xu Yan's and A-ling's lips stay closed; {NOSMILE}",
         zh="【改背後拍】過肩中景、慢推、前景屋門門框：前景左只有站在門檻上的唐小棠後腦與肩（臉與嘴不入鏡，算盤與錢袋抱在胸前看不到）；許硯在院子裡正對我們，從懷裡掏出三份婚書遞給她，她右手接過疊在錢袋上，頭始終不轉；阿令從院子中間走回來，停在他身後兩步（畫右）看著他、嘴閉著。台詞 nospeak，剪接放錄音；spec.json 拿掉她三張臉部參考圖。live：稿子一鏡五人，秦霜背著睡著的小禾已先進屋（不拍）"),
    dict(loc="dawn", cam="Medium shot, slow push in", chars=["xuyan"], night="dawn",
         comp=f"medium shot past {DYING_SMALL} in the left foreground: {XU}, alone in the yard, dropping down onto a round stone stool beside the round stone table, framed from the knees up with clear space above his head, his face three-quarter to screen right, never the lens; worn out: shoulders slumping, eyes heavy, lips closed; behind him {DAWN_BACK}; {NOBLADE}",
         lines=[("xuyan", "總算過了一關……系統，這回總該給點好東西了吧？", "累，鬆一口氣", "inner")],
         motion=f"Xu Yan drops down onto the stone stool, braces both hands on his knees and lets out a long breath, then lifts his eyes to the empty air in front of him; {SILENT_HE}; he is thinking, not speaking; {NOSMILE}",
         zh="中景、慢推、前景左那支插在泥裡快熄的火把：許硯一個人一屁股坐到石桌邊的石凳上，兩手撐膝、長長吐一口氣、抬頭看面前的空氣；他不說話、嘴一直閉著（心裡話，剪接放錄音）"),
    # Xu Yan may smile here, lips closed (the script). No blue light (bible rule 11).
    dict(loc="dawn_c", cam="Close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"close-up of {XU}, sitting, framed from the chest up with space above his head, his two hands together in front of his chest, his face three-quarter to screen right, never the lens; pleased: brows lifting, eyes brightening, the corners of his mouth slowly curling up into a closed-lipped smile, lips closed the whole shot; behind him only the bamboo fence and the deep grey-blue sky before dawn",
         lines=[("xitong", "叮。獲得：造紙術改良。", "冷")],
         panel=[("獲得：造紙術改良", "reward")],
         motion=f"Xu Yan's brows lift; he rubs his palms together in front of his chest and the corners of his mouth slowly curl up; {SILENT_HE}",
         zh="近景、慢推（身後只有籬笆與發青的天）：許硯眉毛一挑、搓搓手、嘴角慢慢翹起來（本鏡可以笑，嘴閉著）；他不說話、不動嘴；系統畫外，面板疊上。不寫藍光、不寫面板"),
    dict(loc="dawn_c", cam="Close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"close-up of {XU}, sitting, framed from the chest up with space above his head, his two hands together in front of his chest, his face three-quarter to screen right, never the lens; at first a closed-lipped smile, then stunned: the smile freezing and draining from his face, eyes going wide, lips closed the whole shot; behind him only the bamboo fence and the deep grey-blue sky before dawn",
         lines=[("xitong", "強制任務：十日內，白紙一百張。", "冷")],
         panel=[("強制任務：十日內，白紙一百張", "task")],
         motion=f"the smile freezes on Xu Yan's face and fades; his rubbing hands stop dead in front of his chest; {SILENT_HE}",
         zh="近景、慢推：許硯的笑一下僵在臉上、慢慢退掉，搓手的兩隻手停住；他不說話、嘴一直閉著；系統畫外，面板疊上"),
    dict(loc="dawn", cam="Medium close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"medium close-up of {XU}, framed from the waist up with clear space above his head and his raised hands, his face three-quarter to screen right, never the lens; desperate, then deflated: brows shooting up, eyes wide, then his shoulders sagging, lips closed the whole shot; behind him {DAWN_BACK}; {NOBLADE}",
         lines=[("xuyan", "十天一百張？我連一張竹簾都沒有！", "崩潰", "inner"),
                ("xitong", "那就去找。系統給方子，不給木匠。", "冷，嫌棄")],
         motion=f"Xu Yan springs up from the stone stool, grabs his hair with both hands and turns half round on the spot; then his hands drop to his sides and his shoulders sag; {SILENT_HE}; he is thinking, not speaking; {NOSMILE}",
         zh="中近景、慢推（長鏡，買 10 秒：錄音 8.7 秒，稿子估 8）：許硯從石凳上彈起來、兩手抓住頭髮、原地轉半圈，最後手放下、肩膀一垮；全程嘴閉著、不動嘴（心裡話＋系統吐槽，都是畫外）"),
    dict(loc="dawn", cam="Medium shot, slow push in", chars=["xuyan"], night="dawn",
         comp=f"medium shot: on screen left {DYING_SMALL}; {XU}, alone, walking to it and crouching beside it, framed full length with clear space above his head, his face three-quarter to screen left toward the torch and then lifted toward the paling sky at the upper left, never the lens; tired and resolute: jaw set, eyes steady, lips closed; behind him {DAWN_BACK}; {NOBLADE}",
         lines=[("xuyan", "好，找就找。天一亮，我就去問誰會做竹簾。", "沉，下定決心", "inner")],
         motion=f"Xu Yan crouches by the torch and sets it upright in the mud with one hand; its flame shrinks to a tiny glow; he lifts his eyes to the paling sky; {SILENT_HE}; he is thinking, not speaking; {NOSMILE}",
         zh="中景、慢推：許硯走到畫左那支快熄的火把旁蹲下、把它扶正，火苗小得只剩一點，他抬頭看發青的天；嘴一直閉著（心裡話，剪接放錄音）"),
    # No blue light (bible rule 11): his reaction only; the penalty panel is the overlay.
    dict(loc="dawn", cam="Medium shot, slow push in", chars=["xuyan"], night="dawn",
         comp=f"medium shot: {XU}, standing alone in the middle of the yard beside {DYING_SMALL} on screen left, framed from the knees up with clear space above his head, his face three-quarter to screen right, never the lens; shocked: eyes snapping wide, brows shooting up, his whole body frozen, lips closed the whole shot; behind him {DAWN_BACK}; {NOBLADE}",
         lines=[("xitong", "失敗：失去讀寫能力。", "冷")],
         panel=[("失敗：失去讀寫能力", "penalty")],
         motion=f"Xu Yan has just stood up; his eyes snap wide and he freezes where he stands; {SILENT_HE}; {NOSMILE}",
         zh="中景推到中近景：許硯剛站起來，一個人站在院子中間、畫左是那支快熄的火把；眼睛一下瞪大、整個人僵住；嘴閉著不說話；系統畫外，面板疊上（結尾，懸念接第 13 集）。不寫藍光"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e012-r2/script.md`（c01–c35 對應 s01–s35；2026-11-06 的 r2 稿，2026-11-14 從 main 帶進來；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-14）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e011-e020.md`。",
    "- 內部工作編號 912（`hailuo/{ff,clips}-dh-e912.json`、`colab/runs/e912/extras.json`、`colab/runs/e912-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e912-dh/`）；發布 slug `zhong-tian-qu-qi-e012-r2`。不放集數、不放片名卡；s01 接第 11 集 s35 同一刻（胡縣令在許硯左耳邊說完「交出她一個」）。",
    "- 第 11 集獨立審稿（`writer-tools/e011-r2/review.md`）的必改一開始就照做：`OFFSCREEN_SPEECH = False`，畫外句、心裡話、系統句的鏡，畫面上每個人寫「says nothing… no mouthing words」；衙役只拿火把、腰間黑布帶、沒有刀鞘，趙捕頭不寫鐵尺；過肩前景頭整個轉開；近景背景只有暗處與畫外人手上的火光；人數與火把數寫死。",
    "- 唐小棠三句台詞（s06、s14、s29）都從背後拍、nospeak 放錄音、spec.json 拿掉她三張臉部參考圖，頭始終不轉；她不說話的臉（s02、s05、s17、s24）寫驚慌或專注、用第 7 集的中性外貌句。",
    "- 一鏡最多三個有名字的人：稿子 s05（四人）、s29（五人）超過：s05 阿令在畫右外；s29 改從唐小棠背後拍，許硯與阿令在畫面裡，秦霜背小禾已先進屋。s28 大全景不點名（二牛是院門口一個小小的背光人影，喊聲放錄音）。錢員外只在 s20–s21，跟胡縣令不同框；s13 胡縣令只露一隻伸進來的胖手。",
    "- 兵器：秦霜的柴刀不拍（extras.json），右手一根木棍；阿令的匕首不拍（s03 改成垂在身側的空拳慢慢鬆開）；趙捕頭、衙役沒有刀與刀鞘。",
    "- 紙上沒有字：婚書摺著；銀票是豎長米黃紙、黑框線、一方紅印、沒有頭像，一直拿在寫明的手裡、紙背朝鏡頭；字條只拍空白的紙背（稿子的淡墨影不拍）。",
    "- 夜：第一、二場深夜、月亮藏在雲後、只有燈籠與火把；第三場天快亮、天色發青、一彎下弦月低在左後屋脊上、只剩石桌旁那支插在泥裡快熄的火把（s25 起，劇情要的那一支，寫明沒人拿；其他火把每支一人）。s31、s35 不寫藍光、不寫面板。",
    "- 交領角色都不能水平翻轉：每鏡用畫左畫右寫死誰在哪；過肩鏡寫明從誰的哪一邊肩後拍。",
    "- 長鏡要買的秒數（BUY）：2026-11-14 照 32 句錄音核過（`~/mokaair-work/videos/zhong-tian-qu-qi-e912-dh/audio`）：s22（8.5 秒）、s33（心裡話＋系統吐槽 8.7 秒，稿子估 8）買 10；s04（拖長音 8.1 秒）、s30（6.3 秒）與有台詞又有動作的 16 鏡買 8；其餘 6（見 `r2.py` 的 BUY 註解）。",
]
FOOT = [
    "- **參考圖都有了**（`assets/refs-live/`）：許硯、阿令、秦霜、唐小棠（l1 交領）、許小禾、王二牛、趙捕頭、胡縣令、錢員外；場景 `set-xujia-yuan-ye-l1`（第 10 集畫的夜院；第三場天快亮也用這張，光寫在提示詞裡）。本集不用試鏡，pilot.py 不會停。",
    "- `gen-dh.mjs` 的 SET 表與 `build-r2.py` 的 EN 表都不用加：地點詞只有 night yard of the Xu farmhouse（第 10 集已登記）；說話的人（含小禾、二牛、錢員外）都在 EN 表裡。",
    "- `colab/runs/e912/extras.json`（照 e911：畫面不放字幕、不要霓虹線與故障效果；拿掉秦霜的柴刀、胡縣令官服換宋代寫法、二牛不寫空手、小禾的草兔塞在腰帶上）與 `colab/runs/e912-live/spec.json`（s06、s14、s29 拿掉唐小棠三張臉部參考圖與身分句；s02、s05、s17、s24 用中性外貌句；s07、s13、s22 把「只有他一人／只有這幾人」改成容許描述裡的背影、肩或手；種子 9121101／9121102）已建。",
    "- 免費準備：`DRY=1 REFS=~/mokaair-work/videos/zhong-tian-qu-qi-e912-dh/runpod/refs-dh-e912 VIDEO_JSON=docs/videos/zhong-tian-qu-qi-e012-r2/video.json st1-ep.sh 912`（refs-dh-e912 是 refs-dh-e911 的複本）→ `pilot.py runpod/a/st1 runpod/live/st1 s01…s35` → `retake.py runpod/live/st1 runpod/live/d1 colab/runs/e912-live/spec.json` → `colab-jobs.json` 加 output_path → `preflight-prompts.py`。草稿等 Colab 空出來再拍。",
    "- 本集沒有新的有聲配角：小禾 Leda、二牛 Sadachbia、錢員外 Algenib、胡縣令 Iapetus、趙捕頭 Orus 照 `cast.json`；衙役、家丁、村民都不說話。",
    "- 配樂：接第 11 集最後那首低沉 suspense（s01「不換」後一個暖的重音、s09 錢袋落泥一個重音、s11 小禾那句底下輕一點的俏皮音型）；第二場帶點俏皮的 tension（s19「事成，再付」重音、s23「不查了」鬆開的重音、s26 嘀咕時抽掉只留風聲）；第三場安靜（s31 叮、s35 失敗懲罰一個沉的重音後收）。音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy. script.md 長鏡清單: c33 at 8. Measured 2026-11-14 against the 32 recordings
# (~/mokaair-work/videos/zhong-tian-qu-qi-e912-dh/audio, half a second between lines, against (buy - 0.3) x 1.1, e011's way):
# s22 runs 8.5 s and s33 8.7 s (thought 5.1 + system 3.0) -> 10 (the script's 8 for c33 is too short); s04 8.1 s (the drawl)
# -> 8 (0.4 s spare); s30 6.3 s -> 8. The rest by e008's estimate (lines of 14 characters or more, or 13 with an action, get
# 8): s05 (5.9 s + running out), s06 (5.4 s), s08 (15 + the walk and the sleeve), s13 (15 + the block), s14 (11 recorded,
# but untie, draw and hold up), s16 (14 + standing up), s17 (14 + the tuck, the hand-over and the slip), s20 (13 + the
# strides), s23 (15), s24 (18 + the hand-over), s25 (13 + the file-out), s26 (5.0 s + hurrying away), s27 (15), s28 (16),
# s29 (17 + the hand-over), s34 (17 + the crouch). The rest stay at gen-dh's 6 (s01 3.1 s, s02 4.0, s07 3.5, s10 3.1, s11
# 4.8, s12 3.9, s19 4.0, s21 4.8, s31 2.5, s32 2.6, s35 2.1; the inserts s03, s09, s15, s18 action only).
BUY = {"s04": 8, "s05": 8, "s06": 8, "s08": 8, "s13": 8, "s14": 8, "s16": 8, "s17": 8, "s20": 8, "s22": 10, "s23": 8,
       "s24": 8, "s25": 8, "s26": 8, "s27": 8, "s28": 8, "s29": 8, "s30": 8, "s33": 10, "s34": 8}
