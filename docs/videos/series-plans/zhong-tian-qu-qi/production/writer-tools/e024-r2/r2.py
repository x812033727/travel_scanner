"""Episode 24 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e024-r2/script.md
(c01-c36 = s01-s36, c15 split into s15 and s15b; the CG-era r2 script), including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and
「真人版的改動（2026-11-16）」, which override the tables. Every line is the script's, word for word; only the staging changes.
Bible: production/r2-bible-e021-e030.md (rules 1-30, the 23->24 and 24->25 hand-overs, the props, people and picture tables). The
fourth episode of arc 3 〈搶親〉: the first morning of the trade war on the county street, the sugar workshop at night and at
first light, the third morning on the county street.

Written from the start the way e023-r2/r2.py stands AFTER its independent review (../e023-r2/review.md), with the e921-e922
picks (colab/runs/e92{1,2}-live/{picks-merged.tsv,fix1/mkspec.py}) and e920-live/review3-plan.md:
- OFFSCREEN_SPEECH = False (rule 15): every shot with an off-screen line, a thought or a system line writes the silence of
  each person on screen (quiet(), SILENT_HE).
- Tang Xiaotang never speaks on camera (rule 3) and in this episode never shows her face at all: every shot of her is from
  behind (TBACK, HEADSTILL; nospeak; spec drops her pictures and identity sentence): s04, s07, s09, s12, s17 (scene 1),
  s30, s32, s34 (scene 3); in s01 she is unnamed (no picture) carrying a door plank; s10 and s13 show only her hand; s35
  only the back of her buns at the left edge, unnamed. "Her face" in the script (blinking, wrinkling her nose, biting her
  lip, pale) is left to the recordings.
- The gold abacus (rule 20 as corrected 2026-11-16): only in one insert, s08 (her "不降" beat, the script's "slaps the abacus
  flat on the counter"), the prop picture prop-jinsuanpan-l1, which already shows the long flat abacus lying on the shop's
  own dark counter-cabinet. c04 (one bead), c12 (a rattle of beads) are not shot; the sound effects carry them. No medium
  shot of her writes the abacus.
- Wei Shaoqing's fan stays closed (e921 fix1 s28): the script's fanning at the window (c06, c36) is a closed fan tapped on
  the sill. He may smile (rule 30): s06, s36. He wears the green jade ornament of his portrait (e020 review 必改 7).
- The Wei shop boy (bible 〈小角色〉: about twenty, thin, a dark red cloth short jacket, a black cloth head wrap, a small bronze
  gong and a wooden mallet, this episode only; the script's grey jacket and red headband are the CG look) has no picture and
  is never named: chars never lists him, so his two lines (s01, s11) are off-screen lines by build-r2's rule even though he is
  seen, side-on, in a wide or medium-wide shot. MINOR gives his voice: Alnilam (bible). The townspeople are six customers
  (rule 25), the Wei men two in grey (rule 25), never "crowd"; one ox cart (the script's three would be three oxen in one
  frame: rule 26's way, the carts' noise to the sound effects).
- Name only what should be drawn (e920 fix1): the tokens are plain pale wooden tokens on red cords, smooth and blank (the
  script's plum-blossom carving dropped: a carved face grows marks); no sign, no writing; the deposit is one small cloth
  pouch; the sugar is rule 28's wording (dark brown slabs; fine white sugar like fresh snow in a shallow clay bowl; brown
  clay funnels, points down, each standing in a squat clay jar).
- A night set with no set picture drifts to a street-stall look (e921): the night close shots in the workshop send a free
  crop of the night picture.
- No more than three named faces (rule 1); unnamed foregrounds get no picture (rule 2); nobody flipped (rule 9); one visible
  action per shot; props in a named hand from the first frame; nothing negated by name (rule 18).

THE AXES (rule 29: the set picture decides):
- The county street (set-xianjie-l1; bible 23->24 names it): the street runs straight away from us; the Xu shop on the LEFT
  (tall plank doors folded back, a dark doorway, a long low plain wooden counter along its front), the Wei shop across the
  street on the RIGHT (two storeys, lattice windows upstairs, swags of red silk over its open doorway, a long low table
  before it). The picture is a bright clear morning with a blue sky and no frost: the script's frost and grey-blue light are
  not written (the third morning is told by the bowl and the lines). The red silk already hangs in the picture: the
  script's unveiling (c01) is not shot. Wei Shaoqing's window is the upper floor on the right. People at the Xu shop look
  screen right across the street; Wei Shaoqing looks down to screen left.
- The Xu shop inside (set-xuji-pu-l1, as e020-e021): the shelves on the LEFT wall, the open front doorway in the middle of
  the back wall, the counter along the RIGHT wall (written; not in the picture). Tang Xiaotang behind the counter in the right
  foreground, seen from behind, faces the doorway; Xu Yan and Wang Erniu face us beyond her.
- The sugar workshop (set-tangfang-ye-l1 at night, set-tangfang-l1 at first light; bible rule 29): the brick stove with its
  iron pan in the LEFT foreground, a long wall on the left with a row of funnels hanging from a bar and a low bench below,
  a round stone basin on a pedestal in the middle, the open side and its railing on the RIGHT with the snow and the creek.
  The script's stove on the right is turned round: Wang Erniu at the stove on the LEFT, Xu Yan beyond him at the bench by
  the left wall, to the RIGHT of Erniu in frame; Erniu looks screen right, Xu Yan screen left. The picture's first light is
  a warm low gold sun on snow: "cold blue dawn" is written as the low morning sun of the picture.

PLACES (the coordinator's decisions, 2026-11-16; every picture looked at full size; script.md 〈真人版的改動〉):
- Street wide shots s01, s02, s29: set-xianjie-l1. Free crops of it (new ids, own l1): the Xu shop front
  set-xianjie-xuji-l1 (the people at the Xu shop seen from the street side: s03, s05, s14, s15, s15b, s18, s30-s32, s34,
  s35); the Wei shop front across the street set-xianjie-weiji-l1 (looking across from the Xu shop: s09, s11, s33); the
  upper floor across the street set-xianjie-lou-l1 (Wei Shaoqing at his window: s06, s36); the low counter in front of the
  Xu shop and the paving set-xianjie-shi-l1 (inserts s10, s16, and s17 at the stall).
- The shop inside s04, s07, s12: set-xuji-pu-l1 (gen-dh's "Xu family shop" picture, kept); the token insert s13 on the
  counter top: set-xuji-pu-cabinet-l1; the abacus insert s08: prop-jinsuanpan-l1.
- The workshop at night s19: set-tangfang-ye-l1; night close shots and the insert s20-s23: its free crop
  set-tangfang-ye-jia-l1 (stove, steam, the wall of funnels, the lamp). First light s27, s28: set-tangfang-l1; close shots and
  the insert s24-s26: its free crop set-tangfang-jia-l1.
- gen-dh SET phrases: "market street" (set-shiji-t1, swapped; the street prompts never say "Xu family shop", which comes first
  in gen-dh's list), "Xu family shop", "sugar workshop".
- Inserts and shots with nobody named (s10, s11, s13, s16, s21, s24, s33) open their motion with NOBODY; the abacus insert s08 with NOBODY_ABACUS
  (its clips-dh text holds "keeps the first frame's set layout and props. " once instead).
- Shared files: no code changed (every speaker but the shop boy is in build-r2.py's EN, and he is never on the chars list; no
  new gen-dh place; cast.json untouched). Six new free pictures in refs-live (new ids with their own l1, rule 19; README
  paragraph).
"""
EP = 924  # internal working number; the published slug is zhong-tian-qu-qi-e024-r2
SLUG = "zhong-tian-qu-qi-e024-r2"
EP_TITLE = "對街五文一塊，他把紅糖淋成雪白（重製版 r2）"
OUTLINE_SECONDS = 179  # script.md: about 179 s, 36 shots (18 + 10 + 8)
TARGET_MINUTES = [3, 4]
TITLE = "對街五文一塊，他把紅糖淋成雪白｜種田娶妻打天下 第24集（重製版）"
DESCRIPTION = "鬥商第一天一早，許記剛卸下門板，對街魏記就敲鑼喊：肥皂五文一塊！排隊的人跑了一半。二牛要跟著降價，唐小棠說不降：他砸的是宰相府的錢，我們砸的是自己的命。她擺出木盆收舊皂頭換新皂，又發會員木牌，老客回頭七成。許硯知道拚價還是輸，兌換了放了九天的製糖法，拿起隔壁攤最便宜的紅糖：今晚回柳溪，我讓它變得比雪還白。當夜在柳溪糖坊，他在凝好的紅糖上淋了一勺黃泥水，二牛嚇得問淋了泥還能吃嗎。天一亮，漏斗裡的糖一層層變白。可是十斤紅糖只出一碗。第三天早上，唐小棠從糖行跑回來：全州的紅糖，昨天一夜被人買光了。對街二樓的魏少卿笑著說：全州的糖，包括鄰鎮。沒糖，看你熬什麼。《種田娶妻打天下》第 24 集（重製版）。"
THUMB = ("比雪還白", "s24")
CHARACTERS = ["xuyan", "tangxiaotang", "erniu", "weishaoqing", "weijihuoji", "xitong"]
MINOR = {
    "weijihuoji": {"id": "weijihuoji", "name": "魏記夥計",
                   "appearance": "East Asian young man of about twenty, thin, an ancient Chinese Song-dynasty shop boy's dark red cloth short jacket and a black cloth head wrap, a small bronze gong in his left hand and a wooden mallet in his right",
                   "voice": {"provider": "gemini", "name": "Alnilam", "style": "標準國語，咬字清楚，台北人平常說話的語調；二十歲左右的店鋪夥計，男聲、年輕、嗓門大、在街上扯開喉嚨吆喝，句尾拉長"}},
}
MUSIC = "one cue per scene: a busy morning market cue of drums, gongs and bamboo flute that thins to a single note when the queue runs off, one accent on a firm refusal and one bright electronic accent on an exchange; then a low woodwind with crackling fire at night in a thatched sugar shed, turning into bright strings at first light, one light accent; then the bright strings broken off by a low suspense cue on a cold morning street, one big accent before it ends; ancient Chinese rural drama, no vocals"

