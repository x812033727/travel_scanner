"""Episode 20 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e020-r2/script.md
(c01-c38 = s01-s38, c37b = s37b; the CG-era r2 script of PR #2024), including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」
and 「真人版的改動（2026-11-16）」, which override the tables. Every line is the script's, word for word; only the staging changes.
Bible: production/r2-bible-e011-e020.md (rules 1-18). The last episode of arc 2; e021-r2 c01 continues s38 at the same moment.

Live action from the first draft, written the way e019-r2/r2.py stands AFTER its independent review (review.md in ../e019-r2)
and with the e917-e919 picking lessons (colab/runs/e91{7,8}-live/picks-merged.tsv, e918-live/fix1, fix2; refs-live/README.md):
- OFFSCREEN_SPEECH = False (bible rule 15): every shot with an off-screen line, a thought or a system line writes the silence
  of each person on screen (quiet(), SILENT_HE), after the action.
- Bible rule 18: nothing is negated by name; backgrounds say what is there. Paper is never read: the bundles of paper are
  "plain white paper tied with a paper cord, blank on every side"; the guild master's ledgers stay closed, plain dark blue
  covers (s23: the script's opened page becomes his palm pressed on the closed stack). The signboard is never in the frame
  (s04: the top edge of the frame stops below it; the red cloth falls out of the top). The carriage lanterns (s15) are
  plain red silk with a thin gold rim; the eave lantern (s34, s36, s38) is one plain white paper lantern, written the same
  way every time (EAVE). Wei Shaoqing's fan is plain cream paper flecked with gold dots, "nothing else on it".
- Hands and props in the first frame, each in its owner's named hand; contact is a state (s34 Sun Zhanggui's palm is already
  on the shutter board). No pointing finger: Xiaohe shows the way with an open hand (s05), Qin Shuang's order is a flat open
  hand swept toward the street (s10), Sun Zhanggui's open palm (s36).
- Tang Xiaotang never speaks on camera (bible rule 3): all ten of her on-screen lines (s02, s06, s08, s14, s18, s22, s24,
  s25, s28, s32) are said from behind her (TBACK, nospeak; spec.json drops her three face pictures and her identity
  sentence), one fixed gaze per shot, her head held still. The counter shots look from behind her across the counter at
  the person she talks to (the customers s06, A-ling s18, the guild master s22, Xu Yan s24, s31, s32); s25 is her back with
  Xiaohe clapping beside her. Her one silent face is s37b (e907's neutral face sentences; colour drained, lips pressed).
  s16 and s37 are her hand only. Costume: the live portrait l1, cross-collared and closed, no outer coat (bible rule 4; the
  script's t2 high collar, "下巴以上" and the apricot outer coat are not used; s03's "pulls her slipping coat straight"
  becomes a light pat on her shoulder).
- The small gold abacus (bible 道具表: the one at her waist in the CG cast; the live portrait has only a gold knot ornament
  there, so it has NO picture): one fixed sentence everywhere (ABACUS). It falls twice (s16, s37) and is hugged at the end
  (s37b, e021 c01). The e917 lesson (the lantern frame came out in five shapes; prop pictures before props): a one-change
  Qwen prop picture prop-jinsuanpan-l1 (live-action/screen-test-e020.py, seeds 37031/37032, NOT run here) goes into the
  two inserts' set slot once picked; until then the inserts send the free floor crop set-xuji-pu-floor-l1 and stay in
  colab-jobs-wait.json (prep920.sh).
- No weapon: Qin Shuang's belt is empty (extras.json; the script's knife at her belt is not written, rule 5); the six young
  men are empty-handed; nobody official is in the episode. Crowds are Song-dynasty townspeople with their hands written
  (CROWD), counted, mostly backs.
- No more than three named faces (rule 1): s29 Erniu, Qin Shuang, Xiaohe; s38 (the script's six) is Wei Shaoqing and Sun
  Zhanggui with Xu Yan's unnamed back in the foreground; Tang Xiaotang, Erniu and Qin Shuang stay off screen in it (e021
  c01 shows them). Over-the-shoulder foregrounds are unnamed and get no picture (rule 2): the guild master in s20, Sun
  Zhanggui in s35, Xu Yan in s38.
- Smiles only where the script allows them (each marked in a comment): s03 Xu Yan, s04 Erniu, s05 Xiaohe, s09 his flustered
  grin, s11 Erniu, s12 Xu Yan, s13 Qin Shuang's mouth corner, s19 the guild master's fawning smile, s24 Xu Yan's mouth
  corners, s25 Xiaohe, s34/s36 Sun Zhanggui's thin smile, s38 Wei Shaoqing. Every other face is written as a set expression.
- Nobody is flipped in the edit: every speaker wears a cross or round collar; sides are written as screen left/right.
State at the junction (e019 s41): the roof at night, Tang Xiaotang's back in the right foreground hugging her knees, chin on
them; Xu Yan facing us an arm's length beyond her, a little left of the middle, in his old grey outer coat, his head turned
to her. s01 is his close-up answering; s02 and s03 are e019 s39/s41's over-the-shoulder again.
Places (the coordinator's decisions, 2026-11-16; listed again in script.md 〈真人版的改動〉; every picture looked at full size):
- The roof (s01-s03): no roof picture (spec drop_set), the dark tiles and the black night sky in words: e019's review 必改
  15 kept the 3D roof picture out of the closer shots (e019 s39-s41), and all three are close.
- The shop set-xuji-pu-l1 (gen-dh "Xu family shop"; the owner's pick 37003): the empty shop as the picture has it: tall
  dark shelves over a long low cabinet along the LEFT wall, the wide front doorway in the middle of the BACK wall between
  lattice panels with the street beyond, plain white panelled walls on the RIGHT, grey stone tiles, bars of sunlight from the
  doorway. The script's layout (counter left, shelves right, door in front) is turned to the picture's: the long dark
  counter is written along the right wall (not in the picture), the shelves are the picture's left-wall shelves, the
  street door is at the back; the back door to the yard (s33) is a plain door in the far right corner. The sunlight bars
  serve every hour: morning cold, afternoon warm, evening low orange, dusk "the last low orange sunlight in thin bars" with
  the street turning blue (the picture's bright light is graded down in the cut).
- Outside (s04 the red cloth, s11 the queue): no picture (spec drop_set). The
  street picture set-shiji-l1 is a vegetable market with false glyphs on two signboards and on hanging plaques; the shop
  picture is the inside. The street is written: grey-tiled wooden shop fronts, frosty flagstones. s15 (the carriage seen
  from behind the counter) sends the shop picture: its doorway, three bright openings between dark posts, is that view.
- The inserts s16, s37: a NEW free crop set-xuji-pu-floor-l1 (refs-live/README.md, last paragraph) until the prop picture
  is picked (above).
- The guild master (live portrait hanghui-huizhang-portrait-l1, the e011-e020 screen test's 37001): a MINOR role here
  (cast.json has no entry; voice Fenrir, unused in arcs 1-2); extras.json gives him the portrait through extras_patch.py
  with the placeholder stem mianshiguan-portrait-t1 (pilot.py's live lookup takes a one-word id only), and spec.json
  swap_pictures puts hanghui-huizhang-portrait-l1 in its place (prep920.sh, absolute paths).
- Shared files: build-r2.py's EN gets "weishaoqing" and "hanghui" (the bible's list; both speak on screen); gen-dh.mjs,
  pilot.py and cast.json are NOT changed.
"""
EP = 920  # internal working number; the published slug is zhong-tian-qu-qi-e020-r2
SLUG = "zhong-tian-qu-qi-e020-r2"
EP_TITLE = "許記開張，宰相之子登門（重製版 r2）"
OUTLINE_SECONDS = 204  # script.md: 203.5 s, 39 shots (3 + 21 + 15)
TARGET_MINUTES = [3, 4]
TITLE = "我的未婚妻，在你家？｜種田娶妻打天下 第20集（重製版）"
DESCRIPTION = "屋頂上，唐小棠問他：若有人來帶我走，你會讓嗎？許硯說：誰來都一樣，先過我這關。六天後，縣城綢緞莊隔壁，許記開張：二十刀白紙、一百塊肥皂，門口擠得紙都掉在地上，秦霜叫二牛帶著練過棍的年輕人在門外排出整齊的長隊。午後一輛掛紅燈籠的黑漆馬車經過門口，唐小棠的金算盤啪地掉在地上，她說是看錯了。前幾天封殺許家的書坊行會會長親自上門求貨，唐小棠一刀加三成。傍晚全部賣空，系統宣布天下歸心百分之一。打烊前孫掌櫃按住門板：有貴客要見你。一個搖著灑金摺扇的公子跨進門：我的未婚妻，在你家？《種田娶妻打天下》第 20 集（重製版）。"
THUMB = ("我的未婚妻，在你家？", "s38")
CHARACTERS = ["xuyan", "tangxiaotang", "qinshuang", "aling", "xiaohe", "erniu", "hanghui", "sunzhanggui", "weishaoqing", "xitong"]
MINOR = {
    "hanghui": {"id": "hanghui", "name": "行會會長",
                "appearance": "East Asian man of about forty-five, thin and small, a narrow face, a thin drooping moustache and a small goatee, an ancient Chinese Song-dynasty guild master's plain grey round-collared silk gown with a white inner collar, a black gauze band round his brow below a small topknot with a thin black hairpin, cloth shoes",
                "voice": {"provider": "gemini", "name": "Fenrir", "style": "標準國語，咬字清楚，台北人平常說話的語調；四十五歲的書坊行會會長，男聲、瘦小、陪著笑、說話有點油、句尾帶乾笑，被壓價時咬著牙"}},
}
MUSIC = "one cue per scene: a quiet night cue of solo guqin on a moonlit roof with one warm accent; then a lively market cue of gongs, drums and bamboo flute for a shop opening, a cold low note and two beats of silence as a carriage passes, then a playful plucked rhythm while a price is haggled, one accent on an abacus bead; then a warm relaxed closing-time cue that gives way to low held strings at dusk, one big accent on a fan snapping open; ancient Chinese rural drama, no vocals"

