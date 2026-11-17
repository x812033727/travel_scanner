"""Episode 26 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e026-r2/script.md
(c01-c40 = s01-s40; c30 split in two: s30/s30b; the CG-era r2 script), including its sections 「這版改了什麼」,
「2026-11-06 審稿後的修改」 and 「真人版的改動（2026-11-17）」, which override the tables. Every line is the script's, word for
word; only the staging changes. Bible: production/r2-bible-e021-e030.md (rules 1-30, the 25->26 and 26->27 hand-overs, the
props, people and picture tables). The sixth episode of arc 3 〈搶親〉: the sugar workshop on the seventh morning, the Xu shop
and the county street on the twenty-sixth morning, the shop's back room that dusk, the shop front on the twenty-seventh
morning.

Written from the start the way e025-r2/r2.py stands AFTER its independent review (../e025-r2/review.md), with what the two
pickers caught in e921-e924 (colab/runs/e92{1,2,3,4}-live/{review-picks-a,review-picks-b,picks-merged}.tsv) and the e924/e925
reviews:
- OFFSCREEN_SPEECH = False (rule 15): every shot with an off-screen line, a thought or a system line writes the silence of
  each person on screen (quiet(), SILENT_HE). Where a back-view or off-screen character speaks, every face toward the camera
  "says nothing, lips closed, listens"; no word that invites a smile or talk (amused, pleased, grin) on a listener.
- Tang Xiaotang never speaks on camera (rule 3) and, as in e024 and e025, never shows her face: every shot of her is from
  behind, "facing straight away from us", head still, just two round buns, one pink ribbon each, the nape bare (TBACK). Her
  lines: s01, s07, s12 (the workshop), s21, s24 (the shop) from behind (nospeak; spec drops her pictures and identity
  sentence); s18, s22 (inserts of her hands), s25 off screen; s23 her back in a shot with no line of hers (not on chars:
  unnamed, no picture). The wide shots s02, s17, s19, s35, s40 leave her out (e924 s01: in a wide she turns and shows a cheek);
  the script's c35 (her opening the first crate) and c40 (her pale at the counter, the 26->27 hand-over) keep her inside the
  shop, off screen; e027's first shot puts her at the counter. Her red eyes (c01, c07), her nod and her smug smile (c24) go to
  the recordings.
- The abacus (rule 20) is in no shot: no insert of it in this script.
- Name only what should be drawn (rules 7, 17, 27, 28): the ledger is "one thick stack of plain blank paper sheets stitched
  along one edge with cord", seen low from the side, never the word for a book; the brush (c21, c22) is not written (no
  writing in this episode: e925 kept the brush to the letter); the Xu wrapping paper is "plain white paper", the Wei/poison
  paper "rough yellowish paper", the cakes "small square white cakes frosted with fine white sugar" (rule 28), the powder
  "greyish white powder" from "one small packet of folded grey paper". Nothing hung is named (signs, boards, banners,
  lanterns): the membership tokens on the counter are not shot (the script's foreground in c19), the Wei shop's red silk is
  "draped over a plain bare wooden beam" (e924's beam, without the word for hanging), the doorway to the front room is "a dark
  doorway" (a cloth door curtain grows characters). No word "open" anywhere (e924 fix1: open fans, open sheets grow text):
  "wide doorway", "flat palm", "its lid lifted off".
- Wei Shaoqing's fan stays closed (e921 fix1, e924): the script's slow opening in c29 is the closed fan raised beside his
  chin; c26 taps the closed fan into his palm; c28 has it tucked in his sash. He does not smile in this episode (rule 30: c26
  cold, c28 losing, c29 cold fury): NOSMILE wording, gritted teeth, the corners of his mouth pulled down. The green jade
  ornament at the front of his topknot (e020 review 必改 7), never a crown.
- The Wei shop clerk (bible 〈小角色〉: about twenty, thin, a dark red cloth short jacket, a black cloth head wrap; the gong was
  e024's only; the script's c26-c27 gong is not written) is "one thin young man of about twenty in a dark red cloth short
  jacket and a black cloth head wrap", afterwards "the young man in dark red" (e925 review 必改 2), never named, never sent,
  side-on, his hands hanging empty. He is never on chars, so his line (s27) is an off-screen line by build-r2's rule although
  he is seen side-on (e024, e025); MINOR gives his voice (Alnilam). The script's close-up c27 is a side-on medium shot (bible).
- The woman's scream in c40 (「糖裡有毒！」, 「用群眾聲音錄，不開新角色」) needs a voice: MINOR "kerenfu" (排隊的婦人), Despina, a
  voice nobody in the series uses; she is never seen (off screen in the wide).
- The man in grey (bible 〈小角色〉 灰衣客人): grey cotton cross-collared short jacket, head wrap pulled low, only from behind or
  side-back, never a face; unnamed, no picture. Customers: six in a line (rule 25, e024), never "crowd".
- Counts written everywhere (rule 25): "exactly two people", "exactly seven people", "exactly eight people"; six crates on
  the cart (c19), three pieces and three packets (c33, c34, c36), three trays (back room).
- Lai San (laisan-portrait-l1: a checked grey-brown cross-collared jacket, an old cloth head wrap below a topknot): small and
  thin, limping on his left foot in every walking shot (bible), thinner and dustier in scene 1; from s14 on, Xu Yan's coarse
  grey apron tied at his waist (script). He may smile only the fawning smile the script marks (c09, c17, s30b).
- Little Xiaohe (xiaohe-portrait-l1 and her angles): eight, patched lilac jacket, red-string pigtails, the straw rabbit in her
  sash (extras); she may laugh in c06 (off screen). Wang Erniu does not smile when angry (c10, c16); he may grin with good news
  (c02, c19).
- One visible action per shot, props and contacts in the first frame (e923-e925 picks): c01 (fold, open, place, shut, stand,
  point) is the note dropped into the box and the lid shut; c03 the pour only; c09 the bows only (he has stopped beyond the
  railing in the first frame); c13 the apron untied; c14 the toss and the catch; c17 the bundle shouldered and two limping
  steps, his glance at the sugar after the last word; c26 the fan tap (he is already on the step, the boy already upright);
  c31 the bar only (the packet comes out in s33); c33 the sifting only (the three pieces already on their papers); c34 the
  packets tucked away, the lamp blown out left to the cut and the sound effects; c35 his raised palm (the plank already
  stacked; Erniu's cart leaving goes to the sound effects); c38 the fall; c39 the passing feet; c40 the ring widening. The
  script's rises (c40 慢升) and follows (c02, c04, c09, c16, c19, c38) are slow push-ins.
- A set picture that is only a plain gradient or dark grows interiors (e923, e925 review): the back room's picture is the dark
  shelf crop set-xuji-pu-houjian-l1, so every back-room prompt writes the concrete table, trays, basket, lamp and shelves.

THE AXES (rule 29: the set picture decides):
- The sugar workshop by morning (set-tangfang-l1; bible 25->26: the stove on the left, the unwalled side on the right): the
  brick stove with its iron pan in the LEFT foreground, the long plaster wall on the left with the funnels set upside down on
  their rack, a round stone basin on a pedestal in the middle, the unwalled right side with its wooden railing, and beyond it
  the snowy dirt path along the creek and the bare willows in a low gold morning sun from the right (the picture's sunrise is
  the script's early sun through the shed's mouth). Xu Yan at the stove on the LEFT, Tang Xiaotang by the stone basin in the
  middle (a low bench beside it, written), Wang Erniu and the stacked sugarcane bundles by the railing on the RIGHT. The
  script's 石磨 is not in the picture and is not written: c03's mill becomes the pour into the pan, c10's push-pole one long
  wooden paddle. Lai San comes along the path on the RIGHT, outside the railing, and talks across it (c08-c11, c14), facing
  screen left; in c17 he is inside, by the cane.
- The Xu shop inside (set-xuji-pu-l1, as e020, e021, e024): the shelves on the LEFT wall, the wide front doorway in the
  middle of the back wall with the bright street beyond, the counter along the RIGHT wall (written). Tang Xiaotang behind the
  counter in the right foreground, seen from behind, faces across it; Xu Yan faces us beyond her. The script's 「櫃檯在畫面左」 is
  the CG picture's and is not used. Erniu's cart comes in through the doorway.
- The county street (set-xianjie-l1 and e024's crops): the Xu shop on the LEFT, the Wei shop with the red silk across the street
  on the RIGHT. People at the Xu shop look screen right across the street; Wei Shaoqing and the clerk look screen left. The line
  of customers stands along the paving before the Xu shop.
- The back room at dusk (set-xuji-pu-houjian-l1, the bible's free crop): dark shelves behind, the long table in the middle, the
  dark doorway to the front room on the LEFT, the plank back door on the RIGHT; Lai San at the table faces screen left toward
  the doorway (c30), screen right toward the basket at the table's corner (c32).
- The shop front, the twenty-seventh morning (set-xianjie-xuji-l1 and set-xianjie-shi-l1): the shop on the LEFT, the line of
  six customers along the paving on the RIGHT; Xu Yan at the doorway looks screen right.

PLACES (the coordinator's decisions, 2026-11-17; every picture looked at full size; script.md 〈真人版的改動〉):
- The workshop: the wides s02, s17 set-tangfang-l1 (gen-dh's, kept); the close shots and the insert set-tangfang-jia-l1
  (e024's); the shots at the railing and on the path (s08, s09, s11, s14) a new free crop set-tangfang-lu-l1 (the railing,
  the snowy path, the bare willows and the creek in the low sun; refs-live/README.md).
- The shop: s19-s21, s23, s24 set-xuji-pu-l1 (gen-dh's "Xu family shop", kept); the inserts s18, s22 on the counter top
  set-xuji-pu-cabinet-l1.
- The street: s25, s40 set-xianjie-l1; the Wei shop front set-xianjie-weiji-l1 (s26-s29); the Xu shop front
  set-xianjie-xuji-l1 (s35, s37); the paving before the shop set-xianjie-shi-l1 (s36, s38, s39). gen-dh's "market street"
  gives set-shiji-l1, swapped everywhere.
- The back room: set-xuji-pu-houjian-l1 (s30-s34; gen-dh's "Xu family shop" gives set-xuji-pu-l1, swapped).
- Inserts and shots with nobody named (s06, s18, s22, s25, s27, s31, s33, s36, s38, s39) open their motion with NOBODY.
- Shared files: no code changed (every on-screen speaker is in build-r2.py's EN; the clerk and the screaming woman are never on
  chars and their voices are MINOR); one new free picture in refs-live (new id with its own l1, rule 19; README paragraph).
"""
EP = 926  # internal working number; the published slug is zhong-tian-qu-qi-e026-r2
SLUG = "zhong-tian-qu-qi-e026-r2"
EP_TITLE = "白糖如雪，對街掀桌（重製版 r2）"
OUTLINE_SECONDS = 215  # script.md: about 215 s, 40 shots (17 + 12 + 5 + 6)
TARGET_MINUTES = [3, 4]
TITLE = "白糖如雪，對街掀桌｜種田娶妻打天下 第26集（重製版）"
DESCRIPTION = "鬥商第七天一早，三船甘蔗下了鍋，小禾把試做的白糖撒在手心，像下雪一樣。跛腳的賴三走到糖坊外，說錢府不要他了，求一口飯吃；二牛記得是他放火燒了紙坊，唐小棠說這種人比老鼠還難防，許硯還是把自己的圍裙丟給他：肯幹就留下。帳本一頁頁翻過十九天，白糖量產，許記是魏記的兩倍；唐小棠每批編號、記買家，用自家的柳溪白紙包糖。糖霜糕排到街尾，對街魏記一個客人都沒有，魏少卿掀了自己的桌子：去告訴孫掌櫃，今晚可以動手了。當晚賴三一個人看鋪子，把三塊不記帳的邊角料撒上藥粉，用黃紙包好。隔天早上，排隊的灰衣客人咬了一口黃紙包的糖糕，捂著肚子倒在許記門口——糖裡有毒！《種田娶妻打天下》第 26 集（重製版）。"
THUMB = ("糖裡有毒！", "s38")
CHARACTERS = ["xuyan", "tangxiaotang", "erniu", "xiaohe", "laisan", "weishaoqing", "weijihuoji", "kerenfu", "xitong"]
MINOR = {
    "weijihuoji": {"id": "weijihuoji", "name": "魏記夥計",
                   "appearance": "East Asian young man of about twenty, thin, an ancient Chinese Song-dynasty shop boy's dark red cloth short jacket and a black cloth head wrap, both hands empty",
                   "voice": {"provider": "gemini", "name": "Alnilam", "style": "標準國語，咬字清楚，台北人平常說話的語調；二十歲左右的店鋪夥計，男聲、年輕；被少爺問話，縮著肩、心虛，越說越小聲"}},
    "kerenfu": {"id": "kerenfu", "name": "排隊的婦人",
                "appearance": "East Asian woman of about forty in a plain Song-dynasty cotton robe and a cloth head wrap (never on screen)",
                "voice": {"provider": "gemini", "name": "Despina", "style": "標準國語，台北人平常說話的語調；四十歲左右的婦人，女聲，排隊買糖時看到有人倒地，嚇得扯開喉嚨尖叫，短促、驚慌"}},
}
MUSIC = "one cue per scene: a warm, driving work cue in a thatched sugar shed on a cold bright morning, one beat of silence turning low when a limping man appears, one cold single note on a jab; then a bright, cocky market cue on a sunny county street, one light accent on a bright chime, one heavy hit when a table is overturned, turning into low strings; then no melody at dusk, only low strings and a crackling oil lamp, one faint bell; then the bright market cue again, cut away to silence when a man falls, one big hit before it ends; ancient Chinese rural drama, no vocals"