# Places (gen-dh SET phrases in the first words of each LOC; see the docstring).
COUNTER_ST = "the long low plain wooden counter along the front of the Xu shop"
STREET = ("a narrow stone-paved street running straight away from us under a clear pale blue sky; on the left the open front of the "
          "Xu shop, its tall plank doors folded back, a dark doorway and a long low plain wooden counter along its front; on the "
          "right across the street a two-storey wooden shop front with dark lattice windows upstairs and long swags of red silk "
          "hung over its wide open doorway, a long low dark table before it; plain wooden shop fronts further down both sides")
WEI_FRONT = "a two-storey wooden shop front with long swags of red silk hung over its wide open doorway and a long low dark table before it"
COUNTER = "one long waist-high counter of plain dark wood with a thick flat top and a plain panelled front"
THE_COUNTER = "the long waist-high dark wooden counter"
SHOP = ("bare dark wooden shelves along the left wall above a long low dark wooden cabinet, a few stacks of pale yellow soap bars "
        "on the lower shelves, the wide open front doorway in the middle of the back wall between dark wooden lattice panels with "
        f"the bright street beyond it, plain white panelled walls on the right with {COUNTER} standing along them, a floor of large "
        "grey stone tiles with bars of morning sunlight across it")
FUNNELS = "a row of brown clay funnels, points down, each standing in a squat clay jar"
SHED = ("a long open shed under a deep thatched roof on rough wooden posts, a brick stove with one wide iron pan in the left "
        f"foreground, a long plaster wall on the left with a low wooden bench along it and {FUNNELS} on the bench, wooden barrels "
        "along the wall, a round stone basin on a pedestal in the middle, the open right side with a wooden railing, snow and "
        "the creek beyond it")
LOC = {
    "street": f"On the market street of the county town on a cold clear winter morning: {STREET}; low morning sun from the right, long shadows on the paving",
    "street_x": "On the market street of the county town on a cold clear winter morning, at the open front of the Xu shop: its tall plank doors of pale wood folded back, a dark doorway, a dark lattice transom above, in low morning sunlight",
    "street_w": f"On the market street of the county town on a cold clear winter morning, looking across the street from the Xu shop: {WEI_FRONT}, in bright morning sunlight",
    "street_up": "On the market street of the county town on a cold clear winter morning, looking up at the upper floor of the shop across the street: dark wooden lattice windows under eaves of grey tiles, plain wooden boards, a swag of red silk below, a clear pale blue sky",
    "street_t": f"On the market street of the county town on a cold clear winter morning, at {COUNTER_ST}, on the grey stone paving in low morning sunlight",
    "shop": f"In the Xu family shop on a cold clear winter morning: {SHOP}; bright morning light from the doorway, the corners of the room dim",
    "shop_t": "In the Xu family shop on a cold clear winter morning, on the dark wooden counter top in soft light",
    "shed_n": f"In the sugar workshop by the Liuxi creek at night: {SHED}; red firelight from the stove, the warm glow of one small oil lamp on the stone basin, steam rising from the pan, cold blue night outside",
    "shed_nc": "In the sugar workshop by the Liuxi creek at night, under the thatched shed by the brick stove: steam rising, red firelight, the warm glow of one small oil lamp, cold blue night beyond",
    "shed_d": f"In the sugar workshop by the Liuxi creek at first light: {SHED}; low warm gold sunlight from the right across the snow and the floor, long shadows",
    "shed_dc": "In the sugar workshop by the Liuxi creek at first light, under the thatched shed by the wall of brown clay funnels, in low warm gold sunlight from the right",
}
LIGHT = {
    "street": "the low morning sunlight stays unchanged",
    "shop": "the morning light from the doorway stays unchanged",
    "shed_n": "the red firelight and the warm lamp glow stay unchanged",
    "shed_d": "the low warm gold morning light stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_N = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves rolled to the forearms"
# the script: the old grey outer coat at night in the workshop (and at first light, the same night)
XU_C = "Xu Yan, in an old plain grey cloth outer coat worn open over his faded blue-grey scholar's robe"
ERNIU = "Wang Erniu, in his coarse brown hemp short jacket with rolled sleeves"
WEI = ("Wei Shaoqing, in his sapphire-blue brocade robe woven with gold thread, a white jade pendant at his waist, a small green "
       "jade ornament at the front of his topknot")
FAN = "one closed folding fan held upright in his right hand like a short slim stick, its dark bamboo ribs pressed tight together"
BOY = ("one thin young shop boy in a dark red cloth short jacket and a black cloth head wrap, a small bronze gong in his left hand "
       "and a wooden mallet in his right, seen side-on, his face in profile")
CUSTOMERS = "customers in plain Song-dynasty cotton robes and cloth head wraps"
TOKENS = "a neat row of small plain pale wooden tokens, each the size of a palm, smooth and blank, each on a short red cord"
TOKEN = "one small plain pale wooden token the size of a palm, smooth and blank, on a short red cord"
TUB = "one large round empty wooden tub"
SLAB = "one dark brown slab of raw cane sugar, rough and pitted"
SLABS = "a shallow round bamboo basket heaped with dark brown slabs of raw cane sugar, rough and pitted"
BOWL = "one shallow clay bowl heaped with fine white sugar like fresh snow"
POUCH = "one small plain grey cloth pouch tied with a string"
PADDLE = "one long wooden paddle"
MUD = "thin opaque yellow-brown mud water, gritty with silt"
# bible rule 20 as corrected by the coordinator (2026-11-16): the long flat one of prop-jinsuanpan-l1, inserts only; the prop
# picture shows it lying on the shop's dark counter-cabinet, which is where s08 puts it.
ABACUS = ("one long flat gold abacus, as long as her forearm, a thin gold frame, lying flat on the dark wooden counter top: a long "
          "row of thin gold rods set close side by side across its width, one thin gold crossbar running along its whole length, "
          "small round gold beads above and below the crossbar on every rod")
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
NOBODY_ABACUS = ("Throughout the shot the abacus keeps the long flat shape it has in <Picture 1>, lying flat on the dark wooden counter "
                 "top. The pictures fix the place and the objects only, never the mood. ")
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with all of her black hair gathered "
         "up into two round buns set high on her head, a short pink silk ribbon wrapped around each bun, the "
         "nape of her neck bare above a pink inner collar, and her light peach-pink silk shoulders; the back of her "
         "head toward us the whole time, her ear the furthest round her head we ever see")
HEADSTILL = "the young woman with the two high round buns keeps her head still, the back of her head toward us the whole shot"
# s01: Tang Xiaotang unnamed, small, from behind (no picture)
SMALL_TANG = ("one young woman in light peach-pink silk with her black hair in two round buns set high on her head, a short pink "
              "ribbon round each, seen only from behind")


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def only_tang(side=None):
    if not side:
        return "she is the only young woman with two high round buns in the frame"
    return (f"she is the only young woman with two high round buns in the frame, and she stays in the {side} "
            f"foreground from the first frame to the last")


