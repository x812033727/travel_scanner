"""Episode 15 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e015-r2/script.md
(c01-c42 = s01-s42; the CG-era r2 script of PR #2024), including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and
「真人版的改動（2026-11-15）」, which override the tables. Every line is the script's, word for word; only the staging changes.
Bible: production/r2-bible-e011-e020.md (rules 1-18).

Live action from the first draft, written the way e014-r2/r2.py stands AFTER its independent review (review.md in ../e014-r2)
and bible rule 18, with the verified e913 retake lessons (colab/runs/e913-live/{fix1,fix2}/review-picks.tsv, pick-review.md):
- OFFSCREEN_SPEECH = False (bible rule 15): every shot with an off-screen line, a thought or a system line writes the silence
  of each person on screen (SILENT_*, quiet()), after the action.
- Bible rule 18: nothing is negated by name. Backgrounds say what is there (bare walls, empty ground, mist, only bamboo);
  the long things people hold are written by their shape (plain wooden staffs smooth and round to both ends); paper is
  blank and lit from the front; a face that must not smile gets things it does (brows knotted, lips pressed flat, a snort,
  a look away), held after the last word. extras.json keeps only "no subtitles, captions or text" and the clear-air line.
- Hand and prop positions are in the composition sentence (the first frame), not only in the action (e913 fix1: actions
  written only in the motion were often ignored).
- Risky faces stay short: Carpenter Shi (s22: written as knotted brows, pulled-down mouth, a snort, never "grudging"),
  Erniu's bad news (s14), Elder Han's moved face (s29) are bought at 6 s.
- Tang Xiaotang never speaks on camera (bible rule 3): her eight lines are inserts of her hand (s02 on the paper stack,
  s05 on the sheet pinned to the post) or shot from close behind her (TBACK, nospeak, spec.json drops her three face
  pictures and her identity sentence): s01, s07, s20, s26, s37, s41. Her silent face (s36, s42) gets e907's neutral face
  sentences in spec.json. Costume: the live portrait l1, cross-collared and closed (bible rule 4; not the script's t2).
- No weapon in this episode (bible rule 5): Qin Shuang's belt is empty all episode (extras.json drops the knife from her look);
  the staffs (Qin Shuang, Erniu, the twelve young men, the four Qian servants) and Elder Han's bamboo walking staff are
  written as plain wooden staffs, smooth and round to both ends (bible rule 17's stick sentence, rule 18's wording).
- No more than three named faces in a shot (bible rule 1): the script's c19 (three villagers plus four named on the ridge)
  keeps only the villagers and a few unnamed onlookers seen from behind; the named ones come in s20-s26.
- Night is night: s01-s08 the shed just before dawn by one candle stub and the grey-blue opening; s31-s35 the grove by cold
  starlight, no lantern (the script: 別帶燈籠).
- Nobody is flipped in the edit: every speaker wears a cross collar; sides are written as screen left/right.
State at the junction (e014 r2.py s42, after its review): the shed at sunset, over-the-shoulder from close behind Tang Xiaotang
(unnamed, hair come loose) in the right foreground, the crumpled guild sheet held up in both hands; Xu Yan facing us straight
ahead of her, the first white sheet in his hands. s01 is the same framing one night later: her back in the right foreground,
seated by the waist-high stack, hair neat again; Xu Yan facing us at the nearer vat, peeling the hundredth sheet.
Places (the coordinator's decisions, 2026-11-15; listed again in script.md 〈真人版的改動〉):
- the shed before dawn: a NEW night picture set-gongpeng-ye-l2, an edit of the day shed set-gongpeng-l2 (e014's redraw)
  relit to one candle stub and the grey-blue before dawn, with the leaning A-frame poles at the far left and the stirring
  stick left in a vat taken out (live-action/screen-test-e015.py, seeds 37011/37012). The old night shed l1 was relit
  from the day shed l1 and still has the floor lattice (a second bamboo mould in the episode of the mould) and the pole
  bundle (e911's spear racks grew in such places). gen-dh SET gets "night work shed" -> dh-set-gongpeng-ye-t1, before
  "work shed"; prep915.sh stops until l2 is in refs-live (pilot.py takes the newest l-version).
- the threshing ground set-dagu-chang-l1 ("threshing ground"), the autumn field set-qiutian-l1 ("autumn stubble field";
  gen-dh SET gets that line before "spring field|...|ploughed field" and before "stream|...|willow", which the field's willow
  would otherwise take), the grove set-zhulin-fen-l3 ("bamboo grove"), the stone bridge set-shiqiao-l1 ("stone bridge").
- the grove picture l3 still has the paper fire of e013/e014 in front of the mound. It is not redrawn: pilot.py takes the
  newest l-version, so an l4 without fire would also go to every later retake of e013 s35-s42 and e014 s01-s09, which need
  the fire. The text matches the picture instead (the e014 review: picture and text agreeing is steadier): a small patch of
  grey ash with a few last dull embers in front of the mound (left from her earlier visit), the only warm light; the two
  close shots that need no grave (s33, s34) drop the grove picture (drop_set) and say only bamboo is behind them (the e913
  yard lesson: a close shot does not need the set picture, and it brings the picture's props).
New face: Elder Han (hanbo-portrait-l1, first appearance), voice Enceladus as cast.json already has it (no shared edit): the
only other Enceladus is Eunuch Chang, who appears only in e060, where Elder Han does not (bible r2-bible-e011-e060.md: Han
e015, e017, e032-e034, e039, e040, e055, e059) -- the cast.json convention of sharing a voice between people who never share
an episode (Charon, Sadaltager, Orus, Fenrir, Rasalgethi). His look in extras.json gets the Song cross collar.
"""
EP = 915  # internal working number; the published slug is zhong-tian-qu-qi-e015-r2
SLUG = "zhong-tian-qu-qi-e015-r2"
EP_TITLE = "一個人的犁（重製版 r2）"
OUTLINE_SECONDS = 225  # script.md: 225 s, 42 shots (18 + 17 + 7)
TARGET_MINUTES = [3, 4]
TITLE = "一個人的犁｜種田娶妻打天下 第15集（重製版）"
DESCRIPTION = "熬了一整夜，蠟燭快燒完，第一百張白紙揭下來：任務完成，系統獎勵的卻是一張曲轅犁圖紙。行會不收，紙就賣給真正用紙的讀書人，明天一早推車進城。天剛亮，打穀場上秦霜帶著年輕人練棍；許硯這才知道，去年冬天牛瘟，全村的牛都死光了，冬麥再種不下去，明年開春全村沒糧。二牛的舅舅打犁頭、石木匠做木架，午後田裡三個漢子拉不動的地，秦霜一個人推著曲轅犁犁完一畝。夜裡竹林墳前，她說這是她娘，墳上沒能寫名字。天亮推紙進城，石橋上錢府的賴三攔路：一車一兩，紙坊賣我，五十兩，橋就通。《種田娶妻打天下》第 15 集（重製版）。"
THUMB = ("一個人的犁", "s25")
CHARACTERS = ["xuyan", "tangxiaotang", "qinshuang", "erniu", "hanbo", "shimujiang", "laisan", "xitong"]
MINOR = {}  # every speaker has a cast.json voice (Elder Han: Enceladus); the young men, villagers and servants are silent
MUSIC = "one cue per scene: a tired but warm cue of soft strings and a low wooden flute before dawn, one bright accent on a chime, sinking low when a young man says all the oxen died, lifting again as a drawing is unrolled; then a rising hopeful cue of strings and drums through an autumn field, swelling as one woman pushes a plough alone, one bright accent on a chime; then a quiet cold cue of a low drone and sparse plucks in a bamboo grove at night; then a low tense cue of muted drums and low strings on a misty stone bridge at dawn, one heavy accent on a demand for money and ending on one held suspended note; ancient Chinese rural drama, no vocals"

# Scene headers. Scene 1 is the shed just before dawn (set-gongpeng-ye-l2, new) and the threshing ground at sunrise
# (set-dagu-chang-l1); scene 2 the autumn field in the afternoon and at sunset (set-qiutian-l1) and the grove at night
# (set-zhulin-fen-l3); scene 3 the stone bridge in the early morning (set-shiqiao-l1). Close shots use the short `_c` headers.
# No person's name in a place phrase; no "courtyard", "yard", "willow"-only field phrases, "stream" or "village lane"
# (gen-dh SET would take another set). Bible rule 18: every place is written as what is there.
SHED_TABLE = ("two big round wooden vats at the left filled with milky white bamboo pulp, a squat stone mortar in the middle, an old "
              "plain wooden table at the right")
SHED_BARE = "the posts and the earthen walls bare, nothing mounted on them and nothing leaning against them"
FLOOR = "the floor is plain packed earth, smooth and empty"
CANDLE = "one short candle burnt down almost to a stub on the old table, its small yellow flame"
STACK = ("a waist-high stack of fresh plain white paper on a low wooden board beside the table, square and neat, every sheet "
         "blank and matte")
POSTSHEET = ("one sheet of plain paper pinned flat to the middle timber post with one wooden peg, thick and opaque, lit from the "
             "front by the candle, completely blank")
GROUND = ("a wide flat threshing ground of packed earth and worn bricks, rows of small conical sheaves of rice straw standing "
          "along its edges, the flat harvested fields and misty hills beyond it")
FIELD = ("a wide harvested rice field of dark earth with short rows of cut rice stubble, a raised grass ridge along its right "
         "side a little higher than the field, one big willow with yellow autumn leaves on the ridge, low tiled farmhouses and "
         "blue hills far off")