# Places (gen-dh SET phrases "sugar workshop", "Xu family shop" and "market street" in the first words of each LOC; see the
# docstring). The street phrases never say "Xu family shop" (it comes before "market street" in gen-dh's list).
SHED = ("a long shed under a deep thatched roof on rough wooden posts, a brick stove with one wide iron pan steaming in the left "
        "foreground, a long plaster wall on the left with a wooden rack high on it carrying a row of brown clay funnels set upside "
        "down, wooden barrels along the wall, a round stone basin on a pedestal in the middle with a low wooden bench beside it, "
        "the unwalled right side with a wooden railing and a tall stack of bundles of green-purple sugarcane tied with straw rope "
        "against it, and beyond the railing a snowy dirt path along the creek and bare willows")
TOWN = ("a narrow stone-paved street running straight away from us under a clear pale blue sky; on the left the front of the Xu "
        "shop, its tall plank doors of pale wood folded back, a dark doorway and a long low plain wooden counter along its "
        "front; on the right across the street a two-storey wooden shop front with dark lattice windows upstairs and long swags "
        "of red silk draped over a plain bare wooden beam above its wide doorway, a long low dark table before it; plain wooden "
        "shop fronts further down both sides")
WEI_FRONT = ("a two-storey wooden shop front with long swags of red silk draped over a plain bare wooden beam above its wide "
             "doorway and a long low dark table before it")
COUNTER = "one long waist-high counter of plain dark wood with a thick flat top and a plain panelled front"
SHOP = ("bare dark wooden shelves along the left wall above a long low dark wooden cabinet, a few stacks of pale yellow soap bars "
        "on the lower shelves, the wide front doorway in the middle of the back wall between dark wooden lattice panels with "
        f"the bright street beyond it, plain white panelled walls on the right with {COUNTER} standing along them, a floor of large "
        "grey stone tiles with bars of morning sunlight across it")
BACKROOM = ("dark empty wooden shelves along the back wall, one long plain wooden table in the middle with three round flat "
            "bamboo trays of small square white cakes frosted with fine white sugar on it and one small bamboo basket of broken "
            "cake ends at its right corner, one small clay oil lamp burning on the table, a dark doorway on the left to the "
            "front of the shop, the plank back door on the right with its thick wooden bar")
LOC = {
    "shed": f"In the sugar workshop by the Liuxi creek on a cold clear winter morning: {SHED}; low warm gold morning sunlight from the right across the snow and the dirt floor, long shadows",
    "shed_c": "In the sugar workshop by the Liuxi creek on a cold clear winter morning, under the thatched shed by the brick stove and the round stone basin, white steam rising from the iron pan, in low warm gold morning sunlight from the right",
    "shed_lu": "In the sugar workshop by the Liuxi creek on a cold clear winter morning, at the unwalled right side of the thatched shed: its wooden railing and rough wooden posts, and beyond the railing a snowy dirt path along the creek, bare willows and the bright creek in the low warm gold morning sun",
    "shop": f"In the Xu family shop on a cold clear winter morning: {SHOP}; bright morning light from the doorway, the corners of the room dim",
    "shop_t": "In the Xu family shop on a cold clear winter morning, on the dark wooden counter top in soft light",
    "back": f"In the back room of the Xu family shop at dusk: {BACKROOM}; the warm orange glow of the oil lamp from below, the rest of the room dim",
    "back_c": f"In the back room of the Xu family shop at dusk, by the long plain wooden table with its trays of small square white cakes and one small clay oil lamp burning on it, dark empty wooden shelves behind; the warm orange glow of the oil lamp from below",
    "street": f"On the market street of the county town on a cold clear winter morning: {TOWN}; low morning sun from the right, long shadows on the paving",
    "street_x": "On the market street of the county town on a cold clear winter morning, at the front of the Xu shop: its tall plank doors of pale wood folded back, a dark doorway, a dark lattice transom above, the grey stone paving before it, in low morning sunlight",
    "street_w": f"On the market street of the county town on a cold clear winter morning, looking across the street from the Xu shop: {WEI_FRONT}, in bright morning sunlight",
    "street_t": "On the market street of the county town on a cold clear winter morning, on the grey stone paving before the Xu shop by its long low plain wooden counter, in low morning sunlight",
}
LIGHT = {
    "shed": "the low warm gold morning light stays unchanged",
    "shop": "the morning light from the doorway stays unchanged",
    "back": "the warm glow of the oil lamp stays unchanged",
    "street": "the low morning sunlight stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_A = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves rolled to the elbows, one coarse grey cloth apron tied at his waist"
XU_R = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves rolled to the elbows"
XU_D = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves down"
ERNIU = "Wang Erniu, in his coarse brown hemp short jacket with rolled sleeves"
XIAOHE = ("little Xiaohe, a girl of eight in her patched lilac cotton jacket, two little pigtails tied with red string, a small "
          "woven straw rabbit tucked into the cloth sash at her waist")
LAI1 = ("Lai San, small and thin, in his dusty checked grey-brown cross-collared short jacket torn at one cuff and an old cloth "
        "head wrap below his topknot, limping on his left foot")
LAI_A = ("Lai San, small and thin, in his checked grey-brown cross-collared short jacket, a coarse grey cloth apron tied at his "
         "waist, an old cloth head wrap below his topknot, limping on his left foot")
WEI = ("Wei Shaoqing, in his sapphire-blue brocade robe woven with gold thread, a white jade pendant at his waist, a small green "
       "jade ornament at the front of his topknot")
FAN = "one closed folding fan held upright in his right hand like a short slim stick, its dark bamboo ribs pressed tight together"
BOY_LOOK = "one thin young man of about twenty in a dark red cloth short jacket and a black cloth head wrap"
RED = "the young man in dark red"
CUSTOMERS = "customers in plain Song-dynasty cotton robes and cloth head wraps"
GREY = ("one man in a plain grey cotton cross-collared short jacket, his cloth head wrap pulled low over his brow, seen from "
        "behind and a little side-on, his face turned away from us")
APRON = "one coarse grey cloth apron"
PADDLE = "one long wooden paddle"
CANE = "one bundle of green-purple sugarcane tied with straw rope"
BOWL = "one shallow clay bowl heaped with fine white sugar like fresh snow"
BOX = "one small dark brown wooden cash box with a brass clasp"
NOTE = "one small strip of plain paper folded twice, its outside blank"
STACK = "one thick stack of plain blank paper sheets stitched along one edge with cord"
CART = "one wooden hand cart"
CRATE = "one plain wooden crate"
CAKE = "one small square white cake frosted with fine white sugar"
WPAPER = "plain blank white paper"
YPAPER = "rough blank yellowish paper"
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# e924 fix1's back-of-head wording, as e925
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with every strand of her black hair "
         "combed smooth and gathered up into just two round buns set high on her head, one bun on each side, one short pink "
         "silk ribbon wrapped around each bun, the nape of her neck bare and clear above a pink inner collar, and her light "
         "peach-pink silk shoulders; the back of her head facing straight away from us the whole time, her head still, her ear "
         "the furthest round her head we ever see")