def back(rest, where, frame="framed from the waist up", facing="facing into the frame toward him", shot="over-the-shoulder medium shot"):
    """Tang Xiaotang seen from behind (rule 3) in the right foreground; the man she speaks to faces us beyond her."""
    return f"{shot} from close behind {TBACK}, {where} in the right foreground, {frame}, {facing}; {only_tang('right')}; {rest}"


SHOTS = [
    # ---- scene 1: the first morning of the trade war, the county street and the Xu shop (23->24: the next morning).
    dict(chapter="大街與許記", loc="street", cam="Wide shot, slow push in", chars=["xuyan"], night="street",
         comp=f"wide shot down the street from beside the Xu shop: in the left foreground in front of the Xu shop {XU_N}, framed from the knees up, already standing still from the first frame holding one tall plank of pale wood upright beside him with both hands, his face in profile to screen right toward the shop across the street, never the lens; wary: brows drawn, lips pressed shut; one step beyond him {SMALL_TANG}, holding a second tall plank upright, her back to us, turned toward the shop across the street; across the street on the right before the red silk {BOY}, standing on its step beside the long low table piled with rough yellow bars of soap; {HANDS}; exactly three people: Xu Yan, the young woman seen only from behind and the shop boy",
         lines=[("weijihuoji", "魏記開張，肥皂五文一塊，先到先得！", "敲鑼，扯開嗓子")],
         motion=f"the shop boy across the street strikes the gong twice and shouts with his mouth wide open, sweeping his mallet toward the heap of soap; {quiet('Xu Yan')}; Xu Yan and the young woman stand still holding their planks; the young woman keeps her head still, the back of her head toward us the whole shot",
         zh="全景、慢推（送縣城大街圖 `set-xianjie-l1`：許記在左、對街魏記在右、紅綢已經掛著）：左前許硯第一格已經停下、兩手扶著一塊門板，側臉朝畫右看對街、嘴閉著；他身後一步是抱著另一塊門板的唐小棠背影（不點名、不送圖）；對街紅綢下的台階上魏記夥計（暗紅短褂、黑布包頭，側面，不點名、不送圖）敲兩下鑼、張嘴吆喝、鑼槌往黃皂堆一掃。稿子『紅綢被拉下來』不拍（圖上紅綢已掛著），揭綢交給音效；稿子的霜與跟拍不寫（圖是晴天、一鏡一個運鏡）"),
    dict(loc="street", cam="High-angle wide shot, slow push in", chars=["erniu"], night="street",
         comp=f"high-angle wide shot looking down on the street: in front of {COUNTER_ST} on the left six {CUSTOMERS} standing in a loose line; {ERNIU}, standing at the end of the line by the shop front, small in the frame, his face three-quarter to screen right toward the shop across the street, never the lens; anxious, not smiling: brows up, lips pressed shut; across the street on the right the swags of red silk and the long low table piled with rough yellow bars of soap; {HANDS}; exactly seven people, all small in the frame",
         motion=f"three of the six customers leave the line and hurry across the street toward the shop with the red silk on the right; Wang Erniu reaches one arm out after them and lets it drop; {quiet('Wang Erniu')}",
         zh="高處俯拍全景、慢推（送大街圖）：許記門口六個客人排成一行（拍法 25 寫實際人數），其中三個快步穿過石板街往右邊魏記走；二牛在隊尾伸手想攔、手垂下，不笑、嘴閉著（無台詞）"),
    dict(loc="street_x", cam="Medium shot, slow push in", chars=["erniu"], night="street",
         comp=f"medium shot from the street side of {ERNIU}, standing at the open front of the shop, framed from the waist up, both hands empty, his right arm already pointing back across the street to the right from the first frame, his face three-quarter to screen left toward the dark doorway, never the lens; anxious, not smiling: brows up, eyes wide, lips moving fast between words; behind him the folded-back plank doors and the dark doorway; {HANDS}",
         lines=[("erniu", "許兄弟，排隊的人跑了一半，全去對街了！", "急，不笑")],
         motion="Wang Erniu jabs his pointing arm toward the street again as he speaks into the doorway, his shoulders tense; after the last word he keeps pointing",
         zh="中景、慢推（送許記門面的免費裁切 `set-xianjie-xuji-l1`）：二牛站在許記門口，兩手空著，右手已經往後指著對街，臉朝畫左的門裡（許硯在裡面）急著說，不笑（原版必修）。稿子『轉身朝鋪子裡喊』改成第一格已經朝門裡（一鏡一個動作）"),
    dict(loc="shop", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="shop",
         comp=back(f"both her hands resting on the counter top; facing us beyond her in the bright doorway at the back, a little left of the middle, {XU_N}, standing just inside the threshold, framed from the knees up, his face three-quarter to screen right toward her, never the lens; grim: brows drawn, lips pressed shut; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
                   "standing behind the counter along the right wall"),
         lines=[("tangxiaotang", "才五文！他那塊黃皂，連豬油錢都不夠。", "不敢相信")],
         motion=f"the young woman's shoulders stiffen and her right hand presses flat on the counter top; {HEADSTILL}; {quiet('Xu Yan')}; he glances back over his shoulder at the street and back at her",
         zh="過肩中景、慢推（送許記鋪子圖 `set-xuji-pu-l1`：架子在左、門在後牆正中、櫃檯在右牆，同第 20、21 集）：前景右唐小棠的背影站在櫃檯後，肩膀一繃、右手按在櫃檯上，不敢相信地說（nospeak，拍法 3）；門口逆光裡許硯看著她、嘴閉著。稿子『近景下巴以上、撥一下算珠』改背影；算珠交給音效（拍法 20）"),
    dict(loc="street_x", cam="Medium close-up, slow push in", chars=["xuyan"], night="street",
         comp=f"medium close-up from the street side of {XU_N}, leaning one shoulder against the edge of the folded-back plank door, both arms already folded across his chest from the first frame, framed from the chest up with space above his head, the low morning sun lighting one side of his face, his face three-quarter to screen right toward the shop across the street, never the lens; narrow-eyed, not smiling: eyes narrowed, lips moving between words; behind him the pale plank door and the dark doorway, soft",
         lines=[("xuyan", "鬥商第一天，他就賠本賣，拿宰相府的錢砸，砸得起。", "瞇眼")],
         motion="Xu Yan narrows his eyes at the shop across the street as he speaks; after the last word he holds still, arms folded",
         zh="中近景、慢推（送許記門面裁切）：許硯靠在折起的門板邊、雙手抱胸，晨光照半邊臉，瞇眼看畫右對街，不笑地說。稿子『把門板靠在牆邊』不拍（第一格已經抱胸），門板靠牆交給音效"),
    dict(loc="street_up", cam="Low-angle medium shot, slow push in", chars=["weishaoqing"], night="street",
         comp=f"low-angle medium shot from the street below of {WEI}, leaning his forearms on the sill of one dark lattice window swung open on the upper floor, framed from the chest up, {FAN}, his face three-quarter to screen left looking down toward the Xu shop below, never the lens; lazy and amused: a slow smile, eyes half-lidded, lips moving lazily between words; behind him the dim room inside the window; around the window the dark lattice and the plain boards under the grey-tiled eaves",
         lines=[("weishaoqing", "許老闆，三十天，本公子陪你慢慢玩。", "居高臨下，拖長音")],
         motion="Wei Shaoqing tilts his head and taps the closed fan twice on the window sill as he speaks, smiling down; after the last word he keeps smiling",
         zh="仰角中景、慢推（送對街二樓的免費裁切 `set-xianjie-lou-l1`）：魏少卿倚在推開的木格窗台上往畫左下的許記看，合著的摺扇在窗台上敲兩下，拖長音、輕佻地笑著說（本鏡可以笑，拍法 30；扇子一直合著，第 21 集 fix1）。稿子『慢慢搧扇子』改成合著敲窗台"),
    dict(loc="shop", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "erniu"], nospeak=["tangxiaotang"], night="shop",
         comp=back(f"both her hands resting on the counter top; facing us beyond her at the far end of the counter, a little left of the middle, {ERNIU}, framed from the waist up, his right hand already raised over the counter top from the first frame, his face three-quarter to screen right toward her, never the lens; hot and anxious, not smiling: brows drawn, jaw set, lips moving fast between words; behind him the bright doorway, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
                   "standing behind the counter along the right wall"),
         lines=[("erniu", "那我們也降價，降到四文，看誰撐得久！", "急，拍櫃檯")],
         motion=f"Wang Erniu brings his open hand down flat on the counter top with a slap as he speaks; {HEADSTILL}; {quiet('the young woman', 'her')}",
         zh="過肩中景、慢推（送鋪子圖）：前景右唐小棠的背影在櫃檯後、嘴閉著（她這鏡不說話）；櫃檯那頭二牛面朝她，一掌拍在櫃檯上，急著說，不笑（原版必修 s07）"),
    dict(loc="shop_t", cam="Insert close-up, slow push in", chars=[], night="shop",
         comp=f"insert close-up, the shot opens directly on {ABACUS}, from its very first frame, one small hand in a thick opaque peach-pink silk sleeve cuff already raised flat just above it; only the hand, its sleeve cuff, the abacus and the dark counter top are in the frame",
         lines=[("tangxiaotang", "不降。他砸的是宰相府的錢，我們砸的是自己的命。", "乾脆")],
         motion=NOBODY_ABACUS + "the open hand comes down flat on the abacus with one sharp slap and stays there, the beads jumping once",
         zh="插鏡、慢推（第一格就是櫃檯上平放的長金算盤；送道具圖 `prop-jinsuanpan-l1`，圖上本來就是放在鋪子的深色櫃面上；不寫『set layout stays』，第 22 集必改 11）：唐小棠的手（桃粉不透的織錦袖口）啪地一掌按在算盤上，算珠一跳；她的台詞畫外。稿子『近景下巴以上、喀地把算盤拍平』改成插鏡（拍法 3、20：算盤只在插鏡；她不露臉）"),
    dict(loc="street_w", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="street",
         comp=f"medium shot from close behind {TBACK}, standing on the stone step just outside the doorway of the Xu shop, framed from the waist up, facing straight away from us toward the street, {TUB} already set down on the step at her feet at the lower edge of the frame; {only_tang()}; beyond her across the street, soft, the shop with the red silk and a few {CUSTOMERS} passing; {HANDS}",
         lines=[("tangxiaotang", "舊皂頭拿來換新皂，一塊折一半，只收五分！", "朝街上喊")],
         motion=f"the young woman claps her hands once and raises her right hand, beckoning to the street; {HEADSTILL}; the passers-by across the street slow and turn toward her",
         zh="中景（從背後）、慢推（送對街魏記門面的免費裁切 `set-xianjie-weiji-l1`）：唐小棠的背影站在許記門口石階上、正背對鏡頭朝街，空木盆第一格已經擺在腳邊；她拍一下手、舉手招呼，朝街上喊（nospeak）。稿子『從櫃檯後抱著木盆走到門口』不拍（一鏡一個動作，抱盆走路交給剪接與音效）"),
    dict(loc="street_t", cam="Insert close-up, slow push in", chars=[], night="street",
         comp=f"insert close-up, the shot opens directly on {TUB} standing on the grey stone step from its very first frame, a few small worn grey ends of soap at its bottom; a woman's rough hand in a coarse brown cloth sleeve cuff above it on the left, and a small hand in a thick opaque peach-pink silk sleeve cuff holding one new pale yellow bar of soap on the right; only the two hands, their sleeve cuffs, the soap and the tub are in the frame",
         motion=NOBODY + "the rough hand drops one small worn grey soap end into the tub, then opens, and the small hand lays the new pale yellow bar of soap into its palm",
         zh="插鏡、慢推（第一格就是石階上的木盆；送門前長櫃與石板的免費裁切 `set-xianjie-shi-l1`）：做粗活的婦人的手（褐色粗布袖口）把一小塊灰皂頭丟進盆裡、手掌攤開，唐小棠的手（桃粉袖口）把一塊新的淡黃肥皂放進她掌心（無台詞）"),
    dict(loc="street_w", cam="Wide shot, slow push in", chars=[], night="street",
         comp=f"wide shot looking across the street at the shop with the red silk: on its step beside the long low table piled with rough yellow bars of soap {BOY}, framed from the knees up, the mallet already frozen in the air above the gong from the first frame; stunned: mouth open, shouting; in the foreground three {CUSTOMERS}, each with one small grey soap end in hand, walking away from the shop toward the left, seen from the side and from behind; {HANDS}; exactly four people",
         lines=[("weijihuoji", "喂！五文一塊，比她那邊便宜十倍啊！", "愣住，喊")],
         motion=NOBODY + "the shop boy shouts after the three customers with his mouth wide open, the mallet still in the air; the three customers keep walking away to the left, their backs to him",
         zh="全景、慢推（送對街魏記門面裁切）：魏記夥計（側面、不點名、不送圖）鑼槌停在半空，張嘴朝走掉的客人喊；前景三個拿著灰皂頭的客人往畫左走回許記（側面與背影）。拍法 25：魏記夥計中景以上只拍側面"),
    dict(loc="shop", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="shop",
         comp=back(f"{TOKENS} laid along the counter top in front of her, her right arm already lifted over them from the first frame; beyond the counter, soft, two {CUSTOMERS} leaning in, a man in brown and a woman in grey, seen side-on; {HANDS}; exactly three people, the young woman in the foreground seen only from behind",
                   "standing behind the counter along the right wall", facing="facing across the counter toward the customers"),
         lines=[("tangxiaotang", "老客憑這塊木牌，往後每次買皂都打九折！", "甜甜地吆喝")],
         motion=f"the young woman sweeps her silk sleeve once over the row of tokens toward the customers; {HEADSTILL}; the two customers lean closer to look at the tokens",
         zh="過肩中景、慢推（送鋪子圖）：前景右唐小棠的背影，面前櫃檯上一排素面小木牌（穿紅繩、沒有字、不刻梅花紋：刻紋會長出記號），衣袖往木牌上一揮，甜甜地吆喝（nospeak；笑與眨眼從背後看不到，交給錄音）；櫃檯外兩個客人虛焦、側面。腰間算盤響成一串交給音效（拍法 20）"),
    dict(loc="shop_t", cam="Insert close-up, slow push in", chars=[], night="shop",
         comp=f"insert close-up, the shot opens directly on {TOKEN} lying in the open palm of an old man's hand in a worn brown cloth sleeve cuff above the dark wooden counter top from its very first frame, a small hand in a thick opaque peach-pink silk sleeve cuff resting on top of it; only the two hands, their sleeve cuffs, the token and the counter top are in the frame",
         lines=[("xitong", "叮。老客回頭，七成。", "冷，宣布")],
         panel=[("老客回頭，七成", "task")],
         motion=NOBODY + "the small hand presses the token gently into the old palm and lets go, and the old hand closes round it and draws it back toward his chest",
         zh="插鏡、慢推（第一格就是木牌在老客掌心；送鋪子櫃面 `set-xuji-pu-cabinet-l1`）：唐小棠的手把木牌按進老客的手（褐色舊布袖口），老客握緊、收回胸前；系統畫外，面板由剪接疊上（拍法 11）"),
    dict(loc="street_x", cam="Medium close-up, slow push in", chars=["xuyan"], night="street",
         comp=f"medium close-up from the street side of {XU_N}, standing by the folded-back plank door, framed from the chest up with space above his head, his right hand already at his chin from the first frame, his face three-quarter to screen right toward the shop across the street, never the lens; unsmiling and thinking: brows drawn, eyes hard, lips moving low between words; in the soft lower left foreground the shoulders of two {CUSTOMERS} at the counter, out of focus; behind him the pale plank door and the dark doorway, soft; {HANDS}",
         lines=[("xuyan", "留得住老客，可他天天五文，拚價還是輸。", "不笑，壓低聲音")],
         motion="Xu Yan rubs his chin slowly as he speaks, his eyes staying on the shop across the street; after the last word he lowers his hand",
         zh="中近景、慢推（送許記門面裁切）：許硯在門邊，手摸下巴，眼睛一直在畫右對街，不笑、壓低聲音說（原版建議 s14）；左下前景虛焦兩個客人的肩（不點名）"),
    # The script's long shot (c15, 11 s: thought, exchange, the system's jab, thought) is split at the exchange, one change of
    # face each (e022 s35/s35b, e023 s13/s13b): s15 thought + exchange (the panel), s15b the jab + his answer. Rule 11: no blue light.
    dict(loc="street_x", cam="Close-up, slow push in", chars=["xuyan"], night="street",
         comp=f"close-up from the street side of {XU_N}, standing by the folded-back plank door, framed from the chest up with space above his head, his face three-quarter to screen right toward the shop across the street, never the lens; thinking hard: eyes narrowing, brows drawn, lips pressed shut; behind him the pale plank door and the dark doorway, soft",
         lines=[("xuyan", "得有一樣東西，是魏記做不出來的。", "心裡話，嘴閉著", "inner"),
                ("xitong", "兌換：製糖法。", "冷，宣布")],
         panel=[("兌換：製糖法", "reward")],
         motion=f"Xu Yan's eyes narrow and then go still, as if something has just been decided; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（稿子 c15 的長鏡在兌換處拆開；送許記門面裁切；拍法 11 不寫藍光，面板由剪接疊上）：許硯眼睛一縮、定住；全程嘴閉著（心裡話與系統畫外）"),
    dict(sid="s15b", loc="street_x", cam="Close-up, slow push in", chars=["xuyan"], night="street",
         comp=f"tight close-up from the street side of {XU_N}, framed from the shoulders up with a little space above his head, his face three-quarter to screen right toward the shop across the street, never the lens; dry and wry: lips pressed shut, one corner of his mouth turned down; behind him the pale plank door, soft",
         lines=[("xitong", "宿主這個獎勵放了九天，終於想起來了。", "冷"),
                ("xuyan", "放著才叫存糧，現在拿出來剛好。", "心裡話，嘴閉著", "inner")],
         motion=f"one corner of Xu Yan's mouth turns down, and then slowly a closed-lipped smile spreads across his face; {SILENT_HE}; he is thinking, not speaking",
         zh="近景（比 s15 再近，肩以上）、慢推（送許記門面裁切）：聽完系統挖苦，許硯嘴角往下一撇，再慢慢抿著嘴笑開；全程嘴閉著（系統句與心裡話畫外）"),
    dict(loc="street_t", cam="Insert close-up, slow push in", chars=[], night="street",
         comp=f"insert close-up, the shot opens directly on {SLABS} sitting on {COUNTER_ST} from its very first frame, a man's hand in a faded blue-grey sleeve rolled to the forearm already lifting {SLAB} from it; only the hand, its sleeve, the slab and the basket are in the frame",
         lines=[("xuyan", "最便宜的紅糖，一斤才十五文。", "賣關子")],
         motion=NOBODY + "the hand raises the slab into the low sunlight and turns it once, and a few dark crumbs fall back into the basket",
         zh="插鏡、慢推（第一格就是竹籃裡的紅糖糕；送門前長櫃裁切，長櫃當隔壁的小攤）：許硯的手（藍灰袖口捲起）拿起一塊黑褐、坑坑疤疤的紅糖糕（拍法 28）舉到陽光下轉一圈，碎糖掉回籃裡；他的台詞畫外"),
    dict(loc="street_t", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="street",
         comp=back(f"her hands low at her sides; facing us beyond her, a little left of the middle, {XU_N}, standing behind {SLABS} on the low counter, framed from the waist up, {SLAB} already held up in his right hand from the first frame, his face three-quarter to screen right toward her, never the lens; pleased with himself: one brow up, lips pressed shut; behind him the stone paving and the street, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
                   "standing at the low counter in front of the Xu shop"),
         lines=[("tangxiaotang", "紅糖？黑乎乎的，拿它跟魏記比什麼？", "皺鼻子")],
         motion=f"the young woman lifts her silk sleeve and waves it once in front of her face; {HEADSTILL}; {quiet('Xu Yan')}; he turns the slab once in his fingers",
         zh="過肩中景、慢推（送門前長櫃裁切）：前景右唐小棠的背影，抬起衣袖在面前搧一下，嫌棄地說（nospeak；皺鼻子交給錄音）；對面許硯拿著紅糖糕、挑眉、嘴閉著。稿子是許硯的手在左前景、她正面，照拍法 3 改從她背後"),
    dict(loc="street_x", cam="Medium close-up, slow push in", chars=["xuyan"], night="street",
         comp=f"medium close-up from the street side of {XU_N}, standing by the folded-back plank door, framed from the chest up with space above his head, {SLAB} already held up in his right hand beside his face from the first frame, his face three-quarter to screen right toward her off screen right, never the lens; cocky and sure: a sly smile, eyes bright, lips moving between words; behind him the pale plank door and the dark doorway, soft; {HANDS}",
         lines=[("xuyan", "今晚回柳溪，我讓它變成白的，比雪還白。", "得意")],
         motion="Xu Yan tosses the slab up a hand's height and catches it again as he speaks, smiling; after the last word he holds it up beside his face",
         zh="中近景、慢推（送許記門面裁切）：許硯把紅糖糕舉在臉旁，往上一拋、接住，得意地笑著說（本鏡可以笑）。稿子『回頭對二牛一抬下巴』不拍（一鏡一個動作）（結尾）"),
    # ---- scene 2: the sugar workshop at Liuxi, night (set-tangfang-ye-l1); Erniu at the stove LEFT, Xu Yan beyond him RIGHT.
    dict(chapter="柳溪糖坊", loc="shed_n", cam="Wide shot, slow push in", chars=["erniu", "xuyan"], night="shed_n",
         comp=f"wide shot down the shed: in the left foreground {ERNIU}, standing at the brick stove, framed from the knees up, {PADDLE} already in both hands stirring the dark bubbling syrup in the wide iron pan from the first frame, his face three-quarter to screen right toward Xu Yan, never the lens; tired, not smiling: sweat on his brow, lips moving between panting words; beyond him on the right of him at the low bench along the left wall {XU_C}, framed full figure, one brown clay pitcher already tilted in his right hand over the funnels from the first frame, his face turned down to the funnels, never the lens; intent: lips pressed shut; {HANDS}; exactly two people",
         lines=[("erniu", "熬了兩個時辰，這鍋黑糖漿，到底要變成什麼？", "邊攪邊喘")],
         motion=f"Wang Erniu keeps stirring the pan as he speaks, panting, and wipes his brow once with the back of his wrist; {quiet('Xu Yan')}; he pours a thick dark stream of syrup into one funnel after another",
         zh="全景、慢推（送夜裡的糖坊圖 `set-tangfang-ye-l1`：灶在左前、漏斗架在左牆、石盆與油燈在中、開口在右；稿子的『灶在右』照拍法 29 改到左）：左前二牛在灶前用長木槳攪鍋裡冒泡的黑糖漿，邊喘邊說、抹汗，不笑；他身後畫面右邊一點、左牆邊矮長凳旁，許硯（外披舊灰外衣）用陶壺把糖漿一個個灌進漏斗、嘴閉著"),
    dict(loc="shed_nc", cam="Medium close-up, slow push in", chars=["xuyan"], night="shed_n",
         comp=f"medium close-up of {XU_C}, standing at the low bench by the wall, framed from the chest up with space above his head, his right hand already resting on the rim of one brown clay funnel at the lower edge of the frame, his face three-quarter to screen left toward Wang Erniu off screen left, never the lens; calm and sure: steady eyes, lips moving between words; steam drifting past his face, the warm lamp glow on one side of it; behind him the plaster wall and the dim shed, soft; {HANDS}",
         lines=[("xuyan", "變成白糖。先讓它在漏斗裡凝住，再淋一樣東西。", "")],
         motion="Xu Yan taps the rim of the funnel once with his knuckle as he speaks; after the last word he looks back at the funnels",
         zh="中近景、慢推（送夜裡糖坊的免費裁切 `set-tangfang-ye-jia-l1`：灶、蒸氣、牆上一排漏斗、油燈；第 21 集：夜戲不送場景圖會長出夜市攤子）：許硯的手搭在漏斗口，用指節敲一下，臉朝畫左的二牛（畫外）說；蒸氣飄過臉、油燈照半邊。稿子『放下陶壺』不拍（第一格手已經在漏斗上）"),
    dict(loc="shed_nc", cam="Insert close-up, slow push in", chars=[], night="shed_n",
         comp=f"high-angle insert close-up, the shot opens directly on the wide mouth of one brown clay funnel filled with set dark brown sugar from its very first frame, a man's hand in a grey cloth sleeve holding one wooden ladle full of {MUD} just above it; only the hand, its sleeve, the ladle and the funnel mouth are in the frame",
         motion=NOBODY + "the ladle tips and the thin yellow-brown mud water pours over the dark sugar, spreads across it and slowly sinks in",
         zh="插鏡（俯拍）、慢推（第一格就是漏斗口凝好的黑褐紅糖；送夜裡糖坊裁切）：許硯的手（灰布袖口）把一勺不透明、土黃、帶泥沙的稀泥水淋在糖面上，攤開、慢慢滲下去（原版建議：不像蛋汁）（無台詞）"),
    dict(loc="shed_nc", cam="Low-angle medium shot, slow push in", chars=["erniu"], night="shed_n",
         comp=f"low-angle medium shot from the height of the stove of {ERNIU}, standing by the stove, framed from the waist up, {PADDLE} in his left hand, his right hand already pointing toward the brown clay funnels beyond the right edge of the frame from the first frame, his face three-quarter to screen right toward Xu Yan off screen right, never the lens; horrified, not smiling: his whole face screwed up, brows up, lips moving fast between words; red firelight from below on his face, steam behind him; {HANDS}",
         lines=[("erniu", "淋泥水？那是吃的糖，淋了泥還能吃嗎？", "嚇一跳，苦著臉")],
         motion="Wang Erniu leans back away from the funnels, his face screwing up, as he speaks; after the last word he keeps pointing, aghast",
         zh="低角度中景（灶台高度往上）、慢推（送夜裡糖坊裁切）：二牛一手拿長木槳、一手指著畫右的漏斗，身子往後縮、皺起整張臉，嚇得說，不笑（原版必修）"),
    dict(loc="shed_nc", cam="Medium close-up, slow push in", chars=["xuyan"], night="shed_n",
         comp=f"medium close-up of {XU_C}, sitting on one upturned clay jar, framed from the chest up with space above his head, one rag already in his hands wiping yellow mud off his fingers from the first frame, his face three-quarter to screen left toward Wang Erniu off screen left, never the lens; amused and not explaining: a small smile, lips moving between words; the warm lamp glow on his face; behind him the dim shed and the steam, soft; {HANDS}",
         lines=[("xuyan", "泥水會把黑的帶下去，能不能吃，等天亮。", "笑，不解釋")],
         motion="Xu Yan wipes his fingers clean on the rag as he speaks, smiling; after the last word he tosses the rag over his shoulder",
         zh="中近景、慢推（送夜裡糖坊裁切）：許硯坐在倒扣的陶罐上，用破布擦掉手指上的黃泥，笑著不解釋地說，說完破布往肩上一甩（本鏡可以笑）"),
    # ---- first light (set-tangfang-l1): the picture's low warm gold sun on the snow.
    dict(loc="shed_dc", cam="Insert close-up, slow push in", chars=[], night="shed_d",
         comp="insert close-up, the shot opens directly on the wide mouth of one brown clay funnel filled with set dark brown sugar, a thin dry crust of yellow-brown silt on top, in low warm morning light from its very first frame; only the funnel mouth and the sugar in it are in the frame",
         motion=NOBODY + "slowly from the top down the dark sugar turns snow-white, layer by layer, the white creeping down into it like melting snow",
         zh="插鏡、慢推（第一格就是漏斗口；送清晨糖坊的免費裁切 `set-tangfang-jia-l1`）：紅糖從上往下一層層變成雪白（無台詞）。稿子的『冷藍晨光』照送的圖寫成低低的金色晨光（拍法 29）"),
    dict(loc="shed_dc", cam="Medium shot, slow push in", chars=["erniu"], night="shed_d",
         comp=f"medium shot of {ERNIU}, standing by the wall of funnels, framed from the waist up, one cone of sugar knocked out of a brown clay funnel already in his left hand from the first frame, its wide top half snow-white and its tip brown, his face three-quarter to screen right toward Xu Yan off screen right, never the lens; low warm morning light on his face; {HANDS}",
         lines=[("erniu", "甜的！白得像雪，甜得也像雪！", "嘗一口，眼睛發亮")],
         motion="Wang Erniu pinches a little snow-white sugar from the cone and puts it in his mouth; his eyes go wide and he breaks into a big grin as he speaks",
         zh="中景、慢推（送清晨糖坊裁切）：二牛手上一個剛敲出來的糖錐（上半雪白、尖端褐色），手指捏一小撮放進嘴裡，眼睛瞪大、咧嘴笑著說（本鏡可以笑；原版建議：不舔糖錐）"),
    dict(loc="shed_dc", cam="Close-up, slow push in", chars=["xuyan"], night="shed_d",
         comp=f"close-up of {XU_C}, framed from the chest up with space above his head, his eyes heavy and tired, his right hand raised at chest height with a little snow-white sugar on the tips of his fingers, his face three-quarter to screen left, never the lens; weary and quietly glad: lips pressed shut; low warm morning light on his face; behind him the plaster wall, soft",
         lines=[("xitong", "叮。白糖試做，成功。", "冷，宣布")],
         panel=[("白糖試做，成功", "task")],
         motion=f"Xu Yan rubs the snow-white sugar between his fingertips, lets out a long breath, and a slow closed-lipped smile spreads across his face; {SILENT_HE}; he is listening, not speaking",
         zh="近景、慢推（送清晨糖坊裁切；拍法 11 不寫藍光）：許硯熬了一夜的臉，搓一搓指尖的白糖、吐一口氣、慢慢抿嘴笑開；全程嘴閉著（系統畫外，面板由剪接疊上）"),
    dict(loc="shed_d", cam="Wide shot, slow push in", chars=["xuyan", "erniu"], night="shed_d",
         comp=f"wide shot down the shed in low warm morning light: in the left foreground {ERNIU}, standing by the cold stove, framed full figure, one empty hemp sack hanging from his left hand, his face three-quarter to screen right toward Xu Yan, never the lens; listening: lips pressed shut; beyond him on the right of him at the low bench along the left wall {XU_C}, framed full figure, already holding {BOWL} in both hands from the first frame, the brown clay funnels on the bench beside him, his face three-quarter to screen left toward Wang Erniu, never the lens; steady, not smiling: lips moving between words; {HANDS}; exactly two people",
         lines=[("xuyan", "十斤紅糖只出一碗，要拿去賣，得有幾百斤才行。", "很穩")],
         motion=f"Xu Yan lifts the bowl a little and looks down into it as he speaks; {quiet('Wang Erniu')}; Erniu nods slowly",
         zh="全景、慢推（送清晨的糖坊圖 `set-tangfang-l1`）：左前二牛站在熄了的灶邊、手提空麻袋、嘴閉著；左牆矮凳邊許硯第一格已經捧著一碗白糖（約一斤，拍法 28 寫法），舉一下、低頭看，很穩地說，不笑。稿子『刮完最後一個糖錐』不拍（一鏡一個動作，刮糖交給音效）"),
    dict(loc="shed_d", cam="Medium shot, slow push in", chars=["erniu", "xuyan"], night="shed_d",
         comp=f"medium shot in low warm morning light: on the left {ERNIU}, framed from the waist up, one empty hemp sack already slung over his left shoulder from the first frame, his right arm pointing out to the right toward the open side of the shed, his face three-quarter to screen right toward Xu Yan, never the lens; eager: brows up, lips moving between words; on the right {XU_C}, framed from the waist up, {BOWL} held in both hands at his chest, his face three-quarter to screen left toward Wang Erniu, never the lens; firm: lips moving between words when it is his turn; behind them the plaster wall and the brown clay funnels, soft; {HANDS}; exactly two people",
         lines=[("erniu", "我去鄰鎮收紅糖，你進城叫小棠去糖行全訂下來！", ""),
                ("xuyan", "好，分兩頭收，一斤都別漏掉。", "點頭")],
         motion="Wang Erniu speaks first, pointing out of the shed, then lowers his arm; Xu Yan nods once and answers him",
         zh="中景、慢推（送清晨的糖坊圖；買 8 秒，見 BUY）：左邊二牛麻袋第一格已經在肩上、往畫右棚外一指說；右邊許硯捧著那碗白糖，點頭回他（兩人一前一後說話）（結尾）。稿子『把空麻袋甩上肩』不拍（第一格已經在肩上），甩袋交給音效"),
    # ---- scene 3: the third morning, the county street at the Xu shop (the same pictures as scene 1).
    dict(chapter="許記門口", loc="street", cam="Wide shot, slow push in", chars=["xuyan"], night="street",
         comp=f"wide shot down the street: in the left foreground {XU_N}, standing at {COUNTER_ST}, framed from the knees up, {BOWL} already set down in the middle of the counter in front of him from the first frame, his face turned down to the bowl, never the lens; pleased and hopeful: a small smile, lips pressed shut; far across the street on the right at the open doorway under the red silk one ox cart piled with plain hemp sacks, and two men in grey cotton short jackets and cloth head wraps carrying sacks inside on their shoulders, small, side-on; {HANDS}; exactly three people: Xu Yan and the two men across the street",
         lines=[("xuyan", "一碗白糖擺在這裡，等紅糖一到，就能熬第二鍋。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan takes one step back from the counter and looks at the bowl, pleased; {SILENT_HE}; across the street behind him the two men carry the sacks in through the doorway one after the other",
         zh="全景、慢推（送大街圖；第三日早上）：左前許硯站在許記門前的長櫃邊，那碗白糖第一格已經擺在櫃上正中，他退一步看、抿嘴微笑、嘴閉著（心裡話畫外）；對街紅綢下的大門前一輛堆滿麻袋的牛車、兩個灰短打的家丁扛袋子進門（側面、小）。稿子的三輛牛車改一輛（拍法 26 的做法：三頭牛同框容易畫壞，其餘的車聲交給音效）、家丁六人改兩人（拍法 25）"),
    dict(loc="street_x", cam="Medium shot from behind, tracking shot that follows the subject", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="street",
         comp=f"medium shot from close behind {TBACK}, framed from the waist up, already arriving at a run at the open front of the Xu shop from the first frame, her right hand already gripping the edge of the folded-back plank door, her left hand holding up her skirt; {only_tang()}; ahead of her the pale plank door and the dark doorway; {HANDS}",
         lines=[("tangxiaotang", "糖行說，全州的紅糖，昨天一夜被人買光了！", "喘著氣，不笑")],
         motion=f"the young woman stops hard at the door and hangs on to the plank door, her shoulders heaving as she pants; {HEADSTILL}",
         zh="中景（從背後）、跟拍（送許記門面裁切）：唐小棠的背影第一格已經跑到許記門口，一手抓住折起的門板、一手提著裙襬，肩膀一起一伏地喘，喘著說（nospeak；臉發白、不笑交給錄音，原版建議 s27）"),
    dict(loc="street_x", cam="Close-up, slow push in", chars=["xuyan"], night="street",
         comp=f"close-up from the street side of {XU_N}, standing at the counter by the folded-back plank door, framed from the chest up with space above his head, his face three-quarter to screen right toward her off screen right, never the lens; stunned, not smiling: eyes wide, brows up, lips moving between words; behind him the pale plank door and the dark doorway, soft",
         lines=[("xuyan", "全州？我們昨天訂的三百斤呢，也沒了？", "愣住")],
         motion="Xu Yan's hand draws back from the bowl below the frame as he speaks, his eyes fixed on her; after the last word he waits, stunned",
         zh="近景、慢推（送許記門面裁切）：許硯愣住，手從畫面下緣外的陶碗上收回來，朝畫右的唐小棠（畫外）問，不笑"),
    dict(loc="street_x", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="street",
         comp=back(f"her right hand already holding out {POUCH} toward him from the first frame; facing us beyond her, a little left of the middle, {XU_N}, standing at the counter by the folded-back plank door, framed from the waist up, his face three-quarter to screen right toward her, never the lens; stunned: brows up, lips pressed shut; behind him the dark doorway, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
                   "standing at the front of the Xu shop"),
         lines=[("tangxiaotang", "沒了。訂金退回來了，一車一車全拉進了魏記。", "")],
         motion=f"the young woman presses the pouch into Xu Yan's hand and his fingers close round it; {HEADSTILL}; {quiet('Xu Yan')}",
         zh="過肩中景、慢推（送許記門面裁切）：前景右唐小棠的背影把一個小灰布包（退回的訂金）塞進許硯手裡（nospeak）；許硯愣著、嘴閉著。稿子『近景下巴以上、回頭往對街看』改背影、不回頭（回頭會露臉）"),
    dict(loc="street_w", cam="Point-of-view wide shot, slow push in", chars=[], night="street",
         comp=f"point-of-view wide shot looking across the street from the Xu shop: the soft rim of {BOWL.replace('one shallow', 'a shallow')} at the very bottom edge of the frame, out of focus; across the street the shop with the red silk, its two tall plank doors standing half open, two men in grey cotton short jackets and cloth head wraps at the doors, seen from behind; {HANDS}; exactly two people",
         motion=NOBODY + "the two men push the two tall plank doors shut from outside, one on each side, and the doorway under the red silk closes",
         zh="主觀全景（許硯看對街）、慢推（送對街魏記門面裁切；前景下緣虛焦是白糖碗的碗沿）：對街兩個灰衣家丁（背影）把兩扇大門推上闔起（無台詞）。稿子『最後一輛牛車駛進大門、門閂落下』只拍闔門（一鏡一個動作），牛車與門閂交給音效"),
    dict(loc="street_x", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="street",
         comp=back(f"her right hand already holding his left sleeve from the first frame; facing us beyond her, a little left of the middle, {XU_N}, standing at the counter, framed from the waist up, {POUCH} in his right hand, his face three-quarter to screen right toward her, never the lens; grim, not smiling: jaw set, lips pressed shut; behind him the dark doorway, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
                   "standing at the front of the Xu shop"),
         lines=[("tangxiaotang", "他買光紅糖，不是要賣，是不讓我們熬。", "咬唇")],
         motion=f"the young woman tugs his sleeve once, hard; {HEADSTILL}; {quiet('Xu Yan')}; his eyes go to the shop across the street",
         zh="過肩中景、慢推（送許記門面裁切）：前景右唐小棠的背影抓著許硯的袖子用力扯一下（nospeak；咬唇交給錄音）；許硯拿著訂金小布包、不笑、嘴閉著"),
    dict(loc="street_x", cam="Medium close-up, slow push in", chars=["xuyan"], night="street",
         comp=f"medium close-up from the street side of {XU_N}, standing at the counter by the folded-back plank door, framed from the chest up with space above his head, already holding {BOWL} in both hands at his chest from the first frame, his face three-quarter to screen right and tilted up toward the upper floor of the shop across the street, never the lens; grave, not smiling: brows drawn, lips moving low between words; at the left edge of the frame, soft and cut off, the back of a young woman's head with two round buns set high, a short pink silk ribbon around each, appearing only once; behind him the pale plank door, soft; {HANDS}",
         lines=[("xuyan", "二牛去了鄰鎮，鄰鎮的糖行，總不會也被買光吧？", "壓低聲音，不笑")],
         motion="Xu Yan lifts his eyes slowly to the upper floor across the street as he speaks, low; after the last word he holds the bowl still",
         zh="中近景、慢推（送許記門面裁切）：許硯第一格已經捧著那碗白糖，慢慢抬眼看畫右上方對街二樓，壓低聲音問，不笑；畫左緣虛焦是唐小棠的兩顆丸子（不點名、不送圖）。稿子『把小布包交還唐小棠、捧起陶碗』不拍（一鏡一個動作），布包交還交給剪接"),
    dict(loc="street_up", cam="Low-angle medium shot, slow push in", chars=["weishaoqing"], night="street",
         comp=f"low-angle medium shot from the street below of {WEI}, leaning his forearms on the sill of one dark lattice window swung open on the upper floor, framed from the chest up, {FAN}, his face three-quarter to screen left looking down toward the Xu shop below, never the lens; coldly pleased: a thin curl at one corner of his mouth, eyes cold, lips moving slowly between words; behind him the dim room inside the window; around the window the dark lattice and the plain boards under the grey-tiled eaves",
         lines=[("weishaoqing", "全州的糖，包括鄰鎮。沒糖，看你熬什麼。", "搖扇，慢慢地")],
         motion="Wei Shaoqing taps the closed fan once on the window sill as he speaks slowly, a cold smile; after the last word he keeps looking down, smiling",
         zh="仰角中景、慢推（送對街二樓裁切）：魏少卿倚在窗台上往畫左下的許硯看，合著的摺扇在窗台上敲一下，薄唇一勾、慢慢地冷笑著說（本鏡可以笑；扇子合著，稿子的『搧一下扇子』改敲窗台）（結尾；懸念交給第 25 集）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e024-r2/script.md`（c01–c36 對應 s01–s36；c15 拆成 s15、s15b，共 37 鏡；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-16）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e021-e030.md`（拍法 1–30 條）。第 3 篇章〈搶親〉第四集。",
    "- 內部工作編號 924（`hailuo/{ff,clips}-dh-e924.json`、`colab/runs/e924/extras.json`、`colab/runs/e924-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e924-dh/`）；發布 slug `zhong-tian-qu-qi-e024-r2`。不放集數、不放片名卡；s01 接第 23 集 s40 的隔天早上（聖經接點 23→24：縣城大街 `set-xianjie-l1`，對街魏記夥計敲鑼「肥皂，五文一塊」，許硯、唐小棠剛卸下門板，許記在左、魏記在右）；s36 交給第 25 集（接點 24→25：對街二樓魏少卿「沒糖，看你熬什麼」）。",
    "- 照第 23 集審稿後的寫法一開始就照做：`OFFSCREEN_SPEECH = False`；`quiet()` 只管嘴；背景寫在場的東西（拍法 18）；道具與接觸寫在第一格；只寫要畫出來的東西：會員木牌寫素面小木牌（不刻梅花紋）、退回的訂金寫一個小灰布包、糖照拍法 28；魏記夥計、客人、家丁不點名、不送圖。",
    "- **唐小棠不露嘴說話、本集也不露臉**（拍法 3）：她的台詞全部從背後拍（s04、s07、s12 鋪子裡；s09、s17、s30、s32、s34 街上；nospeak，spec 拿掉她的圖與身分句；兩顆高丸子、短粉緞帶、後頸露出、頭不動）；s01 抱門板的背影不點名；s10、s13 只拍手；s35 畫左緣虛焦的丸子不點名。**算盤只在 s08 一支插鏡**（拍法 20：道具圖本身就是放在鋪子深色櫃面上的長金算盤，她一掌按下；她的台詞畫外）；c04 撥算珠、c12 算珠響成一串交給音效。",
    "- **魏少卿的摺扇整集合著**（第 21 集 fix1）：c06、c36 的搧扇改成合著的扇子敲窗台；可以笑（拍法 30）。",
    "- **場景圖說了算**（拍法 29，協調者 2026-11-16 決定，每張放大看過）：縣城大街 `set-xianjie-l1`（許記在左、對街魏記在右、紅綢已掛、晴天藍天、沒有霜）；許記鋪子 `set-xuji-pu-l1`（架子在左、門在後牆正中、櫃檯寫在右牆）；糖坊夜 `set-tangfang-ye-l1`、清晨 `set-tangfang-l1`（灶在左前、漏斗在左牆、開口在右：二牛在灶邊畫左、許硯在他畫右）。免費裁切六張（新 id、自帶 l1，見 `refs-live/README.md`）：許記門面 `set-xianjie-xuji-l1`、對街魏記門面 `set-xianjie-weiji-l1`、對街二樓 `set-xianjie-lou-l1`、門前長櫃與石板 `set-xianjie-shi-l1`、夜裡糖坊 `set-tangfang-ye-jia-l1`、清晨糖坊 `set-tangfang-jia-l1`。插鏡：鋪子櫃面 `set-xuji-pu-cabinet-l1`、算盤 `prop-jinsuanpan-l1`。**不需要試鏡**。",
    "- 長鏡要買的秒數（BUY）：照 35 句錄音核過（見 `r2.py` 的 BUY 註解）：**稿子 c15 的長鏡（心裡話＋兌換＋系統吐槽＋心裡話，約 11 秒）拆成 s15 與 s15b**；s06（a05 人聲 6.65 秒）、s15b（a15＋a16 共 6.18 秒，6 秒只剩 0.09 秒）、s19（a20 人聲 6.64 秒）、s28（兩人兩句共 7.0 秒，稿子的長鏡清單也買 8）、s36（本集最後一鏡，要留重音與懸念的尾，同第 23 集 s40）買 8 秒；插鏡 s08、s13、s16 與無台詞的 s21、s24、s33 5 秒；其餘 6 秒。沒有超過約 10 秒的鏡，不再拆。重錄 a18、a21、a34（第一次的檔在 `audio/take1/`）。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音長度＋0.5 秒為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯（l1、angle-a；帶笑的 angle-b 整集不送）、王二牛（l1、angle-a；gen-dh 只送這兩張）、魏少卿 l1。唐小棠整集不送圖。魏記夥計、客人、家丁、手都不送圖。場景見上面。",
    "- 共用檔：程式都沒改（說話的人除了魏記夥計都在 `build-r2.py` 的 `EN`；夥計從不列在 chars，聲音放 `MINOR`（Alnilam，聖經〈小角色〉）；地方都用 `gen-dh.mjs` 已有的 SET 句；`pilot.py`、`cast.json` 不動）；`refs-live` 加六張免費裁切（新 id）與 README 一段。精修文字的 CG 立領句由本檔結尾的 `live_clips()` 在 build 後從 `clips-dh-e924.json` 拿掉（第 22、23 集的做法）。",
    "- `colab/runs/e924/extras.json`（照第 23 集）與 `colab/runs/e924-live/spec.json`（`mkspec.py` 產生；種子 9241101／9241102）。",
    "- 免費準備：scratchpad `prep924.sh`（`DRY=1 … st1-ep.sh 924` → `pilot.py` → `retake.py` → `colab-jobs.json` 加 output_path、套 swap_pictures（絕對路徑）→ 逐鏡查送的場景圖與人物圖 → 精修用的分隔句 → `preflight-prompts.py` → 否定名詞與會長字的名詞掃描）。",
    "- 配樂：大街熱鬧的街市 cue，s02 人跑掉時抽成單音，s08「不降」重音，s15 兌換電子重音；糖坊夜裡低的木管加柴火聲，s24 起亮的弦樂，s26「叮」輕重音；許記門口亮的弦樂，s30 起低沉 suspense，s36 大重音後收。音效見 script.md〈音樂與音效〉（另外：s01 紅綢揭下、s04 算珠、s05 門板靠牆、s09 抱盆走出、s12 算盤響成一串、s27 刮糖、s28 麻袋甩上肩、s29 牛車與其餘兩輛的車聲、s33 門閂、s35 布包交還，都交給音效）。",
]

# Long shots: seconds to buy. Measured 2026-11-16 against the 35 recordings (~/mokaair-work/videos/zhong-tian-qu-qi-e924-dh/audio;
# wave length and silencedetect -35 dB speech span; e013's test: a shot holds (buy - 0.3) x 1.1 s of speech, half a second
# between lines, so 5 s holds 5.17 s, 6 s 6.27 s, 8 s 8.47 s). faster-whisper medium read every take back, one clip per process,
# numpy input, once plain and once with the previous line and the line as context (audio/fw924.txt; audio/README-retakes.txt).
# 8 s: s06 (a05, Wei Shaoqing's drawl: 6.65 s of speech with a 0.55 s pause, over 6.27 s);
#      s15b (a15 2.60 + 0.5 + a16 3.08 = 6.18 s: a 6 s clip leaves 0.09 s);
#      s19 (a20 6.64 s of speech from its first frame);
#      s28 (a27 4.15 + 0.5 + a28 2.34 = 7.0 s, two speakers; the script's long-shot list buys 8 too);
#      s36 (a35 5.16 s fits 6 s, but it is the episode's last shot: the accent and the hook need a held tail, as e923 s40).
# 6 s: every other speaking shot. The tightest: s22 (a22 5.69 s, a face shot), s05 (a04 5.46 s), s04 (a03 4.78 s, a back
#      shot: 1.5 s spare for a trimmed head), s32 (a32 4.57 s, a back shot), s15 (a13 2.86 + 0.5 + a14 1.09 = 4.45 s).
# 5 s: the inserts with an off-screen line hold it: s08 (a07 4.28 s), s13 (a11 1.96 s), s16 (a17 3.59 s).
# No shot runs over about 10 s after the c15 split, so nothing more is split.
# Re-recorded once (first takes in audio/take1/): a18 (拿它 heard 哪怕), a21 (變成白糖 lost by both passes), a34 (二牛 heard 而你又);
# the retakes are kept: a18 4.24 s (speech 3.61), a21 5.32 s (4.66), a34 4.96 s (4.47), all inside 6 s.
BUY = {"s06": 8, "s15b": 8, "s19": 8, "s28": 8, "s36": 8}


# ---- the refine text (e022 review 必改 12, as e023): hailuo/clips-dh-e924.json column 0 is the motion text refine-prep.py sends
# with a picked d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era "Tang Xiaotang's high stand-up
# collar stays closed at her throat." and names her in "<names> shown in <Picture 1>"; in a back shot that draws the collar back
# and turns her face to the lens. Every shot of her here is a back shot: the sentence goes and her name becomes "the young
# woman seen only from behind". Column 1 is recomputed.
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