# Scene 1: the roof at night, no picture (drop_set). Scenes 2-3: the shop (set-xuji-pu-l1); outside and the inserts drop or
# swap it (spec.json). gen-dh SET takes the FIRST pattern in its list order that the whole prompt matches: the shop prompts
# say "Xu family shop" and never "academy", "town square", "city gate", "alley", "teahouse", "tavern", "clinic" or "city
# street" (gen-dh's modern words); the roof prompts say "roof of the farmhouse" and never "Xu family shop" or "yard".
SHOP = ("tall dark wooden shelves along the left wall above a long low dark wooden cabinet, the wide open front doorway in the "
        "middle of the back wall between dark wooden lattice panels with the county town street beyond it, plain white "
        "panelled walls on the right with one long plain dark wooden counter standing in front of them, a floor of large grey "
        "stone tiles and dark wooden beams overhead")
SHELF_FULL = "the upper shelves stacked with bundles of plain blank white paper tied with paper cord and the lower shelves with neat rows of pale cream soap bars"
SHELF_LOW = "the shelves mostly bare, three bundles of blank white paper and a short row of pale soap bars left on them"
SHELF_EMPTY = "the shelves standing completely bare"
STREET = ("on a county town street on an early-winter morning: a row of old grey-tiled wooden shop fronts with plain dark wooden "
          "boards, the street paved with grey flagstones under a thin white frost, cold bright sunlight slanting from the right, "
          "breath showing white in the cold air")
EAVE = "one round plain blank white paper lantern glowing under the eave outside the doorway"
LOC = {
    "roof_c": "On the roof of the farmhouse in the middle of the night, dark grey tiles and the black night sky, cold white moonlight from beyond the upper right",
    "street": f"Outside the Xu family shop {STREET}",
    "door": "In the Xu family shop in the county town on an early-winter afternoon",
    "am": f"In the Xu family shop in the county town on an early-winter morning: {SHOP}; {SHELF_FULL}; cold bright morning sunlight slanting in through the front doorway in long bars across the grey floor",
    "am_c": "In the Xu family shop in the county town on an early-winter morning, dark wooden shelves and the bright front doorway soft behind, cold bright morning sunlight",
    "pm": f"In the Xu family shop in the county town on an early-winter afternoon: {SHOP}; {SHELF_LOW}; warm afternoon sunlight slanting in through the front doorway in long bars across the grey floor",
    "pm_c": "In the Xu family shop in the county town on an early-winter afternoon, dark wooden shelves and the bright front doorway soft behind, warm afternoon sunlight",
    "eve": f"In the Xu family shop in the county town in the early-winter evening: {SHOP}; {SHELF_EMPTY}; low warm orange evening sunlight slanting in through the front doorway in long bars across the grey floor",
    "eve_c": "In the Xu family shop in the county town in the early-winter evening, the bare dark shelves soft behind, low warm orange evening sunlight",
    "dusk": f"In the Xu family shop in the county town at dusk: {SHOP}; {SHELF_EMPTY}; the last low orange sunlight in thin bars across the grey floor, the street beyond the doorway turning deep blue with dusk, {EAVE}",
    "dusk_c": f"In the Xu family shop in the county town at dusk, the shop dim, the last low orange sunlight, the street beyond the doorway deep blue",
    "insert": "In the Xu family shop in the county town, on the grey stone floor",
}
LIGHT = {
    "roof": "the cold moonlight and the deep night stay unchanged",
    "street": "the cold morning sunlight stays unchanged",
    "am": "the cold morning sunlight stays unchanged",
    "pm": "the warm afternoon sunlight stays unchanged",
    "eve": "the low orange evening sunlight stays unchanged",
    "dusk": "the last low sunlight and the blue dusk stay unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow"
XU_COAT = "Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe"
QIN = ("her dark brown cross-collared short jacket, wide plain leather belt with nothing tucked in it and nothing hanging from it, "
       "black trousers, leather boots and high ponytail tied with black cord")
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
ALING = "in her plain grey-white cotton dress with long sleeves covering her wrists, her black hair in a high bun with one plain wooden hairpin"
XIAOHE = ("little Xiaohe, in her patched lilac cotton jacket, her two little pigtails tied with red string, one small woven straw "
          "rabbit tucked in her sash")
ERNIU = "Wang Erniu, in his coarse brown hemp short jacket with the sleeves rolled up"
SUN = "Sun Zhanggui, in his green satin robe with a jade belt hook"
WEI = "Wei Shaoqing, in his sapphire-blue brocade robe woven with gold thread and a small jade crown on his topknot"
GUILD = "the guild master, in his plain grey round-collared silk gown and the black gauze band round his brow"
LEDGERS = "a stack of three thread-bound ledgers with plain dark blue cloth covers, closed"
# e916 fix1 / e918 review 必改 1 / e919 review 建議 (no pearl pins): two high round buns, a short ribbon round each, the nape bare.
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with all of her black hair gathered "
         "up into two round buns set high on her head, a short pink silk ribbon wrapped around each bun, the "
         "nape of her neck bare above a pink inner collar, and her light peach-pink silk shoulders; the back of her "
         "head toward us the whole time, her ear the furthest round her head we ever see")
HEADSTILL = "the young woman with the two high round buns keeps her head still, the back of her head toward us the whole shot"
# The one gold abacus (bible 道具表; no picture until prop-jinsuanpan-l1 is picked).
ABACUS = ("one small gold abacus the size of her palm (a thin flat gold frame and five rows of small round gold beads on thin "
          "gold rods)")
PAPER = "one thick bundle of plain white paper tied with a paper cord, blank on every side"
SOAP = "one pale cream bar of soap the size of a palm, plain and smooth"
BOX = "one small plain pale wooden box the size of two hands with a hinged lid"
BOARD = "one long plain wooden shutter board as tall as a man"
FAN = "one open folding fan of plain cream paper flecked with tiny gold dots, nothing else on it"
CROWD = ("townspeople in Song-dynasty clothes: women in plain cotton cross-collared jackets and long skirts, men in plain hemp "
         "cross-collared short jackets and cloth head wraps, all in cloth shoes, their hands holding only small bamboo baskets or "
         "nothing")
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return (f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, "
            f"no mouthing words, the face set and still")


def only_tang(side):
    """e915 s26/s41: a second Tang appeared beside her back. One person with buns, one fixed side."""
    return (f"she is the only young woman in the frame and the only one with two high round buns, and she stays in the {side} "
            f"foreground from the first frame to the last")


def counter_back(rest):
    """Tang Xiaotang behind the counter, seen from behind (bible rule 3): the camera behind her looks across the counter."""
    return (f"over-the-shoulder medium shot from close behind {TBACK}, standing behind the long dark wooden counter in the right "
            f"foreground, framed from the waist up, facing across the counter; {only_tang('right')}; {rest}")