HEADSTILL = "the young woman with the two high round buns keeps her head still, facing straight away from us, the back of her head toward us the whole shot"
BEHIND_COUNTER = "standing behind the counter along the right wall"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def only_tang(side=None):
    if not side:
        return "she is the only young woman with two high round buns in the frame"
    return (f"she is the only young woman with two high round buns in the frame, and she stays in the {side} "
            f"foreground from the first frame to the last")


def back(rest, where, side="right", frame="framed from the waist up", facing="facing into the frame toward him", shot="over-the-shoulder medium shot"):
    """Tang Xiaotang seen from behind (rule 3) in a foreground corner; the one she speaks with faces us beyond her."""
    return f"{shot} from close behind {TBACK}, {where} in the {side} foreground, {frame}, {facing}; {only_tang(side)}; {rest}"


def alone(rest, where, frame="framed from the waist up"):
    """Tang Xiaotang alone from behind, in the middle of the frame (not at an edge: the pickers' cheek at the frame edge)."""
    return f"medium shot from close behind {TBACK}, {where} in the middle of the frame, {frame}, facing straight away from us; {only_tang()}; {rest}"


SHOTS = [
    # ---- scene 1: the seventh morning, the sugar workshop (25->26: the next morning; the note goes into the cash box).
    dict(chapter="柳溪糖坊", loc="shed_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="shed",
         comp=alone(f"{BOX} on the bench beside her right hip, its lid already lifted from the first frame, {NOTE} already pinched in her right hand just above it; beyond her, soft, the white steam rising from the iron pan on the left and the thatched roof in the low gold morning light; {HANDS}",
                    "sitting on a low wooden bench by the round stone basin"),
         lines=[("tangxiaotang", "字條收好了。二牛，甘蔗先下十捆！", "還帶鼻音，眼睛還紅")],
         motion=f"her right hand drops the folded strip into the cash box and presses the lid shut with one small click; {HEADSTILL}",
         zh="中景（從背後）、慢推（送糖坊的免費裁切 `set-tangfang-jia-l1`；接點 25→26：隔了一夜，糖坊）：唐小棠的背影坐在石盆旁的矮凳上、畫面正中，錢箱在她右手邊、蓋子第一格已經掀起，右手捏著摺兩摺的字條（外面空白），把字條放進去、啪地蓋上（nospeak，拍法 3）。稿子『再摺一次、掀蓋、放進去、扣上、站起來轉身一指』只拍放進去蓋上（一鏡一個動作）；鼻音與紅眼交給錄音"),
    dict(loc="shed", cam="Wide shot, slow push in", chars=["erniu", "xuyan"], night="shed",
         comp=f"wide shot down the shed: on the right by the railing, beside the tall stack of sugarcane bundles, {ERNIU}, framed full figure, {CANE} already on his right shoulder from the first frame, his face three-quarter to screen left toward the middle of the shed, never the lens; cheerful: a broad grin, lips moving between loud words; in the left foreground at the brick stove {XU_A}, crouching, framed full figure, one split log already in his right hand at the stove's fire mouth, his face turned up three-quarter to screen right toward Wang Erniu, never the lens; listening: lips pressed shut; {HANDS}; exactly two people",
         lines=[("erniu", "好嘞！三船甘蔗，夠熬到年底了！", "大嗓門，可以笑")],
         motion=f"Wang Erniu swings the bundle down off his shoulder onto the dirt floor at his feet with a thump as he speaks; {quiet('Xu Yan')}; Xu Yan looks up from the stove",
         zh="全景、慢推（送糖坊圖 `set-tangfang-l1`：灶在左前、石盆在中、右邊欄杆外是雪路與溪）：右邊欄杆旁甘蔗堆，二牛第一格已經扛著一捆甘蔗，咧嘴大聲說、把甘蔗甩到腳邊（本鏡可以笑）；左前灶邊許硯（袖子捲到手肘、腰繫粗灰圍裙）蹲著添柴、抬頭、嘴閉著。唐小棠不入全景（第 24 集 s01）；稿子的跟拍改慢推"),
    dict(loc="shed_c", cam="Medium shot, slow push in", chars=["xuyan"], night="shed",
         comp=f"medium shot of {XU_A}, standing at the brick stove on the left, framed from the waist up, one wooden bucket of pale green cane juice already tilted in both hands over the wide iron pan from the first frame, white steam rising from the pan, his face three-quarter to screen right toward Wang Erniu off screen right, never the lens; busy and sure, not smiling: steady eyes, lips moving between words; behind him the plaster wall and the brown clay funnels set upside down on their rack, soft; {HANDS}",
         lines=[("xuyan", "汁先熬成紅糖，再用黃泥水淋，跟試做那碗一樣。", "邊倒邊說")],
         motion="Xu Yan pours the pale juice in one steady stream into the steaming pan as he speaks; after the last word he keeps pouring, his eyes on Erniu",
         zh="中景、慢推（送糖坊裁切）：許硯在左邊灶前，兩手第一格已經傾著一桶淡綠的甘蔗汁，一道倒進冒白氣的大鐵鍋，朝畫右的二牛（畫外）邊倒邊說，不笑。稿子的石磨圖上沒有（拍法 29）：二牛推磨不拍，只拍倒汁"),
    dict(loc="shed_c", cam="Low-angle medium shot, slow push in", chars=["xiaohe"], night="shed",
         comp=f"low-angle medium shot at a child's height of {XIAOHE}, standing by the brick stove, framed from the knees up, {BOWL} already held carefully in both hands at her chest from the first frame, her face tilted up three-quarter to screen left toward Xu Yan off screen left at the stove, never the lens; curious and worried: big eyes, brows up, lips moving between words; behind her the white steam from the pan in the low gold light, soft; {HANDS}",
         lines=[("xiaohe", "哥哥，那碗白糖這麼少，夠賣給全縣城嗎？", "仰頭問")],
         motion="little Xiaohe takes one small careful step forward, the bowl held level, as she asks; after the last word she keeps looking up",
         zh="低角度中景（小禾的高度）、慢推（送糖坊裁切）：小禾第一格已經兩手捧著那碗白糖（淺陶碗、白糖像新雪，拍法 28），在灶邊小心往前一步，仰頭朝畫左的許硯（畫外）問。稿子的跟拍改慢推"),
    dict(loc="shed_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="shed",
         comp=f"medium close-up of {XU_A}, crouching down to a child's height by the stove, framed from the chest up with space above his head, his right thumb and forefinger already pinching a little white sugar from the first frame, held up at the height of his chin; at the lower right edge of the frame {BOWL} held up by two small hands in patched lilac cotton sleeves, only her two hands in the frame; his face three-quarter to screen right toward the child, never the lens; gentle, not smiling: soft eyes, lips moving softly between words; behind him the white steam, soft; {HANDS}",
         lines=[("xuyan", "這碗是樣子。三船甘蔗熬完，能堆成一座雪山。", "放軟")],
         motion="Xu Yan raises the pinch of sugar a little higher between them as he speaks; after the last word he holds it there",
         zh="中近景、慢推（送糖坊裁切）：許硯蹲到小禾的高度，兩指第一格已經捏著一撮白糖舉到下巴高；畫右下緣只有小禾捧碗的兩隻小手（淡紫袖口）；不笑但眼神放軟地說"),
    dict(loc="shed_c", cam="Insert close-up, slow push in", chars=[], night="shed",
         comp="insert close-up, the shot opens directly on one small palm held flat and face up in a patched lilac cotton sleeve cuff, from its very first frame, a man's thumb and forefinger in a faded blue-grey sleeve rolled to the forearm already pinched together just above it; low gold sunlight slanting across them; only the small hand, its sleeve cuff, the man's two fingers and the falling sugar are in the frame",
         lines=[("xiaohe", "像下雪一樣！我要第一個吃！", "笑出來，可以笑")],
         motion=NOBODY + "the two fingers slowly loosen and fine white sugar sifts down into the small palm, glittering like falling snow in the low sunlight",
         zh="插鏡、慢推（第一格就是小禾攤平的小手心；送糖坊裁切）：許硯的兩指（藍灰袖口捲起）一鬆，白糖在斜光裡像細雪落進她手心；小禾的台詞畫外（可以笑）。稿子『手往上一揚、糖粉在光裡飄』拿掉（一鏡一個動作）"),
    dict(loc="shed_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="shed",
         comp=alone(f"both her hands low at her sides; beyond her, soft, the white steam over the iron pan on the left and the stack of sugarcane bundles by the railing on the right in the low gold morning light; {HANDS}",
                    "standing by the round stone basin"),
         lines=[("tangxiaotang", "先贏給他看。今天第七日，一天都不能歇。", "咬著牙，不笑")],
         motion=f"her shoulders square and both her hands close into small fists at her sides; {HEADSTILL}",
         zh="中景（從背後）、慢推（送糖坊裁切）：唐小棠的背影站在石盆邊、畫面正中，肩膀一挺、兩手握拳，咬著牙說（nospeak）。稿子『近景下巴以上、手背抹眼睛、下巴一抬』改背影（抬手抹眼會帶著頭轉，露側頰）"),
    dict(loc="shed_lu", cam="Point-of-view wide shot, slow push in", chars=["laisan"], night="shed",
         comp=f"point-of-view wide shot looking out past the railing of the shed: in the soft left foreground the wooden railing and one rough post, beyond it the snowy dirt path along the creek in the bright low morning sun, and far along the path, small, {LAI1}, framed full figure, his face three-quarter to screen left toward the shed, never the lens; furtive: head bowed, lips pressed shut; {HANDS}",
         lines=[("erniu", "那個一拐一拐走過來的……不是賴三嗎？", "壓低聲音")],
         motion=f"Lai San limps slowly along the path toward the shed, dragging his left foot at every step; {quiet('Lai San')}",
         zh="主觀全景（唐小棠看出去）、慢推（送新的免費裁切 `set-tangfang-lu-l1`：欄杆、雪路、禿柳與溪）：前景虛焦的欄杆與木柱，遠處雪路上賴三一拐一拐走過來（每一步拖左腳）、低著頭、嘴閉著；二牛的台詞畫外。稿子『停住、彎腰作揖』留到 s09"),
    dict(loc="shed_lu", cam="Medium shot, slow push in", chars=["laisan"], night="shed",
         comp=f"medium shot of {LAI1}, standing on the snowy path just beyond the wooden railing of the shed, framed from the waist up, both hands already pressed together before his chest from the first frame, his face three-quarter to screen left toward the people in the shed beyond the left edge of the frame, never the lens; fawning: a hollow ingratiating smile, eyes darting, lips moving fast between words; behind him the path, the bare willows and the bright creek, soft; {HANDS}",
         lines=[("laisan", "是我，是我。錢府不要我了，賞口飯吃吧。", "哈腰賠笑")],
         motion="Lai San bows low twice over his pressed hands as he speaks; after the last word he stays bent, looking up",
         zh="中景、慢推（送糖坊路邊裁切）：賴三第一格已經停在欄杆外的雪路上、兩手合在胸前，連彎腰兩次、陪笑著說（本鏡可以陪笑）。稿子『跨進棚口』改成隔著欄杆（圖上右邊是欄杆，沒有棚口）；跟拍改慢推"),
    dict(loc="shed_c", cam="Over-the-shoulder medium shot, slow push in", chars=["erniu"], night="shed",
         comp=f"over-the-shoulder medium shot: in the soft right foreground the back of a thin man's shoulder in a checked grey-brown jacket and the edge of an old cloth head wrap, out of focus, unnamed; facing us beyond him across the wooden railing {ERNIU}, framed from the waist up, {PADDLE} already gripped across his chest in both hands from the first frame, his face three-quarter to screen right toward the thin man, never the lens; angry, not smiling: brows knotted, jaw set, lips moving hard between words; behind him the stone basin and the steam, soft; {HANDS}; exactly two people",
         lines=[("erniu", "放火燒紙坊的就是你，還有臉來討飯？", "發怒，不笑")],
         motion="Wang Erniu steps up to the railing and thrusts the paddle out crosswise as he speaks; after the last word he holds it there",
         zh="過肩（賴三肩後拍二牛）、慢推（送糖坊裁切）：前景右虛焦的瘦肩與舊頭巾（不點名、不送圖，拍法 2）；欄杆裡二牛兩手第一格已經橫握一根長木槳在胸前，往欄杆一步、木槳往前一橫，發怒不笑地說。稿子的石磨推桿圖上沒有，改成熬糖的長木槳"),
    dict(loc="shed_lu", cam="Over-the-shoulder medium shot, slow push in", chars=["laisan"], night="shed",
         comp=f"over-the-shoulder medium shot: in the soft left foreground the back of a big man's broad shoulder in a coarse brown hemp jacket and the end of a long wooden paddle, out of focus, unnamed; facing us beyond the wooden railing on the snowy path {LAI1}, framed from the waist up, his face three-quarter to screen left toward the big man, never the lens; cringing, not smiling: neck drawn in, brows up, lips moving fast between words; behind him the path and the bare willows, soft; {HANDS}; exactly two people",
         lines=[("laisan", "火是員外叫我放的，我挨了板子，也被趕出來了。", "縮著脖子")],
         motion="Lai San shrinks back half a step and turns both his empty hands palms up as he speaks; after the last word he holds them out",
         zh="反打（二牛肩後拍賴三）、慢推（送糖坊路邊裁切）：前景左虛焦的寬肩與木槳末端；欄杆外雪路上賴三縮著脖子往後半步、兩隻空手掌心朝上，不笑地說"),
    dict(loc="shed_c", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="shed",
         comp=back(f"{BOX} on the bench beside her, her right hand already resting flat on its lid from the first frame; facing us beyond her, a little left of the middle, by the brick stove, {XU_A}, framed from the waist up, his face three-quarter to screen right toward her, never the lens; listening: he says nothing, his lips closed, brows a little drawn; behind him the steam over the iron pan, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
                   "sitting on a low wooden bench by the round stone basin"),
         lines=[("tangxiaotang", "這種人留在糖坊，比老鼠還難防。", "小聲，不笑")],
         motion=f"the young woman draws the cash box a hand's width closer to her along the bench; {HEADSTILL}; {quiet('Xu Yan')}; he listens, his eyes on her",
         zh="過肩中景、慢推（送糖坊裁切）：前景右唐小棠的背影坐在矮凳上，手壓著錢箱蓋、把錢箱往自己拉近一點，小聲說（nospeak）；灶邊許硯面朝她、嘴閉著聽。稿子『側身靠近許硯』不拍（側身會露臉）"),
    dict(loc="shed_c", cam="Medium shot, slow push in", chars=["xuyan"], night="shed",
         comp=f"medium shot of {XU_A}, standing by the brick stove, framed from the waist up, both hands already at the knot of the apron at his waist from the first frame, his face three-quarter to screen right toward the path beyond the right edge of the frame, never the lens; thinking: eyes lowered, then steady, lips pressed shut; behind him the steam over the iron pan, soft; {HANDS}",
         lines=[("xuyan", "被錢府用完就丟的人，我再丟一次，他就只能回去。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan slowly unties the coarse grey apron and draws it off his waist; {SILENT_HE}; he is thinking, not speaking",
         zh="中景（腰以上：解圍裙要在畫裡）、慢推（送糖坊裁切）：許硯在灶邊，眼睛朝畫右路上的賴三（畫外），慢慢解下腰上的粗灰圍裙；全程嘴閉著（心裡話）。稿子是近景，解圍裙會出畫，改中景"),
    dict(loc="shed_lu", cam="Medium shot, slow push in", chars=["xuyan", "laisan"], night="shed",
         comp=f"medium shot across the railing: on the left inside the shed {XU_R}, framed from the waist up, {APRON} already bunched in his right hand from the first frame, his face three-quarter to screen right toward Lai San, never the lens; flat and calm, not smiling: steady eyes, lips moving between words; on the right beyond the wooden railing on the snowy path {LAI1}, framed from the waist up, both hands already raised before his chest, his face three-quarter to screen left toward Xu Yan, never the lens; stunned: eyes wide, lips pressed shut; {HANDS}; exactly two people",
         lines=[("xuyan", "肯幹就留下。挑甘蔗、洗竹匾，工錢跟大家一樣。", "淡淡地，不笑")],
         motion=f"Xu Yan tosses the apron over the railing and Lai San catches it against his chest with both hands; {quiet('Lai San')}",
         zh="中景、慢推（送糖坊路邊裁切）：左邊棚裡許硯（袖子捲著、圍裙已解下）把圍裙隔著欄杆一拋，右邊欄杆外賴三兩手接住、愣住、嘴閉著；許硯淡淡地說，不笑 ← 因為 c11、c13"),
    dict(loc="shed_c", cam="Close-up, slow push in", chars=["xuyan"], night="shed",
         comp=f"close-up of {XU_R}, by the brick stove, framed from the chest up with space above his head, his face three-quarter to screen right, never the lens; dry and set: brows drawing together, lips pressed shut; behind him only the white steam over the pan, soft",
         lines=[("xitong", "收留放火的人。宿主心真大，出了事系統不管。", "冷"),
                ("xuyan", "不用妳管，出了事，我自己擔。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan's brows draw together, he lets out one slow breath and tucks his chin; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（送糖坊裁切；拍法 11 不寫藍光，面板沒有）：許硯眉頭一皺、吐一口氣、下巴一收；全程嘴閉著（系統畫外、心裡話）。本集的鬥嘴"),
    dict(loc="shed_c", cam="Medium shot, slow push in", chars=["erniu"], night="shed",
         comp=f"medium shot of {ERNIU}, standing by the round stone basin, framed from the waist up, {PADDLE} already leaning upright against the basin beside him from the first frame, his right hand already raised to his face, his face three-quarter to screen right toward the path beyond the right edge of the frame, never the lens; grudging, not smiling: jaw set, a stubborn frown, lips moving between words; behind him the shed and the steam, soft; {HANDS}",
         lines=[("erniu", "許兄弟心軟，我這雙眼睛可不軟，我盯著他。", "不服氣，不笑")],
         motion="Wang Erniu taps two fingers just under his own eyes twice as he speaks; after the last word he lowers the hand and folds his arms",
         zh="中景、慢推（送糖坊裁切）：二牛的木槳第一格已經靠在石盆邊，兩根手指在自己眼下點兩下，朝畫右路上的賴三（畫外）不服氣地說，不笑。稿子『推桿往石磨上一插、哼一聲』不拍（一鏡一個動作）"),
    dict(loc="shed", cam="Low-angle wide shot, slow push in", chars=["laisan", "xiaohe"], night="shed",
         comp=f"low-angle wide shot, the camera at knee height: in the soft foreground the cut ends of the stack of sugarcane bundles by the railing; in the middle by the stack, now inside the shed, {LAI_A}, framed full figure, the apron already tied from the first frame, {CANE} already on his right shoulder, his face three-quarter to screen left toward the stone basin, never the lens; fawning: a hollow eager smile, lips moving fast between words; beyond him on the right, small and soft, {XIAOHE}, standing, {BOWL} held in both hands, her face toward the stove, her lips closed; {HANDS}; exactly two people",
         lines=[("laisan", "謝許秀才！我這就挑，挑到天黑都行。", "哈腰")],
         motion=f"Lai San limps two steps toward the stone basin with the cane on his shoulder as he speaks; after the last word his eyes slide sideways to the bowl of white sugar in the girl's hands and his smile drops; {quiet('little Xiaohe', 'her')}",
         zh="低角度全景（膝蓋高）、慢推（送糖坊圖）：前景虛焦的甘蔗斷口；賴三已經在棚裡、圍裙繫好，第一格已經扛著一捆甘蔗，一拐一拐往石盆走兩步、哈腰說；說完眼睛斜溜到右後方小禾捧著的那碗白糖，討好的笑掉下來（結尾）。許硯不入鏡（一鏡少一個人）；剪在走到一半"),
    # ---- scene 2: the twenty-sixth morning, the Xu shop (set-xuji-pu-l1: shelves left, doorway back middle, counter right).
    dict(chapter="許記與對街魏記", loc="shop_t", cam="Insert close-up, slow push in", chars=[], night="shop",
         comp=f"insert close-up, the shot opens directly on {STACK} lying flat on the dark wooden counter top, seen low from the side so only the pale edges of its blank sheets show, from its very first frame, one small hand in a thick opaque peach-pink silk sleeve cuff already lifting the corner of the top sheet; only the hand, its sleeve cuff, the stack of blank sheets and the counter top are in the frame",
         lines=[("tangxiaotang", "第七日、第十日、第十九日……今天，第二十六日。", "邊翻邊念")],
         motion=NOBODY + "the small hand turns the blank sheets over one after another, faster and faster, a thick sheaf flipping past, and then presses the newest sheet flat with its palm",
         zh="插鏡、慢推（第一格就是櫃面上的帳本；送鋪子櫃面 `set-xuji-pu-cabinet-l1`）：一疊用繩線縫邊的空白紙（低角度從側邊拍，只見紙邊），唐小棠的手（桃粉不透的袖口）一張張翻得越來越快、最後一掌壓平；她的台詞畫外。帳本只寫空白的紙疊（拍法 7、27：不寫 book／ledger，字不入鏡）"),
    dict(loc="shop", cam="Wide shot, slow push in", chars=["erniu", "laisan"], night="shop",
         comp=f"wide shot of the shop from beside the shelves on the left: in the bright doorway in the middle of the back wall {ERNIU}, framed full figure, both hands on the shafts of {CART} stacked with six plain wooden crates, already rolled in over the threshold from the first frame, his face three-quarter to screen right toward Xu Yan off screen right at the counter, never the lens; happy and out of breath: a wide grin, lips moving fast between panting words; just behind him at the threshold {LAI_A}, framed full figure, {CRATE} held in both arms, his face down; on the right {COUNTER} along the white wall; {HANDS}; exactly two people",
         lines=[("erniu", "糖坊今天又出了六箱白糖，後頭還有！", "喘，咧嘴，好消息可以笑")],
         motion=f"Wang Erniu brings the cart to a stop and slaps the top crate once with his flat palm as he speaks; {quiet('Lai San')}",
         zh="全景、慢推（送許記鋪子圖 `set-xuji-pu-l1`：架子在左、門在後牆正中、櫃檯寫在右牆前，同第 20、21、24 集）：後牆正中亮亮的門口，二牛第一格已經把載著六只木箱的手推車推過門檻，停住、拍一下箱子，喘著咧嘴說（本鏡可以笑）；他身後門檻上賴三（腰繫圍裙、跛腳）抱著一箱、低頭、嘴閉著。稿子的櫃檯在左照真人圖改到右牆；前景的會員木牌不拍（掛著的牌長字）；許硯不入鏡（他在畫右外的櫃檯）"),
    dict(loc="shop", cam="Close-up, slow push in", chars=["xuyan"], night="shop",
         comp=f"close-up of {XU_D}, standing at the counter, framed from the chest up with space above his head, {CRATE} before him at the lower edge of the frame, its lid already lifted off and leaning against it from the first frame, heaped with fine white sugar like fresh snow, his right hand already buried in the sugar; his face three-quarter to screen right, eyes on the sugar, never the lens; quietly sure: steady eyes, lips pressed shut; behind him the dark shelves, soft",
         lines=[("xitong", "叮。白糖量產，達成。鬥商第二十六日，許記是魏記兩倍。", "冷，宣布")],
         panel=[("白糖量產，達成", "task"), ("鬥商第二十六日，許記是魏記兩倍", "task")],
         motion=f"Xu Yan lifts a handful of the white sugar and lets it run slowly back through his fingers into the crate; {SILENT_HE}",
         zh="近景、慢推（送鋪子圖）：許硯面前的木箱第一格蓋子已經拿下、靠在箱邊，箱裡雪白的糖；他抄起一把讓糖從指縫流下去，眼神一定；全程嘴閉著（系統畫外；拍法 11 不寫藍光，兩塊面板由剪接疊上）"),
    dict(loc="shop", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="shop",
         comp=back(f"{STACK} lying flat on the counter top before her, both her hands already resting flat on it from the first frame; facing us beyond her across the counter, a little left of the middle, {XU_D}, framed from the waist up, his face three-quarter to screen right toward her, never the lens; listening: he says nothing, his lips closed; behind him the bright doorway, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
                   BEHIND_COUNTER, facing="facing across the counter toward him"),
         lines=[("tangxiaotang", "到今天，我們三百兩，對街才一百五十兩。", "篤定，不笑")],
         motion=f"the young woman pats the stack of sheets twice with her right palm; {HEADSTILL}; {quiet('Xu Yan')}; he listens, his eyes on her",
         zh="過肩中景、慢推（送鋪子圖）：前景右唐小棠的背影在櫃檯後，兩手壓在空白紙疊上、右掌拍兩下，篤定地說（nospeak）；櫃檯對面許硯面朝她、嘴閉著。稿子『拿毛筆舔墨』不拍（本集不寫筆：紙上的字一律不拍）"),
    dict(loc="shop_t", cam="Insert close-up, slow push in", chars=[], night="shop",
         comp=f"insert close-up, the shot opens directly on {CAKE} sitting in the middle of one square sheet of {WPAPER} on the dark wooden counter top, from its very first frame, two small hands in thick opaque peach-pink silk sleeve cuffs already holding two corners of the sheet; only the two hands, their sleeve cuffs, the paper, the cake and the counter top are in the frame",
         lines=[("tangxiaotang", "每一批都編號，誰買了幾塊，我都記在帳上。", "畫外")],
         motion=NOBODY + "the two hands fold the four corners of the white paper over the cake one after another into a neat square packet",
         zh="插鏡、慢推（第一格就是白紙上的糖霜糕；送鋪子櫃面裁切）：唐小棠的兩手（桃粉袖口）把白紙四角一摺包好（拍法 28：許記用素白紙）；她的台詞畫外。稿子『拿筆在帳本側邊點一筆』不拍（不寫筆）"),
    dict(loc="shop", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="shop",
         comp=back(f"her hands low at her sides; facing us beyond her across the counter, a little left of the middle, {XU_D}, framed from the waist up, one small square packet of {WPAPER} already resting on his right palm from the first frame, his face three-quarter to screen right toward her, never the lens; warm and teasing, not smiling: one brow raised, lips moving between words; behind him the bright doorway, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
                   BEHIND_COUNTER, facing="facing across the counter toward him"),
         lines=[("xuyan", "包糖用自家的柳溪白紙，是妳的主意吧？", "挑眉")],
         motion=f"Xu Yan weighs the packet once on his palm as he speaks and lifts his eyes to her; {HEADSTILL}; {quiet('the young woman', 'her')}",
         zh="反打（唐小棠肩後拍許硯）、慢推（送鋪子圖）：前景右唐小棠的背影、嘴閉著（不點名、不送圖：她這鏡沒有台詞）；櫃檯對面許硯掌心托著一包白紙包的糖糕，掂一下、抬眼看她、挑眉說"),
    dict(loc="shop", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="shop",
         comp=alone(f"one small square packet of {WPAPER} on the counter top before her, her right hand already resting beside it from the first frame; beyond her, soft, the shelves and the bright doorway; {HANDS}",
                    BEHIND_COUNTER),
         lines=[("tangxiaotang", "當然。紙裡有柳葉，糖是許記的，誰也冒充不了。", "得意")],
         motion=f"the young woman taps the white packet twice with her fingertips; {HEADSTILL}",
         zh="中景（從背後）、慢推（送鋪子圖）：唐小棠的背影在櫃檯後、畫面正中，用指尖在那包白紙上敲兩下，得意地說（nospeak；點頭與得意的笑交給錄音）（答 c23）"),
    dict(loc="street", cam="High-angle wide shot, slow pan from left to right", chars=[], night="street",
         comp=f"high-angle wide shot from under the eaves of the Xu shop: on the left along the paving before the Xu shop a line of six {CUSTOMERS} standing one behind another, small; across the street on the right {WEI_FRONT}, the long low dark table before it piled with rough yellow bars of soap and dark brown slabs of cane sugar, its stone step bare, and {BOY_LOOK} leaning against its door post, both hands down at his sides, small and side-on; {HANDS}; exactly seven people",
         lines=[("tangxiaotang", "二牛你看，隊伍排到街尾了！", "高興，可以笑")],
         motion=NOBODY + f"the six customers shuffle one step forward at a walking pace, their lips closed; {RED} stays leaning on the post, his lips closed",
         zh="高角度全景、搖鏡（左到右；送縣城大街 `set-xianjie-l1`）：左邊許記門口一條六個人的隊伍（拍法 25：稿子二十人改寫實際入鏡的六人）慢慢往前挪；搖到右邊對街魏記：長矮桌堆滿黃粗皂與紅糖糕、台階空著，暗紅短褂的瘦年輕人靠著門柱；唐小棠的台詞畫外"),
    dict(loc="street_w", cam="Medium shot, slow push in", chars=["weishaoqing"], night="street",
         comp=f"medium shot looking across the street at the shop with the red silk: in the soft foreground the end of its long low dark table piled with rough yellow bars of soap; on its stone step {WEI}, framed from the knees up, {FAN} from the first frame, his face three-quarter to screen left toward the Xu shop across the street, never the lens; cold, not smiling: jaw tight, eyes narrowed, lips moving slowly between words; behind him by the door post {BOY_LOOK}, standing stiffly upright, both hands at his sides, side-on, his lips closed; {HANDS}; exactly two people",
         lines=[("weishaoqing", "一上午了，門口一個客人都沒有？", "冷下臉，拖長音")],
         motion=f"Wei Shaoqing taps the closed fan once into his left palm as he speaks; {quiet(RED)}",
         zh="中景、慢推（送對街魏記門面的免費裁切 `set-xianjie-weiji-l1`）：前景虛焦的長桌一角與黃粗皂；台階上魏少卿第一格已經站在台階邊、合著的摺扇在掌心一敲，冷著臉朝畫左的許記說（不笑，拍法 30；扇子一直合著）；身後門柱邊暗紅短褂的瘦年輕人已經站直、側面、嘴閉著。稿子『從門裡走出來、夥計彈直』不拍（一鏡一個動作）；銅鑼不寫（只在第 24 集）"),
    dict(loc="street_w", cam="Medium shot side-on, slow push in", chars=[], night="street",
         comp=f"medium shot side-on of {BOY_LOOK}, standing by the door post of the shop with the red silk, framed from the waist up, seen side-on, his face in profile to screen left, shoulders hunched, both hands already raised a little before his chest from the first frame; timid, not smiling: head ducked, lips moving between mumbled words; behind him the dark doorway and a fold of red silk, soft; {HANDS}",
         lines=[("weijihuoji", "少爺，全去對面買糖霜糕了。", "越說越小聲")],
         motion=NOBODY + f"{RED} turns one flat palm toward the far side of the street, his mouth moving on the words, and shrinks back half a step",
         zh="側面中景、慢推（送魏記門面裁切）：暗紅短褂的瘦年輕人（魏記夥計，不點名、不送圖、只拍側面，聖經〈小角色〉）縮著肩，一隻手掌朝對街一攤、往後縮半步，越說越小聲（嘴照錄音動；稿子的近景改中景側面；銅鑼不寫）"),
    dict(loc="street_w", cam="Low-angle medium shot, slow push in", chars=["weishaoqing"], night="street",
         comp=f"low-angle medium shot of {WEI}, standing behind the long low dark table before the shop with the red silk, framed from the knees up so the whole table stays in the frame, both hands already gripping the near edge of the table from the first frame, the closed fan tucked in his sash, the table piled with rough yellow bars of soap and dark brown slabs of cane sugar; furious, not smiling: teeth gritted, the corners of his mouth pulled down; on the step behind him {BOY_LOOK}, side-on, his lips closed; {HANDS}; exactly two people",
         motion="Wei Shaoqing heaves the whole table over toward us in one move, and the soap bars and sugar slabs tumble and bounce across the grey stone paving; the young man in dark red jumps back one step; nobody speaking, their lips closed",
         zh="低角度中景、慢推（整個動作留在畫面裡；送魏記門面裁切）：魏少卿兩手第一格已經抓住長桌邊，一掀整張桌子翻過來，粗皂與紅糖糕在石板上彈著滾開；夥計往後一跳；扇子插在腰帶；咬牙、嘴角下拉（拍法 30 輸的鏡不笑）（無台詞）"),
    dict(loc="street_w", cam="Close-up, slow push in", chars=["weishaoqing"], night="street",
         comp=f"close-up of {WEI}, framed from the chest up with space above his head, breathing hard, one lock of black hair fallen loose from his topknot over his brow, {FAN} raised beside his chin from the first frame, his face three-quarter to screen left toward the Xu shop across the street, never the lens; cold fury, not smiling: eyes hard, jaw clenched, lips moving low between words; behind him a fold of red silk, soft",
         lines=[("weishaoqing", "去告訴孫掌櫃，讓他們笑，今晚可以動手了。", "壓低聲音，咬牙")],
         motion="Wei Shaoqing tilts his head a little back toward his shoulder as he speaks, his eyes staying on the Xu shop; after the last word his lips press into a thin line",
         zh="近景、慢推（送魏記門面裁切）：魏少卿喘著氣、髮髻掉下一縷，合著的扇子第一格已經舉在下巴邊，眼睛冷冷看畫左的許記，頭往身後一偏，壓低聲音說（結尾）。稿子『慢慢打開灑金摺扇』改合著（第 21 集 fix1：打開的扇面長假字）；稿子的紅燈籠改紅綢（掛著的燈籠長字）"),
    # ---- the bridge: the back room of the Xu shop at dusk (set-xuji-pu-houjian-l1); the doorway LEFT, the back door RIGHT.
    dict(chapter="許記後間", loc="back", cam="Medium shot, slow push in", chars=["laisan"], night="back",
         comp=f"medium shot of {LAI_A}, standing at the long table, framed from the waist up, one grey rag already under his right hand on the table top from the first frame, his face three-quarter to screen left toward the dark doorway on the left, never the lens; still and listening: eyes sliding toward the doorway, lips pressed shut; on the table beside him the bamboo trays of small square white cakes, the small oil lamp lighting him from below; behind him the dark empty shelves, soft; {HANDS}",
         lines=[("xuyan", "賴三，鋪子交給你，明早我們跟頭一班車來。", "從前面鋪子喊")],
         motion=f"Lai San's hand with the rag stops still on the table top while he listens toward the doorway; {quiet('Lai San')}",
         zh="中景、慢推（送許記後間 `set-xuji-pu-houjian-l1`：暗的空木架；長桌、三只竹匾糖霜糕、桌角小竹籃、一盞油燈都寫在鏡頭裡）：賴三在長桌邊，拿抹布的手停住、朝畫左的門洞聽、嘴閉著；許硯的話從前面鋪子畫外。稿子 c30（7.5 秒、兩個人說話）在這裡拆成兩鏡：一鏡一張臉一件事"),
    dict(sid="s30b", loc="back", cam="Medium shot, slow push in", chars=["laisan"], night="back",
         comp=f"medium shot of {LAI_A}, standing at the long table, framed from the waist up, one grey rag in his right hand, already half bent toward the dark doorway on the left from the first frame, his face three-quarter to screen left toward it, never the lens; fawning: a quick eager smile, lips moving between words; the small oil lamp on the table lighting him from below; behind him the dark empty shelves, soft; {HANDS}",
         lines=[("laisan", "放心，許秀才，門我閂得牢牢的。", "哈腰朝門洞喊")],
         motion="Lai San bows twice toward the dark doorway as he calls back; after the last word he straightens and the smile drops off his face",
         zh="中景、慢推（送後間）：賴三朝畫左的門洞連哈兩次腰、陪笑著喊（可以陪笑），說完直起身、笑掉下來。稿子的簾子不寫（布簾會長字），寫暗的門洞"),
    dict(loc="back_c", cam="Insert close-up, slow push in", chars=[], night="back",
         comp="insert close-up, the shot opens directly on one thick plain wooden bar lying half across the dark planks of a back door in two iron brackets, from its very first frame, a thin hand in a checked grey-brown sleeve cuff already gripping its end; warm lamplight from the side; only the hand, its sleeve cuff, the bar, the brackets and the door planks are in the frame",
         motion=NOBODY + "the hand pushes the bar all the way across into the far bracket with one firm slide",
         zh="插鏡、慢推（第一格就是門閂；送後間）：賴三的瘦手（灰褐格紋袖口）把橫木門閂一推到底（無台詞）。稿子『接著從袖口抽出一小包灰紙包』移到 s33 第一格（一鏡一個動作）"),
    dict(loc="back_c", cam="Low-angle close-up, slow push in", chars=["laisan"], night="back",
         comp=f"low-angle close-up of {LAI_A}, framed from the chest up with space above his head, lit from below by the small oil lamp on the table, his face three-quarter to screen right toward the corner of the table beyond the right edge of the frame, never the lens; guilty and jumpy: eyes darting, lips moving in a low mutter between words; behind him only the dark shelves, soft",
         lines=[("laisan", "邊角料不記帳，少三塊沒人知道。", "自言自語，心虛")],
         motion="Lai San glances left and right once as he mutters, then his eyes settle on the corner of the table beyond the right edge of the frame",
         zh="低角度近景、慢推（油燈從下往上照；送後間）：賴三左右張望一下、自言自語，眼睛落到畫右外的桌角（小竹籃）。稿子『上唇冒汗、舔嘴唇』不寫（拍法 12 皮膚上不寫細小東西）"),
    dict(loc="back_c", cam="High-angle insert close-up, slow push in", chars=[], night="back",
         comp=f"high-angle insert close-up, the shot opens directly on three small broken pieces of white cake frosted with fine white sugar, each lying in the middle of one small square sheet of {YPAPER}, coarse and lumpy, on the plain table top beside one small bamboo basket of broken cake ends, from its very first frame, a thin hand in a checked grey-brown sleeve cuff already holding one small packet of folded grey paper tipped just above them; only the hand, its sleeve cuff, the packet, the three pieces, the yellowish paper and the basket are in the frame",
         motion=NOBODY + "a thin trickle of greyish white powder sifts from the tipped packet over the three pieces and vanishes at once into their white frosting",
         zh="主觀插鏡（俯拍）、慢推（第一格就是黃紙上的三塊邊角料；送後間）：三塊糖霜糕的邊角各放在一張粗黃紙上（不是許記的白紙，拍法 28），賴三的瘦手拿著灰紙包，一細道灰白的粉篩下去、一下就融進糖霜看不出來（無台詞）。稿子『揀出三塊、各用一張黃紙包好』不拍（第一格已經放好；包好的三包在 s34）"),
    dict(loc="back", cam="Medium shot, slow push in", chars=["laisan"], night="back",
         comp=f"medium shot of {LAI_A}, standing at the long table, framed from the waist up, three small square packets of {YPAPER} already in his right hand from the first frame, the small oil lamp on the table lighting him from below; his face three-quarter to screen left toward the dark doorway on the left, never the lens; sly and nervous, not smiling: eyes narrowed, lips moving low between words; behind him the dark shelves, soft; {HANDS}",
         lines=[("laisan", "白紙張張有數，用黃紙包，拉幾天肚子死不了人。", "小聲")],
         motion="Lai San tucks the three packets into the front of his jacket as he speaks and pats it flat once; after the last word he glances toward the doorway",
         zh="中景、慢推（送後間）：賴三手上第一格已經拿著三包粗黃紙包，塞進短衣前襟、拍一下，小聲說，說完回頭看一眼門洞（結尾）。稿子『彎腰吹熄油燈、畫面暗下來』交給剪接（切黑）與音效（一鏡一個動作）"),
    # ---- scene 3: the twenty-seventh morning, the shop front (set-xianjie-xuji-l1, -shi-l1, set-xianjie-l1).
    dict(chapter="許記門口", loc="street_x", cam="Wide shot, slow push in", chars=["xuyan", "laisan"], night="street",
         comp=f"wide shot from the street of the Xu shop front: {XU_D}, standing on the paving before the doorway, framed full figure, the last pale plank already leaning on the stack of plank doors by the doorway from the first frame, his right hand already lifted, palm toward the line, his face three-quarter to screen right toward the line of customers, never the lens; brisk and friendly: a small smile, lips moving between words; beside the stacked planks on the left {LAI_A}, small, framed full figure, side-on, his lips closed; on the right along the paving a line of six {CUSTOMERS}, one behind another, small, their lips closed; {HANDS}; exactly eight people",
         lines=[("xuyan", "各位久等，今天的糖霜糕一人限兩塊！", "朝隊伍")],
         motion=f"Xu Yan raises his flat palm a little higher toward the line as he speaks; {quiet('Lai San')}; the customers shuffle and look toward him, their lips closed",
         zh="全景、慢推（送許記門面的免費裁切 `set-xianjie-xuji-l1`）：許硯第一格已經把最後一塊門板疊好，站在門口石板上朝右邊的隊伍抬手說（可以微笑）；左邊疊著的門板旁賴三（小、側面、嘴閉著）；右邊石板上六個客人排成一列（拍法 25）。唐小棠在店裡掀糖箱不拍（全景裡她會轉頭）；二牛卸完箱趕車走交給音效（一鏡少兩個人）；稿子的推軌改慢推"),
    dict(loc="street_t", cam="Insert close-up, slow push in", chars=[], night="street",
         comp=f"insert close-up behind the stack of pale plank doors leaning by the shop front, the shot opens directly on three small square packets of {YPAPER} held together in a thin hand in a checked grey-brown sleeve cuff, from its very first frame, a second hand in a plain grey cotton sleeve cuff already held flat beneath them, palm up; only the two hands, their sleeve cuffs and the three packets are in the frame",
         motion=NOBODY + "the thin hand presses the three packets down into the grey-sleeved palm, and the grey-sleeved hand closes round them and draws back into its sleeve",
         zh="插鏡、慢推（第一格就是兩隻手；送門前長櫃與石板的免費裁切 `set-xianjie-shi-l1`）：門板後面，賴三的瘦手（灰褐格紋袖口）把三包黃紙包按進灰袖的手心，灰袖的手一握、縮回袖子（無台詞）"),
    dict(loc="street_x", cam="Medium shot, slow push in", chars=["xuyan"], night="street",
         comp=f"medium shot along the line at the shop front: in the soft right foreground the shoulder of a woman customer in a plain grey-blue cotton robe and a cloth head wrap, out of focus; in the middle {GREY}, standing in the line, framed from the waist up, one small white cake already at his mouth in a scrap of {YPAPER} from the first frame; on the left by the doorway {XU_D}, framed from the waist up, his face three-quarter to screen right toward the man in grey, never the lens; frowning, not smiling: brows knotted, eyes on the yellowish paper, lips moving between words; {HANDS}; exactly three people",
         lines=[("xuyan", "這位大哥，你手上這塊，不是剛從我們這兒買的吧？", "看見，皺眉")],
         motion="Xu Yan takes one step toward the man in grey as he speaks; the man in grey bites into the cake, his face staying turned away from us; the woman says nothing, her lips closed",
         zh="中景、慢推（送許記門面裁切）：前景右虛焦一個排隊婦人的肩；中間灰衣客人（只拍側背、布包頭壓低、不給正臉）第一格已經把黃紙包的糖糕送到嘴邊、咬一口；左邊門口許硯看見黃紙、皺眉、往他走一步說"),
    dict(loc="street_t", cam="Medium shot, slow push in", chars=[], night="street",
         comp=f"medium shot on the grey stone paving before the shop: {GREY}, framed full figure, both hands already pressed to his stomach from the first frame, the bitten cake and its scrap of {YPAPER} in one hand; on either side of him two {CUSTOMERS}, side-on, soft; {HANDS}; exactly three people",
         motion=NOBODY + "the man in grey doubles over, staggers one step and sinks down onto his side on the paving, curled up and lying still, the bitten cake and the yellowish paper falling from his hand; the two customers step back; nobody speaking, their lips closed",
         zh="中景、慢推（整個動作留在畫面裡；送石板裁切）：灰衣客人（背影）兩手第一格已經捂著肚子，彎腰、踉蹌一步、側身倒在石板上蜷著不動，糖糕與黃紙掉出手；兩邊排隊的人往後退（無台詞；答 c37：他沒回答）。稿子的跟拍改慢推；『不吐、不流血、不抽搐』照拍法 18 寫成正面的『蜷著不動』"),
    dict(loc="street_t", cam="Low-angle insert close-up, slow push in", chars=[], night="street",
         comp=f"low-angle insert close-up on the grey stone paving, the shot opens directly on one bitten small white cake lying on a crumpled sheet of {YPAPER}, from its very first frame, and beside it one small neat square packet of {WPAPER}; only the paving, the cake, the yellowish paper, the white packet and the feet that pass are in the frame",
         motion=NOBODY + "feet in black cloth shoes hurry past behind them across the paving, and the gust of their passing lifts one corner of the yellowish paper",
         zh="主觀低角度插鏡、慢推（第一格就是石板上的糖糕；送石板裁切）：咬了一口的糖霜糕壓在皺黃紙上，旁邊一包許記的白紙包；一雙雙布鞋的腳踩過去，風掀起黃紙一角（無台詞）"),
    dict(loc="street", cam="High-angle wide shot, slow push in", chars=["xuyan"], night="street",
         comp=f"high-angle wide shot from just inside the Xu shop's doorway, its dark door frame soft at the left edge: on the grey stone paving a little right of the middle {GREY}, curled on his side and lying still; around him six {CUSTOMERS} backing away on every side, a widening ring of bare paving around him; at the left by the doorway {XU_D}, framed full figure, standing frozen, his face three-quarter to screen right toward the man on the ground, never the lens; shocked: eyes wide, lips pressed shut; {HANDS}; exactly eight people",
         lines=[("kerenfu", "糖裡有毒！", "尖叫，短喊")],
         motion=f"the customers back away from the man on the ground at a walking pace and the ring of bare paving grows; {quiet('Xu Yan')}; the customers say nothing, their lips closed",
         zh="高角度全景、慢推（送縣城大街圖；前景虛焦許記的門框）：中右灰衣客人蜷在石板上（背影）；六個客人往四面退開、空出的一圈越來越大；左邊門口許硯僵住、嘴閉著；婦人的尖叫畫外（結尾，懸念 → 第 27 集第一場）。唐小棠在櫃檯邊不入鏡（全景裡她會轉頭；第 27 集第一鏡交代）；稿子『慢升』改慢推（一個運鏡、不升高）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e026-r2/script.md`（c01–c40 對應 s01–s40；c30 拆成兩鏡 s30／s30b，共 41 鏡；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-17）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e021-e030.md`（拍法 1–30 條）。第 3 篇章〈搶親〉第六集。",
    "- 內部工作編號 926（`hailuo/{ff,clips}-dh-e926.json`、`colab/runs/e926/extras.json`、`colab/runs/e926-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e926-dh/`）；發布 slug `zhong-tian-qu-qi-e026-r2`。不放集數、不放片名卡；s01 接第 25 集 s40b 之後的隔天早上（聖經接點 25→26：糖坊，唐小棠把字條收進錢箱）；s40 交給第 27 集（接點 26→27：灰衣客人倒地、「糖裡有毒！」、許硯在門口；唐小棠在店裡櫃檯邊、不入鏡）。",
    "- 照第 25 集審稿後的寫法與第 21–25 集挑片學到的一開始就照做：`OFFSCREEN_SPEECH = False`；背影或畫外的人說話時，每張朝鏡頭的臉都寫不說話、嘴閉著、在聽，不寫會引人笑或開口的字；掛著的東西不點名（會員木牌不拍、魏記的紅綢寫成搭在素木樑上、後間的簾子寫成暗的門洞）；不寫 open（扇子合著、蓋子寫拿下）；道具與接觸寫在第一格；紙一律空白、帳本寫成縫邊的空白紙疊；寫人數。",
    "- **唐小棠不露嘴說話、本集也不露臉**（拍法 3）：她的台詞全部從背後拍（s01、s07、s12 糖坊；s21、s24 鋪子；nospeak，spec 拿掉她的圖與身分句；兩顆高丸子各一條粉緞帶、後頸露出、頭不動、正背對鏡頭）；s18、s22 只拍她的手、s25 畫外；s23 只有背影、不點名不送圖；全景 s02、s17、s19、s35、s40 不拍她。**算盤本集沒有**（拍法 20）。",
    "- **場景圖說了算**（拍法 29，協調者 2026-11-17 決定，每張放大看過）：糖坊 `set-tangfang-l1`（全景）與 `set-tangfang-jia-l1`（近鏡），**新的免費裁切 `set-tangfang-lu-l1`**（欄杆、雪路、禿柳、溪：賴三隔著欄杆的四鏡）；圖上沒有石磨，稿子的推磨改成倒甘蔗汁、推桿改成熬糖的長木槳。許記鋪子 `set-xuji-pu-l1`（櫃檯寫在右牆前、門在後牆正中，稿子的『櫃檯在左』不照用）與櫃面 `set-xuji-pu-cabinet-l1`；大街 `set-xianjie-l1` 與第 24 集的裁切（魏記門面、許記門面、門前石板）；後間 `set-xuji-pu-houjian-l1`（暗的空木架，桌、竹匾、竹籃、油燈寫在鏡頭裡）。**不需要試鏡**。",
    "- **魏少卿**扇子一直合著（s26 敲掌心、s28 插腰帶、s29 舉在下巴邊；稿子 c29『打開灑金摺扇』不照用）；本集都不笑（拍法 30：冷臉、掀桌、咬牙）。**魏記夥計**寫「二十來歲、暗紅布短褂、黑布包頭的瘦年輕人」，不點名、不送圖、只拍側面，兩手空著（銅鑼只在第 24 集）；聲音 Alnilam。**c40 婦人的尖叫**用新的 `MINOR`「排隊的婦人」（Despina，系列沒人用過的聲音），不入鏡。灰衣客人只拍背影與側背；排隊的客人寫六個（拍法 25）。",
    "- 長鏡要買的秒數（BUY）：照錄音核過（見 `r2.py` 的 BUY 註解）；稿子 c30（許硯畫外加賴三回話，約 7.5 秒）拆成 s30／s30b。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音的人聲長度為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯（l1、angle-a；帶笑的 angle-b 整集不送）、王二牛（l1、angle-a）、許小禾（l1 與角度圖，照 `pilot.py`）、賴三 l1、魏少卿 l1。唐小棠整集不送圖。魏記夥計、灰衣客人、排隊的客人、手都不送圖。場景見上面。",
    "- 共用檔：程式都沒改（畫面上說話的人都在 `build-r2.py` 的 `EN`；夥計與婦人從不列在 chars，聲音放 `MINOR`）；`gen-dh.mjs`、`pilot.py`、`cast.json` 不動；`refs-live` 加一張免費裁切（新 id）與 README 一段。精修文字的 CG 立領句由本檔結尾的 `live_clips()` 在 build 後從 `clips-dh-e926.json` 拿掉（第 22–25 集的做法）。",
    "- `colab/runs/e926/extras.json`（照第 25 集）與 `colab/runs/e926-live/spec.json`（`mkspec.py` 產生；種子 9261101／9261102）。",
    "- 免費準備：scratchpad `prep926.sh`（`DRY=1 … st1-ep.sh 926` → `pilot.py` → `retake.py` → `colab-jobs.json` 加 output_path、套 swap_pictures（絕對路徑）→ 逐鏡查送的場景圖與人物圖 → 精修用的分隔句 → `preflight-prompts.py` → 否定名詞、會長字的名詞與掛著的東西掃描）。",
    "- 配樂：糖坊暖而帶勁的勞動 cue，s08 賴三出現停一拍轉低，s15 冷單音；大街明亮的市集 cue，s20「叮」，s28 掀桌重拍轉低弦；後間只有低弦與油燈劈啪，s33 輕鈴；門口明亮 cue，s38 倒地抽空，s40 大重音。音效見 script.md〈音樂與音效〉（另外：s01 錢箱蓋、s03 汁倒進鍋、s30b 之後吹熄油燈、s35 二牛趕車走，都交給音效）。",
]

# Long shots: seconds to buy. Measured 2026-11-17 against the 36 recordings (~/mokaair-work/videos/zhong-tian-qu-qi-e926-dh/audio;
# wave length and silencedetect -35 dB speech span; e013's test: a shot holds (buy - 0.3) x 1.1 s of speech, half a second
# between lines, so 5 s holds 5.17 s, 6 s 6.27 s, 8 s 8.47 s). faster-whisper medium read every take back, one clip per process,
# numpy input, once plain and once with the previous line and the line as context (audio/fw926.txt; audio/README-retakes.txt).
# 8 s: s15 (the system's jab a15 3.73 s + 0.5 + his thought a16 1.97 s = 6.21 s, only 0.06 s inside a 6 s clip: the script's
#      long shot, one face, kept whole); s40 (a36 1.32 s, but it is the episode's last shot: the hook needs a held tail, as
#      e923 s40, e924 s36 and e925 s40b).
# 6 s: every other speaking shot. The tightest: s05 (a05's third take 5.96 s), s18 (a19 5.73 s, the insert her counting runs over), s29
#      (a29 5.23 s), s19 (a20 5.08 s), s37 (a35 5.04 s), s04 (a04 5.03 s), s09 (a09 5.00 s).
# 5 s: the inserts s06 (a06 3.37 s off screen), s22 (a23 3.37 s off screen), the clerk s27 (a28 3.08 s) and the silent
#      inserts s31, s33, s36, s39 as gen-dh buys them. The script's c30 (Xu Yan off screen and Lai San's answer, about 7.5 s)
#      is split into s30 (a30 3.57 s) and s30b (a31 3.49 s): one face, one beat each.
# No shot runs over about 10 s. Re-recorded (first takes in audio/take1/, a05's second in audio/take2/; audio/README-retakes.txt):
# a12 and a26, Tang Xiaotang's YIN pitch outliers against her lines in the same scene (a26's retake still high, 350 Hz, kept: an
# off-screen happy call across the street); a01 (十捆 heard 石墾 plain; the retake from a scratch copy reading "十 kǔn", TTS input
# only); a05 (the start heard 吃完這個 plain; the second take ran 170 Hz, outside Xu Yan's 96-148 Hz, so a third, 124 Hz, is kept);
# a36 (the scream heard 唐禮要讀 plain, r0.00; the retake reads 藏裡有毒, r0.75).
BUY = {"s15": 8, "s40": 8}


# ---- the refine text (e022 review 必改 12, as e023-e025): hailuo/clips-dh-e926.json column 0 is the motion text
# refine-prep.py sends with a picked d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era "Tang
# Xiaotang's high stand-up collar stays closed at her throat." and names her in "<names> shown in <Picture 1>"; in a back shot
# that draws the collar back and turns her face to the lens. Every shot of her here is a back shot: the sentence goes and her
# name becomes "the young woman seen only from behind". Column 1 is recomputed.
COLLAR = "Tang Xiaotang's high stand-up collar stays closed at her throat. "
BACK_NAME = "the young woman seen only from behind"


def live_clips(path):
    import hashlib
    import json
    import re
    clips = json.load(open(path, encoding="utf-8"))
    for key, row in clips.items():
        text = row[0]
        if COLLAR in text:
            text = text.replace(COLLAR, "")
            m = re.search(r"\[Shot 1\] 3D CG\. (.+?) shown in <Picture 1> (keeps?) ", text)
            names = [n for n in m.group(1).split(" and ") if n != "Tang Xiaotang"]
            who = " and ".join(names + [BACK_NAME])
            who = who[0].upper() + who[1:]
            verb = "keep" if names else "keeps"
            text = text.replace(m.group(0), f"[Shot 1] 3D CG. {who} shown in <Picture 1> {verb} ", 1)
            assert "Tang Xiaotang" not in text, (key, "her name is left in a back shot's refine text")
        assert "stand-up collar" not in text, key
        row[0] = text
        row[1] = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    open(path, "w", encoding="utf-8").write(json.dumps(clips, ensure_ascii=False, separators=(",", ":")))


if __name__ == "r2spec":
    import atexit
    import os
    atexit.register(live_clips, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hailuo", f"clips-dh-e{EP}.json"))