GROVE_BAMBOO = "only living bamboo stalks growing straight up all around"
GROVE_BACK = "behind them only dense dark bamboo stalks growing straight up into black night"
EMBERS = ("a small patch of grey ash on the bare earth in front of the mound with a few last dull red embers in it, their faint "
          "warm glow low on the front of the mound, the only warm light")
BRIDGE = ("an old grey stone arch bridge over the misty water, a stone-paved path coming to its near foot from the left, green "
          "bamboo along both banks, a low plank footbridge on short posts across the water at the right, tiled houses on the far "
          "bank")
BAR = "one thick rough log laid across the foot of the bridge as a barrier, each end resting on a low wooden trestle"
LOC = {
    "dawn": f"In the night work shed beside the Xu farmhouse just before dawn: a thatch-and-timber roof on rough wooden posts, open on the right side, a low back wall of packed earth and stone, {SHED_TABLE}; {CANDLE}, the only warm light; {FLOOR}; {SHED_BARE}; beyond the low walls and the open right side only dark roofs and treetops against a cold grey-blue sky just before dawn, still and empty",
    "dawn_c": f"In the night work shed just before dawn, lit only by {CANDLE} and the cold grey-blue sky in the open right side; {SHED_BARE}",
    "ground": f"On the threshing ground of the village at sunrise: {GROUND}; thin white morning mist lying low over the fields; low cold golden sunlight from the far left, long shadows across the ground",
    "ground_c": "On the threshing ground of the village at sunrise, thin white morning mist and low cold golden sunlight from the left",
    "field": f"In an autumn stubble field outside the village in the early afternoon: {FIELD}; clear blue sky, warm slanting afternoon sunlight from the left",
    "field_c": "In an autumn stubble field outside the village in the afternoon, warm slanting sunlight from the left",
    "sunset": f"In an autumn stubble field outside the village at sunset: {FIELD}; the sky turning gold, low golden sunset light from the left, long warm shadows",
    "sunset_c": "In an autumn stubble field outside the village at sunset, low golden sunset light from the left",
    "grove": f"In the bamboo grove behind the village at night: dense tall bamboo on both sides, a small clearing strewn with dry fallen bamboo leaves, a small low earthen grave mound with one short weathered plank stuck upright at its right front, its face bare grey wood, and {EMBERS}; beyond the clearing only more dense bamboo fading into black, {GROVE_BAMBOO}; deep night, a sky full of cold stars through the bamboo tops, cold blue starlight, a light wind in the bamboo leaves",
    "grove_c": f"In the bamboo grove behind the village at night, deep night under cold blue starlight; {GROVE_BACK}",
    "bridge": f"At the near foot of the stone bridge into the county town in the early morning: {BRIDGE}; {BAR}; thin white mist lying on the water; low cold golden morning light from the right",
    "bridge_c": "At the foot of the stone bridge in the early morning, thin white mist on the water and low cold golden light from the right",
}
LIGHT = {
    "dawn": "the one small candle flame and the cold grey-blue before-dawn light stay unchanged",
    "ground": "the thin morning mist and the low cold golden sunlight from the left stay unchanged",
    "pm": "the warm afternoon sunlight from the left stays unchanged",
    "sunset": "the low golden sunset light from the left stays unchanged",
    "grove": "the deep night and the cold blue starlight stay unchanged, the sky stays black",
    "bridge": "the thin mist on the water and the low cold golden light from the right stay unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object).
XU2 = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, the sleeves tied back above his forearms with cloth "
       "strips")
XU_TIRED = f"{XU2}, his eyes red-rimmed from a night awake, his bare forearms pale and puckered from the water"
XU_COAT = "Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe"
QIN = ("her dark brown cross-collared short jacket, wide plain leather belt with nothing tucked in it and nothing hanging from "
       "it, black trousers, leather boots and high ponytail tied with black cord")
QIN_ROLLED = ("her dark brown cross-collared short jacket with the sleeves rolled up to the elbows, wide plain leather belt with "
              "nothing tucked in it and nothing hanging from it, black trousers, leather boots and high ponytail tied with black cord")
ERNIU = "Wang Erniu, in his coarse brown short jacket with the sleeves rolled up, sweat on his brow"
HAN = ("Elder Han, in his faded grey cotton cross-collared long robe, his long white beard down to his chest, his polished old "
       "bamboo walking staff in his right hand")
CARP = ("Carpenter Shi, in his faded brown cross-collared short work jacket with the sleeves rolled up and his worn brown "
        "leather apron, one plain wooden stick through his grey topknot")
LAI = "Lai San, in his grey-brown hemp cross-collared short jacket, his old cloth head wrap pushed crooked to one side"
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
GOLD = "the small gold abacus hanging at her waist"
STAFF = "one plain wooden staff a little taller than a man, smooth and round to both ends"
STICKS = "the only long things anyone holds are plain wooden staffs, smooth and round to both ends"
YOUNG = ("about twelve young village men in Song-dynasty cross-collared coarse hemp short jackets, cloth head-wraps and cloth "
         "shoes, standing in three rows, each holding " + STAFF)
VILLAGERS = ("three village men in Song-dynasty cross-collared coarse hemp short jackets and cloth head-wraps, ropes of plain hemp "
             "across their chests, hauling")
ONLOOKERS = ("a few villagers in Song-dynasty cross-collared hemp jackets and cloth head-wraps standing small and soft on the ridge, "
             "seen from behind and from the side")
SERVANTS = ("four Qian household servants in plain grey Song-dynasty cross-collared short jackets, cloth head-wraps and cloth "
            "shoes, standing in a row behind him, each resting " + STAFF + " on his shoulder")
MOULD = ("one papermaking mould: a flat plain rectangular wooden frame about an arm's length wide filled with very fine, closely "
         "laid thin bamboo strips, one small willow-leaf shape woven into its very middle with finer strips")
WETSHEET = "one wet sheet of fresh plain white paper the size of a book page, matte, thick and completely blank"
SCRAP = "one torn-cornered sheet of plain scrap paper, blank and matte"
CHARCOAL = "one short black stick of charcoal"
DRAWING = ("one torn-cornered sheet of plain paper rolled up loosely, its outside blank")
PLOUGH_OLD = "one old wooden plough with one long straight wooden beam and a dull worn share"
PLOUGH = ("one new curved-beam plough: one wooden beam curved like a drawn bow, a short wooden sole, one new black iron "
          "ploughshare and one smooth polished wooden handle")
CART = ("one wooden wheelbarrow with a single wooden wheel at the front and two long wooden handles, one square bundle wrapped "
        "in brown oilcloth and tied with rope on it")
SLIP = "one small slip of plain paper folded in half, only its blank back toward us, thick and opaque, lit from the front"
NOBLADE = "their hands hold only what is described here, belts and waists plain"
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with two looped buns tied with pink "
         "silk ribbons and pearl pins, two long pink silk ribbons hanging from the buns down over her shoulders, a pink inner "
         "collar at the nape of her neck and her light peach-pink silk shoulders; the back of her head toward us the whole time, "
         "her ear the furthest round her head we ever see, only hair, ribbons and shoulders, her face turned fully away")
LAI_BACK = ("one thin young man seen only from behind, appearing only once: only the back of his head with an old cloth head wrap "
            "pushed crooked and his shoulder in a grey-brown hemp jacket, soft and dark, his face never in the frame")
NOSMILE = "after the last word the lips press flat and the jaw sets, the brows stay drawn, held to the last frame"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
HEADSTILL = "she keeps her head still and never turns it, the back of her head toward us the whole shot"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return (f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, "
            f"no mouthing words, the face set and still")