SHOTS = [
    # ---- scene 1: the roof, day 15 at night, the same moment as e019 s41 (no roof picture: drop_set). Tang Xiaotang on the
    # right hugging her knees, Xu Yan an arm's length to her left facing right.
    dict(chapter="屋頂", loc="roof_c", cam="Close-up, slow push in", chars=["xuyan"], night="roof",
         comp=f"close-up of {XU_COAT}, sitting on the tiles, framed from the chest up with space above his head, his face three-quarter to screen right toward the young woman beyond the right edge of the frame, never the lens; certain and steady: brows level, eyes warm and firm, lips moving evenly between words; behind him only the dark tiles and the black night sky",
         lines=[("xuyan", "誰來都一樣，先過我這關。", "篤定")],
         motion="Xu Yan lifts his right hand from the tiles beside him, rests it on his knee and sits up straight, his eyes on her, then speaks; after the last word he keeps his eyes on her",
         zh="近景、慢推（不送屋頂圖：第 19 集審稿必改 15，屋頂近鏡不帶 3D 圖）：許硯（披舊灰外衣）坐在瓦上，撐在瓦上的右手收回放在膝上、坐直，看著畫右的唐小棠（畫外）篤定地說；說完眼睛不離開她（接第 19 集 s41 同一刻）"),
    # Her muffled line from behind her (bible rule 3), e019 s39/s41's over-the-shoulder: chin on her knees all the shot.
    dict(loc="roof_c", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="roof",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, sitting on the tiles in the right foreground hugging her knees, her chin resting on her knees from the first frame to the last; {only_tang('right')}; facing us an arm's length away a little left of the middle, {XU_COAT}, sitting on the tiles, framed from the waist up with clear space above his head, his face three-quarter to screen right toward her, never the lens; tender and serious: brows lifting a little, eyes on her, lips closed; behind him only the dark tiles and the black night sky; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "這是你說的，我記著了，不許反悔。", "悶悶的")],
         motion=f"the young woman presses her chin down onto her knees and hugs them tighter; {HEADSTILL}; she looks straight ahead at the young man the whole shot; {quiet('Xu Yan')}; his eyes soften",
         zh="【改背後拍】過肩中景、慢推（不送屋頂圖）：前景右唐小棠的背影（兩顆高丸子、短粉緞帶、後頸露出）抱膝，下巴從第一格到最後一格擱在膝上，把膝蓋抱緊（原稿『抬起眼睛看他』與主觀近景不拍：一抬頭就露臉）；對面一臂外許硯看著她、嘴閉著、眼神放軟。台詞 nospeak，剪接放錄音"),
    # He may smile a little here (script). The script's "pulls her slipping outer coat straight" (she has no outer coat in the
    # live costume, bible rule 4) becomes his hand already on her shoulder: one light pat, then the moon.
    dict(loc="roof_c", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="roof",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, sitting on the tiles in the right foreground hugging her knees, her chin resting on her knees; {only_tang('right')}; facing us an arm's length away a little left of the middle, {XU_COAT}, sitting on the tiles, framed from the waist up with clear space above his head, his right hand already resting lightly on her left shoulder, the one nearest him, from the first frame, his face three-quarter to screen right toward her, never the lens; warm: eyes soft, the corners of his mouth lifting a little, lips moving lightly between words; behind him only the dark tiles and the black night sky; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("xuyan", "不反悔。鋪子六天後開張，妳還得替我管帳。", "輕，帶笑")],
         motion=f"Xu Yan gives her shoulder one light pat and speaks; {HEADSTILL}; after the last word he takes his hand back and turns his face up toward the moon beyond the upper right of the frame",
         zh="過肩中景、慢推（不送屋頂圖）：前景右唐小棠的背影（下巴擱在膝上、頭不動）；許硯右手第一格已經輕放在她靠他那邊的左肩上（原稿『把她滑下的外衣拉好』：真人版她沒有外衣，拍法 4），輕拍一下說（本鏡可以微笑）；說完收手、抬頭看畫右上外的月亮"),
    # ---- scene 2: six days later, day 21, the shop opening. Outside (no picture: drop_set), then inside set-xuji-pu-l1.
    # Erniu may laugh (script). The signboard stays above the top of the frame (bible rule 7).
    dict(chapter="許記開張", loc="street", cam="Wide shot, slow tracking shot forward", chars=["erniu"], night="street",
         comp=f"wide shot from the street toward the open shop front, the frosty grey flagstones in the foreground: {ERNIU}, standing on a low wooden stool in front of the wide open doorway of the shop, framed full length, his right hand already gripping the corner of a long plain red cloth that hangs from above the top edge of the frame, the top edge of the frame just below the shop's eave; his face three-quarter to screen left toward the crowd, never the lens; beaming: eyes bright, mouth wide between words; in the soft foreground about twelve {CROWD}, seen from behind, crowded in front of the shop, their breath white; on the right the next shop front with bolts of plain coloured cloth hanging in its doorway; {HANDS}",
         lines=[("erniu", "許記開張囉！柳溪白紙、肥皂，今天開賣！", "扯開大嗓門")],
         motion="in the first second Wang Erniu pulls the red cloth down hard and it slides down from above the top of the frame and drops onto the frosty flagstones in front of the crowd; then he throws up both arms and shouts; the crowd presses a step closer",
         zh="全景、推軌（不送場景圖：店裡的圖是室內，街的圖是有假字招牌的菜市；門外寫成灰瓦木店面、結霜的青石板）：前景是結霜的青石板與十二個街坊的背影（呼白氣）；二牛站在門口的木凳上，右手第一格已經抓著從畫面上緣外垂下的長紅布一角，一扯，紅布從上緣外滑落到人群前；畫面上緣切在屋簷下，**招牌不入鏡**（拍法 7）；隔壁綢緞莊門口掛素色布匹在畫右；二牛舉手大喊（本鏡可以笑）"),
    # Xiaohe may smile (script). The shelves are on the left wall (the picture), which is her right as she faces us.
    dict(loc="am", cam="Medium shot, slow tracking shot", chars=["xiaohe"], night="am",
         comp=f"medium shot just inside the wide front doorway at the back: {XIAOHE}, standing on the grey tiles, framed from the knees up with clear space above her head, her face three-quarter to screen right toward one plump middle-aged woman in a plain blue cotton jacket coming in from the street at the right edge, seen only from behind, never the lens; sweet and eager: eyes bright, a gap-toothed grin, lips moving quickly between words; two {CROWD} stepping past her into the shop, soft; behind her the bright doorway and the frosty street; {HANDS}",
         lines=[("xiaohe", "隔壁綢緞莊的大娘也來了！肥皂在右邊！", "嘴甜")],
         motion="Xiaohe rises on her tiptoes and waves her right hand at the woman, then sweeps her open left hand toward the shelves at screen left, palm up, as she speaks; the woman turns toward the shelves",
         zh="中景、跟拍：小禾站在後面那道大門口內（補丁淡紫短襖、紅繩小辮、腰帶塞草編兔子），朝畫右從隔壁走進來的大娘（背影）踮腳揮右手，再攤開左手掌往畫左的架子一引（不用手指；架子在左牆，正是她面對我們時的右邊）；嘴甜地說（本鏡可以笑）"),
    # Tang Xiaotang from behind across the counter (bible rule 3): the customers face us.
    dict(loc="am", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="am",
         comp=counter_back(f"on the counter in front of her {ABACUS} and a little heap of copper coins, and {PAPER} under her right hand; across the counter facing us three customers framed from the chest up, soft: a woman in a blue cotton jacket, an old man in a cloth head wrap and a young scholar in a plain grey long gown and a square cloth cap, their faces eager; behind them the bright doorway and more people; {HANDS}"),
         lines=[("tangxiaotang", "白紙一刀三百文，肥皂一塊一錢，下一位！", "頭也不抬")],
         motion=f"the young woman pushes the bundle of paper across the counter to the woman with her right hand and sweeps the copper coins toward her with her left; {HEADSTILL}; she looks down at the counter the whole shot; the old man steps up next",
         zh="【改背後拍】過肩中景、慢推：前景右唐小棠的背影站在櫃檯後（櫃檯寫在右牆前，圖上沒有），櫃檯上小金算盤、一小堆銅錢，右手下一刀紙繩紮的白紙；櫃檯對面三個客人（婦人、包頭老人、方巾書生）胸口以上朝我們；她右手把紙推過去、左手把銅錢撥過來，頭不動、一直低頭看櫃檯（頭也不抬）。台詞 nospeak，剪接放錄音"),
    dict(loc="am", cam="Medium shot, slow push in", chars=["aling"], night="am",
         comp=f"medium shot by the shelves on the left wall: A-ling, {ALING}, standing in front of the lower shelves with their neat rows of pale cream soap bars, framed from the waist up with clear space above her head, {SOAP} in her right hand; on screen right one woman in a plain blue cotton jacket seen only from behind, holding out a small empty bamboo basket in both hands; A-ling's face three-quarter to screen right toward the woman, never the lens; calm and plain: brows level, eyes steady, the corners of her mouth level, lips moving softly between words; behind her only the shelves; {HANDS}",
         lines=[("aling", "洗衣洗手都乾淨，一塊能用一個月。", "淡淡地")],
         motion="A-ling lays the bar of soap in the woman's basket and speaks; after the last word she folds her hands in front of her waist inside her sleeves",
         zh="中景、慢推：左牆架子前，阿令（灰白布裙、木簪）右手拿一塊乳白肥皂，放進畫右婦人（背影）兩手捧著的竹籃，淡淡地說（不笑）；說完兩手收進袖裡交握"),
    # From behind and above her (rule 3): the crowd faces us; the bundle slides off the counter's front edge.
    dict(loc="am", cam="High-angle wide shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="am",
         comp=f"high-angle wide shot from above and behind {TBACK}, standing behind the long dark wooden counter in the right foreground, both her hands already braced flat on the counter top from the first frame; {only_tang('right')}; beyond the counter the shop packed with about fifteen {CROWD}, shoulder to shoulder from the counter back to the bright doorway, their faces toward the counter; one woman in a blue cotton jacket is pressed against the front of the counter, and {PAPER} lies at the counter's front edge; {HANDS}",
         lines=[("tangxiaotang", "別擠別擠！紙掉在地上要被踩爛了！", "急，尖聲")],
         motion=f"in the first second the crowd surges and the woman in blue bumps the counter; the bundle of paper slides off its front edge and drops to the floor among the feet; the young woman leans forward over her braced hands; {HEADSTILL}; she looks straight down at the fallen bundle the whole shot; the townspeople's faces turn down toward the floor",
         zh="【改背後拍】高角度全景、從她後上方往下看、慢推：前景右唐小棠的背影，兩手第一格已經撐在櫃檯上；櫃檯外擠滿約十五個街坊（宋式衣著，手上只有竹籃或空手），從櫃檯一路擠到亮亮的門口；第一秒人群一湧，藍衣婦人撞上櫃檯，櫃檯前緣那刀紙滑落到腳邊；她身子往前一探、頭不動、看著地上的紙。台詞 nospeak，剪接放錄音"),
    # He may grin, flustered (the script gives no smile rule; a cheerful raised voice).
    dict(loc="am", cam="Medium shot, slow tracking shot", chars=["xuyan"], night="am",
         comp=f"medium shot in the middle of the crowded shop: {XU}, framed from the knees up with clear space above his head, already bending down from the first frame to {PAPER} lying on the grey tiles at his feet; townspeople in Song-dynasty cross-collared clothes pressing around him, only their shoulders and backs at the edges of the frame, soft; his face three-quarter to screen right, never the lens; flustered and good-humoured: brows raised, eyes wide, mouth wide between words; behind him the shelves on the left wall, soft; {HANDS}",
         lines=[("xuyan", "慢點慢點，人人都有，今天備了一百塊肥皂！", "提高聲音")],
         motion="Xu Yan picks up the bundle, brushes it once with his hand and is jostled two steps back toward screen right; he lifts his left hand open above the crowd and calls out; after the last word he holds the bundle against his chest",
         zh="中景、跟拍：店中間，許硯第一格已經彎腰去撿地上那刀紙，四周只露街坊的肩與背；撿起、拍一下，被擠得往畫右退兩步，舉起攤開的左手提高聲音喊；說完把紙抱在胸前"),
    # Qin Shuang's order: a flat open hand swept toward the street (no pointing, no blade).
    dict(loc="am", cam="Low-angle medium shot, slow push in", chars=["qinshuang"], night="am",
         comp=f"low-angle medium shot from inside the shop toward the wide front doorway at the back, the stone threshold in the soft foreground: Qin Shuang, {QIN}, standing on the threshold in the doorway, framed from the knees up with clear space above her head, her body side-on, her face in profile to screen left toward the street outside the doorway at the left, never the lens; commanding: brows drawn level, eyes sharp, jaw firm, lips moving crisply between words; around her in the doorway the backs and shoulders of a few townspeople, soft; behind her the bright frosty street; {HANDS}",
         lines=[("qinshuang", "二牛，帶你的人在門外列隊，一排五個！", "一聲斷喝")],
         motion="Qin Shuang steps up onto the threshold and sweeps her right hand out flat, palm down, toward the street at screen left as she shouts; after the last word her hand stays out and the people around her step back",
         zh="低角度中景、慢推（前景是門檻）：秦霜（腰帶空著，拍法 5：稿子的柴刀不寫）一步跨上後面大門的門檻，身子側著、臉朝畫左門外的街，右手掌平平往門外一揮（不用手指）斷喝；說完手不收、身邊的人往後讓"),
    # Erniu may grin (script). The six young men are empty-handed (rule 17).
    dict(loc="street", cam="Wide shot, slow tracking shot to the left", chars=["erniu"], night="street",
         comp=f"wide tracking shot along the frosty county town street outside the shop: {ERNIU}, framed from the knees up, walking along beside a single long queue of about twenty {CROWD}, his face three-quarter to screen left toward the queue, never the lens; cheerful and loud: eyes bright, a broad honest grin, mouth wide between words; six young men in Song-dynasty plain hemp cross-collared short jackets, cloth head wraps and cloth shoes, their hands empty, stand spaced along the queue with their arms held out at their sides, keeping it in one straight line that runs away toward the street corner in the distance; {HANDS}",
         lines=[("erniu", "一個一個來，從這裡排到街角，誰也別插隊！", "大嗓門")],
         motion="Wang Erniu walks along the queue and waves it on with a big sweep of his arm as he shouts; the young men hold their arms out and two townspeople who stepped out of the line step back into it",
         zh="全景、往左跟拍（不送場景圖）：門外結霜的大街，二牛沿著一條約二十人的長隊走、大手一揮喊（本鏡可以憨笑）；六個宋式短打、布包頭的年輕人空著手、張開手臂站在隊伍旁，把隊排成一直線、一路排向遠處街角；兩個跨出隊的人退回隊裡"),
    # He may smile (script).
    dict(loc="am", cam="Medium two-shot, slow push in", chars=["xuyan", "qinshuang"], night="am",
         comp=f"medium two-shot at the wide front doorway at the back: on screen left {XU}, leaning his left shoulder against the left door post, framed from the knees up with clear space above his head, his face three-quarter to screen right toward her, never the lens; teasing: one brow raised, eyes bright, the corners of his mouth lifting, lips moving between words; on screen right Qin Shuang, {QIN}, standing against the right door post with her arms at her sides, framed from the knees up, her face three-quarter to screen left toward him, never the lens; brows level, lips closed; beyond them the queue outside on the bright frosty street, soft; {HANDS}; exactly two people in the doorway",
         lines=[("xuyan", "妳練的兵，就拿來排隊買肥皂？", "逗她")],
         motion=f"Xu Yan brushes the dust off his sleeve, leans back against the door post and tilts his head at her as he speaks; {quiet('Qin Shuang', 'her')}",
         zh="中景、慢推：後面大門口，畫左許硯拍掉袖子上的灰、左肩靠上左邊門柱、歪頭逗她（本鏡可以笑）；畫右秦霜靠著右邊門柱、嘴閉著；門外排隊的人虛焦"),
    # Her mouth corner lifts (script).
    dict(loc="am_c", cam="Close-up, slow push in", chars=["qinshuang"], night="am",
         comp=f"close-up of Qin Shuang, {QIN}, standing in the doorway, framed from the chest up with space above her head, her face three-quarter to screen left toward Xu Yan off screen left, never the lens; dry: eyes sidelong, one brow raised, one corner of her mouth lifting a little, lips moving crisply between words; behind her only the queue on the bright street, soft",
         lines=[("qinshuang", "總比讓人把紙踩爛好。他們排得比衙役還齊。", "淡淡")],
         motion="Qin Shuang gives him a sidelong look and folds her arms across her chest as she speaks; after the last word she looks back out at the queue",
         zh="近景、慢推（身後只有門外排隊的人，虛焦）：秦霜斜他一眼、兩手抱到胸前說（本鏡嘴角一勾）；說完回頭看門外的隊"),
    # ---- the afternoon. Tang Xiaotang from behind, looking across the shop at the half-bare shelves on the left wall.
    dict(loc="pm", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="pm",
         comp=counter_back(f"her right hand resting on {ABACUS} lying on the counter in front of her; beyond the counter, across the shop, the shelves on the left wall mostly bare: three bundles of blank white paper on the top shelf and a short row of pale soap bars below; two customers by the shelves, soft; {HANDS}"),
         lines=[("tangxiaotang", "紙只剩三刀，肥皂還剩十二塊，快賣完了。", "笑著撥算盤")],
         motion=f"the young woman's right fingers flick one row of gold beads across the abacus, then another; {HEADSTILL}; she looks across the shop at the bare shelves the whole shot",
         zh="【改背後拍】過肩中景、慢推（午後）：前景右唐小棠背影在櫃檯後，右手撥櫃檯上的小金算盤兩排；櫃檯外、店那頭左牆的架子空了一大半，上層剩三刀紙、下層一小排肥皂；頭不動、一直看著架子。台詞 nospeak，剪接放錄音（原稿『抬頭看門外』併進 s15 的主觀鏡）"),
    # Her point of view out of the doorway: the shop picture is exactly this view (the front doorway in the back wall, three
    # tall bright openings between dark posts and lattice panels); the carriage passes behind the posts, seen in the openings.
    dict(loc="door", cam="Wide shot from her point of view, slow push in", chars=[], night="pm", act=3,
         comp=f"point-of-view shot from behind the counter across the shop toward the front doorway in the back wall, the dark door posts and lattice panels framing three tall bright openings onto the sunlit street; beyond them on the street one black-lacquered covered carriage drawn by two black horses, its curtain down, two round red silk lanterns hanging from the front corners of its roof, plain smooth red all over with a thin gold rim at top and bottom; the driver on the front seat seen only from behind in a dark cotton jacket; across the street grey-tiled wooden shop fronts with plain dark wooden boards; the shop floor between us and the doorway empty in the afternoon light",
         lines=[],
         motion="the carriage rolls slowly from screen right to screen left past the doorway, glimpsed in the bright openings between the dark posts, the two red lanterns swaying with each step of the horses, and passes out of sight at the left",
         zh="主觀（唐小棠從櫃檯後看出門外）、慢推（送鋪子圖：圖上正是這個視線，後牆大門三道亮的高門洞夾著深色門柱與格子板）：門外街上一輛黑漆篷車（兩匹黑馬、簾子放下，車頂前角兩盞素紅綢圓燈籠、上下一圈細金邊，**燈籠上沒有任何圖文**）從畫右往畫左慢慢經過，在門洞之間一段一段看得到，燈籠一晃一晃；車夫只拍背影；對街是灰瓦木店面（素面木板）（無台詞）"),
    # Insert: the abacus falls. The prop picture prop-jinsuanpan-l1 in the set slot once picked; until then the free floor crop.
    dict(loc="insert", cam="Insert close-up, slow push in", chars=[], night="pm", act=2,
         comp=f"insert close-up, the shot opens directly on {ABACUS} slipping out from between the fingers of a small hand in a light peach-pink silk sleeve cuff, a hand's height above the grey stone floor, from its very first frame; only the hand, its sleeve cuff, the gold abacus and the grey stone tiles are in the frame; warm afternoon light across the tiles",
         lines=[],
         motion="the gold abacus drops from the fingers to the grey stone floor, lands flat with its beads jumping and bounces once; the small hand stays open above it, its fingers trembling a little",
         zh="插鏡、慢推（第一格就是正從她指間滑落的小金算盤：巴掌大、細金框、五排小金珠；只有桃粉袖口的手、算盤與青石地磚；送道具圖 `prop-jinsuanpan-l1`（待試鏡挑定），挑定前送免費裁切的地磚圖 `set-xuji-pu-floor-l1`）：算盤掉到地上、算珠一跳、彈一下；手停在上面、手指微抖（無台詞）"),
    dict(loc="pm", cam="Medium shot, slow push in", chars=["aling"], night="pm",
         comp=f"medium shot by the nearly bare shelves on the left wall: A-ling, {ALING}, standing, framed from the waist up with clear space above her head, {SOAP} in her right hand, her body turned toward the bright front doorway at screen right, her eyes on the street beyond it, never the lens; alert and cool: eyes narrowed, brows drawn together, lips pressed together; behind her only the bare shelves; {HANDS}",
         lines=[("aling", "那輛車掛的紅燈籠，是誰家的？", "低聲，盯著門外")],
         motion="A-ling sets the soap down on the shelf by touch, her eyes following something moving away to screen left beyond the doorway; then she turns her head toward the counter beyond the right edge of the frame and speaks low; after the last word her eyes stay on the counter",
         zh="中景、慢推：左牆幾乎空了的架子前，阿令摸著把肥皂放回架上（眼睛不離門外），盯著門外往畫左遠去的馬車，再轉頭朝畫右的櫃檯低聲問；說完眼睛停在櫃檯"),
    # Her answer from behind her (rule 3): A-ling's face takes it. The abacus already picked up (s16's pick-up before the frame).
    dict(loc="pm", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "aling"], nospeak=["tangxiaotang"], night="pm",
         comp=counter_back(f"{ABACUS} already held tight against her chest in her right hand from the first frame, its gold edge showing past her right arm; facing us beyond the counter a little left of the middle A-ling, {ALING}, standing, framed from the waist up with clear space above her head, her face three-quarter to screen right toward her, never the lens; suspicious: eyes narrowed a little, brows drawn, lips pressed together; behind A-ling the bare shelves, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("tangxiaotang", "沒什麼，是我看錯了，一輛過路的車。", "太快")],
         motion=f"the young woman holds the abacus tighter against her chest; {HEADSTILL}; she looks straight ahead at A-ling the whole shot; A-ling's eyes search her, then flick once to the doorway at the back and come back; {quiet('A-ling', 'her')}",
         zh="【改背後拍】過肩中景、慢推：前景右唐小棠背影在櫃檯後，右手第一格已經把撿起的金算盤緊按在胸前（從右臂邊露出一角金框）；櫃檯對面阿令看著她、眼睛瞇一點、眉頭一皺、嘴閉著，眼睛往後面大門一瞟再回來（原稿唐小棠近景『硬擠出笑』改成阿令聽的臉，拍法 3）。台詞 nospeak，剪接放錄音"),
    # The guild master (MINOR, his live portrait through extras.json + swap). A fawning smile is the script's (陪笑).
    dict(loc="pm", cam="Medium shot, slow tracking shot", chars=["hanghui"], night="pm",
         comp=f"medium tracking shot: {GUILD}, {LEDGERS} held against his chest in both arms, squeezing in from the bright front doorway at the back past the shoulders of queuing townspeople in the soft foreground, framed from the waist up with clear space above his head, his face three-quarter to screen right toward the counter beyond the right edge of the frame, never the lens; fawning: brows lifted, eyes creased, a strained polite smile, lips moving between words; behind him the doorway and the half-bare shelves, soft; {HANDS}",
         lines=[("hanghui", "在下是書坊行會的會長，想跟許記談一筆整批的貨。", "拱手，乾笑")],
         motion="the guild master walks up toward the counter at screen right, tucks the ledgers under his left arm and bows with his hands joined in front of his chest as he speaks; after the last word he stays bent a little, smiling",
         zh="中景、跟拍：行會會長（灰圓領綢袍、額上黑紗網巾、小髻；送真人定妝照 `hanghui-huizhang-portrait-l1`）兩手把三本素藍布面合起的帳冊抱在胸前，從後面大門擠過排隊的人（前景的肩虛焦）走到畫右的櫃檯前，把帳冊夾到左臂下、拱手彎腰陪笑地說"),
    # Over the guild master's shoulder (unnamed, no picture: rule 2).
    dict(loc="pm", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="pm",
         comp=f"over-the-shoulder medium shot from close behind one thin man in a grey round-collared silk gown with a black gauze band round his brow seen only from behind, appearing only once, in the right foreground, only the back of his head with a small topknot, his right shoulder and the edge of a closed blue ledger under his arm showing, soft; facing us a little left of the middle {XU}, standing at the near end of the long dark counter with his left elbow resting on its top from the first frame, framed from the waist up with clear space above his head, his face three-quarter to screen right toward the man, never the lens; sly: one brow raised, eyes narrowed, lips moving between words; behind him the plain white panelled wall, soft; {HANDS}; exactly two people, the man in the foreground seen only from behind",
         lines=[("xuyan", "會長親自來進貨？前幾天的告示，不是貼滿全縣城嗎？", "挑眉")],
         motion="Xu Yan settles his elbow on the counter and raises one brow at the man as he speaks; the man in the foreground keeps his head still, the back of his head toward us the whole shot; after the last word Xu Yan waits, his lips pressed together",
         zh="過肩中景、慢推：前景右只有會長的後腦（小髻、黑紗網巾）、右肩與夾在臂下的藍帳冊一角（不點名、不送圖，拍法 2）；許硯第一格已經左手肘撐在櫃檯靠我們這頭，挑眉看他說；說完抿嘴等"),
    dict(loc="pm", cam="Medium shot, slow push in", chars=["hanghui"], night="pm",
         comp=f"medium shot of {GUILD}, standing at the counter, framed from the waist up with clear space above his head, {LEDGERS} under his left arm, a folded plain grey handkerchief already in his right hand, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; uneasy: brows pinched upward, eyes darting, lips stretched thin between words; behind him the half-bare shelves, soft; {HANDS}",
         lines=[("hanghui", "那是誤會。書生天天上門問，書坊不能沒有貨啊。", "乾笑")],
         motion="the guild master dabs his forehead with the handkerchief; the ledgers slip in his left arm and he clutches them tight against his side; he speaks with a dry little laugh in his voice; after the last word his lips press thin",
         zh="中景、慢推：會長站在櫃檯前，右手第一格已經拿著摺好的灰手帕擦額頭，左臂的帳冊一滑、趕緊夾緊；乾笑著說（嘴唇抿薄、眼睛亂轉，不笑）"),
    # From behind her across the counter (rule 3): the guild master's face takes the price. She may smile (script); unseen.
    dict(loc="pm", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "hanghui"], nospeak=["tangxiaotang"], night="pm",
         comp=counter_back(f"her right hand resting on {ABACUS} lying on the counter in front of her; facing us across the counter a little left of the middle {GUILD}, {LEDGERS} against his chest, framed from the waist up with clear space above his head, his face three-quarter to screen right toward her, never the lens; his smile freezing: eyes widening, brows jumping, the corners of his mouth twitching down; behind him the half-bare shelves, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("tangxiaotang", "要貨可以，一刀加三成，三百九十文。", "慢條斯理")],
         motion=f"the young woman's right forefinger slowly pushes one gold bead across, then a second one; {HEADSTILL}; she looks straight ahead at the guild master the whole shot; {quiet('The guild master')}; his throat moves as he swallows",
         zh="【改背後拍】過肩中景、慢推：前景右唐小棠背影，右手在櫃檯上的小金算盤上慢慢撥兩顆珠子；櫃檯對面會長抱著帳冊、笑容僵住（眼睛一睜、眉一跳、嘴角往下抽）、吞口水、嘴閉著（原稿『走到許硯旁邊、把算盤往櫃檯一放』併進第一格之前）。台詞 nospeak，剪接放錄音"),
    # The script's opened page is never filmed (rule 7): his palm pressed on the closed stack.
    dict(loc="pm", cam="Medium shot, slow push in", chars=["hanghui"], night="pm",
         comp=f"medium shot of {GUILD}, standing at the counter, framed from the waist up with clear space above his head, {LEDGERS} lying flat on the counter top in front of him under his right palm from the first frame; his face three-quarter to screen right toward the young woman beyond the right edge of the frame, never the lens; grudging: jaw clenched, the corner of his mouth twitching, brows knotted, lips moving stiffly through his teeth; behind him the half-bare shelves, soft; {HANDS}",
         lines=[("hanghui", "五十刀，加三成就加三成，分五批交。", "咬牙")],
         motion="the guild master gives one stiff nod with his teeth gritted and presses his palm flat down on the closed ledgers as he speaks; after the last word his jaw stays clenched",
         zh="中景、慢推：會長的右掌第一格已經按在櫃檯上合起的那疊素藍帳冊上（原稿『翻開一頁』不拍：紙上的字一律不拍，拍法 7），咬牙點一下頭、從牙縫裡說；說完腮幫還咬著"),
    # Xu Yan's mouth corners may ease (script).
    dict(loc="pm", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="pm",
         comp=counter_back(f"her right forefinger already on one bead of {ABACUS} lying on the counter in front of her; facing us across the counter a little left of the middle {XU}, standing with one hand resting on the counter, framed from the waist up with clear space above his head, his face three-quarter to screen right toward her, never the lens; quietly pleased: eyes bright, the corners of his mouth easing, lips closed; behind him the half-bare shelves, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("tangxiaotang", "好，三天交一批、一批十刀，交一批收一批的錢。", "乾脆")],
         motion=f"in the first second the young woman snaps the bead across with one click; {HEADSTILL}; she looks straight ahead across the counter the whole shot; {quiet('Xu Yan')}; the corners of his mouth ease a little more",
         zh="【改背後拍】過肩中景、慢推：前景右唐小棠背影，右手食指第一格已經按在一顆金珠上，第一秒『喀』一撥；櫃檯對面許硯一手搭在櫃檯上、嘴閉著、嘴角一鬆（本鏡可以）（會長在畫外）。台詞 nospeak，剪接放錄音（結尾）"),
    # ---- scene 3: the evening, closing time (set-xuji-pu-l1, the shelves bare). Xiaohe may laugh (script).
    dict(chapter="打烊前", loc="eve", cam="Medium shot, slow push in", chars=["tangxiaotang", "xiaohe"], nospeak=["tangxiaotang"], night="eve",
         comp=f"medium shot from close behind {TBACK}, standing in the middle foreground facing the completely bare shelves on the left wall, framed from the waist up, both her arms already raised high above her head from the first frame; {only_tang('middle')}; beside her on screen left {XIAOHE}, framed from the knees up, turned three-quarter toward us, her face lifted toward her, never the lens; delighted: a big gap-toothed grin, eyes bright; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "全賣空了！二十刀紙、一百塊肥皂，一樣不剩！", "兩手一舉")],
         motion=f"the young woman gives one small hop on the spot and lands, her arms still raised; {HEADSTILL}; she looks straight ahead at the bare shelves the whole shot; Xiaohe claps her hands and laughs, saying nothing",
         zh="【改背後拍】中景、慢推：前景中唐小棠背影對著左牆全空的架子，兩手第一格已經高舉，原地輕輕一跳、落地（不轉圈）；畫左小禾四分之三朝我們，抬頭看她、拍手笑（不說話，本鏡可以笑）。台詞 nospeak，剪接放錄音"),
    # No blue light, no panel words (rule 11): his reaction only. He was smiling; the second line takes it off.
    dict(loc="eve_c", cam="Close-up, slow push in", chars=["xuyan"], night="eve",
         comp=f"close-up of {XU}, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes on a point in the air in front of him, never the lens; pleased at first: eyes creased, the corners of his mouth lifted, lips closed; behind him only the bare shelves, soft",
         lines=[("xitong", "叮。許記開張，首日售罄。", "冷，宣布"),
                ("xitong", "主線天下歸心，百分之一。", "冷，宣布")],
         panel=[("許記開張，首日售罄", "task"), ("主線天下歸心，百分之一", "task")],
         motion=f"for the first three seconds Xu Yan keeps his pleased look; then the corners of his mouth come down level and one brow lifts slowly, his eyes on the same point in the air; {SILENT_HE}",
         zh="近景、慢推（拍法 11：不寫藍光，面板由剪接疊上）：許硯本來嘴角上揚（本鏡前段可以笑），前三秒不變；之後嘴角收平、一邊眉毛慢慢挑起，眼睛一直看面前空中一點；全程嘴閉著（系統畫外）"),
    dict(loc="eve_c", cam="Close-up, slow push in", chars=["xuyan"], night="eve",
         comp=f"close-up of {XU}, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes sliding sideways to a point in the air in front of him, never the lens; unimpressed: one brow raised, the corners of his mouth flat, lips pressed together; behind him only the bare shelves, soft",
         lines=[("xuyan", "賣空一整天，才漲百分之一？", "心裡話，嫌少", "inner"),
                ("xitong", "嫌少？宿主可以回去試試百分之零。", "冷"),
                ("xuyan", "不嫌，一點都不嫌，百分之一很好。", "心裡話，趕緊改口", "inner")],
         motion=f"for the first three seconds Xu Yan gives the air a sidelong look; then he blows out a breath through his nose and shakes his head once; from the seventh second he lifts both palms a little in front of his chest, eyes wide, like a man taking it back; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（長鏡）：許硯斜眼看面前的空氣（心裡嫌少）；系統回嘴時從鼻子吐一口氣、搖一下頭；第七秒起兩手掌在胸前微微一抬、眼睛一睜（趕緊改口）；全程嘴閉著（心裡話與系統都畫外）"),
    # From behind her: the box of the day's takings (a third box, plain pale wood, not e018's dark brown trap box and not
    # her red lacquer case).
    dict(loc="eve", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="eve",
         comp=counter_back(f"looking down at the counter top in front of her, where {BOX} stands open with strings of copper coins and small lumps of silver inside and {ABACUS} beside it; her right hand already lowering one last string of copper coins into the box from the first frame; beyond the counter the bare shelves and the doorway in the low orange light, soft; {HANDS}"),
         lines=[("tangxiaotang", "今天收十六兩，連賠銀算上，帳上還剩七十七兩。", "清楚，滿意")],
         motion=f"the young woman lays the last string of coins in the box, closes the lid with both hands, then flicks one bead across the abacus with her right forefinger; {HEADSTILL}; she looks down at the box the whole shot",
         zh="【改背後拍】過肩中景、慢推：前景右唐小棠背影低頭看櫃檯，素淡色小木匣（兩個手掌大、跟第 18 集的深褐陷阱箱、她的紅漆妝匣都不同）開著、裝銅錢串與碎銀，旁邊小金算盤；右手第一格已經在放最後一串銅錢，放下、兩手蓋上匣蓋、右手食指撥最後一顆珠子；頭不動、一直低頭看匣子。台詞 nospeak，剪接放錄音"),
    dict(loc="eve", cam="Medium shot, slow tracking shot", chars=["erniu", "qinshuang", "xiaohe"], night="eve",
         comp=f"medium shot near the wide front doorway in the evening: in the middle {ERNIU}, carrying {BOARD} upright against his right shoulder toward the doorway, framed from the knees up with clear space above his head, his face turned back three-quarter to screen right toward the counter beyond the right edge of the frame, never the lens; earnest: brows raised, eyes wide, lips moving between words; behind him on screen left Qin Shuang, {QIN}, holding a stack of shutter boards upright against the wall with both hands, her face toward him, lips closed; in the right foreground {XIAOHE}, sweeping the grey tiles with a bamboo broom held in both hands, lips closed; {HANDS}; exactly three people",
         lines=[("erniu", "我明早回柳溪報信，紙坊得日夜抄才趕得上。", "扛著門板")],
         motion=f"Wang Erniu carries the board to the door post and turns his head back as he speaks; {quiet('Qin Shuang and Xiaohe', 'their', True)}; Xiaohe keeps sweeping; after the last word he sets the foot of the board down by the door post",
         zh="中景、跟拍：二牛右肩扛著一塊人高的素木門板往大門口走、回頭朝畫右的櫃檯（畫外）說；畫左後秦霜兩手扶著靠牆的那疊門板；右前小禾兩手拿竹掃帚掃地；秦霜、小禾嘴閉著。三張臉（拍法 1）"),
    dict(loc="eve", cam="Medium shot, slow push in", chars=["aling"], night="eve",
         comp=f"medium shot: A-ling, {ALING}, walking past the end of the long dark counter with one empty plain wooden bucket held by its rope handle in her right hand and stopping there from the first frame, framed from the waist up with clear space above her head, her face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; quiet and grave: eyes steady, brows drawn together a little, lips moving softly between words; behind her the bare shelves and the doorway in the low orange light, soft; {HANDS}",
         lines=[("aling", "那輛掛紅燈籠的車，昨天也停在對街。", "很輕，看著唐小棠")],
         motion="A-ling stops by the counter, the empty bucket hanging still from her hand, and speaks very quietly; after the last word she keeps her eyes on her, her lips pressed together",
         zh="中景、慢推：阿令右手提一個空木桶（繩把）走過櫃檯一端、停下，朝畫右的唐小棠（畫外）很輕地說；說完抿嘴看著她"),
    # Over Tang Xiaotang's back (silent; rule 3 treatment as her other back shots).
    dict(loc="eve", cam="Over-the-shoulder medium close-up, slow push in", chars=["tangxiaotang", "xuyan"], night="eve",
         comp=counter_back(f"facing us across the counter a little left of the middle {XU}, both his hands planted flat on the counter top from the first frame, leaning toward her, framed from the chest up with space above his head, his face three-quarter to screen right toward her, never the lens; serious and quiet: brows drawn together, eyes searching, lips moving low between words; behind him the bare shelves in the low orange light, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("xuyan", "小棠，那輛車，到底是誰家的？", "壓低聲音")],
         motion=f"Xu Yan leans in over his hands and speaks low; {HEADSTILL}; she looks straight ahead at him the whole shot; after the last word he waits, his eyes on her",
         zh="過肩中近景、慢推：前景右唐小棠的背影（頭不動、看著他）；櫃檯對面許硯兩手第一格已經撐在櫃檯上、往前傾，壓低聲音問；說完看著她等"),
    # Her evasion from behind her: eyes down to the abacus, head still (a turn away would show her face).
    dict(loc="eve", cam="Over-the-shoulder medium close-up, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="eve",
         comp=counter_back(f"her head bowed a little toward {ABACUS} under her right hand on the counter; facing us across the counter a little left of the middle {XU}, both his hands on the counter top, framed from the chest up with space above his head, his face three-quarter to screen right toward her, never the lens; worried: brows drawn together, eyes on her, lips pressed together; behind him the bare shelves in the low orange light, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("tangxiaotang", "明天……明天我再跟你說，好不好？", "避開他的眼睛")],
         motion=f"the young woman picks the abacus up a finger's height and sets it down again; {HEADSTILL}; she looks down at the abacus the whole shot; {quiet('Xu Yan')}; his eyes soften",
         zh="【改背後拍】過肩中近景、慢推（原稿她的近景改成背後）：前景右唐小棠背影，頭微低、看著右手下的金算盤，拿起一指高又放下（避開他的眼睛：頭不轉，一轉就露臉）；櫃檯對面許硯皺眉看她、嘴閉著、眼神放軟。台詞 nospeak，剪接放錄音"),
    # The back door to the yard: a plain door in the far right corner (not in the picture); A-ling leaves through it.
    dict(loc="eve", cam="Medium shot, slow push in", chars=["xuyan", "aling"], night="eve",
         comp=f"medium shot: on screen left {XU}, standing in front of the long dark counter, framed from the knees up with clear space above his head, his face three-quarter to screen right toward the young woman behind the counter beyond the right edge of the frame, never the lens; gentle and resolved: brows easing, lips moving evenly between words; in the soft background at the right, a plain dark wooden back door in the far corner of the white panelled wall, and A-ling, {ALING}, small, the empty bucket in her right hand, her hand already on the door from the first frame; {HANDS}; exactly two people",
         lines=[("xuyan", "好，明天說。二牛，上門板，今天打烊了。", "溫和，再提高聲音")],
         motion=f"Xu Yan nods once and straightens up, then turns his head toward the front doorway at screen left and calls out the second half; in the background A-ling pushes the back door open and steps out, and the door swings shut behind her; {quiet('A-ling', 'her')}",
         zh="中景、慢推：畫左許硯站在櫃檯前、看畫右櫃檯後的唐小棠（畫外）點一下頭、直起身，再轉頭朝畫左大門口喊二牛；背景畫右的遠角一扇素木後門（圖上沒有、寫在這裡），阿令提空桶、手第一格已經在門上，推門出去、門在她身後闔上（她從此在後院井邊、不入鏡，接第 21 集）"),
    # ---- dusk. Sun Zhanggui's palm already on the board (contact as a state). His thin smile is the script's.
    dict(loc="dusk", cam="Medium shot, slow push in", chars=["erniu", "sunzhanggui"], night="dusk",
         comp=f"medium shot at the wide front doorway at dusk, the dark door post in the soft left foreground: {ERNIU}, framed from the knees up with clear space above his head, lowering {BOARD} into the groove at the foot of the doorway with both hands; just outside the doorway on screen right {SUN}, framed from the waist up, his right hand in its wide green satin sleeve already resting flat on the top edge of the board from the first frame, holding it; his face three-quarter to screen left, looking past the big young man into the shop, never the lens; smooth: eyes half closed, a thin polite smile, lips moving slowly between words; behind him the county town street deep blue with dusk and {EAVE}; {HANDS}; exactly two people",
         lines=[("sunzhanggui", "許老闆，先別上門板，有貴客要見你。", "笑咪咪，慢條斯理")],
         motion=f"Wang Erniu stops with the board half lowered and stares at the green sleeve; {quiet('Wang Erniu')}; Sun Zhanggui keeps his palm on the board and speaks; after the last word he keeps smiling",
         zh="中景、慢推（前景是虛焦的門柱）：二牛兩手正把一塊門板往門檻的槽裡放；門外畫右孫掌櫃（綠緞袍、玉帶鉤）右手綠緞袖的手第一格已經平按在門板上緣（接觸寫成狀態）；他越過二牛往店裡看、瞇眼笑咪咪慢條斯理地說（本鏡可以笑）；二牛愣住、手停著、嘴閉著；身後是轉藍的暮色大街與屋簷下一盞點亮的素白紙燈籠"),
    # Over Sun Zhanggui's shoulder (unnamed, no picture: rule 2). Xu Yan does not smile.
    dict(loc="dusk", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="dusk",
         comp=f"over-the-shoulder medium shot from close behind one tall thin man in a green satin robe seen only from behind, appearing only once, in the right foreground, only the back of his head with a topknot and his green satin shoulder showing, soft; facing us a little left of the middle {XU}, standing in front of the long dark counter with both hands on its edge from the first frame, framed from the waist up with clear space above his head, his face three-quarter to screen right toward the man, never the lens; wary: brows drawn low, eyes hard, the corners of his mouth level, lips moving evenly between words; behind him the counter and the bare shelves in the dim dusk, soft; {HANDS}; exactly two people, the man in the foreground seen only from behind",
         lines=[("xuyan", "魏記的孫掌櫃？書院街角那輛黑篷車，也是你的吧？", "戒備")],
         motion="Xu Yan takes his hands off the counter, straightens and steps half a step toward the man as he speaks; the man in the foreground keeps his head still, the back of his head toward us the whole shot; after the last word Xu Yan stays still, his eyes on him",
         zh="過肩中景、慢推：前景右只有孫掌櫃的後腦（髮髻）與綠緞肩（不點名、不送圖，拍法 2）；許硯雙手第一格在櫃檯邊上，放開、直起身、往前半步，戒備地說（不笑）；說完不動、盯著他"),
    dict(loc="dusk", cam="Medium shot, slow push in", chars=["sunzhanggui"], night="dusk",
         comp=f"medium shot of {SUN}, standing in the middle of the wide front doorway at dusk, framed from the waist up with clear space above his head, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; smooth and smiling: eyes half closed, a thin polite smile, lips moving slowly between words; behind him the county town street deep blue with dusk and {EAVE}; {HANDS}",
         lines=[("sunzhanggui", "許老闆好眼力。不過今天，我只是帶路的。", "笑咪咪")],
         motion="Sun Zhanggui gives one slow nod and speaks; then he steps aside to screen right, out of the middle of the doorway, and holds his right hand open, palm up, toward the empty doorway; after the last word he stays aside, smiling",
         zh="中景、慢推：孫掌櫃站在大門口正中、身後是暮色的藍與屋簷下的素白紙燈籠，慢慢點一下頭說（本鏡可以笑咪咪），再往畫右一側身、讓出門口、右手掌心朝上往門口一引（摺扇『唰』只在音效）"),
    # Insert: the abacus slides off the counter edge and she catches it (prop picture once picked; else the floor crop).
    dict(loc="insert", cam="Insert close-up, slow push in", chars=[], night="dusk", act=2,
         comp=f"insert close-up, the shot opens directly on {ABACUS} lying at the very front edge of a dark wooden counter top from its very first frame, the grey stone floor below; a light peach-pink silk sleeve cuff at the right edge of the frame; only the abacus, the counter edge, the sleeve cuff, a small hand and the floor are in the frame; dim dusk light",
         lines=[],
         motion="the pink sleeve brushes the abacus and it tips over the edge of the counter; a small hand darts down after it and catches it in the air below the edge, fingers closing round the gold frame",
         zh="插鏡、慢推（第一格就是櫃檯邊緣的小金算盤；整鏡同一景別，不切、不溶；送道具圖或挑定前的地磚圖）：桃粉袖口一帶，算盤從櫃檯邊翻下去，她的手追下去、在半空一把抓住（無台詞）"),
    # Her one silent face (e907's neutral face sentences in spec.json); colour drained, no smile (script).
    dict(sid="s37b", loc="dusk_c", cam="Close-up, slow push in", chars=["tangxiaotang"], night="dusk",
         comp=f"close-up of Tang Xiaotang {TANG}, standing behind the counter, framed from the chest up with space above her head, {ABACUS} clutched tight against her chest in both hands from the first frame, her face three-quarter to screen left toward the doorway off screen left, never the lens; the colour gone from her face: skin pale, eyes wide and fixed, brows drawn up, lips pressed together and trembling; behind her only the plain white panelled wall in the dim dusk",
         lines=[],
         motion=f"Tang Xiaotang straightens up behind the counter, hugging the abacus tighter to her chest, her eyes fixed on the doorway; {quiet('Tang Xiaotang', 'her')}",
         zh="近景、慢推（整鏡同一景別；中性外貌句）：唐小棠在櫃檯後站直，兩手把金算盤緊抱在胸前，眼睛盯著畫左的大門口（畫外），臉色全退、眼睛睜大、眉頭往上擠、嘴抿著發抖、不笑（無台詞）"),
    # The ending. Six people in the script; three named faces at most (rule 1): Wei Shaoqing and Sun Zhanggui with Xu Yan's
    # unnamed back in the foreground (no picture, rule 2); Tang Xiaotang, Erniu, Qin Shuang off screen (e021 c01 shows them).
    # Wei Shaoqing's smile is the script's (嘴角帶笑).
    dict(loc="dusk", cam="Low-angle wide shot, slow push in", chars=["weishaoqing", "sunzhanggui"], night="dusk",
         comp=f"low-angle wide shot from inside the shop, the dark corner of the long counter in the soft left foreground: in the soft foreground at the left one young man in a faded blue-grey scholar's robe seen only from behind, appearing only once, standing in front of the counter, only his back, his shoulders and the back of his head with a topknot showing; beyond him the wide front doorway at the back: at the right door post {SUN}, standing aside, framed full length, his face three-quarter to screen left, eyes half closed, lips closed; in the middle of the doorway {WEI}, stepping over the threshold from the first frame against the last orange glow and the deep blue street, framed full length, {FAN} in his right hand at his chest; his eyes passing over the young man's shoulder toward the counter beyond the left edge of the frame, never the lens; amused and arrogant: peach-blossom eyes narrowed, one corner of his mouth curling up, lips moving lazily between words; {EAVE}; {HANDS}; exactly three people, the young man in the foreground seen only from behind",
         lines=[("weishaoqing", "我的未婚妻，在你家？", "拖長尾音，笑")],
         motion=f"Wei Shaoqing steps in over the threshold and waves the open fan twice at his chest, then speaks with a lazy drawl; {quiet('Sun Zhanggui')}; the young man in the foreground stays still, the back of his head toward us the whole shot; after the last word Wei Shaoqing stands still, the fan stopped at his chest, smiling",
         zh="低角度全景、慢推（前景左是虛焦的櫃檯一角）：前景左許硯的背影站在櫃檯前（不點名、不送圖，拍法 2）；後面大門口：孫掌櫃側身站在右邊門柱旁、瞇眼、嘴閉著；魏少卿（寶藍織金錦袍、小玉冠）第一格已經逆著最後一點夕照與轉藍的大街跨過門檻，右手一把打開的素米色灑金點摺扇（扇面只有金點）在胸前搖兩下，眼睛越過許硯的肩看向畫左外的櫃檯，拖長尾音、嘴角帶笑地說；屋簷下一盞素白紙燈籠。唐小棠、二牛、秦霜在畫外（一鏡最多三張臉，拍法 1；第 21 集 c01 接他們）（結尾）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e020-r2/script.md`（c01–c38 對應 s01–s38，c37b 是 s37b；2026-11-06 的 r2 稿；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-16）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e011-e020.md`（拍法 1–18 條）。第 2 篇章最後一集。",
    "- 內部工作編號 920（`hailuo/{ff,clips}-dh-e920.json`、`colab/runs/e920/extras.json`、`colab/runs/e920-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e920-dh/`）；發布 slug `zhong-tian-qu-qi-e020-r2`。不放集數、不放片名卡；s01 接第 19 集 s41（屋頂、唐小棠背影抱膝下巴擱在膝上、許硯披舊灰外衣在她左邊一臂外）。s38 交給第 21 集 c01（同一刻：許硯往前一步擋在櫃檯前）。",
    "- 照第 19 集審稿後的寫法一開始就照做：`OFFSCREEN_SPEECH = False`；背景寫在場的東西（拍法 18）；道具與接觸寫在第一格；不用手指指人（s05、s10、s36 攤開手掌）；紙一律是『紙繩紮好、每面空白』的一刀白紙，帳冊合著、素藍布面（s23 原稿『翻開一頁』改成手掌按著合起的帳冊）；招牌不入鏡（s04 畫面上緣切在屋簷下）；燈籠：篷車兩盞素紅綢、屋簷一盞素白紙燈籠，每鏡同一句。",
    "- **唐小棠不露嘴說話**：她十句在畫面上的台詞（s02、s06、s08、s14、s18、s22、s24、s25、s28、s32）都從背後拍（nospeak，spec 拿掉她三張臉部參考圖與身分句；兩顆高丸子各繞一條短粉緞帶、後頸露出、不寫珍珠簪；一個固定視線、頭不動）。櫃檯鏡從她背後越過櫃檯拍對面的人（客人、阿令、會長、許硯）；s18 原稿她的近景改成阿令聽的臉。她唯一的臉是 s37b（不說話、中性外貌句、臉色全退、不笑）；s16、s37 只拍她的手。真人版 l1 交領短襦、沒有外衣：s03『把她滑下的外衣拉好』改成輕拍她的肩。",
    "- **小金算盤沒有參考圖**（定妝照腰間是金色結飾，不是算盤）：每鏡同一句（巴掌大、細金框、五排小金珠）。第 17 集燈籠骨架長成五種樣子的教訓——先做道具圖：`live-action/screen-test-e020.py`（Qwen 只改一件事、種子 37031／37032，**沒有跑**），挑定後 `refs-live/prop-jinsuanpan-l1` 放進兩支插鏡（s16、s37）的場景圖位置；挑定前兩支插鏡送免費裁切的地磚圖 `set-xuji-pu-floor-l1`，並放在 `colab-jobs-wait.json` 等。",
    "- **一鏡最多三張臉**（拍法 1）：s29 二牛、秦霜、小禾；s38 原稿六個人改成魏少卿、孫掌櫃加前景許硯的背影（不點名、不送圖），唐小棠、二牛、秦霜在畫外（第 21 集 c01 接）。過肩前景都不點名、不送圖：s20 會長、s35 孫掌櫃、s38 許硯。秦霜腰帶空著（稿子的柴刀不寫）；六個年輕人空手；群眾寫宋代衣著與人數、手上只有竹籃或空手。",
    "- 場景（協調者 2026-11-16 決定，每張放大看過）：屋頂 s01–s03 不送圖（第 19 集審稿必改 15：近鏡不帶 3D 屋頂圖）；許記鋪子 `set-xuji-pu-l1`（站主挑的 37003，空店、沒有字）照圖寫：**架子在左牆、大門在後牆正中、右邊白色板牆**，櫃檯寫在右牆前（圖上沒有），通後院的後門寫在右邊遠角；門外 s04、s11 不送圖（s15 從櫃檯後看出門的主觀鏡送鋪子圖：圖上正是這個視線）（大街圖 `set-shiji-l1` 是菜市，兩塊招牌與掛牌有假字）。光：早上冷、午後暖、傍晚低低的橘光，s34 起最後一點夕照、門外轉藍（圖的亮度交給調色）。**要不要試鏡**：只有小金算盤的道具圖（建議做，2 支 Qwen）；其他都不用。",
    "- 長鏡要買的秒數（BUY）：照 38 句錄音核過（`~/mokaair-work/videos/zhong-tian-qu-qi-e920-dh/audio`，faster-whisper 一次一支逐句聽寫；見 `r2.py` 的 BUY 註解）：**s27（心裡話、系統、心裡話三句約 9.5 秒，一支裝得下、不拆）買 10 秒**；s04（二牛先扯紅布再喊約 6 秒）、s19（會長邊走邊說約 5.7 秒）、s28（說完還要蓋匣、撥珠）、s36（孫掌櫃慢條斯理約 6.9 秒、再側身）買 8 秒；其餘 6 秒，沒有台詞的 s15、s16、s37、s37b 照 gen-dh 的 5–6 秒。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音長度＋0.5 秒為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯、唐小棠（l1 交領）、秦霜、阿令（l1，高髻木簪）、小禾、二牛、孫掌櫃、魏少卿的 l1（含有的角度圖），會長 `hanghui-huizhang-portrait-l1`（extras.json 先用 `mianshiguan-portrait-t1` 佔位、spec 的 swap_pictures 換成會長）。場景見上面。",
    "- 共用檔：`writer-tools/e001-r2/build-r2.py` 的 `EN` 加 `weishaoqing`（Wei Shaoqing）、`hanghui`（the guild master）（聖經列過；兩人都在畫面上說話）；第 910–919 集逐位元重建相同。`gen-dh.mjs`、`pilot.py`、`cast.json` 不改（會長是 `r2.py` 的 `MINOR`，聲音 Fenrir）。",
    "- `colab/runs/e920/extras.json`（照 e919：畫面不放字幕、空氣清澈那句；拿掉秦霜的柴刀；魏少卿的外貌拿掉『嘴角總掛著輕蔑的笑』與手上的摺扇，笑與扇子由每鏡寫；會長的定妝照與外貌）與 `colab/runs/e920-live/spec.json`（`mkspec.py` 產生；種子 9201101／9201102）。",
    "- 免費準備：`prep920.sh`（`DRY=1 REFS=~/mokaair-work/videos/zhong-tian-qu-qi-e920-dh/runpod/refs-dh-e920 VIDEO_JSON=docs/videos/zhong-tian-qu-qi-e020-r2/video.json st1-ep.sh 920` → `pilot.py` → `retake.py` → `colab-jobs.json` 加 output_path、套 swap_pictures（絕對路徑）→ 逐鏡查送的場景圖與人物圖 → `preflight-prompts.py` → 否定名詞與會長字的名詞掃描）。",
    "- 配樂：屋頂接第 19 集的古箏（s01 一個暖的重音）；開張熱鬧的鑼鼓笛子，s15 馬車一個冷的低音、停兩拍，s19 起俏皮，s24 算珠一個重音；打烊前收工的暖曲，s34 起低沉的弦，s38 摺扇『唰』一個大重音後收。音效見 script.md〈音樂與音效〉（s36 摺扇只在音效）。",
]

# Long shots: seconds to buy. Measured 2026-11-16 against the 38 recordings (~/mokaair-work/videos/zhong-tian-qu-qi-e920-dh/audio;
# wave length and silencedetect -35 dB; e013's test: a shot holds (buy - 0.3) x 1.1 s of speech, half a second between lines,
# so 6 s holds 6.27 s, 8 s 8.47 s and 10 s 10.67 s). faster-whisper medium read every take back, one clip per process
# (scratchpad fw920.txt).
# 10 s: s27 (Xu Yan's thought a26 2.35 + the system a27 2.35 + his thought a28 3.83 + 2 x 0.5 = 9.53 s; one clip, no split).
# 8 s:  s04 (a04 6.02 s of speech after the red cloth comes down in the first second), s19 (a17 5.74 s while he walks in,
#       tucks the ledgers and bows), s28 (a29 5.21 s, then the lid closes and the last bead), s36 (a37 6.85 s of Sun
#       Zhanggui's slow drawl with its pause, then he steps aside).
# 6 s:  every other line (2.36-5.13 s of speech; the tightest s21 a19 5.13 s with the handkerchief during the line, s26 the
#       system's two lines 1.95 + 0.5 + 2.57 = 5.02 s). The silent shots s15, s16, s37, s37b take gen-dh's 5-6 s.
# Re-recorded once (audio/README-retakes.txt; first takes in audio/take1/): a08 (要 dropped), a32 (小棠 heard 小大), a34 (上門板
# heard 上門吧; the retake reads 稍門辦, 板 there): a human ear checks a34, a24 and a27 (system 宿主 heard 叔叔) before the cut.
# a37 opens with a short laugh not in the line (kept: 笑咪咪; s36 buys 8 s). The retakes are 3.72-4.28 s: 6 s holds them.
BUY = {"s04": 8, "s19": 8, "s27": 10, "s28": 8, "s36": 8}