SHOTS = [
    # ---- scene 1a: the shed just before dawn (open on the right; vats left, mortar middle, table right). s01 = e014 s42's
    # framing one night later: Tang Xiaotang's back in the right foreground, Xu Yan facing us straight ahead of her.
    dict(chapter="第一百張", loc="dawn", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="dawn",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, seated on a low stool in the right foreground beside {STACK}, her right hand (on screen right) resting on top of the stack; facing us straight ahead of her a few steps away, beside the nearer vat a little left of the middle, standing, {XU_TIRED}, framed from the waist up with clear space above his head, {MOULD} standing upright in both his hands with {WETSHEET} lying on it, his face three-quarter to screen right toward her, his eyes on the sheet and then on her just right of the lens, never the lens; worn out and careful: eyes heavy, brows drawn together in concentration, lips pressed shut; at the middle post between them, soft and out of focus, {POSTSHEET}; {CANDLE}; {NOBLADE}; exactly two people",
         lines=[("tangxiaotang", "九十八、九十九……就剩最後一張了！", "啞著嗓子，熬了一夜")],
         motion=f"Xu Yan peels the wet sheet carefully off the mould with both hands and turns toward the stack with it held flat; the young woman taps the edge of the stack twice with her right forefinger (on screen right), counting; {HEADSTILL}; {quiet('Xu Yan')}",
         zh="過肩中景、慢推（第一格接第 14 集 s42 的機位，過了一夜）：前景右只有唐小棠的後腦、雙丸子頭、兩條粉緞帶與淡桃粉衣肩（不點名，spec 拿掉她的臉部圖與身分句），坐在矮凳上、右手按著腰高的白紙堆；許硯（袖子綁起、眼睛熬紅、前臂泡得發白）在她正前方、前面那個紙漿桶邊，兩手捧著竹簾、簾上一張濕紙，小心揭下、轉身往紙堆走；中間棚柱上釘著一張紙（虛焦、空白）；木桌上快燒完的蠟燭頭。唐小棠右手食指點兩下紙邊在數，頭始終不轉；許硯嘴閉著。台詞 nospeak，剪接放錄音"),
    # Converted: an insert of hands on the stack (her line laid in; she may smile, unseen). She is in chars with nospeak (as
    # e014 s42 after its review), so build-r2.py does not mark her recording 畫外 (her hand is in the frame); spec.json drops
    # her three pictures and her identity sentence, so only the set picture is sent.
    dict(loc="dawn_c", cam="Insert close-up, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="dawn",
         comp=f"insert close-up, the shot opens directly on the top of the waist-high stack of fresh plain white paper from its very first frame, every sheet blank and matte, square and neat, warm candlelight on it; one young man's two hands with bare forearms, his blue-grey sleeves tied back above them with cloth strips, laying {WETSHEET} flat on the very top; only the hands, the sleeves and the paper are in the frame",
         lines=[("tangxiaotang", "第一百張！說好十天，我們三天就做完了。", "累到晃一下，還是笑了")],
         motion="the young man's two palms smooth the last sheet flat from its middle to its edges and lift away; then one slender hand in a peach-pink silk sleeve comes in from the right and pats the top of the stack twice",
         zh="【改插鏡】插鏡、慢推（第一格就是腰高的白紙堆頂，燭光）：許硯兩手（綁起袖子的前臂）把最後一張濕紙鋪在最上面、兩掌從中間抹平後拿開；一隻桃粉袖口的手從畫右伸進來拍兩下紙堆；臉不入鏡，台詞剪接放錄音（她說時可以笑，看不到）"),
    # The system and a thought: he says nothing (bible rule 15); no blue light (bible rule 11).
    dict(loc="dawn_c", cam="Close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"close-up of {XU_TIRED}, framed from the chest up with space above his head, his face three-quarter to screen right, never the lens; at first brightening: eyes widening, brows lifting, the corners of his closed mouth starting to rise; behind him only one rough timber post of the shed and the warm candlelight",
         lines=[("xitong", "叮。一百張，完成。獎勵：曲轅犁圖紙。", "冷，宣布"), ("xuyan", "犁？我現在缺的是買紙的人，不是犁。", "嫌棄，自言自語", "inner")],
         panel=[("一百張，完成", "task"), ("獎勵：曲轅犁圖紙", "reward")],
         motion=f"Xu Yan straightens his back and his eyes light up; then the brightness drains away, his mouth corners drop, his brows knot and he squints sideways in disbelief, his lips pressed flat; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（身後只有工棚木柱與燭光）：許硯直起腰、眼睛一亮、嘴角剛要往上，接著亮光退掉、嘴角垮下、皺眉斜眼；全程嘴閉著（系統與心裡話畫外，面板兩行疊上）。不寫藍光"),
    dict(loc="dawn", cam="Medium close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"medium close-up of {XU_TIRED}, standing beside the nearer vat at the left, framed from the waist up with clear space above his head, his face three-quarter to screen right, never the lens; fed up: eyes rolling up, then brows knotted, lips pressed flat; at the rim of the vat beside his right hand a small loose heap of torn scrap paper, every piece blank; on the vat's rim {CHARCOAL}; behind him only the low back wall in the dark; {NOBLADE}",
         lines=[("xitong", "圖紙不退。宿主住在村裡，總要吃飯。", "冷，毒舌"), ("xuyan", "畫就畫，總不能白拿一張圖。", "認命，回一句", "inner")],
         motion=f"Xu Yan rolls his eyes, picks {SCRAP} off the small heap with his left hand and the charcoal off the rim with his right; {SILENT_HE}; he is thinking, not speaking; {NOSMILE}",
         zh="中近景、慢推（身後只有棚後矮牆）：許硯翻個白眼，左手從紙漿桶邊一小堆空白廢紙裡撿起一張破了一角的（不是那一百張），右手拿起桶沿上的炭條；全程嘴閉著（系統吐槽與心裡話畫外，吐槽不出面板）"),
    # Converted: an insert of her hand slapping the pinned sheet (its face out of focus and blank; never called a notice);
    # in chars with nospeak like s02.
    dict(loc="dawn_c", cam="Insert close-up, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="dawn",
         comp=f"insert close-up, the shot opens directly on one rough timber post from its very first frame, {POSTSHEET}, soft and out of focus; only the post, the sheet and a hand are in the frame; warm candlelight from the left",
         lines=[("tangxiaotang", "行會不收，這一百張做出來，要賣給誰？", "累，發愁，不笑")],
         motion="one slender hand in a peach-pink silk sleeve comes in from the right and slaps the pinned sheet once flat with its palm, then stays pressed there, fingers spread",
         zh="【改插鏡】插鏡、慢推（第一格就是棚柱）：柱上用木釘釘著一張紙（虛焦、空白、燭光正面照）；一隻桃粉袖口的手從畫右伸進來，拍一下那張紙、手掌按住不動；臉不入鏡，台詞剪接放錄音（提示詞不寫 notice）"),
    # Over her shoulder (unnamed, no pictures): Xu Yan at the left end of the table answers her.
    dict(loc="dawn", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="dawn",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, standing in the right foreground beside a rough timber post at the right edge of the frame; facing us a step away at the left end of the old wooden table, a little left of the middle, {XU_TIRED}, framed from the waist up with clear space above his head, {SCRAP} spread flat on the table under his left hand and {CHARCOAL} in his right hand, his face three-quarter to screen right toward her, his eyes on her face just right of the lens, never the lens; steady and decided: brows level, eyes firm, lips moving between words; {CANDLE} beside the paper; behind him only the dark vats and the low wall; {NOBLADE}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("xuyan", "不賣行會。賣給真正用紙的人，讀書寫字的。", "啞，篤定")],
         motion=f"Xu Yan smooths the torn scrap flat on the table with his left hand and lifts his eyes to answer her; {HEADSTILL}; {NOSMILE}",
         zh="過肩中景、慢推：前景右只有唐小棠的後腦與肩（不點名、不送圖），站在畫右緣的木柱邊；許硯在她正前方、木桌左端、畫面中偏左，左手把破角的廢紙鋪平在桌上、右手拿炭條，抬眼看她、很穩地答；不笑"),
    # Converted: from behind her, seated by the stack; she lays her head on it (the yawn is in the recording only).
    dict(loc="dawn", cam="Medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="dawn",
         comp=f"medium shot from behind and a little above: {TBACK}, {GOLD}, seated on a low stool beside {STACK}, the stack at her left on screen left, her right hand (on screen right) at the small gold abacus at her waist, her back to us; beyond her only the dark vats, the low back wall and the cold grey-blue sky in the open right side; {CANDLE}; {NOBLADE}; nobody else in the frame",
         lines=[("tangxiaotang", "讀書人都在縣城。等紙乾透，明天一早推車進城。", "啞，打著哈欠交代")],
         motion=f"the young woman flicks one bead of the small gold abacus with her right hand (on screen right); then her shoulders sag and she slowly lays her head sideways on top of the stack of paper at her left, her cheek resting on it with her face turned fully away from us toward the stack, and stays there; the back of her head toward us the whole shot",
         zh="【改背後拍】中景、從背後稍高處、慢推：唐小棠坐在矮凳上、紙堆在她左邊（畫左），右手（畫右）撥一下腰間的小金算盤，肩膀一垮、頭慢慢側靠到紙堆上、臉朝紙堆背對我們，不動了；頭始終不轉向鏡頭（稿子的打哈欠只在錄音）。台詞 nospeak，剪接放錄音"),
    dict(loc="dawn_c", cam="Insert close-up, top-down, slow push in", chars=[], night="dawn", act=3,
         comp=f"insert close-up looking straight down, the shot opens directly on {SCRAP} lying flat on the old wooden table from its very first frame, candlelight on it; one young man's right hand, his blue-grey sleeve tied back with a cloth strip, holding {CHARCOAL} on the paper; only the hand, the sleeve, the paper and the wood are in the frame",
         lines=[("xuyan", "轅彎一下，省一半力，用不著牛也拉得動。", "想通了，心裡話", "inner")],
         motion="the charcoal draws a plough seen from the side in a few thick black strokes: one long beam curved like a drawn bow, a short flat sole and a pointed share; only those few strokes are on the sheet, the rest of it plain and blank",
         zh="插鏡、俯拍、慢推（第一格就是桌上的廢紙與炭條）：許硯右手（綁袖的袖口）拿炭條在破角廢紙上畫犁的側面：一根彎得像弓的轅、短犁床、尖犁頭；只有這幾筆線條、其餘空白（心裡話畫外）"),
    # ---- scene 1b: the threshing ground at sunrise (Xu Yan comes in on screen left facing right; Qin Shuang on the right).
    dict(chapter="打穀場", loc="ground", cam="Wide shot, slow pan right", chars=["xuyan", "qinshuang", "erniu"], night="ground", act=3,
         comp=f"wide shot past a conical sheaf of rice straw in the left foreground, keeping Xu Yan in the frame at first: on screen left at the edge of the threshing ground {XU2}, {DRAWING} tucked under his left arm, framed full length, stopping short, his face three-quarter to screen right, never the lens; curious: brows raised, lips closed; on screen right Qin Shuang, {QIN}, {STAFF} in her right hand, framed full length, her face three-quarter to screen left toward the rows, never the lens; stern: brows drawn, jaw set; facing her {YOUNG}; in the middle of the front row {ERNIU}, {STAFF} in both hands; {STICKS}",
         lines=[],
         motion=f"Qin Shuang brings her staff down in one sharp stroke; all the young men thrust their staffs forward together and draw them back; {quiet('Xu Yan, Qin Shuang and Wang Erniu', 'their', True)}",
         zh="全景、慢慢往右搖（從許硯搖到練棍的人）、前景是場邊的稻草垛：左邊場邊許硯（破角的紙捲起夾在左腋下）停住腳；右邊秦霜（腰帶空著）右手一根比人高的素木長棍，往下一劈，面前三排約十二個年輕人（宋式交領短打、布包頭）每人一根長棍，一起出棍收棍；二牛在第一排中間；都嘴閉著（無台詞）"),
    dict(loc="ground", cam="Medium shot, slow push in", chars=["xuyan"], night="ground",
         comp=f"medium shot: {XU2}, framed from the knees up with clear space above his head, {DRAWING} tucked under his left arm, his face three-quarter to screen right toward Qin Shuang off screen right, never the lens; amused: one brow cocked, eyes narrowed, lips moving between words; behind him only the straw sheaves and the misty fields; {NOBLADE}",
         lines=[("xuyan", "天剛亮，妳就帶他們練棍？這是在練兵吧？", "挑眉，半開玩笑")],
         motion=f"Xu Yan takes a few steps onto the threshing ground and moves the rolled sheet from under his left arm into his right hand as he speaks; {NOSMILE}",
         zh="中景、慢推（身後只有稻草垛與霧裡的田）：許硯走進場子幾步，挑眉，把腋下捲著的紙換到右手，朝畫右外的秦霜說；不笑"),
    dict(loc="ground_c", cam="Medium close-up, low angle, slow push in", chars=["qinshuang"], night="ground",
         comp=f"low-angle medium close-up of Qin Shuang, {QIN}, framed from the chest up with space above her head, {STAFF} standing upright in her right hand beside her, a few strands of her ponytail damp with mist, her face three-quarter to screen left toward Xu Yan off screen left, never the lens; curt: brows drawn down, eyes hard, jaw set, lips moving tightly between words; behind her only the thin morning mist and the tops of the straw sheaves; {STICKS}",
         lines=[("qinshuang", "他們自己要學。我只是教他們，別被人打死。", "不想多說")],
         motion=f"Qin Shuang glares at him, turns her face half away toward screen right and thumps the end of the staff once on the ground; {NOSMILE}",
         zh="低角度中近景、慢推（身後只有晨霧與稻草垛頂）：秦霜右手長棍立在身旁、馬尾沾著霧氣，瞪他一眼、臉別開一半、棍子往地上一頓，不想多說；咬牙不笑"),
    # Erniu may grin here (the script: 憨笑).
    dict(loc="ground", cam="Medium shot, slow push in", chars=["erniu"], night="ground",
         comp=f"medium shot: {ERNIU}, standing in the front row of the young men, framed from the knees up with clear space above his head, {STAFF} held in the crook of his left arm, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; sheepish: brows up, an embarrassed open grin between words; behind him only the soft rows of young men and the straw sheaves; {STICKS}",
         lines=[("erniu", "上回火把圍屋，我腿都嚇軟了，總得學兩招。", "不好意思，憨笑")],
         motion="Erniu scratches the back of his head with his right hand, the staff resting in the crook of his left arm",
         zh="中景、慢推（身後只有虛焦的年輕人與稻草垛）：二牛在第一排，長棍夾在左臂彎，右手抓後腦，不好意思地說（本鏡可以憨笑）"),
    # Xu Yan's point of view: nobody on screen; his line off screen.
    dict(loc="ground", cam="Point-of-view wide shot, slow push in", chars=[], night="ground", act=3,
         comp="point-of-view wide shot from the edge of the threshing ground looking out past its last straw sheaves at the flat harvested rice fields beyond: short rows of cut rice stubble standing in the unturned dark earth, the fields wide and empty, nobody anywhere in them, only stubble and earth as far as the misty hills; the foreground only the edge of the threshing ground",
         lines=[("xuyan", "田都收割完了，怎麼還沒人翻土種麥？", "看著田，問二牛")],
         motion="an autumn wind ruffles the stubble and a few sparrows flutter up from the field and away",
         zh="主觀（許硯看場外）、慢推：場外一大片收割完的稻茬田，土沒翻、田裡沒有人；秋風吹過稻茬、幾隻麻雀飛起（許硯的台詞畫外）"),
    # Erniu does not smile (bad news; the original's 必修): written as what his face does; short.
    dict(loc="ground_c", cam="Close-up, slow push in", chars=["erniu"], night="ground",
         comp=f"close-up of {ERNIU}, framed from the chest up with space above his head, {STAFF} lowered with its end on the ground beside him, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; heavy-hearted: the corners of his mouth pulled down, brows sagging, eyes lowered, lips moving low and slow between words; behind him only the thin morning mist",
         lines=[("erniu", "韓伯說，去年冬天牛瘟，全村的牛都死光了。", "悶聲，難過")],
         motion="Erniu lowers his staff, looks down at his own feet, then lifts his eyes heavily toward Xu Yan off screen left; after the last word he swallows and presses his lips together, his brows sagging to the last frame",
         zh="近景、慢推（身後只有晨霧）：二牛把棍子放下、低頭看自己的腳，再抬眼看許硯，悶聲說；嘴角往下、眉毛垂著，說完吞一下、抿嘴（原版必修：不笑）"),
    dict(loc="ground", cam="Medium shot, tracking", chars=["hanbo", "erniu"], night="ground",
         comp=f"medium shot following him as he walks in from the right background: {HAN}, framed from the knees up with clear space above his head, coming to a stop beside the young man, his face three-quarter to screen left toward the fields off screen left, never the lens; grave and certain: white brows drawn together, eyes steady, lips moving slowly between words; beside him on screen left {ERNIU}, {STAFF} lowered at his side, his face turned to the old man, lips closed, brows sagging; behind them only the straw sheaves and the mist; {STICKS}",
         lines=[("hanbo", "冬麥再種不下去，明年開春，全村都沒糧吃。", "篤定，一口氣說完，不拖")],
         motion=f"Elder Han walks up leaning on his bamboo walking staff, stops beside Erniu and taps the staff twice on the ground, his eyes on the fields off screen left; {quiet('Wang Erniu')}; {NOSMILE}",
         zh="中景、跟拍（跟著韓伯由右後往前）：韓伯（白長鬚、灰交領長衫、右手磨亮的竹杖）走過來停在二牛身邊，竹杖在地上點兩下，看著畫左外的田，慢慢篤定地說；二牛在他左邊轉頭看他、嘴閉著；不笑"),
    dict(loc="ground_c", cam="Close-up, slow push in", chars=["xuyan"], night="ground",
         comp=f"close-up of {XU2}, framed from the chest up with space above his head, the rolled sheet in both hands at chest height, his face three-quarter to screen right toward Wang Erniu off screen right, never the lens; decided: brows up, eyes bright and quick, lips moving between words; behind him only the thin morning mist and the edge of the threshing ground",
         lines=[("xuyan", "有圖就有犁。二牛，你舅舅是打鐵的吧？", "篤定，眼睛一亮")],
         motion=f"Xu Yan snaps the sheet open with both hands and holds it up toward Wang Erniu off screen right, its blank back toward us, lit from the front, the charcoal strokes on its far side; {NOSMILE}",
         zh="近景、慢推（身後只有晨霧）：許硯兩手把捲著的紙「唰」地攤開，舉向畫右外的二牛，紙背朝鏡頭、正面打光、空白（不寫透出線條）；不笑"),
    # Erniu reads the drawing (not smiling: earnest). The sheet comes in from the left, held by hands off screen.
    dict(loc="ground", cam="Medium shot, slow push in", chars=["erniu", "hanbo"], night="ground",
         comp=f"medium shot: in front {ERNIU}, framed from the waist up with clear space above his head, his face three-quarter to screen left toward the sheet, never the lens; earnest and amazed: eyes wide, brows up, lips moving between words; the edge of one sheet of paper reaches into the frame from the left, held up by hands off screen, its front toward him and its blank back toward us; one step behind him on screen right {HAN}, leaning forward to look, his lips closed; behind them only the straw sheaves; {STICKS}",
         lines=[("erniu", "是啊，在隔壁村打鐵。這圖上的犁頭，他打得出來！", "認真，越說越興奮")],
         motion=f"Erniu leans in, stares at the sheet and taps one spot on its front with his forefinger; Elder Han cranes forward behind him; {quiet('Elder Han')}",
         zh="中景、慢推：二牛湊過來（紙從畫左伸進來、拿紙的手在畫外，紙背朝我們）瞪大眼看，手指在犁頭的位置點一點，認真地說；韓伯在他身後探頭、嘴閉著"),
    dict(loc="ground", cam="Medium shot, slow push in", chars=["xuyan", "erniu", "qinshuang"], night="ground",
         comp=f"medium shot: on screen left {XU2}, framed from the knees up with clear space above his head, his face three-quarter to screen right toward the young man, never the lens; brisk: brows lifted, eyes quick, lips moving between words; in the middle facing him {ERNIU}, {STAFF} in his right hand, his face three-quarter to screen left, never the lens; eager, lips closed; a few steps behind them on screen right Qin Shuang, {QIN}, her own staff upright in her right hand and her left hand free, watching them, lips closed; {STICKS}; exactly three people in the front, the young men small and soft far behind",
         lines=[("xuyan", "木架我找石師傅，犁頭你跑一趟舅舅家，今天就要。", "交代，很快")],
         motion=f"Xu Yan presses the rolled sheet into Erniu's left hand; Erniu nods once, tosses his staff underhand across to Qin Shuang, who catches it in her left hand, and he turns and runs off toward screen left; {quiet('Qin Shuang', 'her')}",
         zh="中景、慢推：畫左許硯把捲好的圖塞進二牛左手，很快地交代；中間二牛點一下頭，把長棍低低拋給畫右後面的秦霜（她左手接住），轉身往畫左跑（剪在轉身跑的一半）；秦霜嘴閉著"),
    # ---- scene 2a: the autumn field (the field on screen left, the raised ridge on the right; the pullers go toward the left).
    # bible rule 1: the script's four named onlookers on the ridge are left to s20-s26; here only unnamed villagers.
    dict(chapter="一個人的犁", loc="field", cam="Wide shot, low angle, slow push in", chars=[], night="pm", act=3,
         comp=f"low-angle wide shot past a few stalks of rice stubble in the foreground: in the field {VILLAGERS} {PLOUGH_OLD} toward screen left, leaning far forward, their feet sinking into the dark earth; only one short strip of turned earth behind the plough; on the raised ridge at the right edge {ONLOOKERS}; {STICKS}",
         lines=[],
         motion="the three men strain forward on the ropes; the dull share only scrapes the top of the earth and sticks; they stop, panting, hands on their knees",
         zh="低角度全景、慢推、前景是稻茬：田裡三個村民（宋式短打、布包頭）胸前套繩拉一架直轅舊犁往畫左，身子往前傾、腳陷進黑土，犁頭只在土面刮一下就卡住，三人喘著停下（無台詞）；田埂上幾個村民很小、側背（稿子寫的韓伯、唐小棠、秦霜、許硯移到下面幾鏡：一鏡最多三張臉）"),
    # Converted: from behind her on the ridge, looking down at the stuck plough.
    dict(loc="field", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="pm",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, {GOLD}, standing on the raised grass ridge in the right foreground, her left hand (on screen left) holding up the hem of her pleated skirt; below her ahead in the field on screen left, {VILLAGERS} {PLOUGH_OLD}, now standing still beside it, panting, only one short strip of turned earth behind it; {STICKS}",
         lines=[("tangxiaotang", "三個人拉了一上午，才翻了這麼一小塊。", "咬唇，算著，不笑")],
         motion=f"the young woman's right hand (on screen right) comes to rest on the small gold abacus at her waist; down in the field one of the men wipes his brow with his sleeve; {HEADSTILL}",
         zh="【改背後拍】過肩中景、慢推：前景右只有唐小棠的後腦與肩，站在田埂上、左手（畫左）提著裙襬；前面田裡三個村民停在卡住的直轅犁邊喘氣，只翻了一小條；她右手（畫右）停在腰間小金算盤上，頭始終不轉。台詞 nospeak，剪接放錄音"),
    # Erniu may grin here (the script: good news).
    dict(loc="field", cam="Wide shot, tracking", chars=["erniu", "shimujiang"], night="pm",
         comp=f"wide shot following them from right to left past a hanging branch of yellow willow leaves in the foreground: coming down off the raised ridge on the right into the field, one behind the other, {ERNIU} in front and {CARP} behind, carrying {PLOUGH} between them on their shoulders, framed full length with clear space above their heads; Erniu's face three-quarter to screen left toward Xu Yan off screen left, never the lens, beaming: brows up, a wide open grin between words; the carpenter's face three-quarter to screen left, never the lens, grim: brows knotted, mouth pulled down, lips pressed shut; {STICKS}; exactly two people",
         lines=[("erniu", "許兄弟！舅舅的犁頭打好了，石師傅也裝好了！", "大嗓門，高興")],
         motion=f"the two of them step down off the ridge into the field and lower the plough onto the dark earth; {quiet('Carpenter Shi')}",
         zh="全景、跟拍（跟著兩人由右往左）、前景是田埂邊的黃柳枝：二牛在前、石木匠在後，肩上扛著曲轅犁（彎得像弓的木轅、短犁床、新黑鐵犁頭、磨亮的木犁把）從田埂走下田、放在黑土上；二牛朝畫左外的許硯大聲說（本鏡可以咧嘴笑，是好消息）；石木匠皺眉、嘴角往下、嘴閉著"),
    # Carpenter Shi does not smile (e913: written as knotted brows, pulled-down mouth and a snort; never "grudging"); short.
    dict(loc="field", cam="Medium shot, slow push in", chars=["shimujiang"], night="pm",
         comp=f"medium shot: {CARP}, standing beside {PLOUGH} on the dark earth, framed from the knees up with clear space above his head, his right fist resting on the curved wooden beam, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; gruff and stubborn: brows knotted low, one eye narrowed, the corners of his mouth pulled down, lips moving curtly between words and pressed flat between them; behind him only the flat stubble field and the yellow willow far off; {STICKS}",
         lines=[("shimujiang", "轅是彎的。這種犁我做了三十年，頭一回見。", "嘴硬，短促")],
         motion="Carpenter Shi knocks his fist twice on the curved beam and walks half a circle round the plough, eyeing it sideways; after the last word he snorts once through his nose, presses his lips into a hard flat line and keeps glaring at the beam to the last frame",
         zh="中景、慢推（身後只有稻茬田與遠處的黃柳）：石木匠右拳搭在彎轅上，用拳頭敲兩下、繞犁走半圈斜眼看，嘴硬地說；眉頭壓低、嘴角往下，說完鼻子哼一聲、嘴抿成一條線瞪著轅（第 13 集重拍的寫法：不寫「不情願」）"),
    dict(loc="field", cam="Medium shot, slow push in", chars=["erniu"], night="pm",
         comp=f"medium shot: {ERNIU}, standing beside the plough on the dark earth, framed from the knees up with clear space above his head, a rope harness of plain hemp rope in his right hand, his face three-quarter to screen right toward Qin Shuang off screen right, never the lens; eager: brows up, eyes bright, lips moving loudly between words; behind him only the flat stubble field; {STICKS}",
         lines=[("erniu", "我來拉！我力氣大，一個頂兩個！", "搶著，拍胸")],
         motion="Erniu swings the rope harness up over his own shoulder and slaps his chest once with his left hand",
         zh="中景、慢推（身後只有稻茬田）：二牛右手撿起麻繩套往自己肩上一甩、左手拍一下胸口，朝畫右外的秦霜搶著說"),
    # Erniu's shoulder at the right edge: unnamed, no picture.
    dict(loc="field_c", cam="Medium close-up, slow push in", chars=["qinshuang"], night="pm",
         comp=f"medium close-up of Qin Shuang, {QIN}, just come down off the ridge, framed from the chest up with space above her head, {STAFF} in her right hand held out toward screen right, her face three-quarter to screen right toward the young man there, never the lens; brisk and sure: brows level, eyes steady, lips moving crisply between words; at the right edge of the frame, soft and out of focus, only the broad shoulder of one young man in a coarse brown jacket, his face out of the frame; behind her only the flat stubble field; {STICKS}",
         lines=[("qinshuang", "不用你拉。這犁，我一個人推得動。", "乾脆")],
         motion=f"Qin Shuang presses the staff into the young man's hand at the right edge, rolls her sleeves up to the elbows with two quick tugs and steps past him toward the plough on screen left; {NOSMILE}",
         zh="中近景、慢推（身後只有稻茬田）：秦霜剛從田埂下來，右手把長棍塞給畫右緣虛焦的二牛（只露肩、不點名不送圖），兩下把袖子捲到手肘、越過他往畫左的犁走，乾脆地說；不笑（剪在她握住犁把，s25 接推出去）"),
    dict(loc="field", cam="Wide shot, low angle, tracking", chars=["qinshuang"], night="pm", act=3,
         comp=f"low-angle wide shot moving alongside the new furrow, the whole action kept in the frame: Qin Shuang alone, {QIN_ROLLED}, behind {PLOUGH}, both bare hands gripping its polished wooden handle, framed full length with clear space above her head, her face three-quarter to screen left along the furrow, never the lens; set and strong: jaw set, brows level, eyes ahead; in front of the plough only bare dark earth, she alone pushes it; on the raised ridge at the right {ONLOOKERS}; {STICKS}",
         lines=[],
         motion=f"Qin Shuang drives the plough forward; the black iron share bites into the dark earth and one long wave of soil rolls over beside it as she walks on step by step toward screen left; the onlookers on the ridge lean forward with their mouths falling open; {quiet('Qin Shuang', 'her')}",
         zh="低角度全景、跟拍（在犁溝邊跟著她走），整個動作留在畫面裡：秦霜一個人（袖子捲到手肘）在犁後、兩手赤手握木犁把往前一推，鐵犁頭吃進黑土、一道泥浪一路翻過去，一步一步往畫左走；田埂上的人往前探身、嘴張得老大（無台詞）"),
    # Converted: from behind her among the villagers on the ridge.
    dict(loc="field", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="pm",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, standing on the raised grass ridge in the right foreground among {ONLOOKERS}, her left hand (on screen left) gripping the sleeve of the village man beside her; below in the field far ahead on screen left, small, one young woman alone pushing {PLOUGH} along a long fresh furrow; {STICKS}",
         lines=[("tangxiaotang", "她一個人？一個人推，比三個人拉還快！", "瞪大眼，拉著人的袖子")],
         motion=f"the young woman tugs the man's sleeve twice and points her right arm (on screen right) straight out at the field; the man beside her stares; {HEADSTILL}",
         zh="【改背後拍】過肩中景、慢推：前景右只有唐小棠的後腦與肩，站在田埂上的村民之間，左手（畫左）抓著旁邊一個村民的袖子扯兩下、右手（畫右）往田裡一指；遠處田裡很小的秦霜一個人推著曲轅犁；頭始終不轉。台詞 nospeak，剪接放錄音"),
    # Qin Shuang may smile here (the script: 半邊嘴角一勾).
    dict(loc="sunset_c", cam="Medium close-up, slow push in", chars=["qinshuang"], night="sunset",
         comp=f"medium close-up of Qin Shuang, {QIN_ROLLED}, at the end of a long fresh furrow, framed from the chest up with space above her head, both hands resting on the polished wooden handle of the plough at the bottom of the frame, a few strands of her ponytail lifting in the wind, the low sun on her face, her face three-quarter to screen right toward the ridge off screen right, never the lens; cocky: one brow lifted, chin up, one corner of her mouth hooking up, lips moving between words; behind her only the long dark furrows and the gold sky",
         lines=[("qinshuang", "看什麼？這才一畝，還有下一畝。", "挑眉")],
         motion="Qin Shuang looks back at the gaping people on the ridge, flicks her chin up at them, then leans on the handle and swings the plough round to face back down the field",
         zh="中近景、慢推（身後只有翻好的犁溝與夕陽）：秦霜在一長道新犁溝盡頭、兩手搭在犁把上，馬尾被風吹起，回頭看畫右外田埂上看傻的人、揚下巴、半邊嘴角一勾（本鏡可以笑），把犁調頭"),
    # The system; nobody named. The script's slow rise is written as a pull out (gen-dh reads no crane move).
    dict(loc="sunset", cam="Extreme wide high-angle shot, slow pull out", chars=[], night="sunset", act=3,
         comp=f"extreme wide high-angle shot over the whole field: the dark earth turned into long neat rows of fresh furrows from edge to edge, shining in the low gold sun; far off at the end of the field one tiny figure leaning on a plough; on the raised ridge at the right a few villagers in Song-dynasty hemp jackets and cloth head-wraps starting to step down into the field; {STICKS}; every face too small and far to read",
         lines=[("xitong", "叮。曲轅犁，一人可耕。", "冷，宣布")],
         panel=[("曲轅犁，一人可耕", "panel")],
         motion="the villagers on the ridge step down one after another into the furrowed field and walk out toward the tiny figure; the long shadows of the furrows lie still in the low sun",
         zh="大全景、高角度、慢慢拉遠（稿子是慢慢升高；gen-dh 不認升降）：整片田翻成一條條整齊的黑犁溝、在夕陽裡發亮；田尾一個很小的人影扶著犁；田埂上的村民一個個走下田（系統畫外，面板疊上）"),
    # Elder Han moved, not smiling (written as glistening eyes and trembling lips); short.
    dict(loc="sunset", cam="Medium shot, slow push in", chars=["hanbo"], night="sunset",
         comp=f"medium shot: {HAN}, crouched down on the fresh furrows, framed from the knees up with clear space above his head, a handful of dark fresh earth in his left palm, his face three-quarter to screen left, never the lens; deeply moved: eyes glistening, white brows drawn up, his lips trembling and pressed together between words, lips moving slowly between words; behind him only the long dark furrows in the low gold light",
         lines=[("hanbo", "冬麥種得下去了……柳溪明年，有飯吃了。", "眼眶發亮，聲音發顫，句中只停一下")],
         motion="Elder Han lays his bamboo walking staff down beside him, crumbles the earth slowly between his fingers and lifts his eyes to the sky; after the last word he presses his lips together and nods slowly to himself",
         zh="中景、慢推（身後只有夕陽裡的犁溝）：韓伯蹲在新翻的田裡，竹杖放在身邊，左手一把新土，在指間慢慢搓開、抬頭看天，眼眶發亮地說；說完抿嘴、慢慢點頭（不笑）"),
    dict(loc="sunset", cam="Medium two-shot, slow push in", chars=["qinshuang", "xuyan"], night="sunset",
         comp=f"medium two-shot at the foot of the ridge at sunset, the camera to the side of them: on screen left Qin Shuang, {QIN_ROLLED}, framed from the waist up with clear space above her head, the end of a plain hemp rope in her left hand held out toward the left edge of the frame, her face three-quarter to screen right toward him, never the lens; quiet and serious: brows level, eyes on his, lips moving low between words; on screen right a step away {XU2}, framed from the waist up, his face three-quarter to screen left toward her, never the lens; attentive, lips closed; behind them only the furrowed field and the gold sky; {NOBLADE}; exactly two people",
         lines=[("qinshuang", "今晚，你跟我去一個地方。別帶燈籠。", "壓低聲音")],
         motion=f"Qin Shuang lets the rope go to a hand off screen left, steps up close to him and lowers her voice; Xu Yan nods once; {quiet('Xu Yan')}; {NOSMILE}",
         zh="雙人中景、慢推（夕陽，鏡頭在兩人側面）：畫左秦霜（袖子挽著）把犁繩交給畫左外的手（二牛，畫外），走到許硯面前停下、壓低聲音說；畫右許硯點一下頭、嘴閉著；不笑"),
    # ---- scene 2b: the grove at night (Qin Shuang on screen left, Xu Yan on the right; the grave at the left front).
    # No lantern. The picture's fire is written as a few last embers (see the docstring).
    dict(chapter="墳前", loc="grove", cam="Wide shot, slow push in", chars=["qinshuang", "xuyan"], night="grove",
         comp=f"wide shot past a row of dark bamboo stalks in the foreground: along the narrow earth path into the small clearing, on screen left Qin Shuang, {QIN}, walking in first, and on screen right one step behind her {XU_COAT}, both framed full length, small in the frame, their faces in three-quarter profile toward the grave mound, never the lens; quiet and solemn, lips closed; the two of them are lit only by the cold blue starlight and the faint low glow of the embers; their hands are empty; {NOBLADE}; exactly two people",
         lines=[],
         motion=f"Qin Shuang stops in front of the grave mound; Xu Yan stops one step behind her; the bamboo sways overhead in the wind; {quiet('Qin Shuang and Xu Yan', 'their', True)}",
         zh="全景、慢推、前景是一排竹竿：竹林夜，畫左秦霜先走進小空地、畫右許硯（外披舊灰外衣）在她身後一步，走窄土路到小土墳前停下；只有星光與墳前一小堆快熄的餘燼（場景圖上的紙錢火照圖寫成餘燼）；兩人兩手空空、沒有燈籠；嘴都閉著（無台詞）"),
    dict(loc="grove", cam="Medium close-up, slow push in", chars=["qinshuang"], night="grove",
         comp=f"medium close-up of Qin Shuang, {QIN}, kneeling on one knee in front of the small blank plank at the grave mound, framed from the chest up with space above her head, her right hand on the top of the plank, cold blue starlight on her face and the faint warm glow of the embers low on her chin, her face three-quarter to screen right, her eyes lowered to the plank, never the lens; softened and sad: her strong brows eased, eyes lowered, lips moving very softly between words; behind her only the grave mound and dark bamboo; {NOBLADE}",
         lines=[("qinshuang", "這是我娘。墳上，沒能寫她的名字。", "很輕")],
         motion="Qin Shuang brushes a few fallen bamboo leaves off the blank plank with her fingers, slowly, and keeps her eyes down on it; after the last word she presses her lips together and lets her hand rest on the plank",
         zh="中近景、慢推（身後只有墳與竹影）：秦霜單膝跪在空白木牌前，右手搭在木牌頂上，星光照臉、餘燼的暖光在下巴，濃眉放軟，用手指拂掉木牌上的落葉、垂著眼很輕地說；說完抿嘴、手停在木牌上"),
    # drop_set in spec.json (the grove picture is not needed for a close shot of him against bamboo).
    dict(loc="grove_c", cam="Close-up, slow push in", chars=["xuyan"], night="grove",
         comp=f"close-up of {XU_COAT}, crouched down low, framed from the chest up with space above his head, his face three-quarter to screen left toward Qin Shuang off screen left, never the lens; careful and gentle: brows drawn up, eyes soft, lips moving softly between words; cold blue starlight on his face; behind him only dense dark bamboo stalks growing straight up into black night",
         lines=[("xuyan", "那妳娘姓什麼？為什麼不能寫？", "小心地問")],
         motion=f"Xu Yan crouches down beside her to the same height and asks gently, his eyes on her face; {NOSMILE}",
         zh="近景、慢推（身後只有竹竿與黑夜；spec 不送竹林場景圖）：許硯蹲下來跟她一樣高，看著畫左外的她，放輕聲音問；不笑"),
    dict(loc="grove_c", cam="Medium shot, slow push in", chars=["qinshuang"], night="grove",
         comp=f"medium shot of Qin Shuang, {QIN}, rising from one knee to her feet, framed from the knees up with clear space above her head, her face turning away toward screen left, her eyes on the dark bamboo, never the lens; holding it back: jaw set, lips pressed tight between words, brows drawn; cold blue starlight on one side of her face; behind her only dense dark bamboo stalks growing straight up into black night; {NOBLADE}",
         lines=[("qinshuang", "現在不能說。說了，你也會被牽連。", "壓著")],
         motion=f"Qin Shuang stands up from the grave, turns her face away from him toward the bamboo and presses her lips together hard before she speaks; {NOSMILE}",
         zh="中景、慢推（身後只有竹竿與黑夜；spec 不送竹林場景圖）：秦霜從墳前站起來，把臉轉開看竹子、抿著嘴，壓著聲音說；不笑"),
    dict(loc="grove", cam="Medium two-shot, slow push in", chars=["qinshuang", "xuyan"], night="grove",
         comp=f"medium two-shot in the clearing, the camera to the side of them, the grave mound soft in the left foreground: on screen left Qin Shuang, {QIN}, standing, framed from the knees up with clear space above her head, her face three-quarter to screen right toward him, never the lens; guarded, lips closed; on screen right a step away {XU_COAT}, rising to his feet, framed from the knees up, his face three-quarter to screen left toward her, never the lens; gentle and steady: brows eased, lips moving softly between words; cold blue starlight; their hands are empty; {NOBLADE}; exactly two people",
         lines=[("xuyan", "那就等妳想說的那天。走吧，回家。", "輕")],
         motion=f"Xu Yan straightens up and tilts his head once toward the path out of the grove on screen left; Qin Shuang looks at him for a moment, then turns and walks off first toward screen left; Xu Yan follows her; {quiet('Qin Shuang', 'her')}",
         zh="雙人中景、慢推（鏡頭在兩人側面、墳在左前景虛焦）：畫右許硯站起來、往畫左的出路偏一下頭，輕輕地說；畫左秦霜看他一眼，轉身先往畫左走，許硯跟上（剪在兩人轉身走）；秦霜嘴閉著"),
    # ---- scene 3: the stone bridge at dawn (the village path and the cart on the left; the log barrier in the middle; Lai San
    # and the servants behind it on the right, facing left).
    dict(chapter="石橋", loc="bridge", cam="Wide shot, tracking", chars=["xuyan", "tangxiaotang", "laisan"], night="bridge",
         comp=f"wide shot following them from left to right past the grey stone railing of the bridge in the foreground: on screen left {XU2}, pushing {CART} with both hands on its handles, framed full length, his face three-quarter to screen right, never the lens; wary: brows drawing together, lips closed; walking beside the cart on its right side Tang Xiaotang {TANG}, {GOLD}, framed full length, her face three-quarter to screen right, never the lens; uneasy: eyes narrowed at the barrier, lips closed; on screen right behind the log barrier, small in the frame, {LAI}, leaning on the log, his face three-quarter to screen left toward them, never the lens; sly: one brow up, a thin crooked grin, lips moving between words; {SERVANTS}; {STICKS}",
         lines=[("laisan", "站住！今天這座橋，不是白走的。", "喊，得意")],
         motion=f"the cart rolls up to the foot of the bridge and stops in front of the log; the servants take one step forward; Lai San lifts one hand to stop them; {quiet('Xu Yan and Tang Xiaotang', 'their', True)}",
         zh="全景、跟拍（跟著推車由左往右）、前景是橋頭石欄：畫左許硯兩手推獨輪木車（車上一捆油布包好的紙）、唐小棠走在車右邊，推到橋頭橫木前停住；畫右橫木後賴三（灰褐交領短衣、頭巾歪一邊）靠著橫木、抬手攔，喊（人在畫右、不大）；身後四個錢家家丁（宋式灰短打、布包頭）肩上各扛一根素木長棍，往前一步；許硯、唐小棠嘴閉著（唐小棠不說話的臉用中性句）"),
    # Converted: from behind her at the cart; Xu Yan straight ahead of her at its handles.
    dict(loc="bridge", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="bridge",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, standing in the right foreground beside the cart, her left hand (on screen left) pressing down on the oilcloth bundle on the cart; facing us straight ahead of her at the cart's handles, a little left of the middle, {XU2}, framed from the waist up with clear space above his head, his face three-quarter to screen right toward her, his eyes on her face just right of the lens, never the lens; alert: brows drawn together, eyes narrowing, lips pressed shut; behind him only the thin mist on the water and the grey stone railing; {NOBLADE}; exactly two people",
         lines=[("tangxiaotang", "是賴三，錢府的人。那天往鍋裡倒水的就是他。", "小聲，不笑")],
         motion=f"the young woman leans half a step toward him over the bundle; Xu Yan's eyes slide past her toward the barrier off screen right and come back; {HEADSTILL}; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中景、慢推：前景右只有唐小棠的後腦與肩，左手（畫左）按住推車上的油布紙捆，往許硯那邊靠半步；許硯在她正前方的車把後、畫面中偏左，眼神往畫右外的橫木瞟一下又回來、嘴閉著；頭始終不轉。台詞 nospeak，剪接放錄音"),
    # Lai San may grin (oily).
    dict(loc="bridge", cam="Medium shot, slow push in", chars=["laisan"], night="bridge",
         comp=f"medium shot past the thick log barrier in the foreground: {LAI}, leaning both forearms on the log, framed from the waist up with clear space above his head, his face three-quarter to screen left toward the cart off screen left, never the lens; oily and smug: eyes sliding sideways, a crooked grin between words, lips moving lazily; behind him, soft, two of the servants standing still with their staffs on their shoulders; behind them the mist and the stone of the bridge; {STICKS}",
         lines=[("laisan", "許家的貨要過橋，一車一兩。這是錢老爺的規矩。", "拖長音，油嘴滑舌")],
         motion=f"Lai San eyes the cart sideways and raps his knuckles twice on the log as he drawls",
         zh="中景、慢推、前景是橫木：賴三兩臂靠在橫木上，斜眼看畫左外的推車，指節在橫木上敲兩下，拖長音地說（本鏡可以油笑）；身後兩個家丁虛焦、長棍扛在肩上不動"),
    # Over Lai San's shoulder (unnamed, no picture).
    dict(loc="bridge", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="bridge",
         comp=f"over-the-shoulder medium shot from close behind {LAI_BACK}, in the right foreground behind the log barrier; facing us on screen left a step away {XU2}, just let go of the cart's handles, framed from the waist up with clear space above his head, his face three-quarter to screen right toward the man, never the lens; cool and firm: brows level, eyes hard, jaw set, lips moving evenly between words; behind him only the cart soft in the mist and the stone-paved path; {NOBLADE}; exactly two people, the man in the foreground seen only from behind",
         lines=[("xuyan", "橋是官府修的，錢員外憑什麼收過橋錢？", "冷，不退")],
         motion=f"Xu Yan sets the cart's handles down, steps up to the log and stops in front of it; the man in the foreground keeps his head still, the back of his head toward us the whole shot; {NOSMILE}",
         zh="過肩中景、慢推：前景右只有賴三的後腦、歪頭巾與肩（不點名、不送圖）在橫木後；許硯在畫左放下車把、往前一步站到橫木前，冷冷地問；不笑"),
    dict(loc="bridge_c", cam="Close-up, low angle, slow push in", chars=["laisan"], night="bridge",
         comp=f"low-angle close-up of {LAI}, framed from the chest up with space above his head, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; sneering: a crooked grin, eyes narrowed, lips moving between words; behind him only the thin mist over the water and the grey stone of the bridge",
         lines=[("laisan", "橋頭兩邊的地都是錢府的。不走，就繞山。", "冷笑")],
         motion="Lai San grins, jerks his thumb back over his shoulder toward both banks behind him and then pats the log twice with his palm",
         zh="低角度近景、慢推（身後只有水上的霧與橋石）：賴三咧嘴，用拇指往身後兩岸一比，再拍兩下橫木，冷笑地說"),
    # Converted: from behind her at the cart; Lai San straight ahead beyond the log.
    dict(loc="bridge", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "laisan"], nospeak=["tangxiaotang"], night="bridge",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, {GOLD}, standing in the right foreground, her right hand (on screen right) at the small gold abacus at her waist; facing us straight ahead of her a few steps away behind the thick log barrier, {LAI}, framed from the waist up with clear space above his head, his face three-quarter to screen right toward her, his eyes on her face just right of the lens, never the lens; smug: one brow up, a thin crooked grin, lips closed; behind him only the mist and the stone of the bridge; {NOBLADE}; exactly two people",
         lines=[("tangxiaotang", "一車紙才賣五錢，過一次橋就要一兩？", "瞪他，算給他聽")],
         motion=f"the young woman flicks two beads of the small gold abacus with her right hand (on screen right); Lai San's grin widens a little; {HEADSTILL}; {quiet('Lai San')}",
         zh="【改背後拍】過肩中景、慢推：前景右只有唐小棠的後腦與肩，右手（畫右）撥兩下腰間的小金算盤；賴三在她正前方的橫木後，笑得更歪一點、嘴閉著；頭始終不轉。台詞 nospeak，剪接放錄音"),
    # The cliffhanger (bible 15->16): Lai San holds out the folded slip; Xu Yan has not taken it, hands on the cart's handles.
    dict(loc="bridge", cam="Medium shot, slow push in", chars=["laisan", "xuyan", "tangxiaotang"], night="bridge",
         comp=f"medium shot past the oilcloth bundle on the cart in the left foreground, from medium shot pushing toward medium close: on screen right behind the thick log barrier {LAI}, framed from the waist up with clear space above his head, his face three-quarter to screen left toward the young man, never the lens; smug and sly: a crooked grin, eyes glinting, lips moving low between words; two servants behind him each holding one end of the log, soft; on screen left behind the cart {XU2}, both hands on the cart's handles, framed from the waist up, his face three-quarter to screen right toward the man, never the lens; cold: eyes narrowing, jaw set, lips pressed shut; beside the cart between them Tang Xiaotang {TANG}, framed from the waist up, her face three-quarter to screen right toward the man, never the lens; tense: brows drawn, lips closed; {STICKS}",
         lines=[("laisan", "嫌貴？紙坊賣我，五十兩，橋就通。", "壓低，得意")],
         motion=f"Lai San draws {SLIP} out of his left sleeve with his right hand and holds it out across the log toward the young man, and it stops there in front of him; Xu Yan does not take it: his eyes lift from the slip to Lai San's face and narrow; {quiet('Xu Yan and Tang Xiaotang', 'their', True)}",
         zh="中景、慢推（從中景推到中近景）、前景是推車上的油布紙捆：畫右橫木後賴三（身後兩個家丁各扶橫木一端、虛焦）右手從左袖抽出一張摺起的紙（紙背朝鏡頭、空白），隔著橫木伸到許硯面前停住，壓低得意地說；畫左許硯兩手還扶著車把、沒接，眼睛從紙上抬到賴三臉上、瞇起來；唐小棠在車旁、嘴閉著（結尾，懸念接第 16 集）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e015-r2/script.md`（c01–c42 對應 s01–s42；2026-11-06 的 r2 稿；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-15）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e011-e020.md`（拍法 1–18 條）。",
    "- 內部工作編號 915（`hailuo/{ff,clips}-dh-e915.json`、`colab/runs/e915/extras.json`、`colab/runs/e915-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e915-dh/`）；發布 slug `zhong-tian-qu-qi-e015-r2`。不放集數、不放片名卡；s01 接第 14 集 s42 的機位（過了一夜：唐小棠的背在畫右前景、許硯在她正前方）。",
    "- 照第 14 集審稿後的寫法與拍法第 18 條一開始就照做：`OFFSCREEN_SPEECH = False`；畫外句、心裡話、系統句與錄音鏡，畫面上每個人寫整鏡不說話；背景寫在場的東西（空的土牆、晨霧、只有竹子），不寫被否定的名詞；長棍寫成「素木長棍、兩頭圓滑」；不笑寫成皺眉、嘴角往下、抿嘴、鼻子哼一聲、別開臉，說完最後一個字也寫一個動作。手與道具的位置寫在第一格的構圖句裡（第 13 集重拍：只寫在動作句常被忽略）。",
    "- 唐小棠八句台詞都不露嘴、放錄音（nospeak）：s02、s05 是她手的插鏡（拍紙堆、拍柱上的紙）；s01、s07、s20、s26、s37、s41 從她背後拍、對方在她前面、頭始終不轉；spec.json 拿掉她三張臉部參考圖與身分句。她不說話的臉（s36、s42）用第 7 集的中性外貌句。",
    "- 兵器：本集沒有刀（秦霜腰帶整集空著）；秦霜、二牛、十二個年輕人、四個錢家家丁的長棍與韓伯的竹杖都寫成素木長棍、兩頭圓滑。一鏡最多三張有名字的臉：稿子 c19 田埂上的四個人不入鏡，只留三個拉犁的村民與幾個看不清臉的村民。",
    "- 場景：工棚夜景**新畫** `set-gongpeng-ye-l2`（從第 14 集的白天工棚 `set-gongpeng-l2` 改光成天亮前一根蠟燭頭，並拿掉最左邊斜靠的長竿架與桶裡的攪棒；`live-action/screen-test-e015.py`，種子 37011／37012；舊的 l1 從舊白天圖改光，地上還有格柵、左邊還有長竿）。打穀場 `set-dagu-chang-l1`、秋田 `set-qiutian-l1`、竹林 `set-zhulin-fen-l3`、石橋 `set-shiqiao-l1`。竹林圖墳前有紙錢火：不重畫（重畫會讓第 13、14 集重拍拿到沒有火的圖），照圖寫成墳前地上一小堆快熄的餘燼；s33、s34 兩支近景不送竹林圖。",
    "- 新人物韓伯（`hanbo-portrait-l1`，第一次出場），聲音照 `cast.json` 的 Enceladus（另一個 Enceladus 是只在第 60 集出場的常公公，韓伯第 60 集不在，跟 cast.json 裡其他共用聲音的角色同一個做法）；造型句在 extras.json 補宋式交領。",
    "- 長鏡要買的秒數（BUY）：照 40 句錄音核過（`~/mokaair-work/videos/zhong-tian-qu-qi-e915-dh/audio`，見 `r2.py` 的 BUY 註解）：12 鏡買 8 秒（s03、s04 系統加心裡話；s15、s17、s38、s40 台詞 6 秒以上；s18、s21、s24、s25、s35、s36 動作有好幾拍），其餘 6 秒（不能笑的 s14、s22、s29 與唐小棠的背影都留 6 秒）。韓伯 a16、a28 與石木匠 a22 第一次錄得太慢，重錄一次（舊的在 `audio/slow-takes/`）；a22、a28 句中 0.68、0.81 秒的停頓剪到 0.4 秒（原檔在 `audio/long-pause-takes/`）。稿子長鏡清單的 c03 買 10 秒改 8 秒（兩句加起來 8.1 秒，放得下）。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音長度＋0.5 秒為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯、唐小棠（l1 交領）、秦霜、王二牛、韓伯（`hanbo-portrait-l1`，沒有角度圖）、石木匠（`shimujiang-portrait-l1`，沒有角度圖）、賴三（`laisan-portrait-l1`，沒有角度圖）；場景 `set-gongpeng-ye-l2`（新畫，**還沒跑**：`live-action/screen-test-e015.py`，manifest `~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-e015/e015.json`；`prep915.sh` 在這張圖進 refs-live 之前停住）、`set-dagu-chang-l1`、`set-qiutian-l1`、`set-zhulin-fen-l3`、`set-shiqiao-l1`。",
    "- `gen-dh.mjs` 的 SET 加兩行：`night work shed` → `dh-set-gongpeng-ye-t1`（排在 `work shed` 前）、`autumn stubble field` → `dh-set-qiutian-t1`（排在 `spring field|…|ploughed field` 與 `stream|…|willow` 前）；第 910–914 集重建逐位元相同。`build-r2.py` 的 EN 與 `cast.json` 不用改（韓伯、賴三、石木匠都已登記）。",
    "- `colab/runs/e915/extras.json`（照 e914：畫面不放字幕、空氣清澈那句；拿掉秦霜造型句的柴刀；石木匠的造型句改宋式交領短工衣、皮圍裙不寫木屑；二牛的 empty-handed 拿掉；韓伯的長衫寫成宋式交領）與 `colab/runs/e915-live/spec.json`（`mkspec.py` 產生；種子 9151101／9151102）。",
    "- 免費準備：`prep915.sh`（`DRY=1 REFS=~/mokaair-work/videos/zhong-tian-qu-qi-e915-dh/runpod/refs-dh-e915 VIDEO_JSON=docs/videos/zhong-tian-qu-qi-e015-r2/video.json st1-ep.sh 915` → `pilot.py runpod/a/st1 runpod/live/st1 s01…s42` → `retake.py runpod/live/st1 runpod/live/d1 colab/runs/e915-live/spec.json` → `colab-jobs.json` 加 output_path → `preflight-prompts.py`）。工棚夜景挑好、放進 refs-live 再跑；草稿等 Colab 空出來再拍。",
    "- 配樂：第一場疲憊但暖的 cue（s03「叮」一個亮的重音，s14「牛都死光了」沉下來，s16 攤開圖時轉起）；第二場越來越昂揚的 cue（s25 秦霜犁地時起來，s28「叮」），竹林換安靜的冷 cue；第三場壓低的 tension（s38「一車一兩」一個重音，s42 停在一個懸著的音）。音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy. Measured 2026-11-15 against the 40 recordings (~/mokaair-work/videos/zhong-tian-qu-qi-e915-dh/audio;
# ffprobe, silencedetect -35 dB / 0.3 s; e013's test: a shot holds (buy - 0.3) x 1.1 s of speech, half a second between lines).
# The script's long-shot list (c03 at 10, c04 at 8) is replaced by the measurement: s03 holds a03 3.91 + a04 3.68 + 0.5 =
# 8.09 s in 8 (a 10 s silent face is ten seconds of drift), s04 a05 3.14 + a06 3.24 + 0.5 = 6.88 s in 8.
# Re-recorded once (2026-11-15; the first takes are in audio/slow-takes/): Elder Han's a16 (7.80 s, 2.4 characters a second)
# and a28 (7.16 s with a 1.02 s pause) and Carpenter Shi's a22 (5.80 s) came out slow; the emotion was rewritten (篤定，一口氣說完，
# 不拖 / 眼眶發亮，聲音發顫，句中只停一下 / 嘴硬，短促) and the new takes are a16 6.44 s, a28 6.60 s, a22 5.84 s. The pauses a face
# would have to hold still through on screen were then cut to 0.4 s, as e014 did for a06/a10 (originals in
# audio/long-pause-takes/): a22 0.68 s after 轅是彎的。 (now 5.57 s) and a28 0.81 s at 「……」 (now 6.19 s).
# 8 s go to: the long lines s15 (a16 6.44), s38 (a36 6.48), s40 (a38 6.36), s17 (a18 6.00, plus the tap on the sheet), the two
# system shots with a thought (s03, s04), and the shots whose action has several beats: s18 (hand over, nod, toss, catch, run),
# s21 (carry down off the ridge, set the plough down, a 4.68 s line), s24 (hand over the staff, roll both sleeves, step past),
# s25 (the furrow, the episode's spectacle; no line), s35 (stand, nod to the path, she turns, he follows) and s36 (the cart
# rolls up and stops, the servants step forward, a 3.88 s shout). The risky faces stay at gen-dh's 6: s22 the carpenter (a22
# 5.57), s29 Elder Han moved (a28 6.19), s14 Erniu's bad news (a15 5.36); Tang Xiaotang's backs too (s07 a09 5.92 s: its tail
# may run about 0.3 s into the insert s08, whose own thought a10 starts after 0.35 s of silence). Every other line fits 6.
BUY = {s: 8 for s in ["s03", "s04", "s15", "s17", "s18", "s21", "s24", "s25", "s35", "s36", "s38", "s40"]}
